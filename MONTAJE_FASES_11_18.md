# Estratos · Montaje
## Fases 11 a 18: la piel temática

*Continúa `MONTAJE_FASES_3_10.md`. Plan de referencia: el doc **Estratos · Plan de fases 11–18**. Las reglas de las fases 1 a 10 siguen valiendo: un script por fase, encima de lo anterior, con su versión en la primera línea del informe y una AUTOPRUEBA al final.*

---

### Estado en una frase

Las formaciones dejan de ser cajas: cada una es un modelo del tema activo (naturaleza o ciudad). Desde la fase 14, los arañazos de la batería también tienen forma temática y escalan en catástrofes; desde la 15, cada ciclo se entierra con la materia de su tema y la herencia rebrota según su lógica; desde la 16, los cortes enseñan lo que hubo en cada concha (troncos fósiles, basalto, cimientos, sótanos y calles) y dos cortes vecinos se unen en un cañón o una galería de metro; desde la 17, el tiempo se ve en el paisaje: el dosel se balancea y el tráfico corre al tempo, STOP lo congela y un cambio de pattern cruza el planeta como un frente que trae la estación de ese pattern; la 18 cierra las dos escenas (naturaleza y ciudad) como presets listos para actuar, con luz local sin luces nuevas y capas de diagnóstico que el modo actuación oculta. La 19, ya fuera del plan 11–18, añade las señales del modular: viento, ventanas que respiran, esporas, smog, niebla de distancia y glitch. Las vecinas que insisten se funden en clusters con puentes y una pieza protagonista, cada formación es un compuesto que sale del mapa logístico, y los cambios de estado se animan en stop-motion al ritmo de los gates. Desde la fase 12, la velocidad decide el material (obsidiana o pómez en el relieve, hoja cerosa o musgo seco en la vegetación, vidrio negro u hormigón en la ciudad) y la duración del gate, el vigor de los árboles o las plantas de cada edificio. Desde la fase 11 v5 la naturaleza se lee por masa, silueta y bandas de color: el bosque crece hasta un monte boscoso, el relieve es una sola malla con cordilleras y cumbres nevadas, el color sale de los pisos de altitud (ya no de la concha ni del secuenciador, cuyo tinte va al borde) y, desde la fase 13 v2, los ríos bajan azules por el suelo real.

---

### Archivos

