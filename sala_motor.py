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
#               esquina. (Hasta la v6) el suelo del publico (Zonaancho x Zonafondo) se
#               delimita con una tarima, un borde claro y una reticula de
#               0,5 m; el publico se para dentro. Las aristas de la sala, el
#               umbral de la puerta y una reticula de 1 m en suelo y paredes
#               (geometria 'lineas', Constant MAT) dan la perspectiva aunque
#               la sala este a oscuras.
#   v4          la esfera, a 1 m de cada pared de su esquina; la reticula de
#               0,5 m cubre todo el suelo; el publico, sin cabeza (un tronco);
#               Demo elige la visita (paseo, grupo, llena, goteo, vacia) y
#               Luzesfera la luz de la esfera sobre la sala (0: apagada).
#   v7          sin la zona de la camara: la camara cenital ve todo el suelo
#               (fov_cenital) y el publico se para en cualquier sitio de la
#               sala, lejos de las paredes, la esfera y el estrobo.
#   v8          la esfera gira para que el planeta mire al centro de la sala
#               (giro_esfera; Girosfera lo ajusta a mano).
#   v10         ...y desde la v10 mira a la camara de la entrada, con el centro
#               de la imagen medido en la malla (uv_centro), no supuesto.
#   v11         ...y se inclina hacia la altura de esa camara (inclina_esfera;
#               Inclinasfera lo retoca): antes parecia mirar al suelo.
#   v12         la imagen de FASE1 va de frente sobre la bola (Script SOP
#               'frente' en sala_virtual), no envuelta: se ve como en FASE1.
#   v13         MONIGOTES: cada persona es un monigote de hombre (i par) o de
#               mujer (i impar), como los letreros de los aseos, de piezas
#               instanciadas (cabeza, cuerpo o vestido, brazos y piernas) con
#               la misma altura y dentro de la huella del tronco de antes; las
#               piernas se balancean al andar. Monigotes apagado vuelve al
#               tronco. Arcoquietud: un arco ambar en el suelo que se completa
#               en Tfila mientras la persona sigue quieta (el contador de la fila).
#               DEMO GENOZILLA (Demo = genozilla): el publico juega a GENoZilla
#               capitulo a capitulo, con su coreografia escrita (tramos [t,
#               persona, destino]: un punto, una celda del planeta o algo
#               relativo al monstruo, que se pasan a metros en el momento), un
#               titulo al empezar cada capitulo, un rotulo que explica lo que
#               pasa y la vista juego (la sala y la imagen de FASE1 lado a lado).
#               La sala guarda la escena de FASE1 (y su mundo) al entrar y la
#               devuelve al salir; con Guion, prepara cada capitulo con
#               guion_demo del motor de FASE1 (motor v119).
#   v14         GENoZilla anda un tercio mas lento (motor v120, fase 33 v4): los
#               capitulos que lo frenan a proposito lo frenan en proporcion
#               (Canal: Pasomonstruo 72; Relampago: 120) y el Cerco dura 2,5 s mas
#               (21,5 s): al abrirse, los otros tres se quedan donde estan (ya no lo
#               siguen) y le da tiempo a escapar; la comprobacion mira que salga de la
#               celda en la que lo acorralaron.
#   v15         EL PUBLICO A FASE1 EN TODAS LAS DEMOS (Alimentar, encendido): con la
#               sala activa, FASE1 ve al publico de cualquier demo (paseo, grupo, llena,
#               goteo...) por su sala simulada (Fuente = simulada y la tabla
#               sala_personas, como en GENoZilla), y lo marca con un anillo en el globo
#               (motor v132, Marcapublico: tambien sin Modojuego). Al apagar Alimentar o
#               Activa, FASE1 vuelve a su Fuente y a su tabla de antes.
#   v16         GENOZILLA SOBRE EL MUNDO DE FASE1 (motor v133): cada capitulo empieza en
#               el mundo con el que entro la demo (la copia que guarda entrar), no en uno
#               vacio; el guion solo despeja lo que el capitulo necesita libre. El Cerco,
#               con seis visitantes (las seis vecinas del monstruo: en un mundo lleno, las
#               dos que no cerraba el cerco de cuatro le daban de comer). Construir y
#               Aparece se comprueban por lo nuevo (coronas y brotes del capitulo). El
#               Oceano de FASE1 se respeta (se apagaba: el mundo vacio era todo mar).
#   v17         EL PISOTON, CON TRES CABEZAS SEPARADAS (sitio_pison): con tres casillas o
#               mas mirando a la celda del monstruo, uno en cada una; con dos, dos en la
#               primera (en su lado lejos de la otra, a 0,42 m entre si) y el tercero en
#               el lado lejos de la segunda; con una, un triangulo de 0,38 m de lado.
#               Antes, dos en la misma casilla a 0,37 m y el tercero a 0,38, junto a
#               Separacioncabezas (0,35, fase 24): en TouchDesigner dos cabezas se
#               fundian en una, el pisoton contaba dos y no le bajaba acum.
#   v18         LAS DEMOS, REHECHAS POR SECCIONES Y CASOS. Demo: 1 paseo (entran y
#               salen, a veces en grupo; algo de la obra los detiene y, quietos,
#               construyen), 2 probabilidad (estrato humano: la probabilidad minima, la
#               de una persona quieta y la de un grupo, medidas con una lluvia de notas
#               sobre una celda testigo y una vacia), 3 huella (la huella inevitable:
#               quietos construyen y dejan inclusiones; la fila cava tantas conchas como
#               personas, 3 y luego 5), 4 llena (la sala llena, entrando y saliendo), 5
#               genozilla (como estaba) y vacia. Todas las juega el director de GENoZilla:
#               titulo al empezar cada caso (la seccion, el caso y de que va), rotulo abajo,
#               cabecera arriba a la derecha (cabecera_texto: la seccion, el caso y lo que
#               mide FASE1 en vivo) y FASE1 guardada al entrar y devuelta al salir. Sin
#               Modojuego en las demos nuevas. LA CAMARA DE FASE1 SIGUE A LAS CELDAS donde
#               pasan las cosas (foco de cada caso: la gente quieta, la celda testigo, la
#               fila, el monstruo), sin cambiar de altura (motor v140, foco_camara;
#               Siguecamara la apaga). Fuera las demos grupo y goteo (el grupo va dentro del
#               paseo) y el parametro Llegada; Personas es la gente de la sala llena.
#   v19         LAS DEMOS DE SECCION YA NO TOCAN EL GIRO DE FASE1. Hasta la v18, cada caso
#               de paseo, probabilidad, huella y llena ponia Barsperturn 450 (el giro casi
#               parado: el giro vivo no se notaba) y la camara de globo perseguia a las
#               celdas de la gente: al ir de unas a otras, el planeta parecia girar a un
#               lado y al otro. Ahora el Barsperturn de la demo es solo de GENoZilla (como
#               en la v17) y Siguecamara viene apagado (sala_virtual v31 lo apaga una vez).
#               Y la Demo por defecto es la vacia: la v18 hizo del paseo una demo que toma
#               FASE1 (Fuente simulada, sin Modojuego, notas de la gente quieta y, al
#               salir, el mundo de antes); la huella entierra 7 conchas de una vez para
#               que la fila cave y vuelve al mundo de entrada en cada caso. Ninguna debe
#               jugar sola: se eligen a mano.
#   v20         LA SALA LLENA SE VA LLENANDO, SIN POZOS POR TODAS PARTES. La seccion fija
#               Modofila = recta, Minfila 3 y Tfila 5 mientras dura (los devuelve al salir).
#               Entran de uno en uno hasta LLENA_LLENA (55 s) y cada quieto ocupa una
#               casilla de columna y fila pares (sitios_llena): dos quietos nunca son
#               vecinos y no forman fila. Despues cambian de sitio o se van y vuelven;
#               una sola vez (LLENA_LINEA, 62-76 s) tres en linea recta abren un pozo
#               a proposito; a los 100 s se vacia. 120 s (antes 90: entraban casi a la
#               vez a una rejilla apretada y cada corrillo de tres era una escision).
#   v21         LAS DEMOS TOMAN EL MUNDO DE FASE1 DONDE ESTA Y NO TOCAN SU GIRO. Hasta la
#               v20, al entrar se guardaba el mundo y al salir se devolvia (el planeta
#               volvia atras: ciclos, conchas y lo construido durante la demo); la
#               probabilidad y la huella volvian al mundo de la entrada en cada caso
#               (mundo = 'base') y despejaban celdas; la fila de la huella enterraba 7
#               conchas de golpe; GENoZilla rehacia el mundo en cada capitulo, enterraba 6
#               conchas para sus zanjas y ponia Barsperturn 450 (45 y 9 en el primero y el
#               ultimo). Ahora ninguna demo guarda, devuelve, vacia ni entierra el mundo,
#               ni cambia Barsperturn: el planeta gira siempre con los parametros de FASE1
#               (y su giro vivo) y cierra sus ciclos con sus reglas. Los parametros de la
#               demo si se devuelven al salir. Si el mundo aun no tiene lo que un caso
#               necesita (dos celdas vacias bajo la sala para medir la probabilidad;
#               conchas debajo para que una fila o un grito caven), el caso espera: el
#               titulo dice «Esperando que el mundo evolucione» y para probar que, y lo
#               vuelve a mirar cada ESPERA_CADA s (Siguientecap lo salta).
#   v22         LA OBRA, PROYECTADA EN UNA PANTALLA. Soporte (pagina Sala): pantalla (por
#               defecto) o esfera (la de LEDs de antes). La pantalla cuelga en la pared del
#               fondo, pegada a la de la izquierda y al techo (la esquina de arriba a la
#               izquierda vista desde la entrada), con el render entero de FASE1 (16:9) y
#               Altopantalla de alto (3,6 m: 6,4 x 3,6 m; el planeta, el 85 % del alto,
#               unos 3 m: tres veces la esfera de 1 m). Un marco oscuro detras y un
#               proyector colgado del techo delante. Las vistas (entrada, visitante) miran a
#               la pantalla; la peana de la esfera no se dibuja. La fila 'esfera' de la
#               tabla equipos sigue: es el sitio que la gente deja libre junto al estrobo.
# =============================================================================

SALA_VERSION = 'sala v22'

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
# v3: las lineas (Constant MAT: se ven aunque la sala este a oscuras)
LIN_ARISTA = (0.55, 0.55, 0.58)         # las aristas de la sala
LIN_PARED = (0.16, 0.16, 0.18)          # la reticula de 1 m en paredes y suelo
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
# v18: en todas las demos las personas las mueve la coreografia de su caso (el
# director de demos, mas abajo): tramos [t0, t1, (x0, z0), (x1, z1), dentro, andando]
# que pone mover(). Las coreografias salen de hashes de la persona y del tramo: la
# misma sala da la misma historia.

_PLANES = {}


def zona(cfg):
    """(medio ancho, medio fondo) del suelo donde se para el publico. v7: todo
    el suelo de la sala, menos MARGEN junto a las paredes (la camara cenital
    lo ve entero; antes, la zona Zonaancho x Zonafondo)."""
    return (max(0.3, 0.5 * cfg['ancho'] - MARGEN), max(0.3, 0.5 * cfg['fondo'] - MARGEN))


def _punto(cfg, i, v, k, evitar):
    hx, hz = zona(cfg)                  # v3: el publico se para en su suelo (antes, en toda la sala)
    p = None
    for intento in range(10):
        p = (-hx + 2 * hx * h01(i, v, k, intento, 1), -hz + 2 * hz * h01(i, v, k, intento, 2))
        if all(math.hypot(p[0] - e[0], p[1] - e[2]) > APARTE for e in evitar) and not _escondido(p, evitar):
            return p
    return p


def _dist_tramo(p, q, e):
    """Distancia en planta del aparato e (x, y, z) al tramo de p a q."""
    dx, dz = q[0] - p[0], q[1] - p[1]
    L2 = dx * dx + dz * dz
    u = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((e[0] - p[0]) * dx + (e[2] - p[1]) * dz) / L2))
    return math.hypot(p[0] + u * dx - e[0], p[1] + u * dz - e[2])


def _escondido(q, evitar):
    """v7: el punto queda detras de la esfera o del estrobo, mirando desde el
    centro de la sala (en su esquina): para llegar habria que pasar por encima."""
    return any(_dist_tramo((0.0, 0.0), q, e) <= APARTE for e in evitar)


def _libre(cfg, q, evitar):
    """El punto q dentro del suelo del publico, a APARTE de la esfera y del
    estrobo y sin quedar escondido detras de ellos (si no, se acerca al
    centro de la sala)."""
    zx, zz = zona(cfg)
    x, z = q
    for _ in range(12):
        x, z = max(-zx, min(zx, x)), max(-zz, min(zz, z))
        cerca = [e for e in evitar if math.hypot(x - e[0], z - e[2]) <= APARTE]
        if cerca:
            e = cerca[0]
            d = math.hypot(x - e[0], z - e[2]) or 1e-6
            k = (APARTE + 0.15) / d
            nx, nz = e[0] + (x - e[0]) * k, e[2] + (z - e[2]) * k
            if abs(nx) > zx or abs(nz) > zz:            # contra la pared: hacia el centro
                x, z = 0.85 * x, 0.85 * z
            else:
                x, z = nx, nz
        elif _escondido((x, z), evitar):
            x, z = 0.85 * x, 0.85 * z
        else:
            break
    return (max(-zx, min(zx, x)), max(-zz, min(zz, z)))


DESVIO = 0.4                # v7: m de mas al rodear la esfera o el estrobo


def _camino(cfg, p, q, evitar, prof=0):
    """Los puntos de p a q (sin p): si el tramo recto pasa a menos de APARTE
    de la esfera o del estrobo, lo rodea por el lado que da al centro."""
    if prof < 3:
        for e in evitar:
            if _dist_tramo(p, q, e) <= APARTE:
                dx, dz = q[0] - p[0], q[1] - p[1]
                L = math.hypot(dx, dz) or 1e-6
                nx, nz = -dz / L, dx / L                # perpendicular al tramo
                if nx * (0.0 - e[0]) + nz * (0.0 - e[2]) < 0:
                    nx, nz = -nx, -nz                   # hacia el centro de la sala
                w = _libre(cfg, (e[0] + nx * (APARTE + DESVIO), e[2] + nz * (APARTE + DESVIO)), evitar)
                return _camino(cfg, p, w, evitar, prof + 1) + _camino(cfg, w, q, evitar, prof + 1)
    return [q]


def _andar(tr, t, p, q, cfg=None, evitar=()):
    pts = _camino(cfg, p, q, evitar) if cfg is not None and evitar else [q]
    for r in pts:
        dt = math.hypot(r[0] - p[0], r[1] - p[1]) / VELOCIDAD
        tr.append([t, t + dt, p, r, True, True])
        t, p = t + dt, r
    return t


def plan(cfg, i, hasta, evitar=()):
    """Los tramos de la persona i hasta el instante 'hasta' (s desde que se abrio la
    sala): [t0, t1, (x0, z0), (x1, z1), dentro, andando]. v18: los pone la coreografia
    del caso de la demo (tramos_demo); en la demo vacia, nadie."""
    if DEMOS[cfg.get('demo', 0) % len(DEMOS)] == 'vacia':
        fuera = (0.0, 0.5 * cfg['fondo'] + 1.0)
        return [[0.0, hasta + 3600.0, fuera, fuera, False, False]]
    return tramos_demo(cfg, i, hasta)


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


def n_personas(cfg):
    """Las personas de la sala: las de la seccion de la demo (v18; en la sala llena,
    Personas, al menos LLENA_MIN), ninguna en la vacia."""
    demo = DEMOS[cfg.get('demo', 0) % len(DEMOS)]
    sec = SECCIONES.get(demo)
    if sec is None:
        return 0
    n = sec['personas']
    if n == 'personas':
        return max(LLENA_MIN, min(LLENA_MAX, int(cfg.get('personas', LLENA_MIN))))
    return int(n)


def personas(cfg, t, evitar=()):
    """[(i, x, z, altura, andando)] de las personas dentro de la sala en t."""
    out = []
    for i in range(n_personas(cfg)):
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
    if tipo in ('voz', 'grito'):        # v13: una vocal (habla) o un grito: armonicos y algo de aire
        f0 = (110.0 if semilla % 2 == 0 else 190.0) * (1.0 + 0.15 * h01(semilla, 43))
        env = np.minimum(1.0, t / 0.02) * np.exp(-t / (0.12 if tipo == 'voz' else 0.25))
        x = sum(np.sin(2 * math.pi * f0 * h * t) / h for h in (1, 2, 3, 4, 5))
        a = 0.08 if tipo == 'voz' else 0.2
        return a * env * (0.9 * x / 2.3 + 0.1 * _ruido(np, j, semilla))
    return np.zeros(n)


DURA = dict(palmada=0.03, tos=0.3, paso=0.12, clic=0.004, voz=0.35, grito=0.6)


def eventos(cfg, ta, tb, evitar=()):
    """Los ruidos de la sala en [ta, tb): [(t, tipo, (x, y, z), semilla)]."""
    out = []
    for i in range(n_personas(cfg)):
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
            modo = ruido_demo(t)        # v13: la demo GENoZilla habla, calla o grita en sus tramos
            if modo == 'silencio':
                continue
            if modo == 'habla':
                tasa = max(tasa, HABLA_TASA)
            if h01(i, k, 7) >= tasa * RANURA:
                continue
            p = posicion(cfg, i, t, evitar)
            if p is not None:
                tipo = 'voz' if modo == 'habla' else ('palmada' if h01(i, k, 9) < 0.5 else 'tos')
                out.append((t, tipo, (p[0], BOCA, p[1]), i * 1000 + k))
        out += eventos_grito(cfg, i, ta, tb, evitar)
    return out


HABLA_TASA = 0.9            # v13: voces por segundo y persona cuando la sala habla (demo GENoZilla)
GRITO_HZ = 8.0              # palmadas por segundo de cada persona en el grito, todas a la vez
GRITO_VOZ = 0.45            # s entre dos voces del grito de cada persona


def eventos_grito(cfg, i, ta, tb, evitar=()):
    """v13: el grito colectivo de la demo (capitulo Grito): palmadas al unisono, GRITO_HZ
    por segundo, y voces de cada persona, con la ganancia del tramo (D4)."""
    out = []
    tr = [r for r in _GZ.get('ruido', ()) if r[2] == 'grito' and r[0] < tb and r[1] > ta]
    for t0, t1, _ in tr:
        a, b = max(ta, t0), min(tb, t1)
        k = int(math.ceil((a - t0) * GRITO_HZ - 1e-9))
        while t0 + k / GRITO_HZ < b:
            t = t0 + k / GRITO_HZ + 0.012 * h01(i, k, 41)
            p = posicion(cfg, i, t, evitar)
            if p is not None and a <= t < b:
                out.append((t, 'palmada', (p[0], BOCA, p[1]), -(i * 1000 + k + 1)))
            k += 1
        k = int(math.ceil((a - t0) / GRITO_VOZ - 1e-9))
        while t0 + k * GRITO_VOZ < b:
            t = t0 + k * GRITO_VOZ + 0.1 * h01(i, k, 42)
            p = posicion(cfg, i, t, evitar)
            if p is not None and a <= t < b:
                out.append((t, 'grito', (p[0], BOCA, p[1]), -(i * 1000 + k + 501)))
            k += 1
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
        if semilla < 0:                 # v13: el grito de la demo, con su ganancia (D4)
            y = y * float(_GZ.get('ganancia', 1.0))
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
SOPORTES = ['pantalla', 'esfera']        # v22: donde se ve la obra (la pantalla proyectada, por defecto)
SOPORTES_ETIQUETAS = ['Pantalla proyectada (en la esquina de arriba a la izquierda)', 'Esfera de LEDs (1 m)']
PANT_ALTO = 3.6             # v22: m de alto de la pantalla (el planeta, ENCUADRE de ese alto: ~3 m)
PANT_ASPECTO = 16.0 / 9.0   # el render de FASE1, entero
PANT_MARGEN = 0.12          # m de la pantalla a la pared de la izquierda y al techo
PANT_SEPARA = 0.06          # m de la pantalla a la pared del fondo (el marco, detras)
PANT_MARCO = 0.08           # m que el marco sobresale por cada lado
COL_MARCO = (0.03, 0.03, 0.035)
COL_PROYECTOR = (0.12, 0.12, 0.13)
VISTAS = ['visitante', 'entrada', 'orbita', 'cenital', 'juego']   # v2; hasta la v1, libre (= orbita) y cenital
# v13: juego, la sala desde la entrada a la izquierda y la imagen de FASE1 a la derecha


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
                personas=max(0, int(_p('Personas', 18))),
                ruido_publico=max(0.0, _p('Ruidopublico', 0.05)), reaccion=max(0.0, _p('Reaccion', 3.0)),
                volumen_drone=max(0.0, _p('Volumendrone', 0.5)),
                modo_luz=_menu('Modoluz', MODOS_LUZ, 1), hz_prueba=_p('Hzprueba', 2.5),
                luz_casa=max(0.0, _p('Luzcasa', 0.06)), vista=_menu('Vista', VISTAS, 0),
                bruma=max(0.0, min(1.0, _p('Bruma', 0.5))), demo=_menu('Demo', DEMOS, 0),
                sigue_camara=bool(_p('Siguecamara', False)),     # v19: apagado por defecto
                luz_esfera=max(0.0, _p('Luzesfera', 0.0)), giro_esfera=_p('Girosfera', 0.0),
                inclina_esfera=_p('Inclinasfera', 0.0),
                monigotes=bool(_p('Monigotes', True)), arco_quietud=bool(_p('Arcoquietud', False)),
                col_monigote=(_p('Colormonigoter', COL_MONIGOTE[0]), _p('Colormonigoteg', COL_MONIGOTE[1]),
                              _p('Colormonigoteb', COL_MONIGOTE[2])),
                capitulo=_menu('Capitulo', CAP_NOMBRES, 0), buclecap=bool(_p('Buclecap', True)),
                guion=bool(_p('Guion', True)), alimentar=bool(_p('Alimentar', True)),
                soporte=_menu('Soporte', SOPORTES, 0), alto_pantalla=_p('Altopantalla', PANT_ALTO))   # v22


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


