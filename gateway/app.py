from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Circuit Breaker para el servicio de mascotas
fallos_backend = 0
circuito_backend_abierto = False

# Circuit Breaker para el servicio de usuarios
fallos_usuarios = 0
circuito_usuarios_abierto = False


@app.route("/usuarios")
def usuarios():
    global fallos_usuarios, circuito_usuarios_abierto

    if circuito_usuarios_abierto:
        return {"error": "Servicio de usuarios temporalmente bloqueado"}, 503

    try:
        response = requests.get("http://usuarios:5000/usuarios", timeout=2)
        fallos_usuarios = 0
        return jsonify(response.json())

    except:
        fallos_usuarios += 1
        print(f"Fallo número {fallos_usuarios} en usuarios", flush=True)

        if fallos_usuarios >= 3:
            circuito_usuarios_abierto = True
            print("Circuito abierto para usuarios", flush=True)

        return {"error": "Servicio de usuarios no disponible"}, 503


@app.route("/mascotas")
def mascotas():
    global fallos_backend, circuito_backend_abierto

    if circuito_backend_abierto:
        return {"error": "Servicio de mascotas temporalmente bloqueado"}, 503

    try:
        response = requests.get("http://backend:5000/mascotas", timeout=2)
        fallos_backend = 0
        return response.json()

    except:
        fallos_backend += 1
        print(f"Fallo número {fallos_backend} en mascotas", flush=True)

        if fallos_backend >= 3:
            circuito_backend_abierto = True
            print("Circuito abierto para mascotas", flush=True)

        return {"error": "Servicio de mascotas no disponible"}, 503


@app.route("/estado-circuitos")
def estado_circuitos():
    return {
        "mascotas": {
            "fallos": fallos_backend,
            "circuito_abierto": circuito_backend_abierto
        },
        "usuarios": {
            "fallos": fallos_usuarios,
            "circuito_abierto": circuito_usuarios_abierto
        }
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)