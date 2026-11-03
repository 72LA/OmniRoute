"""kg_lib – AI72 house style (flat hard-edged shading, indigo world, own character). Extracted from stylelab v3.
 – flat hard-edged shading, indigo world, own character (no birds/duck)."""
import math, random
FONT = "@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,800;0,900;1,900&display=swap');"

# palette
BG0, BG1, BG2 = "#120c3a", "#1f1660", "#2c1f80"
RING = ["#33258c", "#3c2c9a", "#4634a8"]
SKIN, SKIN_D, SKIN_L = "#ff9db0", "#ec7393", "#ffc3cf"
HAIR, HAIR_D, HAIR_L = "#8a3ee0", "#6527b8", "#b77bff"
HOOD, HOOD_D, HOOD_L = "#22c2b4", "#159a93", "#7ff3e4"
PANTS, PANTS_D = "#3b2f96", "#2a2075"
Y, Y_D, ORA, MAG, BLU, BLU_D = "#ffd23f", "#f0a92a", "#ff8c42", "#ff4fa3", "#46a6ff", "#2c74e0"
LEAF = [("#2ad4c0", "#1aa596"), ("#4a7dff", "#3159d6"), ("#7a4dff", "#5a33d1"), ("#3fb5ff", "#2a86d6")]
INK = "#1b0f3d"

PREFIX = "kg_"   # set per scene by the builder so clipPath ids stay unique across sub-compositions
_id = [0]
def nid(p="c"):
    _id[0] += 1; return f"{PREFIX}{p}{_id[0]}"

def shaded(d, base, shade_d, shade, extra=""):
    """base path + hard-edged shade shape clipped to the base (Kurzgesagt-style two-tone)."""
    c = nid()
    return (f'<clipPath id="{c}"><path d="{d}"/></clipPath><path d="{d}" fill="{base}"/>'
            f'<g clip-path="url(#{c})"><path d="{shade_d}" fill="{shade}"/>{extra}</g>')

def circ(cx, cy, r):
    return f"M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z"

def rrect(x, y, w, h, r):
    return f"M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z"

# ---------------- background world ----------------
def background(seed=3, rings_at=(540, 760)):
    r = random.Random(seed)
    cx, cy = rings_at
    s = f'<rect width="1080" height="1920" fill="{BG1}"/>'
    s += f'<radialGradient id="{PREFIX}vig" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="{BG1}" stop-opacity="0"/><stop offset="1" stop-color="{BG0}"/></radialGradient>'
    for k, (rad, col) in enumerate([(560, RING[0]), (420, RING[1]), (290, RING[2])]):  # flat concentric glow rings
        s += f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{col}" opacity="{0.55 + 0.15*k}"/>'
    for _ in range(80):
        x, y = r.randint(0, 1080), r.randint(0, 1900)
        s += f'<circle cx="{x}" cy="{y}" r="{r.choice([2,2.5,3,4])}" fill="#fff" opacity="{r.uniform(.35,.9):.2f}"/>'
    for _ in range(6):  # tiny 4-point sparkles
        x, y, k = r.randint(60, 1020), r.randint(420, 1400), r.choice([10, 14, 18])
        s += f'<path d="M{x} {y-k} L{x+k*0.25} {y-k*0.25} L{x+k} {y} L{x+k*0.25} {y+k*0.25} L{x} {y+k} L{x-k*0.25} {y+k*0.25} L{x-k} {y} L{x-k*0.25} {y-k*0.25} Z" fill="{Y}" opacity=".9"/>'
    s += f'<rect width="1080" height="1920" fill="url(#{PREFIX}vig)"/>'
    return s

def leaf(x, y, L, ang, pair):
    base, dark = pair
    d = f"M0 0 C {L*0.25} {-L*0.32}, {L*0.75} {-L*0.32}, {L} 0 C {L*0.75} {L*0.32}, {L*0.25} {L*0.32}, 0 0 Z"
    half = f"M0 0 C {L*0.25} {L*0.32}, {L*0.75} {L*0.32}, {L} 0 Z"
    return f'<g transform="translate({x} {y}) rotate({ang})">{shaded(d, base, half, dark)}</g>'

