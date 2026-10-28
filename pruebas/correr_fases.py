"""
Ejecuta los scripts de fase en un TouchDesigner simulado y resume lo que
dicen: versiones, lineas FALLO y AUTOPRUEBA de cada uno.

    python3 pruebas/correr_fases.py            # desde cero: base y fases 3 a 23 (las que haya)
    python3 pruebas/correr_fases.py -v         # con todo el Textport

Despues de las fases simula una sesion corta (SEQ1, SEQ2 y bateria por el
camino del MIDI real, fotograma a fotograma; desde la fase 21, onsets del
microfono por su senal sintetica) y evalua todas las expresiones.
Luego relanza cada fase (de la 3 a la ultima) sobre el proyecto ya
avanzado, como al refrescar el motor, y comprueba que el mundo se conserva.
"""

import contextlib
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import td_simulado  # noqa: E402

FASES = ['fase12_base.py', 'fase3_semilla.py', 'fase4_desborde.py', 'fase5_especies.py',
         'fase6_ciclo.py', 'fase7_erosion.py', 'fase8_conchas.py', 'fase9_arqueologia.py',
         'fase10_direccion.py', 'fase11_piel.py', 'fase12_moduladores.py',
         'fase13_tejido.py', 'fase14_destructores.py', 'fase15_era.py', 'fase16_cortes.py', 'fase17_tiempo.py', 'fase18_escenas.py', 'fase19_modular.py',
         'fase21_microfono.py', 'fase22_camara.py', 'fase23_sala.py']


def correr(sim, archivo, verbose=False):
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            sim.ejecutar(archivo)
        except Exception as e:
            import traceback
            traceback.print_exc(file=buf)
            err = e
    out = buf.getvalue()
    if verbose:
        print(out)
    lineas = out.splitlines()
    version = next((l.split('EJECUTANDO:')[1].strip() for l in lineas if 'EJECUTANDO:' in l), '?')
    fallos = [l for l in lineas if 'FALLO' in l and 'pegame' not in l]
    auto = [l.strip() for l in lineas if 'AUTOPRUEBA OK' in l or 'AUTOPRUEBA FALLIDA' in l]
    bien = err is None and not fallos and auto and all('OK' in a for a in auto)
    print('%-6s %-24s %s' % ('OK' if bien else 'FALLO', archivo, version[:60]))
    if not bien:
        for l in fallos:
            print('         ' + l.strip())
        if err is not None:
            print('         excepcion: %s' % err)
            print('\n'.join('         ' + l for l in out.splitlines()[-15:]))
        if not auto:
            print('         sin AUTOPRUEBA')
    return bien, out


def sesion(sim, compases=48, fps=30.0):
    """SEQ1 en semicorcheas, SEQ2 cada 3 pasos y bateria en negras, por los
    bytes MIDI, fotograma a fotograma a 120 BPM. Desde la fase 21, un clic
    sintetico (Simonset) cada dos negras, por la cadena del microfono."""
    base = sim.op('/project1/FASE1')
    mm = base.op('midi_callbacks').module
    paso = 60.0 / 120.0 / 4
    fpp = fps * paso
    notas1 = [60, 62, 64, 60, 67, 64, 62, 60]
    notas2 = [48, 50, 53]
    k = 0
    pend = []
    for f in range(int(compases * 16 * fpp)):
        sim.fotograma(1.0 / fps)
        p = int(f / fpp)
        if p != k or f == 0:
            k = p
            for b in pend:
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes(b))
            pend = []
            n1 = notas1[p % len(notas1)]
            mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9C, n1, 90 + p % 30]))
            pend.append([0x8C, n1, 0])
            if p % 3 == 0:
                n2 = notas2[(p // 3) % len(notas2)]
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9D, n2, 70]))
                pend.append([0x8D, n2, 0])
            if p % 8 == 2 and getattr(base.par, 'Simonset', None) is not None:
                base.par.Simonset.pulse()
            if p % 16 == 4 and (p // 64) % 2 == 1:
                mm.onReceiveMIDI(None, 0, 'raw', 0, 0, 0, True, bytes([0x9F, 36 + (p // 16) % 4, 100]))
    return sim.expresiones()


def main():
    verbose = '-v' in sys.argv
    hasta = None
    for a in sys.argv[1:]:
        if a.startswith('--hasta='):
            hasta = a.split('=')[1]
    sim = td_simulado.Sim(REPO)
    todo = True
    for f in FASES:
        if not os.path.exists(os.path.join(REPO, f)):
            continue
        bien, _ = correr(sim, f, verbose)
        todo = todo and bien
        if hasta and f.startswith(hasta):
            break
    with contextlib.redirect_stdout(io.StringIO()):
        malas = sesion(sim)
    m = sim.op('/project1/FASE1/motor').module
    W = m.world()
    print('       mundo tras la sesion: %d celdas ocupadas, %d conchas, nivel %d%s'
          % (m.occupied(W), m.n_shells(W), m.cfg()['nivel'],
             ', %d onsets del microfono' % W['mic']['n'] if m.cfg()['nivel'] >= 21 else ''))
    print('%-6s sesion simulada: %d expresiones con error' % ('OK' if not malas else 'FALLO', len(malas)))
    for m_ in malas[:10]:
        print('         %s.%s: %s' % m_)
    # relanzar sobre el proyecto avanzado: el mundo no se pierde
    antes = (m.occupied(W), list(W['occ']))
    print('relanzando las fases sobre el proyecto en el nivel %d' % m.cfg()['nivel'])
    for f in FASES[1:]:
        if not os.path.exists(os.path.join(REPO, f)):
            continue
        bien, _ = correr(sim, f, verbose)
        todo = todo and bien
    m = sim.op('/project1/FASE1/motor').module
    W = m.world()
    igual = list(W['occ']) == antes[1]
    print('%-6s el mundo se conserva al relanzar (%d celdas ocupadas)' % ('OK' if igual else 'FALLO', antes[0]))
    with contextlib.redirect_stdout(io.StringIO()):
        malas2 = sesion(sim, compases=4)
    print('%-6s sesion tras relanzar: %d expresiones con error' % ('OK' if not malas2 else 'FALLO', len(malas2)))
    return 0 if todo and not malas and not malas2 and igual else 1


if __name__ == '__main__':
    sys.exit(main())
