"""
=============================================================================
ESTRATOS - FASE 23: LA LUZ DE LA SALA POR DMX
=============================================================================
Requiere la fase 22. La sala se ilumina con el estado del planeta: cuanto mas
pesa la erosion, mas luz, y cuando supera a la creacion, estroboscopio. El
motor calcula la luz y un solo CHOP la manda por DMX; la seguridad (3
destellos por segundo, solo blanco) vive en el motor, no en el aparato.
TouchDesigner sigue sin mandar nada al BeatStep.

QUE HACE
--------
  BALANCE      en una ventana de Ventanabalance segundos (30), la ocupacion
               destruida entre la depositada, en escalones de ocupacion. La
               erosion suma la caja, los aranazos (pads 4 a 8), sus cortes y
               el microfono; la creacion, las notas de los secuenciadores y
               los pulsos del bombo y el tom.
  DEPOSITO     balance < 0,5: casi a oscuras; un ambar tenue que respira con
               cada nota depositada.
  TENSION      de 0,5 a 1: la intensidad sube y vira a blanco frio; cada onset
               del microfono anade un pulso breve.
  EROSION DOMINANTE
               por encima de Umbralestrobo (1,0), y hasta bajar de
               Salidaestrobo (0,8): estroboscopio blanco; su frecuencia crece
               con el exceso, hasta Maxhz.
  FIN DE CICLO un unico destello blanco y oscuridad durante Noche segundos
               (4), mientras la capa se entierra. El balance empieza de cero.
  SEGURIDAD    como mucho 3 destellos en cualquier ventana de 1 s, contando
               todos los de la sala en un solo limitador (Maxhz no pasa de 3);
               el estroboscopio solo destella en blanco; el fin de ciclo lo
               apaga. Un destello con prioridad (el del fin de ciclo; el
               relampago de la fase 30) espera al primer hueco y el
               estroboscopio se lo cede. El microfono descarta el clic de cada
               destello. Y un cartel a la entrada que avise de las luces
               estroboscopicas (eso es montaje).
  COLAPSO      con Colapsoon (apagado por defecto), Maxerosion segundos (15)
               seguidos con el balance por encima de 1 cierran el ciclo con el
               motivo 'colapso'. 'estancado' no es colapso.
  LEYENDA      SALA  balance 1.12 (30 s)   erosion dominante   estrobo 2.4 Hz
               destellos 2/3   dmx artnet
  ciclos       la tabla gana la columna balance (el valor al cerrar).

OPERADORES (en /project1/FASE1)
-------------------------------
  dmx_canales  Table DAT editable (canal, funcion, foco): que canal DMX es
               cada cosa. Relanzar no la pisa. Funciones: bano_dimmer,
               bano_rojo, bano_verde, bano_azul (un foco con dimmer), bano_r,
               bano_g, bano_b (un foco RGB sin dimmer: el color ya lleva la
               intensidad) y estrobo. Por defecto, 4 focos de bano de 4
               canales (1 a 16) y el estroboscopio en el 17.
  dmx_valores  Script CHOP: un canal por canal DMX (c1, c2...), 0-255.
  dmx_out      DMX Out CHOP (Interfazdmx: Art-Net o USB Pro; Universodmx).

PROBAR SIN PUBLICO NI DMX
-------------------------
  Simbalance fuerza el balance (-1: el real). 0,3: deposito; 0,7: tension;
  1,2: erosion dominante, con el estroboscopio; 10: a tope, y la leyenda nunca
  pasa de 'destellos 3/3'. Forzarciclo: un destello y 4 s a oscuras. Sin
  interfaz DMX el motor calcula igual y la leyenda lo ensena ('sin dmx').

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase23_sala.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase23 v1  (luz de sala por DMX: balance, bano, estroboscopio, noche y colapso)'
banner(VERSION)

base = require_base(23)
motor = install_core(base, CARPETA, 23)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase23)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase23')
add_par(base, page, 'float', 'Ventanabalance', 'Ventana del balance (s)', 30.0, 5.0, 300.0, clamp=True)
add_par(base, page, 'float', 'Umbralestrobo', 'Estroboscopio: entra con este balance', 1.0, 0.1, 5.0, clamp=True)
add_par(base, page, 'float', 'Salidaestrobo', 'Estroboscopio: sale por debajo de', 0.8, 0.1, 5.0, clamp=True)
add_par(base, page, 'float', 'Maxhz', 'Destellos maximos por segundo (tope 3)', 3.0, 0.0, 3.0, clamp=True)
add_par(base, page, 'float', 'Noche', 'Noche de enterramiento (s)', 4.0, 0.0, 30.0, clamp=True)
add_par(base, page, 'toggle', 'Colapsoon', 'Colapso por erosion dominante sostenida', False)
add_par(base, page, 'float', 'Maxerosion', 'Erosion dominante que colapsa (s)', 15.0, 1.0, 120.0, clamp=True)
add_par(base, page, 'menu', 'Interfazdmx', 'Salida DMX', 'artnet',
        menu=list(m.INTERFACES_DMX), menu_labels=['Art-Net', 'USB Pro'])
add_par(base, page, 'int', 'Universodmx', 'Universo DMX', 0, 0, 255, clamp=True)
add_par(base, page, 'float', 'Simbalance', 'Probar: forzar el balance (-1: el real)', -1.0, -1.0, 10.0, clamp=True)
ok('pagina Fase23: Ventanabalance 30, Umbralestrobo 1,0, Salidaestrobo 0,8, Maxhz 3 (tope 3), Noche 4, '
   'Colapsoon (apagado), Maxerosion 15, Interfazdmx (Art-Net), Universodmx 0, Simbalance -1')

# -----------------------------------------------------------------------------
# LA TABLA DE CICLOS GANA LA COLUMNA balance
# -----------------------------------------------------------------------------


def columna_ciclos(t, nombre):
    """Anade la columna a la tabla ciclos, si no la tiene. Devuelve si la ha anadido."""
    if t is None or t.numRows == 0:
        return False
    if nombre in [t[0, k].val for k in range(t.numCols)]:
        return False
    t.appendCol([nombre])
    return True


if columna_ciclos(base.op('ciclos'), 'balance'):
    ok('ciclos: columna balance (el valor al cerrar el ciclo)')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

DMX_CB = r'''# Script CHOP 'dmx_valores' (fase 23): un canal por canal DMX de la tabla
# dmx_canales (c1, c2...), con su valor 0-255. Lo calcula el motor (dmx_cook).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.dmx_cook(scriptOp)
'''

X0, Y0 = -1320, 1500
tabla = get_or_make(base, 'tableDAT', 'dmx_canales', X0, Y0)
if tabla.numRows == 0:
    tabla.appendRow(list(m.DMX_COLS))
    for fila in m.DMX_DEFECTO:
        tabla.appendRow(fila)
    ok('dmx_canales: 4 focos de bano de 4 canales (dimmer, rojo, verde, azul: 1 a 16) y el '
       'estroboscopio en el 17. Editala con tus aparatos: relanzar no la pisa')
else:
    ok('dmx_canales: se conserva (%d canales)' % (tabla.numRows - 1))
cb = get_or_make(base, 'textDAT', 'dmx_valores_callbacks', X0 + 220, Y0 + 140)
cb.text = DMX_CB
vals = get_or_make(base, 'scriptCHOP', 'dmx_valores', X0 + 220, Y0)
setp_any(vals, ['callbacks', 'callbackdat', 'dat'], 'dmx_valores_callbacks')
try:
    dmx = get_or_make(base, 'dmxoutCHOP', 'dmx_out', X0 + 440, Y0)
except Exception as e:
    dmx = None
    info('dmx_out: no pude crear el DMX Out CHOP (%s)' % e)
if dmx is not None:
    connect(dmx, vals, 0)
    setp_any(dmx, ['active'], True)
    if not m.interfaz_dmx_al_dia():
        info('dmx_out: no pude poner la interfaz %s; elige Interface a mano' % base.par.Interfazdmx.eval())
    if not setexpr(dmx, 'universe', "parent().par.Universodmx"):
        info('dmx_out: no pude enlazar el universo; pon Universe = Universodmx')
    ok('dmx_canales -> dmx_valores -> dmx_out: el motor calcula la luz; un solo CHOP la manda')
hay, texto = m.dmx_encontrado()
if hay:
    ok('DMX: salida por %s, universo %d' % (texto, int(base.par.Universodmx.eval())))
else:
    info('sin DMX (%s): el motor calcula la luz igual y la leyenda SALA la ensena' % texto)

set_render(base)

leeme(base, 23, """FASE 23 - LA LUZ DE LA SALA POR DMX
  Balance = erosion / creacion en Ventanabalance s, en escalones de
  ocupacion. Deposito (< 0,5): ambar tenue que respira con cada nota.
  Tension (0,5 a 1): sube y vira a blanco frio, con un pulso por onset.
  Erosion dominante (entra en Umbralestrobo, sale bajo Salidaestrobo):
  estroboscopio blanco, hasta Maxhz. Nunca mas de 3 destellos en 1 s en
  toda la sala. Fin de ciclo: un destello y Noche s a oscuras. Colapsoon:
  Maxerosion s de balance > 1 cierran el ciclo como 'colapso'.
  dmx_canales (editable) -> dmx_valores -> dmx_out (Interfazdmx,
  Universodmx). Simbalance fuerza el balance para probar.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS23 = ('Ventanabalance', 'Umbralestrobo', 'Salidaestrobo', 'Maxhz', 'Noche', 'Colapsoon', 'Maxerosion',
          'Simbalance', 'Nota', 'Velprueba', 'Objetivo', 'Umbraldensidad', 'Reduccionmic', 'Temaenciclo',
          'Padprueba')


