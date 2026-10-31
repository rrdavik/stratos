"""
=============================================================================
ESTRATOS - FASE 21: EL MICROFONO DE LA SALA
=============================================================================
Requiere la fase 19 (o la 20, si tienes los POPs). El microfono entra como un
pad 9 de erosion: el motor ya sabe erosionar, cortar, iluminar la celda y
escalar, asi que esta fase solo anade la deteccion y reutiliza el resto. No
analiza la musica: escucha al publico (una palmada, una tos, unos pasos).

QUE HACE
--------
  ONSET        cada bloque de audio se reparte en 16 bandas; el flujo
               espectral es lo que sube la energia de cada banda (en dB)
               respecto a los bloques anteriores. Un sonido que empieza sube
               de golpe; un drone sostenido, no. Pasa Umbralonset (0,6),
               0,12 s despues del anterior y fuera de la
               ventana de un destello propio (la luz de sala de la fase 23):
               es un onset.
  PAD 9        un onset es un golpe de erosion del pad 9 (rol micro, gris
               calido claro): en la celda del objetivo (Objetivo, como los
               pads) baja Reduccionmic escalones enteros (1), enciende su luz
               y suma en ero_resto como un pad. Desde la fase 14 cuenta como
               aranazo: dos onsets en la misma zona escalan.
  RUIDO        la energia de los onsets de los ultimos 60 s:
               al pasar Umbralcorte (20) abre un corte de Profundidadmic
               conchas (3, radio 1) en la celda del ultimo onset, y la cuenta
               vuelve a cero.
  LEYENDA      MICRO  microfono   flujo 0.12/0.60   onsets 12   ultimo flujo 0.71
               celda 40 hace 1.2 s   ruido 5.3/20 en 60 s
  midi_log     una fila por onset: MICRO onset flujo 0.71 celda 40
  PAGINA (v3)  10 parametros en vez de 12: el tiempo muerto entre onsets
               (0,12 s, antes Refractariomic) y la ventana del ruido (60 s,
               antes Ventanaruido) quedan fijos. Relanzar cualquier fase los
               quita de un proyecto anterior y avisa si los habias cambiado.
  SIN SIMULACION (v4)
               7 parametros. Fuera la simulacion de la v1: mic_sim (Script
               CHOP), mic_fuente (Switch CHOP), Simonset, Simruido y Simdrone,
               y las opciones simulacion y ambos de Fuentemic (pasan a
               microfono). Hace lo mismo, y mejor, la sala virtual
               (sala_virtual.py): su microfono virtual entra por Fuentemic =
               chop. Relanzar cualquier fase la quita de un proyecto anterior.

OPERADORES (en /project1/FASE1)
-------------------------------
  mic_in       Audio Device In CHOP: el microfono (elige el dispositivo en su
               parametro Device; el canal, con Canalmic).
  mic_flujo    Script CHOP: lee el bloque de mic_in (o, con Fuentemic = chop,
               del CHOP de Chopmic), calcula el flujo con numpy y llama al
               motor (sin Audio Spectrum CHOP, para poder probarlo fuera de
               TouchDesigner). Saca los canales flujo y onset.

PROBAR SIN MICROFONO
--------------------
  La sala virtual: exec(sala_virtual.py) pone Fuentemic = chop y Chopmic en
  su microfono virtual (con Usarmic). En la pagina Sala de /project1/SALA,
  Palmada: un clic, un onset, una celda que baja; Volumendrone: un drone que
  no da ninguno; unas cuantas Palmada seguidas: el ruido de sala abre un
  corte. Ruidopublico y Personas, el publico entero.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase21_microfono.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase21 v4  (sin la simulacion: Fuentemic microfono o chop; para probar, la sala virtual)'
banner(VERSION)

base = require_base(21)
motor = install_core(base, CARPETA, 21)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase21)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase21')
# v4: microfono o chop (la simulacion y ambos los quita install_core, fase21_sin_simulacion)
add_par(base, page, 'menu', 'Fuentemic', 'De donde llega el sonido de la sala', 'microfono',
        menu=FUENTEMIC_NOMBRES, menu_labels=FUENTEMIC_ETIQUETAS)
add_par(base, page, 'str', 'Chopmic', 'CHOP con el audio (Fuentemic = chop)', '')
add_par(base, page, 'int', 'Canalmic', 'Canal del microfono (0: el primero)', 0, 0, 31, clamp=True)
add_par(base, page, 'float', 'Umbralonset', 'Umbral de onset del microfono', 0.6, 0.0, 5.0, clamp=True)
add_par(base, page, 'float', 'Reduccionmic', 'Erosion de cada onset (escalones)', 1.0, 0.0, 15.0, clamp=True)
add_par(base, page, 'float', 'Umbralcorte', 'Ruido acumulado en 60 s que abre un corte', 20.0, 1.0, 500.0,
        clamp=True)
add_par(base, page, 'int', 'Profundidadmic', 'Profundidad del corte por ruido', 3, 1, 12, clamp=True)
try:
    base.par.Umbralcorte.label = 'Ruido acumulado en 60 s que abre un corte'
except Exception:
    pass
ok('pagina Fase21: Fuentemic (microfono), Chopmic, Canalmic 0, Umbralonset 0,6, Reduccionmic 1, '
   'Umbralcorte 20 (en 60 s), Profundidadmic 3')

# -----------------------------------------------------------------------------
# EL PAD 9 EN LAS TABLAS DE LA BATERIA
# -----------------------------------------------------------------------------


def _cab(t):
    return [t[0, c].val.strip() for c in range(t.numCols)] if t.numRows else []


def anadir_pad9(t, valores):
    """Anade a la tabla la fila del pad 9 (por nombre de columna), si no la
    tiene. Lo demas no se toca. Devuelve si la ha anadido."""
    cab = _cab(t)
    if 'pad' not in cab:
        return False
    ip = cab.index('pad')
    for r in range(1, t.numRows):
        try:
            if int(float(t[r, ip].val)) == m.PAD_MIC + 1:
                return False
        except Exception:
            pass
    t.appendRow([valores.get(c, '') for c in cab])
    return True


PERFIL_PAD9 = dict(pad=m.PAD_MIC + 1, reduccion='%d' % m.PERFIL_MIC[0], radio=m.PERFIL_MIC[1],
                   profundidad=m.PERFIL_MIC[2], modo='erosion', pulsos='1', capacidad='1', pump_rel='0.15',
                   tipo=m.ROL_MIC, rol=m.ROL_MIC)
COLOR_PAD9 = dict(pad=m.PAD_MIC + 1, r='%.3f' % m.COLOR_MIC[0], g='%.3f' % m.COLOR_MIC[1],
                  b='%.3f' % m.COLOR_MIC[2], rol=m.ROL_MIC)

for nombre, valores, que in (('perfiles_erosion', PERFIL_PAD9, 'la reduccion la da Reduccionmic'),
                             ('colores_drum', COLOR_PAD9, 'gris calido claro')):
    tb = base.op(nombre)
    if tb is None:
        fail('%s: no esta; aplica antes fase7_erosion.py' % nombre)
    elif anadir_pad9(tb, valores):
        ok('%s: fila del pad 9, micro (%s); lo demas se conserva' % (nombre, que))
    else:
        ok('%s: ya tiene el pad 9' % nombre)

# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

MIC_FLUJO_CB = r'''# Script CHOP 'mic_flujo' (fase 21): el flujo espectral del bloque de
# mic_in (o del CHOP de Chopmic), el onset y la erosion los calcula el motor
# (mic_cook).


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    op('motor').module.mic_cook(scriptOp)
'''

mic_in = get_or_make(base, 'audiodeviceinCHOP', 'mic_in', -880, 620)
setp_any(mic_in, ['active'], True)
cb = get_or_make(base, 'textDAT', 'mic_flujo_callbacks', -440, 760)
cb.text = MIC_FLUJO_CB
flujo = get_or_make(base, 'scriptCHOP', 'mic_flujo', -220, 620)
setp_any(flujo, ['callbacks', 'callbackdat', 'dat'], 'mic_flujo_callbacks')
connect(flujo, mic_in, 0)
ok('mic_in -> mic_flujo (o el CHOP de Chopmic): el motor lee cada bloque y busca onsets')

hay, texto = m.microfono_encontrado()
if hay:
    ok('microfono: %s' % texto)
else:
    info('microfono: no encuentro ninguno (%s). Elige el dispositivo en mic_in (Device), '
         'o prueba con la sala virtual (sala_virtual.py, Fuentemic = chop)' % texto)

set_render(base)

leeme(base, 21, """FASE 21 - EL MICROFONO DE LA SALA
  Un pad 9 de erosion que golpean los onsets del publico. mic_in (Audio
  Device In; Device en el operador, Canalmic) o el CHOP de Chopmic
  (Fuentemic = chop: la sala virtual) a mic_flujo: flujo espectral en
  16 bandas, onset con Umbralonset (y 0,12 s de tiempo muerto).
  Cada onset baja Reduccionmic escalones en la celda del objetivo, enciende
  su luz (gris calido) y, desde la fase 14, cuenta como aranazo. La energia
  de los onsets de los ultimos 60 s, al pasar Umbralcorte, abre un corte de
  Profundidadmic conchas. La reduccion del pad 9 de perfiles_erosion la da
  Reduccionmic. Sin microfono: la sala virtual (Palmada, Volumendrone).""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

