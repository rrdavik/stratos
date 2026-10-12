"""
=============================================================================
ESTRATOS - FASE 1+2: LA BASE (NUCLEO, RETICULA, LUZ DE CELDA Y MIDI)
=============================================================================
Sustituye a fase1_tempo_beatstep.py y fase2_seq1_baliza.py, y lleva dentro
el arreglo del render (fix_render_fase2.py ya no hace falta).

QUE CONSTRUYE
-------------
  - el nucleo esferico que gira al TEMPO DEL PROYECTO (lo marca el
    BeatStep a traves de midicontrolx; FASE1 solo lo lee)
  - la RETICULA DE POLO A POLO: cada semitono entre Notapolosur (24, do1)
    y Notapolonorte (108, do8) es una celda. La nota mas grave es el polo
    sur, la mas aguda el polo norte, y las de en medio van en anillos, uno
    por octava (la clase de nota es el meridiano). Pagina Fase3.
  - la LUZ DE CELDA (v3, sustituye a la baliza): cada nota del SEQ1
    enciende en cian el centro de su celda, con un pulso, y la deja tenue
    hasta la siguiente nota. Es la misma luz que da el motor desde la
    fase 3 (mismos nodos: luz_celda, i_luz_celda, mat_luz_celda).
  - la entrada MIDI (nota y canal leidos de los bytes)
  - render, camara, luces y leyenda, y la salida en el nodo 'salida'

EL RENDER
---------
La lista de geometrias del render se ESCRIBE entera desde el principio
('nucleo reticula luz_celda'). Leerla con .eval() y ampliarla la corrompia
(ese parametro referencia operadores): por eso desaparecia la esfera.
Al final, un DIAGNOSTICO DEL RENDER dice que dibuja el render y si algun
nodo de la cadena hasta 'salida' tiene errores.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase12_base.py').read())

Viewer Active sobre 'salida'. Despues, las fases 3 a 10 en orden.

SI YA EXISTE /project1/FASE1
----------------------------
No se borra: se renombra a FASE1_anterior y se apaga (si dentro hay
midicontrolx o master_beat se deja funcionando y se avisa). El mundo de
la anterior NO pasa a la nueva.
=============================================================================
"""

import td
import math

VERSION = 'fase12 v3  (fase 1 + fase 2 + arreglo del render; reticula de polo a polo; luz de celda)'
print('=' * 66)
print('EJECUTANDO: ' + VERSION)
print('=' * 66)

ROOT = op('/project1')
COMP_NAME = 'FASE1'
CORE_RADIUS = 6.0
SEQ1_CHANNEL = 13

# -----------------------------------------------------------------------------
# UTILIDADES
# -----------------------------------------------------------------------------

def mk(parent_comp, optype, name, x, y):
    try:
        o = parent_comp.create(getattr(td, optype), name)
    except Exception:
        o = parent_comp.create(optype, name)
    o.nodeX, o.nodeY = int(x), int(y)
    return o


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


def connect(dst, src, i=0):
    try:
        dst.inputConnectors[i].connect(src)
        return True
    except Exception:
        return False


def flags_on(sop):
    for attr in ('render', 'display'):
        try:
            setattr(sop, attr, True)
        except Exception:
            pass


report = []
def ok(m):   report.append('  OK    ' + m)
def fail(m): report.append('  FALLO ' + m)
def info(m): report.append('  ..    ' + m)




def has_par(o, name):
    try:
        return getattr(o.par, name, None) is not None
    except Exception:
        return False


def fresh(parent_comp, optype, name, x, y):
    old = parent_comp.op(name)
    if old is not None:
        try:
            old.destroy()
        except Exception:
            pass
    return mk(parent_comp, optype, name, x, y)

# -----------------------------------------------------------------------------
# 1. LA FASE1 ANTERIOR: SE GUARDA, NO SE BORRA
# -----------------------------------------------------------------------------

old = ROOT.op(COMP_NAME)
if old is not None:
    new_name = 'FASE1_anterior'
    n = 2
    while ROOT.op(new_name) is not None:
        new_name = 'FASE1_anterior_%d' % n
        n += 1
    old.name = new_name

    keep_alive = []
    for pattern in ('midicontrolx*', 'master_beat*'):
        try:
            keep_alive += [o.path for o in old.findChildren(name=pattern, depth=None)]
        except Exception:
            pass
    if keep_alive:
        info('FASE1 anterior guardada como %s y SIGUE FUNCIONANDO, porque '
             'contiene: %s' % (new_name, ', '.join(keep_alive)))
        info('  sacalos de ahi cuando puedas; puede dar algun error rojo por '
             'rutas que apuntaban a /project1/FASE1')
    else:
        try:
            old.allowCooking = False
            ok('FASE1 anterior guardada como %s y apagada (no se ha borrado nada)'
               % new_name)
        except Exception:
            info('FASE1 anterior guardada como %s (no pude apagarla)' % new_name)


# -----------------------------------------------------------------------------
# 2. COMPONENTE Y PARAMETROS (sin Bpm)
# -----------------------------------------------------------------------------

base = mk(ROOT, 'baseCOMP', COMP_NAME, 0, 300)

page = base.appendCustomPage('Fase1')
p = page.appendFloat('Barsperturn', label='Compases por vuelta')
p[0].default = p[0].val = 8.0
p[0].normMin, p[0].normMax = 0.5, 32.0
p = page.appendFloat('Tilt', label='Inclinacion del eje')
p[0].default = p[0].val = 20.0
p[0].normMin, p[0].normMax = 0.0, 90.0
p = page.appendToggle('Showgrid', label='Mostrar reticula')
p[0].default = p[0].val = True
p = page.appendToggle('Pausa', label='Pausar rotacion')
p[0].default = p[0].val = False
ok('pagina Fase1: Barsperturn, Tilt, Showgrid, Pausa (ya no hay Bpm)')

