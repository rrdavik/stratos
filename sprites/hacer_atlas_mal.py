"""
=============================================================================
ESTRATOS - EL ATLAS DE EMBLEMAS DEL MAL (fase 39)
=============================================================================
No lo carga TouchDesigner: se corre una vez, fuera, para rehacer
sprites/mal_emblemas.png (y la lamina de prueba sprites/mal_emblemas_lamina.png):

    python3 sprites/hacer_atlas_mal.py

Los emblemas del mal se dibujan aqui con Pillow, como tubos de neon: un trazo de
color con su alma clara y un borde oscuro que lo separa del cielo. Rosa neon =
dinero; rojo = vigilancia y demonios; hueso = la calavera. Cuerpos casi negros.

El atlas tiene COLS x FILAS celdas de CELDA_W x CELDA_H (2:1: cabe un dolar, un
demonio y otro dolar en fila), con fondo transparente y recorte duro (el shader
descarta por alfa y lee pixel a pixel). El orden es el de EMBLEMAS_MAL del motor,
de arriba a la izquierda: si se cambia aqui, se cambia alli.
=============================================================================
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
EMBLEMAS = ('prohibido', 'dolar', 'dolar_demonio', 'dolar_demonio_dolar', 'magnate', 'copa', 'diamante',
            'candado', 'ojo', 'sirena', 'calavera', 'proximamente', 'demonio', 'diablillo', 'cabeza', 'coloso')
COLS, FILAS = 4, 4
CELDA_W, CELDA_H = 256, 128
K = 4                                   # se dibuja a 4 x y se reduce: bordes limpios

ROSA = (255, 46, 146)
ROSA_ALMA = (255, 190, 225)
ROJO = (232, 28, 40)
ROJO_ALMA = (255, 150, 140)
HUESO = (240, 230, 206)
NEGRO = (16, 12, 18)
CUERPO = (34, 24, 36)
OJO = (255, 210, 60)

FUENTES = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
           '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
           'C:/Windows/Fonts/arialbd.ttf']


def fuente(px):
    for f in FUENTES:
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def tubo_linea(d, pts, col, alma, w, cerrado=False):
    """Un tubo de neon por una polilinea: borde oscuro, color y alma clara."""
    if cerrado:
        pts = list(pts) + [pts[0]]
    for ancho, c in ((w + 3 * K, NEGRO), (w, col), (max(K, w // 3), alma)):
        d.line(pts, fill=c, width=ancho, joint='curve')
        r = ancho / 2.0
        for x, y in pts:
            d.ellipse((x - r, y - r, x + r, y + r), fill=c)


def tubo_arco(d, caja, a0, a1, col, alma, w):
    for ancho, c in ((w + 3 * K, NEGRO), (w, col), (max(K, w // 3), alma)):
        d.arc(caja, a0, a1, fill=c, width=ancho)


def tubo_texto(d, x, y, txt, px, col, alma):
    f = fuente(px)
    d.text((x, y), txt, font=f, fill=col, anchor='mm', stroke_width=max(2, px // 9), stroke_fill=NEGRO)
    f2 = fuente(int(px * 0.92))
    d.text((x, y), txt, font=f2, fill=alma, anchor='mm')
    d.text((x, y), txt, font=f2, fill=col, anchor='mm', stroke_width=0)


def circulo(cx, cy, r):
    return (cx - r, cy - r, cx + r, cy + r)


# --- los iconos (centro cx cy, lado s en pixeles a escala K) ----------------------------

def dolar(d, cx, cy, s):
    f = fuente(int(s * 0.95))
    d.text((cx, cy), '$', font=f, fill=ROSA, anchor='mm', stroke_width=int(s * 0.07), stroke_fill=NEGRO)
    d.text((cx, cy), '$', font=f, fill=ROSA, anchor='mm', stroke_width=int(s * 0.025), stroke_fill=ROSA)
    f2 = fuente(int(s * 0.62))                  # el alma clara del tubo
    d.text((cx, cy), '$', font=f2, fill=ROSA_ALMA, anchor='mm')


def prohibido(d, cx, cy, s):
    r = s * 0.44
    d.ellipse(circulo(cx, cy, r + 3 * K), fill=NEGRO)
    d.ellipse(circulo(cx, cy, r), fill=ROJO)
    d.ellipse(circulo(cx, cy, r * 0.86), outline=ROJO_ALMA, width=int(s * 0.03))
    d.rounded_rectangle((cx - r * 0.66, cy - r * 0.17, cx + r * 0.66, cy + r * 0.17), radius=int(r * 0.08),
                        fill=HUESO)


def demonio(d, cx, cy, s, ojos=OJO, cuerpo=ROJO, borde=NEGRO):
    """La cara del demonio: cuernos, ojos rasgados y la sonrisa de dientes."""
    r = s * 0.36
    for sg in (-1, 1):                      # los cuernos
        cuerno = [(cx + sg * r * 0.55, cy - r * 0.55), (cx + sg * r * 1.25, cy - r * 1.35),
                  (cx + sg * r * 0.95, cy - r * 0.35)]
        d.polygon(cuerno, fill=cuerpo, outline=borde, width=2 * K)
    d.polygon([(cx - r, cy - r * 0.5), (cx + r, cy - r * 0.5), (cx + r * 0.85, cy + r * 0.45),
               (cx, cy + r * 1.1), (cx - r * 0.85, cy + r * 0.45)], fill=cuerpo, outline=borde, width=3 * K)
    for sg in (-1, 1):                      # los ojos
        d.polygon([(cx + sg * r * 0.15, cy - r * 0.12), (cx + sg * r * 0.7, cy - r * 0.32),
                   (cx + sg * r * 0.55, cy + r * 0.05)], fill=ojos)
    d.chord((cx - r * 0.6, cy - r * 0.1, cx + r * 0.6, cy + r * 0.75), 0, 180, fill=HUESO, outline=borde,
            width=2 * K)
    for k in range(-2, 3):
        x = cx + k * r * 0.2
        d.line((x, cy + r * 0.32, x, cy + r * 0.62), fill=borde, width=2 * K)


def magnate(d, cx, cy, s):
    """La cara del dueno en el totem: un aro rosa, dos dolares de ojos y la sonrisa."""
    r = s * 0.44
    tubo_arco(d, circulo(cx, cy, r), 0, 360, ROSA, ROSA_ALMA, int(s * 0.07))
    d.ellipse(circulo(cx, cy, r * 0.86), fill=NEGRO)
    f = fuente(int(s * 0.34))
    for sg in (-1, 1):
        d.text((cx + sg * r * 0.36, cy - r * 0.22), '$', font=f, fill=ROSA, anchor='mm')
    d.chord((cx - r * 0.55, cy - r * 0.05, cx + r * 0.55, cy + r * 0.62), 0, 180, fill=HUESO)
    for k in range(-2, 3):
        x = cx + k * r * 0.18
        d.line((x, cy + r * 0.25, x, cy + r * 0.55), fill=NEGRO, width=2 * K)


def copa(d, cx, cy, s):
    r = s * 0.42
    w = int(s * 0.07)
    tubo_linea(d, [(cx - r, cy - r * 0.7), (cx + r, cy - r * 0.7), (cx, cy + r * 0.25)], ROSA, ROSA_ALMA, w,
               cerrado=True)
    tubo_linea(d, [(cx, cy + r * 0.25), (cx, cy + r * 0.85)], ROSA, ROSA_ALMA, w)
    tubo_linea(d, [(cx - r * 0.45, cy + r * 0.88), (cx + r * 0.45, cy + r * 0.88)], ROSA, ROSA_ALMA, w)
    d.ellipse(circulo(cx + r * 0.42, cy - r * 0.85, r * 0.16), fill=ROSA_ALMA, outline=NEGRO, width=2 * K)


def diamante(d, cx, cy, s):
    r = s * 0.45
    w = int(s * 0.06)
    top, mid, bot = cy - r * 0.55, cy - r * 0.15, cy + r * 0.8
    pts = [(cx - r * 0.55, top), (cx + r * 0.55, top), (cx + r, mid), (cx, bot), (cx - r, mid)]
    tubo_linea(d, pts, ROSA, ROSA_ALMA, w, cerrado=True)
    tubo_linea(d, [(cx - r, mid), (cx + r, mid)], ROSA, ROSA_ALMA, w // 2 + K)
    for a, b in (((cx - r * 0.2, top), (cx - r * 0.45, mid)), ((cx + r * 0.2, top), (cx + r * 0.45, mid)),
                 ((cx - r * 0.45, mid), (cx, bot)), ((cx + r * 0.45, mid), (cx, bot))):
        tubo_linea(d, [a, b], ROSA, ROSA_ALMA, w // 2 + K)


def candado(d, cx, cy, s):
    r = s * 0.42
    tubo_arco(d, (cx - r * 0.5, cy - r * 0.95, cx + r * 0.5, cy + r * 0.05), 180, 360, ROJO, ROJO_ALMA,
              int(s * 0.08))
    tubo_linea(d, [(cx - r * 0.5, cy - r * 0.45), (cx - r * 0.5, cy - r * 0.05)], ROJO, ROJO_ALMA, int(s * 0.08))
    tubo_linea(d, [(cx + r * 0.5, cy - r * 0.45), (cx + r * 0.5, cy - r * 0.05)], ROJO, ROJO_ALMA, int(s * 0.08))
    d.rounded_rectangle((cx - r * 0.8, cy - r * 0.1, cx + r * 0.8, cy + r * 0.9), radius=int(r * 0.12),
                        fill=ROJO, outline=NEGRO, width=3 * K)
    d.ellipse(circulo(cx, cy + r * 0.3, r * 0.14), fill=NEGRO)
    d.rectangle((cx - r * 0.05, cy + r * 0.3, cx + r * 0.05, cy + r * 0.62), fill=NEGRO)


def ojo(d, cx, cy, s):
    r = s * 0.46
    w = int(s * 0.07)
    arriba = [(cx - r + 2 * r * k / 16.0, cy - r * 0.55 * math.sin(math.pi * k / 16.0)) for k in range(17)]
    abajo = [(cx + r - 2 * r * k / 16.0, cy + r * 0.55 * math.sin(math.pi * k / 16.0)) for k in range(17)]
    d.polygon(arriba + abajo, fill=NEGRO)
    tubo_linea(d, arriba + abajo, ROJO, ROJO_ALMA, w, cerrado=True)
    d.ellipse(circulo(cx, cy, r * 0.3), fill=ROJO, outline=NEGRO, width=2 * K)
    d.ellipse(circulo(cx, cy, r * 0.12), fill=NEGRO)
    d.ellipse(circulo(cx - r * 0.08, cy - r * 0.08, r * 0.05), fill=ROJO_ALMA)


def sirena(d, cx, cy, s):
    r = s * 0.4
    d.rectangle((cx - r * 0.75, cy + r * 0.45, cx + r * 0.75, cy + r * 0.75), fill=(70, 66, 72), outline=NEGRO,
                width=2 * K)
    d.chord((cx - r * 0.55, cy - r * 0.5, cx + r * 0.55, cy + r * 1.0), 180, 360, fill=ROJO, outline=NEGRO,
            width=3 * K)
    d.rectangle((cx - r * 0.55, cy + r * 0.2, cx + r * 0.55, cy + r * 0.47), fill=ROJO, outline=NEGRO, width=2 * K)
    d.ellipse(circulo(cx - r * 0.18, cy - r * 0.05, r * 0.12), fill=ROJO_ALMA)
    for a in (-150, -120, -90, -60, -30):           # los destellos
        t = math.radians(a)
        p0 = (cx + math.cos(t) * r * 0.85, cy + r * 0.15 + math.sin(t) * r * 0.85)
        p1 = (cx + math.cos(t) * r * 1.2, cy + r * 0.15 + math.sin(t) * r * 1.2)
        tubo_linea(d, [p0, p1], ROJO, ROJO_ALMA, int(s * 0.05))


def calavera(d, cx, cy, s, halo=True):
    r = s * 0.42
    if halo:                                        # el resplandor rojo, en aros (sin transparencias)
        for k, c in enumerate(((90, 10, 18), (150, 18, 28), (210, 30, 40))):
            d.ellipse(circulo(cx, cy - r * 0.05, r * (1.18 - 0.07 * k)), fill=c)
    d.ellipse((cx - r * 0.8, cy - r * 0.95, cx + r * 0.8, cy + r * 0.45), fill=HUESO, outline=NEGRO, width=3 * K)
    d.rounded_rectangle((cx - r * 0.48, cy + r * 0.1, cx + r * 0.48, cy + r * 0.78), radius=int(r * 0.12),
                        fill=HUESO, outline=NEGRO, width=3 * K)
    for sg in (-1, 1):
        d.ellipse(circulo(cx + sg * r * 0.33, cy - r * 0.2, r * 0.22), fill=NEGRO)
    d.polygon([(cx, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.22), (cx + r * 0.1, cy + r * 0.22)], fill=NEGRO)
    for k in range(-2, 3):
        x = cx + k * r * 0.17
        d.line((x, cy + r * 0.42, x, cy + r * 0.76), fill=NEGRO, width=2 * K)


def proximamente(d, cx, cy, w, h):
    """El cartel: «PROXIMAMENTE» sobre el dolar, borde de neon rosa."""
    d.rectangle((cx - w * 0.47, cy - h * 0.44, cx + w * 0.47, cy + h * 0.44), fill=NEGRO)
    tubo_linea(d, [(cx - w * 0.44, cy - h * 0.4), (cx + w * 0.44, cy - h * 0.4), (cx + w * 0.44, cy + h * 0.4),
                   (cx - w * 0.44, cy + h * 0.4)], ROSA, ROSA_ALMA, 3 * K, cerrado=True)
    f = fuente(int(h * 0.22))
    d.text((cx, cy - h * 0.18), 'PRÓXIMAMENTE', font=f, fill=ROSA_ALMA, anchor='mm')
    dolar(d, cx, cy + h * 0.16, h * 0.42)


def diablillo(d, cx, cy, s):
    """El diablillo del cluster de 4 a 6: sentado, con su cola y su tridente."""
    r = s * 0.4
    tubo_arco(d, (cx + r * 0.1, cy + r * 0.1, cx + r * 1.1, cy + r * 0.9), 270, 90, ROJO, ROJO_ALMA, int(s * 0.04))
    d.polygon([(cx + r * 1.0, cy + r * 0.85), (cx + r * 1.2, cy + r * 0.95), (cx + r * 1.0, cy + r * 1.05)],
              fill=ROJO)
    d.ellipse((cx - r * 0.45, cy + r * 0.05, cx + r * 0.45, cy + r * 0.85), fill=ROJO, outline=NEGRO, width=3 * K)
    for sg in (-1, 1):                              # las piernas colgando
        d.line((cx + sg * r * 0.2, cy + r * 0.7, cx + sg * r * 0.3, cy + r * 1.05), fill=ROJO, width=int(s * 0.07))
    tubo_linea(d, [(cx - r * 0.85, cy - r * 0.9), (cx - r * 0.85, cy + r * 1.0)], (90, 80, 96), (160, 150, 170),
               int(s * 0.03))
    for k in (-1, 0, 1):
        d.line((cx - r * 0.85 + k * r * 0.14, cy - r * 1.05, cx - r * 0.85 + k * r * 0.14, cy - r * 0.85),
               fill=(160, 150, 170), width=int(s * 0.03))
    demonio(d, cx, cy - r * 0.35, s * 0.62)


def cabeza(d, cx, cy, w, h):
    """La cabeza del cluster de 7 a 9: asoma detras, oscura, con el borde rojo encendido."""
    s = h * 1.0
    r = s * 0.42
    for sg in (-1, 1):
        cuerno = [(cx + sg * r * 0.6, cy - r * 0.3), (cx + sg * r * 1.5, cy - r * 1.05),
                  (cx + sg * r * 1.0, cy - r * 0.0)]
        d.polygon(cuerno, fill=CUERPO, outline=ROJO, width=4 * K)
    cara = [(cx - r * 1.05, cy - r * 0.35), (cx + r * 1.05, cy - r * 0.35), (cx + r * 0.95, cy + r * 0.55),
            (cx, cy + r * 1.15), (cx - r * 0.95, cy + r * 0.55)]
    d.polygon(cara, fill=CUERPO)
    tubo_linea(d, cara, ROJO, ROJO_ALMA, 4 * K, cerrado=True)
    for sg in (-1, 1):
        d.polygon([(cx + sg * r * 0.12, cy - r * 0.02), (cx + sg * r * 0.72, cy - r * 0.22),
                   (cx + sg * r * 0.58, cy + r * 0.15)], fill=ROSA)
    d.chord((cx - r * 0.62, cy + r * 0.05, cx + r * 0.62, cy + r * 0.85), 0, 180, fill=HUESO)
    for k in range(-3, 4):
        x = cx + k * r * 0.16
        d.line((x, cy + r * 0.45, x, cy + r * 0.8), fill=NEGRO, width=2 * K)


def coloso(d, cx, cy, w, h):
    """El coloso del cluster de 10 o mas: los brazos abiertos (abraza el cluster),
    los cuernos y la calavera en el pecho."""
    r = h * 0.42
    torso = [(cx - r * 0.75, cy - r * 0.1), (cx + r * 0.75, cy - r * 0.1), (cx + r * 0.6, cy + r * 1.2),
             (cx - r * 0.6, cy + r * 1.2)]
    for sg in (-1, 1):                              # los brazos, abiertos y hacia abajo
        brazo = [(cx + sg * r * 0.7, cy - r * 0.05), (cx + sg * w * 0.42, cy + r * 0.2),
                 (cx + sg * w * 0.47, cy + r * 1.15), (cx + sg * w * 0.38, cy + r * 1.15),
                 (cx + sg * w * 0.34, cy + r * 0.5), (cx + sg * r * 0.7, cy + r * 0.45)]
        d.polygon(brazo, fill=CUERPO)
        tubo_linea(d, brazo, ROJO, ROJO_ALMA, 3 * K, cerrado=True)
        for k in range(3):                          # las garras
            x = cx + sg * (w * 0.38 + k * w * 0.03)
            d.polygon([(x, cy + r * 1.15), (x + sg * w * 0.012, cy + r * 1.3), (x + sg * w * 0.025, cy + r * 1.15)],
                      fill=ROJO)
    d.polygon(torso, fill=CUERPO)
    tubo_linea(d, torso, ROJO, ROJO_ALMA, 3 * K, cerrado=True)
    cabeza(d, cx, cy - r * 0.55, w, h * 0.55)
    calavera(d, cx, cy + r * 0.6, h * 0.36, halo=False)


def dibujar(nombre, d, x0, y0):
    w, h = CELDA_W * K, CELDA_H * K
    cx, cy = x0 + w / 2.0, y0 + h / 2.0
    s = h * 0.92
    if nombre == 'prohibido':
        prohibido(d, cx, cy, s)
    elif nombre == 'dolar':
        dolar(d, cx, cy, s)
    elif nombre == 'dolar_demonio':
        dolar(d, cx - s * 0.42, cy, s * 0.9)
        demonio(d, cx + s * 0.45, cy + s * 0.06, s * 0.9)
    elif nombre == 'dolar_demonio_dolar':
        dolar(d, cx - s * 0.78, cy, s * 0.8)
        demonio(d, cx, cy + s * 0.06, s * 0.85)
        dolar(d, cx + s * 0.78, cy, s * 0.8)
    elif nombre == 'magnate':
        magnate(d, cx, cy, s)
    elif nombre == 'copa':
        copa(d, cx, cy, s)
    elif nombre == 'diamante':
        diamante(d, cx, cy, s)
    elif nombre == 'candado':
        candado(d, cx, cy, s)
    elif nombre == 'ojo':
        ojo(d, cx, cy, s)
    elif nombre == 'sirena':
        sirena(d, cx, cy, s)
    elif nombre == 'calavera':
        calavera(d, cx, cy, s)
    elif nombre == 'proximamente':
        proximamente(d, cx, cy, w * 0.98, h * 0.98)
    elif nombre == 'demonio':
        demonio(d, cx, cy + s * 0.06, s)
    elif nombre == 'diablillo':
        diablillo(d, cx, cy, s)
    elif nombre == 'cabeza':
        cabeza(d, cx, cy + h * 0.06, w, h * 0.92)
    elif nombre == 'coloso':
        coloso(d, cx, cy - h * 0.02, w, h * 0.92)


def atlas():
    W, H = COLS * CELDA_W, FILAS * CELDA_H
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for k, nombre in enumerate(EMBLEMAS):
        grande = Image.new('RGBA', (CELDA_W * K, CELDA_H * K), (0, 0, 0, 0))
        d = ImageDraw.Draw(grande)
        dibujar(nombre, d, 0, 0)
        chica = grande.resize((CELDA_W, CELDA_H), Image.LANCZOS)
        px = chica.load()
        for y in range(CELDA_H):               # recorte duro: alfa 0 o 255, color sin premultiplicar
            for x in range(CELDA_W):
                r, g, b, a = px[x, y]
                px[x, y] = (r, g, b, 255) if a >= 128 else (0, 0, 0, 0)
        out.paste(chica, ((k % COLS) * CELDA_W, (k // COLS) * CELDA_H))
    return out


def lamina(at):
    """La hoja de prueba: cada emblema sobre el cielo oscuro, con su nombre, y a 20 px."""
    fondo = (22, 22, 26)
    lam = Image.new('RGB', (COLS * (CELDA_W + 120) + 20, FILAS * (CELDA_H + 34) + 20), fondo)
    d = ImageDraw.Draw(lam)
    f = fuente(14)
    for k, nombre in enumerate(EMBLEMAS):
        c = at.crop(((k % COLS) * CELDA_W, (k // COLS) * CELDA_H, (k % COLS + 1) * CELDA_W,
                     (k // COLS + 1) * CELDA_H))
        x, y = 10 + (k % COLS) * (CELDA_W + 120), 10 + (k // COLS) * (CELDA_H + 34)
        lam.paste(c, (x, y), c)
        chico = c.resize((40, 20), Image.NEAREST).resize((80, 40), Image.NEAREST)
        lam.paste(chico, (x + CELDA_W + 20, y + 40), chico)
        d.text((x, y + CELDA_H + 6), '%d %s' % (k, nombre), fill=(220, 220, 220), font=f)
    return lam


if __name__ == '__main__':
    at = atlas()
    ruta = os.path.join(AQUI, 'mal_emblemas.png')
    at.save(ruta)
    lamina(at).save(os.path.join(AQUI, 'mal_emblemas_lamina.png'))
    print('%s: %d x %d, %d x %d celdas de %d x %d' % (ruta, at.size[0], at.size[1], COLS, FILAS, CELDA_W, CELDA_H))
