// =============================================================================
// ESTRATOS - CV -> OSC
// =============================================================================
// Lee hasta 8 tensiones del modular (las que llegan por el cable del Doepfer
// A-180-9, sockets 1-8) y las manda como OSC por el USB, en paquetes SLIP
// (OSC 1.1 por serie). En el ordenador, puente_osc.py los pasa a UDP para el
// OSC In CHOP de TouchDesigner (fase 19, Fuentemodular = osc).
//
// Placas: ESP32-S3 (recomendada), ESP32 clasico y Arduino Nano / Uno (5 V).
// El circuito de entrada de cada canal (ver modular/README.md) lleva +-10 V
// al rango del ADC:   V_nodo = MEDIO + PENDIENTE x V_entrada
// Se manda la tension de ENTRADA en voltios (por ejemplo, de -5 a 5): en
// TouchDesigner, Rangomodular dice que rango es.
//
// Ordenes por el mismo USB (una linea de texto; las manda puente_osc.py):
//   cero         todas las entradas con 0 V (latiguillo a masa): guarda el medio
//   cero 3       solo el canal 3 (1-8)
//   cinco 3      el canal 3 con +5 V exactos: guarda la pendiente
//   cinco 3 4.87 el canal 3 con una tension conocida (medida con el polimetro)
//   borrar       vuelve a los valores de las resistencias
//   info         manda la calibracion de cada canal
// Las respuestas llegan como mensajes OSC /estratos/info (texto).
// =============================================================================

#include <Arduino.h>
#include <string.h>
#if defined(ESP32)
#include <Preferences.h>
#else
#include <EEPROM.h>
#endif

// ---------------------------------------------------------------- configuracion
const uint8_t N_CANALES = 8;
const char *const RUTAS[N_CANALES] = {
    "/estratos/lfo", "/estratos/ruido", "/estratos/espacio", "/estratos/saturacion",
    "/estratos/cv5", "/estratos/cv6", "/estratos/cv7", "/estratos/cv8"};
const float ALISADO = 0.5;         // filtro de cada canal: 0 nada ... 0,9 mucho

#if defined(CONFIG_IDF_TARGET_ESP32S3)
const uint8_t PINES[N_CANALES] = {1, 2, 3, 4, 5, 6, 7, 8};          // ADC1_CH0-CH7
#elif defined(ESP32)
const uint8_t PINES[N_CANALES] = {36, 39, 34, 35, 32, 33, 25, 26};  // ADC1 y ADC2 (sin WiFi)
#else
const uint8_t PINES[N_CANALES] = {A0, A1, A2, A3, A4, A5, A6, A7};  // Nano: A0-A7
#endif

// la red de entrada de cada canal (ver README): R1 de la entrada al nodo,
// R2 del nodo a VCC y R3 del nodo a masa
#if defined(ESP32)
const float VCC = 3.3, R1 = 100000.0, R2 = 27000.0, R3 = 22000.0;
const long BAUDIOS = 921600;       // con USB nativo (ESP32-S3) da igual
const uint8_t MUESTRAS = 8;        // sobremuestreo por lectura
const uint16_t HZ = 100;           // paquetes por segundo (cada uno, los 8 canales)
#else
const float VCC = 5.0, R1 = 100000.0, R2 = 47000.0, R3 = 82000.0;
const long BAUDIOS = 500000;       // exacto a 16 MHz
const uint8_t MUESTRAS = 4;
const uint16_t HZ = 50;            // un paquete son ~300 bytes: a 500000 baudios, 6 ms
#endif

// ---------------------------------------------------------------- estado
float medio[N_CANALES], pendiente[N_CANALES], valor[N_CANALES];
bool primera = true;
char orden[32];
uint8_t n_orden = 0;
unsigned long siguiente = 0;
uint8_t paquete[320];              // un bundle de 8 canales ocupa 304 bytes

