"""
=============================================================================
ESTRATOS - TOUCHDESIGNER SIMULADO (solo para probar, fuera de TouchDesigner)
=============================================================================
Imita lo justo de TouchDesigner para ejecutar los scripts de fase TAL CUAL:
operadores y rutas, parametros (con expresiones), paginas propias, el
storage, el modulo de los Text DAT, Script CHOP y TOP, Table DAT, absTime y el
componente de tiempo del proyecto (/local/time).

Los COMP (base, geometry, camera, light, null) y los operadores de sala de
la fase 21 (Audio Device In CHOP y Switch CHOP y TOP) solo aceptan los
parametros que tienen en TouchDesigner: un nombre equivocado devuelve None,
como alli, y el script lo avisa con '..'. Los demas SOP, MAT, TOP, CHOP y
DAT aceptan cualquier nombre (no comprobamos sus parametros).

Audio: el Audio Device In CHOP no tiene dispositivo (sin canales, como un
ordenador sin microfono) y va en modo Time Slice, como alli: un CHOP que lo
tenga aguas arriba tambien, y un Script CHOP en ese modo no puede fijar
numSamples (deja el aviso de TouchDesigner en Sim.avisos) salvo que ponga
isTimeSlice = False. numpyArray() da las muestras de un CHOP (canales x
muestras): un Script CHOP se cocina antes, una vez por fotograma, y un
Switch pasa la entrada de su index. En un TOP, lo que se le copio.

Lo que no puede comprobar: el aspecto de la imagen, los nombres exactos de
los parametros de SOP y MAT, y el rendimiento real.
=============================================================================
"""

import fnmatch
import sys
import types

CARPETA_TD = 'C:/Users/DareDave/Downloads/est'

ROT_ORDERS = ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
# Parametros que apuntan a un operador: en TouchDesigner, eval() devuelve el
# operador (que se escribe como su ruta completa), no el texto.
OP_PARS = ('material', 'instanceop', 'lookat')
XFORM_ORDERS = ['srt', 'str', 'rst', 'rts', 'tsr', 'trs']

_XFORM = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'px', 'py', 'pz', 'scale',
          'lookat', 'upvecx', 'upvecy', 'upvecz']
_MENUS = {'rord': ROT_ORDERS, 'xord': XFORM_ORDERS, 'instancerord': ROT_ORDERS,
          'instancexord': XFORM_ORDERS,
          'instancecolormode': ['replace', 'multiply', 'add', 'subtract'],
          'viewanglemethod': ['horzfov', 'vertfov', 'focalaperture'],
          'projection': ['perspective', 'ortho'], 'lighttype': ['point', 'cone', 'distant']}
_DEFAULTS = {'sx': 1.0, 'sy': 1.0, 'sz': 1.0, 'scale': 1.0, 'rord': 'xyz', 'xord': 'srt',
             'instancerord': 'xyz', 'instancexord': 'srt', 'instancecolormode': 'multiply',
             'fov': 45.0, 'viewanglemethod': 'horzfov', 'focal': 50.0, 'aperture': 36.0,
             'near': 0.1, 'far': 1000.0, 'dimmer': 1.0, 'render': True, 'instancing': False,
             'cr': 1.0, 'cg': 1.0, 'cb': 1.0,
             'resolutionw': 1280, 'resolutionh': 720, 'lighttype': 'point'}
