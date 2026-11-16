"""
Athlon Rub site v3 imagery, Seedream 5.5 via the Kie.ai task API.

The brief lives in site/docs/imagery-spec.md. This file turns it into prompts.

Seedream 5.5 caps prompts at 5,000 characters, so the long blocks from the
earlier nano-banana-pro pipeline (_style.py, _scenes_product.py) are carried
over in compressed form. Every clause still names a specific failure mode the
earlier rounds hit: oversized bottles, spray mist, varnished skin, invented
label type, derelict gyms, AI skin.

USAGE (run with /usr/bin/python3, which has Pillow)
    python3 generate.py hero-desktop product-stage   # named shots
    python3 generate.py --all                         # every shot
    python3 generate.py --prompts hero-desktop        # write prompts only, no cost

Each run writes the exact prompt to _prompts/{name}.txt and the raw PNG to
_raw/{name}_r{n}.png (n increments, nothing is overwritten).
"""
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "_raw")
PROMPTS = os.path.join(HERE, "_prompts")
REFS_CACHE = os.path.join(HERE, "_refs.json")
for d in (RAW, PROMPTS):
    os.makedirs(d, exist_ok=True)


def _key():
    with open(os.path.join(ROOT, ".env")) as f:
        for line in f:
            if line.startswith("KIE_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("KIE_API_KEY missing from .env")


UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
CREATE_URL = "https://api.kie.ai/api/v1/jobs/createTask"
QUERY_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"
CREDIT_URL = "https://api.kie.ai/api/v1/chat/credit"
UPLOAD_URL = "https://kieai.redpandaai.co/api/file-base64-upload"
T2I = "seedream/5-5-text-to-image"
I2I = "seedream/5-5-image-to-image"


def _headers():
    return {"Authorization": f"Bearer {_key()}", "Content-Type": "application/json",
            "User-Agent": UA}


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=_headers())
    return json.loads(urllib.request.urlopen(req, timeout=180).read().decode())


def get(url):
    req = urllib.request.Request(url, headers=_headers())
    return json.loads(urllib.request.urlopen(req, timeout=120).read().decode())


def credits():
    return get(CREDIT_URL)["data"]


# ---------------------------------------------------------------------------
# Reference bottles. Real 2026-label pack shots, uploaded once, cached for
# 2.5 days (Kie temp files expire after 3).
# ---------------------------------------------------------------------------
SOURCE = os.path.join(ROOT, "Product Photos", "New product photos")
SKU_FILES = {
    "100": os.path.join(SOURCE, "Athlon_Rub_100_ml_web_1400x.webp"),
    "250": os.path.join(SOURCE, "Athlon_Rub_250_ml_web_1200x.webp"),
    "500": os.path.join(SOURCE, "Athlon_Rub_500_ml_web_1200x.webp"),
}


def upload_png(path, name):
    data = base64.b64encode(open(path, "rb").read()).decode()
    res = post(UPLOAD_URL, {"base64Data": "data:image/png;base64," + data,
                            "uploadPath": "images/athlon-rub-v3", "fileName": name})
    return res["data"]["downloadUrl"]


def refs():
    cache = json.load(open(REFS_CACHE)) if os.path.exists(REFS_CACHE) else {}
    fresh = time.time() - cache.get("_t", 0) < 2.5 * 86400
    if fresh and all(k in cache for k in SKU_FILES):
        return cache
    cache = {"_t": time.time()}
    for sku, path in SKU_FILES.items():
        png = os.path.join(PROMPTS, f"_ref_{sku}.png")
        if not os.path.exists(png):
            subprocess.run(["sips", "-s", "format", "png", path, "--out", png],
                           capture_output=True, check=True)
        cache[sku] = upload_png(png, f"athlon_rub_{sku}ml_ref.png")
    json.dump(cache, open(REFS_CACHE, "w"), indent=2)
    return cache


