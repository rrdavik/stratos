# =============================================================================
# ESTRATOS - MOTOR
# =============================================================================
# Este archivo se carga dentro del Text DAT 'motor' de /project1/FASE1.
# Lo cargan los scripts de fase (fase3 ... fase10); no se ejecuta solo.
#
# Contiene TODA la logica del mundo, en dos bloques:
#
#   1. NUCLEO     Python puro: ocupacion, desbordamiento, especies, ciclo,
#                 erosion, conchas y cortes. No toca TouchDesigner.
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

MOTOR_VERSION = 'motor v21'

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
    beats_per_bar=4, umbral_madurez=0.6, umbral_novedad=0.05, compases_quietos=4,
    ciclo_min=8, ciclo_max=64, cambio_entierra=0, giro_vivo=1, giro_min=0.25,
    # fase 7
    dens_umbral=0.60, rad_mult=2.0, target_mode=2,
    perfiles=PERFILES_DEFECTO, tipos=TIPOS_DEFECTO,
    # fase 8
    herencia=0.25, max_shells=24, grosor_tiempo=1, grosor_max=2.0,
    # fase 9
    scar_time=4.0, flash=3.0,
    # fase 7: luz de la bateria en las celdas que golpea
    balizas_drum=1, luz_drum=1.0, vida_baliza_drum=0.8, luz_seq=1,
    erosion_vel=1, vel_ref=100,
    colores_drum=COLORES_DRUM,
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
        hueco=[0] * N,      # conchas retiradas por un corte en esta celda
        resto=[0.0] * N,    # fraccion de herencia acumulada
        gen=0,
        shells=[],
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
        ciclo_t0=None,          # instante en que empezo el mundo actual
        marcha=False,           # el reloj del ciclo avanza
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
    """[(radio interior, radio exterior)] de cada concha, de dentro afuera."""
    r = cfg['core_radius']
    out = []
    for sh in W['shells']:
        g = shell_th(sh, cfg)
        out.append((r, r + g))
        r += g
    return out


def top_radius(W, cfg):
    return cfg['core_radius'] + sum(shell_th(sh, cfg) for sh in W['shells'])


def base_radius(W, cfg, i):
    k = W['hueco'][i]
    if k <= 0:
        return top_radius(W, cfg)
    return top_radius(W, cfg) - sum(shell_th(sh, cfg) for sh in W['shells'][-k:])


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
    res = grow(W, cfg, i, s, vel, now)
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


def bar_tick(W, cfg):
    """Un compas del reloj del ciclo. Devuelve el motivo de cierre o None."""
    foto = snapshot(W, cfg)
    nov, mat = measure(W, cfg, foto)
    W['foto_anterior'] = foto
    W['novedad'], W['madurez'] = nov, mat
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
    if n >= cmax:
        return 'edad maxima'
    return None


def close_cycle(W, cfg, now, motivo):
    """Cierra el mundo: emite fin_de_ciclo y, desde el nivel 8, lo entierra."""
    bars = W['compases_ciclo']
    t0 = W.get('ciclo_t0')
    ev = dict(ciclo=W['ciclo_n'], compases=bars,
              segundos=max(0.0, now - t0) if t0 is not None else 0.0,
              motivo=motivo, madurez=W['madurez'], novedad=W['novedad'], t=now)
    if end_cycle(W, cfg, now, bars):
        ev['grosor'] = shell_th(W['shells'][-1], cfg)
        W['foto_anterior'] = snapshot(W, cfg)
    W['aviso'] = 'fin de ciclo %d: %s a los %d compases' % (ev['ciclo'], motivo, bars)
    W['compases_ciclo'] = 0
    W['quietos'] = 0
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
    if cfg['nivel'] >= 9:
        if depth > 0:
            ev['corte'] = cut(W, cfg, target, depth, rad, now)
        W['flash'] = dict(t=now, cell=target, k=1.0 if depth > 0 else 0.35, pad=pad)
    return ev


def _top_removed(W, c):
    k = 0
    for sh in reversed(W['shells']):
        if sh['rm'][c]:
            k += 1
        else:
            break
    return k