STRICT = {
    'baseCOMP': [],
    'nullCOMP': list(_XFORM),
    'geometryCOMP': list(_XFORM) + [
        'xord', 'rord', 'material', 'render', 'drawpriority', 'pickpriority',
        'instancing', 'instanceop', 'instancetx', 'instancety', 'instancetz',
        'instancerx', 'instancery', 'instancerz', 'instancesx', 'instancesy', 'instancesz',
        'instancerord', 'instancexord', 'instancer', 'instanceg', 'instanceb', 'instancea',
        'instancecolormode', 'instancerottox', 'instancerottoy', 'instancerottoz'],
    'cameraCOMP': list(_XFORM) + ['xord', 'rord', 'fov', 'viewanglemethod', 'focal',
                                  'aperture', 'near', 'far', 'projection'],
    'lightCOMP': list(_XFORM) + ['xord', 'rord', 'dimmer', 'cr', 'cg', 'cb', 'lighttype', 'coneangle', 'conedelta'],
    # fase 21 (sala): los parametros de su pagina principal
    'audiodeviceinCHOP': ['active', 'driver', 'device', 'rate', 'bufferlength'],
    'switchCHOP': ['index'],
    'switchTOP': ['index', 'blend'],
}
# los valores por defecto de estos, solo en ellos (no en los demas operadores)
_SALA = {'audiodeviceinCHOP': dict(active=True, driver='default', device='', rate=44100.0, bufferlength=0.1),
         'switchCHOP': dict(index=0.0), 'switchTOP': dict(index=0.0, blend=False)}
_MENUS_SALA = dict(driver=['default', 'asio'])


class AbsTime(object):
    def __init__(self):
        self.frame = 1
        self.seconds = 0.0


# -----------------------------------------------------------------------------
# PARAMETROS
# -----------------------------------------------------------------------------

class Par(object):
    def __init__(self, owner, name, val=0.0, page=None, custom=False, kind='float'):
        self.owner, self.name, self._val = owner, name, val
        self.page, self.custom, self.kind = page, custom, kind
        self.expr = ''
        self.default = val
        self.label = name
        self.normMin, self.normMax, self.min, self.max = 0.0, 1.0, 0.0, 1.0
        self.clampMin = self.clampMax = False
        self.readOnly = False
        self.menuNames = list(_MENUS.get(name, [])) if not custom else []
        self.menuLabels = list(self.menuNames)

    # valor
    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, v):
        prev = self._val
        if self.menuNames and isinstance(v, int) and not isinstance(v, bool):
            v = self.menuNames[max(0, min(len(self.menuNames) - 1, v))]
        if self.kind == 'int':
            v = int(round(float(v)))
        elif self.kind == 'float':
            try:
                v = float(v)
            except (TypeError, ValueError):
                pass
        elif self.kind == 'toggle':
            v = bool(v)
        if self.kind in ('int', 'float') and isinstance(v, (int, float)):
            if self.clampMin:
                v = max(self.min, v)
            if self.clampMax:
                v = min(self.max, v)
        self._val = v
        self.owner._valor_cambiado(self, prev)

    @property
    def menuIndex(self):
        try:
            return self.menuNames.index(self.eval())
        except ValueError:
            return 0

    @menuIndex.setter
    def menuIndex(self, i):
        self.val = self.menuNames[int(i)]

    def eval(self):
        v = self.owner._eval_expr(self.expr, self) if self.expr else self._val
        if self.name in OP_PARS and not self.custom:
            if not v:
                return None
            return self.owner._op_hermano(str(v)) or self.owner.op(str(v))
        return v

    def pulse(self):
        self.owner._pulsado(self)

    def destroy(self):
        self.owner.par._quitar(self.name)

    # como en TouchDesigner, el parametro se usa como su valor
    def __int__(self):
        return int(float(self.eval()))

    def __float__(self):
        return float(self.eval())

    def __bool__(self):
        return bool(self.eval())

    def __str__(self):
        return str(self.eval())

    def __index__(self):
        return int(self)

    def __eq__(self, o):
        return self.eval() == (o.eval() if isinstance(o, Par) else o)

    def __hash__(self):
        return id(self)

    def __mul__(self, o):
        return float(self) * o

    __rmul__ = __mul__

    def __add__(self, o):
        return float(self) + o

    __radd__ = __add__


