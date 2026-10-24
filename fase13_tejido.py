"""
=============================================================================
ESTRATOS - FASE 13: TEJIDO CONECTIVO (RIOS Y CARRETERAS)
=============================================================================
Requiere la fase 12. Une las formaciones con algo que ninguna senal pide:
el sistema lo deduce del estado. Es la fase en la que el tema se lee de
lejos.

QUE HACE
--------
  RIOS (naturaleza, v2)
               nacen en las cumbres (las celdas con relieve mas altas que sus
               vecinas, y las capitales de relieve) y bajan por el suelo real
               (el suelo de la celda mas el relieve de la fase 11 v5) a la
               vecina mas baja (empate: la de indice menor), hasta una
               hondonada o un llano, hasta otro rio (confluyen: aguas abajo
               el rio se ensancha) o hasta Maxrio tramos. Las hondonadas (las
               lagunas de la fase 8) donde acaba un rio se llenan: lagos
               (Lagos).
               Son cintas de agua (geometria 'rios', mat_piel_agua): azul
               reservado (Colorrio, fuera de la paleta de conchas), sin tintes
               de celda, de pad ni de concha, especular alto (rugosidad 0,1) y
               un emisivo bajo (Emisivorio) para la cara de sombra. Van sobre
               el terreno, con un pequeno desfase, por los bordes de las celdas
               y lejos de su centro: bordean la formacion y la loseta de luz.
               Ancho por caudal: de Anchorio a Anchomaxrio.
  CARRETERAS (ciudad)
               arbol de expansion minima (Kruskal) entre las capitales de
               cluster y las formaciones sueltas con ocupacion de Minvia o
               mas; cada arista va por el camino mas corto de la reticula.
  Las carreteras van de centro a centro de celda, a ras del suelo: pasan
  por debajo de las formaciones que cruzan (geometria 'tejido', el shader
  de la piel: el asfalto es mate). Se recalculan solo cuando cambia la
  ocupacion (los rios, tambien cuando cambia el relieve).

PROBAR SIN BEATSTEP
-------------------
  Tema ciudad: Sembrarzona dos veces en dos zonas separadas (cambia Nota
  entre una y otra): aparece la carretera que las une. Tema naturaleza:
  Sembrarzona2 dos veces y Sembrar2 en el centro (Nota2) para levantarlo:
  el rio baja de la cumbre por las laderas hasta el llano.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase13_tejido.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase13 v2  (rios azules: bajan por el suelo real, cintas que bordean, ancho por caudal, lagos)'
banner(VERSION)

base = require_base(13)
motor = install_core(base, CARPETA, 13)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase13)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase13')
add_par(base, page, 'toggle', 'Rios', 'Rios (naturaleza)', True)
add_par(base, page, 'toggle', 'Carreteras', 'Carreteras (ciudad)', True)
add_par(base, page, 'int', 'Minvia', 'Ocupacion minima de una formacion suelta con carretera', 2, 1, 16,
        clamp=True)
add_par(base, page, 'float', 'Grosorvia', 'Ancho de rios y carreteras', 0.18, 0.02, 1.0)
add_par(base, page, 'int', 'Maxrio', 'Longitud maxima de un rio (celdas)', 12, 1, 60, clamp=True)
add_par(base, page, 'rgb', 'Colorrio', 'Color de los rios (azul reservado)', m.COL_RIO)
add_par(base, page, 'float', 'Anchorio', 'Ancho minimo de un rio', 0.10, 0.01, 1.0)
add_par(base, page, 'float', 'Anchomaxrio', 'Ancho maximo de un rio (caudal)', 0.34, 0.01, 1.5)
add_par(base, page, 'float', 'Emisivorio', 'Emisivo del agua (cara de sombra)', 0.25, 0.0, 1.0)
add_par(base, page, 'toggle', 'Lagos', 'Lagos en las hondonadas', True)
ok('pagina Fase13: Rios, Carreteras, Minvia 2, Grosorvia 0,18 (carreteras), Maxrio 12; v2: Colorrio '
   '(OKLCH 0,55 0,15 255), Anchorio 0,10, Anchomaxrio 0,34, Emisivorio 0,25, Lagos')

# -----------------------------------------------------------------------------
# GEOMETRIA: el tejido, cajas a ras del suelo con el shader de la piel
# -----------------------------------------------------------------------------

materiales_piel(base)
geo = make_instanced(base, 'tejido', 520, 940, 'mat_piel_mineral')
if not setp_any(geo, ['instancea'], 'a'):
    fail('tejido no lee la rugosidad: Instance 2 -> Color A = a')
setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_mineral'")
# v2: los rios, en su geometria, con el material del agua (azul reservado, emisivo bajo)
geo = make_instanced(base, 'rios', 520, 860, 'mat_piel_agua')
if not setp_any(geo, ['instancea'], 'a'):
    fail('rios no lee la rugosidad: Instance 2 -> Color A = a')
setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_agua'")
set_render(base)

leeme(base, 13, """FASE 13 - TEJIDO CONECTIVO
  Naturaleza (v2): los rios nacen en las cumbres y bajan por el suelo real
  (suelo + relieve) a la vecina mas baja, hasta un llano, otro rio o Maxrio;
  en una hondonada, lago (Lagos). Cintas azules (geometria rios,
  mat_piel_agua: Colorrio, Emisivorio) que bordean el centro de las celdas;
  ancho por caudal (Anchorio a Anchomaxrio).
  Ciudad: carreteras por Kruskal entre capitales y formaciones sueltas con
  ocupacion >= Minvia, por el camino mas corto de la reticula.
  A ras del suelo, bajo las formaciones (geometria tejido). Grosorvia.
  Prueba: Sembrarzona en dos zonas separadas.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Rios', 'Carreteras', 'Minvia', 'Maxrio', 'Lagos'):
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


