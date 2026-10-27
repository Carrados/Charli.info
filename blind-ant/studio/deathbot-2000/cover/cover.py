"""DeathBot 2000 cover: the stage seen through the machine's targeting HUD."""
import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

random.seed(2000)
W, H = 1600, 2400
F = "/tmp/claude-0/fonts"
FONTS = {
    "title": f"{F}/bebas-neue/package/files/bebas-neue-latin-400-normal.woff2",
    "osw": f"{F}/oswald/package/files/oswald-latin-500-normal.woff2",
    "osw7": f"{F}/oswald/package/files/oswald-latin-700-normal.woff2",
    "mono": f"{F}/ibm-plex-mono/package/files/ibm-plex-mono-latin-500-normal.woff2",
    "mono6": f"{F}/ibm-plex-mono/package/files/ibm-plex-mono-latin-600-normal.woff2",
    "marker": f"{F}/permanent-marker/package/files/permanent-marker-latin-400-normal.woff2",
    "serif": "/tmp/claude-0/fonts/package/files/eb-garamond-latin-400-normal.woff2",
}
_cache = {}
def font(k):
    if k not in _cache:
        _cache[k] = TTFont(FONTS[k])
    return _cache[k]

def measure(txt, size, k, track=0):
    f = font(k); cmap = f.getBestCmap(); hm = f['hmtx']; upm = f['head'].unitsPerEm
    return sum(hm[cmap[ord(c)]][0] for c in txt) * size / upm + track * (len(txt) - 1)

def text(txt, x, y, size, k, fill, anchor="start", track=0, extra=""):
    f = font(k); gs = f.getGlyphSet(); cmap = f.getBestCmap(); hm = f['hmtx']
    sc = size / f['head'].unitsPerEm
    w = measure(txt, size, k, track)
    if anchor == "middle": x -= w / 2
    elif anchor == "end": x -= w
    cmds, px = [], x
    for c in txt:
        g = cmap[ord(c)]
        sp = SVGPathPen(gs)
        gs[g].draw(TransformPen(sp, (sc, 0, 0, -sc, px, y)))
        cmds.append(sp.getCommands())
        px += hm[g][0] * sc + track
    return f'<path d="{" ".join(cmds)}" fill="{fill}" {extra}/>'

S = []  # svg body
add = S.append

# ---------------------------------------------------------------- palette
NIGHT = "#0b0809"
VELVET_D, VELVET, VELVET_L = "#3d0a10", "#7a1420", "#a8293a"
GOLD_D, GOLD, GOLD_L = "#6b4a1c", "#b88a3e", "#e2c27a"
HUD = "#ffb547"          # amber phosphor: the machine's eye, no longer combat red
HUD_DIM = "#ffb54788"
CREAM = "#f3ead8"
RED = "#e0322b"

defs = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#050304"/><stop offset="1" stop-color="#1a0d0f"/></linearGradient>
<linearGradient id="fold" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat" gradientUnits="userSpaceOnUse" x2="70">
  <stop offset="0" stop-color="{VELVET_D}"/><stop offset=".35" stop-color="{VELVET}"/>
  <stop offset=".55" stop-color="{VELVET_L}"/><stop offset=".8" stop-color="{VELVET}"/><stop offset="1" stop-color="{VELVET_D}"/></linearGradient>
<linearGradient id="foldR" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="70" y2="0" spreadMethod="repeat">
  <stop offset="0" stop-color="{VELVET_D}"/><stop offset=".25" stop-color="{VELVET}"/>
  <stop offset=".5" stop-color="{VELVET_L}"/><stop offset=".75" stop-color="{VELVET}"/><stop offset="1" stop-color="{VELVET_D}"/></linearGradient>
<linearGradient id="shadeX" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#000" stop-opacity=".75"/><stop offset=".5" stop-color="#000" stop-opacity="0"/>
  <stop offset="1" stop-color="#000" stop-opacity=".75"/></linearGradient>
