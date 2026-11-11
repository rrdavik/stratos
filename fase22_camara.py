"""
=============================================================================
ESTRATOS - FASE 22: LA CAMARA CENITAL (CASILLA PROBABLE)
=============================================================================
Requiere la fase 21. Una camara de profundidad en el techo (Orbbec Femto Bolt)
mide cuanta gente hay en cada casilla del suelo, y esa densidad inclina la
probabilidad de que cada senal que llega al planeta actue. El publico no
escribe: solo inclina donde prende lo que ya llega. Es el componente
'presencia' de la "Especificacion TouchDesigner: casilla probable", dentro de
FASE1 y con sus parametros en la pagina Fase22.

QUE HACE
--------
  LA FORMULA   P(c) = C + (1 - C) k d(c).  C = Cuanto (la probabilidad con la
               sala vacia; 0,5 como mucho, tambien en el codigo), k =
               Pesocrear o Pesoerosion, d(c) = la densidad (0-1) de la casilla
               a la que mira la celda. Con Activo apagado, P = 1: el mundo se
               comporta como antes de esta fase.
  EL SORTEO    cada nota constructora del SEQ1 o del SEQ2 (crear) y cada golpe
               de erosion u onset del microfono (erosionar) pasa por un
               sorteo, una vez por evento y en su centro. Si no sale, el
               evento se pierde sin rastro. No hay azar de software: el sorteo
               sale del mapa logistico (celda, tipo y contador de senales): la
               misma sala da el mismo resultado. El bombo y el tom (impulso) no
               se sortean (decision abierta de la especificacion).
  LA DENSIDAD  de la imagen de alturas sobre el suelo: cuerpos entre Alturamin
               y Alturamax, repartidos en un radio de Desenfoque, en casillas
               de Tamcasilla (Anchosala x Fondosala: 11 x 9); una casilla con
               Ocupacionllena de su suelo ocupado esta llena. Sube con Subida
               y baja con Bajada.
  EL MAPEO     la pared de la pantalla es el norte (Latnorte) y el fondo de la
               sala el sur (Latsur); el ancho de la sala cubre Anchoangular
               alrededor de Loncentral, que sigue al giro del planeta: la sala
               cae siempre en la cara visible. La izquierda de la sala, a la
               izquierda de la cara visible; Espejo lo invierte.
  MICROFONO    desde esta fase, un onset cae en la celda que mira a la casilla
               con mas densidad (sin nadie, como los pads), y pasa por el
               sorteo como senal erosiva.
  LEYENDA      CAMARA  femto 30 fps   casillas 4/99   densidad max 0.82
               (casilla 17 -> celda 40)   prendidas 312/598

OPERADORES (en /project1/FASE1)
-------------------------------
  orbbec1      Orbbec TOP: la Femto Bolt (profundidad en metros, NFOV binned
               320 x 288, 30 fps).
  cornerpin1   Corner Pin TOP: endereza y recorta el suelo cubierto, con la
               pared de la pantalla arriba. Sus esquinas se fijan a mano en la
               calibracion (cuatro marcas en el suelo).
  fondo        Movie File In TOP: el suelo vacio (Archivofondo), que graba
               Capturarfondo de la salida de cornerpin1.
  altura_cam   GLSL TOP: la altura de cada pixel = suelo vacio - profundidad.
  sala_personas, sala_sim
               la sala simulada: una tabla de personas (x, y, altura en m) y
               el Script TOP que las dibuja como discos de 25 cm de radio en
               la MISMA imagen de alturas que da la camara.
  fuente       Switch TOP: la camara o la sala simulada (Fuente).
  alturas_sala Resolution TOP: la imagen a 10 pixeles por casilla (unos 5 cm).
               Es lo unico que pasa a Python, 30 veces por segundo; la mascara,
               el desenfoque, la rejilla y el suavizado los hace el motor con
               numpy (asi se prueban fuera de TouchDesigner, y la fase 24 lee
               las cabezas de la misma imagen sin una segunda lectura).
  densidad     Script TOP: la densidad de cada casilla (11 x 9), para mirarla.

PROBAR SIN CAMARA
-----------------
  Fuente = simulada. Simcasilla (0 = junto a la pantalla, a la izquierda; 98 =
  al fondo, a la derecha) y Simponer: una persona en esa casilla; su densidad
  sube en unos 2 s y la leyenda dice a que celda mira. Simquitar la saca y
  Simvaciar vacia la sala. Para llenar una casilla hacen falta varias personas
  cerca (o bajar Desenfoque y Ocupacionllena).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase22_camara.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase22 v1  (camara cenital: densidad por casilla y sorteo de cada senal)'
banner(VERSION)

base = require_base(22)
motor = install_core(base, CARPETA, 22)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase22)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase22')
# probabilidad
add_par(base, page, 'toggle', 'Activo', 'Presencia activa (apagado: todo prende)', True)
add_par(base, page, 'float', 'Cuanto', 'Probabilidad con la sala vacia', 0.5, 0.0, 0.5, clamp=True)
add_par(base, page, 'float', 'Pesocrear', 'Peso de la presencia al construir', 1.0, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Pesoerosion', 'Peso de la presencia al erosionar', 1.0, 0.0, 1.0, clamp=True)
add_par(base, page, 'pulse', 'Reiniciarcuentas', 'Reiniciar contadores')
# captacion
add_par(base, page, 'menu', 'Fuente', 'De donde llega la sala', 'camara',
        menu=list(m.FUENTES_SALA), menu_labels=['Camara', 'Simulada'])
add_par(base, page, 'float', 'Alturamin', 'Altura minima de un cuerpo (m)', 0.8, 0.0, 2.0, clamp=True)
add_par(base, page, 'float', 'Alturamax', 'Altura maxima de un cuerpo (m)', 2.2, 1.0, 3.0, clamp=True)
add_par(base, page, 'pulse', 'Capturarfondo', 'Capturar el suelo vacio')
add_par(base, page, 'str', 'Archivofondo', 'Archivo del suelo vacio', 'fondo_suelo.exr')
# rejilla
add_par(base, page, 'float', 'Anchosala', 'Ancho del suelo cubierto (m)', 5.4, 1.0, 20.0)
add_par(base, page, 'float', 'Fondosala', 'Fondo del suelo cubierto (m)', 4.5, 1.0, 20.0)
add_par(base, page, 'float', 'Tamcasilla', 'Lado de casilla (m)', 0.5, 0.25, 1.0, clamp=True)
add_par(base, page, 'float', 'Desenfoque', 'Radio de reparto (m)', 1.0, 0.0, 2.0, clamp=True)
add_par(base, page, 'float', 'Ocupacionllena', 'Suelo ocupado de una casilla llena', 0.6, 0.1, 1.0, clamp=True)
add_par(base, page, 'float', 'Subida', 'Densidad: subida (s)', 2.0, 0.0, 20.0, clamp=True)
add_par(base, page, 'float', 'Bajada', 'Densidad: bajada (s)', 5.0, 0.0, 20.0, clamp=True)
# mapeo sala -> planeta
LON_EXPR = "me.op('motor').module.lon_central(absTime.frame)"
if add_par(base, page, 'float', 'Loncentral', 'Longitud central (sigue al giro)', 0.0, -180.0, 180.0):
    if setexpr(base, 'Loncentral', LON_EXPR):
        ok('Loncentral: enlazada al giro del planeta (la sala cae siempre en la cara visible)')
    else:
        fail('Loncentral: no pude enlazarla al giro; pon la expresion %s' % LON_EXPR)
add_par(base, page, 'float', 'Anchoangular', 'Longitudes que cubre el ancho de la sala', 180.0, 0.0, 360.0,
        clamp=True)
add_par(base, page, 'float', 'Latnorte', 'Latitud de la pared de la pantalla', 90.0, -90.0, 90.0, clamp=True)
add_par(base, page, 'float', 'Latsur', 'Latitud del fondo de la sala', -90.0, -90.0, 90.0, clamp=True)
add_par(base, page, 'toggle', 'Espejo', 'Invertir izquierda y derecha', False)
# sala simulada
add_par(base, page, 'int', 'Simcasilla', 'Probar: casilla (0 = pantalla, izquierda)', 0, 0, 98)
add_par(base, page, 'pulse', 'Simponer', 'Probar: poner una persona')
add_par(base, page, 'pulse', 'Simquitar', 'Probar: quitarla')
add_par(base, page, 'pulse', 'Simvaciar', 'Probar: vaciar la sala')
ok('pagina Fase22: Activo, Cuanto 0,5 (tope 0,5), Pesocrear 1, Pesoerosion 1, Reiniciarcuentas; '
   'Fuente (camara), Alturamin 0,8, Alturamax 2,2, Capturarfondo, Archivofondo; Anchosala 5,4, '
   'Fondosala 4,5, Tamcasilla 0,5, Desenfoque 1, Ocupacionllena 0,6, Subida 2, Bajada 5; Loncentral '
   '(giro), Anchoangular 180, Latnorte 90, Latsur -90, Espejo; Simcasilla, Simponer, Simquitar, Simvaciar')

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

ALTURA_PIXEL = r'''// GLSL TOP 'altura_cam' (fase 22): la altura sobre el suelo de cada pixel.
// Entrada 0: la profundidad enderezada (cornerpin1, en metros). Entrada 1: el
// suelo vacio (fondo). La Femto Bolt da la profundidad en Z, asi que con la
// camara en vertical la resta es la altura de lo que hay encima. Los pixeles
// sin dato valen 0 y se descartan.
out vec4 fragColor;
void main()
{
    float cur = texture(sTD2DInputs[0], vUV.st).r;
    float bg  = texture(sTD2DInputs[1], vUV.st).r;
    float h = (cur > 0.0 && bg > 0.0) ? max(0.0, bg - cur) : 0.0;
    fragColor = TDOutputSwizzle(vec4(h, h, h, 1.0));
}
'''

SALA_SIM_CB = r'''# Script TOP 'sala_sim' (fase 22): la sala simulada. Dibuja las personas de la
# tabla sala_personas (x, y, altura en metros) como discos en la misma imagen
# de alturas que da la camara (el motor: sala_sim_cook).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.sala_sim_cook(scriptOp)
'''

DENSIDAD_CB = r'''# Script TOP 'densidad' (fase 22): la densidad (0-1) de cada casilla, para
# mirarla. La fila de arriba es la pared de la pantalla.


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.densidad_cook(scriptOp)
'''

FORMATOS_FLOAT = ['mono32float', 'r32float', 'rgba32float']


def intenta(optype, name, x, y):
    """Como get_or_make, pero si esta version de TouchDesigner no tiene el
    operador devuelve None (y el informe lo dice)."""
    try:
        return get_or_make(base, optype, name, x, y)
    except Exception as e:
        info('%s: no pude crear un %s (%s)' % (name, optype, e))
        return None


X0, Y0 = -1320, 1100
orbbec = intenta('orbbecTOP', 'orbbec1', X0, Y0)
if orbbec is not None:
    setp_any(orbbec, ['active'], True)
    if not setmenu(orbbec, ['image'], ['depth']):
        info('orbbec1: no pude elegir la imagen de profundidad; pon Image = Depth')
    if not setmenu(orbbec, ['depthres', 'depthmode', 'depthresolution'],
                   ['nfov2x2binned', 'nfov_2x2binned', 'nfovbinned', '320x288']):
        info('orbbec1: elige a mano la profundidad NFOV binned (320 x 288)')
    setp_any(orbbec, ['fps'], 30)
pin = intenta('cornerpinTOP', 'cornerpin1', X0 + 220, Y0)
if pin is not None:
    if orbbec is not None:
        connect(pin, orbbec, 0)
    setmenu(pin, ['format'], FORMATOS_FLOAT)
fondo = intenta('moviefileinTOP', 'fondo', X0 + 220, Y0 - 140)
if fondo is not None:
    setexpr(fondo, 'file', "parent().par.Archivofondo")
px = get_or_make(base, 'textDAT', 'altura_cam_pixel', X0 + 440, Y0 + 140)
px.text = ALTURA_PIXEL
alt = intenta('glslTOP', 'altura_cam', X0 + 440, Y0)
if alt is not None:
    setp_any(alt, ['pixeldat'], 'altura_cam_pixel')
    setmenu(alt, ['format'], FORMATOS_FLOAT)
    if pin is not None:
        connect(alt, pin, 0)
    if fondo is not None:
        connect(alt, fondo, 1)

tabla = get_or_make(base, 'tableDAT', 'sala_personas', X0 + 220, Y0 - 300)
if tabla.numRows == 0:
    tabla.appendRow(list(m.SALA_COLS))
cb = get_or_make(base, 'textDAT', 'sala_sim_callbacks', X0 + 440, Y0 - 440)
cb.text = SALA_SIM_CB
sim = get_or_make(base, 'scriptTOP', 'sala_sim', X0 + 440, Y0 - 300)
setp_any(sim, ['callbacks', 'callbackdat', 'dat'], 'sala_sim_callbacks')
setmenu(sim, ['format'], FORMATOS_FLOAT)

fuente = get_or_make(base, 'switchTOP', 'fuente', X0 + 660, Y0)
if alt is not None:
    connect(fuente, alt, 0)
connect(fuente, sim, 1 if alt is not None else 0)
if alt is not None:
    setexpr(fuente, 'index', "parent().par.Fuente.menuIndex")
else:
    info('sin altura_cam: fuente solo tiene la sala simulada')

res = get_or_make(base, 'resolutionTOP', 'alturas_sala', X0 + 880, Y0)
connect(res, fuente, 0)
if not setmenu(res, ['outputresolution'], ['custom']):
    info('alturas_sala: pon Output Resolution = Custom')
setp_any(res, ['resmult'], False)
bien = setexpr(res, 'resolutionw', "parent().op('motor').module.px_sala(0, absTime.frame)")
bien = setexpr(res, 'resolutionh', "parent().op('motor').module.px_sala(1, absTime.frame)") and bien
if not bien:
    info('alturas_sala: no pude fijar la resolucion (10 pixeles por casilla)')
if not setmenu(res, ['inputfiltertype'], ['mipmap']):
    info('alturas_sala: pon Input Smoothness = Mipmap Pixels')
setmenu(res, ['format'], FORMATOS_FLOAT)

cb = get_or_make(base, 'textDAT', 'densidad_callbacks', X0 + 1100, Y0 + 140)
cb.text = DENSIDAD_CB
dens = get_or_make(base, 'scriptTOP', 'densidad', X0 + 1100, Y0)
setp_any(dens, ['callbacks', 'callbackdat', 'dat'], 'densidad_callbacks')
setmenu(dens, ['format'], FORMATOS_FLOAT)
ok('orbbec1 -> cornerpin1 -> altura_cam (con fondo) -> fuente (o sala_sim) -> alturas_sala: '
   'el motor lee la imagen de alturas 30 veces por segundo; densidad la ensena')

cols, filas = m.rejilla_sala(m.cfg())
hay, texto = m.camara_encontrada()
if hay:
    ok('camara: %s, %g fps; rejilla de %d x %d casillas' % (texto, m.CAM_FPS, cols, filas))
else:
    info('camara: no encuentro ninguna (%s). Rejilla de %d x %d casillas. Sin camara: Fuente = '
         'simulada y Simponer' % (texto, cols, filas))

set_render(base)

leeme(base, 22, """FASE 22 - LA CAMARA CENITAL (CASILLA PROBABLE)
  La densidad de gente de cada casilla del suelo inclina la probabilidad de
  que cada senal actue: P = Cuanto + (1 - Cuanto) x peso x densidad. Cada nota
  constructora y cada golpe de erosion u onset pasa por el sorteo (mapa
  logistico, sin azar); si no sale, se pierde. Activo apagado: todo prende.
  orbbec1 -> cornerpin1 -> altura_cam (suelo vacio - profundidad) -> fuente
  (o sala_sim) -> alturas_sala; el motor saca la densidad (Alturamin,
  Alturamax, Desenfoque, Tamcasilla, Ocupacionllena, Subida, Bajada).
  Mapeo: pantalla = norte, fondo = sur, ancho = Anchoangular alrededor de
  Loncentral (sigue al giro); Espejo invierte izquierda y derecha.
  El microfono va a la celda de la casilla mas densa. Capturarfondo graba el
  suelo vacio. Sin camara: Fuente = simulada, Simcasilla y Simponer.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS22 = ('Activo', 'Cuanto', 'Pesocrear', 'Pesoerosion', 'Fuente', 'Alturamin', 'Alturamax', 'Anchosala',
          'Fondosala', 'Tamcasilla', 'Desenfoque', 'Ocupacionllena', 'Subida', 'Bajada', 'Anchoangular',
          'Latnorte', 'Latsur', 'Espejo', 'Simcasilla', 'Nota', 'Velprueba', 'Objetivo', 'Umbraldensidad')


