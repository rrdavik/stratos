"""
=============================================================================
ESTRATOS - PIEZAS COMUNES DE LAS FASES 3 A 10
=============================================================================
No se ejecuta solo: lo carga cada script de fase. Contiene:

  - utilidades para crear nodos y parametros (las mismas de fase12_base.py)
  - install_core(): instala o refresca el 'motor' y los DAT que lo usan
    (midi_callbacks, latido, reticula_callbacks, formas_callbacks, pulsos)
    y la luz de celda (luz_celda). Todas las fases lo llaman: relanzar una
    fase deja siempre el motor al dia. Tambien retira las balizas de
    versiones anteriores (baliza, baliza2, balizas_drum, luz_drum).
  - make_instanced(): un Geometry COMP alimentado por un Script CHOP del motor
  - set_render(), set_legend(), autoprueba
=============================================================================
"""

import td
import copy

VERSION_COMUN = 'comun v15'
COMP_PATH = '/project1/FASE1'

RENDER_ORDER = ['nucleo', 'estratos', 'reticula', 'formas_porosas', 'formas_pulidas',
                'coronas', 'luz_celda']
LIGHT_ORDER = ['luz_principal', 'luz_relleno', 'luz_destello']


# -----------------------------------------------------------------------------
# INFORME
# -----------------------------------------------------------------------------

report = []
def ok(m):   report.append('  OK    ' + m)
def fail(m): report.append('  FALLO ' + m)
def info(m): report.append('  ..    ' + m)


def banner(version):
    print('=' * 66)
    print('EJECUTANDO: ' + version)
    print('=' * 66)


def print_report():
    print('CAMBIOS')
    print('-' * 66)
    for line in report:
        print(line)
    print()
    try:
        diagnostico_render(op(COMP_PATH))
    except Exception as e:
        print('  (no pude hacer el diagnostico del render: %s)' % e)


def _errs(o):
    out = []
    for fn in ('errors', 'scriptErrors'):
        try:
            e = getattr(o, fn)()
            if e:
                out.append(str(e).strip())
        except Exception:
            pass
    return ' | '.join(out)


def diagnostico_render(base):
    """Que dibuja el render y que nodos de la cadena tienen errores."""
    print('DIAGNOSTICO DEL RENDER')
    print('-' * 66)
    r = base.op('render')
    try:
        geo = str(r.par.geometry.val)
        print('  render geometria : %r' % geo)
        print('  render camara    : %r   luces: %r' % (r.par.camera.val, r.par.lights.val))
    except Exception as e:
        geo = ''
        print('  FALLO  no pude leer el render: %s' % e)
    for nm in geo.split():
        g = base.op(nm)
        if g is None:
            print('  FALLO  %-15s no existe' % nm)
            continue
        e = _errs(g)
        if e:
            print('  FALLO  %-15s %s' % (nm, e))
    malos = []
    for nm in ['motor', 'latido', 'ritmo', 'reticula_chop', 'formas_callbacks',
               'i_formas_pulidas', 'i_formas_porosas', 'i_coronas', 'i_estratos',
               'i_luz_celda', 'camara', 'render', 'rotulo', 'con_rotulo', 'salida']:
        o = base.op(nm)
        if o is None:
            continue
        try:
            o.cook(force=True)
        except Exception:
            pass
        e = _errs(o)
        if e:
            malos.append((nm, e))
    for nm, e in malos:
        print('  FALLO  %-15s %s' % (nm, e))
    if not malos:
        print('  OK     ningun nodo de la cadena hasta salida tiene errores')
    try:
        if not base.op('ritmo').module.playing():
            print('  AVISO  linea de tiempo PARADA: las formaciones no brotan hasta darle a play')
    except Exception:
        pass
    print('-' * 66)


# -----------------------------------------------------------------------------
# NODOS Y PARAMETROS
# -----------------------------------------------------------------------------

def mk(parent_comp, optype, name, x, y):
    try:
        o = parent_comp.create(getattr(td, optype), name)
    except Exception:
        o = parent_comp.create(optype, name)
    o.nodeX, o.nodeY = int(x), int(y)
    return o


def fresh(parent_comp, optype, name, x, y):
    """Crea el nodo; si ya existia lo borra antes (relanzar es seguro)."""
    old = parent_comp.op(name)
    if old is not None:
        try:
            old.destroy()
        except Exception:
            pass
    return mk(parent_comp, optype, name, x, y)


def get_or_make(parent_comp, optype, name, x, y):
    """Lo reutiliza si existe (conserva su storage); si no, lo crea."""
    o = parent_comp.op(name)
    if o is not None:
        return o
    return mk(parent_comp, optype, name, x, y)


def setp(o, name, value):
    try:
        p = getattr(o.par, name, None)
        if p is not None:
            p.val = value
            return True
    except Exception:
        pass
    return False


