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
#                 arrozal en terrazas y meseta-jardin).
#                 No toca TouchDesigner.
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

MOTOR_VERSION = 'motor v52'

import math

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

DEFAULT_CFG = dict(
    nivel=3,
    core_radius=6.0,
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
    paleta=0, paleta_tono=20.0, paleta_croma=0.09,     # 0 generaciones, 1 mineral
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
    biomas=1, variantes=4, var_angulo=12.0, cuantizar30=0, inclinacion=8.0, densidad_hoja=6,
    traslucidez=0.35, timidez=0.12, emergentes=0.1, orla=1, mezcla=0.3, impostores=1,
    terrazas_por_nota=1, max_terrazas=8, paso_terraza=0.12, muro_terraza=0.25, riego=1,
    color_cultivo=(0.66, 0.80, 0.22), altura_meseta=0.15, max_niveles=3, marco=1, setos=1,
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
    """Fase 3: el gate decide cuanto sube la nota (Gatemode)."""
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
    W.setdefault('terr', {})[i] = W.get('bar_n', 0)
    W['ruina'][i] = 0                   # fase 14: construir sobre la huella la borra
    W['rebrote'][i] = 0                 # fase 15: una nota completa el rebrote
    if cfg['nivel'] >= 12:              # fase 12: la velocidad da el material
        W['ev']['mod'] = dict(s=s, celda=i, vel=int(vel), rug=rugosidad(cfg, vel), gate=None, efecto='')
    res = grow(W, cfg, i, s, vel, now)
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
    (Umbralcorona). Una celda coronada sigue sumando ocupacion, y la cumbre
    sigue alargando la corona, pero el mundo ya se da por hecho. Un
    satelite deja de cambiar antes, al llegar a Limsatelite."""
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
    apagar_destructores(W)              # fase 14: el fin de ciclo lo cierra de golpe
    if end_cycle(W, cfg, now, bars):
        ev['grosor'] = shell_th(W['shells'][-1], cfg)
        W['foto_anterior'] = snapshot(W, cfg)
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
    """Notas que deshace un golpe en su celda. Con Erosionvel, la reduccion
    de la tabla vale a la velocidad Velref (100) y escala en proporcion
    (x1,27 a 127). Minimo: una nota (o la reduccion, si es menor), para que
    un golpe flojo siempre deje huella. Sin Erosionvel, la de la tabla."""
    red = float(red)
    if not cfg.get('erosion_vel', 0) or red <= 0:
        return red
    f = max(0.0, float(vel)) / max(1.0, float(cfg.get('vel_ref', 100)))
    return max(min(red, 1.0), red * f)


def erosion(W, cfg, pad, vel, now):
    """Un golpe de bateria. Un pad en modo impulso (fase 7 v12) no erosiona:
    lo atiende impulso()."""
    perf = cfg['perfiles']
    pad = int(pad) % len(perf)
    if es_impulso(cfg, pad):
        return impulso(W, cfg, pad, vel, now)
    red, rad, depth = perf[pad]
    target = pick_target(W, cfg, pad, vel)
    dens = occupied(W) / float(N)
    over = dens > cfg['dens_umbral']
    rad_eff = max(1, int(round(rad * cfg['rad_mult']))) if over else int(rad)
    removed = 0
    W['t'] = W['t'] if W['t'] is not None else now
    resto = W['ero_resto']
    notas = erosion_notes(cfg, red, vel)
    tematico = cfg['nivel'] >= 14 and es_aranazo(cfg, pad)
    antes = antes_del_golpe(W, cfg, target, now) if tematico else None
    for c, d in rings(target, rad_eff):
        w = ATENUACION ** d             # 1 en la celda, 1/2 el primer anillo, 1/4...
        x = notas * w + resto[c]
        k = int(math.floor(x + 1e-9))
        resto[c] = x - k
        removed += degrade(W, cfg, c, k)
        light_cell(W, cfg, c, pad, w, now)
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
    for _ in range(n):                  # uno detras de otro, con las reglas de siempre
        j = pulso(W, cfg, target, s, vel, now)
        if j is not None:
            desbordes.append(j)
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
# cicatriz (165-235) y el azul de los rios (235-275)
BANDAS_RESERVADAS = ((55.0, 100.0), (120.0, 275.0))
AUREO = 0.6180339887
L_VACIA = (0.50, 0.64)                                  # generacion par, impar
L_OCUPADA = 0.12                                        # la celda ocupada, mas clara
COL_ZOCALO_NEUTRO = (0.12, 0.12, 0.13)                  # zocalo: oscuro y neutro


def _en_banda(h):
    return any(a <= h < b for a, b in BANDAS_RESERVADAS)


def palette_hue(n, t0=20.0):
    """Tono OKLCH (grados) de la generacion n: t0 + frac(n * aureo) * arco
    libre, recorriendo el circulo y saltando las bandas reservadas."""
    libre = 360.0 - sum(b - a for a, b in BANDAS_RESERVADAS)
    x = ((int(n) * AUREO) % 1.0) * libre
    h = float(t0) % 360.0
    for a, b in BANDAS_RESERVADAS:          # si el tono base cae en una banda, empieza a su salida
        if a <= h < b:
            h = b
    for _ in range(2 * len(BANDAS_RESERVADAS) + 2):
        dist, fin = min(((a - h) % 360.0 or 360.0, b) for a, b in BANDAS_RESERVADAS)
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
    key = (round(cfg['paleta_tono'], 6), round(cfg['paleta_croma'], 6), int(gen), bool(ocupada))
    col = _PAL.get(key)
    if col is None:
        L = L_VACIA[int(gen) % 2] + (L_OCUPADA if ocupada else 0.0)
        col = oklch_to_srgb(L, cfg['paleta_croma'], palette_hue(gen, cfg['paleta_tono']))[0]
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
    return (cfg.get('paleta', 0), cfg.get('paleta_tono'), cfg.get('paleta_croma'),
            cfg['nivel'] >= 15, cfg.get('respaldo', 0))


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


def end_cycle(W, cfg, now, bars=None):
    """Entierra el mundo (desde el nivel 8). bars: compases que duro; sin
    ellos, la concha tiene Shellthick."""
    W['ev']['ciclo'] = dict(t=now, n=W.get('ciclo_n', 1))
    W['bomba'] = {}                     # fase 7: sin pumping pendiente
    W['imp_t'] = {}
    if cfg['nivel'] < 8:
        return False
    cerrar_obras(W, cfg)                # los transitos se cierran antes de hornear
    reg = registro_concha(W, cfg) if cfg['nivel'] >= 15 else None
    g = shell_grosor(cfg, bars)
    W['compacta'] = compactar(W, cfg, g)
    r_in = top_radius(W, cfg)
    # cada celda deposita su loseta sobre lo que le queda debajo: una
    # hondonada se tapiza y sigue siendo hondonada, salvo lo que rellene
    # Colmatacion. El radio nominal solo crece g (la colmatacion no es tiempo).
    colm = cfg.get('colmatacion', 0.0)
    s_new = len(W['shells'])
    for c in range(N):
        lg = max(0.0, r_in - suelo(W, cfg, c))
        W['cols'][c].append([s_new, g + colm * lg])
    W['shells'].append(dict(gen=W['gen'], col=list(shell_color(W['gen'])),
                            occ=list(W['occ']), sp=list(W['sp']), rm=[0] * N,
                            grosor=g, r_in=r_in, r_out=r_in + g))
    if reg:                             # fase 15: el registro de la concha
        W['shells'][-1].update(reg)
    W['quitadas'] = [0] * N
    W['gen'] += 1
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
    1 + valor x Pumphorz. Sin pumping (o con Pumpon apagado), (1, 1)."""
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


def build_instances(W, cfg, now, hide_beacons=False, tiles=True):
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
        W['piel'] = build_piel(W, cfg, now, out)
    if lvl >= 13:                   # fase 13: carreteras (tejido) y rios (fase 13 v2, su geometria)
        out['tejido'], W['tejido'] = build_tejido(W, cfg)
        out['rios'], W['rios_res'] = build_rios(W, cfg)
    if lvl >= 14:                   # fase 14: huellas y particulas de los destructores
        build_destructores(W, cfg, now, out)
    if lvl >= 16:                   # fase 16: lo que ensenan los cortes
        build_arqueologia(W, cfg, now, out)
    if lvl >= 17:                   # fase 17: trafico, esporas y el frente
        build_tiempo(W, cfg, now, out)
    if lvl >= 18:                   # fase 18: luz local y, fuera de la actuacion, el diagnostico
        out['luz_local'] = build_luz_local(W, cfg, now)
        out['diagnostico'] = [] if hide_beacons or not cfg.get('diagnostico', 0) else build_diagnostico(W, cfg)
    out['luz_celda'] = cell_lights(W, cfg, now)  # parte del mundo: tambien en actuacion
    out['luz_conchas'] = shell_lights(W, cfg, now)
    if lvl >= 8 and tiles:
        out['estratos'] = build_tiles(W, cfg, now)
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
        for s, r_in, r_out in col[first:]:
            sh = W['shells'][s]
            colr, rug = tile_material(cfg, sh, s, c)
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None:
                colr = _mix(COL_SCAR, colr, max(0.0, min(1.0, (now - t0) / st)))
            rows.append(_tile_row(c, n, r_in, r_out, colr))
            if era:
                rows[-1].append(1.0 if respaldo else rug)
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
# La vegetacion sale de un L-system con angulos cuantizados a 30 grados; el
# basalto, de prismas hexagonales; la ciudad, de pilas de cajas.

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
    # -------------------------------------------------------------- informal
    techo = lambda x, y, z, w, d, g=30.0: _caja(x, y, z, w * 1.15, 0.05, d * 1.1, 0.0, 0.0, g)
    M['inf_caseta'] = [_losa(-0.35, 0.35, 0.0, 0.72, -0.3, 0.3), techo(0.0, 0.84, 0.0, 0.62, 0.66, 20.0)]
    M['inf_caseta2'] = [_losa(-0.3, 0.3, 0.0, 0.8, -0.3, 0.3), _losa(0.3, 0.55, 0.0, 0.5, -0.22, 0.18),
                        techo(0.0, 0.92, 0.0, 0.6, 0.6, -20.0)]
    M['inf_anadidos'] = [_losa(-0.36, 0.36, 0.0, 0.42, -0.3, 0.3),
                         _caja(0.06, 0.6, -0.04, 0.58, 0.34, 0.48, 0.0, 30.0, 0.0),
                         _caja(-0.08, 0.86, 0.06, 0.40, 0.26, 0.38, 0.0, -30.0, 0.0),
                         techo(-0.08, 1.0, 0.06, 0.4, 0.38, 20.0)]
    M['inf_pasarelas'] = (M['inf_anadidos'][:3]
                          + [_losa(0.25, 0.75, 0.52, 0.56, -0.07, 0.07), _losa(-0.07, 0.07, 0.30, 0.34, 0.25, 0.75),
                             _caja(0.0, 1.0, 0.0, 0.3, 0.2, 0.3, 0.0, 60.0, 0.0)])
    M['inf_barrio'] = [_losa(-0.42, -0.02, 0.0, 0.55, -0.4, 0.0), _losa(0.02, 0.42, 0.0, 0.72, -0.38, 0.02),
                       _losa(-0.4, 0.0, 0.0, 0.85, 0.04, 0.42), _losa(0.04, 0.4, 0.0, 0.45, 0.06, 0.4),
                       _caja(0.2, 0.86, -0.18, 0.34, 0.28, 0.3, 0.0, 30.0, 0.0),
                       _caja(-0.2, 1.0, 0.24, 0.26, 0.24, 0.26, 0.0, -30.0, 0.0),
                       _caja(0.22, 0.56, 0.24, 0.3, 0.22, 0.28, 0.0, 60.0, 0.0)]
    M['inf_torre'] = [_losa(-0.3, 0.3, 0.0, 0.3, -0.28, 0.28), _caja(0.04, 0.42, 0.0, 0.5, 0.24, 0.46, 0.0, 30.0, 0.0),
                      _caja(-0.03, 0.62, 0.02, 0.42, 0.2, 0.4, 0.0, -30.0, 0.0),
                      _caja(0.02, 0.78, 0.0, 0.32, 0.16, 0.32, 0.0, 60.0, 0.0),
                      _losa(-0.11, -0.09, 0.84, 1.0, -0.06, -0.04), _losa(0.06, 0.08, 0.84, 0.96, 0.05, 0.07),
                      _caja(0.12, 0.9, -0.08, 0.012, 0.16, 0.012, 0.0, 0.0, 30.0)]
    M['inf_prot1'] = M['inf_barrio'][:4] + [_caja(0.0, 0.92, 0.0, 0.42, 0.3, 0.42, 0.0, 30.0, 0.0)]
    M['inf_prot2'] = M['inf_barrio'] + [_losa(-0.42, 0.42, 0.62, 0.66, -0.06, 0.06)]
    M['inf_prot3'] = (_escalar(M['inf_barrio'], 0.8) + _escalar(M['inf_torre'], 1.0)[1:])
    M['inf_puente'] = [_losa(-0.5, 0.5, 0.0, 0.25, 0.0, 1.0), _losa(-0.5, -0.4, 0.25, 1.0, 0.0, 1.0),
                       _losa(0.4, 0.5, 0.25, 1.0, 0.0, 1.0)]
    # barrio con plantas rectas impuestas (la planificada coloniza la informal)
    M['inf_hib'] = [_losa(-0.40, 0.30, 0.30, 0.34, -0.30, 0.30), _losa(-0.26, 0.40, 0.62, 0.66, -0.24, 0.30)]
    # ------------------------------------------------------------ planificada
    M['pla_bloque'] = _plantas(0.0, 0.0, 0.8, 0.8, 1, h=1.0, losa=0.08)
    M['pla_bloque2'] = (_plantas(-0.15, 0.0, 0.5, 0.8, 1, h=1.0, losa=0.08)
                        + _plantas(0.25, -0.2, 0.3, 0.4, 1, h=0.7, losa=0.06))
    M['pla_plantas'] = _plantas(0.0, 0.0, 0.62, 0.62, 4)
    M['pla_manzana'] = _plantas(-0.1, -0.08, 0.5, 0.5, 4) + _plantas(0.22, 0.22, 0.36, 0.4, 2, sobra=0.04)
    M['pla_podio'] = [_losa(-0.48, 0.48, 0.0, 0.22, -0.48, 0.48)] + _plantas(0.0, 0.0, 0.48, 0.48, 3, y0=0.22, h=0.26)
    M['pla_rascacielos'] = (_plantas(0.0, 0.0, 0.5, 0.5, 2, h=0.2)
                            + _plantas(0.0, 0.0, 0.40, 0.40, 2, h=0.2, y0=0.4)
                            + _plantas(0.0, 0.0, 0.30, 0.30, 1, h=0.2, y0=0.8))
    M['pla_aguja'] = [_losa(-0.12, 0.12, 0.0, 0.12, -0.12, 0.12), _losa(-0.03, 0.03, 0.12, 1.0, -0.03, 0.03)]
    M['pla_prot1'] = [_losa(-0.48, 0.48, 0.0, 0.18, -0.48, 0.48)] + _plantas(0.0, 0.0, 0.56, 0.56, 3, y0=0.18, h=0.27)
    M['pla_prot2'] = ([_losa(-0.48, 0.48, 0.0, 0.16, -0.48, 0.48)] + _plantas(-0.12, -0.12, 0.4, 0.4, 4, y0=0.16, h=0.21)
                      + _plantas(0.22, 0.22, 0.3, 0.3, 2, y0=0.16, h=0.21))
    M['pla_prot3'] = ([_losa(-0.48, 0.48, 0.0, 0.14, -0.48, 0.48)]
                      + _plantas(0.0, 0.0, 0.5, 0.5, 2, y0=0.14, h=0.2)
                      + _plantas(0.0, 0.0, 0.38, 0.38, 2, y0=0.54, h=0.2)
                      + [_losa(-0.02, 0.02, 0.94, 1.0, -0.02, 0.02)])
    M['pla_puente'] = [_losa(-0.5, 0.5, 0.0, 1.0, 0.0, 1.0)]
    # torre invadida por anadidos (la informal coloniza la planificada)
    M['pla_hib'] = [_caja(0.42, 0.45, 0.0, 0.22, 0.2, 0.3, 0.0, 30.0, 0.0),
                    _caja(-0.4, 0.7, 0.1, 0.2, 0.16, 0.26, 0.0, -30.0, 0.0),
                    _caja(0.05, 0.3, 0.42, 0.28, 0.18, 0.2, 0.0, 30.0, 0.0)]
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
           'rel_prot3', 'inf_barrio', 'inf_prot1', 'inf_prot2', 'inf_prot3', 'inf_hib',
           'pla_manzana', 'pla_podio', 'pla_prot1', 'pla_prot2', 'pla_prot3', 'ciu_valla',
           'veg_claro', 'rel_pedregal', 'inf_escombros'):
    PIE[_m] = ('celda', 0.85)
