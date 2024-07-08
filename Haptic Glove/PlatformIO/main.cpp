// I2C device class (I2Cdev) demonstration Arduino sketch for MPU6050 class using DMP (MotionApps v6.12)
// 6/21/2012 by Jeff Rowberg <jeff@rowberg.net>
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib
//
// Changelog:
//      2019-07-10 - Uses the new version of the DMP Firmware V6.12
//                 - Note: I believe the Teapot demo is broken with this versin as
//                 - the fifo buffer structure has changed
//      2016-04-18 - Eliminated a potential infinite loop
//      2013-05-08 - added seamless Fastwire support
//                 - added note about gyro calibration
//      2012-06-21 - added note about Arduino 1.0.1 + Leonardo compatibility error
//      2012-06-20 - improved FIFO overflow handling and simplified read process
//      2012-06-19 - completely rearranged DMP initialization code and simplification
//      2012-06-13 - pull gyro and accel data from FIFO packet instead of reading directly
//      2012-06-09 - fix broken FIFO read sequence and change interrupt detection to RISING
//      2012-06-05 - add gravity-compensated initial reference frame acceleration output
//                 - add 3D math helper file to DMP6 example sketch
//                 - add Euler output and Yaw/Pitch/Roll output formats
//      2012-06-04 - remove accel offset clearing for better results (thanks Sungon Lee)
//      2012-06-01 - fixed gyro sensitivity to be 2000 deg/sec instead of 250
//      2012-05-30 - basic DMP initialization working

/* ============================================
  I2Cdev device library code is placed under the MIT license
  Copyright (c) 2012 Jeff Rowberg

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  ===============================================
*/

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps612.h"
//#include "MPU6050.h" // not necessary if using MotionApps include file

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
 

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for SparkFun breakout and InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 mpu;
//MPU6050 mpu(0x69); // <-- use for AD0 high

/* =========================================================================
   NOTE: In addition to connection 3.3v, GND, SDA, and SCL, this sketch
   depends on the MPU-6050's INT pin being connected to the Arduino's
   external interrupt #0 pin. On the Arduino Uno and Mega 2560, this is
   digital I/O pin 2.
   ========================================================================= */

/* =========================================================================
   NOTE: Arduino v1.0.1 with the Leonardo board generates a compile error
   when using Serial.write(buf, len). The Teapot output uses this method.
   The solution requires a modification to the Arduino USBAPI.h file, which
   is fortunately simple, but annoying. This will be fixed in the next IDE
   release. For more info, see these links:

   http://arduino.cc/forum/index.php/topic,109987.0.html
   http://code.google.com/p/arduino/issues/detail?id=958
   ========================================================================= */



// uncomment "OUTPUT_READABLE_QUATERNION" if you want to see the actual
// quaternion components in a [w, x, y, z] format (not best for parsing
// on a remote host such as Processing or something though)
//#define OUTPUT_READABLE_QUATERNION

// uncomment "OUTPUT_READABLE_EULER" if you want to see Euler angles
// (in degrees) calculated from the quaternions coming from the FIFO.
// Note that Euler angles suffer from gimbal lock (for more info, see
// http://en.wikipedia.org/wiki/Gimbal_lock)
//#define OUTPUT_READABLE_EULER

// uncomment "OUTPUT_READABLE_YAWPITCHROLL" if you want to see the yaw/
// pitch/roll angles (in degrees) calculated from the quaternions coming
// from the FIFO. Note this also requires gravity vector calculations.
// Also note that yaw/pitch/roll angles suffer from gimbal lock (for
// more info, see: http://en.wikipedia.org/wiki/Gimbal_lock)
// #define OUTPUT_READABLE_YAWPITCHROLL

// uncomment "OUTPUT_READABLE_REALACCEL" if you want to see acceleration
// components with gravity removed. This acceleration reference frame is
// not compensated for orientation, so +X is always +X according to the
// sensor, just without the effects of gravity. If you want acceleration
// compensated for orientation, us OUTPUT_READABLE_WORLDACCEL instead.
//#define OUTPUT_READABLE_REALACCEL

// uncomment "OUTPUT_READABLE_WORLDACCEL" if you want to see acceleration
// components with gravity removed and adjusted for the world frame of
// reference (yaw is relative to initial orientation, since no magnetometer
// is present in this case). Could be quite handy in some cases.
#define OUTPUT_READABLE_WORLDACCEL

// uncomment "OUTPUT_TEAPOT" if you want output that matches the
// format used for the InvenSense teapot demo
//#define OUTPUT_TEAPOT

