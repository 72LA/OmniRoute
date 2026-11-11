# malangenommen72 #15 – "Warum machst du so selten Komplimente?" (Zhao & Epley 2021) – Dark v2, upgraded (sub-beats, cam, fx)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dark2_lib as L
from scenes_weil import IN, DRAW, ln, follow, SCENE_CSS
from scenes_motivation import tbox
from scenes_peakend import S

W = L.W; FX = True
KEYS = {"komplimente", "selten", "anlügt", "9", "unterschätzten", "freut", "überschätzten", "peinlich", "stimmung", "heute", "magst", "schick"}
TITLES = {"hook": "MAL ANGENOMMEN …", "study": "9 EXPERIMENTE", "awk": "UND DIE ANGST?", "mood": "WAS WIRKLICH PASSIERT", "tip": "DEIN AUFTRAG"}

def hook(p, dur, lead):
    bub = "M380 700 H690 Q720 700 720 730 V820 Q720 850 690 850 H470 L420 900 L430 850 H380 Q350 850 350 820 V730 Q350 700 380 700 Z"
    inner = (L.spot(p, 540, 920, 420, 300) + tbox(110, 455, 860, ["WARUM MACHST DU SO", "SELTEN KOMPLIMENTE?"], 56)
             + L.figure(p, 300, 1110, 1.0, "point") + f'<g transform="translate(1080 0) scale(-1 1)">{L.figure(p, 300, 1110, 1.0, "stand")}</g>'
             + f'<g id="{p}-bw"><g filter="url(#{p}-glow)">{ln(bub, p + "-bub", 5)}</g>'
             + f'<g class="{p}-dots" opacity="0">{L.big(535, 800, "…", 80)}</g></g>'
             + f'<g class="{p}-th" opacity="0">{L.label(300, 760, "PEINLICH?", 30)}</g>'
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>')
    sv, cam = S(p, inner, dur); t2 = lead + (dur - lead) * 0.55
    js = (cam + DRAW(f".{p}-bub", 0.25, 0.5) + f'tl.to(".{p}-dots", {{opacity: 1, duration: 0.2}}, 0.7);'
          + f'tl.to("#{p}-bw", {{scale: 0, svgOrigin: "430 880", duration: 0.35, ease: "back.in(1.7)"}}, {t2});'
          + IN(f".{p}-th", t2 + 0.3))
    return sv, js

def study(p, dur, lead):
    span = dur - lead; base = 1040
    boxes = "".join(f'<g filter="url(#{p}-glow)">{ln(f"M{150 + k*88} 560 h64 v64 h-64 Z", f"{p}-b{k}", 4)}{ln(f"M{162 + k*88} 592 l14 16 l26 -30", f"{p}-t{k}", 6)}</g>' for k in range(9))
    inner = (L.spot(p, 540, 840, 440, 300) + boxes
             + f'<path d="M150 {base} H930" {W} stroke-width="3" stroke-opacity=".8"/>'
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-e" x="230" y="{base-120}" width="200" height="120" rx="14" {W} stroke-width="5"/>'
             + f'<rect id="{p}-r" x="650" y="{base-330}" width="200" height="330" rx="14" fill="#fff"/></g>'
             + L.label(330, base + 48, "ERWARTET", 26) + L.label(750, base + 48, "ECHTE FREUDE", 26)
             + L.big(750, base - 360, "↑", 90, p + "-up"))
    sv, cam = S(p, inner, dur); js = cam
    for k in range(9):
        t = lead + 0.15 + k * 0.17
        js += DRAW(f".{p}-b{k}", t, 0.18) + DRAW(f".{p}-t{k}", t + 0.12, 0.15)
    tb = lead + span * 0.55
    js += (f'tl.fromTo("#{p}-e", {{scaleY: 0, svgOrigin: "330 {base}"}}, {{scaleY: 1, duration: 0.45, ease: "power3.out"}}, {tb});'
           f'tl.fromTo("#{p}-r", {{scaleY: 0, svgOrigin: "750 {base}"}}, {{scaleY: 1, duration: 0.7, ease: "power3.out"}}, {tb + 0.45});' + IN(f".{p}-up", tb + 1.0))
    return sv, js

def awk(p, dur, lead):
    span = dur - lead; base = 1040
    inner = (L.spot(p, 540, 840, 420, 300) + f'<path d="M150 {base} H930" {W} stroke-width="3" stroke-opacity=".8"/>'
             + f'<g filter="url(#{p}-glow)"><rect id="{p}-g" x="230" y="{base-380}" width="200" height="380" rx="14" fill="#fff"/>'
             + f'<rect id="{p}-x" x="650" y="{base-110}" width="200" height="110" rx="14" {W} stroke-width="5"/></g>'
             + L.label(330, base + 48, "GEDACHT", 26) + L.label(750, base + 48, "ECHT", 26) + L.label(540, 590, "PEINLICH-FAKTOR", 30, cls=p + "-l")
             + f'<g class="{p}-fol" opacity="0"><rect x="200" y="390" width="680" height="64" rx="32" fill="#fff"/>'
             + f'<text x="540" y="433" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="28" fill="#000">+ FOLGEN @malangenommen72</text></g>')
    sv, cam = S(p, inner, dur)
    js = (cam + IN(f".{p}-l", lead) + f'tl.fromTo("#{p}-g", {{scaleY: 0, svgOrigin: "330 {base}"}}, {{scaleY: 1, duration: 0.6, ease: "power3.out"}}, {lead + 0.1});'
          f'tl.fromTo("#{p}-x", {{scaleY: 0, svgOrigin: "750 {base}"}}, {{scaleY: 1, duration: 0.5, ease: "power3.out"}}, {lead + span * 0.5});'
          f'tl.to(".{p}-fol", {{opacity: 1, duration: 0.25}}, {lead});tl.to(".{p}-fol", {{opacity: 0, duration: 0.25}}, {lead + 2.2});')
    return sv, js

def mood(p, dur, lead):
    span = dur - lead
    rays = "".join(ln(f"M{540 + 150*c:.0f} {700 + 150*s:.0f} L{540 + 230*c:.0f} {700 + 230*s:.0f}", f"{p}-ry", 5)
                   for c, s in [(1, 0), (.7, -.7), (0, -1), (-.7, -.7), (-1, 0), (.7, .7), (-.7, .7)])
    inner = (L.spot(p, 540, 860, 320, 300, p + "-sp") + f'<g filter="url(#{p}-glow)">{rays}</g>' + L.figure(p, 540, 1110, 1.2, "wave")
             + f'<path d="M60 1112 H1020" {W} stroke-width="3" stroke-opacity=".7"/>'
             + L.label(230, 760, "STIMMUNG", 34, cls=p + "-l") + L.big(860, 760, "↑", 120, p + "-up")
             + L.label(270, 860, "STOPP?", 30, cls=p + "-st"))
    sv, cam = S(p, inner, dur)
    js = (cam + IN(f".{p}-st", lead) + f'tl.to(".{p}-st", {{opacity: 0, duration: 0.25}}, {lead + span * 0.35});'
          + DRAW(f".{p}-ry", lead + span * 0.45, 0.4) + IN(f".{p}-l", lead + span * 0.5) + IN(f".{p}-up", lead + span * 0.6))
    return sv, js

def tip(p, dur, lead):
    span = dur - lead
    rows = ["1 PERSON", "1 EHRLICHER SATZ", "HEUTE"]; f = (0.05, 0.2, 0.36)
    inner = L.spot(p, 540, 800, 420, 300) + f'<g filter="url(#{p}-glow)">{ln("M130 520 H950 V900 H130 Z", p+"-card", 5)}</g>'
    js = DRAW(f".{p}-card", lead, 0.4)
    for k, r in enumerate(rows):
        y = 610 + k * 105
        inner += f'<g filter="url(#{p}-glow)">{ln(f"M190 {y-28} H246 V{y+28} H190 Z", p+f"-bx{k}", 4)}{ln(f"M200 {y} L215 {y+16} L240 {y-18}", p+f"-tk{k}", 6)}</g>'
        inner += L.label(280, y + 10, r, 32, "start", cls=p + f"-r{k}")
        t = lead + span * f[k]; js += DRAW(f".{p}-bx{k}", t, 0.2) + IN(f".{p}-r{k}", t + 0.1) + DRAW(f".{p}-tk{k}", t + 0.3, 0.2)
    phone = "M470 940 H610 Q630 940 630 960 V1080 Q630 1100 610 1100 H470 Q450 1100 450 1080 V960 Q450 940 470 940 Z M520 1080 H560"
    inner += (f'<g filter="url(#{p}-glow)">{ln(phone, p + "-ph", 5)}{ln("M660 1020 L760 990 L700 1080 Z", p + "-snd", 5)}</g>'
              + L.label(540, 1140, "WARUM SO SELTEN?", 28, op=.85, cls=p + "-lp"))
    sv, cam = S(p, inner, dur)
    js += DRAW(f".{p}-ph", lead + span * 0.58, 0.4) + DRAW(f".{p}-snd", lead + span * 0.68, 0.35) + IN(f".{p}-lp", lead + span * 0.86)
    return sv, cam + js

SCENES = {"hook": hook, "study": study, "awk": awk, "mood": mood, "tip": tip}
SFX = [("whoosh-short", -1, 0.0, 0.18), ("click-soft", 1, 0.2, 0.14), ("click-soft", 1, 0.9, 0.12), ("pop", 1, 3.3, 0.16),
       ("pop", 2, 1.4, 0.15), ("sparkle", 3, 1.8, 0.14), ("click-soft", 4, 0.4, 0.13), ("click-soft", 4, 1.3, 0.13),
       ("click-soft", 4, 2.2, 0.13), ("chime", 4, 4.2, 0.12)]
