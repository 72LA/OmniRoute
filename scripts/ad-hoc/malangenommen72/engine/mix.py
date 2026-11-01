# usage (in episode dir): python3 ../engine/mix.py  -> mix.wav (uses timeline.json, full_voice.wav, sfx.json)
import json, subprocess, wave, numpy as np
SR = 48000
tl = json.load(open("timeline.json")); total = tl["total"]; segs = tl["segs"]
n = int(total * SR)
def load(fn):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", fn, "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768
voice = np.zeros(n); x = load("full_voice.wav")[:n]; voice[:len(x)] = x
sfx = np.zeros(n + SR)
t = lambda d: np.arange(int(d * SR)) / SR
rng = np.random.default_rng(1)
def whoosh():
    tt = t(0.5); nz = rng.standard_normal(len(tt)); k = np.linspace(40, 4, len(tt)).astype(int)
    cs = np.cumsum(np.insert(nz, 0, 0)); out = np.array([(cs[i + 1] - cs[max(0, i - k[i])]) / (i + 1 - max(0, i - k[i])) for i in range(len(tt))])
    return out * np.sin(np.pi * tt / 0.5) ** 2 * 0.9
def ding():
    tt = t(0.8); return (np.sin(2 * np.pi * 1320 * tt) + 0.4 * np.sin(2 * np.pi * 2640 * tt)) * np.exp(-tt * 6) * 0.35
def pop():
    tt = t(0.12); f = np.linspace(900, 250, len(tt)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 30) * 0.6
def blip():
    tt = t(0.07); return np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 50) * 0.35
FX = {"whoosh": whoosh, "ding": ding, "pop": pop, "blip": blip}
for kind, si, off in json.load(open("sfx.json")):
    at = (segs[si][0] if si >= 0 else 0) + off; s = int(at * SR); sig = FX[kind]()
    sfx[s:s + len(sig)] += sig
mix = voice + sfx[:n] * 0.35
mix /= max(1e-9, np.abs(mix).max()) / 0.9
with wave.open("mix.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("mix", round(len(mix) / SR, 2))
