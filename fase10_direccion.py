"""
=============================================================================
ESTRATOS - FASE 10: DIRECCION VISUAL Y CAMARA
=============================================================================
Requiere la fase 9. Lleva el prototipo al lenguaje de la seccion III del
marco conceptual.

QUE HACE
--------
  PALETA       nucleo negro profundo, cada concha de un color (fase 8,
               Paleta; mineral para la anterior), cian solo en cicatrices.
  LUZ          cenital fria y constante (sube con el planeta), relleno
               azulado muy tenue. Eje inclinado 20 grados (Tilt).
  CAMARA       (Modocamara)
     globo       por defecto: mira al centro y encuadra el planeta entero
                 tan grande como dice Encuadre: el alto del planeta en la
                 pantalla (0,85 por defecto: queda sitio arriba y abajo para
                 lo que crece; 1 = de borde a borde). Solo cambia con una
                 concha nueva: la camara se aleja en Camsuave s
                 (amortiguado critico, travelling: el FOV no cambia) y el
                 planeta nunca se sale del cuadro. Crecer, erosionar o el
                 latido no la mueven. Fija en +Z: el giro y el balanceo del
                 planeta ensenan todas sus caras.
     superficie  la camara de la fase 10 v4: orbita lenta (Camvel) a
                 Camaltura de la superficie, mirando al horizonte.
     rasante     (v13, motor v94: TUMBADA, como flotando boca arriba: por
                 defecto mira al cenit, Rasmirada 90, con 140 grados, Rasfov,
                 a Rasaltura 0,6 del suelo mas alto de las celdas de
                 alrededor; las formaciones entran por los bordes y fugan
                 hacia el centro. Con Rasmirada 8 y Rasfov 90, la de la v12.)
                 (v12, motor v92) a ras de suelo y con gran angular. Va
                 ANCLADA al planeta (gira, se balancea y se inclina con el):
                 recorre el paralelo que separa dos anillos de celdas
                 (Rasanillo) a Rasvel grados/s (0 = tripode), a Rasaltura
                 sobre el suelo real de las celdas que tiene a los lados, y
                 mira hacia delante, Rasmirada grados sobre la horizontal.
                 Su angular es Rasfov (90); el del globo y la superficie,
                 Camfov. Las luces no giran con el planeta: desde el suelo,
                 la luz cambia con el giro.
               Desde la v12 el giro y el FOV de la camara los da el motor
               (ya no usa Look At): NO se cambia el FOV en el Camera COMP,
               sino en Camfov y Rasfov.
               Cambiar de modo en directo hace una transicion de 20 s.
               (v11: sin Planofinal: el globo ya es la camara por defecto;
               relanzar la fase lo borra de la pagina)
  ACTUACION    Modoactuacion oculta reticula y leyenda (la luz de celda se
               ve: es parte del mundo). Al
               quitarlo vuelve el modo diagnostico.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase10_direccion.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase10 v13  (camara rasante tumbada: mira al cenit con 140 grados y flota mas alta, sobre las celdas de alrededor)'
banner(VERSION)

base = require_base(10)
motor = install_core(base, CARPETA, 10)

page = get_page(base, 'Fase10')
MODOS_CAM, ROTULOS_CAM = ['globo', 'superficie', 'rasante'], ['Globo entero', 'Superficie', 'Rasante (a ras de suelo)']
add_par(base, page, 'menu', 'Modocamara', 'Camara', 'globo', menu=MODOS_CAM, menu_labels=ROTULOS_CAM)
try:                                    # v12: un proyecto con el menu de antes gana el modo rasante
    if list(base.par.Modocamara.menuNames) != MODOS_CAM:
        base.par.Modocamara.menuNames = MODOS_CAM
        base.par.Modocamara.menuLabels = ROTULOS_CAM
except Exception:
    info('no pude anadir "rasante" al menu Modocamara')
add_encuadre(base)                      # motor v36: un solo parametro de encuadre
add_par(base, page, 'float', 'Camsuave', 'Segundos para el encuadre nuevo', 3.0, 0.0, 20.0)
add_par(base, page, 'toggle', 'Modoactuacion', 'Modo actuacion (sin diagnostico)', False)
add_par(base, page, 'float', 'Camaltura', 'Altura de camara sobre la superficie (superficie)', 4.0, 0.5, 20.0)
add_par(base, page, 'float', 'Camvel', 'Velocidad de camara, grados/s (superficie)', 0.6, 0.0, 6.0)
for nm, lb in (('Camaltura', 'Altura de camara sobre la superficie (superficie)'),
               ('Camvel', 'Velocidad de camara, grados/s (superficie)')):
    try:
        getattr(base.par, nm).label = lb
    except Exception:
        pass
# v12: el FOV del globo y de superficie pasa a un parametro (antes se leia del
# Camera COMP): nace con el que tenga la camara
_fov0 = 45.0
try:
    _pf = base.op('camara').par.fov
    if not _pf.expr:
        _fov0 = float(_pf.eval())
except Exception:
    pass
if not 20.0 <= _fov0 <= 120.0:
    _fov0 = 45.0
add_par(base, page, 'float', 'Camfov', 'Angulo de vision, grados (globo y superficie)', _fov0, 20.0, 120.0)
# v13: tumbada. Los valores de la v12 (0,35 de altura, 90 de angular y mirada 8) pasan a los
# nuevos solo si no se habian tocado; los limites de los deslizadores se amplian
RASANTE_V13 = (('Rasaltura', 'Rasante: altura de ojos sobre el suelo', 0.35, motor.module.RAS_ALTURA, 0.1, 4.0),
               ('Rasfov', 'Rasante: angulo de vision, grados', 90.0, motor.module.RAS_FOV, 60.0, 160.0),
               ('Rasmirada', 'Rasante: mirada, grados sobre la horizontal (90 = al cenit)', 8.0, motor.module.RAS_MIRADA,
                -20.0, 90.0))


def rasante_al_dia(base):
    """Devuelve los parametros que han pasado del valor de la v12 al de la v13."""
    movidos = []
    for nm, rotulo, antes, ahora, lo, hi in RASANTE_V13:
        if add_par(base, page, 'float', nm, rotulo, ahora, lo, hi):
            continue
        p = getattr(base.par, nm)
        try:
            p.normMin, p.normMax, p.label = lo, hi, rotulo
        except Exception:
            pass
        if abs(float(p.eval()) - antes) < 1e-6:
            p.val = ahora
            movidos.append(nm)
    return movidos


_mov = rasante_al_dia(base)
if _mov:
    info('rasante: %s pasan a los valores de la v13 (tumbada, mirando al cenit)' % ', '.join(_mov))
add_par(base, page, 'float', 'Rasvel', 'Rasante: velocidad, grados/s (0 = tripode)', 0.5, 0.0, 6.0)
add_par(base, page, 'int', 'Rasanillo', 'Rasante: va entre el anillo de este numero y el anterior', 4, 1, 12)
ok('pagina Fase10: Modocamara (globo), Encuadre (0,85), Camsuave (3 s), Modoactuacion, '
   'Camaltura, Camvel; Camfov y rasante (Rasaltura, Rasfov, Rasmirada, Rasvel, Rasanillo)')


def quitar_planofinal(base):
    """v11: Planofinal ya no existe (la camara de globo es la de por defecto):
    en un proyecto que lo tenia se borra el parametro."""
    return has_par(base, 'Planofinal') and remove_par(base, 'Planofinal')


if quitar_planofinal(base):
    ok('Planofinal: quitado de la pagina Fase10 (la camara la gobiernan Modocamara, Camaltura y Camvel)')

# --- camara -------------------------------------------------------------------
def camara_al_motor(cam):
    """v12: rx ry rz y fov de la camara son expresiones del motor."""
    try:
        return all("cam('rot'" in getattr(cam.par, ax).expr for ax in ('rx', 'ry', 'rz')) \
            and "cam('fovcam'" in cam.par.fov.expr
    except Exception:
        return False


obj = get_or_make(base, 'nullCOMP', 'objetivo', 400, -280)
for k, ax in enumerate(('tx', 'ty', 'tz')):
    setexpr(obj, ax, "parent().op('motor').module.cam('tgt', %d, absTime.frame)" % k)
set_camera(base)                       # ahora con 'objetivo': Look At
cam = base.op('camara')
if camara_al_motor(cam):
    ok('camara: globo por defecto (mira al centro); superficie y rasante como modos; '
       'el giro y el FOV los da el motor (sin Look At)')
else:
    fail('la camara no recibe el giro o el FOV del motor: en "camara", rx ry rz = cam(\'rot\', 0 1 2) '
         'y fov = cam(\'fovcam\', 0), y Look At vacio')

# --- luces --------------------------------------------------------------------
luz = base.op('luz_principal')
setp(luz, 'tx', 0.0)
setexpr(luz, 'ty', "parent().op('motor').module.surface_radius(absTime.frame) * 2.0 + 14.0")
setp(luz, 'tz', 4.0)
setp(luz, 'dimmer', 1.15)
frias = color_luz(luz, (0.82, 0.90, 1.00))
rel = base.op('luz_relleno')
setp(rel, 'dimmer', 0.16)
frias = color_luz(rel, (0.35, 0.55, 0.80)) and frias
if not frias:
    info('no encontre el color de las luces (cr cg cb): luz_principal y luz_relleno saldran blancas')
# el relleno se aleja con el planeta (antes quedaba dentro al pasar de ~17 de
# radio) y alumbra desde abajo y por delante: la cara que ve la camara de globo
RELLENO = "parent().op('motor').module.cam('Re', 0, absTime.frame) * 2.0 + 14.0"
for ax, k in (('tx', 0.55), ('ty', -0.45), ('tz', 0.70)):
    setexpr(rel, ax, "(%s) * %.2f" % (RELLENO, k))
ok('luces: cenital fria que sube con el planeta, relleno tenue que se aleja con el')

# --- materiales -----------------------------------------------------------------
mn = base.op('mat_nucleo')
for ch in 'rgb':
    setp(mn, 'diffuse' + ch, 0.05)
setp_any(mn, ['shininess', 'specularexp'], 6)
ok('nucleo: negro profundo')

# --- modo actuacion -------------------------------------------------------------
salida = base.op('salida')
con_rot = base.op('con_rotulo') or base.op('rotulo')
render = base.op('render')
modo = fresh(base, 'switchTOP', 'modo', 860, -60)
connect(modo, con_rot if base.op('con_rotulo') is not None else render, 0)
connect(modo, render, 1)
setexpr(modo, 'index', 'int(parent().par.Modoactuacion)')
connect(salida, modo, 0)
ok('salida: con leyenda (diagnostico) o sin ella (Modoactuacion)')

set_render(base)

leeme(base, 10, """FASE 10 - DIRECCION VISUAL
  Camara de globo (Modocamara): el planeta entero y centrado; Encuadre es
  su alto en la pantalla (1 = de borde a borde). Con cada concha nueva se
  aleja en Camsuave s. Superficie: a Camaltura, orbita a Camvel grados/s.
  Rasante: a ras de suelo (Rasaltura), gran angular (Rasfov), anclada al
  planeta, por el paralelo entre dos anillos (Rasanillo) a Rasvel grados/s,
  mirando Rasmirada grados sobre la horizontal. Con Modoactuacion, sin reticula.
  Cambiar de modo hace una transicion de 20 s. El angular del globo: Camfov.
  Modoactuacion: sin reticula ni leyenda; la luz de celda se ve.
  Luz cenital fria; nucleo negro; una concha de cada color; cian en cicatrices.""")

print_report()


def prueba(t):
    import math
    m = t.m
    c = m.cfg()
    # encuadre: el planeta ocupa Encuadre del lado mas estrecho, en varios aspectos
    enc = []
    for R in (6.0, 11.5, 43.0):
        for asp in (16 / 9.0, 4 / 3.0, 1.0, 9 / 16.0):
            for met in ('horzfov', 'vertfov'):
                for k in (0.85, 1.0):
                    d, th = m.distancia_encuadre(R, 45.0, asp, k, met)
                    enc.append(abs(m.fraccion_cuadro(R, d, th) - k) < 1e-9 and th <= math.radians(45) + 1e-9)
    t.check('Encuadre: el planeta ocupa esa fraccion del lado mas estrecho (16:9, 4:3, 1:1, 9:16)', all(enc))
    t.check('altura maxima de las formaciones', m.altura_max(c) > m.limit(c), '%.3f' % m.altura_max(c))
    # camara de globo por el camino real
    m.cam_reset()
    m._CACHE.pop('cam_w', None)
    modo0 = str(base.par.Modocamara.eval())
    base.par.Modocamara = 'globo'
    st = m.camera_state()
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5
    t.check('globo: mira al centro desde +Z y el planeta ocupa Encuadre del cuadro',
            abs(p[0]) < 1e-9 and abs(p[1]) < 1e-9 and max(abs(x) for x in st['tgt']) < 1e-9
            and abs(m.fraccion_cuadro(st['Re'], dist, st['theta']) - st['encuadre']) < 1e-6,
            'dist %.2f, planeta %.2f, %d%% del cuadro' % (dist, st['Re'],
                                                         round(100 * m.fraccion_cuadro(st['Re'], dist, st['theta']))))
    t.check('planos de recorte', st['far'] >= dist + 2 * st['Re'] and 0 < st['near'] < dist - st['Re'])
    _encuadre_cercano(t, m)
    # superficie como modo (sin transicion, para medirla)
    base.par.Modocamara = 'superficie'
    m._CACHE['cam_w'] = 1.0
    m._CACHE.pop('cam_frame', None)
    st = m.camera_state()
    R = st['R']
    p = st['pos']
    dist = (p[0] ** 2 + p[1] ** 2 + p[2] ** 2) ** 0.5 - R
    t.check('superficie: camara a Camaltura de la superficie', abs(dist - float(base.par.Camaltura)) < 0.05,
            '%.2f' % dist)
    g = st['tgt']
    t.check('superficie: mira a un punto de la superficie',
            abs((g[0] ** 2 + g[1] ** 2 + g[2] ** 2) ** 0.5 - R) < 0.05)
    de_, ar_ = m.ejes_de_giro(*st['rot'])[2], m.ejes_de_giro(*st['rot'])[1]
    mira = m._norm((g[0] - p[0], g[1] - p[1], g[2] - p[2]))
    t.check('v12 superficie: el giro del motor mira al objetivo con el horizonte nivelado (como el Look At)',
            m._dot(de_, mira) > 1 - 1e-9 and ar_[1] > 0 and abs(m.ejes_de_giro(*st['rot'])[0][1]) < 1e-9)
    base.par.Modocamara = modo0
    m._CACHE.pop('cam_w', None)
    m._CACHE.pop('cam_frame', None)
    _rasante(t, m)
    t.check('leyenda CAMARA', 'CAMARA' in m.legend())
    before = bool(base.par.Modoactuacion)
    base.par.Modoactuacion = True
    m.on_value('Modoactuacion', True)
    m.reset_world()
    t.midi(0x9C, 0x40, 0x64)
    m.erosion(m.world(), m.cfg(), 0, 100, 0.0)            # el pad 1 ilumina su celda
    inst = m.build_instances(m.world(), m.cfg(), 0.1, hide_beacons=m.performance())
    t.check('modo actuacion: sin reticula; la luz de celda se ve',
            inst['luz_celda'] and 'baliza2' not in inst and not int(base.par.Showgrid))
    base.par.Modoactuacion = before
    m.on_value('Modoactuacion', before)
    t.check('al quitarlo vuelve la reticula', bool(int(base.par.Showgrid)) == (not before))


def _rasante(t, m):
    """v12 (motor v92): la camara rasante."""
    import math
    cam = base.op('camara')
    t.check('v12: la camara recibe el giro y el FOV del motor, sin Look At',
            camara_al_motor(cam) and not cam.par.lookat.eval(), 'lookat %r' % (cam.par.lookat.eval(),))
    # el giro: ida y vuelta por varias direcciones (tambien en vertical)
    bien = True
    for de, ar in (((0, 0, -1), (0, 1, 0)), ((1, 0, 0), (0, 1, 0)), ((0.3, 0.2, 0.9), (0.1, 1, -0.2)),
                   ((0, 1, 0), (0, 0, 1)), ((0, -1, 0), (1, 0, 0)), ((-0.6, 0.7, 0.1), (0.5, 0.2, -0.8)),
                   ((1, 0, 0), (0, 0, 1)), ((-1, 0, 0), (0, -1, 0))):
        rot = m.giro_camara(de, ar)
        d_, a_, f_ = m.ejes_de_giro(*rot)
        ar_o = m._norm(m._cross(m._cross(m._norm(de), ar), m._norm(de)))
        bien = bien and m._dot(f_, m._norm(de)) > 1 - 1e-9 and m._dot(a_, ar_o) > 1 - 1e-9
    t.check('v12: el giro de la camara (rx ry rz, orden xyz) mira adonde se le pide con su arriba', bien)
    modo0 = str(base.par.Modocamara.eval())
    vals0 = dict((n, float(getattr(base.par, n))) for n in ('Rasaltura', 'Rasfov', 'Rasmirada', 'Rasvel',
                                                            'Rasanillo', 'Camfov'))

    def leer(**cache):
        m._CACHE.update(cache)
        m._CACHE.pop('cam_frame', None)
        return m.camera_state()

    # globo: sin giro, y con el angular de Camfov
    base.par.Modocamara = 'globo'
    m.cam_reset()
    st = leer(cam_w=0.0, cam_wr=0.0)
    d_globo = st['d']
    t.check('v12 globo: sin giro, con el angular de Camfov',
            max(abs(x) for x in st['rot']) < 1e-9 and abs(st['fovcam'] - vals0['Camfov']) < 1e-9
            and abs(st['fov'] - vals0['Camfov']) < 1e-9, 'giro %s, fov %.1f' % (st['rot'], st['fovcam']))
    base.par.Rasfov = 110.0
    st = leer()
    t.check('v12: Rasfov no cambia el encuadre del globo', abs(st['d'] - d_globo) < 1e-9
            and abs(st['fovcam'] - vals0['Camfov']) < 1e-9)
    base.par.Rasfov = vals0['Rasfov']
    # rasante, sin transicion
    base.par.Modocamara = 'rasante'
    m._CACHE.pop('ras_g', None)
    st = leer(cam_wr=1.0)
    W, c = m.world(), m.cfg()
    rs, p = st['ras'], st['pos']
    dist = math.sqrt(m._dot(p, p))
    arriba = m._norm(p)
    ca, cb = rs['celdas']
    t.check('rasante: a Rasaltura del suelo de las celdas que tiene a los lados',
            abs(dist - rs['suelo'] - vals0['Rasaltura']) < 1e-6
            and rs['suelo'] >= max(m.suelo(W, c, ca), m.suelo(W, c, cb)) - 1e-6 and ca != cb,
            'ojos a %.2f del centro, suelo %.2f (celdas %d y %d)' % (dist, rs['suelo'], ca, cb))
    de_, ar_ = m.ejes_de_giro(*st['rot'])[2], m.ejes_de_giro(*st['rot'])[1]
    mir = math.degrees(math.asin(max(-1.0, min(1.0, m._dot(de_, arriba)))))
    t.check('rasante: mira Rasmirada grados sobre la horizontal y su arriba es la vertical del sitio',
            abs(mir - vals0['Rasmirada']) < 1e-3       # cerca de 90 el arcoseno pierde precision
            and abs(m._dot(ar_, arriba) - math.cos(math.radians(vals0['Rasmirada']))) < 1e-6
            and abs(m._dot(m.ejes_de_giro(*st['rot'])[0], arriba)) < 1e-9, 'mirada %.2f' % mir)
    t.check('rasante: el angular es Rasfov', abs(st['fovcam'] - vals0['Rasfov']) < 1e-9 and st['modo'] == 'rasante')
    t.check('rasante: planos de recorte', 0 < st['near'] < vals0['Rasaltura'] and st['far'] > dist + 2 * st['R'])
    # anclada al planeta: sobre su paralelo, gire lo que gire
    eje = m.world_dir((0.0, 1.0, 0.0), *m._giro_planeta())
    lat = math.degrees(math.asin(max(-1.0, min(1.0, m._dot(arriba, eje)))))
    t.check('rasante: anclada al planeta, sobre el paralelo entre dos anillos',
            abs(lat - rs['lat']) < 1e-6 and abs(m.paralelo_rasante(vals0['Rasanillo'])[0] - rs['lat']) < 1e-9
            and m.RING_OF[ca] != m.RING_OF[cb], 'latitud %.1f' % lat)
    n_an = len(m.RINGS)
    delante = max(m.suelo(W, c, m.celda_de_lonlat(rs['lat'] + s_, rs['lon'] + dl))
                  for s_ in (-1.0, 1.0) for dl in m.RAS_VECINAS)
    t.check('v13 rasante: flota tambien sobre el suelo de las celdas de delante y de detras',
            rs['suelo'] >= delante - 1e-6, 'suelo %.2f, alrededor %.2f' % (rs['suelo'], delante))
    base.par.Rasmirada = 90.0
    st9 = leer()
    e9 = m.ejes_de_giro(*st9['rot'])
    t.check('v13 rasante: con Rasmirada 90 mira al cenit (por defecto: altura %.1f, mirada %d, angular %d)'
            % (m.RAS_ALTURA, m.RAS_MIRADA, m.RAS_FOV),
            m._dot(e9[2], m._norm(st9['pos'])) > 1 - 1e-9 and abs(m._dot(e9[1], m._norm(st9['pos']))) < 1e-9
            and (m.RAS_ALTURA, m.RAS_MIRADA, m.RAS_FOV) == (0.6, 90.0, 140.0))
    base.par.Rasmirada = vals0['Rasmirada']
    t.check('rasante: Rasanillo fuera de rango se queda en el primer o el ultimo limite',
            m.paralelo_rasante(-3)[1] == 1 and m.paralelo_rasante(99)[1] == max(1, n_an - 1))
    # avanza por el paralelo a Rasvel; en tripode no se mueve
    base.par.Rasvel = 2.0
    lon0 = st['ras']['lon']
    st = leer(cam_t=absTime.seconds - 0.25)
    avanza = abs((st['ras']['lon'] - lon0) % 360.0 - 0.5) < 1e-6
    base.par.Rasvel = 0.0
    lon0 = st['ras']['lon']
    st = leer(cam_t=absTime.seconds - 0.25)
    t.check('rasante: avanza a Rasvel grados/s; con 0, tripode', avanza and abs(st['ras']['lon'] - lon0) < 1e-9)
    # sigue al suelo: una vuelta entera, nunca bajo tierra
    base.par.Rasvel = 6.0
    bajo = 0
    for _ in range(260):
        st = leer(cam_t=absTime.seconds - 0.25)
        rs = st['ras']
        p = st['pos']
        g = max(m.suelo(W, c, rs['celdas'][0]), m.suelo(W, c, rs['celdas'][1]))
        if math.sqrt(m._dot(p, p)) < g + 0.5 * vals0['Rasaltura'] - 1e-9:
            bajo += 1
    t.check('rasante: una vuelta entera sin quedar bajo tierra', bajo == 0, '%d fotogramas' % bajo)
    # transicion desde el globo: sin saltos, y llega
    base.par.Rasvel = 0.0
    base.par.Modocamara = 'globo'
    m.cam_reset()
    st = leer(cam_wr=0.0, cam_w=0.0)
    base.par.Modocamara = 'rasante'
    ant, salto, fovs_ = st['pos'], 0.0, []
    for _ in range(int(m.CAM_TRANS / 0.25) + 4):
        st = leer(cam_t=absTime.seconds - 0.25)
        q = st['pos']
        salto = max(salto, math.sqrt(sum((q[k] - ant[k]) ** 2 for k in range(3))))
        ant = q
        fovs_.append(st['fovcam'])
    t.check('rasante: transicion de %d s desde el globo, sin saltos; el angular se abre con ella' % m.CAM_TRANS,
            st['wr'] == 1.0 and salto < 0.08 * d_globo and all(b >= a - 1e-9 for a, b in zip(fovs_, fovs_[1:]))
            and abs(fovs_[-1] - vals0['Rasfov']) < 1e-9, 'paso mayor %.2f' % salto)
    t.check('leyenda RASANTE', 'RASANTE' in m.legend())
    for n, v in vals0.items():
        setattr(base.par, n, int(v) if n == 'Rasanillo' else v)
    base.par.Modocamara = modo0
    for k in ('cam_w', 'cam_wr', 'cam_frame', 'ras_g', 'ras_gv'):
        m._CACHE.pop(k, None)
    m.cam_reset()


def _encuadre_cercano(t, m):
    """Encuadre (motor v36): el planeta ocupa Encuadre del cuadro; solo
    cambia con una concha nueva, y entonces la camara se aleja."""
    import math
    t0 = absTime.seconds

    def paso(seg):
        m._CACHE['cam_t'] = t0 - seg           # como si hubieran pasado 'seg' segundos
        m._CACHE.pop('cam_frame', None)
        st_ = m.camera_state()
        p_ = st_['pos']
        return st_, math.sqrt(p_[0] ** 2 + p_[1] ** 2 + p_[2] ** 2)

    k0 = float(base.par.Encuadre)
    m.reset_world()
    base.par.Velprueba = 100
    base.par.Nota = 64
    m.on_pulse('Sembrar')
    W, c = m.world(), m.cfg()
    m.cam_reset()
    st, d0 = paso(0.0)
    R = m.top_radius(W, c)
    t.check('el planeta (con la reticula) ocupa Encuadre del cuadro',
            abs(st['Re'] - (R + m.RETICULA_SOBRE)) < 1e-9
            and abs(m.fraccion_cuadro(st['Re'], d0, st['theta']) - k0) < 1e-6,
            'Encuadre %.2f, dist %.2f' % (k0, d0))
    # crecer y el latido no mueven la camara
    ds = []
    for k in range(6):
        m.on_pulse('Sembrar')
        W['vh'] = list(W['h'])
        m._CACHE['inst'] = m.build_instances(W, c, t0 + k)
        ds.append(paso(0.25)[1])
    t.check('crecer no mueve la camara (sin reencuadres)', max(abs(x - d0) for x in ds) < 1e-9,
            'dist %.2f .. %.2f' % (min(ds), max(ds)))
    # una concha nueva: se aleja suave, sin saltos, y el planeta siempre cabe
    m.on_pulse('Forzarciclo')
    W = m.world()
    R2 = m.top_radius(W, c)
    cabe, ds = True, []
    for _ in range(int(4 * max(1.0, float(base.par.Camsuave)) / 0.25) + 8):
        st, d = paso(0.25)
        ds.append(d)
        cabe = cabe and m.fraccion_cuadro(R2 + m.RETICULA_SOBRE, d, st['theta']) <= 1.0 + 1e-9
    fin = m.fraccion_cuadro(R2 + m.RETICULA_SOBRE, ds[-1], st['theta'])
    t.check('concha nueva: la camara se aleja (Camsuave) hasta el mismo Encuadre; el planeta siempre cabe',
            R2 > R and cabe and d0 < ds[0] < ds[-1] and abs(fin - k0) < 0.01,
            'radio %.2f -> %.2f, dist %.2f -> %.2f -> %.2f' % (R, R2, d0, ds[0], ds[-1]))
    base.par.Encuadre = 1.0
    m.cam_reset()
    st, d1 = paso(0.0)
    t.check('Encuadre 1: el planeta de borde a borde', abs(m.fraccion_cuadro(st['Re'], d1, st['theta']) - 1.0) < 1e-6)
    base.par.Encuadre = k0
    t.check('sin Encuadremargen ni Holguraaltura (un solo parametro)',
            not has_par(base, 'Encuadremargen') and not has_par(base, 'Holguraaltura'))
    # v11: relanzar la fase sobre un proyecto que tenia Planofinal lo borra
    if not has_par(base, 'Planofinal'):
        get_page(base, 'Fase10').appendToggle('Planofinal', label='Plano final (v10)')
    tenia = has_par(base, 'Planofinal')
    quitar_planofinal(base)
    t.check('sin Planofinal: relanzar la fase sobre un proyecto que lo tenia borra el parametro',
            tenia and not has_par(base, 'Planofinal') and m._p('Planofinal', None) is None)
    m.cam_reset()


run_test(base, prueba)
print('  Listo: el sistema completo.')
print('  Para actuar: Modoactuacion.')
print('  Ajustes de encuadre: Encuadre (alto del planeta), Camsuave y Tilt; en superficie,')
print('  Camaltura y Camvel.')
print('=' * 66)
