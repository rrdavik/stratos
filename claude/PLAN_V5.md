# Estratos · Plan v5: la huella inevitable

*Plan de fases para llevar el Marco conceptual v5 («La huella inevitable») al proyecto de TouchDesigner. Encargo «conceptualizar v5 stratos», 26 de octubre de 2026; numeración y decisiones cerradas el 28 de octubre de 2026. **No implementa nada.** Cada fase se revisa y se aprueba antes de pasar a código.*

**Numeración.** `main` llega a la fase 19. La 20 (POPs) está hecha en su rama y de momento no se fusiona. Lo que falta del marco v4 entra antes, en las fases 21 (micrófono), 22 (cámara, según la especificación «casilla probable») y 23 (luz de sala por DMX), descritas en «Requerimiento v4 · micrófono, cámara y DMX» y «Tareas técnicas v4 · micrófono, cámara y DMX». Las fases de este plan van de la **24 a la 31**.

| Fase | Qué hace | Marco |
|---|---|---|
| 21 | Micrófono de sala | v4 |
| 22 | Cámara cenital (casilla probable) | v4 / v5 |
| 23 | Luz de sala por DMX, balance y colapso | v4 |
| 24 | Personas | v5 |
| 25 | Huella mínima | v5 |
| 26 | Borrado por erosión | v5 |
| 27 | Clasificación al enterrar | v5 |
| 28 | Noche de enterramiento | v5 |
| 29 | Fila y escisión colectiva | v5 |
| 30 | Relámpago | v5 |
| 31 | Escisiones en el histórico | v5 |

Fuentes leídas para este plan:

