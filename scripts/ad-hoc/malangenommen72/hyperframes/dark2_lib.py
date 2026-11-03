"""dark2_lib – malangenommen72 Dark v2: glowing white line art on black, dot grid, solid glowing figure, spaced-caps labels.
Filters are defined per scene (prefixed ids) because sub-compositions are mounted into one page."""

W = 'stroke="#fff" fill="none" stroke-linecap="round" stroke-linejoin="round"'

def defs(p):
    return (f'<defs><filter id="{p}-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<filter id="{p}-bloom" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<radialGradient id="{p}-spot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".26"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>')

def spot(p, cx, cy, rx, ry, cls=""):
    return f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{p}-spot)"/>'

def background():
    """static page background: black + dot grid in the middle band, faded to the edges."""
    return ('<defs><pattern id="bgdots" width="32" height="32" patternUnits="userSpaceOnUse"><circle cx="16" cy="16" r="1.6" fill="#5a5a5a"/></pattern>'
            '<radialGradient id="bgfade" cx=".5" cy=".5" r=".55"><stop offset=".6" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
            '<mask id="bgmask"><rect x="0" y="420" width="1080" height="900" fill="url(#bgfade)"/></mask></defs>'
            '<rect width="1080" height="1920" fill="#000"/><rect x="0" y="420" width="1080" height="900" fill="url(#bgdots)" mask="url(#bgmask)"/>')

def figure(p, x, y, s=1.0, pose="stand", cls=""):
    """solid white side-view figure (facing right), feet at (x, y). poses: stand, think, sit, point, wave."""
    g = f'<g class="{cls}" transform="translate({x} {y}) scale({s})"><g filter="url(#{p}-bloom)" fill="#fff">'
    g += '<circle cx="0" cy="-205" r="34"/><rect x="-30" y="-165" width="60" height="95" rx="28"/>'
    if pose == "sit":
        g += '<rect x="-24" y="-85" width="80" height="26" rx="13"/><rect x="34" y="-85" width="26" height="80" rx="12"/><rect x="34" y="-12" width="40" height="18" rx="9"/>'
        g += '<rect x="0" y="-150" width="90" height="22" rx="11" transform="rotate(12 0 -140)"/>'
    else:
        g += '<rect x="-13" y="-85" width="26" height="85" rx="12"/><rect x="-4" y="-12" width="40" height="18" rx="9"/>'
        if pose == "think":
            g += '<rect x="2" y="-205" width="22" height="120" rx="11" transform="rotate(14 13 -150)"/>'
        elif pose == "point":
            g += '<rect x="0" y="-150" width="120" height="22" rx="11" transform="rotate(-18 0 -140)"/>'
        elif pose == "wave":
            g += '<rect x="0" y="-150" width="22" height="120" rx="11" transform="rotate(200 11 -140)"/>'
        else:
            g += '<rect x="-6" y="-150" width="22" height="100" rx="11"/>'
    return g + '</g></g>'

def label(x, y, text, size=26, anchor="middle", op=1.0, cls=""):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="600" font-size="{size}" '
            f'letter-spacing="{size*0.38:.0f}" fill="#fff" opacity="{op}">{text}</text>')

def big(x, y, text, size=90, cls="", anchor="middle"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-family="Montserrat" font-weight="900" font-size="{size}" fill="#fff">{text}</text>'
