# malangenommen72 #06 – "Mal angenommen, du könntest nie wieder vergessen" – Dark line-art style.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes_luegen import D, IN, SCENE_CSS, follow  # shared dark helpers

KEYS = {"vergessen", "nie", "2006", "film", "100", "@malangenommen72", "gedankenexperimente", "last", "streit",
        "fehler", "1885", "ebbinghaus", "wichtige", "behalten", "kommentare", "superkraft"}

TITLES = {"hook": "MAL ANGENOMMEN", "film": "DAS GIBT ES WIRKLICH", "hundred": "HSAM", "burden": "GESCHENK ODER LAST?",
          "curve": "DIE VERGESSENSKURVE", "ask": "UND DU?"}

def hook(p, dur, lead):
    cal = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-cal" class="ln" pathLength="1" d="M330 760 H750 V1070 H330 Z M330 840 H750 M420 720 V790 M660 720 V790"/>
    </svg>
    <div id="{p}-day" class="big" style="top:900px;font-size:100px;font-family:var(--font-mono)">TAG 1</div>"""
    html = f'<div id="{p}-line" class="big" style="top:420px;font-size:96px;line-height:1.02">DU VERGISST<br/>NIE WIEDER<br/>ETWAS.</div>' + cal
    js = (D(f"#{p}-cal", 0.2, 0.8)
          + f'const {p}o = {{v: 1}}; tl.fromTo({p}o, {{v: 1}}, {{v: 9999, duration: {max(2.0, dur - 0.8)}, ease: "power2.in", onUpdate: () => {{ document.querySelector("#{p}-day").textContent = "TAG " + Math.round({p}o.v); }}}}, 0.6);')
    return html, js

def film(p, dur, lead):
    holes = "".join(f'<rect x="{120 + k*105}" y="565" width="40" height="26" rx="5" fill="none" stroke="#fff" stroke-width="3"/>'
                    f'<rect x="{120 + k*105}" y="905" width="40" height="26" rx="5" fill="none" stroke="#fff" stroke-width="3"/>' for k in range(9))
    frames = "".join(f'<path class="ln {p}-fr" pathLength="1" d="M{110 + k*290} 610 H{360 + k*290} V885 H{110 + k*290} Z"/>' for k in range(3))
    dates = ["03.02.1980", "14.07.1986", "29.08.1994"]
    lbls = "".join(f'<div class="mono {p}-dt" style="position:absolute;left:{110 + k*290}px;width:250px;text-align:center;top:725px;color:#fff;font-size:30px">{d}</div>' for k, d in enumerate(dates))
    html = f"""
    <div id="{p}-strip" style="position:absolute;left:0;top:0;width:1080px;height:1920px">
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-edge" class="ln" pathLength="1" d="M60 550 H1020 M60 945 H1020"/>
      {holes}{frames}
    </svg>{lbls}</div>
    <div id="{p}-src" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1000px">2006 · PARKER, CAHILL &amp; McGAUGH</div>
    """
    js = (D(f"#{p}-edge", lead, 0.6) + D(f".{p}-fr", lead + 0.3, 0.5)
          + f'tl.fromTo(".{p}-dt", {{opacity: 0}}, {{opacity: 1, duration: 0.2, stagger: 0.25}}, {lead + 0.7});'
          + IN(f"#{p}-src", lead + 0.5)
          + f'tl.fromTo("#{p}-strip", {{x: 0}}, {{x: -180, duration: {max(1.0, dur - lead - 1.2)}, ease: "none"}}, {lead + 1.2});')
    return html, js

def hundred(p, dur, lead):
    dots = "".join(f'<circle class="{p}-d" cx="{190 + (i % 10)*78}" cy="{500 + (i // 10)*48}" r="14" fill="#fff"/>' for i in range(100))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">{dots}</svg>
    <div id="{p}-n" class="big" style="top:1020px;font-size:64px;font-weight:900">100+ MENSCHEN</div>
    <div class="mono" style="position:absolute;left:0;right:0;text-align:center;top:970px">LAUT BERICHTEN · HIGHLY SUPERIOR AUTOBIOGRAPHICAL MEMORY</div>
    """
    js = (f'tl.fromTo(".{p}-d", {{opacity: 0, scale: 0, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.2, stagger: 0.012, ease: "back.out(1.6)"}}, {lead});'
          + IN(f"#{p}-n", lead + 1.4))
    return html, js

