"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DE TRUMPZILLA (fase 38)
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/trumpzilla_emociones.png desde las imagenes de origen (JPG con el fondo
de cuadros gris y blanco pintado):

    python3 sprites/hacer_atlas_trumpzilla.py enfado.jpg cuatro_a.jpg cuatro_b.jpg serio.jpg

  enfado.jpg     una figura: ruge con los punos cerrados (la de 1152 x 1712)
  cuatro_a.jpg   cuatro figuras: rie, llora, panico (llora asustado), calma
  cuatro_b.jpg   cuatro figuras: susto, mueca, furia (roja), carcajada (llora de risa)
  serio.jpg      una figura: serio, con el ceno fruncido

Que hace:
  1. Quita el fondo de cuadros: relleno desde el borde por los grises y blancos
     neutros, y dentro de la figura los huecos que son cuadros (gris y blanco a
     la vez; la camisa, crema y con sombras, no lo es).
  2. Separa las cuatro figuras de cada fila por el contorno izquierdo de la
     figura siguiente (la de la derecha va delante). La cola y las espinas de
     las tres primeras quedan tapadas por la vecina, y la de la cuarta, cortada por
     el borde de la imagen: debajo de las ocho se pone la espalda (espinas y cola)
     de serio.jpg, a su altura y alineada por los pies y la chaqueta.
  3. Recorta cada figura y la mete en su celda (CELDA_W x CELDA_H) con los pies
     abajo y centrados: todas a la misma altura. Todas miran a la izquierda de
     la imagen; el shader las voltea cuando el monstruo camina a la derecha.
  4. Escribe el atlas (COLS x FILAS celdas, en el orden de EMOCIONES, de arriba
     a la izquierda) y una lamina de prueba sobre gris.

El orden de EMOCIONES es el del motor (EMOCIONES_MON): si se cambia aqui, se
cambia alli.
=============================================================================
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

AQUI = os.path.dirname(os.path.abspath(__file__))
CELDA_W, CELDA_H = 192, 256
COLS, FILAS = 4, 3
MARGEN = 6
EMOCIONES = ['serio', 'enfado', 'furia', 'rie', 'carcajada', 'susto', 'mueca', 'llora', 'panico', 'calma']

# el contorno izquierdo de una figura de las filas de cuatro, (y, dx) desde su
# arranque (el borde de la chaqueta a y = 700), en pixeles de la imagen de origen
CONTORNO = [(0, 0), (650, -4), (850, 0), (900, 12), (950, 16), (1000, 20), (1050, 28), (1100, 34),
            (1130, 30), (1150, 14), (1175, -6), (1712, -15)]
PIES_Y = 1150               # por debajo, las garras (la apertura fuerte se las comeria)
BANDA = 40                  # px a la derecha del corte izquierdo donde se buscan restos de la vecina
PADDING = 320               # lienzo de mas a cada lado: la cola de la cuarta sale de la imagen
ARRANQUES = {'a': (300, 562, 852), 'b': (298, 548, 843)}
# la espalda de serio.jpg (espinas y cola enteras): a la derecha de x(y), solo lo
# gris (espinas) y lo verde (cola); la chaqueta y el pelo no
ESPALDA = [(165, 395), (265, 400), (300, 505), (350, 540), (400, 565), (450, 580), (700, 590),
           (750, 575), (935, 560)]


def sin_fondo(path):
    im = np.asarray(Image.open(path).convert('RGB')).astype(np.int16)
    mx, mn = im.max(2), im.min(2)
    fondo = (mx - mn < 22) & (mn > 185)
    lab, n = ndimage.label(fondo)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(borde))
    neutro = mx - mn <= 6
    blanco = neutro & (mn >= 246)
    gris = neutro & (mn >= 205) & (mx <= 232)
    for k in range(1, n + 1):
        if k in borde:
            continue
        comp = lab == k
        sz = comp.sum()
        if sz < 150:
            continue
        fb, fg = (blanco & comp).sum() / sz, (gris & comp).sum() / sz
        if fb > 0.15 and fg > 0.15 and fb + fg > 0.55:
            bg |= comp
    fg = ~bg
    lab2, n2 = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
    keep = np.zeros(n2 + 1, bool)
    keep[1:] = sizes > 400
    fg = keep[lab2]
    fg = ndimage.binary_opening(fg, iterations=1)
    fg = ndimage.binary_erosion(fg, iterations=1)
    return np.dstack([im.astype(np.uint8), (fg * 255).astype(np.uint8)])


