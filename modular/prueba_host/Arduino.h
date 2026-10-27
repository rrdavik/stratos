// Arduino de mentira para compilar cv_osc.ino en el ordenador (prueba_cv_osc.py).
// Las tensiones de entrada y el tiempo los pone la prueba.
#pragma once
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <deque>
#include <vector>

#define A0 14
#define A1 15
#define A2 16
#define A3 17
#define A4 18
#define A5 19
#define A6 20
#define A7 21
#define ADC_11db 3

extern double cv_entrada[8];        // voltios en cada socket del A-180-9
extern unsigned long t_us;
unsigned long micros();
int analogRead(uint8_t pin);
uint32_t analogReadMilliVolts(uint8_t pin);
inline void analogReadResolution(int) {}
inline void analogSetAttenuation(int) {}

inline char *dtostrf(double v, signed char ancho, unsigned char dec, char *s) {
  sprintf(s, "%*.*f", ancho, dec, v);
  return s;
}

struct SerialStub {
  std::vector<uint8_t> salida;
  std::deque<char> entrada;
  void begin(long) {}
  size_t write(uint8_t b) { salida.push_back(b); return 1; }
  int available() { return (int)entrada.size(); }
  int read() { char c = entrada.front(); entrada.pop_front(); return c; }
};
extern SerialStub Serial;

#if defined(ESP32)
#include <map>
#include <string>
class Preferences {
 public:
  static std::map<std::string, std::vector<uint8_t>> &nvs() { static std::map<std::string, std::vector<uint8_t>> m; return m; }
  bool begin(const char *, bool) { return true; }
  void end() {}
  size_t putBytes(const char *k, const void *v, size_t n) {
    nvs()[k] = std::vector<uint8_t>((const uint8_t *)v, (const uint8_t *)v + n); return n; }
  size_t getBytesLength(const char *k) { return nvs().count(k) ? nvs()[k].size() : 0; }
  size_t getBytes(const char *k, void *v, size_t n) { memcpy(v, nvs()[k].data(), n); return n; }
};
#else
struct EEPROMStub {
  uint8_t mem[1024] = {0};
  template <class T> void put(int i, const T &t) { memcpy(mem + i, &t, sizeof(T)); }
  template <class T> void get(int i, T &t) { memcpy(&t, mem + i, sizeof(T)); }
};
extern EEPROMStub EEPROM;
#endif