def prueba(t):
    m = t.m
    guarda = {}
    for nm in PARS22:
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    tb = base.op('sala_personas')
    filas0 = [[c.val for c in tb.row(r)] for r in range(tb.numRows)]
    try:
        _prueba(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass
        tb.clear()
        for f in filas0:
            tb.appendRow(f)
        m.sala_reset()
        m.mic_reset()


def _prueba(t, m):
    np = m._np()
    base.par.Activo = True
    base.par.Fuente = 'simulada'
    base.par.Velprueba = 100
    base.par.Umbraldensidad = 0.95
    base.par.Objetivo = 'seq1'
    reloj = [absTime.seconds + 200.0]
    tb = base.op('sala_personas')

    def vaciar():
        tb.clear()
        tb.appendRow(list(m.SALA_COLS))

    def nuevo():
        m.reset_world()
        m.sala_reset()
        m.mic_reset()
        vaciar()
        return m.world(), m.cfg()

    def imagenes(W, c, seg):
        """seg segundos de camara (30 imagenes por segundo) por la cadena
        sala_sim -> fuente -> alturas_sala -> motor."""
        d = None
        for _ in range(max(1, int(round(seg * m.CAM_FPS)))):
            reloj[0] += 1.0 / m.CAM_FPS
            m._SALA['t_img'] = -99.0
            d = m.sala_tick(W, c, reloj[0])
        return d

    W, c = nuevo()
    cols, filas = m.rejilla_sala(c)
    t.check('rejilla: 5,4 x 4,5 m en casillas de 0,5 m son 11 x 9', (cols, filas) == (11, 9), '%d x %d' % (cols, filas))

    # 1. una persona junto a la pantalla, en el centro: fila 0, columna central
    centro = cols // 2
    base.par.Simcasilla = centro
    m.on_pulse('Simponer')
    d = imagenes(W, m.cfg(), 3.0)
    k = int(d.argmax()) if d is not None else -1
    t.check('Simponer llega por la imagen de sala_sim (no escribiendo densidades): una persona junto a la '
            'pantalla, en el centro, da densidad en la fila 0 y la columna central',
            d is not None and tb.numRows == 2 and k // cols == 0 and k % cols == centro and d.max() > 0.01
            and m._SALA['alt'] is not None and m._SALA['alt'].shape == (filas * m.PX_CASILLA, cols * m.PX_CASILLA),
            'casilla %d, densidad %.3f' % (k, d.max() if d is not None else 0))

    # 2. izquierda de la sala -> izquierda de la cara visible; con Espejo, derecha
    def lado(casilla):
        cf = m.cfg()
        i = m.celda_de_casilla(m.world(), cf, casilla)
        ry = cf['lon_central'] - 90.0
        return m.world_dir(m.normal_i(i), ry, 0.0)[0], i       # x en el mundo: < 0 a la izquierda de la camara
    izq = (filas // 2) * cols + 1                               # a media sala, a la izquierda
    der = (filas // 2) * cols + cols - 2
    xi, ci = lado(izq)
    xd, cd = lado(der)
    base.par.Espejo = True
    xi2, _ = lado(izq)
    base.par.Espejo = False
    t.check('una persona a la izquierda de la sala cae en la mitad izquierda de la cara visible; a la '
            'derecha, en la derecha; con Espejo, al reves',
            xi < -0.1 and xd > 0.1 and xi2 > 0.1, 'x %.2f y %.2f; con Espejo %.2f' % (xi, xd, xi2))
    cf = m.cfg()
    vuelta = m.casilla_de_celda(cf, ci)
    t.check('la celda que mira a una casilla vuelve a una casilla de su zona',
            vuelta is not None and abs(vuelta % cols - izq % cols) <= 2 and abs(vuelta // cols - izq // cols) <= 2,
            'casilla %d -> celda %d -> casilla %s' % (izq, ci, vuelta))
    lon0 = cf['lon_central']
    cf2 = dict(cf)
    cf2['lon_central'] = lon0 + 90.0
    t.check('Loncentral sigue al giro: con el planeta girado, la misma casilla mira a otra celda',
            m.celda_de_casilla(W, cf2, izq) != ci and 'lon_central' in base.par.Loncentral.expr,
            'expresion: %s' % base.par.Loncentral.expr)

    # 3. sala vacia: P = Cuanto en cualquier celda; casilla llena y peso 1: P = 1 en sus celdas
    W, c = nuevo()
    imagenes(W, c, 0.2)
    ps = [m.presencia_prob(W, c, i, tp) for i in range(m.N) for tp in m.TIPOS_SENAL]
    t.check('con la sala vacia la probabilidad es Cuanto (0,5) en cualquier celda',
            all(abs(p - 0.5) < 1e-9 for p in ps))
    celda = next(i for i in range(m.N) if m.casilla_de_celda(c, i) is not None)
    kc = m.casilla_de_celda(c, celda)
    m._SALA['dens'] = np.zeros((filas, cols))
    m._SALA['dens'][kc // cols, kc % cols] = 1.0
    otra = next(i for i in range(m.N) if m.casilla_de_celda(c, i) not in (None, kc))
    base.par.Pesocrear = 0.5
    cm = m.cfg()
    t.check('con una casilla llena y peso 1 la probabilidad es 1 en sus celdas (con peso 0,5: 0,75), y '
            'Cuanto en las demas',
            abs(m.presencia_prob(W, c, celda, 'crear') - 1.0) < 1e-9
            and abs(m.presencia_prob(W, cm, celda, 'crear') - 0.75) < 1e-9
            and abs(m.presencia_prob(W, cm, celda, 'erosionar') - 1.0) < 1e-9
            and abs(m.presencia_prob(W, c, otra, 'crear') - 0.5) < 1e-9)
    base.par.Pesocrear = 1.0

    # 4. Cuanto no pasa de 0,5
    base.par.Cuanto = 0.8
    c8 = dict(m.cfg())
    en_par = float(base.par.Cuanto.eval())
    c8['cuanto'] = 0.8
    m.sala_reset()
    t.check('Cuanto 0,8 se queda en 0,5, en el parametro y en el codigo',
            abs(en_par - 0.5) < 1e-9 and abs(m.presencia_prob(W, c8, 0, 'crear') - 0.5) < 1e-9, '%.2f' % en_par)
    base.par.Cuanto = 0.5

    # 5. el sorteo: ronda Cuanto con la sala vacia, y la misma sala da lo mismo
    def tanda(cf, n=600):
        m.sala_reset()
        return [m.presencia_sortear(W, cf, (7 * j) % m.N, m.TIPOS_SENAL[j % 2]) for j in range(n)]
    c = m.cfg()
    a, b = tanda(c), tanda(c)
    frac = sum(a) / float(len(a))
    cu = m._SALA['cuentas']
    t.check('tras 600 senales con la sala vacia las prendidas rondan Cuanto (0,45 a 0,55); la misma sala da '
            'el mismo resultado; los contadores las cuentan',
            0.45 <= frac <= 0.55 and a == b and cu['crear'][0] + cu['erosionar'][0] == 600
            and cu['crear'][1] + cu['erosionar'][1] == sum(a), 'prendidas %.3f' % frac)
    base.par.Cuanto = 0.2
    f2 = sum(tanda(m.cfg())) / 600.0
    base.par.Cuanto = 0.5
    base.par.Activo = False
    f3 = sum(tanda(m.cfg())) / 600.0
    rec_off = m._SALA['cuentas']['crear'][0]
    base.par.Activo = True
    t.check('con Cuanto 0,2 prende en torno al 20 %; con Activo apagado, todo (y no cuenta)',
            0.15 <= f2 <= 0.25 and f3 == 1.0 and rec_off == 0, '%.3f y %.3f' % (f2, f3))
    m.on_pulse('Reiniciarcuentas')
    t.check('Reiniciarcuentas pone los contadores a cero',
            m._SALA['cuentas'] == dict(crear=[0, 0], erosionar=[0, 0]) and m._SALA['senales'] == 0)

    # 6. subida y bajada (sin desenfoque: una persona llena su casilla)
    W, c = nuevo()
    base.par.Desenfoque = 0.0
    base.par.Simcasilla = 2 * cols + 3
    m.on_pulse('Simponer')
    c = m.cfg()
    d1 = imagenes(W, c, 2.0)[2, 3]                  # tras Subida s: 1 - 1/e
    d2 = imagenes(W, c, 12.0)[2, 3]
    m.on_pulse('Simquitar')
    d3 = imagenes(W, c, 5.0)[2, 3]                  # tras Bajada s: 1/e
    d4 = imagenes(W, c, 60.0)[2, 3]
    t.check('al entrar una persona su casilla sube en torno a Subida (2 s); al irse, baja en torno a Bajada (5 s)',
            0.55 <= d1 <= 0.72 and d2 > 0.98 and 0.28 <= d3 <= 0.45 and d4 == 0.0 and tb.numRows == 1,
            '%.2f a los 2 s, %.2f; %.2f a los 5 s de irse, %.2f' % (d1, d2, d3, d4))
    bajo = m.sala_sim_imagen(c, [[1.0, 1.0, 0.6], [3.0, 1.0, 2.6]])
    t.check('lo que no llega a Alturamin (una mochila) o pasa de Alturamax (una lampara) no cuenta',
            float(m.ocupacion_sala(np, c, bajo).max()) == 0.0)
    base.par.Desenfoque = 1.0

    # 7. el sorteo envuelve las notas y los golpes de erosion; el bombo no
    W, c = nuevo()
    imagenes(W, c, 0.2)
    base.par.Nota = 64
    celda = m.note_cell(64)
    n = 200
    for _ in range(n):
        m.note_on(W, c, m.GEO, 64, 100, reloj[0])
    notas = m._SALA['cuentas']['crear']
    base.par.Activo = False
    W2, c2 = nuevo()
    for _ in range(n):
        m.note_on(W2, c2, m.GEO, 64, 100, reloj[0])
    occ_todo = W2['occ'][celda]
    base.par.Activo = True
    W = m.world()
    t.check('cada nota constructora pasa por el sorteo: con la sala vacia prende la mitad y el mundo crece '
            'menos; con Activo apagado, como antes',
            notas[0] == n and 0.4 * n <= notas[1] <= 0.6 * n and occ_todo > 0,
            'prendidas %d de %d; ocupacion con todo %d' % (notas[1], n, occ_todo))
    W, c = nuevo()
    imagenes(W, c, 0.2)
    for _ in range(30):
        m.on_pulse('Sembrar')
    W = m.world()
    c = m.cfg()
    m.reiniciar_cuentas()
    pads_e = [k for k in range(8) if not m.es_impulso(c, k)]
    pads_i = [k for k in range(8) if m.es_impulso(c, k)]
    evs = [m.erosion(W, c, pads_e[0], 100, reloj[0]) for _ in range(100)]
    perdidos = sum(1 for e in evs if e.get('prende') is False)
    ero = list(m._SALA['cuentas']['erosionar'])
    for _ in range(20):
        m.erosion(W, c, pads_i[0], 100, reloj[0])
    t.check('cada golpe de erosion pasa por el sorteo, una vez (si no prende, no quita nada); el bombo '
            '(impulso) no se sortea',
            ero[0] == 100 and perdidos == 100 - ero[1] and 35 <= perdidos <= 65
            and all(e['quitado'] == 0 for e in evs if e.get('prende') is False)
            and m._SALA['cuentas']['erosionar'] == ero, 'perdidos %d de 100' % perdidos)

    # 8. el microfono, a la celda de la casilla mas densa
    W, c = nuevo()
    base.par.Simcasilla = 4 * cols + 8
    m.on_pulse('Simponer')
    c = m.cfg()
    imagenes(W, c, 3.0)
    kd, dd = m.casilla_mas_densa(c)
    esperada = m.celda_de_casilla(W, c, kd)
    base.par.Cuanto = 0.5
    ev = None
    for _ in range(12):
        ev = m.erosion_mic(W, c, reloj[0], 1.0)
        if ev.get('prende') is not False:
            break
    t.check('desde la fase 22 un onset cae en la celda que mira a la casilla con mas densidad',
            kd == 4 * cols + 8 and ev is not None and ev['celda'] == esperada,
            'casilla %s -> celda %s; onset en %s' % (kd, esperada, ev['celda'] if ev else '-'))
    leg = m.legend()
    t.check('leyenda CAMARA', 'CAMARA   simulada' in leg and 'densidad max' in leg and 'prendidas' in leg
            and 'casilla %d -> celda %d' % (kd, esperada) in leg)
    base.par.Fuente = 'camara'
    W, c = nuevo()
    d = imagenes(W, m.cfg(), 0.5)
    t.check('sin camara (Fuente = camara y ningun aparato): densidad 0 y la leyenda lo dice',
            d is not None and float(d.max()) == 0.0 and 'sin camara' in m.legend())
    base.par.Fuente = 'simulada'
    m.on_pulse('Capturarfondo')
    t.check('operadores: cornerpin1, fondo, altura_cam, sala_sim, fuente, alturas_sala y densidad',
            all(base.op(nm) is not None for nm in ('sala_sim', 'fuente', 'alturas_sala', 'densidad',
                                                   'sala_personas')))


run_test(base, prueba)
print('  Ahora: sin camara, Fuente = simulada, Simcasilla y Simponer (la leyenda CAMARA dice')
print('  la casilla mas densa y su celda). Con la camara: ajusta las esquinas de cornerpin1')
print('  sobre cuatro marcas del suelo y pulsa Capturarfondo con la sala vacia.')
print('=' * 66)
