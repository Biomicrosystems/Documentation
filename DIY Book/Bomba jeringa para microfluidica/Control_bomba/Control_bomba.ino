// Define los pines del driver
#define DIR_PIN 2
#define STEP_PIN 3
#define ENABLE_PIN 4
#define pinRelay 7

// Define el número de pasos por revolución y el modo de micropasos
#define STEPS_PER_REV 950 //pasos por revolución, pasos que permite completar una revolución

// Crea una instancia de la librería AccelStepper
#include <AccelStepper.h>
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

void setup() {
  
  // Configura el pin de habilitación como salida
  pinMode(ENABLE_PIN, OUTPUT);
  // Deshabilita el driver
  digitalWrite(ENABLE_PIN, HIGH);
  // Establece la velocidad y aceleración máximas
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(100);

  //rele
  pinMode(pinRelay, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("¡Encendido!");
  Serial.println("Ingrese la cantidad que quiere dosificar:");
}

void loop() {
  int input;
  float pasos;
  float cantidad_dosificar;
  char buffer[32];
  int bytes_read = 0;
  
  while (Serial.available() == 0) {
    // Esperar hasta que haya datos disponibles en el puerto serie
  }
  //leer los datos del puerto serie hasta que se reciba un caracter
  bytes_read = Serial.readBytesUntil ('\n', buffer, sizeof(buffer));
  //activar rele
  digitalWrite(pinRelay, HIGH);

  //convertir los datos leidos a un número flotante
  cantidad_dosificar = atof(buffer);
  Serial.println("Empezando a dosificar: ");
  Serial.println(cantidad_dosificar);

  //habilitar el driver 
  digitalWrite(ENABLE_PIN, LOW);

  //Calcula la cantidad de pasos necesarios para dosificar esa cantidad
  pasos = (cantidad_dosificar+17.897)/0.5865;
  Serial.println("numero de pasos que dio el motor:");
  Serial.println(pasos);

  // Mueve el motor la cantidad de pasos indicada
  stepper.move(-1*pasos);
  stepper.runToPosition();
  Serial.println("Termine de dosificar");
  Serial.println("Ingrese la cantidad que quiere dosificar:");

  //apagar rele
  delay(500);
  digitalWrite(pinRelay, LOW);
  
  
}
