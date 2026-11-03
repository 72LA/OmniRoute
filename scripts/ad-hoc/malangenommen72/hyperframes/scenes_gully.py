# AI72 #08 – Rätsel: "Warum sind Gullydeckel rund?" – kg house style, riddle format (question -> pause -> solution).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kg_lib as K

KEYS = {"rätsel:", "rätsel", "gullydeckel", "rund?", "rund.", "viereckig", "überleg", "kommentare,", "@ai72,", "lösung:",
        "fallen.", "gleich", "breit.", "quadratischer", "stürzen.", "rollen", "ausrichten.", "richtig?", "schick"}
TITLES = {"hook": "RÄTSEL", "square": "RUND ODER ECKIG?", "think": "DEINE ANTWORT?", "follow": "AI72",
          "solution": "DIE LÖSUNG", "fall": "DAS PROBLEM", "bonus": "BONUS", "share": "HATTEST DU'S?"}
SCENE_CSS = """
.title { top: 258px; font-style: italic; font-size: 78px; letter-spacing: .01em; }
.rule { position: absolute; top: 372px; left: 0; right: 0; text-align: center; font-weight: 800; font-size: 34px; letter-spacing: .18em; color: #fff; }
.card { position: absolute; left: 140px; right: 140px; background: #fff6e6; color: #1b0f3d; border-radius: 26px; text-align: center;
        font-weight: 900; font-size: 54px; line-height: 1.15; padding: 26px 30px; box-shadow: 12px 14px 0 #1b0f3d; }
.pill { position: absolute; border-radius: 60px; font-weight: 900; text-align: center; color: #1b0f3d; }
.big { position: absolute; left: 0; right: 0; text-align: center; font-weight: 900; color: #ffd23f; text-shadow: 0 8px 0 #1b0f3d; }
svg { position: absolute; overflow: visible; }
"""

def S(inner):
    return f'<svg style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{inner}</svg>'

def cover(cx, cy, r, square=False):
    """flat two-tone manhole cover with grip pattern."""
    if square:
        d = K.rrect(cx - r, cy - r, 2 * r, 2 * r, 18)
        g = f'<path d="{K.rrect(cx - r + 10, cy - r + 14, 2 * r, 2 * r, 18)}" fill="{K.INK}"/>'
        g += K.shaded(d, "#7b84b8", f"M{cx} {cy - r - 10} H{cx + r + 10} V{cy + r + 10} H{cx} Z", "#5e669c")
        for k in range(-2, 3):
            g += f'<path d="M{cx - r * 0.7} {cy + k * r * 0.3} H{cx + r * 0.7}" stroke="#4b528a" stroke-width="10" stroke-linecap="round"/>'
        return g
    g = f'<circle cx="{cx + 10}" cy="{cy + 14}" r="{r}" fill="{K.INK}"/>'
    g += K.shaded(K.circ(cx, cy, r), "#7b84b8", f"M{cx} {cy - r - 10} H{cx + r + 10} V{cy + r + 10} H{cx} Z", "#5e669c")
    g += f'<circle cx="{cx}" cy="{cy}" r="{r * 0.82}" fill="none" stroke="#4b528a" stroke-width="10"/>'
    for k in range(-2, 3):
        hw = (max(0.0, (r * 0.7) ** 2 - (k * r * 0.28) ** 2)) ** 0.5
        g += f'<path d="M{cx - hw} {cy + k * r * 0.28} H{cx + hw}" stroke="#4b528a" stroke-width="10" stroke-linecap="round"/>'
    return g

def hole(cx, cy, rx, ry):
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 18}" ry="{ry + 10}" fill="#5e669c"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#0a0626"/>')

def hook(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 1) + K.plant_corner("r", 1260, 2)
             + f'<g id="{p}-cov">{cover(780, 1000, 115)}</g>' + f'<g id="{p}-guy">{K.person(230, 1150, 0.7, "point")}</g>') + \
           '<div class="rule">— AI72 ERKLÄRT —</div>' + \
           f'<div id="{p}-card" class="card" style="top:450px;left:400px;right:70px;font-size:46px">Warum sind<br/>Gullydeckel rund?</div>'
    js = (f'tl.fromTo("#{p}-card", {{scale: 0.7, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.6)"}}, 0.25);'
          f'tl.fromTo("#{p}-cov", {{scale: 0, transformOrigin: "780px 1000px"}}, {{scale: 1, duration: 0.5, ease: "back.out(1.7)"}}, 0.6);')
    return html, js

def square(p, dur, lead):
    html = S(f'<g id="{p}-a">{cover(300, 760, 130, True)}</g><g id="{p}-b">{cover(780, 760, 130)}</g>') + \
           f'<div class="pill" style="left:180px;top:950px;width:240px;height:76px;line-height:76px;font-size:38px;background:#f1eefc">ECKIG?</div>' + \
           f'<div class="pill" style="left:660px;top:950px;width:240px;height:76px;line-height:76px;font-size:38px;background:{K.Y}">RUND!</div>' + \
           f'<div id="{p}-vs" class="big" style="top:705px;font-size:80px">VS</div>'
    js = (f'tl.fromTo("#{p}-a", {{x: -120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-b", {{x: 120, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-vs", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(2)"}}, {lead + 0.6});')
    return html, js

