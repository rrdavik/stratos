"""
=============================================================================
ESTRATOS - FASE 32: EL JUEGO «EL DEVORADOR» - MODO DE JUEGO Y RONDA
=============================================================================
Requiere la fase 31. Turf War de toda la sala contra un monstruo (fases 32 a
37). El juego es un MODO que se enciende encima del mundo: lee y escribe el
mundo con las funciones de siempre y todo lo nuevo se activa con Modojuego.
Con Modojuego apagado, todo se comporta exactamente como antes.

QUE HACE
--------
  MODO         Modojuego encendido crea el estado del juego (W['juego']) y
               empieza la ronda 1. Apagado lo vacia y quita el monstruo, los
               brotes del mal, las zanjas y el agua de juego, sin tocar el resto
               del mundo (el hueco de una zanja se queda: ya es geologia, como el
               de una escision).
  RONDA        dura Duracionronda segundos. Al acabar: recuento, entierro (el
               mismo camino que Forzarciclo: concha, clasificacion y la noche de
               la fase 28) y ronda siguiente. Tras Rondas rondas el modo se
               queda en espera con el resultado en la leyenda; Nuevapartida
               vuelve a la ronda 1. En modo juego el mundo solo se entierra al
               acabar la ronda (o con Forzarciclo): ni el ciclo de la fase 6 ni
               el colapso lo cierran.
  RECUENTO     sobre TODAS las celdas del globo, en la cara visible y fuera de
               ella (D3). Publico: celdas con ocupacion y especie que no es el
               mal; mal: las del mal. Gana el mayor; en empate, el publico.
  HERENCIA     al enterrar en modo juego la ocupacion del mal no se hereda
               (Herenciamal 0, D9). La concha guarda la especie mal en sus
               celdas, como cualquier especie.
  MARCA        un anillo en la celda que mira cada persona de la sala (fase 24),
               de un solo color de la paleta humana, para que cada cual se
               encuentre en el globo (Marcajugador). v2 (motor v132): con
               Marcapublico (encendido), tambien con Modojuego apagado: la sala
               virtual marca a su publico en todas sus demos.
  LIBRE        v3 (motor v143), para pruebas: con Partidalibre la partida no
               tiene reloj ni rondas (Duracionronda y Rondas no cuentan): el
               mundo sigue combatiendo hasta que gana un bando. Gana el MAL
               cuando tiene Dominio de las celdas ocupadas del globo (1, por
               defecto: todas, el publico exterminado). Gana el BIEN (el
               publico) cuando tiene Dominio de ellas, el mal ya ha entrado en
               juego en esta partida y no queda monstruo del mal en pie
               (Trumpzilla y NefanyaMuto esperando o muertos). Al ganar:
               recuento, entierro como un fin de ronda y espera; Nuevapartida
               empieza otra. La demo GENoZilla de la sala la apaga mientras dura.
               Para la sala de verdad, apagado: rondas con reloj.
  RITMO        el juego cuenta en pasos de juego: Pasojuego semicorcheas del
               pulso (fase 17), por defecto 4 (una negra).
  LEYENDA      JUEGO    ronda 2/4   4:12   publico 38   mal 14   (globo)
               JUEGO    libre   12:40   publico 38   mal 14   (globo)   hasta exterminar

OPERADORES (en /project1/FASE1)
-------------------------------
  marcas, i_marcas   Geometry COMP instanciado (listones del anillo), familia
                     plastico del shader de la piel.

PROBAR
------
  Modojuego y Duracionronda 20: a los 20 s se entierra el mundo y la ronda
  pasa a 2. Simponer (fase 22) en una casilla: aparece el anillo en la celda
  que mira. Apagar Modojuego a mitad de ronda: el mundo sigue como estaba.
  Partidalibre (v3): la linea JUEGO dice libre y el tiempo que lleva; la
  partida no acaba hasta que gana el bien o el mal (Dominio 0,9 para que
  acabe antes, con el 90 % del globo ocupado).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase32_juego.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase32 v3  (la partida libre, para pruebas: Partidalibre y Dominio)'
banner(VERSION)

base = require_base(32)
motor = install_core(base, CARPETA, 32)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase32)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase32')
add_par(base, page, 'toggle', 'Modojuego', 'Modo juego', False)
add_par(base, page, 'float', 'Duracionronda', 'Duracion de ronda (s)', 360.0, 20.0, 900.0, clamp=True)
add_par(base, page, 'int', 'Rondas', 'Rondas', 4, 1, 12, clamp=True)
add_par(base, page, 'int', 'Pasojuego', 'Paso de juego (semicorcheas)', 4, 1, 16, clamp=True)
add_par(base, page, 'float', 'Herenciamal', 'Herencia del mal', 0.0, 0.0, 1.0, clamp=True)
add_par(base, page, 'toggle', 'Marcajugador', 'Marca de jugador', True)
add_par(base, page, 'toggle', 'Marcapublico', 'Marca tambien sin juego', True)     # v2
add_par(base, page, 'pulse', 'Nuevapartida', 'Nueva partida')
add_par(base, page, 'toggle', 'Partidalibre', 'Partida libre (pruebas)', False)     # v3
add_par(base, page, 'float', 'Dominio', 'Dominio para ganar (libre)', 1.0, 0.5, 1.0, clamp=True)     # v3
ok('pagina Fase32: Modojuego (apagado), Duracionronda 360 s, Rondas 4, Pasojuego 4, Herenciamal 0, '
   'Marcajugador, Marcapublico (v2: la marca tambien sin juego), Nuevapartida, Partidalibre (v3: apagado, '
   'sin reloj hasta que gana un bando) y Dominio 1')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

if base.op('mat_piel_plastico') is None:
    fail('mat_piel_plastico: no esta (el shader de la piel es de la fase 12)')
geo = make_instanced(base, 'marcas', -440, 2700, 'mat_piel_plastico')
if not setp_any(geo, ['instancea'], 'a'):
    fail('marcas no lee la rugosidad: Instance 2 -> Color A = a')
if has_par(base, 'Materialrespaldo'):
    setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_plastico'")
ok('marcas: el anillo de cada jugador en la celda que mira (familia plastico, paleta humana)')

set_render(base)

leeme(base, 32, """FASE 32 - EL DEVORADOR: MODO DE JUEGO Y RONDA
  Modojuego enciende el juego encima del mundo (apagado, todo como antes).
  Rondas de Duracionronda s: al acabar, recuento del globo entero (publico:
  ocupadas que no son del mal; mal: las del mal; empate, publico), entierro
  como Forzarciclo y ronda siguiente; tras Rondas, espera (Nuevapartida).
  En modo juego solo entierra la ronda. Herenciamal 0: el mal no se hereda.
  Marcajugador: un anillo en la celda de cada persona (Marcapublico: tambien
  con Modojuego apagado). Pasojuego: el paso de
  juego en semicorcheas (4, una negra). Geometria marcas.
  Partidalibre (pruebas): sin reloj ni rondas, hasta que gana un bando: el
  mal con Dominio de las celdas ocupadas del globo (1: todas); el bien con
  Dominio, el mal ya en juego y ningun monstruo del mal en pie.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS32 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Temaenciclo', 'Modojuego', 'Duracionronda', 'Rondas', 'Herenciamal', 'Umbralaparicion',
          'Simbalance', 'Colapsoon', 'Marcapublico', 'Partidalibre', 'Dominio')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS32)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)


