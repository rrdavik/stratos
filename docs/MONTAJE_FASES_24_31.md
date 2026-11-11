# Estratos · Montaje
## Fases 24 a 31: la huella inevitable (plan v5)

*Continúa `MONTAJE_FASES_21_23.md`. Referencia: `docs/PLAN_V5.md` (el doc «Estratos · Plan v5: la huella inevitable», decisiones P1 a P14 cerradas el 28 de octubre de 2026). Las reglas de siempre: un script por fase, encima de la anterior, con su versión en la primera línea del informe, su página `FaseNN`, su línea en la leyenda, su `LEEME` y una AUTOPRUEBA al final que deja el mundo como estaba. El motor gana una versión por fase (de la v83 a la v90). Para tenerlo todo al día, `recargar_todo.py`.*

**Antes de nada:** las fases 24 a 31 necesitan la cámara (o su sala simulada) de la fase 22 y la luz de sala de la fase 23. Todo se prueba sin cámara con `Fuente` = simulada (página Fase22). Las autopruebas de todas las fases corren con `Activo` apagado (el sorteo de la fase 22), para probar lo suyo con todas las señales.

| Fase | Script | Qué hace | Motor |
|---|---|---|---|
| 24 | `fase24_personas.py` | Personas: cabezas, seguimiento, casillas ocupadas y la celda que miran | v83 |
| 25 | `fase25_huella.py` | Huella mínima: inclusiones por llegada y por parada, con su escalón | v84 |

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

