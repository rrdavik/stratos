"""
=============================================================================
ESTRATOS - FASE 29: LA FILA Y LA ESCISION COLECTIVA
=============================================================================
Requiere la fase 28. Lo unico que el publico puede hacer a proposito, y solo
entre varios: una fila sostenida abre una escision, un pozo que atraviesa las
conchas del planeta y que ya no se cierra.

QUE HACE
--------
  FILA         Minfila personas o mas (3) en casillas contiguas (diagonales
               incluidas), sostenida Tfila segundos (5) sobre la ocupacion
               binaria de la fase 24. Modofila = cadena (cualquier forma
               contigua) o recta (todas en una misma fila, columna o diagonal
               de la rejilla, seguidas). Cuenta personas, no casillas. Se
               reconoce de una imagen a la siguiente si comparte alguna
               casilla con la de antes. Puede haber varias filas a la vez,
               cada una con su escision.
  ORIGEN       la casilla de la fila ocupada desde hace mas tiempo. La
               escision se abre en la celda que mira a esa casilla en el
               instante en que la fila cumple Tfila, y esa celda queda fija
               aunque el planeta gire.
  PROFUNDIDAD  personas x Conchasporpersona losetas de la columna de origen,
               con el nucleo como tope. Si se suman personas mientras la fila
               aguanta, la misma escision baja mas (sigue al maximo visto; si
               se van, no sube). La fila solo abre otra cuando se deshace
               (menos de Minfila personas).
  PERMANENCIA  es un hueco: quita losetas de la columna (como un corte de
               radio 0), vacia la celda y borra sus inclusiones. No cuenta en
               el tope por mundo de los cortes, no enciende cicatriz cian,
               ignora Colmatacion en su celda (la concha siguiente la tapiza
               sin cerrarla), un rio no la llena (fase 13) y no ensena
               fosiles (fase 16).
  BALANCE      no pasa por la erosion ni por los pulsos: no es erosion ni
               creacion para la luz de la sala (fase 23).
  FULGURITA    una pieza por concha atravesada, de la superficie al fondo:
               pared exterior de arena fundida, interior vitreo y nucleo
               emisivo de la paleta humana (nunca cian). En cada concha se
               ramifica: dos o tres ramas finas hacia las paredes, decididas
               por el mapa logistico. Las ramas son solo visuales. Lo que
               queda bajo el tapiz de una concha posterior no se dibuja. En la
               noche de enterramiento (fase 28) sus paredes brillan.
  LEYENDA      FILA     4 personas   cadena   5.0/5.0 s
               ESCISION #3   celda 40   conchas 4/12   abierta

OPERADORES (en /project1/FASE1)
-------------------------------
  escisiones   Table DAT: id, jornada, ciclo, hora, personas, conchas, celda,
               estado (abierta, cerrada, enterrada) y testigo. Las ultimas 200.
  i_fulguritas, fulguritas
               Script CHOP y Geometry COMP instanciado (cajas), con
               mat_piel_vidrio (familia vidrio del shader de la piel).

PROBAR SIN CAMARA
-----------------
  Con varias conchas (Forzarciclo unas cuantas veces): Simfila 3 y
  Simformarfila (fase 24). A los 5 s se abre un pozo de 3 conchas con su
  fulgurita en la celda que miraba la casilla mas antigua. Simsumar: baja una
  mas. Simvaciar y otra fila: otra escision. Forzarciclo: el pozo queda
  tapizado y sigue abierto.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase29_fila.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase29 v1  (fila y escision colectiva: un hueco permanente con su fulgurita)'
banner(VERSION)

base = require_base(29)
motor = install_core(base, CARPETA, 29)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase29)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase29')
add_par(base, page, 'int', 'Minfila', 'Personas minimas de una fila', 3, 2, 12, clamp=True)
add_par(base, page, 'float', 'Tfila', 'Tiempo de la fila (s)', 5.0, 0.5, 60.0, clamp=True)
add_par(base, page, 'menu', 'Modofila', 'Forma de la fila', 'cadena',
        menu=list(m.MODOS_FILA), menu_labels=['Cadena (cualquier forma contigua)', 'Recta (en linea)'])
add_par(base, page, 'int', 'Conchasporpersona', 'Conchas por persona', 1, 1, 12, clamp=True)
add_par(base, page, 'pulse', 'Simsumar', 'Sumar una persona a la fila')
ok('pagina Fase29: Minfila 3, Tfila 5 s, Modofila cadena, Conchasporpersona 1, Simsumar')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

tb = get_or_make(base, 'tableDAT', 'escisiones', -880, 1900)
m.escisiones_tabla(m.world())
if tb.numRows == 0:
    tb.appendRow(list(m.ESCISIONES_COLS))
if base.op('mat_piel_vidrio') is None:
    fail('mat_piel_vidrio: no esta (el shader de la piel es de la fase 12)')
geo = make_instanced(base, 'fulguritas', -880, 2500, 'mat_piel_vidrio')
if not setp_any(geo, ['instancea'], 'a'):
    fail('fulguritas no lee la parte de cada pieza: Instance 2 -> Color A = a')
if has_par(base, 'Materialrespaldo'):
    setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_vidrio'")
ok('escisiones (tabla) y fulguritas: paredes, vidrio, nucleo y ramas de cada escision (familia vidrio)')

set_render(base)

leeme(base, 29, """FASE 29 - LA FILA Y LA ESCISION COLECTIVA
  Minfila personas en casillas contiguas durante Tfila s (Modofila: cadena
  o recta) abren una escision en la celda que mira a la casilla mas antigua
  de la fila: personas x Conchasporpersona losetas de su columna, hasta el
  nucleo; baja mas si se suman personas. Es un hueco permanente: vacia la
  celda, borra sus inclusiones, no cuenta como corte ni en el balance, sin
  cicatriz; la concha siguiente la tapiza sin cerrarla. Fulgurita: pared de
  arena fundida, vidrio y nucleo emisivo de la paleta humana, con ramas.
  Tabla escisiones; geometria fulguritas. Sin camara: Simformarfila y
  Simsumar.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS29 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Modofila', 'Conchasporpersona', 'Colmatacion', 'Simbalance',
          'Temaenciclo', 'Tema')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS29)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0             # sin inclusiones de las personas de la prueba
    reloj = [absTime.seconds + 900.0]
    tb = base.op('sala_personas')
    DT = 1.0 / m.CAM_FPS

    def nuevo(conchas=8):
        m.reset_world()
        m.sala_reset()
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        W, c = m.world(), m.cfg()
        for _ in range(conchas):
            m.end_cycle(W, c, reloj[0])
            reloj[0] += 1.0
        return W, c

    def camara(W, c, casillas, seg=None, n=1):
        """Imagenes con una persona en el centro de cada casilla."""
        mx = [m.casilla_xy(c, k) + (1.7,) for k in casillas]
        for _ in range(n if seg is None else int(round(seg * m.CAM_FPS))):
            reloj[0] += DT
            m.sala_mundo(W, c, reloj[0], m.tick_personas(W, c, reloj[0], mx))

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)
    k0 = 4 * cols + 4
    L = [k0, k0 + 1, k0 + 1 + cols]             # en L
    linea = [k0, k0 + 1, k0 + 2]

    # 1. cadena y recta
    t.check('es_recta: una fila, una columna o una diagonal seguidas; una L o una fila con un hueco, no',
            m.es_recta(linea, cols) and m.es_recta([k0, k0 + cols, k0 + 2 * cols], cols)
            and m.es_recta([k0, k0 + cols + 1, k0 + 2 * cols + 2], cols)
            and m.es_recta([k0 + 2, k0 + cols + 1, k0 + 2 * cols], cols)
            and not m.es_recta(L, cols) and not m.es_recta([k0, k0 + 2], cols))
    camara(W, c, L, seg=5.2)
    en_L = len(W['escisiones'])
    base.par.Modofila = 'recta'
    W, c = nuevo()
    camara(W, c, L, seg=5.2)
    recta_L = len(W['escisiones'])
    W, c = nuevo()
    camara(W, c, linea, seg=5.2)
    recta_linea = len(W['escisiones'])
    base.par.Modofila = 'cadena'
    t.check('3 personas en cadena en L durante Tfila: una escision; con Modofila recta, no; en linea, si',
            (en_L, recta_L, recta_linea) == (1, 0, 1), str((en_L, recta_L, recta_linea)))

    # 2. dos personas; una fila que se rompe antes de tiempo
    W, c = nuevo()
    camara(W, c, linea[:2], seg=7.0)
    dos = (len(W['escisiones']), len(m._SALA['filas']))
    W, c = nuevo()
    camara(W, c, linea, n=2)                    # confirmadas: la fila empieza
    camara(W, c, linea, seg=4.9)
    camara(W, c, linea[:2], n=3)                # se rompe a Tfila - 0,1 s
    camara(W, c, linea, seg=4.0)                # otra vez: el tiempo empieza de cero
    rota = len(W['escisiones'])
    camara(W, c, linea, seg=1.2)
    t.check('2 personas no son una fila; una fila que se rompe a Tfila - 0,1 s no abre nada (y al rehacerse '
            'empieza de cero)', dos == (0, 0) and rota == 0 and len(W['escisiones']) == 1,
            '%s, %d' % (dos, rota))

    # 3. el origen: la casilla ocupada desde hace mas tiempo; la celda queda fija
    W, c = nuevo()
    camara(W, c, [linea[2]], seg=1.0)
    camara(W, c, linea, seg=5.2)
    e = W['escisiones'][-1]
    celda0 = m.celda_de_casilla(W, c, linea[2])
    cg = dict(c)
    cg['lon_central'] = c['lon_central'] + 120.0
    camara(W, cg, linea, seg=1.0)
    t.check('el origen es la casilla ocupada desde hace mas tiempo, y la celda no cambia al girar el planeta',
            e['casilla'] == linea[2] and e['origen'] == celda0 and m.celda_de_casilla(W, cg, linea[2]) != celda0
            and len(W['escisiones']) == 1 and W['escisiones'][-1]['origen'] == celda0,
            'casilla %d, celda %d' % (e['casilla'], e['origen']))

    # 4. la profundidad
    W, c = nuevo(8)
    origen = m.celda_de_casilla(W, c, linea[0])
    m.depositar_inclusion(W, c, origen, m.PARADA, reloj[0])
    for _ in range(3):
        m.note_on(W, c, m.GEO, m.cell_note(origen), 100, reloj[0])
    vecina = m.NEIGH[origen][0]
    antes = dict(col=len(W['cols'][origen]), vec=len(W['cols'][vecina]), quitadas=list(W['quitadas']),
                 resto=list(W['ero_resto']), scars=dict(W['scars']), bal=list(W['sala'].get('bal', [])),
                 borr=dict(W['incl_borradas']))
    camara(W, c, linea, seg=5.2)
    e = W['escisiones'][-1]
    tres = (len(W['cols'][origen]), len(e['cortadas']), e['personas'], W['occ'][origen])
    camara(W, c, linea + [k0 + 3, k0 + 4], seg=0.5)
    cinco = (len(W['cols'][origen]), len(e['cortadas']), e['personas'], len(W['escisiones']))
    camara(W, c, linea, seg=0.5)                # se van dos: no sube
    t.check('3 personas y Conchasporpersona 1 quitan 3 losetas de la columna de origen y vacian la celda; 2 mas '
            'mientras aguanta: 5, la misma escision; si se van, no sube',
            antes['col'] == 8 and tres == (5, 3, 3, 0) and cinco == (3, 5, 5, 1)
            and len(W['cols'][origen]) == 3 and e['estado'] == 'abierta' and len(W['cols'][vecina]) == antes['vec'],
            '%s -> %s' % (tres, cinco))
    t.check('el balance de la fase 23 no cambia; ero_resto, quitadas y las cicatrices, tampoco',
            W['quitadas'] == antes['quitadas'] and W['ero_resto'] == antes['resto'] and W['scars'] == antes['scars']
            and W['sala'].get('bal', []) == antes['bal'])
    t.check('las inclusiones de la celda de origen se borran (causa escision)',
            not W['incl'][origen] and W['incl_borradas']['escision'] == antes['borr']['escision'] + 1)
    W, c = nuevo(4)
    origen4 = m.celda_de_casilla(W, c, linea[0])
    camara(W, c, [k0 + j for j in range(6)], seg=5.2)
    e4 = W['escisiones'][-1]
    t.check('con 4 losetas en la columna y 6 personas, se para en el nucleo',
            len(e4['cortadas']) == 4 and e4['profundidad'] == 6 and W['cols'][origen4] == []
            and abs(m.suelo(W, c, origen4) - c['core_radius']) < 1e-9)
    base.par.Conchasporpersona = 2
    W, c = nuevo(8)
    camara(W, c, linea, seg=5.2)
    base.par.Conchasporpersona = 1
    t.check('Conchasporpersona 2: 3 personas abren 6 conchas', len(W['escisiones'][-1]['cortadas']) == 6)

    # 5. se deshace y se forma otra; dos a la vez
    W, c = nuevo()
    camara(W, c, linea, seg=5.2)
    camara(W, c, [], n=3)
    cerrada = W['escisiones'][-1]['estado']
    camara(W, c, linea, seg=5.2)
    otra = [(x['id'], x['estado']) for x in W['escisiones']]
    t.check('la fila se deshace (la escision queda cerrada) y se forma otra: escision nueva',
            cerrada == 'cerrada' and otra == [(1, 'cerrada'), (2, 'abierta')], str(otra))
    W, c = nuevo()
    lejos = [7 * cols + j for j in range(3)]         # otra fila, tres filas de casillas mas alla
    camara(W, c, linea + lejos, seg=5.2)
    t.check('dos filas separadas a la vez: dos escisiones, cada una en su celda',
            len(W['escisiones']) == 2 and len(m._SALA['filas']) == 2
            and W['escisiones'][0]['origen'] != W['escisiones'][1]['origen'],
            str([(x['id'], x['origen']) for x in W['escisiones']]))

    # 6. permanencia: el tapiz, la colmatacion, los lagos y los fosiles
    base.par.Colmatacion = 1.0
    W, c = nuevo(8)
    camara(W, c, linea, seg=5.2)
    e = W['escisiones'][-1]
    i = e['origen']
    hondo0 = m.hueco_escision(W, c, i)
    R0 = m.top_radius(W, c)
    corte = m.NEIGH[m.NEIGH[i][0]][1] if m.NEIGH[m.NEIGH[i][0]][1] != i else m.NEIGH[m.NEIGH[i][0]][2]
    m.cut(W, c, corte, 2, 0, reloj[0])
    m.end_cycle(W, c, reloj[0], 4)
    hondo1 = m.hueco_escision(W, c, i)
    R1 = m.top_radius(W, c)
    t.check('la concha siguiente la tapiza sin cerrarla, tambien con Colmatacion 1 (un corte normal si se rellena)',
            len(W['cols'][i]) == 6 and hondo1[1] - hondo1[0] > 0.5 * (hondo0[1] - hondo0[0]) > 0
            and R1 - m.suelo(W, c, i) > 1e-3 and abs(R1 - m.suelo(W, c, corte)) < 1e-6
            and e['estado'] == 'enterrada', 'hueco %.3f -> %.3f' % (hondo0[1] - hondo0[0], hondo1[1] - hondo1[0]))
    base.par.Colmatacion = 0.0
    m.cut(W, c, corte, 2, 0, reloj[0])
    src = base.op('motor').text
    t.check('la fase 16 no pone fosiles en ella (no cuenta como corte) y un rio no la llena (no es un lago)',
            m.es_escision(W, i) and not m.en_corte(W, c, i) and m.en_corte(W, c, corte) and m.laguna(W, c, i) > 0.02
            and 'and not (cfg[\'nivel\'] >= 29 and es_escision(W, c))' in src)

    # 7. la fulgurita
    W, c = nuevo(8)
    camara(W, c, linea, seg=5.2)
    e = W['escisiones'][-1]
    cols_antes = [list(x) for x in W['cols']]
    out = {}
    filas_f = m.build_fulguritas(W, c, reloj[0], out)
    partes = [int(f[12] // 2) for f in filas_f]
    ramas = len(filas_f) - 3 * 9
    fondo, borde = m.hueco_escision(W, c, e['origen'])
    radios = [math.sqrt(sum(x * x for x in f[0:3])) for f in filas_f]
    cian = [f for f in filas_f if f[10] > f[9] + 0.12 and f[11] > f[9] + 0.12]
    t.check('la fulgurita: una pieza por concha atravesada (3), del fondo a la superficie, cada una con 4 '
            'paredes de arena fundida, 4 laminas de vidrio, un nucleo y 2 o 3 ramas',
            partes.count(m.PARED) == 12 and partes.count(m.VIDRIO) == 12 and partes.count(m.NUCLEO) == 3 + ramas
            and 6 <= ramas <= 9 and min(radios) >= fondo - 1e-6 and max(radios) <= borde + 1e-6
            and all(len(f) == 13 for f in filas_f), '%d instancias, %d ramas' % (len(filas_f), ramas))
    t.check('ninguna pieza de la fulgurita es cian; las ramas no quitan losetas',
            not cian and [list(x) for x in W['cols']] == cols_antes and len(e['cortadas']) == 3)
    m.end_cycle(W, c, reloj[0], 4)
    tapizada = m.build_fulguritas(W, c, reloj[0], {})
    t.check('lo que queda bajo el tapiz de una concha posterior no se dibuja (pero la escision lo guarda)',
            0 < len(tapizada) <= len(filas_f) and len(e['cortadas']) == 3
            and min(math.sqrt(sum(x * x for x in f[0:3])) for f in tapizada) >= m.suelo(W, c, e['origen']) - 1e-6)
    o = base.op('i_fulguritas')
    m._CACHE['inst'] = m.build_instances(W, c, reloj[0])
    o.cook(force=True)
    t.check('i_fulguritas -> fulguritas (mat_piel_vidrio), en el render',
            o.numSamples == len(tapizada) and o.numChans == 13
            and 'fulguritas' in str(base.op('render').par.geometry.val).split())

    # 8. por la sala simulada: Simformarfila y Simsumar; la tabla y la leyenda
    W, c = nuevo(8)
    base.par.Simcasilla = k0
    base.par.Simfila = 3
    m.on_pulse('Simformarfila')
    c = m.cfg()

    def imagenes(seg):
        for _ in range(int(round(seg * m.CAM_FPS))):
            reloj[0] += DT
            m._SALA['t_img'] = -99.0
            m.sala_tick(W, c, reloj[0])
    imagenes(2.0)
    leg_antes = m.legend()
    imagenes(3.3)
    e = W['escisiones'][-1] if W['escisiones'] else None
    m.on_pulse('Simsumar')
    imagenes(0.3)
    m.escisiones_tabla(W)
    te = base.op('escisiones')
    fila_t = dict(zip([te[0, k].val for k in range(te.numCols)], [x.val for x in te.row(1)])) if te.numRows > 1 else {}
    t.check('Simformarfila (3) abre un pozo de 3 conchas a los 5 s; Simsumar: baja una mas; la tabla escisiones',
            e is not None and len(e['cortadas']) == 4 and e['personas'] == 4 and tb.numRows == 5
            and fila_t.get('id') == '1' and fila_t.get('personas') == '4' and fila_t.get('conchas') == '4'
            and fila_t.get('estado') == 'abierta' and fila_t.get('celda') == str(e['origen'])
            and len(fila_t.get('jornada', '')) == 10 and len(fila_t.get('hora', '')) == 8, str(fila_t))
    leg = m.legend()
    t.check('leyenda FILA y ESCISION',
            'FILA     3 personas   cadena   ' in leg_antes and '(sin abrir: fila ' in leg_antes
            and 'FILA     4 personas   cadena   5.0/5.0 s' in leg
            and 'ESCISION #1   celda %d   conchas 4/8   abierta' % e['origen'] in leg,
            ' | '.join(l.strip() for l in leg.splitlines() if 'FILA' in l or 'ESCISION' in l))
    m.close_cycle(W, c, reloj[0], 'forzado')
    t.check('al enterrar el mundo la escision queda enterrada, y la concha la apunta',
            e['estado'] == 'enterrada' and W['shells'][-1].get('escisiones') == [1])


run_test(base, prueba)
print('  Ahora: con varias conchas, Simfila 3 y Simformarfila: a los 5 s, un pozo de 3 conchas con')
print('  su fulgurita (leyenda FILA y ESCISION). Simsumar: baja una mas.')
print('=' * 66)
