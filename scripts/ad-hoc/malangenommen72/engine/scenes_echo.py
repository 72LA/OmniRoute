# Echo im Call – line-art theme. Executed inside render2.py namespace.
KEYS.update({"doppelt!", "doppelt", "verzögert", "sprechen", "anderen", "lautsprecher", "mikrofon", "zurück",
             "@malangenommen72", "gehirn", "vergleicht", "fünftel", "sekunde", "stocken", "person,", "person"})

LBL = font(30, "mono"); LBL_S = font(24, "mono"); BIG = font(150, "Black")

def phone_line(d, cx, cy, p=1.0, w=190, h=340, label=None):
    pts = rr_pts(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 30)
    d.polygon(pts, fill=BGC)
    poly_progress(d, pts, p, closed=True)
    if p > 0.7:
        d.line((cx - 30, cy - h / 2 + 26, cx + 30, cy - h / 2 + 26), fill=FG, width=4)
        d.ellipse((cx - 14, cy + h / 2 - 42, cx + 14, cy + h / 2 - 14), outline=FG, width=4)
    if label and p > 0.9:
        d.text((cx, cy + h / 2 + 40), label, font=LBL, fill=FG, anchor="mm")

def box(d, cx, cy, w, h, label, p=1.0, sub=None):
    pts = rr_pts(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 14)
    d.polygon(pts, fill=BGC); poly_progress(d, pts, p, closed=True, width=5)
    if p > 0.85:
        d.text((cx, cy - (12 if sub else 0)), label, font=LBL, fill=FG, anchor="mm")
        if sub: d.text((cx, cy + 26), sub, font=LBL_S, fill=(170, 170, 170), anchor="mm")

def dash(d, x0, y0, x1, y1, seg=18, gap=12, width=4, fill=None):
    L = math.dist((x0, y0), (x1, y1)); n = int(L // (seg + gap)) + 1
    for k in range(n):
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b), fill=fill or FG, width=width)

def speaker_icon(d, cx, cy):
    d.rectangle((cx - 30, cy - 18, cx - 10, cy + 18), outline=FG, width=4)
    d.polygon([(cx - 10, cy - 18), (cx + 15, cy - 40), (cx + 15, cy + 40), (cx - 10, cy + 18)], outline=FG, width=4)
    for r in (28, 46): d.arc((cx + 15 - r, cy - r, cx + 15 + r, cy + r), -45, 45, fill=FG, width=4)

def mic_icon(d, cx, cy):
    d.rounded_rectangle((cx - 16, cy - 40, cx + 16, cy + 10), radius=16, outline=FG, width=4)
    d.arc((cx - 30, cy - 20, cx + 30, cy + 30), 0, 180, fill=FG, width=4)
    d.line((cx, cy + 30, cx, cy + 48), fill=FG, width=4); d.line((cx - 18, cy + 48, cx + 18, cy + 48), fill=FG, width=4)

