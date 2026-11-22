"""
=============================================================================
ESTRATOS - NEFANYAMUTO: LA CABEZA
=============================================================================
La cabeza en tres cuartos mirando a la izquierda, como la de Trumpzilla, pintada
con capas difuminadas (recortadas por cada forma) y contorno de tinta. Se dibuja
en "unidades" de cabeza: la cara mide unas 64 de ancho, el origen entre los ojos y
la y hacia abajo. retrato() la da reducida a pixel art; lienzo() la da a la
resolucion de trabajo para montarla sobre el cuerpo.

La caricatura: cabeza ancha y cuadrada, canas cortas peinadas hacia atras con
entradas, cejas gruesas muy bajas sobre ojos entornados que miran torcido (mala
leche), la nariz ancha y carnosa con la punta partida por una hendidura (como un
capullo), surcos hondos, la boca ancha de labios finos con las comisuras caidas,
carrillos y orejas de soplillo enormes (en vuelo hacen de alas).
=============================================================================
"""

from PIL import Image, ImageChops, ImageDraw, ImageFilter

TINTA = (28, 16, 18)
PIEL = (216, 150, 118)
PIEL_LUZ = (240, 190, 152)
PIEL_BRILLO = (252, 220, 190)
PIEL_OSC = (182, 110, 86)
PIEL_SOMBRA = (138, 76, 62)
PIEL_HONDA = (88, 42, 40)
ROJEZ = (206, 92, 80)
OREJA_DENTRO = (176, 86, 76)
CANA = (168, 170, 178)
CANA_LUZ = (222, 224, 230)
CANA_OSC = (112, 114, 124)
CANA_HONDA = (68, 70, 80)
CEJA = (46, 42, 46)
CEJA_LUZ = (104, 100, 104)
BLANCO_OJO = (214, 204, 188)
IRIS = (70, 54, 42)
PUPILA = (14, 10, 10)
ROJO_OJO = (255, 50, 20)
LABIO = (160, 84, 78)
LABIO_OSC = (110, 52, 52)
BOCA = (62, 16, 22)
DIENTE = (232, 224, 204)
LENGUA = (184, 76, 84)
CAMISA = (236, 238, 242)
CAMISA_OSC = (178, 184, 200)


def bez(p0, p1, p2, n=10):
    out = []
    for k in range(n + 1):
        t = k / float(n)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out


class Lienzo(object):
    """Lienzo pintado en unidades: x de -ox a ancho - ox, y de -oy a alto - oy; k pixeles
    por unidad. Sirve para la cabeza y para el cuerpo."""

    def __init__(self, k=8, ancho=140, alto=140, ox=70, oy=70):
        self.k, self.ox, self.oy = k, ox, oy
        self.W, self.H = int(ancho * k), int(alto * k)
        self.ancho, self.alto = ancho, alto
        self.im = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [((x + self.ox) * self.k, (y + self.oy) * self.k) for x, y in pts]

    # mascaras
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

    def mover(self, m, dx, dy):
        return ImageChops.offset(m, int(dx * self.k), int(dy * self.k))

    # pintar
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

    def volumen(self, m, luz, osc, d=3.0, blur=1.5, a_luz=0.8, a_osc=0.9, honda=None, dh=None):
        """Sombra en el borde de abajo a la derecha y luz en el de arriba a la
        izquierda (la luz viene de arriba a la izquierda)."""
        sombra = ImageChops.subtract(m, self.mover(m, -d, -d))
        self.pintar(sombra, osc, blur, m, a_osc)
        if honda is not None:
            dh = dh or d * 0.45
            self.pintar(ImageChops.subtract(m, self.mover(m, -dh, -dh)), honda, blur * 0.6, m, a_osc)
        if luz is not None:
            brillo = ImageChops.subtract(m, self.mover(m, d * 0.7, d * 0.7))
            self.pintar(brillo, luz, blur, m, a_luz)

    def forma(self, pts, col, luz=None, osc=None, d=3.0, blur=1.5, borde=1.2, honda=None, a_luz=0.8, a_osc=0.9):
        m = self.m_poli(pts)
        self.pintar(m, col)
        if osc is not None:
            self.volumen(m, luz, osc, d, blur, a_luz, a_osc, honda)
        if borde > 0:
            self.linea(pts + pts[:1], TINTA, borde)
        return m

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

    def final(self, escala, colores=40):
        w, h = max(1, int(round(self.ancho * escala))), max(1, int(round(self.alto * escala)))
        return pixelar(self.im.resize((w, h), Image.LANCZOS), colores)


