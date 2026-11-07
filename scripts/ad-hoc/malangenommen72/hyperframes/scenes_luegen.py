# malangenommen72 #05 – "Mal angenommen, niemand könnte mehr lügen" – Dark line-art style.
KEYS = {"niemand", "lügen", "1,65", "60", "%", "hälfte", "5", "@malangenommen72", "notlügen", "streit", "vertrauen",
        "gedankenexperiment", "welt", "kommentare", "gedankenexperimente"}

TITLES = {"hook": "MAL ANGENOMMEN", "avg": "WIE OFT LÜGEN WIR?", "skew": "WER LÜGT?", "white": "KEINE NOTLÜGEN MEHR",
          "scale": "BESSER ODER SCHLECHTER?", "ask": "UND DU?"}

SCENE_CSS = """
.ln { fill: none; stroke: #fff; stroke-width: 6; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
.thin { stroke-width: 3; }
.mono { font-family: var(--font-mono); color: var(--dim); font-size: 28px; letter-spacing: .05em; }
.big { font-weight: 900; text-align: center; position: absolute; left: 0; right: 0; }
svg { position: absolute; overflow: visible; }
"""

def D(sel, at, d=0.6, ease="power2.inOut"):
    return f'tl.fromTo("{sel}", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {d}, ease: "{ease}"}}, {at});'

def IN(sel, at, d=0.2, blur=8):
    return f'tl.fromTo("{sel}", {{opacity: 0, filter: "blur({blur}px)"}}, {{opacity: 1, filter: "blur(0px)", duration: {d}, ease: "power4.out"}}, {at});'

def hook(p, dur, lead):
    html = f"""
    <div id="{p}-line" class="big" style="top:430px;font-size:104px;line-height:1.02">NIEMAND<br/>KANN MEHR<br/>LÜGEN.</div>
    <svg id="{p}-svg" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
      <path id="{p}-bub" class="ln" pathLength="1" d="M190 760 H890 Q930 760 930 800 V1000 Q930 1040 890 1040 H420 L330 1110 L350 1040 H190 Q150 1040 150 1000 V800 Q150 760 190 760 Z"/>
      <path id="{p}-strike" class="ln" pathLength="1" style="stroke-width:10" d="M230 905 L850 895"/>
    </svg>
    <div id="{p}-lie" class="big" style="top:840px;font-size:96px;letter-spacing:.2em">LÜGE</div>
    """
    js = (D(f"#{p}-bub", 0.1, 0.7) + IN(f"#{p}-lie", 0.5) + D(f"#{p}-strike", 1.5, 0.35, "power3.out")
)
    return html, js

def avg(p, dur, lead):
    x0, x1, y = 140, 940, 960
    ticks = "".join(f'<path class="ln thin {p}-tk" pathLength="1" d="M{x0 + (x1-x0)*k/3} {y-18} V{y+18}"/>' for k in range(4))
    labels = "".join(f'<div class="mono" style="position:absolute;top:{y+40}px;left:{x0 + (x1-x0)*k/3 - 20}px">{k}</div>' for k in range(4))
    mx = x0 + (x1 - x0) * 1.65 / 3
    html = f"""
    <div id="{p}-num" class="big" style="top:470px;font-size:230px;letter-spacing:-.03em">0,00</div>
    <div id="{p}-unit" class="mono big" style="top:760px;font-size:34px">LÜGEN PRO TAG · DURCHSCHNITT</div>
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-axis" class="ln" pathLength="1" d="M{x0} {y} H{x1}"/>
      {ticks}
      <path id="{p}-mk" class="ln" pathLength="1" style="stroke-width:8" d="M{mx} {y-90} V{y-10} M{mx-22} {y-38} L{mx} {y-10} L{mx+22} {y-38}"/>
    </svg>
    {labels}
    <div id="{p}-src" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1080px;opacity:0">SEROTA ET AL., 2010 · ~1.000 ERWACHSENE, USA</div>
    """
    c = lead + (dur - lead) * 0.5
    js = (IN(f"#{p}-num", lead + 0.3) +
          f'const {p}o = {{v: 0}}; tl.fromTo({p}o, {{v: 0}}, {{v: 1.65, duration: 1.6, ease: "power3.out", onUpdate: () => {{ document.querySelector("#{p}-num").textContent = {p}o.v.toFixed(2).replace(".", ","); }}}}, {c});'
          + IN(f"#{p}-unit", lead + 0.6) + D(f"#{p}-axis", lead + 0.8, 0.6) + D(f".{p}-tk", lead + 1.1, 0.3)
          + D(f"#{p}-mk", c + 1.3, 0.45, "power3.out") + f'tl.fromTo("#{p}-src", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {lead + 1.0});')
    return html, js

