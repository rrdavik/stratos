"""
La lamina de la especie del mal (fase 39) dibujada con el motor y los shaders de
verdad, fuera de TouchDesigner: el shader de la piel (los edificios del mal, con la
fila 6 de la paleta y sus fachadas de neon) y el de los emblemas (mat_emblema, con
el atlas sprites/mal_emblemas.png), compilados con moderngl.

    xvfb-run -a python3 pruebas/lamina_mal.py [salida.png]

Filas: el brote (las tres vallas), negocio, ocio y encierro (etapas 2 a 5), la
obra (cartel, estructura, a oscuras, encendida), el rescate (el neon se apaga, la
valla cae), un cluster de diez celdas con su coloso y la prueba a distancia (cada
tipo a unos 20 px de alto, ampliado x 4 sin suavizar, junto a la ciudad y la
industria). Luz plana de sala, de noche: el neon se lee.

Necesita moderngl (pip install moderngl) y una pantalla (Xvfb vale).
"""

import ast
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import glsl_piel as gp  # noqa: E402
import vista_previa as vp  # noqa: E402

FONDO = (0.07, 0.07, 0.085)


def shaders_emblema():
    arbol = ast.parse(open(os.path.join(REPO, 'estratos_comun.py'), encoding='utf-8').read())
    out = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 \
                and getattr(nodo.targets[0], 'id', '') in ('EMBLEMA_VERTEX', 'EMBLEMA_PIXEL'):
            out[nodo.targets[0].id] = ast.literal_eval(nodo.value)
    return out['EMBLEMA_VERTEX'], out['EMBLEMA_PIXEL']


