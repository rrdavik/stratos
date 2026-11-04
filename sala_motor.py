# =============================================================================
# ESTRATOS - SALA VIRTUAL: MOTOR
# =============================================================================
# Este archivo se carga dentro del Text DAT 'sala_motor' de /project1/SALA.
# Lo carga sala_virtual.py; no se ejecuta solo. No es una fase de Estratos ni
# toca su mundo: es una maqueta de la instalacion que habla con FASE1 por los
# mismos sitios que el hardware real.
#
#   SALA        8 x 6 m y 4 de alto (Ancho, Fondo, Alto). Origen en el centro
#               del suelo; x a la derecha y z hacia la entrada, mirando desde
#               ella; y hacia arriba. La entrada, en el centro de la pared de
#               delante (z = Fondo / 2); el fondo de la sala, z = -Fondo / 2.
#   EQUIPOS     la tabla 'equipos' (nombre, tipo, posicion, a donde apunta,
#               tamano): la esfera de LEDs en una esquina del fondo, cuatro
#               altavoces colgados, el subwoofer bajo la esfera, el microfono
#               en lo alto, la camara cenital, cuatro focos de bano y un
#               estroboscopio. Un foco mas es una fila mas.
#   PERSONAS    Personas visitantes que entran por la puerta, pasean entre
#               puntos de la sala, se paran y se van, sin azar: un hash de la
#               persona y del tramo decide cada paso.
#   MICROFONO   el audio que oye el microfono virtual: los pasos, las palmadas
#               y las toses de cada persona, el drone de los cuatro altavoces y
#               el subwoofer y el clic del estroboscopio, cada uno atenuado por
#               su distancia al microfono (1/d) y con su retardo (d / 343 m/s).
#               Sale por el Script CHOP 'audio_mic'; Estratos lo lee con
#               Fuentemic = chop.
#   LUZ         cada foco y el estroboscopio es una Light COMP. Con Modoluz =
#               prueba recorren los tres estados de la fase 23 en un minuto:
#               deposito (ambar tenue que respira), tension (sube y vira a
#               blanco frio) y erosion dominante (estroboscopio blanco, como
#               mucho 3 destellos por segundo).
#   CAMARA      la vista libre (orbita alrededor de la sala) y la cenital,
#               desde la camara de la tabla, con su imagen de profundidad para
#               la fase 22.
#   v2, ESTAR EN LA SALA
#               Vista = visitante (por defecto): los ojos de un visitante, a
#               1,65 m, que pasea despacio entre el publico mirando la esfera;
#               entrada: de pie junto a la puerta; orbita (la libre de la v1)
#               y cenital. Los haces de los focos y del estrobo se ven en la
#               bruma (Bruma), la esfera ilumina la sala con el color medio de
#               lo que muestra, el publico tiene cabeza y sombra, y un plano
#               cenital y un rotulo completan el monitor (monitor_sala).
#   v3, LA SALA DIBUJADA
#               Vista = entrada (por defecto): desde detras de la puerta y por
#               encima de la gente, mirando al fondo, con la esfera en su
#               esquina. El suelo del publico (Zonaancho x Zonafondo) se
#               delimita con una tarima, un borde claro y una reticula de
#               0,5 m; el publico se para dentro. Las aristas de la sala, el
#               umbral de la puerta y una reticula de 1 m en suelo y paredes
#               (geometria 'lineas', Constant MAT) dan la perspectiva aunque
#               la sala este a oscuras.
#   v4          la esfera, a 1 m de cada pared de su esquina; la reticula de
#               0,5 m cubre todo el suelo; el publico, sin cabeza (un tronco);
#               Demo elige la visita (paseo, grupo, llena, goteo, vacia) y
#               Luzesfera la luz de la esfera sobre la sala (0: apagada).
# =============================================================================

SALA_VERSION = 'sala v6'

import math

VEL_SONIDO = 343.0          # m/s
RATE = 44100
TIPOS = ['esfera', 'altavoz', 'sub', 'micro', 'camara', 'foco', 'estrobo']
COLS_EQUIPOS = ['nombre', 'tipo', 'x', 'y', 'z', 'ax', 'ay', 'az', 'tam', 'notas']
INST_CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']
DUMMY_ROW = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]

VELOCIDAD = 0.9             # m/s al andar
PASO = 0.55                 # s entre dos pisadas
RANURA = 0.5                # s: cada persona puede hacer un ruido por ranura
MARGEN = 0.6                # m de las paredes
APARTE = 1.2                # m que las personas dejan alrededor de la esfera y el estrobo
BOCA = 1.5                  # m: de donde salen la voz y las palmas
CICLO_PRUEBA = 60.0         # s: deposito, tension y erosion dominante, un tercio cada uno
DESTELLO = 0.03             # s que dura un destello del estrobo
MAX_HZ = 3.0                # tope duro de destellos por segundo (WCAG 2.3.1)
OJOS = 1.65                 # m: la altura de la camara del visitante
VEL_VISITANTE = 0.45        # m/s: el visitante pasea mas despacio que el publico
PARADA_VISITANTE = 9.0      # s que se para en cada punto
PUNTOS_VISITANTE = 6        # puntos de su paseo (vuelve a empezar)
HAZ_MAX = 8.0               # m: largo maximo de un haz de luz
HAZ_K = 0.10                # brillo de un haz con Bruma 1 y el foco a tope
COL_ESFERA_DEF = (0.35, 0.55, 0.75)     # la luz de la esfera si no se puede medir su imagen

AMBAR = (1.00, 0.55, 0.15)
BLANCO_FRIO = (0.80, 0.90, 1.00)
BLANCO = (1.0, 1.0, 1.0)

COL_SUELO = (0.10, 0.10, 0.11)
COL_PARED = (0.17, 0.17, 0.18)
COL_ZONA = (0.10, 0.38, 0.42)
COL_PUERTA = (0.55, 0.40, 0.12)
COL_TARIMA = (0.07, 0.17, 0.19)         # v3: el suelo del publico, algo mas claro que el resto
# v3: las lineas (Constant MAT: se ven aunque la sala este a oscuras)
LIN_ARISTA = (0.55, 0.55, 0.58)         # las aristas de la sala
LIN_PARED = (0.16, 0.16, 0.18)          # la reticula de 1 m en paredes y suelo
LIN_ZONA = (0.10, 0.50, 0.55)           # el borde de la zona de la camara cenital (v6: mas tenue)
LIN_GRID = (0.06, 0.32, 0.35)           # su reticula
GRID_ZONA = 0.5                         # m entre dos lineas de la reticula del publico
GRID_SALA = 1.0                         # m entre dos lineas de la reticula de la sala
GROSOR = 0.07                           # m: el grueso de una arista (mas que la pared, 0,05: si no, queda dentro)
PUERTA_ANCHO = 1.2
ESFERA_MARGEN = 1.0                     # v4: m entre la esfera y cada pared de su esquina
COL_EQUIPO = dict(altavoz=(0.05, 0.05, 0.06), sub=(0.05, 0.05, 0.06), micro=(0.75, 0.75, 0.78),
                  camara=(0.35, 0.35, 0.38), foco=(0.20, 0.20, 0.22), estrobo=(0.30, 0.30, 0.32),
                  esfera=(0.22, 0.22, 0.24))
