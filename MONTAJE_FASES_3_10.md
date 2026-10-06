# Estratos · Montaje
## Fases 3 a 10: de la baliza al planeta estratificado

*Continúa `MONTAJE_FASE1.md` (fases 1 y 2, ahora en un solo script: `fase12_base.py`). Plan de referencia: `PLAN_FASES.md`.*

---

### Estado en una frase

Cada nota del SEQ1 y del SEQ2 deposita y hace crecer formaciones sobre el planeta. Al toparse con el límite de altura se ramifican, se fusionan y se coronan. La batería las erosiona. Cada ciclo de ecosistema entierra el mundo como una concha nueva, y los cortes profundos dejan ver las capas enterradas.

---

### Archivos

Todos en la misma carpeta: `C:/Users/DareDave/Downloads/est`.

| Archivo | Para qué | Versión |
|---|---|---|
| `fase12_base.py` | Fases 1 y 2 en uno: núcleo, retícula de polo a polo, baliza, MIDI, render y leyenda. Lleva dentro el arreglo del render | `fase12 v2` |
| `estratos_motor.py` | La lógica entera del mundo. Lo cargan las fases; no se ejecuta solo | `motor v7` |
| `estratos_comun.py` | Piezas compartidas por los scripts de fase; no se ejecuta solo | `comun v5` |
| `fase3_semilla.py` | Ocupación, semilla, crecimiento, material, balanceo del eje, polos y anillos | `fase3 v5` |
| `fase4_desborde.py` | Desbordamiento, satélites, fusión, coronación | `fase4 v3` |
| `fase5_especies.py` | SEQ2, arquitectura, híbridos, segunda baliza | `fase5 v1` |
| `fase6_ciclo.py` | Longitud de pattern, biblioteca, ciclo, vuelta por ciclo | `fase6 v1` |
| `fase7_erosion.py` | 8 pads de erosión, huellas, presupuesto de densidad | `fase7 v1` |
| `fase8_conchas.py` | Conchas, herencia, radio que crece | `fase8 v1` |
| `fase9_arqueologia.py` | Cortes, estratigrafía, cicatriz cian, destello | `fase9 v1` |
| `fase10_direccion.py` | Paleta, luz cenital, cámara de superficie, modos | `fase10 v1` |

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
i_formas_pulidas  i_formas_porosas  i_coronas     i_estratos     i_baliza2   (Script CHOP)
     │                │               │              │              │
formas_pulidas    formas_porosas    coronas        estratos       baliza2     (Geometry COMP)
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
| `latido` | Recalcula la baliza | Además avanza el motor y redibuja |
| `baliza_callbacks` | Baliza sobre el radio fijo | Misma lógica de pulso; se posa encima de la formación y sigue a la superficie |
| `reticula_callbacks` | Radio fijo 6 | Marcadores sobre la superficie actual (suben con las conchas) |
| `rotulo` | Tempo + nota | Tempo + nota + motor |

**No relances `fase12_base.py` sobre un proyecto en marcha**: crea una FASE1 nueva y vacía (la vieja queda como `FASE1_anterior`, apagada) y obliga a aplicar de nuevo las fases 3 en adelante. Para refrescar el motor, relanza la última fase aplicada.

**Diagnóstico del render.** `fase12_base.py` y cada fase terminan con un bloque `DIAGNOSTICO DEL RENDER`: qué geometrías dibuja el render, con qué cámara y luces, y qué nodos de la cadena hasta `salida` tienen errores (motor, Script CHOP, rótulo…). Si no ves la imagen, pégame ese bloque. Las leyendas ya no pueden romper la salida: si fallan, escriben el fallo en el rótulo.

---

## FASE 3 · La semilla

Cada nota del SEQ1 suma 1 a la ocupación de su celda.

| Ocupación | Resultado |
|---|---|
| 1 | Semilla: altura `Semillafrac` × límite |
| 2–3 | Crece `Growstep` × límite por señal |
| 4+ | Límite de altura = `Alturafactor` × `Shellthick` (3 × 0,5 = 1,5) |

