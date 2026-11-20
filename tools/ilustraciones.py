#!/usr/bin/env python3
"""Genera las ilustraciones SVG de la web (castellano y valenciano) en assets/images/{es,val}/.
Uso: python3 tools/ilustraciones.py
Cada ilustración es una función que recibe T (textos del idioma) y devuelve el SVG."""
import pathlib
from html import escape

RAIZ = pathlib.Path(__file__).resolve().parent.parent
# Paleta
IND, TEA, AMB, COR, SKY, PUR, GRE = '#5B3FBF', '#14A38B', '#F2A93B', '#E5645A', '#3B82F6', '#9B5DE5', '#2E9E5B'
INK, MUT, BG, PAPER = '#1F2340', '#5B6078', '#F6F4FD', '#FFFFFF'
FONT = "Inter, 'Segoe UI', system-ui, -apple-system, sans-serif"


def svg(w, h, body, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(titulo)}" font-family="{FONT}">\n<title>{escape(titulo)}</title>\n'
            f'<defs><filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1F2340" flood-opacity=".14"/></filter>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{MUT}"/></marker></defs>\n'
            f'<rect width="{w}" height="{h}" rx="22" fill="{BG}"/>\n{body}\n</svg>\n')


def tx(x, y, s, size=16, w=400, c=INK, a='middle', lh=1.25, style=''):
    lines = s.split('\n') if isinstance(s, str) else s
    out = f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="{a}"{style}>'
    for i, l in enumerate(lines):
        out += f'<tspan x="{x}" dy="{0 if i == 0 else size * lh:.1f}">{escape(l)}</tspan>'
    return out + '</text>'


def card(x, y, w, h, fill=PAPER, r=16, stroke=None, sh=True):
    st = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}{" filter=\"url(#sh)\"" if sh else ""}/>'


def head(w, t, sub=None):
    s = tx(w / 2, 52, t, 30, 800)
    if sub:
        s += tx(w / 2, 82, sub, 16, 400, MUT)
    return s


def person(x, y, c=IND, s=1.0, skin='#F5C9A8'):
    return (f'<g transform="translate({x},{y}) scale({s})"><circle cx="0" cy="-34" r="14" fill="{skin}"/>'
            f'<path d="M-20 0 Q-20 -18 0 -18 Q20 -18 20 0 L20 14 L-20 14 Z" fill="{c}"/></g>')


# ---------- iconos (centrados en 0,0, ~60px) ----------
def ic_bulb(c):
    return (f'<circle cx="0" cy="-8" r="20" fill="{c}"/><rect x="-9" y="12" width="18" height="12" rx="3" fill="{MUT}"/>'
            f'<path d="M-7 -8 L-2 2 L2 -6 L7 2" stroke="#fff" stroke-width="3" fill="none"/>')


def ic_flag(c):
    return (f'<path d="M-28 24 L-6 -14 L4 2 L12 -8 L30 24 Z" fill="{c}" opacity=".85"/>'
            f'<line x1="-6" y1="-14" x2="-6" y2="-30" stroke="{INK}" stroke-width="3"/><path d="M-6 -30 L10 -25 L-6 -20Z" fill="{COR}"/>')


def ic_flip(c):
    return (f'<path d="M-30 -2 L-16 -16 L-2 -2 V16 H-30Z" fill="{c}"/><rect x="4" y="-14" width="28" height="22" rx="3" fill="{INK}"/>'
            f'<rect x="8" y="-10" width="20" height="14" fill="#9FE3D5"/><path d="M-12 22 Q4 34 18 14" stroke="{MUT}" stroke-width="3" fill="none" marker-end="url(#ar)"/>')


def ic_team(c):
    return person(-18, 22, c, .7) + person(18, 22, TEA, .7) + person(0, 16, AMB, .8)


def ic_game(c):
    return (f'<rect x="-30" y="-14" width="60" height="30" rx="15" fill="{c}"/><rect x="-20" y="-2" width="12" height="4" fill="#fff"/>'
            f'<rect x="-16" y="-6" width="4" height="12" fill="#fff"/><circle cx="12" cy="-2" r="4" fill="{AMB}"/><circle cx="20" cy="4" r="4" fill="{COR}"/>'
            f'<path d="M-8 -30 h16 v8 a8 8 0 0 1 -16 0z" fill="{AMB}"/>')


def ic_board(c):
    s = f'<rect x="-32" y="-26" width="64" height="48" rx="4" fill="#fff" stroke="{c}" stroke-width="3"/>'
    for i, xx in enumerate((-30, -9, 12)):
        s += f'<line x1="{xx + 19}" y1="-26" x2="{xx + 19}" y2="22" stroke="{c}" stroke-width="1.5"/>' if i < 2 else ''
    for xx, yy, col in ((-27, -20, AMB), (-27, -6, AMB), (-6, -20, SKY), (15, -20, GRE), (15, -6, GRE), (15, 8, GRE)):
        s += f'<rect x="{xx}" y="{yy}" width="13" height="10" fill="{col}"/>'
    return s


def ic_rubric(c):
    s = ''
    for r in range(4):
        for k in range(4):
            col = c if (r + k) % 3 == 0 else '#E8E4F7'
            s += f'<rect x="{-30 + k * 15}" y="{-28 + r * 14}" width="13" height="12" rx="2" fill="{col}"/>'
    return s


def ic_check(c):
    s = f'<rect x="-26" y="-30" width="52" height="60" rx="6" fill="#fff" stroke="{c}" stroke-width="3"/>'
    for i in range(3):
        y = -18 + i * 16
        s += (f'<rect x="-18" y="{y - 5}" width="10" height="10" rx="2" fill="none" stroke="{c}" stroke-width="2"/>'
              f'<path d="M-16 {y} l3 3 l6 -7" stroke="{GRE}" stroke-width="3" fill="none"/><rect x="-3" y="{y - 2}" width="22" height="4" rx="2" fill="#C9C3E8"/>')
    return s