def setp_any(o, names, value):
    for n in names:
        if setp(o, n, value):
            return n
    return None


def setexpr(o, name, expression):
    try:
        p = getattr(o.par, name, None)
        if p is not None:
            p.expr = expression
            return True
    except Exception:
        pass
    return False


def setmenu(o, names, wanted, index=None):
    """Fija un menu por nombre de opcion; si no lo encuentra, por indice."""
    for n in names:
        try:
            p = getattr(o.par, n, None)
        except Exception:
            p = None
        if p is None:
            continue
        try:
            opts = [str(x).lower() for x in p.menuNames]
            for w in wanted:
                if w.lower() in opts:
                    p.val = p.menuNames[opts.index(w.lower())]
                    return True
        except Exception:
            pass
        if index is not None:
            try:
                p.menuIndex = index
                return True
            except Exception:
                pass
    return False


def has_par(o, name):
    try:
        return getattr(o.par, name, None) is not None
    except Exception:
        return False


def connect(dst, src, i=0):
    try:
        dst.inputConnectors[i].connect(src)
        return True
    except Exception:
        return False


def get_page(base, name):
    for pg in base.customPages:
        if pg.name == name:
            return pg
    return base.appendCustomPage(name)


def add_par(base, page, kind, name, label, default=None, lo=None, hi=None,
            menu=None, menu_labels=None, clamp=False):
    """Anade un parametro si no existe. Si ya existe no lo toca: conserva
    lo que hayas ajustado a mano."""
    if has_par(base, name):
        return False
    if kind == 'float':
        p = page.appendFloat(name, label=label)
    elif kind == 'int':
        p = page.appendInt(name, label=label)
    elif kind == 'toggle':
        p = page.appendToggle(name, label=label)
    elif kind == 'pulse':
        page.appendPulse(name, label=label)
        return True
    elif kind == 'menu':
        p = page.appendMenu(name, label=label)
        p[0].menuNames = menu
        p[0].menuLabels = menu_labels or menu
        p[0].default = p[0].val = default
        return True
    else:
        raise ValueError(kind)
    if lo is not None:
        p[0].normMin = lo
        if clamp:
            p[0].min = lo
            p[0].clampMin = True
    if hi is not None:
        p[0].normMax = hi
        if clamp:
            p[0].max = hi
            p[0].clampMax = True
    if default is not None:
        p[0].default = p[0].val = default
    return True


def renew_default(base, name, old, new):
    """Cambia el valor por defecto de un parametro que ya existia. Solo
    toca el valor si seguia en el defecto viejo: lo ajustado a mano se
    respeta."""
    p = getattr(base.par, name, None) if has_par(base, name) else None
    if p is None:
        return False
    try:
        p.default = new
    except Exception:
        pass
    try:
        if abs(float(p.eval()) - float(old)) < 1e-6:
            p.val = new
            info('%s: %g -> %g (nuevo valor por defecto)' % (name, old, new))
            return True
    except Exception:
        pass
    return False


# -----------------------------------------------------------------------------
# REQUISITOS Y NIVEL
# -----------------------------------------------------------------------------

def require_base(fase):
    base = op(COMP_PATH)
    if base is None:
        raise RuntimeError('No encuentro %s. Aplica antes fase12_base.py.' % COMP_PATH)
    for n in ['ritmo', 'nucleo', 'reticula', 'render', 'rotulo']:
        if base.op(n) is None:
            raise RuntimeError('Falta %s en FASE1: aplica fase12_base.py.' % n)
    for n in ['midi_in', 'midi_callbacks']:
        if base.op(n) is None:
            raise RuntimeError('Falta %s en FASE1: aplica fase12_base.py.' % n)
    lvl = current_level(base)
    if fase > 3 and lvl < fase - 1:
        raise RuntimeError('FASE1 esta en la fase %d. Aplica antes la fase %d.'
                           % (lvl, fase - 1))
    return base


def current_level(base):
    try:
        return int(base.par.Nivel)
    except Exception:
        return 2


def set_level(base, fase):
    page = get_page(base, 'Estratos')
    add_par(base, page, 'int', 'Nivel', 'Ultima fase aplicada', 3, 3, 10)
    new = max(current_level(base), fase)
    base.par.Nivel = new
    try:
        base.par.Nivel.readOnly = True
    except Exception:
        pass
    return new


# -----------------------------------------------------------------------------
# TEXTOS DE LOS DAT QUE USAN EL MOTOR
# -----------------------------------------------------------------------------

