"""
Targeted Seedream 5.5 edits on an approved frame. Seedream 5.5 holds unedited
regions at pixel level, so fixing one flaw (a printed shirt, too much oil)
this way keeps the composition, faces and label that already passed QA.

    python3 edit.py            # runs every edit in EDITS
    python3 edit.py hero-desktop roster-combat

Input:  _raw/{name}_r{n}.png named in EDITS
Output: _raw/{name}_r{next}.png, prompt in _prompts/{name}__edit.txt
"""
import io
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as g

KEEP = (
    " Change nothing else: keep the exact same composition, framing, people, "
    "faces, hands, pose, lighting, colour grade, background, and keep the "
    "Athlon Rub bottle and its label exactly as they are."
)

EDITS = {
    "hero-desktop": ("hero-desktop_r1.png",
        "Edit this photograph. Remove the white printed lettering from the "
        "cornerman's black t-shirt sleeve and back so the shirt is plain, "
        "unprinted black cotton."),
    "roster-combat": ("roster-combat_r1.png",
        "Edit this photograph. Remove the printed lettering from the "
        "fighter's black shorts so they are plain, unprinted black satin."),
    "roster-endurance": ("roster-endurance_r1.png",
        "Edit this photograph. There is far too much oil on the runner's shin "
        "and calf: remove the amber streak and the wet look, leaving only a "
        "faint satin sheen on the calf muscle with the rest of the leg's skin "
        "dry and matte."),
    "use-performance": ("use-performance_r1.png",
        "Edit this photograph. Remove all printed lettering and graphics from "
        "the cornerman's black t-shirt (back and sleeve) and from the "
        "fighter's shorts waistband, leaving plain unprinted fabric."),
    "use-recovery": ("use-recovery_r1.png",
        "Edit this photograph. There is far too much oil on the woman's shin "
        "and calf: remove the glossy wet coating, leaving only a faint satin "
        "sheen on the calf muscle with the surrounding skin dry and matte."),
    "cta-locker": ("cta-locker_r1.png",
        "Edit this photograph. Remove the printed lettering from the boxer's "
        "shorts and top so they are plain, unprinted fabric."),
    "use-warmup": ("use-warmup_r1.png",
        "Edit the first image. The bottle's pump is wrong: replace only the "
        "pump head with the one on the bottle in the second image, a short "
        "black cylindrical treatment pump with a tiny round nozzle, no long "
        "curved lotion spout. Keep the short ribbon of amber oil falling from "
        "that nozzle into his cupped palm. Also remove the oil sheen from his "
        "forearm and wrist so that arm is dry and matte.", ["250"]),
}


def upload_jpeg(path, name):
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=95)
    data = buf.getvalue()
    import base64
    res = g.post(g.UPLOAD_URL, {"base64Data": "data:image/jpeg;base64," + base64.b64encode(data).decode(),
                                "uploadPath": "images/athlon-rub-v3-edits", "fileName": name})
    return res["data"]["downloadUrl"], im.size


def ratio_for(size):
    w, h = size
    r = w / h
    options = {"1:1": 1, "4:3": 4/3, "3:4": 3/4, "16:9": 16/9, "9:16": 9/16,
               "2:3": 2/3, "3:2": 3/2, "21:9": 21/9}
    return min(options, key=lambda k: abs(options[k] - r))


def run(name):
    src, instr, *extra = EDITS[name]
    url, size = upload_jpeg(os.path.join(g.RAW, src), f"{name}_src.jpg")
    refs = g.refs()
    urls = [url] + [refs[k] for k in (extra[0] if extra else [])]
    prompt = instr + KEEP
    open(os.path.join(g.PROMPTS, f"{name}__edit.txt"), "w").write(prompt)
    payload = {"model": g.I2I, "input": {"prompt": prompt, "image_urls": urls,
               "aspect_ratio": ratio_for(size), "size": "2K", "output_format": "png"}}
    res = g.post(g.CREATE_URL, payload)
    if res.get("code") != 200:
        return name, f"rejected {res.get('code')} {res.get('msg')}"
    task = res["data"]["taskId"]
    for _ in range(110):
        time.sleep(8)
        try:
            info = g.get(f"{g.QUERY_URL}?taskId={task}")["data"]
        except Exception:
            continue
        if info.get("state") == "success":
            u = json.loads(info["resultJson"])["resultUrls"][0]
            out = g.next_path(name)
            req = urllib.request.Request(u, headers={"User-Agent": g.UA})
            open(out, "wb").write(urllib.request.urlopen(req, timeout=300).read())
            return name, "OK " + os.path.basename(out)
        if info.get("state") == "fail":
            return name, f"FAILED {info.get('failMsg')}"
    return name, "timeout"


if __name__ == "__main__":
    names = sys.argv[1:] or list(EDITS)
    with ThreadPoolExecutor(6) as p:
        for n, msg in p.map(run, names):
            print(n, msg, flush=True)
