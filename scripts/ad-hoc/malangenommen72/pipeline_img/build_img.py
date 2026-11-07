"""Build an image-driven HyperFrames 9:16 short (I-Mind level): generated illustrations + camera moves + flash cuts
+ particles + one big word at a time + hook box + follow pill + loop end.

usage: python3 build_img.py <episode_dir> <project_dir> <style dark|vivid> <stamp text> <beats_module> <img_dir>
beats module: BEATS = [{"img": "a01", "at": (sentence, word_idx), "move": "push|pull|pan-l|pan-r|up|down", "flash": bool, "ov": fn|None}]
              KEYS (lowercase words to highlight), HOOK (list of lines for the text box), FOLLOW (handle), SFX [(name, (s, w), vol)]
"""
import importlib.util, json, os, re, shutil, subprocess, sys, random, wave
from PIL import Image

EPD, PRJ, STYLE, STAMP, MOD, IMGD = sys.argv[1:7]
SFXDIR = "/root/.claude/plugins/marketplaces/hyperframes/skills/media-use/audio/assets/sfx"
spec = importlib.util.spec_from_file_location("beats", MOD); bm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bm)
lines = json.load(open(f"{EPD}/script.json")); segs = json.load(open(f"{EPD}/segs_abs.json"))
TOTAL = round(segs[-1][1] + 1.5, 2)
with wave.open(f"{EPD}/full_voice.wav") as f: VODUR = round(f.getnframes() / f.getframerate(), 3)
W, H = 1080, 1920
DARK = STYLE == "dark"
os.makedirs(f"{PRJ}/compositions", exist_ok=True); os.makedirs(f"{PRJ}/assets/sfx", exist_ok=True); os.makedirs(f"{PRJ}/assets/img", exist_ok=True)
shutil.copy(f"{EPD}/full_voice.wav", f"{PRJ}/assets/voice.wav")
os.makedirs(f"{PRJ}/assets/fonts", exist_ok=True); shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts/Anton-Regular.ttf"), f"{PRJ}/assets/fonts/Anton-Regular.ttf")
FONTFACE = "@font-face{font-family:'Anton';src:url('assets/fonts/Anton-Regular.ttf') format('truetype');font-weight:400;font-style:normal}"

# ---------- word timing (proportional to letters inside each sentence) ----------
words = []   # (sentence, idx, text, t0, t1)
for si, ((a, b), l) in enumerate(zip(segs, lines)):
    ws = l["show"].split(); wt = [len(re.sub(r"\W", "", w)) + 2.2 + (2.5 if w[-1] in ",.?!:" else 0) for w in ws]; tot = sum(wt); t = a
    for wi, w in enumerate(ws):
        d = (b - a) * wt[wi] / tot; words.append((si, wi, w, round(t, 3), round(t + d, 3))); t += d
def T(at):
    s, w = at
    for x in words:
        if x[0] == s and x[1] == w: return x[3]
    raise KeyError(at)

# ---------- images ----------
for bt in bm.BEATS:
    src = f"{IMGD}/{bt['img']}.webp"; dst = f"{PRJ}/assets/img/{bt['img']}.jpg"
    if not os.path.exists(dst):
        im = Image.open(src).convert("RGB")
        r = max(1188 / im.width, 2112 / im.height)          # 10 % headroom for camera moves
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, t = (im.width - 1188) // 2, (im.height - 2112) // 2
        im.crop((l, t, l + 1188, t + 2112)).save(dst, quality=92)

MOVES = {"push": ({"scale": 1.0}, {"scale": 1.09}), "pull": ({"scale": 1.09}, {"scale": 1.0}),
         "pan-l": ({"x": 30, "scale": 1.03}, {"x": -30, "scale": 1.06}), "pan-r": ({"x": -30, "scale": 1.03}, {"x": 30, "scale": 1.06}),
         "up": ({"y": 40, "scale": 1.04}, {"y": -40, "scale": 1.06}), "down": ({"y": -40, "scale": 1.04}, {"y": 40, "scale": 1.06})}
def js_obj(d): return "{" + ", ".join(f"{k}: {v}" for k, v in d.items()) + "}"

