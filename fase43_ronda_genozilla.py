"""
=============================================================================
ESTRATOS - FASE 43: LA RONDA GENOZILLA
=============================================================================
Requiere la fase 42. Cambia como se cuenta la partida en modo juego y le pone
titulos de combate en el centro del mundo.

QUE HACE
--------
  EMPIEZA      la ronda ya no empieza al encender Modojuego: empieza cuando
               aparece el PRIMER MONSTRUO (Trumpzilla, NefanyaMuto o un Godzilla)
               o cuando el MUNDO COLAPSA. Mientras tanto el reloj no corre.
  DURA         Duracionronda (6 min, 360 s).
  COLAPSO      en modo juego el mundo vuelve a poder colapsar: un fin de ciclo
               (la fase 6: estancado, edad maxima, cambio de pattern) o el
               colapso de la sala (fase 23, con Colapsoon). Si colapsa a mitad de
               una ronda, se entierra, la ronda cuenta (recuento, marcada como
               colapso) y empieza otra de 6 min en ese momento.
  FIN          la PARTIDA acaba cuando una ronda llega a sus 6 min (Rondas ya no
               cuenta): recuento, entierro y espera; gana quien domina el globo
               al final. Nuevapartida empieza otra (esperando al monstruo).
  TITULOS      en el centro del mundo, grandes, en una letra de cartel de
               combate (Impact, con sombra):
                 al empezar     3, 2, 1 y «GENoZilla Begins!!!»
                 tras colapso   «RONDA n» (el mundo colapsa)
                 los 5 s finales  estroboscopio y la cuenta 5, 4, 3, 2, 1 (rojo)
                 al acabar      «Stratos x GENoZilla Ends!!!» y quien gana
               El estroboscopio pasa por el limitador comun (3 destellos por
               segundo como mucho).
  HERENCIA     v2 (motor v148): con Herenciareparto (encendido), al enterrar,
               lo heredado conserva su especie (naturaleza, ciudad, industria)
               y cuenta en el reparto: en el construido, en el globo N/C/I y en
               el tramo con el que empieza el mundo nuevo. Hasta ahora quedaba
               neutro y el mundo nuevo volvia al 100 % naturaleza. Apagado, como
               antes.
  MARCADOR     v3-v4 (motor v149-v150): con Marcador (encendido), en modo
               juego, encima del mundo, arriba a la izquierda dos recuadros
               seguidos (v5): NATURAL EVOLUTION (las celdas del publico) con los
               monstruos del bien en accion (Godzilla y el azul) y, a su derecha,
               OUTBREAKS OF EVIL
               (las celdas del mal) con Trumpzilla y NefanyaMuto. Cada monstruo
               en su casilla con la cara y la animacion de su sprite del mundo
               (respira, camina, devora, tiembla, lucha, baile...). Arriba a la
               derecha, la ronda y su reloj (rojo en los 5 s finales). v4: si el
               shader del marcador no compila, marcador_seguro lo deja
               transparente: el mundo nunca se tapa. v6 (motor v151): una
               casilla fija por monstruo (Godzilla y el azul; Trumpzilla y
               NefanyaMuto): en gris y quieto mientras no esta en el planeta.
  APAGADO      Rondagenozilla apagado: las rondas de siempre (fase 32). La
               partida libre (Partidalibre) tampoco tiene rondas. La demo
               GENoZilla de la sala la apaga mientras dura.
  LEYENDA      JUEGO    GENoZilla   esperando al primer monstruo (o al colapso)
               JUEGO    GENoZilla ronda 2   3:12   publico 38   mal 14   (globo)   colapsos 1
               JUEGO    fin GENoZilla   gana el bien   publico 40   mal 12   (2 rondas, 1 colapso)

OPERADORES (en /project1/FASE1)
-------------------------------
  titulo_juego, titulo_juego_sombra, titulo_juego_sub   Text TOP (1280 x 720)
  con_titulo_sombra, con_titulo_texto, con_titulo_juego Over TOP: el titulo
               encima del render. con_rotulo (la leyenda) y out_render (la sala
               virtual) salen de con_titulo_juego.
  marcador_monstruos (GLSL TOP, marcador_pixel; los cuatro atlas de entrada),
  marcador_seguro (Switch TOP: transparente, marcador_vacio, si el shader
  falla), marcador_bien, marcador_mal, marcador_ronda, marcador_reloj (Text
  TOP) y con_marcador_* (Over TOP): el marcador encima del render
  (con_marcador), debajo de los titulos.

PARAMETROS (Juego: Partida; Herenciareparto en Crecimiento: Especies y mezcla)
-----------------------------------------------------------------------------
  Rondagenozilla (encendido), Titulojuego (encendido), Herenciareparto
  (encendido). Duracionronda (Fase32), 360 s.

PROBAR
------
  Modojuego: la leyenda dice que espera al primer monstruo. Simmonstruo: «3, 2,
  1, GENoZilla Begins!!!» y el reloj de 6:00 empieza. Duracionronda 20 para ver
  el final enseguida: estrobo, 5 ... 1 y «Stratos x GENoZilla Ends!!!».
  Forzarciclo a mitad: el mundo colapsa y empieza la ronda siguiente.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase43_ronda_genozilla.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase43 v7  (el marcador: los cuatro atlas siempre enchufados en orden; casilla fija por monstruo)'
banner(VERSION)

base = require_base(43)
motor = install_core(base, CARPETA, 43)
m = motor.module

page = get_page(base, 'Fase43')
add_par(base, page, 'toggle', 'Rondagenozilla', 'Ronda GENoZilla (desde el primer monstruo; 6 min acaban la partida)',
        True)
add_par(base, page, 'toggle', 'Titulojuego', 'Titulos de la ronda en el centro del mundo', True)
add_par(base, page, 'toggle', 'Herenciareparto', 'Lo heredado cuenta en el reparto de especies', True)
add_par(base, page, 'toggle', 'Marcador', 'Marcador de la partida (celdas, ronda y monstruos en pie)', True)
ok('parametros de la fase 43: Rondagenozilla, Titulojuego, Herenciareparto y Marcador (encendidos); la ronda '
   'dura Duracionronda (%d s)' % int(base.par.Duracionronda.eval()) if has_par(base, 'Duracionronda') else
   'parametros de la fase 43: Rondagenozilla, Titulojuego, Herenciareparto y Marcador (encendidos)')


# -----------------------------------------------------------------------------
# OPERADORES: el titulo en el centro del mundo
# -----------------------------------------------------------------------------

def letra(nombres):
    """La primera fuente instalada de la lista (Windows o macOS); si no, Arial."""
    import os
    carpetas = ['C:/Windows/Fonts', os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts'),
                '/Library/Fonts', '/System/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
    hay = []
    for d in carpetas:
        try:
            hay += [f.replace(' ', '').replace('-', '').replace('_', '').lower() for f in os.listdir(d)]
        except Exception:
            pass
    for n in nombres:
        clave = n.replace(' ', '').lower()
        if any(clave in f for f in hay):
            return n
    return 'Arial'


TIT = "parent().op('motor').module.titulo('%s', absTime.frame)"
LETRA_TIT = letra(['Impact', 'Bebas Neue', 'Anton', 'Arial Black'])
LETRA_SUB = letra(['Bahnschrift', 'Arial Black', 'Arial'])
TAM_TIT, TAM_SUB = 140, 30


def titulo_top(nombre, x, y, tam, color, fuente_, dx=0, dy=0, sub=False):
    o = get_or_make(base, 'textTOP', nombre, x, y)
    setmenu(o, ['outputresolution'], ['custom'], None)
    setp_any(o, ['resolutionw'], 1280)
    setp_any(o, ['resolutionh'], 720)
    setp_any(o, ['font', 'fontfamily'], fuente_)
    setp_any(o, ['alignx'], 'center')
    setp_any(o, ['aligny'], 'center')
    setmenu(o, ['positionunit', 'positionunits'], ['pixels'], None)
    setp_any(o, ['positionx', 'textx'], dx)
    setp_any(o, ['positiony', 'texty'], dy)
    for ch in 'rgb':
        setp_any(o, ['bgcolor' + ch, 'backgroundcolor' + ch], 0.0)
    transp = setp_any(o, ['bgalpha', 'backgroundalpha', 'bgcolora'], 0.0)
    setexpr(o, 'text', TIT % ('sub' if sub else 'texto'))
    if sub:
        for n in ('fontsizex', 'fontsize', 'fontsizey'):
            setp(o, n, tam)
    else:                               # entra grande y se asienta (escala)
        for n in ('fontsizex', 'fontsize', 'fontsizey'):
            setexpr(o, n, '%d * %s' % (tam, TIT % 'escala'))
    for ch in 'rgb':
        if color is None:
            setexpr(o, 'fontcolor' + ch, TIT % ch)
        else:
            setp_any(o, ['fontcolor' + ch, 'color' + ch], color['rgb'.index(ch)])
    for n in ('fontalpha', 'fontcolora'):
        setexpr(o, n, TIT % 'alfa')
    return o, bool(transp)


def over(nombre, arriba, abajo, x, y):
    o = get_or_make(base, 'overTOP', nombre, x, y)
    enchufar_en_orden(o, [arriba, abajo])  # v7: arriba en la 0, abajo en la 1, sin correrse
    return o


# -----------------------------------------------------------------------------
# OPERADORES (v4): el marcador encima del mundo
# -----------------------------------------------------------------------------
# Arriba a la izquierda, dos recuadros: NATURAL EVOLUTION (las celdas del publico y
# los monstruos del bien en accion: Godzilla y el azul) y, a su derecha (v5), OUTBREAKS OF EVIL
# (las celdas del mal y Trumpzilla y NefanyaMuto). Cada monstruo en su casilla, con la
# cara y la animacion de su sprite del mundo (las mismas cuentas que sprite_vertex).
# Arriba a la derecha, el reloj de la ronda. Los fondos y los monstruos, en un GLSL TOP
# (marcador_monstruos, con los atlas de entrada); los textos, Text TOP. v4: si el GLSL
# TOP no compila, marcador_seguro pasa a transparente (el mundo nunca se tapa).

MAR = "parent().op('motor').module.marcador('%s', absTime.frame)"
ANCHO, ALTO = 1280, 720
MARGEN = 16
CASILLA_W, CASILLA_H = 84, 112          # una casilla de monstruo (el aspecto del atlas, 0,75)
PAD = 8
CABECERA = 38                           # el alto del titulo de cada recuadro
CAJA_W = 290
CAJA_H = CABECERA + CASILLA_H + PAD
CAJA_X = MARGEN                                         # NATURAL EVOLUTION, arriba a la izquierda
CAJA_MAL_X = CAJA_X + CAJA_W + 12                       # v5: OUTBREAKS OF EVIL, seguido a su derecha
CAJA_Y = ALTO - MARGEN - CAJA_H                         # los dos a la misma altura (y hacia arriba)
RELOJ_W, RELOJ_H = 220, 96

MARCADOR_PIXEL = """// Estratos - el marcador de la partida (fase 43 v4): NATURAL EVOLUTION (el bien) y
// OUTBREAKS OF EVIL (el mal), cada uno con sus monstruos en accion, y el panel del reloj.
// Cada casilla dibuja su monstruo con la cara del atlas (4 x 3 celdas) y la animacion de
// su sprite del mundo (sprite_vertex). Entradas, segun las que haya: 0 trumpzilla,
// 1 nefanyamuto, 2 godzilla, 3 godzilla_azul (sus atlas).
uniform vec4 uMar;          // x encendido, y los 5 s finales, z el reloj (s)
uniform vec4 uB0;           // por casilla: x atlas (-1 vacia), y cara, z animacion, w en pie (0: gris y quieto)
uniform vec4 uB1;
uniform vec4 uE0;
uniform vec4 uE1;
uniform vec4 uCajaB;        // x y (abajo a la izquierda), ancho, alto del recuadro del bien
uniform vec4 uCajaE;        // el del mal
uniform vec4 uReloj;        // x y ancho alto del panel del reloj
uniform vec4 uCasilla;      // ancho, alto de una casilla, pad, alto de la cabecera