def plant_corner(side, y0, seed):
    """branch of flat leaves growing in from a screen edge (frames the picture like the reference poster)."""
    r = random.Random(seed); s = ""
    x0 = -20 if side == "l" else 1100; sgn = 1 if side == "l" else -1
    s += f'<path d="M{x0} {y0} C {x0+sgn*120} {y0-40}, {x0+sgn*200} {y0-120}, {x0+sgn*230} {y0-230}" fill="none" stroke="#4a3aa8" stroke-width="16" stroke-linecap="round"/>'
    for k in range(9):
        t = k / 8
        bx = x0 + sgn * (40 + 190 * t); by = y0 - 20 - 210 * t
        ang = (-50 if k % 2 else 40) + (0 if side == "l" else 180) + r.randint(-12, 12)
        s += leaf(bx, by, r.randint(70, 110), ang, LEAF[(k + seed) % 4])
    return s

def ground_deco(y):
    g = ""
    for x, w, h, c in [(120, 150, 70, ("#3b2ca0", "#2c2085")), (930, 190, 90, ("#3b2ca0", "#2c2085")), (560, 110, 50, ("#4535b0", "#33268e"))]:
        d = f"M{x-w/2} {y} C {x-w/2} {y-h}, {x+w/2} {y-h}, {x+w/2} {y} Z"
        g += shaded(d, c[0], f"M{x} {y-h-10} H{x+w} V{y+5} H{x} Z", c[1])
    for x, k, col in [(300, 1.0, MAG), (760, 0.8, ORA), (990, 0.7, Y)]:
        g += f'<rect x="{x-8*k}" y="{y-60*k}" width="{16*k}" height="{60*k}" rx="{6*k}" fill="#f1eefc"/>'
        cap = f"M{x-40*k} {y-55*k} C {x-40*k} {y-100*k}, {x+40*k} {y-100*k}, {x+40*k} {y-55*k} Z"
        g += shaded(cap, col, f"M{x} {y-110*k} H{x+50*k} V{y-50*k} H{x} Z", "#00000033")
        g += f'<circle cx="{x-14*k}" cy="{y-75*k}" r="{6*k}" fill="#fff" opacity=".8"/>'
    for x, sd in [(40, 11), (1050, 12), (430, 13)]:
        r = random.Random(sd)
        for k in range(5):
            g += leaf(x + r.randint(-20, 20), y - 10, r.randint(60, 95), -90 + r.randint(-55, 55), LEAF[(k + sd) % 4])
    return g

def ground(y):
    s = f'<path d="M0 {y} C 260 {y-60}, 820 {y-60}, 1080 {y} V1920 H0 Z" fill="#2a1d78"/>'
    s += f'<path d="M0 {y+40} C 300 {y-10}, 780 {y-10}, 1080 {y+40} V1920 H0 Z" fill="#221763"/>'
    s += f'<path d="M0 {y+140} C 300 {y+100}, 780 {y+100}, 1080 {y+140} V1920 H0 Z" fill="#170f48"/>'
    return s

# ---------------- props ----------------
def drop(x, y, k):
    d = f"M{x} {y-k*1.5} C {x-k} {y-k*0.2}, {x-k} {y+k}, {x} {y+k} C {x+k} {y+k}, {x+k} {y-k*0.2}, {x} {y-k*1.5} Z"
    return shaded(d, BLU, f"M{x} {y-k*1.6} V{y+k*1.1} H{x+k*1.2} V{y-k*1.6} Z", BLU_D) + f'<ellipse cx="{x-k*0.38}" cy="{y+k*0.1}" rx="{k*0.17}" ry="{k*0.32}" fill="#fff" opacity=".85"/>'

def bubble(x, y, k):
    return f'<circle cx="{x}" cy="{y}" r="{k}" fill="#7fd8ff" opacity=".18"/><circle cx="{x}" cy="{y}" r="{k}" fill="none" stroke="#b9ecff" stroke-width="{max(3,k*0.12)}"/><circle cx="{x-k*0.4}" cy="{y-k*0.4}" r="{k*0.18}" fill="#fff"/>'

