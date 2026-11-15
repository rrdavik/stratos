"""
=============================================================================
ESTRATOS - FASE 38: TRUMPZILLA, EL MONSTRUO EN SPRITE CON EMOCIONES
=============================================================================
Requiere la fase 37. Cambia lo visual del monstruo (provisional en la fase 33:
una esfera con dos ojos) por un sprite: Trumpzilla, un atlas de diez caras que
cambian con lo que le pasa en la partida. La logica del juego no cambia.

QUE HACE
--------
  SPRITE       una lamina de pie sobre su celda, con los pies en el suelo, que
               mira siempre a la camara, con su sombra en el suelo. Su arriba es
               el de la pantalla, inclinado hacia la vertical del planeta (de pie
               hacia fuera) Inclinasprite grados como mucho (30): en el borde
               del globo o en el sur no se tumba ni queda boca abajo; 180, siempre
               la vertical del planeta. Sigue el giro del planeta, avanza entre
               celdas como el monstruo y se voltea hacia donde camina. Su alto,
               Altosprite celdas por tam (crece con lo que devora).
  EMOCIONES    la cara sale del estado del monstruo (la primera que vale):
                 se ahoga            panico     se hunde 2 s y desaparece
                 petrificado (37)    calma      gris piedra, quieto
                 aturdido (37)       mueca      se tambalea y parpadea
                 cae en una zanja    susto      tiembla (1,5 s)
                 su zanja con agua   panico     tiembla
                 en una zanja        llora
                 pisoton (37)        llora      tiembla
                 acorralado (37)     panico     tiembla
                 devora              rie        mastica (carcajada si es grande);
                                                sigue riendo 1,2 s tras tragar
                 aparece             serio      respira
                 busca y anda        enfado     bambolea (furia si es grande)
                 quieto              serio      respira (furia si es grande)
               Emocion fija una cara (para ensayar o para la funcion); auto, la
               del estado.
  PIXELADO     Pixelsprite > 0 agranda los pixeles (filas de pixeles del sprite):
               96 o 64, arcade de 8 bits; 0, el atlas tal cual (256 filas).
  RENDER       el render no dibujaba las geometrias del juego (marcas, brotes_mal,
               tocon, monstruo, agua_juego): ahora si, y trumpzilla.
  LEYENDA      MONSTRUO #3  busca  celda 40 -> 52  tam 0.62  acum 5/8  x2   cara enfado

OPERADORES (en /project1/FASE1)
-------------------------------
  trumpzilla, i_trumpzilla   Geometry COMP instanciado (una lamina: el sprite
               y su sombra) con mat_sprite (GLSL MAT: sprite_vertex y sprite_pixel).
  trumpzilla_atlas   Movie File In TOP con sprites/trumpzilla_emociones.png
               (sampler sAtlas de mat_sprite). Las caras se rehacen con
               sprites/hacer_atlas_trumpzilla.py.

PROBAR
------
  Modojuego. Sembrar hasta 3 en una celda a dos de la del monstruo;
  Simmonstruo: aparece serio, va enfadado a la celda (bambolea), se la come
  riendo. Emocion: pasar por las diez caras. Con una fila de 3 a su paso
  (fase 34): cae con susto y llora en la zanja; con 4, panico con el agua y se
  hunde. Spritemonstruo apagado: la esfera de la fase 33.

COMO USARLO
-----------
  Copia la carpeta sprites del repositorio en la carpeta de los scripts y:
    exec(open('C:/Users/DareDave/Downloads/est/fase38_trumpzilla.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase38 v1  (el devorador: Trumpzilla, el monstruo en sprite con diez emociones)'
banner(VERSION)

base = require_base(38)
motor = install_core(base, CARPETA, 38)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase38)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase38')
add_par(base, page, 'toggle', 'Spritemonstruo', 'Monstruo en sprite (Trumpzilla)', True)
add_par(base, page, 'menu', 'Emocion', 'Emocion', 'auto', menu=['auto'] + list(m.EMOCIONES_MON),
        menu_labels=['Auto (por su estado)'] + [e.capitalize() for e in m.EMOCIONES_MON])
add_par(base, page, 'float', 'Altosprite', 'Alto del sprite (celdas, por tam)', 1.6, 0.2, 4.0, clamp=True)
add_par(base, page, 'int', 'Pixelsprite', 'Pixelado (filas de pixeles; 0 tal cual)', 0, 0, 256, clamp=True)
add_par(base, page, 'float', 'Inclinasprite', 'Inclinacion maxima hacia la normal (grados)', 30.0, 0.0, 180.0,
        clamp=True)
ok('pagina Fase38: Spritemonstruo, Emocion (auto), Altosprite 1,6, Pixelsprite 0, Inclinasprite 30')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

materiales_piel(base)                   # mat_respaldo, para Materialrespaldo
trumpzilla_al_dia(base, CARPETA)
set_render(base)

leeme(base, 38, """FASE 38 - TRUMPZILLA, EL MONSTRUO EN SPRITE
  Con Spritemonstruo, el monstruo es un sprite (atlas de diez caras,
  sprites/trumpzilla_emociones.png) de pie en su celda, que mira a la camara,
  con sombra, y se voltea hacia donde camina. La cara sale de su estado:
  serio al aparecer, enfado al buscar (furia grande), rie al devorar
  (carcajada grande), susto al caer, llora en la zanja, panico con el agua o
  acorralado, mueca aturdido, calma gris petrificado; ahogado se hunde.
  Emocion fija una cara; Altosprite su alto (celdas por tam); Pixelsprite
  agranda los pixeles (0 tal cual); Inclinasprite, cuanto se inclina hacia
  la vertical del planeta (30 grados; 180, del todo). La logica no cambia.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS38 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Simbalance', 'Colapsoon',
          'Spritemonstruo', 'Emocion', 'Altosprite')