class ParCollection(object):
    def __init__(self, owner):
        object.__setattr__(self, '_owner', owner)
        object.__setattr__(self, '_pars', {})
        strict = owner.OPType in STRICT
        object.__setattr__(self, '_strict', strict)
        if strict:
            for n in STRICT[owner.OPType]:
                kind = 'menu' if n in _MENUS else ('str' if n in ('material', 'instanceop', 'lookat')
                                                   or n.startswith('instancerotto') else 'float')
                if n in ('render', 'instancing', 'active'):
                    kind = 'toggle'
                if n == 'device':
                    kind = 'str'
                if n in _MENUS_SALA:
                    kind = 'menu'
                defs = _SALA.get(owner.OPType, _DEFAULTS)
                self._pars[n] = Par(owner, n, defs.get(n, '' if kind == 'str' else 0.0), kind=kind)
                if n in _MENUS_SALA:
                    self._pars[n].menuNames = list(_MENUS_SALA[n])
                    self._pars[n].menuLabels = list(_MENUS_SALA[n])

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        p = self._pars.get(name)
        if p is None and not self._strict:
            p = Par(self._owner, name, _DEFAULTS.get(name, 0.0), kind='any')
            if name in _MENUS:
                p._val = _DEFAULTS.get(name, _MENUS[name][0])
            self._pars[name] = p
        if p is None:
            raise AttributeError(name)
        return p

    def __setattr__(self, name, value):
        p = getattr(self, name)
        p.val = value

    def _quitar(self, name):
        self._pars.pop(name, None)

    def _custom(self):
        return [p for p in self._pars.values() if p.custom]

    def __iter__(self):
        return iter(list(self._pars.values()))


class Page(object):
    def __init__(self, owner, name):
        self.owner, self.name = owner, name

    def _append(self, name, kind, label, val):
        if name in self.owner.par._pars:
            raise ValueError('parametro repetido: %s' % name)
        p = Par(self.owner, name, val, page=self, custom=True, kind=kind)
        p.label = label or name
        self.owner.par._pars[name] = p
        return [p]

    def appendFloat(self, name, label=None, size=1):
        return self._append(name, 'float', label, 0.0)

    def appendInt(self, name, label=None, size=1):
        return self._append(name, 'int', label, 0)

    def appendToggle(self, name, label=None):
        return self._append(name, 'toggle', label, False)

    def appendPulse(self, name, label=None):
        return self._append(name, 'pulse', label, False)

    def appendStr(self, name, label=None):
        return self._append(name, 'str', label, '')

    def appendMenu(self, name, label=None):
        return self._append(name, 'menu', label, '')

    def appendRGB(self, name, label=None):
        return [self._append(name + c, 'float', label, 0.0)[0] for c in 'rgb']

    def destroy(self):
        """Como TouchDesigner: quita la pagina y los parametros que le quedan."""
        for p in [p for p in self.owner.par._custom() if p.page is self]:
            p.destroy()
        if self in self.owner._pages:
            self.owner._pages.remove(self)


# -----------------------------------------------------------------------------
# OPERADORES
# -----------------------------------------------------------------------------

class Connector(object):
    def __init__(self, owner, i):
        self.owner, self.index = owner, i

    def connect(self, src):
        self.owner._inputs[self.index] = src


class OutConnector(object):
    """Salida de un operador: connect(op) usa la primera entrada libre."""
    def __init__(self, owner):
        self.owner = owner

    def connect(self, target):
        k = 0
        while k in target._inputs:
            k += 1
        target._inputs[k] = self.owner


class Cell(object):
    def __init__(self, table, r, c):
        self.table, self.row, self.col = table, r, c

    @property
    def val(self):
        return self.table._rows[self.row][self.col]

    @val.setter
    def val(self, v):
        self.table._rows[self.row][self.col] = str(v)

    def __str__(self):
        return self.val


class Channel(object):
    def __init__(self, chop, name):
        self.chop, self.name = chop, name
        self._vals = [0.0] * chop._n

    @property
    def vals(self):
        return list(self._vals)

    @vals.setter
    def vals(self, v):
        self._vals = [float(x) for x in v]

    def __setitem__(self, i, v):
        while len(self._vals) <= i:
            self._vals.append(0.0)
        self._vals[i] = float(v)

    def __getitem__(self, i):
        return self._vals[i]

    def __len__(self):
        return len(self._vals)


