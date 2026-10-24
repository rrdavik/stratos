"""
=============================================================================
ESTRATOS - PIEZAS COMUNES DE LAS FASES 3 A 11
=============================================================================
No se ejecuta solo: lo carga cada script de fase. Contiene:

  - utilidades para crear nodos y parametros (las mismas de fase12_base.py)
  - install_core(): instala o refresca el 'motor' y los DAT que lo usan
    (midi_callbacks, latido, reticula_callbacks, formas_callbacks, pulsos)
    y la luz de celda (luz_celda). Todas las fases lo llaman: relanzar una
    fase deja siempre el motor al dia. Tambien retira las balizas de
    versiones anteriores (baliza, baliza2, balizas_drum, luz_drum).
  - make_instanced(): un Geometry COMP alimentado por un Script CHOP del motor
    (una caja, una esfera o, desde la fase 11, un modelo del catalogo)
  - instanciar_modelos(): las geometrias de los modelos (fase 11: pulida y
    porosa; fase 12: una por modelo con el shader de la piel)
  - terreno_al_dia(): la malla del relieve (fase 11 v5): la esfera 'terreno'
    que el shader desplaza con el mapa de alturas del motor (Script TOP
    'alturas') y colorea con los pisos (Ramp TOP 'rampa_hipso')
  - set_render(), set_legend(), autoprueba
=============================================================================
"""

import td
import copy
import math

VERSION_COMUN = 'comun v36'
COMP_PATH = '/project1/FASE1'

RENDER_ORDER = ['nucleo', 'estratos', 'terreno', 'tejido', 'rios', 'reticula', 'formas_porosas', 'formas_pulidas',
                'coronas', 'particulas', 'diagnostico', 'luz_celda', 'luz_conchas',
                'luz_local']                    # las capas aditivas, al final
PIEL_PREFIJO = 'mod_'                # geometrias de los modelos (fase 11), tras las formas
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
               'i_luz_celda', 'i_rios', 'mat_piel_agua', 'camara', 'render', 'rotulo', 'con_rotulo',
               'salida']:
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


RIOS_PARS = ('Colorrior', 'Anchorio', 'Anchomaxrio', 'Emisivorio', 'Lagos')


def diagnostico_rios(base, m, version=None):
    """Fase 13 v3: en que punto de la cadena desaparecen los rios. Recorre los
    puntos en orden y para en el primero que falla. Devuelve [(estado, punto,
    texto)], estado OK o FALLA (el
    punto donde desaparecen; no es un fallo del script, es el estado del mundo)."""
    out = []

    def nota(estado, punto, texto):
        out.append((estado, punto, texto))
        return estado != 'FALLA'
    try:
        W, c = m.world(), m.cfg()
    except Exception as e:
        nota('FALLA', 0, 'el motor no responde: %s' % e)
        return out
    # 1. la fase 13
    if not nota('OK' if c['nivel'] >= 13 else 'FALLA', 1,
                'Nivel %d%s' % (c['nivel'], '' if c['nivel'] >= 13 else
                                ': menor de 13, el motor no genera rios; aplica fase13_tejido.py')):
        return out
    # 2. el fix de rios azules (fase 13 v2 o posterior)
    faltan = [nm for nm in RIOS_PARS if not has_par(base, nm)]
    if not nota('FALLA' if faltan else 'OK', 2, 'fase 13 %s; parametros de los rios %s'
                % (version or '?', 'que faltan: ' + ', '.join(faltan) if faltan else 'presentes')):
        return out
    # 3. el motor genera tramos
    if m.tema_de(c) != 'naturaleza':
        nota('FALLA', 3, 'Tema ciudad: los rios son de la naturaleza (en la ciudad hay carreteras)')
        return out
    tj = m.tejido(W, c)
    ter = m.terreno(W, c)
    n_tramos = sum(len(r) - 1 for r in tj['rios'])
    if n_tramos == 0:
        lim = m.limit(c)
        rel = [x for x in range(m.N) if W['occ'][x] > 0 and W['own'][x] == m.ARQ]
        umbral = c['pendiente_min'] * lim
        alto = max(ter['centro'] or [0.0])
        if not rel:
            motivo = 'no hay relieve (ninguna celda del SEQ2): los rios nacen en las cumbres'
        elif ter.get('E') is None:
            motivo = 'el mapa de alturas esta vacio (sin numpy en TouchDesigner?)'
        elif alto <= umbral:
            motivo = ('el relieve mas alto mide %.3f y una fuente pide Pendientemin x el limite = %.3f: '
                      'baja Pendientemin' % (alto, umbral))
        else:
            motivo = ('hay cumbres (relieve max %.3f) pero ninguna vecina mas baja: el relieve no tiene '
                      'pendiente hacia ningun lado' % alto)
        nota('FALLA', 3, 'el motor no genera tramos: %s. Enterrar una concha no borra los rios: se '
                         'recalculan con el mundo nuevo (con relieve vuelven)' % motivo)
        return out
    W['vh'] = list(W['vh'])
    inst = m.build_instances(W, c, absTime.seconds)
    rr = W.get('rios_res') or {}
    nota('OK', 3, 'el motor genera %d tramos (%d fuentes, %d lagos, caudal max %d)'
         % (n_tramos, rr.get('fuentes', 0), rr.get('lagos', 0), rr.get('caudal', 0)))
    # 4. llegan a una geometria del render
    chop, geo = base.op('i_rios'), base.op('rios')
    filas = inst.get('rios', [])
    try:
        if chop is not None:
            m._CACHE['inst'] = inst
            chop.cook(force=True)
        n_chop = chop.numSamples if chop is not None else 0
    except Exception:
        n_chop = 0
    try:
        en_render = 'rios' in str(base.op('render').par.geometry.val).split()
    except Exception:
        en_render = False
    if chop is None or geo is None or n_chop < len(filas) or not en_render:
        nota('FALLA', 4, 'i_rios %s, geometria rios %s, en el render %s; relanza fase13_tejido.py'
             % ('%d muestras de %d' % (n_chop, len(filas)) if chop is not None else 'no existe',
                'existe' if geo is not None else 'no existe', 'si' if en_render else 'no'))
        return out
    nota('OK', 4, 'i_rios con %d instancias; rios en el render' % n_chop)
    # 5. se ven en pantalla
    px = rr.get('px', 0.0)
    mat = nombre_op(geo.par.material.eval()) if has_par(geo, 'material') else '?'
    errs = _errs(base.op('mat_piel_agua')) if base.op('mat_piel_agua') is not None else 'no existe'
    col = m.color_rio(c)
    azules = all(tuple(f[9:12]) in (tuple(col), tuple(m.COL_ORILLA)) for f in filas)
    tapados = 0
    cauces = m.cauces(W, c)['por_celda']
    for g, fs in inst.items():          # copas de arbol que caen sobre la cinta
        if g.startswith('mod_veg_piso'):
            for f in fs:
                r_ = math.sqrt(f[0] ** 2 + f[1] ** 2 + f[2] ** 2)
                d = (f[0] / r_, f[1] / r_, f[2] / r_)
                for lista in cauces.values():
                    if any(math.sqrt(max(0.0, 2.0 * (1.0 - sum(d[k] * q[k] for k in range(3))))) * r_
                           < 0.5 * f[6] for q, _ in lista):
                        tapados += 1
                        break
    problemas = []
    if px < c['ancho_min_px'] - 1e-6:
        problemas.append('mide %.1f px, menos que Anchominpx' % px)
    if mat != 'mat_piel_agua' and mat != 'mat_respaldo':
        problemas.append('su material es %s, no mat_piel_agua' % mat)
    if errs:
        problemas.append('mat_piel_agua: %s' % errs)
    if not azules:
        problemas.append('alguna cinta no lleva el azul de Colorrio')
    if tapados:
        problemas.append('%d pisos de arbol encima de la cinta' % tapados)
    nota('FALLA' if problemas else 'OK', 5,
         ('; '.join(problemas)) if problemas else
         'cintas de %.1f px (Anchominpx %.1f), azul reservado, mat_piel_agua sin errores, sin copas encima, '
         'a %.3f del suelo' % (px, c['ancho_min_px'], m.RIO_LIFT))
    return out


def informe_rios(base, m, version=None):
    """Imprime el diagnostico de los rios (diagnostico_rios)."""
    print('DIAGNOSTICO DE LOS RIOS')
    print('-' * 66)
    for estado, punto, texto in diagnostico_rios(base, m, version):
        print('  %-6s %d. %s' % (estado, punto, texto))
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


def nombre_op(v):
    """Nombre del operador al que apunta un parametro de tipo OP: eval()
    devuelve el operador (su ruta completa), no el texto que se escribio."""
    if v is None:
        return ''
    return getattr(v, 'name', None) or str(v).rstrip('/').rsplit('/', 1)[-1]


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
    if has_par(base, name) or (kind == 'rgb' and has_par(base, name + 'r')):
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
    elif kind == 'str':
        p = page.appendStr(name, label=label)
        if default is not None:
            p[0].default = p[0].val = default
        return True
    elif kind == 'rgb':                  # name + r g b (Colorrio -> Colorrior, Colorriog, Colorriob)
        p = page.appendRGB(name, label=label)
        for k, v in enumerate(default or (1.0, 1.0, 1.0)):
            p[k].default = p[k].val = v
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

PULSOS = r'''# Botones y conmutadores de las paginas Fase3 ... Fase18 -> motor
def onPulse(par):
    op('motor').module.on_pulse(par.name)
    return


def onValueChange(par, prev):
    if par.name in ('Modoactuacion', 'Escena', 'Variantes', 'Varangulo', 'Cuantizar30', 'Densidadhoja'):
        op('motor').module.on_value(par.name, par.eval())
    return
'''

