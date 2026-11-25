# Requerimiento · La sala virtual en su propio proyecto de TouchDesigner

> **Estado: propuesta para revisar. No hay nada implementado.** Este documento analiza si conviene sacar `/project1/SALA` del proyecto de Estratos a otro proyecto (otro proceso) de TouchDesigner, cómo se hablarían los dos y en qué orden se haría. Las decisiones marcadas **[DECIDIR]** son del usuario; la sección 9 las reúne.

*Basado en `sala_virtual v44` (`sala v28`), `motor v147`, fases 21 a 24 y 43. Las líneas citadas son de `main` a 25 de noviembre de 2026.*

---

## 1. El problema

TouchDesigner cocina toda la red en **un solo hilo** (el principal): Python, Script CHOP/SOP/TOP, Execute DAT y la preparación de los render. Hoy, en ese hilo, cada fotograma, van juntos:

| Quién | Qué hace cada fotograma |
|---|---|
| **FASE1** | el motor (`estratos_motor.py`, ~26 500 líneas): mundo, notas, piel, juego, monstruos, luz DMX, micrófono, personas… y su render |
| **SALA** | `latido_sala → frame_tick()`: el director de demos, pasar el público a FASE1, recocinar a la fuerza 6 Script CHOP de instancias (`i_personas`, `i_personas_bolas`, `i_personas_conos`, `i_arcos`, `i_equipos`, `i_haces`) |
| | `audio_mic`: un Script CHOP que sintetiza en Python/numpy el audio del micrófono a 44,1 kHz (pasos, palmadas, toses, drone, sub, clic del estrobo), con 1/d y retardo por fuente |
| | 3 render (`render_sala` 1280×720, `render_cenital` 320×288, `render_plano` 200×180) con 6+ Light COMP con sombra, haces aditivos en la bruma, la esfera/pantalla con GLSL MAT |
| | rótulo, título, cabecera y el monitor compuesto (`salida_sala`) |

Todo lo que gasta la sala lo pierde la pieza. Y la sala **no forma parte de la obra**: es una maqueta para probarla. Sacarla a otro proceso le da su propio hilo principal (y su propia ventana), y deja a FASE1 como estará en la instalación real.

### 1.1 Lo que NO se gana (para no esperar milagros)

- **La GPU es la misma.** Dos procesos se reparten la tarjeta; los render de la sala siguen costando GPU, y el cambio de contexto entre procesos tiene un coste. La ganancia esperable es sobre todo de **CPU / hilo principal**.
- **No es gratis cruzar procesos.** Lo que hoy es un `Select TOP` (cero copias) o una llamada Python pasa a ser un canal con latencia (1-3 fotogramas) y que puede caerse.

Por eso el primer paso (M0, sección 8) es **medir** antes de decidir.

---

## 2. Inventario: cómo se hablan hoy SALA y FASE1

Todo lo que cruza la frontera, encontrado en el código. Es lo que el diseño tiene que resolver una por una.

### 2.1 De FASE1 a la sala («el mundo hacia la sala»)

| # | Qué | Cómo, hoy | Dónde |
|---|---|---|---|
| F1 | **La imagen de la obra** (render con el título de la ronda) | `Out TOP out_render` en FASE1 → `Select TOP imagen_fase1` en SALA | `sala_virtual.py:877-890` |
| F2 | **El estado del mundo** para la cabecera, el rótulo y comprobar cada capítulo/caso | Python directo: `op('/project1/FASE1').op('motor').module`, `F.W()`, `F.cfg()`, `F.par()` | ~130 accesos en `sala_motor.py` 1644-3843 |
| F3 | **La luz de la sala** | **No llega.** FASE1 calcula la luz (fase 23: balance, baño, estrobo, noche) y la saca por `dmx_out` (Art-Net o USB Pro), pero los focos de la sala solo saben `Modoluz = apagado / prueba` | `fase23_sala.py:180`, `sala_motor.py:492-540` |
| F4 | **FASE1 mira a la sala** (al revés de lo esperado) | `motor.demo_genozilla()` lee `op('/project1/SALA').par.Demo` | `estratos_motor.py:21921-21927` |

### 2.2 De la sala a FASE1 («la sala hacia el mundo»)