def prueba(t):
    m = t.m
    guarda = {}
    for nm in PARS23:
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    try:
        _prueba(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass
        m.mic_reset()


def _prueba(t, m):
    base.par.Velprueba = 100
    base.par.Umbraldensidad = 0.95
    base.par.Objetivo = 'seq1'
    base.par.Temaenciclo = False
    base.par.Colapsoon = False
    base.par.Noche = 4.0                # las autopruebas corren sin noche (comun v70): esta la prueba
    reloj = [absTime.seconds + 300.0]
    FPS = 60.0

    def nuevo(sim=-1.0):
        m.reset_world()
        m.mic_reset()
        base.par.Simbalance = sim
        W = m.world()
        m.sala_de(W)
        return W, m.cfg()

    def pasa(W, c, seg):
        """seg segundos de luz, fotograma a fotograma. Devuelve [(t, quien)] de
        los destellos que han salido."""
        fl = []
        s = W['sala']
        for _ in range(int(round(seg * FPS))):
            reloj[0] += 1.0 / FPS
            n0 = s['n']
            m.sala_luz_tick(W, c, reloj[0])
            if s['n'] != n0:
                fl.append((s['ultimo']['t'], s['ultimo']['quien']))
        return fl

    def tope(fl):
        """El mayor numero de destellos en una ventana de 1 s."""
        ts = [x[0] for x in fl]
        return max([sum(1 for u in ts if 0.0 <= u - a <= 1.0) for a in ts] or [0])

    # 1. los tres estados y su luz
    W, c = nuevo(0.3)
    f1 = pasa(W, c, 3.0)
    e1, l1 = W['sala']['estado'], m.bano_valor(W, c, reloj[0])
    W, c = nuevo(0.7)
    f2 = pasa(W, c, 3.0)
    e2, l2 = W['sala']['estado'], m.bano_valor(W, c, reloj[0])
    W, c = nuevo(1.2)
    f3 = pasa(W, c, 3.0)
    e3, l3, hz3 = W['sala']['estado'], m.bano_valor(W, c, reloj[0]), W['sala']['hz']
    t.check('Simbalance 0,3: deposito, ambar tenue y sin destellos; 0,7: tension, mas luz y mas fria; '
            '1,2: erosion dominante, con el estroboscopio',
            (e1, e2, e3) == (m.DEPOSITO, m.TENSION, m.DOMINANTE) and not f1 and not f2 and len(f3) >= 3
            and l1[3] < 0.2 and l1[0] > l1[1] > l1[2] and l2[3] > l1[3] + 0.1 and l2[2] > l1[2] + 0.1
            and l3[3] > l2[3] and hz3 > 0, 'intensidad %.2f, %.2f y %.2f; %.1f Hz' % (l1[3], l2[3], l3[3], hz3))
    W, c = nuevo(0.3)
    pasa(W, c, 2.0)
    antes = m.bano_valor(W, c, reloj[0])[3]
    m.balance_suma(W, c, reloj[0], crea=1)
    pasa(W, c, 0.2)
    t.check('en deposito el ambar respira con cada nota depositada',
            m.bano_valor(W, c, reloj[0])[3] > antes + 0.02)
    W, c = nuevo(0.7)
    pasa(W, c, 2.0)
    antes = m.bano_valor(W, c, reloj[0])[3]
    W['mic']['t'] = reloj[0]
    t.check('en tension cada onset del microfono anade un pulso breve',
            m.bano_valor(W, c, reloj[0] + 0.01)[3] > antes + 0.15
            and abs(m.bano_valor(W, c, reloj[0] + 2.0)[3] - antes) < 0.02)

    # 2. histeresis
    W, c = nuevo(0.9)
    pasa(W, c, 0.5)
    a = W['sala']['estado']
    base.par.Simbalance = 1.0
    pasa(W, m.cfg(), 0.5)
    b = W['sala']['estado']
    base.par.Simbalance = 0.9
    pasa(W, m.cfg(), 0.5)
    d = W['sala']['estado']
    base.par.Simbalance = 0.79
    pasa(W, m.cfg(), 0.5)
    e = W['sala']['estado']
    t.check('histeresis: entra en erosion dominante con 1,0 y no sale hasta bajar de 0,8',
            (a, b, d, e) == (m.TENSION, m.DOMINANTE, m.DOMINANTE, m.TENSION))

    # 3. el limitador: nunca mas de 3 en 1 s, todos blancos; la prioridad sale en el primer hueco
    W, c = nuevo(10.0)
    fl = pasa(W, c, 10.0)
    blancos = True
    for _ in range(30):
        reloj[0] += 1.0 / FPS
        m.sala_luz_tick(W, c, reloj[0])
        r, g, b_ = m.color_destello(W, reloj[0])
        blancos = blancos and r == g == b_
    t.check('con el balance en 10, nunca mas de 3 destellos en una ventana de 1 s, y todos blancos (r = g = b)',
            len(fl) >= 25 and tope(fl) <= 3 and blancos and all(q == 'estrobo' for _, q in fl),
            '%d destellos en 10 s, %d como mucho en 1 s' % (len(fl), tope(fl)))
    fl = pasa(W, c, 1.0)
    while not pasa(W, c, 1.0 / FPS):        # hasta un destello: la ventana queda llena
        pass
    llena = m.destellos_ventana(W, reloj[0])
    ya = m.limitador_destellos(W, c, reloj[0], 'relampago', prioridad=True)
    tras = pasa(W, c, 3.0)
    t.check('un destello con prioridad, con el limitador lleno, espera al primer hueco: sale el, no el '
            'estroboscopio (que cede), y nunca hay 4 en 1 s',
            llena == 3 and not ya and tras and tras[0][1] == 'relampago' and tope(fl + tras) <= 3
            and sum(1 for _, q in tras if q == 'relampago') == 1 and W['sala']['cedidos'] == 1
            and any(q == 'estrobo' for _, q in tras[1:]),
            'ventana %d; ahora %s; despues %s; cedidos %d'
            % (llena, ya, [q for _, q in tras[:3]], W['sala']['cedidos']))
    base.par.Maxhz = 0.0
    W, c = nuevo(10.0)
    sin = pasa(W, c, 3.0)
    base.par.Maxhz = 3.0
    t.check('Maxhz 0: ningun destello', not sin)

    # 4. al enterrar: un destello, el estroboscopio apagado y la sala a oscuras Noche s
    W, c = nuevo(10.0)
    pasa(W, c, 3.0)
    ev = m.close_cycle(W, c, reloj[0], 'forzado')
    t0 = reloj[0]
    noche = pasa(W, c, 3.9)
    oscuro = m.bano_valor(W, c, reloj[0])[3] == 0.0 and W['sala']['hz'] == 0.0 and m.en_noche(W, reloj[0])
    luego = pasa(W, c, 3.0)
    t.check('al enterrar: un unico destello, el estroboscopio apagado y la sala a oscuras durante Noche (4 s); '
            'despues sigue',
            [q for _, q in noche] == ['fin de ciclo'] and oscuro and not m.en_noche(W, reloj[0])
            and any(q == 'estrobo' for _, q in luego) and 'balance' in ev
            and abs((W['sala']['noche'] or [t0, t0 + 4.0])[1] - t0 - 4.0) < 1e-6 or
            ([q for _, q in noche] == ['fin de ciclo'] and oscuro and W['sala']['noche'] is None),
            '%s' % [q for _, q in noche])

    # 5. el microfono descarta el clic de un destello
    W, c = nuevo()
    m.limitador_destellos(W, c, reloj[0], 'estrobo')
    tras = m.detectar_onset(W, c, 2.0, reloj[0] + 0.05)
    luego = m.detectar_onset(W, c, 2.0, reloj[0] + 0.6)
    t.check('un onset que llega justo despues de un destello se descarta; mas tarde, cuenta',
            not tras and luego and W['mic']['descartados'] == 1)

    # 6. el balance, en escalones: notas y bombo, creacion; caja, aranazos y microfono, erosion
    W, c = nuevo()
    base.par.Nota = 64
    celda = m.note_cell(64)

    def zona(W, c, veces):
        for x in [celda] + list(m.NEIGH[celda]):
            for _ in range(veces):
                m.note_on(W, c, m.GEO, m.cell_note(x), 100, reloj[0])
    zona(W, c, 10)
    m.note_on(W, c, m.GEO, 64, 100, reloj[0])
    s = W['sala']
    crea_notas = sum(x[1] for x in s['bal'])
    occ_notas = sum(W['occ'])
    bombo = next(k for k in range(8) if m.es_impulso(c, k))
    m.erosion(W, c, bombo, 100, reloj[0])
    crea_bombo = sum(x[1] for x in s['bal']) - crea_notas
    occ1 = sum(W['occ'])
    t.check('las notas de los secuenciadores y los pulsos del bombo cuentan como creacion, en escalones de ocupacion',
            crea_notas == occ_notas > 0 and crea_bombo == occ1 - occ_notas > 0 and not sum(x[2] for x in s['bal']),
            'notas %d, bombo %d' % (crea_notas, crea_bombo))
    ara = next(k for k in range(8) if m.es_aranazo(c, k))
    cn = dict(c)
    cn['nivel'] = 13                    # el golpe solo, sin el accidente de la fase 14
    cn13 = dict(cn)
    for _ in range(6):
        m.erosion(W, cn13, ara, 127, reloj[0])
    sin_contar = sum(x[2] for x in s['bal'])
    c23 = dict(c)
    c23['nivel'] = 23
    zona(W, c23, 6)
    occ_m = sum(W['occ'])
    m.erosion_mic(W, c23, reloj[0], 1.0)
    e_mic = sum(x[2] for x in s['bal'])
    occ2 = sum(W['occ'])
    for _ in range(6):
        m.erosion(W, c23, ara, 127, reloj[0])
    e_ara = sum(x[2] for x in s['bal']) - e_mic
    occ3 = sum(W['occ'])
    caja = m.pads_corte(c23)[0]
    zona(W, c23, 4)
    antes_e, occ5 = sum(x[2] for x in s['bal']), sum(W['occ'])
    m.erosion(W, c23, caja, 100, reloj[0])
    e_caja = sum(x[2] for x in s['bal']) - antes_e
    occ6 = sum(W['occ'])
    t.check('la caja, los aranazos y el microfono (con su accidente de la fase 14) cuentan como erosion, en '
            'escalones (lo que no baja un escalon no cuenta; antes de la fase 23, nada)',
            sin_contar == 0 and e_ara == occ2 - occ3 > 0 and e_mic == occ_m - occ2 >= 1
            and e_caja == occ5 - occ6 > 0,
            'aranazos %d, micro %d, caja %d' % (e_ara, e_mic, e_caja))
    crea = sum(x[1] for x in s['bal'])
    eros = sum(x[2] for x in s['bal'])
    b = m.balance(W, m.cfg(), reloj[0])
    W['sala']['bal'] = [[reloj[0], 0, 2]]
    solo = m.balance(W, m.cfg(), reloj[0])
    W['sala']['bal'] = [[reloj[0] - 31.0, 5, 5]]
    viejo = m.balance(W, m.cfg(), reloj[0])
    t.check('balance = erosion / creacion en la ventana de 30 s; erosion sin creacion es erosion dominante; '
            'lo que sale de la ventana no cuenta',
            abs(b - eros / float(crea)) < 1e-9 and solo >= m.BALANCE_SIN_CREACION and viejo == 0.0
            and m.estado_sala(W, m.cfg(), reloj[0], solo) == m.DOMINANTE, 'balance %.2f' % b)

    # 7. colapso
    def corre(seg, sim, on, playing=False):
        W, c = nuevo(sim)
        base.par.Colapsoon = on
        c = m.cfg()
        for k in range(int(seg * 30)):
            reloj[0] += 1.0 / 30.0
            out = m.tick(W, c, reloj[0], 120.0, playing)
            if out.get('ciclo'):
                return out['ciclo'], (k + 1) / 30.0, m.en_noche(W, reloj[0])
        return None, seg, False
    ev, seg, de_noche = corre(20.0, 1.2, True)
    ev2, _, _ = corre(20.0, 1.2, False)
    ev3, _, _ = corre(20.0, 0.9, True)
    base.par.Colapsoon = False
    t.check('colapso: con Colapsoon, Maxerosion (15 s) de erosion dominante cierran el ciclo como colapso; '
            'apagado, no; en tension, tampoco',
            ev is not None and ev['motivo'] == 'colapso' and 14.9 <= seg <= 15.2 and ev2 is None and ev3 is None
            and de_noche, 'a los %.1f s' % seg)
    W, c = nuevo(0.2)
    ev = m.close_cycle(W, c, reloj[0], 'estancado')
    t.check('un cierre por estancado no es colapso', ev['motivo'] == 'estancado')

    # 8. la tabla de ciclos, el DMX y la leyenda
    tb = base.op('ciclos')
    cab = [tb[0, k].val for k in range(tb.numCols)] if tb is not None and tb.numRows else []
    n0 = tb.numRows if tb is not None else 0
    W, c = nuevo(1.5)
    pasa(W, c, 1.0)
    m.registrar_ciclo(W, c, m.close_cycle(W, c, reloj[0], 'forzado'))
    fila = dict(zip(cab, [x.val for x in tb.row(tb.numRows - 1)])) if tb is not None and tb.numRows > n0 else {}
    t.check('la tabla ciclos tiene la columna balance, con el valor al cerrar',
            'balance' in cab and fila.get('balance') == '1.50' and fila.get('motivo') == 'forzado', str(fila))
    cab2 = ['ciclo', 'motivo']

    class _T(object):
        numRows, numCols = 1, 2

        def __getitem__(self, rc):
            class _C(object):
                val = cab2[rc[1]]
            return _C()

        def appendCol(self, v):
            cab2.extend(v)
    t.check('una tabla ciclos anterior gana la columna balance (una sola vez)',
            columna_ciclos(_T(), 'balance') and cab2 == ['ciclo', 'motivo', 'balance']
            and not columna_ciclos(type('X', (_T,), dict(numCols=3))(), 'balance'))
    W, c = nuevo(10.0)
    filas = m.dmx_filas()
    fl = []
    while not fl:
        fl = pasa(W, c, 1.0 / FPS)
    v_fl = m.valores_dmx(W, c, reloj[0], filas)
    v_no = m.valores_dmx(W, c, reloj[0] + 0.2, filas)
    por = dict((f[1], k) for k, f in enumerate(filas))
    o = base.op('dmx_valores')
    o.cook(force=True)
    t.check('dmx_canales (17 canales por defecto) -> dmx_valores: el estroboscopio a 255 durante el destello '
            'y a 0 despues; el bano, entre 0 y 255',
            len(filas) == 17 and v_fl[por['estrobo']] == 255 and v_no[por['estrobo']] == 0
            and 0 < v_fl[por['bano_dimmer']] <= 255 and all(0 <= x <= 255 for x in v_fl)
            and o.numChans == 17 and base.op('dmx_out') is not None, 'canales %d' % o.numChans)
    leg = m.legend()
    t.check('leyenda SALA', 'SALA     balance 10.00 (30 s, forzado)   erosion dominante' in leg
            and 'destellos ' in leg and 'dmx' in leg, ' '.join(l.strip() for l in leg.splitlines() if 'SALA' in l))


run_test(base, prueba)
print('  Ahora: Simbalance 0,3 / 0,7 / 1,2 / 10 recorre los estados (la leyenda SALA los dice);')
print('  Forzarciclo: un destello y 4 s a oscuras. Edita dmx_canales con tus focos.')
print('=' * 66)