class OP(object):
    def __init__(self, sim, optype, name, parent):
        self.sim, self.OPType = sim, optype
        self._name, self._parent = name, parent
        self._children = {}
        self._storage = {}
        self._pages = []
        self._errors = []
        self._inputs = {}
        self._text = ''
        self._module = None
        self._rows = []
        self._chans = []
        self._n = 1
        self.rate = 60.0
        self._cocinado = None
        self._timeslice = None              # None: lo decide su entrada
        self.nodeX = self.nodeY = 0
        self.render = self.display = True
        self.allowCooking = True
        self.cooks = 0
        self.destroyed = False
        self.par = ParCollection(self)
        self.inputConnectors = [Connector(self, i) for i in range(4)]
        self.outputConnectors = [OutConnector(self)]
        self.tempo, self.signature1, self.play = 120.0, 4, True     # /local/time

    def __repr__(self):
        return '<%s %s>' % (self.OPType, self.path)

    def __str__(self):
        return self.path

    # nombre y ruta
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        p = self._parent
        if p is not None:
            p._children.pop(self._name, None)
            p._children[new] = self
        self._name = new

    @property
    def path(self):
        if self._parent is None:
            return '/'
        pp = self._parent.path
        return (pp.rstrip('/') + '/' + self._name)

    @property
    def inputs(self):
        return [self._inputs[k] for k in sorted(self._inputs)]

    @property
    def isCOMP(self):
        return self.OPType.endswith('COMP')

    def parent(self, n=1):
        o = self
        for _ in range(int(n)):
            o = o._parent
            if o is None:
                return None
        return o

    @property
    def children(self):
        return list(self._children.values())

    def findChildren(self, name=None, depth=None, type=None, **kw):
        out = []

        def walk(o, d):
            for c in o.children:
                if name is None or fnmatch.fnmatch(c.name, name):
                    out.append(c)
                if depth is None or d + 1 < depth:
                    walk(c, d + 1)
        walk(self, 0)
        return out

    def _resolve(self, path, base):
        if path is None:
            return None
        path = str(path)
        if path.startswith('/'):
            o = self.sim.root
            parts = [p for p in path.split('/') if p]
        else:
            o = base
            parts = [p for p in path.split('/') if p]
        for p in parts:
            if o is None:
                return None
            if p == '..':
                o = o._parent
            elif p == '.':
                continue
            else:
                o = o._children.get(p)
        return o

    def op(self, path):
        """Desde un COMP, relativo a el (sus hijos); desde otro operador,
        relativo a su padre (sus hermanos)."""
        return self._resolve(path, self if self.isCOMP else self._parent)

    def _op_hermano(self, path):
        return self._resolve(path, self._parent)

    def create(self, kind, name=None):
        optype = kind if isinstance(kind, str) else kind.OPType
        name = name or optype + '1'
        base, k = name, 1
        while name in self._children:
            name = '%s%d' % (base, k)
            k += 1
        o = OP(self.sim, optype, name, self)
        self._children[name] = o
        if optype == 'geometryCOMP':           # el relleno por defecto
            t = OP(self.sim, 'torusSOP', 'torus1', o)
            o._children['torus1'] = t
        return o

    def destroy(self):
        if self._parent is not None:
            self._parent._children.pop(self._name, None)
        self.destroyed = True

    # paginas propias
    def appendCustomPage(self, name):
        pg = Page(self, name)
        self._pages.append(pg)
        return pg

    @property
    def customPages(self):
        return list(self._pages)

    @property
    def customPars(self):
        return self.par._custom()

    # storage
    def store(self, k, v):
        self._storage[k] = v

    def fetch(self, k, default=None, search=True):
        return self._storage.get(k, default)

    def unstore(self, k):
        self._storage.pop(k, None)

    @property
    def storage(self):
        return self._storage

    # errores
    def errors(self, recurse=False):
        return '\n'.join(self._errors[-3:])

    def scriptErrors(self, recurse=False):
        return ''

    def warnings(self, recurse=False):
        return ''

    # Text DAT
    @property
    def text(self):
        if self.OPType == 'tableDAT':
            return '\n'.join('\t'.join(r) for r in self._rows)
        return self._text

    @text.setter
    def text(self, t):
        if t != self._text:
            self._text = t
            self._module = None

    @property
    def module(self):
        if self._module is None:
            mod = types.ModuleType(self.name)
            mod.__dict__.update(self.sim.globales_de(self))
            exec(compile(self._text, self.path, 'exec'), mod.__dict__)
            self._module = mod
        return self._module

    # Table DAT
    def appendRow(self, vals=None):
        self._rows.append([str(v) for v in (vals or [])])

    def deleteRow(self, r):
        del self._rows[r]

    def clear(self, keepSize=False, keepFirstRow=False, keepFirstCol=False):
        if self.OPType.endswith('CHOP'):
            self._chans = []
            return
        self._rows = self._rows[:1] if keepFirstRow else []

    @property
    def numRows(self):
        return len(self._rows)

    @property
    def numCols(self):
        return max([len(r) for r in self._rows] or [0])

    def row(self, r):
        if isinstance(r, str):
            r = [x[0] for x in self._rows].index(r)
        return [Cell(self, r, c) for c in range(len(self._rows[r]))]

    def __getitem__(self, key):
        if self.OPType.endswith('CHOP'):
            for ch in self._chans:
                if ch.name == key:
                    return ch
            if isinstance(key, int) and key < len(self._chans):
                return self._chans[key]
            return None
        r, c = key
        if isinstance(c, str):
            if c not in self._rows[0]:
                return None
            c = self._rows[0].index(c)
        if r >= len(self._rows) or c >= len(self._rows[r]):
            return None
        return Cell(self, r, c)

    # CHOP
    @property
    def numSamples(self):
        return self._n

    @numSamples.setter
    def numSamples(self, n):
        if self.OPType == 'scriptCHOP' and self.isTimeSlice:
            self.sim.avisos.append((self.path, 'tdWarning: Editing numSamples is not supported in Time Slice '
                                    'mode. Disable Time Slice mode by setting CHOP.isTimeSlice=False'))
        self._n = int(n)
        for ch in self._chans:
            ch._vals = (ch._vals + [0.0] * self._n)[:self._n]

    @property
    def isTimeSlice(self):
        """Como en TouchDesigner: el Audio Device In va en Time Slice, y un CHOP
        con una entrada en Time Slice tambien (salvo que se diga lo contrario)."""
        if self._timeslice is not None:
            return self._timeslice
        if self.OPType == 'audiodeviceinCHOP':
            return True
        return any(getattr(i, 'isTimeSlice', False) for i in self.inputs if i.OPType.endswith('CHOP'))

    @isTimeSlice.setter
    def isTimeSlice(self, v):
        self._timeslice = bool(v)

    @property
    def numChans(self):
        return len(self._chans)

    @property
    def chans(self):
        return list(self._chans)

    def appendChan(self, name):
        ch = Channel(self, name)
        self._chans.append(ch)
        return ch

    # cocinar
    def cook(self, force=False, recurse=False):
        self.cooks += 1
        self._cocinado = self.sim.absTime.frame
        if self.OPType in ('scriptCHOP', 'scriptTOP'):
            dat = None
            for nm in ('callbacks', 'callbackdat', 'dat'):
                p = self.par._pars.get(nm)
                if p is not None and p.eval():
                    dat = self._op_hermano(p.eval())
                    break
            if dat is None:
                return
            try:
                dat.module.onCook(self)
            except Exception as e:
                self._errors.append('%s: %s' % (self.OPType, e))
                if self.sim.estricto:
                    raise

    # TOP y CHOP
    def copyNumpyArray(self, a):
        self._np = a

    def numpyArray(self):
        if not self.OPType.endswith('CHOP'):
            return getattr(self, '_np', None)
        import numpy
        if self.OPType == 'switchCHOP':
            ins = self.inputs
            if not ins:
                return numpy.zeros((0, 0))
            k = max(0, min(len(ins) - 1, int(float(self.par.index.eval()))))
            src = ins[k]
            self.rate = src.rate
            return src.numpyArray()
        if self.OPType == 'scriptCHOP' and self._cocinado != self.sim.absTime.frame:
            self._cocinado = self.sim.absTime.frame
            self.cook()
        if not self._chans:
            return numpy.zeros((0, self._n), dtype=numpy.float32)
        return numpy.array([ch.vals for ch in self._chans], dtype=numpy.float32)

    @property
    def width(self):
        return int(float(self.par.resolutionw.eval()))

    @property
    def height(self):
        return int(float(self.par.resolutionh.eval()))

    # expresiones y callbacks
    def _eval_expr(self, expr, par):
        g = self.sim.globales_de(self)
        try:
            return eval(expr, g)
        except Exception as e:
            self._errors.append('%s.%s: %s' % (self.name, par.name, e))
            raise

    def _valor_cambiado(self, par, prev):
        if par.custom and self.sim.callbacks_pars:
            for dat in self.sim.parexec_de(self):
                try:
                    fn = getattr(dat.module, 'onValueChange', None)
                    if fn is not None:
                        fn(par, prev)
                except Exception as e:
                    dat._errors.append(str(e))

    def _pulsado(self, par):
        for dat in self.sim.parexec_de(self):
            fn = getattr(dat.module, 'onPulse', None)
            if fn is not None:
                fn(par)


