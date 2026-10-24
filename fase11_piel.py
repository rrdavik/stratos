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

    ocupacion  1     matorral pionero            caseta / bloque
               2     arbol joven (2 derivac.)    anadidos / plantas
               3     arbol adulto (completo)
               Umbralram   arboleda (3 a 7)      pasarelas / manzana
               Umbralfusion bosque (timidez)     barrio / podio
               Umbralmonte monte boscoso         torre de antenas / rascacielos
    (los umbrales son los de la fase 4: Umbralram, Umbralfusion, Umbralcorona;
    el del monte, Umbralmonte)

BROTES, ARBOLES Y TERRAZAS (v8)
-------------------------------
  Ninguna planta es una primitiva (ni conos, ni bolas, ni prismas como copa):
  la vegetacion sale de una BIBLIOTECA DE EJEMPLARES precalculada (al cargar y
  al cambiar Variantes): 7 arboles (modelos arquitectonicos de Halle y
  Oldeman: conifera, pagoda, parasol, drago, frondosa, palmera y sauce) y 6
  matorrales (retama, brezo, helecho, graminea, enebro y palmito) x Variantes
  x derivaciones. Cada ejemplar: ramas (tubos de 4 o 5 lados, grosor por la
  regla de Leonardo) y puntos de hoja (posicion, normal, tamano, tipo,
  profundidad en la copa y nivel de rama); la copa es la suma de racimos de
  tamanos 0,6-1,4 y las hojas van por la ramilla con el angulo aureo. En TD,
  un Script SOP por ejemplar (modelos/veg_<modelo>_<v>_<d>) y su version
  lejana con tarjetas de racimo (_lod, Impostores).
  BIOMAS       la latitud elige la familia (frio, templado, calido) y la semilla
               del motor la planta; el piso montano fuerza la conifera y un rio
               cerca (fase 13), el sauce en lo templado.
  SUCESION     cada gate anade una derivacion: el arbol crece porque se ramifica.
  BOSQUE       ejemplares por disco de Poisson con timidez de copa (Timidez),
               emergentes (Emergentes), orla de matorral (Orla) y Mezcla.
  HIBRIDOS     mesetas construidas en el mapa de alturas: ARROZAL (vegetacion
               sobre relieve: un bancal por nota del SEQ1 por la curva de nivel,
               Riego en cascada con la fase 13) y MESETA-JARDIN (relieve sobre
               vegetacion: un nivel por nota del SEQ2, frutales en Marco, Setos).
  LIGERO       (por defecto, para una maquina modesta) la naturaleza se
               recalcula cada Refresconat s (a saltos: sus Script CHOP casi no
               se recuecen), 6 arboles por celda de bosque, tarjetas de racimo
               con la camara de globo, Variantes 2 y solo el arbol joven y el
               adulto en TD (80 geometrias).
  (Los arboles de pisos de la v6 y la v7 se sustituyen; sus parametros
  Pisoscopa, Anchocopa, Angulorama y Troncofrac se quitan.)

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
  DOSEL        clusters de 4+ celdas y bosques: desde la v8, ejemplares
               reales con timidez de copa (en la v5, bolas sobre una
               envolvente; en la v6, pisos que llegaban a las vecinas).
  PISOS        color por la altura sobre el suelo local (Ramp TOP
               'rampa_hipso'): basal, montano, limite del bosque
               (Limitebosque), roca y nieve (Limitenieve).
  COLOR        la naturaleza no toma el color de la concha ni el tinte del
               secuenciador: el tinte va al borde (fresnel, Tintebordenat) y a
               la loseta de la celda.
  LOD          de lejos (menos de Lodnat px por celda, o mas hojas que el
               presupuesto), tarjetas de racimo (Impostores); nunca esferas.

QUE ANADE
---------
  CATALOGO     tabla 'catalogo' (tema especie estado variante modelo) y las
               cadenas de transito. Los modelos se generan dentro de TD, en
               'modelos': la biblioteca de ejemplares para la vegetacion
               (v8; antes un L-system a 30 grados, bolas y conos),
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

