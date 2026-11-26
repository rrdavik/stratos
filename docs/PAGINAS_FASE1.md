# FASE1: las paginas de parametros por temas

Desde **comun v104** los parametros de FASE1 ya no van en una pestana por fase (Fase1 ... Fase43,
casi cuarenta) sino en **15 pestanas por temas**, cada una con titulos de seccion.
Los nombres de los parametros no cambian: expresiones, escenas y el motor los leen igual.

## Como se pasa un proyecto de antes

Basta con relanzar cualquier fase (o `recargar_todo.py`): `paginas_al_dia()` pasa cada parametro
a la pestana de su tema **con su valor, su expresion y su modo**, pone los titulos, ordena las
pestanas y quita las FaseN que se quedan vacias. TouchDesigner no mueve parametros de pagina: se
quitan y se crean iguales en la otra; el cambio de `Escena`, `Modocamara`, `Variantes`... al
recrearlos no cuenta como un cambio (no recarga el preset de la escena).

Las versiones de las fases sin parametros (`Version26`, `Version28`, `Version30`) y `Nivel`
(la ultima fase aplicada) estan juntas en la pestana **Versiones**.

El reparto esta en `PAGINAS_TEMAS` (estratos_comun.py): un parametro nuevo se anade alli, en su
tema y seccion; si no esta, se queda en la pagina que pida su fase.

## Planeta

**Giro al tempo**

| Parametro | Que hace |
|---|---|
| `Barsperturn` | Compases por vuelta |
| `Tilt` | Inclinacion del eje |
| `Pausa` | Pausar rotacion |
| `Balanceo` | Balanceo del eje en grados (0 = apagado) |
| `Balanceoper` | Periodo del balanceo (s) |
| `Masterbeat` | CHOP de master_beat (vacio: el pulso lo cuenta el motor) |

**Nucleo y reticula**

| Parametro | Que hace |
|---|---|
| `Radionucleo` | Radio del nucleo (menor: las especies se ven mas grandes) |
| `Showgrid` | Mostrar reticula |
| `Leyenda` | Mostrar leyenda |

## MIDI

**SEQ1**

| Parametro | Que hace |
|---|---|
| `Canal` | Canal MIDI del SEQ1 |
| `Filtrar` | Solo ese canal (SEQ1) |
| `Nota` | Ultima nota SEQ1 (muevela para probar) |
| `Sembrar` | Sembrar en Nota (prueba) |
| `Sembrarzona` | Sembrar Nota y sus vecinas (SEQ1, prueba) |

**SEQ2**

| Parametro | Que hace |
|---|---|
| `Canal2` | Canal MIDI del SEQ2 |
| `Filtrar2` | Solo ese canal (SEQ2) |
| `Nota2` | Ultima nota SEQ2 (muevela para probar) |
| `Sembrar2` | Sembrar SEQ2 en Nota2 (prueba) |
| `Sembrarzona2` | Sembrar Nota2 y sus vecinas (SEQ2, prueba) |

**Notas de la reticula**

| Parametro | Que hace |
|---|---|
| `Notapolosur` | Polo sur: nota MIDI (24 do1 - 106) |
| `Notapolonorte` | Polo norte: nota MIDI (26 - 108 do8) |
| `Fuerarango` | Notas fuera del rango |

**Velocidad y gate**

| Parametro | Que hace |
|---|---|
| `Umbralvel` | Velocidad: pulido a partir de |
| `Velprueba` | Velocidad de prueba |
| `Velref` | Velocidad a la que vale la tabla (0 = la velocidad no cuenta) |
| `Gateprueba` | Gate de los botones de prueba (pasos) |

**Bateria**

| Parametro | Que hace |
|---|---|
| `Canaldrum` | Canal MIDI de la bateria |
| `Notabase` | Nota del pad 1 |
| `Padprueba` | Pad de prueba |
| `Erosionar` | Erosionar con el pad de prueba |

## Crecimiento

**Formaciones**

