# Estratos · Montaje
## Fases 11 a 18: la piel temática

*Continúa `MONTAJE_FASES_3_10.md`. Plan de referencia: el doc **Estratos · Plan de fases 11–18**. Las reglas de las fases 1 a 10 siguen valiendo: un script por fase, encima de lo anterior, con su versión en la primera línea del informe y una AUTOPRUEBA al final.*

---

### Estado en una frase

Las formaciones dejan de ser cajas: cada una es un modelo del tema activo (naturaleza o ciudad). Las vecinas que insisten se funden en clusters con puentes y una pieza protagonista, cada formación es un compuesto que sale del mapa logístico, y los cambios de estado se animan en stop-motion al ritmo de los gates. Desde la fase 12, la velocidad decide el material (obsidiana o pómez, vidrio negro u hormigón) y la duración del gate, el vigor de los árboles o las plantas de cada edificio.

---

### Archivos

| Archivo | Para qué | Versión |
|---|---|---|
| `estratos_motor.py` | La lógica entera del mundo; desde la v27, también la piel: catálogo de modelos, clusters, compuestos, tránsitos y partículas; la v28, los moduladores de la fase 12; la v29, ríos y carreteras; la v30, el color de las luces para el shader (`luz_color`) | `motor v30` |
| `estratos_comun.py` | Piezas compartidas; la v17 mete en el render las geometrías de los modelos (`mod_...`) y las partículas, y sabe instanciar un modelo con un Select SOP; la v18 trae el shader de la piel y crea las geometrías de los modelos para el nivel en que esté el proyecto; la v19 mete el `tejido` en el render; la v20 corrige el color de las luces de los uniformes del shader; la v21 añade `nombre_op` | `comun v21` |
| `fase11_piel.py` | La piel: tabla `catalogo`, modelos en `modelos`, geometrías de los modelos, partículas, página Fase11 (v2: relanzable en la fase 12) | `fase11 v2` |
| `fase12_moduladores.py` | Velocidad → material (shader de la piel, una geometría por modelo), gate → vigor y plantas, página Fase12. No confundir con `fase12_base.py` (fases 1 y 2). v2: comprueba que los uniformes se evalúan; v3: la autoprueba compara el material por su nombre (en TouchDesigner, `material` devuelve el operador) | `fase12 v3` |
| `fase13_tejido.py` | Ríos (naturaleza) y carreteras (ciudad), geometría `tejido`, página Fase13 | `fase13 v1` |
| `pruebas/` | TouchDesigner simulado, vista previa del catálogo y comprobación del shader con OpenGL (solo para probar fuera de TouchDesigner; ver *Cómo se ha probado*) | — |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase11_piel.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase12_moduladores.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase13_tejido.py').read())
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

## FASE 12 · Moduladores: velocidad y duración del gate

### Qué hace

Las dos señales que ya modulaban las cajas pasan a modular los modelos temáticos, y el material deja de necesitar geometrías duplicadas. La velocidad sigue sembrando el caos de la fase 11: eso no cambia.

### Un material por modelo

- **Una geometría por modelo**: de 94 a 49 (`mod_<modelo>`; las obras de la ciudad ya tenían una).
- **Shader de la piel**: un GLSL MAT por familia de material, con los mismos shaders (`piel_vertex`, `piel_pixel`):
  - `mat_piel_mineral`: naturaleza, obsidiana ↔ piedra pómez;
  - `mat_piel_dosel`: el dosel, vidrio ahumado con vetas ámbar;
  - `mat_piel_ciudad`: vidrio negro ↔ hormigón brutalista, con ventanas ámbar que se quedan apagadas hasta la fase 17 (`uVentanas`).
  
  Las obras de la ciudad (valla, foso, andamio, grúa) siguen con `mat_poroso`.
- **La rugosidad va en el canal `a`** (el alfa del color de cada instancia: Instance 2 → Color A = `a`). Cada Script CHOP de modelo tiene un canal más. El shader la lee:
  - pulido: reflejo fino y fuerte, y un reflejo de borde frío;
  - rugoso: mate y con poros (manchas de ruido en el espacio del modelo, distintas en cada instancia).
