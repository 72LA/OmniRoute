# malangenommen72 #12 – "Motivation ist überbewertet" (Milne, Orbell & Sheeran 2002; Wenn-dann-Plan) – Dark v2.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import S, IN, DRAW, ln, follow, SCENE_CSS

W = L.W
KEYS = {"motivation", "sport", "satz", "248", "38", "35", "91", "%", "@malangenommen72", "entscheidung", "94", "dienstag",
        "18", "park", "speicher", "montag", "chance", "nichts", "allein"}
TITLES = {"hook": "MAL ANGENOMMEN …", "loop": "1 SATZ", "groups": "DAS EXPERIMENT", "bars": "NACH 1 WOCHE",
          "autopilot": "WARUM ES KLAPPT", "tip": "DEIN SATZ"}

def tbox(x, y, w, lines, size=50, cls=""):
    """TikTok-native text box: white, black bold text (cover + OCR keyword)."""
    h = len(lines) * size * 1.25 + 34
    t = "".join(f'<text x="{x + w/2}" y="{y + 26 + size*0.95 + i*size*1.25}" text-anchor="middle" font-family="Montserrat" '
                f'font-weight="800" font-size="{size}" fill="#000">{s}</text>' for i, s in enumerate(lines))
    return f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff"/>{t}</g>'

def dumbbell(p, x, y, cls):
    d = (f"M{x} {y} H{x+160} M{x-18} {y-40} V{y+40} M{x-38} {y-28} V{y+28} M{x+178} {y-40} V{y+40} M{x+198} {y-28} V{y+28}")
    return f'<g filter="url(#{p}-glow)">' + ln(d, cls, 8) + '</g>'

def hook(p, dur, lead):
    inner = (L.spot(p, 440, 940, 380, 280) + tbox(140, 470, 800, ["MOTIVATION BRINGT", "FAST NICHTS."], 58)
             + f'<g filter="url(#{p}-glow)">{ln("M150 1110 V960 H470 V1110 M150 1030 H470", p+"-couch", 5)}</g>'
             + L.figure(p, 260, 1030, 1.0, "sit") + dumbbell(p, 680, 1080, p + "-db")
             + f'<g class="{p}-z" opacity="0">{L.big(400, 790, "Z z z", 54)}</g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>')
    js = DRAW(f".{p}-couch", 0.1, 0.4) + DRAW(f".{p}-db", 0.4, 0.5) + f'tl.to(".{p}-z", {{opacity: 1, duration: 0.3}}, {max(1.2, dur*0.55)});'
    return S(p, inner), js

def loop(p, dur, lead):
    inner = (L.spot(p, 540, 840, 380, 280)
             + f'<g filter="url(#{p}-glow)">{ln("M250 640 H760 L830 710 V1040 H250 Z M760 640 V710 H830", p+"-pap", 5)}'
             + ln("M310 760 H700 M310 840 H760 M310 920 H620", p+"-ln", 4) + '</g>'
             + L.big(540, 580, "× 2 CHANCE", 80, p+"-v") + L.label(540, 1100, "AM ENDE ZUM ABSCHREIBEN", 28, cls=p+"-t"))
    js = DRAW(f".{p}-pap", lead, 0.5) + DRAW(f".{p}-ln", lead + 0.4, 0.6) + IN(f".{p}-v", lead + 0.3) + IN(f".{p}-t", lead + (dur - lead) * 0.5)
    return S(p, inner), js

def groups(p, dur, lead):
    xs = (200, 540, 880); names = ("OHNE ALLES", "MOTIVATION", "+ 1 SATZ")
    inner = L.spot(p, 540, 860, 460, 280) + L.label(540, 520, "2002 · 248 STUDIERENDE", 28, op=.85, cls=p+"-src")
    for k, x in enumerate(xs):
        inner += f'<g class="{p}-g{k}">' + L.figure(p, x, 1000, 0.8, "stand") + L.label(x, 1060, names[k], 26) + '</g>'
    inner += (f'<g filter="url(#{p}-glow)">{ln("M430 600 H650 V740 H430 Z M455 640 H625 M455 680 H600", p+"-txt", 4)}'
              + ln("M770 590 H990 V770 H770 Z", p+"-note", 4) + '</g>'
              + f'<g class="{p}-nt" opacity="0">{L.label(880, 640, "TAG", 24)}{L.label(880, 690, "ZEIT", 24)}{L.label(880, 740, "ORT", 24)}</g>'
              + f'<path d="M60 1002 H1020" {W} stroke-width="3" stroke-opacity=".6"/>')
    f = [0.28, 0.45, 0.62]
    js = IN(f".{p}-src", lead)
    for k in range(3):
        js += f'tl.fromTo(".{p}-g{k}", {{opacity: 0, y: 40}}, {{opacity: 1, y: 0, duration: 0.4, ease: "power3.out"}}, {lead + (dur - lead) * f[k]});'
    js += DRAW(f".{p}-txt", lead + (dur - lead) * 0.47, 0.4) + DRAW(f".{p}-note", lead + (dur - lead) * 0.72, 0.4)
    js += f'tl.to(".{p}-nt", {{opacity: 1, duration: 0.3}}, {lead + (dur - lead) * 0.8});'
    return S(p, inner), js

