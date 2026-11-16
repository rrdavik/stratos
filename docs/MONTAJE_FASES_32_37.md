# Estratos · Montaje
## Fases 32 a 37: el juego «El devorador»

*Continúa `MONTAJE_FASES_24_31.md`. Referencia: `docs/ENCARGO_JUEGO_DEVORADOR.md` (encargo del 14 de noviembre de 2026; diseño de origen «Stratos · Juegos de sala», apartados 5 a 9). Las reglas de siempre: un script por fase, encima de la anterior, con su versión en la primera línea del informe, su página `FaseNN`, su línea en la leyenda, su `LEEME` y una AUTOPRUEBA al final que deja el mundo como estaba. Para tenerlo todo al día, `recargar_todo.py` (ya lanza también las fases 32 a 37).*

Turf War de toda la sala contra un monstruo. El público construye quedándose quieto; el monstruo aparece en el planeta, va de una construcción próspera a otra devorándola y deja brotes del mal. Al acabar la ronda se compara el territorio del público con el del mal.

**No toca el núcleo.** El juego es un modo que se enciende encima del mundo con `Modojuego`. Con `Modojuego` apagado, el mundo se comporta exactamente como antes (lo comprueba la autoprueba de la fase 32: la misma sesión simulada da el mismo `W` con la fase 31 y con la 37, y `W` no tiene ni `juego` ni `bloqueadas`). Los pocos enganches en el núcleo (el desborde, la colonización, la herencia, la fila, la luz de sala) están todos condicionados al modo de juego. **Lo visual es provisional**: el monstruo, el tocón, el velo de los brotes, las marcas y el agua van en geometrías propias, que se cambian sin tocar la lógica.

| Fase | Script | Qué hace | Motor |
|---|---|---|---|
| 32 | `fase32_juego.py` | Modo de juego, ronda, recuento del globo, herencia del mal y marca de jugador | v106 |
| 33 | `fase33_monstruo.py` | El monstruo (aparición, objetivo, movimiento, devorar, crecer) y los brotes del mal | v107 |
| 33 v4 | `fase33_monstruo.py` | GENoZilla un tercio más lento: `Pasomonstruo` 24 y `Pasogrande` 12 (antes 16 y 8) | v120 |
| 34 | `fase34_zanjas.py` | Zanjas de las filas, caída del monstruo y agua | v108 |
| 35 | `fase35_rescate.py` | Rescatar brotes entre cuatro | v109 |
| 36 | `fase36_luzjuego.py` | La luz de sala cuenta la partida | v110 |
| 37 | `fase37_armas.py` | Armas opcionales: cerco, pisotón, estatuas, grito y relámpago (apagadas) | v111 |

`estratos_comun.py` pasa a la **v82**: la familia de material `mal` en el shader de la piel (`mat_piel_mal`, familia 9) y `SalaJuego`, el ayudante de las autopruebas del juego.

**Antes de nada.** Todo se prueba sin cámara con `Fuente` = simulada (página Fase22) y las filas de prueba de las fases 24 y 29 (`Simfila`, `Simformarfila`, `Simsumar`, `Simvaciar`). Como siempre, las autopruebas corren con `Activo` y `Noche` apagados (salvo la de la fase 36, que pone `Noche` ella) y devuelven tus valores al terminar.

---

## El estado del juego y la unidad de ritmo

El estado vive en `W['juego']` (se guarda con el `.toe`, como el resto del mundo). Lo crea `Modojuego` y lo vacía su apagado:

```python
W['juego'] = dict(
    activo=True, estado='juego',        # 'espera' al acabar la partida
    ronda=1, rondas=4, t0=..., paso=0, semis=0,
    mon=dict(estado='espera', celda=None, tam=0.5, acum=0, objetivo=None, camino=[], mov=0.0,
             t_muerte=None, n=0, ...),   # espera | aparece | busca | devora | cae | muere
    zanjas={},      # celda -> profundidad en conchas
    agua={},        # celda -> nivel de agua en escalones
    rescates={},    # celda -> instante en que empezo el rescate
    ultimoseq={},   # celda -> 'geo' | 'arq'
    recuento=dict(publico=0, mal=0),
    resultados=[],  # una por ronda: ronda, publico, mal, gana
    filas={}, armas={...}, ev={...})
W['bloqueadas'] = {celda: True}     # las celdas de zanjas fijadas, hasta el ciclo siguiente
```