- **El color** también se acerca al material: el de la especie se mezcla con obsidiana o pómez (naturaleza) o con vidrio negro u hormigón (ciudad), según la rugosidad. Así, pulido y rugoso se distinguen también con el material de respaldo.
- **Luces**: el shader no usa las funciones de iluminación de TouchDesigner. Lee como uniformes la posición y el color × dimmer de `luz_principal`, `luz_relleno` y `luz_destello` (página Vectors del GLSL MAT, con expresiones), más un ambiente. El color lo da el motor (`luz_color`), que prueba los nombres del color de la Light COMP (`cr cg cb`).
- **Corregido en comun v20**: la primera versión leía el color de las luces como `lightcolorr/g/b`, que la Light COMP no tiene, y los tres `mat_piel_*` daban `tdAttributeError: 'td.ParCollection' object has no attribute 'lightcolorr'`. Relanza `fase12_moduladores.py` (o la 13) para arreglarlo.

### Velocidad → material

```
continuo (por defecto): rugosidad = Rugmax + (Rugmin − Rugmax) × velocidad / 127
binario:                rugosidad = Rugmin desde Umbralvel (64), Rugmax por debajo
```

Con `Rugmin` 0,05 y `Rugmax` 0,85: velocidad 97 → 0,24; 10 → 0,79; 120 → 0,09. Decisión: continuo.

### Duración del gate → vigor

El gate se mide al soltar la nota, en pasos (60 / (BPM × 4)).

- **Naturaleza**: vigor = 0,6 + 0,8 × gate, entre 0,6 y `Vigormax` (1,5). Gate normal (medio paso) = 1; corto (¼ de paso) = 0,8; ligado (un paso o más) = 1,4 a 1,5. El vigor de cada formación persigue el de sus gates (media con el anterior) y ensancha el tronco y la copa (los modelos de proporciones propias, y la planta de los de celda), sus piezas pequeñas incluidas. Con vigor, una copa puede pasar un poco del ancho de su celda.
- **Ciudad**: plantas por señal. Un gate corto o normal construye una; un gate **ligado** (un paso o más) construye `Plantasligado` (2): la nota cuenta como `Plantasligado` notas de construcción, con la misma velocidad. El gate de la fase 3 (cuánto sube cada nota) sigue igual.

### Materialrespaldo

El shader es lo único que la simulación de TouchDesigner no puede ejecutar. Si la piel no se ve o sale negra, `Materialrespaldo` cambia **en vivo** todas las geometrías de modelos a un Phong (`mat_respaldo`) y pone el alfa a 1. No hace falta relanzar nada.

*Diferencia con el plan*: el plan decía «vuelve a las geometrías duplicadas». Con una sola geometría por modelo y el color ya acercado al material, el Phong distingue pulido y rugoso por el color. El cambio es inmediato y no hace falta mantener 94 geometrías por si acaso.

### Probar sin BeatStep

Los botones de prueba (`Sembrar`, `Sembrar2`, `Sembrarzona`, `Sembrarzona2`) sueltan ahora la nota tras `Gateprueba` pasos (0,5: un gate normal), así que modulan igual que el aparato.

1. `Resetmundo`, `Velprueba` 10 y `Sembrar` varias veces: piedra pómez (o hormigón). `Resetmundo`, `Velprueba` 120: obsidiana (o vidrio negro).
2. `Gateprueba` 0,25, 1 y 2 con `Tema` naturaleza: árboles cada vez más gruesos y anchos.
3. `Tema` ciudad, `Gateprueba` 2 y `Sembrar2`: cada pulsación sube dos plantas (`2 plantas` en la leyenda).
4. Si no se ve la piel: `Materialrespaldo`, y mándame los errores de `mat_piel_mineral` (clic derecho → Info).

### Parámetros (página Fase12)

