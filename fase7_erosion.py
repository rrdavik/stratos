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

LA VELOCIDAD (v7)
-----------------
Con Erosionvel (encendido), la reduccion de la tabla es la de un golpe a
velocidad Velref (100) y escala en proporcion: a 50, la mitad; a 127, x1,27.
Minimo: un golpe siempre deshace al menos una nota en su celda (o la
reduccion, si es menor), para que un golpe flojo no quede en nada. Las
fracciones de nota se acumulan en cada celda: N golpes iguales deshacen
siempre lo mismo. Solo escala la reduccion; radio y profundidad no.
Apagado, la reduccion es la de la tabla, sin mas.
    Erosionvel   la velocidad escala la erosion (encendido)
    Velref       velocidad a la que valen los numeros de la tabla (100)

PERFILES POR DEFECTO (v6, elegidos por el usuario; v12, bombo y tom impulso)
----------------------------------------------------------------------------
    pad 1  bombo        IMPULSO x3       (la tripleta se guarda: -4, 2, 2)
    pad 2  caja         corte           -15 notas   radio 1  profundidad 3
    pad 3  tom          IMPULSO x2       (la tripleta se guarda: -4, 1, 1)
    pad 4  palmas, aro  aranazo          -3 notas   radio 1
    pad 5               aranazo          -2 notas   radio 1
    pad 6               aranazo          -2 notas
    pad 7  charles      aranazo          -1 nota
    pad 8  platillo     aranazo          -1 nota    radio 1
Desde la fase 9 corta la caja. Las etiquetas de tipo son del usuario; el
comportamiento lo deciden el modo y la tripleta.

EL BOMBO Y EL TOM, IMPULSO DE CREACION (v12)
--------------------------------------------
El bombo y la caja/toms en los pads mas destructivos no dejaban un mundo
equilibrado entre creacion y destruccion. Ahora el bombo es la respiracion
del planeta: cada golpe empuja la corteza desde dentro; el tom, un latido
mas corto. El mundo no se rompe al ritmo: se infla y se asienta.
La tabla perfiles_erosion tiene dos columnas mas, para cambiar cualquier pad
a mano:
    modo         erosion (defecto) / impulso
    capacidad    multiplicador de capacidad (solo en impulso): 3 el bombo, 2 el tom
Un pad en impulso ignora reduccion, radio y profundidad: no resta ocupacion,
no deja huella, no corta ni deja cicatriz y no entra en el presupuesto de
densidad. Cae donde caeria la erosion (Objetivo; con alterna, bombo y tom,
impares, caen donde esta el SEQ1) y:
  1. CAPACIDAD. La celda se porta como si fuera 'cap' veces mas grande: el
     limite de altura y los umbrales de ramificacion, fusion, coronacion y
     cumbre, x cap (con cap 3: satelites desde 15, fusion desde 21, corona
     desde 27). Cada senal sigue subiendo Growstep x el limite de siempre,
     hasta el limite nuevo: donde antes se desbordaba en satelites, sigue
     subiendo (montana mas alta, edificio que se vuelve rascacielos).
     cap = max(cap, capacidad del pad): un tom no rebaja un x3 del bombo y
     dos bombos no dan x9. Cada golpe renueva la duracion (Capmodo):
       decae      vuelve a 1 tras Capdur pasos (16 = un compas) sin golpes de
                  impulso en la celda. Lo construido no se recorta: si la
                  ocupacion ya supera el umbral normal, la siguiente nota que
                  dispare un trigger se desborda.
       sostenido  hasta el entierro. La capa nueva empieza con cap 1.
     En una celda vacia el golpe fija igualmente su cap y se ve su color.
  2. PUMPING, UN GOLPE SECO (v13). En el golpe, lo dibujado en la celda
     (formacion, satelite, corona, piezas de fusion) salta de golpe a su
     tamano maximo, anclado en su base: vertical 1 + (cap del pad - 1) x
     Pumpamt (el bombo, x3; el tom, x2), horizontal 1 + (vertical - 1) x
     Pumphorz, sin pasar del ancho de la celda. Sin rampa: el pico se ve en
     el primer fotograma, se sostiene Pumphold s (y al menos 2 fotogramas) y
     vuelve a 1 en los segundos de la columna pump_rel de su pad (el bombo
     0,20, el tom 0,12), deprisa al principio y plano al final:
         escala = 1 + (pico - 1) x (1 - t / pump_rel)^3
     Tope por el ritmo: el golpe entero (pico y caida) cabe en 0,8 x el
     tiempo desde el golpe anterior en la celda (en una rafaga de
     semicorcheas, 0,8 x el paso): vuelve a 1 antes del siguiente. Un golpe
     durante la caida salta otra vez al pico, en seco. Es la transformacion
     final sobre la altura que se ve (ya suavizada), en cada fotograma: no
     cambia la altura real. La velocidad escala el pico entre Pumpvelmin
     (0,6) y 1: un golpe flojo se nota, pero menos.
  3. LUZ. El color del pad sobre la celda, sin tapar el del secuenciador
     (si suena en la celda, el centro se parte). El destello (fase 9) es
     suave y sigue la curva del pumping.
    Capmodo      decae / sostenido (decae)
    Capdur       pasos sin golpes hasta que la capacidad vuelve a 1 (16)
    Pumpamt      cuanto hincha el golpe (1: el bombo x3, el tom x2)
    Pumphorz     cuanto se ensancha (0,30 de lo que crece en altura)
    Pumphold     segundos en el pico (0,04; al menos 2 fotogramas)
    Pumpvelmin   el pico de un golpe a velocidad 1 (0,6 del maximo)
    Pumpon       pumping encendido
    pump_rel     (columna de perfiles_erosion) segundos de caida de cada pad
Leyenda: IMPULSO pad 1 x3 celda 40 cap 3 (16 pasos) en lugar de la linea
EROSION, y MUNDO cuenta las celdas con capacidad: cap+ 7.
A vigilar (sin compensar todavia): con mas capacidad se desborda mas tarde,
asi que el territorio tarda mas en llenarse y los mundos pueden durar mas;
y las celdas con cap alto acumulan mas ocupacion y heredan mas (25 %).

