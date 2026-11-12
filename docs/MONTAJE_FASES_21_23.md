# Estratos · Montaje
## Fases 21 a 23: micrófono, cámara y luz de sala

*Continúa `MONTAJE_FASES_11_18.md` (que llega a la fase 19). Referencias: los docs **Requerimiento v4 · micrófono, cámara y DMX** y **Tareas técnicas v4 · micrófono, cámara y DMX** (decisiones D1 a D10, cerradas el 28 de octubre de 2026). Las reglas de siempre siguen valiendo: un script por fase, encima de lo anterior, con su versión en la primera línea del informe y una AUTOPRUEBA al final. Las fases se hacen en línea: cada una se revisa antes de empezar la siguiente. Esta versión del montaje trae las **fases 21, 22 y 23**. Las fases 24 a 31 (el plan v5) están en `MONTAJE_FASES_24_31.md`.*

---

### ¿Qué script lanzo? `recargar_todo.py`

Cualquier fase recarga el motor y todo lo común (`install_core`), así que **no hace falta lanzar una fase concreta para actualizar**. Para no pensar cuál, un solo comando las deja todas al día, en orden, conservando el mundo:

```python
exec(open('C:/Users/DareDave/Downloads/est/recargar_todo.py').read())
```

- Proyecto nuevo (no existe `/project1/FASE1`): empieza por `fase12_base.py`. Si ya existe, no la lanza.
- Lanza fase 3 … 31 (las que haya), para en la primera que falle y termina con un resumen OK/FALLO por fase.
- Relanza `sala_virtual.py` solo si `/project1/SALA` ya existe (`SALA = True` en el script para montarla también si no).
- No lanza `ajuste_vista.py` (pisa lo ajustado a mano).
- Una fase suelta sigue valiendo para probar solo lo último.

---

### Estado en una frase

La sala entra en la pieza: desde la fase 21 el micrófono escucha al público, y cada sonido que empieza (una palmada, una tos, unos pasos) es un golpe de erosión de un pad 9 que no está en la batería; si la sala hace mucho ruido durante un rato, se abre un corte.

---

### Archivos

| Archivo | Para qué | Versión |
|---|---|---|
| `estratos_motor.py` | La v55 añade el micrófono: flujo espectral, onsets, el pad 9 de erosión (baja escalones enteros), el corte por ruido de sala y la línea `MICRO`; la v56, `Fuentemic` = chop (el audio de cualquier CHOP, como la sala virtual); la v57 saca `mic_sim` y `mic_flujo` del modo Time Slice de su entrada (en TouchDesigner avisaban «Editing numSamples is not supported in Time Slice mode»); la v58, la página Fase3 con seis parámetros menos (fase 3 v13, ver «Página Fase3» en `MONTAJE_FASES_3_10.md`); la v59, la página Fase4 con 4 parámetros (fase 4 v8, ver «Página Fase4»); la v60, la página Fase6 con 9 (fase 6 v6: el compás de la línea de tiempo, ver «Página Fase6»); la v61, la página Fase7 con 12 (fase 7 v16: cada intensidad a 0 apaga lo suyo); la v62, la página Fase8 con 11 (fase 8 v13: la luminosidad del suelo en un solo `Paletaluz`); la v63, la página Fase11 con 35 (fase 11 v9: siete ajustes finos de la geometría, fijos); la v64, la página Fase13 con 12 (fase 13 v6: el ancho máximo del río sale de `Anchorio`); la v65, la página Fase21 con 10 (fase 21 v3: tiempo muerto y ventana del ruido, fijos); la v66, sin la simulación de la fase 21 (`Fuentemic` micrófono o chop) | `motor v66` |
| `estratos_comun.py` | La v37: `require_base(21)` acepta un proyecto en la fase 19 o en la 20 (los POPs, sin fusionar: D1) y el informe dice cuál encontró; la v38 quita de la página Fase3 `Growstep`, `Gatemode`, `Rotextra` y los tres ajustes de la luz de las conchas, conservando lo que hacían; la v39 deja la página Fase4 en `Umbralram`, `Pasoumbral`, `Tramoscumbre` y `Satelite`; la v40 quita de la Fase6 `Negrasporcompas`, `Girovivo` y `Compasesterritorio`; la v41, de la Fase7 `Balizasdrum`, `Erosionvel`, `Pumpon`, `Multradio`, `Pumphold` y `Pumpvelmin`; la v42, de la Fase8 `Paletaalterna`, `Contrasteocupada` y `Tapaluz`; la v43, de la Fase11 `Rebote`, `Maxcaosnat`, `Varangulo`, `Cuantizar30`, `Inclinacion`, `Densidadhoja` y `Muroterraza`; la v44, de la Fase13 `Anchomaxrio` y `Pendientemin`; la v45, de la Fase21 `Refractariomic` y `Ventanaruido`; la v46, la simulación de la fase 21 (`mic_sim`, `mic_fuente`, `Simonset`, `Simruido`, `Simdrone`) | `comun v46` |
| `fase21_microfono.py` | El micrófono: página Fase21, `mic_in` y `mic_flujo`, la fila del pad 9 en `perfiles_erosion` y `colores_drum` (v2: `Fuentemic` = chop y `Chopmic`; v3: la página Fase21 con 10 parámetros en vez de 12; v4: sin la simulación (`mic_sim`, `mic_fuente`, `Simonset`, `Simruido`, `Simdrone`), 7 parámetros) | `fase21 v4` |
| `sala_virtual.py` y `sala_motor.py` | No son una fase: la maqueta de la instalación en `/project1/SALA` (ver *Sala virtual*; v2: estar en la sala, un solo monitor; v3: el render de FASE1 sale por el Out TOP `out_render`; v4: la sala dibujada, el suelo del público con su retícula y la vista desde la entrada; v5: demos de público, la esfera a 1 m de la esquina, retícula en todo el suelo y público sin cabeza; v6: rendimiento, el color de la esfera por el TOP to CHOP `esfera_color` con descarga diferida, `luz_esfera` fuera de los render con `Luzesfera` 0 y el rótulo cada 15 fotogramas; v7: la esfera 3D con el centro del render (el planeta), sin el recuadro de la esfera en el monitor, sin el sub dibujado (rayas bajo la esfera) y fondo negro; v8: sin zona de la cámara, la cenital ve todo el suelo; v9: la esfera gira para que el planeta mire al centro de la sala, `Girosfera` lo ajusta; v10: la esfera lleva coordenadas de textura (Texture SOP) y, desde la v13, es una malla de polígonos (era una esfera primitiva de un punto y salía gris), así que se ve el render, y desde la v19 de frente sobre la cara que mira a la entrada (Script SOP `frente`), como se ve en FASE1; hasta la v18 se envolvía alrededor de la bola y salía estirado, de lado o del revés, y la miniatura de abajo a la derecha es la cámara cenital, más pequeña) | `sala_virtual v23`, `sala v12` |
| `fase7_erosion.py` | v15: relanzada sobre la fase 21, conserva la fila del micrófono (pad 9) de `perfiles_erosion`; v16: la página Fase7 con 12 parámetros en vez de 18 (ver «Página Fase7» en `MONTAJE_FASES_3_10.md`) | `fase7 v16` |
| `fase14_destructores.py` | v3: solo la autoprueba (cuenta también el pad 9 al repartir los pads en arañazos, cortes e impulsos) | `fase14 v3` |
| `fase22_camara.py` | La cámara cenital: página Fase22, `orbbec1` (o `kinect1` y `kinect_metros`, según `Sensor`), `sensor_cam`, `cornerpin1`, `fondo`, `altura_cam`, `sala_sim`, `fuente`, `alturas_sala` y `densidad`; el motor v81 trae la densidad por casilla, el mapeo sala → planeta y el sorteo de cada señal; comun v65, las autopruebas con `Activo` apagado; motor v92: `Sensor` (Femto Bolt o Kinect v2) | `fase22 v2` |
| `fase23_sala.py` | La luz de sala: página Fase23, `dmx_canales`, `dmx_valores` y `dmx_out`; el motor v82 trae el balance, el baño, el estroboscopio con su limitador de destellos, la noche del fin de ciclo y el colapso; comun v66 | `fase23 v1` |
| `docs/PLAN_V5.md` | El plan v5, renumerado a las fases 24–31, encima de la 23 | — |
| `pruebas/` | El TouchDesigner simulado sabe Audio Device In CHOP (sin dispositivo) y Switch CHOP y TOP con sus parámetros reales, y `numpyArray()` en un CHOP; `correr_fases.py` corre las fases 21 a 23 que existan y mete onsets en la sesión | — |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase21_microfono.py').read())
```

---

## FASE 21 · Micrófono

### Qué hace

El micrófono entra como un **pad 9 de erosión**: el motor ya sabía erosionar, cortar, iluminar la celda y escalar, así que la fase añade solo la detección y reutiliza todo lo demás.

- **El onset.** Cada fotograma, `mic_flujo` lee el bloque de audio que ha llegado desde el anterior (unas 735 muestras a 44,1 kHz y 60 fps) y el motor lo reparte en 16 bandas, de 200 Hz a 12 kHz, con la energía de cada una en dB. El **flujo espectral** es lo que sube cada banda respecto al máximo de los tres bloques anteriores, en decenas de dB por banda (1 = todas las bandas han subido 10 dB). Un sonido que empieza sube de golpe; un drone sostenido, no. Es un onset si el flujo pasa `Umbralonset` (0,6), han pasado 0,12 s desde el anterior (fijo desde la v3; antes `Refractariomic`) y no cae en los 0,15 s de un destello propio (los de la luz de sala, que apunta la fase 23; hasta entonces la lista está vacía).
- **El pad 9.** Un onset es un golpe de erosión del pad 9 (rol `micro`, gris cálido claro: D10) en la celda del objetivo, que se elige como la de los pads (`Objetivo`; desde la fase 22, la casilla más ocupada de la sala: D2). Baja `Reduccionmic` **escalones enteros** de ocupación (1), no notas (D3): la celda queda al principio del escalón de abajo; un satélite pierde uno de sus desbordes y una semilla se borra. Lo que no llega a un escalón queda en `ero_resto`, como un pad. Enciende la luz de la celda con su color y, desde la fase 14, **cuenta como arañazo** (D9): dos onsets en la misma zona dentro de `Ventanaescalada` pasos escalan en catástrofe.
- **El ruido de sala.** La energía (el flujo) de los onsets de los últimos 60 s se suma (fijo desde la v3; antes `Ventanaruido`); al pasar `Umbralcorte` (20) se abre un corte de `Profundidadmic` conchas (3) y radio 1 en la celda del último onset —el corte temático de la fase 16, que se une a los vecinos—, y la cuenta vuelve a cero.
- **No analiza la música.** El micrófono escucha al público: no hay Audio Spectrum CHOP ni reacción a lo que suena por los altavoces, solo a los sonidos que empiezan. Por eso hay que ponerlo lejos de los altavoces y subir `Umbralonset` hasta que el drone de la sala no dé ningún onset.

### Operadores (en `/project1/FASE1`)

```
mic_in (Audio Device In) ──► mic_flujo (Script CHOP) ──► motor
      (o, con Fuentemic = chop, el CHOP de Chopmic: el micrófono virtual de la sala)
