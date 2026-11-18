"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DE GODZILLA (fase 40)
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/godzilla_emociones.png (y la lamina de prueba) con Pillow:

    python3 sprites/hacer_atlas_godzilla.py

Godzilla es el monstruo de la creacion: el reverso de Trumpzilla. Un saurio verde
de pie, con la espalda de placas en forma de hoja (lo que crea) y la tripa clara.
Se dibuja con formas (sin imagenes de origen), a 4 veces el tamano y reducido,
con el recorte duro que espera el shader (alfa 0 o 1).

Mismo formato que el atlas de Trumpzilla (sprites/trumpzilla_emociones.png):
4 x 3 celdas de 192 x 256, las caras en el orden de EMOCIONES_MON del motor, de
arriba a la izquierda; todas miran a la izquierda de la imagen, con los pies
abajo y centrados, a la misma altura. Asi el mismo shader (mat_sprite) sirve
para los dos monstruos.

  serio      de pie, la boca cerrada (aparece, quieto)
  enfado     ruge, las garras delante (busca y anda)
  furia      ruge con la boca abierta y las placas encendidas (grande; la lucha)
  rie        sonrie y le brotan hojas (crea)
  carcajada  se rie con la boca abierta y lagrimas de risa (crea, grande)
  susto      los ojos muy abiertos y gotas de sudor
  mueca      encaja un manotazo: el ojo apretado y estrellas (la lucha)
  llora      lagrimas
  panico     los brazos arriba
  calma      los ojos cerrados, saluda con una flor (se va)
=============================================================================
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
CELDA_W, CELDA_H = 192, 256
COLS, FILAS = 4, 3
S = 4                           # supermuestreo
EMOCIONES = ['serio', 'enfado', 'furia', 'rie', 'carcajada', 'susto', 'mueca', 'llora', 'panico', 'calma']

TINTA = (16, 34, 22, 255)
PIEL = (46, 112, 64, 255)
PIEL_OSC = (30, 78, 44, 255)
PIEL_CLARA = (78, 150, 84, 255)
TRIPA = (196, 206, 140, 255)
TRIPA_OSC = (160, 172, 108, 255)
PLACA = (176, 226, 132, 255)
PLACA_OSC = (110, 172, 90, 255)
PLACA_LUZ = (236, 255, 150, 255)
HALO = (250, 255, 190, 255)
GARRA = (236, 230, 214, 255)
DIENTE = (250, 248, 238, 255)
BOCA = (96, 22, 30, 255)
LENGUA = (214, 92, 106, 255)
OJO = (252, 236, 150, 255)
OJO_FURIA = (255, 170, 60, 255)
PUPILA = (20, 16, 12, 255)
AGUA = (120, 200, 255, 255)
ESTRELLA = (255, 226, 80, 255)
FLOR = (250, 120, 170, 255)
FLOR_C = (255, 220, 90, 255)
HOJA = (120, 200, 90, 255)


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

    def final(self):
        im = self.im.resize((CELDA_W, CELDA_H), Image.LANCZOS)
        px = im.load()
        for y in range(CELDA_H):
            for x in range(CELDA_W):
                r, g, b, a = px[x, y]
                if a < 128:
                    px[x, y] = (0, 0, 0, 0)
                else:
                    k = 255.0 / a
                    px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), 255)
        return im


def _rango(a0, a1, n):
    return [a0 + (a1 - a0) * k / float(n) for k in range(n + 1)]


def _rot(p, c, ang):
    a = math.radians(ang)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def _bezier(p0, p1, p2, n=10):
    out = []
    for k in range(n + 1):
        t = k / float(n)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


# --- las partes ---------------------------------------------------------------

def placa(L, base, normal, largo, ancho, col, borde=1.2):
    """Una placa dorsal en forma de hoja dentada: sale de base hacia normal."""
    nx, ny = normal
    tx, ty = -ny, nx
    bx, by = base
    pts = []
    perfil = [(0.0, -1.0), (0.30, -0.95), (0.38, -0.55), (0.62, -0.62), (0.70, -0.28), (1.0, 0.0),
              (0.70, 0.28), (0.62, 0.62), (0.38, 0.55), (0.30, 0.95), (0.0, 1.0)]
    for u, v in perfil:
        pts.append((bx + nx * u * largo + tx * v * ancho * 0.5, by + ny * u * largo + ty * v * ancho * 0.5))
    L.poli(pts, col, borde)
    L.linea([(bx, by), (bx + nx * largo * 0.85, by + ny * largo * 0.85)], PLACA_OSC, 0.9)


