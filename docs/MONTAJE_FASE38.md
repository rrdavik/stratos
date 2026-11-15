# Estratos · Montaje
## Fase 38: Trumpzilla, el monstruo en sprite con emociones

*Continúa `MONTAJE_FASES_32_37.md`. La fase 33 dejó el monstruo provisional (una esfera con dos ojos) en su propio COMP, «para cambiarlo por un sprite tipo arcade de 8 bits sin tocar la lógica». Esta fase lo hace: el monstruo es **Trumpzilla**, un sprite con diez caras que cambian con lo que le pasa en la partida. La lógica del juego no cambia (lo comprueba la autoprueba: la misma partida da el mismo resultado con la fase 37 y con la 38).*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 38 | `fase38_trumpzilla.py` | El monstruo en sprite: atlas de emociones, sombra, volteo, animaciones | v112 | v83 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase38_trumpzilla.py').read())
```

**Antes de lanzarla:** copia la carpeta `sprites/` del repositorio dentro de la carpeta de los scripts (`C:/Users/DareDave/Downloads/est/sprites/trumpzilla_emociones.png`). Si falta, el informe dice `FALLO trumpzilla_atlas: no encuentro ...`.

---

## El atlas

`sprites/trumpzilla_emociones.png`: 768 × 768, 4 × 3 celdas de 192 × 256, con fondo transparente y recorte duro (el shader descarta por alfa). Las caras van de arriba a la izquierda en el orden de `EMOCIONES_MON` del motor:

| # | Cara | Sale de |
|---|---|---|
| 0 | serio | la figura seria, con el ceño fruncido |
| 1 | enfado | la figura que ruge con los puños cerrados |
| 2 | furia | la cara roja (fila de cuatro, b) |
| 3 | rie | fila de cuatro, a |
| 4 | carcajada | llora de risa (fila b) |
| 5 | susto | fila b |
| 6 | mueca | fila b |
| 7 | llora | fila a |
| 8 | panico | llora asustado (fila a) |
| 9 | calma | fila a |

Todas miran a la izquierda de la imagen, con los pies abajo y centrados, a la misma altura. `sprites/trumpzilla_emociones_lamina.png` es la hoja de prueba con los nombres.

**Rehacerlo.** `sprites/hacer_atlas_trumpzilla.py` (fuera de TouchDesigner, con Pillow, NumPy y SciPy) quita el fondo de cuadros pintado de los JPG, separa las cuatro figuras de cada fila por el contorno de la vecina y les pone debajo la espalda (espinas y cola) de la figura seria, porque en las filas la cola queda tapada por la vecina o cortada por el borde:

```
python3 sprites/hacer_atlas_trumpzilla.py enfado.jpg cuatro_a.jpg cuatro_b.jpg serio.jpg
```

Para añadir caras: más celdas en `COLS × FILAS`, el nombre en `EMOCIONES` del script y en `EMOCIONES_MON` del motor (mismo orden), y su regla en `emocion_mon`.

---

## Qué hace

- **El sprite.** Una lámina de pie sobre la celda del monstruo, con los pies en el suelo, que mira siempre a la cámara. Su «arriba» es el de la pantalla, inclinado hacia la vertical del planeta como mucho `Inclinasprite` grados (30): así no se tumba en el borde del globo ni queda boca abajo en el hemisferio sur. Con la cámara rasante la vertical del planeta ya es la de la pantalla. Lleva una sombra redonda en el suelo, sigue el giro del planeta, avanza entre celdas como el monstruo y **se voltea hacia donde camina**. Mide `Altosprite` celdas por `tam` (crece con lo que devora); el ancho, 3/4 del alto.
- **Las emociones.** Salen del estado del monstruo; vale la primera de la lista:

| Situación | Cara | Animación |
|---|---|---|
| Se ahoga (muere) | panico | se hunde 2 s y desaparece |
| Petrificado (estatuas, fase 37) | calma | gris piedra, quieto |
| Aturdido (relámpago, fase 37) | mueca | se tambalea y parpadea |
| Cae en una zanja, y 1,5 s después | susto | tiembla |
| Su zanja tiene agua | panico | tiembla |
| En una zanja | llora | respira |
| Pisotón (fase 37) | llora | tiembla |
| Acorralado (cerco, fase 37) | panico | tiembla |
| Devora, y 1,2 s después de tragar | rie (carcajada si es grande) | mastica |
| Aparece | serio | respira |
| Busca y anda | enfado (furia si es grande) | bambolea |
| Quieto | serio (furia si es grande) | respira |

- **El render.** Las geometrías del juego (`marcas`, `brotes_mal`, `tocon`, `monstruo`, `agua_juego`) no estaban en la lista del Render TOP y **no se dibujaban**. Desde comun v83 están, y `trumpzilla` con ellas.
- **La leyenda.** La línea `MONSTRUO` termina con la cara: `MONSTRUO #3  busca  celda 40 -> 52  tam 0.62  acum 5/8  x2   cara enfado`.

