"""
=============================================================================
ESTRATOS - NEFANYAMUTO: EL DISENO (y luego el atlas de emociones)
=============================================================================
No lo carga TouchDesigner: se corre fuera, con Pillow:

    python3 sprites/hacer_atlas_nefanyamuto.py   # nefanyamuto_diseno.png y nefanyamuto_caras.png

NefanyaMuto, en el estilo de Trumpzilla (figura arcade de tres cuartos, rechoncha,
pintada con volumen, textura y contorno de tinta): la cabeza caricaturizada
(sprites/nefanyamuto_cabeza.py) sobre un cuerpo de MUTO con traje. La chaqueta y
la corbata arriba; las mangas acaban en garfios de quitina; debajo, patas de
insecto con espolones; detras, el abdomen anguloso con el saco naranja que
brilla y las patas de atras con las rodillas muy altas, y las crestas de quitina
que rompen la espalda de la chaqueta. Las orejas de soplillo hacen de alas
(pose 'vuelo').

Mismo formato de celda que Trumpzilla y Godzilla (192 x 256, mirando a la
izquierda, los pies abajo). Se pinta a 8 pixeles por pixel, se reduce, se pasa a
una paleta adaptada y se le pone el contorno de un pixel.
=============================================================================
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import nefanyamuto_cabeza as CAB          # noqa: E402
from nefanyamuto_cabeza import TINTA, bez  # noqa: E402

CELDA_W, CELDA_H = 192, 256
K = 8                                     # pixeles de trabajo por pixel de la celda
ESCALA_CABEZA = 0.64                      # pixeles de la celda por unidad de cabeza
CABEZA = (84, 46)                         # donde cae el origen de la cabeza (entre los ojos)

TRAJE = (40, 46, 78)
TRAJE_LUZ = (80, 92, 140)
TRAJE_OSC = (22, 24, 46)
TRAJE_HONDO = (10, 10, 24)
CAMISA = (236, 238, 242)
CAMISA_OSC = (170, 178, 196)
CORBATA_AZUL = ((44, 100, 220), (110, 160, 255), (22, 56, 150))
CORBATA_ROJA = ((206, 30, 40), (250, 96, 90), (130, 12, 22))
BOTON = (24, 26, 40)
QUITINA = (98, 86, 78)
QUITINA_LUZ = (156, 140, 122)
QUITINA_OSC = (58, 50, 48)
QUITINA_HONDA = (28, 24, 26)
SACO = (244, 124, 30)
SACO_LUZ = (255, 214, 96)
SACO_OSC = (150, 48, 16)
SACO_HALO = (255, 170, 60)


def lienzo():
    return CAB.Lienzo(k=K, ancho=CELDA_W, alto=CELDA_H, ox=0, oy=0)


def tramo(a, b, g0, g1):
    """Un trapecio de a (medio grosor g0) a b (g1)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    px, py = -dy / n, dx / n
    return [(a[0] + px * g0, a[1] + py * g0), (b[0] + px * g1, b[1] + py * g1),
            (b[0] - px * g1, b[1] - py * g1), (a[0] - px * g0, a[1] - py * g0)]


def textura(L, m, caja, n, semilla, osc, luz):
    """Grumos de la quitina: manchas pequenas oscuras y claras dentro de la mascara."""
    rnd = random.Random(semilla)
    x0, y0, x1, y1 = caja
    mo, ml = L.m_vacia(), L.m_vacia()
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(0.5, 1.3)
        L.m_elipse(x, y, r * 1.4, r, mo if rnd.random() < 0.6 else ml)
    L.pintar(mo, osc, 0.15, m, 0.6)
    L.pintar(ml, luz, 0.15, m, 0.45)


def _caja(pts, margen=2):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return (min(xs) - margen, min(ys) - margen, max(xs) + margen, max(ys) + margen)


# --- el MUTO ------------------------------------------------------------------------

