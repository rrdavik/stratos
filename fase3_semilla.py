"""
=============================================================================
ESTRATOS - FASE 3: LA SEMILLA (OCUPACION Y CRECIMIENTO VERTICAL)
=============================================================================
Se apoya en fase12_base.py (fases 1 y 2). No la rehace: le anade piezas.

QUE HACE
--------
Cada nota del SEQ1 suma 1 a la OCUPACION de su celda, y en la celda crece
una formacion geologica:

    ocupacion 1     semilla (altura minima)
    ocupacion 2-3   crece en altura (lo que dure el gate decide cuanto)
    ocupacion 4+    se queda en el LIMITE DE ALTURA = 3 x grosor de concha
                    (el desbordamiento llega en la fase 4)

El MATERIAL lo fija la velocidad de la primera nota y no vuelve a cambiar:
velocidad alta = pulido, casi metalico; baja = poroso y mate.

RETICULA DE POLO A POLO (v5): cada semitono entre Notapolosur (24, do1)
y Notapolonorte (108, do8) es una celda; los dos polos van entre do1 y
do8. La mas grave es el polo sur, la mas aguda el polo norte, y las de
en medio se reparten en anillos, uno por octava: la clase de nota es el
meridiano. Con do1-do8: un anillo de 11 (do#1-si1), seis de 12 (do2-si7)
y do8 en el polo norte. Fuerarango decide que pasa con las notas de
fuera: plegar por octavas, ignorar o limitar al polo. Los tres estan en
la pagina Fase3. Cambiar el rango rehace la reticula y vacia el mundo.

BALANCEO DEL EJE (v2): ademas del giro al tempo, el eje del planeta se
balancea lentamente hacia la camara y en contra (rx), para ver los dos
polos. Ajeno al reloj del secuenciador; se congela con Pausa.
    Rotextra      encendido / apagado (entra y sale en 3 s, sin saltos)
    Balanceo      amplitud en grados (60)
    Balanceoper   segundos por vaiven completo (90)

QUE INSTALA
-----------
  motor             el estado del mundo y toda la logica (estratos_motor.py)
  formas_pulidas    formaciones con material pulido  (+ i_formas_pulidas)
  formas_porosas    formaciones con material poroso  (+ i_formas_porosas)
  formas_callbacks  el Script CHOP que pide al motor las instancias
  pulsos            los botones de la pagina Fase3
Y reescribe midi_callbacks, latido, baliza_callbacks y reticula_callbacks
para que pasen por el motor (la baliza se posa encima de la formacion).

COMO USARLO
-----------
Los cuatro archivos tienen que estar en la misma carpeta:
    estratos_motor.py  estratos_comun.py  fase3_semilla.py  (y los demas)

    exec(open('C:/Users/DareDave/Downloads/est/fase3_semilla.py').read())

Si cambias de carpeta, cambia tambien CARPETA aqui abajo.
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase3 v5  (ocupacion, semilla, crecimiento, material, balanceo, polos y anillos)'
banner(VERSION)

base = require_base(3)
motor = install_core(base, CARPETA, 3)

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase3)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase3')
add_par(base, page, 'float', 'Shellthick', 'Grosor de concha', 0.5, 0.05, 2.0)
add_par(base, page, 'float', 'Alturafactor', 'Limite de altura (x grosor)', 3.0, 1.0, 8.0)
add_par(base, page, 'float', 'Semillafrac', 'Altura de la semilla (x limite)', 0.25, 0.05, 1.0)
add_par(base, page, 'float', 'Growstep', 'Crecimiento por senal (x limite)', 0.30, 0.05, 1.0)
add_par(base, page, 'toggle', 'Gatemode', 'El gate decide el crecimiento', True)
add_par(base, page, 'int', 'Umbralvel', 'Velocidad: pulido a partir de', 64, 1, 127, clamp=True)
add_par(base, page, 'int', 'Velprueba', 'Velocidad de prueba', 100, 1, 127, clamp=True)
add_par(base, page, 'pulse', 'Sembrar', 'Sembrar en Nota (prueba)')
add_par(base, page, 'pulse', 'Resetmundo', 'Vaciar el mundo')
ok('pagina Fase3: Shellthick, Alturafactor, Semillafrac, Growstep, Gatemode, '
   'Umbralvel, Velprueba, Sembrar, Resetmundo, Rotextra, Balanceo, Balanceoper')

# -----------------------------------------------------------------------------
# MATERIALES Y GEOMETRIA
# -----------------------------------------------------------------------------

make_phong(base, 'mat_pulido', 780, 380, spec=1.0, shin=70, diff=1.0)
make_phong(base, 'mat_poroso', 780, 300, spec=0.03, shin=4, diff=0.9)
ok('materiales: mat_pulido (brillo alto) y mat_poroso (mate)')

make_instanced(base, 'formas_porosas', 520, 300, 'mat_poroso')
make_instanced(base, 'formas_pulidas', 520, 380, 'mat_pulido')
set_render(base)

leeme(base, 3, """FASE 3 - LA SEMILLA
  Cada nota del SEQ1 suma ocupacion a su celda:
    1 semilla, 2-3 crece, 4+ limite de altura (3 x Shellthick).
  El gate largo crece mas que el corto (Gatemode). El material lo fija la
  velocidad de la primera nota (Umbralvel): pulido o poroso.
  Prueba sin BeatStep: elige Nota (pagina Fase2) y pulsa Sembrar.
  Resetmundo vacia el planeta.
  Rotextra balancea el eje (Balanceo grados, cada Balanceoper s) para
  ver los polos.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA: notas simuladas por el mismo camino que el MIDI real
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    m.reset_world()
    c = m.cfg()
    i = m.note_cell(64)
    lim = m.limit(c)
    t.midi(0x9C, 0x40, 0x64)                         # mi4, canal 13, vel 100
    W = m.world()
    t.check('1 nota  -> semilla', W['occ'][i] == 1 and abs(W['h'][i] - c['seed_frac'] * lim) < 1e-6,
            'ocupacion %d' % W['occ'][i])
    t.midi(0x9C, 0x40, 0x64)
    t.midi(0x9C, 0x40, 0x64)
    t.check('3 notas -> crece', W['h'][i] > c['seed_frac'] * lim, 'altura %.2f' % W['h'][i])
    t.midi(0x9C, 0x40, 0x64)
    t.midi(0x9C, 0x40, 0x64)
    t.midi(0x9C, 0x40, 0x64)
    t.check('6 notas -> limite de altura, sin desbordar',
            abs(W['h'][i] - lim) < 1e-6 and m.occupied(W) == 1,
            'altura %.2f de %.2f, celdas %d' % (W['h'][i], lim, m.occupied(W)))
    t.midi(0x90, 0x40, 0x64)                         # canal 1: se ignora
    t.check('nota en el canal 1 ignorada', W['occ'][i] == 6)
    t.midi(0x9C, 0x30, 0x14)                         # do3, vel 20: porosa
    j = m.note_cell(48)
    t.check('velocidad 20 -> material poroso', W['vel'][j] == 20 and W['vel'][i] == 100)
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, 0.0)
    chop = base.op('i_formas_pulidas')
    chop.cook(force=True)
    n_pul = chop.numSamples
    chop2 = base.op('i_formas_porosas')
    chop2.cook(force=True)
    t.check('i_formas_pulidas tiene piezas', n_pul >= 3 and chop['ry'] is not None,
            '%d piezas' % n_pul)
    t.check('i_formas_porosas tiene piezas', chop2.numSamples >= 1,
            '%d piezas' % chop2.numSamples)
    leg = m.legend()
    t.check('leyenda MUNDO', 'MUNDO' in leg and ('ocupadas 2/%d' % m.N) in leg)
    sin_bal = [n for n in ('nucleo', 'reticula', 'baliza', 'formas_pulidas', 'formas_porosas')
               if 'wobble(' not in (base.op(n).par.rx.expr or '')]
    t.check('balanceo del eje en el planeta', not sin_bal,
            'sin balanceo: %s' % ', '.join(sin_bal) if sin_bal else '')
    st = {'ph': 0.0, 'env': 1.0}
    m.wobble_step(st, 0.25, True, False, 60.0, 4.0)      # periodo minimo 5 s
    w = m.wobble_step(st, 1.0 / 60, True, False, 60.0, 5.0)
    t.check('balanceo dentro de la amplitud', 0 < w <= 60.0, '%.1f grados' % w)
    v = m.world_dir((0.0, 1.0, 0.0), 0.0, 0.0, 90.0)
    t.check('balanceo de 90: el polo mira a la camara', abs(v[2] - 1.0) < 1e-6)
    lo, hi = m.GRID['lo'], m.GRID['hi']
    t.check('Notapolosur y Notapolonorte caen en los polos',
            m.note_cell(lo) == m.POLE_S and m.note_cell(hi) == m.POLE_N
            and m.normal_i(m.POLE_S)[1] < -0.999 and m.normal_i(m.POLE_N)[1] > 0.999,
            '%s %d y %s %d, %d celdas' % (m.note_name(lo), lo, m.note_name(hi), hi, m.N))
    t.check('vecindad simetrica', all(i in m.NEIGH[j] for i in range(m.N) for j in m.NEIGH[i]))
    t.check('fuera de rango: plegar / ignorar / limitar',
            m.fold_note(lo - 1, 0) == lo + 11 and m.fold_note(lo - 1, 1) is None
            and m.fold_note(hi + 5, 2) == hi)


run_test(base, prueba)
print('  Ahora: PLAY en el BeatStep con el SEQ1 sonando.')
print('  Cada nota deja una formacion; las repetidas crecen hasta el limite.')
print('  Sin BeatStep: Nota (pagina Fase2) + Sembrar (pagina Fase3).')
print('  Para empezar de cero: Resetmundo.')
print('=' * 66)