| Archivo | Para qué | Versión |
|---|---|---|
| `estratos_motor.py` | La lógica entera del mundo; desde la v27, también la piel: catálogo de modelos, clusters, compuestos, tránsitos y partículas; la v28, los moduladores de la fase 12; la v29, ríos y carreteras; la v30, el color de las luces para el shader (`luz_color`); la v31, el aspecto de la cámara sin bucle de cocinado; la v32, el material vegetal en toda la vegetación y el dosel cerrado; la v33, el encuadre cercano de la cámara y medios puentes sin parpadeo; la v34, los destructores de la fase 14; la v35, el ciclo como era (fase 15); la v36, un solo parámetro de encuadre (`Encuadre`); la v37, la compactación de las conchas (`Cortezamax`) y los valores calibrados (ver *Calibración de la vista*); la v38, la arqueología temática de la fase 16; la v39, el tiempo en el paisaje (fase 17); la v40, escenas, luz local y diagnóstico (fase 18); la v41, las señales del modular (fase 19); la v42, el rango -10..10 V; la v43, el impulso del bombo y el tom (fase 7 v12, ver `MONTAJE_FASES_3_10.md`); la v44, su pumping en seco (fase 7 v13); la v45, sus pulsos de ocupación (fase 7 v14); la v46, la naturaleza legible (fase 11 v5: monte boscoso, relieve en un mapa de alturas, dosel por colonización del espacio, pisos de color, tinte al borde) y los ríos azules (fase 13 v2) | `motor v46` |
| `estratos_comun.py` | Piezas compartidas; la v17 mete en el render las geometrías de los modelos (`mod_...`) y las partículas, y sabe instanciar un modelo con un Select SOP; la v18 trae el shader de la piel y crea las geometrías de los modelos para el nivel en que esté el proyecto; la v19 mete el `tejido` en el render; la v20 corrige el color de las luces de los uniformes del shader; la v21 añade `nombre_op`; la v22 gira las marcas de la retícula desde el motor; la v23, shader vegetal y `piel_al_dia` (al relanzar cualquier fase, cada geometría de modelo toma el material de su familia); la v24 añade `Holguraaltura`; la v25 trae de la fase 11 la construcción de los modelos (`construir_modelos`) y el catálogo (`catalogo_al_dia`), para que la fase 14 añada los suyos; la v26 pone a las conchas el shader de la piel desde la fase 15 (`conchas_al_dia`); la v27 sustituye `Encuadremargen` y `Holguraaltura` por `Encuadre` (`camara_al_dia`); la v28 pone a cero el giro y el pivote de la cámara al relanzar (`camara_neutra`); la v29, la calibración de la vista (`calibracion_al_dia`: valores nuevos donde seguían por defecto, `Cortezamax` y el aviso de alturas con salto); la v30, las ventanas de la ciudad por edificio en el shader, el color de `luz_principal` desde el motor (`tiempo_al_dia`) y parámetros de texto; la v31, `luz_local` y `diagnostico` en el render y `Escena` en los pulsos; la v32, niebla de distancia y glitch en el shader de la piel (`uNiebla`, `uNieblaCol`, `uGlitch`) y la niebla de la cámara (`modular_al_dia`); la v33, el terreno (`terreno_al_dia`, `mapas_terreno`: Script TOP `alturas`, Ramp TOP `rampa_hipso`), bolas y conos en los modelos, y en el shader las familias tierra y agua, los pisos, el sombreado rasante y el borde tintado | `comun v33` |
| `fase11_piel.py` | La piel: tabla `catalogo`, modelos en `modelos`, geometrías de los modelos, partículas, página Fase11 (v2: relanzable en la fase 12; v3: la autoprueba cuenta los huecos del dosel; v4: usa `construir_modelos` y `catalogo_al_dia` de comun; v5: la naturaleza legible) | `fase11 v5` |
| `fase12_moduladores.py` | Velocidad → material (shader de la piel, una geometría por modelo), gate → vigor y plantas, página Fase12. No confundir con `fase12_base.py` (fases 1 y 2). v2: comprueba que los uniformes se evalúan; v3: la autoprueba compara el material por su nombre (en TouchDesigner, `material` devuelve el operador); v4: autoprueba del material vegetal; v5: solo la autoprueba (la naturaleza toma el color de los pisos y el relieve es la malla) | `fase12 v5` |
| `fase13_tejido.py` | Ríos (naturaleza) y carreteras (ciudad), geometrías `tejido` y (v2) `rios`, página Fase13 (v2: ríos azules por el suelo real, lagos) | `fase13 v2` |
| `fase14_destructores.py` | Arañazos temáticos y escalada: accidentes, incendio y derrumbes, huellas, derribo de obras, página Fase14 (v2: un pad de impulso no es arañazo) | `fase14 v2` |
| `fase15_era.py` | El ciclo como era: entierro temático, registro de cada concha, herencia (banco de semillas y trazas), tema por ciclo, página Fase15 (v2: la autoprueba no depende de la `Herencia` del proyecto) | `fase15 v2` |
| `fase16_cortes.py` | Arqueología temática: lo que enseñan los cortes (fondo y paredes), unión de cortes (cañón y galería de metro), página Fase16 (v2: solo cambia el texto; corta la caja) | `fase16 v2` |
| `fase17_tiempo.py` | Tiempo: pulso en fase con el beat (dosel, esporas, tráfico, ventanas), transporte, frente de cambio de pattern y biblioteca de patterns, página Fase17 | `fase17 v1` |
| `fase18_escenas.py` | Escenas por tema (tabla `escenas`, `Escena`, `Guardarescena`, `Cargarescena`), luz local (`luz_local`), capas de diagnóstico (`diagnostico`), página Fase18 | `fase18 v1` |
| `fase19_modular.py` | Señales del modular (OSC, un CHOP, a mano o de prueba): viento, respiración de las ventanas, esporas, smog, niebla y glitch; página Fase19 y OSC In CHOP `modular_osc` (v2: rango -10..10 V) | `fase19 v2` |
| `ajuste_vista.py` | No es una fase: pone los valores calibrados de la vista también donde los has tocado a mano, y escribe la línea para volver atrás (ver *Calibración de la vista*) | `ajuste_vista v1` |
| `pruebas/sesion_escena.py` | La sesión de 20 minutos por escena de la fase 18, sobre el motor: densidad, piezas, coste por fotograma y criterios de cierre | — |
| `pruebas/` | TouchDesigner simulado (desde la fase 11 v5, también Script TOP y parámetros RGB), vista previa del catálogo (bolas y conos) y comprobación del shader con OpenGL, con el terreno y los ríos (solo para probar fuera de TouchDesigner; ver *Cómo se ha probado*) | — |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase11_piel.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase12_moduladores.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase13_tejido.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase14_destructores.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase15_era.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase16_cortes.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase17_tiempo.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase18_escenas.py').read())
exec(open('C:/Users/DareDave/Downloads/est/fase19_modular.py').read())
```

Requiere la fase 10. Las fases 3, 4 y 7 cambian solo su autoprueba (`fase3 v12`, `fase4 v7`, `fase7 v11`): sus comprobaciones de cajas siguen valiendo relanzadas en un proyecto que ya está en la fase 11, y las de la erosión de la fase 7, en uno que ya está en la 14 (se miden con el nivel 13: desde la 14 un arañazo es también un accidente). Las de la paleta de la fase 8 (`fase8 v9`) se miden con el nivel 14: desde la 15 la concha lleva la materia de su tema.

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
| semilla (1) | brote: bola o cono pequeño | cono con ruido de crestas y columnas de basalto en las laderas bajas | caseta (2) | bloque de una planta (2) |
| crecimiento (2 a `Umbralram` − 1) | árbol: frondosa (bola) o conífera (cono) según el piso | el cono sube | añadidos oblicuos apilados | apila plantas |
| ramificación (`Umbralram`, 5+) | arboleda: 5 a 12 copas agrupadas | montañas satélite | pasarelas hacia las vecinas | anexos: manzana |
| fusión (`Umbralfusion`, 7+) | bosque: dosel continuo (colonización del espacio) | cordillera (cluster de 3+), sin columnas | barrio denso | podio que une la manzana |
| monte (`Umbralmonte`, 8+) | monte boscoso: sube el terreno y el bosque lo cubre | el terreno sube: cumbres nevadas | — | — |
| coronación (`Umbralcorona`, 9+) | sigue el monte (sin árbol madre) | sigue el monte | torre de antenas | rascacielos con aguja |

*Desde la fase 11 v5 la naturaleza tiene su escalera propia: ver* La naturaleza legible *más abajo. La tabla de la ciudad no cambia.*

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

### La naturaleza legible (fase 11 v5, motor v46, comun v33)

**Qué pasaba.** La ciudad se leía a distancia de cámara de globo y la naturaleza no: hasta el bosque se entendía algo, pero por encima el árbol madre y los compuestos del juego del caos (incrustar, orbitar, inclinar a 30°) se apilaban en un amasijo sin forma, y el relieve no se leía como montaña ni como cordillera. A 13–50 px de alto el detalle de un árbol no existe: la ciudad se lee por su orden repetido (ventanas en rejilla), su silueta (prismas con remate) y su escalera (más ocupación, más alta y densa). **Regla de esta corrección:** la naturaleza se lee por masa, silueta y bandas de color, como la cartografía de montaña a escala pequeña.

**Diagnóstico: de dónde salían el modelo y el color.** Antes de tocar nada se localizó, en el motor v45:
- **Modelos.** El catálogo daba a la vegetación `veg_brote`/`veg_brote2`, `veg_arbol`, `veg_arboleda`, `veg_bosque` y `veg_madre` (L-system de 30°) y al relieve `rel_columna`, `rel_columnas`, `rel_mesetas`, `rel_meseta` y `rel_cumbre` (columnas apiladas). Cada formación era un compuesto de hasta `Maxpiezas` piezas del juego del caos; el dosel, medios puentes (`veg_dosel`) y copas en los huecos.
- **Color por instancia** (`build_piel`): el color de la especie (`COL_ESPECIE`) acercado al material de la velocidad (`material_tema`), y encima el **latido mezclaba el tinte del secuenciador o del pad al 75 %** (`LATIDO_TINTE`) mientras sonaba la nota. Esa era la causa de que el bosque se volviera blanco, ámbar o del color del pad. La concha no pasaba al albedo de los modelos; lo que sí cambiaba con la concha era el fondo: la paleta de generaciones generaba verdes (tono 123° y 145°) que camuflaban el bosque.

**La escalera nueva (vegetación, SEQ1).**

| Ocupación | Antes | Ahora |
|---|---|---|
| 1 | brote angular | brote: bola o cono pequeño |
| 2 a `Umbralram` − 1 | tronco y copa | árbol de silueta clara: frondosa (bola) en el piso basal, conífera (cono) desde el montano; hasta `Maxcaosnat`, pimpollos alrededor |
| `Umbralram` (5) | arboleda en las vecinas | arboleda: de 5 a 12 árboles agrupados |
| `Umbralfusion` (7) | dosel multicelda | bosque: dosel continuo (ver *Dosel*) |
| `Umbralmonte` (8) y más | árbol madre que rompe el dosel | **monte boscoso**: la ocupación ya no añade piezas, sube el terreno de la celda y el bosque lo cubre como una manta |

- Con los umbrales de siempre los estados empiezan una ocupación más tarde que en el encargo (ver *Ojo con los números*); el monte usa su propio umbral, `Umbralmonte` 8.
- **El terreno sube** `Alturamonte` × el límite en 6 ocupaciones (`PASOS_MONTE`) desde `Umbralmonte`; la erosión lo baja y el bosque se reajusta (la copa va siempre sobre el suelo local).
- **El juego del caos** deja de actuar en la naturaleza por encima de `Maxcaosnat` (5). Por debajo solo varía la posición y la escala de las copas, sin incrustar, orbitar ni inclinar; por encima, las copas van en filotaxis (orden repetido). En la ciudad el caos no cambia.
- **El árbol madre desaparece** como pieza (también del catálogo: `veg_madre`, `veg_bosque` y `veg_arboleda` ya no existen). Los protagonistas de los clusters de 2 y 3 celdas son árboles grandes de silueta clara.

**El relieve (SEQ2): montaña y cordillera, una sola malla.**
- El relieve ya no son piezas: es **una sola malla**, la esfera `terreno` (Sphere SOP de 256 × 512), que el shader desplaza en el vertex shader con el **mapa de alturas** del motor (512 × 256 en latitud y longitud, float32, en el Script TOP `alturas`). Así una cordillera es una superficie continua, no columnas por celda, y Python no reconstruye geometría: solo reescribe la textura cuando cambia la ocupación.
- **Montaña suelta:** un cono deformado con ruido de crestas (*ridged multifractal* de 4 octavas sobre la esfera) que talla crestas y valles en las laderas sin tocar la cumbre. Alto: 1,5 × la formación más el monte; la capital de un cluster, un 8 % más.
- **Cordillera** (cluster de relieve de 3 celdas o más): una cresta continua a lo largo del **eje** del cluster (el camino, por la máscara de vecinas, entre sus dos celdas más alejadas), con collados al 85 % entre cumbres; las demás uniones del cluster son estribaciones bajas (35 %). Las cumbres quedan en la capital y en los máximos locales.
- **Las laderas se cierran** sobre la esfera como el dosel: donde no hay relieve la malla se hunde 6 centésimas bajo las losetas (con el suelo erosionado 3 × 3, nunca asoma de una loseta).
- **Las columnas de basalto** quedan como textura de las laderas bajas en los estados 1 a 3 (5 columnas oscuras alrededor del cono). Las mesetas, la cumbre escalonada y los puentes del relieve ya no se dibujan.
- **Híbrido** (la vegetación coloniza el relieve): el bosque sube por la ladera hasta `Limitebosque`; por encima, roca y nieve.

**Dosel por colonización del espacio.**
- En los clusters de vegetación de 4 celdas o más (y en un bosque suelto) la copa es una sola envolvente: se siembran puntos de atracción en el volumen de cada celda y las ramas crecen hacia ellos desde una raíz en el centro (Runions, Lane y Prusinkiewicz, 2007). Cada celda coloniza su parte: **abierta hasta arriba hacia sus vecinas del cluster y en cúpula hacia fuera**, así que las partes se juntan en una sola copa sin solaparse.
- Se calcula en Python, **una vez por celda y vecinas del cluster** (se guarda): un cluster que crece solo rehace sus bordes. La primera versión colonizaba el cluster entero de golpe y, con clusters de 30 celdas que cambian a cada nota, tardaba unos 100 ms cada vez (lo detectó la sesión de 20 minutos).
- **Lo que llega a la imagen** es el borde de la copa: de lejos, las copas de arriba (bolas o conos, 1,25 veces más grandes); cerca, todas y los troncos. Claras arriba, más oscuras abajo: la textura granulada que hace de ventanas de la ciudad.
- **Forma por altitud:** bola (frondosa) en el piso basal, cono (conífera) desde el montano; en el límite del bosque las copas se ralean y por encima no hay ninguna.
- Los clusters de 2 y 3 celdas conservan sus medios puentes del dosel y su protagonista.

**Pisos de color por altitud (tintes hipsométricos).**

| Piso | Altura relativa | Color | Material |
|---|---|---|---|
| Basal | 0–35 % | verde profundo | mate (rugosidad 0,9), granulado |
| Montano | 35 % – `Limitebosque` − 5 % | verde azulado oscuro (coníferas) | mate |
| Límite del bosque | ± 5 % de `Limitebosque` (0,65) | verde y ocre, copas ralas | mate |
| Roca | hasta `Limitenieve` (0,9) | gris cálido que se oscurece hacia arriba, facetado | rugosidad 0,7, normales marcadas |
| Cumbre | `Limitenieve`–100 % | blanco nieve | brillo, rugosidad 0,3 |

- La altura es **sobre el suelo local** (el de la celda), no sobre el radio del núcleo: el planeta crece y los pisos no se mueven. El 100 % es la altura máxima posible: el límite más el monte entero (`Alturamonte` × el límite).
- La rampa está en el **Ramp TOP `rampa_hipso`** (sus claves, en la tabla `rampa_hipso_claves`, las reescribe el motor si cambian `Limitebosque` o `Limitenieve`), y el GLSL MAT del terreno la lee por altura relativa (`sRampa`). Si el sampler no se enlaza, el shader calcula la misma rampa (`uTerreno.w`).
- Las copas y las columnas toman el color de su piso desde el motor (la misma rampa), con un 30 % del material de la velocidad (fase 12).
- **Contraste en las cumbres:** el gris de la roca se oscurece al acercarse a la nieve, así que la cumbre más alta es blanco sobre gris oscuro.
- **Sombreado de laderas:** una luz rasante fija respecto a la cámara (de arriba a la izquierda, como el relieve sombreado suizo) además de la principal, para que crestas y valles se lean aunque el globo gire.

**El color de la naturaleza ya no viene de la concha ni del secuenciador.**
- Los modelos de naturaleza no toman el color de la concha ni el tinte del secuenciador o del pad en el albedo: su color sale de los pisos.
- **El tinte va al borde:** un emisivo de borde (fresnel) alrededor de hasta tres focos (la nota de cada SEQ y el pad más fuerte; uniformes `uTinte0`–`uTinte2`, intensidad `Tintebordenat`), y a la loseta de la celda (`luz_celda`, como antes). Se ve dónde cae la nota sin que el bosque se vuelva ámbar o cian. La nota sigue hinchando la formación (el latido).
- **La paleta de conchas** reserva ahora también los verdes de los pisos (120°–165°) y el azul de los ríos (235°–275°): ver la paleta de generaciones en `MONTAJE_FASES_3_10.md`.

**Detalle según distancia (LOD).** Con la cámara de globo, el dosel es la envolvente con su textura de copas y la montaña la malla; si la celda mide en pantalla `Lodnat` px o más (con el planeta a `Encuadre` del alto) o con la cámara de superficie, aparecen todas las copas y los troncos. La leyenda dice `detalle cerca (N celdas)` o `globo`.

**Parámetros (página Fase11).** `Umbralmonte` 8 · `Maxcaosnat` 5 · `Limitebosque` 0,65 · `Limitenieve` 0,9 · `Alturamonte` 1 (× el límite) · `Lodnat` 80 px · `Tintebordenat` 0,8.

**Leyenda.**
```
NATURA   copas 214   montes 2   cordilleras 1   cumbres nevadas 3   detalle globo
```

**Probar sin BeatStep.**
1. `Sembrar` en una celda una docena de veces (`Velprueba` 100): brote, árbol, arboleda, bosque y, desde la ocupación 8, el terreno sube con el bosque encima.
2. `Sembrarzona2` dos veces y `Sembrar2` en el centro: una cordillera con la cumbre nevada.
3. Una nota sobre un bosque: el borde de las copas se ilumina con el color del SEQ y el verde se mantiene.
4. `Erosionar` sobre un monte: baja el terreno y el bosque baja con él.

**Autoprueba (las siete pruebas del encargo).** Ocupación 1 → 12 en una celda (brote, árbol, arboleda, bosque y un monte que sube, sin árbol madre); un cluster de 5 celdas de relieve en fila es una cordillera continua con cumbres nevadas y sin piezas sueltas; el bosque sobre la cordillera no pasa de `Limitebosque`; una montaña (cumbre blanca) se distingue de un bosque (copas verdes con varios valores); una nota del SEQ1 sobre un bosque deja el albedo igual y enciende el foco del borde; la erosión sobre un monte baja el terreno y el bosque; con las 85 celdas a ocupación 14, la naturaleza tarda en Python lo mismo que la ciudad ± 10 % (más 2 ms de margen); y la línea `NATURA` de la leyenda. Además, `Sembrarzona` × 2 da un cluster de 7 celdas con un dosel de copas y sin puentes, y `Sembrarzona2` × 2, una cordillera sin puentes ni protagonista.

**Rendimiento** (simulación, sesión de naturaleza de 5 minutos, un fotograma sin cambios): `build_instances` 3,9 ms de mediana, frente a 3,5 ms de la ciudad (+11 %) y 3,5 ms de la naturaleza antes del cambio. Cuando cambia la ocupación de una celda con relieve o monte, ese fotograma rehace el mapa de alturas (los parches de cada rasgo se guardan; se recomponen solo las filas con relieve) y TouchDesigner sube la textura: unos ms más en ese fotograma. El tiempo real hay que medirlo en TouchDesigner.

**Lo que necesita el shader.** El relieve solo se levanta con el shader de la piel (`mat_piel_tierra`): con `Materialrespaldo` las formaciones pasan a Phong pero la malla del terreno sigue con su GLSL MAT, porque sin él no hay desplazamiento.

---

## FASE 12 · Moduladores: velocidad y duración del gate

### Qué hace

Las dos señales que ya modulaban las cajas pasan a modular los modelos temáticos, y el material deja de necesitar geometrías duplicadas. La velocidad sigue sembrando el caos de la fase 11: eso no cambia.

### Un material por modelo

- **Una geometría por modelo**: de 94 a 49 (`mod_<modelo>`; las obras de la ciudad ya tenían una).
- **Shader de la piel**: un GLSL MAT por familia de material, con los mismos shaders (`piel_vertex`, `piel_pixel`):
  - `mat_piel_mineral`: el relieve, obsidiana ↔ piedra pómez;
  - `mat_piel_dosel`: desde el motor v32, **toda la vegetación** (árboles, brotes y dosel): hoja cerosa ↔ musgo seco (ver *El aspecto de la naturaleza*). Hasta la v31 era solo el dosel, de vidrio ahumado con vetas ámbar, y los árboles eran de obsidiana;
  - `mat_piel_ciudad`: vidrio negro ↔ hormigón brutalista, con ventanas ámbar que se quedan apagadas hasta la fase 17 (`uVentanas`).
  
  Las obras de la ciudad (valla, foso, andamio, grúa) siguen con `mat_poroso`.
- **La rugosidad va en el canal `a`** (el alfa del color de cada instancia: Instance 2 → Color A = `a`). Cada Script CHOP de modelo tiene un canal más. El shader la lee:
  - pulido: reflejo fino y fuerte, y un reflejo de borde frío;
  - rugoso: mate y con poros (manchas de ruido en el espacio del modelo, distintas en cada instancia).
- **El color** también se acerca al material: el de la especie se mezcla con obsidiana o pómez (naturaleza) o con vidrio negro u hormigón (ciudad), según la rugosidad. Así, pulido y rugoso se distinguen también con el material de respaldo.
- **Luces**: el shader no usa las funciones de iluminación de TouchDesigner. Lee como uniformes la posición y el color × dimmer de `luz_principal`, `luz_relleno` y `luz_destello` (página Vectors del GLSL MAT, con expresiones), más un ambiente. El color lo da el motor (`luz_color`), que prueba los nombres del color de la Light COMP (`cr cg cb`).
- **Corregido en comun v20**: la primera versión leía el color de las luces como `lightcolorr/g/b`, que la Light COMP no tiene, y los tres `mat_piel_*` daban `tdAttributeError: 'td.ParCollection' object has no attribute 'lightcolorr'`. Relanza `fase12_moduladores.py` (o la 13) para arreglarlo.

### El aspecto de la naturaleza (motor v32, comun v23)

En TouchDesigner la naturaleza «parecía hilo de alambre». Tres causas, las tres corregidas:

- **Los árboles y brotes eran de piedra.** Solo el dosel usaba el material vegetal; el resto de la vegetación usaba el mineral (obsidiana pulida ↔ pómez): varillas oscuras con reflejos de metal. Ahora toda la vegetación usa `mat_piel_dosel`, y su color se mezcla con la paleta vegetal en vez de con la obsidiana.
- **El dosel era una red.** Los medios puentes del dosel eran tiras estrechas a media altura de las copas: sobre el planeta formaban una malla de triángulos huecos que flotaba sobre el suelo. Ahora las tiras son más anchas (0,42 × celda en vez de 0,32) y **cada hueco entre tres celdas del cluster unidas entre sí lleva su copa** (el mismo modelo del dosel, centrado en el triángulo y del diámetro de 1,5 × su radio; crece con la etapa `puentes` como los puentes). El dosel se cierra en un techo de copas.
- **Las vetas ámbar** del dosel eran líneas finas y brillantes: de lejos, filamentos. Han desaparecido.
- **Sin parpadeo** (motor v33): los medios puentes que salen de una misma celda tenían las tapas en el mismo plano y se pisaban (z-fighting). Ahora cada uno es un 4 % más alto que el anterior.

El shader vegetal (uFamilia 1):

- hojas en manchas anchas de dos verdes (ruido en el espacio del modelo), cada planta con su matiz;
- las caras de lado (troncos, ramas, bordes de copa: las que no miran hacia fuera del planeta) más pardas y oscuras, con fibra;
- la luz **envuelve** (las caras de lado no se quedan negras) y la copa **deja pasar la luz a contraluz**; ambiente un 60 % más alto que en la piedra;
- la velocidad sigue mandando: pulida (velocidad alta), hoja cerosa con un brillo suave; rugosa (baja), musgo seco, mate y con manchas.

El relieve sigue siendo de obsidiana ↔ pómez, y la ciudad no cambia.

**Para aplicarlo** basta relanzar cualquier fase (por ejemplo `fase13_tejido.py`): `piel_al_dia` reescribe el shader y cambia el material de las geometrías de la vegetación (`piel: N geometrias con el material de su familia`).

**¿Lo cambia alguna fase futura?** No. Ninguna de las fases 14 a 18 del plan cambia el aspecto de la vegetación: la 14 añade rayo, incendio y claro de ceniza; la 15, el entierro como veta de carbón; la 16, los fósiles en los cortes; la 17, el balanceo del dosel y el frente; la 18, presets de paleta y luz por tema. Por eso se corrige aquí. La fase 18 podrá guardar la paleta por tema, pero no la geometría ni el material.

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

- **Ríos (naturaleza)** — desde la fase 13 v2, ver *Ríos azules* más abajo.
  - Nacen en las cumbres: las celdas con relieve más altas que todas sus vecinas, y las capitales de los clusters de relieve.
  - Bajan por el **suelo real** (el suelo de la celda más el relieve de la fase 11 v5 en su centro) hacia la vecina más baja (en empate, la de índice menor), sin volver por donde han pasado. Hasta la v1 bajaban hacia la vecina menos ocupada.
  - Acaban en una hondonada o un llano (ninguna vecina más baja), al llegar a otro río (confluyen), tras `Maxrio` tramos o si no les queda vecina libre.
  - Se trazan de la cumbre más alta a la más baja. Un río que llega a otro acaba ahí, y aguas abajo de la confluencia el río que lo recibe se ensancha: de `Anchorio` con un río a `Anchomaxrio` con cuatro o más.
- **Carreteras (ciudad).**
  - Los nodos son las capitales de los clusters y las formaciones sueltas (sin cluster ni satélites) con ocupación de `Minvia` o más.
  - La distancia entre dos nodos es el número de saltos por la retícula. Kruskal elige el árbol de expansión mínima (en empate, por los índices).
  - Cada arista se dibuja por el camino más corto de la retícula. Los tramos compartidos se dibujan una vez.
- **Las carreteras** van de centro a centro de celda, a ras del suelo de cada celda (6 milésimas por encima), en dos medios tramos que siguen la curva del planeta. Pasan por debajo de las formaciones que cruzan.
- **La geometría `tejido`** es la caja instanciada de siempre, con el shader de la piel: el asfalto es mate. `Materialrespaldo` también la cambia a Phong. Se dibuja justo encima de las conchas. Desde la v2 los ríos van en su propia geometría, `rios`.
- **Se recalcula solo cuando cambia la ocupación** (las especies o los satélites); si no, se reutiliza. Las filas sí se rehacen en cada fotograma, porque el suelo cambia con las conchas y los cortes.

### Parámetros (página Fase13)

`Rios` (encendido) · `Carreteras` (encendido) · `Minvia` 2 · `Grosorvia` 0,18 (carreteras) · `Maxrio` 12 (tramos) · v2: `Colorrio` (OKLCH 0,55 · 0,15 · 255: `#2971C6`) · `Anchorio` 0,10 · `Anchomaxrio` 0,34 · `Emisivorio` 0,25 · `Lagos` (encendido)