def pata(L, cadera, rodilla, tobillo, pie, osc=False, semilla=1):
    """Pata de MUTO: muslo grueso, rodilla con espolon, tibia larga y la cuchilla del
    pie que acaba en garfio."""
    base = QUITINA_OSC if osc else QUITINA
    luz = QUITINA if osc else QUITINA_LUZ
    sombra = QUITINA_HONDA if osc else QUITINA_OSC
    dx = pie[0] - tobillo[0]
    gancho = -1.0 if pie[0] > 96 else 1.0
    piezas = [tramo(cadera, rodilla, 6.0, 4.4), tramo(rodilla, tobillo, 4.2, 2.8),
              [(tobillo[0] - 2.8, tobillo[1]), (tobillo[0] + 2.8, tobillo[1]), (pie[0] + 1.2, pie[1] - 7), (pie[0], pie[1]),
               (pie[0] + gancho * 6, pie[1] - 8), (pie[0] - 1.2, pie[1] - 9)]]
    for pts in piezas:
        m = L.forma(pts, base, luz, sombra, 1.8, 0.7, 1.2, a_luz=0.9)
        textura(L, m, _caja(pts), 40, semilla, sombra, luz)
        semilla += 7
    for p, r in ((rodilla, 5.2), (tobillo, 3.6)):
        nudo = [(p[0] - r, p[1]), (p[0] - r * 0.4, p[1] - r), (p[0] + r * 0.5, p[1] - r * 0.9), (p[0] + r, p[1]),
                (p[0] + r * 0.3, p[1] + r), (p[0] - r * 0.5, p[1] + r * 0.8)]
        L.forma(nudo, base, luz, sombra, 1.6, 0.6, 1.1)
    esp = [(rodilla[0] - 2.5, rodilla[1] - 3), (rodilla[0] + 2 + dx * 0.05, rodilla[1] - 14), (rodilla[0] + 3, rodilla[1] - 2)]
    L.forma(esp, base, luz, sombra, 1.5, 0.6, 1.1)


def abdomen(L, dy=0):
    pts = [(128, 128), (150, 118), (174, 128), (189, 152), (190, 186), (182, 214), (172, 232), (164, 210),
           (152, 188), (136, 170)]
    pts = [(x, y + dy) for x, y in pts]
    m = L.forma(pts, QUITINA, QUITINA_LUZ, QUITINA_OSC, 5, 2.0, 1.4, honda=QUITINA_HONDA)
    textura(L, m, _caja(pts), 160, 11, QUITINA_OSC, QUITINA_LUZ)
    # las placas: bandas que se solapan hacia la punta
    for k, t in enumerate((0.16, 0.34, 0.52, 0.70, 0.86)):
        a = (134 + t * 36, 160 + t * 40 + dy)        # borde de abajo
        b = (150 + t * 40, 118 + t * 60 + dy)        # borde de arriba
        if b[0] > 189:
            b = (189, b[1])
        arco = bez(a, ((a[0] + b[0]) / 2 + 8, (a[1] + b[1]) / 2 + 2), b, 8)
        L.pintar(L.m_linea(arco, 2.6), QUITINA_HONDA, 0.6, m, 0.95)
        L.pintar(L.m_linea([(x - 2, y + 0.8) for x, y in arco], 1.6), QUITINA_LUZ, 0.5, m, 0.85)
    # crestas en sierra por arriba
    for (x, y, h) in ((146, 120, 10), (162, 120, 14), (178, 132, 13), (188, 150, 11), (191, 172, 8)):
        L.forma([(x - 5, y + 3 + dy), (x + 4, y - h + dy), (x + 6, y + 4 + dy)], QUITINA_OSC, QUITINA, QUITINA_HONDA, 1.5, 0.6, 1.1)
    # el saco que brilla: ranura de panal por debajo
    ranura = [(144, 176), (158, 172), (174, 182), (180, 202), (172, 214), (158, 198)]
    ranura = [(x, y + dy) for x, y in ranura]
    L.pintar(L.m_poli(ranura), SACO_HALO, 3.0, None, 0.45)
    mr = L.forma(ranura, SACO_OSC, None, None, borde=1.2)
    for k, (cx, cy) in enumerate(((152, 180), (160, 182), (168, 186), (174, 194), (162, 192), (168, 200),
                                  (176, 204), (156, 188), (172, 210))):
        cy += dy
        hexa = [(cx - 3.6, cy), (cx - 1.8, cy - 3.2), (cx + 1.8, cy - 3.2), (cx + 3.6, cy), (cx + 1.8, cy + 3.2), (cx - 1.8, cy + 3.2)]
        L.pintar(L.m_poli(hexa), SACO_LUZ if k % 3 == 0 else SACO, 0, mr)
    L.pintar(L.m_elipse(164, 190 + dy, 9, 7), SACO_LUZ, 3.0, mr, 0.6)


