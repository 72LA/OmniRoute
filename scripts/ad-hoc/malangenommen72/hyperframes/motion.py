"""motion helpers (GSAP snippets) for cleaner, always-moving scenes."""
def floaty(sel, t, dur, amp=8, period=1.6):
    n = max(1, int(dur / period))
    return f'tl.to("{sel}", {{y: "-={amp}", duration: {period/2}, repeat: {2*n-1}, yoyo: true, ease: "sine.inOut"}}, {t});'
def spin(sel, origin, dur, deg=40):
    return f'tl.fromTo("{sel}", {{rotation: 0, svgOrigin: "{origin}"}}, {{rotation: {deg}, duration: {dur}, ease: "none"}}, 0);'
def pulse(sel, origin, t, dur, amt=0.06, period=1.2):
    n = max(1, int(dur / period))
    return f'tl.fromTo("{sel}", {{scale: 1, svgOrigin: "{origin}"}}, {{scale: {1+amt}, duration: {period/2}, repeat: {2*n-1}, yoyo: true, ease: "sine.inOut"}}, {t});'
def pop(sel, t, origin=None, d=0.5):
    o = f', svgOrigin: "{origin}"' if origin else ', transformOrigin: "50% 50%"'
    return f'tl.fromTo("{sel}", {{scale: 0, opacity: 0{o}}}, {{scale: 1, opacity: 1, duration: {d}, ease: "back.out(1.4)"}}, {t});'
def rise(sel, t, d=0.6, dy=40):
    return f'tl.fromTo("{sel}", {{y: {dy}, opacity: 0}}, {{y: 0, opacity: 1, duration: {d}, ease: "expo.out"}}, {t});'
def grow(sel, origin, t, d=0.8):
    return f'tl.fromTo("{sel}", {{scaleY: 0, svgOrigin: "{origin}"}}, {{scaleY: 1, duration: {d}, ease: "elastic.out(1, 0.75)"}}, {t});'
def count(elid, a, b, t, d=1.0, suffix=""):
    return (f'(function(){{const o={{v:{a}}};const el=document.getElementById("{elid}");'
            f'tl.to(o,{{v:{b},duration:{d},ease:"power2.out",onUpdate:()=>{{el.textContent=Math.round(o.v)+"{suffix}";}}}},{t});'
            f'tl.call(()=>{{el.textContent="{a}{suffix}";}},null,0);}})();')

# ---- added 2026-11-11: eases by role (arrivals land on a long tail, exits accelerate, numbers hold after counting) ----
def land(sel, t, d=0.45, dy=36, blur=8):
    """arrival: rises a little and sharpens, long-tailed ease – use instead of pop() for text and cards."""
    return (f'tl.fromTo("{sel}", {{y: {dy}, opacity: 0, filter: "blur({blur}px)"}}, '
            f'{{y: 0, opacity: 1, filter: "blur(0px)", duration: {d}, ease: "expo.out"}}, {t});')
def leave(sel, t, d=0.2):
    """exit: about half as long as the entrance, accelerating."""
    return f'tl.to("{sel}", {{opacity: 0, filter: "blur(8px)", duration: {d}, ease: "power3.in"}}, {t});'
def slam(sel, t, origin=None, d=0.26, s=1.5):
    """payoff number / stamp: comes in large and lands hard, once per video."""
    o = f', svgOrigin: "{origin}"' if origin else ', transformOrigin: "50% 50%"'
    return f'tl.fromTo("{sel}", {{scale: {s}, opacity: 0{o}}}, {{scale: 1, opacity: 1, duration: {d}, ease: "power4.out"}}, {t});'
def stagger(sel, t, each=0.06, d=0.4, dy=28):
    """list / grid items one after the other (40–80 ms apart)."""
    return (f'tl.fromTo("{sel}", {{y: {dy}, opacity: 0}}, '
            f'{{y: 0, opacity: 1, duration: {d}, ease: "expo.out", stagger: {each}}}, {t});')
def draw(sel, t, d=0.6):
    """line draws itself (path needs pathLength="1" and stroke-dasharray:1)."""
    return f'tl.fromTo("{sel}", {{strokeDashoffset: 1}}, {{strokeDashoffset: 0, duration: {d}, ease: "power2.inOut"}}, {t});'
def shake(sel, t, amp=10, n=5):
    """short shake on a hit (alarm, impact)."""
    return f'tl.fromTo("{sel}", {{x: -{amp}}}, {{x: {amp}, duration: 0.05, repeat: {n}, yoyo: true, ease: "sine.inOut", immediateRender: false}}, {t});tl.set("{sel}", {{x: 0}}, {t + 0.05 * (n + 1)});'
def at_word(words, line, needle, default=None):
    """spoken start time of the first word in `line` that contains `needle` (words = words.json) – anchor beats to the voice."""
    for w in words:
        if w["line"] == line and needle.lower() in w["w"].lower(): return w["t0"]
    return default
