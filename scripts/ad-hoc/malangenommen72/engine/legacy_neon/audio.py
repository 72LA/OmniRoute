import json, subprocess, wave, numpy as np
SR = 48000
tl = json.load(open("timeline.json")); total = tl["total"]
n = int(total * SR) + SR
voice = np.zeros(n); sfx = np.zeros(n)
def load(fn):
    raw = subprocess.run(["ffmpeg","-v","error","-i",fn,"-ar",str(SR),"-ac","1","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float64) / 32768
import os
if os.path.exists("full_voice.wav"):
    x = load("full_voice.wav"); voice[:min(n,len(x))] += x[:n]
else:
  for i, (a, b, sc) in enumerate(tl["segs"]):
    x = load(f"s{i:02d}.wav"); s = int(a * SR); voice[s:s+len(x)] += x
t = lambda d: np.arange(int(d*SR))/SR
rng = np.random.default_rng(1)
def whoosh():
    d=0.5; tt=t(d); noise=rng.standard_normal(len(tt))
    # crude band sweep: moving average with shrinking window
    out=np.zeros_like(noise); k=np.linspace(40,4,len(tt)).astype(int)
    cs=np.cumsum(np.insert(noise,0,0))
    for i in range(len(tt)):
        j=max(0,i-k[i]); out[i]=(cs[i+1]-cs[j])/(i+1-j)
    env=np.sin(np.pi*tt/d)**2
    return out*env*0.9
def ding():
    tt=t(0.8); return (np.sin(2*np.pi*1320*tt)+0.4*np.sin(2*np.pi*2640*tt))*np.exp(-tt*6)*0.35
def pop():
    tt=t(0.12); f=np.linspace(900,250,len(tt)); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*30)*0.6
def place(sig, at):
    s=int(at*SR); sfx[s:s+len(sig)] += sig[:max(0,n-s)]
segs = tl["segs"]
import os as _os
if _os.path.exists("sfx.json"):
    fx = {"whoosh": whoosh, "ding": ding, "pop": pop}
    for kind, si, off in json.load(open("sfx.json")):
        place(fx[kind](), (segs[si][0] if si >= 0 else 0) + off)
else:
    place(whoosh(), 0.0)
    place(pop(), segs[1][0])
    place(ding(), segs[3][0] + 0.45)
    place(pop(), segs[4][0])
    place(whoosh(), segs[5][0] - 0.1)
    place(pop(), segs[8][0])
mix = voice + sfx*0.35
mix = mix[:int((total)*SR)]
mix /= max(1e-9, np.abs(mix).max()) / 0.9
with wave.open("mix.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix*32767).astype(np.int16).tobytes())
print("audio", len(mix)/SR)
