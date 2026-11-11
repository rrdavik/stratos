"""
=============================================================================
ESTRATOS - FASE 30: EL RELAMPAGO
=============================================================================
Requiere la fase 29. Al abrirse una escision, un unico destello blanco en la
sala: el relampago que deja la fulgurita.

QUE HACE
--------
  UN DESTELLO  por escision, al abrirse. Profundizarla (mas personas en la
               fila) no da otro. Solo blanco.
  LIMITADOR    pasa por el limitador comun de la fase 23: como mucho 3
               destellos en cualquier ventana de 1 s, junto con el
               estroboscopio. Si el limitador esta lleno, el relampago espera
               al primer hueco y el estroboscopio cede ese destello (tiene
               prioridad). El microfono descarta su clic, como el de cualquier
               destello.
  EN PANTALLA  la fulgurita recien abierta sube su emisivo un instante.
  DMX          sale por el canal 'estrobo' de dmx_canales, como todos los
               destellos. Si el relampago va a un foco propio, anade una fila
               con la funcion 'relampago' (solo se enciende con el). Sin
               interfaz DMX, el evento queda en el motor y en la leyenda.
  LEYENDA      RELAMPAGO hace 3.2 s   destellos 2/3 en el ultimo segundo   dmx artnet

No tiene parametros nuevos. La pagina Fase30 lleva solo Version30, de solo
lectura.

PROBAR
------
  Formar una fila (Simfila 3, Simformarfila): a los 5 s la leyenda dice
  RELAMPAGO hace 0.0 s. Con Simbalance 10 (el estroboscopio a tope) abrir una
  escision: el contador nunca pasa de 3 y el relampago sale.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase30_relampago.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase30 v1  (relampago: un destello blanco con prioridad al abrirse cada escision)'
banner(VERSION)

base = require_base(30)
motor = install_core(base, CARPETA, 30)
m = motor.module

pagina_version(base, 30, 'Fase 30 (relampago)', VERSION.split('  ')[0])
hay, texto = m.dmx_encontrado()
if hay:
    ok('relampago: sale por el canal estrobo de dmx_canales (%s); con un foco propio, una fila con la '
       'funcion relampago' % texto)
else:
    info('sin DMX (%s): el relampago queda en el motor y en la leyenda' % texto)

set_render(base)

leeme(base, 30, """FASE 30 - EL RELAMPAGO
  Al abrirse una escision, un unico destello blanco. Pasa por el limitador
  de la fase 23 (3 destellos por segundo en toda la sala) con prioridad: si
  esta lleno espera al primer hueco y el estroboscopio se lo cede.
  Profundizar la escision no da otro. La fulgurita recien abierta sube su
  emisivo un instante. DMX: canal estrobo (o una fila 'relampago').""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS30 = ('Fuente', 'Alturamin', 'Alturamax', 'Anchosala', 'Fondosala', 'Tamcasilla', 'Separacioncabezas',
          'Confirmapersona', 'Simcasilla', 'Simfila', 'Espejo', 'Anchoangular', 'Latnorte', 'Latsur', 'Probllegada',
          'Tparada', 'Minfila', 'Tfila', 'Modofila', 'Conchasporpersona', 'Simbalance', 'Maxhz', 'Umbralestrobo',
          'Salidaestrobo', 'Colapsoon', 'Temaenciclo')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS30)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Colapsoon = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    reloj = [absTime.seconds + 1000.0]
    tb = base.op('sala_personas')
    DT = 1.0 / m.CAM_FPS

    def nuevo(sim=0.0, conchas=8):
        m.reset_world()
        m.sala_reset()
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        base.par.Simbalance = sim
        W, c = m.world(), m.cfg()
        for _ in range(conchas):
            m.end_cycle(W, c, reloj[0])
            reloj[0] += 1.0
        m.sala_de(W)
        return W, c

    def paso(W, c, casillas, seg):
        """seg segundos de sala: personas (y filas) y la luz, imagen a imagen.
        Devuelve [(t, quien)] de los destellos."""
        mx = [m.casilla_xy(c, k) + (1.7,) for k in casillas]
        s = W['sala']
        fl = []
        for _ in range(int(round(seg * m.CAM_FPS))):
            reloj[0] += DT
            n0 = s['n']
            m.sala_mundo(W, c, reloj[0], m.tick_personas(W, c, reloj[0], mx))
            m.sala_luz_tick(W, c, reloj[0])
            if s['n'] != n0:
                fl.append((s['ultimo']['t'], s['ultimo']['quien']))
        return fl

    def tope(fl):
        ts = [x[0] for x in fl]
        return max([sum(1 for u in ts if 0.0 <= u - a <= 1.0) for a in ts] or [0])

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)
    k0 = 4 * cols + 3
    linea = [k0, k0 + 1, k0 + 2]

    # 1. una escision, un destello
    fl = paso(W, c, linea, 5.3)
    e = W['escisiones'][-1] if W['escisiones'] else None
    blanco = m.color_destello(W, e['t0'] + 0.01) if e else (0, 1, 2)
    mas = paso(W, c, linea + [k0 + 3, k0 + 4], 1.0)
    t.check('una escision, un destello, en el fotograma en que se abre; profundizarla no da otro',
            e is not None and fl == [(e['t0'], 'relampago')] and e.get('relampago') is True and not mas
            and len(e['cortadas']) == 5 and W['sala']['relampagos'] == 1,
            '%s; al profundizar %s' % ([q for _, q in fl], [q for _, q in mas]))
    t.check('el destello es blanco (r = g = b)', blanco == (1.0, 1.0, 1.0))
    otra = paso(W, c, [], 0.2) + paso(W, c, linea, 5.3)
    t.check('otra escision, otro relampago', [q for _, q in otra] == ['relampago'] and len(W['escisiones']) == 2
            and W['sala']['relampagos'] == 2)

    # 2. con el limitador lleno
    W, c = nuevo(10.0)
    antes = paso(W, c, [], 3.0)
    while not paso(W, c, [], DT):           # hasta un destello del estroboscopio: la ventana, llena
        pass
    llena = m.destellos_ventana(W, reloj[0])
    fila = dict(id=1, personas=3, max=3, casillas=set(linea), origen=linea[0], t0=reloj[0] - 5.0, escision=None)
    e = m.abrir_escision(W, c, fila, linea[0], reloj[0])
    pend = dict(W['sala']['pend'] or {})
    tras = paso(W, c, [], 3.0)
    todos = antes[-3:] + tras
    t.check('con 3 destellos del estroboscopio en el ultimo segundo, el relampago espera (pendiente) y nunca hay '
            '4 en una ventana de 1 s; en el hueco siguiente sale el relampago, no el estroboscopio',
            llena == 3 and e['relampago'] is False and pend.get('quien') == 'relampago'
            and tras and tras[0][1] == 'relampago' and 0.0 < tras[0][0] - e['t0'] < 1.0 and tope(todos) <= 3
            and [q for _, q in tras].count('relampago') == 1 and 'estrobo' in [q for _, q in tras[1:]]
            and W['sala']['cedidos'] == 1 and W['sala']['pend'] is None,
            'ventana %d; luego %s a los %.2f s' % (llena, [q for _, q in tras[:3]],
                                                    (tras[0][0] - e['t0']) if tras else -1.0))
    leg_p = None
    W, c = nuevo(10.0)
    paso(W, c, [], 3.0)
    while not paso(W, c, [], DT):
        pass
    m.abrir_escision(W, c, dict(fila), linea[0], reloj[0])
    reloj0 = reloj[0]
    W['sala']['pend']['t'] = W['sala']['pend'].get('t', reloj0)
    leg_p = m._legend_relampago(W, c)
    t.check('mientras espera, la leyenda dice pendiente', 'pendiente' in leg_p, leg_p.strip())

    # 3. en pantalla y por DMX
    W, c = nuevo()
    paso(W, c, linea, 5.3)
    e = W['escisiones'][-1]
    b0 = m.brillo_fulgurita(c, e, e['t0'])
    b1 = m.brillo_fulgurita(c, e, e['t0'] + 5.0)
    c29 = dict(c)
    c29['nivel'] = 29
    nuc0 = [f for f in m.filas_fulgurita(W, c, e, e['t0']) if int(f[12] // 2) == m.NUCLEO][0]
    nuc1 = [f for f in m.filas_fulgurita(W, c, e, e['t0'] + 5.0) if int(f[12] // 2) == m.NUCLEO][0]
    t.check('la fulgurita recien abierta sube su emisivo un instante (y vuelve); antes de la fase 30, no',
            b0 > 3.0 and b1 == 1.0 and max(nuc0[9:12]) > 2.0 * max(nuc1[9:12]) and max(nuc1[9:12]) <= 1.0
            and m.brillo_fulgurita(c29, e, e['t0']) == 1.0, 'brillo %.1f -> %.1f' % (b0, b1))
    filas_dmx = m.dmx_filas() + [[18, 'relampago', 'foco del relampago']]
    por = dict((f[1], k) for k, f in enumerate(filas_dmx))
    v_r = m.valores_dmx(W, c, e['t0'] + 0.01, filas_dmx)
    v_d = m.valores_dmx(W, c, e['t0'] + 0.5, filas_dmx)
    m.limitador_destellos(W, c, e['t0'] + 2.0, 'estrobo')
    v_e = m.valores_dmx(W, c, e['t0'] + 2.01, filas_dmx)
    t.check('por DMX: el relampago enciende el canal estrobo y, si la hay, la fila relampago (que el '
            'estroboscopio no enciende)',
            v_r[por['estrobo']] == 255 and v_r[por['relampago']] == 255 and v_d[por['estrobo']] == 0
            and v_d[por['relampago']] == 0 and v_e[por['estrobo']] == 255 and v_e[por['relampago']] == 0)
    tras = m.detectar_onset(W, c, 2.0, e['t0'] + 0.05)
    t.check('el microfono descarta el clic del relampago', not tras and W['mic']['descartados'] == 1)

    # 4. por la sala simulada y la leyenda
    W, c = nuevo()
    reloj[0] = absTime.seconds
    base.par.Simcasilla = k0
    base.par.Simfila = 3
    m.on_pulse('Simformarfila')
    c = m.cfg()
    for _ in range(int(5.3 * m.CAM_FPS)):
        reloj[0] += DT
        m._SALA['t_img'] = -99.0
        m.sala_tick(W, c, reloj[0])
    tr = W['sala'].get('t_relampago')
    leg = m.legend()
    linea_l = ' '.join(l.strip() for l in leg.splitlines() if 'RELAMPAGO' in l)
    t.check('Simformarfila: a los 5 s, la escision y su relampago; la linea RELAMPAGO',
            len(W['escisiones']) == 1 and tr == W['escisiones'][0]['t0']
            and 'RELAMPAGO ' in leg and 'en el ultimo segundo' in leg and ('dmx' in linea_l), linea_l)
    t.check('pagina Fase30: solo Version30, de solo lectura',
            has_par(base, 'Version30') and base.par.Version30.readOnly
            and str(base.par.Version30.eval()).startswith('fase30 v'))


run_test(base, prueba)
print('  Ahora: Simfila 3 y Simformarfila: a los 5 s, la leyenda RELAMPAGO dice hace 0.0 s.')
print('  Con Simbalance 10, el contador de destellos nunca pasa de 3.')
print('=' * 66)
