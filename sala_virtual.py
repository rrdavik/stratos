"""
=============================================================================
ESTRATOS - SALA VIRTUAL (maqueta de la instalacion)
=============================================================================
No es una fase: es una maqueta de la sala en /project1/SALA, al lado de FASE1,
para probar la pieza como si estuviera montada. Habla con Estratos por los
mismos sitios que el hardware real, asi que la pieza no sabe si la sala es de
verdad: el microfono virtual entra por Fuentemic = chop (fase 21 v2), la
camara cenital da su imagen de profundidad (para la fase 22) y los focos se
encienden por su cuenta hasta que la fase 23 los mande por DMX.

QUE MONTA
---------
  SALA         8 x 6 m y 4 de alto (Ancho, Fondo, Alto): suelo, tres paredes
               (la de la entrada, abierta para mirar), la puerta en el centro
               de la de delante y, en el suelo, la zona que ve la camara
               (Zonaancho x Zonafondo, 5,4 x 4,5 m).
  EQUIPOS      la tabla 'equipos' (editable; relanzar no la pisa): la esfera
               de LEDs de 1 m en la esquina del fondo a la izquierda, sobre su
               peana con el subwoofer dentro; cuatro altavoces colgados en las
               esquinas; el microfono en lo alto, hacia el centro y lejos de la
               esfera y del estrobo; la camara cenital a 3,5 m; cuatro focos
               de bano (dos junto a la esfera, sin apuntarle) y el
               estroboscopio en el suelo junto a la esfera. Recolocar la
               rehace con las medidas de ahora.
  PERSONAS     Personas (6) que entran por la puerta cada Llegada s (8),
               pasean, se paran y se van, sin azar. Hacen ruido: pasos al
               andar y palmadas o toses (Ruidopublico por segundo y persona;
               Reaccion veces mas con el estrobo encendido).
  MICROFONO    el Script CHOP audio_mic: lo que oye el microfono virtual
               (pasos, palmadas, toses, el drone de los altavoces y el sub con
               Volumendrone y el clic del estrobo), cada fuente por 1/d y con
               su retardo. Con Usarmic, FASE1 lo lee (Fuentemic = chop).
  LUZ          una Light COMP por foco y por estrobo (luz_<nombre>). Modoluz
               = prueba recorre en un minuto deposito, tension y erosion
               dominante (estrobo blanco, Hzprueba, como mucho 3 Hz). Luzcasa,
               una luz tenue para ver la sala con los focos apagados.
  ESFERA       la imagen de FASE1 (su Render TOP 'render') sobre una esfera.
               OJO: la esfera real pide un mapa equirectangular 2:1, que
               Estratos aun no saca; aqui se ve la vista de la camara del
               planeta envolviendo la esfera.
  VISTAS       render_sala: la sala desde la camara libre (Orbita, Distancia,
               Alturavista) o desde la cenital (Vista). render_cenital: lo
               que ve la camara del techo (320 x 288), y 'profundidad', su
               imagen de profundidad, para la fase 22.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/sala_virtual.py').read())
  Mira render_sala. En la pagina Sala: Palmada (una palmada junto al micro),
  Personas, Ruidopublico, Modoluz. La leyenda MICRO de FASE1 cuenta los
  onsets del publico virtual.
=============================================================================
"""

import math

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'sala_virtual v1  (maqueta de la sala: esfera, altavoces, microfono, camara, focos y estrobo)'
banner(VERSION)
SALA_PATH = '/project1/SALA'

fase1 = op(COMP_PATH)
nivel = current_level(fase1) if fase1 is not None else 0
if fase1 is None:
    raise RuntimeError('No encuentro %s. Monta antes Estratos (fase12_base.py y las fases).' % COMP_PATH)

sala = op(SALA_PATH)
if sala is None:
    sala = mk(op('/project1'), 'baseCOMP', 'SALA', 400, 0)
    ok('SALA: componente nuevo en /project1, al lado de FASE1')
else:
    ok('SALA: ya existia; se conserva la tabla de equipos')

