"""
=============================================================================
ESTRATOS - FASE 31: LAS ESCISIONES EN EL HISTORICO
=============================================================================
Requiere la fase 30. Ultima fase del plan v5. Cada escision deja un testigo:
una imagen de su seccion, una veta en la columna de la jornada y una linea en
el registro.

QUE HACE
--------
  TESTIGO      cada escision exporta una imagen cuando su fila se deshace o
               cuando se entierra su mundo, lo que ocurra antes, con su
               profundidad final. Una sola vez.
  SECCION      la imagen es un corte del planeta por la celda de origen y dos
               celdas a cada lado de su anillo, desde la superficie hasta la
               ultima concha atravesada. Se dibuja en Python a partir de las
               columnas (numpy, como los mapas del terreno): cada loseta es
               una banda de su color, las bandas humanas con sus motas y la
               escision con su fulgurita (paredes de arena fundida, vidrio,
               nucleo y ramas). Sin un segundo render ni planos de recorte. Se
               guarda con TOP.save() en PNG, un testigo por fotograma como
               mucho.
  COLUMNA      la columna resumen de la jornada: una banda por ciclo (humana
               con motas, limpia, y una franja oscura arriba si cerro por
               colapso), la mas antigua abajo; cada escision es una veta de
               la paleta humana que une las bandas que atraveso, con un ancho
               proporcional a sus personas. Se exporta al cambiar la fecha (y
               con Exportartestigo). El proyector del historico (D5) la
               mostrara.
  REGISTRO     cada escision, con jornada, ciclo, hora, personas, conchas
               cruzadas y celda de origen: en la tabla escisiones (fase 29) y
               en historico/escisiones.csv (UTF-8, separador ; para abrirlo en
               una hoja en espanol), una fila por escision al cerrarse.
               Relanzar no duplica filas.
  JORNADA      la de D5 cuando exista; hasta entonces, la fecha del sistema
               al abrirse la escision.
  LEYENDA      HISTORICO escisiones hoy 3   ultima #3 J2026-11-11 C14 4
               personas 4 conchas celda 40   testigo exportado

OPERADORES (en /project1/FASE1)
-------------------------------
  seccion      Script TOP (640 x 360): la ultima seccion dibujada.
  columna_jornada
               Script TOP (200 x 720): la columna resumen de hoy.
  escisiones   la tabla de la fase 29 (su columna testigo dice el fichero).
  En la carpeta de Carpetahistorico (por defecto, historico/ junto a los
  scripts): escision_<jornada>_c<ciclo>_<id>.png, columna_<jornada>.png y
  escisiones.csv.

PROBAR
------
  Una fila (Simfila 3, Simformarfila), espera 5 s y Simvaciar: aparece
  historico/escision_...png con el pozo en seccion. Otra fila y Forzarciclo
  sin deshacerla: se exporta al enterrar, con su profundidad de ese momento.
  Exportartestigo: la seccion de la ultima escision, como esta ahora, y la
  columna de hoy.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase31_historico.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase31 v1  (escisiones en el historico: testigo en seccion, columna de la jornada y registro)'
banner(VERSION)

base = require_base(31)
motor = install_core(base, CARPETA, 31)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase31)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase31')
add_par(base, page, 'pulse', 'Exportartestigo', 'Exportar el testigo de la ultima escision')
add_par(base, page, 'str', 'Carpetahistorico', 'Carpeta del historico', CARPETA + '/historico')
ok('pagina Fase31: Exportartestigo, Carpetahistorico (%s/historico)' % CARPETA)

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

SECCION_CB = r'''# Script TOP 'seccion' (fase 31): la seccion por el origen de la ultima escision
# exportada. La dibuja el motor con numpy (seccion_escision).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.seccion_cook(scriptOp)
'''

COLUMNA_CB = r'''# Script TOP 'columna_jornada' (fase 31): la columna resumen de la jornada: una
# banda por ciclo y una veta por escision. La dibuja el motor (columna_jornada).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.columna_cook(scriptOp)
'''

X0, Y0 = -660, 1900
for nombre, texto, x in (('seccion', SECCION_CB, X0), ('columna_jornada', COLUMNA_CB, X0 + 220)):
    cb = get_or_make(base, 'textDAT', nombre + '_callbacks', x, Y0 + 140)
    cb.text = texto
    o = get_or_make(base, 'scriptTOP', nombre, x, Y0)
    setp_any(o, ['callbacks', 'callbackdat', 'dat'], nombre + '_callbacks')
    try:
        o.cook(force=True)
    except Exception:
        pass
if base.op('escisiones') is None:
    fail('escisiones: no esta la tabla; aplica antes fase29_fila.py')
ok('seccion y columna_jornada (Script TOP): el testigo de cada escision y la columna de la jornada')
if m._np() is None:
    fail('numpy: no esta; sin el no se dibujan la seccion ni la columna')
carpeta = m.carpeta_historico(m.cfg())
if carpeta:
    ok('historico: %s (escision_<jornada>_c<ciclo>_<id>.png, columna_<jornada>.png, escisiones.csv)' % carpeta)
else:
    info('historico: no puedo crear la carpeta de Carpetahistorico; pon una que exista')

set_render(base)

leeme(base, 31, """FASE 31 - LAS ESCISIONES EN EL HISTORICO
  Cada escision exporta su testigo (una vez) cuando su fila se deshace o
  al enterrar su mundo: la seccion por el origen, dibujada con numpy (las
  columnas en bandas, las humanas con motas, la fulgurita en el hueco), en
  historico/escision_<jornada>_c<ciclo>_<id>.png. La columna de la jornada
  (una banda por ciclo, una veta por escision, tan ancha como sus personas)
  en columna_<jornada>.png. El registro, en la tabla escisiones y en
  escisiones.csv. Exportartestigo, Carpetahistorico.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS31 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Modofila', 'Conchasporpersona', 'Simbalance', 'Colapsoon', 'Temaenciclo',
          'Carpetahistorico', 'Minhuellas', 'Inclusionesmax', 'Colmatacion')


