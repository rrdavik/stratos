"""
Comprueba el shader de la piel (fase 12) con un OpenGL de verdad, fuera de
TouchDesigner: compila PIEL_VERTEX y PIEL_PIXEL de estratos_comun.py con
unas funciones que imitan las de TouchDesigner (TDDeform, TDInstanceColor,
uTDMats...) y, si compila, dibuja una escena con las instancias reales del
motor (naturaleza y ciudad, velocidades altas y bajas).

    xvfb-run -a python3 pruebas/glsl_piel.py [salida.png]

Desde la fase 11 v5 dibuja tambien la malla del terreno (la esfera desplazada
por el mapa de alturas del motor, con la rampa de los pisos), los rios y los
lagos, con los focos del tinte de una nota del SEQ1.

Necesita moderngl (pip install moderngl) y una pantalla (Xvfb vale). No
comprueba que TouchDesigner declare sus funciones igual: solo que el
shader es GLSL 4.5 correcto y que hace lo que se espera con esos datos.
"""

import ast
import math
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import vista_previa as vp  # noqa: E402

TD_VERTEX = """#version 450
#define TD_NUM_COLOR_BUFFERS 1
struct TDMatrix { mat4 camInverse; mat4 worldInverse; };
uniform TDMatrix uTDMats[1];
in vec3 P;
in vec3 N;
in vec4 Cd;
in vec3 uv0;
#define uv uvTD
vec3 uvTD[1];
in vec3 iT;
in vec3 iR;
in vec3 iS;
in vec4 iC;
uniform mat4 uViewProj;
mat3 tdRot(vec3 r)
{
    vec3 a = radians(r);
    mat3 rx = mat3(1.0, 0.0, 0.0, 0.0, cos(a.x), sin(a.x), 0.0, -sin(a.x), cos(a.x));
    mat3 ry = mat3(cos(a.y), 0.0, -sin(a.y), 0.0, 1.0, 0.0, sin(a.y), 0.0, cos(a.y));
    mat3 rz = mat3(cos(a.z), sin(a.z), 0.0, -sin(a.z), cos(a.z), 0.0, 0.0, 0.0, 1.0);
    return rz * ry * rx;
}
vec4 TDDeform(vec3 p) { uvTD[0] = uv0; return vec4(tdRot(iR) * (p * iS) + iT, 1.0); }
vec3 TDDeformNorm(vec3 n) { return tdRot(iR) * (n / iS); }
vec4 TDWorldToProj(vec4 w) { return uViewProj * w; }
vec4 TDInstanceColor(vec4 c) { return iC * c; }
int TDInstanceID() { return gl_InstanceID; }
int TDCameraIndex() { return 0; }
void TDWritePickingValues() {}
#line 1
"""

TD_PIXEL = """#version 450
#define TD_NUM_COLOR_BUFFERS 1
struct TDMatrix { mat4 camInverse; mat4 worldInverse; };
uniform TDMatrix uTDMats[1];
void TDCheckDiscard() {}
vec4 TDOutputSwizzle(vec4 c) { return c; }
#line 1
"""


def shaders():
    """(PIEL_VERTEX, PIEL_PIXEL) leidos de estratos_comun.py sin ejecutarlo."""
    arbol = ast.parse(open(os.path.join(REPO, 'estratos_comun.py'), encoding='utf-8').read())
    out = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 \
                and getattr(nodo.targets[0], 'id', '') in ('PIEL_VERTEX', 'PIEL_PIXEL'):
            out[nodo.targets[0].id] = ast.literal_eval(nodo.value)
    return out['PIEL_VERTEX'], out['PIEL_PIXEL']


def compilar(ctx):
    v, p = shaders()
    return ctx.program(vertex_shader=TD_VERTEX + v, fragment_shader=TD_PIXEL + p)


def malla(m, prims, c=None):
    """Triangulos con normal plana: (n, 9) = posicion, normal y uv. prims: las
    piezas de un modelo o, desde la fase 11 v8, el nombre de un ejemplar."""
    if isinstance(prims, str):
        tris, uvs = vp.malla_ejemplar(m, prims, c)
    else:
        tris = vp.mallas_de(m, prims)
        uvs = np.zeros((len(tris), 3))
    out = []
    for t, u in zip(tris, uvs):
        n = np.cross(t[1] - t[0], t[2] - t[0])
        ln = np.linalg.norm(n)
        if ln < 1e-12:
            continue
        n = n / ln
        for q in t:
            out.append(np.concatenate([q, n, u]))
    return np.array(out, dtype='f4')


