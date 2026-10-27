# Draws the CharliPedia MCP connector card (1200 x 675). Run: python3 draw.py, then render.cjs.
W,H=1200,675
ink="#10141F"; cream="#F3EBDD"; ruby="#A51C2C"; muted="#5B5246"
tools=["search","get_entry","list_entries","get_court"]
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 f'<rect width="{W}" height="{H}" fill="{ink}"/>']
# faint index-card lines behind
for i in range(14):
    y=40+i*46; s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#1C2333" stroke-width="2"/>')
# the card
s.append(f'<rect x="90" y="95" width="1020" height="485" rx="28" fill="{cream}"/>')
s.append(f'<rect x="90" y="95" width="1020" height="18" rx="9" fill="{ruby}"/>')
s.append(f'<text x="150" y="215" font-family="DejaVu Serif" font-size="78" font-weight="bold" fill="{ink}">CharliPedia</text>')
s.append(f'<text x="152" y="268" font-family="DejaVu Sans" font-size="24" fill="{muted}" letter-spacing="2">MCP SERVER · THE MEMORY OF THE CHARLIVERSE</text>')
s.append(f'<text x="152" y="335" font-family="DejaVu Sans Mono" font-size="34" fill="{ink}">https://mcp.charli.info/</text>')
x=150
for t in tools:
    w=len(t)*19+44
    s.append(f'<rect x="{x}" y="395" width="{w}" height="58" rx="29" fill="none" stroke="{ink}" stroke-width="3"/>')
    s.append(f'<text x="{x+w/2}" y="433" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="28" fill="{ink}">{t}</text>')
    x+=w+22
# padlock
px,py=1010,170
s.append(f'<path d="M{px-42},{py+40} v-34 a42,42 0 0 1 84,0 v34" fill="none" stroke="{ruby}" stroke-width="16" stroke-linecap="round"/>')
s.append(f'<rect x="{px-66}" y="{py+34}" width="132" height="104" rx="16" fill="{ruby}"/>')
s.append(f'<circle cx="{px}" cy="{py+76}" r="13" fill="{cream}"/><rect x="{px-5}" y="{py+80}" width="10" height="32" rx="4" fill="{cream}"/>')
s.append(f'<text x="150" y="530" font-family="DejaVu Sans" font-size="26" font-weight="bold" fill="{ruby}" letter-spacing="2">READ ONLY. NO SIGN-IN. EVERY AGENT WELCOME.</text>')
s.append('</svg>')
open("charlipedia-mcp.svg","w").write("\n".join(s))
