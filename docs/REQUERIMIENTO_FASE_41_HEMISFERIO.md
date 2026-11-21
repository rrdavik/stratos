# Requerimiento · Fase 41 — Hemisferio: el juego solo en la cara visible

> **Implementado** en `fase41_hemisferio.py` (`fase41 v2`, `motor v137`). **Ojo: la v1 de este requerimiento (planeta quieto, retícula solo en la cara visible, monstruos que nunca salen de ella) se descartó.** Lo que vale es el diseño de `MONTAJE_FASE41.md`: el planeta gira como siempre, las notas caen en una reja fija de la cara visible, la superficie tiene el doble de celdas y los monstruos se paran en la cara oculta. Este documento queda como referencia histórica.

*Para una sesión de Claude Code en la nube sobre el repositorio `rrdavik/stratos`. Es autosuficiente: lee esto entero y después `MONTAJE_FASE40.md` y `ENCARGO_JUEGO_DEVORADOR.md` (fases 32 a 40). Parte de `motor v136` / `fase40 v3`.*

---

## 1. Por qué

Hoy la retícula cubre **toda la esfera** (`ring_layout`, `set_grid`): con do1–do8 hay `N = 85` celdas repartidas por todo el globo, y solo las que miran a la sala (`cara_visible`, las que tienen casilla) se ven. El resto está en la cara oculta.

Los monstruos (Trumpzilla y Godzilla) andan por **todas** las celdas. A veces se quedan en la cara oculta y la partida pierde foco e interés: el público no ve qué pasa, ni qué se devora, ni la lucha.

**Qué se pide.** Una variante en la que **el rango de notas solo toca la cara visible**: las mismas `N` celdas se reparten por el hemisferio que mira a la sala (las celdas de la cara visible se **duplican** en número, o lo que es lo mismo, miden la mitad) y **en la cara oculta no hay celdas**. Los monstruos nunca salen de esa cara y van siempre a donde suenan los secuenciadores.

---

## 2. Qué hay que hacer

### 2.1 Retícula en hemisferio (`Hemisferio`)

Un interruptor nuevo, `Hemisferio` (toggle, **apagado de fábrica**: con él apagado el sistema se comporta exactamente como en `motor v136`, celda por celda).

Con `Hemisferio` encendido:

1. **`N` no cambia.** Sigue siendo `hi - lo + 1`: una celda por nota del rango (polo sur = nota más grave, polo norte = la más aguda, un anillo por octava). El rango de notas, `note_cell` y `fold_note` funcionan igual.
2. **Las celdas se reparten solo en el hemisferio que mira a la sala**, es decir, en la franja de longitud `Loncentral ± Anchoangular/2` (180° de fábrica). Cada anillo completo de 12 notas pasa de 30° por celda a 15°: el doble de celdas en la cara visible, ninguna fuera. Los dos polos quedan en los bordes superior e inferior del disco.
3. **El anillo ya no es cerrado.** La clase de nota sigue siendo el meridiano, pero ordenada de izquierda a derecha en la cara visible (do en un borde, si en el otro, igual que ahora pero en 180° y no en 360°). Cambia la vecindad (`NEIGH`):
   - la primera y la última celda de un anillo **dejan de ser vecinas** (ya no se tocan por detrás);
   - la vecindad entre anillos contiguos (hexagonal desplazada) y la de los polos se recalculan sobre la franja abierta;
   - `SIZE_EW` y `SIZE_NS` se recalculan: las celdas miden la mitad de ancho este-oeste.
4. **Todo lo que usa la retícula se adapta**: `NORMALS`, `lonlat_celda`, `celda_de_lonlat`, `celda_de_casilla`, `casilla_de_celda`. En el modo hemisferio **toda celda tiene casilla** (`cara_visible` = todas las celdas, `casilla_de_celda` nunca devuelve `None`).
5. **Cambiar `Hemisferio` es como cambiar el rango de notas**: la geometría cambia y el mundo se vacía (`set_grid` ya devuelve `True` en ese caso). Una partida no cambia de modo a medias.

### 2.2 El planeta no gira en este modo

Si el planeta girase, lo construido pasaría a la cara oculta, que ahora no tiene celdas. **Propuesta por defecto (D1):** con `Hemisferio` encendido, el giro vivo queda apagado (`Giro` fijo, `Loncentral` fijo en 0) y la cámara no rota. Las celdas están ancladas a la vista.

