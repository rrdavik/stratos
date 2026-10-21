# =============================================================================
# ESTRATOS - MOTOR
# =============================================================================
# Este archivo se carga dentro del Text DAT 'motor' de /project1/FASE1.
# Lo cargan los scripts de fase (fase3 ... fase10); no se ejecuta solo.
#
# Contiene TODA la logica del mundo, en dos bloques:
#
#   1. NUCLEO     Python puro: ocupacion, desbordamiento, especies, ciclo,
#                 erosion, conchas, cortes y la piel tematica (fase 11:
#                 catalogo de modelos, clusters, compuestos y transitos;
#                 fase 12: material por la velocidad, vigor por el gate;
#                 fase 13: rios y carreteras; fase 14: aranazos tematicos,
#                 escalada, incendio y derrumbes).
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

MOTOR_VERSION = 'motor v34'

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
# 4-8 aranazos.
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
TIPOS_DEFECTO = ['temblor', 'corte', 'corte profundo', 'aranazo',
                 'aranazo', 'aranazo', 'aranazo', 'aranazo']
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


def pads_corte(cfg):
    """Pads (0-7) cuyo perfil abre corte (profundidad > 0)."""
    return [k for k, p in enumerate(cfg['perfiles']) if p[2] > 0]

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
    beats_per_bar=4, umbral_madurez=0.6, umbral_novedad=0.15, compases_quietos=2,
    umbral_territorio=0.8, compases_territorio=8,
    ciclo_min=8, ciclo_max=64, cambio_entierra=0, giro_vivo=1, giro_min=0.25,
    # fase 7
    dens_umbral=0.60, rad_mult=2.0, target_mode=2,
    perfiles=PERFILES_DEFECTO, tipos=TIPOS_DEFECTO,
    # fase 8
    herencia=0.25, max_shells=24, grosor_tiempo=1, grosor_max=2.0, colmatacion=0.0,
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
    # fase 12: moduladores
    material_modo=1, rug_min=0.05, rug_max=0.85, vigor_max=1.5, plantas_ligado=2,
    gate_prueba=0.5, respaldo=0,
    # fase 13: tejido conectivo
    rios=1, carreteras=1, min_via=2, grosor_via=0.18, max_rio=12,
    # fase 14: destructores
    ventana_escalada=8, golpes_escalada=2, pasos_fuego=6, max_fuego=6, pasos_polvo=8,
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
    if i is None:                       # fuera del rango, modo ignorar
        W['ev']['ultima'] = dict(s=s, celda=-1, occ=0, estado='fuera de rango', t=now)
        return dict(estado='fuera de rango', inc=0.0, celda=-1)
    W['last'][s] = dict(note=int(note), cell=i, t=now, vel=int(vel))
    W.setdefault('terr', {})[i] = W.get('bar_n', 0)
    W['ruina'][i] = 0                   # fase 14: construir sobre la huella la borra
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
    perf = cfg['perfiles']
    pad = int(pad) % len(perf)
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
              doble=over, quitado=removed, t=now, tipo=tipo)
    W['ev']['erosion'] = ev
    if tematico:                        # fase 14: el accidente y la escalada
        destructor(W, cfg, pad, vel, now, ev, antes)
    if cfg['nivel'] >= 9:
        if depth > 0:
            ev['corte'] = cut(W, cfg, target, depth, rad, now)
        W['flash'] = dict(t=now, cell=target, k=1.0 if depth > 0 else 0.35, pad=pad)
    return ev


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
    W['ev']['corte'] = dict(celda=target, conchas=fuera_t, celdas=len(hechos), t=now,
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
BANDAS_RESERVADAS = ((55.0, 100.0), (165.0, 235.0))   # tono OKLCH: ambar SEQ2, cian cicatriz
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
    return (cfg.get('paleta', 0), cfg.get('paleta_tono'), cfg.get('paleta_croma'))


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


def end_cycle(W, cfg, now, bars=None):
    """Entierra el mundo (desde el nivel 8). bars: compases que duro; sin
    ellos, la concha tiene Shellthick."""
    W['ev']['ciclo'] = dict(t=now, n=W.get('ciclo_n', 1))
    if cfg['nivel'] < 8:
        return False
    cerrar_obras(W, cfg)                # los transitos se cierran antes de hornear
    r_in = top_radius(W, cfg)
    g = shell_grosor(cfg, bars)
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
    if piel:
        tick_piel(W, cfg, now, W['paso'], playing)
    if cfg['nivel'] >= 14:
        tick_destructores(W, cfg, now)
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
    lim = limit(cfg)
    out = dict(formas_pulidas=[], formas_porosas=[], coronas=[], estratos=[], luz_celda=[],
               luz_conchas=[])
    R = top_radius(W, cfg)
    piel = lvl >= 11
    if piel:                        # fase 11: todas las geometrias de los modelos, vacias
        for g, _, _ in geometrias_piel(cfg):
            out[g] = []
        out['particulas'] = []
    for i in range(N):
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
        pulido = W['vel'][i] >= cfg['vel_umbral']
        lst = out['formas_pulidas'] if pulido else out['formas_porosas']
        sat = W['par'][i] >= 0
        scale = cfg['sat_size'] if sat else 1.0
        base_col = COL_GEO if own == GEO else COL_ARQ
        col = _material_col(base_col, pulido)
        lt = _latido(W, i, now)
        sc = seq_color(cfg, W['lat_s'][i] if W['lat_s'][i] in (1, 2) else 1)
        Id, pd_ = drum_light(W, cfg, i, now)
        if pd_ is not None and Id >= lt:    # el golpe de bateria, igual que una nota
            lt, sc = Id, drum_color(cfg, pd_)
        if lt > 0:                  # la nota o el golpe: la formacion se enciende
            vh *= 1.0 + LATIDO_AMP * lt
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
    if piel:
        W['piel'] = build_piel(W, cfg, now, out)
    if lvl >= 13:                   # fase 13: rios y carreteras
        out['tejido'], W['tejido'] = build_tejido(W, cfg)
    if lvl >= 14:                   # fase 14: huellas y particulas de los destructores
        build_destructores(W, cfg, now, out)
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
        for s, r_in, r_out in col[first:]:
            sh = W['shells'][s]
            colr = tile_color(cfg, sh, sh['occ'][c], s)
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None:
                colr = _mix(COL_SCAR, colr, max(0.0, min(1.0, (now - t0) / st)))
            rows.append(_tile_row(c, n, r_in, r_out, colr))
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
    if old is not None and light_level(cfg, old, now) > w + 1e-9:
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
        I = min(1.0, light_level(cfg, h, now) * k)
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
        for pd in [pd for pd in pads if light_level(cfg, pads[pd], now) <= 0.0]:
            del pads[pd]
        if not pads:
            del luz[c]
    for c in sorted(set(centros) | set(luz)):
        if c >= N:
            continue
        I, pad = drum_light(W, cfg, c, now)
        lista = sorted(centros.get(c, []))
        if pad is not None and I >= max([env for _, env in lista] or [0.0]):
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
            dx = 0.0 if partes == 1 else (-0.5 + q) * lado_x * g / 2.0
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


# --- el L-system de la vegetacion (angulos de 30 grados) ---------------------
#   F  tramo de tronco o rama        f  avanza sin dibujar
#   +  -  gira 30 grados (a un lado, al otro)
#   &  ^  cabecea 30 grados (se abre, se cierra)
#   /  \  rueda 120 grados (reparte las ramas alrededor)
#   [  ]  empieza y acaba una rama (mas corta y mas fina)
#   C     copa (prisma hexagonal)    H  hoja angular (lamina)
#   D     dosel (copa ancha y plana)

def _lsistema(axioma, reglas, gen):
    s = axioma
    for _ in range(int(gen)):
        s = ''.join(reglas.get(ch, ch) for ch in s)
    return s


def _tortuga(cadena, largo=0.3, ancho=0.07, copa=0.32, k_largo=0.72, k_ancho=0.66):
    pos = (0.0, 0.0, 0.0)
    X, H, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
    pila, prims = [], []
    L, Wd, C = largo, ancho, copa
    for ch in cadena:
        if ch in 'Ff':
            b = _add(pos, H, L)
            if ch == 'F':
                prims.append(_tramo(pos, b, Wd))
            pos = b
        elif ch in '+-':
            g = 30.0 if ch == '+' else -30.0
            H, X = _girar_eje(H, Z, g), _girar_eje(X, Z, g)
        elif ch in '&^':
            g = 30.0 if ch == '&' else -30.0
            H, Z = _girar_eje(H, X, g), _girar_eje(Z, X, g)
        elif ch in '/\\':
            g = 120.0 if ch == '/' else -120.0
            X, Z = _girar_eje(X, H, g), _girar_eje(Z, H, g)
        elif ch == '[':
            pila.append((pos, X, H, Z, L, Wd, C))
            L, Wd, C = L * k_largo, Wd * k_ancho, C * 0.85
        elif ch == ']':
            pos, X, H, Z, L, Wd, C = pila.pop()
        elif ch in 'CD':
            k = (1.0, 0.62) if ch == 'C' else (1.7, 0.30)
            c = _add(pos, (0.0, 1.0, 0.0), C * k[1] * 0.25)
            yaw = math.degrees(math.atan2(H[2], H[0])) // 30 * 30
            prims.append(_hexa(c[0], c[1], c[2], C * k[0], C * k[1], 0.0, yaw, 0.0))
        elif ch == 'H':
            c = _add(pos, H, L * 0.5)
            rx, ry, rz = _euler_xyz(X, H, Z)
            prims.append(_caja(c[0], c[1], c[2], L * 0.8, L * 1.1, Wd * 0.6, rx, ry, rz))
    return prims


def _arbol(axioma, reglas, gen, **kw):
    return _a_alto_uno(_tortuga(_lsistema(axioma, reglas, gen), **kw))


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
    hoja = dict(largo=0.30, ancho=0.05)
    M['veg_brote'] = _a_alto_uno(_tortuga('F[&&H]/[&&H]/[&&H]F[&H]/[&H]/[&H]', **hoja))
    M['veg_brote2'] = _a_alto_uno(_tortuga('F[&&&H]/[&&H]/[&&H]F[&H]', **hoja))
    copa = dict(largo=0.30, ancho=0.08, copa=0.50)
    M['veg_arbol'] = _arbol('FA', {'A': '[&&FC]/[&&FC]/[&&FC]FC'}, 1, **copa)
    M['veg_arboleda'] = _arbol('FA', {'A': '[&&FA]/[&&FA]/[&FA]FC'}, 2, largo=0.34, ancho=0.09,
                               copa=0.55)
    M['veg_bosque'] = _arbol('FFA', {'A': '[&&FD]/[&&FD]/[&&FD]FD'}, 1, largo=0.30, ancho=0.09,
                             copa=0.50)
    M['veg_madre'] = _arbol('FFFFA', {'A': '[&&FA]/[&&FA]/[&&FA]FD'}, 3, largo=0.40, ancho=0.15,
                            copa=0.66, k_largo=0.68)
    M['veg_prot1'] = _arbol('FA', {'A': '[&&FA]/[&&FA]/[&&FA]C'}, 2, largo=0.36, ancho=0.10, copa=0.58)
    M['veg_prot2'] = _arbol('FFA', {'A': '[&&FA]/[&&FA]/[&&FA]FC'}, 2, largo=0.38, ancho=0.11, copa=0.70)
    M['veg_prot3'] = _arbol('FFA', {'A': '[&&FA]/[&&FA]/[&&FA]FD'}, 3, largo=0.40, ancho=0.12,
                            copa=0.62, k_largo=0.68)
    # el dosel: copas anchas y planas de la celda a la vecina (z de 0 a 1)
    M['veg_dosel'] = [_hexa(0.0, 0.5, 0.18, 0.85, 1.0), _hexa(0.08, 0.42, 0.52, 0.80, 0.84, 0.0, 30.0),
                      _hexa(-0.06, 0.55, 0.84, 0.82, 0.9)]
    # bosque sobre terrazas de basalto (el relieve coloniza la vegetacion)
    M['veg_hib'] = [_hexa(0.0, 0.08, 0.0, 1.0, 0.16), _hexa(0.10, 0.22, -0.08, 0.7, 0.14, 0.0, 30.0),
                    _hexa(-0.12, 0.34, 0.10, 0.45, 0.12)]
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
    # arboles que parten la roca (la vegetacion coloniza el relieve)
    M['rel_hib'] = _encajar(_tortuga('[&F&FC]/[&&FFC]', largo=0.28, ancho=0.06, copa=0.26), 0.9)
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
for _m in ('veg_hib', 'rel_mesetas', 'rel_meseta', 'rel_cumbre', 'rel_prot1', 'rel_prot2',
           'rel_prot3', 'inf_barrio', 'inf_prot1', 'inf_prot2', 'inf_prot3', 'inf_hib',
           'pla_manzana', 'pla_podio', 'pla_prot1', 'pla_prot2', 'pla_prot3', 'ciu_valla',
           'veg_claro', 'rel_pedregal', 'inf_escombros'):
    PIE[_m] = ('celda', 0.85)
PIE.update(rel_hib=('celda', 0.6), inf_torre=('celda', 0.6), pla_bloque=('celda', 0.75),
           pla_bloque2=('celda', 0.75), pla_plantas=('celda', 0.6), pla_rascacielos=('celda', 0.55),
           ciu_foso=('celda', 0.75), ciu_andamio=('celda', 0.9))


def _ancho_natural(m):
    b = _caja_modelo(MODELOS[m])
    return max(1e-3, b[1] - b[0], b[5] - b[4])


ANCHO = dict((m, _ancho_natural(m)) for m in MODELOS)


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


def _catalogo_defecto():
    filas = []

    def add(tema, esp, estado, cosas):
        for v, x in enumerate(cosas):
            filas.append((tema, esp, estado, v, x))
    for tema, esp, p in (('naturaleza', 'vegetacion', 'veg'), ('naturaleza', 'relieve', 'rel'),
                         ('ciudad', 'informal', 'inf'), ('ciudad', 'planificada', 'pla')):
        semilla = {'veg': ['veg_brote', 'veg_brote2'], 'rel': ['rel_columna', 'rel_columna2'],
                   'inf': ['inf_caseta', 'inf_caseta2'], 'pla': ['pla_bloque', 'pla_bloque2']}[p]
        resto = {'veg': ['veg_arbol', 'veg_arboleda', 'veg_bosque', 'veg_madre'],
                 'rel': ['rel_columnas', 'rel_mesetas', 'rel_meseta', 'rel_cumbre'],
                 'inf': ['inf_anadidos', 'inf_pasarelas', 'inf_barrio', 'inf_torre'],
                 'pla': ['pla_plantas', 'pla_manzana', 'pla_podio', 'pla_rascacielos']}[p]
        add(tema, esp, 'semilla', semilla)
        for estado, mo in zip(ESTADOS[1:], resto):
            add(tema, esp, estado, [mo])
        add(tema, esp, 'puente', ['veg_dosel' if p == 'veg' else p + '_puente'])
        add(tema, esp, 'protagonista', [p + '_prot1', p + '_prot2', p + '_prot3'])
        add(tema, esp, 'hibrido', [p + '_hib'])
    add('ciudad', 'planificada', 'remate', ['pla_aguja'])
    for tema, esp, mo in (('naturaleza', 'vegetacion', 'veg_claro'), ('naturaleza', 'relieve', 'rel_pedregal'),
                          ('ciudad', 'informal', 'inf_escombros'), ('ciudad', 'planificada', 'ciu_valla')):
        add(tema, esp, 'huella', [mo])     # fase 14: lo que deja una catastrofe
    for obra in ('valla', 'foso', 'andamio', 'grua'):
        add('ciudad', 'obra', obra, ['ciu_' + obra])
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
        if (estado.startswith('cadena') and x in ETAPAS) or x in MODELOS:
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
                   obra='mat_poroso')