- **El gate decide cuánto crece** (`Gatemode`). Al llegar el note off se mide cuánto duró la nota respecto a un paso: un gate al 50 % da el crecimiento normal, un gate corto la mitad o menos (hasta ¼) y uno ligado hasta el doble. Sin note off, crecimiento normal.
- **Material**: la velocidad de la primera nota decide (`Umbralvel`, 64). Por encima, `mat_pulido`: brillo alto, casi metálico. Por debajo, `mat_poroso`: mate. No vuelve a cambiar.
- **Animación**: la altura visible se acerca a la real en ~0,1 s; las formaciones brotan, no aparecen de golpe.
- **Balanceo del eje** (v2): además del giro al tempo, el eje se balancea hacia la cámara y en contra, `Balanceo` grados (60) cada `Balanceoper` segundos (90), para ver los dos polos. Va aparte del reloj del secuenciador y se congela con `Pausa`. `Rotextra` lo enciende y lo apaga; entra y sale en 3 s, sin saltos. Lo llevan todas las geometrías que giran con el planeta (núcleo, retícula, balizas, formas, coronas, estratos) y la luz de destello. Orden de rotación: `Ry Rx Rz` (giro, balanceo, inclinación).

**Página Fase3:** `Shellthick` 0,5 · `Alturafactor` 3 · `Semillafrac` 0,25 · `Growstep` 0,30 · `Gatemode` · `Umbralvel` 64 · `Velprueba` 100 · `Sembrar` · `Resetmundo` · `Rotextra` · `Balanceo` 60 · `Balanceoper` 90 · `Notapolosur` 24 · `Notapolonorte` 108 · `Fuerarango`

Los tres últimos los crea ya `fase12_base.py` en esta página; si venían de la página Fase1 (versión anterior), la fase 3 los mueve aquí conservando su valor.

**Leyenda:** `MUNDO ocupadas 23/85 (27%) max 4 fase 3`, `RANGO do1 24 (polo sur) a do8 108 (polo norte) 85 celdas fuera: plegar` y `ULTIMA geo celda 40 ocupacion 3 crecimiento`. En la línea NOTA: `celda 40 de 85 anillo 4`, y `(como do1 24)` si la nota se ha plegado.

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

Desde la ocupación 4, cada señal que llega a una formación se desborda a una vecina.

| Ocupación | Resultado |
|---|---|
| 4–5 | Satélites en la vecindad (más pequeños: `Tamsatelite`) |
| 6–7 | Fusión: un macizo bajo bajo el núcleo y sus satélites los une en una masa |
| 8+ | Coronación: aguja ámbar (geología) o antena con remate (arquitectura) |

- **Desborde a una celda vacía:** nace un satélite de esa formación.
- **Desborde a su propio satélite:** el satélite crece, hasta `Limsatelite`.
- **Desborde a una formación ajena:** le suma ocupación (presión), sin cascada. Si es de la otra especie, la marca como híbrida.
- **Un satélite que recibe una nota directa** se independiza.

**Decisión: 6 vecinas.** Entre dos anillos completos, la retícula se trata como hexagonal desplazada: 2 vecinas en el mismo anillo, 2 en el de arriba y 2 en el de abajo (los pares miran a los meridianos c−1 y c, los impares a c y c+1). En un anillo incompleto, las vecinas del anillo contiguo son las celdas cuyo arco se solapa con el suyo, y en los anillos extremos se suma el polo. El polo tiene de vecinas todo su anillo (11 con do1).

**Decisión: quién elige la vecina.** No el azar del software:

- `Vecina = velocidad`: velocidad mod nº de vecinas;
- `Vecina = velocidad + ocupación` (por defecto): la formación da la vuelta a su vecindad conforme insiste, aunque la velocidad sea fija.

Si el knob RANDOMNESS del SEQ1 varía la velocidad, la decisión pasa a ser del aparato. **Por confirmar**: gira RANDOMNESS y mira la columna `vel` de `midi_log`.

