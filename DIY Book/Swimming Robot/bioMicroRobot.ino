#include <ESP8266WiFi.h>
#include <Wire.h>
#include <MechaQMC5883.h>
#include <SoftwareSerial.h>


/* el link de referencia fue https://www.esploradores.com/access-point-servidor-web-nodemcu/ */

const char ssid[] = "NodeMCU-ESP8266";    //Definimos la SSDI de nuestro servidor WiFi -nombre de red-.
const char password[] = "12345678";       //Definimos la contraseña de nuestro servidor.
WiFiServer server(80);                    //Definimos el puerto de comunicaciones (el puerto 80 se usa para la comunicación entre el servidor y el cliente).

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

/**************************************
*  Parámetros de recorrido biosensor
************************************/

int _resolution = 4096 ; //¡NO CAMBIAR ESTE PARÁMETRO!
double zero = 0 ; //Centro del ciclo o zero del ciclo.
double verticeInferior = -0.9; //Voltaje mínimo del ciclo.
double verticeSuperior = 0.9; //Voltaje máximo del ciclo.
int ciclos = 20 ; //Cuántas veces pasa por el inicio o por el zero.
double velocidad = 0.050 ; //Velocidad de ciclo.
double correccionZero = 1.15 ; //Corrección del zero.

/***************************
*    Variables Medibles
**************************/

int x, y, z; // Medición de ejes en el magnetómetro.
int azimuth; // Angulo del sensor con respecto al norte magnético de la tierra.
int desiredAngle; // Angulo al que se desea llegar.
float voltage; // Voltaje salida del biosensor.
float current; // Corriente medida por el biosensor.
float lastCurrent; // Última corriente medida.
float oxiCurrent; // Corriente más alta medida.
float redCurrent; // Corriente más baja medida.
float oxiVoltage; // Voltaje en el que se genero la oxiCurrent.
float redVoltage; // Voltaje en el que se genero la redCurrent.
int PWML; // PWM del motor izquierdo.
int PWMR; // PWM del motor derecho.
int bioL; // Dato decisión de dirección biosensor izquierdo.
int bioR; // Dato decisión de dirección biosensor derecho.

/***************************
*     Variables Dummies
**************************/

bool isRunning = false; // Permite o no la toma de datos del biosensor.
bool successfulRun = false; // Permite verificar si se completó o no el ciclo de medición del biosensor.
int recorrido = 0; // Identifica si ya se dió el primer ciclo para evitar errores a la hora de calcular la diferencia entre el dato anterior y el actual en el biosensor.
float diferenciaCorriente; // Permite mitigar el error de posibles ruidos en la medición del biosensor dado que el patrón de los datos no supera el 0.02 entre el anterior y el actual.
int contador = 0; // Permite verificar la cantidad de ciclos del potenciostato para realizar un promedio entre los últimos 3 valores.
bool simulado = true; // Verifica si los valores del biosensor son simulados o no.
float toleranciaBiosensor = 2; // El valor máximo de diferencia entre los datos medidos en el biosensor izquierdo y derecho.
String directionL; // Se envía al cliente para identificar la dirección del motor izquierdo.
String directionR; // Se envía al cliente para identificar la dirección del motor derecho.
byte c; // Variables para guardar datos de envio y recepción potenciostato.
byte data_rcv[4]; // Variables para guardar datos de envio y recepción potenciostato.

/**************************
*         Objetos
*************************/
MechaQMC5883 qmc;
// Se inicializa el objeto serial en los pines D7 y D8 correspondientes a Rx y Tx. 
SoftwareSerial mySerial(D7 , D8); // RX, TX
// La librería maneja las interrupciones automaticamente al llamar la función read() y/o write().
// Esto quiere decir que no hay necesiad de crear una función Handler().

/******************
*  Pines motor A (derecho)
*****************/

const int PINA = D2;

/******************
*  Pines motor B (izquierdo)
*****************/

const int PINB = D5;


/***************************
*    Funciones bioSensor
**************************/

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

/****************************
*      Inicio setup()
***************************/

void setup() {
  Serial.begin(9600);

  /////////////// Magnetómetro ///////////////

  Wire.begin(D4, D1); //Wire.begin(int sda, int scl), esto quiere decir que estamos usando el D4 como sda y el D1 como scl
  qmc.init();
  qmc.setMode(Mode_Continuous,ODR_10Hz,RNG_2G,OSR_512);

  //////////////// Biosensor ////////////////
  
  // Se inicializa el objeto serial.
  mySerial.begin(115200, SWSERIAL_8N1, D7, D8); // RX, TX

  ///////////////// Motores /////////////////

  pinMode(PINA, OUTPUT);
  pinMode(PINB, OUTPUT);  

  /////////////////// Wifi ///////////////////

  server.begin();                         //inicializamos el servidor
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);            //Red con clave, en el canal 1 y visible
  Serial.println();
  Serial.print("Direccion IP Access Point - por defecto: ");      //Imprime la dirección IP
  Serial.println(WiFi.softAPIP()); 
  Serial.print("Direccion MAC Access Point: ");                   //Imprime la dirección MAC
  Serial.println(WiFi.softAPmacAddress()); 

  delay(3000);
  qmc.read(&x, &y, &z,&azimuth);
  delay(100);
  desiredAngle = azimuth;
}

/****************************
*      Inicio loop()
***************************/