| # | Qué | Cómo, hoy | Dónde |
|---|---|---|---|
| S1 | **El público** (lo que vería la cámara cenital) | escribe la tabla `sala_personas` de FASE1 (x, y, altura) y pone `Fuente = simulada`; guarda y devuelve la de antes (`alimentar_entra/sale`) | `sala_motor.py:3238-3345` |
| S2 | **El micrófono** | `Fuentemic = chop` y `Chopmic = /project1/SALA/audio_mic`: FASE1 cocina el Script CHOP de la sala | `sala_virtual.py:1361-1373`, `estratos_motor.py:24109` |
| S3 | **Control del director de demos** | Python directo: `guardar_escena / cargar_escena`, poner y devolver parámetros, `guion_demo(...)`, `note_off(...)`, `foco_camara(...)`, `sala_reset(...)`, `demo_refs`, `losetas_bajo`, `celda_de_casilla`… | `sala_motor.py:2468-3260` |
| S4 | **Autoprueba de las demos** | avanza FASE1 paso a paso con un reloj a mano (`paso_fase1`), hace `deepcopy` del mundo y lo devuelve | `sala_motor.py:3732-3843` |
| S5 | La imagen de profundidad de la cámara cenital | existe (`render_cenital`, `profundidad`) pero **FASE1 no la usa**: la sala simulada va por la tabla (S1) | `sala_virtual.py:1356` |

### 2.3 Lectura

Hay dos clases de cosas muy distintas:

- **Señales** (F1, F3, S1, S2, S5): flujos continuos, de un sentido, con forma fija. Cruzan bien entre procesos y, **mejor aún, ya tienen su equivalente en el hardware real** (proyector, focos DMX, cámara, micrófono).
- **Control** (F2, F4, S3, S4): la sala metida dentro de FASE1, leyendo y escribiendo su mundo con ~130 llamadas. Esto **no cruza** entre procesos sin rehacerlo: es el grueso del trabajo y la decisión más importante (sección 5).

El director de demos son ~2 200 de las 3 843 líneas de `sala_motor.py`, y casi todas tocan FASE1.

---

## 3. El principio que propongo

> **La sala separada habla con Estratos exactamente por los mismos protocolos que el hardware real.**

Ya era la idea de la sala («habla con Estratos por los mismos sitios que el hardware real», cabecera de `sala_virtual.py`), pero hoy se cumple a medias porque comparten proceso. Separados, se puede cumplir del todo:

| Aparato real | Lo que hace en la sala real | La sala virtual, separada |
|---|---|---|
| Proyector / esfera de LEDs | recibe la salida de vídeo | recibe la imagen de FASE1 por **Spout** (textura compartida en GPU) |
| Focos y estroboscopio | reciben **DMX** (Art-Net) | escucha el **mismo Art-Net** que manda `dmx_out` (DMX In CHOP) y enciende sus Light COMP con él |
| Micrófono | entra audio | manda audio (sección 4, canal A) |
| Cámara cenital | da profundidad / personas | manda las personas (y, más adelante, la profundidad) |

La consecuencia buena: **FASE1 en pruebas = FASE1 en la instalación**. Lo que se prueba con la sala es la misma cadena (DMX incluido) que se usará en el montaje, y F3 —que hoy falta— sale casi gratis: los focos virtuales por fin siguen al balance, al estrobo y a la noche de la fase 23.

---

## 4. Los canales (el contrato)

Cada canal tiene nombre, dirección, transporte y forma. El contrato se escribe en un sitio (`estratos_comun.py` o un `contrato_sala.py` común; **[DECIDIR] D7**) con puertos, direcciones OSC y versión, para que los dos proyectos lo lean igual.

| Canal | Dirección | Transporte propuesto | Alternativa | Forma |
|---|---|---|---|---|
| **V** vídeo | FASE1 → SALA | `Syphon Spout Out TOP` (`stratos_obra`) | NDI Out TOP; Touch Out TOP a resolución reducida | la textura de `con_titulo_juego` / `render` |
| **L** luz | FASE1 → SALA | Art-Net de `dmx_out` a `127.0.0.1`, `DMX In CHOP` en SALA | — | 512 canales; la sala los decodifica con la misma tabla `dmx_canales` |
| **P** personas | SALA → FASE1 | OSC (UDP) un mensaje por fotograma con cambios | Touch Out/In DAT de la tabla | `n, x1, y1, h1, x2…` en metros del suelo cubierto (la forma de `SALA_COLS`) |
| **A** audio | SALA → FASE1 | Touch Out/In CHOP a 44,1 kHz | Audio Device Out → cable virtual (VB-Cable) → `Fuentemic = microfono` | 1 canal mono |
| **E** estado | FASE1 → SALA | OSC, unas 10 veces por segundo | Touch Out DAT | lo que la sala dibuja: título/rótulo/cabecera de la demo, y en demos guionizadas, la gente (ver 5) |
| **K** control | SALA → FASE1 | OSC | — | pocas órdenes de alto nivel: `demo <nombre>`, `caso <k>`, `siguiente`, `salir`, `palmada` |
| **H** latido | ambos | OSC, 2 veces por segundo | — | `versión del contrato, frame, reloj`; sin latido 2 s → «sin enlace» |
| *D profundidad* | *SALA → FASE1* | *Spout* | — | *fuera de la v1: para probar `Fuente = camara` con la imagen de la sala* |

