#!/usr/bin/env python3
"""Genera eras.js (escenas SVG + lógica) para el easter egg de Taylor Swift."""
import math, random, json, sys

OUT_JS = sys.argv[1]
W, H = 1600, 900

def f(x): return f"{x:.1f}".rstrip("0").rstrip(".")

def star4(x, y, r, fill, op=1):
    return (f'<path d="M{f(x)} {f(y-r)} Q{f(x+r*.18)} {f(y-r*.18)} {f(x+r)} {f(y)} Q{f(x+r*.18)} {f(y+r*.18)} {f(x)} {f(y+r)} '
            f'Q{f(x-r*.18)} {f(y+r*.18)} {f(x-r)} {f(y)} Q{f(x-r*.18)} {f(y-r*.18)} {f(x)} {f(y-r)}Z" fill="{fill}" opacity="{op}"/>')

def dots(rng, n, x0, x1, y0, y1, rmin, rmax, fill, opmin=.4, opmax=1):
    return "".join(f'<circle cx="{f(rng.uniform(x0,x1))}" cy="{f(rng.uniform(y0,y1))}" r="{f(rng.uniform(rmin,rmax))}" fill="{fill}" opacity="{f(rng.uniform(opmin,opmax))}"/>' for _ in range(n))

def sides(rng, n, y0, y1):
    """puntos solo en los márgenes (izquierda/derecha de la hoja)"""
    pts = []
    for i in range(n):
        x = rng.uniform(20, 400) if i % 2 == 0 else rng.uniform(1200, 1580)
        pts.append((x, rng.uniform(y0, y1)))
    return pts

def cloud(x, y, s, fill, op=.9):
    parts = [(0,0,40),(38,-18,46),(84,-4,40),(118,8,30),(-34,10,28),(40,14,40),(80,16,34)]
    return f'<g opacity="{op}" fill="{fill}">' + "".join(f'<circle cx="{f(x+dx*s)}" cy="{f(y+dy*s)}" r="{f(r*s)}"/>' for dx,dy,r in parts) + '</g>'

def butterfly(x, y, s, c1, c2, rot=0):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({s})">'
            f'<path d="M0 0 C-14 -20 -30 -8 -18 4 C-28 16 -10 22 0 6Z" fill="{c1}"/>'
            f'<path d="M0 0 C14 -20 30 -8 18 4 C28 16 10 22 0 6Z" fill="{c2}"/>'
            f'<rect x="-1.5" y="-8" width="3" height="18" rx="1.5" fill="#3a2a3a"/></g>')

def pine(x, base, h, color):
    w = h * .42
    tiers = ""
    for i in range(4):
        top = base - h + i * h * .2
        bot = top + h * .38
        ww = w * (.45 + i * .2)
        tiers += f'<path d="M{f(x)} {f(top)} L{f(x+ww)} {f(bot)} L{f(x-ww)} {f(bot)}Z"/>'
    return f'<g fill="{color}"><rect x="{f(x-h*.03)}" y="{f(base-h*.12)}" width="{f(h*.06)}" height="{f(h*.12)}"/>{tiers}</g>'

def bare_tree(rng, x, y, length, angle, depth, width, color):
    if depth == 0 or length < 6:
        return ""
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y - length * math.sin(math.radians(angle))
    s = f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{color}" stroke-width="{f(width)}" stroke-linecap="round"/>'
    for da in (-rng.uniform(18, 32), rng.uniform(18, 32)):
        s += bare_tree(rng, x2, y2, length * rng.uniform(.66, .8), angle + da, depth - 1, width * .68, color)
    return s

def firework(rng, x, y, r, colors):
    s = f'<g transform="translate({f(x)} {f(y)})">'
    n = 18
    for i in range(n):
        a = i * 2 * math.pi / n
        c = colors[i % len(colors)]
        x1, y1 = math.cos(a) * r * .25, math.sin(a) * r * .25
        x2, y2 = math.cos(a) * r, math.sin(a) * r
        s += f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>'
        s += f'<circle cx="{f(x2*1.12)}" cy="{f(y2*1.12)}" r="3.2" fill="{c}"/>'
    s += f'<circle r="{f(r*.12)}" fill="#fff" opacity=".8"/></g>'
    return s

def gull(x, y, s, color):
    return f'<path d="M{f(x)} {f(y)} q{f(10*s)} {f(-9*s)} {f(20*s)} 0 q{f(10*s)} {f(-9*s)} {f(20*s)} 0" fill="none" stroke="{color}" stroke-width="{f(2.4*s)}" stroke-linecap="round"/>'

def svg(inner, defs=""):
    return (f'<svg class="era-scene" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs>{defs}</defs>{inner}</svg>')

def lin(id_, stops, vertical=True):
    xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="1"'
    return f'<linearGradient id="{id_}" {xy}>' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>'

def rad(id_, stops):
    return f'<radialGradient id="{id_}">' + "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops) + '</radialGradient>'

scenes = {}

# ---------------------------------------------------------------- Taylor Swift (debut)
rng = random.Random(1)
defs = lin("dbSky", [(0,"#2c6f6a"),(.55,"#8fcfc4"),(1,"#f3eccb")]) + rad("dbSun", [(0,"#fff4c8",.95),(.4,"#ffe7a3",.6),(1,"#ffe7a3",0)])
s = f'<rect width="{W}" height="{H}" fill="url(#dbSky)"/><circle cx="1420" cy="560" r="230" fill="url(#dbSun)"/>'
s += '<path d="M0 690 Q260 610 560 670 T1100 650 T1600 680 V900 H0Z" fill="#7cb98a"/>'
s += '<path d="M0 770 Q380 700 800 780 T1600 750 V900 H0Z" fill="#4f8f5f"/>'
# roble con columpio
s += '<path d="M1360 780 C1368 700 1350 640 1372 560 L1402 560 C1420 640 1404 700 1416 780Z" fill="#5a3a22"/>'
for (dx,dy,r,c) in [(0,-40,90,"#3f7a4a"),(-80,10,70,"#4b8a55"),(80,0,76,"#447f4e"),(-40,-110,70,"#529660"),(50,-100,74,"#3a7044"),(140,-50,56,"#4b8a55"),(-140,-40,52,"#447f4e")]:
    s += f'<circle cx="{1386+dx}" cy="{520+dy}" r="{r}" fill="{c}"/>'
s += '<line x1="1300" y1="560" x2="1300" y2="700" stroke="#6b4a2a" stroke-width="3"/><line x1="1350" y1="560" x2="1350" y2="700" stroke="#6b4a2a" stroke-width="3"/><rect x="1290" y="698" width="70" height="10" rx="3" fill="#8a5a3a"/>'
# cerca y guitarra
for x in range(20, 460, 64):
    s += f'<rect x="{x}" y="700" width="14" height="120" rx="3" fill="#8a5a3a"/>'