page2 = base.appendCustomPage('Fase2')
p = page2.appendInt('Canal', label='Canal MIDI del SEQ1')
p[0].min, p[0].max = 1, 16
p[0].clampMin = p[0].clampMax = True
p[0].normMin, p[0].normMax = 1, 16
p[0].default = p[0].val = SEQ1_CHANNEL
p = page2.appendToggle('Filtrar', label='Solo ese canal')
p[0].default = p[0].val = True
p = page2.appendInt('Nota', label='Ultima nota (muevela para probar)')
p[0].min, p[0].max = 0, 127
p[0].clampMin = p[0].clampMax = True
p[0].normMin, p[0].normMax = 0, 127
p[0].default = p[0].val = 60
ok('pagina Fase2: Canal (13), Filtrar, Nota')

# La reticula: los polos van entre do1 (24) y do8 (108)
page3 = base.appendCustomPage('Fase3')
p = page3.appendInt('Notapolosur', label='Polo sur: nota MIDI (24 do1 - 106)')
p[0].min, p[0].max = 24, 106
p[0].clampMin = p[0].clampMax = True
p[0].normMin, p[0].normMax = 24, 106
p[0].default = p[0].val = 24
p = page3.appendInt('Notapolonorte', label='Polo norte: nota MIDI (26 - 108 do8)')
p[0].min, p[0].max = 26, 108
p[0].clampMin = p[0].clampMax = True
p[0].normMin, p[0].normMax = 26, 108
p[0].default = p[0].val = 108
p = page3.appendMenu('Fuerarango', label='Notas fuera del rango')
p[0].menuNames = ['plegar', 'ignorar', 'limitar']
p[0].menuLabels = ['Plegar por octavas', 'Ignorar', 'Limitar al polo']
p[0].default = p[0].val = 'plegar'
ok('pagina Fase3: Notapolosur 24 (do1), Notapolonorte 108 (do8), Fuerarango plegar')



# -----------------------------------------------------------------------------
# 3. EL TIEMPO DEL PROYECTO
# -----------------------------------------------------------------------------
# Regla de TouchDesigner: un componente usa su propio local/time si lo tiene;
# si no, el de su padre; y asi hasta el del proyecto, /local/time.

def find_time_comp(comp):
    c = comp
    while c is not None:
        try:
            t = c.op('local/time')
        except Exception:
            t = None
        if t is not None:
            return t
        try:
            c = c.parent()
        except Exception:
            c = None
    return op('/local/time')


time_comp = find_time_comp(base)
TIME_PATH = time_comp.path if time_comp is not None else None
if TIME_PATH:
    ok('el tempo se lee de %s' % TIME_PATH)
else:
    fail('no encontre el componente de tiempo del proyecto')

RITMO = '''# El tiempo de FASE1 lo marca el BeatStep, a traves del tempo del proyecto:
#
#     BeatStep  ->  midicontrolx  ->  tempo del proyecto  ->  aqui
#
# FASE1 solo LEE ese tempo. No escribe tempo ni rebobina nada.
#
# El giro se ACUMULA fotograma a fotograma: si el tempo cambia, el planeta
# acelera o frena suavemente, sin saltar. (Calcular el angulo como
# tiempo x tempo haria saltar el planeta en cada cambio de tempo.)

TIME_PATH = __TIME_PATH__


def time_comp():
    t = op(TIME_PATH) if TIME_PATH else None
    return t if t is not None else op('/local/time')


def tempo():
    try:
        v = float(time_comp().tempo)
        return v if v > 0 else 0.0
    except Exception:
        return 0.0


def beats_per_bar():
    try:
        return max(1, int(time_comp().signature1))
    except Exception:
        return 4


def playing():
    # Si la linea de tiempo del proyecto esta parada, el planeta tambien.
    try:
        return bool(time_comp().play)
    except Exception:
        return True


def seconds_per_turn():
    bpm = tempo()
    if bpm <= 0:
        return 0.0
    try:
        bars = max(0.25, float(parent().par.Barsperturn))
    except Exception:
        bars = 8.0
    return bars * beats_per_bar() * 60.0 / bpm


def giro_factor():
    # Giro vivo (fase 6): el motor frena el planeta cuando el mundo deja de
    # cambiar. Sin motor, o antes de la fase 6, vale 1.
    try:
        m = op('motor')
        return float(m.module.giro_factor()) if m is not None else 1.0
    except Exception:
        return 1.0


def rotation(frame=None):
    # 'frame' solo esta para que la expresion se evalue en cada fotograma.
    # Varias geometrias llaman a esto en el mismo fotograma: se calcula una
    # sola vez y las demas reciben el mismo angulo.
    d = op('ritmo')
    f = absTime.frame
    if d.fetch('frame', None) == f:
        return d.fetch('angle', 0.0)
    now = absTime.seconds
    last = d.fetch('t', now)
    dt = max(0.0, min(0.25, now - last))
    angle = d.fetch('angle', 0.0)
    spt = seconds_per_turn()
    try:
        paused = int(parent().par.Pausa)
    except Exception:
        paused = 0
    if spt > 0 and playing() and not paused:
        angle = (angle + dt * 360.0 / spt * giro_factor()) % 360.0
    d.store('angle', angle)
    d.store('t', now)
    d.store('frame', f)
    return angle


def legend(frame=None):
    try:
        return _legend()
    except Exception as e:
        return '\\n  TEMPO    (fallo en la leyenda: %s)' % e


def _legend():
    bpm = tempo()
    spt = seconds_per_turn()
    try:
        bars = float(parent().par.Barsperturn)
    except Exception:
        bars = 0.0
    angle = rotation()
    lines = ['']
    if bpm > 0:
        lines.append('  TEMPO    %5.1f BPM    (tempo del proyecto)' % bpm)
    else:
        lines.append('  TEMPO    sin tempo: revisa %s' % TIME_PATH)
    lines.append('  VUELTA   %g compases = %.1f s     %3d%%'
                 % (bars, spt, int(angle / 3.6)))
    state = []
    try:
        if int(parent().par.Pausa):
            state.append('PAUSA')
    except Exception:
        pass
    if not playing():
        state.append('linea de tiempo parada')
    if state:
        lines.append('  ESTADO   ' + ', '.join(state))
    return '\\n'.join(lines)
'''

