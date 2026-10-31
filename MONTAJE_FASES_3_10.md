# Estratos · Montaje
## Fases 3 a 10: de la baliza al planeta estratificado

*Continúa `MONTAJE_FASE1.md` (fases 1 y 2, ahora en un solo script: `fase12_base.py`). Plan de referencia: `PLAN_FASES.md`. Sigue en `MONTAJE_FASES_11_18.md` (la piel temática, desde la fase 11).*

---

### Estado en una frase

Cada nota del SEQ1 y del SEQ2 deposita y hace crecer formaciones sobre el planeta. Al toparse con el límite de altura se ramifican, se fusionan y se coronan. La batería las erosiona, salvo el bombo y el tom, que las hinchan al golpe y les dan más techo (fase 7 v12). Cuando el mundo madura y deja de cambiar (o llega a su edad máxima) se entierra como una concha nueva, tan gruesa como lo que duró, y los cortes profundos dejan ver las capas enterradas.

---

### Archivos

Todos en la misma carpeta: `C:/Users/DareDave/Downloads/est`.

| Archivo | Para qué | Versión |
|---|---|---|
| `fase12_base.py` | Fases 1 y 2 en uno: núcleo, retícula de polo a polo, luz de celda (v3: sin baliza), MIDI, render y leyenda (v5: letra de 9 y `Leyenda` para ocultarla; v6: cámara de globo sobre el núcleo). Lleva dentro el arreglo del render. Su `ritmo` ya sabe del giro vivo (en un proyecto en marcha lo parchea `estratos_comun.py`) | `fase12 v6` |
| `estratos_motor.py` | La lógica entera del mundo. Lo cargan las fases; no se ejecuta solo. Desde la v27 lleva también la piel y el tejido de las fases 11 a 13 (ver `MONTAJE_FASES_11_18.md`); la v31 quita un bucle de cocinado de la cámara; la v33, el encuadre cercano (el planeta y `Holguraaltura`; solo cambia con una concha nueva); la v34 y la v35, las fases 14 y 15 (ver `MONTAJE_FASES_11_18.md`); la v36, un solo parámetro de encuadre (`Encuadre`); la v37, la compactación de las conchas (`Cortezamax`, ver «Calibración de la vista» en `MONTAJE_FASES_11_18.md`); la v38, la fase 16; la v39, la fase 17; la v40, la fase 18; la v41, la fase 19; la v42, el rango -10..10 V; la v43, el impulso del bombo y el tom (fase 7 v12); la v44, el pumping en seco (fase 7 v13); la v45, los pulsos de ocupación del impulso (fase 7 v14); la v46, la naturaleza legible y los ríos azules (fase 11 v5 y fase 13 v2; la paleta de conchas reserva de 120 a 275 grados); la v47 quita `Planofinal` (fase 10 v11); la v48, los árboles de pisos (fase 11 v6); la v49, sus ramas desde el tercio superior del tronco (fase 11 v7); la v50, ríos que se ven (fase 13 v3); la v51, ríos más vivos (fase 13 v4) | `motor v51` |
| `estratos_comun.py` | Piezas compartidas por los scripts de fase; no se ejecuta solo; desde la v15 pone la cámara de globo en todas las fases; la v16 añade la luz de los secuenciadores en las conchas; de la v17 a la v19, las geometrías, el shader y el tejido de las fases 11 a 13; la v20 fija el color de las luces por su nombre real (`cr cg cb`); la v22 gira las marcas de la retícula desde el motor; la v23 pone `Encuadremargen` a 1,02 y la piel al día al relanzar; la v24 añade `Holguraaltura`; la v25 y la v26, las fases 14 y 15; la v27 sustituye `Encuadremargen` y `Holguraaltura` por `Encuadre`; la v28 devuelve a cero el giro y el pivote de la cámara al relanzar; la v29, la calibración de la vista (`Ciclomin` 16, `Compasesquietos` 3, `Grosormax` 1,5 si seguían por defecto, y `Cortezamax`); la v30, la fase 17 (ventanas por edificio, color de la luz desde el motor); la v31, la fase 18; la v32, la fase 19 (niebla y glitch en el shader); la v33, el terreno, los pisos, el borde tintado y el agua (fase 11 v5 y fase 13 v2); la v34, el diagnóstico de los ríos (fase 13 v3); la v35, el agua más viva (fase 13 v4) | `comun v35` |
| `fase3_semilla.py` | Carga y frenada, semilla, crecimiento, material, balanceo del eje, polos y anillos, luz de celda, latido con el gate (v12: su autoprueba también vale relanzada en la fase 11; v13: la página Fase3 con 16 parámetros en vez de 22, ver «Página Fase3») | `fase3 v13` |
| `fase4_desborde.py` | Desbordamiento con carga, satélites, fusión, coronación, cumbre (v7: autoprueba válida en la fase 11) | `fase4 v7` |
| `fase5_especies.py` | SEQ2, arquitectura, híbridos, luz ámbar del SEQ2; v3: `Filtrar2` y `Nota2`; v4: los parámetros del SEQ2 pasan a la página Fase2 y desaparece la página Fase5 | `fase5 v4` |
| `fase6_ciclo.py` | El ciclo lo cierra el mundo: madurez, novedad, territorio, tabla `ciclos`, giro vivo (v5: eras más largas, `Ciclomin` 16 y `Compasesquietos` 3) | `fase6 v5` |
| `fase7_erosion.py` | Canal 16; erosión en notas; perfiles del usuario; el golpe se ve como una nota (celda y formación); erosión con la velocidad; huellas, presupuesto (v10: autoprueba válida en la fase 11; v12: el bombo y el tom, impulso de creación; v13: pumping en seco, pico al instante; v14: pulsos de ocupación en lugar de capacidad, pumping solo visual con tope y luz con su curva) | `fase7 v14` |
| `fase8_conchas.py` | Conchas con el grosor de su ciclo, herencia, radio nominal; el mundo enterrado se deposita sobre la columna de cada celda (`Colmatacion`, zócalo); cámara de globo; luz de los secuenciadores en las conchas; un color por concha (`Paleta`); v9: desde la fase 15, las conchas con el shader de la piel; v10: la corteza se compacta (`Cortezamax`) y `Grosormax` 1,5; v11: solo la autoprueba (la paleta reserva también los verdes de los pisos y el azul de los ríos, motor v46); v12: conchas discretas (suelo oscuro, poco contraste ocupada/vacía, tapa neutra; `Paletaluz`, `Paletaalterna`, `Contrasteocupada`, `Tapaneutra`, `Tapaluz`, motor v53) | `fase8 v12` |
| `fase9_arqueologia.py` | Cortes en la columna de cada celda, tope por mundo, el núcleo como fondo, estratigrafía, cicatriz cian que se funde con el color de su concha, destello (v8: del color de su pad de verdad, ver abajo; v9: la autoprueba mide sin compactar; v10: el bombo y el tom ya no cortan, su destello es suave y sigue el pumping; v11: la autoprueba, con el pumping en seco) | `fase9 v11` |
| `fase10_direccion.py` | Paleta, luz cenital, cámara de globo (por defecto) o de superficie, modos (v7: la luz cenital fría y el relleno azulado, de verdad; v10: `Encuadre`, el alto del planeta en la pantalla; v11: sin `Planofinal`) | `fase10 v11` |

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
| `luz12_callbacks`, `i_luz_celda`, `luz_celda` | Luz de celda de las fases 1 y 2 (fase12 v3; en la v2 era la baliza cian) | El motor calcula las losetas: `i_luz_celda` pasa a `formas_callbacks` y `luz12_callbacks` se retira. La leyenda NOTA la da el motor. Un proyecto hecho con la fase12 v2 pierde aquí su `baliza` |
| `reticula_callbacks` | Radio fijo 6 | Marcadores sobre la superficie actual (suben con las conchas) |
| `rotulo` | Tempo + nota | Tempo + nota + motor |

**No relances `fase12_base.py` sobre un proyecto en marcha**: crea una FASE1 nueva y vacía (la vieja queda como `FASE1_anterior`, apagada) y obliga a aplicar de nuevo las fases 3 en adelante. Para refrescar el motor, relanza la última fase aplicada.

**Diagnóstico del render.** `fase12_base.py` y cada fase terminan con un bloque `DIAGNOSTICO DEL RENDER`: qué geometrías dibuja el render, con qué cámara y luces, y qué nodos de la cadena hasta `salida` tienen errores (motor, Script CHOP, rótulo…). Si no ves la imagen, pégame ese bloque. Las leyendas ya no pueden romper la salida: si fallan, escriben el fallo en el rótulo.

---

## FASE 3 · La semilla

Cada nota del SEQ1 suma 1 a la **carga** de su celda. Cuando la carga llega al **coste**, se dispara un **trigger de construcción**: la ocupación sube 1 y la carga vuelve a 0. La ocupación cuenta triggers, no notas.

- **El coste sube con la altura** (motor v8). Es 1 abajo y `Costemax` (5) en el límite: coste = 1 + ⌊(`Costemax` − 1) × altura / límite⌋, con la altura nominal de la ocupación actual. Desde el límite, cada trigger cuesta `Costemax` (ramificación, fusión, coronación y cumbre).
- **Frenada:** cada nota sube la formación un escalón × límite / coste. El escalón no es un parámetro (desde la v13; antes `Growstep`): lo calcula el motor, (1 − `Semillafrac`) / (`Umbralram` − 1), para que la formación suba a escalones iguales de la semilla al límite sin saltos (0,2 con los valores por defecto). Un trigger completo sube siempre un escalón, pero repartido entre más notas conforme la formación crece, así que cuanto más alta, más despacio.
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

- **El gate decide cuánto crece** (`Gatemax` > 1; con `Gatemax` 1 el gate no cuenta, lo que antes era `Gatemode` apagado). Al llegar el note off se mide cuánto duró la nota respecto a un paso: un gate al 50 % da el crecimiento normal, un gate corto la mitad o menos (hasta ¼) y uno ligado como mucho `Gatemax` veces (1,25; antes era el doble). Sin note off, crecimiento normal. Se aplica al trozo de escalón de cada nota y no cambia la carga.
- **Techo del escalón** (motor v9): la altura nunca pasa del escalón que se está construyendo. Ni un gate ligado ni la presión de una vecina adelantan la altura a los triggers. Antes, con gates largos, una formación podía tocar el límite con la mitad de las notas.
- **Material**: la velocidad de la primera nota decide (`Umbralvel`, 64) y no vuelve a cambiar. Desde motor v10 la diferencia no depende solo del brillo, que en cajas pequeñas apenas se veía:
  - **Pulido** (por encima): color claro y frío, prismas limpios y algo más esbeltos; en arquitectura, plantas casi pegadas (torre de cristal). `mat_pulido` tiene un reflejo blanco ancho y fuerte (especular 1, brillo 14) y algo de ambiente.
  - **Poroso** (por debajo): color oscuro y terroso. Cada pieza se rompe en 2–3 tramos de ancho irregular, con grietas entre ellos y grumos pegados; en arquitectura, plantas desiguales y descolgadas (hormigón). `mat_poroso` no tiene reflejo.
  - Relanzar la fase 3 o la 4 reajusta los dos materiales.
- **Animación**: la altura visible se acerca a la real en ~0,1 s; las formaciones brotan, no aparecen de golpe.
- **Balanceo del eje** (v2): además del giro al tempo, el eje se balancea hacia la cámara y en contra, `Balanceo` grados (60) cada `Balanceoper` segundos (90), para ver los dos polos. Va aparte del reloj del secuenciador y se congela con `Pausa`. `Balanceo` 0 lo apaga (desde la v13; antes `Rotextra`); entra y sale en 3 s, sin saltos. Lo llevan todas las geometrías que giran con el planeta (núcleo, retícula, luz de celda, formas, coronas, estratos) y la luz de destello. Orden de rotación: `Ry Rx Rz` (giro, balanceo, inclinación).

**Luz de celda** (fase 3 v9, motor v18). No hay balizas: ni la del SEQ1, ni la del SEQ2, ni las de la batería. Cada celda cuenta con luz lo que le está pasando, en una rejilla de 3 × 3 losetas opacas a ras de su superficie (geometría `luz_celda`, Script CHOP `i_luz_celda`, material `mat_luz_celda`). La crea y la mantiene cualquier fase al relanzarse, que también retira las balizas de las versiones anteriores.

- **El centro dice quién construye:** el color del secuenciador que acaba de tocar la celda. SEQ1 cian (blanco desde la fase 9: el cian queda para las cicatrices) y SEQ2 ámbar (fase 5).
  - **El gate manda** (motor v20). Mientras la nota está pulsada, del note on al note off, la loseta brilla a plena luz y crece en alto. Al soltarla se apaga en un cuarto de segundo hasta el reposo: la última celda de cada secuenciador queda tenue (70 % del color) hasta su siguiente nota, para que se vea dónde está cada uno. Una nota corta da un destello; una ligada, una celda encendida todo lo que suena. Una nota sin note off cuenta como pulsada 2 s como mucho.
  - **Más evidente** (v20): la loseta mide un 34 % de la celda (antes 26 %) y sube hasta 0,28 de alto con el gate.
  - **Los dos en la misma celda:** el centro se parte en dos mitades, SEQ1 al oeste y SEQ2 al este.
  - **Con formación,** el centro se ensancha hasta asomar alrededor de su base: se enciende el pie de la formación y se lee desde la cámara aunque la formación sea alta. La luz va en la superficie, no en la punta, así que el ámbar del SEQ2 no se confunde con las coronas.
  - **El latido sigue al gate** (v20). Mientras la nota suena, la formación se hincha un 12 % (antes 5 %), se aclara y se tiñe del color de su secuenciador (cian o blanco el SEQ1, ámbar el SEQ2). Al soltarla, vuelve a su color en ~0,25 s. Con la loseta del centro, la construcción que suena se ve de lejos.
  - **En las fases 1 y 2** (`fase12_base.py`) no se escucha el note off: la luz es un pulso de 0,25 s con cada nota, del mismo tamaño y brillo.
