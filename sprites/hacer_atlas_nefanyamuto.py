"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DE NEFANYAMUTO
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/nefanyamuto_emociones.png (y la lamina de prueba) desde las imagenes de
origen (JPG de 1024 x 1024 en pixel art, con la ciudad en llamas de fondo):

    python3 sprites/hacer_atlas_nefanyamuto.py frente.jpg grita_rie.jpg dientes_llora.jpg

  frente.jpg         una figura de frente, brazos largos, la boca abierta (de ella sale la cara seria)
  grita_rie.jpg      dos figuras: grita con los ojos cerrados (izq.) y se rie (der.)
  dientes_llora.jpg  dos figuras: aprieta los dientes (izq.) y llora de risa (der.)

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
EMOCIONES = ['serio', 'enfado', 'furia', 'rie', 'carcajada', 'susto', 'mueca', 'llora', 'panico', 'calma']
TINTA = (24, 12, 12)

# de que figura sale cada cara (las marcadas con * son provisionales: repiten otra
# figura hasta que haya imagen propia)
ORIGEN = dict(
    serio='serio',          # cabeza de frente.jpg sobre el cuerpo de 'dientes'
    enfado='dientes',
    furia='furia',          # el grito con la cara roja
    rie='rie',
    carcajada='llora_risa',
    susto='grito',          # *
    mueca='dientes',        # *
    llora='llora_risa',     # *
    panico='grito',         # *
    calma='serio',          # *
)


# --- recorte ----------------------------------------------------------------------

def sin_fondo(ruta):
    from rembg import new_session, remove
    global _SESION
    try:
        _SESION
    except NameError:
        _SESION = new_session('isnet-general-use')
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
    """La cabeza de 'donante' (con el cuello de la camisa) sobre 'cuerpo': a la
    escala del ancho de su cabeza, alineada por la coronilla y el centro. La
    cabeza vieja se borra hasta los hombros."""
    cy0, ccx, chw, chom = medidas_cabeza(cuerpo)
    dy0, dcx, dhw, dhom = medidas_cabeza(donante)
    s = chw / dhw
    alto = dhom + 72
    x0 = int(dcx - dhw * 0.62)
    trozo = donante[dy0:dy0 + alto, x0:int(dcx + dhw * 0.62) + 1].copy()
    # abajo se estrecha (el cuello de la camisa, no los hombros)
    yy = np.arange(trozo.shape[0])[:, None]
    xx = np.arange(trozo.shape[1])[None, :] + x0
    deja = np.abs(xx - dcx) < dhw * (0.62 - 0.22 * np.clip((yy - dhom - 30) / 42.0, 0, 1))
    trozo[..., 3] = np.where(deja, trozo[..., 3], 0)
    t = Image.fromarray(trozo)
    t = t.resize((max(1, int(round(t.width * s))), max(1, int(round(t.height * s)))), Image.LANCZOS)
    tt = np.array(t)
    tt[..., 3] = np.where(tt[..., 3] >= 128, 255, 0)
    px, py = int(round(ccx - (dcx - x0) * s)), int(cy0)
    # se borra la cabeza vieja (hasta los hombros) y, debajo, solo lo que tapa la nueva
    huella = np.zeros(cuerpo.shape[:2], bool)
    h, w = tt.shape[:2]
    huella[py:py + h, px:px + w] = tt[..., 3] > 0
    o = cuerpo.copy()
    yy = np.arange(o.shape[0])[:, None]
    xx = np.arange(o.shape[1])[None, :]
    vieja = ((yy < cy0 + chom) & (np.abs(xx - ccx) < chw * 0.56)) | huella
    o[..., 3] = np.where(vieja, 0, o[..., 3])
    out = Image.fromarray(o)
    out.alpha_composite(Image.fromarray(tt), (px, py))
    return np.array(out)


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


def figuras(frente, grita_rie, dientes_llora):
    f = {}
    f['frente'] = limpia(sin_fondo(frente))
    f['grito'], f['rie'] = separa(limpia(sin_fondo(grita_rie)))
    f['dientes'], f['llora_risa'] = separa(limpia(sin_fondo(dientes_llora)))
    f['serio'] = limpia(pon_cabeza(f['dientes'], f['frente']))
    f['furia'] = cara_roja(f['grito'])
    return f


def main(args):
    if len(args) != 3:
        print(__doc__)
        sys.exit(1)
    f = figuras(*args)
    usadas = set(ORIGEN.values())
    alto = max(caja(f[k])[3] - caja(f[k])[1] for k in usadas)
    ancho = max(caja(f[k])[2] - caja(f[k])[0] for k in usadas)
    escala = min((CELDA_H - 2 * MARGEN) / float(alto), (CELDA_W - 2) / float(ancho))
    atlas = Image.new('RGBA', (CELDA_W * COLS, CELDA_H * FILAS), (0, 0, 0, 0))
    lamina = Image.new('RGBA', atlas.size, (60, 62, 68, 255))
    d = ImageDraw.Draw(lamina)
    celdas = {k: a_celda(f[k], escala) for k in usadas}
    for i, nombre in enumerate(EMOCIONES):
        im = celdas[ORIGEN[nombre]]
        x, y = (i % COLS) * CELDA_W, (i // COLS) * CELDA_H
        atlas.paste(im, (x, y))
        lamina.alpha_composite(im, (x, y))
        d.text((x + 4, y + 2), '%d %s' % (i, nombre), fill=(255, 230, 0, 255))
    atlas.save(os.path.join(AQUI, 'nefanyamuto_emociones.png'))
    lamina.save(os.path.join(AQUI, 'nefanyamuto_emociones_lamina.png'))
    print('nefanyamuto_emociones.png (%d x %d), escala %.3f, y la lamina' % (atlas.size + (escala,)))


if __name__ == '__main__':
    main(sys.argv[1:])
