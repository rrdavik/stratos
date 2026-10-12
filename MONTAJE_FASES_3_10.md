# Estratos · Montaje
## Fases 3 a 10: de la baliza al planeta estratificado

*Continúa `MONTAJE_FASE1.md` (fases 1 y 2, ahora en un solo script: `fase12_base.py`). Plan de referencia: `PLAN_FASES.md`.*

---

### Estado en una frase

Cada nota del SEQ1 y del SEQ2 deposita y hace crecer formaciones sobre el planeta. Al toparse con el límite de altura se ramifican, se fusionan y se coronan. La batería las erosiona. Cuando el mundo madura y deja de cambiar (o llega a su edad máxima) se entierra como una concha nueva, tan gruesa como lo que duró, y los cortes profundos dejan ver las capas enterradas.

---

### Archivos

Todos en la misma carpeta: `C:/Users/DareDave/Downloads/est`.

| Archivo | Para qué | Versión |
|---|---|---|
| `fase12_base.py` | Fases 1 y 2 en uno: núcleo, retícula de polo a polo, baliza (la retira la fase 3: la sustituye la luz de celda), MIDI, render y leyenda. Lleva dentro el arreglo del render. Su `ritmo` ya sabe del giro vivo (en un proyecto en marcha lo parchea `estratos_comun.py`) | `fase12 v2` |
| `estratos_motor.py` | La lógica entera del mundo. Lo cargan las fases; no se ejecuta solo | `motor v18` |
| `estratos_comun.py` | Piezas compartidas por los scripts de fase; no se ejecuta solo | `comun v11` |
| `fase3_semilla.py` | Carga y frenada, semilla, crecimiento, material, balanceo del eje, polos y anillos, luz de celda | `fase3 v9` |
| `fase4_desborde.py` | Desbordamiento con carga, satélites, fusión, coronación, cumbre | `fase4 v6` |
| `fase5_especies.py` | SEQ2, arquitectura, híbridos, luz ámbar del SEQ2 | `fase5 v2` |
| `fase6_ciclo.py` | El ciclo lo cierra el mundo: madurez, novedad, tabla `ciclos`, giro vivo | `fase6 v3` |
| `fase7_erosion.py` | Canal 16; erosión en notas; perfiles del usuario; el borde de la celda es la batería; huellas, presupuesto | `fase7 v6` |
| `fase8_conchas.py` | Conchas con el grosor de su ciclo, herencia, radio acumulado | `fase8 v4` |
| `fase9_arqueologia.py` | Cortes con grosores distintos, estratigrafía, cicatriz cian, destello | `fase9 v5` |
| `fase10_direccion.py` | Paleta, luz cenital, cámara de superficie, modos | `fase10 v4` |

Se ejecutan en orden desde el Textport (Alt+T), cada uno después de comprobar el anterior. `fase12_base.py` sustituye a `fase1_tempo_beatstep.py`, `fase2_seq1_baliza.py` y `fix_render_fase2.py`, que ya no hacen falta:

```python
exec(open('C:/Users/DareDave/Downloads/est/fase12_base.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase3_semilla.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase4_desborde.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase5_especies.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase6_ciclo.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase7_erosion.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase8_conchas.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase9_arqueologia.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase10_direccion.py').read())
```

Cada script:

- dice su versión en la primera línea del informe;
- se niega a correr si falta la fase anterior;
- termina con una **AUTOPRUEBA** que simula el MIDI por el mismo camino que el real y deja el mundo como estaba. Si dice `AUTOPRUEBA OK`, el código funciona y cualquier fallo con el aparato es de conexión o de canal.

Si mueves la carpeta, cambia `CARPETA` al principio de cada script de fase.

---

### Cómo está montado

```
BeatStep ──MIDI──> midi_in ──> midi_callbacks (router)
                                    │
                                    ▼
                                 motor  ◄── parámetros de las páginas Fase3…Fase10
                         (estado del mundo 'W')       ◄── pulsos (botones)
                                    │
             latido (cada fotograma): avanza el motor y pide las instancias
                                    │
     ┌──────────────┬───────────────┼──────────────┬──────────────┐
i_formas_pulidas  i_formas_porosas  i_coronas     i_estratos     i_luz_celda     (Script CHOP)
     │                │               │              │              │
formas_pulidas    formas_porosas    coronas        estratos       luz_celda       (Geometry COMP)
```

- **Un solo motor.** Toda la lógica vive en el Text DAT `motor`, cargado desde `estratos_motor.py`. Las fases no reescriben la lógica de las anteriores: suben el parámetro `Nivel` (página Estratos, solo lectura), y el motor activa lo que corresponde a ese nivel. La fase 3 se comporta como fase 3 aunque el motor ya sepa hacer la 10.
- **El mundo sobrevive.** El estado está en el storage del DAT `motor`: se guarda con el `.toe` y no se pierde al relanzar una fase. `Resetmundo` (página Fase3) lo vacía.
- **Relanzar cualquier fase refresca el motor** y los DAT que lo usan. Si cambias `estratos_motor.py`, basta con relanzar la última fase aplicada.
- **Una sola geometría para todo:** una caja de 1×1×1 con la base en y = 0, instanciada con posición, giro, escala y color. Las formas se distinguen por cómo se colocan las cajas, no por usar SOPs distintos.
- **Material por instancia, no:** TouchDesigner no da brillo distinto a cada instancia. Por eso hay dos geometrías, `formas_pulidas` y `formas_porosas`, y el motor reparte cada formación según la velocidad de su nota fundadora.

### Lo que la fase 3 reescribe de las fases 1 y 2

| DAT | Antes | Ahora |
|---|---|---|
| `midi_callbacks` | Solo note on del SEQ1 | Router: note on/off por canal, CC, START/STOP, MMC |
| `latido` | Recalcula la baliza | Avanza el motor y redibuja |
| `baliza`, `baliza_chop`, `baliza_callbacks` | Baliza cian del SEQ1 | **Se retiran** (motor v18): la nota del SEQ1 enciende el centro de su celda (`luz_celda`). La leyenda NOTA la da el motor |
| `reticula_callbacks` | Radio fijo 6 | Marcadores sobre la superficie actual (suben con las conchas) |
| `rotulo` | Tempo + nota | Tempo + nota + motor |

**No relances `fase12_base.py` sobre un proyecto en marcha**: crea una FASE1 nueva y vacía (la vieja queda como `FASE1_anterior`, apagada) y obliga a aplicar de nuevo las fases 3 en adelante. Para refrescar el motor, relanza la última fase aplicada.

**Diagnóstico del render.** `fase12_base.py` y cada fase terminan con un bloque `DIAGNOSTICO DEL RENDER`: qué geometrías dibuja el render, con qué cámara y luces, y qué nodos de la cadena hasta `salida` tienen errores (motor, Script CHOP, rótulo…). Si no ves la imagen, pégame ese bloque. Las leyendas ya no pueden romper la salida: si fallan, escriben el fallo en el rótulo.

---

## FASE 3 · La semilla

Cada nota del SEQ1 suma 1 a la **carga** de su celda. Cuando la carga llega al **coste**, se dispara un **trigger de construcción**: la ocupación sube 1 y la carga vuelve a 0. La ocupación cuenta triggers, no notas.