Retrato = Lienzo


def pixelar(im, colores=48, contorno=True):
    """Recorte duro, paleta adaptada sin tramado y (contorno) un pixel de tinta
    alrededor de la silueta: el acabado arcade."""
    a = im.split()[3].point(lambda v: 255 if v >= 110 else 0)
    fondo = Image.new('RGBA', im.size, (150, 110, 100, 255))
    fondo.alpha_composite(im)
    q = fondo.convert('RGB').quantize(colors=colores, method=Image.Quantize.MEDIANCUT,
                                      dither=Image.Dither.NONE).convert('RGBA')
    q.putalpha(a)
    if contorno:
        borde = a.filter(ImageFilter.MaxFilter(3))
        anillo = ImageChops.subtract(borde, a)
        tinta = Image.new('RGBA', im.size, TINTA + (255,))
        tinta.putalpha(anillo)
        q.alpha_composite(tinta)
    return q


# --- las partes -------------------------------------------------------------------

OREJA_D = [(31, -18), (40, -30), (55, -36), (68, -32), (75, -20), (75, -4), (69, 10), (59, 17), (53, 25),
           (46, 30), (38, 28), (33, 21)]


def oreja(R, lado, tam, ala=0.0):
    """Oreja de soplillo: helice gruesa, concha honda, antihelix y lobulo. lado +1 la
    de cerca (derecha), -1 la de lejos (mas estrecha por el escorzo). tam la agranda;
    ala (0..1) la abre hacia arriba como un ala."""
    ax = 31.0

    def X(p):
        x, y = p
        d = (x - ax) * tam
        y = y * (0.8 + 0.2 * tam) - ala * 0.6 * d * (1 - (y + 30) / 70.0)
        if lado > 0:
            return (ax + d, y)
        return (-28 - d * 0.78, y + 1)
    pts = [X(p) for p in OREJA_D]
    m = R.m_poli(pts)
    R.pintar(m, PIEL)
    R.volumen(m, PIEL_LUZ, PIEL_OSC, 3.0, 1.2)
    R.pintar(R.m_linea([pts[0], pts[-1]], 7), PIEL_SOMBRA, 2.0, m, 0.95)
    concha = [X(p) for p in ((36, -12), (47, -24), (61, -26), (68, -12), (64, 5), (54, 12), (44, 14), (37, 8))]
    R.pintar(R.m_poli(concha), OREJA_DENTRO, 0.6, m, 0.95)
    R.pintar(R.m_poli([X(p) for p in ((38, -6), (46, -10), (53, -1), (49, 10), (40, 10))]), PIEL_HONDA, 1.4, m, 0.85)
    R.pintar(R.m_linea([X(p) for p in ((56, 10), (62, -2), (60, -14), (52, -22))], 3.0), PIEL_LUZ, 0.8, m, 0.8)
    R.linea([X(p) for p in ((40, -25), (55, -31), (67, -27), (71, -14), (70, 2), (62, 11))], PIEL_SOMBRA, 1.0)
    R.pintar(R.m_elipse(*X((46, 22)), 4, 4), ROJEZ, 1.5, m, 0.5)
    R.elipse(*X((35, 4)), 2.2, 3.0, PIEL_OSC)
    R.linea(pts + pts[:1], TINTA, 1.4)


