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
_requirements.txt_ usando `pip`. Pero, antes de esto, si se está en una máquina con Linux lo más probables es que haya
que instalar antes el paquete usando apt de la suiente manera: `apt install python3-opencv`, luego si podemos proceder a instalar
los bindings de OpenCV para Python . Para esto ubíquese en la carpeta 'Streaming' y ejecute: 
`pip install -r requirements.txt`, en este archivo están los paquetes y versiones necesarias. 
Si el paquete de OpenCV por defecto molesta instalando, 
puede instalar _opencv-contrib-python_ como reemplazo, esto ejecutando: 
`pip install opencv-contrib-python`. 

* Recuerde modificar el puerto tanto en cliente como
 en servidor en caso de que el puerto 10000 (usado por defecto) 
esté ocupado.

* Primero se corre el servidor. Luego, al correr un cliente se le mostrará
la opción para escoger a cuál de los dos canales de streaming conectarse. 
En cada uno hay un video diferente. Luego de conectado, el cliente puede
salirse de la transmisión presionando la tecla `q` , al hacer esto se le preguntará
nuevamente un canal para escoger, si presiona `q` de nuevo, terminará el programa.


### Importante
Que el programa corra bien en Multicast depende enteramente de que la interfaz de red usada soporte
Multicasting en primer lugar. En linux (y probablemente en Mac También), podemos checkear que está bien si,
luego de correr el cliente, se ejecuta `netstat -g` para ver los grupos de Multicast del sistema operativo.
Si todo anda bien,al escoger el canal 1, debe haber un grupo con la dirección 224.3.29.71, la cual se define en código. Importante
que este corriendo el cliente al momento de ejecutar `netstat`, porque al acabar el programa el OS elimina el
grupo de la interfaz de red.

---

## Links, Referencias



### Streaming

* https://medium.com/@fromtheast/fast-camera-live-streaming-with-udp-opencv-de2f84c73562
* https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3/49095089
* https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
* https://stackoverflow.com/questions/43315349/how-to-resize-frames-from-video-with-aspect-ratio
* https://stackoverflow.com/questions/46912475/python-webcam-stream-over-udp-socket
* https://docs.python.org/3/library/struct.html

### Multicast
* https://pymotw.com/3/socket/multicast.html
* https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
* https://unix.stackexchange.com/questions/25872/how-can-i-know-if-ip-multicast-is-enabled
* https://wiki.python.org/moin/UdpCommunication
* https://stackoverflow.com/questions/10692956/what-does-it-mean-to-bind-a-multicast-udp-socket~~~~
