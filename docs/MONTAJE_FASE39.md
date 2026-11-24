# Estratos · Montaje
## Fase 39: la especie del mal

*Continúa `MONTAJE_FASE38.md`. La fase 33 dejó el mal provisional: un brote usaba la geometría de su especie de origen bajo un velo casi negro, «hasta que se defina la imaginería». Esta fase pone la imaginería de la lámina «Mal · lámina de una especie nueva»: el mal es una especie con su propia biblioteca, sus emblemas y su demonio. La lógica del juego no cambia (lo comprueba la autoprueba: la misma partida da el mismo resultado con la fase 38 y con la 39).*

| Fase | Script | Qué hace | Motor | Comun |
|---|---|---|---|---|
| 39 | `fase39_mal.py` | La especie del mal: vallas, negocio, ocio y encierro, obra que se enciende, emblemas y demonio | v117 | v87 |
| 39 v2 | `fase39_mal.py` | Con `Oceano` el mal tiene su isla; el coloso a la escala del planeta; los emblemas, al final del render; Trumpzilla solo anda por tierra (`Montierra`) | v118 | v88 |
| 39 v3 | `fase39_mal.py` | La discoteca y sus focos (haces que barren el cielo), el neón de las construcciones finales, los yates en el mar y los demonios grandes un 30 % más pequeños | v120 | v89 |

```python
exec(open('C:/Users/DareDave/Downloads/est/fase39_mal.py').read())
```

**Antes de lanzarla:** copia la carpeta `sprites/` del repositorio dentro de la carpeta de los scripts (`C:/Users/DareDave/Downloads/est/sprites/mal_emblemas.png`). Si falta, el informe dice `FALLO mal_atlas: no encuentro ...`.

También cambian, solo en su autoprueba: `fase12_moduladores.py` v10 y v11 (los remates del mal cuentan desde la fase 39; de noche, las luces a oscuras no son un fallo) y `fase33_monstruo.py` v3 (con la fase 39 prueba el velo provisional con `Especiemal` apagado).

---

## La especie

**El brote es una valla.** Cercar es el primer gesto. Con ocupación 1, la celda del mal es una de tres vallas (la que diga la celda): de obra (paneles de malla sobre pies de hormigón y la señal de prohibido), de torsión (postes, malla, alambre de espino y la placa de «privado») o con cartel (el solar tapiado y una cartelera: «próximamente»).

**La rama se decide al abrir la valla** (la primera vez que pasa de 1) y se queda hasta que vuelve a ser valla o deja de ser del mal:

| Al abrir | Rama |
|---|---|
| `Vecinasencierro` (3) vecinas del mal o más | **encierro**: si crece rodeada por el mal, se cierra |
| la alimenta el SEQ1 (el último secuenciador que la tocó) | **negocio** |
| la alimenta el SEQ2 | **ocio** |

Así, en un clúster, lo de fuera abre comercio y ocio y el encierro crece donde el mal es más denso, tapado por los neones: delante lo que brilla, detrás lo que encierra.

**Los tipos**, con los umbrales de la planificada (con los de fábrica de la fase 4: 1, 2-3, 4-5, 6-7, 8+):

| | 1 | 2-3 | 4-5 | 6-7 | 8+ |
|---|---|---|---|---|---|
| negocio | valla | tienda (toldo, escaparate) | supermercado (escaparate corrido, tótem, coches) | centro comercial (dos alas, atrio en torre, aparcamiento en altura, tótem OFERTA) | gran superficie (nave ciega, banderas, mar de coches, tótem MEGA) |
| ocio | valla | bar (terraza con sombrillas) | sala de fiestas (caja ciega, focos al cielo, la cola) | casino-hotel (marquesina, torre de ventanas rosas, palmeras, fuente rosa) | resort de superlujo (terrazas, torre con helipuerto, yate) |
| encierro | valla | recinto (doble valla, concertina, garita, barrera) | muro (hormigón alrededor de una superficie vacía, una torre) | centro de internamiento (barracones tras el muro, dos torres, portón) | campo (filas de barracones, alambrada, cuatro torres, la puerta) |