def burden(p, dur, lead):
    words = ["STREIT", "PEINLICH", "ABSCHIED", "FEHLER", "KRANKHEIT"]
    boxes = "".join(f'<path class="ln {p}-bx{k}" pathLength="1" d="M{300 + (k%2)*40} {960 - k*95} h{440 - (k%2)*80} v85 h-{440 - (k%2)*80} Z"/>' for k in range(5))
    lbl = "".join(f'<div class="mono {p}-t{k}" style="position:absolute;left:{300 + (k%2)*40}px;width:{440 - (k%2)*80}px;text-align:center;top:{960 - k*95 + 24}px;color:#fff;font-size:32px">{w}</div>' for k, w in enumerate(words))
    html = f'<svg style="left:0;top:0" width="1080" height="1920">{boxes}</svg>{lbl}'
    per = max(0.6, (dur - lead - 1.0) / 5)
    js = "".join(D(f".{p}-bx{k}", lead + 1.2 + k * per, 0.35) + IN(f".{p}-t{k}", lead + 1.35 + k * per) for k in range(5))
    return html, js

def curve(p, dur, lead):
    import math
    x0, y0, w, h = 170, 990, 760, 460
    pts = " ".join(f"{'M' if k == 0 else 'L'}{x0 + w*k/60:.1f} {y0 - h*(0.22 + 0.78*math.exp(-k/9)):.1f}" for k in range(61))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-ax" class="ln" pathLength="1" d="M{x0} {y0 - h - 30} V{y0} H{x0 + w + 20}"/>
      <path id="{p}-cv" class="ln" pathLength="1" style="stroke-width:9" d="{pts}"/>
      <path id="{p}-keep" class="ln thin" pathLength="1" style="stroke-dasharray:1" d="M{x0} {y0 - h*0.22} H{x0 + w}"/>
    </svg>
    <div class="mono" style="position:absolute;left:{x0 - 10}px;top:{y0 - h - 80}px;color:#fff">BEHALTEN</div>
    <div class="mono" style="position:absolute;left:{x0 + w - 90}px;top:{y0 + 18}px;color:#fff">ZEIT →</div>
    <div id="{p}-w" class="mono" style="position:absolute;left:{x0 + w - 300}px;top:{y0 - h*0.22 - 52}px;color:#fff">DAS WICHTIGE</div>
    <div id="{p}-src" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1070px">1885 · HERMANN EBBINGHAUS (VEREINFACHT)</div>
    """
    js = (D(f"#{p}-ax", lead, 0.5) + D(f"#{p}-cv", lead + 0.8, max(1.5, (dur - lead) * 0.45), "power1.inOut")
          + IN(f"#{p}-src", lead + 0.8) + D(f"#{p}-keep", lead + (dur - lead) * 0.7, 0.5) + IN(f"#{p}-w", lead + (dur - lead) * 0.72))
    return html, js

def ask(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-b1" class="ln" pathLength="1" d="M190 560 H890 V700 H190 Z"/>
      <path id="{p}-b2" class="ln" pathLength="1" d="M190 780 H890 V920 H190 Z"/>
    </svg>
    <div id="{p}-t1" class="big" style="top:600px;font-size:56px;font-weight:900">ALLES BEHALTEN</div>
    <div id="{p}-t2" class="big" style="top:820px;font-size:56px;font-weight:900">MANCHES VERGESSEN</div>
    <div id="{p}-c" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1010px;color:#fff;font-size:32px">↓ SCHREIB'S IN DIE KOMMENTARE</div>
    """
    js = (D(f"#{p}-b1", lead, 0.45) + IN(f"#{p}-t1", lead + 0.3) + D(f"#{p}-b2", lead + 0.9, 0.45) + IN(f"#{p}-t2", lead + 1.2)
          + IN(f"#{p}-c", lead + 2.0))
    return html, js

SCENES = {"hook": hook, "film": film, "hundred": hundred, "follow": follow, "burden": burden, "curve": curve, "ask": ask}

SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 1, 0.7, 0.4), ("pop", 2, 1.4, 0.45), ("pop", 3, 0.9, 0.5),
       ("click-soft", 4, 1.4, 0.35), ("click-soft", 4, 2.8, 0.35), ("click-soft", 4, 4.2, 0.35),
       ("whoosh-short", 5, 0.0, 0.4), ("pop", 6, 0.3, 0.45), ("pop", 6, 1.2, 0.45)]