class TablaPrueba(object):
    """Lo justo de una tableDAT para probar anadir_pad9."""

    def __init__(self, filas):
        self.filas = [[str(x) for x in f] for f in filas]

    @property
    def numRows(self):
        return len(self.filas)

    @property
    def numCols(self):
        return max(len(f) for f in self.filas)

    def __getitem__(self, rc):
        r, c = rc
        f = self.filas[r]

        class _C(object):
            val = f[c] if c < len(f) else ''
        return _C()

    def appendRow(self, vals):
        self.filas.append([str(v) for v in vals])


def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Fuentemic', 'Chopmic', 'Canalmic', 'Umbralonset', 'Reduccionmic', 'Umbralcorte', 'Profundidadmic', 'Objetivo', 'Tema', 'Temaenciclo',
               'Nota', 'Velprueba', 'Umbraldensidad', 'Golpesescalada', 'Ventanaescalada'):
        try:
            guarda[nm] = getattr(base.par, nm).eval()
        except Exception:
            pass
    try:
        _prueba(t, m)
    finally:
        for nm, v in guarda.items():
            try:
                getattr(base.par, nm).val = v
            except Exception:
                pass
        m.mic_reset()
        for nm in ('mic_prueba', 'mic_prueba_callbacks'):
            if base.op(nm) is not None:
                base.op(nm).destroy()