# ---------------------------------------------------------------------------
# Shared blocks
# ---------------------------------------------------------------------------
LOOK = (
    "LOOK: a real campaign photograph for a premium athletic brand, shot on an "
    "ARRI Alexa 35 with a cinema prime, never stock, never a render. One "
    "motivated warm key light, a thin separating rim, and deep unlit shadow "
    "that falls to a true black. Genuinely shallow depth of field with smooth "
    "natural falloff and soft, un-busy bokeh. GRADE: shadows sit in deep "
    "forest green (never teal, never blue), highlights are warm amber and "
    "gold, skin stays true to life, everything else low in saturation. Fine "
    "organic film grain, gentle lens vignetting, highlights that roll off "
    "softly. No HDR, no golden-hour sunbeams, no haze machine, no lens flare, "
    "no orange-and-teal push. "
)

STILL_LOOK = (
    "LOOK: a high-end commercial still life, shot on a medium-format camera "
    "with a 120mm macro lens, like a premium spirits or fragrance campaign. "
    "One warm key, a thin gold rim, deep shadow falling to true black. "
    "Background is a deep forest-green to black falloff. Real materials: "
    "honed stone with fine pitting, real plant matter with natural flaws. "
    "Fine grain, no CGI gloss, no floating particles, no lens flare. "
)

PEOPLE = (
    "REAL PEOPLE: visible pores, fine hair, uneven skin tone, small scars and "
    "blemishes, veins standing up from exertion, faces that are not "
    "symmetrical. Sweat obeys gravity. Fabric creases and darkens where damp; "
    "wraps and kit are genuinely worn. The facility is current, clean and well "
    "maintained: taut canvas, tight ropes, swept floors, equipment racked. "
    "Never peeling paint, rust, grime or a derelict-warehouse look. Reportage "
    "framing, caught mid-action, nobody posing for the lens. "
)

SKU = {
    "100": (
        "the Athlon Rub 100 ml bottle from the attached reference: a squat amber "
        "translucent PET bottle with a black pump and a smoke-tinted over-cap. "
        "SMALL: 135 mm tall, 46 mm wide, shorter than a smartphone; a closed "
        "hand hides almost all of it. "
    ),
    "250": (
        "the Athlon Rub 250 ml bottle from the attached reference: a slim amber "
        "translucent PET cylinder with a black pump and a clear over-cap. "
        "MID-SIZE: 195 mm tall, 52 mm wide, about 1.3 smartphone lengths; a hand "
        "around its middle covers half its height. "
    ),
    "500": (
        "the Athlon Rub 500 ml bottle from the attached reference: an amber "
        "boston-round bottle with a sloping shoulder and a black ribbed screw "
        "cap, NO pump. 210 mm tall, 82 mm wide, a full hand to wrap around it, "
        "never a salon jug. "
    ),
}

SCALE = (
    "SIZE: generated shots always render this bottle too large. Err small. If "
    "it looks imposing next to a hand, glove, bench or bag, it is wrong. "
)

LABEL = (
    "LABEL, HIGHEST PRIORITY: copy the label from the reference exactly, same "
    "artwork, layout, wording and colours, no redesign. A matte bright WHITE "
    "wrap label across the middle of the bottle. Top to bottom: a pointed "
    "heraldic SHIELD crest (notched crown, point at the bottom, never round) "
    "in deep forest green outlined in gold with a gold diagonal band and a "
    "star; the wordmark ATHLON in large dark green slanted capitals with RUB "
    "small and letterspaced beneath, flanked by thin gold rules; ALL - SPORTS "
    "RUB in small letterspaced capitals; a dark green and black band at the "
    "bottom with tiny gold icons. Only the shield, ATHLON, RUB and ALL - "
    "SPORTS RUB are legible; finer type softens into printed texture. Never "
    "invent words. "
)

