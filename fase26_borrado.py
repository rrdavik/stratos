"""
=============================================================================
ESTRATOS - FASE 26: BORRADO POR EROSION
=============================================================================
Requiere la fase 25. La huella no es para siempre: una inclusion desaparece
cuando la erosion baja su celda por debajo del escalon en que cayo.

QUE HACE
--------
  LA REGLA     una inclusion se borra cuando la ocupacion de su celda queda
               por debajo de su escalon (occ < escalon). Bajar la carga sin
               bajar el escalon no la borra.
  CELDA VACIA  una inclusion que cayo en una celda sin construir (escalon 0)
               la borra cualquier golpe de erosion que alcance la celda:
               cualquier anillo con peso mayor que 0, aunque ese golpe no
               quite una nota entera.
  FUENTES      valen todas: la caja y los aranazos (pads 2 y 4 a 8), el
               microfono (pad 9, y su corte por ruido), los cortes (vacian la
               celda y se llevan todas sus inclusiones), los accidentes y las
               catastrofes de la fase 14 (bajan la ocupacion) y, desde la fase
               29, la escision (es un corte). El bombo y el tom no borran: son
               impulso y suben la ocupacion.
  COMO         sin tocar las reglas de la erosion: un unico punto de purga
               (purgar_inclusiones) que se llama cuando baja la ocupacion de
               una celda; erosion() avisa ademas a cada celda de sus anillos
               (golpe_inclusiones); y una pasada de seguridad por fotograma,
               solo en las celdas con inclusiones.
  CAUSAS       cada borrado suma en su causa: erosion, micro, corte,
               catastrofe (y escision, desde la fase 29).
  LEYENDA      BORRADO  vivas 12   borradas 5 (erosion 2, micro 1, corte 1,
               catastrofe 1)

No tiene operadores nuevos: la geometria de la fase 25 deja de dibujarlas.
No tiene parametros nuevos: la pagina Fase26 lleva solo Version26, de solo
lectura, para mantener una pagina por fase.

PROBAR
------
  Sembrar cuatro veces en una celda (escalon 4), Probllegada 1 y Simponer en
  la casilla que la mira: la inclusion guarda el 4 (leyenda HUELLA). Padprueba
  7 y Erosionar hasta que la leyenda ULTIMA diga ocupacion 3: la inclusion
  desaparece (BORRADO ... erosion 1). En una celda vacia: un solo Erosionar,
  o una Palmada de la sala virtual, la borra.

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/fase26_borrado.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'fase26 v1  (borrado: la erosion borra las inclusiones que quedan sobre su escalon)'
banner(VERSION)

base = require_base(26)
motor = install_core(base, CARPETA, 26)
m = motor.module

pagina_version(base, 26, 'Fase 26 (borrado)', VERSION.split('  ')[0])

set_render(base)

leeme(base, 26, """FASE 26 - BORRADO POR EROSION
  Una inclusion desaparece cuando la erosion baja su celda por debajo de
  su escalon. En una celda sin construir (escalon 0), cualquier golpe de
  erosion que la alcance la borra, en cualquier anillo. Valen la caja, los
  aranazos, el microfono, los cortes y las catastrofes; el bombo y el tom,
  no. Cada borrado suma en su causa (leyenda BORRADO). Sin parametros.""")

print_report()


# -----------------------------------------------------------------------------
# AUTOPRUEBA
# -----------------------------------------------------------------------------

PARS26 = ('Nota', 'Velprueba', 'Objetivo', 'Umbraldensidad', 'Reduccionmic', 'Temaenciclo', 'Tema', 'Probllegada')


def prueba(t):
    m = t.m
    guarda, filas = guardar_sala(base, PARS26)
    try:
        _prueba(t, m)
    finally:
        devolver_sala(base, m, guarda, filas)


def _prueba(t, m):
    base.par.Velprueba = 100
    base.par.Umbraldensidad = 0.95
    base.par.Objetivo = 'seq1'
    base.par.Temaenciclo = False
    base.par.Nota = 64
    reloj = [absTime.seconds + 600.0]
    celda = m.note_cell(64)

    def nuevo():
        m.reset_world()
        m.sala_reset()
        m.mic_reset()
        W, c = m.world(), dict(m.cfg())
        c['nivel'] = 13                 # el golpe solo, sin el accidente de la fase 14...
        return W, c

    def con(c, nivel=26):
        c = dict(c)
        c['nivel'] = nivel              # ...pero con el borrado de la fase 26
        return c

    def sube(W, c, i, occ):
        for _ in range(200):
            if W['occ'][i] >= occ:
                break
            m.note_on(W, c, m.GEO, m.cell_note(i), 100, reloj[0])
        W['last'][1] = dict(note=64, cell=celda, t=reloj[0], vel=100)

    def golpe(W, c, pad, vel=100):
        """Un golpe del pad en 'celda' (velocidad con vel % 3 == 1: sin desplazarse)."""
        return m.erosion(W, c, pad, vel, reloj[0])

    W, c13 = nuevo()
    c = con(c13)
    ara = next(k for k in range(8) if m.es_aranazo(c, k))
    bombo = next(k for k in range(8) if m.es_impulso(c, k))
    caja = m.pads_corte(c)[0]
    borr = lambda W: dict(W['incl_borradas'])

    # 1. escalon 4: la carga no la borra; bajar a 3, si
    sube(W, c, celda, 4)
    m.note_on(W, c, m.GEO, 64, 100, reloj[0])           # carga 1 de 4
    m.note_on(W, c, m.GEO, 64, 100, reloj[0])           # carga 2
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    m._undo_note(W, c, celda)                           # baja la carga, no el escalon
    sigue = (W['occ'][celda], len(W['incl'][celda]))
    while W['occ'][celda] >= 4:
        m._undo_note(W, c, celda)
    t.check('escalon 4: bajar la carga sin bajar el escalon no borra la inclusion; bajar a 3, si (causa erosion)',
            sigue == (4, 1) and W['occ'][celda] == 3 and not W['incl'][celda] and borr(W)['erosion'] == 1,
            'ocupacion %d, borradas %s' % (W['occ'][celda], borr(W)))
    W, c13 = nuevo()
    sube(W, c13, celda, 4)
    m.depositar_inclusion(W, c13, celda, m.LLEGADA, reloj[0])
    c25 = con(c13, 25)
    for _ in range(40):
        if W['occ'][celda] < 3:
            break
        golpe(W, c25, ara)
    t.check('antes de la fase 26 (nivel 25) la erosion no borra nada', len(W['incl'][celda]) == 1)

    W, c13 = nuevo()
    c = con(c13)
    sube(W, c, celda, 4)
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    n_golpes = 0
    while W['incl'][celda] and n_golpes < 40:
        golpe(W, c, ara)
        n_golpes += 1
    t.check('con los aranazos de un pad: la inclusion se borra en cuanto la celda baja de 4',
            W['occ'][celda] < 4 and not W['incl'][celda] and borr(W)['erosion'] == 1,
            'ocupacion %d tras %d golpes' % (W['occ'][celda], n_golpes))

    # 2. celda vacia
    W, c13 = nuevo()
    c = con(c13)
    W['last'][1] = dict(note=64, cell=celda, t=reloj[0], vel=100)
    m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    ev = golpe(W, c, bombo)
    tras_bombo = len(W['incl'][celda])
    W, c13 = nuevo()
    c = con(c13)
    W['last'][1] = dict(note=64, cell=celda, t=reloj[0], vel=100)
    m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    ev = golpe(W, c, ara, 1)                            # un golpe flojo: no quita ni una nota
    t.check('celda vacia: un aranazo borra la inclusion aunque no quite nada; un bombo (impulso) no',
            tras_bombo == 1 and ev['quitado'] == 0 and not W['incl'][celda] and borr(W)['erosion'] == 1)
    W, c13 = nuevo()
    c = con(c13)
    W['last'][1] = dict(note=64, cell=celda, t=reloj[0], vel=100)
    perf = list(c['perfiles'])
    perf[ara] = (perf[ara][0], 2, 0)                    # radio 2
    c['perfiles'] = perf
    lejos = [x for x, d in m.rings(celda, 2) if d == 2]
    fuera = [x for x, d in m.rings(celda, 3) if d == 3]
    m.depositar_inclusion(W, c, lejos[0], m.PARADA, reloj[0])
    m.depositar_inclusion(W, c, fuera[0], m.PARADA, reloj[0])
    golpe(W, c, ara)
    t.check('tambien en el segundo anillo del golpe (y no mas alla de su radio)',
            not W['incl'][lejos[0]] and len(W['incl'][fuera[0]]) == 1)
    W, c13 = nuevo()
    c = con(c13)
    W['last'][1] = dict(note=64, cell=celda, t=reloj[0], vel=100)
    m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    ev = m.erosion_mic(W, c, reloj[0], 1.0)
    t.check('un onset del microfono la borra (causa micro)',
            ev['celda'] == celda and not W['incl'][celda] and borr(W)['micro'] == 1 and borr(W)['erosion'] == 0,
            str(borr(W)))

    # 3. un corte y una catastrofe
    W, c13 = nuevo()
    c = con(c13)
    for _ in range(3):
        m.end_cycle(W, c, reloj[0])
        reloj[0] += 1.0
    sube(W, c, celda, 3)
    vecina = m.NEIGH[celda][0]
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])     # escalon 3
    m.depositar_inclusion(W, c, vecina, m.PARADA, reloj[0])     # escalon 0, en el primer anillo
    ev = golpe(W, c, caja)
    t.check('un corte con la caja la borra, en su celda y en las de su anfiteatro (causa corte)',
            ev.get('corte', 0) > 0 and not W['incl'][celda] and not W['incl'][vecina]
            and borr(W)['corte'] >= 1 and sum(borr(W).values()) == 2, str(borr(W)))
    W, c13 = nuevo()
    c = con(c13)
    sube(W, c, celda, 3)
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    quitadas = m.bajar_ocupacion(W, c, celda)           # lo que hace un incendio en cada paso
    t.check('un incendio (fase 14) que baja la ocupacion la borra (causa catastrofe)',
            quitadas > 0 and W['occ'][celda] == 2 and not W['incl'][celda] and borr(W)['catastrofe'] == 1,
            str(borr(W)))

    # 4. dos escalones en la misma celda
    W, c13 = nuevo()
    c = con(c13)
    sube(W, c, celda, 2)
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    sube(W, c, celda, 5)
    m.depositar_inclusion(W, c, celda, m.PARADA, reloj[0])
    while W['occ'][celda] > 4:
        m._undo_note(W, c, celda)
    t.check('dos inclusiones con escalones 2 y 5 en la misma celda: bajar a 4 borra solo la de 5',
            W['occ'][celda] == 4 and [x[0] for x in W['incl'][celda]] == [2])

    # 5. la pasada de seguridad y el dibujo
    W, c13 = nuevo()
    c = con(c13)
    sube(W, c, celda, 3)
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    W['occ'][celda] = 1                                 # baja por un camino que no avisa
    antes = len(W['incl'][celda])
    m.tick(W, c, reloj[0], 120.0, False)
    out = {}
    t.check('la pasada de seguridad de cada fotograma purga lo que baje por otro camino; la geometria de la '
            'fase 25 deja de dibujarla',
            antes == 1 and not W['incl'][celda] and m.build_inclusiones(W, c, reloj[0], out) == [])

    # 6. por los pads de verdad y la leyenda
    W = m.world()
    c = m.cfg()
    sube(W, c, celda, 4)
    m.depositar_inclusion(W, c, celda, m.LLEGADA, reloj[0])
    base.par.Padprueba = caja + 1
    m.on_pulse('Erosionar')
    leg = m.legend()
    linea = ' '.join(l.strip() for l in leg.splitlines() if 'BORRADO' in l)
    t.check('cada borrado suma en su causa; la linea BORRADO',
            'BORRADO  vivas 0   borradas ' in leg and 'erosion ' in linea and 'micro ' in linea
            and 'corte ' in linea and 'catastrofe ' in linea and sum(W['incl_borradas'].values()) >= 1, linea)
    t.check('pagina Fase26: solo Version26, de solo lectura',
            has_par(base, 'Version26') and base.par.Version26.readOnly
            and str(base.par.Version26.eval()).startswith('fase26 v'))


run_test(base, prueba)
print('  Ahora: Sembrar x4, Probllegada 1 y Simponer en la casilla que mira a esa celda;')
print('  Erosionar hasta bajar de 4: la inclusion desaparece (leyenda BORRADO).')
print('=' * 66)