Cuerpos casi negros; el neón rosa (el dinero) en los escaparates de la planta baja, una línea en cada forjado y las ventanas de las torres; hormigón y chapa en el encierro. Son diseños de la misma gramática que la ciudad (volúmenes con datos de fachada y remates): la fila 6 de la paleta y cuatro fachadas nuevas en el shader de la ciudad (neón, torre de neón, muro, barracón). Van en **cualquier tema** (naturaleza, ciudad o industria) y **no entran en la piel del público**: ni se dibujan con la especie de origen, ni forman clúster con el público, ni levantan relieve en la naturaleza.

**La obra: terminada = se enciende.** Cada etapa nueva pasa por cuatro pasos, `Pasosobramal` pasos (semicorcheas) cada uno: el cartel «próximamente» sobre la valla; la estructura (forjados y pilares) con su grúa; terminado, aún a oscuras (sin neón, el emblema apagado); la puesta en marcha (el neón titubea y se enciende). Una nota en la celda aviva el neón un momento.

**Los emblemas.** Sobre cada celda flota un sprite con luz propia que mira a la cámara: de lejos se lee el signo, no el edificio.

| | 1 | 2-3 | 4-5 | 6-7 | 8+ |
|---|---|---|---|---|---|
| negocio | prohibido | $ | $ demonio | $ demonio $ | el magnate ($ $ y la sonrisa) |
| ocio | prohibido | copa | $ | $ demonio | diamante |
| encierro | prohibido | candado | ojo | sirena | calavera |

Rosa neón = dinero · rojo = vigilancia y demonios · hueso = la calavera. Desde ocupación 4, uno de cada tres dólares es un demonio. La valla con cartel lleva «próximamente». La calavera, el magnate y el diamante laten despacio.

**El demonio del clúster.** Un clúster del mal (celdas del mal vecinas) de 4 celdas o más invoca a su demonio: de 4 a 6, un **diablillo** sentado en la pieza más alta; de 7 a 9, una **cabeza** que asoma detrás del clúster; de 10 en adelante, el **coloso**, que abraza el clúster con la calavera en el pecho. Los dos grandes se apartan de la cámara para quedar detrás de los edificios. v2: como mucho un cuarto (la cabeza) o un tercio (el coloso) del radio del planeta; en la v1 crecían con el clúster y se salían del planeta.

**Con `Oceano` (v2).** Cada celda del mal es una isla llana, sin montes ni islotes (dos del mal vecinas se unen por un istmo), y sus edificios se apoyan en la meseta. En la v1 las celdas del mal salían del relieve entero: se quedaban a ras del mar, que flota sobre las losetas, y lo tapaba; solo se veían los emblemas, flotando sobre el agua.

**Trumpzilla solo anda por tierra (v2, `Montierra`).** Con `Oceano`, el monstruo no entra en el mar: una celda vacía cuyo terreno (suelo y relieve en su centro) queda a ras del nivel del mar, ni en una hondonada inundada. Lo construido es isla (también los brotes del mal) y las zanjas del juego siguen siendo su trampa. Aparece en una celda vacía de tierra; si todo lo vacío es mar, en una isla de la cara visible. Si entre su isla y la presa solo hay mar, se queda quieto: el público puede cortarle el paso no construyendo puentes. Sin `Oceano`, o en la ciudad y la industria, todo es tierra. **Motor v131:** una celda de mar por la que pasa una carretera de la ciudad o una vía del tren de la industria (las que se dibujan) cuenta como tierra: es su puente entre tierras. La misma regla vale para Godzilla (fase 40 v3).

**El rescate** (fase 35). Mientras dura, el neón parpadea y se apaga y el emblema se debilita; al completarse, la valla cae (1,2 s) y la celda vuelve a ser del público con la especie del último secuenciador.

### Operadores nuevos (en /project1/FASE1)