### Leyenda

```
TEJIDO   rios 2 (9 tramos, 1 lagos)   carreteras 7 tramos
```

### Probar sin BeatStep

1. `Tema` ciudad. Pon `Nota` 64 y pulsa `Sembrarzona` dos veces; pon `Nota` 70 (el meridiano opuesto) y pulsa otras dos. Aparece la carretera que une las dos capitales. Con `Sembrar` en una nota suelta (3 veces, para llegar a `Minvia`) la red se rehace y la incluye.
2. `Tema` naturaleza. `Sembrarzona2` dos veces y `Sembrar2` una docena de veces en el centro (`Nota2`): el río azul baja de la cumbre por las laderas hasta el llano. Dos zonas cercanas pueden dar dos ríos que confluyen.

Con zonas de 7 celdas los ríos son cortos: acaban en cuanto llegan al llano. Se alargan en las cordilleras y cuando bajan a una hondonada.

### Autoprueba

Comprueba:
- **Carreteras:**
  - dos zonas en la ciudad quedan unidas por el camino más corto;
  - una formación suelta entra en la red y el árbol tiene nodos − 1 aristas;
  - el cálculo se reutiliza si la ocupación no cambia;
  - el árbol es el de menor longitud total, comparado con todos los demás posibles;
  - `Carreteras` apagado quita las carreteras.
- **Ríos (v2, las pruebas del encargo):**
  - el río nace en una cumbre y en cada paso baja por el suelo real a la vecina más baja, hasta un llano, una hondonada, otro río o el tope de longitud;
  - en una cordillera con valles los ríos son cintas azules (el color de `Colorrio`, sin tintes), apoyadas en el terreno con un pequeño desfase;
  - una nota del SEQ1 sobre una celda con río enciende su loseta y el río sigue azul y fuera de ella;
  - veinte conchas apiladas: ninguna del azul de los ríos (la banda está reservada);
  - en la cara de sombra el agua lleva su emisivo (`Emisivorio`) y no toma los tintes del borde;
  - dos ríos que confluyen: el tramo de abajo es más ancho;
  - un río que acaba en una hondonada la llena (lago); `Lagos` apagado, sin lago;
  - `Maxrio` corta la longitud y `Rios` apagado los quita.
- **Dibujo:** `i_rios` recibe las cintas con el canal `a`, y la leyenda tiene la línea `TEJIDO` con los lagos.

### Ríos azules (fase 13 v2, motor v46, comun v33)

**Qué pasaba.** Los ríos no se veían azules, así que no se entendía que eran ríos.

**Diagnóstico** (en el orden del encargo, con lo que se encontró):
1. **Color por instancia sobrescrito:** no. Los tramos llevaban su azul (`COL_RIO`) y ningún tinte de celda, de pad ni de concha los tocaba.
2. **Ocultos: sí, la causa principal.** Iban de centro a centro de celda a 6 milésimas del suelo: por debajo de las formaciones que cruzaban y justo bajo la loseta de luz de la celda (`luz_celda`, 2 centésimas por encima del suelo y hasta 0,28 de alto), que además es aditiva y los teñía.
3. **Paleta de conchas: sí.** Las conchas 4 (251°) y 7 (145°) de la paleta de generaciones eran azul y verde: el río desaparecía sobre ellas.
4. **Lado de sombra: sí.** Usaban el material mineral sin emisivo: en la cara oscura del globo el azul (y además oscuro: `(0,12 0,26 0,56)`) se volvía negro.

**Qué cambia.**
- **Azul reservado:** OKLCH 0,55 · 0,15 · 255 (`Colorrio`), distinto del cian de las cicatrices y del ámbar del SEQ2. Su banda (235°–275°) sale de la paleta de conchas, como el cian y el ámbar.
- **Sin tintes:** los ríos van en su geometría (`rios`) con su material (`mat_piel_agua`, familia 4 del shader): ignoran el tinte de celda, de pad y de concha y el borde tintado de la naturaleza.
- **Cinta, no caja:** una cinta continua (una curva Catmull-Rom troceada en tramos planos de 6 milésimas) apoyada en el suelo local más el relieve, con un desfase de 2,5 centésimas (algo más en las laderas). Cruza cada celda por sus bordes y a 0,36 anchos de celda de su centro: **bordea** la formación y la loseta de luz en vez de pasar por debajo. En los bosques, las copas que pisarían el río no se dibujan.
- **Ancho por caudal:** cada tramo suma los ríos que confluyen en él: de `Anchorio` a `Anchomaxrio`.
- **Lagos:** la hondonada (laguna de la fase 8) donde acaba un río se llena hasta su borde más bajo con el mismo azul (`Lagos`).
- **Brillo:** especular alto (rugosidad 0,1) y emisivo bajo (`Emisivorio` 0,25): se lee también en la cara de sombra.
- **Pendiente:** bajan por el suelo real, así que nacen en las cumbres de la fase 11 v5 y bajan entre montes.
- Las cintas solo se recalculan cuando cambian el tejido, el terreno o el suelo; las filas se guardan.

---

## FASE 14 · Destructores I: arañazos y escalada

### Qué hace

Los arañazos de la batería (fase 7) reciben forma temática, y la insistencia destructiva escala igual que la constructiva. **Un golpe es un accidente; varios golpes en la misma zona, una catástrofe.**

| Especie | Un golpe | Escalada | Huella |
|---|---|---|---|
| Vegetación | Rayo que tala el árbol más alto | Incendio que avanza por los puentes del dosel | Claro de ceniza (`veg_claro`) |
| Relieve | Desprendimiento de columnas | Derrumbe de la meseta | Pedregal (`rel_pedregal`) |
| Informal | Se desploma un añadido | Derrumbe en cadena del barrio | Escombros (`inf_escombros`) |
| Planificada | Caen las plantas altas | Demolición por implosión, con polvo | Solar vallado (`ciu_valla`) |

- **Qué es un arañazo.** Un pad de erosión cuyo perfil no tiene profundidad, es decir, que no corta. El plan decía «pads 1–5», pero con los perfiles del usuario la caja corta (pad 2) y, desde la fase 7 v12, el bombo y el tom (pads 1 y 3) son impulso y no destruyen, así que los arañazos son los **pads 4–8**. Si cambias los perfiles, cambian con ellos. Los cortes siguen como en la fase 9; su forma temática es la fase 16.
- **Un golpe: el accidente.** La erosión de la fase 7 se aplica como siempre (notas deshechas en anillos y luz del pad). Además, **la formación más alta de la vecindad del objetivo** (la celda objetivo y sus vecinas; en empate, la de índice menor) **baja un estado**, si la erosión no la ha bajado ya. Por ejemplo, de árbol a crecimiento o de crecimiento a semilla; una semilla se vacía. Deja una nube: brasas y ceniza el rayo, polvo los demás.
- **Escalada.** Cuando caen `Golpesescalada` golpes en la misma vecindad dentro de `Ventanaescalada` pasos, **el golpe que escala es la catástrofe**, no otro accidente. Dos golpes son de la misma zona si el objetivo de uno está en la vecindad del otro, y cada golpe escala una sola vez. La catástrofe empieza en la formación más alta de la vecindad, con su cluster **tal como estaba antes de ese golpe**, para que el golpe no deshaga el bosque antes de que prenda.
- **Incendio, derrumbe y derrumbe en cadena.** Es un autómata de Drossel–Schwabl acotado:
  - en cada paso, cada celda activa puede saltar a sus vecinas del cluster de la misma especie (por los puentes del dosel, la meseta o las pasarelas);
  - **el salto lo decide el mapa logístico**, sembrado con la velocidad del golpe, la celda y el paso: la misma historia da el mismo fuego, y otra velocidad, otro;
  - cada celda activa **pierde 1 de ocupación por paso** y se apaga sin ocupación o a los `Pasosfuego` pasos;
  - **nunca sale del cluster** (decisión del plan) y **como mucho `Maxfuego` celdas activas a la vez** entre todas las catástrofes;
  - si su zona ya tiene una catástrofe en curso, no empieza otra.