s += '<rect x="0" y="724" width="470" height="12" fill="#9c6a45"/><rect x="0" y="770" width="470" height="12" fill="#9c6a45"/>'
s += ('<g transform="translate(330 760) rotate(-16)"><rect x="-6" y="-190" width="12" height="150" fill="#5a3a22"/><rect x="-11" y="-222" width="22" height="36" rx="4" fill="#3b2616"/>'
      '<circle cy="-20" r="40" fill="#d9a05b"/><circle cy="34" r="52" fill="#d9a05b"/><circle cy="-4" r="14" fill="#3b2616"/>'
      '<rect x="-20" y="48" width="40" height="8" rx="2" fill="#3b2616"/>'
      + "".join(f'<line x1="{f(-4+i*2.6)}" y1="-210" x2="{f(-4+i*2.6)}" y2="52" stroke="#f3e6c8" stroke-width=".8"/>' for i in range(4)) + '</g>')
# flores silvestres
for _ in range(70):
    x = rng.uniform(0, W); y = rng.uniform(800, 890)
    if 470 < x < 1130 and rng.random() < .6: continue
    c = rng.choice(["#fff","#f8c8dc","#ffe066","#f4a6c1"])
    s += f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x)}" y2="{f(y+14)}" stroke="#3f7a4a" stroke-width="1.5"/><circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(3,6))}" fill="{c}"/>'
s += butterfly(180, 420, 1, "#f8c8dc", "#f4a6c1", -12) + butterfly(1230, 300, .8, "#fff1a8", "#ffe066", 14) + butterfly(260, 260, .7, "#bfe8ff", "#9fd8ff", 8)
scenes["debut"] = svg(s, defs)

# ---------------------------------------------------------------- Fearless
rng = random.Random(2)
defs = (lin("fsBg", [(0,"#2e1d05"),(.5,"#7a561a"),(1,"#c99a3f")]) + lin("fsCurt", [(0,"#e6be62"),(.5,"#b88a2c"),(1,"#8a6419")], False)
        + rad("fsBulb", [(0,"#fff6d8",1),(.5,"#ffd98a",.6),(1,"#ffd98a",0)]))
s = f'<rect width="{W}" height="{H}" fill="url(#fsBg)"/>'
for x, sp in [(480, 1), (800, 1.2), (1120, 1)]:
    s += f'<path d="M{x-30} 0 L{x+30} 0 L{x+260*sp} 900 L{x-260*sp} 900Z" fill="#fff3cf" opacity=".09"/>'
for side in (0, 1):
    for i in range(6):
        x0 = i * 58
        path = f'M{x0} 0 Q{x0+40} 300 {x0+10+i*6} 560 Q{x0+30} 760 {x0+18} 900 H{x0+58} Q{x0+70} 760 {x0+60+i*6} 560 Q{x0+90} 300 {x0+58} 0Z'
        tr = f'transform="translate({W} 0) scale(-1 1)"' if side else ""
        s += f'<path {tr} d="{path}" fill="url(#fsCurt)" stroke="#6b4a10" stroke-width="1" opacity=".96"/>'
val = "M0 0 H1600 V70 " + " ".join(f"Q{1600-i*80-40} 120 {1600-(i+1)*80} 70" for i in range(20)) + "Z"
s += f'<path d="{val}" fill="#9c7020"/><path d="M0 64 H1600" stroke="#f3d98b" stroke-width="3"/>'
s += '<rect x="0" y="800" width="1600" height="100" fill="#3a2508"/>'
for x in range(40, 1600, 90):
    s += f'<circle cx="{x}" cy="806" r="26" fill="url(#fsBulb)"/><circle cx="{x}" cy="806" r="5" fill="#fff6d8"/>'
for i in range(60):
    x = i * 27 + rng.uniform(-6, 6); y = 868 + rng.uniform(-6, 8)
    s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(11,15))}" fill="#1b1204"/><rect x="{f(x-16)}" y="{f(y+8)}" width="32" height="30" rx="12" fill="#1b1204"/>'
    if rng.random() < .15:
        s += f'<line x1="{f(x+8)}" y1="{f(y+6)}" x2="{f(x+18)}" y2="{f(y-34)}" stroke="#1b1204" stroke-width="6" stroke-linecap="round"/>'
for (x, y) in sides(rng, 26, 120, 760):
    s += star4(x, y, rng.uniform(5, 13), "#fff1b8", rng.uniform(.5, 1))
scenes["fearless"] = svg(s, defs)

# ---------------------------------------------------------------- Speak Now
rng = random.Random(3)
defs = lin("snBg", [(0,"#12061f"),(.55,"#3f1a5e"),(1,"#8c52b8")])
s = f'<rect width="{W}" height="{H}" fill="url(#snBg)"/>' + dots(rng, 140, 0, W, 0, 600, .8, 2, "#fff", .3, .9)
s += '<path d="M170 120 a60 60 0 1 0 60 80 a48 48 0 1 1 -60 -80Z" fill="#f6e7ff" opacity=".9"/>'
for (x, y, r, cols) in [(280,330,110,["#f7a6ff","#ffffff","#c77dff"]),(1330,190,95,["#ffd6a5","#ff9bd2","#fff"]),(1450,450,70,["#b8f2ff","#c77dff","#fff"]),(120,560,70,["#ffd6a5","#f7a6ff"]),(1240,600,55,["#fff","#ff9bd2"])]:
    s += firework(rng, x, y, r, cols)
s += '<path d="M0 820 Q400 760 800 800 T1600 780 V900 H0Z" fill="#1d0b30"/>'
c = "#2a1240"
castle = (f'<g fill="{c}"><rect x="1230" y="600" width="260" height="230"/><rect x="1200" y="540" width="60" height="290"/><rect x="1460" y="540" width="60" height="290"/>'
          f'<rect x="1320" y="480" width="80" height="350"/><path d="M1195 540 L1230 450 L1265 540Z M1455 540 L1490 450 L1525 540Z M1315 480 L1360 360 L1405 480Z"/>'
          + "".join(f'<rect x="{1230+i*26}" y="585" width="16" height="18"/>' for i in range(10)) + '</g>')
s += castle + '<g fill="#ffd98a">' + "".join(f'<rect x="{x}" y="{y}" width="12" height="18" rx="6"/>' for x,y in [(1224,600),(1484,600),(1354,540),(1354,620),(1280,680),(1420,680)]) + '</g>'
s += '<path d="M1360 360 V330 L1386 338 L1360 346" fill="#f7a6ff" stroke="#f7a6ff" stroke-width="2"/>'
for (x, y) in sides(rng, 20, 80, 760):
    s += star4(x, y, rng.uniform(4, 10), "#f7d6ff", rng.uniform(.5, 1))
scenes["speaknow"] = svg(s, defs)