La especie nueva es `MAL = 4` (`SPECIES_NAME[4] = 'mal'`), junto a geología (1), arquitectura (2) e híbrido (3).

**Unidad de ritmo.** Un paso de juego son `Pasojuego` semicorcheas del pulso de la fase 17 (`master_beat` si está; si no, el tempo), por defecto 4: una negra. El juego avanza **semicorchea a semicorchea** (el movimiento del monstruo va en semicorcheas; devorar, el agua y las armas, en pasos de juego), así que el resultado no depende de los fotogramas. No depende de los triggers de los secuenciadores ni de la batería. Con el transporte parado el juego se queda quieto, pero el reloj de la ronda (en segundos) sigue.

---

## FASE 32 · Modo de juego y ronda

```python
exec(open('C:/Users/DareDave/Downloads/est/fase32_juego.py').read())
```

### Qué hace

- **Modo.** `Modojuego` encendido crea `W['juego']` y empieza la ronda 1. Apagado lo vacía y quita el monstruo, los brotes del mal (sus celdas quedan vacías), las zanjas y el agua de juego, sin tocar el resto del mundo.
- **Ronda.** Dura `Duracionronda` segundos. Al acabar: recuento, entierro con `close_cycle` (el mismo camino que `Forzarciclo`: la concha, la clasificación de la fase 27, la noche de la fase 28), y ronda siguiente con el monstruo en espera. Tras `Rondas` rondas el modo se queda en espera con el resultado en la leyenda; `Nuevapartida` vuelve a la ronda 1.
- **Solo entierra la ronda.** En modo juego ni el ciclo de la fase 6 (estancado, edad máxima, cambio de pattern) ni el colapso de la fase 23 cierran el mundo: lo cierra la ronda (o `Forzarciclo`, a mano). El mundo sigue midiendo madurez y novedad como siempre.
- **Recuento.** Sobre **todas las celdas del globo**, en la cara visible y fuera de ella (D3). Público: celdas con `occ > 0` y `sp != MAL`; mal: celdas con `occ > 0` y `sp == MAL`. Gana el mayor; en empate, el público. Se recalcula en cada fotograma (85 celdas: nada). La partida la gana quien gane más rondas (en empate de rondas, el público).
- **Herencia del mal.** Al enterrar en modo juego, la ocupación del mal se hereda con `Herenciamal` (0, D9) en lugar de `Herencia`. La concha guarda `sp = MAL` en sus celdas, como guarda cualquier especie.
- **Marca de jugador.** Un anillo de 8 listones en la celda que mira cada persona de la sala (fase 24), de un solo color de la paleta humana para toda la sala (familia plástico, como las inclusiones).

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `marcas`, `i_marcas` | Geometry COMP instanciado: los listones de los anillos, con `mat_piel_plastico` |

### Parámetros (página Fase32)

`Modojuego` apagado · `Duracionronda` 360 s · `Rondas` 4 · `Pasojuego` 4 · `Herenciamal` 0 · `Marcajugador` encendido · `Nuevapartida` (pulso)

### Leyenda

```
JUEGO    ronda 2/4   4:12   publico 38   mal 14   (globo)
JUEGO    fin   gana publico 3-1   (ronda 4: publico 30   mal 22)   Nuevapartida
```

### Prueba manual

`Modojuego` y `Duracionronda` 20: a los 20 s se entierra el mundo (fila `ronda` en la tabla `ciclos`) y la leyenda pasa a la ronda 2. `Simponer` en una casilla: aparece el anillo en la celda que mira. Apagar `Modojuego` a mitad de ronda: el mundo sigue como estaba, sin los brotes del mal.

### Autoprueba

- Con `Modojuego` apagado, una sesión simulada (notas de los dos secuenciadores, golpes de batería, el reloj del mundo y un entierro a mitad) da el mismo `W` en el nivel 31 que en el actual, sin `juego` ni `bloqueadas`.
- El recuento cuenta todas las celdas del globo, también las de fuera de la cara visible, con un mundo preparado a mano; el empate es del público.
- Fin de ronda: entierro (motivo `ronda`), ronda + 1 y recuento a cero; el mal no se hereda y la concha guarda `sp = MAL`; tras `Rondas`, espera (y no entierra más); `Nuevapartida`.
- La marca: 8 listones en la celda de la persona, del color de la paleta humana; `Marcajugador` apagado, ninguno. La línea `JUEGO`.
- Apagar a mitad de ronda: sin estado de juego ni brotes; las columnas y el resto de la ocupación, iguales.

