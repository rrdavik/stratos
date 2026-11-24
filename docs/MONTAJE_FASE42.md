# Estratos · Montaje
## Fase 42: el Godzilla azul, el segundo monstruo del bien

*Continúa `MONTAJE_FASE41.md`. Con Trumpzilla y NefanyaMuto a la vez en el planeta, el mal hacía mucho daño: el Godzilla verde solo puede con uno (pelea con Trumpzilla) y NefanyaMuto sembraba el mal sin nadie que lo parase. Esta fase pone **otro Godzilla, azul**, que lucha por el bien y tiene por rival a NefanyaMuto.*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 42 | `fase42_godzilla_azul.py` | El Godzilla azul (sale con los dos monstruos del mal a la vez, devora el mal, crea) y su lucha con NefanyaMuto | v146 | v102 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase42_godzilla_azul.py').read())
```

**Antes de lanzarla:** copia la carpeta `sprites/` del repositorio dentro de la carpeta de los scripts (`C:/Users/DareDave/Downloads/est/sprites/godzilla_azul_emociones.png`). Si falta, el informe dice `FALLO godzilla_azul_atlas: no encuentro ...`.

También cambia `estratos_comun.py` (v102): `SalaJuego` apaga `Godzillaazul` en las autopruebas de las fases 32 a 41 (salvo que se pida) y `guardar_sala` lo devuelve como estaba.

---

## Qué hace

**Cuándo sale.** Solo mientras **Trumpzilla y NefanyaMuto están los dos en pie a la vez** (ni esperando ni ahogados), con o sin gente en la sala. Si queda uno solo (o ninguno), **se va**: saluda con la flor (cara *calma*), se mece y se hunde en 2 s. Vuelve cuando vuelven a estar los dos, como pronto `Esperamonstruo` s después de irse.

**Aparece** en la celda vacía de la cara visible más cercana al borde por el que entran las celdas con el giro, lejos de los otros tres monstruos (ni sus celdas ni sus vecinas). En tierra.

**Devora el mal y crea** con las reglas del Godzilla verde: va a la celda del mal de mayor `occ / (1 + coste)`, la devora al mismo ritmo, anda al mismo paso, crece igual y solo por tierra. La celda del mal que vacía recibe un **brote de la creación**. Nunca come lo del público.

### La lucha con NefanyaMuto

Si el Godzilla azul y NefanyaMuto quedan en **celdas contiguas** (o en la misma), fuera de su tregua, la lucha de la fase 40:

1. Se acercan al borde mirándose.
2. **Manotazos** durante `Pasoslucha` pasos (8): uno da (*furia*), el otro recibe (*mueca*), por turnos.
3. Cada uno vuelve a la celda de la que venía.
4. **Tregua** de `Tregua` pasos (16) sin cruzarse ni volver a pelear.

El Godzilla verde sigue peleando con Trumpzilla, y Trumpzilla y NefanyaMuto siguen bailando entre ellos: así cada monstruo del mal tiene quien lo pare. Si NefanyaMuto deja de luchar a mitad (se ahoga o cae en una zanja) o el azul se va, la lucha se acaba.

### Las caras

`sprites/godzilla_azul_emociones.png`: el mismo dibujo y las mismas diez caras que el Godzilla verde, con otra paleta: **piel azul cobalto, tripa gris perla y placas de hielo cian** (casi blancas en la furia). Mismo formato (768 × 768, 4 × 3 celdas de 192 × 256) y mismo shader. Las caras salen como las del verde (*serio* al aparecer, *enfado* al buscar, *ríe* al crear, *calma* sin mal y al irse, *furia*/*mueca* en la lucha). NefanyaMuto, en esta lucha, *furia* cuando da y *mueca* cuando recibe, como Trumpzilla.

**Rehacerlo:**

```bash
python3 sprites/hacer_atlas_godzilla_azul.py
```

`sprites/igualar_brillo.py` también lo iguala (la misma claridad que los otros tres).

### Operadores nuevos (en /project1/FASE1)

| Operador | Tipo | Qué es |
|---|---|---|
| `godzilla_azul`, `i_godzilla_azul` | Geometry COMP + Script CHOP | Una lámina instanciada: la sombra y el sprite |
| `mat_godzilla_azul` | GLSL MAT | Los shaders de Trumpzilla con el sampler `sAtlas` en `godzilla_azul_atlas` |
| `godzilla_azul_atlas` | Movie File In TOP | `sprites/godzilla_azul_emociones.png` |

### Parámetros (página Monstruos, sección *Godzilla azul (fase 42)*)

| Parámetro | Defecto | Qué hace |
|---|---|---|
| `Godzillaazul` | encendido | El Godzilla azul en el juego; apagado, el juego de la fase 41 |
| `Altoazul` | 0,8 | Alto en celdas, por `tam` |
| `Emocionazul` | auto | Fija una cara (ensayo) |
| `Simazul` | pulso | Aparece ya (si no están los dos del mal, se va enseguida) |
| `Simluchaazul` | pulso | Trumpzilla en `Simceldamon`, NefanyaMuto lejos de él y el azul junto a NefanyaMuto: su lucha |

`Pasoslucha` y `Tregua` son los de la fase 40 (valen para las dos luchas).

### Leyenda

```
AZUL     #1  devora  celda 12 -> 12  tam 0.75  acum 4/8   cara rie   luchas 1
AZUL     #1  lucha  celda 40 -> -  tam 0.50  acum 0/8   cara furia   lucha 3/8 pasos con NefanyaMuto
AZUL     #0  espera   del mal en pie 1 (aparece con 2)   luchas 0
```

---

## Prueba manual

1. `Modojuego` y `Simluchaazul`: Trumpzilla, NefanyaMuto y el Godzilla azul junto a NefanyaMuto; se dan manotazos 8 pasos y cada uno se va por donde vino.
2. En partida: cuando NefanyaMuto aparece (al 50 % construido) con Trumpzilla en el planeta, sale el azul y va a por el mal. Si uno de los dos del mal se ahoga, el azul saluda y se va.
3. `Godzillaazul` apagado: el juego de la fase 41.

## Pruebas

`python3 pruebas/correr_fases.py` corre las fases 3 a 42 en el TouchDesigner simulado. La autoprueba de la fase 42 (seis comprobaciones): el atlas y los operadores; con un solo monstruo del mal (o apagado) la partida da lo mismo que tras la fase 41; aparece solo con los dos del mal, lejos de ellos, y se va si queda uno; devora el mal y crea; la lucha con NefanyaMuto, la tregua y la siguiente; `Simluchaazul`, `Simazul`, la leyenda y los apagados.
