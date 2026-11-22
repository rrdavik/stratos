"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DE NEFANYAMUTO
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/nefanyamuto_emociones.png (y la lamina de prueba) desde las imagenes de
origen (JPG de 1024 x 1024 en pixel art, con la ciudad en llamas de fondo):

    python3 sprites/hacer_atlas_nefanyamuto.py frente.jpg grita_rie.jpg dientes_llora.jpg fotos.webp fotos_extra.webp

  frente.jpg         una figura de frente, brazos largos, la boca abierta (de ella sale la cara seria)
  grita_rie.jpg      dos figuras: grita con los ojos cerrados (izq.) y se rie (der.)
  dientes_llora.jpg  dos figuras: aprieta los dientes (izq.) y llora de risa (der.)
  fotos.webp         el collage de cinco fotos (1680 x 1500): se tapa la nariz, los dos
                     indices, se rasca la cabeza, el atril, habla tranquilo
  fotos_extra.webp   el collage de once fotos (1680 x 1500): de el, los ojos cerrados

De las fotos solo se usa la cabeza (FOTOS: el recorte y la elipse de cada una), con
el color pasado al de las cabezas pintadas y las lineas marcadas, sobre uno de los
cuerpos (CUERPO_FOTO). Las doce caras (EMOCIONES) llenan las 4 x 3 celdas: las diez
de EMOCIONES_MON y dos en las que no se entera de nada (despiste, pasmado).

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
    serio=('serio', None),          # cabeza de frente.jpg sobre el cuerpo de 'dientes'
    enfado=('dientes', None),
    furia=('furia', None),          # el grito con la cara roja
    rie=('rie', None),
    carcajada=('llora_risa', None),
    susto=('f_dedos', 'sudor'),     # foto: grita con los dos indices
    mueca=('f_atril', None),        # foto: grita en el atril
    llora=('f_nariz', 'lagrimas'),  # foto: se tapa la nariz con los ojos cerrados
    panico=('grito', 'sudor'),
    calma=('f_calma', None),        # foto: habla tranquilo
    despiste=('f_rasca', 'pregunta'),       # foto: se rasca la cabeza (no se entera)
    pasmado=('f_ojos_cerrados', 'pregunta'),  # foto: ojos cerrados, barbilla arriba (no se entera)
)
# el cuerpo sobre el que va cada cabeza de foto
CUERPO_FOTO = dict(dedos='grito', atril='dientes', nariz='llora_risa', calma='dientes', rasca='rie',
                   ojos_cerrados='llora_risa')
BAJA_FOTO = dict(nariz=0.05, rasca=0.08)
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
#  elipse que la abarca). Las fotos son de 'fotos'
#  (el collage de cinco) y 'fotos_extra' (el de once).
FOTOS = dict(
    nariz=('fotos', (520, 75, 1000, 475), (185, 150), (118, 152)),       # se tapa la nariz, ojos cerrados
    dedos=('fotos', (440, 525, 728, 1010), (142, 122), (88, 122)),       # grita, los dos indices
    rasca=('fotos', (5, 800, 445, 1250), (300, 200), (88, 125)),         # se rasca la cabeza, mira abajo
    atril=('fotos', (1325, 405, 1650, 722), (184, 72), (54, 66)),        # grita en el atril
    calma=('fotos', (1110, 985, 1500, 1245), (220, 96), (84, 94)),       # habla tranquilo
    ojos_cerrados=('fotos_extra', (1040, 25, 1245, 350), (110, 138), (94, 118)),  # ojos cerrados, barbilla arriba
)


def color_cabeza(f):
    """Media y dispersion por canal de la cabeza de una figura pintada (para pasarle
    su color a las fotos)."""
    y0, cx, hw, hom = medidas_cabeza(f)
    trozo = f[y0:y0 + hom, int(cx - hw * 0.45):int(cx + hw * 0.45)]
    a = trozo[..., 3] > 0
    v = trozo[..., :3][a].astype(float)
    return v.mean(0), v.std(0)