### Notas por canal

- **V.** Spout comparte la textura en GPU sin bajarla a CPU: es lo único que sustituye bien al `Select TOP`. Touch Out TOP a 1280×720 a 60 fps son cientos de MB/s por TCP: solo como plan C y más pequeño.
- **L.** Hay que confirmar que `dmx_out` puede mandar Art-Net en unicast a `127.0.0.1` sin interfaz física (o a la dirección de la tarjeta de red), y que un DMX In CHOP en otro proceso de la misma máquina lo recibe. Si en la sala real se usa USB Pro, para pruebas se pasa a Art-Net. La sala gana `Modoluz = dmx` (por defecto) además de `apagado` y `prueba`.
- **P.** Mantener la semántica de hoy: FASE1 recibe en un `OSC In DAT`, escribe su `sala_personas` y usa `Fuente = simulada`. Así **no cambia nada del motor** de las fases 22 y 24. Con el enlace caído, FASE1 vuelve a su Fuente (lo que hoy hace `alimentar_sale`), pero ahora lo decide FASE1, no la sala.
- **A.** El audio entre procesos tiene dos problemas: bloques irregulares y relojes que derivan. El receptor tiene que tolerar bloques de tamaño variable (revisar `mic_flujo`, motor v56) y un pequeño búfer. El cable virtual es lo más fiel (FASE1 lo oye como un micro de verdad) pero obliga a instalar un driver; Touch In CHOP no instala nada. **[DECIDIR] D4.**
- **K.** Las órdenes son pocas y de alto nivel a propósito: nada de leer o escribir el mundo desde la sala.

---

## 5. El director de demos: la decisión grande

Hoy el director vive en la sala y opera FASE1 por dentro (S3, S4, F2). Separados, hay dos caminos:

### Opción D1 (recomendada) — el director se muda a FASE1

El director pasa a ser parte de FASE1 (un módulo `demo_sala` dentro del motor o junto a él, con su página de parámetros), con todo lo que hoy hace sobre el mundo: entrar/salir, parámetros de cada caso, `guion_demo`, comprobar capítulos, cabecera, `foco_camara`, la autoprueba con `paso_fase1`.

- **¿Quién mueve a la gente en una demo?** El guion, que ya sabe dónde tiene que ir cada uno (las casillas relativas al monstruo, a la testigo, a la fila…) porque las calcula con el mundo. FASE1 escribe esa gente **directamente en su `sala_personas`** (sin ida y vuelta) y la manda por **E** a la sala, que la dibuja como monigotes y genera su ruido (pasos, palmadas, el grito).
- **La sala queda como «renderizador + sensores»**: dibuja la sala y la gente que le digan, enciende los focos con el DMX, saca el audio. Con su propio público libre (`plan()`, el paseo sin guion) cuando no hay demo: entonces es la sala la que manda la gente a FASE1 por **P**.
- **Dos modos, explícitos en el contrato:** `publico = sala` (la sala inventa la gente → P) o `publico = guion` (FASE1 la inventa → E).
- **El audio cierra el lazo de verdad:** el grito de la D4 suena en la sala y vuelve a FASE1 por el micrófono, que tiene que abrir el corte. Hoy también pasa por el micrófono virtual, así que no se pierde nada; se gana que sea el mismo camino que en la sala real.
- **Ventajas:** el director está donde están los datos (las 130 llamadas pasan a ser locales); la autoprueba de las demos sigue siendo determinista (no depende de la red); F4 desaparece (el motor ya no mira `/project1/SALA`).
- **Coste:** mover ~2 200 líneas y separar dentro de ellas lo que es «del mundo» de lo que es «de dibujar la sala» (titulo, rótulo, coreografía en metros). Es el grueso del trabajo.

### Opción D2 — el director se queda en la sala y habla por red