# cabeza ancha y cuadrada, carrillos que cuelgan junto a la barbilla
CARA = (bez((-24, -31), (-30, -16), (-30, 0)) + bez((-30, 0), (-32, 16), (-30, 28))
        + bez((-30, 28), (-31, 42), (-19, 48)) + bez((-19, 48), (-4, 55), (12, 51))
        + bez((12, 51), (31, 45), (33, 28)) + bez((33, 28), (37, 10), (35, -6))
        + bez((35, -6), (34, -22), (28, -32))
        + [(22, -36), (14, -38), (6, -39), (0, -42), (-6, -40), (-13, -38), (-19, -35)])

PELO = (bez((-26, -24), (-34, -42), (-24, -52)) + [(-20, -55), (-14, -54), (-10, -58), (-2, -57), (2, -60),
        (10, -59), (16, -61), (24, -57), (30, -53), (36, -46), (40, -36), (42, -22), (40, -6), (36, 2), (31, -4),
        (29, -28), (-21, -32)])


def pelo(R):
    m = R.m_poli(PELO)
    R.pintar(m, CANA)
    R.pintar(R.m_poli([(14, -66), (50, -48), (46, 6), (26, 0), (20, -38)]), CANA_OSC, 4, m, 0.95)
    R.pintar(R.m_poli([(30, -48), (50, -38), (46, 6), (32, 0)]), CANA_HONDA, 3, m, 0.8)
    R.pintar(R.m_elipse(-10, -52, 12, 5), CANA_LUZ, 2.5, m, 1.0)
    tupe = [(-22, -34), (-27, -44), (-20, -53), (-8, -57), (4, -57), (12, -51), (6, -45), (-6, -43), (-14, -39)]
    R.pintar(R.m_poli(tupe), CANA_LUZ, 1.0, m, 0.85)
    for a, b, c, col, w in (((-16, -40), (-4, -54), (18, -56), CANA_OSC, 1.0), ((-4, -44), (12, -54), (30, -48), CANA_HONDA, 1.1),
                            ((-24, -34), (-26, -46), (-10, -54), CANA_OSC, 0.9), ((6, -44), (24, -48), (38, -32), CANA_HONDA, 1.1),
                            ((-14, -48), (0, -58), (16, -58), CANA_LUZ, 1.2), ((16, -42), (32, -42), (40, -18), CANA_HONDA, 1.1),
                            ((0, -50), (18, -56), (34, -44), CANA_LUZ, 0.9), ((20, -34), (34, -32), (38, -10), CANA_OSC, 0.9)):
        R.linea(bez(a, b, c, 8), col, w)
    R.linea(PELO + PELO[:1], TINTA, 1.4)
    # patillas cortas, rapadas sobre las orejas
    for pts in ([(-29, 2), (-32, -16), (-26, -27), (-24, -14), (-26, -2)], [(32, 2), (36, -14), (29, -28), (27, -14), (29, 0)]):
        mm = R.m_poli(pts)
        R.pintar(mm, CANA_OSC)
        R.pintar(mm, CANA, 1.0, R.mover(mm, -1, -1), 0.7)


