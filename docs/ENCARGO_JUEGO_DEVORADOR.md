# Encargo · Juego «El devorador» (fases 32 a 37)

*14 de noviembre de 2026. Encargo para Claude Code. Diseño de origen: «Stratos · Juegos de sala» (https://claude.ai/artifact/Kcc5FSPEn9p9UJYn6dXHUt), apartados 5 a 9.*

Turf War de toda la sala contra un monstruo. El público construye quedándose quieto; el monstruo aparece en el planeta, va de una construcción próspera a otra devorándola y deja brotes del mal. Al acabar la ronda se compara el territorio del público con el del mal.

**No toca el núcleo.** El juego es un modo que se enciende encima del mundo: lee y escribe `W` con las funciones que ya existen y todo lo nuevo se activa con `Modojuego`. Con `Modojuego` apagado, el sistema se comporta exactamente como antes. La imaginería está por definir: lo visual de este encargo es provisional y debe poder cambiarse sin tocar la lógica.

---

## 0. Antes de empezar

**Dependencias.** El juego necesita la cámara y la probabilidad por casilla (fase 22), las personas y la sala simulada (fase 24), la parada (fase 25) y la fila (fase 29, con el fix «prueba de sala en línea»). La luz necesita la fase 23. Los ríos y lagos son de la fase 13, ya en `main`.

**Numeración.** El juego va después del plan v5 (D1, confirmada): fases **32 a 37**, `motor v66` en adelante (una versión por fase).

**Convenciones**, las de siempre: un script `faseNN_<nombre>.py` que carga `estratos_comun.py`, dice su versión en la primera línea, se niega a correr sin la fase anterior (`require_base`), sube `Nivel`, crea su página `FaseNN` en `/project1/FASE1`, añade su línea a la leyenda, escribe su `LEEME` y termina con la autoprueba (`AUTOPRUEBA OK` o qué falla), que deja el mundo como estaba. La lógica va al motor y se activa por `Nivel`. Sin `random`: los sorteos y desempates usan el mapa logístico (`logistica`, `semilla_caos`) o `_hash01`. TouchDesigner sigue sin enviar nada al BeatStep. Presupuesto: menos de 1 ms por fotograma en Python para todo el juego.

**Unidad de ritmo.** Todos los ritmos del juego (devorar, agua) se cuentan en **escalones de ocupación por paso de juego**. Un paso de juego son `Pasojuego` semicorcheas de `master_beat` (por defecto 4, una negra). No dependen de los triggers de los secuenciadores ni de la batería.

---

## 1. Estado del juego en `W`

```python
W['juego'] = dict(
    activo=False, ronda=1, rondas=4, t0=0.0,          # ronda en curso y su inicio
    paso=0,                                           # pasos de juego desde el inicio de la ronda
    mon=dict(
        estado='espera',        # espera | aparece | busca | devora | cae | muere
        celda=None,             # celda actual (indice 0..N-1)
        tam=0.5,                # 0.5 = media celda, 1.0 = celda entera
        acum=0,                 # escalones devorados desde la ultima caida
        objetivo=None,          # celda objetivo
        camino=[],              # celdas hasta el objetivo
        mov=0.0,                # avance acumulado hacia la siguiente celda
        t_muerte=None,          # instante de la muerte, para la reaparicion
        n=0,                    # monstruos aparecidos en la ronda
    ),
    zanjas={},                  # celda -> profundidad en conchas
    agua={},                    # celda -> nivel de agua en escalones
    rescates={},                # celda -> instante en que empezo el rescate
    ultimoseq={},               # celda -> 'geo' | 'arq': ultimo secuenciador que la toco
    recuento=dict(publico=0, mal=0),
)
```

La especie nueva es `sp = 'mal'`, junto a geología, arquitectura e híbrido.

---

## 2. Fase 32 · Modo de juego y ronda

**Qué hace.** Crea la página `Juego`, enciende y apaga el modo, lleva la ronda y el recuento, y pone la marca de cada jugador.

- **Modo.** `Modojuego` encendido activa `W['juego']`; apagado lo vacía y quita monstruo, brotes del mal, zanjas de juego y agua de juego sin tocar el resto del mundo.
- **Ronda.** Dura `Duracionronda` segundos. Al acabar: recuento, entierro forzado con `end_cycle` (el mismo camino que `Forzarciclo`), noche de la fase 28 si está y ronda siguiente. Tras `Rondas` rondas, el modo se queda en espera con el resultado en la leyenda.
- **Recuento.** Sobre **todas las celdas del globo**, en la cara visible y fuera de ella. Público = celdas con `occ > 0` y `sp != 'mal'`; mal = celdas con `occ > 0` y `sp == 'mal'`. Gana el mayor; en empate gana el público.
- **Herencia del mal.** Al enterrar en modo juego, la ocupación del mal no se hereda (`Herenciamal` 0). La concha guarda `sp = 'mal'` en sus celdas como hasta ahora guarda cualquier especie.
- **Marca de jugador.** Un anillo en la celda que mira cada persona de la tabla `personas` (fase 24), para que se encuentre en el globo. Un solo color para toda la sala, de la paleta humana.

**Parámetros (página Fase32).** `Modojuego` · `Duracionronda` 360 s · `Rondas` 4 · `Pasojuego` 4 · `Herenciamal` 0 · `Marcajugador` encendido · `Nuevapartida` (pulso).

**Leyenda.** `JUEGO    ronda 2/4   4:12   publico 38   mal 14   (globo)`

**Prueba manual.** `Modojuego` y `Duracionronda` 20: a los 20 s se entierra el mundo y la ronda pasa a 2. `Simponer` en una casilla: aparece el anillo en la celda que mira. Apagar `Modojuego` a mitad de ronda: el mundo sigue como estaba.

**Autoprueba.**
- Con `Modojuego` apagado, una sesión simulada da el mismo `W` que sin la fase.
- El recuento cuenta todas las celdas del globo, también las que están fuera de la cara visible, y cuenta bien con un mundo preparado a mano.
- Fin de ronda: entierro, ronda + 1, recuento a cero; tras `Rondas`, espera.

---

## 3. Fase 33 · El monstruo y los brotes del mal

**Qué hace.** El monstruo aparece, busca, devora, crece, deja brotes del mal y reaparece. Los brotes crecen con los triggers como cualquier celda.

**Aparición.** Cuando la fracción de celdas de la cara visible con `occ > 0` y `sp != 'mal'` llega a `Umbralaparicion`, el monstruo aparece en la celda vacía de la cara visible más cercana al borde por el que entran las celdas con el giro. Desempate con `_hash01`. Tamaño `Tamanoinicial`.

**Objetivo.** Cada `Recalculo` pasos de juego, y siempre que vacía una celda:

```python
def objetivo(W, m, cfg):
    coste = dijkstra(m['celda'], vecinas6,
                     peso=lambda c: cfg.Costezanja if c in W['juego']['zanjas'] else 1,
                     muro=lambda c: c in W['juego']['agua'])   # no entra en el agua a proposito
    def comestible(c):
        if occ(W, c) == 0 or sp(W, c) == 'mal':
            return False
        if m['tam'] < 1.0 and (es_fusion(W, c) or es_corona(W, c)):
            return False                                      # el pequeno no puede con ellas
        return True
    cand = [c for c in coste if comestible(c)]
    if not cand:
        return None
    return max(cand, key=lambda c: (occ(W, c) / (1 + coste[c]), _hash01(c)))
```

`vecinas6` es la vecindad de la fase 4. `es_fusion` y `es_corona` usan los umbrales de estado de la fase 4 (fusión desde 6, corona desde 8, o los que tenga la página `Fase4`).

**Movimiento.** Avanza una celda por el camino cada `Pasomonstruo` semicorcheas (`Pasogrande` en forma grande). Entrar en una celda de zanja cuesta `Costezanja` veces más. Sin objetivo, se queda quieto.

**Devorar.** Al llegar a su objetivo, en cada paso de juego quita `Ritmodevora` escalones (`Ritmogrande` en forma grande) con `_undo_note()`, de modo que cae primero lo último construido (coronas, satélites, altura), como en la erosión. Cada escalón quitado suma 1 a `acum`. No pasa por `erosion()`: no cuenta en el balance de la fase 23.

**Crecimiento.** `tam = Tamanoinicial + (1 − Tamanoinicial) × min(1, acum / Ocupacionmax)`. Al llegar a 1 pasa a forma grande: más rápido, devora a `Ritmogrande` y ya puede con fusiones y coronas.

**Brote del mal.** Cuando una celda que devora llega a `occ = 0`, se vacía con `_clear_cell()` y recibe un brote: `occ = 1`, `sp = own = 'mal'`. El monstruo busca otro objetivo.

**El mal crece.** Una celda del mal que recibe triggers de un secuenciador crece con las reglas de siempre: carga, ocupación, desborde, fusión y corona. La presencia del público encima sube la probabilidad de que prendan las notas, como en cualquier celda (fase 22). **Desborde del mal:** cae en vecinas vacías o del mal; sobre una celda del público se pierde, sin hibridar (D4).

**Muerte y reaparición.** Muere ahogado (fase 34). `Esperamonstruo` segundos después aparece otro con las mismas reglas.

**Visual provisional.** El monstruo es una instancia propia escalada por `tam`, que sigue el giro del planeta como las formaciones. Los brotes del mal usan la geometría de su especie de origen con una familia de material nueva (`mal`) en `piel_pixel`: casi negra, croma baja y brillo propio débil, para no chocar con los tonos reservados (cian 165°–235°, ámbar 55°–100°, verdes 120°–165°, azul 235°–275°) ni con la paleta humana. Todo se sustituye cuando se defina la imaginería; para el monstruo, la idea es un personaje tipo arcade de 8 bits. Por eso la geometría del monstruo va en un COMP propio que se pueda cambiar por un sprite sin tocar la lógica.

**Parámetros (página Fase33).** `Umbralaparicion` 0,25 · `Tamanoinicial` 0,5 · `Ocupacionmax` 8 · `Ritmodevora` 2 · `Ritmogrande` 3 · `Pasomonstruo` 16 · `Pasogrande` 8 · `Costezanja` 2 · `Recalculo` 4 · `Esperamonstruo` 8 s · `Verobjetivo` encendido · `Simmonstruo` (pulso: aparece ya) · `Simceldamon` (celda donde aparece con `Simmonstruo`).

**Ver el objetivo.** Con `Verobjetivo`, la celda objetivo lleva un **tocón** como marca provisional, para que el público pueda poner zanjas y cebos en el camino (D6). Es una instancia propia, fácil de sustituir cuando llegue la imaginería.

**Leyenda.** `MONSTRUO #3  devora  celda 40 -> 52  tam 0.62  acum 5/8  x2`

**Prueba manual.** `Sembrar` hasta corona en una celda y hasta 3 en otra; `Simmonstruo`: el pequeño va a la de 3, no a la corona. La devora a 2 escalones por negra, deja un brote y crece. Sembrar la celda del brote: crece como mal. Dejar que devore 8 escalones: pasa a forma grande, más rápido, devora a 3 por negra y va a por la corona.

**Autoprueba.**
- El objetivo es el de mayor `occ / (1 + coste)` y el pequeño nunca elige fusión ni corona.
- Devorar quita `Ritmodevora` escalones por paso de juego sin ningún trigger, en orden inverso a la construcción.
- Celda vaciada → brote con `occ = 1` y `sp = 'mal'`; el brote crece con triggers simulados.
- `tam` crece con `acum` y llega a 1 en `Ocupacionmax`; en forma grande, velocidad y ritmo cambian.
- El desborde del mal no entra en celdas del público.
- El balance de la fase 23 no cambia por devorar.
- Dos ejecuciones con la misma sesión simulada dan el mismo resultado (determinismo).

---

## 4. Fase 34 · Zanjas y agua

**Qué hace.** En modo juego, la fila de la fase 29 cava una zanja en todas sus celdas; el monstruo cae en ellas y el agua lo ahoga.

**Zanja.** Cuando una fila abre su escisión (fase 29), en modo juego corta en **todas** las celdas que miran a sus casillas, no solo en la de origen. Profundidad de cada celda: personas × `Conchasporpersona`, con el núcleo como tope, como la escisión. Cada celda de zanja se trata como la escisión: quita losetas, vacía la celda, borra sus inclusiones, no enciende cicatriz cian y la concha siguiente la tapiza. Se registra en `W['juego']['zanjas']`. La fila tiene que estar parada `Tfila` (4 s) para cavar. Si llega gente a la fila mientras sigue parada, las celdas nuevas se añaden a la zanja. Cuando alguien de la fila se mueve, la zanja queda fijada y todas sus celdas entran en `W['bloqueadas']` (fase 29): ninguna fila vuelve a cavarlas ni a profundizarlas hasta el ciclo siguiente; una fila que pasa por ellas solo cava en sus celdas libres. Se apoya en el recorrido de celdas del fix de la fase 29 (derribo en línea).

**Caída.** Si la celda del monstruo pasa a ser zanja, o el monstruo entra en una, cae: `estado = 'cae'`, `acum = 0`, `tam = Tamanoinicial`, forma pequeña. Sigue buscando desde el fondo; cada paso entre zanjas le cuesta `Costezanja`. Cae otra vez solo si tiene `acum > 0`.

**Agua.** Una celda de zanja con profundidad ≥ `Profundidadagua` aflora agua; una que es vecina de un río o un lago de la fase 13 también se llena. Capacidad de una celda: profundidad × `Ocupacionmax` escalones. En cada paso de juego:

```python
def inundar(W, cfg):
    J = W['juego']
    for c, prof in J['zanjas'].items():
        cap = prof * cfg.Ocupacionmax
        if prof >= cfg.Profundidadagua or toca_rio_o_lago(W, c):
            J['agua'][c] = min(cap, J['agua'].get(c, 0) + cfg.Ritmoagua)        # x4: aflora o entra
        for v in vecinas6(c):
            if v in J['zanjas'] and J['agua'].get(c, 0) > J['agua'].get(v, 0):
                capv = J['zanjas'][v] * cfg.Ocupacionmax
                J['agua'][v] = min(capv, J['agua'].get(v, 0) + cfg.Desbordeagua)  # x2: desborde
    m = J['mon']
    if m['celda'] in J['agua'] and J['agua'][m['celda']] >= cfg.Ahoga * J['zanjas'][m['celda']] * cfg.Ocupacionmax:
        morir(W, m)
```

En modo juego se levanta la exclusión de las fases 13 y 29: el agua de juego entra en las escisiones. Fuera del juego todo sigue igual. El agua visible usa la familia `agua` de `piel_pixel` (fase 13).

**Parámetros (página Fase34).** `Zanjajuego` encendido · `Profundidadagua` 4 conchas · `Ritmoagua` 4 · `Desbordeagua` 2 · `Ahoga` 0,5 (fracción de la zanja llena que lo mata) · `Simzanja` (pulso: zanja de `Simfila` celdas desde `Simcasilla` sin esperar a `Tfila`).

**Leyenda.** `ZANJA    3 celdas   prof 4   agua 60%   monstruo dentro`

**Prueba manual.** Con varias conchas, `Simmonstruo` y una fila de 3 (`Simfila` 3, `Simformarfila`) a su paso: cae y vuelve a media celda. Con 4 personas (profundidad 4) la zanja aflora agua, se llena y el monstruo muere; a los `Esperamonstruo` s aparece otro.

**Autoprueba.**
- La fila corta en todas sus celdas en modo juego y solo en el origen fuera de él.
- Una fila que se mueve antes de 4 s no cava; una zanja fijada no se vuelve a cavar hasta `Forzarciclo`, y una fila nueva que la cruza solo cava en las celdas libres.
- Caída: `acum = 0`, `tam = Tamanoinicial`; el camino por zanja cuesta `Costezanja`.
- Agua: aflora con profundidad ≥ `Profundidadagua`, entra desde un río vecino, llena a 4 por paso y desborda a 2 hacia zanjas vecinas más bajas, sin pasar de la capacidad.
- El monstruo muere con el agua por encima de `Ahoga` y reaparece tras `Esperamonstruo`.
- Fuera del modo juego, ríos y lagos siguen sin entrar en las escisiones.

---

## 5. Fase 35 · Rescatar brotes

**Qué hace.** Tres personas coordinadas convierten un brote del mal en una celda del público.

- **Condición.** Una persona en la celda del mal (la que mira su casilla) y `Aliados` personas o más en celdas vecinas (`vecinas6`), todas sostenidas `Taliados` segundos sobre la ocupación binaria de la fase 24. Pueden compartir celda vecina.
- **Efecto.** La celda pasa a la especie de `W['juego']['ultimoseq'][celda]`, el último secuenciador que la tocó (geología o arquitectura; si ninguno, geología). Conserva `occ` y `carga`, y sigue su evolución con las reglas y el ritmo de construcción de siempre. `own` pasa a la nueva especie.
- **Mientras tanto.** Hasta completarse, la persona de encima alimenta el mal con las reglas normales (fase 22). Si alguien se va antes de `Taliados`, el rescate se reinicia.
- **`ultimoseq`.** Se actualiza en cada nota del SEQ1 (`geo`) o del SEQ2 (`arq`) que cae en una celda.

**Parámetros (página Fase35).** `Aliados` 2 · `Taliados` 3 s · `Simrescate` (pulso: pone una persona en la celda de `Simcasilla` y `Aliados` en vecinas).

**Leyenda.** `RESCATE  celda 33   aliados 2/2   2.1/3.0 s`

**Prueba manual.** Un brote crecido a 3; `Simrescate`: a los 3 s la celda es del público con ocupación 3 y la especie del último secuenciador. Quitar un aliado a los 2 s: no hay rescate y el contador vuelve a cero.

**Autoprueba.**
- Rescate con 1 + `Aliados` durante `Taliados`; con un aliado menos o un instante menos, nada.
- La especie es la de `ultimoseq`; `occ` y `carga` se conservan.
- Tras el rescate la celda crece al ritmo normal y el monstruo puede volver a elegirla.

---

## 6. Fase 36 · Luz de juego

**Qué hace.** En modo juego, la luz de sala de la fase 23 cuenta la partida.

- **Baño de luz.** Sigue la parte del mal en el globo, con el mismo recuento de la fase 32: `mal / (publico + mal)`.
- **Estroboscopio.** Entra mientras el monstruo está en forma grande.
- **Muerte del monstruo.** Un destello (relámpago de la fase 30 si existe; si no, un pulso del baño).
- **Seguridad.** Todo pasa por el limitador común de destellos de la fase 23 (3 por segundo como mucho).
- **Fin de ronda.** La noche de la fase 28 al enterrar.

**Parámetros (página Fase36).** `Luzjuego` encendido.

**Leyenda.** `LUZJUEGO baño 0.28   estrobo no   destellos 1/s`

**Prueba manual y autoprueba.** Con `Simbalance` apagado: subir el mal sube el baño; `Simmonstruo` + devorar 8 escalones enciende el estroboscopio; el monstruo ahogado da un destello. Sin interfaz DMX, los eventos quedan en el motor y en la leyenda.

---

## 7. Fase 37 · Armas opcionales

Cada arma tiene su interruptor y empieza **apagada**, para probar primero el juego base. La zanja trampa y el cebo no necesitan fase: salen de las fases 33 y 34.

| Arma | Interruptor | Algoritmo | Efecto | Parámetros |
| --- | --- | --- | --- | --- |
| Cerco | `Armacerco` | Las celdas con una persona quieta (`Tparada`) son muro en el `dijkstra` del objetivo. Si no queda ningún objetivo alcanzable, está acorralado | Acorralado no devora y pierde `Hambre` escalones de `acum` por compás | `Hambre` 1 |
| Pisotón | `Armapison` | `Npison` personas o más en casillas que miran a la celda del monstruo | Mientras aguantan, no devora y `tam` baja `Encoge` por paso | `Npison` 3, `Encoge` 0,05 |
| Estatuas | `Armaestatuas` | Todas las personas quietas y el micrófono por debajo de `Umbralsilencio` durante `Tquietud` | Petrificado `Tpiedra` s. El ruido de sala, al revés, multiplica su velocidad hasta ×2 | `Tquietud` 4 s, `Umbralsilencio`, `Tpiedra` 6 s |
| Grito | `Armagrito` | Ruido sostenido por encima de `Umbralcorte` durante `Ventanaruido` (fase 21) | Abre una zanja de 1 celda en la celda del monstruo, de profundidad `Profgrito`: cae. Recarga `Recargagrito` s | `Profgrito` 2, `Recargagrito` 30 s |
| Relámpago | `Armarelampago` | Una fila abre su zanja a una celda o menos del monstruo | Aturdido `Taturdido` s: ni se mueve ni devora | `Taturdido` 4 s |

**Leyenda.** `ARMAS    cerco on   pison 2/3   estatuas 1.2/4.0 s   grito listo`

**Prueba y autoprueba.** Una por arma con su interruptor encendido y las demás apagadas; con todas apagadas, el juego da el mismo resultado que tras la fase 36.

---

## 8. Decisiones

Todas quedan como parámetro. Las marcadas como confirmadas las ha cerrado Dave; el resto son valores por defecto.

| Nº | Pregunta | Decisión | Estado |
| --- | --- | --- | --- |
| D1 | ¿Juego antes o después del plan v5? | Después: fases 32 a 37 | Confirmada |
| D2 | ¿Cómo aparece el monstruo? | Al pasar `Umbralaparicion` (25 % de la cara visible construida), por el borde de entrada del giro | Por defecto |
| D3 | ¿Qué se cuenta? | Todas las celdas del globo, en la cara visible y fuera de ella | Confirmada |
| D4 | ¿Qué hace el desborde del mal sobre una celda del público? | Se pierde, no hibrida | Confirmada |
| D5 | ¿Cuánto dura la ronda? | 360 s (6 minutos) | Confirmada |
| D6 | ¿Se ve el objetivo del monstruo? | Sí: de momento, un tocón en la celda objetivo (`Verobjetivo`). Más adelante, un monstruo tipo arcade de 8 bits | Confirmada |
| D7 | ¿Profundidad a la que aflora el agua? | 4 conchas: una fila de 3 atrapa, una de 4 ahoga | Por defecto |
| D8 | ¿Ritmos por paso de juego (una negra, `Pasojuego` 4 semicorcheas)? | Monstruo pequeño 2 escalones, grande 3, agua 4 (desborde 2) | Confirmada |
| D9 | ¿Se hereda el mal al enterrar? | No (`Herenciamal` 0) | Confirmada |

Ya decidido por Dave (no tocar): el público alimenta el mal si se para sobre un brote; dos aliados 3 s lo rescatan a la especie del último secuenciador y sigue al ritmo normal; el monstruo pequeño no devora coronas ni fusiones; el agua aflora en zanjas profundas, llena a ×4 y desborda a ×2; el monstruo devora a ×2 pequeño y ×3 grande.

---

## 9. Filas para la hoja `Estratos_parametros`

| Nombre | Etiqueta | Página | Tipo | Defecto | Rango | Qué hace |
| --- | --- | --- | --- | --- | --- | --- |
| `Modojuego` | Modo juego | Fase32 | Interruptor | Apagado | | Enciende el juego encima del mundo |
| `Duracionronda` | Duración de ronda (s) | Fase32 | Decimal | 360 | 20–900 | Segundos por ronda |
| `Rondas` | Rondas | Fase32 | Entero | 4 | 1–12 | Rondas por partida |
| `Pasojuego` | Paso de juego (semicorcheas) | Fase32 | Entero | 4 | 1–16 | Unidad de tiempo de los ritmos del juego |
| `Herenciamal` | Herencia del mal | Fase32 | Decimal | 0 | 0–1 | Fracción del mal que pasa a la concha nueva |
| `Marcajugador` | Marca de jugador | Fase32 | Interruptor | Encendido | | Anillo en la celda de cada persona |
| `Nuevapartida` | Nueva partida | Fase32 | Pulso | | | Ronda 1, recuento a cero |
| `Umbralaparicion` | Umbral de aparición | Fase33 | Decimal | 0,25 | 0–1 | Fracción construida de la cara visible que hace aparecer al monstruo |
| `Tamanoinicial` | Tamaño inicial | Fase33 | Decimal | 0,5 | 0,1–1 | Tamaño al aparecer y tras caer, en celdas |
| `Ocupacionmax` | Ocupación máxima | Fase33 | Entero | 8 | 4–16 | Escalones devorados para llegar a una celda; capacidad de agua por concha |
| `Ritmodevora` | Ritmo de devorar | Fase33 | Entero | 2 | 1–10 | Escalones por paso de juego, pequeño |
| `Ritmogrande` | Ritmo grande | Fase33 | Entero | 3 | 1–10 | Escalones por paso de juego, forma grande |
| `Pasomonstruo` | Paso del monstruo (semicorcheas) | Fase33 | Entero | 16 | 1–64 | Tiempo por celda, pequeño |
| `Pasogrande` | Paso grande (semicorcheas) | Fase33 | Entero | 8 | 1–64 | Tiempo por celda, forma grande |
| `Costezanja` | Coste en zanja | Fase33 | Decimal | 2 | 1–5 | Multiplicador del paso entre zanjas |
| `Recalculo` | Recálculo de objetivo (pasos) | Fase33 | Entero | 4 | 1–32 | Pasos de juego entre recálculos |
| `Esperamonstruo` | Espera de reaparición (s) | Fase33 | Decimal | 8 | 0–120 | Segundos entre una muerte y la aparición siguiente |
| `Verobjetivo` | Ver objetivo | Fase33 | Interruptor | Encendido | | Tocón en la celda objetivo |
| `Simmonstruo` | Simular monstruo | Fase33 | Pulso | | | Hace aparecer el monstruo ya |
| `Simceldamon` | Celda del monstruo simulado | Fase33 | Entero | 0 | 0–N−1 | Dónde aparece con `Simmonstruo` |
| `Zanjajuego` | Zanja de juego | Fase34 | Interruptor | Encendido | | La fila corta en todas sus celdas |
| `Profundidadagua` | Profundidad del agua (conchas) | Fase34 | Entero | 4 | 1–12 | Profundidad a la que aflora agua |
| `Ritmoagua` | Ritmo del agua | Fase34 | Entero | 4 | 1–16 | Escalones por paso al llenar |
| `Desbordeagua` | Desborde del agua | Fase34 | Entero | 2 | 1–16 | Escalones por paso hacia zanjas vecinas |
| `Ahoga` | Nivel que ahoga | Fase34 | Decimal | 0,5 | 0,1–1 | Fracción de zanja llena que mata al monstruo |
| `Simzanja` | Simular zanja | Fase34 | Pulso | | | Zanja de `Simfila` celdas desde `Simcasilla` |
| `Aliados` | Aliados del rescate | Fase35 | Entero | 2 | 1–6 | Personas en vecinas para rescatar un brote |
| `Taliados` | Tiempo del rescate (s) | Fase35 | Decimal | 3 | 0,5–20 | Segundos sostenidos |
| `Simrescate` | Simular rescate | Fase35 | Pulso | | | Persona en la celda y aliados en vecinas |
| `Luzjuego` | Luz de juego | Fase36 | Interruptor | Encendido | | La luz de sala cuenta la partida |
| `Armacerco` · `Armapison` · `Armaestatuas` · `Armagrito` · `Armarelampago` | Armas | Fase37 | Interruptor | Apagado | | Una por arma |
| `Hambre` | Hambre del cerco | Fase37 | Entero | 1 | 0–8 | Escalones de `acum` perdidos por compás acorralado |
| `Npison` | Personas del pisotón | Fase37 | Entero | 3 | 1–10 | Personas sobre la celda del monstruo |
| `Encoge` | Encogimiento | Fase37 | Decimal | 0,05 | 0–0,5 | Tamaño perdido por paso con pisotón |
| `Tquietud` | Tiempo de estatuas (s) | Fase37 | Decimal | 4 | 1–30 | Quietud y silencio sostenidos |
| `Umbralsilencio` | Umbral de silencio | Fase37 | Decimal | | | Nivel de micrófono que cuenta como silencio; se fija en sala |
| `Tpiedra` | Tiempo petrificado (s) | Fase37 | Decimal | 6 | 1–30 | Segundos sin moverse |
| `Profgrito` | Profundidad del grito | Fase37 | Entero | 2 | 1–8 | Conchas que abre el grito |
| `Recargagrito` | Recarga del grito (s) | Fase37 | Decimal | 30 | 5–300 | Segundos entre gritos |
| `Taturdido` | Tiempo aturdido (s) | Fase37 | Decimal | 4 | 1–30 | Segundos sin moverse ni devorar |

`Nº` queda por asignar en la hoja.

---

## 10. Pruebas fuera de TouchDesigner

En `pruebas/correr_fases.py`: añadir las fases 32 a 37 a `FASES`. La sesión simulada gana una partida de dos rondas de 60 s con el monstruo, una fila de 3 que lo atrapa, una de 4 que lo ahoga, un rescate y un brote que crece; al final, el recuento y las dos conchas con `sp = 'mal'` donde toca. `td_simulado.py` no necesita operadores nuevos salvo la geometría del monstruo.

## 11. Entregable

Seis scripts (`fase32_juego.py`, `fase33_monstruo.py`, `fase34_zanjas.py`, `fase35_rescate.py`, `fase36_luzjuego.py`, `fase37_armas.py`), el motor de `v66` a `v71`, `MONTAJE_FASES_32_37.md` (montaje, pruebas manuales y qué ajustar en sala) y las filas del apartado 9 en la hoja `Estratos_parametros`.

Fuera de alcance: las variantes del documento de diseño (oleadas, jefe, dos especies, monstruo guiado, noche, dos bandos, supervivencia, campaña, dos salas) y la imaginería definitiva.