FAMILIAS = ['mineral', 'dosel', 'ciudad']           # uFamilia del shader: 0, 1, 2


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
    return 'ciudad' if modelo[:3] in ('inf', 'pla') else 'mineral'


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
        g = 'mod_' + modelo if modelo.startswith('ciu_') or not doble else \
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
    bases = {}
    for i in range(N):
        bases[i] = _mul(normal_i(i), base_radius(W, cfg, i))

    doce = cfg['nivel'] >= 12         # fase 12: una geometria por modelo, rugosidad en el alfa
    respaldo = doce and cfg.get('respaldo', 0)
    arde = celdas_ardiendo(W, cfg) if cfg['nivel'] >= 14 else {}

    def emit(modelo, pulido, p, marco, dims, col, rug=1.0):
        nonlocal piezas
        fila = _fila_m(p, marco, dims[0], dims[1], dims[2], col)
        if doce:
            fila.append(1.0 if respaldo else rug)
        out.setdefault(geometria_de(modelo, pulido, not doce), []).append(fila)
        piezas += 1

    for i in range(N):
        vh = W['vh'][i]
        own = W['own'][i]
        if vh <= 0.005 or not own:
            continue
        n = normal_i(i)
        e, _, t, _ = _marco(i)
        p0 = bases[i]
        base = base_radius(W, cfg, i)
        cw, cl_ = _cell_sizes(base, i)
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
        lt = _latido(W, i, now)
        sc = seq_color(cfg, W['lat_s'][i] if W['lat_s'][i] in (1, 2) else 1)
        Id, pd_ = drum_light(W, cfg, i, now)
        if pd_ is not None and Id >= lt:
            lt, sc = Id, drum_color(cfg, pd_)
        kb, fl = rebote(cfg, W, i, now, paso)
        if lt > 0:
            vh *= 1.0 + LATIDO_AMP * lt
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
            emit(mo, pulido, p, ej, dims, ck, rug)
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
                emit(hib[0], pulido, p0, ej, dims, ch, rug)
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
    return dict(tema=tema, clusters=len(tam), max=max(tam or [0]), compuestos=compuestos,
                piezas=piezas, obras=obras, medias=medias)


