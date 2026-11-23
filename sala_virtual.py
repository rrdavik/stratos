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
  PERSONAS     sin azar, segun la Demo (v30: cada demo es una seccion con sus
               casos; ver LAS DEMOS):
                 paseo         1 Paseo: entran y salen, a veces en grupo;
                               algo de la obra los detiene
                 probabilidad  2 Estrato humano: la probabilidad minima, la de
                               una persona quieta y la de un grupo
                 huella        3 La huella inevitable: quietos construyen; la
                               fila cava tantas conchas como personas
                 llena         4 Sala llena: Personas (18) se van llenando la
                               sala y cambian de sitio; una sola fila recta (v32)
                 genozilla     5 (v24) el publico juega a GENoZilla capitulo a
                               capitulo (ver DEMO GENOZILLA)
                 vacia         nadie
               v24: cada persona es un MONIGOTE de hombre (i par) o de mujer
               (i impar), como los letreros de los aseos (Monigotes; apagado,
               el tronco de su altura de la v5), de color Colormonigote, con
               las piernas que se balancean al andar. Arcoquietud: un arco
               ambar a sus pies que se cierra en Tfila mientras sigue quieta.
               Hacen ruido: pasos al andar y palmadas o toses (Ruidopublico por segundo y persona;
               Reaccion veces mas con el estrobo encendido).
               v27: con Alimentar (encendido), FASE1 ve al publico de TODAS las
               demos por su sala simulada (Fuente = simulada y la tabla
               sala_personas) y lo marca con un anillo en el globo, tambien sin
               Modojuego (motor v132, Marcapublico). Apagado Alimentar o Activa,
               FASE1 vuelve a su Fuente y a su tabla de antes. OJO: con la sala
               activa, la sala manda sobre la camara de verdad.
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
                 juego      (v24) la sala desde la entrada a la izquierda y la
                            imagen de FASE1 en grande a la derecha (la de la
                            demo GENoZilla); encima, su titulo y su rotulo
               Encima: lo que ve la camara cenital, toda la planta de la sala
               con el publico (abajo a la derecha, 200 x 180; v10, antes un
               plano ortografico aparte de 320 x 240) y el rotulo con la luz, el publico y los onsets
               (arriba a la izquierda). render_cenital (320 x 288) y
               'profundidad' siguen ahi para la fase 22: no hace falta
               mirarlos.

DEMO GENOZILLA (v24, Demo = genozilla)
--------------------------------------
  El publico virtual juega a GENoZilla capitulo a capitulo (la demo web
  «GENoZilla · demo de sala»): 13 capitulos, unos 3 min 50 s. Cada uno empieza
  con su titulo (titulo_demo, 2,8 s, con un velo) y un rotulo abajo
  (rotulo_demo) explica lo que pasa. El juego lo juega FASE1 de verdad: la sala
  mueve a la gente y FASE1 la ve por su sala simulada (Fuente = simulada, la
  tabla sala_personas: la misma imagen de alturas que la camara). Con Guion,
  el motor de FASE1 (motor v119, guion_demo) prepara cada capitulo. Al entrar,
  Guardarescena en el hueco 'antes_demo' (y el mundo y los parametros); al
  salir (otra Demo, o Activa apagada), Cargarescena: FASE1 como estaba.
  Vista = juego (por defecto en la demo): la sala desde la entrada y la imagen
  de FASE1 en grande, lado a lado. Capitulo (el inicial), Siguientecap,
  Buclecap y Guion en la pagina Sala.
  v27 (sala v16, motor v133): cada capitulo empieza en el MUNDO DE FASE1, el
  que habia al entrar en la demo (hasta la v26, en un mundo vacio). El guion
  solo despeja lo que el capitulo necesita libre (donde se para la gente de
  Construir, las vecinas del brote, la celda del monstruo del Cerco) y, si
  hacen falta conchas para cavar y no las hay, entierra copias de la superficie
  por debajo de ella. El Cerco, con seis visitantes.
  v28 (sala v17): en el Pisoton, los dos visitantes que comparten casilla en la
  celda del monstruo, a 0,54 m (antes a 0,37 m, junto a Separacioncabezas 0,35:
  en TouchDesigner sus cabezas se fundian en una, el pisoton contaba dos y no le
  bajaba acum: «acum 12 -> 12»).
  v29: si no hay /project1/SALA pero si otra sala montada en /project1 con otro
  nombre (SALA1 al copiar y pegar, salap...), se usa esa, renombrada a SALA, en
  vez de crear otra. Si hay varias, la primera que se llame SALA-algo; las demas
  quedan paradas, como las copias (v17).

LAS DEMOS (v30, sala v18, motor v140)
-------------------------------------
  Cada demo es una SECCION (su numero y su titulo) hecha de CASOS, y la juega el
  director de GENoZilla: al empezar cada caso, su titulo (titulo_demo, 2,8 s:
  STRATOS · 2 · ESTRATO HUMANO · CASO 2 / 3, el nombre del caso y de que va); abajo,
  el rotulo que explica lo que pasa; arriba a la derecha, la cabecera
  (cabecera_demo: la seccion y el caso y, donde cuenta, lo que mide FASE1 en vivo).
  Al entrar se guarda FASE1 y al salir se devuelve; en las demos nuevas, sin
  Modojuego (el monstruo se comeria lo que construye el publico).
    1 Paseo (80 s)  sueltos que entran y salen; una se interesa por la obra (se
                    queda quieta ante la esfera y su celda construye); un grupo de
                    cuatro entra, se para junto ante la obra y sale junto
    2 Estrato humano  Activo, Cuanto 0,2. Una lluvia de notas cae en una celda
                    testigo y en una vacia; la cabecera dice su probabilidad y
                    cuantas prenden. Casos: Probabilidad minima (sala vacia y dos
                    que cruzan andando: Cuanto), Una persona quieta (sube con su
                    densidad), Un grupo (cinco juntos: casi 1; la celda se corona y
                    desborda)
    3 La huella inevitable  Quietos, construyen (cuatro quietos: inclusion al
                    llegar y al pararse, y sus celdas suenan y construyen encima);
                    La fila cava (Tfila 5: tres en fila abren una escision de 3
                    conchas; se suman dos y baja a 5)
    4 Sala llena (120 s, v32)  Personas entran de uno en uno hasta los 55 s,
                    cada uno a su sitio (nunca junto a otro quieto); luego cambian
                    de sitio, se van y vuelven. Modofila = recta mientras dura y
                    una sola fila recta a proposito (62-76 s): un pozo, no uno
                    por corrillo
    5 GENoZilla     como estaba
  LA CAMARA DE FASE1 SIGUE A LAS CELDAS donde pasan las cosas (la gente quieta, la
  testigo, la fila, el monstruo): la camara de globo gira alrededor del planeta a la
  misma distancia (sin cambiar de altura), suave y como mucho 55 grados del frente
  (motor v140, foco_camara). Siguecamara la apaga. Siguientecap salta al caso
  siguiente; Buclecap vuelve al primero al acabar. Fuera las demos grupo y goteo y
  el parametro Llegada; Personas es ahora la gente de la sala llena.

  v31 (sala v19): LAS DEMOS NO TOCAN EL GIRO DE FASE1. Con la v30 la Demo por
  defecto (paseo) tomaba FASE1 en cuanto la sala estaba activa: cada caso ponia
  Barsperturn 450 (el planeta casi parado y el giro vivo sin notarse) y la camara
  de globo perseguia a la gente de celda en celda (el planeta parecia girar a un
  lado y al otro). La huella, ademas, entierra 7 conchas de golpe para que la fila
  cave y vuelve al mundo de entrada en cada caso. Ahora: el Barsperturn de la demo,
  solo en GENoZilla (como antes); Siguecamara apagado por defecto; y la Demo por
  defecto es la vacia (las demas se eligen a mano). Al relanzar, una vez: si Demo
  estaba en paseo pasa a vacia y Siguecamara se apaga. Y los Over TOP del titulo,
  el rotulo y la cabecera se enchufan desenchufando antes lo que hubiera (enchufa):
  en un proyecto de antes de la v30, con_titulo seguia con con_rotulo_demo en su
  segunda entrada y no con con_cabecera; la autoprueba dice que hay en cada una.
  La autoprueba del titulo compara el punto medio escapado (\u00b7): exec(open(...)
  .read()) lee este archivo en cp1252 en Windows y un '·' literal no coincidia.

  v32 (sala v20): LA SALA LLENA SE VA LLENANDO, SIN POZOS POR TODAS PARTES. Hasta
  la v31 entraban casi a la vez a una rejilla apretada y los quietos quedaban en
  casillas contiguas: con Modofila = cadena, cada corrillo de tres que aguantaba
  Tfila abria una escision (el globo lleno de fulguritas). Ahora la seccion fija
  Modofila = recta, Minfila 3 y Tfila 5 (y los devuelve al salir); entran de uno
  en uno hasta los 55 s y cada quieto ocupa una casilla de columna y fila pares
  (sitios_llena: dos quietos nunca son vecinos); despues cambian de sitio o se
  van y vuelven cada 12-30 s; de 62 a 76 s, una sola fila recta de tres, a
  proposito, abre un pozo; a los 100 s se vacia. Dura 120 s.

  v33 (sala v21, motor v141): LAS DEMOS TOMAN EL MUNDO DONDE ESTA Y NO TOCAN EL
  GIRO. Hasta la v32, cada demo guardaba el mundo de FASE1 al entrar y lo devolvia
  al salir (el planeta volvia atras: ciclos, conchas y lo construido), la
  probabilidad y la huella volvian al mundo de la entrada en cada caso y
  despejaban celdas, la fila de la huella enterraba 7 conchas de golpe y
  GENoZilla rehacia el mundo en cada capitulo, enterraba 6 conchas y ponia
  Barsperturn 450 (45 y 9). Ahora ninguna demo guarda, devuelve, vacia ni
  entierra el mundo ni cambia Barsperturn: el planeta gira con los parametros de
  FASE1 (y su giro vivo) y cierra sus ciclos con sus reglas; los parametros que
  pone la demo si se devuelven al salir. Si al mundo aun le falta lo que un caso
  necesita (dos celdas vacias bajo la sala para la probabilidad; conchas debajo
  para que caven la fila de la huella y las zanjas, el canal y el grito de
  GENoZilla), el caso espera con el titulo 'Esperando que el mundo evolucione'
  y para probar que; lo vuelve a mirar cada 2 s (Siguientecap lo salta). La
  autoprueba juega las demos sobre una copia: deja que esa copia evolucione
  (cierra ciclos) y al acabar FASE1 vuelve a su mundo.

  v34 (sala v22): LA OBRA, PROYECTADA EN UNA PANTALLA. Soporte (pagina Sala):
  pantalla (por defecto; una vez por proyecto se pasa a ella) o esfera (la de LEDs
  de antes). La pantalla cuelga en la pared del fondo, pegada a la de la izquierda
  y al techo, y lleva el render entero de FASE1 (16:9, sin recortes): con
  Altopantalla 3,6 m mide 6,4 x 3,6 y el planeta, unos 3 m (tres veces la esfera
  de 1 m). Un marco oscuro detras y el proyector colgado del techo, delante. Las
  vistas entrada, juego y visitante la miran; con la pantalla, la esfera y su
  peana no se dibujan (render_sala y render_plano eligen una u otra).

  v37: la autoprueba lee la uv del lienzo como la de TouchDesigner (.val, por indice o
  como secuencia): con la v36 el lienzo ya estaba bien (4 puntos, la uv por vertice),
  pero tuple() no la leia y la prueba daba uv [].

  v36: LA PANTALLA EN TOUCHDESIGNER. El Script SOP lienzo crea la uv por vertice
  (como los SOP de TouchDesigner; si no puede, por punto) y recorre el poligono por
  indice: en TouchDesigner la autoprueba no le encontraba puntos (uv []). Si vuelve a
  fallar, el FALLO dice que tiene el lienzo (puntos, prims, atributos y su error).

  v35 (sala v23): GENOZILLA SIN NEFANYAMUTO. Con la fase 41, NefanyaMuto sale solo
  cuando el mundo esta construido al 50 %; sobre el mundo vivo de FASE1 se colaba
  en los capitulos. Cada capitulo de GENoZilla lo apaga (como pone Umbralaparicion
  a 1) y al salir vuelve como estaba.

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