def es_pantalla(c=None):
    """v22: la obra se ve en la pantalla proyectada (Soporte = pantalla), no en la esfera."""
    c = c or cfg()
    return SOPORTES[c.get('soporte', 0) % len(SOPORTES)] == 'pantalla'


def pantalla_rect(c=None):
    """v22: la pantalla en la pared del fondo, pegada a la izquierda y al techo: dict con
    x0 x1 y0 y1 (sus bordes), z (su plano), w h (ancho y alto) y cx cy (su centro). El
    alto es Altopantalla (como mucho el de la sala menos los margenes) y el ancho, 16:9;
    si no cabe a lo ancho, se encoge."""
    c = c or cfg()
    hx, hz = 0.5 * c['ancho'], 0.5 * c['fondo']
    h = max(0.5, min(float(c.get('alto_pantalla', PANT_ALTO)), c['alto'] - 2.0 * PANT_MARGEN))
    w = h * PANT_ASPECTO
    if w > c['ancho'] - 2.0 * PANT_MARGEN:
        w = c['ancho'] - 2.0 * PANT_MARGEN
        h = w / PANT_ASPECTO
    x0, y1 = -hx + PANT_MARGEN, c['alto'] - PANT_MARGEN
    return dict(x0=x0, x1=x0 + w, y0=y1 - h, y1=y1, z=-hz + PANT_SEPARA, w=w, h=h, cx=x0 + 0.5 * w,
                cy=y1 - 0.5 * h)


def pantalla(que, frame=None):
    """v22: para las expresiones del Geometry COMP 'pantalla' (un cuadrado de 1 x 1 en XY):
    tx ty tz (su centro) y sx sy (su ancho y su alto)."""
    try:
        c = cfg()
        if que == 'scale':                  # sin Soporte = pantalla, casi 0 (no se ve)
            return 1.0 if es_pantalla(c) else OCULTA
        r = pantalla_rect(c)
        return dict(tx=r['cx'], ty=r['cy'], tz=r['z'], sx=r['w'], sy=r['h'])[que]
    except Exception:
        return 0.0


OCULTA = 1e-4               # v22: la escala de la obra que no es el Soporte (los render la llevan igual)


def escala_esfera(frame=None):
    """v22: la escala del Geometry COMP de la esfera: 1 con Soporte = esfera; si no, casi 0."""
    try:
        return OCULTA if es_pantalla() else 1.0
    except Exception:
        return 1.0


def obra(c=None, eq=None):
    """v22: el punto donde se ve la obra: el centro de la pantalla o el de la esfera."""
    c = c or cfg()
    if es_pantalla(c):
        r = pantalla_rect(c)
        return (r['cx'], r['cy'], r['z'])
    eq = equipos() if eq is None else eq
    esf = next((e for e in eq if e['tipo'] == 'esfera'), None)
    return esf['pos'] if esf is not None else (0.0, 1.3, -0.5 * c['fondo'])


def ojos(c=None, frame=None):
    """(posicion, a donde mira) de la camara principal segun Vista."""
    c = c or cfg()
    eq = equipos()
    esf = next((e for e in eq if e['tipo'] == 'esfera'), None)
    mira = obra(c, eq)              # v22: la pantalla (o la esfera)
    modo = VISTAS[c['vista'] % len(VISTAS)]
    if modo == 'visitante':
        x, z = paseo_visitante(c, ahora(), evitar_de(eq))
        return (x, OJOS, z), mira
    if modo in ('entrada', 'juego'):          # v13: juego, desde la entrada (a la izquierda del monitor)
        return vista_entrada(c, esf, modo)
    if modo == 'cenital':
        cam = next((e for e in eq if e['tipo'] == 'camara'), None)
        p = cam['pos'] if cam is not None else (0.0, 3.5, 0.0)
        return p, (p[0], 0.0, p[2] - 0.3)
    a = math.radians(_p('Orbita', 30.0))
    R = _p('Distancia', 11.0)
    return (R * math.sin(a), _p('Alturavista', 5.0), R * math.cos(a)), (0.0, 1.0, 0.0)


ENTRADA_ATRAS = 2.2         # v3: m por detras de la puerta (la pared de la entrada esta abierta)
ENTRADA_ALTO = 2.8          # m: algo por encima de los ojos, para ver la reticula del suelo


def vista_entrada(c, esf=None, modo='entrada'):
    """(posicion, a donde mira) de la vista entrada (v3): un poco por detras
    de la puerta y por encima de la gente, mirando hacia abajo y hacia el
    fondo, entre el centro del suelo del publico y la esfera. Se ven la
    reticula del publico entera, la esfera en su esquina y las paredes en
    perspectiva."""
    hz = 0.5 * c['fondo']
    p = (0.0, min(ENTRADA_ALTO, c['alto'] - 0.3), hz + ENTRADA_ATRAS)
    if es_pantalla(c):              # v22: inclinada para que quepa la pantalla entera, hasta su borde de arriba
        r = pantalla_rect(c)
        if modo == 'juego':
            v = FOV_JUEGO
        else:
            v = 2.0 * math.degrees(math.atan(math.tan(math.radians(0.5 * 80.0)) * 720.0 / 1280.0))
        arriba = math.degrees(math.atan2(r['y1'] - p[1], p[2] - r['z']))
        cab = math.radians(arriba - (0.5 * v - ENTRADA_HOLGURA))
        zm = -0.2 * hz                  # hacia el fondo, como con la esfera
        return p, (0.3 * r['cx'], p[1] + math.tan(cab) * (p[2] - zm), zm)
    if esf is None:
        return p, (0.0, 0.0, -0.25 * hz)
    return p, (0.3 * esf['x'], 0.25 * esf['y'], 0.2 * esf['z'])


ENTRADA_HOLGURA = 3.0       # v22: grados entre el borde de arriba de la pantalla y el del cuadro

CENITAL_ASPECTO = 320.0 / 288.0     # render_cenital (y la miniatura, 200 x 180, v9)


def fov_cenital(c=None, frame=None):
    """v7: el angulo horizontal (grados) de la camara cenital para que vea
    todo el suelo de la sala desde donde esta en la tabla, con 2 grados de
    holgura. Ojo: una Femto Bolt en NFOV ve unos 75 x 65 grados; a 3,5 m
    no cubre 8 x 6 m."""
    c = c or cfg()
    cam = next((e for e in equipos() if e['tipo'] == 'camara'), None)
    x, y, z = cam['pos'] if cam is not None else (0.0, 3.5, 0.0)
    y = max(0.5, y)
    medio_x = 0.5 * c['ancho'] + abs(x)
    medio_z = 0.5 * c['fondo'] + abs(z)
    h = math.atan(medio_x / y)
    v = math.atan(math.tan(math.atan(medio_z / y)) * CENITAL_ASPECTO)     # el fondo, en angulo horizontal
    return min(170.0, 2.0 * math.degrees(max(h, v)) + 2.0)


def vista(que, frame=None):
    """La camara principal (Vista): tx ty tz de su posicion, mx my mz de a
    donde mira (el Null 'mirada'), y fov."""
    try:
        c = cfg()
        p, m = ojos(c)
        if que == 'fov':
            modo = VISTAS[c['vista'] % len(VISTAS)]
            return fov_cenital(c) if modo == 'cenital' else {'entrada': 80.0, 'juego': FOV_JUEGO}.get(modo, 62.0)
        if que in ('mx', 'my', 'mz'):
            return m[('mx', 'my', 'mz').index(que)]
        return p[('tx', 'ty', 'tz').index(que)]
    except Exception:
        return 0.0


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


def hacia_esfera(c=None):
    """v10: el punto (x, z) al que mira el planeta: donde esta la camara de la
    vista entrada, la que mira la sala desde la puerta (antes, el centro de la
    sala, que desde la entrada lo dejaba unos 40 grados de lado)."""
    c = c or cfg()
    return (0.0, 0.5 * c['fondo'] + ENTRADA_ATRAS)


def giro_esfera(frame=None):
    """El giro (ry, grados) de la esfera para que su +Z, donde el Script SOP
    'frente' pone la imagen de FASE1 de frente (v12), mire a hacia_esfera(),
    mas Girosfera para ajustarlo a mano."""
    try:
        e = equipo('esfera')
        if e is None:
            return 0.0
        c = cfg()
        hx, hz = hacia_esfera(c)
        return math.degrees(math.atan2(hx - e['x'], hz - e['z'])) + float(c['giro_esfera'])
    except Exception:
        return 0.0


def inclina_esfera(frame=None):
    """v11: la inclinacion (rx, grados) del Transform SOP 'inclinar' de la
    esfera, para que el planeta mire hacia arriba, a la altura de la camara de
    la entrada (a 2,8 m; la esfera, a 1,3): sin ella, el centro de la imagen
    queda en el ecuador de la bola y desde la entrada parece mirar al suelo.
    Inclinasfera suma grados hacia arriba. Negativo: girar sobre X hacia
    atras levanta el +Z."""
    try:
        e = equipo('esfera')
        if e is None:
            return 0.0
        c = cfg()
        hx, hz = hacia_esfera(c)
        alto = min(ENTRADA_ALTO, c['alto'] - 0.3)
        elev = math.degrees(math.atan2(alto - e['y'], math.hypot(hx - e['x'], hz - e['z'])))
        return -(elev + float(c['inclina_esfera']))
    except Exception:
        return 0.0