# -----------------------------------------------------------------------------
# 1. NUCLEO - tejido conectivo (fase 13): rios y carreteras
# -----------------------------------------------------------------------------
# Lo que ninguna senal pide: el sistema lo deduce del estado.
#   RIOS (naturaleza)  nacen en la capital de cada cluster de relieve y bajan
#                      celda a celda hacia la vecina menos ocupada (empate:
#                      la de indice menor), sin volver atras, hasta una celda
#                      vacia, hasta otro rio (confluyen) o hasta Maxrio celdas.
#   CARRETERAS (ciudad) arbol de expansion minima (Kruskal) entre las capitales
#                      de cluster y las formaciones sueltas con ocupacion de
#                      Minvia o mas; cada arista, el camino mas corto por la
#                      reticula.
# Los tramos van de centro a centro de celda, a ras del suelo (por debajo de
# las formaciones), en dos medios tramos que siguen la curva del planeta. Se
# recalculan solo cuando cambia la ocupacion.

COL_RIO = (0.12, 0.26, 0.56)       # azul profundo (fuera del cian de la cicatriz)
COL_VIA = (0.17, 0.17, 0.19)       # asfalto
RUG_RIO, RUG_VIA = 0.05, 0.75      # el agua brilla; el asfalto, mate
TEJIDO_LIFT = 0.006                # sobre el suelo de la celda
TEJIDO_ALTO = 0.035
_TEJIDO = {}