- **La batería se ve igual** (fase 7, motor v21): cada golpe ilumina el centro de la celda y su formación con el color de su pad. Si coinciden en la celda, manda la luz más intensa en ese instante.
- **La luz del secuenciador llega a las conchas de la celda** (desde la fase 8; motor v25, comun v16). Con muchas conchas, y más con la cámara de globo, el centro de la celda se pierde entre las bandas de las losetas. Por eso una nota también tiñe tenuemente las losetas de su celda, que la ocupan entera:
  - **Qué se tiñe:** las losetas dibujadas de la columna de la celda, de arriba abajo: la superior con toda la luz y menos en cada una, hasta apagarse en la cuarta. En las paredes de un corte se siguen leyendo los colores de cada estrato. El zócalo no se tiñe. En una celda en el fondo de un corte se tiñe la loseta del fondo hacia abajo; las paredes vecinas son de otras celdas y no se tiñen.
  - **Pulso y reposo**, como el centro: un pulso con cada nota (0,35) y, mientras es la última celda de ese secuenciador, un reposo tenue (0,10). Es un tinte, no un foco. `Luzconchas` es la intensidad: 0 la apaga, 1 da esos valores y 2 el doble (desde la fase 3 v13; antes un interruptor y `Luzconchaspulso`, `Luzconchasreposo` y `Luzconchasalcance`).
  - **Cómo:** es una capa de **luz aditiva** (geometría `luz_conchas`, Script CHOP `i_luz_conchas`, material constante `mat_luz_conchas` con mezcla aditiva) que envuelve las losetas. Suma el color del secuenciador sin tocar el de la generación ni la diferencia entre loseta ocupada y vacía, se ve igual en la cara en sombra y en las paredes de una hondonada, y nunca oscurece ni tapa: el centro de la celda, la luz de la batería y las formaciones siguen encima.
  - **El reposo respira** (entre el 70 % y el 100 %, cada 2,4 s). Una loseta ocupada es más clara pero quieta: el reposo blanco del SEQ1 no se confunde con ella.
  - **La cicatriz manda:** una loseta en cian por un corte reciente no se tiñe.
  - **Los dos secuenciadores en la misma celda:** una loseta tiene un solo color, así que manda el más encendido y, si empatan, el último que ha tocado.
  - **El SEQ2 sobre una concha de tono parecido:** como la luz se suma, el pulso aclara la loseta además de teñirla, y se nota aunque el color sea parecido. Con la paleta de generaciones ninguna concha es ámbar (la banda del SEQ2 está reservada); con `Paleta` mineral, la base sí lo es.
  - **Rendimiento:** solo se calculan las losetas de las celdas en pulso o en reposo (como mucho 8 filas por fotograma). Las dos mil losetas de las conchas no se recalculan.
  - Se ve también en modo actuación. `Luzconchas` apagado deja las conchas como antes.
- **Sin transparencias en la superficie:** cada zona del centro lleva un color opaco, así que no se mezclan y no hay problemas de orden de dibujo. La única capa aditiva es la luz de las conchas, que se dibuja la última.
- **Interruptores:** `Luzseq` (página Fase3) para el centro, `Luzconchas` (página Fase3) para las conchas y `Balizasdrum` (página Fase7) para la batería. Las tres luces son parte del mundo y se ven también en modo actuación.

**Página Fase3** (16 parámetros desde la v13):

| Para qué | Parámetros |
|---|---|
| Montaje: el teclado y la retícula | `Notapolosur` 24 · `Notapolonorte` 108 · `Fuerarango` |
| Montaje: escala y ritmo de crecimiento | `Shellthick` 0,5 · `Alturafactor` 3,75 · `Semillafrac` 0,20 · `Costemax` 5 · `Gatemax` 1,25 (1 = el gate no cuenta) · `Umbralvel` 64 |
| Montaje: luz y movimiento con el proyector | `Luzseq` · `Luzconchas` 1 (intensidad; 0 apagada) · `Balanceo` 60 (0 = apagado) · `Balanceoper` 90 |
| Pruebas | `Velprueba` 100 · `Sembrar` · `Resetmundo` |

**Quitados en la v13** (relanzar cualquier fase los borra de un proyecto anterior conservando lo que hacían):

| Antes | Ahora |
|---|---|
| `Growstep` | Lo calcula el motor: (1 − `Semillafrac`) / (`Umbralram` − 1). Es lo que ya ponía `ajuste_vista.py` |
| `Gatemode` | `Gatemax` 1. Si estaba apagado, `Gatemax` pasa a 1 |
| `Rotextra` | `Balanceo` 0. Si estaba apagado, `Balanceo` pasa a 0 |
| `Luzconchaspulso`, `Luzconchasreposo`, `Luzconchasalcance` | `Luzconchas` pasa de interruptor a intensidad: `Luzconchaspulso` / 0,35 (0 si estaba apagado). El reposo es siempre 0,10 × `Luzconchas` y el alcance, 4 losetas |

Los tres últimos los crea ya `fase12_base.py` en esta página; si venían de la página Fase1 (versión anterior), la fase 3 los mueve aquí conservando su valor.

**Leyenda:** `MUNDO ocupadas 23/85 (27%) max 4 fase 3`, `RANGO do1 24 (polo sur) a do8 108 (polo norte) 85 celdas fuera: plegar` y `ULTIMA geo celda 40 ocupacion 3 crecimiento carga 1/3`. `Sembrar` también escribe la carga en el Textport.

**Proyecto en marcha:** al relanzar la fase 3 o la 4, `Alturafactor`, `Semillafrac` y los umbrales de la fase 4 pasan a sus valores nuevos solo si seguían en el valor de antes. Lo que hayas ajustado a mano se queda como está; las líneas `..` del informe dicen qué ha cambiado. En la línea NOTA: `celda 40 de 85 anillo 4`, y `(como do1 24)` si la nota se ha plegado.

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

**Parámetros del SEQ2** (fase 5 v4): ya no hay página Fase5. Viven en la **página Fase2**, debajo de los del SEQ1: `Canal` 13 · `Filtrar` · `Nota` · `Canal2` 14 · `Filtrar2` · `Nota2` · `Sembrar2`. Los tres del SEQ2 son los mismos que los del SEQ1. Un proyecto anterior se migra solo al relanzar la fase 5: los parámetros se mueven conservando su valor y la página Fase5, ya vacía, se quita. Con dos secuenciadores en la página, las etiquetas de `Filtrar`, `Nota`, `Filtrar2` y `Nota2` llevan (SEQ1) o (SEQ2).

- `Canal2`: canal MIDI del SEQ2.
- `Filtrar2` ("Solo ese canal (SEQ2)", encendido): apagado, cualquier canal cuenta como SEQ2, salvo el del SEQ1 (`Canal`, si `Filtrar` está encendido) y el de la batería (`Canaldrum`).
- `Nota2` ("Última nota SEQ2"): la actualiza cada nota que llega del SEQ2; también se puede mover a mano, y es la que siembra `Sembrar2`.

**Por confirmar:** el canal del SEQ2. Si sus notas salen en el Textport como `ignorado: canal X`, pon X en `Canal2` (página Fase2).

**Leyenda:** `SEQ2 canal 14 notas 37 hibridas 3`

---

## FASE 6 · El ciclo: lo cierra el mundo

*fase6 v4 (motor v22). La v2 sustituyó a la v1, que deducía el ciclo de la longitud de los patterns; la v4 hace que la edad máxima solo entierre un mundo con el territorio ocupado.*

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

**El bombo y el ciclo.** Cada temblor del bombo (fase 7) cambia la forma de muchas celdas a la vez, las que están por debajo de la corona. Mientras suena, la novedad no baja del umbral y el mundo no se estanca. Desde la fase 6 v4 tampoco se entierra por edad máxima mientras la batería no deje llenar el territorio: un mundo medio vacío ya no se entierra solo por llevar `Ciclomax` compases. Al quitar el bombo, el mundo se asienta y se entierra por estancamiento. Dicho en términos de directo: **el breakdown entierra el mundo**. En simulación (fase 6 v4, `Umbralnovedad` 0,15, `Compasesquietos` 2), el mundo se entierra unos 24 compases después de 16 compases de bombo a negras, porque antes vuelve a crecer lo erosionado.

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

**Territorio** (fase 6 v4). La edad máxima solo entierra un mundo lleno:

```
territorio = celdas tocadas por SEQ1 o SEQ2 en los últimos Compasesterritorio compases, más sus vecinas
ocupación  = celdas del territorio con ocupación > 0 / celdas del territorio   (0 si el territorio está vacío)
```

- Cada nota de un secuenciador apunta su celda con el compás en que llegó. Al pasar `Compasesterritorio` compases (8) sin volver a tocarla, la celda deja de contar.
- La batería no crea territorio: solo lo vacía. Con batería constante, el territorio no se llena y el mundo sigue pasado `Ciclomax`. La leyenda lo dice con `esperando territorio`.
- **No hay tope de seguridad.** Si el territorio no se llena, el mundo no se entierra por edad máxima; lo enterrarán el estancamiento al quitar la batería, `Cambioentierra` o `Forzarciclo`.
- En cuanto el territorio llega a `Umbralterritorio`, el ciclo se cierra en ese mismo compás.
- El grosor de la concha (fase 8) ya está acotado en `Ciclomax` / `Ciclomin` × `Shellthick` y en `Grosormax`: un ciclo de 200 compases da la misma concha que uno de 48 (con los valores por defecto de la fase 8 v10).

**Cierre del ciclo.** Va por orden; nunca antes de `Ciclomin`, salvo con `Forzarciclo`:

| Motivo | Cuándo |
|---|---|
| `cambio de pattern` | Hubo una ráfaga de All Notes Off sin STOP con `Cambioentierra` encendido. Se aplica en cuanto se llega a `Ciclomin` |
| `estancado` | `Compasesquietos` compases seguidos con madurez ≥ `Umbralmadurez` y novedad ≤ `Umbralnovedad` |
| `edad maxima` | El mundo lleva `Ciclomax` compases o más **y** su territorio está ocupado (≥ `Umbralterritorio`). La novedad no cuenta |
| `forzado` | Pulso `Forzarciclo`: cierra al instante |

Cada cierre emite el evento `fin_de_ciclo` (ciclo, compases, segundos, motivo, madurez, novedad, territorio), escribe `AVISO fin de ciclo N: <motivo> a los C compases` en el Textport y añade una fila a la tabla `ciclos`. Desde la fase 8, además entierra el mundo.

Con `Nivel` 6 o 7 el evento solo informa: el mundo no se entierra, así que puede seguir maduro y quieto y volver a cerrarse cada `Ciclomin` compases. Es lo esperado. Si `Ciclomax` < `Ciclomin`, el informe avisa con `..` y se usa `Ciclomax` = `Ciclomin`.

**Cambio de pattern.** Ahora solo se detecta por la ráfaga de All Notes Off (CC 123 en 8 canales o más en 0,12 s) sin STOP. Ya no se detecta por las notas: eso dependía de la biblioteca, que desaparece. Con `Cambioentierra` apagado, la ráfaga solo da el AVISO.

**Giro vivo.** `Barsperturn` vuelve a ser manual para siempre; si tenías `Turnauto`, se queda el valor que tuviera. Con `Girovivo`, el giro del núcleo se multiplica por un factor:

```
objetivo    = clamp(novedad / (4 × Umbralnovedad), Giromin, 1)
giro_factor → objetivo, suavizado en un compás
```

El planeta se frena a medida que el mundo deja de cambiar (justo antes de enterrarse casi se detiene) y vuelve a acelerar con la novedad. El giro sigue acumulándose, así que el cambio de factor no hace saltar el planeta. El factor lo lee `ritmo`; `estratos_comun.py` le añade esa lectura al relanzar cualquier fase, sin perder el ángulo acumulado.

**Tabla `ciclos`.** Una fila por ciclo cerrado: `ciclo`, `compases`, `segundos`, `motivo`, `madurez`, `novedad`, `grosor` (desde la fase 8) y `territorio` (fase 6 v4: la ocupación del territorio al cerrar). Guarda las últimas 200. Al relanzar la fase 6, una tabla antigua gana las columnas que le faltan sin perder filas. Sirve para afinar los umbrales con el aparato.

