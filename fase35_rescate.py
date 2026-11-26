"""
=============================================================================
ESTRATOS - FASE 35: RESCATAR BROTES
=============================================================================
Requiere la fase 34. Tres personas coordinadas convierten un brote del mal
en una celda del publico.

QUE HACE
--------
  CONDICION    una persona en la celda del mal (la que mira su casilla) y
               Aliados personas o mas en sus celdas vecinas (pueden compartir
               celda), todas sostenidas Taliados segundos sobre la ocupacion
               binaria de la fase 24. Las casillas de esas personas quedan fijas
               al empezar (con el planeta girando, la celda que mira cada una
               cambia): lo que se sostiene es su ocupacion.
  EFECTO       la celda pasa a la especie del ultimo secuenciador que la toco
               (geologia o arquitectura; si ninguno, geologia): conserva su
               ocupacion y su carga y sigue con las reglas y el ritmo de
               construccion de siempre. Sus satelites del mal, con ella. El
               monstruo puede volver a elegirla.
  MIENTRAS     hasta completarse, la persona de encima alimenta el mal con las
               reglas normales (fase 22). Si alguien se va antes de Taliados, el
               rescate empieza de cero.
  ULTIMO SEQ   se apunta en cada nota del SEQ1 (geo) o del SEQ2 (arq) que prende
               en una celda.
  LEYENDA      RESCATE  celda 33   aliados 2/2   2.1/3.0 s

PROBAR
------
  Modojuego; un brote crecido a 3 en la celda de Simcasilla; Simrescate: a los
  3 s la celda es del publico, con ocupacion 3 y la especie del ultimo
  secuenciador. Quitar un aliado a los 2 s: no hay rescate y el contador vuelve
  a cero.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase35_rescate.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase35 v2  (el devorador: rescatar brotes del mal entre tres)'
banner(VERSION)

base = require_base(35)
motor = install_core(base, CARPETA, 35)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase35)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase35')
add_par(base, page, 'int', 'Aliados', 'Aliados del rescate', 2, 1, 6, clamp=True)
add_par(base, page, 'float', 'Taliados', 'Tiempo del rescate (s)', 3.0, 0.5, 20.0, clamp=True)
add_par(base, page, 'pulse', 'Simrescate', 'Simular rescate')
# v2: el rescate pide 2 aliados (antes 3). Un proyecto que seguia en 3 pasa a 2 una sola vez;
# un valor puesto a mano se respeta
renew_default(base, 'Aliados', 3, 2)
ok('parametros de la fase 35: Aliados 2, Taliados 3 s, Simrescate')

set_render(base)

leeme(base, 35, """FASE 35 - RESCATAR BROTES
  Una persona en un brote del mal y Aliados en sus celdas vecinas, todas
  Taliados s sobre la ocupacion binaria: la celda pasa a la especie del
  ultimo secuenciador que la toco (geologia si ninguno), con su ocupacion y
  su carga, y sigue creciendo al ritmo de siempre. Si alguien se va antes,
  vuelve a cero. Mientras, la persona de encima alimenta el mal (fase 22).
  Simrescate: una persona en la celda de Simcasilla y Aliados en vecinas.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS35 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Simbalance', 'Colapsoon', 'Temaenciclo', 'Modojuego', 'Umbralaparicion',
          'Aliados', 'Taliados')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS35)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0
    base.par.Tfila = 60.0                   # sin zanjas de las personas del rescate
    S = SalaJuego(base, m, absTime.seconds + 2100.0)
    W, c = S.nuevo(4)
    cols, filas = m.rejilla_sala(c)
    k0 = 4 * cols + 5
    c0 = m.celda_de_casilla(W, c, k0)
    al = m.casillas_hacia(W, c, m.NEIGH[c0], evitar=[k0])[:int(c['aliados'])]
    TA = c['t_aliados']

    def brote(W, occ=3, carga=1):
        W['occ'][c0], W['carga'][c0] = occ, carga
        W['sp'][c0], W['own'][c0], W['par'][c0] = m.MAL, m.GEO, -1
        W['traza'][c0] = 1

    # 1. 1 + Aliados durante Taliados; con un aliado menos, o un instante menos, nada
    brote(W)
    W['juego']['ultimoseq'][c0] = 'arq'
    S.camara(W, c, [k0] + al[:-1], seg=TA + 0.5)
    menos = W['sp'][c0]
    S.camara(W, c, [], n=2)
    S.camara(W, c, [k0] + al, seg=TA - 0.4)
    antes = (W['sp'][c0], c0 in W['juego']['rescates'])
    leg = m._legend_rescate(W, c)
    S.camara(W, c, [k0] + al, seg=0.6)
    t.check('rescate con 1 + Aliados (2) sostenidos Taliados s; con un aliado menos, o un instante menos, nada',
            len(al) == int(c['aliados']) and menos == m.MAL and antes == (m.MAL, True) and W['sp'][c0] == m.ARQ,
            'aliados en %s' % al)
    t.check('la especie es la del ultimo secuenciador (arq); se conservan ocupacion y carga; own, la nueva',
            W['occ'][c0] == 3 and W['carga'][c0] == 1 and W['own'][c0] == m.ARQ and W['juego']['rescatados'] == 1)
    t.check('la linea RESCATE: celda, aliados y tiempo', leg.startswith('  RESCATE  celda %d   aliados %d/%d   ' % (c0, len(al), len(al)))
            and leg.endswith('/%.1f s' % TA), leg.strip())

    # 2. si alguien se va antes, vuelve a cero; sin ultimo secuenciador, geologia
    W, c = S.nuevo(4)
    brote(W)
    S.camara(W, c, [k0] + al, seg=TA - 1.0)
    S.camara(W, c, [k0] + al[:-1], n=3)
    reinicio = c0 not in W['juego']['rescates']
    S.camara(W, c, [k0] + al, seg=TA - 0.4)
    sigue = W['sp'][c0]
    S.camara(W, c, [k0] + al, seg=0.6)
    t.check('si alguien se va antes de Taliados el rescate se reinicia; sin ultimo secuenciador, geologia',
            reinicio and sigue == m.MAL and W['sp'][c0] == m.GEO)

    # 3. tras el rescate crece al ritmo normal y el monstruo puede volver a elegirla
    o0 = W['occ'][c0]
    for _ in range(int(c['cost_max']) * 2):
        m.note_on(W, c, m.GEO, m.cell_note(c0), 100, S.now)
    S.camara(W, c, [], n=2)
    mo = m.aparecer(W, c, S.now, m.NEIGH[c0][0])
    t.check('tras el rescate la celda crece con las reglas de siempre (del publico) y el monstruo puede volver '
            'a elegirla', W['occ'][c0] > o0 and W['sp'][c0] == m.GEO and mo['objetivo'] == c0,
            'occ %d -> %d' % (o0, W['occ'][c0]))

    # 4. el ultimo secuenciador, nota a nota
    x = m.NEIGH[c0][1]
    m.note_on(W, c, m.ARQ, m.cell_note(x), 90, S.now)
    a1 = W['juego']['ultimoseq'].get(x)
    m.note_on(W, c, m.GEO, m.cell_note(x), 90, S.now)
    t.check('ultimoseq: la nota del SEQ2 apunta arq; la del SEQ1, geo', a1 == 'arq'
            and W['juego']['ultimoseq'].get(x) == 'geo')

    # 5. Simrescate
    W, c = S.nuevo(4)
    brote(W)
    base.par.Simcasilla = k0
    m.on_pulse('Simrescate')
    W = m.world()
    c = m.cfg()
    puestas = [m.casilla_de_xy(c, p[0], p[1]) for p in m.sala_personas()]
    S.camara(W, c, puestas, seg=TA + 0.3)
    t.check('Simrescate: una persona en la casilla de Simcasilla y Aliados en vecinas: a los Taliados s, rescatada',
            len(puestas) == 1 + int(c['aliados']) and puestas[0] == k0 and W['sp'][c0] == m.GEO,
            'casillas %s' % puestas)


run_test(base, prueba)
print('  Ahora: Modojuego, un brote crecido a 3 en la celda de Simcasilla y Simrescate: a los 3 s es')
print('  del publico.')
print('=' * 66)