MIDI_CB = r'''# Router MIDI de Estratos (instalado por estratos_comun.py).
#
# Todo se lee de los BYTES del mensaje, como en la fase 2:
#   9n kk vv  note on (vv = 0 es note off)     8n kk vv  note off
#   Bn cc vv  controlador                       F0 ... F7 SysEx (MMC)
#   FA        START                             FC        STOP
# n = canal - 1. El motor decide que hacer con cada canal: SEQ1 (Canal),
# SEQ2 (Canal2, desde la fase 5) y bateria (Canaldrum, desde la fase 7).


def _raw(values):
    for a in reversed(values):
        if isinstance(a, (bytes, bytearray)):
            return bytes(a)
    return None


def _num(x, default=None):
    try:
        return int(float(x))
    except Exception:
        return default


def route_bytes(b):
    m = op('motor').module
    if not b:
        return None
    st = b[0]
    if st == 0xF0:
        return m.midi_sysex(b)
    if st == 0xFA:
        return m.midi_start()
    if st == 0xFC:
        return m.midi_stop()
    if st >= 0xF0:
        return None                                # reloj y demas
    kind, ch = st & 0xF0, (st & 0x0F) + 1
    if len(b) < 3:
        return None
    if kind == 0x90:
        if b[2] > 0:
            return m.midi_note_on(ch, b[1], b[2])
        return m.midi_note_off(ch, b[1])
    if kind == 0x80:
        return m.midi_note_off(ch, b[1])
    if kind == 0xB0:
        return m.midi_cc(ch, b[1], b[2])
    return None


def onReceiveMIDI(*args, **kwargs):
    values = list(args) + list(kwargs.values())
    b = _raw(values)
    if b is not None:
        route_bytes(b)
        return
    # Sin bytes: por los campos con nombre (menos fiable)
    msg = str(kwargs.get('message', args[2] if len(args) > 2 else '')).lower()
    ch = _num(kwargs.get('channel', args[3] if len(args) > 3 else None))
    idx = _num(kwargs.get('index', args[4] if len(args) > 4 else None))
    val = _num(kwargs.get('value', args[5] if len(args) > 5 else None))
    m = op('motor').module
    if 'note' in msg and ch is not None and idx is not None:
        if 'off' in msg or not val:
            m.midi_note_off(ch, idx)
        else:
            m.midi_note_on(ch, idx, val)
    return
'''

LATIDO = r'''# Un latido por fotograma: avanza el motor y redibuja.
def onFrameStart(frame):
    m = parent().op('motor')
    if m is not None:
        try:
            m.module.frame_tick()
        except Exception as e:
            if not me.fetch('err', False):
                print('FALLO en el motor: %s' % e)
                me.store('err', True)
    return
'''

PULSOS = r'''# Botones y conmutadores de las paginas Fase3 ... Fase10 -> motor
def onPulse(par):
    op('motor').module.on_pulse(par.name)
    return


def onValueChange(par, prev):
    if par.name in ('Modoactuacion',):
        op('motor').module.on_value(par.name, par.eval())
    return
'''

FORMAS_CB = r'''# Script CHOP de instancias: cada uno pide al motor su lista por nombre
# (i_formas_pulidas, i_formas_porosas, i_coronas, i_estratos, i_luz_celda).

CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']
DUMMY = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    try:
        rows = op('motor').module.instance_rows(scriptOp.name)
    except Exception:
        rows = []
    if not rows:
        rows = [DUMMY]
    n = len(rows)
    scriptOp.numSamples = n
    chans = [scriptOp.appendChan(nm) for nm in CHANS]
    scriptOp.numSamples = n
    for j, ch in enumerate(chans):
        vals = [float(r[j]) for r in rows]
        try:
            ch.vals = vals
        except Exception:
            for i in range(n):
                ch[i] = vals[i]
    return
'''

RETICULA_CB = r'''# Posicion de las celdas (85 con do1-do8) sobre la superficie ACTUAL del planeta.
# De polo a polo: los polos son las notas extremas del rango y en medio
# un anillo por octava; la clase de nota elige el meridiano.
# (Reescrito por estratos_comun.py: la geometria la da el motor, para que
# la reticula suba con las conchas.)

CHANS = ['tx', 'ty', 'tz', 'nx', 'ny', 'nz', 'r', 'g', 'b']


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    m = op('motor').module
    try:
        show = int(parent().par.Showgrid)
    except Exception:
        show = 1
    rows = []
    if show:
        W, c = m.world(), m.cfg()
        for i in range(m.N):
            R = m.suelo(W, c, i) + 0.06      # cada marca sobre el suelo de su celda
            nx, ny, nz = m.normal_i(i)
            t = i / float(max(1, m.N - 1))
            rows.append([nx * R, ny * R, nz * R, nx, ny, nz,
                         0.30 + 0.45 * t, 0.55, 0.75 - 0.35 * t])
    if not rows:
        rows = [[0, -9999, 0, 0, 1, 0, 0, 0, 0]]
    n = len(rows)
    scriptOp.numSamples = n
    chans = [scriptOp.appendChan(nm) for nm in CHANS]
    scriptOp.numSamples = n
    for i in range(n):
        for j, ch in enumerate(chans):
            ch[i] = float(rows[i][j])
    return
'''