MIC_PRUEBA_CB = r'''# Script CHOP 'mic_prueba' (autoprueba de la fase 21; se borra al terminar):
# un bloque de la senal sintetica por cocinado, con un clic si el motor lo pide.


def onSetupParameters(scriptOp):
    return


def onCook(scriptOp):
    m = op('motor').module
    n = 735
    clic = m._MIC['clic'] > 0
    if clic:
        m._MIC['clic'] -= 1
    x = m.mic_sim_bloque(n, m.MIC_RATE, m._MIC['muestra'], clic=clic)
    m._MIC['muestra'] += n
    scriptOp.isTimeSlice = False
    scriptOp.clear()
    scriptOp.rate = m.MIC_RATE
    scriptOp.numSamples = n
    scriptOp.appendChan('mic').vals = [float(v) for v in x]
'''


def crear_mic_prueba():
    cb = get_or_make(base, 'textDAT', 'mic_prueba_callbacks', -880, 900)
    cb.text = MIC_PRUEBA_CB
    o = get_or_make(base, 'scriptCHOP', 'mic_prueba', -660, 900)
    setp_any(o, ['callbacks', 'callbackdat', 'dat'], 'mic_prueba_callbacks')
    return o


def _prueba(t, m):
    base.par.Velprueba = 100
    base.par.Umbraldensidad = 0.95              # sin el presupuesto de densidad
    base.par.Objetivo = 'seq1'
    base.par.Temaenciclo = False
    base.par.Golpesescalada = 2
    base.par.Ventanaescalada = 8
    base.par.Fuentemic = 'microfono'
    base.par.Canalmic = 0
    base.par.Umbralonset = 0.6
    base.par.Reduccionmic = 1.0
    base.par.Umbralcorte = 20.0
    base.par.Profundidadmic = 3
    R, n = 44100, 735
    reloj = [absTime.seconds + 100.0]
    muestra = [0]

    def bloques(W, c, k, clics=(), drone=False, ruido=0.0):
        """k bloques de 1/60 s de la senal sintetica, con un clic en los de
        clics. Devuelve (onsets, flujo maximo)."""
        evs, fmax = [], 0.0
        for j in range(k):
            reloj[0] += 1.0 / 60.0
            x = m.mic_sim_bloque(n, R, muestra[0], clic=j in clics, ruido=ruido, drone=drone)
            muestra[0] += n
            r = m.mic_bloque(W, c, x, R, reloj[0])
            fmax = max(fmax, r['flujo'])
            if r['onset']:
                evs.append(r['onset'])
        return evs, fmax

    def nuevo(nota=64):
        m.reset_world()
        m.mic_reset()
        base.par.Nota = nota
        return m.world(), m.cfg()

    # 1. el detector
    W, c = nuevo()
    bloques(W, c, 10)
    uno, f1 = bloques(W, c, 20, clics=(5,))
    m.mic_reset()
    bloques(W, c, 6, drone=True)
    dron, fd = bloques(W, c, 300, drone=True)
    t.check('un clic sintetico da un onset; un drone sostenido (5 s), ninguno',
            len(uno) == 1 and not dron, 'flujo del clic %.2f, maximo del drone %.2f' % (f1, fd))
    W, c = nuevo()
    bloques(W, c, 10)
    juntos, _ = bloques(W, c, 30, clics=(5, 9))         # 0,07 s: dentro de Refractariomic
    separados, _ = bloques(W, c, 60, clics=(5, 35))     # 0,5 s
    t.check('dos clics dentro de los 0,12 s de tiempo muerto dan un onset; separados, dos',
            len(juntos) == 1 and len(separados) == 2, '%d y %d' % (len(juntos), len(separados)))

    # 2. un onset es el pad 9: baja escalones enteros, enciende su luz y suma en ero_resto
    W, c = nuevo()
    celda = m.note_cell(64)
    for _ in range(60):                 # ocupacion 4: sin satelites (que bajarian antes)
        if W['occ'][celda] >= 4:
            break
        m.on_pulse('Sembrar')
    occ0 = W['occ'][celda]
    base.par.Reduccionmic = 1.5
    c = dict(m.cfg())
    c['nivel'] = 13                     # el golpe solo, sin el accidente de la fase 14
    ev = m.erosion_mic(W, c, reloj[0], 1.0)
    occ1, resto1 = W['occ'][celda], W['ero_resto'][celda]
    luz = W['luz'].get(celda, {}).get(m.PAD_MIC)
    ev2 = m.erosion_mic(W, c, reloj[0] + 0.5, 1.0)
    occ2 = W['occ'][celda]
    col = m.drum_color(c, m.PAD_MIC)
    t.check('un onset erosiona como el pad 9: Reduccionmic 1,5 baja 1 escalon y deja 0,5 en ero_resto; '
            'el siguiente, 2',
            ev['pad'] == m.PAD_MIC and ev['celda'] == celda and occ0 >= 4 and occ1 == occ0 - 1
            and abs(resto1 - 0.5) < 1e-9 and occ2 == occ0 - 3 and ev2['quitado'] == 2,
            'ocupacion %d -> %d -> %d' % (occ0, occ1, occ2))
    t.check('el onset enciende la luz de su celda con el color del pad 9 (gris calido claro)',
            luz is not None and m.drum_light(W, c, celda, reloj[0] + 0.5)[1] == m.PAD_MIC
            and all(abs(a - b) < 0.01 for a, b in zip(col, m.COLOR_MIC)), str(col))
    base.par.Reduccionmic = 1.0

    # 3. el ruido de sala
    def mundo_con_conchas():
        W, c = nuevo()
        for _ in range(4):
            m.on_pulse('Sembrarzona')
            m.end_cycle(W, c, reloj[0])
            reloj[0] += 1.0
        m.on_pulse('Sembrarzona')
        return W, m.cfg()
    W, c = mundo_con_conchas()
    bloques(W, c, 10)
    evs = []
    while len(evs) < 40 and not W['ruido']['cortes']:
        e, _ = bloques(W, c, 30, clics=(3,))           # un clic cada medio segundo
        evs += e
    ultimo = W['ev'].get('ruido') or {}
    energia = sum(e['flujo'] for e in evs)
    t.check('clics hasta Umbralcorte en 60 s: un corte de Profundidadmic (3) en la celda del '
            'ultimo onset, y la cuenta a cero',
            W['ruido']['cortes'] == 1 and ultimo.get('prof') == 3 and ultimo.get('conchas', 0) > 0
            and ultimo.get('celda') == evs[-1]['celda'] and not W['ruido']['onsets']
            and W['ruido']['total'] == 0.0 and energia >= c['umbral_corte'],
            '%d onsets, energia %.1f, %d conchas' % (len(evs), energia, ultimo.get('conchas', 0)))
    base.par.Umbralcorte = 500.0
    W, c = mundo_con_conchas()
    bloques(W, c, 10)
    evs = []
    for _ in range(12):
        e, _ = bloques(W, c, 30, clics=(3,))
        evs += e
    t.check('ruido por debajo de Umbralcorte: ningun corte',
            len(evs) == 12 and not W['ruido']['cortes'] and W['ruido']['total'] > 0,
            'energia %.1f de 500' % W['ruido']['total'])
    base.par.Umbralcorte = 20.0
    W['ruido']['onsets'] = [[reloj[0] - 70.0, 30.0, 0]]
    m.ruido_tick(W, m.cfg(), reloj[0])
    t.check('lo que sale de los 60 s no cuenta', not W['ruido']['onsets'] and not W['ruido']['cortes'])

    # 4. el destello propio
    W, c = nuevo()
    bloques(W, c, 10)
    W['sala']['destellos'].append(reloj[0] + 1.0 / 60.0)
    tras, _ = bloques(W, c, 3, clics=(0,))
    luego, _ = bloques(W, c, 30, clics=(20,))
    t.check('un onset justo tras un destello propio se descarta; mas tarde, cuenta',
            not tras and len(luego) == 1 and W['mic']['descartados'] == 1)

    # 5. desde la fase 14, dos onsets en la misma zona escalan (D9)
    base.par.Tema = 'naturaleza'
    W, c = nuevo()
    for _ in range(4):
        m.on_pulse('Sembrarzona')
    for _ in range(8):
        m.on_pulse('Sembrar')
    W['vh'] = list(W['h'])
    c = m.cfg()
    e1 = m.erosion_mic(W, c, reloj[0], 1.0)
    e2 = m.erosion_mic(W, c, reloj[0] + W['paso'], 1.0)
    t.check('el pad 9 es un aranazo: dos onsets en la misma zona escalan (incendio en un bosque)',
            m.es_aranazo(c, m.PAD_MIC) and not e1.get('escalada') and e2.get('escalada') == 'incendio',
            str(e2.get('escalada')))

    # 6. las tablas ganan el pad 9 sin perder nada
    cols = ['pad', 'reduccion', 'radio', 'profundidad', 'modo', 'pulsos', 'pump_rel', 'tipo', 'rol']
    ocho = [cols] + [[k + 1, 2, 1, 0, 'erosion', 1, 0.15, 'aranazo', 'x'] for k in range(8)]
    ocho[2][1] = 7                                  # editada a mano
    tb = TablaPrueba(ocho)
    antes = [list(f) for f in tb.filas]
    puesta = anadir_pad9(tb, PERFIL_PAD9)
    otra = anadir_pad9(tb, PERFIL_PAD9)
    f9 = dict(zip(tb.filas[0], tb.filas[-1]))
    t.check('una tabla de 8 filas, editada, gana el pad 9 sin perder nada (y solo una vez)',
            puesta and not otra and tb.filas[:9] == antes and len(tb.filas) == 10
            and f9['pad'] == '9' and f9['modo'] == 'erosion' and f9['rol'] == 'micro', str(tb.filas[-1]))
    c = m.cfg()
    t.check('el motor lee 9 pads; el noveno, de erosion con la reduccion de Reduccionmic',
            len(c['perfiles']) == 9 and c['modos'][m.PAD_MIC] == 'erosion'
            and c['perfiles'][m.PAD_MIC][0] == 1.0 and len(c['colores_drum']) == 9)

    # 7. la cadena de operadores con Fuentemic = chop: un CHOP de prueba (que la
    # autoprueba crea y borra) con la senal sintetica, por mic_flujo
    W, c = nuevo()
    chop = crear_mic_prueba()
    base.par.Fuentemic = 'chop'
    base.par.Chopmic = chop.path
    for _ in range(5):
        m.mic_tick(W, m.cfg(), reloj[0])
    m._MIC['clic'] += 1
    m.mic_tick(W, m.cfg(), reloj[0])
    t.check('Fuentemic chop: un clic en el CHOP de Chopmic llega por mic_flujo: un onset',
            W['mic']['n'] == 1 and base.op('mic_flujo') is not None and 'chop ' in m.legend(),
            'onsets %d' % W['mic']['n'])
    log = base.op('midi_log')
    filas = [log[r, log.numCols - 1].val for r in range(log.numRows)] if log is not None else []
    t.check('midi_log: una fila MICRO por onset', any(f.startswith('MICRO onset flujo') for f in filas))
    t.check('leyenda MICRO', 'MICRO' in m.legend() and 'onsets 1' in m.legend())
    # v4: sin la simulacion
    t.check('sin simulacion: ni mic_sim ni mic_fuente; Simonset, Simruido y Simdrone fuera; '
            'Fuentemic microfono o chop',
            base.op('mic_sim') is None and base.op('mic_fuente') is None
            and not any(has_par(base, nm) for nm in ('Simonset', 'Simruido', 'Simdrone'))
            and list(base.par.Fuentemic.menuNames) == ['microfono', 'chop'])
    # v3: la pagina mas corta
    fuera = [nm for nm, _, _ in FASE21_FIJOS if has_par(base, nm)]
    t.check('pagina Fase21 sin Refractariomic ni Ventanaruido', not fuera,
            'siguen: %s' % ', '.join(fuera) if fuera else '')
    cf = m.cfg()
    t.check('tiempo muerto 0,12 s y ventana del ruido 60 s',
            cf['refractario_mic'] == 0.12 and cf['ventana_ruido'] == 60.0)


run_test(base, prueba)
print('  Ahora: sin microfono, la sala virtual (sala_virtual.py) y su Palmada. Con el')
print('  microfono, elige su Device en mic_in y sube Umbralonset hasta que el drone')
print('  de la sala no de ningun onset.')
print('=' * 66)
