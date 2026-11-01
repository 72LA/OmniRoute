import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gtts
gtts.MODEL = sys.argv[1]; voice = sys.argv[2]; gtts.STYLE = os.environ.get("TTS_STYLE", "")
L = json.load(open("script.json"))
for i, l in enumerate(L):
    fn = f"s{i:02d}.wav"
    if os.path.exists(fn): continue
    print(i, round(gtts.tts(l["say"], voice, fn), 2), flush=True); time.sleep(7)