# -----------------------------------------------------------------------------
# EL TOUCHDESIGNER SIMULADO
# -----------------------------------------------------------------------------

class _Tipo(object):
    def __init__(self, optype):
        self.OPType = optype


class _TD(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        return _Tipo(name)


class Sim(object):
    def __init__(self, carpeta_repo, fps=60.0):
        self.carpeta = carpeta_repo.rstrip('/\\')
        self.fps = fps
        self.absTime = AbsTime()
        self.estricto = False
        self.callbacks_pars = True
        self.avisos = []                    # [(ruta, texto)] de lo que TouchDesigner avisaria
        self.root = OP(self, 'baseCOMP', '', None)
        self.root._name = ''
        local = self.root.create('baseCOMP', 'local')
        local.create('timeCOMP', 'time')
        self.root.create('baseCOMP', 'project1')
        td = _TD('td')
        sys.modules['td'] = td
        self.td = td

    # rutas de Windows -> la carpeta del repositorio
    def open(self, path, *a, **kw):
        p = str(path).replace('\\', '/')
        if p.startswith(CARPETA_TD):
            p = self.carpeta + p[len(CARPETA_TD):]
        return open(p, *a, **kw)

    def op(self, path):
        return self.root._resolve(path, self.root)

    def globales_de(self, o):
        return dict(op=o._op_hermano if not o.isCOMP else o.op, parent=o.parent, me=o,
                    absTime=self.absTime, td=self.td, open=self.open, __name__=o.name)

    def parexec_de(self, comp):
        out = []
        for d in comp.findChildren(depth=1):
            if d.OPType != 'parameterexecuteDAT':
                continue
            try:
                target = d.par.op.eval()
            except Exception:
                target = ''
            if str(target) in (comp.path, comp.name):
                out.append(d)
        return out

    def ejecutar(self, archivo):
        """Ejecuta un script de fase como desde el Textport."""
        g = dict(op=self.op, td=self.td, absTime=self.absTime, open=self.open,
                 __name__='__main__', __builtins__=__builtins__)
        with self.open(CARPETA_TD + '/' + archivo, encoding='utf-8') as f:
            src = f.read()
        exec(compile(src, archivo, 'exec'), g)
        return g

    def fotograma(self, dt=None):
        dt = 1.0 / self.fps if dt is None else dt
        self.absTime.frame += 1
        self.absTime.seconds += dt
        for o in self.op('/project1').findChildren(depth=None):
            if o.OPType == 'executeDAT' and o.par.active.eval():
                fs = None
                for nm in ('framestart', 'onframestart'):
                    if nm in o.par._pars:
                        fs = o.par._pars[nm].eval()
                if fs:
                    o.module.onFrameStart(self.absTime.frame)

    def expresiones(self, raiz='/project1'):
        """Evalua todas las expresiones de todos los parametros. Devuelve
        [(ruta, parametro, error)]."""
        malas = []
        for o in self.op(raiz).findChildren(depth=None):
            for p in list(o.par._pars.values()):
                if p.expr:
                    try:
                        p.eval()
                    except Exception as e:
                        malas.append((o.path, p.name, '%s' % e))
        return malas