```

| Operador | Qué es |
|---|---|
| `mic_in` | Audio Device In CHOP: el micrófono. El dispositivo se elige en su parámetro **Device**; el canal, con `Canalmic` (0, el primero) |
| `mic_flujo` | Script CHOP: lee el bloque de `mic_in` (o del CHOP de `Chopmic`, con `Fuentemic` = chop), el motor calcula el flujo con numpy y busca el onset. Saca los canales `flujo` y `onset` |

El motor recuece `mic_flujo` en cada fotograma desde `latido`: no hace falta que nada lo mire. Hasta la v3 había además `mic_sim` (la simulación) y `mic_fuente` (un Switch entre los dos); relanzar cualquier fase los borra y conecta `mic_flujo` a `mic_in`.

### Parámetros (página Fase21)

`Fuentemic` (micrófono / chop; micrófono) · `Chopmic` (con chop, la ruta del CHOP con el audio) · `Canalmic` 0 · `Umbralonset` 0,6 · `Reduccionmic` 1 escalón · `Umbralcorte` 20 (en 60 s) · `Profundidadmic` 3. Desde la v4, 7 parámetros: fuera `Simonset`, `Simruido` y `Simdrone`, y las opciones simulación y ambos de `Fuentemic` (pasan a micrófono, con un aviso `..`). Desde la v3: `Refractariomic` (0,12 s) y `Ventanaruido` (60 s) quedan fijos; relanzar cualquier fase los quita de un proyecto anterior y avisa con `..` si los habías cambiado. Cada cuánto abre un corte el ruido de la sala lo decide solo `Umbralcorte`

La fila 9 de `perfiles_erosion` es la del micrófono (`pad` 9, `modo` erosion, `tipo` y `rol` micro): de ella se leen el radio y la profundidad (0 y 0), pero la **reducción la da `Reduccionmic`**. La fila 9 de `colores_drum` es su color. Al relanzar, una tabla de 8 filas gana la novena sin perder lo editado, y relanzar la fase 7 ya no la borra.

`Umbralonset` y `Umbralcorte` llevan un valor provisional: se ajustan en la sala (ver *Pruebas pendientes*).

### Leyenda y `midi_log`

```
MICRO    microfono   flujo 0.12/0.60   onsets 12   ultimo flujo 0.71 celda 40 hace 1.2 s   ruido 5.3/20 en 60 s
MICRO    microfono (sin microfono)   flujo 0.00/0.60   onsets 0   ultimo -   ruido 0.0/20 en 60 s
```

Tras los onsets, `cortes N` si el ruido ha abierto alguno y `descartados N` si alguno cayó tras un destello. Cada onset deja una fila en `midi_log` (canal `mic`, la velocidad es el flujo):

```
MICRO onset flujo 0.71 celda 40
MICRO onset flujo 3.10 celda 41 ESCALADA incendio + corte por ruido de 3 conchas
```

### Probar sin micrófono

Con la sala virtual (desde la fase 21 v4, la única simulación):

1. `exec(open('C:/Users/DareDave/Downloads/est/sala_virtual.py').read())`. Con `Usarmic` (página Sala de `/project1/SALA`, encendido) pone `Fuentemic` = chop y `Chopmic` en su micrófono virtual.
2. `Palmada`: una palmada junto al micrófono, un onset; la celda del objetivo baja un escalón y se enciende en gris cálido. La línea `MICRO` cuenta el onset.
3. `Volumendrone`: el drone de los altavoces no da ningún onset (el flujo, en la leyenda, se queda bajo).
4. `Palmada` unas cuantas veces seguidas: el ruido de sala pasa de 20 y se abre un corte.
5. `Personas` y `Ruidopublico`: el público entero, con sus toses y palmadas.

Para volver al micrófono, `Fuentemic` = micrófono (o `Usarmic` apagado y relanzar la sala).

### Dónde poner el micrófono

- **Lejos de los aparatos**: de los altavoces (para que la música no dé onsets), del proyector y de su ventilador, y de los focos (la fase 23 trae un estroboscopio que hace clic).
- En el centro de la sala, alto (colgado o en un pie a 2–2,5 m), apuntando al público y no a la pantalla. Un micrófono de condensador omnidireccional o de superficie va bien; la interfaz, por USB.
- Con la sala vacía y el drone sonando, subir `Umbralonset` hasta que no salga ningún onset en 5 minutos; luego comprobar que una palmada, una tos y unos pasos sí salen.

### Autoprueba

Comprueba, con la señal sintética y sin micrófono:
- un clic da un onset; un drone sostenido de 5 s, ninguno; dos clics dentro de los 0,12 s de tiempo muerto, uno (separados, dos);
- un onset erosiona como el pad 9 en la celda que toca: con `Reduccionmic` 1,5 baja 1 escalón y deja 0,5 en `ero_resto`, y el siguiente baja 2; enciende su luz con su color;
- clics hasta `Umbralcorte` en 60 s: un corte de `Profundidadmic` en la celda del último onset y la cuenta a cero; por debajo del umbral, ningún corte; lo que sale de la ventana no cuenta;
- un onset justo tras un destello simulado se descarta;
- desde el nivel 14, dos onsets en la misma zona escalan (un incendio en un bosque);
- una tabla de perfiles de 8 filas, editada, gana el pad 9 sin perder nada, y el motor lee 9 pads;
- con `Fuentemic` = chop, un clic en un CHOP de prueba (que la autoprueba crea y borra) llega por `mic_flujo` hasta el motor; no quedan `mic_sim`, `mic_fuente` ni sus parámetros;
- la fila `MICRO` en `midi_log` y la línea `MICRO` de la leyenda.

---

### Decisiones tomadas en la fase 21

| Pregunta | Decisión |
|---|---|
| ¿Encima de qué fase? (D1) | De la 19 o de la 20 (POPs, sin fusionar): `require_base(21)` acepta las dos y lo dice en el informe. Nada del motor se activa con `Nivel` 20 |
| ¿Cuánto baja un onset? (D3) | Un escalón entero de ocupación (`Reduccionmic`, 1), no una nota: queda al principio del escalón de abajo |
| ¿Es un arañazo? (D9) | Sí: el pad 9 no corta ni es impulso, así que la fase 14 lo trata como arañazo (accidente y escalada) |
| ¿Su color? (D10) | Gris cálido claro (`#D8CCB8`): no es el blanco del SEQ1, ni el ámbar del SEQ2, ni el cian de las cicatrices |
| ¿Cómo se detecta? | Flujo espectral en 16 bandas en dB contra el máximo de los tres bloques anteriores, sin ventana (un clic al principio del bloque cuenta), calculado con numpy en el motor. Sin Audio Spectrum CHOP, para poder probarlo en el simulador |
| ¿Dónde va el objetivo? (D2) | Como los pads (`Objetivo`) hasta la fase 22; desde ella, la casilla más ocupada |
| ¿Dispositivo y canal? | El dispositivo, en el parámetro Device de `mic_in` (es un menú de los que hay en el ordenador); el canal, con `Canalmic` |
| ¿`Fuentemic` por defecto? | Hasta la v3, ambos, para que `Simonset` funcionara siempre. Desde la v4, micrófono: la simulación es la sala virtual, que pone chop ella misma |

