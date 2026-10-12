"""
=============================================================================
ESTRATOS - FASE 5: DOS ESPECIES (SEQ2 Y LA ARQUITECTURA)
=============================================================================
Requiere la fase 4.

QUE HACE
--------
El SEQ2 entra como segundo generador, con su propia logica de forma:

  GEOLOGIA (SEQ1)      agujas minerales oblicuas, en racimo, desiguales
  ARQUITECTURA (SEQ2)  torres ortogonales de plantas apiladas

Cuando una especie cae sobre una celda de la otra, la COLONIZA y la celda
pasa a HIBRIDA, conservando ambos rastros:
  - geologia colonizada   -> macizo aterrazado (plantas rectas en la ladera)
  - arquitectura colonizada -> torre mineralizada (excrecencias en los flancos)

El SEQ2 no tiene baliza (v2): cada nota suya enciende el CENTRO de su
celda en ambar, con pulso y tenue hasta la siguiente. Si el SEQ1 y el
SEQ2 estan en la misma celda, el centro se parte en dos mitades: SEQ1 al
oeste, SEQ2 al este.

EL CANAL DEL SEQ2
-----------------
Por defecto 14 (el SEQ1 esta en el 13). Si las notas del SEQ2 salen en el
Textport como "ignorado: canal X", pon X en Canal2 (pagina Fase5).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase5_especies.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase5 v2  (SEQ2 arquitectura, hibridos, luz ambar en el centro de la celda)'
banner(VERSION)

base = require_base(5)
motor = install_core(base, CARPETA, 5)

page = get_page(base, 'Fase5')
add_par(base, page, 'int', 'Canal2', 'Canal MIDI del SEQ2', 14, 1, 16, clamp=True)
add_par(base, page, 'int', 'Nota2', 'Nota de prueba del SEQ2', 60, 0, 127, clamp=True)
add_par(base, page, 'pulse', 'Sembrar2', 'Sembrar SEQ2 en Nota2 (prueba)')
ok('pagina Fase5: Canal2 (14), Nota2, Sembrar2')

set_render(base)

leeme(base, 5, """FASE 5 - DOS ESPECIES
  SEQ1 (Canal) construye geologia; SEQ2 (Canal2) construye arquitectura.
  Una especie sobre la otra la coloniza: celda hibrida.
  Centro de la celda en ambar = SEQ2 (con el SEQ1, partido en dos).
  Prueba: Nota2 + Sembrar2.""")

print_report()


def prueba(t):
    m = t.m
    m.reset_world()
    c = m.cfg()
    ch2 = int(base.par.Canal2)
    st2 = 0x90 + ch2 - 1
    t.midi(0x9C, 0x3C, 0x1E)                         # SEQ1 do4 vel 30
    t.midi(st2, 0x3C, 0x64)                          # SEQ2 do4
    t.midi(st2, 0x32, 0x64)                          # SEQ2 re3
    W = m.world()
    i, j = m.note_cell(60), m.note_cell(50)
    t.check('SEQ2 sobre geologia -> hibrida', W['sp'][i] == m.HIB and W['own'][i] == m.GEO)
    t.check('el material lo sigue fijando el fundador', W['vel'][i] == 30)
    t.check('SEQ2 en celda vacia -> arquitectura', W['own'][j] == m.ARQ)
    # luz de celda: el SEQ2 en ambar; con el SEQ1 en la misma celda, los dos
    W2 = m.new_world()
    c2 = dict(c)
    c2['nivel'] = max(5, c2['nivel'])
    m.note_on(W2, c2, m.ARQ, 50, 100, 1.0)
    filas = m.cell_lights(W2, c2, 1.0)
    t.check('nota del SEQ2: el centro de su celda en ambar',
            len(filas) == 1 and tuple(round(x, 3) for x in filas[0][9:12])
            == tuple(round(x, 3) for x in m.COL_SEQ2))
    m.note_on(W2, c2, m.GEO, 50, 100, 1.0)
    filas = m.cell_lights(W2, c2, 1.0)
    cols = set(tuple(round(x, 3) for x in f[9:12]) for f in filas)
    t.check('SEQ1 y SEQ2 en la misma celda: se ven los dos (centro partido)',
            len(filas) == 2 and len(cols) == 2)
    t.check('sin baliza del SEQ2', base.op('baliza2') is None and base.op('i_baliza2') is None)
    t.check('leyenda SEQ2', 'SEQ2' in m.legend())


run_test(base, prueba)
print('  Ahora: PLAY con SEQ1 y SEQ2 sonando. Prueba longitudes distintas')
print('  (16 y 13): los hibridos aparecen donde los dos se cruzan.')
print('  Si el SEQ2 sale como "ignorado: canal X", pon X en Canal2.')
print('=' * 66)
