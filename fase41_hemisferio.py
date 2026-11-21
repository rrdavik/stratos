"""
=============================================================================
ESTRATOS - FASE 41: HEMISFERIO, LA REJA FIJA EN LA CARA VISIBLE
=============================================================================
Requiere la fase 40 (motor v137). Con Hemisferio, las notas, las personas y los monstruos
juegan sobre una reja de celdas que no gira, como la camara y la sala, y la superficie del
planeta, que gira como siempre, pasa por debajo y va encajando en ella. Los monstruos ya no
se pierden: si la rotacion los lleva a la cara oculta se quedan parados hasta que vuelven a
la visible. Sin Hemisferio (de fabrica), todo igual que en la fase 40.

QUE HACE
--------
  SUPERFICIE   Con Hemisferio, el doble de celdas (24 por anillo completo, 15 grados cada una;
               unas 2N - 2 en total, con N las notas del rango). Los anillos pares y los
               impares van desplazados media celda. Gira como siempre (giro vivo).
  REJA         Una nota del rango cae en una celda de la reja de vista, que no gira y cubre
               solo la cara visible (Anchoangular alrededor de Loncentral): la clase de nota
               es la columna (12 por anillo), la octava el anillo y los polos, arriba y abajo.
               De ahi, en la celda de la superficie que esta debajo del centro de esa celda
               en ese instante (Loncentral sigue al giro). Cada 15 grados de giro, la
               superficie encaja otra vez con la reja. Las personas ya iban asi.
  MONSTRUOS    Circulan por la superficie como siempre y aparecen por el borde de entrada
               del giro. Si la rotacion los lleva a la cara oculta, se quedan parados (ni
               andan, ni devoran, ni luchan) hasta que reaparecen en la visible.
  PULSACIONES  El objetivo de los dos pasa a occ x (1 + Pesopulso x calor) / (1 + coste). El
               calor es 1 si sono un secuenciador en la celda o en una vecina en este paso y
               baja a 0 en Ventanapulso pasos de juego (t_gate). Sin pulsaciones recientes
               (o con Pesopulso 0), la regla de siempre: occ / (1 + coste).
  CAMBIO       Cambiar Hemisferio vacia el mundo (otra reticula), como cambiar el rango.

PARAMETROS (pagina Fase41)
--------------------------
  Hemisferio (apagado), Pesopulso 1,0, Ventanapulso 8.
  Leyenda:  HEMISFERIO  celdas 168   cara visible 85/168   objetivo con pulso (calor 0.75)

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase41_hemisferio.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase41 v2  (Hemisferio: reja fija en la cara visible sobre la superficie que gira; los monstruos paran en la cara oculta y van a las pulsaciones)'
banner(VERSION)

base = require_base(41)
motor = install_core(base, CARPETA, 41)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase41)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase41')
add_par(base, page, 'toggle', 'Hemisferio', 'Hemisferio (el juego solo en la cara visible)', False)
add_par(base, page, 'float', 'Pesopulso', 'Peso de las pulsaciones en el objetivo (0 = sin ellas)', 1.0, 0.0, 10.0,
        clamp=True)
add_par(base, page, 'int', 'Ventanapulso', 'Pasos que cuenta una pulsacion', 8, 1, 64, clamp=True)
ok('pagina Fase41: Hemisferio (apagado), Pesopulso 1, Ventanapulso 8')

set_render(base)

leeme(base, 41, """FASE 41 - HEMISFERIO, LA REJA FIJA EN LA CARA VISIBLE
  Con Hemisferio la superficie del planeta tiene el doble de celdas (24 por anillo, 15
  grados) y gira como siempre. Las notas caen en una reja de vista que no gira y cubre solo
  la cara visible; de ella, en la celda de la superficie que esta debajo en ese instante
  (cada 15 grados de giro encajan). Los monstruos andan por la superficie como siempre y, si
  acaban en la cara oculta, se quedan parados hasta que reaparecen en la visible; los dos
  buscan donde suenan los secuenciadores: occ x (1 + Pesopulso x calor) / (1 + coste), el calor
  baja a 0 en Ventanapulso pasos (8). Cambiar Hemisferio vacia el mundo.
  Sin Hemisferio, todo igual que en la fase 40.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS41 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Spritemonstruo', 'Emocion', 'Godzilla', 'Godzillasala', 'Tvacia', 'Malgodzilla', 'Pasoslucha',
          'Tregua', 'Simceldamon', 'Tema', 'Oceano', 'Montierra', 'Hemisferio', 'Pesopulso', 'Ventanapulso',
          'Anchoangular', 'Fuerarango')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS41)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)
        base.par.Hemisferio = False
        m.reset_world()                 # la esfera de siempre y el mundo vacio


