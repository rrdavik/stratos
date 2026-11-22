"""
=============================================================================
ESTRATOS - NEFANYAMUTO: EL DISENO (y luego el atlas de emociones)
=============================================================================
No lo carga TouchDesigner: se corre fuera, con Pillow:

    python3 sprites/hacer_atlas_nefanyamuto.py            # la lamina de diseno

NefanyaMuto: la cabeza caricaturizada (calva con canas peinadas hacia atras,
cejas pesadas, ojeras, la nariz grande, papada) sobre un cuerpo de MUTO de 8 bits:
el torso con chaqueta, camisa y corbata, las mangas que acaban en garfios de
quitina, cuatro patas largas de insecto con las rodillas altas, el caparazon
anguloso y el saco naranja que brilla bajo la tripa.

Mismo formato de celda que Trumpzilla y Godzilla (192 x 256, mirando a la
izquierda, los pies abajo); se dibuja a S veces el tamano, se reduce, se pasa a
una paleta corta (el aire de 8 bits) y lleva el recorte duro del shader.
=============================================================================
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
CELDA_W, CELDA_H = 192, 256
S = 4

TINTA = (22, 18, 24, 255)
# la cara
PIEL = (234, 184, 156, 255)
PIEL_LUZ = (248, 212, 186, 255)
PIEL_OSC = (204, 142, 118, 255)
PIEL_SOMBRA = (164, 104, 90, 255)
MEJILLA = (226, 160, 138, 255)
LABIO = (176, 96, 92, 255)
CANA = (206, 208, 214, 255)
CANA_LUZ = (240, 241, 245, 255)
CANA_OSC = (140, 142, 152, 255)
CEJA = (78, 74, 80, 255)
OJO_BLANCO = (244, 240, 232, 255)
PUPILA = (40, 46, 56, 255)
OJO_ROJO = (255, 70, 40, 255)
# el traje
TRAJE = (34, 40, 72, 255)
TRAJE_LUZ = (58, 68, 112, 255)
TRAJE_OSC = (20, 24, 46, 255)
CAMISA = (240, 242, 246, 255)
CAMISA_OSC = (190, 196, 210, 255)
CORBATA = (40, 96, 210, 255)
CORBATA_OSC = (24, 60, 150, 255)
CORBATA_ROJA = (210, 30, 40, 255)
CORBATA_ROJA_OSC = (140, 16, 26, 255)
# el MUTO
QUITINA = (84, 76, 72, 255)
QUITINA_LUZ = (128, 116, 106, 255)
QUITINA_OSC = (52, 46, 46, 255)
QUITINA_FONDO = (40, 36, 38, 255)
SACO = (240, 116, 28, 255)
SACO_LUZ = (255, 204, 84, 255)
SACO_OSC = (150, 46, 18, 255)
SACO_HALO = (255, 236, 150, 255)


class Lienzo(object):
    """Dibuja en coordenadas de la celda (192 x 256) sobre un lienzo S veces mayor."""

    def __init__(self):
        self.im = Image.new('RGBA', (CELDA_W * S, CELDA_H * S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poli(self, pts, fill, borde=1.4):
        pts = self.P(pts)
        if borde > 0:
            self.d.polygon(pts, fill=fill, outline=TINTA, width=max(1, int(borde * S)))
        else:
            self.d.polygon(pts, fill=fill)

    def elipse(self, cx, cy, rx, ry, fill, borde=1.4):
        caja = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        if borde > 0:
            self.d.ellipse(caja, fill=fill, outline=TINTA, width=max(1, int(borde * S)))
        else:
            self.d.ellipse(caja, fill=fill)

    def linea(self, pts, col=TINTA, ancho=1.4):
        self.d.line(self.P(pts), fill=col, width=max(1, int(ancho * S)), joint='curve')

    def arco(self, cx, cy, rx, ry, a0, a1, col=TINTA, ancho=1.6):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
               for a in _rango(a0, a1, 16)]
        self.linea(pts, col, ancho)

    def final(self, pixel=1):
        """Reduce a la celda (pixel > 1: a la celda / pixel y vuelta, pixeles gordos),
        recorte duro y la paleta corta."""
        w, h = CELDA_W // pixel, CELDA_H // pixel
        im = self.im.resize((w, h), Image.LANCZOS)
        px = im.load()
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a < 128:
                    px[x, y] = (0, 0, 0, 0)
                else:
                    k = 255.0 / a
                    px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), 255)
        im = paletizar(im)
        if pixel > 1:
            im = im.resize((CELDA_W, CELDA_H), Image.NEAREST)
        return im


PALETA = [v for k, v in sorted(globals().items()) if isinstance(v, tuple) and len(v) == 4 and k.isupper()]


def paletizar(im):
    """Cada pixel opaco al color mas cercano de la paleta (sin tramado): el aire de 8 bits."""
    pal = [c[:3] for c in PALETA]
    cache = {}
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            c = cache.get((r, g, b))
            if c is None:
                c = min(pal, key=lambda p: (p[0] - r) ** 2 * 3 + (p[1] - g) ** 2 * 4 + (p[2] - b) ** 2 * 2)
                cache[(r, g, b)] = c
            px[x, y] = c + (255,)
    return im


def _rango(a0, a1, n):
    return [a0 + (a1 - a0) * k / float(n) for k in range(n + 1)]


def _bez(p0, p1, p2, n=10):
    out = []
    for k in range(n + 1):
        t = k / float(n)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


def _mov(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


# --- el MUTO ------------------------------------------------------------------------

def segmento(L, a, b, g0, g1, col, borde=1.3):
    """Un tramo de pata de insecto: un trapecio de a (grosor g0) a b (g1)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1.0
    px, py = -dy / n, dx / n
    L.poli([(a[0] + px * g0, a[1] + py * g0), (b[0] + px * g1, b[1] + py * g1),
            (b[0] - px * g1, b[1] - py * g1), (a[0] - px * g0, a[1] - py * g0)], col, borde)