def soap(x, y, ang):
    d = rrect(-70, -40, 140, 80, 30)
    return f'<g transform="translate({x} {y}) rotate({ang})">' + shaded(d, MAG, "M-80 5 H80 V50 H-80 Z", "#d2357f") + bubble(60, -50, 18) + bubble(20, -70, 11) + '</g>'

def tub(x, y, s):
    d = f"M-170 -30 H170 C 170 60, 120 110, 60 110 H-60 C -120 110, -170 60, -170 -30 Z"
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += shaded(rrect(-185, -55, 370, 34, 17), "#f1eefc", "M-190 -38 H190 V-15 H-190 Z", "#c9c2ea")
    g += shaded(d, "#f1eefc", "M30 -40 H200 V130 H30 Z", "#c9c2ea")
    g += f'<path d="M-150 -40 C -100 -70, -50 -20, 0 -45 C 50 -70, 100 -25, 150 -45 V-30 H-150 Z" fill="{BLU}"/>'
    for bx, by, k in [(-120, -60, 26), (-80, -78, 16), (110, -64, 22)]:
        g += bubble(bx, by, k)
    g += f'<rect x="-110" y="105" width="22" height="30" rx="8" fill="{Y_D}"/><rect x="88" y="105" width="22" height="30" rx="8" fill="{Y_D}"/>'
    return g + '</g>'

# ---------------- hand (mitten, flat two-tone) ----------------
def finger(bx, by, L, wb, wt, ang, wrinkles=0, tone=(SKIN, SKIN_D)):
    hb, ht = wb / 2, wt / 2
    d = f"M{-hb} 0 C {-hb} {-L*0.55}, {-ht} {-L*0.8}, {-ht} {-L+ht} A {ht} {ht} 0 0 1 {ht} {-L+ht} C {ht} {-L*0.8}, {hb} {-L*0.55}, {hb} 0 Z"
    shade = f"M{hb*0.15} 10 V{-L-10} H{hb+20} V10 Z"
    ex = ""
    for k in range(wrinkles):
        yy = -L + ht * 1.5 + k * wt * 0.34
        ex += f'<path d="M{-ht*0.6} {yy} q{ht*0.3} {-wt*0.13} {ht*0.6} 0 t{ht*0.6} 0" fill="none" stroke="#c94f78" stroke-width="{wt*0.09}" stroke-linecap="round"/>'
    return f'<g transform="translate({bx} {by}) rotate({ang})">' + shaded(d, tone[0], shade, tone[1], ex) + '</g>'

def hand(cx, cy, s=1.0, rot=0, wrinkles=0):
    g = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s})">'
    for x, l, a in [(-0.42, 1.5, -11), (-0.14, 1.82, -3), (0.14, 1.75, 4), (0.4, 1.38, 12)]:
        g += finger(x * 230, -60, l * 100, 66, 52, a, wrinkles)
    palm = "M-125 -90 C -60 -112, 60 -112, 125 -90 C 140 -10, 122 90, 62 140 C 22 168, -30 168, -70 140 C -120 100, -140 -10, -125 -90 Z"
    g += shaded(palm, SKIN, "M20 -130 C 80 -60, 90 60, 40 190 H200 V-130 Z", SKIN_D)
    g += finger(-112, 40, 130, 74, 56, -52, 0)  # thumb
    g += shaded("M-52 150 C -20 172, 30 172, 62 150 L 70 240 H -60 Z", SKIN, "M10 140 V250 H90 V140 Z", SKIN_D)
    return g + '</g>'

