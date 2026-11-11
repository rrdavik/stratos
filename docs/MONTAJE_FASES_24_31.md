# Estratos · Montaje
## Fases 24 a 31: la huella inevitable (plan v5)

*Continúa `MONTAJE_FASES_21_23.md`. Referencia: `docs/PLAN_V5.md` (el doc «Estratos · Plan v5: la huella inevitable», decisiones P1 a P14 cerradas el 28 de octubre de 2026). Las reglas de siempre: un script por fase, encima de la anterior, con su versión en la primera línea del informe, su página `FaseNN`, su línea en la leyenda, su `LEEME` y una AUTOPRUEBA al final que deja el mundo como estaba. El motor gana una versión por fase (de la v83 a la v90). Para tenerlo todo al día, `recargar_todo.py`.*

**Antes de nada:** las fases 24 a 31 necesitan la cámara (o su sala simulada) de la fase 22 y la luz de sala de la fase 23. Todo se prueba sin cámara con `Fuente` = simulada (página Fase22). Las autopruebas de todas las fases corren con `Activo` apagado (el sorteo de la fase 22), para probar lo suyo con todas las señales. Y con `Noche` a 0 (comun v70), salvo las de las fases 23, 27 y 28, que la prueban: así la noche de enterramiento no apaga lo que otras fases miran justo después de enterrar. Al terminar devuelven tus valores.

| Fase | Script | Qué hace | Motor |
|---|---|---|---|
| 24 | `fase24_personas.py` | Personas: cabezas, seguimiento, casillas ocupadas y la celda que miran | v83 |
| 25 | `fase25_huella.py` | Huella mínima: inclusiones por llegada y por parada, con su escalón | v84 |
| 26 | `fase26_borrado.py` | Borrado: la erosión borra las inclusiones que quedan sobre su escalón | v85 |
| 27 | `fase27_clasificacion.py` | Clasificación al enterrar: estrato humano o concha limpia, y el colapso | v86 |
| 28 | `fase28_noche.py` | Noche de enterramiento: la esfera se apaga y emiten las inclusiones horneadas | v87 |
| 29 | `fase29_fila.py` | Fila y escisión colectiva: un hueco permanente con su fulgurita | v88 |
| 30 | `fase30_relampago.py` | Relámpago: un destello blanco con prioridad al abrirse cada escisión | v89 |
| 31 | `fase31_historico.py` | Escisiones en el histórico: testigo en sección, columna de la jornada y registro | v90 |

---

## FASE 24 · Personas

```python
exec(open('C:/Users/DareDave/Downloads/est/fase24_personas.py').read())
```

### Qué hace

Convierte la cámara de la fase 22 (o su sala simulada) en personas. No cambia el mundo todavía: prepara lo que usan las fases 25 (huellas) y 29 (filas). En cada imagen de la cámara (30 por segundo):

1. **Máximos de altura.** Sobre `alturas_sala` (la altura de cada píxel, a unos 5 cm): un píxel es una cabeza si supera `Alturamin`, no pasa de `Alturamax` (fase 22) y es un máximo local. Dos máximos más cerca que `Separacioncabezas` (0,35 m) cuentan como una persona: se queda el más alto.
2. **Seguimiento por vecino más cercano.** Los máximos se emparejan con las personas de la imagen anterior, de la pareja más cercana a la más lejana, sin pasar de `Separacioncabezas`. Un máximo sin pareja durante `Confirmapersona` imágenes seguidas (2) es una **persona nueva** (P2). Una persona sin máximo desaparece.
3. **Ocupación binaria por casilla.** Una casilla está ocupada si tiene al menos una persona confirmada. Guarda el instante en que se ocupó (`t_ocupada`) y lo pierde al quedar libre. No pasa por ningún suavizado. Una persona en el borde de dos casillas no cambia de casilla hasta pasar 8 cm del borde.
4. **La celda que mira a la casilla**, en el instante de cada evento: el mapeo de la fase 22 con `Loncentral` de esa imagen (sigue al giro).

La densidad suavizada de la fase 22 sigue a lo suyo (el sorteo de las señales) y aquí no se usa. El estado del sensor (pistas, casillas, contadores) vive en el módulo del motor (`_SALA`), no en `W`.

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `alturas_sala` | La imagen de alturas de la fase 22; el motor la lee una vez por imagen de la cámara y de ella salen la densidad (fase 22) y las cabezas |
| `personas_chop` | Script CHOP: `personas`, `casillas` (ocupadas) y `nuevas` |
| `personas` | Table DAT: `id`, `x`, `y` (m), `altura`, `casilla`, `desde` (s), `nueva` |
| `casillas_ocupadas` | Table DAT: `casilla`, `ocupada`, `personas`, `t_ocupada` (s que lleva ocupada), `celda` (la que mira ahora) |

### Parámetros (página Fase24)

`Separacioncabezas` 0,35 m · `Confirmapersona` 2 · `Simfila` 3 · `Simformarfila`

### Leyenda

```
PERSONAS 3 en sala   casillas 3/99   nuevas 12   simulada
```

### Probar sin cámara

`Fuente` = simulada (fase 22). `Simponer`: `PERSONAS 1`, `nuevas` sube 1 y `casillas_ocupadas` dice qué celda mira. Espera media vuelta del planeta y pulsa en otra casilla: la celda es otra. `Simquitar`: `PERSONAS 0`. `Simfila` 4 y `Simformarfila`: 4 personas en casillas contiguas desde `Simcasilla` (al llegar a la pared, la fila dobla por la casilla de debajo). Las personas simuladas son discos de 1,70 m (más altos en el centro) en la misma imagen que la cámara: de ahí en adelante todo es igual.

