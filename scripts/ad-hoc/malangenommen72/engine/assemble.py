# usage (in episode dir): python3 ../engine/assemble.py <tempo> [echo_first]
import json, os, subprocess, sys, wave, numpy as np
ENG = os.path.dirname(os.path.abspath(__file__))
lines = json.load(open("script.json")); tempo = float(sys.argv[1]); echo_first = len(sys.argv) > 2
SR = 24000
LEAD = float(os.environ.get("VO_LEAD", "0.0"))   # voice starts on frame 0 (retention: biggest drop in second 1)
out = [np.zeros(int(LEAD * SR))]; segs = []; t = LEAD
for i, l in enumerate(lines):
    subprocess.run(["python3", f"{ENG}/tighten.py", f"s{i:02d}.wav", "_s.wav", str(tempo)], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "_s.wav", "-af",
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
        "-ar", str(SR), "-ac", "1", "_t.wav"], check=True)
    with wave.open("_t.wav") as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    d = len(x) / SR
    if i == 0 and echo_first:
        y = np.zeros(len(x) + int(0.6 * SR)); y[:len(x)] += x
        for delay, g in [(0.22, 0.55), (0.44, 0.3)]:
            s = int(delay * SR); y[s:s + len(x)] += x * g
        x = y
    segs.append([round(t, 3), round(t + d, 3)]); out.append(x); t += len(x) / SR
    if i < len(lines) - 1:
        g = float(os.environ.get("VO_GAP", "0.09"))   # was 0.3/0.2 s – no dead air between sentences
        out.append(np.zeros(int(g * SR))); t += g
y = np.concatenate(out); y = y / max(1, np.abs(y).max()) * 30000
with wave.open("full_voice.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.astype(np.int16).tobytes())
json.dump(segs, open("segs_abs.json", "w"))
for s, l in zip(segs, lines): print(f"{s[0]:6.2f}-{s[1]:6.2f} {len(l['say'])/(s[1]-s[0]):5.1f} ch/s {l['say'][:45]}")
print("total", round(t, 2))