---

### Cómo se ha probado

```
python3 pruebas/correr_fases.py        # base y fases 3 a 21 desde cero, sesión, relanzar y otra sesión
```

- **Desde cero**: `fase12_base.py` y las fases 3 a 19 y 21, todas con `AUTOPRUEBA OK`.
- **Sesión simulada** de 48 compases con SEQ1, SEQ2, batería y, con la sala virtual montada, una `Palmada` cada dos negras, fotograma a fotograma por su micrófono virtual y `mic_flujo` (hasta la v3, un `Simonset` por `mic_sim` y `mic_fuente`): los onsets llegan con los del público virtual y todas las expresiones se evalúan sin error.
- **Relanzar** las fases 3 a 21 sobre el proyecto en el nivel 21 (también la 7, que conserva la fila 9): todas OK, el mundo se conserva y otra sesión corre sin errores.
- **D1**: con `Nivel` 20, la fase 21 entra (`base: proyecto en la fase 20`); con 17, pide la 19.
- **Calibración del detector** con la señal sintética: un clic sobre silencio da un flujo de 3,8; sobre el drone, 1,0; el drone solo no pasa de 0,33 en 5 s; un ruido de sala constante, 0,13.

Lo que la simulación no puede comprobar: el audio real (el ruido de la sala, la reverberación, el drone verdadero), los nombres exactos de los parámetros del Audio Device In CHOP (el simulador usa los que conocemos: `active`, `driver`, `device`, `rate` y `bufferlength`; si alguno no existe, el informe lo dice con `..`), y que en TouchDesigner un `cook(force=True)` desde Python recueza la cadena en el mismo fotograma.

### Pruebas pendientes con el aparato

1. **Micrófono y drone.** Con el drone sonando y la sala vacía, subir `Umbralonset` hasta que no salga ningún onset en 5 minutos; luego, que una palmada, una tos y unos pasos sí salgan.
2. **Ruido acumulado.** Con una sala ruidosa, medir cuánto tarda en abrirse un corte y ajustar `Umbralcorte`.
3. **El dispositivo.** Que `mic_in` encuentra la interfaz (la línea `microfono:` del informe y la leyenda sin `(sin microfono)`), y que `Canalmic` es el canal del micrófono.
4. **La cadena en TouchDesigner.** Que `mic_flujo` saca `flujo` cada fotograma con el micrófono (míralo en su visor) y que, con la sala virtual, `Palmada` da un onset.
5. **Clic del estroboscopio** (cuando llegue la fase 23): que el detector no lo toma por público; si lo toma, ensanchar la ventana de descarte (`DESCARTE_DESTELLO` en el motor).

---

## FASE 22 · Cámara cenital (casilla probable)

```python
exec(open('C:/Users/DareDave/Downloads/est/fase22_camara.py').read())
```

### Qué hace

Una cámara de profundidad en el techo (Orbbec Femto Bolt, o una Kinect v2 para probar: `Sensor`) mide cuánta gente hay en cada casilla del suelo, y esa densidad inclina la probabilidad de que cada señal que llega al planeta actúe. El público no escribe: solo inclina dónde prende lo que ya llega. Es el componente `presencia` de la **Especificación TouchDesigner: casilla probable**, dentro de FASE1.