VERSION = 'fase11 v8  (brotes, arboles y terrazas: biblioteca de ejemplares, biomas, arrozal y meseta-jardin)'
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
# v8: brotes, arboles y terrazas (los arboles de pisos de la v6 y la v7 se van)
quitados = [nm for nm in ('Pisoscopa', 'Anchocopa', 'Angulorama', 'Troncofrac') if remove_par(base, nm)]
add_par(base, page, 'toggle', 'Ligero', 'Naturaleza ligera (maquina modesta)', True)
add_par(base, page, 'float', 'Refresconat', 'La naturaleza se recalcula cada (s; 0 cada fotograma)', 0.25, 0.0, 2.0)
add_par(base, page, 'toggle', 'Biomas', 'Biomas por latitud (frio, templado, calido)', True)
add_par(base, page, 'int', 'Variantes', 'Variantes por modelo (biblioteca)', 2, 1, 8, clamp=True)
renew_default(base, 'Variantes', 4, 2)          # v8 ligera: 2 variantes (menos geometrias)
add_par(base, page, 'float', 'Varangulo', 'Variacion del angulo de rama (grados)', 12.0, 0.0, 45.0)
add_par(base, page, 'toggle', 'Cuantizar30', 'Angulos de rama a 30 grados (comparar)', False)
add_par(base, page, 'float', 'Inclinacion', 'Inclinacion hacia la luz (grados)', 8.0, 0.0, 30.0)
add_par(base, page, 'int', 'Densidadhoja', 'Hojas minimas por racimo', 6, 1, 30, clamp=True)
add_par(base, page, 'float', 'Traslucidez', 'Traslucidez del borde de la copa', 0.35, 0.0, 1.0)
add_par(base, page, 'float', 'Timidez', 'Timidez de copa (hueco entre copas)', 0.12, 0.0, 1.0)
add_par(base, page, 'float', 'Emergentes', 'Fraccion de emergentes del bosque', 0.1, 0.0, 1.0)
add_par(base, page, 'toggle', 'Orla', 'Orla de matorral en el borde del bosque', True)
add_par(base, page, 'float', 'Mezcla', 'Ejemplares del otro modelo del bioma', 0.3, 0.0, 1.0)
add_par(base, page, 'toggle', 'Impostores', 'De lejos, tarjetas de racimo', True)
add_par(base, page, 'float', 'Terrazaspornota', 'Bancales por nota del SEQ1 (arrozal)', 1.0, 0.0, 4.0)
add_par(base, page, 'int', 'Maxterrazas', 'Bancales maximos', 8, 1, 16, clamp=True)
add_par(base, page, 'float', 'Pasoterraza', 'Alto de un bancal (x el limite)', 0.12, 0.02, 0.5)
add_par(base, page, 'float', 'Muroterraza', 'Parte del bancal que es muro', 0.25, 0.05, 0.9)
add_par(base, page, 'toggle', 'Riego', 'Los bancales junto a un rio se inundan', True)
add_par(base, page, 'rgb', 'Colorcultivo', 'Verde arroz de los bancales', (0.66, 0.80, 0.22))
add_par(base, page, 'float', 'Alturameseta', 'Alto de un nivel de meseta (x el limite)', 0.15, 0.0, 1.0)
add_par(base, page, 'int', 'Maxniveles', 'Niveles maximos de la meseta', 3, 1, 6, clamp=True)
add_par(base, page, 'menu', 'Marco', 'Marco de los frutales', 'tresbolillo', menu=m.MARCOS,
        menu_labels=['Marco real', 'Tresbolillo'])
