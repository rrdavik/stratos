"""
=============================================================================
ESTRATOS - NEFANYAMUTO: LA CABEZA (estudio de caricatura)
=============================================================================
La cabeza en vista de tres cuartos mirando a la izquierda, como la de Trumpzilla,
con sombreado pintado (capas difuminadas recortadas por la cara) y reducida a
pixel art con una paleta adaptada. Se dibuja en "unidades" de cabeza (la cara
mide unas 62 de ancho, el origen entre los ojos, y hacia abajo); retrato()
devuelve la imagen a la escala final que se pida (pixeles por unidad).

Rasgos: canas peinadas hacia atras con entradas, cejas oscuras y pesadas, ojos
pequenos de parpado caido que miran de reojo, bolsas, la nariz larga y carnosa
con la punta partida en dos por una hendidura (como un capullo), surcos hondos,
labios finos con las comisuras caidas, papada y orejas de soplillo enormes (que
en el monstruo hacen de alas).
=============================================================================
"""

import math

from PIL import Image, ImageChops, ImageDraw, ImageFilter

TINTA = (34, 20, 22)
# piel
PIEL = (222, 164, 134)
PIEL_LUZ = (242, 198, 166)
PIEL_BRILLO = (252, 224, 196)
PIEL_OSC = (190, 124, 100)
PIEL_SOMBRA = (148, 88, 76)
PIEL_HONDA = (104, 58, 56)
ROJEZ = (214, 112, 100)
OREJA_DENTRO = (200, 112, 104)
OJERA = (130, 84, 92)
# pelo y cejas
CANA = (196, 198, 204)
CANA_LUZ = (236, 238, 242)
CANA_OSC = (128, 130, 140)
CANA_HONDA = (88, 90, 100)
CEJA = (60, 56, 60)
CEJA_LUZ = (120, 116, 120)
# ojos y boca
BLANCO_OJO = (226, 218, 204)
IRIS = (78, 62, 50)
PUPILA = (18, 14, 14)
ROJO_OJO = (255, 60, 30)
LABIO = (168, 92, 88)
LABIO_OSC = (118, 58, 60)
BOCA = (70, 20, 26)
DIENTE = (236, 230, 214)
LENGUA = (190, 84, 92)
CAMISA = (238, 240, 244)
CAMISA_OSC = (186, 192, 206)


def bez(p0, p1, p2, n=10):
    out = []
    for k in range(n + 1):
        t = k / float(n)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


class Retrato(object):
    """Lienzo en unidades: x de -ox a ancho - ox, y de -oy a alto - oy; k pixeles por unidad."""

    def __init__(self, k=8, ancho=140, alto=140, ox=70, oy=72):
        self.k, self.ox, self.oy = k, ox, oy
        self.W, self.H = int(ancho * k), int(alto * k)
        self.ancho, self.alto = ancho, alto
        self.im = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [((x + self.ox) * self.k, (y + self.oy) * self.k) for x, y in pts]

    # --- mascaras --------------------------------------------------------------
    def m_vacia(self):
        return Image.new('L', (self.W, self.H), 0)

    def m_poli(self, pts, m=None, v=255):
        m = m or self.m_vacia()
        ImageDraw.Draw(m).polygon(self.P(pts), fill=v)
        return m

    def m_elipse(self, cx, cy, rx, ry, m=None, v=255):
        m = m or self.m_vacia()
        ImageDraw.Draw(m).ellipse(self.P([(cx - rx, cy - ry), (cx + rx, cy + ry)]), fill=v)
        return m

    def m_linea(self, pts, ancho, m=None, v=255):
        m = m or self.m_vacia()
        ImageDraw.Draw(m).line(self.P(pts), fill=v, width=max(1, int(ancho * self.k)), joint='curve')
        return m

    # --- pintar ----------------------------------------------------------------
    def pintar(self, m, col, blur=0.0, clip=None, alpha=1.0):
        if blur > 0:
            m = m.filter(ImageFilter.GaussianBlur(blur * self.k))
        if clip is not None:
            m = ImageChops.multiply(m, clip)
        if alpha < 1.0:
            m = m.point(lambda v: int(v * alpha))
        capa = Image.new('RGBA', (self.W, self.H), tuple(col[:3]) + (0,))
        capa.putalpha(m)
        self.im.alpha_composite(capa)

    def poli(self, pts, col, borde=0.0, tinta=TINTA):
        self.d.polygon(self.P(pts), fill=tuple(col[:3]) + (255,))
        if borde > 0:
            self.linea(pts + pts[:1], tinta, borde)

    def elipse(self, cx, cy, rx, ry, col, borde=0.0, tinta=TINTA):
        caja = self.P([(cx - rx, cy - ry), (cx + rx, cy + ry)])
        if borde > 0:
            self.d.ellipse(caja, fill=tuple(col[:3]) + (255,), outline=tuple(tinta) + (255,),
                           width=max(1, int(borde * self.k)))
        else:
            self.d.ellipse(caja, fill=tuple(col[:3]) + (255,))

    def linea(self, pts, col=TINTA, ancho=1.0):
        self.d.line(self.P(pts), fill=tuple(col[:3]) + (255,), width=max(1, int(ancho * self.k)), joint='curve')

    # --- final -----------------------------------------------------------------
    def final(self, escala, colores=40):
        """Reduce a 'escala' pixeles por unidad, recorte duro y paleta adaptada."""
        w, h = max(1, int(round(self.ancho * escala))), max(1, int(round(self.alto * escala)))
        im = self.im.resize((w, h), Image.LANCZOS)
        return pixelar(im, colores)