| Operador | Tipo | Qué es |
|---|---|---|
| `emblemas_mal`, `i_emblemas_mal` | Geometry COMP + Script CHOP | Una lámina (Rectangle SOP 1 × 1) instanciada: los emblemas y los demonios. Comun v88: lo último del render (son neón opaco; las capas aditivas, dibujadas encima, podían lavarlos) |
| `mat_emblema` | GLSL MAT | `emblema_vertex` y `emblema_pixel`; sampler `sAtlas`; uniformes `uEmblema` (reloj `sprite_t` de `frame_u`, pixelado, columnas y filas) y `uEmblemaInc` (`Inclinasprite`, `Brilloemblema`). Opaco, recortado por alfa, escribe profundidad, sin culling. Luz propia: la noche no lo apaga |
| `mal_atlas` | Movie File In TOP | `sprites/mal_emblemas.png` |
| `emblema_vertex`, `emblema_pixel` | Text DAT | Los shaders |
| `modelos/edi_<diseño>_<v>` y `mod_edi_...` | Script SOP + Geometry COMP | Los 15 diseños del mal (3 vallas y 12 tipos) × variantes, con el shader de la ciudad |
| `modelos/ciu_<remate>` y `mod_ciu_...` | SOP + Geometry COMP | Los remates: caja, cartelera, tótem, farola, coche, bandera, sombrilla, foco, palmera, fuente, helipuerto, yate, concertina, torre de vigía y portón |

En cada fila de `emblemas_mal`, el alfa lleva `emblema + 32 × modo` (0 fijo, 1 parpadeo, 2 detrás, 3 late); r, la luz (1 encendido, 0,14 a oscuras); sx el ancho, sy el alto, sz lo que se aparta de la cámara (detrás). El orden de los emblemas es el de `EMBLEMAS_MAL` del motor.

### El atlas

`sprites/mal_emblemas.png`: 1024 × 512, 4 × 4 celdas de 256 × 128 (2:1: cabe «$ demonio $» en fila), fondo transparente y recorte duro. Lo dibuja `sprites/hacer_atlas_mal.py` con Pillow (tubos de neón: color, alma clara y borde oscuro); `sprites/mal_emblemas_lamina.png` es la hoja de prueba con los nombres y cada emblema a 20 px.

```
python3 sprites/hacer_atlas_mal.py
```

Para añadir emblemas: el dibujo y el nombre en `EMBLEMAS` del script y en `EMBLEMAS_MAL` del motor (mismo orden), y su sitio en `EMBLEMA_DE`.

### Parámetros (página Fase39; Montierra, desde la fase 39 v4, en la página Monstruos)

| Parámetro | Defecto | Qué hace |
|---|---|---|
| `Especiemal` | encendido | El mal con su especie; apagado, el velo provisional de la fase 33 |
| `Vecinasencierro` | 3 | Vecinas del mal que cierran una valla al abrir (encierro) |
| `Pasosobramal` | 8 | Pasos (semicorcheas) por paso de obra: cartel, estructura, a oscuras, encendida |
| `Tamanoemblema` | 0,35 | Alto del emblema, en celdas (crece un poco con la etapa). v2: de 0,45 a 0,35; un proyecto con 0,45 pasa a 0,35 una sola vez |
| `Brilloemblema` | 1 | Multiplica la luz propia de los emblemas |
| `Altomal` | 1,5 | Alto de los edificios del mal, por la altura de planta de la ciudad |
| `Demoniomal` | encendido | El demonio de los clústeres |
| `Montierra` | encendido | (v2) Con `Oceano`, el monstruo solo anda por tierra |
| `Simmal` | pulso | Un clúster de diez celdas alrededor de `Simceldamon`, sembrado de fuera adentro, en obra |

**Leyenda.** `MAL      negocio 3  ocio 3  encierro 2  vallas 2   obras 1   demonio coloso (10 celdas)` (con un rescate en curso, `rescate 40%`).

---

## La noche del mal (v3, motor v120)

