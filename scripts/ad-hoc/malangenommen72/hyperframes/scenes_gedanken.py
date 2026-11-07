# malangenommen72 #07 – "Mal angenommen, du könntest Gedanken lesen" – Dark line-art style.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes_luegen import D, IN, SCENE_CSS, follow

KEYS = {"gedanken", "lesen", "superkraft", "daneben", "20", "%", "drittel", "@malangenommen72", "gedankenexperimente",
        "chef", "date", "freunde", "privat", "gedankenexperiment", "kommentare"}
TITLES = {"hook": "MAL ANGENOMMEN", "easy": "OHNE SUPERKRAFT", "ickes": "WIE GUT LESEN WIR?", "reveal": "PLÖTZLICH WEISST DU ALLES",
          "lock": "LIEBER PRIVAT?", "ask": "UND DU?"}

def head(p, cx, cy, s=1.0, flip=False, cls=""):
    """outline head profile (facing right; flip=True faces left)."""
    f = -1 if flip else 1
    d = (f"M{cx - f*90*s} {cy + 150*s} V{cy + 60*s} C {cx - f*150*s} {cy - 10*s}, {cx - f*140*s} {cy - 170*s}, {cx} {cy - 170*s} "
         f"C {cx + f*120*s} {cy - 170*s}, {cx + f*150*s} {cy - 80*s}, {cx + f*140*s} {cy - 30*s} L {cx + f*175*s} {cy + 30*s} "
         f"L {cx + f*140*s} {cy + 45*s} C {cx + f*140*s} {cy + 90*s}, {cx + f*110*s} {cy + 105*s}, {cx + f*60*s} {cy + 100*s} V{cy + 150*s}")
    return f'<path class="ln {cls}" pathLength="1" d="{d}"/>'

def bubble(cx, cy, w, h, cls, tail=(0, 1)):
    tx, ty = tail
    d = (f"M{cx - w/2 + 40} {cy - h/2} H{cx + w/2 - 40} Q{cx + w/2} {cy - h/2} {cx + w/2} {cy - h/2 + 40} V{cy + h/2 - 40} "
         f"Q{cx + w/2} {cy + h/2} {cx + w/2 - 40} {cy + h/2} H{cx - w/2 + 40} Q{cx - w/2} {cy + h/2} {cx - w/2} {cy + h/2 - 40} "
         f"V{cy - h/2 + 40} Q{cx - w/2} {cy - h/2} {cx - w/2 + 40} {cy - h/2} Z")
    dots = "".join(f'<circle class="{cls}-dot" cx="{cx + tx*(40 + k*36)}" cy="{cy + h/2 + 30 + k*34}" r="{14 - k*4}" fill="none" stroke="#fff" stroke-width="4"/>' for k in range(3))
    return f'<path class="ln {cls}" pathLength="1" d="{d}"/>{dots}'

def hook(p, dur, lead):
    html = f"""
    <div class="big" style="top:420px;font-size:92px;line-height:1.02">DU KANNST<br/>GEDANKEN<br/>LESEN.</div>
    <svg style="left:0;top:0" width="1080" height="1920">{head(p, 330, 930, 0.9, cls=p+"-h")}{bubble(700, 830, 360, 170, p+"-b", (-1, 1))}</svg>
    <div id="{p}-q" class="big" style="top:790px;left:520px;right:auto;width:360px;font-size:70px">? ? ?</div>
    """
    js = (D(f".{p}-h", 0.1, 0.8) + D(f".{p}-b", 0.6, 0.6)
          + f'tl.fromTo(".{p}-b-dot", {{opacity: 0}}, {{opacity: 1, duration: 0.15, stagger: 0.1}}, 0.5);' + IN(f"#{p}-q", 1.1))
    return html, js

def easy(p, dur, lead):
    html = f"""<svg style="left:0;top:0" width="1080" height="1920">
      {head(p, 260, 950, 0.75, cls=p+"-h1")}{head(p, 820, 950, 0.75, True, cls=p+"-h2")}
      {bubble(300, 640, 260, 140, p+"-b1", (0, 1))}{bubble(780, 640, 260, 140, p+"-b2", (0, 1))}</svg>
    <div id="{p}-t1" class="big" style="top:605px;left:170px;right:auto;width:260px;font-size:60px">?</div>
    <div id="{p}-t2" class="big" style="top:605px;left:650px;right:auto;width:260px;font-size:60px">?</div>
    <div id="{p}-x" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1080px;color:#fff">≠ SELTEN TREFFER</div>"""
    js = (D(f".{p}-h1", lead, 0.6) + D(f".{p}-h2", lead + 0.2, 0.6) + D(f".{p}-b1", lead + 0.6, 0.4) + D(f".{p}-b2", lead + 0.8, 0.4)
          + IN(f"#{p}-t1", lead + 1.0) + IN(f"#{p}-t2", lead + 1.1) + IN(f"#{p}-x", lead + 2.0))
    return html, js