EL GOLPE SE VE COMO UNA NOTA (v9)
---------------------------------
Sin balizas ni sectores: cada golpe ilumina, igual que una nota de un
secuenciador, el centro de las celdas que erosiona (loseta luz_celda) y su
formacion, que se hincha y se tine, con el color de su pad (tabla
colores_drum): plena en la celda del golpe, la mitad en el primer anillo y
un cuarto en el segundo. Se apaga en Vidabalizadrum segundos. Si en la
celda hay un secuenciador, manda la luz mas intensa en ese instante (el
golpe, mientras dura); al apagarse vuelve la del secuenciador. Se ve con
formacion, vacia o con huella, y en modo actuacion.
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
  velocidad la velocidad del golpe elige una de las celdas (85 con do1-do8)
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

VERSION = 'fase7 v13  (bombo y tom: impulso de creacion; pumping seco, pico al instante)'
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
add_par(base, page, 'toggle', 'Erosionvel', 'La velocidad escala la erosion', True)
add_par(base, page, 'int', 'Velref', 'Velocidad a la que vale la tabla', 100, 1, 127, clamp=True)
renew_default(base, 'Vidabalizadrum', 0.6, 0.8)
renew_default(base, 'Vidabalizadrum', 1.0, 0.8)
add_par(base, page, 'menu', 'Capmodo', 'Capacidad del impulso', 'decae',
        menu=['decae', 'sostenido'], menu_labels=['Decae tras Capdur pasos', 'Sostenida hasta el entierro'])
add_par(base, page, 'int', 'Capdur', 'Pasos hasta que la capacidad decae', 16, 1, 128, clamp=True)
add_par(base, page, 'float', 'Pumpamt', 'Pumping: cuanto hincha', 1.0, 0.0, 2.0)
add_par(base, page, 'float', 'Pumphorz', 'Pumping: cuanto ensancha', 0.30, 0.0, 1.0)
renew_default(base, 'Pumphorz', 0.15, 0.30)
add_par(base, page, 'float', 'Pumphold', 'Pumping: segundos en el pico', 0.04, 0.0, 0.5)
add_par(base, page, 'float', 'Pumpvelmin', 'Pumping: pico a velocidad minima', 0.6, 0.0, 1.0)
add_par(base, page, 'toggle', 'Pumpon', 'Pumping encendido', True)
viejos = [nm for nm in ('Pumpataque', 'Pumprelease') if remove_par(base, nm)]
if viejos:
    ok('pumping seco (v13): fuera %s (sin rampa; la caida, por pad en perfiles_erosion)' % ', '.join(viejos))
ok('pagina Fase7: Canaldrum (16), Notabase (36), Objetivo, Umbraldensidad, '
   'Multradio, Padprueba, Erosionar, Balizasdrum, Luzdrum, Vidabalizadrum, Erosionvel, Velref')
ok('pagina Fase7 (impulso): Capmodo (decae), Capdur (16), Pumpamt (1), Pumphorz (0,30), '
   'Pumphold (0,04 s), Pumpvelmin (0,6), Pumpon')

COLS = ['pad', 'reduccion', 'radio', 'profundidad', 'modo', 'capacidad', 'pump_rel', 'tipo', 'rol']
COLS_V12 = ['pad', 'reduccion', 'radio', 'profundidad', 'modo', 'capacidad', 'tipo', 'rol']  # sin pump_rel
COLS_V11 = ['pad', 'reduccion', 'radio', 'profundidad', 'tipo', 'rol']   # sin modo ni capacidad


def filas_tabla(t):
    return [[t[r, c].val if t[r, c] is not None else '' for c in range(t.numCols)]
            for r in range(t.numRows)]


def clasificar_perfiles(filas, mm):
    """'v1' / 'v3' / 'v5' / 'v11' / 'v12' si la tabla sigue con los valores
    de esas versiones (sin editar), 'nueva' si ya tiene los de la v13 (con
    modo, capacidad y pump_rel), 'sin_modo' si alguien la edito a mano antes
    de la v12 (le faltan modo, capacidad y pump_rel), 'sin_pump' si la edito
    en la v12 (le falta pump_rel) y 'editada' si la edito despues."""
    if not filas:
        return 'v1'
    cab = [str(x).strip() for x in filas[0]]
    try:
        ix = [cab.index(n) for n in ('reduccion', 'radio', 'profundidad')]
    except ValueError:
        return 'editada'
    it = cab.index('tipo') if 'tipo' in cab else None
    con_modo = 'modo' in cab and 'capacidad' in cab
    con_pump = 'pump_rel' in cab
    a_mano = 'editada' if con_modo and con_pump else 'sin_pump' if con_modo else 'sin_modo'
    if len(filas) != 9:
        return a_mano
    perf, tipos, modos, caps, rels = [], [], [], [], []
    try:
        for f in filas[1:9]:
            perf.append(tuple(int(float(f[k])) for k in ix))
            tipos.append(str(f[it]).strip() if it is not None else '')
            if con_modo:
                modos.append(str(f[cab.index('modo')]).strip())
                caps.append(float(f[cab.index('capacidad')]))
            if con_pump:
                rels.append(float(f[cab.index('pump_rel')]))
    except Exception:
        return a_mano
    if con_modo:
        if perf == list(mm.PERFILES_DEFECTO) and tipos == list(mm.TIPOS_DEFECTO) \
                and modos == list(mm.MODOS_DEFECTO) and caps == list(mm.CAPACIDAD_DEFECTO):
            if not con_pump:
                return 'v12'
            if rels == list(mm.PUMP_REL_DEFECTO):
                return 'nueva'
        return a_mano
    if perf == list(mm.PERFILES_V1) and tipos == list(mm.TIPOS_V1):
        return 'v1'
    if perf == list(mm.PERFILES_V3) and tipos == list(mm.TIPOS_V11):
        return 'v3'
    if perf == list(mm.PERFILES_V5) and tipos == list(mm.TIPOS_V11):
        return 'v5'
    if perf == list(mm.PERFILES_DEFECTO) and tipos == list(mm.TIPOS_V11):
        return 'v11'
    return 'sin_modo'


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
        t.appendRow([k + 1, red, rad, prof, mm.MODOS_DEFECTO[k], '%g' % mm.CAPACIDAD_DEFECTO[k],
                     '%g' % mm.PUMP_REL_DEFECTO[k], mm.TIPOS_DEFECTO[k], mm.ROLES_DEFECTO[k]])


