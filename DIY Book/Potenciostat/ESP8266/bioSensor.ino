#include <SoftwareSerial.h>


// Se inicializa el objeto serial en los pines D7 y D8 correspondientes a Rx y Tx. 
SoftwareSerial mySerial(D7 , D8); // RX, TX


// La librería maneja las interrupciones automaticamente al llamar la función read() y/o write().
// Esto quiere decir que no hay necesiad de crear una función Handler().


/*****************************
*   Comandos potenciostato
****************************/

uint8_t StartID = 0xA0;
uint8_t EndPKG = 0xAB;
uint8_t StartMeasurement = 0x01;
uint8_t StopMeasurement = 0x02;
uint8_t SetStartPoint = 0x03;
uint8_t SetZeroCrossing = 0x04;
uint8_t SetFirstVertex = 0x05;
uint8_t SetSecondVertex = 0x06;
uint8_t SetSpeed = 0x07;
uint8_t SetTimeHold = 0x11;
uint8_t SetFinalValue = 0x12;
uint8_t ACK = 0xB0;
uint8_t ENDRUN = 0xB1;

/***************************
*  Parámetros de recorrido
**************************/

int _resolution = 4096 ; //¡NO CAMBIAR ESTE PARÁMETRO!
double zero = 0 ; //Centro del ciclo o zero del ciclo.
double verticeInferior = -0.9; //Voltaje mínimo del ciclo.
double verticeSuperior = 0.9; //Voltaje máximo del ciclo.
int ciclos = 20 ; //Cuántas veces pasa por el inicio o por el zero.
double velocidad = 0.050 ; //Velocidad de ciclo.
double correccionZero = 1.15 ; //Corrección del zero.

/************************
*  Variables de lectura
***********************/

float voltage;
float current;
float lastCurrent;
float oxiCurrent;
float redCurrent;
float oxiVoltage;
float redVoltage;

/***********************
*  Dummies del ciclo
**********************/

bool isRunning = false;
bool successfulRun = false;
int recorrido = 0;
float diferenciaCorriente;
int contador = 0;

byte c;
byte data_rcv[4];

/***********************
*       Funciones
**********************/

// Función para envio de comandos al potenciostato.

void setData(uint8_t command, int data_low, int data_high)
{
	mySerial.write(StartID);
	mySerial.write(command);
	mySerial.write(data_low);
	mySerial.write(data_high);
	mySerial.write(EndPKG);
}

void setStartPoint(double data)
{
	int dato = (int)(((double)data + (3.3 / 2.0)) / 3.3 * _resolution) - 1;
	uint8_t low = (dato & 0xFF) & 0x3F;
	uint8_t high = (((dato >> 8) << 2) & 0xFC) | (((dato & 0xFF) >> 6) & 0x03);
	setData(SetStartPoint, low, high);
}

void setFirstVertex(double data)
{
	int dato = (int)(((double)data + (3.3 / 2.0)) / 3.3 * _resolution) - 1;
	uint8_t low = (dato & 0xFF) & 0x3F;
	uint8_t high = (((dato >> 8) << 2) & 0xFC) | (((dato & 0xFF) >> 6) & 0x03);
	setData(SetFirstVertex, low, high);
}

void setSecondVertex(double data)
{
	int dato = (int)(((double)data + (3.3 / 2.0)) / 3.3 * _resolution) - 1;
	uint8_t low = (dato & 0xFF) & 0x3F;
	uint8_t high = (((dato >> 8) << 2) & 0xFC) | (((dato & 0xFF) >> 6) & 0x03);
	setData(SetSecondVertex, low, high);
}

void setZeroCrossing(int data)
{
	uint8_t low = (data & 0xFF) & 0x3F;
	uint8_t high = (((data >> 8) << 2) & 0xFC) | (((data & 0xFF) >> 6) & 0x03);
	setData(SetZeroCrossing, low, high);
}

void setSpeed(double data)
{
	int dato = (int)(data / 0.0008);
	uint8_t low = (dato & 0xFF) & 0x3F;
	uint8_t high = (((dato >> 8) << 2) & 0xFC) | (((dato & 0xFF) >> 6) & 0x03);
	setData(SetSpeed, low, high);
}

