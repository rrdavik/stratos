# Estratos · Propuesta: vista inmersiva a ras de suelo

*Análisis de la petición «un nuevo punto de vista inmersivo, darle una vuelta al de acercamiento a la superficie, con alguna vista de cerca con gran angular». 12 de noviembre de 2026, sobre `main` en `motor v91`. **No implementa nada**: es el análisis y una propuesta para aprobar antes de pasar a código.*

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
| **Paralelo** | Avanza despacio (`Rasvel`) por el límite entre dos anillos de celdas: un círculo continuo con formaciones a ambos lados, como una calle o un valle. | **Recomendada para la primera versión.** Determinista, sin azar, y lejos del centro de las celdas. |
| Acción | Viaja hacia la celda de la última nota (`W['ev']['ultima']`) y se queda mirándola crecer. | La más musical. Segunda versión: necesita una ruta entre celdas y decidir qué hace con notas rápidas. |
| Trípode | Quieta en un punto; el mundo cambia delante. | Trivial una vez hecho el paralelo (`Rasvel` 0). |

El paralelo se elige con `Rasanillo` (entre qué anillos) o deriva solo de uno a otro muy despacio.

**Por comprobar al implementar:** cuánto invaden el límite entre anillos los satélites, las fusiones de cluster y los puentes, carreteras y ríos del tejido (fase 13). Si lo cruzan, la cámara sube lo justo sobre lo que tenga delante en lugar de atravesarlo. No he verificado la huella exacta de cada pieza dentro de su celda.

### 4.4 Lo que hay que cambiar

| Dónde | Cambio |
|---|---|
| `camera_state()` | El tercer modo, con su peso de transición; posición en coordenadas del planeta llevada al mundo; altura sobre el suelo local; `near` y `far` medidos desde el suelo real y no desde `Re`. |
| FOV | Hoy el motor lo lee del Camera COMP y la cámara no lo recibe del motor. Hay que invertirlo: el FOV del globo pasa a un parámetro (`Camfov`, con el valor que tenga hoy la cámara), el motor entrega el FOV mezclado (`cam('fov')`) y `_cam_optics()` lee el parámetro. Si no, el encuadre del globo se calcularía con el FOV del rasante. |
| Orientación | El *Look At* del Camera COMP usa un vector arriba fijo; una cámara que recorre el planeta necesita que arriba sea la vertical local. O se le da un vector arriba desde el motor o el motor entrega el giro completo y se quita el *Look At*. **Hay que mirarlo en TouchDesigner**: no sé desde aquí qué admite el Camera COMP de la versión instalada. |
| `niebla()` / `niebla_camara()` | En rasante, la bruma empieza a media celda y es total poco más allá de lo que asoma sobre el horizonte. Propongo además una cantidad mínima propia (`Rasbruma`) aunque el modular no mande espacialidad: sin perspectiva aérea no hay escala. |
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
| **El cielo** | Con la mirada hacia arriba, media imagen es fondo. Hoy es negro, y la bruma es gris azulado (`NIEBLA_COL`): lo lejano quedaría **más claro** que el cielo. | Decidir el cielo: negro con la bruma teñida hacia negro, o un degradado de horizonte del color de la bruma. Es una decisión de dirección visual. |
| Atravesar geometría | Satélites, puentes y coronas pueden cruzar el recorrido. | Subir sobre lo que haya delante; el plano cercano (0,05) hace el resto. Autoprueba con un mundo saturado. |
| Rendimiento | Detalle alto en todas las celdas, como hoy en superficie, contra el presupuesto de hojas (`HOJAS_LIGERO`, 100 000). Además, el cambio de LOD ocurre al cambiar el parámetro, no al acabar la transición: puede notarse un tirón al empezar. | Medir con `pruebas/sesion_escena.py`; si hace falta, el LOD por vecindad. |
| Transición | Pasar de globo a rasante cambia posición, orientación y FOV a la vez durante 20 s. | Mezclar el FOV con la misma curva que la posición; probar si conviene llegar primero y abrir el angular al final. |
| La esfera | El gran angular tiene sentido en una pantalla plana o un proyector. En la esfera real (mapa equirectangular) esta vista no se puede mostrar tal cual. | Asumo que es para proyector o pantalla. Si es para la esfera, la propuesta es otra (apartado 3, cubemap). |

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

## 7. Decisiones que necesito

1. **¿Modo nuevo o sustituir `superficie`?** Recomiendo modo nuevo: `superficie` sigue sirviendo de plano medio entre el globo y el suelo, y sus autopruebas no se tocan.
2. **¿Dónde entra?** Recomiendo en `fase10_direccion.py` (v12) y el motor (v92), donde vive `Modocamara`, y no como fase 32: así sirve en cualquier proyecto desde el nivel 10.
3. **El cielo:** negro o degradado de horizonte.
4. **¿Pantalla y proyector, o también la esfera?**
5. **Ruta de la primera versión:** paralelo (recomendado) o directamente seguir la acción.