`Materialmodo` continuo · `Rugmin` 0,05 · `Rugmax` 0,85 · `Vigormax` 1,5 · `Plantasligado` 2 · `Gateprueba` 0,5 (pasos) · `Materialrespaldo` (apagado)

### Leyenda

```
MOD      vel 97 -> rugosidad 0.24   gate 1.60 -> 2 plantas   continuo
MOD      vel 97 -> rugosidad 0.24   gate 1.60 -> vigor 1.49   continuo
```

Velocidad y rugosidad de la última nota, y el gate y su efecto al soltarla. Con `Materialrespaldo` añade `RESPALDO (Phong)`.

### Autoprueba

Comprueba: una geometría por modelo (49) sin las duplicadas; que cada una lee el canal `a` y usa el shader de su familia; los shaders y los tres GLSL MAT; velocidad 10 rugosa y clara, 120 pulida y oscura, por el camino de `Sembrar`; el modo binario; el canal `a` en las filas; el vigor y la anchura crecientes con `Gateprueba` 0,25, 1 y 2; las 2 plantas por gate ligado en la ciudad; que la velocidad sigue sembrando el caos; `Materialrespaldo` en vivo (Phong y alfa 1) y la vuelta al shader; el canal `a` en el Script CHOP; y la leyenda `MOD` (vel 97 → 0.24, gate 1.60).

### Rendimiento

La mitad de geometrías y de Script CHOP que en la fase 11. En simulación, con unas 480 piezas, el motor tarda unos 3,3 ms por fotograma en calcular las instancias y unos 4,5 ms en total.

---

## FASE 13 · Tejido conectivo: ríos y carreteras

### Qué hace

Une las formaciones con algo que ninguna señal pide: el sistema lo deduce del estado. Es la fase en la que el tema se lee de lejos.

- **Ríos (naturaleza).**
  - Nacen en la capital de cada cluster de relieve.
  - Bajan celda a celda hacia la vecina menos ocupada (en empate, la de índice menor), sin volver por donde han pasado.
  - Acaban al llegar a una celda vacía (la desembocadura), al llegar a otro río (confluyen), tras `Maxrio` tramos o si no les queda vecina libre.
  - Se trazan por orden de capital. Un río que llega a otro acaba ahí, y aguas abajo de la confluencia el río que lo recibe se ensancha: ancho = `Grosorvia` × (0,7 + 0,3 × ríos que pasan por el tramo).
- **Carreteras (ciudad).**
  - Los nodos son las capitales de los clusters y las formaciones sueltas (sin cluster ni satélites) con ocupación de `Minvia` o más.
  - La distancia entre dos nodos es el número de saltos por la retícula. Kruskal elige el árbol de expansión mínima (en empate, por los índices).
  - Cada arista se dibuja por el camino más corto de la retícula. Los tramos compartidos se dibujan una vez.
- **Los tramos** van de centro a centro de celda, a ras del suelo de cada celda (6 milésimas por encima), en dos medios tramos que siguen la curva del planeta. Pasan por debajo de las formaciones que cruzan.
- **La geometría `tejido`** es la caja instanciada de siempre, con el shader de la piel: el agua (azul profundo, fuera de la banda del cian) brilla, el asfalto es mate. `Materialrespaldo` también la cambia a Phong. Se dibuja justo encima de las conchas.
- **Se recalcula solo cuando cambia la ocupación** (las especies o los satélites); si no, se reutiliza. Las filas sí se rehacen en cada fotograma, porque el suelo cambia con las conchas y los cortes.

### Parámetros (página Fase13)

`Rios` (encendido) · `Carreteras` (encendido) · `Minvia` 2 · `Grosorvia` 0,18 · `Maxrio` 12 (tramos)

### Leyenda

```
TEJIDO   rios 2 (9 tramos)   carreteras 7 tramos
```

### Probar sin BeatStep

