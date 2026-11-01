import base64, json, os, sys, urllib.request
MODEL = os.environ.get("ALIGN_MODEL", "gemini-3.8-flash")
fn, sentences = sys.argv[1], json.loads(sys.argv[2])
audio = base64.b64encode(open(fn, "rb").read()).decode()
prompt = ("Hier ist eine deutsche Sprachaufnahme. Sie enthält genau diese Sätze in dieser Reihenfolge:\n" +
          "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences)) +
          "\nGib für jeden Satz die Startzeit und Endzeit in Sekunden mit zwei Nachkommastellen an. "
          "Antworte nur mit JSON: [{\"n\":1,\"start\":0.00,\"end\":0.00}, ...]")
body = {"contents": [{"parts": [{"inline_data": {"mime_type": "audio/wav", "data": audio}}, {"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
r = json.load(urllib.request.urlopen(req, timeout=180))
print(r["candidates"][0]["content"]["parts"][0]["text"])
