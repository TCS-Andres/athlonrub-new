"""
Athlon Rub - Lifestyle photography generation (nano-banana-pro via kie.ai)

Produces two sets of 12 square photographs:

    Set A  athletes/    12 athlete action shots, no product
    Set B  product/     12 of the same world with the product in frame

The brief is realism above everything: the output has to survive being placed
next to real reference photography without reading as generated. The prompt
architecture that serves that lives in _style.py (camera, light, grade, skin,
capture, negatives) and _scenes_product.py (SKU scale, label, integration).

USAGE
-----
    export KIE_API_KEY=...

    python3 "Lifestyle Photos/generate_lifestyle.py"              # all 24
    python3 "Lifestyle Photos/generate_lifestyle.py" A            # set A only
    python3 "Lifestyle Photos/generate_lifestyle.py" B            # set B only
    python3 "Lifestyle Photos/generate_lifestyle.py" A03 B07      # named shots
    python3 "Lifestyle Photos/generate_lifestyle.py" --prompts    # dry run

Reference bottle photographs are uploaded once to kie.ai's file host and the
resulting URLs cached in _refs.json, so reruns cost nothing extra.
"""
import base64
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _style
from _scenes_athletes import ATHLETES
from _scenes_product import (PRODUCTS, SKU, SCALE_BIAS, OIL, LABEL,
                             INTEGRATION, PRODUCT_BRANDING)

# ---------------------------------------------------------------------------
API_KEY = os.environ.get("KIE_API_KEY")
if not API_KEY:
    sys.exit("Set KIE_API_KEY. Get one at https://kie.ai/api-key")

CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
QUERY_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-base64-upload"
MODEL = "nano-banana-pro"

ASPECT = "1:1"
RESOLUTION = "2K"
FMT = "jpg"

# Cloudflare in front of the upload host rejects the default urllib UA.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
HEADERS = {"Authorization": f"Bearer {API_KEY}",
           "Content-Type": "application/json",
           "User-Agent": UA}

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
DIR_A = os.path.join(BASE, "athletes")
DIR_B = os.path.join(BASE, "product")
DIR_P = os.path.join(BASE, "_prompts")
REFS_CACHE = os.path.join(BASE, "_refs.json")
for d in (DIR_A, DIR_B, DIR_P):
    os.makedirs(d, exist_ok=True)

SOURCE = os.path.join(ROOT, "Product Photos", "New product photos")
SKU_FILES = {
    "100": os.path.join(SOURCE, "Athlon_Rub_100_ml_web_1400x.webp"),
    "250": os.path.join(SOURCE, "Athlon_Rub_250_ml_web_1200x.webp"),
    "500": os.path.join(SOURCE, "Athlon_Rub_500_ml_web_1200x.webp"),
}


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=HEADERS)
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode())


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode())


# ---------------------------------------------------------------------------
# Reference upload. The API takes image URLs, not local files, so each bottle
# photo goes up once and the URL is cached.
# ---------------------------------------------------------------------------
def upload_refs():
    cache = {}
    if os.path.exists(REFS_CACHE):
        cache = json.load(open(REFS_CACHE))
    for sku, path in SKU_FILES.items():
        if cache.get(sku):
            continue
        # webp uploads fine, but PNG is what the generator prefers as reference.
        png = os.path.join(DIR_P, f"_ref_{sku}.png")
        if not os.path.exists(png):
            os.system(f'sips -s format png "{path}" --out "{png}" >/dev/null 2>&1')
        data = base64.b64encode(open(png, "rb").read()).decode()
        res = post(UPLOAD_URL, {
            "base64Data": "data:image/png;base64," + data,
            "uploadPath": "images/athlon-rub",
            "fileName": f"athlon_rub_{sku}ml.png",
        })
        cache[sku] = res["data"]["downloadUrl"]
        print(f"  uploaded {sku} ml reference -> {cache[sku]}")
    json.dump(cache, open(REFS_CACHE, "w"), indent=2)
    return cache


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------
def build_jobs(refs):
    jobs = []
    for s in ATHLETES:
        jobs.append({
            "id": s["id"], "slug": s["slug"], "dir": DIR_A, "refs": [],
            "prompt": _style.build(s["scene"]),
        })
    for s in PRODUCTS:
        # Order matters. Scale and the scale-bias correction lead, because the
        # model anchors on whatever it reads first and the size error was the
        # loudest complaint. Then what the product actually is (an oil, not a
        # spray), then the label, then physical integration, then the scene.
        scene = (SKU[s["sku"]] + SCALE_BIAS + OIL + LABEL + INTEGRATION
                 + "THE SCENE: " + s["scene"])
        jobs.append({
            "id": s["id"], "slug": s["slug"], "dir": DIR_B,
            "refs": [refs[s["sku"]]],
            "prompt": _style.build(scene, branding=PRODUCT_BRANDING),
        })
    return jobs


