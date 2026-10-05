"""
=============================================================================
ESTRATOS - FASE 6: EL CICLO (PATTERNS Y LONGITUD DE LA VUELTA)
=============================================================================
Requiere la fase 5. Rehace sobre la base nueva el trabajo aparcado
(fase2f ... fase2j).

QUE HACE
--------
  LONGITUD DEL PATTERN  la deduce escuchando: busca el periodo mas corto
                        con el que se repiten las notas. Tolera la
                        probabilidad: solo compara pasos que han sonado.
  BIBLIOTECA            guarda la huella de cada pattern; al volver a uno
                        conocido lo reconoce en unas tres notas.
  CAMBIO DE PATTERN     lo detecta (a) por la rafaga de All Notes Off que
                        no acompana a un STOP, o (b) porque las notas
                        dejan de encajar con el pattern conocido.
  CICLO DE ECOSISTEMA   Repsporciclo repeticiones del pattern mas largo
                        (o, con Modociclo = hiperperiodo, el minimo comun
                        multiplo de los dos: 16 y 13 -> 208 pasos).
  UNA VUELTA POR CICLO  con Turnauto, Barsperturn se calcula sola: el dia
                        del planeta dura lo que dura un mundo.

EL PASO DE CADA NOTA
--------------------
La longitud no viaja por MIDI y FASE1 no lee el reloj (lo hace
midicontrolx). El paso de cada nota se deduce del tempo del proyecto: se
reancla en cada nota, asi el error no se acumula. START (o MMC play) pone
el paso a 0. Si el BeatStep no usa semicorcheas, ajusta Pasospornegra.

PRUEBA PENDIENTE CON EL APARATO
-------------------------------
Cambia de pattern dos veces y pulsa STOP, mirando el Textport. Cada
rafaga de All Notes Off sale como
    AVISO  All Notes Off sin STOP: cambio de pattern
    AVISO  All Notes Off junto a un STOP
Asi sabremos cuando la envia el BeatStep.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase6_ciclo.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase6 v1  (longitud de pattern, biblioteca, ciclo, vuelta por ciclo)'
banner(VERSION)

base = require_base(6)
motor = install_core(base, CARPETA, 6)

page = get_page(base, 'Fase6')
add_par(base, page, 'int', 'Repsporciclo', 'Repeticiones por ciclo', 8, 1, 64, clamp=True)
add_par(base, page, 'menu', 'Modociclo', 'Ciclo de ecosistema', 'repeticiones',
        menu=['repeticiones', 'hiperperiodo'],
        menu_labels=['Repeticiones del mas largo', 'Hiperperiodo (mcm)'])
add_par(base, page, 'toggle', 'Turnauto', 'Una vuelta por ciclo', True)
add_par(base, page, 'int', 'Longmanual', 'Longitud si no se detecta', 16, 1, 64, clamp=True)
add_par(base, page, 'toggle', 'Longfija', 'Usar siempre la longitud manual', False)
add_par(base, page, 'int', 'Longmin', 'Longitud minima a detectar', 4, 1, 32, clamp=True)
add_par(base, page, 'int', 'Pasosporcompas', 'Pasos por compas', 16, 1, 64, clamp=True)
add_par(base, page, 'int', 'Pasospornegra', 'Pasos por negra', 4, 1, 8, clamp=True)
add_par(base, page, 'pulse', 'Forzarciclo', 'Terminar el ciclo ahora')
add_par(base, page, 'pulse', 'Resetpatterns', 'Olvidar patterns')
ok('pagina Fase6: Repsporciclo, Modociclo, Turnauto, Longmanual, Longfija, '
   'Longmin, Pasosporcompas, Pasospornegra, Forzarciclo, Resetpatterns')

leeme(base, 6, """FASE 6 - EL CICLO
  La longitud de cada pattern se deduce escuchando las notas; la
  biblioteca reconoce patterns ya vistos en ~3 notas.
  Cambio de pattern: rafaga All Notes Off sin STOP, o notas que no encajan.
  Ciclo = Repsporciclo x pattern mas largo (o hiperperiodo).
  Turnauto: Barsperturn = pasos del ciclo / Pasosporcompas.""")

print_report()


def prueba(t):
    m = t.m
    c = m.cfg()
    c['long_fija'] = 0
    W = m.new_world()
    p16 = [60, 62, 63, 67, 60, 70, 65, 64, 60, 62, 72, 67, 61, 70, 65, 66]
    p13 = [48, 50, 55, 53, 48, 57, 52, 50, 59, 55, 49, 54, 51]
    sd = 60.0 / 120.0 / 4
    tt = 0.0
    ends = 0
    for k in range(16 * 10):
        m.note_on(W, c, 1, p16[k % 16], 100, tt, 120.0)
        m.note_on(W, c, 2, p13[k % 13], 100, tt + 0.002, 120.0)
        r = m.tick(W, c, tt + 0.06, 120.0, True)
        ends += r['ciclo']
        tt += sd
    t.check('SEQ1: pattern de 16 pasos', W['det'][1]['L'] == 16, str(W['det'][1]['L']))
    t.check('SEQ2: pattern de 13 pasos', W['det'][2]['L'] == 13, str(W['det'][2]['L']))
    t.check('ciclo = %d x 16 pasos' % c['reps'], W['cycle']['steps'] == c['reps'] * 16,
            str(W['cycle']['steps']))
    c2 = dict(c)
    c2['cycle_mode'] = 1
    t.check('hiperperiodo 16 y 13 = 208 pasos', m.cycle_lengths(W, c2)[0] == 208)
    t.check('ciclos terminados al tocar', ends >= 1, '%d' % ends)
    # probabilidad al 60 %
    import random
    rnd = random.Random(3)
    W2 = m.new_world()
    tt = 0.0
    for k in range(16 * 10):
        if rnd.random() < 0.6:
            m.note_on(W2, c, 1, p16[k % 16], 100, tt + rnd.uniform(-0.004, 0.004), 120.0)
        tt += sd
    t.check('con probabilidad 60 %: 16 pasos', W2['det'][1]['L'] == 16, str(W2['det'][1]['L']))
    # biblioteca
    m.pattern_change(W2, c, 1, None, 'prueba')
    for k in range(4):
        m.note_on(W2, c, 1, p16[(k + 5) % 16], 100, tt, 120.0)
        tt += sd
    t.check('pattern conocido reconocido por la biblioteca',
            W2['det'][1]['L'] == 16 and W2['det'][1]['src'] == 'biblioteca')
    # rafagas
    W3 = m.new_world()
    W3['det'][1]['L'] = 16
    for ch in range(1, 17):
        m.on_cc(W3, c, ch, 123, 0, 10.0)
    r = m.tick(W3, c, 10.5, 120.0, True)
    t.check('All Notes Off sin STOP -> cambio de pattern', r['burst'] == 'cambio')
    W3['det'][1]['L'] = 16
    m.clock_stop(W3, 20.0)
    for ch in range(1, 17):
        m.on_cc(W3, c, ch, 123, 0, 20.02)
    r = m.tick(W3, c, 20.5, 120.0, True)
    t.check('All Notes Off con STOP -> no cambia nada',
            r['burst'] == 'stop' and W3['det'][1]['L'] == 16)
    # MIDI real: START y CC 123 llegan al motor
    m.reset_world()
    t.midi(0xFA)
    t.check('START por MIDI -> paso 0', m.world()['clock']['t_ref'] is not None)
    t.midi(0xBC, 0x7B, 0x00)
    t.check('CC 123 por MIDI llega al detector', len(m.world()['burst']['times']) == 1)
    t.check('leyenda CICLO', 'CICLO' in m.legend())


run_test(base, prueba)
print('  Ahora: PLAY con los dos SEQ. La linea CICLO pasa de "escuchando" a')
print('  "16 pasos (escucha)" tras unas dos vueltas del pattern.')
print('  Con Turnauto, el planeta da una vuelta por ciclo.')
print('  PRUEBA PENDIENTE: cambia de pattern dos veces y pulsa STOP; copia')
print('  las lineas AVISO que salgan aqui.')
print('=' * 66)
