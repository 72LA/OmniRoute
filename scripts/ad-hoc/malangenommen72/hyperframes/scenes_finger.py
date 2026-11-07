# AI72 #06 – "Warum werden deine Finger im Wasser schrumpelig?" – flat infographic style.
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes_kitzeln import POP, face, follow, SCENE_CSS, O, Y, P, C, CR, N2

KEYS = {"schrumpelig?", "schrumpelig", "wasser", "stimmt", "nicht", "nerven", "glatt", "1930er-jahren", "aktive", "blutgefäße",
        "falten", "@ai72", "körper", "murmeln", "schneller", "reifen", "geklärt", "badewanne"}

TITLES = {"hook": "SCHRUMPELFINGER?", "myth": "DER MYTHOS", "nerve": "DIE NERVEN-SPUR", "vessels": "SO FUNKTIONIERT'S",
          "marbles": "DER MURMEL-TEST", "tire": "WIE EIN REIFENPROFIL", "share": "SCHICK'S WEITER"}

def big_hand(id_, cx, cy, s=1.0, wrinkles=True, nerve=None):
    fx = [-0.9, -0.3, 0.3, 0.9]; lens = [1.6, 2.0, 1.9, 1.5]
    out = [f'<g id="{id_}">']
    for x, l in zip(fx, lens):
        out.append(f'<rect x="{cx + (x*95 - 40)*s}" y="{cy - (l*170)*s}" width="{80*s}" height="{l*190*s}" rx="{40*s}" fill="{CR}" stroke="{O}" stroke-width="8"/>')
        if wrinkles:
            for k in range(3):
                yy = cy - (l*170 - 30 - k*24)*s
                out.append(f'<path class="{id_}-wr" d="M{cx + (x*95 - 26)*s} {yy} q{13*s} -10 {26*s} 0 t{26*s} 0" fill="none" stroke="#c98f7a" stroke-width="5" stroke-linecap="round"/>')
    out.append(f'<rect x="{cx - 160*s}" y="{cy - 40*s}" width="{320*s}" height="{300*s}" rx="{90*s}" fill="{CR}" stroke="{O}" stroke-width="8"/>')
    out.append(f'<rect x="{cx - 150*s}" y="{cy}" width="{300*s}" height="{40*s}" fill="{CR}"/>')
    out.append(f'<rect x="{cx + 120*s}" y="{cy + 10*s}" width="{80*s}" height="{170*s}" rx="{40*s}" fill="{CR}" stroke="{O}" stroke-width="8" transform="rotate(-25 {cx + 160*s} {cy + 95*s})"/>')
    if nerve:
        out.append(f'<path d="M{cx} {cy + 250*s} V{cy - 10*s} M{cx} {cy + 40*s} L{cx - 95*s} {cy - 250*s} M{cx} {cy + 40*s} L{cx + 85*s} {cy - 300*s}" fill="none" stroke="{nerve}" stroke-width="12" stroke-linecap="round" stroke-dasharray="{"0" if nerve == Y else "26 22"}"/>')
    out.append("</g>")
    return "".join(out)

def drops(p, n=5):
    return "".join(f'<path class="{p}-drop" d="M{180 + k*170} {560 + (k%2)*60} q-26 40 0 56 q26 -16 0 -56 z" fill="{C}" stroke="{O}" stroke-width="5"/>' for k in range(n))

def hook(p, dur, lead):
    html = f"""<svg style="left:0;top:0" width="1080" height="1920">{drops(p)}{big_hand(p+"-h", 540, 870, 1.05)}</svg>"""
    js = (f'tl.fromTo(".{p}-drop", {{y: -40, opacity: 0}}, {{y: 30, opacity: 1, duration: 0.6, stagger: 0.12, ease: "power2.in"}}, 0.1);'
          + f'tl.fromTo(".{p}-h-wr", {{opacity: 0}}, {{opacity: 1, duration: 0.4, stagger: 0.03}}, 0.6);')
    return html, js