**Página Fase6:** `Umbralmadurez` 0,6 · `Umbralnovedad` 0,15 · `Compasesquietos` 3 · `Ciclomin` 16 · `Ciclomax` 64 (*Edad maxima (si el territorio esta lleno)*) · `Umbralterritorio` 0,8 (*Territorio ocupado para la edad maxima*) · `Compasesterritorio` 8 (*Compases de memoria del territorio*) · `Negrasporcompas` 4 · `Cambioentierra` (apagado) · `Girovivo` (encendido) · `Giromin` 0,25 · `Forzarciclo`

Al relanzar la fase 6 v4, `Umbralnovedad` pasa de 0,05 a 0,15 y `Compasesquietos` de 4 a 2 solo si seguían en el valor anterior por defecto (desde la fase 6 v5 y comun v29, `Ciclomin` pasa de 8 a 16 y `Compasesquietos` de 2 a 3, también solo si seguían por defecto, al relanzar cualquier fase); `Umbralmadurez` sigue en 0,6. La fase 6 v2 quita los parámetros obsoletos: `Repsporciclo`, `Modociclo`, `Turnauto`, `Longmanual`, `Longfija`, `Longmin`, `Pasosporcompas`, `Pasospornegra` y `Resetpatterns`.

**Leyenda:**

```
CICLO    5   compas 23 (8-64)   madurez 64%   novedad 3%   quieto 1/2   territorio 62% (80%)   giro x0.40
CICLO    1   compas 199 (8-64)   madurez 50%   novedad 33%   quieto 0/2   territorio 13% (80%)   giro x0.56   esperando territorio
AVISO    fin de ciclo 4: estancado a los 19 compases
```

`territorio` es la ocupación del territorio y, entre paréntesis, `Umbralterritorio`. `esperando territorio` sale cuando el mundo ya pasó `Ciclomax` y no se entierra porque el territorio no está ocupado. Con el secuenciador parado, en lugar del compás pone `parado`.

**Ojo con el ritmo de crecimiento.** Con la carga por celda de las fases 3 y 4, una formación necesita 31 notas para coronarse. En simulación, un SEQ1 de 16 pasos sin batería madura y se queda quieto hacia el compás 30-40. Por eso `Ciclomax` es 64 (fase 6 v3; con 32 casi todos los ciclos cerraban por `edad maxima`). Al relanzar la fase 6, `Ciclomax` pasa de 32 a 64 solo si seguía en 32.

**Relanzar.** La fase 6 (v2 o posterior) puede ejecutarse sobre un proyecto en nivel 6 o superior: no baja `Nivel` ni borra el mundo. Un mundo guardado por un motor anterior se migra solo: se borran las claves de la detección de longitud y de la biblioteca, el número de ciclo sigue donde iba y las conchas antiguas, que no guardan grosor, se leen con `Shellthick`. Para un proyecto en nivel 8 o superior: `fase6_ciclo.py`, después `fase8_conchas.py` y, por último, la última fase aplicada (por ejemplo `fase9_arqueologia.py` y `fase10_direccion.py`).

**Prueba pendiente con el aparato:** cambia de pattern dos veces y pulsa STOP mirando el Textport. Cada ráfaga sale como `AVISO All Notes Off sin STOP: cambio de pattern` o `AVISO All Notes Off junto a un STOP`. Si al cambiar de pattern no sale nada, el BeatStep no la envía y `Cambioentierra` no hará nada.

---

## FASE 7 · Erosión superficial

*fase 7 v9 (motor v21): erosión en notas y con la velocidad, perfiles del usuario; el golpe se ve como una nota. fase 7 v12 (motor v43): el bombo y el tom dejan de destruir; fase 7 v13 (motor v44): su pumping es un golpe seco; fase 7 v14 (motor v45): suman pulsos de ocupación; ver «El bombo y el tom: impulso de creación».*

Las 8 pistas de batería son las 8 señales de la batería. Cada pad tiene un **perfil de tres números** en la tabla `perfiles_erosion`, editable a mano, y desde la v12 un **modo** (erosión o impulso) y, desde la v14, sus **pulsos**:

- **`reduccion`:** cuántas **notas** de construcción deshace en la celda que golpea. Un golpe de 1 deshace lo que construyó una nota del SEQ. Hasta la v4 contaba escalones.
- **`radio`:** cuántos anillos de vecinas alcanza. 0 es solo la celda, 1 la celda y sus vecinas, 2 un anillo más.
- **`profundidad`:** cuántas conchas atraviesa el corte, desde la fase 9. 0 no corta.

**La misma moneda que la construcción** (v5). Cada nota del SEQ sube la formación un escalón / coste y suma 1 a la carga (fase 3). Cada nota de erosión hace exactamente lo contrario: baja la carga y la altura lo mismo. Al agotarse la carga baja un escalón, y la carga queda llena menos una.

- **Simetría:** lo que costó más notas cuesta más golpes deshacerlo, también cerca del límite (la frenada). N notas de construcción seguidas de N de erosión devuelven la celda a como estaba, mientras no haya satélites de por medio.
- **La carga ya no se vacía de golpe.** Antes, un pad que golpeaba más a menudo de lo que cuesta un escalón dejaba esa celda sin volver a construir nunca. Ahora, si el SEQ toca más notas de las que deshace la batería, la celda sigue creciendo.
- **Orden inverso,** sin cambios: primero los satélites, luego la altura de la celda y al final la **huella**, una mancha oscura que dura hasta que la celda se vuelve a sembrar o se entierra. Los satélites crecen por desbordes, no por notas: cada nota de erosión les quita un desborde.
- **Por encima del límite** la altura no baja: igual que al construir, las notas ahí no suben la formación, sino que desbordan. Lo que cae primero son los satélites.

**Atenuación con la distancia:** completa en la celda objetivo, la mitad en el primer anillo y un cuarto en el segundo (`ATENUACION` = 0,5 por anillo). Las fracciones de nota se acumulan en cada celda: con reducción 1 y radio 1, cada vecina pierde una nota cada dos golpes. Con el presupuesto de densidad el radio puede llegar a 4, y cada anillo sigue recibiendo la mitad que el anterior.

**Perfiles por defecto** (v6, elegidos por el usuario; v12, el bombo y el tom en impulso; v14, pulsos):

| Pad | Rol | Modo | Pulsos | Reducción (notas) | Radio | Profundidad | Tipo |
|---|---|---|---|---|---|---|---|
| 1 | Bombo | impulso | 3 | (4) | (2) | (2) | impulso |
| 2 | Caja | erosión | — | 15 | 1 | 3 | corte |
| 3 | Tom | impulso | 2 | (4) | (1) | (1) | impulso |
| 4 | Palmas, aro… | erosión | — | 3 | 1 | 0 | arañazo |
| 5 | — | erosión | — | 2 | 1 | 0 | arañazo |
| 6 | — | erosión | — | 2 | 0 | 0 | arañazo |
| 7 | Charles | erosión | — | 1 | 0 | 0 | arañazo |
| 8 | Platillo | erosión | — | 1 | 1 | 0 | arañazo |

- **Entre paréntesis,** la tripleta de la v6 del bombo y el tom. El impulso la ignora, pero se guarda: para que uno vuelva a erosionar como antes basta con poner `erosion` en su `modo`.
- **Corta la caja** desde la fase 9 (profundidad 3). Hasta la v11 cortaban también el bombo (2) y el tom (1). Las etiquetas de tipo son del usuario; el comportamiento lo deciden el modo y la tripleta.
- **Escala de referencia:** llegar al límite cuesta 11 notas. La caja (15) deja en semilla una formación en el límite.
- **El tipo es una etiqueta** que sale en la leyenda: lo que decide el comportamiento es el modo y, en erosión, la profundidad.
- **Columnas de la tabla:** `pad`, `reduccion`, `radio`, `profundidad`, `modo` (`erosion` / `impulso`), `pulsos` (pulsos de ocupación de un golpe, solo en impulso; v14, antes `capacidad`), `pump_rel` (segundos de caída del pumping, solo en impulso; v13), `tipo` y `rol`. El motor las lee por nombre; `rol` es solo una nota. Sin las columnas `modo`, `pulsos` (o `capacidad`) o `pump_rel`, el motor usa las de por defecto. El pad 7 es el charles y el 8 el platillo: la columna `rol` de `perfiles_erosion` y de `colores_drum` se corrige al relanzar aunque la tabla esté editada, sin tocar el resto.
- **Al relanzar la fase 7:** si la tabla tiene los valores de la v1, la v3, la v5, la v6–v11, la v12 o la v13 sin editar, se sustituye por la nueva. Si se editó a mano antes de la v14, se conserva: la columna `capacidad` pasa a llamarse `pulsos` con sus números y se le añaden las columnas que le falten (`modo`, `pulsos`, `pump_rel`) con los valores por defecto (bombo 3 pulsos y 0,20 s, tom 2 y 0,12 s, en impulso; el resto en erosión); el informe lo avisa con `..`. Si ya tiene las columnas de ahora y está editada, se conserva tal cual.

**El golpe se ve como una nota** (v9, motor v21). Sin balizas ni sectores: cada golpe ilumina, igual que una nota de un secuenciador, el centro de las celdas que erosiona (la loseta de `luz_celda`) y su formación, que se hincha un 12 % y se tiñe un 75 % del color de su pad. Desaparecen los 8 sectores del borde de la v6.

- **Intensidad:** plena en la celda del golpe, la mitad en el primer anillo y un cuarto en el segundo. Así la luz dibuja la huella del golpe.
- **Cuándo:** se apaga en `Vidabalizadrum` segundos (0,8).
- **Con secuenciador en la celda:** manda la luz más intensa en ese instante. El golpe gana mientras dura; luego vuelve el color del secuenciador (pleno si su nota sigue pulsada, tenue si no). Una nota pulsada y un golpe recién dado empatan, y gana el golpe.
- **Varios pads en la misma celda:** manda el más intenso, y a igualdad el último. Al alternar, cada golpe pinta la celda de su color.
- **Dónde se ve:** con formación, vacía o con huella, y también en modo actuación.
- **Lo que ya tiene significado queda a salvo:**
  - nota y golpe usan el mismo lenguaje (loseta del centro y formación teñida), así que se leen igual; solo cambia el color;
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

**Velocidad** (fase 7 v7). Con `Erosionvel` (encendido por defecto), la reducción escala con la velocidad del golpe:

```
notas = max(min(reduccion, 1), reduccion × velocidad / Velref)
```

- **Los números de la tabla** son los de un golpe a velocidad `Velref` (100). A 50 deshace la mitad y a 127, 1,27 veces más.
- **Mínimo:** un golpe siempre deshace al menos una nota en su celda (o la reducción, si es menor), así que uno flojo nunca queda en nada.
- **Fracciones:** se acumulan en cada celda como las de las vecinas, así que N golpes iguales deshacen siempre lo mismo.
- **Solo escala la reducción:** el radio y la profundidad no cambian con la velocidad, y el desplazamiento de celda (`vel % 3`) sigue como estaba.
- **Con `Erosionvel` apagado,** la reducción es la de la tabla, sin más.
- **Propuesta, sin implementar:** que la luz del golpe también crezca con la velocidad.

**Página Fase7, velocidad:** `Erosionvel` (encendido) · `Velref` 100

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

**Relación con la fase 6:** hasta la v11, mientras sonaba el bombo, cada temblor cambiaba la forma de muchas celdas y vaciaba el territorio, así que el mundo no se estancaba ni se enterraba por edad máxima (fase 6 v4); al quitarlo, el mundo se asentaba y se enterraba por estancamiento. Desde la v12 el bombo ya no destruye: ver los efectos colaterales del impulso, abajo.

### El bombo y el tom: impulso de creación

*fase 7 v12 (motor v43); v13 (motor v44), pumping en seco; v14 (motor v45), pulsos de ocupación.*

**Por qué.** El bombo y la caja/toms en los pads más destructivos impedían un mundo equilibrado entre creación y destrucción. El bombo y el tom dejan de destruir: **suman pulsos de ocupación** a la celda que golpean y, en el golpe, la celda **se hincha** un instante (pumping al beat). Los otros 6 pads no cambian.

**Lectura sinestésica.** El bombo es la respiración del planeta: cada golpe empuja la corteza desde dentro; el tom es un latido más corto. El mundo no se rompe al ritmo: se infla y se asienta. Sin cambios de material: el hinchado es una deformación elástica, no una mutación.

**Qué cambió en la v14.** En la v12 y la v13, el ×3 y el ×2 eran una **capacidad**: `cap` multiplicaba el límite de altura y los umbrales de satélites, fusión y corona, y las estructuras crecían de más. Además, el pumping se medía contra una altura que aún se estaba suavizando y no se aplicaba a lo que acababa de nacer, así que apenas se veía el golpe. Desde la v14 el ×3 y el ×2 son **pulsos de ocupación**, el límite y los umbrales no se tocan, y el pumping es un hinchado puramente visual sobre el tamaño ya asentado. Desaparecen `cap`, `Capmodo` y `Capdur`.

**Un pad en impulso** ignora reducción, radio y profundidad: no resta ocupación, no deja huella, no abre cortes ni cicatriz y no entra en el presupuesto de densidad (`Multradio` no le afecta). Cae donde caería la erosión: lo decide `Objetivo` y la velocidad lo desplaza un semitono. Con `alterna`, el bombo (1) y el tom (3) son impares y caen los dos donde está el SEQ1.