sm_dat = get_or_make(sala, 'textDAT', 'sala_motor', -660, -340)
src = read_text(CARPETA, 'sala_motor.py')
if sm_dat.text != src:
    sm_dat.text = src
try:
    sm = sm_dat.module
    ok('sala_motor cargado (%s)' % sm.SALA_VERSION)
except Exception as e:
    raise RuntimeError('sala_motor no compila: %s' % e)

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Sala)
# -----------------------------------------------------------------------------

page = get_page(sala, 'Sala')
add_par(sala, page, 'toggle', 'Activa', 'Sala activa (personas, sonido y luz)', True)
add_par(sala, page, 'float', 'Ancho', 'Ancho de la sala (m)', 8.0, 2.0, 30.0)
add_par(sala, page, 'float', 'Fondo', 'Fondo de la sala (m)', 6.0, 2.0, 30.0)
add_par(sala, page, 'float', 'Alto', 'Alto de la sala (m)', 4.0, 2.0, 12.0)
add_par(sala, page, 'float', 'Zonaancho', 'Zona de la camara: ancho (m)', 5.4, 1.0, 30.0)
add_par(sala, page, 'float', 'Zonafondo', 'Zona de la camara: fondo (m)', 4.5, 1.0, 30.0)
add_par(sala, page, 'pulse', 'Recolocar', 'Recolocar los equipos con estas medidas (rehace la tabla)')
add_par(sala, page, 'int', 'Personas', 'Personas', 6, 0, 30, clamp=True)
add_par(sala, page, 'float', 'Llegada', 'Segundos entre dos llegadas', 8.0, 0.0, 120.0, clamp=True)
add_par(sala, page, 'float', 'Ruidopublico', 'Palmadas y toses por segundo y persona', 0.05, 0.0, 2.0, clamp=True)
add_par(sala, page, 'float', 'Reaccion', 'Con el estrobo, el publico hace x veces mas ruido', 3.0, 0.0, 10.0, clamp=True)
add_par(sala, page, 'float', 'Volumendrone', 'Volumen del drone (altavoces y sub)', 0.5, 0.0, 2.0, clamp=True)
add_par(sala, page, 'pulse', 'Palmada', 'Probar: una palmada (la persona mas cerca del micro)')
add_par(sala, page, 'pulse', 'Reiniciarsala', 'Abrir la sala de nuevo (las personas vuelven a entrar)')
add_par(sala, page, 'toggle', 'Usarmic', 'FASE1 oye el microfono virtual (Fuentemic = chop)', True)
add_par(sala, page, 'menu', 'Modoluz', 'Luz de la sala', 'prueba', menu=sm.MODOS_LUZ,
        menu_labels=['Apagada', 'Prueba: los tres estados en un minuto'])
add_par(sala, page, 'float', 'Hzprueba', 'Prueba: destellos por segundo del estrobo (tope 3)', 2.5, 0.0, 3.0, clamp=True)
add_par(sala, page, 'float', 'Luzcasa', 'Luz de casa (para ver la sala)', 0.25, 0.0, 1.0, clamp=True)
add_par(sala, page, 'menu', 'Vista', 'Vista de render_sala', 'libre', menu=sm.VISTAS,
        menu_labels=['Libre (orbita)', 'Camara cenital'])
add_par(sala, page, 'float', 'Orbita', 'Vista libre: giro (grados)', 30.0, -180.0, 180.0)
add_par(sala, page, 'float', 'Distancia', 'Vista libre: distancia (m)', 11.0, 3.0, 40.0)
add_par(sala, page, 'float', 'Alturavista', 'Vista libre: altura (m)', 5.0, 0.5, 20.0)
ok('pagina Sala: Activa, Ancho 8, Fondo 6, Alto 4, Zonaancho 5,4, Zonafondo 4,5, Recolocar, Personas 6, '
   'Llegada 8, Ruidopublico 0,05, Reaccion 3, Volumendrone 0,5, Palmada, Reiniciarsala, Usarmic, '
   'Modoluz (prueba), Hzprueba 2,5, Luzcasa, Vista, Orbita, Distancia, Alturavista')

# -----------------------------------------------------------------------------
# LA TABLA DE EQUIPOS
# -----------------------------------------------------------------------------