- **Implosión.** La torre (la planificada más alta de la vecindad) cae entera de golpe, con una nube grande de polvo.
- **Presupuesto.** La escalada cuenta como erosión: lo que quema es ocupación que se pierde. Con la densidad por encima de `Umbraldensidad` (fase 7, 60 %), la catástrofe empieza **más grande**: en la celda y en sus vecinas del cluster, como la erosión con `Multradio`.
- **Huellas.** Una celda que se vacía en una catástrofe deja la huella de su especie: un modelo bajo a ras del suelo. La quita la siguiente nota de construcción en esa celda. Un corte (fase 9) también la quita, y no se dibuja con el otro tema activo.
- **Derribo.** Una obra a medias (cadena de fusión o de coronación sin terminar) que recibe un arañazo en su vecindad se derriba:
  - toda la obra de su cluster retrocede ya una etapa y sigue hacia atrás, una etapa cada `Pasosetapa` pasos, hasta el principio;
  - una nota en el cluster para el derribo, y la obra puede volver a avanzar.
- **Partículas** (instancias del motor, geometría `particulas`):
  - brasas ámbar que suben de lo que arde y ceniza gris que cae;
  - polvo en los derrumbes;
  - las nubes de los accidentes y de las celdas que se apagan encogen y desaparecen en `Pasospolvo` pasos.

  Lo que arde se tiñe de brasa a saltos (stop-motion) y se carboniza con lo que ha ardido, también el dosel que tiene encima.
- **Fin de ciclo.** Lo apaga todo de golpe: no quedan fuegos, polvo, huellas ni obras derribándose, y las obras se cierran como siempre.
- Por debajo del nivel 14, un arañazo sigue siendo la erosión de la fase 7.

### Parámetros (página Fase14)

`Ventanaescalada` 8 (pasos) · `Golpesescalada` 2 · `Pasosfuego` 6 · `Maxfuego` 6 · `Pasospolvo` 8 · `Escalar` (botón de prueba)

### Leyenda

```
EROSION  pad 5   aranazo   -2.0 notas   radio 1   celda 40   densidad 8%   · rayo celda 40
ESCALADA INCENDIO 4 celdas paso 3/6   golpes 0/2 en la zona   huellas 2
```

`golpes` cuenta los arañazos que lleva la zona del último golpe, frente a `Golpesescalada`. `paso` es lo que lleva ardiendo la celda más antigua, frente a `Pasosfuego`. Una implosión reciente sale como `IMPLOSION celda N`.

### Probar sin BeatStep

1. `Tema` naturaleza. `Nota` 64: pulsa `Sembrarzona` cuatro veces y `Sembrar` ocho (un bosque denso).
2. `Padprueba` 5 (un arañazo) y `Escalar`: da `Golpesescalada` arañazos seguidos. El fuego prende en el árbol más alto, salta por el cluster y deja claros de ceniza. También vale pulsar `Erosionar` dos veces seguidas: en menos de un segundo a 120 BPM.
3. Un solo `Erosionar`: el rayo tala el árbol más alto (baja un estado).
4. Con `Tema` ciudad y `Sembrarzona2` (planificada), `Escalar` hace una implosión.
5. `Sembrar` sobre un claro lo borra y vuelve a crecer.

Si `Padprueba` es un pad que corta (1–3), `Escalar` usa el primer pad de arañazo.

### Autoprueba

Comprueba:
- los arañazos son los pads sin profundidad;
- un golpe sobre cada especie hace su accidente en la formación más alta de la vecindad, y esta baja un estado;
- dos golpes en la misma vecindad prenden el incendio, que salta por el cluster (solo vegetación, nunca fuera) y quita 1 de ocupación por paso;
- se apaga sin combustible o a los `Pasosfuego` pasos, nunca con más de `Maxfuego` celdas, y deja claros de ceniza;
- misma historia, mismo fuego; con otra velocidad, otro;
- brasas mientras arde; la huella se dibuja; el polvo se disipa; una nota borra la huella;
- fuera de la ventana o en otra zona no escala;
- `Maxfuego` 2 nunca deja más de 2 celdas ardiendo;
- con la densidad por encima de `Umbraldensidad` la catástrofe empieza más grande;
- el derrumbe deja pedregal, el derrumbe en cadena escombros, y la implosión es inmediata y deja el solar vallado;
- una obra a medias golpeada retrocede y llega al principio;
- `Forzarciclo` con un incendio lo apaga todo, sin obras colgadas;
- en el nivel 13 un arañazo sigue siendo la erosión de la fase 7;
- las líneas `EROSION` y `ESCALADA` de la leyenda.

### Rendimiento

En el simulador, un fotograma del motor con un incendio en curso cuesta lo mismo que sin él (unos 2 ms con el mundo de prueba). Las catástrofes avanzan una vez por paso y sin nada en curso no hacen nada.

---

## FASE 15 · El ciclo como era: entierro temático y herencia

### Qué hace

Cada fin de ciclo entierra el mundo con la materia de su tema, y la herencia rebrota según su lógica. Cambiar de tema entre ciclos deja bosques fósiles bajo ciudades, o ciudades bajo bosques.

- **Entierro.** Antes de hornear, los tránsitos se cierran en su estado final (como desde la fase 11) y los fuegos y derrumbes de la fase 14 se apagan. Las losetas de la concha nueva llevan la materia de lo que hubo en cada celda:
  - naturaleza: **veta de carbón** (negro brillante) donde hubo bosque y **basalto** donde hubo relieve;
  - ciudad: **hormigón gris**, también en las celdas vacías, con la **traza de sus calles**: las celdas por las que pasaban sus carreteras, más oscuras.

  La materia se mezcla con el color de la generación (fase 8) sin taparlo del todo: el carbón un 85 %, el basalto y el hormigón un 60 %. Las celdas vacías de la naturaleza conservan su color de generación. Las conchas enterradas antes de la fase 15 no cambian.
- **Las conchas usan el shader de la piel** (familia mineral), con la rugosidad de cada loseta en el canal `a`: el carbón brilla (0,06), el basalto es medio (0,5), el hormigón es mate (0,85), las calles 0,7, lo demás 0,7 y el zócalo 0,9. `Materialrespaldo` las vuelve a un Phong, como a los modelos. Lo pone `install_core` al relanzar cualquier fase (`conchas_al_dia`); la fase 8 lo vuelve a poner si se relanza.
- **Registro.** Cada concha guarda:
  - su `tema`;
  - por celda, `esp` (especie: 1 vegetación, 2 relieve, 3 informal, 4 planificada; 0 vacía), `estado` (0 semilla a 4 coronación) y `cluster`;
  - sus `vias` (tramos de carretera), `calles` (celdas por las que pasan) y `rios`.

  Lo leerán los cortes de la fase 16. Mientras nada se exponga, no cuesta nada: solo se guarda.
- **Herencia temática**, según el tema del mundo nuevo:
  - **naturaleza: banco de semillas.** Lo heredado no aparece de golpe. Primero son semillas sobre el suelo (partículas pardas, sin modelo); luego brotes que crecen a saltos; luego la formación. Cada etapa dura 2 × `Pasosetapa` pasos. Una nota en la celda la hace brotar de golpe. Con `Rebrote` apagado, lo heredado brota como antes;
  - **ciudad: trazas.** Si lo enterrado era una ciudad, sus carreteras quedan como trazas. La red nueva las prefiere: cada tramo de traza cuesta 1 − 0,9 × `Pesotraza` (con 0,5, 0,55) en lugar de 1, tanto para el árbol de expansión mínima (Kruskal) como para el camino de cada arista. Con `Pesotraza` 0 vuelve el camino más corto.
- **Temaenciclo.** El mundo tiene su tema. Con `Temaenciclo` encendido, cambiar `Tema` no cambia el mundo en curso: espera al siguiente fin de ciclo, y así cada concha tiene un solo tema. La leyenda dice `(ciudad en el proximo ciclo)`. Apagado, el cambio es inmediato, como hasta ahora.
- La paleta de generaciones de la fase 8 se mantiene: cada concha conserva su color.

### Parámetros (página Fase15)

`Pesotraza` 0,5 (0–1) · `Rebrote` (encendido) · `Temaenciclo` (encendido)

### Leyenda

```
ERA      7   naturaleza -> carbon y basalto   herencia 25%   semillas 9   trazas 0 de 0
ERA      8   ciudad -> hormigon   herencia 25%   semillas 0   trazas 4 de 6   (naturaleza en el proximo ciclo)
```

`semillas` son las celdas del banco que aún no han brotado. `trazas 4 de 6` son los tramos de la red actual que siguen una traza, de las trazas heredadas.

### Probar sin BeatStep

1. `Tema` naturaleza. `Sembrarzona` y `Sembrarzona2` (con `Nota` y `Nota2` distintas) y unos `Sembrar` en el centro, para que algo pase la herencia del 25 %.
2. Pon `Tema` en ciudad: la leyenda `ERA` dice que espera. Pulsa `Forzarciclo`: la concha nueva es de carbón y basalto, y el mundo nuevo ya es ciudad.
3. `Sembrarzona` en dos zonas separadas (las carreteras las unen) y `Forzarciclo`: la concha de hormigón con sus calles. Quedan dos conchas de temas distintos; un corte (fase 9) en el bosque enterrado deja ver el carbón.
4. Otra ciudad en las mismas zonas: las carreteras siguen las trazas (`trazas N de M`).
5. Vuelve a naturaleza y a un `Forzarciclo` con un bosque: lo heredado sale como semillas y brota.

### Autoprueba

Comprueba:
- `Temaenciclo`: el cambio de `Tema` espera, la leyenda lo dice, y tras `Forzarciclo` manda el nuevo;
- el registro (tema y, por celda, especie, estado y cluster);
- la materia: carbón brillante y oscuro, basalto, y el color de generación en lo vacío;
- del bosque a la ciudad no quedan semillas ni trazas;
- la concha de ciudad con sus calles más oscuras que el hormigón;
- dos conchas de temas distintos;
- de una ciudad a otra, las trazas son sus carreteras, y con `Pesotraza` el camino sigue una traza aunque sea un tramo más largo (con 0, el más corto);
- el banco de semillas (sin modelo, con semillas), la cadena semillas → brotes → formación, la nota que la completa y `Rebrote` apagado;
- las losetas llevan la rugosidad en el canal `a` (con `Materialrespaldo`, 1);
- `Temaenciclo` apagado: el cambio es inmediato;
- la línea `ERA` de la leyenda.

---

## FASE 16 · Arqueología temática: cortes

### Qué hace

Los cortes de la fase 9 dejan de enseñar solo bandas de color: enseñan lo que había en cada concha, leído de su registro (fase 15).

- **Qué es un corte.** Un pad de erosión cuyo perfil tiene profundidad. El plan decía «pads 6–8»; con los perfiles del usuario corta la caja (**pad 2**). Hasta la fase 7 v11 cortaban también el bombo y el tom, que ahora son impulso. Si cambias los perfiles, cambian con ellos.
- **Naturaleza: sima.** En la veta de carbón, **troncos fósiles** aplastados en horizontal, de piedra clara (donde hubo bosque), y **columnas de basalto** de pie, una junto a otra (donde hubo relieve).
- **Ciudad: excavación.** **Cimientos** corridos con muros cortados y cascotes (ciudad informal), **sótanos** con solera, forjado y pilares, abiertos hacia el corte (planificada) y **tramos de calle** en sección, con aceras, firme y colector (las celdas por las que pasaban sus carreteras).
- **Solo dentro del corte.** Una celda está en el corte si su suelo queda por debajo del radio nominal: el corte y su anfiteatro, y también las hondonadas de cortes de mundos anteriores. Las piezas van:
  - en el **fondo**, medio enterradas en la loseta de arriba de su columna: lo que hubo en esa celda en esa era;
  - en las **paredes**: las losetas de las vecinas más altas que quedan al aire, entre el suelo de la celda y el de la vecina. La pieza asoma de la pared hacia el corte, con el ancho de la cara y el alto de la banda.

  Como mucho `Detalleexpuesto` piezas por celda: primero el fondo, y en las paredes **una por era antes de repetir**, de arriba abajo. Cada concha enseña lo suyo, sea del tema que sea: bajo una ciudad puede salir un bosque fósil. Una concha enterrada antes de la fase 15 no tiene registro y solo enseña su color. La variante sale del mapa logístico, sembrado con la concha y la celda.
