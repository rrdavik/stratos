# Requerimiento · Fase 14 — Destructores I: arañazos y escalada

> **Implementado** en `fase14_destructores.py` (`fase14 v1`, `motor v34`, `comun v25`). Lo que se decidió en cada punto abierto está en `MONTAJE_FASES_11_18.md`, sección *Decisiones tomadas en la fase 14*. Este documento queda como referencia de lo que se pidió.

*Para una sesión de Claude Code en la nube sobre el repositorio `rrdavik/stratos`. Es autosuficiente: lee esto entero antes de tocar nada y después `MONTAJE_FASES_11_18.md` (fases 11 a 13). El plan completo de las fases 11 a 18 está en el doc «Estratos · Plan de fases 11–18»; lo que importa de la fase 14 está copiado aquí.*

---

## 1. Qué hay que hacer

Los arañazos de la batería (fase 7) reciben forma temática, y la insistencia destructiva escala igual que la constructiva. **Un golpe es un accidente; varios golpes en la misma zona, una catástrofe.**

| Especie | Un golpe | Escalada | Huella |
|---|---|---|---|
| Vegetación (naturaleza, SEQ1) | Rayo que tala el árbol más alto | Incendio que avanza por los puentes del dosel | Claro de ceniza |
| Relieve (naturaleza, SEQ2) | Desprendimiento de columnas | Derrumbe de la meseta | Pedregal |
| Informal (ciudad, SEQ1) | Se desploma un añadido | Derrumbe en cadena del barrio | Escombros |
| Planificada (ciudad, SEQ2) | Caen las plantas altas | Demolición por implosión, con polvo | Solar vallado |

Hay **escalada** cuando caen `Golpesescalada` golpes o más en la misma vecindad dentro de `Ventanaescalada` pasos.

- **Incendio.** Es un autómata de Drossel–Schwabl acotado:
  - el fuego salta a las celdas del cluster que tienen vegetación;
  - cada celda que arde pierde 1 de ocupación por paso;
  - se apaga cuando no queda combustible o tras `Pasosfuego` pasos;
  - el salto lo decide el **mapa logístico**, no el azar;
  - **el fuego no sale del cluster** (decisión ya tomada en el plan).
- **Tránsitos inversos.** Si una obra a medias (cadena de fusión o coronación de la fase 11, sin terminar) recibe erosión, se convierte en derribo: la cadena se recorre hacia atrás.
- **Partículas.** Ceniza, brasas (ámbar, emisivas) y polvo, como instancias del motor. El polvo forma una nube local que se disipa en `Pasospolvo` pasos.
- **Presupuesto.**
  - La escalada cuenta como erosión y entra en el umbral de densidad del 60 % (`Umbraldensidad`, `dens_umbral`): por encima, la catástrofe se agranda con `Multradio`, igual que la erosión de la fase 7.
  - `Maxfuego` limita las celdas que arden a la vez.

**Parámetros** (página `Fase14`): `Ventanaescalada` 8 · `Golpesescalada` 2 · `Pasosfuego` 6 · `Maxfuego` 6 · `Pasospolvo` 8.

**Línea de la leyenda** (formato de las otras, en mayúsculas y sin tildes en el código):

```
EROSION  pad 5 rayo celda 52 · INCENDIO 4 celdas paso 3/6
```

### Ojo: qué pads son «arañazos»

El plan habla de «pads 1–5», pero el usuario ha cambiado los perfiles de erosión. Los de ahora son `PERFILES_DEFECTO` en `estratos_motor.py`, con el formato `(reducción, radio, profundidad)`. **Bombo, caja y tom (pads 1–3) cortan** y los pads 4–8 son arañazos. Por eso:

- un **arañazo** es cualquier pad cuyo perfil tiene profundidad 0, es decir, todo pad que no esté en `pads_corte(cfg)`. No lo fijes por número;
- los **cortes** (profundidad > 0) siguen como en la fase 9; su versión temática es la fase 16, no esta;
- la prueba del plan («Padprueba 3 dos veces sobre un bosque») hay que hacerla con un pad de arañazo, por ejemplo `Padprueba` 5.

### Decisiones que tienes que concretar (con propuesta por defecto)

Elige y documenta. Si una no encaja, avisa en el PR.

