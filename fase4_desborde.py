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
la eleccion queda en manos del aparato. Desde la v8 es siempre la
segunda (no hay parametro Vecina): con la velocidad fija del BeatStep la
primera desbordaba siempre hacia el mismo lado.

LA PAGINA FASE4 (v8): 4 parametros en vez de 8.
  Umbralram     ramificacion desde (ocupacion 5)
  Pasoumbral    ocupaciones de un estado al siguiente (2): fusion en
                Umbralram + 2, coronacion + 4, cumbre + 6 (7, 9 y 11);
                antes Umbralfusion, Umbralcorona y Umbralcumbre
  Tramoscumbre  tramos de cumbre (4, un 25 % cada uno)
  Satelite      tamano y altura maxima del satelite, x la formacion madre
                (0,6); antes Tamsatelite y Limsatelite
Relanzar cualquier fase pasa un proyecto anterior a estos cuatro: el paso
sale de Umbralram a Umbralcumbre y Satelite es la media de los dos.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase4_desborde.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase4 v8  (pagina mas corta: umbrales a paso fijo, un solo Satelite)'
banner(VERSION)

base = require_base(4)
motor = install_core(base, CARPETA, 4)

page = get_page(base, 'Fase4')
add_fase4_pars(base, page)
renew_default(base, 'Umbralram', 4, 5)
# los de la fase 3, por si no se ha relanzado
renew_default(base, 'Alturafactor', 3.0, 3.75)
renew_default(base, 'Semillafrac', 0.25, 0.20)
if not has_par(base, 'Costemax'):
    add_par(base, get_page(base, 'Fase3'), 'int', 'Costemax', 'Notas por trigger en el limite',
            5, 1, 12, clamp=True)
if not has_par(base, 'Gatemax'):
    add_par(base, get_page(base, 'Fase3'), 'float', 'Gatemax', GATEMAX_LABEL, 1.25, 1.0, 2.0)
ok('pagina Fase4: Umbralram (5), Pasoumbral (2: fusion 7, corona 9, cumbre 11), Tramoscumbre, '
   'Satelite')

materiales_formas(base)
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
  Pagina Fase4: Umbralram y Pasoumbral (los estados, a paso fijo),
  Tramoscumbre y Satelite (tamano y altura del satelite).""")

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
    c10 = dict(c)
    c10['nivel'] = min(c10['nivel'], 10)   # las coronas en caja (desde la fase 11, del tema)
    m._CACHE['inst'] = m.build_instances(W, c10, 0.0)
    cor = base.op('i_coronas')
    cor.cook(force=True)
    t.check('i_coronas: una corona', cor.numSamples == 1, '%d' % cor.numSamples)
    largo0 = m._CACHE['inst']['coronas'][0][7]
    for k in range(10):
        t.midi(0x9C, 0x40, 0x64)
    W['vh'] = list(W['h'])
    largo1 = m.build_instances(W, c10, 0.0)['coronas'][0][7]
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
    # v8: la pagina mas corta
    fuera = [nm for nm in ('Umbralfusion', 'Umbralcorona', 'Umbralcumbre', 'Tamsatelite',
                           'Limsatelite', 'Vecina') if has_par(base, nm)]
    t.check('pagina Fase4: solo Umbralram, Pasoumbral, Tramoscumbre y Satelite',
            not fuera and all(has_par(base, nm) for nm in FASE4_PARS),
            'siguen: %s' % ', '.join(fuera) if fuera else '')
    paso = int(base.par.Pasoumbral)
    t.check('fusion, corona y cumbre a Pasoumbral una de otra',
            (c['th_fusion'], c['th_crown'], c['th_cumbre'])
            == tuple(c['th_branch'] + k * paso for k in (1, 2, 3)),
            '%d %d %d %d' % (c['th_branch'], c['th_fusion'], c['th_crown'], c['th_cumbre']))
    t.check('Satelite: tamano y altura del satelite',
            c['sat_size'] == c['sat_limit'] == float(base.par.Satelite))


run_test(base, prueba)
print('  Ahora: deja el SEQ1 insistiendo en pocas notas. Las formaciones')
print('  topan con el limite y empiezan a ramificar hacia sus vecinas,')
print('  una vez cada Costemax notas.')
print('  Gira el knob RANDOMNESS del SEQ1 y mira la columna vel de midi_log:')
print('  si la velocidad cambia, la ramificacion cambia de lado.')
print('=' * 66)
