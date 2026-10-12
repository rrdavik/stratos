"""
=============================================================================
ESTRATOS - FASE 3: LA SEMILLA (OCUPACION Y CRECIMIENTO VERTICAL)
=============================================================================
Se apoya en fase12_base.py (fases 1 y 2). No la rehace: le anade piezas.

QUE HACE
--------
Cada nota del SEQ1 suma 1 a la CARGA de su celda. Cuando la carga llega
al COSTE se dispara un trigger de construccion y la OCUPACION sube 1. El
coste crece con la altura: 1 nota abajo, Costemax (5) en el limite. Cada
nota sube la formacion Growstep / coste: cuanto mas alta, mas despacio
(la frenada). Cada nota hace latir la formacion aunque no construya.

    ocupacion 1     semilla (20 % del limite)                    1 nota
    ocupacion 2     brote (40 %)                                 2 notas
    ocupacion 3     crecimiento (60 %)                           4 notas
    ocupacion 4     madurez (80 %)                               7 notas
    ocupacion 5+    LIMITE DE ALTURA = 3,75 x grosor de concha  11 notas
                    (el desbordamiento llega en la fase 4)
El gate decide cuanto sube cada nota: corto, hasta 1/4; ligado, como
mucho Gatemax veces (1,25). Nunca adelanta la altura al escalon que se
esta construyendo.

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
Y reescribe midi_callbacks, latido y reticula_callbacks para que pasen por
el motor.

LUZ DE CELDA (v9): sin balizas. La baliza cian de las fases 1 y 2 se
retira; cada nota del SEQ1 enciende el CENTRO de su celda en cian (blanco
desde la fase 9): un pulso con la nota y tenue hasta la siguiente, para
que se vea donde esta. Con formacion, el centro se ensancha hasta asomar
alrededor de su base. Interruptor: Luzseq (pagina Fase3).

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

VERSION = 'fase3 v10  (carga y frenada, luz de celda, material, balanceo, polos y anillos)'
banner(VERSION)

base = require_base(3)
motor = install_core(base, CARPETA, 3)

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase3)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase3')
add_par(base, page, 'float', 'Shellthick', 'Grosor de concha', 0.5, 0.05, 2.0)
add_par(base, page, 'float', 'Alturafactor', 'Limite de altura (x grosor)', 3.75, 1.0, 8.0)
add_par(base, page, 'float', 'Semillafrac', 'Altura de la semilla (x limite)', 0.20, 0.05, 1.0)
add_par(base, page, 'float', 'Growstep', 'Crecimiento por trigger (x limite)', 0.20, 0.05, 1.0)
add_par(base, page, 'int', 'Costemax', 'Notas por trigger en el limite', 5, 1, 12, clamp=True)
renew_default(base, 'Alturafactor', 3.0, 3.75)
renew_default(base, 'Semillafrac', 0.25, 0.20)
renew_default(base, 'Growstep', 0.30, 0.20)
add_par(base, page, 'toggle', 'Gatemode', 'El gate decide el crecimiento', True)
add_par(base, page, 'float', 'Gatemax', 'Gate ligado: crecimiento max. (x)', 1.25, 1.0, 2.0)
add_par(base, page, 'int', 'Umbralvel', 'Velocidad: pulido a partir de', 64, 1, 127, clamp=True)
add_par(base, page, 'int', 'Velprueba', 'Velocidad de prueba', 100, 1, 127, clamp=True)
add_par(base, page, 'pulse', 'Sembrar', 'Sembrar en Nota (prueba)')
add_par(base, page, 'pulse', 'Resetmundo', 'Vaciar el mundo')
ok('pagina Fase3: Shellthick, Alturafactor, Semillafrac, Growstep, Costemax, Gatemode, Gatemax, '
   'Umbralvel, Velprueba, Sembrar, Resetmundo, Rotextra, Balanceo, Balanceoper')

# -----------------------------------------------------------------------------
# MATERIALES Y GEOMETRIA
# -----------------------------------------------------------------------------

materiales_formas(base)
ok('materiales: mat_pulido (reflejo ancho) y mat_poroso (mate, sin reflejo)')

make_instanced(base, 'formas_porosas', 520, 300, 'mat_poroso')
make_instanced(base, 'formas_pulidas', 520, 380, 'mat_pulido')
set_render(base)

leeme(base, 3, """FASE 3 - LA SEMILLA
  Cada nota del SEQ1 suma carga a su celda; al llegar al coste se
  dispara un trigger y la ocupacion sube 1. El coste sube con la altura,
  de 1 a Costemax (5) en el limite, y cada nota sube menos (frenada):
    1 semilla, 2 brote, 3 crecimiento, 4 madurez, 5+ limite (3,75 x Shellthick).
    Notas: 1, 2, 4, 7 y 11. Costemax 1 = una nota por trigger.
  Gate ligado: como mucho Gatemax (1,25) veces; nunca pasa del escalon.
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
    hs = [W['h'][i]]
    for k in range(3):
        t.midi(0x9C, 0x40, 0x64)
        hs.append(W['h'][i])
    t.check('4 notas -> crecimiento (ocupacion 3)', W['occ'][i] == 3 and hs[-1] > hs[0],
            'ocupacion %d, altura %.2f' % (W['occ'][i], W['h'][i]))
    t.check('frenada: la nota 3 sube menos que la 2', hs[2] - hs[1] < hs[1] - hs[0] - 1e-6,
            '%.3f < %.3f' % (hs[2] - hs[1], hs[1] - hs[0]))
    t.check('carga: la nota 3 no dispara trigger', m.cost(c, 2) == 2)
    W2 = m.new_world()
    for k in range(3):
        m.note_on(W2, c, m.GEO, 64, 100, float(k))
    h3 = W2['h'][i]
    m.note_off(W2, c, m.GEO, 64, 2.0 + 10.0, 120.0)   # gate larguisimo
    t.check('gate ligado: como mucho Gatemax y sin pasar del escalon',
            W2['h'][i] <= m.height_for(c, W2['occ'][i] + 1) + 1e-9
            and W2['h'][i] - h3 <= (c['gate_max'] - 1.0) * c['grow_frac'] * lim / 2 + 1e-9,
            '%.3f -> %.3f' % (h3, W2['h'][i]))
    for k in range(6):
        t.midi(0x9C, 0x40, 0x64)
    t.check('10 notas -> madurez, aun bajo el limite',
            W['occ'][i] == c['th_branch'] - 1 and W['h'][i] < lim,
            'ocupacion %d, altura %.2f de %.2f' % (W['occ'][i], W['h'][i], lim))
    t.midi(0x9C, 0x40, 0x64)
    o11 = W['occ'][i]
    desborda = c['nivel'] >= 4            # relanzada sobre un proyecto ya avanzado
    t.check('11 notas -> limite de altura' + ('' if desborda else ', sin desbordar'),
            abs(W['h'][i] - lim) < 1e-6 and o11 == c['th_branch']
            and (desborda or m.occupied(W) == 1),
            'altura %.2f de %.2f, celdas %d' % (W['h'][i], lim, m.occupied(W)))
    t.check('en el limite cada trigger cuesta Costemax notas',
            m.cost(c, o11) == int(c['cost_max']), '%d' % m.cost(c, o11))
    t.midi(0x90, 0x40, 0x64)                         # canal 1: se ignora
    t.check('nota en el canal 1 ignorada', W['occ'][i] == o11 and W['carga'][i] == 0)
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
    t.check('leyenda MUNDO', 'MUNDO' in leg and ('ocupadas %d/%d' % (m.occupied(W), m.N)) in leg)
    sin_bal = [n for n in ('nucleo', 'reticula', 'luz_celda', 'formas_pulidas', 'formas_porosas')
               if 'wobble(' not in (base.op(n).par.rx.expr or '')]
    t.check('balanceo del eje en el planeta', not sin_bal,
            'sin balanceo: %s' % ', '.join(sin_bal) if sin_bal else '')
    # luz de celda: la nota del SEQ1 enciende el centro de su celda
    Wl = m.new_world()
    cl_ = dict(c)
    m.note_on(Wl, cl_, m.GEO, 64, 100, 1.0)
    pulso = [r for r in m.cell_lights(Wl, cl_, 1.0)]
    reposo = [r for r in m.cell_lights(Wl, cl_, 5.0)]
    col = m.seq_color(cl_, 1)
    t.check('nota del SEQ1: el centro de su celda en su color, y tenue hasta la siguiente',
            len(pulso) == 1 and len(reposo) == 1
            and abs(pulso[0][9] - col[0]) < 1e-6 and reposo[0][10] < pulso[0][10]
            and abs(reposo[0][10] / col[1] - 0.6) < 0.01,
            '%d / %d losetas' % (len(pulso), len(reposo)))
    t.check('sin baliza del SEQ1', base.op('baliza') is None and base.op('baliza_chop') is None)
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
print('  Cada nota deja una formacion; las repetidas crecen hasta el limite,')
print('  cada vez mas despacio (11 notas hasta el limite con Costemax 5).')
print('  Sin BeatStep: Nota (pagina Fase2) + Sembrar (pagina Fase3).')
print('  Para empezar de cero: Resetmundo.')
print('=' * 66)
