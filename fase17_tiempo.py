"""
=============================================================================
ESTRATOS - FASE 17: TIEMPO (TEMPO, TRANSPORTE Y CAMBIO DE PATTERN)
=============================================================================
Requiere la fase 16. Las senales de tiempo dejan de ser solo reloj y se ven
en el paisaje.

QUE HACE
--------
  PULSO        un contador de beats que avanza con el tempo del proyecto y
               se pone a 0 con el START del BeatStep. Con Masterbeat (la ruta
               de un CHOP, por ejemplo master_beat) sigue su primer canal.
               Todo lo que respira va en fase con el, a saltos de
               stop-motion:
                 naturaleza  el dosel se balancea (Swaymax grados, un vaiven
                             cada dos beats) y las esporas derivan sobre los
                             bosques ramificados;
                 ciudad      trafico de puntos por las carreteras de la fase
                             13 (Trafico por tramo, un tramo cada dos beats:
                             con mas BPM, mas deprisa; faros claros a la ida,
                             pilotos rojos a la vuelta) y ventanas que
                             parpadean en cada beat.
  TRANSPORTE   con la linea de tiempo parada o tras un STOP del BeatStep, el
               pulso se congela: el mundo queda quieto pero visible. PLAY o
               START lo reanudan.
  FRENTE       un cambio de pattern (el aviso de la fase 6: All Notes Off
               sin STOP) lanza una banda de polo sur a polo norte en
               Pasosfrente pasos. Naturaleza: frente meteorologico, una
               banda de nubes que dobla los arboles a su paso y tine la luz.
               Ciudad: una ola de ventanas que se encienden o se apagan.
  BIBLIOTECA   cada pattern deja su firma (las notas de un compas) y su
               estacion (tinte de la luz y ventanas). A mitad del frente se
               compara lo que ya ha sonado: si lo reconoce, el frente
               devuelve el tinte que tuvo la ultima vez (la estacion que
               vuelve); si no, estrena uno.
  LEYENDA      TIEMPO   120 bpm   beat 2/4   frente 6/16   pattern B (conocido)

PROBAR SIN BEATSTEP
-------------------
  Pulsa Frenteprueba: el frente recorre el planeta. Cambia el tempo del
  proyecto y mira el trafico de una ciudad con carreteras. Para la linea de
  tiempo: todo se queda quieto.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase17_tiempo.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase17 v1  (tiempo: pulso en fase con el beat, transporte, frente y biblioteca de patterns)'
banner(VERSION)

base = require_base(17)
motor = install_core(base, CARPETA, 17)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase17)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase17')
add_par(base, page, 'float', 'Swaymax', 'Balanceo maximo del dosel (grados)', 6.0, 0.0, 30.0)
add_par(base, page, 'int', 'Trafico', 'Puntos de trafico por tramo de carretera', 2, 0, 8, clamp=True)
add_par(base, page, 'int', 'Pasosfrente', 'Pasos que tarda el frente de polo a polo', 16, 1, 128, clamp=True)
add_par(base, page, 'str', 'Masterbeat', 'CHOP de master_beat (vacio: el pulso lo cuenta el motor)', '')
add_par(base, page, 'pulse', 'Frenteprueba', 'Cambio de pattern de prueba: lanza el frente')
ok('pagina Fase17: Swaymax 6, Trafico 2, Pasosfrente 16, Masterbeat, Frenteprueba')

# la luz cenital, tenida por la estacion; las ventanas de la ciudad, encendidas
if tiempo_al_dia(base):
    ok('luz_principal: su color lo da el motor (la luz fria de la fase 10, tenida por la estacion)')
else:
    info('no pude enlazar el color de luz_principal (cr cg cb): la luz no se tine')
piel_al_dia(base, m)
set_render(base)

leeme(base, 17, """FASE 17 - TIEMPO
  Pulso: beats con el tempo, a 0 con el START (o Masterbeat). Naturaleza:
  el dosel se balancea (Swaymax) y las esporas derivan. Ciudad: trafico por
  las carreteras (Trafico por tramo, un tramo cada dos beats) y ventanas que
  parpadean. STOP o la linea de tiempo parada lo congelan.
  Cambio de pattern (All Notes Off sin STOP, o Frenteprueba): un frente de
  polo a polo en Pasosfrente pasos; nubes que doblan los arboles y tinen la
  luz, u ola de ventanas. Biblioteca: el pattern conocido trae su tinte.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Temaenciclo', 'Swaymax', 'Trafico', 'Pasosfrente',
               'Masterbeat', 'Cambioentierra', 'Carreteras'):
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
        m._CACHE['tinte'] = None