String data;
float dataw, datax, datay, dataz;
float datosw, datosx, datosy, datosz;

float dataAax,dataAay,dataAaz;
float datosAax,datosAay,datosAaz;

int value1,value2,value3,value4,value5; //save analog value
int dataFlex1,dataFlex2,dataFlex3,dataFlex4,dataFlex5;

float flex1,flex2,flex3,flex4,flex5;
float dedo1,dedo2,dedo3,dedo4,dedo5;
float offset1,offset2,offset3,offset4,offset5;
// Lo agregado es lo anterior

#define INTERRUPT_PIN 4  // use pin 2 on Arduino Uno & most boards
const int flexPin1 = 15; 
const int flexPin2 = 14;
const int flexPin3 = 2;
const int flexPin4 = 33;
const int flexPin5 = 32;

//Declaramos el pin del zumbador
// Definición de los pines a los que están conectados los transistores
const int motorPins[] = {17, 18, 19, 23, 25, 26}; // Puedes cambiar estos números de pin según tu configuración


// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 gy;         // [x, y, z]            gyro sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0, 0, 0, 0, 0, 0, 0, 0, 0x00, 0x00, '\r', '\n' };



// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
  mpuInterrupt = true;
}


// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup() {
  // join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
  Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(400, true);
#endif

  // initialize serial communication
  // (115200 chosen because it is required for Teapot Demo output, but it's
  // really up to you depending on your project)
  Serial.begin(115200);
  offset1=0;
  offset2=0;
  offset3=0;
  offset4=0;
  offset5=0;
  while (!Serial); // wait for Leonardo enumeration, others continue immediately

  // NOTE: 8MHz or slower host processors, like the Teensy @ 3.3V or Arduino
  // Pro Mini running at 3.3V, cannot handle this baud rate reliably due to
  // the baud timing being too misaligned with processor ticks. You must use
  // 38400 or slower in these cases, or use some kind of external separate
  // crystal solution for the UART timer.

  // initialize device
  // Serial.println(F("Initializing I2C devices..."));
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);

  // verify connection
  // Serial.println(F("Testing device connections..."));
  // Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

  // wait for ready
  // Serial.println(F("\nSend any character to begin DMP programming and demo: "));
  // while (Serial.available() && Serial.read()); // empty buffer
  // while (!Serial.available());                 // wait for data
  // while (Serial.available() && Serial.read()); // empty buffer again

  // load and configure the DMP
  // Serial.println(F("Initializing DMP..."));
  devStatus = mpu.dmpInitialize();

  // supply your own gyro offsets here, scaled for min sensitivity
  //mpu.setXAccelOffset(-3702); 
  //mpu.setYAccelOffset(-755); 
  //mpu.setZAccelOffset(2426); 
  //mpu.setXGyroOffset(70);
  //mpu.setYGyroOffset(-59);
  //mpu.setZGyroOffset(84);

  mpu.setXAccelOffset(-3708); // -3730
  mpu.setYAccelOffset(-725); // -713
  mpu.setZAccelOffset(2492); // 2748
  mpu.setXGyroOffset(86);
  mpu.setYGyroOffset(-59);
  mpu.setZGyroOffset(85);

  if (devStatus == 0) {
    // Calibration Time: generate offsets and calibrate our MPU6050
    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
    Serial.println();
    // mpu.PrintActiveOffsets();
    // turn on the DMP, now that it's ready
    // Serial.println(F("Enabling DMP..."));
    mpu.setDMPEnabled(true);

    // enable Arduino interrupt detection
    // Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
    // Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
    // Serial.println(F(")..."));
    attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
    mpuIntStatus = mpu.getIntStatus();

    // set our DMP Ready flag so the main loop() function knows it's okay to use it
    // Serial.println(F("DMP ready! Waiting for first interrupt..."));
    dmpReady = true;

    // get expected DMP packet size for later comparison
    packetSize = mpu.dmpGetFIFOPacketSize();
  } else {
    // ERROR!
    // 1 = initial memory load failed
    // 2 = DMP configuration updates failed
    // (if it's going to break, usually the code will be 1)
    Serial.print(F("DMP Initialization failed (code "));
    Serial.print(devStatus);
    Serial.println(F(")"));
  }
  
  for (int i = 0; i < 6; i++) {
    pinMode(motorPins[i], OUTPUT);
  }

}



// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {
  // if programming failed, don't try to do anything
  if (!dmpReady) return;
  // read a packet from FIFO
  if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) { // Get the Latest packet 

#ifdef OUTPUT_READABLE_QUATERNION
    // display quaternion values in easy matrix form: w x y z
    // mpu.dmpGetQuaternion(&q, fifoBuffer);
    // Serial.print("quat\t");
    //Modificado
    float count=200;
    for (int i = 0; i <= count; i++){
      //MPU
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      dataw+=q.w;
      datax+=q.x;
      datay+=q.y;
      dataz+=q.z;

      //Flex
      value1=analogRead(flexPin1);
      value2=analogRead(flexPin2);
      value3=analogRead(flexPin3);
      value4=analogRead(flexPin4);
      value5=analogRead(flexPin5);

      dataFlex1+=value1;
      dataFlex2+=value2;
      dataFlex3+=value3;
      dataFlex4+=value4;
      dataFlex5+=value5;


    }
    datosw=dataw/count;
    datosx=datax/count;
    datosy=datay/count;
    datosz=dataz/count;
    flex1 = float(dataFlex1)/ count;
    flex2 = float(dataFlex2) / count;
    flex3 = float(dataFlex3) / count;
    flex4 = float(dataFlex4) / count;
    flex5 = float(dataFlex5) / count;
  
  

    dataw=0;
    datax=0;
    datay=0;
    dataz=0;
    dataFlex1 = 0;
    dataFlex2 = 0;
    dataFlex3 = 0;
    dataFlex4 = 0;
    dataFlex5 = 0;

    dedo1=constrain(-25.91*log(flex1)+210.6, 0, 180);
    dedo2=constrain(-48.51*log(flex2)+407.77, 0, 180);
    dedo3=constrain(-52.48*log(flex3)+425.61, 0, 180);
    dedo4=constrain(-42.46*log(flex4)+342.99, 0, 180);
    dedo5=constrain(-37.69*log(flex5)+315.14, 0, 180);

    Serial.print(datosw);
    Serial.print(",");
    Serial.print(datosx);
    Serial.print(",");
    Serial.print(datosy);
    Serial.print(",");
    Serial.print(datosz);
    Serial.print(",");
    Serial.print(-dedo1+offset1);
    Serial.print(",");
    Serial.print(-dedo2+offset2);
    Serial.print(",");
    Serial.print(-dedo3+offset3);
    Serial.print(",");
    Serial.print(-dedo4+offset4); 
    Serial.print(",");
    Serial.println(-dedo5+offset5);
    delay(50);
#endif
    
#ifdef OUTPUT_READABLE_EULER
    // display Euler angles in degrees
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetEuler(euler, &q);
    Serial.print("euler\t");
    Serial.print(euler[0] * 180 / M_PI);
    Serial.print("\t");
    Serial.print(euler[1] * 180 / M_PI);
    Serial.print("\t");
    Serial.println(euler[2] * 180 / M_PI);
#endif

#ifdef OUTPUT_READABLE_YAWPITCHROLL
    // display Euler angles in degrees
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
    // Serial.print("ypr\t");
    Serial.print(ypr[0] * 180 / M_PI);
    Serial.print(",");
    Serial.print(ypr[1] * 180 / M_PI);
    Serial.print(",");
    Serial.print(ypr[2] * 180 / M_PI);
    /*
      mpu.dmpGetAccel(&aa, fifoBuffer);
      Serial.print("\tRaw Accl XYZ\t");
      Serial.print(aa.x);
      Serial.print("\t");
      Serial.print(aa.y);
      Serial.print("\t");
      Serial.print(aa.z);
      mpu.dmpGetGyro(&gy, fifoBuffer);
      Serial.print("\tRaw Gyro XYZ\t");
      Serial.print(gy.x);
      Serial.print("\t");
      Serial.print(gy.y);
      Serial.print("\t");
      Serial.print(gy.z);
    */
    Serial.println();
    delay(1000);

#endif

#ifdef OUTPUT_READABLE_REALACCEL
    // display real acceleration, adjusted to remove gravity
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetAccel(&aa, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
    Serial.print("areal\t");
    Serial.print(aaReal.x);
    Serial.print("\t");
    Serial.print(aaReal.y);
    Serial.print("\t");
    Serial.println(aaReal.z);
#endif

#ifdef OUTPUT_READABLE_WORLDACCEL
    // display initial world-frame acceleration, adjusted to remove gravity
    // and rotated based on known orientation from quaternion
    //mpu.dmpGetQuaternion(&q, fifoBuffer);
    //mpu.dmpGetAccel(&aa, fifoBuffer);
    //mpu.dmpGetGravity(&gravity, &q);
    //mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
    //mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);
    //Serial.print("aworld\t");
    //Serial.print(aaWorld.x);
    //Serial.print("\t");
    //Serial.print(aaWorld.y);
    //Serial.print("\t");
    //Serial.println(aaWorld.z);

    float count=200;
    for (int i = 0; i <= count; i++){
      //MPU
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetAccel(&aa, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
      //mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);

      dataw+=q.w;
      datax+=q.x;
      datay+=q.y;
      dataz+=q.z;

      dataAax+=aaReal.x;
      dataAay+=aaReal.y;
      dataAaz+=aaReal.z;

      //Flex
      value1=analogRead(flexPin1);
      value2=analogRead(flexPin2);
      value3=analogRead(flexPin3);
      value4=analogRead(flexPin4);
      value5=analogRead(flexPin5);

      dataFlex1+=value1;
      dataFlex2+=value2;
      dataFlex3+=value3;
      dataFlex4+=value4;
      dataFlex5+=value5;


    }
    datosw=dataw/count;
    datosx=datax/count;
    datosy=datay/count;
    datosz=dataz/count;
    flex1 = float(dataFlex1)/ count;
    flex2 = float(dataFlex2) / count;
    flex3 = float(dataFlex3) / count;
    flex4 = float(dataFlex4) / count;
    flex5 = float(dataFlex5) / count;
    datosAax=dataAax/count;
    datosAay=dataAay/count;
    datosAaz=dataAaz/count;
  
    dataw=0;
    datax=0;
    datay=0;
    dataz=0;
    dataFlex1 = 0;
    dataFlex2 = 0;
    dataFlex3 = 0;
    dataFlex4 = 0;
    dataFlex5 = 0;
    dataAax=0;
    dataAay=0;
    dataAaz=0;

    dedo1=constrain(-25.91*log(flex1)+210.6, 0, 180);
    dedo2=constrain(-48.51*log(flex2)+407.77, 0, 180);
    dedo3=constrain(-52.48*log(flex3)+425.61, 0, 180);
    dedo4=constrain(-42.46*log(flex4)+342.99, 0, 180);
    dedo5=constrain(-37.69*log(flex5)+315.14, 0, 180);

    Serial.print(datosw);
    Serial.print(",");
    Serial.print(datosx);
    Serial.print(",");
    Serial.print(datosy);
    Serial.print(",");
    Serial.print(datosz);
    Serial.print(",");
    Serial.print(-dedo1+offset1);
    Serial.print(",");
    Serial.print(-dedo2+offset2);
    Serial.print(",");
    Serial.print(-dedo3+offset3);
    Serial.print(",");
    Serial.print(-dedo4+offset4); 
    Serial.print(",");
    Serial.print(-dedo5+offset5);
    Serial.print(",");
    Serial.print(datosAax);
    Serial.print(",");
    Serial.print(datosAay);
    Serial.print(",");
    Serial.println(datosAaz);
    delay(50);
#endif

#ifdef OUTPUT_TEAPOT
    // display quaternion values in InvenSense Teapot demo format:
    teapotPacket[2] = fifoBuffer[0];
    teapotPacket[3] = fifoBuffer[1];
    teapotPacket[4] = fifoBuffer[4];
    teapotPacket[5] = fifoBuffer[5];
    teapotPacket[6] = fifoBuffer[8];
    teapotPacket[7] = fifoBuffer[9];
    teapotPacket[8] = fifoBuffer[12];
    teapotPacket[9] = fifoBuffer[13];
    Serial.write(teapotPacket, 14);
    teapotPacket[11]++; // packetCount, loops at 0xFF on purpose
#endif

    // blink LED to indicate activity
    // blinkState = !blinkState;
    // digitalWrite(LED, blinkState);
  }
  if(Serial.available()){
    data = Serial.readStringUntil('\n'); // Lee los datos hasta que encuentre un salto de línea
    int commaIndex1 = data.indexOf(','); // Encuentra la primera coma

    char estado = data.substring(0, commaIndex1).charAt(0); // Obtiene el primer valor (P)
    int motor = data.substring(commaIndex1 + 1).toInt(); // Obtiene el segundo valor (canal)
    switch (estado){
      case 'P':
      digitalWrite(motorPins[motor], HIGH);
      break;
      case 'A':
      digitalWrite(motorPins[motor], LOW);
      break;
    }
    delay(20);
  }
}