**1 · Pulsos.** Un golpe de bombo suma **3 pulsos** a la celda; uno de tom, **2** (columna `pulsos` de `perfiles_erosion`). Cada pulso es un **trigger completo** (ocupación + 1), como si la celda ya hubiera pagado su coste en notas:

- se aplican uno detrás de otro, con las reglas normales de la celda: crecimiento hasta el límite y, por encima, desborde a las vecinas (según `Vecina`), fusión, corona y cumbre cuando toque;
- no se paga coste en notas (`Costemax` no interviene) y la velocidad del golpe no cambia el número de pulsos;
- la estructura queda **al tamaño que le corresponde por esa ocupación**. Ejemplo: una celda con ocupación 2 recibe un bombo y queda en 5, con la altura y el estado de una celda de ocupación 5;
- **celda vacía:** el primer pulso la siembra (ocupación 1, pulida o porosa según la velocidad del golpe y `Umbralvel`) y los demás suman: queda en ocupación = `pulsos`. La especie es la del secuenciador al que sigue el golpe (con `alterna`, el bombo y el tom siguen al SEQ1). Sobre una celda ocupada, los pulsos no cambian su especie ni la colonizan;
- la altura nueva se aplica **de golpe**, en el mismo fotograma, sin el suavizado de la altura ni el stop-motion de la piel (fase 11). Una celda sembrada por un golpe tampoco hace el rebote de nacimiento ni el latido de una nota: el golpe lo hace el pumping;
- los satélites que nazcan por desborde en las vecinas son de esas celdas: crecen normal y no hacen pumping;
- desde la fase 11, el golpe adelanta la obra de la celda una etapa, como una nota (`Avance` gates).

**2 · Pumping, solo visual.** Se aplica a todo lo dibujado en la celda golpeada tras el golpe (formación, satélite si la celda lo es, losa de fusión, corona, piezas de la piel), **sobre su tamaño ya asentado** (el de la ocupación nueva), anclado en la base y sobre la normal:

- **pico vertical** = 1 + (`pulsos` − 1) × `Pumpamt` × la velocidad. Con `Pumpamt` 1: bombo ×3, tom ×2;
- **tope visual:** la altura con pumping no pasa de `Pumptope` × el límite de altura (2), para que una estructura alta no se dispare. Si ya lo pasa, no se hincha;
- **escala horizontal** = 1 + (pico vertical − 1) × `Pumphorz` (0,30), recortada para que ninguna pieza invada la celda vecina (la regla de los anillos polares). Si alguna pieza ya llega al borde (un puente del cluster, una planta que ocupa la celda), la celda no se ensancha;
- **ataque instantáneo:** el pico se ve en el mismo fotograma del golpe;
- **pico sostenido:** `Pumphold` (0,04 s), y como mínimo **2 fotogramas dibujados** (los cuenta el motor);
- **caída** en los segundos de su pad (columna `pump_rel`: el bombo 0,20 s, el tom 0,12 s), deprisa al principio y plana al final, y llega a 1 justo al acabar:
  ```
  escala(t) = 1 + (pico − 1) · (1 − t / pump_rel)^3
  ```
- **tope por el ritmo** (como en la v13): el golpe entero (pico sostenido y caída) cabe en 0,8 × el tiempo desde el golpe anterior de impulso en esa celda, así que vuelve a 1 antes del siguiente. En una ráfaga de semicorcheas es 0,8 × el paso; con el bombo a negras, no recorta. Ver «Decisiones»;
- **retrigger en seco:** un golpe durante la caída salta otra vez al pico, sin partir de la escala actual. Dos golpes en el mismo fotograma (bombo y tom a la vez) dan el pico mayor;
- **velocidad:** escala el pico entre `Pumpvelmin` (0,6, a velocidad 1) y 1 (a 127); nunca por debajo;
- se evalúa **en cada fotograma del render**, después de la altura, sin filtro ni interpolación. La altura real no cambia con él;
- con `Pumpon` apagado no hay pumping; los pulsos suman igual.

Con el bombo a negras a 120 BPM y 30 fps: dos fotogramas en ×3 y luego 2,16, 1,59, 1,25, 1,07, 1,01 y 1.

**3 · Luz.** `luz_celda` de la celda golpeada, con el color del pad, sube a su intensidad máxima en el mismo fotograma del pico y **cae con la misma curva**. Así el golpe se lee aunque la estructura sea pequeña. Como desde la v12, no tapa al secuenciador: si su nota acaba de sonar en la celda, el centro se parte en los dos colores y la formación conserva el tinte del secuenciador. El destello de `luz_destello` (fase 9) es suave (0,35) y sigue la misma curva.

**Parámetros (página Fase7):**

| Parámetro | Etiqueta en el panel | Por defecto | Qué hace | Qué condiciona |
|---|---|---|---|---|
| `Pumpon` | Pumping de bombo y toms | encendido | Enciende el hinchado visual al golpe de los pads en modo impulso | formas_pulidas / formas_porosas, coronas, luz_celda |
| `Pumpamt` | Fuerza del pumping | 1,0 | Pico vertical = 1 + (pulsos − 1) × Pumpamt. Con 1: bombo ×3, tom ×2 | formas_pulidas / formas_porosas, coronas |
| `Pumphorz` | Anchura del pumping | 0,30 | Cuánto del pico vertical se traslada a la anchura; recortada al ancho de la celda | formas_pulidas / formas_porosas, coronas |
| `Pumphold` | Pico sostenido (s) | 0,04 | Segundos que se mantiene el pico antes de caer (mínimo 2 fotogramas) | formas_pulidas / formas_porosas, coronas, luz_celda |
| `Pumpvelmin` | Velocidad minima del pico | 0,6 | Fracción mínima del pico con un golpe flojo | formas_pulidas / formas_porosas, coronas |
| `Pumptope` | Altura maxima con pumping (x limite) | 2,0 | Tope de la altura con pumping, en múltiplos del límite de altura | formas_pulidas / formas_porosas, coronas |

Las etiquetas van sin tildes, como las demás del panel. Columnas de `perfiles_erosion`: `modo`, `pulsos` (bombo 3, tom 2) y `pump_rel` (bombo 0,20 s, tom 0,12 s; los demás pads, 0,15 si pasan a impulso). Al relanzar la fase 7 v14 se quitan `Capmodo` y `Capdur` (y `Pumpataque` y `Pumprelease`, si quedaban de la v12), y la columna `capacidad` de la v12 y la v13 pasa a llamarse `pulsos` con sus números.

**Leyenda:** la línea `IMPULSO` sustituye a la de `EROSION` cuando el golpe es de impulso; `MUNDO` ya no cuenta celdas con capacidad:

```
IMPULSO  pad 1 +3 celda 40 ocupacion 2->5
```

Si el golpe desborda, añade `desbordes N`. En el `midi_log`: `IMPULSO pad 1 +3 celda 40 ocupacion 2->5`.

**Con las otras fases:**

- **fase 9 y 16:** solo corta la caja; el destello del impulso es suave.
- **fase 14:** el bombo y el tom no son arañazos (no hay accidente ni escalada); los arañazos siguen siendo los pads 4 a 8.
- **fases 11 a 17:** los pulsos llegan a la piel como cualquier otro trigger: la celda pasa por los estados de siempre, con los umbrales de siempre.
- **fase 3:** el pumping va en el dibujo del motor, no en la animación de alturas de `fase3_semilla.py`, que no cambia (sigue en v12).

**Efectos colaterales a vigilar** (sin compensar todavía):

- Sobre una celda en el límite, un bombo son **3 desbordes seguidos**: pueden nacer tres satélites de golpe. Con `Vecina` en `velocidadocupacion` se reparten; si salen apelotonados, se ajusta después.
- Más ocupación por golpe: las celdas maduran antes y heredan más, y los mundos se acortan. En la sesión de 20 minutos (`MONTAJE_FASES_11_18.md`, fase 18) pasan de 8 a 15 eras en la naturaleza y de 11 a 17 en la ciudad, todas por estancamiento (de 23 a 62 compases cada una), con los cuatro criterios de cierre cumplidos.

**Autoprueba (v14),** las 12 del encargo:

1. bombo sobre una celda con ocupación 2 → 5; tom → 4;
2. bombo sobre una celda vacía → ocupación 3, sembrada por el primer pulso (especie del SEQ1, pulida por la velocidad);
3. el golpe no cambia el límite de altura ni los umbrales: la celda queda con la altura y el estado de su ocupación;
4. sobre una celda en el límite, cada pulso desborda a una vecina (3 desbordes); de la ocupación 6 a la 9, coronación;
5. la altura nueva se ve en el mismo fotograma del golpe, también con el stop-motion de la piel;
6. el pico (×3 el bombo) en el primer fotograma, y al menos 2 (a 30, 60 y 120 fps);
7. la caída sigue la cúbica, llega a 1 justo en `pump_rel` (0,20 s) y nunca baja de 1;
8. un golpe durante la caída salta otra vez al pico en el fotograma siguiente;
9. en una ráfaga de semicorcheas a 200 BPM, desde el segundo golpe la caída se recorta a 0,8 × el paso menos el pico y la celda vuelve a 1 antes del siguiente;
10. la altura con pumping no pasa de `Pumptope` × el límite y ninguna pieza pasa del ancho de su celda con `Pumphorz` 0,30 (naturaleza y ciudad); una formación baja crece ×3 con el bombo y ×2 con el tom;
11. los satélites que nacen en las vecinas no hacen pumping;
12. el entierro no deja pumping pendiente.

Además: no resta, no deja huella ni corte (con conchas, a nivel 9) y no entra en el presupuesto de densidad; el pico a velocidad 1 es 1 + (pico − 1) × 0,6; la altura real no cambia con el pumping; acabado, lo dibujado es lo de la ocupación nueva, sin hinchar; `Pumpon` apagado lo quita y los pulsos suman igual; la luz de la celda está plena en el pico y cae con la misma curva, y no tapa al SEQ1. También: el pad 1 por MIDI suma 3 pulsos y el 2 erosiona; la tabla se lee con `modo`, `pulsos` y `pump_rel`; las tablas de la v1 a la v13 sin editar se sustituyen; las editadas a mano se completan (y `capacidad` pasa a `pulsos`), y una editada con las columnas de ahora se conserva; solo corta la caja; la leyenda dice `IMPULSO` tras el pad 1 y `EROSION` tras el 4.

**Probar sin BeatStep:** `Padprueba` 1 + `Erosionar` sobre una formación del SEQ1 (`Objetivo` seq1): la ocupación sube 3, la formación salta a su nuevo tamaño, se hincha ×3 y vuelve en una quinta parte de segundo, y la leyenda dice `IMPULSO pad 1 +3 celda ... ocupacion a->b`. Sobre una celda vacía, la siembra con ocupación 3.

---

## FASE 8 · Conchas

En cada fin de ciclo:

1. **La capa se entierra depositada sobre la columna de cada celda**, no a una cota común (fase 8 v5, motor v23). Cada celda apila una loseta con el color de su generación sobre lo que le queda debajo: una hondonada que dejó un corte se tapiza y sigue siendo hondonada. Las celdas que estaban ocupadas quedan más claras: los continentes se leen en el color. Sus formaciones se descartan.

   ```
   grosor de la loseta = grosor de la concha + Colmatacion × laguna(c)
   r_in = suelo(c)        r_out = suelo(c) + grosor de la loseta
   ```

   `Colmatacion` (0 por defecto) dice cuánto rellena la capa nueva las hondonadas: con 0 la capa se apoya en el relieve con su grosor; con 1 rellena hasta la cota nominal (el comportamiento anterior, solo para comparar); en medio, las cuencas se colmatan poco a poco.
2. **El planeta engorda el grosor de la concha.** Con `Grosortiempo` (encendido por defecto), el grosor es proporcional a lo que duró su mundo:

   ```
   grosor = min(Grosormax, Shellthick × clamp(compases / Ciclomin, 0,25, Ciclomax / Ciclomin))
   ```

   Con los valores por defecto (fase 6 v5, fase 8 v10) va de 0,5 (ciclo mínimo, 16 compases) a 1,5 (48 compases o más: `Grosormax`). Sin ese tope, una concha de edad máxima (64 compases) mediría 2,0. `Grosormax` 0 quita el tope, y un `Forzarciclo` temprano da como mínimo 0,125. Sin `Grosortiempo`, siempre `Shellthick`. El grosor de cada estrato registra cuánto tardó su mundo en agotarse.
   **Compactación** (fase 8 v10, motor v37). La concha nueva aplasta las de debajo: todas pierden la misma fracción de su grosor,

   ```
   pérdida = min(corteza × (1 − e^(−grosor nuevo / Cortezamax)), 0,9 × grosor nuevo)
   corteza = radio nominal − núcleo
   ```

   así que la corteza tiende a `Cortezamax` (4) y el planeta deja de engordar. Las conchas recientes se leen gruesas y las viejas se aprietan en vetas finas, como en un corte geológico. El radio sube siempre al menos un 10 % de la concha nueva y nunca baja. Las losetas de cada columna se aplastan igual, así que cortes, hondonadas y lagunas conservan su forma (la laguna se compacta con sus conchas). `Cortezamax` 0: sin compactar (el radio es el tiempo, como hasta la fase 8 v9).
