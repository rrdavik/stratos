# Estratos · Propuesta: vista inmersiva a ras de suelo

*Análisis de la petición «un nuevo punto de vista inmersivo, darle una vuelta al de acercamiento a la superficie, con alguna vista de cerca con gran angular». 12 de noviembre de 2026, sobre `main` en `motor v91`. **No implementa nada**: es el análisis y una propuesta para aprobar antes de pasar a código.*

> **Paso 1 implementado (12 de noviembre de 2026):** `motor v92`, `comun v72`, `fase10 v12`. Qué hay y qué probar, en el apartado 8.
>
> **Decisiones cerradas el 12 de noviembre de 2026** (apartado 7): modo nuevo, en la fase 10, cielo negro, para proyector y pantalla, y recorrido por el pasillo entre anillos.

## En dos líneas

La cámara de superficie de hoy no es inmersiva porque **vuela a más del doble de la altura de lo que mira, en picado y con teleobjetivo**. La propuesta es un tercer modo de cámara, **rasante**: a la altura de una semilla, con gran angular (90°), mirando un poco hacia arriba y **anclada al planeta**, recorriendo el pasillo que queda entre dos anillos de celdas.

Antes de escribir código hay una prueba de cinco minutos con los parámetros que ya existen (apartado 6, paso 0) que dice si la piel aguanta vista de cerca.

---

## 1. Lo que hay hoy

La cámara la calcula `camera_state()` en `estratos_motor.py` (línea 14934) y la monta `fase10_direccion.py`. Tiene dos modos (`Modocamara`):

| Modo | Qué hace |
|---|---|
| `globo` | Fija en +Z, mira al centro. El planeta ocupa `Encuadre` del cuadro; solo retrocede cuando una concha nueva lo engorda (`Camsuave`). |
| `superficie` | Órbita a `Camaltura` (4) sobre el radio nominal, a `Camvel` (0,6°/s), a una latitud que oscila entre 4° y 20°. Mira a un punto de la superficie 25° por delante y 6° más abajo. Transición de 20 s desde el globo. |

El FOV no lo gobierna el motor: `_cam_optics()` lo **lee** del Camera COMP (45° horizontal por defecto) y con él calcula el encuadre del globo.

### La vista de superficie, en cifras

Con los valores por defecto (núcleo 6, corteza hasta 4, límite de altura 1,875, semilla 0,375):

| Radio del planeta | Altura de cámara | Picado bajo la horizontal | Horizonte | Distancia al objetivo | Celda (E-O × N-S) |
|---|---|---|---|---|---|
| 6 | 4 | 61° | a 53° bajo la horizontal | 5,3 | 3,1 × 2,5 |
| 8 | 4 | 54° | a 48° | 5,9 | 4,2 × 3,4 |
| 10 | 4 | 49° | a 44° | 6,6 | 5,2 × 4,2 |

FOV vertical con 45° horizontal en 16:9: **26°**.

## 2. Por qué no resulta inmersiva

1. **Está por encima de todo.** A 4 de altura, la cámara vuela a más del doble de una formación en el límite (1,875). Solo las coronas más largas (hasta 5,8) la alcanzan.
2. **Mira hacia abajo, no al horizonte.** El picado es de 49° a 61°. El horizonte queda en el cuarto superior del cuadro y el resto es suelo visto desde arriba: es una vista de satélite bajo, no de alguien que está allí.
3. **Es un teleobjetivo.** 26° de FOV vertical aplana la profundidad. La sensación de estar dentro la dan el gran angular (las verticales que fugan, lo cercano enorme) y la altura de ojos baja.
4. **No sabe dónde está el suelo.** Usa el radio nominal, no el suelo de la celda que tiene debajo (hondonadas, cortes, escisiones), ni esquiva nada. A 4 de altura no importa; a ras de suelo sí.
5. **Flota en el espacio del mundo.** El planeta gira e inclina el eje (`Balanceo`, hasta 60°) por debajo de una cámara que no gira con él. De lejos se lee como órbita; de cerca, el terreno pasaría barriendo y las formaciones atravesarían la cámara.
6. **La niebla no la sigue.** `niebla()` calcula dónde empieza con la distancia de la cámara de **globo** (`cs['d']`), también en modo superficie: de cerca, la bruma de distancia (fase 19) empieza mucho más allá de lo que se ve. Y es justo lo que da escala a una vista cercana.