# ---------------- character (own design) ----------------
def person(cx, gy, s=1.0, pose="wave"):
    g = f'<g transform="translate({cx} {gy}) scale({s})">'
    g += '<ellipse cx="0" cy="8" rx="150" ry="24" fill="#120a3c" opacity=".6"/>'
    for x in (-44, 44):  # legs + shoes
        g += shaded(rrect(x - 32, -200, 64, 180, 28), PANTS, f"M{x+4} -210 H{x+40} V0 H{x+4} Z", PANTS_D)
        g += shaded(f"M{x-42} -22 C {x-42} -52, {x+48} -52, {x+56} -18 C {x+58} 0, {x-42} 0, {x-42} -22 Z", "#f4f1ff", f"M{x-50} -14 H{x+70} V10 H{x-50} Z", "#cfc6f5")
    # back arm
    g += f'<path d="M-100 -450 C -150 -400, -162 -320, -150 -250" fill="none" stroke="{HOOD_D}" stroke-width="62" stroke-linecap="round"/>'
    g += f'<circle cx="-150" cy="-238" r="36" fill="{SKIN_D}"/>'
    # torso hoodie
    torso = "M-120 -455 C -125 -490, -60 -505, 0 -505 C 60 -505, 125 -490, 120 -455 L 132 -215 C 132 -185, -132 -185, -132 -215 Z"
    g += shaded(torso, HOOD, "M15 -520 C 70 -420, 90 -300, 80 -170 H160 V-520 Z", HOOD_D,
                f'<path d="M-118 -440 C -112 -470, -80 -488, -50 -494 L -60 -470 C -85 -462, -105 -448, -112 -420 Z" fill="{HOOD_L}"/>')
    g += f'<path d="M-62 -500 C -40 -450, 40 -450, 62 -500 C 40 -470, -40 -470, -62 -500 Z" fill="{HOOD_D}"/>'  # hood collar
    g += '<path d="M-22 -470 V-380 M22 -470 V-370" stroke="#f4f1ff" stroke-width="8" stroke-linecap="round"/>'
    g += shaded(rrect(-75, -320, 150, 72, 22), HOOD_D, "M0 -330 H90 V-240 H0 Z", "#0f8079")
    # front arm by pose
    if pose == "wave":
        g += f'<path d="M100 -455 C 170 -480, 205 -560, 205 -640" fill="none" stroke="{HOOD}" stroke-width="64" stroke-linecap="round"/>'
        g += f'<path d="M128 -470 C 185 -500, 210 -560, 212 -620" fill="none" stroke="{HOOD_D}" stroke-width="26" stroke-linecap="round"/>'
        g += hand(206, -708, 0.42, 8, 3)
    else:  # point
        g += f'<path d="M100 -445 C 170 -445, 235 -470, 300 -510" fill="none" stroke="{HOOD}" stroke-width="62" stroke-linecap="round"/>'
        g += finger(312, -512, 78, 42, 32, 60) + f'<circle cx="312" cy="-516" r="38" fill="{SKIN}"/>'
    # neck + head
    g += f'<rect x="-32" y="-540" width="64" height="56" rx="22" fill="{SKIN_D}"/>'
    head = circ(0, -665, 158)
    shade = "M60 -830 C 170 -760, 180 -560, 40 -505 H240 V-830 Z"
    g += f'<circle cx="-150" cy="-650" r="30" fill="{SKIN_D}"/><circle cx="150" cy="-650" r="30" fill="{SKIN_D}"/>'
    g += shaded(head, SKIN, shade, SKIN_D)
    # hair: big rounded purple cap with side swoop + flat highlight
    hair = "M-168 -650 C -190 -800, -90 -870, 10 -868 C 120 -866, 200 -800, 172 -640 C 150 -700, 110 -735, 60 -742 C 30 -705, -40 -700, -80 -735 C -110 -720, -150 -690, -168 -650 Z"
    g += shaded(hair, HAIR, "M40 -900 C 150 -840, 200 -740, 180 -620 H260 V-900 Z", HAIR_D,
                f'<path d="M-120 -790 C -90 -830, -40 -848, 10 -848 C -30 -836, -70 -815, -100 -780 Z" fill="{HAIR_L}"/>')
    g += f'<path d="M-168 -655 C -178 -610, -168 -575, -150 -548 C -150 -590, -148 -625, -136 -670 Z" fill="{HAIR}"/>'
    # face: small dot eyes, blush, tiny smile (like the reference proportions)
    for ex in (-54, 54):
        g += f'<ellipse cx="{ex}" cy="-645" rx="13" ry="17" fill="{INK}"/>'
        g += f'<ellipse cx="{ex*1.6}" cy="-600" rx="26" ry="12" fill="#ff6f9a" opacity=".55"/>'
    g += f'<path d="M-24 -596 q24 22 48 0" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    return g + '</g>'

