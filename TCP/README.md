# lab3-redes
---
En este repositorio se encuentra el código fuente usado para la solución del tercer laboratorio de infraestructura de comunicaciones.

### Estructura 
Hay 3 archivos principales escritos en Python que se usaron para este laboratorio: 

* **client_test.py:** Aquí se encuentra la implementación del cliente
* **server_test.py:** Contiene la implementación básica de un servidor que atiende una sola conexión
* **server_test_threads.py:** Implementación final del servidor MultiThread que soporta multiples conexiones. Este es el servidor usado para pruebas.

Luego se tienen algunos archivos y carpetas necesarios para el correcto funcionamiento del cliente y servidor:

* **save_content:** Folder que usan los clientes para guardar los archivos que reciben del servidor.
* **Lab 3 config.md:** Archivo con algunas configuraciones hechas a la máquina virtual usada en este lab. Además contiene información útil para la configuración inicial del enterno Ubuntu del servidor
* **TCP Sampler.jmx:** Archivo con el grupo de pruebas usado en JMeter
* **video1.mkv, video2.webm:** Videos disponibles en el servidor para ser enviados al cliente.



