"""
Ejecuta los scripts de fase en un TouchDesigner simulado y resume lo que
dicen: versiones, lineas FALLO y AUTOPRUEBA de cada uno.

    python3 pruebas/correr_fases.py            # desde cero: base y fases 3 a 41 (las que haya)
    python3 pruebas/correr_fases.py --hasta=fase24   # solo hasta esa fase
    python3 pruebas/correr_fases.py -v         # con todo el Textport

Despues de las fases simula una sesion corta (SEQ1, SEQ2 y bateria por el
camino del MIDI real, fotograma a fotograma; desde la fase 21, onsets del
microfono: palmadas de la sala virtual, que la sesion oye por su microfono
virtual) y evalua todas las expresiones.
Desde la fase 35, una partida del juego «El devorador» (fases 32 a 37, sin Godzilla): dos
rondas de 60 s con el monstruo, una fila de 3 que lo atrapa, una de 4 que lo
ahoga, un rescate y un brote que crece, por el mismo camino (fotogramas, MIDI y
la tabla de la sala simulada); al final, el recuento y las dos conchas con el
mal donde toca.
Con la sala virtual (sala_virtual v29), la demo GENoZilla de principio a fin
(Demo = genozilla, fotograma a fotograma): los 13 capitulos, la columna
Comprobar de cada uno y, al acabar, FASE1 como estaba (el mundo, las armas,
Fuente y Modojuego).
Luego relanza cada fase (de la 3 a la ultima) sobre el proyecto ya
avanzado, como al refrescar el motor, y comprueba que el mundo se conserva.
Si existe sala_virtual.py, monta la maqueta de la sala tras las fases (la
sesion la oye por su microfono virtual) y la relanza con ellas.
"""

import contextlib
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import td_simulado  # noqa: E402

FASES = ['fase12_base.py', 'fase3_semilla.py', 'fase4_desborde.py', 'fase5_especies.py',
         'fase6_ciclo.py', 'fase7_erosion.py', 'fase8_conchas.py', 'fase9_arqueologia.py',
         'fase10_direccion.py', 'fase11_piel.py', 'fase12_moduladores.py',
         'fase13_tejido.py', 'fase14_destructores.py', 'fase15_era.py', 'fase16_cortes.py', 'fase17_tiempo.py', 'fase18_escenas.py', 'fase19_modular.py',
         'fase21_microfono.py', 'fase22_camara.py', 'fase23_sala.py', 'fase24_personas.py',
         'fase25_huella.py', 'fase26_borrado.py', 'fase27_clasificacion.py', 'fase28_noche.py',
         'fase29_fila.py', 'fase30_relampago.py', 'fase31_historico.py',
         'fase32_juego.py', 'fase33_monstruo.py', 'fase34_zanjas.py', 'fase35_rescate.py', 'fase36_luzjuego.py',
         'fase37_armas.py', 'fase38_trumpzilla.py', 'fase39_mal.py', 'fase40_godzilla.py', 'fase41_hemisferio.py']
SALA = 'sala_virtual.py'           # no es una fase: la maqueta de la instalacion


def correr(sim, archivo, verbose=False):
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            sim.ejecutar(archivo)
        except Exception as e:
            import traceback
            traceback.print_exc(file=buf)
            err = e
    out = buf.getvalue()
    if verbose:
        print(out)
    lineas = out.splitlines()
    version = next((l.split('EJECUTANDO:')[1].strip() for l in lineas if 'EJECUTANDO:' in l), '?')
    fallos = [l for l in lineas if 'FALLO' in l and 'pegame' not in l]
    auto = [l.strip() for l in lineas if 'AUTOPRUEBA OK' in l or 'AUTOPRUEBA FALLIDA' in l]
    bien = err is None and not fallos and auto and all('OK' in a for a in auto)
    print('%-6s %-24s %s' % ('OK' if bien else 'FALLO', archivo, version[:60]))
    if not bien:
        for l in fallos:
            print('         ' + l.strip())
        if err is not None:
            print('         excepcion: %s' % err)
            print('\n'.join('         ' + l for l in out.splitlines()[-15:]))
        if not auto:
            print('         sin AUTOPRUEBA')
    return bien, out


