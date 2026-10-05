"""
=============================================================================
ESTRATOS - FASE 1: EL NUCLEO QUE GIRA AL TEMPO DEL BEATSTEP
=============================================================================
Lee primero MONTAJE_FASE1.md: explica el montaje entero.

QUE CONSTRUYE
-------------
Un nucleo esferico con su reticula de 96 celdas, girando. La velocidad de
giro sale del TEMPO DEL PROYECTO, que marca el BeatStep:

    BeatStep  ->  midicontrolx  ->  tempo del proyecto  ->  FASE1

FASE1 no tiene parametro Bpm: lee el tempo del proyecto y no escribe nada
de tiempo.

COMO USARLO
-----------
    exec(open('C:/ruta/a/fase1_tempo_beatstep.py').read())

Viewer Active sobre el nodo 'salida'.

SI YA EXISTE /project1/FASE1
----------------------------
No se borra: se renombra a FASE1_anterior. Si dentro no hay midicontrolx
ni master_beat, ademas se apaga para que no de errores. Si los hay, se
deja funcionando y se avisa.
=============================================================================
"""

import td

VERSION = 'fase1 v2  (gira al tempo del proyecto; sin parametro Bpm)'
print('=' * 66)
print('EJECUTANDO: ' + VERSION)
print('=' * 66)

ROOT = op('/project1')
COMP_NAME = 'FASE1'
CORE_RADIUS = 6.0


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
ok('parametros: Barsperturn, Tilt, Showgrid, Pausa (ya no hay Bpm)')


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
        angle = (angle + dt * 360.0 / spt) % 360.0
    d.store('angle', angle)
    d.store('t', now)
    d.store('frame', f)
    return angle


def legend(frame=None):
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
# 4. LA RETICULA: 96 celdas, 12 meridianos x 8 bandas
# -----------------------------------------------------------------------------

RETICULA_CB = '''# Posicion de las 96 celdas sobre la esfera.
# La clase de nota (do, do#, re...) elige el meridiano; la octava, la banda.

import math

GRID_COLS = 12
GRID_ROWS = 8
CORE_RADIUS = 6.0
CHANS = ['tx', 'ty', 'tz', 'nx', 'ny', 'nz', 'r', 'g', 'b']


def cell_angles(col, row):
    theta = (col / float(GRID_COLS)) * 2.0 * math.pi
    # el 0.86 evita los polos exactos, donde las celdas degeneran
    phi = ((row + 0.5) / float(GRID_ROWS) - 0.5) * math.pi * 0.86
    return theta, phi


def cell_normal(col, row):
    theta, phi = cell_angles(col, row)
    return (math.cos(phi) * math.cos(theta),
            math.sin(phi),
            math.cos(phi) * math.sin(theta))


def note_to_cell(note):
    return int(note) % GRID_COLS, (int(note) // GRID_COLS) % GRID_ROWS


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
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                nx, ny, nz = cell_normal(c, r)
                d = CORE_RADIUS + 0.06
                t = r / float(GRID_ROWS - 1)
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
    ok('reticula_chop creado')
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
                       ('instancerottoz', 'nz'), ('instancecolorr', 'r'),
                       ('instancecolorg', 'g'), ('instancecolorb', 'b')]:
    setp(reticula, par_name, chan)
setp_any(reticula, ['instancerotmode', 'instancerotatemode'], 1)
setp_any(reticula, ['instancecolormode', 'instcolormode'], 1)


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
setp(render, 'geometry', 'nucleo reticula')
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
setexpr(rotulo, 'text', "parent().op('ritmo').module.legend(absTime.frame)")

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
# 7. NOTA DENTRO DEL PROYECTO
# -----------------------------------------------------------------------------

nota = mk(base, 'textDAT', 'LEEME', -220, -200)
nota.text = """FASE 1 - EL NUCLEO QUE GIRA AL TEMPO DEL BEATSTEP

EL TIEMPO
  BeatStep -> midicontrolx -> tempo del proyecto -> FASE1
  FASE1 lee el tempo del proyecto (nodo 'ritmo'). No tiene parametro Bpm.
  midicontrolx debe escribir el tempo del BeatStep en el componente de
  tiempo del proyecto, por ejemplo:   op('/local/time').tempo = bpm

PARAMETROS (pagina Fase1)
  Barsperturn  compases por vuelta
  Tilt         inclinacion del eje
  Showgrid     mostrar la reticula (sin ella la esfera parece quieta)
  Pausa        congela el giro donde esta

COMPROBAR
  Gira la perilla TEMPO del BeatStep: la linea TEMPO de la leyenda debe
  seguirla y el planeta acelerar o frenar SIN SALTAR.

Mas detalle en MONTAJE_FASE1.md.
"""


# -----------------------------------------------------------------------------
# 8. COMPROBACIONES
# -----------------------------------------------------------------------------

print('CAMBIOS')
print('-' * 66)
for line in report:
    print(line)
print()
print('COMPROBACIONES')
print('-' * 66)

try:
    reticula_chop.cook(force=True)
    missing = [c for c in ('tx', 'ny', 'r') if reticula_chop[c] is None]
    if missing:
        print('  FALLO  faltan channels en reticula_chop: %s' % missing)
    else:
        print('  OK     reticula_chop: %d celdas' % reticula_chop.numSamples)
except Exception as e:
    print('  FALLO  al calcular la reticula: %s' % e)

for g in (nucleo, reticula):
    vivos = [k.name for k in g.children if getattr(k, 'render', False)]
    print('  %-6s %-9s renderiza: %s'
          % ('OK' if vivos else 'FALLO', g.name, vivos if vivos else 'NADA'))

try:
    m = ritmo.module
    bpm = m.tempo()
    spt = m.seconds_per_turn()
    if bpm > 0:
        print('  OK     tempo del proyecto: %.1f BPM  (%s)' % (bpm, TIME_PATH))
        print('  OK     una vuelta = %g compases de %d tiempos = %.1f s'
              % (float(base.par.Barsperturn), m.beats_per_bar(), spt))
    else:
        print('  FALLO  el tempo del proyecto es 0 o no se puede leer (%s)' % TIME_PATH)
    if not m.playing():
        print('  AVISO  la linea de tiempo del proyecto esta PARADA: el planeta')
        print('         no girara hasta que se ponga en marcha')
except Exception as e:
    print('  FALLO  al leer el tempo: %s' % e)

print('-' * 66)
print('  Viewer Active sobre "salida".')
print('  Prueba: gira la perilla TEMPO del BeatStep. Si la linea TEMPO no')
print('  cambia, midicontrolx no esta escribiendo en el tempo del proyecto')
print('  (%s). Mira MONTAJE_FASE1.md, apartado "midicontrolx".' % TIME_PATH)
print('=' * 66)