## 3. Qué significa «de cerca con gran angular» en este planeta

El planeta es pequeño, y eso define la imagen más que cualquier parámetro:

- Con el ojo a 0,35 sobre un planeta de radio 8, **el horizonte del suelo está a 2,4 unidades: menos de una celda**. La curvatura se ve siempre.
- Una formación en el límite asoma sobre el horizonte hasta unas 8 unidades (dos celdas); una corona larga, hasta 13 (tres celdas).
- Es decir: se ve la celda propia, las vecinas enteras y las puntas de las de más allá saliendo de detrás de la curva. No hay «paisaje lejano»: hay un horizonte muy próximo del que emergen cosas altas.

Gran angular, en FOV horizontal de TouchDesigner (16:9):

| FOV horizontal | FOV vertical | Carácter |
|---|---|---|
| 45° (hoy) | 26° | teleobjetivo corto |
| 75° | 47° | angular moderado |
| **90°** | **59°** | gran angular; recomendado de partida |
| 100° | 68° | muy angular, los bordes ya estiran |
| 110° | 78° | extremo; deformación evidente en las esquinas |

Más allá de ~110° una proyección rectilínea ya no sirve y haría falta ojo de pez, que pide renderizar un cubemap y reproyectarlo. Es la misma infraestructura que el mapa equirectangular 2:1 que pide la esfera real y que sigue pendiente (`MONTAJE_FASES_21_23.md`, «Lo que la maqueta no es»). Queda fuera de esta propuesta, pero conviene saber que las dos cosas comparten solución.

## 4. Propuesta: modo `rasante`

Un tercer valor de `Modocamara`. `globo` y `superficie` no se tocan.

### 4.1 Dónde está y adónde mira

- **Altura:** `Rasaltura` (0,35 por defecto: la de una semilla) sobre el **suelo real** de las celdas que tiene al lado (`suelo(W, cfg, i)`), no sobre el radio nominal. Suavizada, para que un corte o un escalón entre celdas no dé un salto.
- **Mirada:** hacia delante en el sentido de la marcha y `Rasmirada` (+8°) **por encima** de la horizontal. El horizonte cae en el tercio inferior y las formaciones se alzan sobre la cámara: bajo, angular y contrapicado es lo que da monumentalidad.
- **FOV:** `Rasfov` (90°), gobernado por el motor.

### 4.2 Anclada al planeta

La cámara se define en coordenadas del planeta y se lleva al mundo con el mismo giro que las geometrías (giro, `Tilt`, balanceo). Consecuencias:

- El recorrido se decide respecto al terreno: se puede saber qué celda hay debajo y qué hay alrededor.
- El horizonte queda nivelado aunque el eje se balancee.
- **Las luces no giran con el planeta** (la cenital está fija sobre el polo del mundo), así que desde el suelo la luz cambia sola con el giro y el balanceo: un «día» gratis, sin tocar la iluminación.

### 4.3 Por dónde va

Tres rutas posibles:

| Ruta | Qué es | Valoración |
|---|---|---|
| **Paralelo** | Avanza despacio (`Rasvel`) por el límite entre dos anillos de celdas: un círculo continuo con formaciones a ambos lados, como una calle o un valle. | **La de la primera versión (decidido).** Determinista, sin azar, y lejos del centro de las celdas. |
| Acción | Viaja hacia la celda de la última nota (`W['ev']['ultima']`) y se queda mirándola crecer. | La más musical. Segunda versión: necesita una ruta entre celdas y decidir qué hace con notas rápidas. |
| Trípode | Quieta en un punto; el mundo cambia delante. | Trivial una vez hecho el paralelo (`Rasvel` 0). |

El paralelo se elige con `Rasanillo` (entre qué anillos) o deriva solo de uno a otro muy despacio.

