"""
Perfil de la piel (encargo «piel por turnos», motor v101), sin TouchDesigner.

    python3 pruebas/perfil_piel.py                    # los tres temas
    python3 pruebas/perfil_piel.py ciudad             # uno
    python3 pruebas/perfil_piel.py ciudad 2 600       # 2 minutos de sesion y 600 fotogramas
    python3 pruebas/perfil_piel.py --sin-turnos       # con Turnos y Cachearq apagados
    python3 pruebas/perfil_piel.py --entera           # Refrescopiel 0: la piel entera en cada fotograma
    python3 pruebas/perfil_piel.py --perfil           # y las funciones que mas cuestan (cProfile)

Para cada tema: 5 minutos de la escena de la fase 18 con los patterns de
sesion_escena.py (SEQ1 en semicorcheas, SEQ2, bombo, caja y aranazos), sin
dibujar, y despues 300 fotogramas seguidos a 30 fps con el secuenciador sonando:
tick + build_instances(refresco=True) en cada uno, como en TouchDesigner.
Mide lo que tarda build_instances (media, p95, maximo y picos por encima de
15 ms fuera de los fines de ciclo), lo que se lleva la piel y la arqueologia, y
cuantas geometrias mod_ cambian de filas por fotograma (cada una es un Script
CHOP que TouchDesigner recuece).
"""

import os
import statistics
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.dirname(AQUI))
import estratos_motor as m  # noqa: E402
import sesion_escena as se  # noqa: E402

PICO_MS = 15.0


