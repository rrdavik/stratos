"""
=============================================================================
ESTRATOS - FASE 41: HEMISFERIO, EL JUEGO SOLO EN LA CARA VISIBLE
=============================================================================
Requiere la fase 40 (motor v137, comun v99). Con Hemisferio, las mismas N celdas del rango de
notas se reparten solo por la cara que mira a la sala y la cara oculta no tiene celdas: los
monstruos no pueden perderse detras del planeta. Sin Hemisferio (de fabrica), todo igual que
en la fase 40.

QUE HACE
--------
  RETICULA     Con Hemisferio, N no cambia (una celda por nota del rango), pero las celdas
               van de un borde de la cara visible al otro (Anchoangular, 180 de fabrica): el
               anillo de 12 notas pasa de 30 a 15 grados por celda, no se cierra por detras
               (la primera y la ultima no son vecinas) y los polos quedan arriba y abajo del
               disco. Toda celda tiene casilla: cara_visible es todo el globo. Cambiar
               Hemisferio (o Anchoangular) es como cambiar el rango de notas: el mundo
               empieza vacio.
  PLANETA      No gira: Loncentral = 0, el giro vivo se para (giro_factor 0) y ritmo.rotation
               devuelve un angulo fijo (comun v99, patch_ritmo_hemi). Las celdas quedan
               ancladas a la vista.
  CERCO        Trumpzilla y Godzilla solo existen en celdas del hemisferio: ningun camino,
               objetivo, aparicion ni retirada sale de la cara visible. Sin giro no hay
               borde de entrada: Trumpzilla aparece en el borde lateral (izquierda y derecha
               alternando con n) y Godzilla en el borde contrario al de Trumpzilla.
  PULSACIONES  El objetivo de los dos pasa a occ x (1 + Pesopulso x calor) / (1 + coste). El
               calor es 1 si sono un secuenciador en la celda o en una vecina en este paso y
               baja a 0 en Ventanapulso pasos de juego (t_gate). Trumpzilla busca el
               publico donde se construye, Godzilla el mal donde crece. Sin pulsaciones
               recientes (o con Pesopulso 0), la regla de siempre: occ / (1 + coste).

PARAMETROS (pagina Fase41)
--------------------------
  Hemisferio (apagado), Pesopulso 1,0, Ventanapulso 8.
  Leyenda:  HEMISFERIO  celdas 85   cara visible 85/85   objetivo con pulso (calor 0.75)

PROBAR
------
  Hemisferio encendido: el planeta se para y las celdas cubren solo la cara visible.
  Modojuego, Simmonstruo y Simmal: los monstruos van a la celda donde suena un SEQ.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase41_hemisferio.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase41 v1  (Hemisferio: la reticula solo en la cara visible, el planeta quieto, los monstruos van a las pulsaciones)'
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

leeme(base, 41, """FASE 41 - HEMISFERIO, EL JUEGO SOLO EN LA CARA VISIBLE
  Con Hemisferio las N celdas del rango de notas se reparten solo por la cara que
  mira a la sala (Anchoangular, 180): el anillo de 12 pasa de 30 a 15 grados por celda,
  no se cierra por detras y la cara oculta no tiene celdas. El planeta no gira
  (Loncentral 0). Los monstruos no salen de la cara visible: Trumpzilla aparece por un
  borde lateral (alternando), Godzilla por el contrario, y los dos buscan donde suenan
  los secuenciadores: occ x (1 + Pesopulso x calor) / (1 + coste), el calor baja a 0 en
  Ventanapulso pasos (8). Cambiar Hemisferio vacia el mundo, como cambiar el rango.
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

    # 1. la reticula: sin Hemisferio la esfera de siempre; con el, las mismas N celdas en la cara visible
    base.par.Hemisferio = False
    m.sync_grid()
    N0, lejos_cfg = m.N, m.cfg()
    esfera = (copy.deepcopy(m.NORMALS), copy.deepcopy(m.NEIGH), list(m.SIZE_EW), list(m.SIZE_NS), m.grid_key())
    ocultas0 = [i for i in range(m.N) if m.casilla_de_celda(lejos_cfg, i) is None]
    base.par.Hemisferio = True
    m.sync_grid()
    c = m.cfg()
    lons = [m.lonlat_celda(i)[1] for i in range(m.N)]
    anillo = [k for k in m.RINGS if len(k) == 12][0]
    pasos = sorted(m.lonlat_celda(k)[1] for k in anillo)
    sim = all(i in m.NEIGH[j] for i in range(m.N) for j in m.NEIGH[i])
    ext = min(anillo, key=lambda k: m.lonlat_celda(k)[1]), max(anillo, key=lambda k: m.lonlat_celda(k)[1])
    t.check('Hemisferio: N no cambia (%d), todas las celdas con casilla y a menos de 90 grados del centro, el anillo '
            'de 12 a 15 grados por celda, sus extremos no son vecinas, la vecindad es simetrica y conexa' % N0,
            m.N == N0 and m.hemisferio() and m.cara_visible(c) == list(range(m.N))
            and all(abs(x) < 90.0 for x in lons) and abs(pasos[1] - pasos[0] - 15.0) < 1e-6
            and ext[1] not in m.NEIGH[ext[0]] and sim and _conexo(m) and ocultas0 != []
            and c['hemisferio'] == 1 and m.grid_key()[:2] == esfera[4] and len(m.grid_key()) == 3,
            'N %d, longitudes %.1f a %.1f, paso %.1f, esfera con %d celdas ocultas' % (
                m.N, min(lons), max(lons), pasos[1] - pasos[0], len(ocultas0)))
    base.par.Hemisferio = False
    m.sync_grid()
    t.check('sin Hemisferio la reticula es la esfera de antes: mismas normales, vecinas y tamanos',
            not m.hemisferio() and m.NORMALS == esfera[0] and m.NEIGH == esfera[1] and m.SIZE_EW == esfera[2]
            and m.SIZE_NS == esfera[3] and m.grid_key() == esfera[4], 'N %d' % m.N)
    base.par.Hemisferio = True
    m.sync_grid()

    # 2. las notas y las casillas: todo cae en la cara visible
    c = m.cfg()
    fuera = []
    for modo in ('plegar', 'limitar'):
        base.par.Fuerarango = modo
        m.sync_grid()
        for nota in range(0, 128):
            i = m.note_cell(nota)
            if i is None or not (0 <= i < m.N) or m.casilla_de_celda(c, i) is None:
                fuera.append((modo, nota))
    base.par.Fuerarango = 'plegar'
    m.sync_grid()
    cols, filas_c = m.rejilla_sala(c)
    W, c = S.nuevo(4)
    celdas_k = [m.celda_de_casilla(W, c, k) for k in range(cols * filas_c)]
    t.check('las 128 notas MIDI (plegar y limitar) y las %d casillas de la sala caen en celdas del hemisferio, y '
            'cada celda tiene su casilla' % (cols * filas_c),
            not fuera and all(0 <= x < m.N for x in celdas_k)
            and all(m.casilla_de_celda(c, x) is not None for x in range(m.N)),
            '%d notas fuera' % len(fuera))

    # 3. el planeta quieto: Loncentral 0, giro fijo, giro vivo parado y el ritmo lo consulta
    rt = base.op('ritmo')
    texto = rt.text if rt is not None else ''
    t.check('el planeta no gira con Hemisferio: Loncentral 0, giro_fijo %.0f, giro_factor 0; sin el, gira (giro_fijo '
            'None); ritmo.rotation consulta al motor' % m.HEMI_RY,
            m.lon_central(0) == 0.0 and m.giro_fijo() == m.HEMI_RY and m.giro_factor() == 0.0
            and 'giro_fijo(' in texto, 'ritmo %s' % ('con el gancho' if 'giro_fijo(' in texto else 'sin el'))

    # 4. el cerco: ninguno sale del hemisferio y los dos se mueven (400 pasos, sala vacia)
    base.par.Godzillasala = 'siempre'
    W, c = S.nuevo(4)
    vis = set(m.cara_visible(c))
    for k, x in enumerate(sorted(vis)[::4]):
        _poner(m, W, x, 2 + k % 4)
    _mal(m, W, c, sorted(vis)[7], 3, S.now)
    _mal(m, W, c, sorted(vis)[-9], 2, S.now)
    m.aparecer(W, c, S.now, sorted(vis)[len(vis) // 2])
    visitas, mal_visto = {'mon': set(), 'bien': set()}, []
    for _ in range(400):
        S.pasos(W, c, 1)
        J = W['juego']
        for nm in ('mon', 'bien'):
            g = J.get(nm)
            if g is None or g.get('celda') is None:
                continue
            visitas[nm].add(g['celda'])
            for x in [g['celda'], g.get('objetivo'), g.get('de'), g.get('retira')] + list(g.get('camino') or []):
                if x is not None and x not in vis:
                    mal_visto.append((nm, x))
    t.check('400 pasos con Trumpzilla y Godzilla: ni su celda, ni su objetivo, ni su camino, ni su retirada salen '
            'de las celdas del hemisferio, y los dos andan (celdas visitadas %d y %d)'
            % (len(visitas['mon']), len(visitas['bien'])),
            not mal_visto and len(visitas['mon']) > 1 and len(visitas['bien']) > 1,
            '%s' % mal_visto[:4])
    base.par.Godzillasala = 'vacia'

    # 5. las pulsaciones: van a donde suena un secuenciador
    W, c = S.nuevo(4)
    a = min(range(m.N), key=lambda i: (abs(m.lonlat_celda(i)[1]) + abs(m.lonlat_celda(i)[0]), i))
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

    # 6. la aparicion: por un borde lateral, alternando, y Godzilla por el contrario
    W, c = S.nuevo(4)
    c = dict(m.cfg(), t_vacia=0.0)
    lon = lambda i: m.lonlat_celda(i)[1]
    c1 = m.celda_aparicion(W, c)
    mo = m.aparecer(W, c, S.now, c1)
    c2 = m.celda_aparicion_bien(W, c)
    mo2 = m.aparecer(W, c, S.now, m.celda_aparicion(W, c))           # el #2, sin Godzilla: el otro borde
    t.check('Trumpzilla #1 aparece en el borde derecho del hemisferio (longitud %.1f), Godzilla en el contrario (%.1f)'
            ' y Trumpzilla #2 en el izquierdo (%.1f)' % (lon(c1), lon(c2) if c2 is not None else 0.0, lon(mo2['celda'])),
            lon(c1) > 60.0 and c2 is not None and lon(c2) < -60.0 and lon(mo2['celda']) < -60.0,
            '%.1f %s %.1f' % (lon(c1), c2, lon(mo2['celda'])))

    # 7. la lucha: en bordes opuestos no se tocan; la leyenda
    W, c = S.nuevo(4)
    c = dict(m.cfg(), t_vacia=0.0)
    izq = min(range(m.N), key=lambda i: (lon(i), i))
    der = max(range(m.N), key=lambda i: (lon(i), i))
    m.aparecer(W, c, S.now, izq)
    m.aparecer_godzilla(W, c, S.now, der)
    sin_lucha = not m.encuentro(W, c, S.now)
    leg = m._legend_hemisferio(W, c)
    base.par.Hemisferio = False
    m.sync_grid()
    leg_off = m._legend_hemisferio(W, m.cfg())
    base.par.Hemisferio = True
    m.sync_grid()
    t.check('dos monstruos en los bordes laterales opuestos no son contiguos y no luchan; la leyenda dice HEMISFERIO '
            'celdas %d, cara visible %d/%d y, apagado, HEMISFERIO apagado' % (m.N, m.N, m.N),
            sin_lucha and leg.strip().startswith('HEMISFERIO  celdas %d   cara visible %d/%d' % (m.N, m.N, m.N))
            and 'apagado' in leg_off, '%s | %s' % (leg.strip(), leg_off.strip()))


run_test(base, prueba)
print('  Ahora: Hemisferio encendido (el planeta se para); Modojuego y Simmonstruo: los monstruos van a donde')
print('  suena un secuenciador y nunca salen de la cara visible.')
print('=' * 66)
