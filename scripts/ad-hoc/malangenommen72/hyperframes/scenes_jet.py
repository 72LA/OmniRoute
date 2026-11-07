# AI72 #10 – Rätsel: "Warum ist der Flug New York -> London kürzer als zurück?" (Jetstream) – kg house style, riddle format.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K
from scenes_gully import S, SCENE_CSS, think, follow, share

KEYS = {"rätsel:", "flug", "york", "london", "kürzer", "strecke,", "flugzeug.", "erddrehung", "nicht,", "kommentare,", "@ai72,",
        "lösung:", "jetstream.", "westwind,", "200", "km/h.", "schiebt", "bremst", "bonus:", "2020", "4", "std.", "56", "min.",
        "rekord", "speicher", "schick"}
TITLES = {"hook": "RÄTSEL", "clue": "GLEICHER WEG?", "think": "DEINE ANTWORT?", "follow": "AI72", "jet": "DIE LÖSUNG",
          "record": "BONUS", "share": "SPEICHERN & TEILEN"}

def plane(cx, cy, s=1.0, flip=False):
    """flat side-view airliner facing right, centre (cx, cy)."""
    body = K.rrect(-150, -26, 300, 52, 26)
    g = f'<g transform="translate({cx} {cy}) scale({-s if flip else s} {s})">'
    g += '<path d="M-120 -20 L-160 -86 H-120 L-70 -20 Z" fill="#cfc6f5"/>'                       # tail fin
    g += K.shaded(body, "#f4f1ff", "M-170 4 H170 V40 H-170 Z", "#cfc6f5")
    g += f'<path d="M110 -26 Q150 -26 160 0 Q150 26 110 26 Z" fill="#f4f1ff"/>'                    # nose
    g += f'<path d="M118 -14 h18 l10 10 h-28 Z" fill="{K.INK}"/>'                                   # cockpit
    g += "".join(f'<circle cx="{x}" cy="-6" r="6" fill="{K.BLU}"/>' for x in range(-90, 100, 28))  # windows
    g += f'<path d="M-30 8 L-80 70 H-40 L30 8 Z" fill="{K.MAG}"/>'                                  # wing
    g += f'<rect x="-150" y="-6" width="300" height="6" fill="{K.MAG}" opacity=".9"/>'
    return g + '</g>'

def city(x, y, name, col):
    return (f'<circle cx="{x}" cy="{y}" r="22" fill="{col}"/><circle cx="{x}" cy="{y}" r="9" fill="#fff"/>'
            f'<text x="{x}" y="{y + 66}" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="34" fill="#fff">{name}</text>')

def hook(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + '<path d="M170 900 Q540 700 910 900" fill="none" stroke="#6b5ad6" stroke-width="8" stroke-dasharray="18 16" stroke-linecap="round"/>'
             + city(170, 900, "NEW YORK", K.ORA) + city(910, 900, "LONDON", K.Y)
             + f'<g id="{p}-pl">{plane(540, 790, 0.75)}</g>') + \
           '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;font-size:46px">NY → London kürzer<br/>als zurück. Warum?</div>' + \
           f'<div class="pill" style="left:110px;top:1030px;width:400px;height:72px;line-height:72px;font-size:32px;background:{K.Y}">HIN ≈ 7 STD</div>' + \
           f'<div class="pill" style="left:570px;top:1030px;width:400px;height:72px;line-height:72px;font-size:32px;background:#f1eefc">ZURÜCK ≈ 8 STD</div>'
    js = (f'tl.fromTo("#{p}-card", {{scale: 0.7, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)"}}, 0.2);'
          f'tl.fromTo("#{p}-pl", {{x: -330, y: 90}}, {{x: 0, y: 0, duration: 1.2, ease: "power2.out"}}, 0.4);')
    return html, js