def pixelar(im, colores=40):
    a = im.split()[3].point(lambda v: 255 if v >= 128 else 0)
    fondo = Image.new('RGBA', im.size, (200, 150, 130, 255))
    fondo.alpha_composite(im)
    rgb = fondo.convert('RGB')
    # des-premultiplica los bordes: lo opaco a medias se lleva a su color
    q = rgb.quantize(colors=colores, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    out = q.convert('RGBA')
    out.putalpha(a)
    return out


# --- las partes -------------------------------------------------------------------

OREJA_D = [(31, -17), (40, -30), (56, -37), (69, -33), (76, -20), (75, -4), (68, 10), (58, 17), (52, 25),
           (45, 30), (38, 28), (33, 21)]


def oreja(R, lado, tam, ala=0.0):
    """Oreja de soplillo, humana: la helice gruesa por fuera, la concha honda, el
    antihelix y el lobulo. lado +1 la de cerca (derecha), -1 la de lejos (mas
    estrecha por el escorzo). tam la agranda hacia fuera; ala (0..1) la abre hacia
    arriba como un ala."""
    ax = 31.0

    def X(p):
        x, y = p
        d = (x - ax) * tam
        y = y - ala * 0.5 * d * (1 - (y + 30) / 70.0)
        if lado > 0:
            return (ax + d, y)
        return (-27 - d * 0.8, y + 1)
    pts = [X(p) for p in OREJA_D]
    m = R.m_poli(pts)
    R.poli(pts, PIEL)
    # sombra donde nace y luz en la helice
    R.pintar(R.m_linea([pts[0], pts[-1]], 7), PIEL_SOMBRA, 2.0, m, 0.95)
    R.pintar(R.m_linea(pts[1:8], 3.4), PIEL_LUZ, 0.8, m, 0.6)
    R.pintar(R.m_elipse(*X((46, 22)), 4, 4), ROJEZ, 1.5, m, 0.4)                      # el lobulo
    # la concha: hueco hondo en medio
    concha = [X(p) for p in ((36, -12), (48, -24), (62, -25), (68, -10), (63, 6), (53, 12), (44, 14), (37, 8))]
    R.pintar(R.m_poli(concha), OREJA_DENTRO, 0.8, m, 0.95)
    R.pintar(R.m_poli([X(p) for p in ((38, -4), (46, -8), (52, 0), (48, 10), (40, 10))]), PIEL_HONDA, 2.0, m, 0.6)
    # el borde interior de la helice y el antihelix (la Y)
    R.linea([X(p) for p in ((40, -25), (56, -31), (68, -27), (72, -14), (70, 2), (62, 11))], PIEL_SOMBRA, 1.0)
    R.linea([X(p) for p in ((56, 10), (62, -2), (60, -14), (52, -22))], PIEL_OSC, 1.6)
    R.linea([X(p) for p in ((60, -14), (48, -17))], PIEL_OSC, 1.2)
    R.elipse(*X((35, 4)), 2.2, 3.0, PIEL_OSC)            # el trago
    R.linea(pts + pts[:1], TINTA, 1.3)


CARA = (bez((-23, -32), (-29, -18), (-28, -2)) + bez((-28, -2), (-30, 14), (-28, 26))
        + bez((-28, 26), (-32, 42), (-22, 52)) + bez((-22, 52), (-6, 60), (10, 56))
        + bez((10, 56), (31, 50), (31, 32)) + bez((31, 32), (35, 14), (33, -4))
        + bez((33, -4), (32, -20), (27, -32))
        + [(22, -38), (14, -41), (6, -42), (0, -47), (-6, -44), (-12, -42), (-18, -39)])

PELO = (bez((-25, -26), (-34, -42), (-24, -52)) + [(-20, -56), (-14, -55), (-10, -60), (-2, -59), (2, -63),
        (10, -62), (16, -64), (24, -60), (30, -56), (36, -48), (40, -38), (42, -24), (40, -8), (35, 2), (30, -6),
        (28, -30), (-20, -34)])


def pelo(R):
    m = R.m_poli(PELO)
    R.poli(PELO, CANA)
    # volumen: oscuro detras y abajo, luz arriba a la izquierda
    R.pintar(R.m_poli([(16, -70), (50, -50), (46, 6), (26, 0), (22, -40)]), CANA_OSC, 4, m, 0.95)
    R.pintar(R.m_poli([(30, -50), (50, -40), (46, 6), (32, 0)]), CANA_HONDA, 3, m, 0.7)
    R.pintar(R.m_elipse(-10, -54, 12, 5), CANA_LUZ, 2.5, m, 1.0)
    # el tupe: la masa de delante peinada hacia arriba y atras
    tupe = [(-22, -36), (-27, -46), (-20, -55), (-8, -60), (4, -60), (12, -54), (6, -48), (-6, -46), (-14, -42)]
    R.pintar(R.m_poli(tupe), CANA_LUZ, 1.2, m, 0.9)
    R.pintar(R.m_linea(bez((-20, -38), (-6, -46), (10, -50)), 2.4), CANA_OSC, 1.2, m, 0.9)
    # mechas hacia atras, alternando oscuras y claras
    for a, b, c, col, w in (((-16, -42), (-4, -56), (18, -58), CANA_OSC, 1.0), ((-4, -46), (12, -56), (30, -50), CANA_HONDA, 1.1),
                            ((-24, -36), (-26, -48), (-10, -56), CANA_OSC, 0.9), ((6, -46), (24, -50), (38, -34), CANA_HONDA, 1.1),
                            ((-14, -50), (0, -60), (16, -60), CANA_LUZ, 1.2), ((16, -44), (32, -44), (40, -20), CANA_HONDA, 1.1),
                            ((0, -52), (18, -58), (34, -46), CANA_LUZ, 0.9), ((20, -36), (34, -34), (38, -12), CANA_OSC, 0.9)):
        R.linea(bez(a, b, c, 8), col, w)
    R.linea(PELO + PELO[:1], TINTA, 1.3)
    # patillas cortas sobre las orejas
    for pts in ([(-28, 0), (-31, -16), (-25, -26), (-23, -14), (-25, -4)], [(31, 0), (34, -14), (28, -28), (26, -14), (28, -2)]):
        R.poli(pts, CANA, 0.9)
        R.pintar(R.m_poli(pts), CANA_OSC, 1.2, R.m_poli(pts), 0.8)


def cara_base(R):
    m = R.m_poli(CARA)
    R.poli(CARA, PIEL)
    # sombras grandes: el lado derecho, las sienes, bajo los pomulos, la papada
    R.pintar(R.m_poli([(16, -40), (40, -30), (40, 50), (6, 54), (14, 30), (20, 0)]), PIEL_OSC, 5, m, 0.95)
    R.pintar(R.m_poli([(24, -10), (40, -10), (40, 48), (14, 50)]), PIEL_SOMBRA, 4, m, 0.7)
    R.pintar(R.m_elipse(-27, -18, 5, 10), PIEL_OSC, 3, m, 0.7)
    R.pintar(R.m_elipse(-24, 14, 5, 9), PIEL_OSC, 3, m, 0.6)           # bajo el pomulo
    R.pintar(R.m_elipse(18, 16, 5, 9), PIEL_SOMBRA, 3, m, 0.5)
    # mofletes caidos y papada
    R.pintar(R.m_linea(bez((-27, 24), (-26, 40), (-14, 46)), 5), PIEL_SOMBRA, 2.5, m, 0.8)
    R.pintar(R.m_linea(bez((28, 22), (26, 40), (12, 48)), 6), PIEL_SOMBRA, 2.5, m, 0.9)
    R.pintar(R.m_linea(bez((-14, 55), (-2, 60), (12, 55)), 3), PIEL_HONDA, 1.5, m, 0.8)
    # los carrillos que cuelgan junto a la barbilla
    R.linea(bez((-26, 36), (-23, 48), (-15, 50), 6), PIEL_HONDA, 0.9)
    R.linea(bez((27, 36), (23, 48), (15, 52), 6), PIEL_HONDA, 0.9)
    R.pintar(R.m_elipse(-4, 53, 7, 3), PIEL_LUZ, 1.5, m, 0.7)
    # luces: frente, pomulo izquierdo, barbilla
    R.pintar(R.m_elipse(-8, -30, 13, 6), PIEL_LUZ, 4, m, 0.9)
    R.pintar(R.m_elipse(-12, -32, 6, 3), PIEL_BRILLO, 2, m, 0.8)
    R.pintar(R.m_elipse(-20, 6, 5, 4), PIEL_LUZ, 3, m, 0.7)
    
    # rojez de la cara (nariz y mejillas)
    R.pintar(R.m_elipse(-21, 14, 6, 5), ROJEZ, 4, m, 0.35)
    R.pintar(R.m_elipse(14, 14, 6, 5), ROJEZ, 4, m, 0.3)
    # arrugas de la frente
    for k in range(3):
        y = -26 - k * 4.5
        R.linea(bez((-18 + k * 2, y + 1), (-2, y - 1.8), (16 - k * 2, y + 0.5), 8), PIEL_OSC, 0.9)
        R.linea(bez((-17 + k * 2, y + 2), (-2, y - 0.6), (15 - k * 2, y + 1.5), 8), PIEL_LUZ, 0.6)
    R.linea(CARA + CARA[:1], TINTA, 1.5)
    return m


class _Baja(object):
    """Desplaza en y lo que se dibuja (para bajar las cejas sin rehacer sus puntos)."""

    def __init__(self, R, dy):
        self.R, self.dy = R, dy

    def _t(self, pts):
        return [(x, y + self.dy) for x, y in pts]

    def m_poli(self, pts, m=None, v=255):
        return self.R.m_poli(self._t(pts), m, v)

    def pintar(self, *a, **k):
        self.R.pintar(*a, **k)

    def poli(self, pts, *a, **k):
        self.R.poli(self._t(pts), *a, **k)

    def linea(self, pts, *a, **k):
        self.R.linea(self._t(pts), *a, **k)


def cejas(R, m, cara):
    ceno = cara.get('ceno', 0.6)            # baja las puntas de dentro
    R = _Baja(R, 1.8)
    alza = cara.get('alza', 0.0)            # sube la de cerca (el pillo)
    # la de cerca (derecha) y la de lejos (izquierda): gruesas, oscuras, poco arqueadas
    for pts in ([(1, -13 + ceno * 2.5), (9, -17.5 - alza * 4), (19, -17 - alza * 3), (24, -13 - alza * 1.5),
                 (19, -14 - alza * 2.5), (9, -14 - alza * 3.5), (2, -10 + ceno * 2.5)],
                [(-6, -13 + ceno * 2.5), (-15, -17), (-23, -15), (-26, -11), (-22, -12.5), (-15, -14), (-7, -10 + ceno * 2.5)]):
        R.pintar(R.m_poli([(x, y + 3) for x, y in pts]), PIEL_SOMBRA, 2.0, m, 0.8)    # la sombra bajo la ceja
        R.poli(pts, CEJA, 0)
        R.linea(pts[:4], CEJA_LUZ, 0.7)
    if ceno > 0.4:
        for x in (-3.5, -1.5):
            R.linea([(x, -14), (x + 0.4, -7)], PIEL_SOMBRA, 0.9)


def ojo(R, m, cx, cy, w, cara, lejos=False):
    """Un ojo pequeno de parpado caido, que mira de reojo."""
    h = cara.get('abre', 1.0) * 3.3
    tipo = cara.get('ojo', 'normal')
    # la cuenca, honda
    R.pintar(R.m_elipse(cx, cy - 1, w * 0.8, 5.5), PIEL_SOMBRA, 2.0, m, 0.9)
    # las bolsas
    R.pintar(R.m_linea(bez((cx - w * 0.5, cy + 3), (cx, cy + 7), (cx + w * 0.55, cy + 2.5)), 2.6), OJERA, 1.4, m, 0.9)
    R.linea(bez((cx - w * 0.45, cy + 5.5), (cx + 1, cy + 9), (cx + w * 0.55, cy + 4.5), 6), PIEL_SOMBRA, 0.8)
    R.linea(bez((cx - w * 0.3, cy + 3.2), (cx + 1, cy + 5.2), (cx + w * 0.5, cy + 2.5), 6), PIEL_OSC, 0.7)
    if cara.get('ojo_rojo'):
        R.pintar(R.m_elipse(cx, cy, w * 0.7, 4.5), ROJO_OJO, 2.0, m, 0.5)
    if tipo == 'cerrado':
        R.linea(bez((cx - w * 0.5, cy), (cx, cy + 1.6), (cx + w * 0.5, cy - 0.4), 6), TINTA, 1.1)
        R.linea(bez((cx - w * 0.5, cy - 2.4), (cx, cy - 4), (cx + w * 0.55, cy - 2), 6), PIEL_SOMBRA, 0.9)
        return
    big = 1.9 if tipo == 'grande' else 1.0
    almendra = bez((cx - w * 0.5, cy), (cx, cy - h * 1.3 * big), (cx + w * 0.5, cy + 0.4), 8) + \
        bez((cx + w * 0.5, cy + 0.4), (cx, cy + h * 1.1 * big), (cx - w * 0.5, cy), 8)
    me = R.m_poli(almendra)
    R.poli(almendra, BLANCO_OJO)
    mira = cara.get('mira', -0.55)          # -1 de reojo a la izquierda, +1 a la derecha
    ix = cx + mira * w * 0.28
    rojo = cara.get('ojo_rojo', False)
    R.pintar(R.m_elipse(ix, cy + 0.4, 3.0, 3.0), ROJO_OJO if rojo else IRIS, 0, me)
    R.pintar(R.m_elipse(ix, cy + 0.4, 1.5, 1.5), PUPILA, 0, me)
    R.pintar(R.m_elipse(ix - 0.9, cy - 0.8, 0.6, 0.6), (250, 250, 250), 0, me)
    # el parpado de arriba: pesado, cae por fuera (la esquina de la derecha baja)
    caida = cara.get('caida', 1.0)
    parp = bez((cx - w * 0.6, cy - 0.4), (cx - w * 0.1, cy - h * 1.8 * big), (cx + w * 0.62, cy + 0.6 * caida), 8) + \
        [(cx + w * 0.62, cy - 3.5), (cx - w * 0.6, cy - 4.5)]
    if big < 1.5:
        parp = bez((cx - w * 0.6, cy - 0.2), (cx - w * 0.05, cy - h * 1.05), (cx + w * 0.62, cy + 1.0 * caida), 8) + \
            [(cx + w * 0.62, cy - 4.5), (cx - w * 0.6, cy - 5)]
    R.poli(parp, PIEL_OSC)
    R.pintar(R.m_poli(parp), PIEL_SOMBRA, 0.8, R.m_poli(parp), 0.5)
    R.linea(parp[:9], TINTA, 1.6)
    R.linea(bez((cx - w * 0.5, cy + 0.2), (cx, cy + h * 1.05 * big), (cx + w * 0.5, cy + 0.6), 6), PIEL_HONDA, 0.6)
    # el pliegue sobre el parpado
    R.linea(bez((cx - w * 0.45, cy - 3.6), (cx + 1, cy - 5.6), (cx + w * 0.6, cy - 2.6), 6), PIEL_SOMBRA, 0.8)
    # patas de gallo
    if not lejos:
        for k in (-1, 0, 1):
            R.linea([(cx + w * 0.7, cy + k * 1.6), (cx + w * 0.7 + 4, cy + k * 2.6)], PIEL_OSC, 0.6)


def nariz_(R, m, cara):
    """Larga y carnosa, la punta en dos lobulos partidos por una hendidura."""
    # el puente: sombra a la derecha, luz a la izquierda
    R.pintar(R.m_poli([(-4, -10), (0, -10), (2, 10), (-1, 14)]), PIEL_OSC, 1.5, m, 0.9)
    R.pintar(R.m_linea([(-7, -6), (-10, 10)], 2.0), PIEL_LUZ, 1.2, m, 0.9)
    # el contorno de la izquierda (perfil de la nariz, sale un poco de la cara)
    R.linea(bez((-6, -8), (-11, 6), (-15, 13), 6), PIEL_OSC, 0.8)
    # las aletas
    for ax, ay in ((-18.5, 21), (1.5, 21)):
        R.elipse(ax, ay, 3.6, 3.2, PIEL)
        R.pintar(R.m_elipse(ax + 0.6, ay + 0.6, 3.4, 3.0), PIEL_OSC, 1.0, R.m_elipse(ax, ay, 3.6, 3.2), 0.8)
        R.linea(bez((ax - 3.2, ay + 2.2), (ax, ay - 4.2), (ax + 3.2, ay + 2.2), 6), PIEL_SOMBRA, 0.9)
    # sombra bajo la nariz
    R.pintar(R.m_elipse(-8, 26, 11, 3), PIEL_HONDA, 2.0, m, 0.8)
    # los dos lobulos de la punta
    for lx, col in ((-12.5, PIEL), (-3.5, PIEL)):
        R.elipse(lx, 18.5, 5.0, 5.4, col)
    mn = R.m_elipse(-12.5, 18.5, 5.0, 5.4, R.m_elipse(-3.5, 18.5, 5.0, 5.4))
    R.pintar(R.m_elipse(-1.5, 20, 4, 5), PIEL_OSC, 1.5, mn, 0.9)
    R.pintar(R.m_elipse(-11, 22, 5, 2.4), PIEL_OSC, 1.2, mn, 0.7)
    R.pintar(R.m_elipse(-11, 17, 5, 5), ROJEZ, 2.0, mn, 0.45)
    R.pintar(R.m_elipse(-4, 17, 4, 4), ROJEZ, 2.0, mn, 0.35)
    R.pintar(R.m_elipse(-14, 16, 1.6, 1.4), PIEL_BRILLO, 0.6, mn, 1.0)
    R.pintar(R.m_elipse(-5.5, 16, 1.4, 1.2), PIEL_LUZ, 0.6, mn, 1.0)
    R.linea(bez((-17, 15), (-18.5, 21), (-14, 24), 5), TINTA, 1.1)
    R.linea(bez((1, 15), (2.5, 21), (-2, 24), 5), PIEL_HONDA, 1.1)
    # la hendidura: casi la parte en dos
    R.pintar(R.m_linea([(-8, 13.5), (-8, 23.5)], 2.4), PIEL_SOMBRA, 0.7, mn, 1.0)
    R.linea([(-8, 15.0), (-8.2, 23.8)], PIEL_HONDA, 1.1)
    R.linea(bez((-17.5, 17), (-15, 24.5), (-8, 23.8), 6) + bez((-8, 23.8), (-2, 24.5), (1.5, 17), 6), TINTA, 1.3)
    # los agujeros
    R.elipse(-14.5, 23.2, 1.8, 1.0, PIEL_HONDA)
    R.elipse(-2.0, 23.2, 1.6, 1.0, PIEL_HONDA)


def nariz(R, m, cara):
    """La nariz, mas grande que en la plantilla: se dibuja en un lienzo propio y se
    escala desde el puente."""
    f = cara.get('nariz', 1.35)
    piv = (-6.0, -10.0)

    class Escalado(object):
        def __init__(self, R):
            self.R = R

        def T(self, pts):
            return [(piv[0] + (x - piv[0]) * f, piv[1] + (y - piv[1]) * f) for x, y in pts]

        def P(self, pts):
            return self.R.P(self.T(pts))

        def m_poli(self, pts, m=None, v=255):
            return self.R.m_poli(self.T(pts), m, v)

        def m_elipse(self, cx, cy, rx, ry, m=None, v=255):
            (cx, cy), = self.T([(cx, cy)])
            return self.R.m_elipse(cx, cy, rx * f, ry * f, m, v)

        def m_linea(self, pts, ancho, m=None, v=255):
            return self.R.m_linea(self.T(pts), ancho * f, m, v)

        def pintar(self, mm, col, blur=0.0, clip=None, alpha=1.0):
            self.R.pintar(mm, col, blur * f, clip, alpha)

        def poli(self, pts, col, borde=0.0, tinta=TINTA):
            self.R.poli(self.T(pts), col, borde, tinta)

        def elipse(self, cx, cy, rx, ry, col, borde=0.0, tinta=TINTA):
            (cx, cy), = self.T([(cx, cy)])
            self.R.elipse(cx, cy, rx * f, ry * f, col, borde, tinta)

        def linea(self, pts, col=TINTA, ancho=1.0):
            self.R.linea(self.T(pts), col, ancho * (1 + (f - 1) * 0.5))
    nariz_(Escalado(R), m, cara)


def surcos(R, m, cara):
    for a, b, c in (((-23, 28), (-29, 38), (-26, 48)), ((7, 28), (13, 38), (11, 50))):
        R.pintar(R.m_linea(bez(a, b, c), 3.0), PIEL_SOMBRA, 1.5, m, 0.9)
        R.linea(bez(a, b, c, 8), PIEL_HONDA, 0.9)
        R.pintar(R.m_linea(bez((a[0] - 2, a[1] + 2), (b[0] - 2, b[1]), (c[0] - 1, c[1])), 2.0), PIEL_LUZ, 1.2, m, 0.6)


def boca(R, m, cara):
    tipo = cara.get('boca', 'seria')
    y = 42
    if tipo == 'grito':
        abre = cara.get('abre_boca', 9)
        top = bez((-20, y + 5), (-8, y - 4), (5, y + 5), 8)
        bot = bez((5, y + 5), (3, y + abre + 1), (-8, y + abre + 1), 5) + bez((-8, y + abre + 1), (-18, y + abre + 1), (-20, y + 5), 5)
        R.poli(top + bot, BOCA)
        mb = R.m_poli(top + bot)
        R.pintar(R.m_poli([(-15, y - 2), (1, y - 2), (1, y + 2.2), (-15, y + 2.2)]), DIENTE, 0, mb)
        R.linea([(-11, y - 1), (-11, y + 2)], LABIO_OSC, 0.5)
        R.linea([(-5, y - 1), (-5, y + 2)], LABIO_OSC, 0.5)
        R.pintar(R.m_poli([(-14, y + abre - 1.5), (-2, y + abre - 1.5), (-2, y + abre + 2), (-14, y + abre + 2)]), DIENTE, 0, mb, 0.8)
        R.pintar(R.m_elipse(-8, y + abre - 2, 6, 2.5), LENGUA, 0.6, mb, 0.9)
        R.linea(top + bot[:1], LABIO_OSC, 1.4)
        R.linea(top + bot + top[:1], TINTA, 1.0)
        R.pintar(R.m_elipse(-8, y + abre + 5, 9, 2.5), PIEL_SOMBRA, 1.5, m, 0.8)
        return
    sonr = cara.get('sonrisa', 0.0)       # >0 la comisura de la derecha sube (sonrisa de pillo)
    izq = (-21, y + 2.5)
    der = (6, y + 2.5 - sonr * 5)
    centro = (-8, y - 0.2)
    # labio de arriba fino, de abajo un poco mas carnoso
    sup = bez(izq, (-14, y - 2.4), centro, 5) + bez(centro, (-1, y - 2.2 - sonr * 1.5), der, 5)
    inf = bez(der, (-6, y + 5.5 - sonr * 2), izq, 8)
    R.poli(sup + inf, LABIO)
    R.pintar(R.m_poli(inf + [centro]), PIEL_LUZ, 1.0, R.m_poli(sup + inf), 0.35)
    linea = bez(izq, (-8, y + 1.6 - sonr * 1.2), der, 8)
    R.linea(linea, TINTA, 1.1)
    # las comisuras hundidas y la sombra bajo el labio
    for p in (izq, der):
        R.pintar(R.m_elipse(p[0], p[1] + 1, 2, 2), PIEL_HONDA, 1.0, m, 0.8)
    R.pintar(R.m_elipse(-8, y + 7, 7, 2.2), PIEL_SOMBRA, 1.5, m, 0.8)
    if sonr > 0.3:
        R.linea(bez((der[0] - 1, der[1] - 1), (der[0] + 3, der[1] - 1), (der[0] + 3, der[1] + 3), 4), PIEL_SOMBRA, 0.9)


def cuello(R):
    """El cuello de la camisa, debajo de la papada."""
    pts = [(-20, 50), (-6, 62), (14, 52), (20, 64), (-2, 70), (-24, 62)]
    R.poli(pts, CAMISA, 1.1)
    R.pintar(R.m_poli([(4, 54), (22, 58), (20, 66), (0, 68)]), CAMISA_OSC, 2, R.m_poli(pts), 0.9)
    R.pintar(R.m_elipse(-2, 58, 22, 6), PIEL_HONDA, 2.5, R.m_poli(pts), 0.6)


def cabeza(R, cara):
    oreja(R, -1, cara.get('orejas', 1.0), cara.get('ala', 0.0))
    oreja(R, 1, cara.get('orejas', 1.0), cara.get('ala', 0.0))
    cuello(R)
    pelo(R)
    m = cara_base(R)
    cejas(R, m, cara)
    ojo(R, m, -14.5, -6, 10.5, cara, lejos=True)
    ojo(R, m, 10.5, -6, 13.0, cara)
    surcos(R, m, cara)
    nariz(R, m, cara)
    boca(R, m, cara)


LIENZO = (170, 170, 85, 94)        # ancho, alto y origen del lienzo de la cabeza, en unidades


def retrato(cara, escala=0.85, k=8, colores=32):
    R = Retrato(k=k, ancho=LIENZO[0], alto=LIENZO[1], ox=LIENZO[2], oy=LIENZO[3])
    cabeza(R, cara)
    return R.final(escala, colores)


CARAS = dict(
    serio=dict(ceno=0.7, mira=-0.6, sonrisa=0.0),
    pillo=dict(ceno=0.2, alza=1.0, mira=-0.9, sonrisa=1.0, abre=0.85),
    enfado=dict(ceno=1.6, mira=-0.3, boca='grito', abre_boca=10, ojo_rojo=False, abre=1.1),
    calculador=dict(ceno=0.5, ojo='cerrado', sonrisa=0.5),
    furia=dict(ceno=1.8, mira=0.0, boca='grito', abre_boca=12, ojo_rojo=True, abre=1.2),
    susto=dict(ceno=-1.0, ojo='grande', mira=0.0, boca='grito', abre_boca=7),
)
