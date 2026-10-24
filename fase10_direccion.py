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
                 tan grande como dice Encuadre: el alto del planeta en la
                 pantalla (0,85 por defecto: queda sitio arriba y abajo para
                 lo que crece; 1 = de borde a borde). Solo cambia con una
                 concha nueva: la camara se aleja en Camsuave s
                 (amortiguado critico, travelling: el FOV no cambia) y el
                 planeta nunca se sale del cuadro. Crecer, erosionar o el
                 latido no la mueven. Fija en +Z: el giro y el balanceo del
                 planeta ensenan todas sus caras.
     superficie  la camara de la fase 10 v4: orbita lenta (Camvel) a
                 Camaltura de la superficie, mirando al horizonte.
               Cambiar de modo en directo hace una transicion de 20 s.
               (v11: sin Planofinal: el globo ya es la camara por defecto;
               relanzar la fase lo borra de la pagina)
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

VERSION = 'fase10 v11  (sin Planofinal: la camara la gobiernan Modocamara, Camaltura y Camvel)'
banner(VERSION)

base = require_base(10)
motor = install_core(base, CARPETA, 10)

page = get_page(base, 'Fase10')
add_par(base, page, 'menu', 'Modocamara', 'Camara', 'globo', menu=['globo', 'superficie'],
        menu_labels=['Globo entero', 'Superficie'])
add_encuadre(base)                      # motor v36: un solo parametro de encuadre
add_par(base, page, 'float', 'Camsuave', 'Segundos para el encuadre nuevo', 3.0, 0.0, 20.0)
add_par(base, page, 'toggle', 'Modoactuacion', 'Modo actuacion (sin diagnostico)', False)
add_par(base, page, 'float', 'Camaltura', 'Altura de camara sobre la superficie (superficie)', 4.0, 0.5, 20.0)
add_par(base, page, 'float', 'Camvel', 'Velocidad de camara, grados/s (superficie)', 0.6, 0.0, 6.0)
for nm, lb in (('Camaltura', 'Altura de camara sobre la superficie (superficie)'),
               ('Camvel', 'Velocidad de camara, grados/s (superficie)')):
    try:
        getattr(base.par, nm).label = lb
    except Exception:
        pass
ok('pagina Fase10: Modocamara (globo), Encuadre (0,85), Camsuave (3 s), Modoactuacion, '
   'Camaltura, Camvel')


def quitar_planofinal(base):
    """v11: Planofinal ya no existe (la camara de globo es la de por defecto):
    en un proyecto que lo tenia se borra el parametro."""
    return has_par(base, 'Planofinal') and remove_par(base, 'Planofinal')


