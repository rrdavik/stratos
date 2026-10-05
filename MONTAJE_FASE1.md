# Estratos · Montaje
## Fases 1 y 2: el núcleo que gira al tempo del BeatStep, y el SEQ1 marcando sus notas

---

### Estado actual en una frase

Una esfera con una retícula de 96 celdas gira al tempo del proyecto, que marca el BeatStep Pro, y cada nota del SEQ1 enciende una baliza cian que pulsa sobre la celda que le corresponde.

---

### Archivos que importan

| Archivo | Para qué | Cuándo ejecutarlo |
|---|---|---|
| `fase1_tempo_beatstep.py` | Construye la fase 1 (se identifica como `fase1 v2`) | Primero |
| `fase2_seq1_baliza.py` | Añade la fase 2 encima (se identifica como `fase2 v3`) | Después de la fase 1 |
| `fix_render_fase2.py` | Repara el render si aplicaste la fase 2 anterior (`fase2 v2`) | Solo en ese caso |
| `contador_master_beat.py` | Referencia para midicontrolx: cómo contar pulsos de reloj | No se ejecuta en FASE1 |
| `MONTAJE_FASE1.md` | Este documento | — |

Todo se ejecuta desde el Textport (Alt+T):

```python
exec(open('C:/Users/DareDave/Downloads/estratosp/fase1_tempo_beatstep.py').read())
exec(open('C:/Users/DareDave/Downloads/estratosp/fase2_seq1_baliza.py').read())
```

La primera línea de cada informe dice qué versión se está ejecutando. Si no coincide con la de la tabla, se está ejecutando otro archivo (pasa a menudo con las descargas repetidas: el navegador guarda la nueva como `archivo (1).py`).

El resto de archivos de la carpeta son intentos anteriores y quedan obsoletos (ver el último apartado).

---

### Cómo fluye el tiempo

```
BeatStep Pro  ──reloj MIDI──>  midicontrolx  ──escribe──>  tempo del proyecto
                                                                  │
                                                                  └──lee──>  FASE1 (nodo ritmo)
                                                                                  │
                                                                                  └──>  giro del planeta
```

Una sola fuente de verdad. El BeatStep es el maestro, midicontrolx traduce su reloj a un tempo y FASE1 lo lee. FASE1 no tiene parámetro `Bpm`, no lee el reloj MIDI, no escribe tempo y no rebobina nada.

### Qué necesita de midicontrolx

**Que escriba el tempo del BeatStep en el componente de tiempo del proyecto.** Normalmente `/local/time`; el informe de la fase 1 te dice exactamente cuál lee FASE1.

```python
op('/local/time').tempo = bpm
```

Si midicontrolx escribía antes en el parámetro `Bpm` de FASE1, hay que cambiar ese destino: el parámetro ya no existe.

Opcional: si midicontrolx arranca y detiene la línea de tiempo del proyecto con el PLAY y el STOP del BeatStep, el planeta se para y arranca con ella.

Sobre `master_beat`: si lo construye contando pulsos de reloj, está enganchado en fase y no puede derivar. `contador_master_beat.py` recoge cómo hacerlo bien (6 pulsos por semicorchea, el primer pulso tras START es la posición 0, no contar en STOP, respetar Song Position Pointer). Las fases 1 y 2 no usan `master_beat`.

---

## FASE 1 · El núcleo que gira

### Qué construye

Todo dentro de `/project1/FASE1`:

| Nodo | Qué es | Para qué sirve |
|---|---|---|
| `ritmo` | Text DAT (módulo) | Lee el tempo del proyecto y acumula el giro. Toda la lógica de tiempo vive aquí. |
| `reticula_callbacks` | Text DAT | Calcula la posición de las 96 celdas. |
| `reticula_chop` | Script CHOP | Publica esas posiciones para instanciar los marcadores. |
| `nucleo` | Geometry COMP | La esfera (SOP `esfera` **dentro**). |
| `reticula` | Geometry COMP | Los 96 marcadores instanciados (SOP `marcador` **dentro**). |
| `mat_nucleo`, `mat_reticula` | Materiales | Gris visible para la esfera, blanco para los marcadores. |
| `camara`, `luz_principal`, `luz_relleno` | Cámara y luces | Encuadre fijo, luz cenital fría y relleno azulado. |
| `render` | Render TOP | 1280×720 (límite de la licencia no comercial). |
| `rotulo`, `con_rotulo` | Text TOP y Over TOP | La leyenda superpuesta a la imagen. |
| `salida` | Out TOP | Lo que miras. |
| `LEEME` | Text DAT | Resumen dentro del proyecto. |