def pata(L, cadera, rodilla, tobillo, pie, osc=False):
    """Pata de MUTO: el muslo sube desde el cuerpo a una rodilla alta y angulosa, la
    tibia larga baja hasta el tobillo y acaba en una cuchilla que se curva en garfio."""
    col = QUITINA_OSC if osc else QUITINA
    luz = QUITINA if osc else QUITINA_LUZ
    segmento(L, cadera, rodilla, 7.0, 5.2, col)
    segmento(L, rodilla, tobillo, 5.2, 3.8, col)
    # la cuchilla: del tobillo al pie, con la punta doblada hacia dentro (hacia el cuerpo)
    dx, dy = pie[0] - tobillo[0], pie[1] - tobillo[1]
    n = math.hypot(dx, dy) or 1.0
    px = -1.0 if pie[0] > 96 else 1.0
    gancho = (pie[0] + px * 6, pie[1] - 7)
    L.poli([(tobillo[0] - 3.8, tobillo[1]), (tobillo[0] + 3.8, tobillo[1]), (pie[0] + 1.2, pie[1] - 6),
            (pie[0], pie[1]), gancho, (pie[0] - 1.2, pie[1] - 7)], col, 1.2)
    for p, r in ((rodilla, 6.0), (tobillo, 4.6)):
        L.poli([(p[0] - r, p[1]), (p[0], p[1] - r * 1.1), (p[0] + r, p[1]), (p[0], p[1] + r)], col, 1.2)
    # la espuela de la rodilla, hacia arriba
    L.poli([(rodilla[0] - 3, rodilla[1] - 3), (rodilla[0] + 1, rodilla[1] - 15), (rodilla[0] + 4, rodilla[1] - 2)], col, 1.0)
    L.linea([_lerp(cadera, rodilla, 0.12), _lerp(cadera, rodilla, 0.85)], luz, 1.4)
    L.linea([_lerp(rodilla, tobillo, 0.1), _lerp(rodilla, tobillo, 0.85)], luz, 1.0)


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def caparazon(L, alas):
    """El abdomen anguloso de placas, que cae hacia atras, con las crestas; y el
    saco que brilla por debajo como un panal."""
    if alas:
        # alas plegadas hacia atras y arriba: membrana oscura con nervios y borde rojizo
        for dx, col in ((10, QUITINA_FONDO), (0, QUITINA_OSC)):
            ala = [(104, 108), (138 + dx, 40), (160 + dx, 22), (172 + dx, 48), (186, 98), (168, 132), (126, 128)]
            L.poli(ala, col, 1.2)
        for q in ((160, 22), (172, 48), (184, 96)):
            L.linea([(116, 116), q], QUITINA_FONDO, 1.1)
        L.linea([(160, 24), (172, 48), (185, 96)], SACO_OSC, 1.2)
    abd = [(96, 114), (122, 100), (154, 102), (178, 118), (188, 142), (186, 166), (176, 196), (160, 178),
           (134, 176), (110, 168)]
    L.poli(abd, QUITINA)
    # las placas: arcos que se solapan, de la cintura a la punta
    for k, t in enumerate((0.18, 0.4, 0.62, 0.82)):
        x = 110 + t * 76
        L.linea(_bez((x - 8, 104 + t * 14), (x + 6, 140), (x - 6, 172 + t * 10), 8), QUITINA_OSC, 1.5)
        L.linea(_bez((x - 5, 108 + t * 14), (x + 8, 140), (x - 3, 168 + t * 10), 8), QUITINA_LUZ, 0.9)
    L.linea([(124, 103), (154, 105), (176, 121)], QUITINA_LUZ, 1.6)
    # crestas de la espalda, en sierra
    for (x, y, h) in ((112, 106, 10), (128, 100, 15), (146, 101, 17), (163, 109, 14), (178, 122, 11)):
        L.poli([(x - 6, y + 3), (x + 4, y - h), (x + 6, y + 3)], QUITINA_OSC, 1.1)
    # el saco: una ranura de panal naranja entre las placas de abajo
    L.poli([(112, 166), (128, 160), (160, 162), (176, 172), (150, 186), (122, 184)], SACO_OSC, 1.4)
    for k, (cx, cy) in enumerate(((124, 172), (132, 168), (140, 174), (148, 168), (156, 174), (164, 172),
                                  (130, 178), (146, 179), (138, 166))):
        L.poli([(cx - 3.6, cy), (cx - 1.8, cy - 3.2), (cx + 1.8, cy - 3.2), (cx + 3.6, cy), (cx + 1.8, cy + 3.2),
                (cx - 1.8, cy + 3.2)], SACO_LUZ if k % 3 == 0 else SACO, 0.7)


