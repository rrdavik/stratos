"""
=============================================================================
ESTRATOS - FASE 11: LA PIEL (GENERADORES CON TEMATICA)
=============================================================================
Requiere la fase 10. Cada pieza que el motor ya coloca deja de ser una caja
y pasa a ser un modelo del tema activo (Tema: naturaleza o ciudad). Las
especies conservan su logica formal: SEQ1 en racimo oblicuo, SEQ2 en
malla ortogonal.

                     NATURALEZA                  CIUDAD
    SEQ1             vegetacion                  ciudad informal
    SEQ2             relieve (basalto)           ciudad planificada

    ocupacion  1     brote / columna             caseta / bloque
               2+    tronco y copa / columnas    anadidos / plantas
               5+    arboleda / mesetas          pasarelas / manzana
               7+    bosque / meseta continua    barrio / podio
               9+    arbol madre / cumbre        torre de antenas / rascacielos
    (los umbrales son los de la fase 4: Umbralram, Umbralfusion, Umbralcorona)

QUE ANADE
---------
  CATALOGO     tabla 'catalogo' (tema especie estado variante modelo) y las
               cadenas de transito. Los modelos se generan dentro de TD, en
               'modelos': un L-system con angulos de 30 grados para la
               vegetacion, prismas hexagonales (Tube SOP de 6 lados) para el
               basalto y pilas de cajas (Box SOP) para la ciudad. Un Geometry
               COMP instanciado por modelo, pulido y poroso (hasta la fase 12).
  VECINDAD     P = ocupacion + Pesovecina x ocupacion de las vecinas de su
               especie. Dos vecinas con P >= Umbralvecindad se funden en un
               cluster (union-find), junto con la fusion por desborde de la
               fase 4. La capital es la celda mas ocupada (empate: indice menor).
  PUENTES      cada celda del cluster lleva un puente hacia cada vecina del
               cluster: dosel, meseta, pasarela o podio. La capital lleva la
               pieza protagonista segun el tamano: 2-3 celdas, 4-6, 7 o mas.
  COMPUESTOS   juego del caos: incrustar, girar y apilar, orbitar, hundir,
               inclinar. Piezas = min(ocupacion, Maxpiezas). Todo lo elige el
               mapa logistico (r = Caos) sembrado con la velocidad fundadora y
               la celda: la misma historia da el mismo compuesto.
  TRANSITOS    stop-motion. Nacimiento con rebote y destello (un paso como
               mucho); crecimiento en un paso. Fusion y coronacion son
               cadenas de etapas que avanzan una por gate en el cluster
               (Avance = gates) o cada Pasosetapa pasos (Avance = pasos).
               La erosion las recorre hacia atras; el fin de ciclo las cierra.
  PARTICULAS   esporas, polvo y obreros: cajas que calcula el motor.

PROBAR SIN BEATSTEP
-------------------
  Sembrarzona (Nota, SEQ1) o Sembrarzona2 (Nota2, SEQ2) dos veces con cada
  tema: cluster, puentes y protagonista. Sembrar en la misma celda con
  Velprueba 100 y luego 101 da dos compuestos distintos; con 100, el mismo.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase11_piel.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase11 v1  (la piel: catalogo de modelos, clusters, puentes, compuestos y transitos)'
banner(VERSION)

base = require_base(11)
motor = install_core(base, CARPETA, 11)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase11)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase11')
add_par(base, page, 'menu', 'Tema', 'Tema', 'naturaleza', menu=m.TEMAS,
        menu_labels=['Naturaleza', 'Ciudad'])
add_par(base, page, 'float', 'Pesovecina', 'Peso de las vecinas en la presion', 0.5, 0.0, 2.0)
add_par(base, page, 'float', 'Umbralvecindad', 'Presion para fundirse (cluster)', 4.0, 1.0, 20.0)
add_par(base, page, 'int', 'Mincluster', 'Celdas minimas de un cluster', 2, 2, 20, clamp=True)
add_par(base, page, 'float', 'Caos', 'Mapa logistico: r (compuestos)', 3.91, 3.5, 4.0)
add_par(base, page, 'int', 'Maxpiezas', 'Piezas maximas por compuesto', 6, 1, 12, clamp=True)
add_par(base, page, 'menu', 'Avance', 'Las obras avanzan', 'gates', menu=m.AVANCES,
        menu_labels=['Una etapa por gate en el cluster', 'Una etapa cada Pasosetapa pasos'])
add_par(base, page, 'int', 'Pasosetapa', 'Pasos por etapa (y al deshacerse)', 2, 1, 16, clamp=True)
add_par(base, page, 'float', 'Rebote', 'Rebote del nacimiento', 0.2, 0.0, 0.6)
add_par(base, page, 'pulse', 'Sembrarzona', 'Sembrar Nota y sus vecinas (SEQ1, prueba)')
add_par(base, page, 'pulse', 'Sembrarzona2', 'Sembrar Nota2 y sus vecinas (SEQ2, prueba)')
ok('pagina Fase11: Tema (naturaleza), Pesovecina 0,5, Umbralvecindad 4, Mincluster 2, Caos 3,91, '
   'Maxpiezas 6, Avance (gates), Pasosetapa 2, Rebote 0,2, Sembrarzona, Sembrarzona2')

# -----------------------------------------------------------------------------
# CATALOGO (tabla editable: tema especie estado variante modelo)
# -----------------------------------------------------------------------------

filas_def = [list(m.CATALOGO_COLS)] + [[str(x) for x in f] for f in m.CATALOGO_FILAS]
cat = get_or_make(base, 'tableDAT', 'catalogo', -440, -480)
actual = [[cell.val for cell in cat.row(r)] for r in range(cat.numRows)]
if not actual or actual[0][:5] != list(m.CATALOGO_COLS) or actual == cat.fetch('defecto', None):
    cat.clear()
    for f in filas_def:
        cat.appendRow(f)
    cat.store('defecto', filas_def)
    ok('catalogo: %d filas (modelos de los dos temas y cadenas de transito)' % (len(filas_def) - 1))
elif actual != filas_def:
    info('catalogo editado a mano: se conserva. Para volver al de por defecto, borralo y relanza')
    for r in actual[1:]:
        if len(r) > 4 and r[4] not in m.MODELOS and r[4] not in m.ETAPAS:
            fail('catalogo: el modelo o etapa %r no existe; se ignora' % r[4])

# -----------------------------------------------------------------------------
# MODELOS: los SOP de cada modelo, dentro de 'modelos'
# -----------------------------------------------------------------------------
# Cada pieza es un Transform SOP sobre una caja o un prisma hexagonal unidad
# (centrados en el origen, de lado 1); el modelo es su Merge, y su salida el
# Null 'salida'. Las geometrias instanciadas lo traen con un Select SOP.

def unir(src, dst, k):
    try:
        src.outputConnectors[0].connect(dst)
        return True
    except Exception:
        return connect(dst, src, k)


def medir(sop):
    """(xmin, xmax, ymin, ymax, zmin, zmax) de los puntos de un SOP, o None
    si no se pueden leer."""
    try:
        pts = list(sop.points)
        if not pts:
            return None
        xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
        return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
    except Exception:
        return None


AJUSTADAS = []


def a_la_unidad(comp, sop, nombre):
    """Un Transform SOP que deja el SOP en el cubo unidad centrado, midiendo
    sus puntos: si algun parametro de la caja o del prisma no se fijo (radio,
    alto, centro), las piezas no se deforman."""
    aj = mk(comp, 'transformSOP', sop.name + '_unidad', 100, sop.nodeY)
    connect(aj, sop, 0)
    b = medir(sop)
    if b is not None:                # el hexagono no mide lo mismo en x y en z: escala comun
        kxz = 1.0 / max(1e-6, b[1] - b[0], b[5] - b[4])
        k = [kxz, 1.0 / max(1e-6, b[3] - b[2]), kxz]
        c = [(b[0] + b[1]) / 2.0, (b[2] + b[3]) / 2.0, (b[4] + b[5]) / 2.0]
        if max(abs(v - 1.0) for v in k) > 1e-3 or max(abs(v) for v in c) > 1e-3:
            AJUSTADAS.append('%s/%s' % (nombre, sop.name))
        setmenu(aj, ['xord'], ['srt'], 0)
        for q, ax in enumerate('xyz'):
            setp(aj, 's' + ax, k[q])
            setp(aj, 't' + ax, -c[q] * k[q])
    return aj


def construir_modelo(modelos, nombre, prims, x, y):
    comp = fresh(modelos, 'baseCOMP', nombre, x, y)
    fuentes = {}
    if any(p[0] == 'caja' for p in prims):
        caja = mk(comp, 'boxSOP', 'caja', 0, 0)
        for ax in ('sizex', 'sizey', 'sizez'):
            setp(caja, ax, 1.0)
        for ax in ('tx', 'ty', 'tz'):
            setp(caja, ax, 0.0)
        fuentes['caja'] = a_la_unidad(comp, caja, nombre)
    if any(p[0] == 'hexa' for p in prims):
        hexa = mk(comp, 'tubeSOP', 'hexa', 0, -120)
        bien = all([setp_any(hexa, ['rad1'], 0.5), setp_any(hexa, ['rad2'], 0.5),
                    setp(hexa, 'height', 1.0), setp_any(hexa, ['cols', 'columns'], 6)])
        setp_any(hexa, ['rows'], 2)
        setp_any(hexa, ['caps', 'endcaps', 'capends'], True)
        setmenu(hexa, ['orient', 'orientation'], ['y'], 1)
        for ax in ('tx', 'ty', 'tz'):
            setp(hexa, ax, 0.0)
        if not bien:
            info('%s: no pude fijar el prisma hexagonal (Tube SOP: radio 0,5, alto 1, 6 columnas, '
                 'eje Y, con tapas); ponlo a mano en modelos/%s/hexa' % (nombre, nombre))
        fuentes['hexa'] = a_la_unidad(comp, hexa, nombre)
    todo = mk(comp, 'mergeSOP', 'todo', 400, 0)
    for k, p in enumerate(prims):
        xf = mk(comp, 'transformSOP', 'p%d' % k, 200, -60 * k)
        connect(xf, fuentes[p[0]], 0)
        for ax, v in zip(('tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'rx', 'ry', 'rz'), p[1:10]):
            setp(xf, ax, float(v))
        setmenu(xf, ['xord'], ['srt'], 0)
        setmenu(xf, ['rord'], ['xyz'], 0)
        unir(xf, todo, k)
    out = mk(comp, 'nullSOP', 'salida', 600, 0)
    connect(out, todo, 0)
    for attr in ('render', 'display'):
        try:
            setattr(out, attr, True)
        except Exception:
            pass
    return comp


modelos = fresh(base, 'baseCOMP', 'modelos', 1100, 900)
nombres = sorted(m.MODELOS)
n_piezas = 0
for k, nm in enumerate(nombres):
    construir_modelo(modelos, nm, m.MODELOS[nm], (k % 8) * 220, -(k // 8) * 160)
    n_piezas += len(m.MODELOS[nm])
ok('modelos: %d modelos (%d piezas) generados en %s' % (len(nombres), n_piezas, modelos.path))
if AJUSTADAS:
    info('la caja o el prisma unidad no salian de lado 1 y centrados (%d, p. ej. %s): se han llevado '
         'a la unidad midiendo sus puntos' % (len(AJUSTADAS), AJUSTADAS[0]))

# -----------------------------------------------------------------------------
# GEOMETRIAS: una por modelo (pulida y porosa), y las particulas
# -----------------------------------------------------------------------------

for nm in [o.name for o in base.children if o.name.startswith(PIEL_PREFIJO)]:
    for viejo in (nm, 'i_' + nm):
        o = base.op(viejo)
        if o is not None:
            try:
                o.destroy()
            except Exception:
                pass
geos = m.geometrias_piel()
sin_color = []
for k, (g, mo, mat) in enumerate(geos):
    geo = make_instanced(base, g, 1400 + (k % 8) * 180, 600 - (k // 8) * 110, mat,
                         sop='select:%s/%s/salida' % (modelos.path, mo), quiet=True)
    if not instance_color_ok(geo)[0]:
        sin_color.append(g)
ok('%d geometrias de modelos (mod_...): pulidas con mat_pulido, porosas y obras con mat_poroso; '
   'giran con el planeta' % len(geos))
for g in sin_color[:3]:
    fail('%s no lee el color por instancia: Instance 2 -> Color R/G/B = r g b, Color Mode = Replace' % g)
make_constant(base, 'mat_particulas', 780, 860, (1.0, 1.0, 1.0))
make_instanced(base, 'particulas', 520, 860, 'mat_particulas')
set_render(base)

leeme(base, 11, """FASE 11 - LA PIEL
  Tema (pagina Fase11): naturaleza (vegetacion SEQ1, basalto SEQ2) o
  ciudad (informal SEQ1, planificada SEQ2). Modelos en 'modelos', tabla
  'catalogo' editable (tema especie estado variante modelo).
  Vecinas con presion >= Umbralvecindad se funden: puentes (dosel, meseta,
  pasarela, podio) y pieza protagonista en la capital.
  Compuestos por juego del caos (Caos, Maxpiezas): misma semilla, mismo
  compuesto. Obras por etapas: Avance gates (una por nota en el cluster)
  o pasos (cada Pasosetapa pasos).
  Prueba: Sembrarzona / Sembrarzona2 dos veces con cada tema.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    import math
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Avance', 'Velprueba', 'Nota', 'Nota2'):
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
    c = m.cfg()
    # 1. el catalogo, completo en los dos temas
    falta = []
    for tema in m.TEMAS:
        for own in (m.GEO, m.ARQ):
            esp = m.especie_de(tema, own)
            for estado in m.ESTADOS + ['puente', 'hibrido']:
                if not m.modelos_de(c, tema, esp, estado):
                    falta.append('%s %s %s' % (tema, esp, estado))
            if len(m.modelos_de(c, tema, esp, 'protagonista')) < 3:
                falta.append('%s %s protagonistas' % (tema, esp))
            cf, cc = m.cadenas_de(c, tema, esp)
            if not cf or not cc:
                falta.append('%s %s cadenas' % (tema, esp))
    for obra in ('valla', 'foso', 'andamio', 'grua'):
        if not m.modelos_de(c, 'ciudad', 'obra', obra):
            falta.append('ciudad obra %s' % obra)
    t.check('catalogo completo en los dos temas (estados, puentes, protagonistas, hibridos, cadenas)',
            not falta, ', '.join(falta[:4]))
    sin_nodos = [g for g, mo, _ in m.geometrias_piel()
                 if base.op(g) is None or base.op('modelos/%s/salida' % mo) is None]
    t.check('cada modelo tiene sus SOP en modelos y sus geometrias (pulida y porosa)',
            not sin_nodos, ', '.join(sin_nodos[:4]))
    grandes = []
    for mo, prims in m.MODELOS.items():
        b = m._caja_modelo(prims)
        planta = max(abs(b[0]), abs(b[1]), abs(b[4]), abs(b[5]))
        if b[2] < -1e-6 or b[3] > 1.0 + 1e-6 or (m.PIE[mo][0] == 'celda' and planta > 0.62):
            grandes.append(mo)
    t.check('los modelos caben en su volumen (base en 0, alto 1; los de planta de celda, en ella)',
            not grandes, ', '.join(grandes))
    # 2. Sembrarzona dos veces con cada tema: cluster, puentes y protagonista
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    base.par.Nota2 = nota
    base.par.Avance = 'gates'
    for tema in m.TEMAS:
        base.par.Tema = tema
        for pulso, s in (('Sembrarzona', m.GEO), ('Sembrarzona2', m.ARQ)):
            m.reset_world()
            m.on_pulse(pulso)
            m.on_pulse(pulso)
            W, c = m.world(), m.cfg()
            W['vh'] = list(W['h'])
            cl = m.clusters(W, c)
            k = cl['de'][i]
            esp = m.especie_de(tema, s)
            n_cl = len(cl['celdas'][k]) if k >= 0 else 0
            inst = m.build_instances(W, c, absTime.seconds + 10.0)
            pm = m.modelos_de(c, tema, esp, 'puente')[0]
            puentes = sum(len(inst.get(m.geometria_de(pm, p), [])) for p in (True, False))
            prot = m.modelos_de(c, tema, esp, 'protagonista')[m.clase_cluster(n_cl)]
            n_prot = sum(len(inst.get(m.geometria_de(prot, p), [])) for p in (True, False))
            enlaces = sum(len(x) for x in cl['mascara'])
            otro = [g for g, mo, _ in m.geometrias_piel() if inst.get(g)
                    and (mo[:3] in ('veg', 'rel')) != (tema == 'naturaleza')]
            t.check('%s, %s: Sembrarzona x2 -> cluster de %d celdas, %d puentes y protagonista'
                    % (tema, esp, n_cl, puentes),
                    n_cl == 1 + len(m.NEIGH[i]) and puentes == enlaces > 0 and n_prot == 1 and not otro,
                    'cluster %d, puentes %d de %d, protagonista %d, del otro tema %d'
                    % (n_cl, puentes, enlaces, n_prot, len(otro)))
        if tema == 'naturaleza':
            sim = all(a in cl['mascara'][b] for a in range(m.N) for b in cl['mascara'][a])
            t.check('puentes simetricos (si a va hacia b, b va hacia a)', sim)
    base.par.Tema = 'naturaleza'
    # 3. el mismo compuesto con la misma semilla
    def compuesto_de(vel):
        m.reset_world()
        base.par.Velprueba = vel
        for _ in range(9):
            m.on_pulse('Sembrar')
        W, c = m.world(), m.cfg()
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, c, absTime.seconds + 10.0)
        filas = sorted(tuple(round(x, 6) for x in f) for g, f_ in inst.items() if g.startswith('mod_')
                       for f in f_)
        return W['vel'][i], W['occ'][i], filas
    a, b, a2 = compuesto_de(100), compuesto_de(101), compuesto_de(100)
    t.check('Sembrar con Velprueba 100, 101 y 100: dos compuestos distintos, y 100 repite el mismo',
            a[2] == a2[2] and a[2] != b[2] and a[0] == 100 and b[0] == 101 and len(a[2]) >= 3,
            'ocupacion %d, %d piezas' % (a[1], len(a[2])))
    c = m.cfg()
    p = m.compuesto(c, m.GEO, 100, i, 6)
    q = m.compuesto(c, m.ARQ, 100, i, 6)
    t.check('SEQ1 en racimo oblicuo (multiplos de 30), SEQ2 en malla ortogonal (de 90, sin inclinar)',
            all(x['giro'] % 30 == 0 for x in p) and all(x['giro'] % 90 == 0 and x['incl'] == 0 for x in q))
    t.check('una ocupacion mayor solo anade piezas', m.compuesto(c, m.GEO, 100, i, 3) == p[:3])
    # 4. la obra avanza con cada gate y se invierte al bajar la ocupacion
    cg = dict(c)
    cg.update(tema=0, avance=0)
    Wg = m.new_world()
    now = 100.0
    zona = [i] + list(m.NEIGH[i])
    for _ in range(2):
        for x in zona[:4]:
            m.note_on(Wg, cg, m.GEO, m.cell_note(x), 100, now, 120.0)
    cl = m.clusters(Wg, cg)
    k = cl['de'][i]
    cf = m.cadenas_de(cg, 'naturaleza', 'vegetacion')[0]
    etapas = [Wg['et_f'][x] for x in cl['celdas'][k]] if k >= 0 else []
    for x in list(range(m.N)):
        Wg['et_f'][x] = min(Wg['et_f'][x], 1)
    antes = Wg['et_f'][i]
    m.note_on(Wg, cg, m.GEO, m.cell_note(i), 100, now + 0.1, 120.0)
    despues = [Wg['et_f'][x] for x in cl['celdas'][k]] if k >= 0 else []
    t.check('la obra avanza una etapa con cada gate en el cluster (todas sus celdas)',
            k >= 0 and antes == 1 and all(e == 2 for e in despues),
            'etapas %s -> %s' % (etapas, despues))
    for x in cl['celdas'][k] if k >= 0 else []:
        m.degrade(Wg, cg, x, 50)                   # la erosion deshace el cluster
    m.note_on(Wg, cg, m.GEO, m.cell_note(i), 100, now + 0.2, 120.0)
    tt = now + 0.2
    paso = m.step_dur(cg, 120.0)
    serie = [Wg['et_f'][i]]
    for f in range(int(4 * cg['pasos_etapa'] * paso * 60) + 2):
        tt += 1 / 60.0
        m.tick(Wg, cg, tt, 120.0, True)
        if Wg['et_f'][i] != serie[-1]:
            serie.append(Wg['et_f'][i])
    t.check('al bajar la ocupacion la obra se recorre hacia atras, una etapa cada Pasosetapa pasos',
            m.clusters(Wg, cg)['de'][i] < 0 and serie[-1] == 0 and serie == sorted(serie, reverse=True),
            'etapas %s' % serie)
    # 5. con Avance = pasos la obra avanza sola
    cp = dict(cg)
    cp['avance'] = 1
    Wp = m.new_world()
    for _ in range(2):
        for x in zona:
            m.note_on(Wp, cp, m.GEO, m.cell_note(x), 100, now, 120.0)
    e0 = Wp['et_f'][i]
    tt = now
    for f in range(int(len(cf) * cp['pasos_etapa'] * paso * 60) + 10):
        tt += 1 / 60.0
        m.tick(Wp, cp, tt, 120.0, True)
    t.check('Avance = pasos: una etapa cada Pasosetapa pasos, sin notas',
            e0 == 0 and Wp['et_f'][i] == len(cf), '%d -> %d de %d' % (e0, Wp['et_f'][i], len(cf)))
    # 6. el fin de ciclo cierra los transitos (con herencia completa, lo
    #    heredado sigue en cluster y su obra queda hecha, no a medias)
    ch = dict(cp)
    ch['herencia'] = 1.0
    Wc = m.new_world()
    for _ in range(2):
        for x in zona[:3]:
            m.note_on(Wc, ch, m.GEO, m.cell_note(x), 100, now, 120.0)
    tf, tc = m.objetivos(Wc, ch)
    a_medias = sum(1 for x in range(m.N) if Wc['et_f'][x] != tf[x])
    m.end_cycle(Wc, ch, now + 1.0, 16)
    tf, tc = m.objetivos(Wc, ch)
    t.check('el fin de ciclo cierra los transitos (ninguno queda a medias)',
            a_medias > 0 and any(tf) and all(Wc['et_f'][x] == tf[x] and Wc['et_c'][x] == tc[x]
                                              for x in range(m.N)),
            '%d a medias antes' % a_medias)
    # 7. nacimiento: rebote y destello en un paso como mucho
    Wn = m.new_world()
    m.note_on(Wn, cp, m.GEO, nota, 100, now, 120.0)
    Wn['paso'] = paso
    medio = m.rebote(cp, Wn, i, now + 0.3 * paso, paso)
    fin = m.rebote(cp, Wn, i, now + paso, paso)
    t.check('nacimiento: rebote y destello que acaban en un paso',
            medio[0] > 1.0 and medio[1] > 0 and fin == (1.0, 0.0), 'escala %.2f' % medio[0])
    # 8. coronacion y particulas (ciudad planificada): grua -> fachada -> aguja
    cz = dict(cp)
    cz.update(tema=1, avance=0)
    Wz = m.new_world()
    for _ in range(2):
        for x in zona:
            m.note_on(Wz, cz, m.ARQ, m.cell_note(x), 100, now, 120.0)
    for _ in range(60):
        m.note_on(Wz, cz, m.ARQ, nota, 100, now, 120.0)
    Wz['vh'] = list(Wz['h'])
    instz = m.build_instances(Wz, cz, now + 10.0)
    cuerpo = m.modelos_de(cz, 'ciudad', 'planificada', 'coronacion')[0]
    t.check('coronacion de la ciudad planificada: rascacielos con aguja',
            Wz['et_c'][i] == 3 and len(instz.get(m.geometria_de(cuerpo, True), [])) == 1
            and len(instz.get(m.geometria_de('pla_aguja', True), [])) == 1,
            'etapa %d' % Wz['et_c'][i])
    Wz2 = m.new_world()
    for _ in range(2):
        for x in zona[:3]:
            m.note_on(Wz2, cz, m.ARQ, m.cell_note(x), 100, now, 120.0)
    cl2 = m.clusters(Wz2, cz)
    for x in cl2['celdas'].get(cl2['de'][i], []):
        Wz2['et_f'][x] = 3                       # 'obreros'
    Wz2['vh'] = list(Wz2['h'])
    instp = m.build_instances(Wz2, cz, now + 10.0)
    t.check('obra de la ciudad: valla, foso y obreros (particulas del motor)',
            instp.get('mod_ciu_valla') and instp.get('mod_ciu_foso') and len(instp.get('particulas', [])) >= 8)
    # 9. nada pasa de la altura maxima (la camara de globo lo encuadra)
    tope = m.top_radius(Wz, cz) + m.altura_max(cz) + 1e-6
    lejos = 0.0
    for g, filas in instz.items():
        if not g.startswith('mod_'):
            continue
        for f in filas:
            M = m._rot_xyz(f[3], f[4], f[5])
            Y = (M[0][1], M[1][1], M[2][1])
            pt = (f[0] + Y[0] * f[7], f[1] + Y[1] * f[7], f[2] + Y[2] * f[7])
            lejos = max(lejos, math.sqrt(sum(v * v for v in pt)))
    t.check('ninguna pieza pasa de la altura maxima', 0 < lejos <= tope, '%.2f <= %.2f' % (lejos, tope))
    # 10. por el camino real: los Script CHOP de los modelos y la leyenda
    m.reset_world()
    base.par.Velprueba = 100
    m.on_pulse('Sembrarzona')
    m.on_pulse('Sembrarzona')
    m.world()['vh'] = list(m.world()['h'])
    m._CACHE['inst'] = m.build_instances(m.world(), m.cfg(), absTime.seconds + 10.0)
    llenas = [g for g, f in m._CACHE['inst'].items() if g.startswith('mod_') and f]
    chop = base.op('i_' + llenas[0]) if llenas else None
    if chop is not None:
        chop.cook(force=True)
    t.check('i_mod_...: el Script CHOP del modelo recibe sus instancias',
            chop is not None and chop.numSamples == len(m._CACHE['inst'][llenas[0]]),
            llenas[0] if llenas else 'ninguna')
    t.check('leyenda TEMA', 'TEMA' in m.legend() and 'clusters' in m.legend())
    t.check('la caja de la fase 3 ya no dibuja formaciones (solo huellas)',
            not m._CACHE['inst']['formas_pulidas'])


run_test(base, prueba)
print('  Ahora: Sembrarzona dos veces (pagina Fase11) y mira el cluster, sus')
print('  puentes y la pieza protagonista. Cambia Tema y repite.')
print('  Con el SEQ1 y el SEQ2 sonando: las obras avanzan con los gates')
print('  (Avance = gates); sin notas en el cluster se quedan a medias.')
print('=' * 66)