layout(location = 0) out vec4 fragColor;

vec4 atlasFetch(int k, vec2 uv, int cara)
{
    vec4 t = vec4(0.0);
#if TD_NUM_2D_INPUTS > 0
    vec2 tam = vec2(1.0);
    if (k == 0) tam = vec2(textureSize(sTD2DInputs[0], 0));
#if TD_NUM_2D_INPUTS > 1
    if (k == 1) tam = vec2(textureSize(sTD2DInputs[1], 0));
#endif
#if TD_NUM_2D_INPUTS > 2
    if (k == 2) tam = vec2(textureSize(sTD2DInputs[2], 0));
#endif
#if TD_NUM_2D_INPUTS > 3
    if (k == 3) tam = vec2(textureSize(sTD2DInputs[3], 0));
#endif
    vec2 celda = tam / vec2(4.0, 3.0);
    float col = mod(float(cara), 4.0);
    float fila = floor(float(cara) / 4.0 + 0.001);
    vec2 px = (vec2(col, 2.0 - fila) + uv) * celda;      // la fila 0 del atlas, arriba
    ivec2 ip = ivec2(clamp(px, vec2(0.0), tam - 1.0));
    if (k == 0) t = texelFetch(sTD2DInputs[0], ip, 0);
#if TD_NUM_2D_INPUTS > 1
    if (k == 1) t = texelFetch(sTD2DInputs[1], ip, 0);
#endif
#if TD_NUM_2D_INPUTS > 2
    if (k == 2) t = texelFetch(sTD2DInputs[2], ip, 0);
#endif
#if TD_NUM_2D_INPUTS > 3
    if (k == 3) t = texelFetch(sTD2DInputs[3], ip, 0);
#endif
#endif
    return t;
}

