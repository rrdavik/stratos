"""
Regresion de la mezcla de especies (fase 11 v22, motor v121), sin TouchDesigner.

    python3 pruebas/regresion_mezcla.py               # contra el motor de main
    python3 pruebas/regresion_mezcla.py otra_rama 3   # contra otra referencia, 3 minutos

Con Tema fijo en cada especie (naturaleza, ciudad, industria), la misma sesion de
sesion_escena.py (SEQ1, SEQ2, bombo, caja y aranazos, fines de ciclo) en el motor de
la referencia (git show <ref>:estratos_motor.py) y en el de esta copia: el mismo
mundo W (sin los campos nuevos de la mezcla: tema_c, fam y mezcla; desde el motor
v143, huella_nat y fund_c) y las mismas
filas de build_instances en cada muestra. Sale con 1 si algo cambia.
"""

import importlib.util
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
NUEVOS = ('tema_c', 'fam', 'mezcla', 'huella_nat', 'fund_c')     # motor v143: huella_nat y fund_c


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def motor_de(ref):
    texto = None
    for r in ('origin/' + ref, ref):
        try:
            texto = subprocess.check_output(['git', 'show', '%s:estratos_motor.py' % r], cwd=REPO)
            break
        except subprocess.CalledProcessError:
            continue
    if texto is None:
        raise SystemExit('no encuentro estratos_motor.py en %s' % ref)
    f = tempfile.NamedTemporaryFile('wb', suffix='.py', delete=False)
    f.write(texto)
    f.close()
    return f.name


def sesion(m, tema, minutos, fps=30.0, tempo=120.0, cada=0.5):
    """La sesion de sesion_escena.py con el motor m y Tema fijo. Devuelve [(t, W, filas)]."""
    import sesion_escena as se
    c = dict(m.DEFAULT_CFG)
    c.update(nivel=19, avance=1, tema=m.TEMAS.index(tema), refresco_piel=0.0)
    for k, v in m.escena_defecto(tema).items():     # la escena de la fase 18 de ese tema
        if k == 'Paleta':
            c['paleta'] = 0 if v == 'generaciones' else 1
        elif k in se.PAR_CFG:
            c[se.PAR_CFG[k]] = v
    W = m.new_world()
    m.ensure(W)
    W['tema'] = c['tema']
    paso = m.step_dur(c, tempo)
    pads = m.pads_corte(c)
    caja = pads[1] if len(pads) > 1 else (pads[0] if pads else 0)
    aranazo = next((k for k in range(8) if m.es_aranazo(c, k)), 4)
    pend, k_paso, sig, out = [], -1, 0.0, []
    for f in range(int(minutos * 60 * fps)):
        t = f / fps
        p = int(t / paso)
        if p != k_paso:
            k_paso = p
            for s, n in pend:
                m.note_off(W, c, s, n, t, tempo)
            pend = []
            bar = p // 16
            pat = se.ORDEN[min(len(se.ORDEN) - 1, int(t // 240.0))]
            n1 = se.PATRONES[pat][p % 16]
            m.note_on(W, c, m.GEO, n1, 80 + (p * 7) % 40, t, tempo)
            pend.append((m.GEO, n1))
            if p % 3 == 0:
                n2 = [36, 43, 41, 39, 46][(p // 3) % 5]
                m.note_on(W, c, m.ARQ, n2, 70, t, tempo)
                pend.append((m.ARQ, n2))
            if (bar // 16) % 2 == 1 and p % 4 == 0:
                m.erosion(W, c, 0, 100, t)
            if p % 128 == 64:
                m.erosion(W, c, caja, 100, t)
            if p % 64 == 40:
                m.erosion(W, c, aranazo, 100, t)
            if p > 0 and p % 512 == 0:
                m.close_cycle(W, c, t, 'prueba')
        m.tick(W, c, t, tempo, True)
        if t >= sig:
            sig += cada
            filas = m.build_instances(W, c, t, tiles=True)
            out.append((round(t, 4), _limpio(W), _redondeo(filas)))
    return out


def _limpio(W):
    """W sin lo nuevo de la mezcla ni lo que no es estado (resumenes de la leyenda)."""
    import copy
    return dict((k, copy.deepcopy(v)) for k, v in W.items() if k not in NUEVOS)


def _redondeo(x):
    if isinstance(x, dict):
        return dict((k, _redondeo(v)) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return [_redondeo(v) for v in x]
    if isinstance(x, float):
        return round(x, 9)
    return x


def diferencia(a, b, ruta=''):
    if type(a) != type(b):
        return ruta or '(raiz)'
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                return '%s.%s' % (ruta, k)
            d = diferencia(a[k], b[k], '%s.%s' % (ruta, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return '%s (longitud %d / %d)' % (ruta, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = diferencia(x, y, '%s[%d]' % (ruta, i))
            if d:
                return d
        return None
    return None if a == b else ruta


def main():
    args = sys.argv[1:]
    ref = next((a for a in args if not a.replace('.', '').isdigit()), 'main')
    nums = [float(a) for a in args if a.replace('.', '').isdigit()]
    minutos = nums[0] if nums else 2.0
    viejo = cargar('motor_ref', motor_de(ref))
    nuevo = cargar('motor_nuevo', os.path.join(REPO, 'estratos_motor.py'))
    print('regresion: %s (%s) frente a %s, Tema fijo, %.1f min por tema'
          % (nuevo.MOTOR_VERSION, 'esta copia', viejo.MOTOR_VERSION + ' de ' + ref, minutos))
    bien = True
    for tema in ('naturaleza', 'ciudad', 'industria'):
        a = sesion(viejo, tema, minutos)
        b = sesion(nuevo, tema, minutos)
        mal = None
        for (ta, Wa, fa), (tb, Wb, fb) in zip(a, b):
            d = diferencia(Wa, Wb, 'W') or diferencia(fa, fb, 'filas')
            if d:
                mal = 't=%.2f: %s' % (ta, d)
                break
        ok = mal is None and len(a) == len(b)
        bien = bien and ok
        print('  %-6s %-10s %d muestras: el mismo W y las mismas filas%s'
              % ('OK' if ok else 'FALLO', tema, len(a), '' if ok else ' (distinto en %s)' % mal))
    return 0 if bien else 1


if __name__ == '__main__':
    sys.exit(main())
