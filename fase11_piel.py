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

    ocupacion  1     matorral pionero            caseta / pabellon
               2     arbol joven (2 derivac.)    casa que crece / bloque
               3     arbol adulto (completo)     tres plantas / bloque
               Umbralram-1 arboleda (3 a 7)      racimo / manzana
               fusion-1    bosque (timidez)      barrio denso / podio
               Umbralmonte monte boscoso
               corona-1                          torre autoconstruida / rascacielos
    (los umbrales son los de la fase 4: Umbralram y, a Pasoumbral, la fusion
    y la corona; el del monte, Umbralmonte)

TEMA INDUSTRIA (v11)
--------------------
  Un tercer Tema. La mina (SEQ1) cava, en racimo oblicuo; la energia (SEQ2)
  transforma, en malla ortogonal. Mismo motor que la ciudad (biblioteca por
  gramatica, obra, mutantes), con piezas de ingenieria: cilindros, celosias,
  hiperboloides y troncos de cono, cada una con su rasgo de lectura.
    mina      brote (bocamina, balancin, cantera), mina con maquinaria
              (castillete, balancines, trituradora), complejo minero
              (lavadero), fundicion (altos hornos con colada), refineria
              (columnas y antorcha)
    energia   aserradero (cobertizo, secadero), serreria (portico), fabrica
              (naves de sierra y chimenea), central termica (la primera torre)
              y central electrica (2-4 torres con penacho, de ella nace la red)
  RECURSO   con Recursos, la mina lee la concha de abajo (registro de la fase
            15): carbon (naturaleza), chatarra (ciudad), escoria (industria) o
            mineral (primera era); terriles y vagonetas de su color.
  EPOCA     por las eras enterradas (vapor 0-2, acero 3-5, quimica 6+) o fija
            (Epoca), en directo: cada planta conserva la suya.
  MUTANTES  CORTA (mina sobre energia: Bancospornota, Maxbancos; se come las
            naves, luego las calderas; queda la chimenea; agua acida y
            rotopala desde 4 bancos; no corta conchas) e INTEGRADA (energia
            sobre mina: Maxbastidor niveles que los castilletes atraviesan).
  CLUSTER   cuenca minera (terriles fundidos y cable aereo); torres que se
            alinean: compartida (2-3), fila (4-6), anillo (7+).
  OBRA      terminada = humea: encofrado deslizante en chimeneas y torres,
            columna tumbada que iza la grua, poleas al final.
  HUMO      particulas del motor (negro, gris o vapor blanco; Emisiones,
            Maxhumo); la nota tine la bocanada de su chimenea. Partes moviles
            (balancin, poleas, rotopala) al tempo.

CIUDAD LEGIBLE: EDIFICIOS POR ETAPA Y CONSTRUCCIONES MUTANTES (v10)
--------------------------------------------------------------------
  Lo mismo que la v8 hizo con la naturaleza. Ninguna etapa es una caja
  desnuda: cada una es un TIPO de edificio, con variantes, con pie, cuerpo
  con ritmo y remate. Sale de una BIBLIOTECA DE EDIFICIOS precalculada (al
  cargar y al cambiar Variantesciudad, Oblicuidad, Retranqueo o Torsionmax)
  por una gramatica de particion (solar -> masa -> plantas -> fachada):
  volumenes (prismas de planta rectangular u octogonal; las L, H, peines y
  patios son varios), datos de fachada por volumen (en el uv de la malla) y
  puntos de remate (deposito, antena, maquinaria, varillas, escalera,
  cable...: instancias ciu_). La fachada NO es geometria: la dibuja el GLSL
  MAT de la ciudad, que cuenta plantas y vanos a la escala del mundo. En TD,
  un Script SOP por ejemplar (modelos/edi_<diseno>_<v>).
    informal     caseta (chabola, contenedor, cubo de cal), casa que crece
                 (laje con varillas), tres plantas (bandas de colores, la de
                 arriba en voladizo), racimo, barrio denso (Kowloon) y torre
                 autoconstruida (cuartos dentados, mastil y valla)
    planificada  pabellon (dientes de sierra, pilotis), bloque (lamina con
                 loggias, torre-punto, H), manzana (Cerda con chaflan y patio,
                 peine), podio y rascacielos (deco con aguja, haz de tubos,
                 torsionada, prisma con corona)
  CRECEN       la informal por agregacion (un cuarto por gate, desplazado e
               inclinado hasta Oblicuidad); la planificada por repeticion (las
               plantas del mismo modulo, una o Plantasligado por gate).
  LENGUAJE     por la latitud (Lenguaje = latitud): frio (hormigon y chapa),
               templado (ladrillo y vidrio), calido (cal y celosia); o fijo, o
               mezcla, en directo: cada edificio conserva el suyo.
  OBRA         solar, excavacion, nucleo con grua, esqueleto, fachada
               (Desfasefachada plantas por detras), coronacion y terminada; la
               informal, en bloque gris con varillas hasta el gate siguiente.
  MUTANTES     COLONIA (informal sobre planificada: parasitos de la azotea
               hacia abajo) y MARCO (planificada sobre informal: la Ville
               Spatiale, con pilares en los callejones y capsulas). Mutacion
               (o la saturacion del modular, Mutacionfuente) dice hasta donde.
  CLUSTER      el racimo se funde en barrio; las torres se buscan: pasarela
               celeste (2-3 celdas), bucle (4-6), losa en la cumbre (7+).
  COLOR        el de la ciudad es suyo; una nota enciende las ventanas del
               edificio con el color de su secuenciador (Tinteventanas,
               Pasostinte). De lejos (Lodciudad), sin los remates pequenos.

TIERRA EN VEZ DE LOSETAS (v17, motor v100)
------------------------------------------
  SEDIMENTO  con Oceano, la concha que entierra un mundo solo deja su capa donde
             se creo algo o llego un desborde en ese mundo (y donde las personas
             dejaron huella o abrieron una escision). El mar no se entierra: la
             tierra sube era a era sobre el, y sus flancos ensenan las capas.
  MAR        el nivel del mar es el del suelo mas bajo. Una celda con sedimento y
             sin nada encima es tierra desnuda (parda, agrietada, con piedras),
             no agua; alrededor de las islas que estan sobre sedimento no hay playa.
  CONCHAS    (Tierra 0,75) las losetas se pintan como capas de tierra: el color
             de su generacion queda en un matiz sobre pardos, con laminas finas
             de sedimento, grano y cantos. Tierra 0: las losetas de color de antes.
             La cicatriz (cian) se sigue viendo.
  LUZ        la celda que suena sigue encendiendose: ademas de la loseta de luz,
             su suelo entero se tine con el color de la senal (antes, solo el borde).
  Las autopruebas de todas las fases corren sin Oceano (apilan conchas en mundos
  vacios); la del oceano y la sedimentacion la hace esta fase.

EL DOBLE DE GRANDE, CON LA TARJETA GRAFICA (v16, motor v99)
-----------------------------------------------------------
  ESCALA     el nucleo pasa de radio 6 a 12. Las formaciones (arboles, montes,
             conchas) miden lo mismo: las celdas son el doble de anchas (cuatro
             veces la superficie) y cada isla tiene sitio para un bosque, playas
             y lagunas. La camara se encuadra sola y las dos luces fijas se
             alejan al doble (una vez). Hasta 24 arboles por celda de bosque.
  PRADERA    (Pradera 300000, Mata 0,16) una sola mata de hierba que la tarjeta
             grafica instancia Pradera veces y coloca ella misma: el vertex
             shader saca de cada numero de instancia un sitio de la esfera, lee
             el mapa de alturas y la planta solo en tierra firme (ni playa, ni
             roca, ni lava), mas espesa en unas manchas que en otras, con su
             tamano, su color y su vaiven. El motor no calcula ninguna: no
             cuesta CPU. Pradera 0 (o Detalle apagado) la quita.
  MAPA       el mapa de alturas se guarda por capas (relieve, montes, islas) y
             a cada nota solo se rehace lo que cambia: con el oceano costaba
             mas de 100 ms por nota (con el mundo lleno); ahora, unos 15.

OCEANO, ISLAS, VOLCANES Y DETALLE (v14, motor v97)
--------------------------------------------------
  OCEANO     (Oceano, encendido) en la naturaleza las celdas vacias son mar: la
             malla del terreno flota sobre las losetas y el shader la pinta de
             agua (honda lejos de la costa, turquesa y espuma junto a ella, con
             olas). Cada celda ocupada es una ISLA con playa: crece y sube con
             la ocupacion hasta salirse de su celda; dos vecinas con 2 o mas se
             unen por un istmo (islas grandes) y desde 3 sueltan islotes
             (archipielagos). El relieve y los montes van encima. En el agua no
             crece nada, salvo el mangle y el junco; los rios acaban en el mar.
             Apagado, todo vuelve a ser como en la v13.
  VOLCANES   (Volcanes 0,2) un cono de relieve suelto, o la capital de una
             cordillera, desde Umbralram, es un volcan con esa probabilidad
             (lo decide su semilla): crater, coladas de lava que brillan,
             penacho de humo y, cada 12 a 28 compases, una erupcion de 2:
             brasas, ceniza y la lava al rojo. Con 0, ninguno.
  PLANTAS    ocho arboles mas (cipres, abedul, araucaria, olivo, baobab, mangle,
             bambu y cardon) y dos matorrales (agave y junco): 23 plantas.
             Frio: conifera, abedul, araucaria. Templado: frondosa, pagoda,
             cipres, olivo (y el sauce junto al rio). Calido: parasol, drago,
             palmera, baobab, bambu, cardon; en la costa, palmera y mangle.
             Cada planta tiene su verde, su corteza (el abedul, blanca; el
             bambu y el cardon, verdes) y algunas, flores o fruto.
  DETALLE    (Detalle, encendido) lo lleva la tarjeta grafica: hojas de verdad
             tambien desde el globo (antes, tarjetas de racimo), presupuesto de
             3 millones de hojas, hasta 10 arboles por celda de bosque, frondas
             pinnadas, troncos de 8 lados, malla del terreno de 512 x 1024 con
             relieve fino en el shader y antialiasing 16x. Resolucion: el
             tamano del render (720p; mas, con licencia comercial o pro).
             Si la maquina no puede, apagar Detalle.

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

PAGINA MAS CORTA (v9)
---------------------
  35 parametros en vez de 42. Siete ajustes finos de la geometria quedan
  fijos en su valor por defecto:
    Rebote 0,2        rebote del nacimiento
    Maxcaosnat 5      ocupacion maxima con juego del caos (naturaleza)
    Varangulo 12      variacion del angulo de rama (grados)
    Cuantizar30 no    angulos de rama a 30 grados (era para comparar)
    Inclinacion 8     inclinacion hacia la luz (grados)
    Densidadhoja 6    hojas minimas por racimo
    Muroterraza 0,25  parte del bancal que es muro
  Se quedan los que cambian las escenas (fase 18), los de rendimiento
  (Ligero, Refresconat, Impostores, Lodnat) y los que dan caracter al
  bosque, los pisos y los hibridos. Relanzar cualquier fase los quita de
  un proyecto anterior y avisa si los habias cambiado.

NATURALEZA LEGIBLE (v5)
-----------------------
  A distancia de globo la naturaleza se lee por masa, silueta y bandas de
  color, no por detalle:
  ESCALERA     desde Umbralmonte la ocupacion ya no anade piezas: sube el
               terreno y el bosque lo cubre como una manta. Sin arbol madre.
               El juego del caos solo mueve y escala copas, y solo hasta
               la ocupacion 5.
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
               la biblioteca de edificios para la ciudad (v10; antes, pilas
               de cajas), con sus remates de cajas (Box SOP). Un Geometry
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
               mucho; rebote 0,2); crecimiento en un paso. Fusion y coronacion son
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

VERSION = 'fase11 v17  (tierra en vez de losetas: el mar no sedimenta, conchas como capas de tierra)'
banner(VERSION)

base = require_base(11)
motor = install_core(base, CARPETA, 11)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase11)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase11')
add_par(base, page, 'menu', 'Tema', 'Tema', 'naturaleza', menu=m.TEMAS,
        menu_labels=['Naturaleza', 'Ciudad', 'Industria'])
