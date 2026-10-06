"""
=============================================================================
ESTRATOS - PIEZAS COMUNES DE LAS FASES 3 A 10
=============================================================================
No se ejecuta solo: lo carga cada script de fase. Contiene:

  - utilidades para crear nodos y parametros (las mismas de fase12_base.py)
  - install_core(): instala o refresca el 'motor' y los DAT que lo usan
    (midi_callbacks, latido, baliza_callbacks, reticula_callbacks,
    formas_callbacks, pulsos). Todas las fases lo llaman: relanzar una
    fase deja siempre el motor al dia.
  - make_instanced(): un Geometry COMP alimentado por un Script CHOP del motor
  - set_render(), set_legend(), autoprueba
=============================================================================
"""

import td
import copy

VERSION_COMUN = 'comun v5'
COMP_PATH = '/project1/FASE1'

RENDER_ORDER = ['nucleo', 'estratos', 'reticula', 'formas_porosas', 'formas_pulidas',
                'coronas', 'baliza', 'baliza2']
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
    for nm in ['motor', 'latido', 'ritmo', 'reticula_chop', 'baliza_chop', 'formas_callbacks',
               'i_formas_pulidas', 'i_formas_porosas', 'i_coronas', 'i_estratos',
               'i_baliza2', 'camara', 'render', 'rotulo', 'con_rotulo', 'salida']:
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
    for n in ['baliza', 'baliza_chop', 'midi_in', 'midi_callbacks']:
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
    c = parent().op('baliza_chop')
    if c is not None:
        c.cook(force=True)
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
# (i_formas_pulidas, i_formas_porosas, i_coronas, i_estratos, i_baliza2).

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

RETICULA_CB = r'''# Posicion de las 96 celdas sobre la superficie ACTUAL del planeta.
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
        R = m.surface_radius() + 0.06
        for i in range(m.N):
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

BALIZA_CB = r'''# Baliza del SEQ1: va a la celda de la nota y pulsa en cada nota.
# (Reescrito por estratos_comun.py: misma logica que la fase 2, pero se
# coloca encima de la formacion de su celda y sigue a la superficie.)

import math

DECAY = 0.12
BASE_RADIUS = 0.90
PEAK_RADIUS = 1.80
LIFT = 0.30


def current_note():
    try:
        return int(parent().par.Nota)
    except Exception:
        return 60


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    m = op('motor').module
    now = absTime.seconds
    note = current_note()
    trig = False
    last = scriptOp.fetch('last_note', None)
    if last is None or int(last) != note:
        scriptOp.store('last_note', note)
        trig = True
    hit_t = scriptOp.fetch('hit_t', -1.0)
    if hit_t > scriptOp.fetch('hit_seen', -1.0):
        scriptOp.store('hit_seen', hit_t)
        trig = True
    if trig:
        scriptOp.store('t0', now)
    t0 = scriptOp.fetch('t0', now - 10.0)
    env = math.exp(-max(0.0, now - t0) / DECAY)
    radius = BASE_RADIUS + PEAK_RADIUS * env
    try:
        p = m.surface_point(note, LIFT, radius)
        if m.performance():
            p = (0.0, -9999.0, 0.0)
    except Exception:
        p = (0.0, -9999.0, 0.0)
    scriptOp.numSamples = 1
    for name, v in [('tx', p[0]), ('ty', p[1]), ('tz', p[2]),
                    ('env', env), ('radius', radius), ('note', note)]:
        scriptOp.appendChan(name)[0] = float(v)
    return


def legend(frame=None):
    m = op('motor').module
    b = op('baliza_chop')
    try:
        note = int(b['note'][0])
        env = float(b['env'][0])
    except Exception:
        note, env = current_note(), 0.0
    i = m.note_cell(note)
    if i is None:
        donde = 'fuera de rango (ignorada)'
    else:
        f = m.fold_note(note)
        donde = 'celda %2d de %d   %s' % (i, m.N, m.cell_label(i))
        if f != note:
            donde += '   (como %s %d)' % (m.note_name(f), f)
    n = int(round(max(0.0, min(1.0, env)) * 12))
    try:
        ch = int(parent().par.Canal)
    except Exception:
        ch = 13
    hits = b.fetch('hits', 0) if b is not None else 0
    lines = [
        '',
        '  NOTA     %-5s %3d    %s' % (m.note_name(note), note, donde),
        '  PULSO    [%s]' % ('#' * n + '.' * (12 - n)),
        '  SEQ1     canal %d    notas recibidas: %d' % (ch, hits),
    ]
    return '\n'.join(lines)
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

    base.op('baliza_callbacks').text = BALIZA_CB
    base.op('reticula_callbacks').text = RETICULA_CB
    ok('baliza y reticula: siguen la superficie que da el motor')

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
    apply_wobble(base)
    set_legend(base)
    return motor


def set_legend(base):
    rot = base.op('rotulo')
    if setexpr(rot, 'text',
               "parent().op('ritmo').module.legend(absTime.frame) + "
               "parent().op('baliza_callbacks').module.legend(absTime.frame) + "
               "parent().op('motor').module.legend(absTime.frame)"):
        ok('leyenda: tempo + nota + motor')
    else:
        fail('no pude enlazar la leyenda')


# -----------------------------------------------------------------------------
# GEOMETRIA INSTANCIADA
# -----------------------------------------------------------------------------

def make_phong(base, name, x, y, spec=0.3, shin=20, diff=1.0):
    m = get_or_make(base, 'phongMAT', name, x, y)
    for ch in 'rgb':
        setp(m, 'diffuse' + ch, diff)
        setp_any(m, ['spec' + ch, 'specular' + ch], spec)
    setp_any(m, ['shininess', 'specularexp'], shin)
    return m


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
                         ('instancesx', 'sx'), ('instancesy', 'sy'), ('instancesz', 'sz'),
                         ('instancecolorr', 'r'), ('instancecolorg', 'g'),
                         ('instancecolorb', 'b')]:
        if not setp(geo, par_name, ch):
            info('%s: no encontre %s' % (name, par_name))
    setmenu(geo, ['instancerord'], ['xyz'], 0)
    setmenu(geo, ['instancecolormode', 'instcolormode'], ['replace'], 0)
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
        if self.nota is not None:
            try:
                self.base.par.Nota = self.nota
            except Exception:
                pass
        b = self.base.op('baliza_chop')
        if b is not None:
            b.store('hits', 0)
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
