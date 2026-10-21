"""
=============================================================================
ESTRATOS - FASE 18: ESCENAS DE PRUEBA Y DIRECCION TEMATICA
=============================================================================
Requiere la fase 17. Cierra las dos escenas acotadas, naturaleza y ciudad,
como presets listos para actuar.

QUE HACE
--------
  ESCENAS      paleta (Paleta, Paletatono, Paletacroma), umbrales
               (Umbralvecindad, Pesovecina, Mincluster, Umbraldensidad),
               Caos, Maxpiezas, material (Rugmin, Rugmax), pulso (Swaymax,
               Trafico) y luz (Luzcalida y el dimmer de luz_principal y
               luz_relleno), guardados por escena en la tabla 'escenas'.
               Escena los carga (tambien el Tema: con Temaenciclo, espera al
               fin de ciclo); Guardarescena guarda lo que haya en la escena
               elegida; Cargarescena vuelve a ella. Al instalar la fase no se
               carga nada: tus valores se quedan hasta que elijas una escena.
  LUZ LOCAL    sin luces nuevas (solo el destello de la fase 9 es una luz):
               emisivos aditivos e instancias (geometria luz_local). Focos
               ambar en las obras a medias de la ciudad, brillo de las brasas
               de lo que arde y la nube de polvo de los derrumbes.
  DIAGNOSTICO  con Diagnostico: los puentes de los clusters (blanco), las
               rutas del tejido (carreteras amarillas, rios azules) y la
               presion de cada celda (verde; rojo desde Umbralvecindad). El
               modo actuacion lo oculta, como la reticula y la leyenda.
  LEYENDA      ESCENA  ciudad   densidad 42%   piezas 310   luz local 12
               transitos a medias 0
  La sesion de 20 minutos por escena (densidad, piezas y fotogramas) se
  mide fuera de TouchDesigner con pruebas/sesion_escena.py.

PROBAR SIN BEATSTEP
-------------------
  Escena ciudad: cambian paleta, Caos, luz... Sembrarzona2 en dos zonas con
  Avance en gates: las obras a medias llevan focos. Escena naturaleza, un
  bosque denso y Escalar (fase 14): brillan las brasas. Diagnostico: puentes,
  rutas y presion; Modoactuacion los oculta.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase18_escenas.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase18 v1  (escenas por tema, luz local, diagnostico y criterios de cierre)'
banner(VERSION)

base = require_base(18)
motor = install_core(base, CARPETA, 18)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase18)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase18')
add_par(base, page, 'menu', 'Escena', 'Escena (carga su preset)', 'naturaleza', menu=m.ESCENAS)
add_par(base, page, 'pulse', 'Guardarescena', 'Guardar lo que hay en la escena elegida')
add_par(base, page, 'pulse', 'Cargarescena', 'Volver a la escena elegida')
add_par(base, page, 'float', 'Luzcalida', 'Luz calida (0 fria de la fase 10, 1 de dia)', 0.0, 0.0, 1.0,
        clamp=True)
add_par(base, page, 'toggle', 'Diagnostico', 'Capas de diagnostico: puentes, rutas y presion', False)
ok('pagina Fase18: Escena, Guardarescena, Cargarescena, Luzcalida, Diagnostico')

tabla = get_or_make(base, 'tableDAT', 'escenas', -440, 140)
if tabla.numRows <= 1 or tabla[0, 0] is None or tabla[0, 0].val != 'escena':
    tabla.clear()
    tabla.appendRow(['escena', 'parametro', 'valor'])
    for esc in m.ESCENAS:
        for k, v in m.escena_defecto(esc).items():
            tabla.appendRow([esc, k, str(v)])
    ok('tabla escenas: naturaleza y ciudad, %d parametros cada una' % len(m.ESCENA_PARS))
else:
    ok('tabla escenas: se conserva la que habia (%d filas)' % (tabla.numRows - 1))

# -----------------------------------------------------------------------------
# GEOMETRIAS: luz local (aditiva) y diagnostico
# -----------------------------------------------------------------------------

mat = make_constant(base, 'mat_luz_local', 780, 700, (1.0, 1.0, 1.0))
set_additive(mat)
geo = make_instanced(base, 'luz_local', 520, 700, 'mat_luz_local')
bien, det = instance_color_ok(geo)
if bien:
    ok('luz_local: focos de obra, brasas y polvo, emisivos y aditivos (sin luces nuevas)')
else:
    fail('luz_local no lee el color por instancia (%s): Instance 2 -> Color R/G/B = r g b' % det)
make_constant(base, 'mat_diagnostico', 780, 940, (1.0, 1.0, 1.0))
make_instanced(base, 'diagnostico', 520, 940, 'mat_diagnostico')
ok('diagnostico: puentes, rutas y presion (con Diagnostico; Modoactuacion lo oculta)')
apply_wobble(base)
set_render(base)

leeme(base, 18, """FASE 18 - ESCENAS Y DIRECCION TEMATICA
  Escena: naturaleza o ciudad carga su preset (paleta, umbrales, Caos,
  Maxpiezas, material, pulso y luz) de la tabla 'escenas'. Guardarescena
  guarda lo que hay en la escena elegida; Cargarescena vuelve a ella.
  Luz local sin luces: focos en las obras, brasas, polvo (luz_local).
  Diagnostico: puentes, rutas y presion; Modoactuacion lo oculta.
  Sesion de 20 minutos: pruebas/sesion_escena.py (fuera de TouchDesigner).""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    nombres = [f[0] for f in m.ESCENA_PARS] + ['Escena', 'Nota', 'Nota2', 'Velprueba', 'Temaenciclo', 'Avance',
                                               'Diagnostico', 'Modoactuacion', 'Padprueba']
    for nm in nombres:
        try:
            guarda[nm] = m._leer(nm) if '.' in nm else getattr(base.par, nm).eval()
        except Exception:
            pass
    filas = [[tabla[r, k].val for k in range(3)] for r in range(tabla.numRows)]
    try:
        _prueba(t, m)
    finally:                                    # Escena primero: cambiarla carga su preset
        for nm, v in sorted(guarda.items(), key=lambda kv: kv[0] != 'Escena'):
            try:
                m._poner(nm, v) if '.' in nm else setattr(getattr(base.par, nm), 'val', v)
            except Exception:
                pass
        tabla.clear()
        for f in filas:
            tabla.appendRow(f)


