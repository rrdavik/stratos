"""
ESTRATOS - PARCHE: la esfera desaparece tras la fase 2

CAUSA
  La fase 2 leia la lista de geometrias del render con .eval(). Ese
  parametro referencia operadores, asi que .eval() devuelve un operador,
  no el texto 'nucleo reticula'. Al escribirlo de vuelta con 'baliza'
  anadida, la lista quedaba corrompida y el render perdia el nucleo y la
  reticula.

QUE HACE
  Una sola cosa: fija la lista del render en 'nucleo reticula baliza'.
  No toca nada mas. Antes y despues te dice que hay.

    exec(open('C:/ruta/a/fix_render_fase2.py').read())
"""

COMP_PATH = '/project1/FASE1'
base = op(COMP_PATH)
if base is None:
    raise RuntimeError('No encuentro %s' % COMP_PATH)
render = base.op('render')
if render is None:
    raise RuntimeError('No encuentro el nodo render en FASE1')

print('=' * 66)
print('PARCHE: lista de geometrias del render')
print('=' * 66)
try:
    print('  antes  : %r' % render.par.geometry.val)
except Exception as e:
    print('  antes  : no pude leerla (%s)' % e)

render.par.geometry = 'nucleo reticula baliza'
print('  ahora  : %r' % render.par.geometry.val)
print('-' * 66)

for nm in ('nucleo', 'reticula', 'baliza'):
    g = base.op(nm)
    if g is None:
        print('  %-9s NO EXISTE' % nm)
        continue
    vivos = [k.name for k in g.children if getattr(k, 'render', False)]
    print('  %-9s renderiza: %s' % (nm, vivos if vivos else 'NADA'))
print('=' * 66)
print('  Mira "salida": deberias ver el nucleo, la reticula y la baliza cian.')
print('=' * 66)
