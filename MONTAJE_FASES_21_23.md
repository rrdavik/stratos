# Estratos · Montaje
## Fases 21 a 23: micrófono, cámara y luz de sala

*Continúa `MONTAJE_FASES_11_18.md` (que llega a la fase 19). Referencias: los docs **Requerimiento v4 · micrófono, cámara y DMX** y **Tareas técnicas v4 · micrófono, cámara y DMX** (decisiones D1 a D10, cerradas el 28 de octubre de 2026). Las reglas de siempre siguen valiendo: un script por fase, encima de lo anterior, con su versión en la primera línea del informe y una AUTOPRUEBA al final. Las fases se hacen en línea: cada una se revisa antes de empezar la siguiente. Esta versión del montaje trae la **fase 21**; la 22 y la 23 se añadirán aquí.*

---

### Estado en una frase

La sala entra en la pieza: desde la fase 21 el micrófono escucha al público, y cada sonido que empieza (una palmada, una tos, unos pasos) es un golpe de erosión de un pad 9 que no está en la batería; si la sala hace mucho ruido durante un rato, se abre un corte.

---

### Archivos

| Archivo | Para qué | Versión |
|---|---|---|
| `estratos_motor.py` | La v55 añade el micrófono: flujo espectral, onsets, el pad 9 de erosión (baja escalones enteros), el corte por ruido de sala y la línea `MICRO` | `motor v55` |
| `estratos_comun.py` | La v37: `require_base(21)` acepta un proyecto en la fase 19 o en la 20 (los POPs, sin fusionar: D1) y el informe dice cuál encontró | `comun v37` |
| `fase21_microfono.py` | El micrófono: página Fase21, `mic_in`, `mic_sim`, `mic_fuente` y `mic_flujo`, la fila del pad 9 en `perfiles_erosion` y `colores_drum` | `fase21 v1` |
| `fase7_erosion.py` | v15: relanzada sobre la fase 21, conserva la fila del micrófono (pad 9) de `perfiles_erosion` | `fase7 v15` |
| `fase14_destructores.py` | v3: solo la autoprueba (cuenta también el pad 9 al repartir los pads en arañazos, cortes e impulsos) | `fase14 v3` |
| `claude/PLAN_V5.md` | El plan v5, renumerado a las fases 24–31, encima de la 23 | — |
| `pruebas/` | El TouchDesigner simulado sabe Audio Device In CHOP (sin dispositivo) y Switch CHOP y TOP con sus parámetros reales, y `numpyArray()` en un CHOP; `correr_fases.py` corre las fases 21 a 23 que existan y mete onsets en la sesión | — |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase21_microfono.py').read())
```

---

## FASE 21 · Micrófono

### Qué hace

El micrófono entra como un **pad 9 de erosión**: el motor ya sabía erosionar, cortar, iluminar la celda y escalar, así que la fase añade solo la detección y reutiliza todo lo demás.

- **El onset.** Cada fotograma, `mic_flujo` lee el bloque de audio que ha llegado desde el anterior (unas 735 muestras a 44,1 kHz y 60 fps) y el motor lo reparte en 16 bandas, de 200 Hz a 12 kHz, con la energía de cada una en dB. El **flujo espectral** es lo que sube cada banda respecto al máximo de los tres bloques anteriores, en decenas de dB por banda (1 = todas las bandas han subido 10 dB). Un sonido que empieza sube de golpe; un drone sostenido, no. Es un onset si el flujo pasa `Umbralonset` (0,6), han pasado `Refractariomic` s (0,12) desde el anterior y no cae en los 0,15 s de un destello propio (los de la luz de sala, que apunta la fase 23; hasta entonces la lista está vacía).
- **El pad 9.** Un onset es un golpe de erosión del pad 9 (rol `micro`, gris cálido claro: D10) en la celda del objetivo, que se elige como la de los pads (`Objetivo`; desde la fase 22, la casilla más ocupada de la sala: D2). Baja `Reduccionmic` **escalones enteros** de ocupación (1), no notas (D3): la celda queda al principio del escalón de abajo; un satélite pierde uno de sus desbordes y una semilla se borra. Lo que no llega a un escalón queda en `ero_resto`, como un pad. Enciende la luz de la celda con su color y, desde la fase 14, **cuenta como arañazo** (D9): dos onsets en la misma zona dentro de `Ventanaescalada` pasos escalan en catástrofe.
- **El ruido de sala.** La energía (el flujo) de los onsets de los últimos `Ventanaruido` s (60) se suma; al pasar `Umbralcorte` (20) se abre un corte de `Profundidadmic` conchas (3) y radio 1 en la celda del último onset —el corte temático de la fase 16, que se une a los vecinos—, y la cuenta vuelve a cero.
- **No analiza la música.** El micrófono escucha al público: no hay Audio Spectrum CHOP ni reacción a lo que suena por los altavoces, solo a los sonidos que empiezan. Por eso hay que ponerlo lejos de los altavoces y subir `Umbralonset` hasta que el drone de la sala no dé ningún onset.

### Operadores (en `/project1/FASE1`)

```
mic_in (Audio Device In) ──┬─────────────────► mic_fuente (Switch) ──► mic_flujo (Script CHOP) ──► motor
                           └──► mic_sim (Script CHOP) ──┘