def mirar(cam, foco, fov=45.0, aspecto=1.0, near=0.5, far=200.0):
    cam, foco = np.array(cam, float), np.array(foco, float)
    f = foco - cam
    f /= np.linalg.norm(f)
    r = np.cross(f, [0.0, 1.0, 0.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    V = np.identity(4)
    V[0, :3], V[1, :3], V[2, :3] = r, u, -f
    V[:3, 3] = -V[:3, :3] @ cam
    t = 1.0 / math.tan(math.radians(fov) / 2)
    Pm = np.zeros((4, 4))
    Pm[0, 0], Pm[1, 1] = t / aspecto, t
    Pm[2, 2], Pm[2, 3] = (far + near) / (near - far), 2 * far * near / (near - far)
    Pm[3, 2] = -1.0
    return Pm @ V


def escena(m):
    """Mundos con una zona de cada especie: naturaleza y ciudad, con
    velocidad alta (pulido) y baja (rugoso)."""
    mundos = []
    for tema, vel in ((0, 120), (0, 12), (1, 120), (1, 12)):
        c = dict(m.DEFAULT_CFG)
        c.update(nivel=12, tema=tema, avance=1)
        W = m.new_world()
        t = 0.0
        paso = m.step_dur(c, 120.0)
        for nota, s in ((64, m.GEO), (40, m.ARQ)):
            i = m.note_cell(nota)
            for _ in range(3):
                for x in [i] + list(m.NEIGH[i]):
                    m.note_on(W, c, s, m.cell_note(x), vel, t, 120.0)
                    m.note_off(W, c, s, m.cell_note(x), t + 0.5 * paso, 120.0)
            for _ in range(12):
                m.note_on(W, c, s, nota, vel, t, 120.0)
        for k in range(90):
            t += 1 / 30.0
            m.tick(W, c, t, 120.0, True)
        mundos.append((c, W, t))
    return mundos


def escena_natural(m):
    """Fase 11 v5: una cordillera de 5 celdas en fila con cumbres, un monte
    boscoso (ocupacion 12) y un bosque de 7 celdas; una nota del SEQ1 encendida."""
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=13, tema=0, avance=1)
    W = m.new_world()
    t = 0.0
    paso = m.step_dur(c, 120.0)
    fila = [m.note_cell(n) for n in (62, 63, 64, 65, 66)]
    for _ in range(4):
        for x in fila:
            for _ in range(4):
                m.note_on(W, c, m.ARQ, m.cell_note(x), 100, t, 120.0)
                m.note_off(W, c, m.ARQ, m.cell_note(x), t + 0.5 * paso, 120.0)
    for x, k in ((fila[1], 40), (fila[3], 24)):
        for _ in range(k):
            m.note_on(W, c, m.ARQ, m.cell_note(x), 100, t, 120.0)
    i = m.note_cell(52)
    for _ in range(3):
        for x in [i] + list(m.NEIGH[i]):
            for _ in range(4):
                m.note_on(W, c, m.GEO, m.cell_note(x), 100, t, 120.0)
                m.note_off(W, c, m.GEO, m.cell_note(x), t + 0.5 * paso, 120.0)
    for _ in range(80):
        m.note_on(W, c, m.GEO, 52, 100, t, 120.0)
    for k in range(120):
        t += 1 / 30.0
        m.tick(W, c, t, 120.0, True)
    # fase 11 v8: arrozal (5 notas del SEQ1 en la cumbre de la cordillera) y
    # meseta-jardin (2 notas del SEQ2 en el bosque)
    for _ in range(5):
        m.note_on(W, c, m.GEO, m.cell_note(fila[1]), 100, t, 120.0)
    veg = [x for x in [i] + list(m.NEIGH[i]) if W['own'][x] == m.GEO]
    if veg:
        i = veg[0]
        for x in [i] + [y for y in m.NEIGH[i] if W['own'][y] == m.GEO][:2]:
            for _ in range(2 if x == i else 1):
                m.note_on(W, c, m.ARQ, m.cell_note(x), 100, t, 120.0)
    for k in range(60):
        t += 1 / 30.0
        m.tick(W, c, t, 120.0, True)
    m.note_on(W, c, m.GEO, m.cell_note(i), 100, t, 120.0)       # la nota: el borde se tine
    return c, W, t, fila, i


def esfera(filas=256, cols=512):
    """La malla del terreno: esfera unidad (posicion y normal)."""
    v = []
    for r in range(filas + 1):
        la = math.pi * r / filas - math.pi / 2
        for k in range(cols + 1):
            lo = 2 * math.pi * k / cols - math.pi
            v.append([math.cos(la) * math.cos(lo), math.sin(la), math.cos(la) * math.sin(lo)])
    v = np.array(v, dtype='f4')
    tri = []
    for r in range(filas):
        for k in range(cols):
            a, b = r * (cols + 1) + k, r * (cols + 1) + k + 1
            c_, d = a + cols + 1, b + cols + 1
            tri += [a, b, d, a, d, c_]
    P = v[np.array(tri)]
    return np.concatenate([P, P, np.zeros_like(P)], axis=1).astype('f4')


def texturas(ctx, m, c):
    """sAlturas (el mapa del motor) y sRampa (la rampa de los pisos)."""
    a = m.alturas_array()
    alt = ctx.texture((a.shape[1], a.shape[0]), 4, a.astype('f4').tobytes(), dtype='f4')
    alt.repeat_x, alt.repeat_y = True, False
    claves = m.rampa_hipso(c)
    fil = np.array([list(m.color_piso(c, x / 255.0)) + [1.0] for x in range(256)], dtype='f4')
    ram = ctx.texture((256, 1), 4, fil.tobytes(), dtype='f4')
    ram.repeat_x = ram.repeat_y = False
    cu = m.cultivos_array()                     # fase 11 v8: bancales, riego y mesetas
    cul = ctx.texture((cu.shape[1], cu.shape[0]), 4, cu.astype('f4').tobytes(), dtype='f4')
    cul.repeat_x, cul.repeat_y = True, False
    return alt, ram, len(claves), cul


def dibujar(ctx, prog, m, c, W, now, cam, foco, lado=700, terreno=None):
    inst = m.build_instances(W, c, now)
    fbo = ctx.simple_framebuffer((lado, lado))
    fbo.use()
    fbo.clear(0.08, 0.08, 0.10, 1.0, depth=1.0)
    ctx.enable(ctx.DEPTH_TEST)
    VP = mirar(cam, foco)
    prog['uViewProj'].write(VP.T.astype('f4').tobytes())
    Ci = np.linalg.inv(np.array([[1, 0, 0, cam[0]], [0, 1, 0, cam[1]], [0, 0, 1, cam[2]], [0, 0, 0, 1.0]]))
    prog['uTDMats[0].camInverse'].write(np.linalg.inv(Ci).T.astype('f4').tobytes())
    if 'uTDMats[0].worldInverse' in prog:
        prog['uTDMats[0].worldInverse'].write(np.identity(4).astype('f4').tobytes())
    uni = m.uniformes_piel(W, c, now) if hasattr(m, 'uniformes_piel') else {}
    for k, v in uni.items():
        if k in prog and k != 'uTerreno':
            prog[k].value = tuple(float(x) for x in v)
    for k in ('uTerreno',):
        if k in prog:
            prog[k].value = (0.0, 1.0, 0.0, 1.0)
    R = m.top_radius(W, c)
    luces = dict(uLuz0=(0.0, R * 2 + 14, 4.0, 0), uLuz0Col=(0.82 * 1.15, 0.90 * 1.15, 1.15, 0),
                 uLuz1=(14.0, -10.0, 18.0, 0), uLuz1Col=(0.10, 0.14, 0.20, 0),
                 uLuz2=(0, 0, 0, 0), uLuz2Col=(0, 0, 0, 0), uAmbiente=(0.16, 0.16, 0.18, 0),
                 uVentanas=(0, 0, 0, 0))
    for k, v in luces.items():
        if k in prog:
            prog[k].value = v
    if terreno is not None and 'uTerreno' in prog:      # fase 11 v5: la malla del relieve
        alt, ram, _, cul = terreno
        alt.use(0)
        ram.use(1)
        cul.use(2)
        if 'sCultivo' in prog:
            prog['sCultivo'].value = 2
        if 'sAlturas' in prog:
            prog['sAlturas'].value = 0
        if 'sRampa' in prog:
            prog['sRampa'].value = 1
        prog['uTerreno'].value = (1.0, float(uni['uTerreno'][1]), float(uni['uTerreno'][2]), 1.0)
        prog['uFamilia'].value = (3.0, 0, 0, 0)
        esf = esfera()
        vbo = ctx.buffer(esf.tobytes())
        ibo = ctx.buffer(np.array([[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]], dtype='f4').tobytes())
        cd = ctx.buffer(np.ones((len(esf), 4), dtype='f4').tobytes())
        vao = ctx.vertex_array(prog, [(vbo, '3f 3f 3f', 'P', 'N', 'uv0'), (cd, '4f', 'Cd'),
                                      (ibo, '3f 3f 3f 4f/i', 'iT', 'iR', 'iS', 'iC')])
        vao.render(instances=1)
        prog['uTerreno'].value = (0.0, 1.0, 0.0, 1.0)
    for g, fam in (('rios', 4.0), ('tejido', 0.0)):    # fase 11 v5: rios y lagos (agua)
        filas = inst.get(g) or []
        if not filas or 'uFamilia' not in prog:
            continue
        prog['uFamilia'].value = (fam, 0, 0, 0)
        tri = malla(m, [('caja', 0.0, 0.5, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)], c)
        vbo = ctx.buffer(tri.tobytes())
        datos = np.array([list(f[:12]) + [f[12] if len(f) > 12 else 1.0] for f in filas], dtype='f4')
        ibo = ctx.buffer(datos.tobytes())
        cd = ctx.buffer(np.ones((len(tri), 4), dtype='f4').tobytes())
        vao = ctx.vertex_array(prog, [(vbo, '3f 3f 3f', 'P', 'N', 'uv0'), (cd, '4f', 'Cd'),
                                      (ibo, '3f 3f 3f 4f/i', 'iT', 'iR', 'iS', 'iC')])
        vao.render(instances=len(filas))
    for g, mo, mat in m.geometrias_piel(c):
        filas = inst.get(g) or []
        if not filas:
            continue
        if 'uFamilia' in prog:
            prog['uFamilia'].value = (float(m.FAMILIAS.index(m.familia_de(mo))) if mo[:3] != 'ciu' else 0.0,
                                      0, 0, 0)
        tri = malla(m, mo if m.es_ejemplar(mo) else m.MODELOS[mo], c)
        vbo = ctx.buffer(tri.tobytes())
        datos = np.array([list(f[:12]) + [f[12] if len(f) > 12 else 1.0] for f in filas], dtype='f4')
        ibo = ctx.buffer(datos.tobytes())
        cd = ctx.buffer(np.ones((len(tri), 4), dtype='f4').tobytes())
        vao = ctx.vertex_array(prog, [(vbo, '3f 3f 3f', 'P', 'N', 'uv0'), (cd, '4f', 'Cd'),
                                      (ibo, '3f 3f 3f 4f/i', 'iT', 'iR', 'iS', 'iC')])
        vao.render(instances=len(filas))
    img = np.frombuffer(fbo.read(components=3), dtype='u1').reshape(lado, lado, 3)[::-1]
    return img, inst


def main():
    import moderngl
    from PIL import Image
    salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'glsl_piel.png')
    ctx = moderngl.create_standalone_context(require=430)
    try:
        prog = compilar(ctx)
    except Exception as e:
        print('FALLO  el shader no compila:\n%s' % e)
        return 1
    print('OK     el shader de la piel compila (%s)' % ctx.info['GL_RENDERER'])
    m = vp.cargar_motor()
    imgs = []
    for c, W, now in escena(m):
        i, j = m.note_cell(64), m.note_cell(40)
        mid = m._norm(m._add(m.normal_i(i), m.normal_i(j)))
        foco = m._mul(mid, 6.5)
        cam = m._add(m._mul(mid, 17.0), m._mul(m.tangents(mid)[0], 6.0))
        img, inst = dibujar(ctx, prog, m, c, W, now, cam, foco)
        imgs.append(img)
        print('       %s, vel %d: %d instancias de modelos'
              % (m.tema_de(c), W['vel'][i], sum(len(v) for k, v in inst.items() if k.startswith('mod_'))))
    fila = lambda a, b: np.concatenate([a, b], axis=1)
    if hasattr(m, 'terreno'):                   # fase 11 v5: la naturaleza legible, cerca y lejos
        c, W, now, cord, bosque = escena_natural(m)
        m.terreno(W, c)
        m.build_instances(W, c, now)
        tex = texturas(ctx, m, c)
        mid = m._norm(m._add(m.normal_i(cord[2]), m.normal_i(bosque)))
        R = m.top_radius(W, c)
        for dist, k in ((R * 2.3, 0.0), (R * 5.2, 0.0)):
            cam = m._add(m._mul(mid, dist), m._mul(m.tangents(mid)[0], dist * 0.25))
            img, inst = dibujar(ctx, prog, m, c, W, now, cam, m._mul(mid, R * 0.6), terreno=tex)
            imgs.append(img)
        pz = W['piel']
        print('       naturaleza legible: %d ejemplares (%d hojas), %d montes, %d cordilleras, %d cumbres '
              'nevadas, rios %d (%d lagos), arrozales %s, mesetas %s'
              % (pz['ejemplares'], pz['hojas'], pz['montes'], pz['cordilleras'], pz['nevadas'],
                 W['rios_res']['rios'], W['rios_res']['lagos'], pz['hibridos']['arrozales'],
                 pz['hibridos']['mesetas']))
    filas_img = [fila(imgs[0], imgs[1]), fila(imgs[2], imgs[3])]
    if len(imgs) >= 6:
        filas_img.append(fila(imgs[4], imgs[5]))
    Image.fromarray(np.concatenate(filas_img, axis=0)).save(salida)
    print('       %s' % salida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
