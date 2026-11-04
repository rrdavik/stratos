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
               (la de la entrada, abierta para mirar) y la puerta en el centro
               de la de delante. v8: la camara cenital ve todo el suelo (hasta
               la v7 solo una zona, Zonaancho x Zonafondo, con tarima y borde).
               v4: dibujada con lineas (geometria 'lineas', Constant MAT, se
               ve a oscuras): las doce aristas, el umbral de la puerta, una
               reticula de 1 m en las paredes y una de 0,5 m en todo el suelo.
  EQUIPOS      la tabla 'equipos' (editable; relanzar no la pisa): la esfera
               de LEDs de 1 m en la esquina del fondo a la izquierda (v5: a
               1 m de cada pared; si no lo esta, se rehace la tabla), sobre su
               peana con el subwoofer dentro; cuatro altavoces colgados en las
               esquinas; el microfono en lo alto, hacia el centro y lejos de la
               esfera y del estrobo; la camara cenital a 3,5 m; cuatro focos
               de bano (dos junto a la esfera, sin apuntarle) y el
               estroboscopio en el suelo junto a la esfera. Recolocar la
               rehace con las medidas de ahora.
  PERSONAS     Personas (6), sin azar, segun la Demo (v5):
                 paseo  entran por la puerta cada Llegada s (8), pasean, se
                        paran dentro del suelo del publico y se van
                 grupo  entran juntos en fila, hacen corro ante la esfera,
                        se quedan casi un minuto y salen juntos
                 llena  la sala se llena deprisa y se quedan casi quietos
                 goteo  de uno en uno: van a la esfera, miran y se van
                 vacia  nadie
               Cada persona es un tronco de su altura (v5: sin cabeza).
               Hacen ruido: pasos al andar y palmadas o toses (Ruidopublico por segundo y persona;
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
               tiene cerca con el color medio de lo que muestra, con
               Luzesfera (v5: 0 por defecto; dejaba una mancha en la pared). Luzcasa, una
               luz tenue para ver la sala con los focos apagados (0,06: la
               sala, a oscuras como la de verdad).
  ESFERA       la imagen de FASE1 (su Render TOP 'render') sobre una esfera.
               v3: sale de FASE1 por el Out TOP 'out_render' y SALA la coge
               con el Select TOP 'imagen_fase1' (no se puede cablear entre
               redes).
               OJO: la esfera real pide un mapa equirectangular 2:1, que
               Estratos aun no saca; aqui se ve la vista de la camara del
               planeta envolviendo la esfera.
  MONITOR (v2) una sola imagen para mirarlo todo: salida_sala (o el Null
               monitor_sala, 1280 x 720). En grande, la sala desde la Vista:
                 entrada    (v4, por defecto) desde detras de la puerta, a
                            2,8 m, mirando al fondo: el suelo del publico
                            entero, la esfera en su esquina y las paredes
                            en perspectiva
                 visitante  los ojos de un visitante (1,65 m) que pasea
                            despacio entre el publico mirando la esfera
                 orbita     desde fuera (Orbita, Distancia, Alturavista)
                 cenital    lo que ve la camara del techo
               Encima: lo que ve la camara cenital, toda la planta de la sala
               con el publico (abajo a la derecha, 200 x 180; v10, antes un
               plano ortografico aparte de 320 x 240) y el rotulo con la luz, el publico y los onsets
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

VERSION = 'sala_virtual v18  (el planeta se inclina hacia la camara de la entrada: Inclinasfera)'
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

# v17: otras salas (copias de SALA con otro nombre, como 'salap'). Este script solo usa
# /project1/SALA; una copia sigue moviendo su publico y dibujando su render cada
# fotograma. Se paran su latido y sus botones (no se borran) y se avisa.
copias = []
for o_ in op('/project1').children:
    try:
        es_copia = o_.isCOMP and o_.path != sala.path and o_.op('sala_motor') is not None
    except Exception:
        es_copia = False
    if es_copia:
        copias.append(o_.path)
        for nm in ('latido_sala', 'pulsos_sala'):
            d = o_.op(nm)
            if d is not None:
                setp(d, 'active', False)
if copias:
    info('OTRA SALA: %s es una copia de SALA (no la crea este script). Su latido y sus botones quedan '
         'parados; si no tiene nada tuyo, borrala' % ', '.join(copias))

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
for viejo in ('Zonaancho', 'Zonafondo'):           # v8: sin zona; la camara ve todo el suelo
    try:
        p_ = getattr(sala.par, viejo, None)
        if p_ is not None:
            p_.destroy()
            ok('%s: quitado (la camara cenital ve todo el suelo de la sala)' % viejo)
    except Exception as e:
        info('%s: no pude quitarlo (%s); ya no se usa' % (viejo, e))
add_par(sala, page, 'pulse', 'Recolocar', 'Recolocar los equipos con estas medidas (rehace la tabla)')
add_par(sala, page, 'int', 'Personas', 'Personas', 6, 0, 30, clamp=True)
add_par(sala, page, 'menu', 'Demo', 'Demo de visita del publico', 'paseo', menu=sm.DEMOS,
        menu_labels=sm.DEMOS_ETIQUETAS)
add_par(sala, page, 'float', 'Llegada', 'Paseo: segundos entre dos llegadas', 8.0, 0.0, 120.0, clamp=True)
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
add_par(sala, page, 'float', 'Luzesfera', 'Luz de la esfera sobre la sala (0 = apagada)', 0.0, 0.0, 1.0,
        clamp=True)
add_par(sala, page, 'toggle', 'Espejosfera', 'Esfera: voltear la imagen en horizontal (espejo)', False)
add_par(sala, page, 'toggle', 'Volteosfera', 'Esfera: voltear la imagen en vertical (boca abajo)', True)
try:                    # v16: el planeta estaba boca abajo, no en espejo (una vez por proyecto)
    if not sala.fetch('volteo_v16', False, search=False):
        sala.store('volteo_v16', True)
        sala.par.Espejosfera = False
        sala.par.Volteosfera = True
        sala.par.Espejosfera.default = False
except Exception as e:
    info('Espejosfera / Volteosfera: no pude ponerlos (%s); deja Espejosfera apagado y Volteosfera '
         'encendido' % e)
add_par(sala, page, 'float', 'Inclinasfera', 'Inclinacion de la esfera (grados hacia arriba; 0 = mira '
        'a la camara de la entrada)', 0.0, -90.0, 90.0)
add_par(sala, page, 'float', 'Girosfera', 'Giro de la esfera (grados; 0 = el planeta mira a la sala)', 0.0,
        -180.0, 180.0)
add_par(sala, page, 'float', 'Bruma', 'Bruma: los haces de los focos se ven (0 = aire limpio)', 0.5, 0.0, 1.0,
        clamp=True)
VISTAS_ETIQUETAS = ['Visitante (pasea entre el publico)', 'Entrada (la sala desde la puerta)', 'Orbita (desde fuera)',
                    'Camara cenital']
add_par(sala, page, 'menu', 'Vista', 'Vista del monitor', 'entrada', menu=sm.VISTAS,
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
try:                                    # v4: el defecto pasa a ser entrada (una vez por proyecto)
    vp = sala.par.Vista
    vp.default = 'entrada'
    vp.menuLabels = VISTAS_ETIQUETAS
    if not sala.fetch('vista_v4', False, search=False):
        sala.store('vista_v4', True)
        if str(vp.eval()) == 'visitante':
            vp.val = 'entrada'
            ok('Vista: entrada (desde la puerta, con el suelo del publico y la esfera en su esquina)')
except Exception as e:
    info('Vista: no pude poner entrada por defecto (%s)' % e)
add_par(sala, page, 'float', 'Orbita', 'Vista libre: giro (grados)', 30.0, -180.0, 180.0)
add_par(sala, page, 'float', 'Distancia', 'Vista libre: distancia (m)', 11.0, 3.0, 40.0)
add_par(sala, page, 'float', 'Alturavista', 'Vista libre: altura (m)', 5.0, 0.5, 20.0)
ok('pagina Sala: Activa, Ancho 8, Fondo 6, Alto 4, Recolocar, Personas 6, '
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
if not sm.esfera_en_esquina():          # v5: la esfera, en una esquina del fondo y a 1 m de cada pared
    sm.recolocar()
    ok('equipos: la esfera no estaba a 1 m de las paredes de su esquina; tabla rehecha (esfera al fondo a '
       'la izquierda, con su sub, su estrobo y los focos que la acompanan)')

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
make_constant(sala, 'mat_lineas', 660, 520, (1.0, 1.0, 1.0))      # v4: el dibujo de la sala, sin luz
set_additive(mat_haz)
setmenu(mat_haz, ['cullface', 'cull'], ['neither', 'none', 'off'], None)
instanciado('sala_caja', 0, 200, 'mat_sala')
instanciado('equipos_geo', 0, 120, 'mat_equipos')
instanciado('personas', 0, 40, 'mat_personas')
for vieja in ('cabezas', 'i_cabezas'):          # v5: el publico, sin cabeza
    if sala.op(vieja) is not None:
        sala.op(vieja).destroy()
instanciado('haces', 0, 440, 'mat_haz', sop='haz')
instanciado('lineas', 0, 520, 'mat_lineas')
ok('sala_caja, equipos_geo y personas (un tronco, sin cabeza): suelo, paredes, el suelo del publico, puerta, aparatos y '
   'publico; haces: la luz de cada foco y del estrobo en la bruma (Bruma); lineas: aristas, umbral de la '
   'puerta, reticula de 1 m y la del suelo del publico (0,5 m)')

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


def menu_por_texto(o, nombres, textos):
    """Pone el menu en la primera opcion cuyo nombre o etiqueta contenga uno de
    los textos. Devuelve la opcion elegida o None."""
    for n in nombres:
        p = getattr(o.par, n, None) if o is not None else None
        if p is None:
            continue
        try:
            opciones = list(zip(p.menuNames, p.menuLabels))
        except Exception:
            continue
        for tx in textos:
            for nm, et in opciones:
                if tx in str(nm).lower() or tx in str(et).lower():
                    p.val = nm
                    return nm
    return None


# v13: la esfera era una esfera primitiva de un solo punto (Primitive Type = prim: setp con
# 'polymesh' no casaba con ningun nombre del menu y no hacia nada). Sin vertices no hay
# coordenadas de textura y la bola salia gris lisa. Malla de poligonos, por nombre o etiqueta.
malla = (setmenu(bola, ['type', 'primtype'], ['polymesh', 'polygonmesh', 'mesh'], None)
         and bola.par.type.eval() != 'prim') or menu_por_texto(bola, ['type', 'primtype'], ['mesh', 'poly'])
try:
    puntos = len(bola.points)
except Exception:
    puntos = 0
if malla and puntos > 1:
    ok('esfera/bola: malla de poligonos (%s, %d puntos), con vertices para la imagen'
       % (bola.par.type.eval(), puntos))
else:
    info('esfera/bola: sigue siendo una esfera primitiva (%s puntos); pon a mano Primitive Type = '
         'Polygon Mesh o la esfera saldra gris' % puntos)
# v10: la Sphere SOP no da coordenadas de textura: sin ellas el Constant MAT lee un
# solo punto de la imagen y la esfera salia gris lisa. Un Texture SOP polar (eje Y)
# se las pone; el planeta queda en el centro de la imagen, de cara a giro_esfera.
uvs = mk(esfera, 'textureSOP', 'uvs', 0, -120)
connect(uvs, bola, 0)
proyeccion = menu_por_texto(uvs, ['type', 'texturetype'], ['polar', 'spher'])
setmenu(uvs, ['axis'], ['y'], 1)
# v18: dos Transform SOP tras las coordenadas de textura: 'centrar' lleva el centro de
# la imagen al +Z de la bola y 'inclinar' lo levanta hacia la camara de la entrada
# (antes el planeta parecia mirar al suelo). El giro hacia la entrada, en la esfera (ry).
centrar = mk(esfera, 'transformSOP', 'centrar', 0, -240)
connect(centrar, uvs, 0)
setexpr(centrar, 'ry', "parent(2).op('sala_motor').module.centro_esfera(absTime.frame)")
inclinar = mk(esfera, 'transformSOP', 'inclinar', 0, -360)
connect(inclinar, centrar, 0)
setexpr(inclinar, 'rx', "parent(2).op('sala_motor').module.inclina_esfera(absTime.frame)")
for o_, si in ((bola, False), (uvs, False), (centrar, False), (inclinar, True)):
    for attr in ('render', 'display'):
        try:
            setattr(o_, attr, si)
        except Exception:
            pass


def centro_imagen(sop):
    """v14: el angulo (grados, 0 = +Z, 90 = +X) del punto de la malla cuyas
    coordenadas de textura caen en el centro de la imagen (u, v = 0,5), o None."""
    mejor = None
    fuentes = []
    try:
        fuentes.append([(p_, p_) for p_ in sop.points])
    except Exception:
        pass
    try:
        fuentes.append([(v_, v_.point) for pr in sop.prims for v_ in pr])
    except Exception:
        pass
    for fuente in fuentes:
        for con_uv, punto in fuente:
            try:
                uv = con_uv.uv
                d = (float(uv[0]) - 0.5) ** 2 + (float(uv[1]) - 0.5) ** 2
                x, z = float(punto.x), float(punto.z)
            except Exception:
                break
            if math.hypot(x, z) > 1e-4 and (mejor is None or d < mejor[0]):
                mejor = (d, x, z)
        if mejor is not None:
            break
    if mejor is None or mejor[0] > 0.01:
        return None
    return math.degrees(math.atan2(mejor[1], mejor[2]))


try:
    uvs.cook(force=True)
except Exception:
    pass
ang = centro_imagen(uvs)
if ang is not None:
    sala.store('uv_centro', ang)
    ok('esfera: el centro de la imagen cae a %.0f grados en la bola; giro_esfera lo pone mirando a la '
       'entrada (Girosfera para retocar)' % ang)
else:
    sala.store('uv_centro', 0.0)
    info('esfera: no pude medir donde cae el centro de la imagen en la bola; se toma +Z. Si el planeta '
         'queda de lado, retoca Girosfera')
if proyeccion:
    ok('esfera: coordenadas de textura con un Texture SOP (%s, eje Y): el render de FASE1 se ve en la bola'
       % proyeccion)
else:
    info('esfera/uvs: no encontre la proyeccion polar del Texture SOP; ponla a mano (Texture Type = Polar, '
         'Axis = Y) o la esfera saldra gris')
for ax in ('tx', 'ty', 'tz'):
    setexpr(esfera, ax, "%s.valor('esfera', '%s', absTime.frame)" % (SM, ax))
setexpr(esfera, 'ry', "%s.giro_esfera(absTime.frame)" % SM)     # v9: el planeta mira a la sala
# v3: el render de FASE1 sale por un Out TOP ('out_render', sin el rotulo) y
# SALA lo recoge con un Select TOP ('imagen_fase1'). Antes se cableaba
# FASE1/render directo a esfera_mini, pero TouchDesigner no deja cablear entre
# redes distintas: el cable no se hacia y esfera_mini, esfera_media, con_esfera,
# con_rotulo y monitor_sala se quedaban en error por falta de entrada.
out_render = get_or_make(fase1, 'outTOP', 'out_render', 960, -300)
connect(out_render, fase1.op('render'), 0)
try:
    out_render.color = (0.1, 0.8, 0.9)
except Exception:
    pass
sel_fase1 = get_or_make(sala, 'selectTOP', 'imagen_fase1', 660, -120)
sale_render = setp_any(sel_fase1, ['top'], out_render.path)
if sale_render and out_render.inputs:
    ok('out_render: el render de FASE1 sale por un Out TOP; SALA lo coge con imagen_fase1 (Select TOP)')
else:
    info('out_render / imagen_fase1: revisa que %s este cableado a %s/render y que imagen_fase1 '
         'apunte a el' % (out_render.path, fase1.path))
# v7: sobre la esfera, solo el centro del render (el planeta, un cuadrado): el
# render entero, casi todo fondo oscuro, la dejaba gris
recorte = get_or_make(sala, 'cropTOP', 'esfera_imagen', 880, -120)
connect(recorte, sel_fase1, 0)
lado = 0.5 * (1.0 - 720.0 / 1280.0)
recortada = all([setp_any(recorte, ['cropleft'], lado), setp_any(recorte, ['cropright'], 1.0 - lado)])
if not recortada:
    info('esfera_imagen: no pude recortar el centro del render (Crop TOP: Left %.3f, Right %.3f)'
         % (lado, 1.0 - lado))
mat_esfera = make_constant(sala, 'mat_esfera', 660, -40, (1.0, 1.0, 1.0))
# v15: un Flip TOP entre el recorte y el material endereza el planeta (el centro de la
# imagen no se mueve al voltear, asi que el giro hacia la entrada no cambia).
espejo = get_or_make(sala, 'flipTOP', 'esfera_espejo', 1100, -120)
connect(espejo, recorte, 0)
# v16: el planeta salia boca abajo, no en espejo: el volteo de la v15 (horizontal) lo
# dejaba en espejo. Se voltea en vertical (Volteosfera) y no en horizontal
# (Espejosfera); los dos, en la pagina Sala para cambiarlos en directo.
volteada = (setexpr(espejo, 'flipx', "bool(parent().par.Espejosfera)")
            and setexpr(espejo, 'flipy', "bool(parent().par.Volteosfera)"))
if not volteada:
    info('esfera_espejo: no pude enlazar Flip X y Flip Y a Espejosfera y Volteosfera; ponlos a mano')
imagen = setp_any(mat_esfera, ['colormap', 'map'], 'esfera_espejo')
setp(esfera, 'material', 'mat_esfera')
if imagen:
    ok('esfera: 1 m con el centro de la imagen de FASE1, derecho (esfera_espejo; la real pide un mapa '
       'equirectangular 2:1)')
else:
    info('esfera: no pude ponerle la imagen; en mat_esfera, Color Map = esfera_espejo')
# v2: la imagen de la esfera, pequena, para el monitor y para medir su color medio
mini = get_or_make(sala, 'resolutionTOP', 'esfera_mini', 880, -40)
connect(mini, sel_fase1, 0)
setmenu(mini, ['outputresolution', 'resolution'], ['custom'], None)
setp_any(mini, ['resolutionw'], 320)
setp_any(mini, ['resolutionh'], 180)
media = get_or_make(sala, 'resolutionTOP', 'esfera_media', 1100, -40)
connect(media, mini, 0)
setmenu(media, ['outputresolution', 'resolution'], ['custom'], None)
setp_any(media, ['resolutionw'], 8)
setp_any(media, ['resolutionh'], 8)
# v6: el color medio, por un TOP to CHOP con descarga diferida (no para el fotograma)
col_chop = get_or_make(sala, 'toptoCHOP', 'esfera_color', 1320, -40)
setp_any(col_chop, ['top'], 'esfera_media')
diferida = setmenu(col_chop, ['downloadtype'], ['delayed', 'nextframe', 'fast'], None)
if diferida:
    ok('esfera_color: el color medio de la esfera, con descarga diferida (antes, 15 ms por fotograma)')
else:
    info('esfera_color: pon Download Type = Delayed a mano, o el color de la esfera parara el fotograma')

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
setmenu(cenital, ['viewanglemethod'], ['horizontal', 'horzfov'], None)
setexpr(cenital, 'fov', "%s.fov_cenital()" % SM)   # v8: todo el suelo de la sala (antes, 75: Femto Bolt NFOV)
if sala.op('vista_plano') is not None:         # v10: la miniatura es la camara cenital
    sala.op('vista_plano').destroy()
MINI_W, MINI_H = 200, 180         # v10: la miniatura de la camara cenital
geos = 'sala_caja lineas equipos_geo personas esfera haces'
r1 = get_or_make(sala, 'renderTOP', 'render_sala', 660, 360)
setexpr(r1, 'camera', "'vista_cenital' if str(parent().par.Vista) == 'cenital' else 'vista'")
setp(r1, 'geometry', geos)
setexpr(r1, 'lights', "%s.luces_render()" % SM)        # v6: sin luz_esfera con Luzesfera 0
setp_any(r1, ['resolutionw'], 1280)
setp_any(r1, ['resolutionh'], 720)
setp_any(r1, ['bgcolorr'], 0.0)
setp_any(r1, ['bgcolorg'], 0.0)
setp_any(r1, ['bgcolorb'], 0.0)
setp_any(r1, ['bgcolora', 'bgalpha'], 1.0)      # v7: fondo negro, no transparente (el visor lo pintaba a cuadros)
setp_any(r1, ['antialias'], 'aa4x')
luz_plano = get_or_make(sala, 'lightCOMP', 'plano_luz', 220, 440)      # solo para el plano: que se lea
setmenu(luz_plano, ['lighttype'], ['distant'], 2)
setp(luz_plano, 'rx', -60.0)
setp(luz_plano, 'dimmer', 0.5)
# v10: la miniatura (abajo a la derecha) es lo que ve la camara cenital: toda la
# planta de la sala (fov_cenital). Mas pequena: 200 x 180, la proporcion de render_cenital.
rp = get_or_make(sala, 'renderTOP', 'render_plano', 660, 120)
setp(rp, 'camera', 'vista_cenital')
setp(rp, 'geometry', 'sala_caja lineas equipos_geo personas esfera')
setexpr(rp, 'lights', "%s.luces_render('plano_luz')" % SM)
setp_any(rp, ['resolutionw'], MINI_W)
setp_any(rp, ['resolutionh'], MINI_H)
setp_any(rp, ['bgcolora', 'bgalpha'], 1.0)      # v7: el plano, un recuadro negro que se lee
r2 = get_or_make(sala, 'renderTOP', 'render_cenital', 660, 280)
setp(r2, 'camera', 'vista_cenital')
setp(r2, 'geometry', 'sala_caja personas')
setp(r2, 'lights', 'luz_casa')
setp_any(r2, ['resolutionw'], 320)
setp_any(r2, ['resolutionh'], 288)
prof = get_or_make(sala, 'depthTOP', 'profundidad', 880, 280)
connect(prof, r2, 0)

# v2: el monitor, una sola imagen con todo: la sala en grande (Vista) y, encima,
# el plano (abajo a la derecha) y el rotulo (arriba a la izquierda). v7: ya no
# lleva lo que muestra la esfera arriba a la derecha. Es lo que hay que mirar: salida_sala.
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


# v7: sin el recuadro de lo que muestra la esfera arriba a la derecha: parecia la
# esfera metida en la esquina de la sala. La esfera 3D ya lo ensena.
if sala.op('con_esfera') is not None:
    sala.op('con_esfera').destroy()
colocados = [encima('con_plano', rp, r1, 'right', 'bottom', 880, 360)]
if transparente:
    con_rotulo = get_or_make(sala, 'overTOP', 'con_rotulo', 1320, 360)
    connect(con_rotulo, rot, 0)
    connect(con_rotulo, sala.op('con_plano'), 1)
    ultimo = con_rotulo
else:
    ultimo = sala.op('con_plano')
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
    ok('monitor_sala (y salida_sala): la sala en grande desde la Vista, con el plano y el rotulo encima. '
       'Es lo unico que hay que mirar')
else:
    info('monitor_sala: no pude colocar el plano en su esquina (Over TOP: Size = Input 2, '
         'Prefit = Native Resolution, Justify); revisalo en con_plano')
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


def diagnostico_esfera():
    """v11: la cadena de la imagen de la esfera, eslabon a eslabon, para saber
    donde se pierde (la esfera sale gris). Pasa el texto entero si sale FALLO."""
    print('DIAGNOSTICO DE LA ESFERA')
    print('-' * 66)

    def linea(bien, que, detalle=''):
        print('  %-6s %-28s %s' % ('OK' if bien else 'FALLO', que, detalle))

    def errores(o):
        try:
            return '; '.join(x for x in (o.errors(recurse=False), o.warnings(recurse=False)) if x)
        except Exception:
            try:
                return o.errors() or ''
            except Exception:
                return ''

    def tam(o):
        try:
            return '%d x %d' % (o.width, o.height)
        except Exception:
            return '?'
    try:
        r = fase1.op('render')
        linea(r is not None, 'FASE1/render', tam(r) if r is not None else 'no existe')
        o = fase1.op('out_render')
        linea(o is not None and bool(o.inputs), 'FASE1/out_render', (tam(o) + '  ' + errores(o)) if o else 'no existe')
        for nm in ('imagen_fase1', 'esfera_imagen', 'esfera_espejo', 'esfera_mini'):
            x = sala.op(nm)
            linea(x is not None and not errores(x) and getattr(x, 'width', 0) > 1, nm,
                  (tam(x) + '  ' + errores(x)) if x is not None else 'no existe')
        x = sala.op('esfera_imagen')
        if x is not None:
            print('         esfera_imagen: crop left %s right %s (unidades %s)'
                  % (x.par.cropleft.eval() if hasattr(x.par, 'cropleft') else '?',
                     x.par.cropright.eval() if hasattr(x.par, 'cropright') else '?',
                     getattr(getattr(x.par, 'cropleftunit', None), 'eval', lambda: '?')()))
        m = sala.op('mat_esfera')
        cm = str(getattr(m.par, 'colormap', None).eval()) if m is not None and hasattr(m.par, 'colormap') else None
        destino = m.op(cm) if m is not None and cm else None
        if destino is None and m is not None and cm:
            destino = m.parent().op(cm)
        linea(m is not None and destino is not None, 'mat_esfera Color Map',
              '%r -> %s' % (cm, destino.path if destino is not None else 'NO ENCONTRADO'))
        if m is not None:
            print('         mat_esfera: tipo %s  color %s' % (m.OPType, tuple(
                round(float(getattr(m.par, 'color' + ch).eval()), 2) if hasattr(m.par, 'color' + ch) else '?'
                for ch in 'rgb')))
        g = sala.op('esfera')
        mat = str(g.par.material.eval()) if g is not None else ''
        mo = g.op(mat) if g is not None and mat else None
        if mo is None and g is not None and mat:
            mo = g.parent().op(mat)
        linea(g is not None and mo is not None and mo.path == (m.path if m else ''), 'esfera Material',
              '%r -> %s' % (mat, mo.path if mo is not None else 'NO ENCONTRADO'))
        if g is not None:
            dibuja = [k.name for k in g.children if getattr(k, 'render', False)]
            linea(dibuja == ['inclinar'], 'esfera dibuja', ' '.join(dibuja) or 'nada')
            u = g.op('uvs')
            if u is not None:
                try:
                    tipo = '%s / eje %s' % (u.par.type.eval(), u.par.axis.eval())
                except Exception:
                    tipo = '?'
                try:
                    attrs = [a.name for a in u.pointAttribs] + [a.name for a in u.vertexAttribs]
                except Exception:
                    attrs = []
                try:
                    muestras = sorted(set(tuple(round(float(v), 2) for v in u.points[k].uv[:2])
                                          for k in range(0, len(u.points), max(1, len(u.points) // 8))))
                except Exception:
                    muestras = '?'
                linea('uv' in attrs, 'uvs (Texture SOP)', '%s  atributos %s  %s' % (tipo, attrs, errores(u)))
                print('         uv de algunos puntos: %s' % (muestras,))
            b = g.op('bola')
            if b is not None:
                try:
                    print('         bola: tipo %s, %d puntos' % (b.par.type.eval(), len(b.points)))
                except Exception:
                    pass
        r1 = sala.op('render_sala')
        if r1 is not None:
            geo_r = str(r1.par.geometry.val).split()          # val: el texto (eval da los operadores)
            linea('esfera' in geo_r, 'render_sala dibuja la esfera', ' '.join(geo_r))
    except Exception as e:
        print('  FALLO  el diagnostico se paro: %s' % e)
    print()


diagnostico_esfera()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    guarda = {}
    for o, nm in ((sala, 'Personas'), (sala, 'Ruidopublico'), (sala, 'Volumendrone'), (sala, 'Modoluz'),
                  (sala, 'Hzprueba'), (sala, 'Activa'), (sala, 'Vista'), (sala, 'Bruma'), (sala, 'Demo'),
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
    sala.par.Demo = 'paseo'
    c = sm.cfg()
    eq = sm.equipos()
    por = dict((tp, [e for e in eq if e['tipo'] == tp]) for tp in sm.TIPOS)
    esf = por['esfera'][0] if por['esfera'] else None
    hx, hz = c['ancho'] / 2.0, c['fondo'] / 2.0

    # 1. los equipos
    t.check('equipos: la esfera en una esquina del fondo, el sub debajo, 4 altavoces colgados, el micro '
            'en lo alto, la camara a 3,5 m, 4 focos y 1 estrobo',
            esf is not None and esf['z'] < 0.0 and sm.esfera_en_esquina(c, eq)
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
    zx, zz = sm.zona(c)
    paradas = [q for i in range(8) for s in sm.plan(c, i, 600.0, ev) if s[4] and not s[5]
               for q in (s[2],)]
    t.check('el publico se para en el suelo de la sala, lejos de las paredes (v8: en toda la sala)',
            paradas and all(abs(x) <= zx + 1e-9 and abs(z) <= zz + 1e-9 for x, z in paradas),
            '%d paradas' % len(paradas))
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
    t.check('v3: el render de FASE1 sale por out_render y SALA lo coge con imagen_fase1, sin cables entre redes',
            fase1.op('out_render') is not None and bool(fase1.op('out_render').inputs)
            and sala.op('imagen_fase1') is not None and bool(sala.op('esfera_mini').inputs)
            and sala.op('esfera_mini').inputs[0] == sala.op('imagen_fase1'))

    # 5b. v2: estar en la sala
    faltan = [nm for nm in ('salida_sala', 'monitor_sala', 'con_plano', 'render_plano', 'esfera_mini',
                            'esfera_imagen', 'esfera_espejo', 'rotulo_sala') if sala.op(nm) is None]
    t.check('un monitor con todo: salida_sala <- monitor_sala, con el plano y el rotulo encima (v7: sin el '
            'recuadro de la esfera)', not faltan and sala.op('con_esfera') is None,
            ('faltan ' + ' '.join(faltan)) if faltan else ('sobra con_esfera' if sala.op('con_esfera') else ''))
    cam_p = sala.op('render_plano').par.camera.eval() if sala.op('render_plano') is not None else None
    cam_n = getattr(cam_p, 'name', str(cam_p).split('/')[-1])      # eval() da el operador, no el texto
    t.check('v10: la miniatura es la camara cenital (sin vista_plano)',
            sala.op('vista_plano') is None and cam_n == 'vista_cenital', 'camara %s' % cam_n)
    t.check('v10: la esfera tiene su Texture SOP (uvs)', sala.op('esfera').op('uvs') is not None)
    esp = sala.op('esfera_espejo')
    t.check('v16: el planeta derecho: esfera_espejo voltea segun Espejosfera y Volteosfera y es el Color '
            'Map de la esfera',
            esp is not None and bool(esp.par.flipx.eval()) == bool(sala.par.Espejosfera.eval())
            and bool(esp.par.flipy.eval()) == bool(sala.par.Volteosfera.eval()) and bool(esp.inputs)
            and str(sala.op('mat_esfera').par.colormap.val).split('/')[-1] == 'esfera_espejo')
    bola_ = sala.op('esfera').op('bola')
    try:
        n_bola = len(bola_.points)
    except Exception:
        n_bola = 0
    t.check('v13: la esfera es una malla (con vertices para la imagen), no una esfera primitiva de un punto',
            n_bola > 1, '%s, %d puntos' % (bola_.par.type.eval() if bola_ else '?', n_bola))
    t.check('v7: sin rayas bajo la esfera: el sub, dentro de la peana, no se dibuja',
            not any(abs(r[0] - por['sub'][0]['x']) < 1e-9 and abs(r[2] - por['sub'][0]['z']) < 1e-9
                    and abs(r[7] - sm.TAM_EQUIPO['sub'][1]) < 1e-9 for r in sm._filas_equipos(c, eq, 5.0)))
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
    sala.par.Vista = 'entrada'
    c = sm.cfg()
    t.check('v4: entrada, desde detras de la puerta y por encima de la gente, mirando hacia abajo y al fondo',
            sm.vista('tz') > hz and sm.vista('ty') > sm.OJOS and sm.vista('my') < sm.vista('ty')
            and sm.vista('mz') < 0.0)
    mg = sm.margen_esfera(c, eq)
    centro_uv = float(sala.fetch('uv_centro', 0.0, search=False))
    g0 = math.radians(sm.giro_esfera())             # 'centrar' deja el centro de la imagen en +Z
    hacia = (math.sin(g0), math.cos(g0))
    he = sm.hacia_esfera(c)
    a_entrada = (he[0] - esf['x'], he[1] - esf['z'])
    t.check('v14: el planeta mira a la camara de la entrada (Girosfera 0)',
            float(sala.par.Girosfera) != 0.0
            or hacia[0] * a_entrada[0] + hacia[1] * a_entrada[1] > 0.99 * math.hypot(*a_entrada),
            'giro %.0f grados; centro de la imagen medido a %.0f' % (sm.giro_esfera(), centro_uv))
    t.check('v18: el planeta se inclina hacia arriba, a la altura de la camara de la entrada (Inclinasfera 0)',
            float(sala.par.Inclinasfera) != 0.0 or sm.inclina_esfera() < 0.0,
            'rx %.1f grados' % sm.inclina_esfera())
    t.check('v5: la esfera en una esquina del fondo, a 1 m de cada pared', sm.esfera_en_esquina(c, eq),
            '%.2f m al fondo, %.2f m al lado' % mg if mg else 'sin esfera')
    lin = sm._filas_lineas(c)
    t.check('la sala dibujada: aristas y reticula (v8: sin el borde de la zona de la camara)',
            sala.op('lineas') is not None and len(lin) > 30
            and 'lineas' in str(sala.op('render_sala').par.geometry.val).split()
            and getattr(sala.par, 'Zonaancho', None) is None,
            '%d lineas' % len(lin))
    cam = por['camara'][0]
    fv = math.radians(sm.fov_cenital(c))
    t.check('v8: la camara cenital ve todo el suelo de la sala',
            math.tan(fv / 2) * cam['y'] >= hx + abs(cam['x']) - 1e-6
            and math.tan(fv / 2) / sm.CENITAL_ASPECTO * cam['y'] >= hz + abs(cam['z']) - 1e-6,
            '%.0f grados en horizontal desde %.1f m' % (sm.fov_cenital(c), cam['y']))
    sala.par.Vista = 'visitante'
    sala.par.Personas = 4
    c = sm.cfg()
    ps = sm.personas(c, 120.0, ev)
    cue = sm._filas_personas(c, eq, 120.0)
    t.check('v5: el publico sin cabeza: un tronco por persona, de toda su altura',
            len(cue) == len(ps) > 0 and sala.op('cabezas') is None
            and all(abs(q[7] - p[3]) < 1e-9 for q, p in zip(cue, ps)))
    # v5: las demos de visita
    sala.par.Personas = 8
    for demo in sm.DEMOS:
        sala.par.Demo = demo
        c = sm.cfg()
        sm._PLANES.clear()
        dentro, lejos, maximo = True, True, 0
        for k in range(240):
            ps = sm.personas(c, 1.0 + 2.5 * k, ev)
            maximo = max(maximo, len(ps))
            for i, x, z, h, andando in ps:
                dentro = dentro and abs(x) <= hx - 0.3 and abs(z) <= hz
                lejos = lejos and all(math.hypot(x - p[0], z - p[2]) > 0.9 for p in ev)
        if demo == 'vacia':
            t.check('demo vacia: nadie en la sala', maximo == 0)
            continue
        t.check('demo %s: el publico dentro de la sala y lejos de la esfera y del estrobo' % demo,
                dentro and lejos and maximo > 0, 'hasta %d a la vez' % maximo)
    sala.par.Demo = 'grupo'
    c = sm.cfg()
    sm._PLANES.clear()
    ps = sm.personas(c, 40.0, ev)
    t.check('demo grupo: a los 40 s estan todos en corro ante la esfera',
            len(ps) == 8 and all(abs(math.hypot(x - esf['x'], z - esf['z']) - sm.CORRO) < 1.2
                                 for _, x, z, _, _ in ps), '%d en la sala' % len(ps))
    sala.par.Demo = 'goteo'
    c = sm.cfg()
    sm._PLANES.clear()
    t.check('demo goteo: de uno en uno', max(len(sm.personas(c, 1.0 + 2.0 * k, ev)) for k in range(300)) <= 2)
    sala.par.Demo = 'llena'
    c = sm.cfg()
    sm._PLANES.clear()
    t.check('demo llena: a los 40 s estan todos', len(sm.personas(c, 40.0, ev)) == 8)
    sala.par.Demo = 'paseo'
    sala.par.Personas = 4
    c = sm.cfg()
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
    t.check('la esfera es una luz: luz_esfera, en su sitio y con el color medio de su imagen (Luzesfera)',
            sala.op('luz_esfera') is not None and abs(sm.luz_esfera('ty') - esf['y']) < 1e-9
            and all(0.0 <= sm.luz_esfera(ch) <= 1.0 for ch in 'rgb'))
    # v6: rendimiento
    lz = sala.par.Luzesfera.eval()
    try:
        sala.par.Luzesfera = 0.0
        sin = sm.luces_render().split()
        sala.par.Luzesfera = 0.5
        con = sm.luces_render().split()
    finally:
        sala.par.Luzesfera = lz
    t.check('v6: con Luzesfera 0, luz_esfera fuera de los render; con luz, dentro',
            'luz_esfera' not in sin and 'luz_esfera' in con and 'luz_foco1' in sin)
    t.check('v6: el color de la esfera por esfera_color (TOP to CHOP), sin numpyArray',
            sala.op('esfera_color') is not None)
    sm._SALA['rotulo'] = None
    r0 = sm.texto_monitor()
    t.check('v6: el rotulo se rehace cada %d fotogramas' % sm.ROTULO_CADA,
            r0 == sm.texto_monitor() and sm._SALA['rotulo_frame'] is not None)
    t.check('el rotulo del monitor: la sala, la luz y la vista',
            'SALA' in sm.texto_monitor() and 'LUZ' in sm.texto_monitor() and 'visitante' in sm.texto_monitor())

    # 6. FASE1 oye el microfono virtual
    if conectado:
        W = m.world()
        m.mic_reset()
        sala.par.Personas = 0
        fase1.par.Fuentemic = 'chop'
        fase1.par.Chopmic = audio.path
        # v14: el reloj de la prueba va 500 s por delante. La hora del ultimo onset
        # se guarda y se pone muy atras (un onset 'futuro' de otra prueba, o de antes
        # de reabrir el proyecto, bloqueaba la palmada por el refractario) y al acabar
        # se devuelve (si no, FASE1 se quedaba sorda hasta que el reloj real llegaba).
        t_onset = W['mic'].get('t', 0.0)
        W['mic']['t'] = -1e9
        try:
            sm._SALA['forzar'] = True
            for _ in range(3):
                sm._SALA['forzar'] = True
                m.mic_tick(W, m.cfg(), absTime.seconds + 500.0)
            antes = W['mic']['n']
            sm.palmada((mic[0] + 0.5, sm.BOCA, mic[2]))
            m.mic_tick(W, m.cfg(), absTime.seconds + 500.5)
            t.check('Palmada: FASE1 la oye por audio_mic y cuenta un onset', W['mic']['n'] == antes + 1,
                    'onsets %d -> %d, flujo %.2f (umbral %.2f)'
                    % (antes, W['mic']['n'], W['mic'].get('flujo', 0.0), m.cfg()['umbral_onset']))
        finally:
            W['mic']['t'] = t_onset
    t.check('leyenda SALA', sm.legend().startswith('SALA') and 'personas' in sm.legend())


def distancia_xz(a, b):
    return math.hypot(a['x'] - b['x'], a['z'] - b['z'])


run_test(fase1, prueba)
print('  Ahora: mira salida_sala (todo en una imagen; Vista = entrada, visitante, orbita o')
print('  cenital). Modoluz = prueba recorre la luz en un minuto; Bruma, los haces en el aire.')
print('  Palmada: la oye FASE1. Personas y Ruidopublico para mas o menos publico.')
print('  ' + sm.legend())
print('=' * 66)