def crestas(L, dy=0):
    """Pinchos de quitina que rompen la espalda de la chaqueta."""
    for (x, y, ang, h) in ((128, 94, -70, 14), (136, 104, -50, 16), (140, 120, -32, 15)):
        a = math.radians(ang)
        ux, uy = math.cos(a), math.sin(a)
        px, py = -uy, ux
        y += dy
        pts = [(x - px * 4.5, y - py * 4.5), (x + ux * h, y + uy * h), (x + px * 4.5, y + py * 4.5)]
        L.forma(pts, QUITINA, QUITINA_LUZ, QUITINA_OSC, 2.0, 0.6, 1.2)


# --- el traje -----------------------------------------------------------------------

def manga(L, hombro, codo, muneca, osc=False, semilla=3):
    """La manga de la chaqueta, el puno y la mano de MUTO: tres garfios largos."""
    base, luz, sombra = (TRAJE_OSC, TRAJE, TRAJE_HONDO) if osc else (TRAJE, TRAJE_LUZ, TRAJE_OSC)
    m = L.m_poli(tramo(hombro, codo, 8.0, 7.0))
    m = L.m_poli(tramo(codo, muneca, 7.0, 6.2), m)
    m = L.m_elipse(codo[0], codo[1], 7.0, 7.0, m)
    m = L.m_elipse(hombro[0], hombro[1], 8.0, 8.0, m)
    L.pintar(m, base)
    L.volumen(m, luz, sombra, 2.5, 1.2, 0.8, 0.95, honda=TRAJE_HONDO if not osc else None)
    L.pintar(L.m_linea([codo, ((codo[0] + muneca[0]) / 2 + 2, (codo[1] + muneca[1]) / 2)], 1.4), sombra, 0.4, m, 0.8)
    dx, dy = muneca[0] - codo[0], muneca[1] - codo[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    puno = (muneca[0] + ux * 3, muneca[1] + uy * 3)
    L.forma(tramo(muneca, puno, 6.4, 6.4), CAMISA, None, CAMISA_OSC, 2, 0.8, 1.1)
    # la mano: un nudo de quitina y tres garfios que se curvan hacia dentro
    qb, ql, qo = (QUITINA_OSC, QUITINA, QUITINA_HONDA) if osc else (QUITINA, QUITINA_LUZ, QUITINA_OSC)
    nudo = (puno[0] + ux * 4, puno[1] + uy * 4)
    L.forma([(nudo[0] - 6, nudo[1] - 3), (nudo[0] + 6, nudo[1] - 3), (nudo[0] + 5, nudo[1] + 4), (nudo[0] - 5, nudo[1] + 4)],
            qb, ql, qo, 1.8, 0.6, 1.2)
    lado = 1.0 if muneca[0] < 96 else -1.0
    for k, (ox, largo) in enumerate(((-4.5, 19), (0, 24), (4.5, 19))):
        a = (nudo[0] + ox, nudo[1] + 2)
        b = (a[0] - lado * 1 + ox * 0.3, a[1] + largo * 0.7)
        c = (a[0] + lado * 5 + ox * 0.3, a[1] + largo)
        curva = bez(a, b, c, 8)
        izq = [(x - 3.0 * (1 - i / 9.0), y) for i, (x, y) in enumerate(curva)]
        der = [(x + 3.0 * (1 - i / 9.0), y) for i, (x, y) in enumerate(curva)]
        L.forma(izq + der[::-1], ql, None, qo, 1.0, 0.4, 1.0)


def chaqueta(L, corbata, dy=0):
    def D(pts):
        return [(x, y + dy) for x, y in pts]
    cuerpo = D([(48, 96), (62, 88), (74, 84), (100, 84), (116, 88), (132, 96), (138, 116), (140, 148), (136, 166),
                (112, 172), (84, 172), (62, 168), (50, 158), (46, 126)])
    m = L.forma(cuerpo, TRAJE, TRAJE_LUZ, TRAJE_OSC, 4, 2.0, 1.5, honda=TRAJE_HONDO)
    # pliegues y costuras
    L.pintar(L.m_linea(D(bez((122, 100), (128, 130), (124, 166))), 2.0), TRAJE_OSC, 1.0, m, 0.9)
    L.pintar(L.m_linea(D(bez((58, 112), (54, 136), (60, 162))), 1.6), TRAJE_OSC, 1.0, m, 0.7)
    L.pintar(L.m_linea(D([(56, 150), (72, 154)]), 1.2), TRAJE_LUZ, 0.6, m, 0.5)
    # la camisa en V
    camisa = D([(72, 84), (100, 84), (88, 140)])
    L.forma(camisa, CAMISA, None, CAMISA_OSC, 3, 1.2, 1.1)
    # la corbata
    col, luz, osc = corbata
    L.forma(D([(83, 86), (93, 86), (91, 95), (85, 95)]), col, luz, osc, 1.5, 0.6, 1.1)
    L.forma(D([(85, 95), (91, 95), (95, 132), (89, 141), (83, 132)]), col, luz, osc, 2.5, 0.8, 1.1)
    # las solapas
    for pts in (D([(62, 86), (73, 84), (88, 138), (80, 136), (68, 112), (56, 104)]),
                D([(112, 86), (100, 84), (88, 138), (96, 134), (108, 112), (120, 102)])):
        L.forma(pts, TRAJE, TRAJE_LUZ, TRAJE_OSC, 2.5, 1.0, 1.2)
    # bolsillos y botones
    for a, b in (((106, 146), (126, 144)), ((58, 146), (72, 148)), ((108, 112), (122, 110))):
        L.linea(D([a, b]), TRAJE_HONDO, 1.1)
        L.linea(D([(a[0], a[1] + 1.2), (b[0], b[1] + 1.2)]), TRAJE_LUZ, 0.6)
    for y in (148, 160):
        L.elipse(89, y + dy, 2.0, 2.0, BOTON, 0.8)


# --- el monstruo entero --------------------------------------------------------------

POSES = dict(
    suelo=dict(
        dy=0,
        patas=dict(tra_lejos=((156, 132), (166, 96), (158, 196), (148, 248)),
                   tra_cerca=((176, 140), (188, 102), (186, 192), (176, 250)),
                   del_lejos=((110, 166), (128, 194), (112, 226), (122, 250)),
                   del_cerca=((70, 166), (40, 192), (56, 226), (44, 250))),
        mangas=(((132, 102), (146, 128), (142, 152)), ((50, 102), (38, 130), (42, 154)))),
    vuelo=dict(
        dy=-6,
        patas=dict(tra_lejos=((150, 160), (162, 184), (152, 212), (162, 236)),
                   tra_cerca=((164, 164), (184, 190), (174, 220), (186, 244)),
                   del_lejos=((110, 164), (122, 192), (110, 220), (120, 244)),
                   del_cerca=((70, 164), (54, 192), (64, 222), (54, 246))),
        mangas=(((132, 102), (150, 120), (160, 134)), ((50, 102), (30, 116), (20, 130)))),
)


def dibujar(cara, pose='suelo', corbata=CORBATA_AZUL):
    P = POSES[pose]
    dy = P['dy']
    L = lienzo()
    pt = P['patas']
    (mh, mc, mm), (fh, fc, fm) = P['mangas']
    sube = (lambda q: [(x, y + dy) for x, y in q])
    pata(L, *sube(pt['tra_lejos']), osc=True, semilla=21)
    manga(L, (mh[0], mh[1] + dy), (mc[0], mc[1] + dy), (mm[0], mm[1] + dy), osc=True)
    abdomen(L, dy)
    pata(L, *sube(pt['tra_cerca']), semilla=31)
    pata(L, *sube(pt['del_lejos']), osc=True, semilla=41)
    pata(L, *sube(pt['del_cerca']), semilla=51)
    crestas(L, dy)
    chaqueta(L, corbata, dy)
    # la cabeza, pintada a la misma resolucion de trabajo
    c = dict(cara)
    if pose == 'vuelo':
        c['ala'] = c.get('ala', 1.0)
        c['orejas'] = c.get('orejas', 1.2)
    kh = K * ESCALA_CABEZA
    H = CAB.lienzo(c, kh)
    x = int(round((CABEZA[0] - CAB.LIENZO[2] * ESCALA_CABEZA) * K))
    y = int(round((CABEZA[1] + dy + (10 if pose == 'vuelo' else 0) - CAB.LIENZO[3] * ESCALA_CABEZA) * K))
    L.im.alpha_composite(H.im, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))
    manga(L, (fh[0], fh[1] + dy), (fc[0], fc[1] + dy), (fm[0], fm[1] + dy))
    im = L.im.resize((CELDA_W, CELDA_H), Image.LANCZOS)
    return CAB.pixelar(im, 64)


