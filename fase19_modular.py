"""
=============================================================================
ESTRATOS - FASE 19: SENALES DEL MODULAR
=============================================================================
Requiere la fase 18. Cuatro senales de control del modular modulan como se
ve el mundo, en el nivel de los moduladores (fase 12): no cambian el mundo.
Llegan como VALORES DE CONTROL (el voltaje convertido), nunca como analisis
del audio: el marco no lo quiere, y analizar el sonido volveria la pieza
visualizacion reactiva.

QUE HACE
--------
  LFO          naturaleza: viento en el dosel, hasta Vientomax grados a un
               lado y al otro (encima del balanceo del pulso). Ciudad: las
               ventanas respiran (Respiracion: cuanto se apagan con el LFO
               abajo).
  RUIDO        naturaleza: mas esporas sobre los bosques. Ciudad: smog, una
               bruma parda que deriva sobre los edificios (Smog).
  ESPACIALIDAD niebla de distancia: lo lejano se funde con la bruma (Niebla).
               En la piel la calcula su shader; para los demas materiales,
               la niebla de la camara.
  SATURACION   fracturas y glitch en los materiales de la piel (Glitch).

DE DONDE LLEGAN (Fuentemodular)
-------------------------------
  osc      OSC por UDP (ethernet), al puerto Puertoosc (9000):
           /estratos/lfo, /estratos/ruido, /estratos/espacio,
           /estratos/saturacion (vale cualquier ruta que acabe asi; si
           ningun canal se llama asi, los cuatro primeros, en ese orden).
           Lo recibe el OSC In CHOP 'modular_osc'.
  chop     cualquier CHOP (Chopmodular): una interfaz de audio acoplada en
           continua (Audio Device In), los CC de un conversor CV-MIDI...
           Se lee su valor, no se analiza.
  manual   los deslizadores Lfo, Ruido, Espacio y Saturacion.
  prueba   un generador sin azar: LFO de 4 s, ruido que salta cada medio
           segundo, espacio que va y viene en 20 s, rafagas de saturacion.
  Rangomodular: en que rango llegan (0..1, -1..1, 0..10 V, -5..5 V,
  -10..10 V).
  Suavizado: segundos para alisarlas (0,15).
  LEYENDA  MODULAR  osc :9000   lfo 0.62   ruido 0.10   espacio 0.40
           saturacion 0.00   hace 0.1 s

PROBAR SIN MODULAR
------------------
  Fuentemodular = prueba: el dosel se mueve con el viento, la niebla va y
  viene y cada ocho segundos los materiales se fracturan. O manual, y mueve
  los deslizadores.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase19_modular.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase19 v2  (senales del modular: viento, respiracion, esporas, smog, niebla y glitch; rango -10..10 V)'
banner(VERSION)

base = require_base(19)
motor = install_core(base, CARPETA, 19)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase19)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase19')
add_par(base, page, 'menu', 'Fuentemodular', 'De donde llegan las senales del modular', 'osc',
        menu=m.FUENTES_MODULAR)
add_par(base, page, 'int', 'Puertoosc', 'Puerto OSC (UDP)', 9000, 1, 65535, clamp=True)
add_par(base, page, 'str', 'Chopmodular', 'CHOP con las senales (Fuentemodular = chop)', '')
add_par(base, page, 'menu', 'Rangomodular', 'Rango en que llegan', '0..1', menu=[r[0] for r in m.RANGOS_MODULAR])
try:                                    # v2: el menu de un proyecto en la v1 gana -10..10 V
    rp = base.par.Rangomodular
    if list(rp.menuNames) != [r[0] for r in m.RANGOS_MODULAR]:
        actual = rp.eval()
        rp.menuNames = rp.menuLabels = [r[0] for r in m.RANGOS_MODULAR]
        rp.val = actual
        ok('Rangomodular: nuevo rango -10..10 V')
except Exception:
    pass
add_par(base, page, 'float', 'Suavizado', 'Suavizado (s)', 0.15, 0.0, 2.0)
for nm, et, v0 in (('Lfo', 'LFO (0,5: sin viento)', 0.5), ('Ruido', 'Ruido', 0.0),
                  ('Espacio', 'Espacialidad', 0.0), ('Saturacion', 'Saturacion', 0.0)):
    add_par(base, page, 'float', nm, '%s (Fuentemodular = manual)' % et, v0, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Vientomax', 'LFO: viento en el dosel (grados)', 12.0, 0.0, 45.0)
add_par(base, page, 'float', 'Respiracion', 'LFO: respiracion de las ventanas', 0.75, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Smog', 'Ruido: smog de la ciudad', 1.0, 0.0, 2.0)
add_par(base, page, 'float', 'Niebla', 'Espacialidad: niebla de distancia', 1.0, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Glitch', 'Saturacion: fracturas y glitch', 1.0, 0.0, 1.0, clamp=True)
ok('pagina Fase19: Fuentemodular (osc), Puertoosc 9000, Chopmodular, Rangomodular, Suavizado, '
   'Lfo Ruido Espacio Saturacion, Vientomax 12, Respiracion 0,75, Smog, Niebla, Glitch')

osc = get_or_make(base, 'oscinCHOP', 'modular_osc', -660, 460)
puerto = setexpr(osc, 'port', 'int(parent().par.Puertoosc)')
setp_any(osc, ['active'], True)
if puerto:
    ok('modular_osc: OSC In CHOP en el puerto Puertoosc (/estratos/lfo, ruido, espacio, saturacion)')
else:
    info('modular_osc: no pude enlazar su puerto; pon Port = Puertoosc a mano')

if modular_al_dia(base):
    ok('camara: niebla lineal que sigue a la espacialidad del modular')
else:
    info('no encontre la niebla de la camara (Fog): solo la piel tendra niebla de distancia')
piel_al_dia(base, m)                    # el shader con la niebla y el glitch
set_render(base)

leeme(base, 19, """FASE 19 - SENALES DEL MODULAR
  Valores de control (no analisis del audio), de Fuentemodular: osc
  (UDP Puertoosc, /estratos/lfo ruido espacio saturacion), chop
  (Chopmodular), manual o prueba. Rangomodular, Suavizado.
  LFO: viento en el dosel (Vientomax) o ventanas que respiran.
  Ruido: esporas o smog. Espacialidad: niebla de distancia.
  Saturacion: fracturas y glitch en los materiales.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Fuentemodular', 'Rangomodular', 'Suavizado', 'Lfo', 'Ruido', 'Espacio', 'Saturacion',
               'Vientomax', 'Respiracion', 'Smog', 'Niebla', 'Glitch', 'Tema', 'Temaenciclo', 'Nota', 'Nota2',
               'Swaymax', 'Velprueba'):
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
        m._CACHE['modular'] = None
        m._CACHE['ventanas'] = None