def myth(p, dur, lead):
    holes = "".join(f'<circle cx="{390 + (k%4)*95}" cy="{720 + (k//4)*80}" r="18" fill="#d8a400"/>' for k in range(12))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-sp"><rect x="342" y="642" width="420" height="300" rx="40" fill="{O}"/><rect x="330" y="630" width="420" height="300" rx="40" fill="{Y}" stroke="{O}" stroke-width="8"/>{holes}</g>
      {drops(p, 4)}
      <g id="{p}-x"><path d="M330 600 L760 960 M760 600 L330 960" stroke="{O}" stroke-width="58" stroke-linecap="round"/>
        <path d="M330 600 L760 960 M760 600 L330 960" stroke="{P}" stroke-width="34" stroke-linecap="round"/></g>
    </svg>
    <div class="lbl" style="left:0;right:0;top:1010px;font-size:46px">„HAUT SAUGT SICH VOLL“</div>
    """
    js = (POP(f"#{p}-sp", lead) + f'tl.fromTo(".{p}-drop", {{y: -60, opacity: 0}}, {{y: 40, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.in"}}, {lead + 0.2});'
          + POP(f"#{p}-x", lead + (dur - lead) * 0.6))
    return html, js

def nerve(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-l">{big_hand(p+"-a", 290, 820, 0.62, True, Y)}</g>
      <g id="{p}-r">{big_hand(p+"-b", 790, 820, 0.62, False, "#8d9bc4")}</g>
    </svg>
    <div id="{p}-la" class="pill" style="left:120px;top:1010px;width:340px;height:84px;line-height:72px;background:{Y};color:{O};font-size:36px">NERV OK</div>
    <div id="{p}-lb" class="pill" style="left:620px;top:1010px;width:340px;height:84px;line-height:72px;background:#fff;color:{O};font-size:36px">NERV KAPUTT</div>
    <div id="{p}-yr" class="lbl" style="left:0;right:0;top:470px;font-size:44px;color:{C}">1930er</div>
    """
    q = lead + (dur - lead) * 0.45
    js = (POP(f"#{p}-yr", lead) + POP(f"#{p}-l", lead + 0.3) + POP(f"#{p}-la", lead + 0.6) + POP(f"#{p}-r", q) + POP(f"#{p}-lb", q + 0.3))
    return html, js

def vessels(p, dur, lead):
    flat = "M140 640 " + " ".join(f"L{140 + k*10} 640" for k in range(81))
    wavy = "M140 640 " + " ".join(f"L{140 + k*10} {640 + 26*math.sin(k/2.2):.1f}" for k in range(81))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <rect x="152" y="652" width="800" height="360" rx="30" fill="{O}"/>
      <rect x="140" y="640" width="800" height="360" rx="30" fill="#f7c9b0" stroke="{O}" stroke-width="8"/>
      <path id="{p}-flat" d="{flat}" fill="none" stroke="{O}" stroke-width="14" stroke-linecap="round"/>
      <path id="{p}-wavy" d="{wavy}" fill="none" stroke="{O}" stroke-width="14" stroke-linecap="round" opacity="0"/>
      <g id="{p}-vessel"><rect x="180" y="820" width="720" height="90" rx="45" fill="{P}" stroke="{O}" stroke-width="8"/></g>
      <path id="{p}-bolt" d="M560 470 l-40 90 h40 l-30 80 l80 -110 h-40 l30 -60 z" fill="{Y}" stroke="{O}" stroke-width="6"/>
    </svg>
    <div class="lbl" style="left:190px;top:930px;font-size:34px">BLUTGEFÄSS</div>
    <div class="lbl" style="left:700px;top:580px;font-size:34px">HAUT</div>
    """
    u0 = lead + (dur - lead) * 0.35; u1 = lead + (dur - lead) * 0.7
    js = (POP(f"#{p}-bolt", lead + 0.4) + f'tl.fromTo("#{p}-vessel", {{scaleY: 1, svgOrigin: "540 865"}}, {{scaleY: 0.4, duration: 0.8, ease: "power2.inOut"}}, {u0});'
          + f'tl.to("#{p}-flat", {{opacity: 0, duration: 0.4}}, {u1});' + f'tl.to("#{p}-wavy", {{opacity: 1, duration: 0.4}}, {u1});')
    return html, js

def marbles(p, dur, lead):
    cols = [Y, P, C, Y, P, C]
    m = "".join(f'<g class="{p}-m" id="{p}-m{k}"><circle cx="{250 + (k%3)*55}" cy="{930 - (k//3)*50}" r="26" fill="{cols[k]}" stroke="{O}" stroke-width="6"/></g>' for k in range(6))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <path d="M150 900 q155 160 310 0 z" fill="{O}" transform="translate(10 12)"/><path d="M150 900 q155 160 310 0 z" fill="{N2}" stroke="{O}" stroke-width="8"/>
      <path d="M620 900 q155 160 310 0 z" fill="{O}" transform="translate(10 12)"/><path d="M620 900 q155 160 310 0 z" fill="{N2}" stroke="{O}" stroke-width="8"/>
      {m}
      <g id="{p}-clk"><circle cx="540" cy="600" r="80" fill="#fff" stroke="{O}" stroke-width="8"/><path id="{p}-hd" d="M540 600 V540" stroke="{O}" stroke-width="10" stroke-linecap="round"/></g>
    </svg>
    <div id="{p}-fast" class="pill" style="left:620px;top:520px;width:330px;height:84px;line-height:72px;background:{Y};color:{O};font-size:40px">SCHNELLER</div>
    """
    js = POP(f"#{p}-clk", lead) + f'tl.fromTo("#{p}-hd", {{rotation: 0, svgOrigin: "540 600"}}, {{rotation: 360, duration: {max(1.5, dur - lead - 0.5)}, ease: "none"}}, {lead + 0.2});'
    for k in range(6):
        js += f'tl.fromTo("#{p}-m{k}", {{x: 0, y: 0}}, {{keyframes: [{{x: 235, y: -160, duration: 0.25, ease: "power2.out"}}, {{x: 470, y: 0, duration: 0.25, ease: "power2.in"}}]}}, {lead + 1.0 + k*0.42});'
    js += POP(f"#{p}-fast", lead + 3.4)
    return html, js