| Parametro | Que hace |
|---|---|
| `Alturafactor` | Limite de altura (x grosor) |
| `Semillafrac` | Altura de la semilla (x limite) |
| `Costemax` | Notas por trigger en el limite |
| `Gatemax` | Gate ligado: crecimiento max. (x; 1 = el gate no cuenta) |
| `Umbralram` | Ramificacion desde (ocupacion) |
| `Pasoumbral` | Ocupaciones entre ramificacion, fusion, corona y cumbre |
| `Tramoscumbre` | Tramos de cumbre (25 % cada uno) |
| `Satelite` | Satelite: tamano y altura max. (x la madre) |

**Velocidad y gate: material y vigor**

| Parametro | Que hace |
|---|---|
| `Materialmodo` | Velocidad -> material |
| `Rugmin` | Rugosidad a velocidad 127 (pulido) |
| `Rugmax` | Rugosidad a velocidad 0 (rugoso) |
| `Vigormax` | Vigor maximo (gate ligado, naturaleza) |
| `Plantasligado` | Plantas por gate ligado (ciudad) |

**Especies y mezcla**

| Parametro | Que hace |
|---|---|
| `Tema` | Tema |
| `Temaenciclo` | Un cambio de Tema espera al fin de ciclo |
| `Topeconstruido` | Tope de construido (fraccion ocupada que es el 100 %) |
| `Madurezmezcla` | Umbral de madurez (% construido: se acaban las cuotas) |
| `Simconstruido` | Simular construido (%; -1 el real; desde Madurezmezcla, madura) |
| `Suelofirme` | Suelo firme (ciudad e industria, donde hubo naturaleza o hay concha) |
| `Valvula` | Valvula de fundacion (puntos de deficit para otra mancha) |
| `Paciencia` | Paciencia de fundacion (celdas nuevas con suelo firme) |
| `Ordenfamilias` | Orden de familias |
| `Precarga` | Precarga (puntos antes del umbral) |
| `Cargaporfotograma` | Carga por fotograma (geometrias) |
| `Herenciareparto` | Lo heredado cuenta en el reparto de especies |

**Clusters y compuestos**

| Parametro | Que hace |
|---|---|
| `Pesovecina` | Peso de las vecinas en la presion |
| `Umbralvecindad` | Presion para fundirse (cluster) |
| `Mincluster` | Celdas minimas de un cluster |
| `Caos` | Mapa logistico: r (compuestos) |
| `Maxpiezas` | Piezas maximas por compuesto |
| `Mutacion` | Mutacion (hasta donde llegan las formas mutantes) |
| `Mutacionfuente` | La mutacion la lleva |

**Obras**

| Parametro | Que hace |
|---|---|
| `Avance` | Las obras avanzan |
| `Pasosetapa` | Pasos por etapa (y al deshacerse) |
| `Obra` | La obra se ve entre etapas |

**Mundo**

| Parametro | Que hace |
|---|---|
| `Resetmundo` | Vaciar el mundo |

## Ciclo

**Fin de ciclo**

| Parametro | Que hace |
|---|---|
| `Umbralmadurez` | Madurez minima para enterrar |
| `Umbralnovedad` | Novedad maxima de un compas quieto |
| `Compasesquietos` | Compases quietos para enterrar |
| `Ciclomin` | Duracion minima (compases) |
| `Ciclomax` | Edad maxima (si el territorio esta lleno) |
| `Umbralterritorio` | Territorio ocupado para la edad maxima |
| `Cambioentierra` | Cambio de pattern entierra el mundo |
| `Giromin` | Factor de giro minimo (1 = el giro no se frena) |
| `Forzarciclo` | Terminar el ciclo ahora |

**Conchas**

| Parametro | Que hace |
|---|---|
| `Shellthick` | Grosor de concha |
| `Maxconchas` | Losetas visibles por columna |
| `Grosortiempo` | Grosor proporcional al ciclo |
| `Grosormax` | Grosor maximo de concha (0: sin limite) |
| `Cortezamax` | Corteza maxima: compacta las conchas viejas (0: el radio es el tiempo) |
| `Colmatacion` | Relleno de las hondonadas al enterrar |
| `Tierra` | Las conchas, como capas de tierra (0: losetas de color) |

**Paleta de las conchas**

