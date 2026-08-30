"""
Athlon Rub — Flat Brand Element System (v2)

WHY THIS EXISTS
---------------
The v1 elements (01-10 in this folder) were rendered as beveled, drop-shadowed,
metallic "trophy shop" graphics. That treatment contradicts the official logo
sheet ("New Logo Athlon Rub Cinturon.pdf"), whose USOS NO PERMITIDOS panel
explicitly forbids "No aplicar efectos", and it does not match the bottle
label, where every icon is flat, solid, single-color gold.

v2 rebuilds the system flat, on the official palette, and extends it from
10 decorative accents to a full website icon set: crest system + benefit
icons + persona icons.

OFFICIAL PALETTE (sampled from the logo sheet, PALETA PRINCIPAL):
    green  #0F2B1E      gold   #D4AF37      black  #0A0A0A

TECHNIQUE
---------
Follows ELEMENT_GENERATION_GUIDE.md verbatim:
  1) Generate on solid pure black (never ask for "transparent background").
  2) Recover true alpha via max(R,G,B) + un-premultiply.
  3) Auto-crop to the alpha bbox.
Then, because the art is flat single-color, derive green / cream / white
colorways by swapping RGB and keeping alpha.

USAGE
-----
    export KIE_API_KEY=...
    python3 "Brand Elements/generate_flat_system.py"            # everything
    python3 "Brand Elements/generate_flat_system.py" 01 02 11   # subset (pilot)
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from PIL import Image

API_KEY = os.environ.get("KIE_API_KEY")
if not API_KEY:
    sys.exit("Set KIE_API_KEY in your environment. Get one at https://kie.ai/api-key")

CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
QUERY_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
MODEL = "nano-banana-pro"

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "system-v2")
DIR_GOLD = os.path.join(OUT, "gold")
DIR_RAW = os.path.join(OUT, "_raw")
DIR_QA = os.path.join(OUT, "_qa")
for d in (DIR_GOLD, DIR_RAW, DIR_QA):
    os.makedirs(d, exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Public URL of the existing crest extraction. Used ONLY as a silhouette
# reference for crest-derived marks; the prompt overrides its finish to flat.
CREST_REF = ("https://raw.githubusercontent.com/TCS-Andres/athlonrub/main/"
             "Brand%20Elements/00_logo_shield.png")

# ---------------------------------------------------------------------------
# Shared prompt blocks
# ---------------------------------------------------------------------------
GOLD = ("ONE single flat solid GOLD color, exactly #D4AF37, filled uniformly "
        "across the entire mark with absolutely no variation in tone")

# The load-bearing style block. Every clause is preventing a specific failure
# mode seen in v1: bevels, gradients, cast shadows, faux-metal sheen.
FLAT = (
    # Background first and loudest: v2 pilot showed the model defaults to a
    # white icon-sheet look when "flat vector icon" leads the prompt.
    "BACKGROUND, THIS IS THE MOST IMPORTANT REQUIREMENT: the artwork sits on a "
    "UNIFORM SOLID PURE BLACK (#000000) backdrop that fills the entire canvas "
    "edge to edge. The background is BLACK. The background is NOT white. DO "
    "NOT use a white background. DO NOT place the artwork on a white sheet, a "
    "white card, a white page, a white tile, or a white rounded square. DO NOT "
    "draw a checkered transparency-indicator pattern. DO NOT draw light gray "
    "and dark gray alternating squares. DO NOT draw any pattern, gradient, "
    "texture, vignette, frame, or border in the background. Flat, opaque, "
    "photographic black, exactly like a product shot taken against a black "
    "studio sweep. EVERY part of the canvas that is not the gold artwork is "
    "pure black, including any area enclosed inside or between parts of the "
    "artwork. The gold artwork is the only thing on the canvas besides flat "
    "black, isolated and centered with a generous black margin around it. "
    "STYLE: a flat vector mark in the Athlon Rub brand system. Rendered "
    "COMPLETELY FLAT in a single solid color: NO gradient, NO bevel, NO "
    "emboss, NO drop shadow, NO cast shadow, NO glow, NO outer stroke, NO 3D "
    "extrusion, NO metallic sheen, NO reflections, NO highlights, NO shading, "
    "NO texture, NO noise. The shape is defined purely by its silhouette. "
    "Bold, confident, geometric athletic-emblem construction with crisp clean "
    "edges and even, generous weight so the mark stays legible at 24 pixels. "
    "Modern sports-crest iconography with the precision of a championship "
    "belt buckle and a professional sports club badge. Not cartoon, not "
    "hand-drawn, not sketchy, not photorealistic, not an app-store app icon. "
    "No text, no letters, no captions, no labels, no numbers anywhere."
)

# Appended to EVERY prompt. Recency matters: without this tail the model
# still slipped to a white background on roughly a third of the batch.
BLACK_TAIL = (
    " FINAL REMINDER, DO NOT IGNORE: the entire background of this image is "
    "SOLID PURE BLACK (#000000). It is not white. It is not light gray. It is "
    "not a white studio backdrop. Fill every pixel that is not gold artwork "
    "with pure black."
)

# Precise description of the crest silhouette, transcribed from the logo sheet.
CREST_SHAPE = (
    "the exact Athlon Rub crest silhouette, which is a Muay Thai championship "
    "belt-buckle shield: a tall pointed gothic arch at the top center, "
    "flanked on each side by a symmetrical concave ogee scroll notch that "
    "dips inward and then rises into a small rounded shoulder peak; from "
    "those shoulders the two outer sides sweep down and curve inward, "
    "narrowing to a softly pointed base at the bottom center"
)

REF_NOTE = (
    "A reference image of the crest is provided. Copy its OUTLINE and "
    "PROPORTIONS exactly. IGNORE its finish completely: the reference has a "
    "metallic gradient and beveled edges, and your version must have neither. "
    "Reproduce the shape only, rendered dead flat in one solid color."
)

# ---------------------------------------------------------------------------
# The element set
# ---------------------------------------------------------------------------
ELEMENTS = [
    # ---- TIER 1: crest system -------------------------------------------
    dict(
        id="01", name="01_crest_outline", ar="4:5", ref=True,
        use="Product card frames, badge containers, avatar frames",
        prompt=(
            f"An EMPTY crest frame drawn as a clean uniform-width outline in {GOLD}. "
            f"The outline traces {CREST_SHAPE}. "
            "The stroke is a single consistent thickness the whole way around, "
            "roughly one twelfth of the crest's width. CRITICAL: the entire "
            "area enclosed inside the outline is PURE BLACK background showing "
            "straight through, completely empty. There is NO star, NO letter, "
            "NO chevron, NO A shape, NO crescent, NO green fill and NO gold "
            "fill anywhere inside the crest. Only the thin gold outline itself "
            "is drawn. It is a hollow ring, like a cookie cutter, so that other "
            "content can later be placed within it. Upright and centered. "
            f"{REF_NOTE} {FLAT}"
        ),
    ),
    dict(
        id="02", name="02_crest_solid", ar="4:5", ref=True,
        use="Solid badge, favicon base, stamp, seal",
        prompt=(
            f"A solid filled crest shape in {GOLD}, with no interior detail at all. "
            f"The silhouette is {CREST_SHAPE}. "
            "A single unbroken solid gold shape, like a die-cut sticker of the "
            "crest. Upright and centered. "
            f"{REF_NOTE} {FLAT}"
        ),
    ),
    dict(
        id="03", name="03_star_excellence", ar="1:1", ref=False,
        use="Star ratings, credential badges, step numbers, list bullets",
        prompt=(
            f"A single bold five-pointed star in {GOLD}, solid filled, centered, "
            "sitting upright with one point straight up. Sharp clean tips, "
            "classic athletic proportions with slightly stout points rather "
            "than thin spindly ones. This is the excellence star from the "
            "center of the Athlon Rub crest, isolated as a standalone mark. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="04", name="04_apex_monogram", ar="1:1", ref=False,
        use="Brand mark in cards, section anchors, watermark",
        prompt=(
            f"A single bold angular letter A in {GOLD}, and NOTHING else. "
            "It is built as a steep inverted V like a mountain peak: two thick "
            "straight legs meeting at a sharp point at the top, joined by a "
            "straight horizontal crossbar near the bottom, with flat angled "
            "cuts at the feet of both legs. It reads at once as the letter A "
            "and as a summit. Solid filled, symmetrical, geometric, athletic. "
            "CRITICAL: draw ONLY this A shape. There is NO shield, NO crest, "
            "NO badge, NO star, NO circle, NO frame and NO outline around it. "
            "The A stands completely alone on the black background. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="05", name="05_chevron_ascend", ar="1:1", ref=False,
        use="Superacion attribute, scroll-to-top, progress markers",
        prompt=(
            f"TWO nested chevrons in {GOLD}, both pointing straight UP, stacked "
            "one directly above the other with an even gap between them, the "
            "upper one identical in size to the lower one. Each chevron is a "
            "clean angular caret with a uniform thick stroke and flat cut "
            "ends. This is the SUPERACION mark from the Athlon Rub brand "
            "attribute row. Symmetrical and centered. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="06", name="06_chevron_forward", ar="16:9", ref=False,
        use="CTAs, forward motion, carousel arrows, FAQ toggles",
        prompt=(
            f"THREE chevrons in {GOLD}, all pointing to the RIGHT, arranged in a "
            "horizontal row with even gaps between them, all three the same "
            "size. Each chevron is a clean angular caret with a uniform thick "
            "stroke and flat cut ends, suggesting speed and forward momentum. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="07", name="07_support_rules", ar="21:9", ref=False,
        use="Wordmark support lines, thin section rules, caption flanks",
        prompt=(
            f"Exactly TWO shapes in {GOLD} on an otherwise empty canvas: a long "
            "slender horizontal wedge on the far left, and its mirror image on "
            "the far right. Each wedge is thickest at the outer edge of the "
            "canvas and tapers steadily inward to a fine needle point, like a "
            "stretched spear or a very long thin triangle lying on its side. "
            "The two needle points face each other but DO NOT meet: a wide "
            "empty black gap spanning the middle third of the canvas separates "
            "them, and that gap stays completely empty. Both wedges sit on the "
            "same horizontal centre line and are perfectly mirrored. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="08", name="08_laurel_open", ar="1:1", ref=False,
        use="Heritage band, awards, testimonial framing",
        prompt=(
            f"An open laurel wreath in {GOLD}: two symmetrical curved branches "
            "of pointed leaves rising from a crossed base at the bottom, "
            "sweeping up and around to form a circle that stays OPEN at the "
            "top with a clear gap between the two upper tips. Each leaf is a "
            "simple solid pointed oval. Clean, geometric, evenly spaced "
            "leaves, flat and graphic rather than ornate or botanical. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="09", name="09_ribbon_banner", ar="16:9", ref=False,
        use="'Best value' / 'Most popular' product labels",
        prompt=(
            f"A horizontal ribbon banner in {GOLD}, solid filled: a wide "
            "rectangular center panel that dips in a gentle downward curve, "
            "with a short angled tail folding back at each end, each tail cut "
            "with a notched V at its outer edge. The banner is empty with no "
            "writing on it. Simple, bold, symmetrical, graphic. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="10", name="10_star_rule_divider", ar="21:9", ref=False,
        use="Section dividers between content blocks",
        prompt=(
            f"A horizontal section divider in {GOLD}: one small solid five-pointed "
            "star centered in the middle of the canvas, with a long slender "
            "tapered rule extending horizontally to the left and another to "
            "the right, each rule thickest where it meets the star and "
            "tapering to a fine point at its far outer end. Perfectly "
            "horizontal, symmetrical. "
            f"{FLAT}"
        ),
    ),

    # ---- TIER 2: benefit / product icons ---------------------------------
    dict(
        id="11", name="11_fast_absorbing", ar="1:1", ref=False,
        use="'Absorbs in about a minute' benefit callout",
        prompt=(
            f"An icon in {GOLD} of a single teardrop-shaped liquid droplet, point "
            "facing up, with THREE short horizontal speed lines trailing "
            "behind it on its left side, the middle line longest. The droplet "
            "is solid filled; the speed lines are simple thick rounded bars. "
            "Communicates a liquid that absorbs quickly. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="12", name="12_warming", ar="1:1", ref=False,
        use="Warming-sensation benefit callout",
        prompt=(
            f"An icon in {GOLD} of THREE rising heat waves: three vertical wavy "
            "lines side by side, each an even thick S-curve ribbon with "
            "rounded ends, the center one taller than the two flanking it. "
            "Clean geometric waves with consistent stroke width, evenly "
            "spaced. Communicates gentle rising warmth. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="13", name="13_non_greasy", ar="1:1", ref=False,
        use="'Non-greasy, will not transfer to clothing' callout",
        prompt=(
            f"An icon in {GOLD} of a simple t-shirt seen flat from the front, "
            "drawn as a clean uniform-width outline with short sleeves and a "
            "round neckline, with a single small solid teardrop droplet "
            "positioned just above the shirt and a short curved line beneath "
            "the droplet indicating it is being repelled and not soaking in. "
            "Communicates a liquid that does not stain fabric. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="14", name="14_botanical_leaf", ar="1:1", ref=False,
        use="Natural / herbal ingredients, paraben-free chips",
        prompt=(
            f"An icon in {GOLD} of a single leaf, solid filled, pointing up and "
            "tilted slightly to the right, with a pointed tip and a rounded "
            "base, and a narrow negative-space center vein running its full "
            "length with two or three short negative-space side veins "
            "branching off. Simple, bold, graphic. This is the natural "
            "ingredients leaf from the Athlon Rub bottle label. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="15", name="15_lab_certified", ar="1:1", ref=False,
        use="FDA-registered / ISO / GMP certified-lab credentials",
        prompt=(
            f"An icon in {GOLD} of a laboratory flask: a conical Erlenmeyer flask "
            "with a narrow straight neck and a wide triangular body, drawn as "
            "a clean uniform-width outline, with a solid horizontal band "
            "across the lower third of the body representing liquid, and two "
            "small solid circles floating above it inside the flask. "
            "Communicates certified laboratory manufacturing. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="16", name="16_tested_clean", ar="1:1", ref=False,
        use="'Tested clean, free of banned substances' credential",
        prompt=(
            f"A solid filled heraldic shield in {GOLD} with flat top corners, "
            "straight sides and a rounded point at the bottom. A bold "
            "checkmark is CUT OUT of the middle of the shield as empty "
            "negative space: the checkmark itself is PURE BLACK, showing the "
            "background straight through the gold shield, like a stencil or a "
            "die-cut. The checkmark is a thick two-stroke tick with flat cut "
            "ends, a short stroke down to the left and a long stroke up to the "
            "right, centred and fully surrounded by gold without touching the "
            "shield edges. Only two tones exist in this image: gold and black. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="17", name="17_heritage_motif", ar="16:9", ref=False,
        use="Thai heritage band, story sections, ornamental divider",
        prompt=(
            f"A symmetrical ornamental divider motif in {GOLD} inspired by "
            "traditional Thai temple gable ornament: a central upward-pointing "
            "flame-like spire with two mirrored curling scroll tendrils "
            "sweeping outward and downward from its base, each tendril "
            "tapering to a fine curled tip. Elegant, geometric, evenly "
            "balanced, reduced to clean simple shapes rather than intricate "
            "filigree. Horizontal composition, centered. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="18", name="18_spray_bottle", ar="1:1", ref=False,
        use="How-to-use steps, product/format indicator",
        prompt=(
            f"An icon in {GOLD} of a spray bottle seen from the front, drawn as a "
            "clean uniform-width outline: a tall rounded-rectangle bottle body, "
            "a short narrow shoulder, and a pump spray cap on top with a small "
            "nozzle projecting to the upper right, plus three short straight "
            "spray lines fanning out from the nozzle. A plain solid label band "
            "crosses the middle of the bottle body with nothing written on it. "
            f"{FLAT}"
        ),
    ),

    # ---- TIER 3: persona icons -------------------------------------------
    dict(
        id="19", name="19_persona_combat", ar="1:1", ref=False,
        use="Persona 01 — Combat Sports",
        prompt=(
            f"A solid filled silhouette in {GOLD} of a single Muay Thai fighter "
            "standing in a fighting stance seen from the side, both fists "
            "raised guarding the face, one knee lifted in a knee strike, body "
            "leaning slightly forward, wearing shorts and hand wraps. One "
            "clean solid shape with no interior lines, like a pictogram on a "
            "sports sign. Athletic, dynamic, confident. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="20", name="20_persona_endurance", ar="1:1", ref=False,
        use="Persona 02 — Soccer & Endurance",
        prompt=(
            f"A solid filled silhouette in {GOLD} of a single runner sprinting to "
            "the right, seen from the side, leaning forward with one leg "
            "extended far forward and the other driving back, both arms "
            "pumping. One clean solid shape with no interior lines, like a "
            "pictogram on a sports sign. This is the running figure from the "
            "Athlon Rub bottle label. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="21", name="21_persona_lifting", ar="1:1", ref=False,
        use="Persona 03 — Hyrox & Lifting",
        prompt=(
            f"An icon in {GOLD} of a barbell seen from the front: a long straight "
            "horizontal bar with two solid weight plates stacked at each end, "
            "a large plate outermost and a smaller collar plate inside it, "
            "perfectly symmetrical. Solid filled, bold and simple. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="22", name="22_persona_paddle", ar="1:1", ref=False,
        use="Persona 04 — Pickleball & Paddle",
        prompt=(
            f"An icon in {GOLD} of a pickleball paddle standing upright with its "
            "handle at the bottom, drawn as a clean uniform-width outline with "
            "a rounded-rectangle face and a short grip wrapped by two bands. "
            "To the lower right of the paddle, clearly separated from it with "
            "black space between, sits one small ball drawn as a circle "
            "outline with seven small round holes cut into it. The ball is "
            "about one quarter the height of the paddle and does not touch or "
            "overlap the paddle. Simple, bold, evenly balanced. "
            f"{FLAT}"
        ),
    ),
    dict(
        id="23", name="23_persona_therapist", ar="1:1", ref=False,
        use="Persona 05 — Therapists & Bodyworkers",
        prompt=(
            f"An icon in {GOLD} of a pair of open hands seen from above, side by "
            "side and slightly overlapping, fingers pointing up and away, in "
            "the position of a therapist applying pressure. Drawn as clean "
            "solid filled shapes with narrow negative-space gaps separating "
            "the fingers. Calm, capable, professional. CRITICAL: the pair of "
            "hands is the ONLY artwork in the image. There are no extra "
            "shapes, no partial shapes, no faint marks and no cropped objects "
            "above, below, or beside the hands. "
            f"{FLAT}"
        ),
    ),
]

# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def http_post(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def http_get(url):
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def download(url, path):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "image/png,image/*,*/*"})
    with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
        f.write(r.read())


def submit(el):
    body = {
        "model": MODEL,
        "input": {
            "prompt": el["prompt"] + BLACK_TAIL,
            "image_input": [CREST_REF] if el.get("ref") else [],
            "aspect_ratio": el["ar"],
            "resolution": "2K",
            "output_format": "png",
        },
    }
    r = http_post(CREATE_URL, body)
    if r.get("code") != 200:
        raise RuntimeError(f"submit failed for {el['name']}: {r}")
    tid = r["data"]["taskId"]
    print(f"  submitted {el['name']:26s} taskId={tid}", flush=True)
    return el["name"], tid


def poll_and_download(name, tid, max_wait=900):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        info = http_get(f"{QUERY_URL}?taskId={tid}")
        data = info.get("data", {})
        state = data.get("state")
        if state == "success":
            result = json.loads(data["resultJson"])
            raw = os.path.join(DIR_RAW, f"{name}.png")
            download(result["resultUrls"][0], raw)
            print(f"  downloaded {name}", flush=True)
            return raw
        if state == "fail":
            raise RuntimeError(
                f"{name} failed: {data.get('failCode')} {data.get('failMsg')}")
        time.sleep(8)
    raise TimeoutError(f"{name} timed out")


# ---------------------------------------------------------------------------
# Alpha extraction (ELEMENT_GENERATION_GUIDE.md pipeline)
# ---------------------------------------------------------------------------
LOW, HIGH = 35, 70
ALPHA_CROP_THRESHOLD = 25
PAD_RATIO = 0.04
GOLD_RGB = (0xD4, 0xAF, 0x37)


def _corner_mean(arr):
    h, w, _ = arr.shape
    k = max(8, min(h, w) // 60)
    corners = np.concatenate([
        arr[:k, :k].reshape(-1, 3), arr[:k, -k:].reshape(-1, 3),
        arr[-k:, :k].reshape(-1, 3), arr[-k:, -k:].reshape(-1, 3)])
    return corners.mean(axis=0)


def black_to_alpha(in_path, out_path):
    """Recover true alpha, then repaint the art in exact brand gold.

    Nano Banana honours the black-backdrop instruction most of the time but
    not always, so both backdrops are handled. Because every mark in this
    system is flat single-colour by design, the recovered alpha is composited
    against a hard #D4AF37 fill: that removes the faint tonal drift the model
    leaves in large solid areas and guarantees exact palette compliance.
    """
    arr = np.array(Image.open(in_path).convert("RGB")).astype(np.float32)

    if _corner_mean(arr).max() > 128:
        # Light backdrop: ink coverage from the blue channel, where flat gold
        # (B=55) is furthest from white (B=255).
        alpha = (255.0 - arr[..., 2]) * (255.0 / (255.0 - GOLD_RGB[2]))
        alpha = np.where(alpha <= 12, 0.0, alpha)
    else:
        # Black backdrop: the documented max(R,G,B) three-zone ramp.
        brightness = np.max(arr, axis=2)
        alpha = np.where(
            brightness <= LOW, 0.0,
            np.where(brightness >= HIGH, brightness,
                     brightness * (brightness - LOW) / (HIGH - LOW)))
    alpha = np.clip(alpha, 0, 255)

    rgb = np.empty(arr.shape, dtype=np.float32)
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = GOLD_RGB
    rgba = np.dstack([rgb, alpha]).astype(np.uint8)

    mask = alpha > ALPHA_CROP_THRESHOLD
    if mask.any():
        rows, cols = np.any(mask, axis=1), np.any(mask, axis=0)
        y0, y1 = np.where(rows)[0][[0, -1]]
        x0, x1 = np.where(cols)[0][[0, -1]]
        h, w = rgba.shape[:2]
        pad = int(min(h, w) * PAD_RATIO)
        rgba = rgba[max(0, y0 - pad):min(h, y1 + 1 + pad),
                    max(0, x0 - pad):min(w, x1 + 1 + pad)]
    Image.fromarray(rgba).save(out_path, "PNG", optimize=True)


# ---------------------------------------------------------------------------
# QA composite — official palette
# ---------------------------------------------------------------------------
GREEN = (0x0F, 0x2B, 0x1E)
CREAM = (0xEA, 0xE9, 0xCB)


def qa(rgba_path, qa_path):
    fg = Image.open(rgba_path).convert("RGBA")
    w, h = fg.size
    sheet = Image.new("RGB", (w * 2, h), GREEN)
    sheet.paste(Image.new("RGB", (w, h), CREAM), (w, 0))
    sheet.paste(fg, (0, 0), fg)
    sheet.paste(fg, (w, 0), fg)
    sheet.save(qa_path, "PNG", optimize=True)


# ---------------------------------------------------------------------------
def reprocess():
    import glob
    names = [os.path.basename(f)[:-4]
             for f in sorted(glob.glob(os.path.join(DIR_RAW, "*.png")))]
    for name in names:
        gold = os.path.join(DIR_GOLD, f"{name}.png")
        black_to_alpha(os.path.join(DIR_RAW, f"{name}.png"), gold)
        qa(gold, os.path.join(DIR_QA, f"{name}.png"))
        print(f"  {name:26s} {os.path.getsize(gold)//1024:5d} KB", flush=True)
    print(f"\nreprocessed {len(names)} element(s)")
    return 0


def main():
    if "--reprocess" in sys.argv:
        return reprocess()
    wanted = set(sys.argv[1:])
    els = [e for e in ELEMENTS if not wanted or e["id"] in wanted]
    print(f"submitting {len(els)} element(s) to {MODEL}...", flush=True)

    subs = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for fut in as_completed([ex.submit(submit, e) for e in els]):
            subs.append(fut.result())

    print("\npolling...", flush=True)
    raws, failures = {}, []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(poll_and_download, n, t): n for n, t in subs}
        for fut in as_completed(futs):
            n = futs[fut]
            try:
                raws[n] = fut.result()
            except Exception as e:
                print(f"  FAILED {n}: {e}", flush=True)
                failures.append(n)

    print("\nextracting alpha...", flush=True)
    for name, raw in sorted(raws.items()):
        gold = os.path.join(DIR_GOLD, f"{name}.png")
        black_to_alpha(raw, gold)
        qa(gold, os.path.join(DIR_QA, f"{name}.png"))
        print(f"  {name:26s} {os.path.getsize(gold)//1024:5d} KB", flush=True)

    print(f"\n{len(raws)}/{len(els)} ready -> {DIR_GOLD}")
    if failures:
        print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
