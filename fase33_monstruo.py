"""
=============================================================================
ESTRATOS - FASE 33: EL MONSTRUO Y LOS BROTES DEL MAL
=============================================================================
Requiere la fase 32. En modo juego, el monstruo aparece, busca, devora, crece,
deja brotes del mal y reaparece. Los brotes crecen con los triggers como
cualquier celda.

QUE HACE
--------
  APARICION    cuando la fraccion de la cara visible construida por el publico
               llega a Umbralaparicion (0,25, D2), en la celda vacia de la cara
               visible mas cercana al borde por el que entran las celdas con el
               giro (desempate _hash01), con Tamanoinicial (media celda).
  OBJETIVO     cada Recalculo pasos de juego y siempre que vacia una celda: un
               Dijkstra por las vecinas (entrar en una zanja cuesta Costezanja;
               el agua es muro) y el objetivo de mayor ocupacion / (1 + coste).
               El pequeno no elige fusiones ni coronas (los umbrales de la fase
               4). Con Verobjetivo, un tocon en la celda objetivo (D6).
  MOVIMIENTO   una celda por el camino cada Pasomonstruo semicorcheas
               (Pasogrande en forma grande). Sin objetivo, quieto.
  DEVORAR      en su objetivo, en cada paso de juego, Ritmodevora escalones
               (Ritmogrande en forma grande) con _undo_note: cae primero lo
               ultimo construido (satelites, coronas, altura), como en la
               erosion. No pasa por erosion(): no cuenta en el balance de la
               fase 23. Cada escalon suma 1 a acum.
  CRECER       tam = Tamanoinicial + (1 - Tamanoinicial) x min(1, acum /
               Ocupacionmax). En 1, forma grande: mas rapido, devora a
               Ritmogrande y ya puede con fusiones y coronas.
  BROTE        la celda que devora hasta vaciarla recibe un brote del mal:
               ocupacion 1, especie mal. Crece con los triggers de los
               secuenciadores como cualquier celda (la presencia del publico
               encima sube la probabilidad de que prendan, fase 22); no hibrida.
               Su desborde cae en vecinas vacias o del mal; sobre una celda del
               publico se pierde (D4).
  MUERTE       muere ahogado (fase 34); Esperamonstruo s despues aparece otro.
  VISUAL       PROVISIONAL. El monstruo (cuerpo y ojos) va en su COMP
               'monstruo', que sigue el giro del planeta: se cambia por un
               sprite tipo arcade de 8 bits sin tocar la logica. Los brotes
               conservan la geometria de su especie de origen y llevan un velo
               de la familia de material nueva mal (mat_piel_mal: casi negro,
               croma baja y brillo propio debil). El tocon, en su COMP 'tocon'.
  LEYENDA      MONSTRUO #3  devora  celda 40 -> 52  tam 0.62  acum 5/8  x2

OPERADORES (en /project1/FASE1)
-------------------------------
  monstruo, tocon, brotes_mal   Geometry COMP instanciados (i_monstruo,
               i_tocon, i_brotes_mal), con mat_piel_mal (familia 9 del shader
               de la piel).

PROBAR
------
  Modojuego. Sembrar hasta corona en una celda y hasta 3 en otra; Simmonstruo
  (aparece en Simceldamon): el pequeno va a la de 3, no a la corona. La
  devora a 2 escalones por negra, deja un brote y crece. Sembrar la celda del
  brote: crece como mal. Dejar que devore 8 escalones: forma grande, mas
  rapido, 3 por negra, y va a por la corona.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase33_monstruo.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase33 v2  (autoprueba: con la fase 38, el cuerpo provisional con Spritemonstruo apagado)'
banner(VERSION)

base = require_base(33)
motor = install_core(base, CARPETA, 33)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase33)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase33')
add_par(base, page, 'float', 'Umbralaparicion', 'Umbral de aparicion', 0.25, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Tamanoinicial', 'Tamano inicial (celdas)', 0.5, 0.1, 1.0, clamp=True)
add_par(base, page, 'int', 'Ocupacionmax', 'Ocupacion maxima', 8, 4, 16, clamp=True)
add_par(base, page, 'int', 'Ritmodevora', 'Ritmo de devorar (escalones por paso)', 2, 1, 10, clamp=True)
add_par(base, page, 'int', 'Ritmogrande', 'Ritmo grande (escalones por paso)', 3, 1, 10, clamp=True)
add_par(base, page, 'int', 'Pasomonstruo', 'Paso del monstruo (semicorcheas)', 16, 1, 64, clamp=True)
add_par(base, page, 'int', 'Pasogrande', 'Paso grande (semicorcheas)', 8, 1, 64, clamp=True)
add_par(base, page, 'float', 'Costezanja', 'Coste en zanja', 2.0, 1.0, 5.0, clamp=True)
add_par(base, page, 'int', 'Recalculo', 'Recalculo de objetivo (pasos)', 4, 1, 32, clamp=True)
add_par(base, page, 'float', 'Esperamonstruo', 'Espera de reaparicion (s)', 8.0, 0.0, 120.0, clamp=True)
add_par(base, page, 'toggle', 'Verobjetivo', 'Ver objetivo', True)
add_par(base, page, 'pulse', 'Simmonstruo', 'Simular monstruo')
add_par(base, page, 'int', 'Simceldamon', 'Celda del monstruo simulado', 0, 0, m.N - 1)
ok('pagina Fase33: Umbralaparicion 0,25, Tamanoinicial 0,5, Ocupacionmax 8, Ritmodevora 2, Ritmogrande 3, '
   'Pasomonstruo 16, Pasogrande 8, Costezanja 2, Recalculo 4, Esperamonstruo 8 s, Verobjetivo, Simmonstruo, '
   'Simceldamon')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

materiales_piel(base)                   # comun v82: con la familia mal (mat_piel_mal)
if base.op('mat_piel_mal') is None:
    fail('mat_piel_mal: no pude crearlo')
for nombre, x, sop in (('monstruo', -220, 'sphere'), ('tocon', 0, 'box'), ('brotes_mal', 220, 'sphere')):
    geo = make_instanced(base, nombre, x, 2700, 'mat_piel_mal', sop=sop, quiet=True)
    if not setp_any(geo, ['instancea'], 'a'):
        fail('%s no lee la parte de cada pieza: Instance 2 -> Color A = a' % nombre)
    if has_par(base, 'Materialrespaldo'):
        setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_mal'")
ok('monstruo, tocon y brotes_mal: geometrias propias (provisionales) con mat_piel_mal, giran con el planeta')

set_render(base)

leeme(base, 33, """FASE 33 - EL MONSTRUO Y LOS BROTES DEL MAL
  En modo juego, el monstruo aparece al construirse Umbralaparicion de la
  cara visible, por el borde de entrada del giro. Objetivo (cada Recalculo
  pasos o al vaciar una celda): Dijkstra, mayor ocupacion / (1 + coste); el
  pequeno no come fusiones ni coronas. Avanza una celda cada Pasomonstruo
  semicorcheas; devora Ritmodevora escalones por paso (lo ultimo construido
  primero; fuera del balance). tam crece con lo devorado hasta 1 en
  Ocupacionmax: forma grande (Pasogrande, Ritmogrande, come coronas). Cada
  celda vaciada deja un brote del mal (occ 1), que crece como cualquier celda
  y no desborda en el publico. Esperamonstruo s tras morir, otro.
  Geometrias monstruo, tocon (Verobjetivo) y brotes_mal: mat_piel_mal.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS33 = ('Fuente', 'Simcasilla', 'Probllegada', 'Tparada', 'Temaenciclo', 'Modojuego', 'Duracionronda',
          'Umbralaparicion', 'Simceldamon', 'Simbalance', 'Colapsoon', 'Loncentral', 'Spritemonstruo')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS33)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ, s=1, par=-1):
    W['occ'][i] = occ
    W['carga'][i] = 0
    W['sp'][i] = s
    W['own'][i] = s if s in (m.GEO, m.ARQ) else m.GEO      # un brote conserva la especie de origen
    W['traza'][i] = m._bit(W['own'][i])
    W['par'][i] = par
    W['h'][i] = m.height_for(m.cfg(), occ)