tabla = sala.op('equipos')
if tabla is None:
    tabla = mk(sala, 'tableDAT', 'equipos', -660, 200)
    sm.recolocar()
    ok('equipos: esfera (esquina del fondo a la izquierda) y sub, 4 altavoces, micro, camara, '
       '4 focos y estrobo. Editala a mano: un foco mas es una fila mas')
else:
    ok('equipos: se conserva como esta (%d filas)' % max(0, tabla.numRows - 1))

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

INST_CB = r'''# Script CHOP de instancias de la sala virtual: piden a sala_motor sus
# filas por nombre (i_sala, i_equipos, i_personas).

CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']
DUMMY = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    try:
        rows = op('sala_motor').module.filas(scriptOp.name)
    except Exception:
        rows = []
    if not rows:
        rows = [DUMMY]
    n = len(rows)
    scriptOp.numSamples = n
    chans = [scriptOp.appendChan(nm) for nm in CHANS]
    scriptOp.numSamples = n
    for j, ch in enumerate(chans):
        ch.vals = [float(r[j]) for r in rows]
'''

AUDIO_CB = r'''# Script CHOP 'audio_mic': lo que oye el microfono virtual (sala_motor).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('sala_motor').module.audio_cook(scriptOp)
'''

LATIDO_SALA = r'''# Un latido por fotograma: las personas y los aparatos de la sala virtual.
def onFrameStart(frame):
    try:
        op('sala_motor').module.frame_tick()
    except Exception as e:
        if not me.fetch('err', False):
            print('FALLO en la sala virtual: %s' % e)
            me.store('err', True)
    return
'''

PULSOS_SALA = r'''# Botones de la pagina Sala -> sala_motor
def onPulse(par):
    op('sala_motor').module.on_pulse(par.name)
    return
'''

SM = "parent().op('sala_motor').module"


def instanciado(name, x, y, mat):
    """Geometry COMP 'name' con una caja de 1 x 1 x 1 (la base en y = 0)
    instanciada desde el Script CHOP 'i_name'."""
    chop = get_or_make(sala, 'scriptCHOP', 'i_' + name, x - 220, y)
    setp_any(chop, ['callbacks', 'callbackdat', 'dat'], 'instancias_sala')
    geo = fresh(sala, 'geometryCOMP', name, x, y)
    for k in list(geo.children):
        try:
            k.render = False
            k.display = False
        except Exception:
            pass
    s = mk(geo, 'boxSOP', 'bloque', 0, 0)
    for ax in ('sizex', 'sizey', 'sizez'):
        setp(s, ax, 1.0)
    setp(s, 'ty', 0.5)
    for attr in ('render', 'display'):
        try:
            setattr(s, attr, True)
        except Exception:
            pass
    setp(geo, 'instanceop', 'i_' + name)
    setp_any(geo, ['instancing', 'instance'], True)
    for par_name, ch in [('instancetx', 'tx'), ('instancety', 'ty'), ('instancetz', 'tz'),
                         ('instancerx', 'rx'), ('instancery', 'ry'), ('instancerz', 'rz'),
                         ('instancesx', 'sx'), ('instancesy', 'sy'), ('instancesz', 'sz')]:
        if not setp(geo, par_name, ch):
            info('%s: no encontre %s' % (name, par_name))
    setmenu(geo, ['instancerord'], ['xyz'], 0)
    set_instance_color(geo, name)
    setp(geo, 'material', mat)
    try:
        chop.cook(force=True)
    except Exception:
        pass
    return geo


cb = get_or_make(sala, 'textDAT', 'instancias_sala', -880, 0)
cb.text = INST_CB
make_phong(sala, 'mat_sala', 660, 200, spec=0.1, shin=4, diff=1.0, amb=0.15)
make_phong(sala, 'mat_equipos', 660, 120, spec=0.5, shin=20, diff=1.0, amb=0.2, emit=0.15)
make_phong(sala, 'mat_personas', 660, 40, spec=0.05, shin=2, diff=1.0, amb=0.2)
instanciado('sala_caja', 0, 200, 'mat_sala')
instanciado('equipos_geo', 0, 120, 'mat_equipos')
instanciado('personas', 0, 40, 'mat_personas')
ok('sala_caja, equipos_geo y personas: suelo, paredes, zona de la camara, puerta, aparatos y publico')

