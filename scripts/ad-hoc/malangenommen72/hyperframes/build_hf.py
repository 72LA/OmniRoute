"""Build a HyperFrames 9:16 project from script.json + segs_abs.json + full_voice.wav.

usage: python3 build_hf.py <episode_dir> <project_dir> <style line|flat> <ep "05"> <scenes_module>
The scenes module defines SCENES: {scene_name: fn(prefix, dur) -> (html, js)} and KEYS (set of lowercase words).
"""
import importlib.util, json, os, re, shutil, sys

EPD, PRJ, STYLE, EP, MOD = sys.argv[1:6]
HERE = os.path.dirname(os.path.abspath(__file__))
SFXDIR = os.environ.get("HF_SFX_DIR", "/root/.claude/plugins/marketplaces/hyperframes/skills/media-use/audio/assets/sfx")
spec = importlib.util.spec_from_file_location("scenes", MOD); sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)

lines = json.load(open(f"{EPD}/script.json"))
segs = json.load(open(f"{EPD}/segs_abs.json"))
WORDS = json.load(open(f"{EPD}/words.json")) if os.path.exists(f"{EPD}/words.json") else None   # from engine/voice.py: word-accurate timing
HOOKCARD = getattr(sc, "HOOKCARD", WORDS is not None)   # big kinetic hook line on frame 0 (needs word timing; opt-out: HOOKCARD = False)
TOTAL = round(segs[-1][1] + 1.6, 2)
import wave as _w
with _w.open(f"{EPD}/full_voice.wav") as _f: VODUR = round(_f.getnframes() / _f.getframerate(), 3)
W, H = 1080, 1920
LINE = STYLE in ("line", "dark2")
DARK2 = STYLE == "dark2"   # malangenommen72 Dark v2
KG = STYLE == "kg"   # AI72 house style (stylelab v3)
CHANNEL = "MAL ANGENOMMEN" if LINE else "AI72"

os.makedirs(f"{PRJ}/compositions", exist_ok=True); os.makedirs(f"{PRJ}/assets/sfx", exist_ok=True)
shutil.copy(f"{EPD}/full_voice.wav", f"{PRJ}/assets/voice.wav")

if LINE:
    CSS_VARS = "--ground:#000;--ink:#fff;--dim:#8a8a8a;--grid:#161616;--accent:#fff;--font-display:'Montserrat';--font-mono:'Space Mono';"
else:
    CSS_VARS = "--ground:#0e1a3d;--ink:#fff;--dim:#9fb0d8;--yellow:#ffd400;--pink:#ff4f8b;--cyan:#3ee0ff;--out:#0a0f24;--navy2:#1c2e64;--cream:#ffecd6;--font-display:'Montserrat';--font-mono:'Space Mono';"

# ---------------- hook card (frame 0) ----------------
def hook_phrases():
    """line 0 split at . ? ! , – into big phrases with their spoken start time (max ~16 characters per phrase)."""
    ws = [w for w in WORDS if w["line"] == 0]; out, cur = [], []
    for w in ws:
        cur.append(w)
        if w["w"][-1:] in ".?!,:–" or len(" ".join(c["w"] for c in cur)) >= 16:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [(round(p[0]["t0"], 3), round(p[-1]["t1"], 3), " ".join(c["w"] for c in p).rstrip(",").upper()) for p in out]

def fit_px(txt, wmax=800, top=132):
    return int(max(64, min(top, wmax / max(1, len(txt)) / 0.66)))

if DARK2 or LINE:
    HK_CSS = ".hk span{background:#fff;color:#000;padding:10px 30px 14px;border-radius:14px;box-shadow:0 0 44px rgba(255,255,255,.55)}"
else:
    HK_CSS = ".hk span{background:#ffd23f;color:#1b0f3d;padding:10px 32px 14px;border-radius:26px;box-shadow:10px 12px 0 #1b0f3d}"
