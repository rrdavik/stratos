# =============================================================================
# ESTRATOS - MOTOR
# =============================================================================
# Este archivo se carga dentro del Text DAT 'motor' de /project1/FASE1.
# Lo cargan los scripts de fase (fase3 ... fase10); no se ejecuta solo.
#
# Contiene TODA la logica del mundo, en dos bloques:
#
#   1. NUCLEO     Python puro: ocupacion, desbordamiento, especies, ciclo,
#                 erosion, conchas y cortes. No toca TouchDesigner.
#   2. ADAPTADOR  Lo que habla con TouchDesigner: lee parametros, recibe
#                 MIDI, alimenta los Script CHOP de instancias, la leyenda.
#
# Cada bloque del nucleo se activa con el NIVEL (parametro Nivel, pagina
# Estratos), que fija el script de la ultima fase aplicada. Asi la fase 3
# se comporta como fase 3 aunque el motor ya sepa hacer la 10.
#
# El estado del mundo vive en el storage de este DAT ('W'): sobrevive a
# guardar el .toe y a recargar el motor.
# =============================================================================

MOTOR_VERSION = 'motor v2'

import math

COLS, ROWS = 12, 8
N = COLS * ROWS
LAT_SPAN = 0.86            # igual que reticula_callbacks: evita los polos

NOTE_NAMES = ['do', 'do#', 're', 're#', 'mi', 'fa',
              'fa#', 'sol', 'sol#', 'la', 'la#', 'si']

GEO, ARQ, HIB = 1, 2, 3
SPECIES_NAME = {0: '-', 1: 'geo', 2: 'arq', 3: 'hib'}

INST_CHANS = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'r', 'g', 'b']
DUMMY_ROW = [0.0, -9999.0, 0.0, 0, 0, 0, 0.001, 0.001, 0.001, 0, 0, 0]

# Perfiles de erosion por defecto: (reduccion 1-3, radio 0-2, profundidad 0-4)
# Pads 1-5: aranazos. 6-8: cortes que atraviesan conchas.
PERFILES_DEFECTO = [
    (1, 0, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0),
    (2, 1, 0), (2, 1, 2), (3, 1, 3), (3, 2, 4),
]

DEFAULT_CFG = dict(
    nivel=3,
    core_radius=6.0,
    # fase 3
    shell_thick=0.5, height_factor=3.0, seed_frac=0.25, grow_frac=0.30,
    gate_mode=1, vel_umbral=64, steps_per_beat=4,
    # fase 4
    th_branch=4, th_fusion=6, th_crown=8, sat_size=0.6, sat_limit=0.6,
    neigh_mode=1,
    # fase 6
    reps=8, cycle_mode=0, long_manual=16, long_min=4, long_fija=0,
    steps_per_bar=16, turn_auto=1,
    # fase 7
    dens_umbral=0.60, rad_mult=2.0, target_mode=2,
    perfiles=PERFILES_DEFECTO,
    # fase 8
    herencia=0.25, max_shells=24,
    # fase 9
    scar_time=4.0, flash=3.0,
)


# -----------------------------------------------------------------------------
# 1. NUCLEO - geometria del reticulo
# -----------------------------------------------------------------------------

def idx(col, row):
    return int(row) * COLS + int(col) % COLS


def colrow(i):
    return i % COLS, i // COLS