def _poner(m, W, i, occ, s=None):
    s = m.GEO if s is None else s
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = s
    W['traza'][i] = 1
    W['h'][i] = m.height_for(m.cfg(), occ)


def _mal(m, W, c, i, occ, now):
    m.brote_mal(W, c, i, now)
    W['occ'][i] = occ


def _conexo(m):
    seen, pila = {0}, [0]
    while pila:
        u = pila.pop()
        for v in m.NEIGH[u]:
            if v not in seen:
                seen.add(v)
                pila.append(v)
    return len(seen) == m.N


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # Trumpzilla no aparece solo (salvo donde se pide)
    base.par.Spritemonstruo = True
    base.par.Emocion = 'auto'
    base.par.Anchoangular = 180.0
    base.par.Fuerarango = 'plegar'
    for nm, v in (('Godzillasala', 'vacia'), ('Tvacia', 0.0), ('Malgodzilla', 1), ('Pasoslucha', 8),
                  ('Tregua', 16), ('Pesopulso', 1.0), ('Ventanapulso', 8)):
        setattr(base.par, nm, v)
    S = SalaJuego(base, m, absTime.seconds + 7100.0, godzilla=True)
    lon = lambda i: m.lonlat_celda(i)[1]
    dlon = lambda a, b: (a - b + 180.0) % 360.0 - 180.0

    # 1. la superficie: sin Hemisferio la esfera de siempre; con el, el doble de celdas (15 grados)
    base.par.Hemisferio = False
    m.sync_grid()
    N0 = m.N
    esfera = (copy.deepcopy(m.NORMALS), copy.deepcopy(m.NEIGH), list(m.SIZE_EW), list(m.SIZE_NS), m.grid_key(),
              copy.deepcopy(m.RINGS))
    base.par.Hemisferio = True
    m.sync_grid()
    c = m.cfg()
    notas = m.GRID['hi'] - m.GRID['lo'] + 1
    anillos = [len(r) for r in m.RINGS]
    completo = [r for r in m.RINGS if len(r) == 24][0]
    paso = sorted(lon(k) for k in completo)
    sim = all(i in m.NEIGH[j] for i in range(m.N) for j in m.NEIGH[i])
    seen, pila = {0}, [0]
    while pila:
        u = pila.pop()
        for v in m.NEIGH[u]:
            if v not in seen:
                seen.add(v)
                pila.append(v)
    t.check('Hemisferio: la superficie tiene el doble de celdas (%d en vez de %d; %d notas), 24 por anillo completo '
            'a 15 grados, polos en los extremos, vecindad simetrica y conexa; la grid_key lo dice' % (m.N, N0, notas),
            m.hemisferio() and m.N == 2 + 2 * sum(len(r) for r in esfera[5]) and m.POLE_N == m.N - 1
            and anillos.count(24) == 6 and abs(paso[1] - paso[0] - 15.0) < 1e-6 and sim and len(seen) == m.N
            and len(m.NEIGH[m.POLE_S]) == len(m.RINGS[0]) and m.grid_key() == [m.GRID['lo'], m.GRID['hi'], 'hemi']
            and len(m.VISTA) == notas, 'N %d, anillos %s' % (m.N, anillos))
    base.par.Hemisferio = False
    m.sync_grid()
    t.check('sin Hemisferio la reticula es la esfera de antes: mismas normales, vecinas y tamanos; cell_note y note_cell '
            'son la identidad con el rango', not m.hemisferio() and m.NORMALS == esfera[0] and m.NEIGH == esfera[1]
            and m.SIZE_EW == esfera[2] and m.SIZE_NS == esfera[3] and m.grid_key() == esfera[4] and m.N == N0
            and m.note_cell(m.cell_note(7)) == 7, 'N %d' % m.N)
    base.par.Hemisferio = True
    m.sync_grid()

    # 2. la reja fija: la nota cae siempre en la misma posicion de la vista, la superficie cambia debajo
    c0 = dict(m.cfg(), lon_central=0.0)
    cols, filas_c = m.rejilla_sala(c0)
    ring = [k for k in range(m.GRID['lo'] + 1, m.GRID['hi']) if (k // 12) == (60 // 12)]        # un anillo completo
    ring = sorted(ring, key=lambda k: k % 12)
    nota_u = {}
    fija = True
    for L in (0.0, 15.0, 37.0, 90.0, -120.0, 179.0):
        cL = dict(c0, lon_central=L)
        celdas = [m.note_cell(n, cL) for n in ring]
        cas = [m.casilla_de_celda(cL, x) for x in celdas]
        us = [(x % cols) for x in cas if x is not None]
        # la columna de la sala de cada nota: creciente con la clase de nota, igual para cualquier giro
        nota_u[L] = us
        fija = fija and None not in cas and us == sorted(us) and len(set(celdas)) == 12
    columnas = sorted(set(tuple(v) for v in nota_u.values()))
    ok_desfase = all(abs(dlon(lon(m.note_cell(n, dict(c0, lon_central=L))) - L, 0.0)) <= 90.0 for n in ring
                     for L in (0.0, 37.0, -120.0))
    t.check('la reja no gira: con Loncentral 0, 15, 37, 90, -120 y 179 las 12 notas de un anillo caen en 12 celdas '
            'distintas, todas a la vista y en el mismo orden de izquierda a derecha, en las mismas columnas de la sala '
            '(salvo el redondeo de media celda)',
            fija and ok_desfase and all(max(abs(a - b) for a, b in zip(v, columnas[0])) <= cols * 0.1
                                        for v in columnas), 'columnas %s' % columnas[:2])
    cA, cB = dict(c0, lon_central=0.0), dict(c0, lon_central=15.0)
    a_ = m.note_cell(64, cA)
    b_ = m.note_cell(64, cB)
    t.check('al girar 15 grados, la superficie encaja otra vez: la nota 64 cae en la celda contigua del mismo anillo, '
            'una celda mas tarde (la %d, la %d)' % (a_, b_),
            a_ != b_ and b_ in m.NEIGH[a_] and m.RING_OF[a_] == m.RING_OF[b_]
            and abs(dlon(lon(b_), lon(a_)) - 15.0) < 1e-6, '%d %d %.1f' % (a_, b_, dlon(lon(b_), lon(a_))))

    # 3. el mundo: una nota MIDI construye en la celda de superficie que hay debajo; cell_note vuelve a la celda
    W, c = S.nuevo(0, juego=False)
    c = dict(m.cfg(), lon_central=0.0)
    r1 = m.note_on(W, c, m.GEO, 64, 100, S.now)
    i1 = r1['celda']
    m.note_off(W, c, m.GEO, 64, S.now + 0.05, 120.0)
    c2 = dict(c, lon_central=60.0)
    r2 = m.note_on(W, c2, m.GEO, 64, 100, S.now + 1.0)
    i2 = r2['celda']
    m.note_off(W, c2, m.GEO, 64, S.now + 1.05, 120.0)
    fuera = [n for n in range(128) if m.note_cell(n, c2) is None or not (0 <= m.note_cell(n, c2) < m.N)
             or (not m.is_pole(m.note_cell(n, c2)) and m.casilla_de_celda(c2, m.note_cell(n, c2)) is None)]
    t.check('una nota MIDI (la 64) construye en una celda; tras girar 60 grados, la misma nota construye en otra: la '
            'superficie de debajo; las 128 notas caen a la vista; cell_note(x) lleva a la celda x (%d, %d)' % (i1, i2),
            i1 == m.note_cell(64, c) and i2 == m.note_cell(64, c2) and i1 != i2 and W['occ'][i1] > 0 and W['occ'][i2] > 0
            and not fuera and all(m.note_cell(m.cell_note(x)) == x for x in range(m.N)),
            'notas fuera %s' % fuera[:4])

    # 4. los monstruos: circulan por la superficie; en la cara oculta se quedan parados hasta que reaparecen
    base.par.Godzillasala = 'siempre'
    W, c = S.nuevo(4)
    c['lon_central'] = 0.0
    vis0 = [x for x in range(m.N) if m.casilla_de_celda(c, x) is not None]
    a = min(vis0, key=lambda x: (abs(lon(x)) + abs(m.lonlat_celda(x)[0]), x))
    dist, _ = m.dijkstra_mon(W, c, a)
    presa = min(x for x in dist if abs(dist[x] - 3.0) < 1e-9)
    _poner(m, W, presa, 6)
    mo = m.aparecer(W, c, S.now, a)
    c['lon_central'] = lon(a) + 180.0       # la superficie gira: su celda queda en la cara oculta
    oculto = m.en_oscuridad(c, mo)
    n0 = (mo['celda'], W['occ'][presa], mo['acum'])
    S.pasos(W, c, 40)
    quieto = (mo['celda'], W['occ'][presa], mo['acum']) == n0 and mo['mov'] == 0.0
    c['lon_central'] = lon(a)               # reaparece en la cara visible
    visible = not m.en_oscuridad(c, mo)
    S.pasos(W, c, 40)
    anda = mo['celda'] != a or W['occ'][presa] < 6
    t.check('Trumpzilla en la cara oculta (Loncentral a 180 grados de su celda) se queda parado 40 pasos sin andar '
            'ni devorar; al volver a la cara visible, anda y devora',
            oculto and quieto and visible and anda, 'oculto %s quieto %s visible %s anda %s (celda %d -> %d, occ %d)'
            % (oculto, quieto, visible, anda, a, mo['celda'], W['occ'][presa]))
    W, c = S.nuevo(4)
    c['lon_central'] = 0.0
    _mal(m, W, c, presa, 3, S.now)
    g = m.aparecer_godzilla(W, c, S.now, a)
    c['lon_central'] = lon(a) + 180.0
    n0 = (g['celda'], W['occ'][presa], g['acum'])
    S.pasos(W, c, 40)
    quieto = (g['celda'], W['occ'][presa], g['acum']) == n0 and m.en_oscuridad(c, g)
    c['lon_central'] = lon(a)
    S.pasos(W, c, 40)
    t.check('Godzilla igual: parado en la cara oculta; al volver a la visible, anda y devora el mal',
            quieto and (g['celda'] != a or W['occ'][presa] < 3 or W['sp'][presa] != m.MAL),
            'quieto %s, celda %d -> %d' % (quieto, a, g['celda']))
    W, c = S.nuevo(4)
    c['lon_central'] = 0.0
    junto = m.NEIGH[a][0]
    mo = m.aparecer(W, c, S.now, a)
    g = m.aparecer_godzilla(W, c, S.now, junto)
    c['lon_central'] = lon(a) + 180.0
    sin = not m.encuentro(W, c, S.now) and W['juego'].get('lucha') is None
    c['lon_central'] = lon(a)
    con = m.encuentro(W, c, S.now)
    t.check('en celdas contiguas pero en la cara oculta no luchan; a la vista, si', sin and con, '%s %s' % (sin, con))
    base.par.Godzillasala = 'vacia'

    # 5. aparecen en la cara visible, por el borde de entrada del giro
    W, c = S.nuevo(4)
    c['lon_central'] = 0.0
    c1 = m.celda_aparicion(W, c)
    t.check('Trumpzilla aparece en una celda de la cara visible (la %d, longitud %.1f)' % (c1, lon(c1)),
            c1 is not None and m.casilla_de_celda(c, c1) is not None, '%s' % c1)

    # 6. las pulsaciones: van a donde suena un secuenciador
    W, c = S.nuevo(4)
    a = min(range(m.N), key=lambda i: (abs(lon(i)) + abs(m.lonlat_celda(i)[0]), i))
    dist, _ = m.dijkstra_mon(W, c, a)
    dos = sorted(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    lejanas = []                            # cuatro celdas a 2 pasos que no se tocan ni comparten vecinas
    for q in dos:
        if all(q != r and q not in m.NEIGH[r] and not (set(m.NEIGH[q]) & set(m.NEIGH[r])) for r in lejanas):
            lejanas.append(q)
    x, y, xm, ym = (lejanas + [None] * 4)[:4]
    W['t'], W['paso'] = S.now, S.SEMI
    c = dict(m.cfg(), t_vacia=0.0)

    def objetivos(cfg_):
        mo = m.aparecer(W, cfg_, S.now, a)
        g = m.aparecer_godzilla(W, cfg_, S.now, a)
        return mo['objetivo'], g['objetivo']
    _poner(m, W, x, 4)
    _poner(m, W, y, 5)                      # y es mas prospera
    _mal(m, W, c, xm, 4, S.now)
    _mal(m, W, c, ym, 5, S.now)
    W['juego']['zanjas'].clear()
    W['t_gate'][:] = [-99.0] * m.N
    callado = objetivos(c)
    W['t_gate'][x] = W['t_gate'][xm] = S.now        # suena un secuenciador en x y en xm
    pulso = objetivos(c)
    cero = objetivos(dict(c, peso_pulso=0.0))
    W['t_gate'][x] = W['t_gate'][xm] = S.now - 4.5  # hace mas que la ventana (8 pasos x 4 x 0,125 s = 4 s)
    viejo = objetivos(c)
    vx = [v for v in m.NEIGH[x] if v not in (a, xm, ym, y)][0]
    vm = [v for v in m.NEIGH[xm] if v not in (a, x, y, ym)][0]
    W['t_gate'][x] = W['t_gate'][xm] = -99.0
    W['t_gate'][vx] = W['t_gate'][vm] = S.now        # suena en una vecina
    de_vecina = objetivos(c)
    t.check('Trumpzilla: sin pulsaciones (o pasada la ventana, o con Pesopulso 0) elige la de mayor occ / (1 + coste), '
            'la %d (occ 5); con un secuenciador sonando en la %d (occ 4), o en su vecina, va a esa' % (y, x),
            callado[0] == y and cero[0] == y and viejo[0] == y and pulso[0] == x and de_vecina[0] == x
            and m.calor_pulso(W, c) is not None,
            'callado %s, pulso %s, Pesopulso 0 %s, viejo %s, vecina %s' % (callado, pulso, cero, viejo, de_vecina))
    t.check('Godzilla igual con el mal: sin pulsaciones (o con Pesopulso 0, o pasada la ventana) a la mas prospera '
            '(la %d); con un secuenciador sonando en la %d, o en su vecina, a esa' % (ym, xm),
            callado[1] == ym and cero[1] == ym and viejo[1] == ym and pulso[1] == xm and de_vecina[1] == xm,
            'callado %s, pulso %s, Pesopulso 0 %s, viejo %s, vecina %s' % (callado, pulso, cero, viejo, de_vecina))

    # 7. la leyenda
    W, c = S.nuevo(4)
    c['lon_central'] = 0.0
    a = [x for x in vis0 if not m.is_pole(x)][0]
    m.aparecer(W, c, S.now, a)
    c['lon_central'] = lon(a) + 180.0
    leg = m._legend_hemisferio(W, c)
    base.par.Hemisferio = False
    m.sync_grid()
    leg_off = m._legend_hemisferio(W, m.cfg())
    base.par.Hemisferio = True
    m.sync_grid()
    t.check('la leyenda dice HEMISFERIO, las celdas, cuantas se ven y quien esta en la cara oculta; apagado, '
            'HEMISFERIO apagado', leg.strip().startswith('HEMISFERIO  celdas %d' % m.N) and 'en la cara oculta: Trumpzilla' in leg
            and 'apagado' in leg_off, '%s | %s' % (leg.strip(), leg_off.strip()))


run_test(base, prueba)
print('  Ahora: Hemisferio encendido (el planeta se para); Modojuego y Simmonstruo: los monstruos van a donde')
print('  suena un secuenciador y nunca salen de la cara visible.')
print('=' * 66)
