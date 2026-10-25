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

LOS PARAMETROS DEL SEQ2 (pagina Fase2, debajo de los del SEQ1)
--------------------------------------------------------------
v3: los mismos tres que el SEQ1. v4: la pagina Fase5 desaparece; los
parametros viven en la pagina Fase2 (los de un proyecto anterior se mueven
conservando su valor).

  Canal2    Canal MIDI del SEQ2. Por defecto 14 (el SEQ1 esta en el 13).
  Filtrar2  Solo ese canal. Encendido: solo cuenta el canal de Canal2. Apagado:
            cualquier canal cuenta como SEQ2, menos el del SEQ1 (Canal, si
            Filtrar esta encendido) y el de la bateria (Canaldrum, fase 7).
  Nota2     Ultima nota del SEQ2. Cada nota que llega la actualiza; tambien se
            puede mover a mano y es la que siembra Sembrar2.

Si las notas del SEQ2 salen en el Textport como "ignorado: canal X", pon X en
Canal2 (pagina Fase2) o apaga Filtrar2.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase5_especies.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase5 v4  (SEQ2 en la pagina Fase2 con el SEQ1; arquitectura, hibridos, luz ambar)'
banner(VERSION)

base = require_base(5)
motor = install_core(base, CARPETA, 5)

PARS_SEQ2 = ('Canal2', 'Filtrar2', 'Nota2', 'Sembrar2')
page = get_page(base, 'Fase2')

# Proyecto anterior a la v4: los parametros estaban en la pagina Fase5. Se
# quitan de ahi y se recrean en la Fase2 con el valor que tenian.
guardados = {}
for nm in PARS_SEQ2:
    try:
        p = getattr(base.par, nm, None)
        if p is not None and p.page is not None and p.page.name != 'Fase2':
            if nm != 'Sembrar2':                     # el pulso no guarda valor
                guardados[nm] = p.eval()
            p.destroy()
    except Exception as e:
        info('no pude mover %s a la pagina Fase2: %s' % (nm, e))

add_par(base, page, 'int', 'Canal2', 'Canal MIDI del SEQ2', 14, 1, 16, clamp=True)
add_par(base, page, 'toggle', 'Filtrar2', 'Solo ese canal (SEQ2)', True)
add_par(base, page, 'int', 'Nota2', 'Ultima nota SEQ2 (muevela para probar)', 60, 0, 127, clamp=True)
add_par(base, page, 'pulse', 'Sembrar2', 'Sembrar SEQ2 en Nota2 (prueba)')
for nm, valor in guardados.items():
    try:
        setattr(base.par, nm, valor)
    except Exception as e:
        info('no pude devolver a %s su valor %r: %s' % (nm, valor, e))

# add_par no toca lo que ya existe, y con dos secuenciadores en la misma
# pagina las etiquetas tienen que decir de cual son.
for nm, etiqueta in (('Filtrar', 'Solo ese canal (SEQ1)'),
                     ('Nota', 'Ultima nota SEQ1 (muevela para probar)'),
                     ('Nota2', 'Ultima nota SEQ2 (muevela para probar)')):
    try:
        getattr(base.par, nm).label = etiqueta
    except Exception:
        pass

# La pagina Fase5 se queda vacia: fuera.
try:
    if not any(p.page is not None and p.page.name == 'Fase5' for p in base.customPars):
        for pg in list(base.customPages):
            if pg.name == 'Fase5':
                pg.destroy()
except Exception as e:
    info('no pude quitar la pagina Fase5 (vacia): %s' % e)
ok('pagina Fase2: Canal (13), Filtrar, Nota del SEQ1 y Canal2 (14), Filtrar2, Nota2, Sembrar2 del SEQ2')

set_render(base)

leeme(base, 5, """FASE 5 - DOS ESPECIES
  SEQ1 (Canal) construye geologia; SEQ2 (Canal2) construye arquitectura.
  Una especie sobre la otra la coloniza: celda hibrida.
  Centro de la celda en ambar = SEQ2 (con el SEQ1, partido en dos).
  Canal2 / Filtrar2 / Nota2 = Canal / Filtrar / Nota del SEQ1, en la misma
  pagina (Fase2).
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
    # Nota2 y Filtrar2, como Nota y Filtrar del SEQ1
    t.check('Nota2 guarda la ultima nota del SEQ2', int(base.par.Nota2) == 0x32)
    t.check('los parametros del SEQ2 estan en la pagina Fase2, con los del SEQ1',
            all(getattr(base.par, nm).page.name == 'Fase2' for nm in PARS_SEQ2 + ('Canal', 'Filtrar', 'Nota')))
    t.check('la pagina Fase5 ya no existe', all(pg.name != 'Fase5' for pg in base.customPages))
    drum = int(base.par.Canaldrum) if has_par(base, 'Canaldrum') else 16
    libre = next(k for k in range(1, 16) if k not in (int(base.par.Canal), ch2, drum))
    k = m.note_cell(64)
    t.check('la nota de prueba cae en una celda libre', k not in (i, j) and m.world()['occ'][k] == 0)
    filtro0 = bool(base.par.Filtrar2)
    try:
        base.par.Filtrar2 = True
        t.midi(0x90 + libre - 1, 0x40, 0x64)             # canal de nadie
        W3 = m.world()
        t.check('Filtrar2 encendido: un canal ajeno se ignora', W3['occ'][k] == 0)
        t.check('...y no mueve Nota2', int(base.par.Nota2) == 0x32)
        base.par.Filtrar2 = False
        t.midi(0x90 + libre - 1, 0x40, 0x64)
        W3 = m.world()
        t.check('Filtrar2 apagado: cualquier canal cuenta como SEQ2',
                W3['occ'][k] >= 1 and W3['own'][k] == m.ARQ)
        t.check('...y Nota2 pasa a ser la ultima nota', int(base.par.Nota2) == 0x40)
        t.midi(0x80 + libre - 1, 0x40, 0x00)             # note off del mismo canal
    finally:
        base.par.Filtrar2 = filtro0


run_test(base, prueba)
print('  Ahora: PLAY con SEQ1 y SEQ2 sonando. Prueba longitudes distintas')
print('  (16 y 13): los hibridos aparecen donde los dos se cruzan.')
print('  Si el SEQ2 sale como "ignorado: canal X", pon X en Canal2 (pagina Fase2) o apaga Filtrar2.')
print('=' * 66)
