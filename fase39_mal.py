"""
=============================================================================
ESTRATOS - FASE 39: LA ESPECIE DEL MAL
=============================================================================
Requiere la fase 38. Lo visual del mal deja de ser provisional (fase 33: la
geometria de la especie de origen bajo un velo casi negro): el mal es una especie
con su propia biblioteca, la de la lamina «Mal, lamina de una especie nueva». La
logica del juego no cambia.

QUE HACE
--------
  BROTE        occ 1: una VALLA. Cercar es el primer gesto: valla de obra (paneles
               y pies de hormigon, prohibido), de torsion (postes y alambre de
               espino, privado) o con cartel (proximamente).
  RAMA         se decide al ABRIR la valla (cuando pasa de 1):
                 con Vecinasencierro (3) vecinas del mal o mas   ENCIERRO
                 la alimenta el SEQ1                              NEGOCIO
                 la alimenta el SEQ2                              OCIO
               (el ultimo secuenciador que la toco). Se queda hasta que vuelve a
               ser valla o deja de ser del mal.
  TIPOS        con los umbrales de la planificada (1, 2-3, 4-5, 6-7, 8+):
                 negocio   tienda, supermercado, centro comercial, gran superficie
                 ocio      bar, sala de fiestas, casino-hotel, resort de superlujo
                 encierro  recinto, muro, centro de internamiento, campo
               Cuerpos casi negros; neon rosa (el dinero) en escaparates, forjados
               y torres; hormigon y barracones en el encierro. Gramatica de la
               ciudad (fila 6 de la paleta; fachadas neon, torre de neon, muro y
               barracon). En cualquier tema; fuera de la piel del publico (ni sus
               clusters ni su relieve).
  OBRA         terminada = se enciende: cartel sobre la valla, estructura y grua,
               terminado a oscuras, puesta en marcha (el neon titubea y se
               enciende). Pasosobramal pasos cada paso de obra.
  EMBLEMAS     un sprite que flota sobre cada celda y mira a la camara, con luz
               propia (de lejos se lee el signo, no el edificio):
                           1      2-3       4-5      6-7        8+
                 negocio   prohib dolar     $ demon  $ demon $  magnate
                 ocio      prohib copa      dolar    $ demon    diamante
                 encierro  prohib candado   ojo      sirena     calavera
               Rosa neon = dinero; rojo = vigilancia y demonios; hueso = la
               calavera. Desde ocupacion 4, uno de cada tres dolares es un demonio.
  DEMONIO      un cluster del mal de 4 celdas o mas invoca a su demonio: 4-6 un
               diablillo sentado en la pieza mas alta; 7-9 una cabeza que asoma
               detras; 10+ el coloso, que abraza el cluster con la calavera en el
               pecho.
  RESCATE      (fase 35) mientras dura, el neon parpadea y se apaga; al
               completarse, la valla cae y la celda es del publico.
  OCEANO       (v2) con Oceano, cada celda del mal tiene su isla, llana, y sus
               edificios se apoyan en ella (sin ella el mar los tapaba y solo
               quedaban los emblemas flotando). El coloso, como mucho un tercio
               del radio del planeta.
  TIERRA       (v2, Montierra) Trumpzilla solo anda por tierra: con Oceano no
               entra en el mar (celda vacia a ras del nivel del mar) ni en las
               hondonadas inundadas; aparece en tierra (si todo lo vacio es mar,
               en una isla). Lo construido es isla; las zanjas, su trampa.
  NOCHE        (v3) la DISCOTECA (otra sala de fiestas: caja negra, tambor de neon,
               la cola) y sus seis focos: haces de colores que barren el cielo (luz
               local, aditiva; tambien los de la sala de fiestas y el casino). Las
               construcciones finales (etapa 4 y 5, encendidas) llevan NEON en el
               contorno de cada volumen (la 5, tambien en las aristas y un forjado de
               cada dos), del color de su rama. Con Oceano, YATES fondeados en el mar
               junto a la isla (casino 1, resort 2, gran superficie 1), con neon en la
               borda. La cabeza y el coloso, un 30 % mas pequenos.
  LEYENDA      MAL      negocio 3  ocio 3  encierro 2  vallas 2   obras 1   demonio coloso (10 celdas)

OPERADORES (en /project1/FASE1)
-------------------------------
  emblemas_mal, i_emblemas_mal   Geometry COMP instanciado (una lamina) con
               mat_emblema (GLSL MAT: emblema_vertex y emblema_pixel).
  mal_atlas    Movie File In TOP con sprites/mal_emblemas.png (se rehace con
               sprites/hacer_atlas_mal.py).
  mod_edi_<diseno>_<v> y mod_ciu_<remate>   los edificios y remates del mal, en
               la biblioteca de la ciudad (modelos/).

PROBAR
------
  Modojuego. Simmal: un cluster de diez celdas alrededor de Simceldamon, de fuera
  adentro: vallas, negocio y ocio por fuera, encierro en el centro, todo en obra
  (cartel, grua, a oscuras, se enciende) y el coloso detras. Especiemal apagado:
  el velo provisional de la fase 33.

  v4 (comun v101): Montierra pasa a la pagina Monstruos, con su valor.

COMO USARLO
-----------
  Copia la carpeta sprites del repositorio en la carpeta de los scripts y:
    exec(open('C:/Users/DareDave/Downloads/est/fase39_mal.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase39 v4  (Montierra, en la pagina Monstruos con los demas parametros de los monstruos)'
banner(VERSION)

base = require_base(39)
motor = install_core(base, CARPETA, 39)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase39)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase39')
add_par(base, page, 'toggle', 'Especiemal', 'Especie del mal (sin: el velo provisional)', True)
add_par(base, page, 'int', 'Vecinasencierro', 'Vecinas del mal para cerrarse (encierro)', 3, 1, 6, clamp=True)
add_par(base, page, 'int', 'Pasosobramal', 'Pasos por paso de obra', 8, 1, 64, clamp=True)
add_par(base, page, 'float', 'Tamanoemblema', 'Tamano del emblema (celdas)', 0.35, 0.05, 3.0, clamp=True)
add_par(base, page, 'float', 'Brilloemblema', 'Brillo del emblema (neon)', 1.0, 0.1, 4.0, clamp=True)
add_par(base, page, 'float', 'Altomal', 'Alto de los edificios del mal (x la planta)', 1.5, 0.5, 4.0, clamp=True)
add_par(base, page, 'toggle', 'Demoniomal', 'El demonio de los clusters', True)
# v4 (comun v101): Montierra, en la pagina Monstruos con los demas de los monstruos
pmon, _movidos = sacar_a_monstruos(base, ('Montierra',))
add_par(base, pmon, 'header', 'Hterreno', 'Por donde andan (fase 39)')
add_par(base, pmon, 'toggle', 'Montierra', 'Los monstruos solo andan por tierra (con Oceano)', True)
monstruos_al_dia(base, _movidos)
add_par(base, page, 'pulse', 'Simmal', 'Simular cluster del mal')
ok('parametros de la fase 39: Especiemal, Vecinasencierro 3, Pasosobramal 8, Tamanoemblema 0,35, Brilloemblema 1, '
   'Altomal 1,5, Demoniomal, Simmal; Montierra, en la pagina Monstruos')

# v2: los emblemas de la v1 (0,45) se veian grandes: un proyecto con 0,45 pasa a 0,35, una sola vez
try:
    _hechas = set(base.fetch('migraciones', [], search=False) or [])
except Exception:
    _hechas = set()
if 'fase39:emblema0.35' not in _hechas:
    if abs(float(base.par.Tamanoemblema.eval()) - 0.45) < 1e-6:
        base.par.Tamanoemblema = 0.35
        ok('Tamanoemblema: de 0,45 (la v1) a 0,35')
    try:
        base.store('migraciones', sorted(_hechas | {'fase39:emblema0.35'}))
    except Exception:
        pass

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

modelos, n_nuevos, n_piezas, ajustadas = construir_modelos(base, m, solo_nuevos=True)
ok('biblioteca del mal: %d disenos (%d ejemplares) y %d remates nuevos en %s'
   % (len(m.DISENOS_MAL), len([e for e in m.edificios_de(m.cfg()) if m.parte_edificio(e)[0] in m.MALES]),
      len(m.MODELOS_MAL), modelos.path))
instanciar_modelos(base, m)
emblemas_al_dia(base, CARPETA)
set_render(base)

leeme(base, 39, """FASE 39 - LA ESPECIE DEL MAL
  El brote es una valla. Al abrir: con Vecinasencierro vecinas del mal,
  ENCIERRO (recinto, muro, internamiento, campo); si no, la del ultimo
  secuenciador: SEQ1 NEGOCIO (tienda, supermercado, centro comercial, gran
  superficie), SEQ2 OCIO (bar, sala de fiestas, casino, resort). Cuerpos
  negros con neon rosa; la obra termina encendiendo el neon (Pasosobramal).
  Encima, el emblema (sprite con luz propia, Tamanoemblema, Brilloemblema).
  Un cluster de 4+ invoca su demonio: diablillo, cabeza (7+), coloso (10+).
  Al rescatar, el neon se apaga y la valla cae. Simmal: un cluster de prueba.
  Especiemal apagado: el velo provisional de la fase 33.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS39 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Especiemal', 'Vecinasencierro', 'Pasosobramal', 'Demoniomal', 'Altomal', 'Tamanoemblema', 'Tema',
          'Oceano', 'Montierra')


