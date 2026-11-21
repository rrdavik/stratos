"""
=============================================================================
ESTRATOS - FASE 40: GODZILLA, EL MONSTRUO DE LA CREACION
=============================================================================
Requiere la fase 39. Godzilla hace por la creacion del mundo lo que Trumpzilla
hace por el mal: devora el mal y deja brotes de la creacion. Sin nadie en la
sala, Trumpzilla ganaba la partida entera; con Godzilla, la lucha del bien y el
mal queda equilibrada. Si los dos monstruos se encuentran, se pelean.

QUE HACE
--------
  CUANDO       Godzillasala = vacia (de fabrica): solo con la sala vacia, sin
               nadie Tvacia s (15; tambien al empezar la partida). Si llega
               gente, se va: saluda con una flor y se hunde. Siempre: tambien
               con publico.
  APARECE      con Malgodzilla (1) celdas del mal o mas en el globo, en la celda
               vacia de la cara visible por la que entran las celdas con el giro
               (como Trumpzilla), lejos de Trumpzilla. Tras irse, como pronto
               Esperamonstruo s despues.
  DEVORA       el mal: va a por la celda del mal de mayor occ / (1 + coste) (el
               pequeno no puede con fusiones ni coronas), con el ritmo, el dano
               (Danomonstruo), el paso y el crecimiento de Trumpzilla. Solo anda
               por tierra, como Trumpzilla (v3, Montierra): no entra en el mar; pasa
               por lo construido, la tierra firme y las carreteras y vias que
               cruzan el agua. No cae en las zanjas ni se ahoga (son del publico
               contra el mal), pero el agua es muro y la zanja cuesta.
  CREA         la celda del mal que vacia recibe un BROTE DE LA CREACION: occ 1,
               con la especie del ultimo secuenciador que la toco. Es del publico
               y crece con las notas como cualquier otra.
  LUCHA        si los dos monstruos quedan en celdas contiguas, se acercan al
               borde y se dan manotazos Pasoslucha pasos de juego (8): ni andan
               ni devoran; uno da (furia, se echa encima) y el otro recibe (mueca,
               tiembla), por turnos. Luego cada uno vuelve a la celda de la que
               venia y hay Tregua pasos (16) en que no se cruzan ni se pelean.
  EMOCIONES    el atlas sprites/godzilla_emociones.png (mismo formato que el de
               Trumpzilla, mismo shader): serio al aparecer, enfado al buscar
               (furia grande), rie al crear (carcajada grande), calma sin mal que
               comer, furia y mueca en la lucha, calma y saluda al irse.
  LEYENDA      GODZILLA #1  devora  celda 12 -> 12  tam 0.75  acum 4/8   creados 3   cara rie   sala vacia
               LUCHA    manotazos 5/8 pasos   celdas 40 | 41   (luchas 2)

OPERADORES (en /project1/FASE1)
-------------------------------
  godzilla, i_godzilla   Geometry COMP instanciado (una lamina: el sprite y su
               sombra) con mat_godzilla (GLSL MAT: sprite_vertex y sprite_pixel,
               los de Trumpzilla).
  godzilla_atlas   Movie File In TOP con sprites/godzilla_emociones.png (se
               rehace con sprites/hacer_atlas_godzilla.py).

PROBAR
------
  Modojuego. Simmal (un cluster del mal) y Simgodzilla: aparece serio, va
  enfadado a la celda del mal mas prospera y la devora riendo; la celda vuelve
  a ser del publico. Simlucha: Trumpzilla y Godzilla en celdas vecinas, se dan
  manotazos 8 pasos y cada uno se va por donde vino.

COMO USARLO
-----------
  Copia la carpeta sprites del repositorio en la carpeta de los scripts y:
    exec(open('C:/Users/DareDave/Downloads/est/fase40_godzilla.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase40 v3  (Godzilla solo anda por tierra, como Trumpzilla; las carreteras y vias cruzan el agua)'
banner(VERSION)

base = require_base(40)
motor = install_core(base, CARPETA, 40)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase40)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase40')
add_par(base, page, 'toggle', 'Godzilla', 'Godzilla (el monstruo de la creacion)', True)
add_par(base, page, 'menu', 'Godzillasala', 'Cuando sale', 'vacia', menu=list(m.GODZILLA_SALA),
        menu_labels=['Solo con la sala vacia', 'Siempre'])
add_par(base, page, 'float', 'Tvacia', 'Sala vacia (s sin nadie)', 15.0, 0.0, 300.0, clamp=True)
add_par(base, page, 'int', 'Malgodzilla', 'Celdas del mal para que aparezca', 1, 1, 64, clamp=True)
add_par(base, page, 'int', 'Pasoslucha', 'Pasos de la lucha (manotazos)', 8, 1, 64, clamp=True)
add_par(base, page, 'int', 'Tregua', 'Pasos de tregua tras la lucha', 16, 0, 256, clamp=True)
add_par(base, page, 'float', 'Altogodzilla', 'Alto de Godzilla (celdas, por tam)', 0.8, 0.2, 4.0, clamp=True)
add_par(base, page, 'menu', 'Emociongodzilla', 'Emocion de Godzilla', 'auto', menu=['auto'] + list(m.EMOCIONES_MON),
        menu_labels=['Auto (por su estado)'] + [e.capitalize() for e in m.EMOCIONES_MON])
add_par(base, page, 'pulse', 'Simgodzilla', 'Simular Godzilla (aparece ya)')
add_par(base, page, 'pulse', 'Simlucha', 'Simular la lucha (junto a Trumpzilla)')
ok('pagina Fase40: Godzilla, Godzillasala (vacia), Tvacia 15 s, Malgodzilla 1, Pasoslucha 8, Tregua 16, '
   'Altogodzilla 0,8, Emociongodzilla (auto), Simgodzilla, Simlucha')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

materiales_piel(base)                   # mat_respaldo, para Materialrespaldo
trumpzilla_al_dia(base, CARPETA)        # los shaders (con las animaciones de la lucha)
godzilla_al_dia(base, CARPETA)
set_render(base)

leeme(base, 40, """FASE 40 - GODZILLA, EL MONSTRUO DE LA CREACION
  Hace por la creacion lo que Trumpzilla por el mal. Con la sala vacia Tvacia
  s (Godzillasala = vacia; siempre, tambien con gente) y Malgodzilla celdas del
  mal, aparece, va a por la celda del mal mas prospera, la devora con el ritmo
  de Trumpzilla y deja un brote de la creacion (del publico). Solo anda por
  tierra (lo construido, tierra firme, carreteras y vias), como Trumpzilla. Si llega
  gente, saluda y se va. Si los dos monstruos quedan en celdas contiguas, se
  acercan al borde y se dan manotazos Pasoslucha pasos (8); luego cada uno
  vuelve a la celda de la que venia, con Tregua pasos (16) sin cruzarse.
  Simgodzilla: aparece ya. Simlucha: la lucha junto a Trumpzilla.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS40 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Spritemonstruo', 'Emocion', 'Godzilla', 'Godzillasala', 'Tvacia', 'Malgodzilla', 'Pasoslucha',
          'Tregua', 'Altogodzilla', 'Emociongodzilla', 'Simceldamon', 'Tema', 'Oceano', 'Montierra')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS40)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ, s=None):
    s = m.GEO if s is None else s
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = s
    W['traza'][i] = 1
    W['h'][i] = m.height_for(m.cfg(), occ)


