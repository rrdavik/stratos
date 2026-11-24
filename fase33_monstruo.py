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
  MOVIMIENTO   una celda por el camino cada Pasomonstruo semicorcheas (32: 8
               negras; Pasogrande 16, 4 negras, en forma grande; en zanja, x
               Costezanja). Sin objetivo, quieto. v6: con Saltosmonstruo avanza a
               SALTOS DE MEDIA CELDA: en su celda hasta la mitad, a media celda
               desde la mitad (sigue siendo de su celda: alli le cuentan la zanja,
               el pisoton, el cerco y el agua) y en la siguiente al llegar. Cada
               salto dura Tiemposalto s (0,15) con un bote de Botesalto x su alto
               (0,15). Apagado, se desliza como antes.
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
  LEYENDA      MONSTRUO #3  busca  celda 40 -> 52  tam 0.62  acum 5/8  x1  paso 5/8
               (paso: negras hechas hacia la celda siguiente / las que cuesta)

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

  v10 (motor v144): el monstruo acaba la celda que devora. Antes, cada
  Recalculo pasos volvia a elegir presa tambien mientras comia y, en un mundo
  denso, dejaba la celda a medias por una vecina llena: picaba de todo, crecia
  y no dejaba brotes del mal.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase33_monstruo.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase33 v10  (motor v144: el monstruo acaba la celda que devora antes de buscar otra)'
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
# v5: la mitad de dano. Multiplica Ritmodevora y Ritmogrande (2 x 0,5 = 1 escalon por paso;
# 3 x 0,5 = 1,5: alterna 1 y 2). Sin publico, el monstruo ganaba la partida entera
add_par(base, page, 'float', 'Danomonstruo', 'Dano del monstruo (x ritmo)', 0.5, 0.0, 2.0, clamp=True)
add_par(base, page, 'int', 'Pasomonstruo', 'Paso del monstruo (semicorcheas)', 32, 1, 128, clamp=True)
add_par(base, page, 'int', 'Pasogrande', 'Paso grande (semicorcheas)', 16, 1, 128, clamp=True)
# v4: GENoZilla anda un tercio mas lento (16 -> 24 y 8 -> 12 semicorcheas por celda). Un
# proyecto con los valores de antes pasa a los nuevos una sola vez; el tope sube a 128
# v6: mas lento aun: 8 negras por celda (32 semicorcheas) y 4 en grande (16). Una sola vez
# tambien: 16 -> 24 -> 32 y 8 -> 12 -> 16; lo cambiado a mano (20, por ejemplo) se respeta
for _nm, _viejo, _nuevo in (('Pasomonstruo', 16, 24), ('Pasogrande', 8, 12),
                            ('Pasomonstruo', 24, 32), ('Pasogrande', 12, 16)):
    renew_default(base, _nm, _viejo, _nuevo)
    try:
        _p = getattr(base.par, _nm)
        if float(_p.max) < 128:
            _p.normMax = 128
            _p.max = 128
    except Exception:
        pass
