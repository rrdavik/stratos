"""
=============================================================================
ESTRATOS - FASE 37: ARMAS OPCIONALES
=============================================================================
Requiere la fase 36. Cinco armas, cada una con su interruptor, todas APAGADAS
de fabrica para probar primero el juego base. La zanja trampa y el cebo no
necesitan fase: salen de las fases 33 y 34.

QUE HACE
--------
  CERCO        (Armacerco) las celdas con una persona quieta Tparada son muro en
               el Dijkstra del objetivo. Si no queda ningun objetivo alcanzable,
               esta acorralado: no devora y pierde Hambre escalones de acum por
               compas.
  PISOTON      (Armapison) Npison personas o mas en casillas que miran a la celda
               del monstruo: mientras aguantan no devora y tam baja Encoge por
               paso de juego.
  ESTATUAS     (Armaestatuas) todas las personas quietas y el microfono por
               debajo de Umbralsilencio durante Tquietud s: petrificado Tpiedra s
               (ni se mueve ni devora). El ruido de sala, al reves, multiplica su
               velocidad hasta x2 (con la energia de la ventana de ruido, fase 21).
  GRITO        (Armagrito) el ruido sostenido por encima de Umbralcorte durante
               Ventanaruido (el corte del ruido de sala, fase 21) abre una zanja
               de 1 celda en la celda del monstruo, de Profgrito conchas: cae.
               Recarga Recargagrito s.
  RELAMPAGO    (Armarelampago) una fila abre su zanja a una celda o menos del
               monstruo: aturdido Taturdido s (ni se mueve ni devora).
  Con todas apagadas el juego da el mismo resultado que tras la fase 36.
  LEYENDA      ARMAS    cerco on   pison 2/3   estatuas 1.2/4.0 s   grito listo

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase37_armas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase37 v1  (el devorador: cerco, pisoton, estatuas, grito y relampago, apagadas de fabrica)'
banner(VERSION)

base = require_base(37)
motor = install_core(base, CARPETA, 37)
m = motor.module

page = get_page(base, 'Fase37')
add_par(base, page, 'toggle', 'Armacerco', 'Arma: cerco', False)
add_par(base, page, 'int', 'Hambre', 'Hambre del cerco (escalones por compas)', 1, 0, 8, clamp=True)
add_par(base, page, 'toggle', 'Armapison', 'Arma: pisoton', False)
add_par(base, page, 'int', 'Npison', 'Personas del pisoton', 3, 1, 10, clamp=True)
add_par(base, page, 'float', 'Encoge', 'Encogimiento por paso', 0.05, 0.0, 0.5, clamp=True)
add_par(base, page, 'toggle', 'Armaestatuas', 'Arma: estatuas', False)
add_par(base, page, 'float', 'Tquietud', 'Tiempo de estatuas (s)', 4.0, 1.0, 30.0, clamp=True)
add_par(base, page, 'float', 'Umbralsilencio', 'Umbral de silencio (flujo del microfono)', 0.3, 0.0, 2.0)
add_par(base, page, 'float', 'Tpiedra', 'Tiempo petrificado (s)', 6.0, 1.0, 30.0, clamp=True)
add_par(base, page, 'toggle', 'Armagrito', 'Arma: grito', False)
add_par(base, page, 'int', 'Profgrito', 'Profundidad del grito (conchas)', 2, 1, 8, clamp=True)
add_par(base, page, 'float', 'Recargagrito', 'Recarga del grito (s)', 30.0, 5.0, 300.0, clamp=True)
add_par(base, page, 'toggle', 'Armarelampago', 'Arma: relampago', False)
add_par(base, page, 'float', 'Taturdido', 'Tiempo aturdido (s)', 4.0, 1.0, 30.0, clamp=True)
ok('pagina Fase37: Armacerco, Armapison, Armaestatuas, Armagrito y Armarelampago (apagadas), Hambre 1, '
   'Npison 3, Encoge 0,05, Tquietud 4 s, Umbralsilencio 0,3 (se fija en sala), Tpiedra 6 s, Profgrito 2, '
   'Recargagrito 30 s, Taturdido 4 s')

set_render(base)

leeme(base, 37, """FASE 37 - ARMAS OPCIONALES (apagadas de fabrica)
  Cerco: personas quietas Tparada son muro; sin objetivo alcanzable, no
  devora y pierde Hambre de acum por compas. Pisoton: Npison personas sobre
  su celda, no devora y encoge Encoge por paso. Estatuas: todos quietos y en
  silencio (Umbralsilencio) Tquietud s, petrificado Tpiedra s; el ruido lo
  acelera hasta x2. Grito: el corte del ruido de sala abre una zanja de
  Profgrito en su celda (recarga Recargagrito s). Relampago: una zanja a una
  celda o menos lo aturde Taturdido s.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS37 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Simbalance', 'Colapsoon', 'Temaenciclo', 'Modojuego', 'Umbralaparicion',
          'Zanjajuego', 'Armacerco', 'Armapison', 'Armaestatuas', 'Armagrito', 'Armarelampago')