Cada una de las ~130 lecturas y escrituras pasa a ser un mensaje (RPC). Problemas: lecturas del mundo cada fotograma con latencia, órdenes que se cruzan con el reloj de FASE1, la autoprueba (S4) deja de poder avanzar FASE1 paso a paso desde otro proceso, y el protocolo crece con cada demo nueva. **No la recomiendo.**

### Opción D3 — separar por fases: primero señales, el director luego

Hacer D1 al final (sección 8, M3) y, mientras tanto, mantener las demos solo con la sala en el mismo proceso. Es compatible con D1; es el orden que propongo.

**[DECIDIR] D1.**

---

## 6. Cómo se lanza: dos opciones de proceso

### P-A (recomendada) — dos proyectos, dos ventanas

`Estratos.toe` (FASE1, como hoy) y `Sala.toe` (nuevo, solo con `/project1/SALA`), abiertos a la vez en la misma máquina, hablando por los canales de la sección 4.

- Cada uno con su Textport, su Perform window (la de la sala puede ir a un segundo monitor) y su ritmo.
- La sala se puede cerrar sin tocar la pieza; la pieza no sabe si la sala existe (solo el latido **H**).
- Abre la puerta a que la sala corra en **otro ordenador** (todo es red salvo Spout, que tiene NDI de reserva).
- `sala_virtual.py` construye en el proyecto donde se lance; `recargar_todo.py` deja de montar la sala (o la monta solo si está en `Sala.toe`).

### P-B — Engine COMP dentro de Estratos

La sala como `.tox` dentro de un Engine COMP de FASE1: TouchDesigner la corre en otro proceso (TouchEngine) y los canales son las entradas/salidas del COMP.

- Ventaja: un solo proyecto, un solo lanzamiento; no hacen falta puertos ni Spout.
- Inconvenientes: depurar la sala es más incómodo (su Textport no está a mano), la imagen de la sala vuelve a componerse en el proceso de FASE1, y hay que **verificar la licencia** (sección 7).

**[DECIDIR] D2.** El contrato de la sección 4 sirve para las dos: con P-B solo cambia el transporte.

---

## 7. Riesgos y cosas a verificar antes de empezar

| Riesgo | Por qué importa | Qué hacer |
|---|---|---|
| **Licencia de TouchDesigner** | Algunas funciones (Engine COMP, Shared Mem, varias instancias, Spout/NDI, DMX) dependen del tipo de licencia; los render de 1280×720 hacen pensar que puede ser Non-Commercial | **[DECIDIR] D3**: qué licencia hay. Comprobar en Derivative cada operador del contrato antes de M1 |
| La ganancia es menor de lo esperado | La GPU es la misma (1.1) | M0: medir con `diagnostico_fps.py` con la sala `Activa` encendida y apagada, y con `Vista` = la más cara |
| Art-Net en local | `dmx_out` puede necesitar una interfaz; el firewall de Windows puede cortar UDP en local | prueba de enlace L en M1 |
| Audio entre procesos | bloques irregulares, deriva de reloj, latencia que pueda afectar al onset del micro y al descarte del clic del estrobo (fase 23: `DESCARTE_DESTELLO`) | medir la latencia de A y revisar ese descarte con el retardo nuevo |
| Spout solo en Windows | la sala real es Windows, pero si algún día se prueba en Mac, Syphon | el contrato nombra «vídeo», no «Spout»; NDI de reserva |
| Código común duplicado | los dos proyectos cargan `estratos_comun.py` | una sola copia en la carpeta `est`; el contrato con versión y la sala avisa si no coincide |
| Las autopruebas | hoy la autoprueba de la sala avanza FASE1 (S4) | D1: la de las demos pasa a FASE1; la sala se prueba con un FASE1 falso que manda E y L grabados; una **prueba de enlace** nueva con los dos en marcha |
| Romper lo que funciona | las demos están probadas y se usan | migración por pasos (sección 8) con la sala en el mismo proceso hasta M4; cada paso deja todo funcionando |

---

## 8. Plan por pasos (cada uno se prueba y se puede parar ahí)