- **La fórmula.** `P(c) = C + (1 − C) k d(c)`: `C` = `Cuanto` (la probabilidad con la sala vacía, 0,5 como mucho, también en el código), `k` = `Pesocrear` o `Pesoerosion`, `d(c)` la densidad (0–1) de la casilla a la que mira el centro de la celda. Con `Activo` apagado, P = 1 y el mundo se comporta como antes.
- **El sorteo.** Cada nota constructora del SEQ1 o del SEQ2 (`crear`) y cada golpe de erosión u onset del micrófono (`erosionar`) pasa por un sorteo, una vez por evento y en su centro (un corte no sale agujereado). Si no sale, el evento se pierde: la leyenda `ULTIMA` y `midi_log` dicen `no prende`. No hay azar de software: sale del mapa logístico a r = 4 (pasado a uniforme), sembrado con la celda, el tipo y el contador de señales, así que la misma sala da el mismo resultado. El bombo y el tom (impulso) no se sortean: es una decisión abierta de la especificación.
- **La densidad.** De la imagen de alturas sobre el suelo: cuerpos entre `Alturamin` (0,8 m) y `Alturamax` (2,2 m), repartidos en un radio de `Desenfoque` (1 m), en casillas de `Tamcasilla` (0,5 m; `Anchosala` 5,4 × `Fondosala` 4,5 m: 11 × 9). Una casilla con `Ocupacionllena` (0,6) de su suelo ocupado está llena. Sube con `Subida` (2 s) y baja con `Bajada` (5 s).
- **El mapeo.** La pared de la pantalla es el norte (`Latnorte` 90°) y el fondo de la sala el sur (`Latsur` −90°); el ancho de la sala cubre `Anchoangular` (180°) alrededor de `Loncentral`, que es una expresión (`lon_central` del motor: 90° + el giro) para que la sala caiga siempre en la cara visible. La izquierda de la sala (mirando a la pantalla) cae a la izquierda de la cara visible; `Espejo` lo invierte.
- **El micrófono (D2).** Desde esta fase un onset cae en la celda que mira a la casilla con más densidad (sin nadie en la sala, donde los pads) y pasa por el sorteo como señal erosiva; si no prende, tampoco suma al ruido de sala.

### Operadores (en `/project1/FASE1`)

```
orbbec1 ───────────────────┐
kinect1 ─► kinect_metros ──┴─► sensor_cam ─► cornerpin1 ─┬─► altura_cam ─┐
                                                 fondo ───┘               ├─► fuente ─► alturas_sala ─► motor ─► densidad
                                        sala_personas ─► sala_sim ────────┘
```

| Operador | Qué es |
|---|---|
| `orbbec1` | Orbbec TOP: la Femto Bolt. Imagen de profundidad (32-bit float, en metros), NFOV binned 320 × 288, 30 fps. Activo solo con `Sensor` = Femto Bolt |
| `kinect1` | Kinect TOP: la Kinect v2. *Image* = Depth Point Cloud, sin remapear a color (512 × 424, XYZ en metros, 30 fps). Activo solo con `Sensor` = Kinect v2 |
| `kinect_metros` | GLSL TOP (`kinect_metros_pixel`): la Z de la nube de puntos (la distancia en metros) en el canal rojo, como la profundidad de la Femto; sin dato, 0 |
| `sensor_cam` | Switch TOP: `orbbec1` o `kinect_metros`, según `Sensor` |
| `cornerpin1` | Corner Pin TOP (de `sensor_cam`): endereza y recorta el suelo cubierto, con la pared de la pantalla arriba. Sus esquinas se ponen a mano en la calibración |
| `fondo` | Movie File In TOP: el suelo vacío (`Archivofondo`), que `Capturarfondo` graba de la salida de `cornerpin1` (con `TOP.save()`) |
| `altura_cam` | GLSL TOP (`altura_cam_pixel`): altura de cada píxel = suelo vacío − profundidad; los píxeles sin dato, 0 |
| `sala_personas`, `sala_sim` | La sala simulada: una tabla editable (x, y, altura en metros; x desde la izquierda, y desde la pantalla) y el Script TOP que dibuja cada persona como un disco de 25 cm de radio en la misma imagen de alturas |
| `fuente` | Switch TOP: la cámara o la sala simulada (`Fuente`) |
| `alturas_sala` | Resolution TOP: la imagen a 10 píxeles por casilla (110 × 90, unos 5 cm). Es lo único que pasa a Python |
| `densidad` | Script TOP: la densidad de cada casilla (11 × 9), para mirarla |

**Diferencia con la especificación.** Allí la máscara, el desenfoque, la rejilla y el suavizado van en la GPU (`mascara_cam`, `desenfoque`, `rejilla`, `retro`, `suavizado`) y solo la rejilla pasa a Python. Aquí la GPU llega hasta la imagen de **alturas** reducida, y lo demás lo hace el motor con numpy (menos de 0,5 ms, y solo 30 veces por segundo). Dos motivos: se prueba entero fuera de TouchDesigner (un GLSL TOP no se puede simular), y la fase 24 necesita esa misma imagen de alturas para contar cabezas, así que hay una sola lectura de la GPU en vez de dos. Los parámetros y la fórmula son los de la especificación; `marco`, `parexec` y `PresenciaExt` son `latido`, `pulsos` y el motor (`presencia_prob`, `presencia_sortear`). La sala simulada no tiene la persona que sigue al ratón: se editan las filas de `sala_personas`.

### Parámetros (página Fase22)

`Activo` · `Cuanto` 0,5 (tope 0,5) · `Pesocrear` 1 · `Pesoerosion` 1 · `Reiniciarcuentas` · `Fuente` (cámara / simulada) · `Sensor` (Femto Bolt / Kinect v2) · `Alturamin` 0,8 · `Alturamax` 2,2 · `Capturarfondo` · `Archivofondo` (`fondo_suelo.exr`) · `Anchosala` 5,4 · `Fondosala` 4,5 · `Tamcasilla` 0,5 · `Desenfoque` 1 · `Ocupacionllena` 0,6 · `Subida` 2 · `Bajada` 5 · `Loncentral` (expresión: el giro) · `Anchoangular` 180 · `Latnorte` 90 · `Latsur` −90 · `Espejo` · `Simcasilla` · `Simponer` · `Simquitar` · `Simvaciar`

Ojo: con `Activo` encendido y la sala vacía (o sin cámara) prende la mitad de las notas, también las de `Sembrar`. Para ensayar sin público como antes, `Activo` apagado. **Las autopruebas de todas las fases corren con `Activo` apagado** (comun v65) y devuelven tu valor al terminar.

### Leyenda

```
CAMARA   femto 30 fps   casillas 4/99   densidad max 0.82 (casilla 17 -> celda 40)   prendidas 312/598
CAMARA   femto (sin camara)   casillas 0/99   densidad max 0.00   prendidas 0/0
CAMARA   kinect 30 fps   casillas 2/99   densidad max 0.31 (casilla 27 -> celda 52)   prendidas 40/71
CAMARA   simulada   casillas 12/99   densidad max 0.09 (casilla 44 -> celda 37)   prendidas 5/9
```

Sin cámara quiere decir que el TOP del `Sensor` (`orbbec1` o `kinect1`) tiene un error o un aviso, o no da imagen: entonces el motor no lee `alturas_sala` (daría una imagen negra o la última), la densidad es 0 y la leyenda dice `(sin camara)`. El informe de la fase 22 copia la primera línea del error.

