exec(open('lib_head.py').read()); exec(open('lib_woman.py').read())
a(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
def tower(x,w,h,col,base=1200,spire=0):
    a(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h+400}" fill="{col}"/>')
    if spire: a(f'<path d="M{x+w/2-6},{base-h} L{x+w/2},{base-h-spire} L{x+w/2+6},{base-h}Z" fill="{col}"/>')
    for yy in range(int(base-h+20), base+300, 26):
        for xx in range(int(x+8), int(x+w-8), 18):
            if random.random()<0.32: a(f'<rect x="{xx}" y="{yy}" width="6" height="9" fill="#f4c27a" opacity="{random.uniform(0.45,0.9):.2f}"/>')
a('<defs><filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter></defs><g filter="url(#soft)">')
for x,w,h,s in [(-10,90,330,0),(70,70,250,0),(130,95,420,60),(860,80,300,0),(920,110,460,80),(990,60,280,0),(780,70,220,0)]:
    tower(x,w,h,'#1a1420',spire=s)
for x,w,h in [(30,120,200),(200,90,160),(700,120,180),(880,140,150)]:
    tower(x,w,h,'#110d16',base=1260)
a('</g>')
woman(a); dog(a, tilt=-6)
a(f'<rect x="0" y="1180" width="{W}" height="356" fill="url(#fade)"/>')
a(f'<text x="{W/2}" y="230" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="150" fill="#f1cf94" letter-spacing="4">GUIDE ME</text>')
a(f'<text x="{W/2}" y="385" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="150" fill="#f1cf94" letter-spacing="4">HOME</text>')
a(f'<text x="{W/2}" y="1360" text-anchor="middle" font-family="{SERIF}" font-size="58" fill="#f6ead2">She needed direction.</text>')
a(f'<text x="{W/2}" y="1435" text-anchor="middle" font-family="{SERIF}" font-size="58" fill="#f6ead2">It gave her love.</text>')
a('</svg>'); open('guide-me-home.svg','w').write('\n'.join(o))