1. **Vecindad de la escalada.** Propuesta: la celda objetivo y sus vecinas (`NEIGH`). Dos golpes cuentan como la misma zona si el objetivo de uno está en la vecindad del otro.
2. **«Tala el árbol más alto».** Propuesta: entre la celda objetivo y sus vecinas con vegetación, la de más altura lógica (`W['h']`) pierde su protagonista o su coronación: baja de estado deshaciendo notas con `degrade()` hasta el estado anterior. Empate: la de índice menor.
3. **Las otras catástrofes.** Propuesta: se propagan por la máscara del cluster (`clusters()['mascara']`) una celda por paso, con la misma regla de −1 de ocupación por paso y el mismo tope de pasos que el fuego. La implosión de la planificada es instantánea en su celda, deja polvo y no se propaga.
4. **Huella.** Propuesta: es un estado visual de la celda vacía que queda hasta que una nota vuelve a sembrarla. Hacen falta modelos nuevos: claro de ceniza, pedregal y escombros (el solar vallado reutiliza `ciu_valla`). Se guarda en el mundo (`W`) y la borra la siguiente nota de construcción en esa celda.
5. **Fin de ciclo.** El entierro (fase 6/8) apaga todos los fuegos y cierra las catástrofes: ninguna queda colgada (criterio de cierre de la fase 18). Las huellas desaparecen con el mundo enterrado.

---

## 2. El proyecto, en lo que necesitas saber

**Qué es.** Una pieza visual en **TouchDesigner**. Un planeta crece con lo que tocan dos secuenciadores y una batería de un Arturia BeatStep Pro:

- SEQ1, canal 13: especie GEO;
- SEQ2, canal 14: especie ARQ;
- batería, canal 16, notas 36–43 = pads 1–8.

Las fases 3 a 13 están hechas y probadas.

**Cómo se ejecuta.** Cada fase es un script que el usuario lanza desde el Textport de TouchDesigner:

```python
exec(open('C:/Users/DareDave/Downloads/est/fase14_destructores.py').read())
```

Los scripts trabajan sobre `/project1/FASE1`, siempre encima de lo anterior, y deben poder **relanzarse** sin borrar el mundo.

**Archivos clave.**

| Archivo | Qué es |
|---|---|
| `estratos_motor.py` | Toda la lógica (ahora `motor v33`). Primero va el **NÚCLEO**, Python puro sin TouchDesigner: mundo `W`, reglas, instancias. Después el **ADAPTADOR**, que habla con TD: `cfg()` lee los parámetros con `_p()`, `chop_names()`, `frame_tick()`, `on_pulse()`, `legend()`, cámara. Las fases se activan con `cfg()['nivel']`. |
| `estratos_comun.py` | Piezas compartidas por los scripts de fase (ahora `comun v24`): `require_base`, `install_core`, `get_page`, `add_par`, `renew_default`, `make_instanced`, `instanciar_modelos`, `materiales_piel`, `set_render`, `leeme`, `print_report`, `run_test` / `Prueba`, shaders de la piel. |
| `fase13_tejido.py` | **Plantilla** de un script de fase: cabecera, `VERSION`, página de parámetros, geometría, `leeme`, autoprueba. |
| `fase11_piel.py` | Catálogo (tabla `catalogo`), modelos (`modelos` COMP con los SOP de cada modelo), partículas. |
| `fase7_erosion.py`, `fase9_arqueologia.py` | La erosión (`erosion()`, perfiles, `Padprueba` + `Erosionar`) y los cortes. |
| `pruebas/td_simulado.py` | TouchDesigner simulado. Los COMP solo aceptan sus parámetros reales (lista `STRICT`). |
| `pruebas/correr_fases.py` | Corre todas las fases desde cero, una sesión simulada por MIDI, relanza todas las fases y otra sesión. Hoy da 26 líneas `OK`. |
| `pruebas/vista_previa.py` | Hoja de contactos PNG del catálogo de modelos (`pruebas/catalogo.png`). |
| `pruebas/glsl_piel.py` | Compila el shader de la piel con OpenGL real: `xvfb-run -a python3 pruebas/glsl_piel.py`. |
| `MONTAJE_FASES_11_18.md` | Documentación de las fases 11+: tabla de archivos y versiones, una sección por fase, cómo se ha probado, problemas frecuentes. |
| `constructor stratos` | Las líneas `exec(...)` de todas las fases, en orden. |

**Lo que ya existe y debes reutilizar.**

- **Erosión** (fase 7):
  - `erosion(W, cfg, pad, vel, now)`: elige el objetivo con `pick_target`, deshace notas en anillos (`rings`, `ATENUACION`) con `degrade(W, cfg, i, k)`, ilumina con `light_cell`, guarda el evento en `W['ev']['erosion']` y cuenta golpes en `W['hits'][3]`;
  - densidad `occupied(W) / N` frente a `dens_umbral`, con `rad_mult`;
  - la llama `midi_note_on` (canal `Canaldrum`) y el pulso `Erosionar` (con `Padprueba` y `Velprueba`).