def anadir_columnas(t, mm):
    """Una tabla editada a mano antes de la v12 o de la v13: se conserva
    todo y se le anaden las columnas que le falten (modo, capacidad y
    pump_rel) con los valores por defecto (bombo x3 y 0,20 s, tom x2 y
    0,12 s, en impulso), detras de profundidad. Devuelve las anadidas."""
    filas = filas_tabla(t)
    cab = [str(x).strip() for x in filas[0]]
    ip = cab.index('pad') if 'pad' in cab else None
    pads = []
    for f in filas[1:]:
        try:
            pads.append(int(float(f[ip])) - 1 if ip is not None else -1)
        except Exception:
            pads.append(-1)
    defecto = dict(modo=lambda k: mm.MODOS_DEFECTO[k] if 0 <= k < 8 else 'erosion',
                   capacidad=lambda k: '%g' % mm.CAPACIDAD_DEFECTO[k] if 0 <= k < 8 else '1',
                   pump_rel=lambda k: '%g' % mm.PUMP_REL_DEFECTO[k] if 0 <= k < 8 else '0.15')
    cuerpo = [list(f) + [''] * (len(cab) - len(f)) for f in filas[1:]]
    nuevas, ancla = [], 'profundidad'
    for col in ('modo', 'capacidad', 'pump_rel'):
        if col not in cab:
            donde = cab.index(ancla) + 1 if ancla in cab else len(cab)
            cab.insert(donde, col)
            for f, k in zip(cuerpo, pads):
                f.insert(donde, defecto[col](k))
            nuevas.append(col)
        ancla = col
    t.clear()
    t.appendRow(cab)
    for f in cuerpo:
        t.appendRow(f)
    return nuevas


tabla = base.op('perfiles_erosion')
if tabla is None:
    tabla = mk(base, 'tableDAT', 'perfiles_erosion', -660, 80)
    escribir_perfiles(tabla, motor.module)
    ok('perfiles_erosion: reduccion en notas; bombo x3 y tom x2 en impulso, la caja corta. Editala a mano')
else:
    estado = clasificar_perfiles(filas_tabla(tabla), motor.module)
    if estado in ('v1', 'v3', 'v5', 'v11', 'v12'):
        escribir_perfiles(tabla, motor.module)
        ok('perfiles_erosion: tenia los valores de la %s, sustituidos (bombo x3 y tom x2 en '
           'impulso; columnas modo, capacidad y pump_rel)' % estado)
    elif estado == 'nueva':
        ok('perfiles_erosion: ya tiene los valores nuevos')
    elif estado in ('sin_modo', 'sin_pump'):
        nuevas = anadir_columnas(tabla, motor.module)
        poner_roles(tabla, motor.module)
        info('perfiles_erosion editada a mano: se conserva y se le anade %s (bombo x3 y 0,20 s, '
             'tom x2 y 0,12 s, en impulso; el resto, erosion). Para que un pad vuelva a erosionar, '
             'pon erosion en su modo' % ', '.join(nuevas))
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

leeme(base, 7, """FASE 7 - EROSION E IMPULSO
  8 pads de bateria (Canaldrum 16, desde Notabase) = 8 perfiles editables
  en perfiles_erosion:
    reduccion    notas de construccion que deshace en la celda
    radio        anillos de vecinas (cada anillo, la mitad)
    profundidad  conchas que corta (fase 9)
    modo         erosion / impulso (v12)
    capacidad    multiplicador de capacidad de un impulso
  IMPULSO (bombo x3 y tom x2): no destruye. La celda golpeada se porta como
  si fuera cap veces mas grande (limite de altura y umbrales x cap) y se
  hincha al golpe, en seco (pumping: pico al instante, Pumphold s en el
  pico y caida de pump_rel s por pad; Pumpamt, Pumphorz, Pumpvelmin,
  Pumpon). Capmodo decae (vuelve a 1 tras Capdur pasos sin golpes;
  lo construido se queda) o sostenido (hasta el entierro).
  Erosionvel: la tabla vale a velocidad Velref (100) y escala con la del
  golpe; como minimo, una nota por golpe.
  Una nota de erosion deshace lo que hizo una nota del SEQ: baja la carga
  y la altura; al agotarse la carga, baja un escalon. Orden: satelites,
  altura, huella.
  Perfiles del usuario: 1 bombo impulso x3, 2 caja (-15, radio 1, corta 3),
  3 tom impulso x2, 4-8 aranazos.
  El golpe se ve como una nota: el centro de la celda y la formacion con
  el color de su pad (colores_drum), en las celdas que erosiona; se apaga
  en Vidabalizadrum s. Luzdrum: intensidad.
  Presupuesto: por encima de Umbraldensidad, radios x Multradio.
  Prueba: Padprueba + Erosionar.""")

print_report()