# -----------------------------------------------------------------------------
# INSTALAR EL MOTOR
# -----------------------------------------------------------------------------

def read_text(carpeta, name):
    path = carpeta.rstrip('/\\') + '/' + name
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception:
        raise RuntimeError('No puedo leer %s. Revisa CARPETA al principio del '
                           'script de fase: debe ser la carpeta donde estan '
                           'todos los archivos de Estratos.' % path)


def install_core(base, carpeta, fase):
    nivel = set_level(base, fase)
    ok('nivel de FASE1: %d' % nivel)

    motor = get_or_make(base, 'textDAT', 'motor', -660, -340)
    src = read_text(carpeta, 'estratos_motor.py')
    if motor.text != src:
        motor.text = src
    try:
        v = motor.module.MOTOR_VERSION
        ok('motor cargado (%s); el estado del mundo se conserva' % v)
    except Exception as e:
        raise RuntimeError('El motor no compila: %s' % e)

    midi_cb = base.op('midi_callbacks')
    midi_cb.text = MIDI_CB
    ok('midi_callbacks: router MIDI (notas, note off, CC, START/STOP, MMC)')

    latido = base.op('latido')
    if latido is None:
        latido = mk(base, 'executeDAT', 'latido', -220, 320)
    latido.text = LATIDO
    latido.store('err', False)
    setp(latido, 'active', True)
    setp_any(latido, ['framestart', 'onframestart'], True)
    ok('latido: el motor avanza en cada fotograma')

    base.op('reticula_callbacks').text = RETICULA_CB
    ok('reticula: sigue la superficie que da el motor')

    formas = get_or_make(base, 'textDAT', 'formas_callbacks', -660, -200)
    formas.text = FORMAS_CB

    pulsos = get_or_make(base, 'parameterexecuteDAT', 'pulsos', -660, -60)
    pulsos.text = PULSOS
    setp(pulsos, 'active', True)
    setp_any(pulsos, ['op', 'ops'], base.path)
    setp_any(pulsos, ['pars'], '*')
    setp_any(pulsos, ['custom'], True)
    setp_any(pulsos, ['builtin'], False)
    setp_any(pulsos, ['valuechange'], True)
    setp_any(pulsos, ['onpulse'], True)
    ok('pulsos: botones de las paginas de fase -> motor')

    add_grid_pars(base)
    set_camera(base)
    set_legend(base)                 # antes de retirar baliza_callbacks
    retirar_balizas(base)
    install_luz_celda(base)
    reparar_color_instancias(base)
    apply_wobble(base)
    patch_ritmo(base)
    return motor


BALIZAS_VIEJAS = ['baliza', 'baliza_chop', 'baliza_callbacks', 'mat_baliza',
                  'baliza2', 'i_baliza2', 'mat_baliza2',
                  'balizas_drum', 'i_balizas_drum', 'mat_balizas_drum',
                  'luz_drum', 'i_luz_drum', 'mat_luz_drum',
                  'luz12_callbacks']    # la luz de las fases 1 y 2 (fase12 v3)


def retirar_balizas(base):
    """Sin balizas: la luz de celda las sustituye. Borra los nodos de las
    versiones anteriores si existen (el mundo vive en el motor: no se toca)."""
    quitados = []
    for nm in BALIZAS_VIEJAS:
        o = base.op(nm)
        if o is None:
            continue
        try:
            o.destroy()
            quitados.append(nm)
        except Exception as e:
            info('no pude borrar %s: %s; apagalo a mano' % (nm, e))
    for nm in ('Tambalizadrum', 'Anillobalizadrum'):
        if remove_par(base, nm):
            quitados.append(nm)
    if quitados:
        ok('balizas retiradas (la luz de celda las sustituye): %s' % ', '.join(quitados))
    set_render(base)


def reparar_color_instancias(base):
    """Las geometrias instanciadas creadas antes de comun v10 (formaciones,
    coronas, estratos) y la reticula de fase12_base.py v2 enlazaban su color
    a instancecolorr/g/b, que no existe: salian del color del material. Se
    reparan aqui, en cada relanzamiento de cualquier fase, sin tocar nada
    mas (ni el mundo ni la posicion de las instancias)."""
    reparadas, malas = [], []
    for geo in list(base.children):
        if str(getattr(geo, 'OPType', '')) != 'geometryCOMP':
            continue
        try:
            src = str(geo.par.instanceop.eval() or '')
        except Exception:
            src = ''
        if not src:
            continue
        antes, _ = instance_color_ok(geo)
        if antes:
            continue
        set_instance_color(geo, geo.name)
        ahora, det = instance_color_ok(geo)
        (reparadas if ahora else malas).append(geo.name if ahora else '%s (%s)' % (geo.name, det))
    if reparadas:
        ok('color por instancia reparado en: %s' % ', '.join(reparadas))
    for g in malas:
        fail('%s no lee el color por instancia: Instance 2 -> Color R/G/B = r g b, '
             'Color Mode = Replace' % g)
    return not malas