ritmo = mk(base, 'textDAT', 'ritmo', -220, -340)
ritmo.text = RITMO.replace('__TIME_PATH__', repr(TIME_PATH))
ok('ritmo creado: giro acumulado a partir del tempo del proyecto')


# -----------------------------------------------------------------------------
# 4. LA RETICULA DE POLO A POLO
# -----------------------------------------------------------------------------

RETICULA_CB = r'''# Posicion de las celdas sobre la esfera: polos en las notas extremas
# del rango y, en medio, un anillo por octava. (La fase 3 reescribe este DAT para que
# la reticula suba con las conchas; la geometria es la misma.)

import math

CORE_RADIUS = 6.0
NOTE_NAMES = ['do', 'do#', 're', 're#', 'mi', 'fa',
              'fa#', 'sol', 'sol#', 'la', 'la#', 'si']


def note_range():
    try:
        lo = int(parent().par.Notapolosur)
        hi = int(parent().par.Notapolonorte)
    except Exception:
        lo, hi = 24, 108
    lo = max(24, min(106, lo))
    hi = max(lo + 2, min(108, hi))
    return lo, hi


def fold_note(note):
    lo, hi = note_range()
    try:
        mode = str(parent().par.Fuerarango.eval())
    except Exception:
        mode = 'plegar'
    n = int(note)
    if lo <= n <= hi:
        return n
    if mode == 'ignorar':
        return None
    if mode == 'plegar':
        while n > hi:
            n -= 12
        while n < lo:
            n += 12
        if lo <= n <= hi:
            return n
    return lo if int(note) < lo else hi


def ring_layout(lo, hi):
    """Reticula en anillos. lo = polo sur, hi = polo norte (notas MIDI).
    Entre medias, un anillo por octava: la clase de nota es el meridiano.
    Los anillos incompletos (el primero y el ultimo, si el rango no empieza
    o acaba en do) reparten sus celdas por igual alrededor.
    Devuelve (normales, anillo de cada celda, celdas de cada anillo,
    alto de banda en grados, radio del casquete polar en grados)."""
    K = hi - lo
    first = (lo + 1) // 12
    rings = []
    ring_of = [-1] * (K + 1)
    for k in range(1, K):
        j = (lo + k) // 12 - first
        while len(rings) <= j:
            rings.append([])
        rings[j].append(k)
        ring_of[k] = j
    R = max(1, len(rings))
    band = 180.0 / (R + 0.5)
    cap = band * 0.25
    normals = [None] * (K + 1)
    normals[0] = (0.0, -1.0, 0.0)
    normals[K] = (0.0, 1.0, 0.0)
    for j, cells in enumerate(rings):
        phi = math.radians(-90.0 + cap + band * (j + 0.5))
        m = len(cells)
        for q, k in enumerate(cells):
            if m == 12:
                th = 2.0 * math.pi * ((lo + k) % 12) / 12.0
            else:
                th = 2.0 * math.pi * (q + 0.5) / m
            normals[k] = (math.cos(phi) * math.cos(th), math.sin(phi),
                          math.cos(phi) * math.sin(th))
    return normals, ring_of, rings, band, cap


_LAYOUT = {}


def cell_normal(k):
    # k = 0 polo sur ... K polo norte (misma geometria que el motor)
    lo, hi = note_range()
    if _LAYOUT.get('key') != (lo, hi):
        _LAYOUT['key'] = (lo, hi)
        _LAYOUT['data'] = ring_layout(lo, hi)
    normals = _LAYOUT['data'][0]
    return normals[max(0, min(len(normals) - 1, int(k)))]


def cell_label(k):
    lo, hi = note_range()
    if k <= 0:
        return 'polo sur'
    if k >= hi - lo:
        return 'polo norte'
    cell_normal(k)
    return 'anillo %d' % (_LAYOUT['data'][1][int(k)] + 1)


def note_name(note):
    # Convencion latina: el do central (60) es do4.
    return '%s%d' % (NOTE_NAMES[int(note) % 12], int(note) // 12 - 1)

CHANS = ['tx', 'ty', 'tz', 'nx', 'ny', 'nz', 'r', 'g', 'b']


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    try:
        show = int(parent().par.Showgrid)
    except Exception:
        show = 1
    rows = []
    if show:
        lo, hi = note_range()
        K = hi - lo
        d = CORE_RADIUS + 0.06
        for k in range(K + 1):
            nx, ny, nz = cell_normal(k)
            t = k / float(K)
            rows.append([nx * d, ny * d, nz * d, nx, ny, nz,
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

reticula_dat = mk(base, 'textDAT', 'reticula_callbacks', -220, 0)
reticula_dat.text = RETICULA_CB
reticula_chop = mk(base, 'scriptCHOP', 'reticula_chop', 0, 0)
if setp_any(reticula_chop, ['callbacks', 'callbackdat', 'dat'], 'reticula_callbacks'):
    ok('reticula_chop creado (%d celdas de polo a polo)' % (int(base.par.Notapolonorte) - int(base.par.Notapolosur) + 1))
else:
    fail('no encontre el campo de callbacks del Script CHOP: asignalo a mano')


# -----------------------------------------------------------------------------
# 5. GEOMETRIA: los SOP van DENTRO de cada Geometry COMP
# -----------------------------------------------------------------------------

nucleo = mk(base, 'geometryCOMP', 'nucleo', 260, -140)
reticula = mk(base, 'geometryCOMP', 'reticula', 260, 0)


def poblar(geo, optype, sop_name, setup):
    for k in list(geo.children):           # apagar el relleno por defecto
        try:
            k.render = False
            k.display = False
        except Exception:
            pass
    sop = mk(geo, optype, sop_name, 0, 0)
    setup(sop)
    flags_on(sop)
    return sop


def _esfera(s):
    for ax in ('radx', 'rady', 'radz'):
        setp(s, ax, CORE_RADIUS)
    setp_any(s, ['type', 'primtype'], 'polymesh')
    setp_any(s, ['rows'], 48)
    setp_any(s, ['cols'], 48)


def _marcador(s):
    setp(s, 'sizex', 0.30)
    setp(s, 'sizey', 0.10)
    setp(s, 'sizez', 0.30)


poblar(nucleo, 'sphereSOP', 'esfera', _esfera)
poblar(reticula, 'boxSOP', 'marcador', _marcador)

ROT_EXPR = "parent().op('ritmo').module.rotation(absTime.frame)"
for g in (nucleo, reticula):
    setexpr(g, 'ry', ROT_EXPR)
    setexpr(g, 'rz', 'parent().par.Tilt')
ok('nucleo y reticula giran juntos, al tempo del proyecto')

setp(reticula, 'instanceop', 'reticula_chop')
setp_any(reticula, ['instancing', 'instance'], True)
for par_name, chan in [('instancetx', 'tx'), ('instancety', 'ty'), ('instancetz', 'tz'),
                       ('instancerottox', 'nx'), ('instancerottoy', 'ny'),
                       ('instancerottoz', 'nz')]:
    setp(reticula, par_name, chan)
setp_any(reticula, ['instancerotmode', 'instancerotatemode'], 1)


def setmenu(o, names, wanted, index=None):
    for n in names:
        p = getattr(o.par, n, None) if has_par(o, n) else None
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


def set_instance_color(geo):
    # El color por instancia es instancer/g/b (pagina Instance 2). La v2 usaba
    # instancecolorr/g/b, que no existe: la reticula salia blanca.
    good = True
    for ch, names in (('r', ['instancer', 'instancecolorr']),
                      ('g', ['instanceg', 'instancecolorg']),
                      ('b', ['instanceb', 'instancecolorb'])):
        if not setp_any(geo, names, ch):
            good = False
    if not setmenu(geo, ['instancecolormode', 'instcolormode', 'colormode'], ['replace'], None):
        good = False
    return good


if set_instance_color(reticula):
    ok('reticula: cada marca con su color (Instance 2: Color R/G/B = r g b, Replace)')
else:
    info('reticula: no pude enlazar el color por instancia; Instance 2 -> Color R/G/B = '
         'r g b, Color Mode = Replace')


# -----------------------------------------------------------------------------
# 6. MATERIALES, CAMARA, LUCES, RENDER, LEYENDA
# -----------------------------------------------------------------------------

mat_nucleo = mk(base, 'phongMAT', 'mat_nucleo', 0, -420)
setp(mat_nucleo, 'diffuser', 0.34)
setp(mat_nucleo, 'diffuseg', 0.33)
setp(mat_nucleo, 'diffuseb', 0.32)
setp_any(mat_nucleo, ['shininess', 'specularexp'], 18)
setp(nucleo, 'material', 'mat_nucleo')

mat_marca = mk(base, 'constantMAT', 'mat_reticula', 0, -500)
setp(mat_marca, 'colorr', 1.0)
setp(mat_marca, 'colorg', 1.0)
setp(mat_marca, 'colorb', 1.0)
setp(reticula, 'material', 'mat_reticula')

cam = mk(base, 'cameraCOMP', 'camara', 260, -280)
setp(cam, 'tz', CORE_RADIUS + 9.0)
setp(cam, 'ty', 1.5)
setp(cam, 'rx', -5)

luz = mk(base, 'lightCOMP', 'luz_principal', 260, -420)
setp(luz, 'tx', -12)
setp(luz, 'ty', 14)
setp(luz, 'tz', 12)
setp(luz, 'dimmer', 1.2)

relleno = mk(base, 'lightCOMP', 'luz_relleno', 260, -500)
setp(relleno, 'tx', 14)
setp(relleno, 'ty', -5)
setp(relleno, 'tz', -9)
setp(relleno, 'dimmer', 0.30)
setp(relleno, 'lightcolorr', 0.35)
setp(relleno, 'lightcolorg', 0.55)
setp(relleno, 'lightcolorb', 0.80)

render = mk(base, 'renderTOP', 'render', 520, -140)
setp(render, 'camera', 'camara')
# La lista se ESCRIBE entera, nunca se lee y se amplia (ver cabecera).
RENDER_GEO = 'nucleo reticula luz_celda'
setp(render, 'lights', 'luz_principal luz_relleno')
setp(render, 'resolutionw', 1280)      # limite de la licencia no comercial
setp(render, 'resolutionh', 720)

rotulo = mk(base, 'textTOP', 'rotulo', 520, 40)
setp(rotulo, 'resolutionw', 1280)
setp(rotulo, 'resolutionh', 720)
bg = setp_any(rotulo, ['bgalpha', 'backgroundalpha', 'bgcolora'], 0.0)
setp_any(rotulo, ['font', 'fontfamily'], 'Consolas')
setp_any(rotulo, ['fontsizex', 'fontsize'], 15)
setp(rotulo, 'fontsizey', 15)
setp_any(rotulo, ['alignx'], 'left')
setp_any(rotulo, ['aligny'], 'top')
setexpr(rotulo, 'text',
        "parent().op('ritmo').module.legend(absTime.frame) + "
        "parent().op('luz12_callbacks').module.legend(absTime.frame)")

salida = mk(base, 'outTOP', 'salida', 960, -140)
if bg:
    over = mk(base, 'overTOP', 'con_rotulo', 740, -40)
    connect(over, rotulo, 0)
    connect(over, render, 1)
    connect(salida, over, 0)
    ok('salida: imagen con la leyenda encima')
else:
    connect(salida, render, 0)
    info('no pude hacer transparente el fondo del rotulo: la salida muestra el '
         'render directo y la leyenda se ve en el nodo rotulo')
try:
    salida.color = (0.1, 0.8, 0.9)
except Exception:
    pass


# -----------------------------------------------------------------------------
# 7. LA LUZ DE CELDA (sustituye a la baliza)
# -----------------------------------------------------------------------------
# Cada nota del SEQ1 enciende el centro de su celda en cian: un pulso con la
# nota, y tenue hasta la siguiente. Es la misma luz que da el motor desde la
# fase 3, con los mismos nodos (luz_celda, i_luz_celda, mat_luz_celda): la
# fase 3 solo cambia quien calcula las losetas.

LUZ12_CB = r'''# Luz de celda de las fases 1 y 2: el centro de la celda de la ultima nota
# del SEQ1, en cian. La celda se calcula igual que en reticula_callbacks.
# (Desde la fase 3 la calcula el motor y este DAT se retira.)