def prueba(t):
    import math
    m = t.m
    m.reset_world()
    c = m.cfg()
    c['nivel'] = min(c['nivel'], 13)              # desde la fase 14 un aranazo es tambien un accidente
    for k in range(16):                           # limite + 2 desbordes
        t.midi(0x9C, 0x40, 0x64)
    W = m.world()
    i = m.note_cell(64)
    sats0 = sum(W['occ'][j] for j in m.satellites_of(W, i))
    occ0 = W['occ'][i]
    c['perfiles'] = [(1, 0, 0)] * 8
    c['modos'] = ['erosion'] * 8                   # todos erosionan (v12: el bombo es impulso)
    c['target_mode'], c['erosion_vel'] = 0, 0
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
    e1 = W['ev'].get('erosion', {})
    t.check('pad 1 (bombo) por MIDI -> impulso: la celda queda con capacidad 3',
            W['hits'].get(3, 0) == 1 and e1.get('modo') == 'impulso'
            and W['cap'][e1['celda']] == 3.0, str(e1.get('modo')))
    t.midi(0x90 + chd - 1, nb + 1, 0x64)
    t.check('pad 2 (caja) por MIDI -> erosion',
            W['hits'].get(3, 0) == 2 and W['ev']['erosion'].get('modo') == 'erosion')
    cf = m.cfg()
    t.check('perfiles leidos de la tabla, con modo y capacidad',
            len(cf['perfiles']) == 8 and len(cf['tipos']) == 8
            and cf['modos'] == list(m.MODOS_DEFECTO) and cf['capacidades'] == list(m.CAPACIDAD_DEFECTO),
            '%s %s' % (cf['modos'], cf['capacidades']))
    cd = dict(m.cfg())
    cd['nivel'] = min(cd['nivel'], 13)            # la erosion de la fase 7, sin los accidentes de la 14
    cd['perfiles'], cd['tipos'] = list(m.PERFILES_DEFECTO), list(m.TIPOS_DEFECTO)
    cd['target_mode'], cd['balizas_drum'], cd['luz_drum'] = 0, 1, 1.0
    cd['erosion_vel'] = 0               # las pruebas de siempre, sin velocidad
    v1 = [COLS_V11[:5]] + [[k + 1] + list(m.PERFILES_V1[k]) + [m.TIPOS_V1[k]] for k in range(8)]
    v3 = [COLS_V11[:5]] + [[k + 1] + list(m.PERFILES_V3[k]) + [m.TIPOS_V11[k]] for k in range(8)]
    ed = [COLS_V11[:5]] + [[k + 1, 2, 2, 0, 'aranazo'] for k in range(8)]
    v5 = [COLS_V11[:5]] + [[k + 1] + list(m.PERFILES_V5[k]) + [m.TIPOS_V11[k]] for k in range(8)]
    v11 = [COLS_V11] + [[k + 1] + list(m.PERFILES_DEFECTO[k]) + [m.TIPOS_V11[k], m.ROLES_DEFECTO[k]]
                        for k in range(8)]
    v12 = [COLS_V12] + [[k + 1] + list(m.PERFILES_DEFECTO[k]) + [m.MODOS_DEFECTO[k], m.CAPACIDAD_DEFECTO[k],
                                                                 m.TIPOS_DEFECTO[k], m.ROLES_DEFECTO[k]]
                        for k in range(8)]
    nueva = [COLS] + [[k + 1] + list(m.PERFILES_DEFECTO[k])
                      + [m.MODOS_DEFECTO[k], m.CAPACIDAD_DEFECTO[k], m.PUMP_REL_DEFECTO[k],
                         m.TIPOS_DEFECTO[k], m.ROLES_DEFECTO[k]] for k in range(8)]
    ed12 = [list(f) for f in v12]
    ed12[1][4] = 'erosion'                          # en la v12, el bombo vuelve a erosionar, a mano
    ed13 = [list(f) for f in nueva]
    ed13[1][6] = 0.3                                # en la v13, el bombo cae mas despacio
    t.check('tabla v1, v3, v5, v11 o v12 sin editar -> se sustituye; editada antes de la v12 o de '
            'la v13 -> se le anade lo que falte; editada despues -> se conserva',
            clasificar_perfiles(v1, m) == 'v1' and clasificar_perfiles(v3, m) == 'v3'
            and clasificar_perfiles(v5, m) == 'v5' and clasificar_perfiles(v11, m) == 'v11'
            and clasificar_perfiles(v12, m) == 'v12' and clasificar_perfiles(ed, m) == 'sin_modo'
            and clasificar_perfiles(ed12, m) == 'sin_pump' and clasificar_perfiles(nueva, m) == 'nueva'
            and clasificar_perfiles(ed13, m) == 'editada')
    ft = FakeTabla(ed)
    anadidas = anadir_columnas(ft, m)
    t.check('tabla editada antes de la v12: conserva sus numeros y gana modo, capacidad y pump_rel',
            anadidas == ['modo', 'capacidad', 'pump_rel']
            and ft.filas[0][:7] == ['pad', 'reduccion', 'radio', 'profundidad', 'modo', 'capacidad', 'pump_rel']
            and [f[4] for f in ft.filas[1:]] == list(m.MODOS_DEFECTO)
            and [float(f[6]) for f in ft.filas[1:]] == list(m.PUMP_REL_DEFECTO)
            and all(f[1:4] == ['2', '2', '0'] for f in ft.filas[1:]), str(ft.filas[:2]))
    ft12 = FakeTabla(ed12)
    anadidas = anadir_columnas(ft12, m)
    t.check('tabla editada en la v12: conserva su modo y gana pump_rel detras de capacidad',
            anadidas == ['pump_rel'] and ft12.filas[0] == COLS and ft12.filas[1][4] == 'erosion'
            and [float(f[6]) for f in ft12.filas[1:]] == list(m.PUMP_REL_DEFECTO), str(ft12.filas[:2]))
    # luz de celda: colores dibujados en el centro de una celda
    def centro_de(Wx, cx, now, celda):
        nn = m.normal_i(celda)
        out = []
        for f in m.cell_lights(Wx, cx, now):
            p = f[:3]
            r = math.sqrt(sum(v * v for v in p))
            if r > 0 and sum(p[q] / r * nn[q] for q in range(3)) > 0.9999:
                out.append(tuple(round(v, 3) for v in f[9:12]))
        return out
    redondo = lambda col: tuple(round(v, 3) for v in col)

    def tinte_formacion(Wx, cx, now, celda):
        """Color de la pieza principal de la formacion de la celda (en caja:
        desde la fase 11 la formacion es un modelo del tema)."""
        Wx['vh'] = list(Wx['h'])
        cx = dict(cx)
        cx['nivel'] = min(cx['nivel'], 10)
        inst = m.build_instances(Wx, cx, now)
        nn = m.normal_i(celda)
        mejor = None
        for f in inst['formas_pulidas'] + inst['formas_porosas']:
            p = f[:3]
            r = math.sqrt(sum(v * v for v in p))
            if r > 0 and sum(p[q] / r * nn[q] for q in range(3)) > 0.9999:
                mejor = f[9:12]
                break
        return mejor
    # 1. un golpe ilumina el centro de la celda y la formacion con el color del pad
    W3 = m.new_world()
    for k in range(4):
        m.note_on(W3, cd, 1, 64, 100, 0.0)
    sin_golpe = tinte_formacion(W3, cd, 2.05, i)
    m.light_cell(W3, cd, i, 1, 1.0, 2.0)            # caja, magenta
    col_caja = m.drum_color(cd, 1)
    centro = centro_de(W3, cd, 2.01, i)
    con_golpe = tinte_formacion(W3, cd, 2.01, i)
    acerca = lambda c_: sum(abs(c_[q] - col_caja[q]) for q in range(3))
    t.check('golpe: el centro de la celda con el color del pad, como una nota',
            len(centro) == 1 and acerca(centro[0]) < 0.05, str(centro))
    t.check('golpe: la formacion se tine del color del pad, como con una nota',
            con_golpe is not None and acerca(con_golpe) < acerca(sin_golpe) - 0.2,
            '%s -> %s' % (sin_golpe and [round(v, 2) for v in sin_golpe],
                          con_golpe and [round(v, 2) for v in con_golpe]))
    bien, det = instance_color_ok(base.op('luz_celda'))
    t.check('luz_celda pinta el color de cada instancia (lo que se dibuja)', bien, det)
    # 2. en la celda del SEQ1: el golpe manda mientras dura; despues vuelve el SEQ1
    W3s = m.new_world()
    m.note_on(W3s, cd, 1, 64, 100, 5.0)
    m.note_off(W3s, cd, 1, 64, 5.05, 120.0)
    m.light_cell(W3s, cd, i, 6, 1.0, 6.0)           # charles en reposo del SEQ1
    durante = centro_de(W3s, cd, 6.01, i)
    despues = centro_de(W3s, cd, 6.0 + cd['vida_baliza_drum'] + 0.01, i)
    t.check('golpe en la celda del SEQ1: se ve el pad; al apagarse, vuelve el SEQ1',
            len(durante) == 1 and len(despues) == 1
            and sum(abs(durante[0][q] - m.drum_color(cd, 6)[q]) for q in range(3)) < 0.1
            and sum(abs(despues[0][q] - m.seq_color(cd, 1)[q] * 0.7) for q in range(3)) < 0.1,
            '%s / %s' % (durante, despues))
    t.check('sin otras senales de bateria: una sola loseta por celda, sin borde',
            len(m.cell_lights(W3s, cd, 6.01)) == 1 and not hasattr(m, 'PAD_DIRS'))
    # 3. un golpe: la celda a plena luz, el radio mas tenue, y se apaga
    W3b = m.new_world()
    m.note_on(W3b, cd, 1, 64, 100, 0.0)
    cd_e = dict(cd, modos=['erosion'] * 8)          # el bombo en modo erosion: radio 2
    ev = m.erosion(W3b, cd_e, 0, 1, 2.0)
    nivel = {c_: m.drum_light(W3b, cd_e, c_, 2.05)[0] for c_ in W3b['luz']}
    anillos = dict(m.rings(ev['celda'], 2))
    a1 = [nivel[x] for x, d in anillos.items() if d == 1 and x in nivel]
    a2 = [nivel[x] for x, d in anillos.items() if d == 2 and x in nivel]
    t.check('el golpe ilumina la celda y su radio, mas tenue al alejarse',
            nivel.get(ev['celda'], 0) > max(a1) > max(a2) > 0, '%d celdas' % len(nivel))
    t.check('se apaga en Vidabalizadrum',
            not m.cell_lights(dict(W3b, last={1: None, 2: None}), cd,
                              2.0 + cd['vida_baliza_drum'] + 1e-3))
    # 4. se ve con formacion, vacia y con huella
    W5 = m.new_world()
    for k in range(6):
        m.note_on(W5, cd, 1, 60, 100, 0.0)          # con formacion
    m.note_on(W5, cd, 1, 62, 100, 0.0)
    hu = m.note_cell(62)
    m.degrade(W5, cd, hu, 1)                        # huella
    W5['last'] = {1: None, 2: None}
    vacia = m.note_cell(70)
    vis = True
    for celda in (m.note_cell(60), hu, vacia):
        m.light_cell(W5, cd, celda, 1, 1.0, 4.0)
        cc = centro_de(W5, cd, 4.01, celda)
        vis = vis and len(cc) == 1 and acerca(cc[0]) < 0.1
    t.check('la luz se ve con formacion, vacia y con huella', vis and W5['huella'][hu] > 0)
    t.check('corta la caja (pad 2); el bombo y el tom (1 y 3) son impulso',
            m.pads_corte(cd) == [1] and m.pads_impulso(cd) == [0, 2]
            and not m.es_aranazo(cd, 0) and not m.es_aranazo(cd, 2) and m.es_aranazo(cd, 3))
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
    # velocidad
    cv = dict(cd)
    cv['erosion_vel'], cv['vel_ref'] = 1, 100
    W9 = m.new_world()
    for k in range(30):
        m.note_on(W9, cv, 1, 64, 100, 0.0)
        m.note_on(W9, cv, 1, 50, 100, 0.0)
    W10 = {k_: (list(v) if isinstance(v, list) else v) for k_, v in W9.items()}
    W10['ero_resto'] = list(W9['ero_resto'])
    fuerte = m.erosion(W9, cv, 3, 127, 6.0)['notas']   # pad 4: 3 notas a Velref
    flojo = m.erosion(W10, cv, 3, 40, 6.0)['notas']
    t.check('con Erosionvel, un golpe fuerte deshace mas notas que uno flojo',
            fuerte > flojo and abs(m.erosion_notes(cv, 3, 100) - 3) < 1e-9,
            '%.2f / %.2f notas' % (fuerte, flojo))
    t.check('el minimo (una nota) se respeta con velocidad 1',
            m.erosion_notes(cv, 15, 1) == 1.0 and m.erosion_notes(cv, 1, 1) == 1.0)
    cv0 = dict(cv)
    cv0['erosion_vel'] = 0
    t.check('sin Erosionvel la velocidad no cambia nada',
            m.erosion_notes(cv0, 3, 1) == 3 and m.erosion_notes(cv0, 3, 127) == 3)
    totales = []
    for r_ in range(2):
        Wn = m.new_world()
        for k in range(20):
            m.note_on(Wn, cv, 1, 64, 100, 0.0)
        quitado = 0
        for k in range(8):
            quitado += m.erosion(Wn, cv, 3, 61, 7.0 + k)['quitado']   # 61 % 3 = 1: sin desplazar
        totales.append(quitado)
    r60 = m.erosion_notes(cv, 3, 61)
    t.check('N golpes iguales deshacen siempre lo mismo, sin perder fracciones',
            totales[0] == totales[1] and totales[0] >= int(8 * r60 * 1.0),
            '%s notas (%.2f por golpe en la celda)' % (totales, r60))
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
    t.check('Padprueba + Erosionar iluminan la celda', k in W['drum'] and W['luz'])
    t.check('leyenda IMPULSO (pad 1) y MUNDO con cap+',
            'IMPULSO  pad 1 x3 celda' in m.legend() and 'cap+ 1' in m.legend(), m.legend()[:200])
    base.par.Padprueba = 4
    m.on_pulse('Erosionar')
    base.par.Padprueba = 1
    cian, ambar, blanco = (0.10, 0.90, 1.00), (1.0, 0.7, 0.3), (0.95, 0.95, 0.92)
    t.check('ningun color es cian, ambar ni blanco',
            all(sum(abs(a - b) for a, b in zip(col, ref)) > 0.3
                for col in cd['colores_drum'] for ref in (cian, ambar, blanco)))
    geo = base.op('luz_celda')
    t.check('luz_celda gira y se balancea con el planeta',
            geo is not None and 'rotation(' in (geo.par.ry.expr or '')
            and 'wobble(' in (geo.par.rx.expr or ''))
    t.check('leyenda EROSION (pad 4)', 'EROSION' in m.legend() and 'IMPULSO' not in m.legend())
    prueba_impulso(t, m, cd)