### Autoprueba

- dos cabezas a 0,30 m cuentan una (la más alta); a 0,40 m, dos; bajo `Alturamin` o sobre `Alturamax`, ninguna;
- una persona que se mueve 0,10 m por fotograma es la misma; una que aparece a 1 m es nueva a los 2 fotogramas; un máximo de un solo fotograma no lo es; sin máximo, desaparece;
- `Simponer` llega por la imagen de la sala; la ocupación no tiene suavizado (con `Confirmapersona` 1, en el mismo fotograma); `t_ocupada` se guarda y se pierde al quedar libre; la histéresis del borde;
- la celda de una casilla sigue a `Loncentral`, y la llegada lleva la celda de ese instante;
- `Simformarfila`, la fila que dobla, la línea `PERSONAS`, `personas_chop` y `Simvaciar`.

### Decisiones tomadas en la fase 24

| Pregunta | Decisión |
|---|---|
| ¿Quién lee la imagen? | El motor, desde `latido` (`sala_tick`), una vez por imagen de la cámara: es la misma lectura de la fase 22. `personas_chop` solo enseña los contadores |
| ¿Radio del máximo local? | Media `Separacioncabezas` (los hombros de alguien más alto no tapan una cabeza vecina); la separación entera la impone el descarte, de la cabeza más alta a la más baja |
| ¿Cuándo está ocupada una casilla? | Con una persona **confirmada**: con `Confirmapersona` 2, una imagen después de entrar (33 ms). Así un máximo fantasma no ocupa nada |
| ¿Una mesa o un bulto plano y alto? | Sale como varias «cabezas»: el detector supone personas. `Alturamin` y la captura del fondo lo evitan |

### Pruebas pendientes con el aparato

1. `Separacioncabezas`, con dos personas juntas y con un niño al lado de un adulto.
2. El paralaje: una cabeza a 1,7 m sale desplazada hacia fuera respecto a los pies; las casillas de 0,5 m deberían absorberlo.
3. El coste de la lectura de `alturas_sala` en el Performance Monitor (presupuesto: menos de 1 ms por fotograma).

---

## FASE 25 · Huella mínima

```python
exec(open('C:/Users/DareDave/Downloads/est/fase25_huella.py').read())
```

### Qué hace

Las personas dejan **inclusiones** en la celda que mira a su casilla. No construyen ni erosionan, pero no pueden pasar sin dejar algo.

- **Llegada.** Al detectarse una persona nueva (fase 24) deja una inclusión con probabilidad `Probllegada` (0,6). **Sin azar de software:** el sí o el no lo decide el mapa logístico sembrado con el id de la persona, la celda y el ciclo, así que la misma sala da el mismo resultado. Con `Probllegada` 1, toda llegada deja huella (la «inevitabilidad estricta», que sigue abierta).
- **Parada.** `Tparada` segundos (3) seguidos con la casilla ocupada, sobre la ocupación binaria, dejan una inclusión segura. Una por parada: la casilla se rearma al quedar libre.
- **Escalón.** Cada inclusión guarda el escalón (`occ`) de su celda en el instante en que cae; en una celda sin construir, 0. La celda es la que miraba la casilla en ese instante: el planeta sigue girando y la inclusión se queda donde cayó.
- **Varias por celda:** una lista por celda, de la más antigua a la más nueva, con tope de 12 (`INCL_CELDA`): el exceso quita la más antigua de las de escalón más alto. 85 celdas × 12 = 1020 como mucho.
- **Aspecto (plastiglomerado).** La matriz es la loseta de la celda, mineral mate: en las celdas con inclusiones su tapa baja de rugosidad 1 a 0,85 (el resto sigue con la regla de la fase 8). Las inclusiones son piezas pequeñas (del 3 al 7 % de la celda), **medio enterradas en el suelo de la celda, alrededor de la formación** (P4), de color saturado de la paleta humana, rugosidad 0,1–0,2 y una dispersión leve (familia nueva del shader de la piel: `plastico`, envoltura de luz y un aclarado a contraluz).
- **La paleta humana (P5).** Croma alto en OKLCH (0,19, lo justo más bajo para caber en sRGB) y luminosidad 0,75 (ni la de los pads oscuros, 0,53–0,69, ni la de los claros, 0,81–0,85), sobre los tonos que quedan libres: 275°–360°, 0°–18°, 40°–55° y 100°–120°. Nunca el ámbar del SEQ2 (55°–100°), los verdes de los pisos (120°–165°), el cian de las cicatrices (165°–235°) ni el azul de los ríos (235°–275°), y sin el rojo saturado puro (18°–40°).
- **Al enterrar** el mundo las inclusiones se vacían: lo heredado empieza sin ninguna. (La fase 27 las cuenta y las hornea antes.)

Las inclusiones son mundo: viven en `W['incl']` (`[escalon, tipo, t, k]`: tipo 1 llegada, 2 parada; `k`, la semilla de su color, posición y tamaño) y se guardan con el `.toe`. El nombre `huella` ya es de la fase 7 (la mancha de la semilla borrada).

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `i_inclusiones`, `inclusiones` | Script CHOP y Geometry COMP instanciado: una esfera de pocas caras por inclusión, deformada y girada por su semilla, con `mat_piel_plastico`. En el render, tras las coronas |
| `mat_piel_plastico`, `mat_piel_vidrio` | Dos familias nuevas del shader de la piel (`uFamilia` 5 y 6). La segunda es para la fulgurita de la fase 29 |

### Parámetros (página Fase25)

`Probllegada` 0,6 · `Tparada` 3 s

### Leyenda

