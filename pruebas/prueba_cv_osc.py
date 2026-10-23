"""
Prueba el conversor CV -> OSC sin placa: compila modular/cv_osc/cv_osc.ino en
el ordenador con un Arduino de mentira (modular/prueba_host), como ESP32-S3 y
como Arduino Nano, le mete tensiones con resistencias desviadas un 1 % y
descodifica lo que sale por el USB con modular/puente_osc.py.

    python3 pruebas/prueba_cv_osc.py
"""

import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(REPO, 'modular'))
import puente_osc as P  # noqa: E402


def compilar(nombre, defines):
    exe = os.path.join(tempfile.gettempdir(), 'cv_osc_%s' % nombre)
    cmd = ['g++', '-std=c++17', '-O1', '-Wall', '-Wno-unused-variable', '-I', os.path.join(REPO, 'modular', 'prueba_host'),
           '-x', 'c++', os.path.join(REPO, 'modular', 'prueba_host', 'main.cpp'), '-o', exe] + defines
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit('FALLO  no compila (%s)' % nombre)
    avisos = [l for l in r.stderr.splitlines() if 'warning' in l]
    return exe, avisos


def fases(salida):
    """{fase: [(ruta, args)]} de la salida de la placa."""
    out, f = {0: []}, 0
    for p in P.Slip().feed(salida):
        for ruta, args in P.osc_leer(p):
            if ruta == '/prueba/fase':
                f = int(args[0])
                out[f] = []
            else:
                out[f].append((ruta, args))
    return out


def ultimos(mensajes):
    v = {}
    for ruta, args in mensajes:
        if args and isinstance(args[0], float):
            v[ruta] = args[0]
    return v


def probar(nombre, defines, tol_bruto, tol_cal):
    exe, avisos = compilar(nombre, defines)
    salida = subprocess.run([exe], capture_output=True).stdout
    F = fases(salida)
    bien = True

    def check(texto, cond, detalle=''):
        nonlocal bien
        bien = bien and cond
        print('  %-6s %s%s' % ('OK' if cond else 'FALLO', texto, ('   (' + detalle + ')') if detalle else ''))

    print('== %s%s' % (nombre, '   (%d avisos del compilador)' % len(avisos) if avisos else ''))
    for a in avisos:
        print('         ' + a)
    infos = [a[0] for r, a in F[0] if r == '/estratos/info']
    check('al arrancar dice quien es', any('cv_osc' in x for x in infos))
    n_bundles = sum(1 for p in P.Slip().feed(salida) if p.startswith(b'#bundle'))
    rutas = [r for r, a in F[1] if r.startswith('/estratos/') and r != '/estratos/info']
    check('cada paquete es un bundle con los 8 canales (%d paquetes)' % n_bundles,
          n_bundles > 50 and rutas[:8] == P.RUTAS)
    esperado = [-5.0, 0.0, 2.5, 5.0, 10.0, -10.0, 1.0, 0.0]
    v1 = ultimos(F[1])
    err = max(abs(v1[r] - e) for r, e in zip(P.RUTAS, esperado))
    check('sin calibrar, la tension de entrada en voltios (error max %.2f V)' % err, err < tol_bruto)
    v2 = ultimos(F[2])
    err0 = max(abs(v) for v in v2.values())
    check('tras "cero", 0 V se leen 0 (error %.3f V)' % err0, err0 < tol_cal)
    v3 = ultimos(F[3])
    check('tras "cinco 1", -5 V en el canal 1 se leen -5 (%.3f V)' % v3['/estratos/lfo'],
          abs(v3['/estratos/lfo'] + 5.0) < tol_cal * 2)
    v5 = ultimos(F[5])
    check('"cinco 2 3.3" calibra con la tension medida: 7,5 V se leen %.3f V' % v5['/estratos/ruido'],
          abs(v5['/estratos/ruido'] - 7.5) < tol_cal * 3)
    infos4 = [a[0] for r, a in F[4] if r == '/estratos/info']
    check('"info" manda la calibracion de los 8 canales', len([x for x in infos4 if x.startswith('canal')]) == 8)
    seg = float(next(a[0] for f in F.values() for r, a in f if r == '/prueba/segundos'))
    hz = n_bundles / seg
    check('%d paquetes por segundo' % round(hz), hz > 40)
    return bien


def main():
    ok = probar('ESP32-S3', ['-DESP32', '-DCONFIG_IDF_TARGET_ESP32S3'], 0.3, 0.02)
    ok = probar('ESP32', ['-DESP32'], 0.3, 0.02) and ok
    ok = probar('Arduino Nano', [], 0.3, 0.06) and ok
    # el puente: SLIP con bytes que hay que escapar y el modo de prueba
    p = P.osc_mensaje('/x', 1.0, 'a\xc0b')
    dec = P.Slip().feed(P.slip(p) + P.slip(bytes([0xC0, 0xDB, 1])))
    print('== puente')
    print('  %-6s SLIP con bytes 0xC0 y 0xDB escapados' % ('OK' if dec == [p, bytes([0xC0, 0xDB, 1])] else 'FALLO'))
    s = P.senales_prueba(1.0)
    print('  %-6s senales de prueba en voltios (-5..5)' % ('OK' if all(-5.01 <= v <= 5.01 for v in s) else 'FALLO'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
