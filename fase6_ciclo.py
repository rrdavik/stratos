"""
=============================================================================
ESTRATOS - FASE 6: EL CICLO (LO CIERRA EL MUNDO)
=============================================================================
Requiere la fase 5.

QUE HACE
--------
El ciclo de ecosistema ya no sale de la longitud de los patterns: lo cierra
el propio mundo. Se inspira en el ciclo adaptativo de Holling (crecer,
madurar, liberar, reorganizar): el mundo se ENTIERRA (fase 8) cuando esta
maduro y deja de cambiar, o cuando alcanza su edad maxima.

  RELOJ DE COMPASES  cuenta compases con el tempo del proyecto (el mismo
                     que hace girar el nucleo). Solo avanza con la linea
                     de tiempo en play, sin STOP despues de la ultima nota
                     y con alguna nota en los ultimos 4 compases.
  FOTO DEL MUNDO     en cada compas, la forma de cada celda: especie,
                     ocupacion (recortada donde la forma deja de cambiar),
                     hibrida, satelite y huella.
  NOVEDAD            celdas cuya forma ha cambiado / celdas vivas.
  MADUREZ            formaciones que han llegado al limite / formaciones.
  CIERRE             maduro y quieto Compasesquietos compases seguidos
                     (estancado); Ciclomax compases, pero solo si el
                     territorio esta ocupado (edad maxima, v4); una
                     rafaga de All Notes Off con Cambioentierra (cambio de
                     pattern) o Forzarciclo. Nunca antes de Ciclomin,
                     salvo Forzarciclo.
  TERRITORIO (v4)    las celdas que han tocado las notas del SEQ1 y del
                     SEQ2 en los ultimos Compasesterritorio compases (8),
                     mas sus vecinas (hasta donde llegan los desbordes).
                     La edad maxima solo entierra si al menos
                     Umbralterritorio (80 %) de ese territorio esta
                     ocupado. Sin tope de seguridad: mientras la bateria
                     deshaga mas de lo que se construye, el mundo sigue.
  GIRO VIVO          el planeta se frena a medida que el mundo deja de
                     cambiar y vuelve a acelerar con la novedad.
  TABLA ciclos       una fila por ciclo cerrado: para afinar los umbrales.

Barsperturn vuelve a ser manual.

PRUEBA PENDIENTE CON EL APARATO
-------------------------------
Cambia de pattern dos veces y pulsa STOP, mirando el Textport. Cada
rafaga de All Notes Off sale como
    AVISO  All Notes Off sin STOP: cambio de pattern
    AVISO  All Notes Off junto a un STOP
Si el BeatStep no la envia, Cambioentierra no hace nada.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase6_ciclo.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase6 v5  (eras mas largas: Ciclomin 16, Compasesquietos 3)'
banner(VERSION)

base = require_base(6)
motor = install_core(base, CARPETA, 6)

OBSOLETOS = ['Repsporciclo', 'Modociclo', 'Turnauto', 'Longmanual', 'Longfija', 'Longmin',
             'Pasosporcompas', 'Pasospornegra', 'Resetpatterns']
quitados = [n for n in OBSOLETOS if remove_par(base, n)]
if quitados:
    ok('quitados de la pagina Fase6: %s (Barsperturn queda como estaba)' % ', '.join(quitados))

page = get_page(base, 'Fase6')
add_par(base, page, 'float', 'Umbralmadurez', 'Madurez minima para enterrar', 0.6, 0.0, 1.0)
add_par(base, page, 'float', 'Umbralnovedad', 'Novedad maxima de un compas quieto', 0.15, 0.0, 1.0)
add_par(base, page, 'int', 'Compasesquietos', 'Compases quietos para enterrar', 3, 1, 64, clamp=True)
renew_default(base, 'Umbralnovedad', 0.05, 0.15)
renew_default(base, 'Compasesquietos', 4, 3)
add_par(base, page, 'int', 'Ciclomin', 'Duracion minima (compases)', 16, 1, 256, clamp=True)
add_par(base, page, 'int', 'Ciclomax', 'Edad maxima (si el territorio esta lleno)', 64, 1, 1024,
        clamp=True)
renew_default(base, 'Ciclomax', 32, 64)
try:
    base.par.Ciclomax.label = 'Edad maxima (si el territorio esta lleno)'
except Exception:
    pass
add_par(base, page, 'float', 'Umbralterritorio', 'Territorio ocupado para la edad maxima', 0.8,
        0.0, 1.0)
add_par(base, page, 'int', 'Compasesterritorio', 'Compases de memoria del territorio', 8, 1, 64,
        clamp=True)
add_par(base, page, 'int', 'Negrasporcompas', 'Negras por compas', 4, 1, 16, clamp=True)
add_par(base, page, 'toggle', 'Cambioentierra', 'Cambio de pattern entierra el mundo', False)
add_par(base, page, 'toggle', 'Girovivo', 'El giro se frena sin novedad', True)
add_par(base, page, 'float', 'Giromin', 'Factor de giro minimo', 0.25, 0.0, 1.0)
add_par(base, page, 'pulse', 'Forzarciclo', 'Terminar el ciclo ahora')
ok('pagina Fase6: Umbralmadurez, Umbralnovedad, Compasesquietos, Ciclomin, Ciclomax, '
   'Umbralterritorio, Compasesterritorio, '
   'Negrasporcompas, Cambioentierra, Girovivo, Giromin, Forzarciclo')
try:
    if int(base.par.Ciclomax) < int(base.par.Ciclomin):
        info('Ciclomax (%d) < Ciclomin (%d): se usa Ciclomax = Ciclomin'
             % (int(base.par.Ciclomax), int(base.par.Ciclomin)))
except Exception:
    pass

ciclos = get_or_make(base, 'tableDAT', 'ciclos', -440, 60)
if ciclos.numRows == 0 or ciclos[0, 0] is None or ciclos[0, 0].val != 'ciclo':
    ciclos.clear()
    ciclos.appendRow(motor.module.CICLOS_COLS)
else:                               # columnas nuevas (territorio), conservando las filas
    cab = [ciclos[0, k].val for k in range(ciclos.numCols)]
    faltan = [k for k in motor.module.CICLOS_COLS if k not in cab]
    if faltan:
        filas = [[ciclos[r, k].val if ciclos[r, k] is not None else ''
                  for k in range(ciclos.numCols)] for r in range(1, ciclos.numRows)]
        ciclos.clear()
        ciclos.appendRow(cab + faltan)
        for f in filas:
            ciclos.appendRow(f + [''] * len(faltan))
        ok('tabla ciclos: columna nueva %s' % ', '.join(faltan))
ok('tabla ciclos: una fila por ciclo cerrado (ultimas 200)')

leeme(base, 6, """FASE 6 - EL CICLO LO CIERRA EL MUNDO
  En cada compas el motor mira la forma de cada celda:
    novedad = celdas que han cambiado / celdas vivas
    madurez = formaciones en el limite / formaciones
  El mundo se entierra cuando lleva Compasesquietos compases maduro
  (Umbralmadurez) y quieto (Umbralnovedad), a partir de Ciclomin.
  Territorio = celdas tocadas por SEQ1/SEQ2 en los ultimos
  Compasesterritorio compases y sus vecinas. Pasado Ciclomax solo se
  entierra si el territorio esta ocupado (Umbralterritorio); si no, la
  leyenda dice 'esperando territorio' y el mundo sigue (sin tope).
  Cambioentierra: una rafaga de All Notes Off sin STOP tambien entierra.
  Girovivo: el planeta se frena cuando el mundo deja de cambiar.
  Tabla ciclos: compases, motivo, madurez, novedad, grosor y territorio.""")

print_report()


def prueba(t):
    m = t.m
    c = dict(m.cfg())
    c['nivel'] = 6                     # el ciclo, sin enterrar (eso es la fase 8)
    cmin, cmax = m.cycle_bounds(c)
    bar = m.bar_dur(c, 120.0)
    fps = 30.0

    def tocar(W, nbars, notas_por_compas):
        """Simula compases a 120 BPM, fotograma a fotograma, por el motor.
        notas_por_compas(k) -> notas del compas k. Devuelve los cierres."""
        fins = []
        tt = W.get('_t', 0.0)
        fpb = int(round(bar * fps))
        for k in range(nbars):
            notas = notas_por_compas(k)
            cada = fpb // max(1, len(notas))
            for f in range(fpb):
                now = tt + f / fps
                if notas and f % cada == 0 and f // cada < len(notas):
                    m.note_on(W, c, m.GEO, notas[f // cada], 100, now, 120.0)
                r = m.tick(W, c, now, 120.0, True)
                if r['ciclo']:
                    fins.append(r['ciclo'])
            tt += bar
        W['_t'] = tt
        return fins

    # 1. estancado: una formacion saturada, rodeada de sus satelites saturados
    W = m.new_world()
    i = m.note_cell(64)
    for j in [i] + list(m.NEIGH[i]):
        W['occ'][j], W['own'][j], W['sp'][j] = 30, m.GEO, m.GEO
        W['h'][j] = m.limit(c)
        W['par'][j] = -1 if j == i else i
    fins = tocar(W, cmax, lambda k: [64, 64, 64, 64])
    esperado = max(cmin, 1 + int(c['compases_quietos']))
    t.check('coronada que sigue sonando -> novedad 0', W['novedad'] == 0.0 or
            (fins and fins[0]['novedad'] == 0.0))
    t.check('cierre por estancado en el compas %d' % esperado,
            fins and fins[0]['motivo'] == 'estancado' and fins[0]['compases'] == esperado,
            str([(f['motivo'], f['compases']) for f in fins[:2]]))
    # 2. edad maxima con el territorio ocupado: se entierra en Ciclomax
    notas = [m.cell_note(x) for x in range(m.N)]

    def llenar(Wx):
        for x in range(m.N):
            if Wx['occ'][x] == 0:
                Wx['occ'][x], Wx['own'][x], Wx['sp'][x] = 1, m.GEO, m.GEO
                Wx['h'][x] = c['seed_frac'] * m.limit(c)
    W = m.new_world()
    llenar(W)
    fins = tocar(W, cmax + 1, lambda k: [notas[(k * 7) % m.N]])
    t.check('territorio ocupado: un cambio en cada compas -> edad maxima en %d' % cmax,
            fins and fins[0]['motivo'] == 'edad maxima' and fins[0]['compases'] == cmax
            and fins[0]['territorio'] >= c['umbral_territorio'],
            str([(f['motivo'], f['compases']) for f in fins[:2]]))
    # 2b. territorio por debajo del umbral (algo lo vacia en cada compas, como
    #     la erosion del drum): no se entierra hasta que se llena
    W = m.new_world()
    fins = []
    for k in range(cmax + 10):
        fins += tocar(W, 1, lambda kk, k=k: [notas[(k * 7) % m.N]])
        for x in range(m.N):
            if x != m.note_cell(notas[(k * 7) % m.N]):
                W['occ'][x], W['own'][x], W['sp'][x], W['h'][x] = 0, 0, 0, 0.0
                W['par'][x] = -1
    sigue = not fins and W['esperando'] and W['territorio'] < c['umbral_territorio']
    llenar(W)
    fins = tocar(W, 1, lambda k: [notas[(k * 11) % m.N]])
    t.check('territorio sin ocupar: pasada la edad maxima el mundo sigue; se entierra '
            'en cuanto se ocupa', sigue and fins and fins[0]['motivo'] == 'edad maxima'
            and fins[0]['compases'] == cmax + 10,
            str([(f['motivo'], f['compases']) for f in fins[:1]]))
    t.check('leyenda: esperando territorio', 'territorio' in m.legend())
    # 2c. el territorio: la celda tocada y sus vecinas, durante Compasesterritorio
    W = m.new_world()
    a = m.note_cell(64)
    W['bar_n'], W['terr'] = 10, {a: 10}
    dentro = m.territory_cells(W, c) == set([a] + list(m.NEIGH[a]))
    W['bar_n'] = 10 + int(c['compases_territorio'])
    t.check('territorio: la celda tocada y sus vecinas; deja de contar a los '
            'Compasesterritorio compases', dentro and not m.territory_cells(W, c))
    # 3. parado: sin notas el reloj no avanza
    W = m.new_world()
    fins = tocar(W, cmax + 2, lambda k: [])
    t.check('sin notas el reloj del ciclo no avanza', not fins and W['compases_ciclo'] == 0)
    # 4. cambio de pattern con Cambioentierra: se aplaza hasta Ciclomin
    c['cambio_entierra'] = 1
    W = m.new_world()
    tocar(W, 1, lambda k: [notas[k % m.N]])
    for ch in range(1, 17):
        m.on_cc(W, c, ch, 123, 0, W['_t'])
    fins = tocar(W, cmax, lambda k: [notas[(k * 7) % m.N]])
    t.check('rafaga antes de Ciclomin -> cierra en Ciclomin por cambio de pattern',
            fins and fins[0]['motivo'] == 'cambio de pattern' and fins[0]['compases'] == cmin,
            str([(f['motivo'], f['compases']) for f in fins[:1]]))
    c['cambio_entierra'] = 0
    # 5. giro vivo acotado
    W = m.new_world()
    W['novedad'] = 0.0
    for k in range(400):
        m.giro_step(W, c, 0.05, 120.0)
    lo = W['giro_factor']
    W['novedad'] = 1.0
    for k in range(400):
        m.giro_step(W, c, 0.05, 120.0)
    t.check('giro vivo entre Giromin y 1',
            abs(lo - c['giro_min']) < 1e-3 and abs(W['giro_factor'] - 1.0) < 1e-3,
            'x%.2f .. x%.2f' % (lo, W['giro_factor']))
    t.check('ritmo multiplica el giro por el giro vivo',
            'giro_factor()' in base.op('ritmo').text)
    # 6. por el camino real: Forzarciclo, START y CC 123
    tabla = base.op('ciclos')
    filas = [[cell.val for cell in tabla.row(r)] for r in range(tabla.numRows)]
    m.reset_world()
    n0 = m.world()['ciclo_n']
    m.on_pulse('Forzarciclo')
    W = m.world()
    t.check('Forzarciclo cierra al instante (forzado)',
            W['ciclo_n'] == n0 + 1 and W['ev']['fin_de_ciclo']['motivo'] == 'forzado')
    t.check('tabla ciclos: fila nueva', tabla.numRows == len(filas) + 1
            and tabla[tabla.numRows - 1, 'motivo'].val == 'forzado')
    t.midi(0xFA)
    t.check('START por MIDI llega al motor', m.world()['clock']['start_t'] > -99.0)
    t.midi(0xBC, 0x7B, 0x00)
    t.check('CC 123 por MIDI llega al detector', len(m.world()['burst']['times']) == 1)
    t.check('leyenda CICLO', 'CICLO' in m.legend() and 'madurez' in m.legend())


run_test(base, prueba)
print('  Ahora: PLAY con los dos SEQ. La linea CICLO cuenta compases, madurez')
print('  y novedad. Sin bateria, el mundo madura, se queda quieto, el planeta')
print('  frena y el ciclo se cierra por "estancado". Con bateria constante,')
print('  los ciclos llegan a "edad maxima". Mira la tabla ciclos.')
print('  PRUEBA PENDIENTE: cambia de pattern dos veces y pulsa STOP; copia')
print('  las lineas AVISO que salgan aqui.')
print('=' * 66)
