"""
=============================================================================
ESTRATOS - FASE 2: EL SEQ1 MARCA SUS NOTAS SOBRE LA RETICULA
=============================================================================
Se apoya en la FASE 1 construida con fase1_tempo_beatstep.py. No la
rehace: le anade piezas.

QUE HACE
--------
Cada nota que toca el SEQ1 del BeatStep (canal MIDI 13):
  - lleva la BALIZA a la celda de esa nota (meridiano = clase de nota,
    banda = octava, igual que la reticula)
  - la hace PULSAR: crece de golpe y se va apagando. Pulsa en CADA nota,
    tambien si se repite la misma: un pattern que repite nota se ve como
    golpes, no como una luz fija.
  - la escribe en la leyenda: nota, meridiano y banda. Aunque la baliza
    quede detras del planeta, ves que la nota cambia.

LA BALIZA
---------
Una ESFERA cian grande: da igual hacia donde la oriente TouchDesigner.
Con su PROPIO material cian fijo: no depende del color por instancia.
Su tamano lo controla el propio SOP, no la escala por instancia.
Gira con el planeta (el mismo angulo que nucleo y reticula).

LA NOTA SE LEE DE LOS BYTES
---------------------------
TouchDesigner numera los controladores desde 1 (el CC 51 aparece como 52).
Si hiciera lo mismo con las notas, cada baliza caeria un semitono
desplazada. Por eso nota y canal se sacan de los bytes del mensaje:
9C 40 64 = nota 64 en el canal 13, sin interpretacion posible.

COMO USARLO
-----------
    exec(open('C:/ruta/a/fase2_seq1_baliza.py').read())

Despues, PLAY en el BeatStep con el SEQ1 sonando. Las primeras notas
salen en el Textport con su resultado.
=============================================================================
"""

import td

VERSION = 'fase2 v3  (SEQ1 canal 13 -> baliza; render corregido)'
print('=' * 66)
print('EJECUTANDO: ' + VERSION)
print('=' * 66)

COMP_PATH = '/project1/FASE1'
SEQ1_CHANNEL = 13

base = op(COMP_PATH)
if base is None:
    raise RuntimeError('No encuentro %s. Construye antes la fase 1 '
                       '(fase1_tempo_beatstep.py).' % COMP_PATH)
for n in ['ritmo', 'nucleo', 'reticula', 'render', 'rotulo']:
    if base.op(n) is None:
        raise RuntimeError('Falta %s en FASE1. Construyela con '
                           'fase1_tempo_beatstep.py.' % n)


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


def fresh(parent_comp, optype, name, x, y):
    """Crea el nodo; si ya existia lo borra antes (relanzar es seguro)."""
    old = parent_comp.op(name)
    if old is not None:
        try:
            old.destroy()
        except Exception:
            pass
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


report = []
def ok(m):   report.append('  OK    ' + m)
def fail(m): report.append('  FALLO ' + m)
def info(m): report.append('  ..    ' + m)


# -----------------------------------------------------------------------------
# 1. PARAMETROS (pagina Fase2)
# -----------------------------------------------------------------------------

page = None
for pg in base.customPages:
    if pg.name == 'Fase2':
        page = pg
if page is None:
    page = base.appendCustomPage('Fase2')

if not has_par(base, 'Canal'):
    p = page.appendInt('Canal', label='Canal MIDI del SEQ1')
    p[0].min, p[0].max = 1, 16
    p[0].clampMin = p[0].clampMax = True
    p[0].normMin, p[0].normMax = 1, 16
    p[0].default = p[0].val = SEQ1_CHANNEL
if not has_par(base, 'Filtrar'):
    p = page.appendToggle('Filtrar', label='Solo ese canal')
    p[0].default = p[0].val = True
if not has_par(base, 'Nota'):
    p = page.appendInt('Nota', label='Ultima nota (muevela para probar)')
    p[0].min, p[0].max = 0, 127
    p[0].clampMin = p[0].clampMax = True
    p[0].normMin, p[0].normMax = 0, 127
    p[0].default = p[0].val = 60
ok('pagina Fase2: Canal (13), Filtrar, Nota')


# -----------------------------------------------------------------------------
# 2. LA BALIZA: logica
# -----------------------------------------------------------------------------