def _prueba(t, m):
    import math
    base.par.Velprueba = 100

    def zona(pulso, nota, veces=2):
        base.par.Nota = nota
        base.par.Nota2 = nota
        for _ in range(veces):
            m.on_pulse(pulso)
    # 1. carreteras: dos zonas separadas, la carretera que las une
    base.par.Tema = 'ciudad'
    m.reset_world()
    a_nota, b_nota = 64, 70                 # mismo anillo, meridianos opuestos
    zona('Sembrarzona', a_nota)
    zona('Sembrarzona', b_nota)
    W, c = m.world(), m.cfg()
    cl = m.clusters(W, c)
    caps = sorted(cl['capital'].values())
    tj = m.tejido(W, c)
    red = {}
    for x, y in tj['vias']:
        red.setdefault(x, set()).add(y)
        red.setdefault(y, set()).add(x)

    def unidos(x, y):
        vistos, pila = {x}, [x]
        while pila:
            z = pila.pop()
            for w in red.get(z, ()):
                if w not in vistos:
                    vistos.add(w)
                    pila.append(w)
        return y in vistos
    d = len(m.camino_corto(caps[0], caps[-1])) - 1 if len(caps) == 2 else -1
    t.check('ciudad, Sembrarzona en dos zonas: la carretera une sus capitales por el camino mas corto',
            len(caps) == 2 and unidos(caps[0], caps[1]) and len(tj['vias']) == d and not tj['rios'],
            'capitales %s, %d tramos (camino %d)' % (caps, len(tj['vias']), d))
    # una formacion suelta con ocupacion >= Minvia entra en la red (se recalcula)
    sola = m.note_cell(67)                  # entre las dos zonas, sin tocarlas
    base.par.Nota = m.cell_note(sola)
    for _ in range(3):
        m.on_pulse('Sembrar')
    W, c = m.world(), m.cfg()
    tj2 = m.tejido(W, c)
    nodos = m.nodos_via(W, c)
    t.check('una formacion suelta (ocupacion >= Minvia) entra en la red: arbol de expansion minima',
            sola in nodos and len(tj2['arbol']) == len(nodos) - 1 and tj2 is not tj,
            '%d nodos, %d aristas' % (len(nodos), len(tj2['arbol'])))
    t.check('se guarda: sin cambio de ocupacion no se recalcula', m.tejido(W, c) is tj2)
    # Kruskal: ninguna otra union de los nodos es mas corta
    total = sum(dd for _, _, dd in tj2['arbol'])
    import itertools
    mejor = None
    pares = [(len(m.camino_corto(x, y)) - 1, x, y) for x, y in itertools.combinations(nodos, 2)]
    for combo in itertools.combinations(pares, len(nodos) - 1):
        padre = dict((x, x) for x in nodos)

        def r(x):
            while padre[x] != x:
                x = padre[x]
            return x
        bien = True
        for dd, x, y in combo:
            if r(x) == r(y):
                bien = False
                break
            padre[r(x)] = r(y)
        if bien:
            s_ = sum(dd for dd, _, _ in combo)
            mejor = s_ if mejor is None else min(mejor, s_)
    t.check('Kruskal: el arbol es el de menor longitud total', mejor is not None and total == mejor,
            '%d (minimo %s)' % (total, mejor))
    base.par.Carreteras = False
    t.check('Carreteras apagado: sin carreteras', not m.tejido(m.world(), m.cfg())['vias'])
    base.par.Carreteras = True
    # 2. rios: un cluster de relieve con una cumbre
    base.par.Tema = 'naturaleza'
    m.reset_world()
    zona('Sembrarzona2', 64)
    base.par.Nota2 = 64
    for _ in range(12):
        m.on_pulse('Sembrar2')
    W, c = m.world(), m.cfg()
    tj = m.tejido(W, c)
    ter = m.terreno(W, c)
    G = [m.suelo(W, c, x) + ter['centro'][x] for x in range(m.N)]
    bien, motivo = bool(tj['rios']), ''
    previos = set()
    for camino in tj['rios']:
        f0 = camino[0]
        if not (ter['centro'][f0] > 0 and all(G[f0] > G[j] for j in m.NEIGH[f0])) \
                and f0 not in m.clusters(W, c)['capital'].values():
            bien, motivo = False, 'no nace en una cumbre'
        for k in range(1, len(camino)):
            libres = [j for j in m.NEIGH[camino[k - 1]] if j not in camino[:k]]
            if camino[k] != min(libres, key=lambda x: (G[x], x)) or G[camino[k]] >= G[camino[k - 1]]:
                bien, motivo = False, 'no baja a la vecina mas baja'
        fin = camino[-1]
        libres = [j for j in m.NEIGH[fin] if j not in camino]
        if not (fin in previos or len(camino) - 1 >= c['max_rio'] or not libres
                or min(G[j] for j in libres) >= G[fin] - 1e-6):
            bien, motivo = False, 'acaba en %d sin llano ni hondonada' % fin
        previos.update(camino)
    t.check('naturaleza: el rio nace en una cumbre y baja por el suelo real (suelo + relieve) a la vecina mas '
            'baja hasta un llano, una hondonada u otro rio', bien and not tj['vias'],
            motivo or 'rios %s' % tj['rios'])
    # confluencia: dos rios que se juntan suman caudal aguas abajo, y el tramo de abajo es mas ancho
    lista = [[0, 1, 2], [5, 1]]
    abajo = {0: 1, 1: 2, 5: 1}
    q = m._caudal(lista, abajo)
    t.check('dos rios confluyen: aguas abajo pasan los dos y el tramo de abajo es mas ancho (%.2f -> %.2f)'
            % (m.ancho_rio(c, 1), m.ancho_rio(c, 2)),
            q.get((1, 2)) == 2 and q.get((0, 1)) == 1 and q.get((5, 1)) == 1
            and m.ancho_rio(c, 1) == c['ancho_rio'] < m.ancho_rio(c, 2) < m.ancho_rio(c, 9) == c['ancho_max_rio'],
            '%s' % q)
    base.par.Maxrio = 1
    t.check('Maxrio: un rio no pasa de Maxrio tramos',
            all(len(r_) - 1 <= 1 for r_ in m.tejido(m.world(), m.cfg())['rios']))
    base.par.Maxrio = 12
    base.par.Rios = False
    t.check('Rios apagado: sin rios', not m.tejido(m.world(), m.cfg())['rios'])
    base.par.Rios = True
    # 3. una cordillera con valles: los rios nacen arriba, bajan y son azules
    W, c = m.world(), m.cfg()
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, absTime.seconds + 10.0)
    filas = m._CACHE['inst'].get('rios', [])
    azul = m.color_rio(c)
    ter = m.terreno(W, c)
    sobre = []
    for f in filas:
        r_ = math.sqrt(f[0] ** 2 + f[1] ** 2 + f[2] ** 2)
        d = (f[0] / r_, f[1] / r_, f[2] / r_)
        cel = max(range(m.N), key=lambda x: sum(d[q] * m.NORMALS[x][q] for q in range(3)))
        sobre.append(r_ - m.suelo(W, c, cel) - m.alto_en(ter, d))
    t.check('cordillera con valles: los rios son cintas azules (%d tramos) apoyadas en el terreno, sin tintes'
            % len(filas), filas and all(tuple(f[9:12]) == tuple(azul) for f in filas)
            and all(-0.02 <= x <= 0.25 for x in sobre) and all(f[7] < 0.01 for f in filas)
            and not m._CACHE['inst'].get('tejido'), 'desfase %.3f a %.3f' % (min(sobre or [0]), max(sobre or [0])))
    h_hue = m.palette_hue
    t.check('el azul de los rios es OKLCH 0,55 0,15 255 y esta fuera de la paleta de conchas',
            m._en_banda(255.0) and all(abs(a - b) < 1e-6 for a, b in zip(m.COL_RIO, m.oklch_to_srgb(0.55, 0.15, 255.0)[0])))
    # 4. una nota del SEQ1 en una celda con rio: la celda se ilumina y el rio sigue azul y fuera de la loseta
    ca = m.cauces(W, c)
    cel = next(iter(sorted(ca['por_celda']))) if ca['por_celda'] else -1
    antes = [list(f) for f in filas]
    if cel >= 0:
        m.note_on(W, c, m.GEO, m.cell_note(cel), 100, absTime.seconds + 10.0, 120.0)
    inst = m.build_instances(W, c, absTime.seconds + 10.0)
    luz = [f for f in inst.get('luz_celda', [])
           if sum(f[q] * m.NORMALS[cel][q] for q in range(3)) > 0.999 * math.sqrt(sum(v * v for v in f[:3]))]
    lado = max([max(f[6], f[8]) for f in luz] or [0.0]) / max(1e-6, m.suelo(W, c, cel))
    lejos = min([math.acos(max(-1.0, min(1.0, sum(d[q] * m.NORMALS[cel][q] for q in range(3)))))
                 for d, _ in ca['por_celda'].get(cel, [])] or [0.0])
    t.check('nota del SEQ1 sobre una celda con rio: la loseta se ilumina y el rio sigue azul, sin pasar por ella',
            cel >= 0 and luz and [list(f) for f in inst.get('rios', [])] == antes and lejos > 0.5 * lado,
            'celda %d, rio a %.3f rad del centro, loseta %.3f' % (cel, lejos, 0.5 * lado))
    # 5. veinte conchas apiladas: ninguna del azul de los rios
    t.check('veinte conchas apiladas: ningun tono de concha en la banda del azul de los rios (235-275)',
            not any(235.0 <= h_hue(n, c['paleta_tono']) < 275.0 for n in range(20))
            and not any(m._en_banda(h_hue(n, c['paleta_tono'])) for n in range(20)))
    # 6. globo girando: el agua se lee en la cara de sombra (emisivo) y no se tine
    mat = base.op('mat_piel_agua')
    uni = m.uniformes_piel(W, c, absTime.seconds)
    t.check('cara de sombra: el agua lleva su emisivo (Emisivorio %.2f) y no toma los tintes del borde'
            % c['emisivo_rio'], mat is not None and uni['uAgua'][0] == c['emisivo_rio'] > 0
            and 'uAgua' in PIEL_PIXEL and 'base * uAgua.x' in PIEL_PIXEL
            and nombre_op(base.op('rios').par.material.eval()) == 'mat_piel_agua')
    # 7. lagos: un rio que acaba en una hondonada (laguna de la fase 8) la llena
    Wl = m.new_world()
    cl_ = dict(c)
    for k in range(3):
        m.end_cycle(Wl, cl_, 10.0 + k)
    a_ = m.note_cell(64)
    b_ = m.NEIGH[a_][0]
    m.cut(Wl, cl_, b_, 2, 0, 20.0)
    Wl['occ'][a_], Wl['own'][a_], Wl['sp'][a_], Wl['vel'][a_] = 12, m.ARQ, m.ARQ, 100
    Wl['h'][a_] = Wl['vh'][a_] = m.height_for(cl_, 12)
    ca = m.cauces(Wl, cl_)
    instl = m.build_instances(Wl, cl_, 30.0)
    lagos = [f for f in instl.get('rios', []) if f[6] > 4 * cl_['ancho_max_rio']]
    base.par.Lagos = False
    sin = m.cauces(Wl, m.cfg())['lagos']
    base.par.Lagos = True
    t.check('lagos: el rio acaba en la hondonada (laguna %.2f) y la llena de agua; Lagos apagado, sin lago'
            % m.laguna(Wl, cl_, b_), b_ in ca['lagos'] and lagos and not sin,
            'lagos %s' % ca['lagos'])
    chop = base.op('i_rios')
    chop.cook(force=True)
    t.check('i_rios recibe las cintas (con el canal a)', chop.numSamples >= 1 and chop['a'] is not None)
    t.check('leyenda TEJIDO', 'TEJIDO' in m.legend() and 'rios' in m.legend() and 'lagos' in m.legend())

run_test(base, prueba)
print('  Ahora: con Tema ciudad, Sembrarzona en dos notas lejanas: la carretera')
print('  las une. Con naturaleza, levanta un cluster de relieve (Sembrarzona2 y')
print('  Sembrar2 en el centro): el rio azul baja de la cumbre por las laderas.')
print('=' * 66)
