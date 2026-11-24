"""
=============================================================================
ESTRATOS - FASE 42: EL GODZILLA AZUL, EL SEGUNDO MONSTRUO DEL BIEN
=============================================================================
Requiere la fase 41. Con Trumpzilla y NefanyaMuto a la vez en el planeta el mal
hacia mucho dano: el Godzilla verde solo puede con uno. Esta fase pone otro
Godzilla, azul, que lucha por el bien.

QUE HACE
--------
  CUANDO       solo mientras los DOS monstruos del mal estan en pie a la vez
               (Trumpzilla y NefanyaMuto, ni esperando ni ahogados), con o sin
               gente en la sala. Si queda uno solo, se va: saluda con la flor y se
               hunde. Vuelve cuando vuelven a estar los dos (como pronto
               Esperamonstruo s despues de irse).
  APARECE      en la celda vacia de la cara visible por la que entran las celdas
               con el giro, lejos de los otros tres monstruos. En tierra.
  DEVORA EL MAL  con las reglas del Godzilla verde (objetivo, ritmo, dano, paso,
               tamano, solo por tierra) y deja brotes de la creacion.
  LUCHA        su rival es NefanyaMuto (el verde sigue con Trumpzilla): si quedan
               en celdas contiguas, la lucha de la fase 40 (al borde, manotazos
               Pasoslucha pasos, cada uno por donde vino y Tregua pasos sin
               cruzarse). NefanyaMuto, furia cuando da y mueca cuando recibe.
  EMOCIONES    las diez caras del Godzilla verde, en su atlas azul
               (sprites/godzilla_azul_emociones.png: piel azul cobalto, tripa gris
               perla y placas de hielo cian; se rehace con
               sprites/hacer_atlas_godzilla_azul.py).
  LEYENDA      AZUL     #1  devora  celda 12 -> 12  tam 0.75  acum 4/8   cara rie   luchas 1
               AZUL     #0  espera   del mal en pie 1 (aparece con 2)   luchas 0

OPERADORES (en /project1/FASE1)
-------------------------------
  godzilla_azul, i_godzilla_azul   Geometry COMP instanciado (una lamina: el
               sprite y su sombra) con mat_godzilla_azul (los shaders de Trumpzilla).
  godzilla_azul_atlas   Movie File In TOP con sprites/godzilla_azul_emociones.png.

PARAMETROS (pagina Monstruos)
-----------------------------
  Godzillaazul, Altoazul, Emocionazul, Simazul, Simluchaazul.

PROBAR
------
  Modojuego. Simluchaazul: Trumpzilla, NefanyaMuto y el Godzilla azul junto a
  NefanyaMuto: se dan manotazos. Simazul: aparece ya (si no estan los dos del
  mal, se va enseguida).

COMO USARLO
-----------
  Copia la carpeta sprites del repositorio en la carpeta de los scripts y:
    exec(open('C:/Users/DareDave/Downloads/est/fase42_godzilla_azul.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase42 v1  (el Godzilla azul: con los dos monstruos del mal a la vez, lucha por el bien)'
banner(VERSION)

base = require_base(42)
motor = install_core(base, CARPETA, 42)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Monstruos)
# -----------------------------------------------------------------------------

PARS_PAGINA = ('Godzillaazul', 'Altoazul', 'Emocionazul', 'Simazul', 'Simluchaazul')
page, _movidos = sacar_a_monstruos(base, PARS_PAGINA)
add_par(base, page, 'header', 'Hazul', 'Godzilla azul (fase 42)')
add_par(base, page, 'toggle', 'Godzillaazul', 'Godzilla azul (sale con los dos monstruos del mal)', True)
add_par(base, page, 'float', 'Altoazul', 'Alto del Godzilla azul (celdas, por tam)', 0.8, 0.2, 4.0, clamp=True)
add_par(base, page, 'menu', 'Emocionazul', 'Emocion del Godzilla azul', 'auto', menu=['auto'] + list(m.EMOCIONES_MON),
        menu_labels=['Auto (por su estado)'] + [e.capitalize() for e in m.EMOCIONES_MON])
add_par(base, page, 'pulse', 'Simazul', 'Simular el Godzilla azul (aparece ya)')
add_par(base, page, 'pulse', 'Simluchaazul', 'Simular su lucha (junto a NefanyaMuto)')
monstruos_al_dia(base, _movidos)
ok('pagina Monstruos (Fase42): Godzillaazul, Altoazul 0,8, Emocionazul (auto), Simazul, Simluchaazul')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

materiales_piel(base)                   # mat_respaldo, para Materialrespaldo
trumpzilla_al_dia(base, CARPETA)        # los shaders
godzilla_azul_al_dia(base, CARPETA)
set_render(base)

leeme(base, 42, """FASE 42 - EL GODZILLA AZUL, EL SEGUNDO MONSTRUO DEL BIEN
  Con Trumpzilla y NefanyaMuto a la vez en el planeta, sale otro Godzilla,
  azul, que lucha por el bien: devora el mal y deja brotes de la creacion,
  como el verde. Su rival es NefanyaMuto: si se juntan, manotazos Pasoslucha
  pasos y Tregua pasos sin cruzarse (el verde sigue con Trumpzilla). Si queda
  un solo monstruo del mal, se va saludando. Simazul: aparece ya.
  Simluchaazul: su lucha junto a NefanyaMuto.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS42 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Spritemonstruo', 'Emocion', 'Godzilla', 'Nefanyamuto', 'Godzillaazul', 'Umbralnefa', 'Pasoslucha',
          'Tregua', 'Altoazul', 'Emocionazul', 'Simceldamon', 'Tema', 'Oceano', 'Montierra')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS42)
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
    base.par.Umbralnefa = 1.0               # NefanyaMuto tampoco
    base.par.Spritemonstruo = True
    base.par.Emocion = 'auto'
    for nm, v in (('Pasoslucha', 8), ('Tregua', 16), ('Altoazul', 0.8), ('Emocionazul', 'auto')):
        setattr(base.par, nm, v)
    S = SalaJuego(base, m, absTime.seconds + 8100.0, nefanya=True, azul=True)

    # 1. el atlas, los operadores y el render
    cols, filas = m.ATLAS_MON
    med = _png_medidas(CARPETA + '/' + AZUL_ATLAS)
    mat = base.op('mat_godzilla_azul')
    nombres = str(base.op('render').par.geometry.val).split()
    t.check('el atlas sprites/godzilla_azul_emociones.png (%d x %d celdas de 192 x 256); godzilla_azul, '
            'i_godzilla_azul y mat_godzilla_azul (sampler sAtlas -> godzilla_azul_atlas); el render dibuja '
            'godzilla_azul' % (cols, filas),
            med == (cols * 192, filas * 256) and base.op('godzilla_azul_atlas') is not None
            and all(base.op(n) is not None for n in ('godzilla_azul', 'i_godzilla_azul'))
            and mat is not None and str(mat.par.sampler0name.eval()) == 'sAtlas'
            and str(mat.par.vec0name.eval()) == 'uSprite' and 'godzilla_azul' in nombres
            and 'i_godzilla_azul' in m.chop_names(m.cfg()), '%s' % (med,))

    vis_ = sorted(m.cara_visible(m.cfg()))
    a = vis_[len(vis_) // 2] if vis_ else m.N // 2
    W, c = S.nuevo(4)
    dist, _ = m.dijkstra_mon(W, c, a)
    junto = m.NEIGH[a][0]
    vis_set = set(vis_)
    # dos celdas de la cara visible lejos de a (y entre si) para los del mal que no deben molestar
    lejos4 = sorted(x for x in dist if abs(dist[x] - 4.0) < 1e-9 and x in vis_set)
    t1 = lejos4[0]
    d1, _ = m.dijkstra_mon(W, c, t1)
    n1 = max((x for x in lejos4 if x in d1), key=lambda x: (d1[x], -x))

    # 2. con un solo monstruo del mal (o el azul apagado), la partida de la fase 41
    def partida(cfg_):
        S2 = SalaJuego(base, m, absTime.seconds + 8600.0, nefanya=True, azul=True)
        W2, _ = S2.nuevo(4)
        for k, x in enumerate(vis_[::7]):
            _poner(m, W2, x, 2 + k % 3)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(16):
            S2.pasos(W2, cfg_, 2)
            m.build_instances(W2, cfg_, S2.now)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento'])), J.get('azul')
    c = m.cfg()
    r41, _ = partida(dict(c, nivel=41))
    r_off, _ = partida(dict(c, azul=0))
    r_uno, az_uno = partida(c)
    t.check('con un solo monstruo del mal, o con Godzillaazul apagado, el juego da lo mismo que tras la fase 41 '
            '(el azul no sale)',
            r_off == r41 and r_uno == r41 and r41[2]['comidos'] > 0 and (az_uno or {}).get('n', 0) == 0,
            'comidos %d; iguales: apagado %s, uno solo %s; azul %s'
            % (r41[2]['comidos'], r_off == r41, r_uno == r41, (az_uno or {}).get('estado')))

    # 3. con los dos del mal en pie, aparece lejos de ellos y va a por el mal; si queda uno, se va
    W, c = S.nuevo(4)
    _mal(m, W, c, a, 2, S.now)
    S.pasos(W, c, 1)
    antes = W['juego'].get('azul', {}).get('estado', 'espera') if W['juego'].get('azul') else 'espera'
    mo = m.aparecer(W, c, S.now, t1)
    x = m.aparecer_nefa(W, c, S.now, n1)
    S.pasos(W, c, 1)
    g = W['juego'].get('azul') or {}
    cerca = {t1, n1} | set(m.NEIGH[t1]) | set(m.NEIGH[n1])
    sale = g.get('estado') in ('aparece', 'busca', 'devora') and g.get('celda') not in cerca \
        and g.get('objetivo') == a
    leg_sale = m._legend_azul(W, c)
    x.update(estado='muere', t_muerte=S.now)
    S.pasos(W, c, 1)
    vete = (g.get('estado'), m.emocion_azul(W, c, g, S.now))
    filas_va = m.build_instances(W, c, S.now).get('godzilla_azul', [])
    S.pasos(W, c, 6)
    fuera = (W['juego']['azul']['estado'], m.build_instances(W, c, S.now).get('godzilla_azul'))
    t.check('sin los dos del mal no sale; con Trumpzilla y NefanyaMuto en pie aparece lejos de ellos y va a por el '
            'mal; si NefanyaMuto se ahoga, se va (calma, adios, sin sombra) y desaparece',
            antes == 'espera' and sale and vete[0] == 'se_va' and vete[1] == ('calma', 'adios')
            and len(filas_va) == 1 and fuera == ('espera', []) and 'AZUL     #1' in leg_sale,
            'antes %s, %s celda %s -> %s, %s, %s | %s' % (antes, g.get('estado'), g.get('celda'), g.get('objetivo'),
                                                       vete, fuera[0], leg_sale.strip()))

    # 4. devora el mal y crea, como el verde
    W, c = S.nuevo(4)
    _mal(m, W, c, a, 2, S.now)
    W['juego']['ultimoseq'][a] = 'geo'
    m.aparecer(W, c, S.now, t1)
    m.aparecer_nefa(W, c, S.now, n1)
    g = m.aparecer_azul(W, c, S.now, junto)
    cara0 = m.emocion_azul(W, c, g, S.now)
    fz = m.build_instances(W, c, S.now).get('godzilla_azul', [])
    celda_pasos = int(c['paso_monstruo']) // int(c['paso_juego'])
    S.pasos(W, c, celda_pasos + 1)
    cara1 = m.emocion_azul(W, c, g, S.now)
    S.pasos(W, c, 3)
    t.check('aparece serio (sprite y sombra en godzilla_azul), va al mal, lo devora riendo y deja un brote de la '
            'creacion (occ 1, naturaleza)',
            cara0 == ('serio', 'respira') and len(fz) == 2 and int(fz[0][12]) == m.SPRITE_SOMBRA
            and _cara(m, fz[-1]) == ('serio', 'respira') and cara1 == ('rie', 'devora')
            and W['occ'][a] == 1 and W['sp'][a] == m.GEO and g['creados'] == 1,
            '%s %s occ %d sp %d creados %d estado %s' % (cara0, cara1, W['occ'][a], W['sp'][a], g.get('creados', 0),
                                                        g['estado']))

    # 5. la lucha con NefanyaMuto: manotazos Pasoslucha pasos y cada uno por donde vino; la tregua
    W, c = S.nuevo(4)
    _mal(m, W, c, junto, 2, S.now)
    m.aparecer(W, c, S.now, t1)
    x = m.aparecer_nefa(W, c, S.now, a)
    g = m.aparecer_azul(W, c, S.now, junto)
    lucha = m.encuentro_azul(W, c, S.now)
    J = W['juego']
    now = S.now + 0.7
    caras = (m.emocion_nefa(W, c, x, now), m.emocion_azul(W, c, g, now),
             m.emocion_nefa(W, c, x, now + m.T_MANOTAZO), m.emocion_azul(W, c, g, now + m.T_MANOTAZO))
    leg = m._legend_azul(W, c)
    S.pasos(W, c, int(c['pasos_lucha']) - 1)
    quietos = (x['estado'], g['estado'], x['celda'], g['celda'])
    S.pasos(W, c, 1)
    fin = (x['estado'], g['estado'], J.get('lucha_azul'), m.en_tregua_azul(W))
    muro = m.muro_tregua(W, c, g)
    x['celda'], x['estado'], g['estado'] = a, 'busca', 'busca'
    g['celda'] = junto
    no_lucha = not m.encuentro_azul(W, c, S.now)
    J['tregua_azul']['hasta'] = J['paso']
    si_lucha = m.encuentro_azul(W, c, S.now)
    t.check('junto a NefanyaMuto, la lucha: furia y mueca por turnos (los dos), %d pasos quietos; luego cada uno '
            'por donde vino; en la tregua no vuelven a luchar y el azul evita a NefanyaMuto; acabada, si'
            % int(c['pasos_lucha']),
            lucha and caras[0][0] != caras[2][0] and {caras[0][0], caras[1][0]} == {'furia', 'mueca'}
            and {caras[2][0], caras[3][0]} == {'furia', 'mueca'} and 'lucha' in leg
            and quietos == ('lucha', 'lucha', a, junto) and fin[:2] == ('busca', 'busca') and fin[2] is None
            and fin[3] and len(muro) > 0 and no_lucha and si_lucha and J['luchas_azul'] == 2,
            '%s caras %s | %s | %s fin %s muro %d %s %s' % (lucha, caras, leg.strip(), quietos, fin, len(muro),
                                                            no_lucha, si_lucha))

    # 6. Simluchaazul, Simazul, Godzillaazul apagado y Modojuego apagado
    W, c = S.nuevo(4)
    base.par.Simceldamon = t1
    msg = m.sim_lucha_azul(W, m.cfg(), S.now)
    leg = m._legend_azul(W, m.cfg())
    base.par.Godzillaazul = False
    c = m.cfg()
    sin = m.build_instances(W, c, S.now)
    S.pasos(W, c, 1)
    acaba = W['juego'].get('lucha_azul') is None and W['juego']['nefa']['estado'] != 'lucha'
    base.par.Godzillaazul = True
    W2, c2 = S.nuevo(4)
    msg_s = m.sim_azul(W2, c2, S.now)
    base.par.Modojuego = False
    apagado = m.build_instances(W, m.cfg(), S.now).get('godzilla_azul')
    t.check('Simluchaazul (manotazos con NefanyaMuto) y la linea AZUL; Godzillaazul apagado: sin sprite y la '
            'lucha se acaba; Simazul aparece; Modojuego apagado: nada',
            'manotazos' in msg and 'lucha' in leg and sin['godzilla_azul'] == [] and acaba
            and 'aparece' in msg_s and apagado == [],
            '%s | %s | %s' % (msg, leg.strip(), msg_s))


run_test(base, prueba)
print('  Ahora: Modojuego; Simluchaazul: el Godzilla azul y NefanyaMuto se dan manotazos.')
print('  En partida, sale solo cuando Trumpzilla y NefanyaMuto estan a la vez en el planeta.')
print('=' * 66)
