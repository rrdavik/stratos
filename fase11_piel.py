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

    ocupacion  1     brote                       caseta / bloque
               2+    arbol (frondosa o conifera) anadidos / plantas
               5+    arboleda (5 a 12 copas)     pasarelas / manzana
               7+    bosque (dosel continuo)     barrio / podio
               8+    monte boscoso (Umbralmonte) torre de antenas / rascacielos
    (los umbrales son los de la fase 4: Umbralram, Umbralfusion, Umbralcorona;
    el del monte, Umbralmonte)

NATURALEZA LEGIBLE (v5)
-----------------------
  A distancia de globo la naturaleza se lee por masa, silueta y bandas de
  color, no por detalle:
  ESCALERA     desde Umbralmonte la ocupacion ya no anade piezas: sube el
               terreno y el bosque lo cubre como una manta. Sin arbol madre.
               El juego del caos solo mueve y escala copas, y solo hasta
               Maxcaosnat.
  RELIEVE      una sola malla ('terreno'): la esfera que el shader desplaza
               con el mapa de alturas del motor. Celda suelta: cono con ruido
               de crestas; cluster de 3+: cordillera con la cresta por su eje.
               Las columnas de basalto, solo en las laderas bajas (estado 1-3).
  DOSEL        clusters de 4+ celdas y bosques: una copa por colonizacion del
               espacio; se ven las copas del borde (bolas abajo, conos arriba).
  PISOS        color por la altura sobre el suelo local (Ramp TOP
               'rampa_hipso'): basal, montano, limite del bosque
               (Limitebosque), roca y nieve (Limitenieve).
  COLOR        la naturaleza no toma el color de la concha ni el tinte del
               secuenciador: el tinte va al borde (fresnel, Tintebordenat) y a
               la loseta de la celda.
  LOD          de lejos, las copas del borde; cerca (Lodnat px por celda o la
               camara de superficie), tambien los troncos.

QUE ANADE
---------
  CATALOGO     tabla 'catalogo' (tema especie estado variante modelo) y las
               cadenas de transito. Los modelos se generan dentro de TD, en
               'modelos': un L-system con angulos de 30 grados para la
               vegetacion (desde la v5, bolas y conos de silueta clara),
               prismas hexagonales (Tube SOP de 6 lados) para el basalto y
               pilas de cajas (Box SOP) para la ciudad. Un Geometry
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

VERSION = 'fase11 v5  (naturaleza legible: monte boscoso, relieve en una malla, dosel por colonizacion, pisos de color, tinte al borde)'
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
add_par(base, page, 'int', 'Umbralmonte', 'Ocupacion desde la que sube el terreno (monte)', 8, 1, 30, clamp=True)
add_par(base, page, 'int', 'Maxcaosnat', 'Ocupacion maxima con juego del caos (naturaleza)', 5, 0, 16, clamp=True)
add_par(base, page, 'float', 'Limitebosque', 'Limite del bosque (altura relativa)', 0.65, 0.4, 0.85)
add_par(base, page, 'float', 'Limitenieve', 'Limite de la nieve (altura relativa)', 0.9, 0.5, 0.98)
add_par(base, page, 'float', 'Alturamonte', 'Crecimiento maximo del suelo (x el limite)', 1.0, 0.0, 3.0)
add_par(base, page, 'float', 'Lodnat', 'Detalle de la naturaleza desde (px por celda)', 80.0, 0.0, 400.0)
add_par(base, page, 'float', 'Tintebordenat', 'Tinte del secuenciador en el borde (fresnel)', 0.8, 0.0, 3.0)
ok('pagina Fase11: Tema (naturaleza), Pesovecina 0,5, Umbralvecindad 4, Mincluster 2, Caos 3,91, '
   'Maxpiezas 6, Avance (gates), Pasosetapa 2, Rebote 0,2, Sembrarzona, Sembrarzona2; v5: Umbralmonte 8, '
   'Maxcaosnat 5, Limitebosque 0,65, Limitenieve 0,9, Alturamonte 1, Lodnat 80, Tintebordenat 0,8')

