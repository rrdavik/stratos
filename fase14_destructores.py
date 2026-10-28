"""
=============================================================================
ESTRATOS - FASE 14: DESTRUCTORES I (ARANAZOS Y ESCALADA)
=============================================================================
Requiere la fase 13. Los aranazos de la bateria (fase 7) reciben forma
tematica, y la insistencia destructiva escala igual que la constructiva: un
golpe es un accidente; varios golpes en la misma zona, una catastrofe.

QUE HACE
--------
  ARANAZOS     los pads de erosion cuyo perfil no tiene profundidad (con
               los perfiles por defecto, del 4 al 8: la caja corta y, desde
               la fase 7 v12, el bombo y el tom son impulso y no destruyen).
               Los cortes no cambian (su version tematica es la fase 16).
  UN GOLPE     la formacion mas alta de la vecindad del objetivo (el objetivo
               y sus vecinas) baja un estado: rayo que tala el arbol
               (vegetacion), desprendimiento de columnas (relieve), se
               desploma un anadido (informal), caen las plantas altas
               (planificada).
  ESCALADA     Golpesescalada golpes en la misma vecindad dentro de
               Ventanaescalada pasos: incendio que salta por los puentes del
               dosel, derrumbe de la meseta, derrumbe en cadena del barrio o
               demolicion por implosion, con polvo. Cada celda activa pierde
               1 de ocupacion por paso y se apaga sin ocupacion o a los
               Pasosfuego pasos. El salto lo decide el mapa logistico (la
               misma historia da el mismo fuego); nunca sale del cluster;
               como mucho Maxfuego celdas activas a la vez. Con la densidad
               por encima de Umbraldensidad (fase 7) empieza mas grande.
  HUELLA       lo que se vacia deja claro de ceniza, pedregal, escombros o
               solar vallado, hasta que una nota vuelve a construir.
  DERRIBO      una obra a medias que recibe un aranazo recorre su cadena
               hacia atras, hasta que una nota del cluster la retoma.
  PARTICULAS   brasas y ceniza de lo que arde, polvo de los derrumbes; las
               nubes se disipan en Pasospolvo pasos.
  El fin de ciclo lo apaga todo.

PROBAR SIN BEATSTEP
-------------------
  Tema naturaleza: Sembrarzona dos veces y Sembrar en el centro para hacer un
  bosque denso. Padprueba en un pad de aranazo (5) y Escalar: el fuego prende
  y recorre el cluster. O Erosionar dos veces seguidas (en menos de Ventana-
  escalada pasos: un segundo a 120 BPM).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase14_destructores.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase14 v3  (destructores: aranazos tematicos, escalada, incendio y derrumbes; autoprueba con el pad 9)'
banner(VERSION)

base = require_base(14)
motor = install_core(base, CARPETA, 14)
m = motor.module

# -----------------------------------------------------------------------------
# PARAMETROS (pagina Fase14)
# -----------------------------------------------------------------------------

page = get_page(base, 'Fase14')
add_par(base, page, 'int', 'Ventanaescalada', 'Pasos en que se suman los golpes de una zona', 8, 1, 64,
        clamp=True)
add_par(base, page, 'int', 'Golpesescalada', 'Golpes en la misma zona para la catastrofe', 2, 1, 8,
        clamp=True)
add_par(base, page, 'int', 'Pasosfuego', 'Pasos que arde (o se derrumba) cada celda', 6, 1, 32, clamp=True)
add_par(base, page, 'int', 'Maxfuego', 'Celdas que arden (o se derrumban) a la vez', 6, 1, 40, clamp=True)
add_par(base, page, 'int', 'Pasospolvo', 'Pasos en que se disipa el polvo', 8, 1, 64, clamp=True)
add_par(base, page, 'pulse', 'Escalar', 'Escalada de prueba: Golpesescalada aranazos con Padprueba')
ok('pagina Fase14: Ventanaescalada 8, Golpesescalada 2, Pasosfuego 6, Maxfuego 6, Pasospolvo 8, Escalar')

# -----------------------------------------------------------------------------
# CATALOGO Y MODELOS: las huellas (claro de ceniza, pedregal, escombros; el
# solar vallado es la valla de las obras)
# -----------------------------------------------------------------------------

n_cat = catalogo_al_dia(base, m)
if n_cat is not None:
    ok('catalogo: %d filas, con la huella de cada especie' % n_cat)
else:
    info('catalogo editado a mano: se conserva; las huellas salen de las de por defecto')
modelos, n_nuevos, n_piezas, ajustadas = construir_modelos(base, m, solo_nuevos=True)
ok('modelos: %d nuevos (%d piezas) en %s' % (n_nuevos, n_piezas, modelos.path))
instanciar_modelos(base, m)
set_render(base)

leeme(base, 14, """FASE 14 - DESTRUCTORES I: ARANAZOS Y ESCALADA
  Aranazos (pads sin profundidad): la formacion mas alta de la vecindad baja
  un estado (rayo, desprendimiento, anadido, plantas altas).
  Golpesescalada golpes en la misma vecindad en Ventanaescalada pasos:
  incendio por el dosel, derrumbe, derrumbe en cadena o implosion. Pasosfuego,
  Maxfuego; mapa logistico; no sale del cluster. Huellas: ceniza, pedregal,
  escombros, solar vallado. Una obra a medias golpeada se derriba.
  Prueba: bosque denso, Padprueba 5 y Escalar.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

