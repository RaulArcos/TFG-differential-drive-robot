# DESARROLLO DE SISTEMA DE CONTROL DE UN ROBOT DIFERENCIAL MÓVIL EMPLEANDO ROS PARA NAVEGACIÓN AUTÓNOMA

Proyecto realizado como trabajo de fin de grado para el Laboratio de Robótica de la Escuela Superior de Ingeniería, UCA.
## Resumen

En este proyecto se ha empleado ROS para el control de un robot diferencial, utilizando un modelo real no comercial. Para ello, se han implementado paquetes ya existentes compatibles con configuraciones adaptadas, así como paquetes desarrollados específicamente para el proyecto. 

<p align="center">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/8aa0af8d-b9e6-47ad-ba7f-98b6ee18cedf" alt="RAH01-Front-nobackground" width="350">
</p>

El resultado es un robot que cuenta con capacidad de navegación autónoma además de detección de personas, junto a una interfaz web que permite el control, visualización del estado, posición y datos del robot en tiempo real a través de un PC de forma inalámbrica.

## Objetivos del Proyecto
- Estudiar el robot diferencial móvil del laboratorio de robótica.
- Estudiar los paquetes de trabajo ROS en la plataforma móvil.
- Definir los requisitos de diseño software para ROS.
- Definir los parámetros para el movimiento del robot diferencial.
- Definir los paquetes de ROS necesarios para mapeo y navegación autónoma.
- Integrar los paquetes en un entorno de ROS.
- Configurar los parámetros de los paquetes de ROS.
- Preparar el entorno hardware con dos computadores empotrados.
- Desarrollar una interfaz web para el uso del robot por parte del usuario.
- Desarrollar una rutina de movimiento empleando planificador ROS con gestión de eventos al detectar objetos.

## Resultados
### Navegación Autónoma

- Se han integrado los paquetes de ROS necesarios para la navegación autónoma del robot junto con sus respectivos ajustes de parámetros.
<p align="center">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/20a447b2-ddd2-4fc0-9d1c-96faca5c6fe4" alt="resultados - navegacion funcionando" width="400">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/c940404a-ed60-4ca7-9ffb-9c4ffc0b6e48" alt="robot-navegating" width="350">
</p>

### Visión Artificial
- Se ha desarrollado un paquete propio de ROS que utiliza la visión artificial para detectar personas.
<p align="center">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/f872e9b6-c274-47dc-b694-c48851620cea" alt="RAH01-People" width="400">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/4d02d726-b176-4441-a5c4-f76590da4c2c" alt="RAH01-People-Distance" width="350">
</p>

### Interfaz Web
- Se ha desarrollado una interfaz web para visualizar y controlar el robot de forma remota.
<p align="center">
  <img src="https://github.com/RaulArcos/TFG-differential-drive-robot/assets/48330837/2d6b29d4-4b20-40ac-a77f-8f2988e1253c" alt="RAH01-Web-Interface" width="600">
</p>

## Equipo de Trabajo
- Raúl Arcos Herrera: Desarrollador
- Arturo Morgado: Tutor
