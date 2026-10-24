"""
Vista previa del catalogo de la fase 11 sin TouchDesigner: dibuja cada
modelo del motor (sus cajas, prismas, bolas y conos, con luz plana) en una hoja de
contactos PNG.

    python3 pruebas/vista_previa.py [salida.png]
    python3 pruebas/vista_previa.py lamina [salida.png]     # fase 11 v8: los ejemplares y su silueta a 18 px

Tambien sirve de rasterizador para otras pruebas: pintar(tris, ...) y
mallas_de(prims).
"""

import math
import os
import sys
import types

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)


def cargar_motor():
    """El motor como modulo de Python (el nucleo no necesita TouchDesigner)."""
    mod = types.ModuleType('motor')
    with open(os.path.join(REPO, 'estratos_motor.py'), encoding='utf-8') as f:
        exec(compile(f.read(), 'estratos_motor.py', 'exec'), mod.__dict__)
    return mod


CAJA_V = np.array([[x, y, z] for x in (-0.5, 0.5) for y in (-0.5, 0.5) for z in (-0.5, 0.5)])
CAJA_F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]


def _hexa_malla():
    v, f = [], []
    for k in range(6):
        a = math.radians(60 * k)
        v.append([0.5 * math.cos(a), -0.5, 0.5 * math.sin(a)])
        v.append([0.5 * math.cos(a), 0.5, 0.5 * math.sin(a)])
    for k in range(6):
        a0, a1, b0, b1 = 2 * k, 2 * k + 1, 2 * ((k + 1) % 6), 2 * ((k + 1) % 6) + 1
        f.append((a0, b0, b1, a1))
    f.append(tuple(2 * k for k in range(6))[::-1])
    f.append(tuple(2 * k + 1 for k in range(6)))
    return np.array(v), f


HEXA_V, HEXA_F = _hexa_malla()


def _bola_malla(filas=6, cols=10):
    """La bola unidad (Sphere SOP de pocas caras: se lee de lejos)."""
    v, f = [[0.0, -0.5, 0.0]], []
    for r in range(1, filas):
        phi = math.pi * r / filas - math.pi / 2
        for k in range(cols):
            a = 2 * math.pi * k / cols
            v.append([0.5 * math.cos(phi) * math.cos(a), 0.5 * math.sin(phi), 0.5 * math.cos(phi) * math.sin(a)])
    v.append([0.0, 0.5, 0.0])
    top = len(v) - 1
    idx = lambda r, k: 1 + (r - 1) * cols + k % cols
    for k in range(cols):
        f.append((0, idx(1, k + 1), idx(1, k)))
        f.append((top, idx(filas - 1, k), idx(filas - 1, k + 1)))
    for r in range(1, filas - 1):
        for k in range(cols):
            f.append((idx(r, k), idx(r, k + 1), idx(r + 1, k + 1), idx(r + 1, k)))
    return np.array(v), f


def _cono_malla(cols=8):
    """El cono unidad: base de diametro 1 en y = -0,5 y punta en y = 0,5."""
    v = [[0.5 * math.cos(2 * math.pi * k / cols), -0.5, 0.5 * math.sin(2 * math.pi * k / cols)]
         for k in range(cols)] + [[0.0, 0.5, 0.0]]
    f = [(k, cols, (k + 1) % cols) for k in range(cols)] + [tuple(range(cols))[::-1]]
    return np.array(v), f


BOLA_V, BOLA_F = _bola_malla()
CONO_V, CONO_F = _cono_malla()
MALLAS = dict(caja=(CAJA_V, CAJA_F), hexa=(HEXA_V, HEXA_F), bola=(BOLA_V, BOLA_F), cono=(CONO_V, CONO_F))


def mallas_de(m, prims, M=None, T=None, S=None):
    """Triangulos (n, 3, 3) de las piezas de un modelo, opcionalmente con una
    transformacion de instancia (S escala, M giro, T traslado)."""
    tris = []
    for p in prims:
        V, F = MALLAS[p[0]]
        R = np.array(m._rot_xyz(p[7], p[8], p[9]))
        P = (V * np.array(p[4:7])) @ R.T + np.array(p[1:4])
        if S is not None:
            P = P * np.array(S)
        if M is not None:
            P = P @ np.array(M).T
        if T is not None:
            P = P + np.array(T)
        for face in F:
            for k in range(1, len(face) - 1):
                tris.append([P[face[0]], P[face[k]], P[face[k + 1]]])
    return np.array(tris).reshape(-1, 3, 3)


def malla_ejemplar(m, nombre, cfg=None, M=None, T=None, S=None):
    """Fase 11 v8: (triangulos (n, 3, 3), uv de cada triangulo) de un ejemplar de
    la biblioteca, con la transformacion de instancia si se da."""
    P, _, U, F = m.malla_ejemplar(nombre, cfg)
    P = np.array(P, float)
    if S is not None:
        P = P * np.array(S)
    if M is not None:
        P = P @ np.array(M).T
    if T is not None:
        P = P + np.array(T)
    F = np.array(F, int).reshape(-1, 3)
    return P[F], np.array(U, float)[F[:, 0]]