### Parámetros (página Fase1)

| Parámetro | Qué hace | Por defecto |
|---|---|---|
| `Barsperturn` | Compases por vuelta | 8 |
| `Tilt` | Inclinación del eje, en grados | 20 |
| `Showgrid` | Muestra u oculta la retícula | Activado |
| `Pausa` | Congela el giro donde está | Desactivado |

### Cómo se calcula la vuelta

```
segundos por vuelta = compases por vuelta × tiempos por compás × 60 / BPM
```

Los tiempos por compás salen de la firma del proyecto (4 en un 4/4). Con 8 compases a 120 BPM: **16 s por vuelta**; a 90 BPM, 21,3 s; a 140 BPM, 13,7 s.

### Por qué el giro se acumula

Calcular el ángulo como *tiempo × tempo* hace saltar el planeta cada vez que cambia el tempo, porque el producto entero se recalcula con el tempo nuevo. Ahora el ángulo se suma fotograma a fotograma: si el tempo cambia, cambia la velocidad, no la posición. Comprobado con saltos bruscos de 120 a 90 y de 90 a 140 BPM: velocidad exacta en cada tramo, ningún salto.

El planeta se queda quieto con `Pausa` o con la línea de tiempo del proyecto parada.

### La retícula: el teclado sobre la esfera

12 meridianos × 8 bandas de latitud = 96 celdas:

