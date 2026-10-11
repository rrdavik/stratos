"""
=============================================================================
ESTRATOS - FASE 8: CONCHAS (ENTERRAR EL MUNDO)
=============================================================================
Requiere la fase 7.

QUE HACE
--------
Al terminar cada ciclo de ecosistema (fase 6: lo cierra el mundo):

  1. La capa activa se ENTIERRA: se convierte en una concha de losetas
     (una por celda) con el color de su generacion. Las celdas que
     estaban ocupadas quedan mas claras: los continentes se leen en el
     color. Las formaciones de esa capa se descartan.
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

El radio del cuerpo ES el tiempo transcurrido: radio del nucleo + suma de
los grosores de todas las conchas.

EL HORNEADO (decision tomada)
-----------------------------
El marco habla de hornear cada concha a una textura sobre una esfera.
Aqui la concha es una capa de losetas instanciadas: igual de barata
(una sola geometria), sin shaders, y en la fase 9 permite abrir cortes
quitando losetas y ver las paredes de cada capa con su color.

Solo se dibujan las ultimas Maxconchas (24); las anteriores quedan dentro
de la esfera del nucleo, que crece para taparlas.

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

VERSION = 'fase8 v4  (conchas con grosor del ciclo, herencia, radio acumulado)'
banner(VERSION)

base = require_base(8)
motor = install_core(base, CARPETA, 8)

page = get_page(base, 'Fase8')
add_par(base, page, 'float', 'Herencia', 'Herencia entre conchas', 0.25, 0.0, 1.0)
add_par(base, page, 'int', 'Maxconchas', 'Conchas visibles', 24, 1, 96, clamp=True)
add_par(base, page, 'toggle', 'Grosortiempo', 'Grosor proporcional al ciclo', True)
add_par(base, page, 'float', 'Grosormax', 'Grosor maximo de concha (0: sin limite)', 2.0, 0.0, 8.0)
ok('pagina Fase8: Herencia (25 %), Maxconchas (24), Grosortiempo, Grosormax (2)')

make_phong(base, 'mat_estratos', 780, 620, spec=0.12, shin=8, diff=1.0)
make_instanced(base, 'estratos', 520, 620, 'mat_estratos')
set_render(base)

esfera = base.op('nucleo').op('esfera')
R_EXPR = "parent(2).op('motor').module.nucleo_radius(absTime.frame)"
done = all(setexpr(esfera, ax, R_EXPR) for ax in ('radx', 'rady', 'radz'))
if done:
    ok('nucleo: su radio cubre las conchas que ya no se dibujan')
else:
    fail('no pude enlazar el radio del nucleo')

cam = base.op('camara')
if setexpr(cam, 'tz', "parent().op('motor').module.surface_radius(absTime.frame) + 9.0"):
    ok('camara: se aleja con el radio del planeta')

leeme(base, 8, """FASE 8 - CONCHAS
  En cada fin de ciclo la capa se entierra como losetas con el color de
  su generacion. Grosor: Shellthick x compases / Ciclomin (Grosortiempo),
  entre 0,25x y Ciclomax/Ciclomin, como mucho Grosormax (2). Radio = nucleo + suma de grosores.
  Herencia (25 %) pasa a la capa nueva. Maxconchas visibles; las demas,
  dentro del nucleo.
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
    alturas = [tiles[k * m.N][7] / 0.98 for k in range(len(gs))]
    t.check('cada concha dibuja su grosor', all(abs(a - b) < 1e-6 for a, b in zip(alturas, gs)))
    t.check('ningun grosor pasa de Grosormax', max(gs) <= gmax + 1e-9, '%.3f' % max(gs))
    cg['grosor_tiempo'] = 0
    m.end_cycle(W2, cg, 0.0, 10 * cmax)
    t.check('sin Grosortiempo: Shellthick', abs(m.shell_th(W2['shells'][-1], cg) - th) < 1e-6)
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