def SCENE(canvas, name, lt, gt, dur):
    d = ImageDraw.Draw(canvas)
    u = lt / max(dur, 0.1)
    if name == "call":
        title(canvas, "HÖRST DU MICH?", lt + 1)
        phone_line(d, 250, 790, 1, label="DU")
        phone_line(d, 830, 790, 1, label="ANDERE")
        # voice travels right, echo comes back
        x = 350 + ((lt * 260) % 380)
        poly_progress(d, wave_pts(x - 40, 700, 110, 34, 3, phase=gt * 8), 1, width=5)
        xe = 730 - ((max(0, lt - 0.6) * 260) % 380)
        for k in range(0, 110, 22):
            poly_progress(d, wave_pts(xe - 40 + k, 880, 14, 22, 0.5, phase=gt * 8 + k), 1, width=5)
        d.text((540, 640), "STIMME  →", font=LBL_S, fill=(170, 170, 170), anchor="mm")
        d.text((540, 950), "←  ECHO", font=LBL_S, fill=(170, 170, 170), anchor="mm")
    elif name == "call2":
        title(canvas, "DOPPELT & VERZÖGERT", lt)
        for y, lab in [(640, "GESAGT"), (900, "GEHÖRT")]:
            d.text((120, y - 110), lab, font=LBL, fill=FG, anchor="lm")
            poly_progress(d, [(120, y + 90), (960, y + 90)], ease_out(lt / 0.6), width=3)
        p = clamp(lt / (dur * 0.7))
        poly_progress(d, wave_pts(140, 640, 520, 70, 6), p)
        poly_progress(d, wave_pts(320, 900, 520, 70, 6), clamp(p - 0.12))
        if u > 0.55:
            dash(d, 140, 560, 140, 1000); dash(d, 320, 560, 320, 1000)
            arrow(d, 150, 1030, 310, 1030, ease_out((u - 0.55) / 0.2), width=4, head=16)
            arrow(d, 310, 1030, 150, 1030, ease_out((u - 0.55) / 0.2), width=4, head=16)
            d.text((230, 1075), "Δt", font=font(40, "mono"), fill=FG, anchor="mm")
    elif name == "stutter":
        title(canvas, "WARUM STOCKST DU?", lt)
        jx = math.sin(gt * 47) * 7
        figure_line(d, 360 + jx, 880, 1.0, "shock", ease_out(lt / 0.5))
        bx, by = 720, 640
        pts = rr_pts(bx - 230, by - 100, bx + 230, by + 100, 40)
        d.polygon(pts, fill=BGC); poly_progress(d, pts, ease_out(lt / 0.4), closed=True)
        if lt > 0.4:
            d.line((bx - 150, by + 100, bx - 210, by + 170), fill=FG, width=LW)
            txt = "I-i-ich ä-äh..."[: int((lt - 0.4) * 9) + 1]
            d.text((bx + jx, by), txt, font=font(54, "ExtraBold"), fill=FG, anchor="mm")
    elif name == "loop":
        title(canvas, "DIE ECHO-SCHLEIFE", lt)
        # stages over the sentence
        box(d, 250, 640, 300, 130, "DEIN HANDY", ease_out(u / 0.12), "✓ OK" if u > 0.15 else None)
        if u > 0.22:
            q = ease_out((u - 0.22) / 0.1)
            poly_progress(d, rr_pts(590, 520, 1020, 1110, 30), q, closed=True, width=3, fill=(140, 140, 140))
            if q > 0.9: d.text((805, 500), "ANDERE PERSON", font=LBL_S, fill=(170, 170, 170), anchor="mm")
        if u > 0.38:
            box(d, 805, 640, 330, 130, "LAUTSPRECHER", ease_out((u - 0.38) / 0.1))
            arrow(d, 400, 640, 638, 640, ease_out((u - 0.38) / 0.12))
            if u > 0.5: speaker_icon(d, 805, 760)
        if u > 0.55:
            box(d, 805, 990, 330, 130, "MIKROFON", ease_out((u - 0.55) / 0.1))
            arrow(d, 805, 820, 805, 920, ease_out((u - 0.55) / 0.12))
            if u > 0.65: mic_icon(d, 950, 880)
        if u > 0.72:
            box(d, 250, 990, 300, 130, "ZURÜCK ZU DIR", ease_out((u - 0.72) / 0.1))
            arrow(d, 638, 990, 400, 990, ease_out((u - 0.72) / 0.12))
            arrow(d, 250, 925, 250, 710, ease_out((u - 0.8) / 0.12))
        if u > 0.9:  # travelling signal dot
            path = [(400, 640), (640, 640), (805, 705), (805, 925), (640, 990), (400, 990), (250, 925), (250, 705), (400, 640)]
            L = poly_len(path); tpos = ((gt * 600) % L); acc = 0
            for i in range(len(path) - 1):
                sl = math.dist(path[i], path[i + 1])
                if acc + sl >= tpos:
                    r = (tpos - acc) / sl; px = path[i][0] + (path[i + 1][0] - path[i][0]) * r; py = path[i][1] + (path[i + 1][1] - path[i][1]) * r
                    d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=FG); break
                acc += sl
    elif name == "follow":
        s = ease_out_back(lt / 0.45); r = 150 * s; cx, cy = 540, 720
        if r > 2:
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=FG, width=6)
            m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m)
            rr = r * 0.62; mx, my = cx - r * 0.15, cy + r * 0.12
            md.ellipse((mx - rr, my - rr, mx + rr, my + rr), outline=255, width=6)
            md.ellipse((mx - rr + r * 0.32, my - rr - r * 0.2, mx + rr + r * 0.32, my + rr - r * 0.2), fill=0)
            canvas.paste((255, 255, 255, 255), (0, 0), m)
            d.text((cx + r * 0.42, cy - r * 0.15), "?", font=font(max(10, int(110 * s)), "Black"), fill=FG, anchor="mm")
        if lt > 0.3:
            d.text((540, 960), "@malangenommen72", font=font(64, "ExtraBold"), fill=FG, anchor="mm")
            q = ease_out((lt - 0.3) / 0.4)
            poly_progress(d, rr_pts(330, 1020, 750, 1110, 45), q, closed=True)
            if q > 0.9: d.text((540, 1066), "+ FOLGEN", font=font(52, "Black"), fill=FG, anchor="mm")
    elif name == "brain":
        title(canvas, "DEIN GEHIRN VERGLEICHT", lt)
        box(d, 250, 620, 330, 150, "PLAN", ease_out(u / 0.1))
        if u > 0.1: poly_progress(d, wave_pts(110, 660, 280, 22, 4), ease_out((u - 0.1) / 0.2), width=4)
        box(d, 250, 940, 330, 150, "OHR", ease_out((u - 0.25) / 0.1))
        if u > 0.35: poly_progress(d, wave_pts(110, 980, 280, 22, 4), ease_out((u - 0.35) / 0.2), width=4)
        if u > 0.5:
            poly_progress(d, circle_pts(760, 780, 90), ease_out((u - 0.5) / 0.15))
            arrow(d, 415, 620, 680, 740, ease_out((u - 0.5) / 0.15), width=5)
            arrow(d, 415, 940, 680, 820, ease_out((u - 0.5) / 0.15), width=5)
        if u > 0.66:
            d.text((760, 780), "=", font=font(110, "Black"), fill=FG, anchor="mm")
            d.text((760, 900), "ABGLEICH", font=LBL_S, fill=(170, 170, 170), anchor="mm")
        if u > 0.82:
            q = ease_out((u - 0.82) / 0.12)
            poly_progress(d, [(900, 780), (935, 820), (1000, 720)], q, width=10)
    elif name == "delay":
        title(canvas, "1/5 SEKUNDE", lt)
        d.text((540, 600), "0,2 s", font=BIG, fill=FG, anchor="mm")
        # ruler
        x0, x1, y = 140, 940, 1010
        poly_progress(d, [(x0, y), (x1, y)], ease_out(lt / 0.5), width=4)
        for k in range(6):
            x = x0 + (x1 - x0) * k / 5
            if lt > 0.3 + k * 0.08:
                d.line((x, y - 18, x, y + 18), fill=FG, width=4)
                d.text((x, y + 48), f"{k * 100}", font=LBL_S, fill=(170, 170, 170), anchor="mm")
        d.text((x1, y - 50), "ms", font=LBL_S, fill=(170, 170, 170), anchor="rm")
        if lt > 0.9:
            mx = x0 + (x1 - x0) * 0.4
            d.polygon([(mx, y - 24), (mx - 18, y - 56), (mx + 18, y - 56)], fill=FG)
        poly_progress(d, wave_pts(140, 790, 360, 40, 3), ease_out((lt - 0.4) / 0.8), width=4)
        poly_progress(d, wave_pts(140 + 320, 880, 360, 40, 3), ease_out((lt - 1.0) / 0.8), width=4)
        if u > 0.6:
            q = ease_out((u - 0.6) / 0.15)
            poly_progress(d, [(870, 760), (950, 840)], q, width=10); poly_progress(d, [(950, 760), (870, 840)], q, width=10)
    elif name == "jammer":
        title(canvas, "DAS STÖR-GERÄT", lt)
        p = ease_out(lt / 0.6)
        poly_progress(d, rr_pts(150, 760, 330, 900, 16), p, closed=True)
        if p > 0.5:
            d.arc((300, 720, 420, 940), -70, 70, fill=FG, width=LW)
            d.line((240, 900, 240, 980), fill=FG, width=LW); d.line((180, 980, 300, 980), fill=FG, width=LW)
            d.text((240, 830), "MIC+SPK", font=LBL_S, fill=FG, anchor="mm")
        if lt > 0.6:
            for k in range(4):
                r = ((lt * 220 + k * 90) % 360) + 60
                d.arc((380 - r, 830 - r, 380 + r, 830 + r), -25, 25, fill=(200, 200, 200), width=4)
        figure_line(d, 820, 900, 0.85, "shock", ease_out((lt - 0.3) / 0.5))
        if lt > 1.0:
            pts = rr_pts(700, 560, 960, 680, 36); d.polygon(pts, fill=BGC); poly_progress(d, pts, 1, closed=True)
            d.text((830, 620), "...?", font=font(60, "Black"), fill=FG, anchor="mm")
        d.text((540, 1110), "SPEECHJAMMER · KURIHARA & TSUKADA, 2012", font=LBL_S, fill=(170, 170, 170), anchor="mm")
    elif name == "share":
        title(canvas, "KENNST DU SO JEMANDEN?", lt)
        phone_line(d, 300, 800, ease_out(lt / 0.5), label="DU")
        phone_line(d, 780, 800, ease_out((lt - 0.2) / 0.5), label="ER / SIE")
        if lt > 0.6:
            q = ease_out((lt - 0.6) / 0.5)
            pts = [(410, 760 - 120 * math.sin(math.pi * k / 30)) for k in range(31)]
            pts = [(410 + 260 * k / 30, 760 - 140 * math.sin(math.pi * k / 30)) for k in range(31)]
            poly_progress(d, pts, q, width=5)
            if q > 0.95: arrow(d, 640, 740, 672, 760, 1, width=5, head=20)
        if lt > 1.2:
            s = ease_out_back((lt - 1.2) / 0.4)
            layer = Image.new("RGBA", (760, 120), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
            ld.rectangle((0, 0, 759, 119), fill=FG)
            ld.text((380, 60), "SCHICK'S IHM / IHR", font=font(58, "Black"), fill=BGC, anchor="mm")
            paste_center(canvas, layer, 540, 1080, scale=s)