def prueba(t):
    import copy
    m = t.m
    guarda, filas = guardar_sala(base, PARS38)
    try:
        _prueba(t, m, copy)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ):
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = m.GEO
    W['traza'][i] = 1
    W['h'][i] = m.height_for(m.cfg(), occ)


def _cara(m, fila):
    """(emocion, animacion) de una fila del sprite."""
    k = int(round(fila[12]))
    return m.EMOCIONES_MON[k % 16], m.ANIMS_MON[k // 16]


def _prueba(t, m, copy):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Umbralaparicion = 1.0          # que no aparezca solo mientras se prepara el mundo
    base.par.Spritemonstruo = True
    base.par.Emocion = 'auto'
    base.par.Altosprite = 1.6
    S = SalaJuego(base, m, absTime.seconds + 4100.0)
    E = m.EMOCIONES_MON

    # 1. el atlas, los operadores y el render
    cols, filas = m.ATLAS_MON
    med = _png_medidas(CARPETA + '/' + SPRITE_ATLAS)
    t.check('el atlas sprites/trumpzilla_emociones.png: %d x %d celdas de 192 x 256 para las %d caras'
            % (cols, filas, len(E)), med == (cols * 192, filas * 256) and len(E) <= cols * filas
            and base.op('trumpzilla_atlas') is not None, '%s' % (med,))
    mat = base.op('mat_sprite')
    nombres = str(base.op('render').par.geometry.val).split()
    t.check('trumpzilla, i_trumpzilla y mat_sprite (sampler sAtlas, uniformes uSprite con sprite_t y uSpriteInc '
            'con Inclinasprite); el render dibuja trumpzilla y las geometrias del juego',
            all(base.op(n) is not None for n in ('trumpzilla', 'i_trumpzilla', 'sprite_vertex', 'sprite_pixel'))
            and mat is not None and str(mat.par.sampler0name.eval()) == 'sAtlas'
            and str(mat.par.vec0name.eval()) == 'uSprite' and str(mat.par.vec1name.eval()) == 'uSpriteInc'
            and 'Inclinasprite' in (mat.par.vec1valuex.expr or '')
            and all(n in nombres for n in ('trumpzilla', 'monstruo', 'tocon', 'brotes_mal', 'marcas', 'agua_juego'))
            and 'sprite_t' in dict(m.canales_frame([])), ' '.join(nombres[-12:]))

    # 2. la logica no cambia: la misma partida que tras la fase 37
    W, c = S.nuevo(4)
    a = 40 if m.N > 50 else m.N // 2
    dist, _ = m.dijkstra_mon(W, c, a)
    lejos = min(x for x in dist if abs(dist[x] - 2.0) < 1e-9)
    junto = m.NEIGH[a][0]

    def partida(cfg_):
        S2 = SalaJuego(base, m, absTime.seconds + 4600.0)
        W2, _ = S2.nuevo(4)
        for x, o in ((lejos, 4), (junto, 3)):
            _poner(m, W2, x, o)
        m.aparecer(W2, cfg_, S2.now, a)
        for _ in range(10):
            S2.pasos(W2, cfg_, 2)
            m.build_instances(W2, cfg_, S2.now)
        J = W2['juego']
        return copy.deepcopy((W2['occ'], W2['sp'], J['mon'], J['recuento']))
    c = m.cfg()
    r38 = partida(c)
    r37 = partida(dict(c, nivel=37))
    t.check('con el sprite, el juego da el mismo resultado que tras la fase 37 (la logica no cambia)',
            r38 == r37 and r38[2]['comidos'] > 0, 'comidos %d' % r38[2]['comidos'])

    # 3. aparece: serio; el sprite y su sombra, en lugar del cuerpo provisional
    W, c = S.nuevo(4)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    inst = m.build_instances(W, c, S.now)
    fz = inst.get('trumpzilla', [])
    cw, cl = m._cell_sizes(m.base_radius(W, c, a), a)
    alto = mo['tam'] * c['alto_sprite'] * min(cw, cl)
    t.check('aparece serio (respira): dos filas en trumpzilla, la sombra (256) y el sprite, alto Altosprite x tam '
            'celdas y ancho 3/4; monstruo vacio',
            len(fz) == 2 and int(fz[0][12]) == m.SPRITE_SOMBRA and _cara(m, fz[1]) == ('serio', 'respira')
            and abs(fz[1][7] - alto) < 1e-6 * max(1.0, alto) and abs(fz[1][6] - 0.75 * fz[1][7]) < 1e-6
            and inst.get('monstruo') == [], '%d filas, %s' % (len(fz), _cara(m, fz[1]) if len(fz) > 1 else '-'))

    # 4. busca: enfado y camina; mira hacia la celda siguiente
    S.pasos(W, c, 1)
    p, n = m.pos_monstruo(W, c, mo)
    d = m.rumbo_mon(W, c, mo, p, n)
    nx = mo['camino'][0] if mo['camino'] else None
    hacia = m._hacia(n, p, m._mul(m.normal_i(nx), m._len(p))) if nx is not None else (0.0, 0.0, 0.0)
    fz = m.build_instances(W, c, S.now)['trumpzilla']
    t.check('busca y anda: enfado (camina); el eje z del sprite, hacia la celda siguiente del camino',
            mo['estado'] == 'busca' and nx is not None and _cara(m, fz[-1]) == ('enfado', 'camina')
            and m._dot(d, hacia) > 0.99, '%s, %s' % (mo['estado'], _cara(m, fz[-1])))
    mo['acum'] = int(c['ocupacion_max'])
    m.actualizar_tam(c, mo)
    t.check('grande: furia', m.emocion_mon(W, c, mo, S.now) == ('furia', 'camina'))
    mo['acum'] = 0
    m.actualizar_tam(c, mo)

    # 5. devora: rie (carcajada si es grande) y sigue riendo T_RISA s
    W, c = S.nuevo(4)
    _poner(m, W, junto, 6)
    mo = m.aparecer(W, c, S.now, junto)
    S.pasos(W, c, 1)
    dev = m.emocion_mon(W, c, mo, S.now)
    mo['acum'] = int(c['ocupacion_max'])
    m.actualizar_tam(c, mo)
    dev_g = m.emocion_mon(W, c, mo, S.now)
    mo['acum'] = 0
    m.actualizar_tam(c, mo)
    mo['estado'] = 'busca'
    mo['camino'] = []
    tras = m.emocion_mon(W, c, mo, S.now + 0.5)
    luego = m.emocion_mon(W, c, mo, S.now + m.T_RISA + 0.6)
    t.check('devora: rie (mastica), carcajada si es grande; tras tragar sigue riendo T_RISA s y vuelve a serio',
            dev == ('rie', 'devora') and dev_g == ('carcajada', 'devora') and tras == ('rie', 'devora')
            and luego == ('serio', 'respira'), '%s %s %s %s' % (dev, dev_g, tras, luego))

    # 6. cae, la zanja y el agua
    W, c = S.nuevo(4)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    J = W['juego']
    m.caer(W, c, mo, S.now)
    cae = m.emocion_mon(W, c, mo, S.now)
    mo['estado'] = 'busca'
    J['zanjas'][a] = 2
    sigue = m.emocion_mon(W, c, mo, S.now + 0.5)
    zanja = m.emocion_mon(W, c, mo, S.now + m.T_SUSTO + 0.1)
    J['agua'][a] = 3
    agua = m.emocion_mon(W, c, mo, S.now + m.T_SUSTO + 0.2)
    t.check('cae: susto (tiembla) T_SUSTO s; en la zanja, llora; con agua en su zanja, panico',
            cae == ('susto', 'tiembla') and sigue == cae and zanja == ('llora', 'respira')
            and agua == ('panico', 'tiembla'), '%s %s %s' % (cae, zanja, agua))
    del J['zanjas'][a], J['agua'][a]

    # 7. las armas de la fase 37
    now = S.now + 10.0
    caras = []
    for campo, val in (('piedra', now + 5.0), ('aturdido', now + 5.0), ('pisoton', True), ('acorralado', True)):
        mo[campo] = val
        caras.append(m.emocion_mon(W, c, mo, now))
        mo[campo] = None if campo in ('piedra', 'aturdido') else False
    t.check('petrificado: calma gris (piedra); aturdido: mueca; pisoton: llora (tiembla); acorralado: panico',
            caras == [('calma', 'piedra'), ('mueca', 'aturdido'), ('llora', 'tiembla'), ('panico', 'tiembla')],
            '%s' % caras)

    # 8. se ahoga: se hunde T_HUNDE s, sin sombra, y desaparece
    t0 = S.now + 20.0
    m.morir(W, c, mo, t0)
    J['ev'].clear()
    W['juego'].setdefault('luz', {})['t_muerte'] = None
    hunde = m.filas_trumpzilla(W, c, mo, t0 + 0.5 * m.T_HUNDE)
    p0, n0 = m.pos_monstruo(W, c, mo)
    baja = m._dot(m._add(hunde[0][:3], p0, -1.0), n0) if hunde else 0.0
    fuera = m.filas_trumpzilla(W, c, mo, t0 + m.T_HUNDE + 0.1)
    t.check('ahogado: panico, se hunde (una fila, sin sombra, por debajo del suelo) y a los T_HUNDE s desaparece',
            len(hunde) == 1 and _cara(m, hunde[0]) == ('panico', 'hunde') and baja < 0.0 and fuera == [],
            '%d filas, baja %.4f' % (len(hunde), baja))

    # 9. Emocion fija, la leyenda y Spritemonstruo apagado
    W, c = S.nuevo(4)
    _poner(m, W, lejos, 3)
    mo = m.aparecer(W, c, S.now, a)
    leg = m._legend_monstruo(W, c)
    base.par.Emocion = 'furia'
    c = m.cfg()
    fija = _cara(m, m.build_instances(W, c, S.now)['trumpzilla'][-1])
    base.par.Emocion = 'auto'
    base.par.Spritemonstruo = False
    c = m.cfg()
    sin = m.build_instances(W, c, S.now)
    base.par.Spritemonstruo = True
    base.par.Modojuego = False
    apagado = m.build_instances(W, m.cfg(), S.now).get('trumpzilla')
    t.check('Emocion fija la cara (furia, con la animacion del estado); la leyenda dice la cara; Spritemonstruo '
            'apagado: el cuerpo provisional (3 filas) y sin sprite; Modojuego apagado: nada',
            fija == ('furia', 'respira') and leg.rstrip().endswith('cara serio') and len(sin['monstruo']) == 3
            and sin['trumpzilla'] == [] and apagado == [], '%s, %s' % (fija, leg.strip()))


run_test(base, prueba)
print('  Ahora: Modojuego; Sembrar hasta 3 en una celda; Simmonstruo: aparece serio, va enfadado y se la')
print('  come riendo. Emocion: las diez caras. Pixelsprite 96: arcade de 8 bits.')
print('=' * 66)