def cut(W, cfg, target, depth, rad, now):
    ns = n_shells(W)
    if ns == 0:
        return 0
    cells = []
    deepest = 0
    for c, d in rings(target, rad):
        dd = min(int(depth) - d, ns)
        if dd <= 0:
            continue
        for s in range(ns - dd, ns):
            W['shells'][s]['rm'][c] = 1
        W['hueco'][c] = _top_removed(W, c)
        _clear_cell(W, c)
        W['huella'][c] = 0.0
        for j in NEIGH[c]:
            if W['par'][j] == c:
                W['par'][j] = -1
        cells.append(c)
        deepest = max(deepest, W['hueco'][c])
    # cicatrices: suelo del corte y paredes que han quedado al aire
    for c in cells:
        h = W['hueco'][c]
        floor = ns - 1 - h
        if floor >= 0:
            W['scars'][floor * 1000 + c] = now
        for j in NEIGH[c]:
            for s in range(ns - h, ns):
                if not W['shells'][s]['rm'][j]:
                    W['scars'][s * 1000 + j] = now
    W['dirty'] = True
    W['ev']['corte'] = dict(celda=target, conchas=deepest, celdas=len(cells), t=now)
    return deepest


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
    return MINERAL[int(gen) % len(MINERAL)]


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
    r_in = top_radius(W, cfg)
    g = shell_grosor(cfg, bars)
    W['shells'].append(dict(gen=W['gen'], col=list(shell_color(W['gen'])),
                            occ=list(W['occ']), sp=list(W['sp']), rm=[0] * N,
                            grosor=g, r_in=r_in, r_out=r_in + g))
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
        W['hueco'][i] = 0
    W['pend'] = {}
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
    for i in range(N):
        h, vh = W['h'][i], W['vh'][i]
        if vh != h:
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
    out = dict(formas_pulidas=[], formas_porosas=[], coronas=[], estratos=[], luz_celda=[])
    R = top_radius(W, cfg)
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
    out['luz_celda'] = cell_lights(W, cfg, now)  # parte del mundo: tambien en actuacion
    if lvl >= 8 and tiles:
        out['estratos'] = build_tiles(W, cfg, now)
    return out


def build_tiles(W, cfg, now):
    rows = []
    ns = n_shells(W)
    first = max(0, ns - int(cfg['max_shells']))
    st = cfg['scar_time']
    radii = shell_radii(W, cfg)
    for s in range(first, ns):
        sh = W['shells'][s]
        r_in, r_out = radii[s]
        th = r_out - r_in
        r_mid = 0.5 * (r_in + r_out)
        base_col = sh['col']
        for c in range(N):
            if sh['rm'][c]:
                continue
            n = normal_i(c)
            col = _tint(base_col, 0.75 + 0.35 * min(1.0, sh['occ'][c] / 4.0))
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None:
                col = _mix(COL_SCAR, col, max(0.0, min(1.0, (now - t0) / st)))
            cw, cl = _cell_sizes(r_mid, c)
            if is_pole(c):
                cw, cl = cw * 1.25, cl * 1.25
            rows.append(_row(_mul(n, r_mid - th * 0.5), n, cw * 1.04, th * 0.98, cl * 1.04, col))
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


# =============================================================================
# 2. ADAPTADOR TOUCHDESIGNER
# =============================================================================
# Todo lo de aqui abajo usa op(), parent(), me y absTime: solo funciona
# dentro de TouchDesigner.

_CACHE = {'frame': None, 'inst': None, 'printed': {}}

CHOP_NAMES = ['i_formas_pulidas', 'i_formas_porosas', 'i_coronas',
              'i_estratos', 'i_luz_celda']

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
        ciclo_min=_p('Ciclomin', c['ciclo_min']),
        ciclo_max=_p('Ciclomax', c['ciclo_max']),
        cambio_entierra=int(_p('Cambioentierra', False)),
        giro_vivo=int(_p('Girovivo', True)),
        giro_min=_p('Giromin', c['giro_min']),
        dens_umbral=_p('Umbraldensidad', c['dens_umbral']),
        rad_mult=_p('Multradio', c['rad_mult']),
        target_mode=_menu('Objetivo', TARGET_MODES, 2),
        herencia=_p('Herencia', c['herencia']),
        max_shells=_p('Maxconchas', c['max_shells']),
        grosor_tiempo=int(_p('Grosortiempo', True)),
        grosor_max=_p('Grosormax', c['grosor_max']),
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
    W, c = world(), cfg()
    hidden = max(0, n_shells(W) - int(c['max_shells']))
    return c['core_radius'] + sum(shell_th(sh, c) for sh in W['shells'][:hidden])


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

CICLOS_COLS = ['ciclo', 'compases', 'segundos', 'motivo', 'madurez', 'novedad', 'grosor']
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
        t.appendRow([ev['ciclo'], ev['compases'], '%.1f' % ev['segundos'], ev['motivo'],
                     '%.2f' % ev['madurez'], '%.2f' % ev['novedad'],
                     '%.3f' % ev['grosor'] if 'grosor' in ev else ''])
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
    dirty = W.get('dirty', True) or _CACHE.get('tiles') is None
    inst = build_instances(W, c, now, hide_beacons=performance(), tiles=dirty)
    if dirty:
        _CACHE['tiles'] = inst['estratos']
    else:
        inst['estratos'] = _CACHE['tiles']
    _CACHE['inst'] = inst
    _CACHE['frame'] = absTime.frame
    for name in CHOP_NAMES:
        o = parent().op(name)
        if o is None:
            continue
        if name == 'i_estratos' and not dirty:
            continue
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