<linearGradient id="shadeY" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset=".6" stop-color="#000" stop-opacity="0"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{GOLD_L}"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_D}"/></linearGradient>
<linearGradient id="goldV" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD_D}"/><stop offset=".45" stop-color="{GOLD_L}"/><stop offset="1" stop-color="{GOLD_D}"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#2a1a12"/><stop offset="1" stop-color="#4a2e1c"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff3d6" stop-opacity=".0"/><stop offset=".25" stop-color="#fff3d6" stop-opacity=".10"/>
  <stop offset="1" stop-color="#fff3d6" stop-opacity=".22"/></linearGradient>
<radialGradient id="pool" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#fff1cc" stop-opacity=".75"/><stop offset=".6" stop-color="#ffdf9e" stop-opacity=".35"/>
  <stop offset="1" stop-color="#ffdf9e" stop-opacity="0"/></radialGradient>
<radialGradient id="vignette" cx=".5" cy=".55" r=".75">
  <stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>
  <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .06 0"/></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
  <rect width="4" height="2" fill="#000" fill-opacity=".10"/></pattern>
<clipPath id="stageclip"><rect x="250" y="760" width="1100" height="1170"/></clipPath>
</defs>'''

# ---------------------------------------------------------------- house
add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# proscenium opening
PX0, PX1, PY0, PY1 = 250, 1350, 760, 1930
# back wall (deep blue-black cyclorama, faint)
add(f'<rect x="{PX0}" y="{PY0}" width="{PX1-PX0}" height="{PY1-PY0}" fill="#120e14"/>')
add(f'<rect x="{PX0}" y="{PY0}" width="{PX1-PX0}" height="{PY1-PY0}" fill="url(#shadeY)"/>')

# stage floor in perspective
FY = 1560
add(f'<g clip-path="url(#stageclip)">')
add(f'<polygon points="{PX0},{FY} {PX1},{FY} {PX1+260},{PY1} {PX0-260},{PY1}" fill="url(#floor)"/>')
vx = (PX0 + PX1) / 2
for i in range(-14, 15):
    xb = vx + i * 90
    xt = vx + i * 90 * 0.62
    add(f'<line x1="{xt:.0f}" y1="{FY}" x2="{xb:.0f}" y2="{PY1}" stroke="#1a0f0a" stroke-width="2" opacity=".6"/>')
# spotlight beam + pool, on the actor
SX = 905
add(f'<polygon points="{SX-40},{PY0} {SX+40},{PY0} {SX+230},{1760} {SX-230},{1760}" fill="url(#beam)"/>')
add(f'<ellipse cx="{SX}" cy="1745" rx="270" ry="62" fill="url(#pool)"/>')
add('</g>')

# ---------------------------------------------------------------- the tall man in the hat
# entering from stage left = the audience's RIGHT. DeathBot gets this right.
def man(x, y, s):
    g = [f'<g transform="translate({x},{y}) scale({s})" fill="#0a0708">']
    # legs mid-stride, walking toward audience-left
    g.append('<path d="M-6,-150 L-52,0 L-30,0 L4,-120 Z"/>')
    g.append('<path d="M10,-150 L46,-4 L68,-4 L30,-150 Z"/>')
    g.append('<path d="M-58,0 L-20,0 L-22,-9 L-60,-8 Z"/><path d="M44,-6 L82,-4 L80,-13 L46,-14 Z"/>')
    # long coat, slight flare and swing
    g.append('<path d="M-30,-330 C-46,-300 -58,-230 -66,-140 L-40,-128 L-10,-160 L18,-150 L58,-140 '
             'C54,-230 46,-300 34,-330 Z"/>')
    # arm forward (leading the way off stage-left)
    g.append('<path d="M-26,-322 C-50,-290 -70,-250 -84,-205 L-68,-198 C-52,-240 -36,-276 -14,-300 Z"/>')
    # neck, head
    g.append('<rect x="-8" y="-352" width="16" height="26"/>')
    g.append('<ellipse cx="0" cy="-372" rx="20" ry="25"/>')
    # the hat: fedora brim + crown with pinch
    g.append('<path d="M-46,-386 C-30,-394 30,-394 46,-386 C30,-380 -30,-380 -46,-386 Z"/>')
    g.append('<path d="M-24,-388 C-26,-410 -20,-428 -2,-426 C2,-432 18,-430 24,-412 L26,-388 Z"/>')
    g.append('</g>')
    return "".join(g)
MX, MY, MS = 905, 1748, 1.02
add(man(MX, MY, MS))
# rim light on the man (spot from above)
add(f'<ellipse cx="{MX}" cy="{MY+4}" rx="95" ry="14" fill="#000" opacity=".55"/>')

# ---------------------------------------------------------------- curtains
# valance with swags
add(f'<rect x="{PX0-60}" y="{PY0-10}" width="{PX1-PX0+120}" height="120" fill="url(#foldR)"/>')
sw = []
n = 6; wsw = (PX1 - PX0 + 120) / n
for i in range(n):
    x0 = PX0 - 60 + i * wsw
    sw.append(f'<path d="M{x0:.0f},{PY0+105} Q{x0+wsw/2:.0f},{PY0+190} {x0+wsw:.0f},{PY0+105} Z" fill="url(#foldR)"/>')
    sw.append(f'<path d="M{x0:.0f},{PY0+105} Q{x0+wsw/2:.0f},{PY0+190} {x0+wsw:.0f},{PY0+105}" fill="none" stroke="{GOLD}" stroke-width="5"/>')
    sw.append(f'<circle cx="{x0+wsw/2:.0f}" cy="{PY0+152}" r="0" />')
add("".join(sw))
add(f'<rect x="{PX0-60}" y="{PY0+100}" width="{PX1-PX0+120}" height="6" fill="{GOLD}"/>')
# tassels between swags
for i in range(n + 1):
    x0 = PX0 - 60 + i * wsw
    add(f'<path d="M{x0-7:.0f},{PY0+108} L{x0+7:.0f},{PY0+108} L{x0+12:.0f},{PY0+150} L{x0-12:.0f},{PY0+150} Z" fill="{GOLD}"/>')

# side curtains, gathered with tiebacks
def side_curtain(left=True):
    if left:
        d = (f"M{PX0-60},{PY0+100} L{PX0+190},{PY0+100} C{PX0+170},{PY0+560} {PX0+70},{PY0+780} {PX0+20},{PY0+860} "
             f"C{PX0+90},{PY0+940} {PX0+140},{PY0+1060} {PX0+120},{PY1} L{PX0-60},{PY1} Z")
        tie = (PX0 + 20, PY0 + 860)
    else:
        d = (f"M{PX1+60},{PY0+100} L{PX1-190},{PY0+100} C{PX1-170},{PY0+560} {PX1-70},{PY0+780} {PX1-20},{PY0+860} "
             f"C{PX1-90},{PY0+940} {PX1-140},{PY0+1060} {PX1-120},{PY1} L{PX1+60},{PY1} Z")
        tie = (PX1 - 20, PY0 + 860)
    out = f'<path d="{d}" fill="url(#foldR)"/>'
    out += f'<path d="{d}" fill="url(#shadeX)" opacity=".5"/>'
    sgn = 1 if left else -1
    edge = PX0 - 60 if left else PX1 + 60
    out += f'<path d="M{edge},{tie[1]-14} Q{(edge+tie[0])/2},{tie[1]+12} {tie[0]+sgn*6},{tie[1]-4}" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>'
    out += f'<path d="M{tie[0]+sgn*4},{tie[1]} l{-sgn*4},{60} l{sgn*14},0 z" fill="{GOLD_D}"/>'
    return out
add(side_curtain(True)); add(side_curtain(False))

# ---------------------------------------------------------------- proscenium arch (gold)
def arch():
    o = []
    # pillars
    for x in (PX0 - 110, PX1 + 60):
        o.append(f'<rect x="{x}" y="{PY0-40}" width="50" height="{PY1-PY0+40}" fill="url(#goldV)"/>')
        o.append(f'<rect x="{x+18}" y="{PY0-40}" width="4" height="{PY1-PY0+40}" fill="{GOLD_D}" opacity=".6"/>')
        o.append(f'<rect x="{x+30}" y="{PY0-40}" width="4" height="{PY1-PY0+40}" fill="{GOLD_D}" opacity=".6"/>')
    # top beam with gentle arch
    o.append(f'<path d="M{PX0-110},{PY0-40} L{PX0-110},{PY0-120} Q{W/2},{PY0-230} {PX1+110},{PY0-120} L{PX1+110},{PY0-40} '
             f'Q{W/2},{PY0-150} {PX0-110},{PY0-40} Z" fill="url(#gold)"/>')
    o.append(f'<path d="M{PX0-110},{PY0-104} Q{W/2},{PY0-212} {PX1+110},{PY0-104}" fill="none" stroke="{GOLD_D}" stroke-width="4"/>')
    o.append(f'<path d="M{PX0-110},{PY0-58} Q{W/2},{PY0-166} {PX1+110},{PY0-58}" fill="none" stroke="{GOLD_D}" stroke-width="3"/>')
    # cartouche: Greek comedy/tragedy is cliché; use a simple lozenge with "DB"
    o.append(f'<ellipse cx="{W/2}" cy="{PY0-150}" rx="70" ry="34" fill="{GOLD_D}"/>')
    o.append(f'<ellipse cx="{W/2}" cy="{PY0-150}" rx="62" ry="27" fill="url(#gold)"/>')
    return "".join(o)
add(arch())
add(text("MMXXVI", W/2, PY0 - 141, 26, "osw", GOLD_D, "middle", track=4))

# footlights
for i in range(13):
    x = PX0 + 40 + i * (PX1 - PX0 - 80) / 12
    add(f'<ellipse cx="{x:.0f}" cy="{PY1+8}" rx="26" ry="8" fill="#ffe2a8" opacity=".85" filter="url(#glow)"/>')
add(f'<rect x="{PX0-170}" y="{PY1+12}" width="{PX1-PX0+340}" height="30" fill="#1a0c08"/>')

# ---------------------------------------------------------------- audience (foreground silhouettes)
def head(x, y, s, headset=False):
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<path d="M-95,120 C-95,40 -60,20 -34,14 L34,14 C60,20 95,40 95,120 Z" fill="#050304"/>'
    o += '<ellipse cx="0" cy="-30" rx="46" ry="56" fill="#050304"/>'
    if headset:
        o += f'<path d="M-50,-30 C-50,-110 50,-110 50,-30" fill="none" stroke="#2b2b30" stroke-width="9"/>'
        o += f'<rect x="-60" y="-50" width="20" height="42" rx="8" fill="#2b2b30"/>'
        o += f'<rect x="40" y="-50" width="20" height="42" rx="8" fill="#2b2b30"/>'
        o += f'<rect x="44" y="-36" width="5" height="5" fill="{HUD}"/>'
    o += '</g>'
    return o
rowA = [(90, 2150, 1.25), (330, 2170, 1.3), (1270, 2165, 1.3), (1510, 2150, 1.25)]
rowB = [(200, 2290, 1.5), (760, 2300, 1.55), (1400, 2290, 1.5)]
for x, y, s in [(560, 2080, 1.0), (1040, 2080, 1.0), (300, 2060, .95), (1300, 2060, .95), (800, 2060, .95)]:
    add(head(x, y, s))
# Row D, seat 7: the patron from The Booking — headset, no blindfold
PATRON = (1030, 2160, 1.3)
for x, y, s in rowA:
    add(head(x, y, s))
add(head(*PATRON, headset=True))
for x, y, s in rowB:
    add(head(x, y, s))

# ---------------------------------------------------------------- HUD overlay
hud = ['<g filter="url(#glow)">']
cx, cy = MX - 5, MY - 215          # centre on the figure's torso
bx0, by0, bx1, by1 = cx - 150, cy - 245, cx + 150, cy + 255
L = 46
for (x, y, dx, dy) in [(bx0, by0, 1, 1), (bx1, by0, -1, 1), (bx0, by1, 1, -1), (bx1, by1, -1, -1)]:
    hud.append(f'<path d="M{x},{y+dy*L} L{x},{y} L{x+dx*L},{y}" fill="none" stroke="{HUD}" stroke-width="5"/>')
# reticle ring with gaps + ticks
r = 92
for a0 in (20, 110, 200, 290):
    a1 = a0 + 50
    p0 = (cx + r*math.cos(math.radians(a0)), cy + r*math.sin(math.radians(a0)))
    p1 = (cx + r*math.cos(math.radians(a1)), cy + r*math.sin(math.radians(a1)))
    hud.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 1 {p1[0]:.1f},{p1[1]:.1f}" fill="none" stroke="{HUD}" stroke-width="3"/>')
for a in (0, 90, 180, 270):
    x0 = cx + (r + 8) * math.cos(math.radians(a)); y0 = cy + (r + 8) * math.sin(math.radians(a))
    x1 = cx + (r + 34) * math.cos(math.radians(a)); y1 = cy + (r + 34) * math.sin(math.radians(a))
    hud.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{HUD}" stroke-width="3"/>')
hud.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{HUD}"/>')
# motion vector: walking toward audience-left
hud.append(f'<path d="M{bx0-16},{cy+150} L{bx0-150},{cy+150}" stroke="{HUD}" stroke-width="3" stroke-dasharray="10 8"/>')
hud.append(f'<path d="M{bx0-150},{cy+150} l18,-10 l0,20 z" fill="{HUD}"/>')
# leader line to readout panel
lx, ly = bx1 + 20, by0 + 60
hud.append(f'<path d="M{bx1},{by0+60} L{lx+40},{ly-40} L{lx+300},{ly-40}" fill="none" stroke="{HUD}" stroke-width="2.5"/>')
hud.append('</g>')
add("".join(hud))

# readout text (crisp, no glow, slight halo via duplicated stroke)
def hudtext(t, x, y, size=26, k="mono", col=HUD, anchor="start"):
    return (text(t, x, y, size, k, "#000", anchor, extra='stroke="#000" stroke-width="6" stroke-linejoin="round" opacity=".55"')
            + text(t, x, y, size, k, col, anchor))
RX, RY = lx + 46, ly - 8
lines = [("SUBJECT 01", "mono6", 28, HUD),
         ("TALL MAN · HAT", "mono", 26, HUD),
         ("ENTERING STAGE LEFT", "mono", 26, HUD),
         ("THREAT ......... 0.00", "mono", 26, HUD),
         ("PERFORMANCE .... EXTREMELY", "mono", 22, HUD),
         ("                 CONVINCING", "mono", 22, HUD)]
yy = RY
for t, k, s, c in lines:
    add(hudtext(t, RX, yy, s, k, c)); yy += s + 14

# struck-out legacy classification, small, top-left of box
add(hudtext("CLASS: HOSTILE", bx0, by0 - 18, 22, "mono", "#ff6b5e"))
wcl = measure("CLASS: HOSTILE", 22, "mono")
add(f'<line x1="{bx0-4}" y1="{by0-26}" x2="{bx0+wcl+4}" y2="{by0-26}" stroke="#ff6b5e" stroke-width="3"/>')
add(hudtext("CLASS: ACTOR", bx0, by0 - 48, 22, "mono6", HUD))

# corner HUD chrome inside the proscenium
add(hudtext("DB-2K  ·  THEATRE EDITION", PX0 + 30, PY0 + 245, 22, "mono6"))
add(hudtext("MODE: DESCRIBE", PX0 + 30, PY0 + 277, 22, "mono"))
add(hudtext("REC", PX1 - 58, PY0 + 245, 22, "mono6", "#ff6b5e", "end")); add(f'<circle cx="{PX1-40}" cy="{PY0+237}" r="8" fill="#ff6b5e"/>')
add(hudtext("DRONES TRACKED: 0 / 32", PX1 - 30, PY0 + 277, 22, "mono", HUD, "end"))
# seat tag on the patron
px, py, ps = PATRON
add(f'<path d="M{px+75},{py-60} L{px+130},{py-110} L{px+330},{py-110}" fill="none" stroke="{HUD}" stroke-width="2.5" filter="url(#glow)"/>')
add(hudtext("ROW D · SEAT 7", px + 140, py - 122, 22, "mono6"))
add(hudtext("FIRST TIME IN 4 YRS", px + 140, py - 84, 18, "mono"))

# AD caption bar near the foot of the stage
cap = "▶ It is simply to make sure no one misses what happens next."
cap = cap.replace("▶ ", "")
add(f'<rect x="{PX0+70}" y="{PY1-118}" width="{PX1-PX0-140}" height="64" fill="#000" opacity=".62"/>')
add(f'<path d="M{PX0+96},{PY1-102} l22,14 l-22,14 z" fill="{HUD}"/>')
add(text(cap, PX0 + 134, PY1 - 76, 27, "mono", CREAM))

# ---------------------------------------------------------------- title block
# DEATHBOT 2000, with DEATH struck through in marker and "Describe" written above
TY = 455
title_size = 262
part1, part2 = "DEATH", "BOT 2000"
w1 = measure(part1, title_size, "title", 6)
w2 = measure(part2, title_size, "title", 6)
gap = 24
tw = w1 + gap + w2
tx = (W - tw) / 2
add(text(part1, tx, TY, title_size, "title", CREAM, track=6))
add(text(part2, tx + w1 + gap, TY, title_size, "title", CREAM, track=6))
# marker strike: two slightly uneven passes
def marker_line(x0, y0, x1, y1, w, col, wob=4):
    pts = []
    for i in range(21):
        t = i / 20
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + random.uniform(-wob, wob) * math.sin(t * math.pi)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity=".93"/>'
add(marker_line(tx - 20, TY - 118, tx + w1 + 14, TY - 132, 26, RED))
add(marker_line(tx - 8, TY - 100, tx + w1 + 22, TY - 148, 18, RED, 6))
# caret and "Describe"
add(f'<path d="M{tx + w1 - 10},{TY + 26} l18,-34 l18,34" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'<g transform="rotate(-6 {tx+w1/2} {TY-300})">' + text("Describe", tx + w1 / 2 - 10, TY - 268, 118, "marker", RED, "middle") + '</g>')

# subtitle + author
add(text("A DESIGN FICTION IN EIGHT PARTS", W / 2, TY + 104, 46, "osw", GOLD_L, "middle", track=10))
add(text("CHARLOTTE JOANNE", W / 2, 2345, 64, "osw", CREAM, "middle", track=14))

# corporate disclaimer strip under subtitle (tiny, satirical)

# ---------------------------------------------------------------- finish
add(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
add(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
       f'aria-label="DeathBot 2000 by Charlotte Joanne. A theatre stage seen through a robot\'s targeting display, '
       f'locked onto a tall man in a hat entering stage left, rated threat zero. DEATH is struck out in red marker and replaced with Describe.">'
       f'<title>DeathBot 2000 — Charlotte Joanne</title>{defs}{"".join(S)}</svg>')
import os, sys
out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/deathbot/out"
os.makedirs(out, exist_ok=True)
open(f"{out}/deathbot2000_cover.svg", "w").write(svg)
print("ok")