**Página Fase4:** `Umbralram` 4 · `Umbralfusion` 6 · `Umbralcorona` 8 · `Tamsatelite` 0,6 · `Limsatelite` 0,6 · `Vecina`

**Leyenda:** `DESBORDE 57 -> 44 satelites 3 fusiones 1 coronas 0`

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

**Baliza del SEQ2:** esfera ámbar, más pequeña que la del SEQ1.

**Página Fase5:** `Canal2` 14 · `Nota2` · `Sembrar2`

**Por confirmar:** el canal del SEQ2. Si sus notas salen en el Textport como `ignorado: canal X`, pon X en `Canal2`.

**Leyenda:** `SEQ2 canal 14 notas 37 hibridas 3`

---

## FASE 6 · El ciclo

Rehace el trabajo aparcado (`fase2f` a `fase2j`) sobre la base nueva.

**El paso de cada nota.** La longitud del pattern no viaja por MIDI, y FASE1 no lee el reloj (eso lo hace midicontrolx). El paso se deduce del tempo del proyecto: cada nota cae N pasos después de la anterior, y el reloj se reancla en cada nota, así el error no se acumula mientras el desfase sea menor de medio paso. START (`FA`) o MMC Play ponen el paso a 0. Si el BeatStep no usa semicorcheas, ajusta `Pasospornegra`.

**Longitud del pattern.** Busca el periodo más corto con el que se repiten las notas, comparando solo pasos que han sonado, así que tolera la probabilidad. No da por buena una longitud L hasta poder comprobar 2L, para no confundir un pattern de 16 cuyas mitades se parecen con uno de 8. Cada 16 notas revisa su conclusión y la corrige si hace falta.

Probado en simulación con patterns aleatorios de 8, 12, 13, 16, 24 y 32 pasos y probabilidad al 100, 80 y 60 %: acierta en 540 de 540 casos. Con 16 pasos al 60 % la detección llega hacia el paso 53 (unas tres vueltas).

**Biblioteca.** Guarda la huella de cada pattern detectado (hasta 16 por secuenciador) y, al volver a uno conocido, lo reconoce en unas tres notas.

**Cambio de pattern.** Se detecta de dos maneras:

- una ráfaga de All Notes Off (CC 123 en 8 canales o más en 0,12 s) que no llega acompañada de un STOP;
- 4 de las últimas 6 notas no encajan con el pattern conocido.

**Ciclo de ecosistema:**

- `Modociclo = repeticiones` (defecto): `Repsporciclo` × el pattern más largo. Con 8 × 16 pasos, 8 compases: 16 s a 120 BPM.
- `Modociclo = hiperperiodo`: mínimo común múltiplo de los dos. Con 16 y 13, 208 pasos.

Nota: tomar al pie de la letra «nueva concha al reinicio del generador más largo» daría una concha cada compás. Con `Repsporciclo = 1` se obtiene exactamente eso.

**Una vuelta por ciclo.** Con `Turnauto`, `Barsperturn` se calcula sola (pasos del ciclo ÷ `Pasosporcompas`): el día del planeta dura un mundo. El giro sigue acumulándose, así que el cambio de longitud no hace saltar el planeta.

**El ciclo solo avanza con el secuenciador en marcha:** línea de tiempo en play, sin STOP posterior a la última nota, y alguna nota en los últimos 4 compases.

**Página Fase6:** `Repsporciclo` 8 · `Modociclo` · `Turnauto` · `Longmanual` 16 · `Longfija` · `Longmin` 4 · `Pasosporcompas` 16 · `Pasospornegra` 4 · `Forzarciclo` · `Resetpatterns`

**Leyenda:**

```
CICLO    SEQ1 16 pasos (escucha)   SEQ2 13 pasos (biblioteca)
         ciclo 4   paso 87/128
AVISO    SEQ1: pattern de 16 pasos (100%)
```

