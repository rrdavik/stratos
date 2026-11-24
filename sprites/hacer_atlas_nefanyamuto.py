"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DE NEFANYAMUTO
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/nefanyamuto_emociones.png (y la lamina de prueba) desde las imagenes de
origen (JPG de 1024 x 1024 en pixel art, con la ciudad en llamas de fondo):

    python3 sprites/hacer_atlas_nefanyamuto.py frente.jpg grita_rie.jpg dientes_llora.jpg fotos.webp

  frente.jpg         una figura de frente, brazos largos, la boca abierta (de ella sale la cara seria)
  grita_rie.jpg      dos figuras: grita con los ojos cerrados (izq.) y se rie (der.)
  dientes_llora.jpg  dos figuras: aprieta los dientes (izq.) y llora de risa (der.)
  fotos.webp         el collage de cinco fotos (1680 x 1500): se tapa la nariz, los dos
                     indices, se rasca la cabeza, el atril, habla tranquilo

De las fotos se usa la cabeza (FOTOS: el recorte y la elipse de cada una), con el
color pasado al de las cabezas pintadas y las lineas marcadas, sobre uno de los
cuerpos (CUERPO_FOTO); las manos que hacen el gesto (el indice levantado, la mano
en la cabeza, los dos indices que apuntan) entran pasadas al color del monstruo,
como garras suyas. Los ojos bizcos y el dedo en la nariz se pintan, y a todas se
les pintan detras las dos patas largas que le faltan al cuerpo para ser un MUTO
(seis extremidades): suben de los hombros a una rodilla alta y bajan al suelo
con el garfio hacia dentro (patas_muto). Las doce caras
(EMOCIONES) llenan las 4 x 3 celdas: las diez de EMOCIONES_MON y dos en las que no
se entera de nada (despiste: bizco; pasmado: hurgandose la nariz).

Necesita Pillow, NumPy, SciPy y rembg (el modelo isnet-general-use se baja la
primera vez a ~/.rembg).

Que hace:
  1. Quita el fondo con rembg y deja el recorte duro (alfa 0 o 255).
  2. Quita los restos del fondo pegados al borde: llamas (naranja y amarillo
     muy saturados que tocan el exterior; el saco del pecho, rodeado de cuerpo,
     se queda) y las islas sueltas.
  3. Separa las dos figuras de cada imagen por la costura vertical que menos
     figura corta (se tocan por las colas).
  4. Las caras que faltan se sacan de las que hay: serio = la cabeza de
     frente.jpg sobre el cuerpo que aprieta los dientes; furia = el grito con la
     cara roja (como la de Trumpzilla).
  5. Mete cada figura en su celda (CELDA_W x CELDA_H) a la misma escala, con los
     pies abajo y centrada, la reduce, le pasa una paleta adaptada y le pone el
     contorno de un pixel. Escribe el atlas (COLS x FILAS, en el orden de
     EMOCIONES, de arriba a la izquierda) y la lamina de prueba sobre gris.

