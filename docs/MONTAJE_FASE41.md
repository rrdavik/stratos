# Estratos · Montaje
## Fase 41: Hemisferio, la reja fija en la cara visible

*Continúa `MONTAJE_FASE40.md`. Requerimiento de origen: `REQUERIMIENTO_FASE_41_HEMISFERIO.md` (la versión v1 de esta fase dejaba el planeta quieto; la v2, que es la buena, lo deja girar como siempre). Los monstruos se perdían a veces en la cara oculta y la partida perdía foco.*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 41 | `fase41_hemisferio.py` | Superficie de doble densidad bajo una reja fija de notas; los monstruos paran en la cara oculta y buscan las pulsaciones | v137 | v98 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase41_hemisferio.py').read())
```

Con `Hemisferio` apagado (de fábrica) todo es idéntico a la fase 40 (la retícula coincide celda por celda con la del motor v136).

---

## La idea

Dos capas. La **superficie** gira con el planeta, como siempre, y con `Hemisferio` tiene el doble de celdas. La **reja de vista** no gira, como la cámara y la sala: es donde caen las notas del rango. La superficie pasa por debajo y va encajando en la reja.

- **Superficie.** `ring_layout(lo, hi, doble)`: 24 celdas por anillo completo (15°), con los anillos pares e impares desplazados media celda (vecindad hexagonal); unas `2N - 2` celdas (168 con do1–do8). El polo sur es la celda 0 y el polo norte la última: **las celdas ya no son las notas**.
- **Reja de vista** (`vista_notas`). Cada nota del rango tiene su posición fija en la cara visible: la clase de nota es la columna (12 por anillo, 15° cada una), la octava el anillo, y los polos arriba y abajo.
- **Nota → celda** (`note_cell(nota, cfg)`). La nota va a su sitio de la reja y de ahí a la celda de la superficie que hay debajo de su centro en ese instante (`Loncentral` sigue al giro: la misma maquinaria de `celda_de_casilla` para las personas). Cada 15° de giro la superficie encaja otra vez con la reja; entre medias, la nota cae en la celda cuyo centro está más cerca. `note_off` usa la celda guardada en `pend`, así que suelta la misma que prendió.
- **`cell_note(x)`.** Con Hemisferio devuelve la nota virtual `CELDA_BASE + x` (1000 + x); `note_cell` la lleva directa a la celda x. Así siguen funcionando las llamadas internas (pruebas, demos) que tocan «la celda x».
- **Monstruos.** Circulan por la superficie como siempre y aparecen en la cara visible por el borde de entrada del giro. Si la rotación los lleva a la cara oculta, `en_oscuridad` los para (entra en `parado`): ni andan, ni devoran, ni luchan; la lucha en curso también se detiene. Cuando la superficie los devuelve a la cara visible, siguen. Los polos se cuentan como visibles.
- **Pulsaciones.** `objetivo` puntúa `occ × (1 + Pesopulso × calor) / (1 + coste)` (los dos monstruos, con su regla de qué se come). `calor_pulso` mira `W['t_gate']` de la celda y sus vecinas: 1 si sonó ahora, 0 pasadas `Ventanapulso` pasos de juego (`Ventanapulso × Pasojuego × W['paso']` s). Sin pulsaciones dentro de la ventana, o con `Pesopulso` 0, la regla de siempre.

Cambiar `Hemisferio` es como cambiar el rango de notas: otra retícula, el mundo empieza vacío (`grid_key()` pasa a `[lo, hi, 'hemi']`).

## Decisiones tomadas

- Las celdas de superficie miden lo mismo que las de la reja (15°) y encajan cada 15° de giro.
- Entre dos encajes, la nota cae en la celda de superficie más cercana al centro de su celda de reja.
- Los monstruos van atados a la superficie (no a la reja) y se paran, no desaparecen, en la cara oculta.
- La franja de la reja usa `Anchoangular` (180° de fábrica) y `Espejo`, como las casillas de la sala.
- Con Hemisferio hay unas 2N celdas y cada una cuesta lo mismo que antes: la ciudad, el terreno y los cachés trabajan con el doble.
- Las cachés de geometría llevan `GRID['hemi']` en la clave (en `terreno` va al final para no mover los índices de la tupla).
- Sin parámetro `Giroenhemisferio`: el planeta siempre gira como siempre.

## Parámetros (página Fase41)

| Parámetro | De fábrica | Qué es |
|---|---|---|
| `Hemisferio` | apagado | Superficie de doble densidad y reja fija de notas |
| `Pesopulso` | 1,0 | Peso de las pulsaciones en el objetivo (0 = regla de hoy) |
| `Ventanapulso` | 8 | Pasos de juego que tarda una pulsación en dejar de contar |

Leyenda: `HEMISFERIO  celdas 168   cara visible 85/168   objetivo con pulso (calor 0.75)   en la cara oculta: Trumpzilla`.

## Autoprueba

`fase41_hemisferio.py` comprueba: la superficie (doble de celdas, 24 por anillo a 15°, simétrica y conexa, y la esfera idéntica sin Hemisferio), la reja que no gira (12 notas en 12 celdas distintas, a la vista y en el mismo orden con cualquier `Loncentral`), el encaje a los 15°, una nota MIDI que construye en otra celda tras girar 60°, los monstruos parados en la cara oculta y en marcha al volver, que no luchan a oscuras, la aparición en la cara visible, el objetivo con y sin pulsaciones (Trumpzilla y Godzilla) y la leyenda. Corre en `pruebas/correr_fases.py`, y las fases 3 a 40 siguen igual.