# -----------------------------------------------------------------------------
# CATALOGO (tabla editable: tema especie estado variante modelo)
# -----------------------------------------------------------------------------

n_cat = catalogo_al_dia(base, m)
if n_cat is not None:
    ok('catalogo: %d filas (modelos de los dos temas y cadenas de transito)' % n_cat)
else:
    info('catalogo editado a mano: se conserva. Para volver al de por defecto, borralo y relanza')

# -----------------------------------------------------------------------------
# MODELOS: los SOP de cada modelo, dentro de 'modelos' (construir_modelos, en
# estratos_comun.py: la fase 14 anade los suyos)
# -----------------------------------------------------------------------------

modelos, n_modelos, n_piezas, ajustadas = construir_modelos(base, m)
ok('modelos: %d modelos (%d piezas) generados en %s' % (n_modelos, n_piezas, modelos.path))
if ajustadas:
    info('la caja o el prisma unidad no salian de lado 1 y centrados (%d, p. ej. %s): se han llevado '
         'a la unidad midiendo sus puntos' % (len(ajustadas), ajustadas[0]))

# -----------------------------------------------------------------------------
# GEOMETRIAS: una por modelo (pulida y porosa; desde la fase 12, una sola con
# el shader de la piel), y las particulas
# -----------------------------------------------------------------------------

