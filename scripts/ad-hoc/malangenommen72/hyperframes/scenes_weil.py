# malangenommen72 #08 – "Ein Wort, das Ja macht" (Langer 1978) – Dark v2 style, useful/actionable format.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L

W = L.W
KEYS = {"wort", "ja", "1978", "kopierer", "60", "%", "„weil“", "93", "sinnlosen", "@malangenommen72", "sofort",
        "automatisch", "achtung:", "echter", "grund", "ehrlichen", "heute"}
TITLES = {"hook": "MAL ANGENOMMEN", "copier": "DER KOPIERER-TEST", "bars": "EIN WORT", "brain": "AUTOPILOT",
          "caution": "ABER ACHTUNG", "tip": "SO NUTZT DU ES"}
SCENE_CSS = """
.title { top: 262px; font-weight: 800; font-size: 64px; letter-spacing: .06em; text-shadow: 0 0 18px rgba(255,255,255,.55); }
svg { position: absolute; overflow: visible; }
"""

def S(p, inner):
    return f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{L.defs(p)}{inner}</svg>'

def IN(sel, at, d=0.25):
    return f'tl.fromTo("{sel}", {{opacity: 0, filter: "blur(8px)"}}, {{opacity: 1, filter: "blur(0px)", duration: {d}, ease: "power4.out"}}, {at});'

def DRAW(sel, at, d=0.6):
    return f'tl.fromTo("{sel}", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {d}, ease: "power2.inOut"}}, {at});'

def ln(d, cls, w=5, extra=""):
    return f'<path class="{cls}" pathLength="1" d="{d}" stroke="#fff" fill="none" stroke-linecap="butt" stroke-linejoin="round" stroke-width="{w}" style="stroke-dasharray:1;stroke-dashoffset:1" {extra}/>'

