from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

fallos_backend = 0
circuito_abierto= False

@app.route("/usuarios")
def usuarios():
    response = requests.get("http://usuarios:5000/usuarios")
    return jsonify(response.json())

@app.route("/mascotas")
def mascotas():
   global fallos_backend, circuito_abierto
   if circuito_abierto:
        return {"error": "Servicio temporalmente bloqueado"}, 503
   try:
        response = requests.get("http://backend:5000/mascotas", timeout=2)
        fallos_backend = 0
        return response.json()
   except:
        fallos_backend += 1
        print(f"Fallo número {fallos_backend}", flush=True)

        if fallos_backend >= 3:
            circuito_abierto = True
            print("Circuito abierto", flush=True)

        return {"error": "Servicio no disponible"}, 503
       

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)