# ---------------------------------------------------------------- Red
rng = random.Random(4)
defs = (lin("rdBg", [(0,"#3b070b"),(.6,"#8e1b20"),(1,"#c0392b")])
        + '<pattern id="rdPlaid" width="68" height="68" patternUnits="userSpaceOnUse"><rect width="68" height="68" fill="none"/>'
          '<rect y="0" width="68" height="8" fill="#000" opacity=".25"/><rect x="0" width="8" height="68" fill="#000" opacity=".25"/>'
          '<rect y="34" width="68" height="3" fill="#fff" opacity=".08"/><rect x="34" width="3" height="68" fill="#fff" opacity=".08"/></pattern>'
        + rad("rdLamp", [(0,"#ffe3a3",.9),(.5,"#ffc46b",.35),(1,"#ffc46b",0)]))
s = f'<rect width="{W}" height="{H}" fill="url(#rdBg)"/><rect width="{W}" height="{H}" fill="url(#rdPlaid)"/>'
s += '<path d="M200 840 C210 720 180 600 214 470 L252 470 C270 600 250 720 262 840Z" fill="#2b1209"/><path d="M234 560 L150 470 M238 520 L330 430" stroke="#2b1209" stroke-width="14" stroke-linecap="round"/>'
for _ in range(34):
    s += f'<circle cx="{f(rng.uniform(80,380))}" cy="{f(rng.uniform(300,520))}" r="{f(rng.uniform(34,60))}" fill="{rng.choice(["#d9480f","#e8590c","#c92a2a","#f08c00","#a61e1e"])}" opacity=".95"/>'
s += '<rect x="0" y="830" width="1600" height="70" fill="#2b0a0c"/>'
s += '<rect x="1372" y="300" width="16" height="540" fill="#1b1414"/><path d="M1350 300 H1410 L1398 250 H1362Z" fill="#1b1414"/><circle cx="1380" cy="286" r="140" fill="url(#rdLamp)"/><circle cx="1380" cy="286" r="14" fill="#fff1c9"/>'
s += ('<path d="M1360 420 Q1380 400 1400 420 L1398 440 Q1380 424 1362 440Z" fill="#d62828"/>'
      '<path d="M1396 428 C1450 420 1500 450 1560 430 L1566 452 C1506 474 1452 446 1398 452Z" fill="#d62828"/>'
      '<path d="M1520 436 v16 M1530 434 v16 M1540 434 v16 M1550 432 v16" stroke="#8e1b20" stroke-width="3"/>'
      '<path d="M1566 440 l14 -4 M1566 446 l16 2 M1566 452 l14 6" stroke="#d62828" stroke-width="2"/>')
for _ in range(60):
    x, y = rng.choice([(rng.uniform(0,440), rng.uniform(80,880)), (rng.uniform(1160,1600), rng.uniform(80,880))])
    s += f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="9" ry="5" transform="rotate({rng.randint(0,180)} {f(x)} {f(y)})" fill="{rng.choice(["#f08c00","#e8590c","#ffb347","#c92a2a"])}" opacity=".9"/>'
scenes["red"] = svg(s, defs)

# ---------------------------------------------------------------- 1989
rng = random.Random(5)
defs = lin("nnBg", [(0,"#6fb6e6"),(.7,"#cfe9fb"),(1,"#f4fbff")]) + lin("nnPic", [(0,"#7fc0ea"),(.6,"#bfe3f7"),(.6,"#e9d6b0"),(1,"#d9c092")])
s = f'<rect width="{W}" height="{H}" fill="url(#nnBg)"/><circle cx="1480" cy="120" r="70" fill="#fff8d6" opacity=".9"/>'
for layer, col, hmin, hmax in [(0, "#a9cdea", 120, 300), (1, "#6f9cc4", 80, 230)]:
    x = -20
    while x < W:
        w = rng.uniform(40, 90); h = rng.uniform(hmin, hmax)
        s += f'<rect x="{f(x)}" y="{f(900-h)}" width="{f(w)}" height="{f(h)}" fill="{col}"/>'
        if layer:
            for wy in range(int(900-h+12), 890, 16):
                for wx in range(int(x+6), int(x+w-6), 12):
                    if rng.random() < .35: s += f'<rect x="{wx}" y="{wy}" width="5" height="7" fill="#e9f6ff" opacity=".7"/>'
        x += w + rng.uniform(2, 10)
s += ('<g fill="#5a88b3"><rect x="250" y="560" width="110" height="340"/><rect x="265" y="500" width="80" height="60"/><rect x="280" y="440" width="50" height="60"/>'
      '<rect x="292" y="380" width="26" height="60"/><rect x="302" y="300" width="6" height="80"/></g>')
for (x, y, rot) in [(90,150,-8),(250,420,6),(1330,170,7),(1220,440,-5)]:
    s += (f'<g transform="rotate({rot} {x+80} {y+95})"><rect x="{x+6}" y="{y+8}" width="160" height="190" fill="#000" opacity=".12"/>'
          f'<rect x="{x}" y="{y}" width="160" height="190" fill="#fffdf7"/><rect x="{x+12}" y="{y+12}" width="136" height="130" fill="url(#nnPic)"/>'
          f'<circle cx="{x+110}" cy="{y+44}" r="14" fill="#fff8d6"/>' + gull(x+30, y+60, .8, "#33506b") + gull(x+64, y+44, .6, "#33506b") + '</g>')
for (x, y) in sides(rng, 14, 60, 560):
    s += gull(x, y, rng.uniform(.8, 1.6), "#2e4a66")
scenes["1989"] = svg(s, defs)

# ---------------------------------------------------------------- reputation
rng = random.Random(6)
defs = lin("rpBg", [(0,"#050505"),(1,"#222")])
s = f'<rect width="{W}" height="{H}" fill="url(#rpBg)"/>'
for _ in range(90):
    x = rng.uniform(0, W)
    s += f'<line x1="{f(x)}" y1="0" x2="{f(x-30)}" y2="900" stroke="#fff" stroke-width=".6" opacity="{f(rng.uniform(.03,.1))}"/>'
for (x, y, rot) in [(40,60,-8),(220,300,5),(1260,80,7),(1330,380,-6),(1180,620,4)]:
    g = f'<g transform="rotate({rot} {x+140} {y+170})"><rect x="{x}" y="{y}" width="280" height="340" fill="#d7d7d2"/>'
    g += f'<rect x="{x+16}" y="{y+16}" width="248" height="26" fill="#1a1a1a"/><rect x="{x+16}" y="{y+50}" width="248" height="4" fill="#1a1a1a"/>'
    for col in range(3):
        for ln in range(22):
            w = 72 if rng.random() > .12 else rng.uniform(30, 60)
            g += f'<rect x="{x+16+col*84}" y="{y+66+ln*12}" width="{f(w)}" height="4" fill="#555"/>'
    g += f'<rect x="{x+100}" y="{y+120}" width="80" height="70" fill="#222"/></g>'
    s += g