---

## FASE 33 · El monstruo y los brotes del mal

```python
exec(open('C:/Users/DareDave/Downloads/est/fase33_monstruo.py').read())
```

### Qué hace

- **Aparición (D2).** Cuando la fracción de celdas de la cara visible (las que tienen casilla en la sala) con `occ > 0` y `sp != MAL` llega a `Umbralaparicion`, el monstruo aparece en la celda vacía de la cara visible más cercana al borde por el que entran las celdas con el giro (el sentido en que avanza `Loncentral`), con desempate `_hash01`, y tamaño `Tamanoinicial`.
- **Objetivo.** Cada `Recalculo` pasos de juego, siempre que vacía una celda y cuando el objetivo deja de ser comestible: un Dijkstra por `vecinas6` (la vecindad de la fase 4) en el que entrar en una zanja cuesta `Costezanja` y el agua es muro. El objetivo es el de mayor `occ / (1 + coste)` (desempate `_hash01`). El pequeño no elige fusiones (`occ` desde `Umbralram + Pasoumbral`) ni coronas (desde `Umbralram + 2 Pasoumbral`): los umbrales de la página Fase4.
- **Movimiento.** Una celda por el camino cada `Pasomonstruo` semicorcheas (`Pasogrande` en forma grande). Sin objetivo, quieto. Entre dos celdas se dibuja a medio camino.
- **Devorar.** En su objetivo, en cada paso de juego quita `Ritmodevora` escalones de ocupación (`Ritmogrande` en forma grande) con `_undo_note()`, en el orden de la erosión: primero los satélites, luego la altura (y, de paso, las inclusiones que quedan por encima, fase 26). No pasa por `erosion()`: no cuenta en el balance de la fase 23. Cada escalón suma 1 a `acum`.
- **Crecer.** `tam = Tamanoinicial + (1 − Tamanoinicial) × min(1, acum / Ocupacionmax)`. En 1, forma grande: más rápido, devora a `Ritmogrande` y puede con fusiones y coronas.
- **Brote del mal.** La celda que llega a `occ = 0` se vacía y recibe un brote: `occ = 1`, `sp = MAL`. El monstruo busca otro objetivo.
- **El mal crece.** Un brote que recibe notas crece con las reglas de siempre (carga, ocupación, desborde, fusión, corona); la presencia del público encima sube la probabilidad de que prendan, como en cualquier celda (fase 22). No hibrida: una nota del otro secuenciador no lo vuelve híbrido. **Desborde del mal (D4):** en una vecina vacía, un satélite del mal; en otra del mal, crece o la presiona; sobre una del público, se pierde (ni hibrida ni la carga).
- **Muerte.** Ahogado (fase 34); `Esperamonstruo` s después aparece otro con las mismas reglas.

### Lo visual (provisional)

- `monstruo`: un cuerpo y dos ojos (esferas) escalados por `tam`, en su propio COMP instanciado, que gira con el planeta. La idea es un personaje tipo arcade de 8 bits: basta con cambiar la esfera de `monstruo` por un sprite; la lógica no se toca.
- `tocon`: con `Verobjetivo`, un tocón en la celda objetivo (D6), para que el público ponga zanjas y cebos en el camino.
- `brotes_mal`: un velo en cada celda del mal (más pequeño en sus satélites). La geometría del brote sigue siendo la de su especie de origen (la de la celda devorada: ver «Diferencias con el encargo»); encima va el velo con la familia de material nueva **mal** (`mat_piel_mal`, familia 9 de `piel_pixel`): casi negra, de croma baja y con un brillo propio débil que late despacio, lejos de los tonos reservados (cian 165°–235°, ámbar 55°–100°, verdes 120°–165°, azul 235°–275°) y de la paleta humana. Los ojos del monstruo emiten; el tocón es mate.

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `monstruo`, `i_monstruo` | Geometry COMP instanciado (esfera): cuerpo y ojos, con `mat_piel_mal` |
| `tocon`, `i_tocon` | Geometry COMP instanciado (caja): la marca del objetivo, con `mat_piel_mal` |
| `brotes_mal`, `i_brotes_mal` | Geometry COMP instanciado (esfera): el velo de cada celda del mal, con `mat_piel_mal` |
| `mat_piel_mal` | GLSL MAT de la piel, familia 9 (lo crea `materiales_piel`, comun v82) |

