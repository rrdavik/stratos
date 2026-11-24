"""
=============================================================================
ESTRATOS - FASE 41: NEFANYAMUTO, EL SEGUNDO MONSTRUO DEL MAL
=============================================================================
Requiere la fase 40. Un MUTO (seis extremidades) con la cabeza de NefanyaMuto:
siembra el mal como Trumpzilla, cada uno por su cuenta. Si se juntan, bailan,
uno de los dos lanza su golpe especial, se giran y se van por caminos contrarios.

QUE HACE
--------
  APARECE      cuando la cara visible esta construida (del publico) Umbralnefa o
               mas (0,5: al 50 %), en la celda vacia de la cara visible por la que
               entran las celdas con el giro, lejos de Trumpzilla y de Godzilla.
               Si se ahoga, vuelve Esperamonstruo s despues.
  DEVORA       como Trumpzilla, con sus mismas reglas (objetivo, ritmo, dano,
               paso, tamano, solo por tierra, la luz), y deja brotes del mal. Cae
               en las zanjas del publico y se ahoga como el. Las armas de la fase
               37 son solo para Trumpzilla.
  BAILE        si Trumpzilla y NefanyaMuto quedan en celdas contiguas: se acercan
               al borde mirandose y bailan Tiemposbaile tiempos (8), sin andar ni
               devorar (rie y carcajada a cada tiempo). Luego uno de los dos
               (Golpebaile: al azar, o uno fijo) lanza SU GOLPE ESPECIAL:
                 Trumpzilla   absorbe para el mal todas las construcciones a
                              Radioabsorbe celdas (2) o menos de cualquiera de
                              los dos.
                 NefanyaMuto  se le enciende el anillo (un pulso electromagnetico
                              alrededor de la cabeza) y abre una zanja delante de
                              el, hacia Trumpzilla: Largozanjanefa celdas (5) en
                              linea, Profzanjanefa conchas (3) en la mas honda. Si
                              Trumpzilla queda dentro, cae.
               Despues se giran y se van por caminos contrarios, con Tregua pasos
               sin cruzarse ni volver a bailar.
  EMOCIONES    el atlas sprites/nefanyamuto_emociones.png (4 x 3: las diez caras
               de Trumpzilla y despiste y pasmado, en las que no se entera de nada).
               Sin nada que comer, pasmado; por la cara oculta, despiste.
  LEYENDA      NEFANYA  #1  busca  celda 40 -> 52  tam 0.62  acum 5/8   cara enfado
               BAILE    5/8 tiempos   celdas 40 | 41   (bailes 1, golpes T 0 / N 0, absorbidas 0)

OPERADORES (en /project1/FASE1)
-------------------------------
  nefanyamuto, i_nefanyamuto   Geometry COMP instanciado (una lamina: el sprite y
               su sombra) con mat_nefanyamuto (los shaders de Trumpzilla, con las
               animaciones nuevas: baile y anillo).
  nefanyamuto_atlas   Movie File In TOP con sprites/nefanyamuto_emociones.png (se
               rehace con sprites/hacer_atlas_nefanyamuto.py).

PROBAR
------
  Modojuego. Simnefa: aparece ya. Simbaile: Trumpzilla y NefanyaMuto en celdas
  vecinas bailan 8 tiempos y uno lanza su golpe (Golpebaile fija quien).

  v2 (comun v101): sus parametros, en la pagina Monstruos con los de los
  otros monstruos; un proyecto de antes los mueve alli y quita la Fase41.

COMO USARLO
-----------
  Copia la carpeta sprites del repositorio en la carpeta de los scripts y:
    exec(open('C:/Users/DareDave/Downloads/est/fase41_nefanyamuto.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase41 v2  (sus parametros, en la pagina Monstruos con los de todos los monstruos)'
banner(VERSION)

base = require_base(41)
motor = install_core(base, CARPETA, 41)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Monstruos)
# -----------------------------------------------------------------------------

# comun v101: en la pagina Monstruos, con los de los otros monstruos (antes, Fase41). Un
# proyecto de antes los pasa alli con su valor; la pagina Fase41, vacia, se quita
PARS_PAGINA = ('Nefanyamuto', 'Umbralnefa', 'Tiemposbaile', 'Golpebaile', 'Radioabsorbe', 'Largozanjanefa',
               'Profzanjanefa', 'Altonefa', 'Emocionnefa', 'Simnefa', 'Simbaile')
page, _movidos = sacar_a_monstruos(base, PARS_PAGINA)
add_par(base, page, 'header', 'Hnefa', 'NefanyaMuto (fase 41)')
add_par(base, page, 'toggle', 'Nefanyamuto', 'NefanyaMuto (el segundo monstruo del mal)', True)
add_par(base, page, 'float', 'Umbralnefa', 'Construido para que aparezca (0 a 1)', 0.5, 0.0, 1.0, clamp=True)
add_par(base, page, 'int', 'Tiemposbaile', 'Tiempos del baile', 8, 1, 64, clamp=True)
add_par(base, page, 'menu', 'Golpebaile', 'Quien lanza el golpe', 'azar', menu=list(m.GOLPES_BAILE),
        menu_labels=['Al azar', 'Trumpzilla', 'NefanyaMuto'])
add_par(base, page, 'int', 'Radioabsorbe', 'Golpe de Trumpzilla: radio (celdas)', 2, 0, 6, clamp=True)
add_par(base, page, 'int', 'Largozanjanefa', 'Golpe de NefanyaMuto: largo de la zanja', 5, 1, 12, clamp=True)
add_par(base, page, 'int', 'Profzanjanefa', 'Golpe de NefanyaMuto: conchas en lo mas hondo', 3, 1, 12, clamp=True)
add_par(base, page, 'float', 'Altonefa', 'Alto de NefanyaMuto (celdas, por tam)', 0.9, 0.2, 4.0, clamp=True)
add_par(base, page, 'menu', 'Emocionnefa', 'Emocion de NefanyaMuto', 'auto', menu=['auto'] + list(m.EMOCIONES_NEFA),
        menu_labels=['Auto (por su estado)'] + [e.capitalize() for e in m.EMOCIONES_NEFA])
add_par(base, page, 'pulse', 'Simnefa', 'Simular NefanyaMuto (aparece ya)')
add_par(base, page, 'pulse', 'Simbaile', 'Simular el baile (junto a Trumpzilla)')
monstruos_al_dia(base, _movidos)
ok('pagina Monstruos (Fase41): Nefanyamuto, Umbralnefa 0,5, Tiemposbaile 8, Golpebaile (azar), Radioabsorbe 2, '
   'Largozanjanefa 5, Profzanjanefa 3, Altonefa 0,9, Emocionnefa (auto), Simnefa, Simbaile')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

materiales_piel(base)                   # mat_respaldo, para Materialrespaldo
trumpzilla_al_dia(base, CARPETA)        # los shaders (con el baile y el anillo)
nefanyamuto_al_dia(base, CARPETA)
set_render(base)

leeme(base, 41, """FASE 41 - NEFANYAMUTO, EL SEGUNDO MONSTRUO DEL MAL
  Un MUTO con la cabeza de NefanyaMuto. Aparece cuando la cara visible esta
  construida Umbralnefa (al 50 %) y siembra el mal como Trumpzilla, por su
  cuenta. Si se juntan, bailan Tiemposbaile tiempos (8) y uno de los dos
  (Golpebaile) lanza su golpe: Trumpzilla absorbe para el mal las
  construcciones a Radioabsorbe celdas (2); NefanyaMuto enciende su anillo y
  abre una zanja de Largozanjanefa celdas (5) hacia Trumpzilla, Profzanjanefa
  conchas (3) en lo mas hondo. Luego se giran y se van por caminos contrarios.
  Simnefa: aparece ya. Simbaile: el baile junto a Trumpzilla.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS41 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Spritemonstruo', 'Emocion', 'Godzilla', 'Nefanyamuto', 'Umbralnefa', 'Tiemposbaile', 'Golpebaile',
          'Radioabsorbe', 'Largozanjanefa', 'Profzanjanefa', 'Altonefa', 'Emocionnefa', 'Tregua', 'Simceldamon',
          'Tema', 'Oceano', 'Montierra')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS41)
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


