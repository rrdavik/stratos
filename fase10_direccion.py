"""
=============================================================================
ESTRATOS - FASE 10: DIRECCION VISUAL Y CAMARA
=============================================================================
Requiere la fase 9. Lleva el prototipo al lenguaje de la seccion III del
marco conceptual.

QUE HACE
--------
  PALETA       nucleo negro profundo, conchas en grises minerales con
               ambar en la base, cian solo en cicatrices.
  LUZ          cenital fria y constante (sube con el planeta), relleno
               azulado muy tenue. Eje inclinado 20 grados (Tilt).
  CAMARA       movimiento lento y continuo, ajeno al reloj del
               secuenciador, a DISTANCIA CONSTANTE DE LA SUPERFICIE
               (Camaltura): el encuadre no cambia y el crecimiento solo se
               nota por acumulacion. Mira al horizonte: la curvatura se
               insinua, el globo entero no se ve.
  PLANO FINAL  Planofinal aleja la camara en 20 s hasta ver el globo
               entero, una vez, como gesto. Al quitarlo vuelve.
  ACTUACION    Modoactuacion oculta reticula, balizas y leyenda. Al
               quitarlo vuelve el modo diagnostico.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase10_direccion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase10 v2  (paleta, luz cenital, camara de superficie, modos)'
banner(VERSION)

base = require_base(10)
motor = install_core(base, CARPETA, 10)

page = get_page(base, 'Fase10')
add_par(base, page, 'toggle', 'Modoactuacion', 'Modo actuacion (sin diagnostico)', False)
add_par(base, page, 'toggle', 'Planofinal', 'Plano final: el globo entero', False)
add_par(base, page, 'float', 'Camaltura', 'Altura de camara sobre la superficie', 4.0, 0.5, 20.0)
add_par(base, page, 'float', 'Camvel', 'Velocidad de camara (grados/s)', 0.6, 0.0, 6.0)
ok('pagina Fase10: Modoactuacion, Planofinal, Camaltura, Camvel')

# --- camara -------------------------------------------------------------------
obj = get_or_make(base, 'nullCOMP', 'objetivo', 400, -280)
for k, ax in enumerate(('tx', 'ty', 'tz')):
    setexpr(obj, ax, "parent().op('motor').module.cam('tgt', %d, absTime.frame)" % k)
cam = base.op('camara')
for k, ax in enumerate(('tx', 'ty', 'tz')):
    setexpr(cam, ax, "parent().op('motor').module.cam('pos', %d, absTime.frame)" % k)
for ax in ('rx', 'ry', 'rz'):
    try:
        getattr(cam.par, ax).expr = ''
    except Exception:
        pass
    setp(cam, ax, 0.0)
if setp(cam, 'lookat', 'objetivo'):
    ok('camara: orbita lenta a Camaltura de la superficie, mirando al horizonte')
else:
    fail('no pude poner Look At en la camara: pon "objetivo" a mano')

# --- luces --------------------------------------------------------------------
luz = base.op('luz_principal')
setp(luz, 'tx', 0.0)
setexpr(luz, 'ty', "parent().op('motor').module.surface_radius(absTime.frame) * 2.0 + 14.0")
setp(luz, 'tz', 4.0)
setp(luz, 'dimmer', 1.15)
setp(luz, 'lightcolorr', 0.82)
setp(luz, 'lightcolorg', 0.90)
setp(luz, 'lightcolorb', 1.00)
rel = base.op('luz_relleno')
setp(rel, 'dimmer', 0.16)
ok('luces: cenital fria que sube con el planeta, relleno tenue')

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
  Camara a Camaltura de la superficie, orbita a Camvel grados/s, ajena al
  secuenciador. Planofinal: el globo entero en 20 s.
  Modoactuacion: sin reticula, balizas ni leyenda.
  Luz cenital fria; nucleo negro; ambar en la base; cian en cicatrices.""")

print_report()


def prueba(t):
    m = t.m
    m._CACHE.pop('cam_frame', None)
    st = m.camera_state()
    R = st['R']
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5 - R
    t.check('camara a Camaltura de la superficie', abs(dist - float(base.par.Camaltura)) < 0.05,
            '%.2f' % dist)
    g = st['tgt']
    t.check('mira a un punto de la superficie',
            abs((g[0] ** 2 + g[1] ** 2 + g[2] ** 2) ** 0.5 - R) < 0.05)
    before = bool(base.par.Modoactuacion)
    base.par.Modoactuacion = True
    m.on_value('Modoactuacion', True)
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    m.erosion(m.world(), m.cfg(), 0, 100, 0.0)            # enciende la baliza del pad 1
    inst = m.build_instances(m.world(), m.cfg(), 0.1, hide_beacons=m.performance())
    vis = m.build_instances(m.world(), m.cfg(), 0.1, hide_beacons=False)
    t.check('modo actuacion: sin balizas (SEQ2 y bateria) ni reticula',
            not inst['baliza2'] and not inst['balizas_drum'] and vis['balizas_drum']
            and not int(base.par.Showgrid))
    base.par.Modoactuacion = before
    m.on_value('Modoactuacion', before)
    t.check('al quitarlo vuelve la reticula', bool(int(base.par.Showgrid)) == (not before))


run_test(base, prueba)
print('  Listo: el sistema completo.')
print('  Para actuar: Modoactuacion. Para cerrar: Planofinal.')
print('  Ajustes de encuadre: Camaltura, Camvel y Tilt.')
print('=' * 66)