def cara_base(R, cara):
    m = R.m_poli(CARA)
    R.pintar(m, PIEL)
    # el lado derecho en sombra, las sienes, bajo los pomulos, carrillos y papada
    R.pintar(R.m_poli([(16, -40), (40, -30), (40, 54), (6, 56), (14, 30), (20, 0)]), PIEL_OSC, 4, m, 0.95)
    R.pintar(R.m_poli([(24, -10), (40, -10), (40, 50), (14, 52)]), PIEL_SOMBRA, 3.5, m, 0.75)
    R.pintar(R.m_elipse(-28, -16, 5, 10), PIEL_OSC, 3, m, 0.8)
    R.pintar(R.m_elipse(-25, 14, 5, 9), PIEL_OSC, 3, m, 0.7)
    R.pintar(R.m_elipse(19, 16, 5, 9), PIEL_SOMBRA, 3, m, 0.6)
    R.pintar(R.m_linea(bez((-29, 26), (-28, 42), (-16, 47)), 5), PIEL_SOMBRA, 2.2, m, 0.85)
    R.pintar(R.m_linea(bez((30, 24), (28, 42), (12, 50)), 6), PIEL_SOMBRA, 2.2, m, 0.95)
    R.pintar(R.m_linea(bez((-16, 52), (-2, 57), (14, 52)), 3), PIEL_HONDA, 1.3, m, 0.9)
    R.linea(bez((-27, 34), (-24, 45), (-16, 47), 6), PIEL_HONDA, 1.0)
    R.linea(bez((28, 34), (24, 46), (15, 50), 6), PIEL_HONDA, 1.0)
    # luces: frente, pomulo izquierdo, barbilla
    R.pintar(R.m_elipse(-8, -28, 13, 5), PIEL_LUZ, 3.5, m, 0.9)
    R.pintar(R.m_elipse(-12, -30, 6, 2.5), PIEL_BRILLO, 1.6, m, 0.8)
    R.pintar(R.m_elipse(-21, 6, 5, 4), PIEL_LUZ, 2.5, m, 0.7)
    R.pintar(R.m_elipse(-4, 49, 7, 3), PIEL_LUZ, 1.4, m, 0.7)
    R.pintar(R.m_elipse(-22, 16, 6, 5), ROJEZ, 3.5, m, 0.35)
    R.pintar(R.m_elipse(15, 16, 6, 5), ROJEZ, 3.5, m, 0.3)
    # la frente fruncida: dos arrugas largas y las del entrecejo
    for k in range(2):
        y = -24 - k * 5
        R.linea(bez((-16 + k * 2, y + 1), (-2, y - 1.8 - cara.get('ceno', 0.8)), (16 - k * 2, y + 0.5), 8), PIEL_SOMBRA, 0.9)
        R.linea(bez((-15 + k * 2, y + 2), (-2, y - 0.6), (15 - k * 2, y + 1.5), 8), PIEL_LUZ, 0.6)
    R.linea(CARA + CARA[:1], TINTA, 1.6)
    return m


def cejas(R, m, cara):
    """Gruesas, oscuras, muy bajas: casi tocan el ojo. ceno baja las puntas de
    dentro; alza sube la de cerca (el pillo)."""
    ceno = cara.get('ceno', 0.8)
    alza = cara.get('alza', 0.0)
    cerca = [(0, -9 + ceno * 2.6), (8, -13 - alza * 4), (18, -13.5 - alza * 3), (25, -9 - alza * 1.2),
             (19, -9.6 - alza * 2.4), (9, -9.4 - alza * 3.2), (1, -5.6 + ceno * 2.6)]
    lejos = [(-6, -9 + ceno * 2.6), (-14, -13), (-22, -12), (-27, -7.5), (-22, -8.8), (-14, -9.4), (-7, -5.6 + ceno * 2.6)]
    for pts in (cerca, lejos):
        R.pintar(R.m_poli([(x, y + 3.2) for x, y in pts]), PIEL_HONDA, 1.6, m, 0.85)
        R.poli(pts, CEJA)
        R.linea(pts[:4], CEJA_LUZ, 0.8)
        R.linea(pts + pts[:1], TINTA, 0.6)
    if ceno > 0.4:
        for x in (-4, -1.5):
            R.linea([(x, -13), (x + 0.5, -5)], PIEL_HONDA, 1.0)
        R.pintar(R.m_elipse(-2.5, -9, 3, 4), PIEL_SOMBRA, 1.2, m, 0.6)