# ---------------------------------------------------------------------------
# Submit / poll / download
# ---------------------------------------------------------------------------
def run_job(job):
    tag = f"{job['id']} {job['slug']}"
    payload = {"model": MODEL, "input": {
        "prompt": job["prompt"],
        "image_input": job["refs"],
        "aspect_ratio": ASPECT,
        "resolution": RESOLUTION,
        "output_format": FMT,
    }}
    # The API intermittently rejects a submission with "prompt cannot exceed
    # 5000 characters" on prompts that its siblings sail through at the same
    # length, so a rejection is retried once before it is believed.
    res = None
    for attempt in (1, 2, 3):
        try:
            res = post(CREATE_URL, payload)
        except Exception as e:
            if attempt == 3:
                return tag, f"submit failed: {e}"
            time.sleep(5)
            continue
        if res.get("code") == 200:
            break
        if attempt == 3:
            return tag, f"submit rejected: {res.get('msg')}"
        time.sleep(5)
    task_id = res["data"]["taskId"]

    deadline = time.time() + 900
    while time.time() < deadline:
        time.sleep(10)
        try:
            info = get(f"{QUERY_URL}?taskId={task_id}")["data"]
        except Exception:
            continue
        state = info.get("state")
        if state == "success":
            url = json.loads(info["resultJson"])["resultUrls"][0]
            out = os.path.join(job["dir"], f"{job['id']}_{job['slug']}.jpg")
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r, open(out, "wb") as f:
                f.write(r.read())
            kb = os.path.getsize(out) // 1024
            return tag, f"OK  {os.path.relpath(out, ROOT)}  ({kb} KB)"
        if state == "fail":
            return tag, f"FAILED  {info.get('failCode')} {info.get('failMsg')}"
    return tag, "timed out after 15 min"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--prompts" in sys.argv

    refs = {} if dry else upload_refs()
    if dry:
        refs = {k: "REF_URL" for k in SKU_FILES}
    jobs = build_jobs(refs)

    if args:
        wanted = {a.upper() for a in args}
        jobs = [j for j in jobs
                if j["id"] in wanted or j["id"][0] in wanted]
    if not jobs:
        sys.exit("Nothing matched. Use A, B, or ids like A03 B07.")

    # Always drop the exact prompts to disk - they are the real asset here,
    # and a shot that misses is re-run from an edited prompt, not from scratch.
    for j in jobs:
        with open(os.path.join(DIR_P, f"{j['id']}_{j['slug']}.txt"), "w") as f:
            f.write(j["prompt"])
    if dry:
        print(f"Wrote {len(jobs)} prompts to {os.path.relpath(DIR_P, ROOT)}")
        return

    print(f"Generating {len(jobs)} images at {RESOLUTION} {ASPECT} ...\n")
    done = 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(run_job, j): j for j in jobs}
        for fut in as_completed(futures):
            tag, msg = fut.result()
            done += 1
            print(f"[{done}/{len(jobs)}] {tag}: {msg}", flush=True)


if __name__ == "__main__":
    main()