**Comprobado al implementar (12 de noviembre):** en la **naturaleza** el pasillo existe: los árboles quedan a los lados y asoman sobre el horizonte. En la **ciudad no**: la planta de un edificio ocupa la celda entera (su escala es el ancho de la celda), así que el límite entre anillos es un callejón sin anchura y la cámara queda pegada a las fachadas o dentro de alguna estructura. La primera versión no esquiva nada: lo que quede a menos del plano cercano se recorta. Es lo primero que hay que mirar en TouchDesigner y lo que decide el siguiente paso (subir la altura en la ciudad, apartar la cámara de lo que tenga delante o dar aire entre anillos).

### 4.4 Lo que hay que cambiar

| Dónde | Cambio |
|---|---|
| `camera_state()` | El tercer modo, con su peso de transición; posición en coordenadas del planeta llevada al mundo; altura sobre el suelo local; `near` y `far` medidos desde el suelo real y no desde `Re`. |
| FOV | Hoy el motor lo lee del Camera COMP y la cámara no lo recibe del motor. Hay que invertirlo: el FOV del globo pasa a un parámetro (`Camfov`, con el valor que tenga hoy la cámara), el motor entrega el FOV mezclado (`cam('fov')`) y `_cam_optics()` lee el parámetro. Si no, el encuadre del globo se calcularía con el FOV del rasante. |
| Orientación | El *Look At* del Camera COMP usa un vector arriba fijo; una cámara que recorre el planeta necesita que arriba sea la vertical local. O se le da un vector arriba desde el motor o el motor entrega el giro completo y se quita el *Look At*. **Hay que mirarlo en TouchDesigner**: no sé desde aquí qué admite el Camera COMP de la versión instalada. |
| `niebla()` / `niebla_camara()` | En rasante, la bruma empieza a media celda y es total poco más allá de lo que asoma sobre el horizonte. Con el cielo negro (decidido), en este modo la bruma funde hacia negro y no hacia `NIEBLA_COL`: lo lejano se apaga contra el cielo en vez de quedar más claro que él. Propongo además una cantidad mínima propia (`Rasbruma`) aunque el modular no mande espacialidad: sin perspectiva aérea no hay escala. |
| LOD (`lod_cerca`, `lod_ciudad`) | Hoy `superficie` pone **todas** las celdas en detalle alto. En rasante solo se ven la celda propia y dos anillos de vecinas: detalle alto para esas (por `NEIGH`) y el lejano para el resto. Primera versión: la bandera de hoy, y medir. |
| Retícula, leyenda, diagnóstico | La retícula asoma 0,2 sobre el suelo y la cámara iría a 0,35: hay que ocultarla en este modo, como hace `Modoactuacion`. |
| `fase10_direccion.py` | El valor nuevo del menú, los parámetros `Ras…` y `Camfov`, la expresión del FOV y su autoprueba. |
| `pruebas/td_simulado.py` | Lo que necesite el simulador para la orientación y el FOV gobernado. |

### 4.5 Parámetros nuevos (página Fase10)

| Parámetro | Por defecto | Rango | Qué es |
|---|---|---|---|
| `Modocamara` | `globo` | + `rasante` | El modo nuevo |
| `Camfov` | el de la cámara hoy (45) | 20–120 | FOV del globo y de superficie |
| `Rasaltura` | 0,35 | 0,1–3 | Altura de ojos sobre el suelo local |
| `Rasfov` | 90 | 60–120 | FOV horizontal en rasante |
| `Rasmirada` | 8 | −20–40 | Grados sobre la horizontal |
| `Rasvel` | 0,5 | 0–6 | Grados por segundo sobre el paralelo (0: trípode) |
| `Rasanillo` | 3 | 0–nº de anillos | Entre qué anillos va |
| `Rasbruma` | 0,35 | 0–1 | Bruma mínima en este modo |

## 5. Riesgos y dudas

