"""
Sesion de 20 minutos por escena (fase 18), sobre el motor sin TouchDesigner.

    python3 pruebas/sesion_escena.py              # las dos escenas, 20 minutos
    python3 pruebas/sesion_escena.py ciudad 5     # una escena, 5 minutos

A 120 BPM y 30 fotogramas por segundo: SEQ1 en semicorcheas (cambia de
pattern cada 4 minutos con una rafaga de All Notes Off: A, B, A, C, A),
SEQ2 cada 3 pasos, y bateria: el bombo (impulso) a negras 16 compases si y 16 no, la
caja (corte) cada 8 compases y un aranazo cada 4. Cada medio segundo dibuja
las instancias y mide la densidad, las piezas y lo que tarda en Python
build_instances (no son los fotogramas de TouchDesigner, pero crecen con
ellos). Al final, los criterios de cierre de la fase 18.
"""

import math
import os
import statistics
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import estratos_motor as m  # noqa: E402

PAR_CFG = dict(Paleta='paleta', Paletatono='paleta_tono', Paletacroma='paleta_croma',
               Umbralvecindad='umbral_vecindad', Pesovecina='peso_vecina', Mincluster='min_cluster',
               Umbraldensidad='dens_umbral', Caos='caos', Maxpiezas='max_piezas', Rugmin='rug_min',
               Rugmax='rug_max', Swaymax='sway_max', Trafico='trafico', Luzcalida='luz_calida',
               Paletaluz='paleta_luz', Paletaalterna='paleta_alterna',
               Contrasteocupada='contraste_ocupada', Tapaneutra='tapa_neutra', Tapaluz='tapa_luz')
PATRONES = {'A': [60, 64, 67, 72, 67, 64, 62, 60, 55, 60, 64, 67, 69, 67, 64, 62],
            'B': [48, 50, 53, 55, 53, 50, 48, 46, 45, 48, 50, 53, 57, 53, 50, 48],
            'C': [72, 71, 67, 64, 62, 64, 67, 71, 74, 76, 74, 71, 67, 64, 62, 60]}
ORDEN = ['A', 'B', 'A', 'C', 'A']


def cfg_escena(nombre):
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=18, avance=1, escena=m.ESCENAS.index(nombre))
    for k, v in m.escena_defecto(nombre).items():
        if k == 'Tema':
            c['tema'] = m.TEMAS.index(v)
        elif k == 'Paleta':
            c['paleta'] = 0 if v == 'generaciones' else 1
        elif k in PAR_CFG:
            c[PAR_CFG[k]] = v
    return c


RAFAGA = 6                  # fotogramas seguidos por muestra