INTEGRATION = (
    "The bottle is a real object in the room: it rests on the surface with a "
    "soft contact shadow and its highlights match the scene's key light. Light "
    "from behind passes through the amber plastic so the oil glows warm like "
    "liquid gold on the lit side and turns deep brown on the shadow side. That "
    "is transmitted light, never an internal lamp; the bottle lights nothing "
    "around it. It must not look composited, pasted in, floating or lit by a "
    "separate studio light. "
)

OIL = (
    "THE PRODUCT IS AN OIL, NOT A SPRAY: a dense amber oil the pump pushes out "
    "slowly into the palm. Never a spray cone, mist or airborne droplets. USE "
    "VERY LITTLE: a coin-sized amount. On skin it is already rubbed in, just a "
    "light satin sheen along the muscle belly while the surrounding skin stays "
    "matte. Never a syrupy, varnished or glazed slick, never running, dripping "
    "or pooling. The action is the rub: flat palm, heel of the hand or thumb "
    "pressing in, skin visibly dragging under the pressure. "
)

NEGATIVE = (
    "Must never read as AI, CGI or illustration: no plastic or poreless skin, "
    "no symmetrical doll faces, no over-sharpened halos, no floating "
    "particles. Anatomy correct: five fingers per hand, thumbs placed right, "
    "joints bending the right way. "
)

BRANDING_PRODUCT = (
    "The Athlon Rub label is the only text or branding in the frame. All "
    "clothing, wraps, gloves, shoes, towels, bags and equipment are plain and "
    "unbranded: no other logos, signage, numbers, watermark or caption. Shirts "
    "and shorts carry no print or lettering on the front, back or sleeves. "
)
BRANDING_NONE = (
    "No text, lettering, numbers, logos, signage, watermark or caption anywhere "
    "in the frame. All clothing and equipment plain and unbranded, with no "
    "print on shirts or shorts. "
)