- **Piel** (fase 11):
  - `clusters(W, cfg)` devuelve `de`, `celdas`, `capital` y `mascara`;
  - `especie_de(tema, own)`, `estado_idx`, `modelos_de(cfg, tema, esp, estado)` y `cadenas_de`;
  - etapas de obra `W['et_f']` / `W['et_c']` con `_etapa`, `tick_piel` (las obras ya retroceden cuando baja su objetivo), `avance_etapa` y `cerrar_obras` (fin de ciclo);
  - `build_piel()` emite las filas de instancia por modelo;
  - partículas con `_particulas(out, n, p0, cw, cl, vh, semilla, k, col, now, paso, modo)` en la geometría `particulas`, de material constante, así que el color de la instancia se ve como emisivo;
  - colores `COL_ESPORA`, `COL_POLVO`, `COL_OBRERO`.
- **Sin azar de software**: `semilla_caos(vel, celda)` y `logistica(x0, r, n)` (mapa logístico, r = `Caos`).
- **Duraciones en pasos**: `step_dur(cfg, tempo)` y `W['paso']`. Un paso a 120 BPM son 125 ms. **La animación no decide**: el estado lógico cambia al instante y lo visual lo persigue (stop-motion, `_stop`, `FOTOS_PASO`).
- **Mundo**: `new_world()` define todas las claves. `ensure(W)` migra los mundos guardados añadiendo las que falten, así que las claves nuevas van en `new_world()` y se migran solas.
- **Catálogo**: las filas por defecto salen de `_catalogo_defecto()`. Si a la tabla `catalogo` de TD le falta un estado, `modelos_de()` usa el de por defecto, de modo que los estados nuevos (por ejemplo `huella`) funcionan aunque el usuario no relance la fase 11. Los **modelos** se definen en `_modelos()` con prims `('caja' | 'hexa', cx, cy, cz, sx, sy, sz, rx, ry, rz)`; `PIE` dice cómo se apoyan y `familia_de(modelo)` qué material llevan. En TD cada modelo necesita sus SOP dentro de `modelos` (los construye `fase11_piel.py`) y su geometría `mod_<modelo>` (`instanciar_modelos(base, m)`). Para modelos nuevos, la fase 14 tiene que crear sus SOP y sus geometrías: lo más limpio es mover a `estratos_comun.py` la parte de `fase11_piel.py` que construye los SOP y llamarla desde las dos fases.

---

## 3. Reglas del proyecto (obligatorias)

- **Un script por fase**: `fase14_destructores.py`, sobre la plantilla de `fase13_tejido.py`:
  - cabecera con QUÉ HACE / PROBAR SIN BEATSTEP / CÓMO USARLO;
  - `VERSION = 'fase14 v1  (...)'` y `banner(VERSION)`;
  - `require_base(14)` e `install_core(base, CARPETA, 14)`;
  - página `Fase14` con `add_par` (nunca pisa un valor que el usuario haya tocado);
  - `leeme(base, 14, ...)` y `print_report()`;
  - autoprueba con `run_test(base, prueba)`, que restaura los parámetros que toque, como `fase13_tejido.py`.
- **Todo valor es un parámetro** de su página y tiene **una línea en la leyenda**.
- **Prueba sin BeatStep con un botón**: `Padprueba` + `Erosionar` ya existen; añade lo que haga falta.
- **Lógica en el motor, piel en el catálogo.** Sube `MOTOR_VERSION` (`motor v34`) y, si tocas `estratos_comun.py`, `VERSION_COMUN` (`comun v25`).
- **Por debajo del nivel 14 nada cambia**: relanzar las fases 7 y 9 en un proyecto que ya está en la 14 tiene que seguir dando `AUTOPRUEBA OK`. Si alguna comprobación antigua deja de valer en el nivel 14, limítala al nivel 13, como se hizo en las fases 3, 4 y 7 con el nivel 10.
- **Código**: comentarios y textos de TD en español **sin tildes** (TouchDesigner y el Textport); documentación (`.md`) en español con tildes. Imita el estilo del código de alrededor.
- **Rendimiento**: el fotograma del motor anda por 4,5 ms en el simulador. Nada de bucles pesados por fotograma: usa cachés como `_CLUSTERS`, `_TEJIDO` o `_COMPUESTOS` y recalcula solo cuando cambie el estado.

### Lo que ya ha fallado en el TouchDesigner real (no lo repitas)