FORMAS_CB = r'''# Script CHOP de instancias: cada uno pide al motor su lista por nombre
# (i_formas_pulidas, i_formas_porosas, i_coronas, i_estratos, i_luz_celda;
# desde la fase 11, i_particulas y un i_mod_... por modelo del catalogo;
# desde la fase 13, i_tejido: rios y carreteras).
# Desde la fase 12 las filas de los modelos traen un canal mas, 'a': la
# rugosidad que lee el shader de la piel.

CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b', 'a']
DUMMY = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0, 1.0]


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
    chans = [scriptOp.appendChan(nm) for nm in CHANS[:len(rows[0])]]
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
# la reticula suba con las conchas. El giro de cada marca, rx ry rz, tambien:
# "rotar hacia un vector" no sabe girar en los polos, donde la normal es
# paralela al vector arriba.)

CHANS = ['tx', 'ty', 'tz', 'nx', 'ny', 'nz', 'rx', 'ry', 'rz', 'r', 'g', 'b']


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
            rx, ry = m.orient((nx, ny, nz))  # la marca, plana sobre su celda
            t = i / float(max(1, m.N - 1))
            rows.append([nx * R, ny * R, nz * R, nx, ny, nz, rx, ry, 0.0,
                         0.30 + 0.45 * t, 0.55, 0.75 - 0.35 * t])
    if not rows:
        rows = [[0, -9999, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
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
# SHADER DE LA PIEL (fase 12): un GLSL MAT por familia de material
# -----------------------------------------------------------------------------
# Lee la rugosidad del alfa del color de cada instancia (0 pulido, 1 rugoso).
# Pulido: reflejo fino y fuerte y un reflejo de borde frio. Rugoso: mate y con
# poros (pomez, hormigon). uFamilia: 0 mineral (obsidiana <-> pomez), 1 dosel
# (toda la vegetacion: hojas en manchas de dos verdes, lados pardos, luz que
# envuelve y contraluz; hoja cerosa <-> musgo seco), 2 ciudad (vidrio negro <-> hormigon, con
# ventanas ambar que enciende uVentanas.x desde la fase 17). Las luces llegan
# como uniformes (posicion y color x dimmer de luz_principal, luz_relleno y
# luz_destello). Si el shader falla, Materialrespaldo vuelve a un Phong.
# Fase 11 v5 (comun v33): 3 tierra, la malla del relieve (la esfera 'terreno'
# desplazada en el vertex shader por el mapa de alturas del motor, sAlturas),
# con los pisos de color de la rampa (sRampa, el Ramp TOP 'rampa_hipso'),
# roca facetada, nieve brillante y un sombreado rasante fijo respecto a la
# camara (relieve sombreado suizo); 4 agua, los rios y lagos: azul reservado,
# especular alto y un emisivo bajo (uAgua.x) para la cara de sombra. En la
# naturaleza el tinte del secuenciador y de los pads no toca el albedo: es
# un emisivo de borde (fresnel, uBorde.x) alrededor de los focos uTinte0-2.

PIEL_VERTEX = r"""// Estratos - piel (fase 12; terreno, fase 11 v5): vertex shader
uniform vec4 uTerreno;      // x: 1 la malla del terreno, y: altura de los pisos, z: lo que se hunde sin relieve
uniform sampler2D sAlturas; // r: relieve sobre el suelo local, g: radio del suelo (lat/lon, fila 0 = polo sur)

out Vertex {
    vec4 color;
    vec3 wPos;
    vec3 wNorm;
    vec3 oPos;
    vec3 pPos;
    float hrel;
    vec3 hoja;
    flat int inst;
    flat int camIndex;
} oVert;

vec2 uvDe(vec3 d)
{
    return vec2(atan(d.z, d.x) * 0.15915494 + 0.5, asin(clamp(d.y, -1.0, 1.0)) * 0.31830989 + 0.5);
}

vec3 sobre(vec3 d)
{
    vec2 a = textureLod(sAlturas, uvDe(d), 0.0).rg;
    float e = max(a.r, 0.0);
    return d * (a.g + e - uTerreno.z * (1.0 - smoothstep(0.0, 0.08, e)));
}

void main()
{
    vec3 p = P;
    vec3 nrm = N;
    float h = -1.0;
    if (uTerreno.x > 0.5) {
        // la esfera unidad, desplazada: el suelo de la celda mas el relieve
        vec3 d = normalize(P);
        vec3 e = normalize(cross(vec3(0.0, 1.0, 0.0), d) + vec3(1e-4, 0.0, 0.0));
        vec3 t = cross(d, e);
        p = sobre(d);
        vec3 pe = sobre(normalize(d + e * 0.004));
        vec3 pn = sobre(normalize(d + t * 0.004));
        nrm = normalize(cross(pe - p, pn - p));
        if (dot(nrm, d) < 0.0)
            nrm = -nrm;
        h = max(textureLod(sAlturas, uvDe(d), 0.0).r, 0.0) / max(1e-4, uTerreno.y);
    }
    vec4 wPos = TDDeform(p);
    gl_Position = TDWorldToProj(wPos);
#ifndef TD_PICKING_ACTIVE
    oVert.camIndex = TDCameraIndex();
    oVert.inst = TDInstanceID();
    oVert.wPos = wPos.xyz;
    oVert.wNorm = normalize(TDDeformNorm(nrm));
    oVert.oPos = p;
    oVert.pPos = (uTDMats[TDCameraIndex()].worldInverse * wPos).xyz;
    oVert.hrel = h;
    // fase 11 v8: el uv de los ejemplares (tipo: 1 corteza, 2 hoja, 3 tarjeta de
    // racimo; profundidad en la copa; nivel de rama, para el viento)
    oVert.hoja = uv[0];
    oVert.color = TDInstanceColor(Cd);
#else
    TDWritePickingValues();
#endif
}
"""

PIEL_PIXEL = r"""// Estratos - piel (fase 12; tierra, agua y borde, fase 11 v5): pixel shader
uniform vec4 uFamilia;      // x: 0 mineral, 1 dosel, 2 ciudad, 3 tierra, 4 agua
uniform vec4 uLuz0;         // posicion de luz_principal
uniform vec4 uLuz0Col;      // su color x dimmer
uniform vec4 uLuz1;         // luz_relleno
uniform vec4 uLuz1Col;
uniform vec4 uLuz2;         // luz_destello
uniform vec4 uLuz2Col;
uniform vec4 uAmbiente;     // rgb
uniform vec4 uVentanas;     // x: ventanas de la ciudad, 0 apagadas (hasta la fase 17) o 1
uniform vec4 uNiebla;       // fase 19: x cantidad 0-1, y distancia donde empieza, z donde es total
uniform vec4 uNieblaCol;    // su color
uniform vec4 uGlitch;       // fase 19: x saturacion del modular 0-1, y tiempo (s)
uniform vec4 uTerreno;      // fase 11 v5: y altura de los pisos, w 1 si sRampa esta enlazada
uniform vec4 uPisos;        // x Limitebosque, y Limitenieve, z sombreado rasante (0 fuera de la naturaleza)
uniform vec4 uBorde;        // x intensidad del borde tintado (Tintebordenat; 0 en la ciudad)
uniform vec4 uTinte0;       // focos del tinte: xyz direccion (planeta), w coseno del borde exterior
uniform vec4 uTinteCol0;    // rgb color x intensidad, w coseno del borde interior
uniform vec4 uTinte1;
uniform vec4 uTinteCol1;
uniform vec4 uTinte2;
uniform vec4 uTinteCol2;
uniform vec4 uAgua;         // x emisivo del agua (Emisivorio)
uniform sampler2D sRampa;   // los pisos de color (Ramp TOP rampa_hipso)
uniform vec4 uHojas;        // fase 11 v8: x Traslucidez
uniform vec4 uCultivo;      // rgb Colorcultivo, w Pasoterraza (unidades del mundo)
uniform vec4 uBancal;       // x Muroterraza, y Setos, z texeles por parcela, w alto de un nivel de meseta
uniform vec4 uRiego;        // rgb el agua de los bancales (el azul de rio con menos croma)
uniform sampler2D sCultivo; // r relieve sin aterrazar, g tope de los bancales, b desde donde se inunda, a meseta (+10 acequia)

in Vertex {
    vec4 color;
    vec3 wPos;
    vec3 wNorm;
    vec3 oPos;
    vec3 pPos;
    float hrel;
    vec3 hoja;
    flat int inst;
    flat int camIndex;
} iVert;

layout(location = 0) out vec4 oFragColor[TD_NUM_COLOR_BUFFERS];

float hash13(vec3 p)
{
    p = fract(p * 0.1031);
    p += dot(p, p.zyx + 31.32);
    return fract((p.x + p.y) * p.z);
}

float ruido(vec3 x)
{
    vec3 i = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    float a = mix(hash13(i), hash13(i + vec3(1.0, 0.0, 0.0)), f.x);
    float b = mix(hash13(i + vec3(0.0, 1.0, 0.0)), hash13(i + vec3(1.0, 1.0, 0.0)), f.x);
    float c = mix(hash13(i + vec3(0.0, 0.0, 1.0)), hash13(i + vec3(1.0, 0.0, 1.0)), f.x);
    float d = mix(hash13(i + vec3(0.0, 1.0, 1.0)), hash13(i + vec3(1.0, 1.0, 1.0)), f.x);
    return mix(mix(a, b, f.y), mix(c, d, f.y), f.z);
}

vec3 luz(vec3 pos, vec3 col, vec3 p, vec3 n, vec3 v, vec3 base, float expo, float ks, float wrap,
         inout vec3 spec)
{
    // wrap > 0: la luz "envuelve" (hojas): las caras de lado no quedan negras
    vec3 l = normalize(pos - p);
    float nl = dot(n, l);
    float nw = max((nl + wrap) / (1.0 + wrap), 0.0);
    vec3 h = normalize(l + v);
    spec += col * ks * pow(max(dot(n, h), 0.0), expo) * step(0.0001, nl);
    return base * col * nw;
}

vec3 rampa(float h)
{
    // la misma rampa que el Ramp TOP (rampa_hipso del motor), por si sRampa no esta
    float lb = uPisos.x;
    float ln = uPisos.y;
    vec3 c = mix(vec3(0.11, 0.29, 0.11), vec3(0.15, 0.34, 0.13), smoothstep(0.0, 0.35, h));
    c = mix(c, mix(vec3(0.07, 0.23, 0.18), vec3(0.10, 0.25, 0.20), smoothstep(0.36, lb - 0.05, h)),
            step(0.355, h));
    c = mix(c, vec3(0.38, 0.37, 0.21), smoothstep(lb - 0.05, lb, h));
    c = mix(c, mix(vec3(0.50, 0.46, 0.40), vec3(0.31, 0.29, 0.27), smoothstep(lb + 0.05, ln - 0.01, h)),
            smoothstep(lb, lb + 0.05, h));
    return mix(c, mix(vec3(0.92, 0.94, 0.97), vec3(1.0), smoothstep(ln, 1.0, h)), step(ln - 0.001, h));
}

vec2 uvMapa(vec3 d)
{
    return vec2(atan(d.z, d.x) * 0.15915494 + 0.5, asin(clamp(d.y, -1.0, 1.0)) * 0.31830989 + 0.5);
}

vec3 foco(vec4 t, vec4 c, vec3 d)
{
    return c.rgb * smoothstep(t.w, c.w, dot(d, t.xyz));
}

void main()
{
    TDCheckDiscard();
    float fam = uFamilia.x;
    // el alfa trae la rugosidad (0-1) y, desde la fase 17, las ventanas del
    // edificio: alfa = rugosidad + 2 x nivel (0-4)
    float nivelv = floor(iVert.color.a * 0.5 + 0.0001);
    float rug = clamp(iVert.color.a - 2.0 * nivelv, 0.02, 1.0);
    float luces = min(1.0, nivelv * 0.25);
    vec3 base = iVert.color.rgb;
    vec3 n = normalize(iVert.wNorm);
    vec3 cam = uTDMats[iVert.camIndex].camInverse[3].xyz;
    vec3 v = normalize(cam - iVert.wPos);
    if (dot(n, v) < 0.0)
        n = -n;
    vec3 q = iVert.oPos * 7.0 + vec3(float(iVert.inst) * 1.731);
    float poro = ruido(q) * 0.65 + ruido(q * 3.1) * 0.35;
    float expo = mix(120.0, 6.0, rug);
    float ks = mix(1.2, 0.03, rug);
    float wrap = 0.0;
    float amb = 1.0;
    bool vegetal = fam > 0.5 && fam < 1.5;
    bool tierra = fam > 2.5 && fam < 3.5;
    bool agua = fam > 3.5;
    float sombra = uPisos.z;
    if (tierra) {
        // los pisos por la altura sobre el suelo local: verde mate y granulado
        // abajo, roca facetada en medio, nieve brillante arriba
        float h = clamp(iVert.hrel, 0.0, 1.0);
        base = uTerreno.w > 0.5 ? texture(sRampa, vec2(h, 0.5)).rgb : rampa(h);
        float roca = smoothstep(uPisos.x, uPisos.x + 0.05, h) * (1.0 - step(uPisos.y, h));
        float nieve = step(uPisos.y, h);
        vec3 nf = normalize(cross(dFdx(iVert.wPos), dFdy(iVert.wPos)));
        if (dot(nf, v) < 0.0)
            nf = -nf;
        n = normalize(mix(n, nf, 0.35 * roca));
        vec3 qg = iVert.pPos * 9.0;
        base *= mix(0.80 + 0.40 * ruido(qg * 3.0), 1.0, max(roca, nieve));
        rug = mix(0.9, mix(0.7, 0.3, nieve), max(roca, nieve));
        expo = mix(48.0, 6.0, rug);
        ks = mix(0.30, 0.02, rug);
        amb = 1.15;
        sombra = max(sombra, 0.65);
        // fase 11 v8: los hibridos son mesetas construidas
        vec2 tuv = uvMapa(normalize(iVert.oPos));
        vec4 cu = texture(sCultivo, tuv);
        float muro = 1.0 - smoothstep(0.55, 0.80, abs(dot(nf, normalize(iVert.wPos))));
        float lejos = clamp(fwidth(cu.r) / max(1e-4, uCultivo.w) * 1.5, 0.0, 1.0);
        if (cu.g > 1e-4 && cu.r < cu.g && uCultivo.w > 1e-5) {
            // ARROZAL: bancales por la curva de nivel (la huella verde arroz, la
            // contrahuella de piedra seca), surcos de cerca, lamina de agua si se riega
            float fr = fract(cu.r / uCultivo.w);
            float m = clamp(uBancal.x, 0.05, 0.9);
            float contra = smoothstep(1.0 - m, 1.0 - m + 0.04, fr) * (1.0 - smoothstep(0.96, 1.0, fr));
            float surco = mix(0.9 + 0.1 * step(0.5, fract(cu.r / uCultivo.w * 7.0)), 0.95, lejos);
            vec3 huella = uCultivo.rgb * surco;
            if (cu.b < cu.g - 1e-5 && cu.r >= cu.b) {
                float planton = step(0.78, ruido(iVert.pPos * 60.0));
                huella = mix(uRiego.rgb, uCultivo.rgb * 0.8, planton * (1.0 - lejos));
                rug = mix(0.08, rug, contra);
                expo = mix(110.0, expo, contra);
                ks = mix(1.2, ks, contra);
                sombra = mix(0.0, sombra, contra);
            }
            base = mix(huella, vec3(0.52, 0.47, 0.40) * mix(0.85, 1.1, ruido(iVert.pPos * 30.0)), contra);
        } else if (cu.a > 0.5) {
            // MESETA-JARDIN: muro vertical de piedra seca, pradera arriba, setos
            // que dividen las parcelas y, con un rio cerca, una acequia azul
            float acequia = step(9.5, cu.a);
            vec2 pc = tuv * vec2(textureSize(sCultivo, 0)) / max(1.0, uBancal.z);
            vec2 g = fract(pc);
            float linea = 1.0 - step(0.07, min(min(g.x, 1.0 - g.x), min(g.y, 1.0 - g.y)));
            vec3 pradera = vec3(0.36, 0.56, 0.24) * mix(0.9, 1.08, ruido(iVert.pPos * 12.0));
            pradera = mix(pradera, vec3(0.10, 0.25, 0.10), linea * step(0.5, uBancal.y));
            float canal = acequia * (1.0 - step(0.08, abs(g.x - 0.5))) * (mod(floor(pc.x), 3.0) < 0.5 ? 1.0 : 0.0);
            pradera = mix(pradera, uRiego.rgb, canal);
            base = mix(pradera, vec3(0.52, 0.47, 0.40), muro);
            rug = mix(0.85, 0.08, canal);
        }
    } else if (agua) {
        rug = clamp(iVert.color.a, 0.02, 1.0);
        expo = 90.0;
        ks = 1.4;
        sombra = 0.0;
    } else if (vegetal && iVert.hoja.x > 0.5) {
        // fase 11 v8: los ejemplares de la biblioteca. Corteza mate y parda; la
        // hoja facetada (el pliegue coge la luz), +-12 % de valor y +-2 % de tono
        // por hoja, mas oscura dentro de la copa y mas clara arriba
        vec3 nf = normalize(cross(dFdx(iVert.wPos), dFdy(iVert.wPos)));
        if (dot(nf, v) < 0.0)
            nf = -nf;
        if (iVert.hoja.x < 1.5) {
            float fibra = ruido(vec3(q.x * 3.0, q.y * 0.35, q.z * 3.0));
            base = mix(vec3(0.17, 0.12, 0.08), base, 0.15) * mix(0.75, 1.1, fibra);
            rug = 1.0;
            expo = 8.0;
            ks = 0.02;
            wrap = 0.2;
        } else {
            float var = fract(iVert.hoja.x);
            float prof = clamp(iVert.hoja.y, 0.0, 1.0);
            base *= (0.88 + 0.27 * var) * (1.0 - 0.38 * prof) * (0.90 + 0.22 * clamp(iVert.oPos.y, 0.0, 1.0));
            base = mix(base, base.gbr * vec3(1.0, 0.96, 1.0), 0.04 * (var - 0.45));
            n = normalize(mix(n, nf, 0.6));
            expo = mix(36.0, 8.0, rug);
            ks = mix(0.30, 0.02, rug);
            wrap = 0.5;
        }
        amb = 1.5;
    } else if (vegetal) {
        // vegetal: hojas en manchas anchas de dos verdes (nada de lineas finas);
        // las caras de lado (troncos, ramas, bordes de copa), mas pardas y oscuras;
        // cada planta con su matiz. Pulido: hoja cerosa; rugoso: musgo seco.
        float arriba = abs(dot(n, normalize(iVert.wPos)));
        float hoja = ruido(q * 0.6) * 0.6 + ruido(q * 1.7) * 0.4;
        float matiz = hash13(vec3(float(iVert.inst) * 0.37, 1.3, 2.7));
        vec3 hojas = base * mix(0.72, 1.28, hoja) * mix(vec3(0.92, 1.0, 1.06), vec3(1.10, 1.02, 0.84), matiz);
        float fibra = ruido(vec3(q.x * 3.0, q.y * 0.35, q.z * 3.0));
        vec3 corteza = base * vec3(0.80, 0.62, 0.44) * mix(0.62, 0.95, fibra);
        base = mix(corteza, hojas, smoothstep(0.30, 0.80, arriba));
        base *= 1.0 - 0.30 * rug * smoothstep(0.45, 0.80, poro);
        expo = mix(36.0, 8.0, rug);
        ks = mix(0.30, 0.02, rug);
        wrap = 0.5;
        amb = 1.6;
    } else {
        // poros: lo rugoso se mancha (pomez, hormigon); lo pulido queda limpio
        base *= 1.0 - 0.45 * rug * smoothstep(0.35, 0.75, poro);
    }
    vec3 spec = vec3(0.0);
    vec3 dif = base * uAmbiente.rgb * amb;
    dif += luz(uLuz0.xyz, uLuz0Col.rgb, iVert.wPos, n, v, base, expo, ks, wrap, spec);
    dif += luz(uLuz1.xyz, uLuz1Col.rgb, iVert.wPos, n, v, base, expo, ks, wrap, spec);
    dif += luz(uLuz2.xyz, uLuz2Col.rgb, iVert.wPos, n, v, base, expo, ks, wrap, spec);
    if (sombra > 0.001 && (fam < 1.5 || fam > 2.5)) {
        // relieve sombreado suizo: una luz rasante fija respecto a la camara (de
        // arriba a la izquierda), para que crestas y valles se lean aunque gire el globo
        mat4 ci = uTDMats[iVert.camIndex].camInverse;
        vec3 lr = normalize(-ci[0].xyz * 0.75 + ci[1].xyz * 0.85 + ci[2].xyz * 0.35);
        dif *= mix(1.0, 0.45 + 0.85 * max(dot(n, lr), 0.0), sombra);
    }
    float fres = pow(1.0 - max(dot(n, v), 0.0), 5.0);
    vec3 col = dif + spec;
    if (agua) {
        // agua: el azul se lee tambien en la cara de sombra (emisivo) y brilla en el
        // borde y con la luz (comun v35: mas vivo)
        col += base * uAgua.x + fres * vec3(0.25, 0.35, 0.45) + spec * 0.5;
    } else if (vegetal && iVert.hoja.x > 1.5) {
        // fase 11 v8: a contraluz el borde de la copa se vuelve traslucido y calido
        // (amarillo verdoso, Traslucidez); dentro de la copa, no
        vec3 l0 = normalize(uLuz0.xyz - iVert.wPos);
        float tras = pow(max(dot(-l0, v), 0.0), 3.0) * (1.0 - clamp(iVert.hoja.y, 0.0, 1.0));
        col += uHojas.x * tras * vec3(0.78, 0.92, 0.30) * uLuz0Col.rgb * 0.9 + fres * vec3(0.05, 0.08, 0.05);
    } else if (vegetal) {
        // a contraluz la copa deja pasar la luz: brillo verde, sin reflejo de vidrio
        vec3 l0 = normalize(uLuz0.xyz - iVert.wPos);
        float tras = pow(max(dot(-l0, v), 0.0), 3.0) * (1.0 - 0.5 * rug);
        col += tras * base * uLuz0Col.rgb * 0.35 + fres * vec3(0.05, 0.08, 0.05);
    } else if (fam > 1.5 && fam < 2.5) {
        // ciudad: vidrio negro con reflejo de borde; ventanas ambar (fase 17): de
        // cada edificio se encienden tantas como diga su nivel (1 de 4 ... todas)
        col += fres * (1.0 - rug) * vec3(0.25, 0.28, 0.32);
        vec2 wv = vec2(iVert.oPos.y * 10.0, (iVert.oPos.x + iVert.oPos.z) * 7.0);
        vec2 w = fract(wv);
        float ventana = step(0.3, w.x) * step(w.x, 0.8) * step(0.25, w.y) * step(w.y, 0.75);
        float cual = hash13(vec3(floor(wv), float(iVert.inst) * 0.731));
        float lado = 1.0 - abs(dot(n, normalize(iVert.wPos)));
        col += ventana * step(0.5, lado) * uVentanas.x * step(cual, luces - 0.001) * vec3(1.0, 0.62, 0.25);
    } else if (!tierra) {
        // mineral: la obsidiana pulida tiene un reflejo de borde frio
        col += fres * (1.0 - rug) * vec3(0.20, 0.22, 0.26);
    }
    if (uBorde.x > 0.001 && !agua && (fam < 1.5 || tierra)) {
        // fase 11 v5: el tinte del secuenciador y de los pads, al borde (fresnel)
        vec3 d = normalize(iVert.pPos);
        vec3 tin = foco(uTinte0, uTinteCol0, d) + foco(uTinte1, uTinteCol1, d) + foco(uTinte2, uTinteCol2, d);
        float borde = 0.15 + 0.85 * pow(1.0 - max(dot(n, v), 0.0), 2.0);
        col += uBorde.x * borde * tin;
    }
    // fase 19: saturacion del modular -> fracturas y glitch en los materiales
    float gl = uGlitch.x;
    if (gl > 0.001) {
        float veta = abs(ruido(q * 0.9 + vec3(3.1)) - 0.5);
        float grieta = 1.0 - smoothstep(0.0, 0.012 + 0.03 * gl, veta);
        col *= 1.0 - 0.85 * grieta * gl;
        float bloque = hash13(vec3(floor(gl_FragCoord.xy / vec2(48.0, 6.0)), floor(uGlitch.y * 12.0)));
        if (bloque < 0.18 * gl)
            col = col.gbr * 1.4 + vec3(0.04, 0.0, 0.06);
    }
    // fase 19: espacialidad del modular -> niebla de distancia
    if (uNiebla.x > 0.001) {
        float dist = length(cam - iVert.wPos);
        float f = uNiebla.x * smoothstep(uNiebla.y, max(uNiebla.y + 0.01, uNiebla.z), dist);
        col = mix(col, uNieblaCol.rgb, f);
    }
    oFragColor[0] = TDOutputSwizzle(vec4(col, 1.0));
    for (int i = 1; i < TD_NUM_COLOR_BUFFERS; i++)
        oFragColor[i] = vec4(0.0);
}
"""


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


ENCUADRE_DEF = 0.85


def add_encuadre(base):
    """El unico parametro del encuadre de la camara de globo (fase 10)."""
    return add_par(base, get_page(base, 'Fase10'), 'float', 'Encuadre',
                   'Alto del planeta en la pantalla (1 = de borde a borde)', ENCUADRE_DEF, 0.3, 1.0, clamp=True)


def camara_al_dia(base):
    """En un proyecto en la fase 10 o mas: el encuadre es un solo parametro,
    Encuadre (motor v36). Quita los dos de antes, Encuadremargen y
    Holguraaltura, que confundian."""
    if not has_par(base, 'Camsuave'):
        return False
    quitados = []
    for nm in ('Encuadremargen', 'Holguraaltura'):
        if has_par(base, nm):
            try:
                getattr(base.par, nm).destroy()
                quitados.append(nm)
            except Exception:
                pass
    nuevo = add_encuadre(base)
    if nuevo or quitados:
        ok('camara: Encuadre (alto del planeta en la pantalla, %s)%s'
           % (str(ENCUADRE_DEF).replace('.', ','),
              '; quitados %s' % ' y '.join(quitados) if quitados else ''))
    return True


# --- calibracion de la vista (comun v29, motor v37) ---------------------------
# Los mundos duraban 8 compases (16 s a 120 BPM) y el radio crecia sin tope:
# a los 20 minutos el planeta media 7 veces el nucleo y las formaciones eran
# motas. Ciclomin 16 y Compasesquietos 3 alargan las eras; Cortezamax compacta
# las conchas viejas y Grosormax 1,5 acota la concha de un mundo largo.

CORTEZA_DEF = 4.0
CALIBRACION = [('Ciclomin', 8, 16), ('Compasesquietos', 2, 3), ('Grosormax', 2.0, 1.5)]


def add_corteza(base):
    """Fase 8: la corteza se compacta (motor v37)."""
    return add_par(base, get_page(base, 'Fase8'), 'float', 'Cortezamax',
                   'Corteza maxima: compacta las conchas viejas (0: el radio es el tiempo)',
                   CORTEZA_DEF, 0.0, 12.0)


def growstep_coherente(semilla, umbral_ram):
    """Growstep con el que la formacion sube a escalones iguales de la
    semilla al limite: (1 - Semillafrac) / (Umbralram - 1)."""
    return (1.0 - semilla) / max(1, int(umbral_ram) - 1)


def alturas_coherentes(base):
    """Avisa si la formacion salta al limite de golpe: con Growstep pequeno
    se queda baja hasta Umbralram y entonces sube del tiron."""
    if not all(has_par(base, n) for n in ('Semillafrac', 'Growstep', 'Umbralram')):
        return True
    sf, gs, tb = float(base.par.Semillafrac), float(base.par.Growstep), int(base.par.Umbralram)
    ideal = growstep_coherente(sf, tb)
    antes = min(1.0, sf + max(0, tb - 2) * gs)
    if 1.0 - antes > 2.0 * ideal + 1e-6:
        info('alturas: con Growstep %.2f la formacion va del %d %% al limite de golpe al llegar a '
             'Umbralram %d; sin salto: Growstep %.2f (lo pone ajuste_vista.py)'
             % (gs, int(round(antes * 100)), tb, ideal))
        return False
    return True


def calibracion_al_dia(base):
    """Los valores nuevos de la calibracion, solo donde seguian en el defecto
    viejo (lo ajustado a mano se respeta), y Cortezamax en la pagina Fase8."""
    for nombre, viejo, nuevo in CALIBRACION:
        renew_default(base, nombre, viejo, nuevo)
    if has_par(base, 'Grosormax') and add_corteza(base):
        ok('conchas: Cortezamax %s (las conchas viejas se compactan; el planeta deja de engordar)'
           % str(CORTEZA_DEF).replace('.', ','))
    alturas_coherentes(base)


# --- el tiempo en el paisaje (comun v30, motor v39) ---------------------------
LUZ_TIEMPO = "parent().op('motor').module.luz_tiempo(%d, absTime.frame)"


def tiempo_al_dia(base):
    """Desde la fase 17, el color de luz_principal lo da el motor: la luz
    cenital fria de la fase 10 tenida por la estacion del pattern que suena."""
    if current_level(base) < 17:
        return False
    luz = base.op('luz_principal')
    if luz is None:
        return False
    hechos = 0
    for k, ch in enumerate('rgb'):
        for pat in ('c%s', 'lightcolor%s', 'color%s'):
            if has_par(luz, pat % ch) and setexpr(luz, pat % ch, LUZ_TIEMPO % k):
                hechos += 1
                break
    return hechos == 3


# --- las senales del modular (comun v32, motor v41) ----------------------------
NIEBLA_CAM = "parent().op('motor').module.niebla_camara('%s', absTime.frame)"


def modular_al_dia(base):
    """Desde la fase 19, la niebla de la camara sigue a la espacialidad del
    modular (para los materiales Phong y constantes; la piel la calcula en su
    shader)."""
    if current_level(base) < 19:
        return False
    cam = base.op('camara')
    if cam is None:
        return False
    bien = bool(setmenu(cam, ['fog'], ['linear'], 1))      # sin espacio, la niebla empieza lejisimos
    bien = setexpr(cam, 'fognear', NIEBLA_CAM % 'cerca') and bien
    bien = setexpr(cam, 'fogfar', NIEBLA_CAM % 'lejos') and bien
    for ch, v in zip('rgb', (0.12, 0.13, 0.16)):
        setp_any(cam, ['fogcolor' + ch], v)
    return bien


def reticula_giro(base):
    """Cada marca de la reticula gira con los canales rx ry rz del
    reticula_chop, como las demas geometrias. fase12_base.py usaba "rotar
    hacia un vector" (Rotate To X/Y/Z = nx ny nz): en los polos la normal es
    paralela al vector arriba y TouchDesigner avisa ('co-linear with the Up
    Vector') y deja esas marcas sin girar."""
    geo = base.op('reticula')
    if geo is None:
        return False
    bien = True
    for par_name, chan in [('instancerx', 'rx'), ('instancery', 'ry'), ('instancerz', 'rz')]:
        bien = setp(geo, par_name, chan) and bien
    setp(geo, 'instancerord', 'xyz')
    for par_name in ('instancerottox', 'instancerottoy', 'instancerottoz'):
        setp(geo, par_name, '')
    if bien:
        ok('reticula: cada marca gira con rx ry rz (sin "rotar hacia un vector")')
    else:
        fail('reticula: no pude enlazar el giro; Instance -> Rotate X/Y/Z = rx ry rz '
             'y vacia Rotate To X/Y/Z')
    return bien


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
    reticula_giro(base)
    camara_al_dia(base)
    calibracion_al_dia(base)
    tiempo_al_dia(base)
    modular_al_dia(base)

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
    piel_al_dia(base, motor.module)
    return motor


def piel_al_dia(base, m):
    """Con la piel ya montada (nivel 12 o mas): el shader de la piel al dia y
    cada geometria de modelo con el material de su familia (motor v32: los
    arboles y brotes pasan del mineral al vegetal, mat_piel_dosel). Sin
    rehacer las geometrias."""
    try:
        c = m.cfg()
        if c['nivel'] < 12 or base.op('mat_piel_dosel') is None:
            return
        materiales_piel(base)
        cambiadas = 0
        for g, mo, mat in m.geometrias_piel(c):
            geo = base.op(g)
            if geo is None or mo.startswith('ciu_'):
                continue
            expr = "'mat_respaldo' if parent().par.Materialrespaldo else '%s'" % mat
            p = getattr(geo.par, 'material', None)
            if p is not None and getattr(p, 'expr', '') != expr:
                setexpr(geo, 'material', expr)
                cambiadas += 1
        if cambiadas:
            ok('piel: %d geometrias con el material de su familia (la vegetacion, mat_piel_dosel)'
               % cambiadas)
        if base.op('terreno') is not None:      # fase 11 v5: la malla del relieve, al dia
            setp(base.op('terreno'), 'material', 'mat_piel_tierra')
    except Exception as e:
        info('piel: no pude poner al dia los materiales (%s); relanza fase12_moduladores.py' % e)
    conchas_al_dia(base, m)


def conchas_al_dia(base, m):
    """Desde la fase 15, las losetas de las conchas usan el shader de la piel
    (familia mineral) con la rugosidad de cada loseta en el canal 'a': el
    carbon brilla, el hormigon es mate. Materialrespaldo vuelve a un Phong."""
    try:
        if m.cfg()['nivel'] < 15:
            return False
        geo = base.op('estratos')
        if geo is None or base.op('mat_piel_mineral') is None:
            return False
        bien = bool(setp_any(geo, ['instancea'], 'a'))
        setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else 'mat_piel_mineral'")
        if bien:
            ok('conchas: shader de la piel (carbon brillante, basalto, hormigon mate; rugosidad en a)')
        else:
            fail('estratos no lee la rugosidad: Instance 2 -> Color A = a')
        return bien
    except Exception as e:
        info('conchas: no pude ponerles el shader de la piel (%s)' % e)
        return False


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
    install_luz_conchas(base, page)
    set_render(base)
    return geo


def install_luz_conchas(base, page):
    """La luz de los secuenciadores en las conchas de la celda (motor v25):
    una capa aditiva sobre sus losetas superiores. Se ve desde la fase 8."""
    add_par(base, page, 'toggle', 'Luzconchas', 'Luz de los secuenciadores en las conchas', True)
    add_par(base, page, 'float', 'Luzconchaspulso', 'Luz en las conchas: pulso de la nota',
            0.35, 0.0, 1.0)
    add_par(base, page, 'float', 'Luzconchasreposo', 'Luz en las conchas: reposo (ultima celda)',
            0.10, 0.0, 1.0)
    add_par(base, page, 'int', 'Luzconchasalcance', 'Luz en las conchas: losetas que alcanza',
            4, 1, 24, clamp=True)
    mat = make_constant(base, 'mat_luz_conchas', 780, 780, (1.0, 1.0, 1.0))
    set_additive(mat)
    geo = make_instanced(base, 'luz_conchas', 520, 780, 'mat_luz_conchas')
    bien, det = instance_color_ok(geo)
    if not bien:
        fail('luz_conchas no lee el color por instancia (%s): Instance 2 -> Color R/G/B = '
             'r g b, Color Mode = Replace' % det)
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


# Lo que el motor no mueve de la camara: giro, pivote y escala en su valor
# neutro. Navegar en el visor de la camara (girar, acercar) los cambia; con un
# giro alrededor de un pivote lejano la camara mira a otra parte y no se ve
# nada (comun v28).
CAM_NEUTRO = (('rx', 0.0), ('ry', 0.0), ('rz', 0.0), ('px', 0.0), ('py', 0.0), ('pz', 0.0),
              ('sx', 1.0), ('sy', 1.0), ('sz', 1.0), ('scale', 1.0))


def camara_neutra(cam):
    """Pone giro, pivote y escala de la camara en su valor neutro. Devuelve
    los parametros que estaban movidos."""
    movidos = []
    for ax, v in CAM_NEUTRO:
        p = getattr(cam.par, ax, None)
        if p is None:
            continue
        try:
            if abs(float(p.eval()) - v) > 1e-6:
                movidos.append(ax)
        except Exception:
            pass
        try:
            p.expr = ''
        except Exception:
            pass
        try:
            p.mode = ParMode.CONSTANT
        except Exception:
            pass
        setp(cam, ax, v)
    return movidos


def set_camera(base):
    """Camara de globo (motor v24): el planeta entero, centrado y tan cerca
    como permite el cuadro. Posicion y planos de recorte los da el motor.
    Si existe 'objetivo' (fase 10) mira a el; si no, mira al centro desde +Z.
    Giro, pivote y escala vuelven a su valor neutro (camara_neutra)."""
    cam = base.op('camara')
    if cam is None:
        fail('no encuentro la camara')
        return False
    good = all(setexpr(cam, ax, CAM_EXPR % ('pos', k)) for k, ax in enumerate(('tx', 'ty', 'tz')))
    obj = base.op('objetivo')
    if obj is not None:
        setp(cam, 'lookat', 'objetivo')
    movidos = camara_neutra(cam)
    if movidos:
        info('camara: %s estaban movidos (se navego en su visor); vuelven a cero. Para mirar '
             'el planeta usa el visor del render, no el de la camara' % ' '.join(movidos))
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
    piel = [n for n in names if n.startswith(PIEL_PREFIJO)]
    resto = [n for n in names if not n.startswith(PIEL_PREFIJO)]
    ok('balanceo del eje en %d geometrias (%s%s): Rotextra, Balanceo, Balanceoper'
       % (len(names), ', '.join(resto), ' y %d de modelos' % len(piel) if piel else ''))
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


def make_instanced(base, name, x, y, mat, sop='box', quiet=False):
    """Geometry COMP 'name' + Script CHOP 'i_name' que pide al motor sus
    instancias. Una caja de 1x1x1 con la base en y=0 (o una esfera de radio
    1, o con sop='select:<ruta>' el SOP de un modelo), escalada, girada y
    coloreada por instancia."""
    chop = fresh(base, 'scriptCHOP', 'i_' + name, x - 220, y)
    setp_any(chop, ['callbacks', 'callbackdat', 'dat'], 'formas_callbacks')
    geo = fresh(base, 'geometryCOMP', name, x, y)
    for k in list(geo.children):
        try:
            k.render = False
            k.display = False
        except Exception:
            pass
    if sop.startswith('select:'):
        s = mk(geo, 'selectSOP', 'modelo', 0, 0)
        if not setp_any(s, ['sop', 'sops', 'soppath'], sop.split(':', 1)[1]):
            info('%s: no encontre el parametro SOP del Select SOP; pon a mano %s'
                 % (name, sop.split(':', 1)[1]))
    elif sop == 'sphere':
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
    if not quiet:
        ok('%s: geometria instanciada desde i_%s, gira con el planeta' % (name, name))
    return geo


# El color x dimmer de cada luz lo da el motor: la Light COMP llama a su color
# cr cg cb (no lightcolorr...), y asi no depende del nombre.
LUZ_COL = "parent().op('motor').module.luz_color('%s', %d, absTime.frame)"
COLOR_LUZ = ('c%s', 'lightcolor%s')      # nombres del color de una Light COMP, por orden


def color_luz(luz, rgb):
    """Fija el color de una Light COMP (cr cg cb). Devuelve el nombre usado."""
    usado = None
    for ch, v in zip('rgb', rgb):
        usado = setp_any(luz, [pat % ch for pat in COLOR_LUZ], v) or usado
    return usado


def color_luz_expr(luz, exprs):
    """Pone expresiones al color de una Light COMP (cr cg cb)."""
    usado = None
    for ch, e in zip('rgb', exprs):
        for pat in COLOR_LUZ:
            if setexpr(luz, pat % ch, e):
                usado = pat % ch
                break
    return usado


MODULAR_U = "parent().op('motor').module.modular_uniforme('%s', %d, absTime.frame)"
PIEL_U = "parent().op('motor').module.piel_uniforme('%s', %d, absTime.frame)"
PIEL_UNIFORMES = [
    ('uFamilia', ('%d', '0', '0', '0')),
    ('uLuz0', ("parent().op('luz_principal').par.tx", "parent().op('luz_principal').par.ty",
               "parent().op('luz_principal').par.tz", '0')),
    ('uLuz0Col', tuple(LUZ_COL % ('luz_principal', k) for k in range(3)) + ('0',)),
    ('uLuz1', ("parent().op('luz_relleno').par.tx", "parent().op('luz_relleno').par.ty",
               "parent().op('luz_relleno').par.tz", '0')),
    ('uLuz1Col', tuple(LUZ_COL % ('luz_relleno', k) for k in range(3)) + ('0',)),
    ('uLuz2', ("parent().op('luz_destello').par.tx", "parent().op('luz_destello').par.ty",
               "parent().op('luz_destello').par.tz", '0')),
    ('uLuz2Col', tuple(LUZ_COL % ('luz_destello', k) for k in range(3)) + ('0',)),
    ('uAmbiente', ('0.16', '0.16', '0.18', '0')),
    ('uVentanas', ("parent().op('motor').module.ventanas_luz(absTime.frame)", '0', '0', '0')),  # fase 17
    ('uNiebla', tuple(MODULAR_U % ('niebla', k) for k in range(4))),           # fase 19
    ('uNieblaCol', tuple(MODULAR_U % ('nieblacol', k) for k in range(4))),
    ('uGlitch', tuple(MODULAR_U % ('glitch', k) for k in range(4))),
    # fase 11 v5: terreno, pisos, borde tintado y agua (uTerreno.x y .w los pone materiales_piel)
    ('uTerreno', ('0', PIEL_U % ('uTerreno', 1), PIEL_U % ('uTerreno', 2), '0')),
    ('uPisos', tuple(PIEL_U % ('uPisos', k) for k in range(3)) + ('0',)),
    ('uBorde', (PIEL_U % ('uBorde', 0), '0', '0', '0')),
] + [(nm % k, tuple(PIEL_U % (nm % k, q) for q in range(4)))
     for k in range(3) for nm in ('uTinte%d', 'uTinteCol%d')] + [
    ('uAgua', (PIEL_U % ('uAgua', 0), '0', '0', '0')),
    # fase 11 v8: hojas, bancales y mesetas
    ('uHojas', (PIEL_U % ('uHojas', 0), '0', '0', '0')),
    ('uCultivo', tuple(PIEL_U % ('uCultivo', q) for q in range(4))),
    ('uBancal', tuple(PIEL_U % ('uBancal', q) for q in range(4))),
    ('uRiego', tuple(PIEL_U % ('uRiego', q) for q in range(3)) + ('0',)),
]
FAMILIAS_PIEL = ['mineral', 'dosel', 'ciudad', 'tierra', 'agua']
# familias que no necesitan los focos del tinte ni los pisos: constantes (no se evaluan)
SIN_TINTE = ('ciudad', 'agua')
PIEL_SAMPLERS = [('sAlturas', 'alturas'), ('sRampa', 'rampa_hipso'), ('sCultivo', 'cultivos')]


def _uniforme(mat, k, nombre, valores):
    """Uniforme vec4 k del GLSL MAT (pagina Vectors): nombre y cuatro valores,
    numeros o expresiones."""
    bien = setp(mat, 'vec%dname' % k, nombre)
    for comp, v in zip('xyzw', valores):
        par = 'vec%dvalue%s' % (k, comp)
        try:
            bien = setp(mat, par, float(v)) and bien
        except ValueError:
            bien = setexpr(mat, par, v) and bien
    return bien


ALTURAS_CB = r'''# Script TOP 'alturas' (fase 11 v5): el mapa de alturas del relieve que pide
# al motor (lat/lon, 512 x 256, float32): r el relieve sobre el suelo local,
# g el radio del suelo. El motor lo recuece solo cuando el mapa cambia.

