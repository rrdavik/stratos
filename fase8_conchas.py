"""
=============================================================================
ESTRATOS - FASE 8: CONCHAS (ENTERRAR EL MUNDO)
=============================================================================
Requiere la fase 7.

QUE HACE
--------
Al terminar cada ciclo de ecosistema (fase 6: lo cierra el mundo):

  1. La capa activa se ENTIERRA: cada celda DEPOSITA una loseta con el
     color de su generacion sobre lo que le queda debajo (su COLUMNA), no
     a una cota comun. Una hondonada que dejo un corte se tapiza y sigue
     siendo hondonada; Colmatacion (0-1) dice cuanto la rellena:
         grosor de la loseta = grosor de la concha + Colmatacion x laguna
         laguna = radio nominal - suelo de la celda
     Las celdas que estaban ocupadas quedan mas claras: los continentes
     se leen en el color. Las formaciones de esa capa se descartan.
     PALETA (motor v26): cada concha de un color. Tono por el angulo
     aureo desde Paletatono, saltando el cian de la cicatriz y el ambar
     del SEQ2 (desde el motor v46, tambien los verdes de los pisos y el
     azul de los rios: 120-275); claro y oscuro alternos; croma de
     mineral (Paletacroma).
     Calculado de la generacion: cambiar la paleta recolorea lo enterrado.
     Paleta = mineral vuelve a la anterior (ambar y grises).
  2. El planeta engorda el GROSOR de la concha. Con Grosortiempo es
     proporcional a lo que duro su mundo:
         grosor = Shellthick x compases / Ciclomin
     entre 0,25x y Ciclomax / Ciclomin, y nunca mas de Grosormax (1,5):
     con los valores por defecto, de 0,5 (16 compases) a 1,5 (48 o mas).
     El grosor de cada estrato registra cuanto tardo su mundo en
     agotarse. Sin Grosortiempo, siempre Shellthick.
     COMPACTACION (v10, motor v37): la concha nueva aplasta las de
     debajo. Todas pierden la misma fraccion, 1 - e^(-grosor / Cortezamax),
     asi que la corteza tiende a Cortezamax (4) y el planeta deja de
     engordar: las conchas recientes se leen gruesas y las viejas se
     aprietan en vetas finas. El radio sube siempre al menos un 10 % de
     la concha nueva y nunca baja. Cortezamax 0: sin compactar.
  3. El 25 % de la ocupacion de cada celda pasa a la capa nueva (la
     fraccion que no llega a 1 se acumula para el ciclo siguiente). Lo
     heredado vuelve a brotar desde la nueva superficie.

El radio NOMINAL del cuerpo es el tiempo transcurrido, comprimido por la
compactacion: radio del nucleo + suma de los grosores de todas las conchas
(la colmatacion no cuenta). El suelo de cada celda es el nucleo + su
columna; la laguna, lo que falta.

EL HORNEADO (decision tomada)
-----------------------------
El marco habla de hornear cada concha a una textura sobre una esfera.
Aqui la concha es una capa de losetas instanciadas: igual de barata
(una sola geometria), sin shaders, y en la fase 9 permite abrir cortes
quitando losetas y ver las paredes de cada capa con su color.

LUZ EN LAS CONCHAS (Luzconchas, pagina Fase3): una nota tine tenuemente las
losetas superiores de su celda (Luzconchasalcance, 4), del color de su
secuenciador: pulso con la nota (Luzconchaspulso) y reposo que respira
mientras es su ultima celda (Luzconchasreposo). Es luz aditiva: no tapa el
color de la generacion, se ve en la sombra y la cicatriz manda.

De cada columna se dibujan sus Maxconchas (24) losetas superiores; bajo
ellas, un ZOCALO (una sola instancia por celda) baja hasta el nucleo. La
esfera del nucleo ya no crece: taparia las hondonadas.

LA CAMARA
---------
La camara de globo (estratos_comun.py, motor v24) encuadra el planeta
entero y retrocede lo justo a cada enterramiento. La fase 10 anade la de
superficie como modo.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase8_conchas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase8 v11  (autoprueba: la paleta tambien reserva los verdes de los pisos y el azul de los rios)'
banner(VERSION)

base = require_base(8)
motor = install_core(base, CARPETA, 8)

page = get_page(base, 'Fase8')
add_par(base, page, 'float', 'Herencia', 'Herencia entre conchas', 0.25, 0.0, 1.0)
add_par(base, page, 'int', 'Maxconchas', 'Conchas visibles', 24, 1, 96, clamp=True)
add_par(base, page, 'toggle', 'Grosortiempo', 'Grosor proporcional al ciclo', True)
add_par(base, page, 'float', 'Grosormax', 'Grosor maximo de concha (0: sin limite)', 1.5, 0.0, 8.0)
add_corteza(base)
add_par(base, page, 'float', 'Colmatacion', 'Relleno de las hondonadas al enterrar', 0.0, 0.0, 1.0,
        clamp=True)
add_par(base, page, 'menu', 'Paleta', 'Paleta de las conchas', 'generaciones',
        menu=['generaciones', 'mineral'], menu_labels=['Un color por concha', 'Mineral (anterior)'])
add_par(base, page, 'float', 'Paletatono', 'Tono de la primera concha (grados)', 20.0, 0.0, 360.0)
add_par(base, page, 'float', 'Paletacroma', 'Saturacion de las conchas', 0.09, 0.0, 0.15, clamp=True)
try:
    base.par.Maxconchas.label = 'Losetas visibles por columna'
except Exception:
    pass
ok('pagina Fase8: Herencia (25 %), Maxconchas (24 por columna), Grosortiempo, Grosormax (1,5), '
   'Cortezamax (4), '
   'Colmatacion (0), Paleta (generaciones), Paletatono (20), Paletacroma (0,09)')

make_phong(base, 'mat_estratos', 780, 620, spec=0.12, shin=8, diff=1.0)
make_instanced(base, 'estratos', 520, 620, 'mat_estratos')
conchas_al_dia(base, motor.module)     # desde la fase 15, las conchas con el shader de la piel
set_render(base)

esfera = base.op('nucleo').op('esfera')
R_EXPR = "parent(2).op('motor').module.nucleo_radius(absTime.frame)"
done = all(setexpr(esfera, ax, R_EXPR) for ax in ('radx', 'rady', 'radz'))
if done:
    ok('nucleo: esfera fija en el radio base; lo que no se dibuja de cada columna, en su zocalo')
else:
    fail('no pude enlazar el radio del nucleo')


leeme(base, 8, """FASE 8 - CONCHAS
  En cada fin de ciclo cada celda deposita una loseta sobre su columna,
  con el color de su generacion (Paleta: uno distinto por concha): las hondonadas se tapizan (Colmatacion
  las rellena). Grosor: Shellthick x compases / Ciclomin (Grosortiempo),
  entre 0,25x y Ciclomax/Ciclomin, como mucho Grosormax (1,5).
  Cortezamax (4): la concha nueva compacta las viejas; la corteza tiende
  a ese grosor y el planeta deja de engordar (0: sin compactar).
  Radio nominal = nucleo + suma de grosores; suelo = nucleo + columna.
  Herencia (25 %) pasa a la capa nueva. Maxconchas losetas por columna;
  debajo, un zocalo hasta el nucleo, que ya no crece.
  Prueba sin esperar: Forzarciclo (pagina Fase6).""")

print_report()


def prueba(t):
    import math
    m = t.m
    c = dict(m.cfg())
    c['corteza_max'] = 0.0              # sin compactar: el radio es el tiempo
    W = m.new_world()
    for g in range(4):
        for k in range(16):
            m.note_on(W, c, 1, 64, 100, g * 10 + k)
        m.end_cycle(W, c, g * 10 + 9)
    i = m.note_cell(64)
    t.check('4 ciclos -> 4 conchas', m.n_shells(W) == 4)
    t.check('el radio crece 4 grosores',
            abs(m.top_radius(W, c) - (c['core_radius'] + 4 * c['shell_thick'])) < 1e-6,
            '%.2f' % m.top_radius(W, c))
    t.check('herencia: la celda insistente sigue ocupada', W['occ'][i] >= 2, str(W['occ'][i]))
    t.check('losetas: una por celda y concha', len(m.build_tiles(W, c, 0.0)) == 4 * m.N)
    # grosor proporcional a la duracion del ciclo
    cmin, cmax = m.cycle_bounds(c)
    th = c['shell_thick']
    cg = dict(c)
    cg['grosor_tiempo'] = 1
    W2 = m.new_world()
    for bars in (1, cmin, 2 * cmin, 10 * cmax):
        m.end_cycle(W2, cg, 0.0, bars)
    gs = [m.shell_th(sh, cg) for sh in W2['shells']]
    gmax = cg['grosor_max'] if cg['grosor_max'] > 0 else 1e9
    want = [min(gmax, x) for x in (th * max(0.25, 1.0 / cmin), th,
                                   th * min(2.0, cmax / float(cmin)), th * cmax / float(cmin))]
    t.check('grosor = Shellthick x compases / Ciclomin, con sus limites',
            all(abs(a - b) < 1e-6 for a, b in zip(gs, want)),
            ' '.join('%.3f' % g for g in gs))
    t.check('radio = nucleo + suma de grosores',
            abs(m.top_radius(W2, cg) - (c['core_radius'] + sum(gs))) < 1e-6,
            '%.3f' % m.top_radius(W2, cg))
    tiles = m.build_tiles(W2, cg, 0.0)
    alturas = [tiles[k][7] / 0.98 for k in range(len(gs))]   # columna de la celda 0
    t.check('cada concha dibuja su grosor', all(abs(a - b) < 1e-6 for a, b in zip(alturas, gs)))
    t.check('ningun grosor pasa de Grosormax', max(gs) <= gmax + 1e-9, '%.3f' % max(gs))
    cg['grosor_tiempo'] = 0
    m.end_cycle(W2, cg, 0.0, 10 * cmax)
    t.check('sin Grosortiempo: Shellthick', abs(m.shell_th(W2['shells'][-1], cg) - th) < 1e-6)
    # columnas: el mundo se deposita sobre el relieve
    c8 = dict(c)
    c8['nivel'] = max(9, c8['nivel'])
    c8['grosor_tiempo'] = 0
    for colm, nombre in ((0.0, '0'), (0.5, '0,5'), (1.0, '1')):
        c8['colmatacion'] = colm
        Wc = m.new_world()
        for g in range(5):
            m.end_cycle(Wc, c8, float(g))
        m.cut(Wc, c8, i, 3, 0, 10.0)
        lg0 = m.laguna(Wc, c8, i)
        s0 = m.suelo(Wc, c8, i)
        otra = (i + m.N // 2) % m.N
        so0 = m.suelo(Wc, c8, otra)
        m.end_cycle(Wc, c8, 11.0)
        lg1 = m.laguna(Wc, c8, i)
        nom_ok = abs(m.radio_nominal(Wc, c8) - (c8['core_radius'] + 6 * th)) < 1e-6
        if colm == 0.0:
            t.check('Colmatacion 0: la loseta nueva empieza en el suelo del corte y la laguna se conserva',
                    abs(m.column_radii(Wc, c8, i)[-1][1] - s0) < 1e-6 and abs(lg1 - lg0) < 1e-6
                    and abs(m.suelo(Wc, c8, otra) - (so0 + th)) < 1e-6 and nom_ok,
                    'laguna %.2f -> %.2f' % (lg0, lg1))
        elif colm == 1.0:
            t.check('Colmatacion 1: todas las celdas quedan en el radio nominal',
                    all(abs(m.suelo(Wc, c8, x) - m.radio_nominal(Wc, c8)) < 1e-6 for x in range(m.N))
                    and nom_ok)
        else:
            t.check('Colmatacion %s: la laguna se reduce a la mitad' % nombre,
                    abs(lg1 - 0.5 * lg0) < 1e-6 and nom_ok, 'laguna %.2f -> %.2f' % (lg0, lg1))
    # zocalo y Maxconchas por columna
    c8['colmatacion'] = 0.0
    c8['max_shells'] = 4
    Wz = m.new_world()
    for g in range(7):
        m.end_cycle(Wz, c8, float(g))
    tz = m.build_tiles(Wz, c8, 0.0)
    zc = m.zocalo_color(c8)
    zoc = [r for r in tz if abs(r[9] - zc[0]) < 1e-6 and abs(r[10] - zc[1]) < 1e-6]
    t.check('Maxconchas por columna: 4 losetas y un zocalo por celda',
            len(tz) == m.N * 5 and len(zoc) == m.N and len(tz) <= m.N * (c8['max_shells'] + 1),
            '%d instancias, %d zocalos' % (len(tz), len(zoc)))
    t.check('el nucleo no crece', abs(m.nucleo_radius() - c['core_radius']) < 1e-6)
    # compactacion (v10, motor v37): la corteza tiende a Cortezamax
    cz = dict(c)
    cz.update(nivel=max(9, c['nivel']), grosor_tiempo=0, colmatacion=0.0, corteza_max=4.0)
    Wk = m.new_world()
    radios = [cz['core_radius']]
    for g in range(40):
        m.end_cycle(Wk, cz, float(g))
        radios.append(m.top_radius(Wk, cz))
    gk = [m.shell_th(sh, cz) for sh in Wk['shells']]
    sube = all(b - a >= m.COMPACTA_CRECE * th - 1e-9 for a, b in zip(radios, radios[1:]))
    t.check('Cortezamax 4: el radio nunca baja y sube al menos un 10 % de cada concha', sube)
    t.check('Cortezamax 4: 40 conchas de %.2f dejan una corteza de menos de 6 (sin compactar, %.0f)'
            % (th, 40 * th), radios[-1] - cz['core_radius'] < 6.0, '%.2f' % (radios[-1] - cz['core_radius']))
    t.check('la concha nueva conserva su grosor; las viejas, mas finas cuanto mas hondas',
            abs(gk[-1] - th) < 1e-9 and all(a <= b + 1e-12 for a, b in zip(gk, gk[1:])) and gk[0] < 0.2 * th,
            '%.3f ... %.3f' % (gk[0], gk[-1]))
    t.check('compactada, cada columna sigue en el radio nominal',
            all(abs(m.suelo(Wk, cz, x) - m.top_radius(Wk, cz)) < 1e-6 for x in range(m.N)))
    Wq = m.new_world()
    for g in range(5):
        m.end_cycle(Wq, cz, float(g))
    m.cut(Wq, cz, i, 3, 0, 10.0)
    lq0 = m.laguna(Wq, cz, i)
    m.end_cycle(Wq, cz, 11.0)
    t.check('la laguna de un corte se compacta como sus conchas',
            0 < Wq['compacta'] < 1 and abs(m.laguna(Wq, cz, i) - lq0 * Wq['compacta']) < 1e-6,
            '%.3f -> %.3f (x%.3f)' % (lq0, m.laguna(Wq, cz, i), Wq['compacta']))
    # paleta de generaciones
    cp = dict(c)
    cp.update(paleta=0, paleta_tono=20.0, paleta_croma=0.09,
              nivel=min(c['nivel'], 14))          # desde la fase 15 la concha lleva la materia de su tema

    def oklch(n, ocup):
        L = m.L_VACIA[n % 2] + (m.L_OCUPADA if ocup else 0.0)
        return L, m.palette_hue(n, cp['paleta_tono'])
    contraste = all(min(abs(oklch(n, 0)[1] - oklch(n + 1, 0)[1]),
                        360 - abs(oklch(n, 0)[1] - oklch(n + 1, 0)[1])) >= 60
                    and abs(oklch(n, 0)[0] - oklch(n + 1, 0)[0]) >= 0.1 - 1e-9 for n in range(200))
    t.check('paleta: dos conchas seguidas difieren 60 grados de tono y 0,1 de luminosidad', contraste)
    t.check('paleta: ningun tono en las bandas reservadas (ambar 55-100; verdes, cian y azul de los rios 120-275)',
            not any(m._en_banda(m.palette_hue(n, cp['paleta_tono'])) for n in range(200)))
    gama = all(m.oklch_to_srgb(oklch(n, o)[0], cp['paleta_croma'], oklch(n, o)[1])[1]
               for n in range(200) for o in (0, 1))
    t.check('paleta: todos los colores dentro de sRGB sin recortar', gama)
    ref = ['#904D4E', '#A47AAF', '#6D651F', '#B8758D', '#685891', '#BC7867', '#824F79', '#889352']
    hx = lambda col: '#%02X%02X%02X' % tuple(int(round(v * 255)) for v in col)
    t.check('paleta: los colores de referencia', [hx(m.generation_color(cp, n, False)) for n in range(8)] == ref)
    t.check('paleta: la loseta ocupada, mas clara que la vacia',
            all(sum(m.generation_color(cp, n, True)) > sum(m.generation_color(cp, n, False)) + 0.1
                for n in range(200)))
    Wp = m.new_world()
    for g in range(3):
        m.note_on(Wp, cp, 1, 64, 100, float(g))
        m.end_cycle(Wp, cp, g + 0.5)
    cm = dict(cp)
    cm['paleta'] = 1
    viejo = [m._tint(m.MINERAL[sh['gen'] % 8], 0.75 + 0.35 * min(1.0, sh['occ'][x] / 4.0))
             for x in range(m.N) for sh in Wp['shells']]
    nuevo = [r[9:12] for r in m.build_tiles(Wp, cm, 0.0)]
    t.check('Paleta mineral: los colores de antes, tal cual',
            all(abs(a[k] - b[k]) < 1e-9 for a, b in zip(viejo, nuevo) for k in range(3)))
    for sh in Wp['shells']:
        sh['col'] = [0.5, 0.4, 0.3]                     # color guardado de un mundo anterior: no manda
    t1 = m.build_tiles(Wp, cp, 0.0)
    ct = dict(cp)
    ct['paleta_tono'] = 200.0
    t2 = m.build_tiles(Wp, ct, 0.0)
    t.check('mundo guardado: lo enterrado sale con la paleta; cambiar Paletatono lo recolorea',
            tuple(t1[0][9:12]) == m.generation_color(cp, Wp['shells'][0]['gen'],
                                                     Wp['shells'][0]['occ'][0] > 0)
            and all(a[9:12] != b[9:12] for a, b in zip(t1, t2)))
    cc = dict(cp)
    cc['nivel'] = max(9, cc['nivel'])
    m.cut(Wp, cc, i, 1, 0, 50.0)
    fondo = m.column_radii(Wp, cc, i)[-1]
    medio = 50.0 + cc['scar_time'] / 2
    fila = [r for r in m.build_tiles(Wp, cc, medio)
            if abs(math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2) - fondo[1]) < 1e-6
            and (r[0] * m.normal_i(i)[0] + r[1] * m.normal_i(i)[1] + r[2] * m.normal_i(i)[2]) > 0.999 * fondo[1]]
    esperado = m._mix(m.COL_SCAR, m.tile_color(cc, Wp['shells'][fondo[0]], Wp['shells'][fondo[0]]['occ'][i]), 0.5)
    t.check('la cicatriz se funde con el color de la concha de la loseta',
            fila and all(abs(fila[0][9 + k] - esperado[k]) < 1e-6 for k in range(3)))
    # la luz del secuenciador en las conchas de la celda
    import math
    cl = dict(c)
    cl.update(nivel=max(9, cl['nivel']), luz_conchas=1, luz_seq=1, grosor_tiempo=0,
              luz_conchas_alcance=4, max_shells=24)
    Wl = m.new_world()
    for g in range(10):
        m.end_cycle(Wl, cl, float(g))
    a, b = m.note_cell(64), m.note_cell(40)
    tiles0 = m.build_tiles(Wl, cl, 25.0)
    m.note_on(Wl, cl, 1, 64, 100, 20.0)
    m.note_on(Wl, cl, 2, 40, 100, 20.0)

    def de_celda(rows, x):
        n = m.normal_i(x)
        out = []
        for r in rows:
            d = math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)
            if d > 0 and (r[0] * n[0] + r[1] * n[1] + r[2] * n[2]) / d > 1 - 1e-6:
                out.append(r)
        return out
    L = m.shell_lights(Wl, cl, 20.05)
    la, lb = de_celda(L, a), de_celda(L, b)
    t.check('nota del SEQ1 y del SEQ2: se tinen las 4 losetas superiores de cada celda',
            len(la) == 4 and len(lb) == 4 and len(L) == 8, '%d + %d de %d' % (len(la), len(lb), len(L)))
    luma = lambda r: r[9] + r[10] + r[11]
    t.check('la luz baja hacia el fondo de la columna',
            all(luma(x) > luma(y) for x, y in zip(la, la[1:])))
    reposo = m.shell_lights(Wl, cl, 25.0)
    ra = de_celda(reposo, a)
    t.check('entre notas, reposo tenue y menor que el pulso',
            len(ra) == 4 and 0 < luma(ra[0]) < luma(la[0]), '%.3f < %.3f' % (luma(ra[0]) if ra else 0, luma(la[0])))
    r1 = de_celda(m.shell_lights(Wl, cl, 25.0 + m.RESPIRA_T / 4), a)
    r2 = de_celda(m.shell_lights(Wl, cl, 25.0 + 3 * m.RESPIRA_T / 4), a)
    t.check('el reposo respira (una loseta ocupada no)', abs(luma(r1[0]) - luma(r2[0])) > 1e-3)
    tiles = m.build_tiles(Wl, cl, 25.0)
    t.check('el color de la generacion no cambia: la luz es una capa aparte',
            tiles == tiles0)
    # en el fondo de un corte: la loseta del fondo, hacia abajo; las paredes vecinas no
    m.cut(Wl, cl, a, 3, 1, 30.0)
    Wl['scars'] = {}
    m.note_on(Wl, cl, 1, 64, 100, 40.0)
    L = m.shell_lights(Wl, cl, 40.05)
    la = de_celda(L, a)
    fondo = m.column_radii(Wl, cl, a)[-1]
    alto_fondo = math.sqrt(sum(x * x for x in la[0][:3])) if la else -1
    t.check('nota en el fondo de un corte: se tine la loseta del fondo; las vecinas no',
            la and abs(alto_fondo - fondo[1]) < 1e-6 and len(L) == len(la) + 4,
            '%d filas, %d de la celda' % (len(L), len(la)))
    # cicatriz: el cian manda
    Wl['scars'][fondo[0] * 1000 + a] = 40.0
    la2 = de_celda(m.shell_lights(Wl, cl, 40.1), a)
    t.check('una loseta con cicatriz reciente no se tine', len(la2) == len(la) - 1)
    # bateria: la loseta del pad sigue viendose en el centro de la celda tenida
    cl7 = dict(cl)
    cl7['perfiles'] = [(0, 0, 0)] * 8
    m.erosion(Wl, cl7, 3, 100, 40.2)
    ev = Wl['ev']['erosion']
    luz_c = de_celda(m.cell_lights(Wl, cl7, 40.25), ev['celda'])
    t.check('golpe de bateria sobre una celda tenida: se ve su luz en el centro',
            len(luz_c) >= 1)
    # interruptor
    cl['luz_conchas'] = 0
    t.check('Luzconchas apagado: ninguna capa de luz', not m.shell_lights(Wl, cl, 40.05))
    # por el camino real
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    n0 = m.n_shells(m.world())
    m.on_pulse('Forzarciclo')
    W = m.world()
    t.check('Forzarciclo entierra la capa', m.n_shells(W) == n0 + 1)
    t.check('Forzarciclo temprano: grosor minimo 0,25x',
            not m.cfg()['grosor_tiempo'] or abs(m.shell_th(W['shells'][-1], m.cfg()) - 0.25 * th) < 1e-6,
            '%.3f' % m.shell_th(W['shells'][-1], m.cfg()))
    m._CACHE['inst'] = m.build_instances(m.world(), m.cfg(), 0.0)
    est = base.op('i_estratos')
    est.cook(force=True)
    t.check('i_estratos dibuja la concha', est.numSamples == m.N, '%d de %d' % (est.numSamples, m.N))
    t.check('leyenda CONCHAS', 'CONCHAS' in m.legend())


run_test(base, prueba)
print('  Ahora: deja sonar varios ciclos (o pulsa Forzarciclo en la pagina')
print('  Fase6). El planeta engorda una capa por ciclo, mas gruesa cuanto')
print('  mas tardo su mundo en agotarse.')
print('  Las conchas viejas se compactan: el planeta tiende a nucleo + Cortezamax.')
print('  Si engorda demasiado: baja Cortezamax; si las eras son cortas, sube Ciclomin.')
print('=' * 66)