def clue(p, dur, lead):
    globe = (K.shaded(K.circ(540, 820, 210), K.BLU, "M540 590 H780 V1050 H540 Z", K.BLU_D)
             + '<path d="M420 700 q60 -40 120 0 q40 30 20 80 q-60 30 -110 -10 Z M560 860 q70 -20 110 30 q-10 60 -80 60 q-50 -40 -30 -90 Z" fill="#2ad4c0"/>')
    html = S(f'<g id="{p}-gl">{globe}</g>'
             + f'<path id="{p}-arr" d="M300 640 A280 280 0 0 1 780 640" fill="none" stroke="{K.Y}" stroke-width="14" stroke-linecap="round"/>'
             + f'<path id="{p}-ah" d="M780 640 l-46 -6 l20 40 Z" fill="{K.Y}"/>'
             + f'<g id="{p}-x"><path d="M380 660 L700 980 M700 660 L380 980" stroke="{K.MAG}" stroke-width="30" stroke-linecap="round"/></g>') + \
           f'<div id="{p}-a" class="pill" style="left:80px;top:470px;width:440px;height:72px;line-height:72px;font-size:30px;background:#f1eefc">GLEICHE STRECKE</div>' + \
           f'<div id="{p}-b" class="pill" style="left:560px;top:470px;width:440px;height:72px;line-height:72px;font-size:30px;background:#f1eefc">GLEICHES FLUGZEUG</div>' + \
           f'<div id="{p}-c" class="pill" style="left:240px;top:1060px;width:600px;height:76px;line-height:76px;font-size:32px;background:{K.Y}">ERDDREHUNG? NEIN!</div>'
    t2 = lead + (dur - lead) * 0.4
    js = (f'tl.fromTo("#{p}-a", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead});'
          f'tl.fromTo("#{p}-b", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.9});'
          f'tl.fromTo("#{p}-gl", {{scale: 0, transformOrigin: "540px 820px"}}, {{scale: 1, duration: 0.5, ease: "back.out(1.6)"}}, {t2 - 0.3});'
          f'tl.fromTo(["#{p}-arr", "#{p}-ah"], {{opacity: 0}}, {{opacity: 1, duration: 0.3}}, {t2 + 0.2});'
          f'tl.fromTo("#{p}-x", {{scale: 0, transformOrigin: "540px 820px"}}, {{scale: 1, duration: 0.35, ease: "back.out(2)"}}, {t2 + 1.0});'
          f'tl.fromTo("#{p}-c", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {t2 + 1.2});')
    return html, js

def jet(p, dur, lead):
    streaks = "".join(f'<path class="{p}-w" d="M{x} {y} h{L}" stroke="{c}" stroke-width="14" stroke-linecap="round" opacity=".9"/>'
                      for x, y, L, c in [(120, 700, 220, "#2ad4c0"), (420, 730, 180, K.Y), (700, 690, 240, "#2ad4c0"), (250, 770, 160, "#7ff3e4"),
                                         (560, 790, 220, K.Y), (860, 760, 140, "#7ff3e4")])
    html = S(f'<rect x="80" y="640" width="920" height="200" rx="100" fill="#2a1f86"/>' + f'<g id="{p}-ws">{streaks}</g>'
             + f'<g id="{p}-e">{plane(330, 900, 0.55)}</g>' + f'<g id="{p}-wst">{plane(760, 995, 0.55, flip=True)}</g>') + \
           f'<div id="{p}-n" class="big" style="top:440px;font-size:80px">JETSTREAM</div>' + \
           f'<div id="{p}-h" class="pill" style="left:90px;top:555px;width:330px;height:64px;line-height:64px;font-size:28px;background:#f1eefc">≈ 10 KM HÖHE</div>' + \
           f'<div id="{p}-s" class="pill" style="left:620px;top:555px;width:360px;height:64px;line-height:64px;font-size:28px;background:{K.Y}">OFT ÜBER 200 KM/H</div>' + \
           f'<div id="{p}-o" class="pill" style="left:80px;top:1060px;width:440px;height:70px;line-height:70px;font-size:30px;background:#2ad4c0">→ OSTEN: SCHUB</div>' + \
           f'<div id="{p}-b" class="pill" style="left:560px;top:1060px;width:440px;height:70px;line-height:70px;font-size:30px;background:{K.MAG};color:#fff">← WESTEN: BREMSE</div>'
    span = dur - lead
    t1 = lead + span * 0.72; t2 = lead + span * 0.86
    js = (f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + 0.2});'
          f'tl.fromTo("#{p}-ws", {{x: -120}}, {{x: 120, duration: {span}, ease: "none"}}, {lead});'
          f'tl.fromTo("#{p}-h", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.18});'
          f'tl.fromTo("#{p}-s", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.45});'
          f'tl.fromTo("#{p}-e", {{x: -260, opacity: 0}}, {{x: 300, opacity: 1, duration: 1.2, ease: "power2.in"}}, {t1 - 0.4});'
          f'tl.fromTo("#{p}-o", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {t1});'
          f'tl.fromTo("#{p}-wst", {{x: 100, opacity: 0}}, {{x: -60, opacity: 1, duration: 1.6, ease: "power3.out"}}, {t2 - 0.3});'
          f'tl.fromTo("#{p}-b", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {t2});')
    return html, js

