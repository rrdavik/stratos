"""
=============================================================================
ESTRATOS - PUENTE USB -> OSC
=============================================================================
La placa del conversor (cv_osc.ino) manda OSC por el USB en paquetes SLIP
(OSC 1.1 por serie). El OSC In CHOP de TouchDesigner solo escucha UDP: este
puente lee el puerto serie y reenvia cada paquete, tal cual, por UDP.

    python3 puente_osc.py                         # busca la placa y manda a 127.0.0.1:9000
    python3 puente_osc.py --serie COM5            # el puerto (Windows: COM5; Mac: /dev/cu.usb...)
    python3 puente_osc.py --ver                   # ademas, enseña los valores
    python3 puente_osc.py --destino 192.168.1.20:9000   # TouchDesigner en otro ordenador
    python3 puente_osc.py --orden cero            # calibra el 0 V (con el puente parado)
    python3 puente_osc.py --orden "cinco 1"       # calibra +5 V en el canal 1
    python3 puente_osc.py --simular               # sin placa: senales de prueba por UDP

Necesita pyserial (pip install pyserial), salvo con --simular.
=============================================================================
"""

import argparse
import math
import socket
import struct
import sys
import time

SLIP_END, SLIP_ESC, SLIP_ESC_END, SLIP_ESC_ESC = 0xC0, 0xDB, 0xDC, 0xDD
RUTAS = ['/estratos/lfo', '/estratos/ruido', '/estratos/espacio', '/estratos/saturacion',
         '/estratos/cv5', '/estratos/cv6', '/estratos/cv7', '/estratos/cv8']


# --------------------------------------------------------------------------- SLIP

class Slip(object):
    """Decodificador SLIP: feed(bytes) devuelve los paquetes completos."""

    def __init__(self):
        self.buf = bytearray()
        self.esc = False

    def feed(self, datos):
        out = []
        for b in datos:
            if self.esc:
                self.esc = False
                if b == SLIP_ESC_END:
                    self.buf.append(SLIP_END)
                elif b == SLIP_ESC_ESC:
                    self.buf.append(SLIP_ESC)
                else:                       # escape roto: se descarta el paquete
                    self.buf = bytearray()
            elif b == SLIP_ESC:
                self.esc = True
            elif b == SLIP_END:
                if self.buf:
                    out.append(bytes(self.buf))
                self.buf = bytearray()
            else:
                self.buf.append(b)
        return out


def slip(paquete):
    out = bytearray([SLIP_END])
    for b in paquete:
        if b == SLIP_END:
            out += bytes([SLIP_ESC, SLIP_ESC_END])
        elif b == SLIP_ESC:
            out += bytes([SLIP_ESC, SLIP_ESC_ESC])
        else:
            out.append(b)
    out.append(SLIP_END)
    return bytes(out)


# --------------------------------------------------------------------------- OSC

def _texto(s):
    b = s.encode('utf-8') + b'\x00'
    return b + b'\x00' * (-len(b) % 4)


def osc_mensaje(ruta, *args):
    tipos = ',' + ''.join('f' if isinstance(a, float) else 'i' if isinstance(a, int) else 's' for a in args)
    cuerpo = b''
    for a in args:
        if isinstance(a, float):
            cuerpo += struct.pack('>f', a)
        elif isinstance(a, int):
            cuerpo += struct.pack('>i', a)
        else:
            cuerpo += _texto(str(a))
    return _texto(ruta) + _texto(tipos) + cuerpo


def osc_bundle(mensajes):
    out = _texto('#bundle') + struct.pack('>Q', 1)
    for m in mensajes:
        out += struct.pack('>i', len(m)) + m
    return out


def _leer_texto(datos, i):
    fin = datos.index(b'\x00', i)
    s = datos[i:fin].decode('utf-8', 'replace')
    return s, fin + 1 + (-(fin + 1 - i) % 4)


def osc_leer(datos):
    """[(ruta, [argumentos])] de un paquete OSC (mensaje o bundle)."""
    if datos.startswith(b'#bundle\x00'):
        out, i = [], 16
        while i + 4 <= len(datos):
            n = struct.unpack('>i', datos[i:i + 4])[0]
            out += osc_leer(datos[i + 4:i + 4 + n])
            i += 4 + n
        return out
    ruta, i = _leer_texto(datos, 0)
    if i >= len(datos):
        return [(ruta, [])]
    tipos, i = _leer_texto(datos, i)
    args = []
    for t in tipos[1:]:
        if t == 'f':
            args.append(struct.unpack('>f', datos[i:i + 4])[0])
            i += 4
        elif t == 'i':
            args.append(struct.unpack('>i', datos[i:i + 4])[0])
            i += 4
        elif t == 's':
            s, i = _leer_texto(datos, i)
            args.append(s)
    return [(ruta, args)]


# --------------------------------------------------------------------------- serie

