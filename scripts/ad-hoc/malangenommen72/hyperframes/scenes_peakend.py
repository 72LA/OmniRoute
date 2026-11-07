# malangenommen72 #13 – "60 oder 90 Sekunden Schmerz?" Peak-End-Regel (Kahneman et al. 1993; Redelmeier et al. 2003) – Dark v2.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import IN, DRAW, ln, follow, SCENE_CSS
from scenes_motivation import tbox

W = L.W
KEYS = {"60", "90", "schmerz", "70", "%", "verrückt", "14", "grad", "30", "wärmer", "peak-end-regel", "schlimmsten", "ende",
        "dauer", "@malangenommen72", "682", "darmspiegelungen", "sanfterem", "schlimm", "schönsten", "leichtesten", "streit",
        "speicher", "date"}
TITLES = {"hook": "MAL ANGENOMMEN …", "loop": "KLINGT VERRÜCKT", "exp": "DAS EXPERIMENT", "rule": "PEAK-END-REGEL",
          "colon": "SOGAR BEIM ARZT", "tip": "SO NUTZT DU ES"}

def S(p, inner, dur):
    """svg scene with a slow camera push-in (keeps motion on screen between beats)."""
    svg = f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{L.defs(p)}<g id="{p}-cam">{inner}</g></svg>'
    js = f'tl.fromTo("#{p}-cam", {{scale: 1}}, {{scale: 1.035, svgOrigin: "540 820", duration: {dur}, ease: "none"}}, 0);'
    return svg, js

def clock(p, cx, cy, r, frac, cls):
    """time ring: dim full circle + bright arc for the share of 90 s."""
    import math
    a = 2 * math.pi * frac - 1e-3
    x = cx + r * math.sin(a); y = cy - r * math.cos(a)
    big = 1 if frac > 0.5 else 0
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="10"/>'
            f'<g filter="url(#{p}-glow)">' + ln(f"M{cx} {cy - r} A{r} {r} 0 {big} 1 {x:.1f} {y:.1f}", cls, 14) + '</g>')

def bucket(p, x, y, cls):
    d = f"M{x} {y} L{x+30} {y+190} H{x+230} L{x+260} {y} M{x+12} {y+60} Q{x+70} {y+40} {x+130} {y+60} T{x+248} {y+60}"
    return f'<g filter="url(#{p}-glow)">' + ln(d, cls, 5) + '</g>'

def hook(p, dur, lead):
    inner = (L.spot(p, 540, 900, 420, 300) + tbox(150, 455, 780, ["60 ODER 90 SEKUNDEN", "SCHMERZ?"], 54)
             + clock(p, 330, 820, 120, 60/90, p + "-c1") + clock(p, 750, 820, 120, 1.0, p + "-c2")
             + L.big(330, 1010, "60 s", 64) + L.big(750, 1010, "90 s", 64)
             + f'<g class="{p}-pick" opacity="0">' + L.label(540, 1105, "FAST 70 % NEHMEN DIE 90", 28) + '</g>'
             + f'<g filter="url(#{p}-glow)">{ln("M610 660 H890 V1045 H610 Z", p+"-sel", 4)}</g>')
    sv, cam = S(p, inner, dur)
    t = lead + (dur - lead) * 0.68
    js = (cam + ""
          + f'tl.fromTo(".{p}-c1", {{strokeDashoffset: 0.6}}, {{strokeDashoffset: 0, duration: 1.0, ease: "power2.out"}}, 0.2);'
          + f'tl.fromTo(".{p}-c2", {{strokeDashoffset: 0.6}}, {{strokeDashoffset: 0, duration: 1.4, ease: "power2.out"}}, 0.2);'
          + DRAW(f".{p}-sel", t, 0.5) + f'tl.to(".{p}-pick", {{opacity: 1, duration: 0.25}}, {t + 0.3});')
    return sv, js

def loop(p, dur, lead):
    inner = (L.spot(p, 420, 900, 320, 300) + L.figure(p, 380, 1110, 1.15, "think")
             + f'<g filter="url(#{p}-glow)">{ln("M600 640 H960 V1100 H600 Z", p+"-box")}</g>'
             + L.big(780, 900, "?", 200, p+"-q") + L.label(780, 1160, "AM ENDE: DER TRICK", 28, cls=p+"-end")
             + f'<path d="M80 1112 H560" {W} stroke-width="3" stroke-opacity=".7"/>')
    sv, cam = S(p, inner, dur)
    return sv, cam + DRAW(f".{p}-box", lead, 0.5) + IN(f".{p}-q", lead + 0.3) + IN(f".{p}-end", lead + 0.7)