def _prueba(t, m):
    base.par.Temaenciclo = False
    base.par.Velprueba = 100
    base.par.Suavizado = 0.15
    base.par.Vientomax = 12.0
    base.par.Swaymax = 0.0
    base.par.Fuentemodular = 'manual'
    reloj = [absTime.seconds + 50.0]

    def senales(lfo=0.0, ruido=0.0, espacio=0.0, saturacion=0.0, seg=2.0):
        base.par.Lfo, base.par.Ruido, base.par.Espacio, base.par.Saturacion = lfo, ruido, espacio, saturacion
        W, c = m.world(), m.cfg()
        for _ in range(int(seg * 30)):
            reloj[0] += 1.0 / 30.0
            m.modular_tick(W, c, m.leer_modular(c, reloj[0]), 1.0 / 30.0, reloj[0])
        m._CACHE['modular'] = dict(W['modular'])
        m._CACHE['ventanas'] = None
        return W, c

    # 1. rangos y canales
    t.check('Rangomodular: 0..10 V, -5..5 V, -10..10 V y -1..1 pasan a 0-1',
            abs(m.normalizar(5.0, 2) - 0.5) < 1e-9 and abs(m.normalizar(0.0, 3) - 0.5) < 1e-9
            and m.normalizar(-1.0, 1) == 0.0 and m.normalizar(12.0, 2) == 1.0
            and abs(m.normalizar(-5.0, 4) - 0.25) < 1e-9
            and '-10..10 V' in list(base.par.Rangomodular.menuNames))
    t.check('canales: por nombre (/estratos/ruido...) o, si no, los cuatro primeros en orden',
            m.canal_de(['estratos/lfo', 'estratos/ruido'], 'ruido', 1) == 1
            and m.canal_de(['chan1', 'chan2', 'chan3', 'chan4'], 'saturacion', 3) == 3
            and m.canal_de(['estratos/lfo'], 'ruido', 1) is None)
    # 2. suavizado
    W, c = senales(lfo=1.0, seg=0.1)
    medio = W['modular']['lfo']
    W, c = senales(lfo=1.0, seg=2.0)
    t.check('Suavizado: la senal llega alisada', 0.1 < medio < 0.9 and W['modular']['lfo'] > 0.99,
            '%.2f a los 0,1 s' % medio)
    # 3. LFO -> viento en el dosel
    base.par.Tema = 'naturaleza'
    m.reset_world()
    W = m.world()
    W['tema'] = 0
    W, c = senales(lfo=1.0)
    a1 = m.balanceo(W, c, 40, 0.0)
    W, c = senales(lfo=0.0)
    a0 = m.balanceo(W, c, 40, 0.0)
    t.check('LFO: viento en el dosel, a un lado y al otro (Vientomax 12)',
            a1[0] >= 11.5 and a0[0] >= 11.5 and a1[1] != a0[1], '%s y %s' % (a1, a0))
    # 4. ruido -> esporas
    base.par.Nota = 64
    for _ in range(3):
        m.on_pulse('Sembrarzona')
    for _ in range(12):
        m.on_pulse('Sembrar')
    W = m.world()
    for i in range(m.N):
        if W['occ'][i] > 0:
            W['vh'][i] = max(W['vh'][i], W['h'][i])
    W, c = senales(ruido=0.0)
    e0 = len(m.build_instances(W, c, reloj[0]).get('particulas', []))
    W, c = senales(ruido=1.0)
    e1 = len(m.build_instances(W, c, reloj[0]).get('particulas', []))
    t.check('ruido: mas esporas sobre los bosques (%d -> %d)' % (e0, e1), e1 > e0)
    # 5. espacialidad -> niebla; saturacion -> glitch
    W, c = senales(espacio=0.0, saturacion=0.0)
    n0, g0 = m.modular_uniforme('niebla', 0), m.modular_uniforme('glitch', 0)
    lejos0 = m.niebla_camara('cerca')
    W, c = senales(espacio=1.0, saturacion=1.0)
    n1, g1 = m.modular_uniforme('niebla', 0), m.modular_uniforme('glitch', 0)
    cerca, lejos = m.modular_uniforme('niebla', 1), m.modular_uniforme('niebla', 2)
    t.check('espacialidad: niebla de distancia (uNiebla y la camara)',
            n0 == 0.0 and n1 > 0.95 and 0 <= cerca < lejos and lejos0 > 1e4 and m.niebla_camara('cerca') < 1e4,
            'cerca %.1f lejos %.1f' % (cerca, lejos))
    t.check('saturacion: fracturas y glitch (uGlitch)', g0 == 0.0 and g1 > 0.95)
    # 6. ciudad: el LFO hace respirar las ventanas; el ruido, smog
    base.par.Tema = 'ciudad'
    m.reset_world()
    W = m.world()
    W['tema'] = 1
    base.par.Nota = 64
    for _ in range(3):
        m.on_pulse('Sembrarzona')
    W = m.world()
    for i in range(m.N):
        if W['occ'][i] > 0:
            W['vh'][i] = max(W['vh'][i], W['h'][i])
    W, c = senales(lfo=0.0)
    v0 = m.ventanas_luz()
    W, c = senales(lfo=1.0)
    v1 = m.ventanas_luz()
    t.check('ciudad: las ventanas respiran con el LFO (Respiracion 0,75)',
            abs(v0 - 0.25) < 0.02 and v1 > 0.98, '%.2f -> %.2f' % (v0, v1))
    W, c = senales(ruido=0.0)
    s0 = [f for f in m.build_instances(W, c, reloj[0]).get('particulas', []) if tuple(f[9:12]) == m.COL_SMOG]
    W, c = senales(ruido=1.0)
    s1 = [f for f in m.build_instances(W, c, reloj[0]).get('particulas', []) if tuple(f[9:12]) == m.COL_SMOG]
    t.check('ciudad: el ruido trae smog (%d)' % len(s1), not s0 and s1)
    # 7. fuentes: prueba (sin azar) y osc sin senal
    base.par.Fuentemodular = 'prueba'
    c = m.cfg()
    p1, p2 = m.leer_modular(c, 3.3), m.leer_modular(c, 3.3)
    p3 = m.leer_modular(c, 7.1)
    t.check('Fuentemodular prueba: senales que cambian, la misma en el mismo instante', p1 == p2 and p1 != p3)
    base.par.Fuentemodular = 'osc'
    c = m.cfg()
    osc = base.op('modular_osc')
    sin = not getattr(osc, 'numChans', 0)
    W = m.world()
    if sin:
        for _ in range(int(3.0 * 30)):          # sin mensajes: vuelven al reposo
            reloj[0] += 1.0 / 30.0
            m.modular_tick(W, c, m.leer_modular(c, reloj[0]), 1.0 / 30.0, reloj[0])
    md = W['modular']
    t.check('Fuentemodular osc: sin mensajes, las senales vuelven al reposo (LFO al centro, sin viento)',
            osc is not None and sin and m.leer_modular(c, 1.0) is None and not md['activo']
            and abs(md['lfo'] - 0.5) < 0.02 and md['saturacion'] < 0.02,
            'lfo %.2f' % md['lfo'])
    t.check('leyenda MODULAR', 'MODULAR' in m.legend() and 'osc :' in m.legend())


run_test(base, prueba)
print('  Ahora: Fuentemodular = prueba para verlo sin el modular. Con el modular,')
print('  manda OSC a este ordenador, puerto Puertoosc: /estratos/lfo, /estratos/ruido,')
print('  /estratos/espacio y /estratos/saturacion (en el rango de Rangomodular).')
print('=' * 66)
