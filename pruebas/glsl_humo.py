"""
Comprueba el humo en la GPU (motor v74, comun v53) y las motas (comun v54: las
demas particulas, suaves) con un OpenGL de verdad, fuera
de TouchDesigner: compila HUMO_VERTEX y HUMO_PIXEL de estratos_comun.py con las
funciones que imitan las de TouchDesigner (las de glsl_piel.py) y dibuja las
bocanadas reales del motor sobre la escena de la industria, en tres fotos del
pulso, para ver que suben, se hinchan y se desvanecen.

    xvfb-run -a python3 pruebas/glsl_humo.py [salida.png]

El humo se compone encima de la imagen de las plantas (sin que los edificios lo
tapen: aqui no se comparte la profundidad). No comprueba que TouchDesigner
declare sus funciones igual ni los parametros de mezcla del GLSL MAT: solo que el
shader es GLSL 4.5 correcto y que hace lo que se espera con esos datos.
"""

import ast
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import glsl_piel as gp  # noqa: E402
import vista_previa as vp  # noqa: E402


def shaders(pref='HUMO'):
    """(PREF_VERTEX, PREF_PIXEL) de estratos_comun.py: HUMO o, desde comun v54, MOTAS."""
    arbol = ast.parse(open(os.path.join(REPO, 'estratos_comun.py'), encoding='utf-8').read())
    out = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 \
                and getattr(nodo.targets[0], 'id', '') in (pref + '_VERTEX', pref + '_PIXEL'):
            out[nodo.targets[0].id] = ast.literal_eval(nodo.value)
    return out[pref + '_VERTEX'], out[pref + '_PIXEL']


