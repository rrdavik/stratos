"""
=============================================================================
ESTRATOS - AJUSTE DE LA VISTA (CALIBRACION)
=============================================================================
No es una fase: no cambia el nivel ni el mundo. Pone en FASE1 los valores
calibrados para ver bien el planeta en una sesion larga, tambien los que
hayas cambiado a mano (relanzar una fase solo cambia los que seguian en el
valor por defecto). Dice en el Textport que ha cambiado (antes -> ahora) y
deja escrita la linea para volver a lo de antes.

POR QUE
-------
Medido en una sesion simulada (SEQ1, SEQ2 y bateria a 120 BPM):
  - con Ciclomin 8 y Umbralnovedad 0,378 el mundo se enterraba cada 9 o
    10 compases (unos 20 s), en cuanto llegaba al limite;
  - con Herencia 0,125 el mundo nuevo arranca casi vacio y madura en
    cuanto el pattern llena sus celdas: eras de ~20 compases. Con 0,25,
    lo heredado que el pattern no toca frena la madurez y las eras se
    asientan en ~50 compases, con cualquier pattern;
  - el radio crecia sin tope: a los 20 minutos el planeta media 3 o 4
    veces el nucleo (radio 24 a 42) y las formaciones eran motas;
  - con Growstep 0,04 la formacion se quedaba entre el 18 y el 34 % y al
    llegar a Umbralram saltaba al limite de golpe. Ademas, como el coste
    de cada escalon sube con la altura, una formacion baja madura con
    pocas notas: otra razon de las eras cortas.

QUE CAMBIA
----------
  ERAS      Ciclomin 16, Compasesquietos 3, Umbralnovedad 0,15,
            Ciclomax 64 y Herencia 0,25: un mundo dura de 32 s a ~2 min a
            120 BPM; sin bateria, unos 50 compases (1 min 40 s).
  CORTEZA   Cortezamax 4 y Grosormax 1,5: la concha nueva compacta las
            viejas (motor v37) y el planeta tiende a nucleo + 4; a los 20
            minutos, radio ~11 en vez de 24-42.
  ALTURAS   desde el motor v58 ya no hace falta: Growstep no es un
            parametro y el motor sube siempre a escalones iguales de la
            semilla al limite, (1 - Semillafrac) / (Umbralram - 1).
No toca nada mas (Shellthick, Alturafactor, umbrales de la fase 4,
camara, tema...).

Lo ya enterrado no adelgaza de golpe: el radio nunca baja. Para ver la
calibracion desde el principio, Resetmundo (pagina Fase3).

COMO USARLO
-----------
    exec(open('C:/Users/DareDave/Downloads/est/ajuste_vista.py').read())
=============================================================================
"""

CARPETA = 'C:/Users/DareDave/Downloads/est'
exec(open(CARPETA + '/estratos_comun.py', encoding='utf-8').read())

VERSION = 'ajuste_vista v2  (eras mas largas y corteza que se compacta; las alturas ya las calcula el motor)'
banner(VERSION)

base = require_base(3)
motor = install_core(base, CARPETA, current_level(base))   # motor al dia, sin tocar el nivel
m = motor.module

AJUSTE = [('Ciclomin', 16), ('Compasesquietos', 3), ('Umbralnovedad', 0.15), ('Ciclomax', 64),
          ('Herencia', 0.25), ('Cortezamax', CORTEZA_DEF), ('Grosormax', 1.5)]

cambios = []
for nombre, valor in AJUSTE:
    if not has_par(base, nombre):
        info('%s: todavia no existe (aplica su fase); no se ajusta' % nombre)
        continue
    p = getattr(base.par, nombre)
    antes = float(p.eval())
    if abs(antes - valor) < 1e-6:
        ok('%s ya estaba en %g' % (nombre, valor))
        continue
    p.val = valor
    cambios.append((nombre, antes))
    ok('%s: %g -> %g' % (nombre, antes, valor))

try:
    if int(base.par.Ciclomax) < int(base.par.Ciclomin):
        info('Ciclomax (%d) < Ciclomin (%d): se usa Ciclomax = Ciclomin'
             % (int(base.par.Ciclomax), int(base.par.Ciclomin)))
except Exception:
    pass

c = m.cfg()
W = m.world()
lim = m.limit(c)
ok('alturas: semilla %.2f, limite %.2f (Alturafactor %g x Shellthick %g), corona hasta %.2f'
   % (m.height_for(c, 1), lim, c['height_factor'], c['shell_thick'], m.altura_max(c)))
if m.n_shells(W):
    info('el planeta ya tiene %d conchas (radio %.2f): lo enterrado no adelgaza de golpe; '
         'para empezar de cero, Resetmundo (pagina Fase3)' % (m.n_shells(W), m.top_radius(W, c)))
if cambios:
    deshacer = "b = op('%s'); " % COMP_PATH + '; '.join(
        'b.par.%s = %s' % (n, int(a) if float(a).is_integer() else round(a, 4)) for n, a in cambios)
    info('para volver a lo de antes, pega en el Textport:')
    report.append('    ' + deshacer)

print_report()
print('  Ahora: deja sonar un rato. Cada era dura al menos Ciclomin compases y el')
print('  planeta engorda cada vez menos (CONCHAS en la leyenda: corteza y compactacion).')
print('=' * 66)