add_par(base, page, 'float', 'Costezanja', 'Coste en zanja', 2.0, 1.0, 5.0, clamp=True)
# v6: a saltos de media celda (pos_monstruo del motor v126); apagado, el deslizamiento de antes
add_par(base, page, 'toggle', 'Saltosmonstruo', 'Saltos de media celda', True)
add_par(base, page, 'float', 'Tiemposalto', 'Tiempo de cada salto (s)', 0.15, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Botesalto', 'Bote del salto (x alto)', 0.15, 0.0, 1.0, clamp=True)
add_par(base, page, 'int', 'Recalculo', 'Recalculo de objetivo (pasos)', 4, 1, 32, clamp=True)
add_par(base, page, 'float', 'Esperamonstruo', 'Espera de reaparicion (s)', 8.0, 0.0, 120.0, clamp=True)
add_par(base, page, 'toggle', 'Verobjetivo', 'Ver objetivo', True)
add_par(base, page, 'pulse', 'Simmonstruo', 'Simular monstruo')
add_par(base, page, 'int', 'Simceldamon', 'Celda del monstruo simulado', 0, 0, m.N - 1)
ok('pagina Fase33: Umbralaparicion 0,25, Tamanoinicial 0,5, Ocupacionmax 8, Ritmodevora 2, Ritmogrande 3, '
   'Danomonstruo 0,5 (v5: la mitad de dano), '
   'Pasomonstruo 32, Pasogrande 16 (v6: 8 y 4 negras por celda), Costezanja 2, '
   'Saltosmonstruo (v6: a saltos de media celda), Tiemposalto 0,15 s, Botesalto 0,15, '
   'Recalculo 4, Esperamonstruo 8 s, Verobjetivo, Simmonstruo, Simceldamon')

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
  semicorcheas (32: 8 negras), a saltos de media celda (Saltosmonstruo,
  Tiemposalto 0,15 s, Botesalto 0,15); devora Ritmodevora x Danomonstruo (0,5: la mitad) escalones
  por paso (lo ultimo construido primero; fuera del balance). tam crece con lo devorado hasta 1 en
  Ocupacionmax: forma grande (Pasogrande, Ritmogrande, come coronas). Cada
  celda vaciada deja un brote del mal (occ 1), que crece como cualquier celda
  y no desborda en el publico. Esperamonstruo s tras morir, otro.
  Geometrias monstruo, tocon (Verobjetivo) y brotes_mal: mat_piel_mal.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS33 = ('Fuente', 'Simcasilla', 'Probllegada', 'Tparada', 'Temaenciclo', 'Modojuego', 'Duracionronda',
          'Umbralaparicion', 'Simceldamon', 'Simbalance', 'Colapsoon', 'Loncentral', 'Spritemonstruo',
          'Especiemal', 'Saltosmonstruo', 'Pasomonstruo', 'Pasogrande')


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
    if has_par(base, 'Especiemal'):         # v3: con la fase 39, el velo provisional de los brotes
        base.par.Especiemal = False
    S = SalaJuego(base, m, absTime.seconds + 1500.0)

    # 1. el objetivo
    W, c = S.nuevo(4)
    J = W['juego']
    vis_ = m.cara_visible(m.cfg())      # motor v137: en la cara visible (en la oculta, el monstruo busca la luz)
    a = vis_[len(vis_) // 2] if vis_ else m.N // 2
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

    # 2. devorar: Ritmodevora x Danomonstruo escalones por paso de juego, sin triggers, al reves de la
    # construccion (v5: 2 x 0,5 = 1)
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
    p2 = (W['occ'][b], W['occ'][sat], mo['acum'])
    S.pasos(W, c, 2)
    t.check('en su objetivo devora Ritmodevora x Danomonstruo (2 x 0,5 = 1) escalon por paso de juego, sin '
            'ningun trigger: primero el satelite y luego la altura',
            p1 == (3, 0, 1, 'devora') and p2 == (2, 0, 2) and W['hits'] == hits and mo['acum'] == 4,
            '%s, %s' % (p1, p2))
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
    d1 = occ0 - W['occ'][b]
    S.pasos(W, c, 1)
    d2 = occ0 - W['occ'][b] - d1
    t.check('tam crece con acum (0,5 + 0,5 x acum / 8) y llega a 1 en Ocupacionmax; en forma grande devora '
            'Ritmogrande x Danomonstruo (3 x 0,5 = 1,5: 1 y 2) por paso y avanza cada Pasogrande (16) semicorcheas',
            tams == [(2, 0.625), (4, 0.75), (6, 0.875), (8, 1.0)] and grande and (d1, d2) == (1, 2)
            and mo['acum'] == 11 and pequeno == (None, int(c['paso_monstruo'])) and mo['objetivo'] == b
            and m.paso_mon(c, mo) == int(c['paso_grande']), '%s, %d y %d' % (tams, d1, d2))

    # 6. el movimiento: una celda cada Pasomonstruo semicorcheas (v6: 32, 8 negras; 16 en grande; el doble en
    # zanja) y, con Saltosmonstruo, dibujado a saltos de media celda
    W, c = S.nuevo(8)
    lejos = _a_distancia(m, W, c, a, 3)
    tiempos = {}
    for forma in ('pequeno', 'grande', 'zanja'):
        W, c = S.nuevo(8)
        _poner(m, W, lejos, 3)
        if forma == 'zanja':
            m.cavar_zanja(W, c, a, 2, S.now)        # sale del fondo de una zanja: Costezanja veces mas
        mo = m.aparecer(W, c, S.now, a)
        if forma == 'grande':
            mo['acum'] = int(c['ocupacion_max'])
            m.actualizar_tam(c, mo)
            m.recalcular_objetivo(W, c, mo, S.now)
        nx = mo['camino'][0] if mo['camino'] else None
        sitios = [m._pos_destino(W, c, d)[0] for d in ([a, None, 0.0], [a, nx, 0.5], [nx, None, 0.0])]
        traza, celdas, leyendas = [], [], {}
        for k in range(1, 2 * int(c['paso_monstruo']) * 2 + 1):
            S.semis(W, c, 1)
            p = m.pos_monstruo(W, c, mo, S.now + 1.0)[0]        # pasado el salto
            traza.append(next((q for q, x in enumerate(sitios) if m._len(m._add(p, x, -1.0)) < 1e-6), -1))
            celdas.append(mo['celda'])
            leyendas[k] = m._legend_monstruo(W, c)
            if mo['celda'] != a:
                break
        tiempos[forma] = (len(celdas), traza, celdas, leyendas)
    esperado = dict(pequeno=int(c['paso_monstruo']), grande=int(c['paso_grande']),
                    zanja=int(round(c['paso_monstruo'] * c['coste_zanja'])))
    t.check('v6: entra en la celda siguiente a las Pasomonstruo (32) semicorcheas exactas, no a las 31; en grande '
            'a las Pasogrande (16); saliendo de una zanja, el doble (64)',
            esperado == dict(pequeno=32, grande=16, zanja=64)
            and all(tiempos[f][0] == esperado[f] and tiempos[f][2][-2] == a and tiempos[f][2][-1] in m.NEIGH[a]
                    for f in esperado), '%s' % dict((f, tiempos[f][0]) for f in tiempos))
    t.check('v6: a saltos de media celda: la posicion dibujada es la de su celda hasta la semicorchea 15, media '
            'celda de la 16 a la 31 y la celda siguiente en la 32; en grande, el corte en la 8 (y la 16); en zanja, '
            'en la 32 (y la 64)',
            all(tiempos[f][1] == [0] * (esperado[f] // 2 - 1) + [1] * (esperado[f] // 2) + [2] for f in esperado),
            ' | '.join('%s %s' % (f, ''.join(str(x) for x in tiempos[f][1])) for f in tiempos))
    t.check('v6: la linea MONSTRUO cuenta el avance en negras: paso 5/8 en pequeno, 3/4 en grande, 11/16 en '
            'zanja', '  paso 5/8' in tiempos['pequeno'][3][20] and '  paso 3/4' in tiempos['grande'][3][12]
            and '  paso 11/16' in tiempos['zanja'][3][44] and '  paso 0/8' in tiempos['pequeno'][3][1],
            '%s | %s' % (tiempos['pequeno'][3][20].strip(), tiempos['zanja'][3][44].strip()))

    # el salto: Tiemposalto s, con una curva suave y un bote de Botesalto x su alto
    W, c = S.nuevo(4)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    nx = mo['camino'][0]
    S.semis(W, c, int(c['paso_monstruo']) // 2)
    t0, T = S.now, float(c['tiempo_salto'])
    pa, ph = m._pos_destino(W, c, [a, None, 0.0])[0], m._pos_destino(W, c, [a, nx, 0.5])[0]
    # v9: el bote al salir y al aterrizar, tambien a una millonesima (no == 0: el salto puede empezar
    # unas milmillonesimas antes de t0, el reloj de la prueba se acumula semicorchea a semicorchea).
    # v7: las posiciones a una milesima (la celda mide unas 4 unidades); v8: Tiemposalto y el bote a
    # una millonesima: TouchDesigner guarda los parametros en precision simple (0,15 es
    # 0,150000006) y con 1e-9 la prueba fallaba con todo bien
    cerca = lambda p, q: m._len(m._add(p, q, -1.0)) < 1e-3      # noqa: E731
    p0, pm, p1 = (m.pos_monstruo(W, c, mo, t0 + x * T)[0] for x in (0.0, 0.5, 1.0))
    b0, bm, b1 = (m.bote_monstruo(W, c, mo, t0 + x * T) for x in (0.0, 0.5, 1.0))
    t.check('v6: cada salto dura Tiemposalto (0,15) s: sale de donde estaba, a mitad de salto va a mitad de camino '
            'con el bote en lo alto (Botesalto 0,15 x su alto) y aterriza a los Tiemposalto s, sin bote',
            abs(T - 0.15) < 1e-6 and cerca(p0, pa) and not cerca(pm, pa) and not cerca(pm, ph) and cerca(p1, ph)
            and abs(b0) < 1e-6 and abs(bm - 0.15) < 1e-6 and abs(b1) < 1e-6 and mo['celda'] == a,
            'T %.9f; sale %s, a mitad %s, aterriza %s; bote %.2e %.9f %.2e; celda %s (%s)'
            % (T, cerca(p0, pa), not cerca(pm, pa) and not cerca(pm, ph), cerca(p1, ph), b0, bm, b1, mo['celda'], a))
    fz = m.filas_trumpzilla(W, dict(c, nivel=38), mo, t0 + 0.5 * T) if hasattr(m, 'filas_trumpzilla') else []
    t.check('v6: el sprite (fase 38) salta igual: el bote lo sube Botesalto x su alto y la sombra se queda en el '
            'suelo', len(fz) == 2 and abs(m._dot(m._add(fz[1][:3], pm, -1.0), m.normal_i(a)) -
                                           0.15 * fz[1][7]) < 0.02 * fz[1][7]
            and m._dot(m._add(fz[0][:3], pm, -1.0), m.normal_i(a)) < 0.02 * fz[1][7], '%d filas' % len(fz))

    # media celda: sigue siendo de la celda de la que sale
    m.cavar_zanja(W, c, a, 2, S.now)
    t.check('v6: en la media celda sigue en la celda de la que sale: una zanja que se abre en ella lo hace caer',
            mo['estado'] == 'cae' and mo['celda'] == a and mo['caidas'] == 1
            and cerca(m.pos_monstruo(W, c, mo, S.now + 1.0)[0], m._pos_destino(W, c, [a, None, 0.0])[0]),
            '%s en %s' % (mo['estado'], mo['celda']))

    # Saltosmonstruo apagado: el deslizamiento continuo de antes
    base.par.Saltosmonstruo = False
    W, c = S.nuevo(4)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    nx = mo['camino'][0]
    S.semis(W, c, 8)
    cont8 = cerca(m.pos_monstruo(W, c, mo, S.now)[0], m._pos_destino(W, c, [a, nx, 0.25])[0])
    S.semis(W, c, 12)
    cont20 = cerca(m.pos_monstruo(W, c, mo, S.now)[0], m._pos_destino(W, c, [a, nx, 20.0 / 32.0])[0])
    sin_bote = m.bote_monstruo(W, c, mo, S.now)
    base.par.Saltosmonstruo = True
    t.check('v6: con Saltosmonstruo apagado, la posicion es continua como antes (mov / need), sin bote',
            cont8 and cont20 and sin_bote == 0.0 and not c['saltos_monstruo'])

    # proyectos viejos: 24 y 12 pasan a 32 y 16 una sola vez; un valor puesto a mano se respeta
    claves = ['Pasomonstruo:24:32', 'Pasogrande:12:16']
    hechas = list(base.fetch('migraciones', [], search=False) or [])
    pm0, pg0 = base.par.Pasomonstruo.eval(), base.par.Pasogrande.eval()
    try:
        base.store('migraciones', [x for x in hechas if x not in claves])
        base.par.Pasomonstruo, base.par.Pasogrande = 24, 12
        renew_default(base, 'Pasomonstruo', 24, 32)
        renew_default(base, 'Pasogrande', 12, 16)
        viejo = (base.par.Pasomonstruo.eval(), base.par.Pasogrande.eval())
        base.par.Pasomonstruo = 24
        otra = renew_default(base, 'Pasomonstruo', 24, 32)
        base.store('migraciones', [x for x in hechas if x not in claves])
        base.par.Pasomonstruo = 20
        renew_default(base, 'Pasomonstruo', 24, 32)
        mano = base.par.Pasomonstruo.eval()
    finally:
        base.store('migraciones', hechas)
        base.par.Pasomonstruo, base.par.Pasogrande = pm0, pg0
    t.check('v6: un proyecto con Pasomonstruo 24 y Pasogrande 12 pasa a 32 y 16 (una sola vez); uno con 20 se '
            'queda en 20', viejo == (32, 16) and not otra and mano == 20, '%s, %s' % (viejo, mano))

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
    t.check('la linea MONSTRUO: numero, estado, celda -> objetivo, tam, acum y ritmo (2 x 0,5 = x1)',
            leg.startswith('  MONSTRUO #1  ') and ' celda %d -> %d  tam 0.50  acum 0/8  x1' % (a, mo['objetivo'])
            in leg, leg.strip())
    t.check('el mal, en la familia 9 del shader de la piel', 'mal' in FAMILIAS_PIEL
            and FAMILIAS_PIEL.index('mal') == 9 and 'bool malo = fam > 8.5' in PIEL_PIXEL)

    # 10. motor v137: a la luz. En la cara oculta camina en el sentido del giro hacia una pulsacion
    # de la cara visible; en la visible prefiere la presa visible a una oculta mas jugosa
    W, c = S.nuevo(4)
    vis = set(m.cara_visible(c))
    osc = [i for i in range(m.N) if i not in vis]
    if osc and vis:
        o0 = osc[len(osc) // 2]
        pul = max(vis, key=lambda i: (W['occ'][i] <= 0, i))
        _poner(m, W, osc[0], 9)
        W['terr'][pul] = W.get('bar_n', 0)
        mo = m.aparecer(W, c, S.now, o0)
        dm, pv = m.dijkstra_mon(W, c, o0)
        t.check('en la cara oculta va a una celda visible con pulsacion (no a la presa oculta de 9), por un '
                'camino que llega a la luz', mo['sombra'] and mo['objetivo'] in vis
                and mo['objetivo'] != osc[0] and mo['camino'][-1] == mo['objetivo'],
                'objetivo %s sombra %s' % (mo['objetivo'], mo.get('sombra')))
        pasos_ = 0
        while mo['celda'] not in vis and mo['camino'] and pasos_ < m.N:
            m.entrar_celda(W, c, mo, mo['camino'][0], S.now)
            pasos_ += 1
        t.check('al pisar la cara visible recalcula el objetivo de siempre (ya no esta en la sombra)',
                mo['celda'] in vis and not mo['sombra'], 'celda %s' % mo['celda'])
        W, c = S.nuevo(4)
        v1, v2 = sorted(vis)[:2]
        _poner(m, W, v1, 2)
        _poner(m, W, osc[0], 9)
        mo = m.aparecer(W, c, S.now, v2)
        t.check('en la cara visible prefiere la presa visible aunque haya otra oculta con mas ocupacion',
                mo['objetivo'] == v1 and not mo['sombra'], 'objetivo %s' % mo['objetivo'])

    # 11. v10 (motor v144): no suelta lo que devora. Comiendo una celda de 2 con una vecina de
    # Umbralfusion - 1 (6 / 2 = 3 > 2), antes la dejaba a medias en el recalculo siguiente
    W, c = S.nuevo(4)
    J = W['juego']
    vis = sorted(m.cara_visible(c))
    x = next((i for i in vis if any(j in vis for j in m.NEIGH[i])), None)
    if x is not None:
        y = next(j for j in m.NEIGH[x] if j in vis)
        yo = max(3, int(c['th_fusion']) - 1)
        _poner(m, W, x, 2)
        _poner(m, W, y, yo)
        mo = m.aparecer(W, c, S.now, x)
        antes = m.objetivo(W, c, mo)[0]
        mo.update(objetivo=x, camino=[], estado='devora', recalc=int(c['recalculo']) - 1)
        S.pasos(W, c, 1)
        uno = (mo['objetivo'], W['occ'][x], W['occ'][y])
        S.pasos(W, c, 1)
        t.check('v10 (motor v144): devorando una celda de 2 con una vecina de %d, que en el recalculo vale mas '
                '(%d / 2), no la suelta: la acaba (brote del mal) y luego va a por la vecina' % (yo, yo),
                antes == y and uno == (x, 1, yo) and W['sp'][x] == m.MAL and J['brotes'] == 1
                and W['occ'][y] == yo and mo['objetivo'] == y,
                'recalculo %s, tras un paso %s, brotes %d, objetivo %s' % (antes, uno, J['brotes'], mo['objetivo']))


run_test(base, prueba)
print('  Ahora: Modojuego; Sembrar hasta corona en una celda y hasta 3 en otra; Simmonstruo: el pequeno')
print('  va a la de 3. Deja que devore 8 escalones: forma grande y a por la corona.')
print('=' * 66)
