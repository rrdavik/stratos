# Genera modular/esquema.svg (python3 modular/esquema.py): bloques, un canal y los valores por placa.
W, H = 1200, 960
o = []
def t(x, y, s, size=15, anchor='start', weight='normal', color='#1b1b1f'):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    o.append('<text x="%g" y="%g" font-size="%d" text-anchor="%s" font-weight="%s" fill="%s">%s</text>'
             % (x, y, size, anchor, weight, color, s))
def l(x1, y1, x2, y2, w=2, color='#1b1b1f', dash=None):
    o.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"%s/>'
             % (x1, y1, x2, y2, color, w, ' stroke-dasharray="%s"' % dash if dash else ''))
def r(x, y, w, h, fill='none', color='#1b1b1f', rx=0, sw=2):
    o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="%g" rx="%g"/>'
             % (x, y, w, h, fill, color, sw, rx))
def punto(x, y):
    o.append('<circle cx="%g" cy="%g" r="4" fill="#1b1b1f"/>' % (x, y))
def flecha(x1, y1, x2, y2):
    l(x1, y1, x2, y2)
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (0.45, -0.45):
        l(x2, y2, x2 - 12 * math.cos(a + s), y2 - 12 * math.sin(a + s))
def res_h(x, y, nombre, valor):          # resistencia horizontal de x a x+80
    l(x, y, x + 20, y); r(x + 20, y - 9, 40, 18, fill='white'); l(x + 60, y, x + 80, y)
    t(x + 40, y - 16, '%s  %s' % (nombre, valor), 13, 'middle')
def res_v(x, y, nombre, valor):          # vertical de y a y+80, rotulo a la izquierda
    l(x, y, x, y + 20); r(x - 9, y + 20, 18, 40, fill='white'); l(x, y + 60, x, y + 80)
    t(x - 16, y + 45, '%s  %s' % (nombre, valor), 13, 'end')
def masa(x, y):
    l(x, y, x, y + 10)
    for k, w in enumerate((22, 14, 6)):
        l(x - w / 2, y + 10 + 5 * k, x + w / 2, y + 10 + 5 * k)
def vcc(x, y, s):
    l(x, y, x, y - 12); l(x - 12, y - 12, x + 12, y - 12); t(x, y - 18, s, 13, 'middle')
def diodo_v(x, y1, y2, nombre=''):       # diodo vertical, catodo arriba (conduce hacia arriba)
    l(x, y1, x, (y1 + y2) / 2 - 10)
    o.append('<polygon points="%g,%g %g,%g %g,%g" fill="white" stroke="#1b1b1f" stroke-width="2"/>'
             % (x - 10, (y1 + y2) / 2 + 8, x + 10, (y1 + y2) / 2 + 8, x, (y1 + y2) / 2 - 8))
    l(x - 10, (y1 + y2) / 2 - 10, x + 10, (y1 + y2) / 2 - 10)
    l(x, (y1 + y2) / 2 + 8, x, y2)

o.append('<rect width="100%" height="100%" fill="#fbfaf7"/>')
t(30, 40, 'Estratos · CV del modular → OSC por USB', 24, weight='bold')
t(30, 66, 'Doepfer A-180-9 (multicore pasivo, sockets 1-8) + red de entrada por canal + ESP32-S3 (o ESP32 / Arduino Nano) + puente_osc.py', 14,
  color='#55555c')

# --- diagrama de bloques
y0 = 110
cajas = [(20, 'Modular', ['LFO, ruido,', 'espacio, saturacion']), (190, 'A-180-9', ['sockets 1-8', 'en la caja']),
         (400, 'Jack RJ45', ['apantallado', 'malla = GND']), (570, '8 x red', ['de entrada', '(abajo)']),
         (740, 'ESP32-S3', ['GPIO 1-8 (ADC1)', 'cv_osc.ino']), (950, 'Ordenador', ['puente_osc.py', 'UDP :9000 -> TD'])]
for x, nom, lineas in cajas:
    r(x, y0, 150 if nom != 'Ordenador' else 210, 86, fill='#ffffff', rx=10)
    t(x + 12, y0 + 26, nom, 16, weight='bold')
    for k, s in enumerate(lineas):
        t(x + 12, y0 + 50 + 18 * k, s, 13, color='#3a3a40')
for (x1, x2, et) in ((170, 190, ''), (340, 400, 'CAT-6a/7'), (550, 570, ''), (720, 740, ''), (890, 950, 'USB')):
    flecha(x1, y0 + 43, x2, y0 + 43)
    if et:
        t((x1 + x2) / 2, y0 + 64, et, 11, 'middle', color='#3a3a40')
