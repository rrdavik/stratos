"""
Vista previa de la camara rasante (motor v92) sin TouchDesigner: un mundo de
prueba visto con la camara de superficie de siempre y con la rasante, una
imagen sobre la otra, con el rasterizador de vista_previa (luz plana, sin
materiales, sin bruma: sirve para juzgar el encuadre, no el acabado).

Limite: el rasterizador descarta los triangulos que cruzan el plano de la
camara. Mirando al cenit con mucho angular (lo de la v13) se pierde casi todo
lo que entra por los bordes, asi que la imagen sale mas vacia de lo que es:
para esa vista, mirar en TouchDesigner. Las dos PNG guardadas son de la v12
(ojos a 0,35, mirada 8, angular 90).

    python3 pruebas/vista_rasante.py [escena] [salida.png] [segundos]

escena: naturaleza, ciudad o industria (por defecto, ciudad). segundos: lo que
dura la sesion que puebla el mundo (por defecto, 90).
"""

import math
import os
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import vista_previa as vp  # noqa: E402
import sesion_escena as se  # noqa: E402

m = se.m
ANCHO, ALTO = 960, 540


def poblar(nombre, segundos, fps=30.0, tempo=120.0):
    """Un mundo con 'segundos' de la sesion de prueba de la escena."""
    c = se.cfg_escena(nombre)
    c['superficie'] = 1                 # de cerca: todo con detalle
    W = m.new_world()
    m.ensure(W)
    W['tema'] = c['tema']
    paso = m.step_dur(c, tempo)
    pend, k_paso, t = [], -1, 0.0
    for f in range(int(segundos * fps)):
        t = f / fps
        p = int(t / paso)
        if p != k_paso:
            k_paso = p
            for s, n in pend:
                m.note_off(W, c, s, n, t, tempo)
            n1 = se.PATRONES['ABC'[(p // 64) % 3]][p % 16]
            m.note_on(W, c, m.GEO, n1, 80 + (p * 7) % 40, t, tempo)
            pend = [(m.GEO, n1)]
            if p % 3 == 0:
                n2 = [60, 67, 65, 63, 70][(p // 3) % 5]
                m.note_on(W, c, m.ARQ, n2, 70, t, tempo)
                pend.append((m.ARQ, n2))
        m.tick(W, c, t, tempo, True)
    W['vh'] = list(W['h'])
    return W, c, t


def vista(inst, c, R, pos, de, ar, fov):
    """La escena desde pos, mirando a 'de' con 'ar' arriba y 'fov' grados en horizontal."""
    de, ar = np.array(m._norm(de)), np.array(ar, float)
    der = np.cross(de, ar)
    der /= np.linalg.norm(der)
    arr = np.cross(der, de)
    Q = np.array([der, arr, -de])       # del mundo a la camara (arriba = +Y, mira por -Z)
    cam = Q @ np.array(pos, float)
    original = vp.pintar

    def girado(img, zb, tris, color, cam_, foco_, escala, centro, luz=(0.5, 0.8, 0.4)):
        return original(img, zb, np.asarray(tris, float) @ Q.T, color, cam, cam + np.array([0.0, 0.0, -1.0]),
                        escala, (ANCHO / 2.0, ALTO / 2.0), luz=Q @ np.array([0.3, 1.0, 0.5]))

    vp.pintar = girado
    es_ej = m.es_ejemplar               # escena() no conoce los edificios: su malla sale como la de un ejemplar
    m.es_ejemplar = lambda n: es_ej(n) or m.es_edificio(n)
    tmp = os.path.join(AQUI, '_vista_rasante_tmp.png')
    try:
        # escena() pinta en un cuadrado: se le da el ancho y se recorta al alto
        vp.escena(m, inst, tmp, cam, cam, lado=ANCHO, escala=(ANCHO / 2.0) / math.tan(math.radians(fov) / 2.0),
                  nucleo=None, cfg=c)
    finally:
        vp.pintar = original
        m.es_ejemplar = es_ej
    im = Image.open(tmp).convert('RGB')
    os.remove(tmp)
    return im


def principal(nombre='ciudad', salida=None, segundos=90.0):
    salida = salida or os.path.join(AQUI, 'vista_rasante_%s.png' % nombre)
    W, c, t = poblar(nombre, segundos)
    inst = m.build_instances(W, c, t, tiles=True)
    # el color de las instancias de la piel no es un color (son codigos para el shader): un gris por modelo.
    # Fuera lo que no es volumen (particulas, luces, diagnostico)
    limpio = {}
    for clave, filas in inst.items():
        if clave.startswith('mod_') and filas and max(filas[0][9:12]) > 1.5:      # edificios: codigos
            g = 0.45 + 0.35 * m._hash01(sum(ord(ch) for ch in clave), 3)
            limpio[clave] = [tuple(f[:9]) + (g, g, g * 1.04) + tuple(f[12:]) for f in filas]
        elif clave.startswith('mod_') or clave in ('estratos', 'tejido'):
            limpio[clave] = filas
    inst = limpio
    R = m.top_radius(W, c)
    # rasante: el paralelo y la longitud con mas formacion a los lados
    lat, _ = m.paralelo_rasante(4)
    lon = max(range(0, 360, 5), key=lambda lo: sum(W['vh'][i] for i in m.suelo_rasante(W, c, lat, lo + 25.0)[1:]))
    g = m.suelo_rasante(W, c, lat, lon)[0]
    pos, de, ar = m.pose_rasante(lat, lon, g + m.RAS_ALTURA, m.RAS_MIRADA)
    # superficie (la de hoy): a 4 de altura sobre el mismo sitio, mirando 25 grados por delante
    az, el = math.radians(lon), math.radians(lat)

    def sph(a, e, r):
        return (r * math.cos(e) * math.cos(a), r * math.sin(e), r * math.cos(e) * math.sin(a))
    s_pos, s_tgt = sph(az, el, R + 4.0), sph(az + math.radians(25.0), el - math.radians(6.0), R)
    s_de = tuple(s_tgt[k] - s_pos[k] for k in range(3))
    a = vista(inst, c, R, s_pos, s_de, (0.0, 1.0, 0.0), 45.0)
    b = vista(inst, c, R, pos, de, ar, m.RAS_FOV)
    hoja = Image.new('RGB', (ANCHO, 2 * ALTO + 6), (255, 255, 255))
    y0 = (ANCHO - ALTO) // 2
    hoja.paste(a.crop((0, y0, ANCHO, y0 + ALTO)), (0, 0))
    hoja.paste(b.crop((0, y0, ANCHO, y0 + ALTO)), (0, ALTO + 6))
    hoja.save(salida)
    print('%s: arriba, superficie (altura 4, fov 45); abajo, rasante (ojos a %.2f, fov %d, mirada %d)' % (salida, m.RAS_ALTURA, m.RAS_FOV, m.RAS_MIRADA))
    print('mundo: %s, %d celdas ocupadas, radio %.2f; rasante en lat %.0f lon %.0f' % (
        nombre, m.occupied(W), R, lat, lon))
    return salida


if __name__ == '__main__':
    a = sys.argv[1:]
    principal(a[0] if a else 'ciudad', a[1] if len(a) > 1 else None, float(a[2]) if len(a) > 2 else 90.0)