3. **Herencia:** el 25 % de la ocupación de cada celda pasa a la capa nueva. La fracción que no llega a 1 se acumula para el ciclo siguiente: una celda con ocupación 2 en ciclos seguidos acaba heredando. Lo heredado vuelve a brotar desde la nueva superficie.

**Columnas y radio nominal** (motor v23). Cada celda guarda su **columna**: la pila de losetas que le quedan, de abajo arriba. Cada loseta lleva su concha (generación: color y ocupación) y su grosor; sus radios salen de su posición en la columna, y el radio exterior de una es el interior de la siguiente, sin huecos ni solapes.

```
suelo(c)      = núcleo + suma de los grosores de la columna de c
radio_nominal = núcleo + suma de los grosores de todas las conchas
laguna(c)     = radio_nominal - suelo(c)          (siempre >= 0)
```

- **El radio nominal** es lo que antes se llamaba radio del planeta: sigue siendo el tiempo transcurrido. Solo crece el grosor de la concha; la colmatación no cuenta como tiempo.
- **La laguna** es el tiempo que la destrucción ha borrado en esa celda.
- **Las conchas siguen existiendo como generaciones** (paleta, grosor nominal, tabla `ciclos`, continentes, herencia), pero ya no tienen una cota única.
- **Quién usa qué cota:** las formaciones y lo heredado, el límite de altura, la luz de celda, el destello y la retícula van sobre `suelo(c)`; la cámara (fases 8 y 10), la luz principal y `radio` en la leyenda, sobre el radio nominal.
- **Mundos guardados:** al cargar un mundo de un motor anterior, las columnas se construyen con las losetas que sobreviven de cada concha, apiladas por orden de generación y sin huecos. Las celdas que estaban cortadas aparecen como hondonadas. Las conchas de un motor v7-v10 se leen con `Shellthick`.

**Paleta de generaciones** (fase 8 v8, motor v26): **cada concha de un color**, y dos seguidas siempre contrastan. El color se calcula en OKLCH (luminosidad perceptual uniforme) y se convierte a sRGB:

```
n         = generación de la concha (0 = la primera)
t         = frac(n × 0,6180339887)                    (ángulo áureo)
tono      = Paletatono + t × 200°, saltando las bandas reservadas (245° hasta el motor v45)
L_vacía   = Paletaluz − Paletaalterna/2 si n es par, Paletaluz + Paletaalterna/2 si es impar
L_ocupada = L_vacía + Contrasteocupada
croma     = Paletacroma
```

**Conchas discretas** (fase 8 v12, motor v53). Desde la cámara de globo, la loseta de arriba de cada columna es el suelo sobre el que crecen las formaciones. Hasta la v11 ese suelo era de tono medio-claro (L 0,50 / 0,64), las celdas ocupadas lo moteaban de manchas claras (+0,12) y competía con lo construido. Ahora:

| Parámetro | Defecto | Antes | Qué hace |
|---|---|---|---|
| `Paletaluz` | 0,35 | 0,57 | Luminosidad media de las conchas |
| `Paletaalterna` | 0,06 | 0,14 | Diferencia de luminosidad entre conchas seguidas |
| `Contrasteocupada` | 0,04 | 0,12 | Cuánto más clara es una loseta ocupada (0 = igual) |
| `Paletacroma` | 0,04 | 0,09 | Saturación |
| `Tapaneutra` | 0,6 | (0) | Mezcla de la cara de arriba hacia un gris neutro (0 = como los flancos, 1 = gris) |
| `Tapaluz` | 0,28 | — | Luminosidad de ese gris |

- **Contraste entre conchas seguidas:** al menos 60° de tono **y** `Paletaalterna` de luminosidad. Con los valores nuevos las bandas de un corte se distinguen sobre todo por el tono.
- **Tapa neutra:** la loseta de arriba de cada columna lleva una **tapa**, una instancia fina (0,02 o un 25 % de la loseta) un poco más ancha que ella y que asoma un 0,4 % por arriba, del color de la concha mezclado `Tapaneutra` hacia el gris `Tapaluz`. Los flancos conservan el color de su concha: el color de cada estrato se ve donde la erosión lo deja a la vista, en las paredes de un corte. Cuesta **una instancia más por celda** (N, no el doble: con 24 conchas visibles, un 4 %). Solo las losetas de arriba enseñan su cara superior, así que no hace falta más. Con `Paleta` mineral no hay tapa.
- **Mate:** la tapa lleva rugosidad 1 en el shader de la piel (fase 15) y `mat_estratos` pasa a especular 0: el suelo no hace brillos que compitan con `mat_pulido`. Los flancos de la fase 15 conservan su materia (el carbón brilla en los cortes).
- **Secuenciador y cicatriz:** el tinte del secuenciador es una capa aditiva aparte y sigue cubriendo la tapa (se lee mejor sobre un suelo oscuro). La cicatriz manda: una loseta recién expuesta sale cian entera, tapa incluida.
- **Jerarquía (informe):** la fase 8 comprueba que la tapa más clara posible, `(1 − Tapaneutra) × (Paletaluz + Paletaalterna/2 + Contrasteocupada) + Tapaneutra × Tapaluz`, queda al menos 0,15 por debajo de la luminosidad de las formaciones (media OKLab de las dos especies, `COL_GEO` y `COL_ARQ`: 0,58). Si no, avisa con `..`. Con los valores nuevos, 0,34; con los de antes, 0,76.
- **Valores antiguos:** `Paletaluz` 0,57 · `Paletaalterna` 0,14 · `Contrasteocupada` 0,12 · `Paletacroma` 0,09 · `Tapaneutra` 0 reproducen la paleta de la v11 tal cual (la autoprueba lo comprueba).
- **Proyecto en marcha:** al relanzar la fase 8, `Paletacroma` pasa de 0,09 a 0,04 solo si seguía en 0,09, y la tabla `escenas` de la fase 18 pasa de 0,09 / 0,06 a 0,04 / 0,03 si no se había tocado. Los mundos guardados se recolorean solos: el color se calcula, no se guarda.

- **Bandas reservadas** (tono OKLCH): 165°–235°, el cian de la cicatriz, y 55°–100°, el ámbar del SEQ2. Desde el motor v46 (fase 11 v5 y fase 13 v2) también 120°–165°, los verdes de los pisos de la naturaleza, y 235°–275°, el azul de los ríos: una sola banda de 120° a 275°. La secuencia se reparte sobre los 200° que quedan, recorriendo el círculo y saltando las bandas; no se recorta al borde. Ninguna concha camufla un bosque ni un río. La banda verde empieza en 120° y no antes: con menos tono libre, dos conchas seguidas dejarían de diferir 60°.
- **Croma contenido** (0,04; 0,09 hasta la v11): las conchas son mineral; las luces (secuenciadores, batería, cicatriz) son saturadas y emisivas, y siguen destacando encima.
- **Sin blancos:** la luminosidad máxima (0,42; 0,76 hasta la v11) queda lejos del blanco del SEQ1. Todos los colores caen dentro de sRGB sin recortar.
- **Se conserva** la alternancia claro / oscuro entre conchas seguidas y la loseta de una celda ocupada más clara que la vacía (los continentes se leen así). El zócalo (gris casi negro) y el núcleo quedan oscuros y neutros, fuera de la paleta.
- **Calculado, no guardado:** el color sale de la generación y de los parámetros. Al cargar un mundo y al cambiar la paleta, todo lo enterrado se vuelve a colorear (el color que guardaban las conchas antiguas ya no manda).
- **`Paleta` = mineral** vuelve a la paleta anterior, tal cual, para comparar: ámbar en la base y después grises minerales y negros alternos; con ella el zócalo vuelve a ser ámbar apagado.

Con los valores de la v12 (`Paletatono` 20, L 0,32 / 0,38, croma 0,04, ocupada +0,04; flancos y, con `Tapaneutra` 0, también tapas):

| n | Tono | Vacía | Ocupada |
|---|---|---|---|
| 0 | 20° | `#452B2A` | `#503534` |
| 1 | 319° | `#4C3C50` | `#57465B` |
| 2 | 103° | `#37341B` | `#413E25` |
| 3 | 357° | `#543A43` | `#5F444D` |
| 4 | 296° | `#342F45` | `#3F3950` |
| 5 | 34° | `#563B34` | `#61453F` |
| 6 | 333° | `#3F2B3C` | `#4A3546` |
| 7 | 117° | `#41452D` | `#4B5037` |

Con los valores de antes (v11):

| n | Tono | Vacía | Ocupada |
|---|---|---|---|
| 0 | 20° | `#904D4E` | `#B67070` |
| 1 | 319° | `#A47AAF` | `#CA9FD6` |
| 2 | 103° | `#6D651F` | `#908844` |
| 3 | 357° | `#B8758D` | `#E099B2` |
| 4 | 296° | `#685891` | `#8A7BB7` |
| 5 | 34° | `#BC7867` | `#E49D8B` |
| 6 | 333° | `#824F79` | `#A7719D` |
| 7 | 117° | `#889352` | `#ADB976` |

Con `Paletatono` 20 y `Paletacroma` 0,09 (motor v46; hasta la v45 las conchas 2, 4 y 7 caían en verde y azul). Cambiar `Paletatono` entre sesiones da otra secuencia con las mismas propiedades.

**Colores de la batería frente a las conchas.** Los pads 1 a 6 son saturados (croma 0,17–0,25, frente a 0,09 de las conchas). Los pads 7 (`#F9A8D4`, rosa) y 8 (`#C4B5FD`, lila) son apagados (croma 0,10–0,11) y quedan cerca de las conchas rosas y lilas claras ocupadas: se distinguen sobre todo porque la luz de celda no se sombrea. Si se confunden, súbeles el croma en `colores_drum`.

**Decisión: el horneado.** El marco pide hornear cada concha a una textura proyectada sobre una esfera. Aquí cada concha es una capa de losetas instanciadas, todas del mismo tamaño porque las celdas son de área igual:

- igual de barata: una sola geometría;
- sin shaders;
- en la fase 9 permite abrir cortes quitando losetas y ver las paredes de cada capa con su color, que es justo lo que pide la estratigrafía.

**Dibujo.** Cada loseta es una instancia a su radio, con el alto de su grosor y el ancho de su celda a ese radio; con `Tapaneutra`, la de arriba de cada columna lleva además su tapa. `Maxconchas` (24) cuenta por columna: se dibujan las 24 losetas superiores de cada celda y, debajo, un **zócalo** (una sola instancia, gris casi negro; ámbar apagado con `Paleta` mineral) desde el núcleo hasta la loseta dibujada más baja. La esfera del núcleo ya no crece: se queda en el radio base, porque una esfera a cota común taparía las hondonadas. Como mucho, celdas × (`Maxconchas` + 2) instancias (con la tapa).

**Continentes** (en la leyenda): regiones de celdas vecinas ocupadas en al menos la mitad de las 8 últimas conchas.

**Cámara:** la de globo (la misma de la fase 10, sin modos): el planeta entero, centrado y tan cerca como permite el cuadro; retrocede a cada enterramiento. Desde comun v15 la pone `estratos_comun.py` en todas las fases que cargan el motor (de la 3 en adelante).

**Página Fase8:** `Paleta` generaciones (*Paleta de las conchas*: generaciones o mineral) · `Paletatono` 20 (*Tono de la primera concha*, 0–360) · `Paletacroma` 0,04 (*Saturación de las conchas*, 0–0,15) · `Paletaluz` 0,35 (*Luminosidad media de las conchas*) · `Paletaalterna` 0,06 (*Diferencia de luminosidad entre conchas seguidas*) · `Contrasteocupada` 0,04 (*Loseta ocupada: cuánto más clara*) · `Tapaneutra` 0,6 (*Tapa de las losetas hacia el gris*) · `Tapaluz` 0,28 (*Luminosidad del gris de la tapa*) · `Herencia` 0,25 · `Maxconchas` 24 (*Losetas visibles por columna*) · `Grosortiempo` (encendido) · `Grosormax` 1,5 · `Cortezamax` 4 (*Corteza máxima: compacta las conchas viejas*, 0–12; 0 = el radio es el tiempo) · `Colmatacion` 0 (*Relleno de las hondonadas al enterrar*, 0–1). Para probar sin esperar a que el mundo se estanque: `Forzarciclo` (página Fase6).

**Leyenda:**

```
CONCHAS  11   radio 10.12   ultima 0.75   corteza 4.12 de 4 (x0.86)   laguna max 1.25 (celda 41)   colmatacion 0%   herencia 25%   continentes 3
```

`radio` es el radio nominal; `corteza`, lo que hay sobre el núcleo, de `Cortezamax`, y el factor de la última compactación; `laguna max`, la celda más honda.

**Ritmo de engorde:** cada concha deposita `Shellthick` por cada `Ciclomin` compases, y la compactación se come casi todo cuando la corteza se acerca a `Cortezamax`. En una sesión simulada de 20 minutos a 120 BPM (SEQ1, SEQ2 y batería), el radio pasa de 6 a ~7,3 (2 min), ~8,4 (5 min), ~9,7 (10 min) y ~10,8 (20 min). Sin compactar (`Cortezamax` 0) y con los valores de antes (`Ciclomin` 8, `Grosormax` 2) llegaba a 42: las formaciones, de 1,875, eran motas. Para un planeta más pequeño, baja `Cortezamax`.