def tire(p, dur, lead):
    tread = "".join(f'<rect x="{470 + k*72}" y="610" width="40" height="300" rx="10" fill="{O}" transform="skewX(-14)"/>' for k in range(7))
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-t"><rect x="232" y="592" width="640" height="340" rx="60" fill="{O}"/><rect x="220" y="580" width="640" height="340" rx="60" fill="#3a4a7e" stroke="{O}" stroke-width="8"/>{tread}</g>
    </svg>
    <div id="{p}-q" class="pill" style="left:150px;top:1000px;width:780px;height:96px;line-height:84px;background:#fff;color:{O};font-size:40px">? NOCH NICHT GANZ GEKLÄRT</div>
    """
    js = POP(f"#{p}-t", lead) + POP(f"#{p}-q", lead + (dur - lead) * 0.55)
    return html, js

def share(p, dur, lead):
    html = f"""
    <svg style="left:0;top:0" width="1080" height="1920">
      <g id="{p}-tub"><rect x="212" y="842" width="660" height="200" rx="80" fill="{O}"/><rect x="200" y="830" width="660" height="200" rx="80" fill="#fff" stroke="{O}" stroke-width="8"/>
        <rect x="230" y="830" width="600" height="40" fill="{C}"/>
        <circle cx="330" cy="810" r="36" fill="#fff" stroke="{O}" stroke-width="5"/><circle cx="740" cy="800" r="30" fill="#fff" stroke="{O}" stroke-width="5"/><circle cx="690" cy="760" r="20" fill="#fff" stroke="{O}" stroke-width="5"/></g>
      {face(p+"-f", 520, 760, 110, "laugh")}
    </svg>
    <div id="{p}-b" class="pill" style="left:120px;top:470px;width:840px;height:150px;background:#fff;color:{O};font-size:48px;line-height:1.15;padding-top:18px">SCHICK'S DEM<br/><span style="color:{P}">BADEWANNEN-PROFI</span></div>
    """
    js = POP(f"#{p}-b", lead) + POP(f"#{p}-tub", lead + 0.3) + POP(f"#{p}-f", lead + 0.5)
    return html, js

SCENES = {"hook": hook, "myth": myth, "nerve": nerve, "vessels": vessels, "follow": follow, "marbles": marbles, "tire": tire, "share": share}

SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 1, 0.0, 0.45), ("pop", 1, 2.7, 0.5), ("pop", 2, 0.3, 0.45), ("pop", 2, 3.0, 0.45),
       ("click-soft", 3, 0.4, 0.4), ("pop", 4, 0.7, 0.5), ("click-soft", 5, 1.0, 0.35), ("click-soft", 5, 1.84, 0.35),
       ("click-soft", 5, 2.68, 0.35), ("pop", 5, 3.4, 0.45), ("pop", 6, 3.9, 0.45), ("pop", 7, 0.0, 0.5)]