// ---------------------------------------------------------------- SLIP y OSC
const uint8_t SLIP_END = 0xC0, SLIP_ESC = 0xDB, SLIP_ESC_END = 0xDC, SLIP_ESC_ESC = 0xDD;

void slip_enviar(const uint8_t *datos, size_t n) {
  Serial.write(SLIP_END);
  for (size_t i = 0; i < n; i++) {
    if (datos[i] == SLIP_END) {
      Serial.write(SLIP_ESC);
      Serial.write(SLIP_ESC_END);
    } else if (datos[i] == SLIP_ESC) {
      Serial.write(SLIP_ESC);
      Serial.write(SLIP_ESC_ESC);
    } else {
      Serial.write(datos[i]);
    }
  }
  Serial.write(SLIP_END);
}

size_t osc_texto(uint8_t *b, const char *s) {  // cadena OSC: terminada en 0 y rellena a 4
  size_t n = strlen(s);
  memcpy(b, s, n);
  b[n++] = 0;
  while (n % 4) b[n++] = 0;
  return n;
}

size_t osc_float(uint8_t *b, const char *ruta, float v) {
  size_t n = osc_texto(b, ruta);
  n += osc_texto(b + n, ",f");
  uint32_t u;
  memcpy(&u, &v, 4);
  b[n++] = (u >> 24) & 0xFF;
  b[n++] = (u >> 16) & 0xFF;
  b[n++] = (u >> 8) & 0xFF;
  b[n++] = u & 0xFF;
  return n;
}

void osc_info(const char *texto) {
  size_t n = osc_texto(paquete, "/estratos/info");
  n += osc_texto(paquete + n, ",s");
  n += osc_texto(paquete + n, texto);
  slip_enviar(paquete, n);
}

// un bundle OSC con los 8 canales: un solo paquete por tick
void enviar_canales() {
  size_t n = osc_texto(paquete, "#bundle");
  for (uint8_t k = 0; k < 7; k++) paquete[n++] = 0;  // marca de tiempo 1: "ya"
  paquete[n++] = 1;
  for (uint8_t c = 0; c < N_CANALES; c++) {
    size_t m = osc_float(paquete + n + 4, RUTAS[c], valor[c]);
    paquete[n++] = 0;
    paquete[n++] = 0;
    paquete[n++] = (m >> 8) & 0xFF;
    paquete[n++] = m & 0xFF;
    n += m;
  }
  slip_enviar(paquete, n);
}

// ---------------------------------------------------------------- lectura
float leer_nodo(uint8_t c) {  // tension en el pin del ADC, en voltios
  float s = 0;
  for (uint8_t k = 0; k < MUESTRAS; k++) {
#if defined(ESP32)
    s += analogReadMilliVolts(PINES[c]) / 1000.0;  // calibrada de fabrica (eFuse)
#else
    s += analogRead(PINES[c]) * VCC / 1023.0;
#endif
  }
  return s / MUESTRAS;
}

float leer_cv(uint8_t c) {
  return (leer_nodo(c) - medio[c]) / pendiente[c];
}

// ---------------------------------------------------------------- calibracion
void calibracion_nominal() {
  float g = 1.0 / R1 + 1.0 / R2 + 1.0 / R3;
  for (uint8_t c = 0; c < N_CANALES; c++) {
    pendiente[c] = (1.0 / R1) / g;
    medio[c] = VCC * (1.0 / R2) / g;
  }
}

void guardar() {
#if defined(ESP32)
  Preferences p;
  p.begin("estratos", false);
  p.putBytes("medio", medio, sizeof(medio));
  p.putBytes("pend", pendiente, sizeof(pendiente));
  p.end();
#else
  EEPROM.put(0, (uint32_t)0x45535443);  // 'ESTC'
  EEPROM.put(4, medio);
  EEPROM.put(4 + sizeof(medio), pendiente);
#endif
}

