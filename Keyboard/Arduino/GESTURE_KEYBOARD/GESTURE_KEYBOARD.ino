#include <Wire.h>
#include <SoftwareSerial.h>

// Pins connected to the HM-11 bluetooth module
int rxPin = 8;
int txPin = 5;
SoftwareSerial bluetooth(rxPin, txPin);

// Pins used for I/O
int btnPin1 = 2;

// I2C address of the MPU-6050
const int MPU_addr = 0x68;
// Variables that will store sensor data
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;

// Status variables, used with buttons
int precBtn1 = HIGH;

void setup()
{
  // Set the pin mode of the buttons using the internal pullup resistor
  pinMode(btnPin1, INPUT_PULLUP);

  // Start the comunication with the MPU-6050 sensor
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0);    // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Start the serial communication
  bluetooth.begin(38400);
}
void loop()
{
  // Read the values of the buttons
  int resultBtn1 = digitalRead(btnPin1);

  // ON btn1 pressed, start the batch and light up the yellow LED
  if (precBtn1 == HIGH && resultBtn1 == LOW)
  {
    bluetooth.println("STARTING BATCH");
  }

  // If the btn1 is pressed, reads the data from the sensor and sends it through the communication channel
  if (resultBtn1 == LOW)
  {
    // Start the transmission with the MPU-6050 sensor
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU_addr, 14, true); // request a total of 14 registers

    // Reads the data from the sensor
    AcX = Wire.read() << 8 | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
    AcY = Wire.read() << 8 | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    AcZ = Wire.read() << 8 | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp = Wire.read() << 8 | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    GyX = Wire.read() << 8 | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    GyY = Wire.read() << 8 | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    GyZ = Wire.read() << 8 | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

    // Based on the current comunication channel, it sends the data.
    bluetooth.print("START");
    bluetooth.print(" "); bluetooth.print(AcX);
    bluetooth.print(" "); bluetooth.print(AcY);
    bluetooth.print(" "); bluetooth.print(AcZ);
    bluetooth.print(" "); bluetooth.print(GyX);
    bluetooth.print(" "); bluetooth.print(GyY);
    bluetooth.print(" "); bluetooth.print(GyZ);
    bluetooth.println(" END");
  }

  // Closes the batch when the button is released
  if (precBtn1 == LOW && resultBtn1 == HIGH)
  {
    bluetooth.println("CLOSING BATCH");
  }

  // Saves the button states
  precBtn1 = resultBtn1;
}