El alfa de cada instancia lleva rugosidad + 2 × parte (0 velo, 1 cuerpo, 2 ojos, 3 tocón).

### Parámetros (página Fase33)

`Umbralaparicion` 0,25 · `Tamanoinicial` 0,5 · `Ocupacionmax` 8 · `Ritmodevora` 2 · `Ritmogrande` 3 · `Pasomonstruo` 24 · `Pasogrande` 12 (fase 33 v4; antes 16 y 8) · `Costezanja` 2 · `Recalculo` 4 · `Esperamonstruo` 8 s · `Verobjetivo` encendido · `Simmonstruo` (pulso: aparece ya) · `Simceldamon` 0

### Leyenda

```
MONSTRUO #3  devora  celda 40 -> 52  tam 0.62  acum 5/8  x2
MONSTRUO #3  devora  celda 52 -> 52  tam 1.00  acum 8/8  x3   GRANDE
MONSTRUO #2  espera   cara visible 18% (aparece al 25%)
MONSTRUO #2  muere   reaparece en 5.5 s
```

### Prueba manual

`Modojuego`. `Sembrar` hasta corona en una celda y hasta 3 en otra; `Simceldamon` cerca de las dos y `Simmonstruo`: el pequeño va a la de 3 (el tocón lo marca), no a la corona. La devora a 2 escalones por negra, deja un brote y crece. Sembrar la celda del brote: crece como mal. Dejar que devore 8 escalones: forma grande, más rápido, 3 por negra, y va a por la corona.

### Autoprueba

- El objetivo es el de mayor `occ / (1 + coste)` (6 a dos celdas antes que 3 al lado), el pequeño nunca elige fusión ni corona y el grande sí.
- Devora 2 escalones por paso de juego sin ningún trigger: primero el satélite, luego la altura. Celda vaciada → brote con `occ = 1` y `sp = MAL`. El balance de la fase 23 no cambia.
- El brote crece con notas simuladas de los dos secuenciadores y sigue siendo del mal.
- El desborde del mal no entra en una celda del público; en una vacía deja un satélite del mal.
- `tam` crece con `acum` y llega a 1 en `Ocupacionmax`; en forma grande devora 3 por paso y avanza cada `Pasogrande`.
- Una celda cada `Pasomonstruo` semicorcheas; la aparición al llegar `Umbralaparicion`, por el borde de entrada; `Simmonstruo`.
- Dos ejecuciones con la misma sesión simulada dan el mismo resultado (determinismo).
- Las geometrías, `Verobjetivo`, la línea `MONSTRUO` y la familia 9 del shader.

---

## FASE 34 · Zanjas y agua

```python
exec(open('C:/Users/DareDave/Downloads/est/fase34_zanjas.py').read())
```

### Qué hace