body = "M-40 880 C80 760 300 900 250 780 S40 690 150 610 S300 560 240 480 S120 400 200 330"
s += f'<path d="{body}" fill="none" stroke="#111" stroke-width="46" stroke-linecap="round"/>'
s += f'<path d="{body}" fill="none" stroke="#2e3a2e" stroke-width="38" stroke-linecap="round"/>'
s += f'<path d="{body}" fill="none" stroke="#56705a" stroke-width="30" stroke-dasharray="3 9" stroke-linecap="round" opacity=".7"/>'
s += ('<g transform="translate(200 330) rotate(-40)"><ellipse rx="40" ry="28" fill="#2e3a2e" stroke="#111" stroke-width="4"/>'
      '<ellipse cx="10" cy="-12" rx="6" ry="4" fill="#b9ff6b"/><ellipse cx="10" cy="12" rx="6" ry="4" fill="#b9ff6b"/>'
      '<ellipse cx="11" cy="-12" rx="1.5" ry="3.5" fill="#111"/><ellipse cx="11" cy="12" rx="1.5" ry="3.5" fill="#111"/>'
      '<path d="M38 0 L66 0 L76 -8 M66 0 L76 8" stroke="#d22" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
scenes["reputation"] = svg(s, defs)

# ---------------------------------------------------------------- Lover
rng = random.Random(7)
defs = lin("lvBg", [(0,"#f6aecb"),(.4,"#d6c0f4"),(.75,"#b3dbf7"),(1,"#fbe3a1")], False)
s = f'<rect width="{W}" height="{H}" fill="url(#lvBg)"/>'
for i, col in enumerate(["#ff9aa2","#ffc48c","#fff3a0","#b8f2c8","#a0d8ff","#c9b6ff"]):
    r = 330 - i * 22
    s += f'<path d="M{-40} 700 A{r} {r} 0 0 1 {-40+2*r} 700" fill="none" stroke="{col}" stroke-width="22" opacity=".8" transform="translate({-r+230} 0)"/>'
for (x, y, sc, col) in [(80,160,1.1,"#fff"),(1250,120,1.3,"#fff"),(1330,520,.9,"#ffe4f1"),(140,560,.8,"#fff4fb"),(1180,330,.7,"#fff")]:
    s += cloud(x, y, sc, col)
s += '<path d="M1440 250 C1440 210 1390 200 1380 240 C1370 200 1320 210 1320 250 C1320 300 1380 320 1380 350 C1380 320 1440 300 1440 250Z" fill="#ffd1e6" opacity=".95"/>'
s += ('<g transform="translate(1250 640)"><rect x="0" y="80" width="220" height="170" fill="#f7b6d2"/><path d="M-20 90 L110 0 L240 90Z" fill="#b69cf0"/>'
      '<rect x="90" y="160" width="46" height="90" rx="6" fill="#ffe7a8"/><path d="M50 140 C50 124 32 122 30 136 C28 122 10 124 10 140 C10 156 30 164 30 172 C30 164 50 156 50 140Z" fill="#fff"/>'
      '<path d="M200 140 C200 124 182 122 180 136 C178 122 160 124 160 140 C160 156 180 164 180 172 C180 164 200 156 200 140Z" fill="#fff"/>'
      '<rect x="150" y="20" width="26" height="50" fill="#b69cf0"/></g>')
s += '<path d="M0 860 Q400 820 800 860 T1600 850 V900 H0Z" fill="#c8f0d2"/>'
for (x, y, sc, a, b, r) in [(330,300,1,"#c9b6ff","#f7a6c8",-10),(1180,560,.9,"#a0d8ff","#c9b6ff",12),(230,720,.8,"#fff3a0","#ffc48c",4),(1500,420,.7,"#f7a6c8","#ffb3d9",-8)]:
    s += butterfly(x, y, sc, a, b, r)
for (x, y) in sides(rng, 16, 60, 820):
    s += star4(x, y, rng.uniform(4, 9), "#fff", rng.uniform(.6, 1))
scenes["lover"] = svg(s, defs)

# ---------------------------------------------------------------- folklore
rng = random.Random(8)
defs = (lin("fkBg", [(0,"#3a4038"),(.45,"#8a9185"),(1,"#d5d8cf")])
        + lin("fkFog", [(0,"#e9ebe4"),(1,"#e9ebe4")]) + rad("fkWin", [(0,"#ffd479",1),(1,"#ffd479",0)]))
s = f'<rect width="{W}" height="{H}" fill="url(#fkBg)"/><circle cx="1300" cy="140" r="46" fill="#eef0ea" opacity=".55"/>'
for layer, (col, hmin, hmax, base, fog) in enumerate([("#a3a99e",220,320,720,.35),("#737b6f",280,420,800,.3),("#434a41",360,520,900,0)]):
    x = -30
    while x < W + 40:
        if not (520 < x < 1080) or layer == 0:
            s += pine(x, base + rng.uniform(-10, 10), rng.uniform(hmin, hmax), col)
        x += rng.uniform(40, 80) if layer < 2 else rng.uniform(70, 120)
    if fog:
        s += f'<rect x="0" y="{base-160}" width="{W}" height="200" fill="#e9ebe4" opacity="{fog}"/>'
s += ('<g transform="translate(50 700)"><rect x="0" y="40" width="170" height="110" fill="#3a3129"/><path d="M-16 48 L85 -20 L186 48Z" fill="#2c2520"/>'
      '<rect x="120" y="-18" width="20" height="50" fill="#2c2520"/><circle cx="54" cy="84" r="60" fill="url(#fkWin)" opacity=".6"/>'
      '<rect x="36" y="68" width="36" height="32" fill="#ffd479"/><path d="M54 68 V100 M36 84 H72" stroke="#3a3129" stroke-width="3"/>'
      '<path d="M130 -24 C110 -60 160 -80 136 -120 C120 -150 160 -170 150 -200" fill="none" stroke="#e9ebe4" stroke-width="10" stroke-linecap="round" opacity=".45"/></g>')
scenes["folklore"] = svg(s, defs)

# ---------------------------------------------------------------- evermore
rng = random.Random(9)
defs = lin("evBg", [(0,"#2f1a0d"),(.55,"#a0572a"),(1,"#e9ad6a")]) + rad("evWin", [(0,"#ffcf7a",1),(1,"#ffcf7a",0)])
s = f'<rect width="{W}" height="{H}" fill="url(#evBg)"/>'
for (x, y, l) in [(110,860,150),(330,880,120),(1300,870,160),(1500,860,130),(1180,880,100)]:
    s += bare_tree(rng, x, y, l, 90 + rng.uniform(-4, 4), 6, 16, "#24130a")
s += '<path d="M0 800 Q300 760 620 800 T1200 790 T1600 800 V900 H0Z" fill="#f3ebe0"/><path d="M0 850 Q400 820 800 850 T1600 845 V900 H0Z" fill="#fffaf2"/>'
s += ('<g transform="translate(1330 690)"><rect x="0" y="40" width="160" height="100" fill="#4a2a18"/><path d="M-18 48 L80 -16 L178 48Z" fill="#f3ebe0"/>'
      '<circle cx="50" cy="84" r="54" fill="url(#evWin)" opacity=".6"/><rect x="34" y="68" width="34" height="30" fill="#ffcf7a"/>'
      '<path d="M51 68 V98 M34 83 H68" stroke="#4a2a18" stroke-width="3"/><rect x="112" y="-14" width="18" height="44" fill="#3a2012"/>'
      '<path d="M121 -20 C100 -56 150 -76 126 -116 C112 -146 150 -166 140 -196" fill="none" stroke="#f3ebe0" stroke-width="10" stroke-linecap="round" opacity=".45"/></g>')
s += dots(rng, 120, 0, W, 0, 860, 1.2, 3.4, "#fffaf2", .5, .95)
scenes["evermore"] = svg(s, defs)

# ---------------------------------------------------------------- Midnights
rng = random.Random(10)
cx, cy = 1420, 330
defs = (lin("mnBg", [(0,"#0b0d29"),(.6,"#2a2463"),(1,"#5b4a9c")]) + rad("mnHaze", [(0,"#c8b6ff",.55),(1,"#c8b6ff",0)])
        + lin("mnWin", [(0,"#06071a"),(1,"#1b1a4a")]))
s = f'<rect width="{W}" height="{H}" fill="url(#mnBg)"/><ellipse cx="800" cy="900" rx="900" ry="300" fill="url(#mnHaze)"/>'
for _ in range(40):
    x, y = (rng.uniform(0, 460), rng.uniform(0, 900)) if rng.random() < .5 else (rng.uniform(1140, 1600), rng.uniform(0, 900))
    s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(8,26))}" fill="{rng.choice(["#b9a6ff","#ffb3e6","#9ec5ff"])}" opacity="{f(rng.uniform(.08,.22))}"/>'
