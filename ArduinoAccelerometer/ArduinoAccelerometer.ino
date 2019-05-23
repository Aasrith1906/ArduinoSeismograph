#include <Wire.h>

const float UpperLimit = 15.00;
const int Number_Data_Points = 500; 
const int Delay = 100;
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ;


struct Acceleration
{
  float acX;
  float acY;
};

struct Acceleration CreateData(float acX, float acY)
{
  struct Acceleration DataPoint;
  DataPoint.acX = acX;
  DataPoint.acY = acY;

  return DataPoint;
}

struct Acceleration ReadData()
{
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)

  float acX = AcX;
  float acY = AcY;
 
  acX = (acX/16384)*9.81;
  acY = (acY/16384)*9.811;
  
  struct Acceleration DataPoint;
  DataPoint = CreateData(acX,acY);

  return DataPoint;
}

void setup() {
  Serial.begin(9600);  
  
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  
  Wire.endTransmission(true);
}

void loop() {

 struct Acceleration DataPoint1;

 DataPoint1 = ReadData();
 
 if(DataPoint1.acX >= UpperLimit or DataPoint1.acY >= UpperLimit)
 {
    Serial.print(DataPoint1.acX);
    Serial.print(",");
    Serial.println(DataPoint1.acY);
    
   for(int i = 0; i <= Number_Data_Points; i++)
   {
     struct Acceleration DataPoint;
     DataPoint = ReadData();
     
     float Acx = DataPoint.acX;
     float Acy = DataPoint.acY;
     
     Serial.write(Acx);
     Serial.write(",");
     Serial.println(Acy);

     delay(50);
    
   }
 }

}