# ---------------------------------------------------------------------------
# Shots. kind: "people" (lifestyle with people), "still" (still life),
# "macro" (no product, close detail). skus: references attached, in order.
# ---------------------------------------------------------------------------
SHOTS = {
    "hero-desktop": {
        "ratio": "16:9", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "Night inside a clean, well-kept Muay Thai gym lit by a single low "
            "tungsten lamp hanging over the ring. FOREGROUND, lower right third, "
            "about 70 cm from the lens and tack sharp: {p250}standing upright on "
            "the edge of the white ring apron, label square to camera, the lamp "
            "behind it so the oil inside glows like liquid gold. BEHIND IT, "
            "softly out of focus in the ring corner: a male fighter seated on the "
            "corner stool, head bowed, taped hands on his knees, chest heaving, "
            "while a cornerman's hands press oil into his shoulder with a flat "
            "palm. The LEFT HALF of the frame falls away into deep green-black "
            "shadow, quiet and empty, leaving clean room for headline type. 50mm "
            "at f/1.4, camera at apron height."
        ),
    },
    "hero-mobile": {
        "ratio": "9:16", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "Vertical frame. Night inside a clean, well-kept Muay Thai gym lit "
            "by a single low tungsten lamp over the ring. LOWER THIRD, centred "
            "slightly right and tack sharp: {p250}standing upright on the edge of "
            "the white ring apron, label square to camera, backlit so the oil "
            "glows like liquid gold. MIDDLE THIRD, softly out of focus: a male "
            "fighter on the corner stool, head bowed, taped hands on his knees, "
            "a cornerman's flat palm pressing oil into his shoulder. The TOP "
            "THIRD is deep green-black shadow, empty and quiet, for headline "
            "type. 50mm at f/1.4 from apron height."
        ),
    },
    "product-stage": {
        "ratio": "16:9", "skus": ["250"], "kind": "still", "oil": False,
        "scene": (
            "A single {p250}standing on a low plinth of honed dark green-black "
            "stone, placed right of centre, label square to camera. A warm light "
            "behind and above shines through the amber bottle so the oil glows "
            "like liquid gold; a thin gold rim light traces its edges. Two or "
            "three small beads of amber oil rest on the stone near its base. "
            "Soft in the background to the right: a few yellow arnica flowers "
            "and a cut Thai Plai root, small and out of focus. The left 45 "
            "percent of the frame is calm, dark negative space. Camera at "
            "bottle mid-height, 120mm at f/5.6."
        ),
    },
    "product-trio": {
        "ratio": "3:2", "skus": ["100", "250", "500"], "kind": "still", "oil": False,
        "scene": (
            "Three Athlon Rub bottles standing in a row on one long plinth of "
            "honed dark green-black stone, labels square to camera, at TRUE "
            "relative scale. The three references are attached in this order. "
            "LEFT, first reference: {p100}CENTRE, second reference: {p250}"
            "RIGHT, third reference: {p500}So the 500 ml is the widest and "
            "slightly the tallest, the 250 ml is slim and nearly as tall, the "
            "100 ml is clearly the smallest. A warm light behind them shines "
            "through the amber so all three glow like liquid gold, a thin gold "
            "rim on each edge, deep forest-green to black background. Even "
            "spacing, centred group, camera at label height, 120mm at f/8 so "
            "all three are sharp."
        ),
    },
    "roster-combat": {
        "ratio": "3:4", "skus": ["250"], "kind": "people", "oil": False,
        "scene": (
            "A female Muay Thai fighter in her late twenties sits on a wooden "
            "bench at the edge of a clean gym, winding a black hand wrap around "
            "her left hand, eyes down, focused. FOREGROUND on the bench, sharp: "
            "{p250}standing upright beside a coiled spare wrap. Warm overhead "
            "tungsten key, ring ropes and heavy bags soft behind. 85mm at f/1.8, "
            "camera at bench height, focus on the bottle and her hands."
        ),
    },
    "roster-endurance": {
        "ratio": "3:4", "skus": ["100"], "kind": "people", "oil": True,
        "scene": (
            "A male distance runner in his thirties sits on the white kerb at "
            "the edge of a clean red running track at dusk, stadium floodlights "
            "just coming on behind, working oil into his calf with the heel of "
            "his palm. On the kerb beside his running shoe, sharp: {p100}Warm "
            "floodlight key from behind and to the side, dusk sky deepening to "
            "dark green-black. 85mm at f/1.8, low camera."
        ),
    },
    "roster-lifting": {
        "ratio": "3:4", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "A woman strength and HYROX athlete in her thirties, chalk on her "
            "hands, kneels beside a loaded barbell in a clean, well-run strength "
            "gym, pressing oil into her right shoulder with her left palm. "
            "FOREGROUND, standing on a black rubber bumper plate, sharp: {p250}"
            "Racked plates and a rig soft behind, one warm overhead light. 85mm "
            "at f/1.8."
        ),
    },
    "roster-paddle": {
        "ratio": "3:4", "skus": ["100"], "kind": "people", "oil": True,
        "scene": (
            "A fit man in his fifties, a pickleball player, sits courtside on a "
            "bench at a clean indoor court, pressing oil into his right forearm "
            "with his left thumb. On the bench beside him: a plain pickleball "
            "paddle, a yellow perforated ball and, sharp in the foreground, "
            "{p100}Court lines and a low net soft behind, warm hall lighting. "
            "85mm at f/2."
        ),
    },
    "roster-therapist": {
        "ratio": "3:4", "skus": ["500"], "kind": "people", "oil": True,
        "scene": (
            "Close and calm: a sports massage therapist's hands working oil into "
            "an athlete's quadriceps on a clean treatment table draped with a "
            "white towel, the heel of one palm driving up the thigh, the skin "
            "dragging under the pressure. The athlete's face is out of frame. "
            "On the table edge in the foreground, sharp: {p500}A quiet studio "
            "with warm wood and a plant soft behind, warm window key from the "
            "left. 85mm at f/2. Sports massage, not a clinic: no braces, no "
            "medical equipment."
        ),
    },
    "use-warmup": {
        "ratio": "3:4", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "Before training in a clean, well-kept boxing gym: a male athlete in "
            "his twenties sits on a wooden bench, hands already wrapped in plain "
            "black hand wraps, and works a small amount of oil into the front of "
            "his right shoulder with the flat palm of his left hand, fingers "
            "spread, the skin dragging slightly under the pressure. BESIDE HIM ON "
            "THE BENCH, sharp, in the lower right of the frame: {p250}standing "
            "upright with its clear over-cap ON, label square to camera, a warm "
            "lamp behind it so the oil inside glows amber. Nobody is touching "
            "the bottle. Only a faint satin sheen where he is rubbing; the rest "
            "of his skin dry and matte. Face partly in frame, focused, eyes down. "
            "Heavy bags and the ring soft behind, warm key from the left. 85mm "
            "at f/2. Plain unprinted black t-shirt and shorts."
        ),
    },
    "use-performance": {
        "ratio": "3:4", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "Between rounds at a Muay Thai bout: a female fighter on the corner "
            "stool, mouthguard out, chest heaving, while her cornerman leans in "
            "and presses oil into her thigh with a flat palm. On the ring apron "
            "in the foreground, sharp: {p250}Hard warm overhead ring light, the "
            "arena beyond falling away into green-black darkness. 50mm at f/1.6."
        ),
    },
    "use-recovery": {
        "ratio": "3:4", "skus": ["500"], "kind": "people", "oil": True,
        "scene": (
            "After the session, a simple, anatomically clear pose: a woman sits "
            "upright on a wooden bench in a clean, quiet locker room, towel "
            "around her neck, hair damp. Both feet flat on the floor, knees bent "
            "at a right angle and slightly apart, shins vertical. She rests both "
            "flat palms on the front of her right thigh, just above the knee, "
            "working oil into the quad, unhurried. Her arms come down in front "
            "of her body and her hands are clearly separate from her legs and "
            "feet. Exactly two arms, two hands, two legs and two feet, every "
            "limb distinct and correctly attached; nothing crossing or merging. "
            "On the bench beside her, sharp: {p500}Softer, calmer light: a "
            "frosted window as key plus one warm practical lamp, deep green "
            "tiled wall behind. 50mm at f/2.2, framed from her head to her feet."
        ),
    },
    "ingredient-arnica": {
        "ratio": "1:1", "skus": [], "kind": "macro", "oil": False,
        "scene": (
            "Botanical still life: a small cluster of fresh Arnica montana "
            "flowers, bright yellow ray petals slightly ragged, orange centres, "
            "short hairy stems, lying on honed dark green-black stone, with one "
            "small bead of clear amber oil on the stone beside them. Warm side "
            "light from the left. Centred, generous dark space around."
        ),
    },
    "ingredient-plai": {
        "ratio": "1:1", "skus": [], "kind": "macro", "oil": False,
        "scene": (
            "Botanical still life: fresh Thai Plai (Zingiber cassumunar) "
            "rhizomes, knobbly pale tan ginger-like roots, one sliced across to "
            "show its vivid yellow interior, lying on honed dark green-black "
            "stone with one small bead of clear amber oil beside them. Warm side "
            "light from the left. Centred, generous dark space around."
        ),
    },
    "ingredient-turmeric": {
        "ratio": "1:1", "skus": [], "kind": "macro", "oil": False,
        "scene": (
            "Botanical still life: fresh turmeric roots with thin papery brown "
            "skin, one snapped open to show bright saturated orange flesh, lying "
            "on honed dark green-black stone with one small bead of clear amber "
            "oil beside them. Warm side light from the left. Centred, generous "
            "dark space around."
        ),
    },
    "ingredient-wintergreen": {
        "ratio": "1:1", "skus": [], "kind": "macro", "oil": False,
        "scene": (
            "Botanical still life: two sprigs of wintergreen (Gaultheria "
            "procumbens), glossy dark green oval leaves with fine toothed edges "
            "and a few bright red berries, lying on honed dark green-black stone "
            "with one small bead of clear amber oil beside them. Warm side light "
            "from the left. Centred, generous dark space around."
        ),
    },
    "oil-macro": {
        "ratio": "16:9", "skus": [], "kind": "macro", "oil": False,
        "scene": (
            "Extreme macro, 2:1 magnification: a single small drop of amber oil "
            "resting on the skin of a forearm. A warm light behind passes "
            "through the drop so it glows gold, with a bright caustic spot on "
            "the skin. Skin pores, fine hairs and natural creases sharp around "
            "it; a faint satin sheen where a little has spread. Placed right of "
            "centre; the edges fall off into deep green-black. Macro lens at f/8."
        ),
    },
    "step-shake": {
        "ratio": "3:2", "skus": ["250"], "kind": "people", "oil": False,
        "scene": (
            "Mid-shake, caught in motion: one hand grips {p250}around its "
            "middle with the clear over-cap on and shakes it hard up and down in "
            "the air at chest height, nothing underneath it. Visible directional "
            "motion blur streaks on the hand and the top and bottom of the "
            "bottle, while the centre of the label stays readable: shield, "
            "ATHLON, RUB. A light froth of amber oil and air bubbles near the "
            "bottle shoulder. Dark green-black background, warm key from the "
            "left, gold rim on the right. 85mm at f/2.8, 1/60s shutter."
        ),
    },
    "step-pump": {
        "ratio": "3:2", "skus": ["250"], "kind": "people", "oil": True,
        "scene": (
            "Close on one hand holding {p250}over-cap removed, tilted slightly "
            "above an open cupped palm. One press of the pump: a short, slow "
            "ribbon of dense amber oil leaves the nozzle and a coin-sized pool "
            "already sits in the palm, glowing where the light passes through "
            "it. Dark green-black background, warm key from behind. 85mm at f/2.8."
        ),
    },
    "step-rub": {
        "ratio": "3:2", "skus": [], "kind": "people", "oil": True,
        "scene": (
            "Close-up, side view: ONE bare lower leg, from just above the knee "
            "down to the foot, rests horizontally along a wooden bench, the heel "
            "on the bench and the toes pointing up. This is the only leg and the "
            "only foot anywhere in the frame: no second leg, no second foot, no "
            "other body parts except two hands and forearms entering from the "
            "top of the frame. Both hands wrap the back of that calf, the heel "
            "of one palm driving up the calf muscle, the skin dragging slightly "
            "under the pressure. Both hands are empty: nothing held, no bottle. "
            "Only a light satin sheen on the calf muscle belly; shin, knee and "
            "foot dry and matte. Dark green-black background, warm raking key "
            "from the left. 85mm at f/2.8."
        ),
    },
    "heritage-camp": {
        "ratio": "16:9", "skus": [], "kind": "people", "oil": False,
        "scene": (
            "A traditional open-air Muay Thai camp in rural Thailand at first "
            "light: a raised wooden-floored ring under a corrugated metal roof "
            "on timber posts, worn leather heavy bags hanging from the beams, "
            "tropical trees and soft morning haze beyond. Old but clean and "
            "swept, cared for. Empty, except one small distant figure skipping "
            "rope. Soft warm dawn light filtered through the haze. 35mm at f/2.8."
        ),
    },
    "cta-locker": {
        "ratio": "21:9", "skus": ["250"], "kind": "people", "oil": False,
        "scene": (
            "A long, quiet, low-lit locker room with deep green tiled walls and "
            "warm practical lamps. FOREGROUND LEFT, sharp, standing on a wooden "
            "bench: {p250}MID-GROUND RIGHT, soft: a boxer seated on the same "
            "bench taping his hands, face in shadow. The centre of the frame is "
            "calm and dark for type. 50mm at f/1.6."
        ),
    },
    "pdp-travel-bag": {
        "ratio": "3:4", "skus": ["100"], "kind": "people", "oil": False,
        "scene": (
            "Three-quarter top-down view into an open black canvas gym duffel on "
            "a wooden bench: rolled hand wraps, a pair of plain boxing gloves, a "
            "folded towel, and {p100}tucked upright in the open side pocket, "
            "label facing camera and sharp. Warm window key from the left. 50mm "
            "at f/2.8. No people."
        ),
    },
}


