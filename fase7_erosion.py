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

CUANTO MAS FRECUENTE EL GOLPE, MAS SUPERFICIAL (v3)
---------------------------------------------------
    pad 1  bombo        temblor          -1  radio 2
    pad 2  caja         corte            -3  radio 1  profundidad 3
    pad 3  tom          corte profundo   -3  radio 2  profundidad 4
    pad 4  palmas, aro  aranazo          -2  radio 1
    pad 5               aranazo          -2
    pad 6               aranazo          -1  radio 1
    pad 7               aranazo          -1
    pad 8  charles      aranazo          -1
El bombo, la pista mas densa, sacude una zona ancha sin vaciarla; la caja
fractura; los toms, que suelen ir en los redobles, abren las heridas. El
temblor se porta como un aranazo (sin corte, destello suave).
Mientras suena el bombo el mundo no deja de cambiar, y los ciclos (fase 6)
acaban por edad maxima; al quitarlo, el mundo se asienta y se entierra por
estancamiento: el breakdown entierra el mundo.

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

BALIZAS DE LA BATERIA (v3)
--------------------------
Una baliza por pad, mas pequena que la del SEQ2 y cada una de su color
(tabla colores_drum, editable), en la celda que recibe el golpe. Cada pad
tiene su hueco en un anillo alrededor del centro de la celda (pad n a
(n-1) x 45 grados), asi bombo y charles en la misma celda se ven los dos.
El anillo nunca es tan pequeno que las 8 se toquen, y se abre lo justo
para que ninguna quede dentro o detras de la baliza del SEQ1 o del SEQ2
(los golpes suelen caer en su celda): con el pulso de la nota se abre y
al apagarse se cierra.
Se enciende con cada golpe, crece con la velocidad, se mantiene casi
entera y se apaga del todo en Vidabalizadrum segundos: los pads
frecuentes casi siempre estan encendidos; los raros destellan.
    Balizasdrum       encendidas / apagadas
    Tambalizadrum     tamano (x la baliza del SEQ2 en reposo), 0,6
    Anillobalizadrum  anillo minimo (x ancho de la celda), 0,35
    Vidabalizadrum    segundos hasta apagarse, 1,0

EL CANAL DE LA BATERIA
----------------------
Canal 16 (confirmado con el aparato), pads desde la nota 36 (do2, por
confirmar). Si salen como "pad fuera de 1-8", ajusta Notabase.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase7_erosion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase7 v4  (canal 16; bombo tiembla, caja y tom cortan; huellas, presupuesto)'
banner(VERSION)

base = require_base(7)
motor = install_core(base, CARPETA, 7)

page = get_page(base, 'Fase7')
add_par(base, page, 'int', 'Canaldrum', 'Canal MIDI de la bateria', 16, 1, 16, clamp=True)
renew_default(base, 'Canaldrum', 10, 16)
add_par(base, page, 'int', 'Notabase', 'Nota del pad 1', 36, 0, 120, clamp=True)
add_par(base, page, 'menu', 'Objetivo', 'Donde cae la erosion', 'alterna',
        menu=['seq1', 'seq2', 'alterna', 'velocidad'],
        menu_labels=['Donde esta el SEQ1', 'Donde esta el SEQ2',
                     'Alterna SEQ1 / SEQ2', 'La velocidad elige celda'])
add_par(base, page, 'float', 'Umbraldensidad', 'Presupuesto de densidad', 0.60, 0.1, 1.0)
add_par(base, page, 'float', 'Multradio', 'Multiplicador de radio', 2.0, 1.0, 4.0)
add_par(base, page, 'int', 'Padprueba', 'Pad de prueba', 1, 1, 8, clamp=True)
add_par(base, page, 'pulse', 'Erosionar', 'Erosionar con el pad de prueba')
add_par(base, page, 'toggle', 'Balizasdrum', 'Balizas de la bateria', True)
add_par(base, page, 'float', 'Tambalizadrum', 'Tamano de baliza (x SEQ2)', 0.6, 0.05, 2.0)
add_par(base, page, 'float', 'Anillobalizadrum', 'Anillo minimo de los pads (x celda)', 0.35, 0.0, 1.0)
add_par(base, page, 'float', 'Vidabalizadrum', 'Vida de la baliza (s)', 1.0, 0.05, 5.0)
renew_default(base, 'Tambalizadrum', 0.5, 0.6)
renew_default(base, 'Vidabalizadrum', 0.6, 1.0)
ok('pagina Fase7: Canaldrum (16), Notabase (36), Objetivo, Umbraldensidad, '
   'Multradio, Padprueba, Erosionar, Balizasdrum, Tambalizadrum, Anillobalizadrum, '
   'Vidabalizadrum')

