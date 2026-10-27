// Ejecuta cv_osc.ino con el Arduino de mentira: fases separadas por mensajes
// /prueba/fase. Las resistencias "reales" se desvian de las nominales, como
// las de verdad (1 %), para que la calibracion tenga algo que corregir.
#include "Arduino.h"
#include "../cv_osc/cv_osc.ino"

double cv_entrada[8] = {0};
unsigned long t_us = 0;
SerialStub Serial;
#if !defined(ESP32)
EEPROMStub EEPROM;
#endif

static double nodo(int c) {  // la red de entrada con resistencias desviadas
  double r1 = R1 * (1.0 + 0.008 * ((c % 3) - 1)), r2 = R2 * 1.01, r3 = R3 * 0.99;
  double g = 1.0 / r1 + 1.0 / r2 + 1.0 / r3;
  return (cv_entrada[c] / r1 + VCC / r2) / g;
}
static int canal_de_pin(uint8_t pin) {
  for (int c = 0; c < N_CANALES; c++)
    if (PINES[c] == pin) return c;
  return 0;
}
unsigned long micros() { return t_us; }
int analogRead(uint8_t pin) {
  double v = nodo(canal_de_pin(pin)) / VCC * 1023.0;
  return (int)fmax(0.0, fmin(1023.0, floor(v + 0.5)));
}
uint32_t analogReadMilliVolts(uint8_t pin) {
  double v = nodo(canal_de_pin(pin)) * 1000.0;
  return (uint32_t)fmax(0.0, fmin(3100.0, floor(v + 0.5)));
}

static void fase(int n) {
  size_t k = osc_texto(paquete, "/prueba/fase");
  k += osc_texto(paquete + k, ",s");
  char t[8];
  snprintf(t, sizeof(t), "%d", n);
  k += osc_texto(paquete + k, t);
  slip_enviar(paquete, k);
}
static void correr(double segundos) {
  unsigned long fin = t_us + (unsigned long)(segundos * 1e6);
  while (t_us < fin) { t_us += 500; loop(); }
}
static void decir(const char *s) {
  for (const char *p = s; *p; p++) Serial.entrada.push_back(*p);
}

int main() {
  // cada fase mide con las entradas quietas; fase 9 marca los cambios
  const double cv1[8] = {-5.0, 0.0, 2.5, 5.0, 10.0, -10.0, 1.0, 0.0};
  memcpy(cv_entrada, cv1, sizeof(cv1));
  setup();
  fase(1);                                 // sin calibrar
  correr(1.0);
  fase(9);
  for (int c = 0; c < 8; c++) cv_entrada[c] = 0.0;
  decir("cero\n");
  correr(0.5);
  fase(2);                                 // tras 'cero', todo a 0 V
  correr(0.5);
  fase(9);
  cv_entrada[0] = 5.0;
  correr(0.3);
  decir("cinco 1\n");
  correr(0.05);
  cv_entrada[0] = -5.0;
  correr(1.0);
  fase(3);                                 // canal 1 a -5 V, calibrado
  correr(0.5);
  fase(9);
  cv_entrada[1] = 3.3;                     // canal 2: calibrar con 3,3 V medidos
  correr(0.3);
  decir("cinco 2 3.3\n");
  correr(0.05);
  cv_entrada[1] = 7.5;
  correr(1.0);
  fase(5);                                 // canal 2 a 7,5 V
  correr(0.5);
  fase(9);
  fase(4);
  decir("info\n");
  correr(0.5);
  char seg[16];
  snprintf(seg, sizeof(seg), "%.3f", t_us / 1e6);
  size_t k = osc_texto(paquete, "/prueba/segundos");
  k += osc_texto(paquete + k, ",s");
  k += osc_texto(paquete + k, seg);
  slip_enviar(paquete, k);
  fwrite(Serial.salida.data(), 1, Serial.salida.size(), stdout);
  return 0;
}
