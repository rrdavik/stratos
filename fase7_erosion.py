"""
=============================================================================
ESTRATOS - FASE 7: EROSION SUPERFICIAL Y PRESUPUESTO DE DENSIDAD
=============================================================================
Requiere la fase 6.

QUE HACE
--------
Las 8 pistas de bateria del BeatStep son las 8 senales de destruccion.
Cada pad tiene un PERFIL de tres numeros (tabla perfiles_erosion,
editable):

    reduccion    cuantas NOTAS de construccion deshace en la celda que
                 golpea (v5: antes eran escalones). Un golpe de 1 deshace
                 lo que construyo una nota del SEQ.
    radio        cuantos anillos de vecinas alcanza: 0 solo la celda, 1 la
                 celda y sus vecinas, 2 un anillo mas. Cada anillo recibe
                 la mitad que el anterior.
    profundidad  cuantas conchas atraviesa el corte (desde la fase 9); 0 no
                 corta.

LA MISMA MONEDA QUE LA CONSTRUCCION (v5)
----------------------------------------
Cada nota del SEQ sube la formacion Growstep / coste y suma 1 a la carga
(fase 3). Cada nota de erosion hace lo contrario: baja la carga y la
altura lo mismo; al agotarse la carga baja un escalon y la carga queda
llena menos una. Lo que costo mas notas cuesta mas golpes deshacerlo,
tambien cerca del limite (la frenada). La carga ya no se vacia de golpe.
Orden: primero los satelites, luego la altura de la celda, al final la
HUELLA (una mancha oscura hasta que la celda se vuelve a sembrar).
En las vecinas, las fracciones de nota se acumulan: con radio 1 y
reduccion 1, cada vecina pierde una nota cada dos golpes.

PERFILES POR DEFECTO (v6, elegidos por el usuario)
--------------------------------------------------
    pad 1  bombo        temblor          -4 notas   radio 2  profundidad 2
    pad 2  caja         corte           -15 notas   radio 1  profundidad 3
    pad 3  tom          corte profundo   -4 notas   radio 1  profundidad 1
    pad 4  palmas, aro  aranazo          -3 notas   radio 1
    pad 5               aranazo          -2 notas   radio 1
    pad 6               aranazo          -2 notas
    pad 7  charles      aranazo          -1 nota
    pad 8  platillo     aranazo          -1 nota    radio 1
Cortan tres pads desde la fase 9: bombo, caja y tom. Las etiquetas de tipo
son del usuario; el comportamiento lo decide la tripleta.
Mientras suena el bombo el mundo no deja de cambiar, y los ciclos (fase 6)
acaban por edad maxima; al quitarlo, el mundo se asienta y se entierra por
estancamiento: el breakdown entierra el mundo.

EL BORDE DE LA CELDA DICE QUIEN DESTRUYE (v6)
---------------------------------------------
Sin balizas: cada celda cuenta con luz lo que le pasa, en una rejilla de
3 x 3 losetas opacas a ras de su superficie (geometria luz_celda, la crea
cualquier fase). El centro es el secuenciador que la toca (fase 3); las 8
losetas del borde son los 8 pads: el pad n a (n-1) x 45 grados (pad 1 al
este, pad 3 al norte...), con el color de su pad (tabla colores_drum).
Cada golpe enciende su sector en las celdas que erosiona: plena luz en la
celda, la mitad en el primer anillo, un cuarto en el segundo. Varios pads
a la vez, cada uno en su sector. Con secuenciador en la celda el centro
conserva su color; sin el, solo se enciende el borde. Colores opacos, sin
mezclas. Se apaga en Vidabalizadrum segundos; tambien se ve en modo
actuacion.
    Balizasdrum     luz de la bateria encendida / apagada
    Luzdrum         intensidad de la luz (1)
    Vidabalizadrum  segundos hasta apagarse (0,8)

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
Canal 16 (confirmado con el aparato), pads desde la nota 36 (do2, por
confirmar). Si salen como "pad fuera de 1-8", ajusta Notabase.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase7_erosion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase7 v6  (erosion en notas, perfiles del usuario, el borde de la celda es la bateria)'
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
add_par(base, page, 'toggle', 'Balizasdrum', 'Luz de la bateria en las celdas', True)
add_par(base, page, 'float', 'Luzdrum', 'Intensidad de la luz de la bateria', 1.0, 0.0, 2.0)
add_par(base, page, 'float', 'Vidabalizadrum', 'Vida de la luz (s)', 0.8, 0.05, 5.0)
renew_default(base, 'Vidabalizadrum', 0.6, 0.8)
renew_default(base, 'Vidabalizadrum', 1.0, 0.8)
ok('pagina Fase7: Canaldrum (16), Notabase (36), Objetivo, Umbraldensidad, '
   'Multradio, Padprueba, Erosionar, Balizasdrum, Luzdrum, Vidabalizadrum')

COLS = ['pad', 'reduccion', 'radio', 'profundidad', 'tipo', 'rol']


def filas_tabla(t):
    return [[t[r, c].val if t[r, c] is not None else '' for c in range(t.numCols)]
            for r in range(t.numRows)]


def clasificar_perfiles(filas, mm):
    """'v1' / 'v3' si la tabla sigue con los valores de esas versiones (sin
    editar), 'nueva' si ya tiene los de la v5 (reduccion en notas) y
    'editada' si alguien la ha cambiado a mano."""
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
    if perf == list(mm.PERFILES_V3) and tipos == list(mm.TIPOS_DEFECTO):
        return 'v3'
    if perf == list(mm.PERFILES_V5) and tipos == list(mm.TIPOS_DEFECTO):
        return 'v5'
    if perf == list(mm.PERFILES_DEFECTO) and tipos == list(mm.TIPOS_DEFECTO):
        return 'nueva'
    return 'editada'


def poner_roles(t, mm):
    """Corrige solo la columna rol (es una nota): no toca el resto."""
    try:
        cab = [t[0, c].val.strip() for c in range(t.numCols)]
        if 'rol' not in cab or 'pad' not in cab:
            return False
        ir, ip = cab.index('rol'), cab.index('pad')
        cambio = False
        for r in range(1, t.numRows):
            k = int(float(t[r, ip].val)) - 1
            if 0 <= k < 8 and t[r, ir].val != mm.ROLES_DEFECTO[k]:
                t[r, ir] = mm.ROLES_DEFECTO[k]
                cambio = True
        return cambio
    except Exception:
        return False


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
    ok('perfiles_erosion: reduccion en notas; bombo tiembla, caja y tom cortan. Editala a mano')
else:
    estado = clasificar_perfiles(filas_tabla(tabla), motor.module)
    if estado in ('v1', 'v3', 'v5'):
        escribir_perfiles(tabla, motor.module)
        ok('perfiles_erosion: tenia los valores de la %s, sustituidos (reduccion en notas)' % estado)
    elif estado == 'nueva':
        ok('perfiles_erosion: ya tiene los valores nuevos')
    else:
        info('perfiles_erosion editada a mano: se conserva. OJO: la columna reduccion '
             'ahora cuenta NOTAS, no escalones (un 3 de antes es mucho mas que un 3 de '
             'ahora); los nuevos valores por defecto estan en el montaje')
        if poner_roles(tabla, motor.module):
            ok('perfiles_erosion: columna rol al dia (7 charles, 8 platillo)')

colores = base.op('colores_drum')
if colores is not None and poner_roles(colores, motor.module):
    ok('colores_drum: columna rol al dia (7 charles, 8 platillo)')
if colores is None:
    colores = mk(base, 'tableDAT', 'colores_drum', -660, 200)
    colores.clear()
    colores.appendRow(['pad', 'r', 'g', 'b', 'rol'])
    for k, (r, g, b) in enumerate(motor.module.COLORES_DRUM):
        colores.appendRow([k + 1, '%.3f' % r, '%.3f' % g, '%.3f' % b, motor.module.ROLES_DEFECTO[k]])
    ok('colores_drum: un color por pad (rojos y violetas los cortes, frios los aranazos)')
else:
    info('colores_drum ya existia: se conserva como esta')

set_render(base)

leeme(base, 7, """FASE 7 - EROSION
  8 pads de bateria (Canaldrum 16, desde Notabase) = 8 perfiles editables
  en perfiles_erosion:
    reduccion    notas de construccion que deshace en la celda
    radio        anillos de vecinas (cada anillo, la mitad)
    profundidad  conchas que corta (fase 9)
  Una nota de erosion deshace lo que hizo una nota del SEQ: baja la carga
  y la altura; al agotarse la carga, baja un escalon. Orden: satelites,
  altura, huella.
  Perfiles del usuario: 1 bombo (-4, radio 2, corta 2), 2 caja (-15,
  radio 1, corta 3), 3 tom (-4, radio 1, corta 1), 4-8 aranazos.
  El borde de la celda dice quien destruye: el golpe enciende el sector
  de su pad (8 sectores alrededor del centro, colores_drum) en las celdas
  que erosiona; se apaga en Vidabalizadrum s. Luzdrum: intensidad.
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
    for k in range(200):
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
    cd = dict(m.cfg())
    cd['perfiles'], cd['tipos'] = list(m.PERFILES_DEFECTO), list(m.TIPOS_DEFECTO)
    cd['target_mode'], cd['balizas_drum'], cd['luz_drum'] = 0, 1, 1.0
    v1 = [COLS[:5]] + [[k + 1] + list(m.PERFILES_V1[k]) + [m.TIPOS_V1[k]] for k in range(8)]
    v3 = [COLS[:5]] + [[k + 1] + list(m.PERFILES_V3[k]) + [m.TIPOS_DEFECTO[k]] for k in range(8)]
    ed = [COLS[:5]] + [[k + 1, 2, 2, 0, 'aranazo'] for k in range(8)]
    v5 = [COLS[:5]] + [[k + 1] + list(m.PERFILES_V5[k]) + [m.TIPOS_DEFECTO[k]] for k in range(8)]
    t.check('tabla v1, v3 o v5 sin editar -> se sustituye; editada -> se conserva',
            clasificar_perfiles(v1, m) == 'v1' and clasificar_perfiles(v3, m) == 'v3'
            and clasificar_perfiles(v5, m) == 'v5' and clasificar_perfiles(ed, m) == 'editada')
    # luz de celda: que hay dibujado en una celda (centro y sectores del borde)
    def losetas(Wx, cx, now, celda):
        nn = m.normal_i(celda)
        e, tt = m.tangents(nn)
        base_r = m.base_radius(Wx, cx, celda)
        cw, cl = m._cell_sizes(base_r, celda)
        if m.is_pole(celda):
            cw, cl = cw * 1.25, cl * 1.25
        centro, borde = [], {}
        for f in m.cell_lights(Wx, cx, now):
            p = f[:3]
            k = sum(p[q] * nn[q] for q in range(3))
            if k <= 0:
                continue
            lat = [p[q] - k * nn[q] for q in range(3)]
            x = sum(lat[q] * e[q] for q in range(3)) / cw
            z = sum(lat[q] * tt[q] for q in range(3)) / cl
            if abs(x) > 0.55 or abs(z) > 0.55:
                continue
            col = tuple(round(v, 3) for v in f[9:12])
            if max(abs(x), abs(z)) < 0.3:
                centro.append(col)
            else:
                d = (1 if x > 0.19 else -1 if x < -0.19 else 0,
                     1 if z > 0.19 else -1 if z < -0.19 else 0)
                borde[m.PAD_DIRS.index(d)] = col
        return centro, borde
    redondo = lambda col: tuple(round(v, 3) for v in col)
    # 1. los 8 pads a la vez en la celda donde toca el SEQ1
    W3 = m.new_world()
    for k in range(3):
        m.note_on(W3, cd, 1, 64, 100, 2.0)
    for pad in range(8):
        m.light_cell(W3, cd, i, pad, 1.0, 2.0)
    centro, borde = losetas(W3, cd, 2.05, i)
    t.check('golpe en la celda del SEQ1: el centro conserva su color y el borde el del pad',
            centro == [redondo([v * (0.6 + 0.4 * math.exp(-0.05 / m.SEQ_DECAY))
                                for v in m.seq_color(cd, 1)])]
            and sorted(borde) == list(range(8))
            and all(borde[pd] == redondo(cd['colores_drum'][pd]) for pd in range(8)),
            'centro %s, %d sectores' % (centro, len(borde)))
    t.check('8 pads a la vez: 8 sectores de 8 colores distintos',
            len(set(borde.values())) == 8)
    bien, det = instance_color_ok(base.op('luz_celda'))
    t.check('luz_celda pinta el color de cada instancia (lo que se dibuja)', bien, det)
    # 2. golpe sin secuenciador en la celda: solo el borde
    vacia = m.note_cell(70)
    m.light_cell(W3, cd, vacia, 6, 1.0, 2.0)
    centro, borde = losetas(W3, cd, 2.05, vacia)
    t.check('golpe sin secuenciador en la celda: solo se enciende el borde',
            not centro and list(borde) == [6])
    # 3. un golpe: la celda a plena luz, el radio mas tenue, y se apaga
    W3b = m.new_world()
    m.note_on(W3b, cd, 1, 64, 100, 0.0)
    ev = m.erosion(W3b, cd, 0, 1, 2.0)              # bombo: radio 2
    nivel = {c_: m.light_level(cd, h[0], 2.05) for c_, h in W3b['luz'].items()}
    anillos = dict(m.rings(ev['celda'], 2))
    a1 = [nivel[x] for x, d in anillos.items() if d == 1 and x in nivel]
    a2 = [nivel[x] for x, d in anillos.items() if d == 2 and x in nivel]
    t.check('el golpe enciende su sector en la celda y su radio, mas tenue al alejarse',
            nivel.get(ev['celda'], 0) > max(a1) > max(a2) > 0, '%d celdas' % len(nivel))
    t.check('se apaga en Vidabalizadrum',
            not W3b['luz'] or not m.cell_lights(dict(W3b, last={1: None, 2: None}), cd,
                                                2.0 + cd['vida_baliza_drum'] + 1e-3))
    # 4. se ve con formacion, vacia y con huella
    W5 = m.new_world()
    for k in range(6):
        m.note_on(W5, cd, 1, 60, 100, 0.0)          # con formacion
    m.note_on(W5, cd, 1, 62, 100, 0.0)
    hu = m.note_cell(62)
    m.degrade(W5, cd, hu, 1)                        # huella
    W5['last'] = {1: None, 2: None}
    vis = True
    for celda in (m.note_cell(60), hu, vacia):
        m.light_cell(W5, cd, celda, 1, 1.0, 4.0)
        vis = vis and bool(losetas(W5, cd, 4.01, celda)[1])
    t.check('la luz se ve con formacion, vacia y con huella', vis and W5['huella'][hu] > 0)
    t.check('los pads 1, 2 y 3 cortan; ningun otro', m.pads_corte(cd) == [0, 1, 2])
    # 4. pad 7 repetido sobre una celda en crecimiento, con el SEQ1 tocando
    W6 = m.new_world()
    for k in range(3):
        m.note_on(W6, cd, 1, 64, 100, 0.0)

    def notas(Wx):      # notas de construccion acumuladas en la celda
        o = Wx['occ'][i]
        return (1 + sum(m.cost(cd, x) for x in range(1, o)) + Wx['carga'][i]) if o else 0
    n_ini, h_ini = notas(W6), W6['h'][i]
    bajadas, pasos = [], []
    for r in range(4):
        m.note_on(W6, cd, 1, 64, 100, 1.0 + r)
        m.note_on(W6, cd, 1, 64, 100, 1.0 + r)
        h0, n0 = W6['h'][i], notas(W6)
        m.erosion(W6, cd, 6, 1, 1.5 + r)
        bajadas.append(round(h0 - W6['h'][i], 4))
        pasos.append(n0 - notas(W6))
    t.check('pad 7: cada golpe deshace una nota (baja un poco, sin vaciar la carga) y, '
            'con el SEQ1 tocando mas, la celda sigue creciendo',
            all(b > 0 for b in bajadas) and pasos == [1] * 4
            and notas(W6) == n_ini + 4 and W6['h'][i] > h_ini,
            'bajadas %s' % bajadas)
    # 5. simetria: N notas de construccion y N de erosion
    malos = []
    for base_n, extra in ((3, 1), (3, 5), (4, 6), (6, 4)):
        W7 = m.new_world()
        for k in range(base_n):
            m.note_on(W7, cd, 1, 64, 100, 0.0)
        antes = (W7['occ'][i], W7['carga'][i], round(W7['h'][i], 6))
        for k in range(extra):
            m.note_on(W7, cd, 1, 64, 100, 0.0)
        m.degrade(W7, cd, i, extra)
        despues = (W7['occ'][i], W7['carga'][i], round(W7['h'][i], 6))
        if antes != despues or m.satellites_of(W7, i):
            malos.append('%d+%d: %s -> %s' % (base_n, extra, antes, despues))
    t.check('simetria: N notas de construccion y N de erosion devuelven la celda',
            not malos, '; '.join(malos))
    # 6. atenuacion: la celda objetivo pierde mas que las vecinas
    W8 = m.new_world()
    for n in range(40, 90):
        for k in range(4):
            m.note_on(W8, cd, 1, n, 100, 0.0)
    m.note_on(W8, cd, 1, 64, 100, 0.0)
    h0 = list(W8['h'])
    ev = m.erosion(W8, cd, 3, 1, 5.0)              # pad 4: -4 notas, radio 1
    caida = lambda x: h0[x] - W8['h'][x]
    vec = [x for x, d in m.rings(ev['celda'], 1) if d == 1]
    t.check('atenuacion: la celda objetivo pierde mas que sus vecinas',
            caida(ev['celda']) > max(caida(x) for x in vec) >= 0,
            '%.3f / %.3f' % (caida(ev['celda']), max(caida(x) for x in vec)))
    # 7. sin balizas
    t.check('ninguna baliza en escena ni en CHOP_NAMES',
            all(base.op(nm) is None for nm in ('baliza', 'baliza_chop', 'baliza2', 'i_baliza2',
                                               'balizas_drum', 'luz_drum'))
            and not [x for x in m.CHOP_NAMES if 'baliza' in x])
    m.reset_world()
    t.midi(0x9C, 0x3C, 0x64)
    m.on_pulse('Erosionar')
    W = m.world()
    k = int(base.par.Padprueba) - 1
    t.check('Padprueba + Erosionar encienden su sector', k in W['drum'] and W['luz'])
    cian, ambar, blanco = (0.10, 0.90, 1.00), (1.0, 0.7, 0.3), (0.95, 0.95, 0.92)
    t.check('ningun color es cian, ambar ni blanco',
            all(sum(abs(a - b) for a, b in zip(col, ref)) > 0.3
                for col in cd['colores_drum'] for ref in (cian, ambar, blanco)))
    geo = base.op('luz_celda')
    t.check('luz_celda gira y se balancea con el planeta',
            geo is not None and 'rotation(' in (geo.par.ry.expr or '')
            and 'wobble(' in (geo.par.rx.expr or ''))
    t.check('leyenda EROSION', 'EROSION' in m.legend())


run_test(base, prueba)
print('  Ahora: anade la bateria del BeatStep (canal 16). Cada golpe ilumina las')
print('  celdas que erosiona con el color de su pad; el bombo hace temblar el')
print('  paisaje; caja y tom abriran cortes en la fase 9.')
print('  Si los golpes salen como "pad fuera de 1-8", ajusta Notabase.')
print('  Ajusta el equilibrio crecimiento / erosion antes de pasar a la fase 8.')
print('=' * 66)