Consecuencias a resolver:

- `celda_aparicion` usa «el borde por el que entran las celdas con el giro». Sin giro ya no hay borde de entrada. **Propuesta (D2):** aparecen en la celda vacía del **borde lateral** más lejano al otro monstruo (lado izquierdo o derecho alternando con `n`, desempate `_hash01`), como pronto después de `Esperamonstruo` y nunca en una celda ni vecina de la del otro monstruo.
- Si más adelante se quiere un balanceo suave (±10° alrededor de `Loncentral`), queda fuera de esta fase.

### 2.3 El cerco de los monstruos: nunca fuera de la cara visible

*(«El cerco» aquí es el recinto donde se mueven los monstruos, no el arma de la fase 37.)*

Con `Hemisferio`, los dos monstruos solo existen y solo se mueven por las celdas de la retícula, que ya están todas en la cara visible. Hay que asegurar que **ningún camino, objetivo, aparición ni retirada pueda salir de ella**:

- `dijkstra_mon`, `objetivo`, `muro_tregua` y la retirada tras la lucha (fase 40: «cada uno se va por donde vino») trabajan solo con celdas del hemisferio.
- La aparición (`celda_aparicion`) ya no tiene el caso de reserva «si no hay vacía en la cara visible, usa cualquiera del globo»: ahora el globo **es** la cara visible.
- La lucha (fase 40) se acerca y retira por celdas contiguas: con el anillo abierto, dos celdas de los bordes laterales ya no son contiguas.
- El recuento de la ronda (`recuento`) y la construida visible (`construida_visible`) coinciden: todo el globo es la cara visible.

### 2.4 Los monstruos buscan las pulsaciones de los secuenciadores

Hoy el objetivo de Trumpzilla es la celda del público con mayor `occ / (1 + coste)` y el de Godzilla la celda del mal con mayor `occ / (1 + coste)`. Con `Hemisferio` **les importa dónde suenan los secuenciadores**:

- La señal ya existe: `W['t_gate'][i]` (última nota en la celda `i`) y `W['terr'][i]` (último compás en que la tocó un SEQ).
- **Propuesta (D3):** la puntuación pasa a `occ × (1 + Pesopulso × calor) / (1 + coste)`, con `calor ∈ [0, 1]` = frescura de la última pulsación en la celda **o en sus vecinas** (1 si es de este paso, bajando linealmente a 0 en `Ventanapulso` pasos de juego). Con `Pesopulso` = 0 es la regla de hoy.
- **Trumpzilla** busca celdas del público con pulsaciones recientes (donde se está construyendo ahora). **Godzilla** busca celdas del mal con pulsaciones recientes (el mal también crece con los triggers de los secuenciadores, fase 33 «BROTE»).
- **Sin pulsaciones recientes en ninguna celda** que pueda comer, vale la regla de hoy (mayor `occ / (1 + coste)`). Nunca se quedan sin objetivo por esto.
- Siguen las reglas de siempre: el pequeño no come fusiones ni coronas, `Montierra`, zanjas y arma del cerco son muro o coste, y el recálculo es cada `Recalculo` pasos o al vaciar una celda.
- Presupuesto: sin coste apreciable (menos de 1 ms por fotograma para todo el juego, como siempre).

### 2.5 Lo que no cambia

El ritmo de los monstruos (`Pasomonstruo`, `Pasogrande`, `Ritmodevora`), el crecimiento, las zanjas, las armas, el rescate, la luz del juego, las caras y los atlas, los brotes y las reglas de la lucha (salvo la contigüidad del 2.3) siguen como en las fases 33 a 40. Todo lo que dependa de que existiera una cara oculta (por ejemplo, el recuento «3 de ellas fuera de la cara visible» de la autoprueba de la fase 32) se ajusta solo en modo hemisferio.

---

## 3. Parámetros (página `Fase41`)

| Parámetro | De fábrica | Qué es |
|---|---|---|
| `Hemisferio` | apagado | Retícula repartida solo por la cara visible; sin cara oculta |
| `Pesopulso` | 1,0 | Cuánto pesan las pulsaciones recientes en el objetivo (0 = regla de hoy) |
| `Ventanapulso` | 8 | Pasos de juego que tarda una pulsación en dejar de contar |
| `Giroenhemisferio` | apagado | Si se enciende, deja girar el planeta aunque haya hemisferio (no recomendado; no soportado en esta fase) |