t(400, y0 + 112, 'Nunca a un switch, router ni al puerto de red: por el cable van voltios, no Ethernet.', 13,
  'middle', color='#b42318', weight='bold')

# --- un canal
y = 420
t(30, 272, 'Un canal (x8): ±10 V → 0,24-2,40 V en el ADC', 18, weight='bold')
t(30, y + 5, 'RJ45 pin n', 14, weight='bold')
t(30, y + 23, '(socket n del A-180-9)', 12, color='#55555c')
l(130, y, 170, y)
res_h(170, y, 'R1', '100k')
nodo = 330
l(250, y, 580, y)
punto(nodo, y)
# R2 a VCC
l(nodo, y, nodo, y - 30)
res_v(nodo, y - 110, 'R2', '27k (Nano 47k)')
vcc(nodo, y - 110, '3V3 (Nano 5V)')
# R3 a masa
res_v(nodo, y, 'R3', '22k (Nano 82k)')
masa(nodo, y + 80)
# condensador
cx = 450
punto(cx, y)
l(cx, y, cx, y + 32); l(cx - 16, y + 32, cx + 16, y + 32); l(cx - 16, y + 40, cx + 16, y + 40); l(cx, y + 40, cx, y + 80)
t(cx + 22, y + 42, 'C1 100n', 13)
masa(cx, y + 80)
# diodos BAT54S
dx = 550
punto(dx, y)
diodo_v(dx, y - 80, y)
vcc(dx, y - 80, '3V3 (Nano 5V)')
diodo_v(dx, y, y + 80)
masa(dx, y + 80)
t(dx + 18, y - 40, 'D1', 13); t(dx + 18, y + 45, 'D2', 13)
t(dx + 18, y + 62, 'BAT54S', 12, color='#55555c')
l(580, y, 660, y)
r(660, y - 22, 150, 44, fill='#ffffff', rx=6)
t(735, y + 5, 'GPIO n (ADC)', 14, 'middle', weight='bold')
t(30, y + 140, 'V_nodo = MEDIO + PENDIENTE x V_entrada   (el firmware lo deshace; "cero" y "cinco" lo calibran)', 14)
t(30, y + 162, 'Impedancia de entrada ~100 kΩ (como una entrada Eurorack); ±12 V caben sin llegar a los diodos en ESP32.', 13,
  color='#3a3a40')

# --- tabla
ty = 640
t(30, ty, 'Valores por placa', 18, weight='bold')
filas = [('', 'ESP32-S3 / ESP32 (3,3 V)', 'Arduino Nano (5 V)'),
         ('R1 · R2 · R3', '100k · 27k · 22k (1 %)', '100k · 47k · 82k (1 %)'),
         ('-10 V · 0 V · +10 V en el ADC', '0,24 · 1,32 · 2,40 V', '0,15 · 2,45 · 4,75 V'),
         ('Resolucion', '~7 mV de CV (12 bits)', '~21 mV de CV (10 bits)'),
         ('Pines de los canales 1-8', 'S3: GPIO 1-8 · ESP32: 36 39 34 35 32 33 25 26', 'A0-A7'),
         ('Paquetes por segundo', '100', '50')]
cols = (30, 330, 760)
for k, fila in enumerate(filas):
    yy = ty + 32 + 28 * k
    if k == 0:
        r(25, yy - 20, 1150, 28, fill='#ecebe6', color='#ecebe6', sw=0)
    for c, s in zip(cols, fila):
        t(c, yy, s, 14, weight='bold' if k == 0 or c == 30 else 'normal')
    l(25, yy + 8, 1175, yy + 8, 1, '#d4d2cb')

# --- RJ45
ry = 860
t(30, ry, 'RJ45 (lado del jack)', 18, weight='bold')
t(30, ry + 26, 'pin 1-8 = sockets 1-8 del A-180-9 = canales 1-8: 1 lfo · 2 ruido · 3 espacio · 4 saturacion · 5-8 libres', 14)
t(30, ry + 48, 'Malla del cable / carcasa del jack = GND de la placa (la masa comun del modular llega por la malla).', 14)
t(30, ry + 70, 'Comprueba con un polimetro (continuidad) que el pin n llega al socket n: no he podido abrir la hoja de Doepfer.',
  14, color='#b42318')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="DejaVu Sans, Helvetica, Arial, sans-serif">%s</svg>' % (W, H, W, H, ''.join(o))
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'esquema.svg'), 'w').write(svg)
print('ok', len(svg))