float rect(vec2 p, vec2 a, vec2 b, float r)     // 1 dentro del rectangulo redondeado a-b
{
    vec2 c = 0.5 * (a + b);
    vec2 h = 0.5 * (b - a) - vec2(r);
    vec2 q = abs(p - c) - h;
    float d = length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - r;
    return 1.0 - smoothstep(-1.0, 1.0, d);
}

vec4 sobre(vec4 abajo, vec4 arriba)
{
    float a = arriba.a + abajo.a * (1.0 - arriba.a);
    vec3 c = vec3(0.0);
    if (a > 0.0)
        c = (arriba.rgb * arriba.a + abajo.rgb * abajo.a * (1.0 - arriba.a)) / a;
    return vec4(c, a);
}

vec4 casilla(vec2 p, vec4 M, vec4 C, float slot, vec3 tono)
{
    vec2 a0 = vec2(C.x + uCasilla.z + slot * (uCasilla.x + uCasilla.z), C.y + uCasilla.z);
    vec2 b0 = a0 + uCasilla.xy;
    float dentro = rect(p, a0, b0, 8.0);
    vec4 res = vec4(tono * 0.18, 0.55 * dentro);
    if (M.x > -0.5) {
        int k = int(M.x + 0.5);
        int cara = int(M.y + 0.5);
        int anim = int(M.z + 0.5);
        float t = uMar.z + 1.7 * slot + 0.9 * M.x;
        vec2 kk = vec2(1.0);
        vec2 d = vec2(0.0);
        float rot = 0.0;
        if (anim == 0) {                                // respira
            kk = vec2(1.0 - 0.012 * sin(t * 2.4), 1.0 + 0.025 * sin(t * 2.4));
        } else if (anim == 1) {                         // camina
            d.y = 0.035 * abs(sin(t * 6.0));
            rot = 0.07 * sin(t * 6.0);
        } else if (anim == 2) {                         // devora
            float mm = sin(t * 9.0);
            kk = vec2(1.0 - 0.04 * mm, 1.0 + 0.06 * mm);
        } else if (anim == 3 || anim == 4) {            // tiembla, hunde
            d = vec2(0.025 * sin(t * 47.0), 0.010 * sin(t * 31.0));
        } else if (anim == 6) {                         // aturdido
            rot = 0.15 * sin(t * 3.0);
        } else if (anim == 7) {                         // lucha
            float g = 0.6 + 0.4 * sin(t * 20.0);
            d = vec2(-0.08 * g, 0.015 * abs(sin(t * 10.0)));
            rot = 0.12 * g;
        } else if (anim == 8) {                         // adios
            rot = 0.06 * sin(t * 2.0);
        } else if (anim == 9) {                         // baile
            float bb = sin(t * 4.0);
            rot = 0.11 * bb;
            d = vec2(0.05 * bb, 0.06 * abs(sin(t * 8.0)));
            kk = vec2(1.0 + 0.03 * sin(t * 8.0), 1.0 - 0.03 * sin(t * 8.0));
        } else if (anim == 10) {                        // anillo
            float g2 = sin(t * 14.0);
            kk = vec2(1.0 + 0.035 * g2);
            d = vec2(0.012 * sin(t * 41.0), 0.0);
        }
        float w = uCasilla.x * 0.86;
        float h = uCasilla.y * 0.86;
        vec2 pie = vec2(0.5 * (a0.x + b0.x), a0.y + 0.05 * uCasilla.y);
        vec2 q = p - pie - d * vec2(w, h);
        q = vec2(q.x * cos(rot) + q.y * sin(rot), -q.x * sin(rot) + q.y * cos(rot));
        vec2 uv = vec2(q.x / (kk.x * w) + 0.5, q.y / (kk.y * h));
        if (uv.x >= 0.0 && uv.x <= 1.0 && uv.y >= 0.0 && uv.y <= 1.0 && dentro > 0.5) {
            vec4 tx = atlasFetch(k, uv, cara);
            if (tx.a > 0.5) {
                vec3 rgb = tx.rgb / tx.a;
                if (anim == 5)
                    rgb = vec3(dot(rgb, vec3(0.30, 0.59, 0.11))) * vec3(0.80, 0.78, 0.74);
                else if (anim == 6)
                    rgb = mix(rgb, vec3(1.0), 0.35 * step(0.5, fract(uMar.z * 3.0)));
                res = sobre(res, vec4(rgb, M.w > 0.5 ? 1.0 : 0.38));
            }
        }
    }
    float marco = dentro - rect(p, a0 + vec2(2.0), b0 - vec2(2.0), 6.0);
    res = sobre(res, vec4(tono, marco * (M.x > -0.5 && M.w > 0.5 ? 1.0 : 0.35)));
    return res;
}

