# Video Streaming via UDP usando Python

---

* **Diego Andrés Gómez Polo**
* **Isabela María Sarmiento Llanos**
* **Juan Sebastián Bautista Rojas**

---
A continuación, una breve explicación de esta parte del proyecto y pasos a seguir para correrlo

## Configuración básica

* Este proyecto usa _OpenCV_ como librería para la lectura y visualización de los videos,
por ende, es necesario que instale los paquetes especificados en el archivo 
_requirements.txt_ usando `pip`. Para esto ubíquese en esta carpeta y ejecute: 
`pip install -r requirements.txt`.

* Antes de correr cliente y servidor recuerde modificar la ip y puerto asignado
al servidor en caso de que no estén corriendo ambos en la misma máquina. También 
recuerde modificar el puerto en caso de que el puerto 8000 (usado por defecto) 
esté ocupado.

* Por defecto el Streaming de video es de la cámara de la máquina. Si Python no
tiene permisos para usarla, el PC no cuenta con una o tiene un indice distinto
en el OS que el que se le asigna por defecto (0), es posible que salga error. 
Si quiere ver un video en particular en vez de la cámara, vaya dentro de _server.py_
y cambie el 0 en `cv2.VideoCapture(0)` a un _string_ con la ruta al archivo de 
video. Por ejemplo, `cv2.VideoCapture('./assets/video.mpeg')`