def sesion(sim, compases=48, fps=30.0):
    """SEQ1 en semicorcheas, SEQ2 cada 3 pasos y bateria en negras, por los
    bytes MIDI, fotograma a fotograma a 120 BPM. Con la sala virtual, una
    palmada (Palmada) cada dos negras, por su microfono virtual y la cadena
    del microfono (hasta la fase 21 v3, un clic de Simonset)."""
    base = sim.op('/project1/FASE1')
    sala = sim.op('/project1/SALA')
    palmada = getattr(sala.par, 'Palmada', None) if sala is not None else None
    mm = base.op('midi_callbacks').module
    paso = 60.0 / 120.0 / 4
    fpp = fps * paso
    notas1 = [60, 62, 64, 60, 67, 64, 62, 60]
    notas2 = [48, 50, 53]
    k = 0
    pend = []
    for f in range(int(compases * 16 * fpp)):
        sim.fotograma(1.0 / fps)
        p = int(f / fpp)
        if p != k or f == 0:
            k = p
            for b in pend:
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes(b))
            pend = []
            n1 = notas1[p % len(notas1)]
            mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9C, n1, 90 + p % 30]))
            pend.append([0x8C, n1, 0])
            if p % 3 == 0:
                n2 = notas2[(p // 3) % len(notas2)]
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9D, n2, 70]))
                pend.append([0x8D, n2, 0])
            if p % 8 == 2 and palmada is not None:
                palmada.pulse()
            if p % 16 == 4 and (p // 64) % 2 == 1:
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9F, 36 + (p // 16) % 4, 100]))
    return sim.expresiones()


def partida(sim, fps=30.0, ronda=60.0):
    """La partida de dos rondas. Un director mira el estado del juego y pone a las
    personas en la tabla sala_personas: una fila de 3 sobre la celda del monstruo
    (cae), luego una de 4 (se llena de agua y se ahoga), un rescate de un brote y
    notas del SEQ1 en otro brote (crece). Devuelve lo que paso."""
    base = sim.op('/project1/FASE1')
    m = base.op('motor').module
    mm = base.op('midi_callbacks').module
    tb = base.op('sala_personas')
    base.par.Fuente = 'simulada'
    base.par.Probllegada = 0.0
    base.par.Duracionronda = ronda
    base.par.Rondas = 2
    base.par.Modojuego = True
    tfila = base.par.Tfila.eval()
    base.par.Tfila = 1.0                # las filas cavan al segundo: el monstruo sigue en su celda
    godz = getattr(base.par, 'Godzilla', None)      # la partida prueba a Trumpzilla solo, como las
    godz0 = godz.eval() if godz is not None else None   # autopruebas de las fases 32 a 39 (comun v91)
    if godz is not None:
        godz.val = False
    paso = 60.0 / 120.0 / 4
    fpp = fps * paso
    notas = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76]
    hechos = dict(caidas=0, muertes=0, rescates=0, crece=0, cuatro=0, tres=0, conchas_mal=[])
    fase = ['espera']
    t_fase = [0.0]
    pend = []
    brote_crece = [None, 0]

    def poner(casillas):
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))
        c = m.cfg()
        for k in casillas:
            x, y = m.casilla_xy(c, k)
            tb.appendRow(['%.3f' % x, '%.3f' % y, '1.70'])

    def fila_en(c, W, celda, n):
        k0 = m.casilla_de_celda(c, celda)
        if k0 is None:
            return None
        cols, filas = m.rejilla_sala(c)
        col, fil = k0 % cols, k0 // cols
        ks = [fil * cols + min(cols - 1, max(0, col + d)) for d in range(-(n // 2), n - n // 2)]
        return sorted(set(ks)) if len(set(ks)) == n else None

    poner([])
    n_frames = int(2 * ronda * fps) + int(fps)
    for f in range(n_frames):
        for b in pend:
            mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes(b))
        pend = []
        if f % int(fpp) == 0:
            p = f // int(fpp)
            n1 = notas[p % len(notas)]
            mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9C, n1, 100]))
            pend.append([0x8C, n1, 0])
        sim.fotograma(1.0 / fps)
        W, c = m.world(), m.cfg()
        J = W.get('juego')
        if not J:
            continue
        now = W.get('t') or 0.0
        mo = J['mon']
        vivo = mo['estado'] not in ('espera', 'muere') and mo['celda'] is not None
        libre = vivo and mo['estado'] == 'devora' and mo['celda'] not in J['zanjas'] \
            and mo['celda'] not in (W.get('bloqueadas') or {}) and m.casilla_de_celda(c, mo['celda']) is not None
        brotes = [i for i in range(m.N) if W['occ'][i] > 0 and W['sp'][i] == m.MAL
                  and m.casilla_de_celda(c, i) is not None and i not in J['zanjas']]
        if J['estado'] != 'juego':
            fase[0] = 'acabada'
        elif fase[0] == 'espera' and vivo:     # ya aparecio solo (Umbralaparicion)
            fase[0] = 'tres'
            t_fase[0] = now
        elif fase[0] in ('espera', 'reaparece', 'fin') and not vivo and now - J['t0'] > 4.0 \
                and mo['estado'] == 'espera' and m.celda_aparicion(W, c) is not None:
            base.par.Simceldamon = m.celda_aparicion(W, c)      # vacia, fuera de las zanjas
            base.par.Simmonstruo.pulse()
            fase[0] = 'tres' if fase[0] == 'espera' else 'fin'
            t_fase[0] = now
        elif fase[0] in ('tres', 'cuatro') and libre and now - t_fase[0] > 1.0:
            n = 3 if fase[0] == 'tres' else 4
            ks = fila_en(c, W, mo['celda'], n)
            if ks:
                poner(ks)
                hechos[fase[0]] += 1
                fase[0] = 'fila%d' % n
                t_fase[0] = now
        elif fase[0] == 'fila3' and now - t_fase[0] > c['t_fila'] + 1.0:
            poner([])
            fase[0] = 'rescate'
            t_fase[0] = now
        elif fase[0] == 'rescate' and brotes and now - t_fase[0] > 1.0:
            b = brotes[0]
            k0 = m.casilla_de_celda(c, b)
            ks = [k0] + m.casillas_hacia(W, c, m.NEIGH[b], evitar=[k0])[:int(c['aliados'])]
            base.par.Tfila = 60.0           # los cuatro del rescate no cavan
            poner(ks)
            hechos.setdefault('log', []).append(('rescate', round(now - J['t0'], 1), b, ks,
                                                 [m.celda_de_casilla(W, c, k) for k in ks]))
            fase[0] = 'rescatando'
            t_fase[0] = now
        elif fase[0] == 'rescatando' and now - t_fase[0] > c['t_aliados'] + 1.0:
            poner([])
            base.par.Tfila = 1.0
            fase[0] = 'cuatro'
            t_fase[0] = now
        elif fase[0] == 'fila4' and (mo['estado'] == 'muere' or now - t_fase[0] > c['t_fila'] + 8.0):
            poner([])
            fase[0] = 'reaparece'
            t_fase[0] = now
        if brote_crece[0] is None and brotes and fase[0] not in ('rescate', 'rescatando'):
            brote_crece[0], brote_crece[1] = brotes[-1], W['occ'][brotes[-1]]
        if brote_crece[0] is not None and f % int(fpp) == 1:
            x = brote_crece[0]
            if W['sp'][x] == m.MAL and W['occ'][x] > 0:
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9C, m.cell_note(x), 100]))
                pend.append([0x8C, m.cell_note(x), 0])
                hechos['crece'] = max(hechos['crece'], W['occ'][x] - brote_crece[1])
            else:
                brote_crece[0] = None
        hechos['caidas'] = max(hechos['caidas'], mo.get('caidas', 0))
        if mo['estado'] == 'muere' and mo.get('t_muerte') == now:
            hechos['muertes'] += 1
        hechos['rescates'] = J['rescatados']
        if J['ev'].get('ronda') and J['ev']['ronda'].get('t') == now:
            fase[0] = 'espera'
            brote_crece[0] = None
            poner([])
            base.par.Tfila = 1.0
            hechos['conchas_mal'].append(sorted(i for i, x in enumerate(W['shells'][-1]['sp'])
                                                if x == m.MAL and W['shells'][-1]['occ'][i] > 0))
    W = m.world()
    J = W['juego']
    hechos['resultados'] = [dict(r) for r in J['resultados']]
    hechos['estado'] = J['estado']
    base.par.Modojuego = False
    base.par.Tfila = tfila
    if godz is not None:
        godz.val = godz0
    poner([])
    for _ in range(int((base.par.Noche.eval() + 1.0) * fps)):     # que acabe la noche del ultimo entierro
        sim.fotograma(1.0 / fps)
    m.sala_reset()                      # la sala, como estaba: sin densidad ni personas de la partida
    m._SALA['t_img'] = -99.0
    return hechos


