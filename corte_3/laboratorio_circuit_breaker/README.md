# Laboratorio: Sistema que aprende a fallar

## FASE 1 – OBSERVAR  
### Sin modificar código

---

## Apagar el servicio de mascotas

- Lo apagué manualmente desde Docker, deteniendo únicamente el contenedor del servicio de mascotas.

El contenedor apagado fue:

```txt
backend-1
```

Este contenedor corresponde al servicio de mascotas.

- También lo apagué usando el comando en la terminal:

```bash
docker compose stop backend
```

Se verificó que el servicio se apagó correctamente para poder seguir con las pruebas.

---

## Hacer varias peticiones al Gateway

A la hora de hacer las peticiones, ingresé varias veces al endpoint del gateway:

```txt
http://localhost:5000/mascotas
```

Después de realizar varias peticiones, el sistema respondió con el siguiente mensaje:

```json
{
  "error": "Servicio temporalmente bloqueado"
}
```

Esto quiere decir que el gateway detectó varios fallos del servicio de mascotas y decidió bloquear temporalmente las llamadas hacia ese servicio.

---

## Revisar logs

Para revisar los logs del gateway, se ejecutó el siguiente comando en la terminal:

```bash
docker compose logs -f gateway
```

En los logs se evidenció lo siguiente:

```txt
Fallo número 1
Fallo número 2
Fallo número 3
Circuito abierto
```

El gateway ya detectó varios fallos del servicio de mascotas y decidió dejar de insistir.

---

## Responder

### ¿Qué hace el sistema actualmente?

El sistema intenta llamar al servicio de mascotas. Como el servicio está apagado, empieza a contar los fallos.

Después de varios intentos fallidos, el Circuit Breaker abre el circuito y el gateway deja de enviar más peticiones al backend de mascotas.

---

### ¿Se protege o insiste?

El sistema se protege, porque después de 3 fallos deja de insistir y responde directamente con el mensaje:

```json
{
  "error": "Servicio temporalmente bloqueado"
}
```

Esto se evidencia en la siguiente parte del código:

```python
if circuito_abierto:
    return {"error": "Servicio temporalmente bloqueado"}, 503
```

Cuando el circuito está abierto, el gateway ya no intenta comunicarse con el servicio de mascotas, sino que responde directamente con un error controlado.

---

## Explicación de lo observado

La cantidad de fallos permite verificar que el gateway intentó comunicarse con el servicio de mascotas.

Como el servicio estaba apagado, el sistema empezó a contar los errores. Al llegar a 3 fallos, abrió el circuito y respondió con el error:

```json
{
  "error": "Servicio temporalmente bloqueado"
}
```

Esto demuestra que el sistema no sigue insistiendo de manera indefinida, sino que se protege cuando detecta que un servicio no está disponible.

---

## Evidencia de la Fase 1

En la siguiente evidencia se muestra el comportamiento del sistema durante la Fase 1:

![Evidencia Fase 1](evidencias/fase1.png)

---

## Conclusión de la Fase 1

En esta fase se comprobó que el sistema ya cuenta con un Circuit Breaker básico en el endpoint `/mascotas`.

Cuando el servicio de mascotas se apaga, el gateway intenta comunicarse con él. Si la comunicación falla, el sistema empieza a contar los fallos. Al llegar al tercer fallo, el circuito se abre y el gateway deja de insistir.

Sin embargo, esta implementación todavía es básica, porque cuando el circuito queda abierto no intenta recuperarse automáticamente. Por eso, en las siguientes fases se debe implementar la lógica de recuperación usando el estado Half-Open.