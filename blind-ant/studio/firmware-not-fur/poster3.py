exec(open('lib_head.py').read()); exec(open('lib_woman.py').read())
CON="'DejaVu Sans Condensed','DejaVu Sans',sans-serif"
RED='#c8261e'; INK='#17120e'; PAPER='#efd9a7'
a(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
for i in range(2600):
    x=random.uniform(0,W); y=random.uniform(0,H)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(0.5,1.8):.1f}" fill="{INK}" opacity="{random.uniform(0.04,0.16):.2f}"/>')
for cx,cy,n in [(120,560,18),(930,700,22),(980,340,10),(60,1040,12),(640,170,8)]:
    for i in range(n):
        a(f'<circle cx="{cx+random.gauss(0,40):.0f}" cy="{cy+random.gauss(0,40):.0f}" r="{random.uniform(1.5,9):.1f}" fill="{RED}" opacity="0.85"/>')
    a(f'<path d="M{cx},{cy} l2,{random.randint(40,90)}" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>')
def T(x,y,txt,size,col=INK,anchor='start',rot=0,weight='bold',font=CON):
    a(f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{weight}" font-size="{size}" fill="{col}" text-anchor="{anchor}" transform="rotate({rot} {x} {y})">{txt}</text>')
T(W/2,170,'GLIDE AID',176,RED,'middle')
T(W/2,300,'2025',140,RED,'middle')
for i,w in enumerate(['ROBOT','RIGHTS','ARE','HUMAN','RIGHTS']): T(40,300+i*58,w,56,INK,'start',-3)
for i,w in enumerate(['FIRMWARE','NOT','FUR']): T(990,300+i*60,w,56,INK,'end',3)
T(990,520,'AI',70,INK,'end',2); T(990,570,'ACCESSIBILITY',40,INK,'end',2)
# Char: the same woman as Charlotte Joanne, with her own hair, make-up and clothes
a('<g transform="translate(-40,40)">')
woman(a, outfit="none", hair=False)
# leather jacket and anarchy T-shirt
a('<path d="M150,1536 L168,1060 C176,985 225,945 300,922 L403,876 C430,900 462,900 489,876 L592,922 C665,945 712,985 722,1060 L740,1536 Z" fill="#141210"/>')
a('<path d="M395,880 L410,1536 L482,1536 L497,880 C470,900 422,900 395,880Z" fill="#221d19"/>')
a(f'<path d="M352,960 C380,940 520,940 548,960 L560,1300 L340,1300 Z" fill="#221d19"/>')
a(f'<circle cx="450" cy="1110" r="62" fill="none" stroke="{RED}" stroke-width="12"/><path d="M405,1170 L450,1045 L495,1170 M412,1120 L492,1120" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round"/>')
a('<path d="M300,922 L395,880 L405,1000 L352,1200 L330,1010 Z" fill="#1c1916" stroke="#6b625a" stroke-width="3"/>')
a('<path d="M592,922 L497,880 L487,1000 L540,1200 L562,1010 Z" fill="#1c1916" stroke="#6b625a" stroke-width="3"/>')
a('<path d="M560,980 L585,1500" stroke="#9a948c" stroke-width="5" stroke-dasharray="6 5"/>')
for x,y in [(320,940),(345,930),(560,930),(585,942),(240,990),(660,990)]: a(f'<circle cx="{x}" cy="{y}" r="6" fill="#c9c2b8"/>')
a('<rect x="360" y="1300" width="180" height="34" fill="#0d0b09" stroke="#7a7268" stroke-width="3"/><rect x="430" y="1302" width="40" height="30" fill="none" stroke="#c9c2b8" stroke-width="4"/>')
# studded choker
a('<path d="M405,842 C430,858 462,858 487,842 L487,862 C462,878 430,878 405,862Z" fill="#141210"/>')
for x in (414,430,446,462,478): a(f'<path d="M{x-5},858 L{x},846 L{x+5},858Z" fill="#d6d0c6"/>')
# red eye make-up and hoop earrings
for cx in (410,482):
    a(f'<path d="M{cx-34},632 Q{cx},596 {cx+34},630 Q{cx},616 {cx-34},632Z" fill="{RED}" opacity="0.75"/>')
    a(f'<path d="M{cx-30},648 Q{cx},664 {cx+28},648" fill="none" stroke="{RED}" stroke-width="5" opacity="0.6"/>')
a('<circle cx="345" cy="712" r="14" fill="none" stroke="#c9c2b8" stroke-width="4"/><circle cx="547" cy="712" r="14" fill="none" stroke="#c9c2b8" stroke-width="4"/>')
# spiky black hair with red streaks, short at the back
spikes=[]
import math
for i in range(17):
    t=math.pi*(1.05+i*0.9/16)
    bx=446+112*math.cos(t); by=640+150*math.sin(t)
    tx=446+(205+random.uniform(-25,25))*math.cos(t); ty=640+(235+random.uniform(-25,25))*math.sin(t)
    spikes.append((bx,by,tx,ty))
d='M330,690 '
for bx,by,tx,ty in spikes: d+=f'L{bx:.0f},{by:.0f} L{tx:.0f},{ty:.0f} '
d+='L562,690 C560,620 540,560 446,548 C352,560 332,620 330,690Z'
a(f'<path d="{d}" fill="#0f0d0c"/>')
a('<path d="M346,660 C350,600 372,580 400,575 C380,600 372,630 368,672Z M546,660 C542,600 520,580 492,575 C512,600 520,630 524,672Z" fill="#0f0d0c"/>')
a('<path d="M330,700 C320,760 330,820 345,860 L360,860 C350,800 348,750 352,690Z M562,700 C572,760 562,820 547,860 L532,860 C542,800 544,750 540,690Z" fill="#0f0d0c"/>')
for (bx,by,tx,ty) in spikes[2::5]: a(f'<path d="M{bx:.0f},{by:.0f} L{tx:.0f},{ty:.0f}" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>')
a('</g>')
# the dog, in screen-print darks
a('<g transform="translate(70,40)">'); dog(a); a('</g>')
# bottom
a(f'<rect x="0" y="1300" width="{W}" height="236" fill="{PAPER}" opacity="0.92"/>')
T(40,1360,'FEATURING',50,INK); T(350,1360,'CHAR + J2O2:',50,RED)
T(40,1460,'ANARCHY',108,RED); T(590,1428,'IN THE ACCESS',44,INK); T(590,1476,'LANE!',44,INK)
a('</svg>')
svg='\n'.join(o)
svg=svg.replace('url(#chrome)','url(#inkA)').replace('url(#chrome2)','url(#inkB)').replace('url(#glow)','url(#glowP)')
svg=svg.replace('</defs>','<linearGradient id="inkA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a7f70"/><stop offset="0.5" stop-color="#3a332c"/><stop offset="1" stop-color="#17120e"/></linearGradient><linearGradient id="inkB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6e6458"/><stop offset="1" stop-color="#17120e"/></linearGradient><radialGradient id="glowP"><stop offset="0" stop-color="#e8f4f8"/><stop offset="0.45" stop-color="#8fc7d8"/><stop offset="1" stop-color="#8fc7d8" stop-opacity="0"/></radialGradient></defs>',1)
open('glide-aid-2025.svg','w').write(svg)