```
HUELLA   inclusiones 17 (llegadas 11, paradas 6)   ultima celda 40 escalon 3 (parada)   llegada 0.6   parada 3 s
```

Las llegadas y las paradas son las de este mundo (las que dejaron inclusión, sigan vivas o no).

### Probar sin cámara

`Fuente` = simulada. `Probllegada` 1 y `Simponer`: aparece una inclusión en la celda que mira a la casilla. `Probllegada` 0 y `Simponer`: nada; deja la persona 3 s: aparece una (parada). Mantenla más: no aparece otra. `Simquitar` y `Simponer` en la misma casilla: puede salir otra.

### Autoprueba

- `Probllegada` 1: toda llegada deja huella; 0: ninguna; 0,6 sobre 1000 llegadas: entre 0,55 y 0,65, la misma sala da las mismas, y otro ciclo da otro reparto;
- la parada a `Tparada` menos un fotograma no deja nada; a `Tparada`, una; seguir quieto no deja más; tras quedar libre, se rearma; una persona que oscila dentro de su casilla sigue parada;
- la inclusión guarda el escalón de su celda (0 en una vacía) y la celda del instante en que se confirmó la persona;
- la paleta humana: ningún tono prohibido y luminosidad distinta de la de los pads;
- el tope de 12 por celda; una instancia por inclusión, pequeña, en el suelo de su celda y con rugosidad 0,1–0,2; `i_inclusiones` en el render; la tapa a 0,85; al enterrar se vacían;
- `Simponer` por la sala simulada y la línea `HUELLA`.

Además, `xvfb-run -a python3 pruebas/glsl_piel.py` compila el shader de la piel con las familias nuevas en un OpenGL de verdad.

### Decisiones tomadas en la fase 25

| Pregunta | Decisión |
|---|---|
| ¿Semilla de la llegada? | `0,05 + 0,9 × frac(id × 0,618 + celda × 0,382 + ciclo × 0,137)` al mapa logístico (r = 4), llevado a uniforme. El id de la persona es el del seguimiento (empieza de cero al recargar el motor) |
| ¿Rojo? | Fuera de la paleta de 18° a 40° («sin rojo saturado puro», P5), además de las bandas reservadas |
| ¿Antes de la fase 27? | Al enterrar, las inclusiones se vacían sin contarse |

### Pruebas pendientes en sala

`Tparada`, y si `Probllegada` se queda en 0,6 o pasa a 1. Que las inclusiones se lean desde la cámara de globo (son pequeñas a propósito: la noche de la fase 28 las enseña).

---

## FASE 26 · Borrado por erosión

```python
exec(open('C:/Users/DareDave/Downloads/est/fase26_borrado.py').read())
```

### Qué hace

Una inclusión desaparece cuando la erosión baja su celda por debajo de su escalón (`occ < escalón`). Bajar la carga sin bajar el escalón no la borra. En una celda sin construir (escalón 0), **cualquier golpe de erosión que la alcance la borra: cualquier anillo con peso mayor que 0, aunque ese golpe no quite una nota entera** (P6).

Valen todas las fuentes: la caja y los arañazos (pads 2 y 4–8), el micrófono (fase 21: el pad 9 y su corte por ruido), los cortes (vacían la celda y se llevan todas sus inclusiones, también las de escalón 0), los accidentes y las catástrofes de la fase 14 (bajan la ocupación) y, desde la fase 29, la escisión (es un corte, P7). El bombo y el tom no borran: son impulso y suben la ocupación. Un golpe que no prende (el sorteo de la fase 22) tampoco.

**Cómo** (sin tocar las reglas de la erosión):

- un único punto de purga, `purgar_inclusiones(W, celda, causa)`, que llaman `_undo_note` y `bajar_escalon` cuando baja la ocupación de una celda (por ahí pasan los arañazos, el micrófono, los accidentes y las catástrofes);
- `erosion()` llama además a `golpe_inclusiones(W, celda)` en cada celda de sus anillos, para el caso de la celda vacía;
- `cut()` llama a `borrar_inclusiones(W, celda, 'corte')` en cada celda que vacía;
- una pasada de seguridad por fotograma (`purga_segura`), solo en las celdas con inclusiones.

Ningún operador nuevo: la geometría de la fase 25 deja de dibujarlas. Los contadores por causa viven en `W['incl_borradas']` y no se ponen a cero al enterrar (sí con `Resetmundo`).

### Parámetros

Ninguno nuevo. La página Fase26 lleva solo `Version26`, de solo lectura (P10), para mantener una página por fase.

### Leyenda

```
BORRADO  vivas 12   borradas 5 (erosion 2, micro 1, corte 1, catastrofe 1)
```

Las causas: `erosion` (un arañazo), `micro` (un onset), `corte` (la caja o cualquier pad que corte, y el corte por ruido de sala), `catastrofe` (el accidente o la catástrofe de la fase 14) y, desde la fase 29, `escision`.

### Probar

`Sembrar` cuatro veces en una celda (escalón 4), `Probllegada` 1 y `Simponer` en la casilla que la mira (la tabla `casillas_ocupadas` dice qué celda mira cada casilla): la inclusión guarda el 4. `Padprueba` 7 y `Erosionar` hasta que la leyenda `ULTIMA` diga ocupación 3 o menos: la inclusión desaparece. En una celda vacía: un solo `Erosionar`, o una `Palmada` de la sala virtual, la borra. Recuerda apagar `Activo` (fase 22) para que todos los golpes prendan.

### Autoprueba