**Relanzar** (fase 8 v5 y fase 9 v6). En un proyecto en la fase 10: `fase8_conchas.py`, `fase9_arqueologia.py` y `fase10_direccion.py`. No baja `Nivel` ni borra el mundo: las columnas se construyen solas a partir de las conchas y las celdas cortadas quedan como hondonadas.

---

## FASE 9 · Arqueología

**Cortes.** Los pads de erosión con profundidad mayor que 0 (por defecto el 2, la caja, con profundidad 3; hasta la fase 7 v11 cortaban también el bombo y el tom, que ahora son impulso) abren un corte en forma de **anfiteatro**. Desde la fase 9 v6 (motor v23) la profundidad se mide en la **columna** de cada celda: un corte de profundidad N quita sus N losetas superiores en la celda golpeada, N − 1 en el primer anillo, N − 2 en el segundo, hasta el radio del pad. En terreno llano da lo mismo que antes; sobre relieve, el corte sigue la forma del suelo. Las paredes son las caras de las losetas vecinas que quedan por encima del suelo nuevo, cada una con su color. El hueco es permanente. La concha siguiente lo tapiza sin rellenarlo: la hondonada se conserva, salvo lo que rellene `Colmatacion` (fase 8).

- **Tope por mundo.** Dentro de un mundo, los golpes repetidos no taladran: cada celda cuenta las losetas que ha perdido en el mundo actual, y un golpe que le pide k quita k menos esas, si sale positivo. La cuenta vuelve a 0 al enterrar.
- **Entre mundos sí se acumula.** Con `Colmatacion` 0, una celda cortada con profundidad N en cada mundo pierde N losetas y recibe 1 por mundo: baja N − 1 por mundo. Es una cuenca de erosión.
- **El núcleo es el fondo.** Una columna vacía tiene el suelo en el radio del núcleo; ningún corte baja de ahí y las losetas que falten se ignoran. La primera vez que una celda se queda sin losetas, la leyenda lo dice: `CORTE celda 41 nucleo alcanzado`.
- **Las formaciones de una celda cortada** se apoyan en el fondo del corte, con el límite de altura medido desde ese suelo.
- **Grosores distintos:** como cada loseta tiene el grosor de su ciclo, un corte de 3 es más o menos hondo según lo que duraron esos mundos.
- **Cicatriz:** el fondo (la loseta superior que queda en la columna cortada) y las paredes recién expuestas (las losetas vecinas con el radio exterior por encima del suelo nuevo y el interior por debajo del anterior) se ven en **cian** y se funden con el color de la concha de cada loseta en `Cicatriz` segundos. Un golpe que no quita nada no expone nada, y enterrar (depositar) no enciende cicatrices.
- **Destello:** `luz_destello`, una luz puntual que sigue el giro del planeta, golpea la celda en cada destrucción: fuerte en los cortes, suave en los arañazos.
- **Luz del SEQ1:** el centro de su celda pasa a blanco, porque el cian queda reservado para lo recién expuesto. El destello toma el color del pad que golpea, aclarado.

**Página Fase9:** `Cicatriz` 4 s · `Destello` 3

**Leyenda:**

```
CORTE    celda 41   3 losetas   suelo 9.25   laguna 2.25   cicatriz 2.1 s
CORTE    celda 41   nucleo alcanzado
```

---

## FASE 10 · Dirección visual

- **Cámara de globo** (por defecto, `Modocamara` = globo; fase 10 v5, motor v24). Mira al centro del planeta (`objetivo` en el origen) y lo encuadra entero, tan cerca como permite el cuadro.
  - **Encuadre** (motor v36, fase 10 v10). Un solo parámetro: `Encuadre`, **el alto del planeta en la pantalla** (del lado más estrecho del cuadro; con 1280 × 720, el alto). Con 0,85, el valor por defecto, el planeta entero ocupa el 85 % del alto y queda sitio arriba y abajo para lo que crece sobre él; con 1 va de borde a borde. El planeta es el radio nominal (núcleo + conchas) más lo que asoma la retícula (0,2).
    - **Solo cambia cuando el planeta engorda** (una concha nueva). Entonces la cámara se aleja en `Camsuave` segundos hasta el mismo `Encuadre`, y el planeta nunca se sale del cuadro. Crecer, erosionar, los cortes o el latido no la mueven.
    - Lo más alto de una construcción puede salirse del cuadro. La leyenda `CAMARA` dice qué parte del alto ocupa el planeta y hasta dónde llega lo más alto (`lo mas alto llega al 97%`; más de 100 %, se sale). Si se sale, baja `Encuadre`.
    - Sustituye a `Encuadremargen` («holgura alrededor del globo») y `Holguraaltura` («holgura para las construcciones»), que confundían. Al relanzar cualquier fase se quitan y aparece `Encuadre`.

    *Historia: hasta la v31, el radio encuadrado era el planeta más toda la altura máxima posible (se veía lejos). La v32 encuadraba lo que se dibujaba en cada fotograma (la cámara no paraba quieta). La v33 a la v35 usaban `Encuadremargen` y `Holguraaltura`.*
  - **Radio que se encuadra (hasta motor v31):** `radio_encuadre = radio nominal + altura máxima`. La altura máxima es lo más alto que llega algo que gira con el planeta: una formación en el límite hinchada por el latido (límite × 1,12) más la corona más larga (la de una torre en el último tramo de cumbre: 0,9 × (1 + 0,25 × `Tramoscumbre`) × límite). Con los valores por defecto, 1,875 × 2,92 = 5,475. Sale del código, no de medir la geometría: el encuadre solo cambia cuando el planeta engorda. El crecimiento, la erosión, los cortes y la colmatación no lo mueven, y ningún suelo pasa del radio nominal.
  - **Distancia:** una esfera de radio R cabe entera si la cámara está a R / sin(θ/2) de su centro, con θ el ángulo de visión del lado más estrecho del cuadro:

    ```
    aspecto = ancho / alto del render (su resolución real)
    tan(fov_v / 2) = tan(fov_h / 2) / aspecto        (TouchDesigner fija el horizontal por defecto)
    θ     = min(fov_h, fov_v)
    α     = atan(Encuadre × tan(θ / 2))                 (el planeta ocupa Encuadre del lado estrecho)
    d_obj = radio del planeta / sin(α)
    d_min = radio del planeta / sin(θ / 2)              (de borde a borde: nunca más cerca)
    ```

    El FOV se lee de la cámara (`fov` y `viewanglemethod`: horizontal, vertical o focal y apertura) y no cambia: el zoom es un travelling. Con 1280 × 720 y 45° horizontales manda el lado vertical (26,3°).
  - **Transición:** la distancia persigue a `d_obj` con un amortiguado crítico que llega en `Camsuave` segundos (3): arranca y frena suave, sin rebote, en segundos y ajena al secuenciador. **Seguridad:** en cada fotograma, la distancia nunca baja de `d_min`; si una concha nueva hace crecer el planeta más de lo que cubre el sitio libre (`Encuadre` por debajo de 1), la parte que no cabe se corrige al instante y el resto llega suave. Con `Encuadre` 0,85 no pasa con conchas normales: en la prueba, el planeta llega como mucho al 88 % del alto durante la transición.
  - **Saltos sin transición:** `Resetmundo`, el cambio de rango y la carga de un mundo guardado (o del motor) llevan la cámara al encuadre nuevo al instante.
  - **Dirección:** fija en +Z, la dirección de referencia hacia la que se balancea el eje. El giro y el balanceo del planeta ya enseñan todas sus caras y los dos polos; `Camvel` no actúa.
  - **Planos de recorte:** `near` y `far` los da el motor con la distancia: `far` = distancia + 2 × radio de encuadre + 10; `near` = un cuarto de lo que hay entre la cámara y el radio de encuadre (entre 0,05 y 5).
- **Cámara de superficie** (`Modocamara` = superficie). La de la fase 10 v4, sin cambios: órbita lenta (`Camvel`, 0,6 °/s: unos 10 minutos por vuelta), ajena al reloj del secuenciador, a `Camaltura` de la superficie. Mira a un punto del horizonte por delante: la curvatura se insinúa y el globo no se ve.
- **Cambio de modo.** Cambiar `Modocamara` en directo hace una transición de 20 s, con curva suave, en los dos sentidos (la dirección se interpola por la esfera, así que la cámara nunca atraviesa el planeta). Desde la fase 10 v11 no hay `Planofinal`: era el cierre que alejaba la cámara de superficie hasta ver el globo, y ahora el globo es la cámara por defecto. Relanzar la fase 10 lo borra de la página.
- **Luz.** Cenital fría que sube con el planeta, y un relleno azulado muy tenue. Desde la fase 10 v5 el relleno se aleja con el planeta (antes quedaba dentro al pasar de unos 17 de radio) y alumbra desde abajo y por delante, la cara que ve la cámara de globo. El destello no cambia. El eje sigue inclinado `Tilt` (20°).
- **Núcleo:** negro profundo.
- **Solo la leyenda.** `Leyenda` (página Fase1, activado) la muestra u oculta sin tocar nada más; la letra es de 9 puntos (15 hasta comun v12). Al relanzar cualquier fase, la letra pasa de 15 a 9 solo si seguía en 15, y aparece `Leyenda`.
- **Modo actuación.** `Modoactuacion` oculta la retícula y la leyenda (la luz de celda se sigue viendo: es parte del mundo): el switch `modo` pasa la salida al render limpio. Al quitarlo vuelve el modo diagnóstico.

**Página Fase10:** `Modocamara` globo · `Encuadre` 0,85 (0,3–1; el alto del planeta en la pantalla) · `Camsuave` 3 s · `Modoactuacion` · `Camaltura` 4 · `Camvel` 0,6. `Camaltura` y `Camvel` solo actúan en modo superficie.

**Leyenda** (diagnóstico, desde la fase 8):

```
CAMARA   globo   dist 32.6 -> 32.6   el planeta ocupa el 85% del alto (Encuadre 0.85)   lo mas alto llega al 97%   fov 45 (horizontal)
```

**Relanzar** (fase 10 v5) en un proyecto en la fase 10: `fase10_direccion.py`. Si quieres la cámara de globo también en la fase 8 de un proyecto que no ha llegado a la 10, relanza la última fase aplicada.

---

### Cómo comprobar el sistema completo

