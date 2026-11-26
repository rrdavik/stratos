"""
=============================================================================
ESTRATOS - FASE 34: ZANJAS Y AGUA
=============================================================================
Requiere la fase 33. En modo juego, la fila de la fase 29 cava una zanja en
todas sus celdas; el monstruo cae en ellas y el agua lo ahoga.

QUE HACE
--------
  ZANJA        una fila parada Tfila (fase 29) corta, en modo juego, en TODAS
               las celdas que miran a sus casillas, no solo en la de origen (la
               escision de la fase 29 sigue abriendose en el origen, con su
               fulgurita y su relampago). Profundidad de cada celda: personas x
               Conchasporpersona, con el nucleo como tope. Cada celda se trata
               como la escision: quita losetas, vacia la celda, borra sus
               inclusiones, sin cicatriz cian, y la concha siguiente la tapiza.
               Si llega gente mientras la fila sigue parada, sus celdas se
               anaden y todas bajan a la profundidad nueva. La celda de cada
               casilla queda fija al empezar a cavar (el planeta gira: una fila
               quieta cava sus celdas, no una franja). Cuando alguien de la
               fila se mueve, la zanja queda FIJADA: sus celdas, bloqueadas
               (W['bloqueadas']) hasta el ciclo siguiente (ninguna fila vuelve a
               cavarlas ni a profundizarlas); una fila que pasa por ellas solo
               cava en sus celdas libres, y para cavar otra vez tiene que volver
               a estar parada Tfila. Una fila que se mueve antes de Tfila no
               cava. Zanjajuego apagado: la fila hace solo su escision.
  CAIDA        si la celda del monstruo pasa a ser zanja, o entra en una, cae:
               acum 0, Tamanoinicial, forma pequena. Sigue buscando desde el
               fondo: entrar en una zanja o salir de ella le cuesta Costezanja
               veces mas. Cae otra vez (de zanja a zanja) solo con acum > 0.
  AGUA         una zanja de Profundidadagua conchas o mas aflora agua; una
               vecina de un rio o de un lago (fase 13) tambien se llena. En cada
               paso de juego: + Ritmoagua escalones y, hacia cada zanja vecina
               con menos agua, + Desbordeagua, sin pasar de la capacidad
               (profundidad x Ocupacionmax). El agua es muro para el monstruo; si
               su celda llega a Ahoga de la zanja llena, se ahoga y Esperamonstruo
               s despues aparece otro. En modo juego el agua de juego entra en
               las escisiones; fuera de el, rios y lagos siguen sin llenarlas.
  ENTIERRO     al enterrar, las zanjas, el agua y las bloqueadas se quedan en el
               mundo enterrado (la concha nueva las tapiza).
  LEYENDA      ZANJA    3 celdas   prof 4   agua 60%   monstruo dentro

OPERADORES (en /project1/FASE1)
-------------------------------
  agua_juego, i_agua_juego   Geometry COMP instanciado (el agua de cada zanja,
               hasta su nivel), con mat_piel_agua (la familia agua de la fase 13).

PROBAR
------
  Con varias conchas (Forzarciclo), Modojuego, Simmonstruo y una fila de 3
  (Simfila 3, Simformarfila) a su paso: cae y vuelve a media celda. Con 4
  personas (profundidad 4) la zanja aflora agua, se llena y el monstruo muere;
  a los Esperamonstruo s aparece otro. Simzanja: una zanja de Simfila celdas
  desde Simcasilla, sin esperar a Tfila.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase34_zanjas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase34 v1  (el devorador: zanjas de las filas, caida del monstruo y agua)'
banner(VERSION)

base = require_base(34)
motor = install_core(base, CARPETA, 34)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase34)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase34')
add_par(base, page, 'toggle', 'Zanjajuego', 'Zanja de juego', True)
add_par(base, page, 'int', 'Profundidadagua', 'Profundidad del agua (conchas)', 4, 1, 12, clamp=True)
add_par(base, page, 'int', 'Ritmoagua', 'Ritmo del agua (escalones por paso)', 4, 1, 16, clamp=True)
add_par(base, page, 'int', 'Desbordeagua', 'Desborde del agua (escalones por paso)', 2, 1, 16, clamp=True)
add_par(base, page, 'float', 'Ahoga', 'Nivel que ahoga (fraccion de la zanja)', 0.5, 0.1, 1.0, clamp=True)
add_par(base, page, 'pulse', 'Simzanja', 'Simular zanja')
ok('parametros de la fase 34: Zanjajuego, Profundidadagua 4, Ritmoagua 4, Desbordeagua 2, Ahoga 0,5, Simzanja')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

if base.op('mat_piel_agua') is None:
    fail('mat_piel_agua: no esta (es de la fase 13)')
geo = make_instanced(base, 'agua_juego', 440, 2700, 'mat_piel_agua')
if not setp_any(geo, ['instancea'], 'a'):
    fail('agua_juego no lee la rugosidad: Instance 2 -> Color A = a')
if has_par(base, 'Materialrespaldo'):
    setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_agua'")
ok('agua_juego: el agua de las zanjas, hasta su nivel (familia agua)')

set_render(base)

leeme(base, 34, """FASE 34 - ZANJAS Y AGUA
  En modo juego, una fila parada Tfila cava una zanja en todas las celdas
  que miran a sus casillas (personas x Conchasporpersona, hasta el nucleo),
  como la escision: vacia, sin cicatriz, la concha siguiente la tapiza. Si
  alguien se mueve, la zanja queda fijada y sus celdas bloqueadas hasta el
  ciclo siguiente. El monstruo cae al entrar (acum 0, media celda); entrar o
  salir cuesta Costezanja. Una zanja de Profundidadagua conchas, o vecina de
  un rio o un lago, se llena (Ritmoagua por paso; Desbordeagua a las vecinas
  mas bajas); el agua es muro y por encima de Ahoga lo ahoga. Simzanja.
  Geometria agua_juego (mat_piel_agua).""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS34 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Modofila', 'Conchasporpersona', 'Simbalance', 'Colapsoon', 'Temaenciclo',
          'Tema', 'Modojuego', 'Umbralaparicion', 'Zanjajuego', 'Colmatacion')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS34)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _celdas(m, W, c, casillas):
    out = []
    for k in casillas:
        x = m.celda_de_casilla(W, c, k)
        if x not in out:
            out.append(x)
    return out


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # el monstruo, solo cuando la prueba lo pone
    S = SalaJuego(base, m, absTime.seconds + 1800.0)
    W, c = S.nuevo(8)
    TF = c['t_fila']
    cols, filas = m.rejilla_sala(c)
    k0 = 4 * cols + 2
    linea = [k0, k0 + 1, k0 + 2]
    celdas = _celdas(m, W, c, linea)

    # 1. en modo juego corta en todas sus celdas; fuera de el, solo en el origen
    S.camara(W, c, linea, seg=TF + 0.3)
    J = W['juego']
    e = W['escisiones'][-1] if W['escisiones'] else None
    todas = sorted(J['zanjas']) == sorted(celdas) and all(J['zanjas'][x] == 3 for x in celdas) \
        and all(len(W['cols'][x]) == 5 for x in celdas)
    W, c = S.nuevo(8, juego=False)
    S.camara(W, c, linea, seg=TF + 0.3)
    e2 = W['escisiones'][-1] if W['escisiones'] else None
    resto = [x for x in celdas if e2 is None or x != e2['origen']]
    t.check('en modo juego la fila corta en todas sus celdas (%d, 3 conchas cada una, con la escision en el '
            'origen); fuera de el, solo en el origen' % len(celdas),
            todas and e is not None and e['origen'] in celdas and e2 is not None and 'juego' not in W
            and len(W['cols'][e2['origen']]) == 5 and all(len(W['cols'][x]) == 8 for x in resto),
            'celdas %s' % celdas)

    # 2. una fila que se mueve antes de Tfila no cava
    W, c = S.nuevo(8)
    J = W['juego']
    otra = [k0, k0 + 1, k0 + 1 + cols]
    S.camara(W, c, linea, seg=TF - 2.0)
    S.camara(W, c, otra, seg=TF - 1.0)
    nada = (len(J['zanjas']), len(W['escisiones']))
    S.camara(W, c, otra, seg=1.3)
    t.check('una fila que se mueve antes de Tfila no cava (el tiempo vuelve a empezar al moverse)',
            nada == (0, 0) and len(J['zanjas']) > 0 and len(W['escisiones']) == 1, '%s' % (nada,))

    # 3. fijada: no se vuelve a cavar hasta Forzarciclo; una fila nueva que la cruza, solo en las libres
    W, c = S.nuevo(8)
    J = W['juego']
    S.camara(W, c, linea, seg=TF + 0.3)
    S.camara(W, c, otra, n=2)                    # alguien se mueve: la zanja queda fijada
    bloq = sorted(W.get('bloqueadas') or {})
    S.camara(W, c, [], n=3)
    cruza = [k0 + 1, k0 + 2, k0 + 3, k0 + 4, k0 + 5]
    S.camara(W, c, cruza, seg=TF + 0.3)
    nuevas = _celdas(m, W, c, cruza)
    libres = [x for x in nuevas if x not in bloq]
    ya = [x for x in nuevas if x in bloq]
    t.check('al moverse alguien la zanja queda fijada: sus celdas, bloqueadas; una fila nueva de 5 que la '
            'cruza solo cava (a 5 conchas) en sus celdas libres',
            bloq == sorted(celdas) and libres and ya and all(J['zanjas'][x] == 3 and len(W['cols'][x]) == 5 for x in ya)
            and all(J['zanjas'][x] == 5 for x in libres), 'bloqueadas %s, libres %s' % (bloq, libres))
    m.on_pulse('Forzarciclo')
    W = m.world()
    t.check('Forzarciclo: el ciclo siguiente, sin bloqueadas ni zanjas de juego (las tapiza la concha nueva)',
            'bloqueadas' not in W and not W['juego']['zanjas'])

    # 4. la caida y el coste
    W, c = S.nuevo(8)
    J = W['juego']
    a = celdas[0]
    mo = m.aparecer(W, c, S.now, a)
    mo['acum'] = 4
    m.actualizar_tam(c, mo)
    m.cavar_zanja(W, c, a, 2, S.now)
    caida = (mo['estado'], mo['acum'], mo['tam'])
    v = m.NEIGH[a][0]
    w_ = next(x for x in m.NEIGH[v] if x != a and x not in m.NEIGH[a])
    m.cavar_zanja(W, c, v, 2, S.now)
    dist, _ = m.dijkstra_mon(W, c, w_)
    m.entrar_celda(W, c, mo, v, S.now)
    sin = mo['caidas']
    mo['acum'] = 2
    m.entrar_celda(W, c, mo, a, S.now)
    t.check('caida: su celda pasa a ser zanja -> cae, acum 0 y Tamanoinicial; de zanja a zanja solo cae otra '
            'vez con acum > 0; entrar en una zanja cuesta Costezanja',
            caida == ('cae', 0, c['tam_inicial']) and sin == 1 and mo['caidas'] == 2 and mo['acum'] == 0
            and abs(dist[v] - c['coste_zanja']) < 1e-9, '%s, coste %.1f' % (caida, dist.get(v, -1)))

    # 5. el agua
    W, c = S.nuevo(8)
    J = W['juego']
    a = celdas[0]
    v = m.NEIGH[a][0]
    m.cavar_zanja(W, c, a, 4, S.now)
    m.cavar_zanja(W, c, v, 3, S.now)
    S.pasos(W, c, 1)
    p1 = (J['agua'].get(a, 0), J['agua'].get(v, 0))
    S.pasos(W, c, 30)
    p30 = (J['agua'].get(a, 0), J['agua'].get(v, 0))
    om = int(c['ocupacion_max'])
    t.check('aflora con profundidad >= Profundidadagua (4 por paso) y desborda a 2 hacia la zanja vecina mas '
            'baja; una de 3 no aflora; nunca pasa de la capacidad (profundidad x Ocupacionmax)',
            p1 == (4, 2) and p30 == (4 * om, 3 * om), '%s -> %s' % (p1, p30))
    base.par.Tema = 'naturaleza'
    W, c = S.nuevo(8)
    J = W['juego']
    try:
        m.prueba_rio(W, c, m.cell_note(celdas[0]), S.now)
    except Exception:
        pass
    dulce = m.celdas_agua_dulce(W, c)
    x = next((x for x in range(m.N) if x not in dulce and W['occ'][x] == 0 and any(j in dulce for j in m.NEIGH[x])),
             None)
    if x is not None:
        m.cavar_zanja(W, c, x, 1, S.now)
        S.pasos(W, c, 1)
    t.check('una zanja poco honda (1 concha) vecina de un rio de la fase 13 tambien se llena',
            x is not None and J['agua'].get(x, 0) == min(4, om), '%d celdas de rio, zanja %s' % (len(dulce), x))

    # 6. se ahoga y reaparece
    base.par.Umbralaparicion = 0.0
    W, c = S.nuevo(8)
    J = W['juego']
    a = celdas[0]
    m.cavar_zanja(W, c, a, 4, S.now)
    mo = m.aparecer(W, c, S.now, a)
    n0 = mo['n']
    S.pasos(W, c, 3)
    vivo = J['mon']['estado']
    S.pasos(W, c, 1)
    muerto = (J['mon']['estado'], J['agua'].get(a, 0))
    t0 = J['mon']['t_muerte']
    m.juego_avanzar(W, c, t0 + c['espera_monstruo'] - 0.2, 0.0)
    antes = J['mon']['estado']
    m.juego_avanzar(W, c, t0 + c['espera_monstruo'] + 0.1, 0.0)
    t.check('el monstruo muere con el agua por encima de Ahoga (16 de 32 a los 4 pasos) y reaparece tras '
            'Esperamonstruo', vivo != 'muere' and muerto == ('muere', 16) and antes == 'muere'
            and J['mon']['estado'] == 'aparece' and J['mon']['n'] == n0 + 1, '%s, %s' % (vivo, muerto))

    # 7. fuera del modo juego, los rios y lagos siguen sin entrar en las escisiones
    W, c = S.nuevo(8, juego=False)
    S.camara(W, c, linea, seg=TF + 0.3)
    lagos = m.cauces(W, c)['lagos']
    t.check('fuera del modo juego, ni agua de juego ni lagos en las escisiones',
            'juego' not in W and W['escisiones'] and all(not m.es_escision(W, x) for x in lagos))
    base.par.Tema = 'naturaleza'

    # 8. Simzanja, la geometria y la leyenda
    base.par.Umbralaparicion = 1.0
    W, c = S.nuevo(8)
    J = W['juego']
    base.par.Simcasilla = k0
    base.par.Simfila = 4
    m.on_pulse('Simzanja')
    W = m.world()
    J = W['juego']
    sz = _celdas(m, W, m.cfg(), m.casillas_fila_sim(m.cfg(), k0, 4))
    c = m.cfg()
    mo = m.aparecer(W, c, S.now, sz[0])
    S.pasos(W, c, 1)
    inst = m.build_instances(W, c, S.now)
    leg = m._legend_zanja(W, c)
    t.check('Simzanja: zanja de Simfila (4) celdas desde Simcasilla, de 4 conchas, fijada en el acto',
            sorted(J['zanjas']) == sorted(sz) and all(J['zanjas'][x] == 4 for x in sz)
            and sorted(W['bloqueadas']) == sorted(sz), str(sz))
    t.check('el agua de las zanjas en agua_juego; la linea ZANJA',
            len(inst.get('agua_juego', [])) == len(sz) and base.op('agua_juego') is not None
            and leg.startswith('  ZANJA    %d celdas   prof 4   agua ' % len(sz)) and 'monstruo dentro' in leg,
            leg.strip())


run_test(base, prueba)
print('  Ahora: Modojuego, Simmonstruo y una fila (Simfila 3, Simformarfila) a su paso: cae. Con 4')
print('  personas la zanja se llena y el monstruo se ahoga; Simzanja la cava sin esperar.')
print('=' * 66)