def _polilinea(puntos, alto):
    ys = np.arange(alto)
    return np.interp(ys, [p[0] for p in puntos], [p[1] for p in puntos])


def ventana(rgba, x0, x1):
    """Lo de la figura entre los contornos x0(y) y x1(y) (arrays por fila)."""
    h, w = rgba.shape[:2]
    xs = np.arange(w)[None, :]
    m = (xs >= x0[:, None]) & (xs < x1[:, None])
    out = rgba.copy()
    out[..., 3] = np.where(m, out[..., 3], 0)
    return out


def sin_restos(rgba, x0):
    """Quita lo que entra por el corte izquierdo x0(y) sin ser del cuerpo (la cola
    y las espinas de la vecina): en una BANDA junto al corte, una apertura rompe
    los puentes finos; luego fuera los trozos (salvo el mayor) que tocan el corte."""
    a = rgba[..., 3] > 0
    h, w = a.shape
    xs = np.arange(w)[None, :]
    banda = (xs >= x0[:, None]) & (xs < x0[:, None] + BANDA)
    abierta = ndimage.binary_opening(a, iterations=3)
    mas = ndimage.binary_opening(a, iterations=7)          # por encima de los pies: las cunas de espinas
    abierta[:PIES_Y] = mas[:PIES_Y]
    a = np.where(banda, abierta, a)
    lab, n = ndimage.label(a)
    if n >= 2:
        sizes = ndimage.sum(a, lab, range(1, n + 1))
        mayor = 1 + int(np.argmax(sizes))
        junto = (xs >= x0[:, None]) & (xs < x0[:, None] + 6) & a
        fuera = set(np.unique(lab[junto])) - {0, mayor}
        a &= ~np.isin(lab, list(fuera))
    out = rgba.copy()
    out[..., 3] = np.where(a, out[..., 3], 0)
    return out


def figuras(rgba, arranques):
    rgba = np.pad(rgba, ((0, 0), (0, PADDING), (0, 0)))
    h, w = rgba.shape[:2]
    cont = _polilinea(CONTORNO, h)
    cortes = [np.full(h, -1.0)] + [a + cont for a in arranques] + [np.full(h, w + 1.0)]
    return [sin_restos(ventana(rgba, cortes[k], cortes[k + 1]), cortes[k]) for k in range(4)]


def espalda(serio):
    """Las espinas y la cola de serio.jpg, sin chaqueta ni pelo."""
    h, w = serio.shape[:2]
    xb = _polilinea(ESPALDA, h)
    ys = np.arange(h)
    xb[(ys < ESPALDA[0][0]) | (ys > ESPALDA[-1][0])] = w + 1
    out = ventana(serio, xb, np.full(h, w + 1.0))
    c = out[..., :3].astype(np.int16)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    gris = c.max(2) - c.min(2) < 40
    verde = (g > b + 10) & (g >= r - 5)
    out[..., 3] = np.where(gris | verde, out[..., 3], 0)
    return out


def _azul_derecho(rgba, f):
    """El borde derecho de la chaqueta a la altura relativa f de la figura."""
    ys = np.nonzero((rgba[..., 3] > 0).any(1))[0]
    y = int(ys.min() + f * (ys.max() - ys.min()))
    c = rgba[y - 3:y + 4].astype(np.int16)
    azul = (c[..., 2] > c[..., 0] + 30) & (c[..., 3] > 0)
    return np.nonzero(azul.any(0))[0].max()


def con_espalda(fig, serio, capa):
    """fig con la espalda de serio debajo: escalada a su altura y alineada por los
    pies (abajo) y por el borde derecho de la chaqueta (a media altura)."""
    def alto(a):
        ys = np.nonzero((a[..., 3] > 0).any(1))[0]
        return ys.min(), ys.max()
    y0, y1 = alto(fig)
    s0, s1 = alto(serio)
    k = (y1 - y0) / float(s1 - s0)
    h, w = serio.shape[:2]
    cs = np.asarray(Image.fromarray(capa, 'RGBA').resize((int(round(w * k)), int(round(h * k))), Image.LANCZOS))
    ss = np.asarray(Image.fromarray(serio, 'RGBA').resize((int(round(w * k)), int(round(h * k))), Image.LANCZOS))
    dx = _azul_derecho(fig, 0.5) - _azul_derecho(ss, 0.5)
    dy = y1 - int(round(s1 * k))
    lienzo = np.zeros_like(fig)
    H, W = fig.shape[:2]
    ch, cw = cs.shape[:2]
    for yy in range(ch):
        ty = yy + dy
        if 0 <= ty < H:
            x0, x1 = max(0, dx), min(W, cw + dx)
            if x1 > x0:
                lienzo[ty, x0:x1] = cs[yy, x0 - dx:x1 - dx]
    lienzo[..., 3] = np.where(lienzo[..., 3] >= 128, 255, 0)
    return debajo(fig, lienzo, (0, 0))