def _a_distancia(m, W, c, a, d, fuera=()):
    dist, _ = m.dijkstra_mon(W, c, a)
    return min(x for x in dist if abs(dist[x] - d) < 1e-9 and x not in fuera)


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # que no aparezca solo mientras se prepara el mundo
    if has_par(base, 'Spritemonstruo'):     # v2: con la fase 38, se prueba el cuerpo provisional
        base.par.Spritemonstruo = False
    S = SalaJuego(base, m, absTime.seconds + 1500.0)

    # 1. el objetivo
    W, c = S.nuevo(4)
    J = W['juego']
    a = 40 if m.N > 50 else m.N // 2
    b = _a_distancia(m, W, c, a, 1)
    d = _a_distancia(m, W, c, a, 2)
    co = _a_distancia(m, W, c, a, 3)
    _poner(m, W, b, 3)
    _poner(m, W, d, 6)
    _poner(m, W, co, int(c['th_crown']))
    mo = m.aparecer(W, c, S.now, a)
    peq = mo['objetivo']
    mo['acum'] = int(c['ocupacion_max'])
    m.actualizar_tam(c, mo)
    gr = m.recalcular_objetivo(W, c, mo, S.now)
    W['occ'][d] = 0
    mo['acum'] = 0
    m.actualizar_tam(c, mo)
    peq2 = m.recalcular_objetivo(W, c, mo, S.now)
    t.check('el objetivo es el de mayor ocupacion / (1 + coste): 6 a 2 celdas antes que 3 al lado; el '
            'pequeno nunca elige la corona (a 3 celdas), el grande si (9 / 4)',
            peq == d and peq2 == b and gr == co and m.objetivo(W, c, mo)[1][-1] == b,
            'pequeno %s, sin la de 6 %s, grande %s' % (peq, peq2, gr))
    _poner(m, W, d, int(c['th_fusion']))
    t.check('el pequeno tampoco elige una fusion', m.recalcular_objetivo(W, c, mo, S.now) == b
            and not m.comestible(W, c, mo, d) and not m.comestible(W, c, mo, co))

    # 2. devorar: Ritmodevora escalones por paso de juego, sin triggers, al reves de la construccion
    W, c = S.nuevo(4)
    J = W['juego']
    _poner(m, W, b, 3)
    sat = next(j for j in m.NEIGH[b] if W['occ'][j] == 0)
    _poner(m, W, sat, 1, par=b)
    bal = list(m.sala_de(W)['bal'])
    hits = dict(W['hits'])
    mo = m.aparecer(W, c, S.now, b)
    S.semis(W, c, int(c['paso_juego']))
    p1 = (W['occ'][b], W['occ'][sat], mo['acum'], mo['estado'])
    S.pasos(W, c, 1)
    t.check('en su objetivo devora Ritmodevora (2) escalones por paso de juego, sin ningun trigger: primero el '
            'satelite y luego la altura', p1 == (2, 0, 2, 'devora') and W['hits'] == hits and mo['acum'] == 4,
            '%s' % (p1,))
    t.check('la celda vaciada recibe un brote: ocupacion 1 y especie mal (conserva la especie de origen para la '
            'geometria) y busca otro objetivo',
            W['occ'][b] == 1 and W['sp'][b] == m.MAL and W['own'][b] == m.GEO and mo['objetivo'] != b
            and J['brotes'] == 1, 'occ %d sp %d acum %d' % (W['occ'][b], W['sp'][b], mo['acum']))
    t.check('devorar no cuenta en el balance de la fase 23', m.sala_de(W)['bal'] == bal)

    # 3. el brote crece con triggers simulados, sin hibridar
    o0 = W['occ'][b]
    for k in range(int(c['cost_max']) * 3):
        m.note_on(W, c, m.ARQ if k % 2 else m.GEO, m.cell_note(b), 100, S.now)
    t.check('el brote crece con los triggers de los dos secuenciadores como cualquier celda y sigue siendo del '
            'mal (no hibrida)', W['occ'][b] > o0 and W['sp'][b] == m.MAL, 'occ %d' % W['occ'][b])

    # 4. el desborde del mal no entra en el publico
    W, c = S.nuevo(2)
    i = a
    nb = m.NEIGH[i]
    _poner(m, W, i, int(c['th_branch']), m.MAL)
    W['own'][i] = m.GEO
    pub = nb[0]
    _poner(m, W, pub, 2)
    k = next(v for v in range(128) if nb[(v + W['occ'][i]) % len(nb)] == pub)
    m.overflow(W, c, i, m.GEO, k, S.now)
    perdido = W['ev']['desborde']['tipo']
    vacia = nb[1]
    k2 = next(v for v in range(128) if nb[(v + W['occ'][i]) % len(nb)] == vacia)
    m.overflow(W, c, i, m.GEO, k2, S.now)
    t.check('el desborde del mal: sobre una celda del publico se pierde (sin hibridar); en una vacia, un '
            'satelite del mal', perdido == 'perdido' and W['occ'][pub] == 2 and W['sp'][pub] == m.GEO
            and W['carga'][pub] == 0 and W['sp'][vacia] == m.MAL and W['par'][vacia] == i,
            '%s, %s' % (perdido, W['ev']['desborde']['tipo']))

    # 5. crecer y la forma grande
    W, c = S.nuevo(4)
    _poner(m, W, b, 12)
    mo = m.aparecer(W, c, S.now, b)
    pequeno = (mo['objetivo'], m.paso_mon(c, mo))
    tams = []
    for ac in (2, 4, 6, 8):
        mo['acum'] = ac
        tams.append((ac, round(m.actualizar_tam(c, mo), 3)))
    grande = m.grande(mo)
    m.recalcular_objetivo(W, c, mo, S.now)
    occ0 = W['occ'][b]
    S.pasos(W, c, 1)
    t.check('tam crece con acum (0,5 + 0,5 x acum / 8) y llega a 1 en Ocupacionmax; en forma grande devora '
            'Ritmogrande (3) por paso y avanza cada Pasogrande semicorcheas',
            tams == [(2, 0.625), (4, 0.75), (6, 0.875), (8, 1.0)] and grande and occ0 - W['occ'][b] == 3
            and mo['acum'] == 11 and pequeno == (None, int(c['paso_monstruo'])) and mo['objetivo'] == b
            and m.paso_mon(c, mo) == int(c['paso_grande']), '%s, %d' % (tams, occ0 - W['occ'][b]))

    # 6. el movimiento: una celda cada Pasomonstruo semicorcheas
    W, c = S.nuevo(4)
    lejos = _a_distancia(m, W, c, a, 3)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    S.semis(W, c, int(c['paso_monstruo']) - 1)
    quieto = mo['celda']
    S.semis(W, c, 1)
    t.check('avanza una celda por el camino cada Pasomonstruo (16) semicorcheas', quieto == a
            and mo['celda'] != a and mo['celda'] in m.NEIGH[a] and mo['objetivo'] == lejos,
            '%s -> %s' % (quieto, mo['celda']))

    # 7. la aparicion: la cara visible construida y el borde de entrada
    base.par.Umbralaparicion = 0.25
    W, c = S.nuevo(4)
    vis = m.cara_visible(c)
    import math
    pon = sorted(vis)[:int(math.ceil(len(vis) * 0.25 - 1e-9))]
    for x in pon[:-1]:
        _poner(m, W, x, 2)
    S.semis(W, c, 1)
    antes = W['juego']['mon']['estado']
    _poner(m, W, pon[-1], 2)
    esperada = m.celda_aparicion(W, c, vis)
    S.semis(W, c, 1)
    mo = W['juego']['mon']
    lon = lambda x: (m.lonlat_celda(x)[1] - c['lon_central'] + 180.0) % 360.0 - 180.0
    libres = [x for x in vis if W['occ'][x] == 0 or x == mo['celda']]
    t.check('aparece al llegar Umbralaparicion de la cara visible construida (no antes), en la celda vacia de '
            'la cara visible mas cercana al borde de entrada del giro, con Tamanoinicial',
            antes == 'espera' and mo['estado'] in ('aparece', 'busca', 'devora') and mo['celda'] == esperada
            and mo['celda'] in vis and abs(mo['tam'] - c['tam_inicial']) < 1e-9
            and lon(mo['celda']) >= max(lon(x) for x in libres) - 1e-6 and mo['n'] == 1,
            'celda %s' % mo['celda'])
    base.par.Simceldamon = 7
    m.on_pulse('Simmonstruo')
    W = m.world()
    t.check('Simmonstruo: aparece ya, en Simceldamon', W['juego']['mon']['celda'] == 7
            and W['juego']['mon']['n'] == 2)

    # 8. determinismo
    def partida(t0):
        S2 = SalaJuego(base, m, t0)
        W, c = S2.nuevo(4)
        for x, o in ((b, 3), (d, 6), (co, 10), (lejos, 4)):
            S2.sembrar(W, c, x, o)
        m.aparecer(W, c, S2.now, a)
        for k in range(12):
            S2.pasos(W, c, 4)
            m.note_on(W, c, m.GEO, m.cell_note(b), 100, S2.now)
        J = W['juego']
        return copy.deepcopy((W['occ'], W['sp'], J['mon'], J['recuento'], J['brotes']))
    r1 = partida(absTime.seconds + 3000.0)
    r2 = partida(absTime.seconds + 3000.0)
    t.check('dos ejecuciones con la misma sesion simulada dan el mismo resultado (determinismo)',
            r1 == r2 and r1[4] > 0, 'brotes %d' % r1[4])

    # 9. lo visual y la leyenda
    W, c = S.nuevo(4)
    _poner(m, W, b, 3)
    _poner(m, W, d, 2, m.MAL)
    mo = m.aparecer(W, c, S.now, a)
    inst = m.build_instances(W, c, S.now)
    leg = m._legend_monstruo(W, c)
    t.check('el monstruo (cuerpo y ojos), el tocon en su objetivo y el velo de cada brote del mal, en sus '
            'geometrias', len(inst.get('monstruo', [])) == 3 and len(inst.get('tocon', [])) == 1
            and len(inst.get('brotes_mal', [])) == 1 and inst['brotes_mal'][0][9:12] == list(m.COL_MAL)
            and all(base.op(n) is not None for n in ('monstruo', 'tocon', 'brotes_mal', 'i_monstruo')),
            '%d %d %d' % (len(inst.get('monstruo', [])), len(inst.get('tocon', [])), len(inst.get('brotes_mal', []))))
    base.par.Verobjetivo = False
    sin = m.build_instances(W, m.cfg(), S.now).get('tocon', [])
    base.par.Verobjetivo = True
    t.check('Verobjetivo apagado: sin tocon', sin == [])
    t.check('la linea MONSTRUO: numero, estado, celda -> objetivo, tam, acum y ritmo',
            leg.startswith('  MONSTRUO #1  ') and ' celda %d -> %d  tam 0.50  acum 0/8  x2' % (a, mo['objetivo'])
            in leg, leg.strip())
    t.check('el mal, en la familia 9 del shader de la piel', 'mal' in FAMILIAS_PIEL
            and FAMILIAS_PIEL.index('mal') == 9 and 'bool malo = fam > 8.5' in PIEL_PIXEL)


run_test(base, prueba)
print('  Ahora: Modojuego; Sembrar hasta corona en una celda y hasta 3 en otra; Simmonstruo: el pequeno')
print('  va a la de 3. Deja que devore 8 escalones: forma grande y a por la corona.')
print('=' * 66)