def _prueba(t, m):
    import math
    base.par.Velprueba = 100
    base.par.Temaenciclo = False
    base.par.Swaymax = 6.0
    base.par.Trafico = 2
    base.par.Pasosfrente = 16
    base.par.Masterbeat = ''
    base.par.Cambioentierra = False
    base.par.Carreteras = True
    reloj = [absTime.seconds + 100.0]

    def correr(seg, tempo=120.0, playing=True):
        W, c = m.world(), m.cfg()
        for _ in range(int(round(seg * 30))):
            reloj[0] += 1.0 / 30.0
            m.tick(W, c, reloj[0], tempo, playing)
        return W, c

    def zona(pulso, nota, veces=3):
        base.par.Nota = nota
        base.par.Nota2 = nota
        for _ in range(veces):
            m.on_pulse(pulso)

    # 1. el pulso: avanza con el tempo, STOP lo congela, START lo pone a 0
    base.par.Tema = 'naturaleza'
    m.reset_world()
    W = m.world()
    W['tema'] = 0
    correr(0.1)
    b0 = W['pulso']['beat']
    correr(1.0, 120.0)
    b1 = W['pulso']['beat']
    correr(1.0, 60.0)
    b2 = W['pulso']['beat']
    t.check('el pulso avanza con el tempo (2 beats por segundo a 120, 1 a 60)',
            abs((b1 - b0) - 2.0) < 0.1 and abs((b2 - b1) - 1.0) < 0.1, '%.2f y %.2f' % (b1 - b0, b2 - b1))
    t.midi(0xFC)                                # STOP del BeatStep
    W['clock']['stop_t'] = reloj[0]
    correr(1.0)
    b3 = W['pulso']['beat']
    parado = W['pulso']['parado'] and abs(b3 - b2) < 1e-9 and 'PARADO' in m.legend()
    correr(0.5, playing=False)
    W['clock']['stop_t'] = -99.0
    W['clock']['start_t'] = -99.0
    correr(0.5, playing=False)
    t.check('STOP o la linea de tiempo parada congelan el pulso', parado and W['pulso']['beat'] == b3)
    m.clock_start(W, reloj[0])
    W['clock']['start_t'] = reloj[0]
    correr(0.5)
    t.check('START: el pulso empieza en 0 y sigue', 0.9 < W['pulso']['beat'] < 1.1 and not W['pulso']['parado'],
            '%.2f' % W['pulso']['beat'])
    # 2. naturaleza: el dosel se balancea con el beat; las esporas derivan
    zona('Sembrarzona', 64, 4)
    for _ in range(10):
        m.on_pulse('Sembrar')
    W, c = correr(3.0)                          # que crezcan (stop-motion)
    W['pulso']['beat'] = 0.5
    i0 = m.build_instances(W, c, reloj[0])
    W['pulso']['beat'] = 1.5
    i1 = m.build_instances(W, c, reloj[0])
    veg = [g for g in i0 if g.startswith('mod_veg_') and i0[g]]
    gira = any([f[3:6] for f in i0[g]] != [f[3:6] for f in i1.get(g, [])] for g in veg)
    inc = [m.balanceo(W, c, x, 0.5)[0] for x in range(m.N)]
    base.par.Swaymax = 0.0
    c0 = m.cfg()
    j0 = m.build_instances(W, c0, reloj[0])
    W['pulso']['beat'] = 0.5
    j1 = m.build_instances(W, c0, reloj[0])
    quieto = all([f[3:6] for f in j0.get(g, [])] == [f[3:6] for f in j1.get(g, [])] for g in veg)
    base.par.Swaymax = 6.0
    t.check('naturaleza: el dosel se balancea en fase con el beat (Swaymax 0: quieto)',
            veg and gira and quieto and 0 < max(inc) <= 6.5, 'hasta %.1f grados' % max(inc))
    esporas = [f for f in i0.get('particulas', []) if abs(f[9] - m.COL_ESPORA[0]) < 1e-6]
    t.check('esporas sobre los bosques ramificados', len(esporas) >= 3, '%d' % len(esporas))
    # 3. el frente: Frenteprueba, de polo a polo, y la biblioteca
    pat1 = [60, 64, 67, 72]
    pat2 = [48, 53, 57, 62]

    def tocar(notas, beats):
        W, c = m.world(), m.cfg()
        for k in range(int(beats * 4)):
            m.note_on(W, c, m.GEO, notas[k % len(notas)], 100, reloj[0], 120.0)
            correr(0.125)

    m.world()['oido'] = []                      # lo sembrado tambien suena: empieza limpio
    tocar(pat1, 4)
    m.on_pulse('Frenteprueba')
    W, c = m.world(), m.cfg()
    f = W['frente']
    t.check('Frenteprueba: empieza el frente y la leyenda lo dice', f is not None and 'frente' in m.legend())
    tocar(pat2, 2)                              # medio frente: 8 pasos
    W, c = m.world(), m.cfg()
    q = m.progreso_frente(W, c)
    nubes = [x for x in m.build_instances(W, c, reloj[0]).get('particulas', [])
             if abs(x[10] - m.COL_NUBE[1] * W['frente']['a']['tinte'][1]) < 1e-6] if W['frente'] else []
    lat = math.degrees(math.asin(max(-1.0, min(1.0, nubes[0][1] / math.sqrt(sum(v * v for v in nubes[0][:3]))))))\
        if nubes else 99.0
    t.check('a mitad del frente, una banda de nubes cerca del ecuador (%d nubes)' % len(nubes),
            0.45 <= (q or 0) <= 0.6 and len(nubes) >= 20 and abs(lat) < 25.0, 'latitud %.0f' % lat)
    dobla = [m.balanceo(W, c, x, m.beat_stop(W, c)) for x in range(m.N)
             if abs(m.latitud(x) - m.lat_frente(q)) < 5.0]
    t.check('el frente dobla los arboles hacia el norte', dobla and all(r == 270.0 and i > 10 for i, r in dobla))
    t.check('a mitad del frente se decide el pattern: nuevo (B)',
            W['frente']['pattern'] == 'B' and W['frente']['conocido'] is False
            and [p['nombre'] for p in W['patrones']] == ['A', 'B'])
    m._CACHE['tinte'] = None
    luz = base.op('luz_principal')
    tin = m.tinte_actual(W, c)
    cr = luz.par.cr.eval() if luz is not None and hasattr(luz.par, 'cr') else None
    t.check('el frente tine la luz (luz_principal sigue al motor)',
            cr is not None and abs(cr - m.LUZ_BASE[0] * tin[0]) < 1e-6 and tin != [1.0, 1.0, 1.0],
            'cr %.3f' % (cr or 0))
    tocar(pat2, 2)
    W, c = m.world(), m.cfg()
    t.check('al llegar al polo norte, la estacion del pattern B se queda',
            W['frente'] is None and W['pattern'] == 'B' and W['estacion']['tinte'] == W['patrones'][1]['tinte'])
    m.on_pulse('Frenteprueba')
    tocar(pat1, 4)
    W, c = m.world(), m.cfg()
    t.check('vuelve el pattern A: lo reconoce y trae su tinte (la estacion que vuelve)',
            W['pattern'] == 'A' and W['ev'].get('frente_fin', {}).get('conocido') is True
            and W['estacion']['tinte'] == W['patrones'][0]['tinte'],
            'pattern %s; %s' % (W['pattern'], ' '.join('%s%s' % (p['nombre'], sorted(p['firma'].items())) for p in W['patrones'])))
    t.check('leyenda TIEMPO con bpm, beat y pattern',
            'TIEMPO' in m.legend() and 'bpm' in m.legend() and 'pattern A (conocido)' in m.legend())
    # 4. el aviso de la fase 6 (All Notes Off sin STOP) lanza el frente
    n_pat = len(W['patrones'])
    for ch in range(8):
        m.on_cc(W, c, ch + 1, 123, 0, reloj[0] + 0.001 * ch)
    correr(0.5)
    W = m.world()
    t.check('All Notes Off sin STOP: cambio de pattern y frente', W['frente'] is not None or len(W['patrones']) > n_pat)
    correr(4.0)
    # 5. ciudad: trafico por las carreteras, al tempo; ventanas que parpadean
    base.par.Tema = 'ciudad'
    m.reset_world()
    W = m.world()
    W['tema'] = 1
    zona('Sembrarzona', 64, 2)
    zona('Sembrarzona', 70, 2)
    zona('Sembrarzona2', 40, 3)
    W, c = correr(3.0)
    W['pulso']['beat'] = 0.0
    ins = m.build_instances(W, c, reloj[0])
    vias = W.get('tejido_vias') or []
    faros = [f for f in ins.get('particulas', []) if tuple(f[9:12]) in (m.COL_FARO, m.COL_PILOTO)]
    W['pulso']['beat'] = 0.5
    ins2 = m.build_instances(W, c, reloj[0])
    faros2 = [f for f in ins2.get('particulas', []) if tuple(f[9:12]) in (m.COL_FARO, m.COL_PILOTO)]
    t.check('ciudad: Trafico puntos por tramo de carretera (%d tramos)' % len(vias),
            vias and len(faros) == 2 * len(vias) and W['tiempo']['trafico'] == len(faros))
    t.check('el trafico se mueve con el pulso (a 120 BPM, un tramo cada segundo)',
            faros and [f[:3] for f in faros] != [f[:3] for f in faros2])
    edif = [f for g, filas in ins.items() if g.startswith(('mod_inf_', 'mod_pla_')) and '_puente' not in g
            for f in filas]
    niveles = set(int(math.floor(f[12] * 0.5 + 0.0001)) for f in edif)
    t.check('ventanas: cada edificio lleva su nivel en el alfa (y el shader las ve desde la fase 17)',
            edif and 4 in niveles and m.ventanas_luz() == 1.0,
            'niveles %s' % ' '.join(str(x) for x in sorted(niveles)))
    parpadea = False
    for b in range(1, 8):
        W['pulso']['beat'] = float(b)
        otro = m.build_instances(W, c, reloj[0])
        e2 = [f for g, filas in otro.items() if g.startswith(('mod_inf_', 'mod_pla_')) and '_puente' not in g
              for f in filas]
        if [round(f[12], 4) for f in e2] != [round(f[12], 4) for f in edif]:
            parpadea = True
            break
    t.check('las ventanas parpadean con el beat', parpadea)
    # 6. ola de ventanas: el frente cambia las ventanas a su paso
    W['estacion'] = dict(tinte=[1.0, 1.0, 1.0], ventanas=1)
    m.on_pulse('Frenteprueba')
    W, c = m.world(), m.cfg()
    W['pulso']['beat'] = W['frente']['beat0'] + 2.0      # mitad del frente
    m.frente_tick(W, c)
    q = m.progreso_frente(W, c)
    bq = m.beat_stop(W, c)
    sur = [x for x in range(m.N) if m.latitud(x) < m.lat_frente(q) - 1.0]
    norte = [x for x in range(m.N) if m.latitud(x) > m.lat_frente(q) + 1.0]
    nv = W['frente']['a']['ventanas']
    apagada, encendida = (0, 3), (1, 4)         # nivel con la estacion apagada / encendida (con parpadeo)
    ola = all(m.ventanas_celda(W, c, x, bq) in (encendida if nv else apagada) for x in sur) \
        and all(m.ventanas_celda(W, c, x, bq) in encendida for x in norte)
    t.check('ciudad: ola de ventanas que se %s al paso del frente' % ('encienden' if nv else 'apagan'),
            sur and norte and ola and nv == 0)


run_test(base, prueba)
print('  Ahora: con el BeatStep en PLAY, el dosel se balancea y el trafico corre al')
print('  tempo; STOP lo congela. Cambia de pattern: un frente cruza el planeta y la')
print('  luz toma la estacion del pattern (la misma si ya habia sonado).')
print('=' * 66)