- el repositorio `rrdavik/stratos` (rama `main` al 27 de octubre de 2026, commit `8fe3543`, etiqueta `v4.0`: el merge del PR #32, el conversor CV → OSC de `modular/`; revisadas también todas las ramas y PR abiertos), que es el contenido de `C:/Users/DareDave/Downloads/est`: `estratos_motor.py`, `estratos_comun.py`, los scripts de fase, `MONTAJE_FASE1.md`, `MONTAJE_FASES_3_10.md`, `MONTAJE_FASES_11_18.md` y `pruebas/`;
- los documentos *Estratos — Marco conceptual v4: El estrato humano* y *Marco conceptual v5: La huella inevitable*;
- la *Especificación TouchDesigner: casilla probable* (19 de octubre de 2026), que define la cámara de la fase 22;
- las dos hojas *Estratos_parametros* de Drive (24 y 25 de octubre de 2026).

---

## 0. Lo que hay que saber antes de leer

El inventario (apartado 1) encontró **cinco desajustes** entre lo que el encargo daba por existente y lo que hay en el repositorio. Así quedan resueltos:

1. **Nada de la sala de v4 está en el repositorio.** No hay cámara, micrófono, balance, DMX, colapso, testigos ni proyector del histórico, ni en `main` ni en ninguna rama o PR abierto. El repositorio llega a la **fase 19** (`motor v54`, `comun v36`), más el conversor CV → OSC de la fase 19 (`modular/`, PR #32, etiqueta `v4.0`). La etiqueta `v4.0` marca esa versión del repositorio, no las piezas del marco v4. **Resuelto:** las piezas de sala entran como fases 21 a 23, antes de este plan. Solo queda pendiente D5: la jornada, el testigo diario y el proyector del histórico.
2. **La fase 20.** Está hecha con POPs en su propia rama y de momento no se fusiona. **Resuelto:** las fases 21 en adelante se apoyan en la 19 y aceptan un proyecto en la 19 o en la 20; lo de POPs se activa con su propio interruptor, no con `Nivel` ≥ 20.
3. **Las fases 11–19 de `main` no usan POPs.** Lo visual va por instancias: Script CHOP → Geometry COMP instanciado, Script SOP para la biblioteca de ejemplares, Script TOP para los mapas y GLSL MAT (`mat_piel_*`) con familias de material. **Resuelto (P1):** las fases de este plan dibujan por instancias, como `main`.
4. **No existe la tabla `ocupacion`.** El estado del mundo vive en el diccionario `W`, en el *storage* del Text DAT `motor` (se guarda con el `.toe`). Las únicas tablas del motor son `ciclos`, `perfiles_erosion`, `colores_drum`, `catalogo`, `escenas`, `midi_log` y las de la rampa.
5. **No existe `PLAN_FASES.md`** en el repositorio (lo citan los documentos de montaje). La hoja *Estratos_parametros* más reciente es una foto de 64 parámetros de un proyecto en `Nivel` 8, y sus columnas no son las que pide el encargo (las filas del apartado 7 usan las del encargo).

---

## 1. Inventario

### 1.1 Versiones de lo que existe

| Script | Versión (primera línea del informe) |
|---|---|
| `estratos_motor.py` | `motor v54` |
| `estratos_comun.py` | `comun v36` |
| `fase12_base.py` | `fase12 v6` (fases 1 y 2) |
| `fase3_semilla.py` | `fase3 v12` |
| `fase4_desborde.py` | `fase4 v7` |
| `fase5_especies.py` | `fase5 v4` |
| `fase6_ciclo.py` | `fase6 v5` |
| `fase7_erosion.py` | `fase7 v14` |
| `fase8_conchas.py` | `fase8 v12` |
| `fase9_arqueologia.py` | `fase9 v11` |
| `fase10_direccion.py` | `fase10 v11` |
| `fase11_piel.py` | `fase11 v8` |
| `fase12_moduladores.py` | `fase12 v7` |
| `fase13_tejido.py` | `fase13 v5` |
| `fase14_destructores.py` | `fase14 v2` |
| `fase15_era.py` | `fase15 v2` |
| `fase16_cortes.py` | `fase16 v2` |
| `fase17_tiempo.py` | `fase17 v1` |
| `fase18_escenas.py` | `fase18 v1` |
| `fase19_modular.py` | `fase19 v2` |
| `ajuste_vista.py` | `ajuste_vista v1` (no es una fase) |
| `modular/` (`cv_osc/cv_osc.ino`, `puente_osc.py`, `esquema.svg`) | Sin versión en el informe (no es una fase). El hardware de la fase 19: Doepfer A-180-9 → ESP32 u Arduino → OSC por USB (SLIP) → `puente_osc.py` → UDP 9000 → `modular_osc`. Prueba: `pruebas/prueba_cv_osc.py`, OK. Los canales 5–8 (`/estratos/cv5`…`cv8`) llegan pero nadie los usa; v5 no los necesita |
| Fase 20 (POPs) | Hecha en su rama, sin fusionar |
| `fase1_tempo_beatstep.py`, `fase2_seq1_baliza.py`, `fix_render_fase2.py` | obsoletos: los sustituye `fase12_base.py` |

### 1.2 Motor y estado por celda

**No hay tabla `ocupacion`** (ver 0.4). Lo que el encargo llama así es el estado `W`, con listas de longitud `N` (85 celdas con el rango do1–do8):

| Clave de `W` | Qué guarda |
|---|---|
| `occ` | Ocupación: triggers de construcción. Es el **escalón** del mundo. |
| `carga` | Notas acumuladas hacia el siguiente trigger (0 a `cost(occ)` − 1). |
| `h`, `vh` | Altura objetivo y visible. `h = height_for(occ)` más la fracción de la carga; desde `Umbralram` la altura no sube (límite) pero `occ` sí. |
| `sp`, `own`, `traza`, `vel`, `par` | Especie visible, fundadora, trazas de híbrido, velocidad fundadora, satélite de. |
| `huella` | Instante de la mancha oscura que deja una semilla borrada (fase 7). **No es la huella mínima de v5**: el nombre está ocupado (ver 4.1). |
| `cols` | **Columna de cada celda**: `[[concha, grosor], ...]` de abajo arriba. El suelo es `núcleo + Σ grosores`. |
| `shells` | Una entrada por concha enterrada: `gen`, `col`, `occ`, `sp`, `rm` (losetas quitadas por celda), `grosor`, `r_in`, `r_out` y, desde la fase 15, el registro (`tema`, `esp`, `estado`, `cluster`, `vias`, `calles`, `rios`). |
| `quitadas` | Losetas que ha perdido cada celda en el mundo actual (tope por mundo de los cortes). |
| `scars` | Cicatrices cian: `concha × 1000 + celda → instante`. |

**Cómo se guardan las conchas por celda.** Al enterrar (`end_cycle`), cada celda apila en su columna una loseta `[s_nueva, g + Colmatacion × laguna]` sobre lo que le queda: una hondonada se tapiza y sigue siendo hondonada. `compactar` aplasta todas las losetas por el mismo factor (`Cortezamax`). Las alturas no se guardan: salen de la posición en la columna.

**Cómo se aplica la erosión sobre los escalones.** `erosion()` → por cada anillo de `rings(objetivo, radio)`, `k = floor(notas × 0,5^d + resto)` notas → `degrade()` → `_undo_note()`: baja la carga; al agotarse, **baja un escalón** (`occ − 1`) y la carga queda llena menos una. Una semilla sin carga se vacía (`_clear_cell`) y deja la `huella` de la fase 7. Los satélites pierden un desborde por nota. Las fracciones quedan en `ero_resto`. Los pads de impulso (bombo y tom) no erosionan: suman pulsos (`occ` sube).

**Cómo se aplican los cortes.** `cut()` (fase 9) y `corte_tematico()` (fase 16) quitan N losetas de la columna en anfiteatro (N − d por anillo), con el tope por mundo de `quitadas`, el núcleo como fondo, y **vacían la celda** (`_clear_cell`: `occ = 0`). Encienden cicatriz cian en el fondo y en las paredes recién expuestas. La concha siguiente tapiza el hueco sin rellenarlo (con `Colmatacion` 0). Solo corta la caja (pad 2, profundidad 3); desde la fase 21, también el ruido acumulado del micrófono.

**Otras bajadas de ocupación**, que también tendrán que borrar inclusiones: los accidentes y catástrofes de la fase 14 (`bajar_estado`, `bajar_ocupacion`, `paso_catastrofe`), los onsets del micrófono (fase 21, pad 9) y el entierro (`end_cycle`), que deja en cada celda solo lo heredado.

**Determinismo.** El proyecto no usa azar de software: el mapa logístico (`logistica`, `semilla_caos`) y `_hash01` deciden todo lo que parece aleatorio. `Probllegada` lo respeta (4.2), y el sorteo de la fase 22 también.

**Estado fuera de `W`.** Lo que no es mundo vive en el módulo, no en el storage: `_COLONAS` (fase 11 v8), `_CACHE`. Es el sitio para el estado del sensor (pistas de personas, temporizadores de casilla).

### 1.3 Cámara cenital — **fase 22**

La fase 22 construye el componente `presencia` de la especificación «casilla probable»: Orbbec TOP (Femto Bolt, profundidad en metros, NFOV binned 320 × 288), `cornerpin1` que endereza el suelo cubierto, captura del suelo vacío (`Capturarfondo`), máscara de cuerpos entre `Alturamin` (0,8 m) y `Alturamax` (2,2 m), rejilla de casillas (`Anchosala` 5,4 m × `Fondosala` 4,5 m en casillas de `Tamcasilla` 0,5 m: 11 × 9), densidad suavizada con `Subida` (2 s) y `Bajada` (5 s), y el mapeo sala → planeta (`Loncentral`, enlazada al giro; `Anchoangular` 180°; `Latnorte` 90°; `Latsur` −90°; `Espejo`). La densidad inclina la probabilidad de cada señal: `P(c) = C + (1 − C) k d(c)`.

Lo que este plan toma de la fase 22:

| Toma | Para qué |
|---|---|
| La profundidad enderezada (`cornerpin1`) y el suelo vacío (`fondo`): altura = suelo − profundidad | Contar personas (fase 24) |
| La rejilla de casillas (columnas × filas) | Ocupación binaria, paradas y filas |
| El mapeo casilla → (latitud, longitud), con `Loncentral` del instante | La celda que mira a la casilla |
| La sala simulada (`sala_sim`, discos de unos 25 cm desde un Table DAT) y `Simcasilla`, `Simponer`, `Simquitar`, `Simvaciar` | Probar sin cámara por el mismo camino |

La densidad suavizada sigue a lo suyo (el sorteo de las señales); v5 no la cambia ni la usa.

### 1.4 Micrófono de sala — **fase 21**

La fase 21 detecta onsets por flujo espectral, erosiona con cada uno como un pad 9 (`Reduccionmic`) y abre un corte con el ruido acumulado (`Ventanaruido`, `Umbralcorte`). El borrado de la fase 26 se engancha en `degrade`, `_undo_note`, `_clear_cell` y `cut`, así que borra con el micrófono sin código propio; solo cuenta la causa `micro` aparte.

### 1.5 Balance erosión/creación y DMX — **fase 23**

La fase 23 crea el balance (`Ventanabalance`), el baño de luz, el estroboscopio, el **limitador común de destellos** (3 por segundo como mucho), la oscuridad de sala al enterrar y el colapso por erosión dominante sostenida (`Colapsoon`, `Maxerosion`). El relámpago (fase 30) pasa por ese limitador. Que la escisión **no cuente en el balance** (2.3 del encargo) se resuelve sin tocar la 23: la escisión no pasa por `erosion()` ni por `pulso()`, que son lo que cuenta el balance.

### 1.6 Enterramiento

| Pieza | Estado |
|---|---|
| Fin de ciclo | **Existe** (fase 6 v5): `close_cycle` con los motivos `cambio de pattern`, `estancado`, `edad maxima` y `forzado`; tabla `ciclos`; `end_cycle` entierra desde el nivel 8. |
| Colapso por erosión dominante | **Fase 23**: motivo `colapso`, apagado por defecto (`Colapsoon`). `estancado` no cuenta como colapso, aunque v4 lo nombre, porque es el cierre normal. La fase 27 lo guarda como marca de la concha. |
| Oscuridad de sala al enterrar | **Fase 23**, con la duración `Noche` (4 s), que la fase 28 usa también para la esfera. |
| Exportación de testigos, jornada y proyector del histórico | **No existe: dependencia D5.** Ningún script guarda imágenes ni ficheros; solo hay un render (`render`, 1280 × 720) y una salida. Hasta D5, la jornada es la fecha del sistema (P13). |

### 1.7 Fases 11–19 y lo que condicionan

Lo que condiciona cómo se dibujarán las inclusiones y las fulguritas:

| Condición | De dónde | Consecuencia para v5 |
|---|---|---|
| Lo visual va por instancias, no por POPs | fases 11–19 | P1: instancias también aquí |
| El shader de la piel (`piel_vertex`, `piel_pixel`) tiene familias (`uFamilia`: mineral, dosel, ciudad, tierra, agua) y lee la rugosidad en el alfa de cada instancia | fase 12, 13 | Las inclusiones son una familia nueva (plástico) y la fulgurita otra (vidrio) |
| El alfa ya codifica más cosas: «alfa = rugosidad + 2 × nivel» (ventanas, fase 17) | fase 17 | La densidad de inclusiones de una loseta enterrada va igual en la parte entera del alfa de `estratos` |
| Las conchas usan el shader de la piel (familia mineral) desde la fase 15, con tapa mate (rugosidad 1) desde la fase 8 v12 | fases 8, 15 | La matriz mate del plastiglomerado ya existe: es la loseta |
| **Colores reservados** del tono OKLCH: 165°–235° cian (cicatriz), 55°–100° ámbar (SEQ2), 120°–165° verdes (pisos), 235°–275° azul (ríos) | fases 8, 11, 13 | La paleta humana sale de lo que queda (275°–360°, 0°–55° y 100°–120°), donde están también los pads de la batería (carmín, magenta, violeta) y el gris cálido del micrófono (fase 21). Ver **P5** |
| La cicatriz cian marca lo recién expuesto | fase 9 | La escisión no enciende cicatriz: «no usa el cian de los cortes» |
| Una celda con el suelo bajo el radio nominal cuenta como corte y enseña fósiles en el fondo y las paredes | fase 16 | La celda de una escisión se excluye |
| Un río que acaba en una hondonada la llena (lago) | fase 13 | La escisión se excluye de los lagos |
| `Colmatacion` rellena las hondonadas al enterrar | fase 8 | Se ignora en la celda de una escisión |
| La luz de las conchas tiñe las losetas de la columna desde arriba | fase 8 | No toca la fulgurita (va en su propia geometría) |
| Naturaleza ligera: la vegetación se recalcula cada `Refresconat` (0,25 s) | fase 11 v8 | Las inclusiones van aparte y no esperan al refresco |
| Rendimiento medido (sesión de 20 min): 4–6 ms de `build_instances` | fase 18 | Presupuesto para v5: menos de 1 ms por fotograma en Python |

---

## 2. Diagrama de dependencias

```
fase 19 ──► 21 MICROFONO ──► 22 CAMARA ──► 23 SALA (DMX, balance, colapso, Noche)
 (main)                          │                 │
                                 ▼                 ▼
                           24 PERSONAS ──► 25 HUELLA ──► 26 BORRADO ──► 27 CLASIFICACION ──► 28 NOCHE
                                 │                          │                 │                 │
                                 └───────────────► 29 FILA Y ESCISION ◄───────┘                 │
                                                      │        │                                │
                                                      ▼        └──────► 31 HISTORICO ◄──────────┘
                                                 30 RELAMPAGO               ▲ (D5: jornada y proyector)
                                                  (limitador de la 23)
```

- **21, 22 y 23** son el requerimiento v4. La 23 deja el limitador de destellos, el colapso y `Noche`.
- **24** necesita 22 (profundidad, rejilla, mapeo y sala simulada).
- **25** necesita 24. **26** necesita 25 (y borra también con el micrófono de la 21).
- **27** necesita 26 (el recuento cuenta las supervivientes) y lee la marca de colapso de la 23.
- **28** necesita 27 (coincide con el recuento) y la oscuridad de sala de la 23; para las paredes que brillan, 29. Se puede aplicar antes que la 29: entonces solo emiten las inclusiones.
- **29** necesita 24 (filas) y 26 (la escisión borra las inclusiones de su celda, como un corte). No necesita 27 ni 28.
- **30** necesita 29 y el limitador de la 23.
- **31** necesita 29 y 27 (bandas de la columna resumen); el disparo al enterrar, 28; la jornada y el proyector, D5.

**Orden:** 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31, después de la 23. El aspecto de la fulgurita va dentro de la 29 (la escisión sin su aspecto no se puede revisar) y las paredes de la noche se activan solas en cuanto existe la 29 (la 28 las busca).

---

## 3. Por fase

Para todas: un script `faseNN_<nombre>.py` que carga `estratos_comun.py`, dice su versión en la primera línea, se niega a correr sin la fase anterior (`require_base`), sube `Nivel`, crea su página `FaseNN` en `/project1/FASE1`, añade su línea a la leyenda, escribe su `LEEME` y termina con la **autoprueba** (`AUTOPRUEBA OK` o qué falla) que deja el mundo como estaba. La lógica va al motor (`motor v58` en adelante, una versión por fase; la 21 a la 23 son de la v55 a la v57) y se activa por `Nivel`, como hasta ahora. Las pruebas fuera de TouchDesigner se añaden a `pruebas/correr_fases.py`. TouchDesigner sigue sin enviar nada al BeatStep.

### Fase 24 · Personas

**Qué hace.** Convierte la cámara de la fase 22 (o su sala simulada) en personas. Cada fotograma de cámara:

1. **Máximos de altura.** Sobre la altura de cada píxel (suelo vacío − profundidad, de `cornerpin1` y `fondo`), reducida a unos 5 cm (Resolution TOP antes de leerla en Python): un píxel es una cabeza si supera `Alturamin` (fase 22), no pasa de `Alturamax` y es el máximo en un disco de radio `Separacioncabezas`. Dos máximos más cerca que `Separacioncabezas` cuentan como una persona (se queda el más alto).
2. **Seguimiento por vecino más cercano.** Se emparejan los máximos con las personas del fotograma anterior, de la pareja más cercana a la más lejana, sin pasar de `Separacioncabezas`. Un máximo sin pareja durante `Confirmapersona` fotogramas seguidos (2) es una **persona nueva** (P2). Una persona sin máximo desaparece.
3. **Ocupación binaria por casilla:** en la rejilla de la fase 22, una casilla está ocupada si tiene al menos una persona. Cada casilla guarda el instante en que se ocupó (`t_ocupada`) y lo pierde al quedar libre.
4. **La celda que mira a la casilla**, en el instante en que se confirma cada evento: el mapeo de la fase 22 da la latitud y la longitud de la casilla con `Loncentral` de ese fotograma (enlazada al giro), y la celda es la de la retícula que las contiene.

La densidad suavizada de la fase 22 no cambia y no se usa para nada de esto: los tiempos de parada y de fila se miden sobre la ocupación binaria.

**Qué añade.**
- Motor: `detectar_cabezas(alturas, cfg)`, `seguir_personas(prev, maximos, cfg)`, `ocupacion_casillas(personas)`, `celda_de_casilla(W, cfg, casilla)`, `tick_personas(W, cfg, now, maximos)`. Estado del sensor en el módulo (`_SALA`: pistas, casillas, contadores), no en `W`.
- Operadores: Resolution TOP `alturas_sala`, Script CHOP `personas_chop` que lo lee, Table DAT `personas` (id, x, y, altura, casilla, desde, nueva) y Table DAT `casillas_ocupadas` (casilla, ocupada, personas, t_ocupada, celda).
- **Simulación:** la sala simulada de la fase 22 (`sala_sim`), con `Simcasilla`, `Simponer`, `Simquitar` y `Simvaciar`. Esta fase añade `Simfila` (n) y `Simformarfila`, que ponen n personas en casillas contiguas desde `Simcasilla`. Las personas simuladas son discos de 1,70 m en la misma imagen que la cámara, así que de ahí en adelante todo es igual: máximos, seguimiento, casillas.

**Parámetros (página Fase24).** `Separacioncabezas` 0,35 m · `Confirmapersona` 2 · `Simfila` 3 · `Simformarfila`.

**Leyenda.**
```
PERSONAS 3 en sala   casillas 3/99   nuevas 12   simulada
```

**Prueba manual.** `Simponer` en una casilla: `PERSONAS 1`, `nuevas` sube 1 y la tabla `casillas_ocupadas` dice qué celda mira. Espera media vuelta del planeta y vuelve a pulsar en otra casilla: la celda es otra. `Simquitar`: `PERSONAS 0`. `Simfila` 4 y `Simformarfila`: 4 personas en casillas contiguas.

**Autoprueba.**
- Dos cabezas a 0,30 m cuentan una; a 0,40 m, dos. Una cabeza bajo `Alturamin` no cuenta.
- Una persona que se mueve 0,10 m por fotograma sigue siendo la misma; una que aparece a 1 m de la más cercana es nueva a los `Confirmapersona` fotogramas, y un máximo de un solo fotograma no lo es.
- La ocupación binaria no depende de ningún slew (una persona que entra se ve en el mismo fotograma).
- La celda de una casilla sigue a `Loncentral`: con el planeta girado, la misma casilla mira a otra celda.
- `Simponer` y `Simformarfila` llegan por la imagen de la sala, no escribiendo en la tabla.
- La línea `PERSONAS` de la leyenda.

### Fase 25 · Huella mínima

**Qué hace.** Las personas dejan **inclusiones** en la celda que mira a su casilla:

- **Llegada:** al detectar una persona nueva, deja una inclusión con probabilidad `Probllegada`. **Sin azar de software:** el sí o el no lo decide el mapa logístico sembrado con el id de la persona, la celda y el ciclo (la misma sala da el mismo resultado), como el resto del motor.
- **Parada:** `Tparada` segundos seguidos con la casilla ocupada (ocupación binaria) dejan una inclusión segura. Una por parada; la casilla se rearma al quedar libre.
- **Escalón:** cada inclusión guarda el escalón (`occ`) de su celda en el instante en que cae.
- **Varias por celda:** una lista por celda, con tope (4.1).
- **Aspecto (plastiglomerado):** la matriz es la loseta de la celda, mineral mate y sin metalicidad; en las celdas con inclusiones su tapa baja de rugosidad 1 a 0,85, dentro de lo que pide v5 (0,8–0,9), sin tocar la regla de la fase 8 en el resto. Las inclusiones son piezas pequeñas, **medio enterradas en el suelo de la celda alrededor de la formación** (P4), de color saturado de la paleta humana (P5; nunca cian ni ámbar), rugosidad 0,1–0,2 y una dispersión subsuperficial leve (familia nueva del shader de la piel, `uFamilia` = plástico: envoltura de luz y un aclarado a contraluz, como la traslucidez de las hojas).

**Qué añade.** Motor: `depositar_inclusion(W, cfg, celda, tipo, now)`, `llegadas(W, cfg, nuevas)`, `paradas(W, cfg, casillas, now)`, `paleta_humana(cfg, k)`, `build_inclusiones(W, cfg, now, out)`. `W['incl']` (4.1). Operadores: Script CHOP `i_inclusiones`, Geometry COMP `inclusiones` (en el render), familia nueva en `piel_pixel`.

**Parámetros (página Fase25).** `Probllegada` 0,6 · `Tparada` 3 s.

**Leyenda.**
```
HUELLA   inclusiones 17 (llegadas 11, paradas 6)   ultima celda 40 escalon 3   llegada 0.6
```

**Prueba manual.** `Probllegada` 1 y `Simponer`: aparece una inclusión en la celda que mira a la casilla. `Probllegada` 0 y `Simponer`: nada; deja la persona 3 s: aparece una (parada). Mantenla más: no aparece otra. `Simquitar` y `Simponer` en la misma casilla: puede salir otra.

**Autoprueba.**
- `Probllegada` 1: toda llegada deja huella; 0: ninguna; 0,6 sobre 1000 llegadas simuladas: entre 0,55 y 0,65, y la misma sala da las mismas.
- La parada a `Tparada` − 1 fotograma no deja nada; a `Tparada`, una; seguir quieto no deja más; tras quedar libre, se rearma.
- La parada se mide en la ocupación binaria: una persona que oscila dentro de la misma casilla sigue parada.
- La inclusión guarda el escalón de su celda; en una celda vacía, 0.
- La celda es la que miraba la casilla al confirmarse, no la que mira después.
- Ninguna inclusión tiene un tono en 55°–100° ni en 165°–235°.
- La línea `HUELLA`.

### Fase 26 · Borrado por erosión

**Qué hace.** Una inclusión desaparece cuando la erosión baja su celda por debajo de su escalón (`occ < escalón`). En una celda sin construir (escalón 0), **cualquier golpe de erosión que la alcance la borra: cualquier anillo con peso mayor que 0, aunque ese golpe no quite una nota entera** (P6). Valen todas las fuentes: la caja y los arañazos (pads 2 y 4–8), el micrófono (fase 21, pad 9, y su corte por ruido), los cortes (vacían la celda), las catástrofes de la fase 14 (bajan la ocupación) y la escisión (es un corte). El bombo y el tom no borran: son impulso y suben la ocupación.

**Cómo** (sin tocar las reglas de la erosión):
- un único punto de purga, `purgar_inclusiones(W, celda, causa)`, que llaman `_undo_note`, `_clear_cell`, `cut`, `bajar_ocupacion` y la escisión cuando la ocupación de una celda baja;
- `erosion()` llama además `golpe_inclusiones(W, celda)` por cada celda de sus anillos, para el caso de la celda vacía;
- una pasada de seguridad por fotograma, solo de las celdas con inclusiones.

**Qué añade.** Motor: las dos funciones y los ganchos; contadores por causa en `W['incl_borradas']`. Ningún operador nuevo: la geometría de la fase 25 deja de dibujarlas.

**Parámetros.** Ninguno nuevo. La página Fase26 lleva solo `Version26`, de solo lectura (P10), para mantener una página por fase.

**Leyenda.**
```
BORRADO  vivas 12   borradas 5 (erosion 2, micro 1, corte 1, catastrofe 1)
```

**Prueba manual.** `Sembrar` cuatro veces en una celda (escalón 4), `Probllegada` 1 y `Simponer` en la casilla que la mira: la inclusión guarda el 4. `Padprueba` 7 y `Erosionar` hasta que la leyenda `ULTIMA` diga ocupación 3: la inclusión desaparece. En una celda vacía: un solo `Erosionar` o un `Simonset` (fase 21) la borra.

**Autoprueba.**
- Escalón 4: bajar la carga sin bajar el escalón no la borra; bajar a 3 sí.
- Celda vacía: un arañazo la borra, también en el segundo anillo; un onset del micrófono la borra; un bombo (impulso) no.
- Un corte con la caja la borra; un incendio (fase 14) que baja la ocupación la borra.
- Dos inclusiones con escalones 2 y 5 en la misma celda: bajar a 4 borra solo la de 5.
- Cada borrado suma en su causa. La línea `BORRADO`.

### Fase 27 · Clasificación al enterrar

**Qué hace.** En `end_cycle`, antes de hornear:

1. Se cuentan las inclusiones supervivientes del mundo que se entierra (las escisiones no cuentan).
2. Con al menos `Minhuellas`, la concha es **estrato humano**; con cero, **concha limpia**, aunque haya habido gente todo el día (todas sus huellas se borraron).
3. **El recuento se hornea en el material:** cada loseta nueva guarda cuántas inclusiones sobrevivieron en su celda y sus colores. El shader de las conchas (familia mineral) las dibuja como motas de la paleta humana en la cara y los flancos de esa loseta, con una cobertura que crece con el número de inclusiones y nunca pasa de `Inclusionesmax` de la loseta. El grosor de la concha no cambia (sigue siendo el de su ciclo, fase 8).
4. **Colapso como marca de cierre:** la concha guarda `cierre` (motivo del ciclo) y `colapso`, que es «sí» cuando la fase 23 cerró el ciclo con el motivo `colapso` (P8). Se combina con humano o limpia.
5. `Umbralpresencia` desaparece: no existe en el repositorio; si existe en el proyecto local, el script lo quita (`remove_par`) y lo dice en el informe.

Las inclusiones del mundo enterrado se vacían; lo heredado (fase 8) empieza sin inclusiones.

**Qué añade.** Motor: `contar_huellas(W)`, `clasificar_concha(W, cfg, ev)` en `end_cycle` y en el registro de la fase 15; campos nuevos en cada entrada de `shells` (4.3); el alfa de `i_estratos` lleva la densidad de inclusiones en su parte entera (como las ventanas de la fase 17); la tabla `ciclos` gana `huellas` y `banda` (`colapso` ya lo añade la 23 con su motivo).

**Parámetros (página Fase27).** `Minhuellas` 1 · `Inclusionesmax` 0,8 (80 %).

**Leyenda.**
```
BANDA    ultima: estrato humano 12 huellas (min 1)   cobertura 15% (max 80%)   colapso no   humanas 3 de 11
```

**Prueba manual.** Deja tres inclusiones y `Forzarciclo`: la concha nueva sale con motas de color en esas tres celdas; un corte con la caja las enseña en la pared. Borra todas antes de `Forzarciclo`: concha limpia. Con `Colapsoon` y `Simbalance` (fase 23) por encima de 1 durante `Maxerosion`: la concha sale con la marca de colapso.

**Autoprueba.**
- 3 supervivientes y `Minhuellas` 1: humana con 3; 0 supervivientes con 40 llegadas borradas: limpia.
- `Minhuellas` 5 con 3: limpia.
- 1000 inclusiones en una celda: la cobertura no pasa de `Inclusionesmax`; el grosor de la concha es el mismo con 0 y con 1000.
- Una escisión abierta no cuenta en el recuento.
- Un cierre por `colapso` marca la concha; uno por `estancado`, no. La marca se combina con humana y con limpia.
- `Umbralpresencia`: ni en la página ni en el motor.
- Un mundo de antes de la fase 27 carga y sus conchas se leen como limpias sin marca.
- La línea `BANDA`.

### Fase 28 · Noche de enterramiento

**Qué hace.** En cada enterramiento, con colapso o sin él, durante `Noche` segundos la esfera apaga lo mineral: solo emiten las inclusiones supervivientes recién horneadas y las paredes de las escisiones (cuando exista la fase 29). Empieza en el mismo fotograma del recuento (fase 27). Mientras tanto, la sala está a oscuras (fase 23, la misma `Noche`; P9). El mundo nuevo sigue funcionando: lo que nace durante la noche se dibuja apagado.

**Cómo** (sin luces nuevas ni geometría nueva): un valor `noche` (0–1) que sale del motor con una entrada y una salida cortas, y llega:
- al shader de la piel y de las conchas como uniforme `uNoche`: lo mineral se multiplica por 1 − `noche`; las inclusiones y la fulgurita suben su emisivo;
- a los dimmers de `luz_principal`, `luz_relleno` y `luz_destello` (lo que dibuja con Phong o constante se apaga con ellos);
- a los materiales constantes aditivos (`luz_celda`, `luz_conchas`, `luz_local`, `particulas`, `reticula`): su color × (1 − `noche`).

Nada se recompila ni sale del render: solo cambian uniformes y expresiones.

**Qué añade.** Motor: `noche_nivel(W, cfg, now)`, `W['noche']` (inicio, fin); uniforme `uNoche` en `piel_pixel`; expresiones en luces y materiales (`noche_al_dia` en comun).

**Parámetros.** Ninguno nuevo: usa `Noche` (4 s), que crea la fase 23. La página Fase28 lleva solo `Version28` (P10).

**Leyenda.**
```
NOCHE    4.0 s   quedan 2.3   emiten 12 inclusiones y 1 escision
```

**Prueba manual.** Con inclusiones vivas, `Forzarciclo`: el planeta se apaga 4 s y solo brillan las motas de la concha nueva. Sin inclusiones: 4 s de oscuridad.

**Autoprueba.**
- `noche` vale 1 desde el fotograma del recuento hasta `Noche` s, y 0 después.
- Durante la noche: dimmers a 0, color de los constantes a 0, `uNoche` 1, y el emisivo de las inclusiones horneadas por encima de 0.
- Con colapso y sin él dura lo mismo, y coincide con la oscuridad de sala de la fase 23.
- Un segundo entierro durante la noche la reinicia.
- `Modoactuacion` no la quita (es parte del mundo).
- La línea `NOCHE`.

### Fase 29 · Fila y escisión colectiva

**Qué hace.**

- **Fila:** `Minfila` personas o más en casillas contiguas (diagonales incluidas), sostenida `Tfila` segundos sobre la ocupación binaria. `Modofila` = `cadena` (cualquier forma contigua, por defecto) o `recta` (todas las casillas en una misma fila, columna o diagonal de la rejilla, seguidas). La fila es una componente conexa de casillas ocupadas; se reconoce de un fotograma al siguiente si comparte alguna casilla con la de antes. Cuenta personas, no casillas. **Puede haber varias filas a la vez en la sala, cada una con su escisión** (P14).
- **Origen:** la casilla de la fila con el `t_ocupada` más antiguo. La escisión se abre en la celda que mira a esa casilla en el instante en que la fila cumple `Tfila`, y esa celda queda fija para esa escisión aunque el planeta gire.
- **Profundidad:** personas × `Conchasporpersona` losetas de la columna de origen, con el núcleo como tope. Si se suman personas mientras la fila aguanta, la misma escisión baja más (la profundidad sigue al máximo de personas visto; si se van, no sube). Esa fila solo abre otra escisión cuando se deshace (menos de `Minfila` personas).
- **Permanencia:** es un hueco. Quita losetas de la columna de origen (como `cut`, con radio 0), vacía la celda y **borra sus inclusiones** (es un corte, P7). No cuenta en el tope por mundo de los cortes (`quitadas`), no enciende cicatriz cian, ignora `Colmatacion` en su celda y la concha siguiente la tapiza sin cerrarla. Las fases 13 (lagos) y 16 (fósiles) la excluyen.
- **Balance:** no pasa por `erosion()` ni por `pulso()`: no es erosión ni creación para la fase 23.
- **Aspecto (fulgurita):** una pieza por concha atravesada, de la superficie al fondo de la escisión, en su propia geometría (`fulguritas`): pared exterior granulada de arena fundida, interior vítreo (rugosidad 0,05–0,1, transmisión alta) y núcleo emisivo de la paleta humana, sin el cian de los cortes. En cada concha que cruza se ramifica un poco: dos o tres ramas finas hacia las paredes vecinas, decididas por el mapa logístico (con la escisión y la concha como semilla). **Las ramas son solo visuales y no quitan material** (P11). Lo que queda bajo el tapiz de una concha posterior no se dibuja, pero se guarda.

**Qué añade.** Motor: `buscar_filas(casillas, cfg)`, `es_recta(casillas)`, `tick_filas(W, cfg, now)`, `abrir_escision`, `profundizar_escision`, `cerrar_escision`, `build_fulguritas(W, cfg, now, out)`; `W['escisiones']` (4.2); exclusiones en `build_rios`/lagos y `build_arqueologia`; `end_cycle` ignora `Colmatacion` en las celdas con escisión. Operadores: Table DAT `escisiones` (4.4), Script CHOP `i_fulguritas`, Geometry COMP `fulguritas`, familia vidrio en `piel_pixel`.

**Parámetros (página Fase29).** `Minfila` 3 · `Tfila` 5 s · `Modofila` cadena · `Conchasporpersona` 1 · `Simsumar` (añade una persona contigua a la fila simulada).

**Leyenda.**
```
FILA     4 personas   cadena   5.0/5.0 s
ESCISION #3   celda 40   conchas 4/12   abierta   (sin abrir: fila 2.1/5.0 s)
```

**Prueba manual.** Con varias conchas: `Simfila` 3 y `Simformarfila` (fase 24). A los 5 s se abre un pozo de 3 conchas con su fulgurita en la celda que miraba la casilla más antigua. `Simsumar`: baja una más. `Simvaciar` y otra fila: otra escisión. `Forzarciclo`: el pozo queda tapizado y sigue abierto.

**Autoprueba.**
- 3 personas en cadena en L durante `Tfila`: escisión; con `Modofila` recta, no; en línea, sí.
- 2 personas: no hay fila. Una fila que se rompe a `Tfila` − 0,1 s: nada.
- El origen es la casilla ocupada desde hace más tiempo, y la celda no cambia al girar el planeta.
- 3 personas y `Conchasporpersona` 1 quitan 3 losetas; 2 más mientras aguanta: 5, la misma escisión; con 4 losetas en la columna, se para en el núcleo.
- La fila se deshace y se forma otra: escisión nueva. Dos filas separadas a la vez: dos escisiones.
- El balance de la fase 23 no cambia; `ero_resto`, `quitadas` y las cicatrices tampoco.
- La concha siguiente la tapiza sin cerrarla, también con `Colmatacion` 1; un río no la llena; la fase 16 no pone fósiles en ella.
- Las inclusiones de la celda de origen se borran (causa `escision`).
- Ninguna pieza de la fulgurita es cian; las ramas no quitan losetas; la línea `FILA` y la `ESCISION`.

### Fase 30 · Relámpago

**Qué hace.** Al abrirse una escisión, un único destello blanco por DMX. Pasa por el limitador común de la fase 23 (como mucho 3 destellos en cualquier ventana de 1 s, junto con el estroboscopio). **Si el limitador está lleno, el relámpago espera al primer hueco y el estroboscopio cede ese destello** (P12). Solo blanco. En pantalla, la fulgurita recién abierta sube su emisivo un instante.

**Qué añade.** Motor: `relampago(W, cfg, now)`, que pide su destello al limitador de la 23 con prioridad; una fila más en `dmx_canales` si el destello va a un foco propio. Sin interfaz DMX, el evento queda en el motor y en la leyenda.

**Parámetros.** Ninguno nuevo. La página Fase30 lleva solo `Version30` (P10).

**Leyenda.**
```
RELAMPAGO hace 3.2 s   destellos 2/3 en el ultimo segundo   dmx artnet
```

**Prueba manual.** Formar una fila: la leyenda dice `RELAMPAGO hace 0.0 s`. Con `Simbalance` 10 (estroboscopio a tope) abrir una escisión: el contador nunca pasa de 3 y el relámpago sale.

**Autoprueba.**
- Una escisión, un destello; profundizarla no da otro.
- Con 3 destellos de estroboscopio en el último segundo, el relámpago espera y nunca hay 4 en una ventana de 1 s; en el hueco siguiente sale el relámpago, no el estroboscopio.
- El destello es blanco (r = g = b).
- La línea `RELAMPAGO`.

### Fase 31 · Escisiones en el histórico

**Qué hace.**

- **Disparo de testigo:** cada escisión exporta una imagen cuando la fila se deshace o cuando se entierra el mundo, lo que ocurra antes, con su profundidad final.
- **Sección por el origen:** un corte del planeta por el plano que pasa por el centro y la celda de origen, desde la superficie hasta la última concha atravesada, unas celdas a cada lado. Se dibuja **en Python a partir de las columnas** (un Script TOP con numpy, como `alturas` y `cultivos`): cada loseta es una banda de su color, las bandas humanas con sus motas, la escisión con su fulgurita. No hace falta un segundo render ni planos de recorte, y se puede probar fuera de TouchDesigner. Se guarda con `TOP.save()` en PNG, en el primer fotograma de la noche o en uno sin cambios del mundo, para no cortar un fotograma.
- **Columna resumen de la jornada:** una columna con una banda por ciclo de la jornada (su tipo: humana, limpia, colapso); cada escisión es una veta que une las bandas que atravesó, con un ancho proporcional a sus personas. Otro Script TOP. Se exporta al cerrar la jornada y la muestra el proyector del histórico (D5).
- **Registro:** cada escisión, con jornada, ciclo, hora, personas, conchas cruzadas y celda de origen (4.4).

**Qué añade.** Motor: `seccion_escision(W, cfg, e, ancho, alto)`, `columna_jornada(W, cfg, jornada)`, `registrar_escision(W, e)`, `exportar_testigo(e)`. Operadores: Script TOP `seccion`, Script TOP `columna_jornada`, Table DAT `escisiones` (de la 29, con las columnas del registro), carpeta `historico/` junto a los scripts. La jornada y el proyector son de D5; hasta entonces, **la jornada es la fecha del sistema al abrir la escisión** (P13).

**Parámetros (página Fase31).** `Exportartestigo` (exporta la sección de la última escisión) · `Carpetahistorico` (por defecto `CARPETA/historico`).

**Leyenda.**
```
HISTORICO escisiones hoy 3   ultima #3 J2 C14 4 personas 4 conchas celda 40   testigo exportado
```

**Prueba manual.** Una fila, `Simvaciar`: aparece `historico/escision_...png` con el pozo en sección. Otra fila y `Forzarciclo` sin deshacerla: se exporta al enterrar, con su profundidad de ese momento.

**Autoprueba.**
- Se exporta una sola vez por escisión, en lo que ocurra antes (fila deshecha o entierro).
- La sección tiene tantas bandas como conchas cruzó la escisión más una de superficie, en el orden de la columna, con los colores de la paleta.
- La columna resumen tiene una banda por ciclo y una veta por escisión, con anchos en la proporción de sus personas.
- El registro tiene sus siete campos, en la tabla y en el fichero; relanzar no duplica filas.
- La línea `HISTORICO`.

---

## 4. Estructuras de datos

### 4.1 Inclusiones por celda

```python
W['incl'] = [[] for _ in range(N)]       # por celda, de la mas antigua a la mas nueva
# cada inclusion:
[escalon, tipo, t, k]
#   escalon  occ de la celda al caer (0 = celda sin construir)
#   tipo     1 llegada, 2 parada
#   t        instante (para la leyenda y el orden)
#   k        semilla del mapa logistico: color de la paleta humana, posicion y tamano
W['incl_borradas'] = dict(erosion=0, micro=0, corte=0, catastrofe=0, escision=0)
```

- Lista corta por celda (un tope, `INCL_CELDA` = 12, como constante del motor; el exceso quita la más antigua de las de escalón más alto). 85 celdas × 12 = 1020 inclusiones como mucho: una fila de instancia cada una.
- En `W` (es mundo: se guarda con el `.toe`). El nombre `huella` ya lo usa la fase 7 para la mancha de la semilla borrada: por eso `incl`.
- El estado del sensor (pistas, `t_ocupada`, temporizadores de parada) va en `_SALA`, en el módulo: no es mundo y no tiene que sobrevivir al `.toe`.

### 4.2 Escisiones

```python
W['escisiones'] = [dict(
    id=3,                 # correlativo de la exposicion
    origen=40,            # celda de origen (fija)
    casilla=17,           # casilla de origen
    personas=4,           # maximo visto mientras la fila aguanta
    profundidad=4,        # losetas pedidas = personas x Conchasporpersona
    cortadas=[11, 10, 9, 8],   # conchas (indices de W['shells']) quitadas de la columna, de arriba abajo
    suelo0=9.25,          # suelo de la celda al abrirse
    estado='abierta',     # abierta -> cerrada (fila deshecha) -> enterrada (su mundo se entierra)
    t0=1234.5, t1=None,   # apertura y cierre
    ciclo=14, jornada='2026-10-27',
    testigo=None,         # ruta de la imagen, al exportarse
    ramas=0.618,          # semilla de las ramas de la fulgurita
)]
```

- Una escisión abierta por fila, y varias filas a la vez (P14).
- `W['shells'][s]['rm'][origen] = 1` en cada concha cortada, como `cut`: las fases 8 y 9 la leen sin cambios.
- Lista acotada (`ESCISIONES_MAX` = 200, como `CICLOS_MAX`): las más viejas se quedan solo en el fichero del registro.

### 4.3 Marca de clasificación en las conchas

Campos nuevos en cada entrada de `W['shells']`:

```python
huellas=12,               # inclusiones supervivientes al enterrar
banda='humana',           # 'humana' o 'limpia'
colapso=False,            # marca de cierre, combinable (motivo 'colapso' de la fase 23)
cierre='estancado',       # motivo del fin de ciclo
incl={40: [k1, k2], 41: [k3]},   # semillas de las inclusiones horneadas, por celda
escisiones=[3],           # ids de las escisiones abiertas en ese mundo (no cuentan en huellas)
```

Una concha sin estos campos (de antes de la fase 27) se lee como `limpia`, sin colapso. Al dibujar, la loseta `[s, g]` de la celda `c` busca `shells[s]['incl'].get(c)` y pone su cobertura en el alfa, con tope `Inclusionesmax`.

### 4.4 Registro del histórico

- **Table DAT `escisiones`** en FASE1, como la tabla `ciclos`: `id`, `jornada`, `ciclo`, `hora`, `personas`, `conchas` (cruzadas), `celda`, `estado`, `testigo`. Últimas 200.
- **Fichero exportable** `historico/escisiones.csv` (UTF-8, separador `;` para abrirlo en una hoja en español, una fila por escisión al cerrarse), y las imágenes `historico/escision_<jornada>_c<ciclo>_<id>.png` y `historico/columna_<jornada>.png`.
- Formato de la hora: `HH:MM:SS` local; jornada: `AAAA-MM-DD` hasta que D5 defina la suya.

---

## 5. Riesgos y rendimiento

| Riesgo | Qué puede pasar | Cómo se acota |
|---|---|---|
| Recuento de personas por fotograma | Leer la altura en Python (`numpyArray`) cuesta una lectura de GPU a CPU de 1–2 ms | Reducir antes en la GPU (Resolution TOP a ~5 cm por píxel: unos 108 × 90 para 5,4 × 4,5 m), máximo local separable en numpy (< 0,5 ms) y solo cuando llega un fotograma nuevo de la cámara (30 fps), no en cada fotograma del render |
| Personas fantasma y parpadeo en las casillas | Un máximo que aparece y desaparece da llegadas falsas; una persona en el borde de dos casillas corta la parada | Seguimiento con radio `Separacioncabezas` y confirmación de `Confirmapersona` fotogramas (P2); histéresis de borde de casilla. Afinar en sala |
| Paralaje | Vista desde arriba, una cabeza a 1,7 m sale desplazada respecto a los pies (lo señala la especificación de la fase 22) | Las casillas de 0,5 m lo absorben; si no, la persona se proyecta al suelo con la nube de puntos |
| Búsqueda de filas | Componentes conexas en cada fotograma | La rejilla es pequeña (99 casillas): componentes y prueba de recta, < 0,1 ms |
| Render de la noche | Cambiar materiales o la lista del render recompila o recuece | Solo uniformes y expresiones (`uNoche`, dimmers, color de los constantes); nada sale del render |
| Legibilidad de la escisión | Un pozo de una celda de ancho apenas se ve desde la cámara de globo | La noche y el emisivo de la fulgurita; el testigo la enseña en sección. Revisar en sala |
| Exportación de secciones | Dibujar y guardar una imagen bloquea un fotograma (10–50 ms) | Una vez por escisión, en el primer fotograma de la noche o en uno sin cambios del mundo |
| Paleta humana frente a la batería | Las inclusiones (saturadas, en 275°–55°) comparten tonos con la luz de los pads 1–3 | Se distinguen por ser materia (brillo y dispersión), no luz; luminosidad distinta de la de los pads (P5) |
| Choques con fases existentes | Lagos que llenan la escisión, fósiles en sus paredes, `Colmatacion` que la cierra, cicatriz cian | Exclusiones explícitas en la fase 29, cada una con su línea en la autoprueba |
| Cuenta de inclusiones en `W` | El storage crece | Topes por celda (12) y de escisiones (200) |
| Fase 20 sin fusionar | Si entra después, su `Nivel` 20 podría encender código en un proyecto que nunca la aplicó | Lo de POPs va con su propio interruptor, no con `Nivel` ≥ 20 (0.2) |

---

## 6. Decisiones tomadas

Las propuestas del plan quedan como decisiones (28 de octubre de 2026).

| | Pregunta | Decisión |
|---|---|---|
| **P1** | ¿POPs o instancias para inclusiones y fulguritas? | Instancias (Script CHOP + Geometry COMP + familia nueva del shader), como `main`. La fase 20 (POPs) sigue sin fusionar |
| **P2** | ¿Cómo se reconoce una persona nueva? | Vecino más cercano con radio `Separacioncabezas`; confirmación tras `Confirmapersona` fotogramas (2) |
| **P3** | `Alturamin` y la rejilla de casillas | Los trae la fase 22, de la especificación «casilla probable»: `Alturamin` 0,8 m, `Alturamax` 2,2 m, casillas de 0,5 m (11 × 9) |
| **P4** | ¿Dónde se ve una inclusión? | En el suelo de la celda, medio enterrada alrededor de la formación |
| **P5** | Paleta humana | Croma alto en OKLCH sobre 275°–360°, 0°–55° y 100°–120°, con luminosidad distinta de la de los pads; sin rojo saturado puro |
| **P6** | En una celda vacía, ¿qué golpe la borra? | Cualquier anillo de la erosión que la alcance (peso > 0), aunque no quite una nota entera |
| **P7** | ¿La escisión borra las inclusiones de su celda de origen? | Sí: es un corte |
| **P8** | Colapso | Lo pone la fase 23 (motivo `colapso`, apagado por defecto); la 27 lo guarda como marca. `estancado` no es colapso |
| **P9** | Luz de sala durante la noche | Oscuridad total, de la fase 23, durante `Noche` |
| **P10** | ¿Fase sin parámetros nuevos? | Página propia con un solo parámetro de solo lectura (`VersionNN`) |
| **P11** | ¿Las ramas de la fulgurita quitan material? | No: solo visuales |
| **P12** | Relámpago con el limitador lleno | Prioridad: espera al primer hueco y el estroboscopio cede ese destello |
| **P13** | ¿Qué es una jornada? | La de D5; hasta entonces, la fecha del sistema al abrir la escisión |
| **P14** | ¿Varias filas a la vez? | Sí, cada fila con su escisión |

Siguen abiertas, como pide el encargo:

- **Forma de la fila:** `Modofila` (cadena por defecto, recta).
- **Inevitabilidad estricta:** `Probllegada` = 1, toda llegada deja huella; con menos, quien cruza sin detenerse puede no dejar ninguna.
- **Valores en sala:** `Umbralonset`, `Umbralcorte` (fase 21), `Tparada`, `Tfila` y `Separacioncabezas` solo se fijan en el espacio real.

Y una dependencia: **D5**, la jornada, el testigo diario y el proyector del histórico de v4.

---

## 7. Filas para la hoja de parámetros

Columnas de la hoja `Estratos_parametros`, tal como las pide el encargo. **Nº** queda por asignar: la hoja de Drive es una foto de 64 parámetros de un proyecto en `Nivel` 8. Los parámetros de la cámara y de la sala simulada (`Alturamin`, `Simcasilla`, `Simponer`, `Simquitar`, `Simvaciar`…) y `Noche` son de las fases 22 y 23: sus filas están en «Tareas técnicas v4».

| Nº | Parámetro | Etiqueta en el panel | Tipo | Defecto | Rango | Qué hace | Clave en el motor | Funciones del motor que lo usan | Operadores de FASE1 que condiciona | Lo crea | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| — | `Separacioncabezas` | Separacion minima entre cabezas (m) | float | 0,35 | 0,15–1,0 | Distancia mínima entre dos máximos de altura para contar dos personas; también el radio del seguimiento | `sep_cabezas` | `detectar_cabezas`, `seguir_personas` | `personas`, `casillas_ocupadas` | fase24 | En sala |
| — | `Confirmapersona` | Fotogramas para confirmar una persona | int | 2 | 1–10 | Fotogramas seguidos antes de dar una persona por nueva | `confirma_persona` | `seguir_personas` | `personas` | fase24 | P2 |
| — | `Simfila` | Personas de la fila de prueba | int | 3 | 1–12 | Cuántas personas pone `Simformarfila` | `sim_fila` | `simular_personas` | `sala_sim` | fase24 | Prueba sin cámara |
| — | `Simformarfila` | Formar una fila | pulse | — | — | Pone `Simfila` personas en casillas contiguas desde `Simcasilla` | — | `simular_personas`, `on_pulse` | `sala_sim`, `personas` | fase24 | Mismo camino que la cámara |
| — | `Probllegada` | Probabilidad de huella al llegar | float | 0,6 | 0–1 | Probabilidad de que una llegada deje inclusión (mapa logístico, sin azar) | `prob_llegada` | `llegadas`, `depositar_inclusion` | `inclusiones` | fase25 | 1 = inevitabilidad estricta |
| — | `Tparada` | Tiempo de parada (s) | float | 3 | 0,5–30 | Segundos seguidos en una casilla para dejar una inclusión segura | `t_parada` | `paradas` | `inclusiones`, `casillas_ocupadas` | fase25 | En sala |
| — | `Version26` | Fase 26 (borrado) | str | fase26 v1 | — | Solo lectura: versión del script | — | — | — | fase26 | P10 |
| — | `Minhuellas` | Huellas minimas para estrato humano | int | 1 | 1–100 | Inclusiones supervivientes para que la banda sea estrato humano | `min_huellas` | `clasificar_concha`, `contar_huellas` | `estratos`, `ciclos` | fase27 | — |
| — | `Inclusionesmax` | Cobertura maxima de inclusiones | float | 0,8 | 0–1 | Cobertura máxima de inclusiones visibles en una loseta de la banda | `inclusiones_max` | `clasificar_concha`, `build_tiles` | `estratos` (alfa) | fase27 | Antes (v4), proporción de la banda |
| — | `Umbralpresencia` | — | — | — | — | Se elimina | — | — | — | fase27 la quita | No existe en el repositorio |
| — | `Version28` | Fase 28 (noche) | str | fase28 v1 | — | Solo lectura: versión del script | — | — | — | fase28 | P10; la noche usa `Noche` (fase 23) |
| — | `Minfila` | Personas minimas de una fila | int | 3 | 2–12 | Personas mínimas en casillas contiguas para formar fila | `min_fila` | `buscar_filas`, `tick_filas` | `escisiones` | fase29 | — |
| — | `Tfila` | Tiempo de la fila (s) | float | 5 | 0,5–60 | Segundos que debe sostenerse la fila para abrir la escisión | `t_fila` | `tick_filas` | `escisiones` | fase29 | En sala |
| — | `Modofila` | Forma de la fila | menu | cadena | cadena / recta | Forma válida de la fila: cualquier forma contigua o en línea | `modo_fila` | `buscar_filas`, `es_recta` | `escisiones` | fase29 | Decisión abierta del encargo |
| — | `Conchasporpersona` | Conchas por persona | int | 1 | 1–12 | Conchas que abre cada persona de la fila | `conchas_persona` | `abrir_escision`, `profundizar_escision` | `estratos`, `fulguritas` | fase29 | Tope: el núcleo |
| — | `Simsumar` | Sumar una persona a la fila | pulse | — | — | Añade una persona contigua a la fila simulada | — | `simular_personas`, `on_pulse` | `sala_sim`, `personas` | fase29 | Prueba sin cámara |
| — | `Version30` | Fase 30 (relampago) | str | fase30 v1 | — | Solo lectura: versión del script | — | — | — | fase30 | P10 |
| — | `Exportartestigo` | Exportar el testigo de la ultima escision | pulse | — | — | Exporta la sección de la última escisión | — | `exportar_testigo`, `on_pulse` | `seccion` | fase31 | — |
| — | `Carpetahistorico` | Carpeta del historico | str | CARPETA/historico | — | Dónde se guardan las imágenes y el registro | `carpeta_historico` | `exportar_testigo`, `registrar_escision` | `seccion`, `columna_jornada`, `escisiones` | fase31 | — |

---

## 8. Fuera de alcance

Como dice el encargo: las variantes de v4 (proyector en plano y controlador de sesgo), la clasificación del mundo por timbres, la entrada de voltajes por ethernet y cualquier cambio en la propuesta artística o en el marco conceptual. La fase 20 (POPs) y D5 (jornada, testigo diario y proyector del histórico) tampoco entran aquí.

---

## 9. Para empezar

1. Fases 21, 22 y 23 (requerimiento v4), revisadas una a una.
2. Fase 24, encima de la 23.
3. Cerrar en sala los valores que solo se fijan allí (apartado 6).
