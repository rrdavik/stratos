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
  LUZ          una Light COMP por foco y por estrobo (luz_<nombre>), con
               sombra: el publico la proyecta. Modoluz = prueba recorre en un
               minuto deposito, tension y erosion dominante (estrobo blanco,
               Hzprueba, como mucho 3 Hz). Con Bruma, cada haz se ve en el aire
               (haces: un cono aditivo del color de su luz, del aparato al
               suelo). La esfera es una luz mas (luz_esfera): ilumina lo que
               tiene cerca con el color medio de lo que muestra. Luzcasa, una
               luz tenue para ver la sala con los focos apagados (0,06: la
               sala, a oscuras como la de verdad).
  ESFERA       la imagen de FASE1 (su Render TOP 'render') sobre una esfera.
               OJO: la esfera real pide un mapa equirectangular 2:1, que
               Estratos aun no saca; aqui se ve la vista de la camara del
               planeta envolviendo la esfera.
  MONITOR (v2) una sola imagen para mirarlo todo: salida_sala (o el Null
               monitor_sala, 1280 x 720). En grande, la sala desde la Vista:
                 visitante  los ojos de un visitante (1,65 m) que pasea
                            despacio entre el publico mirando la esfera
                 entrada    de pie junto a la puerta
                 orbita     desde fuera (Orbita, Distancia, Alturavista)
                 cenital    lo que ve la camara del techo
               Encima: el plano de la sala desde arriba, con el publico y los
               focos (abajo a la derecha), lo que muestra la esfera (arriba a
               la derecha) y el rotulo con la luz, el publico y los onsets
               (arriba a la izquierda). render_cenital (320 x 288) y
               'profundidad' siguen ahi para la fase 22: no hace falta
               mirarlos.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/sala_virtual.py').read())
  Mira salida_sala (o monitor_sala): todo en una imagen. En la pagina Sala:
  Vista, Bruma, Modoluz, Palmada (una palmada junto al micro), Personas,
  Ruidopublico. El rotulo cuenta los onsets del publico virtual.