| Parametro | Que hace |
|---|---|
| `Paleta` | Paleta de las conchas |
| `Paletatono` | Tono de la primera concha (grados) |
| `Paletacroma` | Saturacion de las conchas |
| `Paletaluz` | Luminosidad de las conchas (la tapa, 0,8 x) |
| `Tapaneutra` | Tapa de las losetas hacia el gris (0: como los flancos) |

**Herencia entre ciclos**

| Parametro | Que hace |
|---|---|
| `Herencia` | Herencia entre conchas |
| `Rebrote` | Lo heredado en naturaleza brota de un banco de semillas |

## Erosion

**Erosion de la bateria**

| Parametro | Que hace |
|---|---|
| `Objetivo` | Donde cae la erosion |
| `Umbraldensidad` | Presupuesto de densidad (1 = sin presupuesto) |
| `Pumpamt` | Fuerza del pumping de bombo y toms (0 = sin pumping) |
| `Pumphorz` | Anchura del pumping |
| `Pumptope` | Altura maxima con pumping (x limite) |

**Cicatriz**

| Parametro | Que hace |
|---|---|
| `Cicatriz` | Duracion de la cicatriz (s) |
| `Destello` | Intensidad del destello |

**Escalada y catastrofes**

| Parametro | Que hace |
|---|---|
| `Ventanaescalada` | Pasos en que se suman los golpes de una zona |
| `Golpesescalada` | Golpes en la misma zona para la catastrofe |
| `Pasosfuego` | Pasos que arde (o se derrumba) cada celda |
| `Maxfuego` | Celdas que arden (o se derrumban) a la vez |
| `Pasospolvo` | Pasos en que se disipa el polvo |
| `Apagon` | Industria: la escalada de la energia es un apagon en cadena |
| `Grisu` | Industria: la escalada de la mina es una explosion de grisu |
| `Escalar` | Escalada de prueba: Golpesescalada aranazos con Padprueba |

**Cortes**

| Parametro | Que hace |
|---|---|
| `Detalleexpuesto` | Piezas expuestas por celda del corte |
| `Unircortes` | Dos cortes vecinos seguidos se unen (canon o galeria) |
| `Unirprueba` | Dos cortes vecinos seguidos alrededor de Nota |

## Naturaleza

**Relieve**

| Parametro | Que hace |
|---|---|
| `Umbralmonte` | Ocupacion desde la que sube el terreno (monte) |
| `Limitebosque` | Limite del bosque (altura relativa) |
| `Limitenieve` | Limite de la nieve (altura relativa) |
| `Alturamonte` | Crecimiento maximo del suelo (x el limite) |
| `Oceano` | Oceano: las celdas vacias son mar; las ocupadas, islas |
| `Volcanes` | Volcanes: parte de los conos de relieve que lo son |
| `Inundacion` | Lo que sube el agua de una hondonada (por segundo; 0: no se desborda) |

**Bosque**

| Parametro | Que hace |
|---|---|
| `Biomas` | Biomas por latitud (frio, templado, calido) |
| `Variantes` | Variantes por modelo (biblioteca) |
| `Traslucidez` | Traslucidez del borde de la copa |
| `Timidez` | Timidez de copa (hueco entre copas) |
| `Emergentes` | Fraccion de emergentes del bosque |
| `Orla` | Orla de matorral en el borde del bosque |
| `Mezcla` | Ejemplares del otro modelo del bioma |
| `Swaymax` | Balanceo maximo del dosel (grados) |

**Bancales, mesetas y frutales**

| Parametro | Que hace |
|---|---|
| `Terrazaspornota` | Bancales por nota del SEQ1 (arrozal) |
| `Maxterrazas` | Bancales maximos |
| `Pasoterraza` | Alto de un bancal (x el limite) |
| `Riego` | Los bancales junto a un rio se inundan |
| `Colorcultivo` | Verde arroz de los bancales |
| `Alturameseta` | Alto de un nivel de meseta (x el limite) |
| `Maxniveles` | Niveles maximos de la meseta |
| `Marco` | Marco de los frutales |
| `Setos` | Setos entre las parcelas de la meseta |

**Rios y lagos**

