"""
=============================================================================
ESTRATOS - FASE 9: ARQUEOLOGIA (CORTES PROFUNDOS Y ESTRATIGRAFIA)
=============================================================================
Requiere la fase 8.

QUE HACE
--------
Los pads con profundidad > 0 (por defecto el 2, caja, y el 3, tom) abren un CORTE: quitan
las losetas de las conchas superiores en la celda golpeada, en forma de
anfiteatro (profundidad completa en el centro, un escalon menos por
anillo). Las paredes del corte son las capas enterradas, cada una con el
color de su generacion: bandas que son la historia cromatica de la sesion.

  CICATRIZ   lo recien expuesto (fondo y paredes) se ve CIAN y se integra
             al mineral en Cicatriz segundos. El hueco es permanente: solo
             lo tapa la concha siguiente.
  DESTELLO   cada destruccion dispara un golpe de luz sobre la celda;
             los cortes, mas fuerte. Del color del pad (aclarado).
  LUZ SEQ1   el cian queda reservado a lo recien expuesto: la luz del
             SEQ1 en el centro de la celda pasa a blanca.

Las formaciones de una celda cortada se apoyan en el fondo del corte.
La profundidad se mide en conchas: como cada concha tiene el grosor de su
ciclo (fase 8), un corte de 3 conchas es mas o menos hondo segun lo que
duraron esos mundos. Las paredes usan los radios de cada concha.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase9_arqueologia.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase9 v5  (cortes, estratigrafia con grosores, cicatriz cian, destello)'
banner(VERSION)

base = require_base(9)
motor = install_core(base, CARPETA, 9)

page = get_page(base, 'Fase9')
add_par(base, page, 'float', 'Cicatriz', 'Duracion de la cicatriz (s)', 4.0, 0.2, 20.0)
add_par(base, page, 'float', 'Destello', 'Intensidad del destello', 3.0, 0.0, 10.0)
ok('pagina Fase9: Cicatriz (4 s), Destello (3)')

luz = get_or_make(base, 'lightCOMP', 'luz_destello', 260, -580)
setmenu(luz, ['lighttype'], ['point'], 0)
for k, ax in enumerate(('tx', 'ty', 'tz')):
    setexpr(luz, ax, "parent().op('motor').module.flash_value(%d, absTime.frame)" % k)
setexpr(luz, 'dimmer', "parent().op('motor').module.flash_value(3, absTime.frame)")
for k, ch in enumerate(('lightcolorr', 'lightcolorg', 'lightcolorb')):
    if not setexpr(luz, ch, "parent().op('motor').module.flash_value(%d, absTime.frame)" % (4 + k)):
        setp(luz, ch, (0.80, 0.95, 1.00)[k])
ok('luz_destello: golpe de luz sobre cada destruccion, del color de su pad, sigue el giro')

ok('luz del SEQ1: blanca desde esta fase (el cian queda para lo recien expuesto)')
set_render(base)

leeme(base, 9, """FASE 9 - ARQUEOLOGIA
  Pads con profundidad > 0 abren cortes en anfiteatro: las paredes son
  las conchas enterradas, cada una con su color.
  Lo recien expuesto, cian durante Cicatriz s. Cada destruccion, destello.
  La luz del SEQ1 en el centro de la celda pasa a blanca.""")

print_report()


def prueba(t):
    m = t.m
    c = m.cfg()
    W = m.new_world()
    for g in range(5):
        m.note_on(W, c, 1, 64, 100, g)
        m.end_cycle(W, c, g + 0.5)
    i = m.note_cell(64)
    d = m.cut(W, c, i, 3, 1, 100.0)
    t.check('corte de 3 en 5 conchas', d == 3 and W['hueco'][i] == 3)
    ring = [x for x, dd in m.rings(i, 1) if dd == 1]
    t.check('anfiteatro: el anillo baja un escalon menos',
            all(W['hueco'][x] == 2 for x in ring))
    t.check('cicatrices registradas', len(W['scars']) > 0, '%d losetas' % len(W['scars']))
    tiles = m.build_tiles(W, c, 100.0)
    cian = [r for r in tiles if r[9] < 0.3 and r[11] > 0.8]
    t.check('lo recien expuesto se dibuja cian', len(cian) > 0, '%d' % len(cian))
    later = m.build_tiles(W, c, 100.0 + c['scar_time'] + 1)
    cian2 = [r for r in later if r[9] < 0.3 and r[11] > 0.8]
    t.check('la cicatriz se integra con el tiempo', len(cian2) == 0)
    t.check('la formacion se apoya en el fondo',
            abs(m.base_radius(W, c, i) - (m.top_radius(W, c) - 3 * c['shell_thick'])) < 1e-6)
    # conchas de grosores distintos
    cg = dict(c)
    cg['grosor_tiempo'] = 1
    cmin, cmax = m.cycle_bounds(cg)
    W3 = m.new_world()
    for bars in (cmin, 2 * cmin, cmin // 2 or 1, cmax, cmin):
        m.end_cycle(W3, cg, 0.0, bars)
    gs = [m.shell_th(sh, cg) for sh in W3['shells']]
    m.cut(W3, cg, i, 3, 0, 100.0)
    t.check('corte con grosores distintos: el fondo baja la suma de 3 conchas',
            abs(m.base_radius(W3, cg, i) - (m.top_radius(W3, cg) - sum(gs[-3:]))) < 1e-6,
            'grosores %s' % ' '.join('%.2f' % g for g in gs))
    radii = m.shell_radii(W3, cg)
    rr = [((x[0] ** 2 + x[1] ** 2 + x[2] ** 2) ** 0.5, x[7]) for x in m.build_tiles(W3, cg, 100.0)]
    rad_ok = all(any(abs(a - r_in) < 1e-6 and abs(b - 0.98 * (r_out - r_in)) < 1e-6 for a, b in rr)
                 for r_in, r_out in radii)
    t.check('las paredes usan el radio y el grosor de cada concha', rad_ok)
    # pad profundo por el camino real
    m.reset_world()
    Wr = m.world()
    cr = m.cfg()
    for g in range(3):
        m.note_on(Wr, cr, 1, 64, 100, g)
        m.end_cycle(Wr, cr, g + 0.5)
    t.midi(0x9C, 0x40, 0x64)
    chd = int(base.par.Canaldrum)
    nb = int(base.par.Notabase)
    cortes = m.pads_corte(cr)                            # por defecto, caja y tom
    hondo = max(cortes, key=lambda k: cr['perfiles'][k][2]) if cortes else 0
    t.midi(0x90 + chd - 1, nb + hondo, 0x64)
    ev = Wr['ev'].get('erosion', {})
    t.check('pad %d por MIDI abre un corte' % (hondo + 1), ev.get('corte', 0) >= 1,
            str(ev.get('corte')))
    t.check('destello encendido', Wr['flash'] is not None)
    t.check('leyenda CORTE', 'CORTE' in m.legend())
    c9 = dict(m.cfg())
    c9['nivel'] = max(9, c9['nivel'])
    W9 = m.new_world()
    m.note_on(W9, c9, m.GEO, 64, 100, 1.0)
    f9 = m.cell_lights(W9, c9, 1.0)
    t.check('la luz del SEQ1 es blanca desde la fase 9',
            f9 and tuple(round(x, 3) for x in f9[0][9:12])
            == tuple(round(x, 3) for x in m.COL_SEQ1_BLANCO))


run_test(base, prueba)
print('  Ahora: con varias conchas ya enterradas, golpea la caja (pad 2) y el')
print('  tom (pad 3).')
print('  El corte deja ver las capas; el cian se apaga en Cicatriz segundos.')
print('=' * 66)
