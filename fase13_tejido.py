"""
=============================================================================
ESTRATOS - FASE 13: TEJIDO CONECTIVO (RIOS Y CARRETERAS)
=============================================================================
Requiere la fase 12. Une las formaciones con algo que ninguna senal pide:
el sistema lo deduce del estado. Es la fase en la que el tema se lee de
lejos.

QUE HACE
--------
  RIOS (naturaleza)
               nacen en la capital de cada cluster de relieve y bajan celda a
               celda hacia la vecina menos ocupada (empate: la de indice
               menor), sin volver atras, hasta una celda vacia, hasta otro rio
               (confluyen: aguas abajo el rio se ensancha) o hasta Maxrio
               celdas.
  CARRETERAS (ciudad)
               arbol de expansion minima (Kruskal) entre las capitales de
               cluster y las formaciones sueltas con ocupacion de Minvia o
               mas; cada arista va por el camino mas corto de la reticula.
  Los tramos van de centro a centro de celda, a ras del suelo: pasan por
  debajo de las formaciones que cruzan. Usan la misma caja instanciada que
  todo lo demas (geometria 'tejido'), con el shader de la piel: el agua
  brilla, el asfalto es mate. Se recalculan solo cuando cambia la ocupacion.

PROBAR SIN BEATSTEP
-------------------
  Tema ciudad: Sembrarzona dos veces en dos zonas separadas (cambia Nota
  entre una y otra): aparece la carretera que las une. Tema naturaleza:
  Sembrarzona2 dos veces y Sembrar2 en el centro (Nota2) para levantarlo:
  el rio baja de la cumbre hasta la primera celda vacia.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase13_tejido.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase13 v1  (tejido conectivo: rios en naturaleza, carreteras en la ciudad)'
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
ok('pagina Fase13: Rios, Carreteras, Minvia 2, Grosorvia 0,18, Maxrio 12')

# -----------------------------------------------------------------------------
# GEOMETRIA: el tejido, cajas a ras del suelo con el shader de la piel
# -----------------------------------------------------------------------------

materiales_piel(base)
geo = make_instanced(base, 'tejido', 520, 940, 'mat_piel_mineral')
if not setp_any(geo, ['instancea'], 'a'):
    fail('tejido no lee la rugosidad: Instance 2 -> Color A = a')
setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_mineral'")
set_render(base)

leeme(base, 13, """FASE 13 - TEJIDO CONECTIVO
  Naturaleza: los rios nacen en la capital de cada cluster de relieve y
  bajan a la vecina menos ocupada hasta una celda vacia u otro rio (Maxrio).
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
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Rios', 'Carreteras', 'Minvia', 'Maxrio'):
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
    cl = m.clusters(W, c)
    fuentes = sorted(cl['capital'][k] for k in cl['capital'] if W['own'][cl['capital'][k]] == m.ARQ)
    bien, motivo = bool(tj['rios']), ''
    previos = set()
    for camino in tj['rios']:
        if camino[0] not in fuentes:
            bien, motivo = False, 'no nace en una capital de relieve'
        for k in range(1, len(camino)):
            libres = [j for j in m.NEIGH[camino[k - 1]] if j not in camino[:k]]
            if camino[k] != min(libres, key=lambda x: (W['occ'][x], x)):
                bien, motivo = False, 'no baja a la vecina menos ocupada'
        fin = camino[-1]
        if not (W['occ'][fin] <= 0 or fin in previos or len(camino) - 1 >= c['max_rio']):
            bien, motivo = False, 'acaba en %d (ocupacion %d)' % (fin, W['occ'][fin])
        previos.update(camino)
    t.check('naturaleza: el rio nace en la capital del relieve y baja a la vecina menos ocupada '
            'hasta una celda vacia u otro rio', bien and not tj['vias'],
            motivo or 'rios %s' % tj['rios'])
    # confluencia: dos rios que se juntan suman caudal aguas abajo
    lista = [[0, 1, 2], [5, 1]]
    abajo = {0: 1, 1: 2, 5: 1}
    q = m._caudal(lista, abajo)
    t.check('confluencia: aguas abajo de la union pasan los dos rios',
            q.get((1, 2)) == 2 and q.get((0, 1)) == 1 and q.get((5, 1)) == 1, '%s' % q)
    base.par.Maxrio = 1
    t.check('Maxrio: un rio no pasa de Maxrio tramos',
            all(len(r_) - 1 <= 1 for r_ in m.tejido(m.world(), m.cfg())['rios']))
    base.par.Maxrio = 12
    base.par.Rios = False
    t.check('Rios apagado: sin rios', not m.tejido(m.world(), m.cfg())['rios'])
    base.par.Rios = True
    # 3. los tramos van a ras del suelo de sus celdas, y por el camino real
    W, c = m.world(), m.cfg()
    W['vh'] = list(W['h'])
    m._CACHE['inst'] = m.build_instances(W, c, absTime.seconds + 10.0)
    filas = m._CACHE['inst'].get('tejido', [])
    suelo_min = min(m.base_radius(W, c, x) for x in range(m.N))
    suelo_max = max(m.base_radius(W, c, x) for x in range(m.N))
    radios = [math.sqrt(f[0] ** 2 + f[1] ** 2 + f[2] ** 2) for f in filas]
    t.check('los tramos van a ras del suelo (bajo las formaciones)',
            filas and all(suelo_min - 0.05 <= r_ <= suelo_max + 0.05 for r_ in radios),
            '%d medios tramos' % len(filas))
    chop = base.op('i_tejido')
    chop.cook(force=True)
    t.check('i_tejido recibe los tramos (con el canal a)', chop.numSamples == len(filas) and chop['a'] is not None)
    t.check('leyenda TEJIDO', 'TEJIDO' in m.legend() and 'rios' in m.legend())


run_test(base, prueba)
print('  Ahora: con Tema ciudad, Sembrarzona en dos notas lejanas: la carretera')
print('  las une. Con naturaleza, levanta un cluster de relieve (Sembrarzona2 y')
print('  Sembrar2 en el centro): el rio baja hasta la primera celda vacia.')
print('=' * 66)
