# Estratos · Montaje
## Fase 40: Godzilla, el monstruo de la creación

*Continúa `MONTAJE_FASE39.md`. Sin nadie en la sala, Trumpzilla se comía el planeta: nadie cavaba zanjas, nadie rescataba brotes y el mal ganaba la partida entera (el motor v122 ya le quitó la mitad del daño por eso). Esta fase pone a su reverso: **Godzilla**, que hace por la creación del mundo lo que Trumpzilla hace por el mal. Devora el mal y deja brotes de la creación. Cuando los dos monstruos se encuentran, se pelean a manotazos.*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 40 | `fase40_godzilla.py` | Godzilla (aparece con la sala vacía, devora el mal, crea) y la lucha con Trumpzilla | v123 | v91 |
| 40 v3 | `fase40_godzilla.py` | Godzilla solo anda por tierra, como Trumpzilla; para los dos, las carreteras y vías que cruzan el agua son camino | v131 | v97 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase40_godzilla.py').read())
```

**Antes de lanzarla:** copia la carpeta `sprites/` del repositorio dentro de la carpeta de los scripts (`C:/Users/DareDave/Downloads/est/sprites/godzilla_emociones.png`). Si falta, el informe dice `FALLO godzilla_atlas: no encuentro ...`.

También cambia `estratos_comun.py` (v91): `SalaJuego` apaga `Godzilla` en las autopruebas de las fases 32 a 39 (prueban a Trumpzilla solo; con la sala simulada vacía, Godzilla saldría y les cambiaría la partida) y `guardar_sala` lo devuelve como estaba.

---

## Qué hace

**Cuándo sale.** Con `Godzillasala` = *vacía* (de fábrica), solo cuando no hay nadie en la sala desde hace `Tvacia` segundos (15). Al empezar la partida cuenta como si acabara de haber gente. Si llega alguien, Godzilla **se va**: saluda con una flor (cara *calma*), se mece y se hunde en 2 s. Vuelve cuando la sala lleva otra vez `Tvacia` s vacía (y como pronto `Esperamonstruo` s después de irse). Con *siempre*, también con público.

**Aparece** cuando hay `Malgodzilla` celdas del mal o más en el globo (1), en la celda vacía de la cara visible más cercana al borde por el que entran las celdas con el giro, como Trumpzilla, pero nunca en su celda ni en sus vecinas.

**Devora el mal.** Su objetivo es la celda del mal de mayor `occ / (1 + coste)` (el mismo Dijkstra que Trumpzilla). El pequeño no puede con fusiones ni coronas del mal; el grande, sí. Anda al mismo paso (`Pasomonstruo`, `Pasogrande`), devora al mismo ritmo (`Ritmodevora`, `Ritmogrande` × `Danomonstruo`) y crece igual (`Tamanoinicial`, `Ocupacionmax`): la lucha está **equilibrada**. Nunca come lo del público.

**Crea.** La celda del mal que vacía recibe un **brote de la creación**: ocupación 1 con la especie del último secuenciador que la tocó (fase 35; si ninguno, la de su origen). Es del público, cuenta en el recuento y crece con las notas como cualquier otra. Con la especie del mal (fase 39), la valla cae.

**Solo anda por tierra (v3),** con las reglas de Trumpzilla (`Montierra`, fase 39): con `Oceano` no entra en el mar ni en las hondonadas inundadas. Pasa por lo construido (las islas), la tierra firme y las **carreteras y vías del tren que cruzan el agua** (motor v131: una celda de mar con carretera o vía cuenta como tierra, también para Trumpzilla). Si entre él y el mal solo hay mar, se queda en *calma*. Aparece en tierra (si todo lo vacío es mar, en una isla) y tras la lucha se retira por tierra. En la v1 nadaba. Las zanjas son del público contra el mal: el agua de una zanja es muro para él y entrar en una cuesta `Costezanja`, pero no cae ni se ahoga. Las armas de la fase 37 no le tocan.

### La lucha

Si los dos monstruos quedan en **celdas contiguas** (o en la misma), empieza la lucha:

1. **Se acercan al borde.** Cada uno avanza hacia la celda del otro hasta el 38 % del camino (en 0,6 s) y se miran.
2. **Manotazos** durante `Pasoslucha` pasos de juego (8: dos compases a 4 semicorcheas por paso). Ni andan ni devoran. Por turnos de 0,3 s, uno da (cara *furia*, se echa encima) y el otro recibe (cara *mueca*, tiembla).
3. **Cada uno se va por donde vino**: vuelve a la celda de la que venía (si no vale —es la del otro, agua o mar—, a la vecina más lejos del otro).
4. **Tregua** de `Tregua` pasos (16): ninguno pasa por la celda del otro ni por sus vecinas, y no vuelven a pelear aunque se crucen.

Si uno deja de luchar a mitad (Trumpzilla se ahoga o cae en una zanja, llega gente y Godzilla se va), la lucha se acaba.

### Las caras

El atlas `sprites/godzilla_emociones.png` tiene el formato del de Trumpzilla (768 × 768, 4 × 3 celdas de 192 × 256, las diez caras en el orden de `EMOCIONES_MON`, mirando a la izquierda con los pies abajo) y usa su shader. Godzilla es un saurio verde con las placas de la espalda en forma de hoja (lo que crea) y la tripa clara.

| Situación | Cara | Animación |
|---|---|---|
| Se va (llega gente) | calma (saluda con una flor) | adiós: se mece y se hunde |
| Lucha, da | furia (placas encendidas) | lucha: se echa encima |
| Lucha, recibe | mueca (estrellas) | tiembla |
| Su celda tiene agua | pánico | tiembla |
| En una zanja | susto | respira |
| Devora, y 1,2 s después | ríe (carcajada si es grande) | mastica |
| Aparece | serio | respira |
| Busca y anda | enfado (furia si es grande) | bambolea |
| Sin mal que comer | calma | respira |
| Quieto | serio | respira |

Trumpzilla, en la lucha, igual pero al revés: cuando Godzilla da, él recibe.

**Rehacerlo.** `sprites/hacer_atlas_godzilla.py` (Pillow) lo dibuja con formas, a 4 veces el tamaño y reducido, con el recorte duro del shader. `sprites/godzilla_emociones_lamina.png` es la hoja de prueba. Para cambiarlo por un dibujo hecho a mano basta con otro PNG del mismo formato.

```
python3 sprites/hacer_atlas_godzilla.py
```

### Operadores nuevos (en /project1/FASE1)

| Operador | Tipo | Qué es |
|---|---|---|
| `godzilla`, `i_godzilla` | Geometry COMP + Script CHOP | Una lámina (Rectangle SOP 1 × 1) instanciada: la sombra y el sprite, como `trumpzilla` |
| `mat_godzilla` | GLSL MAT | Los shaders de Trumpzilla (`sprite_vertex`, `sprite_pixel`) con el sampler `sAtlas` en `godzilla_atlas`; mismas luces y uniformes que `mat_sprite` (`Pixelsprite`, `Inclinasprite`, `Brillosprite` valen para los dos) |
| `godzilla_atlas` | Movie File In TOP | `sprites/godzilla_emociones.png` |

El shader (comun v91) suma dos animaciones: 7 *lucha* (se inclina y se echa hacia donde mira, con un temblor rápido) y 8 *adiós* (se mece despacio; el motor lo hunde).

### Parámetros (página Fase40)

| Parámetro | Defecto | Qué hace |
|---|---|---|
| `Godzilla` | encendido | Godzilla en el juego; apagado, el juego de la fase 39 |
| `Godzillasala` | vacía | *Solo con la sala vacía* o *siempre* |
| `Tvacia` | 15 s | Segundos sin nadie en la sala para que salga |
| `Malgodzilla` | 1 | Celdas del mal en el globo para que aparezca |
| `Pasoslucha` | 8 | Pasos de juego de manotazos |
| `Tregua` | 16 | Pasos tras la lucha sin cruzarse ni pelear |
| `Altogodzilla` | 0,8 | Alto en celdas, por `tam` (como `Altosprite`) |
| `Emociongodzilla` | auto | Fija una cara (ensayo) |
| `Simgodzilla` | pulso | Aparece ya (sin esperar a la sala vacía ni al mal) |
| `Simlucha` | pulso | Trumpzilla en `Simceldamon` (si no está) y Godzilla en una vecina: la lucha |

### Leyenda

```
GODZILLA #1  devora  celda 12 -> 12  tam 0.75  acum 4/8   creados 3   cara rie   sala vacia
GODZILLA #1  espera   mal 2 (aparece con 1)   creados 0   sala vacia 6/15 s
LUCHA    manotazos 5/8 pasos   celdas 40 | 41   (luchas 2)
LUCHA    tregua 9 pasos   (luchas 2)
```

---

## Prueba manual

1. `Modojuego`, `Simmal` (un clúster del mal) y `Simgodzilla`: aparece **serio**, va **enfadado** a la celda del mal más próspera, la devora **riendo** y la celda vuelve a ser del público (cae la valla). Sin mal que comer, **calma**.
2. `Simlucha`: Trumpzilla y Godzilla en celdas vecinas se acercan al borde y se dan manotazos 8 pasos (furia y mueca, por turnos); luego cada uno vuelve a su celda de antes. La línea `LUCHA` cuenta los pasos y la tregua.
3. Con la cámara (o `Simponer`): con alguien en la sala Godzilla **se va** saludando; 15 s después de que se vaya el último, vuelve.
4. `Godzilla` apagado: el juego de la fase 39.

## Qué ajustar en sala

- **`Tvacia`**: el tiempo que tiene que estar la sala vacía. Corto, Godzilla entra y sale con cada visitante; largo, el mal avanza sin oposición más rato.
- **`Godzillasala` = siempre**: si con público el mal sigue ganando. Ojo: con los dos monstruos y el público, el mal lo tiene difícil.
- **`Pasoslucha`** y **`Tregua`**: más pasos de lucha, más espectáculo y menos devorar; más tregua, menos luchas seguidas.
- **`Altogodzilla`**: si se quiere que se lea más grande o más pequeño que Trumpzilla.

## Pruebas

`python3 pruebas/correr_fases.py` corre las fases 3 a 40 en el TouchDesigner simulado. La autoprueba de la fase 40 (ocho comprobaciones):

- El atlas, `godzilla`, `i_godzilla`, `mat_godzilla` y el render.
- Sin Godzilla, o con gente en la sala, la misma partida da lo mismo que tras la fase 39; con la sala vacía, Godzilla sale.
- Aparece tras `Tvacia` s de sala vacía (no antes) y va a por el mal; con gente, se va (calma, adiós), desaparece y vuelve.
- Devora el mal con el ritmo de Trumpzilla y deja un brote de la creación con la especie del último secuenciador; nunca come público; el pequeño no puede con una fusión del mal.
- La lucha: se acercan al borde mirándose, manotazos por turnos, 8 pasos quietos, cada uno vuelve a la celda de la que venía, la tregua y la lucha siguiente.
- `Simlucha`, la leyenda, `Godzilla` apagado (acaba la lucha) y `Modojuego` apagado.
- Una ronda con la sala vacía: con Godzilla el mal acaba con menos celdas que sin él, y dos veces la misma ronda dan lo mismo (determinista).
- (v3) Con `Oceano`: con mar entre su isla y el mal no tiene objetivo ni cruza el mar por un camino viejo; con una carretera sobre el agua, va por ella.