def on_pulse(name):
    W, c = world(), cfg()
    now = absTime.seconds
    if name == 'Sembrar':
        note = _p('Nota', 60)
        _seq1_beacon(note)
        r = note_on(W, c, GEO, note, _p('Velprueba', 100), now, tempo())
        ci = r['celda']
        print('SEMBRAR  %s -> celda %d  ocupacion %d  carga %d/%d  (%s)'
              % (note_name(note), ci, W['occ'][ci] if ci >= 0 else 0, W['carga'][ci] if ci >= 0 else 0,
                 cost(c, W['occ'][ci]) if ci >= 0 else 0, r['estado']))
    elif name == 'Sembrar2':
        note = _p('Nota2', 60)
        r = note_on(W, c, ARQ, note, _p('Velprueba', 100), now, tempo())
        ci = r['celda']
        print('SEMBRAR2 %s -> celda %d  ocupacion %d  carga %d/%d  (%s)'
              % (note_name(note), ci, W['occ'][ci] if ci >= 0 else 0, W['carga'][ci] if ci >= 0 else 0,
                 cost(c, W['occ'][ci]) if ci >= 0 else 0, r['estado']))
    elif name == 'Erosionar':
        ev = erosion(W, c, _p('Padprueba', 1) - 1, _p('Velprueba', 100), now)
        print('EROSION  pad %d (%s) -> celda %d, radio %d, notas deshechas %d'
              % (ev['pad'] + 1, ev['tipo'], ev['celda'], ev['rad'], ev['quitado']))
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
    d = top_radius(W, c) + 4.0
    return (v[0] * d, v[1] * d, v[2] * d, c['flash'] * env) + tuple(flash_color(W, c))


def flash_value(k, frame=None):
    return flash_light()[k]


def camera_state():
    if _CACHE.get('cam_frame') == absTime.frame:
        return _CACHE['cam']
    R = surface_radius()
    t = absTime.seconds
    h = _p('Camaltura', 4.0)
    vel = _p('Camvel', 0.6)
    final = _p('Planofinal', False)
    fb = _CACHE.get('cam_final', 0.0)
    last = _CACHE.get('cam_t', t)
    dt = max(0.0, min(0.25, t - last))
    fb += (1.0 if final else -1.0) * dt / 20.0
    fb = max(0.0, min(1.0, fb))
    _CACHE['cam_final'] = fb
    _CACHE['cam_t'] = t
    s = fb * fb * (3 - 2 * fb)
    az = math.radians(vel * t)
    el = math.radians(12.0 + 8.0 * math.sin(t * 0.05))
    def sph(a, e, r):
        return (r * math.cos(e) * math.cos(a), r * math.sin(e), r * math.cos(e) * math.sin(a))
    hh = h + (2.2 * R - h) * s
    pos = sph(az, el, R + hh)
    tgt = sph(az + math.radians(25.0), el - math.radians(6.0), R)
    tgt = _mul(tgt, 1.0 - s)
    st = dict(pos=pos, tgt=tgt, R=R)
    _CACHE['cam'] = st
    _CACHE['cam_frame'] = absTime.frame
    return st


def cam(key, k, frame=None):
    return camera_state()[key][k]


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
        lines.append('  CICLO    %d   %s   madurez %d%%   novedad %d%%   quieto %d/%d%s'
                     % (W['ciclo_n'], pos, int(round(W['madurez'] * 100)),
                        int(round(W['novedad'] * 100)), W['quietos'],
                        int(c['compases_quietos']), giro))
        if W['cambio_pendiente']:
            lines.append('           cambio de pattern: se enterrara al llegar a %d compases' % cmin)
        if W.get('aviso'):
            lines.append('  AVISO    %s' % W['aviso'])
    if lvl >= 7:
        e = W['ev'].get('erosion')
        dens = occupied(W) / float(N)
        flag = '  x%g' % c['rad_mult'] if dens > c['dens_umbral'] else ''
        if e:
            lines.append('  EROSION  pad %d   %s   -%.1f notas   radio %d   celda %d   densidad %d%%%s'
                         % (e['pad'] + 1, e.get('tipo', '-'), e.get('notas', e['red']), e['rad'],
                            e['celda'], int(dens * 100), flag))
        else:
            lines.append('  EROSION  -   densidad %d%%%s' % (int(dens * 100), flag))
    if lvl >= 8:
        ult = '%.2f' % shell_th(W['shells'][-1], c) if W['shells'] else '-'
        lines.append('  CONCHAS  %d   radio %.2f   ultima %s   herencia %d%%   continentes %d'
                     % (n_shells(W), top_radius(W, c), ult, int(c['herencia'] * 100),
                        continents(W)))
    if lvl >= 9:
        k = W['ev'].get('corte')
        if k:
            left = max(0.0, c['scar_time'] - (absTime.seconds - k['t']))
            lines.append('  CORTE    celda %d   %d conchas expuestas   cicatriz %.1f s'
                         % (k['celda'], k['conchas'], left))
    return '\n'.join(lines)