def install_luz_celda(base):
    """La luz de celda: losetas opacas a ras de la superficie, una
    geometria para todas (centro: secuenciadores; borde: bateria)."""
    page = get_page(base, 'Fase3')
    add_par(base, page, 'toggle', 'Luzseq', 'Luz de los secuenciadores en las celdas', True)
    make_constant(base, 'mat_luz_celda', 780, 700, (1.0, 1.0, 1.0))
    geo = make_instanced(base, 'luz_celda', 520, 700, 'mat_luz_celda')
    bien, det = instance_color_ok(geo)
    if not bien:
        fail('luz_celda no lee el color por instancia (%s): Instance 2 -> Color R/G/B = '
             'r g b, Color Mode = Replace' % det)
    set_render(base)
    return geo


RITMO_GIRO_OLD = """    if spt > 0 and playing() and not paused:
        angle = (angle + dt * 360.0 / spt) % 360.0"""
RITMO_GIRO_NEW = """    if spt > 0 and playing() and not paused:
        angle = (angle + dt * 360.0 / spt * giro_factor()) % 360.0"""
RITMO_GIRO_FN = """def giro_factor():
    # Giro vivo (fase 6): el motor frena el planeta cuando el mundo deja de
    # cambiar. Sin motor, o antes de la fase 6, vale 1.
    try:
        m = op('motor')
        return float(m.module.giro_factor()) if m is not None else 1.0
    except Exception:
        return 1.0


def rotation(frame=None):"""


def patch_ritmo(base):
    """Ensena a 'ritmo' a multiplicar el giro por el giro vivo del motor.
    Solo cambia el texto: el angulo acumulado (storage) se conserva."""
    r = base.op('ritmo')
    if r is None:
        return False
    t = r.text
    if 'giro_factor()' in t:
        return True
    if RITMO_GIRO_OLD not in t or 'def rotation(frame=None):' not in t:
        info('ritmo: no reconozco su texto; el giro vivo no se aplica')
        return False
    t = t.replace(RITMO_GIRO_OLD, RITMO_GIRO_NEW)
    t = t.replace('def rotation(frame=None):', RITMO_GIRO_FN, 1)
    r.text = t
    ok('ritmo: el giro se multiplica por el giro vivo del motor')
    return True


CAM_EXPR = "parent().op('motor').module.cam('%s', %d, absTime.frame)"


def set_camera(base):
    """Camara de globo (motor v24): el planeta entero, centrado y tan cerca
    como permite el cuadro. Posicion y planos de recorte los da el motor.
    Si existe 'objetivo' (fase 10) mira a el; si no, mira al centro desde +Z."""
    cam = base.op('camara')
    if cam is None:
        fail('no encuentro la camara')
        return False
    good = all(setexpr(cam, ax, CAM_EXPR % ('pos', k)) for k, ax in enumerate(('tx', 'ty', 'tz')))
    obj = base.op('objetivo')
    if obj is not None:
        setp(cam, 'lookat', 'objetivo')
    else:
        for ax in ('rx', 'ry', 'rz'):
            try:
                getattr(cam.par, ax).expr = ''
            except Exception:
                pass
            setp(cam, ax, 0.0)
    setexpr(cam, 'near', CAM_EXPR % ('near', 0))
    setexpr(cam, 'far', CAM_EXPR % ('far', 0))
    if good:
        ok('camara: el globo entero y centrado; retrocede a cada enterramiento')
    else:
        fail('no pude enlazar la camara al motor')
    return good


def remove_par(base, name):
    """Quita un parametro propio si existe (parametros obsoletos)."""
    try:
        p = getattr(base.par, name, None)
        if p is None:
            return False
        p.destroy()
        return True
    except Exception as e:
        info('no pude quitar %s: %s' % (name, e))
        return False


LEYENDA_LETRA = 9                    # 15 hasta comun v12 (un 40 % menos)
LEYENDA_LETRA_VIEJA = 15


def legend_expr(fuentes):
    """Texto de la leyenda: las fuentes, o nada si Leyenda esta apagado."""
    return ("(" + " + ".join("parent().op('%s').module.legend(absTime.frame)" % f
                             for f in fuentes) + ") if parent().par.Leyenda else ''")