def ojo(R, m, cx, cy, w, cara, lejos=False):
    """Entornado, de parpado gordo, mirando de reojo: la mala leche."""
    h = cara.get('abre', 1.0) * 4.0
    tipo = cara.get('ojo', 'normal')
    R.pintar(R.m_elipse(cx, cy - 0.5, w * 0.8, 5.5), PIEL_HONDA, 2.0, m, 0.75)       # la cuenca
    R.pintar(R.m_linea(bez((cx - w * 0.5, cy + 3), (cx, cy + 6.5), (cx + w * 0.55, cy + 2.5)), 2.4), PIEL_SOMBRA, 1.2, m, 0.9)
    R.linea(bez((cx - w * 0.4, cy + 5), (cx + 1, cy + 8), (cx + w * 0.55, cy + 4), 6), PIEL_SOMBRA, 0.8)
    if cara.get('ojo_rojo'):
        R.pintar(R.m_elipse(cx, cy, w * 0.75, 5), ROJO_OJO, 1.8, m, 0.6)
    if tipo == 'cerrado':
        R.linea(bez((cx - w * 0.5, cy), (cx, cy + 1.4), (cx + w * 0.5, cy - 0.4), 6), TINTA, 1.4)
        return
    big = 2.0 if tipo == 'grande' else 1.0
    almendra = bez((cx - w * 0.5, cy), (cx, cy - h * 1.2 * big), (cx + w * 0.5, cy + 0.5), 8) + \
        bez((cx + w * 0.5, cy + 0.5), (cx, cy + h * 0.9 * big), (cx - w * 0.5, cy), 8)
    me = R.m_poli(almendra)
    R.pintar(me, BLANCO_OJO)
    mira = cara.get('mira', -0.6)
    ix = cx + mira * w * 0.26
    R.pintar(R.m_elipse(ix, cy + 0.6, 3.4, 3.4), ROJO_OJO if cara.get('ojo_rojo') else IRIS, 0, me)
    R.pintar(R.m_elipse(ix, cy + 0.6, 1.8, 1.8), PUPILA, 0, me)
    R.pintar(R.m_elipse(ix - 1.0, cy - 0.6, 0.6, 0.6), (250, 250, 250), 0, me)
    # sombra del parpado sobre el ojo
    R.pintar(R.m_elipse(cx, cy - h, w * 0.6, h), PIEL_HONDA, 0.6, me, 0.5)
    # el parpado de arriba: pesado, tapa la mitad del iris y cae por fuera
    if big < 1.5:
        parp = bez((cx - w * 0.62, cy - 0.6), (cx - w * 0.05, cy - h * 1.15), (cx + w * 0.64, cy + 0.6), 8) + \
            [(cx + w * 0.64, cy - 5.5), (cx - w * 0.62, cy - 6.0)]
        R.poli(parp, PIEL_OSC)
        R.pintar(R.m_poli(parp), PIEL_SOMBRA, 0.8, R.m_poli(parp), 0.6)
        R.linea(parp[:9], TINTA, 1.7)
    else:
        R.linea(almendra[:9], TINTA, 1.3)
    R.linea(bez((cx - w * 0.5, cy + 0.2), (cx, cy + h * 0.9 * big), (cx + w * 0.5, cy + 0.6), 6), PIEL_HONDA, 0.7)
    if not lejos:
        for k in (-1, 0, 1):
            R.linea([(cx + w * 0.7, cy + k * 1.6), (cx + w * 0.7 + 3.5, cy + k * 2.4)], PIEL_SOMBRA, 0.6)