El formato y el orden son los de Trumpzilla y Godzilla (EMOCIONES_MON del
motor): el mismo shader sirve. Las figuras miran de frente; el shader las
voltea al andar a la derecha.
=============================================================================
"""

import os
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from scipy import ndimage

from igualar_brillo import igualar, lamina as lamina_igualada     # la misma claridad para todos los monstruos

AQUI = os.path.dirname(os.path.abspath(__file__))
CELDA_W, CELDA_H = 192, 256
COLS, FILAS = 4, 3
MARGEN = 6
EMOCIONES = ['serio', 'enfado', 'furia', 'rie', 'carcajada', 'susto', 'mueca', 'llora', 'panico', 'calma',
             'despiste', 'pasmado']
TINTA = (24, 12, 12)

# de que figura sale cada cara, y su adorno
ORIGEN = dict(
    serio=('serio', None),            # cabeza de frente.jpg sobre el cuerpo de 'dientes'
    enfado=('enfado_puno', 'golpe'),  # aprieta los dientes y se golpea la palma con el puno
    furia=('furia', None),            # el grito con la cara roja
    rie=('rie', None),
    carcajada=('carcajada', 'jaja'),  # se parte de risa (sin las lagrimas)
    susto=('f_dedos', 'sudor'),       # foto: grita con los dos indices
    mueca=('f_atril', None),          # foto: grita en el atril con el indice levantado
    llora=('f_nariz', None),          # foto: reflexivo, los dedos en la boca (la mano es la de su brazo)
    panico=('grito', 'sudor'),
    calma=('f_rasca', None),          # foto: se rasca la cabeza con la garra, sonrie
    despiste=('bizco', 'pregunta'),   # bizco (no se entera)
    pasmado=('f_calma', None),        # foto: hurgandose la nariz (no se entera)
)
# la gorra plana de campo, ladeada: en que caras y hacia que lado cae (+1 a la derecha de la imagen)
GORRA = dict(rie=1, susto=-1, despiste=1)
# el cuerpo sobre el que va cada cabeza de foto
CUERPO_FOTO = dict(dedos='grito', atril='dientes', nariz='grito', calma='rie', rasca='rie')
BAJA_FOTO = dict(nariz=0.05, rasca=0.08)
# brazos y manos de las fotos que entran con la cabeza (poligonos en el recorte):
# se pasan al color del monstruo, como garras suyas. En MANO_DENTRO la mano esta
# delante de la cara y se toma tambien dentro de la elipse.
BRAZOS_FOTO = dict(
    atril=[(222, 6), (300, 6), (300, 135), (236, 135)],                     # el indice levantado
    rasca=[(118, 18), (292, 18), (292, 118), (225, 215), (138, 236), (96, 204)],   # la mano en la cabeza
    nariz=[(30, 236), (236, 236), (236, 300), (160, 400), (20, 400)],      # la mano bajo la nariz
)
MANO_DENTRO = ('nariz',)
# el antebrazo de monstruo que se dibuja bajo esas manos: muneca, salida y grosor (en anchos de cabeza)
ANTEBRAZO_FOTO = dict(atril=((262, 116), (272, 150), 0.12), rasca=((152, 196), (126, 222), 0.12))
# brazos del cuerpo que se rehacen para que acaben en la mano de la cara: (figura,
# poligono del antebrazo y el puno que se borran, de donde sale el antebrazo nuevo;
# en pixeles desde la esquina de la figura) y a que punto de la foto va (la muneca)
BRAZO_NUEVO = dict(
    nariz=('grito', [(52, 432), (165, 432), (165, 562), (52, 562)], (38, 446), (70, 372)),
    calma=('rie', [(0, 288), (98, 288), (98, 398), (0, 398)], (52, 402), None),     # va al puno del dedo
)
# el puno de 'grito' (recuadro desde su esquina) que se pone sobre la garra izquierda
# de 'llora_risa' (centro y ancho), golpeando la otra garra
PUNO_GRITO = (58, 440, 162, 560)
PUNO_SOBRE = ((158, 468), 132)
# las lagrimas de la carcajada (recuadro desde la esquina de 'llora_risa')
LAGRIMAS = (108, 120, 290, 215)
# las manos que apuntan de la foto de los dos indices (poligono en su recorte); van
# juntas sobre el pecho, del ancho de MANOS_ANCHO cabezas y con su centro MANOS_BAJA
# cabezas por debajo de los hombros
MANOS_DEDOS = [(58, 268), (262, 268), (262, 432), (58, 432)]
MANOS_ANCHO, MANOS_BAJA = 1.15, 0.85
# bizco: los dos ojos (centros) y su radio, en el recorte de la foto o en frente.jpg
BIZCO_FOTO = dict()
BIZCO_FRENTE = ((464, 256), (542, 255), 15)
# hurgarse la nariz: la fosa y el puno, en el recorte de la foto
MOCO_FOTO = dict(calma=dict(fosa=(219, 136), puno=(186, 206)))
# el ancho de la cabeza medido a mano donde la mano o la inclinacion enganan a la medida
ANCHO_FOTO = dict(rasca=185.0)


# --- recorte ----------------------------------------------------------------------

def sin_fondo(ruta):
    from rembg import new_session, remove
    global _SESION
    try:
        _SESION
    except NameError:
        _SESION = new_session('isnet-general-use')
    if ruta is None:
        return None
    im = Image.open(ruta).convert('RGB')
    out = np.array(remove(im, session=_SESION))
    out[..., 3] = np.where(out[..., 3] >= 128, 255, 0)
    return out


def limpia(rgba):
    """Quita las llamas pegadas al borde y las islas: deja la mancha grande."""
    a = rgba[..., 3] > 0
    # los agujeros pequenos dentro de la figura (rembg vacia lo muy brillante, como
    # el centro del saco) se rellenan con su color; los huecos grandes (entre
    # brazos y cuerpo, entre las piernas) son fondo y se quedan
    hueco = ndimage.binary_fill_holes(a) & ~a
    lab, n = ndimage.label(hueco)
    if n:
        tam = ndimage.sum(hueco, lab, range(1, n + 1))
        a |= np.isin(lab, 1 + np.nonzero(tam < 1500)[0])
    r, g, b = [rgba[..., k].astype(int) for k in range(3)]
    fuego = (r > 170) & (g > 70) & (b < 110) & (r - b > 110)
    for _ in range(3):
        fuera = ndimage.binary_dilation(~ndimage.binary_fill_holes(a), iterations=2)
        lab, n = ndimage.label(fuego & a)
        if n == 0:
            break
        toca = np.unique(lab[fuera & (lab > 0)])
        quita = np.isin(lab, toca[toca > 0])
        if not quita.any():
            break
        a &= ~quita
    a &= ~fondo_atrapado(rgba, a)
    lab, n = ndimage.label(a)
    if n > 1:
        tam = ndimage.sum(a, lab, range(1, n + 1))
        a = lab == (1 + int(np.argmax(tam)))
    out = rgba.copy()
    out[..., 3] = np.where(a, 255, 0)
    return out


def fondo_atrapado(rgba, a):
    """El fondo que rembg deja dentro de un hueco del cuerpo (el lazo de la cola):
    manchas claras y gruesas (edificios, llamas) en la mitad de abajo de la figura
    y lejos del saco del pecho. Los filos de luz naranja del cuerpo son finos y
    se quedan."""
    ys, xs = np.nonzero(a)
    if len(ys) == 0:
        return np.zeros_like(a)
    y0, y1 = ys.min(), ys.max()
    xc = (xs.min() + xs.max()) / 2.0
    alto = float(y1 - y0)
    r, g, b = [rgba[..., k].astype(int) for k in range(3)]
    claro = a & (r > 140) & ((r + g + b) / 3 > 95)
    grueso = ndimage.binary_opening(claro, iterations=4)
    lab, n = ndimage.label(grueso)
    quita = np.zeros_like(a)
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        if m.sum() < 400:
            continue
        cy = (sl[0].start + sl[0].stop) / 2.0
        cx = (sl[1].start + sl[1].stop) / 2.0
        pecho = abs(cx - xc) < 0.12 * alto and y0 + 0.25 * alto < cy < y0 + 0.6 * alto
        if pecho or cy < y0 + 0.45 * alto:
            continue
        quita |= lab == i
    if quita.any():
        # cierra la mancha para llevarse tambien las rayas oscuras de dentro (ventanas)
        quita = ndimage.binary_closing(ndimage.binary_dilation(quita, iterations=3), iterations=10)
        quita = ndimage.binary_fill_holes(quita)
    return quita & a


def costura(a, x0, x1):
    """El camino de arriba abajo, entre x0 y x1, que corta menos figura (cada fila
    se mueve a lo sumo un pixel)."""
    coste = a[:, x0:x1].astype(float) * 10.0 + 0.01
    h, w = coste.shape
    acum = coste.copy()
    for y in range(1, h):
        prev = acum[y - 1]
        izq = np.r_[np.inf, prev[:-1]]
        der = np.r_[prev[1:], np.inf]
        acum[y] += np.minimum(np.minimum(izq, prev), der)
    xs = np.zeros(h, int)
    xs[-1] = int(np.argmin(acum[-1]))
    for y in range(h - 2, -1, -1):
        x = xs[y + 1]
        lo, hi = max(0, x - 1), min(w, x + 2)
        xs[y] = lo + int(np.argmin(acum[y, lo:hi]))
    return xs + x0


def separa(rgba, x0=420, x1=640):
    """Las dos figuras de una imagen: la de la izquierda y la de la derecha."""
    a = rgba[..., 3] > 0
    xs = costura(a, x0, x1)
    cols = np.arange(a.shape[1])[None, :]
    izq = cols < xs[:, None]
    out = []
    for lado in (izq, ~izq):
        f = rgba.copy()
        f[..., 3] = np.where(lado & a, 255, 0)
        out.append(limpia(f))
    return out


def caja(rgba):
    ys, xs = np.nonzero(rgba[..., 3])
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


# --- caras derivadas -------------------------------------------------------------------

def cara_roja(rgba, alto_cabeza=0.30):
    """La piel de la cabeza (el cuarto de arriba de la figura) hacia el rojo."""
    x0, y0, x1, y1 = caja(rgba)
    out = rgba.astype(float)
    yc = y0 + int((y1 - y0) * alto_cabeza)
    r, g, b = out[y0:yc, ..., 0], out[y0:yc, ..., 1], out[y0:yc, ..., 2]
    piel = (r > g + 15) & (g > b) & (r > 90)          # tonos de piel (no canas ni camisa)
    k = np.where(piel, 1.0, 0.0)
    k = ndimage.gaussian_filter(k, 1.5)
    baja = np.clip((yc - y0 - np.arange(yc - y0)) / (0.25 * (yc - y0)), 0, 1)[:, None]   # se apaga abajo
    k = k * baja
    out[y0:yc, ..., 0] = np.minimum(255, r + (255 - r) * 0.18 * k)
    out[y0:yc, ..., 1] = g * (1 - 0.32 * k)
    out[y0:yc, ..., 2] = b * (1 - 0.32 * k)
    return out.clip(0, 255).astype(np.uint8)


def medidas_cabeza(f):
    """(arriba, centro x, ancho de la cabeza, fila donde empiezan los hombros)."""
    a = f[..., 3] > 0
    x0, y0, x1, y1 = caja(f)
    ancho = []
    for dy in range(0, 320):
        c = np.nonzero(a[y0 + dy])[0]
        ancho.append((c.min(), c.max()) if len(c) else (0, -1))
    cab = [ancho[d][1] - ancho[d][0] for d in range(55, 95)]
    hw = float(np.median(cab))
    cx = (ancho[80][0] + ancho[80][1]) / 2.0
    hombro = next(d for d in range(110, 320) if ancho[d][1] - ancho[d][0] > 1.22 * hw)
    return y0, cx, hw, hombro


def pon_cabeza(cuerpo, donante):
    """La cabeza de otra figura de las imagenes (con el cuello de la camisa) sobre
    'cuerpo'."""
    dy0, dcx, dhw, dhom = medidas_cabeza(donante)
    alto = dhom + 72
    x0 = int(dcx - dhw * 0.62)
    trozo = donante[dy0:dy0 + alto, x0:int(dcx + dhw * 0.62) + 1].copy()
    # abajo se estrecha (el cuello de la camisa, no los hombros)
    yy = np.arange(trozo.shape[0])[:, None]
    xx = np.arange(trozo.shape[1])[None, :] + x0
    deja = np.abs(xx - dcx) < dhw * (0.62 - 0.22 * np.clip((yy - dhom - 30) / 42.0, 0, 1))
    trozo[..., 3] = np.where(deja, trozo[..., 3], 0)
    return injerta(cuerpo, trozo, dcx - x0, dhw)


def injerta(cuerpo, trozo, tcx, thw, baja=0.0):
    """Pega 'trozo' (una cabeza con alfa; su centro en x tcx, su coronilla arriba y
    su ancho de cabeza thw) sobre la cabeza de 'cuerpo', a la escala de esta. La
    cabeza vieja se borra hasta los hombros; debajo, solo lo que tapa la nueva.
    baja la desplaza hacia abajo (en anchos de cabeza)."""
    cy0, ccx, chw, chom = medidas_cabeza(cuerpo)
    s = chw / float(thw)
    t = Image.fromarray(trozo)
    t = t.resize((max(1, int(round(t.width * s))), max(1, int(round(t.height * s)))), Image.LANCZOS)
    tt = np.array(t)
    tt[..., 3] = np.where(tt[..., 3] >= 128, 255, 0)
    px, py = int(round(ccx - tcx * s)), int(round(cy0 + baja * chw))
    huella = np.zeros(cuerpo.shape[:2], bool)
    h, w = tt.shape[:2]
    y0c, x0c = max(0, py), max(0, px)
    huella[y0c:py + h, x0c:px + w] = tt[y0c - py:, x0c - px:, 3][:huella.shape[0] - y0c, :huella.shape[1] - x0c] > 0
    o = cuerpo.copy()
    yy = np.arange(o.shape[0])[:, None]
    xx = np.arange(o.shape[1])[None, :]
    vieja = ((yy < cy0 + chom) & (np.abs(xx - ccx) < chw * 0.56)) | huella
    o[..., 3] = np.where(vieja, 0, o[..., 3])
    out = Image.fromarray(o)
    out.alpha_composite(Image.fromarray(tt), (px, py), (max(0, -px), max(0, -py)))
    return np.array(out)


def donde_injerta(cuerpo, tcx, thw, baja=0.0):
    """La transformacion de injerta: (px, py, s), un punto (x, y) del trozo va a
    (px + x * s, py + y * s)."""
    cy0, ccx, chw, chom = medidas_cabeza(cuerpo)
    s = chw / float(thw)
    return ccx - tcx * s, cy0 + baja * chw, s


def rellena(rgb, m, vueltas=80):
    """Rellena los pixeles 'm' con el color de alrededor (difusion)."""
    out = rgb.astype(float)
    conocido = (~m).astype(float)
    out[m] = 0
    for _ in range(vueltas):
        suma = ndimage.uniform_filter(out * conocido[..., None], size=(5, 5, 1))
        peso = ndimage.uniform_filter(conocido, size=5)
        nuevo = suma / np.maximum(peso[..., None], 1e-6)
        out[m] = nuevo[m]
        conocido = np.where(m & (peso > 0), 1.0, conocido)
    return out.clip(0, 255).astype(np.uint8)


def sin_lagrimas(f):
    """La carcajada sin las lagrimas: los azules y blancos de la cara se pintan con
    la piel de alrededor."""
    x0, y0 = caja(f)[:2]
    a, b, c, d = LAGRIMAS
    out = f.copy()
    trozo = out[y0 + b:y0 + d, x0 + a:x0 + c]
    r, g, bl = [trozo[..., k].astype(int) for k in range(3)]
    agua = (trozo[..., 3] > 0) & (bl > r - 12) & (bl > 120)
    agua = ndimage.binary_dilation(agua, iterations=3)
    trozo[..., :3] = rellena(trozo[..., :3], agua)
    return out


def borra(f, pts):
    """Borra (alfa 0) un poligono dado desde la esquina de la figura."""
    x0, y0 = caja(f)[:2]
    m = mascara_poli(f.shape[:2], [(x0 + x, y0 + y) for x, y in pts])
    out = f.copy()
    out[..., 3] = np.where(m, 0, out[..., 3])
    return out


def antebrazo(f, a, b, g, ref_muto, curva=0.12):
    """Un antebrazo de monstruo de a a b (absolutos) sobre la figura: un poco curvo,
    grueso en el codo y fino en la muneca, con sombra abajo, filo de luz arriba,
    vetas y contorno."""
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    if ny > 0:                                   # la normal hacia arriba (la luz)
        nx, ny = -nx, -ny
    medio = (a[0] + dx * 0.5 + nx * n * curva, a[1] + dy * 0.5 + ny * n * curva)
    eje = _bez(a, medio, b, 20)
    arriba, abajo = [], []
    for k, (x, y) in enumerate(eje):
        t = k / 20.0
        gg = g * (1.2 - 0.45 * t + 0.18 * math.sin(math.pi * t))
        arriba.append((x + nx * gg, y + ny * gg))
        abajo.append((x - nx * gg, y - ny * gg))
    base = tuple(int(v) for v in np.clip(ref_muto[0], 0, 255))
    osc = tuple(int(v * 0.55) for v in base)
    im = Image.fromarray(f.copy())
    d = ImageDraw.Draw(im)
    ancho = max(2, int(round(g * 0.22)))
    d.polygon(arriba + abajo[::-1], fill=base + (255,))
    # sombra: la mitad de abajo
    sombra = [((x0 + x1) / 2, (y0 + y1) / 2) for (x0, y0), (x1, y1) in zip(arriba, abajo)]
    d.polygon(sombra + abajo[::-1], fill=tuple(int(v * 0.72) for v in base) + (255,))
    # vetas a lo largo
    for k in (0.3, 0.62):
        d.line([(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k) for (x0, y0), (x1, y1) in zip(arriba, abajo)][2:-2],
               fill=osc + (255,), width=max(2, int(g * 0.09)))
    d.line(arriba[1:-1], fill=(200, 100, 56, 255), width=ancho)
    d.line(arriba, fill=TINTA + (255,), width=ancho)
    d.line(abajo, fill=TINTA + (255,), width=ancho)
    return np.array(im)


def _bez(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (k / float(n) for k in range(n + 1))]


def puno_en_palma(f_garras, f_puno, ref_golpe=True):
    """El puno de una figura sobre la garra izquierda de la otra: se golpea la palma."""
    x0, y0 = caja(f_puno)[:2]
    a, b, c, d = PUNO_GRITO
    trozo = f_puno[y0 + b:y0 + d, x0 + a:x0 + c].copy()
    im = Image.fromarray(trozo)
    (cx, cy), ancho = PUNO_SOBRE
    s = ancho / float(im.width)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    t = np.array(im)
    t[..., 3] = np.where(t[..., 3] >= 128, 255, 0)
    gx0, gy0 = caja(f_garras)[:2]
    out = Image.fromarray(f_garras)
    out.alpha_composite(Image.fromarray(t), (int(gx0 + cx - im.width / 2), int(gy0 + cy - im.height / 2)))
    return np.array(out)


# --- las cabezas de las fotos -------------------------------------------------------------

# (imagen, recorte en la imagen, centro de la cabeza en el recorte, semiejes de la
#  elipse que la abarca). Todas del collage de cinco ('fotos').
FOTOS = dict(
    nariz=('fotos', (520, 75, 1000, 475), (185, 150), (118, 152)),       # se tapa la nariz, ojos cerrados
    dedos=('fotos', (440, 525, 728, 1010), (142, 122), (88, 122)),       # grita, los dos indices
    rasca=('fotos', (5, 800, 445, 1250), (300, 200), (88, 125)),         # se rasca la cabeza, mira abajo
    atril=('fotos', (1325, 405, 1650, 722), (184, 72), (54, 66)),        # grita en el atril
    calma=('fotos', (1110, 985, 1500, 1245), (220, 96), (84, 94)),       # habla tranquilo
)


def color_cabeza(f):
    """Media y dispersion por canal de la cabeza de una figura pintada (para pasarle
    su color a las fotos)."""
    y0, cx, hw, hom = medidas_cabeza(f)
    trozo = f[y0:y0 + hom, int(cx - hw * 0.45):int(cx + hw * 0.45)]
    a = trozo[..., 3] > 0
    v = trozo[..., :3][a].astype(float)
    return v.mean(0), v.std(0)


def mascara_poli(forma, pts):
    m = Image.new('L', (forma[1], forma[0]), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return np.array(m) > 0


def transfiere(col, m, ref):
    """Lleva la media y la dispersion por canal de los pixeles 'm' de col a las de ref."""
    for k in range(3):
        v = col[..., k][m]
        if len(v) == 0:
            continue
        nuevo = ref[0][k] + (col[..., k] - v.mean()) * (ref[1][k] / (v.std() + 1e-6))
        col[..., k] = np.where(m, nuevo, col[..., k])
    return col


def repaso(rgb):
    """Mas color, mas contraste y las lineas marcadas: la foto hacia el pixel art."""
    from PIL import ImageEnhance
    pic = Image.fromarray(rgb)
    pic = ImageEnhance.Color(pic).enhance(1.35)
    pic = ImageEnhance.Contrast(pic).enhance(1.25)
    lum = np.array(pic.convert('L')).astype(float)
    borde = np.hypot(ndimage.sobel(lum, 0), ndimage.sobel(lum, 1))
    return np.array(pic).astype(float), np.clip((borde - 60) / 160.0, 0, 1) * 0.55


def recorte_foto(rutas, nombre):
    from rembg import remove
    img, caja_f = FOTOS[nombre][:2]
    im = Image.open(rutas[img]).convert('RGB').crop(caja_f)
    sin_fondo(None)
    return np.array(remove(im, session=_SESION))


def cabeza_foto(rutas, nombre, ref=None, ref_muto=None):
    """La cabeza de una foto, sin fondo y recortada por su elipse (y el brazo de
    BRAZOS_FOTO, pasado al color del monstruo), con el color de la cabeza pintada
    de referencia y las lineas marcadas; bizca o hurgandose la nariz si toca.
    Devuelve (rgba desde la coronilla, centro x, ancho de la cabeza, fila de la
    coronilla en el recorte)."""
    img, caja_f, (cx, cy), (rx, ry) = FOTOS[nombre]
    rgba = recorte_foto(rutas, nombre)
    yy = np.arange(rgba.shape[0])[:, None]
    xx = np.arange(rgba.shape[1])[None, :]
    elipse = ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2 < 1.0
    a = (rgba[..., 3] >= 128) & elipse
    brazo = np.zeros_like(a)
    if nombre in BRAZOS_FOTO:
        brazo = mascara_poli(a.shape, BRAZOS_FOTO[nombre]) & (rgba[..., 3] >= 100) & piel(rgba)
        if nombre not in MANO_DENTRO:
            brazo &= ~a
        brazo = ndimage.binary_closing(brazo, iterations=3) & mascara_poli(a.shape, BRAZOS_FOTO[nombre])
        a = a | brazo
    lab, n = ndimage.label(a)
    if n > 1:
        tam = ndimage.sum(a, lab, range(1, n + 1))
        a = lab == (1 + int(np.argmax(tam)))
        brazo &= a
    if nombre == 'rasca':
        # el gorro (la kipa) se pinta del gris del pelo
        oscuro = (rgba[..., :3].astype(int).sum(2) < 150) & (yy < cy - ry * 0.55) & (np.abs(xx - cx) < rx * 0.7) & ~brazo
        rgba[oscuro, :3] = (150, 150, 156)
    ys = np.nonzero((a & ~brazo).any(1))[0]
    top = ys.min()
    # el ancho de la cabeza: la mediana de las filas entre el 30 y el 50 % de su alto
    h = ys.max() - top
    cab = a & ~brazo
    anchos = [np.ptp(np.nonzero(cab[top + y])[0]) for y in range(int(h * 0.3), int(h * 0.5)) if cab[top + y].any()]
    hw = ANCHO_FOTO.get(nombre, float(np.median(anchos)))
    col, borde = repaso(rgba[..., :3])
    if ref is not None:
        col = transfiere(col, a & ~brazo, ref)
    if ref_muto is not None and brazo.any():
        col = transfiere(col, brazo, ref_muto)
    col = col * (1 - borde[..., None])
    out = np.zeros_like(rgba)
    out[..., :3] = col.clip(0, 255).astype(np.uint8)
    out[..., 3] = np.where(a, 255, 0)
    if nombre in ANTEBRAZO_FOTO and ref_muto is not None:
        mu, sa, g = ANTEBRAZO_FOTO[nombre]
        fondo = np.zeros_like(out)
        fondo = miembro(fondo, mu, sa, g * hw, ref_muto)
        f2 = Image.fromarray(fondo)
        f2.alpha_composite(Image.fromarray(out))
        out = np.array(f2)
    if nombre in BIZCO_FOTO:
        out = bizco(out, *BIZCO_FOTO[nombre])
    if nombre in MOCO_FOTO and ref_muto is not None:
        out = moco(out, MOCO_FOTO[nombre]['fosa'], MOCO_FOTO[nombre]['puno'], hw, ref_muto)
    return out[top:], cx, hw, top


def piel(rgba):
    r, g, b = [rgba[..., k].astype(int) for k in range(3)]
    return (r > 85) & (r > g) & (g > b - 10) & (r - b > 22)


def miembro(rgba, a, b, g, ref_muto):
    """Un antebrazo de monstruo de a a b (medio grosor g): marron, con contorno y el
    filo de luz naranja."""
    im = Image.fromarray(rgba)
    d = ImageDraw.Draw(im)
    base = tuple(int(v) for v in np.clip(ref_muto[0], 0, 255))
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = (dx * dx + dy * dy) ** 0.5
    nx, ny = -dy / n, dx / n
    pts = [(a[0] + nx * g * 0.8, a[1] + ny * g * 0.8), (b[0] + nx * g, b[1] + ny * g),
           (b[0] - nx * g, b[1] - ny * g), (a[0] - nx * g * 0.8, a[1] - ny * g * 0.8)]
    ancho = max(2, int(round(g * 0.25)))
    d.polygon(pts, fill=base + (255,), outline=TINTA + (255,), width=ancho)
    d.line([pts[0], pts[1]], fill=(196, 96, 54, 255), width=ancho)
    for t in (0.35, 0.65):
        q = (a[0] + dx * t, a[1] + dy * t)
        d.line([(q[0] + nx * g * 0.6, q[1] + ny * g * 0.6), (q[0] - nx * g * 0.3, q[1] - ny * g * 0.3)],
               fill=tuple(int(v * 0.6) for v in base) + (255,), width=ancho)
    return np.array(im)


def manos_foto(rutas, ref_muto):
    """Las dos manos que apuntan con el indice (foto de los dedos), en el color del
    monstruo, en las coordenadas de su recorte."""
    rgba = recorte_foto(rutas, 'dedos')
    m = mascara_poli(rgba.shape[:2], MANOS_DEDOS) & (rgba[..., 3] >= 128) & piel(rgba)
    m = ndimage.binary_closing(m, iterations=3)
    lab, n = ndimage.label(m)
    tam = ndimage.sum(m, lab, range(1, n + 1))
    m = np.isin(lab, 1 + np.nonzero(tam > 0.05 * tam.max())[0])
    col, borde = repaso(rgba[..., :3])
    col = transfiere(col, m, ref_muto) * (1 - borde[..., None])
    out = np.zeros_like(rgba)
    out[..., :3] = col.clip(0, 255).astype(np.uint8)
    out[..., 3] = np.where(m, 255, 0)
    ys, xs = np.nonzero(m)
    return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def sobre_pecho(cuerpo, manos):
    """Las manos que apuntan, juntas y grandes, delante del pecho."""
    cy0, ccx, chw, chom = medidas_cabeza(cuerpo)
    im = Image.fromarray(manos)
    s = MANOS_ANCHO * chw / float(im.width)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    a = np.array(im)
    m = a[..., 3] >= 128
    # mas claras que el pecho, con contorno de tinta y el filo de luz naranja arriba a la izquierda
    a[..., :3] = np.clip(a[..., :3].astype(float) * 1.45 + 8, 0, 255).astype(np.uint8)
    filo = m & ~np.roll(np.roll(m, 4, 0), 4, 1)
    a[filo, :3] = (214, 110, 60)
    pad = 6
    b = np.zeros((a.shape[0] + 2 * pad, a.shape[1] + 2 * pad, 4), np.uint8)
    b[pad:-pad, pad:-pad] = np.where(m[..., None], a, 0)
    mb = b[..., 3] > 0
    anillo = ndimage.binary_dilation(mb, iterations=5) & ~mb
    b[anillo] = TINTA + (255,)
    b[mb, 3] = 255
    out = Image.fromarray(cuerpo)
    out.alpha_composite(Image.fromarray(b), (int(ccx - b.shape[1] / 2), int(cy0 + chom + MANOS_BAJA * chw - b.shape[0] / 2)))
    return np.array(out)


def pega(cuerpo, trozo, tcx, ttop, thw):
    """Pega 'trozo' sobre 'cuerpo' sin borrar nada, con la transformacion que lleva
    la cabeza de su foto (centro tcx, coronilla ttop, ancho thw) a la del cuerpo."""
    cy0, ccx, chw, chom = medidas_cabeza(cuerpo)
    s = chw / float(thw)
    t = Image.fromarray(trozo)
    t = t.resize((max(1, int(round(t.width * s))), max(1, int(round(t.height * s)))), Image.LANCZOS)
    tt = np.array(t)
    tt[..., 3] = np.where(tt[..., 3] >= 128, 255, 0)
    px, py = int(round(ccx - tcx * s)), int(round(cy0 - ttop * s))
    out = Image.fromarray(cuerpo)
    out.alpha_composite(Image.fromarray(tt), (max(0, px), max(0, py)), (max(0, -px), max(0, -py)))
    return np.array(out)


def bizco(rgba, ojo1, ojo2, r):
    """Ojos de dibujo, redondos y grandes, con las pupilas juntas hacia la nariz."""
    im = Image.fromarray(rgba)
    d = ImageDraw.Draw(im)
    ancho = max(2, int(round(r * 0.22)))
    (x1, y1), (x2, y2) = sorted([ojo1, ojo2])
    for (x, y), hacia in (((x1, y1), 1), ((x2, y2), -1)):
        R = r * 1.25
        d.ellipse([x - R, y - R * 0.95, x + R, y + R * 0.95], fill=(244, 240, 230, 255), outline=TINTA + (255,), width=ancho)
        px = x + hacia * R * 0.48
        p = R * 0.5
        d.ellipse([px - p, y - p + R * 0.08, px + p, y + p + R * 0.08], fill=(22, 16, 16, 255))
        d.ellipse([px - p * 0.35 - p * 0.3, y - p * 0.5, px - p * 0.3 + p * 0.05, y - p * 0.15], fill=(255, 255, 255, 255))
        # el parpado de arriba, un poco caido: la cara de no enterarse
        d.chord([x - R, y - R * 0.95, x + R, y + R * 0.95], 200, 340, fill=(150, 96, 80, 255), outline=TINTA + (255,), width=ancho)
    return np.array(im)


def moco(rgba, fosa, puno, hw, ref_muto):
    """Un dedo de garra metido en la nariz: el puno abajo a un lado, con los nudillos,
    y el indice que sube inclinado hasta la fosa."""
    im = Image.fromarray(rgba)
    d = ImageDraw.Draw(im)
    base = tuple(int(v) for v in np.clip(ref_muto[0] * 2.1 + 20, 0, 255))
    luz = (226, 140, 90)
    osc = tuple(int(v) for v in np.clip(ref_muto[0] * 0.7, 0, 255))
    ancho = max(2, int(round(hw * 0.022)))
    fx, fy = fosa
    px, py = puno
    g = hw * 0.042                              # medio grosor del dedo
    dx, dy = fx - px, fy - py
    n = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux
    raiz = (px + ux * hw * 0.08, py + uy * hw * 0.08)
    dedo = [(raiz[0] + nx * g * 1.15, raiz[1] + ny * g * 1.15), (fx + nx * g, fy + ny * g),
            (fx - nx * g, fy - ny * g), (raiz[0] - nx * g * 1.15, raiz[1] - ny * g * 1.15)]
    d.polygon(dedo, fill=base + (255,), outline=TINTA + (255,), width=ancho)
    d.line([dedo[0], dedo[1]], fill=luz + (255,), width=ancho)
    for t in (0.4, 0.7):
        qx, qy = raiz[0] + (fx - raiz[0]) * t, raiz[1] + (fy - raiz[1]) * t
        d.line([(qx + nx * g * 0.9, qy + ny * g * 0.9), (qx - nx * g * 0.9, qy - ny * g * 0.9)], fill=osc + (255,), width=ancho)
    # la punta entra en la fosa: sombra
    d.ellipse([fx - g * 1.3, fy - g * 1.0, fx + g * 1.3, fy + g * 0.6], fill=(40, 16, 16, 255))
    # el puno: los otros tres dedos doblados (tres rodillos) y el pulgar
    w, h = hw * 0.16, hw * 0.07
    for k in range(3):
        cy = py + k * h * 0.95
        cx = px - k * h * 0.25
        d.rounded_rectangle([cx - w, cy - h * 0.6, cx + w * 0.7, cy + h * 0.6], radius=h * 0.55,
                            fill=base + (255,), outline=TINTA + (255,), width=ancho)
        d.line([(cx - w * 0.8, cy - h * 0.4), (cx + w * 0.4, cy - h * 0.4)], fill=luz + (255,), width=ancho)
    d.rounded_rectangle([px - w * 1.15, py - h * 0.2, px - w * 0.35, py + h * 2.6], radius=h * 0.4,
                        fill=base + (255,), outline=TINTA + (255,), width=ancho)
    return np.array(im)


def color_muto(f):
    """El color de la piel del monstruo: la tripa y los muslos de una figura (sin el
    saco que brilla)."""
    x0, y0, x1, y1 = caja(f)
    h, w = y1 - y0, x1 - x0
    trozo = f[y0 + int(h * 0.45):y0 + int(h * 0.62), x0 + int(w * 0.3):x0 + int(w * 0.7)]
    v = trozo[..., :3][trozo[..., 3] > 0].astype(float)
    v = v[v.mean(1) < 120]
    return v.mean(0), v.std(0)


# --- la gorra -------------------------------------------------------------------------

TWEED = (118, 102, 74)


def gorra(fig, lado=1, inclina=13.0):
    """Una gorra plana de campo (de tweed, achatada, con la visera corta), ladeada
    hacia 'lado', sobre la cabeza de la figura; y la sombra de la visera en la frente."""
    import math
    cy0, ccx, chw, chom = medidas_cabeza(fig)
    H, W = fig.shape[:2]
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    w = chw * 0.94
    ox, oy = ccx + lado * 0.06 * w, cy0 + 0.30 * w      # el centro de la gorra

    def P(x, y):
        return (ox + x * w, oy + y * w)
    base = TWEED
    osc = tuple(int(v * 0.62) for v in base)
    luz = tuple(min(255, int(v * 1.3)) for v in base)
    borde = max(3, int(w * 0.03))
    # la copa: ancha y achatada, cae un poco por delante sobre la visera
    copa = [P(*q) for q in ((-0.60, 0.08), (-0.62, -0.06), (-0.52, -0.20), (-0.30, -0.30), (0.0, -0.33),
                            (0.30, -0.31), (0.54, -0.22), (0.66, -0.06), (0.64, 0.08), (0.40, 0.14),
                            (0.0, 0.16), (-0.40, 0.14))]
    d.polygon(copa, fill=base + (255,))
    # el volumen: sombra abajo, luz arriba
    d.polygon([P(*q) for q in ((-0.60, 0.02), (0.64, 0.02), (0.40, 0.14), (0.0, 0.16), (-0.40, 0.14))], fill=osc + (255,))
    d.line([P(-0.48, -0.20), P(-0.22, -0.29), P(0.10, -0.30)], fill=luz + (255,), width=borde * 2)
    # el tejido: rayas finas en espiga
    for k in range(-5, 6):
        x = k * 0.11
        d.line([P(x - 0.03, -0.27 + abs(x) * 0.12), P(x + 0.03, 0.02)], fill=osc + (255,), width=max(1, borde // 2))
    # la costura del frente y el boton de arriba
    d.line([P(-0.48, -0.04), P(0.0, -0.12), P(0.52, -0.04)], fill=osc + (255,), width=borde)
    d.ellipse([P(-0.03, -0.35), P(0.05, -0.29)], fill=osc + (255,))
    d.polygon(copa, outline=TINTA + (255,), width=borde)
    # la visera: corta, hacia delante (abajo en la imagen)
    visera = [P(*q) for q in ((-0.46, 0.10), (-0.20, 0.24), (0.0, 0.27), (0.24, 0.24), (0.48, 0.10), (0.0, 0.15))]
    d.polygon(visera, fill=tuple(int(v * 0.5) for v in base) + (255,), outline=TINTA + (255,), width=borde)
    d.line([P(-0.32, 0.17), P(0.0, 0.22), P(0.32, 0.17)], fill=osc + (255,), width=borde)
    capa = capa.rotate(-lado * inclina, resample=Image.BICUBIC, center=(ox, oy))
    # la sombra de la visera en la frente
    sombra = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sombra).ellipse([ox - 0.48 * w, oy + 0.12 * w, ox + 0.48 * w, oy + 0.42 * w], fill=110)
    sombra = sombra.rotate(-lado * inclina, center=(ox, oy)).filter(ImageFilter.GaussianBlur(w * 0.05))
    sombra = Image.fromarray(np.minimum(np.array(sombra), fig[..., 3]))
    out = Image.fromarray(fig)
    oscuro = Image.new('RGBA', (W, H), (30, 14, 12, 0))
    oscuro.putalpha(sombra)
    out.alpha_composite(oscuro)
    a = np.array(capa)
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    out.alpha_composite(Image.fromarray(a))
    return np.array(out)


# --- las dos patas largas del MUTO ----------------------------------------------------

# en anchos de cabeza desde el centro de la cabeza (x, a cada lado) y su coronilla (y);
# el pie, desde el suelo (los pies de la figura)
PATA_HOMBRO = (0.66, 1.50)
PATA_RODILLA = (1.08, 0.24)
PATA_MEDIO = (1.30, -2.10)            # y desde el suelo (la articulacion de la espinilla)
PATA_TOBILLO = (1.22, -0.78)          # y desde el suelo
PATA_PIE = (1.06, 0.0)                # y desde el suelo
PATA_GROSOR = 0.13                    # medio grosor del muslo


def patas_muto(fig, ref_muto, margen=260):
    """Las dos patas largas del MUTO, detras del cuerpo: salen de los hombros,
    suben a una rodilla alta junto a la cabeza y bajan al suelo a los lados de los
    pies, con el garfio de la punta hacia dentro."""
    import math
    cy0, ccx, chw, chom = medidas_cabeza(fig)
    suelo = caja(fig)[3]
    H, W = fig.shape[:2]
    grande = np.zeros((H, W + 2 * margen, 4), np.uint8)
    grande[:, margen:margen + W] = fig
    ccx += margen
    capa = Image.new('RGBA', (grande.shape[1], H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    base = tuple(int(v) for v in np.clip(ref_muto[0] * 1.15 + 6, 0, 255))
    osc = tuple(int(v * 0.6) for v in base)
    luz = (206, 104, 58)
    g0 = PATA_GROSOR * chw
    ancho = max(3, int(g0 * 0.22))

    def tramo(a, b, ga, gb, col):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        nx, ny = -dy / n, dx / n
        pts = [(a[0] + nx * ga, a[1] + ny * ga), (b[0] + nx * gb, b[1] + ny * gb),
               (b[0] - nx * gb, b[1] - ny * gb), (a[0] - nx * ga, a[1] - ny * ga)]
        d.polygon(pts, fill=col + (255,))
        # sombra en un lado, vetas y filo de luz en el otro
        d.polygon([pts[2], pts[3], ((a[0] + pts[3][0]) / 2 + (a[0] - pts[3][0]) * 0.1, (a[1] + pts[3][1]) / 2),
                   ((b[0] + pts[2][0]) / 2, (b[1] + pts[2][1]) / 2)], fill=tuple(int(v * 0.75) for v in col) + (255,))
        for k in (-0.3, 0.25):
            d.line([(a[0] + dx * 0.1 + nx * ga * k, a[1] + dy * 0.1 + ny * ga * k),
                    (a[0] + dx * 0.9 + nx * gb * k, a[1] + dy * 0.9 + ny * gb * k)], fill=osc + (255,), width=max(2, ancho // 2))
        for t in (0.3, 0.55, 0.8):              # grietas de corteza
            q = (a[0] + dx * t, a[1] + dy * t)
            d.line([(q[0] + nx * ga * 0.6, q[1] + ny * ga * 0.6), (q[0] + nx * ga * 0.1, q[1] + ny * ga * 0.1 + gb * 0.3)],
                   fill=osc + (255,), width=max(2, ancho // 2))
        d.line([pts[0], pts[1]], fill=luz + (255,), width=ancho)
        d.polygon(pts, outline=TINTA + (255,), width=ancho)

    def nudo(p, r, col):
        d.polygon([(p[0] - r, p[1]), (p[0] - r * 0.3, p[1] - r * 1.1), (p[0] + r * 0.5, p[1] - r * 0.9), (p[0] + r, p[1]),
                   (p[0] + r * 0.4, p[1] + r), (p[0] - r * 0.6, p[1] + r * 0.8)], fill=col + (255,), outline=TINTA + (255,), width=ancho)

    for lado in (-1, 1):
        col = base if lado > 0 else tuple(int(v * 0.85) for v in base)
        hombro = (ccx + lado * PATA_HOMBRO[0] * chw, cy0 + PATA_HOMBRO[1] * chw)
        rodilla = (ccx + lado * PATA_RODILLA[0] * chw, cy0 + PATA_RODILLA[1] * chw)
        medio = (ccx + lado * PATA_MEDIO[0] * chw, suelo + PATA_MEDIO[1] * chw)
        tobillo = (ccx + lado * PATA_TOBILLO[0] * chw, suelo + PATA_TOBILLO[1] * chw)
        pie = (ccx + lado * PATA_PIE[0] * chw, suelo + PATA_PIE[1] * chw)
        tramo(hombro, rodilla, g0, g0 * 0.85, col)
        tramo(rodilla, medio, g0 * 0.8, g0 * 0.62, col)
        tramo(medio, tobillo, g0 * 0.58, g0 * 0.5, col)
        # la cuchilla del pie con el garfio hacia dentro (hacia el cuerpo), la punta clara
        gx = -lado
        cuchilla = [(tobillo[0] - g0 * 0.5, tobillo[1]), (tobillo[0] + g0 * 0.5, tobillo[1]),
                    (pie[0] + g0 * 0.3, pie[1] - g0 * 1.3), (pie[0] + gx * g0 * 0.2, pie[1]),
                    (pie[0] + gx * g0 * 2.0, pie[1] - g0 * 2.2), (pie[0] + gx * g0 * 0.6, pie[1] - g0 * 1.7),
                    (pie[0] - g0 * 0.3, pie[1] - g0 * 1.5)]
        d.polygon(cuchilla, fill=col + (255,), outline=TINTA + (255,), width=ancho)
        d.line([cuchilla[0], cuchilla[2]], fill=luz + (255,), width=ancho)
        d.polygon([cuchilla[3], cuchilla[4], cuchilla[5]], fill=(176, 150, 128, 255), outline=TINTA + (255,), width=ancho)
        nudo(rodilla, g0 * 1.25, col)
        nudo(medio, g0 * 0.8, col)
        nudo(tobillo, g0 * 0.7, col)
        # el espolon de la rodilla, hacia arriba y afuera
        d.polygon([(rodilla[0] - g0 * 0.5, rodilla[1] - g0 * 0.7), (rodilla[0] + lado * g0 * 0.8, rodilla[1] - g0 * 2.1),
                   (rodilla[0] + g0 * 0.5, rodilla[1] - g0 * 0.6)], fill=col + (255,), outline=TINTA + (255,), width=ancho)
        d.line([(rodilla[0] - g0 * 0.9, rodilla[1] - g0 * 0.3), (rodilla[0] - g0 * 0.2, rodilla[1] - g0 * 1.0)],
               fill=luz + (255,), width=ancho)
    a = np.array(capa)
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    capa = Image.fromarray(a)
    capa.alpha_composite(Image.fromarray(grande))
    return np.array(capa)


# --- adornos (en la celda) ---------------------------------------------------------------

AGUA = (120, 200, 255)


def _gota(d, x, y, r):
    d.polygon([(x, y - r * 2.2), (x - r, y), (x + r, y)], fill=AGUA + (255,), outline=TINTA + (255,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=AGUA + (255,), outline=TINTA + (255,))


def adornos(cel, tipo, cabeza):
    """Lagrimas, sudor o interrogaciones junto a la cabeza (cabeza = (x, y, ancho) en la celda)."""
    from PIL import ImageFont
    d = ImageDraw.Draw(cel)
    x, y, w = cabeza
    if tipo == 'lagrimas':
        for k in range(3):
            _gota(d, x - w * 0.3, y + w * 0.78 + k * 8, 2.6 - k * 0.3)
            _gota(d, x + w * 0.3, y + w * 0.82 + k * 8, 2.4 - k * 0.3)
    elif tipo == 'sudor':
        _gota(d, x + w * 0.62, y + w * 0.2, 3.0)
        _gota(d, x - w * 0.66, y + w * 0.3, 2.6)
        _gota(d, x + w * 0.5, y - w * 0.08, 2.2)
    elif tipo == 'jaja':
        try:
            ff = ImageFont.load_default(size=13)
        except TypeError:
            ff = ImageFont.load_default()
        for (dx, dy, t) in ((0.62, -0.05, 'JA'), (-1.05, 0.12, 'JA'), (0.75, 0.4, 'JA')):
            px, py = x + dx * w, y + dy * w
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    d.text((px + ox, py + oy), t, fill=TINTA + (255,), font=ff)
            d.text((px, py), t, fill=(255, 230, 60, 255), font=ff)
    elif tipo == 'golpe':
        # lineas de impacto donde el puno da en la palma
        gx, gy = x, y
        for ang in (-150, -115, -80, -45, -10):
            import math
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([(gx + ca * 6, gy + sa * 6), (gx + ca * 13, gy + sa * 13)], fill=TINTA + (255,), width=3)
            d.line([(gx + ca * 6, gy + sa * 6), (gx + ca * 13, gy + sa * 13)], fill=(255, 240, 150, 255), width=1)
    elif tipo == 'pregunta':
        try:
            f = ImageFont.load_default(size=22)
        except TypeError:
            f = ImageFont.load_default()
        for (dx, dy, t) in ((0.7, -0.15, 22), (-0.85, 0.05, 16)):
            try:
                ff = ImageFont.load_default(size=t)
            except TypeError:
                ff = f
            px, py = x + dx * w, y + dy * w
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    d.text((px + ox, py + oy), '?', fill=TINTA + (255,), font=ff)
            d.text((px, py), '?', fill=(255, 230, 60, 255), font=ff)
    return cel


# --- celdas -------------------------------------------------------------------------

def a_celda(rgba, escala):
    x0, y0, x1, y1 = caja(rgba)
    im = Image.fromarray(rgba).crop((x0, y0, x1, y1))
    w, h = max(1, int(round((x1 - x0) * escala))), max(1, int(round((y1 - y0) * escala)))
    im = im.resize((w, h), Image.LANCZOS)
    cel = Image.new('RGBA', (CELDA_W, CELDA_H), (0, 0, 0, 0))
    cel.alpha_composite(im, ((CELDA_W - w) // 2, CELDA_H - MARGEN - h))
    return pixelar(cel)


def pixelar(im, colores=96):
    a = im.split()[3].point(lambda v: 255 if v >= 128 else 0)
    fondo = Image.new('RGBA', im.size, (70, 50, 40, 255))
    fondo.alpha_composite(im)
    q = fondo.convert('RGB').quantize(colors=colores, method=Image.Quantize.MEDIANCUT,
                                      dither=Image.Dither.NONE).convert('RGBA')
    q.putalpha(a)
    anillo = ImageChops.subtract(a.filter(ImageFilter.MaxFilter(3)), a)
    tinta = Image.new('RGBA', im.size, TINTA + (255,))
    tinta.putalpha(anillo)
    q.alpha_composite(tinta)
    return q


def figuras(frente, grita_rie, dientes_llora, fotos):
    f = {}
    f['frente'] = limpia(sin_fondo(frente))
    f['grito'], f['rie'] = separa(limpia(sin_fondo(grita_rie)))
    f['dientes'], f['llora_risa'] = separa(limpia(sin_fondo(dientes_llora)))
    f['serio'] = limpia(pon_cabeza(f['dientes'], f['frente']))
    f['furia'] = cara_roja(f['grito'])
    f['bizco'] = limpia(pon_cabeza(f['llora_risa'], bizco(f['frente'].copy(), *BIZCO_FRENTE)))
    f['carcajada'] = sin_lagrimas(f['llora_risa'])
    rutas = dict(fotos=fotos)
    ref = color_cabeza(f['dientes'])
    ref_muto = color_muto(f['dientes'])
    # enfado: la cabeza de los dientes sobre las garras, y el puno golpeando la palma
    f['enfado_puno'] = limpia(pon_cabeza(puno_en_palma(f['llora_risa'], f['grito']), f['dientes']))
    for nombre, cuerpo in CUERPO_FOTO.items():
        cab, cx, hw, top = cabeza_foto(rutas, nombre, ref, ref_muto)
        base = f[cuerpo]
        if nombre in BRAZO_NUEVO:
            fig, poli, codo, muneca = BRAZO_NUEVO[nombre]
            px, py, s = donde_injerta(base, cx, hw, BAJA_FOTO.get(nombre, 0.0))
            if muneca is None:              # el puno del dedo en la nariz
                muneca = MOCO_FOTO[nombre]['puno']
                muneca = (muneca[0] - hw * 0.06, muneca[1] + hw * 0.1)
            x0, y0 = caja(base)[:2]
            fin = (px + muneca[0] * s, py + (muneca[1] - top) * s)
            base = antebrazo(borra(base, poli), (x0 + codo[0], y0 + codo[1]), fin, 0.12 * medidas_cabeza(base)[2],
                             ref_muto)
        f['f_' + nombre] = limpia(injerta(base, cab, cx, hw, BAJA_FOTO.get(nombre, 0.0)))
    return f


def main(args):
    if len(args) != 4:
        print(__doc__)
        sys.exit(1)
    f = figuras(*args)
    ref_muto = color_muto(f['dientes'])
    figs = {}
    for nombre in EMOCIONES:
        origen = ORIGEN[nombre][0]
        fig = gorra(f[origen], GORRA[nombre]) if nombre in GORRA else f[origen]
        figs[nombre] = patas_muto(fig, ref_muto)
    alto = max(caja(v)[3] - caja(v)[1] for v in figs.values())
    ancho = max(caja(v)[2] - caja(v)[0] for v in figs.values())
    escala = min((CELDA_H - 2 * MARGEN) / float(alto), (CELDA_W - 2) / float(ancho))
    atlas = Image.new('RGBA', (CELDA_W * COLS, CELDA_H * FILAS), (0, 0, 0, 0))
    lamina = Image.new('RGBA', atlas.size, (60, 62, 68, 255))
    d = ImageDraw.Draw(lamina)
    for i, nombre in enumerate(EMOCIONES):
        origen, adorno = ORIGEN[nombre]
        fig = figs[nombre]
        im = a_celda(fig, escala)
        if adorno:
            y0, cx, hw, _ = medidas_cabeza(f[origen])
            cx += 260                       # el margen que anade patas_muto
            x0, yb0, x1, yb1 = caja(fig)
            ox = (CELDA_W - int(round((x1 - x0) * escala))) // 2
            oy = CELDA_H - MARGEN - int(round((yb1 - yb0) * escala))
            cab = (ox + (cx - x0) * escala, oy + (y0 - yb0) * escala, hw * escala)
            if adorno == 'golpe':
                # donde el puno da en la palma (PUNO_SOBRE, desde la esquina de la figura de las garras)
                (gx, gy), ancho = PUNO_SOBRE
                fx0, fy0 = caja(f[origen])[:2]
                gx, gy = fx0 + 260 + gx + ancho * 0.42, fy0 + gy - ancho * 0.25
                cab = (ox + (gx - x0) * escala, oy + (gy - yb0) * escala, hw * escala)
            im = adornos(im, adorno, cab)
        x, y = (i % COLS) * CELDA_W, (i // COLS) * CELDA_H
        atlas.paste(im, (x, y))
        lamina.alpha_composite(im, (x, y))
        d.text((x + 4, y + 2), '%d %s' % (i, nombre), fill=(255, 230, 0, 255))
    atlas = igualar(atlas)                  # la claridad comun (igualar_brillo.py)
    atlas.save(os.path.join(AQUI, 'nefanyamuto_emociones.png'))
    lamina_igualada(atlas, EMOCIONES).save(os.path.join(AQUI, 'nefanyamuto_emociones_lamina.png'))
    print('nefanyamuto_emociones.png (%d x %d), escala %.3f, y la lamina' % (atlas.size + (escala,)))


if __name__ == '__main__':
    main(sys.argv[1:])