def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    try:
        a = op('motor').module.alturas_array()
    except Exception as e:
        a = None
        print('AVISO  alturas: %s' % e)
    if a is not None:
        scriptOp.copyNumpyArray(a)
    return
'''


CULTIVOS_CB = r'''# Script TOP 'cultivos' (fase 11 v8): los hibridos de la naturaleza que pide
# al motor (lat/lon, 512 x 256, float32): r el relieve sin aterrazar, g el tope
# de los bancales, b desde donde se inundan, a el nivel de la meseta (+10 con
# acequia). El motor lo recuece solo cuando cambia.

def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    try:
        a = op('motor').module.cultivos_array()
    except Exception as e:
        a = None
        print('AVISO  cultivos: %s' % e)
    if a is not None:
        scriptOp.copyNumpyArray(a)
    return
'''


def mapas_terreno(base):
    """Las texturas del terreno (fase 11 v5): el Script TOP 'alturas' (el mapa
    de alturas del motor, float32) y el Ramp TOP 'rampa_hipso' con sus claves en
    la tabla 'rampa_hipso_claves' (los pisos de color; el motor la reescribe si
    cambian Limitebosque o Limitenieve). Devuelve True si estan."""
    bien = True
    cb = get_or_make(base, 'textDAT', 'alturas_callbacks', 960, 1180)
    cb.text = ALTURAS_CB
    top = get_or_make(base, 'scriptTOP', 'alturas', 1180, 1180)
    bien = bool(setp_any(top, ['callbacks', 'callbackdat', 'dat'], 'alturas_callbacks')) and bien
    if not (setmenu(top, ['format', 'pixelformat'], ['rgba32float', '32bit float (RGBA)'])
            or setp_any(top, ['format', 'pixelformat'], 'rgba32float')):
        info('alturas: pon a mano Pixel Format = 32-bit float (RGBA) en el Script TOP')
    try:
        top.cook(force=True)
    except Exception:
        pass
    cb2 = get_or_make(base, 'textDAT', 'cultivos_callbacks', 960, 1260)     # fase 11 v8
    cb2.text = CULTIVOS_CB
    cu = get_or_make(base, 'scriptTOP', 'cultivos', 1180, 1260)
    bien = bool(setp_any(cu, ['callbacks', 'callbackdat', 'dat'], 'cultivos_callbacks')) and bien
    if not (setmenu(cu, ['format', 'pixelformat'], ['rgba32float', '32bit float (RGBA)'])
            or setp_any(cu, ['format', 'pixelformat'], 'rgba32float')):
        info('cultivos: pon a mano Pixel Format = 32-bit float (RGBA) en el Script TOP')
    try:
        cu.cook(force=True)
    except Exception:
        pass
    tab = get_or_make(base, 'tableDAT', 'rampa_hipso_claves', 960, 1100)
    try:
        m = base.op('motor').module
        tab.clear()
        for f in m.rampa_filas(m.cfg()):
            tab.appendRow(f)
    except Exception:
        bien = False
    ramp = get_or_make(base, 'rampTOP', 'rampa_hipso', 1180, 1100)
    bien = bool(setp_any(ramp, ['dat'], 'rampa_hipso_claves')) and bien
    setmenu(ramp, ['type'], ['horizontal'])
    setmenu(ramp, ['outputresolution'], ['custom'])
    setp_any(ramp, ['resolutionw'], 256)
    setp_any(ramp, ['resolutionh'], 1)
    return bien


def _samplers(mat):
    """Los samplers de la piel: sAlturas (el mapa de alturas) y sRampa (los
    pisos). True si se pudieron enlazar."""
    try:                             # TouchDesigner 2022+: la pagina Samplers es una secuencia
        sec = mat.seq.sampler
        if sec.numBlocks < len(PIEL_SAMPLERS):
            sec.numBlocks = len(PIEL_SAMPLERS)
    except Exception:
        pass
    bien = True
    for k, (nombre, top) in enumerate(PIEL_SAMPLERS):
        bien = bool(setp(mat, 'sampler%dname' % k, nombre)) and bien
        bien = bool(setp_any(mat, ['sampler%dtop' % k], top)) and bien
        setmenu(mat, ['sampler%dextendu' % k], ['repeat'])
        setmenu(mat, ['sampler%dextendv' % k], ['hold'])
    return bien


def materiales_piel(base):
    """El shader de la piel (fase 12): un GLSL MAT por familia de material
    (mat_piel_mineral, mat_piel_dosel, mat_piel_ciudad; desde la fase 11 v5,
    mat_piel_tierra para el relieve y mat_piel_agua para los rios) que lee la
    rugosidad del alfa de cada instancia, y mat_respaldo (Phong) para
    Materialrespaldo. Tambien las texturas del terreno (mapas_terreno)."""
    vdat = get_or_make(base, 'textDAT', 'piel_vertex', 1180, 1020)
    vdat.text = PIEL_VERTEX
    pdat = get_or_make(base, 'textDAT', 'piel_pixel', 1180, 940)
    pdat.text = PIEL_PIXEL
    mapas = mapas_terreno(base)
    malos, sin_rampa = [], []
    for k, fam in enumerate(FAMILIAS_PIEL):
        mat = get_or_make(base, 'glslMAT', 'mat_piel_' + fam, 1400, 1020 - 80 * k)
        bien = bool(setp_any(mat, ['vdat', 'vertexdat'], 'piel_vertex'))
        bien = bool(setp_any(mat, ['pdat', 'pixeldat'], 'piel_pixel')) and bien
        try:                         # TouchDesigner 2022+: la pagina Vectors es una secuencia
            sec = mat.seq.vec
            if sec.numBlocks < len(PIEL_UNIFORMES):
                sec.numBlocks = len(PIEL_UNIFORMES)
        except Exception:
            pass
        rampa = _samplers(mat) and mapas
        if not rampa:
            sin_rampa.append(mat.name)
        for q, (nombre, valores) in enumerate(PIEL_UNIFORMES):
            vals = tuple(v % k if '%d' in v else v for v in valores)
            if nombre == 'uTerreno':
                vals = ('1' if fam == 'tierra' else '0',) + vals[1:3] + ('1' if rampa else '0',)
            elif fam in SIN_TINTE and (nombre.startswith('uTinte') or nombre in ('uPisos', 'uBorde')):
                vals = ('0', '0', '0', '0')
            bien = _uniforme(mat, q, nombre, vals) and bien
        if not bien:
            malos.append(mat.name)
    make_phong(base, 'mat_respaldo', 1400, 780, spec=0.5, shin=24, diff=1.0, amb=0.22, emit=0.03)
    if malos:
        info('%s: no pude fijar los shaders o los uniformes (Vertex/Pixel Shader = piel_vertex / '
             'piel_pixel; Vectors: uFamilia, uLuz0...); si la piel no se ve, Materialrespaldo'
             % ', '.join(malos))
    else:
        ok('shader de la piel: mat_piel_mineral, mat_piel_dosel, mat_piel_ciudad, mat_piel_tierra y '
           'mat_piel_agua (GLSL), mat_respaldo (Phong)')
    if sin_rampa:
        info('%s: no pude enlazar los samplers sAlturas (TOP alturas) y sRampa (TOP rampa_hipso) en la '
             'pagina Samplers; sin ellos no se levanta el relieve' % ', '.join(sin_rampa[:2]))
    return not malos


# -----------------------------------------------------------------------------
# MODELOS DE LA PIEL (fase 11): los SOP de cada modelo, dentro de 'modelos'
# -----------------------------------------------------------------------------
# Cada pieza es un Transform SOP sobre una caja o un prisma hexagonal unidad
# (centrados en el origen, de lado 1); el modelo es su Merge, y su salida el
# Null 'salida'. Las geometrias instanciadas lo traen con un Select SOP.

def unir(src, dst, k):
    try:
        src.outputConnectors[0].connect(dst)
        return True
    except Exception:
        return connect(dst, src, k)


def medir(sop):
    """(xmin, xmax, ymin, ymax, zmin, zmax) de los puntos de un SOP, o None
    si no se pueden leer."""
    try:
        pts = list(sop.points)
        if not pts:
            return None
        xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
        return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
    except Exception:
        return None


def a_la_unidad(comp, sop, nombre, ajustadas):
    """Un Transform SOP que deja el SOP en el cubo unidad centrado, midiendo
    sus puntos: si algun parametro de la caja o del prisma no se fijo (radio,
    alto, centro), las piezas no se deforman."""
    aj = mk(comp, 'transformSOP', sop.name + '_unidad', 100, sop.nodeY)
    connect(aj, sop, 0)
    b = medir(sop)
    if b is not None:                # el hexagono no mide lo mismo en x y en z: escala comun
        kxz = 1.0 / max(1e-6, b[1] - b[0], b[5] - b[4])
        k = [kxz, 1.0 / max(1e-6, b[3] - b[2]), kxz]
        c = [(b[0] + b[1]) / 2.0, (b[2] + b[3]) / 2.0, (b[4] + b[5]) / 2.0]
        if max(abs(v - 1.0) for v in k) > 1e-3 or max(abs(v) for v in c) > 1e-3:
            ajustadas.append('%s/%s' % (nombre, sop.name))
        setmenu(aj, ['xord'], ['srt'], 0)
        for q, ax in enumerate('xyz'):
            setp(aj, 's' + ax, k[q])
            setp(aj, 't' + ax, -c[q] * k[q])
    return aj


def punta_arriba(comp, cono):
    """El cono con la punta hacia +Y: si el Tube SOP deja el radio 0 abajo (el
    orden de rad1 y rad2 depende de la version), se le da la vuelta midiendo
    sus puntos."""
    xf = mk(comp, 'transformSOP', 'cono_arriba', 100, cono.nodeY - 60)
    connect(xf, cono, 0)
    try:
        pts = list(cono.points)
        if pts:
            ys = [p.y for p in pts]
            arriba = [abs(p.x) + abs(p.z) for p in pts if p.y > (max(ys) + min(ys)) / 2.0]
            abajo = [abs(p.x) + abs(p.z) for p in pts if p.y <= (max(ys) + min(ys)) / 2.0]
            if arriba and abajo and max(arriba) > max(abajo):
                setp(xf, 'rx', 180.0)
    except Exception:
        pass
    return xf


def construir_modelo(modelos, nombre, prims, x, y, ajustadas):
    comp = fresh(modelos, 'baseCOMP', nombre, x, y)
    fuentes = {}
    if any(p[0] == 'caja' for p in prims):
        caja = mk(comp, 'boxSOP', 'caja', 0, 0)
        for ax in ('sizex', 'sizey', 'sizez'):
            setp(caja, ax, 1.0)
        for ax in ('tx', 'ty', 'tz'):
            setp(caja, ax, 0.0)
        fuentes['caja'] = a_la_unidad(comp, caja, nombre, ajustadas)
    if any(p[0] == 'hexa' for p in prims):
        hexa = mk(comp, 'tubeSOP', 'hexa', 0, -120)
        bien = all([setp_any(hexa, ['rad1'], 0.5), setp_any(hexa, ['rad2'], 0.5),
                    setp(hexa, 'height', 1.0), setp_any(hexa, ['cols', 'columns'], 6)])
        setp_any(hexa, ['rows'], 2)
        setp_any(hexa, ['caps', 'endcaps', 'capends'], True)
        setmenu(hexa, ['orient', 'orientation'], ['y'], 1)
        for ax in ('tx', 'ty', 'tz'):
            setp(hexa, ax, 0.0)
        if not bien:
            info('%s: no pude fijar el prisma hexagonal (Tube SOP: radio 0,5, alto 1, 6 columnas, '
                 'eje Y, con tapas); ponlo a mano en modelos/%s/hexa' % (nombre, nombre))
        fuentes['hexa'] = a_la_unidad(comp, hexa, nombre, ajustadas)
    if any(p[0] == 'bola' for p in prims):       # fase 11 v5: copas redondas (pocas caras)
        bola = mk(comp, 'sphereSOP', 'bola', 0, -240)
        for ax in ('radx', 'rady', 'radz'):
            setp(bola, ax, 0.5)
        setmenu(bola, ['type', 'primtype'], ['polygon', 'poly'])
        setp_any(bola, ['rows'], 6)
        setp_any(bola, ['cols'], 10)
        for ax in ('tx', 'ty', 'tz'):
            setp(bola, ax, 0.0)
        fuentes['bola'] = a_la_unidad(comp, bola, nombre, ajustadas)
    if any(p[0] == 'cono' for p in prims):       # fase 11 v5: coniferas (Tube SOP con un radio 0)
        cono = mk(comp, 'tubeSOP', 'cono', 0, -360)
        setp_any(cono, ['rad1'], 0.5)
        setp_any(cono, ['rad2'], 0.0)
        setp(cono, 'height', 1.0)
        setp_any(cono, ['cols', 'columns'], 8)
        setp_any(cono, ['rows'], 2)
        setp_any(cono, ['caps', 'endcaps', 'capends'], True)
        setmenu(cono, ['orient', 'orientation'], ['y'], 1)
        for ax in ('tx', 'ty', 'tz'):
            setp(cono, ax, 0.0)
        fuentes['cono'] = a_la_unidad(comp, punta_arriba(comp, cono), nombre, ajustadas)
    todo = mk(comp, 'mergeSOP', 'todo', 400, 0)
    for k, p in enumerate(prims):
        xf = mk(comp, 'transformSOP', 'p%d' % k, 200, -60 * k)
        connect(xf, fuentes[p[0]], 0)
        for ax, v in zip(('tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'rx', 'ry', 'rz'), p[1:10]):
            setp(xf, ax, float(v))
        setmenu(xf, ['xord'], ['srt'], 0)
        setmenu(xf, ['rord'], ['xyz'], 0)
        unir(xf, todo, k)
    out = mk(comp, 'nullSOP', 'salida', 600, 0)
    connect(out, todo, 0)
    for attr in ('render', 'display'):
        try:
            setattr(out, attr, True)
        except Exception:
            pass
    return comp


EJEMPLAR_CB = r'''# Script SOP de un ejemplar de la biblioteca (fase 11 v8): pide al motor la
# malla del ejemplar con el nombre de su COMP (veg_<modelo>_<variante>_<derivacion>
# y _lod, la version lejana con tarjetas de racimo) y la escribe una vez: ramas
# (tubos de 4 o 5 lados) y hojas facetadas. Atributos: N y uv = (tipo,
# profundidad en la copa, nivel de rama). Solo se recuece si cambia la
# biblioteca (Varangulo, Cuantizar30, Densidadhoja).