Las casillas se numeran por filas desde la pantalla: la 0 es la de la izquierda junto a la pantalla y la 98 la de la derecha al fondo.

### Probar sin cámara

1. `Fuente` = simulada. `Simcasilla` 5 (junto a la pantalla, en el centro) y `Simponer`: la leyenda dice `casilla 5 -> celda …`, una celda del norte de la cara visible. Con el desenfoque de 1 m, una persona sola da poca densidad (en torno a 0,1): la casilla se llena con varias personas cerca.
2. `Simcasilla` 45 (a media sala, a la izquierda) y `Simponer`: la celda está en la mitad izquierda del planeta que se ve. Con `Espejo`, en la derecha.
3. `Cuanto` 0 y `Sembrar` varias veces en una nota cuya celda no mira a nadie: `no prende` nunca; `Activo` apagado: prende siempre.
4. Teclea 0,8 en `Cuanto`: se queda en 0,5.
5. `Simquitar` y `Simvaciar`: la densidad baja en unos 5 s.

### Probar con una Kinect v2

1. Windows, el adaptador de la Kinect v2 a USB 3 y el **Kinect for Windows SDK 2.0**. Antes de abrir TouchDesigner, comprueba con *Kinect Studio* (o el *SDK Browser*) que da profundidad.
2. Relanza `fase22_camara.py`. En la página Fase22, `Sensor` = Kinect v2 y `Fuente` = Cámara. La leyenda debe decir `kinect 30 fps`; si dice `kinect (sin camara)`, mira el error de `kinect1`.
3. En `kinect1`: *Hardware Version* = Kinect 2 e *Image* = Depth Point Cloud, sin *Camera Remap* a color. Si el script no encuentra esos nombres lo dice con `..` y hay que ponerlos a mano. Mira `kinect_metros` con el visor: el suelo debe dar la altura de la cámara en metros, y una persona, en torno a 1,7 m menos.
4. **Lo que ve:** unos 70° × 60° y de 0,5 a 4,5 m. Colgada a 3 m del suelo cubre unos 4,2 × 3,5 m, así que baja `Anchosala` y `Fondosala` a lo que cubra de verdad (por ejemplo 4 × 3,5 m: 8 × 7 casillas).
5. Después, `cornerpin1` y `Capturarfondo` como con la Femto (abajo).

### Montaje y calibración

- **En casa:** la Femto Bolt a 2–3 m del suelo, mirando en vertical. **En sala:** a 3,5 m, con un cable USB-C activo, lejos del calor del proyector.
- **`cornerpin1`:** cuatro marcas en el suelo, en las esquinas del área cubierta; se ajustan sus esquinas hasta que las marcas caen en las de la imagen, con la pared de la pantalla arriba. `Anchosala` y `Fondosala`, medidos con cinta.
- **`Capturarfondo`** con la sala vacía, la proyección y las luces encendidas. Después, el suelo vacío no debe dar densidad durante varios minutos, y una mochila en el suelo tampoco.
- En `orbbec1`: *Image* = Depth y la profundidad NFOV binned (320 × 288); si el script no encuentra el nombre del parámetro lo dice con `..`.

### Autoprueba

- la rejilla (11 × 9); `Simponer` llega por la imagen de `sala_sim` (no escribiendo densidades): una persona junto a la pantalla, en el centro, da densidad en la fila 0 y la columna central;
- izquierda de la sala → mitad izquierda de la cara visible, derecha → derecha, y al revés con `Espejo`; `Loncentral` es la expresión del giro y, con el planeta girado, la misma casilla mira a otra celda;
- sala vacía: P = `Cuanto` en cualquier celda; una casilla llena y peso 1: P = 1 en sus celdas (0,75 con peso 0,5);
- `Cuanto` 0,8 se queda en 0,5, en el parámetro y en el código;
- 600 señales con la sala vacía: prenden entre el 45 y el 55 %, y la misma sala da lo mismo; con `Cuanto` 0,2, en torno al 20 %; con `Activo` apagado, todas; `Reiniciarcuentas`;
- una persona que entra: su casilla sube en torno a `Subida`; al irse, baja en torno a `Bajada`; una mochila (0,6 m) y una lámpara (2,6 m) no cuentan;
- las notas y los golpes de erosión pasan por el sorteo (una vez cada uno; el que no prende no quita nada); el bombo no;
- un onset cae en la celda de la casilla más densa; la línea `CAMARA`;
- `Fuente` = cámara con cada `Sensor`: sin aparato, densidad 0 y `femto (sin camara)` o `kinect (sin camara)`; con el aparato enchufado, la leyenda dice `femto 30 fps` o `kinect 30 fps`.

### Decisiones tomadas en la fase 22

| Pregunta | Decisión |
|---|---|
| ¿GPU o numpy? | La GPU hasta la imagen de alturas reducida; máscara, desenfoque, rejilla y suavizado en el motor (ver arriba) |
| ¿Qué se sortea? (D5) | Las notas de los SEQ y los golpes de los pads de erosión y del micrófono. El bombo y el tom, no (abierta en la especificación) |
| ¿Qué queda de una nota que no prende? | El SEQ sigue contando (la leyenda `SEQ1`, el reloj del ciclo, la biblioteca de patterns y el objetivo de los pads); en el mundo no deja nada |
| ¿Densidad de una celda? | La de la casilla a la que mira su centro, como en la especificación. Una celda fuera de la cara que mira a la sala tiene densidad 0 |
| ¿Sorteo sin azar? (D5) | Mapa logístico a r = 4, llevado a uniforme con `2/π · asin(√x)`; semilla: celda, tipo y contador de señales (`Reiniciarcuentas` lo pone a cero) |
| ¿Dónde vive el estado del sensor? | En el módulo del motor (`_SALA`), no en `W`: no es mundo y no se guarda con el `.toe` |

### Pruebas pendientes con el aparato

1. Los nombres de los parámetros del Orbbec TOP, el Kinect TOP, el Corner Pin TOP y el GLSL TOP (el simulador usa los que conocemos; lo que no entre, el informe lo dice con `..`).
2. Que `alturas_sala` da la altura en metros (míralo con el visor: una persona, en torno a 1,7).
3. Las pruebas «en sala» de la especificación: con el estroboscopio disparando y la sala vacía la densidad sigue a cero, y la cadena no baja los fotogramas del render.
4. `Subida`, `Bajada` y `Cuanto`, para que la presencia se note sin parpadear.

---

## FASE 23 · Luz de sala por DMX

```python
exec(open('C:/Users/DareDave/Downloads/est/fase23_sala.py').read())
```

### Qué hace

La sala se ilumina con el estado del planeta: cuanto más pesa la erosión, más luz, y cuando supera a la creación, estroboscopio. El motor calcula la luz y un solo CHOP la manda; la seguridad vive en el motor, no en el aparato. TouchDesigner sigue sin mandar nada al BeatStep.

- **El balance.** En una ventana de `Ventanabalance` segundos (30), la ocupación destruida entre la depositada, **en escalones de ocupación** (D6). La erosión suma la caja, los arañazos (pads 4 a 8), sus cortes, los accidentes que provocan y el micrófono (con su corte por ruido); la creación, las notas de los secuenciadores (con sus desbordes) y los pulsos del bombo y el tom. Lo que no baja un escalón entero no cuenta. Erosión sin creación en la ventana es erosión dominante. Las catástrofes que siguen ardiendo solas (fase 14) no cuentan.