def _prueba(t, m):
    base.par.Velprueba = 100
    base.par.Temaenciclo = False
    base.par.Modoactuacion = False

    def escena(nombre):
        base.par.Escena = nombre
        m.on_value('Escena', nombre)

    # 1. escenas: cargar, guardar y volver
    escena('ciudad')
    c = m.cfg()
    luz = base.op('luz_relleno')
    t.check('Escena ciudad: su paleta, umbrales, Caos, Maxpiezas, pulso y luz',
            abs(c['caos'] - 3.74) < 1e-6 and c['max_piezas'] == 5 and abs(c['paleta_tono'] - 205.0) < 1e-6
            and c['trafico'] == 3 and m.tema_de(c) == 'ciudad'
            and (luz is None or abs(float(luz.par.dimmer.eval()) - 0.24) < 1e-6),
            'Caos %.2f Maxpiezas %d Paletatono %.0f' % (c['caos'], c['max_piezas'], c['paleta_tono']))
    base.par.Maxpiezas = 4
    m.on_pulse('Guardarescena')
    escena('naturaleza')
    n_ok = m.cfg()['max_piezas'] == 6 and abs(m.cfg()['caos'] - 3.91) < 1e-6 and m.tema_de(m.cfg()) == 'naturaleza'
    escena('ciudad')
    t.check('Guardarescena guarda la escena elegida; cambiar de escena y volver la recupera',
            n_ok and m.cfg()['max_piezas'] == 4)
    base.par.Maxpiezas = 6
    m.on_pulse('Cargarescena')
    t.check('Cargarescena vuelve a lo guardado', m.cfg()['max_piezas'] == 4)
    # 2. luz local: focos en las obras a medias
    m.reset_world()
    W = m.world()
    W['tema'] = 1
    for nota in (40, 46):
        base.par.Nota2 = nota
        for _ in range(3):
            m.on_pulse('Sembrarzona2')
    W, c = m.world(), m.cfg()
    tf, tc = m.objetivos(W, c)
    obra = next((i for i in range(m.N) if tf[i] >= 2), None)
    if obra is not None:
        W['et_f'][obra] = 1                     # una obra a medias
    filas = m.build_luz_local(W, c, 0.0)
    focos = [f for f in filas if tuple(f[9:12]) == m.COL_FOCO]
    t.check('luz local: focos ambar en las obras a medias de la ciudad (%d)' % len(focos),
            obra is not None and focos and len(focos) == len(m.obras_a_medias(W, c)))
    # 3. brasas y polvo
    escena('naturaleza')
    m.reset_world()
    W = m.world()
    W['tema'] = 0
    base.par.Nota = 64
    for _ in range(3):
        m.on_pulse('Sembrarzona')
    for _ in range(12):
        m.on_pulse('Sembrar')
    W, c = m.world(), m.cfg()
    vivas = [i for i in range(m.N) if W['occ'][i] > 0][:3]
    W['cats'] = [dict(tipo='incendio', especie='vegetacion', activas=dict((i, 1) for i in vivas), grande=False)]
    W['polvo'] = [[0.0, vivas[0], 'polvo', 8]] if vivas else []
    filas = m.build_luz_local(W, c, 0.05)
    brasas = [f for f in filas if f[9] > 0.15 and f[10] < 0.5 * f[9] and tuple(f[9:12]) != m.COL_FOCO]
    polvo = [f for f in filas if abs(f[9] - f[10] * m.COL_POLVO_LUZ[0] / m.COL_POLVO_LUZ[1]) < 1e-6
             and f[9] < m.COL_POLVO_LUZ[0] + 1e-6]
    t.check('luz local: brillo de las brasas de lo que arde y nube de polvo',
            vivas and len(brasas) >= len(vivas) and polvo, '%d brasas, %d polvo' % (len(brasas), len(polvo)))
    W['cats'] = []
    W['polvo'] = []
    # 4. diagnostico: puentes, rutas y presion; la actuacion lo oculta
    base.par.Diagnostico = True
    c = m.cfg()
    diag = m.build_instances(W, c, 0.0, hide_beacons=False).get('diagnostico', [])
    presion = [f for f in diag if tuple(f[9:12]) in (m.COL_DIAG_BAJA, m.COL_DIAG_ALTA)]
    puentes = [f for f in diag if tuple(f[9:12]) == m.COL_DIAG_PUENTE]
    base.par.Modoactuacion = True
    oculto = not m.build_instances(W, m.cfg(), 0.0, hide_beacons=m.performance()).get('diagnostico')
    base.par.Modoactuacion = False
    base.par.Diagnostico = False
    sin = not m.build_instances(W, m.cfg(), 0.0, hide_beacons=False).get('diagnostico')
    t.check('diagnostico: puentes y presion; Modoactuacion y Diagnostico apagado lo ocultan',
            presion and puentes and oculto and sin, '%d puentes, %d barras' % (len(puentes), len(presion)))
    # 5. criterios de cierre
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    t.check('ningun transito queda colgado tras un fin de ciclo', not m.transitos_colgados(W, c),
            '%d' % len(m.transitos_colgados(W, c)))
    semilla, corona = m.px_formaciones(W, c)
    t.check('una formacion grande se distingue de una pequena a distancia de camara '
            '(semilla %.0f px, coronacion %.0f px en 720)' % (semilla, corona), semilla >= 6 and corona >= 4 * semilla)
    t.check('leyenda ESCENA con densidad, piezas y luz local',
            'ESCENA' in m.legend() and 'densidad' in m.legend())


run_test(base, prueba)
print('  Ahora: elige Escena (naturaleza o ciudad). Ajusta lo que quieras y pulsa')
print('  Guardarescena. Modoactuacion deja solo el mundo, con su luz local.')
print('=' * 66)
