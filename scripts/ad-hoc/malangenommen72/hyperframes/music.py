"""Own royalty-free background music (procedural), ducked under the voice.
usage: python3 music.py <episode_dir> dark|bright [bpm]  -> <episode_dir>/music.wav (48 kHz stereo, length = voice + 1.6 s)"""
import sys, wave, subprocess, numpy as np
ep, style = sys.argv[1], sys.argv[2]
SR = 48000
with wave.open(f"{ep}/full_voice.wav") as w: vsr = w.getframerate(); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
dur = len(v) / vsr + 1.6; N = int(dur * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
def note(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); ai = min(n // 2, int(a * SR)); ri = min(n // 2, int(r * SR))
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e
def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
def saw(f, n, det=0.0):
    ph = (np.arange(n) * f * (1 + det) / SR) % 1.0; return 2 * ph - 1
out = np.zeros((N, 2))
if style == "dark":
    bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 78; beat = 60 / bpm; bar = 4 * beat
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]          # Am F C G
    k = 0; pos = 0.0
    while pos < dur:
        ch = prog[k % 4]; n = int(min(bar, dur - pos) * SR); s = int(pos * SR)
        pad = sum(saw(note(m), n, d) for m in ch for d in (-0.004, 0.004)) / 8
        pad = lp(pad, 900) * env(n, 0.6, 0.6)
        bass = np.sin(2 * np.pi * note(ch[0] - 12) * np.arange(n) / SR) * env(n, 0.05, 0.4) * 0.5
        out[s:s + n, 0] += pad * 0.55 + bass; out[s:s + n, 1] += pad * 0.45 + bass
        pos += bar; k += 1
    # soft heartbeat pulse on 1 and 3
    for b in np.arange(0, dur, 2 * beat):
        s = int(b * SR); n = min(int(0.35 * SR), N - s)
        if n <= 0: break
        tt = np.arange(n) / SR; kick = np.sin(2 * np.pi * (55 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9) * 0.55
        out[s:s + n] += kick[:, None]
    # airy shimmer
    sh = lp(rng.standard_normal(N), 4000) * 0.03 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 7))
    out[:, 0] += sh; out[:, 1] += np.roll(sh, 900)
else:
    bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 104; beat = 60 / bpm; bar = 4 * beat
    prog = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]   # C G Am F
    def pluck(f, n):
        L = max(2, int(SR / f)); buf = rng.uniform(-1, 1, L); y = np.zeros(n)
        for i in range(n):
            y[i] = buf[i % L]; buf[i % L] = 0.5 * (buf[i % L] + buf[(i + 1) % L]) * 0.996
        return y
    cache = {}
    k = 0; pos = 0.0
    while pos < dur:
        ch = prog[k % 4]
        for j in range(8):                                    # 8th-note arpeggio
            st = pos + j * beat / 2
            if st >= dur: break
            m = ch[[0, 1, 2, 3, 2, 1, 2, 3][j]] + 12; s = int(st * SR); n = min(int(0.9 * SR), N - s)
            if m not in cache: cache[m] = pluck(note(m), int(0.9 * SR))
            p = cache[m][:n] * 0.32; pan = 0.35 + 0.3 * (j % 2)
            out[s:s + n, 0] += p * (1 - pan); out[s:s + n, 1] += p * pan
        n = int(min(bar, dur - pos) * SR); s = int(pos * SR)
        pad = sum(np.sin(2 * np.pi * note(m) * np.arange(n) / SR) for m in ch[:3]) / 3 * env(n, 0.3, 0.4) * 0.12
        bass = np.sin(2 * np.pi * note(ch[0] - 24) * np.arange(n) / SR) * env(n, 0.02, 0.3) * 0.35
        out[s:s + n] += (pad + bass)[:, None]
        pos += bar; k += 1
    for b in np.arange(beat / 2, dur, beat):                  # soft off-beat shaker
        s = int(b * SR); n = min(int(0.06 * SR), N - s)
        if n <= 0: break
        hh = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 70) * 0.05
        out[s:s + n] += hh[:, None]
# fade in/out, normalize
out *= np.minimum(1, t / 0.4)[:, None] * np.minimum(1, (dur - t) / 1.2)[:, None]
out /= max(1e-9, np.abs(out).max()); out *= 0.5
# duck under the voice (sidechain from the voice envelope)
vr = np.interp(np.arange(N) / SR, np.arange(len(v)) / vsr, np.abs(v), right=0)
envv = lp(vr, 6); envv = envv / max(1e-9, envv.max())
gain = 1 - 0.6 * np.clip(envv * 3, 0, 1)
out *= gain[:, None]
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open(f"{ep}/music_raw.wav", "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{ep}/music_raw.wav", "-af", "aecho=0.8:0.6:70|140:0.25|0.15,loudnorm=I=-30:TP=-6:LRA=7", "-ar", "48000", f"{ep}/music.wav"], check=True)
print("music", ep, style, round(dur, 2), "s")