**Prueba pendiente con el aparato:** cambia de pattern dos veces y pulsa STOP mirando el Textport. Cada ráfaga sale como `AVISO All Notes Off sin STOP: cambio de pattern` o `AVISO All Notes Off junto a un STOP`. Si al cambiar de pattern no sale nada, el BeatStep no la envía en ese caso; el cambio se detectará igualmente por las notas.

**Si un pattern repite mucho la misma nota,** la longitud es ambigua (16 notas iguales también se repiten cada 4). Para esos casos: `Longfija` + `Longmanual`.

---

## FASE 7 · Erosión superficial

Las 8 pistas de batería son las 8 señales de destrucción. Cada una tiene su perfil en la tabla `perfiles_erosion`, editable a mano:

| Pad | Reducción | Radio | Profundidad | Tipo |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 | arañazo |
| 2 | 1 | 0 | 0 | arañazo |
| 3 | 1 | 1 | 0 | arañazo |
| 4 | 2 | 0 | 0 | arañazo |
| 5 | 2 | 1 | 0 | arañazo |
| 6 | 2 | 1 | 2 | corte |
| 7 | 3 | 1 | 3 | corte |
| 8 | 3 | 2 | 4 | corte profundo |

**Orden de caída** (inverso al crecimiento): primero los satélites, luego la altura, y al final la **huella**, una mancha oscura que dura hasta que la celda se vuelve a sembrar o se entierra.

**Presupuesto de densidad.** Por encima de `Umbraldensidad` (60 % de celdas ocupadas), el radio de todos los eventos se multiplica por `Multradio` (×2); un radio 0 pasa a 1, para que también los arañazos ayuden a aligerar. La leyenda marca `x2` mientras dura.

**Decisión: dónde cae la erosión.** Los pads no tienen altura, así que no dicen celda. Opciones de `Objetivo`:

- `alterna` (defecto): los pads impares caen donde está el SEQ1, los pares donde está el SEQ2;
- `seq1` / `seq2`: siempre donde está ese secuenciador;
- `velocidad`: la velocidad del golpe elige una de las celdas.

En las tres primeras, la velocidad desplaza el golpe un semitono a un lado, al otro o a ninguno. La destrucción persigue a la construcción.

**Página Fase7:** `Canaldrum` 10 · `Notabase` 36 · `Objetivo` · `Umbraldensidad` 0,6 · `Multradio` 2 · `Padprueba` · `Erosionar`

**Por confirmar:** el canal de la batería y la nota del primer pad. Si los golpes salen como `ignorado: canal X` o `pad fuera de 1-8`, ajusta `Canaldrum` y `Notabase`.

**Leyenda:** `EROSION pad 3 -1 radio 1 celda 52 densidad 64% x2`

---

## FASE 8 · Conchas

En cada fin de ciclo:

1. **La capa se entierra** como una concha de losetas, una por celda, con el color de su generación. Las celdas que estaban ocupadas quedan más claras: los continentes se leen en el color. Sus formaciones se descartan.
2. **El planeta engorda** `Shellthick`.
3. **Herencia:** el 25 % de la ocupación de cada celda pasa a la capa nueva. La fracción que no llega a 1 se acumula para el ciclo siguiente: una celda con ocupación 2 en ciclos seguidos acaba heredando. Lo heredado vuelve a brotar desde la nueva superficie.

**Paleta de generaciones:** ámbar en la base, después grises minerales y negros que se alternan en claro y oscuro para que las bandas se distingan.

**Decisión: el horneado.** El marco pide hornear cada concha a una textura proyectada sobre una esfera. Aquí cada concha es una capa de losetas instanciadas, todas del mismo tamaño porque las celdas son de área igual:

- igual de barata: una sola geometría;
- sin shaders;
- en la fase 9 permite abrir cortes quitando losetas y ver las paredes de cada capa con su color, que es justo lo que pide la estratigrafía.

Solo se dibujan las últimas `Maxconchas` (24). Las anteriores quedan dentro de la esfera del núcleo, que crece para taparlas.

**Continentes** (en la leyenda): regiones de celdas vecinas ocupadas en al menos la mitad de las 8 últimas conchas.

