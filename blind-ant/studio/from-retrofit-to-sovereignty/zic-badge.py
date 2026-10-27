import math
S=1080; C=S/2
SANS="'DejaVu Sans','Liberation Sans',Arial,sans-serif"
CON="'DejaVu Sans Condensed','DejaVu Sans',sans-serif"
MAG='#ff2bd6'; MAG2='#ff8af0'; INK='#08040a'
def oct(r,rot=22.5):
    pts=[(C+r*math.cos(math.radians(rot+45*i)),C+r*math.sin(math.radians(rot+45*i))) for i in range(8)]
    return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z'
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">',
f'''<defs><filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="bg"><stop offset="0" stop-color="#1a0618"/><stop offset="1" stop-color="{INK}"/></radialGradient></defs>''',
f'<rect width="{S}" height="{S}" fill="#000"/>',
f'<path d="{oct(500)}" fill="url(#bg)"/>',
f'<g filter="url(#glow)" fill="none" stroke="{MAG}"><path d="{oct(500)}" stroke-width="9"/><path d="{oct(462)}" stroke-width="3"/></g>',
]
# top band text
o.append(f'<g filter="url(#soft)" fill="{MAG2}" font-family="{CON}" font-weight="bold" text-anchor="middle">')
o.append(f'<text x="{C}" y="190" font-size="54" letter-spacing="4">ZERO INFORMATION</text>')
o.append(f'<text x="{C}" y="250" font-size="54" letter-spacing="4">CASUALTIES</text>')
o.append(f'<text x="{C}" y="898" font-size="44" letter-spacing="3">NO SINGLE-SENSE FAILURE</text>')
o.append('</g>')
# rules
o.append(f'<g stroke="{MAG}" stroke-width="3" filter="url(#soft)"><line x1="250" y1="285" x2="830" y2="285"/><line x1="250" y1="850" x2="830" y2="850"/></g>')
# big zero
o.append(f'<g filter="url(#glow)" fill="none" stroke="{MAG}"><ellipse cx="{C}" cy="568" rx="190" ry="250" stroke-width="22"/><ellipse cx="{C}" cy="568" rx="158" ry="218" stroke-width="3"/></g>')
o.append(f'<g filter="url(#soft)" fill="#ffffff" font-family="{SANS}" font-weight="bold" text-anchor="middle" letter-spacing="3">')
for i,w in enumerate(['STATE','SIGNAL','MEANING']):
    o.append(f'<text x="{C}" y="{510+i*70}" font-size="50">{w}</text>')
o.append('</g>')
o.append(f'<g stroke="{MAG}" stroke-width="2" opacity="0.8"><line x1="{C-70}" y1="528" x2="{C+70}" y2="528"/><line x1="{C-70}" y1="598" x2="{C+70}" y2="598"/></g>')
# side panels (vertical)
for x,txt,rot in [(170,'SEMANTIC ACCESS GUARANTEED',-90),(910,'MEANING DELIVERED TO ALL',90)]:
    o.append(f'<g filter="url(#soft)"><rect x="{x-30}" y="355" width="60" height="430" rx="8" fill="none" stroke="{MAG}" stroke-width="3"/>')
    o.append(f'<text x="{x}" y="570" transform="rotate({rot} {x} 570)" text-anchor="middle" dominant-baseline="middle" font-family="{CON}" font-weight="bold" font-size="22" letter-spacing="1.5" fill="{MAG2}">{txt}</text></g>')
# small corner ticks / serial
o.append(f'<text x="{C}" y="944" text-anchor="middle" font-family="{CON}" font-size="19" letter-spacing="4" fill="{MAG}" opacity="0.85">ACSINT · FIELD CERTIFICATION</text>')
o.append('</svg>')
open('zic-badge.svg','w').write('\n'.join(o))