- **Zanja.** En modo juego, una fila parada `Tfila` (fase 29) corta en **todas** las celdas que miran a sus casillas, no solo en la de origen. La escisión de la fase 29 se sigue abriendo en el origen (con su fulgurita, su relámpago, su testigo y su registro) y las demás celdas se cortan igual: profundidad personas × `Conchasporpersona`, con el núcleo como tope; quita losetas, vacía la celda, borra sus inclusiones, no enciende cicatriz cian y la concha siguiente la tapiza (sin `Colmatacion`). Se apunta en `W['juego']['zanjas']`.
- **Parada.** La fila tiene que estar parada `Tfila` para cavar: si alguien se mueve antes, el tiempo vuelve a empezar. Si llega gente a la fila mientras sigue parada, sus celdas se añaden y todas bajan a la profundidad nueva.
- **La celda de cada casilla queda fija** desde que empieza a cavar, como el origen de la escisión. El planeta gira (con `Barsperturn` 8, una vuelta cada 16 s a 120 BPM: unos 22° por segundo) y bajo una persona quieta pasan celdas: sin esto, una fila quieta iría arando una franja.
- **Fijada.** Cuando alguien de la fila se mueve (la fila pierde una casilla) o la fila se deshace, la zanja queda fijada y todas sus celdas entran en `W['bloqueadas']`: ninguna fila vuelve a cavarlas ni a profundizarlas hasta el ciclo siguiente. Una fila que pasa por ellas solo cava en sus celdas libres (también para el origen de su escisión), y para cavar otra vez tiene que volver a estar parada `Tfila`.
- **Caída.** Si la celda del monstruo pasa a ser zanja, o entra en una, cae: `estado = 'cae'` (hasta el paso de juego siguiente), `acum = 0`, `tam = Tamanoinicial`, forma pequeña. Sigue buscando desde el fondo: entrar en una zanja o salir de ella le cuesta `Costezanja` veces más. De zanja a zanja solo cae otra vez con `acum > 0`.
- **Agua.** Una zanja de `Profundidadagua` conchas o más aflora agua; una vecina de un río o un lago de la fase 13 (en la naturaleza) también se llena. Capacidad: profundidad × `Ocupacionmax` escalones. En cada paso de juego, `+ Ritmoagua` en las que afloran o tocan agua dulce y `+ Desbordeagua` hacia cada zanja vecina con menos agua, sin pasar de su capacidad (el código del encargo, tal cual). El agua es muro en el Dijkstra (no entra a propósito). Si la celda del monstruo llega a `Ahoga` de su zanja llena, muere.
- **Entierro.** Al enterrar en modo juego, las zanjas, el agua y las bloqueadas quedan en el mundo enterrado: la concha nueva las tapiza (el hueco sigue, como el de una escisión) y la ronda siguiente empieza sin zanjas de juego.
- **Exclusiones.** En modo juego el agua de juego entra en las escisiones. Fuera del modo juego, ríos y lagos siguen sin entrar en ellas (fases 13 y 29).

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `agua_juego`, `i_agua_juego` | Geometry COMP instanciado: el agua de cada zanja hasta su nivel, con `mat_piel_agua` (la familia agua de la fase 13) |

### Parámetros (página Fase34)

`Zanjajuego` encendido · `Profundidadagua` 4 conchas · `Ritmoagua` 4 · `Desbordeagua` 2 · `Ahoga` 0,5 · `Simzanja` (pulso: zanja de `Simfila` celdas desde `Simcasilla`, sin esperar a `Tfila`, fijada en el acto)

### Leyenda

```
ZANJA    3 celdas   prof 4   agua 60%   monstruo dentro
```

### Prueba manual

Con varias conchas (`Forzarciclo` unas cuantas veces), `Modojuego`, `Simmonstruo` y una fila de 3 (`Simfila` 3, `Simformarfila`) en la celda donde está devorando: cae y vuelve a media celda (una fila de 3 atrapa). Con 4 personas (profundidad 4) la zanja aflora agua, se llena y el monstruo muere (una fila de 4 ahoga, D7); a los `Esperamonstruo` s aparece otro. `Simzanja` hace la zanja sin esperar.

### Autoprueba

- La fila corta en todas sus celdas en modo juego (3 conchas cada una, con la escisión en el origen) y solo en el origen fuera de él.
- Una fila que se mueve antes de `Tfila` no cava. Al moverse alguien la zanja queda fijada; una fila nueva de 5 que la cruza solo cava (a 5 conchas) en sus celdas libres; `Forzarciclo` las libera.
- Caída: `acum = 0`, `tam = Tamanoinicial`; de zanja a zanja solo con `acum > 0`; entrar en una zanja cuesta `Costezanja` en el Dijkstra.
- Agua: aflora a 4 por paso con profundidad ≥ 4, desborda a 2 hacia la vecina más baja, una de 3 no aflora, nunca pasa de la capacidad; una zanja de 1 concha vecina de un río (`Pruebario`) también se llena.
- El monstruo muere con el agua por encima de `Ahoga` (16 de 32 a los 4 pasos) y reaparece tras `Esperamonstruo`.
- Fuera del modo juego, ni agua de juego ni lagos en las escisiones. `Simzanja`, `agua_juego` y la línea `ZANJA`.

---

## FASE 35 · Rescatar brotes

```python
exec(open('C:/Users/DareDave/Downloads/est/fase35_rescate.py').read())
```

### Qué hace