def think(p, dur, lead):
    html = S(K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0) + f'<g id="{p}-guy">{K.person(300, 1150, 0.82, "belly")}</g>'
             + f'<g id="{p}-clk"><circle cx="740" cy="760" r="150" fill="{K.INK}" transform="translate(10 14)"/>'
             + K.shaded(K.circ(740, 760, 150), "#f1eefc", "M740 600 H900 V920 H740 Z", "#cfc6f5")
             + f'<path id="{p}-arc" d="M740 640 A120 120 0 1 1 739.9 640" fill="none" stroke="{K.MAG}" stroke-width="26" stroke-linecap="round" pathLength="1" style="stroke-dasharray:1"/></g>') + \
           f'<div id="{p}-n3" class="big" style="top:690px;left:590px;right:auto;width:300px;font-size:130px;color:{K.INK};text-shadow:none">3</div>' + \
           f'<div id="{p}-n2" class="big" style="top:690px;left:590px;right:auto;width:300px;font-size:130px;color:{K.INK};text-shadow:none;opacity:0">2</div>' + \
           f'<div id="{p}-n1" class="big" style="top:690px;left:590px;right:auto;width:300px;font-size:130px;color:{K.INK};text-shadow:none;opacity:0">1</div>' + \
           f'<div id="{p}-c" class="pill" style="left:520px;top:960px;width:440px;height:80px;line-height:80px;font-size:34px;background:{K.Y}">↓ IN DIE KOMMENTARE</div>'
    step = max(0.9, (dur - lead - 0.5) / 3)
    js = (f'tl.fromTo("#{p}-clk", {{scale: 0, transformOrigin: "740px 760px"}}, {{scale: 1, duration: 0.4, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-arc", {{strokeDashoffset: 0}}, {{strokeDashoffset: 1, duration: {step*3}, ease: "none"}}, {lead + 0.3});'
          f'tl.to("#{p}-n3", {{opacity: 0, duration: 0.05}}, {lead + 0.3 + step});tl.to("#{p}-n2", {{opacity: 1, duration: 0.05}}, {lead + 0.3 + step});'
          f'tl.to("#{p}-n2", {{opacity: 0, duration: 0.05}}, {lead + 0.3 + 2*step});tl.to("#{p}-n1", {{opacity: 1, duration: 0.05}}, {lead + 0.3 + 2*step});'
          f'tl.fromTo("#{p}-c", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 1.2});')
    return html, js

def follow(p, dur, lead):
    html = S(f'<g id="{p}-guy">{K.person(540, 935, 0.6, "wave")}</g>') + \
           f'<div class="big" style="top:955px;font-size:60px;color:#fff;text-shadow:0 5px 0 #1b0f3d">@ai72</div>' + \
           f'<div id="{p}-btn" class="pill" style="left:360px;top:1045px;width:360px;height:84px;line-height:84px;font-size:46px;background:{K.MAG};color:#fff">+ FOLGEN</div>' + \
           f'<div id="{p}-tag" class="pill" style="left:290px;top:420px;width:500px;height:70px;line-height:70px;font-size:32px;background:{K.Y}">JEDES MAL EIN RÄTSEL</div>'
    js = (f'tl.fromTo("#{p}-guy", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5, ease: "expo.out"}}, {lead});'
          f'tl.fromTo("#{p}-btn", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + 0.6});'
          f'tl.fromTo("#{p}-tag", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + 1.2});')
    return html, js

def solution(p, dur, lead):
    arrows = "".join(f'<path class="{p}-d" d="M{620 - 125*c} {760 - 125*s} L{620 + 125*c} {760 + 125*s}" stroke="{K.Y}" stroke-width="8" stroke-linecap="round" opacity="0"/>'
                     for c, s in [(1, 0), (0.707, 0.707), (0, 1), (-0.707, 0.707)])
    html = S(hole(620, 1000, 140, 40) + f'<g id="{p}-cv"><g id="{p}-rot">{cover(620, 760, 130)}</g></g>' + arrows) + \
           f'<div id="{p}-l" class="pill" style="left:250px;top:1080px;width:580px;height:76px;line-height:76px;font-size:34px;background:{K.Y}">ÜBERALL GLEICH BREIT</div>'
    js = (f'tl.fromTo("#{p}-cv", {{scale: 0, transformOrigin: "620px 760px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-rot", {{rotation: 0, svgOrigin: "620 760"}}, {{rotation: 180, duration: {max(2, dur - lead - 1)}, ease: "power1.inOut"}}, {lead + 0.5});'
          f'tl.to(".{p}-d", {{opacity: 1, duration: 0.2, stagger: 0.4}}, {lead + (dur - lead) * 0.55});'
          f'tl.fromTo("#{p}-l", {{scale: 0}}, {{scale: 1, duration: 0.4, ease: "back.out(1.8)"}}, {lead + (dur - lead) * 0.6});')
    return html, js

