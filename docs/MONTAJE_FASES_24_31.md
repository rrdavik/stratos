# Estratos · Montaje
## Fases 24 a 31: la huella inevitable (plan v5)

*Continúa `MONTAJE_FASES_21_23.md`. Referencia: `docs/PLAN_V5.md` (el doc «Estratos · Plan v5: la huella inevitable», decisiones P1 a P14 cerradas el 28 de octubre de 2026). Las reglas de siempre: un script por fase, encima de la anterior, con su versión en la primera línea del informe, su página `FaseNN`, su línea en la leyenda, su `LEEME` y una AUTOPRUEBA al final que deja el mundo como estaba. El motor gana una versión por fase (de la v83 a la v90). Para tenerlo todo al día, `recargar_todo.py`.*

**Antes de nada:** las fases 24 a 31 necesitan la cámara (o su sala simulada) de la fase 22 y la luz de sala de la fase 23. Todo se prueba sin cámara con `Fuente` = simulada (página Fase22). Las autopruebas de todas las fases corren con `Activo` apagado (el sorteo de la fase 22), para probar lo suyo con todas las señales.

| Fase | Script | Qué hace | Motor |
|---|---|---|---|
| 24 | `fase24_personas.py` | Personas: cabezas, seguimiento, casillas ocupadas y la celda que miran | v83 |

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