def brazo(L, hombro, codo, mano, osc=False):
    """La manga de la chaqueta, el puno blanco y la guadana de quitina que cuelga
    con la punta en garfio (como las patas delanteras del MUTO)."""
    col = TRAJE_OSC if osc else TRAJE
    segmento(L, hombro, codo, 7.5, 6.5, col)
    L.elipse(hombro[0], hombro[1], 7.5, 7.5, col)
    segmento(L, codo, mano, 6.5, 5.5, col)
    L.elipse(codo[0], codo[1], 6.4, 6.4, col)
    if not osc:
        L.linea([_lerp(hombro, codo, 0.1), _lerp(hombro, codo, 0.8)], TRAJE_LUZ, 1.6)
        L.linea([_lerp(codo, mano, 0.2), _lerp(codo, mano, 0.8)], TRAJE_LUZ, 1.2)
    dx, dy = mano[0] - codo[0], mano[1] - codo[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    puno = (mano[0] + ux * 3, mano[1] + uy * 3)
    segmento(L, mano, puno, 5.6, 5.6, CAMISA, 1.1)
    # la guadana: un tramo grueso y la cuchilla larga que se dobla en garfio hacia atras
    a = puno
    b = (a[0] + ux * 10, a[1] + uy * 10)
    segmento(L, a, b, 4.6, 3.6, QUITINA_OSC if osc else QUITINA, 1.2)
    L.poli([(b[0] - 4.2, b[1]), (b[0] + 4.2, b[1]), (b[0] + 3, b[1] + 26), (b[0] + 12, b[1] + 30),
            (b[0] + 14, b[1] + 26), (b[0] + 12, b[1] + 36), (b[0] - 1, b[1] + 33), (b[0] - 4, b[1] + 24)],
           QUITINA_LUZ if not osc else QUITINA, 1.2)
    L.linea([(b[0], b[1] + 2), (b[0] + 1, b[1] + 28)], QUITINA_OSC, 1.0)


def torso(L, corbata):
    """El torso del traje: la chaqueta, las solapas, la camisa y la corbata."""
    chaqueta = [(30, 114), (52, 100), (92, 100), (110, 114), (112, 150), (96, 164), (54, 164), (34, 148)]
    L.poli(chaqueta, TRAJE)
    L.linea([(98, 104), (106, 152)], TRAJE_OSC, 1.6)
    # la camisa en V y las solapas
    L.poli([(48, 100), (80, 100), (66, 136)], CAMISA, 1.1)
    L.poli([(44, 101), (62, 101), (64, 132), (50, 118), (54, 112)], TRAJE_LUZ, 1.1)
    L.poli([(84, 101), (68, 101), (67, 132), (80, 118), (76, 112)], TRAJE_LUZ, 1.1)
    # la corbata
    col, osc = corbata
    L.poli([(61, 100), (69, 100), (68, 107), (62, 107)], col, 1.1)
    L.poli([(62, 107), (68, 107), (71, 130), (65, 136), (59, 130)], col, 1.1)
    L.linea([(66, 110), (67, 128)], osc, 1.0)
    # botones
    for y in (142, 152):
        L.elipse(70, y, 1.8, 1.8, TRAJE_OSC, 0.8)


# --- la cabeza ---------------------------------------------------------------------

def cabeza(L, cara, c=(64, 58)):
    """La caricatura, casi de frente, un poco girada hacia la izquierda."""
    cx, cy = c

    def T(pts):
        return [(cx + x, cy + y) for x, y in pts]

    # el cuello de la camisa (debajo de la papada)
    L.poli(T([(-20, 38), (-2, 50), (16, 38), (18, 50), (-1, 54), (-22, 50)]), CAMISA, 1.2)
    # orejas grandes
    for sx in (-1, 1):
        ox = 31 if sx > 0 else -33
        L.elipse(cx + ox, cy + 2, 7.5, 12.5, PIEL)
        L.arco(cx + ox, cy + 2, 4, 7.5, 200 if sx < 0 else -20, 340 if sx < 0 else 160, PIEL_SOMBRA, 1.2)
    # la masa de pelo: gris, peinada hacia atras, mas abultada detras y arriba
    pelo = T(_bez((-33, -2), (-38, -30), (-18, -42)) + _bez((-18, -42), (4, -50), (26, -42))
             + _bez((26, -42), (38, -32), (33, -2)) + [(28, 4), (-28, 4)])
    L.poli(pelo, CANA)
    L.poli(T(_bez((20, -40), (36, -30), (32, 0)) + [(24, 2), (26, -26)]), CANA_OSC, 0)
    # la cara: frente alta, mofletes, papada ancha que cae, barbilla cuadrada
    cara_pts = T(_bez((-28, -16), (-32, 4), (-30, 20)) + _bez((-30, 20), (-31, 36), (-20, 44))
                 + _bez((-20, 44), (-6, 52), (8, 50)) + _bez((8, 50), (24, 44), (27, 32))
                 + _bez((27, 32), (30, 16), (27, -2)) + _bez((27, -2), (27, -12), (24, -18))
                 # las entradas: la frente sube mucho por los lados y deja un pico en medio
                 + [(22, -26), (16, -32), (10, -33), (4, -36), (-2, -34), (-8, -34), (-16, -32), (-22, -28), (-26, -22)])
    L.poli(cara_pts, PIEL)
    # el pelo de las sienes, corto y por encima de la oreja
    L.poli(T([(-29, 4), (-32, -14), (-27, -22), (-25, -12), (-26, -2)]), CANA, 1.1)
    L.poli(T([(26, 2), (29, -12), (24, -20), (22, -10), (23, -2)]), CANA, 1.1)
    # mechas del peinado, hacia atras (a la derecha y arriba)
    for a, b, q in (((-10, -36), (0, -44), (16, -44)), ((-20, -32), (-18, -40), (-4, -44)),
                    ((2, -37), (14, -42), (26, -36)), ((-26, -24), (-28, -34), (-18, -40))):
        L.linea(T(_bez(a, b, q, 6)), CANA_OSC, 1.1)
    L.linea(T(_bez((-14, -40), (0, -47), (14, -46), 6)), CANA_LUZ, 1.8)
    # la frente: brillo y arrugas
    L.linea(T(_bez((-8, -28), (0, -31), (8, -28), 6)), PIEL_LUZ, 2.0)
    arr = cara.get('arrugas', 1.0)
    for k in range(3):
        y = -24 + k * 4.5
        w = 12 - k * 2
        L.linea(T(_bez((-w - 2, y), (-1, y - 1.5 * arr), (w, y), 6)), PIEL_OSC, 1.0)
    # la mitad derecha en sombra (la luz viene de la izquierda) y la sombra de los mofletes
    L.poli(T(_bez((26, -6), (30, 16), (26, 32)) + _bez((26, 32), (22, 42), (10, 48)) + [(14, 40), (20, 24), (21, 2)]),
           PIEL_OSC, 0)
    L.linea(T(_bez((-28, 16), (-29, 34), (-18, 42), 6)), PIEL_OSC, 2.8)
    L.linea(T(_bez((24, 16), (26, 32), (18, 42), 6)), PIEL_OSC, 2.4)
    L.linea(T(_bez((-14, 46), (0, 49), (12, 45), 6)), PIEL_OSC, 1.4)       # pliegue de la barbilla
    L.linea(T(_bez((-22, 34), (-20, 40), (-14, 42), 4)), PIEL_SOMBRA, 1.0)  # el pliegue de la papada
    L.linea(T(_bez((20, 32), (18, 38), (12, 41), 4)), PIEL_SOMBRA, 1.0)
    ojos(L, T, cara)
    nariz(L, T, cara)
    boca(L, T, cara)


def ojos(L, T, cara):
    tipo = cara.get('ojo', 'normal')
    ceja = cara.get('ceja', 0.0)           # + enfado (baja por dentro), - triste (sube por dentro)
    rojo = cara.get('ojo_rojo', False)
    for sx, ex in ((-1, -13), (1, 11)):
        ey = -6
        # ojeras
        L.arco(T([(ex, ey + 4)])[0][0], T([(ex, ey + 4)])[0][1], 6.5, 3.5, 20, 160, PIEL_SOMBRA, 1.3)
        L.arco(T([(ex, ey + 6)])[0][0], T([(ex, ey + 6)])[0][1], 6.0, 3.5, 30, 150, PIEL_OSC, 1.0)
        p = T([(ex, ey)])[0]
        if tipo in ('normal', 'enfado', 'triste'):
            # el ojo pequeno bajo el parpado pesado
            L.elipse(p[0], p[1], 5.2, 3.2, OJO_BLANCO, 1.0)
            L.elipse(p[0] - 1.0, p[1] + 0.4, 2.2, 2.6, OJO_ROJO if rojo else PUPILA, 0)
            L.poli([(p[0] - 6, p[1] - 0.6), (p[0] - 3, p[1] - 3.6), (p[0] + 3, p[1] - 3.6), (p[0] + 6, p[1] - 0.6),
                    (p[0] + 6, p[1] - 2.6), (p[0] - 6, p[1] - 2.6)], PIEL_OSC, 0)
            L.linea([(p[0] - 6, p[1] - 0.8), (p[0] - 2, p[1] - 3.2), (p[0] + 3, p[1] - 3.2), (p[0] + 6, p[1] - 0.8)], TINTA, 1.2)
        elif tipo == 'grande':
            L.elipse(p[0], p[1] - 1, 6.5, 6.0, OJO_BLANCO, 1.2)
            L.elipse(p[0] - 1.0, p[1] - 1, 1.8, 1.8, PUPILA, 0)
        elif tipo == 'cerrado':
            L.arco(p[0], p[1] - 1.5, 5.5, 3.5, 20, 160, TINTA, 1.8)
        elif tipo == 'feliz':
            L.arco(p[0], p[1] + 1.5, 5.5, 3.5, 200, 340, TINTA, 1.8)
        # la ceja: gruesa, con la mitad de dentro mas baja si se enfada
        dentro = 4 if sx < 0 else -4
        fuera = -9 if sx < 0 else 9
        yi = ey - 8 + ceja * 3.0
        yo = ey - 10 - ceja * 1.0
        L.poli(T([(ex + dentro, yi), (ex + fuera, yo), (ex + fuera, yo + 3.2), (ex + dentro, yi + 3.6)]), CEJA, 1.0)
    if ceja > 0.5:
        L.linea(T([(-2, -15), (-1, -9)]), PIEL_SOMBRA, 1.2)        # el entrecejo


def nariz(L, T, cara):
    # la nariz grande, carnosa, que cae un poco hacia la izquierda
    L.poli(T([(-3, -10), (2, -10), (5, 6), (7, 12), (-1, 16), (-11, 13), (-9, 6)]), PIEL, 0)
    L.linea(T([(2, -9), (5, 5)]), PIEL_OSC, 1.2)
    L.elipse(*T([(-3, 11)])[0], 8.0, 6.0, PIEL, 0)
    L.arco(*T([(-3, 11)])[0], 8.0, 6.0, -40, 220, TINTA, 1.3)
    L.elipse(*T([(-5, 9)])[0], 2.6, 1.8, PIEL_LUZ, 0)
    L.elipse(*T([(-7, 14)])[0], 1.8, 1.2, PIEL_SOMBRA, 0)
    L.elipse(*T([(1, 14)])[0], 1.8, 1.2, PIEL_SOMBRA, 0)
    # los surcos de la nariz a la boca, muy marcados
    L.linea(T(_bez((-12, 12), (-17, 20), (-15, 28), 6)), PIEL_SOMBRA, 1.4)
    L.linea(T(_bez((8, 12), (13, 20), (11, 28), 6)), PIEL_SOMBRA, 1.4)


def boca(L, T, cara):
    abre = cara.get('boca', 0.0)
    sonr = cara.get('sonrisa', -0.6)          # de serie, las comisuras hacia abajo
    y = 29
    if abre > 0:
        # grita: la boca ancha con las comisuras hacia abajo, los dientes de arriba
        top = _bez((-12, y + 2 - sonr * 2), (-1, y - 3), (10, y + 2 - sonr * 2), 6)
        bot = _bez((10, y + 2 - sonr * 2), (8, y + abre * 1.8), (-1, y + abre * 2.0), 3) + \
              _bez((-1, y + abre * 2.0), (-10, y + abre * 1.8), (-12, y + 2 - sonr * 2), 3)
        L.poli(T(top + bot), (90, 24, 30, 255), 1.4)
        L.poli(T([(-8, y - 0.5), (6, y - 0.5), (6, y + 2.5), (-8, y + 2.5)]), OJO_BLANCO, 0)
        L.poli(T([(-6, y + abre * 1.5), (4, y + abre * 1.5), (2, y + abre * 1.9 - 1), (-4, y + abre * 1.9 - 1)]),
               (200, 90, 100, 255), 0)
        L.poli(T([(-7, y + abre * 1.7 - 2.5), (5, y + abre * 1.7 - 2.5), (5, y + abre * 1.7), (-7, y + abre * 1.7)]),
               CAMISA_OSC, 0)
    else:
        lab = _bez((-12, y + 1 - sonr * 3), (-1, y - 1 + sonr * 1.5), (10, y + 1 - sonr * 3), 6)
        L.linea(T(lab), LABIO, 2.4)
        L.linea(T(lab), TINTA, 1.0)
        L.linea(T(_bez((-7, y + 4), (-1, y + 5), (5, y + 4), 4)), PIEL_OSC, 1.2)     # el labio de abajo


# --- el monstruo entero --------------------------------------------------------------

PATAS = dict(
    # cadera, rodilla (alta, por encima del cuerpo), tobillo, pie
    del_cerca=((46, 148), (10, 108), (8, 196), (18, 250)),
    del_lejos=((84, 150), (104, 94), (78, 190), (62, 248)),
    tra_cerca=((160, 150), (182, 72), (184, 180), (168, 250)),
    tra_lejos=((140, 146), (150, 70), (138, 184), (118, 248)),
)


def dibujar(cara, alas=False, corbata=(CORBATA, CORBATA_OSC), pixel=1):
    L = Lienzo()
    pata(L, *PATAS['tra_lejos'], osc=True)
    pata(L, *PATAS['del_lejos'], osc=True)
    caparazon(L, alas)
    pata(L, *PATAS['tra_cerca'])
    torso(L, corbata)
    pata(L, *PATAS['del_cerca'])
    cabeza(L, cara)
    brazo(L, (38, 116), (26, 140), (34, 160))
    return L.final(pixel)


CARAS = dict(
    serio=dict(ceja=0.6, sonrisa=-0.7),
    enfado=dict(ceja=1.6, boca=7, sonrisa=-1.0, ojo_rojo=True),
)


def lamina_diseno(salida):
    """Las propuestas, lado a lado y a 3x (pixel a pixel) sobre gris."""
    props = [
        ('A  traje, corbata azul', dibujar(CARAS['serio'])),
        ('A  enfado', dibujar(CARAS['enfado'], corbata=(CORBATA_ROJA, CORBATA_ROJA_OSC))),
        ('B  con alas (MUTO macho)', dibujar(CARAS['serio'], alas=True)),
        ('C  pixel gordo (x2)', dibujar(CARAS['serio'], pixel=2)),
    ]
    k = 3
    W, H = CELDA_W * k, CELDA_H * k
    lam = Image.new('RGBA', (W * len(props) + 16 * (len(props) + 1), H + 40), (60, 62, 68, 255))
    d = ImageDraw.Draw(lam)
    try:
        f = ImageFont.load_default(size=18)
    except TypeError:
        f = ImageFont.load_default()
    for i, (txt, im) in enumerate(props):
        x = 16 + i * (W + 16)
        lam.alpha_composite(im.resize((W, H), Image.NEAREST), (x, 34))
        d.text((x, 8), txt, fill=(255, 230, 0, 255), font=f)
    lam.save(salida)
    print(salida, lam.size)


if __name__ == '__main__':
    lamina_diseno(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'nefanyamuto_diseno.png'))