**Cámara:** en esta fase solo se aleja con el radio para no quedar dentro del planeta. La definitiva llega en la fase 10.

**Página Fase8:** `Herencia` 0,25 · `Maxconchas` 24. Para probar sin esperar a un ciclo: `Forzarciclo` (página Fase6).

**Leyenda:** `CONCHAS 11 radio 11.50 herencia 25% continentes 3`

**Ritmo de engorde:** con los valores por defecto, 0,5 de radio cada 16 s, es decir 37 unidades en 20 minutos sobre un núcleo de 6. Si es demasiado, sube `Repsporciclo` o baja `Shellthick`; también se puede usar el hiperperiodo.

---

## FASE 9 · Arqueología

**Cortes.** Los pads con profundidad mayor que 0 (por defecto el 6, el 7 y el 8) quitan las losetas de las conchas superiores en forma de **anfiteatro**: profundidad completa en la celda golpeada, un escalón menos en cada anillo. Las paredes son las capas enterradas, cada una con su color. El hueco es permanente; solo lo cubre la concha siguiente.

- **Las formaciones de una celda cortada** se apoyan en el fondo del corte.
- **Cicatriz:** el fondo y las paredes recién expuestos se ven en **cian** y se funden con el mineral en `Cicatriz` segundos.
- **Destello:** `luz_destello`, una luz puntual que sigue el giro del planeta, golpea la celda en cada destrucción: fuerte en los cortes, suave en los arañazos.
- **Balizas:** la del SEQ1 pasa a blanca, porque el cian queda reservado para lo recién expuesto.

**Página Fase9:** `Cicatriz` 4 s · `Destello` 3

**Leyenda:** `CORTE celda 41 3 conchas expuestas cicatriz 2.1 s`

---

## FASE 10 · Dirección visual

- **Cámara de superficie.** Órbita lenta (`Camvel`, 0,6 °/s: unos 10 minutos por vuelta), ajena al reloj del secuenciador, a `Camaltura` de la superficie. Mira a un punto del horizonte por delante: la curvatura se insinúa y el globo no se ve. Como la distancia es a la superficie, el encuadre no cambia y el crecimiento solo se nota por acumulación. Se controla con el nodo `objetivo` (Look At).
- **Plano final.** `Planofinal` aleja la cámara en 20 s, con curva suave, hasta ver el globo entero. Al quitarlo vuelve.
- **Luz.** Cenital fría que sube con el planeta, y un relleno azulado muy tenue. El eje sigue inclinado `Tilt` (20°).
- **Núcleo:** negro profundo.
- **Modo actuación.** `Modoactuacion` oculta la retícula, las balizas y la leyenda: el switch `modo` pasa la salida al render limpio. Al quitarlo vuelve el modo diagnóstico.

**Página Fase10:** `Modoactuacion` · `Planofinal` · `Camaltura` 4 · `Camvel` 0,6

---

### Cómo comprobar el sistema completo