starts = [0.0 if i == 0 else T(bt["at"]) for i, bt in enumerate(bm.BEATS)]
hosts, flashes = [], []
for i, bt in enumerate(bm.BEATS):
    sid = f"b{i}"; st = round(starts[i], 3); en = round(starts[i + 1], 3) if i + 1 < len(starts) else TOTAL; dur = round(en - st, 3)
    fr, to = MOVES[bt.get("move", "push")]
    ov_html, ov_js = bt["ov"](sid, dur) if bt.get("ov") else ("", "")
    open(f"{PRJ}/compositions/{sid}.html", "w").write(f"""<template>
  <style>
    {FONTFACE}
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: 'Montserrat'; }}
    #{sid}-img {{ position: absolute; left: -54px; top: -96px; width: 1188px; height: 2112px; transform-origin: 50% 45%; }}
    .ovl {{ position: absolute; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    <img id="{sid}-img" src="assets/img/{bt['img']}.jpg" alt="" />
    {ov_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{sid}-img", {js_obj(fr)}, {{...{js_obj(to)}, duration: {dur}, ease: "sine.inOut"}}, 0);
    tl.fromTo("#{sid}-img", {{filter: "brightness(1.6) blur(6px)"}}, {{filter: "brightness(1) blur(0px)", duration: 0.28, ease: "power2.out"}}, 0);
    {ov_js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
""")
    hosts.append(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    if bt.get("flash") and i > 0: flashes.append(st)

# ---------- fx layer: flashes, particles, vignette, hook box, follow pill, loop box ----------
random.seed(7)
pcol = "#ffffff" if DARK else "#ffe27a"
parts = "".join(f'<i class="pt" style="left:{random.randint(0,1070)}px;top:{random.randint(200,1800)}px;width:{s}px;height:{s}px;opacity:{random.uniform(.25,.7):.2f}"></i>'
                for s in [random.choice([3, 4, 5, 6, 8]) for _ in range(46)])
hook_end = segs[0][1] + 0.25
box_bg, box_fg = ("#fff", "#000")
hook = "".join(f"<div>{l}</div>" for l in bm.HOOK)
fx_js = ['tl.set("#fl", {opacity: 0}, 0);', f'tl.fromTo(".pt", {{y: 0}}, {{y: -260, duration: {TOTAL}, ease: "none", stagger: {{each: 0.05, from: "random"}}}}, 0);',
         f'tl.fromTo("#hook", {{scale: 0.92, opacity: 1}}, {{scale: 1, duration: 0.35, ease: "back.out(1.7)"}}, 0);',
         f'tl.to("#hook", {{opacity: 0, y: -30, duration: 0.25}}, {hook_end});']
for k, t in enumerate(flashes):
    fx_js.append(f'tl.to("#fl", {{opacity: 0.85, duration: 0.06}}, {t - 0.04});tl.to("#fl", {{opacity: 0, duration: 0.22}}, {t + 0.03});')
ft = T(bm.FOLLOW_AT)
fx_js.append(f'tl.fromTo("#fol", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)"}}, {ft});tl.to("#fol", {{opacity: 0, duration: 0.25}}, {ft + 2.0});')
fx_js.append(f'tl.fromTo("#loop", {{opacity: 0, scale: 0.9}}, {{opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.7)"}}, {segs[-1][1] + 0.05});')
vign = ("radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)")
fol_bg = "#fff" if DARK else "#ff4fa3"; fol_fg = "#000" if DARK else "#fff"
open(f"{PRJ}/compositions/fx.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; font-family: 'Montserrat'; }}
    #vg {{ position: absolute; inset: 0; background: {vign}; }}
    .pt {{ position: absolute; border-radius: 50%; background: {pcol}; box-shadow: 0 0 10px {pcol}; }}
    #fl {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}
    .box {{ position: absolute; left: 90px; right: 90px; top: 300px; background: {box_bg}; color: {box_fg}; border-radius: 18px; padding: 22px 26px;
            text-align: center; font-weight: 900; font-size: 58px; line-height: 1.12; box-shadow: 0 10px 40px rgba(0,0,0,.45); }}
    #loop {{ opacity: 0; }}
    #fol {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; opacity: 0; }}
    #fol span {{ display: inline-block; background: {fol_bg}; color: {fol_fg}; font-weight: 900; font-size: 40px; border-radius: 50px; padding: 14px 34px; box-shadow: 0 8px 30px rgba(0,0,0,.4); }}
    #stamp {{ position: absolute; left: 0; right: 0; top: 196px; text-align: center; }}
    #stamp span {{ font-weight: 800; font-size: 28px; letter-spacing: .3em; color: #fff; background: rgba(0,0,0,.45); border: 2px solid rgba(255,255,255,.6); border-radius: 8px; padding: 8px 20px; }}
  </style>
  <div id="root" data-composition-id="fx" data-width="{W}" data-height="{H}">
    <div id="vg"></div>{parts}<div id="fl"></div>
    <div id="stamp"><span>{STAMP}</span></div>
    <div id="hook" class="box">{hook}</div>
    <div id="loop" class="box">{hook}</div>
    <div id="fol"><span>+ FOLGEN {bm.FOLLOW}</span></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {"".join(fx_js)}
    window.__timelines["fx"] = tl;
  </script>
</template>
""")

# ---------- one big word at a time ----------
key_css = (".wd.key{color:#000;background:#fff;padding:0 22px;-webkit-text-stroke:0;text-shadow:none;border-radius:10px}" if DARK
           else ".wd.key{color:#ffd23f}")
cap, cj = [], []
for k, (si, wi, w, t0, t1) in enumerate(words):
    nxt = words[k + 1][3] if k + 1 < len(words) else t1 + 0.3
    end = min(nxt, t1 + 0.35) if si == (words[k + 1][0] if k + 1 < len(words) else si) else t1 + 0.15
    key = re.sub(r"[,.?!:„“\"']", "", w).lower() in bm.KEYS
    cap.append(f'<div id="w{k}" class="wd{" key" if key else ""}">{w.rstrip(",.:;")}</div>')
    cj.append(f'tl.set("#w{k}", {{visibility: "visible"}}, {t0});tl.fromTo("#w{k}", {{scale: 1.35, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.12, ease: "power3.out"}}, {t0});'
              f'tl.set("#w{k}", {{visibility: "hidden"}}, {round(end, 3)});')
open(f"{PRJ}/compositions/caps.html", "w").write(f"""<template>
  <style>
    {FONTFACE}
    #root {{ position: absolute; inset: 0; }}
    .wd {{ position: absolute; left: 50%; top: 1010px; transform: translateX(-50%); white-space: nowrap; visibility: hidden;
           font-family: 'Anton', 'Montserrat'; font-size: 132px; line-height: 1.1; color: #fff; letter-spacing: .01em; text-transform: none;
           -webkit-text-stroke: 12px #000; paint-order: stroke fill; text-shadow: 0 10px 30px rgba(0,0,0,.6); }}
    {key_css}
  </style>
  <div id="root" data-composition-id="caps" data-width="{W}" data-height="{H}">{"".join(cap)}</div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {"".join(cj)}
    window.__timelines["caps"] = tl;
  </script>
</template>
""")

# ---------- sfx ----------
tags = []
for k, (name, at, vol) in enumerate(bm.SFX):
    shutil.copy(f"{SFXDIR}/{name}.mp3", f"{PRJ}/assets/sfx/{name}.mp3")
    t = 0.0 if at is None else round(T(at), 3)
    fd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SFXDIR}/{name}.mp3"], capture_output=True, text=True).stdout)
    tags.append(f'<audio id="fx{k}" class="clip" src="assets/sfx/{name}.mp3" data-start="{t}" data-duration="{round(min(fd, TOTAL - t), 3)}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')
for k, t in enumerate(flashes):
    shutil.copy(f"{SFXDIR}/whoosh-short.mp3", f"{PRJ}/assets/sfx/whoosh-short.mp3")
    tags.append(f'<audio id="wh{k}" class="clip" src="assets/sfx/whoosh-short.mp3" data-start="{round(max(0, t - 0.12), 3)}" data-duration="0.5" data-track-index="{40 + k}" data-volume="0.28"></audio>')

open(f"{PRJ}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
      {chr(10).join(hosts)}
      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{VODUR}" data-track-index="5" data-volume="1"></audio>
      {chr(10).join(tags)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""")
print("built", PRJ, "duration", TOTAL, "beats", len(hosts), "words", len(words), "flashes", len(flashes))
for (si, wi, w, t0, t1) in words: print(f"{si}.{wi} {t0:6.2f} {w}")