vec4 recuadro(vec2 p, vec4 C, vec3 tono)
{
    vec2 a0 = C.xy;
    vec2 b0 = C.xy + C.zw;
    float r = rect(p, a0, b0, 12.0);
    vec4 res = vec4(vec3(0.02, 0.02, 0.03), 0.64 * r);
    float linea = rect(p, vec2(a0.x + 12.0, b0.y - uCasilla.w + 2.0), vec2(b0.x - 12.0, b0.y - uCasilla.w + 4.0), 1.0);
    res = sobre(res, vec4(tono, 0.7 * linea));
    float marco = r - rect(p, a0 + vec2(2.0), b0 - vec2(2.0), 10.0);
    return sobre(res, vec4(tono, 0.6 * marco));
}

void main()
{
    vec2 p = gl_FragCoord.xy;
    vec4 c = vec4(0.0);
    if (uMar.x > 0.5) {
        vec3 bien = vec3(0.35, 0.95, 0.55);
        vec3 mal = vec3(1.0, 0.30, 0.25);
        c = sobre(c, recuadro(p, uCajaB, bien));
        c = sobre(c, casilla(p, uB0, uCajaB, 0.0, bien));
        c = sobre(c, casilla(p, uB1, uCajaB, 1.0, bien));
        c = sobre(c, recuadro(p, uCajaE, mal));
        c = sobre(c, casilla(p, uE0, uCajaE, 0.0, mal));
        c = sobre(c, casilla(p, uE1, uCajaE, 1.0, mal));
        vec4 fr = uMar.y > 0.5 ? vec4(0.35, 0.02, 0.02, 0.72) : vec4(0.02, 0.02, 0.03, 0.64);
        c = sobre(c, fr * vec4(1.0, 1.0, 1.0, rect(p, uReloj.xy, uReloj.xy + uReloj.zw, 12.0)));
    }
    fragColor = TDOutputSwizzle(vec4(c.rgb * c.a, c.a));     // premultiplicado, como los TOP
}
"""


def uniforme(o, k, nombre, exprs):
    setp_any(o, ['vec%dname' % k, 'uniname%d' % k], nombre)
    for ch, e in zip('xyzw', exprs):
        if isinstance(e, str):
            setexpr(o, 'vec%dvalue%s' % (k, ch), e)
        else:
            setp(o, 'vec%dvalue%s' % (k, ch), e)


for viejo in ('con_marcador_bien', 'con_marcador_mal', 'con_marcador_ronda'):   # v3: ya no estan
    if base.op(viejo) is not None:
        base.op(viejo).destroy()
px_dat = get_or_make(base, 'textDAT', 'marcador_pixel', 300, -900)
px_dat.text = MARCADOR_PIXEL
mon_top = get_or_make(base, 'glslTOP', 'marcador_monstruos', 300, -800)
setp_any(mon_top, ['pixeldat'], 'marcador_pixel')
setmenu(mon_top, ['outputresolution'], ['custom'], None)
setp_any(mon_top, ['resolutionw'], ANCHO)
setp_any(mon_top, ['resolutionh'], ALTO)
setmenu(mon_top, ['format'], ['rgba8fixed', 'rgba8'], None)


def nombres_entradas(o):
    try:
        return [x.name for x in o.inputs]
    except Exception:
        return []


def enchufar_en_orden(dst, srcs):
    """v7: las entradas de dst, exactamente srcs y en ese orden (la entrada i, el atlas i
    del shader). En TouchDesigner, al desenchufar una entrada las de detras se corren:
    se desenchufa siempre la primera hasta dejarlo vacio y se enchufa cada una en la
    primera libre. Si TouchDesigner tiene setInputs, primero eso. Devuelve los nombres."""
    quiero = [x.name for x in srcs]
    try:
        if hasattr(dst, 'setInputs'):
            dst.setInputs(list(srcs))
    except Exception:
        pass
    if nombres_entradas(dst) == quiero:
        return quiero
    for _ in range(16):
        if not dst.inputs:
            break
        try:
            dst.inputConnectors[0].disconnect()
        except Exception:
            break
    for i, src in enumerate(srcs):
        hecho = False
        try:
            dst.inputConnectors[i].connect(src)
            hecho = True
        except Exception:
            pass
        if not hecho:
            try:
                src.outputConnectors[0].connect(dst)     # la primera entrada libre
            except Exception:
                pass
    return nombres_entradas(dst)


atlas_ops = []
faltan = []
for n in m.MARCADOR_MON:
    at = base.op(n + '_atlas')
    if at is None:
        faltan.append(n + '_atlas')
        break                               # las entradas, seguidas: sin hueco
    atlas_ops.append(at)
ENTRADAS = enchufar_en_orden(mon_top, atlas_ops)
if ENTRADAS != [x.name for x in atlas_ops]:
    faltan.append('el orden de las entradas (%s)' % ', '.join(ENTRADAS or ['ninguna']))
uniforme(mon_top, 0, 'uMar', [MAR % 'on', MAR % 'final', 'absTime.seconds', 0])
for k, nombre in enumerate(('b0', 'b1', 'e0', 'e1')):
    uniforme(mon_top, 1 + k, 'u' + nombre.upper(), [MAR % (nombre + x) for x in 'acgv'])
uniforme(mon_top, 5, 'uCajaB', [CAJA_X, CAJA_Y, CAJA_W, CAJA_H])
uniforme(mon_top, 6, 'uCajaE', [CAJA_MAL_X, CAJA_Y, CAJA_W, CAJA_H])
uniforme(mon_top, 7, 'uReloj', [ANCHO - MARGEN - RELOJ_W, ALTO - MARGEN - RELOJ_H, RELOJ_W, RELOJ_H])
uniforme(mon_top, 8, 'uCasilla', [CASILLA_W, CASILLA_H, PAD, CABECERA])
# v4: si el shader no compila (o le faltan entradas), el marcador se queda transparente
vacio = get_or_make(base, 'constantTOP', 'marcador_vacio', 300, -700)
setmenu(vacio, ['outputresolution'], ['custom'], None)
setp_any(vacio, ['resolutionw'], ANCHO)
setp_any(vacio, ['resolutionh'], ALTO)
for ch in ('colorr', 'colorg', 'colorb'):
    setp(vacio, ch, 0.0)
setp_any(vacio, ['alpha', 'colora'], 0.0)
seguro = get_or_make(base, 'switchTOP', 'marcador_seguro', 410, -750)
for i in (1, 0):
    try:
        seguro.inputConnectors[i].disconnect()
    except Exception:
        pass
connect(seguro, vacio, 0)
connect(seguro, mon_top, 1)
setexpr(seguro, 'index', "0 if (absTime.frame < 0 or parent().op('marcador_monstruos').errors() "
                         "or parent().op('marcador_pixel') is None) else 1")

LETRA_MAR = letra(['Bahnschrift', 'Impact', 'Arial Black', 'Arial'])


def marcador_top(nombre, x, y, que, tam, color, alinea, dx, dy, color_expr=None):
    o = get_or_make(base, 'textTOP', nombre, x, y)
    setmenu(o, ['outputresolution'], ['custom'], None)
    setp_any(o, ['resolutionw'], ANCHO)
    setp_any(o, ['resolutionh'], ALTO)
    setp_any(o, ['font', 'fontfamily'], LETRA_MAR)
    for n in ('fontsizex', 'fontsize', 'fontsizey'):
        setp(o, n, tam)
    setp_any(o, ['alignx'], alinea)
    setp_any(o, ['aligny'], 'top')
    setmenu(o, ['positionunit', 'positionunits'], ['pixels'], None)
    setp_any(o, ['positionx', 'textx'], dx)
    setp_any(o, ['positiony', 'texty'], dy)
    for ch in 'rgb':
        setp_any(o, ['bgcolor' + ch, 'backgroundcolor' + ch], 0.0)
    transp = setp_any(o, ['bgalpha', 'backgroundalpha', 'bgcolora'], 0.0)
    for i, ch in enumerate('rgb'):
        if color_expr is not None:
            setexpr(o, 'fontcolor' + ch, color_expr[i])
        else:
            setp_any(o, ['fontcolor' + ch, 'color' + ch], color[i])
    setp_any(o, ['fontalpha', 'fontcolora'], 1.0)
    setexpr(o, 'text', MAR % que)
    return o, bool(transp)


X_TXT = CAJA_X + 16
t_bien, b1 = marcador_top('marcador_bien', 300, -980, 'bien', 22, (0.55, 1.0, 0.68), 'left', X_TXT,
                          -(MARGEN + 9))
t_mal, b2 = marcador_top('marcador_mal', 300, -1060, 'mal', 22, (1.0, 0.55, 0.48), 'left', CAJA_MAL_X + 16,
                         -(MARGEN + 9))
t_ronda, b3 = marcador_top('marcador_ronda', 300, -1140, 'ronda', 20, (0.92, 0.92, 0.96), 'right', -(MARGEN + 18),
                           -(MARGEN + 10))
fin_rgb = ["1.0", "0.35 if %s else 1.0" % (MAR % 'final'), "0.30 if %s else 1.0" % (MAR % 'final')]
t_reloj, b4 = marcador_top('marcador_reloj', 300, -1220, 'reloj', 52, None, 'right', -(MARGEN + 18),
                           -(MARGEN + 34), color_expr=fin_rgb)
h1 = over('con_marcador_fondo', seguro, base.op('render'), 520, -800)
h2 = over('con_marcador_textos', t_bien, h1, 520, -980)
h3 = over('con_marcador_textos2', t_mal, h2, 520, -1060)
h4 = over('con_marcador_textos3', t_ronda, h3, 520, -1140)
h5 = over('con_marcador', t_reloj, h4, 520, -1220)
if not faltan and b1 and b2 and b3 and b4:
    ok('marcador: NATURAL EVOLUTION y OUTBREAKS OF EVIL (arriba a la izquierda: sus celdas y sus monstruos en '
       'accion; marcador_monstruos con los atlas de los cuatro) y el reloj de la ronda (arriba a la derecha), '
       'encima del render (con_marcador); si el shader falla, transparente (marcador_seguro)')
else:
    info('marcador: falta %s (el shader dibuja solo los de antes) o no pude hacer transparente algun Text TOP'
         % ', '.join(faltan))

render = base.op('render')
sombra, t1 = titulo_top('titulo_juego_sombra', 520, -560, TAM_TIT, (0.0, 0.0, 0.0), LETRA_TIT, dx=7, dy=-7)
texto, t2 = titulo_top('titulo_juego', 520, -640, TAM_TIT, None, LETRA_TIT)
sub, t3 = titulo_top('titulo_juego_sub', 520, -720, TAM_SUB, (0.92, 0.92, 0.96), LETRA_SUB, dy=-120, sub=True)
c1 = over('con_titulo_sombra', sombra, base.op('con_marcador') or render, 740, -560)
c2 = over('con_titulo_texto', texto, c1, 740, -640)
c3 = over('con_titulo_juego', sub, c2, 740, -720)
rot = base.op('con_rotulo')
if rot is not None:
    try:
        rot.inputConnectors[1].disconnect()
    except Exception:
        pass
    connect(rot, c3, 1)
outr = base.op('out_render')            # la sala virtual: su pantalla ve el titulo
if outr is not None:
    try:
        outr.inputConnectors[0].disconnect()
    except Exception:
        pass
    connect(outr, c3, 0)
if t1 and t2 and t3:
    ok('titulo de la ronda en el centro del mundo: titulo_juego (%s %d, con sombra) y titulo_juego_sub (%s); '
       'con_titulo_juego -> con_rotulo%s' % (LETRA_TIT, TAM_TIT, LETRA_SUB, ' y out_render' if outr else ''))
else:
    info('titulo_juego: no pude hacer transparente el fondo de algun Text TOP; revisa bgalpha')

set_render(base)

leeme(base, 43, """FASE 43 - LA RONDA GENOZILLA
  Con Rondagenozilla, la ronda empieza cuando aparece el primer monstruo o
  cuando el mundo colapsa (un fin de ciclo o el colapso de la sala, que en modo
  juego vuelven a contar) y dura Duracionronda (6 min). Si el mundo colapsa a
  mitad, se entierra, la ronda cuenta y empieza otra de 6 min. La partida acaba
  cuando una ronda llega a sus 6 min. Titulos en el centro del mundo
  (Titulojuego): 3, 2, 1 y GENoZilla Begins!!!; RONDA n tras un colapso; los
  5 s finales, estroboscopio y 5 ... 1; al acabar, Stratos x GENoZilla Ends!!!
  v2: con Herenciareparto, lo heredado conserva su especie y cuenta en el
  reparto (construido, globo N/C/I y el tramo del mundo nuevo).
  v3-v4: Marcador: arriba a la izquierda NATURAL EVOLUTION (celdas del publico y
  los monstruos del bien en accion) y OUTBREAKS OF EVIL (celdas del mal y los
  suyos), gesticulando como sus sprites; arriba a la derecha, la ronda y su
  reloj. Si el shader falla, el marcador queda transparente.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS43 = ('Fuente', 'Probllegada', 'Temaenciclo', 'Modojuego', 'Umbralaparicion', 'Umbralnefa', 'Simbalance',
          'Colapsoon', 'Duracionronda', 'Rondas', 'Rondagenozilla', 'Titulojuego', 'Luzjuego', 'Herenciareparto', 'Marcador')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS43)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _poner(m, W, i, occ):
    W['occ'][i], W['carga'][i], W['par'][i] = occ, 0, -1
    W['sp'][i] = W['own'][i] = m.GEO
    W['traza'][i] = 1
    W['h'][i] = m.height_for(m.cfg(), occ)


