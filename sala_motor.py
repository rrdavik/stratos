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
# =============================================================================

SALA_VERSION = 'sala v1'

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

AMBAR = (1.00, 0.55, 0.15)
BLANCO_FRIO = (0.80, 0.90, 1.00)
BLANCO = (1.0, 1.0, 1.0)

COL_SUELO = (0.10, 0.10, 0.11)
COL_PARED = (0.17, 0.17, 0.18)
COL_ZONA = (0.10, 0.38, 0.42)
COL_PUERTA = (0.55, 0.40, 0.12)
COL_EQUIPO = dict(altavoz=(0.05, 0.05, 0.06), sub=(0.05, 0.05, 0.06), micro=(0.75, 0.75, 0.78),
                  camara=(0.35, 0.35, 0.38), foco=(0.20, 0.20, 0.22), estrobo=(0.30, 0.30, 0.32),
                  esfera=(0.22, 0.22, 0.24))
TAM_EQUIPO = dict(altavoz=(0.32, 0.50, 0.30), sub=(0.60, 0.50, 0.60), micro=(0.06, 0.18, 0.06),
                  camara=(0.28, 0.08, 0.12), foco=(0.22, 0.28, 0.22), estrobo=(0.40, 0.16, 0.20))


def equipos_defecto(ancho=8.0, fondo=6.0, alto=4.0):
    """Las filas de la tabla 'equipos' para una sala de ancho x fondo x alto:
    la esfera (1 m, sobre una peana de 0,8 m) en la esquina del fondo a la
    izquierda con el sub dentro de la peana, cuatro altavoces colgados en las
    esquinas a 3 m, el microfono en lo alto hacia el centro y lejos de la
    esfera y del estrobo, la camara cenital a 3,5 m en el centro, cuatro focos
    de bano colgados que apuntan al suelo y al publico (dos acompanan a la
    esfera, sin apuntarle) y el estroboscopio en el suelo junto a la esfera."""
    hx, hz = ancho / 2.0, fondo / 2.0
    colg = min(3.0, alto - 0.6)                 # altavoces y microfono
    techo = alto - 0.4                          # focos
    ex, ez = -hx + 0.8, -hz + 0.8               # la esfera
    filas = [
        ['esfera', 'esfera', ex, 1.3, ez, ex, 1.3, ez + 1.0, 1.0, 'LEDs, 1 m; peana de 0,8 m'],
        ['sub', 'sub', ex, 0.25, ez, 0.0, 0.25, 0.0, 0.6, 'dentro de la peana de la esfera'],
        ['altavoz1', 'altavoz', -hx + 0.4, colg, -hz + 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, fondo izquierda'],
        ['altavoz2', 'altavoz', hx - 0.4, colg, -hz + 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, fondo derecha'],
        ['altavoz3', 'altavoz', -hx + 0.4, colg, hz - 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, entrada izquierda'],
        ['altavoz4', 'altavoz', hx - 0.4, colg, hz - 0.4, 0.0, 1.6, 0.0, 0.5, 'colgado, entrada derecha'],
        ['micro', 'micro', 1.0, colg, 1.0, 1.0, 0.0, 1.0, 0.18, 'en lo alto, lejos de la esfera y del estrobo'],
        ['camara', 'camara', 0.0, min(3.5, alto - 0.2), 0.0, 0.0, 0.0, 0.0, 0.28, 'cenital (Femto Bolt)'],
        ['foco1', 'foco', -hx + 0.4, techo, -hz + 2.2, -hx + 2.6, 0.0, -hz + 3.4, 50.0,
         'bano, junto a la esfera (no le apunta)'],
        ['foco2', 'foco', -hx + 2.2, techo, -hz + 0.4, -hx + 3.4, 0.0, -hz + 2.6, 50.0,
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


def _punto(cfg, i, v, k, evitar):
    hx, hz = 0.5 * cfg['ancho'] - MARGEN, 0.5 * cfg['fondo'] - MARGEN
    p = None
    for intento in range(10):
        p = (-hx + 2 * hx * h01(i, v, k, intento, 1), -hz + 2 * hz * h01(i, v, k, intento, 2))
        if all(math.hypot(p[0] - e[0], p[1] - e[2]) > APARTE for e in evitar):
            return p
    return p


def _clave(cfg, evitar):
    return (cfg['ancho'], cfg['fondo'], cfg['llegada'], tuple(evitar))


def plan(cfg, i, hasta, evitar=()):
    """Los tramos de la persona i hasta el instante 'hasta' (s desde que se
    abrio la sala): [t0, t1, (x0, z0), (x1, z1), dentro, andando]."""
    clave = _clave(cfg, evitar)
    pl = _PLANES.get(i)
    if pl is None or pl['clave'] != clave:
        pl = _PLANES[i] = dict(clave=clave, tramos=[], t=0.0, vuelta=0)
    puerta = (0.0, 0.5 * cfg['fondo'] - 0.3)
    fuera = (0.0, 0.5 * cfg['fondo'] + 1.0)
    tr = pl['tramos']
    if not tr:
        llega = i * cfg['llegada'] + 4.0 * h01(i, 0, 9)
        tr.append([0.0, llega, fuera, fuera, False, False])
    while tr[-1][1] <= hasta:
        v = pl['vuelta']
        t = tr[-1][1]
        p = puerta
        tr.append([t, t + 1.0, (0.0, 0.5 * cfg['fondo']), puerta, True, True])     # cruza la puerta
        t += 1.0
        for k in range(3 + int(5 * h01(i, v, 3))):
            q = _punto(cfg, i, v, k, evitar)
            dt = math.hypot(q[0] - p[0], q[1] - p[1]) / VELOCIDAD
            tr.append([t, t + dt, p, q, True, True])
            t += dt
            quieto = 3.0 + 9.0 * h01(i, v, k, 4)
            tr.append([t, t + quieto, q, q, True, False])
            t += quieto
            p = q
        dt = math.hypot(puerta[0] - p[0], puerta[1] - p[1]) / VELOCIDAD
        tr.append([t, t + dt, p, puerta, True, True])
        t += dt
        tr.append([t, t + 20.0 + 40.0 * h01(i, v, 5), fuera, fuera, False, False])
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

_SALA = dict(t0=None, frame=None, equipos=None, audio=None, t_audio=None, forzar=False, manuales=[])
MODOS_LUZ = ['apagado', 'prueba']
VISTAS = ['libre', 'cenital']


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
                luz_casa=max(0.0, _p('Luzcasa', 0.25)), vista=_menu('Vista', VISTAS, 0))


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


def vista(que, frame=None):
    """La camara libre: orbita alrededor del centro de la sala."""
    a = math.radians(_p('Orbita', 30.0))
    R = _p('Distancia', 11.0)
    return dict(tx=R * math.sin(a), ty=_p('Alturavista', 5.0), tz=R * math.cos(a)).get(que, 0.0)


def _filas_sala(c):
    W, F, H = c['ancho'], c['fondo'], c['alto']
    hx, hz = W / 2.0, F / 2.0
    zx, zz = c['zona_ancho'] / 2.0, c['zona_fondo'] / 2.0
    g = 0.03
    f = [[0, -0.02, 0, 0, 0, 0, W, 0.02, F] + list(COL_SUELO),
         [0, 0, -hz, 0, 0, 0, W, H, 0.05] + list(COL_PARED),
         [-hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
         [hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
         [0, 0, hz, 0, 0, 0, 1.2, 0.01, 0.12] + list(COL_PUERTA)]
    for x, z, sx, sz in ((0, -zz, 2 * zx, g), (0, zz, 2 * zx, g), (-zx, 0, g, 2 * zz), (zx, 0, g, 2 * zz)):
        f.append([x, 0.0, z, 0, 0, 0, sx, 0.005, sz] + list(COL_ZONA))
    return f


def _filas_equipos(c, eq, t):
    out = []
    for e in eq:
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
    out = []
    for i, x, z, h, _ in personas(c, t, evitar_de(eq)):
        col = (0.35 + 0.4 * h01(i, 11), 0.35 + 0.4 * h01(i, 12), 0.35 + 0.4 * h01(i, 13))
        out.append([x, 0.0, z, 0, 0, 0, 0.42, h, 0.28] + list(col))
    return out


def filas(nombre):
    """Las instancias de los Script CHOP i_sala, i_equipos e i_personas."""
    c = cfg()
    eq = equipos()
    t = ahora()
    if nombre == 'i_sala':
        return _filas_sala(c)
    if nombre == 'i_equipos':
        return _filas_equipos(c, eq, t)
    if nombre == 'i_personas':
        return _filas_personas(c, eq, t) if c['activa'] else []
    return []


def frame_tick():
    """Cada fotograma (latido_sala): las personas y los aparatos se redibujan."""
    if not _p('Activa', True):
        return
    for nm in ('i_personas', 'i_equipos'):
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
