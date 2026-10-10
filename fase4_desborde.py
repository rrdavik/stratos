"""
=============================================================================
ESTRATOS - FASE 4: EL LIMITE COMO MOTOR
=============================================================================
Desbordamiento, ramificacion, fusion y coronacion. Requiere la fase 3.

QUE HACE
--------
Cuando una formacion ha llegado al limite de altura, cada trigger (en el
limite cuesta Costemax notas, 5) se DESBORDA a una celda vecina:

    ocupacion 5-6   ramificacion: satelites en la vecindad      11 notas
    ocupacion 7-8   fusion: un macizo bajo une el nucleo        21 notas
                    con sus satelites
    ocupacion 9-10  coronacion: una aguja ambar remata          31 notas
    ocupacion 11+   cumbre: cada trigger alarga la corona un    41 notas
                    25 %, hasta Tramoscumbre (4) tramos

La PRESION sobre una formacion ajena le suma 1 a la carga (como una nota),
sin cascada.

LA VECINDAD (decision tomada)
-----------------------------
Polos y anillos (uno por octava). Entre dos anillos completos, hexagonal
desplazada: 2 vecinas en el anillo, 2 arriba y 2 abajo. En los anillos
incompletos, las del anillo contiguo cuyo arco se solapa con el suyo, y
en los anillos extremos tambien el polo. El polo tiene de vecinas todo su
anillo.

QUIEN ELIGE LA VECINA (decision tomada)
---------------------------------------
No el azar del software: un valor que viene del BeatStep.
  Vecina = velocidad             (velocidad de la nota) mod vecinas
  Vecina = velocidad + ocupacion (por defecto)
Con la velocidad fija del BeatStep, el primer modo desborda siempre hacia
el mismo lado; el segundo da la vuelta a la formacion conforme insiste.
Si el knob RANDOMNESS del SEQ1 varia la velocidad (miralo en midi_log),
la eleccion queda en manos del aparato.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase4_desborde.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase4 v5  (desborde con carga, satelites, fusion, coronacion, cumbre)'
banner(VERSION)

base = require_base(4)
motor = install_core(base, CARPETA, 4)

page = get_page(base, 'Fase4')
add_par(base, page, 'int', 'Umbralram', 'Ramificacion desde (ocupacion)', 5, 2, 12, clamp=True)
add_par(base, page, 'int', 'Umbralfusion', 'Fusion desde (ocupacion)', 7, 3, 16, clamp=True)
add_par(base, page, 'int', 'Umbralcorona', 'Coronacion desde (ocupacion)', 9, 4, 24, clamp=True)
add_par(base, page, 'int', 'Umbralcumbre', 'Cumbre desde (ocupacion)', 11, 5, 32, clamp=True)
add_par(base, page, 'int', 'Tramoscumbre', 'Tramos de cumbre (25 % cada uno)', 4, 0, 12, clamp=True)
renew_default(base, 'Umbralram', 4, 5)
renew_default(base, 'Umbralfusion', 6, 7)
renew_default(base, 'Umbralcorona', 8, 9)
# los de la fase 3, por si no se ha relanzado
renew_default(base, 'Alturafactor', 3.0, 3.75)
renew_default(base, 'Semillafrac', 0.25, 0.20)
renew_default(base, 'Growstep', 0.30, 0.20)
if not has_par(base, 'Costemax'):
    add_par(base, get_page(base, 'Fase3'), 'int', 'Costemax', 'Notas por trigger en el limite',
            5, 1, 12, clamp=True)
if not has_par(base, 'Gatemax'):
    add_par(base, get_page(base, 'Fase3'), 'float', 'Gatemax', 'Gate ligado: crecimiento max. (x)',
            1.25, 1.0, 2.0)
add_par(base, page, 'float', 'Tamsatelite', 'Tamano de satelite', 0.6, 0.2, 1.0)
add_par(base, page, 'float', 'Limsatelite', 'Altura max. de satelite (x limite)', 0.6, 0.2, 1.0)
add_par(base, page, 'menu', 'Vecina', 'Quien elige la vecina', 'velocidadocupacion',
        menu=['velocidad', 'velocidadocupacion'],
        menu_labels=['Velocidad', 'Velocidad + ocupacion'])
ok('pagina Fase4: Umbralram, Umbralfusion, Umbralcorona, Umbralcumbre, Tramoscumbre, Tamsatelite, '
   'Limsatelite, Vecina')

make_constant(base, 'mat_corona', 780, 460, (1.0, 0.70, 0.30))
make_instanced(base, 'coronas', 520, 460, 'mat_corona')
set_render(base)

leeme(base, 4, """FASE 4 - EL LIMITE COMO MOTOR
  En el limite (ocupacion 5) cada trigger cuesta Costemax notas (5) y se
  desborda a una vecina (6 entre anillos completos; el polo, todo su
  anillo). La elige la velocidad (+ ocupacion).
    5-6 satelites, 7-8 fusion (macizo bajo), 9-10 coronacion (aguja ambar),
    11+ cumbre (la corona crece un 25 % por trigger, Tramoscumbre tramos).
  La presion sobre una formacion ajena le suma carga sin cascada.
  Umbrales y tamanos en la pagina Fase4.""")

print_report()


def prueba(t):
    m = t.m
    m.reset_world()
    c = m.cfg()
    i = m.note_cell(64)
    W = m.world()
    for k in range(11):
        t.midi(0x9C, 0x40, 0x64)
    t.check('11 notas en mi4 -> limite y primer desborde',
            W['occ'][i] == c['th_branch'] and len(m.satellites_of(W, i)) == 1,
            'ocupacion %d' % W['occ'][i])
    for k in range(4):
        t.midi(0x9C, 0x40, 0x64)
    t.check('4 notas mas solo cargan', W['occ'][i] == c['th_branch'] and W['carga'][i] == 4,
            'carga %d/%d' % (W['carga'][i], m.cost(c, W['occ'][i])))
    for k in range(16):
        t.midi(0x9C, 0x40, 0x64)
    sats = m.satellites_of(W, i)
    t.check('31 notas en mi4 -> ocupacion 9', W['occ'][i] == 9, '%d' % W['occ'][i])
    t.check('aparecen satelites en celdas vecinas',
            len(sats) >= 1 and all(j in m.NEIGH[i] for j in sats),
            'satelites en %s' % sats)
    t.check('estado: coronacion', m.state_name(c, W['occ'][i], c['nivel']) == 'coronacion')
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, 0.0)
    cor = base.op('i_coronas')
    cor.cook(force=True)
    t.check('i_coronas: una corona', cor.numSamples == 1, '%d' % cor.numSamples)
    largo0 = m._CACHE['inst']['coronas'][0][7]
    for k in range(10):
        t.midi(0x9C, 0x40, 0x64)
    W['vh'] = list(W['h'])
    largo1 = m.build_instances(W, c, 0.0)['coronas'][0][7]
    t.check('41 notas -> cumbre: la corona crece',
            m.state_name(c, W['occ'][i], c['nivel']) == 'cumbre' and largo1 > largo0 * 1.2,
            'corona %.2f -> %.2f' % (largo0, largo1))
    j = m.NEIGH[i][0]
    W2 = m.new_world()
    m.note_on(W2, c, m.GEO, m.cell_note(j), 100, 0.0)
    m.note_on(W2, c, m.GEO, m.cell_note(j), 100, 0.0)
    o_j, k_j = W2['occ'][j], W2['carga'][j]
    W2['occ'][i], W2['own'][i], W2['sp'][i], W2['h'][i] = c['th_branch'], m.GEO, m.GEO, m.limit(c)
    n_nb = len(m.NEIGH[i])
    vel = 0 if c['neigh_mode'] == 0 else (n_nb - c['th_branch'] % n_nb) % n_nb
    m.overflow(W2, c, i, m.GEO, vel, 1.0)          # desborda a la vecina 0
    t.check('presion: suma 1 a la carga de la vecina',
            W2['carga'][j] == k_j + 1 and W2['occ'][j] == o_j,
            'carga %d -> %d' % (k_j, W2['carga'][j]))
    vec = [len(m.NEIGH[x]) for x in range(m.N) if not m.is_pole(x)]
    t.check('vecindad: hasta 6 vecinas entre anillos; el polo, todo su anillo',
            max(vec) <= 8 and min(vec) >= 1
            and len(m.NEIGH[m.POLE_S]) == len(m.RINGS[0])
            and len(m.NEIGH[m.POLE_N]) == len(m.RINGS[-1]),
            'celdas %d-%d, polo %d' % (min(vec), max(vec), len(m.NEIGH[m.POLE_S])))
    leg = m.legend()
    t.check('leyenda DESBORDE', 'DESBORDE' in leg)


run_test(base, prueba)
print('  Ahora: deja el SEQ1 insistiendo en pocas notas. Las formaciones')
print('  topan con el limite y empiezan a ramificar hacia sus vecinas,')
print('  una vez cada Costemax notas.')
print('  Gira el knob RANDOMNESS del SEQ1 y mira la columna vel de midi_log:')
print('  si la velocidad cambia, la ramificacion cambia de lado.')
print('=' * 66)