def fall(p, dur, lead):
    html = S(hole(540, 1010, 150, 44) + f'<g id="{p}-sq">{cover(540, 720, 105, True)}</g>'
             + f'<path id="{p}-diag" d="M391 1010 H689" stroke="{K.Y}" stroke-width="8" stroke-dasharray="16 12" opacity="0"/>') + \
           f'<div id="{p}-oops" class="big" style="top:520px;font-size:96px;opacity:0">PLUMPS!</div>'
    t = lead + (dur - lead) * 0.35
    js = (f'tl.fromTo("#{p}-sq", {{rotation: 0, svgOrigin: "540 720"}}, {{rotation: 45, duration: 0.6, ease: "power2.inOut"}}, {lead + 0.3});'
          f'tl.to("#{p}-diag", {{opacity: 1, duration: 0.2}}, {lead + 0.6});'
          f'tl.to("#{p}-sq", {{y: 330, scale: 0.55, opacity: 0, duration: 0.6, ease: "power3.in", svgOrigin: "540 720"}}, {t + 0.3});'
          f'tl.fromTo("#{p}-oops", {{scale: 0.4, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)"}}, {t + 0.9});')
    return html, js

def bonus(p, dur, lead):
    html = S(f'<path d="M80 1000 H1000" stroke="#4535b0" stroke-width="10" stroke-linecap="round"/>'
             + f'<g id="{p}-roll"><g id="{p}-spin">{cover(200, 900, 95)}</g></g>' + hole(820, 985, 120, 34)) + \
           f'<div id="{p}-l1" class="pill" style="left:90px;top:560px;width:470px;height:76px;line-height:76px;font-size:30px;background:{K.HOOD}">ROLLEN STATT TRAGEN</div>' + \
           f'<div id="{p}-l2" class="pill" style="left:580px;top:660px;width:380px;height:76px;line-height:76px;font-size:34px;background:{K.Y}">KEIN AUSRICHTEN</div>'
    span = max(2.0, (dur - lead) * 0.6)
    js = (f'tl.fromTo("#{p}-roll", {{x: 0}}, {{x: 560, duration: {span}, ease: "power1.inOut"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-spin", {{rotation: 0, svgOrigin: "200 900"}}, {{rotation: 338, duration: {span}, ease: "power1.inOut"}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-l1", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + 0.5});'
          f'tl.fromTo("#{p}-l2", {{scale: 0}}, {{scale: 1, duration: 0.35, ease: "back.out(1.8)"}}, {lead + (dur - lead) * 0.55});')
    return html, js

def share(p, dur, lead):
    bub = (f'<g id="{p}-b"><rect x="430" y="520" width="580" height="300" rx="70" fill="{K.INK}" transform="translate(10 14)"/>'
           + K.shaded(K.rrect(430, 520, 580, 300, 70), "#f1eefc", "M720 500 H1030 V840 H720 Z", "#cfc6f5")
           + '<path d="M520 810 L 470 900 L 600 815 Z" fill="#f1eefc"/></g>')
    html = S(K.plant_corner("l", 1250, 3) + K.plant_corner("r", 1240, 0) + f'<g id="{p}-guy">{K.person(240, 1150, 0.78, "point")}</g>' + bub) + \
           f'<div id="{p}-t" class="big" style="left:430px;right:auto;width:580px;top:585px;font-size:50px;color:#1b0f3d;text-shadow:none;line-height:1.15">SCHICK\'S AN<br/><span style="color:{K.MAG}">JEMANDEN!</span></div>'
    js = (f'tl.fromTo("#{p}-b", {{scale: 0, transformOrigin: "720px 670px"}}, {{scale: 1, duration: 0.45, ease: "back.out(1.6)"}}, {lead});'
          f'tl.fromTo("#{p}-t", {{opacity: 0}}, {{opacity: 1, duration: 0.2}}, {lead + 0.3});'
          f'tl.fromTo("#{p}-guy", {{x: -40, opacity: 0}}, {{x: 0, opacity: 1, duration: 0.45, ease: "expo.out"}}, 0);')
    return html, js

SCENES = {"hook": hook, "square": square, "think": think, "follow": follow, "solution": solution, "fall": fall, "bonus": bonus, "share": share}
SFX = [("whoosh-short", -1, 0.0, 0.5), ("pop", 0, 0.25, 0.5), ("pop", 0, 0.6, 0.45), ("pop", 1, 0.6, 0.45),
       ("click-soft", 2, 1.3, 0.4), ("click-soft", 2, 2.6, 0.4), ("click-soft", 2, 3.9, 0.4), ("pop", 3, 0.6, 0.5),
       ("sparkle", 4, 0.3, 0.4), ("whoosh-short", 5, 2.0, 0.45), ("impact-bass-1", 5, 2.5, 0.35), ("pop", 6, 0.5, 0.4), ("pop", 7, 0.0, 0.5)]