def skew(p, dur, lead):
    dots = []
    for i in range(100):
        cx = 220 + (i % 10) * 71; cy = 440 + (i // 10) * 60
        cls = "z" if i < 60 else ("hv" if i >= 95 else "m")
        dots.append(f'<circle class="{p}-d {p}-{cls}" cx="{cx}" cy="{cy}" r="20" fill="none" stroke="#fff" stroke-width="4"/>')
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">{"".join(dots)}</svg>
    <div id="{p}-l1" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1065px;font-size:34px;color:#fff">60 % · HEUTE KEINE LÜGE</div>
    <div id="{p}-l2" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1065px;font-size:34px;color:#fff;opacity:0">5 % · FAST DIE HÄLFTE ALLER LÜGEN</div>
    """
    q = max(0.5, dur * 0.45)
    js = (f'tl.fromTo(".{p}-d", {{opacity: 0, scale: 0.4, transformOrigin: "50% 50%"}}, {{opacity: 1, scale: 1, duration: 0.25, stagger: 0.008, ease: "power3.out"}}, {lead});'
          + f'tl.to(".{p}-z", {{opacity: 0.22, duration: 0.3}}, {lead + 1.6});'
          + IN(f"#{p}-l1", lead + 1.6)
          + f'tl.to(".{p}-m", {{opacity: 0.22, duration: 0.3}}, {lead + q});'
          + f'tl.to(".{p}-hv", {{fill: "#fff", scale: 1.25, duration: 0.35, ease: "back.out(1.4)", transformOrigin: "50% 50%"}}, {lead + q});'
          + f'tl.to("#{p}-l1", {{opacity: 0, duration: 0.15}}, {lead + q});' + IN(f"#{p}-l2", lead + q + 0.1))
    return html, js

def follow(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <circle id="{p}-ring" class="ln" pathLength="1" cx="540" cy="630" r="190"/>
      <path id="{p}-moon" class="ln" pathLength="1" style="stroke-width:8" d="M520 495 A145 145 0 1 0 650 725 A116 116 0 1 1 520 495 Z"/>
    </svg>
    <div id="{p}-q" class="big" style="top:490px;left:620px;right:auto;font-size:150px;color:#000;-webkit-text-stroke:6px #fff">?</div>
    <div id="{p}-h" class="big" style="top:850px;font-size:64px;font-weight:800">@malangenommen72</div>
    <div id="{p}-btn" style="position:absolute;left:330px;top:950px;width:420px;height:96px;border:5px solid #fff;border-radius:48px;text-align:center;line-height:86px;font-weight:900;font-size:50px">+ FOLGEN</div>
    """
    js = (D(f"#{p}-ring", lead, 0.6) + D(f"#{p}-moon", lead + 0.25, 0.7) + IN(f"#{p}-q", lead + 0.7)
          + IN(f"#{p}-h", lead + 0.5) + f'tl.fromTo("#{p}-btn", {{scale: 0.6, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.4)"}}, {lead + 0.9});')
    return html, js

def white(p, dur, lead):
    quotes = ["„Das Essen ist lecker.“", "„Mir geht's gut.“", "„Schöne Frisur.“"]
    html = '<svg style="left:0;top:0" width="1080" height="1920">'
    for k in range(3):
        y = 470 + k * 210
        html += (f'<path class="ln {p}-b{k}" pathLength="1" d="M150 {y} H930 Q960 {y} 960 {y+30} V{y+120} Q960 {y+150} 930 {y+150} H260 L200 {y+190} L215 {y+150} H150 Q120 {y+150} 120 {y+120} V{y+30} Q120 {y} 150 {y} Z"/>'
                 f'<path class="ln {p}-x{k}" pathLength="1" style="stroke-width:8" d="M170 {y+78} L910 {y+72}"/>')
    html += "</svg>"
    for k, qt in enumerate(quotes):
        html += f'<div class="big {p}-t{k}" style="top:{470 + k*210 + 38}px;font-size:58px;font-weight:700">{qt}</div>'
    per = max(0.9, (dur - lead - 0.6) / 3.4)
    js = ""
    first = lead + per * 0.6
    for k in range(3):
        t = first + k * per
        js += D(f".{p}-b{k}", t, 0.45) + IN(f".{p}-t{k}", t + 0.25) + D(f".{p}-x{k}", t + per * 0.6, 0.3, "power3.out")
    return html, js

def scale(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-post" class="ln" pathLength="1" d="M540 1060 V560 M420 1060 H660"/>
      <g id="{p}-beam">
        <path id="{p}-bar" class="ln" pathLength="1" d="M200 560 H880"/>
        <path id="{p}-pl" class="ln" pathLength="1" d="M200 560 L140 800 M200 560 L260 800 M110 800 H290"/>
        <path id="{p}-pr" class="ln" pathLength="1" d="M880 560 L820 800 M880 560 L940 800 M790 800 H970"/>
      </g>
    </svg>
    <div id="{p}-a" class="mono" style="position:absolute;left:90px;width:220px;text-align:center;top:830px;font-size:34px;color:#fff">STREIT</div>
    <div id="{p}-b" class="mono" style="position:absolute;left:770px;width:220px;text-align:center;top:830px;font-size:34px;color:#fff">VERTRAUEN</div>
    <div id="{p}-n" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1100px;color:#bbb">* SPEKULATION, KEINE STUDIE</div>
    """
    js = (D(f"#{p}-post", lead, 0.5) + D(f"#{p}-bar", lead + 0.3, 0.4) + D(f"#{p}-pl", lead + 0.6, 0.5) + D(f"#{p}-pr", lead + 0.6, 0.5)
          + IN(f"#{p}-a", lead + 0.9) + IN(f"#{p}-b", lead + 1.9)
          + f'tl.fromTo("#{p}-beam", {{rotation: 0, svgOrigin: "540 560"}}, {{rotation: -7, duration: 0.8, ease: "power2.inOut"}}, {lead + 0.9});'
          + f'tl.to("#{p}-beam", {{rotation: 6, duration: 1.0, ease: "power2.inOut", svgOrigin: "540 560"}}, {lead + 1.9});'
          + f'tl.to("#{p}-beam", {{rotation: 0, duration: 1.0, ease: "power2.inOut", svgOrigin: "540 560"}}, {lead + 3.2});'
          + IN(f"#{p}-n", lead + max(1.0, dur * 0.6)))
    return html, js

def ask(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path id="{p}-qm" class="ln" pathLength="1" style="stroke-width:16" d="M440 600 Q440 470 545 470 Q650 470 650 570 Q650 640 580 670 Q545 690 545 760 V800"/>
      <circle id="{p}-dot" cx="545" cy="880" r="16" fill="#fff" opacity="0"/>
    </svg>
    <div id="{p}-l" class="big" style="top:950px;font-size:60px;font-weight:800">Würdest du dort leben?</div>
    <div id="{p}-c" class="mono" style="position:absolute;left:0;right:0;text-align:center;top:1050px;color:#fff;font-size:32px">↓ SCHREIB'S IN DIE KOMMENTARE</div>
    """
    js = (D(f"#{p}-qm", lead, 0.8, "power3.out") + f'tl.to("#{p}-dot", {{opacity: 1, duration: 0.1}}, {lead + 0.8});'
          + IN(f"#{p}-l", lead + 0.5) + IN(f"#{p}-c", lead + 1.4)
          + f'tl.fromTo("#{p}-c", {{y: 0}}, {{y: 14, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 5}}, {lead + 1.8});')
    return html, js

SCENES = {"hook": hook, "avg": avg, "skew": skew, "follow": follow, "white": white, "scale": scale, "ask": ask}

# (sfx name, segment index (-1 = absolute), offset s, volume)
SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 0, 1.5, 0.6), ("pop", 1, 3.3, 0.5), ("pop", 2, 1.6, 0.4),
       ("pop", 3, 0.9, 0.5), ("click-soft", 4, 1.6, 0.4), ("click-soft", 4, 2.6, 0.4), ("click-soft", 4, 3.6, 0.4),
       ("whoosh-short", 5, 0.0, 0.4), ("pop", 6, 0.8, 0.5)]