def vista(cam, foco):
    cam, foco = np.array(cam, float), np.array(foco, float)
    f = foco - cam
    f /= np.linalg.norm(f)
    r = np.cross(f, [0.0, 1.0, 0.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    V = np.identity(4)
    V[0, :3], V[1, :3], V[2, :3] = r, u, -f
    V[:3, 3] = -V[:3, :3] @ cam
    return V


def lamina():
    """Un Rectangle SOP de 1 x 1 centrado: dos triangulos (P, N, uv)."""
    q = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
    return np.array([[x, y, 0.0, 0.0, 0.0, 1.0, x + 0.5, y + 0.5, 0.0] for x, y in q], dtype='f4')


def humo(ctx, prog, filas, cam, foco, reloj=None, lfo=0.5, lado=700):
    """Las bocanadas (o, sin reloj, las motas) en un framebuffer transparente:
    (rgb premultiplicado, alfa)."""
    fbo = ctx.simple_framebuffer((lado, lado), components=4)
    fbo.use()
    fbo.clear(0.0, 0.0, 0.0, 0.0)
    ctx.disable(ctx.DEPTH_TEST)
    ctx.enable(ctx.BLEND)
    ctx.blend_func = ctx.ONE, ctx.ONE_MINUS_SRC_ALPHA
    V = vista(cam, foco)
    VP = gp.mirar(cam, foco)
    prog['uViewProj'].write(VP.T.astype('f4').tobytes())
    prog['uTDMats[0].camInverse'].write(np.linalg.inv(V).T.astype('f4').tobytes())
    if reloj is not None:
        prog['uHumo'].value = (float(reloj), float(lfo), 0.0, 0.0)
    tri = lamina()
    vbo = ctx.buffer(tri.tobytes())
    datos = np.array([list(f[:12]) + [f[12] if len(f) > 12 else 1.0] for f in filas], dtype='f4')
    ibo = ctx.buffer(datos.tobytes())
    cd = ctx.buffer(np.ones((len(tri), 4), dtype='f4').tobytes())
    vao = ctx.vertex_array(prog, [(vbo, '3f 24x', 'P'), (cd, '4f', 'Cd'),     # N y uv no se usan
                                  (ibo, '3f 3f 3f 4f/i', 'iT', 'iR', 'iS', 'iC')])
    vao.render(instances=len(filas))
    ctx.disable(ctx.BLEND)
    img = np.frombuffer(fbo.read(components=4, dtype='f1'), dtype='u1').reshape(lado, lado, 4)[::-1]
    return img.astype('f4') / 255.0


def main():
    import moderngl
    from PIL import Image
    salida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'glsl_humo.png')
    ctx = moderngl.create_standalone_context(require=430)
    v, p = shaders()
    try:
        prog = ctx.program(vertex_shader=gp.TD_VERTEX + v, fragment_shader=gp.TD_PIXEL + p)
    except Exception as e:
        print('FALLO  el shader del humo no compila:\n%s' % e)
        return 1
    print('OK     el shader del humo compila (%s)' % ctx.info['GL_RENDERER'])
    try:
        piel = gp.compilar(ctx)
    except Exception as e:
        print('FALLO  el shader de la piel no compila:\n%s' % e)
        return 1
    m = vp.cargar_motor()
    c, W, now, a, b = gp.escena_industria(m)
    # la camara, mirando las bocanadas: desde fuera, por encima de la fuente media y algo de lado
    filas0 = m.build_instances(W, c, now).get('humo') or []
    if not filas0:
        print('FALLO  la escena no tiene bocanadas (humo)')
        return 1
    centro = [sum(f[q] for f in filas0) / len(filas0) for q in range(3)]
    mid = m._norm(centro)
    alto = max(f[7] for f in filas0)
    foco = m._add(centro, m._mul(mid, 0.3 * alto))
    cam = m._add(m._add(foco, m._mul(mid, 2.2 * alto + 3.0)), m._mul(m.tangents(mid)[1], 2.0 * alto + 3.0))
    fotos = []
    k = max(1, int(c.get('steps_per_beat', 4))) * m.FOTOS_PASO
    for beat in (3.3, 3.3 + 0.2, 3.3 + 0.4):
        W['pulso']['beat'] = beat
        fondo, inst = gp.dibujar(ctx, piel, m, c, W, now, cam, foco)
        filas = inst.get('humo') or []
        if not filas:
            print('FALLO  la escena no tiene bocanadas (humo)')
            return 1
        reloj = m.beat_stop(W, c)
        h = humo(ctx, prog, filas, cam, foco, reloj, 0.5)
        f = fondo.astype('f4') / 255.0
        img = h[..., :3] + f * (1.0 - h[..., 3:4])
        fotos.append((np.clip(img, 0, 1) * 255).astype('u1'))
        cubre = float((h[..., 3] > 0.05).mean())
        print('       pulso %.2f (reloj a saltos %.3f): %d bocanadas, %.1f%% de la imagen con humo, '
              'alfa max %.2f' % (beat, reloj, len(filas), 100 * cubre, float(h[..., 3].max())))
        if cubre <= 0.0:
            print('FALLO  el humo no se ve')
            return 1
    # comun v54: las demas particulas, motas suaves (mat_motas): las de la industria
    # (balizas, antorcha, faros, pulsos de la red) y las esporas de la naturaleza
    vm, pm = shaders('MOTAS')
    try:
        motas = ctx.program(vertex_shader=gp.TD_VERTEX + vm, fragment_shader=gp.TD_PIXEL + pm)
    except Exception as e:
        print('FALLO  el shader de las motas no compila:\n%s' % e)
        return 1
    print('OK     el shader de las motas compila')
    fila2 = []
    escenas = [('industria', gp.escena_industria(m)[:3])]
    cn, Wn, nown = gp.escena_natural(m)[:3]
    cn = dict(cn, nivel=max(17, cn['nivel']))      # las esporas, desde la fase 17
    escenas.append(('naturaleza', (cn, Wn, nown)))
    for nombre, (c2, W2, now2) in escenas:
        inst = m.build_instances(W2, c2, now2)
        filas = inst.get('particulas') or []
        if not filas:
            print('FALLO  %s: la escena no tiene particulas' % nombre)
            return 1
        centro = [sum(f[q] for f in filas) / len(filas) for q in range(3)]
        mid2 = m._norm(centro)
        R2 = m.top_radius(W2, c2)
        foco2 = m._mul(mid2, R2 * 0.9)
        cam2 = m._add(m._mul(mid2, R2 * 1.9), m._mul(m.tangents(mid2)[1], R2 * 0.5))
        fondo, _ = gp.dibujar(ctx, piel, m, c2, W2, now2, cam2, foco2)
        h = humo(ctx, motas, filas, cam2, foco2)
        img = h[..., :3] + fondo.astype('f4') / 255.0 * (1.0 - h[..., 3:4])
        fila2.append((np.clip(img, 0, 1) * 255).astype('u1'))
        print('       %s: %d motas (%d vagones aparte), %.1f%% de la imagen' %
              (nombre, len(filas), len(inst.get('vagones') or []), 100 * float((h[..., 3] > 0.05).mean())))
    fila2.append(np.zeros_like(fila2[0]))
    Image.fromarray(np.concatenate([np.concatenate(fotos, axis=1), np.concatenate(fila2, axis=1)],
                                   axis=0)).save(salida)
    print('       imagen: %s' % salida)
    return 0


if __name__ == '__main__':
    sys.exit(main())
