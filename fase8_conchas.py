"""
=============================================================================
ESTRATOS - FASE 8: CONCHAS (ENTERRAR EL MUNDO)
=============================================================================
Requiere la fase 7.

QUE HACE
--------
Al terminar cada ciclo de ecosistema (fase 6):

  1. La capa activa se ENTIERRA: se convierte en una concha de 96
     losetas (una por celda) con el color de su generacion. Las celdas
     que estaban ocupadas quedan mas claras: los continentes se leen en
     el color. Las formaciones de esa capa se descartan.
  2. El planeta engorda un grosor de concha (Shellthick).
  3. El 25 % de la ocupacion de cada celda pasa a la capa nueva (la
     fraccion que no llega a 1 se acumula para el ciclo siguiente). Lo
     heredado vuelve a brotar desde la nueva superficie.

El radio del cuerpo ES el tiempo transcurrido.

EL HORNEADO (decision tomada)
-----------------------------
El marco habla de hornear cada concha a una textura sobre una esfera.
Aqui la concha es una capa de 96 losetas instanciadas: igual de barata
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

VERSION = 'fase8 v1  (conchas, herencia, radio que crece)'
banner(VERSION)

base = require_base(8)
motor = install_core(base, CARPETA, 8)

page = get_page(base, 'Fase8')
add_par(base, page, 'float', 'Herencia', 'Herencia entre conchas', 0.25, 0.0, 1.0)
add_par(base, page, 'int', 'Maxconchas', 'Conchas visibles', 24, 1, 96, clamp=True)
ok('pagina Fase8: Herencia (25 %), Maxconchas (24)')

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
  En cada fin de ciclo la capa se entierra como 96 losetas con el color de
  su generacion; el radio crece Shellthick; Herencia (25 %) pasa a la
  capa nueva. Maxconchas visibles; las demas, dentro del nucleo.
  Prueba sin esperar: Forzarciclo (pagina Fase6).""")

print_report()


def prueba(t):
    m = t.m
    c = m.cfg()
    W = m.new_world()
    for g in range(4):
        for k in range(8):
            m.note_on(W, c, 1, 64, 100, g * 10 + k)
        m.end_cycle(W, c, g * 10 + 9)
    i = m.note_cell(64)
    t.check('4 ciclos -> 4 conchas', m.n_shells(W) == 4)
    t.check('el radio crece 4 grosores',
            abs(m.top_radius(W, c) - (c['core_radius'] + 4 * c['shell_thick'])) < 1e-6,
            '%.2f' % m.top_radius(W, c))
    t.check('herencia: la celda insistente sigue ocupada', W['occ'][i] >= 2, str(W['occ'][i]))
    t.check('losetas: 98 por concha', len(m.build_tiles(W, c, 0.0)) == 4 * 98)
    # por el camino real
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    n0 = m.n_shells(m.world())
    m.on_pulse('Forzarciclo')
    t.check('Forzarciclo entierra la capa', m.n_shells(m.world()) == n0 + 1)
    m._CACHE['inst'] = m.build_instances(m.world(), m.cfg(), 0.0)
    est = base.op('i_estratos')
    est.cook(force=True)
    t.check('i_estratos dibuja la concha', est.numSamples == 98, '%d' % est.numSamples)
    t.check('leyenda CONCHAS', 'CONCHAS' in m.legend())


run_test(base, prueba)
print('  Ahora: deja sonar varios ciclos (o pulsa Forzarciclo en la pagina')
print('  Fase6). El planeta engorda una capa por ciclo.')
print('  Si engorda demasiado rapido: sube Repsporciclo o baja Shellthick.')
print('=' * 66)