| Paso | Qué | Se acaba cuando |
|---|---|---|
| **M0 · Medir** | `diagnostico_fps.py` con la sala apagada, encendida en `vacia` y en `genozilla`, `Vista` entrada y juego. Ningún cambio de código | hay números: ms por fotograma de la sala y fps de FASE1 con y sin ella. **Si la sala cuesta poco, se para aquí** y se optimiza dentro (ver 8.1) |
| **M1 · Contrato y señales FASE1 → sala** | contrato con versión y puertos; latido **H**; canal **V** (Spout) y canal **L** (DMX In, `Modoluz = dmx`). Todavía en el mismo `.toe`: la sala lee por los canales y no por `Select TOP`. Con eso se prueba el protocolo sin separar nada | los focos virtuales siguen a la fase 23 (Simbalance 0,3 / 0,7 / 1,2 / 10) y la pantalla se ve por Spout |
| **M2 · Señales sala → FASE1** | canal **P** (personas por OSC a `sala_personas`) y **A** (audio). FASE1 gana su página «Sala virtual» (enlace, puertos, estado) y es quien pone y devuelve Fuente/Fuentemic | `alimentar` y `Usarmic` ya no tocan FASE1 desde la sala; con la sala cerrada FASE1 vuelve a su Fuente en 2 s |
| **M3 · El director a FASE1 (D1)** | módulo `demo_sala` en FASE1; canales **E** y **K**; la sala dibuja la gente del guion; `motor.demo_genozilla()` lee su propio parámetro | todas las demos (1 a 5) pasan su autoprueba en FASE1 y se ven igual en la sala; ya no hay `op('/project1/FASE1')` en la sala ni `op('/project1/SALA')` en el motor |
| **M4 · Separar** | `Sala.toe` (o Engine COMP, según D2); `sala_virtual.py` monta allí; `recargar_todo.py` sin sala | Estratos corre sin la sala dentro; la sala, en su proceso; la prueba de enlace pasa |
| **M5 · Limpiar** | quitar `out_render`/`imagen_fase1`, `Chopmic` a la sala, `alimentar_entra/sale`, el modo de compatibilidad | ningún resto de la sala en FASE1 salvo el receptor del contrato |

### 8.1 Si M0 dice que no compensa

Alternativas dentro del mismo proceso, más baratas: no cocinar los render de la sala cuando no se miran; bajar sombras y bruma; recocinar las instancias solo cuando la gente cambia y no a la fuerza cada fotograma; generar el audio en bloques más grandes o con un CHOP nativo. Se documentarían en otro requerimiento.

---

## 9. Decisiones para revisar

| | Pregunta | Propuesta |
|---|---|---|
| **D0** | ¿Medimos primero (M0) y decidimos con números? | **Sí** |
| **D1** | ¿El director de demos se muda a FASE1 (D1) o se queda en la sala hablando por red (D2)? | **D1**, en el paso M3 |
| **D2** | ¿Dos proyectos y dos ventanas (P-A) o Engine COMP dentro de Estratos (P-B)? | **P-A** |
| **D3** | ¿Qué licencia de TouchDesigner hay en el ordenador de pruebas y en el de la sala? | (pendiente: condiciona D2 y los transportes) |
| **D4** | Audio: ¿Touch In/Out CHOP (nada que instalar) o cable virtual (como un micro real)? | Touch CHOP para empezar; cable virtual como opción |
| **D5** | ¿La sala correrá siempre en la misma máquina o puede ir en otra? | misma máquina, pero el contrato vale para red (NDI en vez de Spout) |
| **D6** | La luz de la sala, ¿por DMX real (Art-Net) desde ya, aunque hoy no llegue? | **Sí**: es lo que más se gana en fidelidad |
| **D7** | ¿El contrato va en `estratos_comun.py` o en un archivo propio (`contrato_sala.py`)? | archivo propio, cargado por los dos |

---

## 10. Criterios de aceptación (de todo el trabajo)

1. Con la sala en marcha, los fps de FASE1 mejoran en lo que M0 haya medido como coste de la sala (±10 %).
2. Con la sala cerrada, FASE1 funciona igual que sin sala y lo dice en una línea de leyenda (`SALA  sin enlace`); al volver a abrirla, se reengancha sola.
3. Los focos virtuales siguen a la fase 23 por DMX: depósito, tensión, erosión dominante (estrobo ≤ 3 Hz) y la noche del fin de ciclo.
4. Las cinco demos se ven y se comprueban igual que hoy, y su autoprueba pasa sin la sala abierta.
5. Ni la sala lee ni escribe el mundo de FASE1, ni el motor busca `/project1/SALA`.
6. Una **prueba de enlace** con los dos procesos dice, canal por canal, si llega y con qué latencia.
7. Relanzar cualquiera de los dos scripts no rompe al otro ni pierde el mundo.