- **Cicatriz.** El cian sigue reservado a lo recién expuesto, en los dos temas: las piezas de una loseta recién abierta salen cian y toman su color en `Cicatriz` segundos, como las losetas.
- **Escalada: cortes que se unen.** Dos cortes en la misma vecindad dentro de `Ventanaescalada` pasos (página Fase14) se unen por el camino más corto (`Unircortes`). Están en la misma vecindad si el objetivo del segundo cae dentro del primero o en su borde (a radio + 1). Cada corte se une una vez.
  - **Naturaleza: cañón.** Las celdas del camino se cortan con la profundidad del menor de los dos cortes. El cañón queda como hondonada, también en los mundos siguientes.
  - **Ciudad: galería de metro** a cielo abierto (falso túnel). Las celdas del camino se excavan una loseta y la galería va dentro de la zanja: solera, hastiales, bóveda de dos faldones y carriles; medio tramo hacia cada excavación. La galería se entierra con su mundo.

### Parámetros (página Fase16)

`Detalleexpuesto` 6 (*Piezas expuestas por celda del corte*, 0–24; 0 = solo bandas de color) · `Unircortes` (encendido) · `Unirprueba` (dos cortes vecinos seguidos alrededor de `Nota`, con el pad de prueba o el primero que corte)

### Leyenda

```
CORTE    celda 40   3 losetas   suelo 7.04   laguna 1.80   cicatriz 2.1 s
CORTE    celda 40   4 eras expuestas: basalto, ruinas, carbon, ruinas   piezas 21 en 7 celdas   + galeria de metro 40-28-27 (3 celdas)
```

Las eras expuestas son las del corte entero (el objetivo y su anfiteatro), de arriba abajo: `carbon` (bosque), `basalto` (relieve), `ruinas` (ciudad), `calles` o `estrato` (nada que enseñar). `piezas` cuenta las de todos los cortes del planeta.

### Probar sin BeatStep

1. Cinco `Forzarciclo` alternando `Tema` (con `Temaenciclo` el cambio espera al fin de ciclo), con `Sembrarzona` y `Sembrarzona2` antes de cada uno: quedan cinco conchas de temas alternos.
2. `Padprueba` en un pad que corte (2, la caja) y `Erosionar`: el corte enseña troncos fósiles, basalto, cimientos y sótanos, primero en cian.
3. `Unirprueba`: dos cortes vecinos seguidos. En naturaleza, un cañón; en ciudad, una galería de metro.

### Autoprueba

Comprueba que los cortes son los pads con profundidad y, con cinco eras de temas alternos:
- que un corte enseña varias eras de los dos temas, con troncos fósiles y piezas de ciudad;
- que las piezas solo están dentro del corte;
- `Detalleexpuesto` (6, 2 y 0) y una pieza por era antes de repetir;
- la cicatriz (cian y después su color) y que una concha sin registro no enseña piezas;
- la línea `CORTE` con las eras y con la unión;
- la galería de metro en la ciudad, que se entierra con su mundo, y el cañón en naturaleza;
- `Unircortes` apagado y pasada `Ventanaescalada`: no se unen.

---

## FASE 17 · Tiempo: tempo, transporte y cambio de pattern

### Qué hace

Las señales de tiempo dejan de ser solo reloj y se ven en el paisaje.

- **Pulso.** Un contador de beats que avanza con el tempo del proyecto (el que escribe midicontrolx desde el BeatStep) y se pone a 0 con el START. Si `Masterbeat` señala un CHOP (por ejemplo `master_beat`), sigue su primer canal: si trae fracción de beat, tal cual; si cuenta beats enteros, cada beat lo pone él y la fracción sale del tempo. Todo lo que respira va en fase con el pulso, a saltos de stop-motion como los tránsitos (`FOTOS_PASO` por paso).
  - **Naturaleza:** el dosel se balancea: hasta `Swaymax` grados, un vaivén cada dos beats, con una onda suave de este a oeste. Los árboles que se inclinan hacia su capital (etapa *inclinar*) no se balancean. Sobre los bosques ramificados (desde la ramificación), las esporas derivan.
  - **Ciudad:** tráfico de puntos por las carreteras de la fase 13: `Trafico` por tramo, un tramo cada dos beats (con más BPM, más deprisa), faros claros a la ida y pilotos rojos a la vuelta. Las ventanas de los edificios parpadean: en cada beat, algunos edificios cambian (el mapa logístico, sin azar).
- **Ventanas.** El shader de la piel ya tenía ventanas ámbar, apagadas hasta ahora. Desde la fase 17 cada edificio lleva su nivel (0 a 4) en el alfa de su instancia, junto a la rugosidad (alfa = rugosidad + 2 × nivel), y se enciende esa parte de sus ventanas: 1 de cada 4 … todas. El uniforme `uVentanas.x` lo da el motor (0 antes de la fase 17).
- **Transporte.** Con la línea de tiempo parada, o si lo último que mandó el BeatStep fue un STOP, el pulso se congela: el mundo queda quieto pero visible (la leyenda dice `PARADO`). PLAY o START lo reanudan; START lo pone a 0.
- **Frente.** Un cambio de pattern (el aviso de la fase 6: una ráfaga de All Notes Off sin STOP) o `Frenteprueba` lanza una banda de polo sur a polo norte en `Pasosfrente` pasos (16: un compás a 4/4).
  - **Naturaleza:** frente meteorológico. Una banda de nubes del color de la estación nueva, que dobla hacia el norte los árboles por los que pasa (hasta 24°) y tiñe la luz poco a poco.
  - **Ciudad:** ola de ventanas. Por donde ya ha pasado, las ventanas toman el estado de la estación nueva: se encienden o se apagan.
- **Biblioteca de patterns.** Cada pattern deja su **firma** (las notas de un compás de cada secuenciador) y su **estación** (el tinte de la luz y si las ventanas están encendidas). Al cambiar, la firma del que se va se guarda. A mitad del frente, lo que ya ha sonado del nuevo se compara con la biblioteca (parecido del coseno, desde 0,8):
  - si lo **reconoce**, el frente devuelve el tinte y las ventanas que tuvo la última vez: la estación que vuelve;
  - si no, es un pattern **nuevo** (B, C...): estrena un tinte (tonos por el ángulo áureo, como la paleta de las conchas) y la ciudad cambia de ventanas.

  El primer pattern (A) es la luz sin tinte.
- **La luz.** Desde la fase 17 el color de `luz_principal` lo da el motor: la luz cenital fría de la fase 10 (0,82 0,90 1,00) por el tinte de la estación. Lo pone `install_core` al relanzar cualquier fase (`tiempo_al_dia`).

### Parámetros (página Fase17)

`Swaymax` 6 (*Balanceo máximo del dosel*, grados) · `Trafico` 2 (*Puntos de tráfico por tramo*, 0–8) · `Pasosfrente` 16 (*Pasos que tarda el frente de polo a polo*) · `Masterbeat` (vacío: *CHOP de master_beat*; vacío, el pulso lo cuenta el motor) · `Frenteprueba`

### Leyenda

```
TIEMPO   120 bpm   beat 2/4   frente 6/16   pattern B (nuevo)   biblioteca 2
TIEMPO   120 bpm   beat 4/4   pattern A (conocido)   biblioteca 2   PARADO
```

### Probar sin BeatStep

1. Naturaleza con un bosque (`Sembrarzona` y unos `Sembrar`), la línea de tiempo en marcha: el dosel se balancea y salen esporas. Para la línea de tiempo: todo se queda quieto.
2. `Frenteprueba`: la banda de nubes cruza el planeta de sur a norte y la luz cambia de tinte.
3. Ciudad con dos zonas (`Sembrarzona` en dos `Nota` separadas): las carreteras llevan tráfico; cambia el tempo del proyecto y mira cómo corre. `Frenteprueba`: la ola de ventanas.

### Autoprueba

Comprueba:
- el pulso a 120 y a 60 BPM, que STOP y la línea de tiempo parada lo congelan, y que START lo pone a 0;
- el dosel que se balancea (y quieto con `Swaymax` 0) y las esporas;
- el frente: la banda de nubes en el ecuador a mitad de camino, los árboles doblados hacia el norte y la luz tenida;
- la biblioteca: pattern nuevo (B), su estación al final del frente, y el A reconocido con su tinte al volver;
- la leyenda `TIEMPO` y el frente que lanza el aviso de la fase 6;
- en la ciudad: `Trafico` puntos por tramo que se mueven con el pulso, el nivel de las ventanas en el alfa, el parpadeo y la ola de ventanas.

---

## FASE 18 · Escenas de prueba y dirección temática

### Qué hace

Cierra las dos escenas acotadas, naturaleza y ciudad, como presets listos para actuar.

- **Escenas por tema.** Cada escena guarda, en la tabla `escenas` (escena, parámetro, valor):
  - el tema: `Tema`;
  - la paleta: `Paleta`, `Paletatono`, `Paletacroma`;
  - los umbrales: `Umbralvecindad`, `Pesovecina`, `Mincluster`, `Umbraldensidad`;
  - el compuesto: `Caos`, `Maxpiezas`;
  - el material: `Rugmin`, `Rugmax`;
  - el pulso: `Swaymax`, `Trafico`;
  - la luz: `Luzcalida` y el dimmer de `luz_principal` y `luz_relleno`.

  `Escena` las carga, también el `Tema`: con `Temaenciclo`, el cambio espera al fin de ciclo. `Guardarescena` guarda lo que haya en la escena elegida y `Cargarescena` vuelve a ella. **Al instalar la fase no se carga nada**: tus valores se quedan hasta que elijas una escena.

  | Escena | Paleta | Umbralvecindad | Caos | Maxpiezas | Rugosidad | Swaymax | Tráfico | Luz |
  |---|---|---|---|---|---|---|---|---|
  | naturaleza | generaciones, tono 20, croma 0,09 | 4 | 3,91 | 6 | 0,05–0,85 | 6 | 2 | cálida 0,35; principal 1,15, relleno 0,16 |
  | ciudad | mineral, tono 205, croma 0,06 | 4,5 | 3,74 | 5 | 0,10–0,90 | 4 | 3 | fría; principal 1,0, relleno 0,24 |

  `Luzcalida` (0–1) lleva la luz cenital fría de la fase 10 hacia una luz de día (1,00 0,88 0,72); el tinte de la estación (fase 17) va encima.
- **Luz local**, sin luces nuevas: solo el destello de la fase 9 es una luz de verdad. Todo son emisivos aditivos e instancias, en la geometría `luz_local` (material constante que suma, como la luz de las conchas):
  - **focos ámbar** en las obras a medias de la ciudad: la lámpara en una esquina y su charco de luz en el suelo;
  - **brillo de las brasas** de lo que arde (fase 14): un charco naranja y un halo a saltos, con la chispa;
  - **la nube de polvo** de los derrumbes y accidentes, iluminada, que crece y se apaga con el polvo.
- **Capas de diagnóstico** (geometría `diagnostico`, con `Diagnostico` encendido):
  - los **puentes** de los clusters, en blanco;
  - las **rutas** del tejido: carreteras en amarillo y ríos en azul;
  - la **presión** de cada celda, en una barra verde que pasa a roja desde `Umbralvecindad`.

  El modo actuación las oculta, como la retícula y la leyenda.
- **Criterios de cierre**, comprobados por la autoprueba y por la sesión de 20 minutos:
  - la densidad se mantiene por debajo del 60 % sin intervención;
  - una formación grande se distingue de una pequeña a distancia de cámara;
  - los fotogramas se mantienen estables con el máximo de piezas;
  - ningún tránsito queda colgado tras un fin de ciclo.

### Sesión de 20 minutos

`python3 pruebas/sesion_escena.py` hace, sobre el motor y sin TouchDesigner, una sesión de 20 minutos por escena a 120 BPM y 30 fotogramas por segundo:
- **SEQ1** en semicorcheas, con un cambio de pattern cada 4 minutos (A, B, A, C, A) por una ráfaga de All Notes Off;
- **SEQ2** cada 3 pasos;
- **batería:** el bombo a negras 16 compases sí y 16 no (desde la fase 7 v12, impulso), la caja (corte) cada 8 compases y un arañazo cada 4.

