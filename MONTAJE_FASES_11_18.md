# Estratos · Montaje
## Fases 11 a 18: la piel temática

*Continúa `MONTAJE_FASES_3_10.md`. Plan de referencia: el doc **Estratos · Plan de fases 11–18**. Las reglas de las fases 1 a 10 siguen valiendo: un script por fase, encima de lo anterior, con su versión en la primera línea del informe y una AUTOPRUEBA al final.*

---

### Estado en una frase

Las formaciones dejan de ser cajas: cada una es un modelo del tema activo (naturaleza o ciudad). Las vecinas que insisten se funden en clusters con puentes y una pieza protagonista, cada formación es un compuesto que sale del mapa logístico, y los cambios de estado se animan en stop-motion al ritmo de los gates.

---

### Archivos

| Archivo | Para qué | Versión |
|---|---|---|
| `estratos_motor.py` | La lógica entera del mundo; desde la v27, también la piel: catálogo de modelos, clusters, compuestos, tránsitos y partículas | `motor v27` |
| `estratos_comun.py` | Piezas compartidas; la v17 mete en el render las geometrías de los modelos (`mod_...`) y las partículas, y sabe instanciar un modelo con un Select SOP | `comun v17` |
| `fase11_piel.py` | La piel: tabla `catalogo`, modelos en `modelos`, una geometría por modelo, partículas, página Fase11 | `fase11 v1` |
| `pruebas/` | TouchDesigner simulado y vista previa del catálogo (solo para probar fuera de TouchDesigner; ver *Cómo se ha probado*) | — |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase11_piel.py').read())
```

Requiere la fase 10. Las fases 3, 4 y 7 cambian solo su autoprueba (`fase3 v12`, `fase4 v7`, `fase7 v10`): sus comprobaciones de cajas siguen valiendo relanzadas en un proyecto que ya está en la fase 11.

---

## FASE 11 · La piel: generadores con temática

### Qué hace

Cada pieza que el motor ya colocaba como caja pasa a ser un modelo del tema activo. `Tema` vale para todo el mundo (decisión: tema por mundo).

| | Naturaleza | Ciudad |
|---|---|---|
| SEQ1 (racimo oblicuo, giros de 30°, puede inclinar) | Vegetación | Ciudad informal |
| SEQ2 (malla ortogonal, giros de 90°, sin inclinar) | Relieve (basalto) | Ciudad planificada |

| Estado (umbrales de la fase 4) | Vegetación | Relieve | Informal | Planificada |
|---|---|---|---|---|
| semilla (1) | brote angular (2 variantes) | columna de basalto (2) | caseta (2) | bloque de una planta (2) |
| crecimiento (2 a `Umbralram` − 1) | tronco y copa | las columnas suben | añadidos oblicuos apilados | apila plantas |
| ramificación (`Umbralram`, 5+) | arboleda; los satélites son arbolitos | mesetas satélite | pasarelas hacia las vecinas | anexos: manzana |
| fusión (`Umbralfusion`, 7+) | bosque, dosel multicelda | meseta continua | barrio denso | podio que une la manzana |
| coronación (`Umbralcorona`, 9+) | árbol madre que rompe el dosel | cumbre escalonada | torre de antenas | rascacielos con aguja |

**Ojo con los números.** El plan habla de ocupación 1, 2–3, 4–5, 6–7 y 8+. Aquí los estados salen de los umbrales que ya tiene el motor (`Umbralram` 5, `Umbralfusion` 7, `Umbralcorona` 9), para que cambiar un umbral cambie también la piel. Con los valores por defecto cada estado empieza una ocupación más tarde que en el plan.

**Híbridos.** La otra especie deja su rastro con su color: árboles que parten la roca (vegetación sobre relieve), bosque sobre terrazas de basalto (relieve sobre vegetación), torre invadida por añadidos (informal sobre planificada) y barrio con plantas rectas impuestas (planificada sobre informal).

### Catálogo y modelos

- **Tabla `catalogo`** (Table DAT, editable): `tema · especie · estado · variante → modelo`. Además de los cinco estados, cada especie tiene `puente`, `protagonista` (tres variantes: 2–3 celdas, 4–6, 7+) e `hibrido`; la planificada, `remate` (la aguja); y la ciudad, las obras (`valla`, `foso`, `andamio`, `grua`). Las cadenas de tránsito van en la misma tabla, con estado `cadena fusion` o `cadena corona` y una etapa por variante.
- Relanzar la fase 11 rehace la tabla solo si nadie la ha tocado; si está editada, se conserva y el informe avisa de los modelos o etapas que no existen (se ignoran). Para volver a la de por defecto, bórrala y relanza.
- **49 modelos**, generados dentro de TouchDesigner en el COMP `modelos`, uno por sub-COMP. Cada pieza de un modelo es un Transform SOP sobre una caja unidad (Box SOP) o un prisma hexagonal unidad (Tube SOP de 6 columnas); el modelo es su Merge, y su salida el Null `salida`.
  - **Vegetación**: un L-system con ángulos cuantizados a 30° (giro y cabeceo de 30°, ramas repartidas a 120°), ramas de caja y copas de prisma hexagonal.
  - **Relieve**: columnas de basalto hexagonales en panal.
  - **Ciudad**: pilas de cajas; la planificada, con losas que sobresalen en cada planta.
- **Por qué no el LSystem SOP.** El plan pedía LSystem SOP para la vegetación. El L-system se calcula en el motor y sale como Transform SOP: así se sabe exactamente qué mide cada árbol (alto 1, base en 0), la autoprueba lo puede comprobar y no depende de cómo escale el LSystem SOP sus ramas. El basalto sí es Tube SOP y la ciudad, Box SOP.
- **La caja y el prisma unidad se miden.** Al construir los modelos, el script lee los puntos de la caja y del prisma y los lleva al cubo unidad centrado (`caja_unidad`, `hexa_unidad`). Si algún parámetro del Tube SOP no se pudo fijar (radio, alto), las piezas no se deforman; el informe lo dice con `..`.
- **Una geometría por modelo, pulida y porosa** (`mod_<modelo>_pul` con `mat_pulido`, `mod_<modelo>_por` con `mat_poroso`): el reparto por velocidad sigue hasta la fase 12. Las obras de la ciudad tienen una sola (`mod_ciu_...`). En total, 94 geometrías: unas 47 por tema. Cada una trae su modelo con un Select SOP desde `modelos/<modelo>/salida` y se instancia desde su Script CHOP `i_mod_...`, como `formas_pulidas`. Las del tema inactivo no reciben instancias.
- **Cómo se apoya un modelo en su celda.** Unos con sus proporciones (árboles, columnas, casetas), escalados con la altura de la formación sin pasar del ancho de la celda; otros con la planta de la celda (mesetas, barrios, manzanas, podios) y el alto de la formación.

### Fusión por vecindad

```
P(c) = ocupación(c) + Pesovecina × Σ ocupación de las vecinas de su especie
```

- Dos vecinas de la misma especie se unen si las dos tienen `P ≥ Umbralvecindad` (union-find). Convive con la fusión por desborde de la fase 4: una formación en fusión (`Umbralfusion`) se une con sus satélites.
- Cuenta como cluster un grupo de `Mincluster` celdas o más.
- **La capital** es la celda más ocupada (sin contar satélites); en empate, la de índice menor.
- **Con los valores por defecto**, `Sembrarzona` dos veces deja la celda y sus vecinas en ocupación 2: P = 2 + 0,5 × (2 + 2 + 2) = 5 ≥ 4 y se funden.

### Multicelda por puentes

- Cada celda del cluster lleva su pieza y **medio puente hacia cada vecina del cluster** unida a ella: los dos medios puentes se encuentran a mitad de camino. La máscara es simétrica (si a va hacia b, b va hacia a). Decisión: puentes, no autotiles.
- Los puentes se apoyan en la menor de las dos formaciones: el **dosel** a media altura de las copas, la **meseta** y el **podio** desde el suelo, la **pasarela** a media altura.
- **La capital lleva la pieza protagonista** según el tamaño del cluster (2–3 celdas, 4–6, 7 o más) cuando su obra de fusión ha terminado. Si está coronada, manda la coronación.

### Compuestos por juego del caos

- Cada formación es un compuesto de piezas: la principal (el modelo del estado) y `mín(ocupación, Maxpiezas)` − 1 piezas más pequeñas (variantes de semilla o de crecimiento).
- Cada pieza nueva sale de la anterior por una operación del kit: **incrustar**, **girar y apilar**, **orbitar** alrededor de la principal, **hundir** o **inclinar** 30°. La malla ortogonal del SEQ2 no inclina (inclinar pasa a apilar), gira de 90 en 90 y coloca las piezas en una rejilla de 1/8 de celda.
- **Sin azar de software.** La operación, el giro, la posición y la variante salen del mapa logístico `x → Caos · x · (1 − x)` (r = 3,91), sembrado con la velocidad fundadora y la celda. La ocupación dice cuántas iteraciones: la misma historia da el mismo compuesto, y crecer solo añade piezas (las de antes no se mueven).
- Nada del compuesto pasa de 1,2 veces la altura de la formación; la coronación, como mucho 1,75 veces más el remate. Todo queda dentro de la altura máxima que encuadra la cámara de globo.

### Tránsitos stop-motion

**La animación no decide.** El estado lógico cambia al instante; lo visible lo persigue a saltos (3 fotos por paso). Un paso dura 60 / (BPM × 4): 125 ms a 120 BPM. (El plan nombraba `Pasospornegra`, que la fase 6 retiró; el motor usa sus 4 pasos por negra de siempre.)

- **Nacimiento**: escala con rebote (`Rebote` 0,2: 0,45 → 1,2 → 0,9 → 1) y destello blanco, en un paso.
- **Crecimiento**: la altura llega a la nueva en un paso, a saltos.
- **Fusión y coronación**: cadenas de etapas. Con `Avance` = gates, cada nota en una celda del cluster (decisión: cualquier nota en cualquiera de sus celdas) adelanta una etapa **la obra del cluster**; una celda que se une a mitad de obra entra en la etapa por la que va. Sin gates en el cluster, la obra se queda a medias. Con `Avance` = pasos, una etapa cada `Pasosetapa` pasos.
- **Hacia atrás**: si la celda deja el cluster (la erosión baja la ocupación) o pierde la corona, la cadena se recorre sola hacia atrás, una etapa cada `Pasosetapa` pasos, con o sin gates.
- **Fin de ciclo**: antes de enterrar, los tránsitos se cierran en su estado final; lo heredado empieza también sin obras a medias.

| Tema | Especie | Fusión | Coronación |
|---|---|---|---|
| Naturaleza | Vegetación | los árboles se **inclinan** hacia la capital → crecen los **puentes** del dosel → los pequeños se **hunden** en la masa → **esporas** | el árbol madre **emerge** del dosel |
| Naturaleza | Relieve | **soldadura** (puentes finos) → **relleno** | **soldadura** (la cumbre a medias) → **relleno** |
| Ciudad | Informal | **soldadura** → **relleno** | **soldadura** → **relleno** |
| Ciudad | Planificada | **solar** vallado → **excavación** con polvo → **obreros** (puntos ámbar) → **andamio**: el podio sube planta a planta | **grúa** → la **fachada** se cierra → **aguja** |

**Partículas.** Esporas (16 pasos tras completar el dosel), polvo y obreros son cajas que calcula el motor, en la geometría `particulas` (material constante). Sus posiciones también salen del mapa logístico y avanzan a saltos.

### Parámetros (página Fase11)

`Tema` naturaleza · `Pesovecina` 0,5 · `Umbralvecindad` 4 · `Mincluster` 2 · `Caos` 3,91 · `Maxpiezas` 6 · `Avance` gates · `Pasosetapa` 2 · `Rebote` 0,2 · `Sembrarzona` (siembra la celda de `Nota` y sus vecinas con el SEQ1) · `Sembrarzona2` (lo mismo con `Nota2` y el SEQ2; no estaba en el plan, sirve para probar las especies del SEQ2 sin el aparato).

### Leyenda

```
TEMA     naturaleza   clusters 3 (max 5)   compuestos 12   piezas 214   obras 2 (1 a medias)
```

`compuestos`: formaciones con más de una pieza. `piezas`: instancias de modelos (piezas, puentes y obras; sin partículas). `obras`: clusters (o formaciones sueltas que se coronan) con algún tránsito pendiente; `a medias`, los que llevan más de un compás sin avanzar.

### Prueba sin BeatStep

1. `Sembrarzona` dos veces con cada `Tema`: la primera solo siembra; la segunda funde la zona en un cluster de 7 celdas (`SEMBRARZONA ... cluster de 7 celdas, capital N` en el Textport), con sus puentes y la protagonista. Lo mismo con `Sembrarzona2` para el relieve y la planificada.
2. `Sembrar` en la misma celda con `Velprueba` 100 y luego 101 (tras `Resetmundo`): dos compuestos distintos. Repetir con 100: el mismo.
3. `Avance` = pasos: la obra termina sola. `Erosionar` sobre un cluster: la obra se deshace hacia atrás.

### Autoprueba

Comprueba: el catálogo completo en los dos temas (estados, puentes, protagonistas, híbridos, obras y cadenas); que cada modelo tenga sus SOP y sus geometrías; que los modelos quepan en su volumen; `Sembrarzona` ×2 en los cuatro casos (cluster de 7, 24 medios puentes, protagonista, nada del otro tema); puentes simétricos; mismo compuesto con la misma semilla y distinto con otra; racimo oblicuo y malla ortogonal; que crecer solo añade piezas; que la obra avanza con cada gate y se deshace al bajar la ocupación; `Avance` = pasos; que el fin de ciclo cierra los tránsitos; el rebote del nacimiento en un paso; la coronación de la planificada (grúa → fachada → aguja); valla, foso y obreros; que ninguna pieza pase de la altura máxima; el Script CHOP de un modelo; la leyenda `TEMA`; y que la caja de la fase 3 ya solo dibuja huellas.

### Rendimiento

- Cada Script CHOP de modelo solo se cocina cuando cambian sus filas: un modelo quieto no cuesta nada.
- Los marcos de cada pieza, los compuestos y los clusters se guardan y no se recalculan en cada fotograma.
- En simulación, con 64 celdas ocupadas, 4 clusters y unas 480 piezas: el motor tarda unos 3,7 ms por fotograma en calcular las instancias (1,6 ms a nivel 10, con la mitad de instancias) y unos 5 ms por fotograma en total, contando los Script CHOP simulados. El tiempo real hay que medirlo en TouchDesigner (fase 18).
- Hasta la fase 12 hay dos geometrías por modelo (pulida y porosa); la fase 12 las reduce a una.

---

### Decisiones tomadas en la fase 11

| Pregunta | Decisión |
|---|---|
| ¿Tema por mundo o mixto? | Por mundo (`Tema`). Cambiarlo cambia la piel al instante; esperar al fin de ciclo es de la fase 15 |
| ¿Multicelda por puentes o autotiles? | Puentes: medio puente de cada celda hacia cada vecina del cluster |
| ¿Qué cuenta como gate en el cluster? | Cualquier nota en una de sus celdas |
| ¿La obra es de cada celda o del cluster? | Del cluster: una celda que se une entra en la etapa por la que va |
| ¿Estados por los números del plan o por los umbrales? | Por los umbrales de la fase 4 (`Umbralram`, `Umbralfusion`, `Umbralcorona`) |
| ¿LSystem SOP? | L-system en el motor, en Transform SOP con ángulos de 30°; basalto con Tube SOP, ciudad con Box SOP |
| ¿Qué siembra el mapa logístico? | Velocidad fundadora y celda; la ocupación da el número de iteraciones |
| ¿Duración de un paso? | 60 / (BPM × 4): `Pasospornegra` ya no existe (fase 6) |
| ¿Cómo se deshace una obra? | Sola, una etapa cada `Pasosetapa` pasos, sin esperar gates |

---

### Cómo se ha probado

Sin TouchDesigner a mano, con un **TouchDesigner simulado** que ejecuta los scripts tal cual (`pruebas/td_simulado.py`): operadores y rutas, parámetros con expresiones, páginas propias, storage, el módulo de los Text DAT, Script CHOP, Table DAT y el tiempo del proyecto. Los COMP solo aceptan los parámetros que tienen en TouchDesigner.

```
python3 pruebas/correr_fases.py        # base y fases 3 a 11 desde cero, sesión, relanzar y otra sesión
python3 pruebas/vista_previa.py        # hoja de contactos del catálogo (pruebas/catalogo.png)
```

- **Desde cero**: `fase12_base.py` y las fases 3 a 11, todas con `AUTOPRUEBA OK`.
- **Sesión simulada** de 16 compases a 120 BPM con SEQ1, SEQ2 y batería por los bytes MIDI, fotograma a fotograma: todas las expresiones de todos los nodos se evalúan sin error.
- **Relanzar** las fases 3 a 11 sobre el proyecto ya en la fase 11: todas OK, el mundo se conserva y otra sesión corre sin errores.
- **Catálogo**: una hoja de contactos dibujada con un rasterizador propio (`pruebas/vista_previa.py`) para ver cada modelo, y escenas de los dos temas con clusters, puentes, coronaciones e híbridos.
- **Medidas**: el arreglo de la caja y el prisma unidad corrige un Tube SOP con el radio por defecto y no toca uno correcto; un catálogo editado se conserva y avisa de los modelos que no existen.

Lo que la simulación no puede comprobar: el aspecto real en el render, los nombres de los parámetros de los SOP (Tube, Transform, Select, Merge) y el tiempo real por fotograma.

### Pruebas pendientes con el aparato

1. **Los modelos en TouchDesigner**: abrir `modelos` y mirar un árbol, una columna y un bloque. Si un modelo sale deformado o vacío, mirar las líneas `..` del informe (parámetros del Tube SOP, del Select SOP o del Merge) y pegármelas.
2. **El prisma hexagonal**: `modelos/rel_columna/hexa` tiene que ser un prisma de 6 caras, de pie (eje Y), con tapas.
3. **Escala**: con la cámara de globo, comprobar que los árboles y las torres se leen a distancia y que los puentes no tapan las formaciones. Si sobran o faltan, se ajustan en `PUENTE` del motor.
4. **Rendimiento**: con SEQ1, SEQ2 y batería, mirar los fotogramas con 400–500 piezas.
5. **Obras a medias**: con `Avance` = gates, un cluster que deja de sonar se queda a medias; comprobar que se lee como obra parada y no como fallo.

### Problemas frecuentes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Las formaciones desaparecen al aplicar la fase 11 | Las geometrías `mod_...` no están en el render | Relanza la fase 11 (o cualquier fase): `set_render` las añade. Mira la línea `render dibuja: ... y 94 geometrias de modelos` |
| Un modelo sale vacío | El Select SOP de su geometría no apunta a `modelos/<modelo>/salida` | El informe avisa con `..`; pon la ruta a mano en el parámetro SOP del Select SOP `modelo` |
| Los prismas salen redondos o enormes | El Tube SOP no aceptó columnas o radio | `hexa_unidad` corrige el tamaño; las columnas, a mano en `hexa` (Columns = 6) |
| Las piezas salen tumbadas | Orden de rotación de las instancias | En la geometría `mod_...`: Instance → Rotate Order = `Rx Ry Rz` (lo fija el script) |
| Todo de un color | Color por instancia sin enlazar | Relanza cualquier fase; si persiste, Instance 2 → Color R/G/B = `r g b`, Color Mode = Replace |
| La obra no avanza | `Avance` = gates y no suena ninguna nota en el cluster | Es lo esperado; con `Avance` = pasos avanza sola |
| `catalogo editado a mano: se conserva` | La tabla no es la de por defecto | Si no la has tocado tú, bórrala y relanza la fase 11 |