import math

CORE_RADIUS = 6.0
NOTE_NAMES = ['do', 'do#', 're', 're#', 'mi', 'fa',
              'fa#', 'sol', 'sol#', 'la', 'la#', 'si']


def note_range():
    try:
        lo = int(parent().par.Notapolosur)
        hi = int(parent().par.Notapolonorte)
    except Exception:
        lo, hi = 24, 108
    lo = max(24, min(106, lo))
    hi = max(lo + 2, min(108, hi))
    return lo, hi


def fold_note(note):
    lo, hi = note_range()
    try:
        mode = str(parent().par.Fuerarango.eval())
    except Exception:
        mode = 'plegar'
    n = int(note)
    if lo <= n <= hi:
        return n
    if mode == 'ignorar':
        return None
    if mode == 'plegar':
        while n > hi:
            n -= 12
        while n < lo:
            n += 12
        if lo <= n <= hi:
            return n
    return lo if int(note) < lo else hi


def ring_layout(lo, hi):
    """Reticula en anillos. lo = polo sur, hi = polo norte (notas MIDI).
    Entre medias, un anillo por octava: la clase de nota es el meridiano.
    Los anillos incompletos (el primero y el ultimo, si el rango no empieza
    o acaba en do) reparten sus celdas por igual alrededor.
    Devuelve (normales, anillo de cada celda, celdas de cada anillo,
    alto de banda en grados, radio del casquete polar en grados)."""
    K = hi - lo
    first = (lo + 1) // 12
    rings = []
    ring_of = [-1] * (K + 1)
    for k in range(1, K):
        j = (lo + k) // 12 - first
        while len(rings) <= j:
            rings.append([])
        rings[j].append(k)
        ring_of[k] = j
    R = max(1, len(rings))
    band = 180.0 / (R + 0.5)
    cap = band * 0.25
    normals = [None] * (K + 1)
    normals[0] = (0.0, -1.0, 0.0)
    normals[K] = (0.0, 1.0, 0.0)
    for j, cells in enumerate(rings):
        phi = math.radians(-90.0 + cap + band * (j + 0.5))
        m = len(cells)
        for q, k in enumerate(cells):
            if m == 12:
                th = 2.0 * math.pi * ((lo + k) % 12) / 12.0
            else:
                th = 2.0 * math.pi * (q + 0.5) / m
            normals[k] = (math.cos(phi) * math.cos(th), math.sin(phi),
                          math.cos(phi) * math.sin(th))
    return normals, ring_of, rings, band, cap


