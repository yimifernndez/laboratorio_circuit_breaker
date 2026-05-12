from flask import Flask, request, jsonify
import requests
import time  # 🔴 CAMBIO: se importa time para controlar el tiempo de recuperación

app = Flask(__name__)

# 🔴 CAMBIO: tiempo que espera el circuito antes de intentar recuperarse
TIEMPO_RECUPERACION = 10

# Circuit Breaker para el servicio de mascotas
fallos_backend = 0
circuito_backend_abierto = False
ultimo_fallo_backend = None  # 🔴 CAMBIO: guarda el momento en que falló mascotas

# Circuit Breaker para el servicio de usuarios
fallos_usuarios = 0
circuito_usuarios_abierto = False
ultimo_fallo_usuarios = None  # 🔴 CAMBIO: guarda el momento en que falló usuarios


@app.route("/usuarios")
def usuarios():
    global fallos_usuarios, circuito_usuarios_abierto, ultimo_fallo_usuarios

    if circuito_usuarios_abierto:
        # 🔴 CAMBIO: se calcula cuánto tiempo ha pasado desde que se abrió el circuito
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - ultimo_fallo_usuarios

        # 🔴 CAMBIO: si no han pasado 10 segundos, sigue bloqueado
        if tiempo_transcurrido < TIEMPO_RECUPERACION:
            return {"error": "Servicio de usuarios temporalmente bloqueado"}, 503

        # 🔴 CAMBIO: si ya pasaron 10 segundos, entra en estado HALF-OPEN
        print("Circuito de usuarios en estado HALF-OPEN", flush=True)

    try:
        response = requests.get("http://usuarios:5000/usuarios", timeout=2)

        # 🔴 CAMBIO: si la prueba funciona, se cierra el circuito
        fallos_usuarios = 0
        circuito_usuarios_abierto = False
        ultimo_fallo_usuarios = None

        print("Circuito de usuarios cerrado", flush=True)

        return jsonify(response.json())

    except:
        fallos_usuarios += 1
        print(f"Fallo número {fallos_usuarios} en usuarios", flush=True)

        if fallos_usuarios >= 3:
            circuito_usuarios_abierto = True
            ultimo_fallo_usuarios = time.time()  # 🔴 CAMBIO: guarda la hora del fallo
            print("Circuito abierto para usuarios", flush=True)

        return {"error": "Servicio de usuarios no disponible"}, 503


@app.route("/mascotas")
def mascotas():
    global fallos_backend, circuito_backend_abierto, ultimo_fallo_backend

    if circuito_backend_abierto:
        # 🔴 CAMBIO: se calcula cuánto tiempo ha pasado desde que se abrió el circuito
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual - ultimo_fallo_backend

        # 🔴 CAMBIO: si no han pasado 10 segundos, sigue bloqueado
        if tiempo_transcurrido < TIEMPO_RECUPERACION:
            return {"error": "Servicio de mascotas temporalmente bloqueado"}, 503

        # 🔴 CAMBIO: si ya pasaron 10 segundos, entra en estado HALF-OPEN
        print("Circuito de mascotas en estado HALF-OPEN", flush=True)

    try:
        response = requests.get("http://backend:5000/mascotas", timeout=2)

        # 🔴 CAMBIO: si la prueba funciona, se cierra el circuito
        fallos_backend = 0
        circuito_backend_abierto = False
        ultimo_fallo_backend = None

        print("Circuito de mascotas cerrado", flush=True)

        return response.json()

    except:
        fallos_backend += 1
        print(f"Fallo número {fallos_backend} en mascotas", flush=True)

        if fallos_backend >= 3:
            circuito_backend_abierto = True
            ultimo_fallo_backend = time.time()  # 🔴 CAMBIO: guarda la hora del fallo
            print("Circuito abierto para mascotas", flush=True)

        return {"error": "Servicio de mascotas no disponible"}, 503

@app.route("/relacion")
def relacion():
    # Consultar servicio de usuarios
    try:
        response_usuarios = requests.get("http://usuarios:5000/usuarios", timeout=2)
        usuarios = response_usuarios.json()
        estado_usuarios = "usuarios funcionando correctamente"
    except:
        usuarios = []
        estado_usuarios = "no está funcionando usuarios"

    # Consultar servicio de mascotas
    try:
        response_mascotas = requests.get("http://backend:5000/mascotas", timeout=2)
        datos_mascotas = response_mascotas.json()
        estado_mascotas = "mascotas funcionando correctamente"

        mascotas = datos_mascotas.get("mascotas", [])

    except:
        mascotas = []
        estado_mascotas = "no está funcionando mascotas"

    return jsonify({
        "estado_usuarios": estado_usuarios,
        "usuarios": usuarios,
        "estado_mascotas": estado_mascotas,
        "mascotas": mascotas
    })


@app.route("/estado-circuitos")
def estado_circuitos():
    return {
        "mascotas": {
            "fallos": fallos_backend,
            "circuito_abierto": circuito_backend_abierto,
            "ultimo_fallo": ultimo_fallo_backend  # 🔴 CAMBIO: muestra cuándo falló
        },
        "usuarios": {
            "fallos": fallos_usuarios,
            "circuito_abierto": circuito_usuarios_abierto,
            "ultimo_fallo": ultimo_fallo_usuarios  # 🔴 CAMBIO: muestra cuándo falló
        }
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)