def pintar(img, zbuf, tris, color, cam, foco, escala, centro, luz=(0.5, 0.8, 0.4)):
    """Rasteriza triangulos con luz plana en img (H, W, 3) y zbuf."""
    H, W = zbuf.shape
    cam = np.array(cam, float)
    fwd = np.array(foco, float) - cam
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 1, 0])
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    luz = np.array(luz) / np.linalg.norm(luz)
    color = np.array(color, float)
    for t in tris:
        n = np.cross(t[1] - t[0], t[2] - t[0])
        ln = np.linalg.norm(n)
        if ln < 1e-12:
            continue
        n /= ln
        rel = t - cam
        z = rel @ fwd
        if np.any(z <= 0.05):
            continue
        x = (rel @ right) / z * escala + centro[0]
        y = -(rel @ up) / z * escala + centro[1]
        if np.dot(n, -fwd) < 0:                   # cara de espaldas
            n = -n
        shade = 0.30 + 0.70 * max(0.0, float(np.dot(n, luz)))
        x0, x1 = int(max(0, np.floor(x.min()))), int(min(W - 1, np.ceil(x.max())))
        y0, y1 = int(max(0, np.floor(y.min()))), int(min(H - 1, np.ceil(y.max())))
        if x0 > x1 or y0 > y1:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        d = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
        if abs(d) < 1e-9:
            continue
        a = ((y[1] - y[2]) * (xs - x[2]) + (x[2] - x[1]) * (ys - y[2])) / d
        b = ((y[2] - y[0]) * (xs - x[2]) + (x[0] - x[2]) * (ys - y[2])) / d
        c = 1 - a - b
        dentro = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6)
        zz = a * z[0] + b * z[1] + c * z[2]
        sub = zbuf[y0:y1 + 1, x0:x1 + 1]
        ok = dentro & (zz < sub)
        sub[ok] = zz[ok]
        img[y0:y1 + 1, x0:x1 + 1][ok] = np.clip(color * shade, 0, 1)


