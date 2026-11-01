import json, os, re, subprocess, sys, time, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gtts
gtts.MODEL = sys.argv[1]; voice = sys.argv[2]; groups = json.loads(sys.argv[3])
gtts.STYLE = os.environ.get("TTS_STYLE", "")
L = json.load(open("script.json"))
for k, g in enumerate(groups):
    fn = f"g{k}.wav"
    if not os.path.exists(fn):
        print("group", k, round(gtts.tts(" ".join(L[i]["say"] for i in g), voice, fn), 2), flush=True); time.sleep(5)
    with wave.open(fn) as w: sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    dur = len(x) / sr
    if len(g) == 1:
        cuts = []
    else:
        log = subprocess.run(["ffmpeg","-v","info","-i",fn,"-af","silencedetect=n=-35dB:d=0.12","-f","null","-"],capture_output=True,text=True).stderr
        st=[float(v) for v in re.findall(r"silence_start: ([0-9.]+)",log)]; en=[float(v) for v in re.findall(r"silence_end: ([0-9.]+)",log)]
        sil=[(a,b) for a,b in zip(st,en) if a>0.05 and b<dur-0.05]
        lead = st[0] == 0 and en[0] or 0
        chars=[len(L[i]["say"]) for i in g]; tot=sum(chars); c=0; prev=lead; cuts=[]
        for j in range(len(g)-1):
            c+=chars[j]; exp=lead+(dur-lead)*c/tot
            cands=[s for s in sil if s[0]>prev+0.5]
            best=min(cands,key=lambda s: abs((s[0]+s[1])/2-exp)-2.0*(s[1]-s[0]))
            cuts.append(best); prev=best[1]
    edges=[0]+[ (a+b)/2 for a,b in cuts ]+[dur]
    for j,i in enumerate(g):
        seg=x[int(edges[j]*sr):int(edges[j+1]*sr)]
        with wave.open(f"s{i:02d}.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(seg.tobytes())
        print(f"  s{i:02d} {edges[j]:6.2f}-{edges[j+1]:6.2f} {len(L[i]['say'])/(edges[j+1]-edges[j]):5.1f} ch/s  {L[i]['say'][:40]}")