ARMAS = ('Armacerco', 'Armapison', 'Armaestatuas', 'Armagrito', 'Armarelampago')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS37)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ):
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = m.GEO
    W['traza'][i] = 1


def _solo(arma=None):
    for a in ARMAS:
        setattr(base.par, a, a == arma)
    return m.cfg()


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 3.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0
    base.par.Zanjajuego = False             # sin zanjas de las personas de las pruebas
    base.par.Tfila = 60.0
    S = SalaJuego(base, m, absTime.seconds + 2700.0)
    W, c = S.nuevo(6)
    cols, filas = m.rejilla_sala(c)
    por = {}
    for k in range(cols * filas):
        por.setdefault(m.celda_de_casilla(W, c, k), []).append(k)
    # a: la celda que mira al centro de la sala (con todas sus vecinas en la sala); lejos, a 2 celdas;
    # ap: la celda con mas casillas (el pisoton necesita Npison casillas que la miren)
    a = m.celda_de_casilla(W, c, (filas // 2) * cols + cols // 2)
    dist, _ = m.dijkstra_mon(W, c, a)
    lejos = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9 and x in por)
    ap = max(por, key=lambda x: (len(por[x]), -x))

    # 0. con todas apagadas, el mismo resultado que tras la fase 36
    def partida(cfg_):
        S2 = SalaJuego(base, m, absTime.seconds + 3500.0)
        W2, _ = S2.nuevo(6)
        for x, o in ((lejos, 4), (m.NEIGH[a][0], 3)):
            _poner(m, W2, x, o)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(10):
            S2.pasos(W2, cfg_, 2)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento']))
    c = _solo()
    r37 = partida(c)
    r36 = partida(dict(c, nivel=36))
    t.check('con todas las armas apagadas, el juego da el mismo resultado que tras la fase 36',
            r37 == r36 and r37[2]['comidos'] > 0, 'comidos %d' % r37[2]['comidos'])

    # 1. cerco: muro de personas quietas; acorralado, no devora y pierde Hambre por compas
    c = _solo('Armacerco')
    W, c = S.nuevo(6)
    _poner(m, W, lejos, 4)
    muro = [por[j][0] for j in m.NEIGH[a]]
    S.camara(W, c, muro, seg=c['t_parada'] + 0.3)
    mo = m.aparecer(W, c, S.now, a)
    mo['acum'] = 3
    m.actualizar_tam(c, mo)
    acorr = (mo['objetivo'], mo['acorralado'])
    S.semis(W, c, 16, casillas=muro)
    t.check('cerco: las celdas con una persona quieta Tparada son muro; sin objetivo alcanzable esta acorralado, '
            'no devora y pierde Hambre (1) de acum por compas',
            acorr == (None, True) and mo['acum'] == 2 and W['occ'][lejos] == 4 and mo['celda'] == a,
            '%s, acum %d, muro %s' % (acorr, mo['acum'], sorted(m.muros_cerco(W, c, S.now))))

    # 2. pisoton
    c = _solo('Armapison')
    W, c = S.nuevo(6)
    a_ = a
    a = ap
    _poner(m, W, a, 6)
    mo = m.aparecer(W, c, S.now, a)
    mo['acum'] = 4
    m.actualizar_tam(c, mo)
    tam0 = mo['tam']
    pis = por[a][:int(c['n_pison'])]
    S.camara(W, c, pis, n=3)
    S.pasos(W, c, 2, casillas=pis)
    pisado = (W['occ'][a], round(mo['tam'], 3), mo['pisoton'])
    leg = m._legend_armas(W, c)
    S.camara(W, c, [], n=3)
    S.pasos(W, c, 1, casillas=[])
    t.check('pisoton: Npison personas sobre su celda: no devora y tam baja Encoge por paso; al irse, devora',
            pisado == (6, round(tam0 - 2 * c['encoge'], 3), True) and W['occ'][a] == 4 and not mo['pisoton']
            and 'pison 3/3' in leg, '%s, %s' % (pisado, leg.strip()))
    a = a_

    # 3. estatuas: quietos y en silencio, petrificado; el ruido lo acelera
    c = _solo('Armaestatuas')
    W, c = S.nuevo(6)
    _poner(m, W, lejos, 4)
    mo = m.aparecer(W, c, S.now, a)
    quietos = [por[lejos][0]]
    S.camara(W, c, quietos, n=3)
    W['mic']['flujo'] = 0.0
    antes = None
    for _ in range(int(round(c['t_quietud'] / S.SEMI)) + 8):
        S.semis(W, c, 1, casillas=quietos)
        if antes is None and mo['piedra'] is not None:
            antes = (S.now - (W['juego']['ev']['piedra']['t']), mo['celda'], W['occ'][lejos], mo['mov'])
    S.semis(W, c, 24, casillas=quietos)
    t.check('estatuas: todos quietos y el microfono en silencio Tquietud s: petrificado Tpiedra s (ni se mueve '
            'ni devora)', antes is not None and S.now < mo['piedra'] and (mo['celda'], W['occ'][lejos]) == antes[1:3]
            and W['juego']['armas']['piedras'] == 1, '%s' % (antes,))
    W, c = S.nuevo(6)
    _poner(m, W, lejos, 4)
    mo = m.aparecer(W, c, S.now, a)
    W['ruido']['total'] = c['umbral_corte']
    S.semis(W, c, int(c['paso_monstruo']) // 2)
    t.check('estatuas: el ruido de sala multiplica la velocidad hasta x2 (una celda en 8 semicorcheas)',
            mo['celda'] != a and m.factor_ruido(W, c) == 2.0)

    # 4. grito
    c = _solo('Armagrito')
    W, c = S.nuevo(6)
    mo = m.aparecer(W, c, S.now, a)
    mo['acum'] = 3
    S.pasos(W, c, 1)
    W['ruido']['cortes'] += 1
    S.pasos(W, c, 1)
    grito = (W['juego']['zanjas'].get(a), mo['estado'], mo['acum'], mo['caidas'])
    W['ruido']['cortes'] += 1
    S.pasos(W, c, 1)
    t.check('grito: el corte del ruido de sala abre una zanja de Profgrito (2) conchas en su celda: cae; '
            'el siguiente antes de Recargagrito, no', grito == (2, 'cae', 0, 1) and W['juego']['zanjas'][a] == 2
            and W['juego']['armas']['gritos'] == 1, str(grito))

    # 5. relampago
    c = _solo('Armarelampago')
    W, c = S.nuevo(6)
    _poner(m, W, lejos, 4)
    mo = m.aparecer(W, c, S.now, a)
    v = m.NEIGH[a][0]
    m.cavar_zanja(W, c, v, 2, S.now)
    m.rayo_relampago(W, c, [v], S.now)
    S.semis(W, c, int(c['paso_monstruo']) + 4)
    aturdido = mo['celda'] == a
    S.semis(W, c, int(round(c['t_aturdido'] / S.SEMI)) + int(c['paso_monstruo']) * 2)
    d2, _ = m.dijkstra_mon(W, c, mo['celda'])
    lejisimo = [x for x in d2 if d2[x] >= 3.0]
    lejos_z = m.rayo_relampago(W, c, lejisimo[:1], S.now) if lejisimo else True
    t.check('relampago: una zanja a una celda o menos lo aturde Taturdido s (ni se mueve ni devora); mas lejos, no',
            aturdido and mo['celda'] != a and W['juego']['armas']['rayos'] == 1 and not lejos_z)
    c = _solo()
    leg = m._legend_armas(W, c)
    t.check('la linea ARMAS', leg.startswith('  ARMAS    cerco off   pison off   estatuas off   grito off'),
            leg.strip())


run_test(base, prueba)
print('  Ahora: cada arma con su interruptor (Armacerco ... Armarelampago), una a una.')
print('=' * 66)