def rios(W, cfg, cl=None):
    """[[celdas del rio], ...] y {celda: celda aguas abajo}. Los rios se trazan
    por orden de capital; uno que llega a otro rio confluye y acaba ahi."""
    cl = cl or clusters(W, cfg)
    fuentes = sorted(cl['capital'][k] for k in cl['capital']
                     if W['own'][cl['capital'][k]] == ARQ)
    lista, abajo = [], {}
    tope = max(1, int(cfg['max_rio']))
    for f in fuentes:
        if f in abajo:                  # la capital ya esta en otro rio
            continue
        camino = [f]
        while len(camino) <= tope:
            c = camino[-1]
            libres = [j for j in NEIGH[c] if j not in camino]
            if not libres:
                break
            j = min(libres, key=lambda x: (W['occ'][x], x))
            camino.append(j)
            if W['occ'][j] <= 0 or j in abajo or any(j in r for r in lista):
                break                   # celda vacia o confluencia
        if len(camino) < 2:
            continue
        for a, b in zip(camino, camino[1:]):
            abajo.setdefault(a, b)
        lista.append(camino)
    return lista, abajo


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


def nodos_via(W, cfg, cl=None):
    """Capitales de cluster y formaciones sueltas (sin satelites) con ocupacion
    de Minvia o mas."""
    cl = cl or clusters(W, cfg)
    nodos = set(cl['capital'].values())
    for i in range(N):
        if W['occ'][i] >= cfg['min_via'] and W['par'][i] < 0 and cl['de'][i] < 0:
            nodos.add(i)
    return sorted(nodos)