def prueba(t):
    import copy
    import time
    m = t.m
    guarda, filas = guardar_sala(base, PARS39)
    try:
        _prueba(t, m, copy, time)
    finally:
        devolver_sala(base, m, guarda, filas)


def _filas_celda(m, W, c, inst, i):
    """Las filas del edificio del mal de la celda i (su ejemplar)."""
    inf = m.info_mal(W, c, i)
    g = m.geometria_de(m.nombre_edificio(inf['ex']['diseno'], inf['ex']['var']))
    p0 = m._mul(m.normal_i(i), m.base_radius(W, c, i))
    return [f for f in inst.get(g, []) if m._len(m._add(f[:3], p0, -1.0)) < 1e-6]


def _emblemas_celda(m, inst, i):
    """Las filas de los emblemas que flotan sobre la celda i (no las de sus satelites)."""
    n = m.normal_i(i)
    return [f for f in inst.get('emblemas_mal', []) if m._dot(m._norm(f[:3]), n) > 0.99999]


def _emblema(m, f):
    q = int(round(f[12]))
    return m.EMBLEMAS_MAL[q % m.EMBLEMA_MODO_K], m.MODOS_EMBLEMA[q // m.EMBLEMA_MODO_K]


def _prueba(t, m, copy, time):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # que el monstruo no aparezca solo
    base.par.Especiemal = True
    base.par.Vecinasencierro = 3
    base.par.Pasosobramal = 8
    base.par.Demoniomal = True
    base.par.Altomal = 1.5
    base.par.Tamanoemblema = 0.35
    base.par.Montierra = True
    S = SalaJuego(base, m, absTime.seconds + 5100.0)
    vis_ = m.cara_visible(m.cfg())      # motor v137: en la cara visible (en la oculta, el monstruo busca la luz)
    a = vis_[len(vis_) // 2] if vis_ else m.N // 2
    vec = list(m.NEIGH[a])

    # 1. el atlas, los operadores, la biblioteca y el render
    cols, fil = m.ATLAS_MAL
    med = _png_medidas(CARPETA + '/' + MAL_ATLAS)
    mat = base.op('mat_emblema')
    nombres = str(base.op('render').par.geometry.val).split()
    c = m.cfg()
    edis = [e for e in m.edificios_de(c) if m.parte_edificio(e)[0] in m.MALES]
    faltan = [e for e in edis if base.op(m.geometria_de(e)) is None] + \
        [mo for mo in m.MODELOS_MAL if base.op(m.geometria_de(mo)) is None]
    t.check('el atlas sprites/mal_emblemas.png (%d x %d celdas de 256 x 128 para %d emblemas), emblemas_mal, '
            'i_emblemas_mal y mat_emblema (sAtlas, uEmblema con sprite_t, uEmblemaInc con Brilloemblema); '
            'el render los dibuja' % (cols, fil, len(m.EMBLEMAS_MAL)),
            med == (cols * 256, fil * 128) and len(m.EMBLEMAS_MAL) <= cols * fil
            and all(base.op(n) is not None for n in ('emblemas_mal', 'i_emblemas_mal', 'emblema_vertex',
                                                      'emblema_pixel', 'mal_atlas'))
            and mat is not None and str(mat.par.sampler0name.eval()) == 'sAtlas'
            and str(mat.par.vec0name.eval()) == 'uEmblema' and 'sprite_t' in (mat.par.vec0valuex.expr or '')
            and 'Brilloemblema' in (mat.par.vec1valuey.expr or '') and 'emblemas_mal' in nombres,
            '%s' % (med,))
    t.check('la biblioteca del mal: %d disenos (%d ejemplares) y %d remates, cada uno con su geometria'
            % (len(m.DISENOS_MAL), len(edis), len(m.MODELOS_MAL)),
            len(m.DISENOS_MAL) == 15 and not faltan and all(m.edificio(c, d, 0)['vols'] for d in m.DISENOS_MAL),
            'faltan %s' % faltan[:4])

    # 2. la logica no cambia: la misma partida que tras la fase 38
    W, c = S.nuevo(4)
    dist, _ = m.dijkstra_mon(W, c, a)
    lejos = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    junto = m.NEIGH[a][0]

    def partida(cfg_):
        S2 = SalaJuego(base, m, absTime.seconds + 5600.0)
        W2, _ = S2.nuevo(4)
        for x, o in ((lejos, 4), (junto, 3)):
            S2.sembrar(W2, cfg_, x, o)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(12):
            S2.pasos(W2, cfg_, 2)
            m.build_instances(W2, cfg_, S2.now)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento']))
    c = m.cfg()
    r39 = partida(c)
    r38 = partida(dict(c, nivel=38))
    t.check('con la especie del mal, el juego da el mismo resultado que tras la fase 38 (la logica no cambia)',
            r39 == r38 and r39[2]['comidos'] > 0 and m.MAL in r39[1], 'comidos %d' % r39[2]['comidos'])

    # 3. la rama, al abrir la valla
    W, c = S.nuevo(4)
    b1, b2 = vec[0], vec[3]
    for x in (b1, b2):
        m.brote_mal(W, c, x, S.now)
    S.semis(W, c, 1)
    v1 = m.info_mal(W, c, b1)
    S.sembrar(W, c, b1, 3, m.GEO)
    S.sembrar(W, c, b2, 3, m.ARQ)
    S.semis(W, c, 1)
    E = W['juego']['mal']
    r1, r2 = E['rama'].get(b1), E['rama'].get(b2)
    S.sembrar(W, c, b1, 4, m.ARQ)                 # despues de abrir, la rama se queda
    S.semis(W, c, 1)
    sigue = E['rama'].get(b1)
    for x in [a] + [y for y in vec if y not in (b1, b2)][:1]:
        m.brote_mal(W, c, x, S.now)
    S.semis(W, c, 1)
    S.sembrar(W, c, a, 2, m.GEO)                    # a: tres vecinas del mal al abrir
    S.semis(W, c, 1)
    ra = E['rama'].get(a)
    t.check('la valla (occ 1, sin rama, emblema %s); al abrir, el SEQ1 abre negocio y el SEQ2 ocio; despues, '
            'otro secuenciador no la cambia; con 3 vecinas del mal, encierro' % v1['emblema'],
            v1['rama'] is None and v1['tipo'] == 'valla' and v1['diseno'] in m.VALLAS_MAL
            and v1['emblema'] in ('prohibido', 'proximamente') and r1 == 'negocio' and r2 == 'ocio'
            and sigue == 'negocio' and ra == 'encierro' and m.vecinas_mal(W, a) >= 3,
            '%s %s %s %s' % (r1, r2, sigue, ra))

    # 4. la escalera de cada rama y su emblema
    W, c = S.nuevo(2)
    m.brote_mal(W, c, a, S.now)
    E = m.mal_estado(W)
    mal = []
    for rama in m.RAMAS_MAL:
        serie = []
        for o in range(1, 10):
            W['occ'][a] = o
            E['rama'][a] = rama
            inf = m.info_mal(W, c, a)
            serie.append((inf['tipo'], inf['emblema']))
        tipos = [x[0] for x in serie]
        esperado = [m.TIPOS_MAL[rama][m.etapa_mal(c, o) - 1] for o in range(1, 10)]
        ems = [x[1] for x in serie[1:]]
        bien = tipos == esperado and set(tipos) == set(m.TIPOS_MAL[rama]) and \
            all(e == m.EMBLEMA_DE[rama][m.etapa_mal(c, o) - 1] for e, o in zip(ems, range(2, 10)))
        mal.append('%s %s' % (rama, '-'.join(sorted(set(tipos), key=tipos.index)) if bien else 'MAL'))
    t.check('las escaleras (occ 1 a 9): %s; con su emblema' % '; '.join(mal), not any('MAL' in x for x in mal))

    # 5. la obra: cartel, estructura y grua, a oscuras, encendida
    W, c = S.nuevo(2)
    m.brote_mal(W, c, a, S.now)
    S.semis(W, c, 1)
    S.sembrar(W, c, a, 6, m.ARQ)
    S.semis(W, c, 1)
    dur = int(c['pasos_obra_mal'])
    pasos = []
    for k in range(4):
        inst = m.build_instances(W, c, S.now)
        filas_em = _emblemas_celda(m, inst, a)
        em = [_emblema(m, f) for f in filas_em]
        fe = _filas_celda(m, W, c, inst, a)
        grua = len(inst.get(m.geometria_de('ciu_grua'), []))
        alfa = fe[0][12] if fe else -1.0
        pasos.append((m.paso_obra_mal(W, c, a, S.now), em[0] if em else None, grua,
                      m.nivel_ventanas(alfa) if fe else -1, m.lenguaje_fila(alfa) if fe else -1,
                      (filas_em or [[0] * 13])[0][9]))
        S.semis(W, c, dur)
    t.check('la obra, %d pasos cada paso: cartel (la valla y proximamente), estructura (esqueleto y grua, sin '
            'emblema), terminado a oscuras (sin neon, emblema apagado), encendido (neon, lenguaje 6)' % dur,
            [p[0] for p in pasos] == [0, 1, 2, 3] and pasos[0][1] == ('proximamente', 'fijo')
            and pasos[1][1] is None and pasos[1][2] == 1 and pasos[2][3] == 0 and pasos[2][4] == m.PALETA_MAL
            and abs(pasos[2][5] - m.LUZ_APAGADO) < 1e-6 and pasos[3][3] == 4 and pasos[3][1][0] == 'dolar_demonio'
            and pasos[3][4] == m.PALETA_MAL, '%s' % pasos)

    # 6. fuera de la piel del publico; sin el velo
    W, c = S.nuevo(2)
    for x in [a] + vec[:3]:
        m.brote_mal(W, c, x, S.now)
    S.semis(W, c, 1)
    for x in [a] + vec[:3]:
        S.sembrar(W, c, x, 5, m.GEO)
    S.semis(W, c, 1)
    inst = m.build_instances(W, c, S.now)
    publico = [g for g, f in inst.items() if g.startswith('mod_edi_') and f and
               m.parte_edificio(g[4:])[0] not in m.MALES]
    cl = m.clusters(W, c)
    t.check('con la especie: sin velo (brotes_mal vacio), ningun edificio del publico en las celdas del mal y '
            'sin clusters del publico con ellas',
            inst.get('brotes_mal') == [] and not publico and all(cl['de'][x] < 0 for x in [a] + vec[:3]),
            'publico %s' % publico[:3])

    # 7. el demonio de los clusters: 3 nada, 4 diablillo, 7 cabeza, 10 coloso (Simmal)
    demonios = []
    for k in (3, 4, 7):
        W, c = S.nuevo(1)
        for x in ([a] + vec)[:k]:
            m.brote_mal(W, c, x, S.now)
            W['occ'][x] = 3
        S.semis(W, c, 1)
        inst = m.build_instances(W, c, S.now)
        demonios.append([e for e, _ in map(lambda f: _emblema(m, f), inst['emblemas_mal'])
                         if e in ('diablillo', 'cabeza', 'coloso')])
    W, c = S.nuevo(1)
    msg = m.sim_mal(W, c, S.now, celda=a)
    S.semis(W, c, 1)
    inst = m.build_instances(W, c, S.now)
    col = [f for f in inst['emblemas_mal'] if _emblema(m, f)[0] == 'coloso']
    r = W['juego']['mal']['rama']
    ramas = set(r.values())
    t.check('el demonio: 3 celdas ninguno, 4 diablillo, 7 cabeza; Simmal (diez celdas, de fuera adentro): '
            'negocio, ocio y encierro, y el coloso detras',
            demonios == [[], ['diablillo'], ['cabeza']] and len(col) == 1 and _emblema(m, col[0])[1] == 'detras'
            and ramas == set(m.RAMAS_MAL) and r.get(a) == 'encierro', '%s; %s' % (demonios, msg))
    leg = m._legend_mal(W, c)

    # 8. el presupuesto
    t0 = time.perf_counter()
    for _ in range(20):
        m.build_mal(W, c, S.now, {})
    ms = (time.perf_counter() - t0) * 1000.0 / 20
    t.check('la leyenda (%s) y el presupuesto: %.2f ms por fotograma con diez celdas' % (leg.strip(), ms),
            'demonio coloso (10 celdas)' in leg and 'encierro' in leg and ms < 3.0)

    # 9. el rescate: el neon parpadea y se apaga; la valla cae
    W, c = S.nuevo(1)
    m.brote_mal(W, c, a, S.now)
    S.semis(W, c, 1)
    S.sembrar(W, c, a, 3, m.GEO)
    E = m.mal_estado(W)
    E['obra'][a] = (m.etapa_mal(c, 3), -1e9)
    W['juego']['rescates'][a] = S.now - 0.9 * c['t_aliados']
    inst = m.build_instances(W, c, S.now)
    em = _emblemas_celda(m, inst, a)[0]
    luces = m.nivel_ventanas(_filas_celda(m, W, c, inst, a)[0][12])
    m.rescatar(W, c, a, S.now)
    S.semis(W, c, 1)
    caida = E['caidas'].get(a)
    ver = m.build_instances(W, c, S.now)
    vallas = sum(len(f) for g, f in ver.items() if g.startswith('mod_edi_valla'))
    S.semis(W, c, int(m.T_CAIDA_MAL / S.SEMI) + 2)
    fin = m.build_instances(W, c, S.now)
    vallas2 = sum(len(f) for g, f in fin.items() if g.startswith('mod_edi_valla'))
    t.check('rescate al 90 %: el neon apagado y el emblema parpadeando y debil; rescatada, la valla cae '
            '(T_CAIDA_MAL s) y desaparece',
            luces == 0 and _emblema(m, em)[1] == 'parpadeo' and em[9] < 0.2 and caida is not None
            and vallas == 1 and vallas2 == 0 and a not in E['caidas'], 'luces %d, luz %.2f' % (luces, em[9]))

    # 10. Especiemal apagado y Modojuego apagado
    W, c = S.nuevo(1)
    m.sim_mal(W, c, S.now, celda=a)
    base.par.Especiemal = False
    c = m.cfg()
    sin = m.build_instances(W, c, S.now)
    base.par.Especiemal = True
    base.par.Modojuego = False
    nada = m.build_instances(W, m.cfg(), S.now)
    t.check('Especiemal apagado: el velo provisional (brotes_mal) y sin emblemas; Modojuego apagado: nada',
            len(sin['brotes_mal']) == 10 and sin['emblemas_mal'] == [] and nada.get('emblemas_mal') == [],
            '%d velos' % len(sin['brotes_mal']))

    # 11. v2: con Oceano, Trumpzilla solo anda por tierra; el mal, sobre su isla
    base.par.Tema = 'naturaleza'
    base.par.Oceano = True
    W, c = S.nuevo(4)
    dist, _ = m.dijkstra_mon(dict(W, juego=dict(zanjas={}, agua={})), dict(c, nivel=38), a)
    b = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    puente = [x for x in m.NEIGH[a] if b in m.NEIGH[x]][0]
    m.brote_mal(W, c, a, S.now)                     # su isla: un brote del mal (no se lo come)
    S.sembrar(W, c, b, 3)
    mar = m.mar_mon(W, c)
    mo = m.aparecer(W, c, S.now, a)
    sin_puente = (mo['objetivo'], list(mo['camino']))
    S.sembrar(W, c, puente, 1)
    m.recalcular_objetivo(W, c, mo, S.now)
    con_puente = (mo['objetivo'], list(mo['camino']))
    base.par.Montierra = False
    m.recalcular_objetivo(W, c, mo, S.now)
    sin_regla = m.mar_mon(W, m.cfg())
    base.par.Montierra = True
    c = m.cfg()
    m.brote_mal(W, c, puente, S.now)
    S.semis(W, c, 1)
    ter = m.terreno(W, c)
    suelo_m = m.suelo_mal(W, c, puente) - m.base_radius(W, c, puente)
    t.check('con Oceano, Trumpzilla solo anda por tierra: con mar entre su isla y la presa no tiene objetivo; '
            'con un puente de tierra va por el; Montierra apagado, todo es tierra. La celda del mal, sobre su isla',
            puente in mar and a not in mar and b not in mar and sin_puente == (None, [])
            and con_puente == (b, [puente, b]) and sin_regla == frozenset()
            and suelo_m > 0.02 and abs(suelo_m - ter['centro'][puente]) < 1e-9,
            'mar %d celdas; sin puente %s, con puente %s; isla %.3f' % (len(mar), sin_puente, con_puente, suelo_m))

    # 12. v3: la discoteca y sus focos, el neon de lo terminado, los yates y los demonios mas pequenos
    base.par.Tema = 'ciudad'
    base.par.Oceano = True

    def mal_en(W, c, x, occ, rama, diseno=None):
        m.brote_mal(W, c, x, S.now)
        W['occ'][x] = occ
        E = m.mal_estado(W)
        E['rama'][x] = rama
        E['obra'][x] = (m.etapa_mal(c, occ), -1e9)
        if diseno is not None:
            for v in range(1, 128):
                W['vel'][x] = v
                if m.info_mal(W, c, x)['diseno'] == diseno:
                    break
        return m.info_mal(W, c, x)

    W, c = S.nuevo(1)
    luz0 = len(m.build_instances(W, c, S.now).get('luz_local') or [])
    inf = mal_en(W, c, a, m.occ_inicio(c, 'planificada', 3), 'ocio', 'discoteca')
    S.semis(W, c, 1)
    inst = m.build_instances(W, c, S.now)
    res3 = dict(W['juego']['mal']['res'])
    haces = len(inst.get('luz_local') or []) - luz0
    W, c = S.nuevo(1)
    inf5 = mal_en(W, c, a, m.occ_inicio(c, 'planificada', 5), 'ocio')
    S.semis(W, c, 1)
    m.build_instances(W, c, S.now)
    res5 = dict(W['juego']['mal']['res'])
    base.par.Oceano = False
    c = m.cfg()
    m.build_instances(W, c, S.now)
    sin_mar = dict(W['juego']['mal']['res'])
    base.par.Oceano = True
    c = m.cfg()
    alto_cabeza = []
    W, c = S.nuevo(1)
    for x in ([a] + vec)[:7]:
        m.brote_mal(W, c, x, S.now)
        W['occ'][x] = 9
    S.semis(W, c, 1)
    inst = m.build_instances(W, c, S.now)
    r0 = m.base_radius(W, c, a)
    alto_cabeza = [f[7] for f in inst['emblemas_mal'] if _emblema(m, f)[0] == 'cabeza']
    t.check('v3: la discoteca (sala de fiestas) con seis focos que barren el cielo (%d filas de luz local); el '
            'neon de lo terminado (resort: %d tubos; la discoteca, ninguno); con Oceano, los yates del resort en '
            'el mar (%d; sin Oceano, %d); la cabeza, como mucho un sexto del radio (%.2f de %.2f)'
            % (haces, res5.get('neon', 0), res5.get('yates', 0), sin_mar.get('yates', 0),
               max(alto_cabeza or [0.0]), r0),
            inf['diseno'] == 'discoteca' and 'discoteca' in m.DISENOS_TIPO['salafiestas'] and haces >= 18
            and res3.get('neon', 0) == 0 and inf5['etapa'] == 5 and res5.get('neon', 0) > 8
            and res5.get('yates', 0) >= 1 and sin_mar.get('yates', 0) == 0
            and len(alto_cabeza) == 1 and alto_cabeza[0] <= 0.17 * r0 + 1e-6,
            'disenos %s; res3 %s; res5 %s' % (inf['diseno'], res3, res5))


run_test(base, prueba)
print('  Ahora: Modojuego y Simmal: un cluster de diez celdas en obra (vallas, negocio, ocio y encierro)')
print('  Con Oceano, Trumpzilla solo anda por tierra (Montierra).')
print('  que se enciende, con el coloso detras. Especiemal apagado: el velo provisional.')
print('=' * 66)