class _Reloj(object):
    """Envuelve una funcion del motor y suma lo que tarda en el fotograma."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.f = getattr(m, nombre)
        self.ms = 0.0
        setattr(m, nombre, self)

    def __call__(self, *a, **k):
        t0 = time.perf_counter()
        try:
            return self.f(*a, **k)
        finally:
            self.ms += (time.perf_counter() - t0) * 1000.0

    def tomar(self):
        v, self.ms = self.ms, 0.0
        return v


class _Secuenciador(object):
    """Los eventos de sesion_escena.py, paso a paso."""

    def __init__(self, W, c, tempo):
        self.W, self.c, self.tempo = W, c, tempo
        self.paso = m.step_dur(c, tempo)
        pads = m.pads_corte(c)
        self.caja = pads[1] if len(pads) > 1 else (pads[0] if pads else 0)
        self.aranazo = next((k for k in range(8) if m.es_aranazo(c, k)), 4)
        self.pend = []
        self.k = -1

    def __call__(self, t):
        W, c, tempo = self.W, self.c, self.tempo
        p = int(t / self.paso)
        if p == self.k:
            return
        self.k = p
        for s, n in self.pend:
            m.note_off(W, c, s, n, t, tempo)
        self.pend = []
        bar = p // 16
        pat = se.ORDEN[min(len(se.ORDEN) - 1, int(t // 240.0))]
        if p > 0 and p % (240 * 8) == 0:
            for ch in range(8):
                m.on_cc(W, c, ch + 1, 123, 0, t + 0.001 * ch)
        n1 = se.PATRONES[pat][p % 16]
        m.note_on(W, c, m.GEO, n1, 80 + (p * 7) % 40, t, tempo)
        self.pend.append((m.GEO, n1))
        if p % 3 == 0:
            n2 = [36, 43, 41, 39, 46][(p // 3) % 5]
            m.note_on(W, c, m.ARQ, n2, 70, t, tempo)
            self.pend.append((m.ARQ, n2))
        if (bar // 16) % 2 == 1 and p % 4 == 0:
            m.erosion(W, c, 0, 100, t)
        if p % 128 == 64:
            m.erosion(W, c, self.caja, 100, t)
        if p % 64 == 40:
            m.erosion(W, c, self.aranazo, 100, t)


def perfil(nombre, minutos=5.0, fotos=300, fps=30.0, tempo=120.0, turnos=True, cprofile=False, entera=False):
    c = se.cfg_escena(nombre)
    if not turnos:
        c.update(turnos=0, cache_arq=0)
    if entera:
        c.update(refresco_piel=0.0)
    W = m.new_world()
    m.ensure(W)
    W['tema'] = c['tema']
    seq = _Secuenciador(W, c, tempo)
    previo = int(minutos * 60 * fps)
    for f in range(previo):
        t = f / fps
        seq(t)
        m.tick(W, c, t, tempo, True)
    t = previo / fps                    # un fotograma sin medir: la biblioteca y los bufers
    m.build_instances(W, c, t - 1.0 / fps, tiles=True, refresco=True)
    relojes = [_Reloj(x) for x in ('build_piel_refresco', 'build_arqueologia')]
    ms, piel, arq, cambian, picos, ciclos = [], [], [], [], 0, 0
    antes = None
    prof = None
    if cprofile:
        import cProfile
        prof = cProfile.Profile()
    try:
        for f in range(fotos):
            t = (previo + f) / fps
            seq(t)
            o = m.tick(W, c, t, tempo, True)
            if prof:
                prof.enable()
            t0 = time.perf_counter()
            inst = m.build_instances(W, c, t, tiles=(f % 30 == 0), refresco=True)
            dt = (time.perf_counter() - t0) * 1000.0
            if prof:
                prof.disable()
            ms.append(dt)
            piel.append(relojes[0].tomar())
            arq.append(relojes[1].tomar())
            if o.get('ciclo'):
                ciclos += 1
            elif dt > PICO_MS:
                picos += 1
            mods = dict((k, v) for k, v in inst.items() if k.startswith('mod_'))
            if antes is not None:
                cambian.append(sum(1 for k, v in mods.items() if antes.get(k) != v))
            antes = mods
    finally:
        for r in relojes:
            setattr(m, r.nombre, r.f)
    if prof:
        import pstats
        pstats.Stats(prof).sort_stats('cumulative').print_stats(25)
    return dict(ms=ms, piel=piel, arq=arq, cambian=cambian, picos=picos, ciclos=ciclos,
                ocupadas=m.occupied(W))


def fila(nombre, d):
    ms = sorted(d['ms'])
    p95 = ms[int(0.95 * (len(ms) - 1))]
    con = sum(1 for x in d['cambian'] if x)
    return ('| %s | %d | %.1f ms | %.1f ms | %.1f ms | %d | %.1f ms | %.1f ms | %d de %d (%.1f por fotograma) |'
            % (nombre, d['ocupadas'], statistics.mean(d['ms']), p95, ms[-1], d['picos'],
               statistics.mean(d['piel']), statistics.mean(d['arq']), con, len(d['cambian']),
               statistics.mean(d['cambian']) if d['cambian'] else 0.0))


def main():
    args = sys.argv[1:]
    temas = [a for a in args if a in m.ESCENAS] or list(m.ESCENAS)
    nums = [float(a) for a in args if a.replace('.', '').isdigit()]
    minutos = nums[0] if nums else 5.0
    fotos = int(nums[1]) if len(nums) > 1 else 300
    turnos = '--sin-turnos' not in args
    entera = '--entera' in args
    modo = 'Refrescopiel 0 (entera)' if entera else ('Turnos y Cachearq' if turnos else 'sin turnos ni cache')
    print('%s · %s · %.0f min de sesion y %d fotogramas a 30 fps' % (m.MOTOR_VERSION, modo, minutos, fotos))
    print('| Tema | Celdas | build_instances media | p95 | max | picos > %.0f ms | piel | arqueologia '
          '| fotogramas con mod_ que cambian |' % PICO_MS)
    print('|---|---|---|---|---|---|---|---|---|')
    for t in temas:
        d = perfil(t, minutos, fotos, turnos=turnos, cprofile='--perfil' in args, entera=entera)
        print(fila(t, d))
        sys.stdout.flush()
    return 0


if __name__ == '__main__':
    sys.exit(main())