- **Condición.** Una persona en la celda del mal (la que mira su casilla) y `Aliados` personas o más en sus celdas vecinas (`vecinas6`; pueden compartir celda), todas sostenidas `Taliados` s sobre la ocupación binaria de la fase 24. Se mira en cada imagen de la cámara. Las casillas de esas personas quedan fijas al empezar el rescate y lo que se sostiene es su ocupación: con el planeta girando, la celda que mira cada casilla cambia en un segundo o dos, y sin esto el rescate casi nunca llegaría a 3 s.
- **Efecto.** La celda pasa a la especie de `W['juego']['ultimoseq'][celda]`, el último secuenciador que la tocó (geología o arquitectura; si ninguno, geología). Conserva `occ` y `carga`, `own` pasa a la nueva especie y sigue con las reglas y el ritmo de construcción de siempre. Sus satélites del mal pasan con ella. El monstruo puede volver a elegirla.
- **Mientras tanto.** Hasta completarse, la persona de encima alimenta el mal con las reglas normales (fase 22). Si alguien se va antes de `Taliados`, el rescate empieza de cero.
- **`ultimoseq`.** Se apunta en cada nota del SEQ1 (`geo`) o del SEQ2 (`arq`) que prende en una celda.

### Parámetros (página Fase35)

`Aliados` 3 · `Taliados` 3 s · `Simrescate` (pulso: una persona en la casilla de `Simcasilla` y `Aliados` en casillas que miran a vecinas de su celda, en la tabla `sala_personas`)

### Leyenda

```
RESCATE  celda 33   aliados 3/3   2.1/3.0 s
RESCATE  -   (rescatados 2)
```

### Prueba manual

`Modojuego`; un brote crecido a 3 en la celda que mira `Simcasilla` (déjalo crecer con `Sembrar` en su nota); `Simrescate`: a los 3 s la celda es del público con ocupación 3 y la especie del último secuenciador. Quitar un aliado (`Simquitar` en su casilla) a los 2 s: no hay rescate y el contador vuelve a cero.

### Autoprueba

- Rescate con 1 + 3 durante `Taliados`; con un aliado menos, o un instante menos, nada.
- La especie es la de `ultimoseq` (o geología); `occ` y `carga` se conservan; si alguien se va, vuelve a cero.
- Tras el rescate crece con las reglas de siempre y el monstruo puede volver a elegirla. `ultimoseq` nota a nota. `Simrescate`.

---

## FASE 36 · Luz de juego

```python
exec(open('C:/Users/DareDave/Downloads/est/fase36_luzjuego.py').read())
```

### Qué hace

En modo juego (con `Luzjuego`), la luz de sala de la fase 23 cuenta la partida:

- **Baño.** Sigue la parte del mal en el globo, con el recuento de la fase 32: `mal / (publico + mal)`, del ámbar (el público) al frío (el mal), con intensidad 0,08 + 0,62 × la parte. Sustituye al balance mientras dura la partida; el colapso no entra en modo juego.
- **Estroboscopio.** Mientras el monstruo está en forma grande, a `Maxhz`.
- **Muerte del monstruo.** Un destello: el relámpago de la fase 30, con prioridad (y un pulso del baño).
- **Seguridad.** Todo pasa por el limitador común de destellos de la fase 23: 3 por segundo como mucho.
- **Fin de ronda.** La noche de la fase 28 al enterrar.

Sin interfaz DMX, los eventos quedan en el motor y en la leyenda. Con la partida en espera, vuelve la luz de la fase 23.

### Parámetros (página Fase36)

`Luzjuego` encendido

### Leyenda

```
LUZJUEGO bano 0.28   estrobo no   destellos 1/s
```

### Prueba manual y autoprueba

Con `Simbalance` apagado (−1): subir el mal sube el baño y lo enfría; con el monstruo grande entra el estroboscopio (nunca más de 3 destellos por segundo); el monstruo ahogado da un relámpago; al acabar la ronda, la noche. `Luzjuego` apagado: la luz de la fase 23.

---

## FASE 37 · Armas opcionales

```python
exec(open('C:/Users/DareDave/Downloads/est/fase37_armas.py').read())
```

Cada arma tiene su interruptor y empieza **apagada**, para probar primero el juego base. La zanja trampa y el cebo no necesitan fase: salen de las fases 33 y 34 (una zanja en el camino del tocón; una construcción próspera que lo atraiga).

