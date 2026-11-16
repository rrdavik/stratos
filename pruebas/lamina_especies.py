"""
La lamina de las especies construidas sobre el oceano (motor v120) dibujada con el
motor y los shaders de verdad, fuera de TouchDesigner: la malla del terreno (el mar
y los muelles de la ciudad y la industria, mat_piel_tierra), los edificios (el
shader de la ciudad), las conchas, el tejido, los emblemas del mal y la luz local
(aditiva: los focos de las discotecas y el neon de las construcciones finales).

    xvfb-run -a python3 pruebas/lamina_especies.py [salida.png]

Filas: la ciudad (tiendas, campos de futbol, mercados, la escalera de siempre)
cerca y lejos; la industria (pozos petroliferos, uno convertido en refineria al
construir encima; termicas y refinerias) cerca y lejos; el mal de noche (la
discoteca con sus focos, el resort con los yates en el mar, el neon de las
construcciones finales y el demonio).

Necesita moderngl (pip install moderngl) y una pantalla (Xvfb vale).
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import glsl_piel as gp  # noqa: E402
import lamina_mal as lm  # noqa: E402
import vista_previa as vp  # noqa: E402

ADITIVO_V = """
out vec3 vCol;
void main()
{
    gl_Position = TDWorldToProj(TDDeform(P));
    vCol = iC.rgb * Cd.rgb;
}
"""
ADITIVO_P = """
in vec3 vCol;
layout(location = 0) out vec4 oFragColor[TD_NUM_COLOR_BUFFERS];
void main()
{
    oFragColor[0] = vec4(vCol, 1.0);
}
"""


class PintorTerreno(lm.Pintor):
    """El pintor de la lamina del mal con la malla del terreno y la luz local."""

    def __init__(self, ctx, m):
        lm.Pintor.__init__(self, ctx, m)
        self.adi = ctx.program(vertex_shader=gp.TD_VERTEX + ADITIVO_V, fragment_shader=gp.TD_PIXEL + ADITIVO_P)
        self.terreno_malla = gp.esfera(512, 1024)
        self.caja = gp.malla(m, [('caja', 0.0, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)])

    def foto_mar(self, c, W, now, cam, foco, ancho=480, alto=420, fov=40.0, noche=False, arriba=None):
        m, ctx = self.m, self.ctx
        arriba = arriba if arriba is not None else tuple(m._norm(foco))
        inst = m.build_instances(W, c, now)
        m.terreno(W, c)
        fbo = ctx.simple_framebuffer((ancho, alto))
        fbo.use()
        fondo = (0.03, 0.03, 0.05) if noche else lm.FONDO
        fbo.clear(fondo[0], fondo[1], fondo[2], 1.0, depth=1.0)
        ctx.enable(ctx.DEPTH_TEST)
        prog = self.piel
        self._camara(prog, cam, foco, fov, ancho / float(alto), arriba)
        uni = m.uniformes_piel(W, c, now)
        for k, v in uni.items():
            if k in prog and k != 'uTerreno':
                prog[k].value = tuple(float(x) for x in v)
        R = m.top_radius(W, c)
        k = 0.45 if noche else 1.0
        luces = dict(uLuz0=(0.0, R * 2 + 14, 4.0, 0), uLuz0Col=(0.82 * k, 0.90 * k, 1.0 * k, 0),
                     uLuz1=(14.0, -10.0, 18.0, 0), uLuz1Col=(0.10, 0.14, 0.20, 0),
                     uLuz2=(0, 0, 0, 0), uLuz2Col=(0, 0, 0, 0), uAmbiente=(0.16 * k, 0.16 * k, 0.18 * k, 0),
                     uVentanas=(1.0 if c['nivel'] >= 17 else 0.0, 0, 0, 0))
        for nm, v in luces.items():
            if nm in prog:
                prog[nm].value = v
        alt, ram, _, cul = gp.texturas(ctx, m, c)
        alt.use(0)
        ram.use(1)
        cul.use(2)
        for nm, u in (('sAlturas', 0), ('sRampa', 1), ('sCultivo', 2)):
            if nm in prog:
                prog[nm].value = u
        prog['uTerreno'].value = (1.0, float(uni['uTerreno'][1]), float(uni['uTerreno'][2]), 1.0)
        prog['uFamilia'].value = (3.0, 0, 0, 0)
        self._dibujar_filas(prog, self.terreno_malla, [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]])
        prog['uTerreno'].value = (0.0, 1.0, 0.0, 1.0)
        for g, fam in (('estratos', 8.0), ('tejido', 0.0)):
            filas = inst.get(g) or []
            if filas:
                prog['uFamilia'].value = (fam, 0, 0, 0)
                self._dibujar_filas(prog, self.caja, filas)
        for g, mo, mat in m.geometrias_piel(c):
            filas = inst.get(g) or []
            if not filas:
                continue
            prog['uFamilia'].value = (float(m.FAMILIAS.index(m.familia_de(mo))) if mo[:3] != 'ciu' else 0.0,
                                      0, 0, 0)
            if mo not in self.mallas:
                es_malla = m.es_ejemplar(mo) or m.es_edificio(mo)
                self.mallas[mo] = gp.malla(m, mo if es_malla else m.MODELOS[mo], c)
            self._dibujar_filas(prog, self.mallas[mo], filas)
        filas = inst.get('emblemas_mal') or []
        if filas:
            e = self.emb
            self._camara(e, cam, foco, fov, ancho / float(alto), arriba)
            self.atlas.use(0)
            e['sAtlas'].value = 0
            e['uEmblema'].value = (float(now), 0.0, float(m.ATLAS_MAL[0]), float(m.ATLAS_MAL[1]))
            e['uEmblemaInc'].value = (30.0, 1.0, 0.0, 0.0)
            self._dibujar_filas(e, self.quad, filas)
        filas = inst.get('luz_local') or []
        if filas:                                   # la luz local: aditiva, sin escribir profundidad
            a = self.adi
            a['uViewProj'].write(self.piel['uViewProj'].read())
            ctx.enable(ctx.BLEND)
            ctx.blend_func = (ctx.ONE, ctx.ONE)
            ctx.depth_mask = False
            self._dibujar_filas(a, self.caja, filas)
            ctx.depth_mask = True
            ctx.disable(ctx.BLEND)
        img = np.frombuffer(fbo.read(components=3), dtype='u1').reshape(alto, ancho, 3)[::-1]
        return Image.fromarray(img.copy()), inst


def vista(m, W, c, a, b, dist, lado=0.18):
    mid = m._norm(m._add(m.normal_i(a), m.normal_i(b)))
    R = m.top_radius(W, c)
    cam = m._add(m._mul(mid, R * dist), m._mul(m.tangents(mid)[1], R * dist * lado))
    return cam, m._mul(mid, R * 0.85)


def con_rotulo(img, texto):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, img.size[0], 18), fill=(0, 0, 0))
    d.text((6, 3), texto, fill=(235, 235, 235))
    return img


def poner_diseno(m, c, W, x, own, occ, diseno):
    """La celda x con ese dueno y ocupacion, y la velocidad fundadora que hace que su
    semilla elija ese diseno (la misma historia, el mismo edificio)."""
    W['occ'][x], W['own'][x], W['sp'][x] = occ, own, own
    W['h'][x] = W['vh'][x] = m.height_for(c, occ)
    W['t_nac'][x] = -50.0
    for vel in range(1, 128):
        W['vel'][x] = vel
        if m.diseno_celda(W, c, x)[0] == diseno:
            return True
    print('       AVISO: %s no sale en la celda %d (occ %d)' % (diseno, x, occ))
    return False


def escena_tiendas(m):
    """La ciudad nueva: quiosco, mercadillo, colmado, bajos y el potrero (informal);
    campo de futbol, galeria de tiendas, bloque con bajos, mercado y estadio (planificada)."""
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=17, tema=1, avance=0, oceano=1)
    W = m.new_world()
    W['estacion'] = dict(tinte=[1.0, 1.0, 1.0], ventanas=1)
    a, b = m.RINGS[3], m.RINGS[4]
    oi = lambda e: m.occ_inicio(c, 'informal', e)
    op = lambda e: m.occ_inicio(c, 'planificada', e)
    celdas = []
    for k, (occ, d) in enumerate(((oi(1), 'quiosco'), (oi(1), 'mercadillo'), (oi(2), 'colmado'), (oi(3), 'bajos'),
                                  (oi(4), 'potrero'))):
        poner_diseno(m, c, W, a[2 * k], m.GEO, occ, d)
        celdas.append((a[2 * k], d))
    for k, (occ, d) in enumerate(((op(1), 'campofutbol'), (op(1), 'galeriatiendas'), (op(2), 'bloquebajos'),
                                  (op(3), 'mercado'), (op(4), 'estadio'))):
        poner_diseno(m, c, W, b[2 * k], m.ARQ, occ, d)
        celdas.append((b[2 * k], d))
    m.cerrar_obras(W, c)
    W['paso'] = 0.125
    return c, W, 2.0, a[4], b[4], celdas


def escena_petroleo(m):
    """La industria nueva: la torre petrolifera y, si se construye encima, la refineria
    (separadores, refinerita, craqueo, petroquimica); termicas de gas y de carbon y el
    ciclo combinado."""
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=17, tema=2, avance=0, oceano=1)
    W = m.new_world()
    W['estacion'] = dict(tinte=[1.0, 1.0, 1.0], ventanas=1)
    a, b = m.RINGS[3], m.RINGS[4]
    om = lambda e: m.occ_inicio(c, 'mina', e)
    celdas = []
    for k, (e, d) in enumerate(((1, 'torrepetrolera'), (2, 'separadora'), (3, 'refinerita'), (4, 'craqueo'),
                                (5, 'petroquimica'))):
        poner_diseno(m, c, W, a[2 * k], m.GEO, om(e), d)
        celdas.append((a[2 * k], d))
    oe = lambda e: m.occ_inicio(c, 'energia', e)
    for k, (e, d) in enumerate(((4, 'termicagas'), (4, 'termicacarbon'), (5, 'ciclocombinado'))):
        poner_diseno(m, c, W, b[2 * k], m.ARQ, oe(e), d)
        celdas.append((b[2 * k], d))
    m.cerrar_obras(W, c)
    W['paso'] = 0.125
    W['pulso']['beat'] = 3.3
    return c, W, 2.0, a[4], b[4], celdas


def escena_mal(m):
    """El mal de noche en la ciudad con Oceano: una discoteca, un casino, un resort junto
    al mar (con sus yates), la gran superficie y el campo; un cluster de 7 (la cabeza)."""
    c, W = lm.mundo(m, tema=1)
    c = dict(c, oceano=1)
    anillo = m.RINGS[3]
    fila = [anillo[k] for k in range(2, 9)]
    ramas = ('ocio', 'ocio', 'ocio', 'negocio', 'negocio', 'encierro', 'ocio')
    occs = (5, 7, 9, 9, 6, 9, 4)
    for x, rama, o in zip(fila, ramas, occs):
        lm.poner_mal(m, c, W, x, o, rama)
    celdas = [(x, '%s %d' % (r, o)) for x, r, o in zip(fila, ramas, occs)]
    return c, W, 30.0, fila[1], fila[4], celdas


def retratos(P, m, c, W, now, celdas, info, noche=False, lado=240, lejos=0.8):
    out = []
    for x, nombre in celdas:
        H = info(W, c, x)
        cam, foco = lm.encuadre(m, W, c, x, H, lejos)
        img, _ = P.foto_mar(c, W, now, cam, foco, ancho=lado, alto=lado, noche=noche)
        out.append(con_rotulo(img, nombre))
    return out


def hoja_de(filas):
    ancho = max(sum(i.size[0] for i in f) for f in filas)
    alto = sum(f[0].size[1] for f in filas)
    hoja = Image.new('RGB', (ancho, alto), (10, 10, 12))
    y = 0
    for f in filas:
        x = 0
        for img in f:
            hoja.paste(img, (x, y))
            x += img.size[0]
        y += f[0].size[1]
    return hoja


def main():
    import moderngl
    salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'lamina_especies.png')
    ctx = moderngl.create_standalone_context(require=430)
    m = vp.cargar_motor()
    P = PintorTerreno(ctx, m)
    filas = []
    alto_ciu = lambda W, c, x: m.info_ciudad(W, c, x)['H']
    for nombre, hacer in (('ciudad', escena_tiendas), ('industria', escena_petroleo)):
        c, W, now, a, b, celdas = hacer(m)
        m.build_instances(W, c, now)
        fotos = retratos(P, m, c, W, now, celdas, alto_ciu)
        cam, foco = vista(m, W, c, a, b, 3.0, 0.35)
        img, inst = P.foto_mar(c, W, now, cam, foco, ancho=240, alto=240)
        fotos.append(con_rotulo(img, '%s con Oceano' % nombre))
        filas += [fotos[:5], fotos[5:]]
        pz = W['piel'].get('ciudad', {})
        print('       %s: %d edificios de %d tipos, islas %s' % (nombre, pz.get('edificios', 0), pz.get('tipos', 0),
                                                              m.rasgos_terreno(W, c)[1].get('islas')))
    c, W, now, a, b, celdas = escena_mal(m)
    m.build_instances(W, c, now)
    alto_mal = lambda W, c, x: m.info_mal(W, c, x)['H'] * m.info_mal(W, c, x)['cima']
    fotos = retratos(P, m, c, W, now, celdas[:5], alto_mal, noche=True, lejos=1.1)
    cam, foco = vista(m, W, c, a, b, 2.6, 0.45)
    img, inst = P.foto_mar(c, W, now, cam, foco, ancho=240, alto=240, noche=True)
    fotos.append(con_rotulo(img, 'el mal de noche'))
    filas.append(fotos)
    yates = inst.get(m.geometria_de('ciu_yate')) or []
    fotos = []
    for f in yates[:3]:                         # los yates, en el mar junto al resort y el casino
        p0 = tuple(f[:3])
        n = m._norm(p0)
        e, t = m.tangents(n)
        foco = m._add(p0, n, 0.05)
        cam = m._add(m._add(p0, n, 0.9), m._norm(m._add(e, t, 0.6)), 1.6)
        img, _ = P.foto_mar(c, W, now, cam, foco, ancho=240, alto=240, noche=True)
        fotos.append(con_rotulo(img, 'yate del mal'))
    if fotos:
        filas.append(fotos)
    res = W['juego']['mal'].get('res', {})
    print('       mal: %s; luz local %d filas' % (dict((k, v) for k, v in res.items() if k != 'demonios'),
                                                   len(inst.get('luz_local') or [])))
    hoja_de(filas).save(salida)
    print('       %s' % salida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
