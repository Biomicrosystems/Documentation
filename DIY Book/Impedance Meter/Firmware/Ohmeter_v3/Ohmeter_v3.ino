#include <EEPROM.h>

// Declaración de Variables - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
float   ohm1;
int     addr = 0;
int     ledState = 13;  /* Se declara el pin 13 como Led State. */
String  orden = "";     /* Esta variable organiza la cadena de caracteres recibidos por UART BlUETOOTH. */
char    unCaracter;     /* Variable que almacena un caracter por tiempo. */
int     actADC = 0;
int     lectura = 0;
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - -


// Configuraciones  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
void setup() {
  Serial.begin(9600);
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
  if (Serial.available()){
    while (Serial.available()){
      delay(3);
      unCaracter = Serial.read();
      orden += unCaracter;
    }
  }
  
/* Si el estado corresponde a ON, encendemos ADC. */
  if (orden == "ON"){
    digitalWrite(ledState,HIGH);
    ohm1=0;
    actADC = 1;
    orden = ""; /* limpiamos la variable de activación para que no se repita la orden sin razón. */
  }
/* Si el estado corresponde a OFF, apagamos ADC. */
  if (orden == "OFF"){
    digitalWrite(ledState,LOW);
    actADC = 0;
    orden = ""; /* limpiamos la variable de activación para que no se repita la orden sin razón. */
  }
/* Si el estado corresponde a READ, apagamos ADC. */
  if (orden == "READ"){
    lectura = 1;
    orden = ""; /* limpiamos la variable de activación para que no se repita la orden sin razón. */
  }
  
// Lectura Análoga    
  if (actADC == 1){
    addr = 0;
    for (int i=0; i<60; i++){
      ohm1=analogRead(0)/4;
      EEPROM.write(addr, ohm1);
      addr = addr + 1;
      delay(990);
      ohm1 = ohm1*4;
      ohm1 = ohm1 * 10.96;
      ohm1 = ohm1 / 1023;
      Serial.println(ohm1);
    }
    actADC = 0;
    Serial.print('F');
    Serial.print('I');
    Serial.println('N');
  }

// Lectura EEPROM
  if (lectura == 1){
    addr = 0;
    for (int i=0; i<60; i++){
      ohm1 = EEPROM.read(addr);
      ohm1 = ohm1*4;
      ohm1 = ohm1 * 10.96;
      ohm1 = ohm1 / 1023;
      Serial.print(addr);
      Serial.print("\t");
      Serial.println(ohm1);
      addr = addr + 1;
      delay(500);
    }
    lectura = 0;
  }
  
}
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - -
