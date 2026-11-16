import json, base64, math
MAP=json.load(open('/home/claude/mapgen/map.json'))
font=base64.b64encode(open('node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2','rb').read()).decode()
INK="#1b1712"; CREAM="#f3ead7"; RED="#c8261e"; DRED="#a51c16"; SKIN="#f0c9a0"; SUIT="#1c2540"
def usa(fill, stroke, sw):
    return "".join(f'<path d="{v["d"]}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>' for k,v in MAP.items() if k not in("Alaska","Hawaii"))
S, ROT, CX, CY = 0.80, -5, 512, 640
def tp(x,y):
    x,y=(x-487)*S,(y-300)*S
    a=math.radians(ROT); return CX+x*math.cos(a)-y*math.sin(a), CY+x*math.sin(a)+y*math.cos(a)
def flag():
    X0,Y0,W,H=18,13,940,585
    sh=H/13; g=[f'<rect x="{X0}" y="{Y0}" width="{W}" height="{H}" fill="#fbf6ea"/>']
    for i in range(0,13,2): g.append(f'<rect x="{X0}" y="{Y0+i*sh:.1f}" width="{W}" height="{sh:.1f}" fill="#b5202a"/>')
    cw,chh=W*0.4,sh*7
    g.append(f'<rect x="{X0}" y="{Y0}" width="{cw:.1f}" height="{chh:.1f}" fill="#25306b"/>')
    for r in range(9):
        n=6 if r%2==0 else 5
        for c in range(n):
            x=X0+cw*((c*2+(1 if r%2==0 else 2))/12); y=Y0+chh*((r+1)/10)
            g.append(f'<polygon points="{star(x,y,11)}" fill="#fff"/>')
    return "".join(g)
def star(cx,cy,r):
    p=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.42
        p.append(f"{cx+math.cos(a)*rr:.1f},{cy+math.sin(a)*rr:.1f}")
    return " ".join(p)
def build(title, square=False):
    o=[]
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024"><style>@font-face{{font-family:A;src:url(data:font/woff2;base64,{font})}}</style>')
    o.append(f'<defs><clipPath id="c"><rect width="1024" height="1024" rx="{0 if square else 224}"/></clipPath></defs><g clip-path="url(#c)">')
    o.append(f'<rect width="1024" height="1024" fill="{RED}"/>')
    for i in range(14):
        a=i*2*math.pi/14; w=0.12
        p=[(512,640),(512+1600*math.cos(a-w),640+1600*math.sin(a-w)),(512+1600*math.cos(a+w),640+1600*math.sin(a+w))]
        o.append(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x,y in p)}" fill="{DRED}"/>')
    # shadow under map
    o.append(f'<ellipse cx="530" cy="930" rx="330" ry="34" fill="#000" opacity=".22"/>')
    # control bar (cross) — positioned under the hand
    barY=250
    bar_pts=[(318,barY+14),(706,barY-14)]   # tilted crossbar ends
    # strings: attach points on map
    targets=["Washington","California","Texas","Florida","Maine","Minnesota"]
    anchors=[(330,barY+13),(372,barY+10),(470,barY+3),(600,barY-6),(694,barY-13),(520,barY)]
    tg=[tp(*MAP[t]["c"]) for t in targets]
    # order anchors left->right to match targets left->right
    pairs=sorted(zip(sorted(anchors), sorted(tg)))
    # map
    o.append(f'<g transform="translate({CX} {CY}) rotate({ROT}) scale({S}) translate(-487 -300)">{usa(INK,INK,16)}<clipPath id="us">{usa("#000","none",0)}</clipPath><g clip-path="url(#us)">{flag()}</g></g>')
    o.append(f'<g stroke="{INK}" stroke-width="4">'+"".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{t[0]:.0f}" y2="{t[1]:.0f}"/>' for a,t in pairs)+'</g>')
    # knots
    o.append("".join(f'<circle cx="{t[0]:.0f}" cy="{t[1]:.0f}" r="9" fill="{RED}" stroke="{INK}" stroke-width="4"/>' for a,t in pairs))
    # crossbar
    o.append(f'<g transform="rotate(-4 512 {barY})"><rect x="300" y="{barY-16}" width="424" height="32" rx="12" fill="#7a5230" stroke="{INK}" stroke-width="9"/>'
             f'<rect x="496" y="{barY-120}" width="32" height="200" rx="12" fill="#7a5230" stroke="{INK}" stroke-width="9"/></g>')
    if title:
        o.append(f'<text x="512" y="1000" font-family="A" font-size="64" text-anchor="middle" fill="{CREAM}" stroke="{INK}" stroke-width="10" paint-order="stroke" letter-spacing="4">THE SOCIAL COLLAPSE</text>')
    o.append('</g>')
    if not square: o.append(f'<rect x="10" y="10" width="1004" height="1004" rx="216" fill="none" stroke="{INK}" stroke-width="20"/>')
    o.append('</svg>')
    return "".join(o)
open("puppet.svg","w").write(build(False))
open("puppet-title.svg","w").write(build(True))
open("puppet-square.svg","w").write(build(False, True))
