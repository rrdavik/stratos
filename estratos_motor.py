# =============================================================================
# ESTRATOS - MOTOR
# =============================================================================
# Este archivo se carga dentro del Text DAT 'motor' de /project1/FASE1.
# Lo cargan los scripts de fase (fase3 ... fase10); no se ejecuta solo.
#
# Contiene TODA la logica del mundo, en dos bloques:
#
#   1. NUCLEO     Python puro: ocupacion, desbordamiento, especies, ciclo,
#                 erosion e impulso, conchas, cortes y la piel tematica (fase 11:
#                 catalogo de modelos, clusters, compuestos y transitos;
#                 fase 12: material por la velocidad, vigor por el gate;
#                 fase 13: rios y carreteras; fase 14: aranazos tematicos,
#                 escalada, incendio y derrumbes; fase 15: el ciclo como era:
#                 entierro tematico, registro y herencia; fase 16: lo que
#                 ensenan los cortes y la union de cortes; fase 17: el tiempo
#                 en el paisaje: pulso, transporte y frente; fase 18: escenas,
#                 luz local y capas de diagnostico; fase 19: las senales del
#                 modular; motor v46: la naturaleza legible, con el relieve en
#                 un mapa de alturas, bosques por colonizacion del espacio,
#                 pisos de color por altitud y rios azules por el suelo real;
#                 motor v52: la vegetacion sale de una biblioteca de ejemplares
#                 con biomas por latitud, y los hibridos son mesetas construidas:
#                 arrozal en terrazas y meseta-jardin; motor v53: conchas
#                 discretas, el suelo oscuro y la tapa neutra; motor v54: el
#                 SEQ2 con Filtrar2 y Nota2, como el SEQ1 con Filtrar y Nota;
#                 fase 21, motor v55: el microfono de la sala, un pad 9 de
#                 erosion que golpea con los onsets del publico; motor v56:
#                 Fuentemic = chop, el audio de cualquier CHOP, como la sala
#                 virtual; motor v57: mic_sim y mic_flujo fuera del modo Time
#                 Slice de su entrada; motor v58: la pagina Fase3 con seis
#                 parametros menos: Growstep sale de Semillafrac y Umbralram,
#                 Gatemax 1 apaga el gate, Balanceo 0 apaga el balanceo y
#                 Luzconchas es la intensidad de la luz de las conchas; motor
#                 v59: la pagina Fase4 con 4 parametros: los umbrales salen de
#                 Umbralram y Pasoumbral, Satelite es tamano y altura del
#                 satelite y la vecina la eligen siempre velocidad + ocupacion;
#                 motor v60: la pagina Fase6 con 9 parametros: el compas sale
#                 de la linea de tiempo, Giromin 1 apaga el giro vivo y la
#                 memoria del territorio queda en 8 compases; motor v61: la
#                 pagina Fase7 con 12 parametros: Luzdrum 0, Velref 0 y
#                 Pumpamt 0 apagan la luz, la velocidad y el pumping, y
#                 Multradio, Pumphold y Pumpvelmin quedan fijos; motor v62: la
#                 pagina Fase8 con 11: Paletaalterna y Contrasteocupada
#                 fijos, y la luminosidad de la tapa sale de Paletaluz; motor
#                 v63: la pagina Fase11 con 35: Rebote, Maxcaosnat, Varangulo,
#                 Cuantizar30, Inclinacion, Densidadhoja y Muroterraza, fijos;
#                 motor v64: la pagina Fase13 con 12: el ancho maximo de un
#                 rio es 3,4 x Anchorio y Pendientemin queda en 0,01; motor
#                 v65: la pagina Fase21 con 10: Refractariomic (0,12 s) y
#                 Ventanaruido (60 s), fijos; motor v66: sin la simulacion
#                 de la fase 21 (mic_sim): Fuentemic es microfono o chop, y
#                 la sala virtual hace de publico; motor v67, fase 11 v10:
#                 la ciudad legible: una biblioteca de edificios por
#                 gramatica (un tipo por etapa, con variantes; la fachada en
#                 el shader), lenguajes por latitud, la obra entre etapas,
#                 colonia y marco como construcciones mutantes y torres que
#                 se buscan en los clusters; motor v68, fase 11 v11: el tema
#                 industria, con mina y energia, recurso de la concha de abajo,
#                 epoca por las eras, corta y planta integrada, vias y red
#                 electrica (fase 13), grisu y apagon (14), y su sitio en las
#                 fases 15 a 19).
#                 Motor v81, fase 22: la camara cenital (casilla probable):
#                 la densidad de cada casilla del suelo, el mapeo sala ->
#                 planeta y el sorteo (mapa logistico) de cada senal.
#                 Motor v82, fase 23: la luz de la sala: el balance entre
#                 erosion y creacion, el bano, el estroboscopio con su
#                 limitador de destellos, la noche del fin de ciclo y el colapso.
#                 Motor v83, fase 24 (plan v5): personas: cabezas (maximos de
#                 altura), seguimiento, ocupacion binaria por casilla y la celda
#                 que mira a cada casilla.
#                 Motor v84, fase 25: la huella minima: inclusiones por llegada
#                 (Probllegada, mapa logistico) y por parada (Tparada), con el
#                 escalon de su celda; la paleta humana y sus instancias.
#                 Motor v85, fase 26: el borrado: una inclusion desaparece
#                 cuando la erosion baja su celda de su escalon (y, en una
#                 celda sin construir, con cualquier golpe que la alcance).
#                 Motor v86, fase 27: la clasificacion al enterrar: estrato
#                 humano o concha limpia, el recuento horneado en el material
#                 de cada loseta y el colapso como marca de cierre.
#                 Motor v87, fase 28: la noche de enterramiento: durante Noche
#                 segundos la esfera se apaga y solo emiten las inclusiones
#                 recien horneadas (y las escisiones).
#                 Motor v88, fase 29: la fila (Minfila personas contiguas
#                 durante Tfila) y la escision colectiva: un hueco permanente
#                 en la columna de la celda de origen, con su fulgurita.
#                 Motor v89, fase 30: el relampago: un destello blanco con
#                 prioridad al abrirse cada escision.
#                 Motor v90, fase 31: las escisiones en el historico: el
#                 testigo (la seccion por el origen, dibujada con numpy), la
#                 columna resumen de la jornada y el registro.
#                 Motor v91: la sala simulada se lee al momento y la primera
#                 lectura diferida de la camara tras sala_reset o un cambio de
#                 Fuente se tira (era la imagen de antes: una sala vacia
#                 heredaba la densidad de la ultima persona).
#                 Motor v92, fase 10 v12: la camara rasante (Modocamara =
#                 rasante): a ras de suelo, con gran angular y anclada al
#                 planeta, por el paralelo entre dos anillos. El motor entrega
#                 el giro de la camara (cam('rot'), ya sin Look At) y su FOV
#                 (cam('fovcam'); el del globo es el parametro Camfov).
#                 Motor v93: cfg_malla(), la configuracion de las mallas de la
#                 biblioteca con solo los parametros que las cambian. Sus
#                 Script SOP pedian cfg() entero y quedaban colgados de todos
#                 los parametros: Loncentral (fase 22) sigue al giro, y con el
#                 planeta girando las 160 mallas se rehacian en cada fotograma
#                 (1 s por fotograma en TouchDesigner).
#                 Motor v94: la camara rasante, tumbada: por defecto mira al
#                 cenit (Rasmirada 90) con 140 grados (Rasfov) y flota mas alta
#                 (Rasaltura 0,6), sobre el suelo mas alto de las celdas de los
#                 lados, de las de delante y de las de detras (antes solo las
#                 dos de al lado: la pared de la celda siguiente tapaba el cuadro).
#                 Motor v95: ojo de pez (Rasojo): con la camara rasante, el
#                 Render TOP pasa a su modo Fish-Eye (180): un solo render con
#                 180 grados alrededor de adonde mira la camara (al cenit: el
#                 horizonte entero en el borde del circulo). Rasfov no cuenta.
#                 Motor v96: cada camara con sus ajustes (CAMARAS): al elegir
#                 Modocamara se ponen los de ese modo. Rasojo, apagado de fabrica.
#                 Motor v97: Sensor = femto (orbbec1) o kinect (kinect1, la
#                 Kinect v2); sin aparato (errores o avisos en su TOP, o sin
#                 imagen) la camara no se lee: densidad 0 y 'sin camara'.
#                 No toca TouchDesigner.
#                 Motor v97, fase 11 v14: el oceano (Oceano: las celdas vacias son mar
#                 y cada celda ocupada una isla que crece con la ocupacion, se une a
#                 sus vecinas por istmos y suelta islotes: archipielagos), los volcanes
#                 (Volcanes: crater, lava en el canal a del mapa de alturas, penacho y
#                 erupciones), ocho arboles y dos matorrales mas (23 plantas), cada
#                 una con su verde, su corteza y sus flores, y Detalle: las hojas de
#                 verdad tambien desde el globo, con el presupuesto a cargo de la GPU.
#                 Motor v98 (visto en TouchDesigner): las islas no pasan de su celda
#                 (con el mundo lleno seguia sin verse el mar) y los istmos son mas
#                 estrechos y desde 3; el abedul, con mas hoja y la corteza blanca solo
#                 en el fuste y las ramas madre.
#                 Motor v99, fase 11 v16: el planeta, el doble de grande (el nucleo de 6 a
#                 12: las celdas el doble de anchas, con las formaciones del mismo tamano:
#                 sitio para el detalle); el mapa de alturas se compone por capas guardadas
#                 (solo se rehace lo que cambia: de mas de 100 ms por nota a unos 15); la
#                 PRADERA, cientos de miles de matas que coloca la tarjeta grafica (el motor
#                 no calcula ninguna), y hasta 24 arboles por celda de bosque.
#                 Motor v100, comun v78, fase 11 v17: tierra en vez de losetas. Con Oceano
#                 la sedimentacion solo cubre lo que se creo o se desbordo en ese mundo: el
#                 mar no se entierra, y la tierra sube era a era sobre el. El nivel del mar es
#                 el del suelo mas bajo (nivel_mar): una celda con sedimento y sin nada encima
#                 es tierra desnuda, no agua. Las conchas se dibujan como capas de tierra
#                 (Tierra: mat_piel_estrato) y la celda que suena ilumina su suelo.
#   2. ADAPTADOR  Lo que habla con TouchDesigner: lee parametros, recibe
#                 MIDI, alimenta los Script CHOP de instancias, la leyenda.
#
# Cada bloque del nucleo se activa con el NIVEL (parametro Nivel, pagina
# Estratos), que fija el script de la ultima fase aplicada. Asi la fase 3
# se comporta como fase 3 aunque el motor ya sepa hacer la 10.
#
# El estado del mundo vive en el storage de este DAT ('W'): sobrevive a
# guardar el .toe y a recargar el motor.
# =============================================================================

MOTOR_VERSION = 'motor v102'

import math
import time as _time

# La reticula la decide el rango de notas (ver set_grid): N cambia.
POLO_SUR_DEF, POLO_NORTE_DEF = 24, 108     # do1 y do8 (MIDI 60 = do4)
FUERA_MODES = ['plegar', 'ignorar', 'limitar']
N = 0

NOTE_NAMES = ['do', 'do#', 're', 're#', 'mi', 'fa',
              'fa#', 'sol', 'sol#', 'la', 'la#', 'si']

GEO, ARQ, HIB = 1, 2, 3
SPECIES_NAME = {0: '-', 1: 'geo', 2: 'arq', 3: 'hib'}

INST_CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']
DUMMY_ROW = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]

# Perfiles de erosion por defecto: (reduccion, radio, profundidad)
#   reduccion    notas de construccion que deshace en la celda objetivo
#   radio        anillos de vecinas afectadas (cada anillo, la mitad)
#   profundidad  conchas que atraviesa el corte (fase 9)
# Valores del usuario: bombo, caja y tom cortan (profundidad 2, 3 y 1);
# 4-8 aranazos. Desde la fase 7 v12 el bombo y el tom son impulso (ver
# MODOS_DEFECTO): sus tripletas se conservan para volver a erosion a mano.
PERFILES_DEFECTO = [
    (4, 2, 2), (15, 1, 3), (4, 1, 1), (3, 1, 0),
    (2, 1, 0), (2, 0, 0), (1, 0, 0), (1, 1, 0),
]
# Los de la fase 7 v5 (primeros en notas), para reconocerlos al relanzar
PERFILES_V5 = [
    (2, 2, 0), (8, 1, 3), (12, 2, 4), (4, 1, 0),
    (3, 0, 0), (2, 1, 0), (1, 0, 0), (1, 0, 0),
]
# Los de la fase 7 v3 (reduccion en escalones), para reconocerlos al relanzar
PERFILES_V3 = [
    (1, 2, 0), (3, 1, 3), (3, 2, 4), (2, 1, 0),
    (2, 0, 0), (1, 1, 0), (1, 0, 0), (1, 0, 0),
]
ATENUACION = 0.5      # cada anillo de vecinas recibe esta fraccion del anterior
TIPOS_DEFECTO = ['impulso', 'corte', 'impulso', 'aranazo',
                 'aranazo', 'aranazo', 'aranazo', 'aranazo']
# Los de la fase 7 v6-v11 (bombo temblor, tom corte profundo)
TIPOS_V11 = ['temblor', 'corte', 'corte profundo', 'aranazo',
             'aranazo', 'aranazo', 'aranazo', 'aranazo']
# Fase 7 v12: un pad erosiona o da impulso. El impulso (bombo y tom) no
# destruye: desde la v14 suma pulsos de ocupacion a la celda que golpea (el
# bombo 3, el tom 2) y la hincha al golpe (pumping, solo visual). Ignora
# reduccion, radio y profundidad.
MODOS_PAD = ['erosion', 'impulso']
MODOS_DEFECTO = ['impulso', 'erosion', 'impulso', 'erosion',
                 'erosion', 'erosion', 'erosion', 'erosion']
PULSOS_DEFECTO = [3, 1, 2, 1, 1, 1, 1, 1]
# Fase 7 v13: segundos de caida del pumping de cada pad (columna pump_rel):
# el bombo, 0,20; el tom, 0,12; los demas, 0,15 si pasan a impulso.
PUMP_REL_DEFECTO = [0.20, 0.15, 0.12, 0.15, 0.15, 0.15, 0.15, 0.15]
ROLES_DEFECTO = ['bombo', 'caja', 'tom', 'palmas, aro', '-', '-', 'charles', 'platillo']
# Los de la fase 7 v1 (para reconocer una tabla sin editar al relanzar)
PERFILES_V1 = [
    (1, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0),
    (2, 1, 0), (2, 1, 2), (3, 1, 3), (3, 2, 4),
]
TIPOS_V1 = ['aranazo'] * 5 + ['corte', 'corte', 'corte profundo']


def _hex(h):
    return tuple(int(h[k:k + 2], 16) / 255.0 for k in (1, 3, 5))


# Balizas de la bateria: un color por pad. Cortes en rojos y violetas,
# aranazos frios y claros. Fuera a proposito: cian (cicatrices), ambar
# (SEQ2, coronas), blanco (SEQ1 desde la fase 9) y los minerales.
COLORES_DRUM = [_hex(h) for h in ('#D7263D', '#E83E8C', '#7C3AED', '#3B5BDB',
                                  '#12B76A', '#A3E635', '#F9A8D4', '#C4B5FD')]


# Fase 21: el microfono es el pad 9 (indice 8) de erosion. No llega por MIDI:
# lo golpean los onsets del publico. Su perfil (reduccion, radio, profundidad)
# va en la novena fila de perfiles_erosion, pero la reduccion la da
# Reduccionmic y cuenta ESCALONES enteros, no notas (D3). Su color, un gris
# calido claro (D10): no es el blanco del SEQ1, ni el ambar del SEQ2, ni el
# cian de las cicatrices.
PAD_MIC = 8
PERFIL_MIC = (1, 0, 0)
COLOR_MIC = _hex('#D8CCB8')
ROL_MIC = 'micro'
PERFILES_PADS = PERFILES_DEFECTO + [PERFIL_MIC]
TIPOS_PADS = TIPOS_DEFECTO + [ROL_MIC]
MODOS_PADS = MODOS_DEFECTO + ['erosion']
PULSOS_PADS = PULSOS_DEFECTO + [1]
PUMP_REL_PADS = PUMP_REL_DEFECTO + [0.15]
ROLES_PADS = ROLES_DEFECTO + [ROL_MIC]
COLORES_PADS = COLORES_DRUM + [COLOR_MIC]


def tipo_perfil(red, rad, depth):
    """Tipo de un perfil sin etiqueta. El temblor se porta como un aranazo."""
    if depth >= 4:
        return 'corte profundo'
    if depth > 0:
        return 'corte'
    return 'aranazo'


def es_impulso(cfg, pad):
    """El pad (0-7) esta en modo impulso (fase 7 v12)."""
    modos = cfg.get('modos') or MODOS_DEFECTO
    return modos[int(pad) % len(modos)] == 'impulso'


def pulsos_pad(cfg, pad):
    """Pulsos de ocupacion de un golpe de impulso del pad (al menos 1)."""
    ps = cfg.get('pulsos') or PULSOS_DEFECTO
    return max(1, int(round(float(ps[int(pad) % len(ps)]))))


def pads_impulso(cfg):
    return [k for k in range(len(cfg['perfiles'])) if es_impulso(cfg, k)]


def pads_corte(cfg):
    """Pads (0-7) cuyo perfil abre corte (profundidad > 0). Un pad de
    impulso no corta, tenga la profundidad que tenga."""
    return [k for k, p in enumerate(cfg['perfiles']) if p[2] > 0 and not es_impulso(cfg, k)]

COL_RED_DEF = (0.60, 0.36, 0.92)           # el violeta electrico de la red (OKLCH 0,62 0,21 300; reservado)
DEFAULT_CFG = dict(
    nivel=3,
    core_radius=12.0,           # motor v99: el doble (6 hasta la v98): las celdas, el doble de anchas
    # fase 3
    shell_thick=0.5, height_factor=3.75, seed_frac=0.20, grow_frac=0.20,
    gate_mode=1, gate_max=1.25, vel_umbral=64, steps_per_beat=4, cost_max=5,
    # fase 4
    th_branch=5, th_fusion=7, th_crown=9, th_cumbre=11, cumbre_tramos=4,
    sat_size=0.6, sat_limit=0.6, neigh_mode=1,
    # fase 6: el ciclo lo cierra el mundo
    beats_per_bar=4, umbral_madurez=0.6, umbral_novedad=0.15, compases_quietos=3,
    umbral_territorio=0.8, compases_territorio=8,
    ciclo_min=16, ciclo_max=64, cambio_entierra=0, giro_vivo=1, giro_min=0.25,
    # fase 7
    dens_umbral=0.60, rad_mult=2.0, target_mode=2,
    perfiles=PERFILES_DEFECTO, tipos=TIPOS_DEFECTO,
    # fase 7 v14: impulso (pulsos de ocupacion y pumping)
    modos=MODOS_DEFECTO, pulsos=PULSOS_DEFECTO,
    pump_amt=1.0, pump_horz=0.30, pump_hold=0.04, pump_velmin=0.6, pump_tope=2.0,
    pump_rels=PUMP_REL_DEFECTO, pump_on=1,
    # fase 8
    herencia=0.25, max_shells=24, grosor_tiempo=1, grosor_max=1.5, colmatacion=0.0,
    corteza_max=4.0,                                    # motor v37: compactacion
    paleta=0, paleta_tono=20.0, paleta_croma=0.04,     # 0 generaciones, 1 mineral
    # motor v53: conchas discretas (luminosidad, contraste y tapa neutra)
    paleta_luz=0.35, paleta_alterna=0.06, contraste_ocupada=0.04,
    tapa_neutra=0.6, tapa_luz=0.28,
    # fase 9
    scar_time=4.0, flash=3.0,
    # fase 7: luz de la bateria en las celdas que golpea
    balizas_drum=1, luz_drum=1.0, vida_baliza_drum=0.8, luz_seq=1,
    # fase 8: la luz de los secuenciadores se extiende a las conchas de la celda
    luz_conchas=1, luz_conchas_pulso=0.35, luz_conchas_reposo=0.10, luz_conchas_alcance=4,
    erosion_vel=1, vel_ref=100,
    colores_drum=COLORES_DRUM,
    # fase 11: la piel
    tema=0, peso_vecina=0.5, umbral_vecindad=4.0, min_cluster=2, caos=3.91, max_piezas=6,
    avance=0, pasos_etapa=2, rebote=0.2, catalogo=None,
    # fase 11 v5: la naturaleza legible
    umbral_monte=8, max_caos_nat=5, limite_bosque=0.65, limite_nieve=0.90, altura_monte=1.0,
    lod_nat=80.0, tinte_borde_nat=0.8, superficie=0,
    # fase 11 v8 (motor v52): brotes, arboles y terrazas
    ligero=1, refresco_piel=0.25, turnos=1, cache_arq=1,     # motor v101: la piel por turnos
    biomas=1, variantes=2, var_angulo=12.0, cuantizar30=0, inclinacion=8.0, densidad_hoja=6,
    traslucidez=0.35, timidez=0.12, emergentes=0.1, orla=1, mezcla=0.3, impostores=1,
    # motor v97: el oceano (las celdas vacias son mar; las ocupadas, islas), los volcanes y el detalle
    oceano=1, volcanes=0.2, detalle=1,
    tierra=0.75,                        # motor v100: cuanto se ven las conchas como capas de tierra
    pradera=300000, mata=0.16,          # motor v99: las matas de la pradera (GPU) y su tamano
    terrazas_por_nota=1, max_terrazas=8, paso_terraza=0.12, muro_terraza=0.25, riego=1,
    color_cultivo=(0.66, 0.80, 0.22), altura_meseta=0.15, max_niveles=3, marco=1, setos=1,
    # fase 11 v10 (motor v67): la ciudad legible
    lenguaje=0, variantes_ciudad=3, fijar_tipo=0, oblicuidad=6.0, alto_planta=0.08, ancho_vano=0.05,
    retranqueo=0.15, torsion_max=90.0, parasitos_por_nota=4, max_parasitos=24, modulo_marco=0.25,
    max_marco=3, capsulas=0.4, mutacion=0.5, mutacion_fuente=0, obra=1, desfase_fachada=2, gruas=1,
    max_gruas=6, tinte_ventanas=1, pasos_tinte=4, lod_ciudad=60.0,
    # fase 11 v11 (motor v68): la industria (13 v7: vias y red; 14 v4: apagon y grisu; 17 v3: turno)
    recursos=1, epoca=0, variantes_ind=3, bancos_por_nota=1.0, max_bancos=6, max_bastidor=3,
    emisiones=0.5, max_humo=6000, lod_ind=60.0,
    vias=1, red=1, min_red=2, ancho_via=0.14, pulso_red=1, color_red=COL_RED_DEF,
    apagon=1, grisu=1, turno=1,
    # fase 12: moduladores
    material_modo=1, rug_min=0.05, rug_max=0.85, vigor_max=1.5, plantas_ligado=2,
    gate_prueba=0.5, respaldo=0,
    # fase 13: tejido conectivo
    rios=1, carreteras=1, min_via=2, grosor_via=0.18, max_rio=12,
    color_rio=None, ancho_rio=0.10, ancho_max_rio=0.34, emisivo_rio=0.6, lagos=1,      # fase 13 v2 (v4: 0,6)
    ancho_min_px=4.0, pendiente_min=0.01, encuadre=0.85,                                # fase 13 v3 (v4: 4 px)
    # fase 14: destructores
    ventana_escalada=8, golpes_escalada=2, pasos_fuego=6, max_fuego=6, pasos_polvo=8,
    # fase 15: el ciclo como era
    peso_traza=0.5, rebrote=1, tema_en_ciclo=1,
    # fase 16: arqueologia tematica
    detalle_expuesto=6, unir_cortes=1,
    # fase 17: el tiempo en el paisaje
    sway_max=6.0, trafico=2, pasos_frente=16, master_beat=None,
    # fase 18: escenas y direccion tematica
    diagnostico=0, luz_calida=0.0, actuacion=0,
    # fase 19: las senales del modular
    fuente_modular=1, rango_modular=0, suavizado=0.15, viento_max=12.0, respiracion=0.75,
    smog=1.0, niebla=1.0, glitch=1.0, modular=None,
    # fase 21: el microfono
    umbral_onset=0.6, refractario_mic=0.12, reduccion_mic=1.0, ventana_ruido=60.0, umbral_corte=20.0,
    prof_mic=3, fuente_mic=0, canal_mic=0, chop_mic='',
    # fase 22: la camara cenital (casilla probable)
    presencia_activa=1, cuanto=0.5, peso_crear=1.0, peso_erosion=1.0, fuente_sala=0, sensor_sala=0,
    altura_min=0.8, altura_max=2.2, archivo_fondo='fondo_suelo.exr',
    ancho_sala=5.4, fondo_sala=4.5, tam_casilla=0.5, desenfoque=1.0, ocupacion_llena=0.6,
    subida=2.0, bajada=5.0, lon_central=0.0, ancho_angular=180.0, lat_norte=90.0, lat_sur=-90.0,
    espejo=0, sim_casilla=0,
    # fase 23: la luz de la sala
    ventana_balance=30.0, umbral_estrobo=1.0, salida_estrobo=0.8, max_hz=3.0, noche=4.0, colapso_on=0,
    max_erosion=15.0, sim_balance=-1.0, interfaz_dmx=0, universo_dmx=0,
    # fase 24: personas
    sep_cabezas=0.35, confirma_persona=2, sim_fila=3,
    # fase 25: la huella minima
    prob_llegada=0.6, t_parada=3.0,
    # fase 27: la clasificacion al enterrar
    min_huellas=1, inclusiones_max=0.8,
    # fase 29: la fila y la escision colectiva
    min_fila=3, t_fila=5.0, modo_fila=0, conchas_persona=1,
    # fase 31: las escisiones en el historico
    carpeta_historico='',
)


# -----------------------------------------------------------------------------
# 1. NUCLEO - geometria del reticulo
# -----------------------------------------------------------------------------

# La reticula va de polo a polo. La nota mas grave del rango
# (Notapolosur) es el POLO SUR y la mas aguda (Notapolonorte) el POLO
# NORTE; las de en medio se reparten en ANILLOS, uno por octava, como en la
# reticula de bandas: la clase de nota es el meridiano y la octava el
# anillo. Con do1-do8: un anillo de 11 (do#1-si1), seis de 12 (do2-si7) y
# el polo norte en do8. Los dos polos van entre do1 (24) y do8 (108).
# Vecinas: las dos del anillo, las del anillo contiguo cuyo arco se solapa
# y, en los anillos extremos, el polo. El polo: todo su anillo.

def ring_layout(lo, hi):
    """Reticula en anillos. lo = polo sur, hi = polo norte (notas MIDI).
    Entre medias, un anillo por octava: la clase de nota es el meridiano.
    Los anillos incompletos (el primero y el ultimo, si el rango no empieza
    o acaba en do) reparten sus celdas por igual alrededor.
    Devuelve (normales, anillo de cada celda, celdas de cada anillo,
    alto de banda en grados, radio del casquete polar en grados)."""
    K = hi - lo
    first = (lo + 1) // 12
    rings = []
    ring_of = [-1] * (K + 1)
    for k in range(1, K):
        j = (lo + k) // 12 - first
        while len(rings) <= j:
            rings.append([])
        rings[j].append(k)
        ring_of[k] = j
    R = max(1, len(rings))
    band = 180.0 / (R + 0.5)
    cap = band * 0.25
    normals = [None] * (K + 1)
    normals[0] = (0.0, -1.0, 0.0)
    normals[K] = (0.0, 1.0, 0.0)
    for j, cells in enumerate(rings):
        phi = math.radians(-90.0 + cap + band * (j + 0.5))
        m = len(cells)
        for q, k in enumerate(cells):
            if m == 12:
                th = 2.0 * math.pi * ((lo + k) % 12) / 12.0
            else:
                th = 2.0 * math.pi * (q + 0.5) / m
            normals[k] = (math.cos(phi) * math.cos(th), math.sin(phi),
                          math.cos(phi) * math.sin(th))
    return normals, ring_of, rings, band, cap


GRID = dict(lo=None, hi=None, mode=0)
NORMALS = []
SIZE_EW = []          # ancho este-oeste de cada celda (rad, esfera unidad)
SIZE_NS = []          # alto norte-sur (rad)
NEIGH = []
RING_OF = []
RINGS = []
POLE_S = 0
POLE_N = 0
NOTA_MIN, NOTA_MAX = 24, 108        # do1 y do8: limites de los polos


def _arc_overlap(a, wa, b, wb):
    d = abs((a - b + math.pi) % (2 * math.pi) - math.pi)
    return d < wa + wb - 1e-6


def set_grid(lo=POLO_SUR_DEF, hi=POLO_NORTE_DEF, mode=0):
    """Rehace la reticula para el rango de notas [lo, hi]. Devuelve True si
    ha cambiado la geometria (el mundo hay que vaciarlo)."""
    global N, NORMALS, SIZE_EW, SIZE_NS, NEIGH, POLE_S, POLE_N, RING_OF, RINGS
    lo = max(NOTA_MIN, min(NOTA_MAX - 2, int(lo)))
    hi = max(lo + 2, min(NOTA_MAX, int(hi)))
    GRID['mode'] = int(mode)
    if GRID['lo'] == lo and GRID['hi'] == hi:
        return False
    GRID['lo'], GRID['hi'] = lo, hi
    K = hi - lo
    N = K + 1
    POLE_S, POLE_N = 0, K
    NORMALS, RING_OF, RINGS, band, cap = ring_layout(lo, hi)
    nb = [[] for _ in range(N)]

    def link(a, b):
        if a != b:
            if b not in nb[a]:
                nb[a].append(b)
            if a not in nb[b]:
                nb[b].append(a)

    def theta(k):
        x, _, z = NORMALS[k]
        return math.atan2(z, x)

    for j, cells in enumerate(RINGS):
        m = len(cells)
        for q, k in enumerate(cells):
            if m > 1:
                link(k, cells[(q + 1) % m])
        if j + 1 < len(RINGS):
            nxt = RINGS[j + 1]
            if m == 12 and len(nxt) == 12:
                # dos anillos completos: hexagonal desplazada, como las bandas
                # (los pares miran a (c-1, c), los impares a (c, c+1))
                pc_a = dict(((lo + k) % 12, k) for k in cells)
                offs = (-1, 0) if (j + 1) % 2 == 0 else (0, 1)
                for b in nxt:
                    c = (lo + b) % 12
                    for o in offs:
                        link(b, pc_a[(c + o) % 12])
            else:
                for a in cells:
                    for b in nxt:
                        if _arc_overlap(theta(a), math.pi / m, theta(b), math.pi / len(nxt)):
                            link(a, b)
    for k in RINGS[0]:
        link(POLE_S, k)
    for k in RINGS[-1]:
        link(POLE_N, k)
    NEIGH = nb
    SIZE_EW, SIZE_NS = [], []
    for k in range(N):
        if k in (POLE_S, POLE_N):
            d = 2.0 * math.sin(math.radians(cap))
            SIZE_EW.append(d)
            SIZE_NS.append(d)
            continue
        m = len(RINGS[RING_OF[k]])
        phi = math.asin(max(-1.0, min(1.0, NORMALS[k][1])))
        SIZE_EW.append(2.0 * math.pi * math.cos(phi) / m)
        SIZE_NS.append(math.radians(band))
    return True


def is_pole(i):
    return i == POLE_S or i == POLE_N


def fold_note(note, mode=None):
    """Nota MIDI -> nota dentro del rango, o None si se ignora.
    plegar: por octavas (conserva la clase de nota); limitar: al polo mas
    cercano; ignorar: no deja nada."""
    lo, hi = GRID['lo'], GRID['hi']
    mode = GRID['mode'] if mode is None else int(mode)
    n = int(note)
    if lo <= n <= hi:
        return n
    if mode == 1:
        return None
    if mode == 0:
        while n > hi:
            n -= 12
        while n < lo:
            n += 12
        if lo <= n <= hi:
            return n
    return lo if int(note) < lo else hi


def note_cell(note):
    n = fold_note(note)
    return None if n is None else n - GRID['lo']


def cell_note(i):
    return GRID['lo'] + int(i)


def note_name(note):
    return '%s%d' % (NOTE_NAMES[int(note) % 12], int(note) // 12 - 1)


def cell_label(i):
    if i == POLE_S:
        return 'polo sur'
    if i == POLE_N:
        return 'polo norte'
    return 'anillo %d' % (RING_OF[int(i)] + 1)


def normal_i(i):
    return NORMALS[i]


set_grid()


def rings(i, k):
    """Celdas a distancia <= k de i, con su distancia: [(celda, d), ...]"""
    seen = {i: 0}
    frontier = [i]
    for d in range(1, int(k) + 1):
        nxt = []
        for c in frontier:
            for n in NEIGH[c]:
                if n not in seen:
                    seen[n] = d
                    nxt.append(n)
        frontier = nxt
    return sorted(seen.items(), key=lambda kv: (kv[1], kv[0]))


def orient(n):
    """Rotaciones (rx, ry) en grados que llevan el eje +Y local a n.
    Orden de TouchDesigner por defecto: primero X, luego Y."""
    x, y, z = n
    y = max(-1.0, min(1.0, y))
    phi = math.asin(y)
    theta = math.atan2(z, x)
    return 90.0 - math.degrees(phi), 90.0 - math.degrees(theta)


def tangents(n):
    """Ejes locales X (este) y Z (sur) de la celda, ya orientados."""
    x, y, z = n
    y = max(-1.0, min(1.0, y))
    phi = math.asin(y)
    theta = math.atan2(z, x)
    e = (math.sin(theta), 0.0, -math.cos(theta))
    t = (math.sin(phi) * math.cos(theta), -math.cos(phi), math.sin(phi) * math.sin(theta))
    return e, t


def _norm(v):
    l = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) or 1.0
    return (v[0] / l, v[1] / l, v[2] / l)


def _len(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def _add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def _mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def _hash01(*vals):
    # Pseudoaleatorio DETERMINISTA por celda: misma celda, misma forma.
    # No decide nada del mundo; solo varia la silueta de las piezas.
    h = 2166136261
    for v in vals:
        h = ((h ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return (h % 10007) / 10006.0


# -----------------------------------------------------------------------------
# 1. NUCLEO - estado del mundo
# -----------------------------------------------------------------------------

def new_world():
    return dict(
        v=1,
        occ=[0] * N,        # ocupacion (triggers de construccion)
        carga=[0] * N,      # notas acumuladas hacia el siguiente trigger
        lat=[-99.0] * N,    # inicio del latido: la nota, y al soltarla, el note off
        lat_s=[1] * N,      # secuenciador de la ultima nota (color del latido)
        seq_off={1: -99.0, 2: -99.0},   # cuando se solto la ultima nota de cada SEQ
        h=[0.0] * N,        # altura objetivo
        vh=[0.0] * N,       # altura visible (se acerca a h suavemente)
        sp=[0] * N,         # especie visible: 0, geo, arq, hib
        own=[0] * N,        # especie fundadora
        traza=[0] * N,      # bits: 1 geo, 2 arq
        vel=[0] * N,        # velocidad del evento fundador
        par=[-1] * N,       # satelite de... (-1: formacion propia)
        huella=[0.0] * N,   # instante en que quedo la huella (0: sin huella)
        resto=[0.0] * N,    # fraccion de herencia acumulada
        gen=0,
        shells=[],          # generaciones enterradas (paleta, grosor nominal, ocupacion)
        cols=[[] for _ in range(N)],   # columna de cada celda: [[concha, grosor], ...] de abajo arriba
        quitadas=[0] * N,   # losetas que ha perdido cada celda en el mundo actual
        nucleo_av=[0] * N,  # la celda ya aviso de que el corte llego al nucleo
        scars={},
        flash=None,
        last={1: None, 2: None},
        pend={},
        hits={1: 0, 2: 0, 3: 0},
        hit_t={1: -1.0, 2: -1.0},
        clock=dict(last_note_t=-99.0, stop_t=-99.0, start_t=-99.0),
        burst=dict(times=[], pending=None),
        drum={},                # pad -> ultimo golpe {t, cell, vel}
        luz={},                 # celda -> {pad: [t, peso]}: luz de la bateria
        ero_resto=[0.0] * N,    # fraccion de nota de erosion pendiente
        # impulso (fase 7 v12)
        imp_t={},               # celda -> ultimo golpe de impulso
        bomba={},               # celda -> {t0, pico, rel, hold, n, t2, tope}: el pumping en curso
        foto_dt=0.0,            # lo que dura un fotograma (el ultimo medido)
        # ciclo (fase 6): lo cierra el mundo
        ciclo_n=1,              # ciclo en curso
        compases_ciclo=0,       # compases que lleva el mundo actual
        quietos=0,              # compases seguidos maduros y quietos
        foto_anterior=None,     # forma de cada celda en el compas anterior
        cambio_pendiente=False, # rafaga de All Notes Off por aplicar
        madurez=0.0,
        novedad=0.0,
        giro_factor=1.0,
        beats=0.0,              # negras acumuladas hacia el siguiente compas
        bar_n=0,                # compases del reloj del ciclo desde el principio
        terr={},                # celda -> ultimo compas en que la toco un SEQ
        territorio=0.0,         # ocupacion del territorio de los patterns
        esperando=False,        # pasada la edad maxima, sin territorio ocupado
        ciclo_t0=None,          # instante en que empezo el mundo actual
        marcha=False,           # el reloj del ciclo avanza
        # la piel (fase 11): transitos de cada celda
        et_f=[0] * N,           # etapa visible de la cadena de fusion
        et_c=[0] * N,           # etapa visible de la cadena de coronacion
        ant_et_f=[0] * N,       # la etapa anterior (para animar el paso)
        ant_et_c=[0] * N,
        t_et_f=[-99.0] * N,     # cuando cambio la etapa
        t_et_c=[-99.0] * N,
        t_gate=[-99.0] * N,     # ultima nota en la celda
        t_nac=[-99.0] * N,      # cuando nacio la formacion (rebote)
        h_obj=[0.0] * N,        # altura que persigue el stop-motion
        h0=[0.0] * N,           # altura visible al empezar el tramo
        t_h=[-99.0] * N,        # cuando empezo el tramo
        paso=0.125,             # duracion de un paso al tempo actual
        piel={},                # resumen de la piel para la leyenda
        tejido={},              # resumen de rios y carreteras para la leyenda
        vig=[1.0] * N,          # vigor de cada formacion (fase 12: duracion del gate)
        # la ciudad legible (fase 11 v10): el edificio de cada celda y su obra
        edi=[-1] * N,           # tipo que se construye: 10 x especie (1 informal, 2 planificada) + etapa
        edi_occ=[0] * N,        # la ocupacion con la que empezo (una planta mas: obra)
        obra=[0] * N,           # paso de la obra (terminada = los pasos del tipo)
        ant_obra=[0] * N,
        t_obra=[-99.0] * N,
        plantas_ant=[0.0] * N,  # plantas ya terminadas al crecer en la misma etapa
        leng=[-1] * N,          # lenguaje con el que se empezo (0 frio, 1 templado, 2 calido)
        mut=[-1.0] * N,         # mutacion con la que se construye (desde el ultimo gate)
        par_vis=[0] * N,        # parasitos que se ven (persiguen a la logica uno por paso)
        marco_vis=[0] * N,      # unidades del marco que se ven (2 por nivel: marco y capsulas)
        t_vis=[-99.0] * N,
        gate_sim=[],            # note off simulados de los botones: [t, s, nota]
        # destructores (fase 14)
        golpes=[],              # aranazos recientes: [t, celda objetivo]
        cats=[],                # catastrofes en curso (incendio, derrumbes)
        polvo=[],               # nubes de particulas: [t0, celda, modo, cuantas]
        ruina=[0] * N,          # huella de una catastrofe (1 + indice de RUINA_ESP; 0 ninguna)
        t_ruina=[-99.0] * N,
        derribo=[0] * N,        # la obra de la celda se recorre hacia atras
        # el ciclo como era (fase 15)
        tema=None,              # tema del mundo (con Temaenciclo, cambia en el fin de ciclo)
        rebrote=[0] * N,        # etapa del rebrote de lo heredado: 1 semillas, 2 brotes, 0 nada
        t_rebrote=[-99.0] * N,
        trazas=[],              # tramos de carretera de la ciudad enterrada: [[a, b], ...]
        # arqueologia tematica (fase 16)
        cortes=[],              # cortes recientes: [t, celda objetivo, profundidad, radio]
        uniones=[],             # cortes unidos: {tipo: canon o galeria, celdas, t, prof}
        arqueo={},              # resumen de lo expuesto para la leyenda
        # el tiempo en el paisaje (fase 17)
        pulso=dict(beat=0.0, parado=False, mb=None, frac=0.0),   # beats acumulados en fase
        oido=[],                # notas recientes de los SEQ: [beat, s, nota]
        patrones=[],            # biblioteca: {nombre, firma, tinte, ventanas, visto}
        pattern=None,           # nombre del pattern que suena (si se conoce)
        pattern_conocido=None,  # si la biblioteca lo reconocio al entrar
        estacion=dict(tinte=[1.0, 1.0, 1.0], ventanas=1),        # la del pattern que suena
        frente=None,            # frente en curso: {beat0, de, a, pattern, conocido}
        # las senales del modular (fase 19), suavizadas, 0-1
        modular=dict(lfo=0.5, ruido=0.0, espacio=0.0, saturacion=0.0, t=-99.0, crudo=None, activo=False),
        # el microfono (fase 21): el ultimo onset, los que llevamos y los descartados
        mic=dict(t=-99.0, n=0, descartados=0, flujo=0.0, ultimo=None),
        ruido=dict(onsets=[], cortes=0, ultimo=None),   # onsets de la ventana: [t, flujo, celda]
        sala=dict(destellos=[]),            # instantes de los destellos propios (fase 23)
        # la huella minima (fase 25): inclusiones de cada celda, [escalon, tipo, t, k]
        incl=[[] for _ in range(N)],
        incl_n=dict(llegadas=0, paradas=0),     # las que ha dejado este mundo
        incl_ultima=None,
        incl_borradas=dict(erosion=0, micro=0, corte=0, catastrofe=0, escision=0),     # fase 26
        noche=None,             # la noche de enterramiento en curso (fase 28): [inicio, fin]
        # las escisiones (fase 29): los huecos que abren las filas
        escisiones=[],
        escision_n=0,           # correlativo de la exposicion
        esc_celdas={},          # celda -> escisiones abiertas en ella (el hueco es permanente)
        aviso='',
        ev={},
        t=None,
        dirty=True,
    )


def ensure(W):
    if 'cycle' in W:                # mundo del motor v7-v10: migrar
        try:
            W.setdefault('ciclo_n', int(W['cycle'].get('count', 0)) + 1)
        except Exception:
            pass
    for k in ('det', 'lib', 'cycle'):   # deteccion de longitud y biblioteca
        W.pop(k, None)
    ck = W.get('clock')
    if isinstance(ck, dict):
        for k in ('t_ref', 'step_ref', 'phase_ref'):
            ck.pop(k, None)
    luz = W.get('luz')
    if isinstance(luz, dict) and any(isinstance(v, list) for v in luz.values()):
        W['luz'] = {}                   # formato del motor v17 (un pad por celda)
    cols = W.get('cols')
    if not isinstance(cols, list) or len(cols) != len(W.get('occ', [])):
        W['cols'] = columns_from_shells(W)  # mundo del motor v22 o anterior
    W.pop('hueco', None)
    base = new_world()
    for k, v in base.items():
        if k not in W:
            W[k] = v
    for k in ('cap', 'cap_t'):          # la capacidad de los motores v43 y v44
        W.pop(k, None)
    if any(not isinstance(b, dict) for b in W['bomba'].values()):
        W['bomba'] = {}                 # pumping del motor v43 (otra envolvente)
    for k, v in base['seq_off'].items():
        W['seq_off'].setdefault(k, v)
    for k, v in base['clock'].items():
        W['clock'].setdefault(k, v)
    return W


def limit(cfg):
    return cfg['height_factor'] * cfg['shell_thick']


PASO_UMBRAL_DEF = 2        # ocupaciones de un estado al siguiente (5, 7, 9, 11)


def growstep_coherente(semilla, umbral_ram):
    """Crecimiento por trigger (x limite) con el que la formacion sube a
    escalones iguales de la semilla al limite: (1 - semilla) / (Umbralram - 1).
    Desde el motor v58 es siempre este (antes, el parametro Growstep)."""
    return (1.0 - semilla) / max(1, int(umbral_ram) - 1)


def height_for(cfg, occ):
    lim = limit(cfg)
    if occ <= 0:
        return 0.0
    if occ >= cfg['th_branch']:
        return lim
    return min(lim, cfg['seed_frac'] * lim + (occ - 1) * cfg['grow_frac'] * lim)


def cost(cfg, occ):
    """Notas que hacen falta para el siguiente trigger de construccion.
    Sube con la altura nominal de la formacion: 1 abajo, Costemax en el
    limite y desde ahi (ramificacion, fusion, coronacion, cumbre)."""
    cm = max(1, int(cfg['cost_max']))
    lim = limit(cfg)
    f = height_for(cfg, max(1, occ)) / lim if lim > 0 else 1.0
    return max(1, min(cm, 1 + int(math.floor((cm - 1) * f + 1e-6))))


def cumbre_tramos(cfg, occ):
    if occ < cfg['th_cumbre']:
        return 0
    return min(int(cfg['cumbre_tramos']), occ - cfg['th_cumbre'] + 1)


def state_name(cfg, occ, lvl=10):
    if occ <= 0:
        return 'vacia'
    if occ == 1:
        return 'semilla'
    if occ < cfg['th_branch']:
        if occ == 2:
            return 'brote'
        if occ == cfg['th_branch'] - 1:
            return 'madurez'
        return 'crecimiento'
    if lvl < 4:
        return 'limite'
    if occ < cfg['th_fusion']:
        return 'ramificacion'
    if occ < cfg['th_crown']:
        return 'fusion'
    if occ < cfg['th_cumbre']:
        return 'coronacion'
    return 'cumbre'


def n_shells(W):
    return len(W['shells'])


def shell_th(sh, cfg):
    """Grosor de una concha. Las del motor v7-v10 no lo guardan: Shellthick."""
    g = sh.get('grosor')
    return float(g) if g else cfg['shell_thick']


def shell_radii(W, cfg):
    """[(radio interior, radio exterior)] NOMINALES de cada concha (generacion),
    de dentro afuera: los que tendria sin cortes. Lo dibujado es la columna."""
    r = cfg['core_radius']
    out = []
    for sh in W['shells']:
        g = shell_th(sh, cfg)
        out.append((r, r + g))
        r += g
    return out


def top_radius(W, cfg):
    """Radio nominal: nucleo + grosores de todas las conchas = tiempo."""
    return cfg['core_radius'] + sum(shell_th(sh, cfg) for sh in W['shells'])


radio_nominal = top_radius


# --- columnas (motor v23): cada celda guarda la pila de losetas que le quedan.
# Una loseta es [concha, grosor]; la concha da su color y su ocupacion. Los
# radios salen de la posicion en la columna: el exterior de una loseta es el
# interior de la siguiente.

def columns_from_shells(W):
    """Columnas de un mundo anterior al motor v23: las losetas que sobreviven
    (sin 'rm') se apilan por orden de generacion y se cierran los huecos."""
    n = len(W.get('occ', []))
    cols = [[] for _ in range(n)]
    try:
        th = cfg()['shell_thick']
    except Exception:
        th = DEFAULT_CFG['shell_thick']
    for s, sh in enumerate(W.get('shells', [])):
        g = sh.get('grosor') or th
        rm = sh.get('rm') or [0] * n
        for c in range(n):
            if c >= len(rm) or not rm[c]:
                cols[c].append([s, float(g)])
    return cols


def suelo(W, cfg, c):
    """Radio del suelo de la celda c: nucleo + su columna."""
    return cfg['core_radius'] + sum(g for _, g in W['cols'][c])


def laguna(W, cfg, c):
    """Tiempo que la destruccion ha borrado en la celda c (siempre >= 0)."""
    return max(0.0, top_radius(W, cfg) - suelo(W, cfg, c))


def column_radii(W, cfg, c):
    """[(concha, r_in, r_out)] de la columna de c, de abajo arriba."""
    r = cfg['core_radius']
    out = []
    for s, g in W['cols'][c]:
        out.append((s, r, r + g))
        r += g
    return out


def base_radius(W, cfg, i):
    """Donde se apoyan formaciones, luz y reticula de la celda: su suelo."""
    return suelo(W, cfg, i)


def max_laguna(W, cfg):
    """(laguna maxima, celda)."""
    R = top_radius(W, cfg)
    best, cell = 0.0, -1
    for c in range(N):
        lg = R - suelo(W, cfg, c)
        if lg > best + 1e-9:
            best, cell = lg, c
    return best, cell


def occupied(W):
    return sum(1 for o in W['occ'] if o > 0)


def _clear_cell(W, i):
    W['occ'][i] = 0
    W['carga'][i] = 0
    W['h'][i] = 0.0
    W['par'][i] = -1


def _bit(s):
    return 1 if s == GEO else 2


# -----------------------------------------------------------------------------
# 1. NUCLEO - crecimiento (fases 3, 4, 5)
# -----------------------------------------------------------------------------

def _mark(W, i, s):
    b = _bit(s)
    if not (W['traza'][i] & b):
        W['traza'][i] |= b
        if W['own'][i] != s:
            W['sp'][i] = HIB                # colonizacion


def _ceiling(W, cfg, i):
    """Techo de altura de una formacion: el escalon que esta construyendo.
    Con carga a medias puede llegar hasta el siguiente escalon, nunca mas
    alla: ni el gate ni la presion adelantan la altura a los triggers."""
    o = W['occ'][i]
    top = height_for(cfg, o + 1 if W['carga'][i] > 0 else o)
    if W['par'][i] >= 0:
        top *= cfg['sat_limit']
    return min(limit(cfg), top)


GATE_MAX = 2.0      # una nota sin note off cuenta como pulsada como mucho 2 s


def held(W, now, s=None, cell=None):
    """True si hay una nota pulsada (gate abierto) del secuenciador s o en
    la celda cell."""
    for k, p in W.get('pend', {}).items():
        if now - p[1] > GATE_MAX or now < p[1]:
            continue
        if s is not None and not k.startswith('%d:' % s):
            continue
        if cell is not None and p[0] != cell:
            continue
        return True
    return False


def _charge(W, cfg, i, now):
    """Una nota (o una presion) llega a una formacion que ya existe.
    Suma 1 a su carga y la hace subir un trozo de escalon: Growstep /
    coste, asi que cada nota sube menos conforme la formacion se acerca
    al limite (la frenada). Cuando la carga llega al coste se dispara el
    trigger: la ocupacion sube 1. Devuelve (trigger, incremento)."""
    lim = limit(cfg)
    o = W['occ'][i]
    k = cost(cfg, o)
    W['lat'][i] = now
    inc = 0.0
    sat = W['par'][i] >= 0
    W['carga'][i] += 1
    if o < cfg['th_branch']:
        inc = cfg['grow_frac'] * lim / k
        W['h'][i] = min(_ceiling(W, cfg, i), W['h'][i] + inc)
    if W['carga'][i] < k:
        return False, inc
    W['carga'][i] = 0
    W['occ'][i] = o + 1
    if o + 1 >= cfg['th_branch'] and not sat:
        W['h'][i] = lim
    return True, inc


def grow(W, cfg, i, s, vel, now):
    lvl = cfg['nivel']
    lim = limit(cfg)
    o = W['occ'][i]
    if o == 0:
        W['occ'][i] = 1
        W['carga'][i] = 0
        W['lat'][i] = now
        W['lat_s'][i] = s
        W['own'][i] = s
        W['sp'][i] = s
        W['traza'][i] = _bit(s)
        W['vel'][i] = int(vel)
        W['par'][i] = -1
        W['h'][i] = cfg['seed_frac'] * lim
        W['huella'][i] = 0.0
        W['t_nac'][i] = now
        W['vig'][i] = 1.0
        return dict(estado='semilla', inc=0.0, celda=i, trigger=True)

    W['lat_s'][i] = s
    if W['par'][i] >= 0:                    # un satelite que recibe senal
        W['par'][i] = -1                    # directa se independiza
    _mark(W, i, s)
    _contar_nota(W, i, s)                   # fase 11 v8: la piel cuenta las notas de cada especie
    trig, inc = _charge(W, cfg, i, now)
    out = dict(celda=i, trigger=trig)
    o = W['occ'][i]
    if trig and o >= cfg['th_branch'] and lvl >= 4:
        out['desborde'] = overflow(W, cfg, i, s, vel, now)
    out['estado'] = state_name(cfg, o, lvl)
    out['inc'] = inc
    return out


def overflow(W, cfg, i, s, vel, now):
    nb = NEIGH[i]
    k = int(vel) if cfg['neigh_mode'] == 0 else int(vel) + W['occ'][i]
    j = nb[k % len(nb)]
    lim = limit(cfg)
    grow_h = cfg['grow_frac'] * lim
    o = W['occ'][j]
    if o == 0:
        W['occ'][j] = 1
        W['carga'][j] = 0
        W['lat'][j] = now
        W['par'][j] = i
        W['own'][j] = W['own'][i]
        W['sp'][j] = W['own'][i]
        W['traza'][j] = _bit(W['own'][i])
        W['vel'][j] = int(vel)
        W['h'][j] = cfg['seed_frac'] * lim
        W['huella'][j] = 0.0
        W['t_nac'][j] = now
        W['vig'][j] = 1.0
        kind = 'satelite nuevo'
    elif W['par'][j] == i:
        W['occ'][j] = o + 1
        W['lat'][j] = now
        W['h'][j] = min(cfg['sat_limit'] * lim, W['h'][j] + grow_h)
        kind = 'satelite crece'
    else:
        # presion sobre una formacion ajena: suma a su carga, sin cascada
        _mark(W, j, s)
        _charge(W, cfg, j, now)
        kind = 'presion'
    W['ev']['desborde'] = dict(de=i, a=j, tipo=kind, t=now)
    return j


def satellites_of(W, i):
    return [j for j in NEIGH[i] if W['par'][j] == i and W['occ'][j] > 0]


def note_off(W, cfg, s, note, now, tempo):
    p = W['pend'].pop('%d:%d' % (s, int(note)), None)
    if p:                           # se suelta la nota: el latido empieza a apagarse
        W['seq_off'][s] = now
        if 0 <= p[0] < N:
            W['lat'][p[0]] = now
    m = _gate_altura(W, cfg, p, now, tempo)
    if p and cfg['nivel'] >= 12:    # fase 12: el gate da vigor (naturaleza) o plantas (ciudad)
        gate_vigor(W, cfg, s, p, now, tempo)
    return m


def _gate_altura(W, cfg, p, now, tempo):
    """Fase 3: el gate decide cuanto sube la nota (Gatemax > 1)."""
    if not p or not cfg['gate_mode']:
        return None
    i, t_on, inc, o = p
    if inc <= 0 or W['occ'][i] != o:
        return None
    step = step_dur(cfg, tempo)
    factor = max(0.0, now - t_on) / step
    # gate al 50 % = incremento normal; ligado como mucho Gatemax veces
    m = max(0.25, min(max(1.0, cfg['gate_max']), 2.0 * factor))
    lim = limit(cfg)
    lo = cfg['seed_frac'] * lim
    W['h'][i] = max(lo, min(_ceiling(W, cfg, i), W['h'][i] + inc * (m - 1.0)))
    return m


def note_on(W, cfg, s, note, vel, now, tempo=120.0):
    W['hits'][s] = W['hits'].get(s, 0) + 1
    W['hit_t'][s] = now
    i = note_cell(note)
    W['clock']['last_note_t'] = now
    if cfg['nivel'] >= 17 and s in (GEO, ARQ):     # fase 17: lo que suena, para la biblioteca
        oir(W, s, note)
    if i is None:                       # fuera del rango, modo ignorar
        W['ev']['ultima'] = dict(s=s, celda=-1, occ=0, estado='fuera de rango', t=now)
        return dict(estado='fuera de rango', inc=0.0, celda=-1)
    W['last'][s] = dict(note=int(note), cell=i, t=now, vel=int(vel))
    if cfg['nivel'] >= 22 and not presencia_sortear(W, cfg, i, 'crear'):
        # fase 22: la nota no prende (el sorteo de la presencia): se pierde sin rastro
        W['ev']['ultima'] = dict(s=s, celda=i, occ=W['occ'][i], estado='no prende', t=now,
                                 carga=W['carga'][i], coste=cost(cfg, W['occ'][i]))
        return dict(estado='no prende', inc=0.0, celda=i, trigger=False)
    W.setdefault('terr', {})[i] = W.get('bar_n', 0)
    W['ruina'][i] = 0                   # fase 14: construir sobre la huella la borra
    W['rebrote'][i] = 0                 # fase 15: una nota completa el rebrote
    if cfg['nivel'] >= 12:              # fase 12: la velocidad da el material
        W['ev']['mod'] = dict(s=s, celda=i, vel=int(vel), rug=rugosidad(cfg, vel), gate=None, efecto='')
    antes = sum(W['occ']) if cfg['nivel'] >= 23 else 0
    res = grow(W, cfg, i, s, vel, now)
    if cfg['nivel'] >= 23:              # fase 23: los escalones ganados, al balance
        balance_suma(W, cfg, now, crea=sum(W['occ']) - antes)
    gate_piel(W, cfg, i, now)           # fase 11: el gate adelanta las obras
    W['pend']['%d:%d' % (s, int(note))] = [i, now, res.get('inc', 0.0), W['occ'][i]]
    W['ev']['ultima'] = dict(s=s, celda=i, occ=W['occ'][i], estado=res['estado'], t=now,
                             carga=W['carga'][i], coste=cost(cfg, W['occ'][i]))
    return res


# -----------------------------------------------------------------------------
# 1. NUCLEO - reloj de compases y ciclo (fase 6)
# -----------------------------------------------------------------------------
# El ciclo lo cierra el propio mundo (ciclo adaptativo de Holling: crecer,
# madurar, liberar, reorganizar). El mundo se entierra cuando esta maduro y
# deja de cambiar, o cuando alcanza su edad maxima. No se detecta la
# longitud de los patterns: con probabilidad y acumulacion el mundo no se
# repite aunque el secuenciador si.

def step_dur(cfg, tempo):
    """Duracion de un paso (semicorchea). Solo la usa el gate."""
    if tempo and tempo > 0:
        return 60.0 / tempo / max(1, cfg['steps_per_beat'])
    return 0.125


def bar_dur(cfg, tempo):
    if tempo and tempo > 0:
        return 60.0 / tempo * max(1, int(cfg['beats_per_bar']))
    return 2.0


def cycle_bounds(cfg):
    cmin = max(1, int(cfg['ciclo_min']))
    return cmin, max(cmin, int(cfg['ciclo_max']))


def clock_start(W, now):
    W['clock']['start_t'] = now
    if 'pulso' in W:                    # fase 17: el pulso se pone en fase con el START
        W['pulso']['beat'] = 0.0
        W['pulso']['mb'] = None
        W['oido'] = []


def clock_stop(W, now):
    W['clock']['stop_t'] = now


def on_cc(W, cfg, ch, num, val, now):
    if num != 123:
        return
    b = W['burst']
    b['times'] = [x for x in b['times'] if now - x[0] < 0.12] + [(now, ch)]
    if b['pending'] is None and len(set(c for _, c in b['times'])) >= 8:
        b['pending'] = now


def _resolve_burst(W, cfg, now, playing):
    b = W['burst']
    if b['pending'] is None or now - b['pending'] < 0.3:
        return None
    t = b['pending']
    b['pending'] = None
    b['times'] = []
    stop = abs(W['clock']['stop_t'] - t) < 0.5 or not playing
    if stop:
        W['aviso'] = 'All Notes Off junto a un STOP'
        return 'stop'
    if cfg['cambio_entierra']:
        W['cambio_pendiente'] = True
        W['aviso'] = 'All Notes Off sin STOP: cambio de pattern, el mundo se enterrara'
    else:
        W['aviso'] = 'All Notes Off sin STOP: cambio de pattern'
    return 'cambio'


def clock_running(W, cfg, now, tempo, playing):
    """El reloj del ciclo avanza con la linea de tiempo en play, sin STOP
    despues de la ultima nota y con alguna nota en los ultimos 4 compases."""
    ck = W['clock']
    if not playing or not tempo or tempo <= 0:
        return False
    if ck['last_note_t'] < -1.0 or ck['stop_t'] > ck['last_note_t']:
        return False
    return now - ck['last_note_t'] < 4 * bar_dur(cfg, tempo)


def form_cap(cfg, sat):
    """Ocupacion a partir de la cual cuenta como la misma forma: la corona
    (Umbralram + 2 Pasoumbral). Una celda coronada sigue sumando ocupacion, y la cumbre
    sigue alargando la corona, pero el mundo ya se da por hecho. Un
    satelite deja de cambiar antes, al llegar a Satelite."""
    if sat:
        g = max(1e-6, cfg['grow_frac'])
        return max(1, 1 + int(math.ceil((cfg['sat_limit'] - cfg['seed_frac']) / g - 1e-9)))
    return cfg['th_crown']


def snapshot(W, cfg):
    """Forma de cada celda: especie, ocupacion recortada donde la forma deja
    de cambiar, hibrida, satelite y huella (desde el nivel 7)."""
    hu_on = cfg['nivel'] >= 7
    out = []
    for i in range(N):
        o = W['occ'][i]
        hu = 1 if hu_on and W['huella'][i] > 0 else 0
        if o <= 0:
            out.append([0, 0, 0, 0, hu])
            continue
        sat = W['par'][i] >= 0
        out.append([W['own'][i], min(o, form_cap(cfg, sat)),
                    1 if W['sp'][i] == HIB else 0, 1 if sat else 0, hu])
    return out


def _alive(f):
    return f[1] > 0 or f[4] > 0


def measure(W, cfg, foto):
    """(novedad, madurez). Novedad: celdas vivas cuya forma ha cambiado.
    Madurez: formaciones (sin contar satelites) que han llegado al limite."""
    prev = W.get('foto_anterior')
    if not prev or len(prev) != N:
        prev = None
    alive = changed = 0
    for i in range(N):
        a = foto[i]
        b = list(prev[i]) if prev else [0, 0, 0, 0, 0]
        if _alive(a) or _alive(b):
            alive += 1
            if a != b:
                changed += 1
    forms = [i for i in range(N) if W['occ'][i] > 0 and W['par'][i] < 0]
    mature = sum(1 for i in forms if W['occ'][i] >= cfg['th_branch'])
    return changed / float(max(1, alive)), mature / float(max(1, len(forms)))


def territory_cells(W, cfg):
    """El territorio de los patterns en uso: las celdas que han tocado las
    notas del SEQ1 y del SEQ2 en los ultimos Compasesterritorio compases,
    mas sus vecinas (hasta donde llegan los desbordes)."""
    ventana = max(1, int(cfg['compases_territorio']))
    ahora = W.get('bar_n', 0)
    terr = W.get('terr', {})
    for c in [c for c, b in terr.items() if ahora - b >= ventana]:
        del terr[c]
    cells = set()
    for c in terr:
        if 0 <= c < N:
            cells.add(c)
            cells.update(NEIGH[c])
    return cells


def territory_occupation(W, cfg):
    """Celdas del territorio ocupadas (formaciones y satelites) / territorio.
    Sin territorio (no ha sonado nada en la ventana), 0."""
    cells = territory_cells(W, cfg)
    if not cells:
        return 0.0
    return sum(1 for c in cells if W['occ'][c] > 0) / float(len(cells))


def bar_tick(W, cfg):
    """Un compas del reloj del ciclo. Devuelve el motivo de cierre o None."""
    foto = snapshot(W, cfg)
    nov, mat = measure(W, cfg, foto)
    W['foto_anterior'] = foto
    W['novedad'], W['madurez'] = nov, mat
    W['bar_n'] = W.get('bar_n', 0) + 1
    W['territorio'] = territory_occupation(W, cfg)
    W['compases_ciclo'] += 1
    if mat >= cfg['umbral_madurez'] and nov <= cfg['umbral_novedad']:
        W['quietos'] += 1
    else:
        W['quietos'] = 0
    cmin, cmax = cycle_bounds(cfg)
    n = W['compases_ciclo']
    if W['cambio_pendiente'] and n >= cmin:
        return 'cambio de pattern'
    if n >= cmin and W['quietos'] >= int(cfg['compases_quietos']):
        return 'estancado'
    # la edad maxima solo entierra un mundo cuyo territorio esta ocupado; sin
    # tope de seguridad: si la bateria no deja llenarlo, el mundo sigue vivo
    W['esperando'] = n >= cmax
    if n >= cmax and W['territorio'] >= cfg['umbral_territorio']:
        return 'edad maxima'
    return None


def close_cycle(W, cfg, now, motivo):
    """Cierra el mundo: emite fin_de_ciclo y, desde el nivel 8, lo entierra."""
    bars = W['compases_ciclo']
    t0 = W.get('ciclo_t0')
    ev = dict(ciclo=W['ciclo_n'], compases=bars,
              segundos=max(0.0, now - t0) if t0 is not None else 0.0,
              motivo=motivo, madurez=W['madurez'], novedad=W['novedad'],
              territorio=W.get('territorio', 0.0), t=now)
    if cfg['nivel'] >= 23:              # fase 23: el balance al cerrar
        ev['balance'] = balance(W, cfg, now)
    apagar_destructores(W)              # fase 14: el fin de ciclo lo cierra de golpe
    if end_cycle(W, cfg, now, bars, motivo):
        ev['grosor'] = shell_th(W['shells'][-1], cfg)
        W['foto_anterior'] = snapshot(W, cfg)
        if cfg['nivel'] >= 27:          # fase 27: la banda de la concha nueva
            ev['huellas'] = W['shells'][-1].get('huellas', 0)
            ev['banda'] = W['shells'][-1].get('banda', 'limpia')
            ev['colapso'] = bool(W['shells'][-1].get('colapso'))
    if cfg['nivel'] >= 23:              # fase 23: un destello y la sala a oscuras
        sala_fin_ciclo(W, cfg, now)
    W['aviso'] = 'fin de ciclo %d: %s a los %d compases' % (ev['ciclo'], motivo, bars)
    W['compases_ciclo'] = 0
    W['quietos'] = 0
    W['esperando'] = False
    W['cambio_pendiente'] = False
    W['ciclo_n'] += 1
    W['ciclo_t0'] = now
    if cfg['nivel'] >= 15:              # fase 15: el tema pendiente entra con el mundo nuevo
        W['tema'] = int(cfg.get('tema_pendiente', cfg['tema']))
    W['ev']['fin_de_ciclo'] = ev
    return ev


def giro_step(W, cfg, dt, tempo):
    """Giro vivo: el planeta se frena cuando el mundo deja de cambiar."""
    if not cfg['giro_vivo'] or cfg['nivel'] < 6:
        W['giro_factor'] = 1.0
        return 1.0
    gmin = max(0.0, min(1.0, cfg['giro_min']))
    un = max(1e-6, cfg['umbral_novedad'])
    obj = max(gmin, min(1.0, W['novedad'] / (4.0 * un)))
    f = W['giro_factor'] + (obj - W['giro_factor']) * min(1.0, dt / bar_dur(cfg, tempo))
    W['giro_factor'] = max(gmin, min(1.0, f))
    return W['giro_factor']


def cycle_tick(W, cfg, now, dt, tempo, playing):
    """Avanza el reloj de compases. Devuelve el fin_de_ciclo o None."""
    run = clock_running(W, cfg, now, tempo, playing)
    W['marcha'] = run
    if not run:
        return None
    if W.get('ciclo_t0') is None:
        W['ciclo_t0'] = now
    W['beats'] += dt * tempo / 60.0
    bpb = max(1, int(cfg['beats_per_bar']))
    while W['beats'] >= bpb:
        W['beats'] -= bpb
        motivo = bar_tick(W, cfg)
        if motivo:
            W['beats'] = min(W['beats'], bpb - 1e-6)
            return close_cycle(W, cfg, now, motivo)
    return None


# -----------------------------------------------------------------------------
# 1. NUCLEO - erosion y cortes (fases 7 y 9)
# -----------------------------------------------------------------------------

def pick_target(W, cfg, pad, vel):
    mode = int(cfg['target_mode'])
    l1, l2 = W['last'].get(1), W['last'].get(2)
    if mode == 3 or (l1 is None and l2 is None):
        return min(N - 1, int(vel) * N // 128)
    if mode == 0:
        src = l1 or l2
    elif mode == 1:
        src = l2 or l1
    else:
        src = (l1 or l2) if pad % 2 == 0 else (l2 or l1)
    i = src['cell']
    return max(0, min(N - 1, i + int(vel) % 3 - 1))     # un semitono a un lado


def _undo_note(W, cfg, i):
    """_undo_note_base y, desde la fase 26, la purga de las inclusiones que
    quedan por encima de la ocupacion de la celda."""
    hecho = _undo_note_base(W, cfg, i)
    if hecho and cfg['nivel'] >= 26:
        purgar_inclusiones(W, i)
    return hecho


def _undo_note_base(W, cfg, i):
    """Deshace una nota de construccion en la celda i: la misma moneda que
    _charge, al reves. Baja la carga y la altura lo que subio esa nota
    (Growstep / coste del escalon); al agotarse la carga baja un escalon y
    la carga queda llena menos una. Una semilla sola se borra y deja huella."""
    o = W['occ'][i]
    if o <= 0:
        return False
    sat = W['par'][i] >= 0
    lim = limit(cfg)
    if sat:                             # los satelites crecen por desbordes
        W['occ'][i] = o - 1
        W['carga'][i] = 0
        W['h'][i] = min(W['h'][i], height_for(cfg, o - 1) * cfg['sat_limit'])
        if W['occ'][i] <= 0:
            _clear_cell(W, i)
        return True
    if o == 1 and W['carga'][i] == 0:
        _clear_cell(W, i)
        W['huella'][i] = max(W['t'] or 0.0, 1e-3)
        return True
    if W['carga'][i] == 0:              # baja un escalon
        o -= 1
        W['occ'][i] = o
        W['carga'][i] = cost(cfg, o)
    W['carga'][i] -= 1
    if o < cfg['th_branch']:
        step = cfg['grow_frac'] * lim / cost(cfg, o)
        W['h'][i] = min(W['h'][i], height_for(cfg, o) + W['carga'][i] * step)
        W['h'][i] = max(height_for(cfg, o), W['h'][i])
    return True


def bajar_escalon(W, cfg, i):
    """Fase 21 (D3): un onset del microfono baja la celda i un escalon de
    ocupacion entero, no una nota: queda al principio del escalon de abajo
    (carga 0, la altura de esa ocupacion). Una semilla se borra y deja
    huella; un satelite pierde uno de sus desbordes."""
    o = W['occ'][i]
    if o <= 0:
        return False
    if W['par'][i] >= 0 or (o == 1):
        while W['occ'][i] >= o and _undo_note(W, cfg, i):
            pass
        return True
    o -= 1
    W['occ'][i] = o
    W['carga'][i] = 0
    W['h'][i] = min(W['h'][i], height_for(cfg, o))
    if cfg['nivel'] >= 26:              # fase 26: las inclusiones de un escalon mas alto se borran
        purgar_inclusiones(W, i)
    return True


def bajar_escalones(W, cfg, i, k):
    """k escalones en el orden de degrade: primero los satelites, luego la celda."""
    hechos = 0
    for _ in range(int(k)):
        sats = satellites_of(W, i)
        j = max(sats, key=lambda x: W['occ'][x]) if sats else i
        if not bajar_escalon(W, cfg, j):
            break
        hechos += 1
    if hechos and W['sp'][i] == HIB:
        _quitar_colona(W, i, W.get('t'))
    return hechos


def degrade(W, cfg, i, k):
    """Deshace k notas en orden inverso a la promocion: primero los
    satelites, luego la altura de la celda, al final la huella."""
    removed = 0
    for _ in range(int(k)):
        sats = satellites_of(W, i)
        if sats:
            j = max(sats, key=lambda x: W['occ'][x])
            ok_ = _undo_note(W, cfg, j)
        else:
            ok_ = _undo_note(W, cfg, i)
        if not ok_:
            break
        removed += 1
    if removed and W['sp'][i] == HIB:       # fase 11 v8: el golpe quita el bancal o el nivel de arriba
        _quitar_colona(W, i, W.get('t'))
    return removed


def erosion_notes(cfg, red, vel):
    """Notas que deshace un golpe en su celda. La reduccion de la tabla vale
    a la velocidad Velref (100) y escala en proporcion (x1,27 a 127).
    Minimo: una nota (o la reduccion, si es menor), para que un golpe flojo
    siempre deje huella. Con Velref 0, la de la tabla."""
    red = float(red)
    if not cfg.get('erosion_vel', 0) or red <= 0:
        return red
    f = max(0.0, float(vel)) / max(1.0, float(cfg.get('vel_ref', 100)))
    return max(min(red, 1.0), red * f)


def erosion(W, cfg, pad, vel, now, target=None):
    """Un golpe de bateria. Un pad en modo impulso (fase 7 v12) no erosiona:
    lo atiende impulso(). target: la celda del golpe (fase 22: el microfono va
    a la casilla mas densa); sin el, la elige pick_target. Desde la fase 22 el
    golpe pasa por el sorteo de la presencia, una vez y en su centro: si no
    prende, se pierde (el evento lleva prende = False)."""
    perf = cfg['perfiles']
    pad = int(pad) % len(perf)
    if es_impulso(cfg, pad):
        return impulso(W, cfg, pad, vel, now)
    red, rad, depth = perf[pad]
    if target is None:
        target = pick_target(W, cfg, pad, vel)
    if cfg['nivel'] >= 22 and not presencia_sortear(W, cfg, target, 'erosionar'):
        tipos = cfg.get('tipos') or []
        ev = dict(pad=pad, red=red, notas=0.0, rad=0, prof=depth, celda=target,
                  dens=occupied(W) / float(N), doble=False, quitado=0, t=now, modo='erosion', prende=False,
                  tipo=tipos[pad] if pad < len(tipos) and tipos[pad] else tipo_perfil(red, rad, depth))
        W['hits'][3] = W['hits'].get(3, 0) + 1
        W['drum'][pad] = dict(t=now, cell=target, vel=int(vel))
        W['ev']['erosion'] = ev
        return ev
    dens = occupied(W) / float(N)
    over = dens > cfg['dens_umbral']
    rad_eff = max(1, int(round(rad * cfg['rad_mult']))) if over else int(rad)
    removed = 0
    W['t'] = W['t'] if W['t'] is not None else now
    resto = W['ero_resto']
    antes23 = sum(W['occ']) if cfg['nivel'] >= 23 else 0
    mic = pad == PAD_MIC                # fase 21: el microfono baja escalones enteros
    notas = erosion_notes(cfg, red, vel) if not mic else float(red)
    tematico = cfg['nivel'] >= 14 and es_aranazo(cfg, pad)
    antes = antes_del_golpe(W, cfg, target, now) if tematico else None
    borra = cfg['nivel'] >= 26          # fase 26: el golpe borra inclusiones
    # la causa de lo que borre este golpe: el microfono, un pad que corta (la caja) o un aranazo
    _CAUSA[0] = 'micro' if mic else ('corte' if depth > 0 and cfg['nivel'] >= 9 else 'erosion')
    for c, d in rings(target, rad_eff):
        w = ATENUACION ** d             # 1 en la celda, 1/2 el primer anillo, 1/4...
        x = notas * w + resto[c]
        k = int(math.floor(x + 1e-9))
        resto[c] = x - k
        removed += bajar_escalones(W, cfg, c, k) if mic else degrade(W, cfg, c, k)
        if borra and w > 0.0:           # en una celda sin construir, cualquier anillo que la alcance (P6)
            golpe_inclusiones(W, c)
        light_cell(W, cfg, c, pad, w, now)
    _CAUSA[0] = 'erosion'
    W['hits'][3] = W['hits'].get(3, 0) + 1
    W['drum'][pad] = dict(t=now, cell=target, vel=int(vel))
    tipos = cfg.get('tipos') or []
    tipo = tipos[pad] if pad < len(tipos) and tipos[pad] else tipo_perfil(red, rad, depth)
    ev = dict(pad=pad, red=red, notas=notas, rad=rad_eff, prof=depth, celda=target, dens=dens,
              doble=over, quitado=removed, t=now, tipo=tipo, modo='erosion')
    W['ev']['erosion'] = ev
    if tematico:                        # fase 14: el accidente y la escalada
        destructor(W, cfg, pad, vel, now, ev, antes)
    if cfg['nivel'] >= 9:
        if depth > 0 and cfg['nivel'] >= 16:    # fase 16: los cortes se unen
            ev['corte'], ev['union'] = corte_tematico(W, cfg, target, depth, rad, now)
        elif depth > 0:
            ev['corte'] = cut(W, cfg, target, depth, rad, now)
        W['flash'] = dict(t=now, cell=target, k=1.0 if depth > 0 else 0.35, pad=pad)
    if cfg['nivel'] >= 23:              # fase 23: los escalones perdidos (con su corte), al balance
        balance_suma(W, cfg, now, eros=antes23 - sum(W['occ']))
    return ev


# --- impulso (fase 7 v14) ------------------------------------------------------
# El bombo es la respiracion del planeta: cada golpe empuja la corteza desde
# dentro; el tom, un latido mas corto. Un pad de impulso:
#   - suma 'pulsos' triggers completos a la celda que golpea (donde cae, como
#     la erosion: Objetivo y la velocidad, que la desplaza un semitono), uno
#     detras de otro y como si ya hubiera pagado su coste en notas: el bombo
#     3, el tom 2. Cada pulso sigue las reglas de siempre: crecimiento hasta
#     el limite y, por encima, desborde a las vecinas, fusion, corona y
#     cumbre; en una celda vacia el primero siembra. La estructura queda al
#     tamano que le toca por su ocupacion, y esa altura se pone de golpe. El
#     limite de altura y los umbrales no cambian.
#   - hincha lo dibujado en esa celda (pumping): un factor visual sobre el
#     tamano ya asentado que salta al pico con el golpe, lo sostiene Pumphold
#     s (y al menos BOMBA_FOTOS fotogramas) y vuelve a 1 en los segundos de su
#     pad (pump_rel), deprisa al principio y plano al final, sin pasar de
#     Pumptope x el limite. Un golpe durante la caida salta otra vez al pico.
#     Los satelites que nacen en las vecinas son de esas celdas: no se hinchan.
#   - enciende la luz de la celda con el color del pad, con la misma curva.
#   - no resta, no deja huella, no corta y no entra en el presupuesto de
#     densidad. La luz de su pad no tapa la del secuenciador.
BOMBA_DESTELLO = 0.35       # el destello de un impulso, suave
BOMBA_FOTOS = 2             # fotogramas completos en el pico, como minimo
BOMBA_TOPE = 0.8            # pico + caida <= 0,8 x el tiempo desde el golpe anterior en la celda
FOTO_DEF = 1.0 / 60.0       # un fotograma, hasta medirlo (TouchDesigner va a 60 fps)


def bomba_frac(W, i, now):
    """Fraccion 0-1 del pumping de la celda i en now. En seco: 1 desde el
    golpe, sin rampa, sostenido Pumphold s y al menos BOMBA_FOTOS fotogramas
    dibujados; luego cae deprisa al principio y plano al final:
        (1 - t / rel)^3
    y llega a 0 justo en rel."""
    b = W.get('bomba', {}).get(i)
    if not b:
        return 0.0
    if b['t2'] is None:                 # aun no se han dibujado dos fotogramas
        return 1.0
    fin = max(b['t0'] + b['hold'], b['t2'])
    if now <= fin:
        return 1.0
    x = (now - fin) / max(1e-9, b['rel'])
    if x >= 1.0:
        return 0.0
    return (1.0 - x) ** 3


def bomba_nivel(W, cfg, i, now):
    """(valor, pico) del pumping de la celda i: la escala vertical es 1 + valor."""
    b = W.get('bomba', {}).get(i)
    if not b:
        return 0.0, 0.0
    return b['pico'] * bomba_frac(W, i, now), b['pico']


def vel_bomba(cfg, vel):
    """La velocidad escala el pico entre Pumpvelmin (0,6, a velocidad 1) y 1
    (a 127): un golpe flojo se nota, pero menos."""
    vmin = max(0.0, min(1.0, cfg.get('pump_velmin', 0.6)))
    v = max(1.0, min(127.0, float(vel)))
    return vmin + (1.0 - vmin) * (v - 1.0) / 126.0


def pump_rel_pad(cfg, pad):
    """Segundos de caida del pumping del pad (columna pump_rel)."""
    rels = cfg.get('pump_rels') or PUMP_REL_DEFECTO
    return max(0.0, float(rels[int(pad) % len(rels)]))


def seq_de_objetivo(W, cfg, pad):
    """El secuenciador (GEO o ARQ) cuya celda sigue el golpe (como en
    pick_target): da la especie de la celda vacia que siembra un impulso."""
    mode = int(cfg['target_mode'])
    l1, l2 = W['last'].get(1), W['last'].get(2)
    if mode == 1 or (mode == 2 and int(pad) % 2 == 1):
        return ARQ if l2 else GEO
    return GEO if l1 or not l2 else ARQ


def pulso(W, cfg, i, s, vel, now):
    """Un pulso de impulso en la celda i: un trigger completo (ocupacion + 1)
    sin pagar notas, con las reglas de siempre. En una celda vacia siembra
    (especie s, pulida o porosa por la velocidad). No cambia la especie ni
    coloniza. Devuelve la celda del desborde, si lo hay."""
    if W['occ'][i] <= 0:
        grow(W, cfg, i, s, vel, now)
        return None
    if W['par'][i] >= 0:                # un satelite que recibe senal directa se independiza
        W['par'][i] = -1
    o = W['occ'][i] + 1
    W['occ'][i] = o
    W['carga'][i] = 0
    W['h'][i] = max(W['h'][i], height_for(cfg, o))     # la altura de su ocupacion
    if o >= cfg['th_branch'] and cfg['nivel'] >= 4:
        return overflow(W, cfg, i, W['own'][i], vel, now)
    return None


def impulso(W, cfg, pad, vel, now):
    pad = int(pad) % len(cfg['perfiles'])
    n = pulsos_pad(cfg, pad)
    target = pick_target(W, cfg, pad, vel)
    W['t'] = W['t'] if W['t'] is not None else now
    occ0 = W['occ'][target]
    s = W['own'][target] if occ0 > 0 and W['own'][target] else seq_de_objetivo(W, cfg, pad)
    desbordes = []
    antes = sum(W['occ']) if cfg['nivel'] >= 23 else 0
    for _ in range(n):                  # uno detras de otro, con las reglas de siempre
        j = pulso(W, cfg, target, s, vel, now)
        if j is not None:
            desbordes.append(j)
    if cfg['nivel'] >= 23:              # fase 23: el bombo y el tom son creacion
        balance_suma(W, cfg, now, crea=sum(W['occ']) - antes)
    W['ruina'][target] = 0              # fase 14: construir sobre la huella la borra
    W['rebrote'][target] = 0            # fase 15: completa el rebrote
    # la altura nueva, de golpe: sin suavizado ni stop-motion (y sin el rebote
    # de nacimiento: el golpe lo hace el pumping)
    W['vh'][target] = W['h_obj'][target] = W['h0'][target] = W['h'][target]
    W['t_h'][target] = now
    if occ0 <= 0:                       # sembrada por el golpe: sin rebote ni latido de una nota
        W['t_nac'][target] = -99.0
        W['lat'][target] = -99.0
    gate_piel(W, cfg, target, now)      # fase 11: el golpe adelanta la obra, como una nota
    # el pumping: pico (vertical - 1) por los pulsos y la velocidad, y caida
    # del pad con un tope por el ritmo: el golpe entero (pico sostenido y
    # caida) cabe en 0,8 x el tiempo desde el golpe anterior en la celda, para
    # que vuelva a 1 antes del siguiente (en una rafaga, 0,8 x el paso)
    pico = (n - 1.0) * max(0.0, cfg['pump_amt']) * vel_bomba(cfg, vel)
    rel = pump_rel_pad(cfg, pad)
    hold = max(0.0, cfg['pump_hold'])
    b = W['bomba'].get(target)
    if b and b['n'] == 0:               # en el mismo fotograma (bombo y tom a la vez): el mayor
        b['pico'] = max(b['pico'], pico)
        b['rel'] = max(b['rel'], min(rel, b['tope']))
    else:                               # retrigger en seco: otra vez al pico
        sostiene = max(hold, BOMBA_FOTOS * (W.get('foto_dt') or FOTO_DEF))
        tope = max(0.0, BOMBA_TOPE * (now - W['imp_t'].get(target, -99.0)) - sostiene)
        W['bomba'][target] = dict(t0=now, pico=pico, rel=min(rel, tope), hold=hold, n=0, t2=None,
                                  tope=tope)
    W['imp_t'][target] = now
    light_cell(W, cfg, target, pad, 1.0, now)
    W['hits'][3] = W['hits'].get(3, 0) + 1
    W['drum'][pad] = dict(t=now, cell=target, vel=int(vel))
    ev = dict(pad=pad, modo='impulso', tipo='impulso', pulsos=n, celda=target, occ0=occ0,
              occ=W['occ'][target], desbordes=desbordes, bomba=pico, caida=W['bomba'][target]['rel'],
              vacia=occ0 <= 0, red=0, notas=0.0, rad=0, prof=0, quitado=0,
              dens=occupied(W) / float(N), doble=False, t=now)
    W['ev']['erosion'] = ev
    if cfg['nivel'] >= 9:
        W['flash'] = dict(t=now, cell=target, k=BOMBA_DESTELLO, pad=pad, bomba=True)
    W['dirty'] = True
    return ev


def impulso_tick(W, cfg, now):
    """Cada fotograma: cuenta los del pico de cada pumping y quita los acabados."""
    bomba = W.get('bomba')
    for i in list(bomba or {}):
        b = bomba[i]
        b['n'] += 1
        if b['n'] == BOMBA_FOTOS:
            b['t2'] = now
        if b['t2'] is not None and now >= max(b['t0'] + b['hold'], b['t2']) + b['rel']:
            del bomba[i]


def cut(W, cfg, target, depth, rad, now):
    """Corte en anfiteatro medido en la columna de cada celda: quita sus N
    losetas superiores (N-1 en el primer anillo...). Tope por mundo: un
    golpe que pide k losetas quita max(0, k - quitadas en este mundo). El
    nucleo es el fondo. Devuelve las losetas quitadas en la celda golpeada."""
    if n_shells(W) == 0:
        return 0
    hechos = []
    nucleo = None
    for c, d in rings(target, rad):
        k = int(depth) - d
        if k <= 0:
            continue
        col = W['cols'][c]
        antes = suelo(W, cfg, c)
        pide = max(0, k - W['quitadas'][c])
        W['quitadas'][c] += pide
        fuera = 0
        while fuera < pide and col:
            s, _ = col.pop()
            if 0 <= s < len(W['shells']):
                W['shells'][s]['rm'][c] = 1
            fuera += 1
        if not col and not W['nucleo_av'][c] and n_shells(W) > 0:
            W['nucleo_av'][c] = 1
            nucleo = c if nucleo is None or c == target else nucleo
        _clear_cell(W, c)
        if cfg['nivel'] >= 26:          # fase 26: el corte se lleva las inclusiones de la celda
            borrar_inclusiones(W, c, 'corte')
        W['huella'][c] = 0.0
        W['ruina'][c] = 0
        for j in NEIGH[c]:
            if W['par'][j] == c:
                W['par'][j] = -1
        hechos.append((c, fuera, antes, suelo(W, cfg, c)))
    # cicatrices: el fondo del corte y las paredes que han quedado al aire
    # (radio exterior por encima del suelo nuevo e interior por debajo del
    # anterior). Una celda que no ha perdido nada no expone nada.
    for c, fuera, antes, ahora in hechos:
        if fuera <= 0:
            continue
        if W['cols'][c]:
            W['scars'][W['cols'][c][-1][0] * 1000 + c] = now
        for j in NEIGH[c]:
            for s, r_in, r_out in column_radii(W, cfg, j):
                if r_out > ahora + 1e-9 and r_in < antes - 1e-9:
                    W['scars'][s * 1000 + j] = now
    W['dirty'] = True
    fuera_t = next((f for c, f, _, _ in hechos if c == target), 0)
    W['ev']['corte'] = dict(celda=target, conchas=fuera_t, celdas=len(hechos), t=now, radio=int(rad),
                            suelo=suelo(W, cfg, target), laguna=laguna(W, cfg, target),
                            nucleo=nucleo)
    if nucleo is not None:
        W['aviso'] = 'celda %d: el corte ha llegado al nucleo' % nucleo
    return fuera_t


# -----------------------------------------------------------------------------
# 1. NUCLEO - conchas (fase 8)
# -----------------------------------------------------------------------------

MINERAL = [
    (0.55, 0.36, 0.16),    # ambar de la base
    (0.40, 0.39, 0.37),
    (0.17, 0.17, 0.18),
    (0.47, 0.31, 0.16),
    (0.29, 0.29, 0.28),
    (0.10, 0.10, 0.11),
    (0.36, 0.32, 0.26),
    (0.23, 0.22, 0.24),
]


def shell_color(gen):
    """Color mineral de una generacion (paleta 'mineral', la anterior)."""
    return MINERAL[int(gen) % len(MINERAL)]


# --- paleta de generaciones (motor v26): cada concha de un color -------------------
# Tono por el angulo aureo sobre el arco que dejan libres las bandas
# reservadas (cian de la cicatriz y ambar del SEQ2), luminosidad que alterna
# claro y oscuro, croma contenido de mineral. En OKLCH, convertido a sRGB.
# El color sale de la generacion y de los parametros: no se guarda.

PALETAS = ['generaciones', 'mineral']
# tono OKLCH reservado: ambar del SEQ2 (55-100); desde el motor v46, una sola
# banda de 120 a 275 con los verdes de los pisos (120-165), el cian de la
# cicatriz (165-235) y el azul de los rios (235-275). Motor v68: con la industria,
# tambien el violeta electrico de su red (285-315; las demas paletas no cambian)
BANDAS_RESERVADAS = ((55.0, 100.0), (120.0, 275.0))
BANDA_RED = (285.0, 315.0)
BANDAS_INDUSTRIA = BANDAS_RESERVADAS + (BANDA_RED,)


def bandas_de(cfg):
    return BANDAS_INDUSTRIA if cfg is not None and tema_de(cfg) == 'industria' else BANDAS_RESERVADAS
AUREO = 0.6180339887
# luminosidad (motor v53, conchas discretas): media Paletaluz, alternando
# +- Paletaalterna / 2 (par oscura, impar clara); la loseta ocupada,
# Contrasteocupada mas clara. Hasta la v52, fijas: 0,50 / 0,64 y +0,12
# (Paletaluz 0,57, Paletaalterna 0,14, Contrasteocupada 0,12).
L_VACIA = (0.50, 0.64)                                  # los valores antiguos (referencia)
TAPA_LUZ_K = 0.8        # motor v62: luminosidad de la tapa = 0,8 x Paletaluz (antes Tapaluz, 0,28)
L_OCUPADA = 0.12


def palette_l(cfg, gen, ocupada):
    """Luminosidad OKLCH de la loseta de la generacion gen."""
    luz = cfg.get('paleta_luz', 0.35)
    alt = cfg.get('paleta_alterna', 0.06)
    L = luz + (0.5 if int(gen) % 2 else -0.5) * alt
    return L + (cfg.get('contraste_ocupada', 0.04) if ocupada else 0.0)
COL_ZOCALO_NEUTRO = (0.12, 0.12, 0.13)                  # zocalo: oscuro y neutro


def _en_banda(h, bandas=BANDAS_RESERVADAS):
    return any(a <= h < b for a, b in bandas)


def palette_hue(n, t0=20.0, bandas=BANDAS_RESERVADAS):
    """Tono OKLCH (grados) de la generacion n: t0 + frac(n * aureo) * arco
    libre, recorriendo el circulo y saltando las bandas reservadas."""
    libre = 360.0 - sum(b - a for a, b in bandas)
    x = ((int(n) * AUREO) % 1.0) * libre
    h = float(t0) % 360.0
    for _ in range(2):
        for a, b in bandas:                 # si el tono base cae en una banda, empieza a su salida
            if a <= h < b:
                h = b
    for _ in range(2 * len(bandas) + 2):
        dist, fin = min(((a - h) % 360.0 or 360.0, b) for a, b in bandas)
        if x < dist:
            return (h + x) % 360.0
        x -= dist
        h = fin % 360.0
    return h


def oklch_to_srgb(L, C, h):
    """((r, g, b) sRGB 0-1, dentro_de_gama). Bjorn Ottosson, OKLab."""
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    lin = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    dentro = all(-1e-6 <= x <= 1.0 + 1e-6 for x in lin)
    enc = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return tuple(enc(max(0.0, min(1.0, x))) for x in lin), dentro


_PAL = {}


def generation_color(cfg, gen, ocupada):
    """Color de una loseta de la generacion gen (paleta de generaciones)."""
    bandas = bandas_de(cfg)             # motor v76: la industria salta tambien el violeta de su red
    key = (round(cfg['paleta_tono'], 6), round(cfg['paleta_croma'], 6), round(cfg.get('paleta_luz', 0.35), 6),
           round(cfg.get('paleta_alterna', 0.06), 6), round(cfg.get('contraste_ocupada', 0.04), 6),
           int(gen), bool(ocupada), bandas)
    col = _PAL.get(key)
    if col is None:
        L = palette_l(cfg, gen, ocupada)
        col = oklch_to_srgb(L, cfg['paleta_croma'], palette_hue(gen, cfg['paleta_tono'], bandas))[0]
        if len(_PAL) > 4096:
            _PAL.clear()
        _PAL[key] = col
    return col


def tile_color(cfg, sh, occ, s=0):
    """Color de la loseta de una celda con ocupacion occ en la concha sh."""
    gen = sh.get('gen', s)
    if cfg.get('paleta', 0) == 1:           # mineral: la paleta anterior, tal cual
        return _tint(shell_color(gen), 0.75 + 0.35 * min(1.0, occ / 4.0))
    return generation_color(cfg, gen, occ > 0)


def zocalo_color(cfg):
    return COL_ZOCALO if cfg.get('paleta', 0) == 1 else COL_ZOCALO_NEUTRO


def palette_key(cfg):
    return (cfg.get('tema'), cfg.get('paleta', 0), cfg.get('paleta_tono'), cfg.get('paleta_croma'),
            cfg.get('paleta_luz'), cfg.get('paleta_alterna'), cfg.get('contraste_ocupada'),
            cfg.get('tapa_neutra'), cfg.get('tapa_luz'),
            cfg['nivel'] >= 15, cfg.get('respaldo', 0))


# --- tapa atenuada (motor v53): el color se reserva a los flancos ---------------
# La cara de arriba de la loseta superior de cada columna (el suelo que se ve
# desde la camara de globo) se mezcla Tapaneutra hacia un gris neutro de
# luminosidad Tapaluz; los flancos, que ensenan los cortes, conservan el
# color de su concha. Una instancia fina por columna (la tapa) sobre su
# loseta: N instancias mas, no el doble. Mate (rugosidad 1). Solo con la
# paleta de generaciones; Tapaneutra 0 no la dibuja.

TAPA_GROSOR = 0.02          # alto de la tapa (como mucho un 25 % de la loseta)
TAPA_K = 1.004              # la tapa envuelve la loseta: sin parpadeo en los flancos
TAPA_ASOMA = 0.004          # y asoma por arriba (menos que la luz de las conchas, 1,2 %)
RUG_TAPA = 1.0              # mate: no compite con los reflejos de lo pulido


def tapa_on(cfg):
    return cfg.get('paleta', 0) != 1 and cfg.get('tapa_neutra', 0.0) > 0


def tapa_gris(cfg):
    return oklch_to_srgb(cfg.get('tapa_luz', 0.28), 0.0, 0.0)[0]


def tapa_color(cfg, col):
    """Color de la tapa sobre una loseta de color col."""
    return _mix(col, tapa_gris(cfg), max(0.0, min(1.0, cfg.get('tapa_neutra', 0.0))))


def _tapa_row(fila, col):
    """La tapa de una loseta (fila de _tile_row): fina, arriba y un poco mas ancha."""
    p, n, h = fila[0:3], _norm(fila[0:3]), fila[7]
    hc = min(TAPA_GROSOR, 0.25 * h)
    t = list(fila)
    t[0:3] = list(_add(p, n, h - hc))
    t[6], t[7], t[8] = fila[6] * TAPA_K, hc + TAPA_ASOMA * h, fila[8] * TAPA_K
    t[9:12] = list(col)
    return t


def srgb_l(col):
    """Luminosidad OKLab (0-1) de un color sRGB 0-1."""
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in col]
    l = 0.4122214708 * lin[0] + 0.5363325363 * lin[1] + 0.0514459929 * lin[2]
    m = 0.2119034982 * lin[0] + 0.6806995451 * lin[1] + 0.1073969566 * lin[2]
    s = 0.0883024619 * lin[0] + 0.2817188376 * lin[1] + 0.6299787005 * lin[2]
    return 0.2104542553 * l ** (1 / 3.) + 0.7936177850 * m ** (1 / 3.) - 0.0040720468 * s ** (1 / 3.)


JERARQUIA_MARGEN = 0.15     # el suelo, al menos esto mas oscuro que lo construido


def jerarquia_suelo(cfg):
    """(luminosidad de la tapa mas clara posible, luminosidad de las
    formaciones). La tapa: la loseta impar ocupada (Paletaluz + Paletaalterna/2
    + Contrasteocupada) mezclada Tapaneutra hacia Tapaluz. Las formaciones: la
    media de las dos especies (COL_GEO, COL_ARQ), en OKLab."""
    lmax = cfg.get('paleta_luz', 0.35) + cfg.get('paleta_alterna', 0.06) / 2 + cfg.get('contraste_ocupada', 0.04)
    tn = max(0.0, min(1.0, cfg.get('tapa_neutra', 0.0))) if tapa_on(cfg) else 0.0
    l_tapa = (1.0 - tn) * lmax + tn * cfg.get('tapa_luz', 0.28)
    return l_tapa, 0.5 * (srgb_l(COL_GEO) + srgb_l(COL_ARQ))


def shell_grosor(cfg, bars=None):
    """Grosor de la concha nueva. Con Grosortiempo, proporcional a lo que
    duro su mundo: Shellthick por cada Ciclomin compases, entre 0,25x y
    Ciclomax / Ciclomin, y nunca mas de Grosormax."""
    th = cfg['shell_thick']
    if bars is None or not cfg['grosor_tiempo']:
        return th
    cmin, cmax = cycle_bounds(cfg)
    g = th * max(0.25, min(cmax / float(cmin), bars / float(cmin)))
    gmax = cfg['grosor_max']
    return min(g, gmax) if gmax > 0 else g


COMPACTA_CRECE = 0.10       # el radio sube al menos un 10 % de cada concha nueva


def compactar(W, cfg, g):
    """La concha nueva (grosor g) aplasta las de debajo (motor v37). Todas
    pierden la misma fraccion, 1 - e^(-g / Cortezamax), asi que la corteza
    (lo que hay sobre el nucleo) tiende a Cortezamax y el planeta deja de
    engordar: las conchas recientes se leen gruesas y las viejas se aprietan
    en vetas finas, como en un corte geologico. El radio sube siempre al
    menos COMPACTA_CRECE x g; nunca baja. Cortezamax 0: sin compactar (el
    radio es el tiempo). Las losetas de cada columna se aplastan igual, asi
    que cortes, hondonadas y lagunas conservan su forma. Devuelve el factor."""
    D = cfg.get('corteza_max', 0.0)
    C = top_radius(W, cfg) - cfg['core_radius']
    if D <= 0 or C <= 1e-9 or g <= 0:
        return 1.0
    perdida = min(C * (1.0 - math.exp(-g / D)), (1.0 - COMPACTA_CRECE) * g)
    k = 1.0 - perdida / C
    r = cfg['core_radius']
    for sh in W['shells']:
        sh['grosor'] = shell_th(sh, cfg) * k
        if 'r_in' in sh:
            sh['r_in'], sh['r_out'] = r, r + sh['grosor']
        r += sh['grosor']
    for col in W['cols']:
        for los in col:
            los[1] *= k
    return k


def sedimenta(W, cfg):
    """[bool por celda]: donde deja su loseta la concha que entierra este mundo. Siempre,
    salvo en la naturaleza con Oceano: alli solo donde se creo algo o llego un desborde
    en este mundo (ocupada, con carga, nacida en el o erosionada en el) y donde las
    personas dejaron su huella (inclusiones, fase 25) o abrieron una escision (fase 29).
    Motor v100."""
    if cfg['nivel'] < 11 or tema_de(cfg) != 'naturaleza' or not cfg.get('oceano'):
        return [True] * N
    t0 = W.get('ciclo_t0')
    quit_ = W.get('quitadas') or [0] * N
    incl = W.get('incl') if cfg['nivel'] >= 25 and len(W.get('incl', ())) == N else None
    esc = W.get('esc_celdas', {}) if cfg['nivel'] >= 29 else {}
    return [bool(W['occ'][c] > 0 or W['carga'][c] > 0 or quit_[c] > 0
                 or (t0 is not None and W['t_nac'][c] >= t0 and W['own'][c])
                 or (incl is not None and incl[c]) or c in esc)
            for c in range(N)]


def nivel_mar(W, cfg):
    """El radio del mar: el suelo mas bajo del planeta (motor v100). Una celda cuyo suelo
    queda por encima es tierra, tenga o no algo encima."""
    return min(suelos_fotograma(W, cfg))


def end_cycle(W, cfg, now, bars=None, motivo=None):
    """Entierra el mundo (desde el nivel 8). bars: compases que duro; sin
    ellos, la concha tiene Shellthick. motivo: el del fin de ciclo (fase 27: la
    concha lo guarda como marca de cierre)."""
    W['ev']['ciclo'] = dict(t=now, n=W.get('ciclo_n', 1))
    W['bomba'] = {}                     # fase 7: sin pumping pendiente
    W['imp_t'] = {}
    if cfg['nivel'] < 8:
        return False
    if cfg['nivel'] >= 31:              # fase 31: el testigo de las escisiones, antes de enterrar
        testigos_al_enterrar(W, cfg, now)
    cerrar_obras(W, cfg)                # los transitos se cierran antes de hornear
    reg = registro_concha(W, cfg) if cfg['nivel'] >= 15 else None
    clas = clasificar_concha(W, cfg, dict(motivo=motivo, t=now)) if cfg['nivel'] >= 27 else None
    g = shell_grosor(cfg, bars)
    W['compacta'] = compactar(W, cfg, g)
    r_in = top_radius(W, cfg)
    # cada celda deposita su loseta sobre lo que le queda debajo: una
    # hondonada se tapiza y sigue siendo hondonada, salvo lo que rellene
    # Colmatacion. El radio nominal solo crece g (la colmatacion no es tiempo).
    colm = cfg.get('colmatacion', 0.0)
    s_new = len(W['shells'])
    huecos = W.get('esc_celdas', {}) if cfg['nivel'] >= 29 else {}
    # motor v100: con Oceano (naturaleza) solo sedimenta lo que se creo o se desbordo en este
    # mundo; el mar no se entierra. Esas celdas quedan sin loseta de esta concha (rm = 1).
    seca = sedimenta(W, cfg)
    for c in range(N):
        if not seca[c]:
            continue
        lg = max(0.0, r_in - suelo(W, cfg, c))
        # fase 29: en la celda de una escision la concha tapiza el hueco sin cerrarlo (sin Colmatacion)
        W['cols'][c].append([s_new, g + (0.0 if c in huecos else colm * lg)])
    W['shells'].append(dict(gen=W['gen'], col=list(shell_color(W['gen'])),
                            occ=list(W['occ']), sp=list(W['sp']), rm=[0 if x else 1 for x in seca],
                            grosor=g, r_in=r_in, r_out=r_in + g))
    if reg:                             # fase 15: el registro de la concha
        W['shells'][-1].update(reg)
    if clas:                            # fase 27: humana o limpia, con sus inclusiones horneadas
        W['shells'][-1].update(clas)
        W['ev']['banda'] = dict(clas, concha=len(W['shells']) - 1, t=now)
    if cfg['nivel'] >= 28:              # fase 28: la noche empieza en el fotograma del recuento
        W['noche'] = [now, now + cfg['noche']] if cfg['noche'] > 0.0 else None
    if cfg['nivel'] >= 29:              # fase 29: las escisiones de este mundo quedan enterradas
        enterrar_escisiones(W, cfg, now)
    if cfg['nivel'] >= 31:              # fase 31: la jornada y el ciclo de la concha (la columna resumen)
        W['shells'][-1].update(jornada=_fecha()[0], ciclo=W.get('ciclo_n', 1))
    W['quitadas'] = [0] * N
    W['gen'] += 1
    if cfg['nivel'] >= 25:              # fase 25: lo heredado empieza sin inclusiones
        vaciar_inclusiones(W)
        W['incl_n'] = dict(llegadas=0, paradas=0)
    her = cfg['herencia']
    for i in range(N):
        W['carga'][i] = 0
        x = W['occ'][i] * her + W['resto'][i]
        n = int(math.floor(x + 1e-9))
        W['resto'][i] = x - n
        if n > 0 and W['own'][i]:
            W['occ'][i] = n
            W['h'][i] = height_for(cfg, n)
            W['par'][i] = -1
            W['traza'][i] = _bit(W['own'][i]) | (3 if W['sp'][i] == HIB else 0)
        else:
            W['occ'][i] = 0
            W['h'][i] = 0.0
            W['par'][i] = -1
        W['vh'][i] = 0.0           # lo heredado vuelve a brotar de la superficie
        W['huella'][i] = 0.0
    W['pend'] = {}
    cerrar_obras(W, cfg)                # y lo heredado empieza sin obras a medias
    if reg:
        herencia_tematica(W, cfg, now, reg)
    W['dirty'] = True
    return True


def continents(W, last=8, thr=0.5):
    sh = W['shells'][-last:]
    if len(sh) < 2:
        return 0
    persist = [sum(1 for s in sh if s['occ'][c] > 0) / float(len(sh)) for c in range(N)]
    cells = set(c for c in range(N) if persist[c] >= thr)
    count = 0
    while cells:
        count += 1
        stack = [cells.pop()]
        while stack:
            c = stack.pop()
            for n in NEIGH[c]:
                if n in cells:
                    cells.discard(n)
                    stack.append(n)
    return count


# -----------------------------------------------------------------------------
# 1. NUCLEO - avance por fotograma
# -----------------------------------------------------------------------------

def tick(W, cfg, now, tempo=120.0, playing=True):
    last = W['t']
    dt = 0.0 if last is None else max(0.0, min(0.25, now - last))
    W['t'] = now
    a = 1.0 - math.exp(-dt / 0.12) if dt > 0 else 0.0
    piel = cfg['nivel'] >= 11
    W['paso'] = step_dur(cfg, tempo)
    sim = W.get('gate_sim')
    if sim:                         # fase 12: los note off simulados de los botones
        for t_off, s_, nota in sorted(e for e in sim if e[0] <= now):
            note_off(W, cfg, s_, nota, t_off, tempo)
        W['gate_sim'] = [e for e in sim if e[0] > now]
    for i in range(N):
        h, vh = W['h'][i], W['vh'][i]
        if piel:                    # fase 11: la altura, a saltos de stop-motion
            W['vh'][i] = vh = vh_stop(W, i, now, W['paso'])
        elif vh != h:
            vh += (h - vh) * a
            if abs(h - vh) < 1e-4:
                vh = h
            W['vh'][i] = vh
        if W['occ'][i] == 0 and vh < 0.01:
            W['vh'][i] = 0.0
            if W['sp'][i]:
                W['sp'][i] = W['own'][i] = W['traza'][i] = 0
    out = dict(ciclo=None, burst=None)
    if cfg['nivel'] >= 9 and W['scars']:
        st = cfg['scar_time']
        for k in [k for k, t0 in W['scars'].items() if now - t0 > st]:
            del W['scars'][k]
        W['dirty'] = True
    if cfg['nivel'] >= 6:
        out['burst'] = _resolve_burst(W, cfg, now, playing)
        out['ciclo'] = cycle_tick(W, cfg, now, dt, tempo, playing)
    if cfg['nivel'] >= 17:              # fase 17: el pulso, el frente y la biblioteca
        pulso_tick(W, cfg, dt, tempo, playing)
        if out['burst'] == 'cambio':
            out['frente'] = cambio_pattern(W, cfg)
        frente_tick(W, cfg)
    if piel:
        tick_piel(W, cfg, now, W['paso'], playing)
    if cfg['nivel'] >= 14:
        tick_destructores(W, cfg, now)
    if cfg['nivel'] >= 15:
        tick_rebrote(W, cfg, now)
    if cfg['nivel'] >= 7:               # fase 7: el pumping cuenta fotogramas y acaba
        if dt > 0:
            W['foto_dt'] = dt
        impulso_tick(W, cfg, now)
    if cfg['nivel'] >= 26:              # fase 26: la pasada de seguridad del borrado
        purga_segura(W)
    if cfg['nivel'] >= 28:              # fase 28: la noche acaba (y las losetas dejan de emitir)
        noche_tick(W, cfg, now)
    if cfg['nivel'] >= 23:              # fase 23: la luz de la sala y el colapso
        if sala_luz_tick(W, cfg, now) == 'colapso' and not out['ciclo']:
            out['ciclo'] = close_cycle(W, cfg, now, 'colapso')
    giro_step(W, cfg, dt, tempo)
    return out


# -----------------------------------------------------------------------------
# 1. NUCLEO - instancias para dibujar
# -----------------------------------------------------------------------------

def _cell_sizes(r, i):
    """(ancho este-oeste, largo norte-sur) de la celda i a radio r: la
    medida de su anillo."""
    return r * SIZE_EW[i], r * SIZE_NS[i]


def _row(p, n, sx, sy, sz, col):
    rx, ry = orient(n)
    return [p[0], p[1], p[2], rx, ry, 0.0, sx, sy, sz, col[0], col[1], col[2]]


def _tint(col, k):
    return (min(1.0, col[0] * k), min(1.0, col[1] * k), min(1.0, col[2] * k))


def _mix(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


COL_GEO = (0.62, 0.60, 0.56)
COL_ARQ = (0.34, 0.36, 0.40)
COL_HUELLA = (0.13, 0.09, 0.06)
COL_CROWN = (1.00, 0.70, 0.30)
COL_SCAR = (0.10, 0.90, 1.00)

COL_POROSO = (0.30, 0.25, 0.20)       # tierra: lo poroso se apaga hacia aqui
COL_BRILLO = (0.92, 0.95, 1.00)       # lo pulido se aclara hacia aqui


def _material_col(base_col, pulido):
    """Pulido: claro, frio y limpio. Poroso: oscuro, terroso, apagado."""
    if pulido:
        return _tint(_mix(base_col, COL_BRILLO, 0.30), 1.25)
    return _tint(_mix(base_col, COL_POROSO, 0.45), 0.72)


# Latido: la nota hincha la formacion un 12 % y la tine (75 %) del color de su
# secuenciador (o el golpe, del de su pad) mientras el gate esta abierto (lo que dura la nota, del note
# on al note off); al soltarla se apaga en ~0,25 s. Una nota corta da un
# destello; una ligada, una formacion encendida todo lo que suena.
LATIDO_AMP, LATIDO_DUR, LATIDO_TINTE = 0.12, 0.25, 0.75


def _latido(W, i, now):
    if held(W, now, cell=i):
        return 1.0
    dt = now - W['lat'][i]
    if dt < 0 or dt > 4 * LATIDO_DUR:
        return 0.0
    return math.exp(-dt / LATIDO_DUR)


def _luz_formacion(W, cfg, i, now):
    """(intensidad, color, hinchado) del latido de la formacion de la celda i:
    la nota del secuenciador o el golpe de bateria, el mas intenso. Un golpe
    de impulso (fase 7 v12) no tapa al secuenciador que suena en la celda, y
    con Pumpon no hincha: la hincha el pumping."""
    lt = _latido(W, i, now)
    sc = seq_color(cfg, W['lat_s'][i] if W['lat_s'][i] in (1, 2) else 1)
    amp = LATIDO_AMP
    Id, pd_ = drum_light(W, cfg, i, now)
    if pd_ is not None and Id >= lt:
        imp = es_impulso(cfg, pd_)
        if not (imp and lt > 0):
            lt, sc = Id, drum_color(cfg, pd_)
            if imp and cfg.get('pump_on', 1):
                amp = 0.0
    return lt, sc, amp


# --- pumping (fase 7 v12): la celda golpeada por un impulso se hincha ----------
SIN_BOMBA = ('particulas', 'luz_celda', 'luz_conchas', 'estratos')
_MODELO_DE_GEO = {}


def _modelo_de_geo(cfg):
    doble = cfg['nivel'] < 12
    m = _MODELO_DE_GEO.get(doble)
    if m is None:
        m = _MODELO_DE_GEO[doble] = dict((g, mo) for g, mo, _ in geometrias_piel(cfg))
    return m


def escalas_bomba(W, cfg, i, now):
    """(vertical, horizontal pedida) del pumping de la celda i: 1 + valor y
    1 + valor x Pumphorz. Sin pumping (o con Pumpamt 0), (1, 1)."""
    if not cfg.get('pump_on', 1) or cfg['nivel'] < 7:
        return 1.0, 1.0
    v, _ = bomba_nivel(W, cfg, i, now)
    return 1.0 + v, 1.0 + v * max(0.0, cfg['pump_horz'])


class _Bomba(object):
    """Hincha lo que dibuja cada celda con pumping: anclado en su base y
    sobre su normal (crece hacia fuera, no se hunde en el planeta). De ancho,
    lo que deje la celda: ninguna pieza pasa del ancho de su celda (la regla
    de los anillos polares), y si alguna ya lo pasa (un puente del cluster),
    la celda no se ensancha. Uso: cerrar() al empezar cada celda, abrir()
    antes de dibujar su formacion y cerrar() al acabar."""

    def __init__(self, W, cfg, now, out):
        self.on = bool(W.get('bomba')) and bool(cfg.get('pump_on', 1)) and cfg['nivel'] >= 7
        self.W, self.cfg, self.now, self.out = W, cfg, now, out
        self.techo = max(1.0, cfg.get('pump_tope', 2.0)) * limit(cfg)    # v14: Pumptope x el limite
        self.i = None
        self.hechas = {}            # celda -> (vertical, horizontal) aplicadas

    def abrir(self, i, p0, n, cw, cl):
        self.cerrar()
        if not self.on or i not in self.W['bomba']:
            return
        sv, sh = escalas_bomba(self.W, self.cfg, i, self.now)
        if sv <= 1.0 + 1e-9:
            return
        self.i, self.p0, self.n, self.cw, self.cl, self.sv, self.sh = i, p0, n, cw, cl, sv, sh
        self.marcas = dict((k, len(v)) for k, v in self.out.items() if isinstance(v, list))

    def cerrar(self):
        if self.i is None:
            return
        i, p0, n = self.i, self.p0, self.n
        self.i = None
        e, t = tangents(n)
        modelos = _modelo_de_geo(self.cfg) if self.cfg['nivel'] >= 11 else {}
        filas = []
        for k, v in self.out.items():
            if k in SIN_BOMBA or not isinstance(v, list):
                continue
            ex, ey, ez = _ext_modelo(modelos[k]) if k in modelos else CAJA_EXT
            for f in v[self.marcas.get(k, 0):]:
                rel = (f[0] - p0[0], f[1] - p0[1], f[2] - p0[2])
                h = _dot(rel, n)
                lado = max(ex * abs(f[6]), ez * abs(f[8]))
                filas.append((f, h, _add(rel, n, -h), abs(_dot(rel, e)) + lado, abs(_dot(rel, t)) + lado,
                              h + ey * abs(f[7])))
        if not filas:
            return
        # de alto, sin pasar de Pumptope x el limite (si ya lo pasa, no se hincha)
        alto = max(x[5] for x in filas)
        sv = min(self.sv, max(1.0, self.techo / alto)) if alto > 1e-9 else self.sv
        # de ancho, lo que pida el alto, sin pasar del ancho de la celda
        tope = min(min(0.5 * self.cw / max(1e-9, x[3]), 0.5 * self.cl / max(1e-9, x[4])) for x in filas)
        sh = min(1.0 + (sv - 1.0) * max(0.0, self.cfg['pump_horz']), max(1.0, tope))
        for f, h, hor, _, _, _ in filas:
            q = _add(_add(p0, n, h * sv), hor, sh)
            f[0], f[1], f[2] = q[0], q[1], q[2]
            f[6] *= sh
            f[7] *= sv
            f[8] *= sh
        self.hechas[i] = (sv, sh)


def _porous_column(p, d, w, hh, wz, col, out, seed):
    """Una pieza porosa: tramos apilados de ancho irregular, con grietas
    entre ellos y algun grumo pegado. Se lee rugosa con cualquier luz."""
    nseg = 3 if hh > 0.25 else 2
    seg = hh / nseg
    e, t = tangents(d)
    for j in range(nseg):
        a, b, c = (_hash01(seed, j, q) for q in (5, 6, 7))
        kw = 0.72 + 0.45 * a
        q = _add(_add(_add(p, d, j * seg), e, (b - 0.5) * 0.18 * w), t, (c - 0.5) * 0.18 * wz)
        out.append(_row(q, d, w * kw, seg * 0.84, wz * (0.72 + 0.45 * c),
                        _tint(col, 0.78 + 0.30 * b)))
    for j in range(2):                      # grumos
        a, b = _hash01(seed, j, 8), _hash01(seed, j, 9)
        side = 1.0 if j == 0 else -1.0
        q = _add(_add(p, d, hh * (0.25 + 0.45 * a)), e, side * 0.55 * w)
        g = 0.32 * w * (0.7 + 0.6 * b)
        out.append(_row(q, d, g, g, g, _tint(col, 0.7)))


def _geo_pieces(W, cfg, i, p0, n, vh, cl, scale, col, out, cw=None, pulido=True):
    e, t = tangents(n)
    cx = min(cl, cw) if cw else cl      # ancho este-oeste real de la celda
    kx = cx / cl
    occ = max(1, W['occ'][i])
    count = 1 + (1 if occ >= 2 else 0) + (1 if occ >= 3 else 0)
    if W['par'][i] >= 0:
        count = 1
    hk = (1.0, 0.62, 0.40)
    wk = (0.36, 0.26, 0.20)
    main_dir, main_top = n, p0
    for k in range(count):
        u1, u2, u3, u4 = (_hash01(i, k, q) for q in (1, 2, 3, 4))
        off = (0.0, 0.0) if k == 0 else ((u1 - 0.5) * 0.7 * cx, (u2 - 0.5) * 0.7 * cl)
        lean = 0.10 + 0.25 * u3
        d = _norm(_add(_add(n, e, kx * lean * (u4 - 0.5) * 2), t, lean * (u1 - 0.5) * 2))
        p = _add(_add(p0, e, off[0]), t, off[1])
        w = wk[k] * cl * scale * (0.8 + 0.4 * u2)
        hh = vh * hk[k]
        if pulido:                          # prisma limpio, algo mas esbelto
            out.append(_row(p, d, 0.85 * w * kx, hh, 0.85 * w * (0.7 + 0.5 * u3),
                            _tint(col, 0.95 + 0.1 * u4)))
        else:
            _porous_column(p, d, w * kx, hh, w * (0.7 + 0.5 * u3), col, out, i * 7 + k)
        if k == 0:
            main_dir, main_top = d, _add(p, d, hh)
    return main_dir, main_top


def _arq_pieces(W, cfg, i, p0, n, vh, cl, scale, col, out, cw=None, pulido=True):
    lim = limit(cfg)
    floor_h = 0.25 * lim
    w = 0.48 * cl * scale
    wx = 0.48 * (min(cl, cw) if cw else cl) * scale
    e, t = tangents(n)
    k = 0
    while k * floor_h < vh - 1e-4 and k < 32:
        p = _add(p0, n, k * floor_h)
        if pulido:                          # torre de cristal: plantas casi pegadas
            hh = min(floor_h, vh - k * floor_h) * 0.97
            out.append(_row(p, n, wx, hh, w, _tint(col, 0.97 + 0.06 * (k % 2))))
        else:                               # hormigon: plantas desiguales y descolgadas
            a, b = _hash01(i, k, 11), _hash01(i, k, 12)
            hh = min(floor_h, vh - k * floor_h) * 0.72
            p = _add(_add(p, e, (a - 0.5) * 0.12 * wx), t, (b - 0.5) * 0.12 * w)
            kw = 0.80 + 0.30 * a
            out.append(_row(p, n, wx * kw, hh, w * (0.80 + 0.30 * b), _tint(col, 0.75 + 0.3 * b)))
        k += 1
    return n, _add(p0, n, vh)


def build_instances(W, cfg, now, hide_beacons=False, tiles=True, refresco=False):
    t_py = _time.perf_counter()
    out = _build_instances(W, cfg, now, hide_beacons, tiles, refresco)
    _TURNOS['ms_inst'] = (_time.perf_counter() - t_py) * 1000.0     # motor v101: para la leyenda PIEL
    return out


def _build_instances(W, cfg, now, hide_beacons=False, tiles=True, refresco=False):
    lvl = cfg['nivel']
    _TERRENO['sello'] = _TERRENO.get('sello', 0) + 1     # un fotograma: el terreno se mira una vez
    lim = limit(cfg)
    out = dict(formas_pulidas=[], formas_porosas=[], coronas=[], estratos=[], luz_celda=[],
               luz_conchas=[])
    R = top_radius(W, cfg)
    piel = lvl >= 11
    if piel:                        # fase 11: todas las geometrias de los modelos, vacias
        for g, _, _ in geometrias_piel(cfg):
            out[g] = []
        out['particulas'] = []
    bomba = _Bomba(W, cfg, now, out)    # fase 7 v12: el pumping de los impulsos
    for i in range(N):
        bomba.cerrar()
        vh = W['vh'][i]
        own = W['own'][i]
        n = normal_i(i)
        base = base_radius(W, cfg, i)
        p0 = _mul(n, base)
        cw, cl = _cell_sizes(base, i)
        if vh <= 0.005 or not own:
            if lvl >= 7 and W['huella'][i] > 0 and W['occ'][i] == 0:
                out['formas_porosas'].append(
                    _row(_add(p0, n, 0.01), n, 0.45 * min(cl, cw), 0.03, 0.45 * cl, COL_HUELLA))
            continue
        if piel:                    # las formaciones son modelos del tema (build_piel)
            continue
        bomba.abrir(i, p0, n, cw, cl)
        pulido = W['vel'][i] >= cfg['vel_umbral']
        lst = out['formas_pulidas'] if pulido else out['formas_porosas']
        sat = W['par'][i] >= 0
        scale = cfg['sat_size'] if sat else 1.0
        base_col = COL_GEO if own == GEO else COL_ARQ
        col = _material_col(base_col, pulido)
        lt, sc, amp = _luz_formacion(W, cfg, i, now)     # la nota o el golpe, igual
        if lt > 0:                  # la nota o el golpe: la formacion se enciende
            vh *= 1.0 + amp * lt
            col = _tint(_mix(col, sc, LATIDO_TINTE * lt), 1.0 + 0.25 * lt)
        if sat:
            col = _tint(col, 0.85)
        if own == GEO:
            d, top = _geo_pieces(W, cfg, i, p0, n, vh, cl, scale, col, lst, cw, pulido)
        else:
            d, top = _arq_pieces(W, cfg, i, p0, n, vh, cl, scale, col, lst, cw, pulido)
        e, t = tangents(n)
        # hibridos: la otra especie deja su rastro
        if W['sp'][i] == HIB:
            if own == GEO:          # macizo aterrazado
                for k in range(2):
                    hh = 0.10 * lim
                    p = _add(p0, n, (0.15 + 0.3 * k) * vh)
                    ww = (0.48 - 0.14 * k) * cl * scale
                    lst.append(_row(p, n, ww * min(1.0, cw / cl), hh, ww, _tint(COL_ARQ, 1.1)))
            else:                   # torre mineralizada
                for k, side in enumerate((1.0, -1.0)):
                    p = _add(_add(p0, n, (0.3 + 0.25 * k) * vh), e, side * 0.17 * min(cl, cw) * scale)
                    dd = _norm(_add(n, e, side * 0.9))
                    ww = 0.07 * cl * scale
                    lst.append(_row(p, dd, ww, 0.35 * vh, ww, _tint(COL_GEO, 1.05)))
        if lvl >= 4:
            o = W['occ'][i]
            fused = (not sat and o >= cfg['th_fusion']) or \
                    (sat and W['occ'][W['par'][i]] >= cfg['th_fusion'])
            if fused:
                kk = 0.80 if not sat else 0.70
                lst.append(_row(p0, n, kk * cw, 0.30 * lim, kk * cl, _tint(base_col, 0.7)))
            if not sat and o >= cfg['th_crown']:
                # cumbre: cada trigger alarga la corona un 25 %, hasta Tramoscumbre
                tr = cumbre_tramos(cfg, o)
                kl, kw = 1.0 + 0.25 * tr, 1.0 + 0.15 * tr
                if own == GEO:
                    out['coronas'].append(_row(top, d, 0.06 * kw * cl, 0.70 * kl * lim,
                                               0.06 * kw * cl, COL_CROWN))
                else:
                    out['coronas'].append(_row(top, n, 0.03 * kw * cl, 0.90 * kl * lim,
                                               0.03 * kw * cl, COL_CROWN))
                    out['coronas'].append(_row(top, n, 0.20 * cl, 0.05 * lim, 0.20 * cl, COL_CROWN))
    bomba.cerrar()
    if piel:
        W['piel'] = build_piel_refresco(W, cfg, now, out) if refresco else build_piel(W, cfg, now, out)
    if lvl >= 13:                   # fase 13: carreteras (tejido) y rios (fase 13 v2, su geometria)
        out['tejido'], W['tejido'] = build_tejido(W, cfg)
        out['rios'], W['rios_res'] = build_rios(W, cfg)
        build_industria_tejido(W, cfg, now, out)        # fase 13 v7: viaductos, torres, pulsos y trenes
    if lvl >= 14:                   # fase 14: huellas y particulas de los destructores
        build_destructores(W, cfg, now, out)
    if lvl >= 16:                   # fase 16: lo que ensenan los cortes
        build_arqueologia(W, cfg, now, out)
    if lvl >= 17:                   # fase 17: trafico, esporas y el frente
        build_tiempo(W, cfg, now, out)
    if lvl >= 18:                   # fase 18: luz local y, fuera de la actuacion, el diagnostico
        out['luz_local'] = build_luz_local(W, cfg, now)
        out['diagnostico'] = [] if hide_beacons or not cfg.get('diagnostico', 0) else build_diagnostico(W, cfg)
    if lvl >= 25:                   # fase 25: las inclusiones de las personas
        build_inclusiones(W, cfg, now, out)
    if lvl >= 29:                   # fase 29: las fulguritas de las escisiones
        build_fulguritas(W, cfg, now, out)
    out['luz_celda'] = cell_lights(W, cfg, now)  # parte del mundo: tambien en actuacion
    out['luz_conchas'] = shell_lights(W, cfg, now)
    if lvl >= 8 and tiles:
        out['estratos'] = build_tiles(W, cfg, now)
    if lvl >= 28:                   # fase 28: la noche apaga las capas de luz y las particulas
        noche_filas(out, 1.0 - noche_nivel(W, cfg, now))
    return out


COL_ZOCALO = _tint(MINERAL[0], 0.55)   # basamento: ambar de la base, apagado


def build_tiles(W, cfg, now):
    """Losetas de cada columna: las Maxconchas superiores, cada una a su
    radio, y debajo un zocalo (una sola instancia) hasta el nucleo."""
    rows = []
    maxs = max(1, int(cfg['max_shells']))
    st = cfg['scar_time']
    core = cfg['core_radius']
    era = cfg['nivel'] >= 15                # fase 15: la rugosidad de cada loseta (canal a)
    respaldo = era and cfg.get('respaldo', 0)
    humano = cfg['nivel'] >= 27             # fase 27: las inclusiones horneadas
    q_tapa = 0
    # fase 28: durante la noche, la concha recien enterrada (sus motas emiten)
    recien = len(W['shells']) - 1 if cfg['nivel'] >= 28 and W.get('noche') else -1
    for c in range(N):
        col = column_radii(W, cfg, c)
        if not col:
            continue
        n = normal_i(c)
        first = max(0, len(col) - maxs)
        if first > 0:                       # zocalo: del nucleo a la loseta dibujada mas baja
            top = col[first][1]
            cw, cl = _cell_sizes(top, c)
            if is_pole(c):
                cw, cl = cw * 1.25, cl * 1.25
            rows.append(_row(_mul(n, core), n, cw * 1.04, (top - core) * 0.98, cl * 1.04,
                             zocalo_color(cfg)))
            if era:
                rows[-1].append(1.0 if respaldo else RUG_ZOCALO)
        tapa = None
        q_tapa = 0
        for s, r_in, r_out in col[first:]:
            sh = W['shells'][s]
            colr, rug = tile_material(cfg, sh, s, c)
            ctapa = tapa_color(cfg, colr) if tapa_on(cfg) else None
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None:              # la cicatriz manda, tambien sobre la tapa
                f = max(0.0, min(1.0, (now - t0) / st))
                colr = _mix(COL_SCAR, colr, f)
                if ctapa is not None:
                    ctapa = _mix(COL_SCAR, ctapa, f)
            rows.append(_tile_row(c, n, r_in, r_out, colr))
            q = cobertura_q(cfg, sh, c) if humano and not respaldo else 0
            if era:                         # fase 27: alfa = rugosidad + 2 x cobertura de inclusiones (en veinteavos)
                rows[-1].append(1.0 if respaldo else rug + 2.0 * q)
                if q and s == recien:       # fase 28: recien horneada (emite en la noche): alfa + 100
                    rows[-1][-1] += ALFA_RECIENTE
            if ctapa is not None:
                tapa = _tapa_row(rows[-1][:12], ctapa)
                q_tapa = q
        if tapa is not None:                # solo la loseta de arriba ensena su tapa
            if era:                         # fase 25: con inclusiones, la matriz del plastiglomerado
                con_incl = cfg['nivel'] >= 25 and bool(W['incl'][c]) if len(W.get('incl', ())) == N else False
                if q_tapa:                  # fase 27: la cara de la loseta de un estrato humano, con sus motas
                    tapa.append(RUG_TAPA_INCL + 2.0 * q_tapa + (ALFA_RECIENTE if s == recien else 0.0))
                else:
                    tapa.append(1.0 if respaldo else (RUG_TAPA_INCL if con_incl else RUG_TAPA))
            rows.append(tapa)
    return rows


def _tile_row(c, n, r_in, r_out, col, k=1.0, kh=1.0):
    """Una loseta de la columna de c entre r_in y r_out (k: ancho relativo,
    kh: alto relativo; la loseta normal es 1, 1)."""
    th = r_out - r_in
    cw, cl = _cell_sizes(0.5 * (r_in + r_out), c)
    if is_pole(c):
        cw, cl = cw * 1.25, cl * 1.25
    return _row(_mul(n, r_in), n, cw * 1.04 * k, th * 0.98 * kh, cl * 1.04 * k, col)


# --- la luz del secuenciador en las conchas (motor v25) ---------------------------
# Una nota tine tenuemente las losetas de su celda: la superior con toda la
# luz, y se apaga hacia abajo en Luzconchasalcance losetas. Es una capa
# aditiva (luz, material constante): suma color sin tapar el de la
# generacion, se ve tambien en la cara en sombra y nunca oscurece. En
# reposo respira despacio: una loseta ocupada es mas clara pero quieta, asi
# que el reposo del SEQ1 (blanco) no se confunde con ella. La cicatriz manda.

LUZ_CONCHAS_K = 1.06        # la capa envuelve la loseta (que mide 1.04)
LUZ_CONCHAS_KH = 1.012      # y asoma por arriba, sin llegar a la luz de celda
RESPIRA_T = 2.4             # periodo del reposo (s)


def shell_lights(W, cfg, now):
    """Filas de la capa de luz sobre las losetas de las celdas que tocan
    los secuenciadores (solo esas: unas pocas filas por fotograma)."""
    if cfg['nivel'] < 8 or not cfg.get('luz_conchas', 1) or not cfg.get('luz_seq', 1):
        return []
    centros = seq_lights(W, cfg, now)
    if not centros:
        return []
    rows = []
    alc = max(1, int(cfg['luz_conchas_alcance']))
    maxs = max(1, int(cfg['max_shells']))
    pul, rep_ = cfg['luz_conchas_pulso'], cfg['luz_conchas_reposo']
    st = cfg['scar_time']
    respira = 0.70 + 0.30 * math.sin(2.0 * math.pi * now / RESPIRA_T)
    for c, lista in centros.items():
        col = column_radii(W, cfg, c)
        if not col:
            continue
        # dos secuenciadores en la celda: el mas encendido; si empatan, el ultimo
        s_, env = max(lista, key=lambda q: (q[1], W['hit_t'].get(q[0], -99.0)))
        I = rep_ * respira + max(0.0, pul - rep_) * env
        if I <= 1e-4:
            continue
        sc = seq_color(cfg, s_)
        n = normal_i(c)
        first = max(0, len(col) - maxs)
        for k, (s, r_in, r_out) in enumerate(reversed(col[first:])):
            if k >= alc:
                break
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None and now - t0 < st:
                continue                    # el cian de la cicatriz no se tapa
            w = I * (1.0 - k / float(alc))
            rows.append(_tile_row(c, n, r_in, r_out, (sc[0] * w, sc[1] * w, sc[2] * w),
                                  LUZ_CONCHAS_K, LUZ_CONCHAS_KH))
    return rows


# --- luz de celda (sin balizas) -----------------------------------------------
# Cada celda cuenta con luz lo que le esta pasando: una loseta opaca en el
# centro de la celda y la propia formacion (se hincha y se tine) con el
# color de quien acaba de tocarla.
#   - una nota de un SEQ: su color mientras suena (gate) y tenue hasta su
#     siguiente nota. Si estan los dos, el centro se parte: SEQ1 al oeste,
#     SEQ2 al este.
#   - un golpe de bateria (motor v21): igual, con el color del pad; plena en
#     la celda del golpe, mas tenue en su radio; se apaga en Vidabalizadrum.
#   - si coinciden, manda la luz mas intensa en ese instante.
# Con formacion, la loseta se ensancha hasta asomar alrededor de su base.
# Colores opacos, sin transparencia: no se mezclan.

COL_SEQ1 = (0.10, 0.90, 1.00)       # cian hasta la fase 8
COL_SEQ1_BLANCO = (0.95, 0.95, 0.92)  # blanco desde la fase 9 (cian = cicatriz)
COL_SEQ2 = (1.00, 0.62, 0.25)       # ambar
SEQ_DECAY = 0.25                    # el pulso de la nota cae en 1/4 de segundo
LUZ_LIFT = 0.02


def seq_color(cfg, s):
    if s == 2:
        return COL_SEQ2
    return COL_SEQ1_BLANCO if cfg['nivel'] >= 9 else COL_SEQ1


def light_level(cfg, h, now):
    """Intensidad 0-1 de la luz de un pad [t, peso] en este instante."""
    vida = max(0.05, cfg['vida_baliza_drum'])
    dt = now - h[0]
    if dt < 0 or dt >= vida:
        return 0.0
    x = dt / vida
    return h[1] * (1.0 - x) * (1.0 - x * 0.5)


def light_cell(W, cfg, c, pad, w, now):
    """El golpe ilumina la celda c (centro y formacion) con el color de su
    pad. Se guarda por pad: manda el mas intenso en cada instante. Un golpe
    mas flojo no apaga uno mas fuerte del mismo pad que siga encendido."""
    luz = W.setdefault('luz', {})
    pads = luz.setdefault(c, {})
    old = pads.get(int(pad))
    if old is not None and not es_impulso(cfg, pad) and light_level(cfg, old, now) > w + 1e-9:
        return
    pads[int(pad)] = [now, float(w)]


def _tile(n, e, t, base, dx, dz, sx, sz, h, col):
    p = _add(_add(_mul(n, base + LUZ_LIFT), e, dx), t, dz)
    return _row(p, n, sx, h, sz, col)


def seq_lights(W, cfg, now):
    """{celda: [(s, env), ...]} de los secuenciadores encendidos."""
    out = {}
    for s in ((1, 2) if cfg['nivel'] >= 5 else (1,)):
        last = W['last'].get(s)
        if not last or last.get('cell') is None or last['cell'] < 0 or last['cell'] >= N:
            continue
        if held(W, now, s=s):           # gate abierto: luz plena
            env = 1.0
        else:                           # se apaga desde que se solto la nota
            t0 = max(W['hit_t'].get(s, -99.0), W['seq_off'].get(s, -99.0))
            env = math.exp(-max(0.0, now - t0) / SEQ_DECAY)
        out.setdefault(last['cell'], []).append((s, env))
    return out


def nivel_pad(W, cfg, c, pd, h, now):
    """Intensidad 0-1 de la luz del pad pd ([t, peso]) en la celda c. La de un
    golpe de erosion se apaga en Vidabalizadrum; la de un impulso (fase 7
    v14) sigue la curva del pumping de la celda: plena en el pico, desde el
    mismo fotograma del golpe, y cae con el."""
    if es_impulso(cfg, pd):
        return h[1] * bomba_frac(W, c, now) if now >= h[0] - 1e-9 else 0.0
    return light_level(cfg, h, now)


def drum_light(W, cfg, c, now):
    """(intensidad, pad) de la luz de bateria mas fuerte en la celda c, o
    (0, None). La celda del golpe a plena luz, su radio mas tenue."""
    if cfg['nivel'] < 7 or not cfg['balizas_drum']:
        return 0.0, None
    pads = W.get('luz', {}).get(c)
    if not pads:
        return 0.0, None
    k = max(0.0, cfg['luz_drum'])
    best, bp = 0.0, None
    for pd, h in pads.items():
        I = min(1.0, nivel_pad(W, cfg, c, pd, h, now) * k)
        if I > best or (I == best and bp is not None and h[0] > pads[bp][0]):
            best, bp = I, pd
    return (best, bp) if best > 0.02 else (0.0, None)


def drum_color(cfg, pad):
    cols = cfg.get('colores_drum') or COLORES_DRUM
    return cols[int(pad) % len(cols)]


def cell_lights(W, cfg, now):
    """Losetas de luz del centro de las celdas. Secuenciadores y bateria se
    ven igual: la loseta del centro (y la formacion, ver build_instances)
    con el color de quien acaba de tocar la celda. Si coinciden, manda la
    luz mas intensa en ese instante (un golpe, por ser el ultimo, suele
    ganar a un secuenciador en reposo)."""
    rows = []
    centros = seq_lights(W, cfg, now) if cfg.get('luz_seq', 1) else {}
    luz = W.get('luz', {})
    for c in list(luz):
        pads = luz[c]
        for pd in [pd for pd in pads if nivel_pad(W, cfg, c, pd, pads[pd], now) <= 0.0]:
            del pads[pd]
        if not pads:
            del luz[c]
    for c in sorted(set(centros) | set(luz)):
        if c >= N:
            continue
        I, pad = drum_light(W, cfg, c, now)
        lista = sorted(centros.get(c, []))
        if pad is not None and lista and es_impulso(cfg, pad):
            # fase 7 v12: el impulso no tapa al secuenciador: el centro se parte
            fuentes = [(seq_color(cfg, s_), env) for s_, env in lista] + [(drum_color(cfg, pad), I)]
        elif pad is not None and I >= max([env for _, env in lista] or [0.0]):
            fuentes = [(drum_color(cfg, pad), I)]
        else:
            fuentes = [(seq_color(cfg, s_), env) for s_, env in lista]
        if not fuentes:
            continue
        n = normal_i(c)
        e, t = tangents(n)
        base = base_radius(W, cfg, c)
        cw, cl = _cell_sizes(base, c)
        if is_pole(c):
            cw, cl = cw * 1.25, cl * 1.25
        lado_x, lado_z = 0.34 * cw, 0.34 * cl
        if W['vh'][c] > 0.005 and W['own'][c]:           # asoma alrededor de la base
            sc = cfg['sat_size'] if W['par'][c] >= 0 else 1.0
            m_ = 0.52 * min(cw, cl) * sc
            lado_x, lado_z = max(lado_x, m_), max(lado_z, m_)
        partes = len(fuentes)
        for q, (col, env) in enumerate(fuentes):
            b = 0.7 + 0.3 * env                    # tenue en reposo, plena con la nota o el golpe
            col = (col[0] * b, col[1] * b, col[2] * b)
            g = 0.80 + 0.20 * env
            sx = lado_x * g / partes
            dx = (q - 0.5 * (partes - 1)) * sx
            rows.append(_tile(n, e, t, base, dx, 0.0, sx * 0.96, lado_z * g,
                              0.06 + 0.22 * env, col))
    return rows


def world_dir(v, angle_deg, tilt_deg, wobble_deg=0.0):
    """Direccion de la celda en el mundo, con el giro del planeta aplicado.
    Orden de rotacion de las geometrias del planeta: Ry Rx Rz
    (ry = giro, rx = balanceo del eje, rz = inclinacion)."""
    a, t, w = math.radians(angle_deg), math.radians(tilt_deg), math.radians(wobble_deg)
    x, y, z = v
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    y, z = y * math.cos(w) - z * math.sin(w), y * math.sin(w) + z * math.cos(w)
    x, y = x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)
    return (x, y, z)


def wobble_step(st, dt, on, paused, amp, period, fade=3.0):
    """Avanza el balanceo del eje. st = {'ph': fase 0-1, 'env': 0-1}.
    La fase se acumula (cambiar el periodo no hace saltar el planeta) y se
    congela con Pausa. Al encender o apagar, la amplitud entra o sale en
    'fade' segundos con curva suave. Devuelve los grados de rx."""
    dt = max(0.0, min(0.25, dt))
    period = max(5.0, period)
    if not paused:
        st['ph'] = (st.get('ph', 0.0) + dt / period) % 1.0
    env = st.get('env', 0.0) + (1.0 if on else -1.0) * dt / fade
    env = max(0.0, min(1.0, env))
    st['env'] = env
    s = env * env * (3 - 2 * env)
    return s * amp * math.sin(2 * math.pi * st['ph'])



# -----------------------------------------------------------------------------
# 1. NUCLEO - la piel (fase 11): los modelos del catalogo
# -----------------------------------------------------------------------------
# Cada modelo es una lista de piezas primitivas en su espacio local: +Y
# arriba (la normal de la celda), la base en y = 0 y el alto ~1. Una pieza
# es ('caja' o 'hexa', centro x y z, tamano x y z, giro x y z en grados,
# orden xyz). En TouchDesigner cada pieza es un Transform SOP sobre una caja
# o un prisma hexagonal (Tube SOP de 6 lados) unidad; el modelo, su Merge.
# Aqui solo hay datos: que modelo va en cada sitio lo decide el motor.
#
# El basalto sale de prismas hexagonales; la vegetacion (fase 11 v8) y la ciudad
# (fase 11 v10) tienen sus bibliotecas de ejemplares; aqui quedan los remates y
# las piezas de obra de la ciudad, las huellas y lo que ensenan los cortes.

def _rot_xyz(rx, ry, rz):
    """Matriz (por filas) de Rz Ry Rx: el orden xyz de TouchDesigner (primero
    X, luego Y, luego Z)."""
    a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
    ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    return ((cb * cc, sa * sb * cc - ca * sc, ca * sb * cc + sa * sc),
            (cb * sc, sa * sb * sc + ca * cc, ca * sb * sc - sa * cc),
            (-sb, sa * cb, ca * cb))


def _euler_xyz(X, Y, Z):
    """(rx, ry, rz) en grados, orden xyz, que llevan los ejes locales x, y, z
    a los vectores X, Y, Z (ortonormales, a derechas)."""
    sb = max(-1.0, min(1.0, -X[2]))
    b = math.asin(sb)
    if abs(math.cos(b)) > 1e-6:
        a = math.atan2(Y[2], Z[2])
        c = math.atan2(X[1], X[0])
    else:
        a = math.atan2(-Z[1], Y[1])
        c = 0.0
    return math.degrees(a), math.degrees(b), math.degrees(c)


def _aplicar(M, v):
    return (M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
            M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
            M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2])


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _girar_eje(v, eje, grados):
    """Gira v alrededor del eje unitario (Rodrigues)."""
    t = math.radians(grados)
    c, s = math.cos(t), math.sin(t)
    k = _dot(eje, v) * (1 - c)
    x = _cross(eje, v)
    return (v[0] * c + x[0] * s + eje[0] * k, v[1] * c + x[1] * s + eje[1] * k,
            v[2] * c + x[2] * s + eje[2] * k)


def _caja(cx, cy, cz, sx, sy, sz, rx=0.0, ry=0.0, rz=0.0):
    return ('caja', cx, cy, cz, sx, sy, sz, rx, ry, rz)


def _hexa(cx, cy, cz, d, h, rx=0.0, ry=0.0, rz=0.0):
    return ('hexa', cx, cy, cz, d, h, d, rx, ry, rz)


def _bola(cx, cy, cz, d, h=None, rx=0.0, ry=0.0, rz=0.0):
    """Bola (Sphere SOP de pocas caras) de diametro d y alto h."""
    return ('bola', cx, cy, cz, d, d if h is None else h, d, rx, ry, rz)


def _cono(cx, cy, cz, d, h, rx=0.0, ry=0.0, rz=0.0):
    """Cono de base d y alto h (la punta arriba)."""
    return ('cono', cx, cy, cz, d, h, d, rx, ry, rz)


def _losa(x0, x1, y0, y1, z0, z1, forma='caja'):
    """Pieza recta entre dos esquinas (sin giro)."""
    return (forma, (x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0,
            abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), 0.0, 0.0, 0.0)


def _tramo(a, b, w, forma='caja'):
    """Pieza de seccion w que va del punto a al b."""
    d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    l = math.sqrt(_dot(d, d)) or 1e-6
    rx, ry = orient(_mul(d, 1.0 / l))
    c = _mul(_add(a, b), 0.5)
    return (forma, c[0], c[1], c[2], w, l, w, rx, ry, 0.0)


def _esquinas(p):
    """Las 8 esquinas de una pieza (el prisma, como su caja)."""
    M = _rot_xyz(p[7], p[8], p[9])
    out = []
    for sx in (-0.5, 0.5):
        for sy in (-0.5, 0.5):
            for sz in (-0.5, 0.5):
                q = _aplicar(M, (sx * p[4], sy * p[5], sz * p[6]))
                out.append((p[1] + q[0], p[2] + q[1], p[3] + q[2]))
    return out


def _caja_modelo(prims):
    """(xmin, xmax, ymin, ymax, zmin, zmax) del modelo."""
    pts = [q for p in prims for q in _esquinas(p)]
    return (min(q[0] for q in pts), max(q[0] for q in pts), min(q[1] for q in pts),
            max(q[1] for q in pts), min(q[2] for q in pts), max(q[2] for q in pts))


def _escalar(prims, k, dy=0.0):
    return [(p[0], p[1] * k, p[2] * k + dy, p[3] * k, p[4] * k, p[5] * k, p[6] * k) + tuple(p[7:])
            for p in prims]


def _a_alto_uno(prims):
    """Escala uniforme para que el modelo vaya de y = 0 a y = 1."""
    b = _caja_modelo(prims)
    k = 1.0 / max(1e-6, b[3] - b[2])
    return _escalar(prims, k, -b[2] * k)


def _encajar(prims, ancho=1.0):
    """Escala uniforme para que quepa en alto 1 y en una planta de 'ancho'
    centrada (la base en y = 0)."""
    b = _caja_modelo(prims)
    k = min(1.0 / max(1e-6, b[3] - b[2]),
            0.5 * ancho / max(1e-6, abs(b[0]), abs(b[1]), abs(b[4]), abs(b[5])))
    return _escalar(prims, k, -b[2] * k)


# --- basalto: columnas hexagonales en panal ----------------------------------

PANAL = [(0.0, 0.0)] + [(math.cos(math.radians(60 * k + 30)), math.sin(math.radians(60 * k + 30)))
                        for k in range(6)]


def _columnas(alturas, d=0.26, sep=None, tapa=None):
    """Columnas de basalto en panal: la central y su anillo de 6. alturas[k]
    es la de la columna k (0 o menos: no hay). tapa: losa sobre las altas."""
    sep = d * 0.87 if sep is None else sep
    out = []
    for (x, z), h in zip(PANAL, alturas):
        if h > 0:
            out.append(_hexa(x * sep, h / 2.0, z * sep, d, h))
    if tapa:
        out.append(_hexa(0.0, tapa - 0.04, 0.0, d * 2.9, 0.08))
    return out


# --- ciudad: pilas de cajas ---------------------------------------------------

def _plantas(x, z, w, d, n, h=0.25, losa=0.035, y0=0.0, sobra=0.06):
    """Torre de n plantas: cuerpo y losa que sobresale en cada una."""
    out = []
    for k in range(int(n)):
        y = y0 + k * h
        out.append(_losa(x - w / 2, x + w / 2, y, y + h - losa, z - d / 2, z + d / 2))
        out.append(_losa(x - w / 2 - sobra / 2, x + w / 2 + sobra / 2, y + h - losa, y + h,
                         z - d / 2 - sobra / 2, z + d / 2 + sobra / 2))
    return out


def _modelos():
    M = {}
    # ------------------------------------------------------------- vegetacion
    # motor v52 (fase 11 v8): la vegetacion ya no tiene modelos de piezas (ni
    # conos, ni prismas, ni bolas): sale de la biblioteca de ejemplares (veg_<modelo>_<v>_<d>).
    # --------------------------------------------------------------- relieve
    M['rel_columna'] = _columnas([1.0], d=0.36)
    M['rel_columna2'] = _columnas([1.0, 0.7, 0, 0, 0.55], d=0.30)
    M['rel_columnas'] = _columnas([1.0, 0.85, 0.7, 0.55, 0.9, 0.62, 0.78], d=0.28)
    M['rel_mesetas'] = _columnas([1.0, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], d=0.30, tapa=0.72)
    M['rel_meseta'] = _columnas([1.0] * 7, d=0.32, tapa=1.0)
    M['rel_cumbre'] = (_columnas([1.0, 0.45, 0.45, 0.45, 0.45, 0.45, 0.45], d=0.34, sep=0.36)
                       + _columnas([0.72, 0.72, 0.72, 0, 0, 0, 0], d=0.22, sep=0.12)[1:])
    M['rel_prot1'] = _columnas([1.0, 0.8, 0.9, 0.7, 0.85, 0.75, 0.95], d=0.32, tapa=0.7)
    M['rel_prot2'] = (_columnas([0.7] * 7, d=0.36, sep=0.34, tapa=0.7)
                      + [_hexa(0.0, 0.85, 0.0, 0.34, 0.3)])
    M['rel_prot3'] = (_columnas([0.5] * 7, d=0.40, sep=0.40)
                      + _columnas([0.8, 0.8, 0.8, 0.8, 0, 0, 0], d=0.26, sep=0.16)
                      + [_hexa(0.0, 0.9, 0.0, 0.22, 0.2)])
    M['rel_puente'] = [_hexa(0.0, 0.5, z, 0.62, 1.0, 0.0, 30.0 * k) for k, z in enumerate((0.2, 0.55, 0.88))]
    # ---------------------------------- remates de la ciudad (fase 11 v10, motor v67)
    # La ciudad sale de la biblioteca de edificios (edi_<diseno>_<v>, Script SOP):
    # estos son sus remates y las piezas de obra, cluster y mutantes, instancias
    # 'ciu_' de cajas (Phong, color por instancia). Las pilas de cajas de la
    # informal y la planificada (inf_caseta ... pla_hib) se van.
    M['ciu_deposito'] = [_hexa(0.0, 0.62, 0.0, 0.9, 0.76), _losa(-0.4, -0.3, 0.0, 0.25, -0.4, -0.3),
                         _losa(0.3, 0.4, 0.0, 0.25, 0.3, 0.4), _losa(-0.4, -0.3, 0.0, 0.25, 0.3, 0.4),
                         _losa(0.3, 0.4, 0.0, 0.25, -0.4, -0.3)]
    M['ciu_antena'] = [_losa(-0.08, 0.08, 0.0, 1.0, -0.08, 0.08), _losa(-0.5, 0.5, 0.7, 0.74, -0.04, 0.04),
                       _losa(-0.35, 0.35, 0.86, 0.9, -0.04, 0.04), _caja(0.2, 0.55, 0.0, 0.5, 0.3, 0.06, 0.0, 0.0, 35.0)]
    M['ciu_maquinaria'] = [_losa(-0.5, 0.1, 0.0, 0.7, -0.4, 0.4), _losa(0.15, 0.5, 0.0, 1.0, -0.3, 0.2),
                           _hexa(0.3, 0.9, 0.3, 0.3, 0.2)]
    M['ciu_varillas'] = [_losa(x - 0.03, x + 0.03, 0.0, 1.0, z - 0.03, z + 0.03)
                         for x in (-0.45, 0.0, 0.45) for z in (-0.45, 0.45)]
    M['ciu_escalera'] = [_caja(0.0, 0.5, 0.0, 0.6, 1.12, 0.12, 40.0, 0.0, 0.0), _losa(-0.5, 0.5, 0.94, 1.0, -0.5, 0.5)]
    M['ciu_cable'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_toldo'] = [_caja(0.0, 0.5, 0.0, 1.0, 0.12, 1.0, 18.0, 0.0, 0.0)]
    M['ciu_chimenea'] = [_losa(-0.12, 0.12, 0.0, 1.0, -0.12, 0.12)]
    M['ciu_bidon'] = [_hexa(0.0, 0.5, 0.0, 0.9, 1.0)]
    M['ciu_mastil'] = [_losa(-0.06, 0.06, 0.0, 1.0, -0.06, 0.06), _losa(-0.5, 0.5, 0.55, 0.58, -0.03, 0.03),
                       _losa(-0.4, 0.4, 0.75, 0.78, -0.03, 0.03), _losa(-0.03, 0.03, 0.82, 0.85, -0.45, 0.45),
                       _losa(-0.3, 0.3, 0.93, 0.96, -0.03, 0.03)]
    M['ciu_vallacima'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, -0.46), _losa(-0.5, 0.5, 0.0, 1.0, 0.46, 0.5),
                          _losa(-0.5, -0.46, 0.0, 1.0, -0.46, 0.46), _losa(0.46, 0.5, 0.0, 1.0, -0.46, 0.46)]
    M['ciu_pretil'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, -0.44), _losa(-0.5, 0.5, 0.0, 1.0, 0.44, 0.5),
                       _losa(-0.5, -0.44, 0.0, 1.0, -0.44, 0.44), _losa(0.44, 0.5, 0.0, 1.0, -0.44, 0.44)]
    M['ciu_pergola'] = ([_losa(x - 0.04, x + 0.04, 0.0, 0.9, z - 0.04, z + 0.04) for x in (-0.45, 0.45)
                         for z in (-0.45, 0.45)]
                        + [_losa(-0.5, 0.5, 0.9, 1.0, z - 0.03, z + 0.03) for z in (-0.4, -0.2, 0.0, 0.2, 0.4)])
    M['ciu_sierra'] = [_caja(x, 0.5, 0.0, 0.2, 1.0, 1.0, 0.0, 0.0, 28.0) for x in (-0.38, -0.13, 0.12, 0.37)]
    M['ciu_aguja'] = [_losa(-0.5, 0.5, 0.0, 0.12, -0.5, 0.5), _losa(-0.25, 0.25, 0.12, 0.3, -0.25, 0.25),
                      _losa(-0.08, 0.08, 0.3, 1.0, -0.08, 0.08)]
    M['ciu_dosaguas'] = [_caja(-0.25, 0.5, 0.0, 0.56, 0.08, 1.0, 0.0, 0.0, 34.0),
                         _caja(0.25, 0.5, 0.0, 0.56, 0.08, 1.0, 0.0, 0.0, -34.0)]
    M['ciu_unagua'] = [_caja(0.0, 0.5, 0.0, 1.0, 0.08, 1.0, 0.0, 0.0, 14.0)]
    M['ciu_balcon'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_pasarela'] = [_losa(-0.5, 0.5, 0.0, 0.25, -0.5, 0.5), _losa(-0.5, -0.4, 0.25, 1.0, -0.5, 0.5),
                         _losa(0.4, 0.5, 0.25, 1.0, -0.5, 0.5)]
    M['ciu_corredor'] = [_losa(-0.5, 0.5, 0.0, 0.12, -0.5, 0.5), _losa(-0.5, -0.42, 0.12, 0.88, -0.5, 0.5),
                         _losa(0.42, 0.5, 0.12, 0.88, -0.5, 0.5), _losa(-0.5, 0.5, 0.88, 1.0, -0.5, 0.5)]
    M['ciu_bucle'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_losa'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    # Ville Spatiale: el modulo del marco (cuatro postes y dos anillos de vigas) y el pilar
    M['ciu_marco'] = ([_losa(x - 0.03, x + 0.03, 0.0, 1.0, z - 0.03, z + 0.03) for x in (-0.47, 0.47)
                       for z in (-0.47, 0.47)]
                      + [_losa(-0.5, 0.5, y, y + 0.06, z - 0.03, z + 0.03) for y in (0.0, 0.94) for z in (-0.47, 0.47)]
                      + [_losa(x - 0.03, x + 0.03, y, y + 0.06, -0.5, 0.5) for y in (0.0, 0.94) for x in (-0.47, 0.47)])
    M['ciu_pilar'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_nucleo'] = [_losa(-0.5, 0.5, 0.0, 0.9, -0.5, 0.5), _losa(-0.56, 0.56, 0.86, 1.0, -0.56, 0.56)]
    M['ciu_tierra'] = [_cono(0.0, 0.0, 0.0, 1.0, 1.0)]
    # ------------------------- la industria (fase 11 v11, motor v68): remates y obra
    M['ciu_terril'] = [_cono(0.0, 0.0, 0.0, 1.0, 1.0), _cono(0.22, 0.0, 0.1, 0.6, 0.7)]
    M['ciu_vagoneta'] = [_losa(-0.5, 0.5, 0.3, 1.0, -0.4, 0.4), _hexa(-0.3, 0.15, 0.0, 0.3, 0.3, 90.0, 0.0, 0.0),
                         _hexa(0.3, 0.15, 0.0, 0.3, 0.3, 90.0, 0.0, 0.0)]
    M['ciu_railes'] = [_losa(-0.5, 0.5, 0.0, 0.4, -0.5, 0.5), _losa(-0.35, -0.25, 0.4, 1.0, -0.5, 0.5),
                       _losa(0.25, 0.35, 0.4, 1.0, -0.5, 0.5)]
    # la polea (gira) y el balancin (cabecea): partes moviles, el motor les da la fase
    M['ciu_polea'] = [_losa(-0.08, 0.08, 0.0, 1.0, -0.06, 0.06), _losa(-0.08, 0.08, 0.44, 0.56, -0.5, 0.5),
                      _caja(0.0, 0.5, 0.0, 0.16, 0.1, 0.96, 45.0, 0.0, 0.0),
                      _caja(0.0, 0.5, 0.0, 0.16, 0.1, 0.96, -45.0, 0.0, 0.0)]
    M['ciu_balancin'] = [_losa(-0.5, 0.35, 0.4, 0.6, -0.12, 0.12), _losa(0.3, 0.5, 0.0, 1.0, -0.14, 0.14),
                         _losa(-0.5, -0.36, 0.0, 0.4, -0.1, 0.1)]
    M['ciu_tuberia'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_cinta'] = [_losa(-0.5, 0.5, 0.6, 1.0, -0.5, 0.5), _losa(-0.1, 0.1, 0.0, 0.6, -0.1, 0.1)]
    M['ciu_troncos'] = [_hexa(x, 0.2 + 0.35 * f, z, 0.32, 1.0, 90.0, 0.0, 0.0)
                        for f, (x, z) in enumerate(((-0.33, 0.0), (0.0, 0.0), (0.33, 0.0), (-0.16, 0.0), (0.16, 0.0)))]
    M['ciu_troncos'] = _a_alto_uno(M['ciu_troncos'])
    M['ciu_tablones'] = [_losa(-0.5, 0.5, y, y + 0.18, z - 0.08, z + 0.08) for y in (0.0, 0.4, 0.8)
                         for z in (-0.3, 0.0, 0.3)]
    M['ciu_portico'] = [_losa(-0.5, -0.42, 0.0, 1.0, -0.5, 0.5), _losa(0.42, 0.5, 0.0, 1.0, -0.5, 0.5),
                        _losa(-0.5, 0.5, 0.88, 1.0, -0.12, 0.12)]
    M['ciu_ciclon'] = [_cono(0.0, 0.0, 0.0, 1.0, 1.0, 180.0, 0.0, 0.0)]
    M['ciu_ciclon'] = _a_alto_uno(M['ciu_ciclon'])
    M['ciu_subestacion'] = ([_losa(x - 0.04, x + 0.04, 0.0, 1.0, z - 0.04, z + 0.04) for x in (-0.4, 0.0, 0.4)
                             for z in (-0.4, 0.4)] + [_losa(-0.5, 0.5, 0.9, 1.0, z - 0.03, z + 0.03) for z in (-0.4, 0.4)]
                            + [_losa(-0.2, 0.2, 0.0, 0.4, -0.2, 0.2)])
    M['ciu_rotopala'] = [_hexa(-0.3, 0.6, 0.0, 0.8, 0.12, 90.0, 0.0, 0.0), _losa(-0.3, 0.5, 0.45, 0.55, -0.06, 0.06),
                         _losa(0.2, 0.5, 0.0, 0.3, -0.3, 0.3)]
    # la corta: un anillo de banco (octogono hueco) y el agua acida del fondo
    M['ciu_anillo'] = [_caja(0.43 * math.cos(math.radians(45 * k)), 0.5, 0.43 * math.sin(math.radians(45 * k)),
                             0.16, 1.0, 0.42, 0.0, -45.0 * k, 0.0) for k in range(8)]
    M['ciu_agua'] = [_hexa(0.0, 0.5, 0.0, 1.0, 1.0)]
    # la planta integrada: un modulo de bastidor con tuberias de colores
    M['ciu_bastidor'] = ([_losa(x - 0.03, x + 0.03, 0.0, 1.0, z - 0.03, z + 0.03) for x in (-0.47, 0.47)
                          for z in (-0.47, 0.47)]
                         + [_losa(-0.5, 0.5, 0.92, 1.0, -0.5, 0.5)]
                         + [_losa(-0.5, 0.5, 0.55, 0.65, z - 0.05, z + 0.05) for z in (-0.2, 0.15)])
    # obra: el encofrado (deslizante o trepante) y la columna tumbada que iza la grua
    M['ciu_encofrado'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, -0.4), _losa(-0.5, 0.5, 0.0, 1.0, 0.4, 0.5),
                          _losa(-0.5, -0.4, 0.0, 1.0, -0.4, 0.4), _losa(0.4, 0.5, 0.0, 1.0, -0.4, 0.4)]
    M['ciu_columna'] = [_hexa(0.0, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 90.0)]
    M['ciu_columna'] = _a_alto_uno(M['ciu_columna'])
    # el tejido de la industria (fase 13): torre de alta tension, poste y viaducto de celosia
    M['ciu_torre'] = [_caja(-0.25, 0.5, 0.0, 0.06, 1.0, 0.06, 0.0, 0.0, -12.0),
                      _caja(0.25, 0.5, 0.0, 0.06, 1.0, 0.06, 0.0, 0.0, 12.0),
                      _losa(-0.5, 0.5, 0.78, 0.82, -0.03, 0.03), _losa(-0.35, 0.35, 0.92, 0.95, -0.03, 0.03)]
    M['ciu_poste'] = [_losa(-0.08, 0.08, 0.0, 1.0, -0.08, 0.08), _losa(-0.5, 0.5, 0.86, 0.92, -0.05, 0.05)]
    M['ciu_viaducto'] = ([_losa(-0.5, 0.5, 0.86, 1.0, -0.5, 0.5)] + [_losa(-0.42, -0.34, 0.0, 0.86, z - 0.04, z + 0.04)
                                                                    for z in (-0.4, 0.0, 0.4)]
                         + [_losa(0.34, 0.42, 0.0, 0.86, z - 0.04, z + 0.04) for z in (-0.4, 0.0, 0.4)])
    # huellas de la industria (fase 14): crater de hundimiento, ruina de nave y hollin
    M['ind_crater'] = [_caja(0.43 * math.cos(math.radians(60 * k)), 0.3, 0.43 * math.sin(math.radians(60 * k)),
                             0.2, 0.6, 0.5, 0.0, -60.0 * k, 20.0) for k in range(6)] + [_hexa(0.0, 0.05, 0.0, 0.6, 0.1)]
    M['ind_ruina'] = ([_losa(x - 0.03, x + 0.03, 0.0, 1.0, z - 0.03, z + 0.03) for x in (-0.4, 0.0, 0.4)
                       for z in (-0.3, 0.3)] + [_losa(-0.45, 0.45, 0.0, 0.35, -0.36, -0.3),
                                                _caja(0.1, 0.8, 0.0, 0.6, 0.04, 0.05, 0.0, 0.0, 18.0)])
    M['ind_hollin'] = [_hexa(0.0, 0.03, 0.0, 1.0, 0.06), _hexa(0.15, 0.3, -0.1, 0.12, 0.6),
                       _caja(-0.2, 0.15, 0.2, 0.5, 0.06, 0.06, 0.0, 30.0, 0.0)]
    # lo que ensenan los cortes de la industria (fase 16): galeria entibada, vagoneta fosil y pozo
    M['ind_galeria'] = [_losa(-0.5, 0.5, 0.0, 0.1, -0.5, 0.5), _losa(-0.5, -0.38, 0.1, 0.8, -0.5, 0.5),
                        _losa(0.38, 0.5, 0.1, 0.8, -0.5, 0.5), _losa(-0.5, 0.5, 0.8, 0.92, -0.5, 0.5),
                        _losa(-0.3, -0.26, 0.1, 0.8, -0.5, 0.5), _losa(0.26, 0.3, 0.1, 0.8, -0.5, 0.5)]
    M['ind_vagoneta'] = [_caja(0.0, 0.4, 0.0, 0.8, 0.4, 0.5, 0.0, 0.0, 14.0), _hexa(-0.25, 0.1, 0.0, 0.2, 0.2, 90.0),
                         _hexa(0.25, 0.1, 0.0, 0.2, 0.2, 90.0)]
    M['ind_pozo'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, -0.38), _losa(-0.5, 0.5, 0.0, 1.0, 0.38, 0.5),
                     _losa(-0.5, -0.38, 0.0, 1.0, -0.38, 0.38), _losa(0.38, 0.5, 0.0, 1.0, -0.38, 0.38),
                     _losa(-0.05, 0.05, 0.0, 1.0, -0.05, 0.05)]
    # ------------------------------------------------------------ obras de la ciudad
    M['ciu_valla'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, -0.47), _losa(-0.5, 0.5, 0.0, 1.0, 0.47, 0.5),
                      _losa(-0.5, -0.47, 0.0, 1.0, -0.47, 0.47), _losa(0.47, 0.5, 0.0, 1.0, -0.47, 0.47)]
    M['ciu_foso'] = [_losa(-0.5, 0.5, 0.0, 1.0, -0.5, 0.5)]
    M['ciu_andamio'] = ([_losa(x - 0.02, x + 0.02, 0.0, 1.0, z - 0.02, z + 0.02)
                         for x in (-0.48, 0.48) for z in (-0.48, 0.48)]
                        + [_losa(-0.5, 0.5, y, y + 0.03, z - 0.02, z + 0.02)
                           for y in (0.33, 0.66, 0.97) for z in (-0.48, 0.48)])
    M['ciu_grua'] = [_losa(-0.04, 0.04, 0.0, 1.0, -0.04, 0.04), _losa(-0.25, 0.85, 0.94, 0.98, -0.03, 0.03),
                     _losa(-0.25, -0.14, 0.86, 0.94, -0.05, 0.05), _losa(0.6, 0.61, 0.72, 0.94, -0.005, 0.005)]
    # ------------------------------------------- huellas de las catastrofes (fase 14)
    # claro de ceniza: el suelo quemado, tocones carbonizados y un tronco caido
    M['veg_claro'] = [_hexa(-0.16, 0.03, 0.1, 0.62, 0.06), _hexa(0.18, 0.04, -0.12, 0.56, 0.08, 0.0, 30.0, 0.0),
                      _hexa(0.1, 0.025, 0.24, 0.4, 0.05, 0.0, 12.0, 0.0),
                      _caja(-0.22, 0.47, 0.12, 0.08, 0.9, 0.08, 6.0, 0.0, -8.0),
                      _caja(0.24, 0.32, -0.18, 0.07, 0.6, 0.07, -10.0, 0.0, 5.0),
                      _caja(0.04, 0.23, 0.28, 0.07, 0.42, 0.07),
                      _caja(-0.04, 0.13, -0.26, 0.62, 0.08, 0.09, 0.0, 30.0, 0.0)]
    # pedregal: trozos de columna y bloques sueltos, uno tumbado
    M['rel_pedregal'] = [_hexa(-0.22, 0.2, -0.12, 0.34, 0.4), _hexa(0.2, 0.15, 0.2, 0.3, 0.3, 0.0, 30.0, 0.0),
                         _caja(0.26, 0.12, -0.22, 0.24, 0.24, 0.2, 0.0, 25.0, 0.0),
                         _caja(-0.16, 0.1, 0.26, 0.2, 0.2, 0.26, 0.0, -20.0, 0.0),
                         _hexa(0.02, 0.5, 0.02, 0.28, 1.0),
                         _hexa(-0.12, 0.12, -0.24, 0.22, 0.46, 90.0, 0.0, 0.0),
                         _caja(0.38, 0.08, 0.06, 0.16, 0.16, 0.16, 0.0, 40.0, 0.0)]
    # escombros: losas inclinadas, un bloque roto, una viga y un trozo de muro
    M['inf_escombros'] = [_losa(-0.42, 0.42, 0.0, 0.16, -0.38, 0.38),
                          _caja(-0.15, 0.36, 0.05, 0.5, 0.06, 0.4, 25.0, 30.0, 0.0),
                          _caja(0.2, 0.3, -0.1, 0.4, 0.06, 0.35, -20.0, -15.0, 10.0),
                          _caja(0.05, 0.5, 0.15, 0.3, 0.25, 0.25, 15.0, 40.0, 20.0),
                          _caja(-0.25, 0.25, -0.25, 0.2, 0.4, 0.12, 0.0, 20.0, 30.0),
                          _caja(0.3, 0.5, 0.25, 0.25, 1.0, 0.06, 0.0, -30.0, 0.0)]
    # ------------------------------------- lo que ensenan los cortes (fase 16)
    # En la pared: X a lo largo de la pared, Y hacia arriba, Z hacia fuera.
    # tronco fosil aplastado en horizontal, con su placa de raices y ramas rotas
    M['fos_tronco'] = [_caja(0.04, 0.5, 0.0, 0.84, 0.36, 0.5), _caja(-0.42, 0.5, 0.0, 0.14, 0.86, 0.56),
                       _caja(0.16, 0.7, 0.0, 0.34, 0.12, 0.36, 0.0, 0.0, 26.0),
                       _caja(0.30, 0.32, 0.0, 0.28, 0.10, 0.36, 0.0, 0.0, -22.0),
                       _caja(0.44, 0.5, 0.0, 0.12, 0.22, 0.4)]
    # dos troncos cruzados, ya casi laminas
    M['fos_tronco2'] = [_caja(-0.04, 0.32, 0.0, 0.88, 0.22, 0.46, 0.0, 0.0, 7.0),
                        _caja(0.06, 0.66, 0.0, 0.78, 0.2, 0.42, 0.0, 0.0, -9.0),
                        _caja(-0.4, 0.5, 0.0, 0.12, 0.6, 0.5)]
    # disyuncion columnar: columnas de basalto de pie, una junto a otra
    M['fos_basalto'] = [_hexa(-0.4 + 0.2 * k, 0.5, 0.0, 0.21, (1.0, 0.86, 0.94, 0.8, 0.92)[k])
                        for k in range(5)]
    # cimientos corridos de la ciudad informal: zapata, muros cortados y cascotes
    M['arq_cimientos'] = [_losa(-0.5, 0.5, 0.0, 0.16, -0.42, 0.42),
                          _losa(-0.46, -0.32, 0.16, 0.74, -0.24, 0.24),
                          _losa(-0.06, 0.08, 0.16, 0.6, -0.24, 0.24),
                          _losa(0.32, 0.46, 0.16, 0.84, -0.24, 0.24),
                          _caja(0.16, 0.82, 0.0, 0.26, 0.1, 0.28, 0.0, 30.0, 16.0),
                          _caja(-0.2, 0.88, 0.0, 0.28, 0.1, 0.32, 0.0, -20.0, -12.0)]
    # sotano de la ciudad planificada, abierto hacia el corte: solera, forjado,
    # muros y pilares
    M['arq_sotano'] = [_losa(-0.5, 0.5, 0.0, 0.08, -0.5, 0.5), _losa(-0.5, 0.5, 0.92, 1.0, -0.5, 0.5),
                       _losa(-0.5, 0.5, 0.08, 0.92, -0.5, -0.4), _losa(-0.5, -0.42, 0.08, 0.92, -0.4, 0.5),
                       _losa(0.42, 0.5, 0.08, 0.92, -0.4, 0.5), _losa(-0.2, -0.12, 0.08, 0.92, 0.04, 0.12),
                       _losa(0.12, 0.2, 0.08, 0.92, 0.04, 0.12)]
    # pilotes bajo los pilotis (fase 11 v10: los cortes ensenan los cimientos de cada tipo)
    M['arq_pilotes'] = ([_losa(-0.5, 0.5, 0.84, 1.0, -0.42, 0.42)]
                        + [_losa(x - 0.05, x + 0.05, 0.0, 0.84, -0.05, 0.05) for x in (-0.38, -0.13, 0.13, 0.38)])
    # tramo de calle en seccion: aceras, firme, zahorra y el colector
    M['arq_calle'] = [_losa(-0.5, 0.5, 0.78, 0.9, -0.5, 0.5), _losa(-0.5, -0.36, 0.9, 1.0, -0.5, 0.5),
                      _losa(0.36, 0.5, 0.9, 1.0, -0.5, 0.5), _losa(-0.46, 0.46, 0.62, 0.78, -0.5, 0.5),
                      _hexa(0.0, 0.28, 0.0, 0.42, 1.0, 90.0, 0.0, 0.0)]
    # galeria de metro a cielo abierto, de la celda a la vecina (Z de 0 a 1):
    # solera, hastiales, boveda de dos faldones y carriles
    M['arq_galeria'] = [_losa(-0.5, 0.5, 0.0, 0.08, 0.0, 1.0), _losa(-0.5, -0.4, 0.08, 0.6, 0.0, 1.0),
                        _losa(0.4, 0.5, 0.08, 0.6, 0.0, 1.0),
                        _caja(-0.25, 0.76, 0.5, 0.54, 0.08, 1.0, 0.0, 0.0, 35.0),
                        _caja(0.25, 0.76, 0.5, 0.54, 0.08, 1.0, 0.0, 0.0, -35.0),
                        _losa(-0.2, -0.16, 0.08, 0.13, 0.0, 1.0), _losa(0.16, 0.2, 0.08, 0.13, 0.0, 1.0)]
    for k, prims in M.items():          # ninguno pasa de alto 1 ni baja de 0
        b = _caja_modelo(prims)
        if b[2] < -1e-6 or b[3] > 1.0 + 1e-6:
            M[k] = _a_alto_uno(prims)
    return M


MODELOS = _modelos()


# Como se apoya cada modelo en su celda:
#   ('esbelto', k)  proporciones propias: escala uniforme con la altura de la
#                   formacion, sin pasar de k veces el ancho de la celda
#   ('celda', k)    planta de k veces la celda (este-oeste y norte-sur);
#                   el alto, el de la formacion
PIE = {}
for _m in MODELOS:
    PIE[_m] = ('esbelto', 0.9)
for _m in ('rel_mesetas', 'rel_meseta', 'rel_cumbre', 'rel_prot1', 'rel_prot2',
           'rel_prot3', 'ciu_valla', 'veg_claro', 'rel_pedregal', 'inf_escombros'):
    PIE[_m] = ('celda', 0.85)
PIE.update(ciu_foso=('celda', 0.75), ciu_andamio=('celda', 0.9))


def _ancho_natural(m):
    b = _caja_modelo(MODELOS[m])
    return max(1e-3, b[1] - b[0], b[5] - b[4])


ANCHO = dict((m, _ancho_natural(m)) for m in MODELOS)


# --- la biblioteca de ejemplares (fase 11 v8, motor v52) ------------------------
# La vegetacion ya no son piezas sueltas (conos, prismas, bolas): cada planta es
# un EJEMPLAR precalculado, inspirado en los modelos arquitectonicos de Halle y
# Oldeman, con dos partes:
#   ramas   tubos de 4 o 5 lados; el grosor sigue la regla de Leonardo
#           (r_padre^2 = suma de r_hijo^2), desde las ramillas hacia el tronco
#   hojas   puntos de hoja: posicion, normal, eje, tamano, tipo, profundidad en
#           la copa (0 borde, 1 dentro) y nivel de rama (para el viento)
# La copa es la suma de sus racimos (de tamanos 0,6 a 1,4); ninguna pieza es una
# primitiva. Se calcula una vez por (modelo, variante, derivacion) y se guarda;
# en TouchDesigner cada ejemplar es una malla (Script SOP, una vez) que se
# instancia entera, con su version lejana de tarjetas de racimo (_lod).
# Ejes del ejemplar: la base en el origen, Y arriba, alto 1.

# Motor v97: ocho arboles mas (cipres, abedul, araucaria, olivo, baobab, mangle, bambu y
# cardon) y dos matorrales (agave y junco). PLANTAS conserva el orden de la v52 y anade
# los nuevos al final: la semilla de cada ejemplar sale de su indice, y los de antes no cambian.
ARBOLES_V52 = ['conifera', 'pagoda', 'parasol', 'drago', 'frondosa', 'palmera', 'sauce']
MATORRALES_V52 = ['retama', 'brezo', 'helecho', 'graminea', 'enebro', 'palmito']
ARBOLES_V97 = ['cipres', 'abedul', 'araucaria', 'olivo', 'baobab', 'mangle', 'bambu', 'cardon']
MATORRALES_V97 = ['agave', 'junco']
ARBOLES = ARBOLES_V52 + ARBOLES_V97
MATORRALES = MATORRALES_V52 + MATORRALES_V97
PLANTAS = ARBOLES_V52 + MATORRALES_V52 + ARBOLES_V97 + MATORRALES_V97
SIN_FUSTE = ('mangle', 'cardon')     # no se leen por el fuste: raices zancudas y columna entera
HOJA_DE = dict(conifera='aguja', pagoda='ancha', parasol='ancha', drago='espada', frondosa='ancha',
               palmera='fronda', sauce='lanceolada', retama='lanceolada', brezo='menuda', helecho='fronda',
               graminea='lamina', enebro='aguja', palmito='abanico',
               cipres='aguja', abedul='menuda', araucaria='aguja', olivo='lanceolada', baobab='ancha',
               mangle='ancha', bambu='lanceolada', cardon='menuda', agave='espada', junco='lamina')
TIPOS_HOJA = ['aguja', 'ancha', 'lanceolada', 'espada', 'fronda', 'abanico', 'lamina', 'menuda']
# Motor v97: flores y frutos. Son hojas de un tipo aparte (uv.x = 4 + color / 10 en la
# malla): el shader les da su color, sin tocar el verde de la instancia.
FLORES = dict(flor_blanca=0, flor_rosa=1, flor_amarilla=2, flor_roja=3, flor_violeta=4, flor_naranja=5)
# La corteza de cada modelo (uv.y de los tubos; el shader elige): 0 parda oscura, 0,25 gris,
# 0,5 blanca (abedul), 0,75 verde (canas y cactus), 1 rojiza
CORTEZA = dict(abedul=0.5, olivo=0.25, baobab=0.25, palmera=0.25, drago=0.25, bambu=0.75, cardon=0.75,
               araucaria=1.0, mangle=1.0, sauce=0.25)
# El verde de cada planta (motor v97): el albedo de la instancia es el piso de su altura
# acercado a este tono (TONO_K). Todos con el verde por delante del rojo y del azul.
TONO_PLANTA = dict(
    conifera=(0.07, 0.24, 0.17), pagoda=(0.16, 0.38, 0.14), parasol=(0.25, 0.41, 0.12), drago=(0.20, 0.37, 0.25),
    frondosa=(0.13, 0.36, 0.10), palmera=(0.22, 0.45, 0.14), sauce=(0.36, 0.52, 0.20), retama=(0.36, 0.45, 0.14),
    brezo=(0.27, 0.35, 0.21), helecho=(0.16, 0.45, 0.14), graminea=(0.50, 0.57, 0.24), enebro=(0.10, 0.28, 0.20),
    palmito=(0.24, 0.43, 0.16), cipres=(0.06, 0.21, 0.12), abedul=(0.43, 0.59, 0.18),
    araucaria=(0.08, 0.27, 0.15), olivo=(0.38, 0.47, 0.35), baobab=(0.31, 0.43, 0.16), mangle=(0.10, 0.34, 0.16),
    bambu=(0.41, 0.57, 0.16), cardon=(0.25, 0.43, 0.27), agave=(0.30, 0.47, 0.39), junco=(0.43, 0.51, 0.20))
TONO_K = 0.6
DERIVACIONES = 3             # el arbol: 1 brinzal, 2 joven, 3 adulto (derivacion completa)
DERIVACION_JOVEN = 2
ANGULO_PLANTA = dict(conifera=84.0, pagoda=88.0, parasol=45.0, drago=34.0, frondosa=36.0, palmera=12.0,
                     sauce=38.0, retama=22.0, brezo=40.0, helecho=55.0, graminea=50.0, enebro=80.0,
                     palmito=45.0, cipres=20.0, abedul=48.0, araucaria=86.0, olivo=58.0, baobab=62.0,
                     mangle=60.0, bambu=6.0, cardon=90.0, agave=48.0,
                     junco=8.0)      # angulo de rama con el eje del padre (grados), antes de Varangulo
ANGULO_AUREO = 137.5         # las hojas, a lo largo de la ramilla con el angulo aureo
R_PUNTA = 0.0035             # radio de una ramilla (alto 1); Leonardo da el resto
SUBE = (0.0, 1.0, 0.0)


class _Planta(object):
    """Esqueleto y hojas de un ejemplar mientras se construye."""

    def __init__(self, modelo, var, deriv, cfg):
        import random
        self.modelo, self.deriv, self.var = modelo, deriv, int(var)
        self.rng = random.Random(7919 * (PLANTAS.index(modelo) + 1) + 104729 * var + 17)
        self.rng2 = random.Random(15485863 * (PLANTAS.index(modelo) + 1) + 32452843 * var + 5)   # las flores
        self.r_punta = R_PUNTA
        self.var_ang = max(0.0, float(cfg.get('var_angulo', 12.0)))
        self.cuant = bool(cfg.get('cuantizar30', 0))
        self.dens = max(1, int(cfg.get('densidad_hoja', 6)))
        self.seg, self.hojas, self.racimos = [], [], []

    def u(self, a=0.0, b=1.0):
        return a + (b - a) * self.rng.random()

    def ang(self, a):
        """El angulo del modelo +- Varangulo (o cuantizado a 30, para comparar)."""
        a = a + self.u(-self.var_ang, self.var_ang)
        return 30.0 * round(a / 30.0) if self.cuant else a

    def tramo(self, a, b, nivel, padre):
        self.seg.append(dict(a=a, b=b, nivel=nivel, hijos=[], padre=padre, r=self.r_punta))
        k = len(self.seg) - 1
        if padre is not None:
            self.seg[padre]['hijos'].append(k)
        return k

    def eje(self, p, d, largo, n, nivel, padre, tropismo=0.0, curva=None):
        """Un eje de n tramos desde p hacia d: tropismo > 0, la punta sube; < 0,
        cuelga. curva: un vector que lo dobla poco a poco. Devuelve (tramos,
        puntos, direccion final)."""
        tr, pts = [], [p]
        for _ in range(int(n)):
            d = _norm(_add(d, SUBE, tropismo))
            if curva is not None:
                d = _norm(_add(d, curva))
            q = _add(p, d, largo / n)
            padre = self.tramo(p, q, nivel, padre)
            tr.append(padre)
            pts.append(q)
            p = q
        return tr, pts, d

    def hijo(self, d, angulo, rumbo):
        """Direccion que se abre 'angulo' grados de d, girada 'rumbo' alrededor de d."""
        ref = SUBE if abs(_dot(d, SUBE)) < 0.95 else (1.0, 0.0, 0.0)
        lado = _norm(_cross(d, ref))
        return _norm(_girar_eje(_girar_eje(d, lado, angulo), d, rumbo))

    def racimo(self, p, d, tam, nivel, padre, tipo=None, n=None, plano=False, abre=55.0, roseta=False):
        """Un racimo: una ramilla de largo 'tam' desde p hacia d con sus hojas
        repartidas con el angulo aureo. Su tamano varia 0,6-1,4; 'plano': las
        hojas miran arriba (platos y techos). 'roseta': todas desde la punta."""
        f = self.u(0.6, 1.4)
        tam *= f
        tipo = tipo or HOJA_DE[self.modelo]
        n = max(self.dens, int(round((n or self.dens) * f)))
        q = _add(p, d, tam)
        k = self.tramo(p, q, nivel + 1, padre)
        self.racimos.append((q, tam, d, plano))
        g0 = self.u(0.0, 360.0)
        ref = SUBE if abs(_dot(d, SUBE)) < 0.95 else (1.0, 0.0, 0.0)
        lado0 = _norm(_cross(d, ref))
        for j in range(n):
            t = 1.0 if roseta else 0.25 + 0.75 * (j + 1) / float(n)
            pos = _add(p, d, tam * t)
            lado = _girar_eje(lado0, d, g0 + ANGULO_AUREO * j)
            if plano:
                ax = _norm(_add(_mul(lado, 1.0), d, 0.35))
                ax = _norm((ax[0], 0.08 * ax[1], ax[2]))
                nrm = SUBE
            else:
                e = math.radians(abre + self.u(-10.0, 10.0))
                ax = _norm(_add(_mul(d, math.cos(e)), lado, math.sin(e)))
                nrm = _norm(_cross(ax, _cross(SUBE, ax))) if abs(_dot(ax, SUBE)) < 0.98 else _norm(lado)
                if nrm[1] < 0:
                    nrm = _mul(nrm, -1.0)
            self.hojas.append([pos, nrm, ax, tam * self.u(0.75, 1.15) * HOJA_K[tipo], tipo, 0.0, nivel + 1])
        return k

    def flor(self, p, d, tam, tipo, n, nivel):
        """Motor v97: n flores (o frutos) del color 'tipo' (FLORES) alrededor de p,
        abiertas en torno a d. Con su propio azar: no mueven el resto del ejemplar."""
        r2 = self.rng2
        ref = SUBE if abs(_dot(d, SUBE)) < 0.95 else (1.0, 0.0, 0.0)
        lado0 = _norm(_cross(d, ref))
        g0 = 360.0 * r2.random()
        for j in range(int(n)):
            lado = _girar_eje(lado0, d, g0 + ANGULO_AUREO * j)
            e = math.radians(62.0 + r2.uniform(-18.0, 18.0))
            ax = _norm(_add(_mul(d, math.cos(e)), lado, math.sin(e)))
            nrm = _norm(_cross(ax, _cross(SUBE, ax))) if abs(_dot(ax, SUBE)) < 0.98 else _norm(lado)
            if nrm[1] < 0:
                nrm = _mul(nrm, -1.0)
            self.hojas.append([_add(p, d, 0.3 * tam * r2.random()), nrm, ax, tam * r2.uniform(0.8, 1.2), tipo,
                               0.0, nivel])

    def cerrar(self):
        """Leonardo, alto 1 y la profundidad de cada hoja en la copa."""
        for s in reversed(self.seg):            # los hijos siempre van despues del padre
            if s['hijos']:
                s['r'] = math.sqrt(sum(self.seg[h]['r'] ** 2 for h in s['hijos']))
        pts = [s['b'] for s in self.seg] + [s['a'] for s in self.seg] + \
              [_add(h[0], h[2], h[3]) for h in self.hojas]
        y0 = min(0.0, min(p[1] for p in pts))
        y1 = max(p[1] for p in pts)
        k = 1.0 / max(1e-6, y1 - y0)
        tr = lambda p: ((p[0]) * k, (p[1] - y0) * k, (p[2]) * k)
        for s in self.seg:
            s['a'], s['b'], s['r'] = tr(s['a']), tr(s['b']), s['r'] * k
        for h in self.hojas:
            h[0], h[3] = tr(h[0]), h[3] * k
        self.racimos = [(tr(q), t * k, d, pl) for q, t, d, pl in self.racimos]
        hs = [h[0] for h in self.hojas] or [(0.0, 0.5, 0.0)]
        c = _mul(tuple(sum(p[q] for p in hs) for q in range(3)), 1.0 / len(hs))
        R = max(_len(_add(p, c, -1.0)) for p in hs) or 1.0
        for h in self.hojas:
            h[5] = max(0.0, min(1.0, 1.0 - _len(_add(h[0], c, -1.0)) / R))
        nmax = max([s['nivel'] for s in self.seg] + [1])
        radio = max([math.hypot(p[0], p[2]) for p in hs] + [math.hypot(s['b'][0], s['b'][2]) for s in self.seg])
        copa = sorted(math.hypot(p[0], p[2]) for p in hs)[int(0.9 * (len(hs) - 1))]
        base_copa = sorted(p[1] for p in hs)[int(0.05 * (len(hs) - 1))]
        return dict(modelo=self.modelo, deriv=self.deriv,
                    ramas=[(s['a'], s['b'], s['r'], s['nivel']) for s in self.seg],
                    radios=[(s['r'], self.seg[s['hijos'][0]]['r'] if s['hijos'] else s['r'] * 0.8,
                             [self.seg[h]['r'] for h in s['hijos']]) for s in self.seg],
                    hojas=[tuple(h) for h in self.hojas], racimos=self.racimos, nmax=nmax,
                    radio=radio, copa=copa, base_copa=base_copa, centro=c,
                    alto_tronco=min([s['b'][1] for s in self.seg if s['nivel'] == 0 and s['hijos']
                                     and len(s['hijos']) > 1] or [base_copa]))


HOJA_K = dict(aguja=0.95, ancha=0.75, lanceolada=0.62, espada=1.25, fronda=0.55, abanico=0.6, lamina=1.0,
              menuda=0.55)   # largo de la hoja, x el del racimo
HOJA_K.update((f, 0.5) for f in FLORES)


def _gen_conifera(P):
    """Rauh / Massart: tronco unico, pisos de ramas casi horizontales, mas
    cortas arriba; las puntas suben. Aguja en haces. Triangulo dentado."""
    pisos = {1: 3, 2: 5, 3: 8}[P.deriv]
    tr, pts, _ = P.eje((0, 0, 0), SUBE, 1.0, pisos + 2, 0, None)
    g = P.u(0, 360)
    for k in range(pisos):
        y = 0.16 + 0.76 * k / max(1, pisos - 1) if pisos > 1 else 0.5
        idx = min(len(tr) - 1, int(y * len(tr)))
        p = _add(pts[0], SUBE, y)
        l = 0.04 + 0.30 * (1.0 - y) ** 1.1
        nr = 4 + (k % 2)
        for j in range(nr):
            d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['conifera']), g + 360.0 * j / nr + ANGULO_AUREO * k)
            t2, p2, d2 = P.eje(p, d, l * P.u(0.85, 1.15), 2 + (P.deriv >= 2), 1, tr[idx], tropismo=0.12)
            for q in range(1, len(p2) - 1 if P.deriv >= 2 else 1):
                for s in (-1.0, 1.0):
                    dl = P.hijo(d2, 55.0, 90.0 * s)
                    P.racimo(p2[q], _norm((dl[0], 0.25, dl[2])), 0.36 * l, 2, t2[q - 1], n=P.dens + 2)
            P.racimo(p2[-1], d2, 0.5 * l, 1, t2[-1], n=P.dens + 3)
    P.racimo(pts[-1], SUBE, 0.14, 0, tr[-1], n=P.dens + 3)


def _gen_pagoda(P):
    """Aubreville: pisos de ramas horizontales que acaban en platos de hojas
    planos. Pisos separados por huecos."""
    pisos = {1: 2, 2: 3, 3: 4}[P.deriv]
    tr, pts, _ = P.eje((0, 0, 0), SUBE, 1.0, 6, 0, None)
    g = P.u(0, 360)
    for k in range(pisos):
        y = 0.38 + 0.56 * k / max(1, pisos - 1) if pisos > 1 else 0.6
        idx = min(len(tr) - 1, int(y * len(tr)))
        l = 0.42 * (1.0 - 0.55 * k / max(1, pisos))
        nr = 5
        for j in range(nr):
            d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['pagoda']), g + 72.0 * j + 31.0 * k)
            t2, p2, d2 = P.eje(_add((0, 0, 0), SUBE, y), d, l, 2, 1, tr[idx], tropismo=0.03)
            for s in (-35.0, 0.0, 35.0):
                dd = _girar_eje(d2, SUBE, s)
                P.racimo(p2[-1], _norm((dd[0], 0.02, dd[2])), 0.42 * l, 1, t2[-1], plano=True, n=P.dens + 4)


def _gen_parasol(P):
    """Troll: el tronco se abre en 3 o 4 brazos oblicuos; ramas plagiotropas
    con una capa fina de hojas arriba. T de techo plano."""
    inc = _norm((P.u(-0.08, 0.08), 1.0, P.u(-0.08, 0.08)))
    tr, pts, d = P.eje((0, 0, 0), inc, 0.55, 3, 0, None)
    nb = 3 + (P.rng.random() < 0.5)
    g = P.u(0, 360)
    for j in range(nb):
        da = P.hijo(d, P.ang(ANGULO_PLANTA['parasol']), g + 360.0 * j / nb)
        t2, p2, d2 = P.eje(pts[-1], da, 0.42, 2, 1, tr[-1], tropismo=0.05)
        nh = {1: 2, 2: 3, 3: 4}[P.deriv]
        for q in range(nh):
            dh = _girar_eje(_norm((d2[0], 0.0, d2[2])), SUBE, -50.0 + 100.0 * q / max(1, nh - 1))
            t3, p3, _ = P.eje(p2[-1], _norm((dh[0], 0.06, dh[2])), 0.30 * P.u(0.8, 1.2), 2, 2, t2[-1])
            for r_ in range(1, len(p3)):
                P.racimo(p3[r_], _norm((dh[0], 0.15, dh[2])), 0.16, 2, t3[r_ - 1], plano=True, n=P.dens + 3)
                if P.var % 3 == 1:              # motor v97: una de cada tres variantes, en flor (flamboyan)
                    P.flor(_add(p3[r_], SUBE, 0.02), SUBE, 0.07, 'flor_roja', 4, 2)


def _gen_drago(P):
    """Leeuwenberg: horquillas de 2 o 3 ramas repetidas, con una roseta de
    hojas de espada en cada punta. Paraguas de penachos."""
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.42, 3, 0, None)
    niveles = {1: 2, 2: 3, 3: 4}[P.deriv]
    frente = [(pts[-1], d, tr[-1], 0.22)]
    for nv in range(niveles):
        sig = []
        for p, dd, pad, l in frente:
            nh = 2 + (P.rng.random() < 0.4)
            g = P.u(0, 360)
            for j in range(nh):
                dh = P.hijo(dd, P.ang(ANGULO_PLANTA['drago']), g + 360.0 * j / nh)
                t2, p2, d2 = P.eje(p, dh, l * P.u(0.85, 1.1), 1, nv + 1, pad, tropismo=0.15)
                sig.append((p2[-1], d2, t2[-1], l * 0.78))
        frente = sig
    for p, dd, pad, l in frente:
        P.racimo(p, _norm(_add(dd, SUBE, 0.6)), 0.15, niveles, pad, roseta=True, abre=70.0, n=P.dens + 8)


def _gen_frondosa(P):
    """Scarrone: 3 o 4 ramas madre ascendentes que se dividen, con racimos de
    hojas en las puntas. Copa lobulada con huecos."""
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.34, 3, 0, None)
    niveles = {1: 2, 2: 3, 3: 4}[P.deriv]
    nm = 3 + (P.rng.random() < 0.6)
    g = P.u(0, 360)
    frente = []
    for j in range(nm):
        dm = P.hijo(d, P.ang(ANGULO_PLANTA['frondosa']), g + 360.0 * j / nm)
        frente.append((pts[-1], dm, tr[-1], 0.30 * P.u(0.8, 1.2)))
    for nv in range(niveles):
        sig = []
        for p, dd, pad, l in frente:
            t2, p2, d2 = P.eje(p, dd, l, 2, nv + 1, pad, tropismo=0.10)
            if nv == niveles - 1:
                P.racimo(p2[-1], d2, 0.20, nv + 1, t2[-1], n=P.dens + 6)
                P.racimo(p2[1], P.hijo(d2, 50.0, P.u(0, 360)), 0.14, nv + 1, t2[0], n=P.dens + 3)
                if P.var % 4 == 2:              # motor v97: una de cada cuatro variantes, en flor (cerezo)
                    P.flor(_add(p2[-1], d2, 0.12), d2, 0.06, 'flor_rosa', 5, nv + 1)
                elif P.var % 4 == 3:            # y otra, con fruto (naranjo)
                    P.flor(_add(p2[-1], d2, 0.08), d2, 0.035, 'flor_naranja', 2, nv + 1)
                continue
            nh = 2 + (P.rng.random() < 0.35)
            gg = P.u(0, 360)
            for q in range(nh):
                sig.append((p2[-1], P.hijo(d2, P.ang(ANGULO_PLANTA['frondosa'] * 0.9), gg + 360.0 * q / nh),
                            t2[-1], l * P.u(0.62, 0.82)))
        frente = sig


def _gen_palmera(P):
    """Corner: tronco curvado sin ramas y una corona de frondas arqueadas.
    Estrella sobre un palo."""
    g = math.radians(P.u(0, 360))
    curva = (0.05 * math.cos(g), 0.0, 0.05 * math.sin(g))
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.82, 6, 0, None, curva=curva)
    nf = {1: 5, 2: 8, 3: 11}[P.deriv]
    g0 = P.u(0, 360)
    for j in range(nf):
        df = P.hijo(d, P.ang(55.0 + 25.0 * (j % 2)), g0 + ANGULO_AUREO * j)
        t2, p2, _ = P.eje(pts[-1], df, 0.46 * P.u(0.85, 1.15), 4, 1, tr[-1], tropismo=-0.32)
        for q in range(1, len(p2)):
            dq = _norm(_add(p2[q], p2[q - 1], -1.0))
            P.hojas.append([p2[q - 1], _norm(_cross(dq, _cross(SUBE, dq))) if abs(dq[1]) < 0.98 else SUBE,
                            dq, 0.17 * P.u(0.9, 1.1), 'fronda', 0.0, 2])
        P.racimos.append((p2[2], 0.18, df, False))


def _gen_sauce(P):
    """Lloron: ramas que suben y cortinas de ramillas colgantes. Cortina."""
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.30, 2, 0, None)
    nm = 3 + int(P.u(0, 2.99))
    g = P.u(0, 360)
    cortinas = {1: 2, 2: 3, 3: 5}[P.deriv]
    for j in range(nm):
        dm = P.hijo(d, P.ang(ANGULO_PLANTA['sauce']), g + 360.0 * j / nm)
        t2, p2, d2 = P.eje(pts[-1], dm, 0.55 * P.u(0.85, 1.15), 3, 1, tr[-1], tropismo=0.06)
        for q in range(cortinas):
            k = len(p2) - 1 - (q % (len(p2) - 1))
            fuera = _norm((d2[0] + P.u(-0.3, 0.3), 0.0, d2[2] + P.u(-0.3, 0.3)))
            t3, p3, _ = P.eje(p2[k], _norm(_add(fuera, SUBE, 0.4)), 0.18, 1, 2, t2[k - 1])
            largo = max(0.15, p3[-1][1] - 0.30) * P.u(0.75, 1.0)     # el tronco se ve debajo
            t4, p4, _ = P.eje(p3[-1], _norm(_add(fuera, SUBE, -2.5)), largo, 4, 3, t3[-1], tropismo=-0.6)
            for r_ in range(1, len(p4)):
                P.racimo(p4[r_ - 1], _norm(_add(p4[r_], p4[r_ - 1], -1.0)), 0.9 * largo / 4.0, 3, t4[r_ - 1],
                         abre=35.0, n=P.dens)


def _gen_retama(P):
    """15-25 tallos desde la base abiertos en abanico; pocas hojas finas."""
    n = 15 + int(P.u(0, 10.99))
    for j in range(n):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['retama'] * P.u(0.3, 1.6)), ANGULO_AUREO * j)
        t2, p2, d2 = P.eje((P.u(-0.03, 0.03), 0.0, P.u(-0.03, 0.03)), d, P.u(0.7, 1.0), 3, 0, None,
                           tropismo=-0.04)
        P.racimo(p2[-1], d2, 0.16, 1, t2[-1], n=max(2, P.dens // 2), abre=20.0)
        if j % 2 == 0:                          # motor v97: la retama, en flor
            P.flor(_add(p2[-1], d2, 0.08), d2, 0.07, 'flor_amarilla', 4, 1)


def _gen_brezo(P):
    """Ramillete bajo y enmaranado; hoja menuda en racimos."""
    for j in range(8):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['brezo'] * P.u(0.5, 1.5)), ANGULO_AUREO * j)
        t2, p2, d2 = P.eje((0.0, 0.0, 0.0), d, P.u(0.45, 0.7), 2, 0, None, tropismo=0.05)
        for q in range(3):
            dh = P.hijo(d2, P.u(20, 60), P.u(0, 360))
            t3, p3, d3 = P.eje(p2[-1 - (q % 2)], dh, P.u(0.25, 0.4), 2, 1, t2[-1 - (q % 2)])
            P.racimo(p3[-1], d3, 0.14, 2, t3[-1], n=P.dens + 4, abre=65.0)
            if (j + q) % 2 == 0:                # motor v97: el brezo, en flor
                P.flor(_add(p3[-1], d3, 0.10), d3, 0.06, 'flor_violeta', 4, 2)


def _gen_helecho(P):
    """Roseta de frondas arqueadas desde la base."""
    for j in range(9 + int(P.u(0, 3.99))):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['helecho'] * P.u(0.7, 1.2)), ANGULO_AUREO * j)
        t2, p2, _ = P.eje((0, 0, 0), d, P.u(0.85, 1.1), 4, 0, None, tropismo=-0.22)
        for q in range(1, len(p2)):
            dq = _norm(_add(p2[q], p2[q - 1], -1.0))
            P.hojas.append([p2[q - 1], _norm(_cross(dq, _cross(SUBE, dq))) if abs(dq[1]) < 0.98 else SUBE,
                            dq, 0.26 * P.u(0.9, 1.1), 'fronda', 0.0, 1])
        P.racimos.append((p2[2], 0.3, d, False))


def _gen_graminea(P):
    """Mata: fuente de laminas que se arquean hacia fuera."""
    for j in range(30 + int(P.u(0, 10.99))):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['graminea'] * P.u(0.2, 1.3)), ANGULO_AUREO * j)
        t2, p2, _ = P.eje((0, 0, 0), d, P.u(0.15, 0.25), 1, 0, None)
        e = math.radians(P.u(-15, 15))
        P.hojas.append([p2[-1], _norm(_cross(d, _cross(SUBE, d))) if abs(d[1]) < 0.98 else SUBE,
                        _norm(_add(d, SUBE, 0.3 + 0.2 * math.sin(e))), P.u(0.6, 0.85), 'lamina', 0.0, 1])
        P.racimos.append((p2[-1], 0.3, d, False))


def _gen_enebro(P):
    """Ramas tendidas a ras de suelo, con agujas."""
    for j in range(6 + int(P.u(0, 2.99))):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['enebro']), 360.0 * j / 6.0 + P.u(-20, 20))
        t2, p2, d2 = P.eje((0, 0.0, 0), d, P.u(1.0, 1.5), 4, 0, None, tropismo=0.03)
        for q in range(1, len(p2)):
            for s in (-1.0, 1.0):
                dl = P.hijo(d2, 50.0, 90.0 * s)
                P.racimo(p2[q], _norm((dl[0], 0.5, dl[2])), 0.14, 1, t2[q - 1], n=P.dens + 4)


def _gen_palmito(P):
    """Abanicos sobre un tallo corto."""
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.25, 2, 0, None)
    for j in range(8 + int(P.u(0, 3.99))):
        dp = P.hijo(d, P.ang(ANGULO_PLANTA['palmito'] * P.u(0.4, 1.4)), ANGULO_AUREO * j)
        t2, p2, d2 = P.eje(pts[-1], dp, P.u(0.4, 0.6), 2, 1, tr[-1], tropismo=0.05)
        P.hojas.append([p2[-1], _norm(_cross(d2, _cross(SUBE, d2))) if abs(d2[1]) < 0.98 else SUBE,
                        d2, 0.38 * P.u(0.85, 1.15), 'abanico', 0.0, 2])
        P.racimos.append((p2[-1], 0.2, d2, False))


# --- motor v97: ocho arboles y dos matorrales mas --------------------------------------

def _gen_cipres(P):
    """Fastigiado: un eje y ramas cortas casi verticales, pegadas a el. Llama estrecha
    y oscura sobre un fuste corto."""
    pisos = {1: 5, 2: 8, 3: 12}[P.deriv]
    tr, pts, _ = P.eje((0, 0, 0), SUBE, 1.0, pisos + 2, 0, None)
    g = P.u(0, 360)
    for k in range(pisos):
        y = 0.20 + 0.72 * k / max(1, pisos - 1)
        idx = min(len(tr) - 1, int(y * len(tr)))
        panza = math.sin(math.pi * min(1.0, (y - 0.12) / 0.92)) ** 0.6
        l = 0.05 + 0.13 * panza
        for j in range(3):
            d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['cipres']), g + 120.0 * j + ANGULO_AUREO * k)
            t2, p2, d2 = P.eje((0.0, y, 0.0), d, l, 2, 1, tr[idx], tropismo=0.5)
            arriba = _norm(_add(d2, SUBE, 1.0))
            P.racimo(p2[1], arriba, 0.75 * l, 1, t2[0], n=P.dens + 3, abre=24.0)
            P.racimo(p2[-1], arriba, 0.9 * l, 1, t2[-1], n=P.dens + 4, abre=24.0)
    P.racimo(pts[-1], SUBE, 0.10, 0, tr[-1], n=P.dens + 3, abre=20.0)


def _gen_abedul(P):
    """Fuste fino, blanco y algo sinuoso; copa alta y ligera, con ramillas que cuelgan."""
    g0 = math.radians(P.u(0, 360))
    curva = (0.018 * math.cos(g0), 0.0, 0.018 * math.sin(g0))
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.95, 8, 0, None, curva=curva)
    n = {1: 4, 2: 7, 3: 11}[P.deriv]
    g = P.u(0, 360)
    for k in range(n):
        idx = 3 + (k * (len(tr) - 3)) // n
        p = pts[idx + 1]
        dr = P.hijo(SUBE, P.ang(ANGULO_PLANTA['abedul']), g + ANGULO_AUREO * k)
        l = 0.36 * (1.0 - 0.5 * k / float(n)) * P.u(0.85, 1.15)
        t2, p2, d2 = P.eje(p, dr, l, 3, 1, tr[idx], tropismo=0.08)
        for q in (2, 3):
            cae = _norm(_add((d2[0], 0.0, d2[2]), SUBE, -1.6))
            t3, p3, d3 = P.eje(p2[q], cae, 0.11 * P.u(0.8, 1.3), 2, 2, t2[q - 1], tropismo=-0.3)
            P.racimo(p3[1], d3, 0.11, 2, t3[0], n=P.dens + 3, abre=55.0)
            P.racimo(p3[-1], d3, 0.11, 2, t3[-1], n=P.dens + 3, abre=55.0)
        P.racimo(p2[1], P.hijo(d2, 50.0, P.u(0, 360)), 0.11, 1, t2[0], n=P.dens + 3, abre=55.0)
        P.racimo(p2[-1], d2, 0.12, 1, t2[-1], n=P.dens + 4, abre=50.0)
    P.racimo(pts[-1], d, 0.10, 0, tr[-1], n=P.dens + 2, abre=45.0)


def _gen_araucaria(P):
    """Pisos de ramas horizontales muy separados, cada vez mas cortos, con la punta
    vuelta hacia arriba y un penacho: una torre de platos con huecos, simetrica."""
    pisos = {1: 3, 2: 4, 3: 6}[P.deriv]
    tr, pts, _ = P.eje((0, 0, 0), SUBE, 1.0, 8, 0, None)
    g = P.u(0, 360)
    for k in range(pisos):
        y = 0.24 + 0.68 * k / max(1, pisos - 1)
        idx = min(len(tr) - 1, int(y * len(tr)))
        l = 0.36 * (1.0 - 0.72 * k / float(pisos))
        for j in range(5):
            d = P.hijo(SUBE, ANGULO_PLANTA['araucaria'] + P.u(-4.0, 4.0), g + 72.0 * j + 36.0 * k)
            t2, p2, d2 = P.eje((0.0, y, 0.0), d, l * P.u(0.92, 1.08), 3, 1, tr[idx], tropismo=0.05)
            P.racimo(p2[-1], _norm(_add(d2, SUBE, 0.9)), 0.07, 1, t2[-1], roseta=True, abre=62.0, n=P.dens + 6)
            P.racimo(p2[-2], _norm(_add(d2, SUBE, 0.25)), 0.06, 1, t2[-2], n=P.dens + 2, abre=40.0)
    P.racimo(pts[-1], SUBE, 0.08, 0, tr[-1], roseta=True, abre=66.0, n=P.dens + 6)


def _gen_olivo(P):
    """Tronco corto, grueso y torcido que se abre muy abajo en 2 o 3 brazos; copa
    baja, ancha y densa de hoja lanceolada gris."""
    g0 = math.radians(P.u(0, 360))
    curva = (0.10 * math.cos(g0), 0.0, 0.10 * math.sin(g0))
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.22, 3, 0, None, curva=curva)
    nm = 2 + (P.rng.random() < 0.6)
    niveles = {1: 2, 2: 3, 3: 3}[P.deriv]
    g = P.u(0, 360)
    frente = [(pts[-1], P.hijo(d, P.ang(ANGULO_PLANTA['olivo']), g + 360.0 * j / nm), tr[-1],
               0.26 * P.u(0.85, 1.15)) for j in range(nm)]
    for nv in range(niveles):
        sig = []
        for p, dd, pad, l in frente:
            t2, p2, d2 = P.eje(p, dd, l, 2, nv + 1, pad, tropismo=0.04)
            P.racimo(p2[-1], d2, 0.13, nv + 1, t2[-1], n=P.dens + 5)
            if nv == niveles - 1:
                P.racimo(p2[1], P.hijo(d2, 60.0, P.u(0, 360)), 0.11, nv + 1, t2[0], n=P.dens + 3)
                continue
            nh = 2 + (P.rng.random() < 0.5)
            gg = P.u(0, 360)
            for q in range(nh):
                sig.append((p2[-1], P.hijo(d2, P.ang(42.0), gg + 360.0 * q / nh), t2[-1], l * P.u(0.6, 0.8)))
        frente = sig


def _gen_baobab(P):
    """Tronco de botella, liso y muy grueso; arriba, un punado de ramas cortas y
    torcidas como raices, con poca hoja."""
    P.r_punta = 0.02                    # ramas gruesas: Leonardo engorda el tronco
    tr, pts, d = P.eje((0, 0, 0), SUBE, 0.62, 4, 0, None)
    nm = {1: 3, 2: 4, 3: 5}[P.deriv]
    g = P.u(0, 360)
    for j in range(nm):
        dm = P.hijo(d, P.ang(ANGULO_PLANTA['baobab']), g + 360.0 * j / nm)
        t2, p2, d2 = P.eje(pts[-1], dm, 0.24 * P.u(0.8, 1.2), 2, 1, tr[-1], tropismo=0.10)
        for q in range(2 + (P.deriv >= 3)):
            dh = P.hijo(d2, P.ang(45.0), P.u(0, 360))
            t3, p3, d3 = P.eje(p2[-1], dh, 0.14 * P.u(0.7, 1.2), 2, 2, t2[-1], tropismo=0.05)
            P.racimo(p3[-1], d3, 0.07, 2, t3[-1], n=P.dens)
            if P.var % 2 == 0:
                P.flor(p3[-1], _mul(SUBE, -1.0), 0.05, 'flor_blanca', 1, 2)


def _gen_mangle(P):
    """Raices zancudas en arco bajo un tronco corto; copa baja, ancha y densa. El
    arbol de la orilla."""
    y0 = 0.30
    P.r_punta = 0.011
    for j in range(6 + int(P.u(0, 3.99))):          # las raices: del tronco al agua
        d = P.hijo(SUBE, 78.0 + P.u(-10.0, 10.0), ANGULO_AUREO * j)
        P.eje((0.0, y0 * P.u(0.7, 1.05), 0.0), d, 0.42 * P.u(0.8, 1.2), 4, 0, None, tropismo=-0.42)
    P.r_punta = R_PUNTA
    tr, pts, d = P.eje((0, y0 * 0.6, 0), SUBE, 0.26, 2, 0, None)
    nm = 3 + (P.rng.random() < 0.5)
    niveles = {1: 1, 2: 2, 3: 2}[P.deriv]
    g = P.u(0, 360)
    frente = [(pts[-1], P.hijo(d, P.ang(ANGULO_PLANTA['mangle']), g + 360.0 * j / nm), tr[-1],
               0.24 * P.u(0.85, 1.15)) for j in range(nm)]
    for nv in range(niveles):
        sig = []
        for p, dd, pad, l in frente:
            t2, p2, d2 = P.eje(p, dd, l, 2, nv + 1, pad, tropismo=0.12)
            P.racimo(p2[-1], d2, 0.14, nv + 1, t2[-1], n=P.dens + 6)
            P.racimo(p2[1], P.hijo(d2, 55.0, P.u(0, 360)), 0.12, nv + 1, t2[0], n=P.dens + 4)
            if nv == niveles - 1:
                continue
            gg = P.u(0, 360)
            for q in range(2):
                sig.append((p2[-1], P.hijo(d2, P.ang(46.0), gg + 180.0 * q), t2[-1], l * P.u(0.6, 0.8)))
        frente = sig


def _gen_bambu(P):
    """Mata de canas verdes, rectas, que se arquean arriba, con penachos de hoja fina
    en los nudos altos."""
    n = {1: 4, 2: 7, 3: 11}[P.deriv]
    for j in range(n):
        gj = math.radians(ANGULO_AUREO * j)
        fuera = (math.cos(gj), 0.0, math.sin(gj))
        base = _mul(fuera, P.u(0.0, 0.07))
        d = _norm(_add(SUBE, fuera, math.tan(math.radians(abs(P.ang(ANGULO_PLANTA['bambu']) * P.u(0.3, 1.2))))))
        P.r_punta = 0.006
        t2, p2, d2 = P.eje(base, d, P.u(0.7, 1.0), 6, 0, None, curva=_mul(fuera, 0.045))
        P.r_punta = R_PUNTA
        for q in range(3, len(p2) - 1):
            dl = P.hijo(d2, 60.0, P.u(0, 360))
            P.racimo(p2[q], _norm((dl[0], 0.15, dl[2])), 0.09, 1, t2[q - 1], n=P.dens, abre=40.0)
        P.racimo(p2[-1], d2, 0.10, 1, t2[-1], n=P.dens + 2, abre=35.0)


def _gen_cardon(P):
    """Cactus de candelabro: una columna gruesa con 2 a 4 brazos que suben; sin
    hojas, con flores blancas en las puntas."""
    P.r_punta = 0.034
    tr, pts, _ = P.eje((0, 0, 0), SUBE, 1.0, 5, 0, None)
    nb = {1: 1, 2: 2, 3: 3}[P.deriv] + (P.rng.random() < 0.5)
    g = P.u(0, 360)
    for j in range(nb):
        idx = 1 + (j % 2)
        d = P.hijo(SUBE, ANGULO_PLANTA['cardon'], g + 360.0 * j / nb + P.u(-25.0, 25.0))
        t2, p2, d2 = P.eje(pts[idx + 1], d, 0.20 * P.u(0.9, 1.2), 1, 1, tr[idx])
        t3, p3, d3 = P.eje(p2[-1], _norm(_add(SUBE, d, 0.08)), P.u(0.22, 0.42), 2, 1, t2[-1])
        P.flor(p3[-1], SUBE, 0.05, 'flor_blanca', 5, 1)
        P.racimos.append((p3[-1], 0.12, SUBE, False))
    P.flor(pts[-1], SUBE, 0.05, 'flor_blanca' if P.var % 2 == 0 else 'flor_roja', 6, 0)
    P.racimos.append((pts[-1], 0.12, SUBE, False))


def _gen_agave(P):
    """Roseta de hojas de espada, gruesas, desde el suelo."""
    for j in range(14 + int(P.u(0, 6.99))):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['agave'] * P.u(0.25, 1.5)), ANGULO_AUREO * j)
        t2, p2, _ = P.eje((0, 0, 0), d, 0.05, 1, 0, None)
        P.hojas.append([p2[-1], _norm(_cross(d, _cross(SUBE, d))) if abs(d[1]) < 0.98 else (1.0, 0.0, 0.0),
                        _norm(_add(d, SUBE, 0.15)), P.u(0.7, 1.0), 'espada', 0.0, 1])
        P.racimos.append((_add(p2[-1], d, 0.4), 0.35, d, False))


def _gen_junco(P):
    """Haz de tallos finos y rectos, cada uno con su lamina: el carrizal de la orilla."""
    for j in range(22 + int(P.u(0, 10.99))):
        d = P.hijo(SUBE, abs(P.ang(ANGULO_PLANTA['junco'] * P.u(0.2, 1.6))), ANGULO_AUREO * j)
        t2, p2, d2 = P.eje((P.u(-0.06, 0.06), 0.0, P.u(-0.06, 0.06)), d, P.u(0.45, 0.8), 2, 0, None)
        P.hojas.append([p2[-1], _norm(_cross(d2, _cross(SUBE, d2))) if abs(d2[1]) < 0.98 else (1.0, 0.0, 0.0),
                        _norm(_add(d2, SUBE, 0.6)), P.u(0.25, 0.4), 'lamina', 0.0, 1])
        if j % 3 == 0:
            P.racimos.append((p2[-1], 0.25, d2, False))


_GEN = dict(conifera=_gen_conifera, pagoda=_gen_pagoda, parasol=_gen_parasol, drago=_gen_drago,
            frondosa=_gen_frondosa, palmera=_gen_palmera, sauce=_gen_sauce, retama=_gen_retama,
            brezo=_gen_brezo, helecho=_gen_helecho, graminea=_gen_graminea, enebro=_gen_enebro,
            palmito=_gen_palmito, cipres=_gen_cipres, abedul=_gen_abedul, araucaria=_gen_araucaria,
            olivo=_gen_olivo, baobab=_gen_baobab, mangle=_gen_mangle, bambu=_gen_bambu, cardon=_gen_cardon,
            agave=_gen_agave, junco=_gen_junco)
_BIBLIO = {}


def etapas_de(modelo):
    """Derivaciones guardadas: los arboles, el joven (2) y el adulto (DERIVACIONES);
    los matorrales, 1. (El brinzal, 1, existe en la biblioteca pero no tiene
    geometria en TouchDesigner: ahorra 7 x Variantes x 2 geometrias.)"""
    return [DERIVACION_JOVEN, DERIVACIONES] if modelo in ARBOLES else [1]


def _clave_biblio(cfg):
    return (round(float(cfg.get('var_angulo', 12.0)), 3), int(bool(cfg.get('cuantizar30', 0))),
            int(cfg.get('densidad_hoja', 6)))


def ejemplar(cfg, modelo, var, deriv):
    """El ejemplar (modelo, variante, derivacion) de la biblioteca (se calcula
    una vez por Varangulo, Cuantizar30 y Densidadhoja)."""
    k = (_clave_biblio(cfg), modelo, int(var), int(deriv))
    e = _BIBLIO.get(k)
    if e is None:
        if len(_BIBLIO) > 2000:
            _BIBLIO.clear()
        P = _Planta(modelo, int(var), int(deriv), cfg)
        _GEN[modelo](P)
        e = _BIBLIO[k] = P.cerrar()
    return e


def variantes(cfg):
    """Variantes por modelo: Variantes, sin pasar de las que hay en TouchDesigner."""
    global VARIANTES_TD
    v = max(1, int(cfg.get('variantes', 4)))
    if VARIANTES_TD is None:                # tras recargar el motor: lo que hizo la fase 11
        try:
            VARIANTES_TD = int(me.fetch('variantes_td', 0))
        except Exception:
            VARIANTES_TD = 0
    if VARIANTES_TD:
        v = min(v, VARIANTES_TD)
    return v


VARIANTES_TD = None          # las variantes con geometria en TouchDesigner (0: sin limite)


def biblioteca(cfg):
    """Precalcula toda la biblioteca: modelos x Variantes x derivaciones.
    Devuelve el numero de ejemplares."""
    n = 0
    for mo in PLANTAS:
        for v in range(variantes(cfg)):
            for d in etapas_de(mo):
                ejemplar(cfg, mo, v, d)
                n += 1
    return n


def nombre_ejemplar(modelo, var, deriv, lejos=False):
    return 'veg_%s_%d_%d%s' % (modelo, var, deriv, '_lod' if lejos else '')


def ejemplares_de(cfg):
    """Los nombres de los ejemplares (y sus versiones lejanas) que necesita TD."""
    out = []
    for mo in PLANTAS:
        for v in range(variantes(cfg)):
            for d in etapas_de(mo):
                out.append(nombre_ejemplar(mo, v, d))
                out.append(nombre_ejemplar(mo, v, d, True))
    return out


def es_ejemplar(nombre):
    if not nombre.startswith('veg_'):
        return False
    partes = nombre[4:].split('_')
    return len(partes) >= 3 and partes[0] in _GEN


def parte_ejemplar(nombre):
    """(modelo, variante, derivacion, lejos) de un nombre veg_<modelo>_<v>_<d>[_lod]."""
    partes = nombre[4:].split('_')
    return partes[0], int(partes[1]), int(partes[2]), len(partes) > 3


# --- la malla de un ejemplar ---------------------------------------------------------
# Hoja facetada low-poly de dos caras, 4 a 6 triangulos con pliegue central. En el
# eje local: X a lo largo de la hoja (0 a 1), Y su normal, Z de lado.
def _plantilla_fronda(pares=7):
    """Motor v97: la fronda (palmera, helecho) es pinnada de verdad: un raquis que
    se arquea y 'pares' de foliolos que cuelgan a los lados (antes, 6 triangulos)."""
    P, T = [], []
    for k in range(pares):
        u = k / float(pares - 1)
        x = 0.10 + 0.84 * u
        y = -0.08 * x
        w = 0.36 * math.sin(math.pi * (0.12 + 0.80 * u)) ** 0.7
        for s_ in (-1.0, 1.0):
            i0 = len(P)
            P += [(x - 0.04, y, 0.0), (x + 0.04, y, 0.0), (x + 0.10, y - 0.16 * w, s_ * w)]
            T.append((i0, i0 + 1, i0 + 2) if s_ > 0 else (i0 + 1, i0, i0 + 2))
    i0 = len(P)
    P += [(0.0, 0.0, -0.014), (0.0, 0.0, 0.014), (1.0, -0.08, 0.0)]
    T.append((i0, i0 + 1, i0 + 2))
    return P, T


_PLANTILLAS = dict(
    # motor v97: la hoja ancha y la lanceolada, en dos tramos (el limbo se comba hacia la punta)
    ancha=([(0, 0, 0), (0.30, -0.05, -0.30), (0.68, -0.08, -0.26), (1, -0.07, 0), (0.68, -0.08, 0.26),
            (0.30, -0.05, 0.30), (0.33, 0.06, 0), (0.68, 0.03, 0)],
           [(0, 6, 1), (1, 6, 7), (1, 7, 2), (2, 7, 3), (0, 5, 6), (5, 7, 6), (5, 4, 7), (4, 3, 7)]),
    flor=([(0, 0, 0), (0.5, -0.05, -0.42), (1, 0, 0), (0.5, -0.05, 0.42), (0.5, 0.09, 0)],
          [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    menuda=([(0, 0, 0), (0.5, -0.05, -0.3), (1, 0, 0), (0.5, -0.05, 0.3), (0.5, 0.05, 0)],
            [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    lanceolada=([(0, 0, 0), (0.28, -0.03, -0.13), (0.65, -0.06, -0.11), (1, -0.08, 0), (0.65, -0.06, 0.11),
                 (0.28, -0.03, 0.13), (0.30, 0.04, 0), (0.65, 0.0, 0)],
                [(0, 6, 1), (1, 6, 7), (1, 7, 2), (2, 7, 3), (0, 5, 6), (5, 7, 6), (5, 4, 7), (4, 3, 7)]),
    espada=([(0, 0, 0), (0.5, -0.03, -0.07), (1, 0.05, 0), (0.5, -0.03, 0.07), (0.5, 0.03, 0)],
            [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    aguja=([(0, 0, 0), (1, 0.08, -0.34), (0.9, 0.14, -0.26), (1, 0.12, 0.0), (0.9, 0.2, 0.06),
            (1, 0.08, 0.34), (0.9, 0.14, 0.26)],
           [(0, 1, 2), (0, 2, 1), (0, 3, 4), (0, 4, 3), (0, 5, 6), (0, 6, 5)]),
    fronda=_plantilla_fronda(),
    abanico=([(0, 0, 0)] + [(0.9 * math.cos(math.radians(a)), 0.05 * (k % 2), 0.9 * math.sin(math.radians(a)))
                            for k, a in enumerate(range(-70, 80, 14))],
             [(0, 1 + 2 * k, 2 + 2 * k) for k in range(5)]),
    lamina=([(0, 0, -0.05), (0, 0, 0.05), (0.5, 0.15, -0.04), (0.5, 0.18, 0.04), (1, -0.1, 0), (0.5, 0.2, 0)],
            [(0, 2, 1), (1, 2, 3), (2, 4, 5), (5, 4, 3)]),
)
# tarjeta de racimo (lejos): estrella dentada de 6 puntas, dos cruzadas
_TARJETA = ([(0, 0, 0)] + [((1.0 if k % 2 == 0 else 0.62) * math.cos(math.pi * k / 4.0), 0.0,
                            (1.0 if k % 2 == 0 else 0.62) * math.sin(math.pi * k / 4.0)) for k in range(8)],
            [(0, 1 + k, 1 + (k + 1) % 8) for k in range(8)])     # estrella dentada de 4 puntas
_MALLAS = {}


def malla_ejemplar(nombre, cfg=None):
    """(puntos, normales, uv, triangulos) de un ejemplar, para su Script SOP.
    uv = (tipo, profundidad, nivel): tipo 1 corteza, 2 + v hoja, 3 + v tarjeta de
    racimo (v en 0-0,9: la variacion de la hoja); profundidad 0 borde, 1 dentro;
    nivel de rama 0 tronco - 1 punta (el viento de la fase 17)."""
    cfg = cfg or DEFAULT_CFG
    if es_edificio(nombre):             # fase 11 v10: un ejemplar de la ciudad (el mismo Script SOP)
        return malla_edificio(nombre, cfg)
    clave = (nombre, _clave_biblio(cfg))
    v = _MALLAS.get(clave)
    if v is not None:
        return v
    import random
    mo, var, d, lejos = parte_ejemplar(nombre)
    e = ejemplar(cfg, mo, var, d)
    rng = random.Random(sum((k + 1) * ord(ch) for k, ch in enumerate(nombre)))
    P, Nn, U, T = [], [], [], []
    nmax = float(max(1, e['nmax']))
    tono = CORTEZA.get(mo, 0.0)             # motor v97: la corteza de cada modelo (v98: fuste y ramas madre)
    for (a, b, nivel), (r0, r1, _) in zip([(s[0], s[1], s[3]) for s in e['ramas']], e['radios']):
        if lejos and (nivel > 1 or r0 < 0.004):
            continue
        # motor v97: tubos mas redondos (antes 5 y 4 lados): el fuste, 8; las ramas madre, 6
        lados = (5 if nivel == 0 else 4) if lejos else (8 if nivel == 0 else (6 if nivel == 1 else 4))
        dv = _norm(_add(b, a, -1.0))
        ref = SUBE if abs(dv[1]) < 0.95 else (1.0, 0.0, 0.0)
        x = _norm(_cross(dv, ref))
        z = _cross(dv, x)
        k0 = len(P)
        for q in range(lados):
            g = 2.0 * math.pi * q / lados
            o = _add(_mul(x, math.cos(g)), z, math.sin(g))
            for c_, r_ in ((a, r0), (b, max(r1, 0.6 * r0))):
                P.append(_add(c_, o, r_))
                Nn.append(o)
                U.append((1.0, tono if nivel <= 1 else 0.0, nivel / nmax))
        for q in range(lados):
            i0, i1 = k0 + 2 * q, k0 + 2 * ((q + 1) % lados)
            T += [(i0, i1, i1 + 1), (i0, i1 + 1, i0 + 1)]
    if lejos:
        for q, t, dd, plano in e['racimos']:
            ref = SUBE if abs(dd[1]) < 0.95 else (1.0, 0.0, 0.0)
            lado = _norm(_cross(dd, ref))
            if plano:
                planos = [(SUBE, (1.0, 0.0, 0.0))]
            else:                          # mira afuera y arriba, a lo largo de la ramilla
                nr = _norm(_add(_norm(_cross(_cross(dd, SUBE), dd)) if abs(dd[1]) < 0.95 else SUBE, SUBE, 0.6))
                planos = [(nr, _norm(_cross(nr, lado)) if abs(_dot(nr, lado)) < 0.95 else lado)]
            centro = q if plano else _add(q, dd, -0.4 * t)
            for nrm, x in planos:          # la tarjeta del racimo
                z = _cross(nrm, x)
                vv = 0.9 * rng.random()
                k0 = len(P)
                for px, py, pz in _TARJETA[0]:
                    P.append(_add(centro, _add(_mul(x, px * t * 0.8), z, pz * t * 0.8)))
                    Nn.append(nrm)
                    U.append((3.0 + vv, 0.3, 1.0))
                T += [(k0 + a_, k0 + b_, k0 + c_) for a_, b_, c_ in _TARJETA[1]]
    else:
        for pos, nrm, ax, tam, tipo, prof, nivel in e['hojas']:
            flor = FLORES.get(tipo)
            pv, tv = _PLANTILLAS['flor' if flor is not None else tipo]
            z = _norm(_cross(ax, nrm))
            y = _cross(z, ax)
            vv = 0.9 * rng.random()
            ux = 2.0 + vv if flor is None else 4.0 + 0.1 * flor + 0.05     # la flor: 4 + color / 10
            k0 = len(P)
            for px, py, pz in pv:
                P.append(_add(pos, _add(_add(_mul(ax, px * tam), y, py * tam), z, pz * tam)))
                Nn.append(y)
                U.append((ux, prof, min(1.0, nivel / nmax)))
            T += [(k0 + a_, k0 + b_, k0 + c_) for a_, b_, c_ in tv]
    v = _MALLAS[clave] = (P, Nn, U, T)
    if len(_MALLAS) > 600:
        _MALLAS.clear()
    return v


# -----------------------------------------------------------------------------
# 1. NUCLEO - la ciudad legible (fase 11 v10, motor v67)
# -----------------------------------------------------------------------------
# Lo que la naturaleza ya hizo (fase 11 v8), en la ciudad: cada etapa de
# ocupacion es un TIPO de edificio distinto, con variantes, y la obra se ve
# entre una etapa y la siguiente. Nada de pilas de cajas que solo ganan altura.
#
#   BIBLIOTECA   al cargar y al cambiar Variantesciudad, Oblicuidad, Retranqueo
#                o Torsionmax: disenos x Variantesciudad. Cada ejemplar sale de
#                una GRAMATICA DE PARTICION (solar -> masa -> plantas ->
#                fachada) y tiene tres partes: volumenes (prismas de planta
#                rectangular u octogonal, con base, alto, giro y voladizo; las L,
#                U, H y patios son varios), datos de fachada por volumen (alto de
#                planta, ancho de vano, proporcion de hueco, materia y semilla:
#                van en el atributo uv de la malla) y puntos de remate (deposito,
#                antena, maquinaria, varillas, escalera, cable...: instancias
#                'ciu_'). La fachada NO es geometria: la dibuja el GLSL MAT de la
#                piel (mat_piel_ciudad) con esos datos y la escala de la
#                instancia: un prisma se lee como edificio con su reticula. En
#                TouchDesigner, un Script SOP por ejemplar (modelos/edi_<diseno>_<v>).
#   TIPOS        informal (SEQ1): caseta, casa que crece, tres plantas, racimo,
#                barrio denso, torre autoconstruida; planificada (SEQ2):
#                pabellon, bloque, manzana, podio, rascacielos. Los umbrales,
#                los de la fase 4 (racimo y manzana desde Umbralram - 1; barrio y
#                podio desde la fusion - 1; torre y rascacielos desde la corona - 1).
#   CRECEN       la informal por agregacion (cada gate una planta o un cuarto,
#                desplazado e inclinado hasta Oblicuidad: se ve por corte, sin
#                estirar); la planificada por repeticion (las plantas son del
#                mismo modulo: la instancia crece y el shader cuenta plantas).
#   LENGUAJE     la latitud (o Lenguaje) elige materias y remates: frio
#                (hormigon y chapa), templado (ladrillo y vidrio), calido (cal y
#                celosia). Se fija al empezar cada edificio: lo terminado
#                conserva el suyo.
#   OBRA         planificada: solar, excavacion, nucleo, esqueleto, fachada
#                (Desfasefachada plantas por detras), coronacion y terminada;
#                informal: la planta nueva en bloque gris con varillas, que el
#                gate siguiente revoca y pinta. Un paso por gate (Avance) o cada
#                Pasosetapa pasos. Gruas (Maxgruas) con baliza.
#   MUTANTES     COLONIA (informal sobre planificada): parasitos de la
#                biblioteca informal, Parasitospornota por nota, de la azotea
#                hacia abajo. MARCO (planificada sobre informal): Ville Spatiale
#                de pilares en los callejones, un nivel por nota, con capsulas.
#                Mutacion (o la saturacion del modular) dice hasta donde llegan.
#   CLUSTER      informal: el racimo se funde en barrio (alturas hacia la
#                capital, corredores cubiertos); planificada: torres que se
#                buscan: pasarela celeste (2-3), bucle (4-6), losa en la cumbre (7+).

LENGUAJE_MODOS = ['latitud', 'frio', 'templado', 'calido', 'mezcla']
LENGUAJES = ['frio', 'templado', 'calido']
LENG_FRIO, LENG_CALIDO = 0.6, 0.25          # latitud relativa, como los biomas
MUTACION_FUENTES = ['manual', 'saturacion']
FIJAR_TIPOS = ['auto', '1', '2', '3']
AVANCE_OBRA = ['gates', 'pasos']

TIPOS = dict(informal=['caseta', 'casa', 'tresplantas', 'racimo', 'barrio', 'torre'],
             planificada=['pabellon', 'bloque', 'manzana', 'podio', 'rascacielos'])
DISENOS_TIPO = dict(caseta=['chabola', 'contenedor', 'cubo'], casa=['laje'], tresplantas=['voladizo'],
                    racimo=['racimo'], barrio=['kowloon'], torre=['dentada'],
                    pabellon=['sierra', 'pilotis'], bloque=['lamina', 'punto', 'hache'],
                    manzana=['cerda', 'peine'], podio=['podio'],
                    rascacielos=['deco', 'tubos', 'torsion', 'prisma'])
# fase 11 v11 (motor v68): la industria. La mina (SEQ1) cava, en racimo oblicuo; la
# energia (SEQ2) transforma, en malla ortogonal
TIPOS.update(mina=['brote', 'mina', 'complejo', 'fundicion', 'refineria'],
             energia=['aserradero', 'serreria', 'fabrica', 'termica', 'central'])
DISENOS_TIPO.update(brote=['bocamina', 'balancin', 'cantera'], mina=['castillete', 'balancines', 'trituradora'],
                    complejo=['lavadero'], fundicion=['altohorno'], refineria=['refineria'],
                    aserradero=['aserradero', 'secadero'], serreria=['serreria'], fabrica=['papelera'],
                    termica=['termica'], central=['central'])
PIEZAS_IND = ['torreref', 'chimenea', 'calderas']    # torres del cluster, testigo y calderas de la corta
TIPO_DE_DISENO = dict((d, t) for t, ds in DISENOS_TIPO.items() for d in ds)
PASOS_OBRA = ['solar', 'excavacion', 'nucleo', 'esqueleto', 'fachada', 'coronacion', 'bloque', 'estructura',
              'montaje', 'puesta']
PIEZAS_EDI = ['cuarto', 'capsula', 'zocalo']     # parasitos, capsulas y el zocalo de los puentes
DISENOS = [d for t in TIPOS['informal'] + TIPOS['planificada'] for d in DISENOS_TIPO[t]] + PIEZAS_EDI
DISENOS_IND = [d for t in TIPOS['mina'] + TIPOS['energia'] for d in DISENOS_TIPO[t]] + PIEZAS_IND
DISENOS = DISENOS + DISENOS_IND
INDUSTRIALES = set(DISENOS_IND)
INFORMALES = set(d for t in TIPOS['informal'] for d in DISENOS_TIPO[t]) | {'cuarto'}
RASCACIELOS = DISENOS_TIPO['rascacielos']
# formas del catalogo que no son ejemplares: los hibridos y las piezas del cluster
CIUDAD_FORMAS = ['colonia', 'marco', 'pasarela', 'bucle', 'losa', 'pasarelas', 'corredores', 'kowloon',
                 'corta', 'integrada', 'cuenca', 'torre compartida', 'fila de torres', 'anillo de torres']
FACHADAS = ['ciega', 'reticula', 'irregular', 'corona', 'zocalo', 'capsula', 'loggia', 'sierra',
            'incandescente', 'bandas', 'celosia']
F_CIEGA, F_RETICULA, F_IRREGULAR, F_CORONA, F_ZOCALO, F_CAPSULA, F_LOGGIA, F_SIERRA = range(8)
F_INCANDESCENTE, F_BANDAS, F_CELOSIA = 8, 9, 10     # industria: colada, chimenea con bandas, celosia
# materias (slots): 0-3 las plantas informales (cada una de un color), 4 cubierta o
# estructura informal, 5 cuerpo planificado, 6 piedra o zocalo, 7 estructura
SLOT_TECHO, SLOT_CUERPO, SLOT_PIEDRA, SLOT_ESTRUCTURA = 4, 5, 6, 7
# PALETA[lenguaje][slot]: el albedo de la ciudad es suyo (ni concha ni tinte). Sin el
# azul de los rios ni el cian de las cicatrices. El shader lleva la misma tabla.
PALETA_CIUDAD = (
    # frio: hormigon y chapa
    ((0.62, 0.63, 0.62), (0.52, 0.32, 0.22), (0.72, 0.58, 0.36), (0.62, 0.24, 0.19),
     (0.30, 0.30, 0.31), (0.66, 0.64, 0.60), (0.46, 0.45, 0.43), (0.34, 0.34, 0.35)),
    # templado: ladrillo y vidrio
    ((0.62, 0.32, 0.22), (0.55, 0.55, 0.53), (0.80, 0.56, 0.52), (0.56, 0.60, 0.38),
     (0.36, 0.29, 0.25), (0.17, 0.18, 0.18), (0.60, 0.31, 0.22), (0.40, 0.40, 0.41)),
    # calido: cal y celosia
    ((0.92, 0.90, 0.85), (0.71, 0.53, 0.38), (0.90, 0.76, 0.40), (0.90, 0.68, 0.62),
     (0.64, 0.52, 0.42), (0.90, 0.89, 0.86), (0.81, 0.74, 0.62), (0.55, 0.42, 0.30)),
    # industria (fase 11 v11), por epoca. Materias: ladrillo u obra, estructura, oxido,
    # hormigon de torre, cubierta, cuerpo de nave, bandas de chimenea, tuberias.
    # vapor: ladrillo rojo, hierro remachado y madera
    ((0.55, 0.24, 0.17), (0.16, 0.15, 0.14), (0.50, 0.28, 0.16), (0.70, 0.68, 0.64),
     (0.20, 0.18, 0.17), (0.58, 0.27, 0.19), (0.62, 0.22, 0.16), (0.42, 0.30, 0.20)),
    # acero: hormigon y acero pintado
    ((0.60, 0.59, 0.56), (0.42, 0.44, 0.40), (0.52, 0.30, 0.18), (0.78, 0.77, 0.74),
     (0.28, 0.28, 0.29), (0.55, 0.56, 0.54), (0.78, 0.24, 0.20), (0.85, 0.70, 0.20)),
    # quimica: acero blanco, aluminio y tuberias de colores
    ((0.88, 0.88, 0.86), (0.78, 0.79, 0.80), (0.55, 0.33, 0.20), (0.90, 0.90, 0.88),
     (0.60, 0.61, 0.62), (0.92, 0.92, 0.90), (0.85, 0.26, 0.20), (0.90, 0.50, 0.15)),
)
PALETA_IND = 3               # las filas de la industria empiezan aqui (3 + epoca)
COL_BLOQUE = (0.56, 0.56, 0.54)          # bloque gris sin revocar
COL_REMATE = dict(deposito=(0.10, 0.10, 0.11), antena=(0.36, 0.36, 0.38), maquinaria=(0.46, 0.46, 0.47),
                  varillas=(0.42, 0.24, 0.16), escalera=(0.50, 0.48, 0.45), cable=(0.06, 0.06, 0.06),
                  toldo=(0.80, 0.30, 0.20), chimenea=(0.40, 0.30, 0.26), bidon=(0.30, 0.42, 0.20),
                  mastil=(0.30, 0.30, 0.32), vallacima=(0.55, 0.52, 0.46), pergola=(0.55, 0.42, 0.30),
                  sierra=(0.48, 0.48, 0.50), aguja=(0.78, 0.74, 0.64), pasarela=(0.40, 0.38, 0.36),
                  corredor=(0.52, 0.42, 0.32), losa=(0.72, 0.72, 0.70), bucle=(0.20, 0.21, 0.22),
                  marco=(0.62, 0.62, 0.64), pilar=(0.58, 0.58, 0.60), nucleo=(0.60, 0.59, 0.56),
                  tierra=(0.42, 0.33, 0.24), balcon=(0.70, 0.66, 0.56), pretil=(0.85, 0.83, 0.78),
                  # industria (fase 11 v11)
                  terril=(0.10, 0.10, 0.10), vagoneta=(0.12, 0.11, 0.10), railes=(0.30, 0.28, 0.26),
                  polea=(0.20, 0.19, 0.18), balancin=(0.90, 0.72, 0.16), tuberia=(0.80, 0.55, 0.15),
                  cinta=(0.30, 0.30, 0.30), troncos=(0.48, 0.32, 0.18), tablones=(0.70, 0.55, 0.36),
                  portico=(0.92, 0.75, 0.15), ciclon=(0.70, 0.70, 0.68), subestacion=(0.55, 0.55, 0.56),
                  rotopala=(0.85, 0.66, 0.18), unagua=(0.4, 0.4, 0.4), dosaguas=(0.4, 0.4, 0.4))
COL_BALIZA = (1.0, 0.18, 0.08)           # la baliza de la grua (particula)
REMATES_LOD = ('varillas', 'escalera', 'cable', 'toldo', 'bidon', 'chimenea', 'pretil', 'balcon')
H_TOPE = 2.1                 # ningun edificio pasa de 2,1 x el limite (la camara lo encuadra)
HUECO_FACHADA = 0.95
FUENTES = ('humo', 'penacho', 'llama', 'baliza')     # industria: de donde sale el humo (particulas)
MOVILES = ('polea', 'balancin', 'rotopala')          # industria: las partes que se mueven al tempo


def _v(x, z, w, d, y0, y1, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.5, giro=0.0, forma='rect',
       hm=1.0, vm=1.0, pila=-1, top=1.0, rol=''):
    """Un volumen de la gramatica: planta (rect, oct o cil: un cilindro de 12
    lados) de w x d centrada en x z, de y0 a y1 en plantas, girada 'giro'
    grados; 'top' estrecha la tapa (troncos de cono, hiperboloides, taludes);
    datos de fachada; 'rol' (industria: nave, calderas, chimenea...)."""
    return dict(x=x, z=z, w=w, d=d, y0=y0, y1=y1, fach=fach, slot=slot, hueco=hueco, giro=giro,
                forma=forma, hm=hm, vm=vm, pila=pila, top=top, rol=rol)


def _rem(tipo, x, y, z, s=0.08, alto=1.0, giro=0.0, vol=-1, largo=None):
    """Un punto de remate: tipo, posicion (y en plantas), tamano (s en fraccion de
    celda, alto en plantas), giro y el volumen sobre el que va (-1 ninguno; en la
    informal por corte solo se ve si su volumen se ve; -2: la cima visible de la
    pila 0). 'largo' (fraccion de celda) para los remates que unen dos puntos."""
    return dict(tipo=tipo, x=x, y=y, z=z, s=s, alto=alto, giro=giro, vol=vol, largo=largo)


class _Gram(object):
    """Lo que necesita la gramatica de un diseno: la semilla y los parametros."""

    def __init__(self, diseno, var, cfg):
        import random
        self.d, self.var = diseno, int(var)
        self.rng = random.Random(104729 * (DISENOS.index(diseno) + 1) + 7919 * int(var) + 31)
        self.base = random.Random(15485863 + 7919 * int(var))     # lo que comparten las etapas
        self.obl = max(0.0, float(cfg.get('oblicuidad', 6.0)))
        self.ret = max(0.0, min(0.4, float(cfg.get('retranqueo', 0.15))))
        self.tor = max(0.0, float(cfg.get('torsion_max', 90.0)))
        self.vols, self.rem = [], []

    def u(self, a=0.0, b=1.0, r=None):
        return a + (b - a) * (r or self.rng).random()

    def add(self, v):
        self.vols.append(v)
        return len(self.vols) - 1


def _cuarto0(G):
    """El primer cuarto de la casa informal de la variante: el mismo en la casa
    que crece, la de tres plantas y la torre autoconstruida (la continuidad)."""
    r = G.base
    return _v(G.u(-0.04, 0.04, r), G.u(-0.04, 0.04, r), G.u(0.30, 0.36, r), G.u(0.26, 0.32, r), 0.0, 1.0,
              fach=F_IRREGULAR, slot=int(G.u(0, 3.99, r)), hueco=G.u(0.3, 0.5, r), pila=0)


def _pila(G, c0, n, desplaza=0.05, vuela=0.0, pila=0):
    """Cuartos apilados sobre c0: cada uno desplazado e inclinado (giro) hasta
    Oblicuidad; el de arriba vuela 'vuela' hacia la calle (+z)."""
    out = [c0]
    prev = c0
    for k in range(1, n):
        g = G.u(-G.obl, G.obl)
        q = _v(prev['x'] + G.u(-desplaza, desplaza), prev['z'] + G.u(-desplaza, desplaza),
               max(0.18, prev['w'] * G.u(0.88, 1.12)), max(0.16, prev['d'] * G.u(0.88, 1.12)),
               prev['y1'], prev['y1'] + 1.0, fach=F_IRREGULAR, slot=(c0['slot'] + k) % 4,
               hueco=G.u(0.28, 0.6), giro=round(g, 1), pila=pila)
        if k == n - 1 and vuela:
            q['z'] += vuela
            q['d'] *= 1.12
        q['x'] = max(-0.5 + q['w'] / 2, min(0.5 - q['w'] / 2, q['x']))
        q['z'] = max(-0.5 + q['d'] / 2, min(0.5 - q['d'] / 2, q['z']))
        out.append(q)
        prev = q
    return out


def _gen_chabola(G):
    c = _v(0.0, 0.0, G.u(0.34, 0.42), G.u(0.28, 0.34), 0.0, 1.0, fach=F_IRREGULAR, slot=int(G.u(0, 3.99)),
           hueco=G.u(0.25, 0.4), pila=0)
    k = G.add(c)
    G.rem += [_rem('techo1', c['x'], 1.0, c['z'], s=c['w'] * 1.2, alto=0.3, vol=k),
              _rem('bidon', c['x'] + c['w'] * 0.62, 0.0, c['z'] + 0.05, s=0.06, alto=0.6, vol=k)]


def _gen_contenedor(G):
    c = _v(0.0, 0.0, G.u(0.48, 0.56), G.u(0.2, 0.24), 0.0, 1.0, fach=F_IRREGULAR, slot=int(G.u(0, 3.99)),
           hueco=0.3, hm=0.9, pila=0)
    k = G.add(c)
    G.rem += [_rem('toldo', c['x'], 0.75, c['z'] + c['d'] * 0.5 + 0.06, s=c['w'] * 0.7, alto=0.12, vol=k),
              _rem('bidon', c['x'] - c['w'] * 0.6, 0.0, c['z'], s=0.05, alto=0.6, vol=k)]


def _gen_cubo(G):
    s = G.u(0.28, 0.32)
    c = _v(0.0, 0.0, s, s, 0.0, 1.0, fach=F_IRREGULAR, slot=0, hueco=0.3, pila=0)
    k = G.add(c)
    G.rem += [_rem('pretil', 0.0, 1.0, 0.0, s=s, alto=0.18, vol=k),
              _rem('escalera', s * 0.55, 0.0, 0.0, s=0.06, alto=1.0, giro=90.0, vol=k),
              _rem('techo', 0.0, 1.0, 0.0, s=s, alto=0.3, vol=k)]


def _gen_laje(G):
    c = _cuarto0(G)
    k = G.add(c)
    G.add(_v(c['x'], c['z'], c['w'] * 1.12, c['d'] * 1.12, 1.0, 1.1, fach=F_CIEGA, slot=SLOT_TECHO, pila=0))
    G.rem += [_rem('varillas', c['x'], 1.1, c['z'], s=c['w'] * 0.9, alto=0.45, vol=k),
              _rem('deposito', c['x'] - c['w'] * 0.25, 1.1, c['z'] - c['d'] * 0.2, s=0.07, alto=0.35, vol=k),
              _rem('escalera', c['x'] + c['w'] * 0.6, 0.0, c['z'], s=0.05, alto=1.1, giro=90.0, vol=k),
              _rem('techo', c['x'], 1.1, c['z'], s=c['w'], alto=0.3, vol=k)]


def _gen_voladizo(G):
    cs = _pila(G, _cuarto0(G), 3, desplaza=0.03, vuela=0.09)
    ks = [G.add(c) for c in cs]
    m = cs[1]
    G.add(_v(m['x'], m['z'] + m['d'] * 0.5 + 0.035, m['w'] * 0.5, 0.07, 1.15, 1.85, fach=F_IRREGULAR,
             slot=(m['slot'] + 2) % 4, hueco=0.6, giro=m['giro'], pila=1))
    t = cs[-1]
    G.rem += [_rem('antena', t['x'] + 0.05, 3.0, t['z'], s=0.04, alto=1.2, vol=ks[-1]),
              _rem('varillas', t['x'], 3.0, t['z'], s=t['w'] * 0.8, alto=0.4, vol=ks[-1]),
              _rem('techo', t['x'], 3.0, t['z'], s=t['w'], alto=0.3, vol=ks[-1])]


def _gen_racimo(G):
    """Casas escalonadas hacia las vecinas, con pasarelas, cables y toldos."""
    casas = []
    n = 5
    for k in range(n):
        a = 2 * math.pi * k / n + G.u(-0.3, 0.3)
        r = 0.0 if k == 0 else G.u(0.22, 0.3)
        x, z = r * math.cos(a), r * math.sin(a)
        alto = 4 if k == 0 else int(G.u(2, 3.99))
        c0 = _v(x, z, G.u(0.2, 0.26), G.u(0.18, 0.24), 0.0, 1.0, fach=F_IRREGULAR, slot=int(G.u(0, 3.99)),
                hueco=G.u(0.3, 0.5), giro=round(G.u(-G.obl, G.obl), 1), pila=k)
        cs = _pila(G, c0, alto, desplaza=0.025, pila=k)
        ks = [G.add(c) for c in cs]
        casas.append((cs[-1], ks[-1]))
        G.rem.append(_rem('techo', cs[-1]['x'], cs[-1]['y1'], cs[-1]['z'], s=cs[-1]['w'], alto=0.3, vol=ks[-1]))
        if k:
            G.rem.append(_rem('toldo', x, 0.8, z + 0.12, s=0.12, alto=0.1, vol=ks[0]))
    for k in range(1, n):                       # pasarelas y cables entre azoteas
        a, ka = casas[0]
        b, kb = casas[k]
        y = min(a['y1'], b['y1'])
        dx, dz = b['x'] - a['x'], b['z'] - a['z']
        largo = math.sqrt(dx * dx + dz * dz)
        g = math.degrees(math.atan2(dx, dz))
        G.rem.append(_rem('pasarela' if k % 2 else 'cable', a['x'] + dx / 2, y - 0.1, a['z'] + dz / 2,
                          s=0.04, alto=0.08, giro=g, vol=kb, largo=largo))
    G.rem.append(_rem('antena', casas[0][0]['x'], casas[0][0]['y1'], casas[0][0]['z'], s=0.04, alto=1.4,
                      vol=casas[0][1]))


def _gen_kowloon(G):
    """Masa continua de alturas parecidas, con callejones como grietas."""
    g = 4
    lado = 0.9
    callejon = 0.035
    paso = lado / g
    for a in range(g):
        for b in range(g):
            x = -lado / 2 + paso * (a + 0.5) + G.u(-0.01, 0.01)
            z = -lado / 2 + paso * (b + 0.5) + G.u(-0.01, 0.01)
            alto = int(G.u(4, 6.99))
            k = G.add(_v(x, z, paso - callejon, paso - callejon * G.u(0.6, 1.4), 0.0, float(alto),
                         fach=F_IRREGULAR, slot=int(G.u(0, 3.99)), hueco=G.u(0.3, 0.55), pila=a * g + b))
            q = G.u()
            if q < 0.45:
                G.rem.append(_rem('antena', x + G.u(-0.03, 0.03), alto, z, s=0.03, alto=1.0 + G.u(), vol=k))
            if q > 0.3:
                G.rem.append(_rem('deposito', x - 0.04, alto, z + 0.03, s=0.06, alto=0.35, vol=k))
            if q > 0.75:
                G.rem.append(_rem('cable', x + paso / 2, alto - 0.3, z, s=0.02, alto=0.04, giro=90.0, vol=k,
                                  largo=paso))


def _gen_dentada(G):
    """Torre autoconstruida: cuartos apilados en voladizo, cada uno desplazado
    del de abajo, con mastil de antenas y valla en la cima (en la cima visible)."""
    cs = _pila(G, _cuarto0(G), 16, desplaza=0.06)
    for c in cs:
        G.add(c)
    G.rem += [_rem('mastil', 0.03, 0.0, 0.0, s=0.05, alto=2.4, vol=-2),
              _rem('vallacima', 0.0, 0.0, 0.0, s=0.3, alto=0.3, vol=-2),
              _rem('varillas', 0.0, 0.0, 0.0, s=0.26, alto=0.4, vol=-2)]


def _gen_cuarto(G):
    G.add(_v(0.0, 0.0, 1.0, 1.0, 0.0, 1.0, fach=F_IRREGULAR, slot=int(G.u(0, 3.99)), hueco=G.u(0.3, 0.55),
             pila=0))


def _gen_capsula(G):
    G.add(_v(0.0, 0.0, 1.0, 1.0, 0.0, 1.0, fach=F_CAPSULA, slot=SLOT_CUERPO, hueco=0.6))


def _gen_zocalo(G):
    G.add(_v(0.0, 0.5, 1.0, 1.0, 0.0, 1.0, fach=F_ZOCALO, slot=SLOT_PIEDRA, hueco=0.8, hm=1.0))


def _gen_sierra(G):
    w, d = G.u(0.62, 0.74), G.u(0.44, 0.52)
    k = G.add(_v(0.0, 0.0, w, d, 0.0, 1.6, fach=F_SIERRA, slot=SLOT_CUERPO, hueco=0.7, hm=1.6))
    G.rem.append(_rem('sierra', 0.0, 1.6, 0.0, s=w, alto=0.5, vol=k, largo=d))


def _gen_pilotis(G):
    w, d = G.u(0.62, 0.72), G.u(0.3, 0.36)
    for a in (-1, 0, 1):
        for b in (-1, 1):
            G.add(_v(a * w * 0.42, b * d * 0.32, 0.035, 0.035, 0.0, 1.0, fach=F_CIEGA, slot=SLOT_ESTRUCTURA))
    k = G.add(_v(0.0, 0.0, w, d, 1.0, 2.2, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.85, vm=2.5))
    G.rem.append(_rem('cubierta', 0.0, 2.2, 0.0, s=0.18, alto=0.3, vol=k))


def _gen_lamina(G):
    w, d = G.u(0.78, 0.86), G.u(0.18, 0.22)
    for a in range(-2, 3):
        G.add(_v(a * w * 0.2, 0.0, 0.05, d * 0.6, 0.0, 1.0, fach=F_CIEGA, slot=SLOT_ESTRUCTURA))
    k = G.add(_v(0.0, 0.0, w, d, 1.0, 8.0, fach=F_LOGGIA, slot=SLOT_CUERPO, hueco=0.7, vm=1.6))
    G.rem += [_rem('maquinaria', -w * 0.3, 8.0, 0.0, s=0.08, alto=0.6, vol=k),
              _rem('maquinaria', w * 0.25, 8.0, 0.0, s=0.06, alto=0.9, vol=k),
              _rem('cubierta', 0.0, 8.0, 0.0, s=0.15, alto=0.3, vol=k)]


def _punto(G, x, z, s, y0, y1, r=None):
    """La torre-punto de la variante: la misma en el bloque y en el podio."""
    r = r or G.base
    s = s * G.u(0.92, 1.08, r)
    return _v(x, z, s, s, y0, y1, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=G.u(0.45, 0.6, r), hm=-1.0)


def _gen_punto(G):
    k = G.add(_punto(G, 0.0, 0.0, 0.34, 0.0, 9.0))
    G.rem += [_rem('maquinaria', 0.05, 9.0, -0.04, s=0.1, alto=0.6, vol=k),
              _rem('antena', -0.08, 9.0, 0.06, s=0.03, alto=1.5, vol=k),
              _rem('cubierta', 0.0, 9.0, 0.0, s=0.12, alto=0.3, vol=k)]


def _gen_hache(G):
    w = G.u(0.18, 0.22)
    for x in (-0.3, 0.3):
        G.add(_v(x, 0.0, w, 0.8, 0.0, 7.0, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.5))
    k = G.add(_v(0.0, 0.0, 0.42, 0.2, 0.0, 7.0, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.5, hm=-1.0))
    G.rem += [_rem('maquinaria', 0.0, 7.0, 0.0, s=0.1, alto=0.5, vol=k),
              _rem('cubierta', 0.3, 7.0, 0.2, s=0.12, alto=0.3, vol=0)]


def _gen_cerda(G):
    """Manzana cerrada con chaflanes y patio: desde arriba, un octogono hueco."""
    a, t = 0.42, G.u(0.11, 0.14)
    c = 0.13
    alto = 6.0
    largo = 2 * (a - c)
    for (x, z, w, d) in ((0.0, a - t / 2, largo, t), (0.0, -a + t / 2, largo, t),
                         (a - t / 2, 0.0, t, largo), (-a + t / 2, 0.0, t, largo)):
        G.add(_v(x, z, w, d, 0.0, alto, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.5, hm=-1.0))
    for sx in (-1, 1):
        for sz in (-1, 1):
            G.add(_v(sx * (a - c * 0.55), sz * (a - c * 0.55), c * 1.5, t, 0.0, alto, fach=F_RETICULA,
                     slot=SLOT_CUERPO, hueco=0.5, giro=45.0 * sx * sz, hm=-1.0))
    G.rem.append(_rem('cubierta', 0.0, alto, a - t / 2, s=0.1, alto=0.3, vol=0))


def _gen_peine(G):
    G.add(_v(-0.36, 0.0, 0.14, 0.86, 0.0, 5.0, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.5, hm=-1.0))
    for z in (-0.32, 0.0, 0.32):
        G.add(_v(0.06, z, 0.72, G.u(0.11, 0.13), 0.0, 5.0 + (1.0 if z == 0.0 else 0.0), fach=F_RETICULA,
                 slot=SLOT_CUERPO, hueco=0.55))
    G.rem.append(_rem('cubierta', 0.06, 6.0, 0.0, s=0.12, alto=0.3, vol=2))


def _gen_podio(G):
    k = G.add(_v(0.0, 0.0, 0.9, 0.9, 0.0, 2.0, fach=F_ZOCALO, slot=SLOT_PIEDRA, hueco=0.8))
    r = G.ret
    t1 = _punto(G, -0.18, -0.15, 0.34 * (1.0 - 0.6 * r), 2.0, 14.0)
    t2 = _punto(G, 0.22, 0.2, 0.26 * (1.0 - 0.6 * r), 2.0, 10.0, G.rng)
    k1, k2 = G.add(t1), G.add(t2)
    G.rem += [_rem('maquinaria', -0.18, 14.0, -0.15, s=0.08, alto=0.5, vol=k1),
              _rem('antena', 0.22, 10.0, 0.2, s=0.03, alto=1.2, vol=k2),
              _rem('cubierta', 0.3, 2.0, -0.3, s=0.12, alto=0.3, vol=k)]


def _gen_deco(G):
    """Escalonado con aguja: retranqueos art deco en piedra, la aguja arriba."""
    r = max(0.08, G.ret)
    w = G.u(0.42, 0.46)
    y = 0.0
    tramos = ((0.0, 7.0), (7.0, 12.0), (12.0, 16.0), (16.0, 19.0), (19.0, 21.0))
    k = 0
    for q, (y0, y1) in enumerate(tramos):
        s = w * max(0.12, 1.0 - 1.35 * r * q)
        k = G.add(_v(0.0, 0.0, s, s, y0, y1, fach=F_CORONA if q == 4 else F_RETICULA, slot=SLOT_PIEDRA,
                     hueco=0.42, vm=0.8))
        y = y1
    G.rem.append(_rem('aguja', 0.0, y, 0.0, s=0.05, alto=10.0, vol=k))


def _gen_tubos(G):
    """Haz de tubos de alturas distintas (Sears): el del centro, el mas alto."""
    s = 0.19
    # de frente se lee escalonado: una columna baja, la del centro la mas alta y otra media
    col = [[0.42, 0.5, 0.36], [0.82, 1.0, 0.7], [0.62, 0.74, 0.55]]
    if G.var % 2:
        col.reverse()
    altos = [col[q % 3][q // 3] * G.u(0.94, 1.0) if col[q % 3][q // 3] < 1.0 else 1.0 for q in range(9)]
    k = 0
    for q in range(9):
        a, b = q % 3 - 1, q // 3 - 1
        kk = G.add(_v(a * s, b * s, s, s, 0.0, round(26.0 * altos[q], 1), fach=F_RETICULA, slot=SLOT_CUERPO,
                      hueco=0.6, vm=0.9))
        if altos[q] == 1.0:
            k = kk
    G.rem += [_rem('antena', -0.02, 26.0, 0.0, s=0.03, alto=3.0, vol=k),
              _rem('antena', 0.03, 26.0, 0.02, s=0.03, alto=2.4, vol=k)]


def _gen_torsion(G):
    """Torsionada: rodajas que giran hasta Torsionmax."""
    n = 13
    s = G.u(0.27, 0.3)
    alto = 28.0
    for q in range(n):
        f = 1.0 - 0.15 * q / (n - 1)          # esbelta, apenas se afila mientras gira
        G.add(_v(0.0, 0.0, s * f, s * 0.8 * f, alto * q / n, alto * (q + 1) / n,
                 fach=F_CORONA if q == n - 1 else F_RETICULA, slot=SLOT_CUERPO, hueco=0.65, forma='oct',
                 giro=round(G.tor * q / (n - 1), 1), vm=0.9))
    G.rem.append(_rem('antena', 0.0, alto, 0.0, s=0.03, alto=1.6, vol=n - 1))


def _gen_prisma(G):
    """Prisma con corona iluminada."""
    s = G.u(0.62, 0.68)
    G.add(_v(0.0, 0.0, s, s * 0.32, 0.0, 19.0, fach=F_RETICULA, slot=SLOT_CUERPO, hueco=0.6, hm=-1.0))
    G.add(_v(0.0, 0.0, s * 0.94, s * 0.28, 19.0, 22.0, fach=F_CORONA, slot=SLOT_CUERPO, hueco=0.8))


# --- la industria (fase 11 v11, motor v68): las piezas de ingenieria --------------
# Aqui si valen las primitivas (cilindros, celosias, hiperboloides, troncos de
# cono), pero ninguna va desnuda: cada pieza lleva su rasgo de lectura (anillos,
# celosia, penacho, llama). Materias de la industria: 0 ladrillo u obra, 1
# estructura metalica, 2 oxido, 3 hormigon de torre, 4 cubierta, 5 cuerpo de nave,
# 6 bandas de chimenea, 7 tuberias de color (la paleta, por epoca). Fuentes: 'humo'
# (chimenea), 'penacho' (torre de refrigeracion) y 'llama' (antorcha).

def _cil(G, x, z, r, y0, y1, slot=1, fach=F_CIEGA, top=1.0, rol='', hueco=0.5):
    return G.add(_v(x, z, 2 * r, 2 * r, y0, y1, fach=fach, slot=slot, forma='cil', top=top, rol=rol,
                    hueco=hueco))


def _chimenea(G, x, z, r, alto, slot=6, rol='chimenea', balizas=False):
    """Chimenea con bandas (y balizas): un tronco de cono; la fuente de humo arriba."""
    k = _cil(G, x, z, r, 0.0, alto, slot=slot, fach=F_BANDAS, top=0.7, rol=rol)
    G.rem.append(_rem('humo', x, alto, z, s=r * 1.4, alto=0.0, vol=k))
    if balizas:
        G.rem.append(_rem('baliza', x, alto * 0.98, z, s=r, alto=0.0, vol=k))
    return k


def _torre_ref(G, x, z, r, alto, rol='torre'):
    """Torre de refrigeracion: un hiperboloide de seis rodajas (la cintura a los
    dos tercios) con el penacho arriba."""
    perfil = [1.0, 0.86, 0.76, 0.70, 0.69, 0.72, 0.78]
    k = 0
    for q in range(6):
        k = _cil(G, x, z, r * perfil[q], alto * q / 6.0, alto * (q + 1) / 6.0, slot=3,
                 top=perfil[q + 1] / perfil[q], rol=rol)
    G.rem.append(_rem('penacho', x, alto, z, s=r * 1.5, alto=0.0, vol=k))
    return k


def _castillete(G, x, z, alto, giro=0.0, rol='castillete'):
    """El castillete: torre de celosia inclinada con dos poleas (la A con ruedas)."""
    k = G.add(_v(x, z, 0.12, 0.12, 0.0, alto, fach=F_CELOSIA, slot=1, top=0.55, giro=giro, rol=rol))
    G.add(_v(x + 0.09, z, 0.03, 0.10, 0.0, alto * 0.8, fach=F_CELOSIA, slot=1, giro=giro - 25.0, rol=rol))
    for dz in (-0.03, 0.03):
        G.rem.append(_rem('polea', x, alto, z + dz, s=0.07, alto=0.8, giro=giro, vol=k))
    return k


def _gen_bocamina(G):
    k = G.add(_v(0.0, -0.08, 0.6, 0.42, 0.0, 1.6, fach=F_CIEGA, slot=4, top=0.55, rol='talud'))
    G.add(_v(0.0, 0.16, 0.12, 0.08, 0.0, 0.6, fach=F_CIEGA, slot=1, rol='galeria'))
    G.rem += [_rem('vagoneta', 0.08, 0.0, 0.3, s=0.07, alto=0.45, vol=k),
              _rem('railes', 0.0, 0.0, 0.32, s=0.06, alto=0.05, largo=0.36, vol=k),
              _rem('terril', -0.3, 0.0, 0.3, s=0.2, alto=1.0, vol=k)]


def _gen_balancin(G):
    for q, (x, z) in enumerate(((0.0, 0.0), (0.24, 0.2))[:1 + G.var % 2]):
        G.add(_v(x, z, 0.22, 0.08, 0.0, 0.3, fach=F_CIEGA, slot=1, rol='base'))
        k = G.add(_v(x, z, 0.04, 0.06, 0.3, 1.5, fach=F_CELOSIA, slot=7, top=0.6, rol='poste'))
        G.rem.append(_rem('balancin', x, 1.5, z, s=0.26, alto=0.5, vol=k))
    kt = _cil(G, -0.26, -0.18, 0.08, 0.0, 0.9, slot=2, rol='tanque')
    G.rem.append(_rem('terril', 0.28, 0.0, -0.26, s=0.14, alto=0.6, vol=kt))


def _gen_cantera(G):
    for q in range(3):
        G.add(_v(0.0, 0.0, 0.62 - 0.14 * q, 0.5 - 0.12 * q, 0.5 * q, 0.5 * q + 0.5, fach=F_CIEGA, slot=2,
                 top=0.9, rol='banco'))
    G.rem += [_rem('mastil', 0.2, 1.5, 0.1, s=0.06, alto=1.6, vol=2),
              _rem('terril', -0.32, 0.0, 0.3, s=0.18, alto=0.8, vol=0)]


def _gen_castillete(G):
    _castillete(G, -0.12, 0.0, 6.0, giro=round(G.u(-G.obl, G.obl), 1))
    G.add(_v(0.14, 0.0, 0.26, 0.22, 0.0, 2.2, fach=F_RETICULA, slot=0, hueco=0.35, rol='maquinas'))
    G.rem += [_rem('terril', 0.22, 0.0, 0.3, s=0.26, alto=2.2, vol=0),
              _rem('vagoneta', -0.1, 0.0, 0.24, s=0.06, alto=0.4, vol=0)]


def _gen_balancines(G):
    for q in range(3):
        x, z = -0.3 + 0.3 * q, -0.2 + 0.18 * (q % 2)
        G.add(_v(x, z, 0.2, 0.07, 0.0, 0.3, fach=F_CIEGA, slot=1, rol='base'))
        k = G.add(_v(x, z, 0.04, 0.05, 0.3, 1.5, fach=F_CELOSIA, slot=7, top=0.6, rol='poste'))
        G.rem.append(_rem('balancin', x, 1.5, z, s=0.24, alto=0.5, vol=k))
    for x in (-0.15, 0.15):
        _cil(G, x, 0.26, 0.09, 0.0, 1.2, slot=2, rol='tanque')


def _gen_trituradora(G):
    for q in range(2):
        G.add(_v(-0.2, -0.15, 0.4 - 0.12 * q, 0.34 - 0.1 * q, 0.5 * q, 0.5 * q + 0.5, fach=F_CIEGA, slot=2,
                 top=0.9, rol='banco'))
    k = G.add(_v(0.2, 0.15, 0.22, 0.2, 0.0, 2.0, fach=F_RETICULA, slot=5, hueco=0.3, rol='trituradora'))
    G.rem += [_rem('cinta', 0.0, 1.2, 0.0, s=0.04, alto=0.15, giro=40.0, vol=k, largo=0.5),
              _rem('terril', 0.3, 0.0, -0.28, s=0.18, alto=1.2, vol=k)]


def _gen_lavadero(G):
    """Complejo minero: lavadero en alto con tolvas, dos castilletes, cintas, terriles y cable."""
    k = G.add(_v(0.0, 0.0, 0.3, 0.22, 2.0, 4.0, fach=F_RETICULA, slot=5, hueco=0.35, rol='lavadero'))
    for x in (-0.11, 0.11):
        G.add(_v(x, 0.0, 0.04, 0.18, 0.0, 2.0, fach=F_CELOSIA, slot=1, rol='lavadero'))
    _castillete(G, -0.3, -0.24, 7.0, giro=round(G.u(-G.obl, G.obl), 1))
    _castillete(G, 0.28, -0.26, 6.0, giro=round(G.u(-G.obl, G.obl), 1))
    G.add(_v(-0.2, 0.26, 0.2, 0.16, 0.0, 1.6, fach=F_RETICULA, slot=0, hueco=0.35, rol='maquinas'))
    G.rem += [_rem('cinta', -0.15, 2.6, -0.12, s=0.04, alto=0.15, giro=-50.0, vol=k, largo=0.36),
              _rem('cinta', 0.15, 2.6, -0.12, s=0.04, alto=0.15, giro=50.0, vol=k, largo=0.36),
              _rem('terril', 0.32, 0.0, 0.3, s=0.28, alto=2.6, vol=k),
              _rem('terril', -0.36, 0.0, 0.08, s=0.22, alto=2.0, vol=k),
              _rem('cable', 0.0, 4.6, 0.3, s=0.02, alto=0.05, giro=90.0, vol=k, largo=0.9)]


def _gen_altohorno(G):
    """Fundicion: altos hornos (troncos de cono de oxido) con la colada
    incandescente al pie, estufas de aire caliente y tuberias de gas."""
    for x in ((0.0,) if G.var % 3 == 1 else (-0.14, 0.18)):
        _cil(G, x, -0.05, 0.035, 0.0, 0.5, slot=0, fach=F_INCANDESCENTE, rol='colada')
        _cil(G, x, -0.05, 0.1, 0.5, 3.5, slot=2, top=0.62, rol='horno')
        _cil(G, x, -0.05, 0.06, 3.5, 5.0, slot=1, top=0.8, rol='horno')
    for q in range(3):
        _cil(G, -0.28 + 0.14 * q, 0.26, 0.055, 0.0, 4.2, slot=1, rol='estufa')
    G.rem += [_rem('tuberia', 0.0, 4.2, 0.12, s=0.03, alto=0.1, giro=30.0, vol=0, largo=0.4),
              _rem('tuberia', 0.1, 3.2, 0.2, s=0.03, alto=0.1, giro=-35.0, vol=0, largo=0.3),
              _rem('humo', 0.18, 5.0, -0.05, s=0.12, alto=0.0, vol=0)]


def _gen_refineria(G):
    """Refineria: haz de columnas de destilacion, bastidores de tuberias, tanques
    de techo flotante y la antorcha con su llama."""
    altos = [11.0, 9.0, 13.0, 8.0, 10.0]
    for q, a in enumerate(altos[:3 + G.var % 3]):
        _cil(G, -0.22 + 0.09 * q, -0.12 + 0.05 * (q % 2), 0.035, 0.0, a, slot=3, rol='columna')
    G.add(_v(0.0, 0.08, 0.5, 0.08, 0.0, 2.2, fach=F_CELOSIA, slot=7, rol='bastidor'))
    for x, z in ((0.24, 0.26), (-0.08, 0.3), (0.3, -0.12)):
        _cil(G, x, z, 0.1, 0.0, 0.9, slot=3, rol='tanque')
    k = _cil(G, 0.36, 0.36, 0.015, 0.0, 14.0, slot=1, rol='antorcha')
    G.rem.append(_rem('llama', 0.36, 14.0, 0.36, s=0.06, alto=0.0, vol=k))


def _gen_aserradero(G):
    for x in (-0.2, 0.2):
        for z in (-0.14, 0.14):
            G.add(_v(x, z, 0.03, 0.03, 0.0, 1.2, fach=F_CIEGA, slot=7, rol='cobertizo'))
    k = G.add(_v(0.0, 0.0, 0.08, 0.06, 0.0, 0.5, fach=F_CIEGA, slot=1, rol='sierra'))
    G.rem += [_rem('dosaguas', 0.0, 1.2, 0.0, s=0.48, alto=0.6, vol=k, largo=0.36),
              _rem('troncos', -0.1, 0.0, 0.3, s=0.3, alto=0.5, vol=k),
              _rem('tablones', 0.28, 0.0, -0.3, s=0.2, alto=0.3, vol=k)]


def _gen_secadero(G):
    for q in range(4):
        G.add(_v(-0.3 + 0.2 * q, 0.0, 0.16, 0.3, 0.0, 1.0, fach=F_CIEGA, slot=0, rol='horno'))
    _chimenea(G, 0.36, 0.24, 0.035, 2.6, slot=0)
    G.rem.append(_rem('troncos', 0.0, 0.0, 0.32, s=0.4, alto=0.5, vol=0))


def _gen_serreria(G):
    G.add(_v(0.0, -0.14, 0.5, 0.26, 0.0, 1.8, fach=F_SIERRA, slot=5, hueco=0.6, rol='nave'))
    k = _cil(G, 0.32, 0.22, 0.08, 0.0, 2.4, slot=3, rol='silo')
    G.rem += [_rem('portico', 0.0, 0.0, 0.26, s=0.5, alto=2.2, vol=k, largo=0.3),
              _rem('troncos', -0.1, 0.0, 0.26, s=0.36, alto=0.5, vol=k),
              _rem('ciclon', 0.32, 2.4, 0.22, s=0.12, alto=0.8, vol=k),
              _rem('cinta', 0.16, 1.2, 0.06, s=0.03, alto=0.1, giro=-40.0, vol=k, largo=0.3)]


def _gen_papelera(G):
    """Fabrica: naves en peine con dientes de sierra, chimenea de ladrillo y depositos."""
    for q in range(3):
        k = G.add(_v(-0.1, -0.3 + 0.2 * q, 0.56, 0.17, 0.0, 1.8, fach=F_SIERRA, slot=5, hueco=0.6, rol='nave'))
        G.rem.append(_rem('sierra', -0.1, 1.8, -0.3 + 0.2 * q, s=0.56, alto=0.5, vol=k, largo=0.17))
    _chimenea(G, 0.32, 0.3, 0.04, 6.0, slot=0)
    for z in (-0.2, 0.05):
        _cil(G, 0.32, z, 0.07, 0.0, 1.4, slot=3, rol='deposito')


def _calderas(G, x, z, w, d, alto):
    return G.add(_v(x, z, w, d, 0.0, alto, fach=F_RETICULA, slot=5, hueco=0.4, rol='calderas'))


def _gen_termica(G):
    _calderas(G, -0.16, -0.08, 0.3, 0.26, 4.0)
    G.add(_v(-0.16, 0.18, 0.4, 0.16, 0.0, 2.0, fach=F_SIERRA, slot=5, hueco=0.6, rol='nave'))
    _chimenea(G, 0.06, -0.3, 0.045, 12.0)
    _torre_ref(G, 0.27, 0.18, 0.15, 5.0)
    G.rem += [_rem('terril', -0.34, 0.0, -0.32, s=0.2, alto=1.0, vol=0),
              _rem('cinta', -0.25, 1.4, -0.22, s=0.03, alto=0.1, giro=45.0, vol=0, largo=0.25)]


def _gen_central(G):
    """Central electrica: 2-4 torres de refrigeracion con penacho, chimenea muy alta
    con balizas, sala de turbinas y subestacion. De aqui nace la red."""
    n = 2 + G.var % 3
    sitios = [(0.22, 0.22), (-0.22, 0.24), (0.24, -0.2), (-0.02, 0.34)][:n]
    for x, z in sitios:
        _torre_ref(G, x, z, 0.13, 6.0)
    _calderas(G, -0.22, -0.16, 0.26, 0.22, 4.0)
    G.add(_v(-0.02, -0.3, 0.3, 0.12, 0.0, 2.4, fach=F_RETICULA, slot=5, hueco=0.5, rol='turbinas'))
    _chimenea(G, -0.36, 0.0, 0.035, 18.0, balizas=True)
    G.rem.append(_rem('subestacion', 0.3, 0.0, -0.36, s=0.18, alto=1.0, vol=0))


def _gen_torreref(G):
    _torre_ref(G, 0.0, 0.0, 0.45, 6.0)


def _gen_chimenea(G):
    _chimenea(G, 0.0, 0.0, 0.12, 12.0)


def _gen_calderas(G):
    _calderas(G, 0.0, 0.0, 0.8, 0.7, 4.0)


_GEN_IND = dict(bocamina=_gen_bocamina, balancin=_gen_balancin, cantera=_gen_cantera,
                castillete=_gen_castillete, balancines=_gen_balancines, trituradora=_gen_trituradora,
                lavadero=_gen_lavadero, altohorno=_gen_altohorno, refineria=_gen_refineria,
                aserradero=_gen_aserradero, secadero=_gen_secadero, serreria=_gen_serreria,
                papelera=_gen_papelera, termica=_gen_termica, central=_gen_central,
                torreref=_gen_torreref, chimenea=_gen_chimenea, calderas=_gen_calderas)


_GEN_EDI = dict(chabola=_gen_chabola, contenedor=_gen_contenedor, cubo=_gen_cubo, laje=_gen_laje,
                voladizo=_gen_voladizo, racimo=_gen_racimo, kowloon=_gen_kowloon, dentada=_gen_dentada,
                cuarto=_gen_cuarto, capsula=_gen_capsula, zocalo=_gen_zocalo, sierra=_gen_sierra,
                pilotis=_gen_pilotis, lamina=_gen_lamina, punto=_gen_punto, hache=_gen_hache,
                cerda=_gen_cerda, peine=_gen_peine, podio=_gen_podio, deco=_gen_deco, tubos=_gen_tubos,
                torsion=_gen_torsion, prisma=_gen_prisma)
_GEN_EDI.update(_GEN_IND)
_EDIFICIOS = {}


def _clave_ciudad(cfg):
    return (round(float(cfg.get('oblicuidad', 6.0)), 2), round(float(cfg.get('retranqueo', 0.15)), 3),
            round(float(cfg.get('torsion_max', 90.0)), 1))


def edificio(cfg, diseno, var):
    """El ejemplar (diseno, variante) de la biblioteca de la ciudad: volumenes y
    remates normalizados (alto 1; x z en fraccion de celda), su alto en plantas,
    el modo de crecer ('corte' la informal por cuartos, 'escala' el resto) y las
    pilas. Se calcula una vez por Oblicuidad, Retranqueo y Torsionmax."""
    k = (_clave_ciudad(cfg), diseno, int(var))
    e = _EDIFICIOS.get(k)
    if e is not None:
        return e
    if len(_EDIFICIOS) > 600:
        _EDIFICIOS.clear()
    G = _Gram(diseno, var, cfg)
    _GEN_EDI[diseno](G)
    alto = max(v['y1'] for v in G.vols)
    vols = []
    for v in G.vols:
        q = dict(v)
        q['y0'], q['y1'] = v['y0'] / alto, v['y1'] / alto
        vols.append(q)
    rem = []
    for r in G.rem:
        q = dict(r)
        q['y'] = r['y'] / alto
        q['alto'] = r['alto']               # en plantas: no escala con el edificio
        rem.append(q)
    xs = [abs(v['x']) + 0.5 * max(v['w'], v['d']) * (1.42 if v['giro'] else 1.0) for v in G.vols]
    e = _EDIFICIOS[k] = dict(diseno=diseno, var=int(var), vols=vols, rem=rem, alto=alto,
                             modo='corte' if diseno == 'dentada' else 'escala',
                             informal=diseno in INFORMALES, industrial=diseno in INDUSTRIALES,
                             fuentes=[r for r in rem if r['tipo'] in FUENTES], radio=min(0.5, max(xs)),
                             pilas=sorted(set(v['pila'] for v in G.vols)))
    return e


def variantes_ciudad(cfg):
    """Variantes por diseno: Variantesciudad, sin pasar de las que tienen geometria."""
    global VARIANTES_CIU_TD
    v = max(1, int(cfg.get('variantes_ciudad', 3)))
    if VARIANTES_CIU_TD is None:
        try:
            VARIANTES_CIU_TD = int(me.fetch('variantes_ciu_td', 0))
        except Exception:
            VARIANTES_CIU_TD = 0
    if VARIANTES_CIU_TD:
        v = min(v, VARIANTES_CIU_TD)
    return v


VARIANTES_CIU_TD = None
VARIANTES_IND_TD = None


def variantes_ind(cfg):
    """Variantes por diseno de la industria: Variantesind, sin pasar de las que tienen geometria."""
    global VARIANTES_IND_TD
    v = max(1, int(cfg.get('variantes_ind', 3)))
    if VARIANTES_IND_TD is None:
        try:
            VARIANTES_IND_TD = int(me.fetch('variantes_ind_td', 0))
        except Exception:
            VARIANTES_IND_TD = 0
    if VARIANTES_IND_TD:
        v = min(v, VARIANTES_IND_TD)
    return v


def variantes_de(cfg, diseno):
    return variantes_ind(cfg) if diseno in INDUSTRIALES else variantes_ciudad(cfg)


def biblioteca_ciudad(cfg):
    """Precalcula la biblioteca de la ciudad y la industria. Devuelve el numero de ejemplares."""
    n = 0
    for d in DISENOS:
        for v in range(variantes_de(cfg, d)):
            edificio(cfg, d, v)
            n += 1
    return n


def nombre_edificio(diseno, var):
    return 'edi_%s_%d' % (diseno, var)


def edificios_de(cfg):
    """Los nombres de los ejemplares de la ciudad que necesita TD."""
    return [nombre_edificio(d, v) for d in DISENOS for v in range(variantes_de(cfg, d))]


def es_edificio(nombre):
    if not nombre.startswith('edi_'):
        return False
    p = nombre[4:].split('_')
    return len(p) == 2 and p[0] in _GEN_EDI


def parte_edificio(nombre):
    p = nombre[4:].split('_')
    return p[0], int(p[1])


def _planta_vol(v):
    """Los vertices (x, z) de la planta de un volumen, en orden (antihorario
    visto desde arriba), girados y en su sitio."""
    w, d = v['w'] / 2.0, v['d'] / 2.0
    if v['forma'] in ('cil', 'cil6'):
        n = 12 if v['forma'] == 'cil' else 6
        pts = [(w * math.cos(2 * math.pi * k / n), d * math.sin(2 * math.pi * k / n)) for k in range(n)]
    elif v['forma'] == 'oct':
        c = 0.29 * min(w, d) * 2.0
        pts = [(-w + c, -d), (w - c, -d), (w, -d + c), (w, d - c), (w - c, d), (-w + c, d), (-w, d - c),
               (-w, -d + c)]
    else:
        pts = [(-w, -d), (w, -d), (w, d), (-w, d)]
    g = math.radians(v['giro'])
    cg, sg = math.cos(g), math.sin(g)
    return [(v['x'] + x * cg - z * sg, v['z'] + x * sg + z * cg) for x, z in pts]


def malla_edificio(nombre, cfg=None):
    """(puntos, normales, uv, triangulos) de un ejemplar de la ciudad para su
    Script SOP. uv = (10 + 8 x fachada + materia + 0,95 x hueco, alto de planta
    (x Alturaplanta; negativo: zocalo comercial en la planta baja), 4 x semilla +
    ancho de vano (x Anchovano)): el shader dibuja la fachada con eso."""
    cfg = cfg or DEFAULT_CFG
    clave = (nombre, _clave_ciudad(cfg))
    v = _MALLAS.get(clave)
    if v is not None:
        return v
    d, var = parte_edificio(nombre)
    e = edificio(cfg, d, var)
    P, Nn, U, T = [], [], [], []
    for q, vol in enumerate(e['vols']):
        semilla = int(_hash01(q + 7 * var, DISENOS.index(d)) * 63.0)
        uv = (10.0 + 8 * vol['fach'] + vol['slot'] + HUECO_FACHADA * max(0.0, min(1.0, vol['hueco'])),
              vol['hm'], 4.0 * semilla + max(0.05, min(3.9, vol['vm'])))
        pl = _planta_vol(vol)
        y0, y1 = vol['y0'], vol['y1']
        m = len(pl)
        tp = float(vol.get('top', 1.0))     # la tapa, estrechada hacia su centro
        pt = [(vol['x'] + (x - vol['x']) * tp, vol['z'] + (z - vol['z']) * tp) for x, z in pl]
        for k in range(m):                  # las caras de los lados
            a, b = pl[k], pl[(k + 1) % m]
            at, bt = pt[k], pt[(k + 1) % m]
            nx, nz = b[1] - a[1], -(b[0] - a[0])
            ln = math.sqrt(nx * nx + nz * nz) or 1.0
            sube = ((a[0] + b[0] - at[0] - bt[0]) * nx + (a[1] + b[1] - at[1] - bt[1]) * nz) / (2.0 * ln)
            nrm = _norm((nx / ln, sube / max(1e-6, y1 - y0) if tp != 1.0 else 0.0, nz / ln))
            k0 = len(P)
            for x, y, z in ((a[0], y0, a[1]), (b[0], y0, b[1]), (bt[0], y1, bt[1]), (at[0], y1, at[1])):
                P.append((x, y, z))
                Nn.append(nrm)
                U.append(uv)
            T += [(k0, k0 + 2, k0 + 1), (k0, k0 + 3, k0 + 2)]
        for y, ny in ((y1, 1.0), (y0, -1.0)):   # la tapa (y el fondo si vuela)
            if ny < 0 and y0 < 1e-6:
                continue
            k0 = len(P)
            for x, z in (pt if ny > 0 else pl):
                P.append((x, y, z))
                Nn.append((0.0, ny, 0.0))
                U.append(uv)
            for k in range(1, m - 1):
                T.append((k0, k0 + k + 1, k0 + k) if ny > 0 else (k0, k0 + k, k0 + k + 1))
    v = _MALLAS[clave] = (P, Nn, U, T)
    return v


def silueta_edificio(cfg, diseno, var=0, px=20, ref=None, lado=False):
    """Silueta de un ejemplar a px de alto (de frente, o de lado), con sus
    remates: set de (x, y). Con ref (plantas que caben en px), a escala comun
    entre disenos; sin el, el edificio llena el cuadro. Para comparar la
    lectura a distancia (la fila inferior de la lamina)."""
    e = edificio(cfg, diseno, var)
    H = float(e['alto'])
    esc = px / max(1.0, ref or (H + 6.0))   # en plantas: la aguja y las antenas cuentan
    pts = set()
    ancho_px = lambda u: int(round((u + 0.5) * px * 0.7))
    for vol in e['vols']:
        pl = _planta_vol(vol)
        xs = [p[1] if lado else p[0] for p in pl]
        for y in range(int(vol['y0'] * H * esc), max(int(vol['y0'] * H * esc) + 1, int(round(vol['y1'] * H * esc)))):
            for x in range(ancho_px(min(xs)), ancho_px(max(xs)) + 1):
                pts.add((x, y))
    for r in e['rem']:
        if r['tipo'] in REMATES_LOD:
            continue
        y0 = int(r['y'] * H * esc)
        for y in range(y0, y0 + max(1, int(round(r['alto'] * esc)))):
            x = ancho_px(r['z'] if lado else r['x'])
            for dx in range(max(1, int(round(r['s'] * px * 0.7)))):
                pts.add((x + dx, y))
    return pts


# -----------------------------------------------------------------------------
# 1. NUCLEO - la piel (fase 11): catalogo, vecindad, compuestos y transitos
# -----------------------------------------------------------------------------
# Logica en el motor, piel en el catalogo. El catalogo dice que modelo va en
# cada estado de cada especie y las cadenas de transito de cada tema; el
# motor decide donde, cuantos y cuando. Toda eleccion (variante, giro,
# operacion) sale del mapa logistico sembrado con la velocidad fundadora y
# la celda; la ocupacion dice cuantas piezas lleva el compuesto.

TEMAS = ['naturaleza', 'ciudad', 'industria']      # fase 11 v11: la industria
AVANCES = ['gates', 'pasos']
ESTADOS = ['semilla', 'crecimiento', 'ramificacion', 'fusion', 'coronacion']
ESPECIES = {('naturaleza', GEO): 'vegetacion', ('naturaleza', ARQ): 'relieve',
            ('ciudad', GEO): 'informal', ('ciudad', ARQ): 'planificada',
            ('industria', GEO): 'mina', ('industria', ARQ): 'energia'}
CATALOGO_COLS = ['tema', 'especie', 'estado', 'variante', 'modelo']


# fase 11 v8: la vegetacion del catalogo son modelos arquitectonicos de la
# biblioteca (PLANTAS) y los hibridos de la naturaleza, formas del terreno
FORMAS = ['bosque', 'arrozal', 'meseta']
MARCOS = ['real', 'tresbolillo']    # el marco de los frutales de la meseta
FORMA_HIBRIDO = dict(veg='meseta', rel='arrozal')


def _catalogo_defecto():
    filas = []

    def add(tema, esp, estado, cosas):
        for v, x in enumerate(cosas):
            filas.append((tema, esp, estado, v, x))
    for tema, esp, p in (('naturaleza', 'vegetacion', 'veg'), ('naturaleza', 'relieve', 'rel')):
        semilla = {'veg': list(MATORRALES), 'rel': ['rel_columna', 'rel_columna2']}[p]
        resto = {'veg': [list(ARBOLES)] * 4,
                 'rel': ['rel_columnas', 'rel_mesetas', 'rel_meseta', 'rel_cumbre']}[p]
        add(tema, esp, 'semilla', semilla)
        for estado, mo in zip(ESTADOS[1:], resto):
            add(tema, esp, estado, mo if isinstance(mo, list) else [mo])
        add(tema, esp, 'puente', ['bosque' if p == 'veg' else p + '_puente'])
        add(tema, esp, 'protagonista', ['frondosa', 'pagoda', 'conifera'] if p == 'veg'
            else [p + '_prot1', p + '_prot2', p + '_prot3'])
        add(tema, esp, 'hibrido', [FORMA_HIBRIDO.get(p, p + '_hib')])
    # fase 11 v10: la ciudad, un tipo de edificio por etapa (etapa1 ... etapa6), con
    # sus disenos de la biblioteca; los estados de siempre, como resumen
    for esp in ('informal', 'planificada'):
        tipos = TIPOS[esp]
        for k, tipo in enumerate(tipos):
            add('ciudad', esp, 'etapa%d' % (k + 1), DISENOS_TIPO[tipo])
        for estado, k in zip(ESTADOS, (0, 1, len(tipos) - 3, len(tipos) - 2, len(tipos) - 1)):
            add('ciudad', esp, estado, DISENOS_TIPO[tipos[k]])
    add('ciudad', 'informal', 'puente', ['ciu_pasarela'])
    add('ciudad', 'planificada', 'puente', [nombre_edificio('zocalo', 0)])
    add('ciudad', 'informal', 'protagonista', ['pasarelas', 'corredores', 'kowloon'])
    add('ciudad', 'planificada', 'protagonista', ['pasarela', 'bucle', 'losa'])
    add('ciudad', 'informal', 'hibrido', ['marco'])           # la planificada sobrevuela la informal
    add('ciudad', 'planificada', 'hibrido', ['colonia'])      # la informal coloniza la planificada
    add('ciudad', 'planificada', 'remate', ['ciu_aguja'])
    # fase 11 v11: la industria, como la ciudad: un tipo por etapa, con sus disenos
    for esp in ('mina', 'energia'):
        tipos = TIPOS[esp]
        for k, tipo in enumerate(tipos):
            add('industria', esp, 'etapa%d' % (k + 1), DISENOS_TIPO[tipo])
        for estado, k in zip(ESTADOS, (0, 1, 2, 3, 4)):
            add('industria', esp, estado, DISENOS_TIPO[tipos[k]])
    add('industria', 'mina', 'puente', ['ciu_terril'])        # la cuenca: terriles fundidos y cable aereo
    add('industria', 'energia', 'puente', ['ciu_tuberia'])    # tuberias y cintas entre las plantas
    add('industria', 'mina', 'protagonista', ['cuenca', 'cuenca', 'cuenca'])
    add('industria', 'energia', 'protagonista', ['torre compartida', 'fila de torres', 'anillo de torres'])
    add('industria', 'mina', 'hibrido', ['integrada'])        # la energia se monta encima de la mina
    add('industria', 'energia', 'hibrido', ['corta'])         # la mina se come la planta
    for tema, esp, mo in (('naturaleza', 'vegetacion', 'veg_claro'), ('naturaleza', 'relieve', 'rel_pedregal'),
                          ('ciudad', 'informal', 'inf_escombros'), ('ciudad', 'planificada', 'ciu_valla')):
        add(tema, esp, 'huella', [mo])     # fase 14: lo que deja una catastrofe
    for obra in ('valla', 'foso', 'andamio', 'grua'):
        add('ciudad', 'obra', obra, ['ciu_' + obra])
        add('industria', 'obra', obra, ['ciu_' + obra])
    for esp, mo in (('mina', 'ind_crater'), ('energia', 'ind_ruina'), ('refineria', 'ind_hollin')):
        add('industria', esp, 'huella', [mo])        # fase 14: lo que deja una catastrofe industrial
    # fase 16: lo que ensenan los cortes, en la pared (expuesto) y en el fondo
    for tema, esp, pared, fondo in (('naturaleza', 'vegetacion', ['fos_tronco', 'fos_tronco2'], ['fos_tronco']),
                                    ('naturaleza', 'relieve', ['fos_basalto'], ['fos_basalto']),
                                    ('ciudad', 'informal', ['arq_cimientos'], ['arq_cimientos']),
                                    ('ciudad', 'planificada', ['arq_sotano'], ['arq_cimientos']),
                                    ('ciudad', 'calle', ['arq_calle'], ['arq_calle']),
                                    ('industria', 'mina', ['ind_galeria', 'ind_vagoneta'], ['ind_pozo']),
                                    ('industria', 'energia', ['arq_sotano'], ['arq_cimientos'])):
        add(tema, esp, 'expuesto', pared)
        add(tema, esp, 'fondo', fondo)
    add('ciudad', 'galeria', 'union', ['arq_galeria'])
    add('industria', 'galeria', 'union', ['ind_galeria'])
    cadenas = {('naturaleza', 'vegetacion'): (['inclinar', 'puentes', 'hundir', 'esporas'], ['emerger']),
               ('naturaleza', 'relieve'): (['soldadura', 'relleno'], ['soldadura', 'relleno']),
               ('ciudad', 'informal'): (['soldadura', 'relleno'], ['soldadura', 'relleno']),
               ('ciudad', 'planificada'): (['solar', 'excavacion', 'obreros', 'andamio'],
                                           ['grua', 'fachada', 'aguja']),
               ('industria', 'mina'): (['soldadura', 'relleno'], ['soldadura', 'relleno']),
               ('industria', 'energia'): (['solar', 'excavacion', 'obreros', 'andamio'], ['grua', 'fachada'])}
    for (tema, esp), (cf, cc) in sorted(cadenas.items()):
        add(tema, esp, 'cadena fusion', cf)
        add(tema, esp, 'cadena corona', cc)
    return filas


CATALOGO_FILAS = _catalogo_defecto()
ETAPAS = ['inclinar', 'puentes', 'hundir', 'esporas', 'emerger', 'soldadura', 'relleno',
          'solar', 'excavacion', 'obreros', 'andamio', 'grua', 'fachada', 'aguja']


def catalogo_de(filas):
    """{(tema, especie, estado): [modelo o etapa por variante]} de unas filas
    del catalogo. Los modelos y etapas que el motor no conoce se ignoran."""
    out = {}
    for tema, esp, estado, var, x in filas:
        lista = out.setdefault((tema, esp, estado), [])
        if (estado.startswith('cadena') and x in ETAPAS) or x in MODELOS or x in PLANTAS or x in FORMAS \
                or x in _GEN_EDI or x in CIUDAD_FORMAS or es_edificio(x):
            lista.append((int(var), x))
    return dict((k, [x for _, x in sorted(v)]) for k, v in out.items())


CATALOGO = catalogo_de(CATALOGO_FILAS)


def _cat(cfg):
    return cfg.get('catalogo') or CATALOGO


def tema_de(cfg):
    return TEMAS[int(cfg.get('tema', 0)) % len(TEMAS)]


def especie_de(tema, own):
    return ESPECIES.get((tema, own), 'vegetacion' if tema == 'naturaleza' else 'informal')


def modelos_de(cfg, tema, esp, estado):
    """Modelos del catalogo para ese estado (con el de por defecto si el
    catalogo editado lo dejo vacio)."""
    lista = _cat(cfg).get((tema, esp, estado)) or CATALOGO.get((tema, esp, estado)) or []
    return lista


def cadenas_de(cfg, tema, esp):
    """(etapas de la fusion, etapas de la coronacion)."""
    c = _cat(cfg)
    return (c.get((tema, esp, 'cadena fusion'), CATALOGO.get((tema, esp, 'cadena fusion'), [])),
            c.get((tema, esp, 'cadena corona'), CATALOGO.get((tema, esp, 'cadena corona'), [])))


def estado_idx(cfg, occ):
    """0 semilla, 1 crecimiento, 2 ramificacion, 3 fusion, 4 coronacion, con
    los umbrales de la fase 4."""
    if occ <= 1:
        return 0
    if occ < cfg['th_branch']:
        return 1
    if occ < cfg['th_fusion']:
        return 2
    if occ < cfg['th_crown']:
        return 3
    return 4


# --- el mapa logistico: sin azar de software ------------------------------------

def semilla_caos(vel, celda):
    """x0 en (0,05; 0,95) de la velocidad fundadora y la celda."""
    return 0.05 + 0.9 * ((int(vel) * 0.6180339887 + int(celda) * 0.3819660113 + 0.1234) % 1.0)


def logistica(x0, r, n, calentar=8):
    """n valores de x -> r x (1 - x), tras unas vueltas de calentamiento."""
    x = min(0.999, max(0.001, float(x0)))
    r = max(0.0, min(4.0, float(r)))
    out = []
    for k in range(int(calentar) + int(n)):
        x = r * x * (1.0 - x)
        if not 1e-9 < x < 1.0 - 1e-9:
            x = 0.3819660113             # punto fijo en 0 o 1: se sale por el aureo
        if k >= calentar:
            out.append(x)
    return out


# --- vecindad: clusters ---------------------------------------------------------

def presion(W, cfg, i):
    """P = ocupacion + Pesovecina x ocupacion de las vecinas de su especie."""
    o = W['occ'][i]
    if o <= 0:
        return 0.0
    s = W['own'][i]
    return o + cfg['peso_vecina'] * sum(W['occ'][j] for j in NEIGH[i]
                                        if W['occ'][j] > 0 and W['own'][j] == s)


_CLUSTERS = {}


def clusters(W, cfg):
    """Formaciones fundidas (se guarda el ultimo calculo: mismo mundo, mismo
    resultado; no lo modifiques)."""
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), cfg['umbral_vecindad'],
             cfg['peso_vecina'], cfg['min_cluster'], cfg['th_fusion'], GRID['lo'], GRID['hi'])
    if _CLUSTERS.get('clave') != clave:
        _CLUSTERS['clave'], _CLUSTERS['cl'] = clave, _clusters(W, cfg)
    return _CLUSTERS['cl']


def _clusters(W, cfg):
    """Formaciones fundidas. Dos vecinas de la misma especie se unen si las dos
    tienen P >= Umbralvecindad; una formacion en fusion (fase 4) se une con
    sus satelites. Union-find; cuentan los grupos de Mincluster celdas o mas.
    Devuelve dict(de=[cluster de cada celda o -1], celdas={id: [...]},
    capital={id: celda}, mascara=[[vecinas del cluster unidas a la celda]])."""
    U = cfg['umbral_vecindad']
    P = [presion(W, cfg, i) for i in range(N)]
    padre = list(range(N))

    def raiz(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a
    enlaces = []
    for i in range(N):
        if W['occ'][i] <= 0 or not W['own'][i]:
            continue
        for j in NEIGH[i]:
            if j <= i or W['occ'][j] <= 0 or W['own'][j] != W['own'][i]:
                continue
            vec = P[i] >= U and P[j] >= U
            des = (W['par'][j] == i and W['occ'][i] >= cfg['th_fusion']) or \
                  (W['par'][i] == j and W['occ'][j] >= cfg['th_fusion'])
            if vec or des:
                enlaces.append((i, j))
                padre[raiz(i)] = raiz(j)
    grupos = {}
    for i in range(N):
        if W['occ'][i] > 0:
            grupos.setdefault(raiz(i), []).append(i)
    minimo = max(2, int(cfg['min_cluster']))
    de = [-1] * N
    celdas, capital = {}, {}
    for k, (r, cs) in enumerate(sorted(grupos.items(), key=lambda kv: min(kv[1]))):
        if len(cs) < minimo:
            continue
        celdas[k] = cs
        capital[k] = max(cs, key=lambda c: (W['par'][c] < 0, W['occ'][c], -c))
        for c in cs:
            de[c] = k
    mascara = [[] for _ in range(N)]
    for i, j in enlaces:
        if de[i] >= 0 and de[i] == de[j]:
            mascara[i].append(j)
            mascara[j].append(i)
    return dict(de=de, celdas=celdas, capital=capital, mascara=mascara, presion=P)


def clase_cluster(n):
    """Pieza protagonista por tamano: 2-3 celdas, 4-6, o 7 y mas."""
    return 0 if n <= 3 else (1 if n <= 6 else 2)


# --- compuestos: el juego del caos ------------------------------------------------

OPS_CAOS = ['incrustar', 'apilar', 'orbitar', 'hundir', 'inclinar']
TOPE_COMPUESTO = 1.2        # nada del compuesto pasa de 1,2 veces la formacion


_COMPUESTOS = {}


def compuesto(cfg, own, vel, celda, occ, sat=False):
    """Piezas de una formacion, en la celda: x, z en fracciones de la celda,
    y en alturas de la formacion, giro e inclinacion en grados (multiplos de
    30; la malla ortogonal del SEQ2, de 90 y sin inclinar), esc relativa a
    la pieza principal, var (0-1) para elegir variante. Iteraciones =
    min(ocupacion, Maxpiezas). La misma semilla da el mismo compuesto, y una
    ocupacion mayor solo le anade piezas. Se guarda: no lo modifiques."""
    n = 1 if sat else max(1, min(int(occ), int(cfg['max_piezas'])))
    clave = (own, int(vel), int(celda), n, float(cfg['caos']))
    out = _COMPUESTOS.get(clave)
    if out is None:
        if len(_COMPUESTOS) > 20000:
            _COMPUESTOS.clear()
        out = _COMPUESTOS[clave] = _compuesto(cfg['caos'], own, vel, celda, n)
    return out


def _compuesto(caos, own, vel, celda, n):
    xs = logistica(semilla_caos(vel, celda), caos, 5 * n + 1)
    orto = own == ARQ
    paso = 90 if orto else 30

    def ang(x):
        return (int(x * 360.0 / paso) * paso) % 360

    piezas = [dict(op='base', x=0.0, y=0.0, z=0.0, giro=float(ang(xs[0])), incl=0.0, rumbo=0.0,
                   esc=1.0, var=xs[0])]
    for k in range(1, n):
        a, b, c, d, v = xs[5 * k - 4:5 * k + 1]
        op = OPS_CAOS[min(len(OPS_CAOS) - 1, int(a * len(OPS_CAOS)))]
        if orto and op == 'inclinar':
            op = 'apilar'
        pr = piezas[-1]
        q = dict(op=op, x=pr['x'], y=pr['y'], z=pr['z'], giro=pr['giro'], incl=0.0, rumbo=0.0,
                 esc=pr['esc'], var=v)
        if op == 'incrustar':
            q.update(x=pr['x'] + (b - 0.5) * 0.3, z=pr['z'] + (c - 0.5) * 0.3,
                     y=pr['y'] + pr['esc'] * (0.2 + 0.4 * d), esc=pr['esc'] * 0.55,
                     giro=(pr['giro'] + paso) % 360)
        elif op == 'apilar':
            q.update(y=pr['y'] + pr['esc'] * 0.85, esc=pr['esc'] * 0.65,
                     giro=(pr['giro'] + paso * (1 + int(b * 3))) % 360)
        elif op in ('orbitar', 'hundir'):
            g = math.radians(ang(b))
            rad = 0.2 + 0.2 * c
            esc = (0.4 + 0.25 * d) if op == 'orbitar' else (0.5 + 0.3 * d)
            q.update(x=rad * math.cos(g), z=rad * math.sin(g), giro=float(ang(b)), esc=esc,
                     y=0.0 if op == 'orbitar' else -0.3 * esc)
        else:                                       # inclinar
            r_ = ang(b)
            g = math.radians(r_)
            q.update(x=pr['x'] + 0.15 * math.cos(g), z=pr['z'] + 0.15 * math.sin(g),
                     y=pr['y'] + pr['esc'] * 0.3, esc=pr['esc'] * 0.6, incl=30.0, rumbo=float(r_))
        if orto:                                    # a la malla
            q['x'], q['z'] = round(q['x'] * 8) / 8.0, round(q['z'] * 8) / 8.0
        q['x'] = max(-0.4, min(0.4, q['x']))
        q['z'] = max(-0.4, min(0.4, q['z']))
        q['esc'] = max(0.12, min(1.0, q['esc']))
        q['y'] = max(-0.35, min(TOPE_COMPUESTO - q['esc'], q['y']))
        piezas.append(q)
    return piezas


# --- transitos: la animacion no decide ------------------------------------------
# El estado logico cambia al instante; lo visible lo persigue. Cada celda
# lleva la etapa visible de su cadena de fusion (et_f) y de coronacion
# (et_c). El objetivo es la cadena entera si la celda esta en un cluster (o
# coronada); si no, 0. Con Avance = gates, cada nota en una celda del
# cluster adelanta una etapa la obra del cluster (todas sus celdas); con
# Avance = pasos, una etapa cada Pasosetapa pasos. Hacia atras (la ocupacion baja) se recorre
# sola, una etapa cada Pasosetapa pasos. Un fin de ciclo lo cierra de golpe.

FOTOS_PASO = 3               # fotogramas de stop-motion por paso


def objetivos(W, cfg, cl=None):
    """(objetivo de la fusion, objetivo de la coronacion) de cada celda."""
    cl = cl or clusters(W, cfg)
    tema = tema_de(cfg)
    tf, tc = [0] * N, [0] * N
    for i in range(N):
        if W['occ'][i] <= 0 or not W['own'][i]:
            continue
        if cfg['nivel'] >= 14 and W['derribo'][i]:
            continue                    # fase 14: la obra se derriba, hacia atras
        cf, cc = cadenas_de(cfg, tema, especie_de(tema, W['own'][i]))
        if cl['de'][i] >= 0:
            tf[i] = len(cf)
        if W['par'][i] < 0 and W['occ'][i] >= cfg['th_crown']:
            tc[i] = len(cc)
    return tf, tc


def _etapa(W, i, clave, valor, now):
    ant = W[clave][i]
    if valor != ant:
        W[clave][i] = valor
        W['ant_' + clave][i] = ant
        W['t_' + clave][i] = now


def gate_piel(W, cfg, i, now):
    """Una nota en la celda i: con Avance = gates, adelanta una etapa la obra
    de su cluster (o la suya, si esta sola). La obra es del cluster: una
    celda que se une a mitad de obra se incorpora en la etapa por la que va."""
    if cfg['nivel'] < 11 or i is None or not 0 <= i < N:
        return
    W['t_gate'][i] = now
    if cfg['nivel'] >= 14 and W['derribo'][i]:   # fase 14: una nota para el derribo
        cl0 = clusters(W, cfg)
        k0 = cl0['de'][i]
        for c in (cl0['celdas'][k0] if k0 >= 0 else [i]):
            W['derribo'][c] = 0
    ciudad_gate(W, cfg, i, now)         # fase 11 v10: la obra del edificio de la celda
    if int(cfg.get('avance', 0)) != 0:
        return
    cl = clusters(W, cfg)
    tf, tc = objetivos(W, cfg, cl)
    k = cl['de'][i]
    celdas = cl['celdas'][k] if k >= 0 else [i]
    meta = max(W['et_f'][c] for c in celdas) + 1
    for c in celdas:
        if W['et_f'][c] < tf[c]:
            _etapa(W, c, 'et_f', min(tf[c], meta), now)
        if W['et_c'][c] < tc[c]:
            _etapa(W, c, 'et_c', W['et_c'][c] + 1, now)


def tick_piel(W, cfg, now, paso, playing=True):
    """Las obras que van solas: hacia atras siempre, hacia delante con
    Avance = pasos. Las celdas vacias no tienen obra."""
    espera = max(1, int(cfg['pasos_etapa'])) * paso
    pasos = int(cfg.get('avance', 0)) == 1
    tf, tc = objetivos(W, cfg)
    for i in range(N):
        if W['occ'][i] <= 0:
            W['et_f'][i] = W['et_c'][i] = 0
            W['derribo'][i] = 0
            continue
        if W['derribo'][i] and W['et_f'][i] == 0 and W['et_c'][i] == 0 and W['obra'][i] == 0:
            W['derribo'][i] = 0         # fase 14: derribada; la obra puede volver a empezar
        for clave, obj in (('et_f', tf[i]), ('et_c', tc[i])):
            e = W[clave][i]
            if now - W['t_' + clave][i] < espera:
                continue
            if e > obj:
                _etapa(W, i, clave, e - 1, now)
            elif e < obj and pasos and playing:
                _etapa(W, i, clave, e + 1, now)
    ciudad_tick(W, cfg, now, paso, playing)     # fase 11 v10: la obra de los edificios y los mutantes


def cerrar_obras(W, cfg):
    """Fin de ciclo: cada transito, en su estado final, sin animacion."""
    if cfg['nivel'] < 11:
        return
    tf, tc = objetivos(W, cfg)
    for i in range(N):
        for clave, obj in (('et_f', tf[i]), ('et_c', tc[i])):
            W[clave][i] = W['ant_' + clave][i] = obj
            W['t_' + clave][i] = -99.0
    cerrar_obras_ciudad(W, cfg)         # fase 11 v10: los edificios, terminados


def _stop(u, fotos=FOTOS_PASO):
    """Progreso 0-1 de un transito a saltos de stop-motion (u en pasos)."""
    if u < 0:
        return 1.0
    return min(1.0, (math.floor(u * fotos) + 1.0) / fotos)


def avance_etapa(W, i, clave, k, now, paso, pasos_k=1.0):
    """Cuanto de la etapa k (1, 2...) se ve en la celda i: 0 si no ha llegado,
    1 si ya esta; entre medias mientras dura su transito (pasos_k pasos)."""
    e = W[clave][i]
    if e < k:
        return 0.0
    if e == k and W['ant_' + clave][i] < k:
        return _stop((now - W['t_' + clave][i]) / (paso * max(1e-6, pasos_k)))
    return 1.0


def rebote(cfg, W, i, now, paso):
    """(escala, destello) del nacimiento: stop-motion de un paso como mucho."""
    u = (now - W['t_nac'][i]) / max(1e-6, paso)
    if u < 0 or u >= 1:
        return 1.0, 0.0
    R = cfg['rebote']
    fotos = (0.45, 1.0 + R, 1.0 - R / 2.0, 1.0)
    return fotos[min(3, int(u * 4))], 1.0 - u


def vh_stop(W, i, now, paso):
    """La altura visible persigue a la logica en un paso, a saltos. Al nacer
    se pone de golpe: el rebote hace el resto."""
    h = W['h'][i]
    if h != W['h_obj'][i]:
        nace = W['vh'][i] <= 0.005 and h > 0 and 0 <= now - W['t_nac'][i] < paso
        W['h0'][i] = h if nace else W['vh'][i]
        W['h_obj'][i] = h
        W['t_h'][i] = now
    q = _stop((now - W['t_h'][i]) / max(1e-6, paso))
    return W['h0'][i] + (h - W['h0'][i]) * q


# --- moduladores (fase 12): velocidad -> material, gate -> vigor -------------------
# La velocidad fundadora da la rugosidad: binario (Umbralvel, como hasta
# ahora) o continuo (de Rugmax a 0 a Rugmin a 127). Va en el alfa del color
# de cada instancia; el GLSL MAT de la piel la lee (pulido: reflejo fino y
# fuerte; rugoso: mate y con poros). El color se acerca al material del
# tema: obsidiana <-> pomez en el relieve, hoja cerosa <-> musgo seco en la
# vegetacion (desde la v32; antes los arboles eran de obsidiana), vidrio
# negro <-> hormigon en la ciudad. La velocidad sigue sembrando el caos.
# El gate, al soltar la nota: en naturaleza da vigor (tronco mas grueso y
# copa mas ancha); en la ciudad, un gate ligado construye Plantasligado
# plantas en vez de una.

MATERIALES = ['binario', 'continuo']
LIGADO = 1.0                # un gate de un paso o mas es ligado
# familia: (color pulido, color rugoso, cuanto pesa sobre el color de la especie)
MATERIAL = dict(mineral=((0.10, 0.10, 0.12), (0.80, 0.78, 0.72), 0.50),
                dosel=((0.14, 0.32, 0.17), (0.42, 0.47, 0.27), 0.45),
                ciudad=((0.08, 0.09, 0.12), (0.68, 0.66, 0.62), 0.60))
MAT_FAMILIA = dict(mineral='mat_piel_mineral', dosel='mat_piel_dosel', ciudad='mat_piel_ciudad',
                   tierra='mat_piel_tierra', agua='mat_piel_agua', obra='mat_poroso')
FAMILIAS = ['mineral', 'dosel', 'ciudad', 'tierra', 'agua']     # uFamilia del shader: 0 a 4 (fase 11 v5: 3 y 4)


def rugosidad(cfg, vel):
    """Rugosidad 0-1 de la velocidad fundadora."""
    lo, hi = cfg['rug_min'], cfg['rug_max']
    if int(cfg.get('material_modo', 1)) == 0:
        return lo if vel >= cfg['vel_umbral'] else hi
    return hi + (lo - hi) * max(0.0, min(1.0, float(vel) / 127.0))


def familia_de(modelo):
    """Familia de material de un modelo. Toda la vegetacion (arboles, brotes y
    dosel) es 'dosel', el material vegetal; desde la v32 los arboles ya no
    son de obsidiana: se veian como alambre."""
    if modelo.startswith('ciu_'):
        return 'obra'
    if modelo == 'veg_claro':           # fase 14: el claro es ceniza, no hoja
        return 'mineral'
    if modelo.startswith('veg_'):
        return 'dosel'
    return 'ciudad' if modelo[:3] in ('inf', 'pla', 'arq', 'edi') else 'mineral'


def material_tema(cfg, col, familia, rug):
    """El color de la especie acercado al material de su familia."""
    m = MATERIAL.get(familia)
    if m is None:
        return col
    t = (rug - cfg['rug_min']) / max(1e-6, cfg['rug_max'] - cfg['rug_min'])
    return _mix(col, _mix(m[0], m[1], max(0.0, min(1.0, t))), m[2])


def vigor_de(cfg, gate_pasos):
    """Vigor de un gate: 1 con el gate normal (medio paso), menos si es
    corto, hasta Vigormax si es ligado."""
    return max(0.6, min(max(0.6, cfg['vigor_max']), 0.6 + 0.8 * gate_pasos))


def gate_vigor(W, cfg, s, p, now, tempo):
    """Se suelta una nota (fase 12). Naturaleza: el vigor de la formacion
    persigue el del gate. Ciudad: un gate ligado construye Plantasligado
    plantas (las que faltan, como notas de la misma velocidad)."""
    i, t_on = p[0], p[1]
    if not 0 <= i < N or W['occ'][i] <= 0:
        return
    g = max(0.0, now - t_on) / step_dur(cfg, tempo)
    W['vig'][i] = 0.5 * W['vig'][i] + 0.5 * vigor_de(cfg, g)
    if tema_de(cfg) == 'ciudad':
        plantas = max(1, int(cfg['plantas_ligado'])) if g >= LIGADO else 1
        for _ in range(plantas - 1):
            grow(W, cfg, i, s, W['vel'][i], now)
        efecto = '%d planta%s' % (plantas, '' if plantas == 1 else 's')
    else:
        efecto = 'vigor %.2f' % W['vig'][i]
    mod = W['ev'].get('mod')
    if mod is None or mod.get('celda') != i:
        mod = W['ev']['mod'] = dict(s=s, celda=i, vel=W['vel'][i], rug=rugosidad(cfg, W['vel'][i]))
    mod.update(gate=g, efecto=efecto)


# --- dibujar la piel ------------------------------------------------------------

COL_ESPECIE = dict(vegetacion=(0.34, 0.52, 0.30), relieve=(0.30, 0.31, 0.35),
                   informal=(0.66, 0.50, 0.38), planificada=(0.60, 0.63, 0.68))
COL_PUENTE = dict(vegetacion=(0.27, 0.44, 0.25), relieve=(0.28, 0.29, 0.33),
                  informal=(0.52, 0.40, 0.30), planificada=(0.52, 0.53, 0.56))
COL_OBRA = dict(valla=(0.80, 0.62, 0.28), foso=(0.16, 0.13, 0.11), andamio=(0.72, 0.68, 0.58),
                grua=(0.92, 0.80, 0.30))
COL_ESPORA = (0.86, 0.94, 0.72)
COL_POLVO = (0.58, 0.52, 0.44)
COL_OBRERO = (1.00, 0.68, 0.22)
# puente de cada especie: (ancho x celda, base y grosor x la formacion mas baja)
PUENTE = dict(vegetacion=(0.42, 0.62, 0.24), relieve=(0.40, 0.0, 0.50),
              informal=(0.12, 0.45, 0.14), planificada=(0.62, 0.0, 0.22))
# hueco del dosel (motor v32): la copa que cierra el triangulo entre tres celdas
# del cluster, con el modelo del dosel centrado (su ancho, su largo y el centro
# de su planta, en unidades del modelo) y un diametro de DOSEL_HUECO x el radio
DOSEL_HUECO = 1.5
DOSEL_ANCHO, DOSEL_LARGO, DOSEL_CENTRO = 1.10, 1.495, (0.08, 0.5025)
CORONA_K = 1.35              # la pieza de coronacion, mas alta que la formacion
CORONA_TRAMO = 0.10          # y un 10 % mas por tramo de cumbre
ANDAMIO_PASOS = 3.0          # el andamio sube planta a planta en 3 pasos
ESPORAS_PASOS = 16.0         # las esporas duran 16 pasos
INCLINAR = 20.0              # grados que se inclinan los arboles hacia la capital


_GEOMETRIAS = {}


def geometria_de(modelo, pulido=True, doble=True):
    """Nombre de la geometria de TouchDesigner de un modelo. En la fase 11,
    pulida y porosa (doble); desde la fase 12, una sola por modelo (el
    material lo da el shader). Las obras de la ciudad tienen siempre una."""
    clave = (modelo, pulido, doble)
    g = _GEOMETRIAS.get(clave)
    if g is None:
        g = 'mod_' + modelo if modelo.startswith('ciu_') or not doble or es_ejemplar(modelo) \
            or es_edificio(modelo) else \
            'mod_%s_%s' % (modelo, 'pul' if pulido else 'por')
        _GEOMETRIAS[clave] = g
    return g


def geometrias_piel(cfg=None):
    """[(geometria, modelo, material)]: en la fase 11, pulida (mat_pulido) y
    porosa (mat_poroso); desde la fase 12, una por modelo con el material de
    su familia."""
    cfg = cfg or DEFAULT_CFG
    clave = (cfg['nivel'] < 12, variantes(cfg), VARIANTES_TD, variantes_ciudad(cfg), VARIANTES_CIU_TD,
             variantes_ind(cfg), VARIANTES_IND_TD)
    v = _GEOS_CACHE.get(clave)
    if v is not None:
        return v
    doble = cfg['nivel'] < 12
    out = []
    for mo in sorted(MODELOS):
        if mo.startswith('ciu_'):
            out.append((geometria_de(mo), mo, 'mat_poroso'))
        elif doble:
            out.append((geometria_de(mo, True), mo, 'mat_pulido'))
            out.append((geometria_de(mo, False), mo, 'mat_poroso'))
        else:
            out.append((geometria_de(mo, doble=False), mo, MAT_FAMILIA[familia_de(mo)]))
    for mo in ejemplares_de(cfg):     # fase 11 v8: la biblioteca, una geometria por ejemplar
        out.append((geometria_de(mo), mo, 'mat_pulido' if doble else MAT_FAMILIA['dosel']))
    for mo in edificios_de(cfg):      # fase 11 v10: la biblioteca de la ciudad, con el shader de la ciudad
        out.append((geometria_de(mo), mo, 'mat_pulido' if doble else MAT_FAMILIA['ciudad']))
    _GEOS_CACHE[clave] = out           # se pide en cada fotograma: se guarda
    return out


_GEOS_CACHE = {}


def _ejes(n, giro=0.0, incl=0.0, rumbo=0.0):
    """Ejes (X, Y, Z) de una pieza sobre la normal n: girada 'giro' grados
    alrededor de la normal e inclinada 'incl' grados hacia 'rumbo'."""
    e, t = tangents(n)
    X, Y, Z = e, n, t
    if giro:
        g = math.radians(giro)
        X, Z = (_add(_mul(X, math.cos(g)), Z, -math.sin(g)), _add(_mul(X, math.sin(g)), Z, math.cos(g)))
    if incl:
        r = math.radians(rumbo)
        d = _add(_mul(e, math.cos(r)), t, math.sin(r))
        eje = _norm(_cross(Y, d))
        X, Y, Z = _girar_eje(X, eje, incl), _girar_eje(Y, eje, incl), _girar_eje(Z, eje, incl)
    return X, Y, Z


_MARCOS = {}


def _marco(i, giro=0.0, incl=0.0, rumbo=0.0):
    """(X, Y, Z, (rx, ry, rz)) de una pieza en la celda i (ver _ejes). Se
    guardan: el giro va en multiplos de 30 y la inclinacion, a los saltos del
    stop-motion, asi que se repiten."""
    clave = (GRID['lo'], GRID['hi'], i, giro, incl, rumbo)
    v = _MARCOS.get(clave)
    if v is None:
        if len(_MARCOS) > 50000:
            _MARCOS.clear()
        ej = _ejes(normal_i(i), giro, incl, rumbo)
        v = _MARCOS[clave] = ej + (_euler_xyz(*ej),)
    return v


def _marco_puente(i, j):
    """Marco del puente de la celda i hacia su vecina j: Z hacia j, Y la normal."""
    clave = (GRID['lo'], GRID['hi'], i, 'puente', j)
    v = _MARCOS.get(clave)
    if v is None:
        n = normal_i(i)
        d = _hacia(n, n, normal_i(j))
        ej = (_cross(n, d), n, d)
        v = _MARCOS[clave] = ej + (_euler_xyz(*ej),)
    return v


def _huecos_dosel(i, mascara, bases):
    """Los huecos del dosel que cierra la celda i: cada triangulo de celdas
    del cluster unidas entre si (i, j, k) en el que i es la de indice menor.
    Da (celdas, centro sobre la superficie, marco, radio del triangulo)."""
    out = []
    mi = mascara[i]
    for j in mi:
        if j <= i:
            continue
        for k in mi:
            if k <= j or k not in mascara[j]:
                continue
            tri = (i, j, k)
            a, b, c = bases[i], bases[j], bases[k]
            g = ((a[0] + b[0] + c[0]) / 3.0, (a[1] + b[1] + c[1]) / 3.0, (a[2] + b[2] + c[2]) / 3.0)
            r = (_len(a) + _len(b) + _len(c)) / 3.0
            nc = _norm(g)
            pc = _mul(nc, r)
            clave = (GRID['lo'], GRID['hi'], 'hueco', tri)
            ej = _MARCOS.get(clave)
            if ej is None:
                d = _hacia(nc, pc, a)
                ej = _MARCOS[clave] = (_cross(nc, d), nc, d, _euler_xyz(_cross(nc, d), nc, d))
            rho = max(_len(_add(x, pc, -1.0)) for x in (a, b, c))
            out.append((tri, pc, ej, rho))
    return out


def _fila_m(p, marco, sx, sy, sz, col):
    rx, ry, rz = marco[3]
    return [p[0], p[1], p[2], rx, ry, rz, sx, sy, sz, col[0], col[1], col[2]]


def _pie(modelo, vh, cw, cl, ancho=1.0):
    """(sx, sy, sz) de un modelo con altura vh en una celda cw x cl. 'ancho'
    (el vigor, fase 12) lo ensancha; con vigor, la copa puede pasar un poco
    del ancho de la celda."""
    modo, k = PIE.get(modelo, ('esbelto', 0.9))
    if modo == 'celda':
        k = min(0.98, k * ancho)
        return k * cw, vh, k * cl
    tope = k * min(cw, cl) / ANCHO.get(modelo, 1.0) * (1.0 + 0.3 * max(0.0, ancho - 1.0))
    s = min(vh * ancho, tope)
    return s, vh, s


def _hacia(n, p_de, p_a):
    """Direccion unitaria de p_de a p_a, sobre el plano tangente de n."""
    d = (p_a[0] - p_de[0], p_a[1] - p_de[1], p_a[2] - p_de[2])
    d = _add(d, n, -_dot(d, n))
    return _norm(d)


def _rumbo(n, d):
    """Grados del rumbo d (en el plano tangente) desde el este hacia el sur."""
    e, t = tangents(n)
    return math.degrees(math.atan2(_dot(d, t), _dot(d, e)))


def _particulas(out, n, p0, cw, cl, vh, semilla, k, col, now, paso, modo, escala=1.0):
    """Instancias de particulas (cajas del motor) de una celda. 'escala'
    las encoge (una nube que se disipa)."""
    e, t = tangents(n)
    xs = _COMPUESTOS.get(('particulas', semilla, k))
    if xs is None:
        xs = _COMPUESTOS[('particulas', semilla, k)] = logistica(semilla, 3.91, 3 * k)
    tau = math.floor(now / paso * FOTOS_PASO) / FOTOS_PASO       # tiempo a saltos
    m = min(cw, cl)
    for q in range(k):
        a, b, c = xs[3 * q:3 * q + 3]
        if modo == 'esporas':           # suben y derivan sobre el dosel
            f = (tau / 8.0 + a) % 1.0
            g = 2 * math.pi * b + tau * 0.15
            r_, h_, s_ = 0.15 + 0.3 * c, vh * (0.6 + 0.9 * f), 0.035 * m
        elif modo == 'polvo':           # nube que se abre a ras de suelo
            f = (tau / 6.0 + a) % 1.0
            g = 2 * math.pi * b
            r_, h_, s_ = 0.1 + 0.4 * f, 0.05 + 0.25 * f * vh, (0.04 + 0.05 * f) * m
        elif modo == 'brasas':          # fase 14: suben deprisa desde lo que arde y se apagan
            f = (tau / 3.0 + a) % 1.0
            g = 2 * math.pi * b + tau * 0.3
            r_, h_, s_ = 0.08 + 0.3 * c, vh * (0.3 + 1.1 * f), 0.03 * m * (1.0 - 0.6 * f)
        elif modo == 'semillas':        # fase 15: el banco de semillas, sobre el suelo
            g = 2 * math.pi * b
            r_, h_, s_ = 0.08 + 0.36 * c, 0.01 + 0.03 * ((tau / 4.0 + a) % 1.0), 0.03 * m
        elif modo == 'smog':            # fase 19: bruma parda que deriva sobre la ciudad
            f = (tau / 24.0 + a) % 1.0
            g = 2 * math.pi * (b + f)
            r_, h_, s_ = 0.2 + 0.35 * c, vh * (1.0 + 0.6 * c), 0.09 * m
        elif modo == 'ceniza':          # fase 14: copos grises que caen y derivan
            f = (tau / 7.0 + a) % 1.0
            g = 2 * math.pi * b + tau * 0.08
            r_, h_, s_ = 0.15 + 0.35 * c, 0.05 + vh * (1.1 - f), 0.028 * m
        else:                           # obreros: puntos que dan vueltas a la obra
            g = 2 * math.pi * b + tau * (0.4 + 0.4 * c) * (1 if a > 0.5 else -1)
            r_, h_, s_ = 0.25 + 0.15 * a, 0.0, 0.03 * m
        p = _add(_add(_add(p0, e, math.cos(g) * r_ * cw), t, math.sin(g) * r_ * cl), n, h_)
        s_ *= escala
        out.append(_row(p, n, s_, s_ * (2.0 if modo == 'obreros' else 1.0), s_, col))


# --- la piel por turnos (motor v101, fase 11 v18) ---------------------------------
# La piel de los tres temas se calcula por porciones en varios fotogramas y se
# publica de una vez cada Refrescopiel segundos: entre dos publicaciones las
# filas de los modelos son las mismas (las mismas listas) y los Script CHOP no
# se recuecen. Una vuelta empieza con su instante de publicacion t_pub = inicio
# + Refrescopiel; todas sus porciones se calculan con now = t_pub (el planeta
# entero en el mismo instante) en un bufer de trabajo agrupado por celda, y al
# cerrarla el bufer pasa a ser el publicado de golpe. Las piezas de cluster van
# con la capital; las globales (gruas, volcanes), al cerrar la vuelta.
# CAMINO INMEDIATO: una celda que recibe nota, impulso, erosion o corte, o que
# cambia de ocupacion, especie o dueno, se recalcula en ese mismo fotograma con
# su vecindad y su cluster (antes y despues) y sustituye sus filas en el
# publicado y en el de trabajo. El fin del tinte de las ventanas y del pumping la
# vuelve a marcar.
# Turnos apagado: la vuelta entera en el fotograma de publicacion. Refrescopiel 0:
# la piel entera en cada fotograma (build_piel), como antes de la fase 11 v8.

# los parametros de la pagina Fase11 (y los de la piel de otras paginas): si cambia
# alguno, la piel vacia sus bufers y publica una vuelta completa (motor v101)
PIEL_CFG = ('peso_vecina', 'umbral_vecindad', 'min_cluster', 'caos', 'max_piezas', 'avance', 'pasos_etapa',
            'umbral_monte', 'limite_bosque', 'limite_nieve', 'altura_monte', 'lod_nat', 'tinte_borde_nat',
            'superficie', 'ligero', 'oceano', 'volcanes', 'detalle', 'pradera', 'mata', 'tierra',
            'refresco_piel', 'biomas', 'variantes', 'traslucidez', 'timidez', 'emergentes', 'orla', 'mezcla',
            'impostores', 'terrazas_por_nota', 'max_terrazas', 'paso_terraza', 'riego', 'color_cultivo',
            'altura_meseta', 'max_niveles', 'marco', 'setos', 'lenguaje', 'variantes_ciudad', 'fijar_tipo',
            'oblicuidad', 'alto_planta', 'ancho_vano', 'retranqueo', 'torsion_max', 'parasitos_por_nota',
            'max_parasitos', 'modulo_marco', 'max_marco', 'capsulas', 'mutacion', 'mutacion_fuente', 'obra',
            'desfase_fachada', 'gruas', 'max_gruas', 'tinte_ventanas', 'pasos_tinte', 'lod_ciudad',
            'recursos', 'epoca', 'variantes_ind', 'bancos_por_nota', 'max_bancos', 'max_bastidor',
            'emisiones', 'max_humo', 'lod_ind', 'th_branch', 'th_fusion', 'th_crown', 'respaldo', 'rug_min',
            'rug_max', 'sat_size', 'height_factor', 'shell_thick', 'core_radius')


_TURNOS = {}

# lo que cambia una nota, un golpe o un corte en la celda (el camino inmediato). El
# avance de las obras y de los transitos (obra, et_f, et_c) no: va a saltos de Refrescopiel.
# EVENTO_LUZ solo cambia la celda (su latido, su tinte); lo demas, tambien a sus vecinas
EVENTO_LUZ = ('t_gate', 'lat', 'lat_s')
EVENTO_CAMPOS = ('occ', 'own', 'sp', 'par', 'vel', 't_nac', 'rebrote', 'ruina', 'derribo') + EVENTO_LUZ


def _emisor_piel(P):
    """La funcion emit de la piel: escribe en P['out'] (el cubo de la celda que se
    esta calculando) y cuenta las piezas."""
    doce, respaldo = P['doce'], P['respaldo']

    def emit(modelo, pulido, p, marco, dims, col, rug=1.0, luces=0):
        fila = _fila_m(p, marco, dims[0], dims[1], dims[2], col)
        if doce:                    # las ventanas (0-4) van en el alfa: rugosidad + 2 x nivel
            fila.append(1.0 if respaldo else rug + 2.0 * luces)
        P['out'].setdefault(geometria_de(modelo, pulido, not doce), []).append(fila)
        P['piezas'][0] += 1

    def contar(k):                  # fase 11 v8: filas copiadas de la memoria de la celda
        P['piezas'][0] += k
    emit.contar = contar
    return emit


def _piel_ctx(W, cfg, now):
    """Lo que la piel mira del planeta entero, una vez por calculo: clusters,
    objetivos, suelos, fuego, pulso y, segun el tema, el mapa de alturas, los
    cauces y los cultivos (naturaleza) o la informacion de cada edificio
    (ciudad e industria). P['celdas']: las celdas que se dibujan, en orden."""
    tema = tema_de(cfg)
    paso = W.get('paso') or 0.125
    cl = clusters(W, cfg)
    tf, tc = objetivos(W, cfg, cl)
    suelos = [base_radius(W, cfg, i) for i in range(N)]
    bases = dict((i, _mul(normal_i(i), suelos[i])) for i in range(N))
    doce = cfg['nivel'] >= 12         # fase 12: una geometria por modelo, rugosidad en el alfa
    tiempo = cfg['nivel'] >= 17       # fase 17: el pulso balancea el dosel y enciende ventanas
    P = dict(W=W, cfg=cfg, now=now, tema=tema, paso=paso, cl=cl, tf=tf, tc=tc, suelos=suelos, bases=bases,
             doce=doce, respaldo=doce and cfg.get('respaldo', 0),
             arde=celdas_ardiendo(W, cfg) if cfg['nivel'] >= 14 else {},
             tiempo=tiempo, bq=beat_stop(W, cfg) if tiempo else 0.0, natural=tema == 'naturaleza',
             out=None, piezas=[0], nat_copas=[0])
    P['emit'] = _emisor_piel(P)
    if P['natural']:                    # fase 11 v5: la naturaleza legible (piel_natural)
        ter = terreno(W, cfg, cl)
        por_celda = cauces(W, cfg, cl, ter)['por_celda'] if cfg['nivel'] >= 13 else {}
        cult = cultivos(W, cfg, ter, por_celda, now, paso)     # fase 11 v8: bancales, riego y acequias
        bq = P['bq']
        ctx = dict(cl=cl, ter=ter, bases=suelos, cauces=por_celda,
                   sway=(lambda i: balanceo_filas(W, cfg, i, bq)) if tiempo else (lambda i: (0.0, 0.0)),
                   cerca=lambda i: cerca_de(W, cfg, i)
                   and not (cfg.get('impostores', 1) and _PRESUPUESTO['lleno']),
                   rio_cerca=lambda i: any(c in por_celda for c in [i] + list(NEIGH[i])),
                   res=dict(hojas=0, todas=0, ejemplares=0, emergentes=0, frutales={},
                            biomas=dict((b, 0) for b in BIOMAS)))
        P.update(ter=ter, cult=cult, ctx=ctx)
        P['celdas'] = [i for i in range(N) if W['vh'][i] > 0.005 and W['own'][i]]
    else:                               # fase 11 v10: la ciudad legible (build_ciudad)
        P['ctx'] = _ciudad_ctx(W, cfg, now, cl, tf, bases, paso)
        P['celdas'] = sorted(P['ctx']['info'])
    P['dib'] = set(P['celdas'])
    return P


def _piel_celda(P, i, out):
    """Dibuja la celda i en out (un dict {geometria: filas}). Las piezas de su
    cluster, si es la capital, y sus puentes van con ella."""
    W, cfg, now, paso = P['W'], P['cfg'], P['now'], P['paso']
    P['out'] = out
    bomba = _Bomba(W, cfg, now, out)    # fase 7 v12: el pumping de los impulsos
    if not P['natural']:
        ctx = P['ctx']
        n = normal_i(i)
        b = P['bases'][i]
        cw, cl_ = _cell_sizes(_len(b), i)
        bomba.abrir(i, b, n, cw, cl_)
        rug = rugosidad(cfg, W['vel'][i]) if P['doce'] else 1.0
        kb, fl = rebote(cfg, W, i, now, paso)
        P['piezas'][0] += piel_ciudad(W, cfg, ctx, i, rug, kb, fl, P['arde'], out, now, paso)
        bomba.cerrar()
        return
    vh = W['vh'][i]
    if vh <= 0.005 or not W['own'][i]:
        return
    n = normal_i(i)
    p0 = P['bases'][i]
    base = P['suelos'][i]
    cw, cl_ = _cell_sizes(base, i)
    bomba.abrir(i, p0, n, cw, cl_)
    rb = W['rebrote'][i] if cfg['nivel'] >= 15 else 0
    if rb == 1:                                 # fase 15: banco de semillas
        _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, vh, semilla_caos(i, 21), 7,
                    COL_SEMILLA, now, paso, 'semillas')
        bomba.cerrar()
        return
    if rb == 2:                                 # y brota, a saltos
        vh *= 0.25 + 0.75 * _stop((now - W['t_rebrote'][i]) / max(1e-6, rebrote_dur(cfg, paso)))
    sat = W['par'][i] >= 0
    pulido = W['vel'][i] >= cfg['vel_umbral']
    if P['doce']:                               # el material del tema, por la velocidad
        rug = rugosidad(cfg, W['vel'][i])
        ancho = W['vig'][i]
    else:
        rug, ancho = 1.0, 1.0
    lt, sc, amp = _luz_formacion(W, cfg, i, now)
    kb, fl = rebote(cfg, W, i, now, paso)
    if lt > 0:                                  # el latido hincha; su color va al borde (uTinte)
        vh *= 1.0 + amp * lt
    P['nat_copas'][0] += piel_natural_cache(W, cfg, P['ctx'], i, vh, rug, ancho, kb, fl, sat, pulido, P['arde'],
                                            P['emit'], out, now, paso, not P['doce'])
    bomba.cerrar()


def _piel_global(P, out):
    """Lo que no es de ninguna celda: el penacho de los volcanes (naturaleza) o las
    gruas (ciudad e industria, que se reparten entre las obras de todo el planeta)."""
    W, cfg, now, paso = P['W'], P['cfg'], P['now'], P['paso']
    P['out'] = out
    P['erupciones'] = 0
    if P['natural']:
        if P['ter'].get('volcanes'):    # motor v97: el penacho y la erupcion de cada volcan
            P['erupciones'] = _volcanes_filas(W, cfg, P['ter'], out, now, paso)
    else:
        P['piezas'][0] += emitir_gruas(W, cfg, P['ctx'], out, now, paso)


def _piel_resumen(P):
    """El resumen de la piel para la leyenda."""
    W, cfg, now, paso = P['W'], P['cfg'], P['now'], P['paso']
    cl, tf, tc = P['cl'], P['tf'], P['tc']
    obras = medias = 0
    compas = paso * max(1, int(cfg['steps_per_beat'])) * max(1, int(cfg['beats_per_bar']))
    vistos = set()
    for i in range(N):
        if W['occ'][i] <= 0:
            continue
        k_ = cl['de'][i]
        grupo = cl['celdas'][k_] if k_ >= 0 else [i]
        clave = ('c', k_) if k_ >= 0 else ('i', i)
        if clave in vistos:
            continue
        vistos.add(clave)
        pend = [c for c in grupo if W['et_f'][c] != tf[c] or W['et_c'][c] != tc[c]]
        if pend:
            obras += 1
            ult = max(max(W['t_et_f'][c], W['t_et_c'][c], W['t_gate'][c]) for c in grupo)
            if now - ult > compas:
                medias += 1
    tam = [len(v) for v in cl['celdas'].values()]
    res = dict(tema=P['tema'], clusters=len(tam), max=max(tam or [0]), compuestos=0,
               piezas=P['piezas'][0], obras=obras, medias=medias)
    if not P['natural']:
        res['ciudad'] = _ciudad_resumen(W, cfg, P['ctx'])
        return res
    ter, cult = P['ter'], P['cult']
    _, ln = _limites_pisos(cfg)
    r_ = P['ctx']['res']
    _PRESUPUESTO['lleno'] = r_['todas'] > presupuesto_hojas(cfg)
    res.update(ejemplares=r_['ejemplares'], hojas=r_['hojas'], emergentes=r_['emergentes'],
               biomas=dict(r_['biomas']), frutales=r_['frutales'], hibridos=ter.get('hibridos', {}),
               inundados=cult['inundados'], parcelas=cult['parcelas'])
    res.update(islas=ter.get('islas', 0), archipielagos=ter.get('archipielagos', 0),
               volcanes=len(ter.get('volcanes', [])), erupciones=P.get('erupciones', 0))
    res.update(copas=P['nat_copas'][0], montes=ter['montes'], cordilleras=ter['cordilleras'],
               nevadas=sum(1 for c in range(N) if ter['centro'][c] >= ln * ter['hmax']),
               cerca=sum(1 for c in range(N) if W['occ'][c] > 0 and lod_cerca(W, cfg, c)))
    return res


def build_piel(W, cfg, now, out):
    """Las formaciones como modelos del tema: compuesto, puentes del cluster,
    pieza protagonista, cadenas de transito y particulas. Devuelve el resumen
    para la leyenda. La ciudad la dibuja piel_ciudad (fase 11 v10). La piel
    entera en este fotograma (Refrescopiel 0, y las autopruebas)."""
    P = _piel_ctx(W, cfg, now)
    for i in P['celdas']:
        _piel_celda(P, i, out)
    _piel_global(P, out)
    return _piel_resumen(P)


# --- el bufer de una vuelta: un cubo por celda ---------------------------------------

def _res_foto(r):
    """Copia del resumen de la leyenda (dict, set, list y numeros) para restar."""
    if isinstance(r, dict):
        return dict((k, _res_foto(v)) for k, v in r.items())
    if isinstance(r, (set, list)):
        return type(r)(r)
    return r


def _res_delta(a, b):
    """Lo que una celda anade al resumen: b - a (numeros, listas de numeros,
    conjuntos y dicts, recursivamente); lo demas, el valor nuevo si cambia."""
    if isinstance(b, dict):
        a = a if isinstance(a, dict) else {}
        d = {}
        for k, v in b.items():
            if k not in a:
                d[k] = _res_foto(v)
            elif a[k] != v:
                d[k] = _res_delta(a[k], v)
        return d
    if isinstance(b, set):
        return b - (a if isinstance(a, set) else set())
    if isinstance(b, bool) or not isinstance(b, (int, float, list)):
        return b
    if isinstance(b, list):
        if isinstance(a, list) and len(a) == len(b) and all(isinstance(x, (int, float)) for x in a + b):
            return [y - x for x, y in zip(a, b)]
        return list(b)
    return b - a if isinstance(a, (int, float)) and not isinstance(a, bool) else b


def _res_suma(acc, d):
    """Suma al resumen acc lo que anade una celda (lo cambia y lo devuelve)."""
    if isinstance(d, dict):
        acc = acc if isinstance(acc, dict) else {}
        for k, v in d.items():
            acc[k] = _res_suma(acc.get(k), v)
        return acc
    if isinstance(d, set):
        return (acc if isinstance(acc, set) else set()) | d
    if isinstance(d, list):
        if isinstance(acc, list) and len(acc) == len(d) and \
                all(isinstance(x, (int, float)) for x in acc + d):
            return [x + y for x, y in zip(acc, d)]
        return list(d)
    if isinstance(d, (int, float)) and not isinstance(d, bool) and isinstance(acc, (int, float)) \
            and not isinstance(acc, bool):
        return acc + d
    return d


def _piel_cubo(P, i):
    """El cubo de la celda i: dict(filas {geometria: filas}, res lo que anade al
    resumen, gruas las que pide, piezas, copas). None si la celda no se dibuja."""
    if i not in P['dib']:
        return None
    ctx = P['ctx']
    antes = _res_foto(ctx['res'])
    g0 = len(ctx.get('gruas', ()))
    p0, c0 = P['piezas'][0], P['nat_copas'][0]
    filas = {}
    _piel_celda(P, i, filas)
    return dict(filas=filas, res=_res_delta(antes, ctx['res']), gruas=list(ctx.get('gruas', ())[g0:]),
                piezas=P['piezas'][0] - p0, copas=P['nat_copas'][0] - c0)


def _vuelta_cerrar(P, cubos):
    """Cierra una vuelta: las piezas globales y el resumen, con lo que dicen los
    cubos (calculados con P o con otro contexto, en el camino inmediato).
    Devuelve dict(cubos, glob {geometria: filas}, res, t)."""
    ctx = P['ctx']
    res0 = _res_foto(ctx['res'])
    plantilla = _piel_ctx_res(P)
    ctx['res'] = plantilla
    gruas = []
    piezas = copas = 0
    for i in sorted(cubos):
        cu = cubos[i]
        _res_suma(plantilla, cu['res'])
        gruas.extend(cu['gruas'])
        piezas += cu['piezas']
        copas += cu['copas']
    if 'gruas' in ctx:
        ctx['gruas'] = gruas
    P['piezas'][0], P['nat_copas'][0] = piezas, copas
    glob = {}
    _piel_global(P, glob)
    res = _piel_resumen(P)
    ctx['res'] = res0
    return dict(cubos=cubos, glob=glob, res=res, t=P['now'])


def _piel_ctx_res(P):
    """El resumen de la leyenda vacio, como lo deja el contexto antes de la primera celda."""
    if P['natural']:
        return dict(hojas=0, todas=0, ejemplares=0, emergentes=0, frutales={},
                    biomas=dict((b, 0) for b in BIOMAS))
    return _ciudad_res_vacio(P['W'], P['cfg'])


def _piel_montar(pub):
    """Las filas publicadas por geometria: las celdas en orden y despues las
    globales. Las listas se montan una vez por publicacion (y por camino
    inmediato) y se reparten por referencia: filas iguales, CHOP sin recocer."""
    mont = {}
    for i in sorted(pub['cubos']):
        for g, f in pub['cubos'][i]['filas'].items():
            mont.setdefault(g, []).extend(f)
    for g, f in pub['glob'].items():
        mont.setdefault(g, []).extend(f)
    pub['mont'] = mont
    return mont


def _firma_piel(W, cfg):
    """Lo que, si cambia, vacia los bufers y publica una vuelta completa en el
    fotograma: el mundo (Resetmundo), el fin de ciclo (Forzarciclo), el tema, la
    reticula, la biblioteca y cualquier parametro de la pagina Fase11."""
    f11 = tuple((k, cfg.get(k)) for k in PIEL_CFG)
    return (id(W), W.get('gen'), len(W.get('shells', ())), GRID['lo'], GRID['hi'], cfg['nivel'], cfg.get('tema'),
            id(cfg.get('catalogo')), _clave_biblio(cfg), f11, bool(cfg.get('turnos', 1)))


def _eventos_piel(W, cfg, T, now):
    """Las celdas que han recibido algo desde el fotograma anterior: (las que han
    cambiado de ocupacion, especie, dueno o columna: tambien sus vecinas; las que
    solo se encienden: nota, impulso, fin del tinte o del pumping)."""
    k_luz = len(EVENTO_CAMPOS) - len(EVENTO_LUZ)
    cols = [W[k] if k in W else [0] * N for k in EVENTO_CAMPOS]
    claves = list(zip(*(cols + [[len(x) for x in W['cols']]])))
    bomba = W.get('bomba') or {}
    imp = W.get('imp_t') or {}
    prev = T.get('claves')
    T['claves'] = claves
    est, luz = set(), set()
    if prev is not None and len(prev) == len(claves):
        for i, (a, b) in enumerate(zip(prev, claves)):
            if a != b:
                if a[:k_luz] != b[:k_luz] or a[-1] != b[-1]:
                    est.add(i)
                else:
                    luz.add(i)
    bp = T.get('bomba', set())
    bn = set(bomba)
    luz.update(bp ^ bn)
    T['bomba'] = bn
    ip = T.get('imp', {})
    luz.update(i for i, t in imp.items() if ip.get(i) != t and 0 <= i < N)
    T['imp'] = dict(imp)
    fines = T.setdefault('fines', {})
    for i, t in list(fines.items()):
        if now >= t:
            luz.add(i)
            del fines[i]
    return est, luz - est


def _vecindad_piel(ev, cls, luz=()):
    """Las celdas del camino inmediato: las que han cambiado, sus vecinas y la
    capital de sus clusters (en cada reparto de clusters de cls: antes y despues;
    la capital lleva las piezas del cluster), y las que solo se encienden (luz).
    El resto del cluster, en la vuelta."""
    d = set(ev) | set(luz)
    for i in ev:
        d.update(NEIGH[i])
    for cl in cls:
        if cl is None:
            continue
        for i in ev:
            k = cl['de'][i]
            if k >= 0:
                d.add(cl['capital'][k])
    return d


def build_piel_refresco(W, cfg, now, out):
    """build_piel por turnos (fase 11 v18, motor v101): ver la cabecera. Solo en el
    fotograma de TouchDesigner (build_instances con refresco)."""
    dt = float(cfg.get('refresco_piel', 0.0))
    T = _TURNOS
    if dt <= 0 or cfg['nivel'] < 11:
        T.clear()
        T['info'] = dict(modo='entera')
        return build_piel(W, cfg, now, out)
    t0 = _time.perf_counter()
    turnos = bool(cfg.get('turnos', 1))
    fdt = max(1e-3, float(W.get('foto_dt') or FOTO_DEF))
    firma = _firma_piel(W, cfg)
    ev, ev_luz = _eventos_piel(W, cfg, T, now)
    info = dict(modo='turnos' if turnos else 'vuelta', inmediatas=0, celdas=0, turno=0, turnos=0)
    if T.get('firma') != firma or T.get('pub') is None:
        # reinicio: una vuelta completa, publicada en este fotograma
        P = _piel_ctx(W, cfg, now)
        cubos = dict((i, c) for i, c in ((i, _piel_cubo(P, i)) for i in P['celdas']) if c is not None)
        T['pub'] = _vuelta_cerrar(P, cubos)
        _piel_montar(T['pub'])
        T.update(firma=firma, vuelta=None, cl=P['cl'], t_sig=now + dt, fines={})
        info.update(celdas=len(P['celdas']), turno=1, turnos=1, reinicio=True)
        ev, ev_luz = set(), set()
    pub = T['pub']
    V = T.get('vuelta')
    if ev or ev_luz:                    # el camino inmediato, en este fotograma
        Pn = _piel_ctx(W, cfg, now)
        D = _vecindad_piel(ev, (T.get('cl'), Pn['cl']), ev_luz)
        T['cl'] = Pn['cl']
        pasos_t = float(cfg.get('pasos_tinte', 4)) * Pn['paso']
        for i in sorted(D):
            cu = _piel_cubo(Pn, i)
            for dst in (pub['cubos'], V['cubos'] if V is not None else None):
                if dst is None:
                    continue
                if cu is None:
                    dst.pop(i, None)
                else:
                    dst[i] = cu
            if V is not None:
                V['hechas'].add(i)
            if not Pn['natural'] and (i in ev or i in ev_luz) and cfg.get('tinte_ventanas', 1) and \
                    W['lat_s'][i] in (1, 2):
                fin = W['t_gate'][i] + pasos_t      # el fin del tinte la vuelve a marcar
                if fin > now:
                    T['fines'][i] = fin + 1e-6
        _piel_montar(pub)
        info['inmediatas'] = len(D)
    if turnos:
        if V is None:                   # una vuelta nueva: su instante de publicacion
            t_pub = now + dt
            V = T['vuelta'] = dict(t_pub=t_pub, P=None, cola=None, cubos={}, hechas=set(), k=0,
                                   K=max(1, int(math.ceil(dt / fdt - 1e-6))))
        if V['P'] is None:              # el contexto, una vez por vuelta (el primer turno)
            V['P'] = _piel_ctx(W, cfg, V['t_pub'])
            V['cola'] = list(V['P']['celdas'])
            V['tam'] = max(1, int(math.ceil(len(V['cola']) / float(V['K']))))
        P = V['P']
        tarde = now >= V['t_pub'] - 1e-9
        n = len(V['cola']) if tarde else V['tam']
        hechas = 0
        while V['cola'] and hechas < n:
            i = V['cola'].pop(0)
            if i in V['hechas']:
                continue
            cu = _piel_cubo(P, i)
            if cu is not None:
                V['cubos'][i] = cu
            hechas += 1
        V['k'] += 1
        info.update(turno=min(V['k'], V['K']), turnos=V['K'], celdas=hechas)
        if not V['cola'] and now + 0.5 * fdt >= V['t_pub']:
            pub = T['pub'] = _vuelta_cerrar(P, V['cubos'])
            _piel_montar(pub)
            T['vuelta'] = None
            info['publica'] = True
    elif now >= T.get('t_sig', 0.0):    # Turnos apagado: la vuelta entera al publicar
        P = _piel_ctx(W, cfg, now)
        cubos = dict((i, c) for i, c in ((i, _piel_cubo(P, i)) for i in P['celdas']) if c is not None)
        pub = T['pub'] = _vuelta_cerrar(P, cubos)
        _piel_montar(pub)
        T['cl'] = P['cl']
        T['t_sig'] = now + dt
        info.update(celdas=len(P['celdas']), turno=1, turnos=1, publica=True)
    for g, f in pub['mont'].items():
        out.setdefault(g, []).extend(f)
    info.update(refresco=dt, ms=(_time.perf_counter() - t0) * 1000.0)
    T['info'] = info
    return pub['res']




def _volcanes_filas(W, cfg, ter, out, now, paso):
    """Motor v97: el penacho de cada volcan (bocanadas de la geometria 'humo', que
    anima la GPU) y, en erupcion, brasas y ceniza. Devuelve los que estan en erupcion."""
    hum = out.setdefault('humo', [])
    lim = limit(cfg)
    n_er = 0
    for c, alto in ter['volcanes']:
        n = NORMALS[c]
        S = suelo(W, cfg, c)
        cw, cl_ = _cell_sizes(S, c)
        m_ = min(cw, cl_)
        p = _mul(n, S + ter['centro'][c] + 0.5 * CRATER_HONDO * alto)
        er = erupcion(cfg, c, now, paso)
        nb = 3 if er <= 0.0 else 8
        col = COL_HUMO['gris'] if er <= 0.0 else _mix(COL_HUMO['gris'], COL_HUMO['negro'], 0.7)
        for q in range(nb):
            hum.append(fila_humo(p, (0.07 if er <= 0.0 else 0.13) * m_, (0.9 if er <= 0.0 else 1.8) * lim,
                                 0.35 * m_, col, (q + _hash01(c, 721)) / float(nb), er <= 0.0))
        if er > 0.0:
            n_er += 1
            parts = out.setdefault('particulas', [])
            _particulas(parts, n, p, 0.5 * cw, 0.5 * cl_, 0.8 * lim * er, semilla_caos(c, 23), 10, COL_BRASA,
                        now, paso, 'brasas')
            _particulas(parts, n, p, cw, cl_, 0.9 * lim, semilla_caos(c, 29), 6, COL_CENIZA, now, paso, 'ceniza')
    return n_er


# --- la ciudad: lenguaje, tipo y obra de cada celda ---------------------------------

# --- la industria: epoca y recurso (fase 11 v11) --------------------------------------
EPOCAS = ['vapor', 'acero', 'quimica']
EPOCA_MODOS = ['eras', 'vapor', 'acero', 'quimica']
RECURSOS = ['carbon', 'chatarra', 'escoria', 'mineral']
RECURSO_DE_TEMA = dict(naturaleza='carbon', ciudad='chatarra', industria='escoria')
COL_RECURSO = dict(carbon=(0.07, 0.07, 0.07), chatarra=(0.46, 0.40, 0.34), escoria=(0.24, 0.21, 0.23),
                   mineral=(0.62, 0.36, 0.20))
COL_HUMO = dict(negro=(0.10, 0.10, 0.10), gris=(0.42, 0.42, 0.43), blanco=(0.92, 0.92, 0.92))
COL_LLAMA = (1.0, 0.55, 0.12)            # antorcha y colada: incandescentes
COL_RED = COL_RED_DEF                    # el violeta electrico de la red (reservado)


def epoca_actual(cfg, W=None):
    """0 vapor, 1 acero, 2 quimica: por las eras enterradas (0-2, 3-5, 6+) o fija (Epoca)."""
    modo = int(cfg.get('epoca', 0))
    if modo in (1, 2, 3):
        return modo - 1
    eras = int(W.get('gen', 0)) if W is not None else 0
    return 0 if eras <= 2 else (1 if eras <= 5 else 2)


def recurso_celda(W, cfg, i):
    """Lo que saca la mina de la celda i: con Recursos, lo que guarda la concha de
    abajo (el registro de la fase 15: naturaleza carbon, ciudad chatarra,
    industria escoria; ninguna, mineral); sin Recursos, la semilla."""
    if not cfg.get('recursos', 1):
        x = logistica(semilla_caos(W['vel'][i], i + 71), 3.91, 1)[0]
        return RECURSOS[min(3, int(x * 4))]
    col = W['cols'][i] if i < len(W.get('cols', [])) else []
    for s_, _ in reversed(col or []):
        if 0 <= s_ < len(W['shells']):
            t = W['shells'][s_].get('tema')
            if t in RECURSO_DE_TEMA:
                return RECURSO_DE_TEMA[t]
            break
    return 'mineral'


def lenguaje_celda(cfg, i, W=None):
    """0 frio, 1 templado, 2 calido: por la latitud (los extremos del registro,
    frio; el centro, calido), fijo o mezcla (el mapa logistico por celda)."""
    if tema_de(cfg) == 'industria':     # fase 11 v11: en la industria, la epoca
        return epoca_actual(cfg, W)
    modo = int(cfg.get('lenguaje', 0))
    if modo in (1, 2, 3):
        return modo - 1
    if modo == 4:
        return min(2, int(logistica(semilla_caos(313, i), 3.91, 1)[0] * 3))
    lat = abs(latitud(i)) / 90.0
    return 0 if lat >= LENG_FRIO else (2 if lat < LENG_CALIDO else 1)


def mutacion_actual(W, cfg):
    """Mutacion (0-1): el mando, o la saturacion del modular (fase 19)."""
    if int(cfg.get('mutacion_fuente', 0)) == 1 and cfg['nivel'] >= 19:
        return max(0.0, min(1.0, float(W['modular'].get('saturacion', 0.0))))
    return max(0.0, min(1.0, float(cfg.get('mutacion', 0.5))))


def etapa_ciudad(cfg, esp, occ):
    """La etapa (1, 2...) del tipo de edificio por la ocupacion, con los
    umbrales de la fase 4: informal 1 caseta, 2 casa, 3 tres plantas, Umbralram-1
    racimo, fusion-1 barrio, corona-1 torre; planificada 1 pabellon, 2 bloque,
    Umbralram-1 manzana, fusion-1 podio, corona-1 rascacielos."""
    tb, tf, tc = int(cfg['th_branch']) - 1, int(cfg['th_fusion']) - 1, int(cfg['th_crown']) - 1
    if occ <= 1:
        return 1
    if esp == 'informal':
        if occ == 2:
            return 2
        return 3 if occ < tb else (4 if occ < tf else (5 if occ < tc else 6))
    return 2 if occ < tb else (3 if occ < tf else (4 if occ < tc else 5))


def occ_inicio(cfg, esp, e):
    """La primera ocupacion de la etapa e."""
    tb, tf, tc = int(cfg['th_branch']) - 1, int(cfg['th_fusion']) - 1, int(cfg['th_crown']) - 1
    if esp == 'informal':
        return [1, 2, 3, tb, tf, tc][e - 1]
    return [1, 2, tb, tf, tc][e - 1]


def pasos_obra(esp, tipo):
    """Los pasos de la obra hacia ese tipo (terminada = len). En la industria,
    terminada = humea: la puesta en marcha es el ultimo paso."""
    if esp == 'informal':
        return ['bloque']
    if esp in ('mina', 'energia'):
        if tipo in ('brote', 'aserradero'):
            return ['montaje']
        return (['solar', 'montaje', 'puesta'] if esp == 'mina'
                else ['solar', 'excavacion', 'estructura', 'montaje', 'puesta'])
    if tipo == 'pabellon':
        return ['solar', 'esqueleto', 'fachada']
    return ['solar', 'excavacion', 'nucleo', 'esqueleto', 'fachada'] + (['coronacion'] if tipo == 'rascacielos'
                                                                       else [])


CONSTRUIDOS = ('ciudad', 'industria')        # los temas que salen de la biblioteca de edificios
ESP_COD = dict(informal=1, planificada=2, mina=3, energia=4)
COD_ESP = dict((v, k) for k, v in ESP_COD.items())


def _codigo_edi(cfg, W, i):
    esp = especie_de(tema_de(cfg), W['own'][i])
    e = etapa_ciudad(cfg, esp, W['occ'][i])
    if W['par'][i] >= 0:
        e = min(e, 2)                   # los satelites, pequenos
    return ESP_COD.get(esp, 2) * 10 + e


def _de_codigo(c):
    esp = COD_ESP.get(c // 10, 'planificada')
    return esp, c % 10, TIPOS[esp][c % 10 - 1]


def _paso_reinicio(pasos):
    """El paso al que vuelve una obra a medias que cambia de etapa."""
    for p in ('esqueleto', 'estructura'):
        if p in pasos:
            return pasos.index(p)
    return 0


def ciudad_sync(W, cfg, i, now):
    """El tipo que toca a la celda i y su obra: una etapa nueva (o una planta
    nueva) empieza obra con el lenguaje y la mutacion de ahora; una bajada (la
    erosion) deja lo de abajo hecho, con polvo. Devuelve True si empieza algo."""
    if W['occ'][i] <= 0 or not W['own'][i]:
        if W['edi'][i] >= 0:
            W['edi'][i], W['obra'][i], W['edi_occ'][i] = -1, 0, 0
            W['leng'][i], W['mut'][i] = -1, -1.0
        return False
    code = _codigo_edi(cfg, W, i)
    old = W['edi'][i]
    esp, e, tipo = _de_codigo(code)
    pasos = pasos_obra(esp, tipo)
    sin_obra = not cfg.get('obra', 1)
    o = W['occ'][i]
    if old != code:
        sube = old >= 0 and old // 10 == code // 10 and code > old
        W['edi'][i] = code
        W['edi_occ'][i] = o
        W['plantas_ant'][i] = 0.0
        if old < 0 or sube:
            hecho = old >= 0 and W['obra'][i] >= len(pasos_obra(*_de_codigo(old)[::2]))
            if sin_obra:
                W['obra'][i] = len(pasos)
            elif esp != 'informal' and old >= 0 and not hecho:
                W['obra'][i] = min(W['obra'][i], _paso_reinicio(pasos))
            else:
                W['obra'][i] = 0
            W['ant_obra'][i] = -1
            W['t_obra'][i] = now
            W['leng'][i] = lenguaje_celda(cfg, i, W)
            W['mut'][i] = mutacion_actual(W, cfg)
            return True
        # baja o cambia de especie: lo de abajo queda hecho; se cae lo de arriba
        W['obra'][i] = len(pasos)
        if old // 10 != code // 10 or W['leng'][i] < 0:
            W['leng'][i] = lenguaje_celda(cfg, i, W)
        _polvo(W, now, i, 'polvo', 6)
        return False
    if o != W['edi_occ'][i]:            # la misma etapa, otra ocupacion
        crece = o > W['edi_occ'][i]
        W['edi_occ'][i] = o
        if crece and not sin_obra:
            if esp == 'informal':       # una planta nueva: bloque gris con varillas
                W['obra'][i], W['ant_obra'][i], W['t_obra'][i] = 0, -1, now
                return True
            if W['obra'][i] >= len(pasos) and esp == 'planificada':     # mas plantas del mismo modulo
                W['plantas_ant'][i] = plantas_de(cfg, W, i, o - 1)
                W['obra'][i] = pasos.index('esqueleto')
                W['ant_obra'][i], W['t_obra'][i] = -1, now
                return True
        elif not crece:
            _polvo(W, now, i, 'polvo', 4)
    return False


def _paso_obra(W, i, k, now):
    W['ant_obra'][i] = W['obra'][i]
    W['obra'][i] = k
    W['t_obra'][i] = now


def ciudad_gate(W, cfg, i, now):
    """Una nota en la celda i (desde gate_piel): la mutacion de lo que se
    construya a partir de ahora y, con Avance = gates, un paso de su obra."""
    if tema_de(cfg) not in CONSTRUIDOS or cfg['nivel'] < 11 or not 0 <= i < N:
        return
    W['mut'][i] = mutacion_actual(W, cfg)
    empieza = ciudad_sync(W, cfg, i, now)
    if W['edi'][i] < 0 or empieza or int(cfg.get('avance', 0)) != 0:
        return
    if cfg['nivel'] >= 14 and W['derribo'][i]:
        return
    esp, e, tipo = _de_codigo(W['edi'][i])
    if W['obra'][i] < len(pasos_obra(esp, tipo)):
        _paso_obra(W, i, W['obra'][i] + 1, now)


def colonos_logicos(W, cfg, i):
    """(parasitos, unidades del marco) que pide la logica en la celda i."""
    if W['sp'][i] != HIB or W['occ'][i] <= 0:
        return 0, 0
    n = notas_colonas(W, i)
    if tema_de(cfg) == 'industria':     # fase 11 v11: bancos de la corta; niveles del bastidor
        if W['own'][i] == ARQ:
            return min(int(cfg['max_bancos']), int(round(cfg['bancos_por_nota'] * n))), 0
        return 0, 2 * min(int(cfg['max_bastidor']), n)
    if W['own'][i] == ARQ:
        return min(int(cfg['max_parasitos']), int(round(cfg['parasitos_por_nota'] * n))), 0
    return 0, 2 * min(int(cfg['max_marco']), n)


def ciudad_tick(W, cfg, now, paso, playing=True):
    """Las obras que van solas (Avance = pasos), el derribo hacia atras y los
    mutantes visibles, que persiguen a la logica uno por paso (los parasitos de
    abajo arriba al irse; del marco, primero las capsulas)."""
    if tema_de(cfg) not in CONSTRUIDOS or cfg['nivel'] < 11:
        return
    espera = max(1, int(cfg['pasos_etapa'])) * paso
    pasos_av = int(cfg.get('avance', 0)) == 1
    for i in range(N):
        if W['occ'][i] <= 0:
            if W['edi'][i] >= 0:
                ciudad_sync(W, cfg, i, now)
            W['par_vis'][i] = W['marco_vis'][i] = 0
            continue
        ciudad_sync(W, cfg, i, now)
        esp, e, tipo = _de_codigo(W['edi'][i])
        tope = len(pasos_obra(esp, tipo))
        if now - W['t_obra'][i] >= espera:
            if cfg['nivel'] >= 14 and W['derribo'][i]:
                if W['obra'][i] > 0:
                    _paso_obra(W, i, W['obra'][i] - 1, now)
            elif pasos_av and playing and W['obra'][i] < tope:
                _paso_obra(W, i, W['obra'][i] + 1, now)
        pl, ml = colonos_logicos(W, cfg, i)
        if now - W['t_vis'][i] >= paso:
            for clave, obj in (('par_vis', pl), ('marco_vis', ml)):
                v = W[clave][i]
                if v != obj:
                    W[clave][i] = v + (1 if obj > v else -1)
                    W['t_vis'][i] = now


def cerrar_obras_ciudad(W, cfg):
    """Fin de ciclo: los edificios, terminados; los mutantes, al dia."""
    if tema_de(cfg) not in CONSTRUIDOS:
        return
    for i in range(N):
        if W['occ'][i] <= 0:
            continue
        ciudad_sync(W, cfg, i, -99.0)
        if W['edi'][i] >= 0:
            esp, e, tipo = _de_codigo(W['edi'][i])
            W['obra'][i] = W['ant_obra'][i] = len(pasos_obra(esp, tipo))
            W['t_obra'][i] = -99.0
        W['par_vis'][i], W['marco_vis'][i] = colonos_logicos(W, cfg, i)


def obras_ciudad(W, cfg):
    """Celdas con un edificio a medias: {celda: paso}."""
    out = {}
    if cfg['nivel'] < 11 or tema_de(cfg) not in CONSTRUIDOS:
        return out
    for i in range(N):
        if W['occ'][i] > 0 and W['edi'][i] >= 0:
            esp, e, tipo = _de_codigo(W['edi'][i])
            p = pasos_obra(esp, tipo)
            if W['obra'][i] < len(p):
                out[i] = p[W['obra'][i]]
    return out


def diseno_celda(W, cfg, i, esp=None, e=None):
    """(diseno, variante) del edificio de la celda i: el catalogo de su etapa y
    el mapa logistico sembrado con la velocidad fundadora y la celda (la misma
    historia, el mismo edificio); Fijartipo lo fuerza para probar."""
    if esp is None:
        esp, e, _ = _de_codigo(_codigo_edi(cfg, W, i))
    lista = [d for d in modelos_de(cfg, tema_de(cfg), esp, 'etapa%d' % e) if d in _GEN_EDI] or \
        DISENOS_TIPO[TIPOS[esp][e - 1]]
    xs = logistica(semilla_caos(W['vel'][i], i + 131 * e), cfg['caos'], 3)
    f = int(cfg.get('fijar_tipo', 0))
    d = lista[min(len(lista) - 1, f - 1 if f > 0 else int(xs[0] * len(lista)))]
    mut = W['mut'][i] if W['mut'][i] >= 0 else mutacion_actual(W, cfg)
    if d == 'torsion' and mut < 0.25:   # sin mutacion, torres rectas
        d = 'prisma'
    nv = variantes_de(cfg, d)
    return d, min(nv - 1, int(xs[1] * nv)), int(xs[2] * 4)


def plantas_de(cfg, W, i, occ=None):
    """Plantas del edificio de la celda i: las de su diseno y, en la planificada,
    las que anade cada ocupacion de la etapa (el mismo modulo); en la torre
    autoconstruida, los cuartos que se ven."""
    occ = W['occ'][i] if occ is None else occ
    esp = especie_de(tema_de(cfg), W['own'][i])
    e = etapa_ciudad(cfg, esp, occ)
    if W['par'][i] >= 0:
        e = min(e, 2)
    d, v, _ = diseno_celda(W, cfg, i, esp, e)
    ex = edificio(cfg, d, v)
    k = max(0, occ - occ_inicio(cfg, esp, e))
    if ex['modo'] == 'corte':
        return float(min(ex['alto'], 7 + 2 * k))
    if esp == 'informal':
        return ex['alto']
    if esp in ('mina', 'energia'):      # la industria: el gate (vigor, fase 12) alarga chimeneas
        vig = W['vig'][i] if cfg['nivel'] >= 12 else 1.0
        return ex['alto'] * (1.0 + 0.12 * k) * (0.85 + 0.15 * vig)
    paso = dict(pabellon=0.0, bloque=3.0, manzana=1.0, podio=3.0, rascacielos=4.0)[TIPOS[esp][e - 1]]
    return ex['alto'] + paso * k


def alto_planta(cfg):
    return max(0.005, float(cfg.get('alto_planta', 0.08))) * limit(cfg)


def lod_ciudad(W, cfg, i):
    """Cerca (remates pequenos): la camara de superficie, o la celda mide en
    pantalla Lodciudad px o mas con la camara de globo."""
    if cfg.get('superficie'):
        return True
    R = top_radius(W, cfg) + RETICULA_SOBRE_DEF
    px = ENCUADRE_DEF * 720.0 / (2.0 * R)
    lod = cfg.get('lod_ind', 60.0) if tema_de(cfg) == 'industria' else cfg.get('lod_ciudad', 60.0)
    return min(SIZE_EW[i], SIZE_NS[i]) * base_radius(W, cfg, i) * px >= lod


def nivel_ventanas(alfa):
    """El nivel de ventanas (0-4) del alfa de una instancia de la piel
    (rugosidad + 2 x nivel + 10 x lenguaje en los edificios)."""
    a = float(alfa)
    a -= 10.0 * math.floor(a / 10.0 + 1e-4)
    return int(math.floor(a * 0.5 + 1e-4))


def lenguaje_fila(alfa):
    return int(math.floor(float(alfa) / 10.0 + 1e-4))


def _resolver_remate(tipo, leng):
    """El remate segun el lenguaje: la cubierta generica de la informal y de la
    planificada cambia con el clima."""
    if tipo == 'techo':
        return (['dosaguas', 'chimenea'], [], ['pretil'])[leng]
    if tipo == 'techo1':
        return (['dosaguas'], ['unagua'], ['unagua'])[leng]
    if tipo == 'cubierta':
        return (['maquinaria'], ['antena'], ['pergola'])[leng]
    return [tipo]


def _dentro(ex, x, z, margen=0.02):
    """El punto (x, z) cae sobre algun volumen del ejemplar (una casa), con margen."""
    for v in ex['vols']:
        pl = _planta_vol(v)
        m = len(pl)
        sobre = True
        for k in range(m):
            a, b = pl[k], pl[(k + 1) % m]
            nx, nz = b[1] - a[1], -(b[0] - a[0])
            ln = math.sqrt(nx * nx + nz * nz) or 1.0
            if ((x - a[0]) * nx + (z - a[1]) * nz) / ln > margen:
                sobre = False
                break
        if sobre:
            return True
    return False


def puestos_colonia(ex, n, mut, semilla, alto):
    """Donde van los n parasitos de una colonia, en el orden en que llegan:
    primero la azotea (o el patio y las cubiertas de un podio o una manzana),
    luego la fachada, planta a planta hacia abajo. [(x, y, z, nx, nz, nivel)]
    en coordenadas del ejemplar (y 0-1); nivel 0 azotea, 1 fachada, 2 colgado
    de otro parasito. Todo del mapa logistico."""
    if n <= 0:
        return []
    xs = logistica(semilla, 3.91, 3 * n + 8)
    vol = max(ex['vols'], key=lambda v: v['w'] * v['d'] * (v['y1'] - v['y0']))
    out = []
    techo = []
    if ex['diseno'] in ('cerda', 'peine', 'podio'):     # el patio y las cubiertas, primero
        bajo = min(ex['vols'], key=lambda v: v['y1'])
        for a, b in ((0.0, 0.0), (0.12, -0.1), (-0.1, 0.12), (0.15, 0.15)):
            techo.append((a, 0.0 if ex['diseno'] == 'cerda' else bajo['y1'], b, 0.0, 0.0, 0))
    for a, b in ((0.0, 0.0), (0.28, 0.24), (-0.26, -0.22), (0.24, -0.28), (-0.22, 0.27), (0.0, 0.32)):
        techo.append((vol['x'] + a * vol['w'], vol['y1'], vol['z'] + b * vol['d'], 0.0, 0.0, 0))
    out += techo
    planta = 1.0 / max(1.0, alto)
    caras = ((1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0))
    k = 0
    f = 1
    while len(out) < n and f < 400:
        y = vol['y1'] - f * planta * 1.15
        if y < vol['y0'] + 0.3 * planta:
            break
        for q in range(4):
            nx, nz = caras[(q + f) % 4]
            u = xs[(k % len(xs))] - 0.5
            k += 1
            vuela = 0.5 + 0.8 * mut          # hasta 0,8 vanos fuera (mas con Mutacion)
            x = vol['x'] + nx * vol['w'] * 0.5 + (0.0 if nx else u * vol['w'] * 0.8)
            z = vol['z'] + nz * vol['d'] * 0.5 + (0.0 if nz else u * vol['d'] * 0.8)
            out.append((x, y, z, nx * vuela, nz * vuela, 1))
            if mut > 0.6 and k % 3 == 0:     # un parasito colgado de otro
                out.append((x, y - planta * 0.9, z, nx * (vuela + 1.1), nz * (vuela + 1.1), 2))
        f += 1
    return out[:n]


def pilares_marco(ex, m):
    """Los nudos de la reticula del marco (modulo m) que caen en los callejones,
    nunca sobre una casa: [(x, z)]."""
    g = max(2, int(round(1.0 / max(0.08, m))))
    paso = 1.0 / g
    nudos = [(-0.5 + a * paso, -0.5 + b * paso) for a in range(g + 1) for b in range(g + 1)]
    libres = [p for p in nudos if not _dentro(ex, p[0], p[1], 0.012)]
    return libres, g, paso


# --- dibujar la ciudad ------------------------------------------------------------------

_INFO_CIU = {}
_CFG_CIU = ('th_branch', 'th_fusion', 'th_crown', 'caos', 'fijar_tipo', 'variantes_ciudad', 'alto_planta',
            'oblicuidad', 'retranqueo', 'torsion_max', 'lenguaje', 'height_factor', 'shell_thick', 'tema',
            'epoca', 'nivel')


def info_ciudad(W, cfg, i, cl=None, clave_cfg=None):
    """Lo que hace falta para dibujar el edificio de la celda i: especie, etapa,
    tipo, diseno, variante, giro, ejemplar, plantas, alto de la malla (H, en el
    mundo), parte visible (vis, 0-1: la torre autoconstruida por corte),
    lenguaje y mutacion. Se guarda (no lo modifiques): solo cambia con la celda."""
    capital = 0
    if cl is not None and W['own'][i] == GEO:
        k_ = cl['de'][i]
        capital = int(k_ >= 0 and cl['capital'][k_] == i and clase_cluster(len(cl['celdas'][k_])) == 2)
    mut = W['mut'][i] if W['mut'][i] >= 0 else mutacion_actual(W, cfg)
    clave = (i, W['occ'][i], W['own'][i], W['par'][i] >= 0, W['vel'][i], W['leng'][i], mut >= 0.25, capital,
             round(W['vig'][i], 2),
             clave_cfg or (tuple(cfg.get(k) for k in _CFG_CIU), id(cfg.get('catalogo')), GRID['lo'], GRID['hi']))
    v = _INFO_CIU.get(clave)
    if v is None:
        if len(_INFO_CIU) > 4000:
            _INFO_CIU.clear()
        v = _INFO_CIU[clave] = _info_ciudad(W, cfg, i, cl if capital else None)
    if v['mut'] != mut:
        v = dict(v, mut=mut)
    return v


def _info_ciudad(W, cfg, i, cl=None):
    own = W['own'][i]
    esp = especie_de(tema_de(cfg), own)
    o = W['occ'][i]
    e = etapa_ciudad(cfg, esp, o)
    if W['par'][i] >= 0:
        e = min(e, 2)
    tipo = TIPOS[esp][e - 1]
    d, v, g4 = diseno_celda(W, cfg, i, esp, e)
    if cl is not None and esp == 'informal' and e >= 4:     # la capital de un barrio grande
        k_ = cl['de'][i]
        if k_ >= 0 and cl['capital'][k_] == i and clase_cluster(len(cl['celdas'][k_])) == 2:
            d = 'kowloon'
    ex = edificio(cfg, d, v)
    hp = alto_planta(cfg)
    pl = plantas_de(cfg, W, i)
    tope = H_TOPE * limit(cfg)
    if ex['modo'] == 'corte':
        H = min(tope, ex['alto'] * hp)
        vis = max(1.0 / ex['alto'], min(1.0, pl / ex['alto']))
    else:
        H = min(tope, pl * hp)
        vis = 1.0
    giro = float((90 if own == ARQ else 30) * g4)
    leng = W['leng'][i] if W['leng'][i] >= 0 else lenguaje_celda(cfg, i, W)
    mut = W['mut'][i] if W['mut'][i] >= 0 else mutacion_actual(W, cfg)
    ind = esp in ('mina', 'energia')
    return dict(esp=esp, etapa=e, tipo=tipo, diseno=d, var=v, giro=giro, ex=ex, plantas=pl, H=H, vis=vis,
                leng=int(leng) + (PALETA_IND if ind else 0), epoca=int(leng) if ind else -1, mut=mut, hp=hp,
                industria=ind)


def _fila_edi(ctx, p, marco, dims, albedo, rug, luces, leng, tinte=0.0, vis=1.0, fin=1.0, modo=0,
              sombra=0.0):
    """La fila de una instancia de un ejemplar de la ciudad. Con el shader de la
    piel: r el tinte de las ventanas (secuenciador + intensidad), g lo visible
    (x 1000) y lo terminado (fraccion), b el modo de obra (1 esqueleto, 2 bloque
    gris) + sombra; alfa = rugosidad + 2 x ventanas + 10 x lenguaje. Sin el
    shader (fase 11 o Materialrespaldo), el albedo."""
    sx, sy, sz = dims
    if not ctx['doce'] or ctx['respaldo']:
        col = _tint(albedo, 1.0 - 0.45 * sombra)
        if fin < 0.999:
            col = _mix(col, COL_BLOQUE, 0.5)
        f = _fila_m(p, marco, sx, sy * (vis if not ctx['doce'] else 1.0), sz, col)
        if ctx['doce']:
            f.append(1.0)
        return f
    f = _fila_m(p, marco, sx, sy, sz, (tinte, float(int(round(max(0.001, vis) * 1000))) +
                                       max(0.0, min(0.999, fin)), float(modo) + 0.9 * max(0.0, min(1.0, sombra))))
    f.append(rug + 2.0 * luces + 10.0 * leng)
    return f


def _fila_ciu(ctx, p, marco, dims, col):
    f = _fila_m(p, marco, dims[0], dims[1], dims[2], col)
    if ctx['doce']:
        f.append(1.0)
    return f


def _en_edi(p0, ej, x, y, z):
    return _add(_add(_add(p0, ej[0], x), ej[2], z), ej[1], y)


def piel_ciudad(W, cfg, ctx, i, rug, kb, fl, arde, out, now, paso):
    """El edificio de la celda i (la biblioteca de la ciudad), sus remates, su
    obra, los mutantes (colonia y marco), las piezas del cluster y los puentes.
    Devuelve las piezas dibujadas."""
    inf = ctx['info'][i]
    cl, bases = ctx['cl'], ctx['bases']
    ex, esp, H, leng, mut = inf['ex'], inf['esp'], inf['H'], inf['leng'], inf['mut']
    res = ctx['res']
    n = normal_i(i)
    p0 = bases[i]
    cw, cl_ = _cell_sizes(_len(p0), i)
    K = 0.94
    sx, sz = K * cw * kb, K * cl_ * kb
    piezas = 0
    lejos = not ctx['cerca'](i)
    k_ = cl['de'][i]
    capital = k_ >= 0 and cl['capital'][k_] == i
    # el cluster: alturas hacia la capital (barrio) y la inclinacion del bucle
    incl, rumbo = 0.0, 0.0
    if k_ >= 0 and esp == 'informal' and inf['etapa'] >= 5 and not capital:
        H = 0.5 * (H + ctx['info'][cl['capital'][k_]]['H'])
    piezas_cl = ctx['cluster'].get(k_) if k_ >= 0 else None
    if piezas_cl and piezas_cl['clase'] == 1 and i in piezas_cl['par']:
        otra = piezas_cl['par'][1] if i == piezas_cl['par'][0] else piezas_cl['par'][0]
        incl = round(9.0 * mut * piezas_cl['q'], 1)
        rumbo = round(_rumbo(n, _hacia(n, n, normal_i(otra))) - inf['giro'], 0)
    H *= kb
    ej = _marco(i, inf['giro'], incl, rumbo)
    # la obra
    pasos = pasos_obra(esp, inf['tipo'])
    codigo = ESP_COD.get(esp, 2) * 10 + inf['etapa']
    # sin obra en curso para este tipo (un mundo hecho a mano, o el motor recien
    # cargado, antes del primer tick), terminado
    s = W['obra'][i] if cfg.get('obra', 1) and W['edi'][i] == codigo else len(pasos)
    hecho = s >= len(pasos)
    paso_ = None if hecho else pasos[s]
    q = _stop((now - W['t_obra'][i]) / max(1e-6, paso))
    pl = max(1.0, inf['plantas'])
    vis, fin, modo, ver = inf['vis'], 1.0, 0, True
    fin0 = min(1.0, W['plantas_ant'][i] / pl) if W['plantas_ant'][i] > 0 else 0.0
    if paso_ in ('solar', 'excavacion', 'nucleo'):
        ver = False
    elif paso_ == 'estructura':              # industria: sube anillo a anillo (encofrado deslizante)
        vis, fin, modo = 0.15 + 0.85 * q, 0.0, 1
    elif paso_ == 'montaje':                 # industria: la estructura se cierra (el castillete, tramo a tramo)
        if esp == 'mina':
            vis, fin, modo = 0.3 + 0.7 * q, 0.3 + 0.7 * q, 0
        else:
            fin, modo = q, 1
    elif paso_ == 'esqueleto':
        vis, fin, modo = fin0 + (1.0 - fin0) * max(0.15, q), fin0, 1
    elif paso_ == 'fachada':
        meta = max(fin0, (pl - cfg.get('desfase_fachada', 2)) / pl)
        fin, modo = fin0 + (meta - fin0) * q, 1
    elif paso_ == 'bloque':                  # la planta nueva, en bloque gris
        vis_pl = vis * ex['alto'] if ex['modo'] == 'corte' else pl
        fin, modo = max(0.0, (vis_pl - 1.0) / max(1.0, vis_pl)) * vis, 2
    if paso_:
        res['obra'][paso_] = res['obra'].get(paso_, 0) + 1
    # luces: las de la estacion (fase 17), apagadas en obra; el tinte de la nota
    luces = ctx['luces'](i) if hecho or esp == 'informal' else 0
    if i in ctx['apagadas']:                 # industria (fase 13): sin corriente, las naves a oscuras
        luces = 0
    tinte = 0.0
    if cfg.get('tinte_ventanas', 1) and W['lat_s'][i] in (1, 2):
        It = 1.0 - (now - W['t_gate'][i]) / max(1e-6, cfg.get('pasos_tinte', 4) * paso)
        if 0.0 < It <= 1.0:
            tinte = W['lat_s'][i] + 0.99 * It
    if fl > 0 and not tinte:                 # el destello del nacimiento
        tinte = 1.0 + 0.99 * fl
    sombra = 0.0
    hib = W['sp'][i] == HIB
    if hib and W['own'][i] == GEO and W['marco_vis'][i] > 0:
        sombra = 0.55                        # el barrio sigue debajo, en sombra
    if i in arde:
        sombra, luces = max(sombra, 0.8 * arde[i]), 0
    nombre = nombre_edificio(ex['diseno'], ex['var'])
    alb = PALETA_CIUDAD[leng][ex['vols'][-1]['slot'] if ex['informal'] else SLOT_CUERPO]
    ind = inf['industria']
    corta = ind and hib and W['own'][i] == ARQ and W['par_vis'][i] > 0     # la corta se come la planta
    if ver and not corta:
        out.setdefault(geometria_de(nombre), []).append(
            _fila_edi(ctx, p0, ej, (sx, H, sz), alb, rug, luces, leng, tinte, vis, fin, modo, sombra))
        piezas += 1
        res['edificios'] += 1
        res['tipos'].add(nombre)
        if ind:
            res['epocas'][inf['epoca']] += 1
        else:
            res['lenguajes'][leng] += 1
    # los remates
    if ver and not corta:
        piezas += _remates(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, vis, hecho, paso_, q, lejos, out)
    if ind and ver and not corta:            # terminada = humea (y la nota suelta su bocanada)
        piezas += _humo(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, hecho, now, paso, out)
    # la obra: valla, tierra, foso, nucleo, grua o andamio, obreros
    if paso_ and ind:
        piezas += _obra_industria(W, cfg, ctx, i, inf, ej, p0, n, cw, cl_, sx, sz, H, paso_, q, vis, now, paso, out)
    elif paso_ and esp == 'planificada':
        piezas += _obra_planificada(W, cfg, ctx, i, inf, ej, p0, n, cw, cl_, sx, sz, H, paso_, q, s, now, paso,
                                    out)
    elif paso_ == 'bloque' and not lejos:
        _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, H, semilla_caos(i, 13), 3, COL_OBRERO,
                    now, paso, 'obreros', 0.6)
    # los mutantes
    if ind and hib and W['own'][i] == ARQ:
        piezas += _corta(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, rug, luces, now, paso, out)
    elif ind and hib and W['own'][i] == GEO:
        piezas += _integrada(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, rug, now, paso, out)
    elif hib and W['own'][i] == ARQ and ver:
        piezas += _colonia(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, now, paso, out)
    elif hib and W['own'][i] == GEO:
        piezas += _marco_ciudad(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, now, paso, out)
    # las piezas del cluster (en la capital) y los puentes
    if piezas_cl and capital:
        piezas += _piezas_cluster(W, cfg, ctx, i, piezas_cl, out)
    if k_ >= 0 and cl['mascara'][i]:
        piezas += _puentes_ciudad(W, cfg, ctx, i, inf, p0, n, cw, cl_, now, paso, out)
    return piezas


_REMATES = {}


def _remates(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, vis, hecho, paso_, q, lejos, out):
    """Los remates del edificio: la lista en coordenadas del ejemplar (se guarda
    por ejemplar, lenguaje y estado) y luego, a su sitio."""
    ex, leng, hp = inf['ex'], inf['leng'], inf['hp']
    puede_crecer = inf['esp'] == 'informal' and (inf['etapa'] < 6 or vis < 0.999)
    tramo = math.ceil(3.0 * q) / 3.0 if paso_ == 'coronacion' else 1.0
    clave = (id(ex), leng, lejos, hecho, puede_crecer, round(vis, 4), paso_ == 'coronacion', tramo, inf['esp'])
    lista = _REMATES.get(clave)
    if lista is None:
        if len(_REMATES) > 4000:
            _REMATES.clear()
        lista = _REMATES[clave] = _lista_remates(ex, leng, lejos, hecho, puede_crecer, vis, paso_, tramo,
                                                  inf['esp'])
    k = 0
    tope = ctx['tope']
    rec = ctx['recurso'](i) if inf['industria'] else None
    for mo, x, y, z, s_, alto, largo, giro, col in lista:
        if y * H + alto * hp > tope:            # nada pasa de la altura maxima
            alto = max(0.0, (tope - y * H) / hp)
        p = _en_edi(p0, ej, x * sx, y * H, z * sz)
        dims = (s_ * sx, alto * hp, largo * sz)
        g = round(inf['giro'] + giro)
        if mo in ('ciu_polea', 'ciu_balancin', 'ciu_rotopala'):     # al tempo (master_beat, fase 17)
            fase = ctx['bq']
            ang = (round(fase * 4.0) * 22.5) % 360.0 if mo != 'ciu_balancin' else \
                round(18.0 * math.sin(2.0 * math.pi * fase) / 3.0) * 3.0
            mk = _marco(i, g, abs(ang), g if ang >= 0 else g + 180)
        else:
            mk = _marco(i, g)
        if rec is not None and mo in ('ciu_terril', 'ciu_vagoneta'):     # el recurso de la concha de abajo
            col = COL_RECURSO[rec]
        out.setdefault(geometria_de(mo), []).append(_fila_ciu(ctx, p, mk, dims, col))
        k += 1
    return k


def _lista_remates(ex, leng, lejos, hecho, puede_crecer, vis, paso_, tramo, esp):
    out = []
    cima = None
    if ex['modo'] == 'corte':                   # la cima visible de la pila 0
        vs = [v for v in ex['vols'] if v['pila'] == 0 and v['y1'] <= vis + 1e-6]
        cima = max(vs, key=lambda v: v['y1']) if vs else ex['vols'][0]
    for r in ex['rem']:
        if r['vol'] >= 0 and ex['modo'] == 'corte' and ex['vols'][r['vol']]['y1'] > vis + 1e-6:
            continue
        x, y, z = r['x'], r['y'], r['z']
        if r['vol'] == -2:
            x, y, z = cima['x'] + r['x'], cima['y1'], cima['z'] + r['z']
        for tipo in _resolver_remate(r['tipo'], leng):
            if lejos and tipo in REMATES_LOD:
                continue
            if tipo in ('deposito', 'antena', 'mastil') and not hecho and esp == 'informal':
                continue                        # aparecen al revocar
            if tipo == 'polea' and not hecho:
                continue                        # industria: las poleas, al final del montaje
            if tipo == 'varillas' and not puede_crecer:
                continue
            if tipo == 'aguja' and paso_ == 'coronacion':
                alto = r['alto'] * tramo        # la grua la sube por tramos
            elif tipo == 'aguja' and not hecho:
                continue
            else:
                alto = r['alto']
            mo = 'ciu_' + tipo
            if mo not in MODELOS:
                continue
            if r['largo'] is not None:
                s_, largo = r['s'], r['largo']
            elif tipo in ('dosaguas', 'unagua', 'pretil', 'pergola', 'sierra', 'vallacima'):
                s_, largo = r['s'] * 1.1, r['s'] * 1.1
            else:
                s_, largo = r['s'], r['s']
            col = COL_REMATE.get(tipo)
            if tipo in ('dosaguas', 'unagua'):
                col = PALETA_CIUDAD[leng][SLOT_TECHO] if leng != 0 else (0.55, 0.56, 0.56)
            if tipo == 'deposito' and leng == 2:
                col = (0.86, 0.86, 0.84)        # en lo calido, el deposito es blanco
            out.append((mo, x, y, z, s_, alto, largo, r['giro'], col))
    return out


def _obra_planificada(W, cfg, ctx, i, inf, ej, p0, n, cw, cl_, sx, sz, H, paso_, q, s, now, paso, out):
    lim = limit(cfg)
    ex = inf['ex']
    k = 0
    pequeno = inf['plantas'] <= 3
    r = ex['radio']
    if paso_ in ('solar', 'excavacion', 'nucleo', 'esqueleto'):
        out.setdefault(geometria_de('ciu_valla'), []).append(
            _fila_ciu(ctx, p0, _marco(i), (2.1 * r * cw, 0.05 * lim, 2.1 * r * cl_), COL_OBRA['valla']))
        k += 1
    if paso_ == 'solar':
        pt = _en_edi(p0, ej, 0.3 * cw, 0.0, 0.28 * cl_)
        out.setdefault(geometria_de('ciu_tierra'), []).append(
            _fila_ciu(ctx, pt, _marco(i), (0.22 * cw, 0.07 * lim, 0.18 * cl_), COL_REMATE['tierra']))
        k += 1
    if paso_ == 'excavacion':
        out.setdefault(geometria_de('ciu_foso'), []).append(
            _fila_ciu(ctx, _add(p0, n, 0.004), _marco(i), (1.8 * r * cw, 0.02 * lim, 1.8 * r * cl_),
                      COL_OBRA['foso']))
        k += 1
        _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, H, semilla_caos(i, 7), 8, COL_POLVO, now,
                    paso, 'polvo')
        _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, H, semilla_caos(i, 11), 8, COL_OBRERO,
                    now, paso, 'obreros')
    alto_g = 0.0
    if paso_ == 'nucleo':                   # el nucleo sube por delante (encofrado trepante)
        hn = H * (0.3 + 0.4 * q)
        out.setdefault(geometria_de('ciu_nucleo'), []).append(
            _fila_ciu(ctx, p0, ej, (0.16 * sx, hn, 0.16 * sz), COL_REMATE['nucleo']))
        k += 1
        alto_g = hn
    elif paso_ in ('esqueleto', 'fachada', 'coronacion'):
        alto_g = H
    if alto_g > 0:
        if pequeno:                         # hasta 3 plantas: andamio con malla
            out.setdefault(geometria_de('ciu_andamio'), []).append(
                _fila_ciu(ctx, p0, ej, (2.1 * r * sx, alto_g * 1.05, 2.1 * r * sz), COL_OBRA['andamio']))
            k += 1
        elif cfg.get('gruas', 1):
            ctx['gruas'].append((W['t_obra'][i], i, ej, p0, n, cw, cl_, r, alto_g))
    return k


def emitir_gruas(W, cfg, ctx, out, now, paso):
    """Las gruas de las obras (Maxgruas, las mas recientes), con su baliza."""
    pedidas = sorted(ctx['gruas'], key=lambda g: (-g[0], g[1]))
    tope = max(0, int(cfg.get('max_gruas', 6))) if cfg.get('gruas', 1) else 0
    for t0, i, ej, p0, n, cw, cl_, r, alto in pedidas[:tope]:
        pg = _en_edi(p0, ej, 0.78 * r * cw, 0.0, -0.5 * r * cl_)
        hc = min(alto * 1.18 + 0.1 * limit(cfg), H_TOPE * limit(cfg) * 1.25)
        out.setdefault(geometria_de('ciu_grua'), []).append(
            _fila_ciu(ctx, pg, _marco(i, 90.0), (0.5 * cw, hc, 0.5 * cl_), COL_OBRA['grua']))
        if int(now / paso) % 2 == 0:            # la baliza de obra parpadea al paso
            out.setdefault('particulas', []).append(_row(_add(pg, n, hc), n, 0.03 * cw, 0.03 * cw, 0.03 * cw,
                                                         COL_BALIZA))
    ctx['res']['gruas'] = min(len(pedidas), tope)
    return min(len(pedidas), tope)


def _colonia(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, now, paso, out):
    """COLONIA: la informal coloniza la planificada. Los parasitos (cuartos y
    casetas de la biblioteca informal) llegan uno por paso: la azotea, luego la
    fachada hacia abajo, en voladizo hasta 0,8 vanos; con escaleras y cables."""
    nv = W['par_vis'][i]
    if nv <= 0:
        return 0
    ex, leng, hp = inf['ex'], inf['leng'], inf['hp']
    pts = puestos_colonia(ex, nv, inf['mut'], semilla_caos(W['vel'][i], i + 777), inf['plantas'])
    xs = logistica(semilla_caos(W['vel'][i], i + 555), 3.91, 2 * len(pts) + 2)
    vano = cfg.get('ancho_vano', 0.05) * limit(cfg)
    k = 0
    u = (now - W['t_vis'][i]) / max(1e-6, paso)
    bote = rebote(cfg, dict(t_nac={i: W['t_vis'][i]}), i, now, paso)[0] if 0 <= u < 1 else 1.0
    for q, (x, y, z, nx, nz, nivel) in enumerate(pts):
        lado = (0.11 if nivel == 0 else 0.075) * (0.85 + 0.3 * xs[2 * q])
        d = 'chabola' if nivel == 0 and xs[2 * q + 1] < 0.4 else 'cuarto'
        v = min(variantes_ciudad(cfg) - 1, int(xs[2 * q + 1] * variantes_ciudad(cfg)))
        vuela = max(abs(nx), abs(nz))           # 0,5 pegado; 1,3 = 0,8 vanos fuera; +1,1 colgado
        fuera = vano * max(0.0, vuela - 0.5)
        sgx = (1.0 if nx > 0 else -1.0) if nx else 0.0
        sgz = (1.0 if nz > 0 else -1.0) if nz else 0.0
        p = _en_edi(p0, ej, x * sx + sgx * (0.5 * lado * sx + fuera), y * H - (hp if nivel else 0.0),
                   z * sz + sgz * (0.5 * lado * sz + fuera))
        g = round(inf['giro'] + (30.0 if xs[2 * q] > 0.5 else -30.0) * (nivel == 0)
                  + (xs[2 * q] - 0.5) * 2.0 * cfg.get('oblicuidad', 6.0))
        e = bote if q == len(pts) - 1 else 1.0
        dims = (lado * sx * e, hp * e, lado * sz * e) if d == 'cuarto' else (2.2 * lado * sx * e, hp * e,
                                                                          2.2 * lado * sz * e)
        out.setdefault(geometria_de(nombre_edificio(d, v)), []).append(
            _fila_edi(ctx, p, _marco(i, g), dims, PALETA_CIUDAD[leng][q % 4], 0.85, ctx['luces'](i), leng))
        k += 1
        if nivel == 1 and q % 4 == 1 and not ctx['lejos'](i):      # escaleras y cables que bajan
            out.setdefault(geometria_de('ciu_escalera'), []).append(
                _fila_ciu(ctx, _en_edi(p0, ej, x * sx, max(0.0, y * H - 2.2 * hp), z * sz), _marco(i, g),
                          (0.03 * sx, 2.2 * hp, 0.03 * sz), COL_REMATE['escalera']))
            k += 1
    ctx['res']['colonias'][i] = (nv, int(cfg['max_parasitos']))
    return k


def _marco_ciudad(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, now, paso, out):
    """CIUDAD ESPACIAL: la planificada sobrevuela la informal con un marco de
    pilares en los callejones (nunca sobre una casa), un nivel por nota hasta
    Maxmarco, y capsulas enchufadas en una fraccion Capsulas de los huecos."""
    u = W['marco_vis'][i]
    if u <= 0:
        return 0
    niveles = (u + 1) // 2
    caps_arriba = u % 2 == 0
    ex = inf['ex']
    m = max(0.1, min(0.5, float(cfg.get('modulo_marco', 0.25))))
    libres, g, paso_m = pilares_marco(ex, m)
    mh = paso_m * min(cw, cl_) * 0.75
    hb = H + 0.35 * inf['hp']
    k = 0
    xs = logistica(semilla_caos(W['vel'][i], i + 999), 3.91, g * g * niveles + len(libres) + 4)
    # pilares: los nudos libres, repartidos (las esquinas siempre lo estan)
    alto_total = hb + niveles * mh
    pil = [p for q, p in enumerate(libres) if xs[q] < 0.5 or abs(p[0]) > 0.49 and abs(p[1]) > 0.49]
    for x, z in pil:
        out.setdefault(geometria_de('ciu_pilar'), []).append(
            _fila_ciu(ctx, _en_edi(p0, ej, x * cw, 0.0, z * cl_), ej, (0.03 * cw, alto_total, 0.03 * cl_),
                      COL_REMATE['pilar']))
        k += 1
    caps = 0
    mut = inf['mut']
    for lv in range(niveles):
        y = hb + lv * mh
        for a in range(g):
            for b in range(g):
                x, z = -0.5 + (a + 0.5) * paso_m, -0.5 + (b + 0.5) * paso_m
                out.setdefault(geometria_de('ciu_marco'), []).append(
                    _fila_ciu(ctx, _en_edi(p0, ej, x * cw, y, z * cl_), ej, (paso_m * cw, mh, paso_m * cl_),
                              COL_REMATE['marco']))
                k += 1
                tiene = xs[len(libres) + lv * g * g + a * g + b] < cfg.get('capsulas', 0.4)
                if tiene and (lv < niveles - 1 or caps_arriba):
                    borde = a in (0, g - 1) or b in (0, g - 1)
                    fuera = 0.62 * paso_m if borde and mut > 0.5 else 0.0     # capsulas en voladizo
                    ox = (-1 if a == 0 else 1 if a == g - 1 else 0) * fuera
                    oz = (-1 if b == 0 else 1 if b == g - 1 else 0) * fuera
                    c = 0.62 * paso_m
                    out.setdefault(geometria_de(nombre_edificio('capsula', (a + b + lv) % variantes_ciudad(cfg))),
                                   []).append(
                        _fila_edi(ctx, _en_edi(p0, ej, (x + ox) * cw, y + 0.18 * mh, (z + oz) * cl_), ej,
                                  (c * cw, 0.62 * mh, c * cl_), PALETA_CIUDAD[2][SLOT_CUERPO], 0.3,
                                  ctx['luces'](i), inf['leng']))
                    caps += 1
                    k += 1
    kc = ctx['cl']['de'][i]
    r = ctx['res']['marcos'].setdefault(kc if kc >= 0 else 'c%d' % i, [0, int(cfg['max_marco']), 0])
    r[0] = max(r[0], niveles)
    r[2] += caps
    return k


def piezas_de_cluster(W, cfg, ctx, tf):
    """{cluster: pieza} de los clusters planificados terminados (su obra de
    fusion, hecha): pasarela celeste (2-3 celdas), bucle (4-6: la capital y su
    vecina mas alta se inclinan una hacia otra) o losa en la cumbre (7+). Con
    Mutacion 0, solo pasarela."""
    cl = ctx['cl']
    out = {}
    for k_, cs in cl['celdas'].items():
        cap = cl['capital'][k_]
        esp = ctx['info'][cap]['esp'] if cap in ctx['info'] else ''
        if not cs or esp not in ('planificada', 'energia'):
            continue
        cf, _ = cadenas_de(cfg, tema_de(cfg), esp)
        if W['et_f'][cap] < tf[cap] or not cf:
            continue
        mut = ctx['info'][cap]['mut']
        clase = clase_cluster(len(cs)) if mut > 0.05 else 0
        if esp == 'energia':            # fase 11 v11: torres que se alinean
            out[k_] = dict(clase=clase, nombre=['torre compartida', 'fila de torres', 'anillo de torres'][clase],
                           par=(), q=1.0, celdas=list(cs), industria=True)
            continue
        par = None
        if clase == 1:
            vec = [j for j in cl['mascara'][cap] if j in ctx['info']] or \
                [j for j in cs if j != cap and j in ctx['info']]
            j = max(vec, key=lambda x: (ctx['info'][x]['H'], -x)) if vec else None
            par = (cap, j) if j is not None else None
            if par is None:
                clase = 0
        out[k_] = dict(clase=clase, nombre=['pasarela', 'bucle', 'losa'][clase], par=par or (), q=1.0,
                       celdas=list(cs))
    return out


def _piezas_cluster(W, cfg, ctx, i, pc, out):
    if pc.get('industria'):
        return _torres_cluster(W, cfg, ctx, i, pc, out)
    info, bases, cl = ctx['info'], ctx['bases'], ctx['cl']
    lim = limit(cfg)
    n = normal_i(i)
    k = 0
    ctx['res']['protagonistas'][pc['nombre']] = ctx['res']['protagonistas'].get(pc['nombre'], 0) + 1
    if pc['clase'] == 0:                    # pasarelas celestes hacia las vecinas
        for j in cl['mascara'][i]:
            if j not in info:
                continue
            y = 0.62 * min(info[i]['H'], info[j]['H'])
            pj = bases[j]
            dist = _len(_add(pj, bases[i], -1.0))
            ej = _marco_puente(i, j)
            mid = _add(_mul(_norm(_add(bases[i], pj)), 0.5 * (_len(bases[i]) + _len(pj))), n, y)
            out.setdefault(geometria_de('ciu_pasarela'), []).append(
                _fila_ciu(ctx, mid, ej, (0.06 * min(_cell_sizes(_len(bases[i]), i)), 0.03 * lim, 0.8 * dist),
                          COL_REMATE['pasarela']))
            k += 1
    elif pc['clase'] == 1:                  # bucle: un puente une las dos cimas inclinadas
        a, b = pc['par']
        y = 0.9 * min(info[a]['H'], info[b]['H'])
        dist = _len(_add(bases[b], bases[a], -1.0))
        ej = _marco_puente(a, b)
        mid = _add(_mul(_norm(_add(bases[a], bases[b])), 0.5 * (_len(bases[a]) + _len(bases[b]))), n, y)
        out.setdefault(geometria_de('ciu_bucle'), []).append(
            _fila_ciu(ctx, mid, ej, (0.28 * min(_cell_sizes(_len(bases[a]), a)), 0.12 * y, 0.85 * dist),
                      COL_REMATE['bucle']))
        k += 1
    else:                                   # losa en la cumbre que corona todas las torres
        cs = pc['celdas']
        cen = _norm(tuple(sum(bases[c][q] for c in cs) for q in range(3)))
        r0 = sum(_len(bases[c]) for c in cs) / len(cs)
        lejos_ = max(cs, key=lambda c: _len(_add(_mul(cen, r0), bases[c], -1.0)))
        rmax = _len(_add(_mul(cen, r0), bases[lejos_], -1.0))
        y = min([info[c]['H'] for c in cs if c in info] or [info[i]['H']])
        nc = cen
        d = _hacia(nc, _mul(nc, r0), bases[lejos_])
        ejl = (_cross(nc, d), nc, d, _euler_xyz(_cross(nc, d), nc, d))
        cw = min(_cell_sizes(r0, i))
        out.setdefault(geometria_de('ciu_losa'), []).append(
            _fila_ciu(ctx, _mul(nc, r0 + y), ejl, (0.45 * cw, 0.05 * lim, 2.0 * rmax + 0.4 * cw),
                      COL_REMATE['losa']))
        k += 1
    return k


def _puentes_ciudad(W, cfg, ctx, i, inf, p0, n, cw, cl_, now, paso, out):
    """Un puente hacia cada vecina del cluster (la mascara): en la informal,
    pasarelas entre azoteas (corredores cubiertos en el barrio); en la
    planificada, el zocalo comercial que une las torres. Crecen con la cadena
    de fusion (soldadura y relleno; o el andamio, planta a planta)."""
    cf = ctx['cadenas'][inf['esp']]
    kp = 0.0
    for nombre, valor in (('soldadura', 0.35), ('relleno', 1.0), ('puentes', 1.0), ('andamio', 1.0)):
        if nombre in cf:
            kp = max(kp, valor * avance_etapa(W, i, 'et_f', cf.index(nombre) + 1, now, paso,
                                              ANDAMIO_PASOS if nombre == 'andamio' else 1.0))
    if kp <= 0:
        return 0
    info, bases = ctx['info'], ctx['bases']
    pm = (modelos_de(cfg, tema_de(cfg), inf['esp'], 'puente') or ['ciu_pasarela'])[0]
    k = 0
    for q, j in enumerate(ctx['cl']['mascara'][i]):
        Hj = info[j]['H'] if j in info else inf['H']
        pj = bases[j]
        largo = 0.5 * math.sqrt((p0[0] - pj[0]) ** 2 + (p0[1] - pj[1]) ** 2 + (p0[2] - pj[2]) ** 2) + 0.06
        ej = _marco_puente(i, j)
        if inf['esp'] == 'mina':            # la cuenca: los terriles se funden en una sierra negra
            centro = _add(p0, ej[2], 0.5 * largo)
            out.setdefault(geometria_de(pm if pm in MODELOS else 'ciu_terril'), []).append(
                _fila_ciu(ctx, centro, ej, (0.2 * min(cw, cl_), 0.09 * limit(cfg) * max(0.35, kp), largo),
                          COL_RECURSO[ctx['recurso'](i)]))
            if kp >= 1 and i < j and inf['etapa'] in (2, 3) and j in info and info[j]['etapa'] in (2, 3):
                # y un cable aereo de baldes une los castilletes (uno por par; los hay en la mina y el complejo)
                y = 0.8 * min(inf['H'], Hj)
                out.setdefault(geometria_de('ciu_cable'), []).append(
                    _fila_ciu(ctx, _add(_add(p0, n, y), ej[2], largo), ej, (0.01 * cw, 0.01 * cw, 2.0 * largo),
                              COL_REMATE['cable']))
        elif inf['esp'] == 'energia':       # tuberias entre las plantas
            y = 0.25 * min(inf['H'], Hj)
            out.setdefault(geometria_de(pm if pm in MODELOS else 'ciu_tuberia'), []).append(
                _fila_ciu(ctx, _add(_add(p0, n, y), ej[2], 0.5 * largo), ej,
                          (0.04 * min(cw, cl_) * (0.35 if kp < 1 else 1.0), 0.04 * min(cw, cl_), largo),
                          PALETA_CIUDAD[inf['leng']][7]))
        elif inf['esp'] == 'planificada':     # el zocalo comercial (z de 0 a 1)
            alto = max(0.01, 2.0 * inf['hp'] * kp * (1.0 + 0.04 * (q % 3)))
            mo = pm if es_edificio(pm) else nombre_edificio('zocalo', 0)
            out.setdefault(geometria_de(mo), []).append(
                _fila_edi(ctx, p0, ej, (0.62 * min(cw, cl_), alto, largo),
                          PALETA_CIUDAD[inf['leng']][SLOT_PIEDRA], 0.6, ctx['luces'](i), inf['leng']))
        else:
            tipo = 'corredor' if inf['etapa'] >= 5 else 'pasarela'
            y = 0.6 * min(inf['H'], Hj) * (1.0 + 0.04 * (q % 3))
            centro = _add(_add(p0, n, y), ej[2], 0.5 * largo)
            ancho = (0.12 if tipo == 'corredor' else 0.05) * min(cw, cl_) * (0.35 if kp < 1 else 1.0)
            out.setdefault(geometria_de('ciu_' + tipo), []).append(
                _fila_ciu(ctx, centro, ej, (ancho, (0.6 if tipo == 'corredor' else 0.15) * inf['hp'], largo),
                          COL_REMATE[tipo]))
        k += 1
    return k



# --- dibujar la industria (fase 11 v11) ------------------------------------------------

COL_AGUA_ACIDA = (0.55, 0.20, 0.12)      # el fondo inundado de la corta: rojizo, nunca azul
COL_BANCO = ((0.50, 0.30, 0.18), (0.42, 0.25, 0.16), (0.58, 0.36, 0.22))
COL_TESTIGO = (0.58, 0.27, 0.19)


def color_humo(ctx, inf, i, tipo):
    """Humo negro (carbon y vapor), gris (acero) o vapor blanco (torres y quimica)."""
    if tipo == 'penacho':
        return COL_HUMO['blanco']
    if ctx['carbon'](i) or inf['epoca'] == 0:
        return COL_HUMO['negro']
    return COL_HUMO['gris'] if inf['epoca'] == 1 else COL_HUMO['blanco']


def _humo(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, hecho, now, paso, out):
    """El humo, el vapor y la llama de la planta terminada: bocanadas al pulso,
    cantidad por la ocupacion y Emisiones (y el ruido del modular), sin pasar de
    Maxhumo. Una nota tine la bocanada de su chimenea del color de su secuenciador;
    con STOP (huelga) el humo se queda quieto.
    Motor v74: las bocanadas son filas fijas de la geometria 'humo' (una por
    bocanada: su fuente, tamano, altura y desfase) que anima la GPU (mat_humo: sube,
    se hincha, deriva y se desvanece con el reloj humo_t de frame_u, a saltos de
    stop-motion). No dependen del pulso, asi que se guardan y no se recalculan en
    cada foto. Las balizas y la llama siguen en 'particulas'."""
    if not hecho:
        return 0
    hum = out.setdefault('humo', [])
    tope = int(cfg.get('max_humo', 6000))
    tin_q = 0
    if W['lat_s'][i] in (1, 2):
        It = 1.0 - (now - W['t_gate'][i]) / max(1e-6, cfg.get('pasos_tinte', 4) * paso)
        if 0.0 < It <= 1.0:
            tin_q = W['lat_s'][i] * 100 + int(It * 20)
    clave = (i, round(H, 4), round(sx, 4), round(sz, 4), id(inf['ex']), inf['epoca'], inf['etapa'],
             tin_q, round(ctx['ruido'], 2), ctx['carbon'](i), cfg.get('emisiones'), p0)
    filas = _HUMO.get(clave)
    if filas is None:
        if len(_HUMO) > 3000:
            _HUMO.clear()
        filas = _HUMO[clave] = []
        _humo_filas(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, now, paso, filas)
    libres = max(0, tope - ctx['humo'][0])
    usar = filas if len(filas) <= libres else filas[:libres]
    hum.extend(usar)
    ctx['humo'][0] += len(usar)
    return len(usar) + _luces_humo(cfg, ctx, inf, ej, p0, sx, sz, H, out.setdefault('particulas', []))


_HUMO = {}

HUMO_PENACHO = 2.0      # en el canal a de una bocanada: desfase (0-1) + 2 si es vapor que respira con el LFO


def fila_humo(p, s, H, m_, col, desfase, penacho=False):
    """Una bocanada de la geometria 'humo' (motor v74): la fuente p, el tamano de
    partida s, la altura que sube H (hasta 0,55 x H), la deriva m_ (en sx, sy y sz:
    el shader los lee como la longitud de cada eje), el color y en a el desfase
    (0-1), mas HUMO_PENACHO si el vapor respira con el LFO."""
    return [p[0], p[1], p[2], 0.0, 0.0, 0.0, max(1e-4, s), max(1e-4, H), max(1e-4, m_),
            col[0], col[1], col[2], (desfase % 1.0) + (HUMO_PENACHO if penacho else 0.0)]


def humo_reloj(frame=None):
    """(tiempo, lfo) de mat_humo: el pulso en beats a saltos de stop-motion
    (FOTOS_PASO por paso; STOP lo congela; 0 antes de la fase 17) y el LFO del
    modular (0,5 sin senal o antes de la fase 19)."""
    try:
        W, c = world(), cfg_foto()
        t = beat_stop(W, c) if c['nivel'] >= 17 else 0.0
        lfo = float(W['modular'].get('lfo', 0.5)) if c['nivel'] >= 19 else 0.5
        return t, lfo
    except Exception:
        return 0.0, 0.5


def _humo_filas(W, cfg, ctx, i, inf, ej, p0, sx, sz, H, now, paso, filas):
    """Las bocanadas de la planta (filas de 'humo')."""
    k = 0
    cant = cfg.get('emisiones', 0.5) * (1.0 + ctx['ruido'])
    tin = None
    if W['lat_s'][i] in (1, 2):
        It = 1.0 - (now - W['t_gate'][i]) / max(1e-6, cfg.get('pasos_tinte', 4) * paso)
        if 0.0 < It <= 1.0:
            tin = (seq_color(cfg, W['lat_s'][i]), It)
    for r in inf['ex']['fuentes']:
        if r['tipo'] in ('baliza', 'llama'):
            continue
        p = _en_edi(p0, ej, r['x'] * sx, r['y'] * H, r['z'] * sz)
        m_ = min(sx, sz)
        col = color_humo(ctx, inf, i, r['tipo'])
        q_n = max(1, min(6, int(round(cant * (1 + inf['etapa']) * 0.8))))     # pocas bocanadas, grandes
        pen = r['tipo'] == 'penacho'            # el vapor de las torres respira con el LFO
        if pen:
            q_n = max(3, q_n)
        ct = _mix(col, tin[0], 0.85 * tin[1]) if tin is not None else col
        for q in range(q_n):
            filas.append(fila_humo(p, r['s'] * m_, H, m_, ct, q / float(q_n), pen))
            k += 1
    return k


def _luces_humo(cfg, ctx, inf, ej, p0, sx, sz, H, parts):
    """Las balizas de las chimeneas altas (parpadean) y la antorcha (crece con la
    saturacion), en 'particulas', con el pulso a saltos."""
    kq = max(1, int(cfg.get('steps_per_beat', 4))) * FOTOS_PASO
    tau = math.floor(ctx['bq'] * kq) / kq
    n = None
    k = 0
    for r in inf['ex']['fuentes']:
        if r['tipo'] not in ('baliza', 'llama'):
            continue
        p = _en_edi(p0, ej, r['x'] * sx, r['y'] * H, r['z'] * sz)
        n = n or _norm(p0)
        m_ = min(sx, sz)
        if r['tipo'] == 'baliza':
            if int(tau * 2.0) % 2 == 0:
                parts.append(_row(p, n, 0.02 * m_, 0.02 * m_, 0.02 * m_, COL_BALIZA))
                k += 1
            continue
        g = 0.05 * m_ * (1.0 + 0.6 * ctx['saturacion'])
        parts.append(_row(p, n, g, 2.2 * g * (0.8 + 0.4 * abs(math.sin(7.0 * tau))), g, COL_LLAMA))
        k += 1
    return k


def _obra_industria(W, cfg, ctx, i, inf, ej, p0, n, cw, cl_, sx, sz, H, paso_, q, vis, now, paso, out):
    """La obra de la industria: valla, foso, el encofrado que sube con la chimenea
    o la torre, la columna tumbada que iza la grua y la grua."""
    lim = limit(cfg)
    ex = inf['ex']
    r = ex['radio']
    k = 0
    if paso_ in ('solar', 'excavacion', 'estructura'):
        out.setdefault(geometria_de('ciu_valla'), []).append(
            _fila_ciu(ctx, p0, _marco(i), (2.1 * r * cw, 0.05 * lim, 2.1 * r * cl_), COL_OBRA['valla']))
        k += 1
    if paso_ == 'solar' and inf['tipo'] == 'refineria':     # la columna llega tumbada
        out.setdefault(geometria_de('ciu_columna'), []).append(
            _fila_ciu(ctx, _en_edi(p0, ej, 0.0, 0.0, 0.2 * cl_), _marco(i, round(inf['giro'])),
                      (0.6 * H, 0.06 * cw, 0.06 * cw), PALETA_CIUDAD[inf['leng']][3]))
        k += 1
    if paso_ == 'excavacion':
        out.setdefault(geometria_de('ciu_foso'), []).append(
            _fila_ciu(ctx, _add(p0, n, 0.004), _marco(i), (1.8 * r * cw, 0.02 * lim, 1.8 * r * cl_),
                      COL_OBRA['foso']))
        k += 1
        _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, H, semilla_caos(i, 7), 6, COL_POLVO, now,
                    paso, 'polvo')
    if paso_ == 'estructura':                   # el encofrado deslizante o trepante, arriba
        altos = [v for v in ex['vols'] if v['rol'] in ('chimenea', 'torre')]
        if altos:
            v = max(altos, key=lambda x: x['y1'])
            y = min(vis, v['y1']) * H
            tp = 1.0 - (1.0 - v.get('top', 1.0)) * min(1.0, max(0.0, (min(vis, v['y1']) - v['y0']) /
                                                                 max(1e-6, v['y1'] - v['y0'])))
            out.setdefault(geometria_de('ciu_encofrado'), []).append(
                _fila_ciu(ctx, _en_edi(p0, ej, v['x'] * sx, y, v['z'] * sz), ej,
                          (v['w'] * sx * tp * 1.25, 0.04 * lim, v['d'] * sz * tp * 1.25), COL_OBRA['grua']))
            k += 1
    if paso_ in ('solar', 'estructura') or (paso_ == 'montaje' and inf['esp'] == 'energia'):
        alto = H * (vis if paso_ == 'estructura' else 1.0) if paso_ != 'solar' else 0.6 * H
        if cfg.get('gruas', 1) and inf['etapa'] >= 2:
            ctx['gruas'].append((W['t_obra'][i], i, ej, p0, n, cw, cl_, r, alto))
    return k


def _corta(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, rug, luces, now, paso, out):
    """CORTA QUE DEVORA: la mina se come la planta. Un banco por nota del SEQ1
    (Bancospornota, hasta Maxbancos), dentro de su anillo de escombreras: los
    bancos suben hacia la cresta y el fondo queda a ras de suelo (no corta
    conchas: eso solo lo hace la caja). Primero se van las naves, luego la sala
    de calderas; queda la chimenea, sola, de testigo. Desde 4 bancos el fondo se
    inunda de agua acida rojiza y una rotopala trabaja el banco mas alto."""
    b = W['par_vis'][i]
    if b <= 0:
        return 0
    lim = limit(cfg)
    mx = max(1, int(cfg['max_bancos']))
    R0 = 0.47
    dr = R0 / (mx + 2.0)
    hc = 0.12 * lim * (1.0 + 0.12 * b)
    k = 0
    for q in range(b):                          # de la cresta (fuera, alto) hacia el fondo
        r_ = R0 - q * dr
        h = hc * (b - q) / float(b)
        out.setdefault(geometria_de('ciu_anillo'), []).append(
            _fila_ciu(ctx, p0, _marco(i, 22.5 * (q % 2)), (2 * r_ * cw, h, 2 * r_ * cl_), COL_BANCO[q % 3]))
        k += 1
    rf = R0 - b * dr                            # el fondo, a ras de suelo
    v = inf['var'] % max(1, variantes_ind(cfg))
    leng = inf['leng']
    if b <= 2:                                  # quedan la sala de calderas y la chimenea
        lado = min(0.9, 1.6 * rf)
        out.setdefault(geometria_de(nombre_edificio('calderas', v)), []).append(
            _fila_edi(ctx, _en_edi(p0, ej, -0.25 * rf * cw, 0.0, 0.0), ej, (lado * cw * 0.6, 4.0 * inf['hp'],
                                                                           lado * cl_ * 0.6),
                      PALETA_CIUDAD[leng][5], rug, luces, leng))
        k += 1
    out.setdefault(geometria_de(nombre_edificio('chimenea', v)), []).append(
        _fila_edi(ctx, _en_edi(p0, ej, 0.2 * rf * cw, 0.0, 0.0), ej, (0.25 * cw, 0.85 * H, 0.25 * cl_),
                  COL_TESTIGO, rug, 0, leng))
    k += 1
    if b >= 4:                                  # agua acida (Rio Tinto) y la rotopala en el banco alto
        out.setdefault(geometria_de('ciu_agua'), []).append(
            _fila_ciu(ctx, _add(p0, normal_i(i), 0.003), _marco(i), (2 * rf * cw * 1.05, 0.01 * lim, 2 * rf * cl_ * 1.05),
                      COL_AGUA_ACIDA))
        g = round(inf['giro'])
        fase = ctx['bq']
        out.setdefault(geometria_de('ciu_rotopala'), []).append(
            _fila_ciu(ctx, _en_edi(p0, ej, (R0 - 0.5 * dr) * cw, hc, 0.0),
                      _marco(i, g, (round(fase * 4.0) * 22.5) % 360.0, g),
                      (0.14 * cw, 0.12 * lim, 0.07 * cl_), (0.85, 0.66, 0.18)))
        k += 2
    ctx['res']['cortas'][i] = (b, mx, b >= 3)
    return k


def _integrada(W, cfg, ctx, i, inf, ej, p0, cw, cl_, sx, sz, H, rug, now, paso, out):
    """PLANTA INTEGRADA: la energia se monta encima de la mina (Zollverein). Un
    nivel de bastidor de tuberias y unidades de proceso por nota del SEQ2 (hasta
    Maxbastidor), que los castilletes atraviesan; las tuberias bajan a los pozos
    y desde el segundo nivel una chimenea corona el conjunto."""
    u = W['marco_vis'][i]
    if u <= 0:
        return 0
    niveles = (u + 1) // 2
    ex = inf['ex']
    m = max(0.1, min(0.5, float(cfg.get('modulo_marco', 0.25))))
    libres, g, paso_m = pilares_marco(ex, m)
    mh = paso_m * min(cw, cl_) * 0.5
    hb = 0.5 * H                                # a media altura: los castilletes lo atraviesan
    k = 0
    xs = logistica(semilla_caos(W['vel'][i], i + 888), 3.91, len(libres) + 4)
    for q, (x, z) in enumerate(libres):
        if xs[q] < 0.35 or (abs(x) > 0.49 and abs(z) > 0.49):
            out.setdefault(geometria_de('ciu_pilar'), []).append(
                _fila_ciu(ctx, _en_edi(p0, ej, x * cw, 0.0, z * cl_), ej, (0.025 * cw, hb + niveles * mh, 0.025 * cl_),
                          PALETA_CIUDAD[inf['leng']][1]))
            k += 1
    tub = PALETA_CIUDAD[inf['leng']][7]
    for lv in range(niveles):
        y = hb + lv * mh
        for a in range(g):
            for b_ in range(g):
                x, z = -0.5 + (a + 0.5) * paso_m, -0.5 + (b_ + 0.5) * paso_m
                out.setdefault(geometria_de('ciu_bastidor'), []).append(
                    _fila_ciu(ctx, _en_edi(p0, ej, x * cw, y, z * cl_), _marco(i, round(inf['giro']) // 90 * 90),
                              (paso_m * cw, mh, paso_m * cl_), tub if (a + b_ + lv) % 2 else PALETA_CIUDAD[inf['leng']][1]))
                k += 1
    for x, z in ((-0.25, -0.25), (0.25, 0.25)):     # las tuberias bajan a los pozos
        out.setdefault(geometria_de('ciu_tuberia'), []).append(
            _fila_ciu(ctx, _en_edi(p0, ej, x * cw, 0.0, z * cl_), ej, (0.03 * cw, hb, 0.03 * cl_), tub))
        k += 1
    if niveles >= 2:                            # la chimenea corona el conjunto
        v = inf['var'] % max(1, variantes_ind(cfg))
        out.setdefault(geometria_de(nombre_edificio('chimenea', v)), []).append(
            _fila_edi(ctx, _en_edi(p0, ej, 0.0, hb + niveles * mh, 0.0), ej, (0.2 * cw, 0.5 * H, 0.2 * cl_),
                      PALETA_CIUDAD[inf['leng']][6], rug, 0, inf['leng']))
        k += 1
    kc = ctx['cl']['de'][i]
    r = ctx['res']['integradas'].setdefault(kc if kc >= 0 else 'c%d' % i, [0, int(cfg['max_bastidor'])])
    r[0] = max(r[0], niveles)
    return k


def _torres_cluster(W, cfg, ctx, i, pc, out):
    """Energia: torres que se alinean. 2-3 celdas, una torre de refrigeracion
    compartida; 4-6, una fila; 7 o mas, un anillo alrededor de la chimenea mas alta."""
    info, bases, cl = ctx['info'], ctx['bases'], ctx['cl']
    n = normal_i(i)
    cw, cl_ = _cell_sizes(_len(bases[i]), i)
    hp = info[i]['hp']
    Ht = min(H_TOPE * limit(cfg), 6.5 * hp)
    sitios = []
    if pc['clase'] == 0:
        vec = [j for j in cl['mascara'][i] if j in info]
        if vec:
            j = vec[0]
            sitios.append(_mul(_norm(_add(bases[i], bases[j])), 0.5 * (_len(bases[i]) + _len(bases[j]))))
    elif pc['clase'] == 1:
        lejos_ = max(pc['celdas'], key=lambda c: (_len(_add(bases[c], bases[i], -1.0)), -c))
        for t in (0.3, 0.55, 0.8):
            pm = _add(_mul(bases[i], 1.0 - t), bases[lejos_], t)
            sitios.append(_mul(_norm(pm), _len(bases[i])))
    else:
        e_, t_ = tangents(n)
        for q in range(6):
            a = 2.0 * math.pi * q / 6.0
            pm = _add(_add(bases[i], e_, 0.8 * cw * math.cos(a)), t_, 0.8 * cl_ * math.sin(a))
            sitios.append(_mul(_norm(pm), _len(bases[i])))
    k = 0
    v = info[i]['var'] % max(1, variantes_ind(cfg))
    for p in sitios:
        nn = _norm(p)
        ejt = _ejes(nn)
        mk = ejt + (_euler_xyz(*ejt),)
        out.setdefault(geometria_de(nombre_edificio('torreref', v)), []).append(
            _fila_edi(ctx, p, mk, (0.42 * cw, Ht, 0.42 * cl_), PALETA_CIUDAD[info[i]['leng']][3], 0.6,
                      ctx['luces'](i), info[i]['leng']))
        k += 1
        if ctx['humo'][0] < int(cfg.get('max_humo', 6000)):     # su penacho (motor v74: en la GPU)
            for q in range(3):
                out.setdefault('humo', []).append(fila_humo(_add(p, nn, 0.95 * Ht), 0.12 * cw, Ht, 0.3 * cw,
                                                            COL_HUMO['blanco'], q / 3.0, True))
                ctx['humo'][0] += 1
    ctx['res']['protagonistas'][pc['nombre']] = ctx['res']['protagonistas'].get(pc['nombre'], 0) + 1
    return k


# --- autopruebas de la piel por turnos (fase 11 v18) ----------------------------------

PRUEBA_NOTAS = (60, 64, 67, 72, 67, 64, 62, 60, 55, 60, 64, 67, 69, 67, 64, 62)
PRUEBA_NOTAS2 = (36, 43, 41, 39, 46)


def _mundo_prueba_piel(cfg, segundos=20.0, eras=0, fps=30.0, tempo=120.0):
    """Un mundo para las autopruebas: el SEQ1 en semicorcheas y el SEQ2 cada 3
    pasos durante segundos, eras veces enterrado (fin de ciclo) y otra mas.
    Devuelve (W, el ultimo instante)."""
    W = new_world()
    ensure(W)
    W['tema'] = cfg.get('tema', 0)
    paso = step_dur(cfg, tempo)
    k, t, pend = -1, 0.0, []
    for e in range(eras + 1):
        for _ in range(int(segundos * fps)):
            t += 1.0 / fps
            p = int(t / paso)
            if p != k:
                k = p
                for s, n in pend:
                    note_off(W, cfg, s, n, t, tempo)
                pend = [(GEO, PRUEBA_NOTAS[p % 16])]
                if p % 3 == 0:
                    pend.append((ARQ, PRUEBA_NOTAS2[(p // 3) % 5]))
                for s, n in pend:
                    note_on(W, cfg, s, n, 100, t, tempo)
            tick(W, cfg, t, tempo, True)
        if e < eras:
            end_cycle(W, cfg, t)
    W['foto_dt'] = 1.0 / fps
    return W, t


def _piel_foto(W, cfg, now):
    """Un fotograma de la piel por turnos: (filas, informe del turno)."""
    _TERRENO['sello'] = _TERRENO.get('sello', 0) + 1
    out = {}
    build_piel_refresco(W, cfg, now, out)
    return out, dict(_TURNOS.get('info') or {})


def _mods(out):
    return dict((g, f) for g, f in out.items() if g.startswith('mod_'))


def autoprueba_turnos(cfg, segundos=20.0):
    """Las autopruebas de la piel por turnos y de la cache de la arqueologia (fase
    11 v18, motor v101), con los valores de cfg y mundos propios: [(texto, bien,
    detalle)]. No toca el mundo de la sesion; los bufers de la piel se vacian."""
    res = []
    fps = 30.0
    cfg = dict(cfg, refresco_piel=0.25, turnos=1, cache_arq=1)
    try:
        # 1. equivalencia: una vuelta por turnos publica lo mismo que la vuelta entera
        iguales, detalle = True, []
        for k, tema in enumerate(TEMAS):
            c = dict(cfg, tema=k)
            W, t1 = _mundo_prueba_piel(c, segundos)
            T0 = t1 + 1.0
            _TURNOS.clear()
            now, A, turnos = T0 - c['refresco_piel'], None, 0
            for f in range(60):
                o, inf = _piel_foto(W, c, now)
                if f > 0 and inf.get('publica'):
                    A, turnos = o, inf.get('turnos', 0)
                    break
                now += 1.0 / fps
            _TURNOS.clear()
            B, _ = _piel_foto(W, dict(c, turnos=0), T0)
            bien = A is not None and A == B and any(_mods(A).values())
            iguales = iguales and bien
            detalle.append('%s %d turnos %d filas%s' % (tema, turnos, sum(len(v) for v in (A or {}).values()),
                                                        '' if bien else ' DISTINTAS'))
        res.append(('equivalencia: una vuelta por turnos publica las mismas filas que la vuelta entera en el '
                    'mismo instante (%s)' % ', '.join(detalle), iguales, ''))
        # y la arqueologia: con la cache, las mismas filas que sin ella
        ca = dict(cfg, nivel=max(16, cfg['nivel']), tema=0)
        W, t1 = _mundo_prueba_piel(ca, segundos, eras=2)
        obj = max(range(N), key=lambda x: (W['occ'][x], -x))
        cut(W, ca, obj, 2, 1, t1)
        tarde = t1 + ca['scar_time'] + 1.0
        _ARQ.clear()
        filas = []
        for cache in (1, 1, 0):
            o = {}
            build_arqueologia(W, dict(ca, cache_arq=cache), tarde, o)
            filas.append(o)
        n_arq = sum(len(v) for v in filas[0].values())
        res.append(('equivalencia: la arqueologia con Cachearq (calculada y de la cache) da las mismas filas que '
                    'sin ella (%d piezas)' % n_arq, filas[0] == filas[1] == filas[2] and n_arq > 0, ''))
        # 4. cicatriz: con un corte reciente las filas cambian en cada fotograma; luego se congelan
        _ARQ.clear()
        st = ca['scar_time']
        cambian = quietas = 0
        malas = []
        antes = None
        k_max = int(st / 0.25) + 6
        for k in range(k_max + 1):
            now = t1 + 0.25 * k
            o = {}
            build_arqueologia(W, ca, now, o)
            if antes is not None:
                if now - 0.25 - t1 < st - 1e-9:     # el anterior aun se fundia: cambian
                    cambian += o != antes
                    if o == antes:
                        malas.append(k)
                elif now - 0.25 - t1 > st + 1e-9:
                    quietas += o == antes
                    if o != antes:
                        malas.append(k)
            antes = o
        res.append(('cicatriz: con un corte reciente las filas de la arqueologia cambian en cada fotograma '
                    'hasta Cicatriz (%d) y luego se congelan (%d, de la cache: %s)'
                    % (cambian, quietas, 'si' if _ARQ.get('cache') else 'no'),
                    not malas and cambian > 0 and quietas > 0 and _ARQ.get('cache'),
                    'fotogramas mal: %s' % malas if malas else ''))
        # 2. sin publicaciones a medias: entre dos publicaciones, sin eventos, las mismas filas
        mal, pubs, vistas = [], 0, 0
        for k, tema in enumerate(TEMAS):
            c = dict(cfg, tema=k)
            W, t1 = _mundo_prueba_piel(c, segundos)
            _TURNOS.clear()
            antes = None
            for f in range(40):
                now = t1 + f / fps
                tick(W, c, now, 120.0, True)
                o, inf = _piel_foto(W, c, now)
                mo = _mods(o)
                libre = not inf.get('publica') and not inf.get('inmediatas') and not inf.get('reinicio')
                if antes is not None and libre:
                    vistas += 1
                    if mo != antes:
                        mal.append('%s %d' % (tema, f))
                pubs += bool(inf.get('publica'))
                antes = mo
        res.append(('sin publicaciones a medias: entre dos publicaciones, sin eventos, las filas de los modelos '
                    'son las mismas fotograma a fotograma (%d fotogramas, %d publicaciones)' % (vistas, pubs),
                    not mal and vistas > 0 and pubs > 0, 'cambian en %s' % ', '.join(mal[:6]) if mal else ''))
        # 3. camino inmediato: una nota cambia su celda en el acto y nada fuera de su vecindad
        c = dict(cfg, tema=0)
        W, t1 = _mundo_prueba_piel(c, segundos)
        sueltas = [x for x in range(N) if not W['occ'][x] and not any(W['occ'][j] for j in NEIGH[x])]
        if sueltas:                         # una celda suelta, sembrada y crecida (2 s)
            subir_escalon(W, c, GEO, sueltas[len(sueltas) // 2], 100, t1)
            for f in range(60):
                t1 += 1.0 / fps
                tick(W, c, t1, 120.0, True)
        _TURNOS.clear()
        now = t1
        for f in range(3):                  # a mitad de vuelta
            now = t1 + f / fps
            _piel_foto(W, c, now)
        cl0 = clusters(W, c)
        libres = [x for x in range(N) if W['occ'][x] and W['own'][x] == GEO and cl0['de'][x] < 0 and
                  W['occ'][x] + 1 < c['th_branch'] and x in _TURNOS['pub']['cubos']]
        bien, texto = False, 'ninguna celda ocupada suelta'
        if libres:
            x = libres[0]
            antes = dict(_TURNOS['pub']['cubos'])
            now += 1.0 / fps
            note_on(W, c, GEO, cell_note(x), 100, now)
            o, inf = _piel_foto(W, c, now)
            despues = _TURNOS['pub']['cubos']
            cl = clusters(W, c)
            vec = set([x]) | set(NEIGH[x])
            if cl['de'][x] >= 0:
                vec |= set(cl['celdas'][cl['de'][x]])
            fuera = [i for i in set(antes) | set(despues) if i not in vec and antes.get(i) is not despues.get(i)]
            propia = x in despues and despues[x] is not antes.get(x) and \
                despues[x]['filas'] != antes[x]['filas']
            bien = propia and not fuera and not inf.get('publica')
            texto = 'celda %d: sus filas en el mismo fotograma %s; inmediatas %d; fuera de su vecindad cambian %d' \
                % (x, 'si' if propia else 'NO', inf.get('inmediatas', 0), len(fuera))
        res.append(('camino inmediato: una nota en una celda cambia sus filas en ese fotograma y no cambia las de '
                    'ninguna celda fuera de su vecindad y su cluster (%s)' % texto, bien, ''))
        # 5. reinicio: Resetmundo, Forzarciclo y un cambio de Tema publican una vuelta completa
        c = dict(cfg, tema=0)
        W, t1 = _mundo_prueba_piel(c, segundos)
        _TURNOS.clear()
        for f in range(3):
            _piel_foto(W, c, t1 + f / fps)
        casos = []
        W2, _ = _mundo_prueba_piel(c, segundos / 2.0)          # Resetmundo: otro mundo
        casos.append(('Resetmundo', W2, c))
        casos.append(('Tema', W2, dict(c, tema=1)))
        casos.append(('Forzarciclo', W2, dict(c, tema=1)))
        bien, det = True, []
        now = t1 + 3.0 / fps
        for nombre, Wx, cx in casos:
            if nombre == 'Forzarciclo':
                end_cycle(Wx, cx, now)
            now += 1.0 / fps
            o, inf = _piel_foto(Wx, cx, now)
            P = _piel_ctx(Wx, cx, now)
            dib = set(i for i in P['celdas'] if _piel_cubo(P, i) is not None)
            ok_ = bool(inf.get('reinicio')) and set(_TURNOS['pub']['cubos']) == dib and \
                (bool(dib) or nombre == 'Forzarciclo')
            bien = bien and ok_
            det.append('%s %s (%d celdas)' % (nombre, 'si' if ok_ else 'NO', len(dib)))
        res.append(('reinicio: Resetmundo, Forzarciclo y un cambio de Tema publican una vuelta completa en el '
                    'fotograma siguiente (%s)' % ', '.join(det), bien, ''))
        # 6. contrato: chop_names sigue listando todas las geometrias instanciadas
        nombres = set(x[2:] for x in chop_names(cfg) if x.startswith('i_'))
        faltan = set()
        for k, tema in enumerate(TEMAS):
            c = dict(cfg, tema=k)
            W, t1 = _mundo_prueba_piel(c, segundos / 2.0)
            _TURNOS.clear()
            o, _ = _piel_foto(W, c, t1)
            faltan |= set(g for g, f in o.items() if f and g not in nombres)
        res.append(('contrato: chop_names lista todas las geometrias que publica la piel por turnos',
                    not faltan, 'faltan %s' % ', '.join(sorted(faltan)) if faltan else ''))
    finally:
        _TURNOS.clear()
        _ARQ.clear()
    return res


def _ciudad_res_vacio(W, cfg):
    """El resumen de la ciudad para la leyenda, vacio (antes de la primera celda)."""
    return dict(lenguajes=[0, 0, 0], edificios=0, tipos=set(), obra={}, gruas=0, colonias={}, marcos={},
                protagonistas={}, mutacion=mutacion_actual(W, cfg),
                fuente=MUTACION_FUENTES[int(cfg.get('mutacion_fuente', 0)) % 2],
                epocas=[0, 0, 0], cortas={}, integradas={}, tema=tema_de(cfg))


def _ciudad_ctx(W, cfg, now, cl, tf, bases, paso):
    """Lo que la ciudad mira del planeta entero (fase 11 v10; motor v101, una vez
    por vuelta): el edificio de cada celda (el cluster mira a sus vecinas), la
    distancia, las ventanas, la red, el recurso de cada mina, el carbon de cada
    planta y las piezas de cada cluster. ctx['info']: las celdas que se dibujan."""
    doce = cfg['nivel'] >= 12
    tiempo = cfg['nivel'] >= 17
    bq = beat_stop(W, cfg) if tiempo else 0.0
    respaldo = doce and cfg.get('respaldo', 0)
    info = {}
    ck = (tuple(cfg.get(k) for k in _CFG_CIU), id(cfg.get('catalogo')), GRID['lo'], GRID['hi'])
    for i in range(N):
        if W['occ'][i] > 0 and W['own'][i] and W['vh'][i] > 0.005:
            info[i] = info_ciudad(W, cfg, i, cl, ck)
    cerca = {}
    if cfg.get('superficie'):
        px_lod = None
    else:
        px_lod = ENCUADRE_DEF * 720.0 / (2.0 * (top_radius(W, cfg) + RETICULA_SOBRE_DEF))
    lod_px = cfg.get('lod_ind', 60.0) if tema_de(cfg) == 'industria' else cfg.get('lod_ciudad', 60.0)

    def es_cerca(i):
        v = cerca.get(i)
        if v is None:
            v = cerca[i] = px_lod is None or \
                min(SIZE_EW[i], SIZE_NS[i]) * _len(bases[i]) * px_lod >= lod_px
        return v
    res = _ciudad_res_vacio(W, cfg)
    luz = {}

    def luces(i):                       # las ventanas de la celda (fase 17), una vez por calculo
        v = luz.get(i)
        if v is None:
            v = luz[i] = ventanas_celda(W, cfg, i, bq) if tiempo and doce and not respaldo else 0
        return v
    ctx = dict(cl=cl, bases=bases, info=info, doce=doce, respaldo=respaldo, res=res, gruas=[], cerca=es_cerca,
               tope=0.96 * altura_max(cfg), lejos=lambda i: not es_cerca(i), luces=luces)
    # fase 11 v11: la industria. El pulso (master_beat desde la fase 17; si no, el reloj),
    # el recurso de cada mina, el carbon que llega a cada planta, la red y el modular
    if tiempo:
        ctx['bq'] = bq
    else:
        ctx['bq'] = now / max(1e-6, paso * max(1, int(cfg.get('steps_per_beat', 4))))
    recursos = {}

    def recurso(i):
        v = recursos.get(i)
        if v is None:
            v = recursos[i] = recurso_celda(W, cfg, i)
        return v
    ind = tema_de(cfg) == 'industria'
    tj = tejido(W, cfg) if ind and cfg['nivel'] >= 13 else {}
    red = tj.get('red') or {}
    carbon_pl = set(p for p, rs in (tj.get('fc') or {}).get('fuente', {}).items() if 'carbon' in rs)
    ctx.update(recurso=recurso, apagadas=set(red.get('apagadas', ())),
               carbon=lambda i: recurso(i) == 'carbon' if info.get(i, {}).get('esp') == 'mina' else i in carbon_pl,
               humo=[0], ruido=float(W['modular'].get('ruido', 0.0)) if cfg['nivel'] >= 19 else 0.0,
               lfo=float(W['modular'].get('lfo', 0.5)) if cfg['nivel'] >= 19 else 0.5,
               saturacion=float(W['modular'].get('saturacion', 0.0)) if cfg['nivel'] >= 19 else 0.0)
    ctx['cluster'] = piezas_de_cluster(W, cfg, ctx, tf)
    ctx['cadenas'] = dict((e, cadenas_de(cfg, tema_de(cfg), e)[0])
                          for e in ('informal', 'planificada', 'mina', 'energia'))
    ctx['industria'] = ind
    return ctx


def _ciudad_resumen(W, cfg, ctx):
    """El resumen de la ciudad para la leyenda (una copia: el de ctx no cambia)."""
    res = dict(ctx['res'])
    res['tipos'] = len(res['tipos'])
    if ctx.get('industria'):            # la leyenda INDUSTRIA
        info = ctx['info']
        res['humo'] = ctx['humo'][0]
        res['recursos'] = dict((r, 0) for r in RECURSOS)
        for i in info:
            if info[i]['esp'] == 'mina':
                res['recursos'][ctx['recurso'](i)] += 1
        res['plantas'] = sum(1 for i in info if info[i]['esp'] == 'energia')
        res['epoca'] = EPOCAS[epoca_actual(cfg, W)]
    return res


def build_ciudad(W, cfg, now, out, cl, tf, bases, paso, arde, bomba=None):
    """La ciudad entera (fase 11 v10): una pasada para saber el edificio de cada
    celda y otra para dibujarlo. Devuelve (piezas, resumen para la leyenda).
    Desde el motor v101 la piel la monta por partes (_piel_ctx, _piel_celda,
    _piel_global); esto queda para quien dibuje solo la ciudad."""
    ctx = _ciudad_ctx(W, cfg, now, cl, tf, bases, paso)
    doce = cfg['nivel'] >= 12
    piezas = 0
    bomba = _Bomba(W, cfg, now, out)
    for i in sorted(ctx['info']):
        bomba.cerrar()
        n = normal_i(i)
        cw, cl_ = _cell_sizes(_len(bases[i]), i)
        bomba.abrir(i, bases[i], n, cw, cl_)
        rug = rugosidad(cfg, W['vel'][i]) if doce else 1.0
        kb, fl = rebote(cfg, W, i, now, paso)
        piezas += piel_ciudad(W, cfg, ctx, i, rug, kb, fl, arde, out, now, paso)
    bomba.cerrar()
    piezas += emitir_gruas(W, cfg, ctx, out, now, paso)
    return piezas, _ciudad_resumen(W, cfg, ctx)

# -----------------------------------------------------------------------------
# 1. NUCLEO - la naturaleza legible (fase 11 v5, motor v46)
# -----------------------------------------------------------------------------
# A 13-50 px de alto el detalle de un arbol no existe: la ciudad se lee por su
# orden repetido, su silueta y su escalera; la naturaleza, por masa, silueta y
# bandas de color, como la cartografia de montana a escala pequena.
#   ESCALERA   1 brote, 2+ arbol (frondosa o conifera), Umbralram arboleda (5 a
#              12 copas), Umbralfusion bosque (dosel continuo) y, desde
#              Umbralmonte, monte boscoso: la ocupacion extra ya no anade
#              piezas, sube el terreno de la celda y el bosque lo cubre.
#   RELIEVE    no son piezas: un mapa de alturas (TERRENO_W x TERRENO_H, lat/lon)
#              que desplaza una sola malla (la esfera 'terreno', en el shader).
#              Una celda suelta es un cono con ruido de crestas (ridged
#              multifractal); un cluster de 3 o mas, una cordillera con la
#              cresta continua por su eje (el camino entre sus dos celdas mas
#              alejadas) y estribaciones por la mascara de vecinas. Las
#              columnas de basalto quedan como textura de las laderas bajas.
#   ARBOLES    (motor v48) cada arbol son piezas instanciadas (arbol_pisos):
#              tronco oscuro y mate que se ve por debajo de la copa (Troncofrac),
#              2 a 4 ramas oblicuas (Angulorama) y 1 a 4 pisos planos
#              (Pisoscopa) que se estrechan hacia arriba (Anchocopa); 9 piezas
#              como mucho. En el bosque (clusters de DOSEL_MIN celdas o mas y
#              bosques sueltos) el piso de abajo llega a las vecinas: el dosel
#              se cierra; la coronacion es un arbol emergente en punta.
#   PISOS      el color sale de la altura sobre el suelo local, en fraccion de
#              la maxima posible (alto_hipso): basal, montano, limite del
#              bosque, roca y nieve (Limitebosque, Limitenieve). Ni la concha
#              ni el tinte del secuenciador tocan el albedo: el tinte va al
#              borde (uTinte, fresnel) y a la loseta de la celda.
#   LOD        con la camara de globo, los arboles jovenes sin ramas; cerca
#              (Lodnat px por celda o camara de superficie), con ellas.

NAT_K_RELIEVE = 1.5          # el cono de relieve, 1,5 veces la altura de su formacion
PASOS_MONTE = 6              # el monte sube del todo en 6 ocupaciones desde Umbralmonte
DOSEL_MIN = 4                # celdas de un cluster para el dosel continuo
CAPITAL_K = 1.08             # la cumbre de la capital, algo mas alta
TERRENO_W, TERRENO_H = 512, 256
HUNDIDO = 0.06               # sin relieve, la malla se hunde bajo las losetas
CANOPIA_K = 0.95             # la copa, de la altura de la formacion
COL_BASALTO_PIE = (0.20, 0.21, 0.24)
COL_TRONCO = (0.17, 0.12, 0.08)    # madera oscura (tronco y ramas, siempre mates)
PISOS_GIRO = 17.0            # cada piso, girado respecto al anterior
RAMA_DESDE = 2.0 / 3.0       # las ramas salen del tercio superior del tronco visible (motor v49)
RAMPA_COLS = ['pos', 'r', 'g', 'b', 'a']
# colores de los pisos (cartografia de montana): verde profundo, verde azulado
# de coniferas, verde y ocre del limite, gris calido facetado y nieve
PISO_BASAL = ((0.11, 0.29, 0.11), (0.15, 0.34, 0.13))
PISO_PRADO, PISO_UMBRIA, PISO_LOMA = (0.21, 0.40, 0.13), (0.10, 0.28, 0.11), (0.20, 0.36, 0.12)   # motor v97
PISO_MONTANO = ((0.07, 0.23, 0.18), (0.10, 0.25, 0.20))
PISO_LIMITE = (0.38, 0.37, 0.21)
PISO_ROCA = ((0.50, 0.46, 0.40), (0.31, 0.29, 0.27))
PISO_NIEVE = ((0.92, 0.94, 0.97), (1.0, 1.0, 1.0))


def monte(W, cfg, i):
    """Lo que sube el terreno de la celda i (naturaleza): nada por debajo de
    Umbralmonte; desde ahi, Alturamonte x el limite en PASOS_MONTE ocupaciones."""
    o = W['occ'][i]
    u = int(cfg['umbral_monte'])
    if o < u or not W['own'][i]:
        return 0.0
    return max(0.0, cfg['altura_monte']) * limit(cfg) * min(1.0, (o - u + 1) / float(PASOS_MONTE))


def alto_hipso(cfg):
    """La altura maxima posible sobre el suelo local (el 100 % de los pisos):
    una formacion en el limite mas el monte entero."""
    return max(1e-6, limit(cfg) * (1.0 + max(0.0, cfg['altura_monte'])))


def _limites_pisos(cfg):
    lb = max(0.40, min(0.85, float(cfg['limite_bosque'])))
    ln = max(lb + 0.10, min(0.98, float(cfg['limite_nieve'])))
    return lb, ln


def rampa_hipso(cfg):
    """[(posicion 0-1, (r, g, b))]: la rampa de los pisos (la del Ramp TOP)."""
    lb, ln = _limites_pisos(cfg)
    # motor v97: el piso basal, con mas paleta (pradera clara de la costa, umbria, loma seca)
    return [(0.0, PISO_BASAL[0]), (0.05, PISO_PRADO), (0.14, PISO_UMBRIA), (0.26, PISO_LOMA),
            (0.35, PISO_BASAL[1]), (0.36, PISO_MONTANO[0]),
            (lb - 0.05, PISO_MONTANO[1]), (lb, PISO_LIMITE), (lb + 0.05, PISO_ROCA[0]),
            (ln - 0.01, PISO_ROCA[1]), (ln, PISO_NIEVE[0]), (1.0, PISO_NIEVE[1])]


_LUT_PISOS = {}


def color_piso(cfg, h):
    """Color del piso a la altura relativa h (0-1) (tabla de 512 pasos)."""
    clave = (cfg['limite_bosque'], cfg['limite_nieve'])
    lut = _LUT_PISOS.get(clave)
    if lut is None:
        if len(_LUT_PISOS) > 32:
            _LUT_PISOS.clear()
        lut = _LUT_PISOS[clave] = [_color_piso(cfg, k / 511.0) for k in range(512)]
    return lut[int(max(0.0, min(1.0, h)) * 511.0 + 0.5)]


def _color_piso(cfg, h):
    claves = rampa_hipso(cfg)
    h = max(0.0, min(1.0, h))
    for (a, ca), (b, cb) in zip(claves, claves[1:]):
        if h <= b:
            return _mix(ca, cb, (h - a) / max(1e-6, b - a))
    return claves[-1][1]


def rug_piso(cfg, h):
    """Rugosidad del piso: mate abajo (0,9), roca (0,7), nieve brillante (0,3)."""
    lb, ln = _limites_pisos(cfg)
    return 0.9 if h < lb + 0.05 else (0.7 if h < ln else 0.3)


def rampa_filas(cfg):
    """Filas de la tabla 'rampa_hipso_claves' (pos r g b a) del Ramp TOP."""
    return [list(RAMPA_COLS)] + [['%.4f' % p, '%.4f' % c[0], '%.4f' % c[1], '%.4f' % c[2], '1']
                                 for p, c in rampa_hipso(cfg)]


# --- el mapa de alturas ---------------------------------------------------------

_TERRENO = {}


def _np():
    try:
        import numpy
        return numpy
    except Exception:
        return None


def _valor3(np, X):
    """Ruido de valor 3D (trilineal suave) en los puntos X (..., 3)."""
    i = np.floor(X)
    f = X - i
    f = f * f * (3.0 - 2.0 * f)
    k = np.array([127.1, 311.7, 74.7])

    def h(o):
        q = (i + np.array(o)) @ k
        return np.modf(np.sin(q) * 43758.5453)[0] % 1.0
    c = {}
    for o in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)):
        c[o] = h(o)
    fx, fy, fz = f[..., 0], f[..., 1], f[..., 2]
    a = c[(0, 0, 0)] + (c[(1, 0, 0)] - c[(0, 0, 0)]) * fx
    b = c[(0, 1, 0)] + (c[(1, 1, 0)] - c[(0, 1, 0)]) * fx
    cc = c[(0, 0, 1)] + (c[(1, 0, 1)] - c[(0, 0, 1)]) * fx
    d = c[(0, 1, 1)] + (c[(1, 1, 1)] - c[(0, 1, 1)]) * fx
    return (a + (b - a) * fy) + ((cc + (d - cc) * fy) - (a + (b - a) * fy)) * fz


def _ruido_crestas(np, D, octavas=4, f0=6.0):
    """Ridged multifractal (Musgrave) sobre la esfera, normalizado a 0-1: crestas
    finas y valles anchos; cada octava pesa segun la anterior."""
    out = np.zeros(D.shape[:-1])
    peso, amp = np.ones(D.shape[:-1]), 1.0
    for o in range(octavas):
        n = _valor3(np, D * (f0 * 2.0 ** o) + 17.3 * o)
        r = 1.0 - np.abs(2.0 * n - 1.0)
        r = r * r * peso
        peso = np.clip(r * 2.0, 0.0, 1.0)
        out += r * amp
        amp *= 0.5
    lo, hi = float(out.min()), float(out.max())
    return ((out - lo) / max(1e-6, hi - lo)).astype(np.float32)


def _rejilla(np):
    """Direcciones de cada texel del mapa (fila 0 = polo sur, columna 0 = -180),
    la celda mas cercana de cada uno y el ruido de crestas. Una por reticula."""
    clave = (GRID['lo'], GRID['hi'])
    g = _TERRENO.get('rejilla')
    if g is not None and g[0] == clave:
        return g[1]
    H, Wd = TERRENO_H, TERRENO_W
    lat = ((np.arange(H) + 0.5) / H - 0.5) * math.pi
    lon = ((np.arange(Wd) + 0.5) / Wd - 0.5) * 2.0 * math.pi
    cl = np.cos(lat)[:, None]
    D = np.stack([cl * np.cos(lon)[None, :], np.repeat(np.sin(lat)[:, None], Wd, 1),
                  cl * np.sin(lon)[None, :]], -1)
    Nn = np.array(NORMALS)
    celda = np.zeros((H, Wd), dtype=np.int32)
    for r0 in range(0, H, 32):                 # por bandas: la matriz entera no cabe comoda
        celda[r0:r0 + 32] = np.argmax(D[r0:r0 + 32] @ Nn.T, axis=-1)
    rej = dict(D=D, celda=celda, ruido=_ruido_crestas(np, D), lat=lat, lon=lon)
    for nm, f0 in (('costa', 6.0), ('islotes', 21.0)):     # motor v97: la costa y los islotes
        v_ = _valor3(np, D * f0 + 31.7) * 0.65 + _valor3(np, D * (2.3 * f0) + 11.1) * 0.35
        lo_, hi_ = float(v_.min()), float(v_.max())
        rej[nm] = ((v_ - lo_) / max(1e-6, hi_ - lo_)).astype(np.float32)
    _TERRENO['rejilla'] = (clave, rej)
    return rej


def _ventana(np, n, radio):
    """(filas, columnas) del mapa que cubren un casquete de 'radio' rad
    alrededor de n (las columnas dan la vuelta)."""
    H, Wd = TERRENO_H, TERRENO_W
    la = math.asin(max(-1.0, min(1.0, n[1])))
    lo = math.atan2(n[2], n[0])
    r0 = max(0, int((la - radio + math.pi / 2) / math.pi * H) - 1)
    r1 = min(H, int((la + radio + math.pi / 2) / math.pi * H) + 2)
    filas = np.arange(r0, r1)
    if abs(la) + radio > 1.45:
        return filas, np.arange(Wd)
    dl = radio / max(0.05, math.cos(abs(la) + radio))
    c0 = int(math.floor((lo - dl) / (2 * math.pi) * Wd + Wd / 2.0)) - 1
    c1 = int(math.ceil((lo + dl) / (2 * math.pi) * Wd + Wd / 2.0)) + 2
    if c1 - c0 >= Wd:
        return filas, np.arange(Wd)
    return filas, np.arange(c0, c1) % Wd


def _semiejes(c, k):
    """Semiejes (rad) del casquete de la celda c, k veces la mitad de la celda."""
    return max(1e-3, 0.5 * SIZE_EW[c] * k), max(1e-3, 0.5 * SIZE_NS[c] * k)


def _eje_cluster(celdas, mascara):
    """El eje de una cordillera: el camino (por la mascara de vecinas) entre
    las dos celdas mas alejadas del cluster. Doble BFS; a igualdad, indices."""
    dentro = set(celdas)

    def bfs(a):
        padre, frente = {a: None}, [a]
        while frente:
            sig = []
            for c in frente:
                for j in sorted(mascara[c]):
                    if j in dentro and j not in padre:
                        padre[j] = c
                        sig.append(j)
            if not sig:
                return frente, padre
            frente = sig
        return frente, padre
    lejos, _ = bfs(min(celdas))
    a = min(lejos)
    lejos, padre = bfs(a)
    b = min(lejos)
    camino = [b]
    while padre[camino[-1]] is not None:
        camino.append(padre[camino[-1]])
    return camino[::-1]


def rasgos_terreno(W, cfg, cl=None):
    """Lo que levanta el terreno: [('cono', celda, alto, k), ('cresta', a, b,
    alto_a, alto_b, collado), ('domo', celda, alto)] y el resumen (cordilleras,
    capitales). Alturas sobre el suelo local, de la ocupacion (no del stop-motion:
    el mapa solo se rehace cuando cambia la ocupacion)."""
    if cfg['nivel'] < 11 or tema_de(cfg) != 'naturaleza':
        return [], dict(cordilleras=0, montes=0, ejes=[], volcanes=[], islas=0, archipielagos=0)
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), GRID['lo'], GRID['hi'],
             cfg.get('oceano', 0), cfg.get('volcanes', 0.0), cfg['caos'],
             tuple(W['vel']) if cfg.get('volcanes', 0.0) > 0 else None, cfg['umbral_vecindad'], cfg['peso_vecina'], cfg['min_cluster'], cfg['th_fusion'], cfg['th_branch'],
             cfg['sat_size'], cfg['umbral_monte'], cfg['altura_monte'], limit(cfg), cfg['seed_frac'],
             cfg['grow_frac'])
    v = _TERRENO.get('rasgos')
    if v is not None and v[0] == clave:
        return v[1]
    v = _rasgos_terreno(W, cfg, cl)
    _TERRENO['rasgos'] = (clave, v)
    return v


def _rasgos_terreno(W, cfg, cl=None):
    cl = cl or clusters(W, cfg)
    rel = [c for c in range(N) if W['occ'][c] > 0 and W['own'][c] == ARQ]
    alto = {}
    for c in rel:
        k = cfg['sat_size'] if W['par'][c] >= 0 else 1.0
        alto[c] = NAT_K_RELIEVE * height_for(cfg, W['occ'][c]) * k + monte(W, cfg, c)
    rasgos, ejes, cords = [], [], 0
    for k_, cs in sorted(cl['celdas'].items()):
        if W['own'][cs[0]] != ARQ:
            continue
        cap = cl['capital'][k_]
        if cap in alto:
            alto[cap] *= CAPITAL_K
        mk = cl['mascara']
        eje = _eje_cluster(cs, mk) if len(cs) >= 3 else []
        if len(eje) >= 2:
            cords += 1
            ejes.append(eje)
        en_eje = set((min(a, b), max(a, b)) for a, b in zip(eje, eje[1:]))
        for a in cs:
            for b in mk[a]:
                if b <= a or a not in alto or b not in alto:
                    continue
                silla = 0.85 if (a, b) in en_eje else (0.35 if len(cs) >= 3 else 0.5)
                rasgos.append(('cresta', a, b, round(alto[a], 3), round(alto[b], 3), silla))
    caps_rel = set(cl['capital'][k_] for k_, cs in cl['celdas'].items() if W['own'][cs[0]] == ARQ)
    volcanes = []
    for c in rel:
        # motor v97: de cuando en cuando el cono es un volcan (crater, lava y penacho)
        if es_volcan(W, cfg, c) and (cl['de'][c] < 0 or c in caps_rel):
            rasgos.append(('volcan', c, round(alto[c], 3), 1.1))
            volcanes.append((c, round(alto[c], 3)))
        else:
            rasgos.append(('cono', c, round(alto[c], 3), 1.1))
    islas = archis = 0
    if cfg.get('oceano'):                   # motor v97: cada celda ocupada es una isla sobre el mar
        tierra = [c for c in range(N) if W['occ'][c] > 0 and W['own'][c]]
        ts = set(tierra)
        for c in tierra:
            sat = W['par'][c] >= 0
            rasgos.append(('isla', c, round(isla_alto(W['occ'][c]), 3),
                           round(isla_k(W['occ'][c]) * (0.75 if sat else 1.0), 3),
                           round(max(0.0, min(1.0, (W['occ'][c] - 2) / 4.0)), 2)))
            for b in NEIGH[c]:              # dos islas vecinas que crecen se unen por un istmo
                if b > c and b in ts and min(W['occ'][c], W['occ'][b]) >= ISTMO_DESDE:
                    rasgos.append(('istmo', c, b, round(min(isla_alto(W['occ'][c]), isla_alto(W['occ'][b])), 3)))
        vistos = set()                      # islas: grupos de celdas ocupadas vecinas; archipielago: 3 o mas
        for c in tierra:
            if c in vistos:
                continue
            grupo, frente = set([c]), [c]
            while frente:
                x = frente.pop()
                for j in NEIGH[x]:
                    if j in ts and j not in grupo:
                        grupo.add(j)
                        frente.append(j)
            vistos |= grupo
            islas += 1
            archis += len(grupo) >= 3
    montes = 0
    for c in range(N):
        if W['occ'][c] > 0 and W['own'][c] == GEO:
            m_ = monte(W, cfg, c)
            if m_ > 1e-6:
                rasgos.append(('domo', c, round(m_, 3)))
                montes += 1
    return rasgos, dict(cordilleras=cords, montes=montes, ejes=ejes, volcanes=volcanes, islas=islas,
                        archipielagos=archis)


# --- motor v99: la pradera, en la tarjeta grafica -------------------------------------------
# Hasta aqui cada planta era una fila que calculaba el motor (Python) y subia por un CHOP.
# La pradera no: es UNA geometria ('pradera': una mata de hojas de pocas decenas de
# triangulos) que TouchDesigner instancia Pradera veces sin datos por instancia. El vertex
# shader de la piel (uFamilia 7) saca de su numero de instancia donde va (una espiral de
# Fibonacci sobre la esfera, con azar), lee el mapa de alturas y la deja en el suelo: solo
# en tierra firme, por encima de la playa, bajo el limite del bosque y fuera de la lava,
# mas espesa en unas manchas que en otras; la que no toca se descarta. Tamano, giro, color
# (el piso de su altura, aclarado) y vaiven con el viento, tambien alli. El motor solo dice
# cuantas (uPradera.x) y de que tamano (Mata).

def malla_pradera():
    """(puntos, normales, uv, triangulos) de la mata de la pradera: 7 hojas en abanico,
    de 3 tramos, que se arquean hacia fuera. Alto 1, radio 0,5. uv = (2 + variacion,
    profundidad, altura): hoja, como las de los ejemplares."""
    v = _MALLAS.get('pradera')
    if v is not None:
        return v
    import random
    rng = random.Random(977)
    P, Nn, U, T = [], [], [], []
    for j in range(7):
        g = math.radians(ANGULO_AUREO * j)
        fuera = (math.cos(g), 0.0, math.sin(g))
        lado = (-math.sin(g), 0.0, math.cos(g))
        alto, vuelo, ancho = rng.uniform(0.6, 1.0), rng.uniform(0.15, 0.5), rng.uniform(0.07, 0.11)
        vv = 0.9 * rng.random()
        k0 = len(P)
        nrm = _norm(_add(fuera, SUBE, 0.6))
        for q in range(4):
            t = q / 3.0
            c_ = _add(_add(_mul(fuera, 0.06 + vuelo * t * t), SUBE, alto * t), lado, 0.0)
            w = ancho * (1.0 - t) ** 0.7
            for s_ in ((-1.0, 1.0) if q < 3 else (0.0,)):
                P.append(_add(c_, lado, s_ * w))
                Nn.append(nrm)
                U.append((2.0 + vv, 0.5 * (1.0 - t), t))
        for q in range(2):
            a, b = k0 + 2 * q, k0 + 2 * q + 2
            T += [(a, a + 1, b + 1), (a, b + 1, b)]
        T.append((k0 + 4, k0 + 5, k0 + 6))
    v = _MALLAS['pradera'] = (P, Nn, U, T)
    return v


# --- motor v97: el oceano, las islas y los volcanes ----------------------------------------
# OCEANO     con Oceano (naturaleza), la malla del terreno ya no se hunde bajo las losetas
#            donde no hay relieve: flota OCEANO_LIFT por encima y el shader la pinta de mar
#            (hondo lejos de la costa, turquesa y espuma junto a ella). Cada celda ocupada
#            levanta una ISLA: una meseta baja con playa, de costa irregular (ruido), que
#            se ensancha y sube con la ocupacion hasta salirse de su celda. Dos islas
#            vecinas con ISTMO_DESDE o mas se unen por un istmo: islas grandes; desde 3 de
#            ocupacion, islotes sueltos alrededor: archipielagos. El relieve y los montes
#            van encima de la isla. Las plantas no crecen en el agua (salvo el mangle y
#            el junco) y la costa calida trae palmeras y manglares.
# VOLCANES   una celda de relieve suelta, o la capital de una cordillera, con Umbralram o
#            mas, es un volcan con probabilidad Volcanes (lo decide su semilla: la velocidad
#            fundadora y la celda, por el mapa logistico). Cono concavo con crater; el canal
#            a del mapa de alturas lleva la lava (el crater y 3 coladas), que el shader
#            enciende; un penacho de humo (la geometria 'humo') y, cada ERUPCION_CADA
#            compases, una erupcion de ERUPCION_DURA: brasas, ceniza y la lava al rojo.
OCEANO_LIFT = 0.012          # el mar, sobre la loseta (por debajo de la luz de la celda, LUZ_LIFT)
ISLA_ALTO = (0.055, 0.008)   # alto de la meseta de la isla: base + por ocupacion (hasta 8)
ISLA_K = (0.60, 0.06, 0.9)   # su radio, x media celda: base + por ocupacion, tope (v98: no se traga el mar)
ISTMO_DESDE = 3
CRATER_Q = 0.22              # radio del crater, x el del cono
CRATER_HONDO = 0.16          # lo que se hunde, x la altura del cono
ERUPCION_CADA = (12, 28)     # compases entre dos erupciones de un volcan (segun la celda)
ERUPCION_DURA = 2.0          # compases que dura


def isla_alto(occ):
    return ISLA_ALTO[0] + ISLA_ALTO[1] * min(8, max(1, int(occ)))


def isla_k(occ):
    return min(ISLA_K[2], ISLA_K[0] + ISLA_K[1] * max(1, int(occ)))


def es_volcan(W, cfg, c):
    """La celda de relieve c es un volcan: lo decide su semilla, con probabilidad Volcanes."""
    p = float(cfg.get('volcanes', 0.0))
    if p <= 0.0 or W['own'][c] != ARQ or W['par'][c] >= 0 or W['occ'][c] < int(cfg['th_branch']):
        return False
    return logistica(semilla_caos(W['vel'][c], c + 531), cfg['caos'], 2)[1] < p


def erupcion(cfg, c, now, paso):
    """0-1: la erupcion del volcan de la celda c en el instante now (0, dormido)."""
    compas = max(1e-6, paso * max(1, int(cfg['steps_per_beat'])) * max(1, int(cfg['beats_per_bar'])))
    P = ERUPCION_CADA[0] + int(_hash01(c, 613) * (ERUPCION_CADA[1] - ERUPCION_CADA[0] + 1))
    f = (now / compas + _hash01(c, 617) * P) % P
    if f >= ERUPCION_DURA:
        return 0.0
    return math.sqrt(max(0.0, math.sin(math.pi * f / ERUPCION_DURA)))


FORMAS_MAX, PARCHES_MAX = 900, 700      # motor v101: las caches del mapa (las menos usadas salen)


def _lru(cache, clave, hacer, tope):
    """Una cache que olvida lo menos usado (sin vaciarse de golpe, que obligaria a
    rehacerlo todo en un fotograma)."""
    v = cache.pop(clave, None)
    if v is None:
        v = hacer()
        if len(cache) >= tope:
            for k in list(cache)[:len(cache) - int(0.75 * tope)]:
                del cache[k]
    cache[clave] = v
    return v


def _forma(clave, hacer):
    """Motor v101: la forma de un parche (filas, columnas, f 0-1) no depende de su
    alto; se guarda y el alto solo la multiplica (una nota cambia el alto de los
    istmos y de los conos, no su forma)."""
    return _lru(_TERRENO.setdefault('formas', {}), clave, hacer, FORMAS_MAX)


def _isla(np, rej, c, H, k, islotes):
    """El parche de la isla de la celda c: meseta de alto H con playa; la costa la
    ondula el ruido y, con 'islotes', hay islotes en el anillo de alrededor."""
    filas, cols, f = _forma(('isla', GRID['lo'], GRID['hi'], c, k, islotes), lambda: _isla_forma(np, rej, c, k, islotes))
    return filas, cols, H * f, float(H)


def _isla_forma(np, rej, c, k, islotes):
    n = NORMALS[c]
    e, t = tangents(n)
    hx, hz = _semiejes(c, k)
    filas, cols = _ventana(np, n, 1.75 * max(hx, hz))
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    x = D @ np.array(e) / hx
    z = D @ np.array(t) / hz
    q = np.sqrt(x * x + z * z)
    q = np.where(D @ np.array(n) > 0.0, q, 9.0)
    f = _smooth(np, 1.0, 0.70, q + 0.62 * (rej['costa'][ix] - 0.5))
    if islotes > 0:
        anillo = _smooth(np, 0.95, 1.12, q) * _smooth(np, 1.7, 1.45, q)
        f = np.maximum(f, 0.6 * anillo * _smooth(np, 0.84 - 0.12 * islotes, 0.92 - 0.12 * islotes,
                                                 rej['islotes'][ix]))
    return filas, cols, f


def _istmo(np, rej, a, b, H):
    """El parche del istmo que une las islas de a y b."""
    filas, cols, f = _forma(('istmo', GRID['lo'], GRID['hi'], a, b), lambda: _istmo_forma(np, rej, a, b))
    return filas, cols, H * f, float(H)


def _istmo_forma(np, rej, a, b):
    na, nb = np.array(NORMALS[a]), np.array(NORMALS[b])
    mid = _norm(tuple((na + nb) / 2.0))
    medio = 0.5 * (min(SIZE_EW[a], SIZE_NS[a]) + min(SIZE_EW[b], SIZE_NS[b]))
    filas, cols = _ventana(np, mid, 0.5 * float(np.linalg.norm(na - nb)) + 0.5 * medio)
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    ab = nb - na
    u = np.clip(((D - na) @ ab) / max(1e-9, float(ab @ ab)), 0.0, 1.0)
    cpt = na + u[..., None] * ab
    cpt /= np.linalg.norm(cpt, axis=-1, keepdims=True)
    dist = np.linalg.norm(D - cpt, axis=-1) / (0.22 * medio) + 0.5 * (rej['costa'][ix] - 0.5)
    f = _smooth(np, 1.0, 0.55, dist)
    return filas, cols, f


def _lava(np, rej, c, k):
    """(filas, columnas, lava 0-1) del volcan de la celda c: 1 en el crater y unas
    coladas que bajan por la ladera (0,6), cada volcan las suyas."""
    n = NORMALS[c]
    e, t = tangents(n)
    hx, hz = _semiejes(c, k)
    filas, cols = _ventana(np, n, 1.1 * max(hx, hz))
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    x = D @ np.array(e) / hx
    z = D @ np.array(t) / hz
    q = np.sqrt(x * x + z * z)
    q = np.where(D @ np.array(n) > 0.0, q, 9.0)
    L = _smooth(np, 0.85 * CRATER_Q, 0.55 * CRATER_Q, q)
    th = np.arctan2(z, x)
    for j in range(3):
        a0 = 2.0 * math.pi * (_hash01(c, 701 + j) + j / 3.0)
        largo = 0.45 + 0.4 * _hash01(c, 711 + j)
        da = np.abs(np.angle(np.exp(1j * (th - a0 - 0.6 * np.sin(5.0 * q + j)))))
        colada = np.exp(-(da * q / 0.045) ** 2) * _smooth(np, 0.6 * CRATER_Q, CRATER_Q, q) \
            * _smooth(np, largo, 0.7 * largo, q)
        L = np.maximum(L, 0.6 * colada)
    return filas, cols, L


def _pintar(np, rej, n, e, t, hx, hz, H, perfil):
    """El parche de un casquete (cono o domo) de alto H: (filas, columnas,
    alturas, alto del rasgo)."""
    filas, cols, f = _forma(('casquete', n, hx, hz, perfil),
                            lambda: _pintar_forma(np, rej, n, e, t, hx, hz, perfil))
    return filas, cols, H * f, float(H)


def _pintar_forma(np, rej, n, e, t, hx, hz, perfil):
    filas, cols = _ventana(np, n, 1.25 * max(hx, hz))
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    x = D @ np.array(e) / hx
    z = D @ np.array(t) / hz
    q = np.sqrt(x * x + z * z)
    q = np.where(D @ np.array(n) > 0.0, q, 9.0)
    if perfil == 'domo':
        f = np.clip(1.0 - q * q, 0.0, 1.0) ** 2
    elif perfil == 'volcan':                # motor v97: ladera concava y crater
        f = np.clip(1.0 - q, 0.0, 1.0) ** 1.35
        fc = (1.0 - CRATER_Q) ** 1.35
        f = np.where(q < CRATER_Q, fc - CRATER_HONDO * (1.0 - (q / CRATER_Q) ** 2), f)
    else:
        f = np.clip(1.0 - q, 0.0, 1.0) ** 1.1
    return filas, cols, f


def _cresta(np, rej, a, b, ha, hb, silla):
    """El parche de la cresta de a a b: el alto baja del de cada cumbre al
    collado (silla x la media) y la anchura es la de media celda."""
    filas, cols, u, sf, perfil = _forma(('cresta', GRID['lo'], GRID['hi'], a, b, silla),
                                        lambda: _cresta_forma(np, rej, a, b, silla))
    H = (ha + (hb - ha) * u) * sf
    return filas, cols, H * perfil, H


def _cresta_forma(np, rej, a, b, silla):
    """Lo que de la cresta no depende de los altos (motor v101: se guarda)."""
    na, nb = np.array(NORMALS[a]), np.array(NORMALS[b])
    mid = _norm(tuple((na + nb) / 2.0))
    medio = 0.5 * (min(SIZE_EW[a], SIZE_NS[a]) + min(SIZE_EW[b], SIZE_NS[b]))
    filas, cols = _ventana(np, mid, 0.5 * float(np.linalg.norm(na - nb)) + medio)
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    ab = nb - na
    u = np.clip(((D - na) @ ab) / max(1e-9, float(ab @ ab)), 0.0, 1.0)
    cpt = na + u[..., None] * ab
    cpt /= np.linalg.norm(cpt, axis=-1, keepdims=True)
    dist = np.linalg.norm(D - cpt, axis=-1)
    w = 0.42 * medio
    return (filas, cols, u, silla + (1.0 - silla) * np.abs(2.0 * u - 1.0) ** 1.5,
            np.clip(1.0 - dist / w, 0.0, 1.0) ** 1.15)


def _parche(np, rej, r):
    """El parche de un rasgo (se guarda por rasgo: al cambiar una celda solo
    se recalculan sus rasgos)."""
    cache = _TERRENO.setdefault('parches', {})
    v = cache.get(r)
    if v is not None:
        return v
    if r[0] == 'cresta':
        v = _cresta(np, rej, *r[1:])
    elif r[0] == 'isla':
        v = _isla(np, rej, *r[1:])
    elif r[0] == 'istmo':
        v = _istmo(np, rej, *r[1:])
    else:
        c = r[1]
        e_, t_ = tangents(NORMALS[c])
        hx, hz = _semiejes(c, r[3] if r[0] in ('cono', 'volcan') else 1.1)
        v = _pintar(np, rej, NORMALS[c], e_, t_, hx, hz, r[2], r[0])
    if len(cache) >= PARCHES_MAX:     # motor v101: salen los de los rasgos que ya no estan
        vivos = (_TERRENO.get('capas') or {}).get('rasgos', ())
        for k in [k for k in cache if k not in vivos and k[0] != 'lava'][:len(cache) - int(0.75 * PARCHES_MAX)]:
            del cache[k]
    cache[r] = v
    return v


def _sobre(np, dst, hloc, parche):
    """El maximo del mapa y el parche, y el alto del rasgo que gana. Motor v101:
    con las filas seguidas y las columnas seguidas (o dando la vuelta una vez),
    por bloques (mucho mas rapido que los indices sueltos)."""
    filas, cols, v, H = parche
    nf, nc = len(filas), len(cols)
    if not nf or not nc:
        return
    if int(filas[-1]) - int(filas[0]) == nf - 1:
        c0_, c1_ = int(cols[0]), int(cols[-1])
        if c1_ - c0_ == nc - 1:
            cortes = ()
        elif c0_ > c1_ and TERRENO_W - c0_ < nc and int(cols[TERRENO_W - c0_ - 1]) == TERRENO_W - 1 and \
                c1_ == nc - (TERRENO_W - c0_) - 1:
            cortes = (TERRENO_W - c0_ - 1,)       # da la vuelta una vez (las de _ventana)
        else:
            cortes = np.flatnonzero(np.diff(cols) != 1)
        if len(cortes) <= 1:
            rs = slice(int(filas[0]), int(filas[-1]) + 1)
            tramos = [(0, nc)] if not len(cortes) else [(0, int(cortes[0]) + 1), (int(cortes[0]) + 1, nc)]
            h2 = np.ndim(H) == 2
            for a, b in tramos:
                cs = slice(int(cols[a]), int(cols[b - 1]) + 1)
                vv = v[:, a:b]
                cur = dst[rs, cs]
                gana = vv > cur
                dst[rs, cs] = np.where(gana, vv, cur)
                hloc[rs, cs] = np.where(gana, H[:, a:b] if h2 else H, hloc[rs, cs])
            return
    ix = np.ix_(filas, cols)
    cur = dst[ix]
    gana = v > cur
    dst[ix] = np.where(gana, v, cur)
    hloc[ix] = np.where(gana, H, hloc[ix])


def _suave5(np, A):
    """La media de cada texel con sus cuatro vecinos. Las columnas dan la vuelta (la
    longitud); las filas no: la de arriba y la de abajo se repiten (motor v100: antes
    daban la vuelta y una isla en el polo dejaba una linea de tierra en la otra punta
    del bloque)."""
    up = np.roll(A, 1, 0)
    up[0] = A[0]
    dn = np.roll(A, -1, 0)
    dn[-1] = A[-1]
    return (A + up + dn + np.roll(A, 1, 1) + np.roll(A, -1, 1)) / 5.0


def _capa_de(r):
    return 'dom' if r[0] == 'domo' else ('isla' if r[0] in ('isla', 'istmo') else 'rel')


def _caja_de(np, filas, cols):
    """(r0, r1, columnas) de un parche."""
    mk = np.zeros(TERRENO_W, dtype=bool)
    mk[cols] = True
    return int(filas[0]), int(filas[-1]) + 1, mk


def _juntar_cajas(np, cajas, margen=0):
    """Junta las cajas [(r0, r1, columnas)] que se tocan (a margen texels o menos):
    las que quedan no se tocan."""
    cajas = [(a, b, m.copy()) for a, b, m in cajas if b > a and m.any()]
    junta = True
    while junta:
        junta = False
        for i in range(len(cajas)):
            a0, a1, am = cajas[i]
            amd = _dilata_circ(np, am, margen) if margen else am
            for j in range(i + 1, len(cajas)):
                b0, b1, bm = cajas[j]
                if a0 - margen < b1 and b0 - margen < a1 and (amd & bm).any():
                    cajas[i] = (min(a0, b0), max(a1, b1), am | bm)
                    del cajas[j]
                    junta = True
                    break
            if junta:
                break
    return cajas


def _capas(np, rej, rasgos):
    """Motor v99: las tres capas del mapa (relieve, montes e islas; cada una, su
    altura y el alto del rasgo que gana), guardadas entre llamadas. Solo se borra
    la ventana de los rasgos que cambian (los que salen y los que entran) y se
    vuelven a pintar los que la tocan: una nota cambia unos pocos, no los 450.
    Motor v101: la ventana son las cajas de lo que cambia en cada capa (juntas
    solo si se tocan) y lo que se vuelve a pintar es solo lo que cae dentro de
    ellas. Deja en _TERRENO['capas_cajas'] las cajas tocadas ([(r0, r1,
    columnas)], 'todo' o []) y en _TERRENO['capas_cambian'] los rasgos que han
    cambiado. No se pueden modificar las matrices que devuelve."""
    clave = (GRID['lo'], GRID['hi'], TERRENO_W, TERRENO_H)
    cp = _TERRENO.get('capas')
    nuevos = set(rasgos)
    todo = False
    if cp is None or cp['clave'] != clave:
        cp = _TERRENO['capas'] = dict(clave=clave, rasgos=set(), parches={})
        for nm in ('rel', 'dom', 'isla'):
            cp[nm] = (np.zeros((TERRENO_H, TERRENO_W)), np.zeros((TERRENO_H, TERRENO_W)))
        todo = True
    cambian = cp['rasgos'] ^ nuevos
    tocadas = []
    if cambian:
        todo = todo or len(cambian) > 0.5 * len(nuevos) + 8
        por_capa = {}
        for r in rasgos:
            por_capa.setdefault(_capa_de(r), []).append(r)
        rangos = cp.setdefault('rangos', {})
        for nm in ('rel', 'dom', 'isla'):
            E, H = cp[nm]
            ch = [r for r in cambian if _capa_de(r) == nm]
            if not ch:
                continue
            if todo:
                E[:] = 0.0
                H[:] = 0.0
                for r in por_capa.get(nm, ()):
                    _sobre(np, E, H, _parche(np, rej, r))
                continue
            cajas = []
            for r in ch:
                pa = cp['parches'].get(r) or _parche(np, rej, r)
                if len(pa[0]):
                    cajas.append(_caja_de(np, pa[0], pa[1]))
            for r0, r1, fc in _juntar_cajas(np, cajas):
                tocadas.append((r0, r1, fc))
                E[r0:r1, fc] = 0.0
                H[r0:r1, fc] = 0.0
                for r in por_capa.get(nm, ()):  # y encima, lo que cae dentro de la caja
                    rg = rangos.get(r)
                    if rg is None:
                        pa = _parche(np, rej, r)
                        rg = rangos[r] = (int(pa[0][0]), int(pa[0][-1]) + 1) if len(pa[0]) else (0, 0)
                    if rg[1] <= r0 or rg[0] >= r1:
                        continue
                    pa = _parche(np, rej, r)
                    cm = fc[pa[1]]
                    if not cm.any():
                        continue
                    # las filas de la caja, seguidas; las columnas, si son seguidas, como vista (sin copiar)
                    a_, b_ = max(rg[0], r0) - rg[0], min(rg[1], r1) - rg[0]
                    i0 = int(cm.argmax())
                    i1 = len(cm) - int(cm[::-1].argmax())
                    h2 = np.ndim(pa[3]) == 2
                    if cm[i0:i1].all():
                        _sobre(np, E, H, (pa[0][a_:b_], pa[1][i0:i1], pa[2][a_:b_, i0:i1],
                                          pa[3][a_:b_, i0:i1] if h2 else pa[3]))
                    else:
                        sub = np.ix_(np.arange(a_, b_), np.flatnonzero(cm))
                        _sobre(np, E, H, (pa[0][a_:b_], pa[1][cm], pa[2][sub], pa[3][sub] if h2 else pa[3]))
        # la ventana de cada rasgo pintado, para borrarlo luego aunque se vacie la cache de parches
        if todo:
            cp['parches'] = dict((r, _parche(np, rej, r)[:2]) for r in nuevos)
        else:
            for r in cambian:
                if r in nuevos:
                    cp['parches'][r] = _parche(np, rej, r)[:2]
                else:
                    cp['parches'].pop(r, None)
        cp['rasgos'] = nuevos
        if len(rangos) > 4 * len(nuevos) + 64:
            cp['rangos'] = dict((r, v) for r, v in rangos.items() if r in nuevos)
    _TERRENO['capas_cajas'] = 'todo' if todo else tocadas
    _TERRENO['capas_cambian'] = cambian
    return cp['rel'], cp['dom'], cp['isla']


def terreno(W, cfg, cl=None):
    """El mapa de alturas de la naturaleza (se guarda: solo se rehace si cambian
    los rasgos o el suelo). dict(E, S: arrays TERRENO_H x TERRENO_W o None sin
    numpy, El: E como listas, centro: [E en el centro de cada celda], hmax,
    version, cordilleras, montes, ejes)."""
    sello = (id(W), _TERRENO.get('sello'), tuple(W['occ']))
    if _TERRENO.get('sello_t') == sello and _TERRENO.get('t') is not None:
        return _TERRENO['t']                # ya visto en este fotograma
    rasgos, res = rasgos_terreno(W, cfg, cl)
    S = suelos_fotograma(W, cfg)
    hib = _hibridos_clave(W, cfg, cl)
    clave = (GRID['lo'], GRID['hi'], tuple(rasgos), S, round(alto_hipso(cfg), 4), hib)
    t = _TERRENO.get('t')
    if t is not None and _TERRENO.get('clave') == clave:
        _TERRENO['sello_t'] = sello
        return t
    np = _np()
    if np is not None:
        rej = _rejilla(np)
        # motor v80: de quien es el relieve (los bocetos): 1 el del SEQ2 (conos y crestas),
        # 0 los montes boscosos del SEQ1 (domos)
        R = np.ones((TERRENO_H, TERRENO_W), dtype=np.float32)
        # motor v99: las capas (relieve, montes, islas) se guardan y solo se rehace lo que
        # cambia. Con el oceano hay unos 450 rasgos y volver a pintarlos todos a cada nota
        # costaba mas de 100 ms: el fotograma entero a 20 fps son 50.
        (Erel, Hrel), (Edom, Hdom), isl = _capas(np, rej, rasgos)
        Eis, His = isl if any(r[0] in ('isla', 'istmo') for r in rasgos) else (None, None)
        # motor v101: si solo cambian rasgos (el mismo reparto, el mismo alto y los mismos
        # hibridos), el mapa se rehace solo en las filas que tocan y un borde de suavizado
        prev = _TERRENO.get('clave')
        hay_vol = any(r[0] == 'volcan' for r in rasgos)
        cajas_hib = _hibridos_cajas(np, prev[5], hib) if prev is not None and prev[5] != hib else []
        if _TERRENO_VENTANA and t is not None and t.get('_np') and prev is not None and \
                prev[:2] == clave[:2] and prev[4] == clave[4] and cajas_hib is not None and \
                _TERRENO.get('capas_cajas') != 'todo' and t.get('_isl') == (Eis is not None) and \
                (t.get('L') is not None) == hay_vol:
            E, R, Lv, El, hib_t = _terreno_ventana(np, rej, t, rasgos, Erel, Hrel, Edom, Hdom, Eis, His,
                                                   cfg, hib, cajas_hib)
            return _terreno_cierre(W, cfg, rasgos, res, S, hib, clave, sello, np, rej, E, R, Lv, El, hib_t,
                                   Eis is not None)
        Lv = None
        r0, r1 = TERRENO_H, 0               # solo las filas con relieve (lo demas es 0)
        for r in rasgos:
            pa = _parche(np, rej, r)
            if len(pa[0]):
                r0, r1 = min(r0, int(pa[0][0])), max(r1, int(pa[0][-1]) + 1)
            if r[0] == 'volcan':
                if Lv is None:
                    Lv = np.zeros((TERRENO_H, TERRENO_W), dtype=np.float32)
                cache = _TERRENO.setdefault('parches', {})
                lv = cache.get(('lava', r[1], r[3]))
                if lv is None:
                    lv = cache[('lava', r[1], r[3])] = _lava(np, rej, r[1], r[3])
                ixl = np.ix_(lv[0], lv[1])
                Lv[ixl] = np.maximum(Lv[ixl], lv[2])
        E = np.zeros((TERRENO_H, TERRENO_W), dtype=np.float32)
        hib_t = None
        if r1 > r0:
            r0, r1 = max(0, r0 - 3), min(TERRENO_H, r1 + 3)
            Nz = rej['ruido'][r0:r1]
            er, hr, ed, hd = Erel[r0:r1], Hrel[r0:r1], Edom[r0:r1], Hdom[r0:r1]
            with np.errstate(divide='ignore', invalid='ignore'):
                fr = np.where(hr > 1e-9, er / np.maximum(hr, 1e-9), 0.0)
                fd = np.where(hd > 1e-9, ed / np.maximum(hd, 1e-9), 0.0)
            er = er * (1.0 - 0.45 * (1.0 - Nz) * (1.0 - fr * fr))      # crestas y valles en las laderas
            ed = ed * (1.0 - 0.15 * (1.0 - Nz) * (1.0 - fd * fd))
            Ez = np.maximum(er, ed)
            for _ in range(2):              # suavizado 3x3: la malla (un vertice por texel) sin dientes
                Ez = _suave5(np, Ez)
                er = _suave5(np, er)
                ed = _suave5(np, ed)
            if Eis is not None:             # motor v97: el relieve, encima de la isla
                ei = Eis[r0:r1]
                ei = _suave5(np, ei)
                # motor v98: el relieve y los montes no pasan de la costa de su isla (ocupaban la
                # celda entera: con el mundo lleno no quedaba mar)
                hi = His[r0:r1]
                with np.errstate(divide='ignore', invalid='ignore'):
                    mk = _smooth(np, 0.0, 1.0, np.where(hi > 1e-9, ei / np.maximum(hi, 1e-9), 0.0))
                Ez = Ez * mk + ei
                if Lv is not None:
                    Lv[r0:r1] = (Lv[r0:r1] * mk).astype(np.float32)
            E[r0:r1] = Ez
            R[r0:r1] = np.where(ed > er, 0.0, 1.0)      # motor v80: lo que gana tras suavizar
        if hib[0] or hib[1]:                # fase 11 v8: bancales y mesetas, en el mismo mapa
            hib_t = _hibridos_terreno(np, rej, E, cfg, hib)
            filas = [k for k in range(TERRENO_H) if hib_t['filas'][k]]
            r0, r1 = min([r0] + filas), max([r1] + [k + 1 for k in filas])
        cero = [0.0] * TERRENO_W
        El = [cero] * r0 + E[r0:r1].tolist() + [cero] * (TERRENO_H - max(r0, r1)) if r1 > r0 \
            else [cero] * TERRENO_H
        return _terreno_cierre(W, cfg, rasgos, res, S, hib, clave, sello, np, rej, E, R, Lv, El, hib_t,
                               Eis is not None)
    return _terreno_cierre(W, cfg, rasgos, res, S, hib, clave, sello, None, None, None, None, None, None, None,
                           False)


_TERRENO_VENTANA = True     # motor v101: el mapa por ventanas (las autopruebas lo comparan con el entero)


def _terreno_cierre(W, cfg, rasgos, res, S, hib, clave, sello, np, rej, E, R, Lv, El, hib_t, isl):
    """El dict del mapa de alturas (lo comun al mapa entero y al de ventanas)."""
    Sa = _suelo_mapa(np, rej, S) if np is not None else None
    t = dict(E=E, S=Sa, El=El, R=R, L=Lv if np is not None else None, centro=[0.0] * N, hmax=alto_hipso(cfg),
             version=_TERRENO.get('version', 0) + 1, rasgos=len(rasgos), **res)
    t['hib'] = hib_t if np is not None else None
    t['hibridos'] = dict(arrozales=dict((i, nb) for i, nb in hib[0]), mesetas=dict(hib[1]))
    t['_np'], t['_isl'] = np is not None, isl
    if El is not None:
        t['centro'] = [alto_en(t, NORMALS[c]) for c in range(N)]
    _TERRENO['clave'], _TERRENO['t'], _TERRENO['version'] = clave, t, t['version']
    _TERRENO['array'] = None
    _TERRENO['sello_t'] = sello
    return t


def _lava_de(np, rej, r):
    """La lava del volcan del rasgo r (se guarda con los parches)."""
    cache = _TERRENO.setdefault('parches', {})
    lv = cache.get(('lava', r[1], r[3]))
    if lv is None:
        lv = cache[('lava', r[1], r[3])] = _lava(np, rej, r[1], r[3])
    return lv


def _tramos_circ(np, mask):
    """Los tramos seguidos de columnas de mask (las columnas dan la vuelta):
    [(inicio, largo)]."""
    n = len(mask)
    if mask.all():
        return [(0, n)]
    if not mask.any():
        return []
    k = int(np.flatnonzero(~mask)[0])         # empezar en una columna vacia: ningun tramo se parte
    m2 = np.roll(mask, -k)
    d = np.diff(np.concatenate(([0], m2.astype(np.int8), [0])))
    ini, fin = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return [((int(s) + k) % n, int(e - s)) for s, e in zip(ini, fin)]


def _dilata_circ(np, mask, k):
    out = mask.copy()
    for d in range(1, k + 1):
        out |= np.roll(mask, d) | np.roll(mask, -d)
    return out


def _terreno_ventana(np, rej, t, rasgos, Erel, Hrel, Edom, Hdom, Eis, His, cfg, hib, cajas_hib):
    """Motor v101: el mapa de alturas rehecho solo en las cajas que tocan los
    rasgos que han cambiado (las de _capas, la lava de los volcanes que cambian y
    los hibridos que cambian) y un borde de suavizado; el resto se copia del mapa
    anterior. Da lo mismo que el mapa entero: cada texel del resultado depende de
    los de entrada a 2 texels o menos (dos pasadas de _suave5), asi que se calcula
    con 4 de margen y se guardan los de 2. Las columnas dan la vuelta. Devuelve
    (E, R, L, El, hibridos)."""
    cajas = list(_TERRENO.get('capas_cajas') or []) + list(cajas_hib)
    for r in _TERRENO.get('capas_cambian', ()):
        if r[0] == 'volcan':
            lv = _lava_de(np, rej, r)
            if len(lv[0]):
                cajas.append(_caja_de(np, lv[0], lv[1]))
    cajas = _juntar_cajas(np, cajas, 8)
    if not cajas:                           # solo el suelo ha cambiado: el mismo mapa
        return t['E'], t['R'], t['L'], t['El'], t['hib']
    E = t['E'].copy()
    R = t['R'].copy()
    Lv = t['L'].copy() if t['L'] is not None else None
    lava = [_lava_de(np, rej, r) for r in rasgos if r[0] == 'volcan'] if Lv is not None else []
    hb = None
    if hib[0] or hib[1]:
        hb = t['hib']
        if hb is None:
            hb = dict(h0=np.zeros_like(E), top=np.zeros_like(E), mesa=np.zeros_like(E))
        hb = dict(h0=hb['h0'].copy(), top=hb['top'].copy(), mesa=hb['mesa'].copy())
    El = list(t['El'])
    for a, b, cm in cajas:
        o0, o1 = max(0, a - 2), min(TERRENO_H, b + 2)
        c0, c1 = max(0, a - 4), min(TERRENO_H, b + 4)
        k0, k1 = o0 - c0, o1 - c0
        sale = _dilata_circ(np, cm, 2)      # las columnas que cambian
        if sale.sum() >= TERRENO_W - 8:
            sale[:] = True
        tramos = _tramos_circ(np, sale)
        for s, n in tramos:
            if n >= TERRENO_W:              # la vuelta entera: _suave5 ya da la vuelta
                idx_in, q0, q1 = np.arange(TERRENO_W), 0, TERRENO_W
            else:
                idx_in, q0, q1 = (s - 2 + np.arange(n + 4)) % TERRENO_W, 2, n + 2
            idx = idx_in[q0:q1]
            Nz = rej['ruido'][c0:c1][:, idx_in]
            er, hr = Erel[c0:c1][:, idx_in], Hrel[c0:c1][:, idx_in]
            ed, hd = Edom[c0:c1][:, idx_in], Hdom[c0:c1][:, idx_in]
            with np.errstate(divide='ignore', invalid='ignore'):
                fr = np.where(hr > 1e-9, er / np.maximum(hr, 1e-9), 0.0)
                fd = np.where(hd > 1e-9, ed / np.maximum(hd, 1e-9), 0.0)
            er = er * (1.0 - 0.45 * (1.0 - Nz) * (1.0 - fr * fr))
            ed = ed * (1.0 - 0.15 * (1.0 - Nz) * (1.0 - fd * fd))
            Ez = np.maximum(er, ed)
            for _ in range(2):
                Ez = _suave5(np, Ez)
                er = _suave5(np, er)
                ed = _suave5(np, ed)
            mk = None
            if Eis is not None:
                ei = _suave5(np, Eis[c0:c1][:, idx_in])
                hi = His[c0:c1][:, idx_in]
                with np.errstate(divide='ignore', invalid='ignore'):
                    mk = _smooth(np, 0.0, 1.0, np.where(hi > 1e-9, ei / np.maximum(hi, 1e-9), 0.0))
                Ez = Ez * mk + ei
            E[o0:o1, idx] = Ez[k0:k1, q0:q1]
            R[o0:o1, idx] = np.where(ed > er, 0.0, 1.0)[k0:k1, q0:q1]
            if Lv is not None:
                Lr = np.zeros((o1 - o0, len(idx)), dtype=np.float32)
                pos = np.full(TERRENO_W, -1)
                pos[idx] = np.arange(len(idx))
                for lv in lava:
                    sel = (lv[0] >= o0) & (lv[0] < o1)
                    cs = pos[lv[1]] >= 0
                    if not sel.any() or not cs.any():
                        continue
                    ixl = np.ix_(lv[0][sel] - o0, pos[lv[1][cs]])
                    Lr[ixl] = np.maximum(Lr[ixl], lv[2][np.ix_(sel, cs)])
                if mk is not None:
                    Lr = (Lr * mk[k0:k1, q0:q1]).astype(np.float32)
                Lv[o0:o1, idx] = Lr
        if hb is not None:                  # los hibridos, en esa caja
            _hibridos_filas(np, rej, E, cfg, hib, hb, o0, o1, sale)
        for r in range(o0, o1):
            fila = list(El[r])
            for s, n in tramos:
                e_ = s + n
                if e_ <= TERRENO_W:
                    fila[s:e_] = E[r, s:e_].tolist()
                else:
                    fila[s:] = E[r, s:].tolist()
                    fila[:e_ - TERRENO_W] = E[r, :e_ - TERRENO_W].tolist()
            El[r] = fila
    hib_t = None
    if hb is not None:
        filas = np.zeros(TERRENO_H, dtype=bool)
        for i, _ in list(hib[0]) + list(hib[1]):
            k = 0.8 if i in dict(hib[0]) else 0.75
            filas[_ventana(np, NORMALS[i], k * max(SIZE_EW[i], SIZE_NS[i]))[0]] = True
        hib_t = dict(h0=hb['h0'], top=hb['top'], mesa=hb['mesa'], filas=filas)
    return E, R, Lv, El, hib_t


def _hibridos_clave(W, cfg, cl):
    """(arrozales ((celda, bancales)...), mesetas ((celda, nivel)...), capitales, parametros)."""
    if cfg['nivel'] < 11 or tema_de(cfg) != 'naturaleza':
        return ((), (), (), ())
    hib = [i for i in range(N) if W['sp'][i] == HIB and W['occ'][i] > 0]
    if not hib:
        return ((), (), (), ())
    arroz = tuple((i, b) for i, b in ((i, bancales(W, cfg, i)) for i in hib) if b)
    mes = tuple((i, nv) for i, nv in ((i, niveles_meseta(W, cfg, i)) for i in hib) if nv)
    caps = ()
    if mes:
        cl = cl or clusters(W, cfg)
        caps = tuple((i, cl['capital'][cl['de'][i]] if cl['de'][i] >= 0 else i) for i, _ in mes)
    return arroz, mes, caps, (cfg['paso_terraza'], cfg['muro_terraza'], cfg['altura_meseta'],
                              cfg['limite_bosque'], round(limit(cfg), 5))


def _smooth(np, a, b, x):
    """smoothstep(a, b, x) (a > b: de bajada)."""
    u = np.clip((x - a) / (b - a if abs(b - a) > 1e-12 else 1e-12), 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def _hibridos_terreno(np, rej, E, cfg, hib):
    """Los hibridos de la naturaleza en el mapa de alturas E (lo cambia):
      ARROZAL  dentro de la banda aterrazada (de la base a bancales x Pasoterraza,
               sin pasar de Limitebosque) la altura se cuantiza:
               h' = D floor(h/D) + D smoothstep(1 - m, 1, fract(h/D))
               (D Pasoterraza, m Muroterraza): los bancales siguen las curvas de
               nivel reales del monte, onduladas por el ruido de crestas
      MESETA   el suelo sube Alturameseta por nivel con el borde vertical: cada
               nivel es la isolinea de la ocupacion del SEQ2 interpolada entre
               las celdas, y se contrae hacia la capital (x MESETA_K)
    Devuelve dict(h0 relieve sin aterrazar, top tope de la banda, mesa nivel de
    la meseta, filas con algo)."""
    arroz, mes, caps, _ = hib
    lim = limit(cfg)
    D = max(1e-4, cfg['paso_terraza'] * lim)
    m = cfg['muro_terraza']
    lb, _ = _limites_pisos(cfg)
    hmax = alto_hipso(cfg)
    h0 = np.zeros_like(E)
    top = np.zeros_like(E)
    mesa = np.zeros_like(E)
    filas = np.zeros(E.shape[0], dtype=bool)
    for i, nb in arroz:
        filas[_arrozal(np, rej, E, h0, top, i, nb, D, m, lb, hmax)] = True
    if mes:
        nivel = dict(mes)
        cap = dict(caps)
        alt = cfg['altura_meseta'] * lim
        for i, nv in mes:
            filas[_meseta(np, rej, mesa, i, nivel, cap)] = True
        E += (mesa * alt).astype(np.float32)
    return dict(h0=h0.astype(np.float32), top=top.astype(np.float32), mesa=mesa.astype(np.float32),
                filas=filas)


def _meseta(np, rej, mesa, i, nivel, cap, o0=0, o1=None, cols=None):
    """La meseta de la celda i en el mapa mesa (el maximo; lo cambia), solo en las
    filas o0-o1 y las columnas cols (motor v101). Devuelve las filas de su ventana."""
    f_, c_ = _ventana(np, NORMALS[i], 0.75 * max(SIZE_EW[i], SIZE_NS[i]))
    filas = f_
    if o1 is not None:
        f_ = f_[(f_ >= o0) & (f_ < o1)]
        if cols is not None:
            c_ = c_[cols[c_]]
        if not len(f_) or not len(c_):
            return filas
    c0 = cap.get(i, i)
    grupo = [x for x in nivel if cap.get(x, x) == c0]
    # cada nivel se contrae hacia la capital (la mas alta del grupo; a igualdad, la del cluster)
    c = max(grupo, key=lambda x: (nivel[x], x == c0, -x))
    otras = set(grupo)
    for x in grupo:
        otras.update(NEIGH[x])
    celdas = sorted(otras)
    Nc = np.array([NORMALS[x] for x in celdas])
    L = np.array([float(nivel.get(x, 0)) for x in celdas])
    tam = np.array([0.5 * (SIZE_EW[x] + SIZE_NS[x]) for x in celdas])
    R0 = max(float(np.linalg.norm(np.array(NORMALS[x]) - np.array(NORMALS[c]))) +
             0.5 * (SIZE_EW[x] + SIZE_NS[x]) * 0.5 for x in grupo)
    ix = np.ix_(f_, c_)
    Dd = rej['D'][ix]
    d2 = ((Dd[..., None, :] - Nc[None, None, :, :]) ** 2).sum(-1)
    w = np.exp(-d2 / (0.42 * tam[None, None, :]) ** 2)
    fld = (w * L[None, None, :]).sum(-1) / np.maximum(1e-9, w.sum(-1))
    dcap = np.linalg.norm(Dd - np.array(NORMALS[c]), axis=-1)
    sube = np.zeros(fld.shape)
    for k in range(1, int(max(L)) + 1):
        dentro = _smooth(np, k - 0.62, k - 0.5, fld)
        if k > 1:
            Rk = R0 * MESETA_K ** (k - 1)
            dentro = dentro * _smooth(np, Rk + 0.012, Rk, dcap)
        sube += dentro
    mesa[ix] = np.maximum(mesa[ix], sube)
    return filas


def _hibridos_cajas(np, prev, hib):
    """Motor v101: las cajas [(r0, r1, columnas)] que cambian los hibridos al pasar de
    prev a hib (los arrozales que cambian y las mesetas de los grupos que cambian,
    antes y despues). None si cambian sus parametros (el mapa entero)."""
    if prev[0] or prev[1]:
        if (hib[0] or hib[1]) and prev[3] != hib[3]:
            return None
    ap, an = dict(prev[0]), dict(hib[0])
    celdas = [(i, 0.8) for i in set(ap) | set(an) if ap.get(i) != an.get(i)]

    def grupos(h):
        cap = dict(h[2])
        g = {}
        for i, nv in h[1]:
            g.setdefault(cap.get(i, i), set()).add((i, nv))
        return g
    gp, gn = grupos(prev), grupos(hib)
    for k in set(gp) | set(gn):
        if gp.get(k) != gn.get(k):
            celdas += [(i, 0.75) for i, _ in gp.get(k, set()) | gn.get(k, set())]
    cajas = []
    for i, k in celdas:
        f_, c_ = _ventana(np, NORMALS[i], k * max(SIZE_EW[i], SIZE_NS[i]))
        if len(f_):
            mk = np.zeros(TERRENO_W, dtype=bool)
            mk[c_] = True
            cajas.append((int(f_[0]), int(f_[-1]) + 1, mk))
    return cajas


def _arrozal(np, rej, E, h0, top, i, nb, D, m, lb, hmax, o0=0, o1=None, cols=None):
    """Los bancales del arrozal de la celda i en E (lo cambia), solo en las filas
    o0-o1 y las columnas cols (motor v101: el mapa por ventanas). Devuelve las
    filas de su ventana."""
    f_, c_ = _ventana(np, NORMALS[i], 0.8 * max(SIZE_EW[i], SIZE_NS[i]))
    if o1 is not None:
        f_ = f_[(f_ >= o0) & (f_ < o1)]
        if cols is not None:
            c_ = c_[cols[c_]]
        if not len(f_) or not len(c_):
            return f_
    ix = np.ix_(f_, c_)
    dentro = rej['celda'][ix] == i
    h = E[ix].astype(np.float64)
    tope = D * min(nb, int(lb * hmax / D))
    banda = dentro & (h < tope)
    q = h / D
    fr = q - np.floor(q)
    hq = D * np.floor(q) + D * _smooth(np, 1.0 - m, 1.0, fr)
    E[ix] = np.where(banda, hq, h).astype(np.float32)
    h0[ix] = np.where(dentro, h, h0[ix])
    top[ix] = np.where(dentro, tope, top[ix])
    return f_


def _hibridos_filas(np, rej, E, cfg, hib, hb, o0, o1, cols):
    """Motor v101: los hibridos de hib en la caja (filas o0-o1, columnas cols) del
    mapa E, que se acaba de rehacer: h0, top y mesa (los de hb, que cambia) se
    ponen a cero en la caja y se vuelven a calcular en ella; los bancales del
    arrozal se cuantizan y la meseta se suma."""
    arroz, mes, caps, _ = hib
    lim = limit(cfg)
    D = max(1e-4, cfg['paso_terraza'] * lim)
    lb, _ = _limites_pisos(cfg)
    hmax = alto_hipso(cfg)
    h0, top, mesa = hb['h0'], hb['top'], hb['mesa']
    h0[o0:o1, cols] = 0.0
    top[o0:o1, cols] = 0.0
    mesa[o0:o1, cols] = 0.0
    for i, nb in arroz:
        _arrozal(np, rej, E, h0, top, i, nb, D, cfg['muro_terraza'], lb, hmax, o0, o1, cols)
    if mes:
        nivel, cap = dict(mes), dict(caps)
        for i, _ in mes:
            _meseta(np, rej, mesa, i, nivel, cap, o0, o1, cols)
        E[o0:o1, cols] += (mesa[o0:o1, cols] * (cfg['altura_meseta'] * lim)).astype(np.float32)



_CULTIVOS = {}


def cultivos(W, cfg, ter, por_celda, now, paso, cl=None):
    """La textura de los cultivos (Script TOP 'cultivos', TERRENO_H x TERRENO_W x 4):
    r el relieve sin aterrazar, g el tope de la banda aterrazada (0: sin bancales),
    b desde donde se inunda (Riego: los bancales del lado del rio, en cascada desde
    arriba, uno por paso; >= g: secos), a nivel de la meseta (0-3) + 10 si la
    cruza una acequia. Devuelve dict(array, inundados {celda: n}, parcelas {celda: n})."""
    np = _np()
    rg = riego(W, cfg, ter, por_celda, now, paso)
    hib = ter.get('hib')
    clave = (ter['version'], tuple(sorted(rg.items())), cfg.get('riego', 1))
    v = _CULTIVOS.get('v')
    if v is not None and v[0] == clave:
        return v[1]
    inund = dict((i, x[1]) for i, x in rg.items())
    out = dict(array=None, inundados=inund, parcelas={})
    if np is None or hib is None:
        _CULTIVOS['v'] = (clave, out)
        return out
    rej = _rejilla(np)
    a = np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)
    a[..., 0] = hib['h0']
    a[..., 1] = hib['top']
    a[..., 2] = hib['top']
    D = cfg['paso_terraza'] * limit(cfg)
    for i, (lado, k) in rg.items():
        f_, c_ = _ventana(np, NORMALS[i], 0.8 * max(SIZE_EW[i], SIZE_NS[i]))
        ix = np.ix_(f_, c_)
        dentro = (rej['celda'][ix] == i) & ((rej['D'][ix] - np.array(NORMALS[i])) @ np.array(lado) > 0.0)
        tope = a[..., 1][ix]
        a[..., 2][ix] = np.where(dentro, tope - k * D, a[..., 2][ix])
    a[..., 3] = hib['mesa']
    mes = ter.get('hibridos', {}).get('mesetas', {})
    if mes:                                     # la acequia: el rio cerca de la meseta
        for i in mes:
            if any(c in por_celda for c in [i] + list(NEIGH[i])):
                f_, c_ = _ventana(np, NORMALS[i], 0.75 * max(SIZE_EW[i], SIZE_NS[i]))
                ix = np.ix_(f_, c_)
                a[..., 3][ix] = np.where(a[..., 3][ix] > 0.5, a[..., 3][ix] + 10.0, a[..., 3][ix])
            m_ = (rej['celda'] == i) & (hib['mesa'] > 0.5)
            ys, xs = np.nonzero(m_)
            out['parcelas'][i] = len(set(zip((xs // PARCELA_TEX).tolist(), (ys // PARCELA_TEX).tolist())))
    out['array'] = a
    _CULTIVOS['v'] = (clave, out)
    return out


HOJAS_TOPE = 300000         # el presupuesto de hojas: si no caben, todo con tarjetas de racimo (Impostores)
_PRESUPUESTO = dict(lleno=False)
HOJAS_LIGERO = 100000       # con Ligero, el presupuesto baja
LIGERO_ARBOLES = 6          # con Ligero, arboles como mucho por celda de bosque
RUTA_HOJAS = 'SOP'          # las hojas van en la malla de cada ejemplar (Script SOP), no en POPs
# Motor v97 (Detalle): la tarjeta grafica lleva las hojas de verdad tambien desde el globo (antes,
# con Ligero, todo eran tarjetas de racimo salvo a ras de suelo) y el presupuesto sube: son
# triangulos en la GPU, no filas que calcule el motor.
HOJAS_DETALLE = 3000000
DETALLE_ARBOLES = 24        # con Detalle y Ligero, arboles como mucho por celda de bosque (v99: celdas el doble de anchas)


def presupuesto_hojas(cfg):
    if cfg.get('detalle', 1):
        return HOJAS_DETALLE
    return HOJAS_LIGERO if cfg.get('ligero', 1) else HOJAS_TOPE


def cerca_de(W, cfg, i):
    """La celda i se dibuja con las hojas de verdad (no con tarjetas de racimo): siempre
    con Detalle; sin el, con la camara de superficie (Ligero) o por Lodnat."""
    if cfg.get('detalle', 1):
        return True
    return bool(cfg.get('superficie')) if cfg.get('ligero', 1) else lod_cerca(W, cfg, i)


PARCELA_TEX = 16            # una parcela de la meseta: 16 x 16 texeles del mapa (los setos, en el shader)


def _miles(n):
    return '%dk' % int(round(n / 1000.0)) if n >= 1000 else str(int(n))


def cultivos_array():
    """El array del Script TOP 'cultivos' (el ultimo calculado) o uno vacio."""
    np = _np()
    if np is None:
        return None
    v = _CULTIVOS.get('v')
    if v is not None and v[1]['array'] is not None:
        return v[1]['array']
    return np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)


def _suelo_mapa(np, rej, S):
    """El radio del suelo de cada texel, erosionado 3x3: la malla hundida nunca
    asoma de una loseta (se guarda por suelos)."""
    v = _TERRENO.get('suelo_mapa')
    if v is not None and v[0] == S:
        return v[1]
    Sc = np.array(S, dtype=np.float32)[rej['celda']]
    Sa = Sc.copy()
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr or dc:
                Sa = np.minimum(Sa, np.roll(np.roll(Sc, dr, axis=0), dc, axis=1))
    _TERRENO['suelo_mapa'] = (S, Sa)
    return Sa


def suelos_fotograma(W, cfg):
    """(suelo de cada celda, redondeado), una vez por fotograma: el terreno,
    los rios y el tejido lo miran varias veces."""
    sello = (id(W), _TERRENO.get('sello'), len(W['cols']))
    v = _TERRENO.get('suelos')
    if v is not None and v[0] == sello:
        return v[1]
    S = tuple(round(suelo(W, cfg, c), 4) for c in range(N))
    _TERRENO['suelos'] = (sello, S)
    return S


def alto_en(t, d):
    """Relieve (sobre el suelo local) en la direccion unitaria d: bilineal en
    el mapa, como lo lee el shader."""
    El = t.get('El')
    if not El:
        return 0.0
    x = (math.atan2(d[2], d[0]) / (2 * math.pi) + 0.5) * TERRENO_W - 0.5
    y = (math.asin(max(-1.0, min(1.0, d[1]))) / math.pi + 0.5) * TERRENO_H - 0.5
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    fx, fy = x - x0, y - y0
    y0c, y1c = max(0, min(TERRENO_H - 1, y0)), max(0, min(TERRENO_H - 1, y0 + 1))
    x0w, x1w = x0 % TERRENO_W, (x0 + 1) % TERRENO_W
    a = El[y0c][x0w] + (El[y0c][x1w] - El[y0c][x0w]) * fx
    b = El[y1c][x0w] + (El[y1c][x1w] - El[y1c][x0w]) * fx
    return a + (b - a) * fy


def alturas_array():
    """El mapa para el Script TOP 'alturas' (TERRENO_H x TERRENO_W x 4, float32):
    r el relieve, g el radio del suelo (erosionado), b de quien es el relieve (motor
    v80: 1 el SEQ2, 0 los montes boscosos del SEQ1; para los bocetos), a la lava de los
    volcanes (motor v97: 1 el crater, 0,6 las coladas; hasta la v96, 1 fijo). None sin numpy."""
    t = _TERRENO.get('t')
    np = _np()
    if t is None or np is None or t['E'] is None:
        if np is None:
            return None
        a = np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)
        a[..., 1] = DEFAULT_CFG['core_radius']
        return a
    a = _TERRENO.get('array')
    if a is None:
        a = np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)
        a[..., 0] = t['E']
        a[..., 1] = t['S']
        a[..., 2] = t['R'] if t.get('R') is not None else 1.0
        if t.get('L') is not None:
            a[..., 3] = t['L']
        _TERRENO['array'] = a
    return a


def suelo_en(W, cfg, t, d, c):
    """Radio del terreno en la direccion d de la celda c: su suelo mas el relieve."""
    return suelo(W, cfg, c) + alto_en(t, d)


def lod_cerca(W, cfg, i):
    """Cerca: la camara de superficie, o la celda mide en pantalla Lodnat px o
    mas con la camara de globo (el planeta ocupa Encuadre del alto)."""
    if cfg.get('superficie'):
        return True
    R = top_radius(W, cfg) + RETICULA_SOBRE_DEF
    px = ENCUADRE_DEF * 720.0 / (2.0 * R)
    return min(SIZE_EW[i], SIZE_NS[i]) * base_radius(W, cfg, i) * px >= cfg['lod_nat']


_COL_NAT = {}


def color_natural(cfg, h, rug, familia='dosel', k=0.3):
    """Albedo de la naturaleza: el piso de su altura, un poco acercado al
    material de la velocidad (fase 12). Sin concha ni tinte del secuenciador."""
    clave = (int(max(0.0, min(1.0, h)) * 511.0 + 0.5), round(rug, 3), familia, k, cfg['limite_bosque'],
             cfg['limite_nieve'], cfg['rug_min'], cfg['rug_max'])
    v = _COL_NAT.get(clave)
    if v is None:
        if len(_COL_NAT) > 20000:
            _COL_NAT.clear()
        v = _COL_NAT[clave] = _color_natural(cfg, h, rug, familia, k)
    return v


def _color_natural(cfg, h, rug, familia, k):
    col = color_piso(cfg, h)
    m = MATERIAL.get(familia)
    if m is None or k <= 0:
        return col
    t = (rug - cfg['rug_min']) / max(1e-6, cfg['rug_max'] - cfg['rug_min'])
    return _mix(col, _mix(m[0], m[1], max(0.0, min(1.0, t))), k)


def _lejos_del_rio(cauce, d, r):
    """True si la direccion d (con radio r, en rad) no pisa ningun rio de la celda."""
    for q, w in cauce:
        dd = 1.0 - _dot(q, d)
        lim = (0.5 * w + r)
        if dd < 0.5 * lim * lim:
            return False
    return True


_SITIOS = {}

# --- que planta le toca a cada celda (fase 11 v8) ------------------------------------
# Con Biomas, la latitud elige la familia (los polos, do1 y do8, frio; el centro
# del registro, calido) y la semilla del motor (velocidad fundadora y celda, por
# el mapa logistico) elige dentro de ella: la misma historia, la misma planta. El
# piso montano fuerza la conifera; el rio de la fase 13 (en la celda o en una
# vecina), el sauce en lo templado.
BIOMAS = ['frio', 'templado', 'calido']
BIOMA_PLANTAS = dict(frio=(['graminea', 'enebro'], ['conifera', 'abedul', 'araucaria']),
                     templado=(['retama', 'brezo', 'junco'], ['frondosa', 'pagoda', 'cipres', 'olivo']),
                     calido=(['helecho', 'palmito', 'agave'],
                             ['parasol', 'drago', 'palmera', 'baobab', 'bambu', 'cardon']))
# motor v97: con Oceano, la celda de costa (alguna vecina es mar) suma las plantas de la orilla
BIOMA_COSTA = dict(frio=([], []), templado=(['junco'], []), calido=([], ['palmera', 'mangle']))
ORILLA_PLANTA = 0.022                       # con Oceano, nada crece por debajo de esta altura (la playa)
ANFIBIAS = ('mangle', 'junco')              # salvo el mangle y el junco, que pisan el agua
BIOMA_FRIO, BIOMA_CALIDO = 0.6, 0.25        # latitud relativa (0 ecuador, 1 polo)
MONTANO = 0.35                              # el piso montano (v5): de aqui a Limitebosque, conifera
SOTOBOSQUE_K = 0.6                          # el matorral al pie del arbol joven
MATORRAL_K = 0.45                           # el matorral, de la altura de la formacion
MESETA_K = 0.55                             # cada nivel de la meseta, 0,55 del de abajo hacia la capital
COPA_MIN = 0.25                             # la copa que cuenta, como poco, al repartir el bosque (x el alto)
EMERGE = (1.3, 1.6)                         # el emergente sobresale del dosel
FRUTAL_K = 0.55                             # los frutales de la meseta, de la altura de la formacion


def bioma_de(i):
    lat = abs(latitud(i)) / 90.0
    return 'frio' if lat >= BIOMA_FRIO else ('calido' if lat < BIOMA_CALIDO else 'templado')


def planta_de(W, cfg, i, arbol=True, hg=0.0, rio=False, k=0):
    """El modelo de la planta k de la celda i (k 0: la principal)."""
    xs = logistica(semilla_caos(W['vel'][i], i + 97 * k), cfg['caos'], 2)
    if not cfg.get('biomas', 1):
        lista = ARBOLES if arbol else MATORRALES
    else:
        b = bioma_de(i)
        lista = BIOMA_PLANTAS[b][1 if arbol else 0]
        if cfg.get('oceano') and any(W['occ'][j] <= 0 for j in NEIGH[i]):
            lista = BIOMA_COSTA[b][1 if arbol else 0] + lista
        if arbol:
            lb, _ = _limites_pisos(cfg)
            if MONTANO <= hg < lb:
                lista = ['conifera']
            elif b == 'templado' and rio:
                lista = ['sauce']
    return lista[min(len(lista) - 1, int(xs[0] * len(lista)))]


def otra_planta(cfg, i, mo):
    """El otro arbol del mismo bioma (la mezcla del bosque); None si no hay."""
    lista = ARBOLES
    if cfg.get('biomas', 1):
        lista = next((v[1] for v in BIOMA_PLANTAS.values() if mo in v[1]), BIOMA_PLANTAS[bioma_de(i)][1])
    otros = [x for x in lista if x != mo]
    return otros[int(_hash01(i, 77) * len(otros))] if otros else None


# --- los hibridos: mesetas construidas -----------------------------------------------
# La piel cuenta las notas que la especie colonizadora deja en cada celda hibrida
# (el estado del motor solo guarda las dos trazas, la fundadora y la ocupacion
# total). La cuenta vive aqui, fuera de W: se rehace si la celda renace.
_COLONAS = {}
_MUROS = []                 # fase 14: los muros que caen como pedregal: [t, celda]


def _contar_nota(W, i, s):
    """Una nota de la especie s en la celda i ya ocupada (las presiones del
    desborde no tallan bancales: no son notas en la celda)."""
    if not 0 <= i < N or W['occ'][i] <= 0:
        return
    e = _COLONAS.get(i)
    if e is None or e['t'] != W['t_nac'][i] or e['own'] != W['own'][i]:
        e = _COLONAS[i] = dict(t=W['t_nac'][i], own=W['own'][i], n={GEO: 0, ARQ: 0})
    e['n'][s] = e['n'].get(s, 0) + 1


def notas_colonas(W, i):
    """Notas de la especie colonizadora en la celda hibrida i (0 si no lo es).
    Sin cuenta (el motor se recargo, un mundo hecho a mano o una celda que se
    hizo hibrida por la presion de un desborde), una."""
    if W['sp'][i] != HIB or W['occ'][i] <= 0:
        return 0
    e = _COLONAS.get(i)
    otra = ARQ if W['own'][i] == GEO else GEO
    if e is None or e['t'] != W['t_nac'][i] or e['own'] != W['own'][i]:
        return 1
    return e['n'].get(otra, 0)


def _quitar_colona(W, i, now):
    """Un golpe en una celda hibrida quita el bancal mas alto (o el nivel de
    arriba de la meseta): en orden inverso a la promocion."""
    if W['sp'][i] != HIB:
        return
    n = notas_colonas(W, i)
    e = _COLONAS.get(i)
    otra = ARQ if W['own'][i] == GEO else GEO
    if e is None or e['t'] != W['t_nac'][i] or e['own'] != W['own'][i]:
        e = _COLONAS[i] = dict(t=W['t_nac'][i], own=W['own'][i], n={GEO: 0, ARQ: 0})
    e['n'][otra] = max(0, n - 1)
    _MUROS.append([now if now is not None else 0.0, i])
    del _MUROS[:-16]


def bancales(W, cfg, i):
    """Bancales del arrozal de la celda i (relieve colonizado por la vegetacion)."""
    if W['own'][i] != ARQ or W['sp'][i] != HIB:
        return 0
    return min(int(cfg['max_terrazas']), int(round(cfg['terrazas_por_nota'] * notas_colonas(W, i))))


def niveles_meseta(W, cfg, i):
    """Niveles de la meseta-jardin de la celda i (vegetacion colonizada por el relieve)."""
    if W['own'][i] != GEO or W['sp'][i] != HIB:
        return 0
    return min(int(cfg['max_niveles']), notas_colonas(W, i))


_RIEGO = {}


def riego(W, cfg, ter, cauces_, now, paso):
    """{celda: (lado, inundados)} de los arrozales con un rio en la celda o en
    una vecina: los bancales de ese lado se inundan en cascada desde arriba,
    uno por paso desde que llego el agua."""
    out = {}
    if not cfg.get('riego', 1) or cfg['nivel'] < 13:
        _RIEGO.clear()
        return out
    for i in range(N):
        nb = bancales(W, cfg, i)
        if nb <= 0:
            continue
        n = NORMALS[i]
        lado = (0.0, 0.0, 0.0)
        for c in [i] + list(NEIGH[i]):
            for q, _ in cauces_.get(c, ()):
                lado = _add(lado, _add(q, n, -1.0))
        if _len(lado) < 1e-9:
            _RIEGO.pop(i, None)
            continue
        t0 = _RIEGO.setdefault(i, now)
        out[i] = (_norm(lado), min(nb, 1 + int(max(0.0, now - t0) / max(1e-6, paso))))
    return out


# --- el bosque: disco de Poisson con timidez de copa -----------------------------------
_POISSON = {}


def _candidatos(i, cw, cl, k, semilla):
    """Puntos de prueba (x, z) de la celda i, en orden fijo, solo los que caen en
    ella (su celda mas cercana) y dentro de su elipse (k: la parte de la celda)."""
    clave = ('cand', GRID['lo'], GRID['hi'], i, round(cw, 5), round(cl, 5), round(k, 2), semilla)
    v = _POISSON.get(clave)
    if v is not None:
        return v
    import random
    rng = random.Random(1009 * i + 7 * semilla + 3)
    n = NORMALS[i]
    e, t = tangents(n)
    vecinas = [NORMALS[j] for j in NEIGH[i]]
    out = []
    for _ in range(900):
        x, z = rng.uniform(-0.75, 0.75) * cw * k, rng.uniform(-0.75, 0.75) * cl * k
        if math.hypot(x / (0.5 * cw * k + 1e-9), z / (0.5 * cl * k + 1e-9)) > 1.25:
            continue
        q = _norm(_add(_add(n, e, x / (cw / max(1e-6, SIZE_EW[i]))), t, z / (cl / max(1e-6, SIZE_NS[i]))))
        dn = _dot(q, n)
        if any(_dot(q, v_) > dn for v_ in vecinas):
            continue
        out.append((x, z))
    _POISSON[clave] = out
    return out


def _poisson(i, cw, cl, r, k=1.0, semilla=0):
    """Puntos (x, z) de la celda i (en su plano tangente) separados al menos r,
    solo los que caen en la celda (la mas cercana): los bosques de celdas
    vecinas encajan sin pisarse. k: la parte de la celda (las etapas del dosel).
    Disco de Poisson por eliminacion sobre candidatos fijos, con una rejilla."""
    clave = (GRID['lo'], GRID['hi'], i, round(cw, 5), round(cl, 5), round(r, 4), round(k, 2), semilla)
    v = _POISSON.get(clave)
    if v is not None:
        return v
    r2 = r * r
    rejilla = {}
    pts = []
    for x, z in _candidatos(i, cw, cl, k, semilla):
        gx, gz = int(math.floor(x / r)), int(math.floor(z / r))
        if any((x - a) ** 2 + (z - b) ** 2 < r2 for dx in (-1, 0, 1) for dz in (-1, 0, 1)
               for a, b in rejilla.get((gx + dx, gz + dz), ())):
            continue
        rejilla.setdefault((gx, gz), []).append((x, z))
        pts.append((x, z))
    pts.sort(key=lambda p: (round(p[0], 6), round(p[1], 6)))
    if len(_POISSON) > 4000:
        _POISSON.clear()
    _POISSON[clave] = pts
    return pts


def _marco_rejilla(i, cw, cl, sep, tresbolillo=True):
    """Los frutales de la meseta en marco real o al tresbolillo, dentro de la celda."""
    n = NORMALS[i]
    e, t = tangents(n)
    vecinas = list(NEIGH[i])
    fila = sep * (math.sqrt(3.0) / 2.0 if tresbolillo else 1.0)
    out = []
    nz = int(0.7 * cl / max(1e-6, fila)) + 1
    nx = int(0.7 * cw / max(1e-6, sep)) + 1
    for a in range(-nz, nz + 1):
        for b in range(-nx, nx + 1):
            x = (b + (0.5 if tresbolillo and a % 2 else 0.0)) * sep
            z = a * fila
            q = _norm(_add(_add(n, e, x / (cw / max(1e-6, SIZE_EW[i]))), t, z / (cl / max(1e-6, SIZE_NS[i]))))
            if any(_dot(q, NORMALS[j]) > _dot(q, n) - 1e-4 for j in vecinas):
                continue
            out.append((x, z))
    return out


def inclinacion_luz(W, cfg, i):
    """(grados, rumbo): el ejemplar se inclina hasta Inclinacion hacia el lado
    con menos vecinas ocupadas, como si buscara la luz."""
    n = normal_i(i)
    s = (0.0, 0.0, 0.0)
    vac = 0
    for j in NEIGH[i]:
        if W['occ'][j] <= 0:
            s = _add(s, _hacia(n, n, normal_i(j)))
            vac += 1
    if vac == 0 or _len(s) < 1e-6:
        return 0.0, 0.0
    k = min(1.0, _len(s) / max(1.0, 0.5 * len(NEIGH[i])))
    return round(cfg.get('inclinacion', 8.0) * k * 2.0) / 2.0, round(_rumbo(n, _norm(s)))


def piel_natural(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out, now, paso):
    """La celda i con el tema naturaleza (fase 11 v8): la vegetacion es una
    sucesion de ejemplares de la biblioteca (matorral pionero, arbol joven,
    adulto, arboleda, bosque y monte), con el bioma de su latitud; los hibridos
    son mesetas construidas en el mapa de alturas (arrozal y meseta-jardin).
    Devuelve el numero de ejemplares."""
    cl, ter = ctx['cl'], ctx['ter']
    own = W['own'][i]
    esp = especie_de('naturaleza', own)
    n = normal_i(i)
    e, _, t, _ = _marco(i)
    S = ctx['bases'][i]
    p0 = _mul(n, S)
    cw, cl_ = _cell_sizes(S, i)
    hmax = ter['hmax']
    o = W['occ'][i]
    est = estado_idx(cfg, o)
    k_ = cl['de'][i]
    ncl = len(cl['celdas'][k_]) if k_ >= 0 else 1
    cf, cc = cadenas_de(cfg, 'naturaleza', esp)
    sway, rumbo_sw = ctx['sway'](i)
    cauce = ctx['cauces'].get(i, ())
    lb, _ = _limites_pisos(cfg)
    lejos = cfg.get('impostores', 1) and not ctx['cerca'](i)
    esc_sat = cfg['sat_size'] if sat else 1.0
    nv = W['vel'][i]
    res = ctx['res']
    cuenta = [0]
    rio = ctx['rio_cerca'](i)

    def pintar(col):
        if fl > 0:                          # destello del nacimiento (no es un tinte)
            col = _mix(col, (1.0, 1.0, 1.0), 0.6 * fl)
        if sat:
            col = _tint(col, 0.9)
        if i in arde:                       # fase 14: brasa a saltos y carbon
            col = _quemar(col, arde[i], int(now / paso * FOTOS_PASO + i) % 2)
        return col

    def sitio(x, z):
        clave = (i, round(x, 5), round(z, 5), S, ter['version'])
        v = _SITIOS.get(clave)
        if v is None:                       # el sitio y su suelo, una vez por mapa
            pt = _add(_add(p0, e, x), t, z)
            d = _norm(pt)
            if len(_SITIOS) > 40000:
                _SITIOS.clear()
            v = _SITIOS[clave] = (pt, d, alto_en(ter, d))
        return v

    def plantar(modelo, deriv, x, z, h, giro=0.0, incl=0.0, rumbo=0.0, var=None, recto=False):
        """Un ejemplar de la biblioteca en (x, z) de la celda, sobre el terreno,
        de alto h. Sin plantas sobre el limite del bosque ni sobre un rio; la
        copa no tapa el rio que pasa al lado (fase 13 v3)."""
        pt, d, E = sitio(x, z)
        hg = E / hmax
        if hg > lb:
            return None
        if cfg.get('oceano') and E < (0.004 if modelo in ANFIBIAS else ORILLA_PLANTA):
            return None                     # motor v97: en el mar no crece nada
        if cauce and not _lejos_del_rio(cauce, d, 0.06 * min(cw, cl_) / max(1e-6, S)):
            return None
        nvar = variantes(cfg)
        var = int(_hash01(i, int(1000 * x), int(1000 * z), 11) * nvar) if var is None else var % nvar
        ej = ejemplar(cfg, modelo, var, deriv)
        h *= kb
        anch = 1.0 if recto else max(0.7, min(1.4, ancho))      # el vigor: tronco y alcance de copa
        rmax = 0.62 * min(cw, cl_) if modelo in ARBOLES else 0.45 * min(cw, cl_)
        if cauce:
            rmax = min(rmax, max(0.10 * min(cw, cl_), min(
                math.sqrt(max(0.0, 2.0 * (1.0 - _dot(q_, d)))) * S - 0.5 * w_ * S - 0.03 for q_, w_ in cauce)))
        r_ej = max(1e-6, ej['radio'] * anch)
        if h * r_ej > rmax and not recto:
            h = rmax / r_ej
        pb = _mul(d, _len(pt) + E)
        g = round(giro) % 360
        if cfg.get('cuantizar30', 0):
            g = 30 * int(g // 30)
        fr = _marco(i, float(g), incl + sway, rumbo if incl > 0 else rumbo_sw)
        ctx['mc'] = (float(g), incl, rumbo, recto)     # para la memoria: balanceo y vigor, al copiar la fila
        # motor v97: cada planta, con su verde (el piso de su altura acercado a su tono)
        col = pintar(_mix(color_natural(cfg, hg, rug), TONO_PLANTA.get(modelo, (0.15, 0.36, 0.13)), TONO_K))
        emit(nombre_ejemplar(modelo, var, deriv, lejos), pulido, pb, fr,
             (h * anch * esc_sat, h, h * anch * esc_sat), col, rug)
        cuenta[0] += 1
        res['hojas'] += len(ej['racimos']) if lejos else len(ej['hojas'])     # lejos: una tarjeta por racimo
        res['todas'] += len(ej['hojas'])
        res['ejemplares'] += 1
        return h * ej['copa'] * anch

    if esp != 'vegetacion':                         # relieve: el cono esta en el mapa
        if est <= 2:                                # columnas de basalto en las laderas bajas
            xs = logistica(semilla_caos(nv, i + 300), 3.91, 15)
            mo = (modelos_de(cfg, 'naturaleza', esp, 'semilla') or ['rel_columna'])[0]
            for q in range(5):
                a, b, c_ = xs[3 * q:3 * q + 3]
                g, r_ = 2 * math.pi * (q + a) / 5.0, 0.30 + 0.12 * b
                x, z = math.cos(g) * r_ * cw * esc_sat, math.sin(g) * r_ * cl_ * esc_sat
                d = _norm(_add(_add(n, e, x / S), t, z / S))
                E = alto_en(ter, d)
                hh = vh * (0.22 + 0.16 * c_) * kb
                w_ = 0.13 * min(cw, cl_) * esc_sat
                col = material_tema(cfg, _mix(color_piso(cfg, E / hmax), COL_BASALTO_PIE, 0.55), 'mineral', rug)
                emit(mo, pulido, _add(_add(_add(p0, e, x), t, z), n, E - 0.25 * hh), _marco(i, 60.0 * q),
                     (w_ / ANCHO.get(mo, 1.0), hh, w_ / ANCHO.get(mo, 1.0)), pintar(col), rug)
        _pedregal(W, cfg, i, p0, n, cw, cl_, vh, rug, emit, now, paso)
        return cuenta[0]

    # ---------------------------------------------------------------- vegetacion
    hg0 = ter['centro'][i] / hmax
    arbol_mo = planta_de(W, cfg, i, True, hg0, rio)
    mata_mo = planta_de(W, cfg, i, False)
    if k_ >= 0:                                     # el bosque del cluster: el modelo de la capital
        cap = cl['capital'][k_]
        if cap != i and W['own'][cap] == GEO:
            arbol_mo = planta_de(W, cfg, cap, True, ter['centro'][cap] / hmax, ctx['rio_cerca'](cap))
    caos = o <= int(cfg['max_caos_nat'])
    xs = logistica(semilla_caos(nv, i), cfg['caos'], 24)
    if caos:                                        # el caos elige variante, giro y escala
        var0, giro0, esc0 = int(xs[0] * 64), 360.0 * xs[1], 0.9 + 0.2 * xs[2]
    else:
        var0, giro0, esc0 = int(_hash01(i, 5) * 64), 360.0 * _hash01(i, 6), 1.0
    incl0, rumbo0 = inclinacion_luz(W, cfg, i)
    deriv_full = DERIVACIONES
    h_ref = height_for(cfg, o) * esc_sat
    meseta = niveles_meseta(W, cfg, i)
    if sat:                                         # satelite: matorral o arbol joven
        if o <= 1:
            plantar(mata_mo, 1, 0.0, 0.0, vh * MATORRAL_K * 1.4, giro0, incl0, rumbo0, var0)
        else:
            plantar(arbol_mo, 2, 0.0, 0.0, vh * 0.8, giro0, incl0, rumbo0, var0)
    elif meseta:                                    # meseta-jardin: la vegetacion se ordena
        ej = ejemplar(cfg, arbol_mo, 0, deriv_full)
        h = vh * FRUTAL_K
        sep = max(2.0 * h_ref * FRUTAL_K * ej['copa'] * 1.05, 0.16 * min(cw, cl_))
        for q, (x, z) in enumerate(_marco_rejilla(i, cw, cl_, sep, int(cfg.get('marco', 1)) == 1)):
            if plantar(arbol_mo, deriv_full, x, z, h * (0.95 + 0.1 * _hash01(i, q, 31)), 0.0, 0.0, 0.0,
                       var0, recto=True):
                res['frutales'][i] = res['frutales'].get(i, 0) + 1
    elif est >= 3 or (k_ >= 0 and ncl >= DOSEL_MIN):    # bosque de ejemplares reales
        kp = 1.0
        if k_ >= 0 and 'puentes' in cf:             # el bosque llena la celda con la etapa 'puentes'
            kp = avance_etapa(W, i, 'et_f', cf.index('puentes') + 1, now, paso)
        ej = ejemplar(cfg, arbol_mo, 0, deriv_full)
        h = vh * esc0
        # el disco se mide con la altura de la ocupacion, no con la visible: el latido
        # y el stop-motion no mueven los arboles de sitio
        # motor v97: los arboles estrechos (cipres, cardon, abedul) no se apinan: COPA_MIN
        r = max(0.08 * min(cw, cl_), h_ref * esc0 * max(ej['copa'], COPA_MIN) * (1.0 + cfg['timidez']))
        otra = otra_planta(cfg, i, arbol_mo)
        rq = math.exp(round(math.log(r / S) / 0.04) * 0.04)          # a saltos del 4 %: el disco se guarda
        pts = _poisson(i, cw / S, cl_ / S, rq, round(0.75 + 0.25 * kp, 1), int(cfg.get('variantes', 4)))
        tope_a = DETALLE_ARBOLES if cfg.get('detalle', 1) else LIGERO_ARBOLES
        if cfg.get('ligero', 1) and len(pts) > tope_a:     # Ligero: 6 del disco (siempre los mismos); Detalle: 10
            pts = sorted(pts, key=lambda p: _hash01(i, int(1e4 * p[0]), int(1e4 * p[1]), 47))[:tope_a]
        for q, (x, z) in enumerate((x * S, z * S) for x, z in pts):     # en unidades de la celda: no se rehace al crecer
            u = _hash01(i, q, 41)
            mo = otra if otra and _hash01(i, q, 42) < cfg['mezcla'] else arbol_mo
            hh = h * (0.82 + 0.22 * u)
            if _hash01(i, q, 43) < cfg['emergentes']:
                hh = h * (EMERGE[0] + (EMERGE[1] - EMERGE[0]) * _hash01(i, q, 44))
                res['emergentes'] += 1
            plantar(mo, deriv_full, x, z, hh, 360.0 * _hash01(i, q, 45), incl0 * 0.5, rumbo0, var0 + q)
        if cfg.get('orla', 1):                      # la orla: matorral en el borde del bosque
            for j in NEIGH[i]:
                if W['occ'][j] > 0 and W['own'][j] == GEO:
                    continue
                dj = _hacia(n, n, normal_i(j))
                bx, bz = _dot(dj, e), _dot(dj, t)
                for s in ((0,) if cfg.get('ligero', 1) else (-1, 1)):
                    x = 0.40 * cw * bx - 0.18 * s * cw * bz
                    z = 0.40 * cl_ * bz + 0.18 * s * cl_ * bx
                    plantar(mata_mo, 1, x, z, vh * MATORRAL_K * 0.9, 120.0 * s + giro0, 0.0, 0.0, var0 + s)
    elif est == 2:                                  # arboleda: ejemplares desiguales y matorral entre ellos
        nn = min(7, 3 + 2 * (o - int(cfg['th_branch'])) + int(2 * xs[3]))
        pts = [(0.0, 0.0)]
        ej = ejemplar(cfg, arbol_mo, 0, deriv_full)
        rr = 0.55 * h_ref * ej['copa']
        for q in range(60):
            if len(pts) >= nn:
                break
            a_, b_ = (xs[4 + q % 18], xs[5 + (q * 7) % 18]) if caos else (_hash01(i, q, 51), _hash01(i, q, 52))
            g_ = 2 * math.pi * ((a_ + 0.618 * q) % 1.0)
            r_ = 0.18 + 0.24 * ((b_ + 0.382 * q) % 1.0)
            x, z = math.cos(g_) * r_ * cw, math.sin(g_) * r_ * cl_
            if all((x - a) ** 2 + (z - b) ** 2 >= rr * rr for a, b in pts):
                pts.append((x, z))
        for q, (x, z) in enumerate(pts):
            esc = 1.0 if q == 0 else 0.55 + 0.4 * _hash01(i, q, 53)
            plantar(arbol_mo, deriv_full, x, z, vh * esc * esc0, giro0 + 97.0 * q, incl0, rumbo0, var0 + q)
        for q in range(min(len(pts) - 1, 2) if cfg.get('ligero', 1) else len(pts) - 1):    # matorral entre ellos
            (x0, z0), (x1, z1) = pts[q], pts[q + 1]
            plantar(mata_mo, 1, 0.5 * (x0 + x1), 0.5 * (z0 + z1), vh * MATORRAL_K * 0.8, 53.0 * q, 0.0, 0.0,
                    var0 + q)
    elif k_ >= 0 and cl['capital'][k_] == i and cf and W['et_f'][i] >= len(cf):
        plantar(arbol_mo, deriv_full, 0.0, 0.0, vh * 1.1, giro0, incl0, rumbo0, var0)   # protagonista
    elif est == 1:                                  # arbol joven (2 derivaciones) o adulto (completa)
        deriv = derivacion(W, cfg, i, now, paso)
        plantar(arbol_mo, deriv, 0.0, 0.0, vh * esc0, giro0, incl0, rumbo0, var0)
        if deriv < deriv_full:                      # el matorral se queda al pie como sotobosque
            ex = 0.30 * min(cw, cl_)
            plantar(mata_mo, 1, ex * math.cos(math.radians(giro0)), ex * math.sin(math.radians(giro0)),
                    vh * MATORRAL_K * SOTOBOSQUE_K * 1.6, giro0 + 60.0, 0.0, 0.0, var0)
    else:                                           # matorral pionero del bioma
        plantar(mata_mo, 1, 0.0, 0.0, vh * MATORRAL_K * 1.6, giro0, incl0, rumbo0, var0)
    res['biomas'][bioma_de(i)] += 1
    if meseta:
        _pedregal(W, cfg, i, p0, n, cw, cl_, vh, rug, emit, now, paso)
    if k_ >= 0 and 'esporas' in cf and W['et_f'][i] >= cf.index('esporas') + 1 \
            and now - W['t_et_f'][i] < ESPORAS_PASOS * paso:
        _particulas(out.setdefault('particulas', []), n, _add(p0, n, alto_en(ter, n)), cw, cl_, vh,
                    semilla_caos(i, 3), 6, COL_ESPORA, now, paso, 'esporas')
    return cuenta[0]


def radio_copa(geometria, fila):
    """Radio de la copa (en el mundo) de una fila de ejemplar (fase 13: la copa no
    tapa el rio). 0 si la geometria no es un ejemplar."""
    nm = geometria[4:] if geometria.startswith('mod_') else geometria
    if not es_ejemplar(nm):
        return 0.0
    mo, var, d, _ = parte_ejemplar(nm)
    return ejemplar(DEFAULT_CFG, mo, var, d)['copa'] * abs(fila[6])


def silueta(cfg, nombre, px=18, ancho=None):
    """La silueta de un ejemplar vista de lado a 'px' pixeles de alto (la prueba
    a distancia de la lamina): set de (columna, fila), fila 0 abajo. ancho: la
    escala horizontal (por defecto, la del alto)."""
    P, _, _, T = malla_ejemplar(nombre, cfg)
    k = (px - 1) / 1.0
    out = set()
    for a, b, c in T:
        pa, pb, pc = P[a], P[b], P[c]
        for u, v in ((0, 0), (1, 0), (0, 1), (0.5, 0), (0, 0.5), (0.5, 0.5), (0.33, 0.33)):
            x = pa[0] + (pb[0] - pa[0]) * u + (pc[0] - pa[0]) * v
            y = pa[1] + (pb[1] - pa[1]) * u + (pc[1] - pa[1]) * v
            out.add((int(round(x * k * (ancho or 1.0))), int(round(y * k))))
    return out


def iou(a, b):
    """Interseccion sobre union de dos siluetas (centradas en su eje)."""
    return len(a & b) / float(max(1, len(a | b)))


_NAT_CACHE = {}
NAT_MEMO = 48                # estados guardados por celda
VH_SALTO = 0.02              # la altura de la vegetacion va a saltos del 2 % del limite
NAT_CFG = ('nivel', 'caos', 'ligero', 'oceano', 'volcanes', 'detalle', 'max_caos_nat', 'th_branch', 'th_fusion', 'th_crown', 'limite_bosque', 'biomas',
           'variantes', 'var_angulo', 'cuantizar30', 'inclinacion', 'densidad_hoja', 'timidez', 'emergentes',
           'orla', 'mezcla', 'impostores', 'marco', 'sat_size', 'avance', 'pasos_etapa', 'max_niveles',
           'rug_min', 'rug_max', 'limite_nieve', 'respaldo', 'lod_nat', 'superficie')


def piel_natural_cache(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out, now, paso, doble):
    """piel_natural con memoria por celda (fase 11 v8): las filas de la celda solo
    se rehacen si cambia algo de lo que la decide; si no, se copian. Las celdas
    que cambian con el tiempo (fuego, esporas, muros que caen) no se guardan."""
    k_ = ctx['cl']['de'][i]
    cf = cadenas_de(cfg, 'naturaleza', especie_de('naturaleza', W['own'][i]))[0]
    vivo = i in arde or any(c == i and 0 <= now - t0 < PEDREGAL_PASOS * paso for t0, c in _MUROS) or \
        (k_ >= 0 and 'esporas' in cf and W['et_f'][i] >= cf.index('esporas') + 1
         and now - W['t_et_f'][i] < ESPORAS_PASOS * paso)
    if vivo:
        return piel_natural(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out, now, paso)
    paso_h = VH_SALTO * limit(cfg)          # la altura visible, a saltos (el latido y el stop-motion)
    vh = max(paso_h, round(vh / paso_h) * paso_h)
    ancho = round(ancho, 2)
    cap = ctx['cl']['capital'][k_] if k_ >= 0 else -1
    kp = avance_etapa(W, i, 'et_f', cf.index('puentes') + 1, now, paso) if k_ >= 0 and 'puentes' in cf else 1.0
    veg = W['own'][i] == GEO                 # la vegetacion: la altura visible solo escala los ejemplares
    clave = (W['occ'][i], W['own'][i], W['sp'][i], W['vel'][i], W['par'][i], None if veg else round(vh, 5), kb,
             round(fl, 3),
             sat, round(rug, 4), None if veg else ancho, pulido, doble, cap,
             min(DOSEL_MIN, len(ctx['cl']['celdas'][k_])) if k_ >= 0 else 1,
             W['vel'][cap] if cap >= 0 else 0, W['own'][cap] if cap >= 0 else 0, round(kp, 3), W['et_f'][i],
             tuple((W['occ'][j] > 0) * W['own'][j] for j in NEIGH[i]), _terreno_local(ctx['ter'], i),
             tuple(W['occ'][j] for j in NEIGH[i]) if cfg.get('oceano') else None,   # v97: la isla vecina crece
             tuple(ctx['cauces'].get(i, ())), ctx['rio_cerca'](i), ctx['cerca'](i),
             derivacion(W, cfg, i, now, paso), notas_colonas(W, i), ctx['bases'][i],
             tuple(cfg.get(x) for x in NAT_CFG), _clave_biblio(cfg), GRID['lo'], GRID['hi'])
    memo = _NAT_CACHE.setdefault(i, {})
    v = memo.get(clave)
    res = ctx['res']
    sway, rumbo_sw = ctx['sway'](i)
    if v is not None:
        filas, d, n, vh0, an0 = v
        ks = vh / vh0 if veg and vh0 > 0 else 1.0
        ka = (max(0.7, min(1.4, ancho)) / max(0.7, min(1.4, an0))) if veg else 1.0
        for g, f, mc in filas:
            f = list(f)
            if mc is not None:                  # el balanceo de la fase 17, sobre la fila guardada
                f[3:6] = _marco(i, mc[0], mc[1] + sway, mc[2] if mc[1] > 0 else rumbo_sw)[3]
                kx = ks * (1.0 if mc[3] else ka)      # la altura visible y el vigor (el sitio no cambia)
                if kx != 1.0 or ks != 1.0:
                    f[6], f[7], f[8] = f[6] * kx, f[7] * ks, f[8] * kx
            out.setdefault(g, []).append(f)
        emit.contar(len(filas))
        for k, x in d.items():
            if k == 'biomas':
                for b, y in x.items():
                    res['biomas'][b] += y
            elif k == 'frutales':
                res['frutales'].update(x)
            else:
                res[k] += x
        return n
    antes = dict((k, (dict(x) if isinstance(x, dict) else x)) for k, x in res.items())
    filas = []
    emit_ = emit

    def emit(modelo, pulido, *a, **kw):     # guarda cada fila y, si es un ejemplar, su marco
        emit_(modelo, pulido, *a, **kw)
        g = geometria_de(modelo, pulido, doble)
        filas.append((g, tuple(out[g][-1]), ctx.pop('mc', None)))
    emit.contar = emit_.contar
    ctx.pop('mc', None)
    n = piel_natural(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out, now, paso)
    d = {}
    for k, x in res.items():
        if k == 'biomas':
            d[k] = dict((b, x[b] - antes[k][b]) for b in x)
        elif k == 'frutales':
            d[k] = dict((c, y) for c, y in x.items() if c == i)
        else:
            d[k] = x - antes[k]
    if len(memo) >= NAT_MEMO:            # el balanceo y el stop-motion repiten estados: varios por celda
        memo.pop(next(iter(memo)))
    memo[clave] = (filas, d, n, vh, ancho)
    return n


def _terreno_local(ter, i):
    """Lo que del mapa de alturas mira la celda i: el relieve en su centro y en
    el de sus vecinas, y sus hibridos (el resto del mapa no la cambia)."""
    c = ter['centro']
    hb = ter.get('hibridos', {})
    return (round(c[i], 4),) + tuple(round(c[j], 4) for j in NEIGH[i]) + \
        (hb.get('arrozales', {}).get(i), hb.get('mesetas', {}).get(i), round(ter['hmax'], 4))


def derivacion(W, cfg, i, now, paso):
    """Derivacion visible del arbol de la celda i: 2 el joven (ocupacion 2), la
    completa el adulto. Avance = gates: cada gate que sube la ocupacion anade una
    derivacion; Avance = pasos: la nueva aparece Pasosetapa pasos despues."""
    o = W['occ'][i]
    obj = max(DERIVACION_JOVEN, min(DERIVACIONES, o))
    if int(cfg.get('avance', 0)) == 1 and now - W['t_h'][i] < cfg['pasos_etapa'] * paso:
        return max(DERIVACION_JOVEN, obj - 1)
    return obj


PEDREGAL_PASOS = 8          # el muro caido se ve 8 pasos


def _pedregal(W, cfg, i, p0, n, cw, cl, vh, rug, emit, now, paso):
    """Fase 14: los muros del bancal o de la meseta que quita un golpe caen como pedregal."""
    if cfg['nivel'] < 14:
        return
    for t0, c in _MUROS:
        if c == i and 0 <= now - t0 < PEDREGAL_PASOS * paso:
            col = material_tema(cfg, COL_RUINA['relieve'], 'mineral', rug)
            w_ = 0.35 * min(cw, cl)
            emit('rel_pedregal', True, _add(p0, n, alto_en(_TERRENO.get('t') or {}, n)), _marco(i, 30.0),
                 (w_, 0.25 * vh, w_), col, rug)


# -----------------------------------------------------------------------------
# 1. NUCLEO - tejido conectivo (fase 13): rios y carreteras
# -----------------------------------------------------------------------------
# Lo que ninguna senal pide: el sistema lo deduce del estado.
#   RIOS (naturaleza)  motor v46: nacen en las cumbres y bajan por el suelo
#                      real (suelo + relieve) a la vecina mas baja, hasta una
#                      hondonada (lago) o un llano, otro rio (confluyen y se
#                      ensancha) o Maxrio tramos. Son cintas de agua del azul
#                      reservado (geometria 'rios'), apoyadas en el terreno,
#                      que bordean el centro de cada celda.
#   CARRETERAS (ciudad) arbol de expansion minima (Kruskal) entre las capitales
#                      de cluster y las formaciones sueltas con ocupacion de
#                      Minvia o mas; cada arista, el camino mas corto por la
#                      reticula.
# Las carreteras van de centro a centro de celda, a ras del suelo (por debajo
# de las formaciones), en dos medios tramos que siguen la curva del planeta.
# Se recalculan solo cuando cambia la ocupacion (los rios, tambien el relieve).

COL_RIO = oklch_to_srgb(0.65, 0.18, 250.0)[0]   # azul reservado, vivo (motor v51; hasta la v50, L 0,55 C 0,15 h 255)
COL_RIO_V50 = oklch_to_srgb(0.55, 0.15, 255.0)[0]
COL_ORILLA = oklch_to_srgb(0.86, 0.06, 245.0)[0]   # la orilla: azul muy claro que recorta el rio sobre el verde
ORILLA_K = 1.8                     # la orilla, 1,8 veces el ancho del rio (motor v51)
COL_VIA = (0.17, 0.17, 0.19)       # asfalto
RUG_RIO, RUG_VIA = 0.10, 0.75      # el agua brilla; el asfalto, mate
TEJIDO_LIFT = 0.006                # sobre el suelo de la celda
TEJIDO_ALTO = 0.035
_TEJIDO = {}


def rios(W, cfg, cl=None, ter=None):
    """[[celdas del rio], ...] y {celda: celda aguas abajo}. Motor v46: bajan por
    el suelo real (suelo de la celda + relieve en su centro), no hacia la vecina
    menos ocupada. Nacen en las cumbres (las celdas con relieve mas altas que
    todas sus vecinas, y las capitales de relieve), se trazan de la mas alta a
    la mas baja y en cada tramo van a la vecina mas baja (empate: la de indice
    menor). Acaban en una hondonada o un llano (ninguna vecina mas baja), al
    llegar a otro rio (confluyen) o tras Maxrio tramos. Fase 13 v3: es cumbre
    la celda con un relieve de Pendientemin x el limite o mas (antes, 0,05), y
    la mas alta de cada cluster de relieve lo es siempre, aunque el mundo sea
    casi plano."""
    cl = cl or clusters(W, cfg)
    ter = ter or terreno(W, cfg, cl)
    G = [suelo(W, cfg, c) + ter['centro'][c] for c in range(N)]
    lim = limit(cfg)
    alto = set(c for c in range(N) if ter['centro'][c] > cfg.get('pendiente_min', 0.05) * lim)
    caps = set(cl['capital'][k] for k in cl['capital'] if W['own'][cl['capital'][k]] == ARQ)
    for k_, cs in cl['celdas'].items():     # v3: la celda mas alta de cada cluster de relieve, siempre
        if W['own'][cs[0]] == ARQ:
            top = max(cs, key=lambda c: (G[c], -c))
            if ter['centro'][top] > 1e-6:
                caps.add(top)
                alto.add(top)
    cumbres = set(c for c in alto if all(G[c] > G[j] + 1e-6 for j in NEIGH[c]))
    fuentes = sorted(cumbres | (caps & alto), key=lambda c: (-G[c], c))
    lista, abajo, en_rio = [], {}, set()
    tope = max(1, int(cfg['max_rio']))
    for f in fuentes:
        if f in en_rio:                 # la cumbre ya esta en otro rio
            continue
        camino = [f]
        while len(camino) <= tope:
            c = camino[-1]
            libres = [j for j in NEIGH[c] if j not in camino]
            if not libres:
                break
            j = min(libres, key=lambda x: (G[x], x))
            if G[j] >= G[c] - 1e-6:
                break                   # hondonada o llano: aqui acaba
            camino.append(j)
            if j in en_rio:
                break                   # confluencia
        if len(camino) < 2:
            continue
        for a, b in zip(camino, camino[1:]):
            abajo.setdefault(a, b)
        en_rio.update(camino)
        lista.append(camino)
    return lista, abajo


def color_rio(cfg):
    """El azul reservado de los rios (Colorrio), fuera de la paleta de conchas."""
    c = cfg.get('color_rio')
    return tuple(c) if c else COL_RIO


ALTO_CUADRO = 720.0           # alto de la imagen con el que se mide el ancho minimo


def px_unidad(W, cfg):
    """Pixeles por unidad de mundo con la camara de globo (el planeta mide
    Encuadre del alto de un cuadro de ALTO_CUADRO px), como px_formaciones."""
    return cfg.get('encuadre', ENCUADRE_DEF) * ALTO_CUADRO / (2.0 * (top_radius(W, cfg) + RETICULA_SOBRE_DEF))


ANCHO_MAX_RIO_K = 3.4      # motor v64: ancho maximo = 3,4 x Anchorio (antes Anchomaxrio, 0,34)


def ancho_rio(cfg, q):
    """Ancho de un tramo por el que pasan q rios: Anchorio con uno, hasta
    Anchomaxrio con cuatro o mas (se ensancha aguas abajo)."""
    lo = max(0.005, cfg['ancho_rio'])
    hi = max(lo, cfg['ancho_max_rio'])
    return lo + (hi - lo) * min(1.0, max(0, q - 1) / 3.0)


_CAUCES = {}
RIO_RECODO = 0.36            # el rio pasa a 0,36 anchos de celda del centro: lo bordea
RIO_FUENTE = 0.12            # nace cerca de la cumbre
RIO_LIFT, RIO_ALTO = 0.025, 0.006


def _borde(a, b):
    return _norm(_add(NORMALS[a], NORMALS[b]))


def _recodo(c, d_in, d_out, lado=1.0):
    """Por donde cruza el rio la celda c, de su borde d_in al d_out: lejos del
    centro (donde estan la formacion y la loseta de luz), hacia el lado de
    los dos bordes; si son opuestos, de lado."""
    n = NORMALS[c]
    v = _add(_add(d_in, d_out), n, -2.0)
    v = _add(v, n, -_dot(v, n))
    if _len(v) < 1e-4:
        v = _mul(_cross(n, _add(d_out, d_in, -1.0)), lado)
        if _len(v) < 1e-9:
            v = tangents(n)[0]
    return _norm(_add(n, _norm(v), RIO_RECODO * min(SIZE_EW[c], SIZE_NS[c])))


def _catmull(P, sub=5):
    """Puntos (direcciones) de una Catmull-Rom por los puntos P: [(dir, tramo)]."""
    out = []
    m = len(P)
    for k in range(m - 1):
        p0, p1, p2, p3 = P[max(0, k - 1)], P[k], P[k + 1], P[min(m - 1, k + 2)]
        for s in range(sub):
            u = s / float(sub)
            u2, u3 = u * u, u * u * u
            q = tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2
                             + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(3))
            out.append((_norm(q), k))
    out.append((P[-1], m - 2))
    return out


def cauces(W, cfg, cl=None, ter=None):
    """Los rios como cintas: dict(muestras=[[(dir, celda, ancho)]], lagos=[celda],
    por_celda={celda: [(dir, ancho en rad)]}). Cada rio va de su cumbre por los
    bordes de las celdas y cruza cada una lejos del centro; un afluente acaba en
    el recodo del rio que lo recibe. Se guarda con el tejido y el terreno."""
    if cfg['nivel'] < 13 or tema_de(cfg) != 'naturaleza' or not cfg.get('rios', 1):
        return dict(muestras=[], lagos=[], por_celda={})
    ter = ter or terreno(W, cfg, cl)
    tj = tejido(W, cfg)
    wmin = cfg.get('ancho_min_px', 0.0) / max(1e-6, px_unidad(W, cfg))     # v3: Anchominpx en pantalla
    clave = (_TEJIDO.get('version'), ter['version'], cfg['ancho_rio'], cfg['ancho_max_rio'],
             cfg.get('lagos', 1), suelos_fotograma(W, cfg), round(wmin, 5))
    if _CAUCES.get('clave') == clave:
        return _CAUCES['c']
    recodos, muestras, lagos, por = {}, [], [], {}
    for camino in tj['rios']:
        P, arista = [], []              # puntos de control y la arista del tramo que sale de cada uno
        a, b = camino[0], camino[1]
        n0 = NORMALS[a]
        v = _add(_borde(a, b), n0, -1.0)
        P.append(_norm(_add(n0, _norm(_add(v, n0, -_dot(v, n0))), RIO_FUENTE * min(SIZE_EW[a], SIZE_NS[a]))))
        arista.append((a, b))
        for k in range(1, len(camino)):
            c_ant, c = camino[k - 1], camino[k]
            d_in = _borde(c_ant, c)
            P.append(d_in)
            arista.append((c_ant, c))
            if k + 1 < len(camino):
                d_out = _borde(c, camino[k + 1])
                q = recodos.setdefault(c, _recodo(c, d_in, d_out, 1.0 if k % 2 else -1.0))
                arista.append((c, camino[k + 1]))
            else:
                if c in recodos:        # confluye: acaba en el recodo del otro rio
                    q = recodos[c]
                else:
                    q = _recodo(c, d_in, _norm(_add(_mul(NORMALS[c], 2.0), d_in, -1.0)),
                                1.0 if k % 2 else -1.0)
                    recodos[c] = q
                    if cfg.get('lagos', 1) and laguna(W, cfg, c) > 0.02 \
                            and not (cfg.get('oceano') and suelo(W, cfg, c) - nivel_mar(W, cfg) < 0.02) \
                            and not (cfg['nivel'] >= 29 and es_escision(W, c)):    # fase 29: un rio no la llena
                        lagos.append(c)
                arista.append((c_ant, c))
            P.append(q)
        lista = []
        for d, k in _catmull(P):
            x, y = arista[min(len(arista) - 1, k)]
            c_ = x if _dot(d, NORMALS[x]) >= _dot(d, NORMALS[y]) else y
            w = max(wmin, ancho_rio(cfg, tj['caudal'].get((x, y), 1)))
            lista.append((d, c_, w))
            por.setdefault(c_, []).append((d, w / max(1e-6, suelo(W, cfg, c_))))
        muestras.append(lista)
    c = dict(muestras=muestras, lagos=sorted(set(lagos)), por_celda=por, wmin=wmin)
    _CAUCES['clave'], _CAUCES['c'] = clave, c
    return c


def build_rios(W, cfg):
    """(filas de la geometria 'rios', resumen): las cintas de agua apoyadas en
    el terreno (con un pequeno desfase) y los lagos de las hondonadas. Azul
    reservado, sin tintes de celda, de pad ni de concha."""
    ca = cauces(W, cfg)
    filas = []
    tj = tejido(W, cfg) if cfg['nivel'] >= 13 else dict(rios=[], caudal={})
    res = dict(rios=len(ca['muestras']), lagos=len(ca['lagos']),
               tramos=sum(len(r) - 1 for r in tj['rios']), fuentes=len(tj['rios']),
               caudal=max(tj['caudal'].values() or [0]), px=0.0)
    if not ca['muestras'] and not ca['lagos']:
        return filas, res
    res['px'] = max(w for lista in ca['muestras'] for _, _, w in lista) * px_unidad(W, cfg) \
        if ca['muestras'] else 0.0
    clave = (id(ca), _CAUCES.get('clave'), cfg.get('respaldo', 0), color_rio(cfg), cfg.get('oceano', 0))
    if _CAUCES.get('filas_clave') == clave:         # las cintas no se mueven: se guardan (sin copiar:
        return _CAUCES['filas'], res                # nadie las modifica despues)
    ter = terreno(W, cfg)
    col = color_rio(cfg)
    hmax = ter['hmax']
    rug = 1.0 if cfg.get('respaldo', 0) else RUG_RIO
    for lista in ca['muestras']:
        pts = []
        tierra = []
        for d, c, w in lista:
            E = alto_en(ter, d)
            pts.append((_mul(d, suelo(W, cfg, c) + E + RIO_LIFT + 0.03 * E / hmax), w))
            tierra.append(E >= ORILLA_PLANTA or not cfg.get('oceano'))
        for k_, ((p, w), (q, w2)) in enumerate(zip(pts, pts[1:])):
            if not tierra[k_ + 1] and any(tierra[:k_ + 1]):
                break                       # motor v97: el rio acaba en el mar (no cruza el oceano)
            if not tierra[k_]:
                continue
            dv = _add(q, p, -1.0)
            L = _len(dv)
            if L < 1e-6:
                continue
            Z = _mul(dv, 1.0 / L)
            mid = _mul(_add(p, q), 0.5)
            Y = _norm(mid)
            Y = _norm(_add(Y, Z, -_dot(Y, Z)))
            X = _cross(Y, Z)
            rx, ry, rz = _euler_xyz(X, Y, Z)
            ww = 0.5 * (w + w2)
            filas.append([mid[0], mid[1], mid[2], rx, ry, rz, ww, RIO_ALTO, L + 0.5 * ww,
                          col[0], col[1], col[2], rug])
            # v51: la orilla, una cinta clara mas ancha justo debajo: el rio se recorta sobre el verde
            po = _add(mid, Y, -0.6 * RIO_ALTO)
            filas.append([po[0], po[1], po[2], rx, ry, rz, ww * ORILLA_K, RIO_ALTO, L + 0.5 * ww * ORILLA_K,
                          COL_ORILLA[0], COL_ORILLA[1], COL_ORILLA[2], rug])
    for c in ca['lagos']:                   # la hondonada se llena hasta su borde mas bajo
        S = suelo(W, cfg, c)
        borde = min(suelo(W, cfg, j) for j in NEIGH[c]) - 0.01
        h = borde - S
        if h <= 0.01:
            continue
        cw, cl_ = _cell_sizes(S, c)
        filas.append(_row(_mul(NORMALS[c], S), NORMALS[c], 1.02 * cw, h, 1.02 * cl_, col) + [rug])
    _CAUCES['filas_clave'], _CAUCES['filas'] = clave, filas
    return filas, res


def _caudal(lista, abajo):
    """{(a, b): rios que pasan por el tramo}: cada rio suma 1 a sus tramos y,
    si confluye, a los del rio al que llega, aguas abajo de la confluencia."""
    q = {}
    for camino in lista:
        for a, b in zip(camino, camino[1:]):
            q[(a, b)] = q.get((a, b), 0) + 1
        c, vistos = camino[-1], set(camino)
        while c in abajo and abajo[c] not in vistos:
            d = abajo[c]
            q[(c, d)] = q.get((c, d), 0) + 1
            vistos.add(d)
            c = d
    return q


def camino_corto(a, b):
    """Celdas del camino mas corto de a a b por la reticula (BFS; a igualdad,
    por las vecinas de indice menor)."""
    if a == b:
        return [a]
    padre = {a: None}
    frente = [a]
    while frente and b not in padre:
        sig = []
        for c in frente:
            for j in sorted(NEIGH[c]):
                if j not in padre:
                    padre[j] = c
                    sig.append(j)
        frente = sig
    if b not in padre:
        return []
    out = [b]
    while out[-1] != a:
        out.append(padre[out[-1]])
    return out[::-1]


def camino_traza(a, b, trazas, peso):
    """Camino de a a b que prefiere las trazas heredadas (fase 15): Dijkstra
    con coste 1 por tramo y 1 - 0,9 x Pesotraza por tramo de traza; a
    igualdad, el de menos tramos y luego el de celdas menores. Devuelve
    (celdas, coste). Sin trazas o sin peso, el camino mas corto."""
    if not trazas or peso <= 0:
        c = camino_corto(a, b)
        return c, float(len(c) - 1)
    import heapq
    barato = 1.0 - 0.9 * max(0.0, min(1.0, peso))
    mejor = {a: (0.0, 0)}
    cola = [(0.0, 0, [a])]
    while cola:
        coste, n, camino = heapq.heappop(cola)
        c = camino[-1]
        if c == b:
            return camino, coste
        if mejor.get(c, (1e18, 0)) < (coste, n):
            continue
        for j in sorted(NEIGH[c]):
            k = coste + (barato if (min(c, j), max(c, j)) in trazas else 1.0)
            if (k, n + 1) < mejor.get(j, (1e18, 0)):
                mejor[j] = (k, n + 1)
                heapq.heappush(cola, (k, n + 1, camino + [j]))
    return [], -1.0


def nodos_via(W, cfg, cl=None):
    """Capitales de cluster y formaciones sueltas (sin satelites) con ocupacion
    de Minvia o mas."""
    cl = cl or clusters(W, cfg)
    nodos = set(cl['capital'].values())
    for i in range(N):
        if W['occ'][i] >= cfg['min_via'] and W['par'][i] < 0 and cl['de'][i] < 0:
            nodos.add(i)
    return sorted(nodos)


def carreteras(W, cfg, cl=None, trazas=None):
    """(aristas del arbol [(a, b, distancia)], tramos [(c, d)]): Kruskal sobre
    las distancias por la reticula entre los nodos. Con trazas (fase 15), la
    distancia es el coste del camino que las prefiere (Pesotraza)."""
    nodos = nodos_via(W, cfg, cl)
    peso = cfg.get('peso_traza', 0.0)
    caminos = {}
    pares = []
    for k, a in enumerate(nodos):
        for b in nodos[k + 1:]:
            if trazas:
                caminos[(a, b)], d = camino_traza(a, b, trazas, peso)
            else:
                d = len(camino_corto(a, b)) - 1
            pares.append((d, a, b))
    padre = dict((x, x) for x in nodos)

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    arbol, tramos = [], []
    for d, a, b in sorted(pares):
        ra, rb = raiz(a), raiz(b)
        if ra == rb or d < 0:
            continue
        padre[ra] = rb
        arbol.append((a, b, d))
        camino = caminos[(a, b)] if trazas else camino_corto(a, b)
        for c, e in zip(camino, camino[1:]):
            if (c, e) not in tramos and (e, c) not in tramos:
                tramos.append((c, e))
    return arbol, tramos


def tejido(W, cfg):
    """Topologia del tejido (se guarda: solo se recalcula si cambia la
    ocupacion). dict(rios, abajo, caudal, arbol, vias)."""
    tema = tema_de(cfg)
    sello = (id(W), _TERRENO.get('sello'), tuple(W['occ']), tema, cfg['rios'], cfg['carreteras'],
             cfg['max_rio'], cfg['min_via'], len(W.get('trazas') or []), cfg.get('vias'), cfg.get('red'),
             cfg.get('min_red'), tuple(W['own']))
    if _TEJIDO.get('sello') == sello:       # ya visto en este fotograma
        return _TEJIDO['t']
    trazas = frozenset((min(a, b), max(a, b)) for a, b in W.get('trazas') or []) \
        if cfg['nivel'] >= 15 else frozenset()
    ter = terreno(W, cfg) if tema == 'naturaleza' and cfg['rios'] else None
    alturas = tuple(round(s_ + e_, 3) for s_, e_ in zip(suelos_fotograma(W, cfg), ter['centro'])) if ter else ()
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), tema, cfg['rios'], cfg['carreteras'],
             cfg['min_via'], cfg['max_rio'], cfg['umbral_vecindad'], cfg['peso_vecina'],
             cfg['min_cluster'], cfg['th_fusion'], GRID['lo'], GRID['hi'], trazas,
             cfg.get('peso_traza', 0.0), alturas, cfg.get('pendiente_min', 0.05), cfg.get('vias'), cfg.get('red'),
             cfg.get('min_red'), cfg.get('recursos'), tuple(len(x) for x in W.get('cols', [])))
    if _TEJIDO.get('clave') == clave:
        _TEJIDO['sello'] = sello
        return _TEJIDO['t']
    t = dict(rios=[], abajo={}, caudal={}, arbol=[], vias=[])
    cl = clusters(W, cfg)
    if tema == 'naturaleza' and cfg['rios']:
        t['rios'], t['abajo'] = rios(W, cfg, cl, ter)
        t['caudal'] = _caudal(t['rios'], t['abajo'])
    if tema == 'ciudad' and cfg['carreteras']:
        t['arbol'], t['vias'] = carreteras(W, cfg, cl, trazas)
    if tema == 'industria':             # fase 13 v7: las vias (como rios) y la red (al reves)
        t['fc'] = ferrocarril(W, cfg, trazas)
        t['vias'] = list(t['fc']['vias'])
        t['red'] = red_electrica(W, cfg)
    _TEJIDO['clave'], _TEJIDO['t'] = clave, t
    _TEJIDO['version'] = _TEJIDO.get('version', 0) + 1
    _TEJIDO['sello'] = sello
    return t


def _tramo_suelo(W, cfg, a, b, ancho, col, rug, out, desplaza=0.0, medio=False):
    """Dos medios tramos de la celda a a la b, a ras del suelo, siguiendo la
    curva: centro de a -> punto medio -> centro de b. 'desplaza' lo aparta de lado
    (los railes de la industria); 'medio', solo el primer medio tramo."""
    na, nb = normal_i(a), normal_i(b)
    ra = base_radius(W, cfg, a) + TEJIDO_LIFT
    rb = base_radius(W, cfg, b) + TEJIDO_LIFT
    pa, pb = _mul(na, ra), _mul(nb, rb)
    pm = _mul(_norm(_add(na, nb)), 0.5 * (ra + rb))
    for p, q in (((pa, pm),) if medio else ((pa, pm), (pm, pb))):
        Y = _norm(_add(p, q))           # el centro, sobre la superficie (no en la cuerda)
        c = _mul(Y, 0.5 * (math.sqrt(_dot(p, p)) + math.sqrt(_dot(q, q))))
        d = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
        d = _add(d, Y, -_dot(d, Y))
        L = math.sqrt(_dot(d, d))
        if L < 1e-6:
            continue
        Z = _mul(d, 1.0 / L)
        X = _cross(Y, Z)
        if desplaza:
            c = _add(c, X, desplaza)
        rx, ry, rz = _euler_xyz(X, Y, Z)
        out.append([c[0], c[1], c[2], rx, ry, rz, ancho, TEJIDO_ALTO, L + 0.5 * ancho,
                    col[0], col[1], col[2], rug])


def build_tejido(W, cfg):
    """(filas de la geometria 'tejido', resumen para la leyenda)."""
    t = tejido(W, cfg)
    W['tejido_vias'] = t['vias'] if tema_de(cfg) == 'ciudad' else []
    if tema_de(cfg) == 'industria':     # fase 13 v7: vias y red
        return build_tejido_industria(W, cfg, t)
    filas = []
    w = cfg['grosor_via']
    for a, b in t['vias']:                  # los rios van en su geometria ('rios', build_rios)
        _tramo_suelo(W, cfg, a, b, w, COL_VIA, RUG_VIA, filas)
    if cfg.get('respaldo', 0):
        for f in filas:
            f[12] = 1.0
    return filas, dict(rios=len(t['rios']), tramos_rio=len(t['caudal']), tramos_via=len(t['vias']))



# --- el tejido de la industria (fase 13 v7, motor v68): vias y red ------------------
# FERROCARRIL, como los rios: nace en cada mina con ocupacion Minvia o mas y baja
# por el camino mas corto (Dijkstra; los tramos de la industria enterrada pesan
# menos, Pesotraza) hasta la planta de energia mas cercana. Las lineas confluyen:
# la carga de un tramo son las lineas que pasan (via unica, doble desde 2) y a la
# llegada se abre una playa de vias. Un desnivel se salva con un viaducto.
# RED ELECTRICA, como un rio al reves: nace en cada central (energia desde la
# fusion - 1) y se ramifica por las formaciones de la industria hasta todas las de
# ocupacion Minred o mas: un arbol con raiz en las centrales (BFS de varias
# fuentes por las celdas ocupadas). La carga de un tramo, las formaciones que
# alimenta aguas abajo: alta tension, media o postes. Lo que no alcanza ninguna
# central se apaga (sin pulsos, naves a oscuras). Los pulsos violeta salen de la
# central hacia fuera, al tempo.
COL_BALASTO, COL_RAIL = (0.16, 0.14, 0.13), (0.70, 0.68, 0.64)
COL_CABLE = (0.10, 0.10, 0.11)


def ferrocarril(W, cfg, trazas):
    """dict(vias=[(a, b)], carga={(a, b): lineas}, playas=[planta], lineas=[[celdas]],
    fuente={planta: set(recursos)})."""
    import heapq
    out = dict(vias=[], carga={}, playas=[], lineas=[], fuente={})
    if not cfg.get('vias', 1):
        return out
    minas = [i for i in range(N) if W['occ'][i] >= max(1, int(cfg['min_via'])) and W['own'][i] == GEO]
    plantas = [i for i in range(N) if W['occ'][i] > 0 and W['own'][i] == ARQ]
    if not minas or not plantas:
        return out
    peso = max(0.0, float(cfg.get('peso_traza', 0.5)))
    dist = dict((p, 0.0) for p in plantas)
    hacia = dict((p, None) for p in plantas)
    cola = [(0.0, p) for p in plantas]
    heapq.heapify(cola)
    while cola:
        d, c = heapq.heappop(cola)
        if d > dist.get(c, 1e9) + 1e-12:
            continue
        for j in sorted(NEIGH[c]):
            w = 1.0 - (0.5 * min(1.0, peso) if (min(c, j), max(c, j)) in trazas else 0.0)
            nd = d + w
            if nd < dist.get(j, 1e9) - 1e-12:
                dist[j], hacia[j] = nd, c
                heapq.heappush(cola, (nd, j))
    for mi in sorted(minas):
        if mi in plantas or mi not in hacia:
            continue
        linea = [mi]
        while hacia[linea[-1]] is not None and len(linea) < N:
            linea.append(hacia[linea[-1]])
        out['lineas'].append(linea)
        destino = linea[-1]
        out['fuente'].setdefault(destino, set()).add(recurso_celda(W, cfg, mi))
        if destino not in out['playas']:
            out['playas'].append(destino)
        for a, b in zip(linea, linea[1:]):
            k = (min(a, b), max(a, b))
            out['carga'][k] = out['carga'].get(k, 0) + 1
    out['vias'] = sorted(out['carga'])
    return out


def red_electrica(W, cfg):
    """dict(tramos=[(padre, hijo)], carga={hijo: formaciones aguas abajo},
    hondo={celda: tramos desde la central}, centrales=[...], apagadas=[...])."""
    out = dict(tramos=[], carga={}, hondo={}, centrales=[], apagadas=[])
    if not cfg.get('red', 1):
        return out
    umbral = int(cfg['th_fusion']) - 1
    nodos = set(i for i in range(N) if W['occ'][i] > 0 and W['own'][i])
    centrales = sorted(i for i in nodos if W['own'][i] == ARQ and W['occ'][i] >= umbral)
    consumo = set(i for i in nodos if W['occ'][i] >= max(1, int(cfg['min_red'])))
    out['centrales'] = centrales
    padre = dict((c, None) for c in centrales)
    hondo = dict((c, 0) for c in centrales)
    frente = list(centrales)
    while frente:
        sig = []
        for c in frente:
            for j in sorted(NEIGH[c]):
                if j in nodos and j not in padre:
                    padre[j], hondo[j] = c, hondo[c] + 1
                    sig.append(j)
        frente = sig
    carga = dict((c, 1 if c in consumo else 0) for c in padre)
    for c in sorted(padre, key=lambda x: -hondo[x]):
        if padre[c] is not None:
            carga[padre[c]] += carga[c]
    # solo las ramas que llevan a algun consumidor
    out['tramos'] = sorted((padre[c], c) for c in padre if padre[c] is not None and carga[c] > 0)
    out['carga'], out['hondo'] = carga, hondo
    out['apagadas'] = sorted(c for c in consumo if c not in padre)
    return out


def nivel_red(carga):
    """0 postes, 1 media tension, 2 alta tension (cerca de la central)."""
    return 2 if carga >= 5 else (1 if carga >= 2 else 0)


def _cable(W, cfg, a, b, h, ancho, col, out):
    """Un tramo de cable entre las torres de a y b, a altura h."""
    pa = _mul(normal_i(a), base_radius(W, cfg, a) + h)
    pb = _mul(normal_i(b), base_radius(W, cfg, b) + h)
    c = _mul(_add(pa, pb), 0.5)
    d = _add(pb, pa, -1.0)
    L = _len(d)
    if L < 1e-6:
        return
    Y = _norm(c)
    Z = _norm(_add(d, Y, -_dot(d, Y)))
    X = _cross(Y, Z)
    rx, ry, rz = _euler_xyz(X, Y, Z)
    out.append([c[0], c[1], c[2], rx, ry, rz, ancho, ancho, L, col[0], col[1], col[2], 0.6])


_TEJ_IND = {}


def _clave_tej_ind(W, cfg, t):
    """Lo que cambia las filas fijas del tejido de la industria: la topologia (la
    version del tejido), el suelo de sus celdas y los anchos (una vez por fotograma)."""
    sello = (id(W), _TERRENO.get('sello'), _TEJIDO.get('version'))
    v = _TEJ_IND.get('clave')
    if v is not None and v[0] == sello:
        return v[1]
    nodos = set(x for e in (t.get('fc') or {}).get('vias', []) for x in e) | \
        set(x for e in (t.get('red') or {}).get('tramos', []) for x in e)
    clave = (_TEJIDO.get('version'), tuple(round(base_radius(W, cfg, x), 4) for x in sorted(nodos)),
             cfg.get('ancho_via'), cfg.get('respaldo', 0), limit(cfg), GRID['lo'], GRID['hi'],
             cfg.get('recursos'))
    _TEJ_IND['clave'] = (sello, clave)
    return clave


def build_tejido_industria(W, cfg, t):
    """Filas del 'tejido' de la industria: balasto y railes (doble via, playas) y
    los cables de la red. Se guardan mientras no cambie la topologia ni el suelo.
    Devuelve (filas, resumen)."""
    clave = _clave_tej_ind(W, cfg, t)
    v = _TEJ_IND.get('filas')
    if v is not None and v[0] == clave:         # las mismas filas: el Script CHOP no se recuece
        return list(v[1]), dict(v[2])
    filas, res = _build_tejido_industria(W, cfg, t)
    _TEJ_IND['filas'] = (clave, filas, dict(res))
    return list(filas), res


def _build_tejido_industria(W, cfg, t):
    filas = []
    w = cfg.get('ancho_via', 0.14)
    lim = limit(cfg)
    fc = t.get('fc') or {}
    for a, b in fc.get('vias', []):
        doble = fc['carga'].get((a, b), 1) >= 2
        wb = w * (1.7 if doble else 1.0)
        _tramo_suelo(W, cfg, a, b, wb, COL_BALASTO, 0.9, filas)
        for off in ((-0.32, -0.12, 0.12, 0.32) if doble else (-0.12, 0.12)):
            _tramo_suelo(W, cfg, a, b, 0.07 * wb, COL_RAIL, 0.2, filas, desplaza=off * wb)
    for p in fc.get('playas', []):                  # la playa de vias: el haz se abre a la llegada
        for j in sorted(NEIGH[p])[:1]:
            for off in (-0.5, -0.25, 0.0, 0.25, 0.5):
                _tramo_suelo(W, cfg, p, j, 0.12 * w, COL_RAIL, 0.2, filas, desplaza=off * w * 2.4, medio=True)
    red = t.get('red') or {}
    for a, b in red.get('tramos', []):
        nv = nivel_red(red['carga'].get(b, 1))
        h = (0.10, 0.20, 0.34)[nv] * lim
        _cable(W, cfg, a, b, h, (0.008, 0.014, 0.022)[nv] * (1.0 + 0.1 * red['carga'].get(b, 1) ** 0.5),
               COL_CABLE, filas)
    if cfg.get('respaldo', 0):
        for f in filas:
            f[12] = 1.0
    res = dict(rios=0, tramos_rio=0, tramos_via=len(fc.get('vias', [])), lineas=len(fc.get('lineas', [])),
               playas=len(fc.get('playas', [])), centrales=len(red.get('centrales', [])),
               tramos_red=len(red.get('tramos', [])), apagadas=len(red.get('apagadas', [])))
    return filas, res


def build_industria_tejido(W, cfg, now, out):
    """Lo que el tejido de la industria pone en las geometrias de los modelos y las
    particulas: viaductos, torres y postes, los pulsos violeta de la red y (desde
    la fase 17) los trenes, cargados con el recurso de su mina hacia la planta y
    vacios de vuelta, al tempo."""
    if tema_de(cfg) != 'industria':
        return
    t = tejido(W, cfg)
    lim = limit(cfg)
    doce = cfg['nivel'] >= 12
    paso = W.get('paso') or 0.125
    spb = max(1, int(cfg.get('steps_per_beat', 4)))
    tau = beat_stop(W, cfg) if cfg['nivel'] >= 17 else now / max(1e-6, paso * spb)
    clave = (_clave_tej_ind(W, cfg, t), doce)
    fijo = _TEJ_IND.get('fijo')
    if fijo is None or fijo[0] != clave:       # viaductos, torres y los extremos de los pulsos: se guardan
        fijo = _TEJ_IND['fijo'] = (clave, _tejido_ind_fijo(W, cfg, t, doce))
    for g, filas_ in fijo[1]['filas'].items():
        out.setdefault(g, []).extend(filas_)
    parts = out.setdefault('particulas', [])
    if cfg.get('pulso_red', 1) and cfg['nivel'] >= 13:     # los pulsos: de la central hacia fuera
        col = cfg.get('color_red') or COL_RED_DEF
        s_ = 0.03 * lim
        for h, pa, d, rx, ry in fijo[1]['pulsos']:
            f = (tau * 0.5 - 0.25 * h) % 1.0
            parts.append([pa[0] + d[0] * f, pa[1] + d[1] * f, pa[2] + d[2] * f, rx, ry, 0.0, s_, s_, s_,
                          col[0], col[1], col[2]])
    if cfg['nivel'] >= 17:                          # fase 17: los trenes (motor v75: en 'vagones', cajas)
        trenes(fijo[1], tau, lim, out.setdefault('vagones', []))


def _tejido_ind_fijo(W, cfg, t, doce):
    """Lo fijo del tejido de la industria para las geometrias de los modelos."""
    lim = limit(cfg)
    salida = {}

    def fila(mo, p, ej, dims, col):
        f = _fila_m(p, ej, dims[0], dims[1], dims[2], col)
        if doce:
            f.append(1.0)
        salida.setdefault(geometria_de(mo), []).append(f)
    fc = t.get('fc') or {}
    for a, b in fc.get('vias', []):                 # viaductos donde la via salva un desnivel
        ra, rb = base_radius(W, cfg, a), base_radius(W, cfg, b)
        if abs(ra - rb) > 0.04 * lim:
            ej = _marco_puente(a, b) if ra > rb else _marco_puente(b, a)
            hi = max(ra, rb)
            pm = _mul(_norm(_add(normal_i(a), normal_i(b))), min(ra, rb))
            L = _len(_add(_mul(normal_i(a), ra), _mul(normal_i(b), rb), -1.0))
            fila('ciu_viaducto', _add(pm, _norm(pm), 0.0), ej, (cfg.get('ancho_via', 0.14) * 1.4, hi - min(ra, rb)
                                                                + 0.01, 0.5 * L), COL_REMATE['subestacion'])
    red = t.get('red') or {}
    puestos = set()
    for a, b in red.get('tramos', []):              # torres y postes en cada nudo
        for c, nv in ((a, nivel_red(red['carga'].get(b, 1))), (b, nivel_red(red['carga'].get(b, 1)))):
            if (c, nv) in puestos:
                continue
            puestos.add((c, nv))
            n = normal_i(c)
            cw, cl_ = _cell_sizes(base_radius(W, cfg, c), c)
            p = _add(_add(_mul(n, base_radius(W, cfg, c)), tangents(n)[0], 0.4 * cw), tangents(n)[1], 0.4 * cl_)
            alto = (0.10, 0.20, 0.34)[nv] * lim
            fila('ciu_torre' if nv else 'ciu_poste', p, _marco(c), (alto * (0.5 if nv else 0.25), alto, 0.05 * cw),
                 (0.55, 0.55, 0.56))
    pulsos = []
    for a, b in red.get('tramos', []):
        nv = nivel_red(red['carga'].get(b, 1))
        alto = (0.10, 0.20, 0.34)[nv] * lim
        pa = _mul(normal_i(a), base_radius(W, cfg, a) + alto)
        pb = _mul(normal_i(b), base_radius(W, cfg, b) + alto)
        rx, ry = orient(_norm(_add(pa, pb)))
        pulsos.append((red['hondo'].get(a, 0), pa, _add(pb, pa, -1.0), rx, ry))
    lineas = []
    for linea in fc.get('lineas', []):
        if len(linea) < 2:
            continue
        tramos = []
        for a, b in zip(linea, linea[1:]):
            pa = _mul(normal_i(a), base_radius(W, cfg, a) + 0.02 * lim)
            pb = _mul(normal_i(b), base_radius(W, cfg, b) + 0.02 * lim)
            d = _add(pb, pa, -1.0)
            rx, ry = orient(_norm(_add(pa, pb)))
            tramos.append((pa, d, _norm(d), rx, ry))
        lineas.append((tramos, COL_RECURSO[recurso_celda(W, cfg, linea[0])]))
    return dict(filas=salida, pulsos=pulsos, lineas=lineas)


def trenes(fijo, tau, lim, parts):
    """Fase 17: un convoy por linea, cargado con el recurso de su mina hacia la
    planta y vacio de vuelta, al tempo (STOP, huelga: se para)."""
    s_, a_ = 0.035 * lim, 0.03 * lim
    for k, (tramos, rec) in enumerate(fijo['lineas']):
        n_ = len(tramos)
        u = (tau / (2.0 * (n_ + 1)) + 0.37 * k) % 2.0     # ida (cargado) y vuelta (vacio)
        ida = u < 1.0
        pos = (u if ida else 2.0 - u) * n_
        q = min(n_ - 1, int(pos))
        fr = pos - q
        pa, d, du, rx, ry = tramos[q]
        sg = -0.05 * lim if ida else 0.05 * lim
        for v in range(4):                          # locomotora y tres vagones
            col = (0.18, 0.18, 0.2) if v == 0 else (rec if ida else (0.45, 0.42, 0.40))
            o = sg * v
            parts.append([pa[0] + d[0] * fr + du[0] * o, pa[1] + d[1] * fr + du[1] * o,
                          pa[2] + d[2] * fr + du[2] * o, rx, ry, 0.0, s_, a_, s_, col[0], col[1], col[2]])


# -----------------------------------------------------------------------------
# 1. NUCLEO - destructores I (fase 14): aranazos tematicos y escalada
# -----------------------------------------------------------------------------
# Los aranazos de la bateria (los pads cuyo perfil no tiene profundidad: los
# que no cortan) toman forma tematica. Un golpe es un accidente: la formacion
# mas alta de la vecindad del objetivo (el objetivo y sus vecinas) baja un
# estado, si la erosion no la ha bajado ya: rayo que tala el arbol,
# desprendimiento de columnas, se desploma un anadido, caen las plantas altas.
# Golpesescalada golpes o mas en la misma vecindad (el objetivo de uno en la
# vecindad del otro) dentro de Ventanaescalada pasos son una catastrofe en la
# formacion mas alta de la vecindad:
#   incendio (vegetacion)    arde y salta por los puentes del dosel a las
#                            celdas del cluster con vegetacion
#   derrumbe (relieve) y derrumbe en cadena (informal): lo mismo, con polvo
#   implosion (planificada)  la torre cae entera de golpe, con polvo
# Cada celda activa pierde 1 de ocupacion por paso y se apaga sin ocupacion o
# a los Pasosfuego pasos. El salto lo decide el mapa logistico sembrado con la
# velocidad del golpe y la celda (sin azar): la misma historia da el mismo
# fuego. Nunca sale de su cluster, y Maxfuego limita las celdas activas a la
# vez. Con la densidad por encima de Umbraldensidad empieza mas grande (la
# celda y sus vecinas del cluster), como la erosion con Multradio. Lo que se
# vacia deja su huella (claro de ceniza, pedregal, escombros, solar vallado)
# hasta que una nota vuelve a construir. Una obra a medias que recibe un
# aranazo se derriba: su cadena se recorre hacia atras hasta que una nota del
# cluster la retome. El fin de ciclo lo apaga todo de golpe.

RUINA_ESP = ['vegetacion', 'relieve', 'informal', 'planificada', 'mina', 'energia', 'refineria']
# fase 11 v11: la industria. La refineria (la mina en su ultima etapa) tiene su propia catastrofe
ACCIDENTE = dict(vegetacion='rayo', relieve='desprendimiento', informal='se desploma un anadido',
                 planificada='caen las plantas altas', mina='derrumbe de galeria', energia='cae una chimenea',
                 refineria='fuga con llamarada')
CATASTROFE = dict(vegetacion='incendio', relieve='derrumbe', informal='derrumbe en cadena',
                  planificada='implosion', mina='explosion de grisu', energia='apagon en cadena',
                  refineria='incendio')
RUINA_ALTO = dict(vegetacion=0.30, relieve=0.22, informal=0.26, planificada=0.12, mina=0.12, energia=0.3,
                  refineria=0.08)    # x limite
TEMA_DE_ESP = dict(vegetacion='naturaleza', relieve='naturaleza', informal='ciudad', planificada='ciudad',
                   mina='industria', energia='industria', refineria='industria')
COL_CENIZA = (0.44, 0.43, 0.41)           # copos de ceniza
COL_CARBON = (0.10, 0.09, 0.08)           # lo que arde se carboniza
COL_BRASA = (1.00, 0.46, 0.10)
COL_RUINA = dict(vegetacion=(0.25, 0.23, 0.21), relieve=(0.38, 0.37, 0.40), informal=(0.46, 0.44, 0.41),
                 planificada=COL_OBRA['valla'], mina=(0.18, 0.16, 0.15), energia=(0.48, 0.30, 0.20),
                 refineria=(0.06, 0.06, 0.06))


def especie_destructor(W, cfg, i):
    """La especie para los destructores: la de la celda, salvo la refineria (la
    mina en su ultima etapa), que arde por sus tuberias."""
    esp = especie_de(tema_de(cfg), W['own'][i])
    if esp == 'mina' and etapa_ciudad(cfg, esp, W['occ'][i]) >= 5:
        return 'refineria'
    return esp


SALTO = 0.5                 # el fuego salta a una vecina si el mapa logistico pasa de aqui
POLVO_MAX = 48              # nubes de particulas a la vez


def es_aranazo(cfg, pad):
    """Un pad de erosion sin profundidad (no corta): los de la fase 14. Un pad
    de impulso (fase 7 v12) no es aranazo ni corte."""
    return int(pad) not in pads_corte(cfg) and not es_impulso(cfg, pad)


def vecindad(i):
    return [i] + list(NEIGH[i])


def victima(W, cfg, objetivo):
    """(celda, estado) de la formacion mas alta de la vecindad del objetivo
    (empate: la de indice menor), o None si la vecindad esta vacia."""
    mejor = None
    for c in vecindad(objetivo):
        if W['occ'][c] > 0 and W['own'][c]:
            k = (-W['h'][c], c)
            if mejor is None or k < mejor[0]:
                mejor = (k, c)
    if mejor is None:
        return None
    return mejor[1], estado_idx(cfg, W['occ'][mejor[1]])


def bajar_ocupacion(W, cfg, i):
    """Quita a la celda i un escalon de ocupacion (las notas que hagan
    falta). Devuelve las notas quitadas."""
    o = W['occ'][i]
    k = 0
    antes, _CAUSA[0] = _CAUSA[0], 'catastrofe'     # fase 26: lo que borre, por catastrofe
    while o > 0 and W['occ'][i] >= o and k < 64:
        if not _undo_note(W, cfg, i):
            break
        k += 1
    _CAUSA[0] = antes
    return k


def bajar_estado(W, cfg, i, e0=None):
    """La formacion de la celda i baja de su estado e0 al anterior (una
    semilla se vacia). Devuelve las notas quitadas."""
    e0 = estado_idx(cfg, W['occ'][i]) if e0 is None else e0
    k = 0
    while W['occ'][i] > 0 and estado_idx(cfg, W['occ'][i]) >= e0:
        q = bajar_ocupacion(W, cfg, i)
        if q <= 0:
            break
        k += q
    return k


def _polvo(W, now, celda, modo, k):
    W['polvo'].append([now, int(celda), modo, int(k)])
    if len(W['polvo']) > POLVO_MAX:
        W['polvo'] = W['polvo'][-POLVO_MAX:]


def derribar(W, cfg, objetivo, now):
    """Las obras a medias de la vecindad del objetivo (la obra es de todo su
    cluster) se derriban: retroceden ya una etapa y siguen hacia atras.
    Devuelve las celdas que empiezan a derribarse."""
    cl = clusters(W, cfg)
    tf, tc = objetivos(W, cfg, cl)
    celdas = set()
    obras = obras_ciudad(W, cfg)        # fase 11 v10: un edificio a medias tambien
    for c in vecindad(objetivo):
        if W['occ'][c] > 0 and (0 < W['et_f'][c] < tf[c] or 0 < W['et_c'][c] < tc[c]):
            k = cl['de'][c]
            celdas.update(cl['celdas'][k] if k >= 0 else [c])
        elif W['occ'][c] > 0 and c in obras and W['obra'][c] > 0:
            celdas.add(c)
    nuevas = 0
    for x in sorted(celdas):
        nuevas += 0 if W['derribo'][x] else 1
        W['derribo'][x] = 1
        for clave in ('et_f', 'et_c'):
            if W[clave][x] > 0:
                _etapa(W, x, clave, W[clave][x] - 1, now)
        if x in obras and W['obra'][x] > 0:
            _paso_obra(W, x, W['obra'][x] - 1, now)
    return nuevas


def foco_catastrofe(W, cfg, i):
    """Donde seria la catastrofe de la celda i: su cluster y sus enlaces de
    la misma especie, tal como estan ahora."""
    cl = clusters(W, cfg)
    k = cl['de'][i]
    zona = sorted(cl['celdas'][k]) if k >= 0 else [i]
    enlaces = dict((c, [j for j in cl['mascara'][c] if W['own'][j] == W['own'][i]]) for c in zona)
    return dict(celda=i, own=W['own'][i], especie=especie_destructor(W, cfg, i),
                zona=zona, enlaces=enlaces)


def antes_del_golpe(W, cfg, objetivo, now):
    """Lo que ve un aranazo antes de hacer dano (fase 14): la victima, si el
    golpe escala (Golpesescalada golpes en la misma vecindad dentro de
    Ventanaescalada pasos; cada golpe escala una vez) y donde seria la
    catastrofe, con el cluster de antes del golpe. Y derriba ya las obras a
    medias que toca."""
    paso = W.get('paso') or 0.125
    ventana = max(1, int(cfg['ventana_escalada'])) * paso
    golpes = [g for g in W['golpes'] if 0 <= now - g[0] <= ventana] + [[now, objetivo]]
    zona = set(vecindad(objetivo))
    n_zona = sum(1 for g in golpes if g[1] in zona)
    escala = n_zona >= max(1, int(cfg['golpes_escalada']))
    W['golpes'] = [g for g in golpes if g[1] not in zona] if escala else golpes
    v = victima(W, cfg, objetivo)
    foco = foco_catastrofe(W, cfg, v[0]) if escala and v is not None else None
    return dict(victima=v, escala=escala, n_zona=n_zona, foco=foco,
                derribo=derribar(W, cfg, objetivo, now))


def destructor(W, cfg, pad, vel, now, ev, antes):
    """Tras la erosion de un aranazo (fase 14): el golpe que escala es la
    catastrofe; los demas, un accidente. 'antes' es lo que vio el golpe
    antes de hacer dano (antes_del_golpe)."""
    acc = None
    ev['escalada'] = None
    if antes['escala']:
        cat = iniciar_catastrofe(W, cfg, antes['foco'], vel, now) if antes['foco'] else None
        ev['escalada'] = cat['tipo'] if cat else None
    elif antes['victima'] is not None and W['own'][antes['victima'][0]]:
        v, e0 = antes['victima']
        esp = especie_destructor(W, cfg, v)
        if W['occ'][v] > 0 and estado_idx(cfg, W['occ'][v]) >= e0:
            ev['quitado'] += bajar_estado(W, cfg, v, e0)
        acc = dict(tipo=ACCIDENTE[esp], especie=esp, celda=v, t=now)
        if esp == 'vegetacion':
            _polvo(W, now, v, 'brasas', 6)
            _polvo(W, now, v, 'ceniza', 4)
        else:
            _polvo(W, now, v, 'polvo', 8)
    ev['accidente'] = acc
    ev['derribo'] = antes['derribo']
    W['ev']['destructor'] = dict(accidente=acc, escalada=ev['escalada'], celda=ev['celda'], t=now,
                                 golpes=0 if antes['escala'] else antes['n_zona'])
    W['dirty'] = True


def _activas(W):
    return sum(len(c['activas']) for c in W['cats'])


def _ruina(W, cat, c, now):
    W['ruina'][c] = 1 + RUINA_ESP.index(cat['especie'])
    W['t_ruina'][c] = now


def iniciar_catastrofe(W, cfg, foco, vel, now):
    """La catastrofe en el foco (foco_catastrofe). Empieza en su celda o, si
    el golpe la ha vaciado, en la mas alta que quede de su zona. Devuelve la
    catastrofe, o None si su zona ya tiene una en curso, no queda nada en
    pie o no queda sitio (Maxfuego)."""
    vivas = [c for c in foco['zona'] if W['occ'][c] > 0 and W['own'][c] == foco['own']]
    if not vivas:
        return None
    tipo = CATASTROFE.get(foco['especie'])          # fase 11 v11: Grisu y Apagon (pagina Fase14)
    if (tipo == 'explosion de grisu' and not cfg.get('grisu', 1)) or \
            (tipo == 'apagon en cadena' and not cfg.get('apagon', 1)):
        return None
    i = foco['celda'] if foco['celda'] in vivas else min(vivas, key=lambda c: (-W['h'][c], c))
    for c in W['cats']:
        if i in c['zona'] and c['activas']:
            return None
    tope = max(1, int(cfg['max_fuego']))
    if _activas(W) >= tope:
        return None
    esp, zona, enlaces = foco['especie'], foco['zona'], foco['enlaces']
    cat = dict(tipo=CATASTROFE[esp], especie=esp, own=foco['own'], origen=i, zona=zona,
               enlaces=enlaces, semilla=semilla_caos(vel, i), t=now, t0=now, k=0,
               activas={}, hechas=[], vacias=0, quitado=0, grande=False)
    inicio = [i]
    if occupied(W) / float(N) > cfg['dens_umbral']:   # presupuesto: el mundo lleno arde mas
        cat['grande'] = True
        inicio += [j for j in enlaces.get(i, []) if W['occ'][j] > 0]
    inicio = inicio[:max(1, tope - _activas(W))]
    W['ev']['catastrofe'] = dict(tipo=cat['tipo'], celda=i, celdas=len(inicio), grande=cat['grande'], t=now)
    W['dirty'] = True
    if cat['tipo'] == 'implosion':                 # cae entera de golpe, con polvo
        for c in inicio:
            while W['occ'][c] > 0 and bajar_ocupacion(W, cfg, c) > 0:
                pass
            _ruina(W, cat, c, now)
            _polvo(W, now, c, 'polvo', 14)
        cat['hechas'], cat['vacias'] = list(inicio), len(inicio)
        return cat
    for c in inicio:
        cat['activas'][c] = 0
    W['cats'].append(cat)
    return cat


def _salto(cfg, cat, b, j):
    """El mapa logistico decide si el fuego salta de b a j en este paso."""
    x0 = (cat['semilla'] + 0.6180339887 * cat['k'] + 0.3819660113 * j + 0.2134 * b) % 1.0
    return logistica(0.05 + 0.9 * x0, cfg['caos'], 1)[0]


def paso_catastrofe(W, cfg, cat, now):
    """Un paso: cada celda activa salta a sus vecinas del cluster (si el
    mapa logistico lo dice y queda sitio) y pierde 1 de ocupacion; se apaga
    sin ocupacion (y deja su huella) o a los Pasosfuego pasos."""
    cat['k'] += 1
    tope = max(1, int(cfg['max_fuego']))
    nuevas = []
    for b in sorted(cat['activas']):
        for j in cat['enlaces'].get(b, []):
            if j in cat['activas'] or j in cat['hechas'] or j in nuevas:
                continue
            if W['occ'][j] <= 0 or W['own'][j] != cat['own']:
                continue
            if _activas(W) + len(nuevas) >= tope:
                break
            if _salto(cfg, cat, b, j) > SALTO:
                nuevas.append(j)
    pasos = max(1, int(cfg['pasos_fuego']))
    fuego = cat['tipo'] == 'incendio'
    for b in sorted(cat['activas']):
        cat['quitado'] += bajar_ocupacion(W, cfg, b)
        cat['activas'][b] += 1
        if W['occ'][b] <= 0 or cat['activas'][b] >= pasos:
            del cat['activas'][b]
            cat['hechas'].append(b)
            if W['occ'][b] <= 0:
                _ruina(W, cat, b, now)
                cat['vacias'] += 1
            _polvo(W, now, b, 'ceniza' if fuego else 'polvo', 5 if fuego else 8)
    for j in nuevas:
        cat['activas'][j] = 0
    W['dirty'] = True


def tick_destructores(W, cfg, now):
    """Avanza las catastrofes un paso cada paso y olvida lo que ya paso."""
    paso = W.get('paso') or 0.125
    if W['cats']:
        for cat in W['cats']:
            n = 0
            while cat['activas'] and now - cat['t'] >= paso - 1e-9 and n < 32:
                cat['t'] += paso
                paso_catastrofe(W, cfg, cat, now)
                n += 1
            if now - cat['t'] >= paso or now < cat['t'] - paso:    # el tiempo ha saltado
                cat['t'] = now
        fin = [c for c in W['cats'] if not c['activas']]
        if fin:
            W['ev']['catastrofe_fin'] = dict(tipo=fin[-1]['tipo'], celdas=len(fin[-1]['hechas']),
                                             vacias=fin[-1]['vacias'], t=now)
            W['cats'] = [c for c in W['cats'] if c['activas']]
    if W['polvo']:
        vida = max(1, int(cfg['pasos_polvo'])) * paso
        W['polvo'] = [p for p in W['polvo'] if now - p[0] < vida]
    if W['golpes']:
        ventana = max(1, int(cfg['ventana_escalada'])) * paso
        W['golpes'] = [g for g in W['golpes'] if now - g[0] <= ventana]


def apagar_destructores(W):
    """Fin de ciclo: se apagan los fuegos, se asienta el polvo, no queda
    ninguna obra derribandose y las huellas quedan enterradas con el mundo."""
    W['cats'] = []
    W['golpes'] = []
    W['polvo'] = []
    W['ruina'] = [0] * N
    W['derribo'] = [0] * N
    W['cortes'] = []                    # fase 16: la galeria de metro queda enterrada
    W['uniones'] = []


def _quemar(col, q, chispa):
    """Color de lo que arde: se carboniza con lo que ha ardido (q, 0-1) y
    brilla de brasa a saltos (chispa, 0 o 1)."""
    return _mix(_mix(col, COL_CARBON, 0.6 * q), COL_BRASA, 0.18 + 0.22 * chispa)


def celdas_ardiendo(W, cfg):
    """{celda: cuanto ha ardido (0-1)} de los incendios en curso."""
    out = {}
    pasos = float(max(1, int(cfg['pasos_fuego'])))
    for cat in W['cats']:
        if cat['tipo'] == 'incendio':
            for c, q in cat['activas'].items():
                out[c] = min(1.0, (q + 1) / pasos)
    return out


def _sitio(W, cfg, c):
    base = base_radius(W, cfg, c)
    n = normal_i(c)
    cw, cl_ = _cell_sizes(base, c)
    return n, _mul(n, base), cw, cl_


def build_destructores(W, cfg, now, out):
    """Las huellas (el modelo de huella de su especie en cada celda vacia que
    la tiene) y las particulas: brasas y ceniza de lo que arde, polvo de los
    derrumbes, y las nubes de los accidentes, que se disipan en Pasospolvo."""
    tema = tema_de(cfg)
    lim = limit(cfg)
    paso = W.get('paso') or 0.125
    doce = cfg['nivel'] >= 12
    respaldo = doce and cfg.get('respaldo', 0)
    for i in range(N):
        r = W['ruina'][i]
        if not r or W['occ'][i] > 0:
            continue
        esp = RUINA_ESP[r - 1]
        if TEMA_DE_ESP.get(esp) != tema:
            continue                        # los modelos del otro tema no se dibujan
        mo = (modelos_de(cfg, tema, esp, 'huella') or [None])[0]
        if mo is None:
            continue
        n, p0, cw, cl_ = _sitio(W, cfg, i)
        dims = _pie(mo, RUINA_ALTO[esp] * lim, cw, cl_)
        fila = _fila_m(p0, _marco(i), dims[0], dims[1], dims[2], COL_RUINA[esp])
        if doce:
            fila.append(1.0 if respaldo else 0.95)
        out.setdefault(geometria_de(mo, False, not doce), []).append(fila)
    parts = out.setdefault('particulas', [])
    for cat in W['cats']:
        fuego = cat['tipo'] == 'incendio'
        for c in sorted(cat['activas']):
            n, p0, cw, cl_ = _sitio(W, cfg, c)
            vh = max(W['vh'][c], 0.3 * lim)
            if fuego:
                _particulas(parts, n, p0, cw, cl_, vh, semilla_caos(c, 5), 6, COL_BRASA, now, paso, 'brasas')
                _particulas(parts, n, p0, cw, cl_, vh, semilla_caos(c, 9), 4, COL_CENIZA, now, paso, 'ceniza')
            else:
                _particulas(parts, n, p0, cw, cl_, vh, semilla_caos(c, 13), 8, COL_POLVO, now, paso, 'polvo')
    vida = max(1, int(cfg['pasos_polvo'])) * paso
    for t0, c, modo, k in W['polvo']:
        q = (now - t0) / vida
        if not 0.0 <= q < 1.0 or not 0 <= c < N:
            continue
        n, p0, cw, cl_ = _sitio(W, cfg, c)
        col = COL_BRASA if modo == 'brasas' else COL_CENIZA if modo == 'ceniza' else COL_POLVO
        _particulas(parts, n, p0, cw, cl_, max(W['vh'][c], 0.3 * lim), semilla_caos(c + int(t0 * 7.0), 17),
                    k, col, now, paso, modo, escala=1.0 - q)


# -----------------------------------------------------------------------------
# 1. NUCLEO - el ciclo como era (fase 15): entierro tematico, registro y herencia
# -----------------------------------------------------------------------------
# Cada fin de ciclo entierra el mundo con la materia de su tema. En la concha
# quedan las losetas de lo que hubo: veta de carbon (negro brillante) donde
# hubo bosque y basalto donde hubo relieve; hormigon gris en la ciudad, con la
# traza de sus calles (las celdas por las que pasaban sus carreteras, mas
# oscuras). Las celdas vacias conservan el color de su generacion (fase 8), y
# la materia se mezcla con el sin taparlo del todo.
# Cada concha guarda su registro: tema, especie, estado y cluster de cada
# celda, y sus carreteras, calles y rios. Lo leeran los cortes de la fase 16;
# mientras nada se exponga, no cuesta nada.
# La herencia rebrota segun su logica. Naturaleza: banco de semillas; lo
# heredado espera como semillas sobre el suelo y brota a saltos (cadena de
# rebrote: semillas -> brotes, 2 x Pasosetapa pasos por etapa), o de golpe con
# una nota en su celda. Ciudad: trazas; la red de carreteras nueva prefiere
# los tramos de la ciudad enterrada (Pesotraza).
# Con Temaenciclo, un cambio de Tema espera al siguiente fin de ciclo: cada
# concha tiene un solo tema, y cambiarlo entre ciclos deja bosques fosiles
# bajo ciudades, o ciudades bajo bosques.

COL_SEMILLA = (0.62, 0.50, 0.28)
CARBON = (0.03, 0.03, 0.04)
BASALTO = (0.19, 0.20, 0.23)
HORMIGON = (0.56, 0.55, 0.52)
CALLE = (0.11, 0.11, 0.12)
# especie: (materia, rugosidad, cuanto pesa sobre el color de la generacion)
ESCORIA = (0.22, 0.20, 0.21)             # fase 11 v11: la veta de escoria y chatarra de la industria
MATERIA = dict(vegetacion=(CARBON, 0.06, 0.85), relieve=(BASALTO, 0.5, 0.6),
               informal=(HORMIGON, 0.85, 0.6), planificada=(HORMIGON, 0.85, 0.6),
               mina=(ESCORIA, 0.35, 0.75), energia=(ESCORIA, 0.6, 0.6), refineria=(ESCORIA, 0.3, 0.8))
MATERIA_TEMA = dict(naturaleza='carbon y basalto', ciudad='hormigon', industria='escoria y chatarra')
RUG_LOSETA, RUG_ZOCALO = 0.7, 0.9


def registro_concha(W, cfg):
    """El registro de la concha que se entierra: tema, y por celda especie
    (1 + indice en RUINA_ESP; 0 vacia), estado y cluster (-1 ninguno); y las
    carreteras, las calles (celdas por las que pasan) y los rios."""
    tema = tema_de(cfg)
    cl = clusters(W, cfg)
    esp, est, clu, tipo = [0] * N, [-1] * N, [-1] * N, [''] * N
    for i in range(N):
        if W['occ'][i] > 0 and W['own'][i]:
            esp[i] = 1 + RUINA_ESP.index(especie_de(tema, W['own'][i]))
            est[i] = estado_idx(cfg, W['occ'][i])
            clu[i] = cl['de'][i]
            if tema in CONSTRUIDOS and cfg['nivel'] >= 11:     # fase 11 v10: la tipologia de cada celda
                tipo[i] = diseno_celda(W, cfg, i)[0]
    t = tejido(W, cfg) if cfg['nivel'] >= 13 else {}
    vias = sorted([min(a, b), max(a, b)] for a, b in t.get('vias', []))
    return dict(tema=tema, esp=esp, estado=est, cluster=clu, tipo=tipo, vias=vias,
                epoca=epoca_actual(cfg, W) if tema == 'industria' else None,
                calles=sorted(set(x for v in vias for x in v)), rios=[list(r) for r in t.get('rios', [])])


def herencia_tematica(W, cfg, now, reg):
    """Lo heredado, segun el tema del mundo nuevo: en naturaleza, banco de
    semillas (rebrote); en la ciudad, las trazas de la ciudad enterrada."""
    nuevo = TEMAS[int(cfg.get('tema_pendiente', cfg['tema'])) % len(TEMAS)]
    W['rebrote'] = [0] * N
    W['t_rebrote'] = [-99.0] * N
    W['trazas'] = []
    if nuevo == 'naturaleza' and cfg.get('rebrote', 1):
        for i in range(N):
            if W['occ'][i] > 0:
                W['rebrote'][i] = 1
                W['t_rebrote'][i] = now
    if nuevo in CONSTRUIDOS and reg['tema'] == nuevo:      # carreteras o vias (fase 11 v11)
        W['trazas'] = [list(v) for v in reg['vias']]


def rebrote_dur(cfg, paso):
    """Lo que dura cada etapa del rebrote."""
    return 2.0 * max(1, int(cfg['pasos_etapa'])) * paso


def tick_rebrote(W, cfg, now):
    """Las semillas brotan y los brotes acaban de crecer, etapa a etapa."""
    if not any(W['rebrote']):
        return
    dur = rebrote_dur(cfg, W.get('paso') or 0.125)
    for i in range(N):
        e = W['rebrote'][i]
        if not e:
            continue
        if W['occ'][i] <= 0:
            W['rebrote'][i] = 0
        elif now - W['t_rebrote'][i] >= dur - 1e-9:
            W['rebrote'][i] = 2 if e == 1 else 0
            W['t_rebrote'][i] = now
            W['dirty'] = True


def tile_material(cfg, sh, s, c):
    """(color, rugosidad) de la loseta de la celda c en la concha sh. Las
    conchas con registro (fase 15) llevan la materia de su tema sobre el color
    de su generacion; las demas, el color de la fase 8."""
    col = tile_color(cfg, sh, sh['occ'][c], s)
    tema = sh.get('tema')
    if tema is None:
        return col, RUG_LOSETA
    rug = RUG_LOSETA
    e = sh['esp'][c]
    if e:
        mat, rug, k = MATERIA[RUINA_ESP[e - 1]]
        col = _mix(col, mat, k)
    elif tema == 'ciudad':                  # el suelo de la ciudad tambien es hormigon
        col, rug = _mix(col, HORMIGON, 0.3), MATERIA['informal'][1]
    elif tema == 'industria':               # y el de la industria, escoria
        col, rug = _mix(col, ESCORIA, 0.3), MATERIA['energia'][1]
    if tema in CONSTRUIDOS and c in sh.get('calles', ()):
        col, rug = _mix(col, CALLE, 0.7), 0.7
    return col, rug


# -----------------------------------------------------------------------------
# 1. NUCLEO - arqueologia tematica (fase 16): lo que ensenan los cortes
# -----------------------------------------------------------------------------
# Los cortes de la fase 9 dejan de ensenar solo bandas de color: en el fondo y
# en las paredes de cada corte aparece lo que hubo en cada concha, leido de su
# registro (fase 15). Naturaleza: en la veta de carbon, troncos fosiles
# aplastados en horizontal (donde hubo bosque) y columnas de basalto (donde
# hubo relieve). Ciudad: cimientos (informal), sotanos (planificada) y tramos
# de calle con su colector (las celdas por las que pasaban sus carreteras).
# Solo dentro del corte: las celdas con el suelo por debajo del radio nominal
# (el corte y su anfiteatro), en su fondo y en las paredes de sus vecinas mas
# altas; como mucho Detalleexpuesto piezas por celda, una por era antes de
# repetir. La cicatriz manda: lo recien expuesto sale cian, en los dos temas.
# Una concha sin registro (enterrada antes de la fase 15) solo ensena su color.
# Escalada: dos cortes en la misma vecindad (el objetivo del segundo dentro del
# primero o en su borde) dentro de Ventanaescalada pasos se unen por el camino
# mas corto (Unircortes). En naturaleza, un canon: las celdas del camino se
# cortan con la profundidad del menor de los dos. En la ciudad, una galeria de
# metro a cielo abierto (falso tunel): una zanja de una loseta con la boveda de
# la galeria dentro. Cada corte se une una vez; la galeria se entierra con su
# mundo y el canon queda como hondonada.

COL_EXPUESTO = dict(vegetacion=(0.62, 0.55, 0.44),      # fosil: piedra clara sobre el carbon
                    relieve=(0.27, 0.28, 0.32),          # columnas de basalto
                    informal=(0.60, 0.58, 0.54), planificada=(0.52, 0.52, 0.50),
                    calle=(0.24, 0.24, 0.25), mina=(0.40, 0.30, 0.20), energia=(0.50, 0.46, 0.42),
                    refineria=(0.30, 0.28, 0.27))
RUG_EXPUESTO = dict(vegetacion=0.35, relieve=0.4, informal=0.85, planificada=0.8, calle=0.7, mina=0.8,
                    energia=0.8, refineria=0.6)
COL_GALERIA, RUG_GALERIA = (0.58, 0.57, 0.53), 0.8
NOMBRE_ERA = dict(vegetacion='carbon', relieve='basalto', informal='ruinas', planificada='ruinas',
                  calle='calles', mina='galerias', energia='escoria', refineria='escoria')
PRIORIDAD_ERA = ['vegetacion', 'planificada', 'informal', 'relieve', 'mina', 'refineria', 'energia', 'calle']
UNION_NOMBRE = dict(canon='canon', galeria='galeria de metro')


def contenido(sh, c):
    """Lo que guarda la concha sh en la celda c: su especie, 'calle' (una
    celda de la ciudad por la que pasaba una carretera) o None."""
    if sh.get('tema') is None:
        return None
    e = sh['esp'][c]
    if e:
        return RUINA_ESP[e - 1]
    if sh['tema'] in ('ciudad', 'industria') and c in sh.get('calles', ()):
        return 'calle'
    return None


def en_corte(W, cfg, c, R=None):
    """La celda c esta dentro de un corte: su suelo, por debajo del radio nominal."""
    if cfg['nivel'] >= 29 and es_escision(W, c):    # fase 29: una escision no es un corte (sin fosiles)
        return False
    R = top_radius(W, cfg) if R is None else R
    return R - suelo(W, cfg, c) > 1e-6


def exposicion(W, cfg, c):
    """Lo que deja ver el corte en la celda c: [(concha, celda de la loseta,
    vecina, r0, r1)]. Primero el fondo (vecina -1: la loseta superior de su
    columna); despues las paredes, las losetas de las vecinas mas altas entre
    su suelo y el de c (r0-r1, la banda que queda al aire), de arriba abajo."""
    s0 = suelo(W, cfg, c)
    out = []
    col = column_radii(W, cfg, c)
    if col:
        s, r_in, r_out = col[-1]
        out.append((s, c, -1, r_in, r_out))
    paredes = []
    for j in sorted(NEIGH[c]):
        sj = suelo(W, cfg, j)
        if sj <= s0 + 1e-6:
            continue
        for s, r_in, r_out in column_radii(W, cfg, j):
            a, b = max(r_in, s0), min(r_out, sj)
            if b - a > 1e-6:
                paredes.append((s, j, j, a, b))
    paredes.sort(key=lambda x: (-x[4], x[2]))
    return out + paredes


CIMIENTO_TIPO = dict(pilotis='arq_pilotes', lamina='arq_pilotes')    # los demas planificados, sotano


def cimiento_de(sh, x, q):
    """Fase 11 v10: lo que ensena el corte bajo cada tipo de la ciudad (el registro
    de la concha guarda la tipologia): pilotes bajo los pilotis, sotanos bajo el
    podio y los bloques, zapatas bajo las casas. None si no hay registro."""
    tipos = sh.get('tipo')
    if sh.get('tema') != 'ciudad' or not tipos or x >= len(tipos) or not tipos[x]:
        return None
    d = tipos[x]
    if d in INFORMALES or q == 'informal':
        return 'arq_cimientos'
    return CIMIENTO_TIPO.get(d, 'arq_sotano')


def piezas_expuestas(W, cfg, c):
    """Las piezas del corte en la celda c, hasta Detalleexpuesto: lo de la
    exposicion que tiene contenido, el fondo primero y una por era antes de
    repetir. [(concha, celda, vecina, r0, r1, contenido)]."""
    tope = max(0, int(cfg['detalle_expuesto']))
    if tope <= 0:
        return []
    cand = []
    for s, x, j, a, b in exposicion(W, cfg, c):
        if 0 <= s < len(W['shells']):
            q = contenido(W['shells'][s], x)
            if q:
                cand.append((s, x, j, a, b, q))
    fondo = [p for p in cand if p[2] < 0]
    vistas = {}
    paredes = []
    for p in cand:
        if p[2] >= 0:
            k = vistas.get(p[0], 0)
            vistas[p[0]] = k + 1
            paredes.append((k, len(paredes), p))
    paredes.sort(key=lambda x: (x[0], x[1]))
    return (fondo + [p for _, _, p in paredes])[:tope]


def eras_expuestas(W, cfg, celdas):
    """[(concha, nombre)] de las eras que ensena el corte en esas celdas, de
    arriba abajo: carbon, basalto, ruinas o calles (lo que mas pesa de lo
    expuesto), o estrato si no guarda nada."""
    expo = [p for c in celdas if en_corte(W, cfg, c) for p in exposicion(W, cfg, c)]
    por_concha = {}
    orden = []
    for s, x, j, a, b in sorted(expo, key=lambda p: (-p[4], p[0])):
        if not 0 <= s < len(W['shells']):
            continue
        if s not in por_concha:
            por_concha[s] = set()
            orden.append(s)
        q = contenido(W['shells'][s], x)
        if q:
            por_concha[s].add(q)
    out = []
    for s in orden:
        q = next((k for k in PRIORIDAD_ERA if k in por_concha[s]), None)
        out.append((s, NOMBRE_ERA[q] if q else 'estrato'))
    return out


def zona_corte(objetivo, rad):
    """El corte y su borde: las celdas a distancia <= radio + 1 del objetivo."""
    return set(c for c, _ in rings(objetivo, int(rad) + 1))


def unir_cortes(W, cfg, objetivo, depth, rad, now):
    """La escalada de los cortes: si un corte reciente (dentro de
    Ventanaescalada pasos) tiene este objetivo en su zona, los dos se unen.
    Devuelve la union o None."""
    paso = W.get('paso') or 0.125
    ventana = max(1, int(cfg['ventana_escalada'])) * paso
    recientes = [k for k in W['cortes'] if 0 <= now - k[0] <= ventana]
    union = None
    if cfg.get('unir_cortes', 1):
        for k in reversed(recientes):
            t0, a, d0, r0 = k
            if a != objetivo and objetivo in zona_corte(a, r0):
                union = abrir_union(W, cfg, a, objetivo, min(int(d0), int(depth)), now)
                recientes.remove(k)                 # cada corte se une una vez
                break
    W['cortes'] = recientes if union else recientes + [[now, int(objetivo), int(depth), int(rad)]]
    return union


def abrir_union(W, cfg, a, b, depth, now):
    """Une los cortes de a y b por el camino mas corto: canon en naturaleza
    (el camino se corta con la profundidad del menor), galeria de metro en la
    ciudad (una zanja de una loseta con su boveda)."""
    galeria = tema_de(cfg) in CONSTRUIDOS
    camino = camino_corto(a, b)
    prof = 1 if galeria else max(1, int(depth))
    for c in camino[1:-1]:
        cut(W, cfg, c, prof, 0, now)
    u = dict(tipo='galeria' if galeria else 'canon', celdas=camino, t=now, prof=prof)
    W['uniones'] = (W['uniones'] + [u])[-8:]
    W['ev']['union'] = u
    return u


def corte_tematico(W, cfg, objetivo, depth, rad, now):
    """El corte de la fase 9 y, desde la 16, su union con un corte reciente.
    La leyenda CORTE sigue hablando del corte del golpe."""
    fuera = cut(W, cfg, objetivo, depth, rad, now)
    ev = W['ev'].get('corte')
    union = unir_cortes(W, cfg, objetivo, depth, rad, now)
    if ev is not None:
        ev['union'] = union
        W['ev']['corte'] = ev
    return fuera, union


def _marco_pared(c, j):
    """(desplazamiento, marco) de una pieza en la pared de la columna de j que
    da a la celda c: el desplazamiento, del eje de j a la cara (a radio 1,
    se escala con el radio); el marco, Y la normal de j, Z hacia fuera de la
    pared y X a lo largo. Tambien el ancho de la cara (a radio 1)."""
    clave = (GRID['lo'], GRID['hi'], c, 'pared', j)
    v = _MARCOS.get(clave)
    if v is None:
        nj = normal_i(j)
        cw, cl = _cell_sizes(1.0, j)
        if is_pole(j):
            cw, cl = cw * 1.25, cl * 1.25
        hw, hl = 0.52 * cw, 0.52 * cl               # la loseta mide 1,04 x la celda
        e, t = tangents(nj)
        d = _hacia(nj, nj, normal_i(c))
        dx, dz = _dot(d, e), _dot(d, t)
        kx = hw / abs(dx) if abs(dx) > 1e-9 else 1e9
        kz = hl / abs(dz) if abs(dz) > 1e-9 else 1e9
        if kx <= kz:
            off, Z, ancho = _mul(d, kx), _mul(e, 1.0 if dx > 0 else -1.0), 2.0 * hl
        else:
            off, Z, ancho = _mul(d, kz), _mul(t, 1.0 if dz > 0 else -1.0), 2.0 * hw
        X = _cross(nj, Z)
        v = _MARCOS[clave] = (off, (X, nj, Z, _euler_xyz(X, nj, Z)), ancho)
    return v


def _variante(lista, s, x, j):
    """Una variante del catalogo, del mapa logistico sembrado con la concha y
    la celda (sin azar)."""
    if not lista:
        return None, 0.0
    v = logistica(semilla_caos(s + 1, x * 7 + j + 1), 3.91, 1)[0]
    return lista[int(v * len(lista)) % len(lista)], v


_ARQ = {}


def _firma_arq(W, cfg):
    """Lo que decide las piezas expuestas (motor v101): la columna de cada celda
    (su suelo y lo que ensena cada corte), las conchas, las uniones (galerias), las
    escisiones (fase 29: no son cortes), las cicatrices y la configuracion que leen
    modelos_de y cimiento_de."""
    return (id(W), GRID['lo'], GRID['hi'], cfg['nivel'], tema_de(cfg), cfg.get('detalle_expuesto'),
            cfg.get('respaldo', 0), cfg['core_radius'], cfg.get('shell_thick'), id(cfg.get('catalogo')),
            len(W['shells']), tuple(tuple(map(tuple, col)) for col in W['cols']),
            tuple((u['tipo'], tuple(u['celdas'])) for u in W['uniones']),
            tuple(sorted(W.get('esc_celdas', {}))) if cfg['nivel'] >= 29 else (),
            tuple(sorted(W['scars'].items())))       # una cicatriz que sale cambia el color (exacto)


def build_arqueologia(W, cfg, now, out):
    """Las piezas expuestas en los cortes y las galerias de metro. Con Cachearq
    (motor v101) guarda sus filas y solo las rehace cuando cambia lo que ensenan
    los cortes (_firma_arq) o mientras alguna cicatriz se esta fundiendo (el color
    pasa del cian al mineral); cuando todas han terminado, una ultima vez con el
    color final. Con la firma igual, las mismas filas: el Script CHOP no se recuece."""
    if not cfg.get('cache_arq', 1):
        _ARQ.clear()
        return _build_arqueologia(W, cfg, now, out)
    st = max(1e-6, cfg['scar_time'])
    vivas = any(0.0 <= now - t0 < st for t0 in W['scars'].values())
    firma = _firma_arq(W, cfg)
    v = _ARQ.get('v')
    if v is not None and v['firma'] == firma and not vivas and not v['vivas']:
        for g, f in v['filas'].items():
            out.setdefault(g, []).extend(f)
        W['arqueo'] = dict(v['arqueo'])
        _ARQ['cache'] = True
        return
    filas = {}
    _build_arqueologia(W, cfg, now, filas)
    for g, f in filas.items():
        out.setdefault(g, []).extend(f)
    _ARQ['v'] = dict(firma=firma, vivas=vivas, filas=filas, arqueo=dict(W['arqueo']))
    _ARQ['cache'] = False


def _build_arqueologia(W, cfg, now, out):
    """Las piezas expuestas en los cortes y las galerias de metro (sin la cache)."""
    doce = cfg['nivel'] >= 12
    respaldo = doce and cfg.get('respaldo', 0)
    st = max(1e-6, cfg['scar_time'])
    R = top_radius(W, cfg)
    n_piezas = n_celdas = 0

    def emit(mo, p, marco, dims, col, rug):
        fila = _fila_m(p, marco, dims[0], dims[1], dims[2], col)
        if doce:
            fila.append(1.0 if respaldo else rug)
        out.setdefault(geometria_de(mo, False, not doce), []).append(fila)

    for c in range(N):
        if not en_corte(W, cfg, c, R):
            continue
        piezas = piezas_expuestas(W, cfg, c)
        if piezas:
            n_celdas += 1
        for s, x, j, a, b, q in piezas:
            sh = W['shells'][s]
            tema = sh['tema']
            col = COL_EXPUESTO.get(q, COL_EXPUESTO['planificada'])
            if tema == 'industria' and sh.get('epoca') is not None:    # la epoca de esa concha
                col = _mix(col, PALETA_CIUDAD[PALETA_IND + int(sh['epoca'])][0], 0.45)
            t0 = W['scars'].get(s * 1000 + x)
            if t0 is not None:                  # la cicatriz manda
                col = _mix(COL_SCAR, col, max(0.0, min(1.0, (now - t0) / st)))
            th = b - a
            if j < 0:                           # en el fondo: medio enterrada
                mo, v = _variante(modelos_de(cfg, tema, q, 'fondo'), s, x, -1)
                mo = cimiento_de(sh, x, q) or mo     # fase 11 v10: los cimientos de cada tipo
                if mo is None:
                    continue
                n = normal_i(c)
                cw, cl_ = _cell_sizes(b, c)
                h = 0.5 * min(th, 0.8)
                giro = 30.0 * int(v * 6)
                emit(mo, _mul(n, b - 0.5 * h), _marco(c, giro), (0.55 * cw, h, 0.55 * cl_), col,
                     RUG_EXPUESTO.get(q, 0.8))
            else:                               # en la pared, asomando al corte
                mo, v = _variante(modelos_de(cfg, tema, q, 'expuesto'), s, x, j)
                mo = cimiento_de(sh, x, q) or mo
                if mo is None:
                    continue
                cols = column_radii(W, cfg, j)
                r_mid = next((0.5 * (ri + ro) for s_, ri, ro in cols if s_ == s), 0.5 * (a + b))
                off, marco, ancho = _marco_pared(c, j)
                ancho *= r_mid
                prof = min(0.3, 0.25 * ancho)
                y0 = a + 0.1 * th
                p = _add(_add(_mul(marco[1], y0), off, r_mid), marco[2], 0.1 * prof)
                emit(mo, p, marco, (0.7 * ancho, 0.8 * th, prof), col, RUG_EXPUESTO.get(q, 0.8))
            n_piezas += 1
    galerias = 0
    for u in W['uniones']:
        if u['tipo'] != 'galeria':
            continue
        cam = u['celdas']
        medio = cam[1:-1]
        g_r = min(suelo(W, cfg, x) for x in medio) if medio else max(suelo(W, cfg, x) for x in cam)
        alto = max(0.05, 0.9 * (R - g_r)) if R - g_r > 0.05 else 0.05
        mo = (modelos_de(cfg, 'ciudad', 'galeria', 'union') or [None])[0]
        if mo is None:
            continue
        for k in range(len(cam) - 1):
            i, j = cam[k], cam[k + 1]
            fin_i, fin_j = k == 0 and medio, k == len(cam) - 2 and medio
            if fin_i:                           # media galeria, de la zanja a la excavacion
                i, j = j, i
            pi, pj = _mul(normal_i(i), g_r), _mul(normal_i(j), g_r)
            largo = math.sqrt(sum((pi[q] - pj[q]) ** 2 for q in range(3)))
            if fin_i or fin_j:
                largo *= 0.5
            cw, cl_ = _cell_sizes(g_r, i)
            emit(mo, pi, _marco_puente(i, j), (0.4 * min(cw, cl_), alto, largo), COL_GALERIA, RUG_GALERIA)
            galerias += 1
    W['arqueo'] = dict(piezas=n_piezas, celdas=n_celdas, galerias=galerias)


# -----------------------------------------------------------------------------
# 1. NUCLEO - el tiempo en el paisaje (fase 17): pulso, transporte y frente
# -----------------------------------------------------------------------------
# Las senales de tiempo dejan de ser solo reloj y se ven en el paisaje.
# PULSO: un contador de beats que avanza con el tempo y se pone a 0 con el START
# del BeatStep (o sigue a master_beat, si Masterbeat lo senala). Todo lo que
# respira va en fase con el: naturaleza, el dosel se balancea (Swaymax grados,
# un vaiven cada dos beats) y las esporas derivan sobre los bosques; ciudad,
# puntos de trafico por las carreteras de la fase 13 (Trafico por tramo, un
# tramo cada dos beats: con mas BPM, mas deprisa) y ventanas que parpadean.
# A saltos de stop-motion, como los transitos.
# TRANSPORTE: con la linea de tiempo parada o tras un STOP, el pulso se congela:
# el mundo queda quieto pero visible. PLAY (o START) lo reanuda.
# FRENTE: un cambio de pattern (el aviso de la fase 6, o Frenteprueba) lanza
# una banda de polo sur a polo norte en Pasosfrente pasos. Naturaleza: un
# frente meteorologico, una banda de nubes que dobla los arboles a su paso y
# tine la luz. Ciudad: una ola de ventanas que se encienden o se apagan.
# BIBLIOTECA: cada pattern deja su firma (las notas de un compas de cada
# secuenciador) y su estacion (tinte de la luz y ventanas). A mitad del frente,
# lo que ya ha sonado del pattern nuevo se compara con la biblioteca: si lo
# reconoce, el frente devuelve el tinte que tuvo la ultima vez (la estacion que
# vuelve); si no, estrena uno. Sin azar: el tinte del pattern n sale del angulo
# aureo, como la paleta de las conchas.

SWAY_BEATS = 2.0            # un vaiven del dosel cada dos beats
TRAFICO_BEATS = 2.0         # un tramo de carretera cada dos beats
FRENTE_ANCHO = 22.0         # grados de latitud de la banda
FRENTE_INCL = 24.0          # lo que dobla los arboles al pasar
FRENTE_NUBES = 44           # nubes de la banda
RECONOCER = 0.8             # parecido minimo (coseno) para reconocer un pattern
TINTE_C = 0.07              # croma del tinte de una estacion
LUZ_BASE = (0.82, 0.90, 1.00)   # la luz cenital fria de la fase 10, sin tenir
COL_FARO, COL_PILOTO = (1.0, 0.90, 0.68), (0.95, 0.22, 0.14)
COL_ESPORA, COL_NUBE = (0.80, 0.86, 0.62), (0.80, 0.82, 0.86)
COL_SMOG = (0.42, 0.39, 0.34)


def pulso_tick(W, cfg, dt, tempo, playing):
    """Avanza el pulso (en beats). Parado si la linea de tiempo no corre o si
    el ultimo mensaje de transporte fue un STOP."""
    p = W['pulso']
    ck = W['clock']
    p['parado'] = (not playing) or ck['stop_t'] > ck['start_t'] or not tempo or tempo <= 0
    if p['parado']:
        return
    mb = cfg.get('master_beat')
    if mb is None:
        p['beat'] += dt * tempo / 60.0
    elif abs(mb - round(mb)) > 1e-3:            # master_beat con fraccion: manda tal cual
        p['beat'] = float(mb)
    else:                                       # cuenta beats enteros: la fraccion, con el tempo
        if mb != p.get('mb'):
            p['mb'], p['frac'] = mb, 0.0
        p['frac'] = min(0.999, p.get('frac', 0.0) + dt * tempo / 60.0)
        p['beat'] = float(mb) + p['frac']


def beat_stop(W, cfg):
    """El pulso a saltos de stop-motion (FOTOS_PASO por paso)."""
    k = max(1, int(cfg['steps_per_beat'])) * FOTOS_PASO
    return math.floor(W['pulso']['beat'] * k) / k


def oir(W, s, nota):
    """Una nota de los SEQ, para la firma del pattern (los ultimos dos compases)."""
    b = W['pulso']['beat']
    W['oido'] = [x for x in W['oido'] if 0.0 <= b - x[0] <= 8.0] + [[b, int(s), int(nota)]]


def firma(notas):
    """{'s:nota': veces} de unas notas [beat, s, nota]."""
    out = {}
    for _, s, n in notas:
        k = '%d:%d' % (s, n)
        out[k] = out.get(k, 0) + 1
    return out


def parecido(a, b):
    """Coseno entre dos firmas (0 si alguna esta vacia)."""
    if not a or not b:
        return 0.0
    num = sum(v * b.get(k, 0) for k, v in a.items())
    den = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
    return num / den if den > 0 else 0.0


def nombre_pattern(n):
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return letras[n % 26] + ('' if n < 26 else str(n // 26))


def tinte_estacion(n):
    """El tinte de la luz del pattern n: el primero, ninguno; los demas, tonos
    por el angulo aureo (los de la paleta), normalizados a 1."""
    if n == 0:
        return [1.0, 1.0, 1.0]
    rgb = oklch_to_srgb(0.9, TINTE_C, palette_hue(n, 40.0))[0]
    m = max(rgb) or 1.0
    return [round(x / m, 4) for x in rgb]


def _patron(W, nombre):
    return next((p for p in W['patrones'] if p['nombre'] == nombre), None)


def _bpb(cfg):
    return max(1, int(cfg['beats_per_bar']))


def cambio_pattern(W, cfg):
    """Un cambio de pattern: la firma del que se va (su ultimo compas) queda en
    la biblioteca con su estacion, y empieza el frente."""
    b = W['pulso']['beat']
    sale = firma([x for x in W['oido'] if 0 <= b - x[0] <= _bpb(cfg)])
    viejo = _patron(W, W['pattern']) if W['pattern'] else None
    if viejo is None and sale:                  # el primero que se oye: se aprende al irse
        viejo = dict(nombre=nombre_pattern(len(W['patrones'])), firma={}, tinte=list(W['estacion']['tinte']),
                     ventanas=int(W['estacion']['ventanas']), visto=b)
        W['patrones'].append(viejo)
    if viejo is not None:
        if sale:
            viejo['firma'] = sale
        viejo['tinte'] = list(W['estacion']['tinte'])
        viejo['ventanas'] = int(W['estacion']['ventanas'])
        viejo['visto'] = b
    de = W['frente']['a'] if W['frente'] and W['frente'].get('a') else W['estacion']
    W['frente'] = dict(beat0=b, de=dict(tinte=list(de['tinte']), ventanas=int(de['ventanas'])), a=None,
                       pattern=None, conocido=None, parecido=0.0)
    W['oido'] = []
    W['ev']['frente'] = dict(beat=b, sale=viejo['nombre'] if viejo else None)
    return W['frente']


def reconocer(W, cfg, f):
    """Lo que ha sonado desde el cambio, contra la biblioteca: el pattern
    conocido mas parecido (desde RECONOCER) o uno nuevo, con su estacion."""
    entra = firma(W['oido'])
    mejor, sim = None, 0.0
    for p in W['patrones']:
        q = parecido(entra, p['firma'])
        if q > sim:
            mejor, sim = p, q
    if mejor is not None and sim >= RECONOCER:
        f.update(pattern=mejor['nombre'], conocido=True, parecido=sim,
                 a=dict(tinte=list(mejor['tinte']), ventanas=int(mejor['ventanas'])))
    else:
        n = len(W['patrones'])
        nuevo = dict(nombre=nombre_pattern(n), firma=entra, tinte=tinte_estacion(n + 1),
                     ventanas=1 - int(f['de']['ventanas']), visto=W['pulso']['beat'])
        W['patrones'].append(nuevo)
        f.update(pattern=nuevo['nombre'], conocido=False, parecido=sim,
                 a=dict(tinte=list(nuevo['tinte']), ventanas=nuevo['ventanas']))
    W['pattern'] = f['pattern']


def progreso_frente(W, cfg):
    """0-1 del frente en curso (None sin frente), a saltos de stop-motion."""
    f = W['frente']
    if not f:
        return None
    pasos = max(1, int(cfg['pasos_frente']))
    u = (W['pulso']['beat'] - f['beat0']) * max(1, int(cfg['steps_per_beat']))
    return max(0.0, min(1.0, math.floor(u * FOTOS_PASO) / (FOTOS_PASO * float(pasos))))


def frente_tick(W, cfg):
    """A mitad de camino se reconoce el pattern; al llegar al polo norte, su
    estacion se queda."""
    q = progreso_frente(W, cfg)
    if q is None:
        return
    f = W['frente']
    if f['a'] is None and q >= 0.5:
        reconocer(W, cfg, f)
    if q >= 1.0:
        if f['a'] is None:
            reconocer(W, cfg, f)
        W['estacion'] = dict(tinte=list(f['a']['tinte']), ventanas=int(f['a']['ventanas']))
        W['ev']['frente_fin'] = dict(pattern=f['pattern'], conocido=f['conocido'])
        W['pattern_conocido'] = f['conocido']
        W['frente'] = None


def latitud(i):
    """Latitud de la celda i en grados (-90 polo sur, 90 polo norte)."""
    return math.degrees(math.asin(max(-1.0, min(1.0, normal_i(i)[1]))))


def lat_frente(q):
    return -90.0 - FRENTE_ANCHO + q * (180.0 + 2.0 * FRENTE_ANCHO)


def tinte_actual(W, cfg):
    """El tinte de la luz: el de la estacion, o el del frente a medio pasar."""
    q = progreso_frente(W, cfg)
    f = W['frente']
    if q is None or not f:
        return list(W['estacion']['tinte'])
    a = f['a']['tinte'] if f['a'] else f['de']['tinte']
    return [x + (y - x) * q for x, y in zip(f['de']['tinte'], a)]


def viento_lfo(W, cfg):
    """El empuje del viento (grados): fase 19, el LFO del modular (Vientomax)."""
    if cfg['nivel'] >= 19:
        return cfg['viento_max'] * (2.0 * W['modular']['lfo'] - 1.0)
    return 0.0


def vaiven(amp, viento, bq, lon):
    """El vaiven del dosel en grados (con signo): Swaymax en fase con el beat, con
    una onda suave por longitud, mas el viento. Lo mismo calcula el vertex shader de
    la piel (motor v77)."""
    return amp * math.sin(2.0 * math.pi * bq / SWAY_BEATS + 0.5 * lon) + viento


def balanceo_gpu(cfg):
    """Motor v77: el vaiven y el viento del dosel los hace el vertex shader de la piel
    (desde la fase 12, y sin Materialrespaldo, que es un Phong sin shader)."""
    return cfg['nivel'] >= 12 and not cfg.get('respaldo', 0)


def balanceo_filas(W, cfg, i, bq):
    """El balanceo que va en las filas de los ejemplares: con el shader (motor v77),
    solo el empuje del frente (el vaiven y el viento los pone la GPU, y las filas no
    cambian con el pulso); sin el, todo, como antes."""
    if not balanceo_gpu(cfg):
        return balanceo(W, cfg, i, bq)
    q = progreso_frente(W, cfg)
    if q is not None and 0.0 < q < 1.0:
        d = abs(latitud(i) - lat_frente(q))
        if d < FRENTE_ANCHO:
            return round(FRENTE_INCL * (1.0 - d / FRENTE_ANCHO) * 2.0) / 2.0, 270.0
    return 0.0, 0.0


def viento_reloj(frame=None):
    """(amplitud, viento, pulso) del vaiven del dosel para el shader de la piel:
    Swaymax, el viento del LFO y el pulso en beats a saltos de stop-motion. Ceros
    antes de la fase 17 (el dosel no se mueve) o sin el shader."""
    try:
        W, c = world(), cfg_foto()
        if c['nivel'] < 17 or not balanceo_gpu(c):
            return 0.0, 0.0, 0.0
        return float(c['sway_max']), float(viento_lfo(W, c)), float(beat_stop(W, c))
    except Exception:
        return 0.0, 0.0, 0.0


def balanceo(W, cfg, i, bq):
    """(inclinacion, rumbo) del dosel de la celda i: el vaiven del pulso
    (Swaymax, en fase con el beat, con una onda suave por longitud) y, si pasa
    el frente, el empuje hacia el norte."""
    n = normal_i(i)
    lon = math.atan2(n[2], n[0])
    sw = vaiven(cfg['sway_max'], viento_lfo(W, cfg), bq, lon)
    incl, rumbo = abs(sw), (0.0 if sw >= 0 else 180.0)
    q = progreso_frente(W, cfg)
    if q is not None and 0.0 < q < 1.0:
        d = abs(latitud(i) - lat_frente(q))
        if d < FRENTE_ANCHO:
            incl, rumbo = FRENTE_INCL * (1.0 - d / FRENTE_ANCHO) + 0.3 * incl, 270.0
    return round(incl * 2.0) / 2.0, rumbo


def ventanas_celda(W, cfg, i, bq):
    """Nivel 0-4 de las ventanas del edificio de la celda i: el de la estacion
    (o el nuevo, si el frente ya ha pasado por su latitud) y, en cada beat,
    algunos edificios parpadean (mapa logistico, sin azar)."""
    base = int(W['estacion']['ventanas'])
    f = W['frente']
    q = progreso_frente(W, cfg)
    if tema_de(cfg) == 'industria' and not cfg.get('turno', 1):
        f = None                        # fase 17 v3: sin Turno, el frente no cambia los focos
    if f and q is not None:
        base = int(f['de']['ventanas'])
        if f['a'] is not None and latitud(i) <= lat_frente(q):
            base = int(f['a']['ventanas'])
    h = logistica(semilla_caos(int(math.floor(bq)) * 7 + 1, i), 3.91, 1)[0]
    if base:
        return 1 if h < 0.3 else 4
    return 3 if h < 0.2 else 0


def build_tiempo(W, cfg, now, out):
    """Lo que el pulso mueve fuera de los modelos: el trafico de las
    carreteras, las esporas sobre los bosques y las nubes del frente."""
    tema = tema_de(cfg)
    bq = beat_stop(W, cfg)
    lim = limit(cfg)
    parts = out.setdefault('particulas', [])
    n_puntos = 0
    if tema == 'ciudad' and cfg['nivel'] >= 13 and cfg.get('carreteras', 1):
        k_tr = max(0, int(cfg['trafico']))
        ancho = cfg['grosor_via']
        for a, b in (W.get('tejido_vias') or []):
            na, nb = normal_i(a), normal_i(b)
            ra = base_radius(W, cfg, a) + TEJIDO_LIFT + TEJIDO_ALTO
            rb = base_radius(W, cfg, b) + TEJIDO_LIFT + TEJIDO_ALTO
            for k in range(k_tr):
                f = (bq / TRAFICO_BEATS + k / float(max(1, k_tr)) + 0.37 * ((a * 7 + b) % 5)) % 1.0
                ida = k % 2 == 0
                g = f if ida else 1.0 - f
                Y = _norm(_add(_mul(na, 1.0 - g), nb, g))
                r = ra + (rb - ra) * g
                Z = _hacia(Y, na, nb)
                lado = _cross(Y, Z)
                p = _add(_mul(Y, r), lado, (0.22 if ida else -0.22) * ancho)
                s_ = 0.85 * ancho               # que se lean desde la camara de globo
                parts.append(_row(p, Y, s_, 0.5 * s_, s_, COL_FARO if ida else COL_PILOTO))
                n_puntos += 1
    if tema == 'naturaleza':
        now_p = bq * max(1, int(cfg['steps_per_beat'])) * 0.125     # el reloj de las esporas, en pasos
        for i in range(N):
            if W['occ'][i] <= 0 or W['own'][i] != GEO or W['vh'][i] <= 0.005:
                continue
            if estado_idx(cfg, W['occ'][i]) < 2:
                continue
            n = normal_i(i)
            base = base_radius(W, cfg, i)
            cw, cl_ = _cell_sizes(base, i)
            k_esp = 3 + int(round(9.0 * W['modular']['ruido'])) if cfg['nivel'] >= 19 else 3
            _particulas(parts, n, _mul(n, base), cw, cl_, W['vh'][i], semilla_caos(i, 31), k_esp,
                        COL_ESPORA, now_p, 0.125, 'esporas')
    if tema in CONSTRUIDOS and cfg['nivel'] >= 19:     # fase 19: el ruido del modular es smog (y humo)
        k_smog = int(round(5.0 * W['modular']['ruido'] * cfg['smog']))
        if k_smog > 0:
            now_p = bq * max(1, int(cfg['steps_per_beat'])) * 0.125
            for i in range(N):
                if W['occ'][i] <= 0 or not W['own'][i] or W['vh'][i] <= 0.005:
                    continue
                n = normal_i(i)
                base = base_radius(W, cfg, i)
                cw, cl_ = _cell_sizes(base, i)
                _particulas(parts, n, _mul(n, base), cw, cl_, max(W['vh'][i], 0.5 * lim),
                            semilla_caos(i, 61), k_smog, COL_SMOG, now_p, 0.125, 'smog')
    q = progreso_frente(W, cfg)
    if q is not None and 0.0 < q < 1.0 and tema == 'naturaleza':
        lat = math.radians(lat_frente(q))
        R = top_radius(W, cfg) + 1.4 * lim
        f = W['frente']
        tin = f['a']['tinte'] if f['a'] else f['de']['tinte']
        col = tuple(c * t for c, t in zip(COL_NUBE, tin))
        for k in range(FRENTE_NUBES):
            x0 = semilla_caos(k, 53)
            lon = 2.0 * math.pi * (k + 0.5 * x0) / FRENTE_NUBES
            la = lat + math.radians(FRENTE_ANCHO) * 0.35 * (x0 - 0.5)
            n = (math.cos(la) * math.cos(lon), math.sin(la), math.cos(la) * math.sin(lon))
            s_ = 0.18 + 0.22 * x0
            parts.append(_row(_mul(n, R * (1.0 + 0.04 * x0)), n, s_ * 1.6, s_ * 0.5, s_, col))
    W['tiempo'] = dict(trafico=n_puntos)


# -----------------------------------------------------------------------------
# 1. NUCLEO - escenas y direccion tematica (fase 18)
# -----------------------------------------------------------------------------
# Las dos escenas acotadas, naturaleza y ciudad, como presets listos para
# actuar: paleta, umbrales, Caos, Maxpiezas, luz y pulso guardados por escena
# (tabla 'escenas'); Escena los carga y Guardarescena guarda lo que haya.
# LUZ LOCAL sin luces nuevas: emisivos aditivos e instancias (geometria
# luz_local). Focos ambar en las obras a medias de la ciudad (la lampara y su
# charco de luz en el suelo), el brillo de las brasas de lo que arde (a saltos,
# con la chispa) y la nube de polvo de los derrumbes y accidentes, que se
# disipa con el polvo. Solo el destello de la fase 9 es una luz de verdad.
# DIAGNOSTICO (geometria diagnostico, con Diagnostico): los puentes de los
# clusters (blanco), las rutas del tejido (carreteras amarillas, rios azules) y
# la presion de cada celda (verde; rojo desde Umbralvecindad). El modo
# actuacion lo oculta, como la reticula y la leyenda.

ENCUADRE_DEF, RETICULA_SOBRE_DEF = 0.85, 0.2     # los de la camara de globo (ver ENCUADRE)
ESCENAS = ['naturaleza', 'ciudad', 'industria']      # fase 18 v2: la escena de la industria
# los parametros de una escena: (nombre, naturaleza, ciudad, industria). 'luz_principal.dimmer'
# y 'luz_relleno.dimmer' son de las luces, no de FASE1.
ESCENA_PARS = [
    ('Tema', 'naturaleza', 'ciudad', 'industria'),
    ('Paleta', 'generaciones', 'mineral', 'mineral'), ('Paletatono', 20.0, 205.0, 30.0),
    ('Paletacroma', 0.04, 0.03, 0.03),
    ('Umbralvecindad', 4.0, 4.5, 4.5), ('Pesovecina', 0.5, 0.5, 0.5), ('Mincluster', 2, 2, 2),
    ('Umbraldensidad', 0.6, 0.6, 0.6),
    ('Caos', 3.91, 3.74, 3.82), ('Maxpiezas', 6, 5, 5),
    ('Rugmin', 0.05, 0.1, 0.15), ('Rugmax', 0.85, 0.9, 0.95),
    ('Swaymax', 6.0, 4.0, 2.0), ('Trafico', 2, 3, 2),
    ('Luzcalida', 0.35, 0.0, 0.1),
    ('luz_principal.dimmer', 1.15, 1.0, 0.95), ('luz_relleno.dimmer', 0.16, 0.24, 0.26),
    ('Refrescopiel', 0.25, 0.25, 0.25),         # motor v101 (fase 18 v3): la piel por turnos, por escena
]
ESCENA_MIGRA = {'Refresconat': 'Refrescopiel'}  # motor v101: lo que una escena guardada llamaba de otro modo
LUZ_CALIDA = (1.00, 0.88, 0.72)             # la luz de dia de la escena de naturaleza
COL_FOCO, COL_CHARCO = (1.00, 0.62, 0.20), (0.30, 0.17, 0.05)
COL_BRILLO_BRASA = (0.55, 0.20, 0.04)
COL_POLVO_LUZ = (0.16, 0.13, 0.10)
COL_DIAG_PUENTE, COL_DIAG_VIA, COL_DIAG_RIO = (0.95, 0.95, 0.95), (1.0, 0.85, 0.2), (0.3, 0.5, 1.0)
COL_DIAG_BAJA, COL_DIAG_ALTA = (0.25, 0.85, 0.35), (0.95, 0.25, 0.2)


def escena_defecto(nombre):
    """{parametro: valor} de la escena por defecto 'naturaleza', 'ciudad' o 'industria'."""
    k = 1 + ESCENAS.index(nombre)
    return dict((fila[0], fila[k]) for fila in ESCENA_PARS)


def obras_a_medias(W, cfg, cl=None):
    """Celdas de la ciudad con una obra a medias (fusion o coronacion sin acabar)."""
    if cfg['nivel'] < 11 or tema_de(cfg) not in CONSTRUIDOS:
        return []
    tf, tc = objetivos(W, cfg, cl)
    obras = obras_ciudad(W, cfg)        # fase 11 v10: y los edificios en obra (planificada)
    return [i for i in range(N) if (0 < W['et_f'][i] < tf[i]) or (0 < W['et_c'][i] < tc[i])
            or (i in obras and obras[i] != 'bloque')]


def transitos_colgados(W, cfg):
    """Celdas cuyo transito no esta en su objetivo (tras un fin de ciclo, ninguna)."""
    if cfg['nivel'] < 11:
        return []
    tf, tc = objetivos(W, cfg)
    return [i for i in range(N) if W['et_f'][i] != tf[i] or W['et_c'][i] != tc[i]]


def px_formaciones(W, cfg, alto_cuadro=720.0, encuadre=ENCUADRE_DEF):
    """(px de una semilla, px de una coronacion) a distancia de la camara de
    globo: el planeta ocupa Encuadre del alto del cuadro."""
    R = top_radius(W, cfg) + RETICULA_SOBRE_DEF
    px = encuadre * alto_cuadro / (2.0 * R)
    lim = limit(cfg)
    return height_for(cfg, 1) * px, lim * (CORONA_K + CORONA_TRAMO * max(0, int(cfg['cumbre_tramos']))) * px


def build_luz_local(W, cfg, now):
    """Focos de las obras, brillo de las brasas y polvo iluminado: filas de la
    geometria aditiva luz_local."""
    out = []
    lim = limit(cfg)
    paso = W.get('paso') or 0.125
    for i in obras_a_medias(W, cfg):
        n, p0, cw, cl_ = _sitio(W, cfg, i)
        e, t = tangents(n)
        m_ = min(cw, cl_)
        poste = _add(_add(p0, e, 0.42 * cw), t, 0.42 * cl_)
        out.append(_row(_add(poste, n, 0.55 * lim), n, 0.07 * m_, 0.05 * m_, 0.07 * m_, COL_FOCO))
        out.append(_row(_add(p0, n, 0.012), n, 0.85 * cw, 0.01, 0.85 * cl_, COL_CHARCO))
    if cfg['nivel'] >= 14:
        for i, q in sorted(celdas_ardiendo(W, cfg).items()):
            n, p0, cw, cl_ = _sitio(W, cfg, i)
            chispa = int(now / paso * FOTOS_PASO + i) % 2
            k = (0.6 + 0.4 * chispa) * (1.0 - 0.5 * q)
            col = tuple(c * k for c in COL_BRILLO_BRASA)
            vh = max(W['vh'][i], 0.3 * lim)
            out.append(_row(_add(p0, n, 0.012), n, 1.1 * cw, 0.01, 1.1 * cl_, col))
            out.append(_row(p0, n, 0.8 * cw, 1.1 * vh, 0.8 * cl_, tuple(0.35 * c for c in col)))
        vida = max(1, int(cfg['pasos_polvo'])) * paso
        for t0, c, modo, k in W['polvo']:
            q = (now - t0) / vida
            if modo != 'polvo' or not 0.0 <= q < 1.0 or not 0 <= c < N:
                continue
            n, p0, cw, cl_ = _sitio(W, cfg, c)
            s_ = 0.6 + 0.6 * q
            col = tuple(x * (1.0 - q) for x in COL_POLVO_LUZ)
            out.append(_row(p0, n, s_ * cw, (0.2 + 0.4 * q) * lim, s_ * cl_, col))
        for cat in W['cats']:
            if cat['tipo'] == 'incendio':
                continue
            for c in sorted(cat['activas']):
                n, p0, cw, cl_ = _sitio(W, cfg, c)
                out.append(_row(p0, n, 0.9 * cw, 0.5 * lim, 0.9 * cl_, COL_POLVO_LUZ))
    return out


def _linea(a, b, grueso, col):
    """Una caja fina de a a b (para el diagnostico)."""
    Y = _norm(_add(a, b))
    d = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    d = _add(d, Y, -_dot(d, Y))
    L = math.sqrt(_dot(d, d))
    if L < 1e-6:
        return None
    Z = _mul(d, 1.0 / L)
    X = _cross(Y, Z)
    c = _mul(_add(a, b), 0.5)
    rx, ry, rz = _euler_xyz(X, Y, Z)
    return [c[0], c[1], c[2], rx, ry, rz, grueso, grueso, L, col[0], col[1], col[2]]


def build_diagnostico(W, cfg):
    """Puentes de los clusters, rutas del tejido y presion de cada celda."""
    out = []
    lim = limit(cfg)
    cl = clusters(W, cfg)
    alto = 0.04 * lim
    sobre = lambda i: _mul(normal_i(i), base_radius(W, cfg, i) + max(W['vh'][i], 0.0) + alto)
    hechos = set()
    for i in range(N):
        for j in cl['mascara'][i]:
            k = (min(i, j), max(i, j))
            if k in hechos:
                continue
            hechos.add(k)
            f = _linea(sobre(i), sobre(j), 0.03, COL_DIAG_PUENTE)
            if f:
                out.append(f)
    if cfg['nivel'] >= 13:
        t = tejido(W, cfg)
        suelo_ = lambda i: _mul(normal_i(i), base_radius(W, cfg, i) + 0.08)
        for a, b in t.get('vias', []):
            f = _linea(suelo_(a), suelo_(b), 0.05, COL_DIAG_VIA)
            if f:
                out.append(f)
        for rio in t.get('rios', []):
            for a, b in zip(rio, rio[1:]):
                f = _linea(suelo_(a), suelo_(b), 0.05, COL_DIAG_RIO)
                if f:
                    out.append(f)
    umbral = max(1e-6, cfg['umbral_vecindad'])
    for i in range(N):
        P = cl['presion'][i]
        if P <= 0:
            continue
        n = normal_i(i)
        e, _t = tangents(n)
        cw, _ = _cell_sizes(base_radius(W, cfg, i), i)
        p = _add(_mul(n, base_radius(W, cfg, i)), e, 0.38 * cw)
        out.append(_row(p, n, 0.06, 0.5 * lim * min(2.0, P / umbral), 0.06,
                        COL_DIAG_ALTA if P >= umbral else COL_DIAG_BAJA))
    return out


# -----------------------------------------------------------------------------
# 1. NUCLEO - las senales del modular (fase 19)
# -----------------------------------------------------------------------------
# Cuatro senales de control del modular, convertidas a 0-1: no es analisis del
# audio (el marco no lo quiere: volveria la pieza visualizacion reactiva), sino
# el voltaje convertido. Llegan por OSC (UDP, por ethernet: /estratos/lfo,
# /estratos/ruido, /estratos/espacio, /estratos/saturacion), desde cualquier
# CHOP (una interfaz de audio acoplada en continua, CC de un conversor CV-MIDI),
# a mano (Lfo, Ruido, Espacio, Saturacion) o de un generador de prueba sin
# azar. Rangomodular dice en que rango llegan (0-1, -1..1, 0-10 V, -5..5 V,
# -10..10 V) y
# Suavizado las alisa. Son moduladores, como la velocidad y el gate (fase 12):
# no cambian el mundo, solo como se ve.
#   LFO          naturaleza: viento en el dosel (hasta Vientomax grados, a un
#                lado y al otro); ciudad: las ventanas respiran (Respiracion).
#   ruido        naturaleza: mas esporas; ciudad: smog sobre los edificios.
#   espacialidad niebla de distancia: lo lejano se funde con la bruma.
#   saturacion   fracturas y glitch en los materiales del shader de la piel.

MODULAR = ['lfo', 'ruido', 'espacio', 'saturacion']
FUENTES_MODULAR = ['manual', 'osc', 'chop', 'prueba']
RANGOS_MODULAR = [('0..1', 0.0, 1.0), ('-1..1', -1.0, 1.0), ('0..10 V', 0.0, 10.0), ('-5..5 V', -5.0, 5.0),
                  ('-10..10 V', -10.0, 10.0)]
NIEBLA_COL = (0.12, 0.13, 0.16)


def normalizar(v, rango):
    """Un valor del modular en 0-1 segun Rangomodular."""
    _, lo, hi = RANGOS_MODULAR[int(rango) % len(RANGOS_MODULAR)]
    return max(0.0, min(1.0, (float(v) - lo) / (hi - lo)))


def generador_prueba(t):
    """Las cuatro senales de prueba, sin azar: un LFO de 4 s, un ruido que salta
    cada medio segundo por el mapa logistico, un espacio que va y viene en 20 s
    y rafagas de saturacion de un segundo cada ocho."""
    k = int(math.floor(t * 2.0))
    return dict(lfo=0.5 + 0.5 * math.sin(2.0 * math.pi * t / 4.0),
                ruido=logistica(semilla_caos(k, 7), 3.91, 1)[0],
                espacio=0.5 - 0.5 * math.cos(2.0 * math.pi * t / 20.0),
                saturacion=1.0 if (t % 8.0) < 1.0 else 0.0)


REPOSO_MODULAR = dict(lfo=0.5, ruido=0.0, espacio=0.0, saturacion=0.0)   # sin senal: nada
SIN_SENAL = 2.0             # segundos sin mensajes para volver al reposo


def modular_tick(W, cfg, crudo, dt, now):
    """Alisa las senales hacia lo que llega (crudo: {senal: 0-1}; None, nada
    nuevo). Si no llega nada en SIN_SENAL segundos, vuelven al reposo: el LFO
    al centro (sin viento) y lo demas a 0."""
    md = W['modular']
    if crudo is not None:
        md['crudo'] = dict(crudo)
        md['t'] = now
    md['activo'] = md['t'] > -90.0 and now - md['t'] <= SIN_SENAL
    destino = crudo if crudo is not None else (md.get('crudo') if md['activo'] else REPOSO_MODULAR)
    tau = max(0.0, cfg['suavizado'])
    a = 1.0 if tau <= 1e-6 else 1.0 - math.exp(-max(0.0, dt) / tau)
    for k in MODULAR:
        if destino and k in destino:
            md[k] += (max(0.0, min(1.0, destino[k])) - md[k]) * a
    return md


def canal_de(nombres, senal, k):
    """Indice del canal de una senal: el que termine en su nombre (lfo,
    ruido...) o, si ninguno, el k-esimo (en el orden de MODULAR)."""
    for j, nm in enumerate(nombres):
        limpio = ''.join(ch for ch in nm.lower() if ch.isalpha())
        if limpio.endswith(senal) or (senal == 'espacio' and limpio.endswith('espacialidad')):
            return j
    if not any(any(s_ in ''.join(ch for ch in nm.lower() if ch.isalpha()) for s_ in MODULAR)
               for nm in nombres):
        return k if k < len(nombres) else None
    return None


def niebla(W, cfg, d, R):
    """(cantidad, cerca, lejos) de la niebla de distancia: empieza en la cara
    del planeta que mira a la camara y, con espacio 1, lo de detras ya es
    bruma."""
    e = W['modular']['espacio'] * cfg['niebla'] if cfg['nivel'] >= 19 else 0.0
    cerca = max(0.0, d - R)
    lejos = d + R * (5.0 - 4.6 * min(1.0, e))
    return min(1.0, e), cerca, lejos


# -----------------------------------------------------------------------------
# 1. NUCLEO - el microfono de la sala (fase 21)
# -----------------------------------------------------------------------------
# El microfono entra como un pad 9 de erosion (PAD_MIC): el motor ya sabe
# erosionar, cortar, iluminar la celda y escalar, asi que aqui solo se detecta.
# Cada bloque de audio se reparte en BANDAS_MIC bandas (energia en dB, con un
# suelo de PISO_MIC dB); el flujo espectral es la suma de lo que sube cada
# banda respecto al maximo de los HIST_MIC bloques anteriores, en decenas de dB
# por banda: un sonido que empieza (una palmada, una tos, unos pasos) sube de
# golpe; un drone sostenido, no. Un onset es un flujo por encima de
# Umbralonset, separado del anterior por 0,12 s (fijo desde el motor v65), y que no cae en la
# ventana de un destello propio (W['sala']['destellos'], que llena la fase 23).
#   onset           erosion() con el pad 9 en la celda del objetivo (Objetivo,
#                   como los pads): baja Reduccionmic escalones enteros (D3),
#                   enciende la luz de la celda con su color y, desde la fase
#                   14, cuenta como aranazo: dos en la misma zona escalan (D9).
#   ruido de sala   la energia (el flujo) de los onsets de los ultimos
#                   60 s (fijo desde el motor v65); al pasar Umbralcorte abre un corte de
#                   Profundidadmic conchas y radio 1 en la celda del ultimo
#                   onset, y la cuenta vuelve a cero.
# Sin azar: la senal sintetica de las autopruebas (clic, ruido y drone) sale de
# un hash del numero de muestra. Desde el motor v66 no hay Script CHOP de
# simulacion (mic_sim): para probar sin microfono, la sala virtual
# (sala_virtual.py, Fuentemic = chop).

BANDAS_MIC = 16
FREC_MIC = (200.0, 12000.0)     # las bandas, repartidas en escala logaritmica
PISO_MIC = -60.0                # dB: el silencio
HIST_MIC = 3                    # bloques anteriores con los que se compara
DESCARTE_DESTELLO = 0.15        # s tras un destello propio en que un onset no cuenta
FUENTES_MIC = ['microfono', 'chop']     # chop: Chopmic (motor v56); v66: sin simulacion ni ambos
FUENTE_CHOP = 1
_MIC = dict(hist=[], muestra=0, clic=0)


def mic_reset():
    """Olvida los bloques anteriores y la senal sintetica pendiente."""
    _MIC.update(hist=[], muestra=0, clic=0)


def bandas_mic(bloque, rate):
    """Energia (dB) de cada banda de un bloque de muestras, o None si el
    bloque es demasiado corto o no hay numpy."""
    np = _np()
    if np is None or bloque is None:
        return None
    x = np.asarray(bloque, dtype=float).ravel()
    if x.size < 32 or rate <= 0:
        return None
    X = np.abs(np.fft.rfft(x)) ** 2 / x.size
    f = np.fft.rfftfreq(x.size, 1.0 / float(rate))
    lim = np.geomspace(FREC_MIC[0], min(FREC_MIC[1], 0.5 * float(rate)), BANDAS_MIC + 1)
    e = np.empty(BANDAS_MIC)
    for b in range(BANDAS_MIC):
        sel = X[(f >= lim[b]) & (f < lim[b + 1])]
        e[b] = sel.mean() if sel.size else 0.0
    return np.maximum(PISO_MIC, 10.0 * np.log10(e + 1e-12))


def flujo_espectral(prev, actual):
    """Suma de las subidas de energia por banda entre dos bloques (prev puede
    ser una lista de bloques: se compara con su maximo), en decenas de dB por
    banda: 1 es que todas las bandas han subido 10 dB."""
    np = _np()
    if prev is None or actual is None or np is None:
        return 0.0
    p = np.max(np.asarray(prev, dtype=float).reshape(-1, len(actual)), axis=0)
    return float(np.maximum(0.0, np.asarray(actual, dtype=float) - p).sum()) / (10.0 * len(actual))


def detectar_onset(W, cfg, flujo, now):
    """El flujo es un onset: pasa Umbralonset, 0,12 s despues del
    anterior y fuera de la ventana de un destello propio (este cuenta como
    descartado)."""
    mc = W['mic']
    if flujo < cfg['umbral_onset'] or now - mc['t'] < cfg['refractario_mic']:
        return False
    sala = W['sala']
    sala['destellos'] = [t for t in sala['destellos'] if now - t <= 5.0]
    if any(0.0 <= now - t <= DESCARTE_DESTELLO for t in sala['destellos']):
        mc['descartados'] += 1
        return False
    mc['t'] = now
    mc['n'] += 1
    return True


def erosion_mic(W, cfg, now, flujo=0.0):
    """Un onset: erosion() con el pad 9 en la celda del objetivo, y su energia
    al ruido de sala. Devuelve el evento de la erosion (con 'flujo' y, si el
    ruido ha abierto un corte, 'corte_ruido')."""
    if len(cfg['perfiles']) <= PAD_MIC:
        return None
    target = None
    if cfg['nivel'] >= 22:              # fase 22 (D2): a la celda que mira a la casilla mas densa
        k, _ = casilla_mas_densa(cfg)
        target = celda_de_casilla(W, cfg, k) if k is not None else None
    ev = erosion(W, cfg, PAD_MIC, int(cfg.get('vel_ref', 100)), now, target)
    ev['flujo'] = flujo
    W['mic']['ultimo'] = dict(t=now, flujo=flujo, celda=ev['celda'])
    if ev.get('prende') is False:       # no ha prendido: ni erosion ni ruido de sala
        ev['corte_ruido'] = None
        W['ev']['micro'] = ev
        return ev
    W['ruido']['onsets'].append([now, float(flujo), ev['celda']])
    ev['corte_ruido'] = ruido_tick(W, cfg, now)
    W['ev']['micro'] = ev
    return ev


def ruido_tick(W, cfg, now):
    """El ruido de sala: la energia de los onsets de los ultimos 60 s.
    Al pasar Umbralcorte, un corte de Profundidadmic conchas y radio 1 en la
    celda del ultimo onset (corte_tematico desde la fase 16; cut antes) y la
    cuenta a cero. Devuelve el corte, o None."""
    r = W['ruido']
    v = max(0.0, cfg['ventana_ruido'])
    r['onsets'] = [o for o in r['onsets'] if 0.0 <= now - o[0] <= v]
    total = sum(o[1] for o in r['onsets'])
    r['total'] = total
    if not r['onsets'] or total < cfg['umbral_corte']:
        return None
    celda = r['onsets'][-1][2]
    prof = max(1, int(cfg['prof_mic']))
    union = None
    antes = sum(W['occ']) if cfg['nivel'] >= 23 else 0
    if cfg['nivel'] >= 16:
        fuera, union = corte_tematico(W, cfg, celda, prof, 1, now)
    else:
        fuera = cut(W, cfg, celda, prof, 1, now)
    if cfg['nivel'] >= 23:              # fase 23: el corte del ruido de sala es erosion
        balance_suma(W, cfg, now, eros=antes - sum(W['occ']))
    r['onsets'] = []
    r['total'] = 0.0
    r['cortes'] += 1
    r['ultimo'] = dict(t=now, celda=celda, conchas=fuera, energia=total, prof=prof, union=union)
    W['ev']['ruido'] = r['ultimo']
    W['flash'] = dict(t=now, cell=celda, k=1.0, pad=PAD_MIC)
    W['aviso'] = 'ruido de sala: corte de %d conchas en la celda %d' % (fuera, celda)
    W['dirty'] = True
    return r['ultimo']


def mic_bloque(W, cfg, bloque, rate, now):
    """Un bloque de audio: su flujo y, si es un onset, la erosion. Devuelve
    {flujo, onset (el evento o None)} o None si el bloque no vale."""
    b = bandas_mic(bloque, rate)
    if b is None:
        return None
    hist = _MIC['hist']
    fl = flujo_espectral(hist, b) if hist else 0.0
    hist.append(b)
    del hist[:-HIST_MIC]
    W['mic']['flujo'] = fl
    ev = erosion_mic(W, cfg, now, fl) if detectar_onset(W, cfg, fl, now) else None
    return dict(flujo=fl, onset=ev)


def _hash_muestras(np, i):
    return (np.sin(i * 12.9898 + 78.233) * 43758.5453) % 1.0 * 2.0 - 1.0


def mic_sim_bloque(n, rate, s0, clic=False, ruido=0.0, drone=False):
    """n muestras de la senal sintetica de las autopruebas desde la muestra
    s0, sin azar: un clic
    (10 ms de ruido que se apaga, como una palmada), ruido de sala (amplitud
    0-1) y un drone de 110 Hz con dos armonicos."""
    np = _np()
    n = max(0, int(n))
    i = np.arange(n, dtype=float) + float(s0)
    x = np.zeros(n)
    if ruido > 0:
        x += float(ruido) * _hash_muestras(np, i)
    if drone:
        t = i / float(rate)
        x += 0.12 * (np.sin(2 * math.pi * 110.0 * t) + 0.5 * np.sin(2 * math.pi * 220.0 * t)
                     + 0.3 * np.sin(2 * math.pi * 330.0 * t))
    if clic:
        m = min(n, int(0.01 * rate))
        j = np.arange(m, dtype=float)
        x[:m] += 0.8 * _hash_muestras(np, i[:m] + 7.0) * np.exp(-j / (0.0018 * rate))
    return x


# =============================================================================
# 2. ADAPTADOR TOUCHDESIGNER
# =============================================================================
# Todo lo de aqui abajo usa op(), parent(), me y absTime: solo funciona
# dentro de TouchDesigner.

# -----------------------------------------------------------------------------
# 1. NUCLEO - la camara cenital (fase 22): casilla probable
# -----------------------------------------------------------------------------
# Una camara de profundidad en el techo mide cuanta gente hay en cada casilla
# del suelo, y esa densidad inclina la probabilidad de que cada senal que llega
# al planeta actue:  P(c) = C + (1 - C) k d(c).  C es Cuanto (la probabilidad con
# la sala vacia, 0,5 como mucho), k el peso de la presencia (Pesocrear o
# Pesoerosion) y d(c) la densidad (0-1) de la casilla que corresponde a la celda.
# El publico no escribe: solo inclina donde prende lo que ya llega.
#
# La imagen llega como ALTURAS sobre el suelo (m), ya enderezada: la fila 0 es la
# pared de la pantalla (el norte) y la columna 0 la izquierda de la sala mirando
# a la pantalla; PX_CASILLA pixeles por casilla. De ahi sale todo con numpy:
# mascara de cuerpos (entre Alturamin y Alturamax), desenfoque (Desenfoque m),
# rejilla (la fraccion de suelo ocupado de cada casilla) y suavizado (Subida y
# Bajada). El estado del sensor vive en el modulo (_SALA): no es mundo.
#
# Mapeo sala -> planeta: la pared de la pantalla es Latnorte y el fondo Latsur;
# el ancho de la sala cubre Anchoangular alrededor de Loncentral (la longitud de
# la cara que mira a la camara del globo: sigue al giro). La izquierda de la
# sala cae a la izquierda de la cara visible; Espejo lo invierte.
# El sorteo no usa azar: sale del mapa logistico (celda, tipo y contador de
# senales), asi que la misma sala da el mismo resultado.

PX_CASILLA = 10                 # pixeles de la imagen de alturas por casilla
DISCO_SIM = 0.25                # radio (m) de una persona de la sala simulada
ALTURA_SIM = 1.70               # y su altura
HOMBROS_SIM = 0.30              # lo que baja del centro (la cabeza) al borde (los hombros)
FUENTES_SALA = ['camara', 'simulada']
FUENTE_SIMULADA = 1
SENSORES_SALA = ['femto', 'kinect']     # v92: el aparato del techo (menu Sensor)
SENSOR_OPS = ('orbbec1', 'kinect1')     # su TOP: Orbbec TOP (Femto Bolt) o Kinect TOP (Kinect v2)
CAM_FPS = 30.0                  # la camara da 30 imagenes por segundo: no se lee mas deprisa
CUANTO_MAX = 0.5                # tope de Cuanto, tambien en el codigo
TIPOS_SENAL = ('crear', 'erosionar')
SALA_COLS = ['x', 'y', 'altura']        # tabla sala_personas (m; x desde la izquierda, y desde la pantalla)


def _sala_nueva():
    return dict(dens=None, t=None, t_img=-99.0, alt=None, hay=False, fps=0.0, senales=0,
                cuentas=dict(crear=[0, 0], erosionar=[0, 0]), ultima=None,
                pistas=[], casillas={}, nuevas=0, id=0, ultimas=[], t_personas=None,    # fase 24
                filas=[], fila_id=0, fila_sim=[],       # fase 29
                purgar=True, fuente=None)       # v91: la lectura diferida pendiente es de antes


_SALA = _sala_nueva()


def sala_reset(cuentas=True):
    """Olvida la densidad (y, con cuentas, los contadores del sorteo)."""
    viejo = dict(_SALA)
    _SALA.clear()
    _SALA.update(_sala_nueva())
    if not cuentas:
        _SALA.update(senales=viejo.get('senales', 0), cuentas=viejo.get('cuentas', _SALA['cuentas']))


def reiniciar_cuentas():
    _SALA['senales'] = 0
    _SALA['cuentas'] = dict(crear=[0, 0], erosionar=[0, 0])


def rejilla_sala(cfg):
    """(columnas, filas) de casillas: Anchosala x Fondosala en casillas de Tamcasilla."""
    t = max(0.05, float(cfg['tam_casilla']))
    return (max(1, int(round(cfg['ancho_sala'] / t))), max(1, int(round(cfg['fondo_sala'] / t))))


def casilla_xy(cfg, k):
    """Centro (x, y) en metros de la casilla k (x desde la izquierda, y desde la pantalla)."""
    cols, filas = rejilla_sala(cfg)
    k = max(0, min(cols * filas - 1, int(k)))
    return ((k % cols + 0.5) * cfg['ancho_sala'] / cols, (k // cols + 0.5) * cfg['fondo_sala'] / filas)


def casilla_de_xy(cfg, x, y):
    """La casilla del punto (x, y) en metros, o None si cae fuera del suelo cubierto."""
    cols, filas = rejilla_sala(cfg)
    if not (0.0 <= x <= cfg['ancho_sala'] and 0.0 <= y <= cfg['fondo_sala']):
        return None
    return (min(filas - 1, int(y * filas / cfg['fondo_sala'])) * cols
            + min(cols - 1, int(x * cols / cfg['ancho_sala'])))


def lonlat_de_uv(cfg, u, v):
    """(latitud, longitud) en grados del punto (u, v) del suelo: u 0-1 de izquierda
    a derecha, v 0-1 de la pantalla al fondo."""
    if cfg['espejo']:
        u = 1.0 - u
    lat = cfg['lat_norte'] - v * (cfg['lat_norte'] - cfg['lat_sur'])
    lon = cfg['lon_central'] - (u - 0.5) * cfg['ancho_angular']
    return lat, (lon + 180.0) % 360.0 - 180.0


def uv_de_lonlat(cfg, lat, lon):
    """El punto (u, v) del suelo que corresponde a (latitud, longitud), o None si
    la celda queda fuera de la cara que mira a la sala."""
    ancho = cfg['ancho_angular']
    rango = cfg['lat_norte'] - cfg['lat_sur']
    if ancho <= 0 or rango == 0:
        return None
    dlon = (lon - cfg['lon_central'] + 180.0) % 360.0 - 180.0
    if abs(dlon) > 0.5 * ancho:
        return None
    u = 0.5 - dlon / ancho
    if cfg['espejo']:
        u = 1.0 - u
    v = (cfg['lat_norte'] - lat) / rango
    if v < 0.0 or v > 1.0:
        return None
    return u, v


def lonlat_celda(i):
    """(latitud, longitud) en grados del centro de la celda i."""
    x, y, z = NORMALS[i]
    return math.degrees(math.asin(max(-1.0, min(1.0, y)))), math.degrees(math.atan2(z, x))


def celda_de_lonlat(lat, lon):
    """La celda de la reticula que contiene (latitud, longitud)."""
    R = max(1, len(RINGS))
    band = 180.0 / (R + 0.5)
    cap = band * 0.25
    if lat <= -90.0 + cap or not RINGS:
        return POLE_S
    if lat >= 90.0 - cap:
        return POLE_N
    cells = RINGS[max(0, min(R - 1, int((lat + 90.0 - cap) / band)))]
    th = math.radians(lon)

    def lejos(k):
        x, _, z = NORMALS[k]
        return abs((math.atan2(z, x) - th + math.pi) % (2.0 * math.pi) - math.pi)
    return min(cells, key=lejos)


def celda_de_casilla(W, cfg, k):
    """La celda que mira a la casilla k, con Loncentral de este instante."""
    cols, filas = rejilla_sala(cfg)
    k = max(0, min(cols * filas - 1, int(k)))
    lat, lon = lonlat_de_uv(cfg, (k % cols + 0.5) / cols, (k // cols + 0.5) / filas)
    return celda_de_lonlat(lat, lon)


def casilla_de_celda(cfg, i):
    """La casilla a la que mira el centro de la celda i, o None."""
    uv = uv_de_lonlat(cfg, *lonlat_celda(i))
    if uv is None:
        return None
    cols, filas = rejilla_sala(cfg)
    return min(filas - 1, int(uv[1] * filas)) * cols + min(cols - 1, int(uv[0] * cols))


def _caja_np(np, a, r, eje):
    """Media movil de 2r + 1 pixeles a lo largo de un eje (fuera de la imagen, cero)."""
    r = int(r)
    if r < 1:
        return a
    pad = [(0, 0), (0, 0)]
    pad[eje] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad), axis=eje)
    k = 2 * r + 1
    return (c[k:] - c[:-k]) / k if eje == 0 else (c[:, k:] - c[:, :-k]) / k


def desenfocar(np, a, r_px):
    """Reparte lo ocupado en un radio de r_px pixeles: dos medias moviles por eje."""
    r = int(round(0.5 * r_px))
    for _ in range(2):
        a = _caja_np(np, _caja_np(np, a, r, 0), r, 1)
    return a


def imagen_sala(np, cfg, alt):
    """La imagen de alturas, al tamano de la rejilla (PX_CASILLA pixeles por casilla)."""
    cols, filas = rejilla_sala(cfg)
    h, w = filas * PX_CASILLA, cols * PX_CASILLA
    a = np.asarray(alt, dtype=float)
    if a.ndim == 3:
        a = a[..., 0]
    if a.shape != (h, w):
        fy = (np.arange(h) * (a.shape[0] / float(h))).astype(int)
        fx = (np.arange(w) * (a.shape[1] / float(w))).astype(int)
        a = a[fy][:, fx]
    return a


def ocupacion_sala(np, cfg, alt):
    """Fraccion de suelo ocupado de cada casilla (filas x columnas): la mascara de
    cuerpos entre Alturamin y Alturamax, repartida con Desenfoque."""
    cols, filas = rejilla_sala(cfg)
    a = imagen_sala(np, cfg, alt)
    m = ((a > cfg['altura_min']) & (a < cfg['altura_max'])).astype(float)
    m = desenfocar(np, m, cfg['desenfoque'] * a.shape[1] / max(1e-6, cfg['ancho_sala']))
    return m.reshape(filas, PX_CASILLA, cols, PX_CASILLA).mean(axis=(1, 3))


def sala_bloque(W, cfg, alt, now):
    """Una imagen de la camara (o None si no hay): la densidad de cada casilla
    persigue a su ocupacion / Ocupacionllena, con Subida al llegar alguien y Bajada
    al irse. Devuelve la densidad (filas x columnas), o None sin numpy."""
    np = _np()
    if np is None:
        return None
    cols, filas = rejilla_sala(cfg)
    prev = _SALA.get('dens')
    if prev is None or prev.shape != (filas, cols):
        prev = np.zeros((filas, cols))
    if alt is None:
        obj = np.zeros((filas, cols))
    else:
        obj = np.clip(ocupacion_sala(np, cfg, alt) / max(1e-6, cfg['ocupacion_llena']), 0.0, 1.0)
    t0 = _SALA.get('t')
    dt = 1.0 / CAM_FPS if t0 is None else max(0.0, min(1.0, now - t0))
    tau = np.where(obj > prev, max(1e-3, cfg['subida']), max(1e-3, cfg['bajada']))
    d = prev + (obj - prev) * (1.0 - np.exp(-dt / tau))
    d[d < 1e-4] = 0.0
    _SALA.update(dens=d, t=now, hay=alt is not None)
    return d


def presencia_densidad(cfg, i):
    """Densidad (0-1) de la casilla a la que mira la celda i (0 fuera de la sala)."""
    d = _SALA.get('dens')
    k = casilla_de_celda(cfg, i) if d is not None else None
    if k is None:
        return 0.0
    cols, filas = rejilla_sala(cfg)
    if d.shape != (filas, cols):
        return 0.0
    return float(d[k // cols, k % cols])


def presencia_prob(W, cfg, i, tipo):
    """P(c) = C + (1 - C) k d(c). Con Activo apagado, 1: todas las senales prenden."""
    if not cfg['presencia_activa']:
        return 1.0
    c = min(max(float(cfg['cuanto']), 0.0), CUANTO_MAX)
    k = cfg['peso_crear'] if tipo == 'crear' else cfg['peso_erosion']
    return c + (1.0 - c) * max(0.0, min(1.0, k)) * presencia_densidad(cfg, i)


def presencia_sortear(W, cfg, i, tipo):
    """El sorteo de una senal con posicion (crear o erosionar), una vez por evento
    y en su centro: prende con la probabilidad de su celda. Sale del mapa logistico
    (a r = 4, pasado a uniforme), sembrado con la celda, el tipo y el contador de
    senales. Cuenta las recibidas y las prendidas."""
    if not cfg['presencia_activa']:
        return True
    p = presencia_prob(W, cfg, i, tipo)
    n = _SALA['senales']
    _SALA['senales'] = n + 1
    x0 = 0.05 + 0.9 * ((n * AUREO + int(i) * 0.3819660113 + (0.27 if tipo == 'crear' else 0.71)) % 1.0)
    u = 2.0 / math.pi * math.asin(math.sqrt(logistica(x0, 4.0, 1)[0]))
    prende = u < p
    cu = _SALA['cuentas'].setdefault(tipo, [0, 0])
    cu[0] += 1
    cu[1] += int(prende)
    _SALA['ultima'] = dict(celda=int(i), tipo=tipo, p=p, prende=prende)
    return prende


def casilla_mas_densa(cfg):
    """(casilla, densidad) de la casilla con mas densidad, o (None, 0)."""
    d = _SALA.get('dens')
    if d is None or not d.size:
        return None, 0.0
    k = int(d.argmax())
    v = float(d.flat[k])
    return (k, v) if v > 0.0 else (None, 0.0)


def casillas_con_gente(umbral=0.01):
    d = _SALA.get('dens')
    return int((d > umbral).sum()) if d is not None else 0


def sala_sim_imagen(cfg, personas):
    """La imagen de alturas de la sala simulada: un disco de DISCO_SIM m por
    persona [x, y, altura] (m), mas alto en el centro (la cabeza) que en el borde
    (los hombros). Es la misma imagen que da la camara, asi que de ahi en adelante
    todo es igual. None sin numpy."""
    np = _np()
    if np is None:
        return None
    cols, filas = rejilla_sala(cfg)
    h, w = filas * PX_CASILLA, cols * PX_CASILLA
    a = np.zeros((h, w))
    mx, my = cfg['ancho_sala'] / w, cfg['fondo_sala'] / h      # metros por pixel
    for p in personas or ():
        x, y = float(p[0]), float(p[1])
        alto = float(p[2]) if len(p) > 2 and p[2] else ALTURA_SIM
        c0, c1 = int((x - DISCO_SIM) / mx), int((x + DISCO_SIM) / mx) + 1
        f0, f1 = int((y - DISCO_SIM) / my), int((y + DISCO_SIM) / my) + 1
        c0, c1, f0, f1 = max(0, c0), min(w, c1), max(0, f0), min(h, f1)
        if c0 >= c1 or f0 >= f1:
            continue
        xx = (np.arange(c0, c1) + 0.5) * mx - x
        yy = (np.arange(f0, f1) + 0.5) * my - y
        d2 = (xx[None, :] ** 2 + yy[:, None] ** 2) / (DISCO_SIM * DISCO_SIM)
        cuerpo = np.where(d2 <= 1.0, alto - HOMBROS_SIM * d2, 0.0)
        a[f0:f1, c0:c1] = np.maximum(a[f0:f1, c0:c1], cuerpo)
    return a



# -----------------------------------------------------------------------------
# 1. NUCLEO - personas (fase 24)
# -----------------------------------------------------------------------------
# La camara de la fase 22 (o su sala simulada), convertida en personas. En cada
# imagen de la camara:
#   1. MAXIMOS DE ALTURA. Un pixel es una cabeza si supera Alturamin, no pasa
#      de Alturamax y es el maximo en un radio de Separacioncabezas. Dos maximos
#      mas cerca que eso cuentan como una persona (se queda el mas alto).
#   2. SEGUIMIENTO por vecino mas cercano: los maximos se emparejan con las
#      personas de la imagen anterior, de la pareja mas cercana a la mas lejana,
#      sin pasar de Separacioncabezas. Un maximo sin pareja durante
#      Confirmapersona imagenes seguidas es una PERSONA NUEVA. Una persona sin
#      maximo desaparece.
#   3. OCUPACION BINARIA: una casilla esta ocupada si tiene al menos una persona;
#      guarda el instante en que se ocupo (t_ocupada) y lo pierde al quedar
#      libre. No pasa por ningun suavizado (la densidad de la fase 22 sigue a lo
#      suyo, el sorteo de las senales, y aqui no se usa).
#   4. LA CELDA QUE MIRA A LA CASILLA se calcula en el instante de cada evento
#      (celda_de_casilla, con Loncentral de esa imagen).
# El estado del sensor (pistas, casillas, contadores) vive en _SALA, no en W.

BORDE_CASILLA = 0.08            # m: una persona no cambia de casilla hasta pasar esto del borde
PERSONAS_COLS = ['id', 'x', 'y', 'altura', 'casilla', 'desde', 'nueva']
CASILLAS_COLS = ['casilla', 'ocupada', 'personas', 't_ocupada', 'celda']


def personas_reset():
    """Olvida las personas, las casillas ocupadas y sus contadores."""
    _SALA.update(pistas=[], casillas={}, nuevas=0, id=0, ultimas=[], t_personas=None)


def _max_local(np, a, r):
    """El maximo de cada pixel en una ventana de 2r + 1 (separable)."""
    r = int(r)
    if r < 1:
        return a
    for eje in (0, 1):
        pad = [(0, 0), (0, 0)]
        pad[eje] = (r, r)
        p = np.pad(a, pad, mode='constant', constant_values=-1.0)
        n = a.shape[eje]
        if eje == 0:
            a = np.maximum.reduce([p[k:k + n] for k in range(2 * r + 1)])
        else:
            a = np.maximum.reduce([p[:, k:k + n] for k in range(2 * r + 1)])
    return a


def detectar_cabezas(alturas, cfg):
    """Las cabezas de la imagen de alturas: [(x, y, altura)] en metros (x desde la
    izquierda, y desde la pantalla), de la mas alta a la mas baja."""
    np = _np()
    if np is None or alturas is None:
        return []
    a = imagen_sala(np, cfg, alturas)
    h, w = a.shape
    mx, my = cfg['ancho_sala'] / w, cfg['fondo_sala'] / h
    sep = max(0.01, float(cfg['sep_cabezas']))
    vale = (a > cfg['altura_min']) & (a <= cfg['altura_max'])
    if not vale.any():
        return []
    b = np.where(vale, a, 0.0)
    # maximo local en media separacion (los hombros de alguien mas alto no tapan una cabeza
    # vecina); la separacion entera la impone el descarte de abajo, de mayor a menor
    cand = vale & (b >= _max_local(np, b, max(1, int(0.5 * sep / max(mx, my)))))
    fs, cs = np.nonzero(cand)
    orden = np.argsort(-b[fs, cs], kind='stable')
    out = []
    for k in orden:
        x, y = (cs[k] + 0.5) * mx, (fs[k] + 0.5) * my
        if all((x - o[0]) ** 2 + (y - o[1]) ** 2 >= sep * sep for o in out):
            out.append((float(x), float(y), float(b[fs[k], cs[k]])))
    return out


def _casilla_con_borde(cfg, x, y, antes):
    """La casilla de (x, y); si la persona estaba en otra y no ha pasado
    BORDE_CASILLA del borde, se queda en la de antes (histeresis)."""
    k = casilla_de_xy(cfg, x, y)
    if antes is None or k is None or k == antes:
        return k
    cols, filas = rejilla_sala(cfg)
    tx, ty = cfg['ancho_sala'] / cols, cfg['fondo_sala'] / filas
    x0, y0 = (antes % cols) * tx, (antes // cols) * ty
    if x0 - BORDE_CASILLA <= x <= x0 + tx + BORDE_CASILLA and y0 - BORDE_CASILLA <= y <= y0 + ty + BORDE_CASILLA:
        return antes
    return k


def seguir_personas(prev, maximos, cfg, now=0.0):
    """Empareja los maximos con las pistas de la imagen anterior (vecino mas
    cercano, sin pasar de Separacioncabezas). Devuelve (pistas, nuevas): una pista
    es {id, x, y, alt, n, conf, desde, casilla}; nuevas, las que se confirman en
    esta imagen (un maximo sin pareja durante Confirmapersona imagenes seguidas)."""
    sep2 = float(cfg['sep_cabezas']) ** 2
    pares = sorted(((p['x'] - mxm[0]) ** 2 + (p['y'] - mxm[1]) ** 2, i, j)
                   for i, p in enumerate(prev) for j, mxm in enumerate(maximos))
    de_pista, de_max = {}, {}
    for d2, i, j in pares:
        if d2 > sep2:
            break
        if i in de_pista or j in de_max:
            continue
        de_pista[i], de_max[j] = j, i
    pistas, nuevas = [], []
    conf_n = max(1, int(cfg['confirma_persona']))
    for j, mxm in enumerate(maximos):
        if j in de_max:
            p = dict(prev[de_max[j]])
            p.update(x=mxm[0], y=mxm[1], alt=mxm[2], n=p['n'] + 1, nueva=False)
        else:
            _SALA['id'] = _SALA.get('id', 0) + 1
            p = dict(id=_SALA['id'], x=mxm[0], y=mxm[1], alt=mxm[2], n=1, conf=False, desde=now, casilla=None,
                     nueva=False)
        p['casilla'] = _casilla_con_borde(cfg, p['x'], p['y'], p.get('casilla'))
        if not p['conf'] and p['n'] >= conf_n:
            p['conf'] = True
            p['nueva'] = True
            p['desde'] = now
            nuevas.append(p)
        pistas.append(p)
    return pistas, nuevas


def ocupacion_casillas(personas, cfg=None):
    """{casilla: personas} de las personas confirmadas: la ocupacion binaria."""
    out = {}
    for p in personas:
        if p.get('conf') and p.get('casilla') is not None:
            out[p['casilla']] = out.get(p['casilla'], 0) + 1
    return out


def personas_en_sala():
    return [p for p in _SALA.get('pistas', ()) if p.get('conf')]


def tick_personas(W, cfg, now, maximos):
    """Una imagen de la camara: el seguimiento, la ocupacion binaria por casilla
    (con su t_ocupada) y las llegadas. Devuelve {personas, nuevas, casillas,
    libres}: nuevas es [{id, casilla, celda, t}], con la celda que mira a la
    casilla en este instante; libres, las casillas que acaban de vaciarse."""
    if 'pistas' not in _SALA:
        personas_reset()
    pistas, nuevas = seguir_personas(_SALA['pistas'], maximos, cfg, now)
    _SALA['pistas'] = pistas
    occ = ocupacion_casillas(pistas, cfg)
    cas = _SALA['casillas']
    libres = [k for k in cas if k not in occ]
    for k in libres:
        del cas[k]
    for k, n in occ.items():
        if k not in cas:
            cas[k] = dict(t_ocupada=now, personas=n)
        else:
            cas[k]['personas'] = n
    evs = []
    for p in nuevas:
        if p['casilla'] is None:
            continue
        evs.append(dict(id=p['id'], casilla=p['casilla'], celda=celda_de_casilla(W, cfg, p['casilla']), t=now))
    _SALA['nuevas'] = _SALA.get('nuevas', 0) + len(evs)
    _SALA['ultimas'] = evs or _SALA.get('ultimas', [])
    _SALA['t_personas'] = now
    return dict(personas=len(personas_en_sala()), nuevas=evs, casillas=cas, libres=libres)


def casillas_fila_sim(cfg, k0, n):
    """n casillas contiguas desde k0, en zigzag: hacia la derecha por su fila y, al
    llegar a la pared, la de debajo y hacia la izquierda (para la fila de prueba)."""
    cols, filas = rejilla_sala(cfg)
    k0 = max(0, min(cols * filas - 1, int(k0)))
    f, c, d = k0 // cols, k0 % cols, 1
    out = []
    while len(out) < n and len(out) < cols * filas:
        out.append(f * cols + c)
        if 0 <= c + d < cols:
            c += d
        else:
            f = f + 1 if f + 1 < filas else f - 1
            d = -d
            if f * cols + c in out:
                break
    return out


def sala_mundo(W, cfg, now, res):
    """Lo que las personas hacen en el mundo, por nivel (fases 25 y 29)."""
    if cfg['nivel'] >= 25:              # fase 25: la huella minima
        res['llegadas'] = llegadas(W, cfg, res['nuevas'], now)
        res['paradas'] = paradas(W, cfg, res['casillas'], now)
    if cfg['nivel'] >= 29:              # fase 29: las filas y sus escisiones
        res['filas'] = tick_filas(W, cfg, now)
    return res


# -----------------------------------------------------------------------------
# 1. NUCLEO - la huella minima (fase 25)
# -----------------------------------------------------------------------------
# Las personas dejan INCLUSIONES en la celda que mira a su casilla:
#   LLEGADA   al detectarse una persona nueva, con probabilidad Probllegada. Sin
#             azar de software: lo decide el mapa logistico sembrado con el id de
#             la persona, la celda y el ciclo (la misma sala da el mismo resultado).
#   PARADA    Tparada segundos seguidos con la casilla ocupada (ocupacion binaria)
#             dejan una inclusion segura. Una por parada: la casilla se rearma al
#             quedar libre.
# Cada inclusion guarda el ESCALON (la ocupacion) de su celda en el instante en
# que cae: [escalon, tipo, t, k]; k es su semilla (color de la paleta humana,
# posicion y tamano). Varias por celda, de la mas antigua a la mas nueva, con
# tope INCL_CELDA (el exceso quita la mas antigua de las de escalon mas alto).
# Es mundo: vive en W['incl'] (el nombre 'huella' ya es de la fase 7).
# ASPECTO (plastiglomerado): piezas pequenas medio enterradas en el suelo de la
# celda, alrededor de la formacion, de color saturado de la paleta humana (nunca
# cian ni ambar), rugosidad 0,1-0,2 (familia plastico del shader de la piel). La
# matriz es la loseta: en las celdas con inclusiones su tapa baja de rugosidad 1
# a RUG_TAPA_INCL.

INCL_CELDA = 12                 # inclusiones por celda, como mucho
LLEGADA, PARADA = 1, 2
TIPO_INCL = {LLEGADA: 'llegada', PARADA: 'parada'}
RUG_TAPA_INCL = 0.85            # la tapa de una celda con inclusiones (v5: 0,8-0,9)
# la paleta humana (P5): lo que queda del tono OKLCH fuera del cian de las
# cicatrices (165-235), el ambar del SEQ2 (55-100), los verdes de los pisos
# (120-165) y el azul de los rios (235-275), y sin el rojo saturado puro (18-40)
BANDAS_HUMANAS = ((275.0, 360.0), (0.0, 18.0), (40.0, 55.0), (100.0, 120.0))
L_HUMANA = 0.75                 # luminosidad: ni la de los pads oscuros (0,53-0,69) ni la de los claros (0,81-0,85)
C_HUMANA = 0.19                 # croma alto (baja lo justo para caber en sRGB)
CAUSAS_BORRADO = ('erosion', 'micro', 'corte', 'catastrofe', 'escision')


def _uniforme_caos(x0):
    """Un valor uniforme en (0, 1) del mapa logistico a r = 4 sembrado con x0."""
    return 2.0 / math.pi * math.asin(math.sqrt(logistica(x0, 4.0, 1)[0]))


def _frac(x):
    return x - math.floor(x)


def tono_humano(k):
    """El tono OKLCH (grados) de la semilla k (0-1), repartido por BANDAS_HUMANAS."""
    total = sum(b - a for a, b in BANDAS_HUMANAS)
    x = _frac(float(k)) * total
    for a, b in BANDAS_HUMANAS:
        if x <= b - a:
            return a + x
        x -= b - a
    return BANDAS_HUMANAS[-1][1]


_PAL_HUMANA = {}


def paleta_humana(cfg, k):
    """El color sRGB (0-1) de la semilla k: croma alto, luminosidad L_HUMANA."""
    q = int(_frac(float(k)) * 256.0)
    col = _PAL_HUMANA.get(q)
    if col is None:
        h = tono_humano(q / 256.0)
        C = C_HUMANA
        col, dentro = oklch_to_srgb(L_HUMANA, C, h)
        while not dentro and C > 0.05:
            C -= 0.01
            col, dentro = oklch_to_srgb(L_HUMANA, C, h)
        _PAL_HUMANA[q] = col
    return col


def incl_de(W):
    """W['incl'], con una lista por celda."""
    inc = W.get('incl')
    if not isinstance(inc, list) or len(inc) != N:
        inc = W['incl'] = [[] for _ in range(N)]
    return inc


def n_inclusiones(W):
    return sum(len(x) for x in incl_de(W))


def depositar_inclusion(W, cfg, celda, tipo, now):
    """Una inclusion en la celda, con el escalon (ocupacion) que tiene ahora.
    Devuelve la inclusion [escalon, tipo, t, k]."""
    lst = incl_de(W)[celda]
    cu = W['incl_n']
    n = cu['llegadas'] + cu['paradas']
    k = _uniforme_caos(0.05 + 0.9 * _frac(n * AUREO + int(celda) * 0.3819660113 + 0.11 * int(tipo)))
    inc = [int(W['occ'][celda]), int(tipo), float(now), k]
    lst.append(inc)
    while len(lst) > INCL_CELDA:        # el exceso: la mas antigua de las de escalon mas alto
        alto = max(x[0] for x in lst[:-1])
        lst.remove(next(x for x in lst[:-1] if x[0] == alto))
    cu['llegadas' if tipo == LLEGADA else 'paradas'] += 1
    W['incl_ultima'] = dict(celda=int(celda), escalon=inc[0], tipo=int(tipo), t=float(now))
    W['dirty'] = True
    return inc


def llegada_prende(W, cfg, persona, celda):
    """El si o el no de una llegada: el mapa logistico sembrado con el id de la
    persona, la celda y el ciclo, contra Probllegada."""
    x0 = 0.05 + 0.9 * _frac(int(persona) * AUREO + int(celda) * 0.3819660113 + int(W.get('ciclo_n', 1)) * 0.137)
    return _uniforme_caos(x0) < cfg['prob_llegada']


def llegadas(W, cfg, nuevas, now):
    """Las personas nuevas [{id, casilla, celda, t}]: cada una deja una inclusion
    en la celda que miraba su casilla al confirmarse, con probabilidad Probllegada.
    Devuelve las inclusiones dejadas."""
    out = []
    for ev in nuevas or ():
        if ev.get('celda') is not None and llegada_prende(W, cfg, ev['id'], ev['celda']):
            out.append(depositar_inclusion(W, cfg, ev['celda'], LLEGADA, now))
    return out


def paradas(W, cfg, casillas, now):
    """Tparada segundos seguidos con la casilla ocupada: una inclusion segura en
    la celda que mira a la casilla en ese instante. Una por parada (la casilla
    se rearma al quedar libre, cuando pierde su t_ocupada)."""
    out = []
    for k, v in (casillas or {}).items():
        if not v.get('parada') and now - v['t_ocupada'] >= cfg['t_parada'] - 1e-9:
            v['parada'] = True
            out.append(depositar_inclusion(W, cfg, celda_de_casilla(W, cfg, k), PARADA, now))
    return out


def vaciar_inclusiones(W):
    """El mundo se entierra: lo heredado empieza sin inclusiones."""
    W['incl'] = [[] for _ in range(N)]
    W['dirty'] = True


# --- la noche de enterramiento (fase 28) --------------------------------------------
# En cada enterramiento, con colapso o sin el, durante Noche segundos (la misma
# de la oscuridad de sala de la fase 23) la esfera apaga lo mineral: solo emiten
# las inclusiones supervivientes recien horneadas (las motas de la concha nueva)
# y, desde la fase 29, las paredes de las escisiones. Empieza en el mismo
# fotograma del recuento. El mundo nuevo sigue funcionando: lo que nace durante
# la noche se dibuja apagado. Sin luces ni geometria nuevas: un valor 'noche'
# (0-1; entra de golpe y sale en NOCHE_SALIDA s) que llega
#   - al shader de la piel (y de las conchas) como uniforme uNoche: todo se
#     multiplica por 1 - noche y las motas recien horneadas suben su emisivo;
#   - a las luces: el color de luz_principal, luz_relleno y luz_destello se
#     multiplica por 1 - noche (lo que dibuja con Phong se apaga con ellas);
#   - a las capas de luz y a las particulas (luz_celda, luz_conchas, luz_local,
#     particulas, humo...): el color de sus instancias, por 1 - noche.
# Nada se recompila ni sale del render.

NOCHE_SALIDA = 0.4              # s que tarda en volver la luz al acabar la noche
ALFA_RECIENTE = 100.0           # lo que suma al alfa una loseta recien horneada (el shader lo lee)
NOCHE_CAPAS = ('luz_celda', 'luz_conchas', 'luz_local', 'particulas', 'humo', 'vagones', 'diagnostico',
               'coronas')
NOCHE_FUERA = ('particulas', 'humo')    # transparentes: a oscuras del todo, no se dibujan


def noche_nivel(W, cfg, now):
    """La noche (0-1): 1 desde el fotograma del recuento hasta Noche s despues;
    luego vuelve a 0 en NOCHE_SALIDA s."""
    n = W.get('noche')
    if not n or now < n[0]:
        return 0.0
    if now <= n[1]:
        return 1.0
    return max(0.0, 1.0 - (now - n[1]) / NOCHE_SALIDA)


def noche_tick(W, cfg, now):
    """Cada fotograma: al acabar la noche (y su salida) se olvida, y las losetas
    dejan de marcarse como recien horneadas."""
    n = W.get('noche')
    if n and now > n[1] + NOCHE_SALIDA:
        W['noche'] = None
        W['dirty'] = True


def noche_filas(out, dia):
    """Apaga las capas de luz y las particulas: el color de sus instancias, por
    dia (1 - noche). A oscuras del todo, las transparentes no se dibujan."""
    if dia >= 0.999:
        return out
    for k in NOCHE_CAPAS:
        filas = out.get(k)
        if not filas:
            continue
        if dia <= 0.02 and k in NOCHE_FUERA:
            out[k] = []
            continue
        out[k] = [list(f[:9]) + [f[9] * dia, f[10] * dia, f[11] * dia] + list(f[12:]) for f in filas]
    return out


def emiten_noche(W, cfg):
    """(inclusiones recien horneadas, escisiones abiertas) que emiten en la noche."""
    sh = W['shells'][-1] if W['shells'] else {}
    n = sum(len(v) for v in sh.get('incl', {}).values()) if sh.get('banda') == 'humana' else 0
    esc = sum(1 for e in W.get('escisiones', ()) if e.get('estado') != 'enterrada' or e.get('t_noche'))
    return n, esc


# --- la clasificacion al enterrar (fase 27) ----------------------------------------
# En end_cycle, antes de hornear: se cuentan las inclusiones supervivientes del
# mundo que se entierra (las escisiones no cuentan). Con al menos Minhuellas, la
# concha es ESTRATO HUMANO; si no, CONCHA LIMPIA, aunque haya habido gente todo
# el dia (todas sus huellas se borraron). El recuento se hornea en el material:
# cada loseta nueva guarda cuantas inclusiones sobrevivieron en su celda y sus
# semillas (sus colores), y el shader de las conchas las dibuja como motas de la
# paleta humana en la cara y los flancos de esa loseta, con una cobertura que
# crece con su numero y nunca pasa de Inclusionesmax. El grosor de la concha no
# cambia. La concha guarda tambien el motivo del cierre y la marca de COLAPSO
# (el motivo 'colapso' de la fase 23), que se combina con humana o limpia. Una
# concha de antes de la fase 27 se lee como limpia, sin colapso.

COB_PASOS = 20                  # la cobertura viaja en el alfa de la loseta en veinteavos
COB_K = 3.0                     # inclusiones con las que una loseta llega a 1 - 1/e de Inclusionesmax
PALETA_HUMANA_8 = [(0.642, 0.635, 0.993), (0.746, 0.587, 0.994), (0.874, 0.509, 0.982), (0.959, 0.475, 0.863), (0.991, 0.484, 0.721), (0.991, 0.510, 0.598), (0.992, 0.546, 0.279), (0.699, 0.716, 0.098)]          # la tabla del shader (comun): paleta_humana en (j + 0,5) / 8


def contar_huellas(W):
    """Las inclusiones supervivientes del mundo (las escisiones no son inclusiones)."""
    return n_inclusiones(W)


def clasificar_concha(W, cfg, ev=None):
    """La marca de la concha que se entierra: {huellas, banda ('humana' o
    'limpia'), colapso, cierre, incl ({celda: [semillas]}), escisiones (ids)}."""
    n = contar_huellas(W)
    motivo = (ev or {}).get('motivo')
    incl = dict((i, [x[3] for x in lst]) for i, lst in enumerate(incl_de(W)) if lst)
    abiertas = [e['id'] for e in W.get('escisiones', ()) if e.get('estado') in ('abierta', 'cerrada')]
    return dict(huellas=n, banda='humana' if n >= max(1, int(cfg['min_huellas'])) else 'limpia',
                colapso=motivo == 'colapso', cierre=motivo or '', incl=incl, escisiones=abiertas)


def banda_de(sh):
    """(banda, huellas, colapso) de una concha; sin marca (antes de la fase 27), limpia."""
    return sh.get('banda', 'limpia'), int(sh.get('huellas', 0)), bool(sh.get('colapso', False))


def cobertura(cfg, n):
    """Cobertura (0-1) de las motas de una loseta con n inclusiones: crece con n y
    nunca pasa de Inclusionesmax."""
    if n <= 0:
        return 0.0
    return max(0.0, min(1.0, cfg['inclusiones_max'])) * (1.0 - math.exp(-n / COB_K))


def cobertura_q(cfg, sh, c):
    """La cobertura de la loseta de la celda c en la concha sh, en veinteavos
    (lo que lleva la parte entera de su alfa, / 2). Solo en un estrato humano."""
    if sh.get('banda') != 'humana':
        return 0
    ks = sh.get('incl', {}).get(c) or sh.get('incl', {}).get(str(c))
    if not ks:
        return 0
    tope = int(math.floor(max(0.0, min(1.0, cfg['inclusiones_max'])) * COB_PASOS + 1e-9))
    return max(1 if tope else 0, min(tope, int(round(cobertura(cfg, len(ks)) * COB_PASOS))))


def cobertura_concha(cfg, sh):
    """La cobertura de la loseta mas cubierta de la concha (0-1)."""
    return max([cobertura_q(cfg, sh, c) for c in sh.get('incl', {})] or [0]) / float(COB_PASOS)


# --- el borrado (fase 26) --------------------------------------------------------
# Una inclusion desaparece cuando la erosion baja su celda por debajo de su
# escalon (occ < escalon). En una celda sin construir (escalon 0), cualquier
# golpe de erosion que la alcance la borra: cualquier anillo con peso mayor que
# 0, aunque ese golpe no quite una nota entera (P6). Valen todas las fuentes: la
# caja y los aranazos, el microfono (y su corte por ruido), los cortes (vacian
# la celda y se llevan todas sus inclusiones), los accidentes y catastrofes de
# la fase 14 y la escision de la fase 29 (es un corte). El bombo y el tom no
# borran: son impulso y suben la ocupacion. Un unico punto de purga
# (purgar_inclusiones), que llaman _undo_note y bajar_escalon; erosion() llama
# ademas a golpe_inclusiones en cada celda de sus anillos; cut(), a
# borrar_inclusiones; y una pasada de seguridad por fotograma mira solo las
# celdas con inclusiones. La causa de cada borrado se cuenta en
# W['incl_borradas'].

_CAUSA = ['erosion']            # quien esta bajando la ocupacion ahora (erosion, micro, catastrofe)


def _borradas(W, causa, n):
    if n:
        b = W['incl_borradas']
        causa = causa or _CAUSA[0]
        b[causa] = b.get(causa, 0) + n
        W['dirty'] = True
    return n


def purgar_inclusiones(W, celda, causa=None):
    """Borra las inclusiones de la celda cuyo escalon queda por encima de su
    ocupacion (occ < escalon). Devuelve cuantas."""
    lst = incl_de(W)[celda]
    if not lst:
        return 0
    o = W['occ'][celda]
    quedan = [x for x in lst if x[0] <= o]
    n = len(lst) - len(quedan)
    if n:
        W['incl'][celda] = quedan
    return _borradas(W, causa, n)


def golpe_inclusiones(W, celda, causa=None):
    """Un golpe de erosion alcanza la celda: borra sus inclusiones de escalon 0
    (las que cayeron sobre la celda sin construir), aunque no baje nada."""
    lst = incl_de(W)[celda]
    if not lst:
        return 0
    quedan = [x for x in lst if x[0] > 0]
    n = len(lst) - len(quedan)
    if n:
        W['incl'][celda] = quedan
    return _borradas(W, causa, n)


def borrar_inclusiones(W, celda, causa):
    """Un corte (o una escision) se lleva todas las inclusiones de la celda."""
    n = len(incl_de(W)[celda])
    if n:
        W['incl'][celda] = []
    return _borradas(W, causa, n)


def purga_segura(W):
    """La pasada de seguridad de cada fotograma, solo en las celdas con
    inclusiones: lo que haya bajado la ocupacion por otro camino."""
    n = 0
    for i, lst in enumerate(incl_de(W)):
        if lst:
            n += purgar_inclusiones(W, i, 'catastrofe' if W.get('cats') else 'erosion')
    return n


def fila_inclusion(W, cfg, i, inc, r0=None):
    """La instancia de una inclusion de la celda i: una pieza pequena, medio
    enterrada en el suelo de la celda, alrededor de la formacion. Posicion, forma
    y color salen de su semilla k."""
    k = inc[3]
    n = normal_i(i)
    r0 = base_radius(W, cfg, i) if r0 is None else r0
    cw, cl = _cell_sizes(r0, i)
    ex, ez = tangents(n)
    ang = 2.0 * math.pi * _frac(k * 7.31)
    rad = 0.26 + 0.16 * _frac(k * 13.7)            # un anillo alrededor de la formacion
    d = _norm(_add(_add(n, ex, rad * cw * math.cos(ang) / r0), ez, rad * cl * math.sin(ang) / r0))
    t = _TERRENO.get('t') if cfg['nivel'] >= 11 else None
    try:
        r = r0 + (alto_en(t, d) if t is not None else 0.0)
    except Exception:
        r = r0
    s = (0.035 + 0.035 * _frac(k * 29.3)) * min(cw, cl)
    fila = _row(_mul(d, r), d, s * (0.7 + 0.6 * _frac(k * 3.7)), s * (0.45 + 0.35 * _frac(k * 5.3)),
                s * (0.7 + 0.6 * _frac(k * 11.1)), paleta_humana(cfg, k))
    fila[5] = 360.0 * _frac(k * 17.9)               # girada sobre la normal
    fila.append(0.10 + 0.10 * _frac(k * 19.7))      # rugosidad 0,1-0,2 (canal a)
    return fila


def build_inclusiones(W, cfg, now, out):
    """Las inclusiones vivas del mundo, una instancia cada una (out['inclusiones'])."""
    rows = []
    for i, lst in enumerate(incl_de(W)):
        if not lst:
            continue
        r0 = base_radius(W, cfg, i)
        for inc in lst:
            rows.append(fila_inclusion(W, cfg, i, inc, r0))
    out['inclusiones'] = rows
    return rows


# -----------------------------------------------------------------------------
# 1. NUCLEO - la fila y la escision colectiva (fase 29)
# -----------------------------------------------------------------------------
# FILA: Minfila personas o mas en casillas contiguas (diagonales incluidas),
# sostenida Tfila segundos sobre la ocupacion binaria. Modofila = cadena
# (cualquier forma contigua) o recta (todas las casillas en una misma fila,
# columna o diagonal de la rejilla, seguidas). Una fila es una componente conexa
# de casillas ocupadas; se reconoce de una imagen a la siguiente si comparte
# alguna casilla con la de antes. Cuenta personas, no casillas. Puede haber
# varias filas a la vez, cada una con su escision (P14).
# ESCISION: se abre en la celda que mira a la casilla de la fila con el t_ocupada
# mas antiguo, en el instante en que la fila cumple Tfila; esa celda queda fija.
# Profundidad: personas x Conchasporpersona losetas de la columna de origen, con
# el nucleo como tope; si se suman personas mientras la fila aguanta, la misma
# escision baja mas (sigue al maximo visto). La fila solo abre otra cuando se
# deshace. Es un HUECO permanente: quita losetas de la columna (como cut, con
# radio 0), vacia la celda y borra sus inclusiones (es un corte, P7). No cuenta
# en el tope por mundo de los cortes (quitadas), no enciende cicatriz cian,
# ignora Colmatacion en su celda (la concha siguiente la tapiza sin cerrarla) y
# las fases 13 (lagos) y 16 (fosiles) la excluyen. No pasa por erosion() ni por
# pulso(): no es erosion ni creacion para el balance de la fase 23.
# FULGURITA: una pieza por concha atravesada, de la superficie al fondo, en su
# propia geometria: pared exterior de arena fundida, interior vitreo y nucleo
# emisivo de la paleta humana (nunca cian), con dos o tres ramas finas por concha
# hacia las paredes vecinas, decididas por el mapa logistico (la escision y la
# concha como semilla). Las ramas son solo visuales: no quitan material (P11).
# Las filas son del sensor (_SALA['filas']); las escisiones, mundo (W['escisiones']).

ESCISIONES_MAX = 200            # las mas viejas se quedan solo en el registro
MODOS_FILA = ['cadena', 'recta']
COL_ARENA = (0.66, 0.58, 0.46)  # la pared de la fulgurita: arena fundida
PARED, VIDRIO, NUCLEO = 0, 1, 2  # las partes de la fulgurita (en el alfa: rugosidad + 2 x parte)
FULG_RAMAS = (2, 3)             # ramas por concha


def _vecinas_casilla(k, cols, filas):
    f, c = k // cols, k % cols
    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (df or dc) and 0 <= f + df < filas and 0 <= c + dc < cols:
                yield (f + df) * cols + c + dc


def es_recta(casillas, cols):
    """Las casillas estan todas en una misma fila, columna o diagonal de la
    rejilla, seguidas."""
    ks = sorted(int(k) for k in casillas)
    if len(ks) <= 1:
        return True
    pts = [(k // cols, k % cols) for k in ks]
    df, dc = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
    if (df, dc) not in ((0, 1), (1, 0), (1, 1), (1, -1)):
        return False
    return all((pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]) == (df, dc) for j in range(len(pts) - 1))


def buscar_filas(casillas, cfg):
    """Las componentes conexas (diagonales incluidas) de las casillas ocupadas
    {casilla: {personas, t_ocupada}}: [{casillas, personas, origen}], donde origen
    es la casilla ocupada desde hace mas tiempo. Sin filtrar por Minfila."""
    cols, filas = rejilla_sala(cfg)
    quedan = set(casillas)
    out = []
    while quedan:
        k0 = min(quedan)
        quedan.discard(k0)
        comp, pila = [k0], [k0]
        while pila:
            k = pila.pop()
            for v in _vecinas_casilla(k, cols, filas):
                if v in quedan:
                    quedan.discard(v)
                    comp.append(v)
                    pila.append(v)
        comp.sort()
        out.append(dict(casillas=comp, personas=sum(int(casillas[k].get('personas', 1)) for k in comp),
                        origen=min(comp, key=lambda k: (casillas[k]['t_ocupada'], k))))
    return out


def es_escision(W, c):
    """La celda c tiene una escision (un hueco permanente)."""
    return int(c) in W.get('esc_celdas', {})


def _fecha():
    import time
    return time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S')


def _quitar_losetas(W, celda, k):
    """Quita hasta k losetas de arriba de la columna de la celda (el nucleo es el
    tope). Devuelve las conchas quitadas, de arriba abajo."""
    col = W['cols'][celda]
    fuera = []
    while len(fuera) < k and col:
        s, _ = col.pop()
        if 0 <= s < len(W['shells']):
            W['shells'][s]['rm'][celda] = 1
        fuera.append(s)
    return fuera


def abrir_escision(W, cfg, fila, casilla, now):
    """La fila ha cumplido Tfila: abre una escision en la celda que mira a su
    casilla de origen en este instante. Devuelve la escision."""
    origen = celda_de_casilla(W, cfg, casilla)
    W['escision_n'] = W.get('escision_n', 0) + 1
    personas = int(fila.get('max', fila['personas']))
    jornada, hora = _fecha()
    e = dict(id=W['escision_n'], origen=origen, casilla=int(casilla), personas=personas,
             profundidad=personas * max(1, int(cfg['conchas_persona'])), cortadas=[],
             suelo0=suelo(W, cfg, origen), estado='abierta', t0=now, t1=None,
             ciclo=W.get('ciclo_n', 1), jornada=jornada, hora=hora, testigo=None,
             ramas=_uniforme_caos(0.05 + 0.9 * _frac(W['escision_n'] * AUREO + origen * 0.3819660113)))
    e['cortadas'] = _quitar_losetas(W, origen, e['profundidad'])
    f0, b0 = hueco_escision(W, cfg, origen)
    e['hondo0'] = max(0.0, b0 - f0)       # lo hondo del hueco al abrirse (para la fulgurita)
    _clear_cell(W, origen)              # un hueco: la celda queda vacia
    W['huella'][origen] = 0.0
    W['ruina'][origen] = 0
    for j in NEIGH[origen]:
        if W['par'][j] == origen:
            W['par'][j] = -1
    borrar_inclusiones(W, origen, 'escision')       # es un corte (P7)
    W.setdefault('esc_celdas', {})[origen] = W.get('esc_celdas', {}).get(origen, 0) + 1
    W['escisiones'].append(e)
    del W['escisiones'][:-ESCISIONES_MAX]
    W['ev']['escision'] = dict(id=e['id'], celda=origen, conchas=len(e['cortadas']), personas=personas, t=now)
    if cfg['nivel'] >= 30:              # fase 30: un relampago por escision
        e['relampago'] = relampago(W, cfg, now)
    W['aviso'] = 'escision %d: %d personas abren %d conchas en la celda %d' % (
        e['id'], personas, len(e['cortadas']), origen)
    W['dirty'] = True
    return e


def profundizar_escision(W, cfg, e, personas, now):
    """Mas personas en la fila: la misma escision baja mas (hasta el nucleo).
    Devuelve las losetas quitadas ahora."""
    if e['estado'] != 'abierta' or personas <= e['personas']:
        return 0
    e['personas'] = int(personas)
    e['profundidad'] = e['personas'] * max(1, int(cfg['conchas_persona']))
    mas = _quitar_losetas(W, e['origen'], e['profundidad'] - len(e['cortadas']))
    e['cortadas'] += mas
    if mas:
        f0, b0 = hueco_escision(W, cfg, e['origen'])
        e['hondo0'] = max(0.0, b0 - f0)
        W['dirty'] = True
    return len(mas)


def cerrar_escision(W, cfg, e, now, estado='cerrada'):
    """La fila se deshace (cerrada) o su mundo se entierra (enterrada): la
    escision ya no baja mas. El hueco se queda."""
    if e['estado'] == 'abierta' or (estado == 'enterrada' and e['estado'] == 'cerrada'):
        e['estado'] = estado
        if e['t1'] is None:
            e['t1'] = now
        if cfg['nivel'] >= 31:          # fase 31: el disparo de testigo, con su profundidad final
            encolar_testigo(W, cfg, e, now)
        return True
    return False


# --- el relampago (fase 30) --------------------------------------------------------
# Al abrirse una escision, un unico destello blanco por DMX. Pasa por el
# limitador comun de la fase 23 (como mucho 3 destellos en cualquier ventana de
# 1 s, junto con el estroboscopio): si esta lleno, el relampago espera al primer
# hueco y el estroboscopio cede ese destello (P12). Solo blanco. Profundizar la
# escision no da otro. En pantalla, la fulgurita recien abierta sube su emisivo
# un instante. Sin interfaz DMX, el evento queda en el motor y en la leyenda.

RELAMPAGO_BRILLO = 2.5          # lo que sube el emisivo de la fulgurita recien abierta
RELAMPAGO_CAIDA = 0.35          # s con los que vuelve


def relampago(W, cfg, now):
    """Pide el destello del relampago al limitador, con prioridad. Devuelve si
    ha salido ahora (si no, queda pendiente y sale en el primer hueco)."""
    s = sala_de(W)
    s['relampagos'] = s.get('relampagos', 0) + 1
    s['t_pedido'] = now
    return limitador_destellos(W, cfg, now, 'relampago', prioridad=True)


def brillo_fulgurita(cfg, e, now):
    """El emisivo de la fulgurita de la escision e: sube al abrirse (fase 30) y vuelve a 1."""
    if cfg['nivel'] < 30:
        return 1.0
    dt = now - e['t0']
    if dt < 0.0 or dt > 10.0 * RELAMPAGO_CAIDA:
        return 1.0
    return 1.0 + RELAMPAGO_BRILLO * math.exp(-dt / RELAMPAGO_CAIDA)


def escision_de(W, ide):
    return next((e for e in reversed(W['escisiones']) if e['id'] == ide), None)


def filas_reset():
    _SALA['filas'] = []
    _SALA['fila_id'] = 0


def tick_filas(W, cfg, now):
    """Cada imagen de la camara: las filas de la sala (componentes de Minfila
    personas o mas, con la forma de Modofila), lo que llevan sostenidas y sus
    escisiones. Devuelve las filas en curso."""
    cas = _SALA.get('casillas', {})
    cols, _ = rejilla_sala(cfg)
    recta = int(cfg['modo_fila']) == 1
    comps = [f for f in buscar_filas(cas, cfg) if f['personas'] >= cfg['min_fila']
             and (not recta or es_recta(f['casillas'], cols))]
    prev = _SALA.get('filas') or []
    usadas, filas = set(), []
    for f in comps:
        cs = set(f['casillas'])
        ant = next((p for p in prev if id(p) not in usadas and p['casillas'] & cs), None)
        if ant is None:
            _SALA['fila_id'] = _SALA.get('fila_id', 0) + 1
            ant = dict(id=_SALA['fila_id'], t0=now, max=0, escision=None)
        else:
            usadas.add(id(ant))
        ant.update(casillas=cs, personas=f['personas'], origen=f['origen'], max=max(ant['max'], f['personas']))
        filas.append(ant)
        if ant['escision'] is None:
            if now - ant['t0'] >= cfg['t_fila'] - 1e-9:
                ant['escision'] = abrir_escision(W, cfg, ant, f['origen'], now)['id']
        else:
            e = escision_de(W, ant['escision'])
            if e is not None:
                profundizar_escision(W, cfg, e, ant['max'], now)
    for p in prev:                      # la fila se deshace: su escision se cierra
        if id(p) not in usadas and p.get('escision') is not None:
            e = escision_de(W, p['escision'])
            if e is not None:
                cerrar_escision(W, cfg, e, now)
    _SALA['filas'] = filas
    return filas


def enterrar_escisiones(W, cfg, now):
    """El mundo se entierra: sus escisiones quedan enterradas (el hueco sigue)."""
    n = 0
    for e in W['escisiones']:
        if e['estado'] in ('abierta', 'cerrada'):
            e['estado'] = 'enterrada'
            if e['t1'] is None:
                e['t1'] = now
            e['t_noche'] = now          # sus paredes brillan en la noche de este entierro
            n += 1
        elif e.get('t_noche') is not None and e['t_noche'] != now:
            e['t_noche'] = None
    return n


def hueco_escision(W, cfg, i):
    """(fondo, borde) del hueco de la celda i: su suelo y el suelo mas alto de sus vecinas."""
    return suelo(W, cfg, i), max([suelo(W, cfg, j) for j in NEIGH[i]] or [suelo(W, cfg, i)])


def filas_fulgurita(W, cfg, e, now=0.0):
    """Las instancias de la fulgurita de la escision e: por cada concha atravesada
    que sigue a la vista (lo que queda bajo el tapiz de una concha posterior no se
    dibuja), cuatro paredes de arena fundida, cuatro laminas de vidrio por dentro,
    un nucleo emisivo y dos o tres ramas finas. El alfa lleva rugosidad + 2 x parte."""
    i = e['origen']
    fondo, borde = hueco_escision(W, cfg, i)
    alto = borde - fondo
    if alto < 1e-4:
        return []
    hondo0 = max(1e-6, e.get('hondo0') or alto)
    n = max(1, len(e['cortadas']))
    vistas = max(1, min(n, int(math.ceil(n * min(1.0, alto / hondo0) - 1e-6))))
    h = alto / vistas
    nrm = normal_i(i)
    X, Y, Z, _ = marco = _marco(i, 0)
    col_n = paleta_humana(cfg, e['ramas'])
    brillo = brillo_fulgurita(cfg, e, now)
    col_n = (col_n[0] * brillo, col_n[1] * brillo, col_n[2] * brillo)
    col_v = _mix(col_n, (0.05, 0.05, 0.06), 0.45)
    rows = []
    for k in range(vistas):
        r0 = fondo + k * h
        cw, cl = _cell_sizes(r0 + 0.5 * h, i)
        base = _mul(nrm, r0)
        concha = e['cortadas'][min(len(e['cortadas']) - 1, n - 1 - k)] if e['cortadas'] else 0
        gris = 0.85 + 0.3 * _hash01(e['id'], concha, 7)
        arena = (COL_ARENA[0] * gris, COL_ARENA[1] * gris, COL_ARENA[2] * gris)
        for sgn in (-1.0, 1.0):         # las paredes y, por dentro, el vidrio
            # al este y al oeste: finas en X, largas en Z
            rows.append(_fila_m(_add(base, X, sgn * 0.46 * cw), marco, 0.06 * cw, h, 0.98 * cl, arena)
                        + [0.9 + 2 * PARED])
            rows.append(_fila_m(_add(base, X, sgn * 0.40 * cw), marco, 0.05 * cw, h, 0.84 * cl, col_v)
                        + [0.07 + 2 * VIDRIO])
            # al norte y al sur: largas en X, finas en Z
            rows.append(_fila_m(_add(base, Z, sgn * 0.46 * cl), marco, 0.98 * cw, h, 0.06 * cl, arena)
                        + [0.9 + 2 * PARED])
            rows.append(_fila_m(_add(base, Z, sgn * 0.40 * cl), marco, 0.84 * cw, h, 0.05 * cl, col_v)
                        + [0.07 + 2 * VIDRIO])
        g = 0.07 * min(cw, cl)
        rows.append(_fila_m(base, marco, g, h, g, col_n) + [0.10 + 2 * NUCLEO])
        # las ramas de esta concha: solo visuales
        x0 = 0.05 + 0.9 * _frac(e['ramas'] + concha * AUREO + e['id'] * 0.137)
        us = logistica(x0, 4.0, 4)
        nr = FULG_RAMAS[0] + (1 if us[0] > 0.5 else 0)
        for j in range(nr):
            ang = int(360.0 * _frac(us[j + 1] + j / float(nr))) // 15 * 15
            mr = _marco(i, ang)
            L = 0.36 * min(cw, cl)
            p = _add(_add(base, mr[0], 0.5 * L), nrm, h * (0.25 + 0.5 * _frac(us[j + 1] * 7.3)))
            rows.append(_fila_m(p, mr, L, 0.10 * h, 0.03 * min(cw, cl), col_n) + [0.10 + 2 * NUCLEO])
    return rows


def build_fulguritas(W, cfg, now, out):
    """Las fulguritas de todas las escisiones con el hueco a la vista."""
    rows = []
    for e in W['escisiones']:
        rows += filas_fulgurita(W, cfg, e, now)
    out['fulguritas'] = rows
    return rows


# -----------------------------------------------------------------------------
# 1. NUCLEO - las escisiones en el historico (fase 31)
# -----------------------------------------------------------------------------
# TESTIGO: cada escision exporta una imagen cuando su fila se deshace o cuando
# se entierra su mundo, lo que ocurra antes, con su profundidad final. Una sola
# vez. La imagen es la SECCION POR EL ORIGEN: un corte del planeta por la celda
# de origen y unas celdas a cada lado de su anillo, desde la superficie hasta la
# ultima concha atravesada. Se dibuja aqui, con numpy, a partir de las columnas:
# cada loseta es una banda de su color, las bandas humanas con sus motas y la
# escision con su fulgurita (paredes de arena fundida, vidrio, nucleo y ramas).
# Sin un segundo render ni planos de recorte: se prueba fuera de TouchDesigner.
# COLUMNA DE LA JORNADA: una banda por ciclo de la jornada (humana, limpia, con
# colapso o sin el), de la mas antigua abajo a la mas nueva arriba; cada
# escision es una veta que une las bandas que atraveso, con un ancho
# proporcional a sus personas.
# REGISTRO: jornada, ciclo, hora, personas, conchas cruzadas y celda de origen
# de cada escision, en la tabla escisiones y en historico/escisiones.csv.
# La jornada, hasta que exista la de D5, es la fecha del sistema al abrirse la
# escision (P13). Las imagenes pendientes de guardar viven en _HIST (modulo).

SECCION_PX = (640, 360)         # ancho x alto de la seccion
COLUMNA_PX = (200, 720)         # y de la columna de la jornada
SECCION_LADO = 2                # celdas a cada lado del origen
FRANJA_SUP = 0.12               # la banda de superficie: esta fraccion del alto
COL_HUECO = (0.03, 0.03, 0.035)
COL_CIELO = (0.0, 0.0, 0.0)
COL_SUELO_VIVO = (0.20, 0.20, 0.21)
REGISTRO_COLS = ['id', 'jornada', 'ciclo', 'hora', 'personas', 'conchas', 'celda', 'estado', 'testigo']
_HIST = dict(pend=[], imagen=None, meta=None, exportadas=0, avisos=[])


def hist_reset():
    _HIST.update(pend=[], imagen=None, meta=None, exportadas=0, avisos=[])


def celdas_seccion(i, lado=SECCION_LADO):
    """Las celdas de la seccion: el origen en el centro y 'lado' a cada lado, por su anillo."""
    if is_pole(i):
        nb = list(NEIGH[i])
        return list(reversed(nb[:lado])) + [i] + nb[lado:2 * lado]
    R = RINGS[RING_OF[i]]
    q = R.index(i)
    lado = min(lado, (len(R) - 1) // 2)
    return [R[(q + d) % len(R)] for d in range(-lado, lado + 1)]


def _tramo_de(W, cfg, celdas, s):
    """(r_in, r_out) de la concha s en la primera celda de la lista que la conserve."""
    for c in celdas:
        for s2, r_in, r_out in column_radii(W, cfg, c):
            if s2 == s:
                return c, r_in, r_out
    return None, None, None


def _motas(np, img, y0, y1, x0, x1, cob, s, c):
    """Las motas de una banda humana: bloques de la paleta humana, sin azar."""
    paso = 6
    for gy in range(y0, y1, paso):
        for gx in range(x0, x1, paso):
            if _hash01(s, c, gx, gy) < cob:
                col = PALETA_HUMANA_8[int(_hash01(gy, gx, c, s, 3) * 8) % 8]
                img[gy:min(y1, gy + paso - 2), gx:min(x1, gx + paso - 2), :3] = col


def seccion_escision(W, cfg, e, ancho=None, alto=None):
    """La seccion por el origen de la escision e: (imagen alto x ancho x 4, float32,
    la fila 0 arriba; meta). meta['bandas'] son las bandas que cruza, de arriba
    abajo: la de superficie y una por concha atravesada, con su color y sus filas
    de pixeles. None sin numpy."""
    np = _np()
    if np is None:
        return None, None
    ancho = int(ancho or SECCION_PX[0])
    alto = int(alto or SECCION_PX[1])
    i = e['origen']
    celdas = celdas_seccion(i)
    otras = [c for c in celdas if c != i]
    tramos = [(s,) + _tramo_de(W, cfg, otras, s)[1:] for s in e['cortadas']]
    r_top = max(suelo(W, cfg, c) for c in celdas)
    fondos = [t[1] for t in tramos if t[1] is not None]
    r_bot = min(fondos + [suelo(W, cfg, i)]) if fondos else suelo(W, cfg, i)
    if r_top - r_bot < 1e-6:
        r_bot = r_top - max(1e-3, cfg['shell_thick'])
    ys = int(round(FRANJA_SUP * alto))

    def fila_de(r):
        return int(round(ys + (r_top - r) / (r_top - r_bot) * (alto - ys)))
    img = np.zeros((alto, ancho, 4), dtype=np.float32)
    img[..., 3] = 1.0
    img[..., :3] = COL_CIELO
    wc = ancho // len(celdas)
    for j, c in enumerate(celdas):
        x0, x1 = j * wc + 1, (j + 1) * wc - 1
        for s, r_in, r_out in column_radii(W, cfg, c):
            y0, y1 = max(ys, fila_de(min(r_out, r_top))), min(alto, fila_de(max(r_in, r_bot)))
            if y1 <= y0:
                continue
            sh = W['shells'][s]
            img[y0:y1, x0:x1, :3] = tile_material(cfg, sh, s, c)[0]
            q = cobertura_q(cfg, sh, c)
            if q:
                _motas(np, img, y0, y1, x0, x1, q / float(COB_PASOS), s, c)
            img[y0:y0 + 1, x0:x1, :3] *= 0.6                     # el limite entre conchas
        if c != i:                                                  # la superficie viva de cada celda
            vivo = W['occ'][c] > 0
            col = seq_color(cfg, 1 if W['own'][c] == GEO else 2) if vivo else COL_SUELO_VIVO
            ysu = fila_de(suelo(W, cfg, c))
            img[max(0, ysu - 6):ysu, x0:x1, :3] = col
    # el hueco de la escision y su fulgurita
    j = celdas.index(i)
    x0, x1 = j * wc + 1, (j + 1) * wc - 1
    yf = min(alto, fila_de(max(r_bot, suelo(W, cfg, i))))
    img[0:yf, x0:x1, :3] = COL_HUECO
    w = x1 - x0
    col_n = paleta_humana(cfg, e['ramas'])
    col_v = _mix(col_n, (0.05, 0.05, 0.06), 0.45)
    pa, pv, pn = max(2, int(0.07 * w)), max(2, int(0.05 * w)), max(2, int(0.04 * w))
    xc = (x0 + x1) // 2
    bandas = [dict(concha='superficie', color=COL_HUECO, y0=0, y1=ys)]
    for k, (s, r_in, r_out) in enumerate(tramos):
        if r_in is None:                # nadie conserva esa concha: reparto a partes iguales
            h = (r_top - r_bot) / max(1, len(tramos))
            r_out, r_in = r_top - k * h, r_top - (k + 1) * h
        y0, y1 = max(ys, fila_de(min(r_out, r_top))), min(yf, fila_de(max(r_in, r_bot)))
        vecina = _tramo_de(W, cfg, otras, s)[0]
        bandas.append(dict(concha=s, color=tile_material(cfg, W['shells'][s], s, vecina if vecina is not None else i)[0],
                           y0=y0, y1=y1))
        if y1 <= y0:
            continue
        gris = 0.85 + 0.3 * _hash01(e['id'], s, 7)
        arena = [x * gris for x in COL_ARENA]
        img[y0:y1, x0:x0 + pa, :3] = arena
        img[y0:y1, x1 - pa:x1, :3] = arena
        img[y0:y1, x0 + pa:x0 + pa + pv, :3] = col_v
        img[y0:y1, x1 - pa - pv:x1 - pa, :3] = col_v
        img[y0:y1, xc - pn // 2:xc - pn // 2 + pn, :3] = col_n
        us = logistica(0.05 + 0.9 * _frac(e['ramas'] + s * AUREO + e['id'] * 0.137), 4.0, 4)
        for q in range(FULG_RAMAS[0] + (1 if us[0] > 0.5 else 0)):  # las ramas, hacia una pared o la otra
            yr = y0 + int((0.25 + 0.5 * _frac(us[q + 1] * 7.3)) * (y1 - y0))
            if math.cos(2.0 * math.pi * _frac(us[q + 1] + q / 3.0)) >= 0.0:
                img[yr:yr + 2, xc:x1 - pa - pv, :3] = col_n
            else:
                img[yr:yr + 2, x0 + pa + pv:xc, :3] = col_n
    meta = dict(id=e['id'], celdas=celdas, bandas=bandas, r_top=r_top, r_bot=r_bot, ancho=ancho, alto=alto,
                columna=wc)
    return img, meta


def encolar_testigo(W, cfg, e, now):
    """El disparo de testigo de la escision e: dibuja su seccion y la deja pendiente
    de guardar. Una sola vez por escision. Devuelve si la ha encolado."""
    if e.get('testigo'):
        return False
    img, meta = seccion_escision(W, cfg, e)
    if img is None:
        return False
    e['testigo'] = 'pendiente'
    _HIST['pend'].append((e['id'], img, meta))
    return True


def testigos_al_enterrar(W, cfg, now):
    """Antes de enterrar el mundo: el testigo de las escisiones que aun no lo tienen."""
    return sum(1 for e in W['escisiones'] if e['estado'] in ('abierta', 'cerrada') and encolar_testigo(W, cfg, e, now))


def nombre_testigo(e):
    return 'escision_%s_c%s_%d.png' % (e.get('jornada', ''), e.get('ciclo', ''), e['id'])


def ciclos_jornada(W, jornada):
    """Las conchas enterradas en la jornada: [(indice, concha)], de la mas antigua a la mas nueva."""
    return [(s, sh) for s, sh in enumerate(W['shells']) if sh.get('jornada') == jornada]


def tipo_banda(sh):
    b, _, col = banda_de(sh)
    return b + (' + colapso' if col else '')


def columna_jornada(W, cfg, jornada, ancho=None, alto=None):
    """La columna resumen de la jornada: (imagen, meta). Una banda por ciclo (la mas
    antigua abajo), del color de su concha: las humanas con motas, las de colapso
    con una franja oscura arriba. Cada escision de la jornada es una veta de la
    paleta humana que une las bandas que atraveso, con un ancho proporcional a
    sus personas. meta: bandas [(ciclo, tipo, y0, y1)] de arriba abajo y vetas
    [(id, personas, x0, x1, y0, y1)]."""
    np = _np()
    if np is None:
        return None, None
    ancho = int(ancho or COLUMNA_PX[0])
    alto = int(alto or COLUMNA_PX[1])
    img = np.zeros((alto, ancho, 4), dtype=np.float32)
    img[..., 3] = 1.0
    ciclos = ciclos_jornada(W, jornada)
    n = len(ciclos)
    meta = dict(jornada=jornada, bandas=[], vetas=[], ancho=ancho, alto=alto)
    if not n:
        return img, meta
    hb = alto / float(n)
    y_de = {}
    for k, (s, sh) in enumerate(ciclos):            # k = 0 la mas antigua: abajo
        y1 = int(round(alto - k * hb))
        y0 = int(round(alto - (k + 1) * hb))
        y_de[s] = (y0, y1)
        img[y0:y1, :, :3] = tile_color(cfg, sh, 0, s)
        b, huellas, col = banda_de(sh)
        if b == 'humana':
            _motas(np, img, y0, y1, 0, ancho, max(0.05, cobertura_concha(cfg, sh)), s, 0)
        if col:
            img[y0:y0 + max(2, int(0.18 * (y1 - y0))), :, :3] *= 0.25
        img[y1 - 1:y1, :, :3] *= 0.5
        meta['bandas'].insert(0, (sh.get('ciclo', s), tipo_banda(sh), y0, y1))
    esc = [e for e in W['escisiones'] if e.get('jornada') == jornada]
    unidad = max(2.0, ancho / 40.0)
    for q, e in enumerate(esc):
        cruza = [y_de[s] for s in e['cortadas'] if s in y_de]
        propia = [y_de[s] for s, sh in ciclos if sh.get('ciclo') == e.get('ciclo')]
        tramo = cruza + propia
        if not tramo:
            continue
        y0, y1 = min(t[0] for t in tramo), max(t[1] for t in tramo)
        wv = int(round(e['personas'] * unidad))
        xc = int((0.12 + 0.76 * _frac((q + 1) * AUREO)) * ancho)
        x0 = max(0, min(ancho - wv, xc - wv // 2))
        img[y0:y1, x0:x0 + wv, :3] = paleta_humana(cfg, e['ramas'])
        meta['vetas'].append((e['id'], e['personas'], x0, x0 + wv, y0, y1))
    return img, meta


def linea_registro(e):
    """La linea del fichero historico/escisiones.csv de la escision e (separador ;)."""
    return ';'.join(str(x) for x in [e['id'], e.get('jornada', ''), e.get('ciclo', ''), e.get('hora', ''),
                                     e['personas'], len(e['cortadas']), e['origen'], e['estado'],
                                     e.get('testigo') or ''])


# -----------------------------------------------------------------------------
# 1. NUCLEO - la luz de la sala (fase 23): balance, bano, estroboscopio y colapso
# -----------------------------------------------------------------------------
# La sala se ilumina con el estado del planeta. En una ventana de Ventanabalance
# segundos se compara la ocupacion destruida con la depositada, en escalones de
# ocupacion (D6): el BALANCE es erosion / creacion. La erosion suma los pads de
# erosion (caja y aranazos), sus cortes y el microfono; la creacion, las notas
# de los secuenciadores y los pulsos del bombo y el tom.
#   deposito   (balance < 0,5)  casi a oscuras: ambar tenue que respira con
#              cada nota depositada.
#   tension    (0,5 a 1)        la intensidad sube y vira a blanco frio; cada
#              onset del microfono anade un pulso breve.
#   erosion dominante (> 1)     estroboscopio blanco; su frecuencia crece con el
#              exceso, hasta Maxhz. Entra con Umbralestrobo y sale por debajo de
#              Salidaestrobo (histeresis).
#   fin de ciclo               un unico destello blanco y oscuridad durante
#              Noche segundos (D7).
# SEGURIDAD (no son parametros que se puedan saltar): como mucho DESTELLOS_MAX
# (3) destellos en cualquier ventana de 1 s, contando TODOS los de la sala en un
# solo limitador (el relampago de la fase 30 pasa por el con prioridad: espera
# al primer hueco y el estroboscopio cede ese destello); el estroboscopio solo
# destella en blanco; el fin de ciclo lo apaga. Cada destello queda en
# W['sala']['destellos'] para que el microfono descarte su clic.
# El colapso (D8), apagado por defecto: con Colapsoon, Maxerosion segundos
# seguidos con el balance por encima de 1 cierran el ciclo con el motivo
# 'colapso'. 'estancado' no es colapso.

DESTELLOS_MAX = 3               # destellos por segundo de toda la sala (WCAG 2.3.1): tope duro
VENTANA_DESTELLOS = 1.0
DUR_DESTELLO = 0.05             # lo que dura encendido un destello (s)
ESTADOS_SALA = ['deposito', 'tension', 'erosion dominante']
DEPOSITO, TENSION, DOMINANTE = 0, 1, 2
BALANCE_TENSION = 0.5
BALANCE_COLAPSO = 1.0           # el colapso cuenta el tiempo con el balance por encima de 1
BALANCE_SIN_CREACION = 99.0     # erosion sin creacion en la ventana
COL_AMBAR = (1.0, 0.62, 0.22)
COL_FRIO = (0.82, 0.90, 1.0)
BANO_SUAVE = 0.4                # s con los que el bano persigue a su estado
INTERFACES_DMX = ['artnet', 'usbpro']
DMX_COLS = ['canal', 'funcion', 'foco']
# funciones de un canal: el bano con dimmer aparte (bano_dimmer + bano_rojo...), o
# con la intensidad en el color (bano_r, bano_g, bano_b), y el estroboscopio
# (cualquier destello de la sala: el suyo, el del fin de ciclo y el relampago); 'relampago'
# (fase 30) es solo para un foco propio del relampago
FUNCIONES_DMX = ['bano_dimmer', 'bano_rojo', 'bano_verde', 'bano_azul', 'bano_r', 'bano_g', 'bano_b', 'estrobo',
                 'relampago']
DMX_DEFECTO = ([[4 * k + j + 1, f, 'bano%d' % (k + 1)] for k in range(4)
                for j, f in enumerate(FUNCIONES_DMX[:4])] + [[17, 'estrobo', 'estrobo']])
SALA_BASE = dict(bal=[], estado=DEPOSITO, balance=0.0, hz=0.0, estrobo_t=-99.0, ultimo=None, pend=None,
                 noche=None, desde=None, t_nota=-99.0, bano=[0.0, 0.0, 0.0, 0.0], t_luz=None, n=0,
                 cedidos=0)


def sala_de(W):
    """W['sala'], con las claves de la fase 23."""
    s = W['sala']
    for k, v in SALA_BASE.items():
        if k not in s:
            s[k] = list(v) if isinstance(v, list) else v
    return s


def balance_suma(W, cfg, now, crea=0, eros=0):
    """Apunta escalones de ocupacion ganados (crea) o perdidos (eros)."""
    if crea <= 0 and eros <= 0:
        return
    s = sala_de(W)
    s['bal'].append([now, max(0, int(crea)), max(0, int(eros))])
    if crea > 0:
        s['t_nota'] = now


def balance(W, cfg, now):
    """Erosion entre creacion en la ventana de Ventanabalance s. Sin creacion y con
    erosion, erosion dominante (BALANCE_SIN_CREACION); sin nada, 0. Simbalance >= 0
    lo fuerza."""
    s = sala_de(W)
    v = max(0.0, cfg['ventana_balance'])
    s['bal'] = [e for e in s['bal'] if 0.0 <= now - e[0] <= v]
    if cfg['sim_balance'] >= 0.0:
        b = float(cfg['sim_balance'])
    else:
        crea = sum(e[1] for e in s['bal'])
        eros = sum(e[2] for e in s['bal'])
        b = eros / float(crea) if crea > 0 else (BALANCE_SIN_CREACION if eros > 0 else 0.0)
    s['balance'] = b
    return b


def estado_sala(W, cfg, now=None, b=None):
    """El estado de la luz (DEPOSITO, TENSION o DOMINANTE) con histeresis: entra
    en erosion dominante con Umbralestrobo y no sale hasta bajar de Salidaestrobo."""
    s = sala_de(W)
    if b is None:
        b = balance(W, cfg, now if now is not None else (W.get('t') or 0.0))
    entra = cfg['umbral_estrobo']
    sale = min(cfg['salida_estrobo'], entra)
    if s['estado'] == DOMINANTE:
        dom = b >= sale
    else:
        dom = b >= entra
    s['estado'] = DOMINANTE if dom else (TENSION if b >= BALANCE_TENSION else DEPOSITO)
    return s['estado']


def en_noche(W, now):
    n = W['sala'].get('noche')
    return bool(n) and n[0] <= now < n[1]


def destellos_ventana(W, now):
    """Destellos de toda la sala en la ultima ventana de 1 s."""
    return sum(1 for t in W['sala']['destellos'] if 0.0 <= now - t <= VENTANA_DESTELLOS)


def _hueco(W, cfg, now):
    tope = min(DESTELLOS_MAX, int(math.floor(cfg['max_hz'] + 1e-9)))
    return destellos_ventana(W, now) < tope


def _destello(W, now, quien):
    s = sala_de(W)
    s['destellos'].append(now)
    s['destellos'] = [t for t in s['destellos'] if now - t <= 5.0]
    s['ultimo'] = dict(t=now, quien=quien)
    s['n'] += 1
    if quien == 'relampago':
        s['t_relampago'] = now
    return True


def limitador_destellos(W, cfg, now, quien='estrobo', prioridad=False):
    """El limitador comun de destellos: concede uno si en la ultima ventana de 1 s
    hay menos de DESTELLOS_MAX (y de Maxhz). Con prioridad (el relampago y el fin de
    ciclo), si no hay hueco el destello queda pendiente: sale en el primero, y el
    estroboscopio cede. Devuelve si el destello ha salido ahora."""
    s = sala_de(W)
    if s['pend'] and not prioridad:
        return False                    # el estroboscopio cede el hueco al pendiente
    if _hueco(W, cfg, now):
        if prioridad and s['pend']:
            s['pend'] = None
        return _destello(W, now, quien)
    if prioridad and not s['pend']:
        s['pend'] = dict(t=now, quien=quien)
    return False


def hz_estrobo(cfg, b):
    """Destellos por segundo del estroboscopio: crece con el exceso del balance
    sobre Salidaestrobo, hasta Maxhz (y nunca mas de DESTELLOS_MAX)."""
    entra = cfg['umbral_estrobo']
    sale = min(cfg['salida_estrobo'], entra)
    x = (b - sale) / max(1e-6, 2.0 * (entra - sale)) if entra > sale else 1.0
    return min(DESTELLOS_MAX, max(0.0, cfg['max_hz'])) * max(0.0, min(1.0, x))


def sala_luz_tick(W, cfg, now):
    """Cada fotograma: el balance y el estado, el destello pendiente, el
    estroboscopio y el colapso. Devuelve 'colapso' si toca cerrar el ciclo."""
    s = sala_de(W)
    b = balance(W, cfg, now)
    est = estado_sala(W, cfg, now, b)
    noche = en_noche(W, now)
    if s['noche'] and now >= s['noche'][1]:
        s['noche'] = None
    if s['pend'] and _hueco(W, cfg, now):           # el destello con prioridad, en el primer hueco
        quien = s['pend']['quien']
        s['pend'] = None
        _destello(W, now, quien)
        if s['hz'] > 0.0:               # era el hueco del estroboscopio: lo cede y espera su turno
            s['cedidos'] += 1
            s['estrobo_t'] = now
    s['hz'] = hz_estrobo(cfg, b) if est == DOMINANTE and not noche else 0.0
    if s['hz'] > 0.0 and now - s['estrobo_t'] >= 1.0 / s['hz'] - 1e-9:
        if limitador_destellos(W, cfg, now, 'estrobo'):
            s['estrobo_t'] = now
    # el bano persigue a su estado
    obj = _bano_objetivo(W, cfg, now, b, est, noche)
    dt = 0.0 if s['t_luz'] is None else max(0.0, min(0.25, now - s['t_luz']))
    s['t_luz'] = now
    a = 1.0 if noche or s['bano'] == [0.0, 0.0, 0.0, 0.0] else 1.0 - math.exp(-dt / BANO_SUAVE)
    s['bano'] = [x + (o - x) * a for x, o in zip(s['bano'], obj)]
    # colapso (D8)
    if cfg['colapso_on'] and b > BALANCE_COLAPSO and not noche:
        if s['desde'] is None:
            s['desde'] = now
        if now - s['desde'] >= cfg['max_erosion']:
            s['desde'] = None
            return 'colapso'
    else:
        s['desde'] = None
    return None


def _bano_objetivo(W, cfg, now, b, est, noche):
    if noche:
        return [0.0, 0.0, 0.0, 0.0]
    s = W['sala']
    if est == DEPOSITO:
        return list(COL_AMBAR) + [0.04 + 0.10 * math.exp(-max(0.0, now - s['t_nota']) / 0.8)]
    x = 1.0 if est == DOMINANTE else max(0.0, min(1.0, (b - BALANCE_TENSION) / BALANCE_TENSION))
    return [a + (f - a) * x for a, f in zip(COL_AMBAR, COL_FRIO)] + [0.15 + 0.55 * x]


def bano_valor(W, cfg, now):
    """(r, g, b, intensidad) del bano de luz, 0-1: el del estado mas, fuera del
    deposito, un pulso breve por cada onset del microfono. A oscuras en la noche."""
    s = sala_de(W)
    if en_noche(W, now):
        return (0.0, 0.0, 0.0, 0.0)
    r, g, b_, dim = s['bano']
    if s['estado'] != DEPOSITO:
        dim += 0.25 * math.exp(-max(0.0, now - W['mic']['t']) / 0.15)
    return (r, g, b_, max(0.0, min(1.0, dim)))


def destello_valor(W, now):
    """1 mientras dura un destello (blanco: r = g = b), 0 si no."""
    u = W['sala'].get('ultimo')
    return 1.0 if u and 0.0 <= now - u['t'] < DUR_DESTELLO else 0.0


def color_destello(W, now):
    v = destello_valor(W, now)
    return (v, v, v)                    # solo blanco


def sala_fin_ciclo(W, cfg, now):
    """Al enterrar: un unico destello blanco (con prioridad), el estroboscopio
    apagado y la sala a oscuras durante Noche s. El balance empieza de cero con
    el mundo nuevo."""
    s = sala_de(W)
    s['bal'] = []
    s['estado'] = DEPOSITO
    s['hz'] = 0.0
    s['desde'] = None
    s['estrobo_t'] = now
    s['bano'] = [0.0, 0.0, 0.0, 0.0]
    limitador_destellos(W, cfg, now, 'fin de ciclo', prioridad=True)
    s['noche'] = [now, now + cfg['noche']] if cfg['noche'] > 0.0 else None


def valores_dmx(W, cfg, now, filas):
    """El valor 0-255 de cada fila [canal, funcion, foco] de dmx_canales."""
    r, g, b_, dim = bano_valor(W, cfg, now)
    fl = destello_valor(W, now)
    u = W['sala'].get('ultimo')
    v = dict(bano_dimmer=dim, bano_rojo=r, bano_verde=g, bano_azul=b_, bano_r=r * dim, bano_g=g * dim,
             bano_b=b_ * dim, estrobo=fl, relampago=fl if u and u.get('quien') == 'relampago' else 0.0)
    return [int(round(255.0 * max(0.0, min(1.0, v.get(str(f[1]).strip(), 0.0))))) for f in filas]



_CACHE = {'frame': None, 'inst': None, 'printed': {}}

CHOP_NAMES = ['i_formas_pulidas', 'i_formas_porosas', 'i_coronas',
              'i_estratos', 'i_luz_celda', 'i_luz_conchas']


def chop_names(c=None):
    """Los Script CHOP de instancias; desde la fase 11, tambien los de los
    modelos y el de las particulas."""
    c = c or cfg()
    if c['nivel'] < 11:
        return list(CHOP_NAMES)
    extra = ['i_tejido', 'i_rios'] if c['nivel'] >= 13 else []
    extra += ['i_luz_local', 'i_diagnostico'] if c['nivel'] >= 18 else []
    extra += ['i_inclusiones'] if c['nivel'] >= 25 else []
    extra += ['i_fulguritas'] if c['nivel'] >= 29 else []
    # motor v75: i_humo (el humo en la GPU, v74: sin esto sus filas no se recocian) e
    # i_vagones (los trenes, en cajas; las demas particulas son motas suaves)
    return CHOP_NAMES + ['i_particulas', 'i_humo', 'i_vagones'] + extra + \
        ['i_' + g for g, _, _ in geometrias_piel(c)]

TARGET_MODES = ['seq1', 'seq2', 'alterna', 'velocidad']


def _p(name, default):
    try:
        p = getattr(parent().par, name, None)
        if p is None:
            return default
        v = p.eval()
        if isinstance(default, bool):
            return bool(v)
        if isinstance(default, int):
            if isinstance(v, str):
                return v
            return int(v)
        if isinstance(default, float):
            return float(v)
        return v
    except Exception:
        return default


def _menu(name, options, default):
    v = _p(name, options[default])
    if isinstance(v, str):
        return options.index(v) if v in options else default
    try:
        return int(v)
    except Exception:
        return default


def _perfiles(n=8):
    """(perfiles, tipos, modos, pulsos, caidas del pumping) de los n primeros
    pads (9 desde la fase 21: el noveno es el microfono) de la tabla
    perfiles_erosion, leidos por nombre de columna (la columna rol es solo
    para leer). Sin las columnas modo y pulsos (o capacidad, su nombre en
    la v12 y la v13), las de por defecto: bombo 3 y tom 2 en impulso; sin
    pump_rel (antes de la v13), 0,20 s el bombo y 0,12 el tom."""
    t = parent().op('perfiles_erosion')
    if t is None or t.numRows < 2:
        return (list(PERFILES_PADS[:n]), list(TIPOS_PADS[:n]), list(MODOS_PADS[:n]), list(PULSOS_PADS[:n]),
                list(PUMP_REL_PADS[:n]))
    out, tipos, modos, caps, rels = [], [], [], [], []
    for r in range(1, min(t.numRows, n + 1)):
        try:
            p = (int(float(t[r, 'reduccion'].val)), int(float(t[r, 'radio'].val)),
                 int(float(t[r, 'profundidad'].val)))
        except Exception:
            p = PERFILES_PADS[r - 1]
        out.append(p)
        try:
            md = t[r, 'modo'].val.strip().lower()
        except Exception:
            md = ''
        modos.append(md if md in MODOS_PAD else MODOS_PADS[r - 1])
        try:
            col = 'pulsos' if t[0, 'pulsos'] is not None else 'capacidad'
            caps.append(max(1, int(round(float(t[r, col].val)))))
        except Exception:
            caps.append(PULSOS_PADS[r - 1])
        try:
            rels.append(max(0.0, float(t[r, 'pump_rel'].val)))
        except Exception:
            rels.append(PUMP_REL_PADS[r - 1])
        try:
            tp = t[r, 'tipo'].val.strip()
        except Exception:
            tp = ''
        tipos.append(tp or ('impulso' if modos[-1] == 'impulso' else tipo_perfil(*p)))
    while len(out) < n:
        out.append(PERFILES_PADS[len(out)])
        tipos.append(TIPOS_PADS[len(tipos)])
        modos.append(MODOS_PADS[len(modos)])
        caps.append(PULSOS_PADS[len(caps)])
        rels.append(PUMP_REL_PADS[len(rels)])
    return out, tipos, modos, caps, rels


def _catalogo():
    """El catalogo de la tabla 'catalogo' (tema especie estado variante
    modelo). Se relee cada medio segundo (60 fps): un cambio en la tabla
    llega enseguida sin leerla en cada fotograma. Sin tabla, el de por defecto."""
    f = _CACHE.get('cat_frame')
    if f is not None and 0 <= absTime.frame - f < 30 and _CACHE.get('cat') is not None:
        return _CACHE['cat']
    t = parent().op('catalogo')
    cat = CATALOGO
    filas = None
    if t is not None and t.numRows > 1:
        filas = []
        for r in range(1, t.numRows):
            try:
                filas.append((t[r, 'tema'].val.strip(), t[r, 'especie'].val.strip(),
                              t[r, 'estado'].val.strip(), int(float(t[r, 'variante'].val)),
                              t[r, 'modelo'].val.strip()))
            except Exception:
                pass
        # motor v101: la tabla igual, el mismo catalogo (el mismo objeto): las caches que lo
        # miran (la piel por turnos, la arqueologia, los edificios) no se vacian cada medio segundo
        if filas == _CACHE.get('cat_filas') and _CACHE.get('cat') is not None:
            cat = _CACHE['cat']
        else:
            cat = catalogo_de(filas) or CATALOGO
    _CACHE['cat'], _CACHE['cat_frame'], _CACHE['cat_filas'] = cat, absTime.frame, filas
    return cat


def _colores_drum(n=8):
    """Colores de las balizas de la bateria (tabla colores_drum: pad r g b) de
    los n primeros pads (9 desde la fase 21: el microfono)."""
    t = parent().op('colores_drum')
    out = list(COLORES_PADS[:n])
    if t is None or t.numRows < 2:
        return out
    for r in range(1, t.numRows):
        try:
            k = int(float(t[r, 'pad'].val)) - 1
            if 0 <= k < n:
                out[k] = tuple(max(0.0, min(1.0, float(t[r, ch].val))) for ch in ('r', 'g', 'b'))
        except Exception:
            pass
    return out


def cfg():
    c = dict(DEFAULT_CFG)
    c.update(
        nivel=_p('Nivel', 3),
        luz_seq=int(_p('Luzseq', True)),
        # v58: Luzconchas es una intensidad (0 apaga; un toggle viejo da 0 o 1)
        luz_conchas=int(_p('Luzconchas', 1.0) > 0.0),
        luz_conchas_pulso=c['luz_conchas_pulso'] * max(0.0, _p('Luzconchas', 1.0)),
        luz_conchas_reposo=c['luz_conchas_reposo'] * max(0.0, _p('Luzconchas', 1.0)),
        shell_thick=_p('Shellthick', c['shell_thick']),
        height_factor=_p('Alturafactor', c['height_factor']),
        seed_frac=_p('Semillafrac', c['seed_frac']),
        cost_max=_p('Costemax', c['cost_max']),
        gate_max=_p('Gatemax', c['gate_max']),
        vel_umbral=_p('Umbralvel', c['vel_umbral']),
        th_branch=_p('Umbralram', c['th_branch']),
        cumbre_tramos=_p('Tramoscumbre', c['cumbre_tramos']),
        sat_size=_p('Satelite', c['sat_size']),
        sat_limit=_p('Satelite', c['sat_limit']),
        beats_per_bar=_compas(c['beats_per_bar']),
        umbral_madurez=_p('Umbralmadurez', c['umbral_madurez']),
        umbral_novedad=_p('Umbralnovedad', c['umbral_novedad']),
        compases_quietos=_p('Compasesquietos', c['compases_quietos']),
        umbral_territorio=_p('Umbralterritorio', c['umbral_territorio']),
        ciclo_min=_p('Ciclomin', c['ciclo_min']),
        ciclo_max=_p('Ciclomax', c['ciclo_max']),
        cambio_entierra=int(_p('Cambioentierra', False)),
        giro_vivo=int(_p('Giromin', c['giro_min']) < 1.0),    # v60: Giromin 1 = sin giro vivo
        giro_min=_p('Giromin', c['giro_min']),
        dens_umbral=_p('Umbraldensidad', c['dens_umbral']),
        target_mode=_menu('Objetivo', TARGET_MODES, 2),
        herencia=_p('Herencia', c['herencia']),
        paleta=_menu('Paleta', PALETAS, 0),
        paleta_tono=_p('Paletatono', c['paleta_tono']) % 360.0,
        paleta_croma=max(0.0, min(0.15, _p('Paletacroma', c['paleta_croma']))),
        paleta_luz=max(0.05, min(0.95, _p('Paletaluz', c['paleta_luz']))),
        tapa_neutra=max(0.0, min(1.0, _p('Tapaneutra', c['tapa_neutra']))),
        max_shells=_p('Maxconchas', c['max_shells']),
        grosor_tiempo=int(_p('Grosortiempo', True)),
        grosor_max=_p('Grosormax', c['grosor_max']),
        corteza_max=max(0.0, _p('Cortezamax', c['corteza_max'])),
        colmatacion=max(0.0, min(1.0, _p('Colmatacion', c['colmatacion']))),
        scar_time=max(0.1, _p('Cicatriz', c['scar_time'])),
        flash=_p('Destello', c['flash']),
    )
    # motor v58: el crecimiento por trigger ya no es un parametro (Growstep):
    # escalones iguales de la semilla al limite. Gatemax 1 apaga el gate.
    c['grow_frac'] = growstep_coherente(c['seed_frac'], c['th_branch'])
    c['gate_mode'] = int(c['gate_max'] > 1.0 + 1e-6)
    # motor v62: el gris de la tapa sigue a la luminosidad de las conchas
    c['tapa_luz'] = TAPA_LUZ_K * c['paleta_luz']
    # motor v59: fusion, corona y cumbre, a Pasoumbral ocupaciones una de otra
    paso = max(1, int(_p('Pasoumbral', PASO_UMBRAL_DEF)))
    c.update(th_fusion=c['th_branch'] + paso, th_crown=c['th_branch'] + 2 * paso,
             th_cumbre=c['th_branch'] + 3 * paso)
    if c['nivel'] >= 7:
        pads = PAD_MIC + 1 if c['nivel'] >= 21 else 8        # fase 21: el pad 9 es el microfono
        c['perfiles'], c['tipos'], c['modos'], c['pulsos'], c['pump_rels'] = _perfiles(pads)
        c['colores_drum'] = _colores_drum(pads)
        # v61: cada intensidad a 0 apaga lo suyo (antes Balizasdrum,
        # Erosionvel y Pumpon); Multradio, Pumphold y Pumpvelmin, fijos
        luz = max(0.0, _p('Luzdrum', c['luz_drum']))
        vr = int(_p('Velref', c['vel_ref']))
        amt = max(0.0, _p('Pumpamt', c['pump_amt']))
        c.update(balizas_drum=int(luz > 0.0), luz_drum=luz,
                 erosion_vel=int(vr > 0), vel_ref=vr if vr > 0 else c['vel_ref'],
                 vida_baliza_drum=_p('Vidabalizadrum', c['vida_baliza_drum']),
                 # fase 7 v12: impulso
                 pump_amt=amt, pump_on=int(amt > 0.0),
                 pump_horz=max(0.0, _p('Pumphorz', c['pump_horz'])),
                 pump_tope=max(1.0, _p('Pumptope', c['pump_tope'])))          # v14
    if c['nivel'] >= 11:
        c.update(tema=_menu('Tema', TEMAS, 0),
                 peso_vecina=max(0.0, _p('Pesovecina', c['peso_vecina'])),
                 umbral_vecindad=_p('Umbralvecindad', c['umbral_vecindad']),
                 min_cluster=max(2, int(_p('Mincluster', c['min_cluster']))),
                 caos=max(0.0, min(4.0, _p('Caos', c['caos']))),
                 max_piezas=max(1, int(_p('Maxpiezas', c['max_piezas']))),
                 avance=_menu('Avance', AVANCES, 0),
                 pasos_etapa=max(1, int(_p('Pasosetapa', c['pasos_etapa']))),
                 catalogo=_catalogo(),
                 # fase 11 v5: la naturaleza legible
                 umbral_monte=max(1, int(_p('Umbralmonte', c['umbral_monte']))),
                 limite_bosque=max(0.0, min(1.0, _p('Limitebosque', c['limite_bosque']))),
                 limite_nieve=max(0.0, min(1.0, _p('Limitenieve', c['limite_nieve']))),
                 altura_monte=max(0.0, _p('Alturamonte', c['altura_monte'])),
                 lod_nat=max(0.0, _p('Lodnat', c['lod_nat'])),
                 tinte_borde_nat=max(0.0, _p('Tintebordenat', c['tinte_borde_nat'])),
                 superficie=int(str(_p('Modocamara', 'globo')) in ('superficie', 'rasante')),   # v92: tambien a ras de suelo
                 # fase 11 v8: brotes, arboles y terrazas
                 ligero=int(bool(_p('Ligero', True))),
                 oceano=int(bool(_p('Oceano', True))),                          # motor v97
                 volcanes=max(0.0, min(1.0, _p('Volcanes', c['volcanes']))),
                 detalle=int(bool(_p('Detalle', True))),
                 pradera=max(0, min(2000000, int(_p('Pradera', c['pradera'])))),          # motor v99
                 mata=max(0.01, min(1.0, _p('Mata', c['mata']))),
                 tierra=max(0.0, min(1.0, _p('Tierra', c['tierra']))),                    # motor v100
                 # motor v101: la piel por turnos (Refrescopiel sustituye a Refresconat)
                 refresco_piel=max(0.0, min(2.0, _p('Refrescopiel', _p('Refresconat', c['refresco_piel'])))),
                 turnos=int(bool(_p('Turnos', True))), cache_arq=int(bool(_p('Cachearq', True))),
                 biomas=int(bool(_p('Biomas', True))),
                 variantes=max(1, min(8, int(_p('Variantes', c['variantes'])))),
                 traslucidez=max(0.0, min(1.0, _p('Traslucidez', c['traslucidez']))),
                 timidez=max(0.0, min(1.0, _p('Timidez', c['timidez']))),
                 emergentes=max(0.0, min(1.0, _p('Emergentes', c['emergentes']))),
                 orla=int(bool(_p('Orla', True))),
                 mezcla=max(0.0, min(1.0, _p('Mezcla', c['mezcla']))),
                 impostores=int(bool(_p('Impostores', True))),
                 terrazas_por_nota=max(0.0, _p('Terrazaspornota', float(c['terrazas_por_nota']))),
                 max_terrazas=max(1, min(16, int(_p('Maxterrazas', c['max_terrazas'])))),
                 paso_terraza=max(0.02, min(0.5, _p('Pasoterraza', c['paso_terraza']))),
                 riego=int(bool(_p('Riego', True))),
                 color_cultivo=(max(0.0, _p('Colorcultivor', c['color_cultivo'][0])),
                                max(0.0, _p('Colorcultivog', c['color_cultivo'][1])),
                                max(0.0, _p('Colorcultivob', c['color_cultivo'][2]))),
                 altura_meseta=max(0.0, min(1.0, _p('Alturameseta', c['altura_meseta']))),
                 max_niveles=max(1, min(6, int(_p('Maxniveles', c['max_niveles'])))),
                 marco=_menu('Marco', MARCOS, 1),
                 setos=int(bool(_p('Setos', True))),
                 # fase 11 v10: la ciudad legible
                 lenguaje=_menu('Lenguaje', LENGUAJE_MODOS, 0),
                 variantes_ciudad=max(1, min(6, int(_p('Variantesciudad', c['variantes_ciudad'])))),
                 fijar_tipo=_menu('Fijartipo', FIJAR_TIPOS, 0),
                 oblicuidad=max(0.0, min(30.0, _p('Oblicuidad', c['oblicuidad']))),
                 alto_planta=max(0.01, min(0.5, _p('Alturaplanta', c['alto_planta']))),
                 ancho_vano=max(0.005, min(0.5, _p('Anchovano', c['ancho_vano']))),
                 retranqueo=max(0.0, min(0.4, _p('Retranqueo', c['retranqueo']))),
                 torsion_max=max(0.0, min(360.0, _p('Torsionmax', c['torsion_max']))),
                 parasitos_por_nota=max(0.0, _p('Parasitospornota', float(c['parasitos_por_nota']))),
                 max_parasitos=max(1, min(64, int(_p('Maxparasitos', c['max_parasitos'])))),
                 modulo_marco=max(0.1, min(0.5, _p('Modulomarco', c['modulo_marco']))),
                 max_marco=max(1, min(6, int(_p('Maxmarco', c['max_marco'])))),
                 capsulas=max(0.0, min(1.0, _p('Capsulas', c['capsulas']))),
                 mutacion=max(0.0, min(1.0, _p('Mutacion', c['mutacion']))),
                 mutacion_fuente=_menu('Mutacionfuente', MUTACION_FUENTES, 0),
                 obra=int(bool(_p('Obra', True))),
                 desfase_fachada=max(0, int(_p('Desfasefachada', c['desfase_fachada']))),
                 gruas=int(bool(_p('Gruas', True))),
                 max_gruas=max(0, min(32, int(_p('Maxgruas', c['max_gruas'])))),
                 tinte_ventanas=int(bool(_p('Tinteventanas', True))),
                 pasos_tinte=max(0.25, _p('Pasostinte', float(c['pasos_tinte']))),
                 lod_ciudad=max(0.0, _p('Lodciudad', c['lod_ciudad'])),
                 # fase 11 v11: la industria
                 recursos=int(bool(_p('Recursos', True))),
                 epoca=_menu('Epoca', EPOCA_MODOS, 0),
                 variantes_ind=max(1, min(6, int(_p('Variantesind', c['variantes_ind'])))),
                 bancos_por_nota=max(0.0, _p('Bancospornota', float(c['bancos_por_nota']))),
                 max_bancos=max(1, min(12, int(_p('Maxbancos', c['max_bancos'])))),
                 max_bastidor=max(1, min(6, int(_p('Maxbastidor', c['max_bastidor'])))),
                 emisiones=max(0.0, min(2.0, _p('Emisiones', c['emisiones']))),
                 max_humo=max(0, int(_p('Maxhumo', c['max_humo']))),
                 lod_ind=max(0.0, _p('Lodind', c['lod_ind'])))
    if c['nivel'] >= 12:
        c.update(material_modo=_menu('Materialmodo', MATERIALES, 1),
                 rug_min=max(0.0, min(1.0, _p('Rugmin', c['rug_min']))),
                 rug_max=max(0.0, min(1.0, _p('Rugmax', c['rug_max']))),
                 vigor_max=max(0.6, _p('Vigormax', c['vigor_max'])),
                 plantas_ligado=max(1, int(_p('Plantasligado', c['plantas_ligado']))),
                 gate_prueba=max(0.01, _p('Gateprueba', c['gate_prueba'])),
                 respaldo=int(_p('Materialrespaldo', False)))
    if c['nivel'] >= 13:
        c.update(rios=int(_p('Rios', True)), carreteras=int(_p('Carreteras', True)),
                 min_via=max(1, int(_p('Minvia', c['min_via']))),
                 grosor_via=max(0.01, _p('Grosorvia', c['grosor_via'])),
                 max_rio=max(1, int(_p('Maxrio', c['max_rio']))),
                 # fase 13 v2: rios azules
                 color_rio=(max(0.0, _p('Colorrior', COL_RIO[0])), max(0.0, _p('Colorriog', COL_RIO[1])),
                            max(0.0, _p('Colorriob', COL_RIO[2]))),
                 ancho_rio=max(0.005, _p('Anchorio', c['ancho_rio'])),
                 emisivo_rio=max(0.0, _p('Emisivorio', c['emisivo_rio'])),
                 lagos=int(_p('Lagos', True)),
                 # fase 13 v7: el tejido de la industria (vias y red)
                 vias=int(_p('Vias', True)), red=int(_p('Red', True)),
                 min_red=max(1, int(_p('Minred', c['min_red']))),
                 ancho_via=max(0.01, _p('Anchovia', c['ancho_via'])),
                 pulso_red=int(_p('Pulsored', True)),
                 color_red=(max(0.0, _p('Colorredr', COL_RED_DEF[0])), max(0.0, _p('Colorredg', COL_RED_DEF[1])),
                            max(0.0, _p('Colorredb', COL_RED_DEF[2]))),
                 # fase 13 v3: rios que se ven desde el globo
                 ancho_min_px=max(0.0, _p('Anchominpx', c['ancho_min_px'])),
                 encuadre=max(0.3, min(1.0, _p('Encuadre', c['encuadre']))))
    if c['nivel'] >= 14:
        c.update(ventana_escalada=max(1, int(_p('Ventanaescalada', c['ventana_escalada']))),
                 golpes_escalada=max(1, int(_p('Golpesescalada', c['golpes_escalada']))),
                 pasos_fuego=max(1, int(_p('Pasosfuego', c['pasos_fuego']))),
                 max_fuego=max(1, int(_p('Maxfuego', c['max_fuego']))),
                 pasos_polvo=max(1, int(_p('Pasospolvo', c['pasos_polvo']))),
                 apagon=int(_p('Apagon', True)), grisu=int(_p('Grisu', True)))     # fase 14 v4
    if c['nivel'] >= 15:
        c.update(peso_traza=max(0.0, min(1.0, _p('Pesotraza', c['peso_traza']))),
                 rebrote=int(_p('Rebrote', True)), tema_en_ciclo=int(_p('Temaenciclo', True)))
        if c['tema_en_ciclo']:          # el tema del mundo manda; el del parametro espera
            Wt = (me.fetch('W', None) or {}).get('tema')
            if Wt is not None and int(Wt) != int(c['tema']):
                c['tema_pendiente'] = c['tema']
                c['tema'] = int(Wt)
    if c['nivel'] >= 16:
        c.update(detalle_expuesto=max(0, int(_p('Detalleexpuesto', c['detalle_expuesto']))),
                 unir_cortes=int(_p('Unircortes', True)))
    if c['nivel'] >= 17:
        c.update(sway_max=max(0.0, _p('Swaymax', c['sway_max'])),
                 trafico=max(0, int(_p('Trafico', c['trafico']))),
                 pasos_frente=max(1, int(_p('Pasosfrente', c['pasos_frente']))),
                 turno=int(_p('Turno', True)),          # fase 17 v3: el frente es un cambio de turno
                 master_beat=_master_beat())
    if c['nivel'] >= 19:
        c.update(fuente_modular=_menu('Fuentemodular', FUENTES_MODULAR, c['fuente_modular']),
                 rango_modular=_menu('Rangomodular', [r[0] for r in RANGOS_MODULAR], 0),
                 suavizado=max(0.0, _p('Suavizado', c['suavizado'])),
                 viento_max=max(0.0, _p('Vientomax', c['viento_max'])),
                 respiracion=max(0.0, min(1.0, _p('Respiracion', c['respiracion']))),
                 smog=max(0.0, _p('Smog', c['smog'])), niebla=max(0.0, min(1.0, _p('Niebla', c['niebla']))),
                 glitch=max(0.0, min(1.0, _p('Glitch', c['glitch']))))
    if c['nivel'] >= 21:
        c.update(umbral_onset=max(0.0, _p('Umbralonset', c['umbral_onset'])),
                 reduccion_mic=max(0.0, _p('Reduccionmic', c['reduccion_mic'])),
                 umbral_corte=max(1e-6, _p('Umbralcorte', c['umbral_corte'])),
                 prof_mic=max(1, int(_p('Profundidadmic', c['prof_mic']))),
                 fuente_mic=_menu('Fuentemic', FUENTES_MIC, c['fuente_mic']),
                 canal_mic=max(0, int(_p('Canalmic', c['canal_mic']))),
                 chop_mic=str(_p('Chopmic', '')).strip())
        red, rad, prof = c['perfiles'][PAD_MIC]           # la reduccion del pad 9, de Reduccionmic
        c['perfiles'][PAD_MIC] = (c['reduccion_mic'], rad, prof)
    if c['nivel'] >= 22:
        c.update(presencia_activa=int(_p('Activo', True)),
                 cuanto=min(CUANTO_MAX, max(0.0, _p('Cuanto', c['cuanto']))),
                 peso_crear=max(0.0, min(1.0, _p('Pesocrear', c['peso_crear']))),
                 peso_erosion=max(0.0, min(1.0, _p('Pesoerosion', c['peso_erosion']))),
                 fuente_sala=_menu('Fuente', FUENTES_SALA, c['fuente_sala']),
                 sensor_sala=_menu('Sensor', SENSORES_SALA, c['sensor_sala']),
                 altura_min=_p('Alturamin', c['altura_min']), altura_max=_p('Alturamax', c['altura_max']),
                 archivo_fondo=str(_p('Archivofondo', c['archivo_fondo'])).strip(),
                 ancho_sala=max(0.5, _p('Anchosala', c['ancho_sala'])),
                 fondo_sala=max(0.5, _p('Fondosala', c['fondo_sala'])),
                 tam_casilla=max(0.25, min(1.0, _p('Tamcasilla', c['tam_casilla']))),
                 desenfoque=max(0.0, _p('Desenfoque', c['desenfoque'])),
                 ocupacion_llena=max(0.1, min(1.0, _p('Ocupacionllena', c['ocupacion_llena']))),
                 subida=max(0.0, _p('Subida', c['subida'])), bajada=max(0.0, _p('Bajada', c['bajada'])),
                 lon_central=_p('Loncentral', c['lon_central']),
                 ancho_angular=max(0.0, min(360.0, _p('Anchoangular', c['ancho_angular']))),
                 lat_norte=_p('Latnorte', c['lat_norte']), lat_sur=_p('Latsur', c['lat_sur']),
                 espejo=int(_p('Espejo', False)), sim_casilla=max(0, int(_p('Simcasilla', 0))))
    if c['nivel'] >= 23:
        c.update(ventana_balance=max(1.0, _p('Ventanabalance', c['ventana_balance'])),
                 umbral_estrobo=max(0.1, _p('Umbralestrobo', c['umbral_estrobo'])),
                 salida_estrobo=max(0.0, _p('Salidaestrobo', c['salida_estrobo'])),
                 max_hz=max(0.0, min(float(DESTELLOS_MAX), _p('Maxhz', c['max_hz']))),
                 noche=max(0.0, _p('Noche', c['noche'])), colapso_on=int(_p('Colapsoon', False)),
                 max_erosion=max(1.0, _p('Maxerosion', c['max_erosion'])),
                 sim_balance=_p('Simbalance', c['sim_balance']),
                 interfaz_dmx=_menu('Interfazdmx', INTERFACES_DMX, c['interfaz_dmx']),
                 universo_dmx=max(0, int(_p('Universodmx', c['universo_dmx']))))
    if c['nivel'] >= 24:
        c.update(sep_cabezas=max(0.05, _p('Separacioncabezas', c['sep_cabezas'])),
                 confirma_persona=max(1, int(_p('Confirmapersona', c['confirma_persona']))),
                 sim_fila=max(1, int(_p('Simfila', c['sim_fila']))))
    if c['nivel'] >= 25:
        c.update(prob_llegada=max(0.0, min(1.0, _p('Probllegada', c['prob_llegada']))),
                 t_parada=max(0.1, _p('Tparada', c['t_parada'])))
    if c['nivel'] >= 27:
        c.update(min_huellas=max(1, int(_p('Minhuellas', c['min_huellas']))),
                 inclusiones_max=max(0.0, min(1.0, _p('Inclusionesmax', c['inclusiones_max']))))
    if c['nivel'] >= 29:
        c.update(min_fila=max(2, int(_p('Minfila', c['min_fila']))),
                 t_fila=max(0.1, _p('Tfila', c['t_fila'])),
                 modo_fila=_menu('Modofila', MODOS_FILA, c['modo_fila']),
                 conchas_persona=max(1, int(_p('Conchasporpersona', c['conchas_persona']))))
    if c['nivel'] >= 31:
        c.update(carpeta_historico=str(_p('Carpetahistorico', '')).strip())
    if c['nivel'] >= 18:
        c.update(diagnostico=int(_p('Diagnostico', False)),
                 luz_calida=max(0.0, min(1.0, _p('Luzcalida', c['luz_calida']))),
                 escena=_menu('Escena', ESCENAS, 0))
    # motor v64: el rio mas caudaloso, ANCHO_MAX_RIO_K veces el mas fino. Motor v71:
    # despues de leer Anchorio (antes se calculaba con el 0,10 de fabrica)
    c['ancho_max_rio'] = ANCHO_MAX_RIO_K * c['ancho_rio']
    return c


_CFG_FOTO = {}


def cfg_malla():
    """Motor v93: la configuracion para las mallas de la biblioteca (malla_ejemplar),
    leyendo SOLO los parametros que las cambian. En TouchDesigner un Script SOP queda
    colgado de cada parametro que lee al cocinarse: con cfg() entero (mas de 200) se
    rehacia al cambiar cualquiera, y Loncentral (fase 22) cambia en cada fotograma con
    el planeta girando. La vegetacion no depende de ningun parametro (Varangulo,
    Cuantizar30 y Densidadhoja son fijos desde la fase 11 v9); la ciudad y la
    industria, de Oblicuidad, Retranqueo y Torsionmax, con los limites de cfg()."""
    c = DEFAULT_CFG
    return dict(var_angulo=c['var_angulo'], cuantizar30=c['cuantizar30'], densidad_hoja=c['densidad_hoja'],
                oblicuidad=max(0.0, min(30.0, _p('Oblicuidad', c['oblicuidad']))),
                retranqueo=max(0.0, min(0.4, _p('Retranqueo', c['retranqueo']))),
                torsion_max=max(0.0, min(360.0, _p('Torsionmax', c['torsion_max']))))


def cfg_foto():
    """Motor v72: la configuracion, una vez por fotograma, para lo que se evalua
    en cada fotograma desde las expresiones (luces, uniformes, camara...). cfg()
    lee unos 180 parametros; se llamaba unas 32 veces por fotograma. NO se puede
    modificar el dict que devuelve (es compartido). Las autopruebas y los scripts
    de fase siguen usando cfg(), que lee siempre lo ultimo."""
    if _CFG_FOTO.get('off'):            # durante una autoprueba: siempre lo ultimo
        return cfg()
    f = absTime.frame
    if _CFG_FOTO.get('f') != f:
        _CFG_FOTO['c'] = cfg()
        _CFG_FOTO['f'] = f
    return _CFG_FOTO['c']


def cfg_foto_pausa(off):
    """Las autopruebas (Prueba, comun v51) la apagan mientras corren."""
    _CFG_FOTO.clear()
    _CFG_FOTO['off'] = bool(off)
    _CACHE.pop('flash_f', None)


def _master_beat():
    """El valor de master_beat (el primer canal del CHOP de Masterbeat), o
    None si no hay ninguno: entonces el pulso lo cuenta el motor."""
    try:
        o = parent().par.Masterbeat.eval()
        o = op(o) if isinstance(o, str) else o
        if o is None or not getattr(o, 'numChans', 0):
            return None
        return float(o[0].eval())
    except Exception:
        return None


def sync_grid():
    """Lee el rango de los parametros y rehace la reticula si ha cambiado."""
    lo = _p('Notapolosur', POLO_SUR_DEF)
    hi = _p('Notapolonorte', POLO_NORTE_DEF)
    mode = _menu('Fuerarango', FUERA_MODES, 0)
    return set_grid(lo, hi, mode)


def world():
    sync_grid()
    W = me.fetch('W', None)
    key = [GRID['lo'], GRID['hi']]
    if W is None or W.get('grid') != key or len(W.get('occ', [])) != N:
        if W is not None:
            print('ESTRATOS  rango %s-%s: reticula de %d celdas, el mundo empieza vacio'
                  % (key[0], key[1], N))
        W = new_world()
        W['grid'] = key
        me.store('W', W)
        _CACHE['inst'] = None
        _CACHE['tiles'] = None
    return ensure(W)


def reset_world():
    sync_grid()
    W = new_world()
    W['grid'] = [GRID['lo'], GRID['hi']]
    me.store('W', W)
    _CACHE['inst'] = None
    _CACHE['tiles'] = None
    _CACHE['frame'] = None


def _ritmo():
    return parent().op('ritmo').module


def tempo():
    try:
        return _ritmo().tempo()
    except Exception:
        return 120.0


def _compas(defecto=4):
    """Negras por compas: las de la linea de tiempo del proyecto (Signature),
    las mismas con las que gira el planeta (motor v60; antes Negrasporcompas)."""
    try:
        return max(1, int(_ritmo().beats_per_bar()))
    except Exception:
        return defecto


def playing():
    try:
        return _ritmo().playing()
    except Exception:
        return True


def surface_radius(frame=None):
    return top_radius(world(), cfg_foto())


def nucleo_radius(frame=None):
    """La esfera del nucleo ya no crece (motor v23): lo que no se dibuja de
    cada columna lo cubre su zocalo, y una esfera a cota comun taparia las
    hondonadas."""
    return cfg_foto()['core_radius']


def floor_radius(i, frame=None):
    """Suelo de la celda i (lo usa la reticula)."""
    return suelo(world(), cfg_foto(), i)


def giro_factor(frame=None):
    """Multiplica el giro del planeta (lo lee 'ritmo'). 1 con Giromin 1."""
    try:
        return float(world().get('giro_factor', 1.0))
    except Exception:
        return 1.0


def performance():
    return bool(_p('Modoactuacion', False))


# --- MIDI --------------------------------------------------------------------

def _log(row):
    t = parent().op('midi_log')
    if t is None:
        return
    t.appendRow([str(v) for v in row])
    while t.numRows > 41:
        t.deleteRow(1)


def _say(key, text):
    n = _CACHE['printed'].get(key, 0)
    if n < 8:
        print(text)
        _CACHE['printed'][key] = n + 1


def _seq1_beacon(note):
    """La ultima nota del SEQ1 queda en Nota (pagina Fase2): la usa Sembrar
    y la leyenda. Ya no hay baliza: la luz del centro de la celda la da el
    motor (cell_lights)."""
    try:
        parent().par.Nota = int(note)
    except Exception:
        pass


def _seq2_beacon(note):
    """La ultima nota del SEQ2 queda en Nota2 (pagina Fase2, junto a Nota), igual
    que la del SEQ1 queda en Nota: es la que siembra Sembrar2."""
    try:
        parent().par.Nota2 = int(note)
    except Exception:
        pass


def _es_seq2(ch, lvl):
    """El canal es del SEQ2 (desde la fase 5): el de Canal2 o, con Filtrar2
    apagado, cualquiera que no sea el del SEQ1 (que se comprueba antes) ni el
    de la bateria."""
    if lvl < 5:
        return False
    if ch == _p('Canal2', 14):
        return True
    if _p('Filtrar2', True):
        return False
    return not (lvl >= 7 and ch == _p('Canaldrum', 16))


def midi_note_on(ch, note, vel):
    c = cfg()
    lvl = c['nivel']
    now = absTime.seconds
    ch1 = _p('Canal', 13)
    filt = _p('Filtrar', True)
    W = world()
    if (not filt) or ch == ch1:
        _seq1_beacon(note)
        r = note_on(W, c, GEO, note, vel, now, tempo())
        res = 'SEQ1 %s' % r['estado']
    elif _es_seq2(ch, lvl):
        _seq2_beacon(note)
        r = note_on(W, c, ARQ, note, vel, now, tempo())
        res = 'SEQ2 %s' % r['estado']
    elif lvl >= 7 and ch == _p('Canaldrum', 16):
        pad = int(note) - _p('Notabase', 36)
        if 0 <= pad < 8:
            ev = erosion(W, c, pad, vel, now)
            if ev['modo'] == 'impulso':
                res = 'IMPULSO pad %d +%d celda %d ocupacion %d->%d' % (pad + 1, ev['pulsos'], ev['celda'],
                                                                      ev['occ0'], ev['occ'])
            else:
                res = 'EROSION pad %d %s celda %d%s' % (pad + 1, ev['tipo'], ev['celda'],
                                                       ' (no prende)' if ev.get('prende') is False else '')
        else:
            res = 'ignorado: pad fuera de 1-8'
    else:
        res = 'ignorado: canal %s' % ch
    _log([absTime.frame, ch, note, vel, res])
    _say('n%s' % ch, 'MIDI  canal %s  nota %s  vel %s  ->  %s' % (ch, note, vel, res))
    return res


def midi_note_off(ch, note):
    c = cfg()
    W = world()
    s = None
    if (not _p('Filtrar', True)) or ch == _p('Canal', 13):
        s = GEO
    elif _es_seq2(ch, c['nivel']):
        s = ARQ
    if s:
        note_off(W, c, s, note, absTime.seconds, tempo())


def midi_cc(ch, num, val):
    c = cfg()
    if c['nivel'] >= 6:
        on_cc(world(), c, ch, num, val, absTime.seconds)


def midi_start():
    clock_start(world(), absTime.seconds)


def midi_stop():
    clock_stop(world(), absTime.seconds)


def midi_sysex(b):
    # MMC: F0 7F 7F 06 01 F7 = stop, 02 = play
    if len(b) >= 6 and b[0] == 0xF0 and b[1] == 0x7F and b[3] == 0x06:
        if b[4] == 0x01:
            midi_stop()
        elif b[4] == 0x02:
            midi_start()


# --- fin de ciclo ------------------------------------------------------------

CICLOS_COLS = ['ciclo', 'compases', 'segundos', 'motivo', 'madurez', 'novedad', 'grosor',
               'territorio', 'balance', 'huellas', 'banda']
CICLOS_MAX = 200


def registrar_ciclo(W, c, ev):
    """AVISO en el Textport y una fila en la tabla 'ciclos'."""
    print('AVISO  %s%s' % (W['aviso'], '  -> concha %d' % n_shells(W) if 'grosor' in ev else ''))
    t = parent().op('ciclos')
    if t is None:
        return
    try:
        if t.numRows == 0:
            t.appendRow(CICLOS_COLS)
        vals = dict(ciclo=ev['ciclo'], compases=ev['compases'], segundos='%.1f' % ev['segundos'],
                    motivo=ev['motivo'], madurez='%.2f' % ev['madurez'],
                    novedad='%.2f' % ev['novedad'],
                    grosor='%.3f' % ev['grosor'] if 'grosor' in ev else '',
                    territorio='%.2f' % ev.get('territorio', 0.0),
                    balance='%.2f' % ev['balance'] if 'balance' in ev else '',
                    huellas=ev.get('huellas', ''),
                    banda=('%s%s' % (ev['banda'], ' + colapso' if ev.get('colapso') else '')) if 'banda' in ev else '')
        cab = [t[0, k].val for k in range(t.numCols)]     # por nombre de columna
        t.appendRow([vals.get(k, '') for k in cab])
        while t.numRows > CICLOS_MAX + 1:
            t.deleteRow(1)
    except Exception as e:
        print('AVISO  tabla ciclos: %s' % e)


# --- fotograma ---------------------------------------------------------------

DIAG = {}                    # motor v102: lo que tarda cada parte del fotograma (diagnostico_fps.py)
DIAG_PARTES = ('mundo', 'instancias', 'chops', 'terreno', 'resto')


def diag_reset():
    """Pone a cero las cuentas del fotograma (la primera pasada de diagnostico_fps.py)."""
    DIAG.clear()
    DIAG.update(n=0, lentos=0, recocidos=0, total=[0.0, 0.0])
    for k in DIAG_PARTES:
        DIAG[k] = [0.0, 0.0]


def _diag_suma(t, partes, chops):
    if 'n' not in DIAG:
        diag_reset()
    DIAG['n'] += 1
    DIAG['recocidos'] += chops
    tot = sum(partes.values())
    DIAG['lentos'] += tot > 1000.0 / 60.0
    for k, v in list(partes.items()) + [('total', tot)]:
        a = DIAG[k]
        a[0] += v
        a[1] = max(a[1], v)


def diag_texto():
    """Las lineas del motor para diagnostico_fps.py: ms de Python por fotograma
    (media y maximo) en cada parte del latido, los Script CHOP recocidos y la PIEL."""
    n = DIAG.get('n', 0)
    if not n:
        return ['  (el motor no ha contado fotogramas: lanza el diagnostico dos veces)']
    nombres = dict(mundo='mundo (tick, sala, micro, modular)', instancias='instancias (build_instances)',
                   chops='Script CHOP recocidos (cook)', terreno='terreno y texturas al dia',
                   resto='resto (frame_u, render, reticula)', total='TOTAL del latido')
    out = ['  %d fotogramas del motor: %.1f ms de media, %.1f de maximo; %d por encima de 16,7 ms; '
           '%.1f Script CHOP recocidos por fotograma'
           % (n, DIAG['total'][0] / n, DIAG['total'][1], DIAG['lentos'], DIAG['recocidos'] / float(n))]
    for k in DIAG_PARTES + ('total',):
        out.append('    %-38s media %7.2f ms   maximo %8.2f ms' % (nombres[k], DIAG[k][0] / n, DIAG[k][1]))
    try:
        c = cfg()
        out.append('  ' + _legend_piel(c).strip())
        nat = sum(1 for g, _, _ in geometrias_piel(c) if g.startswith('mod_veg_'))
        out.append('  geometrias de la piel %d (vegetacion %d)   Variantes %d   Pradera %d   Refrescopiel %s s'
                   % (len(geometrias_piel(c)), nat, variantes(c), int(c.get('pradera', 0)),
                      _coma(c.get('refresco_piel', 0.0), 2)))
    except Exception as e:
        out.append('  (sin la linea PIEL: %s)' % e)
    return out


def _op_chop(name):
    """El Script CHOP de instancias name, guardado (motor v102: con Variantes alto hay
    cientos y buscarlos en cada fotograma costaba)."""
    ops = _CACHE.setdefault('ops_chop', {})
    o = ops.get(name)
    if o is not None:
        try:
            if o.valid:
                return o
        except Exception:
            pass
    o = ops[name] = parent().op(name)
    return o


def frame_tick():
    t0 = _time.perf_counter()
    partes = {}
    W, c = world(), cfg()
    now = absTime.seconds
    if c['nivel'] >= 15 and (W.get('tema') is None or not c['tema_en_ciclo']):
        W['tema'] = int(c['tema'])      # fase 15: el tema del mundo
    if c['nivel'] >= 19:                # fase 19: las senales del modular, antes del mundo
        md = W['modular']
        dt = max(0.0, min(0.25, now - md.get('t_fotograma', now)))
        md['t_fotograma'] = now
        modular_tick(W, c, leer_modular(c, now), dt, now)
    if c['nivel'] >= 22:                # fase 22: la camara, antes del microfono (su objetivo)
        sala_tick(W, c, now)
    if c['nivel'] >= 21:                # fase 21: el microfono, antes del mundo
        mic_tick(W, c, now)
    res = tick(W, c, now, tempo(), playing())
    if c['nivel'] >= 23:                # fase 23: los valores DMX de este fotograma
        o = parent().op('dmx_valores')
        if o is not None:
            try:
                o.cook(force=True)
            except Exception as e:
                _say('dmx_valores', 'AVISO  dmx_valores: %s' % e)
    _CACHE['nivel'] = c['nivel']        # fase 17: para la luz y las ventanas del shader
    _CACHE['modular'] = dict(W['modular']) if c['nivel'] >= 19 else None
    _CACHE['ventanas'] = ventanas_luz_de(W, c)
    _CACHE['tinte'] = tinte_actual(W, c) if c['nivel'] >= 17 else [1.0, 1.0, 1.0]
    _CACHE['luz_calida'] = c.get('luz_calida', 0.0) if c['nivel'] >= 18 else 0.0
    _CACHE['uni'] = uniformes_piel(W, c, now)       # fase 11 v5: pisos, borde y agua del shader
    _CACHE['dia'] = 1.0 - noche_nivel(W, c, now) if c['nivel'] >= 28 else 1.0     # fase 28: las luces
    if res.get('burst'):
        print('AVISO  %s' % W['aviso'])
    if res.get('frente'):
        print('FRENTE  cambio de pattern: el frente recorre el planeta en %d pasos' % int(c['pasos_frente']))
    if res.get('ciclo'):
        registrar_ciclo(W, c, res['ciclo'])
    pk = palette_key(c)                 # cambiar la paleta recolorea todo lo enterrado
    dirty = W.get('dirty', True) or _CACHE.get('tiles') is None or _CACHE.get('pal') != pk
    _CACHE['pal'] = pk
    t1 = _time.perf_counter()
    partes['mundo'] = (t1 - t0) * 1000.0
    inst = build_instances(W, c, now, hide_beacons=performance(), tiles=dirty, refresco=True)
    t2 = _time.perf_counter()
    partes['instancias'] = (t2 - t1) * 1000.0
    if dirty:
        _CACHE['tiles'] = inst['estratos']
    else:
        inst['estratos'] = _CACHE['tiles']
    _CACHE['inst'] = inst
    _CACHE['frame'] = absTime.frame
    hechas = _CACHE.setdefault('filas_chop', {})
    recocidos = 0
    for name in chop_names(c):
        if name == 'i_estratos' and not dirty:
            continue
        if name not in CHOP_NAMES:      # fase 11: solo los modelos que han cambiado
            filas = inst.get(name[2:], [])
            if hechas.get(name) == filas:
                continue
            o = _op_chop(name)
            if o is None:
                continue
            hechas[name] = filas
        else:
            o = _op_chop(name)
            if o is None:
                continue
        o.cook(force=True)
        recocidos += 1
    t3 = _time.perf_counter()
    partes['chops'] = (t3 - t2) * 1000.0
    if dirty or _CACHE.get('ret_R') != top_radius(W, c):
        _CACHE['ret_R'] = top_radius(W, c)
        o = parent().op('reticula_chop')
        if o is not None:
            o.cook(force=True)
    if c['nivel'] >= 31:                # fase 31: testigos, registro y columna de la jornada
        try:
            historico_tick(W, c, now)
        except Exception as e:
            _say('historico_tick', 'AVISO  historico: %s' % e)
    if c['nivel'] >= 29:                # fase 29: la tabla de las escisiones
        escisiones_tabla(W)
    t4 = _time.perf_counter()
    terreno_al_dia_td(W, c)
    t5 = _time.perf_counter()
    partes['terreno'] = (t5 - t4) * 1000.0
    render_tema_al_dia(c)               # motor v69: el render, solo con el tema actual
    render_modo_al_dia(c)               # motor v95: ojo de pez con la camara rasante
    fu = parent().op('frame_u')         # motor v69: giro y uniformes, una vez por fotograma
    if fu is not None:
        try:
            fu.cook(force=True)
        except Exception:
            pass
    W['dirty'] = False
    partes['resto'] = (_time.perf_counter() - t5 + t4 - t3) * 1000.0
    _diag_suma(t0, partes, recocidos)


def terreno_al_dia_td(W, c):
    """Fase 11 v5: el Script TOP 'alturas' se recuece solo cuando cambia el
    mapa de alturas, y la tabla de la rampa de los pisos, cuando cambian
    Limitebosque o Limitenieve."""
    if c['nivel'] < 11:
        return
    t = terreno(W, c)
    o = parent().op('alturas')
    if o is not None and _CACHE.get('alturas_v') != t['version']:
        _CACHE['alturas_v'] = t['version']
        try:
            o.cook(force=True)
        except Exception as e:
            print('AVISO  alturas: %s' % e)
    cu = parent().op('cultivos')            # fase 11 v8: bancales, riego y mesetas
    v = _CULTIVOS.get('v')
    if cu is not None and v is not None and _CACHE.get('cultivos_v') is not v[1]:
        _CACHE['cultivos_v'] = v[1]
        try:
            cu.cook(force=True)
        except Exception as e:
            print('AVISO  cultivos: %s' % e)
    filas = rampa_filas(c)
    tab = parent().op('rampa_hipso_claves')
    if tab is not None and _CACHE.get('rampa') != filas:
        _CACHE['rampa'] = filas
        try:
            tab.clear()
            for f in filas:
                tab.appendRow(f)
        except Exception as e:
            print('AVISO  rampa_hipso_claves: %s' % e)


def uniformes_piel(W, c, now):
    """Los uniformes de la piel que cambian con el mundo (fase 11 v5): altura
    maxima de los pisos, limites, sombreado, intensidad del borde, los tres
    focos de tinte (SEQ1, SEQ2 y el pad mas fuerte) y el emisivo del agua."""
    u = {}
    nat = c['nivel'] >= 11 and tema_de(c) == 'naturaleza'
    lb, ln = _limites_pisos(c) if c['nivel'] >= 11 else (0.65, 0.9)
    mar = nat and bool(c.get('oceano'))     # motor v97: el mar flota sobre las losetas (z < 0)
    u['uTerreno'] = (0.0, alto_hipso(c) if c['nivel'] >= 11 else 1.0, -OCEANO_LIFT if mar else HUNDIDO, 0.0)
    u['uOceano'] = (1.0 if mar else 0.0, now % 3600.0, nivel_mar(W, c) if mar else 0.0, 1.0 if nat else 0.0)
    u['uTierra'] = (c.get('tierra', 0.0) if nat else 0.0, 0.0, 0.0, 0.0)     # motor v100: las conchas, de tierra
    # motor v99: la pradera (GPU): cuantas matas reparte el shader por el planeta y su tamano
    u['uPradera'] = (float(c.get('pradera', 0)) if nat and c.get('detalle', 1) else 0.0, c.get('mata', 0.16), 0.0, 0.0)
    erup = []
    if nat and c.get('volcanes', 0.0) > 0:
        try:
            paso_ = step_dur(c, tempo())
        except Exception:
            paso_ = 0.125
        for cel, _ in rasgos_terreno(W, c)[1].get('volcanes', []):
            erup.append((erupcion(c, cel, now, paso_), cel))
        erup.sort(key=lambda x: (-x[0], x[1]))
    for k in range(3):                      # los tres volcanes mas activos: direccion y erupcion
        if k < len(erup):
            n = normal_i(erup[k][1])
            u['uVolcan%d' % k] = (n[0], n[1], n[2], erup[k][0])
        else:
            u['uVolcan%d' % k] = (0.0, 1.0, 0.0, 0.0)
    u['uPisos'] = (lb, ln, 0.65 if nat else 0.0, 0.0)
    u['uBorde'] = (c.get('tinte_borde_nat', 0.0) if nat else 0.0, 0.0, 0.0, 0.0)
    u['uAgua'] = (c.get('emisivo_rio', 0.25), 0.0, 0.0, 0.0)
    if c['nivel'] >= 11:                    # fase 11 v8: hojas, bancales y mesetas
        cc = c.get('color_cultivo', DEFAULT_CFG['color_cultivo'])
        u['uHojas'] = (c.get('traslucidez', 0.35) if nat else 0.0, 0.0, 0.0, 0.0)
        u['uCultivo'] = (cc[0], cc[1], cc[2], c.get('paso_terraza', 0.12) * limit(c))
        u['uBancal'] = (c.get('muro_terraza', 0.25), float(c.get('setos', 1)), float(PARCELA_TEX),
                        c.get('altura_meseta', 0.15) * limit(c))
        u['uRiego'] = tuple(_mix(color_rio(c), (0.45, 0.50, 0.52), 0.35)) + (0.0,)
    # fase 11 v10: la fachada de la ciudad en el shader: alto de planta y ancho de vano
    # (en el mundo) y los colores de los secuenciadores (el tinte de las ventanas)
    lim_ = limit(c)
    u['uCiudad'] = (c.get('alto_planta', 0.08) * lim_, c.get('ancho_vano', 0.05) * lim_,
                    1.0 if c['nivel'] >= 11 and tema_de(c) in CONSTRUIDOS else 0.0, 0.0)
    u['uSeq1'] = tuple(seq_color(c, 1)) + (0.0,)
    u['uSeq2'] = tuple(seq_color(c, 2)) + (0.0,)
    u['uNoche'] = (noche_nivel(W, c, now) if c['nivel'] >= 28 else 0.0, 0.0, 0.0, 0.0)     # fase 28
    focos = focos_tinte(W, c, now) if nat else []
    for k in range(3):
        if k < len(focos):
            I, cel, col = focos[k]
            n = normal_i(cel)
            ra = 0.5 * max(SIZE_EW[cel], SIZE_NS[cel])
            u['uTinte%d' % k] = (n[0], n[1], n[2], math.cos(1.15 * ra))
            u['uTinteCol%d' % k] = (col[0] * I, col[1] * I, col[2] * I, math.cos(0.45 * ra))
        else:
            u['uTinte%d' % k] = (0.0, 1.0, 0.0, 2.0)
            u['uTinteCol%d' % k] = (0.0, 0.0, 0.0, 3.0)
    return u


def focos_tinte(W, c, now):
    """[(intensidad, celda, color)]: lo que tine el borde de la naturaleza: la
    nota de cada secuenciador y el golpe de pad mas fuerte, los tres mas
    intensos (el albedo no se tine: fase 11 v5)."""
    out = []
    if c.get('luz_seq', 1):
        for cel, lista in seq_lights(W, c, now).items():
            for s_, env in lista:
                if env > 0.02:
                    out.append((env, cel, seq_color(c, s_)))
    for cel in list(W.get('luz', {})):
        I, pd_ = drum_light(W, c, cel, now)
        if pd_ is not None:
            out.append((I, cel, drum_color(c, pd_)))
    out.sort(key=lambda x: (-x[0], x[1]))
    return out[:3]


def piel_uniforme(nombre, k, frame=None):
    """Componente k de un uniforme de la piel (los GLSL MAT lo leen cada
    fotograma; ver uniformes_piel)."""
    try:
        u = _CACHE.get('uni')
        if u is None:
            W, c = world(), cfg_foto()
            u = _CACHE['uni'] = uniformes_piel(W, c, absTime.seconds)
        return float(u.get(nombre, (0.0, 0.0, 0.0, 0.0))[int(k)])
    except Exception:
        return 0.0


def instance_rows(chop_name):
    if _CACHE['inst'] is None:
        W, c = world(), cfg()
        _CACHE['inst'] = build_instances(W, c, absTime.seconds, hide_beacons=performance())
    key = chop_name[2:] if chop_name.startswith('i_') else chop_name
    return _CACHE['inst'].get(key, [])


# --- pulsos de los parametros ------------------------------------------------

def subir_escalon(W, c, s, x, vel, now, tempo=120.0):
    """Motor v70: notas en la celda x hasta que su ocupacion sube 1, las que
    cueste (Costemax): una celda vacia, 1 nota (la semilla). Lo usan Sembrarzona
    (antes, una nota por pulsacion: con Costemax alto, dos pulsaciones no
    formaban el cluster) y las autopruebas. Devuelve las notas tocadas."""
    o0 = W['occ'][x]
    for k in range(max(1, int(c['cost_max'])) + 1):
        note_on(W, c, s, cell_note(x), vel, now, tempo)
        if W['occ'][x] != o0:
            return k + 1
    return k + 1


def _gate_prueba(W, c, s, note, now):
    """Fase 12: los botones de prueba sueltan la nota tras Gateprueba pasos."""
    if c['nivel'] >= 12:
        W.setdefault('gate_sim', []).append([now + c['gate_prueba'] * step_dur(c, tempo()), s, int(note)])


def prueba_rio(W, c, nota, now):
    """Pruebario (fase 13 v3): levanta una cordillera de 5 celdas en el anillo
    de Nota2 (la del centro mas alta), con notas del SEQ2 como Sembrar2, y
    dice el rio que baja de su cumbre. Si no se ve un rio azul desde el globo,
    el fallo esta en la representacion, no en el motor."""
    if c['nivel'] < 13:
        return 'PRUEBARIO  el proyecto esta en el nivel %d: los rios llegan con la fase 13' % c['nivel']
    if tema_de(c) != 'naturaleza':
        return 'PRUEBARIO  Tema ciudad: los rios son de la naturaleza (pon Tema en naturaleza)'
    i = note_cell(nota)
    anillo = RINGS[RING_OF[i]] if 0 <= RING_OF[i] < len(RINGS) else [i]
    q = anillo.index(i) if i in anillo else 0
    fila = [anillo[(q + k) % len(anillo)] for k in (-2, -1, 0, 1, 2)] if len(anillo) >= 5 else [i]
    objetivo = dict((x, int(c['th_crown']) + (3 if x == i else 1)) for x in fila)
    for _ in range(600):                # como Sembrar2, nota a nota, con sus reglas
        faltan = [x for x in fila if W['occ'][x] < objetivo[x]]
        if not faltan:
            break
        for x in faltan:
            note_on(W, c, ARQ, cell_note(x), 110, now, tempo())
            note_off(W, c, ARQ, cell_note(x), now + 0.01, tempo())
    for x in range(N):
        W['vh'][x] = W['h'][x]
    W['dirty'] = True
    tj = tejido(W, c)
    ter = terreno(W, c)
    cumbre = max(fila, key=lambda x: ter['centro'][x])
    rio = next((r for r in tj['rios'] if r[0] in fila), [])
    _, res = build_rios(W, c)
    if not rio:
        return ('PRUEBARIO  cordillera %s, cumbre %d (relieve %.2f): NINGUN RIO: el motor no lo genera; '
                'baja Pendientemin o mira la linea RIOS' % (fila, cumbre, ter['centro'][cumbre]))
    return ('PRUEBARIO  cordillera %s, cumbre %d: rio %s (%d tramos), ancho %.1f px con la camara de globo. '
            'Si no lo ves azul, el fallo esta en la representacion' % (fila, cumbre, rio, len(rio) - 1, res['px']))


def _texto_destructor(ev):
    """Lo que hizo un aranazo de la fase 14, para el Textport."""
    out = ''
    if ev.get('accidente'):
        out += '   %s celda %d' % (ev['accidente']['tipo'], ev['accidente']['celda'])
    if ev.get('derribo'):
        out += '   derribo %d celdas' % ev['derribo']
    if ev.get('escalada'):
        out += '   ESCALADA: %s' % ev['escalada']
    return out


def on_pulse(name):
    W, c = world(), cfg()
    now = absTime.seconds
    if name == 'Sembrar':
        note = _p('Nota', 60)
        _seq1_beacon(note)
        r = note_on(W, c, GEO, note, _p('Velprueba', 100), now, tempo())
        _gate_prueba(W, c, GEO, note, now)
        ci = r['celda']
        print('SEMBRAR  %s -> celda %d  ocupacion %d  carga %d/%d  (%s)'
              % (note_name(note), ci, W['occ'][ci] if ci >= 0 else 0, W['carga'][ci] if ci >= 0 else 0,
                 cost(c, W['occ'][ci]) if ci >= 0 else 0, r['estado']))
    elif name == 'Sembrar2':
        note = _p('Nota2', 60)
        r = note_on(W, c, ARQ, note, _p('Velprueba', 100), now, tempo())
        _gate_prueba(W, c, ARQ, note, now)
        ci = r['celda']
        print('SEMBRAR2 %s -> celda %d  ocupacion %d  carga %d/%d  (%s)'
              % (note_name(note), ci, W['occ'][ci] if ci >= 0 else 0, W['carga'][ci] if ci >= 0 else 0,
                 cost(c, W['occ'][ci]) if ci >= 0 else 0, r['estado']))
    elif name == 'Erosionar':
        ev = erosion(W, c, _p('Padprueba', 1) - 1, _p('Velprueba', 100), now)
        if ev['modo'] == 'impulso':
            print('IMPULSO  pad %d +%d -> celda %d, ocupacion %d -> %d%s'
                  % (ev['pad'] + 1, ev['pulsos'], ev['celda'], ev['occ0'], ev['occ'],
                     ', %d desbordes' % len(ev['desbordes']) if ev['desbordes'] else ''))
        else:
            print('EROSION  pad %d (%s) -> celda %d, radio %d, notas deshechas %d%s'
                  % (ev['pad'] + 1, ev['tipo'], ev['celda'], ev['rad'], ev['quitado'], _texto_destructor(ev)))
    elif name == 'Escalar':             # fase 14: Golpesescalada aranazos seguidos
        pad = _p('Padprueba', 1) - 1
        if not es_aranazo(c, pad):      # el pad de prueba corta: el primer pad de aranazo
            pad = next((k for k in range(len(c['perfiles'])) if es_aranazo(c, k)), pad)
        for _ in range(max(1, int(c['golpes_escalada']))):
            ev = erosion(W, c, pad, _p('Velprueba', 100), now)
        print('ESCALADA  pad %d x%d -> celda %d%s'
              % (pad + 1, max(1, int(c['golpes_escalada'])), ev['celda'], _texto_destructor(ev)))
    elif name == 'Unirprueba':          # fase 16: dos cortes vecinos seguidos
        cortes = pads_corte(c)
        pad = _p('Padprueba', 1) - 1
        if pad not in cortes:
            pad = cortes[0] if cortes else pad
        red, rad, depth = c['perfiles'][pad]
        a = note_cell(_p('Nota', 60))
        if a is None or depth <= 0:
            print('UNIRPRUEBA  sin pad que corte o Nota fuera de rango')
        else:
            lejos = [x for x, d in rings(a, int(rad) + 1) if d == int(rad) + 1]
            b = lejos[0] if lejos else a
            for x in (a, b):
                W['ev']['erosion'] = dict(pad=pad, red=red, notas=0, rad=rad, prof=depth, celda=x,
                                          dens=0.0, doble=False, quitado=0, t=now, tipo='corte')
                fuera, u = corte_tematico(W, c, x, depth, rad, now)
            W['flash'] = dict(t=now, cell=b, k=1.0, pad=pad)
            print('UNIRPRUEBA  pad %d: cortes en %d y %d -> %s'
                  % (pad + 1, a, b, '%s por %s' % (UNION_NOMBRE[u['tipo']], '-'.join(str(x) for x in u['celdas']))
                     if u else 'sin union (Unircortes apagado o fuera de Ventanaescalada)'))
    elif name == 'Cargarescena':        # fase 18: volver a la escena guardada
        n = cargar_escena(ESCENAS[c.get('escena', 0)])
        print('ESCENA  %s cargada (%d parametros)' % (ESCENAS[c.get('escena', 0)], n))
    elif name == 'Guardarescena':       # fase 18: lo que hay, en la escena actual
        n = guardar_escena()
        print('ESCENA  %s guardada (%d parametros)' % (ESCENAS[c.get('escena', 0)], n))
    elif name == 'Frenteprueba':        # fase 17: un cambio de pattern de prueba
        f = cambio_pattern(W, c)
        W['aviso'] = 'Frenteprueba: cambio de pattern'
        print('FRENTE  de polo a polo en %d pasos (pattern saliente %s)'
              % (int(c['pasos_frente']), W['ev']['frente'].get('sale') or '-'))
    elif name == 'Pruebario':           # fase 13 v3: una cordillera de 5 celdas y su rio
        print(prueba_rio(W, c, _p('Nota2', 64), now))
    elif name in ('Sembrarzona', 'Sembrarzona2'):
        s = GEO if name == 'Sembrarzona' else ARQ
        note = _p('Nota' if s == GEO else 'Nota2', 60)
        ci = note_cell(note)
        if ci is None:
            print('SEMBRARZONA  %s fuera de rango' % note_name(note))
        else:
            for x in [ci] + list(NEIGH[ci]):
                subir_escalon(W, c, s, x, _p('Velprueba', 100), now, tempo())
                _gate_prueba(W, c, s, cell_note(x), now)
            if s == GEO:
                _seq1_beacon(note)
            cl = clusters(W, c)
            k = cl['de'][ci]
            print('SEMBRARZONA  %s %s -> celda %d y %d vecinas   %s'
                  % ('SEQ1' if s == GEO else 'SEQ2', note_name(note), ci, len(NEIGH[ci]),
                     'cluster de %d celdas, capital %d' % (len(cl['celdas'][k]), cl['capital'][k])
                     if k >= 0 else 'sin cluster todavia (pulsa otra vez)'))
    elif name in ('Simponer', 'Simquitar', 'Simvaciar'):      # fase 22: la sala simulada
        print(sala_sim_pulso(W, c, name))
    elif name == 'Simformarfila':       # fase 24: una fila de prueba en la sala simulada
        print(sala_fila_pulso(W, c, name))
    elif name == 'Simsumar':            # fase 29: una persona mas, contigua a la fila de prueba
        print(sala_sumar_pulso(W, c))
    elif name == 'Exportartestigo':     # fase 31: la seccion de la ultima escision y la columna de hoy
        print(exportar_pulso(W, c))
    elif name == 'Capturarfondo':       # fase 22: el suelo vacio de referencia
        print(capturar_fondo(c))
    elif name == 'Reiniciarcuentas':    # fase 22: los contadores del sorteo
        reiniciar_cuentas()
        print('CAMARA  contadores de senales recibidas y prendidas, a cero')
    elif name == 'Forzarciclo':
        registrar_ciclo(W, c, close_cycle(W, c, now, 'forzado'))
    elif name == 'Resetmundo':
        reset_world()
        print('MUNDO  vaciado')
    W['dirty'] = True


# --- el microfono (fase 21) ---------------------------------------------------

MIC_RATE = 44100                # la senal sintetica de las autopruebas


def mic_tick(W, c, now):
    """Cada fotograma: mic_flujo lee el bloque del microfono (o del CHOP de
    Chopmic) y avisa al motor; luego el ruido de sala olvida lo que sale de
    su ventana."""
    _CACHE['mic'] = (absTime.frame, W, c, now)
    o = parent().op('mic_flujo')        # con chop, mic_flujo recuece el CHOP de Chopmic
    if o is not None:
        try:
            o.cook(force=True)
        except Exception as e:
            _say('mic_flujo', 'AVISO  mic_flujo: %s' % e)
    ruido_tick(W, c, now)


def _mic_ctx():
    m = _CACHE.get('mic')
    if m and m[0] == absTime.frame:
        return m[1], m[2], m[3]
    return world(), cfg(), absTime.seconds


def _canal(arr, k):
    if arr is None or getattr(arr, 'ndim', 0) < 1 or arr.size == 0:
        return None
    if arr.ndim == 1:
        return arr
    return arr[min(int(k), arr.shape[0] - 1)]


def _sin_timeslice(scriptOp):
    """Un Script CHOP con el Audio Device In aguas arriba hereda su modo Time
    Slice, y en el no puede fijar numSamples: mic_flujo saca un
    bloque (o una muestra) por cocinado, asi que salen de el (motor v57)."""
    try:
        scriptOp.isTimeSlice = False
    except Exception:
        pass


def mic_cook(scriptOp):
    """onCook del Script CHOP mic_flujo: el flujo del bloque del microfono
    (mic_in) o del CHOP de Chopmic, el onset y, si lo hay, la erosion. Saca
    dos canales: flujo y onset."""
    W, c, now = _mic_ctx()
    src = parent().op('mic_in')         # v66: sin mic_fuente ni mic_sim
    if c['fuente_mic'] == FUENTE_CHOP:  # motor v56: el audio de otro CHOP (Chopmic)
        src = op(c['chop_mic']) if c['chop_mic'] else None
        if src is not None:
            try:
                src.cook(force=True)
            except Exception:
                pass
    res = None
    try:
        x = _canal(src.numpyArray(), c['canal_mic']) if src is not None else None
        rate = float(getattr(src, 'rate', MIC_RATE) or MIC_RATE)
        res = mic_bloque(W, c, x, rate, now) if x is not None else None
    except Exception as e:
        _say('micb', 'AVISO  microfono: %s' % e)
    _sin_timeslice(scriptOp)
    scriptOp.clear()
    scriptOp.numSamples = 1
    scriptOp.appendChan('flujo')[0] = res['flujo'] if res else 0.0
    scriptOp.appendChan('onset')[0] = 1.0 if res and res['onset'] else 0.0
    if res and res['onset']:
        _log_onset(W, res['onset'])


def _log_onset(W, ev):
    txt = 'MICRO onset flujo %.2f celda %d' % (ev['flujo'], ev['celda'])
    if ev.get('prende') is False:
        txt += ' (no prende)'
    if ev.get('escalada'):
        txt += ' ESCALADA %s' % ev['escalada']
    cr = ev.get('corte_ruido')
    if cr:
        txt += ' + corte por ruido de %d conchas' % cr['conchas']
    _log([absTime.frame, 'mic', '-', '%.2f' % ev['flujo'], txt])
    _say('onset', txt)
    if cr:
        print('AVISO  %s' % W['aviso'])


def microfono_encontrado():
    """(si, texto) del Audio Device In CHOP mic_in: con canales y sin errores."""
    o = parent().op('mic_in')
    if o is None:
        return False, 'sin mic_in'
    try:
        err = o.errors()
    except Exception:
        err = ''
    nch = getattr(o, 'numChans', 0)
    if err or not nch:
        return False, (err.splitlines()[0] if err else 'sin canales')
    try:
        dev = str(o.par.device.eval())
    except Exception:
        dev = '?'
    return True, '%s, %d canal%s' % (dev or 'por defecto', nch, '' if nch == 1 else 'es')


def _legend_micro(W, c):
    """MICRO (fase 21): la fuente, los onsets, el ultimo y el ruido de sala."""
    mc, r = W['mic'], W['ruido']
    fuente = FUENTES_MIC[int(c['fuente_mic']) % len(FUENTES_MIC)]
    if fuente == 'chop':
        fuente = 'chop %s' % (c['chop_mic'] or '(sin Chopmic)')
    elif not microfono_encontrado()[0]:
        fuente += ' (sin microfono)'
    u = mc.get('ultimo')
    ult = ('flujo %.2f celda %d hace %.1f s' % (u['flujo'], u['celda'], max(0.0, absTime.seconds - u['t']))
           if u else '-')
    txt = ('  MICRO    %s   flujo %.2f/%.2f   onsets %d   ultimo %s   ruido %.1f/%g en %g s'
           % (fuente, mc.get('flujo', 0.0), c['umbral_onset'], mc['n'], ult, r.get('total', 0.0),
              c['umbral_corte'], c['ventana_ruido']))
    if r['cortes']:
        txt += '   cortes %d' % r['cortes']
    if mc['descartados']:
        txt += '   descartados %d' % mc['descartados']
    return txt


# --- la camara cenital (fase 22) -----------------------------------------------

def lon_central(frame=None):
    """Longitud (grados) del centro de la cara del planeta que mira a la camara
    del globo: Loncentral se enlaza aqui, para que la sala caiga siempre en la
    cara visible. La camara mira desde +z y el planeta gira ry: 90 + ry."""
    try:
        ry = float(_ritmo().rotation(frame))
    except Exception:
        ry = 0.0
    return (90.0 + ry + 180.0) % 360.0 - 180.0


def _top_array(o, diferida=True):
    """La imagen de un TOP como (filas x columnas) del canal rojo, con la fila 0
    arriba; None si no hay imagen. numpyArray() entrega primero la fila de abajo.
    diferida: la descarga no espera a la GPU, pero entrega la imagen que habia en
    la llamada ANTERIOR (va una imagen por detras)."""
    if o is None:
        return None
    try:
        a = o.numpyArray(delayed=True) if diferida else o.numpyArray()
    except TypeError:
        a = o.numpyArray()
    except Exception:
        a = None
    if a is None or getattr(a, 'size', 0) == 0:
        return None
    if a.ndim == 3:
        a = a[..., 0]
    return a[::-1]


def sala_personas():
    """Las personas de la tabla sala_personas (la sala simulada): [[x, y, altura], ...]."""
    t = parent().op('sala_personas')
    out = []
    if t is None:
        return out
    for r in range(1, t.numRows):
        try:
            out.append([float(t[r, 0].val), float(t[r, 1].val),
                        float(t[r, 2].val) if t.numCols > 2 and t[r, 2].val else ALTURA_SIM])
        except Exception:
            pass
    return out


def sala_sim_cook(scriptOp):
    """onCook del Script TOP sala_sim: la imagen de alturas de la sala simulada."""
    np = _np()
    a = sala_sim_imagen(cfg(), sala_personas())
    if a is None:
        return
    out = np.zeros(a.shape + (4,), dtype=np.float32)
    out[..., 0] = out[..., 1] = out[..., 2] = a[::-1]
    out[..., 3] = 1.0
    scriptOp.copyNumpyArray(out)


def sala_tick(W, c, now):
    """Cada fotograma (como mucho CAM_FPS veces por segundo): lee la imagen de
    alturas (alturas_sala: la camara o la sala simulada) y actualiza la densidad."""
    if now - _SALA.get('t_img', -99.0) < 1.0 / CAM_FPS - 1e-4 and now >= _SALA.get('t_img', -99.0):
        return None
    _SALA['t_img'] = now
    if c['fuente_sala'] == FUENTE_SIMULADA:
        o = parent().op('sala_sim')
        if o is not None:
            try:
                o.cook(force=True)
            except Exception as e:
                _say('sala_sim', 'AVISO  sala_sim: %s' % e)
    # La sala simulada se lee al momento (110 x 90 pixeles recien cocinados): lo que
    # dice la tabla sala_personas es lo que ve esta imagen. La camara, en diferido
    # (una imagen por detras, sin parar la GPU); tras sala_reset o un cambio de
    # Fuente la primera lectura diferida se tira: es de antes.
    # v92: sin aparato (su TOP con errores o avisos, o sin imagen) no se lee: alturas_sala
    # daria igual una imagen (negra, o la ultima) y la sala no esta vacia de verdad.
    sim = c['fuente_sala'] == FUENTE_SIMULADA
    alt = None
    viva = sim or camara_encontrada(c)[0]
    if viva:
        try:
            o = parent().op('alturas_sala')
            if not sim and (_SALA.get('purgar', True) or _SALA.get('fuente') != c['fuente_sala']):
                _top_array(o)
            alt = _top_array(o, diferida=not sim)
        except Exception as e:
            _say('alturas_sala', 'AVISO  camara: %s' % e)
    _SALA.update(alt=alt, purgar=not viva, fuente=c['fuente_sala'])
    d = sala_bloque(W, c, alt, now)
    if c['nivel'] >= 24:                # fase 24: las personas de esta imagen
        try:
            personas_tick(W, c, now, alt)
        except Exception as e:
            _say('personas', 'AVISO  personas: %s' % e)
    o = parent().op('densidad')
    if o is not None:
        try:
            o.cook(force=True)
        except Exception:
            pass
    return d


def px_sala(k=0, frame=None):
    """Ancho (k = 0) o alto (1) en pixeles de la imagen de alturas: PX_CASILLA
    por casilla. Es la resolucion del Resolution TOP alturas_sala."""
    try:
        return rejilla_sala(cfg_foto())[int(k)] * PX_CASILLA
    except Exception:
        return 110 if not k else 90


def densidad_cook(scriptOp):
    """onCook del Script TOP densidad: la densidad de cada casilla, para mirarla."""
    np = _np()
    d = _SALA.get('dens')
    if np is None:
        return
    if d is None:
        cols, filas = rejilla_sala(cfg_foto())
        d = np.zeros((filas, cols))
    out = np.zeros(d.shape + (4,), dtype=np.float32)
    out[..., 0] = out[..., 1] = out[..., 2] = d[::-1]
    out[..., 3] = 1.0
    scriptOp.copyNumpyArray(out)


def sensor_sala(c=None):
    """(nombre, TOP) del aparato del menu Sensor: ('femto', 'orbbec1') o ('kinect', 'kinect1')."""
    k = (cfg() if c is None else c).get('sensor_sala', 0)
    k = k if k in (0, 1) else 0
    return SENSORES_SALA[k], SENSOR_OPS[k]


def camara_encontrada(c=None):
    """(si, texto) del TOP del Sensor (orbbec1 o kinect1): sin errores ni avisos y
    con imagen de mas de un pixel. No descarga la imagen: se mira cada fotograma."""
    nombre, nop = sensor_sala(c)
    o = parent().op(nop)
    if o is None:
        return False, 'sin %s' % nop
    err = ''
    for f in ('errors', 'warnings'):
        try:
            err = err or str(getattr(o, f)() or '').strip()
        except Exception:
            pass
    try:
        w, h = int(o.width), int(o.height)
    except Exception:
        w = h = 0
    if err or w <= 1:
        return False, '%s: %s' % (nop, err.splitlines()[0] if err else 'sin imagen')
    return True, '%s %d x %d' % (nop, w, h)


def _sim_casilla(c):
    cols, filas = rejilla_sala(c)
    return max(0, min(cols * filas - 1, int(c['sim_casilla'])))


def sala_sim_pulso(W, c, name):
    """Simponer, Simquitar y Simvaciar: escriben en la tabla sala_personas, de la
    que sala_sim dibuja la imagen (el mismo camino que la camara)."""
    t = parent().op('sala_personas')
    if t is None:
        return 'SALA  no esta la tabla sala_personas: relanza fase22_camara.py'
    if t.numRows == 0:
        t.appendRow(SALA_COLS)
    k = _sim_casilla(c)
    if name == 'Simponer':
        x, y = casilla_xy(c, k)
        t.appendRow(['%.3f' % x, '%.3f' % y, '%.2f' % ALTURA_SIM])
        txt = 'una persona en la casilla %d (%.2f, %.2f m)' % (k, x, y)
    elif name == 'Simquitar':
        fuera = 0
        for r in range(t.numRows - 1, 0, -1):
            try:
                if casilla_de_xy(c, float(t[r, 0].val), float(t[r, 1].val)) == k:
                    t.deleteRow(r)
                    fuera += 1
            except Exception:
                pass
        txt = '%d fuera de la casilla %d' % (fuera, k)
    else:
        n = t.numRows - 1
        t.clear()
        t.appendRow(SALA_COLS)
        txt = 'sala vacia (%d fuera)' % max(0, n)
    _SALA['t_img'] = -99.0              # la proxima lectura, ya
    return 'SALA  %s   personas simuladas: %d%s' % (
        txt, t.numRows - 1, '' if c['fuente_sala'] == FUENTE_SIMULADA else '   (Fuente no es simulada: no se ven)')


def capturar_fondo(c):
    """Capturarfondo: guarda el suelo vacio (la salida de cornerpin1) en
    Archivofondo y recarga fondo."""
    src, fondo = parent().op('cornerpin1'), parent().op('fondo')
    ruta = c['archivo_fondo'] or 'fondo_suelo.exr'
    if src is None:
        return 'FONDO  no esta cornerpin1: relanza fase22_camara.py'
    try:
        src.save(ruta)
    except Exception as e:
        return 'FONDO  no pude guardar %s: %s' % (ruta, e)
    if fondo is not None:
        for nm in ('reloadpulse', 'reload'):
            p = getattr(fondo.par, nm, None)
            if p is not None:
                try:
                    p.pulse()
                    break
                except Exception:
                    pass
    return 'FONDO  suelo vacio guardado en %s' % ruta


def _legend_camara(W, c):
    """CAMARA (fase 22): la fuente, las casillas con gente, la mas densa y la
    celda que la mira, y las senales prendidas."""
    cols, filas = rejilla_sala(c)
    if c['fuente_sala'] == FUENTE_SIMULADA:
        fuente = 'simulada'
    else:
        nombre = sensor_sala(c)[0]
        fuente = '%s %g fps' % (nombre, CAM_FPS) if _SALA.get('hay') else '%s (sin camara)' % nombre
    k, d = casilla_mas_densa(c)
    mas = 'densidad max %.2f (casilla %d -> celda %d)' % (d, k, celda_de_casilla(W, c, k)) if k is not None \
        else 'densidad max 0.00'
    cu = _SALA['cuentas']
    rec = cu['crear'][0] + cu['erosionar'][0]
    pre = cu['crear'][1] + cu['erosionar'][1]
    txt = '  CAMARA   %s   casillas %d/%d   %s   prendidas %d/%d' % (
        fuente, casillas_con_gente(), cols * filas, mas, pre, rec)
    if not c['presencia_activa']:
        txt += '   (Activo apagado: todo prende)'
    return txt


# --- la luz de la sala (fase 23) -------------------------------------------------

def dmx_filas():
    """Las filas [canal, funcion, foco] de la tabla dmx_canales."""
    t = parent().op('dmx_canales')
    out = []
    if t is None:
        return out
    for r in range(1, t.numRows):
        try:
            out.append([int(float(t[r, 0].val)), t[r, 1].val, t[r, 2].val if t.numCols > 2 else ''])
        except Exception:
            pass
    return out


def dmx_cook(scriptOp):
    """onCook del Script CHOP dmx_valores: un canal por canal DMX (c1, c2...),
    hasta el mayor de dmx_canales, con su valor 0-255."""
    W, c = world(), cfg_foto()
    filas = dmx_filas()
    vals = valores_dmx(W, c, absTime.seconds, filas) if c['nivel'] >= 23 else [0] * len(filas)
    n = max([f[0] for f in filas] or [0])
    canales = [0.0] * n
    for f, v in zip(filas, vals):
        if 1 <= f[0] <= n:
            canales[f[0] - 1] = max(canales[f[0] - 1], float(v))
    _sin_timeslice(scriptOp)
    scriptOp.clear()
    scriptOp.numSamples = 1
    for k, v in enumerate(canales):
        scriptOp.appendChan('c%d' % (k + 1))[0] = v


def luz_sala(que, k=0, frame=None):
    """Para quien quiera la luz de la sala sin DMX (la sala virtual): 'bano' (k =
    0 r, 1 g, 2 b, 3 intensidad), 'destello' (0 o 1), 'balance', 'estado', 'noche'."""
    W, c = world(), cfg_foto()
    now = absTime.seconds
    if c['nivel'] < 23:
        return 0.0
    if que == 'bano':
        return float(bano_valor(W, c, now)[int(k)])
    if que == 'destello':
        return destello_valor(W, now)
    if que == 'balance':
        return float(sala_de(W)['balance'])
    if que == 'estado':
        return float(sala_de(W)['estado'])
    if que == 'noche':
        return 1.0 if en_noche(W, now) else 0.0
    return 0.0


def dmx_encontrado():
    """(si, texto) del DMX Out CHOP dmx_out: activo y sin errores."""
    o = parent().op('dmx_out')
    if o is None:
        return False, 'sin dmx_out'
    try:
        err = o.errors()
    except Exception:
        err = ''
    if err:
        return False, err.splitlines()[0]
    try:
        if not o.par.active.eval():
            return False, 'apagado'
    except Exception:
        pass
    return True, INTERFACES_DMX[int(cfg_foto().get('interfaz_dmx', 0)) % len(INTERFACES_DMX)]


def interfaz_dmx_al_dia(nombre=None):
    """Lleva Interfazdmx al menu Interface del DMX Out CHOP (sus nombres pueden
    variar entre versiones de TouchDesigner). Devuelve si lo ha conseguido."""
    o = parent().op('dmx_out')
    nombre = str(nombre or _p('Interfazdmx', 'artnet'))
    if o is None:
        return False
    p = getattr(o.par, 'interface', None)
    if p is None:
        return False
    quiere = dict(artnet=['artnet', 'art-net'], usbpro=['usbpro', 'enttecusbpro', 'enttec', 'usbpromk2'])
    try:
        nombres = [str(x).lower() for x in p.menuNames]
        for w in quiere.get(nombre, [nombre]):
            if w in nombres:
                p.val = p.menuNames[nombres.index(w)]
                return True
    except Exception:
        pass
    return False


def _legend_sala(W, c):
    """SALA (fase 23): el balance, el estado, el estroboscopio, los destellos del
    ultimo segundo y la salida DMX."""
    s = sala_de(W)
    now = absTime.seconds
    b = s['balance']
    bal = 'sin creacion' if b >= BALANCE_SIN_CREACION else '%.2f' % b
    txt = '  SALA     balance %s (%g s%s)   %s' % (bal, c['ventana_balance'],
                                               ', forzado' if c['sim_balance'] >= 0.0 else '',
                                               ESTADOS_SALA[s['estado']])
    if s['hz'] > 0.0:
        txt += '   estrobo %.1f Hz' % s['hz']
    txt += '   destellos %d/%d' % (destellos_ventana(W, now), DESTELLOS_MAX)
    if en_noche(W, now):
        txt += '   noche %.1f s' % max(0.0, s['noche'][1] - now)
    if c['colapso_on']:
        txt += '   colapso %s' % ('en %.1f s' % max(0.0, c['max_erosion'] - (now - s['desde']))
                                  if s['desde'] is not None else 'armado')
    hay, texto = dmx_encontrado()
    txt += '   dmx %s' % texto if hay else '   sin dmx (%s)' % texto
    return txt


# --- personas (fase 24) -----------------------------------------------------------

def personas_tablas(W, c, now):
    """Escribe las tablas personas y casillas_ocupadas (solo si han cambiado)."""
    filas_p = [[p['id'], '%.2f' % p['x'], '%.2f' % p['y'], '%.2f' % p['alt'],
                p['casilla'] if p['casilla'] is not None else '', '%.1f' % max(0.0, now - p['desde']),
                1 if p.get('nueva') else 0] for p in personas_en_sala()]
    filas_c = [[k, 1, v['personas'], '%.1f' % max(0.0, now - v['t_ocupada']), celda_de_casilla(W, c, k)]
               for k, v in sorted(_SALA.get('casillas', {}).items())]
    for nombre, cab, filas in (('personas', PERSONAS_COLS, filas_p), ('casillas_ocupadas', CASILLAS_COLS, filas_c)):
        t = parent().op(nombre)
        firma = [[str(x) for x in f] for f in filas]
        if t is None or _CACHE.get('tabla_' + nombre) == firma and t.numRows == len(filas) + 1:
            continue
        _CACHE['tabla_' + nombre] = firma
        t.clear()
        t.appendRow(cab)
        for f in filas:
            t.appendRow(f)


def personas_cook(scriptOp):
    """onCook del Script CHOP personas_chop: personas en sala, casillas ocupadas y
    llegadas (personas nuevas) desde que se cargo el motor."""
    _sin_timeslice(scriptOp)
    scriptOp.clear()
    scriptOp.numSamples = 1
    scriptOp.appendChan('personas')[0] = float(len(personas_en_sala()))
    scriptOp.appendChan('casillas')[0] = float(len(_SALA.get('casillas', {})))
    scriptOp.appendChan('nuevas')[0] = float(_SALA.get('nuevas', 0))


def personas_tick(W, c, now, alt):
    """Tras cada imagen de la camara (sala_tick): las cabezas, el seguimiento, lo
    que las personas hacen en el mundo y las tablas."""
    res = tick_personas(W, c, now, detectar_cabezas(alt, c) if alt is not None else [])
    sala_mundo(W, c, now, res)
    personas_tablas(W, c, now)
    o = parent().op('personas_chop')
    if o is not None:
        try:
            o.cook(force=True)
        except Exception:
            pass
    return res


def sala_fila_pulso(W, c, name):
    """Simformarfila: Simfila personas en casillas contiguas desde Simcasilla, en
    la tabla sala_personas (el mismo camino que la camara)."""
    t = parent().op('sala_personas')
    if t is None:
        return 'SALA  no esta la tabla sala_personas: relanza fase22_camara.py'
    if t.numRows == 0:
        t.appendRow(SALA_COLS)
    cas = casillas_fila_sim(c, _sim_casilla(c), max(1, int(c['sim_fila'])))
    for k in cas:
        x, y = casilla_xy(c, k)
        t.appendRow(['%.3f' % x, '%.3f' % y, '%.2f' % ALTURA_SIM])
    _SALA['fila_sim'] = list(cas)
    _SALA['t_img'] = -99.0
    return 'SALA  fila de %d personas en las casillas %s   personas simuladas: %d%s' % (
        len(cas), ' '.join(str(k) for k in cas), t.numRows - 1,
        '' if c['fuente_sala'] == FUENTE_SIMULADA else '   (Fuente no es simulada: no se ven)')


def _legend_personas(W, c):
    """PERSONAS (fase 24): las que hay, las casillas ocupadas y las llegadas."""
    cols, filas = rejilla_sala(c)
    fuente = 'simulada' if c['fuente_sala'] == FUENTE_SIMULADA else ('camara' if _SALA.get('hay') else 'sin camara')
    return '  PERSONAS %d en sala   casillas %d/%d   nuevas %d   %s' % (
        len(personas_en_sala()), len(_SALA.get('casillas', {})), cols * filas, _SALA.get('nuevas', 0), fuente)


# --- la huella minima (fase 25) -----------------------------------------------------

def _legend_huella(W, c):
    """HUELLA (fase 25): las inclusiones vivas, las llegadas y las paradas que
    las dejaron en este mundo, la ultima y Probllegada."""
    cu = W['incl_n']
    u = W.get('incl_ultima')
    ult = 'ultima celda %d escalon %d (%s)' % (u['celda'], u['escalon'], TIPO_INCL.get(u['tipo'], '?')) if u \
        else 'ultima -'
    return '  HUELLA   inclusiones %d (llegadas %d, paradas %d)   %s   llegada %g   parada %g s' % (
        n_inclusiones(W), cu['llegadas'], cu['paradas'], ult, c['prob_llegada'], c['t_parada'])


# --- la fila y la escision (fase 29) ---------------------------------------------------

ESCISIONES_COLS = ['id', 'jornada', 'ciclo', 'hora', 'personas', 'conchas', 'celda', 'estado', 'testigo']


def fila_escision(e):
    """La fila de la tabla escisiones (y del registro del historico) de una escision."""
    return [e['id'], e.get('jornada', ''), e.get('ciclo', ''), e.get('hora', ''), e['personas'],
            len(e['cortadas']), e['origen'], e['estado'], e.get('testigo') or '']


def escisiones_tabla(W):
    """Escribe la tabla escisiones (las ultimas ESCISIONES_MAX), solo si ha cambiado."""
    t = parent().op('escisiones')
    if t is None:
        return
    filas = [[str(x) for x in fila_escision(e)] for e in W['escisiones']]
    if _CACHE.get('tabla_escisiones') == filas and t.numRows == len(filas) + 1:
        return
    _CACHE['tabla_escisiones'] = filas
    t.clear()
    t.appendRow(ESCISIONES_COLS)
    for f in filas:
        t.appendRow(f)


def sala_sumar_pulso(W, c):
    """Simsumar: una persona mas en la casilla contigua a la fila de prueba."""
    t = parent().op('sala_personas')
    if t is None:
        return 'SALA  no esta la tabla sala_personas: relanza fase22_camara.py'
    fila = list(_SALA.get('fila_sim') or [])
    if not fila:
        return 'SALA  no hay fila de prueba: pulsa antes Simformarfila'
    sig = casillas_fila_sim(c, fila[0], len(fila) + 1)
    if len(sig) <= len(fila):
        return 'SALA  la fila de prueba no cabe mas en la sala'
    x, y = casilla_xy(c, sig[-1])
    t.appendRow(['%.3f' % x, '%.3f' % y, '%.2f' % ALTURA_SIM])
    _SALA['fila_sim'] = sig
    _SALA['t_img'] = -99.0
    return 'SALA  una persona mas en la casilla %d: fila de %d   personas simuladas: %d' % (
        sig[-1], len(sig), t.numRows - 1)


def _legend_fila(W, c):
    """FILA y ESCISION (fase 29): la fila mas larga de la sala y la ultima escision."""
    now = _SALA.get('t_personas') or absTime.seconds
    modo = MODOS_FILA[int(c['modo_fila']) % len(MODOS_FILA)]
    filas = _SALA.get('filas') or []
    if filas:
        f = max(filas, key=lambda x: (x['personas'], -x['id']))
        l1 = '  FILA     %d personas   %s   %.1f/%.1f s' % (
            f['personas'], modo, min(c['t_fila'], max(0.0, now - f['t0'])), c['t_fila'])
        if len(filas) > 1:
            l1 += '   (%d filas)' % len(filas)
    else:
        l1 = '  FILA     -   %s   (desde %d personas, %g s)' % (modo, int(c['min_fila']), c['t_fila'])
    esc = W['escisiones']
    if esc:
        e = esc[-1]
        l2 = '  ESCISION #%d   celda %d   conchas %d/%d   %s' % (
            e['id'], e['origen'], len(e['cortadas']), n_shells(W), e['estado'])
    else:
        l2 = '  ESCISION -'
    pend = [f for f in filas if f['escision'] is None]
    if pend:
        f = max(pend, key=lambda x: now - x['t0'])
        l2 += '   (sin abrir: fila %.1f/%.1f s)' % (max(0.0, now - f['t0']), c['t_fila'])
    return l1 + '\n' + l2


def _legend_relampago(W, c):
    """RELAMPAGO (fase 30): cuanto hace del ultimo, los destellos del ultimo segundo y el DMX."""
    s = sala_de(W)
    now = absTime.seconds
    tr = s.get('t_relampago')
    if s.get('pend') and s['pend'].get('quien') == 'relampago':
        cuando = 'pendiente (espera un hueco)'
    elif tr is not None:
        cuando = 'hace %.1f s' % max(0.0, now - tr)
    else:
        cuando = '-'
    hay, texto = dmx_encontrado()
    return '  RELAMPAGO %s   destellos %d/%d en el ultimo segundo   %s' % (
        cuando, destellos_ventana(W, now), DESTELLOS_MAX, 'dmx %s' % texto if hay else 'sin dmx')


# --- las escisiones en el historico (fase 31) ---------------------------------------

def carpeta_historico(c=None):
    """La carpeta del historico (Carpetahistorico), creada si hace falta. None si no se puede."""
    import os
    c = c or cfg_foto()
    ruta = str(c.get('carpeta_historico') or '').strip()
    if not ruta:
        return None
    try:
        os.makedirs(ruta, exist_ok=True)
    except Exception as e:
        _say('historico', 'AVISO  historico: no puedo crear %s (%s)' % (ruta, e))
        return None
    return ruta.replace('\\', '/').rstrip('/')


def _a_top(img):
    """La imagen (fila 0 arriba) como la quiere un Script TOP (fila 0 abajo)."""
    return img[::-1].copy()


def seccion_cook(scriptOp):
    """onCook del Script TOP seccion: la ultima seccion dibujada."""
    img = _HIST.get('imagen')
    if img is None:
        np = _np()
        if np is None:
            return
        img = np.zeros((SECCION_PX[1], SECCION_PX[0], 4), dtype=np.float32)
        img[..., 3] = 1.0
    scriptOp.copyNumpyArray(_a_top(img))


def columna_cook(scriptOp):
    """onCook del Script TOP columna_jornada: la columna resumen de la jornada de hoy
    (o de la que se esta exportando)."""
    W, c = world(), cfg_foto()
    img, meta = columna_jornada(W, c, _HIST.get('jornada_top') or _fecha()[0])
    if img is not None:
        _HIST['columna_meta'] = meta
        scriptOp.copyNumpyArray(_a_top(img))


def _guardar_top(nombre, ruta):
    """Recuece el Script TOP y lo guarda en ruta (TOP.save). Devuelve si ha ido bien."""
    o = parent().op(nombre)
    if o is None:
        return False
    try:
        o.cook(force=True)
        o.save(ruta)
        return True
    except Exception as e:
        _say('guardar_' + nombre, 'AVISO  historico: no pude guardar %s (%s)' % (ruta, e))
        return False


def exportar_testigo(e, img=None, meta=None):
    """Guarda la seccion de la escision e en historico/escision_<jornada>_c<ciclo>_<id>.png
    (si no se la dan, la dibuja ahora). Devuelve el nombre del fichero, o None."""
    W, c = world(), cfg_foto()
    if img is None:
        img, meta = seccion_escision(W, c, e)
    carpeta = carpeta_historico(c)
    if img is None or carpeta is None:
        return None
    _HIST['imagen'], _HIST['meta'] = img, meta
    nombre = nombre_testigo(e)
    if not _guardar_top('seccion', carpeta + '/' + nombre):
        return None
    e['testigo'] = nombre
    _HIST['exportadas'] += 1
    return nombre


def exportar_columna(jornada=None):
    """Guarda la columna resumen de la jornada en historico/columna_<jornada>.png."""
    c = cfg_foto()
    carpeta = carpeta_historico(c)
    jornada = jornada or _fecha()[0]
    if carpeta is None:
        return None
    _HIST['jornada_top'] = jornada
    nombre = 'columna_%s.png' % jornada
    bien = _guardar_top('columna_jornada', carpeta + '/' + nombre)
    _HIST['jornada_top'] = None
    return nombre if bien else None


def registrar_escision(W, e):
    """Una fila por escision en historico/escisiones.csv (UTF-8, separador ;), al
    cerrarse. No duplica: si ya esta (id, jornada y hora), no la repite. Devuelve
    si la ha escrito."""
    import os
    carpeta = carpeta_historico()
    e['registrada'] = True
    if carpeta is None:
        return False
    ruta = carpeta + '/escisiones.csv'
    clave = '%s;%s;' % (e['id'], e.get('jornada', ''))
    try:
        viejas = []
        if os.path.exists(ruta):
            with open(ruta, encoding='utf-8') as f:
                viejas = f.read().splitlines()
        if any(l.startswith(clave) and l.split(';')[3:4] == [str(e.get('hora', ''))] for l in viejas):
            return False
        with open(ruta, 'a', encoding='utf-8') as f:
            if not viejas:
                f.write(';'.join(REGISTRO_COLS) + '\n')
            f.write(linea_registro(e) + '\n')
        return True
    except Exception as ex:
        _say('registro', 'AVISO  historico: no pude escribir %s (%s)' % (ruta, ex))
        return False


def historico_tick(W, c, now):
    """Cada fotograma: guarda como mucho un testigo pendiente (para no cortar el
    fotograma), apunta en el registro las escisiones que se han cerrado y, al
    cambiar la fecha, exporta la columna de la jornada que acaba."""
    pend = _HIST['pend']
    ids = set(p[0] for p in pend)
    for e in W['escisiones']:           # pendientes de una sesion anterior (el motor se recargo)
        if e.get('testigo') == 'pendiente' and e['id'] not in ids:
            e['testigo'] = None
            encolar_testigo(W, c, e, now)
    if pend:
        ide, img, meta = pend.pop(0)
        e = escision_de(W, ide)
        if e is not None and exportar_testigo(e, img, meta) is None:
            e['testigo'] = None         # no se pudo: no se queda pendiente para siempre
            e['sin_testigo'] = True
    for e in W['escisiones']:
        if e['estado'] != 'abierta' and not e.get('registrada') and e.get('testigo') != 'pendiente':
            registrar_escision(W, e)
    hoy = _fecha()[0]
    ayer = _HIST.get('jornada')
    if ayer and ayer != hoy and (ciclos_jornada(W, ayer) or any(e.get('jornada') == ayer for e in W['escisiones'])):
        exportar_columna(ayer)
    _HIST['jornada'] = hoy
    firma = (len(W['shells']), len(W['escisiones']), hoy)
    if _HIST.get('firma_columna') != firma:
        _HIST['firma_columna'] = firma
        o = parent().op('columna_jornada')
        if o is not None:
            try:
                o.cook(force=True)
            except Exception:
                pass


def exportar_pulso(W, c):
    """Exportartestigo: la seccion de la ultima escision (como esta ahora) y la columna de hoy."""
    if not W['escisiones']:
        return 'HISTORICO  no hay ninguna escision'
    e = W['escisiones'][-1]
    nombre = exportar_testigo(e)
    col = exportar_columna()
    if nombre is None:
        return 'HISTORICO  no pude exportar el testigo de la escision %d (mira Carpetahistorico)' % e['id']
    return 'HISTORICO  %s%s en %s' % (nombre, ' y %s' % col if col else '', carpeta_historico(c))


def _legend_historico(W, c):
    """HISTORICO (fase 31): las escisiones de hoy, la ultima y su testigo."""
    hoy = _fecha()[0]
    n = sum(1 for e in W['escisiones'] if e.get('jornada') == hoy)
    if not W['escisiones']:
        return '  HISTORICO escisiones hoy 0   ultima -'
    e = W['escisiones'][-1]
    tg = e.get('testigo')
    estado = 'testigo pendiente' if tg == 'pendiente' else ('testigo exportado' if tg else
                                                             ('sin testigo' if e['estado'] != 'abierta'
                                                              else 'testigo al deshacerse la fila o al enterrar'))
    return '  HISTORICO escisiones hoy %d   ultima #%d J%s C%s %d personas %d conchas celda %d   %s' % (
        n, e['id'], e.get('jornada', ''), e.get('ciclo', ''), e['personas'], len(e['cortadas']), e['origen'], estado)


def dia(frame=None):
    """1 - noche (fase 28): lo que multiplica el color de las luces. 1 antes de la
    fase 28. Una vez por fotograma (frame_tick); fuera de el, del mundo."""
    v = _CACHE.get('dia')
    if v is None or _CFG_FOTO.get('off'):
        try:
            c = cfg_foto()
            v = 1.0 - noche_nivel(world(), c, absTime.seconds) if c['nivel'] >= 28 else 1.0
        except Exception:
            v = 1.0
    return float(v)


def _legend_noche(W, c):
    """NOCHE (fase 28): lo que dura, lo que queda y lo que emite."""
    n = W.get('noche')
    now = absTime.seconds
    quedan = max(0.0, n[1] - now) if n and now >= n[0] else 0.0
    inc, esc = emiten_noche(W, c)
    return '  NOCHE    %.1f s   quedan %.1f   emiten %d inclusion%s y %d escision%s' % (
        c['noche'], quedan, inc, '' if inc == 1 else 'es', esc, '' if esc == 1 else 'es')


def _legend_banda(W, c):
    """BANDA (fase 27): la ultima concha (humana o limpia, sus huellas y su
    cobertura), el colapso y cuantas conchas son estratos humanos."""
    shells = W['shells']
    humanas = sum(1 for sh in shells if sh.get('banda') == 'humana')
    if not shells:
        return '  BANDA    ultima: -   (min %d)   humanas 0 de 0' % int(c['min_huellas'])
    banda, n, col = banda_de(shells[-1])
    return '  BANDA    ultima: %s %d huellas (min %d)   cobertura %d%% (max %d%%)   colapso %s   humanas %d de %d' % (
        'estrato humano' if banda == 'humana' else 'concha limpia', n, int(c['min_huellas']),
        int(round(100.0 * cobertura_concha(c, shells[-1]))), int(round(100.0 * c['inclusiones_max'])),
        'si' if col else 'no', humanas, len(shells))


def _legend_borrado(W, c):
    """BORRADO (fase 26): las inclusiones vivas y las borradas, por causa."""
    b = W['incl_borradas']
    partes = ['%s %d' % (k, b.get(k, 0)) for k in CAUSAS_BORRADO if k != 'escision' or b.get(k, 0)]
    return '  BORRADO  vivas %d   borradas %d (%s)' % (n_inclusiones(W), sum(b.values()), ', '.join(partes))


# --- cada camara con sus ajustes (motor v96) ---------------------------------------
# Al elegir Modocamara se ponen los ajustes de ese modo (los que se toquen despues
# valen hasta que se vuelva a elegir). Globo y superficie: los de la hoja
# Estratos_parametros (Camaltura 1,7 es la de la captura del 21 de octubre; el
# resto, de fabrica). Rasante: los de la prueba en TouchDesigner del 13 de noviembre
# (Rasanillo 8 pedia el ultimo limite entre anillos: con 7 anillos es el 6).
_CLASICA = (('Camfov', 45.0), ('Encuadre', 0.85), ('Camsuave', 3.0), ('Camaltura', 1.7), ('Camvel', 0.6))
CAMARAS = dict(
    globo=_CLASICA,
    superficie=_CLASICA,
    rasante=(('Rasaltura', 0.77), ('Rasfov', 120.0), ('Rasmirada', -13.6), ('Rasvel', 3.52), ('Rasanillo', 6)),
)


def ajustes_camara(modo):
    """Pone los ajustes de la camara 'modo' (CAMARAS). Devuelve los que ha cambiado."""
    puestos = []
    for nombre, valor in CAMARAS.get(str(modo), ()):
        try:
            p = getattr(parent().par, nombre, None)
            if p is None:
                continue
            if abs(float(p.eval()) - float(valor)) > 1e-9:
                p.val = valor
                puestos.append(nombre)
        except Exception:
            pass
    return puestos


def on_value(name, val):
    if name == 'Modocamara':            # motor v96: cada camara con sus ajustes
        puestos = [] if _CACHE.get('sin_ajustes') else ajustes_camara(val)   # las autopruebas los apartan
        if puestos:
            print('CAMARA  %s: %s' % (val, ', '.join('%s %g' % (n, float(getattr(parent().par, n).eval()))
                                                    for n in puestos)))
    elif name == 'Modoactuacion':
        try:
            parent().par.Showgrid = not bool(val)
        except Exception:
            pass
    elif name in ('Variantes', 'Varangulo', 'Cuantizar30', 'Densidadhoja'):    # fase 11 v8 (v9: solo Variantes)
        c = cfg()
        biblioteca(c)                   # se precalcula de nuevo
        if VARIANTES_TD and int(c['variantes']) > VARIANTES_TD:
            print('FASE11  Variantes %d: hay geometria para %d; relanza fase11_piel.py para las demas'
                  % (int(c['variantes']), VARIANTES_TD))
        mo = parent().op('modelos')
        for o in (mo.findChildren(name='veg_*', depth=1) if mo is not None else []):
            s = o.op('malla')
            if s is not None:
                try:
                    s.cook(force=True)
                except Exception:
                    pass
    elif name in ('Variantesciudad', 'Oblicuidad', 'Retranqueo', 'Torsionmax', 'Variantesind'):   # fase 11 v10-v11
        c = cfg()
        biblioteca_ciudad(c)
        if VARIANTES_CIU_TD and int(c['variantes_ciudad']) > VARIANTES_CIU_TD:
            print('FASE11  Variantesciudad %d: hay geometria para %d; relanza fase11_piel.py para las demas'
                  % (int(c['variantes_ciudad']), VARIANTES_CIU_TD))
        mo = parent().op('modelos')
        for o in (mo.findChildren(name='edi_*', depth=1) if mo is not None else []):
            s = o.op('malla')
            if s is not None:
                try:
                    s.cook(force=True)
                except Exception:
                    pass
    elif name == 'Escena':              # fase 18: cargar la escena elegida
        n = cargar_escena(str(val))
        print('ESCENA  %s cargada (%d parametros)' % (val, n))
    elif name == 'Interfazdmx':         # fase 23: la interfaz del DMX Out CHOP
        if parent().op('dmx_out') is not None and not interfaz_dmx_al_dia(str(val)):
            print('AVISO  dmx_out: no pude poner la interfaz %s; elige Interface a mano' % val)


# --- escenas (fase 18) --------------------------------------------------------

def tabla_escenas():
    """La tabla 'escenas' (escena, parametro, valor), o None."""
    try:
        return parent().op('escenas')
    except Exception:
        return None


def valores_escena(nombre):
    """{parametro: valor (texto)} de la escena en la tabla; si no esta, la de
    por defecto."""
    out = dict((k, str(v)) for k, v in escena_defecto(nombre).items()) if nombre in ESCENAS else {}
    t = tabla_escenas()
    if t is not None:
        guardadas = {}
        for r in range(1, t.numRows):
            if t[r, 0].val == nombre:
                guardadas[t[r, 1].val] = t[r, 2].val
        for viejo, nuevo in ESCENA_MIGRA.items():   # motor v101: Refresconat -> Refrescopiel
            if viejo in guardadas:
                v = guardadas.pop(viejo)
                guardadas.setdefault(nuevo, v)
        out.update(guardadas)
    return out


def _poner(nombre, valor):
    """Pone un parametro de la escena: de FASE1 o de una luz (op.par)."""
    if '.' in nombre:
        o, par = nombre.split('.', 1)
        dst = parent().op(o)
    else:
        dst, par = parent(), nombre
    p = getattr(dst.par, par, None) if dst is not None else None
    if p is None:
        return False
    try:
        v = float(valor)
        p.val = int(v) if getattr(p, 'style', '') == 'Int' else v
    except (ValueError, TypeError):
        p.val = valor
    return True


def cargar_escena(nombre):
    """Pone los parametros de la escena. Devuelve cuantos."""
    n = 0
    for k, v in valores_escena(nombre).items():
        try:
            n += 1 if _poner(k, v) else 0
        except Exception:
            pass
    return n


def _leer(nombre):
    if '.' in nombre:
        o, par = nombre.split('.', 1)
        src = parent().op(o)
    else:
        src, par = parent(), nombre
    p = getattr(src.par, par, None) if src is not None else None
    return None if p is None else p.eval()


def guardar_escena(nombre=None):
    """Guarda en la tabla los valores actuales de los parametros de la escena."""
    nombre = nombre or ESCENAS[_menu('Escena', ESCENAS, 0)]
    t = tabla_escenas()
    if t is None:
        return 0
    filas = [[t[r, k].val for k in range(3)] for r in range(1, t.numRows) if t[r, 0].val != nombre]
    nuevas = []
    for fila in ESCENA_PARS:
        v = _leer(fila[0])
        if v is not None:
            nuevas.append([nombre, fila[0], str(v)])
    t.clear()
    t.appendRow(['escena', 'parametro', 'valor'])
    for f in filas + nuevas:
        t.appendRow(f)
    return len(nuevas)


# --- balanceo del eje (rotacion extra, desde la fase 3) ----------------------

def canales_frame(spec, frame=None):
    """Motor v69 (comun v49): los canales del Script CHOP 'frame_u', una vez por
    fotograma: el giro del planeta (ry), el balanceo del eje (rx) y los uniformes de
    la piel que pide spec [(canal, tipo, nombre, k)]: piel (uniformes_piel), luz
    (color x dimmer de una luz), mod (las senales del modular) y ventanas."""
    out = []
    try:
        out.append(('ry', float(_ritmo().rotation(frame))))
    except Exception:
        out.append(('ry', 0.0))
    try:
        out.append(('rx', float(wobble(frame))))
    except Exception:
        out.append(('rx', 0.0))
    # motor v73: la luz de destello (posicion, dimmer y color), para que luz_destello
    # solo lea canales y no evalue 7 expresiones Python por fotograma
    try:
        fl = flash_light()
    except Exception:
        fl = (0.0, 0.0, 0.0, 0.0) + tuple(FLASH_COL)
    for canal, v in zip(DESTELLO_CANALES, fl):
        out.append((canal, float(v)))
    t_h, lfo_h = humo_reloj(frame)             # motor v74: el reloj de mat_humo
    out.append(('humo_t', float(t_h)))
    out.append(('humo_lfo', float(lfo_h)))
    amp, vto, _ = viento_reloj(frame)          # motor v77: el vaiven del dosel, en la GPU
    out.append(('viento_amp', amp))
    out.append(('viento_lfo', vto))
    for canal, tipo, nombre, k in spec or ():
        try:
            if tipo == 'piel':
                v = piel_uniforme(nombre, k, frame)
            elif tipo == 'luz' and nombre == 'luz_destello':
                # motor v78: el color de luz_destello sale de frame_u (fl_r, fl_g, fl_b y
                # fl_dim, arriba); leerlo de la Light COMP hacia que frame_u dependiera de
                # si mismo ('Cook dependency loop detected' en frame_u)
                v = float(fl[4 + int(k)]) * float(fl[3])
            elif tipo == 'luz':
                v = luz_color(nombre, k, frame)
            elif tipo == 'mod':
                v = modular_uniforme(nombre, k, frame)
            elif tipo == 'ventanas':
                v = ventanas_luz(frame)
            else:
                v = 0.0
        except Exception:
            v = 0.0
        out.append((canal, float(v)))
    return out


def temas_de_modelo(mo):
    """Motor v69: los temas en los que se ve la geometria de un modelo. Las de los
    cortes (fos_, arq_, las galerias de la industria) se ven en todos: ensenan las
    eras de cualquier tema."""
    if es_ejemplar(mo) or mo.startswith(('veg_', 'rel_')):
        return ('naturaleza',)
    if es_edificio(mo):
        return ('industria',) if parte_edificio(mo)[0] in INDUSTRIALES else ('ciudad',)
    if mo in ('ind_crater', 'ind_ruina', 'ind_hollin'):
        return ('industria',)
    if mo == 'inf_escombros':
        return ('ciudad',)
    if mo.startswith('ciu_'):
        return ('ciudad', 'industria')
    return tuple(TEMAS)


# --- motor v79: de que secuenciador sale cada geometria (los bocetos de FASE1) ------
# El SEQ1 es la especie GEO de cada tema (vegetacion, informal, mina) y el SEQ2 la ARQ
# (relieve, planificada, energia). Un modelo es del secuenciador cuya especie lo pide
# en el catalogo; un ejemplar de la vegetacion, por su planta; un edificio, por su
# diseno. Lo que no es de ningun modelo, o lo piden las dos, es de los dos.
GEO_SEQ = {GEO: 1, ARQ: 2}
BOCETO_SEQ2 = ('coronas',)                  # las coronas son del SEQ2 (fase 4)
BOCETO_SEQ1 = ('vagones', 'pradera')        # los vagones salen de las minas (SEQ1); la pradera es vegetacion


def seqs_de_modelo(mo, cfg=None):
    """{1}, {2} o {1, 2}: de que secuenciador sale el modelo mo."""
    cfg = cfg or DEFAULT_CFG
    clave = ('seqs', mo, id(_cat(cfg)))
    v = _CACHE.get(clave)
    if v is not None:
        return v
    propia = dict((esp, GEO_SEQ[own]) for (tema, own), esp in ESPECIES.items())
    buscar = {mo}
    if es_ejemplar(mo):
        buscar.add(parte_ejemplar(mo)[0])
    if es_edificio(mo):
        d = parte_edificio(mo)[0]
        buscar.add(d)
    out = set()
    for (tema, esp, estado), lista in _cat(cfg).items():
        if esp in propia and buscar & set(x for x in lista if isinstance(x, str)):
            out.add(propia[esp])
    if es_edificio(mo):
        d = parte_edificio(mo)[0]
        for esp, tipos in TIPOS.items():
            if esp in propia and any(d in DISENOS_TIPO.get(tp, ()) for tp in tipos):
                out.add(propia[esp])
    if not out:
        out = {1} if mo.startswith('veg_') else {2} if mo.startswith('rel_') else {1, 2}
    _CACHE[clave] = frozenset(out)
    return _CACHE[clave]


def seqs_de_geometria(nombre, cfg=None):
    """{1}, {2} o {1, 2}: de que secuenciador sale lo que dibuja la geometria
    nombre de FASE1 (para los bocetos); None si es de las conchas o la esfera, o
    del armazon (nucleo, reticula, luces de las conchas), que no van por secuenciador."""
    if nombre in ('estratos', 'terreno', 'nucleo', 'reticula', 'luz_conchas', 'diagnostico',
                  'inclusiones', 'fulguritas'):     # fases 25 y 29: las huellas de las personas
        return None
    if nombre in BOCETO_SEQ1:
        return frozenset({1})
    if nombre in BOCETO_SEQ2:
        return frozenset({2})
    for g, mo, _ in geometrias_piel(cfg):
        if g == nombre:
            return seqs_de_modelo(mo, cfg)
    return frozenset({1, 2})


def geometrias_activas(cfg):
    """Las geometrias de los modelos que pueden tener instancias con el tema actual."""
    tema = tema_de(cfg)
    return [g for g, mo, _ in geometrias_piel(cfg) if tema in temas_de_modelo(mo)]


RENDER_2D, RENDER_OJO = 'render2d', 'fisheye180'    # Render Mode del Render TOP: 2D y Fish-Eye (180)


def modo_render(c):
    """El Render Mode que toca: ojo de pez con la camara rasante (desde la mitad de
    su transicion) y Rasojo; si no, el 2D de siempre."""
    if c['nivel'] < 10 or not _p('Rasojo', False):
        return RENDER_2D
    try:
        return RENDER_OJO if camera_state()['wr'] >= 0.5 else RENDER_2D
    except Exception:
        return RENDER_2D


def render_modo_al_dia(c):
    """Motor v95: pone el Render Mode del Render TOP cuando cambia (no en cada
    fotograma). Devuelve si lo ha cambiado."""
    quiere = modo_render(c)
    if _CACHE.get('render_modo') == quiere:
        return False
    try:
        r = parent().op('render')
        if str(r.par.rendermode.eval()) != quiere:
            r.par.rendermode = quiere
        if str(r.par.rendermode.eval()) != quiere:
            raise ValueError('el Render TOP no tiene el modo %s' % quiere)
    except Exception as e:
        if quiere == RENDER_OJO and not _CACHE.get('render_modo_aviso'):
            _CACHE['render_modo_aviso'] = True
            print('AVISO  ojo de pez: no pude poner Render Mode = Fish-Eye (180) en render (%s); '
                  'ponlo a mano o apaga Rasojo' % e)
        _CACHE['render_modo'] = quiere      # no se reintenta en cada fotograma
        return False
    _CACHE['render_modo'] = quiere
    return True


def render_tema_al_dia(c):
    """Motor v69: el Render TOP solo dibuja las geometrias del tema actual (con las
    ~300 de los tres temas, TouchDesigner cocinaba y dibujaba las vacias en cada
    fotograma). Se rehace al cambiar de tema o si una fase rehizo la lista."""
    if c['nivel'] < 11:
        return False
    try:
        r = parent().op('render')
        actual = str(r.par.geometry.val)
    except Exception:
        return False
    clave = (tema_de(c), c['nivel'] < 12, variantes(c), variantes_ciudad(c), variantes_ind(c))
    if _CACHE.get('render_tema') == clave and _CACHE.get('render_str') == actual:
        return False
    nombres = actual.split()
    resto = [n for n in nombres if not n.startswith('mod_')]
    activos = sorted(set(geometrias_activas(c)))
    k = resto.index('coronas') if 'coronas' in resto else len(resto)
    nuevo = ' '.join(resto[:k] + activos + resto[k:])
    try:
        r.par.geometry = nuevo
    except Exception:
        return False
    _CACHE['render_tema'], _CACHE['render_str'] = clave, nuevo
    return True


def wobble(frame=None):
    try:
        return _wobble()
    except Exception:
        return 0.0


def _wobble():
    """Grados de rx de todas las geometrias del planeta. Inclina el eje
    hacia la camara y en contra, para que se vean los dos polos. Ajeno al
    reloj del secuenciador. Pagina Fase3: Balanceo (0 = apagado) y
    Balanceoper."""
    if _CACHE.get('wob_frame') == absTime.frame:
        return _CACHE.get('wob', 0.0)
    t = absTime.seconds
    st = _CACHE.setdefault('wob_st', {'ph': 0.0, 'env': 0.0})
    dt = t - _CACHE.get('wob_t', t)
    _CACHE['wob_t'] = t
    amp = max(0.0, _p('Balanceo', 60.0))
    if amp > 0.0:                       # al poner 0 sale en 3 s con la ultima amplitud
        st['amp'] = amp
    v = wobble_step(st, dt, amp > 0.0, _p('Pausa', False),
                    st.get('amp', amp), _p('Balanceoper', 90.0))
    _CACHE['wob'] = v
    _CACHE['wob_frame'] = absTime.frame
    return v


# --- luz de destello y camara (fases 9 y 10) ---------------------------------

FLASH_COL = (0.80, 0.95, 1.00)


def flash_color(W, c):
    """Color del destello: el del pad que golpea, aclarado para que siga
    siendo un golpe de luz (lo mezcla un 35 % con blanco)."""
    f = W.get('flash') or {}
    if 'pad' not in f:
        return FLASH_COL
    cols = c.get('colores_drum') or COLORES_DRUM
    col = cols[int(f['pad']) % len(cols)]
    return _mix(col, (1.0, 1.0, 1.0), 0.35)


def flash_light():
    """(x, y, z, dimmer, r, g, b) de la luz de destello."""
    W, c = world(), cfg_foto()
    f = W.get('flash')
    if not f or c['nivel'] < 9:
        return (0.0, 0.0, 0.0, 0.0) + FLASH_COL
    env = math.exp(-max(0.0, absTime.seconds - f['t']) / 0.25) * f['k']
    if f.get('bomba'):                  # fase 7: el de un impulso, suave y con la curva del pumping
        env = f['k'] * bomba_frac(W, f['cell'], absTime.seconds)
    try:
        ang = _ritmo().rotation(absTime.frame)
        tilt = float(parent().par.Tilt)
    except Exception:
        ang, tilt = 0.0, 0.0
    v = world_dir(normal_i(f['cell']), ang, tilt, wobble())
    d = suelo(W, c, f['cell']) + W['vh'][f['cell']] + 4.0   # sobre su suelo y su formacion
    return (v[0] * d, v[1] * d, v[2] * d, c['flash'] * env * dia()) + tuple(flash_color(W, c))     # fase 28


DESTELLO_CANALES = ('fl_tx', 'fl_ty', 'fl_tz', 'fl_dim', 'fl_r', 'fl_g', 'fl_b')


def flash_value(k, frame=None):
    """Motor v72: los 7 valores de la luz de destello, calculados una vez por fotograma."""
    f = absTime.frame
    if _CFG_FOTO.get('off'):
        return flash_light()[k]
    if _CACHE.get('flash_f') != f:
        _CACHE['flash_v'] = flash_light()
        _CACHE['flash_f'] = f
    return _CACHE['flash_v'][k]


LUZ_COLOR = ('c%s', 'lightcolor%s', 'color%s')     # el color de una Light COMP es cr cg cb


def luz_color(nombre, k, frame=None):
    """Componente k (0 r, 1 g, 2 b) del color x dimmer de la luz 'nombre',
    para el shader de la piel (fase 12). Prueba los nombres del color de la
    Light COMP (cr cg cb); si no hay ninguno, blanco."""
    try:
        o = parent().op(nombre)
        if o is None:
            return 0.0
        v = 1.0
        for patron in LUZ_COLOR:
            p = getattr(o.par, patron % 'rgb'[int(k)], None)
            if p is not None:
                v = float(p.eval())
                break
        d = getattr(o.par, 'dimmer', None)
        return v * (float(d.eval()) if d is not None else 1.0)
    except Exception:
        return 0.0


# --- camara (motor v24; Encuadre, v36) ---------------------------------------------
# Por defecto, camara de GLOBO: mira al centro, en la direccion de referencia
# (+Z, hacia la que se balancea el eje), y encuadra el planeta entero: su
# diametro ocupa Encuadre del lado mas estrecho del cuadro (1 = de borde a
# borde; con 0,85 queda sitio arriba y abajo para lo que crece sobre el). El
# encuadre solo cambia cuando el planeta engorda (una concha nueva): la camara
# se aleja en Camsuave s y el planeta nunca se sale del cuadro. Crecer,
# erosionar o el latido no la mueven. La de SUPERFICIE (fase 10 v4) queda como
# modo (Modocamara).

CAM_DIR = (0.0, 0.0, 1.0)          # direccion de referencia de la camara
CAM_TRANS = 20.0                   # segundos del cambio de modo (Modocamara)
ENCUADRE = 0.85                    # alto del planeta en la pantalla (1 = de borde a borde)
RETICULA_SOBRE = 0.2               # lo que asoma la reticula sobre el planeta
CAJA_EXT = (0.5, 1.0, 0.5)         # semiejes de la caja de las geometrias (base en y = 0)
SIN_EXTENSION = ('estratos', 'luz_conchas')     # no pasan de la superficie
_EXT = {}


def altura_max(cfg):
    """Lo mas alto que llega, sobre su suelo, algo que gira con el planeta:
    una formacion en el limite hinchada por el latido y, encima, la corona
    mas larga (la de una torre en su ultimo tramo de cumbre)."""
    lim = limit(cfg)
    corona = 0.90 * (1.0 + 0.25 * max(0, int(cfg['cumbre_tramos']))) * lim
    # motor v46: un bosque en lo alto del monte mas alto
    monte_ = max(0.0, cfg.get('altura_monte', DEFAULT_CFG['altura_monte'])) * lim + 1.2 * lim * CANOPIA_K
    monte_ = max(monte_, max(0.0, cfg.get('altura_monte', DEFAULT_CFG['altura_monte'])) * lim
                 + lim * (CORONA_K + CORONA_TRAMO * max(0, int(cfg['cumbre_tramos']))))   # v48: el emergente
    return max(lim * (1.0 + LATIDO_AMP) + corona, monte_ * (1.0 + LATIDO_AMP))


def radio_encuadre(W, cfg):
    """Lo mas lejos que podria llegar algo: el radio nominal mas la altura
    maxima (el encuadre de la v24 a la v31). La camara ya no lo usa."""
    return top_radius(W, cfg) + altura_max(cfg)


def _ext_modelo(modelo):
    """Semiejes (x, y, z) de un modelo del catalogo, desde su origen."""
    v = _EXT.get(modelo)
    if v is None and es_edificio(modelo):     # fase 11 v10: un ejemplar de la ciudad
        v = _EXT[modelo] = (0.5, 1.0, 0.5)
    if v is None and es_ejemplar(modelo):     # fase 11 v8: un ejemplar de la biblioteca
        mo, var, d, _ = parte_ejemplar(modelo)
        r = ejemplar(DEFAULT_CFG, mo, var, d)['radio']
        v = _EXT[modelo] = (r, 1.0, r)
    if v is None:
        b = _caja_modelo(MODELOS[modelo])
        v = _EXT[modelo] = (max(abs(b[0]), abs(b[1])), max(abs(b[2]), abs(b[3])),
                            max(abs(b[4]), abs(b[5])))
    return v


_EJE_Y = {}


def _eje_y(rx, ry, rz):
    """El eje Y local de una instancia girada rx ry rz (orden xyz)."""
    k = (rx, ry, rz)
    v = _EJE_Y.get(k)
    if v is None:
        if len(_EJE_Y) > 50000:
            _EJE_Y.clear()
        a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
        sa, ca, sb, cb, sc, cc = math.sin(a), math.cos(a), math.sin(b), math.cos(b), math.sin(c), math.cos(c)
        v = _EJE_Y[k] = (sa * sb * cc - ca * sc, sa * sb * sc + ca * cc, sa * cb)
    return v


def radio_visible(inst, W, cfg):
    """Lo mas lejos del centro que llega algo de lo que se dibuja (solo para
    la leyenda: dice si lo mas alto cabe con el Encuadre): la superficie (con la
    reticula) y cada instancia. De cada pieza se toma su
    alto (eje Y local, segun lo inclinada que este respecto a la vertical
    de su sitio) y su ancho: una pieza tumbada, como un puente, no cuenta
    su largo como altura. No depende del giro del planeta."""
    r2 = (top_radius(W, cfg) + 0.2) ** 2
    modelos = dict((g, mo) for g, mo, _ in geometrias_piel(cfg)) if cfg['nivel'] >= 11 else {}
    sq = math.sqrt
    for g, filas in inst.items():
        if not filas or g in SIN_EXTENSION:
            continue
        ex, ey, ez = _ext_modelo(modelos[g]) if g in modelos else CAJA_EXT
        for f in filas:
            P = sq(f[0] * f[0] + f[1] * f[1] + f[2] * f[2])
            h = ey * abs(f[7])
            lat = sq((ex * f[6]) ** 2 + (ez * f[8]) ** 2)
            if P > 1e-9:
                uy = _eje_y(f[3], f[4], f[5])
                co = abs(f[0] * uy[0] + f[1] * uy[1] + f[2] * uy[2]) / P
                si = sq(max(0.0, 1.0 - co * co))
            else:
                co, si = 1.0, 1.0
            rad = P + h * co + lat * si
            per = h * si + lat
            d2 = rad * rad + per * per
            if d2 > r2:
                r2 = d2
    return sq(r2)


def fovs(fov_deg, aspect, metodo='horzfov'):
    """(fov horizontal, fov vertical) en radianes. 'metodo' dice a que lado
    se aplica fov_deg (TouchDesigner: horizontal por defecto)."""
    f = math.radians(max(1.0, min(179.0, fov_deg)))
    aspect = max(1e-3, aspect)
    if 'vert' in str(metodo):
        fv = f
        fh = 2.0 * math.atan(aspect * math.tan(fv / 2.0))
    else:
        fh = f
        fv = 2.0 * math.atan(math.tan(fh / 2.0) / aspect)
    return fh, fv


def globe_distance(R, fov_deg, aspect, margen, metodo='horzfov'):
    """(d_obj, d_min, theta): distancia al centro a la que una esfera de
    radio R cabe en el lado mas estrecho del cuadro, con y sin holgura."""
    fh, fv = fovs(fov_deg, aspect, metodo)
    th = min(fh, fv)
    sh = math.sin(th / 2.0)
    d_min = R / sh
    return d_min * max(1.0, margen), d_min, th


def distancia_encuadre(R, fov_deg, aspect, k, metodo='horzfov'):
    """(d, theta): distancia a la que una esfera de radio R ocupa la fraccion
    k del lado mas estrecho del cuadro (1 = de borde a borde), con theta el
    angulo de vision de ese lado."""
    fh, fv = fovs(fov_deg, aspect, metodo)
    th = min(fh, fv)
    a = math.atan(max(0.05, min(1.0, k)) * math.tan(th / 2.0))
    return R / math.sin(a), th


def fraccion_cuadro(r, d, th):
    """Fraccion del lado mas estrecho del cuadro que ocupa una esfera de
    radio r vista desde d (mas de 1: se sale)."""
    if d <= r:
        return float('inf')
    return math.tan(math.asin(r / d)) / math.tan(th / 2.0)


def smooth_damp(cur, vel, target, dt, t_suave):
    """Amortiguado critico: arranca y frena suave, sin rebote. Llega a ~98 %
    en t_suave segundos. Devuelve (posicion, velocidad)."""
    if t_suave <= 1e-6 or dt <= 0:
        return (target, 0.0) if t_suave <= 1e-6 else (cur, vel)
    w = 6.0 / t_suave
    x = w * dt
    e = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
    ch = cur - target
    tmp = (vel + w * ch) * dt
    vel = (vel - w * tmp) * e
    return target + (ch + tmp) * e, vel


def _cam_optics():
    """(fov en grados, metodo, aspecto) de la camara y el render reales."""
    fov, metodo = 45.0, 'horzfov'
    camfov = _p('Camfov', None)        # motor v92: el FOV lo gobierna el motor (la camara lo recibe de cam('fovcam'))
    try:
        cop = parent().op('camara')
        if camfov is None:              # proyecto sin Camfov (fase 10 v11 o anterior): el de la camara
            fov = float(cop.par.fov.eval())
        else:
            fov = float(camfov)
        try:
            metodo = str(cop.par.viewanglemethod.eval())
        except Exception:
            pass
        if 'focal' in metodo and camfov is None:
            fo = float(cop.par.focal.eval())
            ap = float(cop.par.aperture.eval())
            fov, metodo = math.degrees(2.0 * math.atan(ap / (2.0 * max(1e-3, fo)))), 'horzfov'
    except Exception:
        pass
    if 'focal' in metodo and camfov is not None:
        metodo = 'horzfov'
    if not 1.0 <= fov <= 179.0:            # camara sin FOV legible: el de TD por defecto
        fov = 45.0
    # El aspecto sale de los parametros de resolucion del render, nunca de
    # su imagen (r.width): leerla haria depender el render de la camara y la
    # camara del render, y TouchDesigner avisa de un bucle de cocinado.
    aspect = 16.0 / 9.0
    try:
        r = parent().op('render')
        w = float(r.par.resolutionw.eval())
        h = float(r.par.resolutionh.eval())
        if w > 0 and h > 0:
            aspect = w / h
    except Exception:
        pass
    return fov, metodo, aspect


def _slerp_dir(a, b, t):
    a, b = _norm(a), _norm(b)
    d = max(-1.0, min(1.0, a[0] * b[0] + a[1] * b[1] + a[2] * b[2]))
    om = math.acos(d)
    if om < 1e-6:
        return b
    so = math.sin(om)
    ka, kb = math.sin((1 - t) * om) / so, math.sin(t * om) / so
    return _norm((a[0] * ka + b[0] * kb, a[1] * ka + b[1] * kb, a[2] * ka + b[2] * kb))


# --- camara rasante (motor v92) ----------------------------------------------------
# Tercer modo (Modocamara = rasante): a ras de suelo y con gran angular. La
# camara va ANCLADA al planeta (gira, se balancea y se inclina con el): se
# calcula en coordenadas del planeta y se lleva al mundo con world_dir. Recorre
# el paralelo que separa dos anillos de celdas (Rasanillo) a Rasvel grados/s,
# a Rasaltura sobre el suelo real de las dos celdas que tiene a los lados, y
# mira hacia delante, Rasmirada grados sobre la horizontal. Su arriba es la
# vertical del sitio. El FOV (Rasfov) lo entrega el motor: cam('fovcam').

RAS_SUAVE = 1.5                    # segundos con los que la altura sigue al suelo
RAS_LEJOS = 5.0                    # distancia al punto al que mira
RAS_VECINAS = (-15.0, 15.0, 30.0)  # grados de longitud, detras y delante, cuyo suelo tambien cuenta
RAS_ALTURA, RAS_MIRADA, RAS_FOV = 0.6, 90.0, 140.0      # v94: tumbada, mirando al cenit (antes 0,35, 8 y 90)


def paralelo_rasante(k):
    """(latitud en grados, k valido) del limite entre los anillos k - 1 y k."""
    R = max(1, len(RINGS))
    band = 180.0 / (R + 0.5)
    k = max(1, min(max(1, R - 1), int(k)))
    return -90.0 + band * 0.25 + band * k, k


def suelo_rasante(W, cfg, lat, lon):
    """El suelo bajo la camara rasante: el mas alto de las dos celdas que tiene
    a los lados del paralelo, con el relieve de la naturaleza si lo hay."""
    a, b = celda_de_lonlat(lat - 1.0, lon), celda_de_lonlat(lat + 1.0, lon)
    g = max(suelo(W, cfg, a), suelo(W, cfg, b))
    for dl in RAS_VECINAS:              # v94: y las de delante y detras (sus paredes no tapan el cuadro)
        g = max(g, suelo(W, cfg, celda_de_lonlat(lat - 1.0, lon + dl)),
                suelo(W, cfg, celda_de_lonlat(lat + 1.0, lon + dl)))
    try:
        if cfg['nivel'] >= 11 and tema_de(cfg) == 'naturaleza':
            la, lo = math.radians(lat), math.radians(lon)
            d = (math.cos(la) * math.cos(lo), math.sin(la), math.cos(la) * math.sin(lo))
            g += max(0.0, alto_en(terreno(W, cfg), d))
    except Exception:
        pass
    return g, a, b


def pose_rasante(lat, lon, radio, mirada):
    """(posicion, delante, arriba) en coordenadas del PLANETA: sobre el paralelo
    'lat' en la longitud 'lon', a 'radio' del centro, mirando en el sentido de la
    marcha (longitud creciente) y 'mirada' grados sobre la horizontal."""
    la, lo, mi = math.radians(lat), math.radians(lon), math.radians(mirada)
    up = (math.cos(la) * math.cos(lo), math.sin(la), math.cos(la) * math.sin(lo))
    fw = (-math.sin(lo), 0.0, math.cos(lo))
    de = _norm(_add(_mul(fw, math.cos(mi)), up, math.sin(mi)))
    ar = _norm(_add(_mul(up, math.cos(mi)), fw, -math.sin(mi)))
    return _mul(up, radio), de, ar


def giro_camara(delante, arriba):
    """(rx, ry, rz) en grados, orden xyz (primero X: R = Rz Ry Rx, como las
    instancias), de una camara que mira a 'delante' con 'arriba' hacia arriba.
    La camara de TouchDesigner mira por su -Z y su arriba es +Y."""
    f = _norm(delante)
    r = _cross(f, arriba)
    n = math.sqrt(_dot(r, r))
    if n < 1e-9:                        # delante y arriba paralelos: cualquier lado vale
        r = _cross(f, (1.0, 0.0, 0.0) if abs(f[0]) < 0.9 else (0.0, 0.0, 1.0))
        n = math.sqrt(_dot(r, r))
    r = _mul(r, 1.0 / n)
    u = _cross(r, f)
    # columnas de R: derecha, arriba, -delante
    sb = max(-1.0, min(1.0, -r[2]))
    b = math.asin(sb)
    if abs(sb) < 1.0 - 1e-9:
        a = math.atan2(u[2], -f[2])
        c = math.atan2(r[1], r[0])
    else:                               # mirando por el eje Y de la camara: rz = 0
        a = math.atan2(u[0] * sb, u[1])
        c = 0.0
    return (math.degrees(a), math.degrees(b), math.degrees(c))


def ejes_de_giro(rx, ry, rz):
    """(derecha, arriba, delante) de una camara girada rx ry rz (orden xyz)."""
    a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
    sa, ca, sb, cb, sc, cc = math.sin(a), math.cos(a), math.sin(b), math.cos(b), math.sin(c), math.cos(c)
    der = (cc * cb, sc * cb, -sb)
    arr = (cc * sb * sa - sc * ca, sc * sb * sa + cc * ca, cb * sa)
    z = (cc * sb * ca + sc * sa, sc * sb * ca - cc * sa, cb * ca)
    return der, arr, (-z[0], -z[1], -z[2])


def _giro_planeta():
    """(giro, inclinacion, balanceo) del planeta en este fotograma, en grados."""
    try:
        return _ritmo().rotation(absTime.frame), float(parent().par.Tilt), wobble()
    except Exception:
        return 0.0, 0.0, 0.0


def _rasante(W, c, dt, activo):
    """La camara rasante de este fotograma, ya en el mundo: dict(pos, de, ar,
    lat, lon, suelo, alt, celdas)."""
    lat, k = paralelo_rasante(_p('Rasanillo', 4))
    lon = _CACHE.get('ras_lon', 0.0)
    if activo and not _p('Pausa', False):
        lon = (lon + max(0.0, _p('Rasvel', 0.5)) * dt) % 360.0
    _CACHE['ras_lon'] = lon
    g_obj, ca, cb = suelo_rasante(W, c, lat, lon)
    g = _CACHE.get('ras_g')
    if g is None or not activo:
        g, gv = g_obj, 0.0             # al entrar: sobre el suelo, sin transicion
    else:
        g, gv = smooth_damp(g, _CACHE.get('ras_gv', 0.0), g_obj, dt, RAS_SUAVE)
    alt = max(0.05, _p('Rasaltura', RAS_ALTURA))
    g = max(g, g_obj - 0.5 * alt)      # nunca bajo tierra, por brusco que sea el escalon
    _CACHE['ras_g'], _CACHE['ras_gv'] = g, gv
    pos, de, ar = pose_rasante(lat, lon, g + alt, max(-60.0, min(90.0, _p('Rasmirada', RAS_MIRADA))))
    ang, tilt, wob = _giro_planeta()
    return dict(pos=world_dir(pos, ang, tilt, wob), de=world_dir(de, ang, tilt, wob),
                ar=world_dir(ar, ang, tilt, wob), lat=lat, lon=lon, anillo=k, suelo=g, alt=alt,
                celdas=(ca, cb))


def camera_state():
    if _CACHE.get('cam_frame') == absTime.frame:
        return _CACHE['cam']
    W, c = world(), cfg_foto()
    R = top_radius(W, c)
    t = absTime.seconds
    last = _CACHE.get('cam_t')
    dt = 0.0 if last is None else max(0.0, min(0.25, t - last))
    _CACHE['cam_t'] = t
    # globo: el planeta ocupa Encuadre del cuadro; con una concha nueva la
    # camara se aleja en Camsuave s, y el planeta nunca se sale del cuadro
    Re = R + RETICULA_SOBRE
    fov, metodo, aspect = _cam_optics()
    k = max(0.3, min(1.0, _p('Encuadre', ENCUADRE)))
    suave = max(0.0, _p('Camsuave', 3.0))
    d_obj, th = distancia_encuadre(Re, fov, aspect, k, metodo)
    d_min = distancia_encuadre(Re, fov, aspect, 1.0, metodo)[0]
    d = _CACHE.get('cam_d')
    if d is None or R < _CACHE.get('cam_R', R) - 1e-6:
        d, v = d_obj, 0.0              # arranque, Resetmundo, rango o mundo cargado: sin transicion
    else:
        d, v = smooth_damp(d, _CACHE.get('cam_v', 0.0), d_obj, dt, suave)
    salto = 0.0
    if d < d_min:
        salto = d_min - d
        d, v = d_min, max(0.0, v)
    _CACHE.update(cam_d=d, cam_v=v, cam_R=R)
    # modo: peso de la camara de superficie (0 globo, 1 superficie)
    sup = c['nivel'] >= 10 and str(_p('Modocamara', 'globo')) == 'superficie'
    wq = _CACHE.get('cam_w')
    if wq is None:
        wq = 1.0 if sup else 0.0
    wq = max(0.0, min(1.0, wq + (1.0 if sup else -1.0) * dt / CAM_TRANS))
    _CACHE['cam_w'] = wq
    s = wq * wq * (3 - 2 * wq)
    g_pos = _mul(CAM_DIR, d)
    if s > 0.0:
        h = _p('Camaltura', 4.0)
        vel = _p('Camvel', 0.6)
        az = math.radians(vel * t)
        el = math.radians(12.0 + 8.0 * math.sin(t * 0.05))

        def sph(a, e, r):
            return (r * math.cos(e) * math.cos(a), r * math.sin(e), r * math.cos(e) * math.sin(a))
        s_pos = sph(az, el, R + h)
        s_tgt = sph(az + math.radians(25.0), el - math.radians(6.0), R)
        rad = (R + h) * s + d * (1 - s)
        pos = _mul(_slerp_dir(CAM_DIR, s_pos, s), rad)
        tgt = _mul(s_tgt, s)
    else:
        pos, tgt = g_pos, (0.0, 0.0, 0.0)
    # orientacion (motor v92): la da el motor (cam('rot')), no el Look At de la
    # camara. Globo y superficie miran a su objetivo con el +Y del mundo arriba
    de = _norm((tgt[0] - pos[0], tgt[1] - pos[1], tgt[2] - pos[2]))
    ar = (0.0, 1.0, 0.0)
    fovcam = fov
    # modo rasante: peso wr (0 nada, 1 a ras de suelo), con la misma transicion
    ras = c['nivel'] >= 10 and str(_p('Modocamara', 'globo')) == 'rasante'
    wr = _CACHE.get('cam_wr')
    if wr is None:
        wr = 1.0 if ras else 0.0
    wr = max(0.0, min(1.0, wr + (1.0 if ras else -1.0) * dt / CAM_TRANS))
    _CACHE['cam_wr'] = wr
    sr = wr * wr * (3 - 2 * wr)
    rs = None
    if sr > 0.0:
        rs = _rasante(W, c, dt, ras)
        r0 = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
        r1 = math.sqrt(_dot(rs['pos'], rs['pos']))
        pos = _mul(_slerp_dir(pos, rs['pos'], sr), r0 + (r1 - r0) * sr)
        de = _norm(_add(_mul(de, 1.0 - sr), rs['de'], sr)) if sr < 1.0 else rs['de']
        ar = _norm(_add(_mul(ar, 1.0 - sr), rs['ar'], sr)) if sr < 1.0 else rs['ar']
        tgt = _add(pos, de, RAS_LEJOS)
        fovcam = fov + (max(20.0, min(160.0, _p('Rasfov', RAS_FOV))) - fov) * sr
    else:
        _CACHE.pop('ras_g', None)
    rot = giro_camara(de, ar)
    dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
    near = max(0.05, min(5.0, 0.25 * (dist - Re)))
    if rs is not None:                  # a ras de suelo: el plano cercano, por debajo de la altura de ojos
        near = max(0.02, min(near + (0.15 * rs['alt'] - near) * sr, 5.0))
    far = dist + 2.0 * Re + 10.0
    st = dict(pos=pos, tgt=tgt, R=R, Re=Re, d=d, d_obj=d_obj, d_min=d_min, theta=th,
              fov=fov, metodo=metodo, aspect=aspect, encuadre=k, w=s, near=near, far=far,
              salto=salto, modo='rasante' if sr >= 0.5 else ('superficie' if s >= 0.5 else 'globo'),
              rot=rot, de=de, ar=ar, fovcam=fovcam, wr=sr, ras=rs)
    _CACHE['cam'] = st
    _CACHE['cam_frame'] = absTime.frame
    return st


def cam(key, k=0, frame=None):
    v = camera_state()[key]
    return v[k] if isinstance(v, (tuple, list)) else v


def cam_reset():
    """La proxima lectura de la camara salta al encuadre (sin transicion)."""
    for k in ('cam_d', 'cam_v', 'cam_R', 'cam_frame', 'ras_g', 'ras_gv'):
        _CACHE.pop(k, None)


# --- leyenda -----------------------------------------------------------------

def _num_es(x, d=2):
    return ('%%.%df' % d % x).replace('.', ',')


def _miles_es(n):
    return ('%.1fk' % (n / 1000.0)).replace('.', ',') if n >= 1000 else str(int(n))


def _legend_industria(W, c, r):
    """Las lineas INDUSTRIA, CORTA e INTEGRADA de la leyenda (fase 11 v11)."""
    rec = r.get('recursos', {})
    partes = ' · '.join('%s %d' % (k.replace('carbon', 'carbón'), rec[k]) for k in RECURSOS if rec.get(k))
    out = ['  INDUSTRIA  época %s   recursos %s   plantas %d   humo %s/%s'
           % (r.get('epoca', 'vapor').replace('quimica', 'química'), partes or '-', r.get('plantas', 0),
              _miles_es(r.get('humo', 0)), _miles_es(int(c.get('max_humo', 6000))))]
    for i_, (b, mx, testigo) in sorted(r.get('cortas', {}).items())[:2]:
        out.append('  CORTA    celda %d   bancos %d/%d   testigo %s' % (i_, b, mx, 'sí' if testigo else 'no'))
    for k_, (nv, mx) in sorted(r.get('integradas', {}).items(), key=lambda kv: str(kv[0]))[:2]:
        out.append('  INTEGRADA  %s   niveles %d/%d'
                   % ('cluster %s' % k_ if not str(k_).startswith('c') else 'celda %s' % str(k_)[1:], nv, mx))
    return out


def _legend_ciudad(W, c, r):
    """Las lineas CIUDAD, OBRA, COLONIA y MARCO de la leyenda (fase 11 v10); en la
    industria, INDUSTRIA, OBRA, CORTA e INTEGRADA (fase 11 v11)."""
    if r.get('tema') == 'industria':
        out = _legend_industria(W, c, r)
        ob = r.get('obra', {})
        if ob or r.get('gruas'):
            partes = ' · '.join('%s %d' % (k, ob[k]) for k in PASOS_OBRA if ob.get(k))
            out.insert(1, '  OBRA     %d (%s)   gruas %d' % (sum(ob.values()), partes or '-', r.get('gruas', 0)))
        return out
    lg = r.get('lenguajes', [0, 0, 0])
    out = ['  CIUDAD   lenguajes F/T/C %d/%d/%d   edificios %d   tipos %d   MUTACION %s (%s)'
           % (lg[0], lg[1], lg[2], r.get('edificios', 0), r.get('tipos', 0), _num_es(r.get('mutacion', 0.0)),
              'saturacion' if r.get('fuente') == 'saturacion' else 'manual')]
    ob = r.get('obra', {})
    if ob or r.get('gruas'):
        partes = ' · '.join('%s %d' % (k, ob[k]) for k in PASOS_OBRA if ob.get(k))
        out.append('  OBRA     %d (%s)   gruas %d' % (sum(ob.values()), partes or '-', r.get('gruas', 0)))
    for i_, (nv, mx) in sorted(r.get('colonias', {}).items())[:2]:
        out.append('  COLONIA  celda %d   parasitos %d/%d' % (i_, nv, mx))
    for k_, (nv, mx, caps) in sorted(r.get('marcos', {}).items(), key=lambda kv: str(kv[0]))[:2]:
        out.append('  MARCO    %s   niveles %d/%d   capsulas %d'
                   % ('cluster %s' % k_ if not str(k_).startswith('c') else 'celda %s' % str(k_)[1:], nv, mx,
                      caps))
    return out


def _coma(x, d=1):
    return ('%%.%df' % d % x).replace('.', ',')


def _legend_piel(c):
    """Motor v101: la linea PIEL de la leyenda: el turno de la vuelta, las celdas
    calculadas en el, las del camino inmediato, cada cuanto se publica, lo que
    tarda build_instances en Python y la arqueologia (de la cache o calculada)."""
    inf = _TURNOS.get('info') or {}
    if not c.get('cache_arq', 1):
        arq = 'arq sin cache'
    else:
        arq = 'arq cache' if _ARQ.get('cache') else 'arq calcula'
    py = 'python %s ms' % _coma(_TURNOS.get('ms_inst', 0.0))
    modo = inf.get('modo', 'entera')
    if modo == 'entera':
        return '  PIEL     entera en cada fotograma (Refrescopiel 0)   %s   %s' % (py, arq)
    publica = 'publica %s s' % _coma(inf.get('refresco', 0.0), 2)
    if modo == 'vuelta':
        return '  PIEL     vuelta entera (Turnos apagado)   inmediatas %d   %s%s   %s   %s' \
            % (inf.get('inmediatas', 0), publica, ' (ahora)' if inf.get('publica') else '', py, arq)
    return '  PIEL     turno %d/%d   celdas %d   inmediatas %d   %s%s   %s   %s' \
        % (inf.get('turno', 0), inf.get('turnos', 0), inf.get('celdas', 0), inf.get('inmediatas', 0), publica,
           ' (ahora)' if inf.get('publica') else '', py, arq)


def legend(frame=None):
    try:
        return _legend()
    except Exception as e:
        return '\n  MOTOR    fallo en la leyenda: %s' % e


def _legend_nota(W, c, now):
    last = W['last'].get(1)
    if not last:
        try:
            note = int(parent().par.Nota)
        except Exception:
            note = 60
        env = 0.0
    else:
        note = int(last['note'])
        env = math.exp(-max(0.0, now - W['hit_t'].get(1, -99.0)) / SEQ_DECAY)
    i = note_cell(note)
    if i is None:
        donde = 'fuera de rango (ignorada)'
    else:
        f = fold_note(note)
        donde = 'celda %2d de %d   %s' % (i, N, cell_label(i))
        if f != note:
            donde += '   (como %s %d)' % (note_name(f), f)
    k = int(round(max(0.0, min(1.0, env)) * 12))
    return ['  NOTA     %-5s %3d    %s' % (note_name(note), note, donde),
            '  PULSO    [%s]' % ('#' * k + '.' * (12 - k)),
            '  SEQ1     canal %d    notas recibidas: %d' % (_p('Canal', 13), W['hits'].get(1, 0))]


def _legend():
    W, c = world(), cfg()
    lvl = c['nivel']
    lines = [''] + _legend_nota(W, c, absTime.seconds)
    occ = occupied(W)
    mx = max(W['occ'])
    lines.append('  MUNDO    ocupadas %d/%d (%d%%)   max %d   fase %d'
                 % (occ, N, int(occ * 100 / N), mx, lvl))
    lines.append('  RANGO    %s %d (polo sur) a %s %d (polo norte)   %d celdas   fuera: %s'
                 % (note_name(GRID['lo']), GRID['lo'], note_name(GRID['hi']), GRID['hi'],
                    N, FUERA_MODES[GRID['mode']]))
    u = W['ev'].get('ultima')
    if u:
        ctxt = '   carga %d/%d' % (u['carga'], u['coste']) if 'coste' in u else ''
        lines.append('  ULTIMA   %s celda %d   ocupacion %d   %s%s'
                     % (SPECIES_NAME.get(u['s'], '?'), u['celda'], u['occ'], u['estado'], ctxt))
    if lvl >= 4:
        sats = sum(1 for i in range(N) if W['par'][i] >= 0 and W['occ'][i] > 0)
        fus = sum(1 for i in range(N) if W['par'][i] < 0 and W['occ'][i] >= c['th_fusion'])
        cor = sum(1 for i in range(N) if W['par'][i] < 0 and W['occ'][i] >= c['th_crown'])
        cum = sum(1 for i in range(N) if W['par'][i] < 0 and W['occ'][i] >= c['th_cumbre'])
        d = W['ev'].get('desborde')
        dtxt = '%d -> %d' % (d['de'], d['a']) if d else '-'
        lines.append('  DESBORDE %-9s satelites %d   fusiones %d   coronas %d   cumbres %d'
                     % (dtxt, sats, fus, cor, cum))
    if lvl >= 5:
        hib = sum(1 for i in range(N) if W['sp'][i] == HIB)
        lines.append('  SEQ2     canal %d   notas %d   hibridas %d'
                     % (_p('Canal2', 14), W['hits'].get(2, 0), hib))
    if lvl >= 6:
        cmin, cmax = cycle_bounds(c)
        pos = 'compas %d (%d-%d)' % (W['compases_ciclo'], cmin, cmax) if W.get('marcha') \
            else 'parado'
        giro = '   giro x%.2f' % W['giro_factor'] if c['giro_vivo'] else ''
        espera = '   esperando territorio' if W.get('esperando') and W.get('marcha') else ''
        lines.append('  CICLO    %d   %s   madurez %d%%   novedad %d%%   quieto %d/%d   '
                     'territorio %d%% (%d%%)%s%s'
                     % (W['ciclo_n'], pos, int(round(W['madurez'] * 100)),
                        int(round(W['novedad'] * 100)), W['quietos'],
                        int(c['compases_quietos']), int(round(W.get('territorio', 0.0) * 100)),
                        int(round(c['umbral_territorio'] * 100)), giro, espera))
        if W['cambio_pendiente']:
            lines.append('           cambio de pattern: se enterrara al llegar a %d compases' % cmin)
        if W.get('aviso'):
            lines.append('  AVISO    %s' % W['aviso'])
    if lvl >= 7:
        e = W['ev'].get('erosion')
        dens = occupied(W) / float(N)
        flag = '  x%g' % c['rad_mult'] if dens > c['dens_umbral'] else ''
        if e and e.get('modo') == 'impulso':     # fase 7: en lugar de la linea EROSION
            lines.append('  IMPULSO  pad %d +%d celda %d ocupacion %s->%s%s'
                         % (e['pad'] + 1, e.get('pulsos', 0), e['celda'], e.get('occ0', '-'), e.get('occ', '-'),
                            '   desbordes %d' % len(e['desbordes']) if e.get('desbordes') else ''))
        elif e:
            acc = e.get('accidente') if lvl >= 14 else None
            lines.append('  EROSION  pad %d   %s   -%.1f notas   radio %d   celda %d   densidad %d%%%s%s'
                         % (e['pad'] + 1, e.get('tipo', '-'), e.get('notas', e['red']), e['rad'],
                            e['celda'], int(dens * 100), flag,
                            '   · %s celda %d' % (acc['tipo'], acc['celda']) if acc else ''))
        else:
            lines.append('  EROSION  -   densidad %d%%%s' % (int(dens * 100), flag))
    if lvl >= 8:
        ult = '%.2f' % shell_th(W['shells'][-1], c) if W['shells'] else '-'
        lg, lc = max_laguna(W, c)
        lag = '%.2f (celda %d)' % (lg, lc) if lc >= 0 else '0.00'
        cz = c.get('corteza_max', 0.0)
        comp = ('   corteza %.2f de %g (x%.2f)' % (top_radius(W, c) - c['core_radius'], cz,
                                                  W.get('compacta', 1.0)) if cz > 0 else '')
        lines.append('  CONCHAS  %d   radio %.2f   ultima %s%s   laguna max %s   colmatacion %d%%'
                     '   herencia %d%%   continentes %d'
                     % (n_shells(W), top_radius(W, c), ult, comp, lag, int(round(c['colmatacion'] * 100)),
                        int(c['herencia'] * 100), continents(W)))
    if lvl >= 8:
        try:
            cs = camera_state()
            lado = 'vertical' if cs['theta'] <= fovs(cs['fov'], cs['aspect'], cs['metodo'])[0] - 1e-9 \
                else 'horizontal'
            inst = _CACHE.get('inst')
            vis = radio_visible(inst, W, c) if inst else cs['Re']
            alto = fraccion_cuadro(cs['Re'], cs['d'], cs['theta'])
            alto_vis = fraccion_cuadro(vis, cs['d'], cs['theta'])
            lines.append('  CAMARA   %s   dist %.1f -> %.1f   el planeta ocupa el %d%% del %s (Encuadre %.2f)'
                         '   lo mas alto llega al %s   fov %.0f (%s)'
                         % (cs['modo'], cs['d'], cs['d_obj'], int(round(alto * 100)),
                            'alto' if lado == 'vertical' else 'ancho', cs['encuadre'],
                            '%d%%' % int(round(alto_vis * 100)) if alto_vis < 9.99 else 'borde',
                            cs['fov'], 'vertical' if 'vert' in cs['metodo'] else 'horizontal'))
            rs = cs.get('ras')
            if rs:                      # motor v92: a ras de suelo
                lines.append('  RASANTE  anillos %d-%d (lat %.0f)   lon %.0f   suelo %.2f   ojos a %.2f   '
                             'fov %.0f   entre las celdas %d y %d   %d%%'
                             % (rs['anillo'] - 1, rs['anillo'], rs['lat'], rs['lon'], rs['suelo'], rs['alt'],
                                cs['fovcam'], rs['celdas'][0], rs['celdas'][1], int(round(cs['wr'] * 100)))
                             + ('   ojo de pez 180' if _CACHE.get('render_modo') == RENDER_OJO else ''))
        except Exception:
            pass
    if lvl >= 9:
        k = W['ev'].get('corte')
        if k:
            left = max(0.0, c['scar_time'] - (absTime.seconds - k['t']))
            lines.append('  CORTE    celda %d   %d losetas   suelo %.2f   laguna %.2f   cicatriz %.1f s'
                         % (k['celda'], k['conchas'], k.get('suelo', 0.0), k.get('laguna', 0.0), left))
            if lvl >= 16:
                lines.append(_legend_arqueo(W, c, k))
            if k.get('nucleo') is not None:
                lines.append('  CORTE    celda %d   nucleo alcanzado' % k['nucleo'])
    if lvl >= 11:
        pz = W.get('piel') or {}
        lines.append('  TEMA     %s   clusters %d (max %d)   compuestos %d   piezas %d   obras %d (%d a medias)'
                     % (tema_de(c), pz.get('clusters', 0), pz.get('max', 0), pz.get('compuestos', 0),
                        pz.get('piezas', 0), pz.get('obras', 0), pz.get('medias', 0)))
        lines.append(_legend_piel(c))           # motor v101: la piel por turnos
        if pz.get('ciudad'):                    # fase 11 v10: la ciudad legible
            lines += _legend_ciudad(W, c, pz['ciudad'])
        if 'copas' in pz:                       # fase 11 v5: la naturaleza legible
            b = pz.get('biomas', {})            # fase 11 v8: la biblioteca de ejemplares
            lines.append('  NATURALEZA  biomas F/T/C %d/%d/%d   ejemplares %d   %s hojas %s/%s'
                         % (b.get('frio', 0), b.get('templado', 0), b.get('calido', 0), pz.get('ejemplares', 0),
                            RUTA_HOJAS, _miles(pz.get('hojas', 0)), _miles(presupuesto_hojas(c))))
            if pz.get('islas') or pz.get('volcanes'):       # motor v97
                lines.append('  MAR      islas %d   archipielagos %d   volcanes %d (en erupcion %d)'
                             % (pz.get('islas', 0), pz.get('archipielagos', 0), pz.get('volcanes', 0),
                                pz.get('erupciones', 0)))
            lines.append('  NATURA   montes %d   cordilleras %d   cumbres nevadas %d   emergentes %d   detalle %s'
                         % (pz['montes'], pz['cordilleras'], pz['nevadas'], pz.get('emergentes', 0),
                            'cerca (%d celdas)' % pz['cerca'] if pz['cerca'] else 'globo (impostores)'
                            if c.get('impostores', 1) else 'globo'))
            hb = pz.get('hibridos', {})
            for i_, nb in sorted(hb.get('arrozales', {}).items())[:2]:
                lines.append('  ARROZAL  celda %d   bancales %d/%d   inundados %d'
                             % (i_, nb, int(c['max_terrazas']), pz.get('inundados', {}).get(i_, 0)))
            mes = hb.get('mesetas', {})
            if mes:
                cl_ = clusters(W, c)
                grupos = {}
                for i_, nv in mes.items():
                    grupos.setdefault(cl_['de'][i_], []).append(i_)
                for k_, cs in sorted(grupos.items())[:2]:
                    lines.append('  MESETA   cluster %s   niveles %d/%d   frutales %d   parcelas %d'
                                 % (k_ if k_ >= 0 else '-', max(mes[x] for x in cs), int(c['max_niveles']),
                                    sum(pz.get('frutales', {}).get(x, 0) for x in cs),
                                    sum(pz.get('parcelas', {}).get(x, 0) for x in cs)))
    if lvl >= 12:
        md = W['ev'].get('mod')
        modo = MATERIALES[int(c['material_modo'])] + ('   RESPALDO (Phong)' if c['respaldo'] else '')
        if md:
            gate = '   gate %.2f -> %s' % (md['gate'], md['efecto']) if md.get('gate') is not None else ''
            lines.append('  MOD      vel %d -> rugosidad %.2f%s   %s'
                         % (md['vel'], md['rug'], gate, modo))
        else:
            lines.append('  MOD      -   %s' % modo)
    if lvl >= 13:
        tj = W.get('tejido') or {}
        if tema_de(c) == 'industria':           # fase 13 v7: vias y red
            lines.append('  TEJIDO   vías %d (%d tramos, %d playa%s)   red %d centrales %d tramos   apagadas %d'
                         % (tj.get('lineas', 0), tj.get('tramos_via', 0), tj.get('playas', 0),
                            '' if tj.get('playas', 0) == 1 else 's', tj.get('centrales', 0), tj.get('tramos_red', 0),
                            tj.get('apagadas', 0)))
        else:
            lines.append('  TEJIDO   rios %d (%d tramos, %d lagos)   carreteras %d tramos'
                         % (tj.get('rios', 0), tj.get('tramos_rio', 0), (W.get('rios_res') or {}).get('lagos', 0),
                            tj.get('tramos_via', 0)))
        if tema_de(c) == 'naturaleza':          # fase 13 v3: el diagnostico de los rios
            rr = W.get('rios_res') or {}
            lines.append('  RIOS     tramos %d   fuentes %d   lagos %d   caudal max %d   ancho %.1f px'
                         % (rr.get('tramos', 0), rr.get('fuentes', 0), rr.get('lagos', 0), rr.get('caudal', 0),
                            rr.get('px', 0.0)))
    if lvl >= 14:
        lines.append(_legend_escalada(W, c))
    if lvl >= 15:
        lines.append(_legend_era(W, c))
    if lvl >= 17:
        lines.append(_legend_tiempo(W, c))
    if lvl >= 18:
        lines.append(_legend_escena(W, c))
    if lvl >= 19:
        lines.append(_legend_modular(W, c))
    if lvl >= 21:
        lines.append(_legend_micro(W, c))
    if lvl >= 22:
        lines.append(_legend_camara(W, c))
    if lvl >= 23:
        lines.append(_legend_sala(W, c))
    if lvl >= 24:
        lines.append(_legend_personas(W, c))
    if lvl >= 25:
        lines.append(_legend_huella(W, c))
    if lvl >= 26:
        lines.append(_legend_borrado(W, c))
    if lvl >= 27:
        lines.append(_legend_banda(W, c))
    if lvl >= 28:
        lines.append(_legend_noche(W, c))
    if lvl >= 29:
        lines.append(_legend_fila(W, c))
    if lvl >= 30:
        lines.append(_legend_relampago(W, c))
    if lvl >= 31:
        lines.append(_legend_historico(W, c))
    return '\n'.join(lines)


def _legend_arqueo(W, c, k):
    """CORTE (fase 16): las eras que ensena el corte del ultimo golpe, las
    piezas expuestas y la union de cortes."""
    zona = [x for x, _ in rings(k['celda'], int(k.get('radio', 1)) + 1)] if 0 <= k['celda'] < N else []
    eras = eras_expuestas(W, c, zona)
    az = W.get('arqueo') or {}
    txt = '  CORTE    celda %d   %d era%s expuesta%s%s   piezas %d en %d celdas' % (
        k['celda'], len(eras), '' if len(eras) == 1 else 's', '' if len(eras) == 1 else 's',
        ': ' + ', '.join(nm for _, nm in eras) if eras else '', az.get('piezas', 0), az.get('celdas', 0))
    u = k.get('union')
    if u:
        txt += '   + %s %s (%d celdas)' % (UNION_NOMBRE[u['tipo']], '-'.join(str(x) for x in u['celdas']),
                                         len(u['celdas']))
    return txt


def leer_modular(c, now):
    """{senal: 0-1} de la fuente elegida (Fuentemodular), o None si no llega
    nada (sin CHOP o sin canales)."""
    fuente = FUENTES_MODULAR[int(c['fuente_modular']) % len(FUENTES_MODULAR)]
    if fuente == 'manual':
        return dict((k, max(0.0, min(1.0, _p(k.capitalize(), 0.0)))) for k in MODULAR)
    if fuente == 'prueba':
        return generador_prueba(now)
    try:
        if fuente == 'osc':
            ch = parent().op('modular_osc')
        else:
            ruta = str(_p('Chopmodular', '') or '')
            ch = (parent().op(ruta) or op(ruta)) if ruta else None
    except Exception:
        ch = None
    if ch is None or not getattr(ch, 'numChans', 0):
        return None
    chans = list(ch.chans)
    nombres = [x.name for x in chans]
    out = {}
    for k, senal in enumerate(MODULAR):
        j = canal_de(nombres, senal, k)
        if j is None:
            continue
        x = chans[j]
        v = x.eval() if hasattr(x, 'eval') else (x[len(x) - 1] if len(x) else 0.0)
        out[senal] = normalizar(v, c['rango_modular'])
    return out or None


def modular_uniforme(nombre, k, frame=None):
    """Componente k de los uniformes de la fase 19 del shader de la piel:
    uNiebla (cantidad, cerca, lejos), uNieblaCol y uGlitch (cantidad, tiempo)."""
    try:
        md = _CACHE.get('modular')
        if md is None:
            return 0.0 if nombre != 'nieblacol' else NIEBLA_COL[int(k)] if int(k) < 3 else 0.0
        c = cfg_foto()
        if nombre == 'niebla':
            cs = camera_state()
            v = niebla(world(), c, cs['d'], cs['R'])
            return v[int(k)] if int(k) < 3 else 0.0
        if nombre == 'nieblacol':
            return NIEBLA_COL[int(k)] if int(k) < 3 else 0.0
        if nombre == 'glitch':
            return (md['saturacion'] * c['glitch'], absTime.seconds, 0.0, 0.0)[int(k)]
    except Exception:
        pass
    return 0.0


def niebla_camara(cosa, frame=None):
    """La niebla lineal de la camara (para los materiales Phong y constantes):
    'cerca' y 'lejos'."""
    try:
        cs = camera_state()
        e, cerca, lejos = niebla(world(), cfg_foto(), cs['d'], cs['R'])
        if e <= 0.01:                   # sin espacialidad, la niebla empieza lejisimos
            return 1.0e5 if cosa == 'cerca' else 2.0e5
        # la niebla lineal de la camara es total en 'lejos': se estira para que
        # lo mas denso sea la cantidad (e), como en el shader de la piel
        return cerca if cosa == 'cerca' else cerca + (lejos - cerca) / e
    except Exception:
        return 1.0e5 if cosa == 'cerca' else 2.0e5


def _legend_modular(W, c):
    """MODULAR (fase 19): la fuente y las cuatro senales."""
    md = W['modular']
    fuente = FUENTES_MODULAR[int(c['fuente_modular']) % len(FUENTES_MODULAR)]
    if fuente == 'osc':
        fuente = 'osc :%d' % int(_p('Puertoosc', 9000))
    hace = absTime.seconds - md['t'] if md['t'] > -90 else None
    return ('  MODULAR  %s   lfo %.2f   ruido %.2f   espacio %.2f   saturacion %.2f   %s'
            % (fuente, md['lfo'], md['ruido'], md['espacio'], md['saturacion'],
               'sin senal' if hace is None or hace > 2.0 else 'hace %.1f s' % hace))


def _legend_escena(W, c):
    """ESCENA (fase 18): la escena, la densidad, las piezas y la luz local."""
    inst = _CACHE.get('inst') or {}
    piezas = sum(len(v) for k, v in inst.items() if k.startswith('mod_'))
    dens = occupied(W) / float(N)
    return ('  ESCENA   %s   densidad %d%%%s   piezas %d   luz local %d   transitos a medias %d%s'
            % (ESCENAS[c.get('escena', 0)], int(round(dens * 100)), ' (>60%)' if dens > 0.6 else '', piezas,
               len(inst.get('luz_local', [])), len(transitos_colgados(W, c)),
               '   diagnostico' if c.get('diagnostico') else ''))


def _legend_tiempo(W, c):
    """TIEMPO (fase 17): tempo, el beat del compas, el pattern, el frente y
    si el pulso esta parado."""
    p = W['pulso']
    bpb = _bpb(c)
    beat = p['beat']
    txt = '  TIEMPO   %d bpm   beat %d/%d' % (int(round(tempo())), int(math.floor(beat)) % bpb + 1, bpb)
    f = W['frente']
    q = progreso_frente(W, c)
    pat = f['pattern'] if f and f.get('pattern') else W.get('pattern')
    con = f.get('conocido') if f and f.get('pattern') else W.get('pattern_conocido')
    if f and q is not None:
        pasos = max(1, int(c['pasos_frente']))
        txt += '   frente %d/%d' % (min(pasos, int(q * pasos)), pasos)
    if pat:
        txt += '   pattern %s%s' % (pat, '' if con is None else ' (conocido)' if con else ' (nuevo)')
    txt += '   biblioteca %d' % len(W['patrones'])
    if c.get('master_beat') is not None:
        txt += '   master_beat'
    if p.get('parado'):
        txt += '   PARADO'
    return txt


def ventanas_luz(frame=None):
    """uVentanas.x del shader de la piel: las ventanas de la ciudad se ven
    desde la fase 17 (antes, apagadas)."""
    try:
        v = _CACHE.get('ventanas')
        if v is None:
            v = ventanas_luz_de(world(), cfg())
        return v
    except Exception:
        return 0.0


def ventanas_luz_de(W, c):
    """Las ventanas se ven desde la fase 17; desde la 19, en la ciudad,
    respiran con el LFO del modular (Respiracion)."""
    if c['nivel'] < 17:
        return 0.0
    if c['nivel'] >= 19 and tema_de(c) in CONSTRUIDOS and W['modular'].get('activo'):
        return 1.0 - c['respiracion'] * (1.0 - W['modular']['lfo'])
    return 1.0


def luz_tiempo(k, frame=None):
    """Componente k del color de luz_principal: la luz cenital fria de la
    fase 10 tenida por la estacion del pattern (fase 17)."""
    try:
        t = _CACHE.get('tinte')
        cal = _CACHE.get('luz_calida', 0.0)       # fase 18: la escena calienta la luz
        if t is None:
            W, c = world(), cfg_foto()
            t = tinte_actual(W, c) if c['nivel'] >= 17 else [1.0, 1.0, 1.0]
            cal = c.get('luz_calida', 0.0) if c['nivel'] >= 18 else 0.0
        k = int(k)
        return (LUZ_BASE[k] + (LUZ_CALIDA[k] - LUZ_BASE[k]) * cal) * t[k] * dia()     # fase 28: la noche
    except Exception:
        return LUZ_BASE[int(k) % 3]


def _legend_era(W, c):
    """ERA: el ciclo, su tema y la materia en la que se enterrara; la
    herencia, las semillas que esperan y las trazas que se reutilizan."""
    tema = tema_de(c)
    pend = c.get('tema_pendiente')
    pend = '   (%s en el proximo ciclo)' % TEMAS[int(pend) % len(TEMAS)] if pend is not None else ''
    trazas = set((min(a, b), max(a, b)) for a, b in W.get('trazas') or [])
    usadas = sum(1 for a, b in (W.get('tejido_vias') or []) if (min(a, b), max(a, b)) in trazas)
    return ('  ERA      %d   %s -> %s   herencia %d%%   semillas %d   trazas %d de %d%s'
            % (W.get('ciclo_n', 1), tema, MATERIA_TEMA[tema], int(c['herencia'] * 100),
               sum(1 for x in W['rebrote'] if x == 1), usadas, len(trazas), pend))


def _legend_escalada(W, c):
    """ESCALADA: las catastrofes en curso, los golpes de la zona del ultimo
    aranazo y las huellas."""
    pasos = max(1, int(c['pasos_fuego']))
    partes = []
    for cat in W['cats']:
        q = max(cat['activas'].values()) if cat['activas'] else 0
        n = len(cat['activas'])
        partes.append('%s %d celda%s paso %d/%d%s' % (cat['tipo'].upper(), n, '' if n == 1 else 's',
                                                    min(pasos, q + 1), pasos, ' (grande)' if cat['grande'] else ''))
    ev = W['ev'].get('catastrofe') or {}
    t = W['t'] or 0.0
    if ev.get('tipo') == 'implosion' and t - ev.get('t', -99.0) < c['pasos_polvo'] * (W.get('paso') or 0.125):
        partes.append('IMPLOSION celda %d' % ev['celda'])
    d = W['ev'].get('destructor') or {}
    zona = set(vecindad(d['celda'])) if d.get('celda') is not None and 0 <= d['celda'] < N else set()
    g = sum(1 for x in W['golpes'] if x[1] in zona)
    return ('  ESCALADA %s   golpes %d/%d en la zona   huellas %d'
            % (' · '.join(partes) or '-', g, int(c['golpes_escalada']), sum(1 for x in W['ruina'] if x)))