| Estado | Balance | Luz de sala |
|---|---|---|
| Depósito | Menos de 0,5 | Casi a oscuras: ámbar tenue (4 %) que respira con cada nota depositada (hasta el 14 %) |
| Tensión | 0,5 a 1 | La intensidad sube (del 15 al 70 %) y vira del ámbar a blanco frío; cada onset del micrófono añade un pulso breve |
| Erosión dominante | Desde `Umbralestrobo` (1,0) hasta bajar de `Salidaestrobo` (0,8) | Estroboscopio blanco. Su frecuencia: `Maxhz` × (balance − `Salidaestrobo`) / (2 × (`Umbralestrobo` − `Salidaestrobo`)), con tope `Maxhz`: 1,5 Hz al entrar, 2,4 Hz con 1,12 y 3 Hz desde 1,2 |
| Fin de ciclo | Al enterrar | Un único destello blanco y oscuridad durante `Noche` segundos (4). El balance empieza de cero con el mundo nuevo (D7) |

- **Seguridad** (no son parámetros que se puedan saltar): como mucho **3 destellos en cualquier ventana de 1 s**, contando todos los de la sala en un solo limitador (`limitador_destellos`; `Maxhz` no pasa de 3 y con 0 no hay ninguno); el estroboscopio solo destella en blanco (r = g = b); el fin de ciclo lo apaga. Un destello **con prioridad** (el del fin de ciclo; el relámpago de la fase 30) que encuentra el limitador lleno espera al primer hueco, y el estroboscopio le cede ese destello. Cada destello queda apuntado para que el micrófono descarte su clic (0,15 s). Y un cartel a la entrada que avise de luces estroboscópicas (montaje, no código).
- **Un bucle que solo se rompe en silencio.** El estroboscopio provoca ruido, el ruido es erosión y la erosión mantiene el estroboscopio. Es lo que pide el marco: no se compensa.
- **Colapso (D8).** Con `Colapsoon` (apagado por defecto), `Maxerosion` segundos (15) seguidos con el balance por encima de 1 cierran el ciclo con el motivo `colapso`. `estancado` no es colapso. La fase 27 guarda el motivo como marca de la concha.
- **La tabla `ciclos`** gana la columna `balance` (el valor al cerrar); relanzar la añade a una tabla anterior.

### Operadores (en `/project1/FASE1`)

```
dmx_canales (Table DAT) ─► dmx_valores (Script CHOP) ─► dmx_out (DMX Out CHOP)
```

| Operador | Qué es |
|---|---|
| `dmx_canales` | Table DAT editable (`canal`, `funcion`, `foco`): qué canal DMX es cada cosa, porque los focos no están decididos. Relanzar no la pisa. Por defecto, 4 focos de baño de 4 canales (dimmer, rojo, verde, azul: 1 a 16) y el estroboscopio en el 17 |
| `dmx_valores` | Script CHOP: un canal por canal DMX (`c1`, `c2`…), hasta el mayor de la tabla, con su valor 0–255. El motor lo recuece en cada fotograma |
| `dmx_out` | DMX Out CHOP con `dmx_valores` de entrada (`Interfazdmx`: Art-Net o USB Pro; `Universodmx`) |

Funciones de `dmx_canales`: `bano_dimmer`, `bano_rojo`, `bano_verde`, `bano_azul` (un foco con dimmer aparte); `bano_r`, `bano_g`, `bano_b` (un foco RGB sin dimmer: el color ya lleva la intensidad); `estrobo` (255 durante un destello, que dura 0,05 s). Una función que no existe vale 0. La columna `foco` es solo para ti. La IP del nodo Art-Net (o el puerto de la interfaz USB) se pone en `dmx_out`.

`luz_sala(que, k)` del motor da lo mismo sin DMX (`'bano'`, `'destello'`, `'balance'`, `'estado'`, `'noche'`), para la sala virtual o un visor.

### Parámetros (página Fase23)

`Ventanabalance` 30 s · `Umbralestrobo` 1,0 · `Salidaestrobo` 0,8 (siempre por debajo de la entrada) · `Maxhz` 3 (tope duro) · `Noche` 4 s · `Colapsoon` (apagado) · `Maxerosion` 15 s · `Interfazdmx` (Art-Net / USB Pro) · `Universodmx` 0 · `Simbalance` −1 (−1: el balance real)

### Leyenda

```
SALA     balance 1.12 (30 s)   erosion dominante   estrobo 2.4 Hz   destellos 2/3   dmx artnet
SALA     balance 0.00 (30 s)   deposito   destellos 0/3   noche 2.3 s   sin dmx (sin dmx_out)
SALA     balance 1.50 (30 s, forzado)   erosion dominante   estrobo 3.0 Hz   destellos 3/3   colapso en 4.2 s   dmx artnet
```

### Probar sin público ni DMX

1. `Simbalance` 0,3: depósito. `Sembrar`: el ámbar respira (mira `dmx_valores`: `c1` sube y vuelve).
2. `Simbalance` 0,7: tensión, más luz y más fría. Con la sala virtual, `Palmada`: un pulso breve.
3. `Simbalance` 1,2 y luego 10: el estroboscopio; la leyenda nunca pasa de `destellos 3/3`. Baja a 0,9: sigue; a 0,79: se apaga (histéresis).
4. `Forzarciclo`: un destello y 4 s a oscuras (`noche` en la leyenda).
5. `Colapsoon` y `Simbalance` 1,2: a los 15 s, `fin de ciclo …: colapso` y una fila `colapso` en la tabla `ciclos`.
6. `Simbalance` −1 para volver al balance real.

### Montaje

- **USB-DMX** (una interfaz tipo Enttec USB Pro: `Interfazdmx` = USB Pro) o un nodo **Art-Net** (`Interfazdmx` = Art-Net, `Universodmx`; la IP, en `dmx_out`).
- Edita `dmx_canales` con el patch de tus aparatos. **El baño va al suelo y al público, nunca a la pantalla** (ni a la esfera); el estroboscopio sí puede alcanzarla.
- **El cartel de aviso** de luces estroboscópicas, a la entrada.
- El micrófono, lejos del estroboscopio (algunos hacen clic al disparar).

### Autoprueba

- `Simbalance` 0,3, 0,7 y 1,2: depósito, tensión y erosión dominante, con su luz; el ámbar respira con una nota y un onset da un pulso en tensión;
- histéresis: entra con 1,0 y no sale hasta bajar de 0,8;
- con el balance en 10 durante 10 s: nunca más de 3 destellos en 1 s y todos blancos; un destello con prioridad con el limitador lleno sale en el primer hueco, uno solo, y el estroboscopio cede el suyo; con `Maxhz` 0, ninguno;
- al enterrar: un único destello, el estroboscopio apagado y la sala a oscuras `Noche` s; después sigue;
- un onset justo después de un destello se descarta;
- el balance, en escalones: notas y bombo, creación; caja, arañazos y micrófono, erosión; antes de la fase 23 nada cuenta; erosión sin creación, dominante; lo que sale de la ventana no cuenta;
- colapso: con `Colapsoon`, a los 15 s de erosión dominante, y la noche empieza; apagado o en tensión, no; `estancado` no es colapso;
- la tabla `ciclos` con `balance`; `dmx_canales` → `dmx_valores` (17 canales; el estroboscopio a 255 en el destello); la línea `SALA`.

