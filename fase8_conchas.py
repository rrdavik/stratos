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
  2. El planeta engorda el GROSOR de la concha. Con Grosortiempo es
     proporcional a lo que duro su mundo:
         grosor = Shellthick x compases / Ciclomin
     entre 0,25x y Ciclomax / Ciclomin, y nunca mas de Grosormax (2,0):
     con los valores por defecto, de 0,5 (8 compases) a 2,0 (32 o mas).
     El grosor de cada estrato registra cuanto tardo su mundo en
     agotarse. Sin Grosortiempo, siempre Shellthick.
  3. El 25 % de la ocupacion de cada celda pasa a la capa nueva (la
     fraccion que no llega a 1 se acumula para el ciclo siguiente). Lo
     heredado vuelve a brotar desde la nueva superficie.

El radio NOMINAL del cuerpo ES el tiempo transcurrido: radio del nucleo +
suma de los grosores de todas las conchas (la colmatacion no cuenta). El
suelo de cada celda es el nucleo + su columna; la laguna, lo que falta.

EL HORNEADO (decision tomada)
-----------------------------
El marco habla de hornear cada concha a una textura sobre una esfera.
Aqui la concha es una capa de losetas instanciadas: igual de barata
(una sola geometria), sin shaders, y en la fase 9 permite abrir cortes
quitando losetas y ver las paredes de cada capa con su color.

De cada columna se dibujan sus Maxconchas (24) losetas superiores; bajo
ellas, un ZOCALO (una sola instancia por celda) baja hasta el nucleo. La
esfera del nucleo ya no crece: taparia las hondonadas.

LA CAMARA
---------
La camara se aleja con el radio para no quedar dentro del planeta. La
camara definitiva (distancia constante a la superficie) llega en la 10.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase8_conchas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase8 v5  (el mundo enterrado se deposita sobre el relieve: columnas, Colmatacion, zocalo)'
banner(VERSION)

base = require_base(8)
motor = install_core(base, CARPETA, 8)

page = get_page(base, 'Fase8')
add_par(base, page, 'float', 'Herencia', 'Herencia entre conchas', 0.25, 0.0, 1.0)
add_par(base, page, 'int', 'Maxconchas', 'Conchas visibles', 24, 1, 96, clamp=True)
add_par(base, page, 'toggle', 'Grosortiempo', 'Grosor proporcional al ciclo', True)
add_par(base, page, 'float', 'Grosormax', 'Grosor maximo de concha (0: sin limite)', 2.0, 0.0, 8.0)
add_par(base, page, 'float', 'Colmatacion', 'Relleno de las hondonadas al enterrar', 0.0, 0.0, 1.0,
        clamp=True)
try:
    base.par.Maxconchas.label = 'Losetas visibles por columna'
except Exception:
    pass
ok('pagina Fase8: Herencia (25 %), Maxconchas (24 por columna), Grosortiempo, Grosormax (2), '
   'Colmatacion (0)')

make_phong(base, 'mat_estratos', 780, 620, spec=0.12, shin=8, diff=1.0)
make_instanced(base, 'estratos', 520, 620, 'mat_estratos')
set_render(base)

esfera = base.op('nucleo').op('esfera')
R_EXPR = "parent(2).op('motor').module.nucleo_radius(absTime.frame)"
done = all(setexpr(esfera, ax, R_EXPR) for ax in ('radx', 'rady', 'radz'))
if done:
    ok('nucleo: esfera fija en el radio base; lo que no se dibuja de cada columna, en su zocalo')
else:
    fail('no pude enlazar el radio del nucleo')

cam = base.op('camara')
if setexpr(cam, 'tz', "parent().op('motor').module.surface_radius(absTime.frame) + 9.0"):
    ok('camara: se aleja con el radio del planeta')

leeme(base, 8, """FASE 8 - CONCHAS
  En cada fin de ciclo cada celda deposita una loseta sobre su columna,
  con el color de su generacion: las hondonadas se tapizan (Colmatacion
  las rellena). Grosor: Shellthick x compases / Ciclomin (Grosortiempo),
  entre 0,25x y Ciclomax/Ciclomin, como mucho Grosormax (2).
  Radio nominal = nucleo + suma de grosores; suelo = nucleo + columna.
  Herencia (25 %) pasa a la capa nueva. Maxconchas losetas por columna;
  debajo, un zocalo hasta el nucleo, que ya no crece.
  Prueba sin esperar: Forzarciclo (pagina Fase6).""")

print_report()


def prueba(t):
    m = t.m
    c = m.cfg()
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
    zoc = [r for r in tz if abs(r[9] - m.COL_ZOCALO[0]) < 1e-6 and abs(r[10] - m.COL_ZOCALO[1]) < 1e-6]
    t.check('Maxconchas por columna: 4 losetas y un zocalo por celda',
            len(tz) == m.N * 5 and len(zoc) == m.N and len(tz) <= m.N * (c8['max_shells'] + 1),
            '%d instancias, %d zocalos' % (len(tz), len(zoc)))
    t.check('el nucleo no crece', abs(m.nucleo_radius() - c['core_radius']) < 1e-6)
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
print('  Si engorda demasiado rapido: sube Ciclomin o baja Shellthick.')
print('=' * 66)