- la **clase de nota** (do, do#, re...) elige el meridiano;
- la **octava** elige la banda.

| Nota | Meridiano | Banda |
|---|---|---|
| do4 (60) | 0 | 5 |
| do#4 (61) | 1 | 5 |
| mi4 (64) | 4 | 5 |
| sol4 (67) | 7 | 5 |
| do5 (72) | 0 | 6 |

Una escala ascendente da la vuelta al planeta y sube una banda por octava. La lógica está en `cell_normal()` y `note_to_cell()`, en `reticula_callbacks`; la fase 2 usa exactamente las mismas.

### Tu FASE1 anterior

El script de la fase 1 no borra nada. Si ya existía `/project1/FASE1`, la renombra a `FASE1_anterior`. Si dentro no había midicontrolx ni `master_beat`, además la apaga para que no dé errores; si los había, la deja funcionando y avisa.

---

## FASE 2 · El SEQ1 marca sus notas

### Qué hace

Cada nota que toca el SEQ1 del BeatStep (canal MIDI 13):

- lleva la **baliza** a la celda de esa nota;
- la hace **pulsar**: crece de golpe y se apaga enseguida, en **cada** nota, también si se repite la misma. Un pattern que repite nota se ve como golpes, no como una luz fija;
- la escribe en la **leyenda**: nota, meridiano y banda. Aunque la baliza quede detrás del planeta, ves que la nota cambia.

### La baliza

- Una **esfera**: da igual hacia dónde la oriente TouchDesigner.
- Con su **propio material cian fijo** (`mat_baliza`): no depende del color por instancia.
- Su tamaño lo controla el **propio SOP**, no la escala por instancia.
- **Gira con el planeta**: el mismo ángulo que núcleo y retícula en cada fotograma.
- Se coloca sobre la normal de su celda, justo encima del marcador (comprobado: desviación cero).

| Valor | Cifra | Dónde cambiarlo |
|---|---|---|
| Radio en reposo | 0,9 | `BASE_RADIUS` en `baliza_callbacks` |
| Radio en el golpe | 2,7 | `PEAK_RADIUS` (lo que crece: 1,8) |
| Caída del pulso | a un tercio en 0,12 s | `DECAY` |
| Separación de la superficie | 0,3 | `LIFT` |

La caída es corta a propósito: entre dos semicorcheas a 120 BPM (125 ms) la baliza cae al 35 %, así que cada nota se ve como un golpe separado. Con una caída más larga, a semicorcheas no llegaba a apagarse y parecía una bola fija. Si en tempos lentos te resulta demasiado breve, sube `DECAY`.

### Qué añade

Dentro de `/project1/FASE1`, sin rehacer la fase 1:

| Nodo | Qué es | Para qué sirve |
|---|---|---|
| `baliza_callbacks` | Text DAT (módulo) | Posición y pulso de la baliza, y su apartado de la leyenda. |
| `baliza_chop` | Script CHOP | Publica posición, pulso, radio y nota. |
| `latido` | Execute DAT | Recalcula la baliza en cada fotograma, para que el pulso se anime. |
| `baliza` | Geometry COMP | La esfera cian (SOP `esfera_baliza` **dentro**). |
| `mat_baliza` | Constant MAT | Cian fijo. |
| `midi_in` | MIDI In DAT | Recibe el BeatStep. |
| `midi_callbacks` | Text DAT | Filtra las notas del SEQ1 y dispara la baliza. |
| `midi_log` | Table DAT | Últimas 40 notas recibidas y qué se hizo con ellas. |

Y toca dos cosas de la fase 1: añade `baliza` a la lista del render (`nucleo reticula baliza`) y añade su apartado a la leyenda.

### Parámetros (página Fase2)

| Parámetro | Qué hace | Por defecto |
|---|---|---|
| `Canal` | Canal MIDI del SEQ1 | 13 |
| `Filtrar` | Solo atiende a ese canal | Activado |
| `Nota` | Última nota recibida. Muévela a mano para probar sin BeatStep | 60 |

### La nota se lee de los bytes

TouchDesigner numera los controladores desde 1 (el CC 51 del BeatStep aparece como 52). Si hiciera lo mismo con las notas, cada baliza caería un semitono desplazada. Por eso nota y canal se sacan de los bytes del mensaje, que no admiten interpretación: `9C 40 64` es nota 64 en el canal 13 con velocidad 100.

Se ignora todo lo que no sea un *note on* del canal 13 con velocidad mayor que cero: note off, reloj, START y STOP, controladores, SysEx y los demás canales.

### El dispositivo MIDI

El script copia el dispositivo del MIDI In que ya usa midicontrolx (o, si no lo encuentra, el de `FASE1_anterior`). Si no encuentra ninguno, te lo dice y hay que poner a mano en `midi_in` el *Device ID* que tenga el BeatStep en el MIDI Device Mapper.

### La leyenda completa

```
TEMPO    120.0 BPM    (tempo del proyecto)
VUELTA   8 compases = 16.0 s       27%

NOTA     mi4    64    meridiano  4    banda 5
PULSO    [######......]
SEQ1     canal 13    notas recibidas: 37
```

La línea **SEQ1** es el diagnóstico rápido: si el contador no sube al tocar, no está llegando MIDI.

### Autoprueba

Al terminar, el script simula una nota por el mismo camino que el MIDI real (nota 64 en el canal 13, en bytes `9C 40 64`) y comprueba que la baliza la recibe, que pulsa, y que una nota en el canal 1 se ignora. Si dice **AUTOPRUEBA OK**, el código funciona de punta a punta y cualquier fallo con el aparato real es de conexión.

### La corrección del render

La primera versión de la fase 2 (`fase2 v2`) leía la lista de geometrías del render para añadirle la baliza. Ese parámetro referencia operadores, y leerlo devuelve un operador, no el texto: al escribirlo de vuelta, la lista quedaba como `type:geometryCOMP path:.../nucleo baliza` y el render perdía el núcleo y la retícula. La `fase2 v3` escribe la lista entera, sin leerla. Si aplicaste la v2, `fix_render_fase2.py` lo repara: muestra la lista antes y después y no toca nada más.

---

### Cómo comprobar que todo funciona

1. **Gira la perilla TEMPO del BeatStep.** La línea TEMPO la sigue y el planeta acelera o frena sin saltar.
2. **Dale al PLAY con el SEQ1 sonando.** En el Textport aparecen las primeras notas con `DISPARO`; en pantalla, la baliza salta de celda en celda y pulsa con cada nota.
3. **Mueve `Nota` a mano** (página Fase2). La baliza va a esa celda y pulsa: sirve para probar sin el BeatStep.
4. **Desactiva `Showgrid`.** La esfera parece quieta aunque gira: sin detalle en la superficie no se percibe la rotación.
5. **Pon `Tilt` a 0.** El planeta se convierte en un diagrama; a 20 vuelve a ser un cuerpo.
6. **Activa `Pausa`.** Todo se congela; al quitarla sigue desde ese punto.

---

### Problemas frecuentes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| No se ve el núcleo tras la fase 2 | Lista del render corrompida por la `fase2 v2` | `fix_render_fase2.py`, o pon a mano `nucleo reticula baliza` en *Geometry* del render |
| No se ve ninguna esfera | Geometría fuera de su Geometry COMP, o sin flag de render | Los informes lo comprueban: mira las líneas "renderiza" |
| La línea TEMPO no cambia al girar la perilla | midicontrolx no escribe en el tempo del proyecto | Que escriba en el componente que indica el informe (normalmente `/local/time`) |
| TEMPO dice "sin tempo" | El tempo del proyecto es 0 o no se encuentra | Revisa la ruta del informe |
| El planeta no gira | `Pausa` activada o línea de tiempo parada | La línea ESTADO de la leyenda dice cuál |
| "notas recibidas" no sube | El `midi_in` no apunta al BeatStep | Pon su *Device ID* del MIDI Device Mapper |
| Las notas salen como "ignorado: canal X" | El SEQ1 no está en el canal 13 | Cambia `Canal` en la página Fase2 |
| La baliza no se ve aunque la nota cambia | Está en la cara oculta del planeta | Normal: la leyenda muestra la nota igualmente |
| No aparece la leyenda | No se pudo hacer transparente el fondo del rótulo | Mírala en el nodo `rotulo` |
| Errores rojos en `FASE1_anterior` | Rutas antiguas a `/project1/FASE1` | Saca lo que necesites (midicontrolx, `master_beat`) y bórrala |
| El informe no muestra la versión esperada | Se ejecuta otro archivo | Revisa la ruta del `exec` |

---

### Decisiones tomadas por el camino

Lo que se probó, por qué se descartó, y lo que queda de ello:

- **El tiempo, una sola fuente.** Se probó que FASE1 leyera el reloj MIDI por su cuenta (`reloj_chop`), y después que corrigiera el tempo de TouchDesigner para seguir al BeatStep (`tempo_esclavo`). Ambas cosas duplicaban el trabajo de midicontrolx y competían con él. Quedan fuera por completo: FASE1 solo lee el tempo del proyecto.
- **Sin parámetro Bpm en FASE1.** Dos sitios donde vive el tempo acaban diciendo cosas distintas.
- **TouchDesigner solo escucha al BeatStep.** Se probó a cambiar de pattern enviando Program Change desde TouchDesigner; descartado: los cambios se hacen desde el BeatStep.
- **Lo que se sabe del BeatStep por MIDI.** Comprobado con tu aparato: Stop y Play envían MIDI Machine Control (SysEx `F0 7F 7F 06 01/02 F7`) y un CC (51 y 54). También llegan ráfagas de *All Notes Off* (CC 123) a los 16 canales; **falta confirmar** si salen al cambiar de pattern, al pulsar Stop, o en ambos casos. La longitud del pattern no viaja por MIDI.
- **Construir por fases.** Los primeros constructores hacían el sistema entero de una vez y era imposible entender qué fallaba. Desde la fase 1 se avanza un paso cada vez, y cada script se prueba de punta a punta antes de entregarlo.

### Trabajo explorado y aparcado

Para cuando toque, con prototipos ya probados en simulación (archivos `fase2f` a `fase2j`):

- **Detectar la longitud del pattern del SEQ1** escuchando las notas: busca el periodo más corto con el que se repite la secuencia.
- **Biblioteca de patterns**: guarda la huella de cada pattern confirmado y, al volver a él, lo reconoce en unas tres notas.
- **Aviso de cambio de pattern** con la ráfaga de All Notes Off, descartando la que acompaña al Stop. Antes hay que confirmar con el aparato cuándo la envía: cambiar de pattern dos veces y luego pulsar Stop, mirando el Textport.

Habrá que rehacerlos sobre la base nueva: se construyeron sobre la versión anterior de FASE1.

### Archivos obsoletos

No los ejecutes sobre la FASE1 nueva: se construyeron para versiones anteriores.

- Constructores del sistema completo: `build_topografias_drone.py`, `build_estratos_bsp.py`, `build_estratos_test01.py`, `build_estratos_completo.py`, `build_estratos_net.py`.
- Fase 1 original y sus parches: `fase1_nucleo.py`, `fix_fase1.py`.
- Fase 2 anterior y su evolución: `fase2a_nota.py`, `fase2a_baliza.py`, `fase2b_seq1.py`, `fase2c_reloj.py`, `fase2d_reloj_diag.py`, `fase2e_tempo.py`, `fase2f_patrones.py`, `fase2g_program_change.py`, `fase2h_escucha.py`, `fase2i_master_beat_v2.py`, `fase2j_senal_cambio.py`, `fase2l_tiempo_midicontrolx.py`.
- Parches de versiones anteriores: `fix_estratos.py`, `fix_estratos_02.py`, `fix_leyenda.py`.

---

### Lo que viene después

La base está completa: un cuerpo que gira con el tiempo del BeatStep y sabe dónde cae cada nota. Los siguientes pasos naturales son que las notas dejen una construcción en su celda (la primera semilla de la acumulación), y recuperar la detección de patterns para que la longitud de una vuelta siga al pattern del SEQ1.