def carreteras(W, cfg, cl=None):
    """(aristas del arbol [(a, b, distancia)], tramos [(c, d)]): Kruskal sobre
    las distancias por la reticula entre los nodos."""
    nodos = nodos_via(W, cfg, cl)
    pares = []
    for k, a in enumerate(nodos):
        for b in nodos[k + 1:]:
            pares.append((len(camino_corto(a, b)) - 1, a, b))
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
        camino = camino_corto(a, b)
        for c, e in zip(camino, camino[1:]):
            if (c, e) not in tramos and (e, c) not in tramos:
                tramos.append((c, e))
    return arbol, tramos


def tejido(W, cfg):
    """Topologia del tejido (se guarda: solo se recalcula si cambia la
    ocupacion). dict(rios, abajo, caudal, arbol, vias)."""
    tema = tema_de(cfg)
    clave = (tuple(W['occ']), tuple(W['own']), tuple(W['par']), tema, cfg['rios'], cfg['carreteras'],
             cfg['min_via'], cfg['max_rio'], cfg['umbral_vecindad'], cfg['peso_vecina'],
             cfg['min_cluster'], cfg['th_fusion'], GRID['lo'], GRID['hi'])
    if _TEJIDO.get('clave') == clave:
        return _TEJIDO['t']
    t = dict(rios=[], abajo={}, caudal={}, arbol=[], vias=[])
    cl = clusters(W, cfg)
    if tema == 'naturaleza' and cfg['rios']:
        t['rios'], t['abajo'] = rios(W, cfg, cl)
        t['caudal'] = _caudal(t['rios'], t['abajo'])
    if tema == 'ciudad' and cfg['carreteras']:
        t['arbol'], t['vias'] = carreteras(W, cfg, cl)
    _TEJIDO['clave'], _TEJIDO['t'] = clave, t
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
    filas = []
    w = cfg['grosor_via']
    for (a, b), q in sorted(t['caudal'].items()):
        _tramo_suelo(W, cfg, a, b, w * (0.7 + 0.3 * q), COL_RIO, RUG_RIO, filas)
    for a, b in t['vias']:
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
    """Un pad sin profundidad (no corta): los de la fase 14."""
    return int(pad) not in pads_corte(cfg)


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
    extra = ['i_tejido'] if c['nivel'] >= 13 else []
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
    """(perfiles, tipos) de la tabla perfiles_erosion, leidos por nombre de
    columna (la columna rol es solo para leer)."""
    t = parent().op('perfiles_erosion')
    if t is None or t.numRows < 2:
        return list(PERFILES_DEFECTO), list(TIPOS_DEFECTO)
    out, tipos = [], []
    for r in range(1, min(t.numRows, 9)):
        try:
            p = (int(float(t[r, 'reduccion'].val)), int(float(t[r, 'radio'].val)),
                 int(float(t[r, 'profundidad'].val)))
        except Exception:
            p = PERFILES_DEFECTO[r - 1]
        out.append(p)
        try:
            tp = t[r, 'tipo'].val.strip()
        except Exception:
            tp = ''
        tipos.append(tp or tipo_perfil(*p))
    while len(out) < 8:
        out.append(PERFILES_DEFECTO[len(out)])
        tipos.append(TIPOS_DEFECTO[len(tipos)])
    return out, tipos


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
        colmatacion=max(0.0, min(1.0, _p('Colmatacion', c['colmatacion']))),
        scar_time=max(0.1, _p('Cicatriz', c['scar_time'])),
        flash=_p('Destello', c['flash']),
    )
    if c['nivel'] >= 7:
        c['perfiles'], c['tipos'] = _perfiles()
        c['colores_drum'] = _colores_drum()
        c.update(balizas_drum=int(_p('Balizasdrum', True)),
                 luz_drum=_p('Luzdrum', c['luz_drum']),
                 erosion_vel=int(_p('Erosionvel', True)),
                 vel_ref=_p('Velref', c['vel_ref']),
                 vida_baliza_drum=_p('Vidabalizadrum', c['vida_baliza_drum']))
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
                 catalogo=_catalogo())
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
                 max_rio=max(1, int(_p('Maxrio', c['max_rio']))))
    if c['nivel'] >= 14:
        c.update(ventana_escalada=max(1, int(_p('Ventanaescalada', c['ventana_escalada']))),
                 golpes_escalada=max(1, int(_p('Golpesescalada', c['golpes_escalada']))),
                 pasos_fuego=max(1, int(_p('Pasosfuego', c['pasos_fuego']))),
                 max_fuego=max(1, int(_p('Maxfuego', c['max_fuego']))),
                 pasos_polvo=max(1, int(_p('Pasospolvo', c['pasos_polvo']))))
    return c


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
    res = tick(W, c, now, tempo(), playing())
    if res.get('burst'):
        print('AVISO  %s' % W['aviso'])
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
    W['dirty'] = False


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