def luz_esfera(que, frame=None):
    """La luz de la esfera (Light COMP luz_esfera): tx ty tz y r g b d. v22: con la
    pantalla, medio metro delante de su centro."""
    try:
        e = equipo('esfera')
        if que in ('tx', 'ty', 'tz'):
            if es_pantalla():
                x, y, z = obra()
                return (x, y, z + 0.5)[('tx', 'ty', 'tz').index(que)]
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
    return [[0, -0.02, 0, 0, 0, 0, W, 0.02, F] + list(COL_SUELO),
            [0, 0, -hz, 0, 0, 0, W, H, 0.05] + list(COL_PARED),
            [-hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
            [hx, 0, 0, 0, 0, 0, 0.05, H, F] + list(COL_PARED),
            [0, 0, hz, 0, 0, 0, PUERTA_ANCHO, 0.01, 0.12] + list(COL_PUERTA)]


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
    GRID_SALA m en las tres paredes. v7: sin la zona de la camara (la
    camara cenital ve todo el suelo)."""
    W, F, H = c['ancho'], c['fondo'], c['alto']
    hx, hz = W / 2.0, F / 2.0
    y0, yz = 0.008, 0.012           # la reticula y, encima, el umbral de la puerta
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
            if es_pantalla(c):              # v22: con la pantalla, ni esfera ni peana
                continue
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
    if es_pantalla(c):                      # v22: el marco de la pantalla y el proyector
        r = pantalla_rect(c)
        out.append([r['cx'], r['y0'] - PANT_MARCO, r['z'] - 0.5 * PANT_SEPARA, 0, 0, 0, r['w'] + 2 * PANT_MARCO,
                    r['h'] + 2 * PANT_MARCO, 0.5 * PANT_SEPARA] + list(COL_MARCO))
        out.append([r['cx'], c['alto'] - 0.45, r['z'] + PROYECTOR_A, 0, 0, 0, 0.45, 0.18, 0.40] + list(COL_PROYECTOR))
        out.append([r['cx'], c['alto'] - 0.27, r['z'] + PROYECTOR_A, 0, 0, 0, 0.04, 0.27, 0.04] + list(COL_PROYECTOR))
    return out


PROYECTOR_A = 4.2           # v22: m de la pantalla al proyector (colgado del techo, delante)


def _filas_personas(c, eq, t):
    """El cuerpo de cada persona. v13: con Monigotes, las cajas de su monigote (cuerpo,
    brazos y piernas; ver piezas_personas); sin el, un tronco de toda su altura, de ropa
    oscura (v4: sin cabeza)."""
    if c.get('monigotes', True):
        return piezas_personas(c, eq, t)['cajas']
    out = []
    for i, x, z, h, _ in personas(c, t, evitar_de(eq)):
        col = (0.10 + 0.22 * h01(i, 11), 0.10 + 0.22 * h01(i, 12), 0.10 + 0.22 * h01(i, 13))
        out.append([x, 0.0, z, 0, 0, 0, TRONCO[0], h, TRONCO[1]] + list(col))
    return out


# -----------------------------------------------------------------------------
# v13: monigotes de hombre y de mujer (los letreros de los aseos)
# -----------------------------------------------------------------------------
# Un monigote es un punado de piezas instanciadas, con la coronilla a la altura de
# la persona y dentro de la huella del tronco (TRONCO, 0,42 x 0,26 m, girado como
# ella): la camara cenital y la fase 24 los ven igual. Las medidas del encargo son
# para ALTURA_REF; lo vertical escala con la altura y lo ancho se encaje en el ancho
# del tronco (los brazos del hombre, a sus lados, sumaban 0,52 m: ANCHO_K). Las
# piernas se balancean BALANCEO grados con la fase de lo andado; quietos, rectas.

TRONCO = (0.42, 0.26)       # m: ancho y fondo del tronco (y de la huella del monigote)
ALTURA_REF = 1.75           # m: la altura de las medidas del monigote
ANCHO_K = 0.42 / 0.52       # lo ancho, encajado en el tronco
CABEZA = 0.22
CUELLO = 0.02
CUERPO = (0.36, 0.48, 0.20)             # hombre: caja de hombros redondeados
HOMBROS = 0.10                          # alto de la elipse de los hombros
VESTIDO = (0.16, 0.42, 0.52)            # mujer: cono truncado (arriba, abajo, alto)
BRAZO = (0.08, 0.50, 0.08)
BRAZO_MUJER = 0.42
PIERNA = (0.10, 0.12)                   # hombre (ancho, fondo)
PIERNA_MUJER = (0.06, 0.08)
BALANCEO = 15.0             # grados de las piernas al andar
ZANCADA = 2.0 * PASO * VELOCIDAD        # m de una vuelta del balanceo (dos pasos)
COL_MONIGOTE = (0.93, 0.91, 0.86)
ARCO_R = 0.34               # m: radio del arco de quietud
ARCO_SEGS = 24
ARCO_ANCHO = 0.035


def estado_persona(cfg, i, t, evitar=()):
    """dict(x, z, andando, rumbo, andado, quieto) de la persona i en t, o None fuera
    de la sala. rumbo: hacia donde mira (radianes; 0 = +z), el de su ultimo tramo
    andando (sin ninguno, al fondo de la sala); andado: metros desde que echo a andar
    (la fase del balanceo); quieto: segundos parada en su sitio."""
    tr = plan(cfg, i, t, evitar)
    k = None
    for j in range(len(tr) - 1, -1, -1):
        if tr[j][0] <= t:
            k = j
            break
    if k is None or not tr[k][4]:
        return None
    s = tr[k]
    u = 0.0 if s[1] <= s[0] else max(0.0, min(1.0, (t - s[0]) / (s[1] - s[0])))
    x, z = s[2][0] + (s[3][0] - s[2][0]) * u, s[2][1] + (s[3][1] - s[2][1]) * u
    rumbo, andado, quieto = None, 0.0, 0.0
    for j in range(k, -1, -1):          # mira hacia donde andaba la ultima vez
        q = tr[j]
        if not q[4]:
            break
        dx, dz = q[3][0] - q[2][0], q[3][1] - q[2][1]
        if q[5] and dx * dx + dz * dz > 1e-8:
            rumbo = math.atan2(dx, dz)
            break
    if s[5]:                            # andando: lo andado en este tramo y en los seguidos de antes
        andado = math.hypot(s[3][0] - s[2][0], s[3][1] - s[2][1]) * u
        for j in range(k - 1, -1, -1):
            q = tr[j]
            if not (q[4] and q[5]):
                break
            andado += math.hypot(q[3][0] - q[2][0], q[3][1] - q[2][1])
    else:                               # parada: desde cuando, sin moverse de este sitio
        quieto = t - s[0]
        for j in range(k - 1, -1, -1):
            q = tr[j]
            if not q[4] or q[5] or q[2] != s[2]:
                break
            quieto = t - q[0]
    return dict(x=x, z=z, andando=bool(s[5]), rumbo=math.pi if rumbo is None else rumbo,
                andado=andado, quieto=quieto)


def _fila_pieza(px, y, pz, rx, ry, sx, sy, sz, col):
    return [px, y, pz, rx, ry, 0.0, sx, sy, sz] + list(col)


def piezas_monigote(i, x, z, h, rumbo, andado, andando, col=COL_MONIGOTE):
    """Las piezas del monigote de la persona i: dict(cajas, bolas, conos), filas de
    instancia (tx ty tz rx ry rz sx sy sz r g b). Cajas y conos con la base en ty;
    bolas centradas. Hombre si i es par; mujer si es impar."""
    s = h / ALTURA_REF
    ca, sa = math.cos(rumbo), math.sin(rumbo)
    ry = math.degrees(rumbo)

    def lado(d):                        # d metros a la derecha de la persona (su +x)
        return x + d * ca, z - d * sa
    th = BALANCEO * math.sin(2.0 * math.pi * andado / ZANCADA) if andando else 0.0
    cajas, bolas, conos = [], [], []
    cab = CABEZA * s
    bolas.append(_fila_pieza(x, h - 0.5 * cab, z, 0.0, ry, cab, cab, cab, col))
    arriba = h - cab - CUELLO * s                   # los hombros
    if i % 2 == 0:                                  # hombre
        w = CUERPO[0] * ANCHO_K
        abajo = arriba - CUERPO[1] * s              # la cadera
        cajas.append(_fila_pieza(x, abajo, z, 0.0, ry, w, arriba - abajo - 0.5 * HOMBROS * s, CUERPO[2], col))
        bolas.append(_fila_pieza(x, arriba - 0.5 * HOMBROS * s, z, 0.0, ry, w, HOMBROS * s, CUERPO[2], col))
        bw = BRAZO[0] * ANCHO_K
        for sg in (-1.0, 1.0):
            bx, bz = lado(sg * 0.5 * (w + bw))
            cajas.append(_fila_pieza(bx, arriba - 0.03 * s - BRAZO[1] * s, bz, 0.0, ry, bw, BRAZO[1] * s, BRAZO[2], col))
        pw, pf, sep = PIERNA[0] * ANCHO_K, PIERNA[1], 0.5 * w - 0.5 * PIERNA[0] * ANCHO_K - 0.01
    else:                                           # mujer: el vestido
        abajo = arriba - VESTIDO[2] * s             # el bajo del vestido
        conos.append(_fila_pieza(x, abajo, z, 0.0, ry, VESTIDO[1] * ANCHO_K, VESTIDO[2] * s,
                                 min(TRONCO[1], VESTIDO[1] * ANCHO_K), col))
        bw = BRAZO[0] * ANCHO_K
        for sg in (-1.0, 1.0):                      # los brazos salen del vestido
            bx, bz = lado(sg * (0.5 * TRONCO[0] - 0.5 * bw - 0.025))
            cajas.append(_fila_pieza(bx, arriba - 0.03 * s - BRAZO_MUJER * s, bz, 0.0, ry, bw, BRAZO_MUJER * s,
                                     BRAZO[2], col))
        pw, pf, sep = PIERNA_MUJER[0], PIERNA_MUJER[1], 0.06
    for sg in (-1.0, 1.0):                          # las piernas, del suelo a la cadera (o al bajo)
        hx, hz = lado(sg * sep)
        a = math.radians(sg * th)
        L = abajo
        fx, fz = hx - L * math.sin(a) * sa, hz - L * math.sin(a) * ca
        cajas.append(_fila_pieza(fx, abajo - L * math.cos(a), fz, sg * th, ry, pw, L, pf, col))
    return dict(cajas=cajas, bolas=bolas, conos=conos)


def filas_arco(x, z, frac, col=AMBAR):
    """El arco de quietud: ARCO_SEGS cajas finas en el suelo, alrededor de los pies,
    desde el fondo de la sala y en el sentido de las agujas del reloj (visto desde
    arriba), las que cubre frac (0-1)."""
    n = int(round(max(0.0, min(1.0, frac)) * ARCO_SEGS))
    largo = 2.0 * math.pi * ARCO_R / ARCO_SEGS * 0.92
    out = []
    for j in range(n):
        f = 2.0 * math.pi * (j + 0.5) / ARCO_SEGS
        out.append([x + ARCO_R * math.sin(f), 0.004, z - ARCO_R * math.cos(f), 0.0, -math.degrees(f), 0.0,
                    largo, 0.01, ARCO_ANCHO] + list(col))
    return out


_PIEZAS = dict(clave=None, out=None)


def piezas_personas(c, eq, t, t_arco=None):
    """Las piezas de todo el publico en t: dict(cajas, bolas, conos, arcos), una vez por
    instante. Sin Monigotes, los troncos en cajas y nada mas."""
    clave = (t, c.get('monigotes', True), c.get('arco_quietud', False), tuple(c.get('col_monigote', COL_MONIGOTE)),
             n_personas(c), c.get('demo', 0), t_arco)
    if _PIEZAS['clave'] == clave:
        return _PIEZAS['out']
    out = dict(cajas=[], bolas=[], conos=[], arcos=[])
    ev = evitar_de(eq)
    col = tuple(c.get('col_monigote', COL_MONIGOTE))
    ta = t_arco if t_arco is not None else arco_segundos(c)
    for i in range(n_personas(c)):
        e = estado_persona(c, i, t, ev)
        if e is None:
            continue
        h = altura(i)
        if c.get('monigotes', True):
            pz = piezas_monigote(i, e['x'], e['z'], h, e['rumbo'], e['andado'], e['andando'], col)
            for k in ('cajas', 'bolas', 'conos'):
                out[k] += pz[k]
        else:
            cl = (0.10 + 0.22 * h01(i, 11), 0.10 + 0.22 * h01(i, 12), 0.10 + 0.22 * h01(i, 13))
            out['cajas'].append([e['x'], 0.0, e['z'], 0, 0, 0, TRONCO[0], h, TRONCO[1]] + list(cl))
        if ta and not e['andando'] and e['quieto'] > 0.0:
            out['arcos'] += filas_arco(e['x'], e['z'], e['quieto'] / ta)
    _PIEZAS.update(clave=clave, out=out)
    return out


def _puntos_pieza(np, f, forma, px=0.02):
    """Puntos de dentro de una pieza (fila de instancia) en el mundo, cada px/2 o menos:
    caja y cono con la base en ty, bola centrada; giro rx y luego ry (el orden xyz de
    las instancias)."""
    n = [max(3, int(math.ceil(2.0 * abs(f[6 + k]) / px))) for k in range(3)]
    u = (np.arange(n[0]) + 0.5) / n[0] - 0.5
    v = (np.arange(n[1]) + 0.5) / n[1]
    w = (np.arange(n[2]) + 0.5) / n[2] - 0.5
    U, V, Wz = [a.ravel() for a in np.meshgrid(u, v, w, indexing='ij')]
    if forma == 'bola':
        V = V - 0.5
        dentro = U * U + V * V + Wz * Wz <= 0.25
        U, V, Wz = U[dentro], V[dentro], Wz[dentro]
    elif forma == 'cono':               # el radio va de 0,5 abajo a VESTIDO[0] / VESTIDO[1] x 0,5 arriba
        r = 0.5 + (0.5 * VESTIDO[0] / VESTIDO[1] - 0.5) * V
        dentro = U * U + Wz * Wz <= r * r
        U, V, Wz = U[dentro], V[dentro], Wz[dentro]
    px, py, pz = U * f[6], V * f[7], Wz * f[8]
    a, b = math.radians(f[3]), math.radians(f[4])
    py, pz = py * math.cos(a) - pz * math.sin(a), py * math.sin(a) + pz * math.cos(a)
    px, pz = px * math.cos(b) + pz * math.sin(b), -px * math.sin(b) + pz * math.cos(b)
    return px + f[0], py + f[1], pz + f[2]


def alturas_planta(np, piezas, x0, z0, ancho, fondo, px=0.02):
    """La imagen de alturas (filas: z de z0 a z0 + fondo; columnas: x de x0 a x0 + ancho)
    de las piezas {cajas, bolas, conos}: lo que ve una camara cenital de profundidad."""
    w, h = int(round(ancho / px)), int(round(fondo / px))
    img = np.zeros(h * w)
    for k, forma in (('cajas', 'caja'), ('bolas', 'bola'), ('conos', 'cono')):
        for f in piezas.get(k, ()):
            X, Y, Z = _puntos_pieza(np, f, forma, px)
            c = ((X - x0) / px).astype(int)
            r = ((Z - z0) / px).astype(int)
            ok = (c >= 0) & (c < w) & (r >= 0) & (r < h)
            np.maximum.at(img, r[ok] * w + c[ok], Y[ok])
    return img.reshape(h, w)


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
    if nombre in ('i_personas_bolas', 'i_personas_conos', 'i_arcos'):     # v13: monigotes y arcos
        if not c['activa']:
            return []
        pz = piezas_personas(c, eq, t)
        return pz[{'i_personas_bolas': 'bolas', 'i_personas_conos': 'conos', 'i_arcos': 'arcos'}[nombre]]
    if nombre == 'i_haces':
        return _filas_haces(c, eq, t)
    return []


def frame_tick():
    """Cada fotograma (latido_sala): la demo GENoZilla (v13), el publico a FASE1
    (v15), y las personas y los aparatos se redibujan."""
    try:
        demo_tick()
    except Exception as e:
        if not _SALA.get('err_demo'):
            _SALA['err_demo'] = True
            print('SALA  FALLO en la demo: %s' % e)
    try:
        alimentar_tick()
    except Exception as e:
        if not _SALA.get('err_pub'):
            _SALA['err_pub'] = True
            print('SALA  FALLO al pasar el publico a FASE1: %s' % e)
    if not _p('Activa', True):
        return
    for nm in ('i_personas', 'i_personas_bolas', 'i_personas_conos', 'i_arcos', 'i_equipos', 'i_haces'):
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
    elif nombre == 'Siguientecap':              # v13: la demo GENoZilla salta al capitulo siguiente
        _GZ['saltar'] = True
        print('SALA  demo: al caso siguiente' if _GZ.get('activo') else
              'SALA  Siguientecap: no hay ninguna demo en marcha (Demo vacia o Activa apagada)')


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
    if _GZ.get('activo'):                       # v13: la demo (v18: cualquiera)
        lineas.append(legend_demo())
    if _pub_guardado() is not None:             # v15: el publico a FASE1
        try:
            m = op('/project1/FASE1').op('motor').module
            lineas.append('FASE1  ve al publico (Fuente simulada): %d personas en su suelo' % len(m.personas_en_sala()))
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
                % (c['ancho'], c['fondo'], len(ps), n_personas(c), est,
                   ' (estrobo %.1f Hz)' % hz_estrobo(c) if est == 'erosion' else '',
                   sum(1 for e in eq if e['tipo'] == 'foco'),
                   'si' if any(e['tipo'] == 'micro' for e in eq) else 'no'))
    except Exception as e:
        return 'SALA  fallo en la leyenda: %s' % e


# =============================================================================
# v13: LA DEMO GENOZILLA (Demo = genozilla)
# =============================================================================
# El publico virtual juega a GENoZilla capitulo a capitulo (la demo web «GENoZilla ·
# demo de sala»). El juego lo juega FASE1 de verdad (fases 32 a 39): la sala solo
# mueve a la gente, que FASE1 ve por su sala simulada (Fuente = simulada: la tabla
# sala_personas, la misma imagen de alturas que la camara), y con Guion le pide a su
# motor que prepare cada capitulo (guion_demo, motor v119).
#
# Cada capitulo trae su coreografia: tramos [t, persona, destino], t en segundos desde
# que acaba su titulo (negativo: donde esta al empezar el titulo, sin andar). Destinos:
#   (x, z)                          un punto de la sala, en metros
#   ('celda', c, dx, dz)            una celda del planeta (c, un numero o un sitio con
#                                   nombre del guion): el centro de la casilla que la
#                                   mira, mas (dx, dz) metros; se pasa a metros al
#                                   empezar el tramo (casilla_de_celda y el mapeo de la
#                                   fase 22, solo leyendo)
#   ('monstruo', db, dl, dx, dz)    la celda del monstruo desplazada db bandas y dl
#                                   meridianos (celda_desplazada del motor)
#   ('casilla', sitio, j, dx, dz)   la casilla j de un sitio del guion (una fila)
#   ('vecina_mon', j)               (v16) la vecina j del monstruo que no cierra el cerco
#                                   de cuatro (vecinas_cerco del motor)
#   ('pison', i)                    (v17) el sitio del visitante i (0-2) del pisoton en la
#                                   celda del monstruo, con las tres cabezas separadas
#                                   (sitio_pison)
#   ('suelo', columna, fila)        un punto del suelo en casillas de la demo web
#                                   (11 x 9; 0, 0 junto a la pantalla, a la izquierda)
#   'fuera'                         sale por la puerta
# Las personas andan a VELOCIDAD y se paran en el destino. Al acabar el capitulo, su
# columna Comprobar (comprobar_capitulo) dice si FASE1 hizo lo que cuenta el rotulo.

GZ_PERSONAS = 8
TITULO = 2.8                # s del titulo de cada capitulo
TITULO_ENTRA, TITULO_SALE = 0.35, 0.5
VELO = 0.8                  # el velo oscuro del titulo
SIGUE_MIN = 0.12            # m: un destino que se mueve menos no hace andar a nadie
FOV_JUEGO = 75.0            # la vista juego: la sala, en un cuadrado de 720 x 720
GZ_HUECO = 'antes_demo'     # la escena guardada de FASE1 (Guardarescena / Cargarescena)
GANANCIA_MAX = 8.0          # D4: el grito sube su volumen hasta x8 si no pasa Umbralcorte
GRITO_SUBE = 1.6            # cada segundo del grito sin corte, x1,6

ARMAS = ('Armacerco', 'Armapison', 'Armaestatuas', 'Armagrito', 'Armarelampago')
CAP_NOMBRES = ['genozilla', 'construir', 'aparece', 'brotes', 'rescate', 'cebo', 'canal', 'cerco', 'pisoton',
               'estatuas', 'grito', 'relampago', 'fin']

_FUERA = 'fuera'
UMBRAL_SILENCIO_SALA = 0.5  # el drone de la sala virtual (el sub a 41 Hz) da un flujo de hasta 0,35:
                            # en Estatuas, Umbralsilencio por encima (se fija en sala, encargo fase 37)


def _sigue(i, destino, t0, t1, cada=3.0):
    """Tramos que repiten el mismo destino cada 'cada' s (seguir a una celda que gira)."""
    out, t = [], t0
    while t < t1 - 1e-9:
        out.append([t, i, destino])
        t += cada
    return out


def _paseo(personas, t0, t1, cada=3.0, semilla=31):
    """Un paseo sin azar: cada 'cada' s, cada persona va (o no) a otro punto del suelo."""
    out = []
    for k in range(int((t1 - t0) / cada) + 1):
        for i in personas:
            if h01(i, k, semilla) < 0.6:
                out.append([t0 + k * cada, i, ('suelo', 0.5 + 9.5 * h01(i, k, semilla + 1),
                                               0.5 + 7.5 * h01(i, k, semilla + 2))])
    return out


def _sitios(lista, t=-1.0):
    return [[t, i, d] for i, d in enumerate(lista)]


CAPITULOS = [
    dict(nombre='GENoZilla', sub='Toda la sala, un solo equipo, contra un monstruo que devora lo construido.',
         dur=14.0, pars=dict(),          # v21: sin Barsperturn (el giro es el de FASE1)
         coreo=_sitios([('suelo', 2, 6), ('suelo', 5, 3), ('suelo', 8, 5), ('suelo', 3, 2), ('suelo', 9, 7)])
         + _paseo(range(5), 0.5, 13.0),
         rotulos=[(0.0, 'La camara cenital situa a cada persona en una celda del planeta: un anillo en la pantalla.'),
                  (5.0, 'El planeta gira con el tempo: aunque estes quieto, la celda bajo tus pies cambia.'),
                  (10.0, 'El objetivo: que al acabar la ronda haya mas territorio del publico que del mal.')]),
    dict(nombre='Construir quietos', sub='Moviendose, la presencia apenas cuenta. Quietos, se construye.',
         dur=20.0, pars=dict(),
         coreo=[[0.6 * k, i, ('suelo',) + d] for k, (i, d) in enumerate(
             [(0, (6, 1)), (1, (9, 1)), (2, (4, 3)), (3, (8, 3)), (4, (2, 5)), (5, (6, 5)), (6, (9, 6)), (7, (4, 7))])]
         + [[8.0, 6, ('suelo', 7, 5)], [8.0, 1, ('suelo', 1, 8)], [14.0, 1, ('suelo', 2, 7)]],
         rotulos=[(0.0, 'Entran caminando: en movimiento, la probabilidad de que prendan las notas sube poco.'),
                  (5.0, 'Se paran: cada nota que cae en su celda suma ocupacion.'),
                  (11.0, 'Al llenarse, la celda desborda a las vecinas, se funde con ellas y llega a corona.')]),
    dict(nombre='Aparece GENoZilla',
         sub='Va a por lo mas prospero, devora a x2 sin esperar a los secuenciadores y deja brotes del mal.',
         dur=24.0, pars=dict(),
         coreo=_sitios([('suelo', 9, 8), ('suelo', 1, 7), ('suelo', 10, 1)]),
         rotulos=[(0.0, 'Aparece con media celda de tamano cuando la cara visible tiene bastante construido.'),
                  (2.5, 'El tocon marca su objetivo: la celda con mas ocupacion, pesando la distancia.'),
                  (6.0, 'Devora a x2 por negra. Al vaciar la celda, deja un brote del mal y busca otra.'),
                  (14.0, 'Con una celda entera devorada crece a forma grande: mas rapido, x3, y entra el '
                         'estroboscopio.'),
                  (18.0, 'Ya grande, puede con coronas y fusiones.')]),
    dict(nombre='Brotes del mal', sub='Un brote crece con las mismas reglas que lo construido. Pararse encima lo '
                                      'alimenta.',
         dur=15.0, pars=dict(),
         coreo=_sitios([('suelo', 4, 8.5), ('suelo', 5, 8.5), ('suelo', 9, 2)])
         + [[0.0, 0, ('celda', 'brote', 0.0, 0.0, 0)], [0.0, 1, ('celda', 'brote', 0.0, 0.0, 1)]],
         rotulos=[(0.0, 'Dos visitantes se paran sobre un brote del mal.'),
                  (4.0, 'Su presencia sube la probabilidad de las notas en esa celda: el mal crece.'),
                  (9.0, 'Y desborda a las vecinas: el mal se extiende solo.')]),
    dict(nombre='Rescatar un brote', sub='Una persona encima y {aliados} aliados en las celdas vecinas durante '
                                         '{taliados} s.',
         dur=15.0, pars=dict(Tfila=60.0),
         coreo=_sitios([('suelo', 4, 8.5), ('suelo', 2, 8.5), ('suelo', 7, 8.5), ('suelo', 3, 8.5)])
         + [[0.0, 0, ('celda', 'brote', 0.0, 0.0)], [2.0, 1, ('celda', ('aliadas', 0), 0.0, 0.0)],
            [2.2, 2, ('celda', ('aliadas', 1), 0.0, 0.0)], [2.4, 3, ('celda', ('aliadas', 2), 0.0, 0.0)]],
         rotulos=[(0.0, 'Quien esta encima alimenta el mal mientras llegan los aliados.'),
                  (4.0, 'Con los cuatro en su sitio empieza la cuenta de {taliados} segundos.'),
                  (9.0, 'Rescatado: pasa a la especie del ultimo secuenciador y sigue creciendo al ritmo normal.')]),
    dict(nombre='Cebo y zanja trampa',
         sub='Una torre atrae al monstruo; una fila quieta {tfila} s cava una zanja en su camino.',
         dur=21.0, pars=dict(Zanjajuego=True, Rios=False), arco=True,
         coreo=_sitios([('suelo', 3, 7.5), ('suelo', 4, 7.5), ('suelo', 5, 7.5), ('suelo', 9, 7.5),
                        ('suelo', 10, 7.5)])
         + [[0.0, j, ('casilla', 'fila', j)] for j in range(3)]
         + [[0.0, 3, ('celda', 'torre', 0.0, 0.0, 0)], [0.0, 4, ('celda', 'torre', 0.0, 0.0, 1)],
            [15.0, 0, ('suelo', 2, 8.6)], [15.2, 1, ('suelo', 4.5, 8.6)], [15.4, 2, ('suelo', 7, 8.6)]],
         rotulos=[(0.0, 'Dos visitantes engordan una torre: es el cebo.'),
                  (3.0, 'Tres forman una fila y se quedan quietos: el arco ambar cuenta {tfila} segundos.'),
                  (8.0, 'La fila cava una zanja en todas sus celdas. El monstruo viene a por la torre.'),
                  (12.0, 'Cae en la zanja: vuelve a media celda y pierde lo devorado.'),
                  (15.5, 'La fila se mueve: la zanja queda fijada y no se puede volver a cavar hasta el ciclo '
                         'siguiente.')]),
    dict(nombre='Canal: el agua lo ahoga',
         sub='Una fila de 4 cava hasta el agua. Llena a x4 y desborda a x2 hacia la zanja vecina.',
         dur=21.0, pars=dict(Zanjajuego=True, Rios=False, Pasomonstruo=72, Esperamonstruo=3.0), arco=True,
         coreo=_sitios([('suelo', 3, 7.5), ('suelo', 4, 7.5), ('suelo', 5, 7.5), ('suelo', 6, 7.5)])
         + [[0.3, j, ('casilla', 'fila', j)] for j in range(4)]
         + [[13.0, 0, ('suelo', 2, 8.6)], [13.2, 1, ('suelo', 4, 7.8)], [13.4, 2, ('suelo', 7, 8.6)],
            [13.6, 3, ('suelo', 9, 6.5)]],
         rotulos=[(0.0, 'El monstruo avanza por una zanja de 2 conchas: cada paso le cuesta el doble.'),
                  (2.5, 'Cuatro se ponen en fila junto a ella.'),
                  (6.5, 'Su zanja llega a 4 conchas: aflora agua, llena a x4 y se desborda a x2.'),
                  (8.0, 'El agua alcanza al monstruo: muere ahogado.'),
                  (14.0, 'Al poco aparece otro.')]),
    dict(nombre='Cerco', sub='Las celdas con alguien quieto son muro. Sin nada a su alcance, no come y pierde lo '
                             'devorado.',
         dur=21.5, pars=dict(Armacerco=True, Tfila=60.0),      # v14: 2,5 s mas (el monstruo, mas lento)
         coreo=[[-1.0, j, ('monstruo', db, dl)] for j, (db, dl) in enumerate(((0, -1), (0, 1), (1, 0), (-1, 0)))]
         + [[-1.0, 4, ('vecina_mon', 0)], [-1.0, 5, ('vecina_mon', 1)]]      # v16: las otras dos vecinas
         + _sigue(0, ('monstruo', 0, -1), 0.0, 14.5) + _sigue(1, ('monstruo', 0, 1), 0.0, 14.5)
         + _sigue(2, ('monstruo', 1, 0), 0.0, 14.5) + _sigue(3, ('monstruo', -1, 0), 0.0, 14.0)
         + _sigue(4, ('vecina_mon', 0), 0.0, 14.5) + _sigue(5, ('vecina_mon', 1), 0.0, 14.5)
         + [[14.5, 3, ('suelo', 10, 8)]],
         rotulos=[(0.0, 'Seis visitantes rodean al monstruo grande mientras aparece.'),
                  (4.6, 'Acorralado: no alcanza nada que comer y pierde un escalon por compas.'),
                  (9.0, 'El giro mueve las celdas: para mantener el cerco hay que caminar con ellas.'),
                  (15.0, 'Si alguien se va, el cerco se abre y se escapa.')]),
    dict(nombre='Pisoton', sub='Tres personas sobre la celda del monstruo: deja de comer y encoge.',
         dur=16.0, pars=dict(Armapison=True, Tfila=60.0),
         coreo=_sitios([('suelo', 5, 6.2), ('suelo', 7, 6.2), ('suelo', 6, 7.0), ('suelo', 1, 6)])
         # v17: los tres, con las cabezas bien separadas (sitio_pison). Antes, dos en la misma
         # casilla a 0,37 m y el tercero en la de al lado a 0,38: junto a Separacioncabezas
         # (0,35) y en TouchDesigner dos cabezas se fundian en una: el pisoton no llegaba a tres
         + [[t_, i, ('pison', i)] for t_ in (0.2, 6.0) for i in range(3)],
         rotulos=[(0.0, 'El monstruo grande devora una corona.'),
                  (2.0, 'Tres visitantes se le echan encima.'),
                  (4.0, 'Con tres en su celda no come y encoge a cada paso.'),
                  (11.0, 'Ha vuelto a la forma pequena: ya no puede con coronas ni fusiones.')]),
    dict(nombre='Estatuas', sub='Toda la sala quieta y en silencio {tquietud} s: el monstruo queda petrificado.',
         dur=17.0, pars=dict(Armaestatuas=True, Tfila=60.0, Umbralsilencio=('min', UMBRAL_SILENCIO_SALA)),
         arco='estatuas',
         ruido=[(0.0, 3.0, 'habla'), (3.0, 17.0, 'silencio')],
         coreo=_sitios([('suelo', 2, 2), ('suelo', 4, 6), ('suelo', 6, 3), ('suelo', 8, 7), ('suelo', 9, 2),
                        ('suelo', 1, 5)])
         + [[0.0, i, ('suelo',) + d] for i, d in enumerate(((3, 3), (5, 7), (7, 2), (9, 6), (8, 1), (2, 6)))]
         + [[1.6, 0, ('suelo', 2, 2.5)], [1.6, 2, ('suelo', 6, 2.5)], [1.6, 4, ('suelo', 9, 1.5)]],
         rotulos=[(0.0, 'La sala camina y habla: el microfono lo oye.'),
                  (3.0, 'Todos se quedan quietos y en silencio.'),
                  (7.0, 'Petrificado durante {tpiedra} segundos: ni se mueve ni come.'),
                  (13.0, 'Se rompe la piedra. El ruido de la sala, al reves, lo acelera.')]),
    dict(nombre='Grito', sub='Un grito colectivo abre un pozo bajo el monstruo.',
         dur=15.0, pars=dict(Armagrito=True, Rios=False, Tfila=60.0), ruido=[(2.0, 6.5, 'grito')],
         coreo=_sitios([('celda', 'corro', 0.0, 0.0), ('celda', 'corro', -0.4, 0.0), ('celda', 'corro', 0.4, 0.0),
                        ('celda', 'corro', 0.0, -0.4), ('celda', 'corro', 0.0, 0.4)]),
         rotulos=[(0.0, 'El monstruo grande devora una corona.'),
                  (2.0, 'Toda la sala grita a la vez.'),
                  (5.0, 'El ruido de la sala pasa el umbral: se abre un pozo en su celda y cae.'),
                  (9.0, 'El grito tarda {recarga} segundos en recargarse.')]),
    dict(nombre='Relampago', sub='Una fila que cava a una celda o menos del monstruo lo deja aturdido.',
         dur=15.0, pars=dict(Armarelampago=True, Zanjajuego=True, Rios=False, Pasomonstruo=120), arco=True,
         coreo=_sitios([('suelo', 6, 6.6), ('suelo', 7, 6.6), ('suelo', 8, 6.6), ('suelo', 1, 7)])
         + [[0.0, j, ('casilla', 'fila', j)] for j in range(3)],
         rotulos=[(0.0, 'Tres visitantes se plantan en fila junto al monstruo.'),
                  (3.0, 'Quietos {tfila} segundos.'),
                  (7.0, 'La zanja se abre a su lado: relampago, y queda aturdido {taturdido} segundos.')]),
    dict(nombre='Fin de ronda', sub='Al acabar la ronda se cuentan todas las celdas del globo, tambien las de la cara '
                                    'oculta.',
         dur=17.0, pars=dict(Noche=('min', 4.0), Tfila=60.0),      # v21: sin Barsperturn
         coreo=_sitios([('suelo', 2, 4), ('suelo', 4, 6), ('suelo', 6, 3), ('suelo', 8, 5), ('suelo', 9, 7)]),
         rotulos=[(0.0, 'Recuento: publico contra mal, en todo el planeta.'),
                  (3.5, '{gana}'),
                  (9.0, 'El mundo se entierra: la concha guarda el mapa de la partida.')]),
]
CAP_ETIQUETAS = ['%d %s' % (k, cp['nombre']) for k, cp in enumerate(CAPITULOS)]


# =============================================================================
# v18: LAS DEMOS DE LA SALA, POR SECCIONES Y CASOS
# =============================================================================
# Cada demo es una SECCION con su numero y su titulo, hecha de CASOS (capitulos)
# que juega el mismo director que GENoZilla: un titulo al empezar cada caso (la
# seccion, el caso y de que va), un rotulo abajo que explica lo que pasa y una
# cabecera arriba a la derecha (cabecera_texto) con la seccion, el caso y, donde
# cuenta, lo que mide FASE1 en vivo. Las personas las mueve la coreografia del caso.
# Con Siguecamara (v19: apagado por defecto), la camara de FASE1 sigue a las celdas donde
# pasan las cosas (foco del caso; motor v140, foco_camara), sin cambiar de altura. Las
# demos no tocan el giro de FASE1 (v19; v21, tampoco GENoZilla). Al entrar se guarda la escena,
# los parametros y la tabla de FASE1 y al salir se devuelven; el mundo no (v21): la demo lo toma
# donde esta y lo deja como quede. Si le falta algo, el caso espera (falta_caso).
#   1 paseo         la gente entra, pasea y sale, a veces en grupo; algo de la obra
#                   la detiene y, quieta, construye
#   2 probabilidad  estrato humano: la probabilidad de que prenda lo que llega, en
#                   tres casos: minima (nadie quieto), una persona quieta, un grupo
#   3 huella        la huella inevitable: quietos construyen y dejan inclusiones; la
#                   fila cava tantas conchas como personas
#   4 llena         la sala se va llenando y la gente cambia de sitio; una sola fila
#                   recta, a proposito (v20)
#   5 genozilla     GENoZilla, como estaba (13 capitulos)
#   vacia           nadie (sin director)
# Destinos de las coreografias: los de GENoZilla (ver arriba). Claves nuevas de un caso:
#   foco     a donde mira la camara: 'quietos' (las celdas de la gente quieta; si no
#            hay, de la que haya), 'monstruo' (GENoZilla), ('refs', nombre) (celdas del
#            caso)
#   musica   las celdas de la gente quieta suenan (notas del SEQ1, por el sorteo)
#   lluvia   ('testigo', 'control'): una nota cada LLUVIA_CADA s en cada una, contando
#            cuantas prenden (la probabilidad, medida)
#   mundo    'base': el caso empieza en el mundo con el que entro la demo (si no, sigue
#            el que hay); despejar y conchas en sus refs (_refs_caso)

LLENA_MIN, LLENA_MAX = 10, 30    # personas de la sala llena (Personas, entre las dos)
MUSICA_CADA = 0.5               # s entre dos notas por persona quieta (paseo, huella, llena)
MUSICA_QUIETO = 1.0             # s quieta en su casilla antes de que su celda suene
LLUVIA_CADA = 0.35              # s entre dos notas en la celda testigo (y en la de control)
P_DESDE = 8.0                   # s del caso desde los que se mide la probabilidad media (ya asentada)


def _vaga(i, t0, t1, cada=5.0, semilla=41, zona_=(0.8, 10.2, 1.2, 7.8)):
    """Persona i paseando de t0 a t1: cada 'cada' s (mas o menos) a otro punto del suelo
    (columnas y filas de la demo web), sin azar."""
    out, t, k = [], t0, 0
    x0, x1, y0, y1 = zona_
    while t < t1 - 1e-9:
        out.append([t, i, ('suelo', x0 + (x1 - x0) * h01(i, k, semilla), y0 + (y1 - y0) * h01(i, k, semilla + 1))])
        t += cada * (0.75 + 0.5 * h01(i, k, semilla + 2))
        k += 1
    return out


def _coreo_paseo(n, c=None):
    """Paseo (80 s): sueltos que entran y salen, una que se interesa por la obra y un
    grupo de cuatro que entra, se para y sale junto."""
    co = []
    co += [[0.0, 0, ('suelo', 5, 7)]] + _vaga(0, 2.0, 24.0, semilla=11) + [[24.0, 0, _FUERA]]
    co += [[50.0, 0, ('suelo', 7, 6)]] + _vaga(0, 53.0, 66.0, semilla=12) + [[66.0, 0, _FUERA]]
    # la interesada: pasea, se acerca a la esfera (la obra) y se queda mirando
    co += [[3.0, 1, ('suelo', 6, 6)]] + _vaga(1, 5.0, 15.0, semilla=13)
    co += [[15.0, 1, ('suelo', 2.2, 2.6)], [34.0, 1, ('suelo', 5, 4)]] + _vaga(1, 37.0, 44.0, semilla=14) \
        + [[44.0, 1, _FUERA]]
    co += [[7.0, 2, ('suelo', 8, 6)]] + _vaga(2, 9.0, 40.0, semilla=15) + [[40.0, 2, _FUERA]]
    co += [[58.0, 2, ('suelo', 4, 7)]] + _vaga(2, 61.0, 70.0, semilla=16) + [[70.0, 2, _FUERA]]
    co += [[11.0, 3, ('suelo', 9, 4)]] + _vaga(3, 13.0, 30.0, semilla=17) + [[30.0, 3, _FUERA]]
    co += [[44.0, 3, ('suelo', 3, 5)]] + _vaga(3, 47.0, 64.0, semilla=18) + [[64.0, 3, _FUERA]]
    # el grupo: entra en fila india, se para un momento junto y va junto a la obra
    corro_a = ((5.5, 6.5), (6.8, 6.6), (5.9, 7.7), (7.2, 7.7))
    corro_b = ((3.2, 3.4), (4.6, 3.2), (3.4, 4.6), (4.8, 4.5))
    for j in range(4):
        i = 4 + j
        if i >= n:
            break
        co += [[30.0 + 0.7 * j, i, ('suelo',) + corro_a[j]], [39.0 + 0.3 * j, i, ('suelo',) + corro_b[j]],
               [53.0 + 0.5 * j, i, _FUERA]]
    return co


# v20: la sala llena se va llenando y evoluciona sin abrir pozos por todas partes. Hasta
# la v19 entraban 0,7 s uno tras otro a una rejilla de 6 columnas (a casilla y media) y
# daban pasos de +-1 casilla: los quietos quedaban en casillas contiguas, y con Modofila =
# cadena cada corrillo de tres aguantando Tfila era una escision. Ahora la seccion fija
# Modofila = recta (Minfila 3, Tfila 5) y cada persona quieta ocupa una casilla de la
# rejilla par (columna y fila pares de la demo web, 11 x 9): dos quietos nunca son
# vecinos, asi que no forman fila. Solo una vez, a proposito, tres se ponen en linea recta
# (LLENA_LINEA): los de las casillas (4, 4) y (6, 4) y un tercero en medio.
LLENA_DUR = 120.0               # s del caso
LLENA_LLENA = 55.0              # s: para entonces han entrado todos (de uno en uno)
LLENA_CAMBIOS = 98.0            # s: hasta aqui cambian de sitio, se van y vuelven
LLENA_VACIA = 100.0             # s: empiezan a irse todos
LLENA_LINEA = ((4, 4), (5, 4), (6, 4), 62.0, 76.0)    # la fila recta: extremos, medio, de t0 a t1


def sitios_llena(c=None):
    """Las casillas de la rejilla par (columna y fila pares de la demo web) donde puede
    pararse alguien en la sala llena: en el suelo de la camara, lejos de la esfera y del
    estrobo y sin quedar detras (como casillas_libres). Sin sala, todas."""
    todos = [(cx, cy) for cy in range(0, REJILLA_WEB[1], 2) for cx in range(0, REJILLA_WEB[0], 2)]
    if c is None:
        return todos
    try:
        ev = evitar_de(equipos_o_defecto(c))
        F = fase1()
        c1 = F.cfg() if F is not None else dict(ancho_sala=5.4, fondo_sala=4.5)
        w, f = REJILLA_WEB
        out = []
        for cx, cy in todos:
            x, z = de_suelo(c1, (cx + 0.5) / w * c1['ancho_sala'], (cy + 0.5) / f * c1['fondo_sala'])
            q = _libre(c, (x, z), ev)
            if math.hypot(q[0] - x, q[1] - z) < 0.05:
                out.append((cx, cy))
        return out or todos
    except Exception:
        return todos


def _coreo_llena(n, c=None):
    """Sala llena (LLENA_DUR s): entran de uno en uno hasta LLENA_LLENA y cada uno se para
    en una casilla libre de la rejilla par (nunca junto a otro quieto); luego, cada poco,
    unos cambian de sitio y otros se van y vuelven; una sola vez, tres en linea recta
    (LLENA_LINEA) abren un pozo; al final se vacia. Sin azar: h01 decide cada paso."""
    (ax, ay), medio, (bx, by), t_l0, t_l1 = LLENA_LINEA
    extremos = [(ax, ay), (bx, by)]
    sitios = [s_ for s_ in sitios_llena(c) if s_ not in extremos]
    co = []
    ocupa = {}                  # sitio: persona
    sitio_de = {}               # persona: sitio (None, fuera)

    def elige(i, v):
        libres = [s_ for s_ in sitios if s_ not in ocupa]
        if not libres:
            return None
        return max(libres, key=lambda s_: h01(i, v, s_[0], s_[1], 71))

    def ir(t, i, s_):
        viejo = sitio_de.get(i)
        if viejo is not None and ocupa.get(viejo) == i:
            del ocupa[viejo]
        sitio_de[i] = s_
        if s_ is None:
            co.append([t, i, _FUERA])
        else:
            ocupa[s_] = i
            co.append([t, i, ('suelo',) + tuple(s_)])

    # cola de decisiones: (t, persona, que, vuelta, generacion); una decision de una
    # generacion vieja (la persona ya cambio de plan) no cuenta
    gen = dict((i, 0) for i in range(n))
    cola = []
    paso = (LLENA_LLENA - 5.0) / max(1, n)
    for i in range(n):
        cola.append((1.0 + paso * i + 0.4 * paso * h01(i, 72), i, 'entra', 0, 0))
    if n >= 3:
        cola.append((t_l0, 2, 'medio', 0, 0))           # el tercero se pone entre los dos
    while cola:
        cola.sort()
        t, i, que, v, g = cola.pop(0)
        if t >= LLENA_CAMBIOS or (g != gen[i] and que != 'medio'):
            continue
        if n >= 3 and i == 2 and que != 'medio' and t_l0 - 10.0 <= t < t_l0:
            continue                                    # quieto (o fuera) hasta la fila: se mueve a t_l0
        if i < 2 and n >= 3 and que == 'entra':         # los extremos de la fila: su casilla, quietos
            ir(t, i, extremos[i])
            cola.append((t_l1 + 4.0 + 6.0 * h01(i, 73), i, 'cambia', v + 1, gen[i]))
            continue
        if que == 'medio':                              # la fila recta, de t_l0 a t_l1
            gen[i] += 1
            viejo = sitio_de.get(i)
            if viejo is not None and ocupa.get(viejo) == i:
                del ocupa[viejo]
            sitio_de[i] = None
            co.append([t, i, ('suelo',) + tuple(medio)])
            cola.append((t_l1, i, 'cambia', v + 1, gen[i]))
            continue
        if que in ('entra', 'vuelve'):
            s_ = elige(i, v)
            if s_ is None:                              # no cabe: espera fuera a que se libere un sitio
                cola.append((t + 2.0, i, que, v + 1, g))
                continue
            ir(t, i, s_)
            espera = max(0.0, LLENA_LLENA - t) + 14.0 + 16.0 * h01(i, v, 74)
            cola.append((t + espera, i, 'cambia', v + 1, g))
            continue
        # cambia: a otro sitio libre (mas a menudo) o se va y vuelve (tambien si no hay sitio)
        s_ = elige(i, v) if h01(i, v, 75) < 0.6 else None
        if s_ is not None:
            ir(t, i, s_)
            cola.append((t + 12.0 + 12.0 * h01(i, v, 76), i, 'cambia', v + 1, g))
        else:
            ir(t, i, None)
            cola.append((t + 8.0 + 8.0 * h01(i, v, 77), i, 'vuelve', v + 1, g))
    for i in range(n):
        co.append([LLENA_VACIA + 0.3 * i, i, _FUERA])
    co.sort(key=lambda x: (x[0], x[1]))
    return co


CASOS_PASEO = [
    dict(nombre='Paseo', sub='La gente entra, pasea y sale, a veces en grupo. Algo de la obra la detiene.',
         dur=80.0, pars=dict(), musica=True, foco='quietos', coreo=_coreo_paseo,
         rotulos=[(0.0, 'Entran de uno en uno y pasean. Andando, su presencia apenas inclina el mundo.'),
                  (15.0, 'Algo de la obra la detiene: se acerca a la esfera y se queda mirando.'),
                  (21.0, 'Quieta, lo que llega a su celda prende: el mundo empieza a construirse donde esta.'),
                  (30.0, 'Entra un grupo: caminan juntos y se paran juntos.'),
                  (40.0, 'El grupo se acerca a la obra: cuatro quietos, cuatro celdas que construyen.'),
                  (53.0, 'El grupo se va junto; otros siguen entrando y saliendo.'),
                  (70.0, 'La sala se vacia: lo que dejaron queda en el mundo.')]),
]

CASOS_PROBABILIDAD = [
    dict(nombre='Probabilidad minima', sub='Sin nadie quieto, cada celda tiene la misma probabilidad: Cuanto.',
         dur=18.0, pars=dict(), lluvia=('testigo', 'control'), foco=('refs', 'testigo'),
         coreo=[[6.0, 0, ('suelo', 2, 7)], [6.8, 1, ('suelo', 9, 6)]]
         + _vaga(0, 8.0, 16.0, cada=2.2, semilla=21) + _vaga(1, 8.5, 16.0, cada=2.2, semilla=22)
         + [[16.0, 0, _FUERA], [16.3, 1, _FUERA]],
         rotulos=[(0.0, 'Sala vacia: todo lo que llega prende con la probabilidad minima, Cuanto = {cuanto}.'),
                  (6.0, 'Dos personas cruzan andando: su densidad sube despacio y se va con ellas.'),
                  (11.0, 'La celda testigo y la vacia prenden lo mismo: nadie cambia el devenir del mundo.')]),
    dict(nombre='Una persona quieta', sub='P = Cuanto + (1 - Cuanto) x densidad: quieta, su densidad sube.',
         dur=20.0, pars=dict(), lluvia=('testigo', 'control'), foco=('refs', 'testigo'),
         coreo=[[0.0, 0, ('celda', 'testigo', 0.0, 0.0)]] + _sigue(0, ('celda', 'testigo', 0.0, 0.0), 3.0, 20.0),
         rotulos=[(0.0, 'Una persona entra y se para sobre la celda testigo.'),
                  (4.0, 'Quieta, la densidad de su casilla sube (Subida) y con ella la probabilidad de su celda.'),
                  (10.0, 'En su celda prende mas que en la vacia: el mundo se inclina hacia donde esta.')]),
    dict(nombre='Un grupo', sub='Varios juntos sobre la misma celda llenan su casilla: casi todo prende.',
         dur=22.0, pars=dict(), lluvia=('testigo', 'control'), foco=('refs', 'testigo'),
         coreo=[[-1.0, 0, ('celda', 'testigo', 0.0, 0.0)]]
         + [[0.6 * j, 1 + j, ('celda', 'testigo', dx, dz)]
            for j, (dx, dz) in enumerate(((0.4, 0.0), (-0.4, 0.0), (0.0, 0.4), (0.0, -0.4)))]
         + [x for j, (dx, dz) in enumerate(((0.0, 0.0), (0.4, 0.0), (-0.4, 0.0), (0.0, 0.4), (0.0, -0.4)))
            for x in _sigue(j, ('celda', 'testigo', dx, dz), 4.0, 22.0)],
         rotulos=[(0.0, 'Llegan cuatro mas y se juntan con ella sobre la misma celda.'),
                  (5.0, 'Juntos llenan su casilla: la densidad llega a 1 y la probabilidad, casi a 1.'),
                  (12.0, 'La celda crece, se corona y desborda a sus vecinas: entre varios cambian el devenir del '
                         'mundo.')]),
]

CASOS_HUELLA = [
    dict(nombre='Quietos, construyen', sub='Nadie pasa sin dejar algo: al llegar, al pararse y al construir.',
         dur=24.0, pars=dict(), musica=True, foco='quietos',
         coreo=[[1.2 * j, j, ('suelo',) + d] for j, d in enumerate(((2.5, 3.0), (8.0, 2.0), (3.0, 6.5), (8.5, 6.0)))]
         + [[18.0 + 0.4 * j, j, _FUERA] for j in range(4)],
         rotulos=[(0.0, 'Al entrar, cada persona deja una inclusion con probabilidad {probllegada}.'),
                  (5.0, 'Quietos {tparada} s, una inclusion segura en su celda: guarda el escalon de la celda.'),
                  (9.0, 'Y quietos, sus celdas suenan: lo que llega prende y construye encima de su huella.'),
                  (18.0, 'Se van: la huella se queda en el mundo y, al enterrarlo, en su concha.')]),
    dict(nombre='La fila cava', sub='Una fila quieta {tfila} s abre un pozo de tantas conchas como personas.',
         dur=26.0, pars=dict(Minfila=3, Conchasporpersona=1, Tfila=5.0), arco=True, foco=('refs', 'fila_celdas'),
         coreo=[[0.4 * j, j, ('casilla', 'fila', 1 + j)] for j in range(3)]
         + [[11.0, 3, ('casilla', 'fila', 0)], [11.3, 4, ('casilla', 'fila', 4)]]
         + [[21.0 + 0.3 * j, j, _FUERA] for j in range(5)],
         rotulos=[(0.0, 'Tres se ponen en fila y se quedan quietos: el arco ambar cuenta {tfila} segundos.'),
                  (8.5, 'La fila abre una escision: un pozo de tantas conchas como personas.'),
                  (12.0, 'Se suman dos: la misma escision baja hasta cinco conchas.'),
                  (21.0, 'La fila se deshace: el pozo queda abierto, con su fulgurita, para siempre.')]),
]

CASOS_LLENA = [
    dict(nombre='Sala llena', sub='La sala se va llenando y la gente cambia de sitio: el mundo crece donde esta.',
         dur=LLENA_DUR, pars=dict(), musica=True, foco='quietos', coreo=_coreo_llena,
         rotulos=[(0.0, 'La sala se va llenando: entran de uno en uno y cada uno se para en su sitio.'),
                  (14.0, 'Quietos, sus celdas suenan: lo que llega prende y el mundo crece donde esta la gente.'),
                  (32.0, 'Cada llegada y cada parada deja su inclusion.'),
                  (LLENA_LLENA, 'Llena: unos cambian de sitio, otros se van y vuelven; el mundo sigue a la gente.'),
                  (LLENA_LINEA[3], 'Tres en linea recta, quietos {tfila} s: abren un pozo de tantas conchas como '
                                   'personas.'),
                  (LLENA_LINEA[4], 'La fila se deshace: el pozo queda abierto, con su fulgurita.'),
                  (LLENA_VACIA, 'La sala se vacia: lo que dejaron queda en el mundo.')]),
]

SECCIONES = dict(
    paseo=dict(num=1, titulo='Paseo', personas=8, pars=dict(Tfila=60.0), casos=CASOS_PASEO),
    probabilidad=dict(num=2, titulo='Estrato humano', personas=6,
                      pars=dict(Activo=True, Cuanto=0.2, Pesocrear=1.0, Tfila=60.0), casos=CASOS_PROBABILIDAD),
    huella=dict(num=3, titulo='La huella inevitable', personas=8, pars=dict(Tfila=60.0), casos=CASOS_HUELLA),
    llena=dict(num=4, titulo='Sala llena', personas='personas',
               pars=dict(Modofila='recta', Minfila=3, Tfila=5.0), casos=CASOS_LLENA),     # v20
    genozilla=dict(num=5, titulo='GENoZilla', personas=GZ_PERSONAS, pars=dict(), casos=CAPITULOS),
)
DEMOS = ['paseo', 'probabilidad', 'huella', 'llena', 'genozilla', 'vacia']
DEMOS_ETIQUETAS = ['1 Paseo: entran y salen, a veces en grupo; algo de la obra los detiene',
                   '2 Estrato humano: la probabilidad (minima, una persona quieta, un grupo)',
                   '3 La huella inevitable: quietos construyen; la fila cava tantas conchas como personas',
                   '4 Sala llena: mucha gente entrando y saliendo',
                   '5 GENoZilla: el publico juega capitulo a capitulo',
                   'Vacia: nadie']
# lo que cada demo pone en FASE1 mientras dura (y devuelve al salir): GENoZilla juega;
# las demas no (el monstruo se comeria lo que construye el publico)
PARS_DEMO = dict(Fuente='simulada', Modojuego=True)
PARS_SECCION = dict(Fuente='simulada', Modojuego=False)
PARS_CAPITULO = sorted(set(k for sec in SECCIONES.values() for cp in sec['casos'] for k in cp['pars'])
                       | set(k for sec in SECCIONES.values() for k in sec['pars']) | set(ARMAS)
                       | {'Umbralaparicion'})       # v21: Barsperturn, nunca (el giro es el de FASE1)


def pars_demo(demo):
    return PARS_DEMO if demo == 'genozilla' else PARS_SECCION


def demo_activa():
    """La demo que juega el director ahora (o la elegida, si no juega ninguna)."""
    return _GZ.get('demo') or str(_p('Demo', 'paseo'))


def casos(demo=None):
    """Los casos (capitulos) de una demo: los de la que juega, si no se dice."""
    sec = SECCIONES.get(demo or demo_activa())
    return sec['casos'] if sec else CAPITULOS


def coreo_de(cp, c):
    co = cp['coreo']
    return co(n_personas(c), c) if callable(co) else co


def antetitulo(k, demo=None):
    demo = demo or demo_activa()
    if demo == 'genozilla':
        if k == 0:
            return 'STRATOS · JUEGOS DE SALA'
        if k >= len(CAPITULOS) - 1:
            return 'STRATOS · FIN DE RONDA'
        return 'FORMA DE JUGAR %d / %d' % (k, len(CAPITULOS) - 2)
    sec = SECCIONES[demo]
    n = len(sec['casos'])
    if n == 1:
        return 'STRATOS · %d · %s' % (sec['num'], sec['titulo'].upper())
    return 'STRATOS · %d · %s · CASO %d / %d' % (sec['num'], sec['titulo'].upper(), k + 1, n)


_GZ = dict(activo=False, acabada=False, cap=None, t_titulo=None, t0=None, hechas=set(), refs={}, tramos={},
           ruido=[], ganancia=1.0, cortes0=None, t_gan=None, reg={}, saltar=False, cap_par=None,
           antes_cap={}, resultados=[], libres=None, rotulo=None, rotulo_frame=None, ultima_tabla=None,
           demo=None, sec={}, coreo=[], t_nota=None, sueltas=[], t_lluvia=None, cabecera=None, cab_frame=None,
           espera=None)


def ruido_demo(t):
    """El modo del ruido del publico en t (s de la sala): None (fuera de la demo: las
    palmadas y toses de Ruidopublico), 'habla', 'silencio' o 'grito'. En la demo, fuera de
    sus tramos, el publico calla: sus palmadas sueltas serian onsets que erosionan (fase 21)
    justo donde juega."""
    for t0, t1, modo in _GZ.get('ruido', ()):
        if t0 <= t < t1:
            return modo
    return 'silencio' if _GZ.get('activo') else None


# --- las personas de la demo: tramos que pone la coreografia --------------------

def _fuera_de(cfg):
    return (0.0, 0.5 * cfg['fondo'] + 1.0)


def tramos_demo(cfg, i, hasta):
    """Los tramos de la persona i en la demo (los pone la coreografia); fuera de la
    sala mientras no tenga ninguno. El ultimo se alarga hasta 'hasta'."""
    tr = _GZ['tramos'].get(i)
    if not tr:
        f = _fuera_de(cfg)
        tr = _GZ['tramos'][i] = [[0.0, hasta + 3600.0, f, f, False, False]]
    if tr[-1][1] <= hasta:
        tr[-1][1] = hasta + 3600.0
    return tr


def _corta(tr, t):
    """Corta los tramos en t: el que esta en curso acaba ahi (donde este); los de despues, fuera.
    Devuelve (posicion en t, dentro)."""
    while len(tr) > 1 and tr[-1][0] >= t:
        tr.pop()
    s = tr[-1]
    u = 0.0 if s[1] <= s[0] else max(0.0, min(1.0, (t - s[0]) / (s[1] - s[0])))
    p = (s[2][0] + (s[3][0] - s[2][0]) * u, s[2][1] + (s[3][1] - s[2][1]) * u)
    s[1], s[3] = max(s[0], t), p
    return p, s[4]


def mover(cfg, i, q, t, evitar=(), salto=False):
    """La persona i va a q ((x, z) en metros o 'fuera') desde t: anda a VELOCIDAD por
    el camino (rodeando la esfera y el estrobo) y se para alli. Con salto, esta alli
    ya (al empezar el titulo). Devuelve si se mueve."""
    tr = tramos_demo(cfg, i, t)
    p, dentro = _corta(tr, t)
    hz = 0.5 * cfg['fondo']
    puerta = (0.0, hz - 0.3)
    fuera = _fuera_de(cfg)
    largo = 3600.0
    if salto:
        if q == _FUERA:
            tr.append([t, t + largo, fuera, fuera, False, False])
        else:
            tr.append([t, t + largo, q, q, True, False])
        return True
    if q == _FUERA:
        if not dentro:
            tr.append([t, t + largo, fuera, fuera, False, False])
            return False
        t = _andar(tr, t, p, puerta, cfg, evitar)
        tr.append([t, t + 1.0, puerta, (0.0, hz), True, True])
        tr.append([t + 1.0, t + 1.0 + largo, fuera, fuera, False, False])
        return True
    if dentro and math.hypot(q[0] - p[0], q[1] - p[1]) < SIGUE_MIN:
        tr.append([t, t + largo, p, p, True, False])
        return False
    if not dentro:                      # entra por la puerta
        tr.append([t, t + 1.0, (0.0, hz), puerta, True, True])
        t, p = t + 1.0, puerta
    t = _andar(tr, t, p, q, cfg, evitar)
    tr.append([t, t + largo, q, q, True, False])
    del tr[:-120]
    return True


# --- de la sala al planeta: el mapeo de la fase 22, solo leyendo -----------------

def a_suelo(c1, x, z):
    """(x, y) en metros del suelo que cubre la camara de FASE1 (x desde la izquierda,
    y desde la pantalla) del punto (x, z) de la sala: el suelo cubierto, centrado."""
    return x + 0.5 * c1['ancho_sala'], z + 0.5 * c1['fondo_sala']


def de_suelo(c1, x, y):
    return x - 0.5 * c1['ancho_sala'], y - 0.5 * c1['fondo_sala']


def casillas_libres(c, c1, m, evitar=()):
    """Las casillas de FASE1 a las que llega el publico: su centro esta en el suelo
    de la sala, lejos de las paredes, de la esfera y del estrobo, y sin quedar detras."""
    cols, filas = m.rejilla_sala(c1)
    out = set()
    for k in range(cols * filas):
        x, z = de_suelo(c1, *m.casilla_xy(c1, k))
        q = _libre(c, (x, z), evitar)
        if math.hypot(q[0] - x, q[1] - z) < 0.05:
            out.add(k)
    return out


def _ref(refs, r):
    if isinstance(r, (tuple, list)):
        v = refs.get(r[0])
        try:
            return v[int(r[1])] if v is not None else None
        except Exception:
            return None
    if isinstance(r, str):
        return refs.get(r)
    return r


OTRA_EN_CASILLA = 0.13      # m (en diagonal) de dos personas en la misma casilla: 0,37 m entre las dos


def punto_de_celda(m, W, c1, celda, libres=None, j=0):
    """(x, z) de la sala del centro de la casilla j que mira a la celda (las libres, de la
    mas cercana a su centro); con mas personas que casillas, dos por casilla, en diagonal.
    Si ninguna la mira, el borde del suelo cubierto mas cercano."""
    if celda is None:
        return None
    ks = m.casillas_de_celda(W, c1, celda, libres) or m.casillas_de_celda(W, c1, celda)
    if ks:
        x, z = de_suelo(c1, *m.casilla_xy(c1, ks[int(j) % len(ks)]))
        if int(j) >= len(ks):
            d = OTRA_EN_CASILLA if (int(j) // len(ks)) % 2 else -OTRA_EN_CASILLA
            x, z = x + d, z + d
        return x, z
    lat, lon = m.lonlat_celda(celda)
    ancho, rango = c1['ancho_angular'], c1['lat_norte'] - c1['lat_sur']
    if ancho <= 0 or rango == 0:
        return None
    dlon = (lon - c1['lon_central'] + 180.0) % 360.0 - 180.0
    u = max(0.0, min(1.0, 0.5 - dlon / ancho))
    if c1['espejo']:
        u = 1.0 - u
    v = max(0.0, min(1.0, (c1['lat_norte'] - lat) / rango))
    return de_suelo(c1, u * c1['ancho_sala'], v * c1['fondo_sala'])


# v17: el pisoton (tres visitantes en casillas que miran a la celda del monstruo). Con dos
# casillas, dos comparten la primera en diagonal, PISON_APARTE del centro en cada eje (0,42 m
# entre las cabezas y 0,1 m al borde: la camara ve la cabeza unos 0,1 m desplazada), y el
# tercero va al lado lejos de la segunda; con una, un triangulo de radio PISON_RADIO (0,38 m
# de lado). Separacioncabezas (fase 24) es 0,35.
PISON_APARTE = 0.15
PISON_RADIO = 0.22


def sitio_pison(m, W, c1, celda, i):
    """(x, z) de la sala del visitante i (0, 1 o 2) del pisoton sobre la celda: en casillas
    que la miran (todas, ocupadas o no: las ocupan ellos mismos), con las tres cabezas a
    mas de Separacioncabezas. None si ninguna casilla la mira."""
    ks = m.casillas_de_celda(W, c1, celda)
    if not ks:
        return None
    pts = [de_suelo(c1, *m.casilla_xy(c1, k)) for k in ks[:3]]
    i = int(i) % 3
    if len(pts) >= 3:
        return pts[i]
    if len(pts) == 2:
        (ax, az), (bx, bz) = pts
        dx, dz = bx - ax, bz - az
        n = math.hypot(dx, dz) or 1.0
        ux, uz = dx / n, dz / n
        if i == 2:
            return bx + PISON_APARTE * ux, bz + PISON_APARTE * uz
        s_ = 1.0 if i == 0 else -1.0    # en diagonal: uno lejos de la otra casilla, otro hacia ella
        return (ax + PISON_APARTE * (-s_ * ux - s_ * uz), az + PISON_APARTE * (-s_ * uz + s_ * ux))
    ax, az = pts[0]
    a = math.radians(90.0 + 120.0 * i)
    return ax + PISON_RADIO * math.cos(a), az + PISON_RADIO * math.sin(a)


def destino_a_punto(c, F, d, refs, evitar=()):
    """El destino de la coreografia en (x, z) de la sala, o 'fuera', o None si no se
    puede (sin FASE1, sin monstruo...)."""
    if d == _FUERA:
        return _FUERA
    if isinstance(d, (tuple, list)) and len(d) == 2 and all(isinstance(v, (int, float)) for v in d):
        return _libre(c, (float(d[0]), float(d[1])), evitar)
    kind = d[0]
    if kind == 'suelo':
        w, f = REJILLA_WEB
        if F is not None:
            c1 = F.cfg()
            x, z = de_suelo(c1, (d[1] + 0.5) / w * c1['ancho_sala'], (d[2] + 0.5) / f * c1['fondo_sala'])
        else:
            x, z = (d[1] + 0.5) / w * 5.4 - 2.7, (d[2] + 0.5) / f * 4.5 - 2.25
        return _libre(c, (x, z), evitar)
    if F is None:
        return None
    m, c1, W = F.m, F.cfg(), F.W()
    dx = dz = 0.0
    p = None
    if kind == 'celda':
        dx, dz, j = list(d[2:5]) + [0.0, 0.0, 0][len(d[2:5]):]
        p = punto_de_celda(m, W, c1, _ref(refs, d[1]), _GZ.get('libres'), j)
    elif kind == 'monstruo':
        J = W.get('juego') or {}
        mc = (J.get('mon') or {}).get('celda')
        if mc is None:
            return None
        dx, dz, j = list(d[3:6]) + [0.0, 0.0, 0][len(d[3:6]):]
        p = punto_de_celda(m, W, c1, m.celda_desplazada(mc, d[1], d[2]), _GZ.get('libres'), j)
    elif kind == 'pison':               # v17: los tres del pisoton, con las cabezas separadas
        J = W.get('juego') or {}
        mc = (J.get('mon') or {}).get('celda')
        p = sitio_pison(m, W, c1, mc, int(d[1])) if mc is not None else None
    elif kind == 'vecina_mon':          # v16: las vecinas que no cierra el cerco de cuatro
        J = W.get('juego') or {}
        mc = (J.get('mon') or {}).get('celda')
        vs = m.vecinas_cerco(mc) if mc is not None and hasattr(m, 'vecinas_cerco') else []
        if not vs:
            return None
        p = punto_de_celda(m, W, c1, vs[int(d[1]) % len(vs)], _GZ.get('libres'))
    elif kind == 'casilla':
        k = _ref(refs, (d[1], d[2])) if len(d) > 2 and isinstance(d[1], str) else _ref(refs, d[1])
        dx, dz = (list(d[3:5]) + [0.0, 0.0])[:2]
        if k is not None:
            p = de_suelo(c1, *m.casilla_xy(c1, k))
    if p is None:
        return None
    return _libre(c, (p[0] + dx, p[1] + dz), evitar)


REJILLA_WEB = (11, 9)


class Fase1(object):
    """Lo que la demo usa de FASE1: su motor (m), su mundo y su configuracion."""

    def __init__(self, base):
        self.base = base
        self.motor = base.op('motor')
        self.m = self.motor.module
        self._c = None

    def cfg(self, fresca=False):
        """La de este fotograma (cfg_foto), o la ultima (fresca, tras cambiar parametros)."""
        if self._c is None or fresca:
            try:
                self._c = self.m.cfg() if fresca else self.m.cfg_foto()
            except Exception:
                self._c = self.m.cfg()
        return self._c

    def W(self):
        return self.m.world()

    def par(self, nombre, defecto=None):
        p = getattr(self.base.par, nombre, None)
        try:
            return p.eval() if p is not None else defecto
        except Exception:
            return defecto

    def poner(self, nombre, valor):
        p = getattr(self.base.par, nombre, None)
        if p is None:
            return False
        try:
            p.val = valor
            self._c = None
            return True
        except Exception:
            return False


def fase1():
    try:
        b = op('/project1/FASE1')
        if b is None or b.op('motor') is None:
            return None
        return Fase1(b)
    except Exception:
        return None


# --- el director: entrar, capitulos, coreografia, salir ---------------------------

def _guardado():
    try:
        return parent().fetch('gz_guardado', None, search=False)
    except Exception:
        return _GZ.get('guardado')


def _guardar(v):
    _GZ['guardado'] = v
    try:
        if v is None:
            parent().unstore('gz_guardado')
        else:
            parent().store('gz_guardado', v)
    except Exception:
        pass


def _sala_par(nombre, valor):
    try:
        p = getattr(parent().par, nombre, None)
        if p is not None:
            p.val = valor
    except Exception:
        pass


# lo que la demo pone en la pagina Sala (y devuelve al salir): la vista juego, el arco de
# quietud y la luz de casa en lugar de la luz de prueba (su estrobo daria onsets que erosionan)
SALA_DEMO = dict(Vista='juego', Arcoquietud=True, Modoluz='apagado', Luzcasa=('min', 0.35))


def _valor_sala(nombre, valor):
    if isinstance(valor, tuple) and valor and valor[0] == 'min':
        try:
            return max(float(_p(nombre, 0.0)), float(valor[1]))
        except Exception:
            return valor[1]
    return valor


def _valor_par(F, nombre, valor):
    if isinstance(valor, tuple) and valor and valor[0] == 'min':
        try:
            return max(float(F.par(nombre, 0.0)), float(valor[1]))
        except Exception:
            return valor[1]
    return valor


def entrar(c, t, F, now):
    """Al entrar en una demo: guarda la escena de FASE1 en su hueco (Guardarescena en
    GZ_HUECO), sus parametros y la tabla sala_personas; luego pone los de la demo y
    empieza en Capitulo (GENoZilla) o en el primer caso. v21: el mundo no se guarda: la
    demo juega sobre el de FASE1 tal como esta. Si ya habia algo guardado (la sala se
    recargo a mitad), no lo pisa."""
    demo = DEMOS[c['demo'] % len(DEMOS)]
    _GZ.update(activo=True, acabada=False, tramos={}, saltar=False, resultados=[], cap=None, conservas=[],
               demo=demo, sec={}, sueltas=[], t_nota=None, t_lluvia=None, espera=None)
    if _guardado() is None and F is not None:
        try:
            F.m.guardar_escena(GZ_HUECO)
        except Exception:
            pass
        tb = F.base.op('sala_personas')
        nombres = sorted(set(PARS_DEMO) | set(PARS_SECCION) | set(PARS_CAPITULO))
        # v21: el mundo no se guarda (ni se devuelve al salir): la demo lo toma donde esta
        _guardar(dict(pars=dict((k, F.par(k)) for k in nombres if F.par(k) is not None),
                      tabla=[[x.val for x in tb.row(r)] for r in range(tb.numRows)] if tb is not None else None,
                      sala=dict((k, _p(k, None)) for k in SALA_DEMO)))
    if F is not None:
        for k, v in pars_demo(demo).items():
            F.poner(k, v)
    for k, v in SALA_DEMO.items():
        _sala_par(k, _valor_sala(k, v))
    _GZ['cap_par'] = c['capitulo']
    capitulo(c, t, F, now, c['capitulo'] if demo == 'genozilla' else 0)


def salir(F, cfg_sala=None):
    """Devuelve a FASE1 lo que la demo le cambio: los parametros del capitulo y de la
    demo, la escena (Cargarescena del hueco) y la tabla sala_personas. v21: el mundo
    no: sigue como lo dejo la demo (el planeta no vuelve atras)."""
    g = _guardado()
    if F is not None and _GZ.get('antes_cap'):
        for k, v in _GZ['antes_cap'].items():
            F.poner(k, v)
    if F is not None:
        _soltar_notas(F, None)
        try:
            F.m.foco_camara(None)       # v18: la camara de FASE1, a su sitio de siempre
        except Exception:
            pass
    _GZ.update(activo=False, cap=None, antes_cap={}, ruido=[], ganancia=1.0, tramos={}, saltar=False, demo=None,
               sueltas=[], cabecera=None, espera=None)
    if g is not None and F is not None:
        for k, v in g.get('pars', {}).items():
            F.poner(k, v)
        try:
            F.m.cargar_escena(GZ_HUECO)
            t = F.m.tabla_escenas()
            if t is not None:           # el hueco, fuera de la tabla de escenas
                filas = [[t[r, k].val for k in range(t.numCols)] for r in range(t.numRows)]
                t.clear()
                for f in filas:
                    if f and f[0] != GZ_HUECO:
                        t.appendRow(f)
        except Exception:
            pass
        tb = F.base.op('sala_personas')
        if tb is not None and g.get('tabla') is not None:
            tb.clear()
            for f in g['tabla']:
                tb.appendRow(f)
        _GZ['ultima_tabla'] = None      # v15: la tabla es la de antes; la proxima se escribe entera
        try:
            F.m.sala_reset(cuentas=False)
        except Exception:
            pass
        for k, v in (g.get('sala') or {}).items():
            _sala_par(k, v)
    _guardar(None)


def _cap_pars(F, k, c):
    """Los parametros de FASE1 del capitulo k: sus armas (solo la suya) y lo suyo (v21:
    nunca el giro). Devuelve los de antes, para devolverlos al acabar."""
    demo = demo_activa()
    cp = casos(demo)[k]
    if demo == 'genozilla':
        quiere = dict((a, False) for a in ARMAS)
        quiere['Umbralaparicion'] = 1.0     # el monstruo aparece cuando lo dice el guion
    else:
        quiere = dict(SECCIONES[demo]['pars'])
    # v21: ninguna demo toca el giro (Barsperturn): el planeta gira con los parametros de FASE1
    # v16: el Oceano de FASE1 se respeta (hasta la v15 se apagaba: con el, el mundo vacio de cada
    # capitulo era todo mar y el monstruo solo anda por tierra; sobre el mundo de FASE1 no hace falta)
    quiere.update(cp['pars'])
    antes = {}
    for nm, v in quiere.items():
        a = F.par(nm)
        if a is None:
            continue
        antes[nm] = a
        F.poner(nm, _valor_par(F, nm, v))
    return antes


def capitulo(c, t, F, now, k):
    """Empieza el capitulo (el caso) k en t (s de la sala): su titulo, los parametros y
    el guion de FASE1 (en GENoZilla, con Guion) y donde esta cada persona. v21: sobre el
    mundo de FASE1 tal como esta; si aun no tiene lo que el caso necesita (falta_caso),
    el caso espera (_GZ['espera']) con el titulo «Esperando que el mundo evolucione» y
    gz_tick lo vuelve a mirar cada ESPERA_CADA s."""
    demo = demo_activa()
    caps_ = casos(demo)
    k = int(k) % len(caps_)
    previa = _GZ.get('espera')
    previa = previa if previa is not None and previa.get('cap') == k else None
    if F is not None and _GZ.get('antes_cap'):
        for nm, v in _GZ['antes_cap'].items():
            F.poner(nm, v)
    _GZ['antes_cap'] = {}
    cp = caps_[k]
    if previa is not None:              # v21: la espera acaba: el titulo, ya entero (sin fundido de entrada)
        t_tit = t - TITULO_ENTRA
    else:
        t_tit = t
    t0 = t_tit + TITULO
    _GZ.update(cap=k, t_titulo=t_tit, t0=t0, hechas=set(), refs={}, saltar=False,
               ruido=[(t0 + a, t0 + b, md) for a, b, md in cp.get('ruido', ())], ganancia=1.0, cortes0=None,
               t_gan=None, reg=dict(cap=k), coreo=coreo_de(cp, c), t_lluvia=None, espera=None)
    ev = evitar_de(equipos_o_defecto(c))
    falta = None
    if F is not None:
        if demo != 'genozilla':
            _soltar_notas(F, now)
        if demo != 'genozilla' or c['guion']:
            _GZ['antes_cap'] = _cap_pars(F, k, c)
        c1 = F.cfg(fresca=True)
        W = F.W()
        _GZ['libres'] = casillas_libres(c, c1, F.m, ev)
        refs = {}
        try:                            # los sitios del caso (solo leen el mundo)
            if demo == 'genozilla':
                refs = brote_vivo(F, c1, W, k, F.m.demo_refs(W, c1, k, _GZ['libres']) or {}, _GZ['libres'])
            else:
                refs = refs_caso(demo, k, c1, F, W, _GZ['libres'])
        except Exception as e:
            print('SALA  demo %s: no pude preparar el caso %d (%s)' % (demo, k, e))
        _GZ['refs'] = refs
        try:
            falta = falta_caso(demo, k, F, c1, W, refs)
        except Exception as e:
            falta = None
            print('SALA  demo %s: no pude mirar lo que necesita el caso %d (%s)' % (demo, k, e))
        if falta:
            _GZ['espera'] = dict(cap=k, que=falta, desde=previa['desde'] if previa else t, revisa=t + ESPERA_CADA)
            _GZ['t_titulo'], _GZ['t0'] = t, t + TITULO
            if previa is None and not _GZ.get('callado'):
                print('SALA  demo %s, caso %d %s: esperando que el mundo evolucione (%s)'
                      % (demo, k, cp['nombre'], falta))
        elif demo != 'genozilla':
            try:
                _GZ['reg'].update(registro_inicial(F))
            except Exception:
                pass
        else:
            occ0 = list(W['occ'])       # v21: el mundo de FASE1 al empezar el capitulo (no el de la entrada)
            if c['guion']:
                try:                    # v21 (motor v141): sobre el mundo vivo, sin rehacerlo
                    refs = F.m.guion_demo(W, c1, k, 'inicio', now, refs=refs, libres=_GZ['libres'],
                                          vivo=True) or refs
                except Exception as e:
                    print('SALA  GENoZilla: el guion del capitulo %d fallo (%s)' % (k, e))
                _GZ['refs'] = refs
            try:                        # v16: lo que ya habia, para comprobar solo lo nuevo
                Wc = F.W()
                _GZ['reg']['coronas0'] = set(x for x in range(len(Wc['occ'])) if Wc['occ'][x] >= c1['th_crown'])
                # y cuanto del mundo de FASE1 se conserva: sus celdas ocupadas (menos las que el
                # capitulo cava o hace brote a proposito) siguen con su ocupacion o mas
                r_ = refs or {}
                desp = set(r_.get('canal') or ()) | {r_.get('brote')}
                cand = [x for x in range(len(occ0)) if occ0[x] > 0 and x not in desp]
                _GZ['reg']['conserva'] = (sum(1 for x in cand if Wc['occ'][x] >= occ0[x]), len(cand))
                _GZ.setdefault('conservas', []).append((k,) + _GZ['reg']['conserva'])
            except Exception:
                pass
    quien = set()
    for j, (tt, i, d) in enumerate(_GZ['coreo']):
        if tt < 0 and not falta:
            q = destino_a_punto(c, F, d, _GZ['refs'], ev)
            if q is not None:
                mover(c, i, q, t, ev, salto=True)
                quien.add(i)
            _GZ['hechas'].add(j)
    for i in range(n_personas(dict(c, demo=DEMOS.index(demo)))):    # los demas, fuera (entraran si les toca)
        if i not in quien:
            mover(c, i, _FUERA, t, ev, salto=previa is None)
    for i in list(_GZ['tramos']):       # los que sobran (menos Personas en la sala llena), fuera
        if i >= n_personas(dict(c, demo=DEMOS.index(demo))):
            del _GZ['tramos'][i]
    _GZ['rotulo'] = None
    _GZ['cabecera'] = None


ESPERA_CADA = 2.0           # v21: s entre una mirada y otra a lo que necesita un caso que espera
ESPERA_TITULO = 'Esperando que el mundo evolucione'


def _celdas_de_casillas(F, c1, W, ks):
    out = []
    for q in ks or ():
        x = F.m.celda_de_casilla(W, c1, q) if q is not None else None
        if x is not None and x not in out:
            out.append(x)
    return out


def brote_vivo(F, c1, W, k, refs, libres):
    """v21: el brote de los capitulos 3 y 4 de GENoZilla, en una celda vacia bajo la sala (el
    guion no borra lo construido para plantarlo); en el 3, con al menos BROTE_VECINAS vecinas
    vacias (el mal desborda sin pisar al publico: antes se despejaban). Sin ninguna, None
    (el capitulo espera: falta_caso)."""
    if k not in (3, 4):
        return refs
    m = F.m
    r = dict(refs)
    vac = _vacias_bajo_sala(F, c1, W, libres)
    vacia = lambda x: W['occ'][x] == 0 and W['sp'][x] == 0      # noqa: E731
    cols = m.rejilla_sala(c1)[0]
    k0 = m.demo_casilla(c1, 6.0, 4.0)
    orden = sorted(vac, key=lambda x: ((vac[x] % cols - k0 % cols) ** 2 + (vac[x] // cols - k0 // cols) ** 2, x))
    if k == 3:
        orden = [x for x in orden if sum(1 for v in m.NEIGH[x] if vacia(v)) >= BROTE_VECINAS]
    b = orden[0] if orden else None
    r['brote'] = b
    r['musica'] = [b] if b is not None else []
    r['despejar'] = []
    if k == 4 and b is not None:
        r['aliadas'] = m._vecinas_a_la_vista(W, c1, b, max(1, int(c1.get('aliados', 3))), libres)
    return r


BROTE_VECINAS = 3           # v21: vecinas vacias que pide el brote del capitulo 3 para desbordar


def falta_caso(demo, k, F, c1, W, refs):
    """v21: lo que el caso k necesita del mundo de FASE1 y aun no tiene (un texto), o
    None. La demo no lo fabrica (ni vacia celdas ni entierra conchas): espera a que el
    mundo evolucione (el giro trae celdas nuevas bajo la sala; los ciclos, conchas)."""
    r = refs or {}
    if demo == 'probabilidad':
        if r.get('testigo') is None or r.get('control') is None:
            return ('hacen falta dos celdas vacias bajo la sala, no vecinas, para medir la probabilidad (hay %d)'
                    % len(r.get('vacias') or ()))
        return None
    if demo == 'genozilla' and k in (3, 4) and r.get('brote') is None:
        return ('hace falta una celda vacia bajo la sala%s para plantar el brote'
                % (' con %d vecinas vacias' % BROTE_VECINAS if k == 3 else ''))
    pp = max(1, int(c1.get('conchas_persona', 1)))
    pide = []                           # (conchas, celdas, quien cava)
    if demo == 'huella' and k == 1:
        pide.append((5 * pp, r.get('fila_celdas') or [], 'la fila'))
    elif demo == 'genozilla':
        if k == 5:
            pide.append((3 * pp, _celdas_de_casillas(F, c1, W, r.get('fila')), 'la fila'))
        elif k == 6:
            fila = _celdas_de_casillas(F, c1, W, r.get('fila'))
            pide.append((4 * pp, fila, 'la fila'))
            pide.append((2, [x for x in (r.get('canal') or ()) if x not in fila], 'la zanja'))
        elif k == 10:
            pide.append((max(1, int(c1.get('prof_grito', 2))), [r.get('monstruo')], 'el grito'))
        elif k == 11:
            pide.append((3 * pp, _celdas_de_casillas(F, c1, W, r.get('fila')), 'la fila'))
    for n, celdas, quien in pide:
        celdas = [x for x in celdas if x is not None]
        if not celdas:
            continue
        hay = F.m.losetas_bajo(W, celdas)
        if hay < n:
            return 'hacen falta %d conchas debajo para que %s cave (hay %d)' % (n, quien, hay)
    return None


def equipos_o_defecto(c):
    try:
        return equipos()
    except Exception:
        return [fila_equipo(f) for f in equipos_defecto(c['ancho'], c['fondo'], c['alto'])]


def gz_tick(c, t, F, now, emular=False):
    """Un paso de la demo en t (s de la sala; now, el reloj de FASE1): entra o sale,
    cambia de capitulo, mueve a la gente segun la coreografia, el guion a su hora, la
    ganancia del grito y lo que se observa para comprobar el capitulo. v18: cualquier
    demo con seccion (todas menos la vacia); con la musica, la lluvia de notas y el foco
    de la camara de cada caso."""
    demo = DEMOS[c['demo'] % len(DEMOS)]
    activa = c['activa'] and demo in SECCIONES
    if _GZ['activo'] and _GZ.get('demo') != demo:       # v18: otra demo: se sale de la que habia
        cerrar_capitulo(F, now)
        salir(F)
        _GZ['acabada'] = False
    if not activa:
        if _GZ['activo'] or _guardado() is not None:
            salir(F)
        _GZ['acabada'] = False
        return None
    if not _GZ['activo']:
        if _GZ.get('acabada'):
            if _GZ['acabada'] in (True, demo) and not _GZ.get('saltar'):   # v18: acabada esa demo
                return None
            _GZ['acabada'] = False
        entrar(c, t, F, now)
    if demo == 'genozilla' and c['capitulo'] != _GZ.get('cap_par'):     # Capitulo cambiado a mano: a el
        _GZ['cap_par'] = c['capitulo']
        cerrar_capitulo(F, now)
        capitulo(c, t, F, now, c['capitulo'])
    caps_ = casos(demo)
    esp = _GZ.get('espera')
    if esp is not None and not _GZ.get('saltar'):     # v21: el caso espera a que el mundo evolucione
        if t >= esp['revisa']:
            capitulo(c, t, F, now, _GZ['cap'])          # lo vuelve a mirar: si ya lo tiene, empieza
        esp = _GZ.get('espera')
        if esp is not None:
            _GZ['t_titulo'], _GZ['t0'] = t, t + TITULO  # el caso no corre mientras espera
            if F is not None:
                foco_tick(c, F, t, evitar_de(equipos_o_defecto(c)))
                if not emular:
                    a_la_tabla(c, F, t, evitar_de(equipos_o_defecto(c)))
            return None
    cp = caps_[_GZ['cap']]
    if _GZ.get('saltar') or t - _GZ['t0'] >= cp['dur']:
        cerrar_capitulo(F, now)
        sig = _GZ['cap'] + 1
        if sig >= len(caps_):
            if not c['buclecap'] and not _GZ.get('saltar'):
                salir(F)
                _GZ['acabada'] = demo
                return None
            sig = 0
        capitulo(c, t, F, now, sig)
        cp = caps_[_GZ['cap']]
    tc = t - _GZ['t0']
    ev = evitar_de(equipos_o_defecto(c))
    for j, (tt, i, d) in enumerate(_GZ['coreo']):
        if j in _GZ['hechas'] or tt > tc:
            continue
        q = destino_a_punto(c, F, d, _GZ['refs'], ev)
        if q is not None or d == _FUERA:
            mover(c, i, q, t, ev)
            _GZ['hechas'].add(j)
        elif tc - tt > 2.0:             # sin destino (no hay monstruo): se deja
            _GZ['hechas'].add(j)
    if F is None:
        return None
    if demo == 'genozilla':
        if c['guion']:
            try:
                F.m.guion_demo(F.W(), F.cfg(), _GZ['cap'], 'tick', now, tc)
            except Exception as e:
                if not _GZ.get('err_tick'):
                    _GZ['err_tick'] = True
                    print('SALA  GENoZilla: guion_demo fallo (%s)' % e)
        ganancia_grito(F, t)
        observar(F, now, tc)
    else:
        try:
            if tc >= 0.0 and cp.get('musica'):
                musica_quietos(F, now)
            if tc >= 0.0 and cp.get('lluvia'):
                lluvia(F, now, cp['lluvia'])
            observar_caso(c, F, t, now, tc, ev)
        except Exception as e:
            if not _GZ.get('err_caso'):
                _GZ['err_caso'] = True
                print('SALA  demo %s: fallo en el caso %d (%s)' % (demo, _GZ['cap'], e))
    foco_tick(c, F, t, ev)
    if not emular:
        a_la_tabla(c, F, t, ev)
    return tc


# --- v18: lo de las demos de seccion (todas menos GENoZilla) ---------------------

def _celda_de_punto(F, c1, W, x, z):
    """La celda que mira al punto (x, z) de la sala, o None fuera del suelo cubierto."""
    xf, yf = a_suelo(c1, x, z)
    k = F.m.casilla_de_xy(c1, xf, yf)
    return None if k is None else F.m.celda_de_casilla(W, c1, k)


def _fila_central(F, c1, libres, n=5):
    """n casillas seguidas en una fila de la rejilla, todas al alcance del publico, lo mas
    al centro de la sala posible."""
    m = F.m
    cols, filas = m.rejilla_sala(c1)
    k0 = m.demo_casilla(c1, 5.0, 5.0)
    f0, col0 = k0 // cols, k0 % cols
    for df in (0, 1, -1, 2, -2, 3, -3):
        f = f0 + df
        if not 0 <= f < filas:
            continue
        for dc in (0, 1, -1, 2, -2):
            a = col0 - n // 2 + dc
            if a < 0 or a + n > cols:
                continue
            ks = [f * cols + a + j for j in range(n)]
            if libres is None or all(k in libres for k in ks):
                return ks
    return [f0 * cols + max(0, min(cols - n, col0 - n // 2)) + j for j in range(n)]


def _vacias_bajo_sala(F, c1, W, libres):
    """v21: las celdas vacias (sin ocupacion, sin especie, sin zanja) que miran a alguna
    casilla al alcance del publico: {celda: la casilla mas al centro que la mira}."""
    m = F.m
    cols, filas = m.rejilla_sala(c1)
    zj = (W.get('juego') or {}).get('zanjas') or {}
    out = {}
    for k in sorted(libres or (), key=lambda q: (abs(q % cols - (cols - 1) / 2.0)
                                                 + abs(q // cols - (filas - 1) / 2.0), q)):
        x = m.celda_de_casilla(W, c1, k)
        if x is None or x in out or x in zj:
            continue
        if W['occ'][x] == 0 and W['sp'][x] == 0:
            out[x] = k
    return out


def refs_caso(demo, k, c1, F, W, libres):
    """Los sitios con nombre del caso (solo lee): celdas y casillas de su coreografia.
    v21: nada que despejar ni conchas que enterrar: la probabilidad mide sobre dos celdas
    que ya esten vacias bajo la sala (si no las hay, el caso espera: falta_caso)."""
    m = F.m
    cel = lambda cx, cy: m.demo_celda(W, c1, cx, cy, libres)       # noqa: E731
    r = dict(demo=demo, cap=int(k))
    if demo == 'probabilidad':
        vac = _vacias_bajo_sala(F, c1, W, libres)
        r['vacias'] = sorted(vac)
        cols = m.rejilla_sala(c1)[0]
        k0 = m.demo_casilla(c1, 5.0, 4.0)
        d2 = lambda q, q0: (q % cols - q0 % cols) ** 2 + (q // cols - q0 // cols) ** 2     # noqa: E731
        orden = sorted(vac, key=lambda x: (d2(vac[x], k0), x))
        t_ = orden[0] if orden else None
        ctrl = None
        if t_ is not None:              # la de control: vacia, no vecina y lo mas lejos de la testigo
            lejos = [x for x in orden if x != t_ and x not in m.NEIGH[t_]]
            if lejos:
                ctrl = max(lejos, key=lambda x: (d2(vac[x], vac[t_]), -x))
        r['testigo'] = t_
        r['control'] = ctrl
    elif demo == 'huella' and k == 0:
        r['quietos'] = [cel(cx, cy) for cx, cy in ((2.5, 3.0), (8.0, 2.0), (3.0, 6.5), (8.5, 6.0))]
    elif demo == 'huella' and k == 1:
        r['fila'] = _fila_central(F, c1, libres, 5)
        fc = []
        for q in r['fila']:
            x = m.celda_de_casilla(W, c1, q)
            if x not in fc:
                fc.append(x)
        r['fila_celdas'] = fc           # v21: sin conchas enterradas a proposito (falta_caso las pide)
    return r


def _dejadas(W):
    """Las inclusiones que ha dejado la gente en este mundo (llegadas y paradas), sigan
    vivas o no (las borra la erosion o una escision)."""
    cu = W.get('incl_n') or {}
    return int(cu.get('llegadas', 0)) + int(cu.get('paradas', 0))


def registro_inicial(F):
    W = F.W()
    return dict(occ0=list(W['occ']), incl0=F.m.n_inclusiones(W), dej0=_dejadas(W),
                esc0=set(e['id'] for e in W.get('escisiones', ())), dentro_max=0, salidas=0, entradas=0,
                vistos=set(), dentro_prev=set(), grupo=False, p=[], esc_prof=[], llueve={})


def _soltar_notas(F, now):
    """Las notas de la demo que siguen sonando, sueltas (now None: todas, ya)."""
    try:
        W, c1 = F.W(), F.cfg()
        for nota, t_off in list(_GZ.get('sueltas') or ()):
            if now is None or now >= t_off:
                F.m.note_off(W, c1, F.m.GEO, nota, now if now is not None else (W.get('t') or 0.0), F.m.tempo())
                _GZ['sueltas'].remove((nota, t_off))
    except Exception:
        _GZ['sueltas'] = []


def _nota(F, W, c1, celda, now, cada):
    """Una nota del SEQ1 en la celda (pasa por el sorteo de la presencia, como cualquier
    nota). Devuelve si prende."""
    m = F.m
    nota = m.cell_note(celda)
    r = m.note_on(W, c1, m.GEO, nota, 100, now, m.tempo()) or {}
    _GZ.setdefault('sueltas', []).append((nota, now + 0.5 * cada))
    return r.get('estado') not in ('no prende', 'fuera de rango')


def musica_quietos(F, now):
    """La musica de la demo: una nota cada MUSICA_CADA s por cada casilla con alguien
    quieto MUSICA_QUIETO s, en la celda que la mira (como la de GENoZilla)."""
    _soltar_notas(F, now)
    tn = _GZ.get('t_nota')
    if tn is not None and 0.0 <= now - tn < MUSICA_CADA - 1e-9:
        return 0
    _GZ['t_nota'] = now
    m = F.m
    W, c1 = F.W(), F.cfg()
    n = 0
    hechas = set()
    for k, v in sorted((m._SALA.get('casillas') or {}).items()):
        if now - v.get('t_ocupada', now) < MUSICA_QUIETO - 1e-9:
            continue
        x = m.celda_de_casilla(W, c1, k)
        if x is None or x in hechas:
            continue
        hechas.add(x)
        _nota(F, W, c1, x, now, MUSICA_CADA)
        n += 1
    return n


def lluvia(F, now, nombres):
    """La probabilidad, medida: una nota cada LLUVIA_CADA s en cada celda de las refs
    'nombres' (la testigo y la de control), y cuantas prenden."""
    _soltar_notas(F, now)
    tl = _GZ.get('t_lluvia')
    if tl is not None and 0.0 <= now - tl < LLUVIA_CADA - 1e-9:
        return
    _GZ['t_lluvia'] = now
    W, c1 = F.W(), F.cfg()
    cu = _GZ['reg'].setdefault('llueve', {})
    for nm in nombres:
        x = (_GZ.get('refs') or {}).get(nm)
        if x is None:
            continue
        si = _nota(F, W, c1, x, now, LLUVIA_CADA)
        e = cu.setdefault(nm, [0, 0])
        e[0] += 1
        e[1] += int(si)


def observar_caso(c, F, t, now, tc, ev):
    """Lo que pasa en la sala y en FASE1 durante el caso, para la cabecera y para
    comprobarlo al final."""
    reg = _GZ['reg']
    if tc < 0.0:
        return
    dentro = set(i for i, x, z, h, a in personas(c, t, ev))
    prev = reg.get('dentro_prev', set())
    reg['entradas'] = reg.get('entradas', 0) + len(dentro - prev)
    reg['salidas'] = reg.get('salidas', 0) + len(prev - dentro)
    reg['dentro_prev'] = dentro
    reg['dentro_max'] = max(reg.get('dentro_max', 0), len(dentro))
    reg.setdefault('vistos', set()).update(dentro)
    if {4, 5, 6, 7} <= dentro:
        reg['grupo'] = True
    m = F.m
    W, c1 = F.W(), F.cfg()
    dej = _dejadas(W)                   # las que deja la gente (al enterrar el mundo, la cuenta vuelve a 0)
    prev_ = reg.get('dej_prev', reg.get('dej0', dej))
    reg['dej_suma'] = reg.get('dej_suma', 0) + (dej - prev_ if dej >= prev_ else dej)
    reg['dej_prev'] = dej
    r = _GZ.get('refs') or {}
    if r.get('testigo') is not None:
        p = m.presencia_prob(W, c1, r['testigo'], 'crear')
        reg['p_ahora'] = p
        if r.get('control') is not None:
            reg['p_control'] = m.presencia_prob(W, c1, r['control'], 'crear')
        if tc >= P_DESDE:
            reg.setdefault('p', []).append(p)
    nuevas = [e for e in W.get('escisiones', ()) if e['id'] not in reg.get('esc0', ())]
    if nuevas:
        e = nuevas[-1]
        prof = len(e.get('cortadas') or ())
        if not reg['esc_prof'] or reg['esc_prof'][-1] != prof:
            reg['esc_prof'].append(prof)
        reg['esc'] = dict(id=e['id'], personas=e['personas'], conchas=prof, celda=e.get('origen'))


def _promedio(xs):
    return sum(xs) / float(len(xs)) if xs else 0.0


def comprobar_caso(F, demo, k, reg, now):
    """La comprobacion del caso k de una demo de seccion: (bien, que)."""
    m = F.m
    W, c1 = F.W(), F.cfg()
    occ0 = reg.get('occ0') or list(W['occ'])
    crece = [x for x in range(len(W['occ'])) if W['occ'][x] > occ0[x]]
    incl = reg.get('dej_suma', 0)       # las que ha dejado la gente en el caso
    sec = _GZ.setdefault('sec', {})
    if demo == 'paseo':
        bien = (reg.get('dentro_max', 0) >= 5 and reg.get('salidas', 0) >= 4 and reg.get('grupo') and bool(crece))
        return bien, ('hasta %d a la vez, %d salidas, grupo de 4 %s, %d celdas crecen'
                      % (reg.get('dentro_max', 0), reg.get('salidas', 0), 'si' if reg.get('grupo') else 'no',
                         len(crece)))
    if demo == 'probabilidad':
        r = _GZ.get('refs') or {}
        cu = float(c1.get('cuanto', 0.0))
        p = _promedio(reg.get('p') or [])
        sec[k] = p
        ll = reg.get('llueve') or {}
        lt, lc = ll.get('testigo', [0, 0]), ll.get('control', [0, 0])
        que = 'P media %.2f (Cuanto %.2f), testigo %d/%d, control %d/%d' % (p, cu, lt[1], lt[0], lc[1], lc[0])
        if not c1.get('presencia_activa') or lt[0] < 10:
            return False, que + ' (sin sorteo o sin lluvia)'
        if k == 0:                      # v21: con margen hasta el de una persona quieta (cu + 0,08)
            return p < cu + 0.08, que
        if k == 1:
            return p >= cu + 0.08 and p <= 0.9, que
        t_ = r.get('testigo')
        sube = t_ is not None and W['occ'][t_] > occ0[t_]
        return (p >= 0.75 and p > sec.get(1, 0.0) + 0.1 and sube,
                que + ', la testigo %s' % ('crece' if sube else 'no crece'))
    if demo == 'huella' and k == 0:
        q = [x for x in (_GZ.get('refs') or {}).get('quietos', ()) if x is not None]
        suben = [x for x in q if W['occ'][x] > occ0[x]]
        return incl >= 4 and len(suben) >= 3, '%d inclusiones dejadas, %d de %d celdas construyen' % (
            incl, len(suben), len(q))
    if demo == 'huella':
        e = reg.get('esc') or {}
        pr = reg.get('esc_prof') or []
        return (3 in pr and e.get('conchas') == 5 and e.get('personas') == 5,
                'escision: %s conchas con %s personas (fue %s)' % (e.get('conchas', '-'), e.get('personas', '-'),
                                                                  ' -> '.join(str(x) for x in pr) or '-'))
    if demo == 'llena':
        esc = [e for e in W.get('escisiones', ()) if e['id'] not in reg.get('esc0', ())]
        return (reg.get('dentro_max', 0) >= LLENA_MIN and reg.get('salidas', 0) >= 3 and incl >= 5,
                'hasta %d a la vez, %d entradas, %d salidas, %d inclusiones dejadas, %d celdas crecen, %d escisiones'
                % (reg.get('dentro_max', 0), reg.get('entradas', 0), reg.get('salidas', 0), incl, len(crece),
                   len(esc)))
    return True, ''


# --- v18: la camara de FASE1 sigue a las celdas donde pasan las cosas (motor v140) ---

def foco_celdas(c, F, t, ev):
    """Las celdas a las que mira la camara de FASE1 en este caso, o [] (su sitio)."""
    if F is None or _GZ.get('cap') is None:
        return []
    demo = demo_activa()
    cp = casos(demo)[_GZ['cap']]
    modo = cp.get('foco', 'monstruo' if demo == 'genozilla' else 'quietos')
    W, c1 = F.W(), F.cfg()
    if isinstance(modo, tuple) and modo[0] == 'refs':
        v = (_GZ.get('refs') or {}).get(modo[1])
        v = v if isinstance(v, (list, tuple)) else [v]
        v = [x for x in v if x is not None]
        if v:
            return v
        modo = 'quietos'
    if modo == 'monstruo':
        mo = ((W.get('juego') or {}).get('mon') or {})
        if mo.get('celda') is not None and mo.get('estado') not in (None, 'espera', 'muere'):
            return [mo['celda']]
    quietos, todos = [], []
    for i, x, z, h, andando in personas(c, t, ev):
        x_ = _celda_de_punto(F, c1, W, x, z)
        if x_ is None:
            continue
        todos.append(x_)
        if not andando:
            quietos.append(x_)
    return quietos or todos


def foco_tick(c, F, t, ev):
    """La camara de FASE1 mira a las celdas del caso (Siguecamara); sin el, a su sitio."""
    if F is None or not hasattr(F.m, 'foco_camara'):
        return None
    cs = foco_celdas(c, F, t, ev) if c.get('sigue_camara', False) else []
    try:
        F.m.foco_camara(cs)
    except Exception:
        return None
    return cs


def ganancia_grito(F, t):
    """D4: en el tramo del grito, cada segundo sin que FASE1 abra un corte por el ruido
    de sala (Umbralcorte), el grito sube GRITO_SUBE veces (hasta GANANCIA_MAX)."""
    if ruido_demo(t) != 'grito':
        return
    r = F.W().get('ruido') or {}
    n = r.get('cortes', 0)
    if _GZ.get('cortes0') is None:
        _GZ.update(cortes0=n, t_gan=t)
    if n != _GZ['cortes0']:
        return
    if t - _GZ['t_gan'] >= 1.0:
        _GZ['t_gan'] = t
        _GZ['ganancia'] = min(GANANCIA_MAX, _GZ['ganancia'] * GRITO_SUBE)


def a_la_tabla(c, F, t, ev=()):
    """La gente de la sala, en la tabla sala_personas de FASE1 (x, y, altura en metros
    del suelo cubierto): FASE1 la ve por su sala simulada, la misma imagen de alturas
    que la camara."""
    tb = F.base.op('sala_personas')
    if tb is None:
        return
    c1 = F.cfg()
    filas = []
    for i, x, z, h, _ in personas(c, t, ev):
        xf, yf = a_suelo(c1, x, z)
        filas.append(['%.3f' % xf, '%.3f' % yf, '%.2f' % h])
    if filas == _GZ.get('ultima_tabla'):
        return
    _GZ['ultima_tabla'] = filas
    tb.clear()
    tb.appendRow(list(F.m.SALA_COLS))
    for f in filas:
        tb.appendRow(f)


def demo_tick():
    """Desde frame_tick: la demo en el reloj de la sala (sin demo, casi nada)."""
    if not _GZ['activo'] and str(_p('Demo', 'paseo')) not in SECCIONES and _guardado() is None:
        _GZ['acabada'] = False          # v18: sin demo, la que acabo ya puede volver a empezar
        return
    gz_tick(cfg(), ahora(), fase1(), absTime.seconds)


# =============================================================================
# v15: EL PUBLICO A FASE1 EN TODAS LAS DEMOS (Alimentar)
# =============================================================================
# La sala hace de camara cenital en cualquier demo: escribe su gente en la tabla
# sala_personas de FASE1 (a_la_tabla, solo cuando cambia) y pone Fuente = simulada.
# Lo que habia antes (la Fuente y la tabla) se guarda en el storage de la sala
# ('pub_guardado', sobrevive a recargar el motor) y se devuelve al apagar Alimentar o
# Activa. En la demo GENoZilla escribe la tabla su director (gz_tick); aqui solo se
# mantiene lo guardado.

PUB_CLAVE = 'pub_guardado'


def _pub_guardado():
    try:
        return parent().fetch(PUB_CLAVE, None, search=False)
    except Exception:
        return _SALA.get(PUB_CLAVE)


def _pub_guardar(v):
    _SALA[PUB_CLAVE] = v
    try:
        if v is None:
            parent().unstore(PUB_CLAVE)
        else:
            parent().store(PUB_CLAVE, v)
    except Exception:
        pass


def _tabla_de(tb):
    return [[x.val for x in tb.row(r)] for r in range(tb.numRows)] if tb is not None else None


def alimentar_entra(F):
    """Guarda la Fuente y la tabla sala_personas de FASE1 y pone Fuente = simulada."""
    if _pub_guardado() is None:
        _pub_guardar(dict(fuente=F.par('Fuente'), tabla=_tabla_de(F.base.op('sala_personas'))))
    F.poner('Fuente', 'simulada')
    _GZ['ultima_tabla'] = None


def alimentar_sale(F, g=None):
    """FASE1 vuelve a la Fuente y a la tabla de antes de alimentarla."""
    g = _pub_guardado() if g is None else g
    if g is None:
        return False
    if F is not None:
        if g.get('fuente') is not None:
            F.poner('Fuente', g['fuente'])
        tb = F.base.op('sala_personas')
        if tb is not None and g.get('tabla') is not None:
            tb.clear()
            for f in g['tabla']:
                tb.appendRow(f)
        try:
            F.m.sala_reset(cuentas=False)
        except Exception:
            pass
    _GZ['ultima_tabla'] = None
    _pub_guardar(None)
    return True


def alimentar_tick(c=None, F=None, t=None):
    """Cada fotograma: con Activa y Alimentar, la gente de la sala a FASE1. Devuelve
    si la sala alimenta a FASE1."""
    c = cfg() if c is None else c
    F = fase1() if F is None else F
    quiere = c['activa'] and c['alimentar'] and F is not None and F.par('Fuente') is not None
    if not quiere:
        if _pub_guardado() is not None:
            alimentar_sale(F)
        return False
    if _pub_guardado() is None:
        alimentar_entra(F)
    if _GZ.get('activo'):               # en GENoZilla, la tabla la escribe gz_tick
        return True
    a_la_tabla(c, F, ahora() if t is None else t, evitar_de(equipos_o_defecto(c)))
    return True


# --- lo que se mira para comprobar cada capitulo ---------------------------------

def observar(F, now, tc):
    """Lo que pasa en FASE1 durante el capitulo, para comprobarlo al final."""
    reg = _GZ['reg']
    if tc < 0.0:
        return
    m = F.m
    W = F.W()
    J = W.get('juego') or {}
    mo = J.get('mon') or {}
    vivo = mo.get('estado') not in (None, 'espera', 'muere') and mo.get('celda') is not None
    if vivo:
        reg['tam_max'] = max(reg.get('tam_max', 0.0), mo.get('tam', 0.0))
        reg.setdefault('acum_ini', mo.get('acum', 0))
        reg['acum_min'] = min(reg.get('acum_min', 99), mo.get('acum', 0))
        if mo.get('estado') == 'cae' and mo.get('acum', 0) == 0:
            reg['caida0'] = True
        # v16: o cae y pierde lo devorado entre dos miradas (en el mundo de FASE1, lo que su
        # vecina ha desbordado en la zanja se lo come en el mismo fotograma de la caida)
        if mo.get('caidas', 0) > reg.get('caidas', 0) and mo.get('acum', 0) <= 1 < reg.get('acum_prev', 0):
            reg['caida0'] = True
        reg['caidas'] = max(reg.get('caidas', 0), mo.get('caidas', 0))
        reg['acum_prev'] = mo.get('acum', 0)
        if mo.get('acorralado'):
            reg['acorralado'] = True
            reg.setdefault('celda_cerco', mo.get('celda'))      # v14: de donde tiene que escapar
            reg.setdefault('acum_cerco', mo.get('acum', 0))
            reg['acum_cerco_min'] = min(reg.get('acum_cerco_min', 99), mo.get('acum', 0))
        if mo.get('piedra') is not None and now < mo['piedra']:
            reg['piedra'] = True
        if mo.get('aturdido') is not None and now < mo['aturdido'] and tc > 0.5:
            reg['aturdido'] = True
        if reg.get('murio'):
            reg['reaparece'] = True
    reg['acorralado_fin'] = bool(vivo and mo.get('acorralado'))
    if vivo and reg.get('celda_cerco') is not None and mo.get('celda') != reg['celda_cerco']:
        reg['escapa'] = True                # v14: el cerco se abrio y salio de su celda
    if mo.get('estado') == 'muere':
        reg['murio'] = True
    reg['n_max'] = max(reg.get('n_max', 0), mo.get('n', 0))
    try:
        if m.noche_nivel(W, F.cfg(), now) > 0.0:
            reg['noche'] = True
    except Exception:
        pass


def comprobar_capitulo(F, k, reg, now):
    """La columna Comprobar del capitulo k: (bien, que)."""
    m = F.m
    W = F.W()
    c1 = F.cfg()
    J = W.get('juego') or {}
    refs = _GZ.get('refs') or {}
    N = len(W['occ'])
    if not J:
        return False, 'sin partida (Modojuego)'
    if k == 0:
        gente = [p for p in m.personas_en_sala() if p.get('casilla') is not None]
        out = m.build_juego(W, c1, now, {})
        celdas = set(m.celda_de_casilla(W, c1, p['casilla']) for p in gente)
        return (bool(gente) and len(out.get('marcas', ())) >= len(celdas) > 0,
                '%d personas en %d celdas, %d piezas de marca' % (len(gente), len(celdas), len(out.get('marcas', ()))))
    if k == 1:
        cas = m._SALA.get('casillas') or {}
        celdas = set(m.celda_de_casilla(W, c1, q) for q in cas)
        vacias = [x for x in celdas if W['occ'][x] <= 0]
        # v16: en el mundo de FASE1 ya puede haber coronas: cuentan las de este capitulo
        coronas = [x for x in range(N) if W['occ'][x] >= c1['th_crown'] and x not in reg.get('coronas0', ())]
        return (bool(celdas) and not vacias and bool(coronas),
                '%d celdas con gente, %d vacias, coronas nuevas %s' % (len(celdas), len(vacias), coronas))
    if k == 2:
        # v16: los brotes que deja este monstruo (en el mundo de FASE1 puede haber mal de antes)
        mal = J.get('brotes', 0)
        return (mal >= 1 and reg.get('tam_max', 0.0) >= 1.0 - 1e-9,
                '%d brotes del mal, tamano maximo %.2f' % (mal, reg.get('tam_max', 0.0)))
    if k == 3:
        b = refs.get('brote')
        if b is None:
            return False, 'sin brote'
        vec = [x for x in m.NEIGH[b] if W['occ'][x] > 0 and W['sp'][x] == m.MAL]
        return (W['sp'][b] == m.MAL and W['occ'][b] > 1 and bool(vec),
                'el brote %d: ocupacion %d, %d vecinas del mal' % (b, W['occ'][b], len(vec)))
    if k == 4:
        b = refs.get('brote')
        if b is None:
            return False, 'sin brote'
        return (W['sp'][b] in (m.GEO, m.ARQ) and W['occ'][b] >= 4 and J.get('rescatados', 0) >= 1,
                'celda %d: especie %s, ocupacion %d, rescates %d' % (b, W['sp'][b], W['occ'][b],
                                                                     J.get('rescatados', 0)))
    if k == 5:
        b = W.get('bloqueadas') or {}
        zj = J.get('zanjas') or {}
        return (bool(reg.get('caida0')) and bool(zj) and all(x in b for x in zj),
                'caidas %d (acum 0: %s), zanja %s, fijada %s' % (reg.get('caidas', 0), bool(reg.get('caida0')),
                                                                sorted(zj), sorted(b)))
    if k == 6:
        return (bool(reg.get('murio')) and bool(reg.get('reaparece')),
                'ahogado %s, reaparece %s (monstruos %d)' % (bool(reg.get('murio')), bool(reg.get('reaparece')),
                                                            reg.get('n_max', 0)))
    if k == 7:
        baja = reg.get('acum_cerco_min', 99) < reg.get('acum_cerco', -1)
        # v14: que se escapa es que sale de la celda en la que lo acorralaron (antes: que al
        # final no estuviera acorralado; con el monstruo mas lento, en la celda a la que
        # escapa lo vuelven a cercar los que estan cerca)
        return (bool(reg.get('acorralado')) and baja and bool(reg.get('escapa')),
                'acorralado %s, acum %s -> %s, %s' % (
                    bool(reg.get('acorralado')), reg.get('acum_cerco', '-'), reg.get('acum_cerco_min', '-'),
                    'se escapa' if reg.get('escapa') else 'no sale de su celda'))
    if k == 8:
        return (reg.get('acum_min', 99) < 8 and reg.get('acum_ini', 0) >= 8,
                'acum %s -> %s' % (reg.get('acum_ini', '-'), reg.get('acum_min', '-')))
    if k == 9:
        return bool(reg.get('piedra')), 'petrificado %s' % bool(reg.get('piedra'))
    if k == 10:
        A = J.get('armas') or {}
        g = (J.get('ev') or {}).get('grito') or {}
        zj = J.get('zanjas') or {}
        b = W.get('bloqueadas') or {}
        pozo = g.get('celda') is not None and (g['celda'] in zj or g['celda'] in b)
        return (A.get('gritos', 0) >= 1 and pozo and reg.get('caidas', 0) >= 1,
                'gritos %d, pozo en %s, caidas %d' % (A.get('gritos', 0), g.get('celda'), reg.get('caidas', 0)))
    if k == 11:
        A = J.get('armas') or {}
        s = W.get('sala') or {}
        return (bool(reg.get('aturdido')) and A.get('rayos', 0) >= 1 and s.get('relampagos', 0) >= 1,
                'aturdido %s, rayos %d, relampagos %d' % (bool(reg.get('aturdido')), A.get('rayos', 0),
                                                         s.get('relampagos', 0)))
    if k == 12:
        rs = J.get('resultados') or []
        return (bool(rs) and bool(reg.get('noche')),
                'resultados %s, noche %s' % (['%s %d-%d' % (r['gana'], r['publico'], r['mal']) for r in rs],
                                             bool(reg.get('noche'))))
    return True, ''


def cerrar_capitulo(F, now):
    """El capitulo acaba: su comprobacion (al Textport y a _GZ['resultados'])."""
    k = _GZ.get('cap')
    if k is None or F is None:
        return None
    demo = demo_activa()
    try:
        if _GZ.get('espera') is not None:           # v21: no llego a empezar
            bien, que = False, 'sin probar: esperando que el mundo evolucione (%s)' % _GZ['espera']['que']
        elif demo == 'genozilla':
            bien, que = comprobar_capitulo(F, k, _GZ['reg'], now)
        else:
            bien, que = comprobar_caso(F, demo, k, _GZ['reg'], now)
    except Exception as e:
        bien, que = False, 'no pude comprobarlo (%s)' % e
    _GZ['resultados'].append((k, bien, que))
    if not _GZ.get('callado'):
        print('%s  %2d %-24s %s  %s' % ('GENOZILLA' if demo == 'genozilla' else 'DEMO %s' % demo.upper(), k,
                                        casos(demo)[k]['nombre'], 'OK   ' if bien else 'FALLO', que))
    return bien


# --- titulo, rotulo y leyenda ---------------------------------------------------

def _valores_texto(F):
    v = dict(tfila='4', taliados='3', tquietud='4', tpiedra='6', taturdido='4', recarga='30', aliados='3',
             gana='Gana la sala.', cuanto='0,5', probllegada='0,6', tparada='3')
    if F is None:
        return v
    try:
        c1 = F.cfg()
        v.update(cuanto=('%g' % c1['cuanto']).replace('.', ','),
                 probllegada=('%g' % c1['prob_llegada']).replace('.', ','), tparada='%g' % c1['t_parada'])
    except Exception:
        pass
    try:
        c1 = F.cfg()
        v.update(tfila='%g' % c1['t_fila'], taliados='%g' % c1['t_aliados'], tquietud='%g' % c1['t_quietud'],
                 tpiedra='%g' % c1['t_piedra'], taturdido='%g' % c1['t_aturdido'],
                 recarga='%g' % c1['recarga_grito'], aliados='%d' % int(c1['aliados']))
        J = F.W().get('juego') or {}
        rs = J.get('resultados') or []
        if rs:
            r = rs[-1]
            v['gana'] = '%s: publico %d, mal %d, en todo el globo.' % (
                'Gana la sala' if r['gana'] == 'publico' else 'Gana el mal', r['publico'], r['mal'])
    except Exception:
        pass
    return v


def _formato(texto, F):
    try:
        return texto.format(**_valores_texto(F))
    except Exception:
        return texto


def titulo_alfa(frame=None):
    """La opacidad del titulo (Level TOP titulo_fundido), ahora."""
    try:
        return alfa_titulo(ahora())
    except Exception:
        return 0.0


def alfa_titulo(t):
    """La opacidad del titulo (0-1) en t: TITULO s al empezar cada capitulo, con su
    fundido (TITULO_ENTRA de entrada y TITULO_SALE de salida)."""
    if not _GZ.get('activo') or _GZ.get('t_titulo') is None:
        return 0.0
    if _GZ.get('espera') is not None:   # v21: mientras el caso espera, el titulo lo dice entero
        return 1.0
    u = t - _GZ['t_titulo']
    if u < 0.0 or u > TITULO:
        return 0.0
    return max(0.0, min(1.0, u / TITULO_ENTRA, (TITULO - u) / TITULO_SALE))


def titulo_texto(que, frame=None):
    """Las tres lineas del titulo: 'ante' (antetitulo), 'nombre' y 'sub'."""
    k = _GZ.get('cap')
    if not _GZ.get('activo') or k is None:
        return ''
    if que == 'ante':
        return antetitulo(k)
    cp = casos()[k]
    esp = _GZ.get('espera')
    if esp is not None:                 # v21: el caso espera: lo dice y dice por que
        if que == 'nombre':
            return ESPERA_TITULO
        return 'para probar %s: %s' % (cp['nombre'], esp['que'])
    if que == 'nombre':
        return cp['nombre']
    return _formato(cp['sub'], None if demo_activa() == 'genozilla' else fase1())


def rotulo_texto(t=None, F=None):
    """El rotulo del capitulo en t (vacio durante el titulo)."""
    k = _GZ.get('cap')
    if not _GZ.get('activo') or k is None or _GZ.get('espera') is not None:     # v21: esperando, sin rotulo
        return ''
    t = ahora() if t is None else t
    tc = t - _GZ['t0']
    if tc < 0.0:
        return ''
    txt = ''
    for t0, s in casos()[k]['rotulos']:
        if t0 <= tc + 1e-9:
            txt = s
    return _formato(txt, F)


def rotulo_demo(frame=None):
    """El Text TOP rotulo_demo: se rehace cada ROTULO_CADA fotogramas."""
    f = absTime.frame
    if _GZ.get('rotulo') is not None and _GZ.get('rotulo_frame') is not None \
            and 0 <= f - _GZ['rotulo_frame'] < ROTULO_CADA:
        return _GZ['rotulo']
    _GZ['rotulo'], _GZ['rotulo_frame'] = rotulo_texto(F=fase1()), f
    return _GZ['rotulo']


def rotulo_alfa(frame=None):
    return 1.0 if rotulo_demo(frame) else 0.0


def _num(x, d=2):
    return ('%%.%df' % d % x).replace('.', ',')


def cabecera_lineas(F=None):
    """v18: la cabecera de la demo (arriba a la derecha), dos lineas: la seccion y el caso,
    y lo que mide FASE1 en vivo donde cuenta (la probabilidad, la escision)."""
    k = _GZ.get('cap')
    if not _GZ.get('activo') or k is None:
        return ''
    demo = demo_activa()
    sec = SECCIONES.get(demo)
    if sec is None:
        return ''
    caps_ = sec['casos']
    if demo == 'genozilla':
        l1 = '%d · %s   ·   %d/%d %s' % (sec['num'], sec['titulo'].upper(), k, len(caps_) - 1, caps_[k]['nombre'])
    elif len(caps_) > 1:
        l1 = '%d · %s   ·   CASO %d/%d · %s' % (sec['num'], sec['titulo'].upper(), k + 1, len(caps_),
                                              caps_[k]['nombre'])
    else:
        l1 = '%d · %s' % (sec['num'], sec['titulo'].upper())
    reg = _GZ.get('reg') or {}
    l2 = ''
    try:
        if _GZ.get('espera') is not None:           # v21
            l2 = '%s: %s' % (ESPERA_TITULO.lower(), _GZ['espera']['que'])
        elif demo == 'probabilidad' and 'p_ahora' in reg:
            ll = reg.get('llueve') or {}
            lt, lc = ll.get('testigo', [0, 0]), ll.get('control', [0, 0])
            l2 = 'testigo  P %s  prenden %d/%d      vacia  P %s  prenden %d/%d' % (
                _num(reg['p_ahora']), lt[1], lt[0], _num(reg.get('p_control', 0.0)), lc[1], lc[0])
        elif demo == 'huella' and k == 1:
            e = reg.get('esc')
            l2 = ('escision: %d conchas con %d personas' % (e['conchas'], e['personas']) if e
                  else 'escision: aun no')
        elif demo in ('huella', 'paseo', 'llena') and F is not None:
            W_ = F.W()
            l2 = 'en la sala %d   inclusiones dejadas %d (vivas %d)   escisiones %d' % (
                len(reg.get('dentro_prev') or ()), reg.get('dej_suma', 0), F.m.n_inclusiones(W_),
                sum(1 for e in W_.get('escisiones', ()) if e['id'] not in reg.get('esc0', ())))
    except Exception:
        l2 = ''
    return l1 + ('\n' + l2 if l2 else '')


def cabecera_texto(frame=None):
    """El Text TOP cabecera_demo: se rehace cada ROTULO_CADA fotogramas."""
    f = absTime.frame
    if _GZ.get('cabecera') is not None and _GZ.get('cab_frame') is not None \
            and 0 <= f - _GZ['cab_frame'] < ROTULO_CADA:
        return _GZ['cabecera']
    _GZ['cabecera'], _GZ['cab_frame'] = cabecera_lineas(fase1()), f
    return _GZ['cabecera']


def cabecera_alfa(frame=None):
    return 1.0 if cabecera_texto(frame) else 0.0


def legend_demo():
    k = _GZ.get('cap')
    demo = demo_activa()
    nombre = 'GENOZILLA' if demo == 'genozilla' else 'DEMO %s' % demo.upper()
    if k is None:
        return '%s  -' % nombre
    caps_ = casos(demo)
    tc = ahora() - _GZ['t0']
    hechos = _GZ.get('resultados') or []
    esp = _GZ.get('espera')
    return '%s  %d/%d %s   %s   comprobados %d/%d' % (
        nombre, k, len(caps_) - 1, caps_[k]['nombre'],
        ('esperando que el mundo evolucione: %s' % esp['que']) if esp is not None
        else 'titulo' if tc < 0 else '%.1f/%.0f s' % (tc, caps_[k]['dur']),
        sum(1 for r in hechos if r[1]), len(hechos))


def arco_segundos(c):
    """Los segundos que tarda en cerrarse el arco de quietud (None: sin arcos). En la
    demo, solo en los capitulos de fila (Tfila) y de estatuas (Tquietud)."""
    if not c.get('arco_quietud'):
        return None
    F = None
    try:
        F = fase1()
    except Exception:
        F = None
    if _GZ.get('activo') and _GZ.get('cap') is not None:
        a = casos()[_GZ['cap']].get('arco')
        if not a:
            return None
        nombre = 'Tquietud' if a == 'estatuas' else 'Tfila'
    else:
        nombre = 'Tfila'
    try:
        v = float(F.par(nombre, 4.0)) if F is not None else 4.0
    except Exception:
        v = 4.0
    return max(0.5, v)


# --- la demo en tiempo simulado (la autoprueba de la sala) ------------------------

MIC_CAPS = (9, 10)          # capitulos en los que el microfono cuenta (estatuas y grito)


def paso_fase1(F, c, t, now, dt, ev, eq=None, mic=False):
    """Lo que FASE1 hace en un paso de dt s con la gente de la sala en t, sin
    TouchDesigner: la imagen de la camara (las cabezas, de las posiciones), el
    seguimiento, las paradas, filas, rescates y armas (sala_mundo), el microfono (con
    mic) y el juego."""
    m = F.m
    c1 = F.cfg()
    W = F.W()
    W['t'] = now
    maximos = []
    for i, x, z, h, _ in personas(c, t, ev):
        xf, yf = a_suelo(c1, x, z)
        if 0.0 <= xf <= c1['ancho_sala'] and 0.0 <= yf <= c1['fondo_sala']:
            maximos.append((xf, yf, h))
    if demo_activa() != 'genozilla' and hasattr(m, 'sala_sim_imagen'):     # v18: la densidad (el sorteo)
        m.sala_bloque(W, c1, m.sala_sim_imagen(c1, maximos), now)
    res = m.tick_personas(W, c1, now, maximos)
    m.sala_mundo(W, c1, now, res)
    if mic and eq is not None:
        n = max(32, int(round(dt * RATE)))
        ta = t - n / float(RATE)
        x = bloque_audio(c, eq, ta, n, RATE, eventos(c, ta - 0.5, t, ev))
        m.mic_bloque(W, c1, x, RATE, now)
    if m.juego_al_dia(W, c1, now) is not None and m.juego_on(W, c1):
        semi = 60.0 / max(1e-6, m.tempo()) / max(1, int(c1['steps_per_beat']))
        m.juego_avanzar(W, c1, now, dt / semi)


def ensayo(c, demo, hasta, fn, dt=0.25):
    """v18: la gente de una demo sin FASE1 (los destinos del suelo: los de celdas no se
    pueden sin ella): el director, de 0 a 'hasta' s, y fn(cfg de la demo) con sus tramos
    (personas(), estado_persona()... valen hasta 'hasta'). Despues, el director como
    estaba: no toca FASE1 ni la pagina Sala."""
    import copy
    viejo = copy.deepcopy(_GZ)
    cc = dict(c, activa=True, demo=DEMOS.index(demo), buclecap=True)
    try:
        _GZ.update(activo=True, acabada=False, tramos={}, demo=demo, resultados=[], sec={}, callado=True,
                   antes_cap={}, saltar=False)
        capitulo(cc, 0.0, None, 0.0, 0)
        t = 0.0
        while t < hasta - 1e-9:
            t = min(hasta, t + dt)
            gz_tick(cc, t, None, t, emular=True)
        return fn(cc)
    finally:
        _GZ.clear()
        _GZ.update(viejo)


def simular_demo(c, F, caps=None, dt=1.0 / 15.0, dt_mic=1.0 / 60.0, t_ini=10000.0, now_ini=None, demo='genozilla',
                 evoluciona=None, espera_max=30.0):
    """Una demo (GENoZilla, si no se dice) en tiempo simulado, caso a caso: el director
    con un reloj a mano (el de la sala y el de FASE1) y FASE1 paso a paso (paso_fase1).
    Entra (guarda la escena), juega los casos y sale (la devuelve). Devuelve
    [(caso, bien, que)], la comprobacion de cada uno. v21: la demo ya no devuelve el
    mundo al salir; esta prueba si (es de la autoprueba: deja FASE1 como estaba). Sin el
    giro del planeta ni sus ciclos, un caso que espera no veria evolucionar el mundo:
    evoluciona(F, demo, caso, que), si se da, hace de el (una vez por caso); como mucho
    espera_max s y el caso queda sin probar."""
    import copy
    W_antes = copy.deepcopy(F.motor.fetch('W', None)) if F is not None else None
    lista = casos(demo)
    caps = list(range(len(lista))) if caps is None else list(caps)
    eq = equipos_o_defecto(c)
    ev = evitar_de(eq)
    t = float(t_ini)
    now = float(now_ini if now_ini is not None else t_ini)
    cc = dict(c, activa=True, demo=DEMOS.index(demo), capitulo=caps[0], buclecap=False)
    _GZ.update(activo=False, acabada=False, resultados=[], callado=True)
    _PIEZAS['clave'] = None
    try:
        gz_tick(cc, t, F, now, emular=True)              # entra (y empieza caps[0])
        for j, k in enumerate(caps):
            if j > 0:
                if demo == 'genozilla':
                    cc['capitulo'] = k                   # el capitulo siguiente, como con Capitulo
                else:
                    cerrar_capitulo(F, now)
                    capitulo(cc, t, F, now, k)
                gz_tick(cc, t, F, now, emular=True)
            mic = demo == 'genozilla' and k in MIC_CAPS
            paso = dt_mic if mic else dt
            t_esp, evolucionado = t, False
            while t + paso < _GZ['t0'] + lista[k]['dur'] - 1e-6:     # v21: t0 se aplaza mientras espera
                if _GZ.get('espera') is not None:
                    if evoluciona is not None and not evolucionado:
                        evolucionado = True
                        evoluciona(F, demo, k, _GZ['espera']['que'])
                    if t - t_esp > espera_max:
                        break
                t += paso
                now += paso
                gz_tick(cc, t, F, now, emular=True)
                paso_fase1(F, cc, t, now, paso, ev, eq, mic)
        cerrar_capitulo(F, now)
    finally:
        salir(F)
        _GZ.update(activo=False, acabada=False, cap=None, callado=False)
        if W_antes is not None:
            F.motor.store('W', W_antes)
            for k_ in ('inst', 'tiles', 'frame'):
                try:
                    F.m._CACHE[k_] = None
                except Exception:
                    pass
    return list(_GZ['resultados'])