Cada medio segundo dibuja las instancias y mide la densidad, las piezas y lo que tarda `build_instances` en Python. No son los fotogramas de TouchDesigner, pero crecen con ellos.

| Escena | Bombo | Eras (compases) | Frentes | Radio final | Piezas máx. | Densidad máx. | Semilla / coronación | build_instances (mediana, p95) |
|---|---|---|---|---|---|---|---|---|
| naturaleza | erosión (motor v42) | 5 (27–188) | 4 | 9,9 | 263 | 42 % | 11 / 99 px | 2,4 / 4,3 ms |
| naturaleza | impulso, capacidad (motor v43) | 8 (27–112) | 4 | 10,5 | 469 | 58 % | 11 / 94 px | 4,9 / 7,5 ms |
| naturaleza | impulso, pulsos (motor v45) | 15 (25–62) | 4 | 11,0 | 528 | 59 % | 10 / 90 px | 5,6 / 7,5 ms |
| ciudad | erosión (motor v42) | 2 (74 y 209) | 4 | 8,5 | 319 | 54 % | 13 / 115 px | 3,6 / 6,0 ms |
| ciudad | impulso, capacidad (motor v43) | 11 (34–81) | 4 | 11,0 | 485 | 64 % (1 % del tiempo) | 10 / 90 px | 5,5 / 9,4 ms |
| ciudad | impulso, pulsos (motor v45) | 17 (23–57) | 4 | 11,0 | 500 | 62 % (1 % del tiempo) | 10 / 90 px | 6,1 / 9,0 ms |
| naturaleza | naturaleza legible (motor v46) | 15 | 4 | 11,0 | 815 | 59 % | 10 / 90 px | 13,0 / 30,2 ms |
| ciudad | naturaleza legible (motor v46) | 17 | 4 | 11,0 | 500 | 62 % (1 % del tiempo) | 10 / 90 px | 6,5 / 8,4 ms |

Las seis cumplen los cuatro criterios. Con el bombo erosionando, las eras de la ciudad duraban unos 10 minutos: la batería no dejaba madurar el mundo (*el breakdown entierra el mundo*).

**Con el bombo en impulso (fase 7 v12) las eras se acortan,** al revés de lo que esperaba el encargo. Todas las de la naturaleza y 8 de las 11 de la ciudad se cierran por estancamiento (las otras 3, por edad máxima). El bombo era la principal fuente de novedad mientras sonaba; ahora hincha la celda y le da capacidad, pero no cambia su forma, así que el mundo madura y se asienta antes. La capacidad retrasa el desborde, pero en esta sesión pesa más la novedad que se pierde. Hay casi el doble de piezas y más densidad (la ciudad pasa del 60 % un 1 % del tiempo, dentro del criterio del 5 %), y `build_instances` tarda el doble, con fotogramas estables. Sin compensar, como pide el encargo: a vigilar con el aparato (prueba pendiente 11 de `MONTAJE_FASES_3_10.md`).

**Con los pulsos de ocupación (fase 7 v14) se acortan más,** como avisaba el encargo: cada bombo suma 3 triggers y el tom 2, así que las celdas maduran antes y el mundo se asienta antes. Todas las eras de las dos escenas se cierran por estancamiento: 15 en la naturaleza y 17 en la ciudad, de 23 a 62 compases (un minuto largo cada una). La densidad y las piezas apenas cambian respecto a la capacidad. Sin compensar: a vigilar con el aparato.

**Con la naturaleza legible (motor v46)** las dos escenas siguen cumpliendo los cuatro criterios. La ciudad no cambia. La naturaleza tiene más piezas (815: las copas del borde del dosel) y su `build_instances` de muestra tarda el doble que antes (13 ms de mediana) porque cada muestra, medio segundo después de la anterior, encuentra casi siempre la ocupación de alguna montaña cambiada y rehace el mapa de alturas. En un fotograma sin cambios, como la mayoría en TouchDesigner, la naturaleza tarda 3,9 ms frente a 3,5 ms de la ciudad (sesión de 5 minutos). La primera versión del dosel colonizaba el cluster entero en cada cambio y llegaba a 180 ms de p95: se corrigió (ver *La naturaleza legible*).

### Parámetros (página Fase18)

`Escena` (naturaleza / ciudad) · `Guardarescena` · `Cargarescena` · `Luzcalida` 0 (0–1) · `Diagnostico` (apagado)

### Leyenda

```
ESCENA   ciudad   densidad 42%   piezas 310   luz local 12   transitos a medias 0   diagnostico
```

`(>60%)` aparece junto a la densidad cuando pasa del umbral.

### Probar sin BeatStep

1. `Escena` ciudad: cambian la paleta, `Caos`, la luz... `Avance` en gates y `Sembrarzona2` en dos zonas: las obras a medias llevan focos.
2. `Escena` naturaleza, un bosque denso y `Escalar` (fase 14): brillan las brasas.
3. `Diagnostico`: puentes, rutas y presión. `Modoactuacion` los oculta.

### Autoprueba

Comprueba:
- cargar la escena de la ciudad; guardar, cambiar de escena y volver; `Cargarescena`;
- los focos de las obras a medias, el brillo de las brasas y la nube de polvo;
- el diagnóstico (puentes y presión), que se oculta en actuación y con `Diagnostico` apagado;
- que ningún tránsito queda colgado tras `Forzarciclo` y el tamaño en píxeles de una semilla y una coronación;
- la línea `ESCENA` de la leyenda.

---

## FASE 19 · Señales del modular

*Primera fase de «Después de la fase 18» del plan.*

### Qué hace

Cuatro señales de control del modular modulan cómo se ve el mundo, en el nivel de los moduladores (como la velocidad y el gate de la fase 12): no cambian el mundo. Llegan como **valores de control**, el voltaje convertido, y **nunca como análisis del audio**: el marco no lo quiere, y analizar el sonido volvería la pieza visualización reactiva.

| Señal | Naturaleza | Ciudad |
|---|---|---|
| **LFO** | viento en el dosel: hasta `Vientomax` grados (12) a un lado y al otro, encima del balanceo del pulso (fase 17) | las ventanas respiran: con el LFO abajo se apagan hasta `Respiracion` (0,75) |
| **ruido** | más esporas sobre los bosques (de 3 a 12 por celda) | smog: una bruma parda que deriva sobre los edificios (`Smog`) |
| **espacialidad** | niebla de distancia: lo lejano se funde con la bruma (`Niebla`) | igual |
| **saturación** | fracturas (vetas oscuras) y glitch (bloques con los canales cambiados) en los materiales de la piel (`Glitch`) | igual |

- **La niebla**: en la piel la calcula su shader (`uNiebla`: cantidad, dónde empieza y dónde es total; `uNieblaCol`). Para los materiales Phong y constantes, la cámara lleva una niebla lineal que la sigue (`modular_al_dia`). Empieza en la cara del planeta que mira a la cámara; con espacialidad 1, el borde del planeta ya es casi todo bruma.
- **Sin señal, reposo.** Si en 2 segundos no llega nada, las señales vuelven solas al reposo: el LFO al centro (sin viento) y lo demás a 0. Las ventanas no respiran. Un proyecto sin modular se ve como en la fase 18.

### De dónde llegan (`Fuentemodular`)

La decisión del plan seguía abierta (*¿Cómo llegan los voltajes del modular a TouchDesigner? Por confirmar: el BeatStep Pro no tiene entradas de CV*), así que la fase acepta varias fuentes:

- **osc** (por defecto): OSC por UDP al puerto `Puertoosc` (9000), con las rutas `/estratos/lfo`, `/estratos/ruido`, `/estratos/espacio` y `/estratos/saturacion`. Vale cualquier ruta que acabe así; si ningún canal se llama así, se toman los cuatro primeros, en ese orden. Lo recibe el OSC In CHOP `modular_osc`. Sirve para un conversor de CV a OSC o un ordenador o microcontrolador que lea los voltajes.
- **chop**: cualquier CHOP (`Chopmodular`, su ruta), por ejemplo una interfaz de audio acoplada en continua (Expert Sleepers ES-8 o ES-9 en un Audio Device In CHOP) o los CC de un conversor de CV a MIDI. Se lee su valor actual; no se analiza.
- **manual**: los deslizadores `Lfo` (0,5: sin viento), `Ruido`, `Espacio` y `Saturacion`.
- **prueba**: un generador sin azar: un LFO de 4 s, un ruido que salta cada medio segundo por el mapa logístico, una espacialidad que va y viene en 20 s y ráfagas de saturación de 1 s cada 8.

`Rangomodular` dice en qué rango llegan (0..1, -1..1, 0..10 V, -5..5 V, -10..10 V) y `Suavizado` (0,15 s) las alisa.

### Parámetros (página Fase19)

`Fuentemodular` (osc / chop / manual / prueba) · `Puertoosc` 9000 · `Chopmodular` · `Rangomodular` (0..1; también -1..1, 0..10 V, -5..5 V, -10..10 V) · `Suavizado` 0,15 · `Lfo` 0,5 · `Ruido` 0 · `Espacio` 0 · `Saturacion` 0 · `Vientomax` 12 · `Respiracion` 0,75 · `Smog` 1 · `Niebla` 1 · `Glitch` 1

### Leyenda

```
MODULAR  osc :9000   lfo 0.62   ruido 0.10   espacio 0.40   saturacion 0.00   hace 0.1 s
MODULAR  osc :9000   lfo 0.50   ruido 0.00   espacio 0.00   saturacion 0.00   sin senal
```

### Probar sin el modular

`Fuentemodular` = prueba: el dosel se mueve con el viento, la niebla va y viene y cada ocho segundos los materiales se fracturan. O `Fuentemodular` = manual y mueve los deslizadores.

### Autoprueba

Comprueba:
- los rangos y la elección de canales;
- el suavizado;
- el viento en el dosel a un lado y al otro y las esporas con el ruido;
- la niebla (`uNiebla` y la cámara) y el glitch (`uGlitch`);
- en la ciudad, las ventanas que respiran y el smog;
- el generador de prueba (cambia, y es el mismo en el mismo instante);
- que sin mensajes OSC las señales vuelven al reposo;
- la línea `MODULAR`.

---

## Calibración de la vista (motor v37, comun v29)

### Qué pasaba

Medido con el motor en una sesión simulada de 20 minutos a 120 BPM (SEQ1 de 16 pasos, SEQ2 cada 3 pasos; con y sin batería, que erosiona a negras 16 compases sí y 16 no):

- **Eras de 20 segundos.** Con los valores del proyecto (`Umbralnovedad` 0,378, `Herencia` 0,125, `Growstep` 0,04) y `Ciclomin` 8, sin batería, el mundo se enterraba cada 9 o 10 compases, en cuanto llegaba al límite: 61 conchas en 20 minutos. Tres causas juntas: el umbral de novedad alto da el mundo por quieto enseguida; con poca herencia el mundo nuevo arranca casi vacío y madura en cuanto el pattern llena sus celdas; y con `Growstep` pequeño la formación se queda baja, y como el coste de cada escalón sube con la altura, madura con pocas notas.
- **Un planeta que no paraba de crecer.** El radio era el tiempo: `Shellthick` por cada `Ciclomin` compases. A los 20 minutos, radio 25 con los valores del proyecto y 42 con los de por defecto, sobre un núcleo de 6. La cámara se alejaba con cada concha y las formaciones (límite ~2) acababan siendo motas.
- **Un salto de altura.** Con `Growstep` 0,04, `Semillafrac` 0,18 y `Umbralram` 6, la formación iba del 18 al 34 % y al ramificarse saltaba al límite de golpe.

### Qué cambia

| Parámetro | Antes | Ahora | Por qué |
|---|---|---|---|
| `Ciclomin` (Fase6) | 8 | 16 | Una era dura al menos 32 s a 120 BPM |
| `Compasesquietos` (Fase6) | 2 | 3 | El mundo tiene que estar quieto 3 compases para enterrarse |
| `Grosormax` (Fase8) | 2,0 | 1,5 | La concha de un mundo largo no domina el corte (48 compases o más) |
| `Cortezamax` (Fase8, nuevo) | — | 4 | **Compactación:** la concha nueva aplasta las viejas; la corteza tiende a 4 y el planeta deja de engordar (ver fase 8 en `MONTAJE_FASES_3_10.md`) |
| `Umbralnovedad`, `Ciclomax`, `Herencia` | 0,15 · 64 · 0,25 | igual | Los valores por defecto ya eran buenos; `ajuste_vista.py` los devuelve ahí |
| `Growstep` | — | (1 − `Semillafrac`) / (`Umbralram` − 1) | Escalones iguales de la semilla al límite; con los valores por defecto ya lo es (0,2) |