- escalón 4: bajar la carga no la borra; bajar a 3, sí; con los arañazos de un pad, en cuanto la celda baja de 4; en el nivel 25, nada se borra;
- celda vacía: un arañazo flojo la borra aunque no quite nada, también en el segundo anillo (y no más allá del radio); un onset del micrófono la borra (causa `micro`); un bombo no;
- un corte con la caja la borra en su celda y en las de su anfiteatro (causa `corte`); lo que hace un incendio en cada paso (`bajar_ocupacion`) la borra (causa `catastrofe`);
- escalones 2 y 5 en la misma celda: bajar a 4 borra solo la de 5;
- la pasada de seguridad; cada borrado en su causa; la línea `BORRADO`; `Version26` de solo lectura.

### Decisiones tomadas en la fase 26

| Pregunta | Decisión |
|---|---|
| ¿Una inclusión de escalón 0 en una celda que luego se construyó? | La sigue borrando cualquier golpe de erosión que alcance la celda: no tiene escalón que la proteja |
| ¿La causa de un golpe de la caja? | `corte`, también por lo que bajan sus anillos antes de cortar |
| ¿La causa del accidente que provoca un onset? | `catastrofe`; el escalón que baja el propio onset, `micro` |

---

## FASE 27 · Clasificación al enterrar

```python
exec(open('C:/Users/DareDave/Downloads/est/fase27_clasificacion.py').read())
```

### Qué hace

En `end_cycle`, antes de hornear:

1. **Recuento.** Se cuentan las inclusiones supervivientes del mundo que se entierra (las escisiones de la fase 29 no cuentan).
2. **Banda.** Con al menos `Minhuellas` (1), la concha es **estrato humano**; si no, **concha limpia**, aunque haya habido gente todo el día (todas sus huellas se borraron, o no llegan al mínimo).
3. **El recuento se hornea en el material.** Cada loseta nueva guarda cuántas inclusiones sobrevivieron en su celda y sus semillas (sus colores). El shader de las conchas (familia mineral) las dibuja como motas de la paleta humana en la cara y los flancos de esa loseta, con una cobertura que crece con el número de inclusiones, `Inclusionesmax × (1 − e^(−n/3))`: 23 % con una, 51 % con tres, 79 % con doce, y nunca más de `Inclusionesmax` (0,8). El grosor de la concha no cambia (sigue siendo el de su ciclo, fase 8). En una concha limpia no se dibuja ninguna.
4. **Colapso como marca de cierre.** La concha guarda `cierre` (el motivo del fin de ciclo) y `colapso`, que es «sí» cuando la fase 23 cerró el ciclo con el motivo `colapso` (P8). Se combina con humana o limpia. `estancado` no es colapso.
5. **`Umbralpresencia` desaparece:** no existe en el repositorio; si existe en el proyecto local, el script lo quita y lo dice en el informe.

Las inclusiones del mundo enterrado se vacían; lo heredado (fase 8) empieza sin inclusiones.

**Cómo viaja al shader.** El alfa de cada instancia de `estratos` ya llevaba la rugosidad (fase 15); ahora lleva `rugosidad + 2 × cobertura en veinteavos` (como las ventanas de la fase 17: «alfa = rugosidad + 2 × nivel»). Las motas van fijas al planeta (una rejilla en su espacio, 36 por unidad), cada una con un color de la tabla `HUMANA` del shader, que son ocho muestras de `paleta_humana` del motor (la autoprueba comprueba que coinciden). La tapa de la loseta de arriba lleva las mismas motas. Con `Materialrespaldo` (Phong) no hay motas.

Campos nuevos de cada entrada de `W['shells']`: `huellas`, `banda` (`humana` o `limpia`), `colapso`, `cierre`, `incl` (`{celda: [semillas]}`) y `escisiones` (los ids de las que cruzaban ese mundo). Una concha sin estos campos (de antes de la fase 27) se lee como limpia, sin colapso. La tabla `ciclos` gana `huellas` y `banda` (`humana`, `limpia`, `humana + colapso`…).

### Parámetros (página Fase27)

`Minhuellas` 1 · `Inclusionesmax` 0,8 (80 %)

### Leyenda

```
BANDA    ultima: estrato humano 12 huellas (min 1)   cobertura 51% (max 80%)   colapso no   humanas 3 de 11
BANDA    ultima: concha limpia 0 huellas (min 1)   cobertura 0% (max 80%)   colapso si   humanas 3 de 12
```

La cobertura es la de la loseta más cubierta de la última concha.

### Probar

Deja tres inclusiones (`Probllegada` 1 y `Simponer` en tres casillas) y `Forzarciclo`: la concha nueva sale con motas de color en esas tres celdas; un corte con la caja las enseña en la pared. Borra todas antes de `Forzarciclo` (o no dejes ninguna): concha limpia. Con `Colapsoon` y `Simbalance` (fase 23) por encima de 1 durante `Maxerosion`: la concha sale con la marca de colapso.

### Autoprueba

- 3 supervivientes y `Minhuellas` 1: humana con 3, y cada loseta guarda las de su celda; el mundo enterrado queda sin inclusiones; 0 supervivientes con 40 llegadas borradas: limpia; `Minhuellas` 5 con 3: limpia y sin motas;
- la cobertura crece con el número y no pasa de `Inclusionesmax` (1000 en una celda: 80 %; con 0,3: 30 %); el grosor es el mismo con 0 y con 1000;
- el alfa de la loseta y de su tapa lleva la cobertura (más con 3 que con 1; nada sin inclusiones), y la conserva bajo la concha siguiente; la tabla del shader es la del motor;
- una escisión abierta no cuenta en el recuento;
- un cierre por `colapso` marca la concha y se combina con humana y con limpia; por `estancado`, no; con `Colapsoon`, la erosión dominante sostenida entierra una concha con la marca;
- `Umbralpresencia`, ni en la página ni en el motor; un mundo de antes de la fase 27 carga y sus conchas se leen como limpias;
- la tabla `ciclos` y la línea `BANDA`.