void loop() {

  /////////////// Magnetómetro ///////////////

  qmc.read(&x, &y, &z,&azimuth);
  delay(100);

  //////////////// Biosensor ////////////////

  if(simulado == false){
  setFirstVertex(verticeSuperior);
  setSecondVertex(verticeInferior);
  setSpeed(velocidad);
  setZeroCrossing(ciclos);
  startMeasurement();
  isRunning = true;
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
  else{
    bioL = bioR = 100;
  }

  ///////////////// Motores /////////////////

  /*if(abs(bioL-bioR) > toleranciaBiosensor){
    if(bioL > bioR) // Debe girar a la izquierda.
    {
      PWML = 66;
      PWMR = 78;
    }
    else // Debe girar a la derecha.
    {
      PWML = 66;
      PWMR = 78;
    }

  }
  else{*/
  if(abs(desiredAngle - azimuth) > 5 )  // Si la diferencia entre el angulo deseado y el angulo real es mayor a 5°, se debe realizar un cambio.
  {
    if(desiredAngle < azimuth) // Debe girar a la izquierda.
    {
      PWML = 66;
      PWMR = 80;
      directionL = "Turn Left";
      directionR = "";
    }
    else // Debe girar a la derecha.
    {
      PWML = 70;
      PWMR = 70;
      directionL = "";
      directionR = "Turn Right";
    }
  }
  else // Debe mantener el curso hacia adelante.
  {
    PWML = 66;
    PWMR = 77;
    directionL = "Straight";
    directionR = "Straight";
  }
  //}

  analogWrite(PINA, PWMR);
  analogWrite(PINB, PWML);

  /////////////////// Wifi ///////////////////

  // Comprueba si el cliente ha conectado
WiFiClient client = server.available(); 
  if (!client) {
    return;
  }
  // Espera hasta que el cliente envía alguna petición.
  Serial.println("nuevo cliente");
  while(!client.available()){
    delay(1);
  }
  // Imprime el número de clientes conectados.
  Serial.printf("Clientes conectados al Access Point: %dn", WiFi.softAPgetStationNum());

  // Se envía respuesta al cliente acompañado de una línea en blanco.
  client.println("HTTP/1.1 200 OK");
  client.println("");  

  // Se envía el contenido del HTML.
  client.print("<html><head> <meta http-equiv='refresh' content='1' /><style>table {   font-family: arial, sans-serif; border-collapse: collapse; width: 100%; }");
  client.print("td, th { border: 0px solid #dddddd; text-align: center; padding: 8px; }");
  client.print("</style> </head> <body>");
  client.print("<h2 align='center' >BiomicroRobot V1</h2>");
  client.print("<table style='width:100%'>");
  client.print("<tr> <th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'></th>");
  client.print("<th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Fixed Angle</th>");
  client.print("<th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th></tr>");
  client.print("<tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th>");
  client.print("<th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");
  
  // Angulo deseado.
  client.print("<p style='color:blue;'>");
  client.print(desiredAngle);
  client.print("</p>");

  client.print("</th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th></tr>");
  client.print("<tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Biosensor Left </th>");
  client.print("<th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%' rowspan='5'> ");
  client.print("<canvas id='myRobot' width='200' height='200' style='border:0px solid #CCCCCC;'> Your browser does not support the HTML canvas tag.</canvas>");
  client.print("<script> var c = document.getElementById('myRobot'); var ctx = c.getContext('2d'); ctx.moveTo(100,1); ctx.lineTo(170,50); ctx.stroke(); ctx.moveTo(100,1); ctx.lineTo(30,50); ctx.stroke(); ctx.moveTo(170,50); ctx.lineTo(170,190); ctx.stroke(); ctx.moveTo(30,50); ctx.lineTo(30,190); ctx.stroke(); ctx.moveTo(30,190); ctx.lineTo(170,190); ctx.stroke(); ctx.beginPath(); ctx.arc(15, 138, 14, 0, 2 * Math.PI); ctx.stroke(); ctx.beginPath(); ctx.arc(185, 138, 14, 0, 2 * Math.PI); ctx.stroke(); </script>");
  client.print(" </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Biosensor Right </th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");

  // Biosensor izquierdo
  client.print("<p style='color:blue;'>");
  client.print(bioL);  // bioL        
  client.print("</p>");

  client.print(" </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");

  // Biosensor derecho
  client.print("<p style='color:blue;'>");
  client.print(bioR);  // bioR       
  client.print("</p>");

  client.print(" </th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th>");
  client.print("</tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>PWM Left  </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>PWM Right </th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");

  // PWM Left
  client.print("<p style='color:blue;'>");
  client.print(float(PWML)/71*100);         
  client.print("&#37;<br>(");
  client.print(PWML);
  client.print(")</p>"); 

  client.print("</th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");

  // PWM Right
  client.print("<p style='color:blue;'>");
  client.print(float(PWMR)/90*100);         
  client.print("&#37;<br>(");
  client.print(PWMR);
  client.print(")</p>");

  client.print("</th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Direction Left</th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Yaw </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>Direction Right</th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");
  // Direction Left
  if (directionL=="Turn Left")
  {
    client.print("<p style='color:red;'>");
    client.print(directionL);
    client.print("</p>");
  }
  else
  {
    client.print("<p style='color:green;'>");
    client.print(directionL);
    client.print("</p>");
  }
  client.print(" </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");

  // Angulo con respecto al norte
  client.print("<p style='color:blue;'>");
  client.print(azimuth);      
  client.print("</p>");

  client.print("</th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'>");
  // Direction Right
  if (directionR=="Turn Right")
  {
    client.print("<p style='color:red;'>");
    client.print(directionR);
    client.print("</p>");
  }
  else
  {
    client.print("<p style='color:green;'>");
    client.print(directionR);
    client.print("</p>");
  }            
  client.print("</th></tr><tr><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th><th style='width:33%; background-color:#EEEEEE;vertical-align:center;text-align:center; width:33%'> </th></tr></tr></table></body></html>");
  
  // The HTTP response ends with another blank line:
  client.println();

}