_LAYOUT = {}


def cell_normal(k):
    # k = 0 polo sur ... K polo norte (misma geometria que el motor)
    lo, hi = note_range()
    if _LAYOUT.get('key') != (lo, hi):
        _LAYOUT['key'] = (lo, hi)
        _LAYOUT['data'] = ring_layout(lo, hi)
    normals = _LAYOUT['data'][0]
    return normals[max(0, min(len(normals) - 1, int(k)))]


def cell_label(k):
    lo, hi = note_range()
    if k <= 0:
        return 'polo sur'
    if k >= hi - lo:
        return 'polo norte'
    cell_normal(k)
    return 'anillo %d' % (_LAYOUT['data'][1][int(k)] + 1)


def note_name(note):
    # Convencion latina: el do central (60) es do4.
    return '%s%d' % (NOTE_NAMES[int(note) % 12], int(note) // 12 - 1)

SEQ_DECAY = 0.25      # el pulso de la nota cae en 1/4 de segundo
COL_SEQ1 = (0.10, 0.90, 1.00)
LIFT = 0.02
CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']


def current_note():
    try:
        return int(parent().par.Nota)
    except Exception:
        return 60


def orient(n):
    x, y, z = n
    y = max(-1.0, min(1.0, y))
    return 90.0 - math.degrees(math.asin(y)), 90.0 - math.degrees(math.atan2(z, x))


def cell_size(k):
    """(ancho este-oeste, largo norte-sur) de la celda k sobre el nucleo."""
    lo, hi = note_range()
    cell_normal(k)
    normals, ring_of, rings, band, cap = _LAYOUT['data']
    if k <= 0 or k >= hi - lo:
        d = 2.0 * CORE_RADIUS * math.radians(cap) * 1.25
        return d, d
    j = ring_of[int(k)]
    phi = math.radians(-90.0 + cap + band * (j + 0.5))
    ns = CORE_RADIUS * math.radians(band)
    ew = CORE_RADIUS * math.cos(phi) * 2.0 * math.pi / max(1, len(rings[j]))
    return ew, ns


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
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
    env = math.exp(-max(0.0, now - t0) / SEQ_DECAY)
    scriptOp.store('env', env)
    f = fold_note(note)
    if f is None:
        row = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]
    else:
        lo, _ = note_range()
        k = f - lo
        n = cell_normal(k)
        cw, cl = cell_size(k)
        g = 0.75 + 0.25 * env                      # crece en el pulso
        b = 0.6 + 0.4 * env                        # tenue en reposo
        rx, ry = orient(n)
        d = CORE_RADIUS + LIFT
        row = [n[0] * d, n[1] * d, n[2] * d, rx, ry, 0.0,
               0.26 * cw * g, 0.05 + 0.08 * env, 0.26 * cl * g,
               COL_SEQ1[0] * b, COL_SEQ1[1] * b, COL_SEQ1[2] * b]
    scriptOp.numSamples = 1
    for name, v in zip(CHANS, row):
        scriptOp.appendChan(name)[0] = float(v)
    return


