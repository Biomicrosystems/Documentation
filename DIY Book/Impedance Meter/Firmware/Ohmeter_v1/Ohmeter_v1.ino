
// Declaración de Variables - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#include <SoftwareSerial.h>
SoftwareSerial bluetooth(2,3); // RX, TX.
float   ohm1;
int     ledState = 13;  /* Se declara el pin 13 como Led State. */
String  orden = "";     /* Esta variable organiza la cadena de caracteres recibidos por UART BlUETOOTH. */
char    unCaracter;     /* Variable que almacena un caracter por tiempo. */
int     actADC = 0;
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - -


// Configuraciones  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  pinMode(ledState,OUTPUT);
  analogReference(INTERNAL);  //Ref = 1.1V
// Led State
  digitalWrite(ledState,HIGH);
  delay(500);
  digitalWrite(ledState,LOW);
  delay(500);
  digitalWrite(ledState,HIGH);
  delay(500);
  digitalWrite(ledState,LOW);
}
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - -


// Programa Principal - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
void loop(){
  
/* Se arma una cadena de caracteres a partir de los caracteres recibidos uno a uno por UART Bluetooth*/
  if (bluetooth.available()){
    while (bluetooth.available()){
      delay(3);
      unCaracter = bluetooth.read();
      orden += unCaracter;
    }
  }
  
/* Si el estado corresponde a ON, encendemos ADC. */
  if (orden == "ON"){
    digitalWrite(ledState,HIGH);
    Serial.write("Hemos recibido el comando ");
    Serial.println(orden);
    ohm1=0;
    actADC = 1;
    orden = ""; /* limpiamos la variable de activación para que no se repita la orden sin razón. */
  }
/* Si el estado corresponde a OFF, apagamos ADC. */
  if (orden == "OFF"){
    digitalWrite(ledState,LOW);
    Serial.write("Hemos recibido el comando ");
    Serial.println(orden);
    actADC = 0;
    orden = ""; /* limpiamos la variable de activación para que no se repita la orden sin razón. */
  }
  
// Lectura Análoga    
  if (actADC == 1){
    for (int i=0; i<20; i++){
      ohm1=analogRead(0)+ohm1;
      delay(100);
    }
    ohm1=ohm1/20;
    ohm1 = ohm1 * 10.96;
    ohm1 = ohm1 / 1023;
    bluetooth.print(ohm1);
    Serial.println(ohm1);
  }
  
}
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - -
