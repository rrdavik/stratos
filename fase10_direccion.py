"""
=============================================================================
ESTRATOS - FASE 10: DIRECCION VISUAL Y CAMARA
=============================================================================
Requiere la fase 9. Lleva el prototipo al lenguaje de la seccion III del
marco conceptual.

QUE HACE
--------
  PALETA       nucleo negro profundo, cada concha de un color (fase 8,
               Paleta; mineral para la anterior), cian solo en cicatrices.
  LUZ          cenital fria y constante (sube con el planeta), relleno
               azulado muy tenue. Eje inclinado 20 grados (Tilt).
  CAMARA       (Modocamara)
     globo       por defecto: mira al centro y encuadra el planeta entero
                 tan cerca como permite el cuadro (Encuadremargen de
                 holgura, 1,02). Radio que se encuadra (motor v33) = radio
                 nominal + Holguraaltura (0,4) x altura maxima de las
                 formaciones: algo de sitio para las construcciones. Solo
                 cambia con una concha nueva: crecer, erosionar o el latido
                 no mueven la camara. Con cada concha se aleja en Camsuave s
                 (amortiguado critico, travelling: el FOV no cambia); el
                 planeta nunca se sale del cuadro. Fija en +Z: el giro y el
                 balanceo del planeta ensenan todas sus caras.
     superficie  la camara de la fase 10 v4: orbita lenta (Camvel) a
                 Camaltura de la superficie, mirando al horizonte.
                 Planofinal la lleva en 20 s al encuadre de globo.
               Cambiar de modo en directo hace la misma transicion de 20 s.
  ACTUACION    Modoactuacion oculta reticula y leyenda (la luz de celda se
               ve: es parte del mundo). Al
               quitarlo vuelve el modo diagnostico.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase10_direccion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase10 v9  (camara de globo cercana: el planeta y Holguraaltura; superficie como modo; paleta)'
banner(VERSION)

base = require_base(10)
motor = install_core(base, CARPETA, 10)

page = get_page(base, 'Fase10')
add_par(base, page, 'menu', 'Modocamara', 'Camara', 'globo', menu=['globo', 'superficie'],
        menu_labels=['Globo entero', 'Superficie'])
add_par(base, page, 'float', 'Encuadremargen', 'Holgura alrededor del globo', 1.02, 1.0, 1.5, clamp=True)
renew_default(base, 'Encuadremargen', 1.08, 1.02)    # motor v33: encuadre cercano
add_par(base, page, 'float', 'Camsuave', 'Segundos para el encuadre nuevo', 3.0, 0.0, 20.0)
add_par(base, page, 'float', 'Holguraaltura', 'Holgura para la altura de las construcciones (0 planeta, 1 todo)', 0.4, 0.0, 1.0,
        clamp=True)
add_par(base, page, 'toggle', 'Modoactuacion', 'Modo actuacion (sin diagnostico)', False)
add_par(base, page, 'toggle', 'Planofinal', 'Plano final: el globo entero (en superficie)', False)
add_par(base, page, 'float', 'Camaltura', 'Altura de camara sobre la superficie (superficie)', 4.0, 0.5, 20.0)
add_par(base, page, 'float', 'Camvel', 'Velocidad de camara, grados/s (superficie)', 0.6, 0.0, 6.0)
for nm, lb in (('Planofinal', 'Plano final: el globo entero (en superficie)'),
               ('Camaltura', 'Altura de camara sobre la superficie (superficie)'),
               ('Camvel', 'Velocidad de camara, grados/s (superficie)')):
    try:
        getattr(base.par, nm).label = lb
    except Exception:
        pass
ok('pagina Fase10: Modocamara (globo), Encuadremargen (1,02), Camsuave (3 s), Holguraaltura (0,4), Modoactuacion, '
   'Planofinal, Camaltura, Camvel')

# --- camara -------------------------------------------------------------------
obj = get_or_make(base, 'nullCOMP', 'objetivo', 400, -280)
for k, ax in enumerate(('tx', 'ty', 'tz')):
    setexpr(obj, ax, "parent().op('motor').module.cam('tgt', %d, absTime.frame)" % k)
set_camera(base)                       # ahora con 'objetivo': Look At
cam = base.op('camara')
try:
    lk = cam.par.lookat.eval()
except Exception:
    lk = None
if lk:
    ok('camara: globo por defecto (mira al centro); superficie como modo')
else:
    fail('no pude poner Look At en la camara: pon "objetivo" a mano')

# --- luces --------------------------------------------------------------------
luz = base.op('luz_principal')
setp(luz, 'tx', 0.0)
setexpr(luz, 'ty', "parent().op('motor').module.surface_radius(absTime.frame) * 2.0 + 14.0")
setp(luz, 'tz', 4.0)
setp(luz, 'dimmer', 1.15)
frias = color_luz(luz, (0.82, 0.90, 1.00))
rel = base.op('luz_relleno')
setp(rel, 'dimmer', 0.16)
frias = color_luz(rel, (0.35, 0.55, 0.80)) and frias
if not frias:
    info('no encontre el color de las luces (cr cg cb): luz_principal y luz_relleno saldran blancas')
# el relleno se aleja con el planeta (antes quedaba dentro al pasar de ~17 de
# radio) y alumbra desde abajo y por delante: la cara que ve la camara de globo
RELLENO = "parent().op('motor').module.cam('Re', 0, absTime.frame) * 2.0 + 14.0"
for ax, k in (('tx', 0.55), ('ty', -0.45), ('tz', 0.70)):
    setexpr(rel, ax, "(%s) * %.2f" % (RELLENO, k))
ok('luces: cenital fria que sube con el planeta, relleno tenue que se aleja con el')

# --- materiales -----------------------------------------------------------------
mn = base.op('mat_nucleo')
for ch in 'rgb':
    setp(mn, 'diffuse' + ch, 0.05)
setp_any(mn, ['shininess', 'specularexp'], 6)
ok('nucleo: negro profundo')

# --- modo actuacion -------------------------------------------------------------
salida = base.op('salida')
con_rot = base.op('con_rotulo') or base.op('rotulo')
render = base.op('render')
modo = fresh(base, 'switchTOP', 'modo', 860, -60)
connect(modo, con_rot if base.op('con_rotulo') is not None else render, 0)
connect(modo, render, 1)
setexpr(modo, 'index', 'int(parent().par.Modoactuacion)')
connect(salida, modo, 0)
ok('salida: con leyenda (diagnostico) o sin ella (Modoactuacion)')

set_render(base)

leeme(base, 10, """FASE 10 - DIRECCION VISUAL
  Camara de globo (Modocamara): el planeta entero, centrado, tan cerca
  como permite el cuadro (Encuadremargen), con Holguraaltura para las
  construcciones; solo retrocede, en Camsuave s, a cada enterramiento. Superficie: a Camaltura, orbita a Camvel grados/s;
  Planofinal la lleva al globo en 20 s.
  Modoactuacion: sin reticula ni leyenda; la luz de celda se ve.
  Luz cenital fria; nucleo negro; una concha de cada color; cian en cicatrices.""")

print_report()


def prueba(t):
    import math
    m = t.m
    c = m.cfg()
    # encuadre: el globo entero con su holgura en varios aspectos
    enc = []
    for R in (6.0, 11.5, 43.0):
        for asp in (16 / 9.0, 4 / 3.0, 1.0, 9 / 16.0):
            for met in ('horzfov', 'vertfov'):
                d, dmin, th = m.globe_distance(R, 45.0, asp, 1.08, met)
                enc.append(abs(math.asin(R / d) - math.asin(1 / 1.08 * math.sin(th / 2))) < 1e-9
                           and math.asin(R / dmin) <= th / 2 + 1e-9 and th <= math.radians(45) + 1e-9)
    t.check('encuadre: el globo cabe entero con la holgura de Encuadremargen (16:9, 4:3, 1:1, 9:16)',
            all(enc))
    t.check('altura maxima de las formaciones', m.altura_max(c) > m.limit(c), '%.3f' % m.altura_max(c))
    # camara de globo por el camino real
    m.cam_reset()
    m._CACHE.pop('cam_w', None)
    modo0 = str(base.par.Modocamara.eval())
    base.par.Modocamara = 'globo'
    st = m.camera_state()
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5
    t.check('globo: mira al centro desde +Z y el globo cabe',
            abs(p[0]) < 1e-9 and abs(p[1]) < 1e-9 and max(abs(x) for x in st['tgt']) < 1e-9
            and math.asin(st['Re'] / dist) <= st['theta'] / 2 + 1e-9,
            'dist %.2f radio encuadre %.2f' % (dist, st['Re']))
    t.check('planos de recorte', st['far'] >= dist + 2 * st['Re'] and 0 < st['near'] < dist - st['Re'])
    _encuadre_cercano(t, m)
    # superficie como modo (sin transicion, para medirla)
    base.par.Modocamara = 'superficie'
    m._CACHE['cam_w'] = 1.0
    m._CACHE.pop('cam_frame', None)
    st = m.camera_state()
    R = st['R']
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5 - R
    t.check('superficie: camara a Camaltura de la superficie', abs(dist - float(base.par.Camaltura)) < 0.05,
            '%.2f' % dist)
    g = st['tgt']
    t.check('superficie: mira a un punto de la superficie',
            abs((g[0] ** 2 + g[1] ** 2 + g[2] ** 2) ** 0.5 - R) < 0.05)
    base.par.Modocamara = modo0
    m._CACHE.pop('cam_w', None)
    m._CACHE.pop('cam_frame', None)
    t.check('leyenda CAMARA', 'CAMARA' in m.legend())
    before = bool(base.par.Modoactuacion)
    base.par.Modoactuacion = True
    m.on_value('Modoactuacion', True)
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    m.erosion(m.world(), m.cfg(), 0, 100, 0.0)            # el pad 1 ilumina su celda
    inst = m.build_instances(m.world(), m.cfg(), 0.1, hide_beacons=m.performance())
    t.check('modo actuacion: sin reticula; la luz de celda se ve',
            inst['luz_celda'] and 'baliza2' not in inst and not int(base.par.Showgrid))
    base.par.Modoactuacion = before
    m.on_value('Modoactuacion', before)
    t.check('al quitarlo vuelve la reticula', bool(int(base.par.Showgrid)) == (not before))


def _encuadre_cercano(t, m):
    """Encuadre cercano (motor v33): el planeta entero mas Holguraaltura de
    la altura maxima; solo cambia con una concha nueva."""
    import math
    t0 = absTime.seconds

    def paso(seg):
        m._CACHE['cam_t'] = t0 - seg           # como si hubieran pasado 'seg' segundos
        m._CACHE.pop('cam_frame', None)
        st_ = m.camera_state()
        p_ = st_['pos']
        return st_, math.sqrt(p_[0] ** 2 + p_[1] ** 2 + p_[2] ** 2)

    hol = float(base.par.Holguraaltura)
    m.reset_world()
    base.par.Velprueba = 100
    base.par.Nota = 64
    m.on_pulse('Sembrar')
    W, c = m.world(), m.cfg()
    m.cam_reset()
    st, d0 = paso(0.0)
    R = m.top_radius(W, c)
    Re = R + hol * m.altura_max(c)
    d_ok = m.globe_distance(Re, st['fov'], st['aspect'], st['margen'], st['metodo'])[0]
    t.check('encuadre cercano: el planeta y Holguraaltura de la altura maxima, con Encuadremargen',
            abs(d0 - d_ok) < 1e-6 and abs(st['Re'] - Re) < 1e-9 and Re < m.radio_encuadre(W, c, 1.0),
            'radio %.2f (planeta %.2f; antes %.2f), dist %.2f' % (Re, R, m.radio_encuadre(W, c, 1.0), d0))
    # crecer y el latido no mueven la camara
    ds = []
    for k in range(6):
        m.on_pulse('Sembrar')
        W['vh'] = list(W['h'])
        m._CACHE['inst'] = m.build_instances(W, c, t0 + k)
        ds.append(paso(0.25)[1])
    t.check('crecer no mueve la camara (sin reencuadres)', max(abs(x - d0) for x in ds) < 1e-9,
            'dist %.2f .. %.2f' % (min(ds), max(ds)))
    # una concha nueva: se aleja suave, sin saltos, y el planeta siempre cabe
    m.on_pulse('Forzarciclo')
    W = m.world()
    R2 = m.top_radius(W, c)
    cabe, ds = True, []
    for _ in range(int(4 * max(1.0, float(base.par.Camsuave)) / 0.25) + 8):
        st, d = paso(0.25)
        ds.append(d)
        cabe = cabe and math.asin(min(1.0, (R2 + 0.2) / d)) <= st['theta'] / 2 + 1e-9
    d_fin = m.globe_distance(R2 + hol * m.altura_max(c), st['fov'], st['aspect'], st['margen'], st['metodo'])[0]
    t.check('concha nueva: la camara se aleja suave (Camsuave) y el planeta siempre cabe',
            R2 > R and cabe and d0 < ds[0] < d0 + 0.5 * (d_fin - d0) and abs(ds[-1] - d_fin) < 0.02 * d_fin,
            'radio %.2f -> %.2f, dist %.2f -> %.2f -> %.2f' % (R, R2, d0, ds[0], ds[-1]))
    base.par.Holguraaltura = 1.0
    t.check('Holguraaltura 1: todo lo que podria crecer (el encuadre de antes)',
            abs(m.radio_encuadre(W, c) - (R2 + m.altura_max(c))) < 1e-9)
    base.par.Holguraaltura = hol
    m.cam_reset()


run_test(base, prueba)
print('  Listo: el sistema completo.')
print('  Para actuar: Modoactuacion. Para cerrar: Planofinal.')
print('  Ajustes de encuadre: Encuadremargen, Camsuave y Tilt; en superficie,')
print('  Camaltura y Camvel.')
print('=' * 66)
