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
recuerde modificar el puerto en caso de que el puerto 10000 (usado por defecto) 
esté ocupado.

* Primero se corren los clientes y luego el servidor en este caso. Sino, 
el servidor queda esperando confirmación de los clientes y se activa el timeout.
Para modificar este comportamiento habría que quitar el timeout en servidor y
modificar el protocolo para que el cliente no espere el mensaje de servidor ni mande 
el ack, si no que empiece enseguida recibir paquetes.

* Por defecto el Streaming de video es de la cámara de la máquina. Si Python no
tiene permisos para usarla, el PC no cuenta con una o tiene un indice distinto
en el OS que el que se le asigna por defecto (0), es posible que salga error. 
Si quiere ver un video en particular en vez de la cámara, vaya dentro de _server.py_
y cambie el 0 en `cv2.VideoCapture(0)` a un _string_ con la ruta al archivo de 
video. Por ejemplo, `cv2.VideoCapture('./assets/video.mpeg')`

### Importante
Que el programa corra bien en Multicast depende enteramente de que la interfaz de red usada soporte
Multicasting en primer lugar. En linux (y probablemente en Mac También), podemos checkear que está bien si,
luego de correr el cliente, se ejecuta `netstat -g` para ver los grupos de Multicast del sistema operativo.
Si todo anda bien, debe haber un grupo con la dirección 224.3.29.71, la cual se define en código. Importante
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
* https://stackoverflow.com/questions/10692956/what-does-it-mean-to-bind-a-multicast-udp-socket