def legend(frame=None):
    try:
        c = op('i_luz_celda')
        note = current_note()
        env = c.fetch('env', 0.0) if c is not None else 0.0
        lo, hi = note_range()
        f = fold_note(note)
        if f is None:
            donde = 'fuera de rango (ignorada)'
        else:
            k = f - lo
            donde = 'celda %2d de %d   %s' % (k, hi - lo + 1, cell_label(k))
            if f != note:
                donde += '   (como %s %d)' % (note_name(f), f)
        n = int(round(max(0.0, min(1.0, env)) * 12))
        try:
            ch = int(parent().par.Canal)
        except Exception:
            ch = 13
        hits = c.fetch('hits', 0) if c is not None else 0
        lines = ['',
                 '  NOTA     %-5s %3d    %s' % (note_name(note), note, donde),
                 '  PULSO    [%s]' % ('#' * n + '.' * (12 - n)),
                 '  SEQ1     canal %d    notas recibidas: %d' % (ch, hits)]
        return '\n'.join(lines)
    except Exception as e:
        return '\n  NOTA     (fallo en la leyenda: %s)' % e
'''

for viejo in ('baliza', 'baliza_chop', 'baliza_callbacks', 'mat_baliza'):
    o = base.op(viejo)
    if o is not None:
        try:
            o.destroy()
        except Exception:
            pass

luz_cb = fresh(base, 'textDAT', 'luz12_callbacks', -220, 200)
luz_cb.text = LUZ12_CB
luz_chop = fresh(base, 'scriptCHOP', 'i_luz_celda', 0, 200)
if setp_any(luz_chop, ['callbacks', 'callbackdat', 'dat'], 'luz12_callbacks'):
    ok('i_luz_celda creado')
else:
    fail('no encontre el campo de callbacks del Script CHOP: asignalo a mano')

# El pulso tiene que animarse aunque no lleguen notas: se recalcula cada
# fotograma.
latido = fresh(base, 'executeDAT', 'latido', -220, 320)
latido.text = '''def onFrameStart(frame):
    c = parent().op('i_luz_celda')
    if c is not None:
        c.cook(force=True)
    return
'''
setp(latido, 'active', True)
if setp_any(latido, ['framestart', 'onframestart'], True):
    ok('latido: la luz de celda se recalcula en cada fotograma')
else:
    fail('latido: activa a mano "Frame Start" en el nodo latido')

# Geometria: una caja de 1x1x1 con la base en y = 0, instanciada con
# posicion, giro, escala y color (igual que hara make_instanced en la fase 3)
luz_geo = fresh(base, 'geometryCOMP', 'luz_celda', 260, 200)
for k in list(luz_geo.children):
    try:
        k.render = False
        k.display = False
    except Exception:
        pass
caja = mk(luz_geo, 'boxSOP', 'bloque', 0, 0)
for ax in ('sizex', 'sizey', 'sizez'):
    setp(caja, ax, 1.0)
setp(caja, 'ty', 0.5)
flags_on(caja)
setp(luz_geo, 'instanceop', 'i_luz_celda')
setp_any(luz_geo, ['instancing', 'instance'], True)
for par_name, ch in [('instancetx', 'tx'), ('instancety', 'ty'), ('instancetz', 'tz'),
                     ('instancerx', 'rx'), ('instancery', 'ry'), ('instancerz', 'rz'),
                     ('instancesx', 'sx'), ('instancesy', 'sy'), ('instancesz', 'sz')]:
    setp(luz_geo, par_name, ch)
setmenu(luz_geo, ['instancerord'], ['xyz'], 0)
color_ok = set_instance_color(luz_geo)
setexpr(luz_geo, 'ry', "parent().op('ritmo').module.rotation(absTime.frame)")
setexpr(luz_geo, 'rz', 'parent().par.Tilt')
mat = fresh(base, 'constantMAT', 'mat_luz_celda', 260, 320)
setp(mat, 'colorr', 1.0)
setp(mat, 'colorg', 1.0)
setp(mat, 'colorb', 1.0)
setp(luz_geo, 'material', 'mat_luz_celda')

# La lista se ESCRIBE entera, no se lee y se amplia: este parametro
# referencia operadores, y leerlo con .eval() devuelve un operador, no el
# texto. Escribir eso de vuelta corrompe la lista y el render pierde el
# nucleo y la reticula.
if setp(render, 'geometry', RENDER_GEO):
    ok('render dibuja: %s' % RENDER_GEO)
else:
    fail('no pude fijar la geometria del render: pon a mano "%s"' % RENDER_GEO)
if color_ok:
    ok('luz_celda: el centro de la celda de cada nota en cian, gira con el planeta')
else:
    info('luz_celda: no pude enlazar el color por instancia; Instance 2 -> Color '
         'R/G/B = r g b, Color Mode = Replace')


# -----------------------------------------------------------------------------
# 8. ENTRADA MIDI
# -----------------------------------------------------------------------------

midi_log = fresh(base, 'tableDAT', 'midi_log', -440, 200)
midi_log.clear()
midi_log.appendRow(['frame', 'canal', 'nota', 'vel', 'resultado'])

MIDI_CB = '''# Notas del SEQ1 -> luz de celda.
#
# Nota y canal se leen de los BYTES del mensaje: 9n kk vv = note on en el
# canal n+1, nota kk, velocidad vv. Asi no importa como numere
# TouchDesigner los indices. Todo lo que no sea un note on se ignora.