**Línea de la leyenda** (en mayúsculas y sin tildes en el código, como las demás):

```
HEMISFERIO  celdas 85 · cara visible 85/85 · objetivo con pulso (calor 0.75)
```

---

## 4. Decisiones que tienes que concretar (con propuesta por defecto)

Elige y documenta. Si una no encaja, avísalo en el PR.

1. **Giro del planeta (D1).** Propuesta: apagado y `Loncentral` fijo con `Hemisferio`. Alternativa: dejarlo girar y que las celdas que pasan por el borde se «envuelvan» (más complejo; no recomendado).
2. **Aparición (D2).** Propuesta: borde lateral, alternando lado, lejos del otro monstruo.
3. **Cómo se mide «dónde hay pulsaciones» (D3).** Propuesta: `t_gate` de la celda y las vecinas, con la frescura lineal y `Pesopulso` / `Ventanapulso`. Alternativa: contar solo la última celda tocada por cada SEQ (`W['last']`), más simple pero menos estable.
4. **Reparto de las 12 clases de nota en 180° (D4).** Propuesta: do en el borde izquierdo y si en el derecho, `15°` por celda en el anillo completo. Los anillos incompletos (el primero y el último si el rango no empieza o acaba en do) reparten sus celdas por igual a lo ancho, como hoy.
5. **Anchoangular distinto de 180° (D5).** Propuesta: la franja usa `Anchoangular` (se reparte en ese ancho); por debajo de ~120° las celdas salen muy estrechas y la autoprueba lo avisa, no lo impide.
6. **Partidas guardadas / mundo existente.** Propuesta: cambiar `Hemisferio` vacía el mundo (como cambiar el rango); no hay migración.

---

## 5. Convenciones

Las de siempre: un script `fase41_hemisferio.py` que carga `estratos_comun.py`, dice su versión en la primera línea, se niega a correr sin la fase anterior (`require_base`), sube `Nivel`, crea su página `Fase41` en `/project1/FASE1`, añade su línea a la leyenda, escribe su `LEEME` y termina con la autoprueba (`AUTOPRUEBA OK` o qué falla), que deja el mundo como estaba. La lógica va al motor (`motor v137`) y se activa con `Nivel` y `Hemisferio`. Sin `random`: sorteos y desempates con `logistica`, `semilla_caos` o `_hash01`. TouchDesigner no envía nada al BeatStep. Se documenta en `docs/MONTAJE_FASE41.md` y se añade a `pruebas/correr_fases.py`.

---

## 6. Criterio de cierre (la autoprueba lo comprueba)

1. **Retícula.** Con `Hemisferio` y do1–do8: `N = 85`; todas las celdas tienen casilla; ninguna tiene longitud fuera de `Loncentral ± Anchoangular/2`; el anillo de 12 mide 15° por celda; la primera y la última del anillo **no** son vecinas; `NEIGH` es simétrico y conexo. Con `Hemisferio` apagado, la retícula es idéntica byte a byte a la de `motor v136`.
2. **Notas.** Todas las notas del rango (y las plegadas por `fold_note`) caen en una celda de la cara visible; `note_cell` y `celda_de_casilla` son coherentes entre sí.
3. **Cerco.** Mil pasos de partida simulada con `Simmonstruo` y `Godzillasala` = siempre: ninguna celda de ningún monstruo, objetivo, camino, aparición ni retirada queda fuera del hemisferio (trivial por construcción, pero se comprueba) y ninguno se queda sin moverse más de `Recalculo` pasos con comida alcanzable.
4. **Pulsaciones.** Con el público construido en dos zonas y los secuenciadores sonando solo en una, Trumpzilla elige la celda de esa zona aunque la otra tenga más `occ`; sin pulsaciones, elige la de mayor `occ / (1 + coste)`. Lo mismo, con el mal, para Godzilla. Con `Pesopulso` = 0, la elección es la de la fase 33/40 en todos los casos.
5. **Lucha y aparición.** La aparición cumple D2; la lucha se acerca, pelea y se retira sin salir de las celdas; con anillos abiertos, dos monstruos en los bordes laterales opuestos no se consideran contiguos.
6. **Sin regresiones.** Las autopruebas de las fases 32 a 40, con `Hemisferio` apagado, pasan igual que en `motor v136`.
7. **Presupuesto.** El juego completo sigue por debajo de 1 ms por fotograma en Python.
