"""
=============================================================================
ESTRATOS - FASE 4: EL LIMITE COMO MOTOR
=============================================================================
Desbordamiento, ramificacion, fusion y coronacion. Requiere la fase 3.

QUE HACE
--------
Cuando una formacion ha llegado al limite de altura, la senal que no
puede subir se DESBORDA a una celda vecina:

    ocupacion 4-5   ramificacion: satelites en la vecindad
    ocupacion 6-7   fusion: un macizo bajo une el nucleo con sus satelites
    ocupacion 8+    coronacion: una aguja ambar remata la formacion

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

VERSION = 'fase4 v3  (desborde, satelites, fusion, coronacion; polos y anillos)'
banner(VERSION)

base = require_base(4)
motor = install_core(base, CARPETA, 4)

page = get_page(base, 'Fase4')
add_par(base, page, 'int', 'Umbralram', 'Ramificacion desde (ocupacion)', 4, 2, 12, clamp=True)
add_par(base, page, 'int', 'Umbralfusion', 'Fusion desde (ocupacion)', 6, 3, 16, clamp=True)
add_par(base, page, 'int', 'Umbralcorona', 'Coronacion desde (ocupacion)', 8, 4, 24, clamp=True)
add_par(base, page, 'float', 'Tamsatelite', 'Tamano de satelite', 0.6, 0.2, 1.0)
add_par(base, page, 'float', 'Limsatelite', 'Altura max. de satelite (x limite)', 0.6, 0.2, 1.0)
add_par(base, page, 'menu', 'Vecina', 'Quien elige la vecina', 'velocidadocupacion',
        menu=['velocidad', 'velocidadocupacion'],
        menu_labels=['Velocidad', 'Velocidad + ocupacion'])
ok('pagina Fase4: Umbralram, Umbralfusion, Umbralcorona, Tamsatelite, '
   'Limsatelite, Vecina')

make_constant(base, 'mat_corona', 780, 460, (1.0, 0.70, 0.30))
make_instanced(base, 'coronas', 520, 460, 'mat_corona')
set_render(base)

leeme(base, 4, """FASE 4 - EL LIMITE COMO MOTOR
  Desde la ocupacion 4 la senal se desborda a una vecina (6 entre anillos
  completos; el polo, todo su anillo). La elige la velocidad (+ ocupacion).
    4-5 satelites, 6-7 fusion (macizo bajo), 8+ coronacion (aguja ambar).
  La presion sobre una formacion ajena le suma ocupacion sin cascada.
  Umbrales y tamanos en la pagina Fase4.""")

print_report()


def prueba(t):
    m = t.m
    m.reset_world()
    c = m.cfg()
    i = m.note_cell(64)
    for k in range(9):
        t.midi(0x9C, 0x40, 0x64)
    W = m.world()
    sats = m.satellites_of(W, i)
    t.check('9 notas en mi4 -> ocupacion 9', W['occ'][i] == 9)
    t.check('aparecen satelites en celdas vecinas',
            len(sats) >= 1 and all(j in m.NEIGH[i] for j in sats),
            'satelites en %s' % sats)
    t.check('estado: coronacion', m.state_name(c, W['occ'][i], c['nivel']) == 'coronacion')
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, 0.0)
    cor = base.op('i_coronas')
    cor.cook(force=True)
    t.check('i_coronas: una corona', cor.numSamples == 1, '%d' % cor.numSamples)
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
print('  topan con el limite y empiezan a ramificar hacia sus vecinas.')
print('  Gira el knob RANDOMNESS del SEQ1 y mira la columna vel de midi_log:')
print('  si la velocidad cambia, la ramificacion cambia de lado.')
print('=' * 66)
