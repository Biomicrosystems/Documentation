using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using Oculus;
using System.Globalization;


public class RotarCubo : MonoBehaviour
{
    OVRHand rightHand; // Cambia a Right para la mano derecha
    public static RotarCubo Instance { get; private set; }
    private SerialPort serialPort;
    public Vector3 posicionFija = new Vector3(0f, 0f, 0f);
    Quaternion datosRotacion;
    Vector3 datosMovimiento;

    private void Awake(){
        if(Instance == null){
            Instance=this;
        }
        else
        {
            Destroy(gameObject);
        }
        serialPort=new SerialPort("COM5",115200);//Cambiar el número del COM de acuerdo al observado al cargar el código en la ESP32
        serialPort.ReadTimeout=250;
        serialPort.Open();

        datosRotacion=Quaternion.identity;
        datosMovimiento=posicionFija;
    }
    public string data; //Variable para leer los datos enviados de la ESP32
    float w,x,y,z; //Variabbles para almacenar los datos correspondientes de los quaterniones
    float dedo1,dedo2,dedo3,dedo4,dedo5; //Variables para almacenar los datos correspondientes de los dedos

    public Transform dorso;

    public Transform dedo1Obj;
    public Transform dedo1Obj_2;

    public Transform dedo2Obj;
    public Transform dedo2Obj_2;
    public Transform dedo2Obj_3;

    public Transform dedo3Obj;
    public Transform dedo3Obj_2;
    public Transform dedo3Obj_3;

    public Transform dedo4Obj;
    public Transform dedo4Obj_2;
    public Transform dedo4Obj_3;

    public Transform dedo5Obj;
    public Transform dedo5Obj_2;
    public Transform dedo5Obj_3;

    // Movimientos
    float aceleracionX, aceleracionY, aceleracionZ;
    float velocidadX=0, velocidadY=0, velocidadZ=0;
    float posicionX=0, posicionY=0, posicionZ=0;
    float tiempoAnterior;
    
    void Start()
    {
        tiempoAnterior = Time.time;
    }

    public void retro(string num)
    {
        serialPort.Write(num+'\n');
        Debug.Log("Se manda un: " + num);
    }

    // Update is called once per frame
    void Update()
    {
        try{
            if(serialPort.IsOpen){
                //Leer por líneas los datos recibidos
                data=serialPort.ReadLine();
                //print(data);
                //Limpiar el buffer del puerto serie
                serialPort.DiscardInBuffer();
                //Obtener un string con diferentes posiciones separando la data por ","
                string[] datos=data.Split(",");
                //Convertir los datos correspondientes a cada variable del quaternion en float
                w=float.Parse(datos[0], CultureInfo.InvariantCulture);
                x=float.Parse(datos[1], CultureInfo.InvariantCulture);
                y=float.Parse(datos[2], CultureInfo.InvariantCulture);
                z=float.Parse(datos[3], CultureInfo.InvariantCulture);
                aceleracionX=float.Parse(datos[9], CultureInfo.InvariantCulture)*9.81f/8192f;
                aceleracionY=float.Parse(datos[10], CultureInfo.InvariantCulture)*9.81f/8192f;
                aceleracionZ=float.Parse(datos[11], CultureInfo.InvariantCulture)*9.81f/8192f;
                datosRotacion.Set(z, -x, -y, w);
                Debug.Log("Ace X: "+aceleracionX+" Ace Y: "+aceleracionY+" Ace Z: "+aceleracionZ);

                float tiempoActual=Time.time;
                float deltaTime= tiempoActual-tiempoAnterior;
                Debug.Log("Delta t: "+deltaTime);
                //Velocidades
                velocidadX = (aceleracionZ*deltaTime);
                velocidadY = (-aceleracionX*deltaTime);
                velocidadZ = (-aceleracionY*deltaTime);  
                //Posiciones
                posicionX =(velocidadX*deltaTime+0.5f*aceleracionX*deltaTime*deltaTime)*10;
                posicionY =(velocidadY*deltaTime+0.5f*aceleracionY*deltaTime*deltaTime)*10;
                posicionZ =(velocidadZ*deltaTime+0.5f*aceleracionZ*deltaTime*deltaTime)*10;
                Debug.Log("X: "+posicionX+" Y: "+posicionY+" Z: "+posicionZ);
                //Actualizar tiempo anterior
                tiempoAnterior=tiempoActual;
                //Actualizar datos posicion
                datosMovimiento.Set(posicionX,posicionY,posicionZ);
                //Mano
                dorso.rotation = datosRotacion;
                dorso.transform.position = datosMovimiento;

                //Datos dedos
                dedo1=float.Parse(datos[4], CultureInfo.InvariantCulture);
                dedo2=float.Parse(datos[5], CultureInfo.InvariantCulture);
                dedo3=float.Parse(datos[6], CultureInfo.InvariantCulture);
                dedo4=float.Parse(datos[7], CultureInfo.InvariantCulture);
                dedo5=float.Parse(datos[8], CultureInfo.InvariantCulture);
                
                dedo1Obj.localRotation = Quaternion.AngleAxis(3*dedo1/4, Vector3.forward);
                dedo1Obj_2.localRotation = Quaternion.AngleAxis(dedo1/4, Vector3.forward);
                dedo2Obj.localRotation = Quaternion.AngleAxis(5*dedo2/8, Vector3.forward);
                dedo2Obj_2.localRotation = Quaternion.AngleAxis(5*dedo2/16, Vector3.forward);
                dedo2Obj_3.localRotation = Quaternion.Euler(0,0, dedo2/16);
                dedo3Obj.localRotation = Quaternion.AngleAxis(5*dedo3/8, Vector3.forward);
                dedo3Obj_2.localRotation = Quaternion.AngleAxis(5*dedo3/16, Vector3.forward);
                dedo3Obj_3.localRotation = Quaternion.Euler(0,0,dedo3/16);
                dedo4Obj.localRotation = Quaternion.AngleAxis(5*dedo4/8, Vector3.forward);
                dedo4Obj_2.localRotation = Quaternion.AngleAxis(5*dedo4/16, Vector3.forward);
                dedo4Obj_3.localRotation = Quaternion.Euler(0,0,dedo4/16);
                dedo5Obj.localRotation = Quaternion.AngleAxis(5*dedo5/8, Vector3.forward);
                dedo5Obj_2.localRotation = Quaternion.AngleAxis(5*dedo5/16, Vector3.forward);
                dedo5Obj_3.localRotation = Quaternion.Euler(0,0,dedo5/16);
                
                transform.position= posicionFija;
            }
        } catch (System.Exception ex){
            ex=new System.Exception();
            Debug.Log("Se produjo un error al leer los datos del puerto serie: " + ex.Message);
        }
    }
    
}