COLS = ['pad', 'reduccion', 'radio', 'profundidad', 'tipo', 'rol']


def filas_tabla(t):
    return [[t[r, c].val if t[r, c] is not None else '' for c in range(t.numCols)]
            for r in range(t.numRows)]


def clasificar_perfiles(filas, mm):
    """'v1' si la tabla sigue con los valores de la fase 7 v1, 'nueva' si ya
    tiene los de la v3 y 'editada' si alguien la ha cambiado a mano."""
    if not filas:
        return 'v1'
    cab = [str(x).strip() for x in filas[0]]
    try:
        ix = [cab.index(n) for n in ('reduccion', 'radio', 'profundidad')]
    except ValueError:
        return 'editada'
    it = cab.index('tipo') if 'tipo' in cab else None
    if len(filas) != 9:
        return 'editada'
    perf, tipos = [], []
    try:
        for f in filas[1:9]:
            perf.append(tuple(int(float(f[k])) for k in ix))
            tipos.append(str(f[it]).strip() if it is not None else '')
    except Exception:
        return 'editada'
    if perf == list(mm.PERFILES_V1) and tipos == list(mm.TIPOS_V1):
        return 'v1'
    if perf == list(mm.PERFILES_DEFECTO) and tipos == list(mm.TIPOS_DEFECTO):
        return 'nueva'
    return 'editada'


def escribir_perfiles(t, mm):
    t.clear()
    t.appendRow(COLS)
    for k in range(8):
        red, rad, prof = mm.PERFILES_DEFECTO[k]
        t.appendRow([k + 1, red, rad, prof, mm.TIPOS_DEFECTO[k], mm.ROLES_DEFECTO[k]])


tabla = base.op('perfiles_erosion')
if tabla is None:
    tabla = mk(base, 'tableDAT', 'perfiles_erosion', -660, 80)
    escribir_perfiles(tabla, motor.module)
    ok('perfiles_erosion: bombo tiembla, caja y tom cortan, 4-8 aranazos. Editala a mano')
else:
    estado = clasificar_perfiles(filas_tabla(tabla), motor.module)
    if estado == 'v1':
        escribir_perfiles(tabla, motor.module)
        ok('perfiles_erosion: tenia los valores de la v1, sustituidos por los nuevos')
    elif estado == 'nueva':
        if 'rol' not in [x.strip() for x in filas_tabla(tabla)[0]]:
            escribir_perfiles(tabla, motor.module)
        ok('perfiles_erosion: ya tiene los valores nuevos')
    else:
        info('perfiles_erosion editada a mano: se conserva; los nuevos valores por '
             'defecto estan en el montaje')

colores = base.op('colores_drum')
if colores is None:
    colores = mk(base, 'tableDAT', 'colores_drum', -660, 200)
    colores.clear()
    colores.appendRow(['pad', 'r', 'g', 'b', 'rol'])
    for k, (r, g, b) in enumerate(motor.module.COLORES_DRUM):
        colores.appendRow([k + 1, '%.3f' % r, '%.3f' % g, '%.3f' % b, motor.module.ROLES_DEFECTO[k]])
    ok('colores_drum: un color por pad (rojos y violetas los cortes, frios los aranazos)')
else:
    info('colores_drum ya existia: se conserva como esta')

make_constant(base, 'mat_balizas_drum', 780, 700, (1.0, 1.0, 1.0))
make_instanced(base, 'balizas_drum', 520, 700, 'mat_balizas_drum', sop='sphere')
set_render(base)

