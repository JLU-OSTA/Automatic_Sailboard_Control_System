#include <MFRC522Extended.h>

#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"
MPU6050 accelgyro;
int16_t ax, ay, az;
bool blinkState = false;
void setup() {
    Wire.begin();
    Serial.begin(19200);
    accelgyro.initialize();
}

void loop() {
    accelgyro.getAcceleration(&ax, &ay, &az);
    Serial.print(ax); Serial.print("\t");
    Serial.print(ay); Serial.print("\t");
    Serial.println(az); 
    delay(50);
}