| Arma | Interruptor | Cuándo | Efecto | Parámetros |
|---|---|---|---|---|
| Cerco | `Armacerco` | Las celdas con una persona quieta `Tparada` (fase 25) son muro en el Dijkstra. Sin objetivo alcanzable (pero con alguno al otro lado), acorralado | Acorralado no devora y pierde `Hambre` escalones de `acum` por compás | `Hambre` 1 |
| Pisotón | `Armapison` | `Npison` personas o más en casillas que miran a la celda del monstruo | Mientras aguantan, no devora y `tam` baja `Encoge` por paso (hasta 0,1; `acum` baja con él) | `Npison` 3, `Encoge` 0,05 |
| Estatuas | `Armaestatuas` | Al menos una persona, todas quietas (las mismas casillas ocupadas) y el flujo del micrófono por debajo de `Umbralsilencio`, durante `Tquietud` | Petrificado `Tpiedra` s: ni se mueve ni devora. El ruido de sala (la energía de la ventana de la fase 21), al revés, multiplica su velocidad hasta ×2 (en `Umbralcorte`) | `Tquietud` 4 s, `Umbralsilencio` 0,3, `Tpiedra` 6 s |
| Grito | `Armagrito` | El ruido sostenido por encima de `Umbralcorte` durante `Ventanaruido`: el corte del ruido de sala de la fase 21 | Una zanja de 1 celda en la celda del monstruo, de `Profgrito` conchas más (fijada): cae. Recarga `Recargagrito` s | `Profgrito` 2, `Recargagrito` 30 s |
| Relámpago | `Armarelampago` | Una fila (o `Simzanja`) abre su zanja a una celda o menos del monstruo | Aturdido `Taturdido` s: ni se mueve ni devora | `Taturdido` 4 s |

### Leyenda

```
ARMAS    cerco on   pison 2/3   estatuas 1.2/4.0 s   grito listo   relampago off
```

### Prueba y autoprueba

Una por arma con su interruptor encendido y las demás apagadas; con todas apagadas, el juego da el mismo resultado que tras la fase 36 (la misma partida en el nivel 36 y en el 37).

---

## Pruebas fuera de TouchDesigner

`pruebas/correr_fases.py` corre las fases 32 a 37 con las demás y, tras la sesión de siempre, una **partida simulada** por el camino real (fotogramas, MIDI del SEQ1 y la tabla `sala_personas` de la sala simulada): dos rondas de 60 s; en cada una, `Simmonstruo`, una fila de 3 en la celda donde devora (cae), otra de 4 en otra celda (se llena de agua y se ahoga), un rescate de un brote y notas del SEQ1 en otro brote (crece). Al final comprueba el resultado de las dos rondas, las caídas, los ahogados, el rescate, el brote que crece y que las dos conchas enterradas guardan `sp = MAL` en tantas celdas como contó el recuento del mal. La partida usa `Tfila` 1 s (y lo devuelve), para que la fila cave mientras el monstruo sigue en su celda. `td_simulado.py` no necesitó operadores nuevos.

---

## Diferencias con el encargo

