"""Batch image generation via Stable Horde (free, anonymous). usage: python3 horde_batch.py prompts.json outdir [concurrency]"""
import json, os, sys, time, threading, urllib.request
import numpy as np
from PIL import Image
BAD = set()
def smooth(p):
    a = np.asarray(Image.open(p).convert("L").resize((256, 455)), dtype=float)
    g = np.abs(np.diff(a, axis=1))[:-1] + np.abs(np.diff(a, axis=0))[:, :-1]
    return float((g < 6).mean())
API = "https://stablehorde.net/api/v2"
H = {"apikey": "0000000000", "Content-Type": "application/json", "Client-Agent": "video-studio:1.1:anon"}
NEG = "text, letters, words, watermark, signature, logo, photo, photorealistic, 3d render, blurry, deformed, extra limbs, ugly, nsfw"
def req(m, u, b=None):
    r = urllib.request.Request(API + u, data=json.dumps(b).encode() if b else None, headers=H, method=m)
    return json.load(urllib.request.urlopen(r, timeout=90))
def gen(name, prompt, out, model="Juggernaut XL", upscale=True):
    path = f"{out}/{name}.webp"
    if os.path.exists(path): return
    for attempt in range(7):
        try:
            p = {"width": 576, "height": 1024, "steps": 28, "cfg_scale": 6, "n": 1, "sampler_name": "k_euler_a"}
            if upscale: p["post_processing"] = ["RealESRGAN_x2plus"]
            body = {"prompt": prompt + " ### " + NEG, "params": p, "models": [model], "nsfw": False, "censor_nsfw": True, "r2": True, "slow_workers": True}
            if BAD: body.update({"workers": sorted(BAD), "worker_blacklist": True})
            j = req("POST", "/generate/async", body)
            i = j["id"]; t0 = time.time()
            while True:
                time.sleep(12); s = req("GET", f"/generate/check/{i}")
                if s.get("done"): break
                if s.get("faulted") or time.time() - t0 > 1500: raise RuntimeError("faulted/timeout")
            g = req("GET", f"/generate/status/{i}")["generations"][0]
            if g.get("censored"): raise RuntimeError("censored")
            urllib.request.urlretrieve(g["img"], path); sm = smooth(path)
            if sm < 0.6:
                BAD.add(g.get("worker_id")); os.remove(path); raise RuntimeError(f"garbage smooth={sm:.2f} worker={g.get('worker_name')}")
            print("ok", name, int(time.time() - t0), f"smooth={sm:.2f}", g.get("worker_name"), flush=True); return
        except Exception as e:
            print("retry", name, attempt, str(e)[:120], flush=True)
            if "upscal" in str(e).lower() or "kudos" in str(e).lower(): upscale = False
            time.sleep(10)
    print("FAILED", name, flush=True)
if __name__ == "__main__":
    try:
        ws = req("GET", "/workers?type=image")
        for w in ws:
            if any(k in w.get("name", "").lower() for k in ("dumbstupid", "gn100", "nothingdark")): BAD.add(w["id"])
        print("blacklisted", len(BAD), flush=True)
    except Exception as e: print("worker list failed", e, flush=True)
    items = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    conc = int(sys.argv[3]) if len(sys.argv) > 3 else 4; sem = threading.Semaphore(conc); ths = []
    def run(it):
        with sem: gen(it["name"], it["prompt"], out, it.get("model", "Juggernaut XL"))
    for it in items:
        t = threading.Thread(target=run, args=(it,)); t.start(); ths.append(t); time.sleep(2)
    for t in ths: t.join()