def set_legend_font(rot):
    """Letra de la leyenda: baja de 15 a 9; respeta un tamano puesto a mano."""
    for n in ('fontsizex', 'fontsize', 'fontsizey'):
        p = getattr(rot.par, n, None) if rot is not None else None
        if p is not None:
            try:
                if abs(float(p.eval()) - LEYENDA_LETRA_VIEJA) < 1e-6:
                    p.val = LEYENDA_LETRA
            except Exception:
                pass


def set_legend(base):
    add_par(base, get_page(base, 'Fase1'), 'toggle', 'Leyenda', 'Mostrar leyenda', True)
    rot = base.op('rotulo')
    set_legend_font(rot)
    if setexpr(rot, 'text', legend_expr(['ritmo', 'motor'])):
        ok('leyenda: tempo + motor (nota incluida); Leyenda la oculta')
    else:
        fail('no pude enlazar la leyenda')


# -----------------------------------------------------------------------------
# GEOMETRIA INSTANCIADA
# -----------------------------------------------------------------------------

def make_phong(base, name, x, y, spec=0.3, shin=20, diff=1.0, amb=None, emit=None):
    m = get_or_make(base, 'phongMAT', name, x, y)
    for ch in 'rgb':
        setp_any(m, ['diff' + ch, 'diffuse' + ch], diff)
        setp_any(m, ['spec' + ch, 'specular' + ch], spec)
        if amb is not None:
            setp_any(m, ['amb' + ch, 'ambient' + ch], amb)
        if emit is not None:
            setp_any(m, ['emit' + ch, 'emission' + ch], emit)
    setp_any(m, ['shininess', 'specularexp'], shin)
    return m


def materiales_formas(base):
    """Pulido: reflejo blanco ancho y fuerte, que se ve en cajas pequenas.
    Poroso: sin reflejo, difuso apagado. El motor ademas les da color y
    forma distintos (lo poroso, rugoso y en tramos)."""
    make_phong(base, 'mat_pulido', 780, 380, spec=1.0, shin=14, diff=1.0, amb=0.25, emit=0.04)
    make_phong(base, 'mat_poroso', 780, 300, spec=0.0, shin=1, diff=0.80, amb=0.10, emit=0.0)


def make_constant(base, name, x, y, rgb):
    m = get_or_make(base, 'constantMAT', name, x, y)
    for ch, v in zip(('colorr', 'colorg', 'colorb'), rgb):
        setp(m, ch, v)
    return m


SPIN_EXPR = "parent().op('ritmo').module.rotation(absTime.frame)"
WOBBLE_EXPR = "parent().op('motor').module.wobble(absTime.frame)"


def set_spin(geo):
    """Giro del planeta en una geometria: ry = giro al tempo, rx = balanceo
    del eje, rz = inclinacion. Orden Ry Rx Rz: primero gira sobre su eje,
    luego el eje se balancea hacia la camara y al final se inclina."""
    setexpr(geo, 'ry', SPIN_EXPR)
    setexpr(geo, 'rx', WOBBLE_EXPR)
    setexpr(geo, 'rz', 'parent().par.Tilt')
    return setmenu(geo, ['rord'], ['yxz'])


GRID_PARS = ('Notapolosur', 'Notapolonorte', 'Fuerarango')


def add_grid_pars(base):
    """Rango de notas de la reticula, en la pagina Fase3. Si estaban en
    otra pagina (version anterior), se mueven conservando su valor. Los
    polos van entre do1 (24) y do8 (108)."""
    page = get_page(base, 'Fase3')
    keep = {}
    for nm in GRID_PARS:
        try:
            p = getattr(base.par, nm, None)
            if p is not None and p.page.name != 'Fase3':
                keep[nm] = p.eval()
                p.destroy()
        except Exception:
            pass
    add_par(base, page, 'int', 'Notapolosur', 'Polo sur: nota MIDI (24 do1 - 106)', 24, 24, 106, clamp=True)
    add_par(base, page, 'int', 'Notapolonorte', 'Polo norte: nota MIDI (26 - 108 do8)', 108, 26, 108, clamp=True)
    add_par(base, page, 'menu', 'Fuerarango', 'Notas fuera del rango', 'plegar',
            menu=['plegar', 'ignorar', 'limitar'],
            menu_labels=['Plegar por octavas', 'Ignorar', 'Limitar al polo'])
    for nm, lo, hi in (('Notapolosur', 24, 106), ('Notapolonorte', 26, 108)):
        try:
            p = getattr(base.par, nm)
            p.min, p.max, p.normMin, p.normMax = lo, hi, lo, hi
            p.clampMin = p.clampMax = True
            if nm in keep:
                p.val = max(lo, min(hi, int(keep[nm])))
            elif not (lo <= int(p.eval()) <= hi):
                p.val = max(lo, min(hi, int(p.eval())))
        except Exception:
            pass
    if 'Fuerarango' in keep:
        try:
            base.par.Fuerarango = keep['Fuerarango']
        except Exception:
            pass
    ok('pagina Fase3: Notapolosur (24, do1), Notapolonorte (108, do8), Fuerarango '
       '(plegar / ignorar / limitar). Cambiar el rango vacia el mundo')
    for nm in GRID_PARS:
        try:
            pg = getattr(base.par, nm).page.name
            if pg != 'Fase3':
                info('%s sigue en la pagina %s: no pude moverlo a Fase3' % (nm, pg))
        except Exception:
            pass