def nariz(R, m, cara):
    """Ancha y carnosa; la punta en dos lobulos partidos por una hendidura (un
    capullo). f la agranda desde el puente."""
    f = cara.get('nariz', 1.3)
    pv = (-6.0, -8.0)

    def T(pts):
        return [(pv[0] + (x - pv[0]) * f, pv[1] + (y - pv[1]) * f) for x, y in pts]

    def E(cx, cy, rx, ry):
        (cx, cy), = T([(cx, cy)])
        return cx, cy, rx * f, ry * f
    # el puente: sombra a la derecha, luz a la izquierda, el perfil
    R.pintar(R.m_poli(T([(-4, -8), (0, -8), (3, 10), (-1, 14)])), PIEL_OSC, 1.5, m, 0.9)
    R.pintar(R.m_linea(T([(-6, -3), (-10, 10)]), 2.4), PIEL_LUZ, 1.0, m, 0.9)
    R.linea(T(bez((-9, 4), (-12, 9), (-15, 13), 4)), PIEL_SOMBRA, 1.0)
    # las aletas, anchas
    for ax, ay in ((-19, 20.5), (2, 20.5)):
        me = R.m_elipse(*E(ax, ay, 4.0, 3.4))
        R.pintar(me, PIEL)
        R.pintar(R.mover(me, 0.6, 0.6), PIEL_OSC, 1.0, me, 0.85)
        R.linea(T(bez((ax - 3.6, ay + 2.4), (ax, ay - 4.6), (ax + 3.6, ay + 2.4), 6)), PIEL_SOMBRA, 1.0)
    R.pintar(R.m_elipse(*E(-8, 26, 12, 3)), PIEL_HONDA, 1.8, m, 0.85)            # sombra debajo
    # los dos lobulos
    mn = R.m_elipse(*E(-12.5, 18, 5.4, 5.8))
    mn = R.m_elipse(*E(-3.5, 18.5, 5.2, 5.6), mn)
    R.pintar(mn, PIEL)
    R.pintar(R.m_elipse(*E(-1, 20, 4, 5)), PIEL_OSC, 1.4, mn, 0.95)
    R.pintar(R.m_elipse(*E(-11, 22.5, 5, 2.4)), PIEL_OSC, 1.0, mn, 0.8)
    R.pintar(R.m_elipse(*E(-11, 17, 5, 5)), ROJEZ, 1.8, mn, 0.5)
    R.pintar(R.m_elipse(*E(-4, 17, 4, 4)), ROJEZ, 1.8, mn, 0.4)
    R.pintar(R.m_elipse(*E(-14, 15.5, 1.6, 1.4)), PIEL_BRILLO, 0.5, mn, 1.0)
    R.pintar(R.m_elipse(*E(-5.5, 15.5, 1.3, 1.1)), PIEL_LUZ, 0.5, mn, 1.0)
    # la hendidura: casi la parte en dos
    R.pintar(R.m_linea(T([(-8, 12.5), (-8, 23.5)]), 2.6), PIEL_SOMBRA, 0.6, mn, 1.0)
    R.linea(T([(-8, 14), (-8.2, 24)]), PIEL_HONDA, 1.2)
    R.linea(T(bez((-18, 15), (-19, 22), (-14, 24.2), 5)), TINTA, 1.2)
    R.linea(T(bez((-14, 24.2), (-8, 24.8), (-2, 24.2), 5)), TINTA, 1.3)
    R.linea(T(bez((-2, 24.2), (2.5, 21), (1.5, 15), 5)), PIEL_HONDA, 1.1)
    R.elipse(*E(-14.5, 23.4, 1.9, 1.0), PIEL_HONDA)
    R.elipse(*E(-2.0, 23.4, 1.7, 1.0), PIEL_HONDA)


def surcos(R, m, cara):
    for a, b, c in (((-24, 26), (-30, 36), (-27, 46)), ((7, 26), (14, 36), (12, 48))):
        R.pintar(R.m_linea(bez(a, b, c), 3.2), PIEL_SOMBRA, 1.3, m, 0.95)
        R.linea(bez(a, b, c, 8), PIEL_HONDA, 1.1)
        R.pintar(R.m_linea(bez((a[0] - 2.5, a[1] + 2), (b[0] - 2.5, b[1]), (c[0] - 1.5, c[1])), 2.0), PIEL_LUZ, 1.0, m, 0.6)