def _mal(m, W, c, i, occ, now):
    m.brote_mal(W, c, i, now)
    W['occ'][i] = occ


def _cara(m, fila):
    k = int(round(fila[12]))
    return m.EMOCIONES_MON[k % 16], m.ANIMS_MON[k // 16]


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # Trumpzilla no aparece solo (salvo donde se pide)
    base.par.Spritemonstruo = True
    base.par.Emocion = 'auto'
    for nm, v in (('Godzillasala', 'vacia'), ('Tvacia', 15.0), ('Malgodzilla', 1), ('Pasoslucha', 8),
                  ('Tregua', 16), ('Altogodzilla', 0.8), ('Emociongodzilla', 'auto')):
        setattr(base.par, nm, v)
    S = SalaJuego(base, m, absTime.seconds + 5100.0, godzilla=True)

    # 1. el atlas, los operadores y el render
    cols, filas = m.ATLAS_MON
    med = _png_medidas(CARPETA + '/' + GODZILLA_ATLAS)
    mat = base.op('mat_godzilla')
    nombres = str(base.op('render').par.geometry.val).split()
    t.check('el atlas sprites/godzilla_emociones.png (%d x %d celdas de 192 x 256, el formato de Trumpzilla); '
            'godzilla, i_godzilla y mat_godzilla (los shaders de Trumpzilla, sampler sAtlas -> godzilla_atlas); el '
            'render dibuja godzilla' % (cols, filas),
            med == (cols * 192, filas * 256) and base.op('godzilla_atlas') is not None
            and all(base.op(n) is not None for n in ('godzilla', 'i_godzilla'))
            and mat is not None and str(mat.par.sampler0name.eval()) == 'sAtlas'
            and str(mat.par.vec0name.eval()) == 'uSprite' and 'godzilla' in nombres
            and 'anim == 7' in base.op('sprite_vertex').text and 'i_godzilla' in m.chop_names(m.cfg()),
            '%s' % (med,))

    vis_ = m.cara_visible(m.cfg())      # motor v137: en la cara visible (en la oculta, el monstruo busca la luz)
    a = vis_[len(vis_) // 2] if vis_ else m.N // 2
    W, c = S.nuevo(4)
    dist, _ = m.dijkstra_mon(W, c, a)
    lejos = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    junto = m.NEIGH[a][0]
    otro = [x for x in m.NEIGH[a] if x != junto and x not in m.NEIGH[junto]][0]

    # 2. la logica de la fase 39, sin Godzilla o con gente en la sala
    def partida(cfg_, casillas=None):
        S2 = SalaJuego(base, m, absTime.seconds + 5600.0, godzilla=True)
        W2, _ = S2.nuevo(4)
        for x, o in ((lejos, 4), (junto, 3)):
            _poner(m, W2, x, o)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(16):
            S2.pasos(W2, cfg_, 2, casillas)
            m.build_instances(W2, cfg_, S2.now)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento'])), J.get('bien')
    c = m.cfg()
    r39, _ = partida(dict(c, nivel=39))
    r39g, _ = partida(dict(c, nivel=39), [0])
    r_off, _ = partida(dict(c, godzilla=0, t_vacia=0.0))
    r_gente, g_gente = partida(dict(c, t_vacia=0.0), [0])
    _, g_vacia = partida(dict(c, t_vacia=0.0))
    t.check('sin Godzilla, o con gente en la sala (Godzillasala vacia), el juego da lo mismo que tras la fase 39; '
            'con la sala vacia, Godzilla sale',
            r_off == r39 and r_gente == r39g and r39[2]['comidos'] > 0 and (g_gente or {}).get('n', 0) == 0
            and g_vacia is not None and g_vacia['n'] >= 1,
            'comidos %d, godzilla con gente %s, sin gente %s; iguales: apagado %s, con gente %s'
            % (r39[2]['comidos'], (g_gente or {}).get('n'), (g_vacia or {}).get('n'), r_off == r39, r_gente == r39g))

    # 3. la sala vacia Tvacia s y el mal: aparece; con gente, se va
    W, c = S.nuevo(4)
    _mal(m, W, c, a, 2, S.now)
    _poner(m, W, lejos, 6)
    S.pasos(W, c, 20)                       # 10 s sin nadie: aun no
    antes = W['juego']['bien']['estado']
    S.pasos(W, c, 12)                       # 16 s
    g = W['juego']['bien']
    sale = g['estado'] in ('aparece', 'busca', 'devora') and g['objetivo'] == a
    S.pasos(W, c, 2, [0])                   # llega gente: se va
    vete = (g['estado'], m.emocion_godzilla(W, c, g, S.now))
    filas_va = m.build_instances(W, c, S.now).get('godzilla', [])
    S.pasos(W, c, 6, [0])                   # 3 s: ya no esta
    fuera = (W['juego']['bien']['estado'], m.build_instances(W, c, S.now).get('godzilla'))
    S.pasos(W, c, 34, [])                   # 17 s sin nadie (y Esperamonstruo): vuelve
    vuelve = W['juego']['bien']
    t.check('con mal en el globo aparece tras Tvacia s de sala vacia (no antes) y va a por el mal, no por el '
            'publico; llega gente: se va (calma, adios, una fila sin sombra), desaparece y vuelve con la sala vacia',
            antes == 'espera' and sale and vete[0] == 'se_va' and vete[1] == ('calma', 'adios')
            and len(filas_va) == 1 and fuera == ('espera', []) and vuelve['n'] == 2
            and vuelve['estado'] != 'espera',
            'antes %s, %s -> %s, %s, %s, vuelve #%d %s' % (antes, g['estado'], g['objetivo'], vete, fuera[0],
                                                         vuelve['n'], vuelve['estado']))

    # 4. devora el mal y crea: el brote de la creacion
    W, c = S.nuevo(4)
    c = dict(c, t_vacia=0.0)
    _mal(m, W, c, a, 2, S.now)
    W['juego']['ultimoseq'][a] = 'arq'
    _poner(m, W, lejos, 6)
    g = m.aparecer_godzilla(W, c, S.now, junto)
    cara0 = m.emocion_godzilla(W, c, g, S.now)
    fz = m.build_instances(W, c, S.now).get('godzilla', [])
    celda_pasos = int(c['paso_monstruo']) // int(c['paso_juego'])     # v2: 8 pasos por celda (fase 33 v6)
    S.pasos(W, c, celda_pasos + 1)
    cara1 = m.emocion_godzilla(W, c, g, S.now)
    S.pasos(W, c, 3)
    J = W['juego']
    t.check('aparece serio (sprite y sombra en godzilla), va a la celda del mal (no a la del publico, mas '
            'prospera), la devora riendo con el ritmo de Trumpzilla (1 por paso) y deja un brote de la creacion: '
            'occ 1 con la especie del ultimo secuenciador (SEQ2: arquitectura)',
            cara0 == ('serio', 'respira') and len(fz) == 2 and int(fz[0][12]) == m.SPRITE_SOMBRA
            and cara1 == ('rie', 'devora') and W['occ'][a] == 1 and W['sp'][a] == m.ARQ and W['own'][a] == m.ARQ
            and g['acum'] == 2 and J['creados'] == 1 and g['creados'] == 1 and W['occ'][lejos] == 6,
            '%s %s occ %d sp %d acum %d creados %d' % (cara0, cara1, W['occ'][a], W['sp'][a], g['acum'],
                                                     J.get('creados', 0)))
    sin_mal = m.emocion_godzilla(W, c, g, S.now + 5.0)
    om = int(c['th_fusion'])
    _mal(m, W, c, otro, om, S.now)
    peq = m.comestible_bien(W, c, g, otro)
    g['acum'] = int(c['ocupacion_max'])
    m.actualizar_tam(c, g)
    t.check('sin mal que comer, calma; el pequeno no puede con una fusion del mal y el grande si; nunca come '
            'publico', sin_mal == ('calma', 'respira') and not peq and m.comestible_bien(W, c, g, otro)
            and not m.comestible_bien(W, c, g, lejos), '%s %s' % (sin_mal, peq))

    # 5. la lucha: se acercan al borde, manotazos Pasoslucha pasos y cada uno por donde vino
    W, c = S.nuevo(4)
    c = dict(c, t_vacia=0.0)
    v = junto
    d1 = [x for x in m.NEIGH[a] if x != v and x not in m.NEIGH[v]][0]
    d2 = [x for x in m.NEIGH[v] if x != a and x not in m.NEIGH[a] and x not in m.NEIGH[d1] and x != d1][0]
    _poner(m, W, a, 3)
    _mal(m, W, c, v, 2, S.now)
    mo = m.aparecer(W, c, S.now, a)
    mo['de'] = d1
    g = m.aparecer_godzilla(W, c, S.now, v)
    g['de'] = d2
    lucha = m.encuentro(W, c, S.now)
    J = W['juego']
    now = S.now + 0.7
    caras = (m.emocion_mon(W, c, mo, now), m.emocion_godzilla(W, c, g, now),
             m.emocion_mon(W, c, mo, now + m.T_MANOTAZO), m.emocion_godzilla(W, c, g, now + m.T_MANOTAZO))
    pm, nm_ = m.pos_monstruo(W, c, mo, now)
    hacia = m._hacia(nm_, pm, m._mul(m.normal_i(v), m._len(pm)))
    centro = m._mul(m.normal_i(a), m._len(pm))
    borde = m._dot(m._add(pm, centro, -1.0), hacia) > 0.0
    mira = m._dot(m.rumbo_mon(W, c, mo, pm, nm_), hacia) > 0.99
    S.pasos(W, c, 7)
    quietos = (mo['estado'], g['estado'], mo['celda'], g['celda'], W['occ'][a], W['occ'][v])
    leg = m._legend_lucha(W, c)
    S.pasos(W, c, 1)
    fin = (mo['estado'], g['estado'], mo['retira'], g['retira'], J.get('lucha'))
    t.check('en celdas contiguas, la lucha: se acercan al borde mirandose, uno da (furia, lucha) y el otro recibe '
            '(mueca, tiembla), por turnos; Pasoslucha pasos sin andar ni devorar; luego cada uno vuelve a la '
            'celda de la que venia',
            lucha and caras[0] == ('mueca', 'tiembla') and caras[1] == ('furia', 'lucha')
            and caras[2] == ('furia', 'lucha') and caras[3] == ('mueca', 'tiembla') and borde and mira
            and quietos == ('lucha', 'lucha', a, v, 3, 2) and 'manotazos 7/8' in leg
            and fin == ('busca', 'busca', d1, d2, None),
            '%s %s %s %s fin %s' % (lucha, caras, quietos, leg.strip(), fin))
    S.pasos(W, c, int(c['paso_monstruo']) // int(c['paso_juego']) + 1)     # v2: una celda, 8 pasos
    vuelta = (mo['celda'], g['celda'])
    muro = m.muro_tregua(W, c, mo)
    tregua = m.en_tregua(W)
    mo['celda'], mo['estado'], g['estado'] = d1, 'busca', 'busca'
    g['celda'] = [x for x in m.NEIGH[d1] if x != a][0]
    no_pelea = not m.encuentro(W, c, S.now)
    J['tregua']['hasta'] = J['paso']
    si_pelea = m.encuentro(W, c, S.now)
    t.check('vuelven (Trumpzilla a %d, Godzilla a %d); en la tregua cada uno evita la celda del otro y sus '
            'vecinas y no se pelean aunque se junten; acabada, si' % (d1, d2),
            vuelta == (d1, d2) and tregua and g['celda'] in m.NEIGH[d1] and no_pelea and si_pelea
            and J['luchas'] == 2, '%s tregua %s muro %d %s %s' % (vuelta, tregua, len(muro), no_pelea, si_pelea))

    # 6. la leyenda, Simgodzilla, Simlucha, Godzilla apagado y Modojuego apagado
    W, c = S.nuevo(4)
    _mal(m, W, c, a, 2, S.now)
    base.par.Simceldamon = a
    msg_l = m.sim_lucha(W, m.cfg(), S.now)
    leg_g = m._legend_godzilla(W, m.cfg())
    leg_l = m._legend_lucha(W, m.cfg())
    base.par.Godzilla = False
    c = m.cfg()
    sin = m.build_instances(W, c, S.now)
    S.pasos(W, c, 1)
    base.par.Godzilla = True
    base.par.Modojuego = False
    apagado = m.build_instances(W, m.cfg(), S.now).get('godzilla')
    t.check('Simlucha (manotazos), las lineas GODZILLA y LUCHA; Godzilla apagado: sin sprite y la lucha se acaba; '
            'Modojuego apagado: nada',
            'manotazos' in msg_l and leg_g.strip().startswith('GODZILLA #1  lucha') and 'manotazos 0/8' in leg_l
            and sin['godzilla'] == [] and W['juego'] is not None and W['juego'].get('lucha') is None
            and apagado == [], '%s | %s | %s' % (msg_l, leg_g.strip(), leg_l.strip()))

    # 7. sala vacia toda la ronda: el mal no se lo lleva todo, y el resultado es determinista
    def ronda(**over):
        S3 = SalaJuego(base, m, absTime.seconds + 6400.0, godzilla=True)
        W3, c3 = S3.nuevo(4)
        cfg_ = dict(c3, **over)
        for k, x in enumerate(sorted(m.cara_visible(cfg_))[::3]):
            _poner(m, W3, x, 2 + k % 4)
        m.aparecer(W3, cfg_, S3.now, a)
        for _ in range(40):
            S3.pasos(W3, cfg_, 4)
        J3 = W3['juego']
        return copy.deepcopy((W3['occ'], W3['sp'], J3['recuento'], J3.get('creados', 0), J3.get('luchas', 0)))
    r1 = ronda(t_vacia=0.0)
    r2 = ronda(t_vacia=0.0)
    solo = ronda(t_vacia=0.0, godzilla=0)
    t.check('sala vacia 160 pasos: con Godzilla el mal acaba con menos celdas que sin el (crea %d, luchas %d); '
            'dos veces la misma ronda, el mismo resultado' % (r1[3], r1[4]),
            r1 == r2 and r1[3] > 0 and r1[2]['mal'] < solo[2]['mal'],
            'mal %d con Godzilla, %d sin; publico %d / %d' % (r1[2]['mal'], solo[2]['mal'], r1[2]['publico'],
                                                            solo[2]['publico']))

    # 8. v3: con Oceano, Godzilla solo anda por tierra, como Trumpzilla; las carreteras cruzan el agua
    base.par.Tema = 'naturaleza'
    base.par.Oceano = True
    base.par.Montierra = True
    base.par.Modojuego = True
    W, c = S.nuevo(4)
    c = dict(c, t_vacia=0.0)
    dist, _ = m.dijkstra_mon(dict(W, juego=dict(zanjas={}, agua={})), dict(c, nivel=38), a)
    b = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    puente = [x for x in m.NEIGH[a] if b in m.NEIGH[x]][0]
    _poner(m, W, a, 2)                              # su isla: una celda del publico
    _mal(m, W, c, b, 2, S.now)                      # la presa, en la isla de enfrente
    W['tejido_vias'], W['vias_ind'] = [], []
    mar = m.mar_mon(W, c)
    g = m.aparecer_godzilla(W, c, S.now, a)
    sin_puente = (g['objetivo'], list(g['camino']))
    W['tejido_vias'] = [(a, puente), (puente, b)]   # una carretera sobre el agua
    m.recalcular_bien(W, c, g, S.now)
    por_via = (g['objetivo'], list(g['camino']), puente in m.mar_mon(W, c))
    W['tejido_vias'] = []
    m.recalcular_bien(W, c, g, S.now)
    g['camino'] = [puente, b]                       # un camino viejo que cruza el mar: no lo sigue
    g['mov'] = 1e6
    m.mover_godzilla(W, c, S.now)
    no_nada = (g['celda'], g['objetivo'])
    t.check('con Oceano, Godzilla solo anda por tierra, como Trumpzilla: con mar entre su isla y el mal no tiene '
            'objetivo ni lo cruza; con una carretera sobre el agua va por ella',
            puente in mar and a not in mar and b not in mar and sin_puente == (None, [])
            and por_via == (b, [puente, b], False) and no_nada == (a, None),
            'mar %d celdas; sin puente %s, por la carretera %s, camino viejo %s'
            % (len(mar), sin_puente, por_via, no_nada))


run_test(base, prueba)
print('  Ahora: Modojuego; Simmal y Simgodzilla: Godzilla devora el mal y crea. Simlucha: los dos')
print('  monstruos se dan manotazos 8 pasos y cada uno se va por donde vino.')
print('=' * 66)