void cargar() {
  calibracion_nominal();
#if defined(ESP32)
  Preferences p;
  p.begin("estratos", true);
  if (p.getBytesLength("medio") == sizeof(medio) && p.getBytesLength("pend") == sizeof(pendiente)) {
    p.getBytes("medio", medio, sizeof(medio));
    p.getBytes("pend", pendiente, sizeof(pendiente));
  }
  p.end();
#else
  uint32_t marca = 0;
  EEPROM.get(0, marca);
  if (marca == 0x45535443) {
    EEPROM.get(4, medio);
    EEPROM.get(4 + sizeof(medio), pendiente);
  }
#endif
  for (uint8_t c = 0; c < N_CANALES; c++) {  // una calibracion rota no deja el canal mudo
    if (!(pendiente[c] > 0.01 && pendiente[c] < 1.0) || !(medio[c] > 0.0 && medio[c] < VCC)) {
      calibracion_nominal();
      break;
    }
  }
}

void ejecutar(char *linea) {
  char *palabra = strtok(linea, " \r\n");
  char *arg = strtok(NULL, " \r\n");
  char *arg2 = strtok(NULL, " \r\n");
  int c = arg ? atoi(arg) - 1 : -1;
  float ref = arg2 ? atof(arg2) : 5.0;
  char txt[64];
  if (!palabra) return;
  if (!strcmp(palabra, "cero")) {
    for (uint8_t k = 0; k < N_CANALES; k++) {
      if (c < 0 || c == k) medio[k] = leer_nodo(k);
    }
    guardar();
    osc_info(c < 0 ? "cero: medio guardado en los 8 canales" : "cero: medio guardado");
  } else if (!strcmp(palabra, "cinco") && c >= 0 && c < N_CANALES) {
    float p = (leer_nodo(c) - medio[c]) / ref;
    if (fabs(ref) > 0.5 && p > 0.01 && p < 1.0) {
      pendiente[c] = p;
      guardar();
      osc_info("cinco: pendiente guardada");
    } else {
      osc_info("cinco: no llega esa tension al canal (antes, cero; al menos 0,5 V)");
    }
  } else if (!strcmp(palabra, "borrar")) {
    calibracion_nominal();
    guardar();
    osc_info("borrar: valores de las resistencias");
  } else if (!strcmp(palabra, "info")) {
    for (uint8_t k = 0; k < N_CANALES; k++) {
      char a[12], b[12];
      dtostrf(medio[k], 1, 4, a);
      dtostrf(pendiente[k], 1, 5, b);
      snprintf(txt, sizeof(txt), "canal %d %s medio %s pendiente %s", k + 1, RUTAS[k], a, b);
      osc_info(txt);
    }
  } else {
    osc_info("ordenes: cero [c], cinco c [voltios], borrar, info");
  }
}

void leer_ordenes() {
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') {
      if (n_orden) {
        orden[n_orden] = 0;
        ejecutar(orden);
        n_orden = 0;
      }
    } else if (n_orden < sizeof(orden) - 1) {
      orden[n_orden++] = ch;
    }
  }
}

// ---------------------------------------------------------------- arduino
void setup() {
  Serial.begin(BAUDIOS);
#if defined(ESP32)
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);  // hasta ~2,5 V (ESP32) o ~3,1 V (ESP32-S3)
#endif
  cargar();
  siguiente = micros();
  osc_info("estratos cv_osc: 8 canales");
}

void loop() {
  leer_ordenes();
  unsigned long ahora = micros();
  if ((long)(ahora - siguiente) < 0) return;
  siguiente += 1000000UL / HZ;
  if ((long)(ahora - siguiente) > 100000L) siguiente = ahora;  // tras un atasco, sin rafagas
  for (uint8_t c = 0; c < N_CANALES; c++) {
    float v = leer_cv(c);
    valor[c] = primera ? v : ALISADO * valor[c] + (1.0 - ALISADO) * v;
  }
  primera = false;
  enviar_canales();
}