def apply_wobble(base):
    """Pone el balanceo en todas las geometrias que giran con el planeta
    (nucleo, reticula, balizas, formas, coronas, estratos)."""
    page = get_page(base, 'Fase3')
    add_par(base, page, 'toggle', 'Rotextra', 'Balanceo del eje (ver los polos)', True)
    add_par(base, page, 'float', 'Balanceo', 'Amplitud del balanceo (grados)', 60.0, 0.0, 90.0)
    add_par(base, page, 'float', 'Balanceoper', 'Periodo del balanceo (s)', 90.0, 5.0, 600.0)
    names, sin_orden = [], []
    for g in list(base.children):
        try:
            e = g.par.ry.expr or ''
        except Exception:
            continue
        if 'rotation(' not in e:
            continue
        if not set_spin(g):
            sin_orden.append(g.name)
        names.append(g.name)
    ok('balanceo del eje en %d geometrias (%s): Rotextra, Balanceo, Balanceoper'
       % (len(names), ', '.join(names)))
    for n in sin_orden:
        info('%s: no pude fijar Rotate Order = Ry Rx Rz; ponlo a mano' % n)


# El color por instancia se llama instancer/g/b en el Geometry COMP (pagina
# Instance 2). Las versiones anteriores de este archivo usaban
# instancecolorr/g/b, que no existe: las instancias no cogian su color.
INST_COLOR_PARS = (('r', ['instancer', 'instancecolorr']),
                   ('g', ['instanceg', 'instancecolorg']),
                   ('b', ['instanceb', 'instancecolorb']))
INST_COLOR_MODE = ['instancecolormode', 'instcolormode', 'colormode']


def set_instance_color(geo, name=''):
    """Que la geometria pinte cada instancia con sus canales r g b
    (Color Mode = Replace). Devuelve True si quedo configurada."""
    good = True
    for ch, names in INST_COLOR_PARS:
        if not setp_any(geo, names, ch):
            info('%s: no encontre el color de instancia (%s)' % (name or geo.name, names[0]))
            good = False
    if not setmenu(geo, INST_COLOR_MODE, ['replace'], None):
        info('%s: no pude fijar Instance Color Mode = Replace; ponlo a mano' % (name or geo.name))
    return good


def instance_color_ok(geo):
    """(True/False, detalle): la geometria lee r g b por instancia."""
    if geo is None:
        return False, 'no existe'
    for ch, names in INST_COLOR_PARS:
        val = None
        for n in names:
            try:
                p = getattr(geo.par, n, None)
            except Exception:
                p = None
            if p is not None:
                val = str(p.eval())
                break
        if val != ch:
            return False, '%s = %r' % (names[0], val)
    for n in INST_COLOR_MODE:
        try:
            p = getattr(geo.par, n, None)
        except Exception:
            p = None
        if p is not None:
            v = str(p.eval()).lower()
            if 'replace' not in v:
                return False, '%s = %s' % (n, v)
            break
    return True, ''


def set_additive(mat):
    """Material que suma su color a lo que hay detras (luz): nunca oscurece."""
    a = setp_any(mat, ['blending', 'blend'], True)
    b = setmenu(mat, ['srcblend', 'srcblendcolor'], ['one'], None)
    d = setmenu(mat, ['destblend', 'dstblend', 'destblendcolor'], ['one'], None)
    setp_any(mat, ['depthwrite', 'writedepth'], False)
    if not (a and b and d):
        info('%s: no pude fijar la mezcla aditiva (Blending, Src/Dest = One); '
             'ponla a mano' % mat.name)
    return bool(a and b and d)