| Parametro | Que hace |
|---|---|
| `Rios` | Rios (naturaleza) |
| `Maxrio` | Longitud maxima de un rio (celdas) |
| `Colorrio` | Color de los rios (azul reservado) |
| `Anchorio` | Ancho minimo de un rio (el maximo, 3,4 x) |
| `Anchominpx` | Ancho minimo del rio en pantalla (px, camara de globo) |
| `Emisivorio` | Emisivo del agua (cara de sombra) |
| `Lagos` | Lagos en las hondonadas |
| `Pruebario` | Cordillera de prueba y su rio (en Nota2) |

**Pradera y detalle**

| Parametro | Que hace |
|---|---|
| `Pradera` | Pradera: matas que reparte la tarjeta grafica (0: sin pradera) |
| `Mata` | Tamano de una mata de la pradera |
| `Detalle` | Detalle alto: hojas de verdad desde el globo (tarjeta grafica) |
| `Ligero` | Naturaleza ligera (maquina modesta) |
| `Impostores` | De lejos, tarjetas de racimo |
| `Lodnat` | Detalle de la naturaleza desde (px por celda) |
| `Tintebordenat` | Tinte del secuenciador en el borde (fresnel) |

## Ciudad

**Ciudad**

| Parametro | Que hace |
|---|---|
| `Lenguaje` | Lenguaje de la ciudad |
| `Variantesciudad` | Variantes por diseno (biblioteca de la ciudad) |
| `Fijartipo` | Fijar el diseno (para probar) |
| `Oblicuidad` | Oblicuidad de los anadidos informales (grados) |
| `Alturaplanta` | Alto de una planta (x el limite) |
| `Anchovano` | Ancho de un vano (x el limite) |
| `Retranqueo` | Retranqueo de las torres |
| `Torsionmax` | Giro maximo de la torsionada (grados) |
| `Parasitospornota` | Parasitos por nota del SEQ1 (colonia) |
| `Maxparasitos` | Parasitos maximos |
| `Modulomarco` | Modulo del marco (x la celda) |
| `Maxmarco` | Niveles maximos del marco |
| `Capsulas` | Huecos del marco con capsula |
| `Desfasefachada` | Plantas de la fachada por detras del esqueleto |
| `Gruas` | Gruas en las obras |
| `Maxgruas` | Gruas a la vez |
| `Tinteventanas` | Una nota enciende las ventanas con el color de su SEQ |
| `Pasostinte` | Pasos que tarda en apagarse ese color |
| `Lodciudad` | Remates pequenos desde (px por celda) |

**Carreteras y trafico**

| Parametro | Que hace |
|---|---|
| `Carreteras` | Carreteras (ciudad) |
| `Minvia` | Ocupacion minima de una formacion suelta con carretera |
| `Grosorvia` | Ancho de las carreteras |
| `Pesotraza` | Preferencia de las carreteras por las trazas heredadas |
| `Trafico` | Puntos de trafico por tramo de carretera |

**Industria**

| Parametro | Que hace |
|---|---|
| `Epoca` | Epoca de la industria |
| `Variantesind` | Variantes por diseno (industria) |
| `Recursos` | La mina saca lo que guarda la concha de abajo |
| `Bancospornota` | Bancos de la corta por nota del SEQ1 |
| `Maxbancos` | Bancos maximos de la corta |
| `Maxbastidor` | Niveles maximos del bastidor (planta integrada) |
| `Emisiones` | Humo y vapor de la industria |
| `Maxhumo` | Particulas de humo maximas |
| `Lodind` | Remates pequenos de la industria desde (px por celda) |
| `Turno` | Industria: el frente es un cambio de turno (ola de focos de sodio) |

**Ferrocarril y red electrica**

| Parametro | Que hace |
|---|---|
| `Vias` | Ferrocarril (industria) |
| `Anchovia` | Ancho del ferrocarril |
| `Red` | Red electrica (industria) |
| `Minred` | Ocupacion minima de una formacion con corriente |
| `Pulsored` | Pulsos por la red, al tempo |
| `Colorred` | Color de la red (violeta reservado) |

**El frente del cambio de pattern**

| Parametro | Que hace |
|---|---|
| `Pasosfrente` | Pasos que tarda el frente de polo a polo |
| `Frenteprueba` | Cambio de pattern de prueba: lanza el frente |