PIE.update(inf_torre=('celda', 0.6), pla_bloque=('celda', 0.75),
           pla_bloque2=('celda', 0.75), pla_plantas=('celda', 0.6), pla_rascacielos=('celda', 0.55),
           ciu_foso=('celda', 0.75), ciu_andamio=('celda', 0.9))


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

ARBOLES = ['conifera', 'pagoda', 'parasol', 'drago', 'frondosa', 'palmera', 'sauce']
MATORRALES = ['retama', 'brezo', 'helecho', 'graminea', 'enebro', 'palmito']
PLANTAS = ARBOLES + MATORRALES
HOJA_DE = dict(conifera='aguja', pagoda='ancha', parasol='ancha', drago='espada', frondosa='ancha',
               palmera='fronda', sauce='lanceolada', retama='lanceolada', brezo='menuda', helecho='fronda',
               graminea='lamina', enebro='aguja', palmito='abanico')
TIPOS_HOJA = ['aguja', 'ancha', 'lanceolada', 'espada', 'fronda', 'abanico', 'lamina', 'menuda']
DERIVACIONES = 3             # el arbol: 1 brinzal, 2 joven, 3 adulto (derivacion completa)
ANGULO_PLANTA = dict(conifera=84.0, pagoda=88.0, parasol=45.0, drago=34.0, frondosa=36.0, palmera=12.0,
                     sauce=38.0, retama=22.0, brezo=40.0, helecho=55.0, graminea=50.0, enebro=80.0,
                     palmito=45.0)   # angulo de rama con el eje del padre (grados), antes de Varangulo
ANGULO_AUREO = 137.5         # las hojas, a lo largo de la ramilla con el angulo aureo
R_PUNTA = 0.0035             # radio de una ramilla (alto 1); Leonardo da el resto
SUBE = (0.0, 1.0, 0.0)


class _Planta(object):
    """Esqueleto y hojas de un ejemplar mientras se construye."""

    def __init__(self, modelo, var, deriv, cfg):
        import random
        self.modelo, self.deriv = modelo, deriv
        self.rng = random.Random(7919 * (PLANTAS.index(modelo) + 1) + 104729 * var + 17)
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
        self.seg.append(dict(a=a, b=b, nivel=nivel, hijos=[], padre=padre, r=R_PUNTA))
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


def _gen_brezo(P):
    """Ramillete bajo y enmaranado; hoja menuda en racimos."""
    for j in range(8):
        d = P.hijo(SUBE, P.ang(ANGULO_PLANTA['brezo'] * P.u(0.5, 1.5)), ANGULO_AUREO * j)
        t2, p2, d2 = P.eje((0.0, 0.0, 0.0), d, P.u(0.45, 0.7), 2, 0, None, tropismo=0.05)
        for q in range(3):
            dh = P.hijo(d2, P.u(20, 60), P.u(0, 360))
            t3, p3, d3 = P.eje(p2[-1 - (q % 2)], dh, P.u(0.25, 0.4), 2, 1, t2[-1 - (q % 2)])
            P.racimo(p3[-1], d3, 0.14, 2, t3[-1], n=P.dens + 4, abre=65.0)


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


_GEN = dict(conifera=_gen_conifera, pagoda=_gen_pagoda, parasol=_gen_parasol, drago=_gen_drago,
            frondosa=_gen_frondosa, palmera=_gen_palmera, sauce=_gen_sauce, retama=_gen_retama,
            brezo=_gen_brezo, helecho=_gen_helecho, graminea=_gen_graminea, enebro=_gen_enebro,
            palmito=_gen_palmito)
_BIBLIO = {}