```

| Operador | Qué es |
|---|---|
| `mic_in` | Audio Device In CHOP: el micrófono. El dispositivo se elige en su parámetro **Device**; el canal, con `Canalmic` (0, el primero) |
| `mic_sim` | Script CHOP: clic (`Simonset`), ruido (`Simruido`) y drone (`Simdrone`) sintéticos, sin azar; con `Fuentemic` = ambos, sumados a `mic_in` |
| `mic_fuente` | Switch CHOP: `mic_in` con `Fuentemic` = micrófono; `mic_sim` con simulación o ambos |
| `mic_flujo` | Script CHOP: lee el bloque de `mic_fuente`, el motor calcula el flujo con numpy y busca el onset. Saca los canales `flujo` y `onset` |

El motor recuece `mic_sim` y `mic_flujo` en cada fotograma desde `latido`: no hace falta que nada los mire.

### Parámetros (página Fase21)

`Fuentemic` (micrófono / simulación / ambos; ambos) · `Canalmic` 0 · `Umbralonset` 0,6 · `Refractariomic` 0,12 s · `Reduccionmic` 1 escalón · `Ventanaruido` 60 s · `Umbralcorte` 20 · `Profundidadmic` 3 · `Simonset` · `Simruido` 0 · `Simdrone` apagado

La fila 9 de `perfiles_erosion` es la del micrófono (`pad` 9, `modo` erosion, `tipo` y `rol` micro): de ella se leen el radio y la profundidad (0 y 0), pero la **reducción la da `Reduccionmic`**. La fila 9 de `colores_drum` es su color. Al relanzar, una tabla de 8 filas gana la novena sin perder lo editado, y relanzar la fase 7 ya no la borra.

`Umbralonset` y `Umbralcorte` llevan un valor provisional: se ajustan en la sala (ver *Pruebas pendientes*).

### Leyenda y `midi_log`

```
MICRO    ambos   flujo 0.12/0.60   onsets 12   ultimo flujo 0.71 celda 40 hace 1.2 s   ruido 5.3/20 en 60 s
MICRO    microfono (sin microfono)   flujo 0.00/0.60   onsets 0   ultimo -   ruido 0.0/20 en 60 s
```

Tras los onsets, `cortes N` si el ruido ha abierto alguno y `descartados N` si alguno cayó tras un destello. Cada onset deja una fila en `midi_log` (canal `mic`, la velocidad es el flujo):

```
MICRO onset flujo 0.71 celda 40
MICRO onset flujo 3.10 celda 41 ESCALADA incendio + corte por ruido de 3 conchas
```

### Probar sin micrófono

1. `Fuentemic` = simulación (o ambos, el valor por defecto).
2. `Simonset`: un clic, un onset; la celda del objetivo baja un escalón y se enciende en gris cálido. La línea `MICRO` cuenta el onset.
3. `Simdrone`: un drone sostenido de 110 Hz que no da ningún onset (el flujo, en la leyenda, se queda bajo).
4. `Simonset` unas cuantas veces seguidas (unas seis, con clics limpios): el ruido de sala pasa de 20 y se abre un corte.
5. `Simruido` sube un ruido de sala de fondo: con él, los clics se oyen menos y dan menos flujo.

### Dónde poner el micrófono

- **Lejos de los aparatos**: de los altavoces (para que la música no dé onsets), del proyector y de su ventilador, y de los focos (la fase 23 trae un estroboscopio que hace clic).
- En el centro de la sala, alto (colgado o en un pie a 2–2,5 m), apuntando al público y no a la pantalla. Un micrófono de condensador omnidireccional o de superficie va bien; la interfaz, por USB.
- Con la sala vacía y el drone sonando, subir `Umbralonset` hasta que no salga ningún onset en 5 minutos; luego comprobar que una palmada, una tos y unos pasos sí salen.

### Autoprueba

Comprueba, con la señal sintética y sin micrófono:
- un clic da un onset; un drone sostenido de 5 s, ninguno; dos clics dentro de `Refractariomic`, uno (separados, dos);
- un onset erosiona como el pad 9 en la celda que toca: con `Reduccionmic` 1,5 baja 1 escalón y deja 0,5 en `ero_resto`, y el siguiente baja 2; enciende su luz con su color;
- clics hasta `Umbralcorte` en `Ventanaruido`: un corte de `Profundidadmic` en la celda del último onset y la cuenta a cero; por debajo del umbral, ningún corte; lo que sale de la ventana no cuenta;
- un onset justo tras un destello simulado se descarta;
- desde el nivel 14, dos onsets en la misma zona escalan (un incendio en un bosque);
- una tabla de perfiles de 8 filas, editada, gana el pad 9 sin perder nada, y el motor lee 9 pads;
- `Simonset` llega por `mic_sim`, `mic_fuente` y `mic_flujo` hasta el motor;
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
| ¿Por qué `Fuentemic` = ambos por defecto? | Para que `Simonset` funcione siempre, con o sin micrófono |

---

### Cómo se ha probado

```
python3 pruebas/correr_fases.py        # base y fases 3 a 21 desde cero, sesión, relanzar y otra sesión
```

- **Desde cero**: `fase12_base.py` y las fases 3 a 19 y 21, todas con `AUTOPRUEBA OK`.
- **Sesión simulada** de 48 compases con SEQ1, SEQ2, batería y un `Simonset` cada dos negras, fotograma a fotograma por la cadena `mic_sim` → `mic_fuente` → `mic_flujo`: los 96 clics dan 96 onsets y todas las expresiones se evalúan sin error.
- **Relanzar** las fases 3 a 21 sobre el proyecto en el nivel 21 (también la 7, que conserva la fila 9): todas OK, el mundo se conserva y otra sesión corre sin errores.
- **D1**: con `Nivel` 20, la fase 21 entra (`base: proyecto en la fase 20`); con 17, pide la 19.
- **Calibración del detector** con la señal sintética: un clic sobre silencio da un flujo de 3,8; sobre el drone, 1,0; el drone solo no pasa de 0,33 en 5 s; un ruido de sala constante, 0,13.

Lo que la simulación no puede comprobar: el audio real (el ruido de la sala, la reverberación, el drone verdadero), los nombres exactos de los parámetros del Audio Device In CHOP y del Switch CHOP (el simulador usa los que conocemos: `active`, `driver`, `device`, `rate`, `bufferlength` e `index`; si alguno no existe, el informe lo dice con `..`), y que en TouchDesigner un `cook(force=True)` desde Python recueza la cadena en el mismo fotograma.

### Pruebas pendientes con el aparato

1. **Micrófono y drone.** Con el drone sonando y la sala vacía, subir `Umbralonset` hasta que no salga ningún onset en 5 minutos; luego, que una palmada, una tos y unos pasos sí salgan.
2. **Ruido acumulado.** Con una sala ruidosa, medir cuánto tarda en abrirse un corte y ajustar `Umbralcorte`.
3. **El dispositivo.** Que `mic_in` encuentra la interfaz (la línea `microfono:` del informe y la leyenda sin `(sin microfono)`), y que `Canalmic` es el canal del micrófono.
4. **La cadena en TouchDesigner.** Que `mic_flujo` saca `flujo` cada fotograma con el micrófono (míralo en su visor) y que `Simonset` con `Fuentemic` = simulación da un onset.
5. **Clic del estroboscopio** (cuando llegue la fase 23): que el detector no lo toma por público; si lo toma, ensanchar la ventana de descarte (`DESCARTE_DESTELLO` en el motor).