VERSION = 'sala_virtual v37  (la autoprueba lee la uv de la pantalla como la da TouchDesigner)'
banner(VERSION)
SALA_PATH = '/project1/SALA'

fase1 = op(COMP_PATH)
nivel = current_level(fase1) if fase1 is not None else 0
if fase1 is None:
    raise RuntimeError('No encuentro %s. Monta antes Estratos (fase12_base.py y las fases).' % COMP_PATH)

def salas_montadas(raiz):
    """v29: los COMP de raiz con un sala_motor dentro: salas montadas con este script (o
    copias), se llamen como se llamen (SALA1 al copiar y pegar, salap...)."""
    out = []
    for o_ in raiz.children:
        try:
            if o_.isCOMP and o_.op('sala_motor') is not None:
                out.append(o_)
        except Exception:
            pass
    # primero las que se llaman SALA-algo, luego las que tienen su tabla de equipos
    out.sort(key=lambda o_: (not o_.name.upper().startswith('SALA'), o_.op('equipos') is None, o_.name))
    return out


sala = op(SALA_PATH)
if sala is None:
    # v29: si ya hay una sala con otro nombre, se usa esa (renombrada a SALA: el motor y RECARGAR
    # TODO la buscan en /project1/SALA); antes se creaba otra y quedaban dos
    ya = salas_montadas(op('/project1'))
    if ya:
        viejo = ya[0].name
        ya[0].name = 'SALA'
        sala = op(SALA_PATH) or ya[0]
        ok('SALA: ya existia como %s; se usa esa, renombrada a SALA (no se crea otra)' % viejo)
    else:
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

# v24: si la demo GENoZilla estaba en marcha, FASE1 vuelve antes a como estaba (su escena y su
# mundo): la autoprueba guarda el mundo de ahora y la demo, al volver a entrar, guardaria el suyo.
try:
    if sm._guardado() is not None:
        sm.salir(sm.fase1())
        ok('demo GENoZilla: estaba en marcha; FASE1 vuelve a como estaba (con Demo = genozilla, empieza '
           'otra vez al acabar el script)')
except Exception as e:
    info('demo GENoZilla: no pude devolver FASE1 a como estaba (%s)' % e)

# v24: el guion de la demo GENoZilla vive en el motor de FASE1 (motor v119). Si el motor de
# FASE1 es de antes, se pone al dia aqui, como hace cada fase (el mundo se conserva).
motor1 = fase1.op('motor')
if motor1 is not None:
    src1 = read_text(CARPETA, 'estratos_motor.py')
    if motor1.text != src1:
        motor1.text = src1
        try:
            ok('motor de FASE1 al dia (%s): trae el guion de la demo GENoZilla; el mundo se conserva'
               % motor1.module.MOTOR_VERSION)
        except Exception as e:
            raise RuntimeError('el motor de FASE1 no compila: %s' % e)

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
add_par(sala, page, 'int', 'Personas', 'Sala llena: personas', 18, sm.LLENA_MIN, sm.LLENA_MAX, clamp=True)
renew_default(sala, 'Personas', 6, 18)              # v30: es la gente de la sala llena
try:
    sala.par.Personas.label = 'Sala llena: personas'
except Exception:
    pass
add_par(sala, page, 'menu', 'Demo', 'Demo de la sala', 'vacia', menu=sm.DEMOS,
        menu_labels=sm.DEMOS_ETIQUETAS)      # v31: vacia por defecto (las demos toman FASE1)
add_par(sala, page, 'toggle', 'Siguecamara', 'Demos: la camara de FASE1 sigue a las celdas donde pasan las cosas',
        False)    # v30; v31 apagado por defecto
add_par(sala, page, 'toggle', 'Alimentar', 'FASE1 ve a este publico (Fuente = simulada) y lo marca', True)    # v27


def menu_al_dia(nombre, nombres, etiquetas):
    """v24: un menu que ya existia toma las opciones nuevas y conserva lo elegido."""
    try:
        p_ = getattr(sala.par, nombre)
        if list(p_.menuNames) != list(nombres) or list(p_.menuLabels) != list(etiquetas):
            antes_ = str(p_.eval())
            p_.menuNames = list(nombres)
            p_.menuLabels = list(etiquetas)
            if antes_ in nombres:
                p_.val = antes_
            return True
    except Exception as e:
        info('%s: no pude poner sus opciones nuevas (%s)' % (nombre, e))
    return False


if menu_al_dia('Demo', sm.DEMOS, sm.DEMOS_ETIQUETAS):
    ok('Demo: las demos nuevas por secciones y casos (paseo, probabilidad, huella, llena, genozilla, vacia)')
try:                    # v31: una vez por proyecto, FASE1 vuelve a girar y a cerrar sus ciclos sola
    if not sala.fetch('demos_v31', False, search=False):
        sala.store('demos_v31', True)
        for nm_, dflt_ in (('Demo', 'vacia'), ('Siguecamara', False)):
            try:
                getattr(sala.par, nm_).default = dflt_
            except Exception:
                pass
        if str(sala.par.Demo.eval()) == 'paseo':
            sala.par.Demo = 'vacia'
            ok('Demo paseo -> vacia: las demos toman FASE1 (su giro, su mundo y sus conchas); eligelas a mano')
        if bool(sala.par.Siguecamara.eval()):
            sala.par.Siguecamara = False
            ok('Siguecamara -> apagado: la camara de FASE1 en su sitio, el planeta gira siempre hacia el mismo lado')
except Exception as e:
    info('Demo / Siguecamara: no pude ponerlos en vacia y apagado (%s); ponlos a mano' % e)
# v24: la demo GENoZilla
add_par(sala, page, 'menu', 'Capitulo', 'GENoZilla: capitulo inicial', sm.CAP_NOMBRES[0], menu=sm.CAP_NOMBRES,
        menu_labels=sm.CAP_ETIQUETAS)
menu_al_dia('Capitulo', sm.CAP_NOMBRES, sm.CAP_ETIQUETAS)
add_par(sala, page, 'pulse', 'Siguientecap', 'Demo: saltar al caso siguiente')
add_par(sala, page, 'toggle', 'Buclecap', 'Demo: al acabar el ultimo caso, volver al primero', True)
for nm_, lb_ in (('Siguientecap', 'Demo: saltar al caso siguiente'),
                 ('Buclecap', 'Demo: al acabar el ultimo caso, volver al primero')):
    try:
        getattr(sala.par, nm_).label = lb_
    except Exception:
        pass
add_par(sala, page, 'toggle', 'Guion', 'GENoZilla: el guion prepara FASE1 en cada capitulo', True)
# v24: monigotes
add_par(sala, page, 'toggle', 'Monigotes', 'Publico de monigotes (apagado: troncos)', True)
add_par(sala, page, 'rgb', 'Colormonigote', 'Color de los monigotes', sm.COL_MONIGOTE)
add_par(sala, page, 'toggle', 'Arcoquietud', 'Arco de quietud a los pies (cuenta Tfila)', False)
for viejo in ('Llegada',):          # v30: el paseo lo lleva su coreografia
    try:
        p_ = getattr(sala.par, viejo, None)
        if p_ is not None:
            p_.destroy()
            ok('%s: quitado (el paseo lo lleva su coreografia)' % viejo)
    except Exception as e:
        info('%s: no pude quitarlo (%s); ya no se usa' % (viejo, e))
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
add_par(sala, page, 'toggle', 'Volteosfera', 'Esfera: voltear la imagen en vertical (boca abajo)', False)
try:                    # v19: la imagen va de frente y derecha: sin volteos (una vez por proyecto)
    if not sala.fetch('volteo_v19', False, search=False):
        sala.store('volteo_v19', True)
        for nm in ('Espejosfera', 'Volteosfera'):
            getattr(sala.par, nm).val = False
            getattr(sala.par, nm).default = False
except Exception as e:
    info('Espejosfera / Volteosfera: no pude apagarlos (%s); apagalos a mano' % e)
try:                    # v20: los retoques a mano de antes de la v19 (imagen envuelta) sobran
    if not sala.fetch('giro_v20', False, search=False):
        sala.store('giro_v20', True)
        antes = (float(sala.par.Girosfera), float(sala.par.Inclinasfera))
        sala.par.Girosfera = 0.0
        sala.par.Inclinasfera = 0.0
        if any(abs(v) > 1e-6 for v in antes):
            ok('Girosfera %g -> 0 e Inclinasfera %g -> 0: con la imagen de frente, el giro y la inclinacion '
               'automaticos ya ponen el planeta mirando a la entrada' % antes)
except Exception as e:
    info('Girosfera / Inclinasfera: no pude ponerlos a 0 (%s); ponlos a mano' % e)
add_par(sala, page, 'float', 'Inclinasfera', 'Inclinacion de la esfera (grados hacia arriba; 0 = mira '
        'a la camara de la entrada)', 0.0, -90.0, 90.0)
add_par(sala, page, 'float', 'Girosfera', 'Giro de la esfera (grados; 0 = el planeta mira a la sala)', 0.0,
        -180.0, 180.0)
# v34: la obra en una pantalla proyectada (por defecto) o en la esfera de LEDs
add_par(sala, page, 'menu', 'Soporte', 'Donde se ve la obra', 'pantalla', menu=sm.SOPORTES,
        menu_labels=sm.SOPORTES_ETIQUETAS)
menu_al_dia('Soporte', sm.SOPORTES, sm.SOPORTES_ETIQUETAS)
add_par(sala, page, 'float', 'Altopantalla', 'Pantalla: alto en m (16:9; el planeta, el 85 % del alto)', sm.PANT_ALTO,
        1.0, 6.0)
try:                    # v34: una vez por proyecto, a la pantalla (la esfera de LEDs se queda como opcion)
    if not sala.fetch('soporte_v34', False, search=False):
        sala.store('soporte_v34', True)
        sala.par.Soporte.default = 'pantalla'
        if str(sala.par.Soporte.eval()) != 'pantalla':
            sala.par.Soporte = 'pantalla'
        ok('Soporte: pantalla (la obra proyectada arriba a la izquierda; la esfera de LEDs, en Soporte = esfera)')
except Exception as e:
    info('Soporte: no pude ponerlo en pantalla (%s); ponlo a mano' % e)
add_par(sala, page, 'float', 'Bruma', 'Bruma: los haces de los focos se ven (0 = aire limpio)', 0.5, 0.0, 1.0,
        clamp=True)
VISTAS_ETIQUETAS = ['Visitante (pasea entre el publico)', 'Entrada (la sala desde la puerta)', 'Orbita (desde fuera)',
                    'Camara cenital']
VISTAS_ETIQUETAS.append('Juego (la sala y la imagen de FASE1, lado a lado)')         # v24
add_par(sala, page, 'menu', 'Vista', 'Vista del monitor', 'entrada', menu=sm.VISTAS,
        menu_labels=VISTAS_ETIQUETAS)
try:                                    # v2: libre pasa a llamarse orbita y el defecto es visitante
    vp = sala.par.Vista
    if 'visitante' not in list(vp.menuNames):
        antes = str(vp.eval())
        vp.menuNames = list(sm.VISTAS)
        vp.menuLabels = VISTAS_ETIQUETAS
        vp.default = 'visitante'
        vp.val = 'cenital' if antes == 'cenital' else 'visitante'
        vp.label = 'Vista del monitor'
        ok('Vista: visitante (pasea entre el publico), entrada, orbita (la libre de antes) y cenital')
except Exception as e:
    info('Vista: no pude poner las vistas nuevas (%s)' % e)
if menu_al_dia('Vista', sm.VISTAS, VISTAS_ETIQUETAS):        # v24: y juego
    ok('Vista: con juego (la sala y la imagen de FASE1, lado a lado; la de la demo GENoZilla)')
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
   'Alturavista (las tres, solo con Vista = orbita); v24: Capitulo, Siguientecap, Buclecap, Guion, '
   'Monigotes, Colormonigote, Arcoquietud')

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
# v25: onValueChange vacio. El Parameter Execute DAT trae Value Change encendido y, sin
# esta funcion, TouchDesigner daba 'Cannot find function named: onValueChange' cada vez
# que cambiaba un parametro de la sala.
def onPulse(par):
    op('sala_motor').module.on_pulse(par.name)
    return


def onValueChange(par, prev):
    return