def _fuente(t):
    try:
        return ImageFont.load_default(size=t)
    except TypeError:
        return ImageFont.load_default()


def lamina_diseno(salida):
    C = CAB.CARAS
    props = [
        ('serio', dibujar(C['serio'])),
        ('pillo', dibujar(C['pillo'])),
        ('enfado', dibujar(C['enfado'], corbata=CORBATA_ROJA)),
        ('vuela (orejas-alas)', dibujar(C['furia'], 'vuelo', corbata=CORBATA_ROJA)),
    ]
    k = 3
    W, H = CELDA_W * k, CELDA_H * k
    lam = Image.new('RGBA', (W * len(props) + 16 * (len(props) + 1), H + 40), (60, 62, 68, 255))
    d = ImageDraw.Draw(lam)
    f = _fuente(18)
    for i, (txt, im) in enumerate(props):
        x = 16 + i * (W + 16)
        lam.alpha_composite(im.resize((W, H), Image.NEAREST), (x, 34))
        d.text((x, 8), txt, fill=(255, 230, 0, 255), font=f)
    lam.save(salida)
    print(salida, lam.size)


def lamina_caras(salida):
    """El estudio de la cabeza: a la escala del sprite (x4) y a 2x (x3)."""
    nombres = ['serio', 'pillo', 'enfado', 'calculador', 'furia', 'susto']
    f = _fuente(16)
    w0, h0 = CAB.LIENZO[0], CAB.LIENZO[1]
    filas = []
    for esc, zoom in ((ESCALA_CABEZA, 4), (1.2, 3)):
        filas.append([(n, esc, CAB.retrato(CAB.CARAS[n], esc).resize((int(round(w0 * esc)) * zoom, int(round(h0 * esc)) * zoom),
                                                                     Image.NEAREST)) for n in nombres])
    W = max(sum(im.size[0] + 10 for _, _, im in fila) for fila in filas) + 10
    H = sum(fila[0][2].size[1] + 24 for fila in filas) + 10
    lam = Image.new('RGBA', (W, H), (60, 62, 68, 255))
    d = ImageDraw.Draw(lam)
    y = 4
    for fila in filas:
        x = 10
        for n, esc, im in fila:
            d.text((x, y), '%s  (%.2f px/u)' % (n, esc), fill=(255, 230, 0), font=f)
            lam.alpha_composite(im, (x, y + 20))
            x += im.size[0] + 10
        y += fila[0][2].size[1] + 24
    lam.save(salida)
    print(salida, lam.size)


if __name__ == '__main__':
    lamina_diseno(os.path.join(AQUI, 'nefanyamuto_diseno.png'))
    if '--caras' in sys.argv:
        lamina_caras(os.path.join(AQUI, 'nefanyamuto_caras.png'))
