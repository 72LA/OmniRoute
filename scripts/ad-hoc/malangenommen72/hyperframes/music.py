"""Own royalty-free background music (procedural), ducked under the voice.

usage: python3 music.py <episode_dir> dark|bright [bpm] [--key A] [--prog NAME] [--lift SEC] [--seed N] [--level -27]
  -> <episode_dir>/music.wav (48 kHz stereo, length = voice + 1.6 s)

Variety per video (so no two videos sound the same):
  --key   root note C, C#, D … B. Default: picked from the episode folder name (stable per video).
  --prog  chord progression. dark (minor): pop = i-VI-III-VII · fall = i-VII-VI-VII · plagal = i-iv-VI-V · rise = VI-VII-i-i
                              bright (major): pop = I-V-vi-IV · fifties = I-vi-IV-V · lift = IV-I-V-vi · walk = I-IV-vi-V
          Default: picked from the episode folder name.
  --lift  second where the arrangement opens up (extra octave + faster hats) – set it to the start of the payoff scene
          (default 62 % of the length = where GO.md puts the resolution).
Structure: starts on a hit at 0.0 s (no fade-in – the first second must not be quiet), opens at --lift, ends on the
root chord with a 1 s fade. Same mix rules as before: bed far under the voice, sidechain duck while the voice speaks.
"""
import argparse, json, os, subprocess, wave, zlib
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("ep"); ap.add_argument("style", choices=["dark", "bright"]); ap.add_argument("bpm", nargs="?", type=float)
ap.add_argument("--key"); ap.add_argument("--prog"); ap.add_argument("--lift", type=float); ap.add_argument("--seed", type=int)
ap.add_argument("--level", type=float, default=-27.0)   # LUFS of the bed before ducking
A = ap.parse_args()
ep, style = A.ep, A.style
SR = 48000
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PROGS = {"dark": {"pop": [0, 8, 3, 10], "fall": [0, 10, 8, 10], "plagal": [0, 5, 8, 7], "rise": [8, 10, 0, 0]},
         "bright": {"pop": [0, 7, 9, 5], "fifties": [0, 9, 5, 7], "lift": [5, 0, 7, 9], "walk": [0, 5, 9, 7]}}