def cabeza_foto(rutas, nombre, ref=None):
    """La cabeza de una foto, sin fondo y recortada por su elipse, con un repaso de
    color y de contorno para que case con el pixel art (mas saturada, mas
    contraste y las lineas marcadas). Devuelve (rgba, centro x, ancho)."""
    from rembg import remove
    img, caja_f, (cx, cy), (rx, ry) = FOTOS[nombre]
    im = Image.open(rutas[img]).convert('RGB').crop(caja_f)
    sin_fondo(None)
    rgba = np.array(remove(im, session=_SESION))
    yy = np.arange(rgba.shape[0])[:, None]
    xx = np.arange(rgba.shape[1])[None, :]
    elipse = ((xx - cx) / float(rx)) ** 2 + ((yy - cy) / float(ry)) ** 2 < 1.0
    a = (rgba[..., 3] >= 128) & elipse
    lab, n = ndimage.label(a)
    if n > 1:
        tam = ndimage.sum(a, lab, range(1, n + 1))
        a = lab == (1 + int(np.argmax(tam)))
    if nombre == 'rasca':
        # el gorro (la kipa) se pinta del gris del pelo
        oscuro = (rgba[..., :3].astype(int).sum(2) < 150) & (yy < cy - ry * 0.55) & (np.abs(xx - cx) < rx * 0.7)
        rgba[oscuro, :3] = (150, 150, 156)
    ys = np.nonzero(a.any(1))[0]
    top = ys.min()
    rgba = rgba[top:]
    a = a[top:]
    # el ancho de la cabeza: la mediana de las filas entre el 30 y el 50 % de su alto
    h = ys.max() - top
    anchos = [np.ptp(np.nonzero(a[y])[0]) for y in range(int(h * 0.3), int(h * 0.5)) if a[y].any()]
    hw = float(np.median(anchos))
    hw = ANCHO_FOTO.get(nombre, hw)
    # el repaso de dibujo
    from PIL import ImageEnhance
    pic = Image.fromarray(rgba[..., :3])
    pic = ImageEnhance.Color(pic).enhance(1.35)
    pic = ImageEnhance.Contrast(pic).enhance(1.25)
    lum = np.array(pic.convert('L')).astype(float)
    borde = np.hypot(ndimage.sobel(lum, 0), ndimage.sobel(lum, 1))
    borde = np.clip((borde - 60) / 160.0, 0, 1) * 0.55
    col = np.array(pic).astype(float)
    if ref is not None:
        # el color de la cabeza pintada de referencia (media y dispersion por canal)
        for k in range(3):
            v = col[..., k][a]
            col[..., k] = ref[0][k] + (col[..., k] - v.mean()) * (ref[1][k] / (v.std() + 1e-6))
    col = col * (1 - borde[..., None])
    out = np.zeros_like(rgba)
    out[..., :3] = col.clip(0, 255).astype(np.uint8)
    out[..., 3] = np.where(a, 255, 0)
    return out, cx, hw


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


def figuras(frente, grita_rie, dientes_llora, fotos, fotos_extra):
    f = {}
    f['frente'] = limpia(sin_fondo(frente))
    f['grito'], f['rie'] = separa(limpia(sin_fondo(grita_rie)))
    f['dientes'], f['llora_risa'] = separa(limpia(sin_fondo(dientes_llora)))
    f['serio'] = limpia(pon_cabeza(f['dientes'], f['frente']))
    f['furia'] = cara_roja(f['grito'])
    rutas = dict(fotos=fotos, fotos_extra=fotos_extra)
    ref = color_cabeza(f['dientes'])
    for nombre, cuerpo in CUERPO_FOTO.items():
        cab, cx, hw = cabeza_foto(rutas, nombre, ref)
        f['f_' + nombre] = limpia(injerta(f[cuerpo], cab, cx, hw, BAJA_FOTO.get(nombre, 0.0)))
    return f


def main(args):
    if len(args) != 5:
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