def record(p, dur, lead):
    clock = (f'<circle cx="300" cy="820" r="150" fill="{K.INK}" transform="translate(10 14)"/>'
             + K.shaded(K.circ(300, 820, 150), "#f1eefc", "M300 660 H460 V980 H300 Z", "#cfc6f5")
             + f'<g id="{p}-hand"><path d="M300 820 V700" stroke="{K.MAG}" stroke-width="16" stroke-linecap="round"/></g>'
             + f'<circle cx="300" cy="820" r="16" fill="{K.INK}"/>')
    html = S(clock + f'<g id="{p}-pl">{plane(760, 760, 0.6)}</g>'
             + f'<path d="M560 840 h120 M520 880 h180 M580 920 h100" stroke="{K.Y}" stroke-width="10" stroke-linecap="round" id="{p}-sp"/>') + \
           f'<div id="{p}-n" class="big" style="top:470px;font-size:100px">4:56 STD</div>' + \
           f'<div id="{p}-y" class="pill" style="left:560px;top:960px;width:400px;height:70px;line-height:70px;font-size:30px;background:{K.Y}">FEB. 2020 · STURM</div>' + \
           f'<div id="{p}-r" class="pill" style="left:200px;top:1050px;width:680px;height:72px;line-height:72px;font-size:30px;background:#f1eefc">REKORD OHNE ÜBERSCHALL</div>'
    span = dur - lead
    js = (f'tl.fromTo("#{p}-y", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-pl", {{x: -200}}, {{x: 60, duration: {span}, ease: "power1.inOut"}}, {lead});'
          f'tl.fromTo("#{p}-hand", {{rotation: 0, svgOrigin: "300 820"}}, {{rotation: 720, duration: {span * 0.6}, ease: "power2.inOut"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-n", {{scale: 0.3, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)"}}, {lead + span * 0.45});'
          f'tl.fromTo("#{p}-r", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + span * 0.8});')
    return html, js

SCENES = {"hook": hook, "clue": clue, "think": think, "follow": follow, "jet": jet, "record": record, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.2, 0.45), ("whoosh-short", 0, 0.5, 0.35), ("pop", 1, 0.0, 0.4), ("pop", 1, 0.9, 0.4),
       ("pop", 1, 3.2, 0.45), ("click-soft", 2, 1.2, 0.4), ("click-soft", 2, 2.3, 0.4), ("pop", 3, 0.6, 0.5), ("sparkle", 4, 0.2, 0.4),
       ("whoosh-short", 4, 6.8, 0.4), ("whoosh-short", 4, 8.3, 0.35), ("pop", 5, 3.8, 0.5), ("pop", 6, 0.0, 0.5)]