def ickes(p, dur, lead):
    x0, w = 160, 760
    html = f"""<svg style="left:0;top:0" width="1080" height="1920">
      <path class="ln" id="{p}-f1" pathLength="1" d="M{x0} 600 H{x0 + w} V680 H{x0} Z"/>
      <path class="ln" id="{p}-f2" pathLength="1" d="M{x0} 860 H{x0 + w} V940 H{x0} Z"/>
      <rect id="{p}-b1" x="{x0 + 8}" y="608" width="{(w - 16) * 0.20}" height="64" fill="#fff" style="transform-origin:{x0}px 640px"/>
      <rect id="{p}-b2" x="{x0 + 8}" y="868" width="{(w - 16) * 0.33}" height="64" fill="#fff" style="transform-origin:{x0}px 900px"/>
    </svg>
    <div class="mono" style="position:absolute;left:{x0}px;top:545px;color:#fff;font-size:32px">FREMDE</div>
    <div class="mono" style="position:absolute;left:{x0}px;top:805px;color:#fff;font-size:32px">ENGE FREUNDE</div>
    <div id="{p}-v1" class="big" style="top:592px;left:{x0 + 200}px;right:auto;font-size:64px">≈ 20 %</div>
    <div id="{p}-v2" class="big" style="top:852px;left:{x0 + 300}px;right:auto;font-size:64px">≈ 1/3</div>
    <div class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1040px">WILLIAM ICKES · EMPATHIE-GENAUIGKEIT</div>"""
    t2 = lead + (dur - lead) * 0.62
    js = (D(f"#{p}-f1", lead, 0.5) + D(f"#{p}-f2", lead + 0.2, 0.5)
          + f'tl.fromTo("#{p}-b1", {{scaleX: 0}}, {{scaleX: 1, duration: 0.8, ease: "power3.out"}}, {lead + 2.5});' + IN(f"#{p}-v1", lead + 3.1)
          + f'tl.fromTo("#{p}-b2", {{scaleX: 0}}, {{scaleX: 1, duration: 0.8, ease: "power3.out"}}, {t2});' + IN(f"#{p}-v2", t2 + 0.6))
    return html, js

def reveal(p, dur, lead):
    labels = ["CHEF", "DATE", "FREUNDE"]
    html = '<svg style="left:0;top:0" width="1080" height="1920">'
    for k in range(3):
        html += bubble(540 + (k - 1) * 40, 520 + k * 200, 640, 150, f"{p}-b{k}", ((-1) ** k, 1))
    html += "</svg>"
    for k, l in enumerate(labels):
        html += f'<div class="{p}-t{k} big" style="top:{480 + k*200}px;font-size:56px;font-weight:900;opacity:0">{l}: „…“</div>'
    per = max(1.2, (dur - lead) / 3.6)
    js = ""
    for k in range(3):
        t = lead + 1.6 + k * per
        js += D(f".{p}-b{k}", t, 0.4) + f'tl.fromTo(".{p}-b{k}-dot", {{opacity: 0}}, {{opacity: 1, duration: 0.15, stagger: 0.08}}, {t});' + IN(f".{p}-t{k}", t + 0.3)
    return html, js

def lock(p, dur, lead):
    html = f"""<svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-sh"><path class="ln" id="{p}-shk" pathLength="1" style="stroke-width:14" d="M420 700 V600 Q420 480 540 480 Q660 480 660 600 V700"/></g>
      <path class="ln" id="{p}-body" pathLength="1" style="stroke-width:10" d="M360 700 H720 V980 H360 Z"/>
      <circle id="{p}-kh" cx="540" cy="820" r="22" fill="#fff" opacity="0"/><rect id="{p}-kb" x="532" y="830" width="16" height="70" fill="#fff" opacity="0"/>
    </svg>
    <div id="{p}-n" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1050px;color:#bbb">* NUR EIN GEDANKENEXPERIMENT</div>"""
    js = (D(f"#{p}-body", lead, 0.6) + D(f"#{p}-shk", lead + 0.3, 0.6)
          + f'tl.fromTo("#{p}-sh", {{y: -60}}, {{y: 0, duration: 0.35, ease: "power3.in"}}, {lead + 1.4});'
          + f'tl.to(["#{p}-kh", "#{p}-kb"], {{opacity: 1, duration: 0.2}}, {lead + 1.75});' + IN(f"#{p}-n", lead + (dur - lead) * 0.6))
    return html, js

def ask(p, dur, lead):
    html = f"""<svg style="left:0;top:0" width="1080" height="1920">{bubble(540, 700, 720, 360, p+"-b", (-1, 1))}</svg>
    <div id="{p}-t" class="big" style="top:610px;font-size:58px;font-weight:900;line-height:1.2">WESSEN GEDANKEN<br/>ZUERST?</div>
    <div id="{p}-c" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1040px;color:#fff;font-size:32px">↓ SCHREIB'S IN DIE KOMMENTARE</div>"""
    js = (D(f".{p}-b", lead, 0.6) + f'tl.fromTo(".{p}-b-dot", {{opacity: 0}}, {{opacity: 1, duration: 0.15, stagger: 0.1}}, {lead + 0.5});'
          + IN(f"#{p}-t", lead + 0.4) + IN(f"#{p}-c", lead + 1.4))
    return html, js

SCENES = {"hook": hook, "easy": easy, "ickes": ickes, "follow": follow, "reveal": reveal, "lock": lock, "ask": ask}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 1, 2.0, 0.4), ("pop", 2, 3.1, 0.45), ("pop", 2, 6.5, 0.45),
       ("pop", 3, 0.9, 0.5), ("click-soft", 4, 1.9, 0.35), ("click-soft", 4, 4.2, 0.35), ("click-soft", 4, 6.5, 0.35),
       ("click", 5, 1.75, 0.5), ("pop", 6, 0.4, 0.45)]
