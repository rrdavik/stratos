"""
=============================================================================
ESTRATOS - FASE 28: LA NOCHE DE ENTERRAMIENTO
=============================================================================
Requiere la fase 27. En cada enterramiento, con colapso o sin el, la esfera
se apaga durante Noche segundos: solo emiten las inclusiones supervivientes
recien horneadas (las motas de la concha nueva) y, cuando exista la fase 29,
las paredes de las escisiones. Mientras tanto la sala esta a oscuras (fase
23, la misma Noche).

QUE HACE
--------
  CUANDO       empieza en el mismo fotograma del recuento (fase 27) y dura
               Noche segundos (4; el parametro lo crea la fase 23). Vuelve en
               0,4 s. Un segundo entierro durante la noche la reinicia.
               Modoactuacion no la quita: es parte del mundo.
  EL MUNDO     nuevo sigue funcionando: lo que nace durante la noche se
               dibuja apagado.
  COMO         sin luces ni geometria nuevas. Un valor 'noche' (0-1) sale del
               motor y llega:
                 - al shader de la piel y de las conchas como uniforme uNoche:
                   todo se multiplica por 1 - noche, y las motas de las
                   losetas recien horneadas suben su emisivo;
                 - a las luces: el color de luz_principal, luz_relleno y
                   luz_destello se multiplica por 1 - noche (lo que dibuja
                   con Phong se apaga con ellas);
                 - a las capas de luz y a las particulas (luz_celda,
                   luz_conchas, luz_local, particulas, humo...): el color de
                   sus instancias, por 1 - noche.
               Nada se recompila ni sale del render.
  LEYENDA      NOCHE    4.0 s   quedan 2.3   emiten 12 inclusiones y 1 escision

No tiene parametros nuevos: usa Noche (fase 23). La pagina Fase28 lleva solo
Version28, de solo lectura.

PROBAR
------
  Con inclusiones vivas (Probllegada 1 y Simponer), Forzarciclo: el planeta
  se apaga 4 s y solo brillan las motas de la concha nueva. Sin inclusiones:
  4 s de oscuridad.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase28_noche.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase28 v1  (noche de enterramiento: la esfera se apaga y emiten las inclusiones horneadas)'
banner(VERSION)

base = require_base(28)
motor = install_core(base, CARPETA, 28)
m = motor.module

pagina_version(base, 28, 'Fase 28 (noche)', VERSION.split('  ')[0])
if not has_par(base, 'Noche'):
    fail('Noche: no esta; aplica antes fase23_sala.py')
if noche_al_dia(base):
    ok('luces: el color de luz_principal, luz_relleno y luz_destello, por 1 - noche')
else:
    fail('luz_relleno: no pude enlazar su color con la noche (Color = <valor> * %s)' % DIA_EXPR)
if 'uNoche' in (base.op('piel_pixel').text if base.op('piel_pixel') is not None else ''):
    ok('shader de la piel: uniforme uNoche (apaga lo mineral; las motas recien horneadas emiten)')
else:
    fail('piel_pixel: sin uNoche (el shader de la piel es de la fase 12)')

set_render(base)

leeme(base, 28, """FASE 28 - LA NOCHE DE ENTERRAMIENTO
  En cada enterramiento, durante Noche s (fase 23), la esfera se apaga:
  solo emiten las motas de las inclusiones recien horneadas (y, desde la
  fase 29, las escisiones). uNoche en el shader de la piel; el color de las
  luces y de las capas de luz, por 1 - noche. El mundo nuevo sigue: lo que
  nace de noche se dibuja apagado. Un segundo entierro la reinicia.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS28 = ('Noche', 'Colapsoon', 'Simbalance', 'Minhuellas', 'Inclusionesmax', 'Temaenciclo', 'Modoactuacion',
          'Nota', 'Velprueba')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS28)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)
        m._CACHE.pop('dia', None)


