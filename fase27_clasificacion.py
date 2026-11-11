"""
=============================================================================
ESTRATOS - FASE 27: CLASIFICACION AL ENTERRAR
=============================================================================
Requiere la fase 26. Al enterrar el mundo se cuentan las huellas que han
sobrevivido a la erosion: con ellas, la concha es un estrato humano; sin
ellas, una concha limpia, aunque haya habido gente todo el dia.

QUE HACE (en end_cycle, antes de hornear)
-----------------------------------------
  RECUENTO     las inclusiones supervivientes del mundo que se entierra (las
               escisiones de la fase 29 no cuentan).
  BANDA        con al menos Minhuellas (1), ESTRATO HUMANO; si no, CONCHA
               LIMPIA: todas sus huellas se borraron, o no llegan al minimo.
  HORNEADO     el recuento va al material: cada loseta nueva guarda cuantas
               inclusiones sobrevivieron en su celda y sus semillas (sus
               colores). El shader de las conchas (familia mineral) las dibuja
               como motas de la paleta humana en la cara y los flancos de esa
               loseta, con una cobertura que crece con el numero de
               inclusiones y nunca pasa de Inclusionesmax (0,8) de la loseta.
               El grosor de la concha no cambia (el de su ciclo, fase 8).
  COLAPSO      la concha guarda el motivo del cierre y la marca de colapso
               (si la fase 23 cerro el ciclo con el motivo 'colapso'). Se
               combina con humana o limpia. 'estancado' no es colapso.
  DESPUES      las inclusiones del mundo enterrado se vacian: lo heredado
               empieza sin ninguna.
  Umbralpresencia   desaparece: no existe en el repositorio; si tu proyecto
               lo tiene, este script lo quita y lo dice en el informe.
  LEYENDA      BANDA    ultima: estrato humano 12 huellas (min 1)   cobertura
               78% (max 80%)   colapso no   humanas 3 de 11
  ciclos       la tabla gana las columnas huellas y banda.

PROBAR
------
  Deja tres inclusiones (Probllegada 1 y Simponer en tres casillas) y
  Forzarciclo: la concha nueva sale con motas de color en esas tres celdas;
  un corte con la caja las ensena en la pared. Borra todas antes de
  Forzarciclo: concha limpia. Con Colapsoon y Simbalance por encima de 1
  durante Maxerosion (fase 23): la concha sale con la marca de colapso.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase27_clasificacion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase27 v1  (clasificacion al enterrar: estrato humano o concha limpia, y el colapso)'
banner(VERSION)

base = require_base(27)
motor = install_core(base, CARPETA, 27)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase27)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase27')
add_par(base, page, 'int', 'Minhuellas', 'Huellas minimas para estrato humano', 1, 1, 100, clamp=True)
add_par(base, page, 'float', 'Inclusionesmax', 'Cobertura maxima de inclusiones', 0.8, 0.0, 1.0, clamp=True)
ok('pagina Fase27: Minhuellas 1, Inclusionesmax 0,8 (80 % de la loseta)')
if remove_par(base, 'Umbralpresencia'):
    ok('Umbralpresencia: quitado (v5 no lo usa: la banda la decide el recuento de huellas)')
else:
    ok('Umbralpresencia: no existia (nada que quitar)')

for col in ('huellas', 'banda'):
    if columna_tabla(base.op('ciclos'), col):
        ok('ciclos: columna %s' % col)

set_render(base)

leeme(base, 27, """FASE 27 - CLASIFICACION AL ENTERRAR
  Al enterrar se cuentan las inclusiones supervivientes. Con al menos
  Minhuellas, estrato humano; si no, concha limpia. Cada loseta nueva
  guarda las de su celda y el shader las dibuja como motas de la paleta
  humana, con una cobertura que crece con su numero y no pasa de
  Inclusionesmax. La concha guarda el motivo del cierre y la marca de
  colapso (fase 23), que se combina con humana o limpia. Tabla ciclos:
  huellas y banda. Umbralpresencia desaparece.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS27 = ('Minhuellas', 'Inclusionesmax', 'Colapsoon', 'Maxerosion', 'Simbalance', 'Nota', 'Velprueba',
          'Temaenciclo', 'Materialrespaldo')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS27)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Temaenciclo = False
    base.par.Colapsoon = False
    reloj = [absTime.seconds + 700.0]
    celdas = [m.note_cell(n) for n in (60, 64, 67)]

    def nuevo():
        m.reset_world()
        m.sala_reset()
        return m.world(), m.cfg()

    def entierra(W, c, motivo='forzado'):
        reloj[0] += 1.0
        return m.close_cycle(W, c, reloj[0], motivo)

    # 1. humana y limpia
    W, c = nuevo()
    for i in celdas:
        m.depositar_inclusion(W, c, i, m.LLEGADA, reloj[0])
    n0 = m.contar_huellas(W)
    ev = entierra(W, c)
    sh = W['shells'][-1]
    t.check('3 supervivientes y Minhuellas 1: estrato humano con 3; cada loseta guarda las de su celda',
            n0 == 3 and m.banda_de(sh) == ('humana', 3, False) and sorted(sh['incl']) == sorted(celdas)
            and all(len(v) == 1 for v in sh['incl'].values()) and ev['banda'] == 'humana' and ev['huellas'] == 3,
            str(m.banda_de(sh)))
    t.check('las inclusiones del mundo enterrado se vacian', m.n_inclusiones(W) == 0)
    W, c = nuevo()
    for k in range(40):
        i = celdas[k % 3]
        m.depositar_inclusion(W, c, i, m.LLEGADA, reloj[0])
        m.golpe_inclusiones(W, i, 'erosion')
    ev = entierra(W, c)
    t.check('0 supervivientes con 40 llegadas borradas: concha limpia',
            W['incl_n'] == dict(llegadas=0, paradas=0) and m.banda_de(W['shells'][-1]) == ('limpia', 0, False)
            and W['incl_borradas']['erosion'] == 40 and ev['banda'] == 'limpia')
    base.par.Minhuellas = 5
    W, c = nuevo()
    for i in celdas:
        m.depositar_inclusion(W, c, i, m.LLEGADA, reloj[0])
    entierra(W, c)
    limpia5 = m.banda_de(W['shells'][-1])
    filas5 = [f for f in m.build_tiles(W, c, reloj[0]) if len(f) > 12 and f[12] > 1.5]
    base.par.Minhuellas = 1
    t.check('Minhuellas 5 con 3 supervivientes: limpia (y sin motas)', limpia5 == ('limpia', 3, False) and not filas5)

    # 2. la cobertura y el grosor
    W, c = nuevo()
    cobs = [m.cobertura(c, n) for n in (0, 1, 3, 12, 1000)]
    entierra(W, c)
    g0 = W['shells'][-1]['grosor']
    W, c = nuevo()
    W['incl'][celdas[0]] = [[0, 1, 0.0, (k * 0.618) % 1.0] for k in range(1000)]
    entierra(W, c)
    sh = W['shells'][-1]
    q = m.cobertura_q(c, sh, celdas[0])
    t.check('la cobertura crece con el numero de inclusiones y nunca pasa de Inclusionesmax (1000 en una '
            'celda: 80 %); el grosor de la concha es el mismo con 0 y con 1000',
            cobs[0] == 0.0 and cobs[0] < cobs[1] < cobs[2] < cobs[3] <= cobs[4] <= 0.8 + 1e-9
            and len(sh['incl'][celdas[0]]) == 1000 and q == 16 and abs(sh['grosor'] - g0) < 1e-12,
            'cobertura %s' % ['%.2f' % x for x in cobs])
    base.par.Inclusionesmax = 0.3
    c3 = m.cfg()
    t.check('con Inclusionesmax 0,3 ninguna loseta pasa del 30 %', m.cobertura_q(c3, sh, celdas[0]) == 6
            and m.cobertura(c3, 1000) <= 0.3 + 1e-9)
    base.par.Inclusionesmax = 0.8

    # 3. el horneado en el material: la parte entera del alfa de la loseta
    W, c = nuevo()
    for k in range(3):
        m.depositar_inclusion(W, c, celdas[0], m.PARADA, reloj[0])
    m.depositar_inclusion(W, c, celdas[1], m.LLEGADA, reloj[0])
    entierra(W, c)
    sh = W['shells'][-1]

    def losetas(W, c, i):
        n = m._norm(m.normal_i(i))
        return [f for f in m.build_tiles(W, c, reloj[0]) if m._norm(f[0:3]) == n]
    a0 = [f[12] for f in losetas(W, c, celdas[0])]
    a1 = [f[12] for f in losetas(W, c, celdas[1])]
    a2 = [f[12] for f in losetas(W, c, celdas[2])]
    q0, q1 = m.cobertura_q(c, sh, celdas[0]), m.cobertura_q(c, sh, celdas[1])
    t.check('el recuento se hornea en el material: el alfa de la loseta (y de su tapa) lleva rugosidad + 2 x '
            'cobertura, mas con 3 inclusiones que con 1, y nada en una celda sin ellas',
            q0 > q1 >= 1 and len(a0) == 2 and all(int((a % 100) // 2) == q0 for a in a0)
            and all(int((a % 100) // 2) == q1 for a in a1) and all(a <= 1.0 for a in a2)
            and all(0.0 < a % 100 - 2 * q0 <= 1.0 for a in a0), 'alfa %s, %s y %s' % (a0, a1, a2))
    entierra(W, c)                      # otra concha encima: la de abajo conserva sus motas
    a0b = [f[12] for f in losetas(W, c, celdas[0])]
    t.check('la loseta humana conserva sus motas bajo la concha siguiente (un corte las ensena en la pared)',
            sorted(int((a % 100) // 2) for a in a0b) == [0, 0, q0], str(a0b))
    tabla = [m.paleta_humana(c, (j + 0.5) / 8.0) for j in range(8)]
    px = base.op('piel_pixel').text if base.op('piel_pixel') is not None else ''
    en_shader = all('vec3(%.3f, %.3f, %.3f)' % col in px for col in tabla)
    t.check('la tabla de la paleta humana del shader es la del motor',
            en_shader and 'HUMANA[8]' in px
            and all(abs(a - b) < 1e-3 for x, y in zip(tabla, m.PALETA_HUMANA_8) for a, b in zip(x, y)))

    # 4. las escisiones no cuentan
    W, c = nuevo()
    m.depositar_inclusion(W, c, celdas[0], m.LLEGADA, reloj[0])
    W['escisiones'] = [dict(id=7, origen=celdas[1], estado='abierta', personas=4)]
    n = m.contar_huellas(W)
    clas = m.clasificar_concha(W, c, dict(motivo='forzado'))
    W['escisiones'] = []
    t.check('una escision abierta no cuenta en el recuento (la concha apunta cuales cruzaban su mundo)',
            n == 1 and clas['huellas'] == 1 and clas['escisiones'] == [7])

    # 5. el colapso, marca de cierre combinable
    W, c = nuevo()
    m.depositar_inclusion(W, c, celdas[0], m.LLEGADA, reloj[0])
    entierra(W, c, 'colapso')
    hc = m.banda_de(W['shells'][-1])
    cierre = W['shells'][-1]['cierre']
    entierra(W, c, 'colapso')
    lc = m.banda_de(W['shells'][-1])
    entierra(W, c, 'estancado')
    le = m.banda_de(W['shells'][-1])
    t.check('un cierre por colapso marca la concha, y se combina con humana y con limpia; uno por estancado, no',
            hc == ('humana', 1, True) and cierre == 'colapso' and lc == ('limpia', 0, True)
            and le == ('limpia', 0, False) and W['shells'][-1]['cierre'] == 'estancado')
    base.par.Colapsoon = True
    base.par.Simbalance = 1.2
    W, c = nuevo()
    m.depositar_inclusion(W, c, celdas[0], m.LLEGADA, reloj[0])
    ev = None
    for _ in range(int(20 * 30)):
        reloj[0] += 1.0 / 30.0
        ev = m.tick(W, c, reloj[0], 120.0, False).get('ciclo')
        if ev:
            break
    base.par.Colapsoon = False
    base.par.Simbalance = -1.0
    t.check('con Colapsoon, la erosion dominante sostenida (fase 23) entierra una concha con la marca de colapso',
            ev is not None and ev['motivo'] == 'colapso' and ev.get('colapso') is True
            and m.banda_de(W['shells'][-1]) == ('humana', 1, True))

    # 6. Umbralpresencia, los mundos de antes y la tabla
    src = base.op('motor').text
    t.check('Umbralpresencia: ni en las paginas ni en el motor',
            not has_par(base, 'Umbralpresencia') and 'Umbralpresencia' not in src)
    W, c = nuevo()
    entierra(W, c)
    vieja = W['shells'][-1]
    for k in ('huellas', 'banda', 'colapso', 'cierre', 'incl', 'escisiones'):
        vieja.pop(k, None)
    W['dirty'] = True
    filas_v = m.build_tiles(W, c, reloj[0])
    t.check('un mundo de antes de la fase 27 carga y sus conchas se leen como limpias, sin marca',
            m.banda_de(vieja) == ('limpia', 0, False) and filas_v and all(f[12] <= 1.0 for f in filas_v)
            and 'concha limpia 0 huellas' in m.legend())
    tb = base.op('ciclos')
    cab = [tb[0, k].val for k in range(tb.numCols)] if tb is not None and tb.numRows else []
    W, c = nuevo()
    for i in celdas[:2]:
        m.depositar_inclusion(W, c, i, m.LLEGADA, reloj[0])
    m.registrar_ciclo(W, c, entierra(W, c, 'colapso'))
    fila = dict(zip(cab, [x.val for x in tb.row(tb.numRows - 1)])) if tb is not None else {}
    t.check('la tabla ciclos tiene huellas y banda', fila.get('huellas') == '2' and fila.get('banda') == 'humana + colapso',
            '%s / %s' % (fila.get('huellas'), fila.get('banda')))
    leg = m.legend()
    linea = ' '.join(l.strip() for l in leg.splitlines() if 'BANDA' in l)
    t.check('leyenda BANDA', 'BANDA    ultima: estrato humano 2 huellas (min 1)   cobertura ' in leg
            and '(max 80%)   colapso si   humanas 1 de 1' in leg, linea)


run_test(base, prueba)
print('  Ahora: deja inclusiones (Probllegada 1, Simponer) y Forzarciclo: la concha nueva sale')
print('  con motas de color en esas celdas (leyenda BANDA). Sin inclusiones: concha limpia.')
print('=' * 66)