def exp(p, dur, lead):
    span = dur - lead
    y1, y2 = 900, 1020; x0 = 140; unit = 800 / 90
    inner = (L.spot(p, 540, 800, 440, 300) + bucket(p, 410, 470, p + "-bk")
             + f'<g class="{p}-hand">' + f'<g filter="url(#{p}-glow)">' + ln("M540 380 V560 M515 560 Q540 600 565 560", p + "-arm", 8) + '</g></g>'
             + L.big(540, 760, "14 °C", 64, p + "-t")
             + f'<g filter="url(#{p}-glow)">{ln(f"M{x0} {y1} H{x0 + 60*unit:.0f}", p+"-a", 26)}{ln(f"M{x0} {y2} H{x0 + 60*unit:.0f}", p+"-b", 26)}'
             + ln(f"M{x0 + 60*unit:.0f} {y2} H{x0 + 90*unit:.0f}", p+"-b2", 26, 'stroke-opacity=".45"') + '</g>'
             + L.label(x0, y1 - 32, "VERSION A · 60 s", 24, "start") + L.label(x0, y2 - 32, "VERSION B · 90 s", 24, "start")
             + f'<g class="{p}-w" opacity="0">' + L.label(x0 + 75*unit, y2 + 62, "+1 °C", 30) + '</g>')
    sv, cam = S(p, inner, dur)
    js = (cam + DRAW(f".{p}-bk", lead, 0.6) + DRAW(f".{p}-arm", lead + 0.3, 0.5) + IN(f".{p}-t", lead + 0.6)
          + DRAW(f".{p}-a", lead + span * 0.38, 0.8) + DRAW(f".{p}-b", lead + span * 0.6, 0.8)
          + DRAW(f".{p}-b2", lead + span * 0.78, 0.6) + f'tl.to(".{p}-w", {{opacity: 1, duration: 0.25}}, {lead + span * 0.82});')
    return sv, js

def rule(p, dur, lead):
    span = dur - lead
    curve = "M130 960 C 220 940, 260 800, 330 760 C 380 730, 400 580, 450 560 C 500 545, 520 700, 600 760 C 680 820, 760 860, 950 900"
    inner = (L.spot(p, 540, 780, 440, 300)
             + f'<path d="M130 980 H960 M130 980 V520" {W} stroke-width="3" stroke-opacity=".8"/>'
             + f'<g filter="url(#{p}-glow)">{ln(curve, p+"-c", 7)}</g>'
             + f'<g class="{p}-pk" opacity="0"><circle cx="450" cy="560" r="18" fill="#fff"/></g>'
             + f'<g class="{p}-en" opacity="0"><circle cx="950" cy="900" r="18" fill="#fff"/></g>'
             + L.label(450, 520, "PEAK", 30, cls=p + "-pl") + L.label(880, 860, "ENDE", 30, cls=p + "-el")
             + L.label(560, 1030, "ZEIT →", 24, op=.7)
             + f'<g filter="url(#{p}-glow)">{ln("M180 1080 H900 M180 1080 l24 -16 M180 1080 l24 16 M900 1080 l-24 -16 M900 1080 l-24 16", p+"-d", 4)}</g>'
             + f'<g class="{p}-x" opacity="0">' + L.label(540, 1125, "DAUER: FAST EGAL", 28) + '</g>')
    sv, cam = S(p, inner, dur)
    js = (cam + DRAW(f".{p}-c", lead, 1.6) + f'tl.to(".{p}-pk", {{opacity: 1, duration: 0.2}}, {lead + span * 0.45});' + IN(f".{p}-pl", lead + span * 0.45)
          + f'tl.to(".{p}-en", {{opacity: 1, duration: 0.2}}, {lead + span * 0.62});' + IN(f".{p}-el", lead + span * 0.62)
          + DRAW(f".{p}-d", lead + span * 0.8, 0.4) + f'tl.to(".{p}-x", {{opacity: 1, duration: 0.25}}, {lead + span * 0.84});')
    return sv, js