- **El coste sube con la altura** (motor v8). Es 1 abajo y `Costemax` (5) en el límite: coste = 1 + ⌊(`Costemax` − 1) × altura / límite⌋, con la altura nominal de la ocupación actual. Desde el límite, cada trigger cuesta `Costemax` (ramificación, fusión, coronación y cumbre).
- **Frenada:** cada nota sube la formación `Growstep` × límite / coste. Un trigger completo sube siempre un escalón, pero repartido entre más notas conforme la formación crece, así que cuanto más alta, más despacio.
- **Latido:** cada nota hincha la formación un 5 % y la aclara durante ~0,2 s, aunque no dispare ningún trigger. Así se ve que la nota ha llegado.
- `Costemax` 1 deja el comportamiento antiguo: un trigger por nota.

| Ocupación | Estado | Altura | Coste del siguiente | Notas acumuladas |
|---|---|---|---|---|
| 1 | semilla | 20 % | 1 | 1 |
| 2 | brote | 40 % | 2 | 2 |
| 3 | crecimiento | 60 % | 3 | 4 |
| 4 | madurez | 80 % | 4 | 7 |
| 5+ | límite: `Alturafactor` × `Shellthick` (3,75 × 0,5 = 1,875) | 100 % | 5 | 11 |

Antes se llegaba al límite con 4 notas. Ahora hacen falta 11, y el límite es un 25 % más alto (1,875 en vez de 1,5). Con una nota por pattern (16 pasos a 120 BPM) son ~20 s en vez de 6.

- **El gate decide cuánto crece** (`Gatemode`). Al llegar el note off se mide cuánto duró la nota respecto a un paso: un gate al 50 % da el crecimiento normal, un gate corto la mitad o menos (hasta ¼) y uno ligado como mucho `Gatemax` veces (1,25; antes era el doble). Sin note off, crecimiento normal. Se aplica al trozo de escalón de cada nota y no cambia la carga.
- **Techo del escalón** (motor v9): la altura nunca pasa del escalón que se está construyendo. Ni un gate ligado ni la presión de una vecina adelantan la altura a los triggers. Antes, con gates largos, una formación podía tocar el límite con la mitad de las notas.
- **Material**: la velocidad de la primera nota decide (`Umbralvel`, 64) y no vuelve a cambiar. Desde motor v10 la diferencia no depende solo del brillo, que en cajas pequeñas apenas se veía:
  - **Pulido** (por encima): color claro y frío, prismas limpios y algo más esbeltos; en arquitectura, plantas casi pegadas (torre de cristal). `mat_pulido` tiene un reflejo blanco ancho y fuerte (especular 1, brillo 14) y algo de ambiente.
  - **Poroso** (por debajo): color oscuro y terroso. Cada pieza se rompe en 2–3 tramos de ancho irregular, con grietas entre ellos y grumos pegados; en arquitectura, plantas desiguales y descolgadas (hormigón). `mat_poroso` no tiene reflejo.
  - Relanzar la fase 3 o la 4 reajusta los dos materiales.
- **Animación**: la altura visible se acerca a la real en ~0,1 s; las formaciones brotan, no aparecen de golpe.
- **Balanceo del eje** (v2): además del giro al tempo, el eje se balancea hacia la cámara y en contra, `Balanceo` grados (60) cada `Balanceoper` segundos (90), para ver los dos polos. Va aparte del reloj del secuenciador y se congela con `Pausa`. `Rotextra` lo enciende y lo apaga; entra y sale en 3 s, sin saltos. Lo llevan todas las geometrías que giran con el planeta (núcleo, retícula, luz de celda, formas, coronas, estratos) y la luz de destello. Orden de rotación: `Ry Rx Rz` (giro, balanceo, inclinación).

**Luz de celda** (fase 3 v9, motor v18). No hay balizas: ni la del SEQ1, ni la del SEQ2, ni las de la batería. Cada celda cuenta con luz lo que le está pasando, en una rejilla de 3 × 3 losetas opacas a ras de su superficie (geometría `luz_celda`, Script CHOP `i_luz_celda`, material `mat_luz_celda`). La crea y la mantiene cualquier fase al relanzarse, que también retira las balizas de las versiones anteriores.

- **El centro dice quién construye:** el color del secuenciador que acaba de tocar la celda. SEQ1 cian (blanco desde la fase 9: el cian queda para las cicatrices) y SEQ2 ámbar (fase 5).
  - **Pulso y reposo:** con cada nota, un pulso en el que la loseta crece y brilla. Después, la última celda de cada secuenciador queda tenue (60 % del color) hasta su siguiente nota, para que se vea dónde está cada uno.
  - **Los dos en la misma celda:** el centro se parte en dos mitades, SEQ1 al oeste y SEQ2 al este.
  - **Con formación,** el centro se ensancha hasta asomar alrededor de su base: se enciende el pie de la formación y se lee desde la cámara aunque la formación sea alta. La luz va en la superficie, no en la punta, así que el ámbar del SEQ2 no se confunde con las coronas.
  - **Convive con el latido:** la formación se sigue hinchando un 5 % y aclarando con cada nota.
- **El borde dice quién destruye** (fase 7): las 8 losetas de alrededor son los 8 pads de la batería.
- **Sin transparencias:** cada zona lleva un color opaco, así que no se mezclan y no hay problemas de orden de dibujo.
- **Interruptores:** `Luzseq` (página Fase3) para el centro y `Balizasdrum` (página Fase7) para el borde. Las dos luces son parte del mundo y se ven también en modo actuación.

**Página Fase3:** `Luzseq` · `Shellthick` 0,5 · `Alturafactor` 3,75 · `Semillafrac` 0,20 · `Growstep` 0,20 (por trigger) · `Costemax` 5 · `Gatemode` · `Gatemax` 1,25 · `Umbralvel` 64 · `Velprueba` 100 · `Sembrar` · `Resetmundo` · `Rotextra` · `Balanceo` 60 · `Balanceoper` 90 · `Notapolosur` 24 · `Notapolonorte` 108 · `Fuerarango`

Los tres últimos los crea ya `fase12_base.py` en esta página; si venían de la página Fase1 (versión anterior), la fase 3 los mueve aquí conservando su valor.

**Leyenda:** `MUNDO ocupadas 23/85 (27%) max 4 fase 3`, `RANGO do1 24 (polo sur) a do8 108 (polo norte) 85 celdas fuera: plegar` y `ULTIMA geo celda 40 ocupacion 3 crecimiento carga 1/3`. `Sembrar` también escribe la carga en el Textport.

**Proyecto en marcha:** al relanzar la fase 3 o la 4, `Alturafactor`, `Semillafrac`, `Growstep` y los umbrales de la fase 4 pasan a sus valores nuevos solo si seguían en el valor de antes. Lo que hayas ajustado a mano se queda como está; las líneas `..` del informe dicen qué ha cambiado. En la línea NOTA: `celda 40 de 85 anillo 4`, y `(como do1 24)` si la nota se ha plegado.

**Probar sin BeatStep:** elige `Nota` (página Fase2) y pulsa `Sembrar` varias veces.

**Retícula de polo a polo** (motor v7):