s += '<rect x="70" y="130" width="360" height="520" rx="10" fill="#1d1846" stroke="#b9a6ff" stroke-width="3"/><rect x="92" y="152" width="316" height="476" fill="url(#mnWin)"/>'
s += dots(rng, 50, 96, 404, 156, 624, .8, 2.2, "#fff", .5, 1)
s += '<path d="M330 230 a40 40 0 1 0 40 54 a32 32 0 1 1 -40 -54Z" fill="#f4eeff"/>'
s += '<path d="M250 152 V628 M92 390 H408" stroke="#1d1846" stroke-width="12"/>'
s += '<path d="M60 120 C120 300 60 500 110 680 H40 V120Z M440 120 C380 300 440 500 390 680 H460 V120Z" fill="#3b2f7a" opacity=".85"/>'
s += f'<circle cx="{cx}" cy="{cy}" r="150" fill="#c8b6ff" opacity=".18"/><circle cx="{cx}" cy="{cy}" r="120" fill="#f2ecff" stroke="#b9a6ff" stroke-width="10"/>'
for i in range(12):
    a = math.radians(i * 30)
    r1, r2 = (92, 108) if i % 3 == 0 else (98, 108)
    s += f'<line x1="{f(cx+r1*math.sin(a))}" y1="{f(cy-r1*math.cos(a))}" x2="{f(cx+r2*math.sin(a))}" y2="{f(cy-r2*math.cos(a))}" stroke="#2a2463" stroke-width="{4 if i%3==0 else 2}" stroke-linecap="round"/>'
s += f'<line class="clock-hand hour" x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-60}" stroke="#2a2463" stroke-width="8" stroke-linecap="round"/>'
s += f'<line class="clock-hand minute" x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-92}" stroke="#2a2463" stroke-width="5" stroke-linecap="round"/>'
s += f'<circle cx="{cx}" cy="{cy}" r="8" fill="#b9a6ff"/>'
s += '<g fill="#12103a">' + "".join(f'<rect x="{x}" y="{900-h}" width="{w}" height="{h}"/>' for x,w,h in [(1140,70,160),(1215,50,220),(1270,90,140),(1365,60,250),(1430,80,180),(1515,90,120)]) + '</g>'
s += '<g fill="#ffd98a" opacity=".7">' + "".join(f'<rect x="{f(rng.uniform(1145,1595))}" y="{f(rng.uniform(700,890))}" width="5" height="7"/>' for _ in range(40)) + '</g>'
scenes["midnights"] = svg(s, defs)

# ---------------------------------------------------------------- The Tortured Poets Department
rng = random.Random(11)
defs = lin("tpBg", [(0,"#f3eee3"),(1,"#d6cdb9")])
s = f'<rect width="{W}" height="{H}" fill="url(#tpBg)"/>'
for (x, y, rot) in [(60,80,-10),(260,260,8),(1240,60,6),(1300,330,-7),(1160,560,5),(40,460,4)]:
    g = f'<g transform="rotate({rot} {x+120} {y+150})"><rect x="{x+5}" y="{y+6}" width="240" height="300" fill="#000" opacity=".08"/><rect x="{x}" y="{y}" width="240" height="300" fill="#fbf9f3"/>'
    for ln in range(14):
        yy = y + 40 + ln * 18; ww = rng.uniform(120, 200)
        g += f'<path d="M{x+20} {yy} ' + " ".join(f"q6 -{f(rng.uniform(2,5))} 12 0" for _ in range(int(ww/12))) + '" fill="none" stroke="#333" stroke-width="1.2" opacity=".55"/>'
    g += '</g>'
    s += g
tw = ('<g transform="translate(30 640)"><rect x="40" y="-120" width="220" height="150" fill="#fbf9f3" stroke="#bbb"/>'
      + "".join(f'<rect x="60" y="{-100+i*18}" width="{rng.randint(90,170)}" height="3" fill="#333" opacity=".6"/>' for i in range(6))
      + '<rect x="0" y="20" width="300" height="30" rx="10" fill="#2a2a2a"/><path d="M-10 50 H310 L340 200 H-40Z" fill="#1c1c1c"/>')
for row in range(4):
    for k in range(10 - row):
        tw += f'<circle cx="{f(10 + row*14 + k*30)}" cy="{80+row*28}" r="10" fill="#e9e4d8" stroke="#555" stroke-width="2"/>'
tw += '<rect x="60" y="190" width="180" height="12" rx="6" fill="#e9e4d8"/></g>'
s += tw
s += ('<g transform="translate(1420 760) rotate(-40)"><rect x="-10" y="-260" width="20" height="200" rx="8" fill="#141414"/><rect x="-11" y="-120" width="22" height="10" fill="#c9b27a"/>'
      '<path d="M-10 -60 L10 -60 L0 -10Z" fill="#c9c9c9"/><line x1="0" y1="-56" x2="0" y2="-22" stroke="#555" stroke-width="1.5"/></g>')