def hook(p, dur, lead):
    inner = (L.spot(p, 420, 900, 300, 300)
             + L.big(540, 520, "EIN WORT.", 96) + L.big(540, 625, "MEHR JA.", 96)
             + f'<g filter="url(#{p}-glow)">{ln("M560 760 H900 Q930 760 930 790 V880 Q930 910 900 910 H640 L590 960 L600 910 H560 Q530 910 530 880 V790 Q530 760 560 760 Z", p+"-bub")}</g>'
             + f'<g class="{p}-w" opacity="0">{L.big(730, 858, "„WEIL …“", 58)}</g>'
             + L.figure(p, 400, 1120, 1.2, "stand") + f'<path d="M80 1122 H1000" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = DRAW(f".{p}-bub", 0.3, 0.6) + f'tl.to(".{p}-w", {{opacity: 1, duration: 0.25}}, 0.8);'
    return S(p, inner), js

def copier(p, dur, lead):
    inner = (L.spot(p, 640, 900, 320, 260)
             + f'<g filter="url(#{p}-glow)">'
             + ln("M640 760 H960 V1110 H640 Z M640 830 H960 M660 760 L700 700 H900 L940 760 M690 960 H910 M690 1010 H910", p+"-cp")
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/></g>'
             + L.figure(p, 560, 1110, 1.0, "point", p+"-f1") + L.figure(p, 330, 1110, 0.95, "stand", p+"-f2") + f'<g class="{p}-f3">' + L.figure(p, 160, 1110, 0.9, "stand") + "</g>"
             + L.label(540, 640, "1978 · ELLEN LANGER", 30, cls=p+"-src"))
    js = (DRAW(f".{p}-cp", lead, 0.8) + IN(f".{p}-src", lead + 0.4)
          + f'tl.fromTo(".{p}-f3", {{x: -120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.6, ease: "expo.out"}}, {lead + 1.6});'
          + f'tl.fromTo(".{p}-f2, .{p}-f1", {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {lead + 0.2});')
    return S(p, inner), js

def bars(p, dur, lead):
    base, top = 1050, 520
    h1, h2 = (base - top) * 0.60, (base - top) * 0.93
    inner = (L.spot(p, 540, 860, 380, 320)
             + f'<path d="M120 {base} H960" {W} stroke-width="3" stroke-opacity=".8"/>'
             + "".join(f'<path d="M120 {base - (base-top)*k/4} H960" stroke="#fff" stroke-opacity=".18" stroke-width="2" stroke-dasharray="8 10"/>' for k in range(1, 5))
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-b1" x="250" y="{base - h1}" width="200" height="{h1}" rx="14" {W} stroke-width="5" style="transform-origin:350px {base}px"/>'
             + f'<rect id="{p}-b2" x="630" y="{base - h2}" width="200" height="{h2}" rx="14" fill="#fff" style="transform-origin:730px {base}px"/></g>'
             + L.big(350, base - h1 - 30, "60 %", 70, p+"-v1") + L.big(730, base - h2 - 30, "93 %", 70, p+"-v2")
             + L.label(350, base + 50, "OHNE GRUND", 28) + L.label(730, base + 50, "MIT „WEIL“", 28)
             + L.label(540, base + 100, "AUCH BEI SINNLOSEM GRUND", 28, op=.8, cls=p+"-note"))
    t2 = lead + (dur - lead) * 0.38
    js = (f'tl.fromTo("#{p}-b1", {{scaleY: 0}}, {{scaleY: 1, duration: 0.7, ease: "power3.out"}}, {lead + 0.6});' + IN(f".{p}-v1", lead + 1.2)
          + f'tl.fromTo("#{p}-b2", {{scaleY: 0}}, {{scaleY: 1, duration: 0.8, ease: "power3.out"}}, {t2});' + IN(f".{p}-v2", t2 + 0.6)
          + IN(f".{p}-note", lead + (dur - lead) * 0.7))
    return S(p, inner), js

def follow(p, dur, lead):
    inner = (L.spot(p, 540, 700, 260, 260)
             + f'<g filter="url(#{p}-glow)">{ln("M350 700 a190 190 0 1 0 380 0 a190 190 0 1 0 -380 0", p+"-ring", 6)}'
             + ln("M520 565 A145 145 0 1 0 650 795 A116 116 0 1 1 520 565 Z", p+"-moon", 8) + '</g>'
             + f'<g class="{p}-q" opacity="0">{L.big(650, 660, "?", 130)}</g>'
             + f'<g class="{p}-h" opacity="0">{L.big(540, 980, "@malangenommen72", 60)}</g>'
             + f'<g filter="url(#{p}-glow)">{ln("M380 1030 H700 Q745 1030 745 1075 Q745 1120 700 1120 H380 Q335 1120 335 1075 Q335 1030 380 1030 Z", p+"-btn", 5)}</g>'
             + f'<g class="{p}-bt" opacity="0">{L.label(540, 1088, "+ FOLGEN", 34)}</g>')
    js = (DRAW(f".{p}-ring", lead, 0.6) + DRAW(f".{p}-moon", lead + 0.2, 0.7) + f'tl.to(".{p}-q", {{opacity: 1, duration: 0.2}}, {lead + 0.7});'
          + f'tl.to(".{p}-h", {{opacity: 1, duration: 0.2}}, {lead + 0.5});' + DRAW(f".{p}-btn", lead + 0.8, 0.4) + f'tl.to(".{p}-bt", {{opacity: 1, duration: 0.2}}, {lead + 1.1});')
    return S(p, inner), js

def brain(p, dur, lead):
    inner = (L.spot(p, 420, 860, 300, 300) + L.figure(p, 360, 1110, 1.25, "think")
             + f'<g filter="url(#{p}-glow)">{ln("M700 600 H960 V700 H700 Z", p+"-in")}{ln("M700 860 H960 V960 H700 Z", p+"-out")}'
             + ln("M560 650 H690 M830 710 V850", p+"-ar", 4) + '</g>'
             + L.label(830, 660, "„WEIL …“", 30) + L.label(830, 922, "→ JA", 34)
             + L.label(810, 790, "GUTER GRUND?", 22, "end", op=.8, cls=p+"-mid"))
    js = (DRAW(f".{p}-in", lead + 0.3, 0.4) + DRAW(f".{p}-ar", lead + 0.8, 0.5) + IN(f".{p}-mid", lead + 1.2)
          + DRAW(f".{p}-out", lead + (dur - lead) * 0.55, 0.4))
    return S(p, inner), js

def caution(p, dur, lead):
    inner = (L.spot(p, 540, 840, 380, 280)
             + f'<g filter="url(#{p}-glow)">{ln("M120 560 H500 V1020 H120 Z", p+"-c1")}{ln("M580 560 H960 V1020 H580 Z", p+"-c2")}</g>'
             + L.label(310, 620, "KLEINE BITTE", 28) + L.label(770, 620, "GROSSE BITTE", 28)
             + L.big(310, 790, "5", 120) + L.label(310, 840, "SEITEN", 28) + L.big(770, 790, "20", 120) + L.label(770, 840, "SEITEN", 28)
             + L.label(310, 950, "„WEIL“ REICHT", 28, cls=p+"-r1") + L.label(770, 935, "NUR ECHTER", 28, cls=p+"-r2") + L.label(770, 968, "GRUND HILFT", 28, cls=p+"-r2"))
    js = (DRAW(f".{p}-c1", lead, 0.5) + DRAW(f".{p}-c2", lead + 0.3, 0.5) + IN(f".{p}-r1", lead + 1.0) + IN(f".{p}-r2", lead + (dur - lead) * 0.5))
    return S(p, inner), js

def tip(p, dur, lead):
    steps = ["1 · BITTE", "2 · „WEIL“", "3 · ECHTER GRUND"]
    inner = L.spot(p, 540, 820, 380, 300) + f'<g filter="url(#{p}-glow)">{ln("M180 540 H900 V1040 H180 Z", p+"-card")}</g>'
    for k, st in enumerate(steps):
        y = 660 + k * 120
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M240 {y-28} H296 V{y+28} H240 Z", p+f"-box{k}", 4)}{ln(f"M250 {y} L265 {y+16} L290 {y-18}", p+f"-tick{k}", 6)}</g>'
        inner += L.label(330, y + 10, st, 30, "start", cls=p + f"-t{k}")
    inner += L.label(540, 1110, "↓ KOMMENTIER DEIN ERGEBNIS", 28, op=.8, cls=p+"-c")
    per = max(0.8, (dur - lead) / 4.5)
    js = DRAW(f".{p}-card", lead, 0.5)
    for k in range(3):
        t = lead + 0.8 + k * per
        js += DRAW(f".{p}-box{k}", t, 0.25) + IN(f".{p}-t{k}", t + 0.1) + DRAW(f".{p}-tick{k}", t + 0.35, 0.25)
    js += IN(f".{p}-c", lead + (dur - lead) * 0.75)
    return S(p, inner), js

SCENES = {"hook": hook, "copier": copier, "bars": bars, "follow": follow, "brain": brain, "caution": caution, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 1, 1.6, 0.4), ("pop", 2, 1.2, 0.45), ("pop", 2, 4.6, 0.5),
       ("pop", 3, 1.1, 0.5), ("click-soft", 4, 2.6, 0.4), ("click-soft", 5, 0.3, 0.35), ("pop", 6, 1.2, 0.4), ("pop", 6, 2.5, 0.4), ("pop", 6, 3.8, 0.4)]