'''

SM = "parent().op('sala_motor').module"


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


def instanciado(name, x, y, mat, sop='box'):
    """Geometry COMP 'name' instanciada desde el Script CHOP 'i_name': una caja
    de 1 x 1 x 1 con la base en y = 0, una esfera de diametro 1 centrada
    (sop='sphere'), un cono abierto de diametro 1 y largo 1 con la punta en
    el origen hacia -Z, como la luz de una Light COMP (sop='haz'), o (v24) el
    vestido de los monigotes: un cono truncado cerrado, de diametro 1 abajo y
    VESTIDO arriba, alto 1 y la base en y = 0 (sop='vestido')."""
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
        # v26: la bola de los monigotes (cabeza y hombros), malla de poligonos. Hasta la
        # v25 se pedia con setp('polymesh'), que no casa con ningun nombre del menu (como
        # le pasaba a la esfera hasta la v13): se quedaba en Primitive Type = prim, una
        # esfera primitiva de un solo punto, y sus instancias salian en el suelo. Ahora,
        # por nombre o etiqueta, y un Transform SOP la deja en diametro 1 y centrada,
        # midiendo sus puntos.
        bola = mk(geo, 'sphereSOP', 'bola', 0, 120)
        for ax in ('radx', 'rady', 'radz'):
            setp(bola, ax, 0.5)
        for ax in ('tx', 'ty', 'tz'):
            setp(bola, ax, 0.0)
        malla = ((setmenu(bola, ['type', 'primtype'], ['polymesh', 'polygonmesh', 'mesh'], None)
                  and str(bola.par.type.eval()) != 'prim')
                 or menu_por_texto(bola, ['type', 'primtype'], ['mesh', 'poly']))
        setp_any(bola, ['rows'], 12)
        setp_any(bola, ['cols'], 16)
        s = mk(geo, 'transformSOP', 'a_la_unidad', 200, 0)
        connect(s, bola, 0)
        b = medir(bola)
        if not malla or b is None or min(b[1] - b[0], b[3] - b[2], b[5] - b[4]) < 1e-3:
            info('%s/bola: sigue siendo una esfera primitiva (medidas %s); pon a mano Primitive Type = '
                 'Polygon Mesh o la cabeza de los monigotes saldra en el suelo' % (name, b))
        else:
            setmenu(s, ['xord'], ['srt'], 0)
            for q, ax in enumerate('xyz'):
                k = 1.0 / (b[2 * q + 1] - b[2 * q])
                setp(s, 's' + ax, k)
                setp(s, 't' + ax, -0.5 * (b[2 * q] + b[2 * q + 1]) * k)
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
    elif sop == 'vestido':
        cono = mk(geo, 'tubeSOP', 'cono', 0, 120)
        setp_any(cono, ['rad1'], 0.5)
        setp_any(cono, ['rad2'], 0.5 * sm.VESTIDO[0] / sm.VESTIDO[1])
        setp(cono, 'height', 1.0)
        setp_any(cono, ['cols', 'columns'], 20)
        setp_any(cono, ['rows'], 2)
        setp_any(cono, ['caps', 'endcaps', 'capends'], True)
        setmenu(cono, ['orient', 'orientation'], ['y'], 1)
        arriba = punta_arriba(geo, cono)        # lo estrecho arriba
        s = mk(geo, 'transformSOP', 'al_suelo', 200, 0)
        connect(s, arriba, 0)
        setp(s, 'ty', 0.5)                      # la base en y = 0
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
# v24: los monigotes (cabeza y hombros, y el vestido) y el arco de quietud
instanciado('personas_bolas', 0, -200, 'mat_personas', sop='sphere')
instanciado('personas_conos', 0, -280, 'mat_personas', sop='vestido')
make_constant(sala, 'mat_arcos', 660, 600, (1.0, 1.0, 1.0))      # se ve a oscuras, como las lineas
instanciado('arcos', 0, -360, 'mat_arcos')
ok('monigotes: personas (cuerpo, brazos y piernas), personas_bolas (cabeza y hombros) y personas_conos '
   '(el vestido), de Colormonigote; arcos: el arco de quietud (Arcoquietud), ambar en el suelo')
instanciado('haces', 0, 440, 'mat_haz', sop='haz')
instanciado('lineas', 0, 520, 'mat_lineas')
ok('sala_caja, equipos_geo y personas (v24: monigotes; sin Monigotes, un tronco): suelo, paredes, el suelo del '
   'publico, puerta, aparatos y publico; haces: la luz de cada foco y del estrobo en la bruma (Bruma); lineas: aristas, umbral de la '
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
# v19: la imagen de FASE1 ya es un planeta visto de frente. Hasta la v18 se envolvia
# alrededor de la bola (Texture SOP equirectangular): salia estirada, de lado y del revés
# segun los volteos. Ahora el Script SOP 'frente' le pone a cada punto las coordenadas de
# textura de una proyeccion de frente (u, v = x, y de la bola, de -r a r -> de 0 a 1):
# la cara +Z de la bola muestra la imagen tal cual. 'inclinar' (rx) la levanta hacia la
# camara de la entrada y la esfera (ry) la gira hacia ella.
FRENTE_CB = r"""# Script SOP 'frente' de la esfera (sala_virtual v19): coordenadas de textura
# de una proyeccion de frente, a lo largo de Z.


def onSetupParameters(scriptOp):
    return


def _uv(q, r):
    return (0.5 + 0.5 * q.x / r, 0.5 + 0.5 * q.y / r, 0.0)


def onCook(scriptOp):
    scriptOp.clear()
    if not scriptOp.inputs:
        return
    scriptOp.copy(scriptOp.inputs[0])
    pts = scriptOp.points
    r = max([max(abs(q.x), abs(q.y)) for q in pts] or [0.5]) or 0.5
    # v21: la malla de la Sphere SOP ya trae uv por vertice, y un uv por punto con el
    # mismo nombre no se puede crear ('Vertex Attribute with that name already
    # exists'). Si hay uv por vertice, se reescribe ese; si no, se crea por punto.
    if 'uv' in [a.name for a in scriptOp.vertexAttribs]:
        for pr in scriptOp.prims:
            for v in pr:
                v.uv = _uv(v.point, r)
    else:
        if 'uv' not in [a.name for a in scriptOp.pointAttribs]:
            scriptOp.pointAttribs.create('uv', (0.0, 0.0, 0.0))
        for q in pts:
            q.uv = _uv(q, r)
    return
"""
cb_frente = mk(esfera, 'textDAT', 'frente_callbacks', 200, -120)
cb_frente.text = FRENTE_CB
frente = mk(esfera, 'scriptSOP', 'frente', 0, -120)
connect(frente, bola, 0)
setp_any(frente, ['callbacks', 'callbackdat', 'dat'], 'frente_callbacks')
inclinar = mk(esfera, 'transformSOP', 'inclinar', 0, -240)
connect(inclinar, frente, 0)
setexpr(inclinar, 'rx', "parent(2).op('sala_motor').module.inclina_esfera(absTime.frame)")
for o_, si in ((bola, False), (frente, False), (inclinar, True)):
    for attr in ('render', 'display'):
        try:
            setattr(o_, attr, si)
        except Exception:
            pass
try:
    frente.cook(force=True)
    con_uv = ('uv' in [a.name for a in frente.pointAttribs] + [a.name for a in frente.vertexAttribs]
              and not frente.errors())
except Exception:
    con_uv = False
if con_uv:
    ok('esfera: la imagen de FASE1 de frente (Script SOP frente), mirando a la entrada: como se ve en FASE1')
else:
    info('esfera/frente: el Script SOP no puso las coordenadas de textura (%s); la esfera saldra gris'
         % (frente.errors() if hasattr(frente, 'errors') else '?'))
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
# v15: un Flip TOP entre el recorte y el material; desde la v19, con la imagen de frente,
# sin volteos (Espejosfera y Volteosfera apagados), por si hiciera falta.
espejo = get_or_make(sala, 'flipTOP', 'esfera_espejo', 1100, -120)
connect(espejo, recorte, 0)
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
# v34: la pantalla proyectada: un rectangulo de 1 x 1 en XY (Script SOP 'lienzo', con uv de 0 a
# 1) que el Geometry COMP escala y coloca (sala_motor.pantalla). Su material lleva el render
# entero de FASE1 (imagen_fase1, 16:9): lo mismo que recibiria el proyector.
PANTALLA_CB = r"""# Script SOP 'lienzo' de la pantalla (sala_virtual v34): un rectangulo de 1 x 1
# en el plano XY, mirando a +Z, con las coordenadas de textura de 0 a 1.
# v36: la uv, por vertice (como la llevan los SOP de TouchDesigner); si no se puede, por
# punto. El poligono se recorre por indice.

ESQUINAS = ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))


def onSetupParameters(scriptOp):
    return


def clase_uv(scriptOp):
    # 'vertex' o 'point': donde va la uv (la que ya haya o la que se pueda crear)
    for clase in ('vertex', 'point'):
        if 'uv' in [a.name for a in getattr(scriptOp, clase + 'Attribs')]:
            return clase
    for clase in ('vertex', 'point'):
        try:
            getattr(scriptOp, clase + 'Attribs').create('uv', (0.0, 0.0, 0.0))
            return clase
        except Exception:
            pass
    return None


def onCook(scriptOp):
    scriptOp.clear()
    clase = clase_uv(scriptOp)
    pr = scriptOp.appendPoly(4, closed=True, addPoints=True)
    for k in range(4):
        x, y = ESQUINAS[k]
        v = pr[k]
        q = v.point
        q.x, q.y, q.z = x, y, 0.0
        uv = (x + 0.5, y + 0.5, 0.0)
        if clase == 'vertex':
            v.uv = uv
        elif clase == 'point':
            q.uv = uv
    return
"""


def _uv2(a):
    """v37: (u, v) de un valor de uv de TouchDesigner, se lea como se lea: .val, por
    indice o como secuencia (en TouchDesigner no siempre se deja convertir con tuple)."""
    for leer in (lambda x: x.val, lambda x: (x[0], x[1]), lambda x: tuple(x), lambda x: x):
        try:
            t = leer(a)
            return (round(float(t[0]), 3), round(float(t[1]), 3))
        except Exception:
            pass
    raise ValueError('no se como leer %s (%r)' % (type(a).__name__, a))


def _vertices(pr):
    try:
        return [pr[k] for k in range(len(pr))]
    except Exception:
        return list(pr)


def uvs_lienzo(lz, errores=None):
    """v36: las uv del rectangulo (por vertice o por punto), redondeadas y ordenadas.
    v37: si no se pueden leer, el porque va a errores (una lista)."""
    if lz is None:
        return []
    out = []
    try:
        if any(a.name == 'uv' for a in lz.vertexAttribs):
            for pr in lz.prims:
                for v in _vertices(pr):
                    out.append(_uv2(v.uv))
        else:
            for q in lz.points:
                out.append(_uv2(q.uv))
    except Exception as e:
        if errores is not None:
            errores.append('%s: %s' % (type(e).__name__, e))
        return []
    return sorted(out)


def diag_lienzo(lz):
    """v36: lo que tiene el Script SOP lienzo, para el FALLO de la autoprueba."""
    if lz is None:
        return 'no existe'
    try:
        at = ['%s:%s' % (k[0], a.name) for k in ('vertex', 'point') for a in getattr(lz, k + 'Attribs')]
        err = (lz.errors() or '').strip().replace('\n', ' / ')
        return '%d puntos, %d prims, atributos %s%s' % (len(lz.points), len(lz.prims), at,
                                                       (', error: ' + err) if err else '')
    except Exception as e:
        return 'no lo pude leer (%s)' % e


pantalla = fresh(sala, 'geometryCOMP', 'pantalla', 0, -560)
for k in list(pantalla.children):
    try:
        k.render = False
        k.display = False
    except Exception:
        pass
cb_lienzo = mk(pantalla, 'textDAT', 'lienzo_callbacks', 200, 0)
cb_lienzo.text = PANTALLA_CB
lienzo_sop = mk(pantalla, 'scriptSOP', 'lienzo', 0, 0)
setp_any(lienzo_sop, ['callbacks', 'callbackdat', 'dat'], 'lienzo_callbacks')
for attr in ('render', 'display'):
    try:
        setattr(lienzo_sop, attr, True)
    except Exception:
        pass
for ax in ('tx', 'ty', 'tz', 'sx', 'sy', 'scale'):
    setexpr(pantalla, ax, "%s.pantalla('%s', absTime.frame)" % (SM, ax))
setexpr(esfera, 'scale', "%s.escala_esfera(absTime.frame)" % SM)      # v34: sin Soporte = esfera, no se ve
mat_pantalla = make_constant(sala, 'mat_pantalla', 660, -560, (1.0, 1.0, 1.0))
con_imagen = setp_any(mat_pantalla, ['colormap', 'map'], 'imagen_fase1')
setp(pantalla, 'material', 'mat_pantalla')
try:
    lienzo_sop.cook(force=True)
    lienzo_bien = len(lienzo_sop.points) == 4 and not lienzo_sop.errors() \
        and any('uv' in [a.name for a in getattr(lienzo_sop, k_ + 'Attribs')] for k_ in ('vertex', 'point'))
except Exception:
    lienzo_bien = False
if con_imagen and lienzo_bien:
    r_ = sm.pantalla_rect()
    ok('pantalla: %s x %s m arriba a la izquierda (pared del fondo), con el render entero de FASE1; el planeta, '
       'unos %s m' % tuple(('%.1f' % v).replace('.', ',') for v in (r_['w'], r_['h'], 0.85 * r_['h'])))
else:
    info('pantalla: el rectangulo (Script SOP lienzo) o su imagen (mat_pantalla, Color Map = imagen_fase1) no '
         'quedaron bien; revisalos (lienzo: %s)' % diag_lienzo(lienzo_sop))
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
PUBLICO = 'personas personas_bolas personas_conos'       # v24: los monigotes
# v34: la pantalla y la esfera, las dos en los render; la que no es el Soporte, a escala casi 0
geos = 'sala_caja lineas equipos_geo %s arcos esfera pantalla haces' % PUBLICO
r1 = get_or_make(sala, 'renderTOP', 'render_sala', 660, 360)
setexpr(r1, 'camera', "'vista_cenital' if str(parent().par.Vista) == 'cenital' else 'vista'")
setp(r1, 'geometry', geos)
setexpr(r1, 'lights', "%s.luces_render()" % SM)        # v6: sin luz_esfera con Luzesfera 0
setp_any(r1, ['resolutionw'], 1280)
setp_any(r1, ['resolutionh'], 720)
# v24: con Vista = juego, la sala en un cuadrado de 720 x 720 (a la izquierda del monitor)
JUEGO_EXPR = "str(parent().par.Vista) == 'juego'"
setexpr(r1, 'resolutionw', "720 if %s else 1280" % JUEGO_EXPR)
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
setp(rp, 'geometry', 'sala_caja lineas equipos_geo %s arcos esfera pantalla' % PUBLICO)
setexpr(rp, 'lights', "%s.luces_render('plano_luz')" % SM)
setp_any(rp, ['resolutionw'], MINI_W)
setp_any(rp, ['resolutionh'], MINI_H)
setp_any(rp, ['bgcolora', 'bgalpha'], 1.0)      # v7: el plano, un recuadro negro que se lee
r2 = get_or_make(sala, 'renderTOP', 'render_cenital', 660, 280)
setp(r2, 'camera', 'vista_cenital')
setp(r2, 'geometry', 'sala_caja %s' % PUBLICO)      # v24: los monigotes; sin el arco del suelo
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


def enchufa(dst, src, i):
    """v31: connect, pero si en la entrada i quedaba otro (un Over TOP de una version
    anterior: con_titulo tenia con_rotulo_demo donde la v30 pone con_cabecera), lo
    desenchufa antes. Devuelve si en la entrada i queda src."""
    try:
        c = dst.inputConnectors[i]
        if [x.owner for x in c.connections] != [src]:
            c.disconnect()
            c.connect(src)
        return [x.owner for x in c.connections] == [src]
    except Exception:
        return connect(dst, src, i)


def entrada(o, i):
    """v31: el nombre del operador en la entrada i de o ('-' si no hay nada)."""
    try:
        cs = o.inputConnectors[i].connections
        return cs[0].owner.name if cs else '-'
    except Exception:
        try:
            return o.inputs[i].name
        except Exception:
            return '-'


def encima(nombre, arriba, abajo, horiz, vert, x, y, margen=16):
    """Over TOP: 'arriba' a su tamano, en la esquina (horiz, vert) de 'abajo',
    a 'margen' px del borde (v24: centrado, horiz o vert 'center'). Devuelve si pudo
    colocarlo."""
    o = get_or_make(sala, 'overTOP', nombre, x, y)
    enchufa(o, arriba, 0)
    enchufa(o, abajo, 1)
    bien = [setmenu(o, ['size', 'outputresolution'], ['input2', 'in2'], None),
            setmenu(o, ['prefit'], ['nativeres', 'native'], None),
            setmenu(o, ['justifyh'], [horiz], None),
            setmenu(o, ['justifyv'], [vert], None)]
    setmenu(o, ['tunit'], ['pixels'], None)
    setp(o, 'tx', 0 if horiz == 'center' else (-margen if horiz == 'right' else margen))
    setp(o, 'ty', 0 if vert == 'center' else (margen if vert == 'bottom' else -margen))
    return all(bien)


def fuente(nombre):
    """v24: el nombre de la fuente si esta instalada (en la carpeta de fuentes de
    Windows, del usuario o de macOS); si no, Arial."""
    import os
    clave = nombre.replace(' ', '').lower()
    carpetas = ['C:/Windows/Fonts', os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts'),
                '/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    for d in carpetas:
        try:
            for f in os.listdir(d):
                if clave in f.replace(' ', '').replace('-', '').replace('_', '').lower():
                    return nombre
        except Exception:
            pass
    return 'Arial'


def texto_top(nombre, x, y, w, h, expr, tam, color, fuente_, alinea_y='center', pos_y=0, fondo=None, envolver=False):
    """v24: un Text TOP de w x h con el texto de la expresion, centrado, de color
    (r, g, b) y tamano tam; fondo (r, g, b, a) o transparente."""
    o = get_or_make(sala, 'textTOP', nombre, x, y)
    setmenu(o, ['outputresolution'], ['custom'], None)
    setp_any(o, ['resolutionw'], w)
    setp_any(o, ['resolutionh'], h)
    setp_any(o, ['font', 'fontfamily'], fuente_)
    setp_any(o, ['fontsizex', 'fontsize'], tam)
    setp(o, 'fontsizey', tam)
    setp_any(o, ['alignx'], 'center')
    setp_any(o, ['aligny'], alinea_y)
    setp_any(o, ['positionx', 'textx'], 0)
    setp_any(o, ['positiony', 'texty'], pos_y)
    for ch, v in zip('rgb', color):
        setp_any(o, ['fontcolor' + ch, 'color' + ch], v)
    setp_any(o, ['fontalpha', 'fontcolora'], 1.0)
    f = fondo or (0.0, 0.0, 0.0, 0.0)
    for ch, v in zip('rgb', f[:3]):
        setp_any(o, ['bgcolor' + ch, 'backgroundcolor' + ch], v)
    transp = setp_any(o, ['bgalpha', 'backgroundalpha', 'bgcolora'], f[3])
    if envolver:
        setp_any(o, ['wordwrap'], True)
    setexpr(o, 'text', expr)
    return o, bool(transp)


# v7: sin el recuadro de lo que muestra la esfera arriba a la derecha: parecia la
# esfera metida en la esquina de la sala. La esfera 3D ya lo ensena.
if sala.op('con_esfera') is not None:
    sala.op('con_esfera').destroy()
# v24: la vista juego: la sala (720 x 720) a la izquierda y la imagen de FASE1 (560 x 720, el
# centro del render: el planeta) a la derecha, en un lienzo de 1280 x 720
lienzo = get_or_make(sala, 'constantTOP', 'juego_lienzo', 660, 680)
setmenu(lienzo, ['outputresolution'], ['custom'], None)
setp_any(lienzo, ['resolutionw'], 1280)
setp_any(lienzo, ['resolutionh'], 720)
for ch in ('colorr', 'colorg', 'colorb'):
    setp(lienzo, ch, 0.0)
setp_any(lienzo, ['alpha', 'colora'], 1.0)
j_fase1 = get_or_make(sala, 'cropTOP', 'juego_fase1', 880, 760)
connect(j_fase1, sel_fase1, 0)
lado_j = 0.5 * (1.0 - 560.0 / 1280.0)
setp_any(j_fase1, ['cropleft'], lado_j)
setp_any(j_fase1, ['cropright'], 1.0 - lado_j)
juego_ok = [encima('juego_sala', r1, lienzo, 'left', 'top', 880, 680, margen=0),
            encima('juego_lado', j_fase1, sala.op('juego_sala'), 'right', 'top', 1100, 680, margen=0)]
base_mon = get_or_make(sala, 'switchTOP', 'monitor_base', 1100, 440)
connect(base_mon, r1, 0)
connect(base_mon, sala.op('juego_lado'), 1)
setexpr(base_mon, 'index', "1 if %s else 0" % JUEGO_EXPR)
colocados = [encima('con_plano', rp, base_mon, 'right', 'bottom', 880, 360)]
if transparente:
    con_rotulo = get_or_make(sala, 'overTOP', 'con_rotulo', 1320, 360)
    connect(con_rotulo, rot, 0)
    connect(con_rotulo, sala.op('con_plano'), 1)
    ultimo = con_rotulo
else:
    ultimo = sala.op('con_plano')
    info('rotulo_sala: no pude hacer transparente su fondo; el rotulo se ve en su nodo')
# v24: el titulo y el rotulo de la demo GENoZilla, encima de todo (salen en salida_sala)
TXT = "parent().op('sala_motor').module.%s(absTime.frame)"
f_titulo, f_rotulo = fuente('Space Grotesk'), fuente('Inter')
velo = get_or_make(sala, 'constantTOP', 'titulo_velo', 1320, 840)
setmenu(velo, ['outputresolution'], ['custom'], None)
setp_any(velo, ['resolutionw'], 1280)
setp_any(velo, ['resolutionh'], 720)
for ch in ('colorr', 'colorg', 'colorb'):
    setp(velo, ch, 0.02)
setp_any(velo, ['alpha', 'colora'], sm.VELO)
t_ante, _ = texto_top('titulo_ante', 1100, 920, 1280, 720, "parent().op('sala_motor').module.titulo_texto('ante', "
                      "absTime.frame)", 22, sm.AMBAR, f_titulo, pos_y=95)
t_nom, _ = texto_top('titulo_demo', 1100, 1000, 1280, 720, "parent().op('sala_motor').module.titulo_texto('nombre', "
                     "absTime.frame)", 64, (0.91, 0.92, 0.95), f_titulo, pos_y=10)
t_sub, _ = texto_top('titulo_sub', 1100, 1080, 1280, 720, "parent().op('sala_motor').module.titulo_texto('sub', "
                     "absTime.frame)", 24, (0.55, 0.58, 0.64), f_rotulo, pos_y=-75)
capa = velo
for k_, (nm_, o_) in enumerate((('titulo_c1', t_ante), ('titulo_c2', t_nom), ('titulo_c3', t_sub))):
    ov = get_or_make(sala, 'overTOP', nm_, 1320, 920 + 80 * k_)
    connect(ov, o_, 0)
    connect(ov, capa, 1)
    setmenu(ov, ['size', 'outputresolution'], ['input2', 'in2'], None)
    capa = ov
fundido = get_or_make(sala, 'levelTOP', 'titulo_fundido', 1540, 1000)
connect(fundido, capa, 0)
titulo_ok = setexpr(fundido, 'opacity', TXT % 'titulo_alfa')
rot_demo, rot_transp = texto_top('rotulo_demo', 1100, 1200, 1152, 84, TXT % 'rotulo_demo', 22,
                                 (0.91, 0.92, 0.95), f_rotulo, fondo=(0.02, 0.027, 0.04, 0.82), envolver=True)
rot_fundido = get_or_make(sala, 'levelTOP', 'rotulo_fundido', 1320, 1200)
connect(rot_fundido, rot_demo, 0)
rotulo_ok = setexpr(rot_fundido, 'opacity', TXT % 'rotulo_alfa')
colocados.append(encima('con_rotulo_demo', rot_fundido, ultimo, 'center', 'bottom', 1540, 440, margen=16))
# v30: la cabecera de la demo, arriba a la derecha: la seccion, el caso y lo que mide FASE1
cab_demo, _ = texto_top('cabecera_demo', 1100, 1300, 640, 60, TXT % 'cabecera_texto', 16,
                        sm.AMBAR, f_rotulo, fondo=(0.02, 0.027, 0.04, 0.72))
cab_fundido = get_or_make(sala, 'levelTOP', 'cabecera_fundido', 1320, 1300)
connect(cab_fundido, cab_demo, 0)
cabecera_ok = setexpr(cab_fundido, 'opacity', TXT % 'cabecera_alfa')
colocados.append(encima('con_cabecera', cab_fundido, sala.op('con_rotulo_demo'), 'right', 'top', 1540, 480,
                        margen=12))
colocados.append(encima('con_titulo', fundido, sala.op('con_cabecera'), 'center', 'center', 1540, 520, margen=0))
ultimo = sala.op('con_titulo')
if titulo_ok and rotulo_ok and cabecera_ok:
    ok('titulo_demo, rotulo_demo y cabecera_demo: el titulo de cada caso de las demos (2,8 s sobre un velo, con '
       'fundido; %s), el rotulo abajo (%s) y la seccion y el caso arriba a la derecha, encima del monitor y en '
       'salida_sala' % (f_titulo, f_rotulo))
else:
    info('titulo_demo / rotulo_demo / cabecera_demo: no pude enlazar su opacidad (Level TOP: Opacity); revisa '
         'titulo_fundido, rotulo_fundido y cabecera_fundido')
if all(juego_ok):
    ok('Vista = juego: la sala desde la entrada (720 x 720) y la imagen de FASE1 en grande (560 x 720), lado a lado')
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
setp_any(pulsos, ['valuechange'], False)      # v25: solo los botones (onPulse)
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
            u = g.op('frente')
            if u is not None:
                tipo = 'proyeccion de frente'
                try:
                    attrs = [a.name for a in u.pointAttribs] + [a.name for a in u.vertexAttribs]
                except Exception:
                    attrs = []
                try:
                    muestras = sorted(set(tuple(round(float(v), 2) for v in u.points[k].uv[:2])
                                          for k in range(0, len(u.points), max(1, len(u.points) // 8))))
                except Exception:
                    muestras = '?'
                linea('uv' in attrs, 'frente (Script SOP)', '%s  atributos %s  %s' % (tipo, attrs, errores(u)))
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
                  (sala, 'Monigotes'), (sala, 'Arcoquietud'), (sala, 'Capitulo'), (sala, 'Guion'),
                  (sala, 'Alimentar'), (fase1, 'Fuentemic'), (fase1, 'Chopmic')):
        try:
            guarda[(o, nm)] = getattr(o.par, nm).eval()
        except Exception:
            pass
    t0 = sm._SALA['t0']
    import copy
    # v27: el estado de sala del motor de FASE1 (personas, densidad y los contadores del sorteo
    # de la presencia), como estaba: la prueba mueve gente y juega la demo, y el sorteo de lo
    # que venga despues no debe depender de ella
    sala1 = copy.deepcopy(dict(t.m._SALA))
    try:
        _prueba(t, t.m)
    finally:
        t.m._SALA.clear()
        t.m._SALA.update(sala1)
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

    # 2. las personas (v30: las mueve la coreografia de cada demo; sin FASE1, sm.ensayo)
    c = sm.cfg()
    ev = sm.evitar_de(eq)
    T0 = sm.TITULO                      # la coreografia empieza al acabar el titulo

    def recorrido(cc):
        out = dict(dentro=True, lejos=True, quietos=0, mueven=0, n45=sm.personas(cc, T0 + 45.0, ev),
                   paradas=[s_[2] for i_ in range(sm.n_personas(cc)) for s_ in sm.plan(cc, i_, 80.0, ev)
                            if s_[4] and not s_[5]],
                   p3=sm.posicion(cc, 3, T0 + 5.0, ev), entradas=[])
        for k in range(160):
            for i_, x, z, h, andando in sm.personas(cc, 0.5 * k, ev):
                out['dentro'] = out['dentro'] and abs(x) <= hx - 0.3 and abs(z) <= hz
                out['lejos'] = out['lejos'] and all(math.hypot(x - p[0], z - p[2]) > 0.9 for p in ev)
                out['mueven'] += 1 if andando else 0
                out['quietos'] += 0 if andando else 1
        for i_ in range(sm.n_personas(cc)):
            tr = sm.plan(cc, i_, 80.0, ev)
            out['entradas'] += [s_ for k, s_ in enumerate(tr) if k > 0 and s_[4] and not tr[k - 1][4]]
        return out
    r1 = sm.ensayo(c, 'paseo', 80.0, recorrido)
    r2 = sm.ensayo(c, 'paseo', 80.0, recorrido)
    t.check('v30: paseo: las personas entran, pasean y se paran dentro de la sala, lejos de la esfera y del estrobo',
            r1['dentro'] and r1['lejos'] and r1['quietos'] > 0 and r1['mueven'] > 0 and 0 < len(r1['n45']) <= 8,
            '%d dentro a los 45 s' % len(r1['n45']))
    t.check('sin azar: la misma sala da la misma historia', r1['n45'] == r2['n45'])
    zx, zz = sm.zona(c)
    t.check('el publico se para en el suelo de la sala, lejos de las paredes (v8: en toda la sala)',
            r1['paradas'] and all(abs(x) <= zx + 1e-9 and abs(z) <= zz + 1e-9 for x, z in r1['paradas']),
            '%d paradas' % len(r1['paradas']))
    t.check('nadie esta dentro antes de llegar; se entra por la puerta',
            r1['p3'] is None and r1['entradas'] and all(s_[2] == (0.0, hz) for s_ in r1['entradas']),
            '%d entradas' % len(r1['entradas']))

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
    fr = sala.op('esfera').op('frente')
    try:
        fr_uv = ('uv' in [a.name for a in fr.pointAttribs] + [a.name for a in fr.vertexAttribs]
                 and not fr.errors() and not sala.op('esfera').op('frente_callbacks').errors())
    except Exception:
        fr_uv = False
    t.check('v19: la imagen de frente: el Script SOP frente pone las coordenadas de textura', fr_uv)
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
    obra_ = sm.obra(c, eq)              # v34: la pantalla (o la esfera, con Soporte = esfera)
    t.check('visitante: los ojos a 1,65 m y mirando la obra (v34: la pantalla, o la esfera)',
            abs(p[1] - sm.OJOS) < 1e-9 and esf is not None and mira == obra_)
    t.check('el monitor mira por la camara de la Vista', sm.vista('ty') == sm.OJOS
            and abs(sm.vista('mx') - obra_[0]) < 1e-9)
    sala.par.Vista = 'orbita'
    t.check('orbita: desde fuera, como la vista libre de antes', sm.vista('ty') == float(sala.par.Alturavista))
    sala.par.Vista = 'entrada'
    c = sm.cfg()
    t.check('v4: entrada, desde detras de la puerta y por encima de la gente, mirando hacia abajo y al fondo',
            sm.vista('tz') > hz and sm.vista('ty') > sm.OJOS and sm.vista('my') < sm.vista('ty')
            and sm.vista('mz') < 0.0)
    prueba_pantalla(t, c, eq, hx, hz)
    mg = sm.margen_esfera(c, eq)
    g0 = math.radians(sm.giro_esfera())             # 'frente' pone la imagen en el +Z de la bola
    hacia = (math.sin(g0), math.cos(g0))
    he = sm.hacia_esfera(c)
    a_entrada = (he[0] - esf['x'], he[1] - esf['z'])
    t.check('v14: el planeta mira a la camara de la entrada (Girosfera 0)',
            float(sala.par.Girosfera) != 0.0
            or hacia[0] * a_entrada[0] + hacia[1] * a_entrada[1] > 0.99 * math.hypot(*a_entrada),
            'giro %.0f grados' % sm.giro_esfera())
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
    sala.par.Monigotes = False
    c = sm.cfg()

    def troncos(cc):
        ps_ = sm.personas(cc, T0 + 45.0, ev)
        return ps_, sm._filas_personas(cc, eq, T0 + 45.0)
    ps, cue = sm.ensayo(c, 'paseo', T0 + 45.0, troncos)
    sm._PIEZAS['clave'] = None
    t.check('v5: sin Monigotes, el publico es un tronco por persona, de toda su altura (sin cabeza)',
            len(cue) == len(ps) > 0 and sala.op('cabezas') is None
            and all(abs(q[7] - p[3]) < 1e-9 for q, p in zip(cue, ps)))
    sala.par.Monigotes = True
    # v30: las demos de la sala (las que no necesitan FASE1 para poner a su gente)
    t.check('v30: Demo: paseo, probabilidad, huella, llena, genozilla y vacia; cada una con su seccion',
            sm.DEMOS == ['paseo', 'probabilidad', 'huella', 'llena', 'genozilla', 'vacia']
            and all(d_ in sm.SECCIONES for d_ in sm.DEMOS[:-1]) and 'vacia' not in sm.SECCIONES
            and [len(sm.casos(d_)) for d_ in sm.DEMOS[:-1]] == [1, 3, 2, 1, 13])
    sala.par.Personas = 18
    c = sm.cfg()

    def visita(cc):
        dentro, lejos, maximo, juntos = True, True, 0, 0
        for k in range(int(cc['_hasta'] / 0.5)):
            ps_ = sm.personas(cc, 0.5 * k, ev)
            maximo = max(maximo, len(ps_))
            ids = set(q[0] for q in ps_)
            juntos = max(juntos, len(ids & {4, 5, 6, 7}))
            for i_, x, z, h, andando in ps_:
                dentro = dentro and abs(x) <= hx - 0.3 and abs(z) <= hz
                lejos = lejos and all(math.hypot(x - p[0], z - p[2]) > 0.9 for p in ev)
        return dentro, lejos, maximo, juntos, len(sm.personas(cc, cc['_hasta'] - 0.5, ev))
    for demo, hasta in (('paseo', 82.0), ('huella', 26.0), ('llena', 120.0), ('vacia', 30.0)):
        c_ = dict(c, _hasta=hasta)
        if demo == 'vacia':
            sala.par.Demo = 'vacia'
            c_ = dict(sm.cfg(), _hasta=hasta)
            maximo = max(len(sm.personas(c_, 1.0 + 2.5 * k, ev)) for k in range(20))
            t.check('demo vacia: nadie en la sala', maximo == 0)
            continue
        dentro, lejos, maximo, juntos, al_final = sm.ensayo(c_, demo, hasta, visita)
        t.check('demo %s: el publico dentro de la sala y lejos de la esfera y del estrobo' % demo,
                dentro and lejos and maximo > 0, 'hasta %d a la vez' % maximo)
        if demo == 'paseo':
            t.check('v30: paseo: un grupo de cuatro entra junto, y al acabar la sala se ha vaciado',
                    juntos == 4 and al_final == 0, 'grupo %d, al final %d' % (juntos, al_final))
        elif demo == 'llena':
            t.check('v30: llena: Personas (18) en la sala a la vez casi todos, y al acabar se vacia',
                    maximo >= 15 and al_final == 0, 'hasta %d a la vez, al final %d' % (maximo, al_final))
    # v32: la sala llena se va llenando y solo forma una fila recta, la de LLENA_LINEA
    t.check('v32: la sala llena fija Modofila = recta (Minfila 3, Tfila 5) mientras dura',
            sm.SECCIONES['llena']['pars'] == dict(Modofila='recta', Minfila=3, Tfila=5.0))
    for n_ in (sm.LLENA_MIN, 18, sm.LLENA_MAX):
        co_ = sm._coreo_llena(n_, c)
        sitio_, pegados, maximo, t_ = {}, set(), 0, 0.0
        llenos = []
        while t_ <= sm.LLENA_DUR:
            for tt, i_, d_ in co_:
                if tt <= t_:
                    sitio_[i_] = d_
            q_ = sorted((i_, tuple(d_[1:])) for i_, d_ in sitio_.items() if d_ != 'fuera')
            maximo = max(maximo, len(q_))
            if t_ in (15.0, 30.0, 45.0):
                llenos.append(len(q_))
            for a_ in range(len(q_)):
                for b_ in range(a_ + 1, len(q_)):
                    (i_, p_), (j_, r_) = q_[a_], q_[b_]
                    if max(abs(p_[0] - r_[0]), abs(p_[1] - r_[1])) <= 1:
                        pegados.add((t_, i_, j_))
            t_ += 0.5
        l0, l1 = sm.LLENA_LINEA[3], sm.LLENA_LINEA[4]
        t.check('v32: llena con %d: entran poco a poco, nadie queda junto a otro fuera de la fila de %g a %g s, '
                'y al final se vacia' % (n_, l0, l1),
                llenos == sorted(llenos) and llenos[0] < llenos[-1] and maximo >= min(n_, 20)
                and all(l0 <= p_[0] <= l1 for p_ in pegados)
                and {(p_[1], p_[2]) for p_ in pegados} == {(0, 2), (1, 2)}
                and all(d_ == 'fuera' for d_ in sitio_.values()),
                'a los 15, 30 y 45 s %s; hasta %d; %d instantes con vecinos' % (llenos, maximo, len(pegados)))
    sala.par.Demo = 'paseo'
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
    t.check('la obra es una luz: luz_esfera, en su sitio (v34: delante de la pantalla) y con el color medio de su '
            'imagen (Luzesfera)',
            sala.op('luz_esfera') is not None and abs(sm.luz_esfera('ty') - sm.obra(c)[1]) < 1e-9
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
        # v23: palmadas que seguian en la cola (Palmada pulsado, o de otra prueba) entraban
        # todas en el primer bloque de calentamiento: el bloque de antes ya llevaba golpes
        # (pico 1,33) y la palmada de la prueba casi no subia el flujo (0,10). Cola vacia.
        cola = len(sm._SALA['manuales'])
        sm._SALA['manuales'] = []
        try:
            sm._SALA['forzar'] = True
            for _ in range(3):
                sm._SALA['forzar'] = True
                m.mic_tick(W, m.cfg(), absTime.seconds + 500.0)
            antes = W['mic']['n']
            pico_antes = float(np.max(np.abs(sm._SALA['audio']))) if sm._SALA['audio'] is not None else -1.0
            sm.palmada((mic[0] + 0.5, sm.BOCA, mic[2]))
            m.mic_tick(W, m.cfg(), absTime.seconds + 500.5)
            # v22: si falla, de donde se pierde la palmada: el bloque de la sala (sm._SALA['audio']),
            # lo que saca el CHOP audio_mic y lo que FASE1 lee de el (Fuentemic, Chopmic)
            xa = sm._SALA['audio']
            try:
                xc = audio.numpyArray()
                chop_txt = '%d canal(es) x %d muestras, pico %.3f, time slice %s' % (
                    xc.shape[0], xc.shape[-1], float(np.max(np.abs(xc))) if xc.size else 0.0,
                    getattr(audio, 'isTimeSlice', '?'))
            except Exception as e:
                chop_txt = 'no pude leerlo (%s)' % e
            cm = m.cfg()
            t.check('Palmada: FASE1 la oye por audio_mic y cuenta un onset', W['mic']['n'] == antes + 1,
                    'onsets %d -> %d, flujo %.2f (umbral %.2f) | bloque de la sala: %s muestras, pico %.3f '
                    '(antes %.3f), palmadas pendientes %d, en la cola al empezar %d | audio_mic: %s | FASE1: Fuentemic %s, Chopmic %s, '
                    'Canalmic %s'
                    % (antes, W['mic']['n'], W['mic'].get('flujo', 0.0), cm['umbral_onset'],
                       len(xa) if xa is not None else 0, float(np.max(np.abs(xa))) if xa is not None else -1.0,
                       pico_antes, sum(1 for q in sm._SALA['manuales'] if q[0] is None), cola, chop_txt,
                       cm.get('fuente_mic'), cm.get('chop_mic'), cm.get('canal_mic')))
        finally:
            W['mic']['t'] = t_onset
    t.check('leyenda SALA', sm.legend().startswith('SALA') and 'personas' in sm.legend())
    prueba_monigotes(t, m, eq)
    prueba_alimentar(t, m)
    prueba_genozilla(t, m)
    prueba_demos(t, m)


def prueba_alimentar(t, m):
    """v27: el publico de cualquier demo, en FASE1 y marcado en el globo; al apagar
    Alimentar, FASE1 como estaba."""
    F = sm.Fase1(fase1)
    tb = fase1.op('sala_personas')
    if tb is None or F.par('Fuente') is None:
        info('v27: sin la sala simulada de FASE1 (fase 22): no pruebo Alimentar')
        return
    sm.alimentar_sale(F)
    pars = ('Fuente', 'Modojuego', 'Marcapublico', 'Marcajugador')
    antes = dict((nm, F.par(nm)) for nm in pars if F.par(nm) is not None)
    fuente0, tabla0 = F.par('Fuente'), sm._tabla_de(tb)
    try:
        F.poner('Fuente', 'camara')
        fuente0 = F.par('Fuente')
        for nm in ('Modojuego',):
            F.poner(nm, False)
        for nm in ('Marcapublico', 'Marcajugador'):
            F.poner(nm, True)
        sala.par.Demo = 'llena'
        sala.par.Personas = 10
        sala.par.Activa = True
        sala.par.Alimentar = True
        c = sm.cfg()
        ev = sm.evitar_de(sm.equipos())

        def alimenta(cc):               # v30: la gente de la sala llena (sm.ensayo), sin el director
            sm._GZ['activo'] = False
            d_ = sm.personas(cc, 40.0, ev)
            return d_, sm.alimentar_tick(cc, F, 40.0)
        dentro, si = sm.ensayo(c, 'llena', 40.0, alimenta)
        filas = sm._tabla_de(tb)[1:]
        t.check('v27: Alimentar: en la demo llena, FASE1 pasa a Fuente = simulada y la tabla sala_personas '
                'lleva a cada persona de la sala',
                si and F.par('Fuente') == 'simulada' and len(filas) == len(dentro) > 0,
                'Fuente %s, %d filas, %d personas' % (F.par('Fuente'), len(filas), len(dentro)))
        import copy
        W = copy.deepcopy(m.world())        # una copia: la prueba no toca el mundo de FASE1
        c1 = m.cfg()
        now = absTime.seconds + 900.0
        for k in range(int(m.CAM_FPS * 3)):
            m.personas_tick(W, c1, now + k / float(m.CAM_FPS), m.sala_sim_imagen(c1, m.sala_personas()))
        gente = [p for p in m.personas_en_sala() if p.get('casilla') is not None]
        celdas = set(m.celda_de_casilla(W, c1, p['casilla']) for p in gente)
        marcas = m.build_instances(W, c1, now + 3.0).get('marcas', [])
        t.check('v27: sin Modojuego, FASE1 marca en el globo la celda de cada persona (un anillo por celda)',
                bool(gente) and len(marcas) == m.MARCA_SEGMENTOS * len(celdas),
                '%d personas en %d celdas, %d piezas de marca' % (len(gente), len(celdas), len(marcas)))
        sala.par.Alimentar = False
        no = sm.alimentar_tick(sm.cfg(), F, 41.0)
        t.check('v27: Alimentar apagado: FASE1 vuelve a su Fuente y a su tabla de antes',
                not no and F.par('Fuente') == fuente0 and sm._tabla_de(tb) == tabla0 and sm._pub_guardado() is None,
                'Fuente %s' % F.par('Fuente'))
    finally:
        sm.alimentar_sale(F)
        for nm, v in antes.items():
            F.poner(nm, v)
        tb.clear()
        for f in tabla0:
            tb.appendRow(f)
        m.sala_reset(cuentas=False)


def prueba_monigotes(t, m, eq):
    """v24: los monigotes, vistos por la camara cenital como los troncos (v30: con la gente
    del paseo, sm.ensayo)."""
    sala.par.Demo = 'paseo'
    sala.par.Monigotes = True
    sm.ensayo(sm.cfg(), 'paseo', 82.0, lambda cc: _prueba_monigotes(t, m, eq, cc))


def _prueba_monigotes(t, m, eq, c):
    import numpy as np
    ev = sm.evitar_de(eq)
    quietos, peor_h, fuera, sexo = 0, 0.0, 0, True
    for k in range(30):
        tt = 8.0 + 2.4 * k
        for i in range(8):
            e = sm.estado_persona(c, i, tt, ev)
            if e is None or e['andando']:
                continue
            h = sm.altura(i)
            pz = sm.piezas_monigote(i, e['x'], e['z'], h, e['rumbo'], e['andado'], False)
            sexo = sexo and (len(pz['conos']) == (i % 2)) and pz['bolas']
            img = sm.alturas_planta(np, pz, e['x'] - 0.4, e['z'] - 0.4, 0.8, 0.8, px=0.01)
            quietos += 1
            peor_h = max(peor_h, abs(float(img.max()) - h))
            fs, cs = np.nonzero(img > 0.01)
            X, Z = (cs + 0.5) * 0.01 - 0.4, (fs + 0.5) * 0.01 - 0.4
            a = e['rumbo']
            lat, fre = X * math.cos(a) - Z * math.sin(a), X * math.sin(a) + Z * math.cos(a)
            fuera += int(((np.abs(lat) > 0.5 * sm.TRONCO[0] + 0.01) | (np.abs(fre) > 0.5 * sm.TRONCO[1] + 0.01)).sum())
    t.check('v24: monigotes: la coronilla a la altura de la persona (3 cm) y la huella dentro de la del tronco '
            '(0,42 x 0,26 m, girado como ella); hombre las personas pares, mujer (vestido) las impares',
            quietos > 0 and peor_h <= 0.03 and fuera == 0 and sexo,
            '%d personas quietas, %.1f cm de diferencia como mucho, %d pixeles fuera' % (quietos, 100 * peor_h, fuera))
    c1 = m.cfg()
    x0, z0 = sm.de_suelo(c1, 0.0, 0.0)
    bien, cuentas = True, []
    for k in range(20):
        tt = 6.0 + 3.6 * k
        dentro, lejos = [], 0
        for i, x, z, h, _ in sm.personas(c, tt, ev):
            xf, yf = sm.a_suelo(c1, x, z)
            if 0.0 <= xf <= c1['ancho_sala'] and 0.0 <= yf <= c1['fondo_sala']:
                dentro.append((xf, yf))
            elif -0.15 <= xf <= c1['ancho_sala'] + 0.15 and -0.15 <= yf <= c1['fondo_sala'] + 0.15:
                lejos += 1              # en el borde: se le ve la cabeza o no
        # dos cabezas a menos de Separacioncabezas cuentan como una (fase 24)
        grupos = []
        for q in dentro:
            cerca = [g for g in grupos if any(math.hypot(q[0] - p_[0], q[1] - p_[1]) < c1['sep_cabezas'] for p_ in g)]
            for g in cerca:
                grupos.remove(g)
            grupos.append(sum(cerca, []) + [q])
        dentro = len(dentro)
        juntos = dentro - len(grupos)
        cuenta = []
        for mon in (True, False):
            sm._PIEZAS['clave'] = None
            pz = sm.piezas_personas(dict(c, monigotes=mon), eq, tt, t_arco=0)
            img = sm.alturas_planta(np, pz, x0, z0, c1['ancho_sala'], c1['fondo_sala'], px=0.02)
            cuenta.append(len(m.detectar_cabezas(img, c1)))
        bien = bien and dentro - juntos <= cuenta[0] <= dentro + lejos
        cuentas.append((dentro, cuenta[0], cuenta[1]))
    sm._PIEZAS['clave'] = None
    t.check('v24: la fase 24 cuenta cada monigote una vez en la imagen de la camara cenital (paseo, 8 personas; '
            'el tronco plano, de 0,42 m, salia dos veces)', bien,
            'personas en el suelo cubierto / monigotes contados / troncos contados: %s'
            % ' '.join('%d/%d/%d' % q for q in cuentas[:8]))
    andando, parados = [], []
    for k in range(200):
        tt = 3.0 + 0.35 * k
        for i in range(8):
            e = sm.estado_persona(c, i, tt, ev)
            if e is None:
                continue
            pz = sm.piezas_monigote(i, e['x'], e['z'], 1.75, e['rumbo'], e['andado'], e['andando'])
            (andando if e['andando'] else parados).append(max(abs(f[3]) for f in pz['cajas']))
    t.check('v24: las piernas se balancean al andar (15 grados) y quietos estan rectas',
            andando and 10.0 <= max(andando) <= sm.BALANCEO + 1e-6 and parados and max(parados) == 0.0,
            '%.1f grados como mucho andando, %d instantes' % (max(andando or [0.0]), len(andando)))
    medio = sm.filas_arco(0.0, 0.0, 0.5)
    t.check('v24: el arco de quietud se completa al cumplir su tiempo (Tfila), en el suelo y ambar',
            not sm.filas_arco(0.0, 0.0, 0.0) and len(medio) == sm.ARCO_SEGS // 2
            and len(sm.filas_arco(0.0, 0.0, 2.0)) == sm.ARCO_SEGS and all(f[1] < 0.02 for f in medio)
            and tuple(medio[0][9:12]) == tuple(sm.AMBAR))
    bb = medir(sala.op('personas_bolas/a_la_unidad')) if sala.op('personas_bolas/a_la_unidad') else None
    t.check('v26: la bola de los monigotes (cabeza y hombros), de diametro 1 y centrada',
            bb is not None and all(abs(v - w) < 0.02 for v, w in zip(bb, (-0.5, 0.5) * 3)),
            'medidas %s' % (None if bb is None else ['%.3f' % v for v in bb]))
    sm._PIEZAS['clave'] = None
    con = sm.piezas_personas(dict(c, arco_quietud=True), eq, sm.TITULO + 48.0, t_arco=4.0)
    sm._PIEZAS['clave'] = None
    t.check('v24: los monigotes y el arco, instanciados (personas, personas_bolas, personas_conos, arcos) y en la '
            'camara cenital (sin el arco)',
            all(sala.op(n_) is not None and sala.op('i_' + n_) is not None
                for n_ in ('personas', 'personas_bolas', 'personas_conos', 'arcos'))
            and all(n_ in str(sala.op('render_cenital').par.geometry.val).split()
                    for n_ in ('personas', 'personas_bolas', 'personas_conos'))
            and 'arcos' not in str(sala.op('render_cenital').par.geometry.val).split() and con['arcos'],
            '%d piezas de arco a los 50 s del paseo' % len(con['arcos']))


def prueba_genozilla(t, m):
    """v24: la demo GENoZilla en tiempo simulado, capitulo a capitulo; al acabar, FASE1
    como estaba."""
    import copy
    caps = sm.CAPITULOS
    t.check('v24: GENoZilla: 13 capitulos (unos 3 min 50 s); en los de las armas, solo la suya',
            len(caps) == 13 and 220.0 <= sum(cp['dur'] for cp in caps) <= 240.0
            and all([a for a in sm.ARMAS if caps[k]['pars'].get(a)] == [sm.ARMAS[k - 7]] for k in range(7, 12))
            and not any(caps[k]['pars'].get(a) for k in list(range(7)) + [12] for a in sm.ARMAS),
            '%.0f s' % sum(cp['dur'] for cp in caps))
    sala.par.Demo = 'genozilla'
    sala.par.Guion = True
    motor_ = fase1.op('motor')
    # v27: la demo juega sobre el mundo de FASE1; si esta casi vacio (un proyecto recien
    # montado), uno compuesto para la prueba. v33: la demo ya no entierra conchas para sus
    # zanjas (espera a que el mundo las tenga): la prueba deja que el mundo evolucione hasta
    # tenerlas (evolucionar). Al acabar, FASE1 vuelve a su mundo.
    Worig = copy.deepcopy(motor_.fetch('W', None))
    cambiado = False
    try:
        cambiado = componer_mundo(m)
        cambiado = evolucionar(m, 14) > 0 or cambiado
        _prueba_genozilla(t, m, copy, caps, motor_)
    finally:
        if cambiado:
            motor_.store('W', Worig)
            for k_ in ('inst', 'tiles', 'frame'):
                m._CACHE[k_] = None


def prueba_pantalla(t, c, eq, hx, hz):
    """v34: la pantalla proyectada, arriba a la izquierda, entera en la vista entrada."""
    r = sm.pantalla_rect(c)
    t.check('v34: Soporte = pantalla por defecto; la pantalla, pegada a la pared del fondo, a la de la izquierda y '
            'al techo, 16:9, con el planeta unas tres veces la esfera de 1 m',
            str(sala.par.Soporte.default) == 'pantalla' and sm.es_pantalla(c)
            and abs(r['x0'] + hx - sm.PANT_MARGEN) < 1e-9 and abs(r['y1'] - (c['alto'] - sm.PANT_MARGEN)) < 1e-9
            and abs(r['z'] + hz - sm.PANT_SEPARA) < 1e-9 and abs(r['w'] / r['h'] - 16.0 / 9.0) < 1e-6
            and 0.85 * r['h'] >= 2.8 and r['x1'] <= hx,
            '%.2f x %.2f m, planeta %.2f m' % (r['w'], r['h'], 0.85 * r['h']))
    pan = sala.op('pantalla')
    lz = pan.op('lienzo') if pan is not None else None
    err_uv = []
    uvs = uvs_lienzo(lz, err_uv)
    t.check('v34: la pantalla lleva el render entero de FASE1 (mat_pantalla, Color Map = imagen_fase1, uv de 0 a 1) '
            'y se coloca y escala sola (sala_motor.pantalla)',
            pan is not None and str(sala.op('mat_pantalla').par.colormap.val).split('/')[-1] == 'imagen_fase1'
            and uvs == [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
            and abs(float(pan.par.sx.eval()) - r['w']) < 1e-6 and abs(float(pan.par.ty.eval()) - r['cy']) < 1e-6
            and float(pan.par.scale.eval()) == 1.0 and float(sala.op('esfera').par.scale.eval()) < 1e-3
            and all(n_ in str(sala.op(rn).par.geometry.val).split() for rn in ('render_sala', 'render_plano')
                    for n_ in ('pantalla', 'esfera')),
            'uv %s; lienzo: %s%s' % (uvs, diag_lienzo(lz), ('; al leer la uv: ' + err_uv[0]) if err_uv else ''))
    # entera en la vista entrada: sus cuatro esquinas dentro del cuadro (80 grados, 16:9)
    p, m_ = sm.vista_entrada(c, None, 'entrada')

    def dentro(q, fov_h=80.0, asp=1280.0 / 720.0):
        f = [m_[k] - p[k] for k in range(3)]
        lf = math.sqrt(sum(v * v for v in f))
        f = [v / lf for v in f]
        der = [-f[2], 0.0, f[0]]
        ld = math.sqrt(sum(v * v for v in der))
        der = [v / ld for v in der]
        arr = [der[1] * f[2] - der[2] * f[1], der[2] * f[0] - der[0] * f[2], der[0] * f[1] - der[1] * f[0]]
        d = [q[k] - p[k] for k in range(3)]
        z_ = sum(a * b for a, b in zip(d, f))
        th = math.tan(math.radians(0.5 * fov_h))
        return z_ > 0 and abs(sum(a * b for a, b in zip(d, der)) / z_) <= th \
            and abs(sum(a * b for a, b in zip(d, arr)) / z_) <= th / asp
    esquinas = [(x, y, r['z']) for x in (r['x0'], r['x1']) for y in (r['y0'], r['y1'])]
    t.check('v34: desde la entrada se ve la pantalla entera (sus cuatro esquinas en el cuadro)',
            all(dentro(q) for q in esquinas), ' '.join('%s' % dentro(q) for q in esquinas))
    e_ = next(e for e in eq if e['tipo'] == 'esfera')
    peana = lambda c_: [f_ for f_ in sm._filas_equipos(c_, eq, 5.0)         # noqa: E731
                        if abs(f_[0] - e_['x']) < 1e-9 and abs(f_[2] - e_['z']) < 1e-9]
    t.check('v34: con la pantalla, la esfera y su peana no se dibujan; con Soporte = esfera, si',
            not peana(c) and len(peana(dict(c, soporte=1))) == 1 and sm.obra(dict(c, soporte=1), eq) == e_['pos'])


def evolucionar(m, conchas):
    """v33: el mundo de FASE1 como si hubiera evolucionado hasta tener al menos 'conchas'
    losetas debajo de cada celda (lo que harian sus ciclos con el tiempo), con la misma
    superficie (_demo_conchas del motor). Solo para la autoprueba (que luego devuelve el
    mundo). Devuelve las conchas enterradas."""
    W = m.world()
    n = m._demo_conchas(W, dict(m.cfg(), presencia_activa=False), W.get('t') or 0.0, conchas, range(m.N))
    if n:
        for k_ in ('inst', 'tiles', 'frame'):
            m._CACHE[k_] = None
    return n


def evoluciona(F, demo, k, que):
    """v33: para simular_demo, que juega sin el giro del planeta ni sus ciclos: un caso que
    espera ve evolucionar la copia del mundo de la autoprueba como la veria en la sala
    (conchas nuevas debajo; celdas vacias que el giro trae bajo la sala)."""
    m = F.m
    if 'conchas' in que:
        evolucionar(m, len(m.world()['shells']) + 6)
        return
    W, c1 = F.W(), F.cfg()
    cols, filas = m.rejilla_sala(c1)
    centro = m.celda_de_casilla(W, c1, m.demo_casilla(c1, 6.0, 4.0))
    lejos = m.celda_de_casilla(W, c1, m.demo_casilla(c1, 1.0, 7.0))
    celdas = [x for x in [centro, lejos] + list(m.NEIGH[centro] if centro is not None else ()) if x is not None]
    m._demo_despejar(W, dict(c1, presencia_activa=False), celdas)
    for k_ in ('inst', 'tiles', 'frame'):
        m._CACHE[k_] = None


def componer_mundo(m, minimo=12):
    """v27: si el mundo de FASE1 tiene menos de 'minimo' celdas ocupadas, siembra una de
    cada tres (ocupacion 1 a 6, las dos especies). Devuelve si lo hizo."""
    W = m.world()
    if m.occupied(W) >= minimo:
        return False
    c = dict(m.cfg(), presencia_activa=False)
    now = W.get('t') or 0.0
    for i in range(0, m.N, 3):
        for _ in range(1 + (i // 3) % 6):
            m.subir_escalon(W, c, m.GEO if i % 2 else m.ARQ, i, 100, now)
    W['dirty'] = True
    return True


def _prueba_genozilla(t, m, copy, caps, motor_):
    W0 = copy.deepcopy(motor_.fetch('W', None))
    antes = dict((nm, getattr(fase1.par, nm).eval()) for nm in sm.ARMAS + ('Fuente', 'Modojuego', 'Tfila',
                                                                          'Barsperturn'))
    vista0 = str(sala.par.Vista.eval())
    F = sm.Fase1(fase1)
    res = sm.simular_demo(sm.cfg(), F, evoluciona=evoluciona)
    for k, bien, que in res:
        t.check('v24: GENoZilla %d %s: %s' % (k, caps[k]['nombre'], COMPRUEBA[k]), bien, que)
    t.check('v24: GENoZilla: se juegan los 13 capitulos', len(res) == 13, '%d' % len(res))
    cons = list(sm._GZ.get('conservas') or [])
    t.check('v27: cada capitulo empieza en el mundo de FASE1: sus celdas ocupadas (menos las que despeja) '
            'siguen con su ocupacion o mas',
            len(cons) == 13 and all(n > 0 and si >= 0.8 * n for _, si, n in cons),
            ' '.join('%d:%d/%d' % x for x in cons))
    W1 = motor_.fetch('W', None)
    despues = dict((nm, getattr(fase1.par, nm).eval()) for nm in antes)
    tb = fase1.op('escenas')
    hueco = [r for r in range(tb.numRows) if tb[r, 0].val == sm.GZ_HUECO] if tb is not None else []
    t.check('v24: al salir de la demo FASE1 queda como estaba: el mismo mundo (Guardarescena / Cargarescena en '
            'antes_demo), las armas, Fuente, Modojuego, Tfila y el giro; y la Vista de la sala',
            W1 == W0 and despues == antes and not hueco and str(sala.par.Vista.eval()) == vista0
            and sm._guardado() is None,
            '' if despues == antes else 'antes %s, despues %s' % (antes, despues))
    g = dict(sm._GZ)
    try:
        sm._GZ.update(activo=True, cap=5, demo='genozilla', t_titulo=100.0, t0=100.0 + sm.TITULO)
        alfas = [sm.alfa_titulo(100.0 + u) for u in (0.1, 1.0, 2.6, 3.0)]
        rot = sm.rotulo_texto(100.0 + sm.TITULO + 3.5, F)
        ante = sm.titulo_texto('ante')
    finally:
        sm._GZ.clear()
        sm._GZ.update(g)
    t.check('v24: el titulo de cada capitulo: 2,8 s con fundido de entrada y de salida, y su antetitulo',
            0.0 < alfas[0] < 0.5 and alfas[1] == 1.0 and 0.0 < alfas[2] < 1.0 and alfas[3] == 0.0
            and ante == 'FORMA DE JUGAR 5 / 11', '%s  %s' % (['%.2f' % a for a in alfas], ante))
    t.check('v24: el rotulo explica lo que pasa, con los tiempos de FASE1 (Tfila)',
            ('%g segundos' % fase1.par.Tfila.eval()) in rot, rot)
    sala.par.Vista = 'juego'
    t.check('v24: Vista = juego: la sala desde la entrada y la imagen de FASE1 lado a lado (monitor_base), con el '
            'titulo y el rotulo encima del monitor',
            sm.vista('fov') == sm.FOV_JUEGO and sm.ojos(sm.cfg())[0][2] > 0.0
            and all(sala.op(n_) is not None for n_ in ('juego_lado', 'monitor_base', 'titulo_demo', 'rotulo_demo',
                                                       'con_titulo', 'con_rotulo_demo'))
            and sala.op('monitor_sala').inputs and sala.op('monitor_sala').inputs[0] == sala.op('con_titulo'))


def prueba_demos(t, m):
    """v30: las demos de secciones y casos en tiempo simulado, con FASE1 de verdad: cada
    caso hace lo que cuenta su rotulo; al salir, FASE1 como estaba. Y la camara que sigue
    a las celdas sin cambiar de altura."""
    import copy
    motor_ = fase1.op('motor')
    Worig = copy.deepcopy(motor_.fetch('W', None))
    cambiado = False
    try:
        cambiado = componer_mundo(m)
        _prueba_espera(t, m, motor_)            # v33: antes de evolucionar (con las conchas que haya)
        cambiado = evolucionar(m, 6) > 0 or cambiado
        _prueba_demos(t, m, copy, motor_)
    finally:
        if cambiado:
            motor_.store('W', Worig)
            for k_ in ('inst', 'tiles', 'frame'):
                m._CACHE[k_] = None
        m.foco_camara(None)
        m._CACHE.pop('foco_dir', None)


def _prueba_espera(t, m, motor_):
    """v33: ninguna demo toca el giro; y un caso al que le falta algo del mundo espera,
    con el titulo que lo dice."""
    con_giro = [cp['nombre'] for sec in sm.SECCIONES.values() for cp in sec['casos'] if 'Barsperturn' in cp['pars']]
    t.check('v33: ninguna demo cambia Barsperturn (el planeta gira con los parametros de FASE1) ni guarda el '
            'mundo para devolverlo',
            not con_giro and 'Barsperturn' not in sm.PARS_CAPITULO and not hasattr(sm, 'GIRO_DEMO')
            and not any('Barsperturn' in sec['pars'] for sec in sm.SECCIONES.values())
            and 'W' not in (sm._guardado() or {}),
            ', '.join(con_giro))
    F = sm.Fase1(fase1)
    W, c1 = F.W(), dict(F.cfg(fresca=True), conchas_persona=1)
    lib = sm.casillas_libres(sm.cfg(), c1, m, sm.evitar_de(sm.equipos_o_defecto(sm.cfg())))
    refs = sm.refs_caso('huella', 1, c1, F, W, lib)
    hay = m.losetas_bajo(W, refs['fila_celdas'])
    falta = sm.falta_caso('huella', 1, F, c1, W, refs)
    t.check('v33: La fila cava pide 5 conchas debajo de la fila; sin ellas, espera (y no las entierra)',
            (falta is None) == (hay >= 5) and (falta is None or 'conchas' in falta)
            and m.losetas_bajo(F.W(), refs['fila_celdas']) == hay,
            'hay %d: %s' % (hay, falta or 'puede cavar'))
    g = dict(sm._GZ)
    try:
        sm._GZ.update(activo=True, cap=1, demo='huella', t_titulo=100.0, t0=100.0 + sm.TITULO, cabecera=None,
                      espera=dict(cap=1, que='hacen falta 5 conchas debajo para que la fila cave (hay 2)',
                                  desde=100.0, revisa=102.0))
        txt = (sm.titulo_texto('nombre'), sm.titulo_texto('sub'), sm.alfa_titulo(130.0), sm.rotulo_texto(130.0),
               sm.cabecera_lineas(F))
    finally:
        sm._GZ.clear()
        sm._GZ.update(g)
    t.check('v33: mientras espera, el titulo lo dice entero (Esperando que el mundo evolucione) para probar el '
            'caso y que le falta',
            txt[0] == 'Esperando que el mundo evolucione' and txt[1].startswith('para probar La fila cava: hacen falta')
            and txt[2] == 1.0 and txt[3] == '' and 'esperando que el mundo evolucione' in txt[4],
            ' | '.join(str(x) for x in txt).replace(chr(10), ' / '))


def _prueba_demos(t, m, copy, motor_):
    F = sm.Fase1(fase1)
    t.check('v31: Demo vacia y Siguecamara apagado por defecto (las demos toman FASE1: se eligen a mano)',
            sala.par.Demo.default == 'vacia' and not sala.par.Siguecamara.default,
            'Demo %s, Siguecamara %s' % (sala.par.Demo.default, sala.par.Siguecamara.default))
    nombres = sorted(set(sm.PARS_CAPITULO) | set(sm.PARS_SECCION))
    sala.par.Personas = 14
    for demo in ('paseo', 'probabilidad', 'huella', 'llena'):
        W0 = copy.deepcopy(motor_.fetch('W', None))
        antes = dict((nm, F.par(nm)) for nm in nombres if F.par(nm) is not None)
        vista0 = str(sala.par.Vista.eval())
        sala.par.Demo = demo
        res = sm.simular_demo(sm.cfg(), F, demo=demo, evoluciona=evoluciona)
        cs = sm.casos(demo)
        for k, bien, que in res:
            t.check('v30: demo %s, caso %d %s' % (demo, k + 1, cs[k]['nombre']), bien, que)
        W1 = motor_.fetch('W', None)
        despues = dict((nm, F.par(nm)) for nm in antes)
        t.check('v30: demo %s: se juegan sus %d casos y al salir FASE1 queda como estaba (la autoprueba devuelve el mundo; los parametros '
                'y la Vista de la sala)' % (demo, len(cs)),
                len(res) == len(cs) and W1 == W0 and despues == antes and str(sala.par.Vista.eval()) == vista0
                and sm._guardado() is None,
                '' if despues == antes else 'antes %s, despues %s' % (
                    dict((k_, v) for k_, v in antes.items() if despues.get(k_) != v),
                    dict((k_, v) for k_, v in despues.items() if antes.get(k_) != v)))
    # el titulo y la cabecera de cada seccion y caso
    g = dict(sm._GZ)
    try:
        sm._GZ.update(activo=True, cap=1, demo='probabilidad', t_titulo=100.0, t0=100.0 + sm.TITULO,
                      reg=dict(p_ahora=0.43, p_control=0.2, llueve=dict(testigo=[10, 4], control=[10, 2])),
                      cabecera=None)
        ante = sm.titulo_texto('ante')
        nom = sm.titulo_texto('nombre')
        cab = sm.cabecera_lineas(F)
        sm._GZ.update(cap=0, demo='paseo')
        ante1 = sm.titulo_texto('ante')
    finally:
        sm._GZ.clear()
        sm._GZ.update(g)
    # v31: las entradas de con_titulo y de con_cabecera, por nombre (lo que haya en cada una)
    cadena = [entrada(sala.op('con_titulo'), 0), entrada(sala.op('con_titulo'), 1),
              entrada(sala.op('con_cabecera'), 0), entrada(sala.op('con_cabecera'), 1)]
    t.check('v30: cada caso con su titulo (la seccion y el caso) y la cabecera arriba a la derecha con la seccion, '
            'el caso y la probabilidad medida',
            # v31: el punto medio, escapado (\u00b7): exec(open(...).read()) lee este archivo en
            # cp1252 en Windows y un '·' literal llegaba como 'Â·' (sala_motor se lee en utf-8)
            ante == u'STRATOS \u00b7 2 \u00b7 ESTRATO HUMANO \u00b7 CASO 2 / 3' and nom == 'Una persona quieta'
            and ante1 == u'STRATOS \u00b7 1 \u00b7 PASEO' and cab.startswith(u'2 \u00b7 ESTRATO HUMANO')
            and 'P 0,43' in cab
            and 'prenden 4/10' in cab and sala.op('cabecera_demo') is not None
            and cadena == ['titulo_fundido', 'con_cabecera', 'cabecera_fundido', 'con_rotulo_demo'],
            '%s | %s | %s | con_titulo <- %s' % (ante, ante1, cab.replace(chr(10), ' / '), ' / '.join(cadena)))
    # v30 (motor v140): la camara sigue a las celdas, a la misma distancia (con un reloj a mano)
    m._CACHE.pop('foco_dir', None)
    giro_p = m._giro_planeta()
    dots = [(m._dot(m._norm(m.world_dir(m.NORMALS[i], *giro_p)), m.CAM_DIR), i) for i in range(m.N)]
    lejos = min((d_, i) for d_, i in dots if d_ > 0.35)[1]      # a unos 65 grados del frente
    now, dt = 5000.0, 1.0 / 30.0
    for k in range(240):
        m.foco_camara([lejos], t=now)
        now += dt
        cur = m._dir_foco(dt, now)
    obj = m.foco_objetivo(now)
    ang = math.degrees(math.acos(max(-1.0, min(1.0, m._dot(cur, obj)))))
    giro = math.degrees(math.acos(max(-1.0, min(1.0, m._dot(cur, m.CAM_DIR)))))
    m._CACHE.pop('cam_frame', None)
    st = m.camera_state()
    dist = math.sqrt(sum(v * v for v in st['pos']))
    t.check('v30 (motor v140): con foco, la camara de globo gira hacia la celda (a menos de 3 grados en 8 s; como '
            'mucho %g grados del frente) a la misma distancia del planeta' % m.FOCO_MAX,
            ang < 3.0 and 5.0 < giro <= m.FOCO_MAX + 0.5
            and (st['w'] > 0.0 or st['wr'] > 0.0 or abs(dist - st['d']) < 1e-6),
            'a %.1f grados del objetivo, %.1f del frente, distancia %.3f (d %.3f)' % (ang, giro, dist, st['d']))
    m.foco_camara(None)
    for k in range(400):
        now += dt
        cur = m._dir_foco(dt, now)
    giro = math.degrees(math.acos(max(-1.0, min(1.0, m._dot(cur, m.CAM_DIR)))))
    t.check('v30 (motor v140): sin foco, la camara vuelve a su sitio', giro < 1.0, '%.2f grados' % giro)
    m._CACHE.pop('foco_dir', None)
    m._CACHE.pop('cam_frame', None)


COMPRUEBA = ['marca de jugador en la celda de cada persona', 'ocupacion en las celdas con gente y una corona',
             'un brote del mal y el monstruo en forma grande', 'el brote crece y desborda a sus vecinas',
             'rescatado: geologia o arquitectura con su ocupacion', 'cae (acum 0) y la zanja queda fijada',
             'muere ahogado y aparece otro', 'acorralado pierde acum; si alguien se va, se escapa',
             'el pisoton le baja acum de 8', 'petrificado', 'el grito abre un pozo en su celda y cae',
             'aturdido y un relampago', 'un resultado de ronda y la noche']


def distancia_xz(a, b):
    return math.hypot(a['x'] - b['x'], a['z'] - b['z'])


run_test(fase1, prueba)
print('  Ahora: mira salida_sala (todo en una imagen; Vista = entrada, visitante, orbita,')
print('  cenital o juego). Modoluz = prueba recorre la luz en un minuto; Bruma, los haces en el aire.')
print('  Demo: 1 paseo, 2 probabilidad (estrato humano), 3 huella, 4 llena, 5 genozilla: cada una con')
print('  sus casos y su titulo (Vista = juego); con Siguecamara la camara de FASE1 sigue a las celdas.')
print('  Demo = vacia (por defecto). Ninguna demo reinicia el mundo ni toca el giro: lo toman donde esta;')
print('  si le falta algo a un caso, su titulo dice: Esperando que el mundo evolucione.')
print('  Palmada: la oye FASE1. Personas y Ruidopublico para mas o menos publico.')
print('  ' + sm.legend())
print('=' * 66)