for (x, y, r) in [(1400,790,26),(1440,815,12),(1370,820,9),(420,560,14),(1500,700,8)]:
    s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#141414"/>'
scenes["ttpd"] = svg(s, defs)

# ---------------------------------------------------------------- The Life of a Showgirl
rng = random.Random(12)
defs = (lin("sgBg", [(0,"#2a8c83"),(1,"#6fd3c5")]) + lin("sgCurt", [(0,"#ff9a4d"),(.5,"#f0701f"),(1,"#b8480f")], False)
        + rad("sgBulb", [(0,"#fff6d8",1),(.5,"#ffd98a",.6),(1,"#ffd98a",0)]))
s = f'<rect width="{W}" height="{H}" fill="url(#sgBg)"/>'
for i in range(36):
    a1 = math.radians(180 + i * 5); a2 = math.radians(180 + i * 5 + 2.5)
    s += f'<path d="M800 900 L{f(800+1400*math.cos(a1))} {f(900+1400*math.sin(a1))} L{f(800+1400*math.cos(a2))} {f(900+1400*math.sin(a2))}Z" fill="#fff" opacity=".08"/>'
s += dots(rng, 160, 0, W, 0, 900, .8, 2, "#fff", .3, .9)
for side in (0, 1):
    for i in range(6):
        x0 = i * 62
        path = f'M{x0} 0 Q{x0+44} 280 {x0+14+i*7} 540 Q{x0+34} 760 {x0+22} 900 H{x0+62} Q{x0+74} 760 {x0+64+i*7} 540 Q{x0+96} 280 {x0+62} 0Z'
        tr = f'transform="translate({W} 0) scale(-1 1)"' if side else ""
        s += f'<path {tr} d="{path}" fill="url(#sgCurt)" stroke="#8a3208" stroke-width="1"/>'
val = "M0 0 H1600 V90 " + " ".join(f"Q{1600-i*80-40} 150 {1600-(i+1)*80} 90" for i in range(20)) + "Z"
s += f'<path d="{val}" fill="#d95f14"/>' + "".join(f'<line x1="{x}" y1="{95+ (12 if (x//40)%2 else 0)}" x2="{x}" y2="{128+ (12 if (x//40)%2 else 0)}" stroke="#ffd98a" stroke-width="2"/>' for x in range(10, 1600, 20))
for x in range(30, 1600, 60):
    s += f'<circle cx="{x}" cy="30" r="20" fill="url(#sgBulb)"/><circle cx="{x}" cy="30" r="5" fill="#fff6d8"/>'
for (bx, flip) in [(130, 1), (1470, -1)]:
    g = f'<g transform="translate({bx} 900) scale({flip} 1)">'
    for i in range(9):
        a = -150 + i * 15
        g += f'<ellipse cx="0" cy="-110" rx="26" ry="110" transform="rotate({a+90})" fill="{["#ffe3c2","#ff9a4d","#fff6ea"][i%3]}" stroke="#d95f14" stroke-width="1.5"/>'
    s += g + '</g>'
scenes["showgirl"] = svg(s, defs)

# ---------------------------------------------------------------- datos de cada era
ERAS = [
    dict(id="debut", body="Patrick Hand", bodyFam="Patrick Hand", name="Taylor Swift", font="Dancing Script:wght@700", fam="Dancing Script",
         pal=dict(card="#f3faf8", ink="#1f3b38", muted="#4e6d69", line="#cfe5e0", accent="#2f8f85", soft="#d3efe9"),
         fx="chars", chars=["♪", "♫", "♬"], colors=["#2f8f85", "#1f5f59", "#f4a6c1"]),
    dict(id="fearless", body="Marcellus", bodyFam="Marcellus", name="Fearless", font="Cinzel:wght@600", fam="Cinzel",
         pal=dict(card="#fffaf0", ink="#3b2e12", muted="#7a6636", line="#eadcb4", accent="#b8892e", soft="#f6e7bd"),
         fx="chars", chars=["✦", "✧", "★"], colors=["#f3d98b", "#e0b04a", "#fff3c4"]),
    dict(id="speaknow", body="Dancing Script:wght@500;700", bodyFam="Dancing Script", name="Speak Now", font="Parisienne", fam="Parisienne",
         pal=dict(card="#faf5fd", ink="#2e1640", muted="#6b4f80", line="#e3d3ee", accent="#8c3fb8", soft="#eedcf8"),
         fx="firework", colors=["#f7a6ff", "#c77dff", "#ffd6a5", "#ffffff"]),
    dict(id="red", body="Oswald:wght@300;500", bodyFam="Oswald", name="Red", font="Oswald:wght@500", fam="Oswald",
         pal=dict(card="#fff7f5", ink="#3a0d10", muted="#7d3a3e", line="#f0d2d2", accent="#b3242a", soft="#f7d5d5"),
         fx="chars", chars=["🍂", "🍁"], colors=[]),
    dict(id="1989", body="Architects Daughter", bodyFam="Architects Daughter", name="1989", font="Permanent Marker", fam="Permanent Marker",
         pal=dict(card="#f7fbff", ink="#1b2c3d", muted="#516a82", line="#d6e6f3", accent="#3b8fd0", soft="#d9ecfa"),
         fx="camera"),
    dict(id="reputation", body="Grenze Gotisch:wght@400;600", bodyFam="Grenze Gotisch", name="reputation", font="UnifrakturMaguntia", fam="UnifrakturMaguntia",
         pal=dict(card="#141414", ink="#eeeeee", muted="#a3a3a3", line="#333333", accent="#b9c7b9", soft="#2a2a2a"),
         fx="chars", chars=["🐍", "🖤"], colors=[], snake=True),
    dict(id="lover", body="Fredoka:wght@400;600", bodyFam="Fredoka", name="Lover", font="Pacifico", fam="Pacifico",
         pal=dict(card="#fff8fc", ink="#3b2340", muted="#7d5d82", line="#f3d8ea", accent="#e56fa8", soft="#fbe0ee"),
         fx="chars", chars=["💗", "🦋", "💖"], colors=[]),
    dict(id="folklore", body="IM Fell English", bodyFam="IM Fell English", name="folklore", font="IM Fell English", fam="IM Fell English",
         pal=dict(card="#f2f1ec", ink="#2c302b", muted="#676d65", line="#d8d8d0", accent="#6f7d68", soft="#e1e5dc"),
         fx="fireflies"),
    dict(id="evermore", body="Cormorant Garamond:wght@500;700", bodyFam="Cormorant Garamond", name="evermore", font="Cormorant Garamond:wght@700", fam="Cormorant Garamond",
         pal=dict(card="#fbf4ec", ink="#3a2414", muted="#7c5a41", line="#ead9c6", accent="#b9692f", soft="#f3dcc6"),
         fx="chars", chars=["❄", "❅", "❆"], colors=["#ffffff", "#f3ebe0", "#dfe9f3"]),
    dict(id="midnights", body="Bodoni Moda:wght@400;600", bodyFam="Bodoni Moda", name="Midnights", font="Bodoni Moda:wght@600", fam="Bodoni Moda",
         pal=dict(card="#161836", ink="#eae6ff", muted="#aaa3d6", line="#2f2f5c", accent="#b9a6ff", soft="#2e2a5c"),
         fx="clock", chars=["✦", "✧"], colors=["#b9a6ff", "#ffb3e6", "#ffffff"]),
    dict(id="ttpd", body="Special Elite", bodyFam="Special Elite", name="The Tortured Poets Department", font="Special Elite", fam="Special Elite",
         pal=dict(card="#faf7f0", ink="#1c1c1c", muted="#5e5a52", line="#e0dbcf", accent="#1c1c1c", soft="#e8e3d6"),
         fx="words", words=["poema", "tinta", "musa", "verso", "querida", "pluma", "capítulo", "borrador", "manuscrito"]),
    dict(id="showgirl", body="Josefin Sans:wght@400;600", bodyFam="Josefin Sans", name="The Life of a Showgirl", font="Limelight", fam="Limelight",
         pal=dict(card="#fff6ee", ink="#3a1f0e", muted="#8a5a3c", line="#f5d9c3", accent="#e8661c", soft="#fde0cc"),
         fx="confetti", colors=["#f0701f", "#3fb3a7", "#ffd98a", "#ffffff", "#ff9a4d"]),
]
for e in ERAS:
    e["scene"] = scenes[e["id"]]