def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    try:
        m = parent(2).op('motor').module
        P, Nn, U, T = m.malla_ejemplar(scriptOp.parent().name, m.cfg())
    except Exception as e:
        print('AVISO  %s: %s' % (scriptOp.parent().name, e))
        return
    for nm in ('N', 'uv'):
        try:
            scriptOp.pointAttribs.create(nm, (0.0, 0.0, 0.0))
        except Exception:
            pass
    pts = []
    for k in range(len(P)):
        p = scriptOp.appendPoint()
        p.P = P[k]
        try:
            p.N = Nn[k]
            p.uv = U[k]
        except Exception:
            pass
        pts.append(p)
    for a, b, c in T:
        poly = scriptOp.appendPoly(3, closed=True, addPoints=False)
        poly[0].point = pts[a]
        poly[1].point = pts[b]
        poly[2].point = pts[c]
    return
'''


def construir_ejemplar(modelos, nombre, x, y):
    """Fase 11 v8: el COMP de un ejemplar de la biblioteca, con su Script SOP
    (callbacks: modelos/ejemplar_callbacks) y la salida."""
    comp = fresh(modelos, 'baseCOMP', nombre, x, y)
    s = mk(comp, 'scriptSOP', 'malla', 0, 0)
    setp_any(s, ['callbacks', 'callbackdat', 'dat'], '../ejemplar_callbacks')
    out = mk(comp, 'nullSOP', 'salida', 200, 0)
    connect(out, s, 0)
    for attr in ('render', 'display'):
        try:
            setattr(out, attr, True)
        except Exception:
            pass
    return comp


def construir_modelos(base, m, solo_nuevos=False):
    """Los SOP de cada modelo del motor, dentro de 'modelos' (fase 11). Con
    solo_nuevos conserva los que ya estan y anade los que falten (los de una
    fase posterior). Devuelve (modelos, modelos hechos, piezas, ajustadas)."""
    modelos = base.op('modelos')
    if modelos is None or not solo_nuevos:
        modelos = fresh(base, 'baseCOMP', 'modelos', 1100, 900)
    ajustadas = []
    hechos = piezas = 0
    for k, nm in enumerate(sorted(m.MODELOS)):
        if solo_nuevos and modelos.op(nm) is not None:
            continue
        construir_modelo(modelos, nm, m.MODELOS[nm], (k % 8) * 220, -(k // 8) * 160, ajustadas)
        hechos += 1
        piezas += len(m.MODELOS[nm])
    # fase 11 v8: la biblioteca de ejemplares (un Script SOP por ejemplar)
    cb = get_or_make(modelos, 'textDAT', 'ejemplar_callbacks', -440, 200)
    cb.text = EJEMPLAR_CB
    c = m.cfg()
    m.VARIANTES_TD = 0
    m.biblioteca(c)
    nombres = m.ejemplares_de(c)
    fila0 = len(m.MODELOS) // 8 + 2
    for k, nm in enumerate(nombres):
        if solo_nuevos and modelos.op(nm) is not None:
            continue
        construir_ejemplar(modelos, nm, (k % 12) * 220, -(fila0 + k // 12) * 160)
        hechos += 1
    m.VARIANTES_TD = m.variantes(c)
    try:
        base.op('motor').store('variantes_td', m.VARIANTES_TD)
    except Exception:
        pass
    return modelos, hechos, piezas, ajustadas


def catalogo_al_dia(base, m):
    """La tabla 'catalogo' con las filas por defecto del motor, salvo que se
    haya editado a mano (entonces se conserva y se avisa de lo que no existe).
    Devuelve el numero de filas o None si se conserva la editada."""
    filas_def = [list(m.CATALOGO_COLS)] + [[str(x) for x in f] for f in m.CATALOGO_FILAS]
    cat = get_or_make(base, 'tableDAT', 'catalogo', -440, -480)
    actual = [[cell.val for cell in cat.row(r)] for r in range(cat.numRows)]
    if not actual or actual[0][:5] != list(m.CATALOGO_COLS) or actual == cat.fetch('defecto', None):
        cat.clear()
        for f in filas_def:
            cat.appendRow(f)
        cat.store('defecto', filas_def)
        return len(filas_def) - 1
    if actual == filas_def:
        cat.store('defecto', filas_def)
        return len(filas_def) - 1
    if actual != filas_def:
        for r in actual[1:]:
            if len(r) > 4 and r[4] not in m.MODELOS and r[4] not in m.ETAPAS:
                fail('catalogo: el modelo o etapa %r no existe; se ignora' % r[4])
    return None


def instanciar_modelos(base, m):
    """Las geometrias de los modelos de la piel, las que pide el motor para el
    nivel actual: en la fase 11, pulida (mat_pulido) y porosa (mat_poroso);
    desde la fase 12, una por modelo, con el shader de su familia, la
    rugosidad en el canal 'a' y Materialrespaldo para volver a un Phong. Borra
    las que hubiera."""
    c = m.cfg()
    doce = c['nivel'] >= 12
    if doce:
        materiales_piel(base)
    for nm in [o.name for o in base.children if o.name.startswith(PIEL_PREFIJO)]:
        for viejo in (nm, 'i_' + nm):
            o = base.op(viejo)
            if o is not None:
                try:
                    o.destroy()
                except Exception:
                    pass
    modelos = base.op('modelos')
    geos, sin_color, sin_alfa = m.geometrias_piel(c), [], []
    for k, (g, mo, mat) in enumerate(geos):
        geo = make_instanced(base, g, 1400 + (k % 8) * 180, 600 - (k // 8) * 110, mat,
                             sop='select:%s/%s/salida' % (modelos.path, mo), quiet=True)
        if not instance_color_ok(geo)[0]:
            sin_color.append(g)
        if doce and not mo.startswith('ciu_'):
            if not setp_any(geo, ['instancea'], 'a'):
                sin_alfa.append(g)
            setexpr(geo, 'material', "'mat_respaldo' if parent().par.Materialrespaldo else '%s'" % mat)
    if doce:
        ok('%d geometrias de modelos (mod_...): una por modelo, con el shader de su familia '
           '(Materialrespaldo: Phong); giran con el planeta' % len(geos))
    else:
        ok('%d geometrias de modelos (mod_...): pulidas con mat_pulido, porosas y obras con mat_poroso; '
           'giran con el planeta' % len(geos))
    for g in sin_color[:3]:
        fail('%s no lee el color por instancia: Instance 2 -> Color R/G/B = r g b, Color Mode = Replace' % g)
    for g in sin_alfa[:3]:
        fail('%s no lee la rugosidad: Instance 2 -> Color A = a' % g)
    return geos


TERRENO_FILAS, TERRENO_COLS = 256, 512      # la malla, del tamano del mapa de alturas


def terreno_al_dia(base, m=None):
    """La malla del relieve (fase 11 v5): una sola esfera de radio 1
    ('terreno', Sphere SOP de 256 x 512) que el shader de la piel
    (mat_piel_tierra) desplaza con el mapa de alturas del motor y colorea con
    los pisos. Gira con el planeta. No es instanciada: el relieve de todas
    las celdas es una sola malla. Devuelve la geometria."""
    materiales_piel(base)
    geo = base.op('terreno')
    if geo is None or str(getattr(geo, 'OPType', '')) != 'geometryCOMP':
        geo = fresh(base, 'geometryCOMP', 'terreno', 520, 1020)
        for k in list(geo.children):
            try:
                k.destroy()
            except Exception:
                pass
    s = geo.op('esfera') or mk(geo, 'sphereSOP', 'esfera', 0, 0)
    for ax in ('radx', 'rady', 'radz'):
        setp(s, ax, 1.0)
    setmenu(s, ['type', 'primtype'], ['polymesh', 'mesh'])
    bien = bool(setp_any(s, ['rows'], TERRENO_FILAS)) and bool(setp_any(s, ['cols'], TERRENO_COLS))
    for attr in ('render', 'display'):
        try:
            setattr(s, attr, True)
        except Exception:
            pass
    set_spin(geo)
    setp(geo, 'material', 'mat_piel_tierra')
    if not bien:
        info('terreno: pon a mano Rows %d y Columns %d en terreno/esfera (Sphere SOP, Polygon Mesh)'
             % (TERRENO_FILAS, TERRENO_COLS))
    ok('terreno: la malla del relieve (esfera de %d x %d desplazada por el mapa de alturas en '
       'mat_piel_tierra; texturas alturas y rampa_hipso)' % (TERRENO_FILAS, TERRENO_COLS))
    return geo


def set_render(base):
    names = [n for n in RENDER_ORDER if base.op(n) is not None]
    piel = sorted(o.name for o in base.children if o.name.startswith(PIEL_PREFIJO)
                  and str(getattr(o, 'OPType', '')) == 'geometryCOMP')
    if piel:                         # los modelos de la fase 11, tras las formas
        k = names.index('coronas') if 'coronas' in names else len(names)
        names = names[:k] + piel + names[k:]
    lights = [n for n in LIGHT_ORDER if base.op(n) is not None]
    r = base.op('render')
    a = setp(r, 'geometry', ' '.join(names))
    b = setp(r, 'lights', ' '.join(lights))
    if a:
        resto = [n for n in names if not n.startswith(PIEL_PREFIJO)]
        ok('render dibuja: %s' % ' '.join(resto)
           + ('  y %d geometrias de modelos (mod_...)' % (len(names) - len(resto))
              if len(resto) < len(names) else ''))
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
