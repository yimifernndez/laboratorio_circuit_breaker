# Laboratorio: Sistema que aprende a fallar

## Integrantes

- Nombre del estudiante: Jimmy Fernandez
- Grupo: ING DE SISTEMAS
- Tema: Circuit Breaker en sistemas distribuidos

---

## Descripción general

Este laboratorio tiene como objetivo analizar e implementar un mecanismo de Circuit Breaker en un sistema distribuido compuesto por un gateway y varios servicios independientes.

El sistema cuenta con los siguientes servicios:

- Gateway
- Servicio de mascotas
- Servicio de usuarios
- Base de datos MySQL

El propósito principal es evitar que el gateway siga insistiendo cuando un servicio está caído, mejorando así la estabilidad y resiliencia del sistema.

---

## FASE 1 – OBSERVAR

En esta fase se apagó el servicio de mascotas para observar el comportamiento actual del gateway sin realizar nuevas modificaciones al código.

Se realizaron varias peticiones al endpoint:

http://localhost:5000/mascotas

Al estar apagado el servicio backend de mascotas, el gateway empezó a registrar fallos. En los logs se evidencia que el sistema detectó el fallo número 1, fallo número 2 y fallo número 3. Después del tercer fallo, el sistema abrió el circuito y dejó de insistir sobre el servicio caído.

### ¿Qué hace el sistema actualmente?

El sistema intenta comunicarse con el servicio de mascotas. Si el servicio no responde, aumenta un contador de fallos. Cuando el contador llega a 3, el Circuit Breaker abre el circuito y bloquea temporalmente las llamadas al servicio.

### ¿Se protege o insiste?

El sistema se protege, porque después de tres fallos deja de insistir y responde con el mensaje:

```json
{"error":"Servicio temporalmente bloqueado"}