**Cómo llega a un proyecto en marcha.** Relanzar cualquier fase (comun v29) cambia `Ciclomin`, `Compasesquietos` y `Grosormax` solo si seguían en el valor por defecto viejo, crea `Cortezamax` en la página Fase8 y avisa con `..` si la altura salta al límite. Lo ajustado a mano no se toca. Para ponerlo todo en los valores calibrados, incluido lo tocado a mano, está `ajuste_vista.py`:

```python
exec(open('C:/Users/DareDave/Downloads/est/ajuste_vista.py').read())
```

No cambia el nivel ni el mundo. Pone `Ciclomin` 16, `Compasesquietos` 3, `Umbralnovedad` 0,15, `Ciclomax` 64, `Herencia` 0,25, `Cortezamax` 4, `Grosormax` 1,5 y el `Growstep` sin salto. Dice qué ha cambiado (`antes -> ahora`) y escribe la línea para volver a lo de antes. No toca `Shellthick`, `Alturafactor`, los umbrales de la fase 4, la cámara ni el tema. Lo ya enterrado no adelgaza de golpe, porque el radio nunca baja; para verlo desde el principio, `Resetmundo` (página Fase3).

### Resultado (simulación, 20 minutos)

| Caso | Sin batería: eras · compases de media · radio a 2/5/10/20 min | Con batería: eras · compases · radio |
|---|---|---|
| Proyecto, antes | 61 · 9,7 · 8,0 / 10,8 / 15,5 / 25,2 | 23 · 25,4 · 7,8 / 10,4 / 15,5 / 24,5 |
| Por defecto, antes | 12 · 47,9 · 8,9 / 11,9 / 15,9 / 25,9 | 19 · 30,9 · 8,8 / 14,7 / 22,6 / 42,2 |
| Por defecto, ahora | 12 · 48,5 · 7,5 / 8,7 / 9,8 / 10,8 | 13 · 45,3 · 7,3 / 8,4 / 9,7 / 10,8 |
| Proyecto + `ajuste_vista.py` | 11 · 50,8 · 6,6 / 7,5 / 8,8 / 10,1 | 5 · 118 · 6,4 / 7,4 / 8,1 / 9,1 |

Las conchas visibles, de la más nueva a la más vieja, con los valores por defecto: 1,5 · 1,06 · 0,74 · 0,51 · 0,35 · 0,24 · 0,17 · 0,11: las recientes se leen como bandas y las viejas como vetas.

Con `Umbralram` 6 (el del proyecto) y una batería que erosiona sin parar, el mundo tarda más en madurar: eras de ~4 minutos. Es lo esperado (*el breakdown entierra el mundo*); con `Umbralram` 5 bajan a ~50 compases.

### Autoprueba

La de la fase 8 (v10) comprueba que con `Cortezamax` 4 el radio nunca baja y sube al menos un 10 % de cada concha; que 40 conchas de 0,5 dejan una corteza de menos de 6 (sin compactar, 20); que la concha nueva conserva su grosor y las viejas son más finas cuanto más hondas; que compactada, cada columna sigue en el radio nominal; y que la laguna de un corte se compacta como sus conchas. Las demás comprobaciones de las fases 8 y 9 se miden sin compactar.

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

**Fase 11 v5 · naturaleza legible.** Causa encontrada: los modelos de naturaleza eran compuestos del juego del caos sobre un L-system de 30° y el árbol madre, y el latido mezclaba al 75 % el tinte del secuenciador o del pad en su albedo; la paleta de conchas generaba verdes que camuflaban el bosque. La concha no pasaba al albedo de los modelos.

| Decisión | Alternativa descartada | Motivo |
|---|---|---|
| Por encima del bosque sube el terreno | Más piezas apiladas (árbol madre, caos) | A escala de globo el apilado es ruido |
| Pisos por altura relativa al suelo local | Por radio absoluto | El planeta crece y los pisos se moverían |
| Tinte del SEQ al borde (fresnel, focos uTinte) | Tinte en el albedo | El verde es lo que dice «naturaleza» |
| Dosel por colonización del espacio, una parte por celda abierta a sus vecinas del cluster | Copas sueltas por celda; colonizar el cluster entero de golpe | Masa única sin solapes; el cluster entero tardaba ~100 ms en cada cambio |
| Cordillera como malla por cluster | Columnas por celda | Silueta continua legible |
| Una sola esfera desplazada en el shader por un mapa de alturas (Script TOP) | Un Script SOP que rehace la malla en Python | Sin reconstruir geometría: solo una textura cuando cambia la ocupación |
| El mapa se rehace con la ocupación, no con el stop-motion | Seguir la altura visible fotograma a fotograma | Rehacerlo 24 veces por segundo no cabe en el fotograma; la cumbre salta a su altura nueva |
| Escalera por los umbrales (`Umbralram`, `Umbralfusion`) y `Umbralmonte` aparte | Los números del encargo (4–5, 6–7) | Como en el resto de la piel: cambiar un umbral cambia la piel |
| Puntos de atracción por hash determinista | El mapa logístico | Sus ternas casi se repiten: la cúpula de una celda suelta quedaba vacía |
| Banda verde reservada desde 120° | Desde 100° (todo el verde amarillento) | Con menos tono libre dos conchas seguidas dejarían de diferir 60° |

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

**Fase 13 v2 · ríos azules.** Causa encontrada: ocultos (bajo las formaciones y bajo la loseta de luz, que además los teñía), la paleta de conchas con azules y verdes, y sin emisivo en la cara de sombra. El color por instancia no estaba sobrescrito.

| Decisión | Alternativa descartada | Motivo |
|---|---|---|
| Azul reservado y excluido de la paleta | Azul libre | Se camuflaba con conchas azules |
| Cinta que bordea | Caja que pasa por debajo | Quedaba tapada |
| Bajada por el suelo real | Hacia la vecina menos ocupada | Hoy el planeta tiene relieve |
| Emisivo bajo | Solo difuso | Se perdía en la cara de sombra |
| Geometría y material propios (`rios`, `mat_piel_agua`) | Seguir en `tejido` con el mineral | Ningún tinte ni borde puede tocarlos |

### Decisiones tomadas en la fase 14

| Pregunta | Decisión |
|---|---|
| ¿Qué pads son arañazos? | Los que no cortan (perfil sin profundidad), no los números 1–5: con los perfiles del usuario, 4–8 |
| ¿Qué es la vecindad? | La celda objetivo y sus vecinas. Dos golpes son de la misma zona si el objetivo de uno está en la vecindad del otro |
| ¿Qué tala el rayo? | La formación más alta de la vecindad (en empate, la de índice menor) baja un estado, si la erosión no la ha bajado ya |
| ¿El golpe que escala también es un accidente? | No: es la catástrofe, y el cluster de la catástrofe es el de antes de ese golpe |
| ¿El fuego salta fuera del cluster? | No (decisión del plan). Solo por los enlaces del cluster de su especie |
| ¿Cómo se propagan las otras catástrofes? | El derrumbe y el derrumbe en cadena, igual que el fuego; la implosión, de golpe y sin propagarse |
| ¿Cuánto dura la huella? | Hasta la siguiente nota de construcción en su celda, un corte o el fin de ciclo |
| ¿Qué es el presupuesto del 60 %? | Por encima de `Umbraldensidad`, la catástrofe empieza en la celda y sus vecinas del cluster |
| ¿Qué para un derribo? | Una nota en el cluster, o que la obra llegue al principio |

### Decisiones tomadas en la fase 15

| Pregunta | Decisión |
|---|---|
| ¿El cambio de tema es inmediato o espera al fin de ciclo? | Espera (`Temaenciclo`, encendido por defecto); apagado, inmediato |
| ¿Cómo convive la materia con la paleta de generaciones? | Se mezcla con el color de la generación (carbón 85 %, basalto y hormigón 60 %); lo vacío de la naturaleza queda con su color |
| ¿Qué es la traza de las calles en la concha? | Las celdas por las que pasaban las carreteras, más oscuras |
| ¿Cuándo hay banco de semillas? | Cuando el mundo nuevo es de naturaleza (venga de lo que venga) y `Rebrote` está encendido |
| ¿Cuándo hay trazas? | Cuando el mundo nuevo es una ciudad y lo enterrado también lo era |
| ¿Cuánto pesa una traza? | Coste 1 − 0,9 × `Pesotraza` por tramo, en el árbol y en el camino de cada arista |
| ¿Brillo del carbón? | Las conchas pasan al shader de la piel (mineral), con la rugosidad de cada loseta |

### Decisiones tomadas en la fase 16

| Pregunta | Decisión |
|---|---|
| ¿Qué pads cortan? | Los que tienen profundidad en su perfil (con los del usuario, 1–3), no «6–8» |
| ¿Dónde se ven las piezas? | En el fondo de cada celda del corte y en las paredes de sus vecinas más altas, asomando hacia el corte |
| ¿Qué cuenta como corte? | Toda celda con el suelo por debajo del radio nominal: también las hondonadas de mundos anteriores |
| ¿Qué es «la misma vecindad» de dos cortes? | El objetivo del segundo dentro del primero o en su borde (radio + 1) |
| ¿Cómo se ve una galería de metro? | Falso túnel: una zanja de una loseta con la bóveda dentro; se entierra con su mundo |
| ¿Hasta dónde baja el cañón? | La profundidad del menor de los dos cortes, con el tope por mundo de la fase 9 |

### Decisiones tomadas en la fase 17

| Pregunta | Decisión |
|---|---|
| ¿Qué es `master_beat`? | Un CHOP opcional (`Masterbeat`). Sin él, el motor cuenta beats con el tempo y los pone a 0 con el START del BeatStep |
| ¿Qué para el pulso? | La línea de tiempo parada o un STOP del BeatStep (hasta el siguiente START) |
| ¿Hacia dónde va el frente? | De polo sur a polo norte, y los árboles se doblan hacia el norte |
| ¿Cómo se reconoce un pattern? | Por las notas de un compás de cada secuenciador (no el orden), con un parecido de 0,8 o más. La fase 6 v2 había quitado la biblioteca anterior; esta es nueva y solo sirve para la estación |
| ¿Cuándo se decide si es conocido? | A mitad del frente, con lo que ya ha sonado del pattern nuevo |
| ¿Cómo llegan las ventanas al shader? | En el alfa de cada instancia (rugosidad + 2 × nivel), sin geometría nueva |
| ¿Cómo se tiñe la luz? | El color de `luz_principal` sale del motor; también lo ven los materiales Phong |

### Decisiones tomadas en la fase 18

| Pregunta | Decisión |
|---|---|
| ¿Qué guarda una escena? | Tema, paleta, umbrales de vecindad y densidad, `Caos`, `Maxpiezas`, rugosidad, pulso y luz (`Luzcalida` y dimmers). No el mundo |
| ¿Dónde se guardan? | En la tabla `escenas` de FASE1, que viaja con el .toe |
| ¿Se carga una escena al instalar? | No: los valores del proyecto se quedan hasta que se elige una |
| ¿Luz local con luces? | No: emisivos aditivos e instancias (`luz_local`); la única luz nueva sigue siendo el destello de la fase 9 |
| ¿Qué capas de diagnóstico había? | Ninguna: la fase 18 las crea (puentes, rutas y presión) y el modo actuación las oculta |
| ¿Cómo se miden los 20 minutos? | Fuera de TouchDesigner (`pruebas/sesion_escena.py`); los fotogramas reales quedan para el aparato |

### Decisiones tomadas en la fase 19

| Pregunta | Decisión |
|---|---|
| ¿Cómo llegan los voltajes del modular? | Sigue abierta en el plan. La fase acepta OSC por UDP (lo previsto), cualquier CHOP (interfaz acoplada en continua, CV a MIDI), deslizadores y un generador de prueba |
| ¿Análisis del audio? | No: solo valores de control |
| ¿Qué pasa sin señal? | A los 2 s vuelven al reposo (LFO al centro, lo demás a 0): un proyecto sin modular se ve igual |
| ¿Dónde se calcula la niebla? | En el shader de la piel (`uNiebla`) y, para lo demás, en la niebla lineal de la cámara |

---

### Cómo se ha probado

Sin TouchDesigner a mano, con un **TouchDesigner simulado** que ejecuta los scripts tal cual (`pruebas/td_simulado.py`): operadores y rutas, parámetros con expresiones, páginas propias, storage, el módulo de los Text DAT, Script CHOP, Table DAT y el tiempo del proyecto. Los COMP solo aceptan los parámetros que tienen en TouchDesigner.