BALIZA_CB = '''# Baliza: lleva la esfera cian a la celda de la nota y la hace pulsar.
#
# La celda se calcula EXACTAMENTE igual que en reticula_callbacks:
#   meridiano = clase de nota (do, do#, re...), banda = octava.

import math

GRID_COLS = 12
GRID_ROWS = 8
CORE_RADIUS = 6.0

DECAY = 0.12          # segundos hasta caer a un tercio. Corto a proposito:
                      # entre dos semicorcheas a 120 BPM (125 ms) cae al 35 %,
                      # y cada nota se ve como un golpe separado
BASE_RADIUS = 0.90    # tamano en reposo: visible aunque este en el borde
PEAK_RADIUS = 1.80    # cuanto crece en el golpe
LIFT = 0.30           # separacion de la superficie

NOTE_NAMES = ['do', 'do#', 're', 're#', 'mi', 'fa',
              'fa#', 'sol', 'sol#', 'la', 'la#', 'si']


def cell_angles(col, row):
    theta = (col / float(GRID_COLS)) * 2.0 * math.pi
    phi = ((row + 0.5) / float(GRID_ROWS) - 0.5) * math.pi * 0.86
    return theta, phi


def cell_normal(col, row):
    theta, phi = cell_angles(col, row)
    return (math.cos(phi) * math.cos(theta),
            math.sin(phi),
            math.cos(phi) * math.sin(theta))


def note_to_cell(note):
    return int(note) % GRID_COLS, (int(note) // GRID_COLS) % GRID_ROWS


def note_name(note):
    # Convencion latina: el do central (60) es do4.
    return '%s%d' % (NOTE_NAMES[int(note) % 12], int(note) // 12 - 1)


def current_note():
    try:
        return int(parent().par.Nota)
    except Exception:
        return 60


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    scriptOp.clear()
    now = absTime.seconds
    note = current_note()

    # Golpe 1: la nota ha cambiado (MIDI, o el parametro Nota movido a mano)
    trig = False
    last = scriptOp.fetch('last_note', None)
    if last is None or int(last) != note:
        scriptOp.store('last_note', note)
        trig = True
    # Golpe 2: ha llegado una nota del SEQ1, aunque sea la misma de antes
    hit_t = scriptOp.fetch('hit_t', -1.0)
    if hit_t > scriptOp.fetch('hit_seen', -1.0):
        scriptOp.store('hit_seen', hit_t)
        trig = True
    if trig:
        scriptOp.store('t0', now)
    t0 = scriptOp.fetch('t0', now - 10.0)

    env = math.exp(-max(0.0, now - t0) / DECAY)
    radius = BASE_RADIUS + PEAK_RADIUS * env
    c, r = note_to_cell(note)
    nx, ny, nz = cell_normal(c, r)
    d = CORE_RADIUS + LIFT + radius

    scriptOp.numSamples = 1
    for name, v in [('tx', nx * d), ('ty', ny * d), ('tz', nz * d),
                    ('env', env), ('radius', radius), ('note', note)]:
        scriptOp.appendChan(name)[0] = float(v)
    return


def legend(frame=None):
    # Apartado de la leyenda: se anade debajo del de ritmo.
    b = op('baliza_chop')
    try:
        note = int(b['note'][0])
        env = float(b['env'][0])
    except Exception:
        note, env = current_note(), 0.0
    c, r = note_to_cell(note)
    n = int(round(max(0.0, min(1.0, env)) * 12))
    try:
        ch = int(parent().par.Canal)
    except Exception:
        ch = 13
    hits = b.fetch('hits', 0) if b is not None else 0
    lines = [
        '',
        '  NOTA     %-5s %3d    meridiano %2d    banda %d' % (note_name(note), note, c, r),
        '  PULSO    [%s]' % ('#' * n + '.' * (12 - n)),
        '  SEQ1     canal %d    notas recibidas: %d' % (ch, hits),
    ]
    return '\\n'.join(lines)
'''

baliza_cb = fresh(base, 'textDAT', 'baliza_callbacks', -220, 200)
baliza_cb.text = BALIZA_CB
baliza_chop = fresh(base, 'scriptCHOP', 'baliza_chop', 0, 200)
if setp_any(baliza_chop, ['callbacks', 'callbackdat', 'dat'], 'baliza_callbacks'):
    ok('baliza_chop creado')
else:
    fail('no encontre el campo de callbacks del Script CHOP: asignalo a mano')

# El pulso tiene que animarse aunque no lleguen notas: se recalcula cada
# fotograma.
latido = fresh(base, 'executeDAT', 'latido', -220, 320)
latido.text = '''def onFrameStart(frame):
    c = parent().op('baliza_chop')
    if c is not None:
        c.cook(force=True)
    return
'''
setp(latido, 'active', True)
if setp_any(latido, ['framestart', 'onframestart'], True):
    ok('latido: la baliza se recalcula en cada fotograma')
else:
    fail('latido: activa a mano "Frame Start" en el nodo latido')


# -----------------------------------------------------------------------------
# 3. LA BALIZA: geometria (el SOP va DENTRO del Geometry COMP)
# -----------------------------------------------------------------------------

baliza = fresh(base, 'geometryCOMP', 'baliza', 260, 200)
for k in list(baliza.children):          # apagar el relleno por defecto
    try:
        k.render = False
        k.display = False
    except Exception:
        pass
esfera = mk(baliza, 'sphereSOP', 'esfera_baliza', 0, 0)
R_EXPR = "parent(2).op('baliza_chop')['radius'][0]"   # el valor, no el canal
for ax in ('radx', 'rady', 'radz'):
    setexpr(esfera, ax, R_EXPR)