HK_CSS += (".hk{position:absolute;left:0;right:0;top:268px;text-align:center;font-weight:900;line-height:1.1;opacity:0;white-space:nowrap;z-index:5}"
           ".hk span{display:inline-block}.flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none;z-index:6}")

# ---------------- scenes ----------------
hosts = []
for i, ((a, b), l) in enumerate(zip(segs, lines)):
    sid = f"s{i}"
    start = 0 if i == 0 else round(a, 3)
    end = round(segs[i + 1][0], 3) if i + 1 < len(segs) else TOTAL
    dur = round(end - start, 3)
    lead = round(a - start, 3)            # when the voice line starts inside the scene
    if KG:
        import kg_lib; kg_lib.PREFIX = f"{sid}_"
    html, js = sc.SCENES[l["scene"]](sid, dur, lead)
    title = sc.TITLES.get(l["scene"]) if i > 0 else None   # hook scene: no title – only the hook visual + text
    title_html = f'<div id="{sid}-title" class="title">{title}</div>' if title else ""
    title_js = (f'tl.fromTo("#{sid}-title", {{opacity: 0, filter: "blur(8px)"}}, {{opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out"}}, 0);'
                if title and i > 0 else "")
    if i == 0:   # punch-in on frame 0: motion from the very first frame
        title_js += f'tl.fromTo("#{sid}-wrap", {{scale: 1.12}}, {{scale: 1, duration: 0.45, ease: "expo.out"}}, 0);'
        if HOOKCARD:   # first second: flash on frame 0, one big hook phrase at a time on the spoken word, a camera jump on each phrase
            ph = hook_phrases()
            title_js += f'tl.fromTo("#{sid}-flash", {{opacity: 0.4}}, {{opacity: 0, duration: 0.2, ease: "power2.out", immediateRender: false}}, 0.034);'
            for k, (t0, t1, txt) in enumerate(ph):
                hid = f"{sid}-hk{k}"; t1 = ph[k + 1][0] if k + 1 < len(ph) else dur
                title_html += f'<div id="{hid}" class="hk" style="font-size:{fit_px(txt)}px"><span>{txt}</span></div>'
                if k == 0:
                    title_js += f'tl.fromTo("#{hid}", {{scale: 1.1, opacity: 1}}, {{scale: 1, opacity: 1, duration: 0.3, ease: "expo.out"}}, 0);'
                else:
                    z = 1.05 + 0.03 * (k % 2); ox = (42, 58)[k % 2]
                    title_js += (f'tl.set("#{hid}", {{opacity: 1}}, {t0});'
                                 f'tl.fromTo("#{hid}", {{scale: 1.16, rotation: {(-2, 2)[k % 2]}}}, {{scale: 1, rotation: 0, duration: 0.24, ease: "back.out(1.7)", immediateRender: false}}, {t0});'
                                 f'tl.fromTo("#{sid}-wrap", {{scale: {z + 0.07}, transformOrigin: "{ox}% 45%"}}, {{scale: {z}, duration: 0.4, ease: "expo.out", immediateRender: false}}, {t0});')
                if k + 1 < len(ph): title_js += f'tl.set("#{hid}", {{opacity: 0}}, {t1});'
            title_html += f'<div id="{sid}-flash" class="flash"></div>'
        html = f'<div id="{sid}-wrap" style="position:absolute;inset:0;transform-origin:50% 45%">{html}</div>'
    elif getattr(sc, "ENTER", True):   # every later scene lands on a move (cut on motion): slightly large + soft, settles in 0.34 s
        title_js += f'tl.fromTo("#{sid}-wrap", {{scale: 1.07, filter: "blur(10px)"}}, {{scale: 1, filter: "blur(0px)", duration: 0.34, ease: "expo.out"}}, 0);'
        html = f'<div id="{sid}-wrap" style="position:absolute;inset:0;transform-origin:50% 43%">{html}</div>'
    open(f"{PRJ}/compositions/{sid}.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: var(--font-display); color: var(--ink); }}
    .title {{ position: absolute; left: 0; right: 0; top: 250px; text-align: center; font-weight: 900; font-size: 84px; letter-spacing: -0.01em; line-height: 1.05; padding: 0 70px; }}
    {sc.SCENE_CSS}
    {HK_CSS}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    {title_html}
    {html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {title_js}
    {js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
""")
    hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{start}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')

# ---------------- captions ----------------
def chunks(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if len(" ".join(cur)) >= 14 or w.endswith((",", ".", "?", "!", ":", "“")) or len(cur) == 3:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

groups = []   # (start, end, [words], [word start times] or None)
if WORDS:      # word-accurate: every group opens on its first spoken word, every word lights up when it is said
    for li, l in enumerate(lines):
        if li == 0 and HOOKCARD: continue          # the hook line is the big card on top, not a caption
        ws = [w for w in WORDS if w["line"] == li]; cur = []
        for w in ws:
            cur.append(w)
            if len(" ".join(c["w"] for c in cur)) >= 14 or w["w"].endswith((",", ".", "?", "!", ":", "“")) or len(cur) == 3:
                groups.append((cur[0]["t0"], cur[-1]["t1"], [c["w"] for c in cur], [c["t0"] for c in cur])); cur = []
        if cur: groups.append((cur[0]["t0"], cur[-1]["t1"], [c["w"] for c in cur], [c["t0"] for c in cur]))
    for k in range(len(groups) - 1):               # hold each group until the next one starts (max 0.5 s after its last word)
        a, b, ws, ts = groups[k]; groups[k] = (a, min(groups[k + 1][0], b + 0.5), ws, ts)
else:
    for (a, b), l in zip(segs, lines):
        cs = chunks(l["show"]); tot = sum(len(" ".join(c)) + 4 for c in cs); t0 = a
        for c in cs:
            d = (b - a) * (len(" ".join(c)) + 4) / tot; groups.append((round(t0, 3), round(t0 + d, 3), c, None)); t0 += d

def word_html(w, wid=""):
    k = re.sub(r"[,.?!:„“\"]", "", w).lower() in sc.KEYS
    return f'<span {f'id="{wid}" ' if wid else ""}class="w{" key" if k else ""}">{w}</span>'

cap_divs, cap_js = [], []
for gi, (a, b, ws, ts) in enumerate(groups):
    gid = f"cg{gi}"
    cap_divs.append(f'<div id="{gid}" class="cg">{" ".join(word_html(w, f"{gid}w{k}" if ts else "") for k, w in enumerate(ws))}</div>')
    if ts:
        for k, t in enumerate(ts):
            dim = 1 if re.sub(r"[,.?!:„“\"]", "", ws[k]).lower() in sc.KEYS else 0.4   # key words keep their box/colour, they only pop
            if k: cap_js.append(f'tl.fromTo("#{gid}w{k}", {{opacity: {dim}, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.1, ease: "power3.out"}}, {round(t, 3)});')
    cap_js.append(f'tl.set("#{gid}", {{visibility: "visible", opacity: 1}}, {a});'
                  f'tl.fromTo("#{gid}", {{scale: 0.9}}, {{scale: 1, duration: 0.14, ease: "power3.out"}}, {a});'
                  f'tl.set("#{gid}", {{opacity: 0, visibility: "hidden"}}, {b + 0.04 if gi + 1 == len(groups) or groups[gi+1][0] > b + 0.04 else groups[gi+1][0]});')
if DARK2:
    cap_css = (".cg{position:absolute;left:0;right:0;top:1190px;text-align:center;font-family:var(--font-display);font-weight:800;font-size:80px;color:#fff;"
               "visibility:hidden;opacity:0;padding:0 70px;line-height:1.15;overflow:visible;text-shadow:0 0 16px rgba(255,255,255,.45)}"
               ".cg .w{display:inline-block}"
               ".cg .key{background:#fff;color:#000;padding:0 12px;text-shadow:none}")
elif LINE:
    cap_css = (".cg{position:absolute;left:0;right:0;top:1150px;text-align:center;font-family:var(--font-display);font-weight:800;font-size:76px;color:#fff;"
               "visibility:hidden;opacity:0;padding:0 80px;line-height:1.15;overflow:visible}"
               ".cg .key{background:#fff;color:#000;padding:0 12px}"
               ".cg .w:not(.key){-webkit-text-stroke:10px #000;paint-order:stroke fill}")
elif KG:
    cap_css = (".cg{position:absolute;left:0;right:0;top:1170px;text-align:center;font-family:var(--font-display);font-weight:900;font-size:82px;color:#fff;"
               "visibility:hidden;opacity:0;padding:0 70px;line-height:1.15;overflow:visible;text-shadow:0 6px 0 #1b0f3d}"
               ".cg .w{display:inline-block}"
               ".cg .key{color:#ffd23f}")
else:
    cap_css = (".cg{position:absolute;left:0;right:0;top:1150px;text-align:center;font-family:var(--font-display);font-weight:900;font-size:78px;color:#fff;"
               "visibility:hidden;opacity:0;padding:0 80px;line-height:1.15;overflow:visible;-webkit-text-stroke:12px #0a0f24;paint-order:stroke fill}"
               ".cg .key{color:#ffd400}")
open(f"{PRJ}/compositions/caps.html", "w").write(f"""<template>
  <style>#root {{ position: absolute; inset: 0; }} {cap_css}</style>
  <div id="root" data-composition-id="caps" data-width="{W}" data-height="{H}">
    {"".join(cap_divs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {"".join(cap_js)}
    window.__timelines["caps"] = tl;
  </script>
</template>
""")

# ---------------- sound effects ----------------
sfx_tags = []
for k, (name, si, off, vol) in enumerate(sc.SFX):
    shutil.copy(f"{SFXDIR}/{name}.mp3", f"{PRJ}/assets/sfx/{name}.mp3")
    t = round((segs[si][0] if si >= 0 else 0) + off, 3)
    import subprocess
    fd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SFXDIR}/{name}.mp3"], capture_output=True, text=True).stdout.strip())
    fd = round(min(fd, TOTAL - t), 3)
    sfx_tags.append(f'<audio id="fx{k}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}" data-duration="{fd}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')


# ---------------- fx: particles + soft light sweep between scenes (opt-in: sc.FX = True) ----------------
fx_host = ""
if getattr(sc, "FX", False):
    import random as _r
    _r.seed(11); pc = "#ffffff" if LINE else "#ffe27a"
    parts = "".join(f'<i class="pt" style="left:{_r.randint(0,1070)}px;top:{_r.randint(240,1700)}px;width:{s}px;height:{s}px;opacity:{_r.uniform(.15,.45):.2f}"></i>'
                    for s in [_r.choice([3, 4, 5, 6]) for _ in range(38)])
    sweep_js = "".join(f'tl.fromTo("#sw", {{x: -1400, opacity: 0.55}}, {{x: 1400, opacity: 0.55, duration: 0.42, ease: "power2.inOut"}}, {round(max(0, segs[i][0] - 0.22), 3)});'
                       for i in range(1, len(segs)))
    open(f"{PRJ}/compositions/fx.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .pt {{ position: absolute; border-radius: 50%; background: {pc}; box-shadow: 0 0 8px {pc}; }}
    #sw {{ position: absolute; top: 0; left: 0; width: 700px; height: 1920px; opacity: 0;
           background: linear-gradient(100deg, rgba(255,255,255,0) 0%, rgba(255,255,255,.16) 45%, rgba(255,255,255,.32) 50%, rgba(255,255,255,.16) 55%, rgba(255,255,255,0) 100%); }}
  </style>
  <div id="root" data-composition-id="fx" data-width="{W}" data-height="{H}">{parts}<div id="sw"></div></div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.set("#sw", {{opacity: 0}}, 0);
    tl.fromTo(".pt", {{y: 0}}, {{y: -220, duration: {TOTAL}, ease: "none", stagger: {{each: 0.04, from: "random"}}}}, 0);
    {sweep_js}
    window.__timelines["fx"] = tl;
  </script>
</template>
""")
    fx_host = f'<div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>'

# ---------------- progress bar on top: runs linearly 0 -> 100 % over the whole video (opt-out: sc.PROGRESS = False) ----------------
prog_host = ""
if getattr(sc, "PROGRESS", True):
    if LINE:
        trk, fill, glow, tick = "rgba(255,255,255,.16)", "#ffffff", "0 0 14px rgba(255,255,255,.85)", "rgba(0,0,0,.85)"
    else:
        trk, fill, glow, tick = "rgba(10,6,40,.55)", "linear-gradient(90deg,#3ee0ff 0%,#ffd23f 100%)", "0 0 14px rgba(255,210,63,.8)", "rgba(27,15,61,.9)"
    head = "#ffffff" if LINE else "#ffd23f"
    ticks = "".join(f'<i class="tk" style="left:{round(W * segs[i][0] / TOTAL) - 2}px"></i>' for i in range(1, len(segs)))
    open(f"{PRJ}/compositions/prog.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #pg-trk {{ position: absolute; left: 0; top: 0; width: {W}px; height: 14px; background: {trk}; }}
    #pg-fill {{ position: absolute; left: 0; top: 0; width: {W}px; height: 14px; background: {fill}; box-shadow: {glow}; transform-origin: 0 50%; transform: scaleX(0); }}
    .tk {{ position: absolute; top: 0; width: 4px; height: 14px; background: {tick}; }}
    #pg-head {{ position: absolute; left: -11px; top: -4px; width: 22px; height: 22px; border-radius: 50%; background: {head}; box-shadow: {glow}; }}
  </style>
  <div id="root" data-composition-id="prog" data-width="{W}" data-height="{H}">
    <div id="pg-trk"></div><div id="pg-fill"></div>{ticks}<div id="pg-head"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#pg-fill", {{scaleX: 0}}, {{scaleX: 1, duration: {TOTAL}, ease: "none"}}, 0);
    tl.fromTo("#pg-head", {{x: 0}}, {{x: {W}, duration: {TOTAL}, ease: "none"}}, 0);
    window.__timelines["prog"] = tl;
  </script>
</template>
""")
    prog_host = f'<div id="prog" data-composition-id="prog" data-composition-src="compositions/prog.html" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>'

music_tag = ""
if os.path.exists(f"{EPD}/music.wav"):   # own procedural bed, already ducked + at -30 LUFS
    shutil.copy(f"{EPD}/music.wav", f"{PRJ}/assets/music.wav")
    music_tag = f'<audio id="bgm" class="clip" src="assets/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="6" data-volume="1"></audio>'
# ---------------- background + stamp ----------------
if DARK2:
    import dark2_lib
    bg_css = """#bg{position:absolute;inset:0}
      #stamp{position:absolute;left:0;right:0;top:190px;text-align:center}
      #stamp span{font-family:var(--font-display);font-weight:600;font-size:28px;letter-spacing:.35em;color:#cfcfcf;border:2px solid #777;padding:8px 20px}"""
    bg_html = '<svg id="bg" width="1080" height="1920" viewBox="0 0 1080 1920">' + dark2_lib.background() + '</svg>'
elif LINE:
    bg_css = """#bg{position:absolute;inset:0;background-color:#000;
      background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:60px 60px}
      .mark{position:absolute;width:50px;height:50px;border-color:#777;border-style:solid;border-width:0}
      #stamp{position:absolute;left:0;right:0;top:186px;text-align:center}
      #stamp span{font-family:var(--font-mono);font-size:30px;color:#ccc;border:2px solid #aaa;padding:6px 18px;letter-spacing:.06em}"""
    bg_html = ('<div id="bg"></div>'
               '<div class="mark" style="left:40px;top:180px;border-left-width:3px;border-top-width:3px"></div>'
               '<div class="mark" style="right:40px;top:180px;border-right-width:3px;border-top-width:3px"></div>'
               '<div class="mark" style="left:40px;top:1290px;border-left-width:3px;border-bottom-width:3px"></div>'
               '<div class="mark" style="right:40px;top:1290px;border-right-width:3px;border-bottom-width:3px"></div>')
elif KG:
    import kg_lib; kg_lib.PREFIX = "bg_"
    bg_css = """#bg{position:absolute;inset:0}
      #stamp{position:absolute;left:0;right:0;top:186px;text-align:center}
      #stamp span{font-family:var(--font-display);font-weight:900;font-size:30px;color:#1b0f3d;background:#ffd23f;border-radius:30px;padding:8px 24px}"""
    bg_html = ('<svg id="bg" width="1080" height="1920" viewBox="0 0 1080 1920">' + kg_lib.background(3, (540, 780))
               + kg_lib.ground(1150) + kg_lib.ground_deco(1560) + '</svg>')
else:
    bg_css = """#bg{position:absolute;inset:0;background:linear-gradient(180deg,#0c1636 0%,#16285c 100%)}
      #bg i{position:absolute;border-radius:50%;background:#fff;opacity:.7}
      .deco{position:absolute}
      #stamp{position:absolute;left:0;right:0;top:186px;text-align:center}
      #stamp span{font-family:var(--font-display);font-weight:900;font-size:28px;color:#0a0f24;background:#ffd400;border:4px solid #0a0f24;border-radius:30px;padding:6px 22px}"""
    import random
    random.seed(4)
    stars = "".join(f'<i style="left:{random.randint(0,1070)}px;top:{random.randint(0,1910)}px;width:{s}px;height:{s}px"></i>'
                    for s in [random.choice([3, 4, 5, 6]) for _ in range(70)])
    deco = ('<svg class="deco" style="left:70px;top:1360px" width="70" height="70"><polygon points="35,5 65,60 5,60" fill="#ffd400" stroke="#0a0f24" stroke-width="6"/></svg>'
            '<svg class="deco" style="left:960px;top:420px" width="60" height="60"><circle cx="30" cy="30" r="22" fill="#ff4f8b" stroke="#0a0f24" stroke-width="6"/></svg>'
            '<svg class="deco" style="left:40px;top:600px" width="90" height="40"><path d="M5 20 Q 20 0 35 20 T 65 20 T 85 20" fill="none" stroke="#3ee0ff" stroke-width="9" stroke-linecap="round"/></svg>'
            '<svg class="deco" style="left:950px;top:1400px" width="60" height="60"><path d="M30 8 V52 M8 30 H52" stroke="#ffd400" stroke-width="10" stroke-linecap="round"/></svg>')
    bg_html = f'<div id="bg">{stars}</div>{deco}'

index = f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ {CSS_VARS} }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: var(--ground); }}
      #root {{ width: 100%; height: 100%; position: relative; font-family: var(--font-display); }}
      {bg_css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      {bg_html}
      <div id="stamp" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="0"><span>{CHANNEL} #{EP}</span></div>
      {chr(10).join(hosts)}
      {fx_host}
      {prog_host}
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>
      {music_tag}
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{VODUR}" data-track-index="5" data-volume="1"></audio>
      {chr(10).join(sfx_tags)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open(f"{PRJ}/index.html", "w").write(index)
print("built", PRJ, "duration", TOTAL, "scenes", len(hosts), "caption groups", len(groups))