def sesion(nombre, minutos=20.0, fps=30.0, tempo=120.0, muestra=0.5):
    c = cfg_escena(nombre)
    W = m.new_world()
    m.ensure(W)
    W['tema'] = c['tema']
    paso = m.step_dur(c, tempo)
    pads_corte = m.pads_corte(c)
    caja = pads_corte[1] if len(pads_corte) > 1 else (pads_corte[0] if pads_corte else 0)
    aranazo = next((k for k in range(8) if m.es_aranazo(c, k)), 4)
    datos = dict(dens=[], piezas=[], ms=[], luz=[], particulas=[], colgados=[], eras=0, frentes=0,
                 px=[], chops=[])
    pend = []
    k_paso = -1
    t = 0.0
    sig = 0.0
    fotos = int(minutos * 60 * fps)
    for f in range(fotos):
        t = f / fps
        p = int(t / paso)
        if p != k_paso:
            k_paso = p
            for s, n in pend:
                m.note_off(W, c, s, n, t, tempo)
            pend = []
            bar = p // 16
            pat = ORDEN[min(len(ORDEN) - 1, int(t // 240.0))]
            if p > 0 and p % (240 * 8) == 0:     # cada 4 minutos (8 pasos por segundo): All Notes Off
                for ch in range(8):
                    m.on_cc(W, c, ch + 1, 123, 0, t + 0.001 * ch)
            n1 = PATRONES[pat][p % 16]
            m.note_on(W, c, m.GEO, n1, 80 + (p * 7) % 40, t, tempo)
            pend.append((m.GEO, n1))
            if p % 3 == 0:
                n2 = [36, 43, 41, 39, 46][(p // 3) % 5]
                m.note_on(W, c, m.ARQ, n2, 70, t, tempo)
                pend.append((m.ARQ, n2))
            if (bar // 16) % 2 == 1 and p % 4 == 0:
                m.erosion(W, c, 0, 100, t)       # bombo (desde la fase 7 v12, impulso)
            if p % 128 == 64:
                m.erosion(W, c, caja, 100, t)    # caja: corte cada 8 compases
            if p % 64 == 40:
                m.erosion(W, c, aranazo, 100, t)  # un aranazo cada 4 compases
        out = m.tick(W, c, t, tempo, True)
        if out.get('frente'):
            datos['frentes'] += 1
        if out.get('ciclo'):
            datos['eras'] += 1
            datos['colgados'].append(len(m.transitos_colgados(W, c)))
        if t >= sig:
            sig += muestra
            # como en TouchDesigner: fotogramas seguidos (con el refresco de la naturaleza,
            # fase 11 v8) y los Script CHOP de modelos que habria que recocer
            ms, recocer, antes = [], [], None
            for j in range(RAFAGA):
                t0 = time.perf_counter()
                inst = m.build_instances(W, c, t + j / fps, tiles=(j == 0), refresco=True)   # losetas: como en TD
                ms.append((time.perf_counter() - t0) * 1000.0)
                mods = dict((k, v) for k, v in inst.items() if k.startswith('mod_'))
                if antes is not None:
                    recocer.append(sum(1 for k, v in mods.items() if antes.get(k, []) != v))
                antes = mods
            datos['ms'].append(statistics.mean(ms))
            datos['chops'].append(statistics.mean(recocer) if recocer else 0.0)
            datos['dens'].append(m.occupied(W) / float(m.N))
            datos['piezas'].append(sum(len(v) for k, v in inst.items() if k.startswith('mod_')))
            datos['particulas'].append(len(inst.get('particulas', [])))
            datos['luz'].append(len(inst.get('luz_local', [])))
            datos['px'].append(m.px_formaciones(W, c))
    datos['R'] = m.top_radius(W, c)
    return datos


def informe(nombre, d, minutos):
    ms = d['ms']
    n = len(ms)
    q = max(1, n // 4)
    p95 = sorted(ms)[int(0.95 * (n - 1))]
    med = statistics.median(ms)
    ini, fin = statistics.median(ms[:q]), statistics.median(ms[-q:])
    sobre = sum(1 for x in d['dens'] if x > 0.6) / float(max(1, n))
    semilla = min(x[0] for x in d['px'])
    corona = min(x[1] for x in d['px'])
    criterios = [
        ('la densidad se mantiene por debajo del 60 %% (max %d %%, %.0f %% del tiempo por encima)'
         % (round(100 * max(d['dens'])), 100 * sobre), sobre <= 0.05),
        ('una formacion grande se distingue de una pequena (semilla %.0f px, coronacion %.0f px en 720)'
         % (semilla, corona), semilla >= 6 and corona >= 4 * semilla),
        ('fotogramas estables con el maximo de piezas (%d piezas; build_instances %.1f ms de mediana, '
         'p95 %.1f, primer cuarto %.1f, ultimo %.1f)' % (max(d['piezas']), med, p95, ini, fin),
         p95 <= 3.0 * med and fin <= 2.0 * max(ini, 1.0)),
        ('ningun transito colgado tras %d fines de ciclo' % d['eras'], not any(d['colgados'])),
    ]
    print('== %s, %.0f minutos: %d eras, %d frentes, radio %.1f, piezas max %d, particulas max %d, '
          'luz local max %d, CHOP de modelos a recocer por fotograma %.1f'
          % (nombre, minutos, d['eras'], d['frentes'], d['R'], max(d['piezas']), max(d['particulas']),
             max(d['luz']), statistics.mean(d['chops']) if d['chops'] else 0.0))
    for texto, bien in criterios:
        print('   %-6s %s' % ('OK' if bien else 'FALLO', texto))
    return all(b for _, b in criterios)


def main():
    escenas = [a for a in sys.argv[1:] if a in m.ESCENAS] or list(m.ESCENAS)
    nums = [a for a in sys.argv[1:] if a.replace('.', '').isdigit()]
    minutos = float(nums[0]) if nums else 20.0
    bien = True
    for e in escenas:
        bien = informe(e, sesion(e, minutos), minutos) and bien
    return 0 if bien else 1


if __name__ == '__main__':
    sys.exit(main())