def ic_laptop(c):
    return (f'<rect x="-28" y="-24" width="56" height="36" rx="4" fill="{INK}"/><rect x="-24" y="-20" width="48" height="28" fill="#1E293B"/>'
            f'<path d="M-36 14 H36 L30 22 H-30Z" fill="{MUT}"/><text x="0" y="0" font-size="13" fill="#7EE7C7" text-anchor="middle" font-family="monospace">&lt;/&gt;</text>')


def ic_folder(c):
    return (f'<path d="M-32 -18 H-8 L-2 -12 H32 V24 H-32Z" fill="{c}"/><rect x="-26" y="-22" width="44" height="30" fill="#fff" transform="rotate(-6)"/>'
            f'<path d="M-32 -6 H32 V24 H-32Z" fill="{c}"/>')


def ic_eye(c):
    return (f'<path d="M-32 0 Q0 -30 32 0 Q0 30 -32 0Z" fill="#fff" stroke="{c}" stroke-width="3"/><circle r="11" fill="{c}"/><circle r="4" fill="{INK}"/>')


def ic_mirror(c):
    return person(-14, 22, c, .75) + person(16, 22, TEA, .75) + f'<path d="M-6 -36 q8 -10 18 0" stroke="{AMB}" stroke-width="3" fill="none" marker-end="url(#ar)"/>'


def ic_lupa(c):
    return f'<circle cx="-6" cy="-6" r="18" fill="#fff" stroke="{c}" stroke-width="5"/><line x1="7" y1="7" x2="24" y2="24" stroke="{c}" stroke-width="7" stroke-linecap="round"/>'


