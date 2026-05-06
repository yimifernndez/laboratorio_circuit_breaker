# Laboratorio: Sistema que aprende a fallar

## FASE 1 – OBSERVAR  
### Sin modificar código

En esta primera fase se realizó la observación del comportamiento actual del sistema cuando uno de sus servicios deja de funcionar.  
Para esta prueba se apagó el servicio de mascotas y se realizaron varias peticiones desde el gateway.

---

## 1. Apagar el servicio de mascotas

Primero se apagó manualmente el contenedor correspondiente al servicio de mascotas desde Docker.

El servicio apagado fue:

```txt
backend-1
```

Este servicio corresponde al backend de mascotas.

También se realizó la misma acción desde la terminal usando el siguiente comando:

```bash
docker compose stop backend
```

Con este comando se detuvo correctamente el servicio `backend`, permitiendo continuar con las pruebas desde el gateway.

---

## 2. Hacer varias peticiones al Gateway

Después de apagar el servicio de mascotas, se realizaron varias peticiones al endpoint del gateway:

```txt
http://localhost:5000/mascotas
```

Al realizar varias peticiones, el sistema respondió con el siguiente mensaje:

```json
{
  "error": "Servicio temporalmente bloqueado"
}
```

Esto indica que el gateway detectó que el servicio de mascotas no estaba disponible y aplicó el comportamiento del Circuit Breaker.

---

## 3. Revisar logs

Luego se revisaron los logs del gateway con el siguiente comando:

```bash
docker compose logs -f gateway
```

En los logs se evidenció el siguiente comportamiento:

```txt
Fallo número 1
Fallo número 2
Fallo número 3
Circuito abierto
```

Esto demuestra que el gateway intentó comunicarse varias veces con el servicio de mascotas.  
Como el servicio estaba apagado, el sistema empezó a contar los fallos. Al llegar al tercer fallo, el circuito se abrió.

---

## 4. Responder

### ¿Qué hace el sistema actualmente?

El sistema intenta llamar al servicio de mascotas desde el gateway.  
Como el servicio se encuentra apagado, empieza a contar los fallos. Después de varios intentos fallidos, el Circuit Breaker abre el circuito y el gateway deja de enviar más peticiones al backend de mascotas.

---

### ¿Se protege o insiste?

El sistema se protege.

Después de tres fallos, deja de insistir y responde directamente con el mensaje:

```json
{
  "error": "Servicio temporalmente bloqueado"
}
```

Esto sucede porque en el código existe una validación que revisa si el circuito está abierto:

```python
if circuito_abierto:
    return {"error": "Servicio temporalmente bloqueado"}, 503
```

Cuando el circuito está abierto, el gateway ya no intenta comunicarse con el servicio de mascotas, sino que responde directamente con un error controlado.

---

## 5. Explicación del comportamiento observado

El Circuit Breaker implementado en el endpoint `/mascotas` funciona como una protección para el sistema.

Cuando el servicio de mascotas está apagado, el gateway intenta comunicarse con él.  
Cada vez que la comunicación falla, aumenta el contador de fallos.

El código utilizado para contar los fallos es:

```python
except:
    fallos_backend += 1
    print(f"Fallo número {fallos_backend}", flush=True)
```

Cuando el contador llega a tres fallos, el circuito se abre:

```python
if fallos_backend >= 3:
    circuito_abierto = True
    print("Circuito abierto", flush=True)
```

Esto permite que el gateway deje de insistir sobre un servicio que no está funcionando.

---

## 6. Evidencia de la Fase 1

A continuación se presenta la evidencia de la Fase 1, donde se observa el servicio apagado, las peticiones realizadas al gateway y los logs que muestran los fallos detectados.

![Evidencia Fase 1](evidencias/fase1.png)

---

## Conclusión de la Fase 1

En esta fase se comprobó que el sistema ya cuenta con una protección básica usando Circuit Breaker en el endpoint `/mascotas`.

El sistema detecta los fallos del servicio de mascotas, cuenta los intentos fallidos y, al llegar a tres fallos, abre el circuito.  
Esto evita que el gateway siga insistiendo sobre un servicio caído.

Sin embargo, el comportamiento todavía es limitado, porque una vez el circuito se abre, queda bloqueado y no intenta recuperarse automáticamente.  
Por esta razón, en las siguientes fases se debe mejorar la lógica agregando el comportamiento de recuperación mediante Half-Open.