def bars(p, dur, lead):
    base, top = 1000, 540
    vals = (38, 35, 91); xs = (230, 540, 850); names = ("OHNE", "MOTIVATION", "+ 1 SATZ"); f = (0.3, 0.55, 0.8)
    inner = (L.spot(p, 540, 840, 440, 300) + f'<path d="M100 {base} H980" {W} stroke-width="3" stroke-opacity=".8"/>'
             + "".join(f'<path d="M100 {base - (base-top)*k/4} H980" stroke="#fff" stroke-opacity=".16" stroke-width="2" stroke-dasharray="8 10"/>' for k in range(1, 5)))
    js = ""
    for k in range(3):
        h = (base - top) * vals[k] / 100
        fill = 'fill="#fff"' if k == 2 else W + ' stroke-width="5"'
        inner += (f'<g filter="url(#{p}-glow)"><rect id="{p}-b{k}" x="{xs[k]-80}" y="{base - h}" width="160" height="{h}" rx="12" {fill} style="transform-origin:{xs[k]}px {base}px"/></g>'
                  + L.big(xs[k], base - h - 24, f"{vals[k]} %", 62, p + f"-v{k}") + L.label(xs[k], base + 48, names[k], 26))
        t = lead + (dur - lead) * f[k] - 0.3
        js += f'tl.fromTo("#{p}-b{k}", {{scaleY: 0}}, {{scaleY: 1, duration: 0.6, ease: "power3.out"}}, {t});' + IN(f".{p}-v{k}", t + 0.45)
    inner += L.label(540, 1095, "TRAINIERT (SELBST BERICHTET)", 26, op=.75)
    return S(p, inner), js

def autopilot(p, dur, lead):
    inner = (L.spot(p, 540, 800, 440, 280)
             + f'<g filter="url(#{p}-glow)">{ln("M110 600 H480 V760 H110 Z", p+"-w", 5)}{ln("M600 600 H970 V760 H600 Z", p+"-d", 5)}'
             + ln("M495 680 H585 M555 650 L585 680 L555 710", p+"-ar", 5) + '</g>'
             + L.label(295, 655, "WENN", 26, op=.7) + L.big(295, 725, "DI 18:00", 50, p+"-wt")
             + L.label(785, 655, "DANN", 26, op=.7) + L.big(785, 725, "PARK", 50, p+"-dt")
             + f'<g class="{p}-guy">' + L.figure(p, 300, 1000, 0.7, "stand") + '</g>'
             + f'<path d="M100 1002 H980" {W} stroke-width="3" stroke-opacity=".6"/>'
             + L.label(540, 1070, "94 STUDIEN: BESTÄTIGT", 28, cls=p+"-s1") + L.label(540, 1115, "EFFEKT MEIST KLEINER", 26, op=.8, cls=p+"-s2"))
    t2 = lead + (dur - lead) * 0.32; t3 = lead + (dur - lead) * 0.62
    js = (DRAW(f".{p}-w", lead, 0.4) + IN(f".{p}-wt", lead + 0.3) + DRAW(f".{p}-ar", t2, 0.3) + DRAW(f".{p}-d", t2 + 0.2, 0.4) + IN(f".{p}-dt", t2 + 0.5)
          + f'tl.fromTo(".{p}-guy", {{x: 0}}, {{x: 480, duration: 2.0, ease: "power1.inOut"}}, {t2 + 0.4});'
          + IN(f".{p}-s1", t3) + IN(f".{p}-s2", t3 + 0.5))
    return S(p, inner), js

def tip(p, dur, lead):
    rows = ["ICH MACHE SPORT", "AM DIENSTAG", "UM 18 UHR", "IM PARK"]; f = (0.04, 0.16, 0.3, 0.42)
    inner = L.spot(p, 540, 800, 420, 300) + f'<g filter="url(#{p}-glow)">{ln("M130 520 H950 V990 H130 Z", p+"-card", 5)}</g>'
    js = DRAW(f".{p}-card", lead, 0.4)
    for k, r in enumerate(rows):
        y = 610 + k * 100
        inner += L.big(540, y, r, 52, p + f"-r{k}") + f'<path d="M260 {y+18} H820" stroke="#fff" stroke-opacity=".25" stroke-width="2"/>'
        js += IN(f".{p}-r{k}", lead + (dur - lead) * f[k])
    inner += L.label(540, 1050, "↓ SPEICHER DIR DAS", 30, cls=p+"-sv") + L.label(540, 1105, "SCHICK'S DEM „AB MONTAG“-TYP", 26, cls=p+"-sh")
    js += IN(f".{p}-sv", lead + (dur - lead) * 0.58) + IN(f".{p}-sh", lead + (dur - lead) * 0.74)
    return S(p, inner), js

SCENES = {"hook": hook, "loop": loop, "groups": groups, "bars": bars, "follow": follow, "autopilot": autopilot, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 0, 0.4, 0.35), ("pop", 1, 0.4, 0.45), ("click-soft", 2, 2.4, 0.35),
       ("click-soft", 2, 3.8, 0.35), ("click-soft", 2, 5.3, 0.35), ("pop", 3, 2.1, 0.4), ("pop", 3, 3.9, 0.4), ("sparkle", 3, 5.7, 0.45),
       ("pop", 4, 1.1, 0.5), ("whoosh-short", 5, 3.0, 0.35), ("pop", 5, 5.3, 0.4), ("pop", 6, 0.3, 0.35), ("pop", 6, 2.9, 0.35),
       ("sparkle", 6, 4.0, 0.4)]