if menu_al_dia(base, 'Tema', m.TEMAS, ['Naturaleza', 'Ciudad', 'Industria']):
    info('v11: Tema gana la industria (naturaleza / ciudad / industria)')
add_par(base, page, 'float', 'Pesovecina', 'Peso de las vecinas en la presion', 0.5, 0.0, 2.0)
add_par(base, page, 'float', 'Umbralvecindad', 'Presion para fundirse (cluster)', 4.0, 1.0, 20.0)
add_par(base, page, 'int', 'Mincluster', 'Celdas minimas de un cluster', 2, 2, 20, clamp=True)
add_par(base, page, 'float', 'Caos', 'Mapa logistico: r (compuestos)', 3.91, 3.5, 4.0)
add_par(base, page, 'int', 'Maxpiezas', 'Piezas maximas por compuesto', 6, 1, 12, clamp=True)
add_par(base, page, 'menu', 'Avance', 'Las obras avanzan', 'gates', menu=m.AVANCES,
        menu_labels=['Una etapa por gate en el cluster', 'Una etapa cada Pasosetapa pasos'])
add_par(base, page, 'int', 'Pasosetapa', 'Pasos por etapa (y al deshacerse)', 2, 1, 16, clamp=True)
add_par(base, page, 'pulse', 'Sembrarzona', 'Sembrar Nota y sus vecinas (SEQ1, prueba)')
add_par(base, page, 'pulse', 'Sembrarzona2', 'Sembrar Nota2 y sus vecinas (SEQ2, prueba)')
add_par(base, page, 'int', 'Umbralmonte', 'Ocupacion desde la que sube el terreno (monte)', 8, 1, 30, clamp=True)
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
add_par(base, page, 'float', 'Traslucidez', 'Traslucidez del borde de la copa', 0.35, 0.0, 1.0)
add_par(base, page, 'float', 'Timidez', 'Timidez de copa (hueco entre copas)', 0.12, 0.0, 1.0)
add_par(base, page, 'float', 'Emergentes', 'Fraccion de emergentes del bosque', 0.1, 0.0, 1.0)
add_par(base, page, 'toggle', 'Orla', 'Orla de matorral en el borde del bosque', True)
add_par(base, page, 'float', 'Mezcla', 'Ejemplares del otro modelo del bioma', 0.3, 0.0, 1.0)
add_par(base, page, 'toggle', 'Impostores', 'De lejos, tarjetas de racimo', True)
add_par(base, page, 'float', 'Terrazaspornota', 'Bancales por nota del SEQ1 (arrozal)', 1.0, 0.0, 4.0)
add_par(base, page, 'int', 'Maxterrazas', 'Bancales maximos', 8, 1, 16, clamp=True)
add_par(base, page, 'float', 'Pasoterraza', 'Alto de un bancal (x el limite)', 0.12, 0.02, 0.5)
add_par(base, page, 'toggle', 'Riego', 'Los bancales junto a un rio se inundan', True)
add_par(base, page, 'rgb', 'Colorcultivo', 'Verde arroz de los bancales', (0.66, 0.80, 0.22))
add_par(base, page, 'float', 'Alturameseta', 'Alto de un nivel de meseta (x el limite)', 0.15, 0.0, 1.0)
add_par(base, page, 'int', 'Maxniveles', 'Niveles maximos de la meseta', 3, 1, 6, clamp=True)
add_par(base, page, 'menu', 'Marco', 'Marco de los frutales', 'tresbolillo', menu=m.MARCOS,
        menu_labels=['Marco real', 'Tresbolillo'])
add_par(base, page, 'toggle', 'Setos', 'Setos entre las parcelas de la meseta', True)
# v14 (motor v97): el oceano, los volcanes y el detalle que lleva la tarjeta grafica
add_par(base, page, 'toggle', 'Oceano', 'Oceano: las celdas vacias son mar; las ocupadas, islas', True)
add_par(base, page, 'float', 'Volcanes', 'Volcanes: parte de los conos de relieve que lo son', 0.2, 0.0, 1.0)
add_par(base, page, 'toggle', 'Detalle', 'Detalle alto: hojas de verdad desde el globo (tarjeta grafica)', True)
add_par(base, page, 'float', 'Tierra', 'Las conchas, como capas de tierra (0: losetas de color)', 0.75, 0.0, 1.0)
# v10: la ciudad legible
add_par(base, page, 'menu', 'Lenguaje', 'Lenguaje de la ciudad', 'latitud', menu=m.LENGUAJE_MODOS,
        menu_labels=['Por latitud (como los biomas)', 'Frio: hormigon y chapa', 'Templado: ladrillo y vidrio',
                     'Calido: cal y celosia', 'Mezcla'])
add_par(base, page, 'int', 'Variantesciudad', 'Variantes por diseno (biblioteca de la ciudad)', 3, 1, 6,
        clamp=True)
add_par(base, page, 'menu', 'Fijartipo', 'Fijar el diseno (para probar)', 'auto', menu=m.FIJAR_TIPOS,
        menu_labels=['Auto (el mapa logistico)', 'Diseno 1', 'Diseno 2', 'Diseno 3'])
add_par(base, page, 'float', 'Oblicuidad', 'Oblicuidad de los anadidos informales (grados)', 6.0, 0.0, 30.0)
add_par(base, page, 'float', 'Alturaplanta', 'Alto de una planta (x el limite)', 0.08, 0.01, 0.5)
add_par(base, page, 'float', 'Anchovano', 'Ancho de un vano (x el limite)', 0.05, 0.005, 0.5)
add_par(base, page, 'float', 'Retranqueo', 'Retranqueo de las torres', 0.15, 0.0, 0.4)
add_par(base, page, 'float', 'Torsionmax', 'Giro maximo de la torsionada (grados)', 90.0, 0.0, 360.0)
add_par(base, page, 'float', 'Parasitospornota', 'Parasitos por nota del SEQ1 (colonia)', 4.0, 0.0, 16.0)
add_par(base, page, 'int', 'Maxparasitos', 'Parasitos maximos', 24, 1, 64, clamp=True)
add_par(base, page, 'float', 'Modulomarco', 'Modulo del marco (x la celda)', 0.25, 0.1, 0.5)
add_par(base, page, 'int', 'Maxmarco', 'Niveles maximos del marco', 3, 1, 6, clamp=True)
add_par(base, page, 'float', 'Capsulas', 'Huecos del marco con capsula', 0.4, 0.0, 1.0)
add_par(base, page, 'float', 'Mutacion', 'Mutacion (hasta donde llegan las formas mutantes)', 0.5, 0.0, 1.0)
add_par(base, page, 'menu', 'Mutacionfuente', 'La mutacion la lleva', 'manual', menu=m.MUTACION_FUENTES,
        menu_labels=['El mando Mutacion', 'La saturacion del modular (fase 19)'])
add_par(base, page, 'toggle', 'Obra', 'La obra se ve entre etapas', True)
add_par(base, page, 'int', 'Desfasefachada', 'Plantas de la fachada por detras del esqueleto', 2, 0, 10, clamp=True)
add_par(base, page, 'toggle', 'Gruas', 'Gruas en las obras', True)
add_par(base, page, 'int', 'Maxgruas', 'Gruas a la vez', 6, 0, 32, clamp=True)
add_par(base, page, 'toggle', 'Tinteventanas', 'Una nota enciende las ventanas con el color de su SEQ', True)
add_par(base, page, 'float', 'Pasostinte', 'Pasos que tarda en apagarse ese color', 4.0, 0.25, 32.0)
add_par(base, page, 'float', 'Lodciudad', 'Remates pequenos desde (px por celda)', 60.0, 0.0, 400.0)
# v11: la industria
add_par(base, page, 'toggle', 'Recursos', 'La mina saca lo que guarda la concha de abajo', True)
add_par(base, page, 'menu', 'Epoca', 'Epoca de la industria', 'eras', menu=m.EPOCA_MODOS,
        menu_labels=['Por las eras enterradas', 'Vapor', 'Acero', 'Quimica'])
add_par(base, page, 'int', 'Variantesind', 'Variantes por diseno (industria)', 3, 1, 6, clamp=True)
add_par(base, page, 'float', 'Bancospornota', 'Bancos de la corta por nota del SEQ1', 1.0, 0.0, 4.0)
add_par(base, page, 'int', 'Maxbancos', 'Bancos maximos de la corta', 6, 1, 12, clamp=True)
add_par(base, page, 'int', 'Maxbastidor', 'Niveles maximos del bastidor (planta integrada)', 3, 1, 6, clamp=True)
add_par(base, page, 'float', 'Emisiones', 'Humo y vapor de la industria', 0.5, 0.0, 2.0)
add_par(base, page, 'int', 'Maxhumo', 'Particulas de humo maximas', 6000, 0, 20000, clamp=True)
add_par(base, page, 'float', 'Lodind', 'Remates pequenos de la industria desde (px por celda)', 60.0, 0.0, 400.0)
ok('pagina Fase11: Tema (naturaleza), Pesovecina 0,5, Umbralvecindad 4, Mincluster 2, Caos 3,91, '
   'Maxpiezas 6, Avance (gates), Pasosetapa 2, Sembrarzona, Sembrarzona2; v5: Umbralmonte 8, '
   'Limitebosque 0,65, Limitenieve 0,9, Alturamonte 1, Lodnat 80, Tintebordenat 0,8; v8: '
   'Ligero, Refresconat 0,25, Biomas, Variantes 2, Traslucidez 0,35, '
   'Timidez 0,12, Emergentes 0,1, Orla, Mezcla 0,3, Impostores, Terrazaspornota 1, Maxterrazas 8, '
   'Pasoterraza 0,12, Riego, Colorcultivo, Alturameseta 0,15, Maxniveles 3, Marco '
   '(tresbolillo), Setos; v10: Lenguaje (latitud), Variantesciudad 3, Fijartipo (auto), Oblicuidad 6, '
   'Alturaplanta 0,08, Anchovano 0,05, Retranqueo 0,15, Torsionmax 90, Parasitospornota 4, Maxparasitos 24, '
   'Modulomarco 0,25, Maxmarco 3, Capsulas 0,4, Mutacion 0,5, Mutacionfuente (manual), Obra, '
   'Desfasefachada 2, Gruas, Maxgruas 6, Tinteventanas, Pasostinte 4, Lodciudad 60; v11: Tema + industria, '
   'Recursos, Epoca (eras), Variantesind 3, Bancospornota 1, Maxbancos 6, Maxbastidor 3, Emisiones 0,5, '
   'Maxhumo 6000, Lodind 60; v14: Oceano, Volcanes 0,2, Detalle, Resolucion (720p); v16: Pradera 300000, Mata 0,16; v17: Tierra 0,75')
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
ok('modelos: %d modelos (%d piezas, %d ejemplares de la biblioteca: %d plantas x %d variantes x '
   'derivaciones, cerca y lejos; y %d edificios: %d disenos x %d variantes) generados en %s'
   % (n_modelos, n_piezas, len(m.ejemplares_de(m.cfg())), len(m.PLANTAS), m.variantes(m.cfg()),
      len(m.edificios_de(m.cfg())), len(m.DISENOS), m.variantes_ciudad(m.cfg()), modelos.path))
if ajustadas:
    info('la caja o el prisma unidad no salian de lado 1 y centrados (%d, p. ej. %s): se han llevado '
         'a la unidad midiendo sus puntos' % (len(ajustadas), ajustadas[0]))

# -----------------------------------------------------------------------------
# GEOMETRIAS: una por modelo (pulida y porosa; desde la fase 12, una sola con
# el shader de la piel), y las particulas
# -----------------------------------------------------------------------------