def firma_mundo(W):
    """Lo que la demo no puede cambiar del mundo (el resto, W['t'] y lo del fotograma, si)."""
    return (list(W['occ']), list(W['sp']), list(W['own']), len(W['shells']), len(W.get('escisiones', [])),
            sorted(W.get('esc_celdas', {}).items()), 'juego' in W, W.get('ciclo_n'))


def genozilla(sim, fps=30.0, fps_mic=60.0):
    """La demo GENoZilla de la sala virtual de principio a fin, fotograma a fotograma
    (el microfono a fps_mic en Estatuas y Grito, como en TouchDesigner). Devuelve
    (resultados [(capitulo, bien, que)], FASE1 como estaba)."""
    sala = sim.op('/project1/SALA')
    base = sim.op('/project1/FASE1')
    sm = sala.op('sala_motor').module
    m = base.op('motor').module
    pars = list(sm.ARMAS) + ['Fuente', 'Modojuego', 'Tfila', 'Barsperturn', 'Pasomonstruo', 'Noche', 'Oceano']
    sim.fotograma(1.0 / fps)            # lo que FASE1 hace sola en un fotograma (limpiar celdas vacias) no es de la demo
    antes = (firma_mundo(m.world()), dict((k, getattr(base.par, k).eval()) for k in pars),
             str(sala.par.Vista.eval()), str(sala.par.Modoluz.eval()))
    demo0 = str(sala.par.Demo.eval())
    sala.par.Buclecap = False
    sala.par.Guion = True
    sala.par.Capitulo = sm.CAP_NOMBRES[0]
    sala.par.Demo = 'genozilla'
    tope = int((sum(c['dur'] for c in sm.CAPITULOS) + len(sm.CAPITULOS) * sm.TITULO + 10.0) * fps_mic)
    for _ in range(tope):
        dt = 1.0 / (fps_mic if sm._GZ.get('cap') in sm.MIC_CAPS else fps)
        sim.fotograma(dt)
        if sm._GZ.get('acabada'):
            break
    res = list(sm._GZ.get('resultados') or [])
    despues = (firma_mundo(m.world()), dict((k, getattr(base.par, k).eval()) for k in pars),
               str(sala.par.Vista.eval()), str(sala.par.Modoluz.eval()))
    sala.par.Demo = demo0
    sim.fotograma(1.0 / fps)
    return res, antes == despues, antes, despues