# --- camara (motor v24; encuadre cercano, v33) -----------------------------------
# Por defecto, camara de GLOBO: mira al centro, en la direccion de referencia
# (+Z, hacia la que se balancea el eje), y encuadra el planeta entero tan
# cerca como permite el cuadro, con Holguraaltura de la altura maxima para las
# construcciones. El encuadre solo cambia cuando el planeta engorda (una
# concha nueva): crecer, erosionar o el latido no mueven la camara. (La v32
# perseguia lo que se dibujaba y la camara no paraba quieta.) La de
# SUPERFICIE (fase 10 v4) queda como modo (Modocamara).

CAM_DIR = (0.0, 0.0, 1.0)          # direccion de referencia de la camara
CAM_TRANS = 20.0                   # segundos de Planofinal y del cambio de modo
HOLGURA_ALTURA = 0.4               # fraccion de la altura maxima que se encuadra
CAJA_EXT = (0.5, 1.0, 0.5)         # semiejes de la caja de las geometrias (base en y = 0)
SIN_EXTENSION = ('estratos', 'luz_conchas')     # no pasan de la superficie
_EXT = {}


def altura_max(cfg):
    """Lo mas alto que llega, sobre su suelo, algo que gira con el planeta:
    una formacion en el limite hinchada por el latido y, encima, la corona
    mas larga (la de una torre en su ultimo tramo de cumbre)."""
    lim = limit(cfg)
    corona = 0.90 * (1.0 + 0.25 * max(0, int(cfg['cumbre_tramos']))) * lim
    return lim * (1.0 + LATIDO_AMP) + corona