def note_to_cell(note):
    return int(note) % COLS, (int(note) // COLS) % ROWS


def note_cell(note):
    c, r = note_to_cell(note)
    return idx(c, r)


def note_name(note):
    return '%s%d' % (NOTE_NAMES[int(note) % 12], int(note) // 12 - 1)


def cell_angles(col, row):
    theta = (col / float(COLS)) * 2.0 * math.pi
    phi = ((row + 0.5) / float(ROWS) - 0.5) * math.pi * LAT_SPAN
    return theta, phi


def cell_normal(col, row):
    theta, phi = cell_angles(col, row)
    return (math.cos(phi) * math.cos(theta),
            math.sin(phi),
            math.cos(phi) * math.sin(theta))


def normal_i(i):
    c, r = colrow(i)
    return cell_normal(c, r)


def _build_neighbors():
    # Reticula hexagonal desplazada: 2 vecinas en la misma banda y 2 en
    # cada banda contigua. Las bandas pares miran a (c-1, c), las impares a
    # (c, c+1). Es simetrica: si A es vecina de B, B lo es de A.
    # En los polos (bandas 0 y 7) solo hay 4 vecinas: el desborde se reparte
    # entre las que existen (rebota, no se pierde).
    out = []
    for i in range(N):
        c, r = colrow(i)
        res = [idx((c - 1) % COLS, r), idx((c + 1) % COLS, r)]
        offs = (-1, 0) if r % 2 == 0 else (0, 1)
        for rr in (r - 1, r + 1):
            if 0 <= rr < ROWS:
                for o in offs:
                    res.append(idx((c + o) % COLS, rr))
        out.append(res)
    return out


NEIGH = _build_neighbors()


def rings(i, k):
    """Celdas a distancia <= k de i, con su distancia: [(celda, d), ...]"""
    seen = {i: 0}
    frontier = [i]
    for d in range(1, int(k) + 1):
        nxt = []
        for c in frontier:
            for n in NEIGH[c]:
                if n not in seen:
                    seen[n] = d
                    nxt.append(n)
        frontier = nxt
    return sorted(seen.items(), key=lambda kv: (kv[1], kv[0]))


def orient(n):
    """Rotaciones (rx, ry) en grados que llevan el eje +Y local a n.
    Orden de TouchDesigner por defecto: primero X, luego Y."""
    x, y, z = n
    y = max(-1.0, min(1.0, y))
    phi = math.asin(y)
    theta = math.atan2(z, x)
    return 90.0 - math.degrees(phi), 90.0 - math.degrees(theta)


def tangents(n):
    """Ejes locales X (este) y Z (sur) de la celda, ya orientados."""
    x, y, z = n
    y = max(-1.0, min(1.0, y))
    phi = math.asin(y)
    theta = math.atan2(z, x)
    e = (math.sin(theta), 0.0, -math.cos(theta))
    t = (math.sin(phi) * math.cos(theta), -math.cos(phi), math.sin(phi) * math.sin(theta))
    return e, t


def _norm(v):
    l = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2) or 1.0
    return (v[0] / l, v[1] / l, v[2] / l)


def _add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def _mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def _hash01(*vals):
    # Pseudoaleatorio DETERMINISTA por celda: misma celda, misma forma.
    # No decide nada del mundo; solo varia la silueta de las piezas.
    h = 2166136261
    for v in vals:
        h = ((h ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return (h % 10007) / 10006.0


# -----------------------------------------------------------------------------
# 1. NUCLEO - estado del mundo
# -----------------------------------------------------------------------------

def _new_det():
    return dict(hist={}, L=None, fp=None, phase=0, src='', score=0.0,
                miss=[], since=0)


def new_world():
    return dict(
        v=1,
        occ=[0] * N,        # ocupacion
        h=[0.0] * N,        # altura objetivo
        vh=[0.0] * N,       # altura visible (se acerca a h suavemente)
        sp=[0] * N,         # especie visible: 0, geo, arq, hib
        own=[0] * N,        # especie fundadora
        traza=[0] * N,      # bits: 1 geo, 2 arq
        vel=[0] * N,        # velocidad del evento fundador
        par=[-1] * N,       # satelite de... (-1: formacion propia)
        huella=[0.0] * N,   # instante en que quedo la huella (0: sin huella)
        hueco=[0] * N,      # conchas retiradas por un corte en esta celda
        resto=[0.0] * N,    # fraccion de herencia acumulada
        gen=0,
        shells=[],
        scars={},
        flash=None,
        last={1: None, 2: None},
        pend={},
        hits={1: 0, 2: 0, 3: 0},
        hit_t={1: -1.0, 2: -1.0},
        det={1: _new_det(), 2: _new_det()},
        lib={1: [], 2: []},
        clock=dict(t_ref=None, step_ref=0, phase_ref=0, last_note_t=-99.0,
                   stop_t=-99.0, start_t=-99.0),
        cycle=dict(idx=None, count=0, steps=0, anchor=0, pos=0.0, last_t=-99.0),
        burst=dict(times=[], pending=None),
        aviso='',
        ev={},
        t=None,
        dirty=True,
    )


def ensure(W):
    base = new_world()
    for k, v in base.items():
        if k not in W:
            W[k] = v
    for s in (1, 2):
        if s not in W['det']:
            W['det'][s] = _new_det()
        if s not in W['lib']:
            W['lib'][s] = []
    return W


def limit(cfg):
    return cfg['height_factor'] * cfg['shell_thick']


def height_for(cfg, occ):
    lim = limit(cfg)
    if occ <= 0:
        return 0.0
    if occ >= cfg['th_branch']:
        return lim
    return min(lim, cfg['seed_frac'] * lim + (occ - 1) * cfg['grow_frac'] * lim)


def state_name(cfg, occ, lvl=10):
    if occ <= 0:
        return 'vacia'
    if occ == 1:
        return 'semilla'
    if occ < cfg['th_branch']:
        return 'crecimiento'
    if lvl < 4:
        return 'limite'
    if occ < cfg['th_fusion']:
        return 'ramificacion'
    if occ < cfg['th_crown']:
        return 'fusion'
    return 'coronacion'


def n_shells(W):
    return len(W['shells'])


def top_radius(W, cfg):
    return cfg['core_radius'] + n_shells(W) * cfg['shell_thick']


def base_radius(W, cfg, i):
    return top_radius(W, cfg) - W['hueco'][i] * cfg['shell_thick']


def occupied(W):
    return sum(1 for o in W['occ'] if o > 0)


def _clear_cell(W, i):
    W['occ'][i] = 0
    W['h'][i] = 0.0
    W['par'][i] = -1


def _bit(s):
    return 1 if s == GEO else 2


# -----------------------------------------------------------------------------
# 1. NUCLEO - crecimiento (fases 3, 4, 5)
# -----------------------------------------------------------------------------

def grow(W, cfg, i, s, vel, now):
    lvl = cfg['nivel']
    lim = limit(cfg)
    o = W['occ'][i]
    if o == 0:
        W['occ'][i] = 1
        W['own'][i] = s
        W['sp'][i] = s
        W['traza'][i] = _bit(s)
        W['vel'][i] = int(vel)
        W['par'][i] = -1
        W['h'][i] = cfg['seed_frac'] * lim
        W['huella'][i] = 0.0
        return dict(estado='semilla', inc=0.0, celda=i)

    if W['par'][i] >= 0:                    # un satelite que recibe senal
        W['par'][i] = -1                    # directa se independiza
    b = _bit(s)
    if not (W['traza'][i] & b):
        W['traza'][i] |= b
        if W['own'][i] != s:
            W['sp'][i] = HIB                # colonizacion
    o += 1
    W['occ'][i] = o
    inc = 0.0
    out = dict(celda=i)
    if o < cfg['th_branch']:
        inc = cfg['grow_frac'] * lim
        W['h'][i] = min(lim, W['h'][i] + inc)
    else:
        W['h'][i] = lim
        if lvl >= 4:
            out['desborde'] = overflow(W, cfg, i, s, vel, now)
    out['estado'] = state_name(cfg, o, lvl)
    out['inc'] = inc
    return out


def overflow(W, cfg, i, s, vel, now):
    nb = NEIGH[i]
    k = int(vel) if cfg['neigh_mode'] == 0 else int(vel) + W['occ'][i]
    j = nb[k % len(nb)]
    lim = limit(cfg)
    grow_h = cfg['grow_frac'] * lim
    o = W['occ'][j]
    if o == 0:
        W['occ'][j] = 1
        W['par'][j] = i
        W['own'][j] = W['own'][i]
        W['sp'][j] = W['own'][i]
        W['traza'][j] = _bit(W['own'][i])
        W['vel'][j] = int(vel)
        W['h'][j] = cfg['seed_frac'] * lim
        W['huella'][j] = 0.0
        kind = 'satelite nuevo'
    elif W['par'][j] == i:
        W['occ'][j] = o + 1
        W['h'][j] = min(cfg['sat_limit'] * lim, W['h'][j] + grow_h)
        kind = 'satelite crece'
    else:
        # presion sobre una formacion ajena: suma ocupacion, sin cascada
        W['occ'][j] = o + 1
        b = _bit(s)
        if not (W['traza'][j] & b):
            W['traza'][j] |= b
            if W['own'][j] != s:
                W['sp'][j] = HIB
        if W['par'][j] >= 0:
            W['h'][j] = min(cfg['sat_limit'] * lim, W['h'][j] + grow_h)
        else:
            W['h'][j] = lim if o + 1 >= cfg['th_branch'] else min(lim, W['h'][j] + grow_h)
        kind = 'presion'
    W['ev']['desborde'] = dict(de=i, a=j, tipo=kind, t=now)
    return j


def satellites_of(W, i):
    return [j for j in NEIGH[i] if W['par'][j] == i and W['occ'][j] > 0]


def note_off(W, cfg, s, note, now, tempo):
    p = W['pend'].pop('%d:%d' % (s, int(note)), None)
    if not p or not cfg['gate_mode']:
        return None
    i, t_on, inc, o = p
    if inc <= 0 or W['occ'][i] != o:
        return None
    step = step_dur(cfg, tempo)
    factor = max(0.0, now - t_on) / step
    m = max(0.25, min(2.0, 2.0 * factor))     # gate al 50 % = incremento normal
    lim = limit(cfg)
    lo = cfg['seed_frac'] * lim
    W['h'][i] = max(lo, min(lim, W['h'][i] + inc * (m - 1.0)))
    return m


def note_on(W, cfg, s, note, vel, now, tempo=120.0):
    W['hits'][s] = W['hits'].get(s, 0) + 1
    W['hit_t'][s] = now
    i = note_cell(note)
    W['last'][s] = dict(note=int(note), cell=i, t=now, vel=int(vel))
    if cfg['nivel'] >= 6:
        st = clock_note(W, cfg, now, tempo)
        det_note(W, cfg, s, int(note), st)
    res = grow(W, cfg, i, s, vel, now)
    W['pend']['%d:%d' % (s, int(note))] = [i, now, res.get('inc', 0.0), W['occ'][i]]
    W['ev']['ultima'] = dict(s=s, celda=i, occ=W['occ'][i], estado=res['estado'], t=now)
    return res


# -----------------------------------------------------------------------------
# 1. NUCLEO - reloj, patterns y ciclo (fase 6)
# -----------------------------------------------------------------------------

def step_dur(cfg, tempo):
    if tempo and tempo > 0:
        return 60.0 / tempo / max(1, cfg['steps_per_beat'])
    return 0.125


def step_at(W, cfg, now, tempo):
    ck = W['clock']
    if ck['t_ref'] is None:
        return None
    return ck['step_ref'] + (now - ck['t_ref']) / step_dur(cfg, tempo)


def clock_note(W, cfg, now, tempo):
    """Paso del secuenciador en el que cae una nota. Se reancla en cada
    nota: el error no se acumula mientras el jitter sea < medio paso."""
    ck = W['clock']
    if ck['t_ref'] is None:
        st = 0
        ck['phase_ref'] = 0
    else:
        st = int(round(step_at(W, cfg, now, tempo)))
    ck['t_ref'] = now
    ck['step_ref'] = st
    ck['last_note_t'] = now
    return st


def clock_start(W, cfg, now):
    ck = W['clock']
    ck['t_ref'] = now
    ck['step_ref'] = 0
    ck['phase_ref'] = 0
    ck['start_t'] = now
    for s in (1, 2):
        d = W['det'][s]
        d['hist'] = {}
        d['phase'] = 0
        d['miss'] = []
    W['cycle']['idx'] = None
    W['aviso'] = 'START: patterns en el paso 1'


def clock_stop(W, now):
    W['clock']['stop_t'] = now


def _pair_score(hist, steps, L):
    agree = tot = 0
    for st in steps:
        o = hist.get(st + L)
        if o is not None:
            tot += 1
            if o == hist[st]:
                agree += 1
    return agree, tot


def estimate_period(hist, lmin=4, lmax=64, min_pairs=8, thr=0.9):
    """Periodo mas corto con el que se repiten las notas. Solo compara
    pasos que han sonado (tolera la probabilidad). Antes de dar por buena
    una longitud L espera a poder comprobar 2L: asi un pattern de 16 cuyas
    mitades se parecen no se confunde con uno de 8."""
    if len(hist) < min_pairs + 2:
        return None
    steps = sorted(hist)
    res = {}
    for L in range(max(1, lmin), lmax + 1):
        a, t = _pair_score(hist, steps, L)
        if t >= max(min_pairs, L // 4):
            res[L] = (a / float(t), t)
    if not res:
        return None
    best = max(v[0] for v in res.values())
    if best < thr:
        return None
    for L in sorted(res):
        sc, t = res[L]
        if sc >= thr and sc >= best - 0.02:
            if 2 * L <= lmax and 2 * L not in res:
                return None                      # falta ver dos vueltas
            return L, sc, t
    return None


def _fingerprint(hist, L, phase):
    fp = [None] * L
    for st in sorted(hist):
        fp[(st - phase) % L] = hist[st]
    return fp


def _lib_add(W, s, L, fp):
    lib = W['lib'][s]
    for e in lib:
        if e['L'] == L and _fp_equiv(e['fp'], fp):
            e['fp'] = [b if b is not None else a for a, b in zip(e['fp'], fp)]
            return
    lib.append(dict(L=L, fp=list(fp)))
    del lib[:-16]


def _fp_equiv(a, b):
    L = len(a)
    for rot in range(L):
        ok = True
        both = 0
        for k in range(L):
            x, y = a[k], b[(k + rot) % L]
            if x is not None and y is not None:
                both += 1
                if x != y:
                    ok = False
                    break
        if ok and both >= max(3, L // 3):
            return True
    return False


def lib_match(W, s, recent):
    """recent: [(paso, nota)] de las ultimas notas. Devuelve (L, fp, fase)
    si exactamente un pattern de la biblioteca encaja."""
    if len(recent) < 3:
        return None
    found = []
    for e in W['lib'][s]:
        L, fp = e['L'], e['fp']
        for rot in range(L):
            if all(fp[(st + rot) % L] == nt for st, nt in recent):
                found.append((L, fp, (-rot) % L))
                break
    if len(found) == 1:
        return found[0]
    return None


def det_note(W, cfg, s, note, st):
    d = W['det'][s]
    d['hist'][st] = note
    for k in [k for k in d['hist'] if k < st - 256]:
        del d['hist'][k]
    d['since'] += 1
    if cfg['long_fija']:
        d['L'], d['src'] = int(cfg['long_manual']), 'manual'
        if not d['fp'] or len(d['fp']) != d['L']:
            d['fp'] = [None] * d['L']
            d['phase'] = W['clock']['phase_ref']
    if d['L']:
        L = d['L']
        pos = (st - d['phase']) % L
        exp = d['fp'][pos]
        if exp is not None:
            d['miss'].append(1 if exp != note else 0)
            d['miss'] = d['miss'][-8:]
        d['fp'][pos] = note
        if cfg['long_fija']:
            return
        if len(d['miss']) >= 6 and sum(d['miss']) >= 4:
            pattern_change(W, cfg, s, st, 'las notas ya no encajan')
            return
        if d['since'] % 16 == 0:                 # revision periodica
            est = estimate_period(d['hist'], lmin=int(cfg['long_min']))
            if est and est[0] != L and est[1] >= 0.95:
                d['L'] = est[0]
                d['fp'] = _fingerprint(d['hist'], est[0], d['phase'])
                d['src'], d['score'], d['miss'] = 'escucha', est[1], []
                _lib_add(W, s, est[0], d['fp'])
                W['aviso'] = 'SEQ%d: corregido a %d pasos' % (s, est[0])
        return
    recent = sorted(d['hist'].items())[-3:]
    if d['since'] >= 3:
        m = lib_match(W, s, recent)
        if m:
            d['L'], d['fp'], d['phase'] = m[0], list(m[1]), m[2]
            d['src'], d['score'], d['miss'] = 'biblioteca', 1.0, []
            W['aviso'] = 'SEQ%d: pattern reconocido (%d pasos)' % (s, m[0])
            return
    est = estimate_period(d['hist'], lmin=int(cfg['long_min']))
    if est:
        L, score, tot = est
        phase = W['clock']['phase_ref'] if d['phase'] is None else d['phase']
        d['L'], d['phase'] = L, phase
        d['fp'] = _fingerprint(d['hist'], L, phase)
        d['src'], d['score'], d['miss'] = 'escucha', score, []
        _lib_add(W, s, L, d['fp'])
        W['aviso'] = 'SEQ%d: pattern de %d pasos (%d%%)' % (s, L, int(score * 100))


def pattern_change(W, cfg, s, st, reason):
    d = W['det'][s]
    keep = sorted(d['hist'].items())[-3:] if st is not None else []
    d['hist'] = dict(keep)
    d['L'], d['fp'], d['src'], d['miss'], d['since'] = None, None, '', [], len(keep)
    bar = max(1, int(cfg['steps_per_bar']))
    ref = st if st is not None else W['clock']['step_ref']
    d['phase'] = (int(ref) // bar) * bar
    W['aviso'] = 'SEQ%d: cambio de pattern (%s)' % (s, reason)
    W['cycle']['idx'] = None


def on_cc(W, cfg, ch, num, val, now):
    if num != 123:
        return
    b = W['burst']
    b['times'] = [x for x in b['times'] if now - x[0] < 0.12] + [(now, ch)]
    if b['pending'] is None and len(set(c for _, c in b['times'])) >= 8:
        b['pending'] = now


def _resolve_burst(W, cfg, now, playing):
    b = W['burst']
    if b['pending'] is None or now - b['pending'] < 0.3:
        return None
    t = b['pending']
    b['pending'] = None
    b['times'] = []
    stop = abs(W['clock']['stop_t'] - t) < 0.5 or not playing
    if stop:
        W['aviso'] = 'All Notes Off junto a un STOP'
        return 'stop'
    for s in (1, 2):
        pattern_change(W, cfg, s, None, 'All Notes Off')
    W['aviso'] = 'All Notes Off sin STOP: cambio de pattern'
    return 'cambio'


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def cycle_lengths(W, cfg):
    L1 = W['det'][1]['L']
    L2 = W['det'][2]['L'] if cfg['nivel'] >= 5 else None
    known = [L for L in (L1, L2) if L]
    if not known:
        known = [int(cfg['long_manual'])]
    longest = max(known)
    if cfg['cycle_mode'] == 1 and L1 and L2:
        steps = L1 * L2 // _gcd(L1, L2)
    else:
        steps = int(cfg['reps']) * longest
    steps = max(1, min(4096, steps))
    s_long = 1 if (L1 or 0) >= (L2 or 0) else 2
    anchor = W['det'][s_long]['phase'] if W['det'][s_long]['L'] else W['clock']['phase_ref']
    return steps, int(anchor or 0)


def clock_running(W, cfg, now, tempo, playing):
    ck = W['clock']
    if not playing or ck['t_ref'] is None:
        return False
    if ck['stop_t'] > ck['last_note_t']:
        return False
    # sin notas durante 4 compases: el secuenciador esta parado
    return now - ck['last_note_t'] < 4 * cfg['steps_per_bar'] * step_dur(cfg, tempo)


def cycle_tick(W, cfg, now, tempo, playing):
    """Devuelve True si acaba de terminar un ciclo de ecosistema."""
    cy = W['cycle']
    steps, anchor = cycle_lengths(W, cfg)
    if steps != cy['steps'] or anchor != cy['anchor']:
        cy['steps'], cy['anchor'] = steps, anchor
        cy['idx'] = None
    if not clock_running(W, cfg, now, tempo, playing):
        return False
    st = step_at(W, cfg, now, tempo)
    k = int(math.floor((st - anchor) / float(steps)))
    cy['pos'] = ((st - anchor) % steps)
    if cy['idx'] is None:
        cy['idx'] = k
        return False
    if k > cy['idx']:
        cy['idx'] = k
        return True
    return False


# -----------------------------------------------------------------------------
# 1. NUCLEO - erosion y cortes (fases 7 y 9)
# -----------------------------------------------------------------------------

def pick_target(W, cfg, pad, vel):
    mode = int(cfg['target_mode'])
    l1, l2 = W['last'].get(1), W['last'].get(2)
    if mode == 3 or (l1 is None and l2 is None):
        return min(N - 1, int(vel) * N // 128)
    if mode == 0:
        src = l1 or l2
    elif mode == 1:
        src = l2 or l1
    else:
        src = (l1 or l2) if pad % 2 == 0 else (l2 or l1)
    c, r = colrow(src['cell'])
    return idx((c + int(vel) % 3 - 1) % COLS, r)


def degrade(W, cfg, i, k):
    """Quita k unidades de ocupacion en orden inverso a la promocion:
    primero satelites, luego altura, al final la huella."""
    removed = 0
    for _ in range(int(k)):
        sats = satellites_of(W, i)
        if sats:
            j = max(sats, key=lambda x: W['occ'][x])
            W['occ'][j] -= 1
            W['h'][j] = min(W['h'][j], height_for(cfg, W['occ'][j]) * cfg['sat_limit'])
            if W['occ'][j] <= 0:
                _clear_cell(W, j)
            removed += 1
        elif W['occ'][i] > 1:
            W['occ'][i] -= 1
            cap = height_for(cfg, W['occ'][i])
            if W['par'][i] >= 0:
                cap *= cfg['sat_limit']
            W['h'][i] = min(W['h'][i], cap)
            removed += 1
        elif W['occ'][i] == 1:
            was_sat = W['par'][i] >= 0
            _clear_cell(W, i)
            if not was_sat:
                W['huella'][i] = max(W['t'] or 0.0, 1e-3)
            removed += 1
        else:
            break
    return removed


def erosion(W, cfg, pad, vel, now):
    perf = cfg['perfiles']
    pad = int(pad) % len(perf)
    red, rad, depth = perf[pad]
    target = pick_target(W, cfg, pad, vel)
    dens = occupied(W) / float(N)
    over = dens > cfg['dens_umbral']
    rad_eff = max(1, int(round(rad * cfg['rad_mult']))) if over else int(rad)
    removed = 0
    W['t'] = W['t'] if W['t'] is not None else now
    for c, _ in rings(target, rad_eff):
        removed += degrade(W, cfg, c, red)
    W['hits'][3] = W['hits'].get(3, 0) + 1
    ev = dict(pad=pad, red=red, rad=rad_eff, prof=depth, celda=target, dens=dens,
              doble=over, quitado=removed, t=now)
    W['ev']['erosion'] = ev
    if cfg['nivel'] >= 9:
        if depth > 0:
            ev['corte'] = cut(W, cfg, target, depth, rad, now)
        W['flash'] = dict(t=now, cell=target, k=1.0 if depth > 0 else 0.35)
    return ev


def _top_removed(W, c):
    k = 0
    for sh in reversed(W['shells']):
        if sh['rm'][c]:
            k += 1
        else:
            break
    return k


def cut(W, cfg, target, depth, rad, now):
    ns = n_shells(W)
    if ns == 0:
        return 0
    cells = []
    deepest = 0
    for c, d in rings(target, rad):
        dd = min(int(depth) - d, ns)
        if dd <= 0:
            continue
        for s in range(ns - dd, ns):
            W['shells'][s]['rm'][c] = 1
        W['hueco'][c] = _top_removed(W, c)
        _clear_cell(W, c)
        W['huella'][c] = 0.0
        for j in NEIGH[c]:
            if W['par'][j] == c:
                W['par'][j] = -1
        cells.append(c)
        deepest = max(deepest, W['hueco'][c])
    # cicatrices: suelo del corte y paredes que han quedado al aire
    for c in cells:
        h = W['hueco'][c]
        floor = ns - 1 - h
        if floor >= 0:
            W['scars'][floor * 1000 + c] = now
        for j in NEIGH[c]:
            for s in range(ns - h, ns):
                if not W['shells'][s]['rm'][j]:
                    W['scars'][s * 1000 + j] = now
    W['dirty'] = True
    W['ev']['corte'] = dict(celda=target, conchas=deepest, celdas=len(cells), t=now)
    return deepest


# -----------------------------------------------------------------------------
# 1. NUCLEO - conchas (fase 8)
# -----------------------------------------------------------------------------

MINERAL = [
    (0.55, 0.36, 0.16),    # ambar de la base
    (0.40, 0.39, 0.37),
    (0.17, 0.17, 0.18),
    (0.47, 0.31, 0.16),
    (0.29, 0.29, 0.28),
    (0.10, 0.10, 0.11),
    (0.36, 0.32, 0.26),
    (0.23, 0.22, 0.24),
]


def shell_color(gen):
    return MINERAL[int(gen) % len(MINERAL)]


def end_cycle(W, cfg, now):
    W['cycle']['count'] += 1
    W['cycle']['last_t'] = now
    if cfg['nivel'] < 8:
        W['ev']['ciclo'] = dict(t=now, n=W['cycle']['count'])
        return False
    W['shells'].append(dict(gen=W['gen'], col=list(shell_color(W['gen'])),
                            occ=list(W['occ']), sp=list(W['sp']), rm=[0] * N))
    W['gen'] += 1
    her = cfg['herencia']
    for i in range(N):
        x = W['occ'][i] * her + W['resto'][i]
        n = int(math.floor(x + 1e-9))
        W['resto'][i] = x - n
        if n > 0 and W['own'][i]:
            W['occ'][i] = n
            W['h'][i] = height_for(cfg, n)
            W['par'][i] = -1
            W['traza'][i] = _bit(W['own'][i]) | (3 if W['sp'][i] == HIB else 0)
        else:
            W['occ'][i] = 0
            W['h'][i] = 0.0
            W['par'][i] = -1
        W['vh'][i] = 0.0           # lo heredado vuelve a brotar de la superficie
        W['huella'][i] = 0.0
        W['hueco'][i] = 0
    W['pend'] = {}
    W['dirty'] = True
    W['ev']['ciclo'] = dict(t=now, n=W['cycle']['count'])
    return True


def continents(W, last=8, thr=0.5):
    sh = W['shells'][-last:]
    if len(sh) < 2:
        return 0
    persist = [sum(1 for s in sh if s['occ'][c] > 0) / float(len(sh)) for c in range(N)]
    cells = set(c for c in range(N) if persist[c] >= thr)
    count = 0
    while cells:
        count += 1
        stack = [cells.pop()]
        while stack:
            c = stack.pop()
            for n in NEIGH[c]:
                if n in cells:
                    cells.discard(n)
                    stack.append(n)
    return count


# -----------------------------------------------------------------------------
# 1. NUCLEO - avance por fotograma
# -----------------------------------------------------------------------------

def tick(W, cfg, now, tempo=120.0, playing=True):
    last = W['t']
    dt = 0.0 if last is None else max(0.0, min(0.25, now - last))
    W['t'] = now
    a = 1.0 - math.exp(-dt / 0.12) if dt > 0 else 0.0
    for i in range(N):
        h, vh = W['h'][i], W['vh'][i]
        if vh != h:
            vh += (h - vh) * a
            if abs(h - vh) < 1e-4:
                vh = h
            W['vh'][i] = vh
        if W['occ'][i] == 0 and vh < 0.01:
            W['vh'][i] = 0.0
            if W['sp'][i]:
                W['sp'][i] = W['own'][i] = W['traza'][i] = 0
    out = dict(ciclo=False, burst=None)
    if cfg['nivel'] >= 9 and W['scars']:
        st = cfg['scar_time']
        for k in [k for k, t0 in W['scars'].items() if now - t0 > st]:
            del W['scars'][k]
        W['dirty'] = True
    if cfg['nivel'] >= 6:
        out['burst'] = _resolve_burst(W, cfg, now, playing)
        if cycle_tick(W, cfg, now, tempo, playing):
            end_cycle(W, cfg, now)
            out['ciclo'] = True
    return out


# -----------------------------------------------------------------------------
# 1. NUCLEO - instancias para dibujar
# -----------------------------------------------------------------------------

def _cell_sizes(r, row):
    _, phi = cell_angles(0, row)
    cw = 2.0 * math.pi * r * math.cos(phi) / COLS
    cl = math.pi * LAT_SPAN * r / ROWS
    return cw, cl


def _row(p, n, sx, sy, sz, col):
    rx, ry = orient(n)
    return [p[0], p[1], p[2], rx, ry, 0.0, sx, sy, sz, col[0], col[1], col[2]]


def _tint(col, k):
    return (min(1.0, col[0] * k), min(1.0, col[1] * k), min(1.0, col[2] * k))


def _mix(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


COL_GEO = (0.62, 0.60, 0.56)
COL_ARQ = (0.34, 0.36, 0.40)
COL_HUELLA = (0.13, 0.09, 0.06)
COL_CROWN = (1.00, 0.70, 0.30)
COL_SCAR = (0.10, 0.90, 1.00)


def _geo_pieces(W, cfg, i, p0, n, vh, cl, scale, col, out):
    e, t = tangents(n)
    occ = max(1, W['occ'][i])
    count = 1 + (1 if occ >= 2 else 0) + (1 if occ >= 3 else 0)
    if W['par'][i] >= 0:
        count = 1
    hk = (1.0, 0.62, 0.40)
    wk = (0.36, 0.26, 0.20)
    main_dir, main_top = n, p0
    for k in range(count):
        u1, u2, u3, u4 = (_hash01(i, k, q) for q in (1, 2, 3, 4))
        off = (0.0, 0.0) if k == 0 else ((u1 - 0.5) * 0.7 * cl, (u2 - 0.5) * 0.7 * cl)
        lean = 0.10 + 0.25 * u3
        d = _norm(_add(_add(n, e, lean * (u4 - 0.5) * 2), t, lean * (u1 - 0.5) * 2))
        p = _add(_add(p0, e, off[0]), t, off[1])
        w = wk[k] * cl * scale * (0.8 + 0.4 * u2)
        hh = vh * hk[k]
        out.append(_row(p, d, w, hh, w * (0.7 + 0.5 * u3), _tint(col, 0.9 + 0.2 * u4)))
        if k == 0:
            main_dir, main_top = d, _add(p, d, hh)
    return main_dir, main_top


def _arq_pieces(W, cfg, i, p0, n, vh, cl, scale, col, out):
    lim = limit(cfg)
    floor_h = 0.25 * lim
    w = 0.48 * cl * scale
    k = 0
    while k * floor_h < vh - 1e-4 and k < 32:
        hh = min(floor_h, vh - k * floor_h) * 0.86
        p = _add(p0, n, k * floor_h)
        out.append(_row(p, n, w, hh, w, _tint(col, 0.95 + 0.08 * (k % 2))))
        k += 1
    return n, _add(p0, n, vh)


def build_instances(W, cfg, now, hide_beacons=False, tiles=True):
    lvl = cfg['nivel']
    lim = limit(cfg)
    out = dict(formas_pulidas=[], formas_porosas=[], coronas=[], estratos=[], baliza2=[])
    R = top_radius(W, cfg)
    for i in range(N):
        vh = W['vh'][i]
        own = W['own'][i]
        c, r = colrow(i)
        n = normal_i(i)
        base = base_radius(W, cfg, i)
        p0 = _mul(n, base)
        cw, cl = _cell_sizes(base, r)
        if vh <= 0.005 or not own:
            if lvl >= 7 and W['huella'][i] > 0 and W['occ'][i] == 0:
                out['formas_porosas'].append(
                    _row(_add(p0, n, 0.01), n, 0.45 * cl, 0.03, 0.45 * cl, COL_HUELLA))
            continue
        pulido = W['vel'][i] >= cfg['vel_umbral']
        lst = out['formas_pulidas'] if pulido else out['formas_porosas']
        sat = W['par'][i] >= 0
        scale = cfg['sat_size'] if sat else 1.0
        base_col = COL_GEO if own == GEO else COL_ARQ
        col = _tint(base_col, 1.15 if pulido else 0.9)
        if sat:
            col = _tint(col, 0.85)
        if own == GEO:
            d, top = _geo_pieces(W, cfg, i, p0, n, vh, cl, scale, col, lst)
        else:
            d, top = _arq_pieces(W, cfg, i, p0, n, vh, cl, scale, col, lst)
        e, t = tangents(n)
        # hibridos: la otra especie deja su rastro
        if W['sp'][i] == HIB:
            if own == GEO:          # macizo aterrazado
                for k in range(2):
                    hh = 0.10 * lim
                    p = _add(p0, n, (0.15 + 0.3 * k) * vh)
                    ww = (0.48 - 0.14 * k) * cl * scale
                    lst.append(_row(p, n, ww, hh, ww, _tint(COL_ARQ, 1.1)))
            else:                   # torre mineralizada
                for k, side in enumerate((1.0, -1.0)):
                    p = _add(_add(p0, n, (0.3 + 0.25 * k) * vh), e, side * 0.17 * cl * scale)
                    dd = _norm(_add(n, e, side * 0.9))
                    ww = 0.07 * cl * scale
                    lst.append(_row(p, dd, ww, 0.35 * vh, ww, _tint(COL_GEO, 1.05)))
        if lvl >= 4:
            o = W['occ'][i]
            fused = (not sat and o >= cfg['th_fusion']) or \
                    (sat and W['occ'][W['par'][i]] >= cfg['th_fusion'])
            if fused:
                kk = 0.80 if not sat else 0.70
                lst.append(_row(p0, n, kk * cw, 0.30 * lim, kk * cl, _tint(base_col, 0.7)))
            if not sat and o >= cfg['th_crown']:
                if own == GEO:
                    out['coronas'].append(_row(top, d, 0.06 * cl, 0.70 * lim, 0.06 * cl, COL_CROWN))
                else:
                    out['coronas'].append(_row(top, n, 0.03 * cl, 0.90 * lim, 0.03 * cl, COL_CROWN))
                    out['coronas'].append(_row(top, n, 0.20 * cl, 0.05 * lim, 0.20 * cl, COL_CROWN))
    if lvl >= 5 and not hide_beacons:
        b = beacon(W, cfg, 2, now)
        if b:
            p, rad = b
            out['baliza2'].append([p[0], p[1], p[2], 0, 0, 0, rad, rad, rad, 1, 0.7, 0.3])
    if lvl >= 8 and tiles:
        out['estratos'] = build_tiles(W, cfg, now)
    return out


def build_tiles(W, cfg, now):
    rows = []
    th = cfg['shell_thick']
    ns = n_shells(W)
    first = max(0, ns - int(cfg['max_shells']))
    st = cfg['scar_time']
    for s in range(first, ns):
        sh = W['shells'][s]
        r_mid = cfg['core_radius'] + (s + 0.5) * th
        base_col = sh['col']
        for c in range(N):
            if sh['rm'][c]:
                continue
            col_i, row_i = colrow(c)
            n = normal_i(c)
            cw, cl = _cell_sizes(r_mid, row_i)
            col = _tint(base_col, 0.75 + 0.35 * min(1.0, sh['occ'][c] / 4.0))
            t0 = W['scars'].get(s * 1000 + c)
            if t0 is not None:
                col = _mix(COL_SCAR, col, max(0.0, min(1.0, (now - t0) / st)))
            rows.append(_row(_mul(n, r_mid - th * 0.5), n, cw * 1.04, th * 0.98, cl * 1.04, col))
        # casquetes polares
        cap = 2.0 * r_mid * math.sin(math.radians(90.0 * (1 - LAT_SPAN) + 0.5)) * 1.15
        for pole in ((0.0, 1.0, 0.0), (0.0, -1.0, 0.0)):
            rows.append(_row(_mul(pole, r_mid - th * 0.5), pole, cap, th * 0.98, cap,
                             _tint(base_col, 0.8)))
    return rows


def beacon(W, cfg, s, now, base_radius_=0.9, peak=1.8, decay=0.12, lift=0.3):
    last = W['last'].get(s)
    if not last:
        return None
    i = last['cell']
    env = math.exp(-max(0.0, now - W['hit_t'].get(s, -99.0)) / decay)
    rad = (base_radius_ + peak * env) * (0.55 if s == 2 else 1.0)
    n = normal_i(i)
    d = base_radius(W, cfg, i) + W['vh'][i] + lift + rad
    return _mul(n, d), rad


def world_dir(v, angle_deg, tilt_deg, wobble_deg=0.0):
    """Direccion de la celda en el mundo, con el giro del planeta aplicado.
    Orden de rotacion de las geometrias del planeta: Ry Rx Rz
    (ry = giro, rx = balanceo del eje, rz = inclinacion)."""
    a, t, w = math.radians(angle_deg), math.radians(tilt_deg), math.radians(wobble_deg)
    x, y, z = v
    x, z = x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a)
    y, z = y * math.cos(w) - z * math.sin(w), y * math.sin(w) + z * math.cos(w)
    x, y = x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)
    return (x, y, z)


def wobble_step(st, dt, on, paused, amp, period, fade=3.0):
    """Avanza el balanceo del eje. st = {'ph': fase 0-1, 'env': 0-1}.
    La fase se acumula (cambiar el periodo no hace saltar el planeta) y se
    congela con Pausa. Al encender o apagar, la amplitud entra o sale en
    'fade' segundos con curva suave. Devuelve los grados de rx."""
    dt = max(0.0, min(0.25, dt))
    period = max(5.0, period)
    if not paused:
        st['ph'] = (st.get('ph', 0.0) + dt / period) % 1.0
    env = st.get('env', 0.0) + (1.0 if on else -1.0) * dt / fade
    env = max(0.0, min(1.0, env))
    st['env'] = env
    s = env * env * (3 - 2 * env)
    return s * amp * math.sin(2 * math.pi * st['ph'])


# =============================================================================
# 2. ADAPTADOR TOUCHDESIGNER
# =============================================================================
# Todo lo de aqui abajo usa op(), parent(), me y absTime: solo funciona
# dentro de TouchDesigner.

_CACHE = {'frame': None, 'inst': None, 'printed': {}}

CHOP_NAMES = ['i_formas_pulidas', 'i_formas_porosas', 'i_coronas',
              'i_estratos', 'i_baliza2']

TARGET_MODES = ['seq1', 'seq2', 'alterna', 'velocidad']


def _p(name, default):
    try:
        p = getattr(parent().par, name, None)
        if p is None:
            return default
        v = p.eval()
        if isinstance(default, bool):
            return bool(v)
        if isinstance(default, int):
            if isinstance(v, str):
                return v
            return int(v)
        if isinstance(default, float):
            return float(v)
        return v
    except Exception:
        return default


def _menu(name, options, default):
    v = _p(name, options[default])
    if isinstance(v, str):
        return options.index(v) if v in options else default
    try:
        return int(v)
    except Exception:
        return default


def _perfiles():
    t = parent().op('perfiles_erosion')
    if t is None or t.numRows < 2:
        return PERFILES_DEFECTO
    out = []
    for r in range(1, min(t.numRows, 9)):
        try:
            out.append((int(float(t[r, 'reduccion'].val)), int(float(t[r, 'radio'].val)),
                         int(float(t[r, 'profundidad'].val))))
        except Exception:
            out.append(PERFILES_DEFECTO[r - 1])
    while len(out) < 8:
        out.append(PERFILES_DEFECTO[len(out)])
    return out


def cfg():
    c = dict(DEFAULT_CFG)
    c.update(
        nivel=_p('Nivel', 3),
        shell_thick=_p('Shellthick', c['shell_thick']),
        height_factor=_p('Alturafactor', c['height_factor']),
        seed_frac=_p('Semillafrac', c['seed_frac']),
        grow_frac=_p('Growstep', c['grow_frac']),
        gate_mode=int(_p('Gatemode', True)),
        vel_umbral=_p('Umbralvel', c['vel_umbral']),
        th_branch=_p('Umbralram', c['th_branch']),
        th_fusion=_p('Umbralfusion', c['th_fusion']),
        th_crown=_p('Umbralcorona', c['th_crown']),
        sat_size=_p('Tamsatelite', c['sat_size']),
        sat_limit=_p('Limsatelite', c['sat_limit']),
        neigh_mode=_menu('Vecina', ['velocidad', 'velocidadocupacion'], 1),
        reps=_p('Repsporciclo', c['reps']),
        cycle_mode=_menu('Modociclo', ['repeticiones', 'hiperperiodo'], 0),
        long_manual=_p('Longmanual', c['long_manual']),
        long_min=_p('Longmin', c['long_min']),
        long_fija=int(_p('Longfija', False)),
        steps_per_bar=_p('Pasosporcompas', c['steps_per_bar']),
        steps_per_beat=_p('Pasospornegra', c['steps_per_beat']),
        turn_auto=int(_p('Turnauto', True)),
        dens_umbral=_p('Umbraldensidad', c['dens_umbral']),
        rad_mult=_p('Multradio', c['rad_mult']),
        target_mode=_menu('Objetivo', TARGET_MODES, 2),
        herencia=_p('Herencia', c['herencia']),
        max_shells=_p('Maxconchas', c['max_shells']),
        scar_time=max(0.1, _p('Cicatriz', c['scar_time'])),
        flash=_p('Destello', c['flash']),
    )
    if c['nivel'] >= 7:
        c['perfiles'] = _perfiles()
    return c


def world():
    W = me.fetch('W', None)
    if W is None:
        W = new_world()
        me.store('W', W)
    return ensure(W)


def reset_world():
    me.store('W', new_world())
    _CACHE['inst'] = None
    _CACHE['tiles'] = None
    _CACHE['frame'] = None


def _ritmo():
    return parent().op('ritmo').module


def tempo():
    try:
        return _ritmo().tempo()
    except Exception:
        return 120.0


def playing():
    try:
        return _ritmo().playing()
    except Exception:
        return True


def surface_radius(frame=None):
    return top_radius(world(), cfg())


def nucleo_radius(frame=None):
    W, c = world(), cfg()
    hidden = max(0, n_shells(W) - int(c['max_shells']))
    return c['core_radius'] + hidden * c['shell_thick']


def surface_point(note, lift, radius):
    """Punto de la baliza del SEQ1 (lo usa baliza_callbacks)."""
    W, c = world(), cfg()
    i = note_cell(note)
    d = base_radius(W, c, i) + W['vh'][i] + lift + radius
    return _mul(normal_i(i), d)


def performance():
    return bool(_p('Modoactuacion', False))


# --- MIDI --------------------------------------------------------------------

def _log(row):
    t = parent().op('midi_log')
    if t is None:
        return
    t.appendRow([str(v) for v in row])
    while t.numRows > 41:
        t.deleteRow(1)


def _say(key, text):
    n = _CACHE['printed'].get(key, 0)
    if n < 8:
        print(text)
        _CACHE['printed'][key] = n + 1


def _seq1_beacon(note):
    try:
        parent().par.Nota = int(note)
    except Exception:
        pass
    b = parent().op('baliza_chop')
    if b is not None:
        b.store('hit_t', absTime.seconds)
        b.store('hits', b.fetch('hits', 0) + 1)


def midi_note_on(ch, note, vel):
    c = cfg()
    lvl = c['nivel']
    now = absTime.seconds
    ch1 = _p('Canal', 13)
    filt = _p('Filtrar', True)
    W = world()
    if (not filt) or ch == ch1:
        _seq1_beacon(note)
        r = note_on(W, c, GEO, note, vel, now, tempo())
        res = 'SEQ1 %s' % r['estado']
    elif lvl >= 5 and ch == _p('Canal2', 14):
        r = note_on(W, c, ARQ, note, vel, now, tempo())
        res = 'SEQ2 %s' % r['estado']
    elif lvl >= 7 and ch == _p('Canaldrum', 10):
        pad = int(note) - _p('Notabase', 36)
        if 0 <= pad < 8:
            ev = erosion(W, c, pad, vel, now)
            res = 'EROSION pad %d celda %d' % (pad + 1, ev['celda'])
        else:
            res = 'ignorado: pad fuera de 1-8'
    else:
        res = 'ignorado: canal %s' % ch
    _log([absTime.frame, ch, note, vel, res])
    _say('n%s' % ch, 'MIDI  canal %s  nota %s  vel %s  ->  %s' % (ch, note, vel, res))
    return res


def midi_note_off(ch, note):
    c = cfg()
    W = world()
    s = None
    if (not _p('Filtrar', True)) or ch == _p('Canal', 13):
        s = GEO
    elif c['nivel'] >= 5 and ch == _p('Canal2', 14):
        s = ARQ
    if s:
        note_off(W, c, s, note, absTime.seconds, tempo())


def midi_cc(ch, num, val):
    c = cfg()
    if c['nivel'] >= 6:
        on_cc(world(), c, ch, num, val, absTime.seconds)


def midi_start():
    if cfg()['nivel'] >= 6:
        clock_start(world(), cfg(), absTime.seconds)
        print('MIDI  START: patterns en el paso 1')


def midi_stop():
    clock_stop(world(), absTime.seconds)


def midi_sysex(b):
    # MMC: F0 7F 7F 06 01 F7 = stop, 02 = play
    if len(b) >= 6 and b[0] == 0xF0 and b[1] == 0x7F and b[3] == 0x06:
        if b[4] == 0x01:
            midi_stop()
        elif b[4] == 0x02:
            midi_start()


# --- fotograma ---------------------------------------------------------------

def frame_tick():
    W, c = world(), cfg()
    now = absTime.seconds
    res = tick(W, c, now, tempo(), playing())
    if res.get('burst'):
        print('AVISO  %s' % W['aviso'])
    if res.get('ciclo'):
        print('CICLO  %d terminado%s' % (W['cycle']['count'],
                                         ' -> concha %d' % n_shells(W) if c['nivel'] >= 8 else ''))
    if c['nivel'] >= 6 and c['turn_auto']:
        bars = W['cycle']['steps'] / float(max(1, c['steps_per_bar']))
        try:
            if bars > 0 and abs(float(parent().par.Barsperturn) - bars) > 1e-6:
                parent().par.Barsperturn = bars
        except Exception:
            pass
    dirty = W.get('dirty', True) or _CACHE.get('tiles') is None
    inst = build_instances(W, c, now, hide_beacons=performance(), tiles=dirty)
    if dirty:
        _CACHE['tiles'] = inst['estratos']
    else:
        inst['estratos'] = _CACHE['tiles']
    _CACHE['inst'] = inst
    _CACHE['frame'] = absTime.frame
    for name in CHOP_NAMES:
        o = parent().op(name)
        if o is None:
            continue
        if name == 'i_estratos' and not dirty:
            continue
        o.cook(force=True)
    if dirty or _CACHE.get('ret_R') != top_radius(W, c):
        _CACHE['ret_R'] = top_radius(W, c)
        o = parent().op('reticula_chop')
        if o is not None:
            o.cook(force=True)
    W['dirty'] = False


def instance_rows(chop_name):
    if _CACHE['inst'] is None:
        W, c = world(), cfg()
        _CACHE['inst'] = build_instances(W, c, absTime.seconds, hide_beacons=performance())
    key = chop_name[2:] if chop_name.startswith('i_') else chop_name
    return _CACHE['inst'].get(key, [])


# --- pulsos de los parametros ------------------------------------------------

def on_pulse(name):
    W, c = world(), cfg()
    now = absTime.seconds
    if name == 'Sembrar':
        note = _p('Nota', 60)
        _seq1_beacon(note)
        r = note_on(W, c, GEO, note, _p('Velprueba', 100), now, tempo())
        print('SEMBRAR  %s -> celda %d  ocupacion %d  (%s)'
              % (note_name(note), r['celda'], W['occ'][r['celda']], r['estado']))
    elif name == 'Sembrar2':
        note = _p('Nota2', 60)
        r = note_on(W, c, ARQ, note, _p('Velprueba', 100), now, tempo())
        print('SEMBRAR2 %s -> celda %d  ocupacion %d  (%s)'
              % (note_name(note), r['celda'], W['occ'][r['celda']], r['estado']))
    elif name == 'Erosionar':
        ev = erosion(W, c, _p('Padprueba', 1) - 1, _p('Velprueba', 100), now)
        print('EROSION  pad %d -> celda %d, radio %d, quitado %d'
              % (ev['pad'] + 1, ev['celda'], ev['rad'], ev['quitado']))
    elif name == 'Forzarciclo':
        end_cycle(W, c, now)
        print('CICLO  forzado: %d%s' % (W['cycle']['count'],
                                       '  conchas %d' % n_shells(W) if c['nivel'] >= 8 else ''))
    elif name == 'Resetmundo':
        reset_world()
        print('MUNDO  vaciado')
    elif name == 'Resetpatterns':
        for s in (1, 2):
            W['det'][s] = _new_det()
            W['lib'][s] = []
        W['cycle']['idx'] = None
        print('PATTERNS  olvidados')
    W['dirty'] = True


def on_value(name, val):
    if name == 'Modoactuacion':
        try:
            parent().par.Showgrid = not bool(val)
        except Exception:
            pass


# --- balanceo del eje (rotacion extra, desde la fase 3) ----------------------

def wobble(frame=None):
    """Grados de rx de todas las geometrias del planeta. Inclina el eje
    hacia la camara y en contra, para que se vean los dos polos. Ajeno al
    reloj del secuenciador. Pagina Fase3: Rotextra, Balanceo, Balanceoper."""
    if _CACHE.get('wob_frame') == absTime.frame:
        return _CACHE.get('wob', 0.0)
    t = absTime.seconds
    st = _CACHE.setdefault('wob_st', {'ph': 0.0, 'env': 0.0})
    dt = t - _CACHE.get('wob_t', t)
    _CACHE['wob_t'] = t
    v = wobble_step(st, dt, _p('Rotextra', True), _p('Pausa', False),
                    _p('Balanceo', 60.0), _p('Balanceoper', 90.0))
    _CACHE['wob'] = v
    _CACHE['wob_frame'] = absTime.frame
    return v


# --- luz de destello y camara (fases 9 y 10) ---------------------------------

def flash_light():
    """(x, y, z, dimmer) de la luz de destello."""
    W, c = world(), cfg()
    f = W.get('flash')
    if not f or c['nivel'] < 9:
        return (0.0, 0.0, 0.0, 0.0)
    env = math.exp(-max(0.0, absTime.seconds - f['t']) / 0.25) * f['k']
    try:
        ang = _ritmo().rotation(absTime.frame)
        tilt = float(parent().par.Tilt)
    except Exception:
        ang, tilt = 0.0, 0.0
    v = world_dir(normal_i(f['cell']), ang, tilt, wobble())
    d = top_radius(W, c) + 4.0
    return (v[0] * d, v[1] * d, v[2] * d, c['flash'] * env)


def flash_value(k, frame=None):
    return flash_light()[k]


def camera_state():
    if _CACHE.get('cam_frame') == absTime.frame:
        return _CACHE['cam']
    R = surface_radius()
    t = absTime.seconds
    h = _p('Camaltura', 4.0)
    vel = _p('Camvel', 0.6)
    final = _p('Planofinal', False)
    fb = _CACHE.get('cam_final', 0.0)
    last = _CACHE.get('cam_t', t)
    dt = max(0.0, min(0.25, t - last))
    fb += (1.0 if final else -1.0) * dt / 20.0
    fb = max(0.0, min(1.0, fb))
    _CACHE['cam_final'] = fb
    _CACHE['cam_t'] = t
    s = fb * fb * (3 - 2 * fb)
    az = math.radians(vel * t)
    el = math.radians(12.0 + 8.0 * math.sin(t * 0.05))
    def sph(a, e, r):
        return (r * math.cos(e) * math.cos(a), r * math.sin(e), r * math.cos(e) * math.sin(a))
    hh = h + (2.2 * R - h) * s
    pos = sph(az, el, R + hh)
    tgt = sph(az + math.radians(25.0), el - math.radians(6.0), R)
    tgt = _mul(tgt, 1.0 - s)
    st = dict(pos=pos, tgt=tgt, R=R)
    _CACHE['cam'] = st
    _CACHE['cam_frame'] = absTime.frame
    return st


def cam(key, k, frame=None):
    return camera_state()[key][k]


# --- leyenda -----------------------------------------------------------------

def legend(frame=None):
    W, c = world(), cfg()
    lvl = c['nivel']
    lines = ['']
    occ = occupied(W)
    mx = max(W['occ'])
    lines.append('  MUNDO    ocupadas %d/96 (%d%%)   max %d   fase %d'
                 % (occ, int(occ * 100 / 96), mx, lvl))
    u = W['ev'].get('ultima')
    if u:
        lines.append('  ULTIMA   %s celda %d   ocupacion %d   %s'
                     % (SPECIES_NAME.get(u['s'], '?'), u['celda'], u['occ'], u['estado']))
    if lvl >= 4:
        sats = sum(1 for i in range(N) if W['par'][i] >= 0 and W['occ'][i] > 0)
        fus = sum(1 for i in range(N) if W['par'][i] < 0 and W['occ'][i] >= c['th_fusion'])
        cor = sum(1 for i in range(N) if W['par'][i] < 0 and W['occ'][i] >= c['th_crown'])
        d = W['ev'].get('desborde')
        dtxt = '%d -> %d' % (d['de'], d['a']) if d else '-'
        lines.append('  DESBORDE %-9s satelites %d   fusiones %d   coronas %d'
                     % (dtxt, sats, fus, cor))
    if lvl >= 5:
        hib = sum(1 for i in range(N) if W['sp'][i] == HIB)
        lines.append('  SEQ2     canal %d   notas %d   hibridas %d'
                     % (_p('Canal2', 14), W['hits'].get(2, 0), hib))
    if lvl >= 6:
        d1, d2 = W['det'][1], W['det'][2]
        def ltxt(d):
            return '%d pasos (%s)' % (d['L'], d['src']) if d['L'] else 'escuchando'
        cy = W['cycle']
        lines.append('  CICLO    SEQ1 %s   SEQ2 %s' % (ltxt(d1), ltxt(d2)))
        lines.append('           ciclo %d   paso %d/%d'
                     % (cy['count'], int(cy['pos']), cy['steps']))
        if W.get('aviso'):
            lines.append('  AVISO    %s' % W['aviso'])
    if lvl >= 7:
        e = W['ev'].get('erosion')
        dens = occupied(W) / 96.0
        flag = '  x%g' % c['rad_mult'] if dens > c['dens_umbral'] else ''
        if e:
            lines.append('  EROSION  pad %d   -%d   radio %d   celda %d   densidad %d%%%s'
                         % (e['pad'] + 1, e['red'], e['rad'], e['celda'], int(dens * 100), flag))
        else:
            lines.append('  EROSION  -   densidad %d%%%s' % (int(dens * 100), flag))
    if lvl >= 8:
        lines.append('  CONCHAS  %d   radio %.2f   herencia %d%%   continentes %d'
                     % (n_shells(W), top_radius(W, c), int(c['herencia'] * 100), continents(W)))
    if lvl >= 9:
        k = W['ev'].get('corte')
        if k:
            left = max(0.0, c['scar_time'] - (absTime.seconds - k['t']))
            lines.append('  CORTE    celda %d   %d conchas expuestas   cicatriz %.1f s'
                         % (k['celda'], k['conchas'], left))
    return '\n'.join(lines)
