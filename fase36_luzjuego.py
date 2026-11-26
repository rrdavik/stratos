"""
=============================================================================
ESTRATOS - FASE 36: LUZ DE JUEGO
=============================================================================
Requiere la fase 35. En modo juego, la luz de sala de la fase 23 cuenta la
partida.

QUE HACE
--------
  BANO         sigue la parte del mal en el globo, con el recuento de la fase
               32: mal / (publico + mal), del ambar (el publico) al frio (el mal),
               y mas intenso cuanto mas mal. Sustituye al balance de la fase 23
               mientras dura la partida (el colapso no entra en modo juego).
  ESTROBO      entra mientras el monstruo esta en forma grande.
  MUERTE       un destello: el relampago de la fase 30 (con prioridad).
  SEGURIDAD    todo pasa por el limitador comun de destellos de la fase 23 (3
               por segundo como mucho, con el estroboscopio y los relampagos).
  FIN DE RONDA la noche de la fase 28 al enterrar.
  Sin interfaz DMX, los eventos quedan en el motor y en la leyenda.
  LEYENDA      LUZJUEGO bano 0.28   estrobo no   destellos 1/s

PROBAR
------
  Con Simbalance apagado (-1) y Modojuego: subir el mal sube el bano;
  Simmonstruo y dejar que devore 8 escalones enciende el estroboscopio; el
  monstruo ahogado da un destello.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase36_luzjuego.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase36 v1  (el devorador: la luz de sala cuenta la partida)'
banner(VERSION)

base = require_base(36)
motor = install_core(base, CARPETA, 36)
m = motor.module

page = get_page(base, 'Fase36')
add_par(base, page, 'toggle', 'Luzjuego', 'Luz de juego', True)
ok('parametros de la fase 36: Luzjuego (encendido)')

set_render(base)

leeme(base, 36, """FASE 36 - LUZ DE JUEGO
  En modo juego (Luzjuego), el bano de la fase 23 sigue la parte del mal en
  el globo (mal / (publico + mal), del ambar al frio); el estroboscopio entra
  con el monstruo en forma grande; su muerte da un relampago (fase 30). Todo
  por el limitador comun (3 destellos por segundo); al enterrar, la noche de
  la fase 28.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS36 = ('Fuente', 'Simcasilla', 'Probllegada', 'Tparada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion',
          'Simbalance', 'Colapsoon', 'Noche', 'Luzjuego', 'Duracionronda')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS36)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _luz(m, W, c, t0, seg, fps=60.0):
    """La luz de sala, fotograma a fotograma: [(t, destellos en el ultimo segundo)]."""
    out = []
    for k in range(int(seg * fps)):
        now = t0 + k / fps
        m.sala_luz_tick(W, c, now)
        out.append((now, m.destellos_ventana(W, now)))
    return out


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Tparada = 30.0
    base.par.Colapsoon = False
    base.par.Simbalance = -1.0
    base.par.Umbralaparicion = 1.0
    S = SalaJuego(base, m, absTime.seconds + 2400.0)

    # 1. el bano sigue la parte del mal
    W, c = S.nuevo(2)
    vis = sorted(m.cara_visible(c))
    for x in vis[:8]:
        W['occ'][x], W['sp'][x], W['own'][x] = 2, m.GEO, m.GEO
    S.semis(W, c, 1)
    _luz(m, W, c, S.now, 3.0)
    poco = list(m.sala_de(W)['bano'])
    for x in vis[:6]:
        W['sp'][x] = m.MAL
    S.semis(W, c, 1)
    _luz(m, W, c, S.now + 3.0, 3.0)
    mucho = list(m.sala_de(W)['bano'])
    leg = m._legend_luzjuego(W, c)
    t.check('con Simbalance apagado, subir el mal sube el bano y lo enfria (del ambar al frio)',
            mucho[3] > poco[3] + 0.2 and mucho[2] > poco[2] and abs(m.parte_mal(W) - 0.75) < 1e-9,
            'intensidad %.2f -> %.2f' % (poco[3], mucho[3]))
    t.check('la linea LUZJUEGO: bano (la parte del mal), estrobo y destellos',
            leg.startswith('  LUZJUEGO bano 0.75   estrobo no   destellos '), leg.strip())

    # 2. el estroboscopio con la forma grande, por el limitador
    W, c = S.nuevo(2)
    b = vis[10]
    W['occ'][b], W['sp'][b], W['own'][b] = 12, m.GEO, m.GEO
    mo = m.aparecer(W, c, S.now, b)
    S.pasos(W, c, 1)
    peq = _luz(m, W, c, S.now, 1.0)
    hz0 = m.sala_de(W)['hz']
    mo['acum'] = int(c['ocupacion_max'])
    m.actualizar_tam(c, mo)
    gran = _luz(m, W, c, S.now + 1.0, 3.0)
    s = m.sala_de(W)
    t.check('el estroboscopio entra con el monstruo en forma grande (no antes) y nunca pasa de 3 destellos por '
            'segundo', hz0 == 0.0 and s['hz'] > 0.0 and max(n for _, n in peq) == 0
            and 0 < max(n for _, n in gran) <= m.DESTELLOS_MAX, 'max %d/s' % max(n for _, n in gran))

    # 3. la muerte: un relampago, con prioridad
    rel = s.get('relampagos', 0)
    t1 = S.now + 4.0
    m.morir(W, c, mo, t1)
    despues = _luz(m, W, c, t1, 1.5)
    t.check('el monstruo ahogado da un destello (el relampago de la fase 30), por el limitador',
            s.get('relampagos', 0) == rel + 1 and s.get('t_relampago') is not None and s['t_relampago'] >= t1
            and max(n for _, n in despues) <= m.DESTELLOS_MAX and s['hz'] == 0.0)

    # 4. fin de ronda: la noche de la fase 28
    base.par.Noche = 4.0
    base.par.Duracionronda = 20.0
    W, c = S.nuevo(2)
    W['juego']['t0'] = S.now - 20.0
    S.semis(W, c, 1)
    t.check('fin de ronda: la noche de la fase 28 al enterrar', W.get('noche') is not None
            and m.sala_de(W)['noche'] is not None and W['juego']['ronda'] == 2)

    # 5. Luzjuego apagado: la luz de la fase 23
    base.par.Noche = 0.0
    base.par.Duracionronda = 360.0
    base.par.Luzjuego = False
    W, c = S.nuevo(2)
    for x in vis[:6]:
        W['occ'][x], W['sp'][x], W['own'][x] = 2, m.MAL, m.GEO
    S.semis(W, c, 1)
    _luz(m, W, c, S.now, 2.0)
    apagada = list(m.sala_de(W)['bano'])
    base.par.Luzjuego = False
    leg = m._legend_luzjuego(W, m.cfg())
    base.par.Luzjuego = True
    t.check('Luzjuego apagado: el bano de la fase 23 (en deposito, aunque el mal domine)',
            apagada[3] < 0.2 and 'apagada' in leg, '%.2f' % apagada[3])


run_test(base, prueba)
print('  Ahora: Modojuego; subir el mal sube el bano; con el monstruo grande, el estroboscopio.')
print('=' * 66)