# la esfera de LEDs, con la imagen de FASE1
esfera = fresh(sala, 'geometryCOMP', 'esfera', 0, -40)
for k in list(esfera.children):
    try:
        k.render = False
        k.display = False
    except Exception:
        pass
bola = mk(esfera, 'sphereSOP', 'bola', 0, 0)
for ax in ('radx', 'rady', 'radz'):
    setexpr(bola, ax, "0.5 * parent(2).op('sala_motor').module.valor('esfera', 'cono', absTime.frame)")
setp_any(bola, ['type', 'primtype'], 'polymesh')
setp_any(bola, ['rows'], 40)
setp_any(bola, ['cols'], 40)
for attr in ('render', 'display'):
    try:
        setattr(bola, attr, True)
    except Exception:
        pass
for ax in ('tx', 'ty', 'tz'):
    setexpr(esfera, ax, "%s.valor('esfera', '%s', absTime.frame)" % (SM, ax))
mat_esfera = make_constant(sala, 'mat_esfera', 660, -40, (1.0, 1.0, 1.0))
imagen = setp_any(mat_esfera, ['colormap', 'map'], fase1.path + '/render')
setp(esfera, 'material', 'mat_esfera')
if imagen:
    ok('esfera: 1 m con la imagen de FASE1/render (la real pide un mapa equirectangular 2:1)')
else:
    info('esfera: no pude ponerle la imagen; en mat_esfera, Color Map = %s/render' % fase1.path)

# las luces: una por foco y por estrobo de la tabla, y la de casa
for o in [o for o in sala.children if o.name.startswith('luz_')]:
    o.destroy()
luces = []
eqs = sm.equipos()
for k, e in enumerate(x for x in eqs if x['tipo'] in ('foco', 'estrobo')):
    l = mk(sala, 'lightCOMP', 'luz_' + e['nombre'], 220, 200 - 80 * k)
    setmenu(l, ['lighttype'], ['cone'], 1)
    for ax in ('tx', 'ty', 'tz', 'rx', 'ry'):
        setexpr(l, ax, "%s.valor('%s', '%s', absTime.frame)" % (SM, e['nombre'], ax))
    setexpr(l, 'coneangle', "%s.valor('%s', 'cono', absTime.frame)" % (SM, e['nombre']))
    setp(l, 'conedelta', 10.0)
    color_luz_expr(l, ["%s.valor('%s', '%s', absTime.frame)" % (SM, e['nombre'], ch) for ch in 'rgb'])
    setexpr(l, 'dimmer', "%s.valor('%s', 'd', absTime.frame)" % (SM, e['nombre']))
    luces.append(l.name)
casa = mk(sala, 'lightCOMP', 'luz_casa', 220, 280)
setmenu(casa, ['lighttype'], ['point'], 0)
setp(casa, 'ty', 3.8)
setexpr(casa, 'dimmer', "float(parent().par.Luzcasa)")
luces.append(casa.name)
ok('luces: %s (conos desde la tabla; Modoluz las enciende)' % ' '.join(luces))

# las camaras y los renders
centro = get_or_make(sala, 'nullCOMP', 'centro', 440, 360)
setp(centro, 'ty', 1.0)
vista = get_or_make(sala, 'cameraCOMP', 'vista', 440, 280)
for ax in ('tx', 'ty', 'tz'):
    setexpr(vista, ax, "%s.vista('%s', absTime.frame)" % (SM, ax))
setp(vista, 'lookat', 'centro')
setp(vista, 'fov', 50.0)
cenital = get_or_make(sala, 'cameraCOMP', 'vista_cenital', 440, 200)
for ax in ('tx', 'ty', 'tz'):
    setexpr(cenital, ax, "%s.valor('camara', '%s', absTime.frame)" % (SM, ax))