instanciar_modelos(base, m)
terreno_al_dia(base, m)                 # v5: la malla del relieve (esfera desplazada por el mapa de alturas)
particulas_al_dia(base, crear=True)     # comun v54: motas suaves (mat_motas) y los trenes en 'vagones'
humo_al_dia(base, crear=True)           # comun v53: el humo, en la GPU (mat_humo)
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
  Maxterrazas, Pasoterraza, Riego, Colorcultivo) y
  meseta-jardin (Alturameseta, Maxniveles, Marco, Setos); textura
  'cultivos' para el shader. Ligero (por defecto): la naturaleza se
  recalcula cada Refresconat s (a saltos), 6 arboles por celda de bosque y
  tarjetas de racimo con la camara de globo.
  v10, ciudad legible: cada etapa es un tipo de edificio (biblioteca de
  edificios por gramatica, modelos/edi_*; la fachada la dibuja el shader),
  con lenguaje por latitud (Lenguaje), obra visible entre etapas (Obra,
  Desfasefachada, Gruas, Maxgruas), construcciones mutantes (colonia:
  Parasitospornota, Maxparasitos; marco: Modulomarco, Maxmarco, Capsulas;
  Mutacion, Mutacionfuente), torres que se buscan en los clusters, el tinte
  del secuenciador en las ventanas (Tinteventanas, Pasostinte) y Lodciudad.
  v11, tema industria: mina (SEQ1) y energia (SEQ2), del aserradero y la
  bocamina a la refineria y la central; recurso de la concha de abajo
  (Recursos), Epoca, corta que devora (Bancospornota, Maxbancos) y planta
  integrada (Maxbastidor), humo (Emisiones, Maxhumo), Variantesind, Lodind.""")

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


def _omax(c):
    """La ocupacion hasta la que se recorren las escaleras: 9 con los umbrales de
    fabrica; con Umbralram o Pasoumbral mas altos, hasta la ultima etapa (corona)."""
    return max(9, int(c['th_crown']))


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
            geos = dict((mo, set()) for mo in list(m.MODELOS) + m.ejemplares_de(c) + m.PLANTAS + m.FORMAS
                        + m.edificios_de(c))
            for g, mo, _ in m.geometrias_piel(c):
                geos[mo].add(g)
            puentes = sum(len(inst.get(g, [])) for g in geos[pm])
            prot = m.modelos_de(c, tema, esp, 'protagonista')[m.clase_cluster(n_cl)]
            if tema in ('ciudad', 'industria'):     # v10-v11: la pieza del cluster (losa, torres...)
                n_prot = sum((W.get('piel') or {}).get('ciudad', {}).get('protagonistas', {}).values())
            else:
                n_prot = sum(len(inst.get(g, [])) for g in geos.get(prot, ()))
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
            else:                           # v10: la ciudad, con su pieza de cluster en la planificada
                edis = sum(len(f) for g, f in inst.items() if g.startswith('mod_edi_') and 'zocalo' not in g)
                en_obra = len(m.obras_ciudad(W, c))
                t.check('%s, %s: Sembrarzona x2 -> cluster de %d celdas, %d edificios (%d en obra), %d puentes%s'
                        % (tema, esp, n_cl, edis, en_obra, puentes,
                           ' y la pieza del cluster' if esp in ('planificada', 'energia') else ''),
                        n_cl == 1 + len(m.NEIGH[i]) and puentes == enlaces > 0 and edis + en_obra >= n_cl
                        and n_prot == (1 if esp in ('planificada', 'energia') else 0) and not otro,
                        'cluster %d, puentes %d de %d, pieza %d, del otro tema %d'
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
            m.subir_escalon(Wg, cg, m.GEO, x, 100, now, 120.0)
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
            m.subir_escalon(Wp, cp, m.GEO, x, 100, now, 120.0)
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
            m.subir_escalon(Wc, ch, m.GEO, x, 100, now, 120.0)
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
    # 8. la ciudad planificada coronada (v10): un rascacielos terminado, sin grua
    cz = dict(cp)
    cz.update(tema=1, avance=0)
    Wz = m.new_world()
    for _ in range(2):
        for x in zona:
            m.subir_escalon(Wz, cz, m.ARQ, x, 100, now, 120.0)
    for _ in range(60):
        m.note_on(Wz, cz, m.ARQ, nota, 100, now, 120.0)
    m.cerrar_obras(Wz, cz)
    Wz['vh'] = list(Wz['h'])
    instz = m.build_instances(Wz, cz, now + 10.0)
    infz = m.info_ciudad(Wz, cz, i)
    t.check('ciudad planificada coronada: un rascacielos (%s) terminado, sin grua' % infz['diseno'],
            infz['tipo'] == 'rascacielos' and instz.get(m.geometria_de(m.nombre_edificio(infz['diseno'],
                                                                                          infz['var'])))
            and not instz.get('mod_ciu_grua'), 'tipo %s' % infz['tipo'])
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
    _prueba_ciudad(t, m)
    _prueba_industria(t, m)
    _prueba_rendimiento_td(t, m)


def _prueba_natural(t, m):
    """Las pruebas de la naturaleza: la v5 (naturaleza legible), la v8 (brotes,
    arboles y terrazas) y la v14 (oceano, islas, volcanes y detalle). Las de la v5 y
    la v8 se hacen sin oceano, sin volcanes y sin Detalle (miden el relieve y los
    impostores tal como eran); las de la v14, con ellos."""
    guarda = {}
    for nm in ('Oceano', 'Volcanes', 'Detalle'):
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    try:
        base.par.Oceano, base.par.Volcanes, base.par.Detalle = False, 0.0, False
        _prueba_natural_(t, m)
        base.par.Oceano, base.par.Volcanes, base.par.Detalle = True, 1.0, True
        _prueba_oceano(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass


def _prueba_oceano(t, m):
    """v14 (motor v97): oceano con islas que crecen y se unen, volcanes y Detalle."""
    import numpy as np
    base.par.Tema = 'naturaleza'
    c = m.cfg()
    i = m.note_cell(int(base.par.Nota))
    rej = m._rejilla(np)

    def mundo(celdas, own, occ, vel=100):
        W = m.new_world()
        for x in celdas:
            W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = occ, own, own, vel
            W['h'][x] = W['vh'][x] = m.height_for(c, occ)
        return W

    def tierra(W):
        return m.terreno(W, c)['E'] > m.ORILLA_PLANTA

    # 1. el mar: sin nada ocupado, todo agua; la malla flota sobre las losetas
    W0 = m.new_world()
    u = m.uniformes_piel(W0, c, 10.0)
    t.check('oceano: sin celdas ocupadas todo es mar (la malla del terreno flota %.3f sobre las losetas; '
            'sin Oceano se hunde %.2f)' % (m.OCEANO_LIFT, m.HUNDIDO),
            not tierra(W0).any() and u['uOceano'][0] == 1.0 and abs(u['uTerreno'][2] + m.OCEANO_LIFT) < 1e-9
            and m.uniformes_piel(W0, dict(c, oceano=0), 10.0)['uTerreno'][2] == m.HUNDIDO)
    # 2. una isla que crece con la ocupacion
    areas = []
    for o in (1, 3, 6, 9):
        areas.append(int((tierra(mundo([i], m.GEO, o)) & (rej['celda'] >= 0)).sum()))
    W1 = mundo([i], m.GEO, 1)
    ter1 = m.terreno(W1, c)
    t.check('isla: una celda ocupada es una isla (el centro a %.3f sobre el mar) que crece con la ocupacion '
            '(%s texeles de tierra con 1, 3, 6 y 9)'
            % (ter1['centro'][i], ' < '.join(str(a) for a in areas)),
            ter1['centro'][i] > m.ORILLA_PLANTA and all(b > a for a, b in zip(areas, areas[1:]))
            and ter1['islas'] == 1)
    # 3. dos islas vecinas se unen por un istmo; tres o mas, un archipielago
    j = m.NEIGH[i][0]
    medio = m._norm(m._add(m.NORMALS[i], m.NORMALS[j]))
    sueltas = m.alto_en(m.terreno(mundo([i, j], m.GEO, 1), c), medio)
    Wu = mundo([i, j] + [x for x in m.NEIGH[i][1:3]], m.GEO, 4)
    teru = m.terreno(Wu, c)
    t.check('islas vecinas: con ocupacion 1 hay mar entre ellas (%.3f); al crecer se unen por un istmo (%.3f) '
            'y son un archipielago (%d isla, %d archipielago)' % (sueltas, m.alto_en(teru, medio), teru['islas'],
                                                                 teru['archipielagos']),
            sueltas < m.ORILLA_PLANTA < m.alto_en(teru, medio) and teru['islas'] == 1
            and teru['archipielagos'] == 1)
    # 4. nada crece en el mar; la costa calida trae palmeras y manglares
    Wb = mundo([i], m.GEO, int(c['th_fusion']))
    instb = m.build_instances(Wb, c, absTime.seconds + 10.0)
    terb = m.terreno(Wb, c)
    mods = dict((g, mo) for g, mo, _ in m.geometrias_piel(c))
    pies = [(mods[g], f) for g, fs in instb.items() if g in mods and m.es_ejemplar(mods[g]) for f in fs]
    secos = all(m.alto_en(terb, m._norm(tuple(f[:3]))) >= 0.004 for _, f in pies)
    calida = [x for x in range(m.N) if m.bioma_de(x) == 'calido' and not m.is_pole(x)]
    costa = set(m.planta_de(mundo([x], m.GEO, 3, v), c, x, True) for x in calida for v in (40, 70, 100, 127))
    t.check('en el mar no crece nada (%d ejemplares, todos en tierra) y la costa calida trae palmera y mangle'
            % len(pies), pies and secos and 'mangle' in costa and 'palmera' in costa, 'costa: %s' % sorted(costa))
    # 5. volcanes: con Volcanes 1, el cono suelto es un volcan con crater, lava y penacho
    Wv = mundo([i], m.ARQ, int(c['th_crown']), 110)
    instv = m.build_instances(Wv, c, absTime.seconds + 10.0)
    terv = m.terreno(Wv, c)
    sel = rej['celda'] == i
    L = terv['L'] if terv['L'] is not None else np.zeros_like(terv['E'])
    borde = float(terv['E'][sel].max())
    t.check('volcan: el cono es un volcan (crater %.2f por debajo del borde), con lava en el mapa (crater y '
            'coladas) y penacho de %d bocanadas; con Volcanes 0, ninguno'
            % (borde - terv['centro'][i], len(instv.get('humo', []))),
            [v[0] for v in terv['volcanes']] == [i] and terv['centro'][i] < borde - 0.02 * terv['hmax']
            and L[sel].max() > 0.9 and ((L > 0.2) & (L < 0.7)).any() and len(instv.get('humo', [])) >= 3
            and not m.rasgos_terreno(Wv, dict(c, volcanes=0.0))[1]['volcanes'])
    paso = m.step_dur(c, 120.0)
    compas = paso * int(c['steps_per_beat']) * int(c['beats_per_bar'])
    serie = [m.erupcion(c, i, k * 0.25 * compas, paso) for k in range(4 * (m.ERUPCION_CADA[1] + 2))]
    activos = sum(1 for v in serie if v > 0)
    t0 = next(k for k, v in enumerate(serie) if v > 0) * 0.25 * compas
    inste = m.build_instances(Wv, c, t0 + 0.3 * compas)
    ue = m.uniformes_piel(Wv, c, t0 + 0.3 * compas)
    t.check('erupcion: de cuando en cuando (%d de %d cuartos de compas), con mas humo (%d bocanadas), brasas y '
            'ceniza, y la lava al rojo (uVolcan0 %.2f)' % (activos, len(serie), len(inste.get('humo', [])),
                                                         ue['uVolcan0'][3]),
            0 < activos <= 0.25 * len(serie) and len(inste.get('humo', [])) > len(instv.get('humo', []))
            and len(inste.get('particulas', [])) >= 10 and ue['uVolcan0'][3] > 0.2
            and abs(sum(ue['uVolcan0'][q] * m.NORMALS[i][q] for q in range(3)) - 1.0) < 1e-6
            and Wv['piel']['volcanes'] == 1)
    # 6. Detalle: hojas de verdad desde el globo, y mas presupuesto
    Wd = mundo([i] + list(m.NEIGH[i]), m.GEO, int(c['th_fusion']))
    instd = m.build_instances(Wd, c, absTime.seconds + 10.0)
    lod = [g for g in instd if g in mods and mods[g].endswith('_lod') and instd[g]]
    hojas_d = Wd['piel']['hojas']
    cl = dict(c, detalle=0)
    m.build_instances(Wd, cl, absTime.seconds + 10.0)
    t.check('Detalle: desde el globo, hojas de verdad (%d hojas, sin tarjetas de racimo; sin Detalle, %d) y '
            'presupuesto de %d' % (hojas_d, Wd['piel']['hojas'], m.presupuesto_hojas(c)),
            not lod and hojas_d > 2 * Wd['piel']['hojas'] and m.presupuesto_hojas(c) == m.HOJAS_DETALLE
            and m.cerca_de(Wd, c, i) and not m.cerca_de(Wd, dict(cl, superficie=0), i))
    # 7. cada planta, su verde; la malla del terreno, el doble de fina; el shader
    verdes = set(m.TONO_PLANTA[mo] for mo in m.PLANTAS)
    sh = base.op('piel_pixel').text if base.op('piel_pixel') is not None else ''
    esf = base.op('terreno').op('esfera') if base.op('terreno') is not None else None
    t.check('paleta: %d plantas, %d verdes distintos (todos con el verde por delante); corteza y flores en la '
            'malla; el shader pinta mar, playa, lava y relieve fino; malla del terreno de %d x %d'
            % (len(m.PLANTAS), len(verdes), TERRENO_FILAS, TERRENO_COLS),
            len(verdes) == len(m.PLANTAS) and all(v[1] > v[0] and v[1] > v[2] for v in verdes)
            and all(k in sh for k in ('uOceano', 'uVolcan0', 'relieveFino', 'CORTEZA', 'FLOR'))
            and esf is not None and int(esf.par.rows) == TERRENO_FILAS and int(esf.par.cols) == TERRENO_COLS
            and any(u_[0] > 3.95 for u_ in m.malla_ejemplar(m.nombre_ejemplar('retama', 0, 1), c)[2])
            and any(abs(u_[1] - 0.5) < 1e-9 for u_ in m.malla_ejemplar(m.nombre_ejemplar('abedul', 0, 3), c)[2]))
    m.reset_world()
    m.on_pulse('Sembrarzona2')
    W = m.world()
    W['vh'] = list(W['h'])
    m.build_instances(W, m.cfg(), absTime.seconds + 10.0)
    t.check('leyenda MAR (islas, archipielagos, volcanes)', '  MAR ' in m.legend())
    # v16 (motor v99): el doble de grande, la pradera en la GPU y el mapa por capas
    import time
    cw, cl_ = m._cell_sizes(c['core_radius'], i)
    t.check('escala: nucleo de radio %g; la celda de Nota mide %.1f x %.1f, %.1f veces el limite de altura '
            '(antes 1,2); las luces fijas, al doble (una sola vez)' % (c['core_radius'], cw, cl_,
                                                                       min(cw, cl_) / m.limit(c)),
            c['core_radius'] == 12.0 and min(cw, cl_) > 2.0 * m.limit(c)
            and 'escala:nucleo12' in (base.fetch('migraciones', [], search=False) or []))
    pr = base.op('pradera')
    vsh = base.op('piel_vertex').text if base.op('piel_vertex') is not None else ''
    Pm, _, Um, Tm = m.malla_pradera()
    un = m.uniformes_piel(m.new_world(), c, 10.0)
    t.check('pradera: una mata de %d triangulos instanciada Pradera veces (%d) sin datos por instancia; la coloca '
            'el vertex shader (uFamilia 7) sobre el mapa de alturas; en la ciudad, ninguna'
            % (len(Tm), int(un['uPradera'][0])),
            pr is not None and pr.op('mata') is not None and base.op('n_pradera') is not None
            and base.op('mat_piel_pradera') is not None and 'mat_piel_pradera' in (pr.par.material.expr or '')
            and str(pr.par.instanceop.eval() or '').endswith('n_pradera')
            and all(k in vsh for k in ('uPradera', 'TDInstanceID', 'azar('))
            and int(un['uPradera'][0]) == int(base.par.Pradera) > 0 and 20 <= len(Tm) <= 80
            and all(2.0 <= u_[0] < 3.0 for u_ in Um)
            and m.uniformes_piel(m.new_world(), dict(c, tema=1), 10.0)['uPradera'][0] == 0.0
            and 'pradera' in str(base.op('render').par.geometry.val).split())
    Wc = mundo(range(m.N), m.GEO, 9)
    for x in range(0, m.N, 3):
        Wc['own'][x] = Wc['sp'][x] = m.ARQ
    m.terreno(Wc, c)
    ts = []
    for k in range(5):
        Wc['occ'][(11 * k + 5) % m.N] += 1
        t0 = time.time()
        Ei = m.terreno(Wc, c)['E'].copy()
        ts.append(time.time() - t0)
    m._TERRENO.pop('capas', None)
    m._TERRENO['clave'] = m._TERRENO['sello_t'] = None
    t0 = time.time()
    Ef = m.terreno(Wc, c)['E']
    entero = time.time() - t0
    t.check('mapa de alturas por capas: una nota rehace solo lo que cambia (%.0f ms; entero, %.0f ms) y da '
            'exactamente el mismo mapa' % (1000 * min(ts), 1000 * entero),
            float(np.abs(Ei - Ef).max()) == 0.0 and min(ts) < 0.6 * entero)
    # v17 (motor v100): el mar no sedimenta; la tierra sube sobre el; las conchas, de tierra
    c8 = dict(c, nivel=max(15, c['nivel']))
    j = m.NEIGH[i][0]
    lejos = max(range(m.N), key=lambda x: -sum(m.NORMALS[x][q] * m.NORMALS[i][q] for q in range(3)))
    Ws = mundo([i, j], m.GEO, 3)
    m.ensure(Ws)
    Ws['ciclo_t0'] = 0.0
    core = c8['core_radius']
    m.end_cycle(Ws, c8, 10.0)
    g1 = m.top_radius(Ws, c8) - core
    solo = [x for x in range(m.N) if Ws['cols'][x]]
    u8 = m.uniformes_piel(Ws, c8, 11.0)
    t.check('sedimentacion: al enterrar un mundo con 2 celdas ocupadas, la concha (%.2f) solo deja loseta en '
            'ellas (%d de %d); el mar sigue en el nucleo (nivel del mar %.2f) y la concha lo apunta (rm)'
            % (g1, len(solo), m.N, m.nivel_mar(Ws, c8)),
            sorted(solo) == sorted([i, j]) and g1 > 0 and abs(m.suelo(Ws, c8, i) - core - g1) < 1e-6
            and abs(m.nivel_mar(Ws, c8) - core) < 1e-9 and abs(u8['uOceano'][2] - core) < 1e-6
            and Ws['shells'][-1]['rm'][lejos] == 1 and Ws['shells'][-1]['rm'][i] == 0
            and all(m.sedimenta(Ws, dict(c8, oceano=0))) and all(m.sedimenta(Ws, dict(c8, tema=1))))
    est = base.op('estratos')
    t.check('conchas como capas de tierra: estratos con mat_piel_estrato (uFamilia 8) y Tierra %.2f en la '
            'naturaleza (0 en la ciudad); la celda que suena ilumina su suelo' % u8['uTierra'][0],
            base.op('mat_piel_estrato') is not None and (est is None or c['nivel'] < 15
                                                         or 'mat_piel_estrato' in (est.par.material.expr or ''))
            and abs(u8['uTierra'][0] - float(base.par.Tierra)) < 1e-9
            and m.uniformes_piel(Ws, dict(c8, tema=1), 11.0)['uTierra'][0] == 0.0
            and all(k in sh for k in ('uTierra', 'sobreMar', 'estrato')))
    # v15: con las 85 celdas ocupadas sigue habiendo mar
    Wll = mundo(range(m.N), m.GEO, 12)
    agua = float((~tierra(Wll)).mean())
    t.check('con todas las celdas ocupadas sigue habiendo mar (%d %% del mapa)' % int(100 * agua),
            0.08 < agua < 0.6)
    m.reset_world()


def _prueba_natural_(t, m):
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
            and not prim and cv > 0.6 and len(m.ARBOLES) == 15 and len(m.MATORRALES) == 8,
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
    for mo in [x for x in m.ARBOLES if x not in m.SIN_FUSTE]:     # v14: el mangle y el cardon no tienen fuste
        filas = {}
        for x, y in sil[mo]:
            filas.setdefault(y, []).append(x)
        ancho = lambda y: (max(filas[y]) - min(filas[y]) + 1) if y in filas else 0
        if min(ancho(0), ancho(1)) > 0.35 * max(ancho(y) for y in filas):
            tronco.append(mo)
    mat_arb = max(m.iou(sil[p], sil[q]) for p in m.ARBOLES for q in m.MATORRALES)
    t.check('a 18 px los %d arboles se distinguen (el par mas parecido, %s y %s, %.2f), todos con el tronco '
            'visible, y ninguno se confunde con un matorral (%.2f)' % (len(m.ARBOLES), peor[0], peor[1], peor[2],
                                                                       mat_arb),
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
    instm = m.build_instances(Wm, dict(c, sway_max=0.0, viento_max=0.0), 3.0)   # sin balanceo ni viento
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
    t.check('el arbol se inclina hacia el lado sin vecinas (%.1f grados, <= %.0f); de lejos, '
            'tarjetas de racimo si Impostores (%d)' % (ang, c['inclinacion'], len(lejos)),
            0.5 < ang <= c['inclinacion'] + c.get('sway_max', 0.0) + 0.6
            and (bool(lejos) != bool(m.cerca_de(Wi, c, i))
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
    # los tiempos se informan, no se comprueban: dependen de la maquina y de lo que haga en
    # ese momento, y la naturaleza no se recalcula en cada fotograma sino cada Refresconat
    # (unas 4 veces por segundo); lo que se comprueba es el presupuesto de hojas
    ref = float(m.cfg().get('refresco_nat', 0.25))
    por_foto = 1000 * tiempos['naturaleza'] * (min(1.0, 1.0 / (30.0 * ref)) if ref > 0 else 1.0)
    t.check('rendimiento: %d celdas en bosque maximo, hojas %d (presupuesto %d); naturaleza %.1f ms por calculo '
            '(cada %.2f s: unos %.1f ms por fotograma a 30 fps), ciudad %.1f ms (solo se informa)'
            % (m.N, hojas, m.presupuesto_hojas(cc), 1000 * tiempos['naturaleza'], ref, por_foto,
               1000 * tiempos['ciudad']),
            hojas <= m.presupuesto_hojas(cc))
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
    # v9: la pagina mas corta
    fuera = [nm for nm, _, _ in FASE11_FIJOS if has_par(base, nm)]
    t.check('pagina Fase11 sin Rebote, Maxcaosnat, Varangulo, Cuantizar30, Inclinacion, '
            'Densidadhoja ni Muroterraza', not fuera, 'siguen: %s' % ', '.join(fuera) if fuera else '')
    cf = m.cfg()
    t.check('los siete fijos, en su valor por defecto',
            all(cf[k] == m.DEFAULT_CFG[k] for k in ('rebote', 'max_caos_nat', 'var_angulo', 'cuantizar30',
                                                     'inclinacion', 'densidad_hoja', 'muro_terraza')))



def _prueba_ciudad(t, m):
    """Las pruebas de la ciudad legible (v10): edificios por etapa, lenguajes,
    obra y construcciones mutantes."""
    import math
    import time
    guarda = {}
    for nm in ('Tema', 'Lenguaje', 'Mutacion', 'Mutacionfuente', 'Fijartipo', 'Avance'):
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    try:
        _prueba_ciudad_(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass


def _prueba_ciudad_(t, m):
    import math
    import time
    base.par.Tema = 'ciudad'
    base.par.Lenguaje = 'latitud'
    base.par.Fijartipo = 'auto'
    base.par.Mutacion = 0.5
    base.par.Mutacionfuente = 'manual'
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    c = m.cfg()
    c12 = dict(c, nivel=max(12, c['nivel']), respaldo=0)    # las filas con el shader (alfa y canales)
    ahora = absTime.seconds + 10.0
    unico = [10.0]

    def t_unico():
        unico[0] += 1.0             # cada mundo, su cuenta de colonas (la piel la guarda por celda)
        return unico[0]

    def mundo(celdas, own, occ, vel=100, cerrar=True):
        W = m.new_world()
        for x in celdas:
            W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = occ, own, own, vel
            W['h'][x] = W['vh'][x] = m.height_for(m.cfg(), occ)
            W['t_nac'][x] = -50.0
        if cerrar:
            m.cerrar_obras(W, m.cfg())
        return W

    def edis(inst, celda=None, pref='mod_edi_'):
        """[(geometria, fila)] de los ejemplares de la ciudad (de una celda)."""
        out = []
        for g, fs in inst.items():
            if g.startswith(pref):
                for f in fs:
                    if celda is None or max(range(m.N), key=lambda x: sum(f[q] * m.NORMALS[x][q]
                                                                          for q in range(3))) == celda:
                        out.append((g, f))
        return out

    def filas(inst, g):
        return inst.get(m.geometria_de(g), [])

    # 0. la biblioteca: disenos x variantes, cada etapa con pie, cuerpo con ritmo y remate
    n_bib = m.biblioteca_ciudad(c)
    desnudas = []
    for esp in ('informal', 'planificada'):
        for tipo in m.TIPOS[esp]:
            for d in m.DISENOS_TIPO[tipo]:
                ex = m.edificio(c, d, 0)
                ritmo = any(v['fach'] in (m.F_RETICULA, m.F_IRREGULAR, m.F_LOGGIA, m.F_SIERRA, m.F_ZOCALO,
                                          m.F_CORONA) for v in ex['vols'])
                remate = bool(ex['rem']) or len(ex['vols']) > 1
                if not (ritmo and remate):
                    desnudas.append(d)
    P, Nn, U, T = m.malla_edificio('edi_punto_0', c)
    t.check('biblioteca de la ciudad: %d ejemplares (%d disenos x %d variantes); ninguna etapa es una caja '
            'desnuda; la fachada va en el uv (%d puntos, %d triangulos en la torre-punto)'
            % (n_bib, len(m.DISENOS), m.variantes_ciudad(c), len(P), len(T)),
            n_bib == len(m.DISENOS) * m.variantes_ciudad(c) and not desnudas and P and min(u[0] for u in U) >= 10.0
            and max(p[1] for p in P) <= 1.0 + 1e-9 and min(p[1] for p in P) >= -1e-9,
            'desnudas: %s' % desnudas)
    # 1. escalera informal: ocupacion 1 a 9 en una celda
    serie = []
    for o in range(1, _omax(c) + 1):
        W = mundo([i], m.GEO, o)
        inf = m.info_ciudad(W, c, i)
        inst = m.build_instances(W, c, ahora)
        serie.append((o, inf['tipo'], inf['diseno'], len(edis(inst, i)), inst))
    # lo esperado, con los umbrales de la fase 4 del proyecto (Umbralram, Pasoumbral)
    esperado = [m.TIPOS['informal'][m.etapa_ciudad(c, 'informal', o) - 1] for o in range(1, _omax(c) + 1)]
    casa = serie[1][4]
    varillas = bool(filas(casa, 'ciu_varillas')) or not m.lod_ciudad(mundo([i], m.GEO, 2), c, i)
    tres = m.edificio(c, serie[2][2], m.info_ciudad(mundo([i], m.GEO, 3), c, i)['var'])
    bandas = len(set(v['slot'] for v in tres['vols'][:3]))
    t.check('escalera informal 1 -> %d: %s; la casa que crece con varillas, tres plantas de %d colores'
            % (_omax(c), ' / '.join('%d %s' % (o, d) for o, _, d, _, _ in serie), bandas),
            [x[1] for x in serie] == esperado and set(esperado) == set(m.TIPOS['informal'])
            and all(x[3] >= 1 for x in serie) and varillas and bandas == 3,
            'tipos %s' % [x[1] for x in serie])
    # 2. escalera planificada, con la obra entre etapas (grua, esqueleto, fachada con desfase)
    serie = []
    for o in range(1, _omax(c) + 1):
        W = mundo([i], m.ARQ, o)
        serie.append((o, m.info_ciudad(W, c, i)['tipo'], m.info_ciudad(W, c, i)['diseno']))
    esperado = [m.TIPOS['planificada'][m.etapa_ciudad(c, 'planificada', o) - 1] for o in range(1, _omax(c) + 1)]
    cg = dict(c12)
    cg.update(avance=0)
    Wo = m.new_world()
    t0 = 100.0
    vistas = []
    k = 0
    while m.etapa_ciudad(cg, 'planificada', Wo['occ'][i]) < 5 and k < 400:   # notas del SEQ2 hasta el rascacielos
        m.note_on(Wo, cg, m.ARQ, nota, 100, t0 + 0.01 * k, 120.0)
        k += 1
    pasos_ = m.pasos_obra('planificada', 'rascacielos')
    gruas = esq = fachada = 0
    for q in range(len(pasos_) + 1):
        Wo['vh'] = list(Wo['h'])
        tq = t0 + 10.0 + q
        inst = m.build_instances(Wo, cg, tq + 5.0)
        vistas.append(m.obras_ciudad(Wo, cg).get(i, 'terminada'))
        ed = edis(inst, i)
        if filas(inst, 'ciu_grua'):
            gruas += 1
        if ed and any(int(f[11]) == 1 for _, f in ed):
            esq += 1
        if vistas[-1] == 'fachada' and ed and any(0.0 < f[10] % 1.0 < 0.998 for _, f in ed):
            fachada += 1
        m.note_on(Wo, cg, m.ARQ, nota, 100, tq, 120.0)
        m.note_off(Wo, cg, m.ARQ, nota, tq + 0.01, 120.0)
        while Wo['occ'][i] > 8:
            break
    fin_ok = vistas[-1] == 'terminada'
    t.check('escalera planificada 1 -> %d: %s; la obra entre etapas: %s (grua en %d pasos, esqueleto en %d, '
            'fachada con desfase en %d)' % (_omax(c), ' / '.join('%d %s' % (o, d) for o, _, d in serie), ' -> '.join(vistas),
                                            gruas, esq, fachada),
            [x[1] for x in serie] == esperado and set(esperado) == set(m.TIPOS['planificada'])
            and vistas[:len(pasos_)] == pasos_ and fin_ok and gruas >= 3
            and esq >= 1 and fachada >= 1, 'tipos %s' % [x[1] for x in serie])
    # 3. semilla: Velprueba 100 dos veces, el mismo edificio; 101, otro
    def edificio_de(vel):
        W = mundo([i], m.ARQ, 8, vel)
        inf = m.info_ciudad(W, c, i)
        return (inf['diseno'], inf['var'], inf['giro']), sorted(tuple(round(v, 5) for v in f)
                                                             for _, f in edis(m.build_instances(W, c, ahora), i))
    a, b, a2 = edificio_de(100), edificio_de(101), edificio_de(100)
    t.check('semilla: Velprueba 100 dos veces da el mismo edificio (%s %d); 101, otro (%s %d)'
            % (a[0][0], a[0][1], b[0][0], b[0][1]), a == a2 and a[0] != b[0])
    # 4. lenguaje: la misma tipologia en el ecuador, templada y en el polo; en directo
    def por_leng(lg):
        return [x for x in range(m.N) if m.lenguaje_celda(c, x) == lg and not m.is_pole(x)]
    lengs = []
    for lg in (2, 1, 0):
        x = por_leng(lg)[len(por_leng(lg)) // 2]
        W = mundo([x], m.ARQ, 3)
        f = edis(m.build_instances(W, c12, ahora), x)
        lengs.append(m.lenguaje_fila(f[0][1][12]) if f else -1)
    base.par.Lenguaje = 'latitud'
    W = m.world()
    m.reset_world()
    W = m.world()
    ce = por_leng(2)[0]
    for _ in range(3):
        m.note_on(W, m.cfg(), m.ARQ, m.cell_note(ce), 100, ahora, 120.0)
    m.tick(W, m.cfg(), ahora + 0.01, 120.0, True)
    antes = W['leng'][ce]
    base.par.Lenguaje = 'frio'
    m.tick(W, m.cfg(), ahora + 0.02, 120.0, True)
    sigue = W['leng'][ce]
    o0 = W['occ'][ce]
    k = 0
    while m.etapa_ciudad(m.cfg(), 'planificada', W['occ'][ce]) == m.etapa_ciudad(m.cfg(), 'planificada', o0) \
            and k < 200:
        m.note_on(W, m.cfg(), m.ARQ, m.cell_note(ce), 100, ahora + 0.03, 120.0)
        k += 1
    nuevo = W['leng'][ce]
    base.par.Lenguaje = 'latitud'
    t.check('lenguaje: ecuador cal y celosia, templado ladrillo y vidrio, polo hormigon y chapa (%s); en directo, '
            'lo construido conserva el suyo (%d -> %d) y la etapa siguiente sale fria (%d)'
            % ('/'.join(str(x) for x in lengs), antes, sigue, nuevo),
            lengs == [2, 1, 0] and antes == 2 and sigue == 2 and nuevo == 0)
    # 5. colonizacion: torre-punto con 1, 3 y 6 notas del SEQ1
    base.par.Fijartipo = '2'
    c = m.cfg()
    res5 = []
    for notas in (1, 3, 6):
        W = mundo([i], m.ARQ, 3)
        W['t_nac'][i] = t_unico()
        for _ in range(notas):
            m.note_on(W, c, m.GEO, nota, 100, 2.0, 120.0)
        W['occ'][i] = 3
        m.cerrar_obras(W, c)
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, c, ahora)
        inf = m.info_ciudad(W, c, i)
        pts = m.puestos_colonia(inf['ex'], W['par_vis'][i], inf['mut'], 0.5, inf['plantas'])
        par = [f for g, f in edis(inst, i) if g.startswith(('mod_edi_cuarto', 'mod_edi_chabola'))]
        res5.append((notas, W['par_vis'][i], len(par), pts))
    azotea = all(p[5] == 0 for p in res5[0][3])
    bajan = sum(1 for p in res5[1][3] if p[5] >= 1) > 0
    arrecife = len(res5[2][3]) == int(c['max_parasitos']) and min(p[1] for p in res5[2][3]) < 0.6
    t.check('colonia sobre la torre-punto: 1, 3 y 6 notas del SEQ1 -> %s parasitos; primero la azotea, '
            'luego bajan por la fachada y al final un arrecife' % '/'.join(str(x[2]) for x in res5),
            [x[1] for x in res5] == [4, 12, 24] and [x[2] for x in res5] == [4, 12, 24] and azotea and bajan
            and arrecife, 'logicos %s' % [x[1] for x in res5])
    base.par.Fijartipo = 'auto'
    c = m.cfg()
    # 6. ciudad espacial: barrio de 4 celdas con 1 y 3 notas del SEQ2
    z4 = [i] + list(m.NEIGH[i])[:3]
    res6 = []
    for notas in (1, 3):
        W = mundo(z4, m.GEO, m.occ_inicio(c, 'informal', 5))         # un barrio denso
        tn = t_unico()
        for x in z4:
            W['t_nac'][x] = tn
        for x in z4:
            for _ in range(notas):
                m.note_on(W, c, m.ARQ, m.cell_note(x), 100, 2.0, 120.0)
            W['occ'][x] = 6
        m.cerrar_obras(W, c)
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, c, ahora)
        inf = m.info_ciudad(W, c, i)
        libres, g, paso_m = m.pilares_marco(inf['ex'], c['modulo_marco'])
        sobre_casa = [p for p in libres if m._dentro(inf['ex'], p[0], p[1], 0.0)]
        caps = len([1 for g_, f in edis(inst) if g_.startswith('mod_edi_capsula')])
        res6.append(((W['marco_vis'][i] + 1) // 2, len(filas(inst, 'ciu_marco')), caps, len(filas(inst, 'ciu_pilar')),
                     sobre_casa))
    t.check('ciudad espacial sobre un barrio de 4 celdas: 1 y 3 notas del SEQ2 -> marco de %d y %d niveles, '
            '%d y %d capsulas, %d pilares; ninguno sobre una casa' % (res6[0][0], res6[1][0], res6[0][2],
                                                                     res6[1][2], res6[1][3]),
            res6[0][0] == 1 and res6[1][0] == 3 and res6[1][1] > res6[0][1] > 0 and res6[1][2] > 0
            and res6[1][3] > 0 and not res6[0][4] and not res6[1][4])
    # 7. torres que se buscan: clusters planificados de 2, 5 y 8 celdas
    def cluster_de(n_celdas, mut=0.5):
        base.par.Mutacion = mut
        cc = m.cfg()
        celdas = [i]
        frente = list(m.NEIGH[i])
        while len(celdas) < n_celdas and frente:
            x = frente.pop(0)
            if x not in celdas and not m.is_pole(x):
                celdas.append(x)
                frente += [y for y in m.NEIGH[x] if y not in celdas]
        W = mundo(celdas, m.ARQ, 8)
        cl = m.clusters(W, cc)
        tf, _ = m.objetivos(W, cc, cl)
        for x in celdas:
            W['et_f'][x] = W['ant_et_f'][x] = tf[x]
            W['mut'][x] = mut
        inst = m.build_instances(W, cc, ahora)
        return W['piel'].get('ciudad', {}).get('protagonistas', {}), len(cl['celdas'].get(cl['de'][i], []))
    p2, p5, p8 = cluster_de(2), cluster_de(5), cluster_de(8)
    p5_0, _ = cluster_de(5, 0.0)
    t.check('torres que se buscan: clusters de %d, %d y %d celdas -> %s, %s y %s; con Mutacion 0, pasarela'
            % (p2[1], p5[1], p8[1], list(p2[0]), list(p5[0]), list(p8[0])),
            list(p2[0]) == ['pasarela'] and list(p5[0]) == ['bucle'] and list(p8[0]) == ['losa']
            and list(p5_0) == ['pasarela'])
    base.par.Mutacion = 0.5
    # 8. mutacion: la misma escena a 0 y a 1; con Mutacionfuente = saturacion la lleva el modular
    def colonia_mut(mut):
        W = mundo([i], m.ARQ, 3)
        W['t_nac'][i] = t_unico()
        for _ in range(6):
            m.note_on(W, c, m.GEO, nota, 100, 2.0, 120.0)
        W['occ'][i] = 3
        m.cerrar_obras(W, c)
        inf = m.info_ciudad(W, c, i)
        pts = m.puestos_colonia(inf['ex'], 24, mut, 0.5, inf['plantas'])
        return max(max(abs(p[3]), abs(p[4])) for p in pts), sum(1 for p in pts if p[5] == 2)
    v0, v1 = colonia_mut(0.0), colonia_mut(1.0)
    cs = dict(c)
    cs.update(mutacion_fuente=1, nivel=19)
    Ws = m.new_world()
    Ws['modular']['saturacion'] = 0.2
    s1 = m.mutacion_actual(Ws, cs)
    Ws['modular']['saturacion'] = 0.9
    s2 = m.mutacion_actual(Ws, cs)
    Wt = mundo([i], m.ARQ, _omax(c))
    Wt['mut'][i] = 0.0
    tor0 = [m.diseno_celda(Wt, dict(c, fijar_tipo=3), i)[0]]
    Wt['mut'][i] = 1.0
    tor1 = [m.diseno_celda(Wt, dict(c, fijar_tipo=3), i)[0]]
    t.check('mutacion: a 0 parasitos pegados (%.2f) y torre recta (%s); a 1 voladizo maximo (%.2f), %d '
            'parasitos colgados de otros y torsionada (%s); la saturacion la lleva (%.1f -> %.1f)'
            % (v0[0], tor0[0], v1[0], v1[1], tor1[0], s1, s2),
            v0[0] <= 0.5 + 1e-9 and v0[1] == 0 and v1[0] > 1.2 and v1[1] > 0 and tor0 == ['prisma']
            and tor1 == ['torsion'] and abs(s1 - 0.2) < 1e-9 and abs(s2 - 0.9) < 1e-9)
    # 9. lectura a distancia: siluetas a 20 px, como la fila inferior de la lamina
    sil = dict((d, m.silueta_edificio(c, d, 0, 20)) for d in m.RASCACIELOS)
    pares = [(p, q, m.iou(sil[p], sil[q])) for k, p in enumerate(m.RASCACIELOS) for q in m.RASCACIELOS[k + 1:]]
    peor = max(pares, key=lambda x: x[2])
    bp = m.iou(m.silueta_edificio(c, 'kowloon', 0, 20, 20), m.silueta_edificio(c, 'podio', 0, 20, 20))
    t.check('a 20 px los cuatro rascacielos se distinguen (el par mas parecido, %s y %s, %.2f) y un barrio '
            'denso no se confunde con un podio (%.2f)' % (peor[0], peor[1], peor[2], bp),
            peor[2] < 0.75 and bp < 0.75)
    # 10. derribo: un aranazo sobre la colonia quita los parasitos de abajo; sobre el marco, las capsulas
    W = mundo([i], m.ARQ, 3)
    W['t_nac'][i] = t_unico()
    for _ in range(6):
        m.note_on(W, c, m.GEO, nota, 100, 2.0, 120.0)
    W['occ'][i] = 3
    m.cerrar_obras(W, c)
    inf = m.info_ciudad(W, c, i)
    todos = m.puestos_colonia(inf['ex'], W['par_vis'][i], inf['mut'], 0.5, inf['plantas'])
    m._quitar_colona(W, i, 3.0)
    tt = 3.0
    for _ in range(12):
        tt += 1.0
        m.ciudad_tick(W, c, tt, 0.5)
    quedan = m.puestos_colonia(inf['ex'], W['par_vis'][i], inf['mut'], 0.5, inf['plantas'])
    abajo = quedan == todos[:len(quedan)] and len(quedan) < len(todos) and \
        min(p[1] for p in todos[len(quedan):]) <= min(p[1] for p in quedan)
    Wm = mundo([i], m.GEO, m.occ_inicio(c, 'informal', 5))
    Wm['t_nac'][i] = t_unico()
    for _ in range(3):
        m.note_on(Wm, c, m.ARQ, nota, 100, 2.0, 120.0)
    Wm['occ'][i] = 6
    m.cerrar_obras(Wm, c)
    u0 = Wm['marco_vis'][i]
    m._quitar_colona(Wm, i, 3.0)
    m.ciudad_tick(Wm, c, 10.0, 0.5)
    u1 = Wm['marco_vis'][i]
    m.ciudad_tick(Wm, c, 11.0, 0.5)
    u2 = Wm['marco_vis'][i]
    t.check('derribo: un golpe sobre la colonia quita los parasitos mas bajos (%d -> %d); sobre el marco, '
            'primero las capsulas (%d -> %d) y despues el nivel (%d)' % (len(todos), len(quedan), u0, u1, u2),
            abajo and u0 == 6 and u1 == 5 and u2 == 4)
    # 11. el derribo de la fase 14: un edificio a medias que recibe un aranazo va hacia atras
    cd_ = dict(c, nivel=14, avance=0)
    Wd = mundo([i], m.ARQ, 3)
    Wd['obra'][i], Wd['t_obra'][i] = 3, 0.0
    m.derribar(Wd, cd_, i, 1.0)
    medio = Wd['obra'][i]
    tt = 1.0
    for _ in range(20):
        tt += cd_['pasos_etapa'] * 0.125 + 0.01
        m.tick_piel(Wd, cd_, tt, 0.125)
    t.check('derribo de un edificio a medias: retrocede un paso (3 -> %d) y sigue hacia atras hasta el solar (%d)'
            % (medio, Wd['obra'][i]), medio == 2 and Wd['obra'][i] == 0 and not Wd['derribo'][i])
    # 12. el tinte del secuenciador en las ventanas: todas a la vez, y se apaga en Pasostinte pasos
    W = mundo([i], m.ARQ, 3)
    W['t_gate'][i], W['lat_s'][i] = ahora, 2
    W['paso'] = 0.125
    f1 = edis(m.build_instances(W, c12, ahora), i)
    f2 = edis(m.build_instances(W, c12, ahora + c['pasos_tinte'] * 0.125 + 0.01), i)
    t1 = f1[0][1][9] if f1 else 0.0
    t2 = f2[0][1][9] if f2 else 9.0
    t.check('tinte de las ventanas: una nota del SEQ2 enciende el edificio con su color (r %.2f) y se apaga '
            'en Pasostinte pasos (%.2f)' % (t1, t2), 2.0 < t1 < 3.0 and t2 == 0.0)
    # 13. la paleta: la misma en el motor y en el shader; sin el azul de los rios ni el cian
    import re
    txt = PIEL_PIXEL[PIEL_PIXEL.index('const vec3 PALETA['):]
    txt = txt[:txt.index(');')]
    nums = [float(x) for x in re.findall(r'[0-9]+\.[0-9]+', txt)]
    mot = [v for lg in m.PALETA_CIUDAD for col in lg for v in col]
    frios = [col for lg in m.PALETA_CIUDAD for col in lg if col[2] > col[0] + 0.08 and col[2] > col[1] - 0.02]
    t.check('la paleta de la ciudad, la misma en el motor y en el shader (%d colores), sin azules ni cianes'
            % (len(mot) // 3), nums == mot and not frios, 'frios %s' % frios)
    # 14. de lejos (Lodciudad) se apagan los remates pequenos; la silueta se queda
    W = mundo([i], m.GEO, 2)
    cl_ = dict(c)
    cl_['lod_ciudad'] = 0.0
    ce_ = m.build_instances(W, cl_, ahora)
    cl_['lod_ciudad'] = 1e9
    le_ = m.build_instances(W, cl_, ahora)
    t.check('Lodciudad: de cerca, varillas y escalera (%d); de lejos, no (%d), y el edificio sigue'
            % (len(filas(ce_, 'ciu_varillas')) + len(filas(ce_, 'ciu_escalera')),
               len(filas(le_, 'ciu_varillas')) + len(filas(le_, 'ciu_escalera'))),
            filas(ce_, 'ciu_varillas') and not filas(le_, 'ciu_varillas') and not filas(le_, 'ciu_escalera')
            and edis(le_, i))
    # 15. fase 15 y 16: el registro guarda la tipologia; los cortes ensenan sus cimientos
    W = mundo([i, m.NEIGH[i][0]], m.ARQ, 1)
    W['occ'][m.NEIGH[i][0]] = 3
    reg = m.registro_concha(W, dict(c, nivel=15))
    sh = dict(tema='ciudad', tipo=['pilotis', 'podio', 'laje'] + [''] * (m.N - 3))
    t.check('registro de la concha con la tipologia de cada celda (%s); cimientos: pilotes, sotano y zapatas'
            % reg['tipo'][i], reg['tipo'][i] in m.DISENOS_TIPO['pabellon']
            and [m.cimiento_de(sh, k, 'planificada') for k in range(3)] == ['arq_pilotes', 'arq_sotano',
                                                                             'arq_cimientos'])
    # 16. la leyenda CIUDAD, OBRA, COLONIA y MARCO
    m.reset_world()
    Wl = m.world()
    for x, v in ((i, m.ARQ), (m.NEIGH[i][0], m.GEO)):
        Wl['occ'][x], Wl['own'][x], Wl['sp'][x], Wl['vel'][x] = 3 if v == m.ARQ else 6, v, m.HIB, 100
        Wl['h'][x] = Wl['vh'][x] = m.height_for(m.cfg(), Wl['occ'][x])
        Wl['t_nac'][x] = -50.0
    Wl['par_vis'][i] = 8
    Wl['marco_vis'][m.NEIGH[i][0]] = 3
    Wl['obra'] = [0] * m.N
    m.build_instances(Wl, m.cfg(), absTime.seconds + 10.0)
    ley = m.legend()
    t.check('leyenda CIUDAD (lenguajes F/T/C, edificios, tipos, MUTACION), COLONIA y MARCO',
            'CIUDAD   lenguajes F/T/C' in ley and 'MUTACION 0,50 (manual)' in ley and 'COLONIA  celda' in ley
            and 'MARCO' in ley, ' '.join([l.strip() for l in ley.split('\n') if 'CIUDAD' in l][:1]))
    Wl['edi'] = [-1] * m.N
    m.tick(Wl, m.cfg(), absTime.seconds + 10.0, 120.0, True)
    m.build_instances(Wl, m.cfg(), absTime.seconds + 10.0)
    ley = m.legend()
    t.check('leyenda OBRA (pasos y gruas)', 'OBRA     ' in ley and 'gruas' in ley,
            ' '.join([l.strip() for l in ley.split('\n') if 'OBRA' in l][:1]))
    # 17. rendimiento: las 85 celdas en ciudad a ocupacion maxima frente a la naturaleza
    tiempos = {}
    for tema in ('naturaleza', 'ciudad'):
        base.par.Tema = tema
        cc = m.cfg()
        W = mundo(range(m.N), m.GEO, 14, cerrar=False)
        for x in range(0, m.N, 3):
            W['own'][x] = W['sp'][x] = m.ARQ
        m.cerrar_obras(W, cc)
        m.build_instances(W, cc, absTime.seconds + 10.0)
        m.build_instances(W, cc, absTime.seconds + 10.0)
        ts = []
        for _ in range(5):
            t0 = time.time()
            m.build_instances(W, cc, absTime.seconds + 10.0)
            ts.append(time.time() - t0)
        tiempos[tema] = min(ts)
    base.par.Tema = 'ciudad'
    # solo se informa: el tiempo depende de la maquina y de lo que haga en ese momento
    t.check('rendimiento: %d celdas a ocupacion maxima, ciudad %.1f ms por calculo, naturaleza %.1f ms '
            '(solo se informa)' % (m.N, 1000 * tiempos['ciudad'], 1000 * tiempos['naturaleza']),
            tiempos['ciudad'] > 0.0 and tiempos['naturaleza'] > 0.0)


def _prueba_industria(t, m):
    """Las pruebas del tema industria (v11)."""
    guarda = {}
    for nm in ('Tema', 'Epoca', 'Recursos', 'Mutacion', 'Fijartipo', 'Avance', 'Emisiones'):
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    try:
        _prueba_industria_(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass


def _prueba_industria_(t, m):
    import time
    base.par.Tema = 'industria'
    base.par.Epoca = 'eras'
    base.par.Recursos = True
    base.par.Fijartipo = 'auto'
    base.par.Mutacion = 0.5
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    c = m.cfg()
    c12 = dict(c, nivel=max(12, c['nivel']), respaldo=0)
    ahora = absTime.seconds + 10.0
    unico = [500.0]

    def t_unico():
        unico[0] += 1.0
        return unico[0]

    def mundo(celdas, own, occ, vel=100, cerrar=True, cc=None):
        W = m.new_world()
        for x in celdas:
            W['occ'][x], W['own'][x], W['sp'][x], W['vel'][x] = occ, own, own, vel
            W['h'][x] = W['vh'][x] = m.height_for(m.cfg(), occ)
            W['t_nac'][x] = -50.0
        if cerrar:
            m.cerrar_obras(W, cc or m.cfg())
        return W

    def edis(inst, celda=None, pref='mod_edi_'):
        out = []
        for g, fs in inst.items():
            if g.startswith(pref):
                for f in fs:
                    if celda is None or max(range(m.N), key=lambda x: sum(f[q] * m.NORMALS[x][q]
                                                                          for q in range(3))) == celda:
                        out.append((g, f))
        return out

    def filas(inst, g):
        return inst.get(m.geometria_de(g), [])

    def humo(inst, cols=None, celda=None):
        cols = cols or list(m.COL_HUMO.values())
        return [f for f in inst.get('humo', []) if tuple(round(v, 3) for v in f[9:12])     # motor v74
                in [tuple(round(v, 3) for v in col) for col in cols]
                and (celda is None or max(range(m.N), key=lambda x: sum(f[q] * m.NORMALS[x][q]
                                                                        for q in range(3))) == celda)]

    # 0. la biblioteca: ninguna pieza desnuda (celosia, bandas, colada, penacho, llama o remate)
    desnudas = []
    for d in m.DISENOS_IND:
        ex = m.edificio(c, d, 0)
        rasgo = any(v['fach'] in (m.F_CELOSIA, m.F_BANDAS, m.F_INCANDESCENTE, m.F_RETICULA, m.F_SIERRA)
                    for v in ex['vols']) or ex['fuentes'] or ex['rem']
        if not rasgo:
            desnudas.append(d)
    t.check('biblioteca de la industria: %d disenos x %d variantes; ninguna pieza desnuda'
            % (len(m.DISENOS_IND), m.variantes_ind(c)), not desnudas and len(m.DISENOS_IND) >= 18,
            'desnudas: %s' % desnudas)
    # 1. escalera de la mina: 1 a 9
    serie = []
    for o in range(1, _omax(c) + 1):
        W = mundo([i], m.GEO, o)
        inf = m.info_ciudad(W, c, i)
        inst = m.build_instances(W, c, ahora)
        serie.append((o, inf['tipo'], inf['diseno'], len(edis(inst, i))))
    esperado = [m.TIPOS['mina'][m.etapa_ciudad(c, 'mina', o) - 1] for o in range(1, _omax(c) + 1)]
    t.check('escalera de la mina 1 -> %d: %s' % (_omax(c), ' / '.join('%d %s' % (o, d) for o, _, d, _ in serie)),
            [x[1] for x in serie] == esperado and set(esperado) == set(m.TIPOS['mina'])
            and all(x[3] >= 1 for x in serie), 'tipos %s' % [x[1] for x in serie])
    # 2. escalera de la energia, con la obra: chimenea deslizante, torre por anillos y primer humo
    serie = [(o, m.info_ciudad(mundo([i], m.ARQ, o), c, i)['tipo']) for o in range(1, _omax(c) + 1)]
    esperado = [m.TIPOS['energia'][m.etapa_ciudad(c, 'energia', o) - 1] for o in range(1, _omax(c) + 1)]
    cg = dict(c12, avance=0)
    Wo = m.new_world()
    k = 0
    while m.etapa_ciudad(cg, 'energia', Wo['occ'][i]) < 5 and k < 400:      # hasta la central
        m.note_on(Wo, cg, m.ARQ, nota, 100, 100.0 + 0.01 * k, 120.0)
        k += 1
    for x in range(m.N):                    # sin los satelites del desborde (humean por su cuenta)
        if x != i:
            Wo['occ'][x] = Wo['own'][x] = Wo['sp'][x] = 0
            Wo['h'][x] = Wo['vh'][x] = 0.0
    pasos_ = m.pasos_obra('energia', 'central')
    vistas, encofrado, humo_obra, humo_fin = [], 0, 0, 0
    for q in range(len(pasos_) + 1):
        Wo['vh'] = list(Wo['h'])
        tq = 120.0 + q
        inst = m.build_instances(Wo, cg, tq + 5.0)
        vistas.append(m.obras_ciudad(Wo, cg).get(i, 'terminada'))
        if filas(inst, 'ciu_encofrado'):
            encofrado += 1
        if vistas[-1] != 'terminada':
            humo_obra += len(humo(inst, celda=i))
        else:
            humo_fin = len(humo(inst, celda=i))
        # el gate de una nota (Avance = gates), sin subir la ocupacion: con otros
        # umbrales, las notas llevarian la central a la coronacion a mitad de obra
        m.gate_piel(Wo, cg, i, tq)
    t.check('escalera de la energia 1 -> %d: %s; la obra: %s (encofrado %d, humo en obra %d, al terminar %d)'
            % (_omax(c), ' / '.join('%d %s' % s_ for s_ in serie), ' -> '.join(vistas), encofrado, humo_obra, humo_fin),
            [x[1] for x in serie] == esperado and set(esperado) == set(m.TIPOS['energia'])
            and vistas[:len(pasos_)] == pasos_ and vistas[-1] == 'terminada'
            and encofrado >= 1 and humo_obra == 0 and humo_fin > 0)
    # 3. recurso: la concha de abajo (naturaleza: carbon; ciudad: chatarra)
    res3 = []
    base.par.Fijartipo = '1'                # el castillete, con su terril
    for tema, rec in (('naturaleza', 'carbon'), ('ciudad', 'chatarra'), (None, 'mineral')):
        W = mundo([i], m.GEO, 3)
        if tema:
            W['shells'] = [dict(tema=tema, esp=[0] * m.N)]
            W['cols'][i] = [[0, 0.5]]
        inst = m.build_instances(W, m.cfg(), ahora, tiles=False)
        terril = [f for f in filas(inst, 'ciu_terril')]
        res3.append((m.recurso_celda(W, c, i), terril and tuple(terril[0][9:12]) == m.COL_RECURSO[rec]))
    base.par.Fijartipo = 'auto'
    t.check('recurso: sobre naturaleza carbon, sobre ciudad chatarra, sin concha mineral (%s); terriles de su color'
            % ', '.join(r for r, _ in res3), [r for r, _ in res3] == ['carbon', 'chatarra', 'mineral']
            and all(ok_ for _, ok_ in res3))
    # 4. epoca: por las eras (vapor, acero, quimica) y fija en directo
    eps = []
    for gen in (0, 3, 6):
        W = mundo([i], m.ARQ, 4, cerrar=False)
        W['gen'] = gen
        m.cerrar_obras(W, c)
        eps.append(m.info_ciudad(W, c, i)['epoca'])
    t.check('epoca por las eras enterradas: 0 -> vapor, 3 -> acero, 6 -> quimica (%s)' % eps, eps == [0, 1, 2])
    # 5. corta que devora: fabrica y 1, 3 y 5 notas del SEQ1
    o_fab = m.occ_inicio(c, 'energia', 3)
    o_com = m.occ_inicio(c, 'mina', 3)
    res5 = []
    for notas in (1, 3, 5):
        W = mundo([i], m.ARQ, o_fab)            # una fabrica
        W['t_nac'][i] = t_unico()
        cols0 = [list(map(list, x)) for x in W['cols']]
        for _ in range(notas):
            m.note_on(W, c, m.GEO, nota, 100, 2.0, 120.0)
        W['occ'][i] = o_fab
        m.cerrar_obras(W, c)
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, c, ahora)
        planta = [g for g, _ in edis(inst, i) if g.startswith('mod_edi_papelera')]
        res5.append((W['par_vis'][i], len(filas(inst, 'ciu_anillo')), bool(planta),
                     len([g for g, _ in edis(inst, i) if 'calderas' in g]),
                     len([g for g, _ in edis(inst, i) if 'chimenea' in g]), len(filas(inst, 'ciu_agua')),
                     [list(map(list, x)) for x in W['cols']] == cols0))
    t.check('corta sobre una fabrica: 1, 3 y 5 notas del SEQ1 -> %s bancos; se come las naves, luego las calderas; '
            'queda la chimenea de testigo; agua acida desde 4; ninguna concha cortada'
            % '/'.join(str(x[0]) for x in res5),
            [x[0] for x in res5] == [1, 3, 5] and [x[1] for x in res5] == [1, 3, 5] and not any(x[2] for x in res5)
            and res5[0][3] == 1 and res5[2][3] == 0 and all(x[4] == 1 for x in res5) and res5[2][5] == 1
            and res5[0][5] == 0 and all(x[6] for x in res5), str(res5))
    # 6. planta integrada: complejo minero y 1 y 3 notas del SEQ2
    res6 = []
    for notas in (1, 3):
        W = mundo([i], m.GEO, o_com)            # un complejo minero
        W['t_nac'][i] = t_unico()
        for _ in range(notas):
            m.note_on(W, c, m.ARQ, nota, 100, 2.0, 120.0)
        W['occ'][i] = o_com
        m.cerrar_obras(W, c)
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, c, ahora)
        inf = m.info_ciudad(W, c, i)
        cast = max(v['y1'] for v in inf['ex']['vols'] if v['rol'] == 'castillete')
        res6.append(((W['marco_vis'][i] + 1) // 2, len(filas(inst, 'ciu_bastidor')), cast > 0.5 + 1e-6,
                     len([g for g, _ in edis(inst, i) if 'chimenea' in g])))
    t.check('planta integrada sobre un complejo minero: 1 y 3 notas del SEQ2 -> bastidor de %d y %d niveles; los '
            'castilletes lo atraviesan; la chimenea corona desde el segundo nivel' % (res6[0][0], res6[1][0]),
            res6[0][0] == 1 and res6[1][0] == 3 and res6[1][1] == 3 * res6[0][1] > 0 and all(x[2] for x in res6)
            and res6[0][3] == 0 and res6[1][3] == 1, str(res6))
    # 7. torres que se alinean: clusters de energia de 2, 5 y 8 celdas
    def cluster_de(n_celdas):
        celdas = [i]
        frente = list(m.NEIGH[i])
        while len(celdas) < n_celdas and frente:
            x = frente.pop(0)
            if x not in celdas and not m.is_pole(x):
                celdas.append(x)
                frente += [y for y in m.NEIGH[x] if y not in celdas]
        W = mundo(celdas, m.ARQ, 7)
        cl = m.clusters(W, c)
        tf, _ = m.objetivos(W, c, cl)
        for x in celdas:
            W['et_f'][x] = W['ant_et_f'][x] = tf[x]
            W['mut'][x] = 0.5
        m.build_instances(W, c, ahora)
        return list(W['piel'].get('ciudad', {}).get('protagonistas', {}))
    p2, p5, p8 = cluster_de(2), cluster_de(5), cluster_de(8)
    t.check('torres que se alinean: clusters de 2, 5 y 8 celdas -> %s, %s y %s' % (p2, p5, p8),
            p2 == ['torre compartida'] and p5 == ['fila de torres'] and p8 == ['anillo de torres'])
    # 8. tinte: una nota sobre una planta suelta una bocanada del color de su secuenciador
    W = mundo([i], m.ARQ, int(c['th_fusion']) - 1)      # la termica (6 con los umbrales de fabrica)
    W['t_gate'][i], W['lat_s'][i] = ahora, 2
    W['paso'] = 0.125
    inst = m.build_instances(W, c, ahora)
    sq = m.seq_color(c, 2)
    tenidas = [f for f in inst.get('humo', []) if abs(f[9] - m.COL_HUMO['negro'][0]) > 0.05
               and abs(f[9] - m.COL_HUMO['gris'][0]) > 0.05 and abs(f[9] - m.COL_HUMO['blanco'][0]) > 0.02
               and f[9] > f[11]]
    t.check('tinte: una nota del SEQ2 sobre una central termica suelta una bocanada de su color (%d particulas)'
            % len(tenidas), tenidas and sq[0] > sq[2])
    # 9. partes moviles al tempo: el balancin cabecea
    W = mundo([i], m.GEO, 2)
    base.par.Fijartipo = '2'
    cm = m.cfg()
    W['pulso']['beat'] = 0.0
    r1 = [tuple(f[3:6]) for f in filas(m.build_instances(W, cm, 100.0), 'ciu_balancin')]
    W['pulso']['beat'] = 0.25               # desde la fase 17, el pulso (master_beat)
    r2 = [tuple(f[3:6]) for f in filas(m.build_instances(W, cm, 100.31), 'ciu_balancin')]
    base.par.Fijartipo = 'auto'
    t.check('partes moviles: los balancines cabecean al tempo (%d)' % len(r1), r1 and r1 != r2)
    # 10. lectura a distancia: la industria frente a la ciudad, a 20 px
    ind_ = m.silueta_edificio(c, 'central', 0, 20, 30)
    peor = max(m.iou(ind_, m.silueta_edificio(c, d, 0, 20, 30)) for d in ('prisma', 'deco', 'podio', 'tubos'))
    blanca = m.PALETA_CIUDAD[m.PALETA_IND + 1][3]
    brillo = any(v['fach'] == m.F_INCANDESCENTE for v in m.edificio(c, 'altohorno', 0)['vols'])
    t.check('a 20 px la central se distingue de la ciudad (el mas parecido, %.2f): torres blancas (%.2f), humo y '
            'brillo naranja de la colada' % (peor, min(blanca)), peor < 0.75 and min(blanca) > 0.7 and brillo
            and m.edificio(c, 'central', 0)['fuentes'])
    # 10b. el violeta de la red, reservado: fuera de la paleta de conchas (y de la industria)
    tonos = [m.palette_hue(n, c['paleta_tono'], m.bandas_de(c)) for n in range(200)]
    t.check('el violeta de la red queda fuera de la paleta de conchas (%d generaciones) y de la industria'
            % len(tonos), not any(m.BANDA_RED[0] <= h < m.BANDA_RED[1] for h in tonos)
            and all(col[2] <= max(col[0], col[1]) + 0.02 for fila in m.PALETA_CIUDAD[m.PALETA_IND:] for col in fila))
    # 11. leyenda INDUSTRIA
    m.reset_world()
    Wl = m.world()
    for x, v, o in ((i, m.GEO, 4), (m.NEIGH[i][0], m.ARQ, 8), (m.NEIGH[i][1], m.ARQ, 4)):
        Wl['occ'][x], Wl['own'][x], Wl['sp'][x], Wl['vel'][x] = o, v, v, 100
        Wl['h'][x] = Wl['vh'][x] = m.height_for(m.cfg(), o)
        Wl['t_nac'][x] = -50.0
    Wl['sp'][m.NEIGH[i][1]] = m.HIB
    Wl['par_vis'][m.NEIGH[i][1]] = 4
    m.cerrar_obras(Wl, m.cfg())
    Wl['par_vis'][m.NEIGH[i][1]] = 4
    m.build_instances(Wl, m.cfg(), absTime.seconds + 10.0)
    ley = m.legend()
    t.check('leyenda INDUSTRIA (epoca, recursos, plantas, humo) y CORTA',
            'INDUSTRIA  época vapor   recursos' in ley and 'humo' in ley and 'CORTA    celda' in ley,
            ' '.join(l.strip() for l in ley.split('\n') if 'INDUSTRIA' in l or 'CORTA' in l))
    # 12. rendimiento: las 85 celdas al maximo con el humo en Maxhumo, frente a la ciudad
    tiempos = {}
    for tema in ('ciudad', 'industria'):
        base.par.Tema = tema
        cc = m.cfg()
        W = mundo(range(m.N), m.GEO, 14, cerrar=False)
        for x in range(0, m.N, 3):
            W['own'][x] = W['sp'][x] = m.ARQ
        m.cerrar_obras(W, cc)
        m.build_instances(W, cc, absTime.seconds + 10.0)
        ts = []
        for _ in range(9):
            t0 = time.time()
            m.build_instances(W, cc, absTime.seconds + 10.0)
            ts.append(time.time() - t0)
        tiempos[tema] = min(ts)
        if tema == 'industria':
            nh = W['piel'].get('ciudad', {}).get('humo', 0)
    base.par.Tema = 'industria'
    t.check('rendimiento: %d celdas al maximo, humo %d de %d (Maxhumo); industria %.1f ms por calculo, '
            'ciudad %.1f ms (solo se informa)'
            % (m.N, nh, int(c['max_humo']), 1000 * tiempos['industria'], 1000 * tiempos['ciudad']),
            nh <= int(c['max_humo']))


def _prueba_mallas_sin_cfg(t, m):
    """comun v73 (motor v93): las mallas de la biblioteca no leen cfg() entero."""
    leidos = []
    p0 = m._p

    def espia(nombre, defecto):
        leidos.append(nombre)
        return p0(nombre, defecto)

    m._p = espia
    try:
        cm = m.cfg_malla()
        de_malla = set(leidos)
        del leidos[:]
        c = m.cfg()
        de_cfg = set(leidos)
    finally:
        m._p = p0
    con_expr = sorted(n for n in de_cfg if getattr(getattr(base.par, n, None), 'expr', ''))
    t.check('las mallas de la biblioteca leen 3 parametros (cfg() lee %d, y %s cambia en cada fotograma)'
            % (len(de_cfg), ', '.join(con_expr) or 'ninguno'),
            de_malla == set(('Oblicuidad', 'Retranqueo', 'Torsionmax')) and not (de_malla & set(con_expr)),
            ', '.join(sorted(de_malla)))
    t.check('cfg_malla da las mismas mallas que cfg()',
            m._clave_biblio(cm) == m._clave_biblio(c) and m._clave_ciudad(cm) == m._clave_ciudad(c))
    cb = base.op('modelos').op('ejemplar_callbacks')
    t.check('el callback de las mallas pide cfg_malla (y ejemplares_al_dia lo repone en un proyecto de antes)',
            'cfg_malla()' in cb.text and not ejemplares_al_dia(base))


def _prueba_rendimiento_td(t, m):
    """v12 (comun v49, motor v69): lo que se calcula una vez por fotograma y lo que
    no se dibuja."""
    _prueba_mallas_sin_cfg(t, m)
    tema0 = str(base.par.Tema.eval())
    fu = base.op('frame_u')
    try:
        if fu is not None:
            fu.cook(force=True)
        # comun v52: gira solo 'planeta'; las geometrias, sus hijas, no leen el giro
        con_giro, sueltas = [], []
        for g in [o for o in base.children if o.name.startswith(PIEL_PREFIJO)]:
            for nm in ('rx', 'ry'):
                if (getattr(g.par, nm).expr or ''):
                    con_giro.append('%s.%s' % (g.name, nm))
            if not gira_con_planeta(g):
                sueltas.append(g.name)
        canales = [ch.name for ch in getattr(fu, '_chans', [])] if fu is not None else []
        t.check('el giro y el balanceo, una vez por fotograma en frame_u y solo en planeta: las geometrias '
                'son sus hijas y no leen el giro (%d canales en frame_u)' % len(canales),
                fu is not None and fu['ry'] is not None and fu['rx'] is not None and not con_giro and not sueltas,
                ', '.join((con_giro + sueltas)[:3]))
        # motor v75: cada geometria instanciada tiene su Script CHOP en chop_names (el
        # motor solo recuece esos: el humo de la v74 no estaba y no se habria actualizado)
        nombres = set(m.chop_names(m.cfg()))
        sin_cocer = []
        for g in base.children:
            try:
                iop = str(g.par.instanceop.eval() or '') if g.OPType == 'geometryCOMP' else ''
            except Exception:
                iop = ''
            iop = iop.split('/')[-1]
            if iop.startswith('i_') and base.op(iop) is not None and iop not in nombres:
                sin_cocer.append(iop)
        t.check('cada geometria instanciada tiene su Script CHOP en chop_names (humo y vagones incluidos)',
                not sin_cocer and 'i_humo' in nombres and 'i_vagones' in nombres, ', '.join(sin_cocer[:4]))
        pa = base.op('particulas')
        t.check('particulas: motas suaves (una lamina con mat_motas) y los trenes en cajas (vagones)',
                pa is not None and pa.op('lamina') is not None and 'mat_motas' in (pa.par.material.expr or '')
                and base.op('vagones') is not None and base.op('mat_motas') is not None)
        t.check('la luz de destello lee sus 7 valores de frame_u (sin Python)',
                base.op('luz_destello') is None or ("frame_u')['fl_tx']" in (base.op('luz_destello').par.tx.expr or '')
                                                    and fu['fl_dim'] is not None))
        res = []
        for tema in m.TEMAS:
            base.par.Tema = tema
            c = m.cfg()
            m._CACHE.pop('render_tema', None)
            m.render_tema_al_dia(c)
            geos = [g for g in str(base.op('render').par.geometry.val).split() if g.startswith('mod_')]
            mods = dict((g, mo) for g, mo, _ in m.geometrias_piel(c))
            ajenas = [g for g in geos if m.tema_de(c) not in m.temas_de_modelo(mods.get(g, ''))]
            res.append((tema, len(geos), len(mods), ajenas))
        t.check('el render solo dibuja las geometrias del tema activo (%s)'
                % ', '.join('%s %d de %d' % (a, b, n) for a, b, n, _ in res),
                all(not x[3] and 0 < x[1] < x[2] for x in res), str([x[3][:2] for x in res]))
    finally:
        base.par.Tema = tema0
        m._CACHE.pop('render_tema', None)
        m.render_tema_al_dia(m.cfg())


run_test(base, prueba)
print('  Ahora: Sembrarzona dos veces (pagina Fase11) y mira el cluster, sus')
print('  puentes y la pieza protagonista. Cambia Tema y repite.')
print('  Con el SEQ1 y el SEQ2 sonando: las obras avanzan con los gates')
print('  (Avance = gates); sin notas en el cluster se quedan a medias.')
print('=' * 66)
