"""
=============================================================================
ESTRATOS - FASE 7: EROSION SUPERFICIAL Y PRESUPUESTO DE DENSIDAD
=============================================================================
Requiere la fase 6.

QUE HACE
--------
Las 8 pistas de bateria del BeatStep son las 8 senales de destruccion.
Cada pad tiene un PERFIL (tabla perfiles_erosion, editable):

    reduccion     1-3  unidades de ocupacion que quita
    radio         0-2  anillos de vecinas afectadas
    profundidad   0-4  conchas que atraviesa (se activa en la fase 9)

La erosion degrada en ORDEN INVERSO al crecimiento: primero caen los
satelites, luego la altura, y al final queda la HUELLA (una mancha oscura
que dura hasta que la celda se vuelve a sembrar o se entierra).

PRESUPUESTO DE DENSIDAD: si mas del 60 % de las celdas esta ocupado, el
radio de todos los eventos se duplica (un radio 0 pasa a 1) hasta volver
por debajo del umbral. La escena se aligera cuando pesa.

DONDE CAE LA EROSION (decision tomada)
--------------------------------------
Los pads de bateria no tienen altura, asi que no dicen celda. Objetivo:
  alterna   (defecto) pads impares donde esta el SEQ1, pares donde el SEQ2
  seq1/seq2 siempre donde esta ese secuenciador
  velocidad la velocidad del golpe elige una de las 96 celdas
En los tres primeros, la velocidad desplaza el golpe un meridiano a un
lado o al otro: decide el aparato, no el software.

EL CANAL DE LA BATERIA
----------------------
Por defecto 10, pads desde la nota 36 (do2). Si salen como "ignorado:
canal X" o "pad fuera de 1-8", ajusta Canaldrum y Notabase.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase7_erosion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase7 v1  (8 pads de erosion, huellas, presupuesto de densidad)'
banner(VERSION)

base = require_base(7)
motor = install_core(base, CARPETA, 7)

page = get_page(base, 'Fase7')
add_par(base, page, 'int', 'Canaldrum', 'Canal MIDI de la bateria', 10, 1, 16, clamp=True)
add_par(base, page, 'int', 'Notabase', 'Nota del pad 1', 36, 0, 120, clamp=True)
add_par(base, page, 'menu', 'Objetivo', 'Donde cae la erosion', 'alterna',
        menu=['seq1', 'seq2', 'alterna', 'velocidad'],
        menu_labels=['Donde esta el SEQ1', 'Donde esta el SEQ2',
                     'Alterna SEQ1 / SEQ2', 'La velocidad elige celda'])
add_par(base, page, 'float', 'Umbraldensidad', 'Presupuesto de densidad', 0.60, 0.1, 1.0)
add_par(base, page, 'float', 'Multradio', 'Multiplicador de radio', 2.0, 1.0, 4.0)
add_par(base, page, 'int', 'Padprueba', 'Pad de prueba', 1, 1, 8, clamp=True)
add_par(base, page, 'pulse', 'Erosionar', 'Erosionar con el pad de prueba')
ok('pagina Fase7: Canaldrum (10), Notabase (36), Objetivo, Umbraldensidad, '
   'Multradio, Padprueba, Erosionar')

tabla = base.op('perfiles_erosion')
if tabla is None:
    tabla = mk(base, 'tableDAT', 'perfiles_erosion', -660, 80)
    tabla.clear()
    tabla.appendRow(['pad', 'reduccion', 'radio', 'profundidad', 'tipo'])
    tipos = ['aranazo', 'aranazo', 'aranazo', 'aranazo', 'aranazo',
             'corte', 'corte', 'corte profundo']
    perf = motor.module.PERFILES_DEFECTO
    for k in range(8):
        red, rad, prof = perf[k]
        tabla.appendRow([k + 1, red, rad, prof, tipos[k]])
    ok('perfiles_erosion: 8 pads (5 aranazos, 3 cortes). Editala a mano')
else:
    info('perfiles_erosion ya existia: se conserva como esta')

leeme(base, 7, """FASE 7 - EROSION
  8 pads de bateria (Canaldrum, desde Notabase) = 8 perfiles editables en
  perfiles_erosion: reduccion, radio, profundidad.
  Orden de caida: satelites, altura, huella.
  Presupuesto: por encima de Umbraldensidad, radios x Multradio.
  Prueba: Padprueba + Erosionar.""")

print_report()


def prueba(t):
    m = t.m
    m.reset_world()
    c = m.cfg()
    for k in range(7):
        t.midi(0x9C, 0x40, 0x64)
    W = m.world()
    i = m.note_cell(64)
    sats0 = sum(W['occ'][j] for j in m.satellites_of(W, i))
    occ0 = W['occ'][i]
    c['perfiles'] = [(1, 0, 0)] * 8
    c['target_mode'] = 0
    m.erosion(W, c, 0, 1, 0.0)                    # velocidad 1: sin desplazar
    sats1 = sum(W['occ'][j] for j in m.satellites_of(W, i))
    t.check('la erosion quita primero satelites', sats1 == sats0 - 1 and W['occ'][i] == occ0,
            'satelites %d -> %d' % (sats0, sats1))
    for k in range(20):
        m.erosion(W, c, 0, 1, 0.0)
    t.check('... y al final deja la huella', W['occ'][i] == 0 and W['huella'][i] > 0)
    W2 = m.new_world()
    for n in range(96):
        m.note_on(W2, c, 1, n, 100, 0.0)
    ev = m.erosion(W2, c, 0, 100, 0.0)
    t.check('presupuesto: con el mundo lleno el radio se duplica', ev['doble'] and ev['rad'] >= 1)
    # el MIDI de bateria llega al motor
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    t.midi(0x9C, 0x40, 0x64)
    chd = int(base.par.Canaldrum)
    nb = int(base.par.Notabase)
    t.midi(0x90 + chd - 1, nb, 0x64)
    W = m.world()
    t.check('pad 1 por MIDI -> erosion', W['hits'].get(3, 0) == 1 and 'erosion' in W['ev'])
    t.check('perfiles leidos de la tabla', len(m.cfg()['perfiles']) == 8)
    t.check('leyenda EROSION', 'EROSION' in m.legend())


run_test(base, prueba)
print('  Ahora: anade la bateria del BeatStep. Cada golpe aligera el paisaje.')
print('  Si los golpes salen como "ignorado", ajusta Canaldrum y Notabase.')
print('  Ajusta el equilibrio crecimiento / erosion antes de pasar a la fase 8.')
print('=' * 66)