setp(cenital, 'rx', -90.0)
setp(cenital, 'fov', 75.0)                  # Femto Bolt, NFOV: unos 75 x 65 grados
geos = 'sala_caja equipos_geo personas esfera'
r1 = get_or_make(sala, 'renderTOP', 'render_sala', 660, 360)
setexpr(r1, 'camera', "'vista_cenital' if str(parent().par.Vista) == 'cenital' else 'vista'")
setp(r1, 'geometry', geos)
setp(r1, 'lights', ' '.join(luces))
setp_any(r1, ['resolutionw'], 1280)
setp_any(r1, ['resolutionh'], 720)
r2 = get_or_make(sala, 'renderTOP', 'render_cenital', 660, 280)
setp(r2, 'camera', 'vista_cenital')
setp(r2, 'geometry', 'sala_caja personas')
setp(r2, 'lights', 'luz_casa')
setp_any(r2, ['resolutionw'], 320)
setp_any(r2, ['resolutionh'], 288)
prof = get_or_make(sala, 'depthTOP', 'profundidad', 880, 280)
connect(prof, r2, 0)
ok('render_sala (vista libre o cenital), render_cenital (320 x 288) y profundidad (para la fase 22)')

# el microfono virtual
cb = get_or_make(sala, 'textDAT', 'audio_callbacks', -880, -200)
cb.text = AUDIO_CB
audio = get_or_make(sala, 'scriptCHOP', 'audio_mic', -660, -200)
setp_any(audio, ['callbacks', 'callbackdat', 'dat'], 'audio_callbacks')
conectado = False
if sala.par.Usarmic.eval():
    if nivel >= 21 and has_par(fase1, 'Chopmic'):
        fase1.par.Fuentemic = 'chop'
        fase1.par.Chopmic = audio.path
        conectado = True
        ok('microfono virtual: FASE1 lo oye (Fuentemic = chop, Chopmic = %s)' % audio.path)
    else:
        info('microfono virtual: FASE1 esta en la fase %d; con la fase 21 v2 lo oira por '
             'Fuentemic = chop' % nivel)
else:
    info('microfono virtual: Usarmic apagado; FASE1 sigue con su Fuentemic')

# latido y botones
latido = get_or_make(sala, 'executeDAT', 'latido_sala', -880, 320)
latido.text = LATIDO_SALA
latido.store('err', False)
setp(latido, 'active', True)
setp_any(latido, ['framestart', 'onframestart'], True)
pulsos = get_or_make(sala, 'parameterexecuteDAT', 'pulsos_sala', -880, 440)
pulsos.text = PULSOS_SALA
setp(pulsos, 'active', True)
setp_any(pulsos, ['op', 'ops'], sala.path)
setp_any(pulsos, ['pars'], '*')
setp_any(pulsos, ['custom'], True)
setp_any(pulsos, ['builtin'], False)
setp_any(pulsos, ['onpulse'], True)
ok('latido_sala y pulsos_sala: la sala avanza cada fotograma; Palmada y Reiniciarsala')

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    guarda = {}
    for o, nm in ((sala, 'Personas'), (sala, 'Ruidopublico'), (sala, 'Volumendrone'), (sala, 'Modoluz'),
                  (sala, 'Hzprueba'), (sala, 'Activa'), (fase1, 'Fuentemic'), (fase1, 'Chopmic')):
        try:
            guarda[(o, nm)] = getattr(o.par, nm).eval()
        except Exception:
            pass
    t0 = sm._SALA['t0']
    try:
        _prueba(t, t.m)
    finally:
        for (o, nm), v in guarda.items():
            try:
                getattr(o.par, nm).val = v
            except Exception:
                pass
        sm._SALA.update(t0=t0, forzar=False, audio=None)
        sm._PLANES.clear()
        t.m.mic_reset()