1. `Tema` ciudad. Pon `Nota` 64 y pulsa `Sembrarzona` dos veces; pon `Nota` 70 (el meridiano opuesto) y pulsa otras dos. Aparece la carretera que une las dos capitales. Con `Sembrar` en una nota suelta (3 veces, para llegar a `Minvia`) la red se rehace y la incluye.
2. `Tema` naturaleza. `Sembrarzona2` dos veces y `Sembrar2` una docena de veces en el centro (`Nota2`): el río baja de la cumbre hasta la primera celda vacía. Dos zonas cercanas pueden dar dos ríos que confluyen.

Con zonas de 7 celdas los ríos son cortos: acaban en cuanto encuentran una celda vacía. Se alargan cuando el relieve queda rodeado de territorio ocupado.

### Autoprueba

Comprueba:
- **Carreteras:**
  - dos zonas en la ciudad quedan unidas por el camino más corto;
  - una formación suelta entra en la red y el árbol tiene nodos − 1 aristas;
  - el cálculo se reutiliza si la ocupación no cambia;
  - el árbol es el de menor longitud total, comparado con todos los demás posibles;
  - `Carreteras` apagado quita las carreteras.
- **Ríos:**
  - el río nace en la capital del relieve y en cada paso baja a la vecina menos ocupada;
  - acaba en una celda vacía, en otro río o al tope de longitud;
  - en una confluencia suma el caudal aguas abajo;
  - `Maxrio` corta la longitud y `Rios` apagado los quita.
- **Dibujo:** los tramos van a ras del suelo, `i_tejido` recibe las filas con el canal `a`, y la leyenda tiene la línea `TEJIDO`.

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

### Decisiones tomadas en la fase 12

| Pregunta | Decisión |
|---|---|
| ¿Material binario o continuo? | Continuo (`Materialmodo`); binario como antes, con `Umbralvel` |
| ¿Por dónde llega la rugosidad al shader? | Por el alfa del color de cada instancia (canal `a`): no hace falta ningún atributo personalizado |
| ¿Qué hace `Materialrespaldo`? | Cambia en vivo el material de todas las geometrías a un Phong, sin duplicarlas |
| ¿Qué es un gate ligado? | Un gate de un paso o más |
| ¿Cómo da plantas la ciudad? | La nota ligada cuenta como `Plantasligado` notas de construcción |
| ¿Cómo da vigor la naturaleza? | Ensancha tronco y copa (escala horizontal), con media entre el vigor de la formación y el de cada gate |

---

### Decisiones tomadas en la fase 13

| Pregunta | Decisión |
|---|---|
| ¿Tramos por centros o por bordes de celda? | Centros, a ras del suelo, en dos medios tramos que siguen la curva |
| ¿Dónde nace un río? | En la capital de cada cluster de relieve (la más ocupada) |
| ¿Empates al bajar? | La vecina de índice menor |
| ¿Qué es una formación suelta? | Una formación (no satélite) que no está en ningún cluster |
| ¿Distancia de Kruskal? | Saltos por la retícula (camino más corto) |
| ¿Ríos en la ciudad o carreteras en la naturaleza? | No: cada tema tiene su tejido |

---

### Cómo se ha probado

Sin TouchDesigner a mano, con un **TouchDesigner simulado** que ejecuta los scripts tal cual (`pruebas/td_simulado.py`): operadores y rutas, parámetros con expresiones, páginas propias, storage, el módulo de los Text DAT, Script CHOP, Table DAT y el tiempo del proyecto. Los COMP solo aceptan los parámetros que tienen en TouchDesigner.

```
python3 pruebas/correr_fases.py        # base y fases 3 a 13 desde cero, sesión, relanzar y otra sesión
python3 pruebas/vista_previa.py        # hoja de contactos del catálogo (pruebas/catalogo.png)
xvfb-run -a python3 pruebas/glsl_piel.py   # compila y dibuja el shader de la piel con OpenGL (necesita moderngl)
```

