"""
=============================================================================
ESTRATOS - RECARGAR TODO: todas las fases, en orden, de una vez
=============================================================================
No es una fase: es el atajo para no tener que pensar cual lanzar.

Cada fase carga el motor (estratos_motor.py), las piezas comunes y las
migraciones de los parametros ("al dia") sobre el proyecto, y conserva el
mundo. Despues de tocar cualquier archivo del repositorio basta con esto:

    exec(open('C:/Users/DareDave/Downloads/est/recargar_todo.py').read())

QUE HACE
--------
  - Si no existe /project1/FASE1 (proyecto nuevo), empieza por fase12_base.py.
    Si ya existe, NO la lanza (es la que crea el proyecto desde cero).
  - Lanza fase3 ... fase31 en orden, las que haya en la carpeta (las que no
    existan todavia se saltan en silencio).
  - Relanza /project1/SALA con sala_virtual.py solo si ya estaba montada
    (poner SALA = True para montarla tambien si no lo estaba).
  - Para en la primera fase que falle (excepcion o linea FALLO / AUTOPRUEBA
    FALLIDA): las siguientes dependen de ella.
  - No lanza ajuste_vista.py (pisa lo ajustado a mano) ni nada que no sea
    una fase.
  - Al final, un resumen: OK o FALLO por fase, con su version.

Una fase suelta (por ejemplo fase21_microfono.py) sigue valiendo para probar
solo lo ultimo: ya recarga el motor y todo lo comun. Esto es para dejarlo
todo al dia de una vez.
=============================================================================
"""

import sys

CARPETA = 'C:/Users/DareDave/Downloads/est'
SALA = False        # True: montar la sala virtual aunque no exista todavia

FASES_ORDEN = ['fase3_semilla.py', 'fase4_desborde.py', 'fase5_especies.py',
               'fase6_ciclo.py', 'fase7_erosion.py', 'fase8_conchas.py',
               'fase9_arqueologia.py', 'fase10_direccion.py', 'fase11_piel.py',
               'fase12_moduladores.py', 'fase13_tejido.py', 'fase14_destructores.py',
               'fase15_era.py', 'fase16_cortes.py', 'fase17_tiempo.py',
               'fase18_escenas.py', 'fase19_modular.py', 'fase21_microfono.py',
               'fase22_camara.py', 'fase23_sala.py', 'fase24_personas.py', 'fase25_huella.py',
               'fase26_borrado.py', 'fase27_clasificacion.py', 'fase28_noche.py', 'fase29_fila.py',
               'fase30_relampago.py', 'fase31_historico.py']


class _Eco(object):
    """Deja pasar todo al Textport y se queda con una copia para el resumen."""

    def __init__(self, destino):
        self.destino = destino
        self.texto = []

    def write(self, s):
        self.texto.append(s)
        return self.destino.write(s)

    def flush(self):
        try:
            self.destino.flush()
        except Exception:
            pass


def _lee(archivo):
    try:
        with open(CARPETA + '/' + archivo, encoding='utf-8') as f:
            return f.read()
    except (IOError, OSError):
        return None


def _lanza(archivo, src):
    """Ejecuta un script de fase como desde el Textport. Devuelve
    (bien, version, motivo)."""
    eco = _Eco(sys.stdout)
    viejo = sys.stdout
    sys.stdout = eco
    error = None
    try:
        exec(compile(src, archivo, 'exec'), dict(globals()))
    except Exception as e:
        import traceback
        traceback.print_exc(file=eco)
        error = '%s: %s' % (type(e).__name__, e)
    finally:
        sys.stdout = viejo
    lineas = ''.join(eco.texto).splitlines()
    version = next((l.split('EJECUTANDO:')[1].strip() for l in lineas
                    if 'EJECUTANDO:' in l), '?')
    fallos = [l.strip() for l in lineas if 'FALLO' in l and 'pegame' not in l]
    autos = [l for l in lineas if 'AUTOPRUEBA OK' in l or 'AUTOPRUEBA FALLIDA' in l]
    if error:
        return False, version, error
    if fallos:
        return False, version, fallos[0]
    if not autos:
        return False, version, 'sin AUTOPRUEBA'
    if not all('OK' in a for a in autos):
        return False, version, 'AUTOPRUEBA FALLIDA'
    return True, version, ''


def _recargar():
    plan = []
    if op('/project1/FASE1') is None:
        plan.append('fase12_base.py')
    plan += FASES_ORDEN
    if SALA or op('/project1/SALA') is not None:
        plan.append('sala_virtual.py')

    resumen = []
    for archivo in plan:
        src = _lee(archivo)
        if src is None:
            continue                       # esa fase todavia no existe
        print('\n>>>>>> %s' % archivo)
        bien, version, motivo = _lanza(archivo, src)
        resumen.append((bien, archivo, version, motivo))
        if not bien:
            break

    print('\n' + '=' * 70)
    print('RECARGAR TODO')
    for bien, archivo, version, motivo in resumen:
        print('%-6s %-24s %s' % ('OK' if bien else 'FALLO', archivo, version[:60]))
        if not bien:
            print('         %s' % motivo)
    if all(r[0] for r in resumen) and resumen:
        print('RECARGAR TODO OK: %d scripts' % len(resumen))
    else:
        print('RECARGAR TODO PARADO en %s: arregla eso y vuelve a lanzar.'
              % (resumen[-1][1] if resumen else '(nada que lanzar)'))
    print('=' * 70)
    return resumen


_RESUMEN = _recargar()