void startMeasurement()
{
	mySerial.write(StartID);
	mySerial.write(StartMeasurement);
	mySerial.write(EndPKG);
}

void stopMeasurement()
{
	mySerial.write(StartID);
	mySerial.write(StopMeasurement);
	mySerial.write(EndPKG);
}


void setup() {
  // Se inicializa el objeto serial.
  mySerial.begin(115200, SWSERIAL_8N1, D7, D8); // RX, TX
  // Se inicializa el puerto serial.
  Serial.begin(9600);
  delay(1000);
}

void loop() {
  if(Serial.available()>0){
    int inicio=Serial.read();
    Serial.println(inicio);
    if (inicio==49) {
      setFirstVertex(verticeSuperior);
      setSecondVertex(verticeInferior);
      setSpeed(velocidad);
      setZeroCrossing(ciclos);
      startMeasurement();
      isRunning = true;
    }
   }
  while ((mySerial.available() > 0) && isRunning)
  {
    c = mySerial.read();
    switch (c) {
      case 0xA0:
        //Serial.println("s");
        while ((mySerial.peek() == -1));
        data_rcv[0] = mySerial.read();
        while ((mySerial.peek() == -1));
        data_rcv[1] = mySerial.read();
        while ((mySerial.peek() == -1));
        data_rcv[2] = mySerial.read();
        while ((mySerial.peek() == -1));
        data_rcv[3] = mySerial.read();

        voltage = ((data_rcv[0] << 6) & 0x0FC0) | data_rcv[1];
        current = ((data_rcv[2] << 6) & 0x0FC0) | data_rcv[3];

        voltage = (float)((voltage - (_resolution / 2)) * (3.3 / _resolution));
        current = (float)((current - (_resolution / 2)) * (3.3 / _resolution)) + correccionZero;

        if(recorrido>0){
        diferenciaCorriente = fabs(lastCurrent-current);
        if(diferenciaCorriente < 0.02){
        if(contador>=1){
          current = (current+lastCurrent)/2;
        }
        if((voltage > 0.1) && (voltage < 1))
        {
          if (current >= oxiCurrent)
          {
            oxiCurrent = current;
            oxiVoltage = voltage;
          }
        }
        if((voltage < -0.1) && (voltage > -1.5))
        {
          if (current <= redCurrent)
          {
            redCurrent = current;
            redVoltage = voltage;
          }
        }
        if(voltage < -3)
        {
            Serial.print("---------------> max vox:");
            Serial.print(oxiVoltage);
            Serial.print(",");
            Serial.print(" , max cox:");       
            Serial.println(oxiCurrent);
            oxiCurrent = 0;
            oxiVoltage = 0;
        }
        if(voltage > 3)
        {
            Serial.print("---------------> max vre:");
            Serial.print(redVoltage);
            Serial.print(",");
            Serial.print(" , cre:");       
            Serial.print(redCurrent);
            redCurrent = 0;
            redVoltage = 0;
        }
        if(contador==2){
        Serial.print("vox:");
        Serial.print(oxiVoltage);
        Serial.print(",");
        Serial.print(",cox:");       
        Serial.print(oxiCurrent);
        Serial.print(",");
        
        Serial.print("vre:");
        Serial.print(redVoltage);
        Serial.print(",");
        Serial.print(",cre:");       
        Serial.print(redCurrent);
        Serial.print(",");
        
        Serial.print("v:");
        Serial.print(voltage);
        Serial.print(",");
        Serial.print(",c:");
        Serial.println(current);

        contador = 0;
        
        successfulRun = true;
        }
        contador=contador+1;
        }
        }
        recorrido=recorrido+1;
        lastCurrent = current;
        break;
      case 0xB0:
        // ("ACK");
        break;
      case 0xB1:
        // ("ENDRUN");
        stopMeasurement();
        isRunning = false;
        recorrido=0;
        break;
      default:
        break;
        
    }
  }

}
