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

//チップセレクトピンに10を使用
#define CS 10
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

#define PIN 6         // Arduinoで使うピン
#define NUMPIXELS 72  // LEDの数。

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV16);  // 1MHz
  SPI.setBitOrder(MSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  pinMode(CS, OUTPUT);
  pixels.begin();
  pixels.setBrightness(30);
}

void loop() {
  int d;
  readItems(REG_ACCEL_YOUT_H, &d, 1);
  Serial.println(d);
  if (d < -8000) {
    color(0xFF, 0x00, 0x00);
  } else if (d < 8000) {
    color(0x00, 0xFF, 0x00);
  } else {
    color(0x00, 0x00, 0xFF);
  }
  pixels.show();
  delay(100);
}

void readItems(uint8_t regAddr, int* d, int n) {
  uint8_t d0, d1;
  digitalWrite(CS, LOW);
  SPI.transfer(regAddr | 0x80);
  for (int i = 0; i < n; ++i) {
    d0 = SPI.transfer(0x00);
    d1 = SPI.transfer(0x00);
    d[i] = (int)((d0 << 8) + (d1 & 0xFF));
  }
  digitalWrite(CS, HIGH);
}

void color(int r, int g, int b) {
  for (int i = 0; i < NUMPIXELS; ++i)
    pixels.setPixelColor(i, pixels.Color(r, g, b));
}