"""
=============================================================================
ESTRATOS - FASE 25: LA HUELLA MINIMA
=============================================================================
Requiere la fase 24. Las personas dejan INCLUSIONES en la celda del planeta
que mira a su casilla: no construyen ni erosionan, pero no pueden pasar sin
dejar algo.

QUE HACE
--------
  LLEGADA      al detectarse una persona nueva (fase 24), deja una inclusion
               con probabilidad Probllegada (0,6). Sin azar de software: el si
               o el no lo decide el mapa logistico sembrado con el id de la
               persona, la celda y el ciclo (la misma sala da el mismo
               resultado). Con Probllegada 1, toda llegada deja huella.
  PARADA       Tparada segundos (3) seguidos con la casilla ocupada (la
               ocupacion binaria de la fase 24) dejan una inclusion segura.
               Una por parada: la casilla se rearma al quedar libre.
  ESCALON      cada inclusion guarda el escalon (la ocupacion) de su celda en
               el instante en que cae; en una celda sin construir, 0. La fase
               26 la borra cuando la erosion baja la celda de ese escalon.
  VARIAS       una lista por celda, con tope de 12 (el exceso quita la mas
               antigua de las de escalon mas alto).
  ASPECTO      plastiglomerado. La matriz es la loseta de la celda, mineral
               mate: en las celdas con inclusiones su tapa baja de rugosidad
               1 a 0,85. Las inclusiones son piezas pequenas medio enterradas
               en el suelo de la celda, alrededor de la formacion, de color
               saturado de la PALETA HUMANA (croma alto sobre los tonos que
               quedan libres: nunca cian, ambar, verde de piso ni azul de rio,
               y sin rojo puro), rugosidad 0,1-0,2 y una dispersion leve
               (familia nueva del shader de la piel: plastico).
  ENTIERRO     al enterrar el mundo las inclusiones se vacian (la fase 27 las
               cuenta y las hornea antes): lo heredado empieza sin ninguna.
  LEYENDA      HUELLA   inclusiones 17 (llegadas 11, paradas 6)   ultima celda
               40 escalon 3 (parada)   llegada 0.6   parada 3 s

OPERADORES (en /project1/FASE1)
-------------------------------
  i_inclusiones, inclusiones
               Script CHOP y Geometry COMP instanciado (una esfera baja de
               poligonos por inclusion, deformada y girada por su semilla),
               con mat_piel_plastico. En el render, tras las coronas.

PROBAR SIN CAMARA
-----------------
  Fuente = simulada. Probllegada 1 y Simponer: aparece una inclusion en la
  celda que mira a la casilla. Probllegada 0 y Simponer: nada; deja la persona
  3 s: aparece una (parada). Mantenla mas: no aparece otra. Simquitar y
  Simponer en la misma casilla: puede salir otra.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase25_huella.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase25 v1  (huella minima: inclusiones por llegada y por parada, con su escalon)'
banner(VERSION)

base = require_base(25)
motor = install_core(base, CARPETA, 25)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase25)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase25')
add_par(base, page, 'float', 'Probllegada', 'Probabilidad de huella al llegar', 0.6, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Tparada', 'Tiempo de parada (s)', 3.0, 0.5, 30.0, clamp=True)
ok('pagina Fase25: Probllegada 0,6 (1: toda llegada deja huella), Tparada 3 s')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

if base.op('mat_piel_plastico') is None:
    fail('mat_piel_plastico: no esta (el shader de la piel es de la fase 12)')
geo = make_instanced(base, 'inclusiones', -880, 2300, 'mat_piel_plastico', sop='sphere')
bola = geo.op('bola')
if bola is not None:                    # pocas caras: son piezas pequenas, y puede haber un millar
    setp_any(bola, ['rows'], 6)
    setp_any(bola, ['cols'], 8)
if not setp_any(geo, ['instancea'], 'a'):
    fail('inclusiones no lee la rugosidad: Instance 2 -> Color A = a')
if has_par(base, 'Materialrespaldo'):
    setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_plastico'")
ok('inclusiones: una pieza por inclusion, con el shader de la piel (familia plastico)')

set_render(base)

leeme(base, 25, """FASE 25 - LA HUELLA MINIMA
  Las personas dejan inclusiones en la celda que mira a su casilla. Llegada:
  con probabilidad Probllegada (mapa logistico: id de la persona, celda y
  ciclo; sin azar). Parada: Tparada s seguidos con la casilla ocupada, una
  segura por parada. Cada una guarda el escalon de su celda al caer. Hasta
  12 por celda. Son piezas pequenas de la paleta humana (plastico), medio
  enterradas en el suelo de la celda; su loseta baja la rugosidad a 0,85.
  Al enterrar se vacian. Geometria inclusiones (i_inclusiones).""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS25 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Nota', 'Velprueba')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS25)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    reloj = [absTime.seconds + 500.0]
    tb = base.op('sala_personas')
    DT = 1.0 / m.CAM_FPS

    def nuevo(prob=0.6):
        m.reset_world()
        m.sala_reset()
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        base.par.Probllegada = prob
        return m.world(), m.cfg()

    def camara(W, c, maximos, n=1):
        """n imagenes con esas cabezas [(x, y, altura)]: personas y lo que dejan."""
        res = None
        for _ in range(n):
            reloj[0] += DT
            res = m.sala_mundo(W, c, reloj[0], m.tick_personas(W, c, reloj[0], maximos))
        return res

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)
    k1 = 4 * cols + 5
    x1, y1 = m.casilla_xy(c, k1)
    aqui = [(x1, y1, 1.7)]
    celda = m.celda_de_casilla(W, c, k1)

    # 1. la llegada
    W, c = nuevo(1.0)
    camara(W, c, aqui, 2)
    uno = (m.n_inclusiones(W), [x[:2] for x in W['incl'][celda]], dict(W['incl_n']))
    W, c = nuevo(0.0)
    camara(W, c, aqui, 2)
    cero = m.n_inclusiones(W)
    t.check('Probllegada 1: toda llegada deja una inclusion en la celda que mira a su casilla; 0: ninguna',
            uno == (1, [[0, m.LLEGADA]], dict(llegadas=1, paradas=0)) and cero == 0, str(uno))
    W, c = nuevo(0.6)

    def tanda():
        return [m.llegada_prende(W, c, j + 1, (7 * j) % m.N) for j in range(1000)]
    a, b = tanda(), tanda()
    frac = sum(a) / 1000.0
    t.check('Probllegada 0,6 sobre 1000 llegadas simuladas: entre 0,55 y 0,65 dejan huella, y la misma sala '
            'da las mismas (sin azar de software)', 0.55 <= frac <= 0.65 and a == b, '%.3f' % frac)
    W['ciclo_n'] += 1
    otro = tanda()
    W['ciclo_n'] -= 1
    t.check('en otro ciclo el reparto es otro (la semilla lleva el ciclo)', otro != a)

    # 2. la parada
    W, c = nuevo(0.0)
    camara(W, c, aqui, 2)               # confirmada: la casilla esta ocupada desde ahora
    n_tp = int(round(c['t_parada'] * m.CAM_FPS))
    camara(W, c, aqui, n_tp - 1)
    antes = m.n_inclusiones(W)
    camara(W, c, aqui, 1)
    justo = (m.n_inclusiones(W), [x[:2] for x in W['incl'][celda]])
    camara(W, c, aqui, 5 * n_tp)
    mas = m.n_inclusiones(W)
    camara(W, c, [], 2)                 # la casilla queda libre: se rearma
    camara(W, c, aqui, 2 + n_tp)
    otra = m.n_inclusiones(W)
    t.check('la parada: a Tparada menos un fotograma no deja nada; a Tparada, una; seguir quieto no deja mas; '
            'tras quedar libre, se rearma',
            antes == 0 and justo == (1, [[0, m.PARADA]]) and mas == 1 and otra == 2
            and W['incl_n'] == dict(llegadas=0, paradas=2), '%d, %d, %d, %d' % (antes, justo[0], mas, otra))
    W, c = nuevo(0.0)
    for k in range(2 + n_tp):           # oscila 10 cm dentro de su casilla
        camara(W, c, [(x1 + (0.05 if k % 2 else -0.05), y1, 1.7)], 1)
    t.check('la parada se mide en la ocupacion binaria: una persona que oscila dentro de su casilla sigue parada',
            m.n_inclusiones(W) == 1 and W['incl'][celda][0][1] == m.PARADA)

    # 3. el escalon
    W, c = nuevo(1.0)
    nota = m.cell_note(celda)
    for _ in range(40):
        if W['occ'][celda] >= 3:
            break
        m.note_on(W, c, m.GEO, nota, 100, reloj[0])
    occ = W['occ'][celda]
    camara(W, c, aqui, 2)
    k2 = k1 + 3 if m.celda_de_casilla(W, c, k1 + 3) != celda else k1 - 4
    vacia = m.celda_de_casilla(W, c, k2)
    x2, y2 = m.casilla_xy(c, k2)
    camara(W, c, aqui + [(x2, y2, 1.7)], 2)
    t.check('la inclusion guarda el escalon (la ocupacion) de su celda al caer; en una celda vacia, 0',
            occ >= 3 and W['incl'][celda][0][0] == occ and W['occ'][vacia] == 0
            and [x[0] for x in W['incl'][vacia]] == [0] and W['incl_ultima']['celda'] == vacia,
            'escalon %d y %s' % (W['incl'][celda][0][0], [x[0] for x in W['incl'][vacia]]))

    # 4. la celda del instante en que se confirma
    W, c = nuevo(1.0)
    cg = dict(c)
    cg['lon_central'] = c['lon_central'] + 120.0
    girada = m.celda_de_casilla(W, cg, k1)
    camara(W, cg, aqui, 2)
    camara(W, c, aqui, 20)              # el planeta sigue girando: la inclusion no se mueve
    t.check('la celda es la que miraba la casilla al confirmarse la persona, no la que mira despues',
            girada != celda and len(W['incl'][girada]) == 1 and not W['incl'][celda])

    # 5. la paleta humana
    tonos = [m.tono_humano(j / 512.0) for j in range(512)]
    prohibido = [h for h in tonos if 55.0 < h < 100.0 or 120.0 < h < 275.0 or 18.0 < h < 40.0]
    cols_h = [m.paleta_humana(c, j / 64.0) for j in range(64)]
    Ls = [m.srgb_l(x) for x in cols_h]
    pads = [m.srgb_l(x) for x in m.COLORES_PADS]
    t.check('la paleta humana: ningun tono en 55-100 (ambar), 120-165 (pisos), 165-235 (cian) ni 235-275 (rios), '
            'ni rojo puro; luminosidad distinta de la de los pads',
            not prohibido and all(abs(l - m.L_HUMANA) < 0.03 for l in Ls)
            and all(abs(m.L_HUMANA - p) > 0.05 for p in pads)
            and all(max(x) - min(x) > 0.25 for x in cols_h), '%d tonos prohibidos' % len(prohibido))

    # 6. varias por celda, con tope
    W, c = nuevo()
    W['occ'][celda] = 2
    for _ in range(4):
        m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    W['occ'][celda] = 5
    for _ in range(m.INCL_CELDA):
        m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    esc = sorted(x[0] for x in W['incl'][celda])
    t.check('varias por celda, hasta 12: el exceso quita la mas antigua de las de escalon mas alto',
            len(esc) == m.INCL_CELDA and esc == [2] * 4 + [5] * 8, str(esc))

    # 7. el dibujo
    out = {}
    filas_i = m.build_inclusiones(W, c, reloj[0], out)
    r0 = m.base_radius(W, c, celda)
    cw, cl = m._cell_sizes(r0, celda)
    n = m.normal_i(celda)

    def lejos(f):
        d = m._norm(f[0:3])
        return math.acos(max(-1.0, min(1.0, sum(a * b for a, b in zip(d, n))))) * r0
    t.check('una instancia por inclusion: pequena (menos del 10 % de la celda), en el suelo de su celda, '
            'alrededor de la formacion, con rugosidad 0,1-0,2 en el canal a',
            len(filas_i) == m.INCL_CELDA and all(len(f) == 13 and 0.10 <= f[12] <= 0.20 for f in filas_i)
            and all(max(f[6:9]) < 0.10 * min(cw, cl) for f in filas_i)
            and all(0.2 * min(cw, cl) < lejos(f) < 0.5 * max(cw, cl) for f in filas_i)
            and len(set(tuple(f[9:12]) for f in filas_i)) > 3,
            '%d filas' % len(filas_i))
    o = base.op('i_inclusiones')
    m._CACHE['inst'] = m.build_instances(W, c, reloj[0])
    o.cook(force=True)
    t.check('i_inclusiones -> inclusiones (mat_piel_plastico), en el render',
            o.numSamples == m.INCL_CELDA and o.numChans == 13 and base.op('inclusiones') is not None
            and 'inclusiones' in str(base.op('render').par.geometry.val).split()
            and base.op('mat_piel_plastico') is not None,
            '%d instancias, %d canales' % (o.numSamples, o.numChans))
    for _ in range(3):
        m.end_cycle(W, c, reloj[0])
        reloj[0] += 1.0
    W['occ'][celda] = 3
    W['dirty'] = True
    def tapas(W, c):
        """La rugosidad de la tapa (la pieza fina) de la columna de la celda."""
        return [f[12] for f in m.build_tiles(W, c, reloj[0])
                if f[7] < 0.03 and sum(a * b for a, b in zip(m._norm(f[0:3]), n)) > 0.999999]
    sin = tapas(W, c)
    m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    con = tapas(W, c)
    t.check('la matriz: en una celda con inclusiones la tapa de su loseta baja de rugosidad 1 a 0,85',
            sin == [m.RUG_TAPA] and con == [m.RUG_TAPA_INCL], '%s -> %s' % (sin, con))
    m.end_cycle(W, c, reloj[0])
    t.check('al enterrar el mundo las inclusiones se vacian', m.n_inclusiones(W) == 0
            and W['incl_n'] == dict(llegadas=0, paradas=0))

    # 8. por la sala simulada, y la leyenda
    W, c = nuevo(1.0)
    base.par.Simcasilla = k1
    m.on_pulse('Simponer')
    c = m.cfg()
    for _ in range(2):
        reloj[0] += DT
        m._SALA['t_img'] = -99.0
        m.sala_tick(W, c, reloj[0])
    leg = m.legend()
    linea = ' '.join(l.strip() for l in leg.splitlines() if 'HUELLA' in l)
    t.check('Probllegada 1 y Simponer: una inclusion en la celda que mira a la casilla; la linea HUELLA',
            len(W['incl'][celda]) == 1 and 'HUELLA   inclusiones 1 (llegadas 1, paradas 0)   ultima celda %d '
            'escalon 0 (llegada)   llegada 1' % celda in leg, linea)


run_test(base, prueba)
print('  Ahora: Fuente = simulada, Probllegada 1 y Simponer: una inclusion en la celda que')
print('  mira a la casilla (leyenda HUELLA). Probllegada 0: solo las paradas de 3 s.')
print('=' * 66)
