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