def duplicados():
    """Funciones de nivel de modulo definidas dos veces en el motor o en comun. Python se
    queda con la ultima sin avisar: al fusionar dos ramas, una funcion nueva con el nombre
    de otra la tapa (motor v115: las dos inundar). [(archivo, nombre, lineas)]"""
    import ast
    out = []
    for f in ('estratos_motor.py', 'estratos_comun.py'):
        with open(os.path.join(REPO, f), encoding='utf-8') as fh:
            arbol = ast.parse(fh.read())
        vistas = {}
        for n in arbol.body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                vistas.setdefault(n.name, []).append(n.lineno)
        out += [(f, k, v) for k, v in sorted(vistas.items()) if len(v) > 1]
    return out


def main():
    # las rutas de Windows de los scripts (C:/...) no existen aqui: lo que alguno cree con
    # una ruta asi (la carpeta historico de la fase 31) cae en una carpeta temporal, no en
    # el repositorio
    import tempfile
    os.chdir(tempfile.mkdtemp(prefix='estratos_pruebas_'))
    verbose = '-v' in sys.argv
    hasta = None
    for a in sys.argv[1:]:
        if a.startswith('--hasta='):
            hasta = a.split('=')[1]
    sim = td_simulado.Sim(REPO)
    todo = True
    dup = duplicados()
    print('%-6s funciones definidas dos veces en el motor y en comun: %d' % ('OK' if not dup else 'FALLO', len(dup)))
    for f, k, v in dup:
        print('         %s: %s (lineas %s)' % (f, k, ', '.join(str(x) for x in v)))
    todo = todo and not dup
    for f in FASES:
        if not os.path.exists(os.path.join(REPO, f)):
            continue
        bien, _ = correr(sim, f, verbose)
        todo = todo and bien
        if hasta and f.startswith(hasta):
            break
    if os.path.exists(os.path.join(REPO, SALA)) and not hasta:
        bien, _ = correr(sim, SALA, verbose)
        todo = todo and bien
        # sala_virtual v27: la sala alimenta a FASE1 con su publico (Alimentar; lo prueba su
        # autoprueba). La sesion y la partida son de FASE1, con su propia gente: sin el
        sala = sim.op('/project1/SALA')
        if sala is not None and getattr(sala.par, 'Alimentar', None) is not None:
            sala.par.Alimentar = False
            sala.op('sala_motor').module.alimentar_tick()      # sin avanzar el reloj: la sesion, la de siempre
    with contextlib.redirect_stdout(io.StringIO()):
        malas = sesion(sim)
    m = sim.op('/project1/FASE1/motor').module
    W = m.world()
    print('       mundo tras la sesion: %d celdas ocupadas, %d conchas, nivel %d%s'
          % (m.occupied(W), m.n_shells(W), m.cfg()['nivel'],
             ', %d onsets del microfono' % W['mic']['n'] if m.cfg()['nivel'] >= 21 else ''))
    print('%-6s sesion simulada: %d expresiones con error' % ('OK' if not malas else 'FALLO', len(malas)))
    for m_ in malas[:10]:
        print('         %s.%s: %s' % m_)
    if m.cfg()['nivel'] >= 35:          # fases 32 a 37: una partida de dos rondas
        with contextlib.redirect_stdout(io.StringIO()):
            h = partida(sim)
        rs = h['resultados']
        bien = (h['estado'] == 'espera' and len(rs) == 2 and h['tres'] and h['cuatro'] and h['caidas'] >= 1
                and h['muertes'] >= 1 and h['rescates'] >= 1 and h['crece'] >= 1 and len(h['conchas_mal']) == 2
                and all(len(x) == r['mal'] > 0 for x, r in zip(h['conchas_mal'], rs)))
        todo = todo and bien
        print('%-6s partida simulada: %s   caidas %d, ahogados %d, rescates %d, brote +%d, conchas con mal %s'
              % ('OK' if bien else 'FALLO', '  '.join('ronda %d publico %d mal %d (%s)' % (
                  r['ronda'], r['publico'], r['mal'], r['gana']) for r in rs) or 'sin rondas',
                 h['caidas'], h['muertes'], h['rescates'], h['crece'],
                 '/'.join(str(len(x)) for x in h['conchas_mal'])))
        if not bien:
            print('         %s' % dict((k, v) for k, v in h.items() if k != 'resultados'))
        W = m.world()
    sala = sim.op('/project1/SALA')
    if sala is not None and sala.op('sala_motor') is not None and hasattr(sala.op('sala_motor').module, 'CAPITULOS'):
        with contextlib.redirect_stdout(io.StringIO()):
            res, igual, antes, despues = genozilla(sim)
        bien = len(res) == 13 and all(r[1] for r in res) and igual
        todo = todo and bien
        print('%-6s demo GENoZilla (sala virtual): %d/%d capitulos comprobados, FASE1 %s al salir'
              % ('OK' if bien else 'FALLO', sum(1 for r in res if r[1]), len(res),
                 'como estaba' if igual else 'CAMBIADA'))
        for k, b, que in res:
            if not b:
                print('         capitulo %d: %s' % (k, que))
        if not igual:
            print('         antes   %s' % (antes[1:],))
            print('         despues %s' % (despues[1:],))
        W = m.world()
    # relanzar sobre el proyecto avanzado: el mundo no se pierde
    antes = (m.occupied(W), list(W['occ']))
    print('relanzando las fases sobre el proyecto en el nivel %d' % m.cfg()['nivel'])
    for f in FASES[1:] + [SALA]:
        if not os.path.exists(os.path.join(REPO, f)):
            continue
        bien, _ = correr(sim, f, verbose)
        todo = todo and bien
    m = sim.op('/project1/FASE1/motor').module
    W = m.world()
    igual = list(W['occ']) == antes[1]
    print('%-6s el mundo se conserva al relanzar (%d celdas ocupadas)' % ('OK' if igual else 'FALLO', antes[0]))
    with contextlib.redirect_stdout(io.StringIO()):
        malas2 = sesion(sim, compases=4)
    print('%-6s sesion tras relanzar: %d expresiones con error' % ('OK' if not malas2 else 'FALLO', len(malas2)))
    avisos = sorted(set(sim.avisos))
    print('%-6s avisos de TouchDesigner: %d' % ('OK' if not avisos else 'FALLO', len(avisos)))
    for ruta, texto in avisos[:10]:
        print('         %s: %s' % (ruta, texto))
    return 0 if todo and not malas and not malas2 and igual and not avisos else 1


if __name__ == '__main__':
    sys.exit(main())
