exec(open('lib_head.py').read()); exec(open('lib_woman.py').read())
a('''<defs>
<linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f5560"/><stop offset="0.3" stop-color="#6d7c74"/><stop offset="0.5" stop-color="#d9a866"/><stop offset="0.62" stop-color="#e9c58a"/><stop offset="1" stop-color="#c9d3d8"/></linearGradient>
<linearGradient id="snowg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9eef2"/><stop offset="1" stop-color="#b9c6d0"/></linearGradient>
<linearGradient id="jacket" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a6236"/><stop offset="1" stop-color="#5a3c1e"/></linearGradient>
<pattern id="plaid" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#a3262a"/><rect width="40" height="14" fill="#2a1a1c" opacity="0.75"/><rect width="14" height="40" fill="#2a1a1c" opacity="0.6"/><rect x="26" width="3" height="40" fill="#e8c9a0" opacity="0.4"/></pattern>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="url(#sky2)"/>')
def pine(x,base,h,col):
    w=h*0.42
    for i in range(4):
        y0=base-h+i*h*0.2; ww=w*(0.45+i*0.18)
        a(f'<path d="M{x},{y0:.0f} L{x+ww:.0f},{y0+h*0.32:.0f} L{x-ww:.0f},{y0+h*0.32:.0f}Z" fill="{col}"/>')
for x,h in [(20,380),(90,300),(150,420),(-30,260),(880,360),(950,420),(1010,300),(820,260)]:
    pine(x,1000,h,'#24372f')
for x,h in [(60,250),(200,220),(760,230),(930,260)]:
    pine(x,1030,h,'#1a2a24')
# cabin
a('<path d="M840,960 L900,915 L960,960 L960,1010 L840,1010Z" fill="#4a2e22"/><path d="M830,962 L900,908 L970,962" fill="none" stroke="#eef2f5" stroke-width="10" stroke-linejoin="round"/>')
a('<rect x="858" y="972" width="22" height="20" fill="#f6c46c"/><rect x="918" y="972" width="22" height="20" fill="#f6c46c"/><circle cx="899" cy="981" r="40" fill="#f6c46c" opacity="0.15"/>')
a(f'<path d="M0,1000 C250,980 700,990 1024,975 L1024,1536 L0,1536Z" fill="url(#snowg)"/>')
# man (right)
M='#e6b9a1'
a('<path d="M560,1536 L572,860 C580,790 640,760 700,750 L760,744 L820,750 C885,762 940,800 950,870 L980,1536Z" fill="url(#jacket)"/>')
a('<path d="M690,750 L760,744 L830,752 L800,980 L760,1080 L722,980Z" fill="url(#plaid)"/>')
a('<path d="M690,750 C700,790 720,800 735,790 L760,744Z M830,752 C820,792 800,800 786,790 L760,744Z" fill="#d8c29a"/>')
a('<path d="M640,770 C680,760 700,760 720,800 L700,900 Z" fill="#cbb48a"/><path d="M880,775 C845,765 822,768 806,802 L822,905Z" fill="#cbb48a"/>')
a('<path d="M840,880 L905,880 L905,940 L840,940Z" fill="#6d4a28" stroke="#4a3018" stroke-width="3"/>')
a(f'<path d="M732,650 L732,750 C748,766 778,766 794,750 L794,650Z" fill="{M}"/>')
a(f'<path d="M762,470 C816,470 846,512 846,570 C846,634 812,690 762,696 C712,690 680,634 680,570 C680,512 708,470 762,470Z" fill="url(#skin)"/>')
a('<path d="M678,555 C676,500 700,452 762,446 C826,452 850,500 848,555 C820,540 800,532 762,532 C726,532 704,540 678,555Z" fill="#7a5a34"/>')
a('<path d="M672,548 C670,468 704,400 762,394 C822,400 856,468 852,548 C826,524 800,516 762,516 C724,516 700,524 672,548Z" fill="#b89c6a"/>')
a('<path d="M672,548 C700,520 730,512 762,512 C796,512 824,520 852,548 L852,566 C826,542 798,534 762,534 C728,534 700,542 672,566Z" fill="#a38858"/>')
for xx in range(690,840,14): a(f'<line x1="{xx}" y1="420" x2="{xx+2}" y2="530" stroke="#a38858" stroke-width="3" opacity="0.6"/>')
a('<path d="M715,585 C728,578 742,578 752,584 M774,584 C784,578 798,578 811,585" fill="none" stroke="#5a3a22" stroke-width="5" stroke-linecap="round"/>')
a('<path d="M720,602 Q734,594 748,603 M778,603 Q792,594 806,602" fill="none" stroke="#2a1a14" stroke-width="5" stroke-linecap="round"/>')
a('<path d="M762,610 C758,630 752,642 752,648 C758,654 768,654 774,649" fill="none" stroke="#c48d76" stroke-width="3.5" stroke-linecap="round"/>')
a('<path d="M728,662 C745,688 782,688 798,662 C780,670 746,670 728,662Z" fill="#fff" stroke="#9a4a40" stroke-width="3"/>')
a('<ellipse cx="716" cy="640" rx="18" ry="10" fill="#e08a7a" opacity="0.3"/><ellipse cx="808" cy="640" rx="18" ry="10" fill="#e08a7a" opacity="0.3"/>')
# sledge
a('<g stroke="#8a5a2a" stroke-width="12" fill="none" stroke-linecap="round"><path d="M820,1536 L820,1180 C820,1120 880,1110 900,1150"/><path d="M960,1536 L960,1180 C960,1120 1020,1110 1040,1150"/></g>')
for y in (1220,1290,1360,1430): a(f'<rect x="814" y="{y}" width="152" height="30" rx="5" fill="#b07a40" stroke="#7a4a20" stroke-width="3"/>')
# woman (left), eyes closed, coat and scarf
a('<g transform="translate(-170,20)">'); woman(a, eyes_closed=True, outfit="coat"); a('</g>')
# dog in the middle, facing the man
a('<g transform="translate(1215,-40) scale(-0.86,0.86)">'); dog(a); a('</g>')
# her hand on a long white cane
a('<path d="M150,1110 C190,1150 250,1180 300,1185" fill="none" stroke="#22314f" stroke-width="44" stroke-linecap="round"/>')
a('<path d="M312,1170 L232,1536" stroke="#f4f4f2" stroke-width="13" stroke-linecap="round"/><path d="M241,1494 L232,1536" stroke="#c0262c" stroke-width="13"/>')
a('<path d="M290,1165 C300,1150 330,1150 338,1168 C344,1185 336,1205 318,1208 C300,1210 286,1198 286,1185Z" fill="#b8a07a" stroke="#8a7350" stroke-width="3"/>')
# snow
for i in range(120):
    x=random.uniform(0,W); y=random.uniform(380,1450); r=random.uniform(1.2,3.6)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#ffffff" opacity="{random.uniform(0.4,0.9):.2f}"/>')
a(f'<rect x="0" y="1180" width="{W}" height="356" fill="url(#fade)" opacity="0.85"/>')
a(f'<text x="{W/2}" y="175" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="92" fill="#f6dfa6" letter-spacing="1">GLIDING HOME</text>')
a(f'<text x="{W/2}" y="300" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="92" fill="#f6dfa6" letter-spacing="1">FOR CHRISTMAS</text>')
a(f'<text x="{W/2}" y="1360" text-anchor="middle" font-family="{SERIF}" font-size="54" fill="#f6ead2">Sometimes the heart needs</text>')
a(f'<text x="{W/2}" y="1432" text-anchor="middle" font-family="{SERIF}" font-size="54" fill="#f6ead2">a little help finding home.</text>')
a('</svg>'); open('gliding-home-for-christmas.svg','w').write('\n'.join(o))