def hoja(m, nombres, salida, lado=200, cols=8):
    filas = (len(nombres) + cols - 1) // cols
    lienzo = Image.new('RGB', (cols * lado, filas * (lado + 16)), (24, 24, 28))
    dib = ImageDraw.Draw(lienzo)
    for k, nm in enumerate(nombres):
        img = np.zeros((lado, lado, 3)) + np.array([0.12, 0.12, 0.14])
        zb = np.full((lado, lado), np.inf)
        prims = m.MODELOS[nm]
        # suelo de referencia: la huella unidad
        suelo = mallas_de(m, [('caja', 0, -0.01, 0, 1.0, 0.02, 1.0, 0, 0, 0)])
        pintar(img, zb, suelo, (0.25, 0.25, 0.28), (1.6, 1.25, 2.2), (0, 0.45, 0), lado * 0.9,
               (lado / 2, lado / 2))
        col = (0.55, 0.75, 0.45) if nm.startswith('veg') else (0.62, 0.62, 0.70) if nm.startswith('rel') \
            else (0.85, 0.65, 0.45) if nm.startswith('inf') else (0.72, 0.76, 0.82) if nm.startswith('pla') \
            else (0.90, 0.80, 0.35)
        pintar(img, zb, mallas_de(m, prims), col, (1.6, 1.25, 2.2), (0, 0.45, 0), lado * 0.9,
               (lado / 2, lado / 2))
        x, y = (k % cols) * lado, (k // cols) * (lado + 16)
        lienzo.paste(Image.fromarray((img * 255).astype('uint8')), (x, y))
        dib.text((x + 4, y + lado + 2), '%s (%d)' % (nm, len(prims)), fill=(220, 220, 220))
    lienzo.save(salida)
    return salida


UNIDAD = [('caja', 0.0, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)]     # la caja de las fases 3-10


def escena(m, inst, salida, cam, foco, lado=900, escala=None, nucleo=None, cfg=None):
    """Dibuja las instancias de build_instances (modelos, cajas y particulas)
    vistas desde cam hacia foco."""
    img = np.zeros((lado, lado, 3)) + np.array([0.08, 0.08, 0.10])
    zb = np.full((lado, lado), np.inf)
    escala = escala or lado * 1.2
    luz = np.array(cam, float) - np.array(foco, float) + np.array([0.0, 4.0, 0.0])   # luz de la camara
    if nucleo:
        r, k = nucleo, 24
        tris = []
        for a in range(k):
            for b in range(k):
                def pt(i, j):
                    th, ph = 2 * math.pi * i / k, math.pi * j / k - math.pi / 2
                    return [r * math.cos(ph) * math.cos(th), r * math.sin(ph), r * math.cos(ph) * math.sin(th)]
                p00, p10, p01, p11 = pt(a, b), pt(a + 1, b), pt(a, b + 1), pt(a + 1, b + 1)
                tris += [[p00, p10, p11], [p00, p11, p01]]
        pintar(img, zb, np.array(tris), (0.12, 0.12, 0.13), cam, foco, escala, (lado / 2, lado / 2), luz=luz)
    for clave, filas in inst.items():
        if not filas or clave in ('luz_conchas',):
            continue
        prims = UNIDAD
        nm = None
        if clave.startswith('mod_'):
            nm = clave[4:]
            for suf in ('_pul', '_por'):
                if nm.endswith(suf):
                    nm = nm[:-len(suf)]
            prims = None if m.es_ejemplar(nm) else m.MODELOS[nm]
        for f in filas:
            if f[1] < -9000:
                continue
            M = m._rot_xyz(f[3], f[4], f[5])
            if prims is None:                   # fase 11 v8: un ejemplar, corteza y hojas
                tris, uv = malla_ejemplar(m, nm, cfg, M, f[0:3], f[6:9])
                hoja = uv[:, 0] >= 1.5
                pintar(img, zb, tris[~hoja], (0.20, 0.14, 0.09), cam, foco, escala, (lado / 2, lado / 2), luz=luz)
                pintar(img, zb, tris[hoja], f[9:12], cam, foco, escala, (lado / 2, lado / 2), luz=luz)
                continue
            tris = mallas_de(m, prims, M, f[0:3], f[6:9])
            pintar(img, zb, tris, f[9:12], cam, foco, escala, (lado / 2, lado / 2), luz=luz)
    Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')).save(salida)
    return salida


def lamina(m, salida, lado=170, px=18):
    """Fase 11 v8: la lamina de la naturaleza. Fila de arriba, los 13 ejemplares
    de la biblioteca (variante 0, derivacion completa) de cerca; de abajo, su
    silueta a 'px' pixeles de alto (la prueba a distancia), con la bola y el
    cono de las versiones anteriores para comparar."""
    c = dict(m.DEFAULT_CFG)
    nombres = [m.nombre_ejemplar(mo, 0, m.etapas_de(mo)[-1]) for mo in m.PLANTAS]
    cols = len(nombres) + 2
    lienzo = Image.new('RGB', (cols * lado, 2 * lado + 32), (236, 236, 230))
    dib = ImageDraw.Draw(lienzo)
    for k, nm in enumerate(nombres):
        img = np.zeros((lado, lado, 3)) + np.array([0.93, 0.93, 0.90])
        zb = np.full((lado, lado), np.inf)
        tris, uv = malla_ejemplar(m, nm, c)
        hojas = uv[:, 0] >= 1.5
        pintar(img, zb, tris[~hojas], (0.30, 0.22, 0.14), (0, 0.5, 3.4), (0, 0.5, 0), lado * 1.25,
               (lado / 2, lado / 2))
        pintar(img, zb, tris[hojas], (0.22, 0.48, 0.20), (0, 0.5, 3.4), (0, 0.5, 0), lado * 1.25,
               (lado / 2, lado / 2))
        lienzo.paste(Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')), (k * lado, 0))
        dib.text((k * lado + 4, lado + 2), nm[4:], fill=(40, 40, 40))
    sil = [m.silueta(c, nm, px) for nm in nombres]
    r = px // 2
    sil.append(set((x, y) for x in range(-r, r + 1) for y in range(px) if x * x + (y - r + 0.5) ** 2 <= r * r))
    sil.append(set((x, y) for y in range(px) for x in range(-r, r + 1) if abs(x) <= r * (1 - y / (px - 1.0))))
    for k, s in enumerate(sil):
        chico = Image.new('RGB', (2 * px, px), (236, 236, 230))
        for x, y in s:
            if 0 <= x + px < 2 * px and 0 <= y < px:
                chico.putpixel((x + px, px - 1 - y), (34, 70, 32))
        grande = chico.resize((lado, lado // 2), Image.NEAREST)
        lienzo.paste(grande, (k * lado, lado + 16 + lado // 4))
    dib.text((len(nombres) * lado + 4, lado + 2), 'bola (v5)', fill=(40, 40, 40))
    dib.text(((len(nombres) + 1) * lado + 4, lado + 2), 'cono (v5)', fill=(40, 40, 40))
    lienzo.save(salida)
    return salida


if __name__ == '__main__':
    m = cargar_motor()
    if len(sys.argv) > 1 and sys.argv[1] == 'lamina':
        print(lamina(m, sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQUI, 'lamina_naturaleza.png')))
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'catalogo.png')
        print(hoja(m, sorted(m.MODELOS), out))