def make_instanced(base, name, x, y, mat, sop='box'):
    """Geometry COMP 'name' + Script CHOP 'i_name' que pide al motor sus
    instancias. Una caja de 1x1x1 con la base en y=0 (o una esfera de radio
    1), escalada, girada y coloreada por instancia."""
    chop = fresh(base, 'scriptCHOP', 'i_' + name, x - 220, y)
    setp_any(chop, ['callbacks', 'callbackdat', 'dat'], 'formas_callbacks')
    geo = fresh(base, 'geometryCOMP', name, x, y)
    for k in list(geo.children):
        try:
            k.render = False
            k.display = False
        except Exception:
            pass
    if sop == 'sphere':
        s = mk(geo, 'sphereSOP', 'bola', 0, 0)
        for ax in ('radx', 'rady', 'radz'):
            setp(s, ax, 1.0)
        setp_any(s, ['type', 'primtype'], 'polymesh')
        setp_any(s, ['rows'], 20)
        setp_any(s, ['cols'], 20)
    else:
        s = mk(geo, 'boxSOP', 'bloque', 0, 0)
        for ax in ('sizex', 'sizey', 'sizez'):
            setp(s, ax, 1.0)
        setp(s, 'ty', 0.5)
    for attr in ('render', 'display'):
        try:
            setattr(s, attr, True)
        except Exception:
            pass
    setp(geo, 'instanceop', 'i_' + name)
    setp_any(geo, ['instancing', 'instance'], True)
    for par_name, ch in [('instancetx', 'tx'), ('instancety', 'ty'), ('instancetz', 'tz'),
                         ('instancerx', 'rx'), ('instancery', 'ry'), ('instancerz', 'rz'),
                         ('instancesx', 'sx'), ('instancesy', 'sy'), ('instancesz', 'sz')]:
        if not setp(geo, par_name, ch):
            info('%s: no encontre %s' % (name, par_name))
    setmenu(geo, ['instancerord'], ['xyz'], 0)
    set_instance_color(geo, name)
    set_spin(geo)
    setp(geo, 'material', mat)
    try:
        chop.cook(force=True)
    except Exception:
        pass
    ok('%s: geometria instanciada desde i_%s, gira con el planeta' % (name, name))
    return geo


def set_render(base):
    names = [n for n in RENDER_ORDER if base.op(n) is not None]
    lights = [n for n in LIGHT_ORDER if base.op(n) is not None]
    r = base.op('render')
    a = setp(r, 'geometry', ' '.join(names))
    b = setp(r, 'lights', ' '.join(lights))
    if a:
        ok('render dibuja: %s' % ' '.join(names))
    else:
        fail('no pude fijar la geometria del render: pon a mano "%s"' % ' '.join(names))
    return a and b


def leeme(base, fase, text):
    d = get_or_make(base, 'textDAT', 'LEEME_fases', -440, -340)
    secs = d.fetch('secs', {})
    secs[fase] = text
    d.store('secs', secs)
    d.text = '\n\n'.join(secs[k] for k in sorted(secs))


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

class Prueba(object):
    """Guarda el mundo, deja probar, y lo restaura al terminar."""

    def __init__(self, base):
        self.base = base
        self.motor = base.op('motor')
        self.m = self.motor.module
        self.saved = copy.deepcopy(self.motor.fetch('W', None))
        self.checks = []
        self.ciclos = None
        tb = base.op('ciclos')
        if tb is not None:
            try:
                self.ciclos = [[cell.val for cell in tb.row(r)] for r in range(tb.numRows)]
            except Exception:
                self.ciclos = None
        try:
            self.nota = int(base.par.Nota)
        except Exception:
            self.nota = None

    def check(self, label, cond, detail=''):
        self.checks.append((bool(cond), label, detail))

    def midi(self, *byts):
        mm = self.base.op('midi_callbacks').module
        mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes(byts))

    def finish(self):
        if self.saved is None:
            self.m.reset_world()
        else:
            self.motor.store('W', self.saved)
        try:
            self.m._CACHE['inst'] = None
            self.m._CACHE['tiles'] = None
            self.m._CACHE['printed'] = {}
        except Exception:
            pass
        tb = self.base.op('ciclos')
        if tb is not None and self.ciclos is not None:
            try:
                tb.clear()
                for fila in self.ciclos:
                    tb.appendRow(fila)
            except Exception:
                pass
        if self.nota is not None:
            try:
                self.base.par.Nota = self.nota
            except Exception:
                pass
        log = self.base.op('midi_log')
        if log is not None:
            log.clear()
            log.appendRow(['frame', 'canal', 'nota', 'vel', 'resultado'])
        print('AUTOPRUEBA')
        print('-' * 66)
        good = True
        for passed, label, detail in self.checks:
            good = good and passed
            print('  %-6s %s%s' % ('OK' if passed else 'FALLO', label,
                                   ('   (' + detail + ')') if detail else ''))
        print('-' * 66)
        print('  AUTOPRUEBA %s' % ('OK' if good else 'FALLIDA: pegame este bloque'))
        print('-' * 66)
        return good


def run_test(base, fn):
    t = Prueba(base)
    try:
        fn(t)
    except Exception as e:
        import traceback
        t.check('la prueba se ejecuto entera', False, '%s' % e)
        traceback.print_exc()
    return t.finish()