def ic_chart(c):
    return (f'<rect x="-28" y="-26" width="56" height="50" rx="5" fill="#fff" stroke="{c}" stroke-width="2"/>'
            f'<polyline points="-20,14 -8,4 2,8 12,-6 22,-14" stroke="{c}" stroke-width="4" fill="none"/>'
            + ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{AMB}"/>' for x, y in ((-20, 14), (-8, 4), (2, 8), (12, -6), (22, -14))))


def ic_medal(c):
    return (f'<path d="M-14 -32 L-4 -8 M14 -32 L4 -8" stroke="{COR}" stroke-width="8"/><circle cy="8" r="20" fill="{c}"/>'
            f'<circle cy="8" r="13" fill="none" stroke="#fff" stroke-width="3"/><path d="M0 0 l3 6 l7 1 l-5 5 l1 7 l-6 -3 l-6 3 l1 -7 l-5 -5 l7 -1z" fill="#fff"/>')


def ic_bus(c):
    return (f'<rect x="-34" y="-22" width="68" height="38" rx="8" fill="{c}"/><rect x="-28" y="-16" width="16" height="14" fill="#DDF3FF"/>'
            f'<rect x="-8" y="-16" width="16" height="14" fill="#DDF3FF"/><rect x="12" y="-16" width="16" height="14" fill="#DDF3FF"/>'
            f'<circle cx="-20" cy="18" r="7" fill="{INK}"/><circle cx="20" cy="18" r="7" fill="{INK}"/>')


def ic_mic(c):
    return (f'<rect x="-9" y="-30" width="18" height="34" rx="9" fill="{c}"/><path d="M-18 -4 a18 18 0 0 0 36 0" stroke="{INK}" stroke-width="3" fill="none"/>'
            f'<line x1="0" y1="14" x2="0" y2="26" stroke="{INK}" stroke-width="3"/><line x1="-12" y1="26" x2="12" y2="26" stroke="{INK}" stroke-width="3"/>')


def ic_code(c):
    return (f'<rect x="-30" y="-24" width="60" height="44" rx="6" fill="{c}"/><text x="0" y="6" font-size="22" font-weight="800" fill="#fff" text-anchor="middle" font-family="monospace">{{}}</text>')


def ic_trophy(c):
    return (f'<path d="M-18 -26 H18 V-6 a18 18 0 0 1 -36 0Z" fill="{c}"/><path d="M-18 -20 h-10 a10 10 0 0 0 10 14 M18 -20 h10 a10 10 0 0 1 -10 14" stroke="{c}" stroke-width="4" fill="none"/>'
            f'<rect x="-4" y="10" width="8" height="10" fill="{c}"/><rect x="-14" y="20" width="28" height="7" rx="2" fill="{INK}"/>')


def ic_robot(c):
    return (f'<rect x="-22" y="-20" width="44" height="34" rx="8" fill="{c}"/><circle cx="-9" cy="-4" r="5" fill="#fff"/><circle cx="9" cy="-4" r="5" fill="#fff"/>'
            f'<rect x="-8" y="6" width="16" height="3" fill="#fff"/><line x1="0" y1="-20" x2="0" y2="-30" stroke="{INK}" stroke-width="3"/><circle cy="-32" r="4" fill="{COR}"/>'
            f'<rect x="-16" y="16" width="32" height="10" rx="3" fill="{MUT}"/>')


def ic_shield(c):
    return f'<path d="M0 -30 L26 -20 V0 Q26 22 0 32 Q-26 22 -26 0 V-20Z" fill="{c}"/><path d="M-10 0 l7 8 l14 -16" stroke="#fff" stroke-width="5" fill="none"/>'


def ic_globe(c):
    return (f'<circle r="26" fill="{c}"/><ellipse rx="11" ry="26" fill="none" stroke="#fff" stroke-width="2.5"/>'
            f'<line x1="-26" x2="26" stroke="#fff" stroke-width="2.5"/><path d="M-22 -13 H22 M-22 13 H22" stroke="#fff" stroke-width="2"/>')


def icon(fn, x, y, c, s=1.0):
    return f'<g transform="translate({x},{y}) scale({s})">{fn(c)}</g>'


# ---------- ilustraciones ----------
def pd_bases(T):
    W, H = 1100, 680
    b = head(W, T['t'], T['sub'])
    # sol / meta
    b += f'<circle cx="960" cy="150" r="42" fill="{AMB}"/>' + tx(960, 156, T['meta'], 13, 700, INK)
    # tejado
    b += f'<path d="M210 250 L550 120 L890 250 Z" fill="{IND}" filter="url(#sh)"/>' + tx(550, 215, T['techo'], 26, 800, '#fff')
    # pilares
    cols = [COR, AMB, TEA, SKY, PUR]
    for i, (p, c) in enumerate(zip(T['pilares'], cols)):
        x = 240 + i * 128
        b += f'<rect x="{x}" y="262" width="104" height="220" rx="10" fill="{c}" filter="url(#sh)"/>'
        b += f'<rect x="{x - 6}" y="256" width="116" height="14" rx="4" fill="{INK}" opacity=".2"/>'
        b += tx(x + 52, 360, p, 15, 700, '#fff')
    # suelo contexto
    b += card(200, 492, 700, 54, '#EDE9FB', 10) + tx(550, 525, T['contexto'], 17, 700, IND)
    # cimientos
    b += f'<rect x="170" y="556" width="760" height="86" rx="10" fill="{MUT}" filter="url(#sh)"/>'
    for i in range(10):
        b += f'<line x1="{170 + i * 76}" y1="556" x2="{170 + i * 76}" y2="642" stroke="#fff" stroke-opacity=".15" stroke-width="2"/>'
    b += tx(550, 588, T['cim'], 18, 800, '#fff') + tx(550, 616, T['cim2'], 14, 400, '#E7E9F3')
    # personas
    b += person(110, 640, TEA, 1.1) + person(990, 640, COR, 1.1) + person(1040, 640, SKY, .9)
    return svg(W, H, b, T['t'])


def pd_preguntas(T):
    W, H = 1100, 700
    b = head(W, T['t'], T['sub'])
    cx, cy = 550, 350
    pos = [(200, 200, COR), (900, 200, AMB), (200, 500, TEA), (900, 500, SKY), (550, 640, PUR)]
    for (x, y, c) in pos[:4]:
        b += f'<line x1="{x}" y1="{y}" x2="{cx}" y2="{cy}" stroke="{c}" stroke-width="3" stroke-dasharray="6 6"/>'
    b += f'<line x1="550" y1="470" x2="550" y2="608" stroke="{PUR}" stroke-width="3" stroke-dasharray="6 6"/>'
    b += f'<g filter="url(#sh)"><path d="M480 240 H600 L640 280 V470 H480Z" fill="#fff" stroke="{IND}" stroke-width="3"/><path d="M600 240 V280 H640" fill="#EDE9FB" stroke="{IND}" stroke-width="3"/></g>'
    for i in range(6):
        b += f'<rect x="500" y="{300 + i * 24}" width="{110 - (i % 3) * 18}" height="8" rx="4" fill="#C9C3E8"/>'
    b += tx(560, 455, 'PD', 22, 800, IND)
    for (x, y, c), (q, a) in zip(pos, T['preg']):
        if y < 600:
            b += card(x - 160, y - 55, 320, 110) + f'<rect x="{x - 160}" y="{y - 55}" width="10" height="110" rx="5" fill="{c}"/>'
            b += tx(x + 5, y - 15, q, 21 if len(q) < 22 else 17, 800, c) + tx(x + 5, y + 18, a, 15, 400, MUT)
        else:
            b += card(x - 230, y - 32, 460, 52) + f'<rect x="{x - 230}" y="{y - 32}" width="10" height="52" rx="5" fill="{c}"/>'
            b += tx(x, y - 7, q, 18, 800, c) + tx(x, y + 13, a, 13, 400, MUT)
    return svg(W, H, b, T['t'])


def eval_ciclo(T):
    W, H = 1000, 760
    b = head(W, T['t'], T['sub'])
    cx, cy, r = 500, 420, 170
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#DCD6F5" stroke-width="40"/>'
    cols = [SKY, AMB, COR, TEA]
    import math
    for i, c in enumerate(cols):
        a0, a1 = math.radians(-90 + i * 90 + 8), math.radians(-90 + (i + 1) * 90 - 8)
        x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
        b += f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{c}" stroke-width="40" fill="none"/>'
        b += f'<path d="M{x1:.1f} {y1:.1f} l0 0" stroke="{c}" stroke-width="2" marker-end="url(#ar)"/>'
    pos = [(cx, cy - r - 2), (cx + r + 2, cy), (cx, cy + r + 2), (cx - r - 2, cy)]
    off = [(0, -70), (175, 0), (0, 72), (-175, 0)]
    icons = [ic_lupa, ic_chart, ic_medal, ic_bulb]
    for (x, y), (dx, dy), c, (t, s), fn in zip(pos, off, cols, T['fases'], icons):
        b += f'<circle cx="{x}" cy="{y}" r="34" fill="#fff" stroke="{c}" stroke-width="5" filter="url(#sh)"/>' + icon(fn, x, y, c, .62)
        b += card(x + dx - 130, y + dy - 34, 260, 68) + tx(x + dx, y + dy - 8, t, 17, 800, c) + tx(x + dx, y + dy + 16, s, 13, 400, MUT)
    b += person(cx - 30, cy + 40, IND, 1.3) + person(cx + 36, cy + 40, TEA, 1.1)
    b += tx(cx, cy - 60, T['centro'], 17, 800, IND)
    return svg(W, H, b, T['t'])


def eval_momentos(T):
    W, H = 1100, 440
    b = head(W, T['t'], T['sub'])
    b += f'<line x1="120" y1="250" x2="990" y2="250" stroke="{MUT}" stroke-width="6" stroke-linecap="round" marker-end="url(#ar)"/>'
    b += tx(1000, 285, T['curso'], 14, 700, MUT, 'end')
    for x, c, fn, (t, a, e) in zip((220, 550, 880), (SKY, AMB, COR), (ic_lupa, ic_chart, ic_medal), T['mom']):
        b += f'<circle cx="{x}" cy="250" r="46" fill="#fff" stroke="{c}" stroke-width="6" filter="url(#sh)"/>' + icon(fn, x, 250, c, .8)
        b += tx(x, 172, t, 22, 800, c)
        b += card(x - 150, 312, 300, 100) + tx(x, 342, a, 15, 700, INK) + tx(x, 370, e, 13, 400, MUT)
    return svg(W, H, b, T['t'])


def eval_instrumentos(T):
    W, H = 1100, 600
    b = head(W, T['t'], T['sub'])
    fns = [ic_rubric, ic_check, ic_laptop, ic_folder, ic_eye, ic_mirror]
    cols = [IND, TEA, SKY, AMB, COR, PUR]
    for i, (fn, c, (t, d)) in enumerate(zip(fns, cols, T['ins'])):
        x, y = 70 + (i % 3) * 330, 120 + (i // 3) * 230
        b += card(x, y, 300, 200) + f'<rect x="{x}" y="{y}" width="300" height="8" rx="4" fill="{c}"/>'
        b += f'<circle cx="{x + 150}" cy="{y + 66}" r="44" fill="{c}" opacity=".12"/>' + icon(fn, x + 150, y + 66, c, .95)
        b += tx(x + 150, y + 140, t, 19, 800, c) + tx(x + 150, y + 165, d, 13, 400, MUT)
    return svg(W, H, b, T['t'])


def met_mosaico(T):
    W, H = 1100, 640
    b = head(W, T['t'], T['sub'])
    fns = [ic_bulb, ic_flag, ic_flip, ic_team, ic_game, ic_board]
    cols = [AMB, TEA, SKY, COR, PUR, IND]
    for i, (fn, c, (t, d)) in enumerate(zip(fns, cols, T['met'])):
        x, y = 70 + (i % 3) * 330, 120 + (i // 3) * 250
        b += card(x, y, 300, 225, c, 20)
        b += f'<circle cx="{x + 150}" cy="{y + 78}" r="52" fill="#fff" opacity=".95"/>' + icon(fn, x + 150, y + 78, c, 1.05)
        b += tx(x + 150, y + 162 - (6 if chr(10) in t else 0), t, 20, 800, '#fff') + tx(x + 150, y + 203, d, 13.5, 400, '#fff')
    return svg(W, H, b, T['t'])


def eduscrum_ciclo(T):
    W, H = 1100, 660
    b = head(W, T['t'], T['sub'])
    # backlog
    b += card(40, 140, 220, 400) + tx(150, 176, T['backlog'], 17, 800, IND)
    for i, it in enumerate(T['items']):
        b += f'<rect x="58" y="{196 + i * 56}" width="184" height="44" rx="8" fill="#EDE9FB"/>' + tx(150, 224 + i * 56 - (7 if chr(10) in it else 0), it, 13, 600, INK)
    b += tx(150, 520, T['po'], 13, 700, MUT)
    b += f'<line x1="262" y1="330" x2="320" y2="330" stroke="{MUT}" stroke-width="4" marker-end="url(#ar)"/>'
    # planning
    b += card(330, 270, 170, 120, AMB) + tx(415, 312, T['plan'], 17, 800, '#fff') + tx(415, 340, T['plan2'], 12.5, 400, '#fff')
    b += f'<line x1="500" y1="330" x2="560" y2="330" stroke="{MUT}" stroke-width="4" marker-end="url(#ar)"/>'
    # sprint circle
    cx, cy = 680, 330
    b += f'<circle cx="{cx}" cy="{cy}" r="120" fill="#fff" stroke="{TEA}" stroke-width="10" filter="url(#sh)"/>'
    b += f'<path d="M{cx + 26} {cy - 128} a34 34 0 1 0 -52 0" stroke="{SKY}" stroke-width="6" fill="none"/><path d="M{cx - 34} {cy - 134} l8 10 l6 -12z" fill="{SKY}"/>'
    b += tx(cx, cy - 218, T['daily'], 15, 800, SKY) + tx(cx, cy - 199, T['daily2'], 12, 400, MUT)
    b += tx(cx, cy - 30, T['sprint'], 24, 800, TEA) + tx(cx, cy, T['sprint2'], 13, 400, MUT)
    b += icon(ic_board, cx, cy + 60, TEA, 1.0)
    b += f'<line x1="800" y1="330" x2="850" y2="330" stroke="{MUT}" stroke-width="4" marker-end="url(#ar)"/>'
    # review + retro
    b += card(860, 200, 200, 110, COR) + tx(960, 240, T['review'], 17, 800, '#fff') + tx(960, 268, T['review2'], 12.5, 400, '#fff')
    b += card(860, 350, 200, 110, PUR) + tx(960, 390, T['retro'], 17, 800, '#fff') + tx(960, 418, T['retro2'], 12.5, 400, '#fff')
    b += f'<path d="M960 470 Q960 600 680 600 Q420 600 415 400" stroke="{MUT}" stroke-width="3" fill="none" stroke-dasharray="7 6" marker-end="url(#ar)"/>'
    b += tx(680, 625, T['vuelta'], 14, 700, MUT)
    # roles
    b += person(330, 520, IND, 1.0) + tx(330, 560, T['rol1'], 12, 700, IND)
    b += person(420, 520, TEA, 1.0) + tx(420, 560, T['rol2'], 12, 700, TEA)
    return svg(W, H, b, T['t'])


def eduscrum_tablero(T):
    W, H = 1100, 620
    b = head(W, T['t'], T['sub'])
    b += card(60, 115, 980, 470, '#FFFFFF', 14)
    heads = T['cols']
    xs = [60, 260, 500, 740]
    widths = [200, 240, 240, 300]
    colc = [MUT, AMB, SKY, GRE]
    for x, w, h, c in zip(xs, widths, heads, colc):
        b += f'<rect x="{x}" y="115" width="{w}" height="46" fill="{c}" {"rx=\"14\"" if x == 60 else ""}/>' + tx(x + w / 2, 145, h, 16, 800, '#fff')
        b += f'<line x1="{x}" y1="115" x2="{x}" y2="585" stroke="#E2E0EE" stroke-width="2"/>'
    # col 0: team info
    b += tx(160, 195, T['equipo'], 15, 800, INK)
    for i, p in enumerate(T['miembros']):
        b += person(100 + (i % 2) * 120, 260 + (i // 2) * 90, [IND, TEA, COR, AMB][i], .85) + tx(100 + (i % 2) * 120, 290 + (i // 2) * 90, p, 11.5, 600, MUT)
    b += f'<rect x="78" y="420" width="164" height="140" rx="8" fill="#EDE9FB"/>' + tx(160, 444, T['dod'], 13, 800, IND) + tx(160, 466, T['dod2'], 11.5, 400, INK)
    notes = {1: T['todo'], 2: T['doing'], 3: T['done']}
    ncol = {1: '#FFE7A3', 2: '#CFE4FF', 3: '#CDEFD9'}
    for k, items in notes.items():
        for j, it in enumerate(items):
            x = xs[k] + 20 + (j % 2) * ((widths[k] - 40) / 2 + 4)
            y = 180 + (j // 2) * 98
            ww = (widths[k] - 48) / 2
            rot = (-2, 2, 1, -1)[j % 4]
            b += f'<g transform="rotate({rot} {x + ww / 2} {y + 40})"><rect x="{x}" y="{y}" width="{ww:.0f}" height="82" fill="{ncol[k]}" filter="url(#sh)"/>'
            b += f'<circle cx="{x + ww / 2:.0f}" cy="{y + 8}" r="4" fill="{COR}"/>' + tx(x + ww / 2, y + 36, it, 12, 600, INK) + '</g>'
    # burndown
    bx, by = 760, 470
    b += f'<rect x="{bx}" y="{by - 20}" width="260" height="110" rx="8" fill="#F6F4FD"/>' + tx(bx + 130, by, T['burn'], 12.5, 800, INK)
    b += f'<polyline points="{bx + 20},{by + 20} {bx + 240},{by + 80}" stroke="#C9C3E8" stroke-width="3" stroke-dasharray="5 4" fill="none"/>'
    b += f'<polyline points="{bx + 20},{by + 20} {bx + 70},{by + 30} {bx + 120},{by + 52} {bx + 160},{by + 58}" stroke="{COR}" stroke-width="4" fill="none"/>'
    return svg(W, H, b, T['t'])


def neae_mapa(T):
    W, H = 1100, 700
    b = head(W, T['t'], T['sub'])
    cx, cy = 550, 400
    b += f'<circle cx="{cx}" cy="{cy}" r="270" fill="#EDE9FB" stroke="{IND}" stroke-width="3" stroke-dasharray="10 8"/>'
    b += f'<rect x="{cx - 60}" y="{cy - 292}" width="120" height="36" rx="18" fill="{IND}"/>' + tx(cx, cy - 267, T['neae'], 18, 800, '#fff')
    b += f'<circle cx="{cx}" cy="{cy}" r="92" fill="{IND}" filter="url(#sh)"/>' + tx(cx, cy - 18, T['nee'], 22, 800, '#fff') + tx(cx, cy + 10, T['nee2'], 12.5, 400, '#E9E6FA')
    import math
    cols = [TEA, AMB, COR, SKY, PUR, GRE, '#D9822B', '#C2417A']
    n = len(T['grupos'])
    for i, (g, c) in enumerate(zip(T['grupos'], cols)):
        a = math.radians(-90 + 360 / n * i + 22)
        x, y = cx + 185 * math.cos(a), cy + 185 * math.sin(a)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="62" fill="{c}" filter="url(#sh)"/>' + tx(x, y - (len(g.split(chr(10))) - 1) * 8 + 5, g, 13, 700, '#fff')
    b += tx(cx, 690, T['pie'], 13, 400, MUT)
    return svg(W, H, b, T['t'])


def inclusion_niveles(T):
    W, H = 1100, 560
    b = head(W, T['t'], T['sub'])
    cols = [TEA, SKY, AMB, COR]
    for i, ((n, d, e), c) in enumerate(zip(T['niv'], cols)):
        w = 820 - i * 170
        x = 140 + i * 85
        y = 460 - i * 92
        b += f'<rect x="{x}" y="{y}" width="{w}" height="80" rx="12" fill="{c}" filter="url(#sh)"/>'
        b += tx(x + 40, y + 50, n, 30, 800, '#fff')
        b += tx(x + w / 2 + 20, y + 34, d, 16, 800, '#fff') + tx(x + w / 2 + 20, y + 58, e, 12.5, 400, '#fff')
    b += f'<line x1="1010" y1="530" x2="1010" y2="190" stroke="{MUT}" stroke-width="4" marker-end="url(#ar)"/>'
    b += tx(1030, 360, T['eje'], 13, 700, MUT, 'start', style=' writing-mode="tb"')
    b += person(80, 530, IND, 1.0) + person(60, 540, TEA, .8) + person(104, 545, AMB, .75)
    return svg(W, H, b, T['t'])


def complementarias(T):
    W, H = 1100, 640
    b = head(W, T['t'], T['sub'])
    for k, (x, c, tit, sub, items, fns) in enumerate((
            (50, SKY, T['comp'], T['comp2'], T['ci'], (ic_bus, ic_mic, ic_code, ic_shield)),
            (570, COR, T['extra'], T['extra2'], T['ei'], (ic_trophy, ic_robot, ic_globe, ic_bulb)))):
        b += card(x, 110, 480, 500) + f'<rect x="{x}" y="110" width="480" height="84" rx="16" fill="{c}"/>'
        b += tx(x + 240, 145, tit, 22, 800, '#fff') + tx(x + 240, 174, sub, 13, 400, '#fff')
        for i, (it, fn) in enumerate(zip(items, fns)):
            yy = 215 + i * 96
            b += f'<circle cx="{x + 60}" cy="{yy + 40}" r="36" fill="{c}" opacity=".12"/>' + icon(fn, x + 60, yy + 40, c, .78)
            t1, t2 = it
            b += tx(x + 115, yy + 34, t1, 16, 800, INK, 'start') + tx(x + 115, yy + 56, t2, 12.5, 400, MUT, 'start')
    return svg(W, H, b, T['t'])


def ruta(T):
    W, H = 1200, 420
    b = head(W, T['t'], T['sub'])
    pts = [(90, 300), (210, 200), (330, 300), (450, 200), (570, 300), (690, 200), (810, 300), (930, 200), (1050, 300)]
    d = 'M60 330 C 120 330, 150 180, 210 200 S 300 330, 330 300 S 420 170, 450 200 S 540 330, 570 300 S 660 170, 690 200 S 780 330, 810 300 S 900 170, 930 200 S 1020 330, 1050 300 L 1150 300'
    b += f'<path d="{d}" stroke="#DCD6F5" stroke-width="34" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#fff" stroke-width="3" fill="none" stroke-dasharray="14 12"/>'
    cols = [IND, SKY, TEA, GRE, AMB, '#D9822B', COR, PUR, '#C2417A']
    for i, ((x, y), c, t) in enumerate(zip(pts, cols, T['temas'])):
        b += f'<circle cx="{x}" cy="{y}" r="26" fill="{c}" stroke="#fff" stroke-width="4" filter="url(#sh)"/>' + tx(x, y + 7, str(i + 1), 19, 800, '#fff')
        ty = (y - 44 - (14 if chr(10) in t else 0)) if y < 250 else y + 52
        b += tx(x, ty, t, 12.5, 700, INK)
    b += icon(ic_flag, 1150, 270, GRE, 1.0) + tx(1150, 340, T['meta'], 14, 800, GRE)
    return svg(W, H, b, T['t'])


TEXTOS = {
    'es': {
        'pd-bases': dict(t='Las bases de la programación didáctica', sub='Una casa que se construye desde los cimientos: sin normativa ni contexto, no se sostiene',
                         meta='Alumnado\ncompetente', techo='PROGRAMACIÓN DIDÁCTICA',
                         pilares=['Objetivos\ny RA', 'Contenidos\ny secuencia', 'Metodología\ny recursos', 'Evaluación', 'Inclusión'],
                         contexto='Contexto: centro · entorno · grupo · alumnado con NEAE',
                         cim='CIMIENTOS: CURRÍCULO OFICIAL Y NORMATIVA',
                         cim2='LOE-LOMLOE · LO 3/2022 · RD 659/2023 · RD del título · Decreto 114/2025 · evaluación e inclusión'),
        'pd-preguntas': dict(t='Las preguntas que responde una programación', sub='Si tu PD contesta a estas cinco preguntas, está completa',
                             preg=[('¿Qué enseñar?', 'Objetivos, RA, competencias\ny contenidos'), ('¿Cuándo enseñar?', 'Secuenciación y temporalización\nde las unidades'),
                                   ('¿Cómo enseñar?', 'Metodología, actividades,\nrecursos y espacios'), ('¿Qué, cómo y cuándo evaluar?', 'Criterios, instrumentos,\ncalificación y recuperación'),
                                   ('¿A quién?', 'Contexto del centro, del grupo y atención a la diversidad')]),
        'eval-ciclo': dict(t='¿Qué es evaluar?', sub='Recoger información para valorar el aprendizaje, tomar decisiones y mejorar',
                           centro='Alumnado y docente', fases=[('1. Recoger información', 'Observar, corregir, preguntar'), ('2. Valorar', 'Comparar con los criterios'),
                                                              ('3. Decidir', 'Calificar, reforzar, ampliar'), ('4. Mejorar', 'Retroalimentar y ajustar la enseñanza')]),
        'eval-momentos': dict(t='Los tres momentos de la evaluación', sub='La evaluación acompaña todo el curso, no solo el final', curso='Curso escolar',
                              mom=[('Inicial', '¿De dónde partimos?', 'Cuestionario, prueba sencilla, encuesta'), ('Continua', '¿Cómo vamos?', 'Prácticas, observación, portafolio'),
                                   ('Final', '¿Hemos llegado?', 'Logro de los RA, calificación')]),
        'eval-instrumentos': dict(t='Instrumentos de evaluación', sub='Varía los instrumentos: cada uno mira el aprendizaje desde un ángulo distinto',
                                  ins=[('Rúbrica', 'Proyectos, informes, exposiciones'), ('Lista de cotejo', '¿Se cumple el procedimiento?'),
                                       ('Prueba práctica', 'Instalar, configurar, programar'), ('Portafolio', 'La evolución a lo largo del curso'),
                                       ('Observación', 'Diario y escalas de valoración'), ('Auto y coevaluación', 'Reflexionar sobre cómo se aprende')]),
        'met-mosaico': dict(t='Metodologías activas', sub='El alumnado deja de escuchar para empezar a hacer',
                            met=[('Aprendizaje basado\nen proyectos', 'Crear un producto real'), ('Aprendizaje basado\nen retos', 'Resolver un problema abierto'),
                                 ('Flipped classroom', 'Teoría en casa, práctica en clase'), ('Aprendizaje\ncooperativo', 'Equipos con roles'),
                                 ('Gamificación', 'Mecánicas de juego'), ('eduScrum', 'Sprints, tablero y retrospectiva')]),
        'eduscrum-ciclo': dict(t='eduScrum: el ciclo de un sprint', sub='El docente marca el qué; el equipo decide el cómo',
                               backlog='Pila de aprendizaje', items=['Objetivos y RA', 'Criterios de\nevaluación', 'Definición de\nterminado', 'Retos de la unidad', 'Entregables'],
                               po='Docente = product owner', plan='Planificación', plan2='Tareas, reparto y\ndefinición de diversión',
                               daily='Stand-up al inicio de cada clase', daily2='¿Qué hice? ¿Qué haré? ¿Qué me frena?', sprint='SPRINT', sprint2='2 a 4 semanas · una unidad',
                               review='Revisión', review2='Se muestra lo aprendido\ny se evalúa', retro='Retrospectiva', retro2='¿Cómo hemos trabajado?\n¿Qué mejoramos?',
                               vuelta='Siguiente sprint', rol1='Docente', rol2='eduScrum master'),
        'eduscrum-tablero': dict(t='El tablero de un equipo eduScrum', sub='Ejemplo: unidad «Instalación de un servidor web» en 2.º ASIR',
                                 cols=['Equipo', 'Por hacer', 'Haciendo', 'Hecho'], equipo='Equipo «Los Root»', miembros=['Ana · master', 'Iván', 'Lucía', 'Omar'],
                                 dod='Definición de terminado', dod2='Probado en la VM\nDocumentado en Git\nRevisado por otro\nmiembro del equipo',
                                 todo=['Configurar\nHTTPS', 'Virtual hosts', 'Pruebas de\ncarga', 'Manual de\nusuario'], doing=['Instalar\nApache', 'Permisos y\nusuarios'],
                                 done=['Preparar la VM', 'Diagrama de\nred', 'Estudiar\ndocumentación', 'Plan del\nsprint'], burn='Gráfico de avance (burndown)'),
        'neae-mapa': dict(t='Alumnado con necesidad específica de apoyo educativo (NEAE)', sub='Las NEE son una parte de las NEAE (LOE, art. 71)',
                          neae='NEAE', nee='NEE', nee2='Discapacidad o trastornos\ngraves de conducta,\ncomunicación o lenguaje',
                          grupos=['Altas\ncapacidades', 'Trastornos de\natención o\naprendizaje', 'Retraso\nmadurativo', 'Trastornos del\nlenguaje y la\ncomunicación',
                                  'Desconocimiento\ngrave de la\nlengua', 'Vulnerabilidad\nsocioeducativa', 'Incorporación\ntardía', 'Condiciones\npersonales o\nde historia escolar'],
                          pie='Toda persona con NEE tiene NEAE, pero no al revés.'),
        'inclusion-niveles': dict(t='Niveles de respuesta para la inclusión', sub='Orden 20/2019 de la Comunitat Valenciana: de todo el centro a cada alumno o alumna',
                                  eje='Más individual', niv=[('I', 'Toda la comunidad educativa', 'Planes de centro, accesibilidad, convivencia'),
                                                             ('II', 'Grupo-clase', 'DUA, metodologías activas, tutoría'),
                                                             ('III', 'Respuesta diferenciada', 'Refuerzo, ampliación, acceso'),
                                                             ('IV', 'Respuesta especializada', 'Apoyos especializados')]),
        'complementarias': dict(t='Actividades complementarias y extraescolares', sub='Las dos se programan en la PD y se incluyen en la programación general anual (PGA)',
                                comp='Complementarias', comp2='En horario lectivo · forman parte del currículo · para todo el grupo',
                                ci=[('Visita a una empresa o CPD', 'Ver en real lo que se trabaja en el aula'), ('Charla de un profesional', 'Ciberseguridad, desarrollo, sistemas'),
                                    ('CodeWeek, Hour of Code', 'Jornadas de programación en el centro'), ('Jornada de ciberseguridad', 'Retos tipo CTF, Día de Internet Segura')],
                                extra='Extraescolares', extra2='Fuera del horario lectivo · voluntarias · no evaluables',
                                ei=[('Olimpiadas y concursos', 'Olimpiada de Informática, Skills, CyberOlympics'), ('Club de robótica o maker', 'Arduino, Raspberry Pi, impresión 3D'),
                                    ('Movilidad Erasmus+', 'Prácticas y estancias en el extranjero'), ('Hackathon', 'Desarrollar un proyecto en un fin de semana')]),
        'ruta': dict(t='La ruta del bloque II', sub='Nueve paradas hasta la defensa ante el tribunal', meta='Oposición',
                     temas=['Marco\nlegal', 'Títulos y\ncurrículos', 'La PD', 'Metodología', 'Evaluación', 'Inclusión', 'Unidad de\nprogramación', 'Oposiciones\n254', 'Defensa']),
    },
    'val': {
        'pd-bases': dict(t='Les bases de la programació didàctica', sub='Una casa que es construeix des dels fonaments: sense normativa ni context, no s\'aguanta',
                         meta='Alumnat\ncompetent', techo='PROGRAMACIÓ DIDÀCTICA',
                         pilares=['Objectius\ni RA', 'Continguts\ni seqüència', 'Metodologia\ni recursos', 'Avaluació', 'Inclusió'],
                         contexto='Context: centre · entorn · grup · alumnat amb NESE',
                         cim='FONAMENTS: CURRÍCULUM OFICIAL I NORMATIVA',
                         cim2='LOE-LOMLOE · LO 3/2022 · RD 659/2023 · RD del títol · Decret 114/2025 · avaluació i inclusió'),
        'pd-preguntas': dict(t='Les preguntes que respon una programació', sub='Si la teua PD contesta aquestes cinc preguntes, està completa',
                             preg=[('Què ensenyar?', 'Objectius, RA, competències\ni continguts'), ('Quan ensenyar?', 'Seqüenciació i temporització\nde les unitats'),
                                   ('Com ensenyar?', 'Metodologia, activitats,\nrecursos i espais'), ('Què, com i quan avaluar?', 'Criteris, instruments,\nqualificació i recuperació'),
                                   ('A qui?', 'Context del centre, del grup i atenció a la diversitat')]),
        'eval-ciclo': dict(t='Què és avaluar?', sub='Recollir informació per a valorar l\'aprenentatge, prendre decisions i millorar',
                           centro='Alumnat i docent', fases=[('1. Recollir informació', 'Observar, corregir, preguntar'), ('2. Valorar', 'Comparar amb els criteris'),
                                                             ('3. Decidir', 'Qualificar, reforçar, ampliar'), ('4. Millorar', 'Retroalimentar i ajustar l\'ensenyament')]),
        'eval-momentos': dict(t='Els tres moments de l\'avaluació', sub='L\'avaluació acompanya tot el curs, no només el final', curso='Curs escolar',
                              mom=[('Inicial', 'D\'on partim?', 'Qüestionari, prova senzilla, enquesta'), ('Contínua', 'Com anem?', 'Pràctiques, observació, portafolis'),
                                   ('Final', 'Hi hem arribat?', 'Assoliment dels RA, qualificació')]),
        'eval-instrumentos': dict(t='Instruments d\'avaluació', sub='Varia els instruments: cadascun mira l\'aprenentatge des d\'un angle diferent',
                                  ins=[('Rúbrica', 'Projectes, informes, exposicions'), ('Llista de control', 'Es compleix el procediment?'),
                                       ('Prova pràctica', 'Instal·lar, configurar, programar'), ('Portafolis', 'L\'evolució al llarg del curs'),
                                       ('Observació', 'Diari i escales de valoració'), ('Auto i coavaluació', 'Reflexionar sobre com s\'aprén')]),
        'met-mosaico': dict(t='Metodologies actives', sub='L\'alumnat deixa d\'escoltar per a començar a fer',
                            met=[('Aprenentatge basat\nen projectes', 'Crear un producte real'), ('Aprenentatge basat\nen reptes', 'Resoldre un problema obert'),
                                 ('Flipped classroom', 'Teoria a casa, pràctica a classe'), ('Aprenentatge\ncooperatiu', 'Equips amb rols'),
                                 ('Gamificació', 'Mecàniques de joc'), ('eduScrum', 'Sprints, tauler i retrospectiva')]),
        'eduscrum-ciclo': dict(t='eduScrum: el cicle d\'un sprint', sub='El docent marca el què; l\'equip decideix el com',
                               backlog='Pila d\'aprenentatge', items=['Objectius i RA', 'Criteris\nd\'avaluació', 'Definició\nd\'acabat', 'Reptes de la unitat', 'Lliurables'],
                               po='Docent = product owner', plan='Planificació', plan2='Tasques, repartiment i\ndefinició de diversió',
                               daily='Stand-up a l\'inici de cada classe', daily2='Què vaig fer? Què faré? Què em frena?', sprint='SPRINT', sprint2='2 a 4 setmanes · una unitat',
                               review='Revisió', review2='Es mostra el que s\'ha après\ni s\'avalua', retro='Retrospectiva', retro2='Com hem treballat?\nQuè millorem?',
                               vuelta='Sprint següent', rol1='Docent', rol2='eduScrum master'),
        'eduscrum-tablero': dict(t='El tauler d\'un equip eduScrum', sub='Exemple: unitat «Instal·lació d\'un servidor web» en 2n ASIR',
                                 cols=['Equip', 'Per fer', 'Fent', 'Fet'], equipo='Equip «Els Root»', miembros=['Anna · master', 'Iván', 'Lucía', 'Omar'],
                                 dod='Definició d\'acabat', dod2='Provat en la VM\nDocumentat en Git\nRevisat per un altre\nmembre de l\'equip',
                                 todo=['Configurar\nHTTPS', 'Virtual hosts', 'Proves de\ncàrrega', 'Manual\nd\'usuari'], doing=['Instal·lar\nApache', 'Permisos i\nusuaris'],
                                 done=['Preparar la VM', 'Diagrama de\nxarxa', 'Estudiar\ndocumentació', 'Pla de\nl\'sprint'], burn='Gràfic d\'avanç (burndown)'),
        'neae-mapa': dict(t='Alumnat amb necessitat específica de suport educatiu (NESE)', sub='Les NEE són una part de les NESE (LOE, art. 71)',
                          neae='NESE', nee='NEE', nee2='Discapacitat o trastorns\ngreus de conducta,\ncomunicació o llenguatge',
                          grupos=['Altes\ncapacitats', 'Trastorns\nd\'atenció o\naprenentatge', 'Retard\nmaduratiu', 'Trastorns del\nllenguatge i la\ncomunicació',
                                  'Desconeixement\ngreu de la\nllengua', 'Vulnerabilitat\nsocioeducativa', 'Incorporació\ntardana', 'Condicions\npersonals o\nd\'història escolar'],
                          pie='Tota persona amb NEE té NESE, però no a l\'inrevés.'),
        'inclusion-niveles': dict(t='Nivells de resposta per a la inclusió', sub='Ordre 20/2019 de la Comunitat Valenciana: de tot el centre a cada alumne o alumna',
                                  eje='Més individual', niv=[('I', 'Tota la comunitat educativa', 'Plans de centre, accessibilitat, convivència'),
                                                             ('II', 'Grup classe', 'DUA, metodologies actives, tutoria'),
                                                             ('III', 'Resposta diferenciada', 'Reforç, ampliació, accés'),
                                                             ('IV', 'Resposta especialitzada', 'Suports especialitzats')]),
        'complementarias': dict(t='Activitats complementàries i extraescolars', sub='Totes dues es programen en la PD i s\'inclouen en la programació general anual (PGA)',
                                comp='Complementàries', comp2='En horari lectiu · formen part del currículum · per a tot el grup',
                                ci=[('Visita a una empresa o CPD', 'Veure en real el que es treballa a l\'aula'), ('Xarrada d\'un professional', 'Ciberseguretat, desenvolupament, sistemes'),
                                    ('CodeWeek, Hour of Code', 'Jornades de programació en el centre'), ('Jornada de ciberseguretat', 'Reptes tipus CTF, Dia d\'Internet Segura')],
                                extra='Extraescolars', extra2='Fora de l\'horari lectiu · voluntàries · no avaluables',
                                ei=[('Olimpíades i concursos', 'Olimpíada d\'Informàtica, Skills, CyberOlympics'), ('Club de robòtica o maker', 'Arduino, Raspberry Pi, impressió 3D'),
                                    ('Mobilitat Erasmus+', 'Pràctiques i estades a l\'estranger'), ('Hackathon', 'Desenvolupar un projecte en un cap de setmana')]),
        'ruta': dict(t='La ruta del bloc II', sub='Nou parades fins a la defensa davant del tribunal', meta='Oposició',
                     temas=['Marc\nlegal', 'Títols i\ncurrículums', 'La PD', 'Metodologia', 'Avaluació', 'Inclusió', 'Unitat de\nprogramació', 'Oposicions\n254', 'Defensa']),
    },
}

FUNCS = {'pd-bases': pd_bases, 'pd-preguntas': pd_preguntas, 'eval-ciclo': eval_ciclo, 'eval-momentos': eval_momentos,
         'eval-instrumentos': eval_instrumentos, 'met-mosaico': met_mosaico, 'eduscrum-ciclo': eduscrum_ciclo,
         'eduscrum-tablero': eduscrum_tablero, 'neae-mapa': neae_mapa, 'inclusion-niveles': inclusion_niveles,
         'complementarias': complementarias, 'ruta': ruta}

if __name__ == '__main__':
    for lang, textos in TEXTOS.items():
        d = RAIZ / 'assets' / 'images' / lang
        d.mkdir(parents=True, exist_ok=True)
        for nombre, fn in FUNCS.items():
            (d / f'{nombre}.svg').write_text(fn(textos[nombre]), encoding='utf-8')
    print('Ilustraciones generadas:', len(FUNCS) * len(TEXTOS))