**La discoteca.** Una sala de fiestas más (ocio, etapa 3, la que diga la celda): caja negra con la cornisa de neón, un tambor de neón encima, la entrada con su marquesina y la cola, y **seis focos** en la cubierta. Encendida, cada foco lanza un **haz de luz** que barre el cielo (de colores: rosa, cian, violeta y blanco), con un halo tenue y la lámpara; los focos de la sala de fiestas y del casino también. Los haces van en la **luz local** (`luz_local`, la geometría aditiva de la fase 18): no son luces de verdad y no cuestan nada a la escena.

**El neón de lo terminado.** Las construcciones finales encendidas (etapa 4: centro comercial, casino-hotel, centro de internamiento; etapa 5: gran superficie, resort, campo) llevan tubos de neón en el contorno de la cubierta de cada volumen; la etapa 5, también en las aristas y en un forjado de cada dos. Del color de su rama (negocio rosa y oro; ocio rosa, cian y violeta; encierro rojo) y titubean un poco. En obra, a oscuras o durante el rescate (el neón apagado), no.

**Los yates.** Con `Oceano`, el casino trae un yate, el resort dos y la gran superficie del magnate uno: fondeados en las celdas de mar vecinas de su isla (vacías y a ras del nivel del mar), se mecen con el oleaje y llevan neón en la borda y en la cabina (luz local). En cualquier tema.

**Los demonios, más pequeños.** La cabeza, como mucho un sexto del radio del planeta (antes un cuarto); el coloso, un cuarto (antes un tercio); los dos crecen un 30 % menos con el clúster. El diablillo no cambia.

**Leyenda.** Con neón o yates, al final: `neon 92  yates 2`.

## Prueba manual

1. `Modojuego`. `Simmal`: diez celdas alrededor de `Simceldamon`. Por fuera, vallas, negocio y ocio; en el centro, encierro. Todas en obra: cartel «próximamente», grúas, terminadas a oscuras y, al final, el neón se enciende titubeando. Detrás, el coloso.
2. Siembra con el SEQ1 una celda vacía junto a un brote suelto: el brote abre negocio; con el SEQ2, ocio.
3. Naturaleza con `Oceano`: `Simmal` levanta el clúster sobre sus islas, con los edificios encima del mar. `Simmonstruo` en una isla separada por mar de lo construido: no se mueve; siembra una celda entre las dos y cruza por ella.
4. `Simrescate` sobre una celda del mal: el neón parpadea, se apaga, la valla cae y la celda vuelve a ser del público.
5. `Especiemal` apagado: vuelve el velo de la fase 33.

## Qué ajustar en sala

- **`Tamanoemblema`** y **`Brilloemblema`**: que el signo se lea desde el público sin tapar los edificios ni deslumbrar junto al planeta.
- **`Altomal`**: más alto si los edificios del mal se pierden como losas oscuras; 1 los deja a la escala de la ciudad.
- **`Pasosobramal`**: con tempos rápidos, más pasos para que la obra se vea.
- **`Vecinasencierro`**: 2 cierra antes (más encierro); 4, casi solo en el centro de los clústeres grandes.

## Pruebas

- `python3 pruebas/correr_fases.py` corre las fases 3 a 39 en el TouchDesigner simulado (la autoprueba de la fase 39: trece comprobaciones (v3: la discoteca con sus seis haces, el neón del resort y ninguno en la discoteca, los yates con y sin `Oceano` y la cabeza a un sexto del radio), la última con `Oceano`: el monstruo no cruza el mar y sí un puente de tierra, y la celda del mal sobre su isla; la lógica, igual que con la 38; presupuesto, unos 0,3 ms por fotograma con diez celdas).
- `xvfb-run -a python3 pruebas/lamina_mal.py` dibuja la lámina con el motor y los shaders de verdad (moderngl: `pip install moderngl`): las vallas, las tres escaleras, la obra, el rescate, un clúster con su coloso y la prueba a distancia (~24 px, ampliado × 4) junto a la ciudad y la industria. Deja `pruebas/lamina_mal.png`.
