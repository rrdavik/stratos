"""
=============================================================================
ESTRATOS - LA MISMA CLARIDAD PARA TODOS LOS MONSTRUOS
=============================================================================
No lo carga TouchDesigner: se corre fuera, con Pillow y NumPy:

    python3 sprites/igualar_brillo.py

Los tres monstruos en sprite (Trumpzilla, Godzilla y NefanyaMuto) salian de
origenes distintos (fotos, formas dibujadas, pixel art) y con claridades muy
distintas: con las mismas luces del planeta (mat_sprite) Godzilla se veia claro
y NefanyaMuto oscuro. Aqui se lleva cada atlas a la misma luminancia media
(LUM_OBJETIVO, sobre los pixeles opacos, 0 a 255) con una curva de gamma por
canal: el negro sigue negro y el blanco blanco, y se reparte el cambio por los
medios tonos (no se queman los claros ni se empastan los oscuros).

Es idempotente: un atlas ya igualado no cambia. Los tres hacer_atlas_* lo llaman
antes de guardar (igualar), asi que al rehacer un atlas sale ya igualado.
Reescribe tambien la lamina de prueba de cada uno.

Los emblemas del mal (mal_emblemas.png) no entran: son neon con luz propia.
=============================================================================
"""

import ast
import os

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
LUM_OBJETIVO = 72.0             # luminancia media (0-255) de los pixeles opacos de cada atlas
PESOS = np.array([0.299, 0.587, 0.114])
ATLAS = (('trumpzilla_emociones.png', 'hacer_atlas_trumpzilla.py'),
         ('godzilla_emociones.png', 'hacer_atlas_godzilla.py'),
         ('nefanyamuto_emociones.png', 'hacer_atlas_nefanyamuto.py'))


def luminancia(im):
    """La luminancia media (0-255) de los pixeles opacos (alfa > 128) de una imagen RGBA."""
    a = np.asarray(im.convert('RGBA')).astype(np.float64)
    m = a[..., 3] > 128
    return float((a[..., :3][m] @ PESOS).mean()) if m.any() else 0.0


def igualar(im, objetivo=LUM_OBJETIVO):
    """La imagen RGBA con la luminancia media de lo opaco en objetivo (gamma por canal; el
    alfa no se toca). Busca la gamma por biseccion; si ya esta, la devuelve igual."""
    im = im.convert('RGBA')
    a = np.asarray(im).astype(np.float64)
    m = a[..., 3] > 128
    if not m.any():
        return im
    rgb = a[..., :3][m] / 255.0
    if abs(float((rgb @ PESOS).mean()) * 255.0 - objetivo) < 0.5:
        return im
    lo, hi = 0.2, 5.0                   # la gamma: < 1 aclara, > 1 oscurece
    for _ in range(60):
        g = 0.5 * (lo + hi)
        if float(((rgb ** g) @ PESOS).mean()) * 255.0 > objetivo:
            lo = g
        else:
            hi = g
    g = 0.5 * (lo + hi)
    out = a.copy()
    out[..., :3] = 255.0 * (a[..., :3] / 255.0) ** g
    return Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8), 'RGBA')


def _emociones(script):
    """La tupla EMOCIONES del guion hacer_atlas_* (leida sin importarlo: algunos necesitan rembg)."""
    with open(os.path.join(AQUI, script)) as f:
        arbol = ast.parse(f.read())
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and any(getattr(t, 'id', '') == 'EMOCIONES' for t in nodo.targets):
            return list(ast.literal_eval(nodo.value))
    return []


def lamina(atlas, nombres, cols=4, celda=(192, 256)):
    """La lamina de prueba: el atlas sobre gris con el numero y el nombre de cada cara."""
    lam = Image.new('RGBA', atlas.size, (60, 62, 68, 255))
    lam.alpha_composite(atlas)
    d = ImageDraw.Draw(lam)
    for k, nombre in enumerate(nombres):
        d.text(((k % cols) * celda[0] + 4, (k // cols) * celda[1] + 2), '%d %s' % (k, nombre),
               fill=(255, 230, 0, 255))
    return lam


def main():
    for archivo, script in ATLAS:
        ruta = os.path.join(AQUI, archivo)
        im = Image.open(ruta).convert('RGBA')
        antes = luminancia(im)
        im = igualar(im)
        im.save(ruta)
        lamina(im, _emociones(script)).save(os.path.splitext(ruta)[0] + '_lamina.png')
        print('%-28s luminancia %5.1f -> %5.1f' % (archivo, antes, luminancia(im)))


if __name__ == '__main__':
    main()