def etapas_de(modelo):
    """Derivaciones guardadas: los arboles, 1 a DERIVACIONES; los matorrales, 1."""
    return list(range(1, DERIVACIONES + 1)) if modelo in ARBOLES else [1]


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
_PLANTILLAS = dict(
    ancha=([(0, 0, 0), (0.45, -0.06, -0.32), (1, 0, 0), (0.45, -0.06, 0.32), (0.5, 0.06, 0)],
           [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    menuda=([(0, 0, 0), (0.5, -0.05, -0.3), (1, 0, 0), (0.5, -0.05, 0.3), (0.5, 0.05, 0)],
            [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    lanceolada=([(0, 0, 0), (0.4, -0.04, -0.14), (1, 0, 0), (0.4, -0.04, 0.14), (0.45, 0.04, 0)],
                [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    espada=([(0, 0, 0), (0.5, -0.03, -0.07), (1, 0.05, 0), (0.5, -0.03, 0.07), (0.5, 0.03, 0)],
            [(0, 4, 1), (1, 4, 2), (0, 3, 4), (3, 2, 4)]),
    aguja=([(0, 0, 0), (1, 0.08, -0.34), (0.9, 0.14, -0.26), (1, 0.12, 0.0), (0.9, 0.2, 0.06),
            (1, 0.08, 0.34), (0.9, 0.14, 0.26)],
           [(0, 1, 2), (0, 2, 1), (0, 3, 4), (0, 4, 3), (0, 5, 6), (0, 6, 5)]),
    fronda=([(0, 0, 0), (1, -0.08, 0), (0.25, 0.0, -0.35), (0.55, -0.03, -0.32), (0.85, -0.06, -0.22),
             (0.25, 0.0, 0.35), (0.55, -0.03, 0.32), (0.85, -0.06, 0.22), (0.5, 0.03, 0)],
            [(0, 2, 8), (8, 3, 1), (8, 4, 1), (0, 8, 5), (8, 6, 1), (8, 1, 7)]),
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
    for (a, b, nivel), (r0, r1, _) in zip([(s[0], s[1], s[3]) for s in e['ramas']], e['radios']):
        if lejos and (nivel > 1 or r0 < 0.004):
            continue
        lados = 5 if nivel == 0 else 4
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
                U.append((1.0, 0.0, nivel / nmax))
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
            pv, tv = _PLANTILLAS[tipo]
            z = _norm(_cross(ax, nrm))
            y = _cross(z, ax)
            vv = 0.9 * rng.random()
            k0 = len(P)
            for px, py, pz in pv:
                P.append(_add(pos, _add(_add(_mul(ax, px * tam), y, py * tam), z, pz * tam)))
                Nn.append(y)
                U.append((2.0 + vv, prof, min(1.0, nivel / nmax)))
            T += [(k0 + a_, k0 + b_, k0 + c_) for a_, b_, c_ in tv]
    v = _MALLAS[clave] = (P, Nn, U, T)
    if len(_MALLAS) > 600:
        _MALLAS.clear()
    return v


# -----------------------------------------------------------------------------
# 1. NUCLEO - la piel (fase 11): catalogo, vecindad, compuestos y transitos
# -----------------------------------------------------------------------------
# Logica en el motor, piel en el catalogo. El catalogo dice que modelo va en
# cada estado de cada especie y las cadenas de transito de cada tema; el
# motor decide donde, cuantos y cuando. Toda eleccion (variante, giro,
# operacion) sale del mapa logistico sembrado con la velocidad fundadora y
# la celda; la ocupacion dice cuantas piezas lleva el compuesto.

TEMAS = ['naturaleza', 'ciudad']
AVANCES = ['gates', 'pasos']
ESTADOS = ['semilla', 'crecimiento', 'ramificacion', 'fusion', 'coronacion']
ESPECIES = {('naturaleza', GEO): 'vegetacion', ('naturaleza', ARQ): 'relieve',
            ('ciudad', GEO): 'informal', ('ciudad', ARQ): 'planificada'}
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
    for tema, esp, p in (('naturaleza', 'vegetacion', 'veg'), ('naturaleza', 'relieve', 'rel'),
                         ('ciudad', 'informal', 'inf'), ('ciudad', 'planificada', 'pla')):
        semilla = {'veg': list(MATORRALES), 'rel': ['rel_columna', 'rel_columna2'],
                   'inf': ['inf_caseta', 'inf_caseta2'], 'pla': ['pla_bloque', 'pla_bloque2']}[p]
        resto = {'veg': [list(ARBOLES)] * 4,
                 'rel': ['rel_columnas', 'rel_mesetas', 'rel_meseta', 'rel_cumbre'],
                 'inf': ['inf_anadidos', 'inf_pasarelas', 'inf_barrio', 'inf_torre'],
                 'pla': ['pla_plantas', 'pla_manzana', 'pla_podio', 'pla_rascacielos']}[p]
        add(tema, esp, 'semilla', semilla)
        for estado, mo in zip(ESTADOS[1:], resto):
            add(tema, esp, estado, mo if isinstance(mo, list) else [mo])
        add(tema, esp, 'puente', ['bosque' if p == 'veg' else p + '_puente'])
        add(tema, esp, 'protagonista', ['frondosa', 'pagoda', 'conifera'] if p == 'veg'
            else [p + '_prot1', p + '_prot2', p + '_prot3'])
        add(tema, esp, 'hibrido', [FORMA_HIBRIDO.get(p, p + '_hib')])
    add('ciudad', 'planificada', 'remate', ['pla_aguja'])
    for tema, esp, mo in (('naturaleza', 'vegetacion', 'veg_claro'), ('naturaleza', 'relieve', 'rel_pedregal'),
                          ('ciudad', 'informal', 'inf_escombros'), ('ciudad', 'planificada', 'ciu_valla')):
        add(tema, esp, 'huella', [mo])     # fase 14: lo que deja una catastrofe
    for obra in ('valla', 'foso', 'andamio', 'grua'):
        add('ciudad', 'obra', obra, ['ciu_' + obra])
    # fase 16: lo que ensenan los cortes, en la pared (expuesto) y en el fondo
    for tema, esp, pared, fondo in (('naturaleza', 'vegetacion', ['fos_tronco', 'fos_tronco2'], ['fos_tronco']),
                                    ('naturaleza', 'relieve', ['fos_basalto'], ['fos_basalto']),
                                    ('ciudad', 'informal', ['arq_cimientos'], ['arq_cimientos']),
                                    ('ciudad', 'planificada', ['arq_sotano'], ['arq_cimientos']),
                                    ('ciudad', 'calle', ['arq_calle'], ['arq_calle'])):
        add(tema, esp, 'expuesto', pared)
        add(tema, esp, 'fondo', fondo)
    add('ciudad', 'galeria', 'union', ['arq_galeria'])
    cadenas = {('naturaleza', 'vegetacion'): (['inclinar', 'puentes', 'hundir', 'esporas'], ['emerger']),
               ('naturaleza', 'relieve'): (['soldadura', 'relleno'], ['soldadura', 'relleno']),
               ('ciudad', 'informal'): (['soldadura', 'relleno'], ['soldadura', 'relleno']),
               ('ciudad', 'planificada'): (['solar', 'excavacion', 'obreros', 'andamio'],
                                           ['grua', 'fachada', 'aguja'])}
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
        if (estado.startswith('cadena') and x in ETAPAS) or x in MODELOS or x in PLANTAS or x in FORMAS:
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
        if W['derribo'][i] and W['et_f'][i] == 0 and W['et_c'][i] == 0:
            W['derribo'][i] = 0         # fase 14: derribada; la obra puede volver a empezar
        for clave, obj in (('et_f', tf[i]), ('et_c', tc[i])):
            e = W[clave][i]
            if now - W['t_' + clave][i] < espera:
                continue
            if e > obj:
                _etapa(W, i, clave, e - 1, now)
            elif e < obj and pasos and playing:
                _etapa(W, i, clave, e + 1, now)


def cerrar_obras(W, cfg):
    """Fin de ciclo: cada transito, en su estado final, sin animacion."""
    if cfg['nivel'] < 11:
        return
    tf, tc = objetivos(W, cfg)
    for i in range(N):
        for clave, obj in (('et_f', tf[i]), ('et_c', tc[i])):
            W[clave][i] = W['ant_' + clave][i] = obj
            W['t_' + clave][i] = -99.0


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
    return 'ciudad' if modelo[:3] in ('inf', 'pla', 'arq') else 'mineral'


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
        g = 'mod_' + modelo if modelo.startswith('ciu_') or not doble or es_ejemplar(modelo) else \
            'mod_%s_%s' % (modelo, 'pul' if pulido else 'por')
        _GEOMETRIAS[clave] = g
    return g


def geometrias_piel(cfg=None):
    """[(geometria, modelo, material)]: en la fase 11, pulida (mat_pulido) y
    porosa (mat_poroso); desde la fase 12, una por modelo con el material de
    su familia."""
    doble = (cfg or DEFAULT_CFG)['nivel'] < 12
    out = []
    for mo in sorted(MODELOS):
        if mo.startswith('ciu_'):
            out.append((geometria_de(mo), mo, 'mat_poroso'))
        elif doble:
            out.append((geometria_de(mo, True), mo, 'mat_pulido'))
            out.append((geometria_de(mo, False), mo, 'mat_poroso'))
        else:
            out.append((geometria_de(mo, doble=False), mo, MAT_FAMILIA[familia_de(mo)]))
    for mo in ejemplares_de(cfg or DEFAULT_CFG):     # fase 11 v8: la biblioteca, una geometria por ejemplar
        out.append((geometria_de(mo), mo, 'mat_pulido' if doble else MAT_FAMILIA['dosel']))
    return out


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


def build_piel(W, cfg, now, out):
    """Las formaciones como modelos del tema: compuesto, puentes del cluster,
    pieza protagonista, cadenas de transito y particulas. Devuelve el resumen
    para la leyenda."""
    lim = limit(cfg)
    tema = tema_de(cfg)
    paso = W.get('paso') or 0.125
    cl = clusters(W, cfg)
    tf, tc = objetivos(W, cfg, cl)
    piezas = compuestos = 0
    suelos = [base_radius(W, cfg, i) for i in range(N)]
    bases = dict((i, _mul(normal_i(i), suelos[i])) for i in range(N))

    doce = cfg['nivel'] >= 12         # fase 12: una geometria por modelo, rugosidad en el alfa
    respaldo = doce and cfg.get('respaldo', 0)
    arde = celdas_ardiendo(W, cfg) if cfg['nivel'] >= 14 else {}
    tiempo = cfg['nivel'] >= 17       # fase 17: el pulso balancea el dosel y enciende ventanas
    bq = beat_stop(W, cfg) if tiempo else 0.0

    def emit(modelo, pulido, p, marco, dims, col, rug=1.0, luces=0):
        nonlocal piezas
        fila = _fila_m(p, marco, dims[0], dims[1], dims[2], col)
        if doce:                    # las ventanas (0-4) van en el alfa: rugosidad + 2 x nivel
            fila.append(1.0 if respaldo else rug + 2.0 * luces)
        out.setdefault(geometria_de(modelo, pulido, not doce), []).append(fila)
        piezas += 1

    def contar(k):                  # fase 11 v8: filas copiadas de la memoria de la celda
        nonlocal piezas
        piezas += k
    emit.contar = contar

    natural = tema == 'naturaleza'      # fase 11 v5: la naturaleza legible (piel_natural)
    nat_copas = 0
    if natural:
        ter = terreno(W, cfg, cl)
        por_celda = cauces(W, cfg, cl, ter)['por_celda'] if cfg['nivel'] >= 13 else {}
        cult = cultivos(W, cfg, ter, por_celda, now, paso)     # fase 11 v8: bancales, riego y acequias
        ctx = dict(cl=cl, ter=ter, bases=suelos, cauces=por_celda,
                   sway=(lambda i: balanceo(W, cfg, i, bq)) if tiempo else (lambda i: (0.0, 0.0)),
                   cerca=lambda i: lod_cerca(W, cfg, i) and not (cfg.get('impostores', 1) and _PRESUPUESTO['lleno']),
                   rio_cerca=lambda i: any(c in por_celda for c in [i] + list(NEIGH[i])),
                   res=dict(hojas=0, todas=0, ejemplares=0, emergentes=0, frutales={},
                            biomas=dict((b, 0) for b in BIOMAS)))
    bomba = _Bomba(W, cfg, now, out)    # fase 7 v12: el pumping de los impulsos
    for i in range(N):
        bomba.cerrar()
        vh = W['vh'][i]
        own = W['own'][i]
        if vh <= 0.005 or not own:
            continue
        n = normal_i(i)
        e, _, t, _ = _marco(i)
        p0 = bases[i]
        base = base_radius(W, cfg, i)
        cw, cl_ = _cell_sizes(base, i)
        bomba.abrir(i, p0, n, cw, cl_)
        rb = W['rebrote'][i] if cfg['nivel'] >= 15 else 0
        if rb == 1:                                 # fase 15: banco de semillas
            _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, vh, semilla_caos(i, 21), 7,
                        COL_SEMILLA, now, paso, 'semillas')
            continue
        if rb == 2:                                 # y brota, a saltos
            vh *= 0.25 + 0.75 * _stop((now - W['t_rebrote'][i]) / max(1e-6, rebrote_dur(cfg, paso)))
        esp = especie_de(tema, own)
        cf, cc = cadenas_de(cfg, tema, esp)
        sat = W['par'][i] >= 0
        o = W['occ'][i]
        est = estado_idx(cfg, o)
        pulido = W['vel'][i] >= cfg['vel_umbral']
        if doce:                                    # el material del tema, por la velocidad
            rug = rugosidad(cfg, W['vel'][i])
            col = material_tema(cfg, COL_ESPECIE[esp], 'ciudad' if tema == 'ciudad' else
                                'dosel' if esp == 'vegetacion' else 'mineral', rug)
            ancho = W['vig'][i] if tema == 'naturaleza' else 1.0
        else:
            rug, ancho = 1.0, 1.0
            col = _material_col(COL_ESPECIE[esp], pulido)
        lt, sc, amp = _luz_formacion(W, cfg, i, now)
        kb, fl = rebote(cfg, W, i, now, paso)
        if natural:                                 # el latido hincha; su color va al borde (uTinte)
            if lt > 0:
                vh *= 1.0 + amp * lt
            nat_copas += piel_natural_cache(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out,
                                            now, paso, not doce)
            continue
        if lt > 0:
            vh *= 1.0 + amp * lt
            col = _tint(_mix(col, sc, LATIDO_TINTE * lt), 1.0 + 0.25 * lt)
        if fl > 0:                                  # destello del nacimiento
            col = _mix(col, (1.0, 1.0, 1.0), 0.6 * fl)
        if sat:
            col = _tint(col, 0.85)
        if i in arde:                               # fase 14: brasa a saltos y carbon
            q_a = arde[i]
            chispa = int(now / paso * FOTOS_PASO + i) % 2
            col = _quemar(col, q_a, chispa)
        k_ = cl['de'][i]
        capital = k_ >= 0 and cl['capital'][k_] == i
        comp = compuesto(cfg, own, W['vel'][i], i, o, sat)
        # pieza principal: el estado, la protagonista o la coronacion
        modelo = None
        alto = 1.0
        dy = 0.0
        q_c = [avance_etapa(W, i, 'et_c', k + 1, now, paso) for k in range(len(cc))]
        if not sat and q_c and q_c[0] > 0:
            tr = cumbre_tramos(cfg, o)
            kc = CORONA_K + CORONA_TRAMO * tr
            modelo = (modelos_de(cfg, tema, esp, 'coronacion') or [None])[0]
            if 'emerger' in cc:                     # el arbol madre emerge del dosel
                alto, dy = kc, -(1.0 - q_c[cc.index('emerger')]) * 0.5
            elif 'fachada' in cc:                   # grua -> la fachada se cierra -> aguja
                alto = kc * (0.55 + 0.45 * q_c[cc.index('fachada')])
            else:                                   # soldadura -> relleno
                alto = kc * (0.6 + 0.4 * q_c[-1])
        elif capital and W['et_f'][i] >= len(cf) and cf:
            prot = modelos_de(cfg, tema, esp, 'protagonista')
            if prot:
                modelo = prot[min(len(prot) - 1, clase_cluster(len(cl['celdas'][k_])))]
                alto = 1.0 + 0.1 * clase_cluster(len(cl['celdas'][k_]))
        if modelo is None:
            lista = modelos_de(cfg, tema, esp, ESTADOS[min(est, 1) if sat else min(est, 3)])
            if not lista:
                continue
            modelo = lista[min(len(lista) - 1, int(comp[0]['var'] * len(lista)))]
        # inclinacion hacia la capital (vegetacion, etapa 'inclinar')
        incl, rumbo = 0.0, 0.0
        if k_ >= 0 and not capital and 'inclinar' in cf:
            q = avance_etapa(W, i, 'et_f', cf.index('inclinar') + 1, now, paso)
            if q > 0:
                incl = INCLINAR * q
                rumbo = round(_rumbo(n, _hacia(n, n, normal_i(cl['capital'][k_]))), 1)
        if tiempo and esp == 'vegetacion' and incl == 0.0:     # fase 17: el dosel se balancea
            incl, rumbo = balanceo(W, cfg, i, bq)
        luces = ventanas_celda(W, cfg, i, bq) if tiempo and doce and tema == 'ciudad' and not respaldo else 0
        hund = 'hundir' in cf and k_ >= 0 and avance_etapa(W, i, 'et_f', cf.index('hundir') + 1,
                                                             now, paso)
        if len(comp) > 1:
            compuestos += 1
        esc_sat = cfg['sat_size'] if sat else 1.0
        for k, pz in enumerate(comp):
            if k == 0:
                mo, esc, giro = modelo, 1.0, pz['giro']
                ej = _marco(i, giro, incl, rumbo)
                h_ = vh * alto * kb
                dims = _pie(mo, h_, cw * esc_sat * kb, cl_ * esc_sat * kb, ancho)
                p = _add(p0, ej[1], dy * vh)
            else:
                sub = modelos_de(cfg, tema, esp, 'crecimiento' if est >= 2 and pz['var'] > 0.5
                                 else 'semilla') or [modelo]
                mo = sub[min(len(sub) - 1, int(pz['var'] * 7) % len(sub))]
                esc = pz['esc']
                ej = _marco(i, pz['giro'], pz['incl'] + incl, pz['rumbo'] if pz['incl'] else rumbo)
                y = pz['y'] - (0.4 * esc * hund if hund else 0.0)
                h_ = vh * esc * kb
                dims = _pie(mo, h_, cw * esc * esc_sat * kb, cl_ * esc * esc_sat * kb, ancho)
                p = _add(_add(_add(p0, e, pz['x'] * cw * esc_sat), t, pz['z'] * cl_ * esc_sat), n, y * vh)
            ck = _tint(col, 0.88 + 0.24 * pz['var'])
            emit(mo, pulido, p, ej, dims, ck, rug, luces)
        # hibrido: la otra especie deja su rastro, con la planta de la principal
        if W['sp'][i] == HIB:
            hib = modelos_de(cfg, tema, esp, 'hibrido')
            otra = especie_de(tema, ARQ if own == GEO else GEO)
            if hib:
                ej = _marco(i, comp[0]['giro'])
                propio = PIE.get(hib[0], ('esbelto', 0))[0] == 'celda'
                dims = _pie(hib[0] if propio else modelo, vh * kb, cw * esc_sat * kb, cl_ * esc_sat * kb)
                ch = material_tema(cfg, COL_ESPECIE[otra], familia_de(hib[0]), rug) if doce \
                    else _material_col(COL_ESPECIE[otra], pulido)
                emit(hib[0], pulido, p0, ej, dims, ch, rug, luces)
        # remate y grua de la coronacion de la ciudad
        if not sat and 'aguja' in cc and q_c and q_c[0] > 0:
            top = _add(p0, n, vh * alto)
            qa = q_c[cc.index('aguja')]
            if qa > 0:
                rem = modelos_de(cfg, tema, esp, 'remate')
                if rem:
                    emit(rem[0], pulido, top, _marco(i), (0.5 * cw * 0.3, 0.35 * vh * qa, 0.5 * cl_ * 0.3),
                         col, rug)
            else:
                g = modelos_de(cfg, tema, 'obra', 'grua')
                if g:
                    pg = _add(_add(p0, e, 0.42 * cw), t, -0.3 * cl_)
                    emit(g[0], False, pg, _marco(i, 90.0), (0.5 * cw, vh * CORONA_K * 1.15, 0.5 * cl_),
                         COL_OBRA['grua'])
        # puentes del cluster
        if k_ >= 0 and cl['mascara'][i]:
            kp = 0.0
            for nombre, valor in (('soldadura', 0.35), ('relleno', 1.0), ('puentes', 1.0), ('andamio', 1.0)):
                if nombre in cf:
                    kp = max(kp, valor * avance_etapa(W, i, 'et_f', cf.index(nombre) + 1, now, paso,
                                                      ANDAMIO_PASOS if nombre == 'andamio' else 1.0))
            pm = modelos_de(cfg, tema, esp, 'puente')
            if kp > 0 and pm:
                kw, y0, gr = PUENTE[esp]
                if 'andamio' in cf:                 # el podio sube planta a planta
                    k_ancho, k_alto = 1.0, kp
                elif 'soldadura' in cf:             # soldadura fina, luego relleno
                    k_ancho, k_alto = (0.35 if kp < 1 else 1.0), 1.0
                else:                               # los puentes del dosel crecen
                    k_ancho, k_alto = kp, 1.0
                for q, j in enumerate(cl['mascara'][i]):
                    vmin = min(W['vh'][i], W['vh'][j]) if W['vh'][j] > 0.005 else W['vh'][i]
                    pj = bases[j]
                    largo = 0.5 * math.sqrt((p0[0] - pj[0]) ** 2 + (p0[1] - pj[1]) ** 2
                                            + (p0[2] - pj[2]) ** 2) + 0.06
                    ej = _marco_puente(i, j)
                    # cada medio puente de la celda, un poco mas alto que el anterior: sus
                    # tapas, en el mismo plano, se pisarian y parpadearian (z-fighting)
                    alto_p = max(0.01, gr * vmin * k_alto * (1.0 + 0.04 * (q % 3)))
                    cp = material_tema(cfg, COL_PUENTE[esp], familia_de(pm[0]), rug) if doce \
                        else _material_col(COL_PUENTE[esp], pulido)
                    if i in arde:                   # fase 14: el dosel de lo que arde, tambien
                        cp = _quemar(cp, arde[i], int(now / paso * FOTOS_PASO + i) % 2)
                    emit(pm[0], pulido, _add(p0, n, y0 * vmin), ej, (kw * min(cw, cl_) * k_ancho, alto_p, largo),
                         cp, rug)
                if esp == 'vegetacion':             # el dosel se cierra: una copa en cada hueco
                    for tri, pc, ej, rho in _huecos_dosel(i, cl['mascara'], bases):
                        vs = [W['vh'][x] for x in tri if W['vh'][x] > 0.005]
                        vmin = min(vs) if vs else W['vh'][i]
                        sx_, sz_ = DOSEL_HUECO * rho * k_ancho / DOSEL_ANCHO, DOSEL_HUECO * rho * k_ancho / DOSEL_LARGO
                        pc = _add(_add(_add(pc, ej[1], y0 * vmin), ej[0], -DOSEL_CENTRO[0] * sx_),
                                  ej[2], -DOSEL_CENTRO[1] * sz_)
                        emit(pm[0], pulido, pc, ej, (sx_, max(0.01, gr * vmin * k_alto), sz_), cp, rug)
        # obras de la ciudad y particulas
        if k_ >= 0 and cf:
            ef = W['et_f'][i]
            if 'solar' in cf and 1 <= ef < len(cf):
                emit('ciu_valla', False, p0, _marco(i), _pie('ciu_valla', 0.12 * lim, cw, cl_), COL_OBRA['valla'])
            if 'excavacion' in cf and cf.index('excavacion') + 1 <= ef < len(cf):
                emit('ciu_foso', False, _add(p0, n, 0.005), _marco(i), _pie('ciu_foso', 0.03 * lim, cw, cl_),
                     COL_OBRA['foso'])
                if ef == cf.index('excavacion') + 1:
                    _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, vh,
                                semilla_caos(i, 7), 8, COL_POLVO, now, paso, 'polvo')
            if 'obreros' in cf and ef == cf.index('obreros') + 1:
                _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, vh,
                            semilla_caos(i, 11), 8, COL_OBRERO, now, paso, 'obreros')
            if 'andamio' in cf:
                qa = avance_etapa(W, i, 'et_f', cf.index('andamio') + 1, now, paso, ANDAMIO_PASOS)
                if 0 < qa < 1:
                    emit('ciu_andamio', False, p0, _marco(i),
                         _pie('ciu_andamio', PUENTE[esp][2] * vh * 1.3, cw, cl_), COL_OBRA['andamio'])
            if 'esporas' in cf and ef >= cf.index('esporas') + 1 \
                    and now - W['t_et_f'][i] < ESPORAS_PASOS * paso:
                _particulas(out.setdefault('particulas', []), n, p0, cw, cl_, vh,
                            semilla_caos(i, 3), 6, COL_ESPORA, now, paso, 'esporas')
    bomba.cerrar()
    # resumen para la leyenda
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
    res = dict(tema=tema, clusters=len(tam), max=max(tam or [0]), compuestos=compuestos,
               piezas=piezas, obras=obras, medias=medias)
    if natural:
        _, ln = _limites_pisos(cfg)
        r_ = ctx['res']
        _PRESUPUESTO['lleno'] = r_['todas'] > HOJAS_TOPE    # el fotograma siguiente: impostores si no caben
        res.update(ejemplares=r_['ejemplares'], hojas=r_['hojas'], emergentes=r_['emergentes'],
                   biomas=dict(r_['biomas']), frutales=r_['frutales'], hibridos=ter.get('hibridos', {}),
                   inundados=cult['inundados'], parcelas=cult['parcelas'])
        res.update(copas=nat_copas, montes=ter['montes'], cordilleras=ter['cordilleras'],
                   nevadas=sum(1 for c in range(N) if ter['centro'][c] >= ln * ter['hmax']),
                   cerca=sum(1 for c in range(N) if W['occ'][c] > 0 and lod_cerca(W, cfg, c)))
    return res


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
    return [(0.0, PISO_BASAL[0]), (0.35, PISO_BASAL[1]), (0.36, PISO_MONTANO[0]),
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
        return [], dict(cordilleras=0, montes=0, ejes=[])
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), GRID['lo'], GRID['hi'],
             cfg['umbral_vecindad'], cfg['peso_vecina'], cfg['min_cluster'], cfg['th_fusion'], cfg['th_branch'],
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
    for c in rel:
        rasgos.append(('cono', c, round(alto[c], 3), 1.1))
    montes = 0
    for c in range(N):
        if W['occ'][c] > 0 and W['own'][c] == GEO:
            m_ = monte(W, cfg, c)
            if m_ > 1e-6:
                rasgos.append(('domo', c, round(m_, 3)))
                montes += 1
    return rasgos, dict(cordilleras=cords, montes=montes, ejes=ejes)


def _pintar(np, rej, n, e, t, hx, hz, H, perfil):
    """El parche de un casquete (cono o domo) de alto H: (filas, columnas,
    alturas, alto del rasgo)."""
    filas, cols = _ventana(np, n, 1.25 * max(hx, hz))
    ix = np.ix_(filas, cols)
    D = rej['D'][ix]
    x = D @ np.array(e) / hx
    z = D @ np.array(t) / hz
    q = np.sqrt(x * x + z * z)
    q = np.where(D @ np.array(n) > 0.0, q, 9.0)
    if perfil == 'domo':
        f = np.clip(1.0 - q * q, 0.0, 1.0) ** 2
    else:
        f = np.clip(1.0 - q, 0.0, 1.0) ** 1.1
    return filas, cols, H * f, np.full(f.shape, float(H))


def _cresta(np, rej, a, b, ha, hb, silla):
    """El parche de la cresta de a a b: el alto baja del de cada cumbre al
    collado (silla x la media) y la anchura es la de media celda."""
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
    H = (ha + (hb - ha) * u) * (silla + (1.0 - silla) * np.abs(2.0 * u - 1.0) ** 1.5)
    return filas, cols, H * np.clip(1.0 - dist / w, 0.0, 1.0) ** 1.15, H


def _parche(np, rej, r):
    """El parche de un rasgo (se guarda por rasgo: al cambiar una celda solo
    se recalculan sus rasgos)."""
    cache = _TERRENO.setdefault('parches', {})
    v = cache.get(r)
    if v is not None:
        return v
    if r[0] == 'cresta':
        v = _cresta(np, rej, *r[1:])
    else:
        c = r[1]
        e_, t_ = tangents(NORMALS[c])
        hx, hz = _semiejes(c, r[3] if r[0] == 'cono' else 1.1)
        v = _pintar(np, rej, NORMALS[c], e_, t_, hx, hz, r[2], r[0])
    if len(cache) > 3000:
        cache.clear()
    cache[r] = v
    return v


def _sobre(np, dst, hloc, parche):
    """El maximo del mapa y el parche, y el alto del rasgo que gana."""
    filas, cols, v, H = parche
    ix = np.ix_(filas, cols)
    cur = dst[ix]
    gana = v > cur
    dst[ix] = np.where(gana, v, cur)
    hloc[ix] = np.where(gana, H, hloc[ix])


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
    E = Sa = El = None
    centro = [0.0] * N
    if np is not None:
        rej = _rejilla(np)
        Erel = np.zeros((TERRENO_H, TERRENO_W))
        Hrel = np.zeros_like(Erel)
        Edom = np.zeros_like(Erel)
        Hdom = np.zeros_like(Erel)
        r0, r1 = TERRENO_H, 0               # solo las filas con relieve (lo demas es 0)
        for r in rasgos:                    # conos y crestas (relieve), domos (montes)
            pa = _parche(np, rej, r)
            if len(pa[0]):
                r0, r1 = min(r0, int(pa[0][0])), max(r1, int(pa[0][-1]) + 1)
            if r[0] == 'domo':
                _sobre(np, Edom, Hdom, pa)
            else:
                _sobre(np, Erel, Hrel, pa)
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
                Ez = (Ez + np.roll(Ez, 1, 0) + np.roll(Ez, -1, 0) + np.roll(Ez, 1, 1) + np.roll(Ez, -1, 1)) / 5.0
            E[r0:r1] = Ez
        if hib[0] or hib[1]:                # fase 11 v8: bancales y mesetas, en el mismo mapa
            hib_t = _hibridos_terreno(np, rej, E, cfg, hib)
            filas = [k for k in range(TERRENO_H) if hib_t['filas'][k]]
            r0, r1 = min([r0] + filas), max([r1] + [k + 1 for k in filas])
        cero = [0.0] * TERRENO_W
        El = [cero] * r0 + E[r0:r1].tolist() + [cero] * (TERRENO_H - max(r0, r1)) if r1 > r0 \
            else [cero] * TERRENO_H
        Sa = _suelo_mapa(np, rej, S)
    t = dict(E=E, S=Sa, El=El, centro=centro, hmax=alto_hipso(cfg),
             version=_TERRENO.get('version', 0) + 1, rasgos=len(rasgos), **res)
    t['hib'] = hib_t if np is not None else None
    t['hibridos'] = dict(arrozales=dict((i, nb) for i, nb in hib[0]), mesetas=dict(hib[1]))
    if El is not None:
        t['centro'] = [alto_en(t, NORMALS[c]) for c in range(N)]
    _TERRENO['clave'], _TERRENO['t'], _TERRENO['version'] = clave, t, t['version']
    _TERRENO['array'] = None
    _TERRENO['sello_t'] = sello
    return t


def _hibridos_clave(W, cfg, cl):
    """(arrozales ((celda, bancales)...), mesetas ((celda, nivel)...), capitales, parametros)."""
    if cfg['nivel'] < 11 or tema_de(cfg) != 'naturaleza':
        return ((), (), (), ())
    arroz = tuple((i, bancales(W, cfg, i)) for i in range(N) if bancales(W, cfg, i))
    mes = tuple((i, niveles_meseta(W, cfg, i)) for i in range(N) if niveles_meseta(W, cfg, i))
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
        f_, c_ = _ventana(np, NORMALS[i], 0.8 * max(SIZE_EW[i], SIZE_NS[i]))
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
        filas[f_] = True
    if mes:
        nivel = dict(mes)
        cap = dict(caps)
        alt = cfg['altura_meseta'] * lim
        for i, nv in mes:
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
            f_, c_ = _ventana(np, NORMALS[i], 0.75 * max(SIZE_EW[i], SIZE_NS[i]))
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
            filas[f_] = True
        E += (mesa * alt).astype(np.float32)
    return dict(h0=h0.astype(np.float32), top=top.astype(np.float32), mesa=mesa.astype(np.float32),
                filas=filas)


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
RUTA_HOJAS = 'SOP'          # las hojas van en la malla de cada ejemplar (Script SOP), no en POPs
PARCELA_TEX = 6             # una parcela de la meseta: 6 x 6 texeles del mapa (los setos, en el shader)


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
    r el relieve, g el radio del suelo (erosionado), b 0, a 1. None sin numpy."""
    t = _TERRENO.get('t')
    np = _np()
    if t is None or np is None or t['E'] is None:
        if np is None:
            return None
        a = np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)
        a[..., 1] = DEFAULT_CFG['core_radius']
        a[..., 3] = 1.0
        return a
    a = _TERRENO.get('array')
    if a is None:
        a = np.zeros((TERRENO_H, TERRENO_W, 4), dtype=np.float32)
        a[..., 0] = t['E']
        a[..., 1] = t['S']
        a[..., 3] = 1.0
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
BIOMA_PLANTAS = dict(frio=(['graminea', 'enebro'], ['conifera']),
                     templado=(['retama', 'brezo'], ['frondosa', 'pagoda']),
                     calido=(['helecho', 'palmito'], ['parasol', 'drago', 'palmera']))
BIOMA_FRIO, BIOMA_CALIDO = 0.6, 0.25        # latitud relativa (0 ecuador, 1 polo)
MONTANO = 0.35                              # el piso montano (v5): de aqui a Limitebosque, conifera
SOTOBOSQUE_K = 0.6                          # el matorral al pie del arbol joven
MATORRAL_K = 0.45                           # el matorral, de la altura de la formacion
MESETA_K = 0.55                             # cada nivel de la meseta, 0,55 del de abajo hacia la capital
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


def _poisson(i, cw, cl, r, k=1.0, semilla=0):
    """Puntos (x, z) de la celda i (en su plano tangente, en unidades del mundo)
    separados al menos r, solo los que caen en la celda (la mas cercana): los
    bosques de celdas vecinas encajan sin pisarse. k: la parte de la celda
    (las etapas del dosel)."""
    clave = (GRID['lo'], GRID['hi'], i, round(cw, 4), round(cl, 4), round(r, 4), round(k, 2), semilla)
    v = _POISSON.get(clave)
    if v is not None:
        return v
    import random
    rng = random.Random(1009 * i + 7 * semilla + 3)
    n = NORMALS[i]
    e, t = tangents(n)
    vecinas = list(NEIGH[i])
    pts = []
    for _ in range(40 * max(4, int((cw * cl) / max(1e-6, r * r)) + 4)):
        x, z = rng.uniform(-0.75, 0.75) * cw * k, rng.uniform(-0.75, 0.75) * cl * k
        # la celda mas cercana: el punto en la esfera unidad
        q = _norm(_add(_add(n, e, x / (cw / max(1e-6, SIZE_EW[i]))), t, z / (cl / max(1e-6, SIZE_NS[i]))))
        if any(_dot(q, NORMALS[j]) > _dot(q, n) for j in vecinas):
            continue
        if math.hypot(x / (0.5 * cw * k + 1e-9), z / (0.5 * cl * k + 1e-9)) > 1.25:
            continue
        if all((x - a) ** 2 + (z - b) ** 2 >= r * r for a, b in pts):
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
        col = pintar(color_natural(cfg, hg, rug))
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
        r = max(0.08 * min(cw, cl_), h_ref * esc0 * ej['copa'] * (1.0 + cfg['timidez']))
        otra = otra_planta(cfg, i, arbol_mo)
        for q, (x, z) in enumerate(_poisson(i, cw, cl_, r, 0.75 + 0.25 * kp, int(cfg.get('variantes', 4)))):
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
                for s in (-1, 1):
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
        for q in range(len(pts) - 1):               # matorral entre ellos
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
NAT_CFG = ('nivel', 'caos', 'max_caos_nat', 'th_branch', 'th_fusion', 'th_crown', 'limite_bosque', 'biomas',
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
    cap = ctx['cl']['capital'][k_] if k_ >= 0 else -1
    kp = avance_etapa(W, i, 'et_f', cf.index('puentes') + 1, now, paso) if k_ >= 0 and 'puentes' in cf else 1.0
    clave = (W['occ'][i], W['own'][i], W['sp'][i], W['vel'][i], W['par'][i], round(vh, 5), kb, round(fl, 3),
             sat, round(rug, 4), round(ancho, 4), pulido, doble, cap, len(ctx['cl']['celdas'][k_]) if k_ >= 0 else 1,
             W['vel'][cap] if cap >= 0 else 0, W['own'][cap] if cap >= 0 else 0, round(kp, 3), W['et_f'][i],
             tuple((W['occ'][j] > 0) * W['own'][j] for j in NEIGH[i]), ctx['ter']['version'],
             tuple(ctx['cauces'].get(i, ())), ctx['rio_cerca'](i), ctx['cerca'](i), ctx['sway'](i),
             derivacion(W, cfg, i, now, paso), notas_colonas(W, i), ctx['bases'][i],
             tuple(cfg.get(x) for x in NAT_CFG), _clave_biblio(cfg), GRID['lo'], GRID['hi'])
    v = _NAT_CACHE.get(i)
    res = ctx['res']
    if v is not None and v[0] == clave:
        _, filas, d, n = v
        for g, f in filas:
            out.setdefault(g, []).append(list(f))
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
    marcas = dict((g, len(f)) for g, f in out.items() if isinstance(f, list))
    n = piel_natural(W, cfg, ctx, i, vh, rug, ancho, kb, fl, sat, pulido, arde, emit, out, now, paso)
    filas = []
    for g, f in out.items():
        if isinstance(f, list) and len(f) > marcas.get(g, 0) and g != 'particulas':
            filas += [(g, tuple(x)) for x in f[marcas.get(g, 0):]]
    d = {}
    for k, x in res.items():
        if k == 'biomas':
            d[k] = dict((b, x[b] - antes[k][b]) for b in x)
        elif k == 'frutales':
            d[k] = dict((c, y) for c, y in x.items() if c == i)
        else:
            d[k] = x - antes[k]
    if len(_NAT_CACHE) > 4 * N:
        _NAT_CACHE.clear()
    _NAT_CACHE[i] = (clave, filas, d, n)
    return n


def derivacion(W, cfg, i, now, paso):
    """Derivacion visible del arbol de la celda i: 2 el joven (ocupacion 2), la
    completa el adulto. Avance = gates: cada gate que sube la ocupacion anade una
    derivacion; Avance = pasos: la nueva aparece Pasosetapa pasos despues."""
    o = W['occ'][i]
    obj = max(1, min(DERIVACIONES, o))
    if int(cfg.get('avance', 0)) == 1 and now - W['t_h'][i] < cfg['pasos_etapa'] * paso:
        return max(1, obj - 1)
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
                    if cfg.get('lagos', 1) and laguna(W, cfg, c) > 0.02:
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
    clave = (id(ca), _CAUCES.get('clave'), cfg.get('respaldo', 0), color_rio(cfg))
    if _CAUCES.get('filas_clave') == clave:         # las cintas no se mueven: se guardan (sin copiar:
        return _CAUCES['filas'], res                # nadie las modifica despues)
    ter = terreno(W, cfg)
    col = color_rio(cfg)
    hmax = ter['hmax']
    rug = 1.0 if cfg.get('respaldo', 0) else RUG_RIO
    for lista in ca['muestras']:
        pts = []
        for d, c, w in lista:
            E = alto_en(ter, d)
            pts.append((_mul(d, suelo(W, cfg, c) + E + RIO_LIFT + 0.03 * E / hmax), w))
        for (p, w), (q, w2) in zip(pts, pts[1:]):
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
             cfg['max_rio'], cfg['min_via'], len(W.get('trazas') or []))
    if _TEJIDO.get('sello') == sello:       # ya visto en este fotograma
        return _TEJIDO['t']
    trazas = frozenset((min(a, b), max(a, b)) for a, b in W.get('trazas') or []) \
        if cfg['nivel'] >= 15 else frozenset()
    ter = terreno(W, cfg) if tema == 'naturaleza' and cfg['rios'] else None
    alturas = tuple(round(s_ + e_, 3) for s_, e_ in zip(suelos_fotograma(W, cfg), ter['centro'])) if ter else ()
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), tema, cfg['rios'], cfg['carreteras'],
             cfg['min_via'], cfg['max_rio'], cfg['umbral_vecindad'], cfg['peso_vecina'],
             cfg['min_cluster'], cfg['th_fusion'], GRID['lo'], GRID['hi'], trazas,
             cfg.get('peso_traza', 0.0), alturas, cfg.get('pendiente_min', 0.05))
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
    _TEJIDO['clave'], _TEJIDO['t'] = clave, t
    _TEJIDO['version'] = _TEJIDO.get('version', 0) + 1
    _TEJIDO['sello'] = sello
    return t


def _tramo_suelo(W, cfg, a, b, ancho, col, rug, out):
    """Dos medios tramos de la celda a a la b, a ras del suelo, siguiendo la
    curva: centro de a -> punto medio -> centro de b."""
    na, nb = normal_i(a), normal_i(b)
    ra = base_radius(W, cfg, a) + TEJIDO_LIFT
    rb = base_radius(W, cfg, b) + TEJIDO_LIFT
    pa, pb = _mul(na, ra), _mul(nb, rb)
    pm = _mul(_norm(_add(na, nb)), 0.5 * (ra + rb))
    for p, q in ((pa, pm), (pm, pb)):
        Y = _norm(_add(p, q))           # el centro, sobre la superficie (no en la cuerda)
        c = _mul(Y, 0.5 * (math.sqrt(_dot(p, p)) + math.sqrt(_dot(q, q))))
        d = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
        d = _add(d, Y, -_dot(d, Y))
        L = math.sqrt(_dot(d, d))
        if L < 1e-6:
            continue
        Z = _mul(d, 1.0 / L)
        X = _cross(Y, Z)
        rx, ry, rz = _euler_xyz(X, Y, Z)
        out.append([c[0], c[1], c[2], rx, ry, rz, ancho, TEJIDO_ALTO, L + 0.5 * ancho,
                    col[0], col[1], col[2], rug])


def build_tejido(W, cfg):
    """(filas de la geometria 'tejido', resumen para la leyenda)."""
    t = tejido(W, cfg)
    W['tejido_vias'] = t['vias']
    filas = []
    w = cfg['grosor_via']
    for a, b in t['vias']:                  # los rios van en su geometria ('rios', build_rios)
        _tramo_suelo(W, cfg, a, b, w, COL_VIA, RUG_VIA, filas)
    if cfg.get('respaldo', 0):
        for f in filas:
            f[12] = 1.0
    return filas, dict(rios=len(t['rios']), tramos_rio=len(t['caudal']), tramos_via=len(t['vias']))


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

RUINA_ESP = ['vegetacion', 'relieve', 'informal', 'planificada']
ACCIDENTE = dict(vegetacion='rayo', relieve='desprendimiento', informal='se desploma un anadido',
                 planificada='caen las plantas altas')
CATASTROFE = dict(vegetacion='incendio', relieve='derrumbe', informal='derrumbe en cadena',
                  planificada='implosion')
RUINA_ALTO = dict(vegetacion=0.30, relieve=0.22, informal=0.26, planificada=0.12)    # x limite
COL_CENIZA = (0.44, 0.43, 0.41)           # copos de ceniza
COL_CARBON = (0.10, 0.09, 0.08)           # lo que arde se carboniza
COL_BRASA = (1.00, 0.46, 0.10)
COL_RUINA = dict(vegetacion=(0.25, 0.23, 0.21), relieve=(0.38, 0.37, 0.40), informal=(0.46, 0.44, 0.41),
                 planificada=COL_OBRA['valla'])
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
    while o > 0 and W['occ'][i] >= o and k < 64:
        if not _undo_note(W, cfg, i):
            break
        k += 1
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
    for c in vecindad(objetivo):
        if W['occ'][c] > 0 and (0 < W['et_f'][c] < tf[c] or 0 < W['et_c'][c] < tc[c]):
            k = cl['de'][c]
            celdas.update(cl['celdas'][k] if k >= 0 else [c])
    nuevas = 0
    for x in sorted(celdas):
        nuevas += 0 if W['derribo'][x] else 1
        W['derribo'][x] = 1
        for clave in ('et_f', 'et_c'):
            if W[clave][x] > 0:
                _etapa(W, x, clave, W[clave][x] - 1, now)
    return nuevas


def foco_catastrofe(W, cfg, i):
    """Donde seria la catastrofe de la celda i: su cluster y sus enlaces de
    la misma especie, tal como estan ahora."""
    cl = clusters(W, cfg)
    k = cl['de'][i]
    zona = sorted(cl['celdas'][k]) if k >= 0 else [i]
    enlaces = dict((c, [j for j in cl['mascara'][c] if W['own'][j] == W['own'][i]]) for c in zona)
    return dict(celda=i, own=W['own'][i], especie=especie_de(tema_de(cfg), W['own'][i]),
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
        esp = especie_de(tema_de(cfg), W['own'][v])
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
        if (esp in ('vegetacion', 'relieve')) != (tema == 'naturaleza'):
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
MATERIA = dict(vegetacion=(CARBON, 0.06, 0.85), relieve=(BASALTO, 0.5, 0.6),
               informal=(HORMIGON, 0.85, 0.6), planificada=(HORMIGON, 0.85, 0.6))
MATERIA_TEMA = dict(naturaleza='carbon y basalto', ciudad='hormigon')
RUG_LOSETA, RUG_ZOCALO = 0.7, 0.9


def registro_concha(W, cfg):
    """El registro de la concha que se entierra: tema, y por celda especie
    (1 + indice en RUINA_ESP; 0 vacia), estado y cluster (-1 ninguno); y las
    carreteras, las calles (celdas por las que pasan) y los rios."""
    tema = tema_de(cfg)
    cl = clusters(W, cfg)
    esp, est, clu = [0] * N, [-1] * N, [-1] * N
    for i in range(N):
        if W['occ'][i] > 0 and W['own'][i]:
            esp[i] = 1 + RUINA_ESP.index(especie_de(tema, W['own'][i]))
            est[i] = estado_idx(cfg, W['occ'][i])
            clu[i] = cl['de'][i]
    t = tejido(W, cfg) if cfg['nivel'] >= 13 else {}
    vias = sorted([min(a, b), max(a, b)] for a, b in t.get('vias', []))
    return dict(tema=tema, esp=esp, estado=est, cluster=clu, vias=vias,
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
    if nuevo == 'ciudad' and reg['tema'] == 'ciudad':
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
    if tema == 'ciudad' and c in sh.get('calles', ()):
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
                    calle=(0.24, 0.24, 0.25))
RUG_EXPUESTO = dict(vegetacion=0.35, relieve=0.4, informal=0.85, planificada=0.8, calle=0.7)
COL_GALERIA, RUG_GALERIA = (0.58, 0.57, 0.53), 0.8
NOMBRE_ERA = dict(vegetacion='carbon', relieve='basalto', informal='ruinas', planificada='ruinas',
                  calle='calles')
PRIORIDAD_ERA = ['vegetacion', 'planificada', 'informal', 'relieve', 'calle']
UNION_NOMBRE = dict(canon='canon', galeria='galeria de metro')


def contenido(sh, c):
    """Lo que guarda la concha sh en la celda c: su especie, 'calle' (una
    celda de la ciudad por la que pasaba una carretera) o None."""
    if sh.get('tema') is None:
        return None
    e = sh['esp'][c]
    if e:
        return RUINA_ESP[e - 1]
    if sh['tema'] == 'ciudad' and c in sh.get('calles', ()):
        return 'calle'
    return None


def en_corte(W, cfg, c, R=None):
    """La celda c esta dentro de un corte: su suelo, por debajo del radio nominal."""
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
    galeria = tema_de(cfg) == 'ciudad'
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


def build_arqueologia(W, cfg, now, out):
    """Las piezas expuestas en los cortes y las galerias de metro."""
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
            col = COL_EXPUESTO[q]
            t0 = W['scars'].get(s * 1000 + x)
            if t0 is not None:                  # la cicatriz manda
                col = _mix(COL_SCAR, col, max(0.0, min(1.0, (now - t0) / st)))
            th = b - a
            if j < 0:                           # en el fondo: medio enterrada
                mo, v = _variante(modelos_de(cfg, tema, q, 'fondo'), s, x, -1)
                if mo is None:
                    continue
                n = normal_i(c)
                cw, cl_ = _cell_sizes(b, c)
                h = 0.5 * min(th, 0.8)
                giro = 30.0 * int(v * 6)
                emit(mo, _mul(n, b - 0.5 * h), _marco(c, giro), (0.55 * cw, h, 0.55 * cl_), col,
                     RUG_EXPUESTO[q])
            else:                               # en la pared, asomando al corte
                mo, v = _variante(modelos_de(cfg, tema, q, 'expuesto'), s, x, j)
                if mo is None:
                    continue
                cols = column_radii(W, cfg, j)
                r_mid = next((0.5 * (ri + ro) for s_, ri, ro in cols if s_ == s), 0.5 * (a + b))
                off, marco, ancho = _marco_pared(c, j)
                ancho *= r_mid
                prof = min(0.3, 0.25 * ancho)
                y0 = a + 0.1 * th
                p = _add(_add(_mul(marco[1], y0), off, r_mid), marco[2], 0.1 * prof)
                emit(mo, p, marco, (0.7 * ancho, 0.8 * th, prof), col, RUG_EXPUESTO[q])
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


def balanceo(W, cfg, i, bq):
    """(inclinacion, rumbo) del dosel de la celda i: el vaiven del pulso
    (Swaymax, en fase con el beat, con una onda suave por longitud) y, si pasa
    el frente, el empuje hacia el norte."""
    n = normal_i(i)
    lon = math.atan2(n[2], n[0])
    sw = cfg['sway_max'] * math.sin(2.0 * math.pi * bq / SWAY_BEATS + 0.5 * lon)
    if cfg['nivel'] >= 19:              # fase 19: el LFO del modular es viento
        sw += cfg['viento_max'] * (2.0 * W['modular']['lfo'] - 1.0)
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
    if tema == 'ciudad' and cfg['nivel'] >= 19:     # fase 19: el ruido del modular es smog
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
ESCENAS = ['naturaleza', 'ciudad']
# los parametros de una escena: (nombre, naturaleza, ciudad). 'luz_principal.dimmer'
# y 'luz_relleno.dimmer' son de las luces, no de FASE1.
ESCENA_PARS = [
    ('Tema', 'naturaleza', 'ciudad'),
    ('Paleta', 'generaciones', 'mineral'), ('Paletatono', 20.0, 205.0), ('Paletacroma', 0.09, 0.06),
    ('Umbralvecindad', 4.0, 4.5), ('Pesovecina', 0.5, 0.5), ('Mincluster', 2, 2),
    ('Umbraldensidad', 0.6, 0.6),
    ('Caos', 3.91, 3.74), ('Maxpiezas', 6, 5),
    ('Rugmin', 0.05, 0.1), ('Rugmax', 0.85, 0.9),
    ('Swaymax', 6.0, 4.0), ('Trafico', 2, 3),
    ('Luzcalida', 0.35, 0.0),
    ('luz_principal.dimmer', 1.15, 1.0), ('luz_relleno.dimmer', 0.16, 0.24),
]
LUZ_CALIDA = (1.00, 0.88, 0.72)             # la luz de dia de la escena de naturaleza
COL_FOCO, COL_CHARCO = (1.00, 0.62, 0.20), (0.30, 0.17, 0.05)
COL_BRILLO_BRASA = (0.55, 0.20, 0.04)
COL_POLVO_LUZ = (0.16, 0.13, 0.10)
COL_DIAG_PUENTE, COL_DIAG_VIA, COL_DIAG_RIO = (0.95, 0.95, 0.95), (1.0, 0.85, 0.2), (0.3, 0.5, 1.0)
COL_DIAG_BAJA, COL_DIAG_ALTA = (0.25, 0.85, 0.35), (0.95, 0.25, 0.2)


def escena_defecto(nombre):
    """{parametro: valor} de la escena por defecto 'naturaleza' o 'ciudad'."""
    k = 1 + ESCENAS.index(nombre)
    return dict((fila[0], fila[k]) for fila in ESCENA_PARS)


def obras_a_medias(W, cfg, cl=None):
    """Celdas de la ciudad con una obra a medias (fusion o coronacion sin acabar)."""
    if cfg['nivel'] < 11 or tema_de(cfg) != 'ciudad':
        return []
    tf, tc = objetivos(W, cfg, cl)
    return [i for i in range(N) if (0 < W['et_f'][i] < tf[i]) or (0 < W['et_c'][i] < tc[i])]


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


# =============================================================================
# 2. ADAPTADOR TOUCHDESIGNER
# =============================================================================
# Todo lo de aqui abajo usa op(), parent(), me y absTime: solo funciona
# dentro de TouchDesigner.

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
    return CHOP_NAMES + ['i_particulas'] + extra + ['i_' + g for g, _, _ in geometrias_piel(c)]

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


def _perfiles():
    """(perfiles, tipos, modos, pulsos, caidas del pumping) de la tabla
    perfiles_erosion, leidos por nombre de columna (la columna rol es solo
    para leer). Sin las columnas modo y pulsos (o capacidad, su nombre en
    la v12 y la v13), las de por defecto: bombo 3 y tom 2 en impulso; sin
    pump_rel (antes de la v13), 0,20 s el bombo y 0,12 el tom."""
    t = parent().op('perfiles_erosion')
    if t is None or t.numRows < 2:
        return (list(PERFILES_DEFECTO), list(TIPOS_DEFECTO), list(MODOS_DEFECTO), list(PULSOS_DEFECTO),
                list(PUMP_REL_DEFECTO))
    out, tipos, modos, caps, rels = [], [], [], [], []
    for r in range(1, min(t.numRows, 9)):
        try:
            p = (int(float(t[r, 'reduccion'].val)), int(float(t[r, 'radio'].val)),
                 int(float(t[r, 'profundidad'].val)))
        except Exception:
            p = PERFILES_DEFECTO[r - 1]
        out.append(p)
        try:
            md = t[r, 'modo'].val.strip().lower()
        except Exception:
            md = ''
        modos.append(md if md in MODOS_PAD else MODOS_DEFECTO[r - 1])
        try:
            col = 'pulsos' if t[0, 'pulsos'] is not None else 'capacidad'
            caps.append(max(1, int(round(float(t[r, col].val)))))
        except Exception:
            caps.append(PULSOS_DEFECTO[r - 1])
        try:
            rels.append(max(0.0, float(t[r, 'pump_rel'].val)))
        except Exception:
            rels.append(PUMP_REL_DEFECTO[r - 1])
        try:
            tp = t[r, 'tipo'].val.strip()
        except Exception:
            tp = ''
        tipos.append(tp or ('impulso' if modos[-1] == 'impulso' else tipo_perfil(*p)))
    while len(out) < 8:
        out.append(PERFILES_DEFECTO[len(out)])
        tipos.append(TIPOS_DEFECTO[len(tipos)])
        modos.append(MODOS_DEFECTO[len(modos)])
        caps.append(PULSOS_DEFECTO[len(caps)])
        rels.append(PUMP_REL_DEFECTO[len(rels)])
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
    if t is not None and t.numRows > 1:
        filas = []
        for r in range(1, t.numRows):
            try:
                filas.append((t[r, 'tema'].val.strip(), t[r, 'especie'].val.strip(),
                              t[r, 'estado'].val.strip(), int(float(t[r, 'variante'].val)),
                              t[r, 'modelo'].val.strip()))
            except Exception:
                pass
        cat = catalogo_de(filas) or CATALOGO
    _CACHE['cat'], _CACHE['cat_frame'] = cat, absTime.frame
    return cat


def _colores_drum():
    """Colores de las balizas de la bateria (tabla colores_drum: pad r g b)."""
    t = parent().op('colores_drum')
    out = list(COLORES_DRUM)
    if t is None or t.numRows < 2:
        return out
    for r in range(1, t.numRows):
        try:
            k = int(float(t[r, 'pad'].val)) - 1
            if 0 <= k < 8:
                out[k] = tuple(max(0.0, min(1.0, float(t[r, ch].val))) for ch in ('r', 'g', 'b'))
        except Exception:
            pass
    return out


def cfg():
    c = dict(DEFAULT_CFG)
    c.update(
        nivel=_p('Nivel', 3),
        luz_seq=int(_p('Luzseq', True)),
        luz_conchas=int(_p('Luzconchas', True)),
        luz_conchas_pulso=max(0.0, _p('Luzconchaspulso', c['luz_conchas_pulso'])),
        luz_conchas_reposo=max(0.0, _p('Luzconchasreposo', c['luz_conchas_reposo'])),
        luz_conchas_alcance=max(1, int(_p('Luzconchasalcance', c['luz_conchas_alcance']))),
        shell_thick=_p('Shellthick', c['shell_thick']),
        height_factor=_p('Alturafactor', c['height_factor']),
        seed_frac=_p('Semillafrac', c['seed_frac']),
        grow_frac=_p('Growstep', c['grow_frac']),
        cost_max=_p('Costemax', c['cost_max']),
        gate_mode=int(_p('Gatemode', True)),
        gate_max=_p('Gatemax', c['gate_max']),
        vel_umbral=_p('Umbralvel', c['vel_umbral']),
        th_branch=_p('Umbralram', c['th_branch']),
        th_fusion=_p('Umbralfusion', c['th_fusion']),
        th_crown=_p('Umbralcorona', c['th_crown']),
        th_cumbre=_p('Umbralcumbre', c['th_cumbre']),
        cumbre_tramos=_p('Tramoscumbre', c['cumbre_tramos']),
        sat_size=_p('Tamsatelite', c['sat_size']),
        sat_limit=_p('Limsatelite', c['sat_limit']),
        neigh_mode=_menu('Vecina', ['velocidad', 'velocidadocupacion'], 1),
        beats_per_bar=_p('Negrasporcompas', c['beats_per_bar']),
        umbral_madurez=_p('Umbralmadurez', c['umbral_madurez']),
        umbral_novedad=_p('Umbralnovedad', c['umbral_novedad']),
        compases_quietos=_p('Compasesquietos', c['compases_quietos']),
        umbral_territorio=_p('Umbralterritorio', c['umbral_territorio']),
        compases_territorio=_p('Compasesterritorio', c['compases_territorio']),
        ciclo_min=_p('Ciclomin', c['ciclo_min']),
        ciclo_max=_p('Ciclomax', c['ciclo_max']),
        cambio_entierra=int(_p('Cambioentierra', False)),
        giro_vivo=int(_p('Girovivo', True)),
        giro_min=_p('Giromin', c['giro_min']),
        dens_umbral=_p('Umbraldensidad', c['dens_umbral']),
        rad_mult=_p('Multradio', c['rad_mult']),
        target_mode=_menu('Objetivo', TARGET_MODES, 2),
        herencia=_p('Herencia', c['herencia']),
        paleta=_menu('Paleta', PALETAS, 0),
        paleta_tono=_p('Paletatono', c['paleta_tono']) % 360.0,
        paleta_croma=max(0.0, min(0.15, _p('Paletacroma', c['paleta_croma']))),
        max_shells=_p('Maxconchas', c['max_shells']),
        grosor_tiempo=int(_p('Grosortiempo', True)),
        grosor_max=_p('Grosormax', c['grosor_max']),
        corteza_max=max(0.0, _p('Cortezamax', c['corteza_max'])),
        colmatacion=max(0.0, min(1.0, _p('Colmatacion', c['colmatacion']))),
        scar_time=max(0.1, _p('Cicatriz', c['scar_time'])),
        flash=_p('Destello', c['flash']),
    )
    if c['nivel'] >= 7:
        c['perfiles'], c['tipos'], c['modos'], c['pulsos'], c['pump_rels'] = _perfiles()
        c['colores_drum'] = _colores_drum()
        c.update(balizas_drum=int(_p('Balizasdrum', True)),
                 luz_drum=_p('Luzdrum', c['luz_drum']),
                 erosion_vel=int(_p('Erosionvel', True)),
                 vel_ref=_p('Velref', c['vel_ref']),
                 vida_baliza_drum=_p('Vidabalizadrum', c['vida_baliza_drum']),
                 # fase 7 v12: impulso
                 pump_amt=max(0.0, _p('Pumpamt', c['pump_amt'])),
                 pump_horz=max(0.0, _p('Pumphorz', c['pump_horz'])),
                 pump_hold=max(0.0, _p('Pumphold', c['pump_hold'])),       # v13: golpe seco
                 pump_velmin=max(0.0, min(1.0, _p('Pumpvelmin', c['pump_velmin']))),
                 pump_tope=max(1.0, _p('Pumptope', c['pump_tope'])),          # v14
                 pump_on=int(_p('Pumpon', True)))
    if c['nivel'] >= 11:
        c.update(tema=_menu('Tema', TEMAS, 0),
                 peso_vecina=max(0.0, _p('Pesovecina', c['peso_vecina'])),
                 umbral_vecindad=_p('Umbralvecindad', c['umbral_vecindad']),
                 min_cluster=max(2, int(_p('Mincluster', c['min_cluster']))),
                 caos=max(0.0, min(4.0, _p('Caos', c['caos']))),
                 max_piezas=max(1, int(_p('Maxpiezas', c['max_piezas']))),
                 avance=_menu('Avance', AVANCES, 0),
                 pasos_etapa=max(1, int(_p('Pasosetapa', c['pasos_etapa']))),
                 rebote=max(0.0, _p('Rebote', c['rebote'])),
                 catalogo=_catalogo(),
                 # fase 11 v5: la naturaleza legible
                 umbral_monte=max(1, int(_p('Umbralmonte', c['umbral_monte']))),
                 max_caos_nat=max(0, int(_p('Maxcaosnat', c['max_caos_nat']))),
                 limite_bosque=max(0.0, min(1.0, _p('Limitebosque', c['limite_bosque']))),
                 limite_nieve=max(0.0, min(1.0, _p('Limitenieve', c['limite_nieve']))),
                 altura_monte=max(0.0, _p('Alturamonte', c['altura_monte'])),
                 lod_nat=max(0.0, _p('Lodnat', c['lod_nat'])),
                 tinte_borde_nat=max(0.0, _p('Tintebordenat', c['tinte_borde_nat'])),
                 superficie=int(str(_p('Modocamara', 'globo')) == 'superficie'),
                 # fase 11 v8: brotes, arboles y terrazas
                 biomas=int(bool(_p('Biomas', True))),
                 variantes=max(1, min(8, int(_p('Variantes', c['variantes'])))),
                 var_angulo=max(0.0, min(45.0, _p('Varangulo', c['var_angulo']))),
                 cuantizar30=int(bool(_p('Cuantizar30', False))),
                 inclinacion=max(0.0, min(30.0, _p('Inclinacion', c['inclinacion']))),
                 densidad_hoja=max(1, min(30, int(_p('Densidadhoja', c['densidad_hoja'])))),
                 traslucidez=max(0.0, min(1.0, _p('Traslucidez', c['traslucidez']))),
                 timidez=max(0.0, min(1.0, _p('Timidez', c['timidez']))),
                 emergentes=max(0.0, min(1.0, _p('Emergentes', c['emergentes']))),
                 orla=int(bool(_p('Orla', True))),
                 mezcla=max(0.0, min(1.0, _p('Mezcla', c['mezcla']))),
                 impostores=int(bool(_p('Impostores', True))),
                 terrazas_por_nota=max(0.0, _p('Terrazaspornota', float(c['terrazas_por_nota']))),
                 max_terrazas=max(1, min(16, int(_p('Maxterrazas', c['max_terrazas'])))),
                 paso_terraza=max(0.02, min(0.5, _p('Pasoterraza', c['paso_terraza']))),
                 muro_terraza=max(0.05, min(0.9, _p('Muroterraza', c['muro_terraza']))),
                 riego=int(bool(_p('Riego', True))),
                 color_cultivo=(max(0.0, _p('Colorcultivor', c['color_cultivo'][0])),
                                max(0.0, _p('Colorcultivog', c['color_cultivo'][1])),
                                max(0.0, _p('Colorcultivob', c['color_cultivo'][2]))),
                 altura_meseta=max(0.0, min(1.0, _p('Alturameseta', c['altura_meseta']))),
                 max_niveles=max(1, min(6, int(_p('Maxniveles', c['max_niveles'])))),
                 marco=_menu('Marco', MARCOS, 1),
                 setos=int(bool(_p('Setos', True))))
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
                 ancho_max_rio=max(0.005, _p('Anchomaxrio', c['ancho_max_rio'])),
                 emisivo_rio=max(0.0, _p('Emisivorio', c['emisivo_rio'])),
                 lagos=int(_p('Lagos', True)),
                 # fase 13 v3: rios que se ven desde el globo
                 ancho_min_px=max(0.0, _p('Anchominpx', c['ancho_min_px'])),
                 pendiente_min=max(0.0, _p('Pendientemin', c['pendiente_min'])),
                 encuadre=max(0.3, min(1.0, _p('Encuadre', c['encuadre']))))
    if c['nivel'] >= 14:
        c.update(ventana_escalada=max(1, int(_p('Ventanaescalada', c['ventana_escalada']))),
                 golpes_escalada=max(1, int(_p('Golpesescalada', c['golpes_escalada']))),
                 pasos_fuego=max(1, int(_p('Pasosfuego', c['pasos_fuego']))),
                 max_fuego=max(1, int(_p('Maxfuego', c['max_fuego']))),
                 pasos_polvo=max(1, int(_p('Pasospolvo', c['pasos_polvo']))))
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
                 master_beat=_master_beat())
    if c['nivel'] >= 19:
        c.update(fuente_modular=_menu('Fuentemodular', FUENTES_MODULAR, c['fuente_modular']),
                 rango_modular=_menu('Rangomodular', [r[0] for r in RANGOS_MODULAR], 0),
                 suavizado=max(0.0, _p('Suavizado', c['suavizado'])),
                 viento_max=max(0.0, _p('Vientomax', c['viento_max'])),
                 respiracion=max(0.0, min(1.0, _p('Respiracion', c['respiracion']))),
                 smog=max(0.0, _p('Smog', c['smog'])), niebla=max(0.0, min(1.0, _p('Niebla', c['niebla']))),
                 glitch=max(0.0, min(1.0, _p('Glitch', c['glitch']))))
    if c['nivel'] >= 18:
        c.update(diagnostico=int(_p('Diagnostico', False)),
                 luz_calida=max(0.0, min(1.0, _p('Luzcalida', c['luz_calida']))),
                 escena=_menu('Escena', ESCENAS, 0))
    return c


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


def playing():
    try:
        return _ritmo().playing()
    except Exception:
        return True


def surface_radius(frame=None):
    return top_radius(world(), cfg())


def nucleo_radius(frame=None):
    """La esfera del nucleo ya no crece (motor v23): lo que no se dibuja de
    cada columna lo cubre su zocalo, y una esfera a cota comun taparia las
    hondonadas."""
    return cfg()['core_radius']


def floor_radius(i, frame=None):
    """Suelo de la celda i (lo usa la reticula)."""
    return suelo(world(), cfg(), i)


def giro_factor(frame=None):
    """Multiplica el giro del planeta (lo lee 'ritmo'). 1 sin Girovivo."""
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
    elif lvl >= 5 and ch == _p('Canal2', 14):
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
                res = 'EROSION pad %d %s celda %d' % (pad + 1, ev['tipo'], ev['celda'])
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
    elif c['nivel'] >= 5 and ch == _p('Canal2', 14):
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
               'territorio']
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
                    territorio='%.2f' % ev.get('territorio', 0.0))
        cab = [t[0, k].val for k in range(t.numCols)]     # por nombre de columna
        t.appendRow([vals.get(k, '') for k in cab])
        while t.numRows > CICLOS_MAX + 1:
            t.deleteRow(1)
    except Exception as e:
        print('AVISO  tabla ciclos: %s' % e)


# --- fotograma ---------------------------------------------------------------

def frame_tick():
    W, c = world(), cfg()
    now = absTime.seconds
    if c['nivel'] >= 15 and (W.get('tema') is None or not c['tema_en_ciclo']):
        W['tema'] = int(c['tema'])      # fase 15: el tema del mundo
    if c['nivel'] >= 19:                # fase 19: las senales del modular, antes del mundo
        md = W['modular']
        dt = max(0.0, min(0.25, now - md.get('t_fotograma', now)))
        md['t_fotograma'] = now
        modular_tick(W, c, leer_modular(c, now), dt, now)
    res = tick(W, c, now, tempo(), playing())
    _CACHE['nivel'] = c['nivel']        # fase 17: para la luz y las ventanas del shader
    _CACHE['modular'] = dict(W['modular']) if c['nivel'] >= 19 else None
    _CACHE['ventanas'] = ventanas_luz_de(W, c)
    _CACHE['tinte'] = tinte_actual(W, c) if c['nivel'] >= 17 else [1.0, 1.0, 1.0]
    _CACHE['luz_calida'] = c.get('luz_calida', 0.0) if c['nivel'] >= 18 else 0.0
    _CACHE['uni'] = uniformes_piel(W, c, now)       # fase 11 v5: pisos, borde y agua del shader
    if res.get('burst'):
        print('AVISO  %s' % W['aviso'])
    if res.get('frente'):
        print('FRENTE  cambio de pattern: el frente recorre el planeta en %d pasos' % int(c['pasos_frente']))
    if res.get('ciclo'):
        registrar_ciclo(W, c, res['ciclo'])
    pk = palette_key(c)                 # cambiar la paleta recolorea todo lo enterrado
    dirty = W.get('dirty', True) or _CACHE.get('tiles') is None or _CACHE.get('pal') != pk
    _CACHE['pal'] = pk
    inst = build_instances(W, c, now, hide_beacons=performance(), tiles=dirty)
    if dirty:
        _CACHE['tiles'] = inst['estratos']
    else:
        inst['estratos'] = _CACHE['tiles']
    _CACHE['inst'] = inst
    _CACHE['frame'] = absTime.frame
    hechas = _CACHE.setdefault('filas_chop', {})
    for name in chop_names(c):
        o = parent().op(name)
        if o is None:
            continue
        if name == 'i_estratos' and not dirty:
            continue
        if name not in CHOP_NAMES:      # fase 11: solo los modelos que han cambiado
            filas = inst.get(name[2:], [])
            if hechas.get(name) == filas:
                continue
            hechas[name] = filas
        o.cook(force=True)
    if dirty or _CACHE.get('ret_R') != top_radius(W, c):
        _CACHE['ret_R'] = top_radius(W, c)
        o = parent().op('reticula_chop')
        if o is not None:
            o.cook(force=True)
    terreno_al_dia_td(W, c)
    W['dirty'] = False


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
    u['uTerreno'] = (0.0, alto_hipso(c) if c['nivel'] >= 11 else 1.0, HUNDIDO, 0.0)
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
            W, c = world(), cfg()
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
                note_on(W, c, s, cell_note(x), _p('Velprueba', 100), now, tempo())
                _gate_prueba(W, c, s, cell_note(x), now)
            if s == GEO:
                _seq1_beacon(note)
            cl = clusters(W, c)
            k = cl['de'][ci]
            print('SEMBRARZONA  %s %s -> celda %d y %d vecinas   %s'
                  % ('SEQ1' if s == GEO else 'SEQ2', note_name(note), ci, len(NEIGH[ci]),
                     'cluster de %d celdas, capital %d' % (len(cl['celdas'][k]), cl['capital'][k])
                     if k >= 0 else 'sin cluster todavia (pulsa otra vez)'))
    elif name == 'Forzarciclo':
        registrar_ciclo(W, c, close_cycle(W, c, now, 'forzado'))
    elif name == 'Resetmundo':
        reset_world()
        print('MUNDO  vaciado')
    W['dirty'] = True


def on_value(name, val):
    if name == 'Modoactuacion':
        try:
            parent().par.Showgrid = not bool(val)
        except Exception:
            pass
    elif name in ('Variantes', 'Varangulo', 'Cuantizar30', 'Densidadhoja'):    # fase 11 v8
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
    elif name == 'Escena':              # fase 18: cargar la escena elegida
        n = cargar_escena(str(val))
        print('ESCENA  %s cargada (%d parametros)' % (val, n))


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
        for r in range(1, t.numRows):
            if t[r, 0].val == nombre:
                out[t[r, 1].val] = t[r, 2].val
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

def wobble(frame=None):
    try:
        return _wobble()
    except Exception:
        return 0.0


def _wobble():
    """Grados de rx de todas las geometrias del planeta. Inclina el eje
    hacia la camara y en contra, para que se vean los dos polos. Ajeno al
    reloj del secuenciador. Pagina Fase3: Rotextra, Balanceo, Balanceoper."""
    if _CACHE.get('wob_frame') == absTime.frame:
        return _CACHE.get('wob', 0.0)
    t = absTime.seconds
    st = _CACHE.setdefault('wob_st', {'ph': 0.0, 'env': 0.0})
    dt = t - _CACHE.get('wob_t', t)
    _CACHE['wob_t'] = t
    v = wobble_step(st, dt, _p('Rotextra', True), _p('Pausa', False),
                    _p('Balanceo', 60.0), _p('Balanceoper', 90.0))
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
    W, c = world(), cfg()
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
    return (v[0] * d, v[1] * d, v[2] * d, c['flash'] * env) + tuple(flash_color(W, c))


def flash_value(k, frame=None):
    return flash_light()[k]


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
    try:
        cop = parent().op('camara')
        fov = float(cop.par.fov.eval())
        try:
            metodo = str(cop.par.viewanglemethod.eval())
        except Exception:
            pass
        if 'focal' in metodo:
            fo = float(cop.par.focal.eval())
            ap = float(cop.par.aperture.eval())
            fov, metodo = math.degrees(2.0 * math.atan(ap / (2.0 * max(1e-3, fo)))), 'horzfov'
    except Exception:
        pass
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


def camera_state():
    if _CACHE.get('cam_frame') == absTime.frame:
        return _CACHE['cam']
    W, c = world(), cfg()
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
    dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2)
    near = max(0.05, min(5.0, 0.25 * (dist - Re)))
    far = dist + 2.0 * Re + 10.0
    st = dict(pos=pos, tgt=tgt, R=R, Re=Re, d=d, d_obj=d_obj, d_min=d_min, theta=th,
              fov=fov, metodo=metodo, aspect=aspect, encuadre=k, w=s, near=near, far=far,
              salto=salto, modo='superficie' if s >= 0.5 else 'globo')
    _CACHE['cam'] = st
    _CACHE['cam_frame'] = absTime.frame
    return st


def cam(key, k=0, frame=None):
    v = camera_state()[key]
    return v[k] if isinstance(v, (tuple, list)) else v


def cam_reset():
    """La proxima lectura de la camara salta al encuadre (sin transicion)."""
    for k in ('cam_d', 'cam_v', 'cam_R', 'cam_frame'):
        _CACHE.pop(k, None)


# --- leyenda -----------------------------------------------------------------

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
        if 'copas' in pz:                       # fase 11 v5: la naturaleza legible
            b = pz.get('biomas', {})            # fase 11 v8: la biblioteca de ejemplares
            lines.append('  NATURALEZA  biomas F/T/C %d/%d/%d   ejemplares %d   %s hojas %s/%s'
                         % (b.get('frio', 0), b.get('templado', 0), b.get('calido', 0), pz.get('ejemplares', 0),
                            RUTA_HOJAS, _miles(pz.get('hojas', 0)), _miles(HOJAS_TOPE)))
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
        c = cfg()
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
        e, cerca, lejos = niebla(world(), cfg(), cs['d'], cs['R'])
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
    if c['nivel'] >= 19 and tema_de(c) == 'ciudad' and W['modular'].get('activo'):
        return 1.0 - c['respiracion'] * (1.0 - W['modular']['lfo'])
    return 1.0


def luz_tiempo(k, frame=None):
    """Componente k del color de luz_principal: la luz cenital fria de la
    fase 10 tenida por la estacion del pattern (fase 17)."""
    try:
        t = _CACHE.get('tinte')
        cal = _CACHE.get('luz_calida', 0.0)       # fase 18: la escena calienta la luz
        if t is None:
            W, c = world(), cfg()
            t = tinte_actual(W, c) if c['nivel'] >= 17 else [1.0, 1.0, 1.0]
            cal = c.get('luz_calida', 0.0) if c['nivel'] >= 18 else 0.0
        k = int(k)
        return (LUZ_BASE[k] + (LUZ_CALIDA[k] - LUZ_BASE[k]) * cal) * t[k]
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
