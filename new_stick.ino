// MPU9250とArduinoのつなぎ方
// https://ryusakura.wordpress.com/2017/05/24/

// Arduino 日本語リファレンス
// http://www.musashinodenpa.com/arduino/ref/index.php

// Arduinoに接続したNeoPixelの色と明るさをシリアル通信で制御する
// https://qiita.com/yuji_miyano/items/ad92ae41ac2d97ab0171

#include <Adafruit_NeoPixel.h>
#include <SPI.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#include "image.h"

// MPU9250レジスタ定義
#define REG_ACCEL_XOUT_H 0x3B
#define REG_ACCEL_XOUT_L 0x3C
#define REG_ACCEL_YOUT_H 0x3D
#define REG_ACCEL_YOUT_L 0x3E
#define REG_ACCEL_ZOUT_H 0x3F
#define REG_ACCEL_ZOUT_L 0x40
#define REG_TEMP_OUT_H 0x41
#define REG_TEMP_OUT_L 0x42
#define REG_GYRO_XOUT_H 0x43
#define REG_GYRO_XOUT_L 0x44
#define REG_GYRO_YOUT_H 0x45
#define REG_GYRO_YOUT_L 0x46
#define REG_GYRO_ZOUT_H 0x47
#define REG_GYRO_ZOUT_L 0x48
#define REG_WHO_AM_I 0x75

// ピンアサイン
#define LED_PIN 6
// #define BUTTON_PIN 7
#define CS 10
// #define MOSI 11
// #define MISO 12
// #define CLK 13

Adafruit_NeoPixel pixels(IMG_HEIGHT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV16);  // 1MHz
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  pinMode(CS, OUTPUT);
  pixels.begin();
  pixels.setBrightness(20);
}

void loop() {
  char d[1] = {0};
  readSpi(REG_ACCEL_XOUT_H, (uint8_t*)d, sizeof(d), CS);
  const image_t* image = currect_image();
  int line = ((int)d[0] + 0x80) * IMG_WIDTH / 0x100;
  // Serial.println(line);
  if (0 <= line && line < IMG_HEIGHT) {
    draw_pixels(image, line);
    pixels.show();
  }
}

static void draw_pixels(const image_t* image, int line) {
  for (int i = 0; i < IMG_HEIGHT; ++i) {
    image_t c = pgm_read_word(image + line * IMG_HEIGHT + i);
    uint8_t r = (c & 0xF800) >> 8;
    uint8_t g = (c & 0x07E0) >> 3;
    uint8_t b = (c & 0x001F) << 3;
    pixels.setPixelColor(i, r, g, b);
  }
}

static const image_t* currect_image() {
  static int nimg = 0;
  static unsigned long time = millis();
  if (3000 < millis() - time) {
    nimg = (nimg + 1) % COUNT_OF_IMAGES;
    time = millis();
  }
  return images[nimg];
}

static void readSpi(uint8_t reg, uint8_t* buf, int len, int cs) {
  digitalWrite(cs, LOW);
  SPI.transfer(reg | 0x80);
  for (int i = 0; i < len; ++i) buf[i] = SPI.transfer(0x00);
  digitalWrite(cs, HIGH);
}