## Camara

**Camara**

| Parametro | Que hace |
|---|---|
| `Modocamara` | Camara |
| `Encuadre` | Alto del planeta en la pantalla (1 = de borde a borde) |
| `Camsuave` | Segundos para el encuadre nuevo |
| `Camaltura` | Altura de camara sobre la superficie (superficie) |
| `Camvel` | Velocidad de camara, grados/s (superficie) |
| `Camfov` | Angulo de vision, grados (globo y superficie) |

**Rasante**

| Parametro | Que hace |
|---|---|
| `Rasojo` | Rasante: ojo de pez (180 grados; Rasfov no cuenta) |
| `Rasaltura` | Rasante: altura de ojos sobre el suelo |
| `Rasfov` | Rasante: angulo de vision, grados |
| `Rasmirada` | Rasante: mirada, grados sobre la horizontal (90 = al cenit) |
| `Rasvel` | Rasante: velocidad, grados/s (0 = tripode) |
| `Rasanillo` | Rasante: va entre el anillo de este numero y el anterior |

## Vista

**Escenas**

| Parametro | Que hace |
|---|---|
| `Escena` | Escena (carga su preset) |
| `Guardarescena` | Guardar lo que hay en la escena elegida |
| `Cargarescena` | Volver a la escena elegida |

**Actuacion y diagnostico**

| Parametro | Que hace |
|---|---|
| `Modoactuacion` | Modo actuacion (sin diagnostico) |
| `Diagnostico` | Capas de diagnostico: puentes, rutas y presion |

**Render y rendimiento**

| Parametro | Que hace |
|---|---|
| `Resolucion` | Resolucion del render |
| `Materialrespaldo` | Material de respaldo (Phong, si el shader falla) |
| `Refrescopiel` | La piel se publica cada (s; 0 entera en cada fotograma) |
| `Turnos` | La piel por turnos (doble bufer; apagado: la vuelta entera) |
| `Cachearq` | Cache de la arqueologia (filas iguales mientras no cambien los cortes) |

**Luz de los secuenciadores**

| Parametro | Que hace |
|---|---|
| `Luzseq` | Luz de los secuenciadores en las celdas |
| `Luzespecie` | Luz de los secuenciadores sobre la especie (ciudad, industria y mezcla) |
| `Luzconchas` | Luz de los secuenciadores en las conchas (0 apagada, 1 normal) |

**Luz de la bateria**

| Parametro | Que hace |
|---|---|
| `Luzdrum` | Intensidad de la luz de la bateria (0 = apagada) |
| `Vidabalizadrum` | Vida de la luz (s) |

**Luz de la escena**

| Parametro | Que hace |
|---|---|
| `Luzcalida` | Luz calida (0 fria de la fase 10, 1 de dia) |

**Bocetos (alambre)**

| Parametro | Que hace |
|---|---|
| `Bocetoseq1` | SEQ1 en alambre (vegetacion, informal, mina) |
| `Bocetoseq2` | SEQ2 en alambre (relieve, planificada, energia) |
| `Bocetoconchas` | Conchas y esfera en alambre (conchas, terreno, nucleo) |
| `Colorboceto` | Color del alambre |
| `Bocetoreticula` | Pixeles entre las lineas del terreno |
| `Bocetohojas` | Parte de las hojas que se dibujan en alambre (0-1) |

## Modular

**Entrada**

| Parametro | Que hace |
|---|---|
| `Fuentemodular` | De donde llegan las senales del modular |
| `Puertoosc` | Puerto OSC (UDP) |
| `Chopmodular` | CHOP con las senales (Fuentemodular = chop) |
| `Rangomodular` | Rango en que llegan |
| `Suavizado` | Suavizado (s) |

**Valores a mano (Fuentemodular = manual)**

| Parametro | Que hace |
|---|---|
| `Lfo` | LFO (0,5: sin viento) (Fuentemodular = manual) |
| `Ruido` | Ruido (Fuentemodular = manual) |
| `Espacio` | Espacialidad (Fuentemodular = manual) |
| `Saturacion` | Saturacion (Fuentemodular = manual) |

**Efectos**