def prueba(t):
    m = t.m
    guarda = {}
    for nm in ('Tema', 'Nota', 'Nota2', 'Velprueba', 'Padprueba', 'Maxfuego', 'Umbraldensidad',
               'Golpesescalada', 'Ventanaescalada', 'Pasosfuego', 'Pasospolvo', 'Avance'):
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
    base.par.Umbraldensidad = 0.95             # sin presupuesto hasta su comprobacion
    c = m.cfg()
    pads = [k for k in range(len(c['perfiles'])) if m.es_aranazo(c, k)]
    t.check('aranazos: los pads de erosion sin profundidad (%s); ni los cortes ni los impulsos'
            % ' '.join(str(k + 1) for k in pads),
            pads and all(k not in m.pads_corte(c) and k not in m.pads_impulso(c) for k in pads)
            and len(pads) + len(m.pads_corte(c)) + len(m.pads_impulso(c)) == len(c['perfiles']))
    pad = pads[0]

    def zona(tema, s, nota, veces=2, centro=0):
        base.par.Tema = tema
        base.par.Nota = nota
        base.par.Nota2 = nota
        for _ in range(veces):
            m.on_pulse('Sembrarzona' if s == m.GEO else 'Sembrarzona2')
        for _ in range(centro):
            m.on_pulse('Sembrar' if s == m.GEO else 'Sembrar2')
        W = m.world()
        W['vh'] = list(W['h'])
        return W, m.cfg()

    def pasos(W, c, k):
        """k pasos de las catastrofes; devuelve la historia de celdas activas."""
        nonlocal now
        hist = []
        for _ in range(k):
            now += W['paso']
            m.tick_destructores(W, c, now)
            hist.append(sorted((x, q) for cat in W['cats'] for x, q in cat['activas'].items()))
        return hist

    # 1. un golpe: el accidente de cada especie
    acc = []
    for tema, s, esp in (('naturaleza', m.GEO, 'vegetacion'), ('naturaleza', m.ARQ, 'relieve'),
                         ('ciudad', m.GEO, 'informal'), ('ciudad', m.ARQ, 'planificada')):
        m.reset_world()
        W, c = zona(tema, s, 64)
        objetivo = m.pick_target(W, c, pad, 100)
        v, e0 = m.victima(W, c, objetivo)
        ev = m.erosion(W, c, pad, 100, now)
        a = ev.get('accidente') or {}
        bien = a.get('tipo') == m.ACCIDENTE[esp] and a.get('celda') == v and \
            (W['occ'][v] == 0 or m.estado_idx(c, W['occ'][v]) < e0) and not ev.get('escalada')
        acc.append('%s %s' % (esp, 'bien' if bien else 'MAL (%s)' % a))
    t.check('un golpe: la mas alta de la vecindad baja un estado (rayo, desprendimiento, anadido, plantas)',
            all(x.endswith('bien') for x in acc), '; '.join(acc))
    # 2. escalada en un bosque denso: el incendio
    def incendio(vel=100):
        nonlocal now
        m.reset_world()
        W, c = zona('naturaleza', m.GEO, 64, veces=4, centro=8)
        cl = m.clusters(W, c)
        occ0 = list(W['occ'])
        ev1 = m.erosion(W, c, pad, vel, now)
        now += W['paso']
        ev2 = m.erosion(W, c, pad, vel, now)
        cat = W['cats'][0] if W['cats'] else None
        zona_ = set(cat['zona']) if cat else set()
        hist, bajadas, dentro, tope = [], True, True, True
        for _ in range(80):
            antes = dict((x, W['occ'][x]) for cat_ in W['cats'] for x in cat_['activas'])
            h = pasos(W, c, 1)[0]
            hist.append(h)
            for x, o in antes.items():
                bajadas = bajadas and W['occ'][x] < o
            dentro = dentro and all(x in zona_ and W['own'][x] in (m.GEO, 0) for x, _ in h)
            tope = tope and len(h) <= c['max_fuego']
            if not W['cats']:
                break
        return W, c, ev1, ev2, cat, cl, occ0, hist, bajadas, dentro, tope
    W, c, ev1, ev2, cat, cl, occ0, hist, bajadas, dentro, tope = incendio()
    ardidas = sorted(set(x for h in hist for x, _ in h))
    t.check('escalada: Golpesescalada aranazos en la misma vecindad -> incendio',
            not ev1.get('escalada') and ev2.get('escalada') == 'incendio' and cat is not None,
            'arden %s' % ardidas)
    t.check('el incendio salta por el cluster (solo vegetacion, nunca fuera) y cada celda pierde 1 por paso',
            len(ardidas) > 1 and dentro and bajadas, '%d celdas, %d pasos' % (len(ardidas), len(hist)))
    t.check('se apaga sin combustible o a los Pasosfuego pasos; Maxfuego celdas a la vez como mucho',
            not W['cats'] and tope and all(q < c['pasos_fuego'] for h in hist for _, q in h))
    vacias = [x for x in ardidas if W['occ'][x] == 0]
    t.check('lo que se vacia deja claro de ceniza (huella) y se dibuja',
            vacias and all(W['ruina'][x] == 1 + m.RUINA_ESP.index('vegetacion') for x in vacias),
            '%d claros' % len(vacias))
    hist2 = incendio()[7]
    hist3 = incendio(vel=113)[7]
    t.check('misma historia, mismo fuego (mapa logistico); otra velocidad, otro fuego',
            hist2 == hist and hist3 != hist)
    # particulas y huella dibujadas
    W, c = m.world(), m.cfg()
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4, centro=8)
    m.erosion(W, c, pad, 100, now)
    m.erosion(W, c, pad, 100, now)
    pasos(W, c, 2)
    inst = m.build_instances(W, c, now)
    brasas = [f for f in inst.get('particulas', []) if abs(f[9] - m.COL_BRASA[0]) < 1e-6
              and abs(f[10] - m.COL_BRASA[1]) < 1e-6]
    t.check('brasas y ceniza mientras arde (particulas del motor)', len(brasas) > 0, '%d brasas' % len(brasas))
    pasos(W, c, 80)
    inst = m.build_instances(W, c, now)
    claros = inst.get(m.geometria_de('veg_claro', False, False), [])
    pasos(W, c, int(c['pasos_polvo']) + 1)
    t.check('la huella se dibuja (mod_veg_claro) y el polvo se disipa en Pasospolvo pasos',
            claros and not W['polvo'], '%d claros' % len(claros))
    x = next((i for i in range(m.N) if W['ruina'][i]), None)
    if x is not None:
        base.par.Nota = m.cell_note(x)
        m.on_pulse('Sembrar')
    t.check('una nota sobre la huella la borra', x is not None and W['ruina'][x] == 0)
    # 3. fuera de la ventana o en otra zona: no escala
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4)
    ev1 = m.erosion(W, c, pad, 100, now)
    ev2 = m.erosion(W, c, pad, 100, now + (c['ventana_escalada'] + 1) * W['paso'])
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4)
    ev3 = m.erosion(W, c, pad, 100, now)
    W, c = zona('naturaleza', m.GEO, 70, veces=4)        # el otro lado del planeta
    ev4 = m.erosion(W, c, pad, 100, now)
    t.check('fuera de Ventanaescalada o en otra zona no escala',
            not ev2.get('escalada') and not ev4.get('escalada') and not W['cats'])
    # 4. Maxfuego
    base.par.Maxfuego = 2
    h = incendio()[7]
    base.par.Maxfuego = 6
    t.check('Maxfuego 2: nunca mas de 2 celdas ardiendo', h and max(len(x) for x in h) <= 2,
            'max %d' % max(len(x) for x in h))
    # 5. presupuesto: por encima de Umbraldensidad empieza mas grande
    base.par.Umbraldensidad = 0.01
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4, centro=8)
    m.erosion(W, c, pad, 100, now)
    m.erosion(W, c, pad, 100, now)
    grande = W['cats'][0] if W['cats'] else {}
    base.par.Umbraldensidad = 0.95
    t.check('presupuesto: con la densidad por encima de Umbraldensidad la catastrofe empieza mas grande',
            grande and grande['grande'] and len(grande['activas']) > 1,
            '%d celdas al empezar' % len(grande.get('activas', {})))
    # 6. las otras especies
    otras = []
    for tema, s, esp in (('naturaleza', m.ARQ, 'relieve'), ('ciudad', m.GEO, 'informal'),
                         ('ciudad', m.ARQ, 'planificada')):
        m.reset_world()
        W, c = zona(tema, s, 64, veces=4)
        m.erosion(W, c, pad, 100, now)
        ev = m.erosion(W, c, pad, 100, now)
        pasos(W, c, 60)
        ruinas = [i for i in range(m.N) if W['ruina'][i] == 1 + m.RUINA_ESP.index(esp)]
        bien = ev.get('escalada') == m.CATASTROFE[esp] and ruinas and not W['cats']
        if esp == 'planificada':                     # de golpe, con polvo
            bien = bien and W['ev']['catastrofe']['tipo'] == 'implosion'
        otras.append('%s: %s, %d huellas' % (esp, ev.get('escalada'), len(ruinas)))
        inst = m.build_instances(W, c, now)
        mo = m.modelos_de(c, tema, esp, 'huella')[0]
        bien = bien and bool(inst.get(m.geometria_de(mo, False, False)))
        otras[-1] += '' if bien else ' MAL'
    t.check('derrumbe (pedregal), derrumbe en cadena (escombros) e implosion (solar vallado)',
            not any(x.endswith('MAL') for x in otras), '; '.join(otras))
    # 7. derribo: una obra a medias que recibe un aranazo va hacia atras
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4)
    cl = m.clusters(W, c)
    k = cl['de'][m.note_cell(64)]
    celdas = cl['celdas'][k] if k >= 0 else []
    for x in celdas:
        W['et_f'][x] = W['ant_et_f'][x] = 2
    m.erosion(W, c, pad, 100, now)
    medio = [W['et_f'][x] for x in celdas]
    for q in range(40):
        m.tick_piel(W, c, now + (q + 1) * c['pasos_etapa'] * W['paso'], W['paso'])
    t.check('derribo: la obra a medias retrocede una etapa y sigue hacia atras hasta el principio',
            celdas and all(e == 1 for e in medio) and all(W['et_f'][x] == 0 for x in celdas)
            and not any(W['derribo'][x] for x in celdas), 'etapas %s' % medio)
    # 8. fin de ciclo con un fuego: se apaga todo, sin transitos colgados
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4, centro=8)
    m.erosion(W, c, pad, 100, now)
    m.erosion(W, c, pad, 100, now)
    ardia = bool(W['cats'])
    m.on_pulse('Forzarciclo')
    W, c = m.world(), m.cfg()
    tf, tc = m.objetivos(W, c)
    t.check('Forzarciclo con un incendio: se apaga, sin huellas ni obras colgadas',
            ardia and not W['cats'] and not W['polvo'] and not any(W['ruina'])
            and all(W['et_f'][i] == tf[i] and W['et_c'][i] == tc[i] for i in range(m.N)))
    # 9. por debajo del nivel 14 nada cambia
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4)
    c13 = dict(c, nivel=13)
    ev = m.erosion(W, c13, pad, 100, now)
    ev = m.erosion(W, c13, pad, 100, now)
    t.check('en el nivel 13 un aranazo sigue siendo la erosion de la fase 7',
            'accidente' not in ev and not W['cats'])
    # 10. leyenda
    m.reset_world()
    W, c = zona('naturaleza', m.GEO, 64, veces=4, centro=8)
    m.erosion(W, c, pad, 100, now)
    ley1 = m.legend()
    m.erosion(W, c, pad, 100, now)
    ley2 = m.legend()
    t.check('leyenda: el accidente en EROSION y la catastrofe en ESCALADA',
            ' rayo celda' in ley1 and 'golpes 1/' in ley1 and 'ESCALADA INCENDIO' in ley2)


run_test(base, prueba)
print('  Ahora: Tema naturaleza, Sembrarzona dos veces y Sembrar en el centro;')
print('  Padprueba 5 y Escalar (o Erosionar dos veces seguidas): el fuego prende')
print('  y recorre el cluster, y deja claros de ceniza.')
print('=' * 66)