`xvfb-run -a python3 pruebas/glsl_piel.py` compila el shader con las motas.

### Decisiones tomadas en la fase 27

| Pregunta | Decisión |
|---|---|
| ¿Qué curva sigue la cobertura? | `Inclusionesmax × (1 − e^(−n/3))`, en veinteavos (lo que cabe en el alfa); con al menos una inclusión, al menos un veinteavo |
| ¿Motas en una concha limpia que tenía supervivientes bajo el mínimo? | No se dibujan (es limpia), pero la concha las guarda |
| ¿Los colores de cada inclusión? | La concha guarda la semilla de cada una; el shader reparte los ocho colores de la paleta entre las motas de la loseta (no una mota por inclusión) |

---

## FASE 28 · Noche de enterramiento

```python
exec(open('C:/Users/DareDave/Downloads/est/fase28_noche.py').read())
```

### Qué hace

En cada enterramiento, con colapso o sin él, durante `Noche` segundos la esfera se apaga: solo emiten las inclusiones supervivientes recién horneadas (las motas de la concha nueva) y, cuando exista la fase 29, las paredes de las escisiones. Empieza en el mismo fotograma del recuento (fase 27) y vuelve en 0,4 s. Mientras tanto la sala está a oscuras (fase 23, la misma `Noche`; P9). El mundo nuevo sigue funcionando: lo que nace durante la noche se dibuja apagado. Un segundo entierro durante la noche la reinicia. `Modoactuacion` no la quita: es parte del mundo. Con `Noche` 0 no hay noche.

**Cómo** (sin luces nuevas ni geometría nueva): un valor `noche` (0–1) que sale del motor (`noche_nivel`) y llega:

- al shader de la piel y de las conchas como uniforme `uNoche`: todo se multiplica por 1 − `noche`, y las motas de las losetas recién horneadas suben su emisivo. Esas losetas se marcan en su alfa (+100) solo mientras dura la noche;
- a las luces: el **color** de `luz_principal` (que ya da el motor, `luz_tiempo`), de `luz_relleno` (una expresión: su valor × `dia()`) y el dimmer de `luz_destello` (que ya sale de `frame_u`) se multiplican por 1 − `noche`. Lo que dibuja con Phong se apaga con ellas;
- a las capas de luz y a las partículas (`luz_celda`, `luz_conchas`, `luz_local`, `particulas`, `humo`, `vagones`, `diagnostico`): el color de sus instancias, por 1 − `noche`; a oscuras del todo, las partículas y el humo no se dibujan.

Nada se recompila ni sale del render: solo cambian uniformes, una expresión y colores de instancia.

### Parámetros

Ninguno nuevo: usa `Noche` (4 s), que crea la fase 23. La página Fase28 lleva solo `Version28` (P10).

### Leyenda

```
NOCHE    4.0 s   quedan 2.3   emiten 12 inclusiones y 1 escision
```

### Probar

Con inclusiones vivas (`Probllegada` 1 y `Simponer`), `Forzarciclo`: el planeta se apaga 4 s y solo brillan las motas de la concha nueva. Sin inclusiones: 4 s de oscuridad.

### Autoprueba

- `noche` vale 1 desde el fotograma del recuento hasta `Noche` s y 0 después; coincide con la oscuridad de sala de la fase 23;
- durante la noche: `uNoche` 1, las capas de luz a 0, las luces a 0, y solo las losetas recién horneadas emiten;
- lo que nace de noche existe y se dibuja apagado; al acabar, la luz vuelve y las losetas dejan de emitir;
- con colapso y sin él dura lo mismo; un segundo entierro la reinicia; sin inclusiones, oscuridad sin nada que emita; `Modoactuacion` no la quita; `Noche` 2 dura 2 s;
- la línea `NOCHE` y `Version28`.

### Decisiones tomadas en la fase 28

| Pregunta | Decisión |
|---|---|
| ¿Dimmers o color de las luces? | El color: los dimmers de `luz_principal` y `luz_relleno` son de las escenas de la fase 18, y una expresión en ellos las rompería. El resultado es el mismo (color × dimmer = 0) |
| ¿Los materiales constantes? | Se apaga el color de sus instancias en el motor, en vez de una expresión en cada material: relanzar una fase anterior rehace esos materiales y perdería la expresión |
| ¿Qué motas emiten? | Solo las de la concha recién enterrada (un estrato humano más viejo, expuesto en un corte, sigue apagado) |
| ¿Las inclusiones que caen durante la noche? | Apagadas, como todo lo que nace de noche |
| ¿La retícula? | No se toca: solo se ve fuera de la actuación (`Showgrid`) |

### Pruebas pendientes en TouchDesigner

Que nada parpadee al entrar en la noche (no debe recompilarse ningún shader), y que el fondo del render sea negro. Si algún material Phong o constante sigue viéndose de noche, dímelo: es una geometría que no pasa por las luces ni por las capas de la lista.

---

## FASE 29 · Fila y escisión colectiva

```python
exec(open('C:/Users/DareDave/Downloads/est/fase29_fila.py').read())
```

### Qué hace

Lo único que el público puede hacer a propósito, y solo entre varios: una fila sostenida abre una **escisión**, un pozo que atraviesa las conchas del planeta y que ya no se cierra.

