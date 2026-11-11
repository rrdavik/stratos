"""
=============================================================================
ESTRATOS - FASE 24: PERSONAS
=============================================================================
Requiere la fase 23. Primera fase del plan v5 ("La huella inevitable").
Convierte la camara de la fase 22 (o su sala simulada) en personas: quien
llega, donde esta y a que celda del planeta mira su casilla. No cambia el
mundo todavia: prepara lo que usan las fases 25 (huellas) y 29 (filas).

QUE HACE (en cada imagen de la camara, 30 por segundo)
------------------------------------------------------
  CABEZAS      sobre la imagen de alturas (alturas_sala, unos 5 cm por pixel):
               un pixel es una cabeza si supera Alturamin, no pasa de
               Alturamax (fase 22) y es el maximo en un radio de
               Separacioncabezas. Dos maximos mas cerca que eso cuentan como
               una persona (se queda el mas alto).
  SEGUIMIENTO  por vecino mas cercano: los maximos se emparejan con las
               personas de la imagen anterior, de la pareja mas cercana a la
               mas lejana, sin pasar de Separacioncabezas. Un maximo sin
               pareja durante Confirmapersona imagenes seguidas (2) es una
               PERSONA NUEVA. Una persona sin maximo desaparece.
  CASILLAS     ocupacion binaria: una casilla esta ocupada si tiene al menos
               una persona. Guarda el instante en que se ocupo (t_ocupada) y
               lo pierde al quedar libre. No pasa por ningun suavizado: los
               tiempos de parada y de fila (fases 25 y 29) se miden aqui. Una
               persona en el borde de dos casillas no cambia hasta pasar 8 cm.
  CELDA        la celda que mira a la casilla, en el instante de cada evento:
               el mapeo de la fase 22 con Loncentral de esa imagen (sigue al
               giro del planeta).
  LEYENDA      PERSONAS 3 en sala   casillas 3/99   nuevas 12   simulada

La densidad suavizada de la fase 22 no cambia y no se usa para nada de esto.

OPERADORES (en /project1/FASE1)
-------------------------------
  alturas_sala la imagen de alturas de la fase 22: la lee el motor.
  personas_chop      Script CHOP: personas, casillas (ocupadas) y nuevas.
  personas           Table DAT: id, x, y, altura, casilla, desde (s), nueva.
  casillas_ocupadas  Table DAT: casilla, ocupada, personas, t_ocupada (s que
               lleva ocupada) y celda (la que mira ahora).

PROBAR SIN CAMARA
-----------------
  Fuente = simulada (fase 22). Simponer: PERSONAS 1, 'nuevas' sube 1 y
  casillas_ocupadas dice que celda mira. Espera media vuelta del planeta y
  pulsa en otra casilla: la celda es otra. Simquitar: PERSONAS 0. Simfila 4 y
  Simformarfila: 4 personas en casillas contiguas desde Simcasilla. Las
  personas simuladas son discos de 1,70 m en la misma imagen que la camara:
  de ahi en adelante todo es igual (maximos, seguimiento, casillas).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase24_personas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase24 v1  (personas: cabezas, seguimiento, casillas ocupadas y la celda que miran)'
banner(VERSION)

base = require_base(24)
motor = install_core(base, CARPETA, 24)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase24)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase24')
add_par(base, page, 'float', 'Separacioncabezas', 'Separacion minima entre cabezas (m)', 0.35, 0.15, 1.0, clamp=True)
add_par(base, page, 'int', 'Confirmapersona', 'Fotogramas para confirmar una persona', 2, 1, 10, clamp=True)
add_par(base, page, 'int', 'Simfila', 'Personas de la fila de prueba', 3, 1, 12, clamp=True)
add_par(base, page, 'pulse', 'Simformarfila', 'Formar una fila')
ok('pagina Fase24: Separacioncabezas 0,35 m, Confirmapersona 2, Simfila 3, Simformarfila')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

PERSONAS_CB = r'''# Script CHOP 'personas_chop' (fase 24): personas en sala, casillas ocupadas y
# llegadas. Las cabezas las saca el motor de alturas_sala (personas_tick).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.personas_cook(scriptOp)
'''

if base.op('alturas_sala') is None:
    fail('alturas_sala: no esta; aplica antes fase22_camara.py')
X0, Y0 = -1320, 1900
cb = get_or_make(base, 'textDAT', 'personas_callbacks', X0, Y0 + 140)
cb.text = PERSONAS_CB
ch = get_or_make(base, 'scriptCHOP', 'personas_chop', X0, Y0)
setp_any(ch, ['callbacks', 'callbackdat', 'dat'], 'personas_callbacks')
for nombre, cab, x in (('personas', m.PERSONAS_COLS, X0 + 220), ('casillas_ocupadas', m.CASILLAS_COLS, X0 + 440)):
    tb = get_or_make(base, 'tableDAT', nombre, x, Y0)
    tb.clear()
    tb.appendRow(list(cab))
m.personas_reset()
ok('alturas_sala -> motor -> personas_chop, personas y casillas_ocupadas')

set_render(base)

leeme(base, 24, """FASE 24 - PERSONAS
  La camara (o la sala simulada), en personas. Cabezas: maximos de altura
  entre Alturamin y Alturamax, separados Separacioncabezas. Seguimiento
  por vecino mas cercano; un maximo sin pareja durante Confirmapersona
  imagenes es una persona nueva. Ocupacion binaria por casilla (t_ocupada)
  y la celda que mira a cada casilla, con el giro de ese instante.
  Tablas personas y casillas_ocupadas; personas_chop. Sin camara: Fuente =
  simulada, Simponer, Simquitar, Simfila y Simformarfila.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS24 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simfila', 'Simcasilla', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS24)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    reloj = [absTime.seconds + 400.0]
    tb = base.op('sala_personas')

    def nuevo():
        m.reset_world()
        m.sala_reset()
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        return m.world(), m.cfg()

    def imagen(W, c, n=1):
        """n imagenes de la camara por la cadena sala_sim -> alturas_sala -> motor."""
        for _ in range(n):
            reloj[0] += 1.0 / m.CAM_FPS
            m._SALA['t_img'] = -99.0
            m.sala_tick(W, c, reloj[0])

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)

    # 1. las cabezas
    def cabezas(personas):
        return m.detectar_cabezas(m.sala_sim_imagen(c, personas), c)
    una = cabezas([[2.0, 2.0, 1.7], [2.30, 2.0, 1.6]])
    dos = cabezas([[2.0, 2.0, 1.7], [2.40, 2.0, 1.6]])
    baja = cabezas([[2.0, 2.0, 0.7]])
    alta = cabezas([[2.0, 2.0, 2.6]])
    t.check('dos cabezas a 0,30 m cuentan una (la mas alta); a 0,40 m, dos',
            len(una) == 1 and abs(una[0][2] - 1.7) < 0.02 and len(dos) == 2
            and abs(dos[0][0] - 2.0) < 0.06 and abs(dos[1][0] - 2.4) < 0.06,
            '%d y %d' % (len(una), len(dos)))
    t.check('una cabeza bajo Alturamin no cuenta; algo por encima de Alturamax, tampoco',
            not baja and not alta)

    # 2. el seguimiento
    W, c = nuevo()
    pistas = []
    ids = []
    for k in range(12):                 # 0,10 m por fotograma
        pistas, nuevas = m.seguir_personas(pistas, [(1.0 + 0.10 * k, 2.0, 1.7)], c, reloj[0] + k / 30.0)
        ids.append(pistas[0]['id'])
    t.check('una persona que se mueve 0,10 m por fotograma sigue siendo la misma',
            len(set(ids)) == 1 and pistas[0]['conf'] and pistas[0]['n'] == 12)
    p1, n1 = m.seguir_personas(pistas, [(2.1, 2.0, 1.7), (3.1, 2.0, 1.7)], c, reloj[0] + 1.0)
    p2, n2 = m.seguir_personas(p1, [(2.1, 2.0, 1.7), (3.1, 2.0, 1.7)], c, reloj[0] + 1.03)
    otra = [p for p in p2 if p['id'] != ids[0]]
    t.check('una que aparece a 1 m de la mas cercana es nueva a los Confirmapersona (2) fotogramas',
            not n1 and len(n2) == 1 and len(otra) == 1 and n2[0]['id'] == otra[0]['id'] and otra[0]['conf'])
    p3, n3 = m.seguir_personas(p2, [(2.1, 2.0, 1.7), (3.1, 2.0, 1.7), (4.5, 1.0, 1.7)], c, reloj[0] + 1.06)
    p4, n4 = m.seguir_personas(p3, [(2.1, 2.0, 1.7), (3.1, 2.0, 1.7)], c, reloj[0] + 1.1)
    p5, n5 = m.seguir_personas(p4, [(2.1, 2.0, 1.7)], c, reloj[0] + 1.13)
    t.check('un maximo de un solo fotograma no es una persona; una persona sin maximo desaparece',
            not n3 and not n4 and len(p4) == 2 and len(p5) == 1 and p5[0]['id'] == ids[0])

    # 3. la ocupacion binaria, sin suavizado, y por la imagen de la sala
    W, c = nuevo()
    k1 = 2 * cols + 3
    base.par.Simcasilla = k1
    m.on_pulse('Simponer')
    c = m.cfg()
    imagen(W, c, 1)
    antes = (len(m.personas_en_sala()), dict(m._SALA['casillas']))
    imagen(W, c, 1)
    cas = m._SALA['casillas']
    tp = base.op('personas')
    tc = base.op('casillas_ocupadas')
    t.check('Simponer llega por la imagen de la sala: a los Confirmapersona (2) fotogramas hay una persona, '
            'su casilla esta ocupada y las tablas lo dicen (sin ningun suavizado)',
            antes == (0, {}) and len(m.personas_en_sala()) == 1 and list(cas) == [k1] and m._SALA['nuevas'] == 1
            and tp.numRows == 2 and int(tp[1, 4].val) == k1 and tc.numRows == 2 and int(tc[1, 0].val) == k1
            and int(tc[1, 4].val) == m.celda_de_casilla(W, c, k1) and tb.numRows == 2,
            'casillas %s, nuevas %d' % (list(cas), m._SALA['nuevas']))
    base.par.Confirmapersona = 1
    W, c = nuevo()
    m.on_pulse('Simponer')
    c = m.cfg()
    imagen(W, c, 1)
    t.check('con Confirmapersona 1 la persona que entra se ve en el mismo fotograma',
            len(m.personas_en_sala()) == 1 and list(m._SALA['casillas']) == [k1])
    base.par.Confirmapersona = 2
    c = m.cfg()
    t0 = m._SALA['casillas'][k1]['t_ocupada']
    imagen(W, c, 30)
    sigue = m._SALA['casillas'][k1]['t_ocupada'] == t0
    m.on_pulse('Simquitar')
    imagen(W, c, 1)
    libre = not m._SALA['casillas'] and not m.personas_en_sala()
    m.on_pulse('Simponer')
    imagen(W, c, 2)
    t.check('la casilla guarda cuando se ocupo y lo pierde al quedar libre (Simquitar: PERSONAS 0); '
            'al volver a ocuparse, empieza de nuevo',
            sigue and libre and m._SALA['casillas'][k1]['t_ocupada'] > t0 + 0.9)
    # una persona que oscila en el borde de dos casillas no cambia de casilla
    xb = (k1 % cols + 1) * c['ancho_sala'] / cols                 # el borde derecho de la casilla
    yb = (k1 // cols + 0.5) * c['fondo_sala'] / filas
    pistas, _ = m.seguir_personas([], [(xb - 0.10, yb, 1.7)], c, reloj[0])
    cas_b = []
    for k in range(8):
        pistas, _ = m.seguir_personas(pistas, [(xb + (0.05 if k % 2 else -0.05), yb, 1.7)], c, reloj[0])
        cas_b.append(pistas[0]['casilla'])
    pistas, _ = m.seguir_personas(pistas, [(xb + 0.2, yb, 1.7)], c, reloj[0])
    t.check('una persona que oscila en el borde de dos casillas no cambia de casilla (8 cm de histeresis); '
            'al cruzar, si',
            set(cas_b) == {k1} and pistas[0]['casilla'] == k1 + 1)

    # 4. la celda de una casilla sigue al giro
    c = m.cfg()
    a = m.celda_de_casilla(W, c, k1)
    cg = dict(c)
    cg['lon_central'] = c['lon_central'] + 120.0
    b = m.celda_de_casilla(W, cg, k1)
    W, c = nuevo()
    m.on_pulse('Simponer')
    cg = dict(m.cfg())
    cg['lon_central'] += 120.0
    res = None
    for _ in range(2):
        reloj[0] += 1.0 / m.CAM_FPS
        res = m.tick_personas(W, cg, reloj[0], m.detectar_cabezas(m.sala_sim_imagen(cg, m.sala_personas()), cg))
    t.check('la celda de una casilla sigue a Loncentral: con el planeta girado, la misma casilla mira a otra '
            'celda, y la llegada lleva la celda de ese instante',
            a != b and res['nuevas'] and res['nuevas'][0]['celda'] == b and res['nuevas'][0]['casilla'] == k1,
            'celda %d y, girado 120 grados, %d' % (a, b))

    # 5. la fila de prueba
    W, c = nuevo()
    base.par.Simcasilla = 4 * cols + 2
    base.par.Simfila = 4
    m.on_pulse('Simformarfila')
    c = m.cfg()
    imagen(W, c, 2)
    cas = sorted(m._SALA['casillas'])
    t.check('Simfila 4 y Simformarfila: 4 personas en casillas contiguas, por la imagen de la sala',
            cas == [4 * cols + 2 + k for k in range(4)] and len(m.personas_en_sala()) == 4
            and m._SALA['nuevas'] == 4 and tb.numRows == 5, str(cas))
    zig = m.casillas_fila_sim(c, cols - 2, 5)
    t.check('la fila de prueba dobla al llegar a la pared: sigue por la casilla de debajo',
            zig == [cols - 2, cols - 1, 2 * cols - 1, 2 * cols - 2, 2 * cols - 3], str(zig))
    leg = m.legend()
    t.check('leyenda PERSONAS', 'PERSONAS 4 en sala   casillas 4/99   nuevas 4   simulada' in leg,
            ' '.join(l.strip() for l in leg.splitlines() if 'PERSONAS' in l))
    o = base.op('personas_chop')
    o.cook(force=True)
    t.check('personas_chop: personas, casillas y nuevas',
            o.numChans == 3 and [float(ch[0]) for ch in o.chans] == [4.0, 4.0, 4.0])
    m.on_pulse('Simvaciar')
    imagen(W, c, 1)
    t.check('Simvaciar: nadie en la sala', not m.personas_en_sala() and not m._SALA['casillas']
            and base.op('personas').numRows == 1 and base.op('casillas_ocupadas').numRows == 1)


run_test(base, prueba)
print('  Ahora: Fuente = simulada, Simcasilla y Simponer: PERSONAS 1 y la tabla')
print('  casillas_ocupadas dice que celda mira. Simfila 4 y Simformarfila: una fila.')
print('=' * 66)