| Riesgo | Por qué | Qué propongo |
|---|---|---|
| **La piel no está hecha para verse de cerca** | Las formaciones se diseñaron y se prueban para leerse a pocos píxeles con la cámara de globo (anchos mínimos en píxeles, siluetas a 18 px, tarjetas de racimo). A pantalla completa pueden verse pobres: cajas, prismas, losetas planas con escalones entre celdas. | El paso 0: mirarlo antes de escribir nada. Es el riesgo que decide si la propuesta vale la pena. |
| **El cielo** | Con la mirada hacia arriba, media imagen es fondo. Hoy es negro, y la bruma es gris azulado (`NIEBLA_COL`): lo lejano quedaría **más claro** que el cielo. | **Decidido: cielo negro.** La bruma del modo rasante funde hacia negro. El color de la bruma en `globo` y `superficie` no cambia. |
| Atravesar geometría | Satélites, puentes y coronas pueden cruzar el recorrido. | Subir sobre lo que haya delante; el plano cercano (0,05) hace el resto. Autoprueba con un mundo saturado. |
| Rendimiento | Detalle alto en todas las celdas, como hoy en superficie, contra el presupuesto de hojas (`HOJAS_LIGERO`, 100 000). Además, el cambio de LOD ocurre al cambiar el parámetro, no al acabar la transición: puede notarse un tirón al empezar. | Medir con `pruebas/sesion_escena.py`; si hace falta, el LOD por vecindad. |
| Transición | Pasar de globo a rasante cambia posición, orientación y FOV a la vez durante 20 s. | Mezclar el FOV con la misma curva que la posición; probar si conviene llegar primero y abrir el angular al final. |
| La esfera | El gran angular tiene sentido en una pantalla plana o un proyector. En la esfera real (mapa equirectangular) esta vista no se puede mostrar tal cual. | **Decidido: proyector y pantalla.** La esfera queda fuera (apartado 3, cubemap). |

## 6. Plan por pasos

**Paso 0 — Mirar antes de construir (sin código, hoy).** Con el proyecto abierto:

1. `Modocamara` = `superficie`, `Camaltura` = 0,5 (su mínimo), `Camvel` = 0,3.
2. En el Camera COMP `camara`, FOV = 90.
3. `Modoactuacion` activado, para quitar retícula y leyenda.

No es el modo propuesto (no está anclada, no sigue el suelo y mira casi a la horizontal en vez de hacia arriba), pero enseña lo esencial: cómo se ven las formaciones de cerca y con angular. Al terminar, el FOV de `camara` vuelve a 45: en globo el motor lo lee para encuadrar. Si lo que se ve no convence, lo primero es la piel y no la cámara.

**Paso 1 — El modo.** `rasante` con ruta de paralelo, altura sobre el suelo local, mirada, FOV gobernado por el motor y orientación con la vertical local. Retícula oculta. Autoprueba.

**Paso 2 — Atmósfera.** Bruma propia del modo y la decisión del cielo.

**Paso 3 — Rendimiento y acción.** LOD por vecindad si las medidas lo piden; ruta de acción (seguir la última nota).

**Fuera de alcance:** ojo de pez y salida equirectangular (cubemap).

### Autoprueba prevista (paso 1)

- en rasante, la cámara está a `Rasaltura` del suelo de la celda que tiene debajo, también sobre una hondonada y sobre un corte;
- el eje de la cámara queda `Rasmirada` grados sobre la horizontal local y su arriba es la vertical local, también cerca de los polos;
- el FOV que recibe la cámara es `Camfov` en globo y `Rasfov` en rasante, y el encuadre del globo no cambia al tocar `Rasfov`;
- la cámara gira con el planeta: con el giro y el balanceo en marcha, sigue sobre el mismo paralelo;
- planos de recorte: `near` menor que la distancia al suelo, `far` más allá del planeta;
- con un mundo saturado, ninguna pieza queda entre la cámara y su plano cercano;
- ida y vuelta de globo a rasante sin saltos; `globo` y `superficie` dan lo mismo que antes.

## 7. Decisiones cerradas (12 de noviembre de 2026)

