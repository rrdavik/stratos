# Estratos · Plan v5: la huella inevitable

*Plan de fases para llevar el Marco conceptual v5 («La huella inevitable») al proyecto de TouchDesigner. Encargo «conceptualizar v5 stratos», 26 de octubre de 2026. **No implementa nada.** Cada fase se revisa y se aprueba antes de pasar a código.*

Fuentes leídas para este plan:

- el repositorio `rrdavik/stratos` (rama `main` al 27 de octubre de 2026, commit `8fe3543`, etiqueta `v4.0`: el merge del PR #32, el conversor CV → OSC de `modular/`; revisadas también todas las ramas y PR abiertos), que es el contenido de `C:/Users/DareDave/Downloads/est`: `estratos_motor.py`, `estratos_comun.py`, los scripts de fase, `MONTAJE_FASE1.md`, `MONTAJE_FASES_3_10.md`, `MONTAJE_FASES_11_18.md` y `pruebas/`;
- el documento *Estratos — Marco conceptual v4: El estrato humano* (Drive, 14 de octubre de 2026);
- las dos hojas *Estratos_parametros* de Drive (24 y 25 de octubre de 2026).

---

## 0. Lo que hay que saber antes de leer

El inventario (apartado 1) encuentra **cinco desajustes** entre lo que el encargo da por existente y lo que hay en el repositorio. No los resuelvo aquí: los señalo, y el plan se apoya en ellos como dependencias.

1. **Nada de la sala de v4 está en el repositorio.** No hay cámara cenital (Femto Bolt, Orbbec TOP), casilla probable, densidad suavizada, micrófono de sala, balance erosión/creación, DMX, colapso, testigos ni proyector del histórico, ni en `main` ni en ninguna rama o PR abierto. El repositorio llega a la **fase 19** (`motor v54`, `comun v36`), más el conversor CV → OSC de la fase 19 (`modular/`, PR #32, etiqueta `v4.0`). La etiqueta `v4.0` marca esa versión del repositorio, no las piezas del marco v4. Si esas piezas existen en la carpeta local y no se han subido, hay que subirlas antes de la fase 21; si no existen, son dependencias por construir (D1 a D5, apartado 1.7).
2. **No hay fase 20.** El encargo habla de «fases 11–20» y prevé numerar desde la 21. En el repositorio la siguiente libre es la **20**. Numero desde la **21**, como pide el encargo, y dejo la 20 reservada para lo que haya en local (o para la primera dependencia de v4, si se decide construirla).
3. **Las fases 11–19 no usan POPs.** Lo visual va por instancias: Script CHOP → Geometry COMP instanciado, Script SOP para la biblioteca de ejemplares, Script TOP para los mapas y GLSL MAT (`mat_piel_*`) con familias de material. El propio motor lo dice: `RUTA_HOJAS = 'SOP'  # las hojas van en la malla de cada ejemplar (Script SOP), no en POPs`, y `MONTAJE_FASES_11_18.md` lo justifica: «los nombres de los parámetros de POPs no se pueden comprobar aquí». La convención del encargo («POPs para lo visual, como en las fases 11 en adelante») no se cumple hoy. Ver la decisión pendiente **P1**.
4. **No existe la tabla `ocupacion`.** El estado del mundo vive en el diccionario `W`, en el *storage* del Text DAT `motor` (se guarda con el `.toe`). No hay ningún Table DAT llamado `ocupacion`. Las únicas tablas del motor son `ciclos`, `perfiles_erosion`, `colores_drum`, `catalogo`, `escenas`, `midi_log` y las de la rampa.
5. **No existe `PLAN_FASES.md`** en el repositorio (lo citan los documentos de montaje). El diagrama del apartado 2 sigue el estilo de los diagramas de `MONTAJE_FASES_3_10.md`. La hoja *Estratos_parametros* más reciente es una foto de 64 parámetros de un proyecto en `Nivel` 8, y sus columnas no son las que pide el encargo (las filas del apartado 7 usan las del encargo).

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
| `modular/` (`cv_osc/cv_osc.ino`, `puente_osc.py`, `esquema.svg`) | Sin versión en el informe (no es una fase). El hardware de la fase 19: Doepfer A-180-9 → ESP32 u Arduino → OSC por USB (SLIP) → `puente_osc.py` → UDP 9000 → `modular_osc`. Cierra la decisión abierta de la fase 19 (cómo llegan los voltajes). Prueba: `pruebas/prueba_cv_osc.py`, OK. Los canales 5–8 (`/estratos/cv5`…`cv8`) llegan pero nadie los usa. v5 no los necesita |
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

**Cómo se aplican los cortes.** `cut()` (fase 9) y `corte_tematico()` (fase 16) quitan N losetas de la columna en anfiteatro (N − d por anillo), con el tope por mundo de `quitadas`, el núcleo como fondo, y **vacían la celda** (`_clear_cell`: `occ = 0`). Encienden cicatriz cian en el fondo y en las paredes recién expuestas. La concha siguiente tapiza el hueco sin rellenarlo (con `Colmatacion` 0). Solo corta la caja (pad 2, profundidad 3).

**Otras bajadas de ocupación**, que también tendrán que borrar inclusiones: los accidentes y catástrofes de la fase 14 (`bajar_estado`, `bajar_ocupacion`, `paso_catastrofe`) y el entierro (`end_cycle`), que deja en cada celda solo lo heredado.

**Determinismo.** El proyecto no usa azar de software: el mapa logístico (`logistica`, `semilla_caos`) y `_hash01` deciden todo lo que parece aleatorio. `Probllegada` tiene que respetarlo (4.2).

**Estado fuera de `W`.** Lo que no es mundo vive en el módulo, no en el storage: `_COLONAS` (fase 11 v8), `_CACHE`. Es el sitio para el estado del sensor (pistas de personas, temporizadores de casilla).

### 1.3 Cámara cenital (Femto Bolt, Orbbec TOP) — **no existe: dependencia D1**

No hay en el repositorio ningún Orbbec TOP, casilla probable, mapeo casilla → celda ni densidad suavizada con `Subida` y `Bajada`. `Alturamin`, que el encargo cita como existente, tampoco. Lo único parecido es la cámara de render (`camara`), que no tiene que ver.

Lo que el plan **necesita** de D1 (el contrato, no la implementación):

| Necesita | Para qué |
|---|---|
| Un mapa de alturas del suelo en metros (TOP), con `Alturacamara` o equivalente | Contar personas (fase 21) |
| La rejilla de casillas: número, tamaño en metros y su posición en el mapa | Ocupación binaria, paradas y filas |
| `casilla_dir(casilla)`: la dirección del mundo a la que mira cada casilla | La celda que mira a la casilla (con el giro de ese instante) |
| La densidad suavizada por casilla (0–1) | Sigue como está: inclinar la probabilidad de las señales. v5 no la cambia |

Mientras D1 no exista, la fase 21 funciona solo con la simulación (convención del apartado 4 del encargo) y deja el enchufe de la cámara listo.

### 1.4 Micrófono de sala — **no existe: dependencia D2**

No hay detección de onsets, `Umbralonset`, `Reduccionmic`, `Ventanaruido` ni `Umbralcorte`. El plan no depende de él para funcionar: el borrado de la fase 23 se engancha en `degrade`, `_undo_note`, `_clear_cell` y `cut`, así que **cualquier fuente de erosión futura** (el micrófono como novena pista, sus cortes por ruido acumulado) borrará inclusiones sin tocar la fase 23.

### 1.5 Balance erosión/creación y DMX — **no existe: dependencia D3**

No hay ventana de balance, baño de luz, estroboscopio, `Umbralestrobo`, `Maxhz`, DMX Out CHOP ni limitador de destellos. La fase 27 (relámpago) depende de D3; sin DMX, el relámpago queda registrado en el motor y en la leyenda (`sin DMX`) y se prueba igual. Que la escisión **no cuente en el balance** (2.3 del encargo) se resuelve sin D3: la escisión no pasa por `erosion()` ni por `pulso()`, que son lo que contaría el balance.

### 1.6 Enterramiento

| Pieza | Estado |
|---|---|
| Fin de ciclo | **Existe** (fase 6 v5): `close_cycle` con los motivos `cambio de pattern`, `estancado`, `edad maxima` y `forzado`; tabla `ciclos`; `end_cycle` entierra desde el nivel 8. |
| Colapso por erosión dominante | **No existe: D4.** Ningún motivo se llama colapso y ninguna concha guarda esa marca. Según v4, «colapso» es un ciclo cerrado antes de su duración máxima «por saturación, estancamiento o erosión dominante sostenida»: con esa definición casi todas las conchas actuales (cierre por `estancado`) serían colapso. Ver **P8**. |
| Exportación de testigos | **No existe: D5.** Ningún script guarda imágenes ni ficheros. No hay concepto de **jornada**. |
| Proyector del histórico | **No existe: D5.** Solo hay un render (`render`, 1280 × 720) y una salida. |

### 1.7 Fases 11–19 y lo que condicionan

Lo que condiciona cómo se dibujarán las inclusiones y las fulguritas:

| Condición | De dónde | Consecuencia para v5 |
|---|---|---|
| Lo visual va por instancias, no por POPs | fases 11–19 | P1: o se sigue igual, o se estrena POPs en la fase 22 |
| El shader de la piel (`piel_vertex`, `piel_pixel`) tiene familias (`uFamilia`: mineral, dosel, ciudad, tierra, agua) y lee la rugosidad en el alfa de cada instancia | fase 12, 13 | Las inclusiones serían una familia nueva (plástico) y la fulgurita otra (vidrio) |
| El alfa ya codifica más cosas: «alfa = rugosidad + 2 × nivel» (ventanas, fase 17) | fase 17 | La densidad de inclusiones de una loseta enterrada puede ir igual en la parte entera del alfa de `estratos` |
| Las conchas usan el shader de la piel (familia mineral) desde la fase 15, con tapa mate (rugosidad 1) desde la fase 8 v12 | fases 8, 15 | La matriz mate del plastiglomerado ya existe: es la loseta |
| **Colores reservados** del tono OKLCH: 165°–235° cian (cicatriz), 55°–100° ámbar (SEQ2), 120°–165° verdes (pisos), 235°–275° azul (ríos) | fases 8, 11, 13 | La paleta humana tiene que salir de lo que queda (275°–360° y 0°–55°, más 100°–120°), y ahí están también los pads de la batería (carmín, magenta, violeta). Ver **P5** |
| La cicatriz cian marca lo recién expuesto | fase 9 | La escisión no puede encender cicatriz: «no usa el cian de los cortes» |
| Una celda con el suelo bajo el radio nominal cuenta como corte y enseña fósiles en el fondo y las paredes | fase 16 | La celda de una escisión enseñaría troncos fósiles en vez de fulgurita: hay que excluirla |
| Un río que acaba en una hondonada la llena (lago) | fase 13 | La escisión se llenaría de agua: hay que excluirla de los lagos |
| `Colmatacion` rellena las hondonadas al enterrar | fase 8 | Con `Colmatacion` > 0 la escisión se cerraría poco a poco: hay que ignorarla en su celda |
| La luz de las conchas tiñe las losetas de la columna desde arriba | fase 8 | No toca la fulgurita (va en su propia geometría) |
| Naturaleza ligera: la vegetación se recalcula cada `Refresconat` (0,25 s) | fase 11 v8 | Las inclusiones van aparte y no esperan al refresco |
| Rendimiento medido (sesión de 20 min): 4–6 ms de `build_instances` | fase 18 | Presupuesto para v5: menos de 1 ms por fotograma en Python |

---

## 2. Diagrama de dependencias

```
                    ┌─────────────── dependencias de v4 (no están en el repositorio) ───────────────┐
                    │  D1 cámara cenital   D2 micrófono   D3 balance + DMX   D4 colapso   D5 testigo, │
                    │  (Orbbec, casillas,  (onsets,       (baño, estrobo,    (erosión     jornada y  │
                    │   casilla -> celda)   cortes)        limitador 3 Hz)    dominante)   proyector  │
                    └──────┬──────────────────┬────────────────┬────────────────┬────────────┬──────┘
                           │ (o simulación)   │ (opcional)     │                │ (marca)    │
fase 19 (motor v54) ──► 21 PERSONAS ──► 22 HUELLA MINIMA ──► 23 BORRADO ──► 24 CLASIFICACION ──► 25 NOCHE
                           │                                   ▲  │              ▲                 │
                           │                                   │  └──────┐       │                 │
                           └──────────────────────► 26 FILA Y ESCISION ──┴──► 27 RELAMPAGO       │
                                                         │                       ▲ (D3)            │
                                                         └──────────────► 28 HISTORICO ◄──────────┘
                                                                              ▲ (D5)
```

- **21** necesita D1 para la cámara real; sin ella funciona con la simulación.
- **22** necesita 21. **23** necesita 22 (y se beneficia de D2 sin depender de él).
- **24** necesita 23 (el recuento cuenta las supervivientes) y deja el campo de colapso (D4) preparado.
- **25** necesita 24 (coincide con el recuento) y, para las paredes que brillan, 26. Se puede aplicar antes que la 26: entonces solo emiten las inclusiones.
- **26** necesita 21 (filas) y 23 (la escisión borra las inclusiones de su celda, como un corte). No necesita 24 ni 25.
- **27** necesita 26 y D3.
- **28** necesita 26 y 24 (bandas de la columna resumen); el disparo al enterrar, 25; la jornada y el proyector, D5.

**Orden propuesto:** 21 → 22 → 23 → 24 → 25 → 26 → 27 → 28, el del encargo. Lo único que cambio es dónde se resuelven dos cosas: el aspecto de la fulgurita va dentro de la 26 (la escisión sin su aspecto no se puede revisar) y las paredes de la noche se activan solas en cuanto existe la 26 (la 25 las busca).

---

## 3. Por fase

Para todas: un script `faseNN_<nombre>.py` que carga `estratos_comun.py`, dice su versión en la primera línea, se niega a correr sin la fase anterior (`require_base`), sube `Nivel`, crea su página `FaseNN` en `/project1/FASE1`, añade su línea a la leyenda, escribe su `LEEME` y termina con la **autoprueba** (`AUTOPRUEBA OK` o qué falla) que deja el mundo como estaba. La lógica va al motor (`motor v55` en adelante, una versión por fase) y se activa por `Nivel`, como hasta ahora. Las pruebas fuera de TouchDesigner se añaden a `pruebas/correr_fases.py`. TouchDesigner sigue sin enviar nada al BeatStep.

### Fase 21 · Personas

**Qué hace.** Convierte la cámara (o la simulación) en personas. Cada fotograma de cámara:

1. **Máximos de altura.** Sobre el mapa de alturas, reducido a una rejilla de unos 5 cm (Resolution TOP antes de leerlo en Python): un píxel es una cabeza si supera `Alturamin` y es el máximo en un disco de radio `Separacioncabezas`. Dos máximos más cerca que `Separacioncabezas` cuentan como una persona (se queda el más alto).
2. **Seguimiento por vecino más cercano.** Se emparejan los máximos con las personas del fotograma anterior, de la pareja más cercana a la más lejana, sin pasar de `Separacioncabezas` (decisión **P2**). Un máximo que se queda sin pareja es una **persona nueva**. Una persona sin máximo desaparece.
3. **Ocupación binaria por casilla:** una casilla está ocupada si tiene al menos una persona. Cada casilla guarda el instante en que se ocupó (`t_ocupada`) y lo pierde al quedar libre.
4. **La celda que mira a la casilla**, en el instante en que se confirma cada evento: `celda = argmax_c ( world_dir(normal(c), giro, Tilt, balanceo) · casilla_dir(casilla) )`, con el giro, la inclinación y el balanceo de ese fotograma (los mismos de `world_dir`, que ya usan la luz y la retícula).

La densidad suavizada de D1 no cambia y no se usa para nada de esto: los tiempos de parada y de fila se miden sobre la ocupación binaria.

**Qué añade.**
- Motor: `detectar_cabezas(alturas, cfg)`, `seguir_personas(prev, maximos, cfg)`, `ocupacion_casillas(personas)`, `celda_de_casilla(W, cfg, casilla)`, `tick_personas(W, cfg, now, maximos)` y `simular_personas()`. Estado del sensor en el módulo (`_SALA`: pistas, casillas, contadores), no en `W`.
- Operadores: Table DAT `personas` (id, x, y, altura, casilla, desde, nueva) y Table DAT `casillas` (casilla, ocupada, personas, t_ocupada, celda); si existe D1, un Script CHOP o Script TOP `sala` que lee el mapa de alturas.
- **Simulación** (convención del encargo): `Simcasilla` elige una casilla; `Simponer` y `Simquitar` ponen o quitan una persona en ella; `Simfila` (n) y `Simformarfila` ponen n personas en casillas contiguas desde `Simcasilla`; `Simvaciar` vacía la sala. **Entran por el mismo camino que la cámara:** la simulación dibuja cabezas (discos de 1,70 m) en un mapa de alturas sintético, y de ahí en adelante todo es igual: máximos, seguimiento, casillas. Es lo mismo que hacen las autopruebas con los bytes MIDI.

**Parámetros (página Fase21).** `Separacioncabezas` 0,35 m · `Fuentepersonas` (camara / simulada / ambas; *propuesto*) · `Simcasilla` · `Simponer` · `Simquitar` · `Simfila` 3 · `Simformarfila` · `Simvaciar`. `Alturamin` y la rejilla de casillas son de D1; si D1 no los trae, se crean aquí y se marcan en la hoja (**P3**).

**Leyenda.**
```
PERSONAS 3 en sala   casillas 3/64   nuevas 12   simulada
```

**Prueba manual.** `Simponer` en una casilla: `PERSONAS 1`, `nuevas` sube 1 y la tabla `casillas` dice qué celda mira. Espera media vuelta del planeta y vuelve a pulsar en otra casilla: la celda es otra. `Simquitar`: `PERSONAS 0`. `Simfila` 4 y `Simformarfila`: 4 personas en casillas contiguas.

**Autoprueba.**
- Dos cabezas a 0,30 m cuentan una; a 0,40 m, dos. Una cabeza bajo `Alturamin` no cuenta.
- Una persona que se mueve 0,10 m por fotograma sigue siendo la misma; una que aparece a 1 m de la más cercana es nueva.
- La ocupación binaria no depende de ningún slew (una persona que entra se ve en el mismo fotograma).
- La celda de una casilla cambia con el giro: con el planeta girado 180°, la casilla mira a la celda antípoda de la de antes.
- `Simponer` y `Simquitar` llegan por el mapa de alturas, no escribiendo en la tabla.
- La línea `PERSONAS` de la leyenda.

### Fase 22 · Huella mínima

**Qué hace.** Las personas dejan **inclusiones** en la celda que mira a su casilla:

- **Llegada:** al detectar una persona nueva, deja una inclusión con probabilidad `Probllegada`. **Sin azar de software:** el sí o el no lo decide el mapa logístico sembrado con el id de la persona, la celda y el ciclo (la misma sala da el mismo resultado), como el resto del motor.
- **Parada:** `Tparada` segundos seguidos con la casilla ocupada (ocupación binaria) dejan una inclusión segura. Una por parada; la casilla se rearma al quedar libre.
- **Escalón:** cada inclusión guarda el escalón (`occ`) de su celda en el instante en que cae.
- **Varias por celda:** una lista por celda, con tope (4.1).
- **Aspecto (plastiglomerado):** la matriz es la loseta de la celda, que ya es mineral mate y sin metalicidad (tapa con rugosidad 1, fase 8 v12). v5 pide 0,8–0,9: *propuesta*, bajar la tapa a 0,85 solo en las celdas con inclusiones, para no tocar la regla de la fase 8 en el resto. Las inclusiones son piezas pequeñas, medio enterradas en el suelo de la celda alrededor de la formación, de color saturado de la paleta humana (nunca cian ni ámbar), rugosidad 0,1–0,2 y una dispersión subsuperficial leve (familia nueva del shader de la piel: `uFamilia` = plástico: envoltura de luz y un aclarado a contraluz, como la traslucidez de las hojas). Dónde van exactamente (suelo o flanco de la formación, a la altura de su escalón) es la decisión **P4**.

**Qué añade.** Motor: `depositar_inclusion(W, cfg, celda, tipo, now)`, `llegadas(W, cfg, nuevas)`, `paradas(W, cfg, casillas, now)`, `paleta_humana(cfg, k)`, `build_inclusiones(W, cfg, now, out)`. `W['incl']` (4.1). Operadores: Script CHOP `i_inclusiones`, Geometry COMP `inclusiones` (en el render), familia nueva en `piel_pixel`. Si se elige POPs (P1), un POP network `inclusiones_pop` en vez de la geometría instanciada.

**Parámetros (página Fase22).** `Probllegada` 0,6 · `Tparada` 3 s.

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

### Fase 23 · Borrado por erosión

**Qué hace.** Una inclusión desaparece cuando la erosión baja su celda por debajo de su escalón (`occ < escalón`). En una celda sin construir (escalón 0), cualquier golpe de erosión que la alcance la borra. Valen todas las fuentes: la caja y los arañazos (pads 2 y 4–8), el micrófono cuando exista (D2), los cortes (vacían la celda), las catástrofes de la fase 14 (bajan la ocupación) y la escisión (es un corte). El bombo y el tom no borran: son impulso y suben la ocupación.

**Cómo** (sin tocar las reglas de la erosión):
- un único punto de purga, `purgar_inclusiones(W, celda, causa)`, que llaman `_undo_note`, `_clear_cell`, `cut`, `bajar_ocupacion` y la escisión cuando la ocupación de una celda baja;
- `erosion()` llama además `golpe_inclusiones(W, celda)` por cada celda de sus anillos, para el caso de la celda vacía (qué cuenta como «golpe» en un anillo lejano: **P6**);
- una pasada de seguridad por fotograma, solo de las celdas con inclusiones.

**Qué añade.** Motor: las dos funciones y los ganchos; contadores por causa en `W['incl_borradas']`. Ningún operador nuevo: la geometría de la fase 22 deja de dibujarlas.

**Parámetros.** Ninguno nuevo. La fase 23 no tiene página (o una vacía, solo con la versión, si la convención lo exige: **P10**).

**Leyenda.**
```
BORRADO  vivas 12   borradas 5 (erosion 3, corte 1, catastrofe 1)
```

**Prueba manual.** `Sembrar` cuatro veces en una celda (escalón 4), `Probllegada` 1 y `Simponer` en la casilla que la mira: la inclusión guarda el 4. `Padprueba` 7 y `Erosionar` hasta que la leyenda `ULTIMA` diga ocupación 3: la inclusión desaparece. En una celda vacía: un solo `Erosionar` la borra.

**Autoprueba.**
- Escalón 4: bajar la carga sin bajar el escalón no la borra; bajar a 3 sí.
- Celda vacía: un arañazo la borra; un bombo (impulso) no.
- Un corte con la caja la borra; un incendio (fase 14) que baja la ocupación la borra.
- Dos inclusiones con escalones 2 y 5 en la misma celda: bajar a 4 borra solo la de 5.
- Cada borrado suma en su causa. La línea `BORRADO`.

### Fase 24 · Clasificación al enterrar

**Qué hace.** En `end_cycle`, antes de hornear:

1. Se cuentan las inclusiones supervivientes del mundo que se entierra (las escisiones no cuentan).
2. Con al menos `Minhuellas`, la concha es **estrato humano**; con cero, **concha limpia**, aunque haya habido gente todo el día (todas sus huellas se borraron).
3. **El recuento se hornea en el material:** cada loseta nueva guarda cuántas inclusiones sobrevivieron en su celda y sus colores. El shader de las conchas (familia mineral) las dibuja como motas de la paleta humana en la cara y los flancos de esa loseta, con una cobertura que crece con el número de inclusiones y nunca pasa de `Inclusionesmax` de la loseta. El grosor de la concha no cambia (sigue siendo el de su ciclo, fase 8).
4. **Colapso como marca de cierre:** la concha guarda `cierre` (motivo del ciclo) y `colapso` (sí/no), combinable con humano o limpia. Mientras no exista D4, `colapso` es siempre «no» (**P8**).
5. `Umbralpresencia` desaparece: no existe en el repositorio; si existe en el proyecto local, el script lo quita (`remove_par`) y lo dice en el informe.

Las inclusiones del mundo enterrado se vacían; lo heredado (fase 8) empieza sin inclusiones.

**Qué añade.** Motor: `contar_huellas(W)`, `clasificar_concha(W, cfg, ev)` en `end_cycle` y en el registro de la fase 15; campos nuevos en cada entrada de `shells` (4.3); el alfa de `i_estratos` lleva la densidad de inclusiones en su parte entera (como las ventanas de la fase 17); la tabla `ciclos` gana `huellas`, `banda` y `colapso`.

**Parámetros (página Fase24).** `Minhuellas` 1 · `Inclusionesmax` 0,8 (80 %).

**Leyenda.**
```
BANDA    ultima: estrato humano 12 huellas (min 1)   cobertura 15% (max 80%)   colapso no   humanas 3 de 11
```

**Prueba manual.** Deja tres inclusiones y `Forzarciclo`: la concha nueva sale con motas de color en esas tres celdas; un corte con la caja las enseña en la pared. Borra todas antes de `Forzarciclo`: concha limpia.

**Autoprueba.**
- 3 supervivientes y `Minhuellas` 1: humana con 3; 0 supervivientes con 40 llegadas borradas: limpia.
- `Minhuellas` 5 con 3: limpia.
- 1000 inclusiones en una celda: la cobertura no pasa de `Inclusionesmax`; el grosor de la concha es el mismo con 0 y con 1000.
- Una escisión abierta no cuenta en el recuento.
- La marca de colapso se guarda aparte del tipo y se combina con los dos.
- `Umbralpresencia`: ni en la página ni en el motor.
- Un mundo de antes de la fase 24 carga y sus conchas se leen como limpias sin marca.
- La línea `BANDA`.

### Fase 25 · Noche de enterramiento

**Qué hace.** En cada enterramiento, con colapso o sin él, durante `Noche` segundos la esfera apaga lo mineral: solo emiten las inclusiones supervivientes recién horneadas y las paredes de las escisiones (cuando exista la fase 26). Empieza en el mismo fotograma del recuento (fase 24). El mundo nuevo sigue funcionando: lo que nace durante la noche se dibuja apagado.

**Cómo** (sin luces nuevas ni geometría nueva): un valor `noche` (0–1) que sale del motor con una entrada y una salida cortas, y llega:
- al shader de la piel y de las conchas como uniforme `uNoche`: lo mineral se multiplica por 1 − `noche`; las inclusiones y la fulgurita suben su emisivo;
- a los dimmers de `luz_principal`, `luz_relleno` y `luz_destello` (lo que dibuja con Phong o constante se apaga con ellos);
- a los materiales constantes aditivos (`luz_celda`, `luz_conchas`, `luz_local`, `particulas`, `reticula`): su color × (1 − `noche`).

Nada se recompila ni sale del render: solo cambian uniformes y expresiones. Qué hace la luz de sala durante la noche (D3) es **P9**.

**Qué añade.** Motor: `noche_nivel(W, cfg, now)`, `W['noche']` (inicio, fin); uniforme `uNoche` en `piel_pixel`; expresiones en luces y materiales (`noche_al_dia` en comun).

**Parámetros (página Fase25).** `Noche` 4 s.

**Leyenda.**
```
NOCHE    4.0 s   quedan 2.3   emiten 12 inclusiones y 1 escision
```

**Prueba manual.** Con inclusiones vivas, `Forzarciclo`: el planeta se apaga 4 s y solo brillan las motas de la concha nueva. Sin inclusiones: 4 s de oscuridad.

**Autoprueba.**
- `noche` vale 1 desde el fotograma del recuento hasta `Noche` s, y 0 después.
- Durante la noche: dimmers a 0, color de los constantes a 0, `uNoche` 1, y el emisivo de las inclusiones horneadas por encima de 0.
- Con colapso y sin él dura lo mismo.
- Un segundo entierro durante la noche la reinicia.
- `Modoactuacion` no la quita (es parte del mundo).
- La línea `NOCHE`.

### Fase 26 · Fila y escisión colectiva

**Qué hace.**

- **Fila:** `Minfila` personas o más en casillas contiguas (diagonales incluidas), sostenida `Tfila` segundos sobre la ocupación binaria. `Modofila` = `cadena` (cualquier forma contigua, por defecto) o `recta` (todas las casillas en una misma fila, columna o diagonal de la rejilla, seguidas). La fila es una componente conexa de casillas ocupadas; se reconoce de un fotograma al siguiente si comparte alguna casilla con la de antes. Cuenta personas, no casillas.
- **Origen:** la casilla de la fila con el `t_ocupada` más antiguo. La escisión se abre en la celda que mira a esa casilla en el instante en que la fila cumple `Tfila`, y esa celda queda fija para esa escisión aunque el planeta gire.
- **Profundidad:** personas × `Conchasporpersona` losetas de la columna de origen, con el núcleo como tope. Si se suman personas mientras la fila aguanta, la misma escisión baja más (la profundidad sigue al máximo de personas visto; si se van, no sube). Solo se abre otra cuando la fila se deshace (menos de `Minfila` personas).
- **Permanencia:** es un hueco. Quita losetas de la columna de origen (como `cut`, con radio 0), vacía la celda y borra sus inclusiones (es un corte, P7). No cuenta en el tope por mundo de los cortes (`quitadas`), no enciende cicatriz cian, ignora `Colmatacion` en su celda y la concha siguiente la tapiza sin cerrarla. Las fases 13 (lagos) y 16 (fósiles) la excluyen.
- **Balance:** no pasa por `erosion()` ni por `pulso()`: no es erosión ni creación.
- **Aspecto (fulgurita):** una pieza por concha atravesada, de la superficie al fondo de la escisión, en su propia geometría (`fulguritas`): pared exterior granulada de arena fundida, interior vítreo (rugosidad 0,05–0,1, transmisión alta) y núcleo emisivo de la paleta humana, sin el cian de los cortes. En cada concha que cruza se ramifica un poco: dos o tres ramas finas hacia las paredes vecinas, decididas por el mapa logístico (con la escisión y la concha como semilla). Las ramas son solo visuales (**P11**). Lo que queda bajo el tapiz de una concha posterior no se dibuja, pero se guarda.

**Qué añade.** Motor: `buscar_filas(casillas, cfg)`, `es_recta(casillas)`, `tick_filas(W, cfg, now)`, `abrir_escision`, `profundizar_escision`, `cerrar_escision`, `build_fulguritas(W, cfg, now, out)`; `W['escisiones']` (4.2); exclusiones en `build_rios`/lagos y `build_arqueologia`; `end_cycle` ignora `Colmatacion` en las celdas con escisión. Operadores: Table DAT `escisiones` (4.4), Script CHOP `i_fulguritas`, Geometry COMP `fulguritas`, familia vidrio en `piel_pixel` (o su POP network, P1).

**Parámetros (página Fase26).** `Minfila` 3 · `Tfila` 5 s · `Modofila` cadena · `Conchasporpersona` 1. Para probar, los de la fase 21 (`Simfila`, `Simformarfila`) y `Simsumar` (*propuesto*: añade una persona contigua a la fila).

**Leyenda.**
```
FILA     4 personas   cadena   5.0/5.0 s
ESCISION #3   celda 40   conchas 4/12   abierta   (sin abrir: fila 2.1/5.0 s)
```

**Prueba manual.** Con varias conchas: `Simfila` 3 y `Simformarfila`. A los 5 s se abre un pozo de 3 conchas con su fulgurita en la celda que miraba la casilla más antigua. `Simsumar`: baja una más. `Simvaciar` y otra fila: otra escisión. `Forzarciclo`: el pozo queda tapizado y sigue abierto.

**Autoprueba.**
- 3 personas en cadena en L durante `Tfila`: escisión; con `Modofila` recta, no; en línea, sí.
- 2 personas: no hay fila. Una fila que se rompe a `Tfila` − 0,1 s: nada.
- El origen es la casilla ocupada desde hace más tiempo, y la celda no cambia al girar el planeta.
- 3 personas y `Conchasporpersona` 1 quitan 3 losetas; 2 más mientras aguanta: 5, la misma escisión; con 4 losetas en la columna, se para en el núcleo.
- La fila se deshace y se forma otra: escisión nueva.
- El balance (si existe D3) no cambia; `ero_resto`, `quitadas` y las cicatrices tampoco.
- La concha siguiente la tapiza sin cerrarla, también con `Colmatacion` 1; un río no la llena; la fase 16 no pone fósiles en ella.
- Las inclusiones de la celda de origen se borran (causa `escision`).
- Ninguna pieza de la fulgurita es cian; la línea `FILA` y la `ESCISION`.

### Fase 27 · Relámpago

**Qué hace.** Al abrirse una escisión, un único destello blanco por DMX. Cuenta dentro del límite de 3 destellos por segundo junto con el estroboscopio: un limitador común (una ventana deslizante de 1 s con, como mucho, 3 destellos) por el que pasan todos. Si el limitador está lleno, el relámpago espera al primer hueco y el estroboscopio cede ese destello (**P12**). Solo blanco. En pantalla, opcional: la fulgurita recién abierta sube su emisivo un instante.

**Qué añade.** Motor: `limitador_destellos(W, now)`, `relampago(W, cfg, now)`, eventos para el canal de D3. Operadores: un canal más en el CHOP que alimenta el DMX Out de D3. Sin D3, el evento queda en el motor y en la leyenda.

**Parámetros.** Ninguno nuevo en el encargo. El canal DMX del destello lo fija D3.

**Leyenda.**
```
RELAMPAGO hace 3.2 s   destellos 2/3 en el ultimo segundo   sin DMX
```

**Prueba manual.** Formar una fila: la leyenda dice `RELAMPAGO hace 0.0 s`. Con D3 y el estroboscopio a tope, abrir una escisión: el contador nunca pasa de 3.

**Autoprueba.**
- Una escisión, un destello; profundizarla no da otro.
- Con 3 destellos de estroboscopio en el último segundo, el relámpago espera y nunca hay 4 en una ventana de 1 s.
- El destello es blanco (r = g = b).
- La línea `RELAMPAGO`.

### Fase 28 · Escisiones en el histórico

**Qué hace.**

- **Disparo de testigo:** cada escisión exporta una imagen cuando la fila se deshace o cuando se entierra el mundo, lo que ocurra antes, con su profundidad final.
- **Sección por el origen:** un corte del planeta por el plano que pasa por el centro y la celda de origen, desde la superficie hasta la última concha atravesada, unas celdas a cada lado. Se dibuja **en Python a partir de las columnas** (un Script TOP con numpy, como `alturas` y `cultivos`): cada loseta es una banda de su color, las bandas humanas con sus motas, la escisión con su fulgurita. No hace falta un segundo render ni planos de recorte, y se puede probar fuera de TouchDesigner. Se guarda con `TOP.save()` en PNG.
- **Columna resumen de la jornada:** una columna con una banda por ciclo de la jornada (su tipo: humana, limpia, colapso); cada escisión es una veta que une las bandas que atravesó, con un ancho proporcional a sus personas. Otro Script TOP. Se exporta al cerrar la jornada y la muestra el proyector del histórico (D5).
- **Registro:** cada escisión, con jornada, ciclo, hora, personas, conchas cruzadas y celda de origen (4.4).

**Qué añade.** Motor: `seccion_escision(W, cfg, e, ancho, alto)`, `columna_jornada(W, cfg, jornada)`, `registrar_escision(W, e)`, `exportar_testigo(e)`. Operadores: Script TOP `seccion`, Script TOP `columna_jornada`, Table DAT `escisiones` (de la 26, con las columnas del registro), carpeta `historico/` junto a los scripts. La jornada y el proyector son de D5; hasta entonces, jornada = la fecha del sistema (**P13**).

**Parámetros (página Fase28).** Ninguno en el encargo. Para probar: `Exportartestigo` (*propuesto*: exporta la sección de la última escisión) y `Carpetahistorico` (*propuesto*, por defecto `CARPETA/historico`).

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
W['incl_borradas'] = dict(erosion=0, corte=0, catastrofe=0, escision=0)
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

- Una escisión abierta por fila. Que puedan convivir varias filas en la sala a la vez, cada una con su escisión, es **P14**.
- `W['shells'][s]['rm'][origen] = 1` en cada concha cortada, como `cut`: las fases 8 y 9 la leen sin cambios.
- Lista acotada (`ESCISIONES_MAX` = 200, como `CICLOS_MAX`): las más viejas se quedan solo en el fichero del registro.

### 4.3 Marca de clasificación en las conchas

Campos nuevos en cada entrada de `W['shells']`:

```python
huellas=12,               # inclusiones supervivientes al enterrar
banda='humana',           # 'humana' o 'limpia'
colapso=False,            # marca de cierre, combinable
cierre='estancado',       # motivo del fin de ciclo
incl={40: [k1, k2], 41: [k3]},   # semillas de las inclusiones horneadas, por celda
escisiones=[3],           # ids de las escisiones abiertas en ese mundo (no cuentan en huellas)
```

Una concha sin estos campos (de antes de la fase 24) se lee como `limpia`, sin colapso. Al dibujar, la loseta `[s, g]` de la celda `c` busca `shells[s]['incl'].get(c)` y pone su cobertura en el alfa, con tope `Inclusionesmax`.

### 4.4 Registro del histórico

- **Table DAT `escisiones`** en FASE1, como la tabla `ciclos`: `id`, `jornada`, `ciclo`, `hora`, `personas`, `conchas` (cruzadas), `celda`, `estado`, `testigo`. Últimas 200.
- **Fichero exportable** `historico/escisiones.csv` (UTF-8, separador `;` para abrirlo en una hoja en español, una fila por escisión al cerrarse), y las imágenes `historico/escision_<jornada>_c<ciclo>_<id>.png` y `historico/columna_<jornada>.png`.
- Formato de la hora: `HH:MM:SS` local; jornada: `AAAA-MM-DD` hasta que D5 defina la suya.

---

## 5. Riesgos y rendimiento

| Riesgo | Qué puede pasar | Cómo se acota |
|---|---|---|
| Recuento de personas por fotograma | Leer el mapa de alturas en Python (`numpyArray`) cuesta una lectura de GPU a CPU de 1–2 ms; un máximo local a resolución completa (640 × 576) es caro | Reducir antes en la GPU (Resolution TOP a ~5 cm por píxel: 120 × 120 para 6 × 6 m), máximo local separable en numpy (< 0,5 ms) y solo cuando llega un fotograma nuevo de la cámara (30 fps), no en cada fotograma del render |
| Personas fantasma y parpadeo en las casillas | Un máximo que aparece y desaparece da llegadas falsas; una persona en el borde de dos casillas corta la parada | Seguimiento con radio `Separacioncabezas`; *propuesta* (P2): confirmar una persona nueva tras 2–3 fotogramas y una histéresis de borde de casilla. Afinar en sala |
| Búsqueda de filas | Componentes conexas en cada fotograma | La rejilla de casillas es pequeña (decenas): componentes y prueba de recta, < 0,1 ms |
| Render de la noche | Cambiar materiales o la lista del render recompila o recuece | Solo uniformes y expresiones (`uNoche`, dimmers, color de los constantes); nada sale del render |
| Legibilidad de la escisión | Un pozo de una celda de ancho apenas se ve desde la cámara de globo | La noche y el emisivo de la fulgurita; el testigo la enseña en sección. Revisar en sala |
| Exportación de secciones | Dibujar y guardar una imagen bloquea un fotograma (10–50 ms) | Una vez por escisión; *propuesta*: dejarla para el primer fotograma de la noche o para un fotograma sin cambios del mundo |
| Paleta humana frente a la batería | Las inclusiones (saturadas, en 275°–55°) comparten tonos con la luz de los pads 1–3 | Se distinguen por ser materia (brillo y dispersión), no luz; P5 |
| Choques con fases existentes | Lagos que llenan la escisión, fósiles en sus paredes, `Colmatacion` que la cierra, cicatriz cian | Exclusiones explícitas en la fase 26, cada una con su línea en la autoprueba |
| Cuenta de inclusiones en `W` | El storage crece | Topes por celda (12) y de escisiones (200) |
| Dependencias de v4 | Sin D1 no hay sala real; sin D3, ni relámpago ni balance | Cada fase funciona y se prueba con la simulación; el enchufe a v4 es una función con su contrato (1.3) |

---

## 6. Decisiones pendientes

Cada una con una propuesta, sin darla por cerrada.

| | Pregunta | Propuesta |
|---|---|---|
| **P1** | ¿POPs o instancias para inclusiones y fulguritas? Las fases 11–19 del repositorio no usan POPs (0.3) | Instancias (Script CHOP + Geometry COMP + familia nueva del shader), como el resto: se prueban fuera de TouchDesigner y cuestan lo mismo. Si en local hay fases con POPs, se adopta su patrón; dime cuál |
| **P2** | ¿Cómo se reconoce una persona nueva? | Vecino más cercano con radio `Separacioncabezas`; confirmación tras N fotogramas (parámetro propuesto `Confirmapersona`, 2) para no dar llegadas por ruido |
| **P3** | `Alturamin` y la rejilla de casillas | Que los traiga D1; si no, se crean en la página Fase21 (`Alturamin` 1,0 m, casillas de 0,5 m) y se marcan como de v4 |
| **P4** | ¿Dónde se ve una inclusión? | En el suelo de la celda, medio enterrada alrededor de la formación (se lee como huella y no se mezcla con los modelos temáticos). Alternativa: en el flanco de la formación a la altura de su escalón (dice mejor qué la borra, pero un árbol o un edificio con guijarros de plástico se lee peor) |
| **P5** | Paleta humana | Croma alto en OKLCH sobre 275°–360°, 0°–55° y 100°–120°, con luminosidad distinta de la de los pads; sin rojo saturado puro (el umbral de destellos rojos no aplica a materia, pero mejor no acercarse) |
| **P6** | En una celda vacía, ¿qué golpe la borra? | Cualquier anillo de la erosión que la alcance (peso > 0), aunque ese golpe no quite una nota entera |
| **P7** | ¿La escisión borra las inclusiones de su celda de origen? | Sí: es un corte (2.7 del encargo). Es la ironía de la regla: el colectivo se lleva la huella mínima del sitio donde abre |
| **P8** | Colapso: ¿qué motivos lo marcan y se incluye su fase? | No se incluye en v5: el campo `colapso` queda en las conchas y lo pondrá D4 (erosión dominante sostenida, cuando exista el balance). `estancado` no cuenta como colapso, aunque v4 lo nombre, porque hoy es el cierre normal |
| **P9** | Luz de sala durante la noche | Oscuridad total (como el colapso de v4), cuando exista D3 |
| **P10** | ¿Fase sin página? (la 23 y la 27 no tienen parámetros nuevos) | Página con un solo parámetro de solo lectura (`Version23`), para no romper «una página propia por fase», o sin página: dime cuál prefieres |
| **P11** | ¿Las ramas de la fulgurita quitan material? | No: son solo visuales, finas, dentro de las paredes vecinas |
| **P12** | Relámpago con el limitador lleno | El relámpago tiene prioridad: espera al primer hueco y el estroboscopio cede ese destello |
| **P13** | ¿Qué es una jornada? | La de D5; hasta entonces, la fecha del sistema al abrir la escisión |
| **P14** | ¿Varias filas a la vez? | Sí, cada fila con su escisión. Alternativa: una sola en toda la sala hasta que se deshaga |

Y las del encargo, que se dejan abiertas tal cual:

- **Forma de la fila:** `Modofila` (cadena por defecto, recta).
- **Inevitabilidad estricta:** `Probllegada` = 1, toda llegada deja huella; con menos, quien cruza sin detenerse puede no dejar ninguna.
- **Valores en sala:** `Umbralonset`, `Umbralcorte` (D2), `Tparada`, `Tfila` y `Separacioncabezas` solo se fijan en el espacio real.
- **Colapso por erosión dominante sostenida:** sigue sin fase (P8).

---

## 7. Filas para la hoja de parámetros

Columnas de la hoja `Estratos_parametros`, tal como las pide el encargo. **Nº** queda por asignar: la hoja de Drive es una foto de 64 parámetros de un proyecto en `Nivel` 8, y el número real depende de la hoja actual. Las filas *propuestas* no están en el encargo y solo entran si se aprueba su decisión.

| Nº | Parámetro | Etiqueta en el panel | Tipo | Defecto | Rango | Qué hace | Clave en el motor | Funciones del motor que lo usan | Operadores de FASE1 que condiciona | Lo crea | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| — | `Separacioncabezas` | Separacion minima entre cabezas (m) | float | 0,35 | 0,15–1,0 | Distancia mínima entre dos máximos de altura para contar dos personas; también el radio del seguimiento | `sep_cabezas` | `detectar_cabezas`, `seguir_personas` | `personas`, `casillas` | fase21 | En sala |
| — | `Fuentepersonas` | De donde llegan las personas | menu | camara | camara / simulada / ambas | Elige la cámara, la simulación o las dos | `fuente_personas` | `tick_personas` | `sala`, `personas` | fase21 | Propuesto |
| — | `Simcasilla` | Casilla de prueba | int | 0 | 0–casillas − 1 | Casilla donde actúan los botones de simulación | `sim_casilla` | `simular_personas` | `personas` | fase21 | Prueba sin cámara |
| — | `Simponer` | Poner una persona | pulse | — | — | Pone una persona (una cabeza en el mapa de alturas sintético) en `Simcasilla` | — | `simular_personas`, `on_pulse` | `personas`, `casillas` | fase21 | Mismo camino que la cámara |
| — | `Simquitar` | Quitar la persona | pulse | — | — | Quita la persona de `Simcasilla` | — | `simular_personas`, `on_pulse` | `personas`, `casillas` | fase21 | Prueba sin cámara |
| — | `Simfila` | Personas de la fila de prueba | int | 3 | 1–12 | Cuántas personas pone `Simformarfila` | `sim_fila` | `simular_personas` | `personas` | fase21 | Prueba sin cámara |
| — | `Simformarfila` | Formar una fila | pulse | — | — | Pone `Simfila` personas en casillas contiguas desde `Simcasilla` | — | `simular_personas`, `on_pulse` | `personas`, `casillas` | fase21 | Prueba sin cámara |
| — | `Simvaciar` | Vaciar la sala | pulse | — | — | Quita todas las personas simuladas | — | `simular_personas`, `on_pulse` | `personas`, `casillas` | fase21 | Prueba sin cámara |
| — | `Confirmapersona` | Fotogramas para confirmar una persona | int | 2 | 1–10 | Fotogramas seguidos antes de dar una persona por nueva | `confirma_persona` | `seguir_personas` | `personas` | fase21 | Propuesto (P2) |
| — | `Probllegada` | Probabilidad de huella al llegar | float | 0,6 | 0–1 | Probabilidad de que una llegada deje inclusión (mapa logístico, sin azar) | `prob_llegada` | `llegadas`, `depositar_inclusion` | `inclusiones` | fase22 | 1 = inevitabilidad estricta |
| — | `Tparada` | Tiempo de parada (s) | float | 3 | 0,5–30 | Segundos seguidos en una casilla para dejar una inclusión segura | `t_parada` | `paradas` | `inclusiones`, `casillas` | fase22 | En sala |
| — | `Minhuellas` | Huellas minimas para estrato humano | int | 1 | 1–100 | Inclusiones supervivientes para que la banda sea estrato humano | `min_huellas` | `clasificar_concha`, `contar_huellas` | `estratos`, `ciclos` | fase24 | — |
| — | `Inclusionesmax` | Cobertura maxima de inclusiones | float | 0,8 | 0–1 | Cobertura máxima de inclusiones visibles en una loseta de la banda | `inclusiones_max` | `clasificar_concha`, `build_tiles` | `estratos` (alfa) | fase24 | Antes (v4), proporción de la banda |
| — | `Umbralpresencia` | — | — | — | — | Se elimina | — | — | — | fase24 la quita | No existe en el repositorio |
| — | `Noche` | Noche de enterramiento (s) | float | 4 | 0–30 | Segundos en que la esfera apaga lo mineral al enterrar | `noche` | `noche_nivel` | `luz_principal`, `luz_relleno`, `luz_destello`, `mat_piel_*`, `mat_luz_*` | fase25 | 0 = sin noche |
| — | `Minfila` | Personas minimas de una fila | int | 3 | 2–12 | Personas mínimas en casillas contiguas para formar fila | `min_fila` | `buscar_filas`, `tick_filas` | `escisiones` | fase26 | — |
| — | `Tfila` | Tiempo de la fila (s) | float | 5 | 0,5–60 | Segundos que debe sostenerse la fila para abrir la escisión | `t_fila` | `tick_filas` | `escisiones` | fase26 | En sala |
| — | `Modofila` | Forma de la fila | menu | cadena | cadena / recta | Forma válida de la fila: cualquier forma contigua o en línea | `modo_fila` | `buscar_filas`, `es_recta` | `escisiones` | fase26 | Decisión abierta del encargo |
| — | `Conchasporpersona` | Conchas por persona | int | 1 | 1–12 | Conchas que abre cada persona de la fila | `conchas_persona` | `abrir_escision`, `profundizar_escision` | `estratos`, `fulguritas` | fase26 | Tope: el núcleo |
| — | `Simsumar` | Sumar una persona a la fila | pulse | — | — | Añade una persona contigua a la fila simulada | — | `simular_personas`, `on_pulse` | `personas`, `casillas` | fase26 | Propuesto |
| — | `Exportartestigo` | Exportar el testigo de la ultima escision | pulse | — | — | Exporta la sección de la última escisión | — | `exportar_testigo`, `on_pulse` | `seccion` | fase28 | Propuesto |
| — | `Carpetahistorico` | Carpeta del historico | str | CARPETA/historico | — | Dónde se guardan las imágenes y el registro | `carpeta_historico` | `exportar_testigo`, `registrar_escision` | `seccion`, `columna_jornada`, `escisiones` | fase28 | Propuesto |

---

## 8. Fuera de alcance

Como dice el encargo: las variantes de v4 (proyector en plano y controlador de sesgo), la clasificación del mundo por timbres, la entrada de voltajes por ethernet y cualquier cambio en la propuesta artística o en el marco conceptual. Tampoco entra aquí construir las dependencias D1 a D5: el plan dice qué necesita de ellas y deja cada fase lista para funcionar sin ellas.

---

## 9. Para la revisión

Antes de escribir la fase 21 necesito:

1. Saber si las piezas de v4 (D1 a D5) y una posible fase 20 existen en la carpeta local. Si existen, que se suban al repositorio para ajustar el inventario.
2. La decisión **P1** (POPs o instancias).
3. El visto bueno al orden (21 a 28) y a las propuestas que se quieran cerrar ya (sobre todo P2, P4, P7 y P14).