| Parametro | Que hace |
|---|---|
| `Vientomax` | LFO: viento en el dosel (grados) |
| `Respiracion` | LFO: respiracion de las ventanas |
| `Smog` | Ruido: smog de la ciudad |
| `Niebla` | Espacialidad: niebla de distancia |
| `Glitch` | Saturacion: fracturas y glitch |

## Sala

**Microfono**

| Parametro | Que hace |
|---|---|
| `Fuentemic` | De donde llega el sonido de la sala |
| `Chopmic` | CHOP con el audio (Fuentemic = chop) |
| `Canalmic` | Canal del microfono (0: el primero) |
| `Umbralonset` | Umbral de onset del microfono |
| `Reduccionmic` | Erosion de cada onset (escalones) |
| `Umbralcorte` | Ruido acumulado en 60 s que abre un corte |
| `Profundidadmic` | Profundidad del corte por ruido |

**Camara cenital**

| Parametro | Que hace |
|---|---|
| `Fuente` | De donde llega la sala |
| `Sensor` | Camara del techo |
| `Alturamin` | Altura minima de un cuerpo (m) |
| `Alturamax` | Altura maxima de un cuerpo (m) |
| `Capturarfondo` | Capturar el suelo vacio |
| `Archivofondo` | Archivo del suelo vacio |

**El suelo y el planeta**

| Parametro | Que hace |
|---|---|
| `Anchosala` | Ancho del suelo cubierto (m) |
| `Fondosala` | Fondo del suelo cubierto (m) |
| `Tamcasilla` | Lado de casilla (m) |
| `Desenfoque` | Radio de reparto (m) |
| `Ocupacionllena` | Suelo ocupado de una casilla llena |
| `Subida` | Densidad: subida (s) |
| `Bajada` | Densidad: bajada (s) |
| `Loncentral` | Longitud central (sigue al giro) |
| `Anchoangular` | Longitudes que cubre el ancho de la sala |
| `Latnorte` | Latitud de la pared de la pantalla |
| `Latsur` | Latitud del fondo de la sala |
| `Espejo` | Invertir izquierda y derecha |

**Personas**

| Parametro | Que hace |
|---|---|
| `Separacioncabezas` | Separacion minima entre cabezas (m) |
| `Confirmapersona` | Fotogramas para confirmar una persona |

**Probar la sala**

| Parametro | Que hace |
|---|---|
| `Simcasilla` | Probar: casilla (0 = pantalla, izquierda) |
| `Simponer` | Probar: poner una persona |
| `Simquitar` | Probar: quitarla |
| `Simvaciar` | Probar: vaciar la sala |
| `Simfila` | Personas de la fila de prueba |
| `Simformarfila` | Formar una fila |

**Balance, estroboscopio y DMX**

| Parametro | Que hace |
|---|---|
| `Ventanabalance` | Ventana del balance (s) |
| `Umbralestrobo` | Estroboscopio: entra con este balance |
| `Salidaestrobo` | Estroboscopio: sale por debajo de |
| `Maxhz` | Destellos maximos por segundo (tope 3) |
| `Noche` | Noche de enterramiento (s) |
| `Colapsoon` | Colapso por erosion dominante sostenida |
| `Maxerosion` | Erosion dominante que colapsa (s) |
| `Interfazdmx` | Salida DMX |
| `Universodmx` | Universo DMX |
| `Simbalance` | Probar: forzar el balance (-1: el real) |

## Presencia

**Presencia**

| Parametro | Que hace |
|---|---|
| `Activo` | Presencia activa (apagado: todo prende) |
| `Cuanto` | Probabilidad con la sala vacia |
| `Pesocrear` | Peso de la presencia al construir |
| `Pesoerosion` | Peso de la presencia al erosionar |
| `Reiniciarcuentas` | Reiniciar contadores |

**Huella**

| Parametro | Que hace |
|---|---|
| `Probllegada` | Probabilidad de huella al llegar |
| `Tparada` | Tiempo de parada (s) |
| `Minhuellas` | Huellas minimas para estrato humano |
| `Inclusionesmax` | Cobertura maxima de inclusiones |

**Fila**

