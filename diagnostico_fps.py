"""
=============================================================================
ESTRATOS - DIAGNOSTICO DE FOTOGRAMAS (no es una fase: no cambia nada)
=============================================================================
Dice que operadores se estan cocinando en cada fotograma y cuanto tardan,
para encontrar por que el proyecto va lento. Solo lee; lo unico que guarda es
una foto de los contadores en el storage de /project1 (clave 'diag_fps').

COMO USARLO
-----------
Con el proyecto en marcha y lento, DOS veces, con unos 10 segundos entre una
y otra:

    exec(open('C:/Users/DareDave/Downloads/est/diagnostico_fps.py').read())

La primera hace la foto. La segunda escribe en el Textport:
  - los fotogramas por segundo reales entre las dos;
  - los operadores que mas tiempo se llevan por fotograma (veces que se han
    cocinado x lo que tardo la ultima), en CPU y en GPU;
  - cuantos operadores de cada tipo se cocinan en todos los fotogramas.
Copia y pega esa salida entera.

Para comparar: hazlo una vez con Modocamara = globo y otra con rasante.
=============================================================================
"""

import time as _t

RAIZ_DIAG = '/project1'
TOPE_DIAG = 30


def _num(o, attr):
    try:
        return float(getattr(o, attr))
    except Exception:
        return 0.0


def _foto_diag():
    raiz = op(RAIZ_DIAG)
    ops = {}
    for o in raiz.findChildren():
        try:
            ops[o.path] = int(_num(o, 'totalCooks'))
        except Exception:
            pass
    return dict(t=_t.time(), frame=int(absTime.frame), ops=ops)


def _informe_diag(antes, ahora):
    raiz = op(RAIZ_DIAG)
    seg = max(1e-6, ahora['t'] - antes['t'])
    fot = max(1, ahora['frame'] - antes['frame'])
    filas, por_tipo, total_cpu, total_gpu = [], {}, 0.0, 0.0
    for o in raiz.findChildren():
        n = ahora['ops'].get(o.path, 0) - antes['ops'].get(o.path, 0)
        if n <= 0:
            continue
        veces = n / float(fot)
        cpu, gpu = _num(o, 'cpuCookTime'), _num(o, 'gpuCookTime')
        filas.append((veces * cpu, veces * gpu, veces, cpu, gpu, o.path, o.OPType))
        total_cpu += veces * cpu
        total_gpu += veces * gpu
        if veces >= 0.9:
            k = por_tipo.setdefault(o.OPType, [0, 0.0, 0.0])
            k[0] += 1
            k[1] += veces * cpu
            k[2] += veces * gpu
    print('')
    print('=' * 100)
    print('DIAGNOSTICO DE FOTOGRAMAS   %s' % RAIZ_DIAG)
    print('=' * 100)
    print('  %d fotogramas en %.1f s = %.1f fps reales   (%.0f ms por fotograma)' % (fot, seg, fot / seg, 1000.0 * seg / fot))
    try:
        b = op('/project1/FASE1')
        print('  Nivel %s   Modocamara %s   Tema %s   motor: %s' % (
            b.par.Nivel.eval(), b.par.Modocamara.eval(), getattr(b.par, 'Tema', None) and b.par.Tema.eval(),
            b.op('motor').module.MOTOR_VERSION))
    except Exception as e:
        print('  (no pude leer FASE1: %s)' % e)
    print('  operadores cocinados: %d   suma CPU %.1f ms/fotograma   suma GPU %.1f ms/fotograma' % (
        len(filas), total_cpu, total_gpu))
    print('  (las sumas cuentan dos veces lo que un COMP incluye de sus hijos: valen para comparar, no como total)')
    for titulo, col in (('LOS QUE MAS CPU SE LLEVAN', 0), ('LOS QUE MAS GPU SE LLEVAN', 1)):
        print('')
        print('  %s (ms por fotograma | veces por fotograma | ms la ultima vez | operador)' % titulo)
        for f in sorted(filas, key=lambda f: -f[col])[:TOPE_DIAG]:
            if f[col] <= 0.0:
                break
            print('  %9.2f | %6.2f | %8.2f | %-14s %s' % (f[col], f[2], f[3 + col], f[6], f[5]))
    print('')
    print('  SE COCINAN EN TODOS LOS FOTOGRAMAS, POR TIPO (cuantos | CPU ms/fotograma | GPU ms/fotograma)')
    for tipo, (n, c, g) in sorted(por_tipo.items(), key=lambda kv: -(kv[1][1] + kv[1][2]))[:TOPE_DIAG]:
        print('  %-18s %5d | %9.2f | %9.2f' % (tipo, n, c, g))
    print('=' * 100)


_raiz_diag = op(RAIZ_DIAG)
_antes_diag = _raiz_diag.fetch('diag_fps', None)
_ahora_diag = _foto_diag()
if _antes_diag and 1.0 <= _ahora_diag['t'] - _antes_diag['t'] <= 600.0 and _ahora_diag['frame'] > _antes_diag['frame']:
    _informe_diag(_antes_diag, _ahora_diag)
    _raiz_diag.unstore('diag_fps')
else:
    _raiz_diag.store('diag_fps', _ahora_diag)
    print('DIAGNOSTICO DE FOTOGRAMAS: foto hecha (%d operadores). Espera unos 10 s y lanzalo otra vez.'
          % len(_ahora_diag['ops']))
