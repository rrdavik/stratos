"""
=============================================================================
ESTRATOS - FASE 12: MODULADORES (VELOCIDAD Y DURACION DEL GATE)
=============================================================================
Requiere la fase 11. (No confundir con fase12_base.py, que son las fases 1
y 2.) Las dos senales que ya modulaban las cajas pasan a modular los modelos
tematicos, y el material deja de necesitar geometrias duplicadas.

QUE HACE
--------
  UN MATERIAL POR MODELO
               una geometria por modelo (de 94 a 49). Un GLSL MAT por familia
               (mat_piel_mineral, mat_piel_dosel, mat_piel_ciudad) lee la
               rugosidad del canal 'a' (el alfa del color) de cada instancia:
               pulido, reflejo fino y fuerte; rugoso, mate y con poros.
  VELOCIDAD -> MATERIAL
               naturaleza: obsidiana pulida <-> piedra pomez; el dosel, vidrio
               ahumado con vetas ambar. Ciudad: vidrio negro <-> hormigon
               brutalista, con ventanas ambar apagadas hasta la fase 17.
               Materialmodo: binario (Umbralvel, como hasta ahora) o continuo
               (de Rugmax a velocidad 0 a Rugmin a 127).
  GATE -> VIGOR
               naturaleza: tronco mas grueso y copa mas ancha con gates largos
               (hasta Vigormax), mas finos con gates cortos. Ciudad: un gate
               ligado (un paso o mas) construye Plantasligado plantas.
  La velocidad sigue sembrando el caos de la fase 11: eso no cambia.

  MATERIALRESPALDO
               si el shader falla (no se ve la piel), cambia en vivo todas las
               geometrias a un Phong (mat_respaldo). El color por instancia ya
               distingue pulido y rugoso.

PROBAR SIN BEATSTEP
-------------------
  Sembrar en la misma celda con Velprueba 10 y 120 (tras Resetmundo), y con
  Gateprueba 0,25, 1 y 2. Los botones de prueba sueltan la nota tras
  Gateprueba pasos. La leyenda MOD dice velocidad, rugosidad, gate y efecto.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase12_moduladores.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase12 v2  (moduladores: velocidad -> material por shader, gate -> vigor y plantas)'
banner(VERSION)

base = require_base(12)
motor = install_core(base, CARPETA, 12)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase12)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase12')
add_par(base, page, 'menu', 'Materialmodo', 'Velocidad -> material', 'continuo', menu=m.MATERIALES,
        menu_labels=['Binario (Umbralvel)', 'Continuo (0 a 127)'])
add_par(base, page, 'float', 'Rugmin', 'Rugosidad a velocidad 127 (pulido)', 0.05, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Rugmax', 'Rugosidad a velocidad 0 (rugoso)', 0.85, 0.0, 1.0, clamp=True)
add_par(base, page, 'float', 'Vigormax', 'Vigor maximo (gate ligado, naturaleza)', 1.5, 0.6, 3.0)
add_par(base, page, 'int', 'Plantasligado', 'Plantas por gate ligado (ciudad)', 2, 1, 8, clamp=True)
add_par(base, page, 'float', 'Gateprueba', 'Gate de los botones de prueba (pasos)', 0.5, 0.05, 8.0)
add_par(base, page, 'toggle', 'Materialrespaldo', 'Material de respaldo (Phong, si el shader falla)', False)
ok('pagina Fase12: Materialmodo (continuo), Rugmin 0,05, Rugmax 0,85, Vigormax 1,5, Plantasligado 2, '
   'Gateprueba 0,5, Materialrespaldo')

# -----------------------------------------------------------------------------
# GEOMETRIAS: una por modelo, con el shader de la piel
# -----------------------------------------------------------------------------

if base.op('modelos') is None:
    raise RuntimeError('Falta modelos en FASE1: aplica antes fase11_piel.py.')
instanciar_modelos(base, m)
set_render(base)

leeme(base, 12, """FASE 12 - MODULADORES
  Velocidad -> material: obsidiana <-> pomez (naturaleza), vidrio negro <->
  hormigon (ciudad), dosel de vidrio ahumado con vetas ambar. Rugosidad en
  el canal 'a' de cada instancia; un GLSL MAT por familia (mat_piel_...).
  Materialmodo binario o continuo; Rugmin y Rugmax.
  Gate -> vigor (naturaleza, Vigormax) o plantas por senal (ciudad: gate
  ligado = Plantasligado plantas).
  Si no se ve la piel: Materialrespaldo (Phong).
  Prueba: Sembrar con Velprueba 10 y 120, y con Gateprueba 0,25, 1 y 2.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Avance', 'Velprueba', 'Nota', 'Nota2', 'Materialmodo', 'Gateprueba',
               'Materialrespaldo'):
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