setp_any(esfera, ['type', 'primtype'], 'polymesh')
setp_any(esfera, ['rows'], 24)
setp_any(esfera, ['cols'], 24)
for attr in ('render', 'display'):
    try:
        setattr(esfera, attr, True)
    except Exception:
        pass

# Posicion por instanciado (una instancia). Solo traslacion.
setp(baliza, 'instanceop', 'baliza_chop')
setp_any(baliza, ['instancing', 'instance'], True)
setp(baliza, 'instancetx', 'tx')
setp(baliza, 'instancety', 'ty')
setp(baliza, 'instancetz', 'tz')

# Gira con el planeta: el mismo angulo que nucleo y reticula
setexpr(baliza, 'ry', "parent().op('ritmo').module.rotation(absTime.frame)")
setexpr(baliza, 'rz', 'parent().par.Tilt')

mat = fresh(base, 'constantMAT', 'mat_baliza', 260, 320)
setp(mat, 'colorr', 0.10)
setp(mat, 'colorg', 0.90)
setp(mat, 'colorb', 1.00)
setp(baliza, 'material', 'mat_baliza')

# La lista se ESCRIBE entera, no se lee y se amplia: este parametro
# referencia operadores, y leerlo con .eval() devuelve un operador, no el
# texto. Escribir eso de vuelta corrompe la lista y el render pierde el
# nucleo y la reticula.
render = base.op('render')
if setp(render, 'geometry', 'nucleo reticula baliza'):
    ok('render dibuja: nucleo reticula baliza')
else:
    fail('no pude fijar la geometria del render: pon a mano "nucleo reticula baliza"')
ok('baliza: esfera cian con su propio material, gira con el planeta')


# -----------------------------------------------------------------------------
# 4. ENTRADA MIDI
# -----------------------------------------------------------------------------

midi_log = fresh(base, 'tableDAT', 'midi_log', -440, 200)
midi_log.clear()
midi_log.appendRow(['frame', 'canal', 'nota', 'vel', 'resultado'])

MIDI_CB = '''# Notas del SEQ1 -> baliza.
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
    c = op('baliza_chop')
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
    c = op('baliza_chop')
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
# 5. LEYENDA: se anade el apartado de la nota
# -----------------------------------------------------------------------------

rotulo = base.op('rotulo')
if setexpr(rotulo, 'text',
           "parent().op('ritmo').module.legend(absTime.frame) + "
           "parent().op('baliza_callbacks').module.legend(absTime.frame)"):
    ok('leyenda: apartado NOTA / PULSO / SEQ1 debajo del de tempo')
else:
    fail('no pude enlazar la leyenda')


# -----------------------------------------------------------------------------
# 6. AUTOPRUEBA: una nota simulada por el mismo camino que el MIDI real
# -----------------------------------------------------------------------------

print('CAMBIOS')
print('-' * 66)
for line in report:
    print(line)
print()
print('AUTOPRUEBA (sin BeatStep): nota 64 en el canal 13, en bytes 9C 40 64')
print('-' * 66)

passed = False
try:
    mm = midi_cb.module
    before = int(base.par.Nota)
    baliza_chop.store('printed', 99)            # que la prueba no ensucie
    mm.onReceiveMIDI(None, 0, 'Note On', 13, 65, 100, True, bytes([0x9C, 0x40, 0x64]))
    baliza_chop.cook(force=True)
    note = int(baliza_chop['note'][0])
    env = float(baliza_chop['env'][0])
    rad = float(baliza_chop['radius'][0])
    ign = mm.handle(1, 60, 100)
    print('  nota leida de los bytes : %d  (debe ser 64, aunque el campo decia 65)' % note)
    print('  pulso                   : %.2f  (debe estar cerca de 1)' % env)
    print('  radio                   : %.2f' % rad)
    print('  nota en el canal 1      : %s' % ign)
    print('  leyenda:')
    for l in baliza_cb.module.legend().split('\n'):
        if l.strip():
            print('   ' + l)
    passed = note == 64 and env > 0.8 and ign.startswith('ignorado')
    base.par.Nota = before
    baliza_chop.store('hits', 0)
    baliza_chop.store('printed', 0)
    midi_log.clear()
    midi_log.appendRow(['frame', 'canal', 'nota', 'vel', 'resultado'])
except Exception as e:
    print('  FALLO en la autoprueba: %s' % e)

print('-' * 66)
print('  AUTOPRUEBA %s' % ('OK' if passed else 'FALLIDA: pegame este bloque'))
print('-' * 66)
print('  Ahora: PLAY en el BeatStep con el SEQ1 sonando.')
print('  Las primeras notas salen aqui, con DISPARO o el motivo de ignorarlas.')
print('  Si no sale ninguna: el Device ID de midi_in no es el del BeatStep.')
print('  Si salen como "ignorado: canal X": el SEQ1 no esta en el 13; cambia')
print('  Canal en la pagina Fase2.')
print('  Para probar sin BeatStep: mueve Nota en la pagina Fase2.')
print('=' * 66)