def prueba(t):
    import shutil
    import tempfile
    m = t.m
    guarda, filas = guardar_sala(base, PARS31)
    tmp = tempfile.mkdtemp(prefix='estratos_historico_')
    try:
        _prueba(t, m, tmp)
    finally:
        devolver_sala(base, m, guarda, filas)
        m.hist_reset()
        shutil.rmtree(tmp, ignore_errors=True)


def _prueba(t, m, tmp):
    import os
    np = m._np()
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Colapsoon = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Carpetahistorico = tmp
    reloj = [absTime.seconds + 1100.0]
    tb = base.op('sala_personas')
    DT = 1.0 / m.CAM_FPS

    def nuevo(conchas=8):
        m.reset_world()
        m.sala_reset()
        m.hist_reset()
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        W, c = m.world(), m.cfg()
        for _ in range(conchas):
            m.end_cycle(W, c, reloj[0])
            reloj[0] += 1.0
        return W, c

    def camara(W, c, casillas, seg):
        mx = [m.casilla_xy(c, k) + (1.7,) for k in casillas]
        for _ in range(int(round(seg * m.CAM_FPS))):
            reloj[0] += DT
            m.sala_mundo(W, c, reloj[0], m.tick_personas(W, c, reloj[0], mx))

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)
    k0 = 4 * cols + 3
    linea = [k0, k0 + 1, k0 + 2]

    # 1. el disparo de testigo: una vez, en lo que ocurra antes
    camara(W, c, linea, 5.3)
    e = W['escisiones'][-1]
    abierta = (e.get('testigo'), len(m._HIST['pend']))
    camara(W, c, [], 0.2)                       # la fila se deshace
    deshecha = (e['estado'], e.get('testigo'), len(m._HIST['pend']))
    m.close_cycle(W, c, reloj[0], 'forzado')    # y luego se entierra su mundo: no otra vez
    t.check('una escision abierta no tiene testigo; al deshacerse la fila se dispara; al enterrar despues, '
            'no se repite',
            abierta == (None, 0) and deshecha == ('cerrada', 'pendiente', 1) and len(m._HIST['pend']) == 1
            and m._HIST['pend'][0][0] == e['id'], '%s -> %s' % (abierta, deshecha))
    W, c = nuevo()
    camara(W, c, linea + [k0 + 3], 5.3)
    e2 = W['escisiones'][-1]
    hondo = len(e2['cortadas'])
    m.close_cycle(W, c, reloj[0], 'forzado')    # sin deshacer la fila: se dispara al enterrar
    meta2 = m._HIST['pend'][0][2] if m._HIST['pend'] else {}
    camara(W, c, [], 0.2)
    t.check('una fila que sigue en pie al enterrar: el testigo se dispara al enterrar, con su profundidad de '
            'ese momento (4 conchas), y no otra vez al deshacerse',
            e2['estado'] == 'enterrada' and len(m._HIST['pend']) == 1 and hondo == 4
            and len(meta2.get('bandas', [])) == 5, '%d bandas' % len(meta2.get('bandas', [])))

    # 2. la seccion
    W, c = nuevo()
    origen = m.celda_de_casilla(W, c, linea[0])
    vecinas = [x for x in m.celdas_seccion(origen) if x != origen]
    W['incl'][vecinas[0]] = [[0, 1, 0.0, 0.3], [0, 1, 0.0, 0.7]]      # una banda humana a un lado
    m.end_cycle(W, c, reloj[0])
    camara(W, c, linea, 5.3)
    e = W['escisiones'][-1]
    img, meta = m.seccion_escision(W, c, e)
    bandas = meta['bandas']
    j_vec = meta['celdas'].index(vecinas[1])
    xv = j_vec * meta['columna'] + meta['columna'] // 2
    j_or = meta['celdas'].index(origen)
    xo = j_or * meta['columna'] + meta['columna'] // 2
    bien_color = True
    for b in bandas[1:]:
        ym = (b['y0'] + b['y1']) // 2
        bien_color = bien_color and all(abs(float(img[ym, xv, k]) - b['color'][k]) < 1e-4 for k in range(3))
    orden = [b['concha'] for b in bandas]
    nucleo_col = m.paleta_humana(c, e['ramas'])
    en_hueco = [tuple(round(float(v), 3) for v in img[(b['y0'] + b['y1']) // 2, xo, :3]) for b in bandas[1:]]
    arena = img[(bandas[1]['y0'] + bandas[1]['y1']) // 2, j_or * meta['columna'] + 3, :3]
    humana = img[:, meta['celdas'].index(vecinas[0]) * meta['columna'] + 2:
                 (meta['celdas'].index(vecinas[0]) + 1) * meta['columna'] - 2, :3]
    n_motas = sum(1 for col in m.PALETA_HUMANA_8
                  if bool((np.abs(humana - np.array(col, dtype=np.float32)).max(axis=2) < 1e-3).any()))
    t.check('la seccion tiene tantas bandas como conchas cruzo la escision mas una de superficie, en el orden '
            'de la columna (de arriba abajo), con los colores de la paleta',
            img.shape == (m.SECCION_PX[1], m.SECCION_PX[0], 4) and len(bandas) == len(e['cortadas']) + 1 == 4
            and orden == ['superficie'] + list(e['cortadas']) and e['cortadas'] == sorted(e['cortadas'], reverse=True)
            and bien_color and all(bandas[k]['y1'] <= bandas[k + 1]['y0'] + 1 for k in range(1, len(bandas) - 1)),
            str(orden))
    t.check('en el hueco, la fulgurita: el nucleo de la paleta humana en el centro y la pared de arena fundida '
            'en el borde; a los lados, las columnas vecinas; la banda humana, con sus motas',
            all(all(abs(v - n_) < 2e-3 for v, n_ in zip(px, nucleo_col)) for px in en_hueco)
            and abs(float(arena[0]) - float(arena[2])) > 0.1 and n_motas >= 2
            and len(meta['celdas']) == 5 and meta['celdas'][2] == origen, 'motas de %d colores' % n_motas)
    cian = (np.abs(img[..., :3] - np.array(m.COL_SCAR, dtype=np.float32)).max(axis=2) < 0.02).any()
    t.check('la seccion no lleva el cian de los cortes', not bool(cian))

    # 3. exportar: el fichero del testigo, una sola vez, y el registro
    camara(W, c, [], 0.2)
    m.historico_tick(W, c, reloj[0])
    nombre = m.nombre_testigo(e)
    n_exp = m._HIST['exportadas']
    m.historico_tick(W, c, reloj[0])
    m.historico_tick(W, c, reloj[0])
    csv = os.path.join(tmp, 'escisiones.csv')
    lineas = open(csv, encoding='utf-8').read().splitlines() if os.path.exists(csv) else []
    campos = dict(zip(lineas[0].split(';'), lineas[1].split(';'))) if len(lineas) > 1 else {}
    t.check('el testigo se exporta una sola vez (historico/escision_<jornada>_c<ciclo>_<id>.png, con TOP.save)',
            e['testigo'] == nombre and nombre == 'escision_%s_c%s_%d.png' % (e['jornada'], e['ciclo'], e['id'])
            and n_exp == 1 and m._HIST['exportadas'] == 1 and not m._HIST['pend'], str(e.get('testigo')))
    m.escisiones_tabla(W)
    te = base.op('escisiones')
    fila_t = dict(zip([te[0, k].val for k in range(te.numCols)], [x.val for x in te.row(1)])) if te.numRows > 1 else {}
    siete = ('id', 'jornada', 'ciclo', 'hora', 'personas', 'conchas', 'celda')
    t.check('el registro tiene sus siete campos (jornada, ciclo, hora, personas, conchas cruzadas y celda de '
            'origen, con su id), en la tabla y en el fichero',
            len(lineas) == 2 and all(campos.get(k) not in (None, '') for k in siete)
            and all(fila_t.get(k) == campos.get(k) for k in siete) and campos['personas'] == '3'
            and campos['conchas'] == '3' and campos['celda'] == str(origen) and campos['testigo'] == nombre
            and campos['estado'] == 'cerrada', str(campos))
    e['registrada'] = False                     # como al relanzar con el fichero ya escrito
    m.registrar_escision(W, e)
    m.historico_tick(W, c, reloj[0])
    lineas2 = open(csv, encoding='utf-8').read().splitlines()
    t.check('relanzar no duplica filas', lineas2 == lineas and e.get('registrada') is True)

    # 4. la columna de la jornada
    W, c = nuevo(0)
    hoy = m._fecha()[0]
    m.end_cycle(W, c, reloj[0], 4, 'forzado')                   # ciclo 1: limpia
    W['ciclo_n'] = 2
    m.depositar_inclusion(W, c, m.note_cell(60), m.LLEGADA, reloj[0])
    m.end_cycle(W, c, reloj[0], 4, 'estancado')                 # ciclo 2: humana
    W['ciclo_n'] = 3
    m.end_cycle(W, c, reloj[0], 4, 'colapso')                   # ciclo 3: limpia + colapso
    W['ciclo_n'] = 4
    camara(W, c, linea, 5.3)                                    # 3 personas
    camara(W, c, [], 0.2)
    lejos = [7 * cols + j for j in range(6)]
    camara(W, c, lejos, 5.3)                                    # 6 personas
    m.end_cycle(W, c, reloj[0], 4, 'forzado')                   # ciclo 4
    img, meta = m.columna_jornada(W, c, hoy)
    vetas = dict((v[0], v) for v in meta['vetas'])
    e3, e6 = W['escisiones'][0], W['escisiones'][1]
    a3 = vetas[e3['id']][3] - vetas[e3['id']][2] if e3['id'] in vetas else 0
    a6 = vetas[e6['id']][3] - vetas[e6['id']][2] if e6['id'] in vetas else 0
    tipos = [b[1] for b in meta['bandas']]
    t.check('la columna resumen tiene una banda por ciclo de la jornada (la mas nueva arriba), con su tipo',
            img.shape == (m.COLUMNA_PX[1], m.COLUMNA_PX[0], 4) and [b[0] for b in meta['bandas']] == [4, 3, 2, 1]
            and tipos == ['limpia', 'limpia + colapso', 'humana', 'limpia']
            and all(meta['bandas'][k][3] <= meta['bandas'][k + 1][2] + 1 for k in range(3)), str(tipos))
    v3 = vetas.get(e3['id'])
    col3 = m.paleta_humana(c, e3['ramas'])
    px = img[(v3[4] + v3[5]) // 2, (v3[2] + v3[3]) // 2, :3] if v3 else (0, 0, 0)
    t.check('y una veta por escision, que une las bandas que atraveso, con anchos en la proporcion de sus '
            'personas (3 y 6)',
            len(meta['vetas']) == 2 and a3 > 0 and a6 == 2 * a3 and e3['personas'] == 3 and e6['personas'] == 6
            and all(abs(float(px[k]) - col3[k]) < 1e-4 for k in range(3))
            and v3[5] - v3[4] >= 3 * (meta['bandas'][0][3] - meta['bandas'][0][2]) - 3,
            'anchos %d y %d' % (a3, a6))
    vacia, mv = m.columna_jornada(W, c, '1999-01-01')
    t.check('una jornada sin ciclos: columna vacia', mv['bandas'] == [] and mv['vetas'] == [] and float(vacia[..., :3].max()) == 0.0)

    # 5. por el boton y la leyenda
    m.hist_reset()
    W, c = nuevo()
    camara(W, c, linea, 5.3)
    W = m.world()
    antes = m.legend()
    m.on_pulse('Exportartestigo')
    e = W['escisiones'][-1]
    leg = m.legend()
    linea_l = ' '.join(l.strip() for l in leg.splitlines() if 'HISTORICO' in l)
    t.check('Exportartestigo exporta la seccion de la ultima escision; la linea HISTORICO',
            'testigo al deshacerse la fila o al enterrar' in antes
            and e['testigo'] == m.nombre_testigo(e)
            and 'HISTORICO escisiones hoy 1   ultima #1 J%s C1 3 personas 3 conchas celda %d   testigo exportado'
            % (hoy, e['origen']) in leg, linea_l)
    o1, o2 = base.op('seccion'), base.op('columna_jornada')
    o1.cook(force=True)
    o2.cook(force=True)
    a1 = o1.numpyArray()
    a2 = o2.numpyArray()
    t.check('seccion (640 x 360) y columna_jornada (200 x 720), Script TOP',
            a1 is not None and a1.shape == (360, 640, 4) and a2 is not None and a2.shape == (720, 200, 4)
            and float(a1[..., :3].max()) > 0.1)


run_test(base, prueba)
print('  Ahora: una fila (Simfila 3, Simformarfila), espera 5 s y Simvaciar: en la carpeta de')
print('  Carpetahistorico aparece escision_<jornada>_c<ciclo>_<id>.png y una linea en escisiones.csv.')
print('=' * 66)
