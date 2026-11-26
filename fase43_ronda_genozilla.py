"""
=============================================================================
ESTRATOS - FASE 43: LA RONDA GENOZILLA
=============================================================================
Requiere la fase 42. Cambia como se cuenta la partida en modo juego y le pone
titulos de combate en el centro del mundo.

QUE HACE
--------
  EMPIEZA      la ronda ya no empieza al encender Modojuego: empieza cuando
               aparece el PRIMER MONSTRUO (Trumpzilla, NefanyaMuto o un Godzilla)
               o cuando el MUNDO COLAPSA. Mientras tanto el reloj no corre.
  DURA         Duracionronda (6 min, 360 s).
  COLAPSO      en modo juego el mundo vuelve a poder colapsar: un fin de ciclo
               (la fase 6: estancado, edad maxima, cambio de pattern) o el
               colapso de la sala (fase 23, con Colapsoon). Si colapsa a mitad de
               una ronda, se entierra, la ronda cuenta (recuento, marcada como
               colapso) y empieza otra de 6 min en ese momento.
  FIN          la PARTIDA acaba cuando una ronda llega a sus 6 min (Rondas ya no
               cuenta): recuento, entierro y espera; gana quien domina el globo
               al final. Nuevapartida empieza otra (esperando al monstruo).
  TITULOS      en el centro del mundo, grandes, en una letra de cartel de
               combate (Impact, con sombra):
                 al empezar     3, 2, 1 y «GENoZilla Begins!!!»
                 tras colapso   «RONDA n» (el mundo colapsa)
                 los 5 s finales  estroboscopio y la cuenta 5, 4, 3, 2, 1 (rojo)
                 al acabar      «Stratos x GENoZilla Ends!!!» y quien gana
               El estroboscopio pasa por el limitador comun (3 destellos por
               segundo como mucho).
  APAGADO      Rondagenozilla apagado: las rondas de siempre (fase 32). La
               partida libre (Partidalibre) tampoco tiene rondas. La demo
               GENoZilla de la sala la apaga mientras dura.
  LEYENDA      JUEGO    GENoZilla   esperando al primer monstruo (o al colapso)
               JUEGO    GENoZilla ronda 2   3:12   publico 38   mal 14   (globo)   colapsos 1
               JUEGO    fin GENoZilla   gana el bien   publico 40   mal 12   (2 rondas, 1 colapso)

OPERADORES (en /project1/FASE1)
-------------------------------
  titulo_juego, titulo_juego_sombra, titulo_juego_sub   Text TOP (1280 x 720)
  con_titulo_sombra, con_titulo_texto, con_titulo_juego Over TOP: el titulo
               encima del render. con_rotulo (la leyenda) y out_render (la sala
               virtual) salen de con_titulo_juego.

PARAMETROS (pagina Fase43)
--------------------------
  Rondagenozilla (encendido), Titulojuego (encendido). Duracionronda (Fase32),
  360 s.

PROBAR
------
  Modojuego: la leyenda dice que espera al primer monstruo. Simmonstruo: «3, 2,
  1, GENoZilla Begins!!!» y el reloj de 6:00 empieza. Duracionronda 20 para ver
  el final enseguida: estrobo, 5 ... 1 y «Stratos x GENoZilla Ends!!!».
  Forzarciclo a mitad: el mundo colapsa y empieza la ronda siguiente.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase43_ronda_genozilla.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase43 v1  (la ronda GENoZilla: empieza con el primer monstruo o el colapso; titulos de combate)'
banner(VERSION)

base = require_base(43)
motor = install_core(base, CARPETA, 43)
m = motor.module

page = get_page(base, 'Fase43')
add_par(base, page, 'toggle', 'Rondagenozilla', 'Ronda GENoZilla (desde el primer monstruo; 6 min acaban la partida)',
        True)
add_par(base, page, 'toggle', 'Titulojuego', 'Titulos de la ronda en el centro del mundo', True)
ok('parametros de la fase 43: Rondagenozilla y Titulojuego (encendidos); la ronda dura Duracionronda (%d s)'
   % int(base.par.Duracionronda.eval()) if has_par(base, 'Duracionronda') else
   'parametros de la fase 43: Rondagenozilla y Titulojuego (encendidos)')


# -----------------------------------------------------------------------------
# OPERADORES: el titulo en el centro del mundo
# -----------------------------------------------------------------------------

def letra(nombres):
    """La primera fuente instalada de la lista (Windows o macOS); si no, Arial."""
    import os
    carpetas = ['C:/Windows/Fonts', os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts'),
                '/Library/Fonts', '/System/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    hay = []
    for d in carpetas:
        try:
            hay += [f.replace(' ', '').replace('-', '').replace('_', '').lower() for f in os.listdir(d)]
        except Exception:
            pass
    for n in nombres:
        clave = n.replace(' ', '').lower()
        if any(clave in f for f in hay):
            return n
    return 'Arial'


TIT = "parent().op('motor').module.titulo('%s', absTime.frame)"
LETRA_TIT = letra(['Impact', 'Bebas Neue', 'Anton', 'Arial Black'])
LETRA_SUB = letra(['Bahnschrift', 'Arial Black', 'Arial'])
TAM_TIT, TAM_SUB = 140, 30


def titulo_top(nombre, x, y, tam, color, fuente_, dx=0, dy=0, sub=False):
    o = get_or_make(base, 'textTOP', nombre, x, y)
    setmenu(o, ['outputresolution'], ['custom'], None)
    setp_any(o, ['resolutionw'], 1280)
    setp_any(o, ['resolutionh'], 720)
    setp_any(o, ['font', 'fontfamily'], fuente_)
    setp_any(o, ['alignx'], 'center')
    setp_any(o, ['aligny'], 'center')
    setmenu(o, ['positionunit', 'positionunits'], ['pixels'], None)
    setp_any(o, ['positionx', 'textx'], dx)
    setp_any(o, ['positiony', 'texty'], dy)
    for ch in 'rgb':
        setp_any(o, ['bgcolor' + ch, 'backgroundcolor' + ch], 0.0)
    transp = setp_any(o, ['bgalpha', 'backgroundalpha', 'bgcolora'], 0.0)
    setexpr(o, 'text', TIT % ('sub' if sub else 'texto'))
    if sub:
        for n in ('fontsizex', 'fontsize', 'fontsizey'):
            setp(o, n, tam)
    else:                               # entra grande y se asienta (escala)
        for n in ('fontsizex', 'fontsize', 'fontsizey'):
            setexpr(o, n, '%d * %s' % (tam, TIT % 'escala'))
    for ch in 'rgb':
        if color is None:
            setexpr(o, 'fontcolor' + ch, TIT % ch)
        else:
            setp_any(o, ['fontcolor' + ch, 'color' + ch], color['rgb'.index(ch)])
    for n in ('fontalpha', 'fontcolora'):
        setexpr(o, n, TIT % 'alfa')
    return o, bool(transp)


def over(nombre, arriba, abajo, x, y):
    o = get_or_make(base, 'overTOP', nombre, x, y)
    for i, src in ((0, arriba), (1, abajo)):
        try:
            o.inputConnectors[i].disconnect()
        except Exception:
            pass
        connect(o, src, i)
    return o


render = base.op('render')
sombra, t1 = titulo_top('titulo_juego_sombra', 520, -560, TAM_TIT, (0.0, 0.0, 0.0), LETRA_TIT, dx=7, dy=-7)
texto, t2 = titulo_top('titulo_juego', 520, -640, TAM_TIT, None, LETRA_TIT)
sub, t3 = titulo_top('titulo_juego_sub', 520, -720, TAM_SUB, (0.92, 0.92, 0.96), LETRA_SUB, dy=-120, sub=True)
c1 = over('con_titulo_sombra', sombra, render, 740, -560)
c2 = over('con_titulo_texto', texto, c1, 740, -640)
c3 = over('con_titulo_juego', sub, c2, 740, -720)
rot = base.op('con_rotulo')
if rot is not None:
    try:
        rot.inputConnectors[1].disconnect()
    except Exception:
        pass
    connect(rot, c3, 1)
outr = base.op('out_render')            # la sala virtual: su pantalla ve el titulo
if outr is not None:
    try:
        outr.inputConnectors[0].disconnect()
    except Exception:
        pass
    connect(outr, c3, 0)
if t1 and t2 and t3:
    ok('titulo de la ronda en el centro del mundo: titulo_juego (%s %d, con sombra) y titulo_juego_sub (%s); '
       'con_titulo_juego -> con_rotulo%s' % (LETRA_TIT, TAM_TIT, LETRA_SUB, ' y out_render' if outr else ''))
else:
    info('titulo_juego: no pude hacer transparente el fondo de algun Text TOP; revisa bgalpha')

set_render(base)

leeme(base, 43, """FASE 43 - LA RONDA GENOZILLA
  Con Rondagenozilla, la ronda empieza cuando aparece el primer monstruo o
  cuando el mundo colapsa (un fin de ciclo o el colapso de la sala, que en modo
  juego vuelven a contar) y dura Duracionronda (6 min). Si el mundo colapsa a
  mitad, se entierra, la ronda cuenta y empieza otra de 6 min. La partida acaba
  cuando una ronda llega a sus 6 min. Titulos en el centro del mundo
  (Titulojuego): 3, 2, 1 y GENoZilla Begins!!!; RONDA n tras un colapso; los
  5 s finales, estroboscopio y 5 ... 1; al acabar, Stratos x GENoZilla Ends!!!""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS43 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Umbralnefa', 'Simbalance',
          'Colapsoon', 'Duracionronda', 'Rondas', 'Rondagenozilla', 'Titulojuego', 'Luzjuego')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS43)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ):
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = m.GEO
    W['traza'][i] = 1
    W['h'][i] = m.height_for(m.cfg(), occ)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Simbalance = -1.0
    base.par.Umbralaparicion = 1.0          # Trumpzilla no aparece solo: lo pide la prueba
    base.par.Umbralnefa = 1.0
    base.par.Duracionronda = 20.0
    base.par.Rondas = 4
    base.par.Titulojuego = True
    S = SalaJuego(base, m, absTime.seconds + 9100.0, rondagz=True)
    vis = sorted(m.cara_visible(m.cfg()))
    a = vis[len(vis) // 2]

    # 1. los operadores: el titulo encima del render, la leyenda y la sala encima de el
    rot = base.op('con_rotulo')
    ops = all(base.op(n) is not None for n in ('titulo_juego', 'titulo_juego_sombra', 'titulo_juego_sub',
                                               'con_titulo_juego'))
    cable = rot is None or (len(rot.inputs) > 1 and rot.inputs[1] is base.op('con_titulo_juego'))
    t.check('titulo_juego, su sombra y titulo_juego_sub encima del render (con_titulo_juego); con_rotulo sale de el',
            ops and cable, 'operadores %s, con_rotulo %s' % (ops, cable))

    # 2. con Modojuego la ronda espera al primer monstruo: el reloj no corre
    W, c = S.nuevo(4)
    for k, x in enumerate(vis[::5]):
        _poner(m, W, x, 2 + k % 3)
    conchas0 = len(W['shells'])
    S.reloj[0] += 60.0                      # tres rondas enteras sin monstruo
    S.pasos(W, c, 2)
    J = W['juego']
    leg0 = m._legend_juego(W, c)
    t.check('sin monstruo la ronda no empieza: 60 s despues, ronda 0, sin entierro, el reloj entero y la leyenda '
            'lo dice; sin titulo',
            J['ronda'] == 0 and not J['gz']['corre'] and len(W['shells']) == conchas0 and J['estado'] == 'juego'
            and abs(m.tiempo_ronda(W, c, S.now) - 20.0) < 1e-9 and 'esperando al primer monstruo' in leg0
            and m.titulo_gz(W, c, S.now) is None, leg0.strip())

    # 3. aparece el primer monstruo: empieza la ronda 1 con «3, 2, 1» y «GENoZilla Begins!!!»
    _poner(m, W, a, 4)
    m.aparecer(W, c, S.now, a)
    S.semis(W, c, 1)
    t_ini = W['juego']['t0']
    tits = [m.titulo_gz(W, c, t_ini + u) for u in (0.3, 1.3, 2.3, 3.5, 3.0 + m.T_BEGINS + 0.5)]
    J = W['juego']
    t.check('el primer monstruo empieza la ronda 1 (6 min de reloj desde ahi): 3, 2, 1 y GENoZilla Begins!!!, '
            'que luego se va',
            J['ronda'] == 1 and J['gz']['corre'] and J['gz']['por'] == 'monstruo'
            and [x['texto'] if x else None for x in tits] == ['3', '2', '1', 'GENoZilla Begins!!!', None]
            and all(x['alfa'] > 0.5 for x in tits[:4]) and m.tiempo_ronda(W, c, t_ini) == 20.0,
            '%s' % [x['texto'] if x else None for x in tits])

    # 4. el mundo colapsa a mitad: entierro, la ronda cuenta y empieza otra de 6 min ya
    S.reloj[0] += 5.0
    S.semis(W, c, 1)
    conchas1 = len(W['shells'])
    ev = m.colapso_gz(W, c, S.now, 'estancado')
    J = W['juego']
    tit = m.titulo_gz(W, c, S.now + 0.5)
    t.check('el mundo colapsa a mitad de la ronda: se entierra (estancado), la ronda 1 cuenta como colapso y '
            'empieza la 2 en ese momento, con su titulo; la partida sigue',
            ev is not None and len(W['shells']) == conchas1 + 1 and J['ronda'] == 2 and J['estado'] == 'juego'
            and J['resultados'][-1].get('colapso') == 'estancado' and abs(J['t0'] - S.now) < 1e-9
            and J['gz']['colapsos'] == 1 and tit is not None and tit['texto'] == 'RONDA 2',
            'ronda %d, resultados %s, titulo %s' % (J['ronda'], J['resultados'], tit and tit['texto']))

    # 5. el fin de ciclo de la fase 6 tambien colapsa el mundo en modo juego (cycle_tick)
    W['cambio_pendiente'] = True
    W['compases_ciclo'] = 10 ** 6
    W['beats'] = float(c['beats_per_bar']) - 1e-3
    W['clock']['last_note_t'] = S.now           # el reloj del ciclo corre: hay notas recientes
    W['clock']['stop_t'] = -1e9
    ev2 = m.cycle_tick(W, c, S.now + 0.1, 0.01, 120.0, True)
    J = W['juego']
    t.check('un fin de ciclo (cambio de pattern) en modo juego tambien colapsa: ronda 3',
            ev2 is not None and J['ronda'] == 3 and J['resultados'][-1].get('colapso') == 'cambio de pattern',
            'ronda %d %s' % (J['ronda'], J['resultados'][-1]))
    W['cambio_pendiente'] = False

    # 6. los 5 s finales: estroboscopio y la cuenta 5 ... 1; a los 6 min, fin de la partida y Ends!!!
    t3 = J['t0']
    S.reloj[0] = t3 + 20.0 - 4.6
    S.semis(W, c, 1)
    q = m.final_gz(W, c, S.now)
    tq = m.titulo_gz(W, c, S.now)
    hz = m.hz_juego(W, c, False, S.now)
    antes = m.final_gz(W, c, t3 + 10.0)
    luz = []
    for k in range(int(4.0 * 60)):
        now = S.now + k / 60.0
        m.sala_luz_tick(W, c, now)
        luz.append(m.destellos_ventana(W, now))
    S.reloj[0] = t3 + 20.0 + 0.01
    fin = S.semis(W, c, 1)
    J = W['juego']
    te = m.titulo_gz(W, c, S.now + 1.0)
    rp = m.resultado_partida(J)
    leg = m._legend_juego(W, c)
    t.check('los 5 s finales: estrobo (por el limitador) y la cuenta 5 ... 1 en rojo; a los 20 s (Duracionronda) '
            'la partida acaba (no hay ronda 4 aunque Rondas sea 4) con Stratos x GENoZilla Ends!!! y quien gana',
            antes is None and q == 5 and tq is not None and tq['texto'] == '5' and hz > 0.0
            and 0 < max(luz) <= m.DESTELLOS_MAX and fin is not None and J['estado'] == 'espera'
            and te is not None and te['texto'] == 'Stratos x GENoZilla Ends!!!' and 'GANA' in te['sub']
            and rp['gana'] == J['resultados'][-1]['gana'] and 'fin GENoZilla' in leg,
            'q %s hz %.1f destellos %d fin %s | %s | %s' % (q, hz, max(luz), J['estado'], te and te['sub'],
                                                         leg.strip()))

    # 7. el colapso antes del primer monstruo empieza la ronda 1
    W, c = S.nuevo(4)
    for k, x in enumerate(vis[::5]):
        _poner(m, W, x, 2 + k % 3)
    m.colapso_gz(W, c, S.now, 'edad maxima')
    J = W['juego']
    tb = m.titulo_gz(W, c, S.now + 1.5)
    t.check('antes del primer monstruo, el colapso del mundo empieza la ronda 1 (con 3, 2, 1)',
            J['ronda'] == 1 and J['gz']['corre'] and J['gz']['por'] == 'colapso' and J['resultados'] == []
            and tb is not None and tb['texto'] == '2', 'ronda %d por %s' % (J['ronda'], J['gz'].get('por')))

    # 8. Rondagenozilla apagado: la ronda de la fase 32 (empieza con Modojuego, Rondas rondas)
    S2 = SalaJuego(base, m, absTime.seconds + 9900.0)
    W, c = S2.nuevo(4)
    S2.reloj[0] += 20.5
    S2.semis(W, c, 1)
    J = W['juego']
    t.check('Rondagenozilla apagado: la ronda de siempre (empieza con Modojuego; a los 20 s, la ronda 2) y sin '
            'titulos',
            J.get('gz') is None and J['ronda'] == 2 and J['estado'] == 'juego' and m.titulo_gz(W, c, S2.now) is None,
            'ronda %d' % J['ronda'])


run_test(base, prueba)
print('  Ahora: Modojuego; la ronda empieza con el primer monstruo (Simmonstruo) o el colapso del mundo.')
print('  Duracionronda 20 para ver el final: estrobo, 5 ... 1 y Stratos x GENoZilla Ends!!!')
print('=' * 66)
