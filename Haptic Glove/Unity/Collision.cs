using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Collision : MonoBehaviour
{
    
    private void OnTriggerEnter(Collider collision)
    {   
        
        string colliderTag = collision.gameObject.tag;
        // Realiza acciones específicas según la etiqueta del colisionador
        switch (colliderTag)
        {
            case "ColliderPalm":
                RotarCubo.Instance.retro("P,0");
                Debug.Log("Ha tocado la palma.");
                break;
            case "ColliderIndice1":
                RotarCubo.Instance.retro("P,4");
                Debug.Log("Ha tocado el indice.");
                break;
            case "ColliderMiddle1":
                RotarCubo.Instance.retro("P,5");
                Debug.Log("Ha tocado el medio.");
                break;
            case "ColliderPinky1":
                RotarCubo.Instance.retro("P,1");
                Debug.Log("Ha tocado el meñique.");
                break;
            case "ColliderRing1":
                RotarCubo.Instance.retro("P,2");
                Debug.Log("Ha tocado el anular.");
                break;
            case "ColliderThumb2":
                RotarCubo.Instance.retro("P,3");
                Debug.Log("Ha tocado el pulgar.");
                break;
            //case "Do":
                //RotarCubo.Instance.retro("P,6,262");
                //Debug.Log("Ha tocado la tecla Do.");
                //break;
            //case "Do#":
                //RotarCubo.Instance.retro("P,6,277");
                //Debug.Log("Ha tocado la tecla Do#.");
                //break;
            //case "Re":
                //RotarCubo.Instance.retro("P,6,294");
                //Debug.Log("Ha tocado la tecla Re.");
                //break;
            //case "Re#":
                //RotarCubo.Instance.retro("P,6,311");
                //Debug.Log("Ha tocado la tecla Re#.");
                //break;
            //case "Mi":
                //RotarCubo.Instance.retro("P,6,330");
                //Debug.Log("Ha tocado la tecla Mi.");
                //break;
            //case "Fa":
                //RotarCubo.Instance.retro("P,6,349");
                //Debug.Log("Ha tocado la tecla Fa.");
                //break;
            //case "Fa#":
                //RotarCubo.Instance.retro("P,6,370");
                //Debug.Log("Ha tocado la tecla Fa#.");
                //break;
            //case "Sol":
                //RotarCubo.Instance.retro("P,6,392");
                //Debug.Log("Ha tocado la tecla Sol.");
                //break;
            //case "Sol#":
                //RotarCubo.Instance.retro("P,6,415");
                //Debug.Log("Ha tocado la tecla Sol#.");
                //break;
            //case "La":
                //RotarCubo.Instance.retro("P,6,440");
                //Debug.Log("Ha tocado la tecla La.");
                //break;
            //case "La#":
                //RotarCubo.Instance.retro("P,6,466");
                //Debug.Log("Ha tocado la tecla La#.");
                //break;
            //case "Si":
                //RotarCubo.Instance.retro("P,6,494");
                //Debug.Log("Ha tocado la tecla Si.");
                //break;
            default:
                //RotarCubo.Instance.retro("Yolo");
                Debug.Log("Colisión con objeto no reconocido " + colliderTag);
                break;
        }
        
    }

    private void OnTriggerExit(Collider collision)
    {   
        
        string colliderTag = collision.gameObject.tag;
        // Realiza acciones específicas según la etiqueta del colisionador
        switch (colliderTag)
        {
            case "ColliderPalm":
                RotarCubo.Instance.retro("A,0");
                Debug.Log("Saliendo de tocar la palma.");
                break;
            case "ColliderIndice1":
                RotarCubo.Instance.retro("A,4");
                Debug.Log("Saliendo de tocar el indice.");
                break;
            case "ColliderMiddle1":
                RotarCubo.Instance.retro("A,5");
                Debug.Log("Saliendo de tocar el medio.");
                break;
            case "ColliderPinky1":
                RotarCubo.Instance.retro("A,1");
                Debug.Log("Saliendo de tocar el meñique.");
                break;
            case "ColliderRing1":
                RotarCubo.Instance.retro("A,2");
                Debug.Log("Saliendo de tocar el anular.");
                break;
            case "ColliderThumb2":
                RotarCubo.Instance.retro("A,3");
                Debug.Log("Saliendo de tocar el pulgar.");
                break;
            //case "Do":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Do.");
                //break;
            //case "Do#":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Do#.");
                //break;
            //case "Re":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Re.");
                //break;
            //case "Re#":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Re#.");
                //break;
            //case "Mi":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Mi.");
                //break;
            //case "Fa":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Fa.");
                //break;
            //case "Fa#":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Fa#.");
                //break;
            //case "Sol":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Sol.");
                //break;
            //case "Sol#":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Sol#.");
                //break;
            //case "La":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla La.");
                //break;
            //case "La#":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla La#.");
                //break;
            //case "Si":
                //RotarCubo.Instance.retro("A,6,0");
                //Debug.Log("Saliendo de tocar la tecla Si.");
                //break;
            default:
                //RotarCubo.Instance.retro("Yolo");
                Debug.Log("Saliendo colisión con objeto no reconocido " + colliderTag);
                break;
        }
        
    }
}