- **Numeración del motor.** El encargo pedía `motor v66` a `v71`, pero el motor ya iba por la v105: las fases 32 a 37 son las **v106 a v111** (una por fase en la cabecera del motor), y `comun` pasa a la v82.
- **`own` del brote.** El encargo dice `sp = own = 'mal'`. Aquí `sp = MAL` marca el mal (es lo que cuentan el recuento, la herencia, el desborde, el rescate y la concha) y `own` conserva la especie de la celda devorada. Así el brote usa la geometría de su especie de origen, como pide el apartado visual, sin tocar las decenas de sitios de la piel que eligen la geometría por `own`. Al rescatar, `own` sí pasa a la especie nueva.
- **Familia `mal`.** Cada modelo tiene una sola geometría (y un solo material) para todas sus celdas, así que la familia nueva no puede ir en la geometría del brote: va en un velo propio (`brotes_mal`, familia 9 de `piel_pixel`). Cuando llegue la imaginería, se sustituye ese velo.
- **`W['bloqueadas']` y el «fix de la fase 29».** El fix «prueba de sala en línea» (derribo en línea) que cita el encargo no está en el repositorio. `W['bloqueadas']` lo crea la fase 34 (solo en modo juego, se vacía al enterrar y al apagar el modo), y el recorrido de celdas de la fila es el de `celda_de_casilla` de cada casilla.
- **La escisión en modo juego.** También espera a que la fila esté parada `Tfila` (no solo a que exista), y su origen es la casilla más antigua cuya celda no está bloqueada. `Tfila` sigue en 5 s (fase 29; el encargo habla de 4).
- **Profundidad de una zanja.** Las losetas que se quitan de verdad (el núcleo es el tope). Una celda sin losetas no llega a ser zanja.
- **Coste del movimiento.** El Dijkstra cuesta `Costezanja` al entrar en una zanja (el código del encargo). Moverse cuesta `Costezanja` veces más al entrar en una zanja **o al salir de su fondo**: «sigue buscando desde el fondo». Con los valores por defecto el monstruo tarda 32 semicorcheas en salir y el agua lo ahoga en 16: una fila de 4 ahoga, una de 3 atrapa (D7).
- **Zanjas y entierro.** Las zanjas y el agua de juego son del mundo en curso: al enterrar, la concha nueva las tapiza (el hueco se queda, como el de una escisión) y la ronda siguiente empieza sin zanjas. Apagar `Modojuego` las olvida (el hueco ya es geología) y vacía las celdas del mal.
- **Solo entierra la ronda.** En modo juego el ciclo de la fase 6 y el colapso no cierran el mundo; si no, una ronda de 6 minutos se enterraría sola a los 16–64 compases.
- **El público sobre el mal.** El encargo fija el desborde del mal sobre el público (se pierde). El desborde del público sobre una celda del mal no está fijado: hace lo de siempre (presión), así que construir pegado a un brote lo alimenta.
- **El giro.** El encargo piensa en «la celda que mira cada persona» como si fuera fija; el planeta gira unos 22° por segundo (`Barsperturn` 8). La zanja fija la celda de cada casilla al empezar a cavar y el rescate fija sus casillas al empezar (la ocupación binaria es por casilla). El pisotón, el cerco y la marca miran la celda de cada instante. Lo descubrió la partida simulada.
- **`ultimoseq`.** Se apunta con las notas que prenden (las que no prenden, fase 22, no tocan la celda).
- **`Umbralsilencio`.** Sin valor en el encargo («se fija en sala»): 0,3 de flujo espectral del micrófono (la mitad de `Umbralonset`).

## Qué ajustar en sala

- **`Duracionronda` y `Rondas`**: 360 s y 4 (D5). Para enseñar el juego, 120 s y 2.
- **`Umbralaparicion`**: con poca gente el 25 % de la cara visible tarda en llenarse; bájalo si el monstruo no llega, o usa `Simmonstruo`.
- **`Pasomonstruo` / `Pasogrande`**: desde la fase 33 v4 (motor v120) GENoZilla anda un tercio más lento: el pequeño da un paso cada compás y medio (24 semicorcheas; antes 16) y el grande cada 12 (antes 8). Un proyecto con los valores de antes pasa a los nuevos una sola vez; el tope sube a 128. Si la sala no llega a cortarle el camino, súbelo.
- **`Tfila`** (fase 29) y **`Conchasporpersona`**: deciden lo rápido que se cava y lo honda que queda la zanja; con pocas conchas en el planeta (al empezar la jornada) las zanjas salen poco hondas. Entierra unas cuantas conchas antes de abrir la partida.
- **`Profundidadagua`** y **`Ahoga`**: una fila de 4 ahoga con 4 conchas por debajo; si el público no consigue reunir a 4, prueba 3.
- **`Aliados`** y **`Taliados`**: cuatro personas tres segundos. Con la cámara real, mira la línea `RESCATE` para ver si las celdas vecinas caen en las casillas que esperas (las celdas son más anchas que las casillas).
- **Armas**: una a una, empezando por el cerco y el pisotón (no necesitan micrófono). `Umbralsilencio` con la sala en silencio real: mira el flujo del micrófono en la línea `MICRO` (fase 21).
- **Rendimiento**: el juego entero cuesta menos de 1 ms por fotograma en Python (el Dijkstra es de 85 celdas y se hace cada 4 pasos de juego); mídelo con el diagnóstico de la fase 18 (`pruebas/diagnostico_fps.py`).