1. **PLAY con el SEQ1.** Las celdas que toca se siembran; las que repite crecen hasta el límite y después ramifican.
2. **Añade el SEQ2.** Aparecen torres; donde los dos se cruzan, híbridos.
3. **Deja tocar el SEQ1 sin batería.** La madurez sube, la novedad baja, el planeta frena el giro y el ciclo se cierra por `estancado`.
4. **Con batería constante,** los ciclos llegan a `edad maxima`. Al parar la batería, el mundo se asienta y se entierra.
5. **Añade la batería.** Los arañazos rebajan el paisaje y la densidad se mantiene por debajo del 60 %.
6. **Fin de ciclo.** El mundo se entierra, el planeta engorda y lo heredado vuelve a brotar.
7. **Pads 2 y 3 con varias conchas.** Se abre un corte con las capas a la vista, primero en cian.
8. **`Modoactuacion`.**

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
| Todas las formaciones, coronas, estratos o marcas de la retícula del mismo color | Geometría creada antes de comun v10, o retícula de `fase12_base.py` v2: el color por instancia se enlazaba a `instancecolorr/g/b`, que no existe | Relanza cualquier fase (comun v12): repara el color de todas las geometrías instanciadas sin tocar el mundo, y el informe dice cuáles. Si persiste: Instance 2 → Color R/G/B = `r` `g` `b`, Color Mode = Replace |
| Pulidas y porosas iguales | Los parámetros de brillo del Phong no se pudieron fijar | Sube Specular y Shininess en `mat_pulido` a mano |
| SEQ2 o batería `ignorado: canal X` | Canal distinto del de por defecto | `Canal2` (Fase2) o `Canaldrum` (Fase7); para el SEQ2, también apagar `Filtrar2` |
| Batería `pad fuera de 1-8` | Los pads no empiezan en do2 (36) | `Notabase` (Fase7) = la nota del pad 1 |
| La luz sale de un solo color | `luz_celda` no lee el color por instancia | Relanza cualquier fase (la recrea). Si persiste, en `luz_celda`: Instance 2 → Color R/G/B = `r` `g` `b` y Color Mode = Replace. El informe lo avisa con `FALLO luz_celda no lee el color por instancia` |
| No se ve dónde caen las notas con muchas conchas | El centro de la celda es pequeño desde la cámara de globo y se pierde entre las bandas de las losetas | Comprueba que `Luzconchas` esté encendido; sube `Luzconchaspulso` (y `Luzconchasreposo` para ver dónde está cada secuenciador entre notas) o `Luzconchasalcance` para que se tiñan más losetas. Si no se ve nada, relanza cualquier fase (crea `luz_conchas` y la mete en el render) y mira que `mat_luz_conchas` tenga la mezcla aditiva |
| No se ve la luz de una celda | `Luzseq` (secuenciadores) o `Balizasdrum` (batería) apagados, `Luzdrum` a 0, la batería o el secuenciador no llegan (mira las líneas `EROSION` y `NOTA`), o `luz_celda` fuera del render | Revisa esos; relanzar cualquier fase vuelve a meter `luz_celda` en el render |
| El mundo nunca se entierra por estancamiento | La batería está destruyendo: cada golpe genera novedad (hasta la fase 7 v11, también el bombo) | Es lo esperado; quita la batería para que el mundo se asiente |
| El bombo o el tom no erosionan ni cortan | Desde la fase 7 v12 son impulso: suman pulsos de ocupación (v14) y hinchan la celda un instante | Es lo esperado. Para que uno vuelva a erosionar, pon `erosion` en su `modo` de `perfiles_erosion` |
| La celda golpeada no se hincha | `Pumpon` apagado, `Pumpamt` 0, 1 pulso en la tabla, o la estructura ya pasa de `Pumptope` × el límite | Revisa esos; la leyenda dice dónde cayó (`IMPULSO ... celda N`) |
| Nacen varios satélites de golpe | Un bombo sobre una celda en el límite son 3 desbordes seguidos (fase 7 v14) | Es lo esperado. Con `Vecina` en `velocidadocupacion` se reparten; si salen apelotonados, baja los `pulsos` del pad |
| El mundo no se entierra nunca (la leyenda dice `esperando territorio`) | La batería no deja que se llene el territorio: cada golpe lo vacía, y la edad máxima solo entierra un mundo con el territorio ocupado | Quita la batería (el mundo se asienta y se entierra por estancamiento) o baja `Umbralterritorio`. Mira la columna `territorio` de la tabla `ciclos` |
| Los ciclos siempre acaban por edad máxima | Umbrales demasiado exigentes o un mundo que tarda en coronarse (carga) | Baja `Umbralmadurez`, sube `Umbralnovedad` o sube `Ciclomax`, y mira la tabla `ciclos` |
| Ciclos demasiado cortos | El mundo madura rápido (pattern al 100 %, pocas notas), `Umbralnovedad` alto, `Herencia` baja (el mundo nuevo arranca casi vacío) o un `Semillafrac` alto (los escalones bajos cuestan pocas notas) | `ajuste_vista.py` (ver «Calibración de la vista» en `MONTAJE_FASES_11_18.md`), o sube `Ciclomin` o `Compasesquietos` |
| Ciclos sin tocar o que no terminan | Línea de tiempo parada, o un STOP posterior | Play en el proyecto; el ciclo se reanuda con la siguiente nota (la leyenda pone `parado`) |
| El globo se acerca al borde un instante al enterrar | La concha nueva es gruesa y la transición tarda (nunca se sale) | Baja `Camsuave` o `Encuadre` (Fase10) |
| El planeta se ve pequeño | `Encuadre` bajo, o motor anterior al v36 | Sube `Encuadre` (1 = de borde a borde); relanza cualquier fase con motor v36 |
| Una construcción alta se sale del cuadro | `Encuadre` alto para ese mundo | Baja `Encuadre`; la leyenda dice `lo mas alto llega al ...%` |
| Pantalla negra (solo la leyenda) y la cámara está bien según la leyenda | Se navegó en el visor de la cámara: TouchDesigner guardó giro y pivote en `camara` (`rx ry rz`, `px py pz`) y la cámara mira a otra parte | Relanza cualquier fase con comun v28 (los pone a cero y lo avisa), o pon esos seis parámetros a 0. Para mirar el planeta usa el visor del render, no el de la cámara |
| No entiendo `Encuadremargen` ni `Holguraaltura` | Parámetros de los motores v33 a v35 | Relanza cualquier fase con motor v36: se quitan y queda `Encuadre` |
| La cámara se mueve todo el rato y el mundo se ve a ratos | Motor v32 (encuadraba lo que se dibujaba en cada fotograma) | Relanza cualquier fase con motor v33 |
| Hondonadas que bajan sin parar | Un pad con profundidad cae en cada mundo sobre las mismas celdas: pierde N losetas y recibe 1 | Sube `Colmatacion` (Fase8) o baja su profundidad en `perfiles_erosion` |
| El planeta engorda demasiado rápido | Sin compactación (`Cortezamax` 0, o motor anterior al v37), el engorde es `Shellthick` por cada `Ciclomin` compases | Relanza cualquier fase con comun v29 (crea `Cortezamax` 4) y baja `Cortezamax` si aún es mucho. Lo ya enterrado no adelgaza de golpe: `Resetmundo` para empezar de cero |
| La formación se queda baja y salta al límite de golpe | Motor anterior a la v58 con `Growstep` pequeño para `Semillafrac` y `Umbralram` | Relanza cualquier fase: desde la fase 3 v13 el escalón lo calcula el motor y no hay salto |
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
| 3 | ¿Incremento de altura por gate o fijo? | Por gate, con el fijo de respaldo (`Gatemax` 1) |
| 4 | ¿6 vecinas? | Hexagonal desplazada entre anillos completos; solape de arcos en los incompletos |
| 4 | ¿Quién elige la vecina? | Velocidad + ocupación (`Vecina`) |
| 4 | ¿Desborde en los polos? | El polo desborda a cualquiera de las celdas de su anillo |
| 5 | Canal del SEQ2 | 14 (`Canal2`), por confirmar |
| 6 | ¿Qué es un ciclo de ecosistema? | Lo cierra el mundo: maduro y quieto (`Umbralmadurez`, `Umbralnovedad`, `Compasesquietos`) desde `Ciclomin`, o lleno pasado `Ciclomax` |
| 6 | ¿Cuándo entierra la edad máxima? | Solo cuando el territorio (celdas tocadas por los secuenciadores en los últimos `Compasesterritorio` compases y sus vecinas) está ocupado (`Umbralterritorio` 0,8). Sin tope de seguridad; la novedad no cuenta |
| 6 | ¿Cómo se cuenta el tiempo? | En compases del tempo del proyecto (`ritmo.tempo()`); ya no se deduce el paso de cada nota |
| 6 | ¿Una vuelta por ciclo? | No: `Barsperturn` manual y `Girovivo` |
| 6 | ¿Los satélites cuentan para la madurez? | No: madurez = formaciones propias en el límite. Su forma se recorta al llegar a `Limsatelite` |
| 7 | Canal y pads de la batería | Canal 16 (confirmado), pads desde 36 (`Notabase`), por confirmar |
| 3–7 | ¿Balizas? | Sin balizas: secuenciadores y batería se ven igual, con la loseta del centro de la celda y la formación del color de quien acaba de tocarla; si coinciden, la luz más intensa |
| 7 | ¿Qué deshace un golpe? | Notas de construcción, con la misma moneda que la fase 3; la mitad en cada anillo de vecinas |
| 7 | ¿Qué pads cortan? | Perfiles del usuario: la caja (2), profundidad 3; 4 a 8 arañazos. Hasta la v11 cortaban también el bombo y el tom |
| 7 | ¿Qué hacen el bombo y el tom? (v12, v14) | Impulso: no destruyen. En la v12 y la v13 daban capacidad ×3 y ×2 (límite y umbrales multiplicados); desde la v14 suman 3 y 2 pulsos de ocupación (triggers completos) y el límite y los umbrales no cambian. Pumping al golpe, solo visual |
| 7 | ¿Qué especie siembra un impulso en una celda vacía? (v14) | La del secuenciador al que sigue el golpe (como `Objetivo`); sobre una celda ocupada, los pulsos no cambian su especie ni la colonizan |
| 7 | ¿El impulso adelanta las obras de la piel? (v14) | Sí, una etapa por golpe, como una nota (`Avance` gates) |
| 7 | ¿Pumping a saltos de stop-motion? (v12) | No: continuo. Desde la v13, un golpe seco (pico al instante, sostenido y caída cúbica en segundos) |
| 7 | ¿Tope de la caída por tempo? (v13; se mantiene en la v14) | El encargo pedía 0,8 × el paso (y el de la v14 lo repite). A 120 BPM eso es 0,1 s y dejaría el bombo (0,20) y el tom (0,12) iguales, cuando tienen que verse distintos. Además, con el pico sostenido la celda no llegaría a 1 antes del paso siguiente. Decisión: el golpe entero (pico y caída) cabe en 0,8 × el tiempo desde el golpe anterior de impulso en esa celda. En una ráfaga de semicorcheas es el tope por paso; con el bombo a negras, no recorta. El primer golpe de una ráfaga no sabe que viene otro: cae con su `pump_rel` y el segundo lo pilla a medio camino y salta otra vez al pico |
| 7 | ¿La velocidad y `Erosionvel`? (v13) | La velocidad escala siempre el pico del pumping (de `Pumpvelmin` a 1); `Erosionvel` sigue siendo solo de la erosión |
| 7 | ¿Dónde cae la erosión? | Alterna entre SEQ1 y SEQ2, desplazada por la velocidad (`Objetivo`) |
| 7 | ¿Radio 0 × 2? | Pasa a 1 |
| 8 | ¿Dónde se deposita el mundo enterrado? | Sobre la columna de cada celda: las hondonadas se tapizan. `Colmatacion` 0 (1 reproduce lo anterior) |
| 9 | Profundidad de corte | N losetas desde el suelo de cada columna, con tope por mundo; el núcleo es el fondo |
| 8–9 | Límite de altura en una hondonada | Medido desde el suelo de la celda, no desde la cota nominal |
| 8, 10 | Cámara | Radio nominal, para no meterse en las hondonadas |
| 8 | Núcleo | Esfera fija en el radio base; un zócalo por celda bajo las losetas visibles |
| 10 | Cámara por defecto | Globo encuadrado (radio nominal + altura máxima, travelling con FOV fijo, cámara fija en +Z, amortiguado crítico con mínimo de seguridad). La de superficie queda como modo (`Modocamara`) |
| 3–9 | Cámara antes de la fase 10 | La misma de globo, puesta por `estratos_comun.py` en todas las fases con motor; en las fases 1 y 2, `fase12_base.py` encuadra el núcleo con la misma fórmula |
| 8 | Paleta de las conchas | Un color por concha: ángulo áureo sobre el arco que dejan el cian y el ámbar, croma de mineral, claro y oscuro alternos, calculado de la generación. `Paleta` mineral para la anterior |
| 8 | Horneado a textura | Capa de losetas instanciadas |
| 8 | Grosor de concha | Proporcional a la duración del ciclo (`Grosortiempo`), entre 0,25× y `Ciclomax`/`Ciclomin` × `Shellthick` (0,5; límite de altura 1,875), con un tope de `Grosormax` (1,5). Las conchas viejas se compactan (`Cortezamax` 4): el radio es el tiempo comprimido |
| 3–4 | ¿Cuántas notas por trigger? | De 1 a `Costemax` (5) según la altura, con frenada; 5 desde el límite. La presión suma carga |
| 3 | ¿Cómo se reparten las notas? | `Notapolosur` y `Notapolonorte` (entre do1 y do8) son los polos; en medio, un anillo por octava; el rango decide el número de celdas; `Fuerarango` para las de fuera |

### Cómo se ha probado

Sin TouchDesigner a mano, todo se ha probado en simulación:

- **Desde cero frente a relanzado** (motor v19). Con un TouchDesigner simulado que ejecuta los scripts tal cual, se comparan dos proyectos:
  - uno construido desde cero, con `fase12_base.py` y las fases 3 a 10;
  - otro construido con la versión anterior al PR #7 (con baliza, `baliza2` y `balizas_drum`), con un mundo en marcha, y relanzado con las fases 3, 5, 7, 9 y 10.

  Los dos quedan con los mismos nodos, parámetros y lista del render, sin ninguna baliza, con el color por instancia enlazado en la retícula, las formaciones, las coronas, los estratos y la luz de celda, y con todas las expresiones evaluándose sin error. El mundo relanzado conserva su ocupación y sus conchas. Todas las autopruebas salen OK, incluida la de la fase 3 relanzada a nivel 10, que antes fallaba porque esperaba que no hubiera desborde. En ese TouchDesigner simulado, el Geometry COMP solo acepta los parámetros que tiene en TouchDesigner, para que un nombre equivocado no pase desapercibido.
- **Velocidad (fase 7 v7):** un golpe fuerte deshace más que uno flojo; el mínimo de una nota se respeta a velocidad 1; sin `Erosionvel` no cambia nada; N golpes iguales deshacen siempre lo mismo.

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
- **La edad máxima de la fase 6 v4** (motor v22):
  - Territorio ocupado y un cambio en cada compás: cierre por `edad maxima` en `Ciclomax`.
  - Territorio sin ocupar: pasado `Ciclomax` el mundo sigue, con `esperando territorio`; en cuanto se ocupa, se cierra en ese compás.
  - El territorio es la celda tocada y sus vecinas, y deja de contar a los `Compasesterritorio` compases.
  - 200 compases de SEQ1 con batería constante (bombo a negras y caja en 2 y 4, o un bombo por compás): ningún cierre ni error; territorio entre 0 % y 16 %, y la leyenda dice `esperando territorio`.
  - Sin batería: cierres por `estancado` cada 10-18 compases.
  - Bombo a negras durante 16 compases sobre un mundo maduro: ningún cierre; al quitarlo, cierre por `estancado` 24 compases después.
  - Relanzar sobre un proyecto antiguo: `Umbralnovedad` y `Compasesquietos` pasan a 0,15 y 2, la tabla `ciclos` gana la columna `territorio` y los parámetros nuevos salen con sus etiquetas.