COLA_SUP = ((122, 132), (178, 176), (190, 238))
COLA_INF = ((186, 246), (142, 236), (114, 198))
ESPALDA = ((122, 78), (150, 136), (140, 200))


def espina():
    """Los puntos de la espalda (nuca, lomo y cola) con su normal hacia fuera y el
    tamano de su placa."""
    pts = [(100, 26), (112, 46)]
    pts += [_bezier(*ESPALDA, n=10)[k] for k in (1, 3, 5, 7)]
    pts += [_bezier(*COLA_SUP, n=10)[k] for k in (4, 6, 8, 9)]
    tam = [22, 30, 40, 46, 46, 42, 34, 26, 19, 13]
    out = []
    for k, q in enumerate(pts):
        a = pts[max(0, k - 1)]
        b = pts[min(len(pts) - 1, k + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        n = math.hypot(tx, ty)
        out.append((q, (ty / n, -tx / n), tam[k]))
    return out


def placas(L, brillo):
    col = PLACA_LUZ if brillo else PLACA
    for q, (nx, ny), t in espina():
        base = (q[0] - nx * 8, q[1] - ny * 8)
        if brillo:
            placa(L, base, (nx, ny), t * 1.3, t * 0.85, HALO, 0)
        placa(L, base, (nx, ny), t, t * 0.55, col)


def cola(L):
    L.poli(_bezier(*COLA_SUP, n=14) + _bezier(*COLA_INF, n=14), PIEL)
    L.linea(_bezier((122, 170), (160, 218), (186, 242), 10), PIEL_OSC, 1.2)
    for k in range(6):                  # anillos de escamas
        p = _bezier(*COLA_SUP, n=7)[k + 1]
        q = _bezier((COLA_INF[2]), (COLA_INF[1]), (COLA_INF[0]), n=7)[k + 1]
        L.linea(_bezier(p, ((p[0] + q[0]) / 2 - 4, (p[1] + q[1]) / 2 + 2), q, 6), PIEL_OSC, 0.9)


def pierna(L, x, y, osc=False):
    """El muslo, la pierna y el pie con tres garras hacia la izquierda; (x, y) la cadera."""
    col = PIEL_OSC if osc else PIEL
    L.poli(_bezier((x - 10, y + 30), (x - 16, y + 48), (x - 8, y + 52), 5)
           + [(x + 14, y + 52)] + _bezier((x + 14, y + 52), (x + 20, y + 36), (x + 16, y + 26), 5), col)
    L.elipse(x, y + 12, 25, 28, col)
    pie = (_bezier((x - 30, y + 58), (x - 30, y + 46), (x - 10, y + 46), 5)
           + _bezier((x + 10, y + 46), (x + 24, y + 48), (x + 20, y + 58), 5))
    L.poli(pie, col)
    for k in range(3):
        gx = x - 30 + k * 10
        L.poli([(gx + 2, y + 53), (gx - 7, y + 59), (gx + 5, y + 59)], GARRA, 1.0)
    if not osc:
        L.arco(x - 2, y + 10, 16, 18, 120, 240, PIEL_CLARA, 1.4)
        for k in range(3):
            L.arco(x + 4, y + 2 + k * 10, 10, 4, 200, 340, PIEL_OSC, 0.9)
        L.arco(x - 6, y + 44, 8, 3, 180, 360, PIEL_OSC, 0.9)


def cuerpo(L):
    pts = (_bezier((80, 90), (58, 140), (66, 200), 10) + _bezier((66, 200), (100, 226), (140, 200), 8)
           + _bezier(*ESPALDA[::-1], n=10) + _bezier((122, 78), (100, 66), (80, 90), 6))
    L.poli(pts, PIEL)
    L.linea(_bezier((128, 96), (144, 140), (136, 196), 8), PIEL_OSC, 2.2)
    tripa = (_bezier((80, 98), (62, 150), (74, 204), 10) + _bezier((74, 204), (90, 212), (104, 204), 4)
             + _bezier((104, 204), (108, 150), (98, 96), 10))
    L.poli(tripa, TRIPA, 1.0)
    for k in range(9):
        y = 108 + k * 11
        x0 = 70 + abs(y - 152) * 0.10
        L.linea(_bezier((x0, y), ((x0 + 102) / 2, y + 3), (102 - abs(y - 152) * 0.04, y), 4), TRIPA_OSC, 1.0)
    for y in (112, 136, 160):
        L.arco(124, y, 8, 5, 180, 330, PIEL_OSC, 0.9)


def cuello(L):
    L.poli(_bezier((76, 104), (68, 76), (66, 58), 6) + _bezier((104, 44), (118, 66), (122, 90), 6), PIEL, 0)
    L.linea(_bezier((78, 104), (68, 82), (64, 66), 6), TINTA, 1.4)
    for k in range(3):
        L.arco(96, 70 + k * 10, 10, 4, 190, 330, PIEL_OSC, 0.9)


def brazo(L, pose, osc=False):
    """El brazo (el hombro delante del cuerpo): abajo, delante, arriba, saluda,
    tripa, golpe o cubre (la cara)."""
    col = PIEL_OSC if osc else PIEL
    hx, hy = (100, 108) if osc else (86, 112)
    manos = dict(abajo=((70, 136), (58, 156)), delante=((62, 126), (40, 128)), arriba=((66, 96), (52, 72)),
                 saluda=((62, 100), (46, 78)), tripa=((68, 140), (86, 152)), golpe=((56, 108), (22, 100)),
                 cubre=((62, 96), (54, 64)))
    codo, mano = manos[pose]
    if osc:
        codo, mano = (codo[0] + 12, codo[1] - 4), (mano[0] + 14, mano[1] - 4)
    for a, b, g in (((hx, hy), codo, 9.5), (codo, mano, 7.5)):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy) or 1.0
        px, py = -dy / n * g, dx / n * g
        L.poli([(a[0] + px, a[1] + py), (b[0] + px * 0.8, b[1] + py * 0.8),
                (b[0] - px * 0.8, b[1] - py * 0.8), (a[0] - px, a[1] - py)], col)
        L.elipse(b[0], b[1], g * 0.9, g * 0.9, col)
    L.elipse(hx, hy, 10, 10, col)
    # tres garras, hacia donde apunta el antebrazo
    dx, dy = mano[0] - codo[0], mano[1] - codo[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = dx / n, dy / n
    for k in (-1, 0, 1):
        a = math.atan2(uy, ux) + k * 0.55
        bx, by = mano[0] + math.cos(a) * 5.5, mano[1] + math.sin(a) * 5.5
        L.poli([(bx - math.sin(a) * 2.4, by + math.cos(a) * 2.4), (bx + math.cos(a) * 8, by + math.sin(a) * 8),
                (bx + math.sin(a) * 2.4, by - math.cos(a) * 2.4)], GARRA, 0.9)
    return mano


def cabeza(L, cara):
    """El craneo, el morro (mira a la izquierda) y la mandibula, que se abre con
    cara['boca'] grados; el ojo, la ceja y la sonrisa."""
    giro = cara.get('giro', 0.0)
    c = (84, 56)

    def R(pts):
        return [_rot(p, c, giro) for p in pts]
    ang = cara.get('boca', 0.0)
    piv = (90, 62)
    mand = (_bezier((92, 60), (64, 64), (36, 66), 6) + [(34, 72)]
            + _bezier((40, 78), (66, 86), (96, 76), 6))
    mand = [_rot(p, piv, -ang) for p in mand]
    if ang > 2:
        L.poli(R([(90, 58), (38, 58), _rot((34, 70), piv, -ang), _rot((66, 76), piv, -ang), (92, 72)]), BOCA, 1.0)
        L.poli(R([_rot(p, piv, -ang * 0.6) for p in [(80, 70), (54, 70), (48, 74), (78, 76)]]), LENGUA, 0)
    L.poli(R(mand), PIEL)
    if ang > 2:
        for k in range(5):
            b = _rot((42 + k * 9, 66), piv, -ang)
            L.poli(R([(b[0] - 3.2, b[1] + 1), (b[0], b[1] - 6), (b[0] + 3.2, b[1] + 1)]), DIENTE, 0.8)
    craneo = (_bezier((104, 68), (118, 34), (94, 24), 8) + _bezier((94, 24), (68, 20), (54, 36), 8)
              + _bezier((54, 36), (30, 40), (28, 52), 4) + [(30, 60), (60, 61), (92, 62)])
    L.poli(R(craneo), PIEL)
    L.linea(R(_bezier((56, 36), (74, 30), (88, 36), 6)), PIEL_CLARA, 1.6)    # el brillo del craneo
    L.elipse(*_rot((33, 49), c, giro), 1.8, 1.5, TINTA, 0)       # la nariz
    if ang > 2:
        for k in range(6):
            x = 34 + k * 9
            L.poli(R([(x - 3.2, 60), (x, 67), (x + 3.2, 60)]), DIENTE, 0.8)
    else:
        sonr = cara.get('sonrisa', 0.0)
        y = 62
        L.linea(R(_bezier((40, y), (60, y + 1 - sonr * 2.5), (80, y - sonr * 6), 8)), TINTA, 1.6)
        if sonr > 0.5:
            L.linea(R([(80, y - sonr * 6 - 2), (82, y - sonr * 6 + 3)]), TINTA, 1.4)
    for k in range(3):
        L.arco(*_rot((100, 46 + k * 8), c, giro), 6, 3, 100, 260, PIEL_OSC, 0.9)
    ojo(L, R, cara)


def ojo(L, R, cara):
    tipo = cara.get('ojo', 'normal')
    ex, ey = 68, 40
    p = R([(ex, ey)])[0]
    col = OJO_FURIA if cara.get('furia') else OJO
    if tipo in ('normal', 'enfado', 'triste'):
        L.elipse(p[0], p[1], 6.5, 5.4, col, 1.3)
        L.elipse(p[0] - 2.0, p[1] + 0.3, 2.3, 3.6, PUPILA, 0)
        L.elipse(p[0] - 2.8, p[1] - 1.6, 0.9, 0.9, DIENTE, 0)
    elif tipo == 'grande':
        L.elipse(p[0], p[1] - 1, 9.0, 8.5, DIENTE, 1.4)
        L.elipse(p[0] - 1.0, p[1] - 1, 2.0, 2.0, PUPILA, 0)
    elif tipo == 'feliz':
        L.arco(p[0], p[1] + 2.5, 6.5, 5.5, 190, 350, TINTA, 2.2)
    elif tipo == 'cerrado':
        L.arco(p[0], p[1] - 2.5, 6.5, 4.5, 20, 160, TINTA, 2.2)
    elif tipo == 'apretado':
        L.linea(R([(ex - 7, ey - 5), (ex + 3, ey), (ex - 7, ey + 5)]), TINTA, 2.2)
    ceja = cara.get('ceja', 0.0)            # + enfadado (baja delante), - triste (sube delante)
    if tipo not in ('feliz', 'cerrado'):
        L.poli(R([(ex - 10, ey - 9 + ceja * 3.5), (ex + 9, ey - 11 - ceja * 2), (ex + 9, ey - 7 - ceja * 2),
                  (ex - 10, ey - 6 + ceja * 3.5)]), PIEL_OSC, 1.2)


# --- los extras -----------------------------------------------------------------

def gota(L, x, y, r, col=AGUA):
    L.poli([(x, y - r * 2.2), (x - r, y), (x + r, y)], col, 0.8)
    L.elipse(x, y, r, r, col, 0.8)


def estrella(L, x, y, r):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    L.poli(pts, ESTRELLA, 0.9)


def hoja(L, x, y, ang, t):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    L.poli([(x, y), (x + ux * t * 0.5 + px * t * 0.35, y + uy * t * 0.5 + py * t * 0.35), (x + ux * t, y + uy * t),
            (x + ux * t * 0.5 - px * t * 0.35, y + uy * t * 0.5 - py * t * 0.35)], HOJA, 0.9)


def flor(L, x, y, r):
    for k in range(5):
        a = math.radians(k * 72 - 90)
        L.elipse(x + math.cos(a) * r, y + math.sin(a) * r, r * 0.75, r * 0.75, FLOR, 0.8)
    L.elipse(x, y, r * 0.6, r * 0.6, FLOR_C, 0.8)


def vapor(L, x, y):
    for k in range(3):
        L.arco(x - k * 7, y - k * 3, 4, 6, 200, 340, (230, 236, 230, 255), 1.2)


# --- las caras -------------------------------------------------------------------

CARAS = dict(
    serio=dict(boca=0, ojo='normal', ceja=0.2, brazo='abajo'),
    enfado=dict(boca=14, ojo='enfado', ceja=1.0, brazo='delante'),
    furia=dict(boca=26, ojo='enfado', ceja=1.4, brazo='golpe', furia=True, brillo=True, giro=-6),
    rie=dict(boca=0, ojo='feliz', sonrisa=1.0, brazo='abajo', hojas=True),
    carcajada=dict(boca=22, ojo='cerrado', brazo='tripa', lagrima_risa=True, giro=-8, hojas=True),
    susto=dict(boca=9, ojo='grande', ceja=-1.0, brazo='delante', sudor=True, giro=5),
    mueca=dict(boca=0, ojo='apretado', sonrisa=-0.8, brazo='cubre', estrellas=True, giro=10),
    llora=dict(boca=0, ojo='triste', ceja=-1.2, sonrisa=-1.0, brazo='abajo', lagrimas=True, giro=6),
    panico=dict(boca=18, ojo='grande', ceja=-1.4, brazo='arriba', sudor=True, giro=-4),
    calma=dict(boca=0, ojo='cerrado', sonrisa=0.7, brazo='saluda', flor=True),
)


def dibujar(nombre):
    cara = CARAS[nombre]
    L = Lienzo()
    brillo = cara.get('brillo', False)
    placas(L, brillo)
    cola(L)
    brazo(L, 'golpe' if cara['brazo'] == 'golpe' else ('arriba' if cara['brazo'] in ('arriba',) else 'abajo'), True)
    pierna(L, 122, 186, True)
    cuerpo(L)
    pierna(L, 88, 188)
    cuello(L)
    cabeza(L, cara)
    mano = brazo(L, cara['brazo'])
    if cara.get('flor'):
        L.linea([(mano[0] - 2, mano[1] - 2), (mano[0] - 6, mano[1] - 18)], PLACA_OSC, 1.4)
        flor(L, mano[0] - 6, mano[1] - 22, 5.0)
    if cara.get('hojas'):
        for x, y, a, t in ((24, 92, -150, 15), (14, 130, 160, 13), (30, 18, -120, 14), (156, 30, -40, 14),
                           (176, 100, -20, 13), (20, 196, -170, 12)):
            hoja(L, x, y, a, t)
    if cara.get('lagrima_risa'):
        gota(L, 56, 32, 3.6)
        gota(L, 42, 26, 3.0)
        gota(L, 80, 26, 3.2)
    if cara.get('lagrimas'):
        for k in range(3):
            gota(L, 62 - k * 2, 56 + k * 12, 3.4 - k * 0.4)
    if cara.get('sudor'):
        gota(L, 108, 18, 3.6)
        gota(L, 120, 36, 3.0)
        gota(L, 40, 20, 3.0)
    if cara.get('estrellas'):
        estrella(L, 36, 16, 9)
        estrella(L, 62, 8, 6)
        estrella(L, 18, 36, 6)
    if cara.get('furia'):
        vapor(L, 22, 40)
    return L.final()


def main():
    atlas = Image.new('RGBA', (CELDA_W * COLS, CELDA_H * FILAS), (0, 0, 0, 0))
    lamina = Image.new('RGBA', atlas.size, (60, 62, 68, 255))
    d = ImageDraw.Draw(lamina)
    try:
        fuente = ImageFont.load_default()
    except Exception:
        fuente = None
    for k, nombre in enumerate(EMOCIONES):
        im = dibujar(nombre)
        x, y = (k % COLS) * CELDA_W, (k // COLS) * CELDA_H
        atlas.paste(im, (x, y))
        lamina.alpha_composite(im, (x, y))
        d.text((x + 4, y + 2), '%d %s' % (k, nombre), fill=(255, 230, 0, 255), font=fuente)
    atlas.save(os.path.join(AQUI, 'godzilla_emociones.png'))
    lamina.save(os.path.join(AQUI, 'godzilla_emociones_lamina.png'))
    print('godzilla_emociones.png (%d x %d) y la lamina' % atlas.size)


if __name__ == '__main__':
    main()