def _prueba(t, m):
    base.par.Fuente = 'simulada'
    base.par.Temaenciclo = False
    base.par.Probllegada = 0.0
    base.par.Colapsoon = False
    base.par.Simbalance = -1.0
    base.par.Umbralaparicion = 1.0          # Trumpzilla no aparece solo: lo pide la prueba
    base.par.Umbralnefa = 1.0
    base.par.Duracionronda = 20.0
    base.par.Rondas = 4
    base.par.Titulojuego = True
    S = SalaJuego(base, m, absTime.seconds + 9100.0, rondagz=True)
    vis = sorted(m.cara_visible(m.cfg()))
    a = vis[len(vis) // 2]

    # 1. los operadores: el titulo encima del render, la leyenda y la sala encima de el
    rot = base.op('con_rotulo')
    ops = all(base.op(n) is not None for n in ('titulo_juego', 'titulo_juego_sombra', 'titulo_juego_sub',
                                               'con_titulo_juego'))
    cable = rot is None or nombres_entradas(rot)[1:2] == ['con_titulo_juego']
    t.check('titulo_juego, su sombra y titulo_juego_sub encima del render (con_titulo_juego); con_rotulo sale de el',
            ops and cable, 'operadores %s, con_rotulo %s' % (ops, cable))

    # 2. con Modojuego la ronda espera al primer monstruo: el reloj no corre
    W, c = S.nuevo(4)
    for k, x in enumerate(vis[::5]):
        _poner(m, W, x, 2 + k % 3)
    conchas0 = len(W['shells'])
    S.reloj[0] += 60.0                      # tres rondas enteras sin monstruo
    S.pasos(W, c, 2)
    J = W['juego']
    leg0 = m._legend_juego(W, c)
    t.check('sin monstruo la ronda no empieza: 60 s despues, ronda 0, sin entierro, el reloj entero y la leyenda '
            'lo dice; sin titulo',
            J['ronda'] == 0 and not J['gz']['corre'] and len(W['shells']) == conchas0 and J['estado'] == 'juego'
            and abs(m.tiempo_ronda(W, c, S.now) - 20.0) < 1e-9 and 'esperando al primer monstruo' in leg0
            and m.titulo_gz(W, c, S.now) is None, leg0.strip())

    # 3. aparece el primer monstruo: empieza la ronda 1 con «3, 2, 1» y «GENoZilla Begins!!!»
    _poner(m, W, a, 4)
    m.aparecer(W, c, S.now, a)
    S.semis(W, c, 1)
    t_ini = W['juego']['t0']
    tits = [m.titulo_gz(W, c, t_ini + u) for u in (0.3, 1.3, 2.3, 3.5, 3.0 + m.T_BEGINS + 0.5)]
    J = W['juego']
    t.check('el primer monstruo empieza la ronda 1 (6 min de reloj desde ahi): 3, 2, 1 y GENoZilla Begins!!!, '
            'que luego se va',
            J['ronda'] == 1 and J['gz']['corre'] and J['gz']['por'] == 'monstruo'
            and [x['texto'] if x else None for x in tits] == ['3', '2', '1', 'GENoZilla Begins!!!', None]
            and all(x['alfa'] > 0.5 for x in tits[:4]) and m.tiempo_ronda(W, c, t_ini) == 20.0,
            '%s' % [x['texto'] if x else None for x in tits])

    # 4. el mundo colapsa a mitad: entierro, la ronda cuenta y empieza otra de 6 min ya
    S.reloj[0] += 5.0
    S.semis(W, c, 1)
    conchas1 = len(W['shells'])
    ev = m.colapso_gz(W, c, S.now, 'estancado')
    J = W['juego']
    tit = m.titulo_gz(W, c, S.now + 0.5)
    t.check('el mundo colapsa a mitad de la ronda: se entierra (estancado), la ronda 1 cuenta como colapso y '
            'empieza la 2 en ese momento, con su titulo; la partida sigue',
            ev is not None and len(W['shells']) == conchas1 + 1 and J['ronda'] == 2 and J['estado'] == 'juego'
            and J['resultados'][-1].get('colapso') == 'estancado' and abs(J['t0'] - S.now) < 1e-9
            and J['gz']['colapsos'] == 1 and tit is not None and tit['texto'] == 'RONDA 2',
            'ronda %d, resultados %s, titulo %s' % (J['ronda'], J['resultados'], tit and tit['texto']))

    # 5. el fin de ciclo de la fase 6 tambien colapsa el mundo en modo juego (cycle_tick)
    W['cambio_pendiente'] = True
    W['compases_ciclo'] = 10 ** 6
    W['beats'] = float(c['beats_per_bar']) - 1e-3
    W['clock']['last_note_t'] = S.now           # el reloj del ciclo corre: hay notas recientes
    W['clock']['stop_t'] = -1e9
    ev2 = m.cycle_tick(W, c, S.now + 0.1, 0.01, 120.0, True)
    J = W['juego']
    t.check('un fin de ciclo (cambio de pattern) en modo juego tambien colapsa: ronda 3',
            ev2 is not None and J['ronda'] == 3 and J['resultados'][-1].get('colapso') == 'cambio de pattern',
            'ronda %d %s' % (J['ronda'], J['resultados'][-1]))
    W['cambio_pendiente'] = False

    # 6. los 5 s finales: estroboscopio y la cuenta 5 ... 1; a los 6 min, fin de la partida y Ends!!!
    t3 = J['t0']
    S.reloj[0] = t3 + 20.0 - 4.6
    S.semis(W, c, 1)
    q = m.final_gz(W, c, S.now)
    tq = m.titulo_gz(W, c, S.now)
    hz = m.hz_juego(W, c, False, S.now)
    antes = m.final_gz(W, c, t3 + 10.0)
    luz = []
    for k in range(int(4.0 * 60)):
        now = S.now + k / 60.0
        m.sala_luz_tick(W, c, now)
        luz.append(m.destellos_ventana(W, now))
    S.reloj[0] = t3 + 20.0 + 0.01
    fin = S.semis(W, c, 1)
    J = W['juego']
    te = m.titulo_gz(W, c, S.now + 1.0)
    rp = m.resultado_partida(J)
    leg = m._legend_juego(W, c)
    t.check('los 5 s finales: estrobo (por el limitador) y la cuenta 5 ... 1 en rojo; a los 20 s (Duracionronda) '
            'la partida acaba (no hay ronda 4 aunque Rondas sea 4) con Stratos x GENoZilla Ends!!! y quien gana',
            antes is None and q == 5 and tq is not None and tq['texto'] == '5' and hz > 0.0
            and 0 < max(luz) <= m.DESTELLOS_MAX and fin is not None and J['estado'] == 'espera'
            and te is not None and te['texto'] == 'Stratos x GENoZilla Ends!!!' and 'GANA' in te['sub']
            and rp['gana'] == J['resultados'][-1]['gana'] and 'fin GENoZilla' in leg,
            'q %s hz %.1f destellos %d fin %s | %s | %s' % (q, hz, max(luz), J['estado'], te and te['sub'],
                                                         leg.strip()))

    # 7. el colapso antes del primer monstruo empieza la ronda 1
    W, c = S.nuevo(4)
    for k, x in enumerate(vis[::5]):
        _poner(m, W, x, 2 + k % 3)
    m.colapso_gz(W, c, S.now, 'edad maxima')
    J = W['juego']
    tb = m.titulo_gz(W, c, S.now + 1.5)
    t.check('antes del primer monstruo, el colapso del mundo empieza la ronda 1 (con 3, 2, 1)',
            J['ronda'] == 1 and J['gz']['corre'] and J['gz']['por'] == 'colapso' and J['resultados'] == []
            and tb is not None and tb['texto'] == '2', 'ronda %d por %s' % (J['ronda'], J['gz'].get('por')))

    # 8. Rondagenozilla apagado: la ronda de la fase 32 (empieza con Modojuego, Rondas rondas)
    S2 = SalaJuego(base, m, absTime.seconds + 9900.0)
    W, c = S2.nuevo(4)
    S2.reloj[0] += 20.5
    S2.semis(W, c, 1)
    J = W['juego']
    t.check('Rondagenozilla apagado: la ronda de siempre (empieza con Modojuego; a los 20 s, la ronda 2) y sin '
            'titulos',
            J.get('gz') is None and J['ronda'] == 2 and J['estado'] == 'juego' and m.titulo_gz(W, c, S2.now) is None,
            'ronda %d' % J['ronda'])


    # 9. v2: lo heredado conserva su especie y cuenta en el reparto (Herenciareparto)
    def enterrar(sigue):
        c9 = m._mezcla_cfg(m.cfg(), nivel=43, herencia_reparto=sigue)
        W9 = m._mezcla_mundo(c9)
        for k, x in enumerate(range(0, m.N, 2)):
            W9['occ'][x], W9['own'][x], W9['sp'][x] = 2, m.GEO, m.GEO
            W9['tema_c'][x] = (m.NAT, m.CIU, m.IND)[k % 3]
        antes = list(m.celdas_de(W9))
        m.mezcla_enterrar(W9, c9)
        e = m.mezcla_estado(W9, c9, avanzar=False)
        return antes, list(m.celdas_de(W9)), e
    a1, d1, e1 = enterrar(1)
    a0, d0, e0 = enterrar(0)
    t.check('Herenciareparto: al enterrar, lo heredado conserva su especie (N/C/I), cuenta en el construido y el '
            'mundo nuevo empieza en su tramo; apagado, neutro y en el primer tramo, como antes',
            d1 == a1 and sum(d1) > 0 and e1['construido'] > 0.0 and abs(e1['pico'] - e1['construido']) < 1e-9
            and e1['tramo'] > 0 and d0 == [0, 0, 0] and e0['pico'] == 0.0 and e0['tramo'] == 0,
            'con: %s -> %s, construido %.0f %%, tramo %d; sin: %s, tramo %d'
            % (a1, d1, e1['construido'], e1['tramo'], d0, e0['tramo']))

    # 10. v3: el marcador (los operadores, las celdas, la ronda y los monstruos en pie)
    base.par.Marcador = True
    S3 = SalaJuego(base, m, absTime.seconds + 10400.0, rondagz=True)
    W, c = S3.nuevo(4)
    for k, x in enumerate(vis[::5]):
        _poner(m, W, x, 2 + k % 3)
    S3.semis(W, c, 1)
    M0 = m.marcador_gz(W, c, S3.now)
    rec0 = dict(W['juego']['recuento'])
    _poner(m, W, a, 4)
    mo = m.aparecer(W, c, S3.now, a)
    S3.semis(W, c, 1)
    M1 = m.marcador_gz(W, c, S3.now)
    cara, anim = m.emocion_mon(W, c, mo, S3.now)
    sh = base.op('con_titulo_sombra')
    ops = all(base.op(n) is not None for n in ('marcador_monstruos', 'marcador_pixel', 'marcador_seguro',
                                               'marcador_bien', 'marcador_mal', 'marcador_ronda', 'marcador_reloj',
                                               'con_marcador'))
    bajo_titulo = nombres_entradas(sh) if sh is not None else []
    entradas = nombres_entradas(base.op('marcador_monstruos'))
    cable = (len(bajo_titulo) > 1 and bajo_titulo[1] == 'con_marcador'
             and entradas == [n + '_atlas' for n in m.MARCADOR_MON])        # el azul, la cuarta
    vals = [m.marcador_valor(M1, q) for q in ('bien', 'mal', 'e0a', 'e0c', 'e0g', 'e0v', 'e1a', 'e1v', 'b1a',
                                                'b1g', 'b1v')]
    base.par.Marcador = False
    apagado = m.marcador_gz(W, m.cfg(), S3.now)
    t.check('el marcador: construidas y mal (el recuento), ESPERANDO sin monstruo; con Trumpzilla, RONDA 1, su '
            'reloj y su casilla con la cara y la animacion de su sprite; los operadores encima del render y '
            'debajo de los titulos; Marcador apagado, nada',
            ops and cable and M0 is not None and M0['ronda'] == 'ESPERANDO' and M0['monstruos'] == []
            and M0['publico'] == rec0['publico'] and M0['mal'] == rec0['mal'] and M1['ronda'] == 'RONDA 1'
            and M1['reloj'] == '0:20' and len(M1['monstruos']) == 1 and M1['monstruos'][0][0] == 0
            and M1['monstruos'][0][1] == m.EMOCIONES_MON.index(cara)
            and M1['monstruos'][0][2] == m.ANIMS_MON.index(anim) and M1['monstruos'][0][3] == 'mal'
            and apagado is None
            and vals == ['NATURAL EVOLUTION   %d' % M1['publico'], 'OUTBREAKS OF EVIL   %d' % M1['mal'], 0.0,
                         float(m.EMOCIONES_MON.index(cara)), float(m.ANIMS_MON.index(anim)), 1.0, 1.0, 0.0, 3.0,
                         float(m.ANIMS_MON.index('piedra')), 0.0],
            'operadores %s cable %s (con_titulo_sombra <- %s; marcador_monstruos <- %s) | %s | %s | %s'
            % (ops, cable, bajo_titulo, entradas, M0, M1, vals))


run_test(base, prueba)
print('  Ahora: Modojuego; la ronda empieza con el primer monstruo (Simmonstruo) o el colapso del mundo.')
print('  Duracionronda 20 para ver el final: estrobo, 5 ... 1 y Stratos x GENoZilla Ends!!!')
print('=' * 66)
