"""
=============================================================================
ESTRATOS - EL ATLAS DE EMOCIONES DEL GODZILLA AZUL (fase 42)
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/godzilla_azul_emociones.png (y la lamina de prueba) con Pillow:

    python3 sprites/hacer_atlas_godzilla_azul.py

El Godzilla azul es el segundo monstruo del bien: el mismo saurio que Godzilla
(hacer_atlas_godzilla.py, las mismas formas y las mismas diez caras) con otra
paleta: la piel azul cobalto, la tripa gris perla y las placas de la espalda de
hielo cian, que se encienden casi blancas en la furia. Asi se distingue de un
vistazo del Godzilla verde y de los dos monstruos del mal.

Mismo formato que los otros atlas: 4 x 3 celdas de 192 x 256, las caras en el
orden de EMOCIONES_MON del motor; mismo shader (mat_godzilla_azul).
=============================================================================
"""

import os

from PIL import Image

import hacer_atlas_godzilla as G
from igualar_brillo import igualar, lamina as lamina_igualada     # la misma claridad para todos los monstruos

EMOCIONES = ['serio', 'enfado', 'furia', 'rie', 'carcajada', 'susto', 'mueca', 'llora', 'panico', 'calma']

PALETA = dict(
    TINTA=(12, 22, 46, 255),
    PIEL=(44, 82, 168, 255),
    PIEL_OSC=(28, 54, 120, 255),
    PIEL_CLARA=(84, 128, 214, 255),
    TRIPA=(196, 208, 226, 255),
    TRIPA_OSC=(150, 166, 194, 255),
    PLACA=(120, 220, 240, 255),
    PLACA_OSC=(70, 160, 206, 255),
    PLACA_LUZ=(200, 250, 255, 255),
    HALO=(210, 248, 255, 255),
    OJO=(255, 240, 170, 255),
    OJO_FURIA=(120, 230, 255, 255),
    HOJA=(110, 210, 200, 255),
)


def main():
    for nombre, col in PALETA.items():      # las funciones de dibujo leen la paleta del modulo
        setattr(G, nombre, col)
    atlas = Image.new('RGBA', (G.CELDA_W * G.COLS, G.CELDA_H * G.FILAS), (0, 0, 0, 0))
    for k, nombre in enumerate(EMOCIONES):
        im = G.dibujar(nombre)
        atlas.paste(im, ((k % G.COLS) * G.CELDA_W, (k // G.COLS) * G.CELDA_H))
    atlas = igualar(atlas)                  # la claridad comun (igualar_brillo.py)
    atlas.save(os.path.join(G.AQUI, 'godzilla_azul_emociones.png'))
    lamina_igualada(atlas, EMOCIONES).save(os.path.join(G.AQUI, 'godzilla_azul_emociones_lamina.png'))
    print('godzilla_azul_emociones.png (%d x %d) y la lamina' % atlas.size)


if __name__ == '__main__':
    main()