### Decisiones tomadas en la fase 23

| Pregunta | Decisión |
|---|---|
| ¿Cómo se cuenta el balance? (D6) | Por la ocupación total antes y después de cada evento: una nota o un pulso suman los escalones que gana el mundo; un golpe de erosión, los que pierde (con su corte y su accidente) |
| ¿Frecuencia del estroboscopio? | La de la tabla de arriba: reproduce el ejemplo del requerimiento (balance 1,12 → 2,4 Hz) |
| ¿Ventana de 1 s? | Cerrada: el cuarto destello sale más de 1 s después del primero. A `Maxhz` 3, el estroboscopio da 3 destellos cada 1,02 s |
| ¿Qué hace la prioridad? (P12) | El destello queda pendiente y sale en el primer hueco; el estroboscopio no destella mientras tanto y, al salir el pendiente, espera su periodo entero |
| ¿Y el balance al enterrar? | Se vacía: el estroboscopio no sigue con la erosión del mundo enterrado |
| ¿Dónde se comprueba el colapso? | En cada fotograma (`tick`), no en el reloj de compases: una sala ruidosa colapsa el mundo aunque el secuenciador esté parado |
| ¿La sala virtual? | Sus focos siguen con su `Modoluz`; `luz_sala()` queda listo para enlazarlos |

### Pruebas pendientes con el aparato

1. Los nombres del menú *Interface* del DMX Out CHOP (si `Interfazdmx` no entra, el informe lo dice con `..` y se elige a mano).
2. Que la interfaz y los focos responden a `dmx_canales`, y que el baño no lava la proyección.
3. **Medir en sala** que el estroboscopio nunca pasa de 3 destellos por segundo, y que su clic no da onsets (si los da, ensanchar `DESCARTE_DESTELLO` en el motor).
4. El bucle: con público, el estroboscopio provoca ruido; la sala en silencio lo apaga.

---

## Sala virtual (maqueta de la instalación)

*No es una fase: no cambia `Nivel` ni el mundo. Es una maqueta de la sala en `/project1/SALA`, al lado de FASE1, para probar la pieza como si estuviera montada.*

```python
exec(open('C:/Users/DareDave/Downloads/est/sala_virtual.py').read())
```

Habla con Estratos **por los mismos sitios que el hardware real**, así que la pieza no sabe si la sala es de verdad:

| Aparato real | En la maqueta | Entra o sale de FASE1 por |
|---|---|---|
| Micrófono | `audio_mic`: pasos, palmadas y toses de cada persona, el drone de los cuatro altavoces y el sub y el clic del estrobo, cada uno por 1/d y con su retardo (d / 343 m/s) | `Fuentemic` = chop, `Chopmic` = `/project1/SALA/audio_mic` (lo pone el script con `Usarmic`) |
| Cámara cenital | `vista_cenital` a 3,5 m (75° de campo, como la Femto Bolt en NFOV), `render_cenital` (320 × 288) y `profundidad` | La fase 22, cuando exista |
| Focos y estrobo | Una Light COMP por fila de la tabla (`luz_<nombre>`), con sombra; con `Modoluz` = prueba recorren en un minuto depósito, tensión y erosión dominante; con `Bruma`, su haz se ve en el aire | La fase 23 (DMX), cuando exista |
| Esfera de LEDs | Una esfera de 1 m con la imagen de `FASE1/render` (sale por el Out TOP `FASE1/out_render` y SALA la coge con el Select TOP `imagen_fase1`), que además ilumina la sala (`luz_esfera`, con el color medio de esa imagen) | — |

### La sala

- **8 × 6 m y 4 de alto** (`Ancho`, `Fondo`, `Alto`). Origen en el centro del suelo; mirando desde la entrada, x a la derecha y z hacia la entrada. La entrada, en el centro de la pared de delante; esa pared no se dibuja, para poder mirar dentro.
- **La cámara cenital ve todo el suelo** (v8): su ángulo se calcula para cubrir la sala entera desde donde está en la tabla (unos 100° en horizontal desde 3,5 m en una sala de 8 × 6). El público se para en cualquier sitio, lejos de las paredes, la esfera y el estrobo. Hasta la v7 había una zona de la cámara (`Zonaancho` × `Zonafondo`, 5,4 × 4,5 m) con tarima y borde turquesa; ya no. Ojo: una Femto Bolt en NFOV ve unos 75 × 65°; desde 3,5 m no cubre 8 × 6 m.
- **La sala dibujada** (v4, geometría `lineas` con Constant MAT, se ve aunque la sala esté a oscuras): las doce aristas, el umbral de la puerta, una retícula de 1 m en las tres paredes y una de 0,5 m en todo el suelo (v5; en la v4 solo cubría el suelo del público), para leer la perspectiva.
- **La tabla `equipos`** (nombre, tipo, posición, a dónde apunta y tamaño o ángulo del cono) es editable y relanzar no la pisa; `Recolocar` la rehace con las medidas de ahora. Un foco más es una fila más (y relanzar, para crear su luz). Por defecto:

| Equipo | Dónde |
|---|---|
| Esfera de LEDs, 1 m | Esquina del fondo a la izquierda, a 1 m de cada pared (v5), sobre una peana de 0,8 m (centro a 1,3 m) |
| Subwoofer | Dentro de la peana, bajo la esfera |
| 4 altavoces | Colgados a 3 m en las cuatro esquinas, apuntando al centro |
| Micrófono | Colgado a 3 m, hacia el centro (1, 1), a más de 3 m del estrobo y del sub |
| Cámara | Cenital, a 3,5 m en el centro |
| 4 focos de baño | Colgados a 3,6 m, conos de 50°. Dos acompañan a la esfera (a su lado y detrás), apuntando al suelo y al público, nunca a ella |
| Estroboscopio | En el suelo junto a la esfera, cono de 100°, hacia la sala |

La especificación no fija cuántos focos hay («los focos no están decididos»): los 4 + 1 son el punto de partida.

### Personas y ruido

`Personas` (6) entran por la puerta cada `Llegada` s (8), pasean por 3 a 7 puntos parándose de 3 a 12 s en cada uno, salen y vuelven al rato, sin azar (un hash de la persona y del tramo) y lejos de la esfera y del estrobo. Hacen ruido: pisadas al andar (unos 20 dB por debajo de una palmada: solo cuentan las de cerca del micro), y palmadas o toses (`Ruidopublico` por segundo y persona, 0,05; `Reaccion` veces más con el estrobo encendido, 3). En 5 minutos simulados con 6 personas: 48 de 52 palmadas, 27 de 46 toses y 16 de 704 pisadas dan onset, y unos pocos los da el clic del estrobo.

### Parámetros (página Sala de `/project1/SALA`)