- **Fila:** `Minfila` personas o más (3) en casillas contiguas (diagonales incluidas), sostenida `Tfila` segundos (5) sobre la ocupación binaria de la fase 24. `Modofila` = `cadena` (cualquier forma contigua, por defecto) o `recta` (todas las casillas en una misma fila, columna o diagonal de la rejilla, seguidas). La fila es una componente conexa de casillas ocupadas; se reconoce de una imagen a la siguiente si comparte alguna casilla con la de antes. Cuenta personas, no casillas. **Puede haber varias filas a la vez en la sala, cada una con su escisión** (P14).
- **Origen:** la casilla de la fila con el `t_ocupada` más antiguo. La escisión se abre en la celda que mira a esa casilla en el instante en que la fila cumple `Tfila`, y esa celda queda fija para esa escisión aunque el planeta gire.
- **Profundidad:** personas × `Conchasporpersona` losetas de la columna de origen, con el núcleo como tope. Si se suman personas mientras la fila aguanta, la misma escisión baja más (la profundidad sigue al máximo de personas visto; si se van, no sube). Esa fila solo abre otra escisión cuando se deshace (menos de `Minfila` personas, o deja de ser recta con `Modofila` recta): entonces la escisión queda `cerrada`. Al enterrar su mundo queda `enterrada` y ya no baja más.
- **Permanencia:** es un hueco. Quita losetas de la columna de origen (como `cut`, con radio 0), vacía la celda y **borra sus inclusiones** (es un corte, P7; causa `escision` en la leyenda `BORRADO`). No cuenta en el tope por mundo de los cortes (`quitadas`), no enciende cicatriz cian, ignora `Colmatacion` en su celda y la concha siguiente la tapiza sin cerrarla. La fase 13 no la llena (no es un lago) y la fase 16 no pone fósiles en ella (no cuenta como corte).
- **Balance:** no pasa por `erosion()` ni por `pulso()`: no es erosión ni creación para la fase 23.
- **Aspecto (fulgurita):** una pieza por concha atravesada, de la superficie al fondo de la escisión, en su propia geometría (`fulguritas`): cuatro paredes exteriores de arena fundida (granuladas y mates), cuatro láminas de vidrio por dentro (rugosidad 0,07; dejan pasar la luz del núcleo y brillan en el borde) y un núcleo emisivo de la paleta humana, sin el cian de los cortes. En cada concha que cruza se ramifica: dos o tres ramas finas del núcleo hacia las paredes, decididas por el mapa logístico (con la escisión y la concha como semilla). **Las ramas son solo visuales y no quitan material** (P11). Lo que queda bajo el tapiz de una concha posterior no se dibuja, pero se guarda. En la noche de enterramiento (fase 28) el vidrio y el núcleo brillan.

Las filas son del sensor (`_SALA['filas']`, en el módulo); las escisiones son mundo (`W['escisiones']`, con `W['escision_n']`, el correlativo de la exposición, y `W['esc_celdas']`, las celdas con hueco).

### Operadores (en `/project1/FASE1`)

| Operador | Qué es |
|---|---|
| `escisiones` | Table DAT, como `ciclos`: `id`, `jornada`, `ciclo`, `hora`, `personas`, `conchas` (cruzadas), `celda`, `estado` (abierta, cerrada, enterrada), `testigo`. Las últimas 200 |
| `i_fulguritas`, `fulguritas` | Script CHOP y Geometry COMP instanciado (cajas), con `mat_piel_vidrio` (familia `vidrio` del shader de la piel: el alfa lleva rugosidad + 2 × parte, 0 pared, 1 vidrio, 2 núcleo) |

### Parámetros (página Fase29)

`Minfila` 3 · `Tfila` 5 s · `Modofila` cadena · `Conchasporpersona` 1 · `Simsumar` (añade una persona contigua a la fila simulada)

### Leyenda

```
FILA     4 personas   cadena   5.0/5.0 s
ESCISION #3   celda 40   conchas 4/12   abierta   (sin abrir: fila 2.1/5.0 s)
```

`conchas 4/12`: las que cruza, de las que tiene el planeta. Entre paréntesis, la fila que todavía no ha cumplido `Tfila`.

### Probar sin cámara

Con varias conchas (`Forzarciclo` unas cuantas veces): `Fuente` = simulada, `Simfila` 3 y `Simformarfila` (fase 24). A los 5 s se abre un pozo de 3 conchas con su fulgurita en la celda que miraba la casilla más antigua. `Simsumar`: baja una más. `Simvaciar` y otra fila: otra escisión. `Forzarciclo`: el pozo queda tapizado y sigue abierto.

### Autoprueba

- `es_recta`; 3 personas en cadena en L durante `Tfila`: escisión; con `Modofila` recta, no; en línea, sí;
- 2 personas: no hay fila; una fila que se rompe a `Tfila` − 0,1 s: nada, y al rehacerse empieza de cero;
- el origen es la casilla ocupada desde hace más tiempo, y la celda no cambia al girar el planeta;
- 3 personas quitan 3 losetas y vacían la celda; 2 más mientras aguanta: 5, la misma escisión; si se van, no sube; con 4 losetas y 6 personas, se para en el núcleo; `Conchasporpersona` 2;
- el balance, `ero_resto`, `quitadas` y las cicatrices no cambian; las inclusiones de la celda se borran (causa `escision`);
- la fila se deshace y se forma otra: escisión nueva; dos filas a la vez: dos escisiones;
- la concha siguiente la tapiza sin cerrarla, también con `Colmatacion` 1 (un corte normal sí se rellena); no cuenta como corte ni como lago;
- la fulgurita: por concha, 4 paredes, 4 vidrios, un núcleo y 2 o 3 ramas, entre el fondo y el borde del hueco; ninguna pieza cian; las ramas no quitan losetas; bajo el tapiz no se dibuja; `i_fulguritas` en el render;
- `Simformarfila` y `Simsumar` por la sala simulada, la tabla `escisiones`, las líneas `FILA` y `ESCISION`, y la escisión enterrada con su mundo.