- **Fase 7 v3:**
  - Perfiles nuevos: el pad 1 resta 1 en radio 2 sin abrir corte; los pads 2 y 3 abren cortes desde el nivel 9; ningún otro pad corta.
  - Relanzar sustituye una tabla con los valores de la v1, conserva una editada a mano y no pisa un `Canaldrum` cambiado a mano.
  - Luz de celda (motor v18):
    - la nota del SEQ1 enciende el centro de su celda en su color y queda tenue hasta la siguiente; la del SEQ2, en ámbar; con los dos en la misma celda, el centro se parte y se ven los dos;
    - desde la fase 9, el SEQ1 en blanco;
    - golpe (motor v21): el centro de la celda y la formación con el color del pad; en la celda del SEQ1 manda el golpe mientras dura y luego vuelve el SEQ1; una sola loseta por celda, sin borde; `luz_celda` lee el color por instancia;
    - la luz se ve con formación, vacía y con huella, gira con el planeta y sube con el radio;
    - no queda ninguna baliza en escena ni en `CHOP_NAMES`;
    - los pads 1, 2 y 3 cortan.
  - Fase 7 v5: el golpe ilumina la celda con el color de su pad y su radio más tenue, y se apaga a tiempo; dos pads dan dos colores y `luz_drum` lee el color por instancia; la luz se ve con formación, vacía y con huella; el pad 7 repetido con el SEQ1 tocando deshace una nota por golpe y la celda sigue creciendo; N notas de construcción y N de erosión devuelven la celda; la celda objetivo pierde más que sus vecinas; las balizas de la v3 desaparecen.
  - Balizas de la batería (v4, retiradas en la v5) fuera de la silueta del SEQ1 y del SEQ2 (en reposo y en el pulso), en el ecuador, junto al polo y en el polo, y con el SEQ2 en la celda vecina; las 8 de una celda sin tocarse; tamaño entre 0,18 y 0,30, por encima del mínimo perceptible (0,15) y por debajo del SEQ2 en reposo (0,495).
  - Balizas de la batería: los 8 pads en la misma celda encienden 8 balizas, cada una en su hueco y con su color; se apagan en `Vidabalizadrum`; ninguna es cian, ámbar ni blanca; giran y se balancean con el planeta; `Padprueba` + `Erosionar` también las encienden; `Modoactuacion` las oculta.
- **Sesión simulada de 192 compases** a 120 BPM: SEQ1 de 16 pasos al 90 %, SEQ2 de 13 y batería a tramos de 48 compases. Cierra por `estancado` en los tramos sin batería y por `edad maxima` en los tramos con batería (antes de la fase 6 v4; ahora, en los tramos con batería espera a que se ocupe el territorio).
- **Los scripts:** las fases 1 y 2 reales y las 3 a 10, ejecutadas en orden contra un TouchDesigner simulado, todas con `AUTOPRUEBA OK`. También se comprueba que no se puede saltar una fase y que relanzar una no borra el mundo.
- **Una sesión simulada:** 24 compases a 120 BPM con SEQ1 (16 pasos), SEQ2 (13) y batería, fotograma a fotograma. Detecta las dos longitudes, entierra conchas, y todas las expresiones de los nodos se evalúan sin error.

**El color de las luces** (fase 9 v8, fase 10 v7, comun v20). La Light COMP llama a su color `cr cg cb`, no `lightcolorr/g/b`. Hasta ahora los scripts usaban este último nombre y fallaban en silencio: la luz cenital y el relleno salían blancos, y el destello no tomaba el color de su pad. Ahora se fija por su nombre real (y se avisa con `..` si no está). Relanza la fase 9 y la 10 para verlo; si prefieres las luces blancas de antes, ponlas a mano en blanco.

**Dos avisos del render** (motor v31, comun v22). Desde la fase 10, el encuadre de la cámara leía el tamaño de la imagen del render (`render.width`), y el render depende de la cámara y las luces: TouchDesigner avisaba `Cook dependency loop detected` en `render` y `luz_relleno` (Translate). Ahora el aspecto sale de los parámetros de resolución del render (`resolutionw/h`), que no dependen de nada. Y la retícula giraba cada marca con «rotar hacia un vector» (`instancerottox/y/z` = la normal), que en los polos es paralela al vector arriba (`co-linear with the Up Vector`) y deja esas marcas sin girar; ahora el motor da el giro (`rx ry rz`, la marca plana sobre su celda, también en los polos) y se vacía «rotar hacia un vector». Relanza cualquier fase para aplicarlo. El aviso de `midiout` (`Could not open the MIDI interface`) no es de estos scripts: es el mapeador MIDI de TouchDesigner, que intenta abrir la salida del BeatStep.

Lo que la simulación no puede comprobar son los nombres exactos de algunos parámetros de TouchDesigner (orden de rotación y modo de color de las instancias, brillo del Phong, Look At). Los scripts los intentan con los nombres habituales y avisan con `..` si no los encuentran. La tabla de problemas dice dónde ponerlos a mano.

- **El mundo enterrado sobre el relieve** (motor v23, fase 8 v5, fase 9 v6):
  - Corte de 3 y enterrar con `Colmatacion` 0: la loseta nueva empieza en el suelo del corte, la laguna es la misma antes y después, y las celdas intactas suben un grosor.
  - `Colmatacion` 1: todas las celdas quedan en el radio nominal. Con 0,5, la laguna se reduce a la mitad. El radio nominal es el núcleo más la suma de las conchas con cualquier `Colmatacion`.
  - Golpes repetidos sobre la misma celda en un mundo no quitan más que su profundidad.
  - Corte de 2 en la misma celda durante 10 mundos: baja una loseta por mundo, llega al núcleo, avisa una sola vez y no da errores.
  - Ninguna columna tiene huecos ni solapes.
  - En la celda más honda, la formación, la luz de celda, la retícula y el destello van sobre su suelo.
  - Con más losetas que `Maxconchas`: se dibujan `Maxconchas` y el zócalo; la esfera del núcleo no crece.
  - Un corte enciende el fondo y las paredes recién expuestas; enterrar no enciende nada.
  - Un mundo del motor v16 con una celda cortada y enterrada y otra cortada en el mundo actual se relanza sin error: las dos quedan como hondonadas con la laguna que les toca.
  - Sesión de 160 compases a 120 BPM con SEQ1, SEQ2 y batería a tramos (16 compases con, 32 sin): 7 ciclos, 39 celdas con laguna tapizadas por conchas posteriores (130 losetas por debajo de su cota nominal), y todas las expresiones se evalúan sin error. Con los perfiles por defecto el bombo también corta, así que las cuencas bajan deprisa.

- **La cámara de globo** (motor v24, fase 10 v5):
  - Con radios 6, 11,5 y 43, aspectos 16:9, 4:3, 1:1 y 9:16 y FOV horizontal o vertical, el planeta ocupa exactamente `Encuadre` del lado más estrecho (0,85 y 1). Con conchas que crecen, fotograma a fotograma, la cámara se aleja y el planeta vuelve al 85 % sin pasar nunca del 100 %.
  - Concha fina: la distancia sube de 54,6 a 55,8 suave (como mucho 0,03 por fotograma) y sin bajar nunca; el globo cabe en todos los fotogramas.
  - Seis conchas gruesas de golpe al principio: salta de 54,6 a 103,5 (lo justo para que quepa) y el resto, hasta 111,7, llega suave.
  - Notas, erosión, cortes y `Colmatacion` sin enterrar: el radio de encuadre no cambia.
  - Resolución 720 × 1280: el encuadre se recalcula (con el FOV horizontal fijo, el lado estrecho pasa a ser el horizontal).
  - `Resetmundo`: salta al encuadre del núcleo en un fotograma.
  - Superficie en directo y vuelta a globo: transiciones de 20 s sin saltos (como mucho 0,16 por fotograma); la cámara no baja nunca del radio + `Camaltura`; al final, a `Camaltura` de la superficie.
  - Sesión de 26 conchas (37,5 de radio ganado, acelerada): distancia de 54,6 a 233,1 siempre creciente, globo entero en todos los fotogramas, 6 saltos de seguridad al principio (el mayor, 3,7), planos de recorte correctos y todas las expresiones evaluadas sin error.

- **La luz del secuenciador en las conchas** (motor v25, fase 8 v7):
  - Con 10 conchas, una nota del SEQ1 y otra del SEQ2 tiñen las 4 losetas superiores de su celda, más fuerte arriba.
  - Entre notas, la última celda de cada uno mantiene un reposo tenue (0,24 frente a 0,97 de brillo en la loseta superior) que respira; el color de las losetas (la generación, ocupada o vacía) no cambia: la luz va en una capa aparte.
  - Nota en el fondo de un corte: se tiñen la loseta del fondo y las de debajo; las paredes vecinas, no.
  - Una loseta con cicatriz reciente no se tiñe.
  - Un golpe de batería sobre una celda teñida sigue encendiendo su centro.
  - Con `Luzconchas` apagado no hay capa de luz.
  - Rendimiento con 24 conchas (2.040 losetas) y los dos secuenciadores en semicorcheas: como mucho 8 filas de luz por fotograma; la diferencia queda en el ruido (unas centésimas de milisegundo por fotograma).
  - La luz de celda no estaba por debajo de las losetas: va sobre el suelo de su celda + 0,02, por encima de la cara superior de la loseta de arriba (que llega a r_in + 0,98 × grosor).

- **Cada concha de un color** (motor v26, fase 8 v8):
  - Para n de 0 a 200, dos conchas seguidas difieren al menos 60° de tono y 0,1 de luminosidad, y ningún tono cae en 55°–100° ni en 165°–235°.
  - Todos los colores, vacía y ocupada, caen dentro de sRGB sin recortar; los 8 primeros coinciden con la tabla de referencia; la ocupada es siempre más clara que la vacía.
  - `Paleta` mineral reproduce exactamente los colores anteriores.
  - Un mundo con el color guardado en sus conchas sale con la paleta nueva, y cambiar `Paletatono` recolorea todas las losetas (el cambio de paleta rehace las losetas en el fotograma siguiente).
  - El cian de un corte se funde con el color de la concha de cada loseta.
  - Desde cero y relanzando, todas las autopruebas salen OK.

### Pruebas pendientes con el aparato

1. **All Notes Off:** cambiar de pattern dos veces y pulsar STOP, y copiar las líneas AVISO.
2. **RANDOMNESS:** comprobar si cambia la velocidad (columna `vel` de `midi_log`).
3. **Canal del SEQ2 y nota del pad 1.**
4. **Ciclos reales:** SEQ1 al 100 % sin batería; SEQ1 al 60 % con SEQ2 de 13 pasos; con batería constante. Copiar la tabla `ciclos` de cada caso para afinar `Umbralmadurez`, `Umbralnovedad`, `Compasesquietos` y `Ciclomax`.
5. **Quitar la batería:** con un mundo maduro y la batería destruyendo, quitarla y comprobar en cuántos compases se cierra el ciclo por `estancado` (en simulación, unos 24). Desde la fase 7 v12 el bombo no destruye: probarlo con la caja y los arañazos.
6. **Batería constante:** comprobar que la leyenda dice `esperando territorio` pasado `Ciclomax` y apuntar la ocupación del territorio, para afinar `Umbralterritorio`.
7. **Cuencas:** con la batería real, medir cuánto bajan las cuencas en 10 minutos (`laguna max` en la leyenda) y ajustar `Colmatacion`.
8. **Cámara de globo:** comprobar en el proyector real que el planeta ocupa el alto que dice `Encuadre` (la leyenda `CAMARA` lo dice) y que se aleja cuando crece una concha. Si la pantalla o la ventana de salida no es 16:9 y recorta la imagen, el planeta puede salirse aunque el render lo encuadre: pon la ventana con la misma proporción que el render (1280 × 720).
9. **Luz en las conchas:** con la cámara de globo y 10 conchas o más, comprobar que se ve dónde cae cada nota, y ajustar `Luzconchas` (la intensidad) con la luz real del proyector.
10. **Paleta:** con 10 conchas o más y un corte de 4, comprobar desde la cámara de globo que las bandas se distinguen una a una, y que los pads 7 y 8 no se confunden con las conchas.
11. **Impulso (fase 7 v12–v14):** con el bombo a negras sobre el SEQ1, mirar si cada golpe se ve como un golpe y la celda vuelve a su tamaño entre golpe y golpe; con bombo y tom alternando, si el bombo se nota más grande y algo más largo (ajustar `Pumpamt`, `Pumphold`, `pump_rel`, `Pumphorz` y `Pumptope`), y si los satélites que nacen de golpe salen apelotonados. Copiar la tabla `ciclos` de 20 minutos con y sin bombo para ver cuánto se acortan los mundos.

---

### Después de la fase 10

Fuera de este montaje: entrada por ethernet (OSC/UDP) como generador o modulador adicional; puente OSC hacia Unreal para el formato instalación (la tabla de ocupación y los eventos del motor son exactamente lo que habría que enviar); extensión física a motores.