`Activa` · `Ancho` 8 · `Fondo` 6 · `Alto` 4 · `Recolocar` · `Personas` 6 · `Llegada` 8 s · `Ruidopublico` 0,05 · `Reaccion` 3 · `Volumendrone` 0,5 · `Palmada` · `Reiniciarsala` · `Usarmic` · `Modoluz` (apagada / prueba) · `Hzprueba` 2,5 (tope 3) · `Luzcasa` 0,06 (hasta la v1, 0,25) · `Bruma` 0,5 (v2) · `Demo` (paseo / grupo / llena / goteo / vacía; v5) · `Luzesfera` 0 (v5) · `Espejosfera` y `Volteosfera` apagados (v16; desde la v19, con la imagen de frente, no hacen falta) · `Inclinasfera` 0° (v18: grados hacia arriba sobre la inclinación automática hacia la cámara de la entrada) · `Girosfera` 0° (v9: ajuste a mano del giro de la esfera; a 0, el planeta mira a la cámara de la entrada desde la v14, antes al centro de la sala) · `Vista` (visitante / entrada / órbita / cenital; v2; por defecto entrada desde la v4) · `Orbita` 30° · `Distancia` 11 m · `Alturavista` 5 m (las tres, solo con `Vista` = órbita)

### Cómo mirarla (v2: un solo monitor)

Abre **`salida_sala`** (o el Null `monitor_sala`): una sola imagen de 1280 × 720 con todo. No hace falta abrir ningún otro render.

```
┌───────────────────────────────────────────────────────────┐
│ SALA 8x6 m   personas 5/6   luz tension ...  ┌──────────┐ │
│ LUZ tension (40%)  sube y vira a blanco frio │ la esfera│ │
│ MICRO onsets 12   flujo 0.31                 └──────────┘ │
│                                                           │
│          la sala desde la Vista (en grande)               │
│                                              ┌──────────┐ │
│                                              │  plano   │ │
│                                              └──────────┘ │
└───────────────────────────────────────────────────────────┘
```

- **En grande, la sala desde `Vista`:**
  - *entrada* (por defecto desde la v4): desde detrás de la puerta (2,2 m) y a 2,8 m de alto, mirando al fondo: el suelo del público entero con su retícula, la esfera en su esquina del fondo y las paredes en perspectiva.
  - *visitante*: los ojos de un visitante, a 1,65 m, que pasea despacio entre el público (6 puntos de la sala, se para 9 s en cada uno) mirando la esfera. Es la vista para sentir la sala.
  - *órbita*: desde fuera, como la vista libre de la v1 (`Orbita`, `Distancia`, `Alturavista`).
  - *cenital*: lo que ve la cámara del techo.
- (Hasta la v6, arriba a la derecha, lo que muestra la esfera. Desde la v7 no se pone: parecía la esfera metida en la esquina de la sala, y la esfera 3D ya lo enseña.)
- **Abajo a la derecha**, lo que ve la cámara cenital (200 × 180, v10): toda la planta de la sala, con su propia luz para que se lea; dónde está el público. Hasta la v9 era un plano ortográfico aparte, más grande (320 × 240).
- **Arriba a la izquierda**, el rótulo: la sala y el público, el estado de la luz (depósito, tensión o erosión, y cuánto le queda) con la bruma y la vista, y los onsets que cuenta FASE1.

**La luz, como en la sala.** La sala está a oscuras (`Luzcasa` 0,06). Los focos y el estrobo dan sombra al público. Con `Bruma` (0,5) cada haz se ve en el aire: un cono del color de su luz que va del aparato al suelo y se apaga con él (0 = aire limpio). La esfera es una luz más: ilumina lo que tiene cerca (hasta unos 6 m) con el color medio de lo que muestra, con `Luzesfera` (v5: 0 por defecto, porque dejaba una mancha gris en la pared). El suelo brilla un poco, así que refleja la esfera y los focos. El público es un tronco de ropa oscura, de la altura de cada persona (v5: sin cabeza): a contraluz se lee como personas.

**Demos de visita (v5, `Demo`).** *paseo*: llegan de uno en uno cada `Llegada` s, pasean, se paran en el suelo del público y se van. *grupo*: entran juntos en fila, hacen corro ante la esfera (a 2,2 m), se quedan casi un minuto y salen juntos; cada 90 s. *llena*: la sala se llena deprisa y el público se queda casi quieto, con algún paso corto. *goteo*: de uno en uno, cada 35 s; van a la esfera, miran y se van. *vacía*: nadie.

`render_cenital` (320 × 288) y `profundidad` siguen ahí, porque son la entrada de la cámara para la fase 22, pero no hace falta mirarlos. `Palmada` da una palmada junto a la persona más cerca del micro, y el rótulo cuenta el onset.

### Autoprueba

- los equipos (esfera en una esquina del fondo, sub debajo, 4 altavoces colgados, micro en lo alto, cámara a 3,5 m, 4 focos y 1 estrobo); ningún foco de baño apunta a la esfera; el micro, a más de 3 m del estrobo y del sub; una luz por foco y estrobo;
- las personas entran por la puerta, pasean y se paran dentro de la sala y lejos de la esfera; la misma sala da la misma historia;
- el drone de los altavoces y el sub no da onsets en 5 s; una palmada junto al micro da un onset y más flujo que una al otro lado de la sala; el sonido llega con su retardo;
- la luz de prueba: el estrobo solo en blanco y como mucho 3 destellos en cualquier ventana de 1 s; depósito en ámbar tenue y tensión hacia blanco frío;
- `render_cenital` y `profundidad`; la esfera con la imagen de FASE1;
- (v2) el monitor (`salida_sala` ← `monitor_sala`, con el plano, la esfera y el rótulo); el visitante pasea dentro de la sala, lejos de la esfera y del estrobo, sin correr, con los ojos a 1,65 m mirando la esfera; la órbita, como la vista libre de antes; una cabeza por persona; un haz por aparato encendido, del color de su luz y hasta el suelo, y ninguno sin bruma o con la luz apagada; `luz_esfera` en su sitio y con un color válido; el rótulo con la sala, la luz y la vista;
- `Palmada`: FASE1 la oye por `audio_mic` y cuenta un onset.

### Lo que la maqueta no es

- **La esfera real pide un mapa equirectangular 2:1** por HDMI (especificación técnica). Estratos aún no lo saca: renderiza una cámara mirando al globo, que vale para un proyector. En la maqueta, esa imagen envuelve la esfera. Sacar el mapa equirectangular (un Render TOP en cubemap y su conversión) es trabajo de Estratos, no de la maqueta, y no está en ninguna fase del plan.
- **Sin reverberación ni ruido de fondo de la sala**: por eso `Umbralonset` y `Umbralcorte` se siguen ajustando en la sala real.
- **La cámara pone «la pared de la pantalla» al norte** (especificación «casilla probable»). Con la esfera en una esquina no hay pared de pantalla: queda por decidir qué lado de la zona es el norte del planeta (lo natural, el del fondo, donde está la esfera).
- En el simulador de pruebas solo se comprueba que todo se monta y calcula; cómo se ve, solo en TouchDesigner. En la v2 hay cuatro ajustes que el simulador no conoce y que hay que mirar al lanzarla en TouchDesigner (si alguno no entra, el informe lo dice con `..` y qué poner a mano): la mezcla aditiva de `mat_haz`, la sombra de los focos (*Shadow Type*), la atenuación de `luz_esfera` y la colocación del plano y de la esfera en las esquinas del monitor (Over TOP: *Fixed Layer* = Input 2, *Prefit* = Native Resolution, *Justify*).
- **La bruma es un truco**: un cono aditivo por haz, no humo de verdad. Se ve bien desde dentro; desde muy cerca de un foco el cono se nota.
