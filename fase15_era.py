"""
=============================================================================
ESTRATOS - FASE 15: EL CICLO COMO ERA (ENTIERRO TEMATICO Y HERENCIA)
=============================================================================
Requiere la fase 14. Cada fin de ciclo entierra el mundo con la materia de
su tema, y la herencia rebrota segun su logica. Cambiar de tema entre
ciclos deja bosques fosiles bajo ciudades, o ciudades bajo bosques.

QUE HACE
--------
  ENTIERRO     antes de hornear, los transitos se cierran en su estado
               final (y los fuegos de la fase 14 se apagan). La concha de
               naturaleza es una veta de carbon (negro brillante) donde hubo
               bosque y basalto donde hubo relieve; la de ciudad, hormigon
               gris con la traza de sus calles. Las celdas vacias conservan
               el color de su generacion (fase 8). Las conchas usan el shader
               de la piel: el carbon brilla, el hormigon es mate.
  REGISTRO     cada concha guarda su tema y, por celda, especie, estado y
               cluster; y sus carreteras, calles y rios. Lo leeran los cortes
               de la fase 16.
  HERENCIA     naturaleza: banco de semillas. Lo heredado espera como
               semillas sobre el suelo y brota a saltos (semillas -> brotes),
               o de golpe con una nota en su celda (Rebrote).
               Ciudad: trazas. La red de carreteras nueva prefiere los
               tramos de la ciudad enterrada (Pesotraza).
  TEMA         con Temaenciclo, un cambio de Tema espera al siguiente fin de
               ciclo: cada concha tiene un solo tema.

PROBAR SIN BEATSTEP
-------------------
  Tema naturaleza: Sembrarzona y Sembrarzona2, y Forzarciclo: la concha de
  carbon y basalto. Cambia Tema a ciudad (espera: lo dice la leyenda ERA),
  Sembrarzona en dos zonas y Forzarciclo: la concha de hormigon con sus
  calles. Quedan dos conchas de temas distintos.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase15_era.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase15 v2  (el ciclo como era: entierro tematico, registro y herencia)'
banner(VERSION)

base = require_base(15)
motor = install_core(base, CARPETA, 15)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase15)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase15')
add_par(base, page, 'float', 'Pesotraza', 'Preferencia de las carreteras por las trazas heredadas', 0.5,
        0.0, 1.0, clamp=True)
add_par(base, page, 'toggle', 'Rebrote', 'Lo heredado en naturaleza brota de un banco de semillas', True)
add_par(base, page, 'toggle', 'Temaenciclo', 'Un cambio de Tema espera al fin de ciclo', True)
ok('pagina Fase15: Pesotraza 0,5, Rebrote, Temaenciclo')

# las conchas, con el shader de la piel (lo hace install_core; aqui se comprueba)
if not conchas_al_dia(base, m):
    info('conchas: sin el shader de la piel (falta estratos o mat_piel_mineral: relanza la fase 8 y la 12)')
set_render(base)

leeme(base, 15, """FASE 15 - EL CICLO COMO ERA
  Entierro: carbon (bosque) y basalto (relieve) en naturaleza; hormigon con
  la traza de sus calles en la ciudad. Registro por concha: tema, especie,
  estado, cluster, carreteras, calles y rios.
  Herencia: banco de semillas que rebrota (naturaleza, Rebrote); trazas que
  prefieren las carreteras nuevas (ciudad, Pesotraza).
  Temaenciclo: un cambio de Tema espera al fin de ciclo.
  Prueba: naturaleza, Forzarciclo; Tema ciudad, Forzarciclo.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Pesotraza', 'Rebrote', 'Temaenciclo', 'Materialrespaldo',
               'Herencia'):
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
    now = absTime.seconds
    base.par.Velprueba = 100
    base.par.Temaenciclo = True
    base.par.Rebrote = True
    base.par.Herencia = 0.5                     # que algo se herede, sea cual sea la del proyecto

    def tema_mundo(nombre):
        """Mundo vacio con ese tema (el parametro y el del mundo)."""
        base.par.Tema = nombre
        m.reset_world()
        m.world()['tema'] = m.TEMAS.index(nombre)

    def zona(pulso, nota, veces=3):
        base.par.Nota = nota
        base.par.Nota2 = nota
        for _ in range(veces):
            m.on_pulse(pulso)

    def bosque_heredable():
        """Un bosque con una cumbre: algo pasa la herencia (25 %)."""
        zona('Sembrarzona', 64, 4)
        for _ in range(12):
            m.on_pulse('Sembrar')

    # 1. Temaenciclo: el cambio de Tema espera al fin de ciclo
    tema_mundo('naturaleza')
    zona('Sembrarzona', 64)
    zona('Sembrarzona2', 40)
    base.par.Tema = 'ciudad'
    c = m.cfg()
    espera = m.tema_de(c) == 'naturaleza' and m.TEMAS[c.get('tema_pendiente', -1)] == 'ciudad' \
        and 'ciudad en el proximo ciclo' in m.legend()
    W = m.world()
    occ0, own0 = list(W['occ']), list(W['own'])
    cl0 = m.clusters(W, c)
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    t.check('Temaenciclo: un cambio de Tema espera al fin de ciclo; despues manda el nuevo',
            espera and m.tema_de(c) == 'ciudad' and 'tema_pendiente' not in c)
    sh = W['shells'][-1]
    # 2. el registro de la concha
    reg = sh.get('tema') == 'naturaleza' and all(
        (sh['esp'][i] > 0) == (occ0[i] > 0 and own0[i] > 0) for i in range(m.N)) and all(
        sh['cluster'][i] == cl0['de'][i] for i in range(m.N) if occ0[i] > 0) and all(
        sh['estado'][i] == m.estado_idx(c, occ0[i]) for i in range(m.N) if occ0[i] > 0)
    t.check('registro: cada concha guarda tema y, por celda, especie, estado y cluster',
            reg and 'vias' in sh and 'calles' in sh and 'rios' in sh)
    # 3. la materia de la concha de naturaleza
    bosque = [i for i in range(m.N) if sh['esp'][i] == 1 + m.RUINA_ESP.index('vegetacion')]
    relieve = [i for i in range(m.N) if sh['esp'][i] == 1 + m.RUINA_ESP.index('relieve')]
    vacia = next(i for i in range(m.N) if sh['esp'][i] == 0)
    s_ = len(W['shells']) - 1
    luma = lambda col: col[0] + col[1] + col[2]
    cb, rb = m.tile_material(c, sh, s_, bosque[0])
    cr, rr = m.tile_material(c, sh, s_, relieve[0])
    cv, rv = m.tile_material(c, sh, s_, vacia)
    t.check('naturaleza: carbon brillante donde hubo bosque, basalto donde hubo relieve; '
            'lo vacio conserva el color de su generacion',
            luma(cb) < 0.5 and rb < 0.15 and luma(cb) < luma(cr) and rr > rb
            and cv == m.tile_color(c, sh, 0, s_), 'carbon %.2f, basalto %.2f' % (luma(cb), luma(cr)))
    # 4. herencia en la ciudad: nada que rebrote; trazas solo de una ciudad
    t.check('del bosque a la ciudad: sin semillas ni trazas', not any(W['rebrote']) and not W['trazas'])
    # 5. la concha de ciudad, con sus calles
    zona('Sembrarzona', 64, 2)
    zona('Sembrarzona', 70, 2)
    vias = list(m.tejido(m.world(), m.cfg())['vias'])
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    sh = W['shells'][-1]
    s_ = len(W['shells']) - 1
    calle = sh['calles'][0] if sh['calles'] else None
    ccalle = m.tile_material(c, sh, s_, calle)[0] if calle is not None else (1, 1, 1)
    edificio = next((i for i in range(m.N) if sh['esp'][i] and i not in sh['calles']), None)
    ced, red_ = m.tile_material(c, sh, s_, edificio) if edificio is not None else ((0, 0, 0), 0)
    t.check('ciudad: hormigon gris con la traza de sus calles (mas oscuras)',
            sh['tema'] == 'ciudad' and vias and len(sh['vias']) == len(vias)
            and luma(ccalle) < luma(ced) and red_ > 0.6,
            '%d tramos, calle %.2f, hormigon %.2f' % (len(vias), luma(ccalle), luma(ced)))
    t.check('dos conchas de temas distintos (bosque fosil bajo la ciudad)',
            [x.get('tema') for x in W['shells'][-2:]] == ['naturaleza', 'ciudad'])
    # 6. trazas: la red nueva prefiere los tramos de la ciudad enterrada
    trazas = set((a, b) for a, b in W['trazas'])
    t.check('de la ciudad a la ciudad: las trazas son sus carreteras',
            trazas == set((min(a, b), max(a, b)) for a, b in vias))
    a, b = m.note_cell(64), m.note_cell(70)
    corto = m.camino_corto(a, b)
    rodeo = None                                  # otro camino, sin celdas del corto, un tramo mas largo
    for j in sorted(m.NEIGH[a]):
        if j in corto:
            continue
        p = m.camino_corto(j, b)
        if p and len(p) == len(corto) and not set(p[:-1]) & set(corto):
            rodeo = [a] + p
            break
    tz = frozenset((min(x, y), max(x, y)) for x, y in zip(rodeo, rodeo[1:])) if rodeo else frozenset()
    p5, _ = m.camino_traza(a, b, tz, 0.5)
    p0, _ = m.camino_traza(a, b, tz, 0.0)
    t.check('Pesotraza: el camino sigue la traza aunque sea un tramo mas largo (0 = el mas corto)',
            rodeo and p5 == rodeo and p0 == corto,
            'corto %d, traza %d tramos' % (len(corto) - 1, len(rodeo or []) - 1))
    # 7. naturaleza: banco de semillas
    base.par.Tema = 'naturaleza'                  # espera al fin de ciclo
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    tema_mundo('naturaleza')
    bosque_heredable()
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    semillas = [i for i in range(m.N) if W['rebrote'][i] == 1]
    W['vh'] = list(W['h'])
    inst = m.build_instances(W, c, now)
    dibujadas = set()
    for g, filas in inst.items():
        if g.startswith('mod_'):
            for f in filas:
                for i in semillas:
                    nn = m.normal_i(i)
                    r = (f[0] ** 2 + f[1] ** 2 + f[2] ** 2) ** 0.5
                    if r > 0 and sum(f[q] / r * nn[q] for q in range(3)) > 0.999:
                        dibujadas.add(i)
    granos = [f for f in inst.get('particulas', []) if abs(f[9] - m.COL_SEMILLA[0]) < 1e-6]
    t.check('naturaleza: lo heredado espera como banco de semillas (sin modelo, con semillas)',
            semillas and not dibujadas and len(granos) >= len(semillas),
            '%d celdas, %d semillas' % (len(semillas), len(granos)))
    dur = m.rebrote_dur(c, W['paso'])
    m.tick_rebrote(W, c, now + dur)
    brotes = all(W['rebrote'][i] == 2 for i in semillas)
    m.tick_rebrote(W, c, now + 2 * dur)
    t.check('la cadena de rebrote: semillas -> brotes -> la formacion',
            brotes and not any(W['rebrote'][i] for i in semillas))
    tema_mundo('naturaleza')
    bosque_heredable()
    m.on_pulse('Forzarciclo')
    W = m.world()
    x = next((i for i in range(m.N) if W['rebrote'][i]), None)
    if x is not None:
        base.par.Nota = m.cell_note(x)
        m.on_pulse('Sembrar')
    t.check('una nota en la celda la hace brotar de golpe', x is not None and W['rebrote'][x] == 0)
    base.par.Rebrote = False
    tema_mundo('naturaleza')
    bosque_heredable()
    m.on_pulse('Forzarciclo')
    t.check('Rebrote apagado: lo heredado brota como antes', not any(m.world()['rebrote']))
    base.par.Rebrote = True
    # 8. las losetas llevan su rugosidad (canal a) y Materialrespaldo la pone a 1
    W, c = m.world(), m.cfg()
    filas = m.build_tiles(W, c, now)
    base.par.Materialrespaldo = True
    filas_r = m.build_tiles(W, m.cfg(), now)
    base.par.Materialrespaldo = False
    t.check('las losetas llevan la rugosidad en el canal a (Materialrespaldo: 1)',
            filas and all(len(f) == 13 for f in filas) and all(f[12] == 1.0 for f in filas_r)
            and min(f[12] for f in filas) < 0.15,
            '%d losetas, columnas %s, rugosidad min %s, con respaldo %s, conchas %s' % (
                len(filas), sorted(set(len(f) for f in filas)),
                round(min(f[12] for f in filas), 2) if filas and len(filas[0]) > 12 else '-',
                sorted(set(round(f[12], 2) for f in filas_r if len(f) > 12)),
                [(x.get('tema'), sum(1 for e in x.get('esp', []) if e)) for x in W['shells']]))
    # 9. Temaenciclo apagado: el cambio es inmediato
    base.par.Temaenciclo = False
    tema_mundo('naturaleza')
    base.par.Tema = 'ciudad'
    t.check('Temaenciclo apagado: el cambio de Tema es inmediato', m.tema_de(m.cfg()) == 'ciudad')
    base.par.Temaenciclo = True
    t.check('leyenda ERA', 'ERA' in m.legend() and 'herencia' in m.legend())


run_test(base, prueba)
print('  Ahora: Tema naturaleza, siembra y Forzarciclo; cambia Tema a ciudad')
print('  (espera al fin de ciclo), siembra y Forzarciclo: dos conchas de temas')
print('  distintos, carbon y basalto bajo hormigon con sus calles.')
print('=' * 66)