class Pintor(object):
    """Los dos programas (piel y emblemas), el atlas y una esfera de suelo."""

    def __init__(self, ctx, m):
        self.ctx, self.m = ctx, m
        self.piel = gp.compilar(ctx)
        v, p = shaders_emblema()
        self.emb = ctx.program(vertex_shader=gp.TD_VERTEX + v, fragment_shader=gp.TD_PIXEL + p)
        im = Image.open(os.path.join(REPO, 'sprites', 'mal_emblemas.png')).convert('RGBA')
        im = im.transpose(Image.FLIP_TOP_BOTTOM)          # como TouchDesigner: la fila 0 de la imagen, arriba
        self.atlas = ctx.texture(im.size, 4, im.tobytes())
        self.atlas.filter = (ctx.NEAREST if hasattr(ctx, 'NEAREST') else 0x2600,) * 2
        self.esf = gp.esfera(48, 96)
        quad = []
        for a, b, c in (((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5)), ((-0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))):
            for x, y in (a, b, c):
                quad.append([x, y, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        self.quad = np.array(quad, dtype='f4')
        self.mallas = {}

    def _camara(self, prog, cam, foco, fov, aspecto, arriba=(0.0, 1.0, 0.0)):
        cam, foco = np.array(cam, float), np.array(foco, float)
        f = foco - cam
        f /= np.linalg.norm(f)
        r = np.cross(f, np.array(arriba, float))
        r /= np.linalg.norm(r)
        u = np.cross(r, f)
        V = np.identity(4)
        V[0, :3], V[1, :3], V[2, :3] = r, u, -f
        V[:3, 3] = -V[:3, :3] @ cam
        near, far = 0.2, 200.0
        k = 1.0 / math.tan(math.radians(fov) / 2)
        Pm = np.zeros((4, 4))
        Pm[0, 0], Pm[1, 1] = k / aspecto, k
        Pm[2, 2], Pm[2, 3] = (far + near) / (near - far), 2 * far * near / (near - far)
        Pm[3, 2] = -1.0
        prog['uViewProj'].write((Pm @ V).T.astype('f4').tobytes())
        Ci = np.identity(4)
        Ci[:3, 0], Ci[:3, 1], Ci[:3, 2], Ci[:3, 3] = r, u, -f, cam
        prog['uTDMats[0].camInverse'].write(Ci.T.astype('f4').tobytes())
        for k in ('uTDMats[0].worldInverse', 'uTDMats[0].world'):
            if k in prog:
                prog[k].write(np.identity(4).astype('f4').tobytes())

    def _dibujar_filas(self, prog, tri, filas):
        if not filas:
            return
        ctx = self.ctx
        vbo = ctx.buffer(tri.tobytes())
        datos = np.array([list(f[:12]) + [f[12] if len(f) > 12 else 1.0] for f in filas], dtype='f4')
        ibo = ctx.buffer(datos.tobytes())
        cd = ctx.buffer(np.ones((len(tri), 4), dtype='f4').tobytes())
        usa = [x for x in ('P', 'N', 'uv0') if x in prog]          # los que el shader no usa, se saltan
        fmt = ' '.join('3f' if x in usa else '12x' for x in ('P', 'N', 'uv0'))
        vao = ctx.vertex_array(prog, [(vbo, fmt) + tuple(usa), (cd, '4f', 'Cd'),
                                      (ibo, '3f 3f 3f 4f/i', 'iT', 'iR', 'iS', 'iC')])
        vao.render(instances=len(filas))

    def foto(self, c, W, now, cam, foco, ancho=420, alto=420, fov=40.0, suelo=True, arriba=None):
        arriba = arriba if arriba is not None else tuple(self.m._norm(foco))
        m, ctx = self.m, self.ctx
        inst = m.build_instances(W, c, now)
        fbo = ctx.simple_framebuffer((ancho, alto))
        fbo.use()
        fbo.clear(FONDO[0], FONDO[1], FONDO[2], 1.0, depth=1.0)
        ctx.enable(ctx.DEPTH_TEST)
        prog = self.piel
        self._camara(prog, cam, foco, fov, ancho / float(alto), arriba)
        uni = m.uniformes_piel(W, c, now)
        for k, v in uni.items():
            if k in prog and k != 'uTerreno':
                prog[k].value = tuple(float(x) for x in v)
        if 'uTerreno' in prog:
            prog['uTerreno'].value = (0.0, 1.0, 0.0, 1.0)
        R = m.top_radius(W, c)
        luces = dict(uLuz0=(0.0, R * 2 + 14, 4.0, 0), uLuz0Col=(0.55, 0.58, 0.68, 0),
                     uLuz1=(14.0, -10.0, 18.0, 0), uLuz1Col=(0.10, 0.12, 0.18, 0),
                     uLuz2=(0, 0, 0, 0), uLuz2Col=(0, 0, 0, 0), uAmbiente=(0.10, 0.10, 0.12, 0),
                     uVentanas=(0.0, 0, 0, 0))
        for k, v in luces.items():
            if k in prog:
                prog[k].value = v
        if suelo:                                   # el suelo: una esfera oscura en el radio de las celdas
            r0 = m.base_radius(W, c, 40)
            prog['uFamilia'].value = (0.0, 0, 0, 0)
            self._dibujar_filas(prog, self.esf, [[0, 0, 0, 0, 0, 0, r0, r0, r0, 0.10, 0.10, 0.11, 0.9]])
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
        img = np.frombuffer(fbo.read(components=3), dtype='u1').reshape(alto, ancho, 3)[::-1]
        return Image.fromarray(img.copy()), inst


# --- los mundos ----------------------------------------------------------------------

def mundo(m, nivel=39, tema=1):
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=nivel, tema=tema, modo_juego=1)
    W = m.new_world()
    W['paso'] = 0.125
    m.juego_al_dia(W, c, 1.0)
    return c, W


def poner_mal(m, c, W, i, occ, rama=None, now=1.0, hecho=True, seq=None):
    m.brote_mal(W, c, i, now)
    W['occ'][i] = occ
    if seq is not None:
        W['lat_s'][i] = seq
    E = m.mal_estado(W)
    e = m.etapa_mal(c, occ)
    if rama and e > 1:
        E['rama'][i] = rama
    E['obra'][i] = (e, -1e9 if hecho else now)


def encuadre(m, W, c, i, H, lejos=1.0):
    n = m.normal_i(i)
    p0 = m._mul(n, m.base_radius(W, c, i))
    e, t = m.tangents(n)
    d = m._norm(m._add(m._mul(e, 0.55), t, 0.85))
    foco = m._add(p0, n, 0.45 * H + 0.6)
    cam = m._add(m._add(p0, n, 2.4 + 0.7 * H), d, (5.2 + 1.0 * H) * lejos)
    return cam, foco


def celda_con_valla(m, valla, desde=34):
    for i in range(desde, m.N):
        if m.VALLAS_MAL[int(m._hash01(i, 389) * 3) % 3] == valla:
            return i
    return desde


def retrato(P, m, occ, rama=None, i=40, ajuste=None, lejos=1.0, ancho=300, alto=300, now=1.0):
    c, W = mundo(m)
    poner_mal(m, c, W, i, occ, rama)
    if ajuste:
        ajuste(c, W, i)
    inf = m.info_mal(W, c, i)
    cam, foco = encuadre(m, W, c, i, inf['H'] * inf['cima'], lejos)
    img, _ = P.foto(c, W, now, cam, foco, ancho, alto)
    return img, inf


# --- la lamina -------------------------------------------------------------------------

def fuente(px, negrita=False):
    for f in (('DejaVuSans-Bold.ttf' if negrita else 'DejaVuSans.ttf'),):
        ruta = os.path.join('/usr/share/fonts/truetype/dejavu', f)
        if os.path.exists(ruta):
            return ImageFont.truetype(ruta, px)
    return ImageFont.load_default()


def main():
    import moderngl
    salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'lamina_mal.png')
    ctx = moderngl.create_standalone_context(require=430)
    m = vp.cargar_motor()
    P = Pintor(ctx, m)
    print('OK     los shaders de la piel y de los emblemas compilan (%s)' % ctx.info['GL_RENDERER'])
    filas = []          # (titulo, [(imagen, rotulo, subrotulo)])
    # el brote
    br = []
    for v, sub in (('vallaobra', 'paneles, pies de hormigon, prohibido'),
                   ('vallatorsion', 'postes, alambre de espino, privado'),
                   ('vallacartel', 'proximamente: anuncia lo que viene')):
        img, inf = retrato(P, m, 1, i=celda_con_valla(m, v))
        br.append((img, '1 · %s' % v, sub))
    filas.append(('BROTE (OCUPACION 1) · LA VALLA: CERCAR ES EL PRIMER GESTO', br))
    rot = {2: '2-3', 3: '4-5', 4: '6-7', 5: '8+'}
    for rama, titulo in (('negocio', 'NEGOCIO (SEQ1) · DE LA TIENDA A LA GRAN SUPERFICIE'),
                         ('ocio', 'OCIO (SEQ2) · DEL BAR AL RESORT DE SUPERLUJO'),
                         ('encierro', 'ENCIERRO (RODEADA POR EL MAL) · DEL RECINTO AL CAMPO')):
        fila = []
        for e in (2, 3, 4, 5):
            occ = m.occ_inicio(dict(m.DEFAULT_CFG), 'planificada', e)
            img, inf = retrato(P, m, occ, rama)
            fila.append((img, '%s · %s' % (rot[e], inf['tipo']), 'emblema: %s' % inf['emblema']))
        filas.append((titulo, fila))
    # la obra
    ob = []
    for k, txt in enumerate(('cartel sobre la valla', 'estructura y grua', 'terminado, a oscuras',
                             'puesta en marcha: se enciende')):
        def aj(c, W, i, k=k):
            E = m.mal_estado(W)
            dur = c['pasos_obra_mal'] * W['paso']
            E['obra'][i] = (4, 1.0 - (k + 0.5) * dur if k < 3 else 1.0 - 5 * dur)
        img, inf = retrato(P, m, 6, 'ocio', ajuste=aj)
        ob.append((img, 'obra %d' % k, txt))
    # el rescate
    def aj_r(c, W, i):
        W['juego']['rescates'][i] = 1.0 - 0.6 * c['t_aliados']
    img, _ = retrato(P, m, 4, 'negocio', ajuste=aj_r)
    ob.append((img, 'rescate 60 %', 'el neon parpadea y se apaga'))
    c, W = mundo(m)
    i = 40
    poner_mal(m, c, W, i, 3, 'negocio')
    m.mal_tick(W, c, 1.0)
    W['sp'][i] = W['own'][i] = m.GEO                # rescatada: la valla cae
    m.mal_tick(W, c, 1.0)
    W['occ'][i] = 0                                 # (sin la celda del publico, para ver la valla)
    cam, foco = encuadre(m, W, c, i, 0.3)
    img, _ = P.foto(c, W, 1.0 + 0.55 * m.T_CAIDA_MAL, cam, foco, 300, 300)
    ob.append((img, 'rescatada', 'cae la valla'))
    filas.append(('OBRA · TERMINADA = SE ENCIENDE   ·   RESCATE · 3 ALIADOS, 3 S', ob))
    # el cluster
    c, W = mundo(m)
    print('       ' + m.sim_mal(W, c, 1.0, celda=40))
    now = 30.0
    n = m.normal_i(40)
    e_, t_ = m.tangents(n)
    p0 = m._mul(n, m.base_radius(W, c, 40))
    foco = m._add(p0, n, 1.6)
    cam = m._add(m._add(p0, n, 6.5), m._norm(m._add(m._mul(e_, 0.4), t_, 0.9)), 14.0)
    grande, inst = P.foto(c, W, now, cam, foco, 1240, 560, fov=46.0)
    res = W['juego']['mal'].get('res', {})
    print('       cluster: %s' % m._legend_mal(W, c).strip())
    # la prueba a distancia: cada tipo a ~20 px de alto, x 4
    dist = []
    for rama in ('negocio', 'ocio', 'encierro'):
        for e in (1, 2, 3, 4, 5):
            occ = m.occ_inicio(dict(m.DEFAULT_CFG), 'planificada', e)
            img, _ = retrato(P, m, occ, rama if e > 1 else None, lejos=1.0, ancho=240, alto=240)
            dist.append(img.resize((24, 24), Image.BOX).resize((96, 96), Image.NEAREST))
    comp = []
    for nombre, fn in (('ciudad', gp.escena_ciudad), ('industria', gp.escena_industria)):
        c2, W2, t2, a, b = fn(m)
        for x in (a, b):
            inf = m.info_ciudad(W2, c2, x)
            cam, foco = encuadre(m, W2, c2, x, inf['H'])
            img, _ = P.foto(c2, W2, t2, cam, foco, 240, 240)
            comp.append((nombre, img.resize((24, 24), Image.BOX).resize((96, 96), Image.NEAREST)))
    # componer
    ancho = 1280
    f_t, f_r, f_s = fuente(17, True), fuente(13, True), fuente(11)
    alto = 70 + sum(30 + 300 + 40 for _ in filas) + 30 + 560 + 20 + 30 + 2 * 110 + 40
    lam = Image.new('RGB', (ancho, alto), (18, 18, 22))
    d = ImageDraw.Draw(lam)
    rosa = (255, 70, 150)
    d.text((20, 18), 'Mal · lamina de una especie nueva (fase 39, motor %s)' % m.MOTOR_VERSION.split()[-1],
           font=fuente(24, True), fill=(235, 235, 235))
    d.text((20, 50), 'dibujada con el motor y los shaders de TouchDesigner (moderngl): los edificios con '
           'la piel de la ciudad, fila 6; los emblemas, mat_emblema', font=f_s, fill=(160, 160, 160))
    y = 72
    for titulo, cosas in filas:
        d.text((20, y + 6), titulo, font=f_t, fill=rosa)
        y += 30
        for k, (img, r, s) in enumerate(cosas):
            x = 20 + k * (300 + 10)
            if x + 300 > ancho:
                break
            lam.paste(img, (x, y))
            d.text((x + 4, y + 304), r, font=f_r, fill=(225, 225, 225))
            d.text((x + 4, y + 322), s, font=f_s, fill=(150, 150, 150))
        y += 340
    d.text((20, y + 6), 'FUSION (CLUSTER) · DIEZ CELDAS: DELANTE LO QUE BRILLA, DETRAS LO QUE ENCIERRA, '
           'ENCIMA EL COLOSO', font=f_t, fill=rosa)
    y += 30
    lam.paste(grande.resize((ancho - 40, int(560 * (ancho - 40) / 1240.0))), (20, y))
    y += int(560 * (ancho - 40) / 1240.0) + 20
    d.text((20, y + 6), 'PRUEBA A DISTANCIA · ~24 PX, AMPLIADO X 4 SIN SUAVIZAR · ¿SE DISTINGUE EL MAL DE LA '
           'CIUDAD Y LA INDUSTRIA?', font=f_t, fill=rosa)
    y += 30
    for k, img in enumerate(dist):
        x = 20 + (k % 5) * 100 + (k // 5) * 520
        if k // 5 == 2:
            x = 20 + (k % 5) * 100
            lam.paste(img, (x, y + 110))
        else:
            lam.paste(img, (x, y))
    for k, (nombre, img) in enumerate(comp):
        x = 540 + k * 100
        lam.paste(img, (x, y + 110))
        d.text((x, y + 208), nombre, font=f_s, fill=(160, 160, 160))
    d.text((20, y + 208), 'mal: negocio (arriba izq.), ocio (arriba der.), encierro', font=f_s, fill=(160, 160, 160))
    lam = lam.crop((0, 0, ancho, y + 230))
    lam.save(salida)
    print('OK     %s' % salida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
