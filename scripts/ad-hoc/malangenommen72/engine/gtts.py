import base64, json, os, sys, time, urllib.request, wave
MODEL = os.environ.get("TTS_MODEL", "gemini-3.8-flash-tts")
KEY = os.environ["GEMINI_API_KEY"]
STYLE = ""
def tts(text, voice, out):
    body = {"contents": [{"parts": [{"text": STYLE + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
              "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    for attempt in range(6):
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            part = r["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            rate = int(part["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in part["mimeType"] else 24000
            with wave.open(out, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
            return len(pcm) / 2 / rate
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]; print("HTTP", e.code, msg, file=sys.stderr)
            if e.code == 400: raise SystemExit(1)
            time.sleep(min(60, 8 * (attempt + 1)))
    raise SystemExit("TTS failed")
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "sample":
        voice = sys.argv[2]
        print(voice, tts("Forscher ließen Studenten ein peinliches T-Shirt tragen. Das Ergebnis überrascht.", voice, f"sample_{voice}.wav"))
    else:
        voice = sys.argv[2]; lines = json.load(open(sys.argv[3])); durs = []
        for i, s in enumerate(lines):
            d = tts(s["say"], voice, f"s{i:02d}.wav"); durs.append(d); print(i, round(d, 2), flush=True)
        json.dump(durs, open("durs.json", "w")); print(sum(durs))
