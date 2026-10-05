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

El SEQ2 tiene su propia baliza, ambar y mas pequena.

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

VERSION = 'fase5 v1  (SEQ2 arquitectura, hibridos, segunda baliza)'
banner(VERSION)

base = require_base(5)
motor = install_core(base, CARPETA, 5)

page = get_page(base, 'Fase5')
add_par(base, page, 'int', 'Canal2', 'Canal MIDI del SEQ2', 14, 1, 16, clamp=True)
add_par(base, page, 'int', 'Nota2', 'Nota de prueba del SEQ2', 60, 0, 127, clamp=True)
add_par(base, page, 'pulse', 'Sembrar2', 'Sembrar SEQ2 en Nota2 (prueba)')
ok('pagina Fase5: Canal2 (14), Nota2, Sembrar2')

make_constant(base, 'mat_baliza2', 780, 540, (1.0, 0.62, 0.25))
make_instanced(base, 'baliza2', 520, 540, 'mat_baliza2', sop='sphere')
set_render(base)

leeme(base, 5, """FASE 5 - DOS ESPECIES
  SEQ1 (Canal) construye geologia; SEQ2 (Canal2) construye arquitectura.
  Una especie sobre la otra la coloniza: celda hibrida.
  Baliza ambar = SEQ2. Prueba: Nota2 + Sembrar2.""")

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
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, 0.0)
    b2 = base.op('i_baliza2')
    b2.cook(force=True)
    t.check('baliza del SEQ2 colocada', b2.numSamples == 1 and float(b2['ty'][0]) > -100)
    t.check('leyenda SEQ2', 'SEQ2' in m.legend())


run_test(base, prueba)
print('  Ahora: PLAY con SEQ1 y SEQ2 sonando. Prueba longitudes distintas')
print('  (16 y 13): los hibridos aparecen donde los dos se cruzan.')
print('  Si el SEQ2 sale como "ignorado: canal X", pon X en Canal2.')
print('=' * 66)
