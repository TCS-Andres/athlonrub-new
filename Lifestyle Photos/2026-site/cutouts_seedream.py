"""
Seedream 5.5 transparent-background attempt at the three product cutouts,
for comparison against recraft/remove-background. Writes
_raw/cutouts/seedream_{sku}.png.
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as g

OUT = os.path.join(g.RAW, "cutouts")
os.makedirs(OUT, exist_ok=True)

PROMPT = (
    "Remove the background completely and return only the bottle on a fully "
    "transparent background. Keep the bottle, its label, pump and over-cap "
    "exactly identical to the input image, pixel for pixel: do not redraw, "
    "retouch, relight, sharpen or change any text, logo or artwork on the "
    "label. The clear over-cap stays semi-transparent. No shadow, no "
    "reflection, no backdrop, no added objects."
)


def one(sku, url):
    payload = {"model": g.I2I, "input": {
        "prompt": PROMPT, "image_urls": [url], "aspect_ratio": "auto",
        "size": "2K", "output_format": "png", "background": "transparent"}}
    res = g.post(g.CREATE_URL, payload)
    if res.get("code") != 200:
        return sku, f"rejected {res.get('code')} {res.get('msg')}"
    task = res["data"]["taskId"]
    for _ in range(100):
        time.sleep(8)
        info = g.get(f"{g.QUERY_URL}?taskId={task}")["data"]
        if info.get("state") == "success":
            u = json.loads(info["resultJson"])["resultUrls"][0]
            out = os.path.join(OUT, f"seedream_{sku}.png")
            req = urllib.request.Request(u, headers={"User-Agent": g.UA})
            open(out, "wb").write(urllib.request.urlopen(req, timeout=300).read())
            return sku, "OK " + out
        if info.get("state") == "fail":
            return sku, f"FAILED {info.get('failMsg')}"
    return sku, "timeout"


if __name__ == "__main__":
    refs = g.refs()
    with ThreadPoolExecutor(3) as p:
        for sku, msg in p.map(lambda k: one(k, refs[k]), ["100", "250", "500"]):
            print(sku, msg)