| Parametro | Que hace |
|---|---|
| `Minfila` | Personas minimas de una fila |
| `Tfila` | Tiempo de la fila (s) |
| `Modofila` | Forma de la fila |
| `Conchasporpersona` | Conchas por persona |
| `Simsumar` | Sumar una persona a la fila |

**Historico**

| Parametro | Que hace |
|---|---|
| `Exportartestigo` | Exportar el testigo de la ultima escision |
| `Carpetahistorico` | Carpeta del historico |

## Juego

**Partida**

| Parametro | Que hace |
|---|---|
| `Modojuego` | Modo juego |
| `Rondagenozilla` | Ronda GENoZilla (desde el primer monstruo; 6 min acaban la partida) |
| `Duracionronda` | Duracion de ronda (s) |
| `Rondas` | Rondas |
| `Pasojuego` | Paso de juego (semicorcheas) |
| `Nuevapartida` | Nueva partida |
| `Partidalibre` | Partida libre (pruebas) |
| `Dominio` | Dominio para ganar (libre) |
| `Titulojuego` | Titulos de la ronda en el centro del mundo |
| `Marcador` | Marcador de la partida (celdas, ronda y monstruos en pie) |

**Marcas y luz**

| Parametro | Que hace |
|---|---|
| `Marcajugador` | Marca de jugador |
| `Marcapublico` | Marca tambien sin juego |
| `Luzjuego` | Luz de juego |

**Zanja**

| Parametro | Que hace |
|---|---|
| `Zanjajuego` | Zanja de juego |
| `Profundidadagua` | Profundidad del agua (conchas) |
| `Ritmoagua` | Ritmo del agua (escalones por paso) |
| `Desbordeagua` | Desborde del agua (escalones por paso) |
| `Ahoga` | Nivel que ahoga (fraccion de la zanja) |
| `Simzanja` | Simular zanja |

**Rescate**

| Parametro | Que hace |
|---|---|
| `Aliados` | Aliados del rescate |
| `Taliados` | Tiempo del rescate (s) |
| `Simrescate` | Simular rescate |

**Armas**

| Parametro | Que hace |
|---|---|
| `Armacerco` | Arma: cerco |
| `Hambre` | Hambre del cerco (escalones por compas) |
| `Armapison` | Arma: pisoton |
| `Npison` | Personas del pisoton |
| `Encoge` | Encogimiento por paso |
| `Armaestatuas` | Arma: estatuas |
| `Tquietud` | Tiempo de estatuas (s) |
| `Umbralsilencio` | Umbral de silencio (flujo del microfono) |
| `Tpiedra` | Tiempo petrificado (s) |
| `Armagrito` | Arma: grito |
| `Profgrito` | Profundidad del grito (conchas) |
| `Recargagrito` | Recarga del grito (s) |
| `Armarelampago` | Arma: relampago |
| `Taturdido` | Tiempo aturdido (s) |

**El mal**

| Parametro | Que hace |
|---|---|
| `Herenciamal` | Herencia del mal |
| `Especiemal` | Especie del mal (sin: el velo provisional) |
| `Vecinasencierro` | Vecinas del mal para cerrarse (encierro) |
| `Pasosobramal` | Pasos por paso de obra |
| `Tamanoemblema` | Tamano del emblema (celdas) |
| `Brilloemblema` | Brillo del emblema (neon) |
| `Altomal` | Alto de los edificios del mal (x la planta) |
| `Demoniomal` | El demonio de los clusters |
| `Simmal` | Simular cluster del mal |

## Monstruos

La llevan sus fases (33, 38, 39, 40, 41 y 42), por secciones:

- **Monstruo: aparicion, apetito y pasos (fase 33)**
- **Trumpzilla y los sprites (fase 38)**
- **Por donde andan (fase 39)**
- **Godzilla (fase 40)**
- **NefanyaMuto (fase 41)**
- **Godzilla azul (fase 42)**

## Versiones

**Versiones instaladas**

| Parametro | Que hace |
|---|---|
| `Nivel` | Ultima fase aplicada |
| `Version26` | Fase 26 (borrado) |
| `Version28` | Fase 28 (noche) |
| `Version30` | Fase 30 (relampago) |