leeme(base, 7, """FASE 7 - EROSION
  8 pads de bateria (Canaldrum 16, desde Notabase) = 8 perfiles editables
  en perfiles_erosion: reduccion, radio, profundidad, tipo (rol: solo nota).
  Cuanto mas frecuente el golpe, mas superficial: 1 bombo tiembla (radio 2),
  2 caja corta, 3 tom corte profundo, 4-8 aranazos.
  Balizas de la bateria: una por pad, de su color (colores_drum), en su
  hueco de la celda golpeada; se apagan en Vidabalizadrum s.
  Orden de caida: satelites, altura, huella.
  Presupuesto: por encima de Umbraldensidad, radios x Multradio.
  Prueba: Padprueba + Erosionar.""")

print_report()


def prueba(t):
    import math
    m = t.m
    m.reset_world()
    c = m.cfg()
    for k in range(16):                           # limite + 2 desbordes
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
    t.check('perfiles leidos de la tabla', len(m.cfg()['perfiles']) == 8
            and len(m.cfg()['tipos']) == 8)
    # perfiles por defecto: el bombo tiembla, solo caja y tom cortan
    cd = dict(m.cfg())
    cd['perfiles'], cd['tipos'] = list(m.PERFILES_DEFECTO), list(m.TIPOS_DEFECTO)
    cd['target_mode'] = 0
    W3 = m.new_world()
    for n in range(40, 80):
        for k in range(3):
            m.note_on(W3, cd, 1, n, 100, 0.0)
    m.note_on(W3, cd, 1, 60, 100, 0.0)
    occ0 = list(W3['occ'])
    ev = m.erosion(W3, cd, 0, 1, 1.0)
    tocadas = sum(1 for a, b in zip(occ0, W3['occ']) if b < a)
    t.check('pad 1 (bombo): temblor, -1 en radio 2, sin corte',
            ev['tipo'] == 'temblor' and ev['red'] == 1 and ev['prof'] == 0
            and 'corte' not in ev and tocadas >= 7, '%d celdas' % tocadas)
    t.check('solo los pads 2 y 3 cortan', m.pads_corte(cd) == [1, 2])
    v1 = [COLS[:5]] + [[k + 1] + list(m.PERFILES_V1[k]) + [m.TIPOS_V1[k]] for k in range(8)]
    ed = [COLS[:5]] + [[k + 1, 2, 2, 0, 'aranazo'] for k in range(8)]
    t.check('tabla con los valores v1 -> se sustituye; editada -> se conserva',
            clasificar_perfiles(v1, m) == 'v1' and clasificar_perfiles(ed, m) == 'editada')
    # balizas de la bateria: un golpe de cada pad en la misma celda
    cb = dict(m.cfg())
    cb['perfiles'], cb['tipos'] = [(1, 0, 0)] * 8, ['aranazo'] * 8
    cb['target_mode'], cb['balizas_drum'] = 0, 1
    W4 = m.new_world()
    m.note_on(W4, cb, 1, 60, 100, 0.0)
    for pad in range(8):
        m.erosion(W4, cb, pad, 1, 5.0)
    celda = m.note_cell(60)
    filas = m.drum_beacons(W4, cb, 5.0)
    n = m.normal_i(celda)
    huecos = set()
    bien = len(filas) == 8
    for pad, f in enumerate(filas):
        col = tuple(round(x, 3) for x in f[9:12])
        bien = bien and col == tuple(round(x, 3) for x in cb['colores_drum'][pad])
        d = (f[0] * n[0] + f[1] * n[1] + f[2] * n[2])
        lat = [f[k] - d * n[k] for k in range(3)]
        huecos.add(tuple(round(x, 4) for x in lat))
        bien = bien and W4['drum'][pad]['cell'] == celda
    t.check('8 pads en la misma celda: 8 balizas, cada una en su hueco y con su color',
            bien and len(huecos) == 8, '%d balizas' % len(filas))
    t.check('se apagan en Vidabalizadrum',
            not m.drum_beacons(W4, cb, 5.0 + cb['vida_baliza_drum'] + 1e-3))
    cian, ambar, blanco = (0.10, 0.90, 1.00), (1.0, 0.7, 0.3), (0.95, 0.95, 0.92)
    t.check('ninguna es cian, ambar ni blanca',
            all(sum(abs(a - b) for a, b in zip(col, ref)) > 0.3
                for col in cb['colores_drum'] for ref in (cian, ambar, blanco)))
    m.reset_world()
    t.midi(0x9C, 0x3C, 0x64)
    m.on_pulse('Erosionar')
    W = m.world()
    k = int(base.par.Padprueba) - 1
    t.check('Padprueba + Erosionar encienden su baliza', k in W['drum'])
    # las balizas de la bateria no quedan tapadas por las de los secuenciadores
    def holguras(Wb, cb_, celda, now):
        filas_ = m.drum_beacons(Wb, cb_, now)
        nn = m.normal_i(celda)
        seq = m.seq_beacons(Wb, cb_, now)
        def lat(v):
            k = v[0] * nn[0] + v[1] * nn[1] + v[2] * nn[2]
            return math.sqrt(sum((v[q] - k * nn[q]) ** 2 for q in range(3)))
        h_seq = min([lat([f[q] - cc[q] for q in range(3)]) - R - f[6]
                     for f in filas_ for cc, R in seq] or [9.0])
        h_ent = min([lat([filas_[a][q] - filas_[b][q] for q in range(3)]) - filas_[a][6] - filas_[b][6]
                     for a in range(len(filas_)) for b in range(a + 1, len(filas_))] or [9.0])
        return len(filas_), h_seq, h_ent
    ecuador = min(range(m.N), key=lambda x: abs(m.normal_i(x)[1]))
    casos = [('ecuador', ecuador), ('junto al polo', m.RINGS[0][0]), ('polo', m.POLE_S)]
    cs = dict(cb)
    cs['nivel'] = max(5, cs['nivel'])
    peor = []
    for nombre, celda in casos:
        for s_, sn in ((m.GEO, 'SEQ1'), (m.ARQ, 'SEQ2')):
            for fase_, dt_ in (('reposo', 1.0), ('pulso', 0.0)):
                Wb = m.new_world()
                for k in range(6):
                    m.note_on(Wb, cs, s_, m.cell_note(celda), 100, 10.0)
                Wb['vh'] = list(Wb['h'])
                for pad in range(8):
                    Wb['drum'][pad] = dict(t=10.0 + dt_ - 0.01, cell=celda, vel=127)
                nb_, hs, he = holguras(Wb, cs, celda, 10.0 + dt_)
                if nb_ != 8 or hs <= 0 or he <= 0:
                    peor.append('%s %s %s (%d, %.2f, %.2f)' % (nombre, sn, fase_, nb_, hs, he))
    t.check('8 balizas fuera de la silueta del SEQ1 y del SEQ2 (reposo y pulso, '
            'ecuador, junto al polo y polo) y sin pisarse', not peor, '; '.join(peor[:3]))
    rmax, rmin = m.drum_radius(cb, 127), m.drum_radius(cb, 1)
    t.check('tamano: perceptible (>= 0,15) y menor que el SEQ2 en reposo',
            rmin >= 0.15 and rmax < m.BALIZA2_RADIO, '%.2f a %.2f' % (rmin, rmax))
    geo = base.op('balizas_drum')
    t.check('balizas_drum gira y se balancea con el planeta',
            geo is not None and 'rotation(' in (geo.par.ry.expr or '')
            and 'wobble(' in (geo.par.rx.expr or ''))
    t.check('leyenda EROSION', 'EROSION' in m.legend())


run_test(base, prueba)
print('  Ahora: anade la bateria del BeatStep (canal 16). El bombo hace temblar')
print('  el paisaje; caja y tom abriran cortes en la fase 9.')
print('  Cada pad enciende su baliza de color donde cae el golpe.')
print('  Si los golpes salen como "pad fuera de 1-8", ajusta Notabase.')
print('  Ajusta el equilibrio crecimiento / erosion antes de pasar a la fase 8.')
print('=' * 66)
