# Estratos · Montaje
## Fase 41: NefanyaMuto, el segundo monstruo del mal

*Continúa `MONTAJE_FASE40.md`. Trumpzilla deja de estar solo: cuando el mundo está construido a la mitad aparece **NefanyaMuto**, un MUTO (seis extremidades) con la cabeza de NefanyaMuto. Siembra el mal por su cuenta, como Trumpzilla. Si los dos se juntan, **bailan**, uno de ellos lanza **su golpe especial**, se giran y se van por caminos contrarios.*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 41 | `fase41_nefanyamuto.py` | NefanyaMuto (aparece al 50 %, siembra el mal), el baile con Trumpzilla y los dos golpes especiales | v142 | v99 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase41_nefanyamuto.py').read())
```

**Antes de lanzarla:** copia la carpeta `sprites/` del repositorio dentro de la carpeta de los scripts (`C:/Users/DareDave/Downloads/est/sprites/nefanyamuto_emociones.png`). Si falta, el informe dice `FALLO nefanyamuto_atlas: no encuentro ...`.

También cambian `estratos_comun.py` (v99: el shader de los sprites con dos animaciones nuevas, *baile* y *anillo*; `SalaJuego` apaga `Nefanyamuto` en las autopruebas de las fases 32 a 40, que prueban a Trumpzilla y Godzilla sin él) y la sala virtual (v35, sala v23: los capítulos de GENoZilla lo apagan, como ponen `Umbralaparicion` a 1, y al salir vuelve como estaba).

---

## Qué hace

**Cuándo sale.** Cuando la cara visible está construida (celdas del público) `Umbralnefa` o más: **0,5, al 50 %**. Aparece en la celda vacía de la cara visible por la que entran las celdas con el giro (como Trumpzilla), lejos de Trumpzilla y de Godzilla. Si se ahoga, vuelve `Esperamonstruo` s después (si el mundo sigue construido a ese punto).

**Siembra el mal** con las reglas de Trumpzilla: va a la construcción de mayor `occ / (1 + coste)` (el pequeño no puede con fusiones ni coronas), la devora con el mismo ritmo y daño, anda al mismo paso, crece igual, solo por tierra y buscando la cara visible. La celda que vacía recibe un brote del mal. Cae en las zanjas del público y se ahoga como Trumpzilla. Las armas de la fase 37 (cerco, pisotón, estatuas, grito, relámpago) son solo para Trumpzilla.

### El baile

Si Trumpzilla y NefanyaMuto quedan en **celdas contiguas** (o en la misma), fuera de su tregua:

1. **Se acercan al borde** mirándose, como en la lucha con Godzilla.
2. **Bailan** `Tiemposbaile` tiempos (8; un tiempo son `Pasos por tiempo` semicorcheas). Ni andan ni devoran. Caras *ríe* y *carcajada* a cada tiempo, los dos, con la animación *baile* (se balancean y botan).
3. **El golpe especial.** Uno de los dos lo lanza (`Golpebaile`: al azar —determinista: la misma partida da lo mismo— o uno fijo) y se queda dos tiempos en la pose:
   - **Trumpzilla absorbe para el mal** todas las construcciones (celdas del público) a `Radioabsorbe` celdas (2) o menos de cualquiera de los dos: alrededor de ellos y las siguientes inmediatas. Pasan al mal con lo que tenían; su obra del mal empieza en su etapa. Trumpzilla, *furia*; NefanyaMuto, *despiste*.
   - **NefanyaMuto** enciende su **anillo** (un pulso electromagnético azul alrededor de la cabeza, el poder de los MUTO) y abre una **zanja delante de él, hacia Trumpzilla**: `Largozanjanefa` celdas (5) en línea, con `Profzanjanefa` conchas (3) en la más honda (la del medio) y menos hacia los extremos (1 2 3 2 1). Lo que hubiera en esas celdas se va con la zanja. Trumpzilla, que está en la primera, **cae** (pierde lo comido). NefanyaMuto, *furia* con el anillo; Trumpzilla, *susto*.
4. **Se giran y se van por caminos contrarios:** cada uno a la vecina más lejos del otro. Hay `Tregua` pasos (16, el de la fase 40) en que no se cruzan ni vuelven a bailar.

Si uno deja de bailar a mitad (se ahoga, cae en una zanja, se apaga NefanyaMuto), el baile se acaba. Godzilla solo pelea con Trumpzilla.

### Las caras

El atlas `sprites/nefanyamuto_emociones.png` tiene el formato de los otros (768 × 768, 4 × 3 celdas de 192 × 256) y usa su shader, pero llena las doce celdas: las diez caras de `EMOCIONES_MON` y dos de no enterarse de nada, *despiste* (bizco) y *pasmado* (hurgándose la nariz). Sale de imágenes en pixel art y de fotos (`sprites/hacer_atlas_nefanyamuto.py`).

| Situación | Cara | Animación |
|---|---|---|
| Se ahoga (muere) | pánico | se hunde |
| Baila | ríe / carcajada a cada tiempo | baile |
| Lanza su golpe (y mientras brilla el anillo) | furia | anillo |
| Recibe el golpe de Trumpzilla | despiste | tiembla |
| Cae, y 1,5 s después | susto | tiembla |
| Su zanja tiene agua | pánico | tiembla |
| En una zanja | llora (reflexivo) | respira |
| Devora, y 1,2 s después de tragar | ríe (carcajada si es grande) | mastica |
| Aparece | serio | respira |
| Anda por la cara oculta (hacia la luz) | despiste | camina |
| Busca y anda | enfado (furia si es grande) | camina |
| Sin nada que comer | pasmado | respira |
| Quieto | serio (furia si es grande) | respira |

Trumpzilla, en el baile: *ríe* / *carcajada* con la animación *baile*; en su golpe, *furia* (animación *lucha*); si lo recibe, *susto*.

### El shader (comun v99)

`sprite_vertex` y `sprite_pixel` (los de todos los monstruos) suman dos animaciones:

- **9 *baile***: se balancea, se mece a los lados y bota a tiempo.
- **10 *anillo***: se hincha y tiembla; el pixel shader dibuja un anillo azul con luz propia alrededor de la cabeza (centrado en el 74 % del alto de la celda, radio 0,155 del alto) y una onda que se abre. El anillo se ve fuera del dibujo (donde el atlas es transparente) y por delante de la cara.

### Operadores nuevos (en /project1/FASE1)

| Operador | Tipo | Qué es |
|---|---|---|
| `nefanyamuto`, `i_nefanyamuto` | Geometry COMP + Script CHOP | Una lámina (Rectangle SOP 1 × 1) instanciada: la sombra y el sprite, como `trumpzilla` |
| `mat_nefanyamuto` | GLSL MAT | Los shaders de Trumpzilla con el sampler `sAtlas` en `nefanyamuto_atlas`; mismos uniformes (`Pixelsprite`, `Inclinasprite`, `Brillosprite` valen para todos) |
| `nefanyamuto_atlas` | Movie File In TOP | `sprites/nefanyamuto_emociones.png` |

### Parámetros (página Monstruos; en la fase 41 v1, página Fase41)

| Parámetro | Defecto | Qué hace |
|---|---|---|
| `Nefanyamuto` | encendido | NefanyaMuto en el juego; apagado, el juego de la fase 40 |
| `Umbralnefa` | 0,5 | Lo construido de la cara visible (0 a 1) para que aparezca |
| `Tiemposbaile` | 8 | Tiempos del baile antes del golpe |
| `Golpebaile` | azar | Quién lanza el golpe: *al azar*, *Trumpzilla* o *NefanyaMuto* |
| `Radioabsorbe` | 2 | Golpe de Trumpzilla: celdas alrededor de los dos que pasan al mal |
| `Largozanjanefa` | 5 | Golpe de NefanyaMuto: celdas de la zanja |
| `Profzanjanefa` | 3 | Golpe de NefanyaMuto: conchas en lo más hondo |
| `Altonefa` | 0,9 | Alto en celdas, por `tam` (su sprite lleva las patas largas: va algo más alto que Trumpzilla para que se lea igual) |
| `Emocionnefa` | auto | Fija una cara (ensayo) |
| `Simnefa` | pulso | Aparece ya (sin esperar al 50 %) |
| `Simbaile` | pulso | Trumpzilla en `Simceldamon` (si no está) y NefanyaMuto en una vecina: el baile |

### Leyenda

```
NEFANYA  #1  busca  celda 40 -> 52  tam 0.62  acum 5/8   cara enfado
NEFANYA  #0  espera   construido 34 % (aparece con 50 %)
BAILE    5/8 tiempos   celdas 40 | 41   (bailes 1, golpes T 0 / N 0, absorbidas 0)
BAILE    golpe de nefanyamuto   celdas 40 | 41   (bailes 1, golpes T 0 / N 1, absorbidas 0)
BAILE    tregua 9 pasos   (bailes 1, golpes T 0 / N 1, absorbidas 0)
```

---

## Prueba manual

1. `Modojuego` y `Simnefa`: aparece **serio**, va **enfadado** a la construcción más próspera, la devora **riendo** y deja un brote del mal. Sin nada que comer, **pasmado**.
2. `Simbaile`: Trumpzilla y NefanyaMuto en celdas vecinas se acercan al borde y bailan 8 tiempos (ríe y carcajada). Con `Golpebaile` = *Trumpzilla*, las construcciones alrededor pasan al mal; con *NefanyaMuto*, el anillo azul y la zanja de 5 celdas hacia Trumpzilla, que cae. Luego cada uno se va por su lado. La línea `BAILE` cuenta los tiempos, el golpe y la tregua.
3. Sin `Simnefa`: siembra con el público hasta que la cara visible esté construida a la mitad; la línea `NEFANYA` cuenta lo construido y aparece al pasar el 50 %.
4. `Nefanyamuto` apagado: el juego de la fase 40.

## Qué ajustar en sala

- **`Umbralnefa`**: más bajo, sale antes (y el mal tiene dos monstruos desde el principio); más alto, solo cuando el público ya ha construido mucho.
- **`Golpebaile`**: *al azar* para la partida; los fijos, para ensayar cada golpe.
- **`Radioabsorbe`**: el golpe de Trumpzilla es muy duro (con radio 2, hasta 19 celdas por monstruo); con 1, más suave.
- **`Largozanjanefa`** y **`Profzanjanefa`**: la zanja necesita conchas debajo para cavarse; en un mundo joven sale más corta o más somera.

## Pruebas

`python3 pruebas/correr_fases.py` corre las fases 3 a 41 en el TouchDesigner simulado. La autoprueba de la fase 41 (nueve comprobaciones):

- El atlas (doce caras), `nefanyamuto`, `i_nefanyamuto`, `mat_nefanyamuto`, los shaders con el baile y el anillo, y el render.
- Sin NefanyaMuto, o con la cara visible construida por debajo de `Umbralnefa`, la misma partida da lo mismo que tras la fase 40.
- Al 50 % construido aparece (no antes), lejos de Trumpzilla, y va a por una construcción del público.
- Aparece serio, devora riendo y deja un brote del mal; sin nada que comer, pasmado (la cara 11 del atlas).
- Cae en las zanjas del público como Trumpzilla.
- El baile: cara a cara en el borde, ríe y carcajada a cada tiempo, 8 tiempos quietos; el golpe de Trumpzilla absorbe las construcciones a 2 celdas (con su ocupación) y no las de más lejos; se van cada uno a la vecina más lejos del otro; la tregua y el baile siguiente.
- El golpe de NefanyaMuto: furia con el anillo y la zanja de 5 celdas en línea hacia Trumpzilla (1 2 3 2 1 conchas); Trumpzilla cae; NefanyaMuto se va.
- `Golpebaile` al azar: salen los dos golpes y la misma partida da lo mismo.
- `Simbaile`, las líneas `NEFANYA` y `BAILE`, `Nefanyamuto` apagado (acaba el baile) y `Modojuego` apagado.

La partida simulada de `correr_fases.py` (fases 32 a 37) sigue probando a Trumpzilla solo: apaga Godzilla y NefanyaMuto mientras dura.

---

## La página Monstruos y la misma claridad para los tres sprites (24-nov-2026)

| Script | Versión | Comun |
|---|---|---|
| `fase33_monstruo.py`, `fase38_trumpzilla.py`, `fase39_mal.py`, `fase40_godzilla.py`, `fase41_nefanyamuto.py` | v11, v3, v4, v4, v2 | v101 |

**Todos los parámetros de los monstruos, en una página.** La página **Monstruos** de FASE1 junta lo que estaba en las páginas Fase33, Fase38, Fase40 y Fase41, y `Montierra` de la Fase39, en este orden y con un título por sección: *Monstruo: aparición, apetito y pasos (fase 33)*, *Trumpzilla y los sprites (fase 38)*, *Por dónde andan (fase 39)*, *Godzilla (fase 40)* y *NefanyaMuto (fase 41)*. Las armas (Fase37), las zanjas (Fase34) y el rescate (Fase35) se quedan en sus páginas: son del público.

En un proyecto de antes basta con relanzar las fases (o `recargar_todo.py`): cada una saca sus parámetros de su página vieja guardando el valor, la expresión y el modo, los vuelve a crear en Monstruos y les devuelve lo que tenían; las páginas Fase33, Fase38, Fase40 y Fase41, ya vacías, se quitan (`sacar_a_monstruos` y `monstruos_al_dia`, comun v101). Algunas etiquetas dicen ahora de quién son: *Emocion de Trumpzilla*, *Alto de Trumpzilla*, y `Pixelsprite`, `Inclinasprite` y `Brillosprite` *de los sprites* (valen para los tres).

**La misma claridad.** Los tres atlas venían de orígenes distintos y bajo las mismas luces Godzilla se veía claro (luminancia media 99) y NefanyaMuto oscuro (52; Trumpzilla, 65). `sprites/igualar_brillo.py` lleva los tres a la misma luminancia media de lo opaco (72) con una curva de gamma por canal (el negro sigue negro y el blanco blanco) y rehace las láminas de prueba. Los tres `hacer_atlas_*.py` lo llaman antes de guardar, así que un atlas rehecho sale ya igualado. Copia otra vez la carpeta `sprites/` en la de los scripts.

```bash
python3 sprites/igualar_brillo.py
```

La hoja `docs/Estratos_parametros.xlsx` tiene la pestaña nueva **Parámetros Monstruos** (los 45 parámetros y los 5 títulos, con su Nº, qué hacen, la clave y las funciones del motor) y, en «Todos los parámetros», la página Monstruos, las etiquetas nuevas, `Partidalibre` y `Dominio` (Fase32 v3) y los 11 de NefanyaMuto (393 en total).