LOG_MAX = 40
PRINT_FIRST = 8


def _num(x, default=None):
    try:
        return int(float(x))
    except Exception:
        return default


def _raw(values):
    for a in reversed(values):
        if isinstance(a, (bytes, bytearray)):
            return bytes(a)
    return None


def parse_note_on(args, kwargs):
    values = list(args) + list(kwargs.values())
    b = _raw(values)
    if b is not None:
        if len(b) >= 3 and 0x90 <= b[0] <= 0x9F:
            return (b[0] & 0x0F) + 1, b[1], b[2]
        return None
    # Sin bytes: por los campos con nombre (menos fiable, ver arriba)
    msg = str(kwargs.get('message', args[2] if len(args) > 2 else '')).lower()
    if 'note' in msg and 'on' in msg and 'off' not in msg:
        return (_num(kwargs.get('channel', args[3] if len(args) > 3 else None)),
                _num(kwargs.get('index', args[4] if len(args) > 4 else None)),
                _num(kwargs.get('value', args[5] if len(args) > 5 else None)))
    return None


def trigger(note):
    try:
        parent().par.Nota = int(note)
    except Exception:
        pass
    c = op('i_luz_celda')
    if c is not None:
        c.store('hit_t', absTime.seconds)
        c.store('hits', c.fetch('hits', 0) + 1)


def _log(row):
    t = op('midi_log')
    if t is None:
        return
    t.appendRow([str(v) for v in row])
    while t.numRows > LOG_MAX + 1:
        t.deleteRow(1)


def handle(ch, note, vel):
    if note is None or vel is None or vel <= 0:
        return None                               # velocidad 0 = note off
    try:
        filt = int(parent().par.Filtrar)
        want = int(parent().par.Canal)
    except Exception:
        filt, want = 1, 13
    if filt and ch is not None and ch != want:
        result = 'ignorado: canal %s (SEQ1 en %s)' % (ch, want)
    else:
        trigger(note)
        result = 'DISPARO'
    _log([absTime.frame, ch, note, vel, result])
    c = op('i_luz_celda')
    n = c.fetch('printed', 0) if c is not None else 99
    if n < PRINT_FIRST:
        print('MIDI  canal %s  nota %s  vel %s  ->  %s' % (ch, note, vel, result))
        c.store('printed', n + 1)
    return result


def onReceiveMIDI(*args, **kwargs):
    r = parse_note_on(args, kwargs)
    if r is not None:
        handle(*r)
    return