`xvfb-run -a python3 pruebas/glsl_piel.py` compila el shader con la familia vidrio.

### Decisiones tomadas en la fase 29

| Pregunta | Decisión |
|---|---|
| ¿Cuántas piezas de fulgurita se ven tras un entierro? | Las conchas atravesadas, en proporción a lo que queda del hueco a la vista (el tapiz tapa las de abajo) |
| ¿Cuándo deja de bajar una escisión? | Al deshacerse la fila o al enterrar su mundo; una fila que sigue en pie tras el entierro no abre otra hasta deshacerse |
| ¿Dos filas que se juntan? | La componente nueva hereda la primera fila que comparte casilla; la otra se da por deshecha y su escisión se cierra |
| ¿La jornada y la hora? | La fecha y la hora del sistema al abrirse (P13), hasta que D5 defina la jornada |
| ¿El lago? | Se comprueba la regla en el código; con un río de verdad acabando en la escisión, en TouchDesigner |

### Pruebas pendientes

Que la escisión se lea desde la cámara de globo (un pozo de una celda de ancho: la noche y el núcleo emisivo ayudan); `Tfila` y `Minfila` en sala; un río que acabe en una escisión (no debe llenarla).

---

## FASE 30 · Relámpago

```python
exec(open('C:/Users/DareDave/Downloads/est/fase30_relampago.py').read())
```

### Qué hace

Al abrirse una escisión, un único destello blanco por DMX. Profundizarla no da otro. Pasa por el limitador común de la fase 23 (como mucho 3 destellos en cualquier ventana de 1 s, junto con el estroboscopio). **Si el limitador está lleno, el relámpago espera al primer hueco y el estroboscopio cede ese destello** (P12). Solo blanco. El micrófono descarta su clic, como el de cualquier destello. En pantalla, la fulgurita recién abierta sube su emisivo un instante (× 3,5, y vuelve en 0,35 s).

**DMX.** El relámpago enciende el canal `estrobo` de `dmx_canales`, como todos los destellos de la sala. Si va a un foco propio, añade una fila con la función `relampago`: solo se enciende con él. Sin interfaz DMX, el evento queda en el motor y en la leyenda.

### Parámetros

Ninguno nuevo. La página Fase30 lleva solo `Version30` (P10).

### Leyenda

```
RELAMPAGO hace 3.2 s   destellos 2/3 en el ultimo segundo   dmx artnet
RELAMPAGO pendiente (espera un hueco)   destellos 3/3 en el ultimo segundo   sin dmx
```

### Probar

Formar una fila (`Simfila` 3, `Simformarfila`): a los 5 s la leyenda dice `RELAMPAGO hace 0.0 s`. Con `Simbalance` 10 (el estroboscopio a tope) abrir una escisión: el contador nunca pasa de 3 y el relámpago sale.

### Autoprueba

- una escisión, un destello, en el fotograma en que se abre; profundizarla no da otro; otra escisión, otro relámpago; el destello es blanco;
- con 3 destellos del estroboscopio en el último segundo, el relámpago queda pendiente y nunca hay 4 en una ventana de 1 s; en el hueco siguiente sale el relámpago, uno solo, y el estroboscopio cede el suyo; mientras espera, la leyenda dice `pendiente`;
- la fulgurita recién abierta sube su emisivo y vuelve (antes de la fase 30, no);
- por DMX: el canal `estrobo` y la fila `relampago` (que el estroboscopio no enciende); el micrófono descarta su clic;
- `Simformarfila` por la sala simulada, la línea `RELAMPAGO` y `Version30`.

### Decisiones tomadas en la fase 30

| Pregunta | Decisión |
|---|---|
| ¿Dos escisiones a la vez con el limitador lleno? | Un solo relámpago pendiente: los dos comparten el destello |
| ¿El emisivo de la fulgurita espera al destello? | No: sube al abrirse la escisión, aunque el destello de sala espere su hueco |

---

## FASE 31 · Escisiones en el histórico

```python
exec(open('C:/Users/DareDave/Downloads/est/fase31_historico.py').read())
```

### Qué hace

- **Disparo de testigo:** cada escisión exporta una imagen cuando la fila se deshace o cuando se entierra el mundo, lo que ocurra antes, con su profundidad final. Una sola vez (la escisión guarda el nombre del fichero en `testigo`).
- **Sección por el origen:** un corte del planeta por la celda de origen y dos celdas a cada lado de su anillo, desde la superficie hasta la última concha atravesada. Se dibuja **en Python a partir de las columnas** (numpy, `seccion_escision`): cada loseta es una banda de su color, las bandas humanas con sus motas, y en el hueco la fulgurita (paredes de arena fundida, vidrio, núcleo y ramas, con las mismas semillas que en el planeta). No hace falta un segundo render ni planos de recorte, y se prueba fuera de TouchDesigner. Se guarda con `TOP.save()` en PNG, como mucho un testigo por fotograma. La sección se dibuja en el instante del disparo (antes de que el entierro tapice el hueco) y se guarda en el fotograma siguiente.
- **Columna resumen de la jornada:** una banda por ciclo de la jornada, la más antigua abajo, del color de su concha: las humanas con motas, y una franja oscura arriba si el ciclo cerró por colapso. Cada escisión es una veta de la paleta humana que une las bandas que atravesó (y la de su propio ciclo), con un ancho proporcional a sus personas. Se exporta al cambiar la fecha (la jornada que acaba) y con `Exportartestigo`. La mostrará el proyector del histórico (D5).
- **Registro:** cada escisión, con jornada, ciclo, hora, personas, conchas cruzadas y celda de origen, en la tabla `escisiones` (fase 29) y en `escisiones.csv`, una fila al cerrarse (UTF-8, separador `;` para abrirlo en una hoja en español). Relanzar no duplica filas.
- **Jornada:** la de D5 cuando exista; hasta entonces, **la fecha del sistema al abrirse la escisión** (P13). Desde esta fase cada concha guarda la jornada y el ciclo en que se enterró.

