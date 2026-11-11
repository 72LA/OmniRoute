"""voice.py – one continuous TTS take per video, word-accurate timing, natural pause tightening, clean chain.

usage (in the episode dir, next to script.json):
    python3 <repo>/engine/voice.py [--model gemini-3.8-flash-tts] [--voice Puck] [--style "..."] [--tempo auto|1.06]
                                   [--gap 0.14] [--inner 0.10] [--take take.wav]

Replaces tts_groups.py + assemble.py + tighten.py + clean_voice.sh for new videos (those stay for old projects).
Why: the old chain cut the take into sentences by silence guessing (wrong cuts when two sentences had no pause),
re-joined them with hard cuts and spread captions by character count. This one keeps the take whole (natural
prosody across sentences), finds every word with a local speech model and only shortens pauses.

Outputs: full_voice.wav (24 kHz mono, cleaned), full_voice_raw.wav, segs_abs.json (sentence [start, end]),
         words.json ([{"t0","t1","w","line"}] – the `show` words with their spoken time), take.wav (cached TTS).
One TTS request per video (free tier: 10 per day and model). An existing take.wav is reused, never re-requested.
"""
import argparse, base64, json, os, re, subprocess, sys, time, urllib.error, urllib.request, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--model", default=os.environ.get("TTS_MODEL", "gemini-3.8-flash-tts"))
ap.add_argument("--voice", default="Puck")
ap.add_argument("--style", default=os.environ.get("TTS_STYLE_META",
                "curious, lively German explainer for a short video; brisk, confident pace; clear emphasis on numbers; no long pauses"))
ap.add_argument("--tempo", default="auto")
ap.add_argument("--gap", type=float, default=0.14)     # pause kept between sentences
ap.add_argument("--inner", type=float, default=0.10)   # longest pause kept inside a sentence
ap.add_argument("--take", default="take.wav")
ap.add_argument("--target", type=float, default=19.0)  # characters per second aimed at by --tempo auto
A = ap.parse_args()
FALLBACKS = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-3.8-flash-lite-tts"]
SR = 24000
lines = json.load(open("script.json"))