def _prueba(t, m):
    c = m.cfg()
    # 1. una geometria por modelo, con la rugosidad en el canal a y el shader de su familia
    geos = m.geometrias_piel(c)
    dobles = [o.name for o in base.children if o.name.startswith('mod_')
              and (o.name.endswith('_pul') or o.name.endswith('_por'))]
    t.check('una geometria por modelo (%d), sin las pulidas y porosas de la fase 11' % len(geos),
            len(geos) == len(m.MODELOS) and all(base.op(g) is not None for g, _, _ in geos) and not dobles,
            '%d duplicadas' % len(dobles))
    malas = []
    for g, mo, mat in geos:
        geo = base.op(g)
        if mo.startswith('ciu_'):
            continue
        try:
            alfa = str(geo.par.instancea.eval())
        except Exception:
            alfa = '?'
        if alfa != 'a' or str(geo.par.material.eval()) != mat:
            malas.append('%s (a=%s, %s)' % (g, alfa, geo.par.material.eval()))
    t.check('cada geometria lee la rugosidad (canal a) y usa el shader de su familia',
            not malas, ', '.join(malas[:3]))
    sh = base.op('piel_vertex'), base.op('piel_pixel')
    mats = [base.op('mat_piel_' + f) for f in FAMILIAS_PIEL]
    t.check('shader de la piel: piel_vertex, piel_pixel y un GLSL MAT por familia',
            sh[0] is not None and sh[1] is not None and sh[0].text == PIEL_VERTEX
            and sh[1].text == PIEL_PIXEL and all(x is not None for x in mats)
            and all(str(x.par.vec0name.eval()) == 'uFamilia' for x in mats if x is not None))
    malos = []
    for x in mats:
        for q in range(len(PIEL_UNIFORMES)):
            for comp in 'xyzw':
                p = getattr(x.par, 'vec%dvalue%s' % (q, comp), None) if x is not None else None
                try:
                    float(p.eval())
                except Exception as e:
                    malos.append('%s.vec%dvalue%s: %s' % (x.name if x is not None else '?', q, comp, e))
    col = [m.luz_color(nm, k) for nm in ('luz_principal', 'luz_relleno') for k in range(3)]
    t.check('los uniformes del shader (luces, familia) se evaluan sin error',
            not malos and all(v > 0 for v in col), '; '.join(malos[:2]) or
            'color x dimmer %s' % ' '.join('%.2f' % v for v in col))
    # 2. velocidad -> material: Sembrar con Velprueba 10 y 120 (por el camino real)
    nota = int(base.par.Nota)
    i = m.note_cell(nota)
    base.par.Tema = 'naturaleza'
    base.par.Gateprueba = 0.5

    def sembrar(vel, n, gate=0.5, pulso='Sembrar'):
        m.reset_world()
        base.par.Velprueba = vel
        base.par.Gateprueba = gate
        now = absTime.seconds
        paso = m.step_dur(m.cfg(), m.tempo())
        for k in range(n):
            m.on_pulse(pulso)
            m.tick(m.world(), m.cfg(), now + (k + 1) * (gate + 0.5) * paso, m.tempo(), True)
        W = m.world()
        W['vh'] = list(W['h'])
        inst = m.build_instances(W, m.cfg(), now + 100.0)
        principal = None
        for g, filas in inst.items():
            for f in filas:
                if g.startswith('mod_') and abs(sum(f[q] * m.normal_i(i)[q] for q in range(3))
                                                - m.base_radius(W, m.cfg(), i)) < 1e-6:
                    principal = principal or f
        return W, inst, principal
    base.par.Materialmodo = 'continuo'
    _, inst10, f10 = sembrar(10, 6)
    _, inst120, f120 = sembrar(120, 6)
    c = m.cfg()
    luma = lambda f: f[9] + f[10] + f[11]
    t.check('velocidad 10: rugosa (pomez); 120: pulida (obsidiana)',
            f10 and f120 and abs(f10[12] - m.rugosidad(c, 10)) < 1e-9 and abs(f120[12] - m.rugosidad(c, 120)) < 1e-9
            and f10[12] > 0.7 > 0.15 > f120[12] and luma(f10) > luma(f120) + 0.5,
            'rugosidad %.2f y %.2f' % (f10[12] if f10 else -1, f120[12] if f120 else -1))
    base.par.Materialmodo = 'binario'
    cb = m.cfg()
    t.check('Materialmodo binario: Rugmax por debajo de Umbralvel, Rugmin desde ahi',
            m.rugosidad(cb, cb['vel_umbral'] - 1) == cb['rug_max'] and m.rugosidad(cb, cb['vel_umbral']) == cb['rug_min'])
    base.par.Materialmodo = 'continuo'
    canal = all(len(f) == 13 for g, fs in inst10.items() if g.startswith('mod_') for f in fs)
    t.check('las filas de los modelos traen el canal a', canal and any(g.startswith('mod_') and fs
                                                                       for g, fs in inst10.items()))
    # 3. gate -> vigor (naturaleza): Gateprueba 0,25, 1 y 2
    vig, ancho = [], []
    for g in (0.25, 1.0, 2.0):
        W, _, f = sembrar(100, 6, g)
        vig.append(W['vig'][i])
        ancho.append(f[6] if f else 0.0)
    t.check('naturaleza: Gateprueba 0,25 / 1 / 2 -> vigor y anchura crecientes',
            vig[0] < 1.0 < vig[1] < vig[2] + 1e-9 and ancho[0] < ancho[1] <= ancho[2] + 1e-9,
            'vigor %s, ancho %s' % (' '.join('%.2f' % v for v in vig), ' '.join('%.2f' % a for a in ancho)))
    # 4. gate -> plantas (ciudad): un gate ligado construye Plantasligado plantas
    base.par.Tema = 'ciudad'
    base.par.Nota2 = nota
    W1, _, _ = sembrar(100, 8, 0.5, 'Sembrar2')
    o1 = (W1['occ'][i], W1['carga'][i])
    W2, _, _ = sembrar(100, 8, 2.0, 'Sembrar2')
    o2 = (W2['occ'][i], W2['carga'][i])
    efecto = W2['ev'].get('mod', {}).get('efecto', '')
    t.check('ciudad: gate ligado -> %d plantas por senal' % m.cfg()['plantas_ligado'],
            o2 > o1 and efecto == '%d plantas' % m.cfg()['plantas_ligado'],
            'ocupacion y carga %s -> %s, %s' % (o1, o2, efecto))
    base.par.Tema = 'naturaleza'
    # 5. la velocidad sigue sembrando el caos de la fase 11
    c = m.cfg()
    t.check('la velocidad sigue sembrando el caos (100 y 101 dan compuestos distintos)',
            m.compuesto(c, m.GEO, 100, i, 6) != m.compuesto(c, m.GEO, 101, i, 6))
    # 6. Materialrespaldo: Phong y alfa 1, en vivo
    base.par.Materialrespaldo = True
    _, instr, fr = sembrar(10, 6)
    g0 = next(g for g, mo, _ in geos if not mo.startswith('ciu_'))
    t.check('Materialrespaldo: todas las geometrias a mat_respaldo (Phong), alfa 1',
            str(base.op(g0).par.material.eval()) == 'mat_respaldo' and fr and fr[12] == 1.0)
    base.par.Materialrespaldo = False
    t.check('sin respaldo vuelve el shader', str(base.op(g0).par.material.eval()).startswith('mat_piel_'))
    # 7. por el camino real: el Script CHOP con su canal a, y la leyenda
    W, inst, _ = sembrar(97, 6, 1.6)
    m._CACHE['inst'] = inst
    llenas = [g for g, f in inst.items() if g.startswith('mod_') and f and len(f[0]) == 13]
    chop = base.op('i_' + llenas[0]) if llenas else None
    if chop is not None:
        chop.cook(force=True)
    t.check('i_mod_...: el Script CHOP tiene el canal a (rugosidad)',
            chop is not None and chop['a'] is not None and abs(chop['a'][0] - m.rugosidad(m.cfg(), 97)) < 1e-6)
    leg = m.legend()
    t.check('leyenda MOD: velocidad -> rugosidad, gate -> efecto',
            'MOD' in leg and 'rugosidad 0.24' in leg and 'gate 1.60' in leg, [l for l in leg.split('\n')
                                                                             if 'MOD' in l][0].strip()
            if 'MOD' in leg else '')


run_test(base, prueba)
print('  Ahora: Sembrar con Velprueba 10 y luego 120 (pagina Fase3, tras')
print('  Resetmundo): pomez y obsidiana. Cambia Gateprueba (0,25, 1, 2) y mira')
print('  el vigor de los arboles; en la ciudad, Gateprueba 2 sube 2 plantas.')
print('  Si los modelos se ven negros o no se ven: Materialrespaldo y pegame')
print('  los errores de mat_piel_mineral (clic derecho > Info).')
print('=' * 66)