add_par(base, page, 'toggle', 'Setos', 'Setos entre las parcelas de la meseta', True)
ok('pagina Fase11: Tema (naturaleza), Pesovecina 0,5, Umbralvecindad 4, Mincluster 2, Caos 3,91, '
   'Maxpiezas 6, Avance (gates), Pasosetapa 2, Rebote 0,2, Sembrarzona, Sembrarzona2; v5: Umbralmonte 8, '
   'Maxcaosnat 5, Limitebosque 0,65, Limitenieve 0,9, Alturamonte 1, Lodnat 80, Tintebordenat 0,8; v8: '
   'Ligero, Refresconat 0,25, Biomas, Variantes 2, Varangulo 12, Cuantizar30 no, Inclinacion 8, Densidadhoja 6, Traslucidez 0,35, '
   'Timidez 0,12, Emergentes 0,1, Orla, Mezcla 0,3, Impostores, Terrazaspornota 1, Maxterrazas 8, '
   'Pasoterraza 0,12, Muroterraza 0,25, Riego, Colorcultivo, Alturameseta 0,15, Maxniveles 3, Marco '
   '(tresbolillo), Setos')
if quitados:
    info('v8: quitados los parametros de los arboles de pisos (%s)' % ', '.join(quitados))

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
ok('modelos: %d modelos (%d piezas y %d ejemplares de la biblioteca: %d plantas x %d variantes x '
   'derivaciones, cerca y lejos) generados en %s'
   % (n_modelos, n_piezas, len(m.ejemplares_de(m.cfg())), len(m.PLANTAS), m.variantes(m.cfg()), modelos.path))
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
  tinte del secuenciador al borde (Tintebordenat); Lodnat.
  v8, brotes, arboles y terrazas: la vegetacion sale de la biblioteca de
  ejemplares (modelos/veg_*: ramas y hojas, sin primitivas), con biomas por
  latitud (Biomas) y sucesion matorral -> arbol -> arboleda -> bosque ->
  monte; bosque con timidez de copa (Timidez, Emergentes, Orla, Mezcla); de
  lejos, tarjetas de racimo (Impostores). Hibridos: arrozal (Terrazaspornota,
  Maxterrazas, Pasoterraza, Muroterraza, Riego, Colorcultivo) y
  meseta-jardin (Alturameseta, Maxniveles, Marco, Setos); textura
  'cultivos' para el shader. Ligero (por defecto): la naturaleza se
  recalcula cada Refresconat s (a saltos), 6 arboles por celda de bosque y
  tarjetas de racimo con la camara de globo.""")

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
            geos = dict((mo, set()) for mo in list(m.MODELOS) + m.ejemplares_de(c) + m.PLANTAS + m.FORMAS)
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
            if esp == 'vegetacion':         # v8: ejemplares de la biblioteca, ninguna pieza suelta
                ejs = sum(len(f) for g, f in inst.items() if g.startswith('mod_veg_') and m.es_ejemplar(g[4:]))
                t.check('naturaleza, vegetacion: Sembrarzona x2 -> cluster de %d celdas con %d ejemplares de la '
                        'biblioteca, sin puentes ni protagonista' % (n_cl, ejs),
                        n_cl == 1 + len(m.NEIGH[i]) and ejs >= n_cl and puentes == 0
                        and n_prot == 0 and not otro, 'puentes %d, protagonista %d' % (puentes, n_prot))
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
    """Las pruebas de la naturaleza: la v5 (naturaleza legible) y la v8 (brotes,
    arboles y terrazas)."""
    import math
    import time
    base.par.Tema = 'naturaleza'
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    c = m.cfg()

    def mundo(celdas, own, occ, vel=100):
        W = m.new_world()
        for x in celdas:
            W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = occ, own, own, vel
            W['h'][x] = W['vh'][x] = m.height_for(m.cfg(), occ)
        return W

    def piezas(inst, pref):
        """[('mod_' + modelo, fila)] de los modelos que empiezan por pref."""
        mods = dict((g, mo) for g, mo, _ in m.geometrias_piel(m.cfg()))
        return [('mod_' + mods[g], f) for g, fs in inst.items() if g in mods and mods[g].startswith(pref)
                for f in fs]

    def celda_de(f):
        return max(range(m.N), key=lambda x: sum(f[q] * m.NORMALS[x][q] for q in range(3)))

    def plantas(inst, celda=None):
        """[(modelo, variante, derivacion, lejos, fila)] de los ejemplares (de una celda)."""
        out = []
        for g, f in piezas(inst, 'veg_'):
            if m.es_ejemplar(g[4:]) and (celda is None or celda_de(f) == celda):
                out.append(m.parte_ejemplar(g[4:]) + (f,))
        return out

    # 1. ninguna planta es una primitiva: la biblioteca de ejemplares
    prim = [mo for mo, prims in m.MODELOS.items() if mo.startswith('veg_') and mo != 'veg_claro']
    n_bib = m.biblioteca(c)
    leo = []
    for mo in m.PLANTAS:
        e = m.ejemplar(c, mo, 0, m.etapas_de(mo)[-1])
        for (r0, r1, hijos) in e['radios']:
            if hijos and abs(r0 * r0 - sum(h * h for h in hijos)) > 1e-9 + 1e-6 * r0 * r0:
                leo.append(mo)
                break
    tamanos = [tm for _, tm, _, _ in m.ejemplar(c, 'frondosa', 0, 3)['racimos']]
    cv = (max(tamanos) - min(tamanos)) / max(1e-9, sum(tamanos) / len(tamanos))
    t.check('biblioteca de ejemplares: %d (%d plantas x %d variantes x derivaciones), ramas por la regla de '
            'Leonardo, racimos desiguales (%.2f), sin modelos vegetales de piezas'
            % (n_bib, len(m.PLANTAS), m.variantes(c), cv),
            n_bib == sum(len(m.etapas_de(mo)) for mo in m.PLANTAS) * m.variantes(c) and not leo
            and not prim and cv > 0.6 and len(m.ARBOLES) == 7 and len(m.MATORRALES) == 6,
            'Leonardo falla en %s; piezas: %s' % (leo, prim))
    sube = m.ejemplar(c, 'conifera', 0, 3)['ramas']
    cuelga = m.ejemplar(c, 'sauce', 0, 3)['ramas']
    puntas_suben = sum(1 for a, b, r, nv in sube if nv == 1 and b[1] > a[1]) > 0.6 * sum(1 for x in sube if x[3] == 1)
    t.check('tropismo: las ramas de la conifera suben; el sauce cuelga cortinas',
            puntas_suben and sum(1 for a, b, r, nv in cuelga if b[1] < a[1] - 0.6 * m._len(m._add(b, a, -1.0)))
            >= 10)
    # 2. escalera: matorral, arbol joven, adulto, arboleda, bosque y monte
    serie, montes = [], []
    for o in range(1, 13):
        W = mundo([i], m.GEO, o)
        inst = m.build_instances(W, c, absTime.seconds + 10.0)
        serie.append((o, plantas(inst, i)))
        montes.append(m.terreno(W, c)['centro'][i])
    d = dict(serie)
    arb = lambda p: [x for x in p if x[0] in m.ARBOLES]
    mat = lambda p: [x for x in p if x[0] in m.MATORRALES]
    tb, tf = int(c['th_branch']), int(c['th_fusion'])
    u = int(c['umbral_monte'])
    escalera = (len(d[1]) == 1 and mat(d[1]) and not arb(d[1])
                and len(arb(d[2])) == 1 and arb(d[2])[0][2] == 2 and mat(d[2])
                and len(arb(d[3])) == 1 and arb(d[3])[0][2] == m.DERIVACIONES
                and 3 <= len(arb(d[tb])) <= 7 and mat(d[tb])
                and len(arb(d[tf])) >= 3)
    sube_m = all(montes[o - 1] == 0.0 for o in range(1, u)) and \
        all(montes[o] > montes[o - 1] for o in range(u, min(12, u + m.PASOS_MONTE - 1)))
    t.check('ocupacion 1 -> 12: matorral pionero, arbol joven (2 derivaciones, sotobosque), adulto (completo), '
            'arboleda (3 a 7), bosque y, desde Umbralmonte, el monte bajo el bosque',
            escalera and sube_m, ' / '.join('%d:%d+%d' % (o, len(arb(p)), len(mat(p))) for o, p in serie))
    # 3. prueba 1: de matorral a arbol en una celda calida, una templada y una fria
    def por_bioma(b):
        return [x for x in range(m.N) if m.bioma_de(x) == b and not m.is_pole(x)]
    pasos = []
    bien = True
    for b in m.BIOMAS:
        x = por_bioma(b)[len(por_bioma(b)) // 2]
        mats, arbs = m.BIOMA_PLANTAS[b]
        W1 = mundo([x], m.GEO, 1)
        W3 = mundo([x], m.GEO, 3)
        p1 = plantas(m.build_instances(W1, c, absTime.seconds + 10.0), x)
        p3 = plantas(m.build_instances(W3, c, absTime.seconds + 10.0), x)
        bien = bien and p1 and all(q[0] in mats for q in p1) and arb(p3) and all(q[0] in arbs for q in arb(p3))
        pasos.append('%s %s -> %s' % (b, p1[0][0] if p1 else '-', arb(p3)[0][0] if arb(p3) else '-'))
    t.check('matorral -> arbol por bioma: %s; ninguna esfera ni cono' % '; '.join(pasos), bien)
    # 4. prueba 2: la semilla (Velprueba 100 dos veces, el mismo ejemplar; 101, otro)
    def ejemplar_de(vel):
        W = mundo([i], m.GEO, 3, vel)
        return sorted(tuple(round(v, 6) for v in q[4]) + q[:3] for q in plantas(m.build_instances(
            W, c, absTime.seconds + 10.0), i))
    a, b, a2 = ejemplar_de(100), ejemplar_de(101), ejemplar_de(100)
    t.check('semilla: Velprueba 100 dos veces da el mismo ejemplar; 101, otro', a == a2 and a != b and a)
    # 5. prueba 3: lectura a distancia (siluetas a 18 px, como la fila inferior de la lamina)
    sil = dict((mo, m.silueta(c, m.nombre_ejemplar(mo, 0, m.etapas_de(mo)[-1]))) for mo in m.PLANTAS)
    pares = [(p, q, m.iou(sil[p], sil[q])) for k, p in enumerate(m.ARBOLES) for q in m.ARBOLES[k + 1:]]
    peor = max(pares, key=lambda x: x[2])
    tronco = []
    for mo in m.ARBOLES:
        filas = {}
        for x, y in sil[mo]:
            filas.setdefault(y, []).append(x)
        ancho = lambda y: (max(filas[y]) - min(filas[y]) + 1) if y in filas else 0
        if min(ancho(0), ancho(1)) > 0.35 * max(ancho(y) for y in filas):
            tronco.append(mo)
    mat_arb = max(m.iou(sil[p], sil[q]) for p in m.ARBOLES for q in m.MATORRALES)
    t.check('a 18 px los siete arboles se distinguen (el par mas parecido, %s y %s, %.2f), todos con el tronco '
            'visible, y ninguno se confunde con un matorral (%.2f)' % (peor[0], peor[1], peor[2], mat_arb),
            peor[2] < 0.75 and not tronco and mat_arb < 0.75, 'sin tronco: %s' % tronco)
    # 6. prueba 4: bosque de 5 celdas (troncos en el borde, huecos entre copas, emergentes)
    zona = [i] + list(m.NEIGH[i])[:4]
    Wb = mundo(zona, m.GEO, int(c['th_fusion']))
    instb = m.build_instances(Wb, c, absTime.seconds + 10.0)
    pb = plantas(instb)
    arboles = [q for q in pb if q[0] in m.ARBOLES]
    orla = [q for q in pb if q[0] in m.MATORRALES]
    emer = Wb['piel']['emergentes']
    timidos = True
    for x in zona:
        en = [q[4] for q in arboles if celda_de(q[4]) == x]
        for k, f in enumerate(en):
            for g in en[k + 1:]:
                dd = m._len(m._add(tuple(f[:3]), tuple(g[:3]), -1.0))
                if dd < 0.2 * min(f[7], g[7]):
                    timidos = False
    t.check('bosque de 5 celdas: %d ejemplares por disco de Poisson (timidez %.2f), %d emergentes, orla de %d '
            'matorrales; ninguna copa redonda' % (len(arboles), c['timidez'], emer, len(orla)),
            len(arboles) >= 3 * len(zona) and 1 <= emer <= max(2, 0.25 * len(arboles)) and orla and timidos)
    verdes = [f for _, _, _, _, f in arboles]
    cumbre = m.color_piso(c, 1.0)
    t.check('una montana grande (cumbre blanca) se distingue de un bosque (verde): %d ejemplares verdes'
            % len(verdes), verdes and all(f[10] > f[9] and f[10] > f[11] for f in verdes) and min(cumbre) > 0.9)
    # 7. prueba 5: arrozal (cordillera de 4 celdas, 5 notas del SEQ1 en la mas alta)
    fila = [m.note_cell(n) for n in (62, 63, 64, 65)]
    Wa = mundo(fila, m.ARQ, 9)
    Wa['occ'][fila[1]] = 12
    for x in fila:
        Wa['t_nac'][x] = 1.0
    for _ in range(5):
        m.note_on(Wa, c, m.GEO, m.cell_note(fila[1]), 100, 2.0, 120.0)
    Wa['vh'] = list(Wa['h'])
    m.build_instances(Wa, c, 3.0)
    tera = m.terreno(Wa, c)
    D = c['paso_terraza'] * m.limit(c)
    import numpy as np
    rej = m._rejilla(np)
    sel = rej['celda'] == fila[1]
    E = tera['E'][sel]
    top = 5 * D
    banda = E[E < top - 1e-6]
    escalones = sorted(set(int(round(v / D)) for v in banda if abs(v / D - round(v / D)) < 0.05))
    llano = np.mean(np.abs(banda / D - np.round(banda / D)) < 0.05) if len(banda) else 0.0
    t.check('arrozal: 5 notas del SEQ1 tallan %d bancales que siguen el relieve (%d%% de la banda en llano); por '
            'encima, roca y nieve (cumbre a %.2f del tope de los pisos)'
            % (m.bancales(Wa, c, fila[1]), int(100 * llano), float(E.max()) / tera['hmax']),
            m.bancales(Wa, c, fila[1]) == 5 and len(escalones) >= 4 and llano > 0.5 and E.max() > top,
            'escalones %s' % escalones)
    # 8. prueba 6: riego (un rio por la celda: los bancales de su lado, en cascada, uno por paso)
    cr = dict(c)
    cr['nivel'] = max(13, c['nivel'])
    q = m._norm(m._add(m.NORMALS[fila[1]], m.tangents(m.NORMALS[fila[1]])[0], 0.3))
    por = {fila[1]: [(q, 0.02)]}
    m._RIEGO.clear()
    paso = 0.125
    r0 = m.cultivos(Wa, cr, tera, por, 10.0, paso)['inundados'].get(fila[1], 0)
    cu = m.cultivos(Wa, cr, tera, por, 10.0 + 2.5 * paso, paso)
    r1 = cu['inundados'].get(fila[1], 0)
    A = cu['array']
    agua = sel & (A[..., 2] < A[..., 1] - 1e-6)
    lado = (rej['D'] - np.array(m.NORMALS[fila[1]])) @ np.array(m._add(q, m.NORMALS[fila[1]], -1.0))
    t.check('riego: con un rio en la celda los bancales se inundan en cascada (%d -> %d en 2,5 pasos), solo los '
            'de su lado' % (r0, r1), r0 == 1 and r1 == 3 and agua.any() and (lado[agua] > 0).all())
    m._RIEGO.clear()
    # 9. prueba 8: un golpe sobre el arrozal quita el bancal mas alto
    antes = m.bancales(Wa, c, fila[1])
    m.degrade(Wa, c, fila[1], 1)
    t.check('erosion: un golpe sobre el arrozal quita el bancal mas alto (%d -> %d)'
            % (antes, m.bancales(Wa, c, fila[1])), m.bancales(Wa, c, fila[1]) == antes - 1)
    # 10. prueba 7: meseta-jardin (bosque de 4 celdas y 2 notas del SEQ2)
    z4 = [i] + list(m.NEIGH[i])[:3]
    Wm = mundo(z4, m.GEO, int(c['th_fusion']))
    for x in z4:
        Wm['t_nac'][x] = 1.0
    for _ in range(2):
        m.note_on(Wm, c, m.ARQ, m.cell_note(i), 100, 2.0, 120.0)
    Wm['vh'] = list(Wm['h'])
    instm = m.build_instances(Wm, c, 3.0)
    term = m.terreno(Wm, c)
    alt = c['altura_meseta'] * m.limit(c)
    dentro = [q[4] for q in plantas(instm, i) if q[0] in m.ARBOLES]
    fuera = [q[4] for x in z4[1:] for q in plantas(instm, x) if q[0] in m.ARBOLES]
    alto = lambda f: f[7]
    rectos = all(m._dot(m._eje_y(f[3], f[4], f[5]), m.normal_i(i)) > 0.9999 for f in dentro)
    unif = dentro and max(alto(f) for f in dentro) <= 1.11 * min(alto(f) for f in dentro)
    desig = fuera and max(alto(f) for f in fuera) > 1.15 * min(alto(f) for f in fuera)
    t.check('meseta-jardin: 2 notas del SEQ2 suben %d niveles (%.2f del alto de un nivel en la capital), %d '
            'frutales rectos e iguales en marco, %d parcelas con setos; fuera, bosque silvestre'
            % (m.niveles_meseta(Wm, c, i), term['centro'][i] / max(1e-9, alt), len(dentro),
               Wm['piel']['parcelas'].get(i, 0)),
            m.niveles_meseta(Wm, c, i) == 2 and term['centro'][i] > 1.5 * alt and len(dentro) >= 3 and rectos
            and unif and desig and Wm['piel']['parcelas'].get(i, 0) >= 2,
            'rectos %s, iguales %s, desiguales fuera %s' % (rectos, unif, desig))
    # 11. una nota del SEQ1 sobre un bosque: el borde se ilumina, el verde se mantiene
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
            'se mantiene (albedo igual); traslucidez del borde de la copa (uHojas)',
            antes == despues and abs(sum(foco[q] * m.NORMALS[i][q] for q in range(3)) - 1.0) < 1e-6
            and min(uni['uTinteCol0'][:3]) > 0.5 and uni['uBorde'][0] > 0
            and abs(uni['uHojas'][0] - c['traslucidez']) < 1e-9)
    # 12. inclinacion hacia la luz y LOD
    Wi = mundo([i, m.NEIGH[i][0]], m.GEO, 3)
    insti = m.build_instances(Wi, c, absTime.seconds + 10.0)
    fi = [q[4] for q in plantas(insti, i) if q[0] in m.ARBOLES][0]
    ang = math.degrees(math.acos(max(-1.0, min(1.0, m._dot(m._eje_y(fi[3], fi[4], fi[5]), m.normal_i(i))))))
    lejos = [q for q in plantas(insti) if q[3]]
    t.check('el arbol se inclina hacia el lado sin vecinas (%.1f grados, <= Inclinacion %.0f); de lejos, '
            'tarjetas de racimo si Impostores (%d)' % (ang, c['inclinacion'], len(lejos)),
            0.5 < ang <= c['inclinacion'] + c.get('sway_max', 0.0) + 0.6
            and (bool(lejos) != bool(c.get('superficie') if c['ligero'] else m.lod_cerca(Wi, c, i))
                 or not c['impostores']))
    # 13. la erosion sobre un monte baja el terreno y el bosque baja con el
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
    # 14. prueba 9: rendimiento con las 85 celdas en bosque maximo, naturaleza frente a ciudad
    tiempos, hojas = {}, 0
    for tema, own in (('naturaleza', m.GEO), ('ciudad', m.GEO)):
        base.par.Tema = tema
        cc = m.cfg()
        W = mundo(range(m.N), own, 14)
        for x in range(0, m.N, 3):
            W['own'][x] = W['sp'][x] = m.ARQ
        m.build_instances(W, cc, absTime.seconds + 10.0)      # la biblioteca, el mapa y el presupuesto
        m.build_instances(W, cc, absTime.seconds + 10.0)
        ts = []
        for _ in range(5):                  # el minimo de 5: la medida con menos ruido de la maquina
            t0 = time.time()
            m.build_instances(W, cc, absTime.seconds + 10.0)
            ts.append(time.time() - t0)
        tiempos[tema] = min(ts)
        if tema == 'naturaleza':
            hojas = W['piel']['hojas']
    base.par.Tema = 'naturaleza'
    t.check('rendimiento: %d celdas en bosque maximo, naturaleza %.1f ms por fotograma, ciudad %.1f ms; hojas '
            '%d (presupuesto %d)' % (m.N, 1000 * tiempos['naturaleza'], 1000 * tiempos['ciudad'], hojas,
                                     m.HOJAS_TOPE),
            tiempos['naturaleza'] <= 1.1 * tiempos['ciudad'] + 0.002 and hojas <= m.HOJAS_TOPE)
    # 15. Refresconat: entre dos refrescos las filas de la vegetacion no cambian (los CHOP no se recuecen)
    cq = m.cfg()
    cq['refresco_nat'] = 0.25
    Wq = mundo([i] + list(m.NEIGH[i]), m.GEO, 7)
    t0 = absTime.seconds + 50.0
    f0 = m.build_instances(Wq, cq, t0, refresco=True)
    f1 = m.build_instances(Wq, cq, t0 + 0.1, refresco=True)
    veg = lambda inst: dict((g, v) for g, v in inst.items() if g.startswith('mod_veg_'))
    Wq['occ'][i] = 8
    f2 = m.build_instances(Wq, cq, t0 + 0.15, refresco=True)
    t.check('Refresconat %.2f s: entre dos refrescos la vegetacion copia sus filas; una ocupacion nueva '
            'refresca enseguida' % cq['refresco_nat'], veg(f0) == veg(f1) and veg(f0) and veg(f2) != veg(f1))
    m.reset_world()
    m.on_pulse('Sembrarzona')
    m.on_pulse('Sembrarzona')
    W = m.world()
    W['vh'] = list(W['h'])
    m.build_instances(W, m.cfg(), absTime.seconds + 10.0)
    ley = m.legend()
    t.check('leyenda NATURALEZA (biomas F/T/C, ejemplares, hojas) y NATURA (montes, cordilleras)',
            'NATURALEZA' in ley and 'biomas F/T/C' in ley and 'hojas' in ley and 'NATURA ' in ley)


run_test(base, prueba)
print('  Ahora: Sembrarzona dos veces (pagina Fase11) y mira el cluster, sus')
print('  puentes y la pieza protagonista. Cambia Tema y repite.')
print('  Con el SEQ1 y el SEQ2 sonando: las obras avanzan con los gates')
print('  (Avance = gates); sin notas en el cluster se quedan a medias.')
print('=' * 66)