- **Desde cero**: `fase12_base.py` y las fases 3 a 13, todas con `AUTOPRUEBA OK`.
- **Sesión simulada** de 16 compases a 120 BPM con SEQ1, SEQ2 y batería por los bytes MIDI, fotograma a fotograma: todas las expresiones de todos los nodos se evalúan sin error.
- **Relanzar** las fases 3 a 13 sobre el proyecto ya en la última (también la 11, que crea las geometrías del nivel en que esté): todas OK, el mundo se conserva y otra sesión corre sin errores.
- **El shader de la piel** (fase 12): se compila con un OpenGL 4.5 de verdad (Mesa, sin pantalla, con Xvfb), sustituyendo las funciones de TouchDesigner (`TDDeform`, `TDInstanceColor`, `uTDMats`...) por otras equivalentes. Se dibuja con las instancias reales del motor: obsidiana y vidrio negro pulidos a velocidad alta, pómez y hormigón con poros a velocidad baja, dosel ahumado con vetas ámbar.
- **Catálogo**: una hoja de contactos dibujada con un rasterizador propio (`pruebas/vista_previa.py`) para ver cada modelo, y escenas de los dos temas con clusters, puentes, coronaciones e híbridos.
- **Medidas**: el arreglo de la caja y el prisma unidad corrige un Tube SOP con el radio por defecto y no toca uno correcto; un catálogo editado se conserva y avisa de los modelos que no existen.

Lo que la simulación no puede comprobar: el aspecto real en el render, los nombres de los parámetros de los SOP (Tube, Transform, Select, Merge) y del GLSL MAT (Vertex/Pixel Shader, página Vectors), que TouchDesigner declare sus funciones de shader como las imitamos, y el tiempo real por fotograma.

### Pruebas pendientes con el aparato

1. **Los modelos en TouchDesigner**: abrir `modelos` y mirar un árbol, una columna y un bloque. Si un modelo sale deformado o vacío, mirar las líneas `..` del informe (parámetros del Tube SOP, del Select SOP o del Merge) y pegármelas.
2. **El prisma hexagonal**: `modelos/rel_columna/hexa` tiene que ser un prisma de 6 caras, de pie (eje Y), con tapas.
3. **Escala**: con la cámara de globo, comprobar que los árboles y las torres se leen a distancia y que los puentes no tapan las formaciones. Si sobran o faltan, se ajustan en `PUENTE` del motor.
4. **Rendimiento**: con SEQ1, SEQ2 y batería, mirar los fotogramas con 400–500 piezas.
5. **Obras a medias**: con `Avance` = gates, un cluster que deja de sonar se queda a medias; comprobar que se lee como obra parada y no como fallo.
6. **El shader (fase 12)**: que `mat_piel_mineral`, `mat_piel_dosel` y `mat_piel_ciudad` compilan sin errores (clic derecho → Info) y que la página Vectors tiene `uFamilia`, `uLuz0`... con valores. Si no, `Materialrespaldo` y pegarme los errores.
7. **Pulido y rugoso**: con la cámara de globo, que la obsidiana y la pómez (y el vidrio y el hormigón) se distinguen; si no, ajustar `Rugmin` y `Rugmax`.
8. **Ríos y carreteras (fase 13)**: con varias conchas, que se leen desde la cámara de globo sobre los colores de las conchas; si no, subir `Grosorvia`.

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
| Fase 12: los modelos salen negros, blancos o no se ven | El shader no compila o no recibe sus uniformes | `Materialrespaldo` (Phong, en vivo) y pégame los errores de `mat_piel_mineral` |
| `mat_piel_...`: `no attribute 'lightcolorr'` | Uniformes de la primera versión (comun v18/v19) | Relanza `fase12_moduladores.py` con comun v20 o posterior |
| Fase 12: pulido y rugoso iguales | La geometría no lee el canal `a` | En la geometría `mod_...`: Instance 2 → Color A = `a`. El informe lo avisa con `FALLO ... no lee la rugosidad` |
| Fase 12: el gate no cambia nada | Sin note off (el aparato no lo envía) o `Gateprueba` en los botones | Mira la línea `MOD`: sin `gate` es que no llega el note off |