TAM_EQUIPO = dict(altavoz=(0.32, 0.50, 0.30), sub=(0.60, 0.50, 0.60), micro=(0.06, 0.18, 0.06),
                  camara=(0.28, 0.08, 0.12), foco=(0.22, 0.28, 0.22), estrobo=(0.40, 0.16, 0.20))


def equipos_defecto(ancho=8.0, fondo=6.0, alto=4.0):
    """Las filas de la tabla 'equipos' para una sala de ancho x fondo x alto:
    la esfera (1 m, sobre una peana de 0,8 m) en la esquina del fondo a la
    izquierda, a ESFERA_MARGEN (1 m) de cada pared (v4), con el sub dentro de la peana, cuatro altavoces colgados en las
    esquinas a 3 m, el microfono en lo alto hacia el centro y lejos de la
    esfera y del estrobo, la camara cenital a 3,5 m en el centro, cuatro focos
    de bano colgados que apuntan al suelo y al publico (dos acompanan a la
    esfera, sin apuntarle) y el estroboscopio en el suelo junto a la esfera."""
    hx, hz = ancho / 2.0, fondo / 2.0
    colg = min(3.0, alto - 0.6)                 # altavoces y microfono
    techo = alto - 0.4                          # focos
    m = ESFERA_MARGEN + 0.5                     # v4: 1 m entre la esfera (1 m) y cada pared
    ex, ez = -hx + m, -hz + m                   # la esfera
    filas = [
        ['esfera', 'esfera', ex, 1.3, ez, ex, 1.3, ez + 1.0, 1.0, 'LEDs, 1 m; peana de 0,8 m'],
        ['sub', 'sub', ex, 0.25, ez, 0.0, 0.25, 0.0, 0.6, 'dentro de la peana de la esfera'],
        ['altavoz1', 'altavoz', -hx + 0.4, colg, -hz + 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, fondo izquierda'],
        ['altavoz2', 'altavoz', hx - 0.4, colg, -hz + 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, fondo derecha'],
        ['altavoz3', 'altavoz', -hx + 0.4, colg, hz - 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, entrada izquierda'],
        ['altavoz4', 'altavoz', hx - 0.4, colg, hz - 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, entrada derecha'],
        ['micro', 'micro', 1.0, colg, 1.0, 1.0, 0.0, 1.0, 0.18, 'en lo alto, lejos de la esfera y del estrobo'],
        ['camara', 'camara', 0.0, min(3.5, alto - 0.2), 0.0, 0.0, 0.0, 0.0, 0.28, 'cenital (Femto Bolt)'],
        ['foco1', 'foco', ex - 0.6, techo, ez + 1.6, ex + 0.6, 0.0, ez + 3.6, 50.0,
         'bano, junto a la esfera (no le apunta)'],
        ['foco2', 'foco', ex + 1.6, techo, ez - 0.6, ex + 3.6, 0.0, ez + 0.6, 50.0,
         'bano, junto a la esfera (no le apunta)'],
        ['foco3', 'foco', hx - 2.0, techo, -hz + 1.5, hx - 2.0, 0.0, -hz + 2.5, 50.0, 'bano, al suelo'],
        ['foco4', 'foco', 0.0, techo, hz - 1.5, 0.0, 0.0, hz - 2.5, 50.0, 'bano, al publico'],
        ['estrobo', 'estrobo', ex + 1.2, 0.3, ez - 0.4, 0.0, 1.5, 0.0, 100.0, 'en el suelo, junto a la esfera'],
    ]
    return [[f[0], f[1]] + ['%g' % round(float(v), 3) for v in f[2:9]] + [f[9]] for f in filas]


# -----------------------------------------------------------------------------
# geometria
# -----------------------------------------------------------------------------

def h01(*vals):
    """Un numero 0-1 que solo depende de vals (sin azar)."""
    x = 0.0
    for k, v in enumerate(vals):
        x += float(v) * (12.9898 + 7.233 * k) + 0.618 * k
    return (math.sin(x) * 43758.5453) % 1.0


def _resta(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _largo(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def distancia(a, b):
    return _largo(_resta(a, b))


def angulo(u, v):
    """Grados entre dos vectores."""
    lu, lv = _largo(u), _largo(v)
    if lu < 1e-9 or lv < 1e-9:
        return 0.0
    c = (u[0] * v[0] + u[1] * v[1] + u[2] * v[2]) / (lu * lv)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def giro_hacia(d):
    """(rx, ry) que llevan el -Z de una Light COMP o una camara (orden xyz) a
    la direccion d."""
    L = _largo(d)
    if L < 1e-9:
        return 0.0, 0.0
    dx, dy, dz = d[0] / L, d[1] / L, d[2] / L
    return math.degrees(math.asin(max(-1.0, min(1.0, dy)))), math.degrees(math.atan2(-dx, -dz))


def fila_equipo(f):
    """Una fila de la tabla en un dict con numeros (las que no se leen, None)."""
    try:
        e = dict(nombre=f[0].strip(), tipo=f[1].strip().lower())
        for k, c in enumerate(('x', 'y', 'z', 'ax', 'ay', 'az', 'tam')):
            e[c] = float(f[2 + k])
        e['pos'] = (e['x'], e['y'], e['z'])
        e['eje'] = _resta((e['ax'], e['ay'], e['az']), e['pos'])
        return e
    except Exception:
        return None


def foco_alcanza(e, punto, radio=0.0):
    """El cono del foco (o del estrobo) e toca una esfera de radio 'radio'
    centrada en punto: su eje y la direccion al punto forman menos de medio
    angulo del cono mas el radio angular de la esfera."""
    d = _resta(punto, e['pos'])
    L = _largo(d)
    extra = math.degrees(math.asin(min(1.0, radio / L))) if L > radio else 90.0
    return angulo(e['eje'], d) < 0.5 * e['tam'] + extra


# -----------------------------------------------------------------------------
# personas
# -----------------------------------------------------------------------------
# Cada persona i llega a los i * Llegada s (mas un poco), entra por la puerta,
# pasea por 3 a 7 puntos de la sala parandose en cada uno de 3 a 12 s, vuelve a
# la puerta, se va un rato (20 a 60 s) y vuelve. Cada tramo lo decide un hash
# de la persona, la vuelta y el tramo: la misma sala da la misma historia.

_PLANES = {}


def zona(cfg):
    """(medio ancho, medio fondo) del suelo del publico (v3): Zonaancho x
    Zonafondo, centrado, sin pasar del margen de las paredes."""
    return (max(0.3, min(0.5 * cfg.get('zona_ancho', cfg['ancho']), 0.5 * cfg['ancho'] - MARGEN)),
            max(0.3, min(0.5 * cfg.get('zona_fondo', cfg['fondo']), 0.5 * cfg['fondo'] - MARGEN)))


def _punto(cfg, i, v, k, evitar):
    hx, hz = zona(cfg)                  # v3: el publico se para en su suelo (antes, en toda la sala)
    p = None
    for intento in range(10):
        p = (-hx + 2 * hx * h01(i, v, k, intento, 1), -hz + 2 * hz * h01(i, v, k, intento, 2))
        if all(math.hypot(p[0] - e[0], p[1] - e[2]) > APARTE for e in evitar):
            return p
    return p


def _clave(cfg, evitar):
    return (cfg['ancho'], cfg['fondo'], cfg.get('zona_ancho'), cfg.get('zona_fondo'), cfg['llegada'],
            cfg.get('demo', 0), cfg['personas'], tuple(evitar))


# v4: demos de visita, a elegir con el parametro Demo de SALA
DEMOS = ['paseo', 'grupo', 'llena', 'goteo', 'vacia']
DEMOS_ETIQUETAS = ['Paseo: llegan de uno en uno (Llegada), pasean, se paran y se van',
                   'Grupo: entran juntos en fila, hacen corro ante la esfera y salen juntos',
                   'Llena: la sala se llena deprisa y el publico se queda casi quieto',
                   'Goteo: de uno en uno, van a la esfera, miran y se van',
                   'Vacia: nadie']
CICLO_GRUPO = 90.0          # s: el grupo entra, se queda y sale; luego vuelve a entrar
ESTANCIA_GRUPO = 55.0       # s desde que entra el primero hasta que sale el primero
CORRO = 2.2                 # m de la esfera al corro del grupo
FILA_CORRO = 7              # personas por fila del corro
TURNO_GOTEO = 35.0          # s entre dos visitantes del goteo


def _libre(cfg, q, evitar):
    """El punto q dentro del suelo del publico; si cae cerca de la esfera o
    del estrobo, se aleja de ellos hasta quedar a APARTE."""
    zx, zz = zona(cfg)
    x, z = q
    for _ in range(6):
        x, z = max(-zx, min(zx, x)), max(-zz, min(zz, z))
        cerca = [e for e in evitar if math.hypot(x - e[0], z - e[2]) <= APARTE]
        if not cerca:
            break
        e = cerca[0]
        d = math.hypot(x - e[0], z - e[2]) or 1e-6
        k = (APARTE + 0.15) / d
        x, z = e[0] + (x - e[0]) * k, e[2] + (z - e[2]) * k
    return (x, z)


def _corro(cfg, i, evitar):
    """El sitio de la persona i en el corro del grupo: un arco de cara a la
    esfera (filas de FILA_CORRO, cada una 0,7 m mas atras)."""
    c = evitar[0] if evitar else (0.0, 0.0, -0.5 * cfg['fondo'])       # la esfera va primero
    n = max(1, int(cfg['personas']))
    fila, k = divmod(i, FILA_CORRO)
    en_fila = min(FILA_CORRO, n - fila * FILA_CORRO)
    base = math.atan2(-c[0], -c[2])              # de la esfera hacia el centro de la sala
    a = base + math.radians(100.0) * ((k + 0.5) / en_fila - 0.5)
    r = CORRO + 0.7 * fila
    return _libre(cfg, (c[0] + r * math.sin(a), c[2] + r * math.cos(a)), evitar)


def _sitio_lleno(cfg, i, v, evitar):
    """Llena: el sitio de la persona i, repartido por el suelo del publico."""
    zx, zz = zona(cfg)
    n = max(1, int(cfg['personas']))
    cols = max(1, int(round(math.sqrt(n * zx / zz))))
    filas_ = int(math.ceil(n / float(cols)))
    f, k = divmod(i, cols)
    x = -zx + 2 * zx * (k + 0.2 + 0.6 * h01(i, v, 21)) / cols
    z = -zz + 2 * zz * (f + 0.2 + 0.6 * h01(i, v, 22)) / filas_
    return _libre(cfg, (x, z), evitar)


def _andar(tr, t, p, q):
    dt = math.hypot(q[0] - p[0], q[1] - p[1]) / VELOCIDAD
    tr.append([t, t + dt, p, q, True, True])
    return t + dt


def _quieto(tr, t, p, d):
    tr.append([t, t + max(0.5, d), p, p, True, False])
    return t + max(0.5, d)


def _visita(cfg, i, v, t, demo, evitar):
    """Los tramos de una visita (de cruzar la puerta a volver a ella) y el
    instante en que vuelve a estar en la puerta."""
    hz = 0.5 * cfg['fondo']
    puerta = (0.0, hz - 0.3)
    tr = [[t, t + 1.0, (0.0, hz), puerta, True, True]]          # cruza la puerta
    t, p = t + 1.0, puerta
    if demo == 'grupo':
        q = _corro(cfg, i, evitar)
        t = _andar(tr, t, p, q)
        sale = v * CICLO_GRUPO + ESTANCIA_GRUPO + 1.2 * i
        t = _quieto(tr, t, q, sale - t)
        p = q
    elif demo == 'llena':
        q = _sitio_lleno(cfg, i, v, evitar)
        t = _andar(tr, t, p, q)
        t = _quieto(tr, t, q, 50.0 + 60.0 * h01(i, v, 23))
        a = 2 * math.pi * h01(i, v, 24)          # un paso corto y vuelve a quedarse
        q2 = _libre(cfg, (q[0] + 0.45 * math.cos(a), q[1] + 0.45 * math.sin(a)), evitar)
        t = _andar(tr, t, q, q2)
        t = _quieto(tr, t, q2, 30.0 + 40.0 * h01(i, v, 25))
        p = q2
    elif demo == 'goteo':
        c = evitar[0] if evitar else (0.0, 0.0, -hz)
        a = math.atan2(-c[0], -c[2]) + math.radians(50.0) * (h01(i, v, 26) - 0.5)
        r = APARTE + 0.5 + 0.6 * h01(i, v, 27)
        q = _libre(cfg, (c[0] + r * math.sin(a), c[2] + r * math.cos(a)), evitar)
        t = _andar(tr, t, p, q)
        t = _quieto(tr, t, q, 10.0 + 8.0 * h01(i, v, 28))
        q2 = _punto(cfg, i, v, 0, evitar)
        t = _andar(tr, t, q, q2)
        t = _quieto(tr, t, q2, 3.0 + 4.0 * h01(i, v, 29))
        p = q2
    else:                                        # paseo
        for k in range(3 + int(5 * h01(i, v, 3))):
            q = _punto(cfg, i, v, k, evitar)
            t = _andar(tr, t, p, q)
            t = _quieto(tr, t, q, 3.0 + 9.0 * h01(i, v, k, 4))
            p = q
    t = _andar(tr, t, p, puerta)
    return tr, t


def _llegada(cfg, i, v, demo):
    """Cuando entra la persona i en su visita v (la primera, v = 0)."""
    n = max(1, int(cfg['personas']))
    if demo == 'grupo':
        return v * CICLO_GRUPO + 2.0 + 1.2 * i
    if demo == 'llena':
        return 1.5 * i + 4.0 * h01(i, 0, 9)
    if demo == 'goteo':
        return (v * n + i) * TURNO_GOTEO + 2.0
    return i * cfg['llegada'] + 4.0 * h01(i, 0, 9)


def plan(cfg, i, hasta, evitar=()):
    """Los tramos de la persona i hasta el instante 'hasta' (s desde que se
    abrio la sala): [t0, t1, (x0, z0), (x1, z1), dentro, andando]. v4: segun
    la demo (cfg['demo'], el parametro Demo)."""
    clave = _clave(cfg, evitar)
    pl = _PLANES.get(i)
    if pl is None or pl['clave'] != clave:
        pl = _PLANES[i] = dict(clave=clave, tramos=[], t=0.0, vuelta=0)
    fuera = (0.0, 0.5 * cfg['fondo'] + 1.0)
    demo = DEMOS[cfg.get('demo', 0) % len(DEMOS)]
    tr = pl['tramos']
    if demo == 'vacia':
        tr[:] = [[0.0, hasta + 3600.0, fuera, fuera, False, False]]
        return tr
    if not tr:
        tr.append([0.0, _llegada(cfg, i, 0, demo), fuera, fuera, False, False])
    while tr[-1][1] <= hasta:
        v = pl['vuelta']
        visita, t = _visita(cfg, i, v, tr[-1][1], demo, evitar)
        tr.extend(visita)
        if demo in ('grupo', 'goteo'):
            vuelve = max(t + 5.0, _llegada(cfg, i, v + 1, demo))
        elif demo == 'llena':
            vuelve = t + 5.0 + 10.0 * h01(i, v, 5)
        else:
            vuelve = t + 20.0 + 40.0 * h01(i, v, 5)
        tr.append([t, vuelve, fuera, fuera, False, False])
        pl['vuelta'] = v + 1
    del tr[:-200]                       # memoria acotada: lo viejo ya no se pregunta
    return tr


def tramo_en(cfg, i, t, evitar=()):
    for s in reversed(plan(cfg, i, t, evitar)):
        if s[0] <= t:
            return s
    return None


def posicion(cfg, i, t, evitar=()):
    """(x, z, andando) de la persona i en t, o None si esta fuera de la sala."""
    s = tramo_en(cfg, i, t, evitar)
    if s is None or not s[4]:
        return None
    u = 0.0 if s[1] <= s[0] else max(0.0, min(1.0, (t - s[0]) / (s[1] - s[0])))
    return (s[2][0] + (s[3][0] - s[2][0]) * u, s[2][1] + (s[3][1] - s[2][1]) * u, s[5])


def altura(i):
    return 1.55 + 0.40 * h01(i, 6)


def personas(cfg, t, evitar=()):
    """[(i, x, z, altura, andando)] de las personas dentro de la sala en t."""
    out = []
    for i in range(int(cfg['personas'])):
        p = posicion(cfg, i, t, evitar)
        if p is not None:
            out.append((i, p[0], p[1], altura(i), p[2]))
    return out


# -----------------------------------------------------------------------------
# luz (Modoluz = prueba)
# -----------------------------------------------------------------------------

def estado_prueba(t):
    """('deposito' | 'tension' | 'erosion', 0-1 dentro del estado)."""
    f = (t % CICLO_PRUEBA) / CICLO_PRUEBA * 3.0
    k = int(f)
    return ('deposito', 'tension', 'erosion')[min(2, k)], f - k


def hz_estrobo(cfg):
    return max(0.0, min(MAX_HZ, cfg['hz_prueba']))


def destellos(cfg, ta, tb):
    """Instantes de los destellos del estrobo en [ta, tb)."""
    f = hz_estrobo(cfg)
    if cfg['modo_luz'] != 1 or f <= 0:
        return []
    out = []
    k = int(math.ceil(ta * f - 1e-9))
    while k / f < tb:
        t = k / f
        if estado_prueba(t)[0] == 'erosion':
            out.append(t)
        k += 1
    return out


def estrobo_activo(cfg, t):
    return cfg['modo_luz'] == 1 and estado_prueba(t)[0] == 'erosion' and hz_estrobo(cfg) > 0


def luz_de(cfg, e, t):
    """(r, g, b, dimmer) de un foco o el estrobo e en t."""
    if cfg['modo_luz'] != 1:
        return (0.0, 0.0, 0.0, 0.0)
    est, u = estado_prueba(t)
    if e['tipo'] == 'estrobo':
        f = hz_estrobo(cfg)
        if est != 'erosion' or f <= 0:
            return (1.0, 1.0, 1.0, 0.0)
        k = math.floor(t * f + 1e-9)
        return BLANCO + ((1.0 if 0.0 <= t - k / f < DESTELLO else 0.0),)
    if est == 'deposito':
        return AMBAR + (0.15 + 0.08 * math.sin(2.0 * math.pi * t / 4.0),)
    if est == 'tension':
        col = tuple(a + (b - a) * u for a, b in zip(AMBAR, BLANCO_FRIO))
        return col + (0.25 + 0.45 * u,)
    return BLANCO_FRIO + (0.5,)


# -----------------------------------------------------------------------------
# el microfono
# -----------------------------------------------------------------------------
# Lo que oye el microfono en un bloque: cada fuente, por 1/d y con su retardo.
# Los ruidos (pasos, palmadas, toses y el clic del estrobo) son eventos con su
# instante y su sitio; el drone de los altavoces y el sub es continuo. Sin
# reverberacion: la sala real la pondra, y por eso Umbralonset se ajusta alli.

def _np():
    try:
        import numpy
        return numpy
    except Exception:
        return None


def _ruido(np, j, semilla):
    return (np.sin((j + 7919.0 * semilla) * 12.9898 + 78.233) * 43758.5453) % 1.0 * 2.0 - 1.0


def plantilla(np, tipo, n, rate, semilla):
    """Las n primeras muestras de un ruido de tipo, sin azar."""
    j = np.arange(n, dtype=float)
    t = j / rate
    if tipo == 'palmada':
        return 0.9 * _ruido(np, j, semilla) * np.exp(-t / 0.004)
    if tipo == 'tos':
        env = np.minimum(1.0, t / 0.01) * np.exp(-t / 0.08)
        return 0.55 * _ruido(np, j, semilla) * env * (0.6 + 0.4 * np.sin(2 * math.pi * 320.0 * t))
    if tipo == 'paso':                  # unos 20 dB por debajo de una palmada: solo cuentan los de cerca
        return 0.09 * (np.sin(2 * math.pi * 70.0 * t) * np.exp(-t / 0.03)
                       + 0.3 * _ruido(np, j, semilla) * np.exp(-t / 0.005))
    if tipo == 'clic':
        return 0.6 * _ruido(np, j, semilla) * np.exp(-t / 0.0006)
    return np.zeros(n)


DURA = dict(palmada=0.03, tos=0.3, paso=0.12, clic=0.004)


def eventos(cfg, ta, tb, evitar=()):
    """Los ruidos de la sala en [ta, tb): [(t, tipo, (x, y, z), semilla)]."""
    out = []
    for i in range(int(cfg['personas'])):
        # los pasos: mientras anda, una pisada cada PASO s desde que echo a andar
        for s in plan(cfg, i, tb, evitar):
            if not (s[4] and s[5]) or s[1] <= ta or s[0] >= tb:
                continue
            k = max(0, int(math.ceil((ta - s[0]) / PASO - 1e-9)))
            while s[0] + k * PASO < min(tb, s[1]):
                t = s[0] + k * PASO
                p = posicion(cfg, i, t, evitar)
                if p is not None:
                    out.append((t, 'paso', (p[0], 0.0, p[1]), i * 1000 + k))
                k += 1
        # palmadas y toses: Ruidopublico por segundo y persona (mas con el estrobo)
        for k in range(int(math.floor(ta / RANURA)), int(math.floor(tb / RANURA)) + 1):
            t = (k + h01(i, k, 8)) * RANURA
            if not ta <= t < tb:
                continue
            tasa = cfg['ruido_publico'] * (cfg['reaccion'] if estrobo_activo(cfg, t) else 1.0)
            if h01(i, k, 7) >= tasa * RANURA:
                continue
            p = posicion(cfg, i, t, evitar)
            if p is not None:
                out.append((t, 'palmada' if h01(i, k, 9) < 0.5 else 'tos', (p[0], BOCA, p[1]), i * 1000 + k))
    return out


def bloque_audio(cfg, equipos, ta, n, rate, evs, mic=None):
    """n muestras de lo que oye el microfono desde ta (s): los eventos evs, el
    drone de los altavoces y el sub (Volumendrone) y nada mas."""
    np = _np()
    x = np.zeros(int(n))
    if mic is None:
        m = [e for e in equipos if e['tipo'] == 'micro']
        if not m:
            return x
        mic = m[0]['pos']
    t = ta + np.arange(int(n), dtype=float) / rate
    vol = max(0.0, cfg['volumen_drone'])
    for e in equipos:
        if vol <= 0 or e['tipo'] not in ('altavoz', 'sub'):
            continue
        d = max(1.0, distancia(e['pos'], mic))
        u = t - d / VEL_SONIDO
        if e['tipo'] == 'altavoz':
            x += vol * 0.12 / d * (np.sin(2 * math.pi * 110.0 * u) + 0.5 * np.sin(2 * math.pi * 220.0 * u)
                                   + 0.3 * np.sin(2 * math.pi * 330.0 * u))
        else:
            x += vol * 0.15 / d * np.sin(2 * math.pi * 41.0 * u)
    for te, tipo, p, semilla in evs:
        d = max(0.5, distancia(p, mic))
        k0 = int(round((te + d / VEL_SONIDO - ta) * rate))
        m = int(DURA[tipo] * rate)
        if k0 >= n or k0 + m <= 0:
            continue
        y = plantilla(np, tipo, m, rate, semilla) / d
        a, b = max(0, k0), min(int(n), k0 + m)
        x[a:b] += y[a - k0:b - k0]
    return x


# =============================================================================
# ADAPTADOR TOUCHDESIGNER
# =============================================================================
# Lo de aqui abajo usa parent(), op() y absTime: solo funciona dentro de
# TouchDesigner (o del simulado de pruebas/).

_SALA = dict(t0=None, frame=None, equipos=None, audio=None, t_audio=None, forzar=False, manuales=[],
             col_esfera=None, col_frame=None, rotulo=None, rotulo_frame=None)
ROTULO_CADA = 15            # v5: el rotulo se rehace cada 15 fotogramas (un cuarto de segundo)
MODOS_LUZ = ['apagado', 'prueba']
VISTAS = ['visitante', 'entrada', 'orbita', 'cenital']      # v2; hasta la v1, libre (= orbita) y cenital


def _p(name, default):
    try:
        p = getattr(parent().par, name, None)
        if p is None:
            return default
        v = p.eval()
        if isinstance(default, bool):
            return bool(v)
        if isinstance(default, int):
            return int(v) if not isinstance(v, str) else v
        if isinstance(default, float):
            return float(v)
        return v
    except Exception:
        return default


def _menu(name, opciones, defecto):
    v = _p(name, opciones[defecto])
    if isinstance(v, str):
        return opciones.index(v) if v in opciones else defecto
    try:
        return int(v)
    except Exception:
        return defecto


def cfg():
    return dict(activa=bool(_p('Activa', True)),
                ancho=max(2.0, _p('Ancho', 8.0)), fondo=max(2.0, _p('Fondo', 6.0)), alto=max(2.0, _p('Alto', 4.0)),
                zona_ancho=_p('Zonaancho', 5.4), zona_fondo=_p('Zonafondo', 4.5),
                personas=max(0, int(_p('Personas', 6))), llegada=max(0.0, _p('Llegada', 8.0)),
                ruido_publico=max(0.0, _p('Ruidopublico', 0.05)), reaccion=max(0.0, _p('Reaccion', 3.0)),
                volumen_drone=max(0.0, _p('Volumendrone', 0.5)),
                modo_luz=_menu('Modoluz', MODOS_LUZ, 1), hz_prueba=_p('Hzprueba', 2.5),
                luz_casa=max(0.0, _p('Luzcasa', 0.06)), vista=_menu('Vista', VISTAS, 0),
                bruma=max(0.0, min(1.0, _p('Bruma', 0.5))), demo=_menu('Demo', DEMOS, 0),
                luz_esfera=max(0.0, _p('Luzesfera', 0.0)))


def ahora():
    """Segundos desde que se abrio la sala (Reiniciarsala la vuelve a abrir)."""
    if _SALA['t0'] is None:
        _SALA['t0'] = absTime.seconds
    return absTime.seconds - _SALA['t0']


def reiniciar(t=None):
    _SALA['t0'] = absTime.seconds if t is None else absTime.seconds - t
    _PLANES.clear()


def equipos(frame=None):
    """Las filas de la tabla 'equipos' (se releen una vez por fotograma)."""
    if _SALA['equipos'] is not None and _SALA['frame'] == absTime.frame:
        return _SALA['equipos']
    out = []
    t = parent().op('equipos')
    if t is not None:
        for r in range(1, t.numRows):
            e = fila_equipo([t[r, c].val if t[r, c] is not None else '' for c in range(len(COLS_EQUIPOS))])
            if e is not None:
                out.append(e)
    _SALA['equipos'], _SALA['frame'] = out, absTime.frame
    return out


def equipo(nombre):
    return next((e for e in equipos() if e['nombre'] == nombre), None)


def evitar_de(eq):
    return tuple(e['pos'] for e in eq if e['tipo'] in ('esfera', 'estrobo'))


def valor(nombre, que, frame=None):
    """Para las expresiones de las Light COMP y las camaras: tx ty tz rx ry
    (hacia donde apunta), cono (el angulo del foco) y r g b d (su luz)."""
    try:
        e = equipo(nombre)
        if e is None:
            return 0.0
        if que in ('tx', 'ty', 'tz'):
            return e['pos'][('tx', 'ty', 'tz').index(que)]
        if que in ('rx', 'ry'):
            return giro_hacia(e['eje'])[0 if que == 'rx' else 1]
        if que == 'cono':
            return e['tam']
        c = cfg()
        if not c['activa']:
            return 0.0
        l = luz_de(c, e, ahora())
        return l[('r', 'g', 'b', 'd').index(que)]
    except Exception:
        return 0.0


def paseo_visitante(cfg, t, evitar=()):
    """(x, z) del visitante en t: pasea a VEL_VISITANTE entre PUNTOS_VISITANTE
    puntos de la sala (lejos de la esfera y del estrobo), se para
    PARADA_VISITANTE s en cada uno y vuelve a empezar. Sin azar ni estado."""
    pts = [(0.0, 0.5 * cfg['fondo'] - 0.8)]
    pts += [_punto(cfg, 777, 0, k, evitar) for k in range(PUNTOS_VISITANTE)]
    tramos = []
    for k, p in enumerate(pts):
        q = pts[(k + 1) % len(pts)]
        tramos.append((p, p, PARADA_VISITANTE))
        tramos.append((p, q, math.hypot(q[0] - p[0], q[1] - p[1]) / VEL_VISITANTE))
    T = sum(d for _, _, d in tramos)
    u = t % T if T > 0 else 0.0
    for p, q, d in tramos:
        if u <= d or d <= 0:
            f = 0.0 if d <= 0 else u / d
            f = f * f * (3.0 - 2.0 * f)             # arranca y se para sin tirones
            return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
        u -= d
    return pts[0]


def ojos(c=None, frame=None):
    """(posicion, a donde mira) de la camara principal segun Vista."""
    c = c or cfg()
    eq = equipos()
    esf = next((e for e in eq if e['tipo'] == 'esfera'), None)
    mira = esf['pos'] if esf is not None else (0.0, 1.3, -0.5 * c['fondo'])
    modo = VISTAS[c['vista'] % len(VISTAS)]
    if modo == 'visitante':
        x, z = paseo_visitante(c, ahora(), evitar_de(eq))
        return (x, OJOS, z), mira
    if modo == 'entrada':
        return vista_entrada(c, esf)
    if modo == 'cenital':
        cam = next((e for e in eq if e['tipo'] == 'camara'), None)
        p = cam['pos'] if cam is not None else (0.0, 3.5, 0.0)
        return p, (p[0], 0.0, p[2] - 0.3)
    a = math.radians(_p('Orbita', 30.0))
    R = _p('Distancia', 11.0)
    return (R * math.sin(a), _p('Alturavista', 5.0), R * math.cos(a)), (0.0, 1.0, 0.0)


ENTRADA_ATRAS = 2.2         # v3: m por detras de la puerta (la pared de la entrada esta abierta)
ENTRADA_ALTO = 2.8          # m: algo por encima de los ojos, para ver la reticula del suelo


def vista_entrada(c, esf=None):
    """(posicion, a donde mira) de la vista entrada (v3): un poco por detras
    de la puerta y por encima de la gente, mirando hacia abajo y hacia el
    fondo, entre el centro del suelo del publico y la esfera. Se ven la
    reticula del publico entera, la esfera en su esquina y las paredes en
    perspectiva."""
    hz = 0.5 * c['fondo']
    p = (0.0, min(ENTRADA_ALTO, c['alto'] - 0.3), hz + ENTRADA_ATRAS)
    if esf is None:
        return p, (0.0, 0.0, -0.25 * hz)
    return p, (0.3 * esf['x'], 0.25 * esf['y'], 0.2 * esf['z'])


def vista(que, frame=None):
    """La camara principal (Vista): tx ty tz de su posicion, mx my mz de a
    donde mira (el Null 'mirada'), y fov."""
    try:
        c = cfg()
        p, m = ojos(c)
        if que == 'fov':
            modo = VISTAS[c['vista'] % len(VISTAS)]
            return {'cenital': 75.0, 'entrada': 80.0}.get(modo, 62.0)
        if que in ('mx', 'my', 'mz'):
            return m[('mx', 'my', 'mz').index(que)]
        return p[('tx', 'ty', 'tz').index(que)]
    except Exception:
        return 0.0


def plano(que, frame=None):
    """La camara del plano (ortografica, desde arriba): ty y el ancho."""
    c = cfg()
    if que == 'ancho':
        return 1.08 * max(c['ancho'], c['fondo'] * 4.0 / 3.0)
    return c['alto'] + 2.0


def haz(e):
    """(largo, diametro) del haz de un foco o del estrobo: hasta el suelo,
    como mucho HAZ_MAX."""
    L = _largo(e['eje'])
    dy = e['eje'][1] / L if L > 1e-9 else -1.0
    largo = HAZ_MAX if dy > -0.05 else min(HAZ_MAX, e['y'] / -dy)
    return largo, 2.0 * largo * math.tan(math.radians(min(170.0, e['tam']) / 2.0))


def _media(ch):
    try:
        v = list(ch.vals)
    except Exception:
        v = [float(ch.eval())]
    return sum(v) / float(len(v)) if v else 0.0


def color_esfera(frame=None):
    """(r, g, b) medio de la imagen de la esfera, una vez por fotograma; si
    no se puede medir (o Luzesfera = 0), COL_ESFERA_DEF. v5: lo lee del TOP
    to CHOP 'esfera_color' (descarga diferida); antes, numpyArray() sobre
    'esfera_media' bajaba la textura de la GPU en el momento y paraba el
    fotograma (15 ms en luz_esfera, segun el inspector de rendimiento)."""
    if _SALA['col_esfera'] is not None and _SALA['col_frame'] == absTime.frame:
        return _SALA['col_esfera']
    col = COL_ESFERA_DEF
    if cfg()['luz_esfera'] > 0:
        try:
            ch = parent().op('esfera_color')
            if ch is not None and ch.numChans >= 3:
                col = tuple(max(0.0, min(1.0, _media(ch[k]))) for k in range(3))
        except Exception:
            pass
    _SALA['col_esfera'], _SALA['col_frame'] = col, absTime.frame
    return col


def luz_esfera(que, frame=None):
    """La luz de la esfera (Light COMP luz_esfera): tx ty tz y r g b d."""
    try:
        e = equipo('esfera')
        if que in ('tx', 'ty', 'tz'):
            return e['pos'][('tx', 'ty', 'tz').index(que)] if e is not None else 0.0
        if que == 'd':                      # v4: Luzesfera (0 por defecto: la mancha en la pared sobraba)
            c = cfg()
            return c['luz_esfera'] if c['activa'] else 0.0
        return color_esfera()[('r', 'g', 'b').index(que)]
    except Exception:
        return 0.0


def _filas_sala(c):
    W, F, H = c['ancho'], c['fondo'], c['alto']
    hx, hz = W / 2.0, F / 2.0
    zx, zz = zona(c)
    return [[0, -0.02, 0, 0, 0, 0, W, 0.02, F] + list(COL_SUELO),
            [0, 0, -hz, 0, 0, 0, W, H, 0.05] + list(COL_PARED),
            [-hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
            [hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
            [0, 0, hz, 0, 0, 0, PUERTA_ANCHO, 0.01, 0.12] + list(COL_PUERTA),
            [0, 0, 0, 0, 0, 0, 2 * zx, 0.006, 2 * zz] + list(COL_TARIMA)]     # v3: el suelo del publico


def _marcas(a, b, paso):
    """Las posiciones de a a b (incluidos) cada 'paso', centradas."""
    n = max(1, int(round((b - a) / paso)))
    return [a + (b - a) * k / float(n) for k in range(n + 1)]


def _linea(p, q, col, g=GROSOR):
    """Una linea recta de p a q, paralela a un eje: una caja fina (la caja
    tiene la base en y = 0)."""
    sx, sy, sz = (max(g, abs(q[0] - p[0])), max(g, abs(q[1] - p[1])), max(g, abs(q[2] - p[2])))
    return [0.5 * (p[0] + q[0]), min(p[1], q[1]), 0.5 * (p[2] + q[2]), 0, 0, 0, sx, sy, sz] + list(col)


def _filas_lineas(c):
    """v3: el dibujo de la sala, para leerla en perspectiva aunque este a
    oscuras: las doce aristas, el umbral de la puerta, una reticula de
    GRID_ZONA m en todo el suelo (v4; antes solo en el del publico), una de
    GRID_SALA m en las tres paredes, y el borde del suelo del publico
    (Zonaancho x Zonafondo), donde se pararia la gente."""
    W, F, H = c['ancho'], c['fondo'], c['alto']
    hx, hz = W / 2.0, F / 2.0
    zx, zz = zona(c)
    y0, yz = 0.008, 0.012           # la reticula (sobre la tarima) y, encima, el borde del publico
    f = []
    # v4: la reticula de GRID_ZONA m cubre todo el suelo de la sala
    for x in _marcas(-hx, hx, GRID_ZONA)[1:-1]:
        f.append(_linea((x, y0, -hz), (x, y0, hz), LIN_GRID, 0.015))
    for z in _marcas(-hz, hz, GRID_ZONA)[1:-1]:
        f.append(_linea((-hx, y0, z), (hx, y0, z), LIN_GRID, 0.015))
    # las tres paredes, cada GRID_SALA m
    for x in _marcas(-hx, hx, GRID_SALA)[1:-1]:
        f.append(_linea((x, 0.0, -hz + 0.03), (x, H, -hz + 0.03), LIN_PARED, 0.012))
    for z in _marcas(-hz, hz, GRID_SALA)[1:-1]:
        for x in (-hx + 0.03, hx - 0.03):
            f.append(_linea((x, 0.0, z), (x, H, z), LIN_PARED, 0.012))
    for y in _marcas(0.0, H, GRID_SALA)[1:-1]:
        f.append(_linea((-hx, y, -hz + 0.03), (hx, y, -hz + 0.03), LIN_PARED, 0.012))
        for x in (-hx + 0.03, hx - 0.03):
            f.append(_linea((x, y, -hz), (x, y, hz), LIN_PARED, 0.012))
    # el suelo del publico: su borde (la reticula ya pasa por encima)
    for p, q in (((-zx, yz, -zz), (zx, yz, -zz)), ((-zx, yz, zz), (zx, yz, zz)),
                 ((-zx, yz, -zz), (-zx, yz, zz)), ((zx, yz, -zz), (zx, yz, zz))):
        f.append(_linea(p, q, LIN_ZONA, 0.025))
    # las doce aristas
    for y in (0.0, H - GROSOR):
        f.append(_linea((-hx, y, -hz), (hx, y, -hz), LIN_ARISTA))
        f.append(_linea((-hx, y, hz), (hx, y, hz), LIN_ARISTA))
        f.append(_linea((-hx, y, -hz), (-hx, y, hz), LIN_ARISTA))
        f.append(_linea((hx, y, -hz), (hx, y, hz), LIN_ARISTA))
    for x in (-hx, hx):
        for z in (-hz, hz):
            f.append(_linea((x, 0.0, z), (x, H, z), LIN_ARISTA))
    # la puerta: su umbral en el suelo, con un tope a cada lado (sin marco
    # alto: la vista entrada mira a traves de ella y lo tendria delante)
    px = 0.5 * PUERTA_ANCHO
    f.append(_linea((-px, yz, hz - 0.06), (px, yz, hz - 0.06), COL_PUERTA, 0.06))
    for x in (-px, px):
        f.append(_linea((x, 0.0, hz - 0.06), (x, 0.25, hz - 0.06), COL_PUERTA, 0.06))
    return f


def _filas_equipos(c, eq, t):
    out = []
    for e in eq:
        if e['tipo'] == 'sub':              # v6: va dentro de la peana; dibujado, sus caras y las de la
            continue                        # peana coincidian y salian rayas bajo la esfera
        if e['tipo'] == 'esfera':           # la peana; la esfera tiene su geometria
            alto = max(0.05, e['y'] - 0.5 * e['tam'])
            out.append([e['x'], 0.0, e['z'], 0, 0, 0, 0.6 * e['tam'], alto, 0.6 * e['tam']]
                       + list(COL_EQUIPO['esfera']))
            continue
        sx, sy, sz = TAM_EQUIPO.get(e['tipo'], (0.2, 0.2, 0.2))
        col = COL_EQUIPO.get(e['tipo'], (0.5, 0.5, 0.5))
        rx, ry = giro_hacia(e['eje']) if e['tipo'] in ('altavoz', 'foco', 'estrobo') else (0.0, 0.0)
        if e['tipo'] in ('foco', 'estrobo') and c['activa']:
            l = luz_de(c, e, t)             # el aparato se enciende con su luz
            col = tuple(max(a, b * l[3]) for a, b in zip(col, l[:3]))
        out.append([e['x'], e['y'] - 0.5 * sy, e['z'], rx, ry, 0, sx, sy, sz] + list(col))
    return out


def _filas_personas(c, eq, t):
    """El cuerpo de cada persona: un tronco de toda su altura, de ropa oscura
    (en una sala a oscuras el publico se lee a contraluz). v4: sin cabeza."""
    out = []
    for i, x, z, h, _ in personas(c, t, evitar_de(eq)):
        col = (0.10 + 0.22 * h01(i, 11), 0.10 + 0.22 * h01(i, 12), 0.10 + 0.22 * h01(i, 13))
        out.append([x, 0.0, z, 0, 0, 0, 0.42, h, 0.26] + list(col))
    return out


def _filas_haces(c, eq, t):
    """Un cono por foco y por estrobo, del color de su luz, en la bruma: la
    punta en el aparato, la base en el suelo. Sin luz (o sin Bruma), nada."""
    out = []
    if not c['activa'] or c['bruma'] <= 0:
        return out
    for e in eq:
        if e['tipo'] not in ('foco', 'estrobo'):
            continue
        r, g, b, d = luz_de(c, e, t)
        k = HAZ_K * c['bruma'] * d
        if k <= 1e-4:
            continue
        largo, diam = haz(e)
        rx, ry = giro_hacia(e['eje'])
        out.append([e['x'], e['y'], e['z'], rx, ry, 0, diam, diam, largo, r * k, g * k, b * k])
    return out


def filas(nombre):
    """Las instancias de los Script CHOP i_sala, i_equipos, i_personas,
    (v2) i_haces y (v3) i_lineas."""
    c = cfg()
    eq = equipos()
    t = ahora()
    if nombre == 'i_sala':
        return _filas_sala(c)
    if nombre == 'i_lineas':
        return _filas_lineas(c)
    if nombre == 'i_equipos':
        return _filas_equipos(c, eq, t)
    if nombre == 'i_personas':
        return _filas_personas(c, eq, t) if c['activa'] else []
    if nombre == 'i_haces':
        return _filas_haces(c, eq, t)
    return []


def frame_tick():
    """Cada fotograma (latido_sala): las personas y los aparatos se redibujan."""
    if not _p('Activa', True):
        return
    for nm in ('i_personas', 'i_equipos', 'i_haces'):
        o = parent().op(nm)
        if o is not None:
            o.cook(force=True)


def audio_cook(scriptOp):
    """onCook del Script CHOP audio_mic: las muestras desde el bloque anterior.
    Dos cocinados en el mismo fotograma dan el mismo bloque (Palmada fuerza uno
    nuevo)."""
    np = _np()
    if (_SALA['audio'] is not None and _SALA.get('audio_frame') == absTime.frame
            and not _SALA['forzar']):
        x = _SALA['audio']
    else:
        c = cfg()
        t = ahora()
        tl = _SALA['t_audio']
        dt = t - tl if tl is not None and t > tl else 1.0 / 60.0
        n = max(32, min(RATE // 4, int(round(dt * RATE))))
        ta = t - n / float(RATE)
        eq = equipos()
        _SALA['manuales'] = [m for m in _SALA['manuales'] if m[0] is None or m[0] > t - 1.0]
        if _SALA['forzar']:
            _SALA['manuales'] = [(ta + 0.002,) + tuple(m[1:]) if m[0] is None else m
                                 for m in _SALA['manuales']]
        evs = []
        if c['activa']:
            atras = ta - 0.5                # las colas de lo que empezo antes
            evs = eventos(c, atras, t, evitar_de(eq))
            est = [e for e in eq if e['tipo'] == 'estrobo']
            if est:
                evs += [(d, 'clic', est[0]['pos'], int(d * 1000)) for d in destellos(c, atras, t)]
            evs += [m for m in _SALA['manuales'] if m[0] is not None and m[0] >= atras]
        x = bloque_audio(c, eq, ta, n, RATE, evs) if c['activa'] else np.zeros(n)
        _SALA.update(audio=x, audio_frame=absTime.frame, t_audio=t, forzar=False)
    scriptOp.clear()
    scriptOp.rate = RATE
    scriptOp.numSamples = len(x)
    scriptOp.appendChan('mic').vals = [float(v) for v in x]


def palmada(donde=None):
    """Una palmada en el proximo bloque: donde (x, y, z) o, si no, la de la
    persona mas cercana al microfono (o en el centro de la sala)."""
    if donde is None:
        c = cfg()
        eq = equipos()
        m = next((e for e in eq if e['tipo'] == 'micro'), None)
        ps = personas(c, ahora(), evitar_de(eq))
        if ps and m is not None:
            i, x, z, h, _ = min(ps, key=lambda q: math.hypot(q[1] - m['x'], q[2] - m['z']))
            donde = (x, BOCA, z)
        else:
            donde = (0.0, BOCA, 0.0)
    _SALA['manuales'].append((None, 'palmada', tuple(donde), len(_SALA['manuales']) + 1))
    _SALA['forzar'] = True
    return donde


def margen_esfera(c=None, eq=None):
    """(a la pared del fondo, a la de su lado) en m, de la superficie de la
    esfera a cada pared; None si no hay esfera."""
    c = c or cfg()
    eq = equipos() if eq is None else eq
    esf = next((e for e in eq if e['tipo'] == 'esfera'), None)
    if esf is None:
        return None
    r = 0.5 * esf['tam']
    return (esf['z'] + 0.5 * c['fondo'] - r, 0.5 * c['ancho'] - abs(esf['x']) - r)


def esfera_en_esquina(c=None, eq=None):
    """La esfera esta en una esquina del fondo de la sala, a ESFERA_MARGEN
    (1 m, v4) de cada pared, con 20 cm de tolerancia."""
    m = margen_esfera(c, eq)
    return m is not None and all(abs(d - ESFERA_MARGEN) <= 0.2 for d in m)


def recolocar():
    """Rehace la tabla 'equipos' con las medidas de ahora (Ancho, Fondo, Alto)."""
    t = parent().op('equipos')
    if t is None:
        return 0
    c = cfg()
    t.clear()
    t.appendRow(COLS_EQUIPOS)
    for f in equipos_defecto(c['ancho'], c['fondo'], c['alto']):
        t.appendRow(f)
    _SALA['equipos'] = None
    _PLANES.clear()
    return t.numRows - 1


def on_pulse(nombre):
    if nombre == 'Recolocar':
        n = recolocar()
        print('SALA  equipos recolocados para %gx%gx%g m (%d filas). Si cambia el numero de focos, '
              'relanza sala_virtual.py para sus luces' % (cfg()['ancho'], cfg()['fondo'], cfg()['alto'], n))
    elif nombre == 'Palmada':
        p = palmada()
        print('SALA  palmada en (%.1f, %.1f) m' % (p[0], p[2]))
    elif nombre == 'Reiniciarsala':
        reiniciar()
        print('SALA  abierta de nuevo: las personas vuelven a entrar')


def texto_monitor(frame=None):
    """El rotulo del monitor (v2): la sala, la luz y lo que oye FASE1. v5:
    se rehace cada ROTULO_CADA fotogramas; entre medias, el mismo texto (el
    Text TOP no se vuelve a dibujar)."""
    f = absTime.frame
    if _SALA['rotulo'] is not None and _SALA['rotulo_frame'] is not None \
            and 0 <= f - _SALA['rotulo_frame'] < ROTULO_CADA:
        return _SALA['rotulo']
    _SALA['rotulo'], _SALA['rotulo_frame'] = _texto_monitor(), f
    return _SALA['rotulo']


def luces_render(extra=''):
    """v5: la lista de luces de los render de la sala; luz_esfera solo con
    Luzesfera > 0 (una luz a 0 se sigue calculando en cada pixel)."""
    try:
        nombres = [o.name for o in parent().children if o.name.startswith('luz_')]
    except Exception:
        nombres = []
    if cfg()['luz_esfera'] <= 0:
        nombres = [n for n in nombres if n != 'luz_esfera']
    return ' '.join(sorted(nombres) + ([extra] if extra else []))


def _texto_monitor():
    lineas = [legend()]
    try:
        c = cfg()
        modo = VISTAS[c['vista'] % len(VISTAS)]
        t = ahora()
        if c['modo_luz'] == 1:
            est, u = estado_prueba(t)
            luz = 'LUZ  %s (%d%%)   %s' % (est, int(u * 100), {
                'deposito': 'ambar tenue que respira', 'tension': 'sube y vira a blanco frio',
                'erosion': 'estrobo blanco %.1f Hz' % hz_estrobo(c)}[est])
        else:
            luz = 'LUZ  apagada (Modoluz)'
        lineas.append('%s   bruma %d%%   vista %s' % (luz, int(c['bruma'] * 100), modo))
    except Exception:
        pass
    try:
        m = op('/project1/FASE1').op('motor').module
        mc = m.world().get('mic') or {}
        if 'n' in mc:
            lineas.append('MICRO  onsets %d   flujo %.2f' % (mc['n'], mc.get('flujo', 0.0)))
    except Exception:
        pass
    return '\n'.join(lineas)


def legend(frame=None):
    """Una linea para el Textport o un Text TOP."""
    try:
        c = cfg()
        t = ahora()
        eq = equipos()
        ps = personas(c, t, evitar_de(eq))
        est = estado_prueba(t)[0] if c['modo_luz'] == 1 else 'apagada'
        return ('SALA  %gx%g m   personas %d/%d   luz %s%s   %d focos   microfono %s'
                % (c['ancho'], c['fondo'], len(ps), c['personas'], est,
                   ' (estrobo %.1f Hz)' % hz_estrobo(c) if est == 'erosion' else '',
                   sum(1 for e in eq if e['tipo'] == 'foco'),
                   'si' if any(e['tipo'] == 'micro' for e in eq) else 'no'))
    except Exception as e:
        return 'SALA  fallo en la leyenda: %s' % e