| | Decisión |
|---|---|
| 1 | **Modo nuevo.** `rasante` es un tercer valor de `Modocamara`; `globo` y `superficie` no se tocan, ni sus autopruebas. |
| 2 | **En la fase 10.** `fase10_direccion.py` (v12) y el motor (v92): sirve en cualquier proyecto desde el nivel 10. No hay fase 32. |
| 3 | **Cielo negro.** Sin degradado de horizonte; la bruma del modo funde hacia negro. |
| 4 | **Proyector y pantalla.** Proyección rectilínea; sin ojo de pez ni salida equirectangular. |
| 5 | **Pasillo entre anillos.** La primera versión recorre el paralelo entre dos anillos (`Rasanillo`, `Rasvel`; con `Rasvel` 0, trípode). Seguir la acción queda para el paso 3. |

Queda por hacer el paso 0 (mirar la piel de cerca con los parámetros de hoy) y las dos comprobaciones señaladas en 4.3 y 4.4: lo que invade el límite entre anillos y cómo dar a la cámara la vertical local en TouchDesigner.

## 8. Paso 1: lo implementado y qué probar

`motor v92`, `comun v72` y `fase10_direccion.py` v12. Para tenerlo: relanzar `fase10_direccion.py` (o `recargar_todo.py`).

**Qué hay**

- `Modocamara` = `rasante`: la cámara anclada al planeta, por el paralelo entre dos anillos (`Rasanillo`, 4: latitud 12° N con 7 anillos), a `Rasvel` grados/s (0,5; con 0, trípode), a `Rasaltura` (0,35) sobre el suelo más alto de las dos celdas que tiene a los lados (con el relieve de la naturaleza), mirando `Rasmirada` (8°) sobre la horizontal, con `Rasfov` (90°). Transición de 20 s desde y hacia los otros modos; el angular se abre con ella.
- **El giro y el FOV de la cámara los da ahora el motor** (`cam('rot')`, `cam('fovcam')`) y el Camera COMP ya no usa *Look At*. El angular del globo y de superficie es el parámetro nuevo `Camfov`, que nace con el FOV que tuviera la cámara. **El FOV ya no se cambia en el Camera COMP.**
- Con `rasante`, todas las celdas van con el detalle alto (la misma bandera que `superficie`).
- Leyenda: línea `RASANTE` con anillos, latitud, longitud, suelo, altura de ojos, FOV y las dos celdas vecinas.
- `pruebas/vista_rasante.py`: una vista previa sin TouchDesigner (superficie de hoy arriba, rasante abajo). Luz plana y sin materiales: sirve para el encuadre, no para el acabado. `pruebas/vista_rasante_naturaleza.png` y `pruebas/vista_rasante_ciudad.png` son sus salidas.

**Lo que no hace todavía:** no esquiva geometría, no oculta la retícula por sí sola (usar `Modoactuacion`), no tiene bruma ni LOD propios (pasos 2 y 3).

**Probado fuera de TouchDesigner:** la autoprueba de la fase 10 (15 comprobaciones nuevas, todas OK, también relanzada sobre el nivel 31) y la batería `pruebas/correr_fases.py`, que da lo mismo que antes del cambio. Esa batería ya traía fallos antes de tocar nada (`particulas` y `humo` con `Materialrespaldo` desde la fase 11, y cuatro de la esfera en `sala_virtual.py`); no son de este cambio y siguen igual.

**Qué mirar en TouchDesigner, por orden**

1. Tras relanzar la fase 10, **el globo se ve exactamente igual que antes**. Si no, el fallo está en el giro o el FOV que entrega el motor: es lo único que cambia para los modos de siempre.
2. `superficie` se ve igual que antes (antes la orientaba el *Look At*; ahora, el motor).
3. El menú `Modocamara` tiene `Rasante`. Si no aparece, el informe de la fase lo dice.
4. `rasante` con `Modoactuacion`: horizonte nivelado y abajo, formaciones alzándose, sin avisos de bucle de cocinado en `camara`.
5. Naturaleza frente a ciudad: si en la ciudad la cámara atraviesa edificios (lo esperable, ver 4.3).
6. Fotogramas por segundo en `rasante` frente a `globo`.
7. Cómo se ve la piel de cerca: es la pregunta del paso 0.