JS = r"""/* Easter egg: escribir "taylor" cambia la página a una era de Taylor Swift.
   Cada era trae una escena ilustrada de fondo, recolorea la hoja, cambia la tipografía
   de los títulos y tiene un detalle al tocar el fondo. Esc regresa a la normalidad.
   Archivo generado por tools/gen_eras.py: para cambiar algo, edita ese script y vuelve a correrlo. */
(function () {
    var ERAS = __ERAS__;
    var root = document.documentElement;
    var page = document.querySelector(".page");
    if (!page) return;
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var layer = document.createElement("div");
    layer.className = "era-bg";
    layer.setAttribute("aria-hidden", "true");
    document.body.insertBefore(layer, page);
    var fxLayer = document.createElement("div");
    fxLayer.className = "era-fx";
    fxLayer.setAttribute("aria-hidden", "true");
    document.body.appendChild(fxLayer);
    var chip = document.createElement("div");
    chip.className = "era-chip";
    chip.setAttribute("role", "status");
    document.body.appendChild(chip);

    var current = null, chipTimer = null, loadedFonts = {};
    var VARS = { card: "--card", ink: "--ink", muted: "--muted", line: "--line", accent: "--accent", soft: "--accent-soft" };

    function loadFont(era) {
        if (loadedFonts[era.id]) return;
        loadedFonts[era.id] = true;
        var families = [era.font, era.body].filter(function (x, i, a) { return a.indexOf(x) === i; });
        var link = document.createElement("link");
        link.rel = "stylesheet";
        link.href = "https://fonts.googleapis.com/css2?" + families.map(function (f) {
            return "family=" + f.replace(/ /g, "+");
        }).join("&") + "&display=swap";
        document.head.appendChild(link);
    }

    function setEra(era) {
        if (era && window.__disney) window.__disney(false);   // una era apaga el modo Disney
        if (era && window.__vangogh) window.__vangogh(false);
        if (era && window.__sonora) window.__sonora(false);
        stopSnake();
        current = era;
        Object.keys(VARS).forEach(function (k) {
            if (era) root.style.setProperty(VARS[k], era.pal[k]); else root.style.removeProperty(VARS[k]);
        });
        if (!era) {
            root.style.removeProperty("--font-head");
            root.style.removeProperty("--font-body");
            root.classList.remove("era");
            root.removeAttribute("data-era");
            layer.innerHTML = "";
            return;
        }
        loadFont(era);
        root.style.setProperty("--font-head", '"' + era.fam + '", Georgia, serif');
        root.style.setProperty("--font-body", '"' + era.bodyFam + '", system-ui, sans-serif');
        root.classList.add("era");
        root.setAttribute("data-era", era.id);
        layer.classList.remove("show");
        layer.innerHTML = era.scene;
        void layer.offsetWidth;
        layer.classList.add("show");
        if (era.snake) startSnake();
        chip.textContent = "✨ Era: " + era.name + " ✨";
        chip.classList.add("on");
        clearTimeout(chipTimer);
        chipTimer = setTimeout(function () { chip.classList.remove("on"); }, 3500);
    }

    // ---------- efectos al tocar el fondo ----------
    function particle(html, x, y, cls) {
        var el = document.createElement("span");
        el.className = "era-part " + (cls || "");
        el.innerHTML = html;
        el.style.left = x + "px";
        el.style.top = y + "px";
        fxLayer.appendChild(el);
        return el;
    }
    function fly(el, frames, ms) {
        var a = el.animate(frames, { duration: ms, easing: "cubic-bezier(.2,.7,.4,1)", fill: "forwards" });
        a.onfinish = function () { el.remove(); };
    }
    function burstChars(era, x, y) {
        for (var i = 0; i < 14; i++) {
            var el = particle(era.chars[i % era.chars.length], x, y);
            if (era.colors.length) el.style.color = era.colors[i % era.colors.length];
            el.style.fontSize = (16 + Math.random() * 18) + "px";
            var a = Math.random() * Math.PI * 2, d = 50 + Math.random() * 110;
            var dx = Math.cos(a) * d, dy = Math.sin(a) * d - 40, fall = 120 + Math.random() * 160;
            fly(el, [
                { transform: "translate(-50%,-50%) scale(.4)", opacity: 1 },
                { transform: "translate(calc(-50% + " + dx + "px), calc(-50% + " + dy + "px)) rotate(" + (Math.random() * 180 - 90) + "deg)", opacity: 1, offset: .35 },
                { transform: "translate(calc(-50% + " + dx * 1.3 + "px), calc(-50% + " + (dy + fall) + "px)) rotate(" + (Math.random() * 360 - 180) + "deg)", opacity: 0 }
            ], 1600 + Math.random() * 900);
        }
    }
    function firework(era, x, y) {
        for (var i = 0; i < 28; i++) {
            var el = particle("", x, y, "dot");
            el.style.background = era.colors[i % era.colors.length];
            el.style.boxShadow = "0 0 8px " + era.colors[i % era.colors.length];
            var a = i * Math.PI * 2 / 28, d = 90 + Math.random() * 40;
            fly(el, [
                { transform: "translate(-50%,-50%)", opacity: 1 },
                { transform: "translate(calc(-50% + " + Math.cos(a) * d + "px), calc(-50% + " + Math.sin(a) * d + "px))", opacity: 1, offset: .55 },
                { transform: "translate(calc(-50% + " + Math.cos(a) * d * 1.1 + "px), calc(-50% + " + (Math.sin(a) * d + 60) + "px))", opacity: 0 }
            ], 1400);
        }
    }
    function fireflies(x, y) {
        for (var i = 0; i < 12; i++) {
            var el = particle("", x, y, "firefly");
            var dx = (Math.random() * 2 - 1) * 160, dy = -80 - Math.random() * 200;
            fly(el, [
                { transform: "translate(-50%,-50%)", opacity: 0 },
                { transform: "translate(calc(-50% + " + dx * .4 + "px), calc(-50% + " + dy * .3 + "px))", opacity: 1, offset: .25 },
                { transform: "translate(calc(-50% + " + dx * .7 + "px), calc(-50% + " + dy * .7 + "px))", opacity: .3, offset: .6 },
                { transform: "translate(calc(-50% + " + dx + "px), calc(-50% + " + dy + "px))", opacity: 0 }
            ], 2600 + Math.random() * 1400);
        }
    }
    function camera(x, y) {
        var flash = particle("", 0, 0, "flash");
        fly(flash, [{ opacity: .9 }, { opacity: 0 }], 500);
        for (var i = 0; i < 4; i++) {
            var el = particle('<svg viewBox="0 0 40 16" width="' + (30 + i * 6) + '"><path d="M2 12 q9 -10 18 0 q9 -10 18 0" fill="none" stroke="#2e4a66" stroke-width="3" stroke-linecap="round"/></svg>', x, y);
            var dx = 200 + Math.random() * 260, dy = -180 - Math.random() * 200;
            fly(el, [
                { transform: "translate(-50%,-50%) scaleY(1)" },
                { transform: "translate(calc(-50% + " + dx * .5 + "px), calc(-50% + " + dy * .5 + "px)) scaleY(-1)", offset: .5 },
                { transform: "translate(calc(-50% + " + dx + "px), calc(-50% + " + dy + "px)) scaleY(1)", opacity: 0 }
            ], 2200 + i * 200);
        }
    }
    function clockStrike(era, x, y) {
        if (root.classList.contains("midnight")) return;
        root.classList.add("midnight");
        setTimeout(function () { burstChars(era, x, y); }, 900);
        setTimeout(function () { root.classList.remove("midnight"); }, 4500);
    }
    function typeWord(era, x, y) {
        var word = era.words[Math.floor(Math.random() * era.words.length)];
        var el = particle("", x, y, "typed");
        var i = 0;
        var iv = setInterval(function () {
            el.textContent = word.slice(0, ++i);
            if (i >= word.length) {
                clearInterval(iv);
                fly(el, [{ opacity: 1, transform: "translate(-50%,-50%)" }, { opacity: 1, offset: .6 }, { opacity: 0, transform: "translate(-50%,-80%)" }], 1800);
            }
        }, 110);
    }
    function confetti(era, x, y) {
        for (var i = 0; i < 26; i++) {
            var feather = i % 6 === 0;
            var el = particle(feather ? "🪶" : "", x, y, feather ? "" : "confetti");
            if (!feather) el.style.background = era.colors[i % era.colors.length];
            var a = -Math.PI / 2 + (Math.random() - .5) * 2.2, d = 120 + Math.random() * 160;
            var dx = Math.cos(a) * d, dy = Math.sin(a) * d;
            fly(el, [
                { transform: "translate(-50%,-50%) rotate(0deg)", opacity: 1 },
                { transform: "translate(calc(-50% + " + dx + "px), calc(-50% + " + dy + "px)) rotate(" + (Math.random() * 720) + "deg)", opacity: 1, offset: .4 },
                { transform: "translate(calc(-50% + " + dx * 1.2 + "px), calc(-50% + " + (dy + 300) + "px)) rotate(" + (Math.random() * 1080) + "deg)", opacity: 0 }
            ], 2200 + Math.random() * 800);
        }
    }

    layer.addEventListener("click", function (e) {
        if (!current || reduce) return;
        var x = e.clientX, y = e.clientY;
        switch (current.fx) {
            case "chars": burstChars(current, x, y); break;
            case "firework": firework(current, x, y); break;
            case "fireflies": fireflies(x, y); break;
            case "camera": camera(x, y); break;
            case "clock": clockStrike(current, x, y); break;
            case "words": typeWord(current, x, y); break;
            case "confetti": confetti(current, x, y); break;
        }
    });

    // ---------- reputation: una serpiente que sigue al mouse ----------
    var snake = null, snakeRaf = null, mouse = { x: -100, y: -100 };
    function onMove(e) { mouse.x = e.clientX; mouse.y = e.clientY; }
    function startSnake() {
        if (reduce || !window.matchMedia("(hover: hover)").matches) return;
        snake = [];
        for (var i = 0; i < 18; i++) {
            var seg = document.createElement("span");
            seg.className = "snake-seg" + (i === 0 ? " head" : "");
            var size = i === 0 ? 20 : Math.max(6, 16 - i * .55);
            seg.style.width = seg.style.height = size + "px";
            fxLayer.appendChild(seg);
            snake.push({ el: seg, x: mouse.x, y: mouse.y });
        }
        document.addEventListener("mousemove", onMove);
        (function tick() {
            var tx = mouse.x, ty = mouse.y;
            snake.forEach(function (s, i) {
                var k = i === 0 ? .25 : .45;
                s.x += (tx - s.x) * k; s.y += (ty - s.y) * k;
                s.el.style.transform = "translate(" + s.x + "px," + s.y + "px) translate(-50%,-50%)";
                tx = s.x; ty = s.y;
            });
            snakeRaf = requestAnimationFrame(tick);
        })();
    }
    function stopSnake() {
        if (!snake) return;
        cancelAnimationFrame(snakeRaf);
        document.removeEventListener("mousemove", onMove);
        snake.forEach(function (s) { s.el.remove(); });
        snake = null;
    }

    var typed = "";
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && current) { setEra(null); return; }
        if (e.key.length !== 1) return;
        typed = (typed + e.key.toLowerCase()).slice(-6);
        if (typed !== "taylor") return;
        var options = ERAS.filter(function (x) { return x !== current; });
        setEra(options[Math.floor(Math.random() * options.length)]);
    });
    window.__setEra = function (id) { setEra(ERAS.filter(function (x) { return x.id === id; })[0] || null); };
    // index.html descarga este archivo la primera vez que alguien escribe "taylor"
    if (window.__erasWant) window.__setEra(window.__erasWant);
    else if (window.__erasPending) setEra(ERAS[Math.floor(Math.random() * ERAS.length)]);
})();
"""
with open(OUT_JS, "w") as fh:
    fh.write(JS.replace("__ERAS__", json.dumps(ERAS, ensure_ascii=False, indent=1)))
print("eras.js:", round(len(open(OUT_JS).read())/1024), "KB")