class FakeTabla(object):
    """Lo justo de una tableDAT para probar anadir_columnas."""

    def __init__(self, filas):
        self.filas = [[str(x) for x in f] for f in filas]

    @property
    def numRows(self):
        return len(self.filas)

    @property
    def numCols(self):
        return max(len(f) for f in self.filas)

    def __getitem__(self, rc):
        r, c = rc
        f = self.filas[r]
        if c >= len(f):
            return None

        class _C(object):
            val = f[c]
        return _C()

    def clear(self):
        self.filas = []

    def appendRow(self, f):
        self.filas.append([str(x) for x in f])


def prueba_impulso(t, m, cd):
    """Las pruebas del impulso (v12): bombo y tom amplian la capacidad de
    la celda y la hinchan al golpe (v13: en seco)."""
    import math
    c = dict(cd)
    c.update(target_mode=0, erosion_vel=0, cap_modo=0, cap_dur=16, pump_amt=1.0, pump_horz=0.30,
             pump_hold=0.04, pump_velmin=0.6, pump_rels=list(m.PUMP_REL_DEFECTO), pump_on=1)
    paso = m.step_dur(c, 120.0)
    i = m.note_cell(64)
    lim = m.limit(c)

    def mundo(notas=0, t0=0.0):
        Wx = m.new_world()
        Wx['paso'] = paso
        for k in range(notas):
            m.note_on(Wx, c, 1, 64, 100, t0)
        return Wx
    # 1. no resta ocupacion, no deja huella ni corte (ni con conchas, en la fase 9)
    c9 = dict(c, nivel=9)
    W1 = mundo()
    for g in range(2):
        m.note_on(W1, c9, 1, 64, 100, 0.0)
        m.end_cycle(W1, c9, 0.5 + g)
    for k in range(8):
        m.note_on(W1, c9, 1, 64, 100, 3.0)
    antes = (list(W1['occ']), list(W1['carga']), list(W1['h']), list(W1['huella']),
             [len(x) for x in W1['cols']], dict(W1['scars']))
    ev = m.erosion(W1, c9, 0, 100, 4.0)
    ev3 = m.erosion(W1, c9, 2, 100, 4.1)
    despues = (list(W1['occ']), list(W1['carga']), list(W1['h']), list(W1['huella']),
               [len(x) for x in W1['cols']], dict(W1['scars']))
    t.check('impulso: no resta ocupacion, no deja huella ni corte',
            antes == despues and ev['modo'] == ev3['modo'] == 'impulso' and ev['quitado'] == 0
            and 'corte' not in ev and ev['celda'] == i)
    Wl = mundo()
    for n in range(96):
        m.note_on(Wl, c, 1, n, 100, 0.0)
    occ0 = list(Wl['occ'])
    evl = m.erosion(Wl, c, 0, 100, 1.0)
    t.check('impulso: no entra en el presupuesto de densidad (radio 0, Multradio no le afecta)',
            not evl['doble'] and evl['rad'] == 0 and list(Wl['occ']) == occ0
            and list(Wl['luz']) == [evl['celda']])
    # 2. con cap 3 sube hasta 3 veces el limite y no se desborda antes de ocupacion 12
    W2 = mundo(1)
    m.erosion(W2, c, 0, 100, 0.0)
    primero, hmax = None, 0.0
    for k in range(120):
        r = m.note_on(W2, c, 1, 64, 100, 0.01)
        hmax = max(hmax, W2['h'][i])
        if r.get('desborde') is not None and primero is None:
            primero = W2['occ'][i]
    t.check('cap 3: la formacion sube hasta 3 x el limite y no se desborda antes de ocupacion 12',
            primero is not None and primero >= 12 and abs(hmax - 3.0 * lim) < 1e-6,
            'primer desborde con ocupacion %s, altura %.2f de %.2f' % (primero, hmax, 3.0 * lim))
    W2b = mundo(1)
    hb = 0.0
    for k in range(40):
        m.note_on(W2b, c, 1, 64, 100, 0.01)
        hb = max(hb, W2b['h'][i])
    t.check('... sin impulso, la de siempre: limite x 1 y desborde desde %d' % c['th_branch'],
            abs(hb - lim) < 1e-6 and m.satellites_of(W2b, i))
    # 3. bombo + tom en la misma celda: cap 3, no 6 ni 2
    caps = []
    for orden in ((0, 2), (2, 0), (0, 0)):
        W3 = mundo(1)
        for k, pad in enumerate(orden):
            m.erosion(W3, c, pad, 100, 0.1 * k)
        caps.append(W3['cap'][i])
    t.check('bombo + tom en la misma celda -> cap 3 (ni 6 ni 2); dos bombos, 3', caps == [3.0, 3.0, 3.0],
            str(caps))
    # 4. decae: tras Capdur pasos sin golpes, cap 1 y la altura no baja
    W4 = mundo(1)
    m.erosion(W4, c, 0, 100, 0.0)
    for k in range(30):
        m.note_on(W4, c, 1, 64, 100, 0.01)
    o4, h4 = W4['occ'][i], W4['h'][i]
    t_fin = c['cap_dur'] * paso
    m.tick(W4, c, t_fin - 0.05, 120.0, True)
    sigue = W4['cap'][i]
    m.tick(W4, c, t_fin + 0.01, 120.0, True)
    h4b = W4['h'][i]
    des = None
    for k in range(12):
        r = m.note_on(W4, c, 1, 64, 100, t_fin + 0.02)
        des = des or r.get('desborde')
    t.check('decae: tras Capdur pasos sin golpes la capacidad vuelve a 1 y la altura no baja; '
            'la siguiente nota que dispara se desborda',
            sigue == 3.0 and W4['cap'][i] == 1.0 and o4 > c['th_branch'] and h4 > lim
            and abs(h4b - h4) < 1e-9 and W4['h'][i] >= h4 - 1e-9 and des is not None,
            'ocupacion %d, altura %.2f -> %.2f -> %.2f (limite %.2f)' % (o4, h4, h4b, W4['h'][i], lim))
    cs = dict(c, cap_modo=1)
    W4s = mundo(1)
    m.erosion(W4s, cs, 0, 100, 0.0)
    m.tick(W4s, cs, 10 * t_fin, 120.0, True)
    t.check('sostenido: la capacidad se queda', W4s['cap'][i] == 3.0)
    W4r = mundo(1)
    m.erosion(W4r, c, 0, 100, 0.0)
    m.erosion(W4r, c, 2, 100, t_fin * 0.75)         # el tom renueva la duracion
    m.tick(W4r, c, t_fin + 0.01, 120.0, True)
    t.check('cada golpe renueva la duracion', W4r['cap'][i] == 3.0)
    # 5. golpe en una celda vacia
    W5 = mundo()
    W5['last'][1] = dict(note=64, cell=i, t=0.0, vel=100)
    try:
        ev5 = m.erosion(W5, c, 0, 100, 0.0)
        bien5 = ev5['vacia'] and W5['cap'][i] == 3.0 and W5['occ'][i] == 0 and i in W5['luz']
        m.build_instances(W5, dict(c, nivel=10), 0.01)
    except Exception as e_:
        bien5 = False
        ev5 = e_
    t.check('golpe en celda vacia: fija cap sin error y se ve su color', bien5, str(ev5)[:80])
    # 6. pumping en seco (v13)
    c10 = dict(c, nivel=10)

    def golpe(Wx, pad, vel, t0, fps, fotos, cx=c10):
        """Golpe en t0 y 'fotos' fotogramas a 'fps': [(t, escala vertical)]."""
        m.tick(Wx, cx, t0 - 1.0 / fps, 120.0, True)
        m.erosion(Wx, cx, pad, vel, t0)
        out, tt = [], t0
        for _ in range(fotos):
            tt += 1.0 / fps
            m.tick(Wx, cx, tt, 120.0, True)
            out.append((tt, m.escalas_bomba(Wx, cx, i, tt)[0]))
        return out
    serie = golpe(mundo(6), 0, 127, 1.0, 30.0, 12)
    t.check('pumping 1: el pico (x3 el bombo) en el primer fotograma tras el golpe, sin valores intermedios',
            abs(serie[0][1] - 3.0) < 1e-12, '%s' % [round(v, 3) for _, v in serie])
    en_pico = {}
    for fps in (30.0, 60.0, 120.0):
        sr = golpe(mundo(6), 0, 127, 1.0, fps, int(fps))
        k = 0
        while k < len(sr) and abs(sr[k][1] - 3.0) < 1e-12:
            k += 1
        en_pico[fps] = k
    t.check('pumping 2: el pico dura al menos 2 fotogramas (y Pumphold, 0,04 s)',
            all(k >= 2 and k >= int(0.04 * fps) for fps, k in en_pico.items()), str(en_pico))
    W6 = mundo(6)
    sr = golpe(W6, 0, 127, 1.0, 240.0, 120)
    b = None
    W6b = mundo(6)
    golpe(W6b, 0, 127, 1.0, 240.0, 2)
    b = dict(W6b['bomba'][i])
    fin = max(b['t0'] + b['hold'], b['t2'])
    esc = lambda tt: m.escalas_bomba(W6b, c10, i, tt)[0]
    cub = all(abs(esc(fin + x * b['rel']) - (1 + 2.0 * (1 - x) ** 3)) < 1e-9 for x in (0.1, 0.5, 0.9))
    t.check('pumping 3: cae como 1 + (pico - 1)(1 - t / pump_rel)^3, llega a 1 justo en pump_rel '
            '(0,20 s el bombo) y nunca baja de 1',
            abs(b['rel'] - 0.20) < 1e-12 and cub and esc(fin + b['rel']) == 1.0 and esc(fin + b['rel'] - 1e-6) > 1.0
            and min(v for _, v in sr) >= 1.0 and sr[-1][1] == 1.0 and i not in W6['bomba'],
            'caida %.3f s' % b['rel'])
    W6r = mundo(6)
    golpe(W6r, 0, 127, 1.0, 60.0, 9)                # el bombo, ya cayendo
    antes_r = m.escalas_bomba(W6r, c10, i, 1.15)[0]
    m.erosion(W6r, c10, 0, 127, 1.15)
    m.tick(W6r, c10, 1.15 + 1 / 60.0, 120.0, True)
    t.check('pumping 4: un golpe durante la caida salta otra vez al pico en el fotograma siguiente',
            1.0 < antes_r < 3.0 and m.escalas_bomba(W6r, c10, i, 1.15 + 1 / 60.0)[0] == 3.0,
            '%.3f -> %.3f' % (antes_r, m.escalas_bomba(W6r, c10, i, 1.15 + 1 / 60.0)[0]))
    # 5. rafaga de semicorcheas a 200 BPM (paso 0,075 s) a 120 fps
    c200 = dict(c10)
    paso200 = m.step_dur(c200, 200.0)
    Wq = mundo(6)
    Wq['paso'] = paso200
    fps = 120.0
    tt = 2.0
    m.tick(Wq, c200, tt - 1 / fps, 200.0, True)
    vuelve, rels = [], []
    for k in range(4):
        t0 = 2.0 + k * paso200
        while tt < t0 - 1e-9:
            tt += 1 / fps
            m.tick(Wq, c200, tt, 200.0, True)
            if k and tt < t0 - 1e-9:
                ultima = m.escalas_bomba(Wq, c200, i, tt)[0]
        if k:
            vuelve.append(ultima)
        m.erosion(Wq, c200, 0, 127, t0)
        rels.append(Wq['bomba'][i]['rel'])
    sostiene = max(0.04, 2.0 / fps)
    t.check('pumping 5: en una rafaga de pasos cortos, desde el segundo golpe la caida se recorta a '
            '0,8 x el paso (menos el pico) y la celda vuelve a 1 antes del siguiente; el primero (que '
            'no sabe que viene otro) ya ha bajado cuando llega el segundo',
            abs(rels[0] - 0.20) < 1e-12 and all(abs(r - (0.8 * paso200 - sostiene)) < 1e-6 for r in rels[1:])
            and 1.0 < vuelve[0] < 3.0 and all(v == 1.0 for v in vuelve[1:]), 'caidas %s, antes de cada golpe %s'
            % ([round(r, 3) for r in rels], [round(v, 3) for v in vuelve]))
    flojo = golpe(mundo(6), 0, 1, 1.0, 30.0, 1)[0][1]
    tom = golpe(mundo(6), 2, 127, 1.0, 30.0, 1)[0][1]
    Wt = mundo(6)
    golpe(Wt, 2, 127, 1.0, 30.0, 1)
    t.check('pumping 6: a velocidad minima, el pico es 1 + (pico - 1) x 0,6; el tom, x2 y mas corto (0,12 s)',
            abs(flojo - (1 + 2.0 * 0.6)) < 1e-12 and abs(tom - 2.0) < 1e-12
            and abs(Wt['bomba'][i]['rel'] - 0.12) < 1e-12, 'flojo %.3f, tom %.3f' % (flojo, tom))
    Wh = mundo(6)
    Wh['vh'] = list(Wh['h'])
    h0, vh0 = list(Wh['h']), list(Wh['vh'])
    golpe(Wh, 0, 127, 1.0, 30.0, 4)
    t.check('pumping 7: la altura real (y la que se ve antes del pumping) no cambia',
            Wh['h'] == h0 and Wh['vh'] == vh0)
    Wb = mundo(6)
    Wb['vh'] = list(Wb['h'])
    sin = m.build_instances(Wb, c10, 0.9)
    golpe(Wb, 0, 127, 1.0, 30.0, 12)
    Wb['luz'] = {}                                  # sin la luz del pad, solo el pumping
    tras = m.build_instances(Wb, c10, 1.4)
    claves = ('formas_pulidas', 'formas_porosas', 'coronas')
    igual = all([[round(x, 9) for x in f] for f in sin[k]] == [[round(x, 9) for x in f] for f in tras[k]]
                for k in claves)
    t.check('pumping: acabado, lo dibujado vuelve exactamente a como estaba', igual and not Wb['bomba'])

    def filas_celda(inst, celda):
        out = []
        for k in claves:
            for f in inst[k]:
                p = f[:3]
                if max(range(m.N), key=lambda x: sum(p[q] * m.normal_i(x)[q] for q in range(3))) == celda:
                    out.append(f)
        return out

    def extension(f, celda, Wx):
        n = m.normal_i(celda)
        e, tt = m.tangents(n)
        b = m.base_radius(Wx, c10, celda)
        p0 = [n[q] * b for q in range(3)]
        rel = [f[q] - p0[q] for q in range(3)]
        lado = max(0.5 * abs(f[6]), 0.5 * abs(f[8]))
        cw, cl = m._cell_sizes(b, celda)
        return (abs(sum(rel[q] * e[q] for q in range(3))) + lado) / (0.5 * cw), \
            (abs(sum(rel[q] * tt[q] for q in range(3))) + lado) / (0.5 * cl)
    peor = []
    for tema_arq in (False, True):
        Wp = mundo()
        for k in range(10):
            m.note_on(Wp, c10, 2 if tema_arq else 1, 64, 100, 0.0)
        Wp['vh'] = list(Wp['h'])
        Wp['lat'] = [-99.0] * m.N
        Wp['pend'] = {}
        base_f = filas_celda(m.build_instances(Wp, c10, 5.0), i)
        m.erosion(Wp, c10, 0, 127, 5.0)
        Wp['luz'] = {}
        hin = filas_celda(m.build_instances(Wp, c10, 5.0), i)     # el pico, en el mismo instante
        for f0, f1 in zip(base_f, hin):
            x0, x1 = extension(f0, i, Wp), extension(f1, i, Wp)
            peor.append(max(x1[0] - max(1.0, x0[0]), x1[1] - max(1.0, x0[1])))
        alto0 = max(abs(f[7]) for f in base_f)
        alto1 = max(abs(f[7]) for f in hin)
        peor.append(0.0 if abs(alto1 - 3.0 * alto0) < 1e-6 else 9.0)
    t.check('pumping 8: con Pumphorz 0,30 ninguna pieza pasa del ancho de su celda; crece x3 en altura',
            peor and max(peor) <= 1e-6, 'exceso %.4f' % max(peor or [9]))
    c_off = dict(c10, pump_on=0)
    Woff = mundo(6)
    m.erosion(Woff, c_off, 0, 127, 1.0)
    t.check('Pumpon apagado: sin pumping', m.escalas_bomba(Woff, c_off, i, 1.0) == (1.0, 1.0))
    # la luz: el color del pad sin tapar el del secuenciador
    W8 = mundo(3)
    W8['vh'] = list(W8['h'])
    m.note_on(W8, c10, 1, 64, 100, 6.0)
    m.erosion(W8, c10, 0, 100, 6.0)
    cent = [f for f in m.cell_lights(W8, c10, 6.01)
            if sum(f[q] * m.normal_i(i)[q] for q in range(3)) > 0.0
            and max(range(m.N), key=lambda x: sum(f[q] * m.normal_i(x)[q] for q in range(3))) == i]
    cols = sorted(tuple(round(v, 2) for v in f[9:12]) for f in cent)
    t.check('la luz del impulso no tapa la del SEQ1: el centro se parte en los dos colores',
            len(cent) == 2, str(cols))
    # 7. el entierro reinicia la capacidad
    c8 = dict(c, nivel=8)
    W7 = mundo(4)
    m.erosion(W7, c8, 0, 100, 0.0)
    m.erosion(W7, c8, 2, 100, 0.0)
    W7['last'][1]['cell'] = m.note_cell(70)
    m.erosion(W7, c8, 0, 100, 0.1)
    n_cap = m.celdas_cap(W7)
    m.end_cycle(W7, c8, 1.0)
    t.check('entierro: la capa nueva empieza con cap 1', n_cap == 2 and m.celdas_cap(W7) == 0
            and not W7['bomba'])


run_test(base, prueba)
print('  Ahora: anade la bateria del BeatStep (canal 16). Cada golpe ilumina las')
print('  celdas que golpea con el color de su pad. El bombo y el tom no destruyen:')
print('  hinchan la celda al golpe y le dan capacidad (x3 y x2), asi que sus')
print('  formaciones suben mas antes de desbordarse; la caja abrira cortes en la fase 9.')
print('  Si los golpes salen como "pad fuera de 1-8", ajusta Notabase.')
print('  Ajusta el equilibrio crecimiento / erosion antes de pasar a la fase 8.')
print('=' * 66)