=============================================================================
"""

import math

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'sala_virtual v2  (estar en la sala: un monitor, vista de visitante, haces en la bruma y sombras)'
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
add_par(sala, page, 'float', 'Luzcasa', 'Luz de casa (para ver la sala a oscuras)', 0.06, 0.0, 1.0, clamp=True)
renew_default(sala, 'Luzcasa', 0.25, 0.06)          # v2: la sala, a oscuras como la de verdad
add_par(sala, page, 'float', 'Bruma', 'Bruma: los haces de los focos se ven (0 = aire limpio)', 0.5, 0.0, 1.0,
        clamp=True)
VISTAS_ETIQUETAS = ['Visitante (pasea entre el publico)', 'De pie en la entrada', 'Orbita (desde fuera)',
                    'Camara cenital']
add_par(sala, page, 'menu', 'Vista', 'Vista del monitor', 'visitante', menu=sm.VISTAS,
        menu_labels=VISTAS_ETIQUETAS)
try:                                    # v2: libre pasa a llamarse orbita y el defecto es visitante
    vp = sala.par.Vista
    if list(vp.menuNames) != list(sm.VISTAS):
        antes = str(vp.eval())
        vp.menuNames = list(sm.VISTAS)
        vp.menuLabels = VISTAS_ETIQUETAS
        vp.default = 'visitante'
        vp.val = 'cenital' if antes == 'cenital' else 'visitante'
        vp.label = 'Vista del monitor'
        ok('Vista: visitante (pasea entre el publico), entrada, orbita (la libre de antes) y cenital')
except Exception as e:
    info('Vista: no pude poner las vistas nuevas (%s)' % e)
add_par(sala, page, 'float', 'Orbita', 'Vista libre: giro (grados)', 30.0, -180.0, 180.0)
add_par(sala, page, 'float', 'Distancia', 'Vista libre: distancia (m)', 11.0, 3.0, 40.0)
add_par(sala, page, 'float', 'Alturavista', 'Vista libre: altura (m)', 5.0, 0.5, 20.0)
ok('pagina Sala: Activa, Ancho 8, Fondo 6, Alto 4, Zonaancho 5,4, Zonafondo 4,5, Recolocar, Personas 6, '
   'Llegada 8, Ruidopublico 0,05, Reaccion 3, Volumendrone 0,5, Palmada, Reiniciarsala, Usarmic, '
   'Modoluz (prueba), Hzprueba 2,5, Luzcasa 0,06, Bruma 0,5, Vista (visitante), Orbita, Distancia, '
   'Alturavista (las tres, solo con Vista = orbita)')

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


def instanciado(name, x, y, mat, sop='box'):
    """Geometry COMP 'name' instanciada desde el Script CHOP 'i_name': una caja
    de 1 x 1 x 1 con la base en y = 0, una esfera de diametro 1 centrada
    (sop='sphere') o un cono abierto de diametro 1 y largo 1 con la punta en
    el origen hacia -Z, como la luz de una Light COMP (sop='haz')."""
    chop = get_or_make(sala, 'scriptCHOP', 'i_' + name, x - 220, y)
    setp_any(chop, ['callbacks', 'callbackdat', 'dat'], 'instancias_sala')
    geo = fresh(sala, 'geometryCOMP', name, x, y)
    for k in list(geo.children):
        try:
            k.render = False
            k.display = False
        except Exception:
            pass
    if sop == 'sphere':
        s = mk(geo, 'sphereSOP', 'bola', 0, 0)
        for ax in ('radx', 'rady', 'radz'):
            setp(s, ax, 0.5)
        setp_any(s, ['type', 'primtype'], 'polymesh')
        setp_any(s, ['rows'], 12)
        setp_any(s, ['cols'], 16)
    elif sop == 'haz':
        cono = mk(geo, 'tubeSOP', 'cono', 0, 120)
        setp_any(cono, ['rad1'], 0.5)
        setp_any(cono, ['rad2'], 0.0)
        setp(cono, 'height', 1.0)
        setp_any(cono, ['cols', 'columns'], 24)
        setp_any(cono, ['rows'], 2)
        setp_any(cono, ['caps', 'endcaps', 'capends'], False)
        setmenu(cono, ['orient', 'orientation'], ['y'], 1)
        arriba = punta_arriba(geo, cono)        # la punta en +Y, la base en -Y
        s = mk(geo, 'transformSOP', 'a_la_luz', 200, 0)
        connect(s, arriba, 0)
        setp(s, 'ty', -0.5)                     # la punta en el origen...
        setp(s, 'rx', 90.0)                     # ...y el cono hacia -Z
        setmenu(s, ['xord'], ['trs'], None)     # primero baja, luego gira
    else:
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
# v2: la sala a oscuras; el suelo, algo brillante (refleja la esfera y los focos)
make_phong(sala, 'mat_sala', 660, 200, spec=0.18, shin=12, diff=0.9, amb=0.03)
make_phong(sala, 'mat_equipos', 660, 120, spec=0.5, shin=20, diff=1.0, amb=0.03, emit=0.15)
make_phong(sala, 'mat_personas', 660, 40, spec=0.05, shin=2, diff=0.9, amb=0.02)
mat_haz = make_constant(sala, 'mat_haz', 660, 440, (1.0, 1.0, 1.0))
set_additive(mat_haz)
setmenu(mat_haz, ['cullface', 'cull'], ['neither', 'none', 'off'], None)
instanciado('sala_caja', 0, 200, 'mat_sala')
instanciado('equipos_geo', 0, 120, 'mat_equipos')
instanciado('personas', 0, 40, 'mat_personas')
instanciado('cabezas', 0, -120, 'mat_personas', sop='sphere')
instanciado('haces', 0, 440, 'mat_haz', sop='haz')
ok('sala_caja, equipos_geo, personas y cabezas: suelo, paredes, zona de la camara, puerta, aparatos y '
   'publico; haces: la luz de cada foco y del estrobo en la bruma (Bruma)')

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
# v2: la imagen de la esfera, pequena, para el monitor y para medir su color medio
mini = get_or_make(sala, 'resolutionTOP', 'esfera_mini', 880, -40)
connect(mini, fase1.op('render'), 0)
setmenu(mini, ['outputresolution', 'resolution'], ['custom'], None)
setp_any(mini, ['resolutionw'], 320)
setp_any(mini, ['resolutionh'], 180)
media = get_or_make(sala, 'resolutionTOP', 'esfera_media', 1100, -40)
connect(media, mini, 0)
setmenu(media, ['outputresolution', 'resolution'], ['custom'], None)
setp_any(media, ['resolutionw'], 8)
setp_any(media, ['resolutionh'], 8)

# las luces: una por foco y por estrobo de la tabla, la de la esfera y la de casa
for o in [o for o in sala.children if o.name.startswith('luz_')]:
    o.destroy()
luces = []
sombras = 0
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
    if setmenu(l, ['shadowtype'], ['soft', 'soft2d', 'hard', 'hard2d'], None):   # v2: el publico da sombra
        sombras += 1
    luces.append(l.name)
le = mk(sala, 'lightCOMP', 'luz_esfera', 220, 360)
setmenu(le, ['lighttype'], ['point'], 0)
for ax in ('tx', 'ty', 'tz'):
    setexpr(le, ax, "%s.luz_esfera('%s', absTime.frame)" % (SM, ax))
color_luz_expr(le, ["%s.luz_esfera('%s', absTime.frame)" % (SM, ch) for ch in 'rgb'])
setexpr(le, 'dimmer', "%s.luz_esfera('d', absTime.frame)" % SM)
atenua = setp_any(le, ['attenuated', 'attenuation'], True)
setp_any(le, ['attenuationstart', 'attenstart'], 0.6)
setp_any(le, ['attenuationend', 'attenend'], 6.0)
luces.append(le.name)
casa = mk(sala, 'lightCOMP', 'luz_casa', 220, 280)
setmenu(casa, ['lighttype'], ['point'], 0)
setp(casa, 'ty', 3.8)
setexpr(casa, 'dimmer', "float(parent().par.Luzcasa)")
luces.append(casa.name)
ok('luces: %s (conos desde la tabla; Modoluz las enciende; la esfera ilumina la sala con el color '
   'medio de su imagen)' % ' '.join(luces))
if not sombras:
    info('luces: no encontre Shadow Type en las Light COMP; para que el publico de sombra, '
         'pon Shadow Type = Soft a mano en los luz_foco y luz_estrobo')
if not atenua:
    info('luz_esfera: no encontre la atenuacion; ponla a mano (Attenuated, de 0,6 a 6 m)')

# las camaras y los renders
mirada = get_or_make(sala, 'nullCOMP', 'mirada', 440, 360)
for ax, m_ in (('tx', 'mx'), ('ty', 'my'), ('tz', 'mz')):
    setexpr(mirada, ax, "%s.vista('%s', absTime.frame)" % (SM, m_))
vieja = sala.op('centro')
if vieja is not None:
    vieja.destroy()
vista = get_or_make(sala, 'cameraCOMP', 'vista', 440, 280)
for ax in ('tx', 'ty', 'tz'):
    setexpr(vista, ax, "%s.vista('%s', absTime.frame)" % (SM, ax))
setp(vista, 'lookat', 'mirada')
setexpr(vista, 'fov', "%s.vista('fov', absTime.frame)" % SM)
cenital = get_or_make(sala, 'cameraCOMP', 'vista_cenital', 440, 200)
for ax in ('tx', 'ty', 'tz'):
    setexpr(cenital, ax, "%s.valor('camara', '%s', absTime.frame)" % (SM, ax))
setp(cenital, 'rx', -90.0)
setp(cenital, 'fov', 75.0)                  # Femto Bolt, NFOV: unos 75 x 65 grados
plano = get_or_make(sala, 'cameraCOMP', 'vista_plano', 440, 120)
setp(plano, 'rx', -90.0)
setexpr(plano, 'ty', "%s.plano('ty', absTime.frame)" % SM)
orto = setmenu(plano, ['projection'], ['ortho', 'orthographic'], None)
setexpr(plano, 'orthowidth', "%s.plano('ancho', absTime.frame)" % SM)
geos = 'sala_caja equipos_geo personas cabezas esfera haces'
r1 = get_or_make(sala, 'renderTOP', 'render_sala', 660, 360)
setexpr(r1, 'camera', "'vista_cenital' if str(parent().par.Vista) == 'cenital' else 'vista'")
setp(r1, 'geometry', geos)
setp(r1, 'lights', ' '.join(luces))
setp_any(r1, ['resolutionw'], 1280)
setp_any(r1, ['resolutionh'], 720)
setp_any(r1, ['bgcolorr'], 0.0)
setp_any(r1, ['bgcolorg'], 0.0)
setp_any(r1, ['bgcolorb'], 0.0)
setp_any(r1, ['antialias'], 'aa4x')
luz_plano = get_or_make(sala, 'lightCOMP', 'plano_luz', 220, 440)      # solo para el plano: que se lea
setmenu(luz_plano, ['lighttype'], ['distant'], 2)
setp(luz_plano, 'rx', -60.0)
setp(luz_plano, 'dimmer', 0.5)
rp = get_or_make(sala, 'renderTOP', 'render_plano', 660, 120)
setp(rp, 'camera', 'vista_plano')
setp(rp, 'geometry', 'sala_caja equipos_geo personas cabezas esfera')
setp(rp, 'lights', ' '.join(luces + ['plano_luz']))
setp_any(rp, ['resolutionw'], 320)
setp_any(rp, ['resolutionh'], 240)
r2 = get_or_make(sala, 'renderTOP', 'render_cenital', 660, 280)
setp(r2, 'camera', 'vista_cenital')
setp(r2, 'geometry', 'sala_caja personas cabezas')
setp(r2, 'lights', 'luz_casa')
setp_any(r2, ['resolutionw'], 320)
setp_any(r2, ['resolutionh'], 288)
prof = get_or_make(sala, 'depthTOP', 'profundidad', 880, 280)
connect(prof, r2, 0)
if not orto:
    info('vista_plano: no encontre Projection = Orthographic; el plano saldra en perspectiva')

# v2: el monitor, una sola imagen con todo: la sala en grande (Vista) y, encima,
# el plano (abajo a la derecha), lo que muestra la esfera (arriba a la derecha) y
# el rotulo (arriba a la izquierda). Es lo que hay que mirar: salida_sala.
MONITOR_TXT = "parent().op('sala_motor').module.texto_monitor(absTime.frame)"
rot = get_or_make(sala, 'textTOP', 'rotulo_sala', 880, 520)
setp_any(rot, ['resolutionw'], 1280)
setp_any(rot, ['resolutionh'], 720)
transparente = setp_any(rot, ['bgalpha', 'backgroundalpha', 'bgcolora'], 0.0)
setp_any(rot, ['font', 'fontfamily'], 'Consolas')
setp_any(rot, ['fontsizex', 'fontsize'], 12)
setp(rot, 'fontsizey', 12)
setp_any(rot, ['alignx'], 'left')
setp_any(rot, ['aligny'], 'top')
setp_any(rot, ['positionx', 'textx'], 16)
setp_any(rot, ['positiony', 'texty'], -16)
setexpr(rot, 'text', MONITOR_TXT)


def encima(nombre, arriba, abajo, horiz, vert, x, y):
    """Over TOP: 'arriba' a su tamano, en la esquina (horiz, vert) de 'abajo',
    a 16 px del borde. Devuelve si pudo colocarlo."""
    o = get_or_make(sala, 'overTOP', nombre, x, y)
    connect(o, arriba, 0)
    connect(o, abajo, 1)
    bien = [setmenu(o, ['size', 'outputresolution'], ['input2', 'in2'], None),
            setmenu(o, ['prefit'], ['nativeres', 'native'], None),
            setmenu(o, ['justifyh'], [horiz], None),
            setmenu(o, ['justifyv'], [vert], None)]
    setmenu(o, ['tunit'], ['pixels'], None)
    setp(o, 'tx', -16 if horiz == 'right' else 16)
    setp(o, 'ty', 16 if vert == 'bottom' else -16)
    return all(bien)


colocados = [encima('con_plano', rp, r1, 'right', 'bottom', 880, 360),
             encima('con_esfera', mini, sala.op('con_plano'), 'right', 'top', 1100, 360)]
if transparente:
    con_rotulo = get_or_make(sala, 'overTOP', 'con_rotulo', 1320, 360)
    connect(con_rotulo, rot, 0)
    connect(con_rotulo, sala.op('con_esfera'), 1)
    ultimo = con_rotulo
else:
    ultimo = sala.op('con_esfera')
    info('rotulo_sala: no pude hacer transparente su fondo; el rotulo se ve en su nodo')
monitor = get_or_make(sala, 'nullTOP', 'monitor_sala', 1540, 360)
connect(monitor, ultimo, 0)
salida = get_or_make(sala, 'outTOP', 'salida_sala', 1760, 360)
connect(salida, monitor, 0)
for o in (monitor, salida):
    try:
        o.color = (0.1, 0.8, 0.9)
    except Exception:
        pass
if all(colocados):
    ok('monitor_sala (y salida_sala): la sala en grande desde la Vista, con el plano, la esfera y el '
       'rotulo encima. Es lo unico que hay que mirar')
else:
    info('monitor_sala: no pude colocar el plano o la esfera en su esquina (Over TOP: Size = Input 2, '
         'Prefit = Native Resolution, Justify); revisalo en con_plano y con_esfera')
ok('render_cenital (320 x 288) y profundidad: la camara del techo, para la fase 22 (no hace falta mirarlos)')

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
                  (sala, 'Hzprueba'), (sala, 'Activa'), (sala, 'Vista'), (sala, 'Bruma'),
                  (fase1, 'Fuentemic'), (fase1, 'Chopmic')):
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

    # 5b. v2: estar en la sala
    t.check('un monitor con todo: salida_sala <- monitor_sala, con el plano, la esfera y el rotulo encima',
            sala.op('salida_sala') is not None and sala.op('monitor_sala') is not None
            and all(sala.op(nm) is not None for nm in ('con_plano', 'con_esfera', 'render_plano',
                                                       'esfera_mini', 'rotulo_sala')))
    sala.par.Vista = 'visitante'
    c = sm.cfg()
    ev = sm.evitar_de(eq)
    pasos = [sm.paseo_visitante(c, 7.0 * k, ev) for k in range(80)]
    vel = max(math.hypot(b[0] - a[0], b[1] - a[1]) / 7.0 for a, b in zip(pasos, pasos[1:]))
    t.check('visitante: pasea dentro de la sala, lejos de la esfera y del estrobo, sin correr',
            all(abs(x) <= hx and abs(z) <= hz for x, z in pasos)
            and all(math.hypot(x - p[0], z - p[2]) > 0.9 for x, z in pasos[1:] for p in ev)
            and len(set(pasos)) > 5 and vel <= 1.5 * sm.VEL_VISITANTE < sm.VELOCIDAD,
            '%.2f m/s como mucho (arranca y frena suave)' % vel)
    p, mira = sm.ojos(c)
    t.check('visitante: los ojos a 1,65 m y mirando la esfera',
            abs(p[1] - sm.OJOS) < 1e-9 and esf is not None and mira == esf['pos'])
    t.check('el monitor mira por la camara de la Vista', sm.vista('ty') == sm.OJOS
            and abs(sm.vista('mx') - esf['pos'][0]) < 1e-9)
    sala.par.Vista = 'orbita'
    t.check('orbita: desde fuera, como la vista libre de antes', sm.vista('ty') == float(sala.par.Alturavista))
    sala.par.Vista = 'visitante'
    sala.par.Personas = 4
    c = sm.cfg()
    ps = sm.personas(c, 120.0, ev)
    cab = sm._filas_cabezas(c, eq, 120.0)
    cue = sm._filas_personas(c, eq, 120.0)
    t.check('el publico tiene cabeza: una por persona, encima de su cuerpo',
            len(cab) == len(cue) == len(ps) > 0
            and all(abs(k[1] - (q[7] + 0.04 + 0.5 * sm.CABEZA)) < 1e-6 for k, q in zip(cab, cue)))
    sala.par.Modoluz = 'prueba'
    sala.par.Bruma = 0.5
    c = sm.cfg()
    luminosos = [e for e in eq if e['tipo'] in ('foco', 'estrobo') and sm.luz_de(c, e, 5.0)[3] > 0]
    hz5 = sm._filas_haces(c, eq, 5.0)
    f0 = por['foco'][0]
    largo, diam = sm.haz(f0)
    t.check('Bruma: un haz por aparato encendido, del color de su luz, del aparato al suelo',
            len(hz5) == len(luminosos) > 0 and hz5[0][9] > hz5[0][11]
            and abs(largo * -sm._largo(f0['eje']) ** -1 * f0['eje'][1] - f0['y']) < 1e-6,
            '%d haces, el primero de %.1f m' % (len(hz5), largo))
    t.check('sin Bruma o con la luz apagada, ningun haz',
            not sm._filas_haces(dict(c, bruma=0.0), eq, 5.0)
            and not sm._filas_haces(dict(c, modo_luz=0), eq, 5.0))
    t.check('la esfera es una luz: luz_esfera, en su sitio y con el color medio de su imagen',
            sala.op('luz_esfera') is not None and abs(sm.luz_esfera('ty') - esf['y']) < 1e-9
            and all(0.0 <= sm.luz_esfera(ch) <= 1.0 for ch in 'rgb'))
    t.check('el rotulo del monitor: la sala, la luz y la vista',
            'SALA' in sm.texto_monitor() and 'LUZ' in sm.texto_monitor() and 'visitante' in sm.texto_monitor())

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
print('  Ahora: mira salida_sala (todo en una imagen; Vista = visitante, entrada, orbita o')
print('  cenital). Modoluz = prueba recorre la luz en un minuto; Bruma, los haces en el aire.')
print('  Palmada: la oye FASE1. Personas y Ruidopublico para mas o menos publico.')
print('  ' + sm.legend())
print('=' * 66)