```
python3 pruebas/correr_fases.py        # base y fases 3 a 19 desde cero, sesión, relanzar y otra sesión
python3 pruebas/sesion_escena.py       # 20 minutos por escena y los criterios de cierre de la fase 18
python3 pruebas/vista_previa.py        # hoja de contactos del catálogo (pruebas/catalogo.png)
xvfb-run -a python3 pruebas/glsl_piel.py   # compila y dibuja el shader de la piel con OpenGL (necesita moderngl)
```

- **Desde cero**: `fase12_base.py` y las fases 3 a 19, todas con `AUTOPRUEBA OK`.
- **Sesión simulada** de 48 compases a 120 BPM (entierra un mundo) con SEQ1, SEQ2 y batería por los bytes MIDI, fotograma a fotograma: todas las expresiones de todos los nodos se evalúan sin error.
- **Relanzar** las fases 3 a 19 sobre el proyecto ya en la última (también la 11, que crea las geometrías del nivel en que esté): todas OK, el mundo se conserva y otra sesión corre sin errores.
- **El shader de la piel** (fase 12): se compila con un OpenGL 4.5 de verdad (Mesa, sin pantalla, con Xvfb), sustituyendo las funciones de TouchDesigner (`TDDeform`, `TDInstanceColor`, `uTDMats`...) por otras equivalentes. Se dibuja con las instancias reales del motor: obsidiana y vidrio negro pulidos a velocidad alta, pómez y hormigón con poros a velocidad baja, y la vegetación (desde el motor v32) en dos verdes con los lados pardos.
- **Catálogo**: una hoja de contactos dibujada con un rasterizador propio (`pruebas/vista_previa.py`) para ver cada modelo, y escenas de los dos temas con clusters, puentes, coronaciones e híbridos.
- **Fase 14**: un incendio en un bosque denso, dibujado con el shader real: el dosel de lo que arde se tiñe de brasa y se carboniza, y lo que se vacía queda como claro de ceniza. La fase 14 añade sus tres modelos a un proyecto cuya fase 11 se hizo con un motor anterior (`modelos: 3 nuevos`).
- **Fase 15**: un mundo de naturaleza enterrado bajo una ciudad, dibujado con el shader real: un corte en el bosque deja ver las losetas de carbón, negras y con brillo, bajo el hormigón mate de la ciudad.
- **Fase 16**: cinco eras de temas alternos y un corte con la caja, dibujados con el shader real: troncos fósiles claros en las paredes de carbón, cimientos en el fondo y, con dos cortes vecinos en la ciudad, la bóveda de la galería en su zanja. La fase 16 añade sus siete modelos a un proyecto cuya fase 15 se hizo con el motor anterior (`modelos: 7 nuevos`).
- **Fase 17**: una ciudad con las ventanas ámbar encendidas por edificio y un planeta de naturaleza con la banda de nubes del frente a mitad de camino, dibujados con el shader real. Al pasar un proyecto de la fase 16 a la 17, `luz_principal` toma su color del motor y `uVentanas` pasa a 1.
- **Fase 18**: la sesión de 20 minutos por escena (ver arriba) cumple los cuatro criterios de cierre.
- **Fase 19**: el shader de la piel con la niebla de distancia y con las fracturas y el glitch, dibujado con OpenGL.
- **Fase 11 v5 y fase 13 v2**: el shader con la malla del terreno (la esfera desplazada por el mapa de alturas real del motor, con la rampa de los pisos), los ríos y los focos de tinte, dibujado con OpenGL: una cordillera de 5 celdas con cumbres nevadas, roca facetada y laderas verdes, copas sobre las laderas bajo el límite del bosque y el río azul bajando. La sesión de 20 minutos de la fase 18 sirvió para encontrar el coste de colonizar el dosel por cluster (ver *La naturaleza legible*).
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
9. **Destructores (fase 14)**: con la batería, que un arañazo suelto se lee como accidente y dos seguidos en la misma zona como catástrofe; que el fuego se ve avanzar (brasas, dosel que se carboniza) y que las huellas se distinguen de las formaciones. Si el fuego se apaga demasiado pronto o arrasa demasiado, ajustar `Pasosfuego` y `Maxfuego`.
10. **El ciclo como era (fase 15)**: que las conchas con el shader de la piel se ven bien (si no, `Materialrespaldo`); que el carbón se distingue del basalto y el hormigón de sus calles; que el banco de semillas se lee como semillas y no como un fallo.
11. **Cortes temáticos (fase 16)**: con varias conchas de temas distintos y la caja, que desde la cámara de globo se ven las piezas de las paredes y del fondo (si quedan pequeñas o tapadas, dímelo y ajusto su tamaño); que la galería de metro se lee como galería y el cañón como cañón.
12. **Tiempo (fase 17)**: que el balanceo del dosel y el tráfico van a tempo y se paran con STOP; que el BeatStep manda All Notes Off al cambiar de pattern (si no, solo funciona `Frenteprueba`); que el frente se ve cruzar y que la luz de un pattern conocido vuelve. Si tienes `master_beat`, pon su ruta en `Masterbeat`.
13. **Escenas (fase 18)**: que cada escena se ve como se espera y que guardar y cargar no tocan el mundo; que los focos de obra, las brasas y el polvo se leen como luz (mezcla aditiva de `mat_luz_local`) y no tapan nada; con la sesión real de 20 minutos, los fotogramas con el máximo de piezas.
14. **Modular (fase 19)**: decidir cómo llegan los voltajes (OSC o un CHOP) y comprobar en la leyenda `MODULAR` que llegan y en qué rango. Que la niebla de la cámara existe (página Fog de `camara`; si no, solo la piel tiene niebla) y que el glitch no molesta a la lectura con saturación baja.
15. **Naturaleza legible (fase 11 v5)**: que `mat_piel_tierra` compila (clic derecho → Info) y que su página Samplers tiene `sAlturas` = `alturas` y `sRampa` = `rampa_hipso`; que `alturas` es de 32 bits float y que las montañas salen hacia fuera y en su sitio (si salen del revés en latitud, el Script TOP voltea la imagen: dímelo y lo invierto); que `modelos/veg_conifera/cono` tiene la punta arriba; a distancia de globo, que una cordillera nevada se distingue de un bosque y que el borde se enciende con la nota. Medir los fotogramas cuando cambia la ocupación de una montaña (se rehace el mapa).
16. **Ríos azules (fase 13 v2)**: que se ven azules desde la cámara de globo, también en la cara de sombra (si no, sube `Emisivorio`), y que los lagos llenan las hondonadas sin tapar las cicatrices.

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
| `render`: `Cook dependency loop detected` (con `luz_relleno`, Translate) | La cámara leía el tamaño de la imagen del render (motor v30 o anterior) | Relanza cualquier fase con motor v31 o posterior |
| `reticula`: `Rotate to Vectors is co-linear with the Up Vector` | «Rotar hacia un vector» en los polos (comun v21 o anterior) | Relanza cualquier fase con comun v22 o posterior |
| La naturaleza parece hilo de alambre (varillas oscuras, una red sobre el planeta) | Motor v31 o anterior: árboles de obsidiana y dosel de tiras | Relanza cualquier fase con motor v32 y comun v23: mira la línea `piel: N geometrias con el material de su familia` |
| El planeta se ve lejos y pequeño | `Encuadre` bajo, o motor anterior al v36 | Sube `Encuadre` (Fase10; 1 = de borde a borde) y relanza cualquier fase con motor v36 |
| La cámara se mueve todo el rato y el mundo se ve a ratos | Motor v32 | Relanza cualquier fase con motor v33: el encuadre solo cambia con una concha nueva |
| Fase 14: un arañazo no hace nada temático | El pad corta (perfil con profundidad) o la vecindad del objetivo está vacía | Los arañazos son los pads sin profundidad (con los perfiles por defecto, 4–8); toca cerca de formaciones |
| Fase 14: dos golpes no escalan | Más de `Ventanaescalada` pasos entre ellos, o zonas distintas | Sube `Ventanaescalada`, o usa `Escalar` |
| Fase 14: no se ven las huellas | Proyecto con modelos de antes del motor v34 | Relanza `fase14_destructores.py`: la línea `modelos: 3 nuevos` las crea |
| Fase 15: cambio `Tema` y no pasa nada | `Temaenciclo`: espera al fin de ciclo (lo dice la leyenda `ERA`) | `Forzarciclo`, o apaga `Temaenciclo` |
| Fase 15: las conchas salen blancas, negras o planas | El shader de la piel en `estratos` | `Materialrespaldo`, y pégame los errores de `mat_piel_mineral` |
| Fase 15: lo heredado no aparece | Banco de semillas: brota en 4 × `Pasosetapa` pasos | Espera, toca una nota en la celda o apaga `Rebrote` |
| Fase 16: el corte solo enseña bandas de color | Las conchas se enterraron antes de la fase 15 (sin registro), o estaban vacías, o `Detalleexpuesto` es 0 | Deja enterrar unos ciclos con la fase 15 o la 16 y vuelve a cortar |
| Fase 19: `MODULAR ... sin senal` | No llegan mensajes al puerto `Puertoosc`, o las rutas no acaban en lfo/ruido/espacio/saturacion | Mira el OSC In CHOP `modular_osc` (canales y valores); revisa el puerto y el cortafuegos; o `Fuentemodular` = chop |
| Fase 19: los árboles se quedan inclinados | El LFO llega fuera de rango o en reposo no vale el centro | Ajusta `Rangomodular`; con `Fuentemodular` = manual, `Lfo` 0,5 es sin viento |
| Fase 18: al elegir `Escena` no cambia nada | El cambio de `Escena` no llega al motor (el DAT `pulsos` es de una versión anterior) | Relanza la fase 18; o pulsa `Cargarescena` |
| Fase 18: la luz local tapa lo que hay detrás | `mat_luz_local` sin mezcla aditiva | En `mat_luz_local`: Blending encendido, Source y Destination en One |
| Fase 17: nada se mueve | El pulso está parado: línea de tiempo en pausa o el último mensaje del BeatStep fue un STOP (la leyenda dice `PARADO`) | PLAY en el proyecto o START en el BeatStep |
| Fase 17: no llega ningún frente | El BeatStep no manda All Notes Off al cambiar de pattern, o lo manda junto a un STOP | Prueba con `Frenteprueba`; mira el AVISO de la fase 6 en el Textport |
| Fase 17: la luz no cambia de color | `luz_principal` con su color fijo (relanzaste la fase 10 después) | Relanza la fase 17 |
| Fase 16: dos cortes no se unen | Mismo objetivo, demasiado lejos (más allá de radio + 1) o más tarde que `Ventanaescalada` pasos; o `Unircortes` apagado | Prueba con `Unirprueba`; sube `Ventanaescalada` (página Fase14) |
| Pantalla negra (solo la leyenda) tras relanzar una fase | Giro y pivote guardados en `camara` al navegar en su visor | Relanza cualquier fase con comun v28 (los pone a cero); mira el planeta en el visor del render |
| `midiout`: `Could not open the MIDI interface` | El mapeador MIDI de TouchDesigner (no es de los scripts) | Nada: la entrada MIDI funciona igual; si molesta, quita la salida en Dialogs → MIDI Device Mapper |
| Fase 12: pulido y rugoso iguales | La geometría no lee el canal `a` | En la geometría `mod_...`: Instance 2 → Color A = `a`. El informe lo avisa con `FALLO ... no lee la rugosidad` |
| Fase 11 v5: no se levanta ninguna montaña | Sin el mapa de alturas o sin el shader: el Script TOP `alturas` no tiene numpy o no está enlazado (página Samplers de `mat_piel_tierra`), o `terreno` no está en el render | Mira las líneas `..` del informe de la fase 11 (`alturas`, `samplers`); relanza `fase11_piel.py` |
| Fase 11 v5: las montañas salen en otra latitud o del revés | El Script TOP voltea la imagen respecto al motor | Dímelo: se invierte la fila en `alturas_array` |
| Fase 11 v5: el bosque sale con el color de la concha o de la nota | Proyecto con motor anterior al v46 | Relanza `fase11_piel.py` (o cualquier fase): la línea `motor cargado (motor v46)` |
| Fase 13 v2: los ríos no se ven | `rios` no está en el render o `Rios` apagado | Relanza `fase13_tejido.py`: la línea `render dibuja: ... rios ...` |
| Fase 12: el gate no cambia nada | Sin note off (el aparato no lo envía) o `Gateprueba` en los botones | Mira la línea `MOD`: sin `gate` es que no llega el note off |