def radio_encuadre(W, cfg, holgura=None):
    """Radio que se encuadra: el nominal mas 'holgura' (Holguraaltura, 0,4)
    por la altura maxima. Con 1, todo lo que podria llegar a crecer (el
    encuadre de la v24 a la v31); con 0, solo el planeta. Solo cambia cuando
    el planeta engorda (los suelos nunca pasan del nominal)."""
    if holgura is None:
        holgura = _p('Holguraaltura', HOLGURA_ALTURA)
    return top_radius(W, cfg) + max(0.0, min(1.0, float(holgura))) * altura_max(cfg)


def _ext_modelo(modelo):
    """Semiejes (x, y, z) de un modelo del catalogo, desde su origen."""
    v = _EXT.get(modelo)
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
    la leyenda: dice si Holguraaltura deja fuera algo): la superficie (con la
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
    # globo: persigue el encuadre (solo cambia con una concha nueva o los
    # parametros) en Camsuave s; el planeta nunca se sale del cuadro
    Re = radio_encuadre(W, c)
    fov, metodo, aspect = _cam_optics()
    margen = max(1.0, _p('Encuadremargen', 1.02))
    suave = max(0.0, _p('Camsuave', 3.0))
    d_obj, _, th = globe_distance(Re, fov, aspect, margen, metodo)
    d_min = globe_distance(R + 0.2, fov, aspect, 1.0, metodo)[1]
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
    sup = c['nivel'] >= 10 and str(_p('Modocamara', 'globo')) == 'superficie' \
        and not _p('Planofinal', False)
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
              fov=fov, metodo=metodo, aspect=aspect, margen=margen, w=s, near=near, far=far,
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
        if e:
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
        lines.append('  CONCHAS  %d   radio %.2f   ultima %s   laguna max %s   colmatacion %d%%'
                     '   herencia %d%%   continentes %d'
                     % (n_shells(W), top_radius(W, c), ult, lag, int(round(c['colmatacion'] * 100)),
                        int(c['herencia'] * 100), continents(W)))
    if lvl >= 8:
        try:
            cs = camera_state()
            lado = 'vertical' if cs['theta'] <= fovs(cs['fov'], cs['aspect'], cs['metodo'])[0] - 1e-9 \
                else 'horizontal'
            inst = _CACHE.get('inst')
            vis = radio_visible(inst, W, c) if inst else cs['R']
            lines.append('  CAMARA   %s   dist %.1f -> %.1f   radio encuadre %.2f (lo dibujado llega a %.2f)'
                         '   fov %.0f (%s; manda el %s)   margen %.2f'
                         % (cs['modo'], cs['d'], cs['d_obj'], cs['Re'], vis, cs['fov'],
                            'vertical' if 'vert' in cs['metodo'] else 'horizontal', lado,
                            cs['margen']))
        except Exception:
            pass
    if lvl >= 9:
        k = W['ev'].get('corte')
        if k:
            left = max(0.0, c['scar_time'] - (absTime.seconds - k['t']))
            lines.append('  CORTE    celda %d   %d losetas   suelo %.2f   laguna %.2f   cicatriz %.1f s'
                         % (k['celda'], k['conchas'], k.get('suelo', 0.0), k.get('laguna', 0.0), left))
            if k.get('nucleo') is not None:
                lines.append('  CORTE    celda %d   nucleo alcanzado' % k['nucleo'])
    if lvl >= 11:
        pz = W.get('piel') or {}
        lines.append('  TEMA     %s   clusters %d (max %d)   compuestos %d   piezas %d   obras %d (%d a medias)'
                     % (tema_de(c), pz.get('clusters', 0), pz.get('max', 0), pz.get('compuestos', 0),
                        pz.get('piezas', 0), pz.get('obras', 0), pz.get('medias', 0)))
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
        lines.append('  TEJIDO   rios %d (%d tramos)   carreteras %d tramos'
                     % (tj.get('rios', 0), tj.get('tramos_rio', 0), tj.get('tramos_via', 0)))
    if lvl >= 14:
        lines.append(_legend_escalada(W, c))
    return '\n'.join(lines)


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