def _prueba(t, m):
    base.par.Temaenciclo = False
    base.par.Colapsoon = False
    base.par.Noche = 4.0
    reloj = [absTime.seconds + 800.0]
    celdas = [m.note_cell(n) for n in (60, 64, 67)]

    def nuevo():
        m.reset_world()
        m.sala_reset()
        return m.world(), m.cfg()

    def entierra(W, c, motivo='forzado', n_incl=3):
        for i in celdas[:n_incl]:
            m.depositar_inclusion(W, c, i, m.LLEGADA, reloj[0])
        return m.close_cycle(W, c, reloj[0], motivo)

    # 1. lo que dura
    W, c = nuevo()
    antes = m.noche_nivel(W, c, reloj[0])
    entierra(W, c)
    t0 = reloj[0]
    vals = [m.noche_nivel(W, c, t0 + x) for x in (0.0, 0.01, 2.0, 3.99, 4.0, 4.2, 4.41, 6.0)]
    t.check('la noche vale 1 desde el fotograma del recuento hasta Noche (4 s) y 0 despues (vuelve en 0,4 s)',
            antes == 0.0 and vals[:5] == [1.0] * 5 and 0.0 < vals[5] < 1.0 and vals[6] == 0.0 and vals[7] == 0.0
            and W['noche'] == [t0, t0 + 4.0], str(['%.2f' % v for v in vals]))
    t.check('coincide con la oscuridad de sala de la fase 23', W['sala']['noche'] == W['noche'])

    # 2. durante la noche
    u = m.uniformes_piel(W, c, t0 + 1.0)
    sh = W['shells'][-1]
    filas_n = m.build_tiles(W, c, t0 + 1.0)
    emiten = [f for f in filas_n if f[12] >= m.ALFA_RECIENTE]
    W['luz'][celdas[0]] = {0: [t0 + 1.0, 1.0]}
    W['last'][1] = dict(note=60, cell=celdas[0], t=t0 + 1.0, vel=100)
    W['hit_t'][1] = t0 + 1.0
    out = m.build_instances(W, c, t0 + 1.0)
    capas = [k for k in m.NOCHE_CAPAS if out.get(k)]
    apagadas = all(f[9] == f[10] == f[11] == 0.0 for k in capas for f in out[k])
    t.check('durante la noche: uNoche 1, las capas de luz a 0 y las losetas recien horneadas con sus motas '
            'emitiendo (alfa + 100), y solo ellas',
            u['uNoche'][0] == 1.0 and apagadas and 'luz_celda' in capas and not out.get('particulas')
            and len(emiten) == 6 and sh['banda'] == 'humana' and m.emiten_noche(W, c) == (3, 0),
            '%d losetas emiten; capas %s' % (len(emiten), capas))
    W['noche'] = [absTime.seconds - 1.0, absTime.seconds + 3.0]     # las luces leen el reloj de TouchDesigner
    m._CACHE.pop('dia', None)
    if base.op('frame_u') is not None:      # el dimmer de luz_destello sale de frame_u: el de este instante
        base.op('frame_u').cook(force=True)
    luces = [m.luz_color(nm, k) for nm in ('luz_principal', 'luz_relleno', 'luz_destello') for k in range(3)]
    fl = m.flash_light()
    W['noche'] = None
    m._CACHE.pop('dia', None)
    dia_luces = [m.luz_color(nm, k) for nm in ('luz_principal', 'luz_relleno') for k in range(3)]
    W['noche'] = [t0, t0 + 4.0]
    t.check('y las luces a 0 (luz_principal, luz_relleno y luz_destello); de dia, encendidas',
            all(abs(v) < 1e-9 for v in luces) and fl[3] == 0.0 and all(v > 0.01 for v in dia_luces)
            and DIA_EXPR in base.op('luz_relleno').par.cr.expr, 'de noche %s; de dia %s'
            % (['%.2f' % v for v in luces[:6]], ['%.2f' % v for v in dia_luces]))

    # 3. lo que nace de noche se dibuja apagado; al acabar, vuelve
    m.note_on(W, c, m.GEO, 72, 100, t0 + 1.5)
    m.depositar_inclusion(W, c, m.note_cell(72), m.PARADA, t0 + 1.5)
    u2 = m.uniformes_piel(W, c, t0 + 2.0)
    vivo = W['occ'][m.note_cell(72)] == 1 and m.n_inclusiones(W) == 1
    m.tick(W, c, t0 + 4.5, 120.0, False)
    fin = (W['noche'], m.uniformes_piel(W, c, t0 + 4.5)['uNoche'][0],
           [f for f in m.build_tiles(W, c, t0 + 4.5) if f[12] >= m.ALFA_RECIENTE])
    out2 = m.build_instances(W, c, t0 + 4.5)
    t.check('el mundo nuevo sigue funcionando de noche (lo que nace se dibuja apagado); al acabar, la luz vuelve '
            'y las losetas dejan de emitir',
            vivo and u2['uNoche'][0] == 1.0 and fin == (None, 0.0, []) and len(out2['inclusiones']) == 1,
            str(fin[:2]))

    # 4. con colapso y sin el; un segundo entierro; sin inclusiones; Modoactuacion
    W, c = nuevo()
    entierra(W, c, 'colapso')
    d1 = W['noche'][1] - W['noche'][0]
    reloj[0] += 2.0
    entierra(W, c, 'forzado', n_incl=0)
    t.check('con colapso y sin el dura lo mismo; un segundo entierro durante la noche la reinicia',
            abs(d1 - 4.0) < 1e-9 and W['noche'] == [reloj[0], reloj[0] + 4.0]
            and m.noche_nivel(W, c, reloj[0] + 3.5) == 1.0)
    limpias = [f for f in m.build_tiles(W, c, reloj[0] + 1.0) if f[12] >= m.ALFA_RECIENTE]
    t.check('sin inclusiones (concha limpia): Noche s de oscuridad, sin nada que emita',
            W['shells'][-1]['banda'] == 'limpia' and not limpias and m.emiten_noche(W, c) == (0, 0)
            and m.uniformes_piel(W, c, reloj[0] + 1.0)['uNoche'][0] == 1.0)
    if has_par(base, 'Modoactuacion'):
        base.par.Modoactuacion = True
        ca = m.cfg()
        t.check('Modoactuacion no la quita (es parte del mundo)',
                m.noche_nivel(W, ca, reloj[0] + 1.0) == 1.0
                and m.uniformes_piel(W, ca, reloj[0] + 1.0)['uNoche'][0] == 1.0)
        base.par.Modoactuacion = False
    base.par.Noche = 2.0
    W, c = nuevo()
    entierra(W, c)
    t.check('Noche 2: dura 2 s', W['noche'] == [reloj[0], reloj[0] + 2.0])
    base.par.Noche = 4.0

    # 5. la leyenda y la pagina
    W, c = nuevo()
    reloj[0] = absTime.seconds
    entierra(W, c)
    leg = m.legend()
    linea = ' '.join(l.strip() for l in leg.splitlines() if 'NOCHE' in l)
    t.check('leyenda NOCHE', 'NOCHE    4.0 s   quedan 4.0   emiten 3 inclusiones y 0 escisiones' in leg, linea)
    t.check('pagina Fase28: solo Version28, de solo lectura',
            has_par(base, 'Version28') and base.par.Version28.readOnly
            and str(base.par.Version28.eval()).startswith('fase28 v'))


run_test(base, prueba)
print('  Ahora: con inclusiones vivas, Forzarciclo: el planeta se apaga 4 s y solo brillan')
print('  las motas de la concha nueva (leyenda NOCHE).')
print('=' * 66)