def buscar_puerto():
    """El puerto serie de la placa: si solo hay uno con pinta de USB, ese."""
    from serial.tools import list_ports
    pistas = ('usb', 'cp210', 'ch340', 'ch9102', 'ftdi', 'esp32', 'arduino', 'jtag', 'acm')
    candidatos = [p.device for p in list_ports.comports()
                  if any(x in ('%s %s %s' % (p.device, p.description, p.hwid)).lower() for x in pistas)]
    if len(candidatos) == 1:
        return candidatos[0]
    todos = [p.device for p in list_ports.comports()]
    raise SystemExit('No se cual es la placa. Puertos: %s. Usa --serie.' % (', '.join(todos) or 'ninguno'))


def abrir(puerto, baudios):
    import serial
    return serial.Serial(puerto, baudios, timeout=0.05)


def destino_de(texto):
    host, _, puerto = texto.rpartition(':')
    return (host or '127.0.0.1', int(puerto))


class Vista(object):
    """Los ultimos valores, en una linea, unas cuantas veces por segundo."""

    def __init__(self, activa):
        self.activa, self.valores, self.t = activa, {}, 0.0
        self.paquetes = 0

    def anotar(self, mensajes):
        self.paquetes += 1
        for ruta, args in mensajes:
            if ruta == '/estratos/info':
                print('PLACA  %s' % ' '.join(str(a) for a in args))
            elif args and isinstance(args[0], float):
                self.valores[ruta] = args[0]
        if self.activa and time.time() - self.t > 0.25:
            self.t = time.time()
            linea = '  '.join('%s %+6.2f V' % (r.split('/')[-1], v) for r, v in sorted(self.valores.items(),
                                                                                 key=lambda kv: RUTAS.index(kv[0])
                                                                                 if kv[0] in RUTAS else 99))
            print('\r' + linea, end='', flush=True)


def puente(args):
    import serial
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destino = destino_de(args.destino)
    vista = Vista(args.ver)
    puerto = args.serie or buscar_puerto()
    print('PUENTE  %s (%d baudios) -> UDP %s:%d   Ctrl+C para parar' % (puerto, args.baudios, destino[0], destino[1]))
    while True:
        try:
            s = abrir(puerto, args.baudios)
            dec = Slip()
            while True:
                datos = s.read(4096)
                for p in dec.feed(datos):
                    udp.sendto(p, destino)
                    try:
                        vista.anotar(osc_leer(p))
                    except Exception:
                        pass
        except serial.SerialException as e:
            print('\nPUENTE  %s: %s; reintento en 1 s' % (puerto, e))
            time.sleep(1.0)


def orden(args):
    puerto = args.serie or buscar_puerto()
    s = abrir(puerto, args.baudios)
    time.sleep(1.5)                         # algunas placas se reinician al abrir el puerto
    s.reset_input_buffer()
    s.write((args.orden.strip() + '\n').encode('ascii'))
    dec = Slip()
    fin = time.time() + 2.0
    while time.time() < fin:
        for p in dec.feed(s.read(4096)):
            for ruta, a in osc_leer(p):
                if ruta == '/estratos/info':
                    print('PLACA  %s' % ' '.join(str(x) for x in a))


def senales_prueba(t):
    """Las de la fase 19 en voltios, sin azar: LFO de +-5 V (4 s), ruido 0-5 V
    que salta cada medio segundo, espacio 0-5 V (20 s) y rafagas de 5 V."""
    x = 0.05 + 0.9 * ((int(t * 2.0) * 0.6180339887 + 0.1234) % 1.0)
    for _ in range(9):
        x = 3.91 * x * (1.0 - x)
    return [5.0 * math.sin(2.0 * math.pi * t / 4.0), 5.0 * x,
            2.5 - 2.5 * math.cos(2.0 * math.pi * t / 20.0), 5.0 if t % 8.0 < 1.0 else 0.0]


def simular(args):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destino = destino_de(args.destino)
    vista = Vista(args.ver)
    print('SIMULAR  senales de prueba -> UDP %s:%d (Rangomodular: -5..5 V)   Ctrl+C para parar' % destino)
    t0 = time.time()
    while True:
        t = time.time() - t0
        p = osc_bundle([osc_mensaje(r, float(v)) for r, v in zip(RUTAS, senales_prueba(t))])
        udp.sendto(p, destino)
        vista.anotar(osc_leer(p))
        time.sleep(0.01)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Estratos: OSC de la placa por USB (SLIP) -> UDP')
    ap.add_argument('--serie', help='puerto serie de la placa (si no, se busca)')
    ap.add_argument('--baudios', type=int, default=921600, help='921600 (ESP32) o 500000 (Arduino Nano)')
    ap.add_argument('--destino', default='127.0.0.1:9000', help='host:puerto del OSC In de TouchDesigner')
    ap.add_argument('--ver', action='store_true', help='enseña los valores')
    ap.add_argument('--orden', help='manda una orden a la placa: cero, "cero 3", "cinco 3", borrar, info')
    ap.add_argument('--simular', action='store_true', help='sin placa: senales de prueba')
    args = ap.parse_args(argv)
    try:
        if args.simular:
            simular(args)
        elif args.orden:
            orden(args)
        else:
            puente(args)
    except KeyboardInterrupt:
        print('\nPUENTE  parado')


if __name__ == '__main__':
    main()