- **Los polos son las notas extremas del rango.** `Notapolosur` (24, do1) es el **polo sur** y `Notapolonorte` (108, do8) el **polo norte**. Los dos van entre do1 y do8: `Notapolosur` de 24 a 106, `Notapolonorte` de 26 a 108.
- **En medio, un anillo por octava, como la retícula de bandas.** La clase de nota es el meridiano y la octava el anillo. Con do1–do8: un anillo de 11 (do#1–si1), seis de 12 (do2–si7) y do8 en el polo norte; 85 celdas. Si el rango no empieza o acaba en do, el primer y el último anillo quedan incompletos y reparten sus celdas por igual alrededor.
- **Los anillos se reparten por igual entre los dos casquetes polares.** Con do1–do8, 24° de alto cada uno; el casquete del polo, 6° de radio.
- **Notación:** MIDI 60 = do4. Los límites van en número MIDI, el de la columna `nota` de `midi_log`.
- **`Fuerarango`:** `plegar` (por defecto) lleva la nota por octavas dentro del rango y conserva su meridiano; `ignorar` no deja nada, aunque la nota sigue contando para la detección de patterns; `limitar` la manda al polo más cercano.
- **Cambiar el rango rehace la retícula y vacía el mundo** (también las conchas). Es para ajustarlo antes de tocar.
- En los anillos cercanos a los polos la celda es estrecha de este a oeste. El ancho y la dispersión de agujas, torres y excrecencias se ajustan al ancho real de la celda: ninguna pieza invade a la vecina.
---

## FASE 4 · El límite como motor

Desde el límite (ocupación 5), cada trigger se desborda a una vecina. En el límite cada trigger cuesta `Costemax` notas (5): las notas intermedias solo cargan y hacen latir la formación.

| Ocupación | Resultado | Notas acumuladas |
|---|---|---|
| 5–6 | Satélites en la vecindad (más pequeños: `Tamsatelite`) | 11 |
| 7–8 | Fusión: un macizo bajo bajo el núcleo y sus satélites los une en una masa | 21 |
| 9–10 | Coronación: aguja ámbar (geología) o antena con remate (arquitectura) | 31 |
| 11+ | **Cumbre:** cada trigger alarga la corona un 25 % (y la ensancha un poco), hasta `Tramoscumbre` tramos (4: corona al doble, con 56 notas) | 41 |

- **Desborde a una celda vacía:** nace un satélite de esa formación.
- **Desborde a su propio satélite:** el satélite crece, hasta `Limsatelite`.
- **Desborde a una formación ajena (presión):** le suma 1 a la carga, como si le llegara una nota: crece su trozo de escalón y, si completa la carga, sube su ocupación. No hay cascada: aunque esté en el límite, no desborda a su vez. Si es de la otra especie, la marca como híbrida.
- **Un satélite que recibe una nota directa** se independiza.

**Decisión: 6 vecinas.** Entre dos anillos completos, la retícula se trata como hexagonal desplazada: 2 vecinas en el mismo anillo, 2 en el de arriba y 2 en el de abajo (los pares miran a los meridianos c−1 y c, los impares a c y c+1). En un anillo incompleto, las vecinas del anillo contiguo son las celdas cuyo arco se solapa con el suyo, y en los anillos extremos se suma el polo. El polo tiene de vecinas todo su anillo (11 con do1).

**Decisión: quién elige la vecina.** No el azar del software:

- `Vecina = velocidad`: velocidad mod nº de vecinas;
- `Vecina = velocidad + ocupación` (por defecto): la formación da la vuelta a su vecindad conforme insiste, aunque la velocidad sea fija.

Si el knob RANDOMNESS del SEQ1 varía la velocidad, la decisión pasa a ser del aparato. **Por confirmar**: gira RANDOMNESS y mira la columna `vel` de `midi_log`.

**Página Fase4:** `Umbralram` 5 · `Umbralfusion` 7 · `Umbralcorona` 9 · `Umbralcumbre` 11 · `Tramoscumbre` 4 · `Tamsatelite` 0,6 · `Limsatelite` 0,6 · `Vecina`

**Leyenda:** `DESBORDE 57 -> 44 satelites 3 fusiones 1 coronas 0 cumbres 0`

---

## FASE 5 · Dos especies

| | Geología (SEQ1) | Arquitectura (SEQ2) |
|---|---|---|
| Piezas | 1 a 3 agujas por celda, inclinadas, de tamaños desiguales | Torre de plantas apiladas (4 plantas en el límite) |
| Ángulos | Oblicuos | Rectos, alineados con la celda |
| Corona | Aguja ámbar fina | Antena con remate plano |

**Híbridos:** cuando una especie cae sobre una celda de la otra, la celda pasa a híbrida y guarda ambos rastros:

- geología colonizada → **macizo aterrazado**: dos plantas rectas en la ladera;
- arquitectura colonizada → **torre mineralizada**: dos excrecencias oblicuas en los flancos.

El material lo sigue decidiendo la nota fundadora.

**Luz del SEQ2** (fase 5 v2): cada nota del SEQ2 enciende el centro de su celda en ámbar, con pulso y tenue hasta la siguiente. Ya no hay esfera. Si el SEQ1 está en la misma celda, el centro se parte en dos.

**Página Fase5:** `Canal2` 14 · `Nota2` · `Sembrar2`

**Por confirmar:** el canal del SEQ2. Si sus notas salen en el Textport como `ignorado: canal X`, pon X en `Canal2`.

**Leyenda:** `SEQ2 canal 14 notas 37 hibridas 3`

---

## FASE 6 · El ciclo: lo cierra el mundo

*fase6 v2 (motor v11). Sustituye a la v1, que deducía el ciclo de la longitud de los patterns.*

**Por qué cambia.** La v1 medía la partitura, no el mundo. Con probabilidad, aleatoriedad y acumulación, el mundo no se repite aunque el secuenciador sí. La detección llegaba tarde (16 pasos al 60 %: hacia el paso 53) y, con patterns repetitivos, no llegaba nunca. Además, el ciclo resultante seguía siendo una constante (`Repsporciclo`) escalada por la longitud: en la práctica, un temporizador.

**Regla:** el mundo se entierra cuando está **maduro y deja de cambiar**, o cuando alcanza su **edad máxima**. Se inspira en el ciclo adaptativo de Holling: crecer (fases 3 a 5), madurar y estancarse, liberar (erosión, fase 7) y reorganizar (enterramiento con herencia, fase 8). Hasta ahora la reorganización la disparaba el reloj; ahora la dispara el estado del mundo. Ya no se detecta la longitud de los patterns.

**Señales.** La v2 no añade ninguna entrada MIDI; de hecho escucha menos. Lo nuevo es que escucha al propio mundo: el estado de las celdas pasa a ser una entrada del ciclo.

| Escucha | Origen | Para qué |
|---|---|---|
| Pulso de tempo | Tempo del proyecto (`ritmo.tempo()`), que fija el BeatStep vía midicontrolx, el mismo desde la fase 1 | Contar compases (`Negrasporcompas`) y suavizar `giro_factor` en un compás |
| Transporte | Play o pausa de la línea de tiempo | El reloj del ciclo solo avanza en play |
| STOP | Mensaje de transporte MIDI | Para el reloj si llega después de la última nota; distingue la ráfaga de All Notes Off que acompaña a un STOP |
| START / MMC Play | `FA` o MMC Play | Solo reanuda la marcha; ya no pone ningún paso a 0 |
| Última nota | Note on | Condición de marcha: alguna nota en los últimos 4 compases |
| All Notes Off | CC 123 en 8 canales o más en 0,12 s, sin STOP | AVISO de cambio de pattern; con `Cambioentierra`, entierra el mundo (respetando `Ciclomin`) |
| Estado del mundo | Especie, ocupación, híbrida, satélite y huella de cada celda | La foto de cada compás, de la que salen madurez y novedad |
| `Forzarciclo` | Pulso de la página Fase6 | Cierra el ciclo al instante (control de prueba, no señal) |

| Produce | Qué es | Quién la usa |
|---|---|---|
| Compás del ciclo | Compases desde el último cierre | Regla de cierre, leyenda, grosor de la concha (fase 8) |
| Madurez | 0–1: formaciones que han llegado al límite | Regla de cierre, leyenda, tabla `ciclos` |
| Novedad | 0–1: celdas vivas cuya forma ha cambiado desde el compás anterior | Regla de cierre, `giro_factor`, leyenda, tabla `ciclos` |
| Compases quietos | Compases seguidos maduros y sin novedad | Regla de cierre, leyenda |
| `giro_factor` | Entre `Giromin` y 1 | Velocidad de rotación del núcleo |
| `fin_de_ciclo` | Ciclo, compases, segundos, motivo, madurez y novedad | Fase 8 (enterramiento y grosor), tabla `ciclos`, AVISO |

Deja de escuchar, respecto a la v1: el intervalo entre notas como medida del paso, la secuencia de tonos como huella de pattern (biblioteca y cambio por notas) y START/MMC Play como paso 0.

**El bombo y el ciclo.** Cada temblor del bombo (fase 7) cambia la forma de muchas celdas a la vez, las que están por debajo de la corona. Mientras suena, la novedad no baja del umbral y los ciclos se cierran por edad máxima. Al quitarlo, el mundo se asienta y se entierra por estancamiento. Dicho en términos de directo: **el breakdown entierra el mundo**. En simulación, el mundo tarda unos 30 compases en asentarse después de 16 compases de bombo a negras, porque antes vuelve a crecer lo erosionado. Con `Umbralnovedad` 0,10, unos 20.

**Reloj de compases.** Cuenta compases con el tempo del proyecto, el mismo que hace girar el núcleo (`ritmo.tempo()`). Un compás son `Negrasporcompas` negras (4). Solo avanza con el secuenciador en marcha: línea de tiempo en play, ningún STOP posterior a la última nota y alguna nota en los últimos 4 compases. START y MMC Play se siguen recibiendo, pero ya no ponen ningún paso a 0.

**Las dos medidas.** En cada compás que avanza el reloj, el motor toma una foto de la forma de cada celda:

```
forma(celda) = (especie, min(ocupación, Umbralcorona), híbrida, satélite, huella)
novedad = celdas cuya forma ha cambiado desde el compás anterior / celdas vivas (ahora o en el compás anterior)
madurez = formaciones con ocupación >= Umbralram / formaciones (sin contar satélites)
```

- **El recorte a `Umbralcorona` es obligatorio.** Una celda coronada sigue sumando ocupación con cada nota, y la cumbre sigue alargando la corona, pero su forma ya cuenta como hecha. Si se midiera el contador, la novedad no llegaría nunca a 0.
- **Satélites:** se recortan antes, en la ocupación con la que llegan a `Limsatelite` (3 con los valores por defecto). Después siguen sumando ocupación con cada desborde, pero ya no cambian de forma.
- **La huella** solo cuenta desde el nivel 7.
- **Un mundo vacío** tiene madurez 0, así que nunca se cierra por estancamiento.

**Cierre del ciclo.** Va por orden; nunca antes de `Ciclomin`, salvo con `Forzarciclo`:

| Motivo | Cuándo |
|---|---|
| `cambio de pattern` | Hubo una ráfaga de All Notes Off sin STOP con `Cambioentierra` encendido. Se aplica en cuanto se llega a `Ciclomin` |
| `estancado` | `Compasesquietos` compases seguidos con madurez ≥ `Umbralmadurez` y novedad ≤ `Umbralnovedad` |
| `edad maxima` | El mundo llega a `Ciclomax` compases |
| `forzado` | Pulso `Forzarciclo`: cierra al instante |

Cada cierre emite el evento `fin_de_ciclo` (ciclo, compases, segundos, motivo, madurez, novedad), escribe `AVISO fin de ciclo N: <motivo> a los C compases` en el Textport y añade una fila a la tabla `ciclos`. Desde la fase 8, además entierra el mundo.

Con `Nivel` 6 o 7 el evento solo informa: el mundo no se entierra, así que puede seguir maduro y quieto y volver a cerrarse cada `Ciclomin` compases. Es lo esperado. Si `Ciclomax` < `Ciclomin`, el informe avisa con `..` y se usa `Ciclomax` = `Ciclomin`.

**Cambio de pattern.** Ahora solo se detecta por la ráfaga de All Notes Off (CC 123 en 8 canales o más en 0,12 s) sin STOP. Ya no se detecta por las notas: eso dependía de la biblioteca, que desaparece. Con `Cambioentierra` apagado, la ráfaga solo da el AVISO.

**Giro vivo.** `Barsperturn` vuelve a ser manual para siempre; si tenías `Turnauto`, se queda el valor que tuviera. Con `Girovivo`, el giro del núcleo se multiplica por un factor:

```
objetivo    = clamp(novedad / (4 × Umbralnovedad), Giromin, 1)
giro_factor → objetivo, suavizado en un compás
```

El planeta se frena a medida que el mundo deja de cambiar (justo antes de enterrarse casi se detiene) y vuelve a acelerar con la novedad. El giro sigue acumulándose, así que el cambio de factor no hace saltar el planeta. El factor lo lee `ritmo`; `estratos_comun.py` le añade esa lectura al relanzar cualquier fase, sin perder el ángulo acumulado.

**Tabla `ciclos`.** Una fila por ciclo cerrado: `ciclo`, `compases`, `segundos`, `motivo`, `madurez`, `novedad` y, desde la fase 8, `grosor`. Guarda las últimas 200. Sirve para afinar los umbrales con el aparato.

**Página Fase6:** `Umbralmadurez` 0,6 · `Umbralnovedad` 0,05 · `Compasesquietos` 4 · `Ciclomin` 8 · `Ciclomax` 64 · `Negrasporcompas` 4 · `Cambioentierra` (apagado) · `Girovivo` (encendido) · `Giromin` 0,25 · `Forzarciclo`

La fase 6 v2 quita los parámetros obsoletos: `Repsporciclo`, `Modociclo`, `Turnauto`, `Longmanual`, `Longfija`, `Longmin`, `Pasosporcompas`, `Pasospornegra` y `Resetpatterns`.

**Leyenda:**

```
CICLO    5   compas 23 (8-64)   madurez 64%   novedad 3%   quieto 2/4   giro x0.40
AVISO    fin de ciclo 4: estancado a los 19 compases
```

Con el secuenciador parado, en lugar del compás pone `parado`.

**Ojo con el ritmo de crecimiento.** Con la carga por celda de las fases 3 y 4, una formación necesita 31 notas para coronarse. En simulación, un SEQ1 de 16 pasos sin batería madura y se queda quieto hacia el compás 30-40. Por eso `Ciclomax` es 64 (fase 6 v3; con 32 casi todos los ciclos cerraban por `edad maxima`). Al relanzar la fase 6, `Ciclomax` pasa de 32 a 64 solo si seguía en 32.

**Relanzar.** `fase6 v2` puede ejecutarse sobre un proyecto en nivel 6 o superior: no baja `Nivel` ni borra el mundo. Un mundo guardado por un motor anterior se migra solo: se borran las claves de la detección de longitud y de la biblioteca, el número de ciclo sigue donde iba y las conchas antiguas, que no guardan grosor, se leen con `Shellthick`. Para un proyecto en nivel 8 o superior: `fase6_ciclo.py`, después `fase8_conchas.py` y, por último, la última fase aplicada (por ejemplo `fase9_arqueologia.py` y `fase10_direccion.py`).

**Prueba pendiente con el aparato:** cambia de pattern dos veces y pulsa STOP mirando el Textport. Cada ráfaga sale como `AVISO All Notes Off sin STOP: cambio de pattern` o `AVISO All Notes Off junto a un STOP`. Si al cambiar de pattern no sale nada, el BeatStep no la envía y `Cambioentierra` no hará nada.

---

## FASE 7 · Erosión superficial

*fase 7 v6 (motor v18): erosión en notas, perfiles del usuario y el borde de la celda para la batería.*

Las 8 pistas de batería son las 8 señales de destrucción. Cada pad tiene un **perfil de tres números** en la tabla `perfiles_erosion`, editable a mano:

- **`reduccion`:** cuántas **notas** de construcción deshace en la celda que golpea. Un golpe de 1 deshace lo que construyó una nota del SEQ. Hasta la v4 contaba escalones.
- **`radio`:** cuántos anillos de vecinas alcanza. 0 es solo la celda, 1 la celda y sus vecinas, 2 un anillo más.
- **`profundidad`:** cuántas conchas atraviesa el corte, desde la fase 9. 0 no corta.

**La misma moneda que la construcción** (v5). Cada nota del SEQ sube la formación `Growstep` / coste y suma 1 a la carga (fase 3). Cada nota de erosión hace exactamente lo contrario: baja la carga y la altura lo mismo. Al agotarse la carga baja un escalón, y la carga queda llena menos una.

- **Simetría:** lo que costó más notas cuesta más golpes deshacerlo, también cerca del límite (la frenada). N notas de construcción seguidas de N de erosión devuelven la celda a como estaba, mientras no haya satélites de por medio.
- **La carga ya no se vacía de golpe.** Antes, un pad que golpeaba más a menudo de lo que cuesta un escalón dejaba esa celda sin volver a construir nunca. Ahora, si el SEQ toca más notas de las que deshace la batería, la celda sigue creciendo.
- **Orden inverso,** sin cambios: primero los satélites, luego la altura de la celda y al final la **huella**, una mancha oscura que dura hasta que la celda se vuelve a sembrar o se entierra. Los satélites crecen por desbordes, no por notas: cada nota de erosión les quita un desborde.
- **Por encima del límite** la altura no baja: igual que al construir, las notas ahí no suben la formación, sino que desbordan. Lo que cae primero son los satélites.

**Atenuación con la distancia:** completa en la celda objetivo, la mitad en el primer anillo y un cuarto en el segundo (`ATENUACION` = 0,5 por anillo). Las fracciones de nota se acumulan en cada celda: con reducción 1 y radio 1, cada vecina pierde una nota cada dos golpes. Con el presupuesto de densidad el radio puede llegar a 4, y cada anillo sigue recibiendo la mitad que el anterior.

**Perfiles por defecto** (v6, elegidos por el usuario):

| Pad | Rol | Reducción (notas) | Radio | Profundidad | Tipo |
|---|---|---|---|---|---|
| 1 | Bombo | 4 | 2 | 2 | temblor |
| 2 | Caja | 15 | 1 | 3 | corte |
| 3 | Tom | 4 | 1 | 1 | corte profundo |
| 4 | Palmas, aro… | 3 | 1 | 0 | arañazo |
| 5 | — | 2 | 1 | 0 | arañazo |
| 6 | — | 2 | 0 | 0 | arañazo |
| 7 | Charles | 1 | 0 | 0 | arañazo |
| 8 | Platillo | 1 | 1 | 0 | arañazo |

- **Cortan tres pads** desde la fase 9: bombo (profundidad 2), caja (3) y tom (1). Las etiquetas de tipo son del usuario; el comportamiento lo decide la tripleta.
- **Escala de referencia:** llegar al límite cuesta 11 notas. La caja (15) deja en semilla una formación en el límite.
- **El tipo es una etiqueta** que sale en la leyenda: lo que decide el comportamiento es la profundidad.
- **Columnas de la tabla:** `pad`, `reduccion`, `radio`, `profundidad`, `tipo` y `rol`. El motor las lee por nombre; `rol` es solo una nota. El pad 7 es el charles y el 8 el platillo: la columna `rol` de `perfiles_erosion` y de `colores_drum` se corrige al relanzar aunque la tabla esté editada, sin tocar el resto.
- **Al relanzar la fase 7:** si la tabla tiene los valores de la v1, la v3 o la v5 sin editar, se sustituye. Si está editada, se conserva y el informe avisa con `..` de que la columna `reduccion` ahora cuenta notas.

**El borde de la celda dice quién destruye** (v6). Las 8 losetas del borde de la rejilla de 3 × 3 de `luz_celda` son los 8 pads: el pad n a (n − 1) × 45°. El pad 1 queda al este, el 3 al norte, el 5 al oeste y el 7 al sur.

- **Cada golpe enciende el sector de su pad** en las celdas que erosiona, con el color del pad: plena intensidad en la celda objetivo, la mitad en el primer anillo y un cuarto en el segundo. Así la luz dibuja la huella del golpe. La intensidad se ve en el tamaño de la loseta, no en el color, que siempre es opaco y pleno.
- **Con secuenciador en la celda,** el centro conserva su color y el borde lleva el del pad: se ven los dos a la vez y sin mezclarse. **Sin secuenciador** (el golpe se desplazó a una vecina, o `Objetivo` en `velocidad`), solo se enciende el borde.
- **Varios pads a la vez en la misma celda:** cada uno en su sector, todos visibles.
- **Cuándo:** se apaga en `Vidabalizadrum` segundos (0,8). Con un bombo a negras a 120 BPM su sector está casi siempre encendido; los pads raros destellan casi un segundo.
- **Dónde se ve:** con formación, vacía o con huella, y también en modo actuación. Con formación, el borde queda fuera de la base de la pieza principal. Un macizo de fusión, que ocupa el 80 % de la celda, tapa parte de cada sector, pero el borde exterior asoma.
- **Lo que ya tiene significado queda a salvo:**
  - el latido aclara la formación, no la superficie;
  - el ámbar de las coronas, el cian de las cicatrices y el blanco del SEQ1 no están en la paleta de la batería;
  - el oscuro de la huella no puede confundirse con colores opacos y plenos.
- **Destello de la fase 9:** `luz_destello` usa también el color del pad, aclarado un 35 % con blanco para que siga siendo un golpe de luz.

**Colores:** tabla `colores_drum` (columnas `pad`, `r`, `g`, `b`, de 0 a 1, más `rol` para leer), editable a mano. Relanzar la fase no la pisa.

| Pad | Rol típico | Color | Hex |
|---|---|---|---|
| 1 | Bombo | rojo carmín | `#D7263D` |
| 2 | Caja | magenta | `#E83E8C` |
| 3 | Tom | violeta | `#7C3AED` |
| 4 | Palmas, aro… | azul ultramar | `#3B5BDB` |
| 5 | — | verde esmeralda | `#12B76A` |
| 6 | — | lima | `#A3E635` |
| 7 | Charles | rosa claro | `#F9A8D4` |
| 8 | Platillo | lila claro | `#C4B5FD` |

**Por qué las balizas salían todas del mismo color.** `make_instanced` enlazaba el color de las instancias a los parámetros `instancecolorr/g/b`. En el Geometry COMP de TouchDesigner se llaman `instancer/g/b` (página Instance 2), así que la geometría nunca leía los canales `r g b` y pintaba todo con el color del material. Ahora `estratos_comun.py` (comun v10) prueba los dos nombres y fija Color Mode = Replace. La autoprueba comprueba en `luz_celda` que el color por instancia está enlazado, y no solo las filas del motor.

**Ojo:** el mismo fallo afecta a todas las geometrías instanciadas creadas antes de comun v10: formaciones, coronas y estratos. También a la retícula de `fase12_base.py`, que no se relanza. Probablemente por eso pulidas y porosas se distinguían poco por color. Para que cojan su color hay que relanzar las fases que las crean (3, 4, 5 y 8), o poner a mano en cada una Instance 2 → Color R/G/B = `r` `g` `b` y Color Mode = Replace.

**Velocidad (propuesta, no implementada):** que la reducción escale con la velocidad del golpe, × (0,5 + vel/127): la mitad a velocidad 0, igual a 64 y 1,5 veces a 127. Con el desplazamiento de celda que ya hace la velocidad, quedaría como la única entrada expresiva de la batería. Pendiente de decidir.

**Presupuesto de densidad.** Por encima de `Umbraldensidad` (60 % de celdas ocupadas), el radio de todos los eventos se multiplica por `Multradio` (×2), y un radio 0 pasa a 1 para que también los arañazos ayuden a aligerar. La leyenda marca `x2` mientras dura.

**Decisión: dónde cae la erosión.** Los pads no tienen altura, así que no dicen celda. Opciones de `Objetivo`:

- `alterna` (defecto): los pads impares caen donde está el SEQ1, los pares donde está el SEQ2;
- `seq1` / `seq2`: siempre donde está ese secuenciador;
- `velocidad`: la velocidad del golpe elige una de las celdas.

En las tres primeras, la velocidad desplaza el golpe un semitono a un lado, al otro o a ninguno. La destrucción persigue a la construcción.

**Página Fase7:** `Canaldrum` 16 (confirmado con el aparato) · `Notabase` 36 · `Objetivo` · `Umbraldensidad` 0,6 · `Multradio` 2 · `Padprueba` · `Erosionar` · `Balizasdrum` (encendido: luz de la batería) · `Luzdrum` 1 (intensidad) · `Vidabalizadrum` 0,8. Al relanzar la fase 7:

- `Canaldrum` pasa a 16 solo si seguía en 10, y `Vidabalizadrum` a 0,8 solo si seguía en 0,6 o 1,0;
- se retiran `Tambalizadrum` y `Anillobalizadrum`. Las balizas (`balizas_drum`, `luz_drum` de la v5…) las retira cualquier fase al relanzarse.

**Por confirmar:** la nota del primer pad. Si los golpes salen como `pad fuera de 1-8`, ajusta `Notabase`.

**Leyenda:** `EROSION pad 1 temblor -2 notas radio 2 celda 52 densidad 64% x2`

**Relación con la fase 6:** mientras suena el bombo, cada temblor cambia la forma de muchas celdas y los ciclos se cierran por edad máxima. Al quitarlo, el mundo se asienta y se entierra por estancamiento: el breakdown entierra el mundo.

---

## FASE 8 · Conchas

En cada fin de ciclo:

1. **La capa se entierra** como una concha de losetas, una por celda, con el color de su generación. Las celdas que estaban ocupadas quedan más claras: los continentes se leen en el color. Sus formaciones se descartan.
2. **El planeta engorda el grosor de la concha.** Con `Grosortiempo` (encendido por defecto), el grosor es proporcional a lo que duró su mundo:

   ```
   grosor = min(Grosormax, Shellthick × clamp(compases / Ciclomin, 0,25, Ciclomax / Ciclomin))
   ```

   Con los valores por defecto va de 0,5 (ciclo mínimo, 8 compases) a 2,0 (32 compases o más: `Grosormax`). Sin ese tope, una concha de edad máxima (64 compases) mediría 4,0, más del doble que una formación en su límite (1,875). `Grosormax` 0 quita el tope. y un `Forzarciclo` temprano da como mínimo 0,125. Sin `Grosortiempo`, siempre `Shellthick`. El grosor de cada estrato registra cuánto tardó su mundo en agotarse.
3. **Herencia:** el 25 % de la ocupación de cada celda pasa a la capa nueva. La fracción que no llega a 1 se acumula para el ciclo siguiente: una celda con ocupación 2 en ciclos seguidos acaba heredando. Lo heredado vuelve a brotar desde la nueva superficie.

**Radio acumulado.** Cada concha guarda su `grosor`, `r_in` y `r_out`. El radio del planeta es el del núcleo más la suma de los grosores, y de él dependen las losetas (cada una con la altura de su concha), la retícula, la luz de celda, las formaciones, la cámara y la esfera del núcleo que tapa las conchas más allá de `Maxconchas`. Las conchas de un motor anterior se leen con `Shellthick`.

**Paleta de generaciones:** ámbar en la base, después grises minerales y negros que se alternan en claro y oscuro para que las bandas se distingan.

**Decisión: el horneado.** El marco pide hornear cada concha a una textura proyectada sobre una esfera. Aquí cada concha es una capa de losetas instanciadas, todas del mismo tamaño porque las celdas son de área igual:

- igual de barata: una sola geometría;
- sin shaders;
- en la fase 9 permite abrir cortes quitando losetas y ver las paredes de cada capa con su color, que es justo lo que pide la estratigrafía.

Solo se dibujan las últimas `Maxconchas` (24). Las anteriores quedan dentro de la esfera del núcleo, que crece para taparlas.

**Continentes** (en la leyenda): regiones de celdas vecinas ocupadas en al menos la mitad de las 8 últimas conchas.

**Cámara:** en esta fase solo se aleja con el radio para no quedar dentro del planeta. La definitiva llega en la fase 10.

**Página Fase8:** `Herencia` 0,25 · `Maxconchas` 24 · `Grosortiempo` (encendido) · `Grosormax` 2,0. Para probar sin esperar a que el mundo se estanque: `Forzarciclo` (página Fase6).

**Leyenda:** `CONCHAS 11 radio 11.50 ultima 0.75 herencia 25% continentes 3`

**Ritmo de engorde:** de media, `Shellthick` por cada `Ciclomin` compases: 0,5 cada 16 s a 120 BPM, unas 37 unidades en 20 minutos sobre un núcleo de 6. El radio es el tiempo transcurrido, salvo en los ciclos de más de 32 compases, que el tope de `Grosormax` recorta. Para frenar el engorde, sube `Ciclomin` o baja `Shellthick`.

---

## FASE 9 · Arqueología

**Cortes.** Los pads con profundidad mayor que 0 (por defecto el 2, la caja, y el 3, el tom) quitan las losetas de las conchas superiores en forma de **anfiteatro**: profundidad completa en la celda golpeada, un escalón menos en cada anillo. Las paredes son las capas enterradas, cada una con su color. El hueco es permanente; solo lo cubre la concha siguiente.

- **Las formaciones de una celda cortada** se apoyan en el fondo del corte.
- **Grosores distintos** (fase 9 v2): la profundidad se sigue midiendo en conchas. Como cada concha tiene el grosor de su ciclo, un corte de 3 conchas es más o menos hondo según lo que duraron esos mundos. El fondo baja la suma de los grosores quitados y las paredes usan el radio de cada concha.
- **Cicatriz:** el fondo y las paredes recién expuestos se ven en **cian** y se funden con el mineral en `Cicatriz` segundos.
- **Destello:** `luz_destello`, una luz puntual que sigue el giro del planeta, golpea la celda en cada destrucción: fuerte en los cortes, suave en los arañazos.
- **Luz del SEQ1:** el centro de su celda pasa a blanco, porque el cian queda reservado para lo recién expuesto. El destello toma el color del pad que golpea, aclarado.

**Página Fase9:** `Cicatriz` 4 s · `Destello` 3

**Leyenda:** `CORTE celda 41 3 conchas expuestas cicatriz 2.1 s`

---

## FASE 10 · Dirección visual

- **Cámara de superficie.** Órbita lenta (`Camvel`, 0,6 °/s: unos 10 minutos por vuelta), ajena al reloj del secuenciador, a `Camaltura` de la superficie. Mira a un punto del horizonte por delante: la curvatura se insinúa y el globo no se ve. Como la distancia es a la superficie, el encuadre no cambia y el crecimiento solo se nota por acumulación. Se controla con el nodo `objetivo` (Look At).
- **Plano final.** `Planofinal` aleja la cámara en 20 s, con curva suave, hasta ver el globo entero. Al quitarlo vuelve.
- **Luz.** Cenital fría que sube con el planeta, y un relleno azulado muy tenue. El eje sigue inclinado `Tilt` (20°).
- **Núcleo:** negro profundo.
- **Modo actuación.** `Modoactuacion` oculta la retícula y la leyenda (la luz de celda se sigue viendo: es parte del mundo): el switch `modo` pasa la salida al render limpio. Al quitarlo vuelve el modo diagnóstico.

**Página Fase10:** `Modoactuacion` · `Planofinal` · `Camaltura` 4 · `Camvel` 0,6

---

### Cómo comprobar el sistema completo

1. **PLAY con el SEQ1.** Las celdas que toca se siembran; las que repite crecen hasta el límite y después ramifican.
2. **Añade el SEQ2.** Aparecen torres; donde los dos se cruzan, híbridos.
3. **Deja tocar el SEQ1 sin batería.** La madurez sube, la novedad baja, el planeta frena el giro y el ciclo se cierra por `estancado`.
4. **Con batería constante,** los ciclos llegan a `edad maxima`. Al parar la batería, el mundo se asienta y se entierra.
5. **Añade la batería.** Los arañazos rebajan el paisaje y la densidad se mantiene por debajo del 60 %.
6. **Fin de ciclo.** El mundo se entierra, el planeta engorda y lo heredado vuelve a brotar.
7. **Pads 2 y 3 con varias conchas.** Se abre un corte con las capas a la vista, primero en cian.
8. **`Modoactuacion`, y al final `Planofinal`.**

---

### Problemas frecuentes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `No puedo leer .../estratos_motor.py` | `CARPETA` no apunta a la carpeta de los archivos | Corrige `CARPETA` al principio del script de fase |
| `FASE1 esta en la fase N. Aplica antes la fase N+1` | Fases saltadas | Aplícalas en orden |
| `FALLO en el motor: ...` en el Textport | Error dentro del motor | Pégame la línea; el resto de FASE1 sigue funcionando |
| Las notas no dejan formaciones | Línea de tiempo parada, o el `midi_callbacks` antiguo | Play en la línea de tiempo; si sigue, relanza la última fase aplicada |
| No se ve nada en `salida` | Un nodo de la cadena con error | Mira el bloque `DIAGNOSTICO DEL RENDER` del Textport y pégamelo |
| Formaciones tumbadas o metidas en el planeta | El orden de rotación de instancias no es X → Y | En cada geometría (`formas_*`, `coronas`, `estratos`): Instance → Rotate Order = `Rx Ry Rz` |
| El planeta da tumbos en vez de balancearse | El Rotate Order de la geometría (pestaña Xform) no es `Ry Rx Rz` | El informe lo avisa con `..`; ponlo a mano en esa geometría |
| Todas las formaciones del mismo color | Geometría creada antes de comun v10: el color por instancia no está enlazado | Relanza la fase que la crea, o en cada geometría: Instance 2 → Color R/G/B = `r` `g` `b`, Color Mode = Replace |
| Pulidas y porosas iguales | Los parámetros de brillo del Phong no se pudieron fijar | Sube Specular y Shininess en `mat_pulido` a mano |
| SEQ2 o batería `ignorado: canal X` | Canal distinto del de por defecto | `Canal2` (Fase5) o `Canaldrum` (Fase7) |
| Batería `pad fuera de 1-8` | Los pads no empiezan en do2 (36) | `Notabase` (Fase7) = la nota del pad 1 |
| La luz sale de un solo color | `luz_celda` no lee el color por instancia | Relanza cualquier fase (la recrea). Si persiste, en `luz_celda`: Instance 2 → Color R/G/B = `r` `g` `b` y Color Mode = Replace. El informe lo avisa con `FALLO luz_celda no lee el color por instancia` |
| No se ve la luz de una celda | `Luzseq` (centro) o `Balizasdrum` (borde) apagados, `Luzdrum` a 0, la batería o el secuenciador no llegan (mira las líneas `EROSION` y `NOTA`), o `luz_celda` fuera del render | Revisa esos; relanzar cualquier fase vuelve a meter `luz_celda` en el render |
| El mundo nunca se entierra por estancamiento | El bombo está sonando: cada temblor genera novedad | Es lo esperado; quita el bombo para que el mundo se asiente |
| Los ciclos siempre acaban por edad máxima | Batería constante, umbrales demasiado exigentes o un mundo que tarda en coronarse (carga) | Con batería es lo esperado. Si no, baja `Umbralmadurez`, sube `Umbralnovedad` o sube `Ciclomax`, y mira la tabla `ciclos` |
| Ciclos demasiado cortos | El mundo madura rápido (pattern al 100 %, pocas notas) | Sube `Ciclomin` o `Compasesquietos` |
| Ciclos sin tocar o que no terminan | Línea de tiempo parada, o un STOP posterior | Play en el proyecto; el ciclo se reanuda con la siguiente nota (la leyenda pone `parado`) |
| El planeta engorda demasiado rápido | Engorde = `Shellthick` por cada `Ciclomin` compases | Sube `Ciclomin` o baja `Shellthick` |
| `Cambioentierra` no hace nada | El BeatStep no envía All Notes Off al cambiar de pattern | Prueba pendiente con el aparato |
| El planeta no frena aunque el mundo esté quieto | `ritmo` sin el giro vivo, o `Girovivo` apagado | Relanza la última fase aplicada (parchea `ritmo`); mira que salga `ritmo: el giro se multiplica…` |
| La retícula no sube con las conchas | `reticula_chop` no se recocina | Se recocina sola en cada cambio de radio; si no, relanza la fase 8 |
| La cámara no mira al planeta (fase 10) | No se fijó Look At | En `camara`: Look At = `objetivo` |
| Rendimiento bajo con muchas conchas | Demasiadas losetas | Baja `Maxconchas` |

Las líneas `..` de los informes avisan de parámetros de TouchDesigner que el script no encontró con el nombre esperado. No impiden que funcione, pero dicen qué ajustar a mano.

---

### Decisiones tomadas por el camino

Las que el plan dejaba abiertas, con el valor por defecto que se ha elegido. Todas quedan como parámetro para cambiarlas.

| Fase | Pregunta | Decisión |
|---|---|---|
| 3 | ¿Incremento de altura por gate o fijo? | Por gate, con el fijo de respaldo (`Gatemode`) |
| 4 | ¿6 vecinas? | Hexagonal desplazada entre anillos completos; solape de arcos en los incompletos |
| 4 | ¿Quién elige la vecina? | Velocidad + ocupación (`Vecina`) |
| 4 | ¿Desborde en los polos? | El polo desborda a cualquiera de las celdas de su anillo |
| 5 | Canal del SEQ2 | 14 (`Canal2`), por confirmar |
| 6 | ¿Qué es un ciclo de ecosistema? | Lo cierra el mundo: maduro y quieto (`Umbralmadurez`, `Umbralnovedad`, `Compasesquietos`), entre `Ciclomin` y `Ciclomax` |
| 6 | ¿Cómo se cuenta el tiempo? | En compases del tempo del proyecto (`ritmo.tempo()`); ya no se deduce el paso de cada nota |
| 6 | ¿Una vuelta por ciclo? | No: `Barsperturn` manual y `Girovivo` |
| 6 | ¿Los satélites cuentan para la madurez? | No: madurez = formaciones propias en el límite. Su forma se recorta al llegar a `Limsatelite` |
| 7 | Canal y pads de la batería | Canal 16 (confirmado), pads desde 36 (`Notabase`), por confirmar |
| 3–7 | ¿Balizas? | Sin balizas: el centro de la celda muestra el secuenciador y el borde, la batería (un sector por pad, colores opacos) |
| 7 | ¿Qué deshace un golpe? | Notas de construcción, con la misma moneda que la fase 3; la mitad en cada anillo de vecinas |
| 7 | ¿Qué pads cortan? | Perfiles del usuario: bombo (1), caja (2) y tom (3), con profundidad 2, 3 y 1; 4 a 8 arañazos |
| 7 | ¿Dónde cae la erosión? | Alterna entre SEQ1 y SEQ2, desplazada por la velocidad (`Objetivo`) |
| 7 | ¿Radio 0 × 2? | Pasa a 1 |
| 8 | Horneado a textura | Capa de losetas instanciadas |
| 8 | Grosor de concha | Proporcional a la duración del ciclo (`Grosortiempo`), entre 0,25× y `Ciclomax`/`Ciclomin` × `Shellthick` (0,5; límite de altura 1,875), con un tope de `Grosormax` (2,0) |
| 3–4 | ¿Cuántas notas por trigger? | De 1 a `Costemax` (5) según la altura, con frenada; 5 desde el límite. La presión suma carga |
| 3 | ¿Cómo se reparten las notas? | `Notapolosur` y `Notapolonorte` (entre do1 y do8) son los polos; en medio, un anillo por octava; el rango decide el número de celdas; `Fuerarango` para las de fuera |

### Cómo se ha probado

Sin TouchDesigner a mano, todo se ha probado en simulación:

- **El motor:** 18 pruebas. Orientación de las piezas sobre la normal de cada celda, vecindad simétrica, crecimiento y límite, gate, desborde y estados, híbridos, ráfagas con y sin STOP, ciclos y conchas, orden de la erosión y presupuesto, cortes y cicatrices, herencia y continentes, y que el mundo se pueda guardar.
- **El ciclo de la fase 6 v2** (motor v11):
  - Mundo vacío: no cierra nunca por `estancado`; cierra por `edad maxima` en `Ciclomax`.
  - Celdas coronadas que siguen recibiendo notas: novedad 0 y cierre por `estancado` en `max(Ciclomin, 1 + Compasesquietos)`.
  - Erosión en cada compás: no hay estancamiento y cierra por `edad maxima`.
  - Secuenciador parado: no hay cierres.
  - `Forzarciclo` cierra al instante (`forzado`) y escribe en la tabla `ciclos`.
  - `Cambioentierra`: una ráfaga antes de `Ciclomin` se aplaza hasta `Ciclomin`, una después cierra en el compás siguiente, y con el toggle apagado solo sale el AVISO.
  - Grosor proporcional con sus dos límites; radio = núcleo + suma de grosores; fondo y paredes de los cortes con grosores distintos.
  - `Girovivo` acotado entre `Giromin` y 1.
  - Un mundo del motor v7-v10 carga y sigue funcionando.
- **Fase 7 v3:**
  - Perfiles nuevos: el pad 1 resta 1 en radio 2 sin abrir corte; los pads 2 y 3 abren cortes desde el nivel 9; ningún otro pad corta.
  - Relanzar sustituye una tabla con los valores de la v1, conserva una editada a mano y no pisa un `Canaldrum` cambiado a mano.
  - Luz de celda (motor v18):
    - la nota del SEQ1 enciende el centro de su celda en su color y queda tenue hasta la siguiente; la del SEQ2, en ámbar; con los dos en la misma celda, el centro se parte y se ven los dos;
    - desde la fase 9, el SEQ1 en blanco;
    - golpe en la celda del SEQ1: el centro conserva su color y el borde muestra el del pad;
    - 8 pads a la vez: 8 sectores de 8 colores, y `luz_celda` lee el color por instancia;
    - golpe sin secuenciador: solo el borde;
    - la luz se ve con formación, vacía y con huella, gira con el planeta y sube con el radio;
    - no queda ninguna baliza en escena ni en `CHOP_NAMES`;
    - los pads 1, 2 y 3 cortan.
  - Fase 7 v5: el golpe ilumina la celda con el color de su pad y su radio más tenue, y se apaga a tiempo; dos pads dan dos colores y `luz_drum` lee el color por instancia; la luz se ve con formación, vacía y con huella; el pad 7 repetido con el SEQ1 tocando deshace una nota por golpe y la celda sigue creciendo; N notas de construcción y N de erosión devuelven la celda; la celda objetivo pierde más que sus vecinas; las balizas de la v3 desaparecen.
  - Balizas de la batería (v4, retiradas en la v5) fuera de la silueta del SEQ1 y del SEQ2 (en reposo y en el pulso), en el ecuador, junto al polo y en el polo, y con el SEQ2 en la celda vecina; las 8 de una celda sin tocarse; tamaño entre 0,18 y 0,30, por encima del mínimo perceptible (0,15) y por debajo del SEQ2 en reposo (0,495).
  - Balizas de la batería: los 8 pads en la misma celda encienden 8 balizas, cada una en su hueco y con su color; se apagan en `Vidabalizadrum`; ninguna es cian, ámbar ni blanca; giran y se balancean con el planeta; `Padprueba` + `Erosionar` también las encienden; `Modoactuacion` las oculta.
  - Bombo a negras durante 16 compases sobre un mundo maduro: ningún cierre por `estancado`. Al quitarlo, cierre por `estancado` unos 30 compases después (20 con `Umbralnovedad` 0,10).
- **Sesión simulada de 192 compases** a 120 BPM: SEQ1 de 16 pasos al 90 %, SEQ2 de 13 y batería a tramos de 48 compases. Cierra por `estancado` en los tramos sin batería y por `edad maxima` en los tramos con batería.
- **Los scripts:** las fases 1 y 2 reales y las 3 a 10, ejecutadas en orden contra un TouchDesigner simulado, todas con `AUTOPRUEBA OK`. También se comprueba que no se puede saltar una fase y que relanzar una no borra el mundo.
- **Una sesión simulada:** 24 compases a 120 BPM con SEQ1 (16 pasos), SEQ2 (13) y batería, fotograma a fotograma. Detecta las dos longitudes, entierra conchas, y todas las expresiones de los nodos se evalúan sin error.

Lo que la simulación no puede comprobar son los nombres exactos de algunos parámetros de TouchDesigner (orden de rotación y modo de color de las instancias, brillo del Phong, Look At). Los scripts los intentan con los nombres habituales y avisan con `..` si no los encuentran. La tabla de problemas dice dónde ponerlos a mano.

### Pruebas pendientes con el aparato

1. **All Notes Off:** cambiar de pattern dos veces y pulsar STOP, y copiar las líneas AVISO.
2. **RANDOMNESS:** comprobar si cambia la velocidad (columna `vel` de `midi_log`).
3. **Canal del SEQ2 y nota del pad 1.**
4. **Ciclos reales:** SEQ1 al 100 % sin batería; SEQ1 al 60 % con SEQ2 de 13 pasos; con batería constante. Copiar la tabla `ciclos` de cada caso para afinar `Umbralmadurez`, `Umbralnovedad`, `Compasesquietos` y `Ciclomax`.
5. **Quitar el bombo:** con un mundo maduro y el bombo sonando, quitarlo y comprobar en cuántos compases se cierra el ciclo por `estancado` (en simulación, unos 30).

---

### Después de la fase 10

Fuera de este montaje: entrada por ethernet (OSC/UDP) como generador o modulador adicional; puente OSC hacia Unreal para el formato instalación (la tabla de ocupación y los eventos del motor son exactamente lo que habría que enviar); extensión física a motores.