if quitar_planofinal(base):
    ok('Planofinal: quitado de la pagina Fase10 (la camara la gobiernan Modocamara, Camaltura y Camvel)')

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
  Camara de globo (Modocamara): el planeta entero y centrado; Encuadre es
  su alto en la pantalla (1 = de borde a borde). Con cada concha nueva se
  aleja en Camsuave s. Superficie: a Camaltura, orbita a Camvel grados/s;
  cambiar de modo hace una transicion de 20 s.
  Modoactuacion: sin reticula ni leyenda; la luz de celda se ve.
  Luz cenital fria; nucleo negro; una concha de cada color; cian en cicatrices.""")

print_report()


def prueba(t):
    import math
    m = t.m
    c = m.cfg()
    # encuadre: el planeta ocupa Encuadre del lado mas estrecho, en varios aspectos
    enc = []
    for R in (6.0, 11.5, 43.0):
        for asp in (16 / 9.0, 4 / 3.0, 1.0, 9 / 16.0):
            for met in ('horzfov', 'vertfov'):
                for k in (0.85, 1.0):
                    d, th = m.distancia_encuadre(R, 45.0, asp, k, met)
                    enc.append(abs(m.fraccion_cuadro(R, d, th) - k) < 1e-9 and th <= math.radians(45) + 1e-9)
    t.check('Encuadre: el planeta ocupa esa fraccion del lado mas estrecho (16:9, 4:3, 1:1, 9:16)', all(enc))
    t.check('altura maxima de las formaciones', m.altura_max(c) > m.limit(c), '%.3f' % m.altura_max(c))
    # camara de globo por el camino real
    m.cam_reset()
    m._CACHE.pop('cam_w', None)
    modo0 = str(base.par.Modocamara.eval())
    base.par.Modocamara = 'globo'
    st = m.camera_state()
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5
    t.check('globo: mira al centro desde +Z y el planeta ocupa Encuadre del cuadro',
            abs(p[0]) < 1e-9 and abs(p[1]) < 1e-9 and max(abs(x) for x in st['tgt']) < 1e-9
            and abs(m.fraccion_cuadro(st['Re'], dist, st['theta']) - st['encuadre']) < 1e-6,
            'dist %.2f, planeta %.2f, %d%% del cuadro' % (dist, st['Re'],
                                                         round(100 * m.fraccion_cuadro(st['Re'], dist, st['theta']))))
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
    """Encuadre (motor v36): el planeta ocupa Encuadre del cuadro; solo
    cambia con una concha nueva, y entonces la camara se aleja."""
    import math
    t0 = absTime.seconds

    def paso(seg):
        m._CACHE['cam_t'] = t0 - seg           # como si hubieran pasado 'seg' segundos
        m._CACHE.pop('cam_frame', None)
        st_ = m.camera_state()
        p_ = st_['pos']
        return st_, math.sqrt(p_[0] ** 2 + p_[1] ** 2 + p_[2] ** 2)

    k0 = float(base.par.Encuadre)
    m.reset_world()
    base.par.Velprueba = 100
    base.par.Nota = 64
    m.on_pulse('Sembrar')
    W, c = m.world(), m.cfg()
    m.cam_reset()
    st, d0 = paso(0.0)
    R = m.top_radius(W, c)
    t.check('el planeta (con la reticula) ocupa Encuadre del cuadro',
            abs(st['Re'] - (R + m.RETICULA_SOBRE)) < 1e-9
            and abs(m.fraccion_cuadro(st['Re'], d0, st['theta']) - k0) < 1e-6,
            'Encuadre %.2f, dist %.2f' % (k0, d0))
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
        cabe = cabe and m.fraccion_cuadro(R2 + m.RETICULA_SOBRE, d, st['theta']) <= 1.0 + 1e-9
    fin = m.fraccion_cuadro(R2 + m.RETICULA_SOBRE, ds[-1], st['theta'])
    t.check('concha nueva: la camara se aleja (Camsuave) hasta el mismo Encuadre; el planeta siempre cabe',
            R2 > R and cabe and d0 < ds[0] < ds[-1] and abs(fin - k0) < 0.01,
            'radio %.2f -> %.2f, dist %.2f -> %.2f -> %.2f' % (R, R2, d0, ds[0], ds[-1]))
    base.par.Encuadre = 1.0
    m.cam_reset()
    st, d1 = paso(0.0)
    t.check('Encuadre 1: el planeta de borde a borde', abs(m.fraccion_cuadro(st['Re'], d1, st['theta']) - 1.0) < 1e-6)
    base.par.Encuadre = k0
    t.check('sin Encuadremargen ni Holguraaltura (un solo parametro)',
            not has_par(base, 'Encuadremargen') and not has_par(base, 'Holguraaltura'))
    # v11: relanzar la fase sobre un proyecto que tenia Planofinal lo borra
    if not has_par(base, 'Planofinal'):
        get_page(base, 'Fase10').appendToggle('Planofinal', label='Plano final (v10)')
    tenia = has_par(base, 'Planofinal')
    quitar_planofinal(base)
    t.check('sin Planofinal: relanzar la fase sobre un proyecto que lo tenia borra el parametro',
            tenia and not has_par(base, 'Planofinal') and m._p('Planofinal', None) is None)
    m.cam_reset()


run_test(base, prueba)
print('  Listo: el sistema completo.')
print('  Para actuar: Modoactuacion.')
print('  Ajustes de encuadre: Encuadre (alto del planeta), Camsuave y Tilt; en superficie,')
print('  Camaltura y Camvel.')
print('=' * 66)