def tts(text, out):
    models = [A.model] + [m for m in FALLBACKS if m != A.model]
    for model in models:
        for with_style in (True, False):       # older models reject speech_metadata -> retry plain
            part = {"text": text}
            if with_style and A.style: part["speech_metadata"] = {"style": A.style}
            body = {"contents": [{"role": "user", "parts": [part]}],
                    "generationConfig": {"responseModalities": ["AUDIO"],
                                         "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": A.voice}}}}}
            req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                         data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            try:
                r = json.load(urllib.request.urlopen(req, timeout=180))
                d = r["candidates"][0]["content"]["parts"][0]["inlineData"]; raw = base64.b64decode(d["data"])
                if raw[:4] == b"RIFF":
                    open(out, "wb").write(raw)
                else:
                    rate = int(d["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in d["mimeType"] else SR
                    with wave.open(out, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(raw)
                print("tts ok:", model, "style" if with_style and A.style else "plain"); return
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:200].replace("\n", " "); print("tts", model, e.code, msg, file=sys.stderr)
                if e.code == 400 and with_style: continue      # try again without style
                if e.code == 429: time.sleep(20)
                break                                           # next model
            except (KeyError, IndexError) as e:
                print("tts", model, "no audio in answer", e, file=sys.stderr); break
    raise SystemExit("TTS failed on all models – quota used up? Try again later or pass --take <file>.")


def load(fn):
    tmp = "_v.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", fn, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", tmp], check=True)
    with wave.open(tmp) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    os.remove(tmp); return x


def save(fn, x):
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def norm(s): return re.sub(r"[^a-zäöüß0-9]", "", s.lower())


# ---- 1. take -------------------------------------------------------------------------------------------------------
if not os.path.exists(A.take):
    tts(" ".join(l["say"] for l in lines), A.take)
x = load(A.take)

# ---- 2. words (local speech model, no quota) ---------------------------------------------------------------------
from faster_whisper import WhisperModel   # pip install faster-whisper
x16 = np.interp(np.arange(0, len(x), SR / 16000), np.arange(len(x)), x).astype(np.float32)
segs, _ = WhisperModel(os.environ.get("ALIGN_MODEL", "small"), device="cpu", compute_type="int8").transcribe(
    x16, language="de", word_timestamps=True, initial_prompt=" ".join(l["show"] for l in lines)[:800])
heard = [(w.start, w.end, w.word.strip()) for s in segs for w in s.words if w.word.strip()]
if len(heard) < 3: raise SystemExit("speech model found no words – check the take")

# sentence ends: expected position by characters, snapped to the nearest heard word end (prefers . ? ! and a real pause)
chars = np.cumsum([len(norm(l["say"])) for l in lines]); total = chars[-1]
hc = np.cumsum([max(1, len(norm(w))) for _, _, w in heard]); hc = hc / hc[-1] * total
ends = []
lo = 0
for i in range(len(lines) - 1):
    best, bs = None, 1e9
    for k in range(lo, len(heard) - (len(lines) - 1 - i)):
        gap = heard[k + 1][0] - heard[k][1]
        score = abs(hc[k] - chars[i]) - (6 if heard[k][2][-1:] in ".?!" else 0) - min(gap, 0.6) * 12
        if score < bs: best, bs = k, score
    ends.append(best); lo = best + 1
ends.append(len(heard) - 1)
starts = [0] + [e + 1 for e in ends[:-1]]

# ---- 3. tighten: keep the take whole, only shorten pauses (short crossfades, no hard cuts) ---------------------
def bounds(i):          # refine a word edge to the real energy edge
    return heard[i][0], heard[i][1]
frame = int(0.005 * SR)
env = np.sqrt(np.convolve(x * x, np.ones(frame) / frame, mode="same"))
thr = max(0.004, env.max() * 0.02)
def speech_start(t):
    i = int(max(0, t - 0.12) * SR); j = int(min(len(x) / SR, t + 0.12) * SR)
    on = np.where(env[i:j] > thr)[0]
    return (i + on[0]) / SR if len(on) else t
def speech_end(t):
    i = int(max(0, t - 0.12) * SR); j = int(min(len(x) / SR, t + 0.2) * SR)
    on = np.where(env[i:j] > thr)[0]
    return (i + on[-1]) / SR if len(on) else t

# silent stretches anywhere in the take
quiet = env < thr; runs = []; k = 0
while k < len(quiet):
    if quiet[k]:
        j = k
        while j < len(quiet) and quiet[j]: j += 1
        runs.append((k / SR, j / SR)); k = j
    else: k += 1
sent_gap_at = {}
for i in range(len(lines) - 1):
    sent_gap_at[i] = (heard[ends[i]][1] + heard[starts[i + 1]][0]) / 2
pieces, cuts = [], []     # cuts: (source_time, seconds_removed) for remapping
pos = 0.0
t_first = speech_start(heard[0][0])
if t_first > 0.01: cuts.append((0.0, t_first)); pos = t_first
for a, b in runs:
    if b <= pos or a < t_first: continue
    if b >= len(x) / SR - 0.005:                 # tail silence: keep 0.12 s
        keep_tail = min(b - a, 0.12)
        pieces.append((pos, a + keep_tail)); pos = None; break
    is_sent = any(a - 0.05 <= g <= b + 0.05 for g in sent_gap_at.values())
    keep = A.gap if is_sent else A.inner
    if b - a > keep + 0.02:
        pieces.append((pos, a + keep / 2)); cuts.append((a + keep / 2, (b - a) - keep)); pos = b - keep / 2
if pos is not None: pieces.append((pos, len(x) / SR))
xf = int(0.006 * SR); out = np.zeros(0, np.float32)
for a, b in pieces:
    seg = x[int(a * SR):int(b * SR)].copy()
    if len(out) >= xf and len(seg) >= xf:
        r = np.linspace(0, 1, xf, dtype=np.float32)
        out[-xf:] = out[-xf:] * (1 - r) + seg[:xf] * r; seg = seg[xf:]
    out = np.concatenate([out, seg])
def remap(t):
    removed = sum(d for at, d in cuts if at <= t)
    removed += (len([1 for at, d in cuts if at <= t and at > 0]) ) * (xf / SR)
    return max(0.0, t - removed)

# ---- 4. tempo + clean chain ---------------------------------------------------------------------------------------
dur0 = len(out) / SR
cps = sum(len(l["say"]) for l in lines) / dur0
tempo = float(np.clip(A.target / cps, 1.0, 1.10)) if A.tempo == "auto" else float(A.tempo)
save("full_voice_raw.wav", out / max(1e-6, np.abs(out).max()) * 0.92)
chain = (f"atempo={tempo:.4f}," if abs(tempo - 1) > 0.004 else "") + (
    "highpass=f=80,deesser=i=0.35:m=0.5:f=0.5,equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=3200:t=q:w=1:g=1.8,"
    "equalizer=f=9000:t=h:w=1:g=1.5,acompressor=threshold=0.11:ratio=3:attack=6:release=120:makeup=1.7,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "full_voice_raw.wav", "-af", chain, "-ar", str(SR), "-ac", "1", "full_voice.wav"], check=True)
with wave.open("full_voice.wav") as w: vdur = w.getnframes() / SR
T = lambda t: round(min(vdur, remap(t) / tempo), 3)

# ---- 5. timing files -----------------------------------------------------------------------------------------------
seg_abs, words = [], []
for i, l in enumerate(lines):
    hs = heard[starts[i]:ends[i] + 1]
    a = 0.0 if i == 0 else T(speech_start(hs[0][0])); b = T(speech_end(hs[-1][1]))
    seg_abs.append([a, b])
    show = l["show"].split()
    # spread the `show` words over the heard words of this sentence (digits vs spelled numbers differ in count)
    hw = np.array([max(1, len(norm(w))) for _, _, w in hs], float); hpos = np.concatenate([[0], np.cumsum(hw)]) / hw.sum()
    ht = [T(hs[0][0])] + [T(e) for _, e, _ in hs]; ht[0] = a
    if len(show) == len(hs):
        for (s, e, _), w in zip(hs, show): words.append({"t0": T(s), "t1": T(e), "w": w, "line": i})
    else:
        sw = np.array([max(1, len(norm(w))) for w in show], float); spos = np.concatenate([[0], np.cumsum(sw)]) / sw.sum()
        for k, w in enumerate(show):
            words.append({"t0": round(float(np.interp(spos[k], hpos, ht)), 3), "t1": round(float(np.interp(spos[k + 1], hpos, ht)), 3), "w": w, "line": i})
    words[-len(show)]["t0"] = a
for k in range(1, len(words)):                      # monotonic, no overlaps
    words[k]["t0"] = max(words[k]["t0"], words[k - 1]["t0"] + 0.02)
    words[k - 1]["t1"] = min(max(words[k - 1]["t1"], words[k - 1]["t0"] + 0.04), words[k]["t0"]) if words[k]["line"] == words[k - 1]["line"] else words[k - 1]["t1"]
json.dump(seg_abs, open("segs_abs.json", "w")); json.dump(words, open("words.json", "w"), ensure_ascii=False)
for (a, b), l, s, e in zip(seg_abs, lines, starts, ends):
    print(f"{a:6.2f}-{b:6.2f} {len(l['say'])/max(0.01, b-a):5.1f} ch/s | heard: {' '.join(w for _, _, w in heard[s:e+1])[:70]}")
print(f"take {len(x)/SR:.2f} s -> tightened {dur0:.2f} s -> tempo {tempo:.3f} -> {vdur:.2f} s | first word at {seg_abs[0][0]:.2f} s")
print("CHECK: every 'heard' line must match its script sentence. If not: fix script punctuation or cut by hand.")