def boca(R, m, cara):
    tipo = cara.get('boca', 'seria')
    y = 39
    if tipo == 'grito':
        abre = cara.get('abre_boca', 9)
        top = bez((-21, y + 4), (-8, y - 4), (6, y + 4), 8)
        bot = bez((6, y + 4), (4, y + abre + 1), (-8, y + abre + 1), 5) + bez((-8, y + abre + 1), (-19, y + abre + 1), (-21, y + 4), 5)
        R.poli(top + bot, BOCA)
        mb = R.m_poli(top + bot)
        R.pintar(R.m_poli([(-17, y - 3), (3, y - 3), (3, y + 2.6), (-17, y + 2.6)]), DIENTE, 0, mb)
        for x in (-11, -5):
            R.linea([(x, y - 2), (x, y + 1.4)], LABIO_OSC, 0.5)
        R.pintar(R.m_poli([(-14, y + abre - 1.5), (-2, y + abre - 1.5), (-2, y + abre + 2), (-14, y + abre + 2)]), DIENTE, 0, mb, 0.8)
        R.pintar(R.m_elipse(-8, y + abre - 2, 6, 2.5), LENGUA, 0.6, mb, 0.9)
        R.linea(top, LABIO, 1.4)
        R.linea(top + bot + top[:1], TINTA, 0.9)
        R.pintar(R.m_elipse(-8, y + abre + 5, 9, 2.5), PIEL_SOMBRA, 1.4, m, 0.85)
        return
    sonr = cara.get('sonrisa', 0.0)
    izq = (-22, y + 3)
    der = (7, y + 3 - sonr * 5)
    centro = (-8, y - 0.6)
    sup = bez(izq, (-14, y - 2.0), centro, 5) + bez(centro, (-1, y - 1.8 - sonr * 1.5), der, 5)
    inf = bez(der, (-6, y + 5.0 - sonr * 2), izq, 8)
    mb = R.m_poli(sup + inf)
    R.pintar(mb, LABIO)
    R.pintar(R.m_poli(inf + [centro]), PIEL_LUZ, 0.8, mb, 0.3)
    R.linea(bez(izq, (-8, y + 1.2 - sonr * 1.2), der, 8), TINTA, 1.3)
    for p in (izq, der):
        R.pintar(R.m_elipse(p[0], p[1] + 1, 2.2, 2.2), PIEL_HONDA, 0.9, m, 0.9)
    R.pintar(R.m_elipse(-8, y + 7, 7, 2.2), PIEL_SOMBRA, 1.4, m, 0.85)
    if sonr > 0.3:
        R.linea(bez((der[0] - 1, der[1] - 1), (der[0] + 3, der[1] - 1), (der[0] + 3, der[1] + 3), 4), PIEL_SOMBRA, 0.9)


def cuello(R):
    pts = [(-20, 46), (-6, 58), (14, 48), (22, 60), (-2, 68), (-26, 58)]
    mm = R.m_poli(pts)
    R.pintar(mm, CAMISA)
    R.pintar(R.m_poli([(4, 50), (24, 54), (22, 64), (0, 66)]), CAMISA_OSC, 2, mm, 0.9)
    R.pintar(R.m_elipse(-2, 54, 22, 6), PIEL_HONDA, 2.5, mm, 0.6)
    R.linea(pts + pts[:1], TINTA, 1.1)


def cabeza(R, cara):
    oreja(R, -1, cara.get('orejas', 1.0), cara.get('ala', 0.0))
    oreja(R, 1, cara.get('orejas', 1.0), cara.get('ala', 0.0))
    cuello(R)
    pelo(R)
    m = cara_base(R, cara)
    surcos(R, m, cara)
    ojo(R, m, -14.5, -3, 10.5, cara, lejos=True)
    ojo(R, m, 11, -3, 13.0, cara)
    cejas(R, m, cara)
    nariz(R, m, cara)
    boca(R, m, cara)


LIENZO = (190, 190, 95, 104)        # ancho, alto y origen del lienzo de la cabeza, en unidades


def lienzo(cara, k):
    """La cabeza pintada a k pixeles por unidad (sin reducir), en un Lienzo."""
    R = Lienzo(k=k, ancho=LIENZO[0], alto=LIENZO[1], ox=LIENZO[2], oy=LIENZO[3])
    cabeza(R, cara)
    return R


def retrato(cara, escala=0.85, k=8, colores=40):
    return lienzo(cara, k).final(escala, colores)


CARAS = dict(
    serio=dict(ceno=1.0, mira=-0.6),
    pillo=dict(ceno=0.3, alza=1.0, mira=-0.9, sonrisa=1.0, abre=0.85),
    enfado=dict(ceno=1.8, mira=-0.3, boca='grito', abre_boca=10, abre=1.05),
    calculador=dict(ceno=0.6, ojo='cerrado', sonrisa=0.5),
    furia=dict(ceno=2.0, mira=0.0, boca='grito', abre_boca=12, ojo_rojo=True, abre=1.15),
    susto=dict(ceno=-1.0, ojo='grande', mira=0.0, boca='grito', abre_boca=7),
)