- El color de una Light COMP es `cr cg cb`, no `lightcolorr/g/b`.
- Los parámetros que apuntan a un operador (`material`, `instanceop`, `lookat`) devuelven el **operador** con `.eval()`, no el texto: compara con `nombre_op()`.
- **Nunca leas `.width` / `.height` de un TOP en una expresión**: crea un bucle de cocinado con el render. Usa sus parámetros `resolutionw/h`.
- Nada de «rotar hacia un vector» en las instancias: el motor da `rx ry rz` (`orient`, `_euler_xyz`).
- **No toques la cámara**: el encuadre solo cambia con una concha nueva (motor v33). Si algo de la fase 14 sube más que la altura máxima, no muevas la cámara por ello.
- Nada de caras coplanarias que se solapen: producen parpadeo (z-fighting). Varía un poco las alturas, como en los medios puentes de la v33.
- Una geometría nueva solo se dibuja si su nombre está en `RENDER_ORDER` (comun) o empieza por `mod_`; `set_render(base)` reescribe la lista. Su Script CHOP es `i_<nombre>` con `formas_callbacks` y tiene que estar en `chop_names(c)`.
- El color por instancia va en Instance 2 → Color R/G/B = `r g b` con Color Mode = Replace. La rugosidad de la piel va en el canal `a` (alfa).
- Materiales: la vegetación usa `mat_piel_dosel` (vegetal), el relieve `mat_piel_mineral`, la ciudad `mat_piel_ciudad` y las obras `ciu_*` usan `mat_poroso`. Las brasas pueden ir en `particulas` con un color ámbar alto.

---

## 4. Pruebas y criterios de aceptación

1. `python3 pruebas/correr_fases.py`, con `fase14_destructores.py` añadido a `FASES`: todo `OK`, también el relanzamiento sobre el proyecto avanzado y las dos sesiones simuladas (0 expresiones con error, el mundo se conserva).
2. La autoprueba de la fase 14 comprueba, por lo menos:
   - un golpe de arañazo sobre cada especie hace su accidente (rayo, desprendimiento, añadido, plantas altas) y deja su evento en la leyenda;
   - `Golpesescalada` golpes en la misma vecindad dentro de `Ventanaescalada` pasos inician la catástrofe; los mismos golpes fuera de la ventana o en zonas separadas no la inician;
   - **incendio**:
     - solo arde dentro del cluster y solo vegetación;
     - cada celda pierde 1 de ocupación por paso;
     - se apaga sin combustible o tras `Pasosfuego`;
     - nunca hay más de `Maxfuego` celdas ardiendo;
     - **misma historia, mismo fuego** (determinista);
   - la ceniza, las brasas y el polvo aparecen como instancias de `particulas`, y el polvo se disipa en `Pasospolvo`;
   - la huella (claro de ceniza, pedregal, escombros, solar vallado) queda en la celda y la borra la siguiente nota de construcción;
   - una obra a medias que recibe erosión recorre su cadena hacia atrás;
   - presupuesto: con densidad por encima de `Umbraldensidad`, la catástrofe se agranda con `Multradio`;
   - `Forzarciclo` con un fuego activo: el fuego se apaga y no queda ningún tránsito colgado;
   - en el nivel 13 (o con el arañazo como cortes) se mantiene el comportamiento de antes.
3. Si añades modelos, regenera `pruebas/catalogo.png` con `python3 pruebas/vista_previa.py pruebas/catalogo.png` y míralo: deben leerse de lejos y sin caras coplanarias.
4. Si tocas el shader, `xvfb-run -a python3 pruebas/glsl_piel.py` debe decir que compila.

## 5. Entregables

- `fase14_destructores.py` (`fase14 v1`), `estratos_motor.py` (`motor v34`) y `estratos_comun.py` (`comun v25`) si hace falta.
- `pruebas/correr_fases.py` con la fase 14 y el simulador al día si hace falta (un parámetro de COMP nuevo va a `STRICT`).
- `MONTAJE_FASES_11_18.md`:
  - tabla de archivos y versiones al día, con la línea `exec` de la fase 14;
  - una sección **FASE 14** con el mismo formato que las de las fases 11 a 13: qué hace, decisiones tomadas, parámetros, leyenda, cómo probarlo en TD sin BeatStep;
  - lo comprobado en *Cómo se ha probado* y las filas nuevas de *Problemas frecuentes*.
- `constructor stratos` con la línea de la fase 14.
- Commits en español, en una rama propia, y un **pull request a `main`** que diga qué se decidió en cada punto de «Decisiones que tienes que concretar» y qué no se ha podido comprobar fuera de TouchDesigner (el aspecto en pantalla).

**Para el usuario, al final:** qué archivos descargar a `C:/Users/DareDave/Downloads/est`, qué fase lanzar y qué líneas del informe confirman que ha ido bien (`fase14 v1`, `motor v34`, `AUTOPRUEBA OK`).
