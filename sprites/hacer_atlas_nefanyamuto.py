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
como garras suyas. Los ojos bizcos y el dedo en la nariz se pintan. Las doce caras
(EMOCIONES) llenan las 4 x 3 celdas: las diez de EMOCIONES_MON y dos en las que no
se entera de nada (despiste: bizco; pasmado: bizco y hurgandose la nariz).

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
    enfado=('enfado_dedos', None),    # aprieta los dientes y apunta con los dos indices (las manos de la foto)
    furia=('furia', None),            # el grito con la cara roja
    rie=('rie', None),
    carcajada=('llora_risa', None),
    susto=('f_dedos', 'sudor'),       # foto: grita con los dos indices
    mueca=('f_atril', None),          # foto: grita en el atril con el indice levantado
    llora=('f_nariz', 'lagrimas'),    # foto: se tapa la nariz con los ojos cerrados
    panico=('grito', 'sudor'),
    calma=('f_rasca', None),          # foto: se rasca la cabeza con la garra, sonrie
    despiste=('bizco', 'pregunta'),   # bizco (no se entera)
    pasmado=('f_calma', None),        # foto: bizco y hurgandose la nariz (no se entera)
)
# el cuerpo sobre el que va cada cabeza de foto
CUERPO_FOTO = dict(dedos='grito', atril='dientes', nariz='llora_risa', calma='llora_risa', rasca='rie')
BAJA_FOTO = dict(nariz=0.05, rasca=0.08)
# brazos y manos de las fotos que entran con la cabeza (poligonos en el recorte):
# se pasan al color del monstruo, como garras suyas
BRAZOS_FOTO = dict(
    atril=[(222, 6), (300, 6), (300, 135), (236, 135)],                     # el indice levantado
    rasca=[(118, 18), (292, 18), (292, 118), (225, 215), (138, 236), (96, 204)],   # la mano en la cabeza
)
# el antebrazo de monstruo que se dibuja bajo esas manos: muneca, salida y grosor (en anchos de cabeza)
ANTEBRAZO_FOTO = dict(atril=((262, 116), (272, 150), 0.12), rasca=((152, 196), (126, 222), 0.12))
# las manos que apuntan de la foto de los dos indices (poligono en su recorte); van
# juntas sobre el pecho, del ancho de MANOS_ANCHO cabezas y con su centro MANOS_BAJA
# cabezas por debajo de los hombros
MANOS_DEDOS = [(58, 268), (262, 268), (262, 432), (58, 432)]
MANOS_ANCHO, MANOS_BAJA = 1.15, 0.85
# bizco: los dos ojos (centros) y su radio, en el recorte de la foto o en frente.jpg
BIZCO_FOTO = dict(calma=((206, 105), (246, 107), 10.5))
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
        brazo = mascara_poli(a.shape, BRAZOS_FOTO[nombre]) & (rgba[..., 3] >= 100) & piel(rgba) & ~a
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
    rutas = dict(fotos=fotos)
    ref = color_cabeza(f['dientes'])
    ref_muto = color_muto(f['dientes'])
    for nombre, cuerpo in CUERPO_FOTO.items():
        cab, cx, hw, top = cabeza_foto(rutas, nombre, ref, ref_muto)
        f['f_' + nombre] = limpia(injerta(f[cuerpo], cab, cx, hw, BAJA_FOTO.get(nombre, 0.0)))
        if nombre == 'dedos':
            f['enfado_dedos'] = limpia(sobre_pecho(f['dientes'], manos_foto(rutas, ref_muto)))
    return f


def main(args):
    if len(args) != 4:
        print(__doc__)
        sys.exit(1)
    f = figuras(*args)
    usadas = set(o for o, _ in ORIGEN.values())
    alto = max(caja(f[k])[3] - caja(f[k])[1] for k in usadas)
    ancho = max(caja(f[k])[2] - caja(f[k])[0] for k in usadas)
    escala = min((CELDA_H - 2 * MARGEN) / float(alto), (CELDA_W - 2) / float(ancho))
    atlas = Image.new('RGBA', (CELDA_W * COLS, CELDA_H * FILAS), (0, 0, 0, 0))
    lamina = Image.new('RGBA', atlas.size, (60, 62, 68, 255))
    d = ImageDraw.Draw(lamina)
    for i, nombre in enumerate(EMOCIONES):
        origen, adorno = ORIGEN[nombre]
        im = a_celda(f[origen], escala)
        if adorno:
            y0, cx, hw, _ = medidas_cabeza(f[origen])
            x0, yb0, x1, yb1 = caja(f[origen])
            ox = (CELDA_W - int(round((x1 - x0) * escala))) // 2
            oy = CELDA_H - MARGEN - int(round((yb1 - yb0) * escala))
            im = adornos(im, adorno, (ox + (cx - x0) * escala, oy + (y0 - yb0) * escala, hw * escala))
        x, y = (i % COLS) * CELDA_W, (i // COLS) * CELDA_H
        atlas.paste(im, (x, y))
        lamina.alpha_composite(im, (x, y))
        d.text((x + 4, y + 2), '%d %s' % (i, nombre), fill=(255, 230, 0, 255))
    atlas.save(os.path.join(AQUI, 'nefanyamuto_emociones.png'))
    lamina.save(os.path.join(AQUI, 'nefanyamuto_emociones_lamina.png'))
    print('nefanyamuto_emociones.png (%d x %d), escala %.3f, y la lamina' % (atlas.size + (escala,)))


if __name__ == '__main__':
    main(sys.argv[1:])
