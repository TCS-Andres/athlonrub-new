"""
Export the approved frames to the site and write the image manifest.

    python3 export.py

SELECTED maps each shot to the raw take that passed QA. Landscape exports at
2400 / 1200 px wide, portrait and square at 1600 / 800 (never upscaled).
Also writes site/src/_data/images.json and _contact_sheet.jpg.
"""
import json
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "_raw")
SCENES = os.path.join(ROOT, "site", "src", "assets", "img", "scenes")
PRODUCTS = os.path.join(ROOT, "site", "src", "assets", "img", "products")
MANIFEST = os.path.join(ROOT, "site", "src", "_data", "images.json")
os.makedirs(SCENES, exist_ok=True)
os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)

SELECTED = {
    "hero-desktop": ("r2", "A Pro bottle of Athlon Rub on a ring apron in a dim Muay Thai gym while a cornerman works oil into a seated fighter's shoulder"),
    "hero-mobile": ("r1", "A Pro bottle of Athlon Rub on a ring apron, a cornerman working oil into a seated fighter's shoulder behind it"),
    "product-stage": ("r1", "Athlon Rub Pro bottle on a dark green stone plinth with arnica flowers and Thai Plai root"),
    "product-trio": ("r1", "The three Athlon Rub sizes, Travel, Pro and Coach, side by side on a stone plinth"),
    "roster-combat": ("r2", "A Muay Thai fighter wrapping her hands on a gym bench beside a bottle of Athlon Rub"),
    "roster-endurance": ("r2", "A runner working oil into his calf at the edge of a running track at dusk, a Travel bottle by his shoe"),
    "roster-lifting": ("r1", "A strength athlete kneeling by a barbell, working oil into her shoulder, a Pro bottle on a bumper plate"),
    "roster-paddle": ("r1", "A pickleball player courtside pressing oil into his forearm, paddle, ball and Travel bottle on the bench"),
    "roster-therapist": ("r1", "A sports massage therapist working oil into an athlete's thigh, a Coach bottle on the table"),
    "use-warmup": ("r4", "A boxer with wrapped hands working Athlon Rub into his shoulder on a gym bench before training, a Pro bottle beside him"),
    "use-performance": ("r2", "Between rounds, a cornerman works oil into a fighter's thigh, a Pro bottle on the ring apron"),
    "use-recovery": ("r3", "After training, a woman on a locker-room bench works oil into her thigh beside a Coach bottle"),
    "ingredient-arnica": ("r1", "Arnica montana flowers on dark stone beside a bead of amber oil"),
    "ingredient-plai": ("r1", "Thai Plai rhizomes, one cut open to show the yellow interior, beside a bead of amber oil"),
    "ingredient-turmeric": ("r1", "Fresh turmeric roots, one split to show orange flesh, beside a bead of amber oil"),
    "ingredient-wintergreen": ("r1", "Wintergreen sprigs with red berries on dark stone beside a bead of amber oil"),
    "oil-macro": ("r1", "Macro of a single drop of amber oil resting on the skin of a forearm"),
    "step-shake": ("r2", "A hand shaking a Pro bottle of Athlon Rub"),
    "step-pump": ("r1", "One press of the pump dispensing a coin-sized amount of amber oil into an open palm"),
    "step-rub": ("r3", "Both hands working oil into a calf muscle, the leg resting on a bench"),
    "heritage-camp": ("r1", "A traditional open-air Muay Thai camp in Thailand at dawn, wooden ring and heavy bags"),
    "cta-locker": ("r2", "A Pro bottle on a locker-room bench while a boxer tapes his hands"),
    "pdp-travel-bag": ("r1", "An open gym bag with gloves, wraps and a Travel bottle of Athlon Rub in the side pocket"),
}

# Focal points for crops (CSS object-position). The bottle in product-stage sits
# at 62% of the frame width; 72% centres it in the 4:5 crops the site uses.
FOCUS = {
    "product-stage": "72% 50%",
}

PRODUCT_ALT = {
    "bottle-travel": "Athlon Rub Travel, 3.4 fl oz / 100 mL",
    "bottle-pro": "Athlon Rub Pro, 8.5 fl oz / 250 mL",
    "bottle-coach": "Athlon Rub Coach, 17 fl oz / 500 mL",
    "bottle-travel-hd": "Athlon Rub Travel, 3.4 fl oz / 100 mL",
    "bottle-pro-hd": "Athlon Rub Pro, 8.5 fl oz / 250 mL",
    "bottle-coach-hd": "Athlon Rub Coach, 17 fl oz / 500 mL",
    "bundle-6": "Six Athlon Rub Pro bottles",
    "bundle-12": "Twelve Athlon Rub Pro bottles",
    "bundle-case": "A case of Athlon Rub Travel bottles",
}


def resize_to(im, w):
    if im.width <= w:
        return im
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def main():
    manifest = {}
    thumbs = []
    for name, (take, alt) in SELECTED.items():
        im = Image.open(os.path.join(RAW, f"{name}_{take}.png")).convert("RGB")
        landscape = im.width > im.height
        lg_w, sm_w = (2400, 1200) if landscape else (1600, 800)
        lg = resize_to(im, lg_w)
        sm = resize_to(im, sm_w)
        lg.save(os.path.join(SCENES, f"{name}-lg.webp"), "WEBP", quality=82, method=6)
        sm.save(os.path.join(SCENES, f"{name}-sm.webp"), "WEBP", quality=80, method=6)
        manifest[name] = {
            "alt": alt, "w": lg.width, "h": lg.height,
            "src": f"/assets/img/scenes/{name}-lg.webp",
            "srcSm": f"/assets/img/scenes/{name}-sm.webp", "smW": sm.width,
        }
        if name in FOCUS:
            manifest[name]["focus"] = FOCUS[name]
        t = im.copy()
        t.thumbnail((640, 640))
        d = ImageDraw.Draw(t)
        d.rectangle((0, 0, 8 + 7 * len(name), 20), fill=(0, 0, 0))
        d.text((5, 5), name, fill=(230, 200, 120))
        thumbs.append(t)
        print(f"{name}: {take} -> {lg.size} / {sm.size}")

    meta = json.load(open(os.path.join(RAW, "cutouts", "_meta.json")))
    for name, m in meta.items():
        manifest[name] = {"alt": PRODUCT_ALT[name], "w": m["w"], "h": m["h"],
                          "src": f"/assets/img/products/{name}.webp",
                          "png": f"/assets/img/products/{name}.png"}
        if "mm" in m:
            manifest[name]["mm"] = m["mm"]

    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)

    # contact sheet: scenes, then products on brand green
    for name in ["bottle-travel", "bottle-pro", "bottle-coach", "bundle-6", "bundle-12", "bundle-case"]:
        p = Image.open(os.path.join(PRODUCTS, f"{name}.png"))
        bg = Image.new("RGBA", p.size, (14, 61, 40, 255))
        bg.alpha_composite(p)
        t = bg.convert("RGB")
        t.thumbnail((640, 640))
        thumbs.append(t)
    cols = 5
    cw, ch = 640, 640
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (20, 24, 22))
    for i, t in enumerate(thumbs):
        x = (i % cols) * cw + (cw - t.width) // 2
        y = (i // cols) * ch + (ch - t.height) // 2
        sheet.paste(t, (x, y))
    sheet.save(os.path.join(HERE, "_contact_sheet.jpg"), quality=86)
    print("manifest:", len(manifest), "entries")


if __name__ == "__main__":
    main()