def debajo(fig, capa, d):
    """capa (desplazada d) detras de fig."""
    dx, dy = d
    c = np.roll(np.roll(capa, dy, 0), dx, 1)
    fa = fig[..., 3:4] / 255.0
    ca = c[..., 3:4] / 255.0
    out = fig.copy().astype(np.float32)
    out[..., :3] = fig[..., :3] * fa + c[..., :3] * ca * (1 - fa)
    a = fa + ca * (1 - fa)
    out[..., :3] = np.where(a > 0, out[..., :3] / np.maximum(a, 1e-6), 0)
    out[..., 3:4] = a * 255
    return out.clip(0, 255).astype(np.uint8)


def recorte(rgba):
    ys, xs = np.nonzero(rgba[..., 3] > 0)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def a_celda(rgba):
    """La figura en su celda: los pies abajo y en el centro, a la altura comun."""
    f = recorte(rgba)
    h, w = f.shape[:2]
    a = f[..., 3] > 0
    pies = a[int(h * 0.92):]
    px = np.nonzero(pies.any(0))[0]
    ancla = 0.5 * (px.min() + px.max())
    s = (CELDA_H - 2 * MARGEN) / float(h)
    s = min(s, (CELDA_W / 2.0 - 2) / max(ancla, 1.0), (CELDA_W / 2.0 - 2) / max(w - ancla, 1.0))
    nw, nh = max(1, int(round(w * s))), max(1, int(round(h * s)))
    im = Image.fromarray(f, 'RGBA').resize((nw, nh), Image.LANCZOS)
    arr = np.asarray(im).copy()
    arr[..., 3] = np.where(arr[..., 3] >= 128, 255, 0)      # recorte duro: el shader descarta por alfa
    celda = Image.new('RGBA', (CELDA_W, CELDA_H), (0, 0, 0, 0))
    celda.paste(Image.fromarray(arr, 'RGBA'), (int(round(CELDA_W / 2.0 - ancla * s)), CELDA_H - MARGEN - nh))
    return celda


def hacer(enfado, cuatro_a, cuatro_b, serio, salida):
    A = figuras(sin_fondo(cuatro_a), ARRANQUES['a'])
    B = figuras(sin_fondo(cuatro_b), ARRANQUES['b'])
    se = sin_fondo(serio)
    capa = espalda(se)
    for fs in (A, B):
        for k in range(4):
            fs[k] = con_espalda(fs[k], se, capa)
    fuentes = dict(serio=se, enfado=sin_fondo(enfado),
                   rie=A[0], llora=A[1], panico=A[2], calma=A[3],
                   susto=B[0], mueca=B[1], furia=B[2], carcajada=B[3])
    atlas = Image.new('RGBA', (COLS * CELDA_W, FILAS * CELDA_H), (0, 0, 0, 0))
    for k, nombre in enumerate(EMOCIONES):
        atlas.paste(a_celda(fuentes[nombre]), ((k % COLS) * CELDA_W, (k // COLS) * CELDA_H))
    atlas.save(salida)
    lamina = Image.new('RGBA', atlas.size, (70, 74, 80, 255))
    lamina.alpha_composite(atlas)
    d = ImageDraw.Draw(lamina)
    for k, nombre in enumerate(EMOCIONES):
        d.text(((k % COLS) * CELDA_W + 4, (k // COLS) * CELDA_H + 2), '%d %s' % (k, nombre), fill=(255, 255, 0))
    lamina.convert('RGB').save(os.path.splitext(salida)[0] + '_lamina.png')
    print('atlas %s: %d emociones en %d x %d celdas de %d x %d' % (salida, len(EMOCIONES), COLS, FILAS,
                                                                  CELDA_W, CELDA_H))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(1)
    hacer(*sys.argv[1:5], salida=sys.argv[5] if len(sys.argv) > 5 else
          os.path.join(AQUI, 'trumpzilla_emociones.png'))