1. **PLAY con el SEQ1.** Las celdas que toca se siembran; las que repite crecen hasta el límite y después ramifican.
2. **Añade el SEQ2.** Aparecen torres; donde los dos se cruzan, híbridos.
3. **Espera unas tres vueltas.** La línea CICLO pasa de `escuchando` a `16 pasos (escucha)`.
4. **Cambia de pattern en el BeatStep.** Sale un AVISO de cambio; al volver al pattern anterior, `biblioteca`.
5. **Añade la batería.** Los arañazos rebajan el paisaje y la densidad se mantiene por debajo del 60 %.
6. **Fin de ciclo.** El mundo se entierra, el planeta engorda y lo heredado vuelve a brotar.
7. **Pads 6 a 8 con varias conchas.** Se abre un corte con las capas a la vista, primero en cian.
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
| Todas las formaciones del mismo color | El modo de color por instancia no es Replace | En cada geometría: Instance → Color Mode = Replace |
| Pulidas y porosas iguales | Los parámetros de brillo del Phong no se pudieron fijar | Sube Specular y Shininess en `mat_pulido` a mano |
| SEQ2 o batería `ignorado: canal X` | Canal distinto del de por defecto | `Canal2` (Fase5) o `Canaldrum` (Fase7) |
| Batería `pad fuera de 1-8` | Los pads no empiezan en do2 (36) | `Notabase` (Fase7) = la nota del pad 1 |
| La longitud no se detecta nunca | Pattern muy repetitivo, o no son semicorcheas | `Longfija` + `Longmanual`, o ajusta `Pasospornegra` |
| La longitud sale la mitad de la real | Las dos mitades del pattern son iguales (en realidad se repite así) | Es correcto; si no lo quieres, `Longfija` |
| Ciclos sin tocar o que no terminan | Línea de tiempo parada, o un STOP posterior | Play en el proyecto; el ciclo se reanuda con la siguiente nota |
| El planeta engorda demasiado rápido | Ciclos cortos | Sube `Repsporciclo`, baja `Shellthick`, o hiperperiodo |
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
| 6 | Paso de cada nota sin leer el reloj | Del tempo del proyecto, reanclado en cada nota |
| 6 | ¿Qué es un ciclo de ecosistema? | 8 repeticiones del pattern más largo (`Repsporciclo`, `Modociclo`) |
| 7 | Canal y pads de la batería | Canal 10, pads desde 36 (`Canaldrum`, `Notabase`), por confirmar |
| 7 | ¿Dónde cae la erosión? | Alterna entre SEQ1 y SEQ2, desplazada por la velocidad (`Objetivo`) |
| 7 | ¿Radio 0 × 2? | Pasa a 1 |
| 8 | Horneado a textura | Capa de losetas instanciadas |
| 8 | Grosor de concha | 0,5 (límite de altura 1,5) |
| 3 | ¿Cómo se reparten las notas? | `Notapolosur` y `Notapolonorte` (entre do1 y do8) son los polos; en medio, un anillo por octava; el rango decide el número de celdas; `Fuerarango` para las de fuera |

### Cómo se ha probado

Sin TouchDesigner a mano, todo se ha probado en simulación:

- **El motor:** 18 pruebas. Orientación de las piezas sobre la normal de cada celda, vecindad simétrica, crecimiento y límite, gate, desborde y estados, híbridos, detección de longitud (16 y 13 a la vez, con probabilidad, biblioteca, cambio por notas), ráfagas con y sin STOP, ciclos y conchas, orden de la erosión y presupuesto, cortes y cicatrices, herencia y continentes, y que el mundo se pueda guardar.
- **Los scripts:** las fases 1 y 2 reales y las 3 a 10, ejecutadas en orden contra un TouchDesigner simulado, todas con `AUTOPRUEBA OK`. También se comprueba que no se puede saltar una fase y que relanzar una no borra el mundo.
- **Una sesión simulada:** 24 compases a 120 BPM con SEQ1 (16 pasos), SEQ2 (13) y batería, fotograma a fotograma. Detecta las dos longitudes, entierra conchas, y todas las expresiones de los nodos se evalúan sin error.

Lo que la simulación no puede comprobar son los nombres exactos de algunos parámetros de TouchDesigner (orden de rotación y modo de color de las instancias, brillo del Phong, Look At). Los scripts los intentan con los nombres habituales y avisan con `..` si no los encuentran. La tabla de problemas dice dónde ponerlos a mano.

### Pruebas pendientes con el aparato

1. **All Notes Off:** cambiar de pattern dos veces y pulsar STOP, y copiar las líneas AVISO.
2. **RANDOMNESS:** comprobar si cambia la velocidad (columna `vel` de `midi_log`).
3. **Canales del SEQ2 y de la batería,** y la nota del pad 1.

---

### Después de la fase 10

Fuera de este montaje: entrada por ethernet (OSC/UDP) como generador o modulador adicional; puente OSC hacia Unreal para el formato instalación (la tabla de ocupación y los eventos del motor son exactamente lo que habría que enviar); extensión física a motores.