### Operadores y ficheros

| Qué | Dónde |
|---|---|
| `seccion` | Script TOP (640 × 360): la última sección dibujada |
| `columna_jornada` | Script TOP (200 × 720): la columna resumen de hoy |
| `escisiones` | La tabla de la fase 29; su columna `testigo` dice el fichero |
| `escision_<jornada>_c<ciclo>_<id>.png` | La carpeta de `Carpetahistorico` (por defecto, `historico/` junto a los scripts; está en `.gitignore`) |
| `columna_<jornada>.png` | Ídem |
| `escisiones.csv` | Ídem: `id;jornada;ciclo;hora;personas;conchas;celda;estado;testigo` |

### Parámetros (página Fase31)

`Exportartestigo` (la sección de la última escisión, como está ahora, y la columna de hoy) · `Carpetahistorico` (por defecto `C:/Users/DareDave/Downloads/est/historico`)

### Leyenda

```
HISTORICO escisiones hoy 3   ultima #3 J2026-11-11 C14 4 personas 4 conchas celda 40   testigo exportado
```

### Probar

Una fila (`Simfila` 3, `Simformarfila`), espera 5 s y `Simvaciar`: aparece `historico/escision_….png` con el pozo en sección y una línea en `escisiones.csv`. Otra fila y `Forzarciclo` sin deshacerla: se exporta al enterrar, con su profundidad de ese momento.

### Autoprueba

- una escisión abierta no tiene testigo; al deshacerse la fila se dispara; al enterrar después no se repite; una fila que sigue en pie al enterrar dispara al enterrar, con su profundidad de ese momento, y no otra vez al deshacerse;
- la sección tiene tantas bandas como conchas cruzó la escisión más una de superficie, en el orden de la columna, con los colores de la paleta; en el hueco, el núcleo de la paleta humana y la pared de arena; la banda humana, con sus motas; sin el cian de los cortes;
- el testigo se exporta una sola vez; el registro tiene sus siete campos en la tabla y en el fichero; relanzar no duplica filas;
- la columna resumen tiene una banda por ciclo, con su tipo, y una veta por escisión, con anchos en la proporción de sus personas (3 y 6);
- `Exportartestigo`, la línea `HISTORICO` y los dos Script TOP.

La autoprueba escribe en una carpeta temporal y la borra: no toca tu `historico/`.

### Decisiones tomadas en la fase 31

| Pregunta | Decisión |
|---|---|
| ¿Qué celdas enseña la sección? | El origen y dos a cada lado de su anillo (en un polo, sus vecinas) |
| ¿Cuándo se guarda? | La imagen se dibuja en el disparo y se guarda en el fotograma siguiente, una por fotograma (`historico_tick`). El plan decía «el primer fotograma de la noche o uno sin cambios»: guardar un PNG de 640 × 360 es la única parte lenta, y queda fuera del fotograma del entierro |
| ¿Cuándo «cierra la jornada»? | Al cambiar la fecha del sistema, hasta que D5 la defina |
| ¿La clave de una fila del registro? | `id`, `jornada` y `hora`: `Resetmundo` reinicia los ids |

### Pruebas pendientes en TouchDesigner

Que `TOP.save()` del Script TOP escribe el PNG en `Carpetahistorico` (si no puede, la consola dice `AVISO  historico: …` y la escisión queda `sin testigo`); el tiempo que tarda (no debe cortar el fotograma); y D5: la jornada, el testigo diario y el proyector del histórico, que siguen fuera.

---

## Cómo se ha probado (fases 22 a 31)

```
python3 pruebas/correr_fases.py                  # base y fases 3 a 31 desde cero, sesión, relanzar y otra sesión
python3 pruebas/correr_fases.py --hasta=fase29   # solo hasta esa fase
xvfb-run -a python3 pruebas/glsl_piel.py         # el shader de la piel en un OpenGL de verdad (pip install moderngl)
```

- Las fases 22 a 31 dan `AUTOPRUEBA OK` al aplicarse y al relanzarse sobre el proyecto en el nivel 31, y las fases 11 a 21 siguen dando `AUTOPRUEBA OK` relanzadas encima; el mundo se conserva y las sesiones simuladas no dejan expresiones con error ni avisos.
- El shader de la piel compila con las familias `plastico` y `vidrio`, las motas de la paleta humana y `uNoche`.
- **Fallos que ya estaban en `main` y no son de estas fases:** en el simulador, la primera pasada de cada fase da `FALLO  particulas.material: Materialrespaldo` (y `humo`) hasta que la fase 12 crea ese parámetro (y las fases 3 a 10, también al relanzarlas), y `sala_virtual.py` falla cuatro comprobaciones de su esfera (`frente`). Por eso `correr_fases.py` termina con FALLO aunque todas las autopruebas pasen.

Lo que el simulador no comprueba: la imagen real (cómo se ven las inclusiones, las motas, la noche y la fulgurita), los nombres exactos de los parámetros del Orbbec TOP, el Corner Pin TOP, el GLSL TOP y el DMX Out CHOP, la cámara y el DMX de verdad, y el rendimiento.