def _prueba(t, m):
    sala.par.Activa = True
    c = sm.cfg()
    eq = sm.equipos()
    por = dict((tp, [e for e in eq if e['tipo'] == tp]) for tp in sm.TIPOS)
    esf = por['esfera'][0] if por['esfera'] else None
    hx, hz = c['ancho'] / 2.0, c['fondo'] / 2.0

    # 1. los equipos
    t.check('equipos: la esfera en una esquina del fondo, el sub debajo, 4 altavoces colgados, el micro '
            'en lo alto, la camara a 3,5 m, 4 focos y 1 estrobo',
            esf is not None and esf['z'] < -hz + 1.5 and abs(esf['x']) > hx - 1.5
            and len(por['sub']) == 1 and distancia_xz(por['sub'][0], esf) < 0.3 and por['sub'][0]['y'] < esf['y']
            and len(por['altavoz']) == 4 and all(e['y'] >= 2.5 for e in por['altavoz'])
            and len(por['micro']) == 1 and por['micro'][0]['y'] >= 2.5
            and len(por['camara']) == 1 and abs(por['camara'][0]['y'] - 3.5) < 0.3
            and len(por['foco']) == 4 and len(por['estrobo']) == 1,
            '%d filas' % len(eq))
    malos = [e['nombre'] for e in por['foco'] if esf is not None and sm.foco_alcanza(e, esf['pos'], 0.5 * esf['tam'])]
    t.check('ningun foco de bano apunta a la esfera', not malos, ' '.join(malos))
    mic = por['micro'][0]['pos']
    t.check('el micro, lejos del estrobo y del sub (mas de 3 m)',
            sm.distancia(mic, por['estrobo'][0]['pos']) > 3.0 and sm.distancia(mic, por['sub'][0]['pos']) > 3.0)
    t.check('una luz por foco y por estrobo', all(sala.op('luz_' + e['nombre']) is not None
                                                 for e in por['foco'] + por['estrobo']))

    # 2. las personas
    sala.par.Personas = 8
    c = sm.cfg()
    ev = sm.evitar_de(eq)
    sm._PLANES.clear()
    dentro, lejos, quietos, mueven = True, True, 0, 0
    for k in range(400):
        tt = 60.0 + 1.5 * k
        for i, x, z, h, andando in sm.personas(c, tt, ev):
            dentro = dentro and abs(x) <= hx - 0.3 and abs(z) <= hz
            lejos = lejos and all(math.hypot(x - p[0], z - p[2]) > 0.9 for p in ev)
            mueven += 1 if andando else 0
            quietos += 0 if andando else 1
    n1 = sm.personas(c, 90.0, ev)
    sm._PLANES.clear()
    n2 = sm.personas(c, 90.0, ev)
    t.check('las personas entran, pasean y se paran dentro de la sala, lejos de la esfera y del estrobo',
            dentro and lejos and quietos > 0 and mueven > 0 and 0 < len(n1) <= 8,
            '%d dentro a los 90 s' % len(n1))
    t.check('sin azar: la misma sala da la misma historia', n1 == n2)
    p0 = sm.posicion(c, 0, 0.0, ev)
    entradas = [s for k, s in enumerate(sm.plan(c, 3, 300.0, ev)) if s[4] and not sm.plan(c, 3, 300.0, ev)[k - 1][4]]
    t.check('nadie esta dentro antes de llegar; se entra por la puerta',
            p0 is None and entradas and all(s[2] == (0.0, hz) for s in entradas), '%d entradas' % len(entradas))

    # 3. lo que oye el microfono
    import numpy as np
    sala.par.Volumendrone = 0.5
    c = sm.cfg()
    R, n = sm.RATE, 735

    def flujos(evs, bloques=60, desde=0.0):
        m.mic_reset()
        W = m.new_world()
        cm = m.cfg()
        fl, ons = [], 0
        for k in range(bloques):
            ta = desde + k * n / float(R)
            x = sm.bloque_audio(c, eq, ta, n, R, [e for e in evs if ta - 0.5 <= e[0] < ta + n / float(R)])
            r = m.mic_bloque(W, cm, x, R, 1000.0 + ta)
            fl.append(r['flujo'])
            ons += 1 if r['onset'] else 0
        return fl, ons
    _, solo_drone = flujos([], bloques=300)
    cerca = (mic[0] + 0.5, sm.BOCA, mic[2])
    lejos_p = (-hx + 0.8, sm.BOCA, -hz + 1.8)          # al otro lado, junto a la esfera
    fc, oc = flujos([(0.5, 'palmada', cerca, 1)])
    fl_, ol = flujos([(0.5, 'palmada', lejos_p, 1)])
    t.check('el drone de los altavoces y el sub (5 s) no da onsets', solo_drone == 0)
    t.check('una palmada junto al micro da un onset y llega con mas flujo que una al otro lado de la sala',
            oc == 1 and max(fc) > max(fl_), '%.2f cerca, %.2f lejos (%.1f m)'
            % (max(fc), max(fl_), sm.distancia(lejos_p, mic)))
    d = sm.distancia(cerca, mic)
    x = sm.bloque_audio(dict(c, volumen_drone=0.0), eq, 0.0, 4410, R, [(0.0, 'palmada', cerca, 1)])
    llega = int(np.argmax(np.abs(x) > 1e-4))
    t.check('el sonido llega con su retardo (d / 343 m/s)', abs(llega - d / sm.VEL_SONIDO * R) <= 2,
            '%d muestras para %.2f m' % (llega, d))

    # 4. la luz de prueba
    sala.par.Modoluz = 'prueba'
    sala.par.Hzprueba = 3.0
    c = sm.cfg()
    est = por['estrobo'][0]
    fl_t = [sm.luz_de(c, est, 40.0 + j / 300.0) for j in range(int(20 * 300))]
    on = [40.0 + j / 300.0 for j, l in enumerate(fl_t) if l[3] > 0 and (j == 0 or fl_t[j - 1][3] == 0)]
    peor = max(sum(1 for x in on if a <= x < a + 1.0) for a in on) if on else 0
    blanco = all(l[0] == l[1] == l[2] for l in fl_t if l[3] > 0)
    t.check('estrobo: solo blanco y como mucho 3 destellos en cualquier ventana de 1 s',
            on and blanco and peor <= 3, '%d destellos en 20 s, %d en el peor segundo' % (len(on), peor))
    f = por['foco'][0]
    dep, ten = sm.luz_de(c, f, 5.0), sm.luz_de(c, f, 39.0)
    t.check('deposito: ambar tenue; tension: sube y vira a blanco frio',
            dep[0] > dep[1] > dep[2] and dep[3] < 0.3 and ten[2] >= ten[0] - 0.25 and ten[3] > dep[3])
    t.check('con el estrobo encendido el publico hace mas ruido (Reaccion)',
            sm.estrobo_activo(c, 45.0) and not sm.estrobo_activo(c, 5.0))

    # 5. la camara cenital y la esfera
    t.check('render_cenital (320 x 288) y profundidad, para la fase 22',
            sala.op('render_cenital') is not None and sala.op('profundidad') is not None)
    t.check('la esfera lleva la imagen de FASE1', bool(imagen))

    # 6. FASE1 oye el microfono virtual
    if conectado:
        W = m.world()
        m.mic_reset()
        sala.par.Personas = 0
        fase1.par.Fuentemic = 'chop'
        fase1.par.Chopmic = audio.path
        sm._SALA['forzar'] = True
        for _ in range(3):
            sm._SALA['forzar'] = True
            m.mic_tick(W, m.cfg(), absTime.seconds + 500.0)
        antes = W['mic']['n']
        sm.palmada((mic[0] + 0.5, sm.BOCA, mic[2]))
        m.mic_tick(W, m.cfg(), absTime.seconds + 500.5)
        t.check('Palmada: FASE1 la oye por audio_mic y cuenta un onset', W['mic']['n'] == antes + 1,
                'onsets %d -> %d' % (antes, W['mic']['n']))
    t.check('leyenda SALA', sm.legend().startswith('SALA') and 'personas' in sm.legend())


def distancia_xz(a, b):
    return math.hypot(a['x'] - b['x'], a['z'] - b['z'])


run_test(fase1, prueba)
print('  Ahora: mira render_sala (Vista libre, Orbita). Palmada: la oye FASE1. Personas y')
print('  Ruidopublico para mas o menos publico; Modoluz = prueba recorre la luz en un minuto.')
print('  ' + sm.legend())
print('=' * 66)