## 9. Tras la primera prueba en TouchDesigner: tumbada (13 de noviembre de 2026)

`motor v94`, `fase10 v13`. En TouchDesigner la v12 quedaba pegada a las paredes de las conchas y casi no se veía nada, y la vista que se busca es otra: **tumbado, flotando, mirando hacia arriba con todo el angular posible**.

**Qué cambia**

- Por defecto mira al cenit (`Rasmirada` 90), con `Rasfov` 140 y `Rasaltura` 0,6. Los valores de la v12 pasan a estos solo si no se habían tocado; los deslizadores llegan ahora a 90, 160 y 4.
- La cámara flota sobre el suelo más alto de las celdas de los lados **y de las de delante y detrás** (15° atrás, 15° y 30° adelante). Antes solo contaban las dos de al lado, y la pared de la celda siguiente llenaba el cuadro.

**El límite de esta versión.** La cámara sigue siendo rectilínea. Con 140° en horizontal (114° en vertical) mirando al cenit entra lo que esté a más de 20° sobre el horizonte por los lados y a más de 33° por arriba y abajo: las formaciones vecinas asoman por los bordes y fugan hacia el centro, pero el anillo del horizonte no se ve. A partir de 150° los bordes se estiran mucho.

**«Casi 360» de verdad es un ojo de pez**, y eso no sale de una cámara normal: hay que renderizar un cubemap (seis vistas) y reproyectarlo. Es el mismo trabajo que el mapa equirectangular de la esfera (apartado 3). Cuesta hasta seis renders por fotograma, así que hay que medirlo contra los 20 fps antes de comprometerse.

**Palancas mientras tanto:** `Rasmirada` 50–70 mete más formación y menos cielo; `Rasaltura` más alta despega de las paredes; `Rasfov` hasta 160.

## 10. Ojo de pez (13 de noviembre de 2026)

`motor v95`, `fase10 v14`.

**Cómo está hecho.** El Render TOP de TouchDesigner tiene un modo propio, *Fish-Eye (180)* (`rendermode` = `fisheye180`): un solo render que cubre 180° alrededor de adonde mira la cámara. No hace falta el cubemap de seis vistas del apartado 9, así que el coste debería ser el de un render normal. Los shaders de la piel ya proyectan con `TDWorldToProj`, que es lo que ese modo necesita.

- Parámetro nuevo `Rasojo` (encendido por defecto). Con `Modocamara` = `rasante`, el motor pone el render en ojo de pez; al salir, vuelve al 2D. Lo cambia solo cuando toca, no en cada fotograma.
- Mirando al cenit (`Rasmirada` 90), el horizonte entero queda en el borde del círculo y las formaciones fugan hacia el centro.
- `Rasfov` no cuenta con el ojo de pez: son siempre 180°.
- La leyenda dice `ojo de pez 180` en la línea `RASANTE`.

**Lo que no sé sin verlo en TouchDesigner**

1. **Cómo encaja el círculo en 1280 × 720**: si sale un círculo centrado con negro a los lados, una elipse estirada o recortado arriba y abajo. Según lo que salga, se ajusta la resolución del render en ese modo.
2. **Las caras grandes cerca de la cámara.** Ese modo dobla los vértices, no las caras: una loseta o una pared grande junto a la cámara sale con los bordes rectos y puede verse rota. Si pasa, hay dos salidas: subdividir las piezas grandes o pasar al cubemap con reproyección (más caro, pero exacto).
3. **El cambio de modo es un corte** a mitad de la transición de 20 s, no un fundido.
4. Que los materiales que no son de la piel (Phong y constantes: núcleo, retícula, luz de celda) se dibujen bien en ese modo.

Si TouchDesigner no acepta el modo, el Textport dice `AVISO  ojo de pez: …` y el render se queda en 2D.

Fuentes de los nombres del modo: [Render TOP](https://derivative.ca/UserGuide/Render_TOP) y [Projection TOP](https://derivative.ca/UserGuide/Projection_TOP), vistos solo a través de un buscador: desde aquí no se puede abrir la documentación de Derivative.