def build(name):
    s = SHOTS[name]
    fill = {f"p{k}": SKU[k] for k in SKU}
    scene = s["scene"].format(**fill)
    parts = ["THE SHOT: " + scene]
    if s["skus"]:
        parts += [SCALE, LABEL, INTEGRATION]
    if s.get("oil"):
        parts.append(OIL)
    parts.append(STILL_LOOK if s["kind"] in ("still", "macro") else LOOK)
    if s["kind"] == "people" and name not in ("step-shake", "step-pump", "step-rub", "heritage-camp", "pdp-travel-bag"):
        parts.append(PEOPLE)
    parts.append(BRANDING_PRODUCT if s["skus"] else BRANDING_NONE)
    if s["kind"] == "people":
        parts.append(NEGATIVE)
    return " ".join(p.strip() for p in parts)


def next_path(name):
    n = 1
    while os.path.exists(os.path.join(RAW, f"{name}_r{n}.png")):
        n += 1
    return os.path.join(RAW, f"{name}_r{n}.png")


def run(name, ref_urls):
    s = SHOTS[name]
    prompt = build(name)
    urls = [ref_urls[k] for k in s["skus"]]
    inp = {"prompt": prompt, "aspect_ratio": s["ratio"], "size": "2K",
           "output_format": "png"}
    if urls:
        inp["image_urls"] = urls
    payload = {"model": I2I if urls else T2I, "input": inp}
    res = None
    for attempt in (1, 2, 3):
        try:
            res = post(CREATE_URL, payload)
        except Exception as e:  # network
            if attempt == 3:
                return name, f"submit failed: {e}"
            time.sleep(5)
            continue
        if res.get("code") == 200:
            break
        if attempt == 3:
            return name, f"submit rejected: {res.get('code')} {res.get('msg')}"
        time.sleep(5)
    task = res["data"]["taskId"]
    deadline = time.time() + 900
    while time.time() < deadline:
        time.sleep(8)
        try:
            info = get(f"{QUERY_URL}?taskId={task}")["data"]
        except Exception:
            continue
        st = info.get("state")
        if st == "success":
            url = json.loads(info["resultJson"])["resultUrls"][0]
            out = next_path(name)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=300) as r, open(out, "wb") as f:
                f.write(r.read())
            return name, f"OK {os.path.basename(out)} ({os.path.getsize(out)//1024} KB, task {task})"
        if st == "fail":
            return name, f"FAILED {info.get('failCode')} {info.get('failMsg')}"
    return name, "timed out"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    names = list(SHOTS) if "--all" in sys.argv else args
    bad = [n for n in names if n not in SHOTS]
    if bad:
        sys.exit(f"unknown shots: {bad}")
    for n in names:
        p = build(n)
        open(os.path.join(PROMPTS, f"{n}.txt"), "w").write(p)
        print(f"{n}: prompt {len(p)} chars")
        if len(p) > 4950:
            sys.exit(f"{n} prompt too long ({len(p)})")
    if "--prompts" in sys.argv:
        return
    ref_urls = refs()
    c0 = credits()
    print(f"credits before: {c0}")
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(run, n, ref_urls): n for n in names}
        for f in as_completed(futs):
            n, msg = f.result()
            print(f"  {n}: {msg}", flush=True)
    c1 = credits()
    print(f"credits after: {c1}  (spent {c0 - c1:.2f} for {len(names)} shots)")


if __name__ == "__main__":
    main()
