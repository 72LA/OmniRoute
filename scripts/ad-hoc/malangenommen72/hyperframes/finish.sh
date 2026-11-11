#!/bin/bash
# usage: finish.sh <project_dir> [out_name]   – lint, check, render, then two-pass loudness (-14 LUFS, true peak <= -1.5 dBTP)
# HF = HyperFrames CLI (default: npx hyperframes). Single-pass loudnorm overshot to 0.0 dBFS on #17; two passes hold the peak.
set -e; HF="${HF:-npx hyperframes}"; cd "$1"; OUT="${2:-final.mp4}"
$HF lint | tail -3
$HF check --json > check.json 2>/dev/null || true
python3 - <<'PY'
import json
try:
    d = json.load(open("check.json")); s = json.dumps(d)
    print("check: errors", s.count('"severity": "error"') + s.count('"severity":"error"'), "warnings", s.count('"severity": "warning"') + s.count('"severity":"warning"'), "(details: check.json)")
except Exception as e: print("check: could not parse check.json –", e)
PY
$HF render --quality delivery -o out.mp4 | tail -2
M=$(ffmpeg -hide_banner -i out.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$M" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -v error -i out.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,alimiter=limit=0.84:level=false" -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^ +I:|Peak:" | tail -2 | tr -s ' ' | tr '\n' ' '; echo; echo "done: $1/$OUT"