def _sesion(m, W, c, t0, pasos=160):
    """Una sesion simulada: notas del SEQ1 y del SEQ2, golpes de bateria, el reloj
    del mundo y un entierro a mitad."""
    now = t0
    n1 = [60, 62, 64, 60, 67, 64, 62, 60]
    n2 = [48, 50, 53]
    for k in range(pasos):
        now += 0.125
        if k % 2 == 0:
            m.note_on(W, c, m.GEO, n1[(k // 2) % 8], 90 + k % 30, now)
        if k % 3 == 0:
            m.note_on(W, c, m.ARQ, n2[(k // 3) % 3], 70, now)
        if k % 2 == 1:
            m.note_off(W, c, m.GEO, n1[(k // 2) % 8], now, 120.0)
        if k % 16 == 9:
            m.erosion(W, c, k % 8, 100, now)
        m.tick(W, c, now, 120.0, True)
        if k == pasos // 2:
            m.close_cycle(W, c, now, 'forzado')
    return now


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Colapsoon = False
    S = SalaJuego(base, m, absTime.seconds + 1300.0)

    # 1. con Modojuego apagado, el mismo mundo que sin la fase
    W, c = S.nuevo(4, juego=False)
    c = dict(c, herencia_reparto=0)     # la herencia de la mezcla de la fase 43 no es del juego
    W0 = copy.deepcopy(W)
    c31 = dict(c, nivel=31)
    WA = copy.deepcopy(W0)
    _sesion(m, WA, c31, S.now)
    WB = copy.deepcopy(W0)
    _sesion(m, WB, c, S.now)
    distintas = sorted(k for k in set(WA) | set(WB) if WA.get(k) != WB.get(k))
    t.check('con Modojuego apagado, una sesion simulada da el mismo mundo que sin la fase (y sin juego ni '
            'bloqueadas en W)', not distintas and 'juego' not in WB and 'bloqueadas' not in WB
            and m.occupied(WB) > 0, ', '.join(distintas[:6]) or '%d celdas' % m.occupied(WB))

    # 2. el recuento: todo el globo, tambien fuera de la cara visible
    W, c = S.nuevo(2)
    vis = set(m.cara_visible(c))
    fuera = [i for i in range(m.N) if i not in vis]
    dentro = sorted(vis)
    pub = dentro[:3] + fuera[:2]
    mal = dentro[5:7] + fuera[4:5]
    for i in pub:
        W['occ'][i], W['sp'][i], W['own'][i] = 2, m.GEO, m.GEO
    for i in mal:
        W['occ'][i], W['sp'][i], W['own'][i] = 1, m.MAL, m.ARQ
    W['sp'][fuera[6]] = m.MAL                   # sin ocupacion: no cuenta
    S.semis(W, c, 1)
    J = W['juego']
    t.check('el recuento cuenta todas las celdas del globo (5 del publico y 3 del mal, 3 de ellas fuera de la '
            'cara visible)', m.recuento(W) == (5, 3) and J['recuento'] == dict(publico=5, mal=3)
            and len(fuera) > 0 and len(vis) > 0, str(J['recuento']))
    t.check('gana el mayor; en empate, el publico',
            m.ganador(5, 3) == 'publico' and m.ganador(3, 5) == 'mal' and m.ganador(4, 4) == 'publico')

    # 3. herencia del mal: no se hereda; la concha guarda la especie mal
    i_mal, i_pub = mal[0], pub[0]
    W['occ'][i_mal] = W['occ'][i_pub] = 8
    conchas = m.n_shells(W)
    base.par.Duracionronda = 20.0
    c = m.cfg()
    J['t0'] = S.now - 20.0
    ev = S.semis(W, c, 1)
    sh = W['shells'][-1]
    t.check('fin de ronda: el entierro (una concha mas, motivo ronda), ronda 2 y el recuento a cero',
            ev is not None and ev.get('motivo') == 'ronda' and m.n_shells(W) == conchas + 1 and J['ronda'] == 2
            and J['recuento'] == dict(publico=0, mal=0) and J['resultados'][-1]['publico'] == 5
            and J['resultados'][-1]['mal'] == 3 and J['resultados'][-1]['gana'] == 'publico',
            'ronda %d, %s' % (J['ronda'], J['recuento']))
    t.check('al enterrar, la ocupacion del mal no se hereda (Herenciamal 0) y la del publico si (Herencia); '
            'la concha guarda sp = mal en sus celdas',
            W['occ'][i_mal] == 0 and W['sp'][i_mal] == 0 and W['occ'][i_pub] == 2
            and sh['sp'][i_mal] == m.MAL and sh['sp'][i_pub] == m.GEO,
            'mal %d, publico %d' % (W['occ'][i_mal], W['occ'][i_pub]))

    # 4. las rondas: tras Rondas, espera; Nuevapartida
    base.par.Rondas = 3
    c = m.cfg()
    for _ in range(2):
        J['t0'] = S.now - 20.0
        S.semis(W, c, 1)
    leg = m._legend_juego(W, c)
    espera = (J['estado'], J['ronda'], len(J['resultados']))
    S.semis(W, c, 40)
    t.check('tras Rondas rondas el modo se queda en espera, con el resultado en la leyenda; no entierra mas',
            espera == ('espera', 3, 3) and len(J['resultados']) == 3 and 'fin   gana publico 3-0' in leg,
            leg.strip())
    m.on_pulse('Nuevapartida')
    W = m.world()
    J = W['juego']
    t.check('Nuevapartida: ronda 1, recuento a cero', J['estado'] == 'juego' and J['ronda'] == 1
            and not J['resultados'] and J['recuento'] == dict(publico=0, mal=0))

    # 5. la marca de jugador y la leyenda
    base.par.Rondas = 4
    base.par.Duracionronda = 360.0
    W, c = S.nuevo(2)
    cols, filas = m.rejilla_sala(c)
    k = 4 * cols + 5
    S.camara(W, c, [k], n=3)
    inst = m.build_instances(W, c, S.now)
    celda = m.celda_de_casilla(W, c, k)
    filas_m = inst.get('marcas', [])
    n0 = m.normal_i(celda)
    cerca = all(sum(a * b for a, b in zip(m._norm(r[:3]), n0)) > 0.98 for r in filas_m)
    col = m.paleta_humana(c, m.MARCA_K)
    base.par.Marcajugador = False
    sin = m.build_instances(W, m.cfg(), S.now).get('marcas', [])
    base.par.Marcajugador = True
    t.check('una persona en la sala: un anillo (%d listones) en la celda que mira su casilla, del color de la '
            'paleta humana; Marcajugador apagado, sin anillo' % m.MARCA_SEGMENTOS,
            len(filas_m) == m.MARCA_SEGMENTOS and cerca and all(tuple(r[9:12]) == tuple(col) for r in filas_m)
            and sin == [], 'celda %d, %d filas' % (celda, len(filas_m)))
    leg = m._legend_juego(W, c)
    t.check('la linea JUEGO: ronda, tiempo que queda, publico y mal del globo',
            leg.startswith('  JUEGO    ronda 1/4   ') and '(globo)' in leg and 'publico 0   mal 0' in leg, leg.strip())

    # 6. apagar a mitad de ronda: el mundo sigue como estaba (sin el mal)
    W, c = S.nuevo(3)
    for i in pub[:2]:
        S.sembrar(W, c, i, 3)
    W['occ'][mal[0]], W['sp'][mal[0]], W['own'][mal[0]] = 2, m.MAL, m.GEO
    occ = list(W['occ'])
    cols_ = copy.deepcopy(W['cols'])
    base.par.Modojuego = False
    c = m.cfg()
    m.tick(W, c, S.now + 0.1, 120.0, True)
    esperado = [0 if i == mal[0] else o for i, o in enumerate(occ)]
    t.check('apagar Modojuego a mitad de ronda: sin estado de juego ni brotes del mal; el resto del mundo, igual',
            'juego' not in W and W['occ'] == esperado and W['cols'] == cols_ and W['sp'][mal[0]] == 0,
            '%d celdas' % m.occupied(W))
    t.check('fuera del modo juego, la linea JUEGO dice apagado', 'apagado' in m._legend_juego(W, c))

    # 7. v2: la marca del publico sin juego (Marcapublico)
    cols, filas = m.rejilla_sala(c)
    k = 4 * cols + 5
    S.camara(W, c, [k], n=3)
    con = m.build_instances(W, m.cfg(), S.now).get('marcas', [])
    base.par.Marcapublico = False
    sin = m.build_instances(W, m.cfg(), S.now).get('marcas', [])
    base.par.Marcapublico = True
    t.check('v2: Modojuego apagado y una persona en la sala: su anillo (Marcapublico); apagado, sin anillo',
            len(con) == m.MARCA_SEGMENTOS and sin == [], '%d filas con, %d sin' % (len(con), len(sin)))
    o = base.op('i_marcas')
    t.check('marcas e i_marcas (Geometry COMP instanciado)', o is not None and base.op('marcas') is not None)

    # 8. v3: la partida libre
    _prueba_libre(t, m, S)


def _prueba_libre(t, m, S):
    if has_par(base, 'Umbralaparicion'):
        base.par.Umbralaparicion = 1.0      # el monstruo no aparece solo: lo pone la prueba
    W, c = S.nuevo(3)
    base.par.Partidalibre = True
    base.par.Dominio = 1.0
    base.par.Duracionronda = 20.0
    base.par.Rondas = 1
    c = m.cfg()
    J = W['juego']
    vis = sorted(m.cara_visible(c))
    pub, mal = vis[:4], vis[6:8]
    for i in pub:
        W['occ'][i], W['sp'][i], W['own'][i] = 2, m.GEO, m.GEO
    J['t0'] = S.now - 100.0                 # el reloj de la ronda, muy pasado
    S.semis(W, c, 2)
    leg = m._legend_juego(W, c)
    t.check('v3: con Partidalibre no hay reloj ni rondas (Duracionronda 20 s, 100 s pasados, Rondas 1): sigue la '
            'ronda 1; sin el mal aun, el publico no gana; la linea JUEGO dice libre',
            J['estado'] == 'juego' and J['ronda'] == 1 and not J['resultados'] and not J.get('mal_visto')
            and 'libre' in leg and 'sin el mal aun' in leg and 'hasta exterminar' in leg, leg.strip())

    for i in mal:                           # el mal entra
        W['occ'][i], W['sp'][i], W['own'][i] = 1, m.MAL, m.GEO
    S.semis(W, c, 1)
    v_mal_dentro = J['estado'] == 'juego' and J.get('mal_visto')
    for i in mal:                           # el mal desaparece; su monstruo, en pie
        W['occ'][i] = 0
        W['sp'][i] = W['own'][i] = 0
    J['mon'].update(estado='busca', celda=vis[10])
    v_pie = m.victoria_libre(W, c, J, len(pub), 0)
    J['mon'].update(estado='muere', t_muerte=S.now)
    v_muerto = m.victoria_libre(W, c, J, len(pub), 0)
    J['mon'] = m.mon_nuevo(1, c['tam_inicial'])
    t.check('v3: el bien gana solo con el mal ya en juego y sin monstruo del mal en pie (Trumpzilla buscando: no; '
            'muerto: si)', v_mal_dentro and v_pie is None and v_muerto == 'publico', '%s / %s' % (v_pie, v_muerto))
    t.check('v3: el mal gana al exterminar al publico; con Dominio 0,9, con el 90 % de las celdas ocupadas',
            m.victoria_libre(W, c, J, 0, 5) == 'mal' and m.victoria_libre(W, c, J, 1, 9) is None
            and m.victoria_libre(W, dict(c, dominio=0.9), J, 1, 9) == 'mal'
            and m.victoria_libre(W, dict(c, dominio=0.9), J, 9, 1) == 'publico'
            and m.victoria_libre(W, dict(c, dominio=0.9), J, 8, 2) is None)

    conchas = m.n_shells(W)
    ev = S.semis(W, c, 1)                   # sin mal ni monstruo: gana el bien
    leg = m._legend_juego(W, c)
    r = J['resultados'][-1] if J['resultados'] else {}
    t.check('v3: al ganar el bien, recuento, entierro (una concha mas) y espera; la linea JUEGO lo dice',
            ev is not None and J['estado'] == 'espera' and r.get('gana') == 'publico' and r.get('libre')
            and m.n_shells(W) == conchas + 1 and m.resultado_partida(J)['gana'] == 'publico'
            and 'fin de la partida libre' in leg and 'gana el bien' in leg, leg.strip())

    m.on_pulse('Nuevapartida')
    W = m.world()
    J = W['juego']
    c = m.cfg()
    for i in pub:
        W['occ'][i] = 0
        W['sp'][i] = W['own'][i] = 0
    for i in mal:
        W['occ'][i], W['sp'][i], W['own'][i] = 2, m.MAL, m.GEO
    S.semis(W, c, 1)
    leg = m._legend_juego(W, c)
    t.check('v3: Nuevapartida empieza otra libre; sin publico en el globo, gana el mal',
            J['estado'] == 'espera' and J['resultados'][-1]['gana'] == 'mal' and 'gana el mal' in leg, leg.strip())

    base.par.Partidalibre = False
    c = m.cfg()
    m.on_pulse('Nuevapartida')
    W = m.world()
    J = W['juego']
    J['t0'] = S.now - 20.0
    S.semis(W, c, 1)
    t.check('v3: Partidalibre apagado, vuelve el reloj: a los 20 s acaba la ronda (Rondas 1: espera)',
            J['estado'] == 'espera' and len(J['resultados']) == 1 and not J['resultados'][0].get('libre'))


run_test(base, prueba)
print('  Ahora: Modojuego y Duracionronda 20: a los 20 s se entierra el mundo y la ronda pasa a 2.')
print('  Simponer en una casilla: el anillo en la celda que mira.')
print('=' * 66)