MINOR_ROOTS = {0, 5, 7} if style == "dark" else {9, 2, 4}     # scale degrees (semitones) that carry a minor triad
h = zlib.crc32(os.path.basename(os.path.abspath(ep)).encode())
seed = A.seed if A.seed is not None else h
key = A.key or ["A", "D", "E", "F#", "G", "B", "C"][h % 7]
pname = A.prog or sorted(PROGS[style])[(h // 7) % 4]
root = 57 + ((NOTES.index(key) - 9 + 6) % 12 - 6) if style == "dark" else 60 + ((NOTES.index(key) + 6) % 12 - 6)

with wave.open(f"{ep}/full_voice.wav") as w: vsr = w.getframerate(); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
dur = len(v) / vsr + 1.6; N = int(dur * SR); t = np.arange(N) / SR
lift = A.lift if A.lift is not None else dur * 0.62
rng = np.random.default_rng(seed)
def note(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); ai = min(n // 2, int(a * SR)); ri = min(n // 2, int(r * SR))
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e
def lp(x, fc):      # gentle low-pass in the frequency domain (fast, no per-sample loop)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); return np.fft.irfft(X / (1 + (f / fc) ** 2), len(x))
def saw(f, n, det=0.0): return 2 * ((np.arange(n) * f * (1 + det) / SR) % 1.0) - 1
def chord(deg):
    r = root + deg; third = 3 if deg in MINOR_ROOTS else 4
    return [r, r + third, r + 7]
def add(buf, s, x, l=1.0, r=1.0):
    n = min(len(x), N - s)
    if n > 0 and s >= 0: buf[s:s + n, 0] += x[:n] * l; buf[s:s + n, 1] += x[:n] * r
cache = {}
def pluck(m, n):
    if m not in cache:
        f = note(m); L = max(2, int(SR / f)); buf = rng.uniform(-1, 1, L); y = np.zeros(int(0.9 * SR))
        for i in range(len(y)):
            y[i] = buf[i % L]; buf[i % L] = 0.5 * (buf[i % L] + buf[(i + 1) % L]) * 0.996
        cache[m] = y
    return cache[m][:n]

out = np.zeros((N, 2))
bpm = A.bpm or (78 if style == "dark" else 104); beat = 60 / bpm; bar = 4 * beat
prog = PROGS[style][pname]
nbars = int(np.ceil(dur / bar))
for k in range(nbars):
    pos = k * bar; s = int(pos * SR); n = int(min(bar, dur - pos) * SR)
    if n <= 0: break
    last = k == nbars - 1
    ch = chord(0 if last else prog[k % 4]); open_ = pos + bar / 2 >= lift
    if style == "dark":
        pad = sum(saw(note(m), n, d) for m in ch for d in (-0.004, 0.004)) / 8
        if open_: pad += sum(saw(note(m + 12), n, d) for m in ch[:2] for d in (-0.003, 0.003)) / 14
        pad = lp(pad, 1500 if open_ else 900) * env(n, 0.04 if k == 0 else 0.5, 0.6)
        bass = np.sin(2 * np.pi * note(ch[0] - 12) * np.arange(n) / SR) * env(n, 0.03, 0.4) * 0.5
        add(out, s, pad * 0.55 + bass, 1.0, 0.82); add(out, s, pad * 0.1, 0.0, 1.0)
        for b in ([0, 2] if not open_ else [0, 1.5, 2, 3.5]):               # heartbeat, busier after the lift
            tt = np.arange(int(0.35 * SR)) / SR
            add(out, int((pos + b * beat) * SR), np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.55)
        if open_:                                                             # soft bell on the chord tones
            for j, m in enumerate(rng.permutation(ch + [ch[0] + 12])):
                tt = np.arange(int(0.7 * SR)) / SR
                add(out, int((pos + j * beat) * SR), np.sin(2 * np.pi * note(m + 12) * tt) * np.exp(-tt * 5) * 0.12, 0.4 + 0.2 * (j % 2), 0.6 - 0.2 * (j % 2))
    else:
        tones = ch + [ch[0] + 12]
        pat = [0, 1, 2, 3, 2, 1, 2, 3] if (seed + k // 4) % 2 == 0 else [0, 2, 1, 3, 0, 2, 3, 1]
        for j in range(8):                                                    # 8th-note arpeggio
            st = pos + j * beat / 2
            if st >= dur: break
            m = tones[pat[j]] + 12; p = pluck(m, int(0.9 * SR)) * 0.32; pan = 0.35 + 0.3 * (j % 2)
            add(out, int(st * SR), p, 1 - pan, pan)
            if open_ and j % 2 == 0: add(out, int(st * SR), pluck(m + 12, int(0.6 * SR)) * 0.14, pan, 1 - pan)
        pad = sum(np.sin(2 * np.pi * note(m) * np.arange(n) / SR) for m in ch) / 3 * env(n, 0.05 if k == 0 else 0.3, 0.4) * 0.12
        bass = np.sin(2 * np.pi * note(ch[0] - 24) * np.arange(n) / SR) * env(n, 0.02, 0.3) * 0.35
        add(out, s, pad + bass)
        step = beat / 2 if open_ else beat
        for b in np.arange(pos + beat / 2, min(pos + bar, dur), step):       # off-beat shaker, 8ths after the lift
            n2 = int(0.06 * SR); add(out, int(b * SR), rng.standard_normal(n2) * np.exp(-np.arange(n2) / SR * 70) * 0.05)
    if last:                                                                  # ring out on the root chord
        break
# hit on frame 0: low thump + bright chord pluck, so the first second has weight
tt = np.arange(int(0.5 * SR)) / SR
add(out, 0, np.sin(2 * np.pi * (48 + 70 * np.exp(-tt * 26)) * tt) * np.exp(-tt * 7) * 0.9)
for m in chord(prog[0]): add(out, 0, pluck(m + 12, int(0.9 * SR)) * 0.25)
# air
sh = lp(rng.standard_normal(N), 4000) * 0.03 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7))
out[:, 0] += sh; out[:, 1] += np.roll(sh, 900)
# no fade-in; 1 s fade-out
out *= np.minimum(1, (dur - t) / 1.0)[:, None]
out /= max(1e-9, np.abs(out).max()); out *= 0.5
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open(f"{ep}/music_raw.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
# level first (so the duck depth is real), then duck under the voice
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{ep}/music_raw.wav", "-af",
                f"highpass=f=45,aecho=0.8:0.6:70|140:0.22|0.12,loudnorm=I={A.level}:TP=-6:LRA=9", "-ar", str(SR), f"{ep}/_m.wav"], check=True)
with wave.open(f"{ep}/_m.wav") as w: m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, 2) / 32768
m = m[:N] if len(m) >= N else np.vstack([m, np.zeros((N - len(m), 2))])
vr = np.interp(np.arange(N) / SR, np.arange(len(v)) / vsr, np.abs(v), right=0)
envv = lp(vr, 5); envv = np.clip(envv / max(1e-9, np.percentile(envv, 95)), 0, 1)
gain = 1 - 0.62 * np.clip(envv * 2.5, 0, 1)                                  # about -8 dB while the voice speaks
gain[: int(0.25 * SR)] = np.maximum(gain[: int(0.25 * SR)], np.linspace(1, 0.38, int(0.25 * SR)))   # let the frame-0 hit through
m *= gain[:, None]
with wave.open(f"{ep}/music.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(m, -1, 1) * 32767).astype(np.int16).tobytes())
os.remove(f"{ep}/_m.wav")
json.dump({"style": style, "bpm": bpm, "key": key, "prog": pname, "lift": round(lift, 2), "seed": int(seed)}, open(f"{ep}/music.json", "w"))
print(f"music {ep}: {style} {bpm:g} bpm, key {key}, prog {pname}, lift at {lift:.1f} s, {dur:.2f} s")
