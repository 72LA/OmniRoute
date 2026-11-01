import subprocess, sys, wave, numpy as np, re
src, dst, tempo = sys.argv[1], sys.argv[2], float(sys.argv[3])
with wave.open(src) as w: sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),np.int16)
log=subprocess.run(["ffmpeg","-v","info","-i",src,"-af","silencedetect=n=-40dB:d=0.28","-f","null","-"],capture_output=True,text=True).stderr
st=[float(v) for v in re.findall(r"silence_start: ([0-9.]+)",log)]; en=[float(v) for v in re.findall(r"silence_end: ([0-9.]+)",log)]
keep=[]; pos=0
for a,b in zip(st,en):
    if a<0.01: pos=int(max(0,b-0.05)*sr); continue
    if b>=len(x)/sr-0.01: keep.append(x[pos:int((a+0.15)*sr)]); pos=None; break
    keep.append(x[pos:int((a+0.11)*sr)]); pos=int((b-0.11)*sr)
if pos is not None: keep.append(x[pos:])
y=np.concatenate(keep)
with wave.open("_tmp.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","_tmp.wav","-af",f"atempo={tempo}",dst],check=True)
print(len(x)/sr, "->", len(y)/sr/tempo)
