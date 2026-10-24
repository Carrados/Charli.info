# Draws the Carrados logo (the mark, CARRADOS, .COM and the tagline) as SVG, with all text turned into outlines.
# Fonts: Poppins Bold and Medium, and EB Garamond 400 (npm @fontsource/eb-garamond). Edit the paths below, then run it.
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
def text(t, x, y, size, path, track=0):
    f=TTFont(path); gs=f.getGlyphSet(); cm=f.getBestCmap(); hm=f['hmtx']; sc=size/f['head'].unitsPerEm
    out=[]; px=x
    for c in t:
        g=cm[ord(c)]; sp=SVGPathPen(gs); gs[g].draw(TransformPen(sp,(sc,0,0,-sc,px,y))); out.append(sp.getCommands()); px+=hm[g][0]*sc+track
    return " ".join(out), px
POP="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
POPM="/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
GAR="/tmp/claude-0/fonts/package/files/eb-garamond-latin-400-normal.woff2"
d1,w1=text("CARRADOS", 330, 160, 132, POP, track=10)
d2,w2=text(".COM", 330, 270, 96, POPM, track=8)
d3,w3=text("Insight Without Sight", 332, 360, 74, GAR)
W=int(max(w1,w2,w3))+30
# mark: 0..100 box scaled to 300px, centred on the two text lines
mark='<g transform="translate(0,22) scale(3.25)" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M85.2,20.4 A46,46 0 1 0 85.2,79.6 L76,71.9 A34,34 0 1 1 76,28.1 Z"/><path d="M24,61 Q48,40 72,61 Q48,82 24,61 Z"/><circle cx="48" cy="61" r="7.5"/><path d="M48,44 V37 M38.5,46.5 L35,40.5 M57.5,46.5 L61,40.5 M31,52 L26,48 M65,52 L70,48"/></g>'
def svg(colour, title=True):
    t='<title>Carrados: Insight Without Sight</title>' if title else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 390" role="img" aria-label="Carrados.com: Insight Without Sight" style="color:{colour}">{t}{mark}<g fill="currentColor"><path d="{d1}"/><path d="{d2}"/><path d="{d3}"/></g></svg>'
open("/tmp/claude-0/logo/carrados-logo.svg","w").write(svg("#16191d"))
open("/tmp/claude-0/logo/carrados-logo-inherit.svg","w").write(svg("currentColor"))
print(W)
