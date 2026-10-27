import random
random.seed(7)
W,H=1024,1536
SERIF="'DejaVu Serif','Liberation Serif',Georgia,serif"
o=[]
a=o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1426"/><stop offset="0.35" stop-color="#2a1f3d"/><stop offset="0.62" stop-color="#7a3a2c"/><stop offset="0.78" stop-color="#b8612f"/><stop offset="1" stop-color="#2a1a20"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#3a0510"/><stop offset="0.35" stop-color="#6B0817"/><stop offset="0.7" stop-color="#8E1B24"/><stop offset="1" stop-color="#A51C2C"/></linearGradient>
<linearGradient id="hairhi" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8303c" stop-opacity="0.9"/><stop offset="1" stop-color="#8E1B24" stop-opacity="0"/></linearGradient>
<radialGradient id="skin" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stop-color="#f6dccb"/><stop offset="0.7" stop-color="#ecc5ae"/><stop offset="1" stop-color="#d9a990"/></radialGradient>
<linearGradient id="coat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c1f2a"/><stop offset="1" stop-color="#0b0c12"/></linearGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9fb4cf"/><stop offset="0.45" stop-color="#3d5576"/><stop offset="1" stop-color="#15223a"/></linearGradient>
<linearGradient id="chrome2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f97ba"/><stop offset="1" stop-color="#1a2944"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#e6f6ff"/><stop offset="0.4" stop-color="#55c8ff"/><stop offset="1" stop-color="#55c8ff" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0c12" stop-opacity="0"/><stop offset="1" stop-color="#0b0c12" stop-opacity="0.95"/></linearGradient>
</defs>''')
