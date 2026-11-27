"""
=============================================================================
ESTRATOS - EL ATLAS DEL MARCADOR (fase 43 v10)
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/marcador_atlas.png con Pillow (despues de rehacer cualquiera de los
atlas de los monstruos):

    python3 sprites/hacer_atlas_marcador.py

Los cuatro atlas de emociones (4 x 3 caras cada uno) en una sola imagen de 2 x 2,
para que el shader del marcador (marcador_monstruos) lea de una sola entrada:

    arriba    0 trumpzilla      1 nefanyamuto
    abajo     2 godzilla        3 godzilla_azul

(el numero, el de MARCADOR_MON del motor). Cada atlas se reduce a 576 x 576
(caras de 144 x 192) para que el total, 1152 x 1152, quepa en el limite de 1280
pixeles de la licencia no comercial; en el marcador cada monstruo mide 36 x 48.
=============================================================================
"""

import os

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEN = ['trumpzilla', 'nefanyamuto', 'godzilla', 'godzilla_azul']
LADO = 576


def hacer():
    out = Image.new('RGBA', (2 * LADO, 2 * LADO), (0, 0, 0, 0))
    for k, n in enumerate(ORDEN):
        im = Image.open(os.path.join(AQUI, '%s_emociones.png' % n)).convert('RGBA')
        im = im.resize((LADO, LADO), Image.LANCZOS)
        a = im.getchannel('A').point(lambda v: 255 if v >= 128 else 0)    # pixel art: alfa limpio
        im.putalpha(a)
        out.paste(im, ((k % 2) * LADO, (k // 2) * LADO))
    ruta = os.path.join(AQUI, 'marcador_atlas.png')
    out.save(ruta, optimize=True)
    return ruta


if __name__ == '__main__':
    print(hacer())