'''

midi_cb = fresh(base, 'textDAT', 'midi_callbacks', -440, 80)
midi_cb.text = MIDI_CB
midi_in = fresh(base, 'midiinDAT', 'midi_in', -220, 80)
setp(midi_in, 'active', True)
if setp_any(midi_in, ['callbacks', 'callbackdat'], 'midi_callbacks'):
    ok('midi_in creado, sus callbacks en midi_callbacks')
else:
    fail('no encontre el campo de callbacks del MIDI In DAT')


# Dispositivo: el mismo que ya usa midicontrolx (o la FASE1 anterior)
def find_device():
    sources = []
    try:
        for t in op('/').findChildren(name='midicontrolx*', depth=None):
            sources += [o for o in t.findChildren(depth=None)
                        if str(o.OPType).lower().startswith('midiin')]
    except Exception:
        pass
    for nm in ('FASE1_anterior', 'FASE1_anterior_2'):
        o = op('/project1/%s/midi_in' % nm)
        if o is not None:
            sources.append(o)
    for o in sources:
        for pname in ('id', 'device'):
            p = getattr(o.par, pname, None) if has_par(o, pname) else None
            if p is not None:
                try:
                    return pname, p.eval(), o.path
                except Exception:
                    pass
    return None, None, None


pname, dev, src = find_device()
if pname and setp(midi_in, pname, dev):
    ok('dispositivo MIDI copiado de %s (%s = %s)' % (src, pname, dev))
else:
    info('no encontre otro MIDI In del que copiar el dispositivo: pon a mano '
         'en midi_in el Device ID que tenga el BeatStep en el MIDI Device Mapper')



# -----------------------------------------------------------------------------
# 9. NOTA DENTRO DEL PROYECTO
# -----------------------------------------------------------------------------

nota = mk(base, 'textDAT', 'LEEME', -220, -200)
nota.text = """FASE 1+2 - LA BASE

EL TIEMPO
  BeatStep -> midicontrolx -> tempo del proyecto -> FASE1
  FASE1 lee el tempo del proyecto (nodo 'ritmo'). No tiene parametro Bpm.

LA RETICULA (pagina Fase3)
  Notapolosur / Notapolonorte  notas MIDI de los polos, entre 24 (do1) y 108 (do8)
  Fuerarango                   plegar por octavas, ignorar o limitar al polo
  Cada semitono del rango es una celda; en medio, un anillo por octava.

PARAMETROS (pagina Fase1)
  Barsperturn, Tilt, Showgrid, Pausa

EL SEQ1 (pagina Fase2)
  Canal (13), Filtrar, Nota (muevela para probar sin BeatStep)

Mas detalle en MONTAJE_FASE1.md y MONTAJE_FASES_3_10.md.
"""


# -----------------------------------------------------------------------------
# 10. INFORME, DIAGNOSTICO DEL RENDER Y AUTOPRUEBA
# -----------------------------------------------------------------------------

print('CAMBIOS')
print('-' * 66)
for line in report:
    print(line)
print()


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


def diagnostico_render():
    print('DIAGNOSTICO DEL RENDER')
    print('-' * 66)
    r = base.op('render')
    try:
        print('  render geometria : %r' % r.par.geometry.val)
        print('  render camara    : %r   luces: %r' % (r.par.camera.val, r.par.lights.val))
    except Exception as e:
        print('  FALLO  no pude leer el render: %s' % e)
    for nm in RENDER_GEO.split():
        g = base.op(nm)
        if g is None:
            print('  FALLO  %-9s no existe' % nm)
            continue
        vivos = [k.name for k in g.children if getattr(k, 'render', False)]
        e = _errs(g)
        print('  %-6s %-9s renderiza: %s%s' % ('OK' if vivos and not e else 'FALLO', nm,
              vivos if vivos else 'NADA', ('   ERROR: ' + e) if e else ''))
    malos = []
    for nm in ('ritmo', 'reticula_chop', 'i_luz_celda', 'camara', 'render',
               'rotulo', 'con_rotulo', 'salida'):
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
    if malos:
        for nm, e in malos:
            print('  FALLO  %-13s %s' % (nm, e))
    else:
        print('  OK     ningun nodo de la cadena hasta salida tiene errores')
    print('-' * 66)


diagnostico_render()

print('AUTOPRUEBA (sin BeatStep)')
print('-' * 66)
passed = False
try:
    reticula_chop.cook(force=True)
    n_cel = reticula_chop.numSamples
    K = int(base.par.Notapolonorte) - int(base.par.Notapolosur)
    print('  reticula                : %d celdas (deben ser %d)' % (n_cel, K + 1))
    rm = reticula_dat.module
    sur = rm.cell_normal(0)[1] < -0.999 and rm.cell_normal(K)[1] > 0.999
    print('  polos                   : %s' % ('do1 abajo, do8 arriba' if sur else 'MAL'))
    mm = midi_cb.module
    before = int(base.par.Nota)
    luz_chop.store('printed', 99)
    mm.onReceiveMIDI(None, 0, 'Note On', 13, 65, 100, True, bytes([0x9C, 0x40, 0x64]))
    luz_chop.cook(force=True)
    note = int(base.par.Nota)
    env = float(luz_chop.fetch('env', 0.0))
    col = [float(luz_chop[ch][0]) for ch in ('r', 'g', 'b')]
    cian = abs(col[1] / max(1e-6, col[2]) - 0.9) < 0.05 and col[0] < 0.2
    ign = mm.handle(1, 60, 100)
    print('  nota leida de los bytes : %d  (debe ser 64, aunque el campo decia 65)' % note)
    print('  pulso                   : %.2f  (debe estar cerca de 1)' % env)
    print('  luz de celda            : %s' % ('cian en el centro de la celda' if cian else 'MAL %s' % col))
    print('  nota en el canal 1      : %s' % ign)
    sin_baliza = all(base.op(nm) is None for nm in ('baliza', 'baliza_chop', 'baliza_callbacks'))
    print('  sin baliza              : %s' % ('si' if sin_baliza else 'NO'))
    for l in luz_cb.module.legend().split('\n'):
        if l.strip():
            print('   ' + l)
    passed = (n_cel == K + 1 and sur and note == 64 and env > 0.8 and cian and sin_baliza
              and str(ign).startswith('ignorado'))
    base.par.Nota = before
    luz_chop.store('hits', 0)
    luz_chop.store('printed', 0)
    midi_log.clear()
    midi_log.appendRow(['frame', 'canal', 'nota', 'vel', 'resultado'])
except Exception as e:
    print('  FALLO en la autoprueba: %s' % e)

try:
    m = ritmo.module
    bpm = m.tempo()
    if bpm > 0:
        print('  tempo del proyecto      : %.1f BPM  (%s)' % (bpm, TIME_PATH))
    else:
        print('  FALLO  el tempo del proyecto es 0 o no se puede leer (%s)' % TIME_PATH)
    if not m.playing():
        print('  AVISO  la linea de tiempo esta PARADA: el planeta no gira y, desde')
        print('         la fase 3, las formaciones no brotan hasta darle a play')
except Exception as e:
    print('  FALLO  al leer el tempo: %s' % e)

print('-' * 66)
print('  AUTOPRUEBA %s' % ('OK' if passed else 'FALLIDA: pegame este bloque'))
print('-' * 66)
print('  Viewer Active sobre "salida": nucleo, reticula y la luz cian en la celda de la nota.')
print('  Ahora: PLAY en la linea de tiempo y en el BeatStep con el SEQ1.')
print('  Si las notas no salen aqui: el Device ID de midi_in no es el del BeatStep.')
print('  Siguiente: fase3_semilla.py')
print('=' * 66)
