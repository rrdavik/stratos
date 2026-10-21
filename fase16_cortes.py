"""
=============================================================================
ESTRATOS - FASE 16: ARQUEOLOGIA TEMATICA (CORTES)
=============================================================================
Requiere la fase 15. Los cortes de la fase 9 dejan de ensenar solo bandas
de color: ensenan lo que habia en cada concha, leido de su registro (fase
15).

QUE HACE
--------
  CORTES       los pads cuyo perfil tiene profundidad (con los perfiles por
               defecto, bombo, caja y tom: pads 1-3; el plan decia 6-8). Si
               cambias los perfiles, cambian con ellos.
  NATURALEZA   sima: en la veta de carbon, troncos fosiles aplastados en
               horizontal (donde hubo bosque) y columnas de basalto (donde
               hubo relieve).
  CIUDAD       excavacion: cimientos (ciudad informal), sotanos (planificada)
               y tramos de calle con su colector (donde pasaban carreteras).
  DONDE        solo dentro del corte: en el fondo de cada celda cortada y en
               las paredes de sus vecinas mas altas, como mucho
               Detalleexpuesto piezas por celda, una por era antes de
               repetir. Cada concha ensena lo suyo, sea del tema que sea:
               bajo una ciudad puede salir un bosque fosil.
  CICATRIZ     el cian sigue reservado a lo recien expuesto, en los dos
               temas: piezas y losetas.
  ESCALADA     dos cortes en la misma vecindad (el objetivo del segundo
               dentro del primero o en su borde) dentro de Ventanaescalada
               pasos (pagina Fase14) se unen por el camino mas corto
               (Unircortes). Naturaleza: un canon, el camino cortado con la
               profundidad del menor. Ciudad: una galeria de metro a cielo
               abierto, una zanja de una loseta con la boveda dentro. La
               galeria se entierra con su mundo; el canon queda.
  LEYENDA      CORTE  celda 41   3 eras expuestas: carbon, ruinas, carbon

PROBAR SIN BEATSTEP
-------------------
  Cinco Forzarciclo alternando Tema (con Temaenciclo el cambio espera al
  fin de ciclo), con Sembrarzona y Sembrarzona2 antes de cada uno. Despues,
  Padprueba en un pad que corte (2, la caja) y Erosionar. Unirprueba da dos
  cortes vecinos seguidos alrededor de Nota: canon o galeria.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase16_cortes.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase16 v1  (arqueologia tematica: lo que ensenan los cortes, canon y galeria de metro)'
banner(VERSION)

base = require_base(16)
motor = install_core(base, CARPETA, 16)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase16)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase16')
add_par(base, page, 'int', 'Detalleexpuesto', 'Piezas expuestas por celda del corte', 6, 0, 24, clamp=True)
add_par(base, page, 'toggle', 'Unircortes', 'Dos cortes vecinos seguidos se unen (canon o galeria)', True)
add_par(base, page, 'pulse', 'Unirprueba', 'Dos cortes vecinos seguidos alrededor de Nota')
ok('pagina Fase16: Detalleexpuesto 6, Unircortes, Unirprueba')

# -----------------------------------------------------------------------------
# CATALOGO Y MODELOS: troncos fosiles, basalto, cimientos, sotano, calle y
# galeria de metro
# -----------------------------------------------------------------------------

n_cat = catalogo_al_dia(base, m)
if n_cat is not None:
    ok('catalogo: %d filas, con lo expuesto de cada especie (pared y fondo) y la galeria' % n_cat)
else:
    info('catalogo editado a mano: se conserva; lo expuesto sale de las filas por defecto')
modelos, n_nuevos, n_piezas, ajustadas = construir_modelos(base, m, solo_nuevos=True)
ok('modelos: %d nuevos (%d piezas) en %s' % (n_nuevos, n_piezas, modelos.path))
instanciar_modelos(base, m)
set_render(base)

leeme(base, 16, """FASE 16 - ARQUEOLOGIA TEMATICA: CORTES
  Los cortes (pads con profundidad) ensenan lo que hubo en cada concha:
  naturaleza, troncos fosiles en la veta de carbon y columnas de basalto;
  ciudad, cimientos, sotanos y tramos de calle. En el fondo y en las paredes
  del corte, hasta Detalleexpuesto piezas por celda, una por era.
  Lo recien expuesto, cian. Dos cortes vecinos en Ventanaescalada pasos se
  unen (Unircortes): canon en naturaleza, galeria de metro en la ciudad.
  Prueba: cinco Forzarciclo alternando Tema; Padprueba 2 y Erosionar;
  Unirprueba.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Padprueba', 'Temaenciclo', 'Herencia', 'Detalleexpuesto',
               'Unircortes', 'Ventanaescalada', 'Grosortiempo', 'Colmatacion', 'Cortezamax', 'Avance'):
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
    import math
    base.par.Velprueba = 100
    base.par.Temaenciclo = True
    base.par.Herencia = 0.25
    base.par.Detalleexpuesto = 6
    base.par.Unircortes = True
    base.par.Ventanaescalada = 8
    base.par.Grosortiempo = False               # conchas de Shellthick: paredes que se ven
    base.par.Colmatacion = 0.0
    c = m.cfg()
    cortes = m.pads_corte(c)
    t.check('cortes: los pads con profundidad (%s)' % ' '.join(str(k + 1) for k in cortes), bool(cortes))
    if not cortes:
        return
    pad = max(cortes, key=lambda k: c['perfiles'][k][2])       # el mas hondo
    base.par.Padprueba = pad + 1

    def zona(pulso, nota, veces=3):
        base.par.Nota = nota
        base.par.Nota2 = nota
        for _ in range(veces):
            m.on_pulse(pulso)

    # 1. cinco eras alternando el tema, con bosque, relieve y ciudad
    base.par.Tema = 'naturaleza'
    m.reset_world()
    m.world()['tema'] = 0
    for g in range(5):
        zona('Sembrarzona', 64)
        zona('Sembrarzona2', 52)
        base.par.Tema = 'ciudad' if g % 2 == 0 else 'naturaleza'    # espera al fin de ciclo
        m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    temas = [sh.get('tema') for sh in W['shells']]
    t.check('cinco eras alternando el tema', temas == ['naturaleza', 'ciudad'] * 2 + ['naturaleza'],
            ' '.join(str(x) for x in temas))
    # 2. un corte por el camino del pad de prueba: lo expuesto
    i = m.note_cell(64)
    m.world()['last'] = {1: dict(note=64, cell=i, t=absTime.seconds, vel=100)}
    base.par.Tema = 'naturaleza'
    m.on_pulse('Erosionar')
    W, c = m.world(), m.cfg()
    ev = W['ev'].get('corte') or {}
    obj = ev.get('celda', -1)
    now = absTime.seconds
    inst = m.build_instances(W, c, now)
    expuestas = dict((g, filas) for g, filas in inst.items()
                     if g.startswith('mod_fos_') or g.startswith('mod_arq_'))
    n_filas = sum(len(v) for v in expuestas.values())
    en_corte = [x for x in range(m.N) if m.en_corte(W, c, x)]
    t.check('el corte abre %d losetas en la celda %d' % (ev.get('conchas', 0), obj), ev.get('conchas', 0) >= 2)
    zona_c = [x for x, _ in m.rings(obj, c['perfiles'][pad][1] + 1)]
    eras = m.eras_expuestas(W, c, zona_c)
    nombres = [nm for _, nm in eras]
    t.check('el corte ensena varias eras, de los dos temas (%s)' % ', '.join(nombres),
            len(eras) >= 3 and 'carbon' in nombres and 'ruinas' in nombres)
    t.check('piezas expuestas: troncos fosiles, basalto, cimientos o sotanos (%d)' % n_filas,
            n_filas > 0 and any(g.startswith('mod_fos_tronco') for g in expuestas)
            and any(g.startswith('mod_arq_') for g in expuestas),
            ' '.join('%s %d' % (g[4:], len(v)) for g, v in sorted(expuestas.items()) if v))
    # 3. solo dentro del corte: cada pieza, junto a una celda del corte
    R = m.top_radius(W, c)
    dentro = True
    for filas in expuestas.values():
        for f in filas:
            r = math.sqrt(f[0] ** 2 + f[1] ** 2 + f[2] ** 2)
            u = (f[0] / r, f[1] / r, f[2] / r)
            cerca = max(range(m.N), key=lambda x: sum(u[k] * m.normal_i(x)[k] for k in range(3)))
            if r > R + 1e-6 or not (cerca in en_corte or any(j in en_corte for j in m.NEIGH[cerca])):
                dentro = False
    t.check('las piezas solo estan dentro del corte, por debajo de la superficie', dentro)
    # 4. Detalleexpuesto
    por_celda = [len(m.piezas_expuestas(W, c, x)) for x in en_corte]
    base.par.Detalleexpuesto = 2
    c2 = m.cfg()
    por_celda2 = [len(m.piezas_expuestas(W, c2, x)) for x in en_corte]
    base.par.Detalleexpuesto = 0
    c0 = m.cfg()
    vacio = not any(g.startswith('mod_fos_') or g.startswith('mod_arq_')
                    for g, filas in m.build_instances(W, c0, now).items() if filas)
    base.par.Detalleexpuesto = 6
    t.check('Detalleexpuesto: como mucho N piezas por celda (6, 2, 0)',
            max(por_celda) <= 6 and max(por_celda2) <= 2 and vacio and sum(por_celda2) < sum(por_celda),
            '%d -> %d piezas' % (sum(por_celda), sum(por_celda2)))
    s_fondo = [p for x in en_corte for p in m.piezas_expuestas(W, c, x)]
    eras_celda = all(len(set(p[0] for p in m.piezas_expuestas(W, c2, x) if p[2] >= 0))
                     == len([p for p in m.piezas_expuestas(W, c2, x) if p[2] >= 0])
                     or len(set(p[0] for p in m.piezas_expuestas(W, c, x) if p[2] >= 0)) <= 1
                     for x in en_corte)
    t.check('una pieza por era antes de repetir', eras_celda and s_fondo)
    # 5. la cicatriz: lo recien expuesto, cian; despues, su color
    cian = lambda col: col[2] > 0.8 and col[0] < 0.4
    recien = [f for filas in expuestas.values() for f in filas if cian(f[9:12])]
    luego = m.build_instances(W, c, now + c['scar_time'] + 1.0)
    luego_cian = [f for g, filas in luego.items() if g.startswith(('mod_fos_', 'mod_arq_'))
                  for f in filas if cian(f[9:12])]
    t.check('cicatriz: lo recien expuesto sale cian y despues toma su color',
            recien and not luego_cian, '%d piezas cian' % len(recien))
    # 6. una concha sin registro (anterior a la fase 15) solo ensena su color
    sin = dict(W['shells'][-1])
    sin.pop('tema', None)
    t.check('una concha sin registro no ensena piezas', m.contenido(sin, obj) is None)
    t.check('leyenda CORTE con las eras expuestas', 'eras expuestas' in m.legend())
    # 7. union de cortes: el mundo de ahora es de ciudad -> galeria de metro
    W['cortes'] = []
    m.on_pulse('Unirprueba')
    W, c = m.world(), m.cfg()
    u = W['ev'].get('union') or {}
    gal = m.build_instances(W, c, absTime.seconds).get('mod_arq_galeria', [])
    t.check('dos cortes vecinos en la ciudad: galeria de metro (%d tramos)' % len(gal),
            m.tema_de(c) == 'ciudad' and u.get('tipo') == 'galeria' and gal
            and W['arqueo'].get('galerias', 0) == len(gal), '-'.join(str(x) for x in u.get('celdas', [])))
    t.check('leyenda CORTE con la union', 'galeria de metro' in m.legend())
    # 8. el fin de ciclo entierra la galeria; en naturaleza, canon
    base.par.Tema = 'naturaleza'
    m.on_pulse('Forzarciclo')
    W = m.world()
    t.check('el fin de ciclo entierra las uniones', not W['uniones'])
    W['cortes'] = []
    base.par.Nota = 70
    m.on_pulse('Unirprueba')
    W, c = m.world(), m.cfg()
    u = W['ev'].get('union') or {}
    t.check('dos cortes vecinos en naturaleza: canon por el camino mas corto',
            m.tema_de(c) == 'naturaleza' and u.get('tipo') == 'canon' and len(u.get('celdas', [])) >= 2
            and all(m.en_corte(W, c, x) for x in u['celdas'])
            and not m.build_instances(W, c, absTime.seconds).get('mod_arq_galeria'),
            '-'.join(str(x) for x in u.get('celdas', [])))
    # 9. sin Unircortes, o fuera de Ventanaescalada, no se unen
    base.par.Unircortes = False
    W['cortes'] = []
    n_u = len(W['uniones'])
    base.par.Nota = 76
    m.on_pulse('Unirprueba')
    t.check('Unircortes apagado: los cortes no se unen', len(m.world()['uniones']) == n_u)
    base.par.Unircortes = True
    W, c = m.world(), m.cfg()
    a = m.note_cell(64)
    b = [x for x, d in m.rings(a, 2) if d == 2][0]
    W['cortes'] = [[absTime.seconds - 100.0, a, 2, 1]]
    u = m.unir_cortes(W, c, b, 2, 1, absTime.seconds)
    t.check('pasada Ventanaescalada, no se unen', u is None)


run_test(base, prueba)
print('  Ahora: con varias conchas de temas distintos, golpea la caja (pad 2):')
print('  el corte ensena troncos fosiles, basalto, cimientos y sotanos. Dos')
print('  golpes seguidos en sitios vecinos los unen: canon o galeria de metro.')
print('=' * 66)
