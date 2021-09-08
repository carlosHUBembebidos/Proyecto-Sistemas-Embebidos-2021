Autor: Carlos Armando Rodríguez Lema


El archivo Prueba_2.py es un archivo compatible con python, este archivo contiene el código de programación de la Raspberry pi.
El código verifica y realiza las reservaciones de los usuarios, también elimina y envía las órdenes a través de comunicación serial
a la tarjeta de Arduino para accionar el motor por pasos y el indicador led. En el código también se configura la Raspberry para que
se comunique con una aplicación a través de una conexión de red local.

El archivo main.c fue elaborado con la herramienta AtmelStudio. En este código se programa la tarjeta de Arduino UNO utilizando lenguaje C
y se controla el funcionamiento del led indicador, además de controlar el motor paso a paso cada vez que la Raspberry así lo decida siempre
y cuando se haya producido una interripción a través de los botones implementados en el puerto D0 y D1 de nuestra tarjeta

Enlace Video Proyecto: https://youtu.be/apDYtlrCSCE
