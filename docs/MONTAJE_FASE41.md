# Estratos · Montaje
## Fase 41: Hemisferio, el juego solo en la cara visible

*Continúa `MONTAJE_FASE40.md`. Requerimiento de origen: `REQUERIMIENTO_FASE_41_HEMISFERIO.md`. Los monstruos se perdían a veces en la cara oculta del planeta y la partida perdía foco. Con **Hemisferio** las celdas solo existen en la cara visible.*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 41 | `fase41_hemisferio.py` | Retícula solo en la cara visible, planeta quieto, monstruos que buscan las pulsaciones | v137 | v99 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase41_hemisferio.py').read())
```

Con `Hemisferio` apagado (de fábrica) todo es idéntico a la fase 40 (la retícula coincide celda por celda con la del motor v136).

---

## Qué hace

**Retícula.** Con `Hemisferio`, `N` no cambia (una celda por nota del rango), pero `set_grid(lo, hi, mode, hemi)` reparte las celdas por la franja de longitud `±Anchoangular/2` (180° de fábrica): el anillo de 12 notas pasa de 30° a 15° por celda, el anillo **no se cierra por detrás** (la primera y la última celda no son vecinas), los polos quedan arriba y abajo del disco, `SIZE_EW` mide la mitad y toda celda tiene casilla (`cara_visible` = todo el globo). `Anchoangular` se limita a 30–180°. Cambiar `Hemisferio` o `Anchoangular` es como cambiar el rango de notas: el mundo empieza vacío (`grid_key()` pasa a `[lo, hi, ancho]`).

**El planeta no gira (D1).** `lon_central` devuelve 0, `giro_factor` 0 y `giro_fijo()` da `HEMI_RY = -90`. `ritmo.rotation()` lo consulta (comun v99, `patch_ritmo_hemi`, que `install_core` aplica en todas las fases); sin Hemisferio, `giro_fijo()` es `None` y gira como siempre.

**El cerco.** Trumpzilla y Godzilla solo pisan celdas de la retícula, que ya son todas la cara visible: ningún camino, objetivo, aparición ni retirada sale de ella. Sin giro no hay borde de entrada (D2): `signo_borde` hace que Trumpzilla aparezca en el borde lateral derecho (el #2 en el izquierdo, alternando con `n`) y Godzilla en el borde contrario al de Trumpzilla.

**Pulsaciones (D3).** `objetivo` puntúa `occ × (1 + Pesopulso × calor) / (1 + coste)` (los dos monstruos, con su regla de qué se come). `calor_pulso` mira `W['t_gate']` de la celda y sus vecinas: 1 si sonó ahora, 0 pasadas `Ventanapulso` pasos de juego (`Ventanapulso × Pasojuego × W['paso']` s). Sin pulsaciones dentro de la ventana, o con `Pesopulso` 0, la regla de siempre.

## Decisiones tomadas

- **D1** giro apagado y `Loncentral` 0 (sin balanceo). **D2** borde lateral alternando; Godzilla en el contrario. **D3** `t_gate` de la celda y las vecinas, frescura lineal. **D4** clases de nota de izquierda a derecha, 15° por celda; los anillos incompletos reparten por igual a lo ancho. **D5** la franja usa `Anchoangular` (30–180°). **D6** sin migración: cambiar `Hemisferio` vacía el mundo.
- No se ha creado el parámetro `Giroenhemisferio` del requerimiento (quedaba como «no soportado en esta fase»).
- La reserva de `celda_aparicion` («si no hay vacía en la cara visible, usa cualquiera») se deja: con Hemisferio equivale a la cara visible.
- Las cachés de geometría del motor llevan `GRID['hemi']` en su clave (en `terreno` va al final para no mover los índices de la tupla).

## Parámetros (página Fase41)

| Parámetro | De fábrica | Qué es |
|---|---|---|
| `Hemisferio` | apagado | Retícula solo en la cara visible |
| `Pesopulso` | 1,0 | Peso de las pulsaciones en el objetivo (0 = regla de hoy) |
| `Ventanapulso` | 8 | Pasos de juego que tarda una pulsación en dejar de contar |

Leyenda: `HEMISFERIO  celdas 85   cara visible 85/85   objetivo con pulso (calor 0.75)`.

## Autoprueba

`fase41_hemisferio.py` comprueba: la retícula (N, casillas, 15°, extremos no vecinos, simétrica y conexa, y la esfera idéntica sin Hemisferio), las 128 notas en plegar y limitar y las casillas, el planeta quieto, 400 pasos con los dos monstruos sin salir del hemisferio, el objetivo con y sin pulsaciones (Trumpzilla y Godzilla), la aparición por los bordes y la leyenda. Corre en `pruebas/correr_fases.py`, y las fases 3 a 40 siguen igual.