def colon(p, dur, lead):
    span = dur - lead
    a = "M140 900 C 200 860, 260 640, 330 620 C 380 610, 410 640, 430 680 L 440 900"
    b = "M600 900 C 660 860, 720 640, 790 620 C 840 610, 860 700, 900 800 C 920 850, 950 880, 980 890"
    inner = (L.spot(p, 540, 780, 460, 300) + L.label(540, 520, "2003 · 682 PATIENTEN", 28, op=.85, cls=p + "-src")
             + f'<path d="M120 900 H460 M580 900 H990" {W} stroke-width="3" stroke-opacity=".7"/>'
             + f'<g filter="url(#{p}-glow)">{ln(a, p+"-a", 6)}{ln(b, p+"-b", 6)}</g>'
             + L.label(290, 960, "KURZ · HARTES ENDE", 22) + L.label(785, 960, "LÄNGER · SANFT", 22)
             + f'<g class="{p}-ra" opacity="0">' + L.big(290, 1060, "SCHLIMMER", 44) + '</g>'
             + f'<g class="{p}-rb" opacity="0">' + L.big(785, 1060, "MILDER", 44) + '</g>'
             + L.label(540, 1120, "SO ERINNERT", 24, op=.75, cls=p + "-m"))
    sv, cam = S(p, inner, dur)
    js = (cam + IN(f".{p}-src", lead + 0.2) + DRAW(f".{p}-a", lead + span * 0.2, 0.8) + DRAW(f".{p}-b", lead + span * 0.38, 1.0)
          + f'tl.to(".{p}-ra", {{opacity: 1, duration: 0.25}}, {lead + span * 0.62});'
          + f'tl.to(".{p}-rb", {{opacity: 1, duration: 0.25}}, {lead + span * 0.72});' + IN(f".{p}-m", lead + span * 0.62))
    return sv, js

def tip(p, dur, lead):
    steps = ["TREFFEN: BESTES ZULETZT", "SPORT: LEICHT ENDEN", "STREIT: VERSÖHNT ENDEN"]; f = (0.08, 0.26, 0.42)
    inner = L.spot(p, 540, 800, 420, 300) + f'<g filter="url(#{p}-glow)">{ln("M100 540 H980 V1000 H100 Z", p+"-card", 5)}</g>'
    js = DRAW(f".{p}-card", lead, 0.4)
    for k, s_ in enumerate(steps):
        y = 650 + k * 120
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M150 {y-28} H206 V{y+28} H150 Z", p+f"-box{k}", 4)}{ln(f"M160 {y} L175 {y+16} L200 {y-18}", p+f"-tick{k}", 6)}</g>'
        inner += L.label(232, y + 10, s_, 27, "start", cls=p + f"-t{k}")
        t = lead + (dur - lead) * f[k]
        js += DRAW(f".{p}-box{k}", t, 0.25) + IN(f".{p}-t{k}", t + 0.1) + DRAW(f".{p}-tick{k}", t + 0.35, 0.25)
    inner += L.label(540, 1060, "↓ SPEICHER DIR DAS", 30, cls=p+"-sv") + L.label(540, 1110, "60 ODER 90 SEKUNDEN?", 26, op=.85, cls=p+"-lp")
    sv, cam = S(p, inner, dur)
    js += IN(f".{p}-sv", lead + (dur - lead) * 0.66) + IN(f".{p}-lp", lead + (dur - lead) * 0.85)
    return sv, cam + js

SCENES = {"hook": hook, "loop": loop, "exp": exp, "rule": rule, "follow": follow, "colon": colon, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("click-soft", 0, 0.3, 0.4), ("pop", 0, 4.6, 0.45), ("click-soft", 1, 0.3, 0.35),
       ("click-soft", 2, 2.9, 0.35), ("click-soft", 2, 4.3, 0.35), ("sparkle", 2, 5.7, 0.4), ("pop", 3, 2.7, 0.4), ("pop", 3, 3.8, 0.4),
       ("pop", 4, 1.0, 0.5), ("click-soft", 5, 1.6, 0.35), ("pop", 5, 4.7, 0.4), ("pop", 5, 5.4, 0.4),
       ("pop", 6, 0.7, 0.35), ("pop", 6, 2.3, 0.35), ("pop", 6, 3.7, 0.35), ("sparkle", 6, 5.7, 0.4)]