def _cara(m, fila):
    k = int(round(fila[12]))
    return m.EMOCIONES_NEFA[k % 16], m.ANIMS_MON[k // 16]


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # Trumpzilla no aparece solo (salvo donde se pide)
    base.par.Spritemonstruo = True
    base.par.Emocion = 'auto'
    for nm, v in (('Umbralnefa', 0.5), ('Tiemposbaile', 8), ('Golpebaile', 'azar'), ('Radioabsorbe', 2),
                  ('Largozanjanefa', 5), ('Profzanjanefa', 3), ('Altonefa', 0.9), ('Emocionnefa', 'auto'),
                  ('Tregua', 16)):
        setattr(base.par, nm, v)
    S = SalaJuego(base, m, absTime.seconds + 7100.0, nefanya=True)

    # 1. el atlas, los operadores y el render
    cols, filas = m.ATLAS_MON
    med = _png_medidas(CARPETA + '/' + NEFA_ATLAS)
    mat = base.op('mat_nefanyamuto')
    nombres = str(base.op('render').par.geometry.val).split()
    t.check('el atlas sprites/nefanyamuto_emociones.png (%d x %d celdas de 192 x 256: doce caras, las diez y '
            'despiste y pasmado); nefanyamuto, i_nefanyamuto y mat_nefanyamuto (sampler sAtlas -> '
            'nefanyamuto_atlas); los shaders con el baile y el anillo; el render dibuja nefanyamuto' % (cols, filas),
            med == (cols * 192, filas * 256) and len(m.EMOCIONES_NEFA) == cols * filas
            and base.op('nefanyamuto_atlas') is not None
            and all(base.op(n) is not None for n in ('nefanyamuto', 'i_nefanyamuto'))
            and mat is not None and str(mat.par.sampler0name.eval()) == 'sAtlas'
            and str(mat.par.vec0name.eval()) == 'uSprite' and 'nefanyamuto' in nombres
            and 'anim == 9' in base.op('sprite_vertex').text and 'anim == 10' in base.op('sprite_pixel').text
            and 'i_nefanyamuto' in m.chop_names(m.cfg()), '%s' % (med,))

    vis_ = sorted(m.cara_visible(m.cfg()))
    a = vis_[len(vis_) // 2] if vis_ else m.N // 2
    W, c = S.nuevo(4)
    dist, _ = m.dijkstra_mon(W, c, a)
    lejos = min(x for x in dist if abs(dist[x] - 3.0) < 1e-9)

    # 2. la logica de la fase 40, sin NefanyaMuto o con el mundo construido por debajo de Umbralnefa
    def partida(cfg_):
        S2 = SalaJuego(base, m, absTime.seconds + 7600.0, nefanya=True)
        W2, _ = S2.nuevo(4)
        for k, x in enumerate(vis_[::5]):
            _poner(m, W2, x, 2 + k % 3)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(16):
            S2.pasos(W2, cfg_, 2)
            m.build_instances(W2, cfg_, S2.now)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento'])), J.get('nefa')
    c = m.cfg()
    r40, _ = partida(dict(c, nivel=40))
    r_off, _ = partida(dict(c, nefanya=0))
    r_bajo, n_bajo = partida(c)
    t.check('sin NefanyaMuto, o con la cara visible construida por debajo de Umbralnefa, el juego da lo mismo '
            'que tras la fase 40 (NefanyaMuto no sale)',
            r_off == r40 and r_bajo == r40 and r40[2]['comidos'] > 0 and (n_bajo or {}).get('n', 0) == 0,
            'comidos %d; iguales: apagado %s, por debajo %s; nefa %s'
            % (r40[2]['comidos'], r_off == r40, r_bajo == r40, (n_bajo or {}).get('estado')))

    # 3. aparece al 50 % construido, lejos de Trumpzilla, y va a por el publico
    W, c = S.nuevo(4)
    vis = sorted(m.cara_visible(c))
    mitad = (len(vis) + 1) // 2
    libres = [x for x in vis if x != a and x not in m.NEIGH[a]]
    for x in libres[:mitad - 1]:
        _poner(m, W, x, 2)
    mo = m.aparecer(W, c, S.now, a)
    S.pasos(W, c, 2)
    antes = (W['juego'].get('nefa') or {}).get('estado', 'espera')
    pct_antes = m.construida_visible(W, c)
    leg0 = m._legend_nefa(W, c)
    _poner(m, W, libres[mitad - 1], 2)
    S.pasos(W, c, 1)
    x = W['juego']['nefa']
    sale = x['estado'] in ('aparece', 'busca', 'devora') and x['celda'] not in ({mo['celda']} | set(m.NEIGH[mo['celda']]))
    presa = x['objetivo'] is not None and W['sp'][x['objetivo']] != m.MAL and W['occ'][x['objetivo']] > 0
    t.check('al %.0f %% construido no sale (espera); al %.0f %%, aparece lejos de Trumpzilla y va a por una '
            'construccion del publico' % (100 * pct_antes, 100 * m.construida_visible(W, c)),
            antes == 'espera' and pct_antes < 0.5 and 'espera' in leg0 and sale and presa,
            '%s %s -> %s celda %s objetivo %s | %s' % (antes, pct_antes, x['estado'], x['celda'], x['objetivo'],
                                                       leg0.strip()))

    # 4. devora como Trumpzilla y deja un brote del mal; las caras; cae en las zanjas
    W, c = S.nuevo(4)
    junto = m.NEIGH[a][0]
    _poner(m, W, a, 2)
    x = m.aparecer_nefa(W, c, S.now, junto)
    cara0 = m.emocion_nefa(W, c, x, S.now)
    fz = m.build_instances(W, c, S.now).get('nefanyamuto', [])
    celda_pasos = int(c['paso_monstruo']) // int(c['paso_juego'])
    S.pasos(W, c, celda_pasos + 1)
    cara1 = m.emocion_nefa(W, c, x, S.now)
    S.pasos(W, c, 4)
    brote = (W['occ'][a], W['sp'][a])
    sin = m.emocion_nefa(W, c, x, S.now + 5.0)
    fila_sin = m.build_instances(W, c, S.now + 5.0).get('nefanyamuto', [])
    t.check('aparece serio (sprite y sombra en nefanyamuto), va a la construccion, la devora riendo y deja un '
            'brote del mal; sin nada que comer, pasmado (la cara 11 del atlas)',
            cara0 == ('serio', 'respira') and len(fz) == 2 and int(fz[0][12]) == m.SPRITE_SOMBRA
            and cara1 == ('rie', 'devora') and brote == (1, m.MAL) and x['comidos'] >= 2
            and sin == ('pasmado', 'respira') and _cara(m, fila_sin[-1]) == ('pasmado', 'respira'),
            '%s %s brote %s comidos %d sin %s' % (cara0, cara1, brote, x['comidos'], sin))
    x['acum'] = 3
    m.cavar_zanja(W, c, x['celda'], 1, S.now)
    t.check('cae en las zanjas del publico como Trumpzilla (acum 0, susto)',
            x['estado'] == 'cae' and x['acum'] == 0 and m.emocion_nefa(W, c, x, S.now)[0] == 'susto',
            '%s acum %d' % (x['estado'], x['acum']))

    # 5. el baile: 8 tiempos cara a cara; el golpe de Trumpzilla; se van por caminos contrarios
    def preparar(golpe):
        base.par.Golpebaile = golpe
        W, c = S.nuevo(4)
        v = m.NEIGH[a][0]
        zona = set(q for p in (a, v) for q, _ in m.rings(p, 2)) - {a, v}
        fuera = [q for q, d in m.rings(a, 4) if d == 4]
        for q in sorted(zona)[::2]:
            _poner(m, W, q, 2)
        _poner(m, W, fuera[0], 3)
        mo = m.aparecer(W, c, S.now, a)
        x = m.aparecer_nefa(W, c, S.now, v)
        return W, c, v, zona, fuera[0], mo, x
    W, c, v, zona, fuera, mo, x = preparar('trumpzilla')
    baila = m.encuentro_baile(W, c, S.now)
    J = W['juego']
    pub0 = sorted(q for q in zona if W['occ'][q] > 0 and W['sp'][q] != m.MAL)
    caras = []
    for k in range(4):
        S.semis(W, c, 4)
        caras.append((m.emocion_mon(W, c, mo, S.now), m.emocion_nefa(W, c, x, S.now)))
    pm, nm_ = m.pos_monstruo(W, c, mo, S.now)
    hacia = m._hacia(nm_, pm, m._mul(m.normal_i(v), m._len(pm)))
    borde = m._dot(m._add(pm, m._mul(m.normal_i(a), m._len(pm)), -1.0), hacia) > 0.0
    mira = m._dot(m.rumbo_mon(W, c, mo, pm, nm_), hacia) > 0.99
    leg = m._legend_baile(W, c)
    S.semis(W, c, 15)
    quietos = (mo['estado'], x['estado'], mo['celda'], x['celda'], J['baile']['golpe'])
    S.semis(W, c, 1)
    golpe = (J['baile']['golpe'], m.emocion_mon(W, c, mo, S.now), m.emocion_nefa(W, c, x, S.now))
    pub1 = [q for q in pub0 if W['sp'][q] == m.MAL]
    occ_igual = all(W['occ'][q] > 0 for q in pub0)
    S.semis(W, c, 8)
    fin = (mo['estado'], x['estado'], mo['retira'], x['retira'], J.get('baile'))
    lejos_m = m._dot(m.normal_i(mo['retira']), m.normal_i(v)) < m._dot(m.normal_i(a), m.normal_i(v)) \
        if mo['retira'] is not None else False
    lejos_x = m._dot(m.normal_i(x['retira']), m.normal_i(a)) < m._dot(m.normal_i(v), m.normal_i(a)) \
        if x['retira'] is not None else False
    t.check('juntos, el baile: cara a cara en el borde, rie y carcajada a cada tiempo (los dos, animacion baile), '
            '8 tiempos sin andar ni devorar; el golpe de Trumpzilla (furia; NefanyaMuto, despiste) absorbe para el '
            'mal las %d construcciones a 2 celdas (con lo que tenian) y no la de 4; luego se giran y se van cada '
            'uno a la vecina mas lejos del otro' % len(pub0),
            baila and caras[0][0] == ('carcajada', 'baile') and caras[1][0] == ('rie', 'baile')
            and caras[0][1] == ('carcajada', 'baile') and borde and mira and '4/8 tiempos' in leg
            and quietos == ('baile', 'baile', a, v, None)
            and golpe == ('trumpzilla', ('furia', 'lucha'), ('despiste', 'tiembla'))
            and len(pub1) == len(pub0) > 0 and occ_igual and W['sp'][fuera] != m.MAL
            and fin[:2] == ('busca', 'busca') and fin[4] is None and lejos_m and lejos_x,
            '%s caras %s borde %s mira %s | %s | %s golpe %s absorbidas %d/%d fin %s'
            % (baila, caras[:2], borde, mira, leg.strip(), quietos, golpe, len(pub1), len(pub0), fin))
    S.pasos(W, c, int(c['paso_monstruo']) // int(c['paso_juego']) + 1)
    vuelta = (mo['celda'], x['celda'])
    tregua = m.en_tregua_baile(W)
    muro = m.muro_tregua(W, c, x)
    x['celda'] = [q for q in m.NEIGH[mo['celda']]][0]
    x['estado'] = mo['estado'] = 'busca'
    no_baila = not m.encuentro_baile(W, c, S.now)
    J['tregua_baile']['hasta'] = J['paso']
    si_baila = m.encuentro_baile(W, c, S.now)
    t.check('se van (Trumpzilla a %s, NefanyaMuto a %s); en la tregua cada uno evita al otro y no vuelven a '
            'bailar aunque se junten; acabada, si' % vuelta,
            tregua and len(muro) > 0 and no_baila and si_baila and J['bailes'] == 2,
            'tregua %s muro %d %s %s' % (tregua, len(muro), no_baila, si_baila))

    # 6. el golpe de NefanyaMuto: el anillo y la zanja de 5 celdas hacia Trumpzilla (1 2 3 2 1 conchas)
    W, c, v, zona, fuera, mo, x = preparar('nefanyamuto')
    m.encuentro_baile(W, c, S.now)
    J = W['juego']
    linea = m.linea_zanja(W, c, v, a, 5)
    S.semis(W, c, 32)
    cara_g = m.emocion_nefa(W, c, x, S.now)
    fila_g = m.build_instances(W, c, S.now).get('nefanyamuto', [])
    profs = [J['zanjas'].get(q, 0) for q in linea]
    S.semis(W, c, 8)
    t.check('el golpe de NefanyaMuto: furia con el anillo (animacion anillo en su sprite) y una zanja de 5 celdas '
            'en linea hacia Trumpzilla, %s conchas (3 en medio); Trumpzilla, en la primera, cae; luego NefanyaMuto '
            'se va' % profs,
            J.get('golpes', {}).get('nefanyamuto') == 1 and cara_g == ('furia', 'anillo')
            and _cara(m, fila_g[-1]) == ('furia', 'anillo') and linea[0] == a and len(linea) == 5
            and profs == [1, 2, 3, 2, 1] and mo['caidas'] >= 1 and x['estado'] == 'busca'
            and J.get('baile') is None and m.perfil_zanja(4, 3) == [1, 2, 2, 1],
            'golpes %s cara %s linea %s profs %s trump %s caidas %d nefa %s'
            % (J.get('golpes'), cara_g, linea, profs, mo['estado'], mo['caidas'], x['estado']))

    # 7. al azar: determinista, y salen los dos golpes
    base.par.Golpebaile = 'azar'
    W, c = S.nuevo(4)
    J = W['juego']
    quienes = []
    for k in range(1, 13):
        J['baile'] = dict(n=k, mon=a, nefa=m.NEIGH[a][k % len(m.NEIGH[a])])
        quienes.append(m.quien_golpea(W, c))
    J['baile'] = None
    otra = []
    for k in range(1, 13):
        J['baile'] = dict(n=k, mon=a, nefa=m.NEIGH[a][k % len(m.NEIGH[a])])
        otra.append(m.quien_golpea(W, c))
    J['baile'] = None
    t.check('Golpebaile al azar: unas veces Trumpzilla y otras NefanyaMuto (%d / %d en 12 bailes), y la misma '
            'partida da lo mismo' % (quienes.count('trumpzilla'), quienes.count('nefanyamuto')),
            quienes == otra and 'trumpzilla' in quienes and 'nefanyamuto' in quienes, '%s' % quienes)

    # 8. Simnefa, Simbaile, la leyenda, Nefanyamuto apagado y Modojuego apagado
    W, c = S.nuevo(4)
    base.par.Simceldamon = a
    msg_b = m.sim_baile(W, m.cfg(), S.now)
    leg_n = m._legend_nefa(W, m.cfg())
    leg_b = m._legend_baile(W, m.cfg())
    base.par.Nefanyamuto = False
    c = m.cfg()
    sin = m.build_instances(W, c, S.now)
    S.pasos(W, c, 1)
    base.par.Nefanyamuto = True
    base.par.Modojuego = False
    apagado = m.build_instances(W, m.cfg(), S.now).get('nefanyamuto')
    t.check('Simbaile (bailan), las lineas NEFANYA y BAILE; Nefanyamuto apagado: sin sprite y el baile se acaba '
            '(Trumpzilla sigue); Modojuego apagado: nada',
            'bailan' in msg_b and leg_n.strip().startswith('NEFANYA  #1  baile') and '0/8 tiempos' in leg_b
            and sin['nefanyamuto'] == [] and W['juego'] is not None and W['juego'].get('baile') is None
            and apagado == [], '%s | %s | %s' % (msg_b, leg_n.strip(), leg_b.strip()))


run_test(base, prueba)
print('  Ahora: Modojuego; Simnefa: NefanyaMuto aparece. Simbaile: bailan 8 tiempos y uno lanza su')
print('  golpe (Golpebaile: Trumpzilla absorbe las construcciones; NefanyaMuto, el anillo y la zanja).')
print('=' * 66)