instanciar_modelos(base, m)
terreno_al_dia(base, m)                 # v5: la malla del relieve (esfera desplazada por el mapa de alturas)
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
  Prueba: Sembrarzona / Sembrarzona2 dos veces con cada tema.
  v5, naturaleza legible: desde Umbralmonte sube el terreno (monte
  boscoso); el relieve es una sola malla ('terreno', mapa de alturas
  'alturas'); clusters de 4+ y bosques, un dosel por colonizacion del
  espacio; pisos de color (rampa_hipso: Limitebosque, Limitenieve); el
  tinte del secuenciador al borde (Tintebordenat); Lodnat.""")

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
    sin_nodos = [g for g, mo, _ in m.geometrias_piel(c)
                 if base.op(g) is None or base.op('modelos/%s/salida' % mo) is None]
    t.check('cada modelo tiene sus SOP en modelos y sus geometrias',
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
            geos = dict((mo, set()) for mo in m.MODELOS)
            for g, mo, _ in m.geometrias_piel(c):
                geos[mo].add(g)
            puentes = sum(len(inst.get(g, [])) for g in geos[pm])
            prot = m.modelos_de(c, tema, esp, 'protagonista')[m.clase_cluster(n_cl)]
            n_prot = sum(len(inst.get(g, [])) for g in geos[prot])
            enlaces = sum(len(x) for x in cl['mascara'])
            if esp == 'vegetacion':          # motor v32: el dosel cierra cada hueco entre tres celdas
                mk_ = cl['mascara']
                enlaces += sum(1 for a in range(m.N) for b in mk_[a] if b > a
                               for c_ in mk_[a] if c_ > b and c_ in mk_[b])
            otro = [g for g, mo, _ in m.geometrias_piel(c) if inst.get(g)
                    and (mo[:3] in ('veg', 'rel')) != (tema == 'naturaleza')]
            if esp == 'vegetacion':         # v5: un dosel por colonizacion del espacio, sin puentes
                copas = sum(len(inst.get(g, [])) for g in geos['veg_copa'] | geos['veg_cono'])
                t.check('naturaleza, vegetacion: Sembrarzona x2 -> cluster de %d celdas con un dosel de %d copas '
                        '(colonizacion del espacio), sin puentes ni protagonista' % (n_cl, copas),
                        n_cl == 1 + len(m.NEIGH[i]) and copas >= 2 * n_cl and puentes == 0 and n_prot == 0
                        and not otro, 'copas %d, puentes %d, protagonista %d' % (copas, puentes, n_prot))
            elif esp == 'relieve':          # v5: una cordillera en el mapa de alturas, sin piezas de puente
                ter = m.terreno(W, c)
                altos = sum(1 for x in cl['celdas'][k] if ter['centro'][x] > 0.1 * m.limit(c)) if k >= 0 else 0
                t.check('naturaleza, relieve: Sembrarzona x2 -> cluster de %d celdas que es una cordillera '
                        '(%d celdas levantadas en el mapa), sin puentes ni protagonista' % (n_cl, altos),
                        n_cl == 1 + len(m.NEIGH[i]) and ter['cordilleras'] == 1 and altos == n_cl
                        and puentes == 0 and n_prot == 0 and not otro,
                        'cordilleras %d, puentes %d, protagonista %d' % (ter['cordilleras'], puentes, n_prot))
            else:
                t.check('%s, %s: Sembrarzona x2 -> cluster de %d celdas, %d puentes y protagonista'
                        % (tema, esp, n_cl, puentes),
                        n_cl == 1 + len(m.NEIGH[i]) and puentes == enlaces > 0 and n_prot == 1 and not otro,
                        'cluster %d, puentes %d de %d, protagonista %d, del otro tema %d'
                        % (n_cl, puentes, enlaces, n_prot, len(otro)))
        if tema == 'naturaleza':
            sim = all(a in cl['mascara'][b] for a in range(m.N) for b in cl['mascara'][a])
            t.check('puentes simetricos (si a va hacia b, b va hacia a)', sim)
    base.par.Tema = 'ciudad'                # v5: en la naturaleza el caos solo mueve copas
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
    base.par.Tema = 'naturaleza'
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
            Wz['et_c'][i] == 3 and len(instz.get(m.geometria_de(cuerpo, True, cz['nivel'] < 12), [])) == 1
            and len(instz.get(m.geometria_de('pla_aguja', True, cz['nivel'] < 12), [])) == 1,
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
    _prueba_natural(t, m)


def _prueba_natural(t, m):
    """v5: las pruebas del encargo 'naturaleza legible'."""
    import math
    import time
    base.par.Tema = 'naturaleza'
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    lim = m.limit(m.cfg())

    def mundo(celdas, own, occ, vel=100):
        W = m.new_world()
        for x in celdas:
            W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = occ, own, own, vel
            W['h'][x] = W['vh'][x] = m.height_for(m.cfg(), occ)
        return W

    def piezas(inst, pref):
        """[('mod_' + modelo, fila)] de los modelos que empiezan por pref (en la fase 11
        la geometria lleva _pul o _por: se nombra por su modelo)."""
        mods = dict((g, mo) for g, mo, _ in m.geometrias_piel(m.cfg()))
        return [('mod_' + mods[g], f) for g, fs in inst.items() if g in mods and mods[g].startswith(pref)
                for f in fs]

    def celda_de(f):
        return max(range(m.N), key=lambda x: sum(f[q] * m.NORMALS[x][q] for q in range(3)))
    # 1. ocupacion 1 -> 12 en una celda de vegetacion: brote, arbol, arboleda, bosque, monte
    c = m.cfg()
    serie, montes = [], []
    for o in range(1, 13):
        W = mundo([i], m.GEO, o)
        inst = m.build_instances(W, c, absTime.seconds + 10.0)
        ps = [g[4:] for g, f in piezas(inst, 'veg_') if celda_de(f) == i]
        montes.append(m.terreno(W, c)['centro'][i])
        serie.append((o, ps))
    def es(o, cond):
        return cond(dict(serie)[o])
    u = int(c['umbral_monte'])
    escalera = (es(1, lambda p: len(p) == 1 and p[0].startswith('veg_brote'))
                and es(3, lambda p: p and p[0] in ('veg_arbol', 'veg_conifera'))
                and es(int(c['th_branch']), lambda p: 5 <= len(p) <= 12 and set(p) <= {'veg_arbol', 'veg_conifera'})
                and es(int(c['th_fusion']), lambda p: len(p) >= 5 and set(p) <= {'veg_copa', 'veg_cono', 'veg_tronco'})
                and all(not set(dict(serie)[o]) - {'veg_copa', 'veg_cono', 'veg_tronco'} for o in range(u, 13)))
    sube = all(montes[o - 1] == 0.0 for o in range(1, u)) and \
        all(montes[o] > montes[o - 1] for o in range(u, min(12, u + m.PASOS_MONTE - 1)))
    t.check('ocupacion 1 -> 12 en una celda: brote, arbol, arboleda, bosque y, desde Umbralmonte, un monte '
            'que sube con el bosque encima (sin arbol madre ni amasijo)',
            escalera and sube and 'veg_madre' not in m.MODELOS,
            ' / '.join('%d:%s' % (o, len(p)) for o, p in serie) + '   monte %.2f' % montes[-1])
    # 2. cluster de 5 celdas de relieve en fila: una cordillera continua con cumbres nevadas
    fila = [m.note_cell(n) for n in (62, 63, 64, 65, 66)]
    W = mundo(fila, m.ARQ, 9)
    W['occ'][fila[2]] = 12
    cl = m.clusters(W, c)
    ter = m.terreno(W, c, cl)
    cresta = min(m.alto_en(ter, m._norm(m._add(m.NORMALS[a], m.NORMALS[b]))) for a, b in zip(fila, fila[1:]))
    _, ln = m._limites_pisos(c)
    nevadas = [x for x in fila if ter['centro'][x] >= ln * ter['hmax']]
    inst = m.build_instances(W, c, absTime.seconds + 10.0)
    t.check('cluster de 5 celdas de relieve en fila: una cordillera continua (cresta %.2f) con cumbres nevadas '
            '(%d) y sin piezas sueltas por celda' % (cresta, len(nevadas)),
            ter['cordilleras'] == 1 and cresta > 0.4 * min(ter['centro'][x] for x in fila) and nevadas
            and not piezas(inst, 'rel_puente') and not piezas(inst, 'rel_cumbre'),
            'eje %s' % (ter['ejes'][0] if ter['ejes'] else '-'))
    # 3. bosque sobre la cordillera (hibrido): hasta Limitebosque; por encima, roca y nieve
    for x in fila:
        W['sp'][x] = m.HIB
    inst = m.build_instances(W, c, absTime.seconds + 10.0)
    arboles = piezas(inst, 'veg_')
    altos = [m.alto_en(ter, m._norm(tuple(f[:3]))) / ter['hmax'] for _, f in arboles]
    t.check('bosque sobre cordillera: %d arboles, todos por debajo de Limitebosque (%.2f); arriba solo roca y nieve'
            % (len(arboles), c['limite_bosque']),
            arboles and max(altos) <= c['limite_bosque'] + 1e-6 and m.color_piso(c, 0.95)[0] > 0.85
            and m.color_piso(c, 0.8)[1] < 0.5, 'el mas alto a %.2f' % max(altos or [0]))
    # 4. de lejos (formacion de ~13 px), una montana grande se distingue de un bosque
    Wb = mundo([i] + list(m.NEIGH[i]), m.GEO, 7)
    instb = m.build_instances(Wb, c, absTime.seconds + 10.0)
    verdes = [f for _, f in piezas(instb, 'veg_co')]
    cumbre = m.color_piso(c, 1.0)
    t.check('una montana grande (cumbre blanca) se distingue de un bosque (verde granulado): %d copas verdes'
            % len(verdes), verdes and all(f[10] > f[9] and f[10] > f[11] for f in verdes)
            and min(cumbre) > 0.9 and len(set(round(f[10], 3) for f in verdes)) > 3)
    # 5. una nota del SEQ1 sobre un bosque: el borde se ilumina, el verde se mantiene
    m.reset_world()
    W, c = m.world(), m.cfg()
    for x in [i] + list(m.NEIGH[i]):
        W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = 7, m.GEO, m.GEO, 100
        W['h'][x] = W['vh'][x] = m.height_for(c, 7)
    ahora = absTime.seconds + 10.0
    antes = [f[9:12] for _, f in piezas(m.build_instances(W, c, ahora), 'veg_')]
    m.note_on(W, c, m.GEO, nota, 100, ahora, 120.0)
    W['occ'][i] = 7
    despues = [f[9:12] for _, f in piezas(m.build_instances(W, c, ahora), 'veg_')]
    uni = m.uniformes_piel(W, c, ahora)
    foco = uni['uTinte0']
    t.check('una nota del SEQ1 sobre un bosque: el borde se ilumina con el color del SEQ1 (uTinte) y el verde '
            'se mantiene (albedo igual)',
            antes == despues and abs(sum(foco[q] * m.NORMALS[i][q] for q in range(3)) - 1.0) < 1e-6
            and min(uni['uTinteCol0'][:3]) > 0.5 and uni['uBorde'][0] > 0)
    # 6. la erosion sobre un monte baja el terreno y el bosque se reajusta
    W = mundo([i], m.GEO, 12)
    inst0 = m.build_instances(W, c, absTime.seconds + 10.0)
    h0 = m.terreno(W, c)['centro'][i]
    r0 = max(math.sqrt(sum(v * v for v in f[:3])) for _, f in piezas(inst0, 'veg_'))
    m.degrade(W, c, i, 3)
    W['vh'] = list(W['h'])
    inst1 = m.build_instances(W, c, absTime.seconds + 10.0)
    h1 = m.terreno(W, c)['centro'][i]
    r1 = max(math.sqrt(sum(v * v for v in f[:3])) for _, f in piezas(inst1, 'veg_'))
    t.check('la erosion sobre un monte baja el terreno (%.2f -> %.2f) y el bosque baja con el' % (h0, h1),
            W['occ'][i] < 12 and h1 < h0 and r1 < r0)
    # 7. rendimiento: 85 celdas a maxima ocupacion, naturaleza frente a ciudad
    tiempos = {}
    for tema, own in (('naturaleza', m.GEO), ('ciudad', m.GEO)):
        base.par.Tema = tema
        cc = m.cfg()
        W = mundo(range(m.N), own, 14)
        for x in range(0, m.N, 3):
            W['own'][x] = W['sp'][x] = m.ARQ
        m.build_instances(W, cc, absTime.seconds + 10.0)      # el dosel y el mapa, una vez
        t0 = time.time()
        for _ in range(5):
            m.build_instances(W, cc, absTime.seconds + 10.0)
        tiempos[tema] = (time.time() - t0) / 5.0
    base.par.Tema = 'naturaleza'
    t.check('rendimiento: %d celdas a maxima ocupacion, naturaleza %.1f ms por fotograma, ciudad %.1f ms '
            '(el dosel y el mapa de alturas se calculan una vez)' % (m.N, 1000 * tiempos['naturaleza'],
                                                                      1000 * tiempos['ciudad']),
            tiempos['naturaleza'] <= 1.1 * tiempos['ciudad'] + 0.002)
    m.reset_world()
    m.on_pulse('Sembrarzona')
    m.on_pulse('Sembrarzona')
    W = m.world()
    W['vh'] = list(W['h'])
    m.build_instances(W, m.cfg(), absTime.seconds + 10.0)
    t.check('leyenda NATURA (copas, montes, cordilleras, cumbres nevadas, detalle)',
            'NATURA' in m.legend() and 'copas' in m.legend())


run_test(base, prueba)
print('  Ahora: Sembrarzona dos veces (pagina Fase11) y mira el cluster, sus')
print('  puentes y la pieza protagonista. Cambia Tema y repite.')
print('  Con el SEQ1 y el SEQ2 sonando: las obras avanzan con los gates')
print('  (Avance = gates); sin notas en el cluster se quedan a medias.')
print('=' * 66)