### Operadores nuevos (en /project1/FASE1)

| Operador | Tipo | Qué es |
|---|---|---|
| `trumpzilla`, `i_trumpzilla` | Geometry COMP + Script CHOP | Una lámina (Rectangle SOP 1 × 1) instanciada: la sombra y el sprite |
| `mat_sprite` | GLSL MAT | `sprite_vertex` y `sprite_pixel`; sampler `sAtlas`; uniformes `uSprite` (reloj `sprite_t` de `frame_u`, `Pixelsprite`, columnas y filas) y `uSpriteInc` (`Inclinasprite`). Blending One / One Minus Source Alpha, escribe profundidad, sin culling |
| `trumpzilla_atlas` | Movie File In TOP | `sprites/trumpzilla_emociones.png` |
| `sprite_vertex`, `sprite_pixel` | Text DAT | Los shaders |

En cada fila de `trumpzilla`, el alfa lleva `cara + 16 × animación` (el sprite) o `256` (la sombra). El eje z local de la instancia es hacia donde camina; el shader lo usa para voltear el dibujo. La cara se lee del atlas con `texelFetch` (sin suavizar).

### Parámetros (página Fase38)

| Parámetro | Defecto | Qué hace |
|---|---|---|
| `Spritemonstruo` | encendido | Trumpzilla en lugar del cuerpo provisional de la fase 33 |
| `Emocion` | auto | Fija una cara (ensayo o función); auto, la del estado |
| `Altosprite` | 1,6 | Alto en celdas, por `tam` |
| `Pixelsprite` | 0 | Filas de píxeles de alto (96 o 64: arcade de 8 bits); 0, el atlas tal cual |
| `Inclinasprite` | 30 | Grados que se inclina hacia la vertical del planeta (180: del todo) |

---

## Prueba manual

1. `Modojuego`. `Sembrar` hasta 3 en una celda a dos de la del monstruo; `Simmonstruo`: aparece **serio**, va **enfadado** a la celda (bambolea, mirando hacia donde va) y se la come **riendo**.
2. Deja que devore 8 escalones: forma grande, **furia** al buscar y **carcajada** al devorar.
3. Con una fila de 3 a su paso (`Simfila` 3, `Simformarfila`): cae con **susto** y **llora** en la zanja. Con 4 (zanja con agua): **pánico**, y al ahogarse se hunde.
4. `Emocion`: pasa por las diez caras. `Pixelsprite` 96 y 64: más arcade. `Inclinasprite` 0 y 180: siempre vertical en pantalla / siempre de pie sobre el planeta.
5. `Spritemonstruo` apagado: vuelve la esfera de la fase 33.

## Qué ajustar en sala

- **`Altosprite`** según la distancia del público y el tamaño de las celdas: que se lea la cara sin tapar las construcciones que devora.
- **`Pixelsprite`**: con el proyector, 0 puede verse ruidoso de lejos; 96 da un aire arcade y se lee mejor.
- **`Inclinasprite`**: 30 es el término medio en la vista de globo; si molesta que se incline, 0.

## Pruebas

`python3 pruebas/correr_fases.py` corre las fases 3 a 38 en el TouchDesigner simulado (la autoprueba de la fase 38: once comprobaciones). La autoprueba de la fase 33 (v2) apaga `Spritemonstruo` para seguir probando el cuerpo provisional.
