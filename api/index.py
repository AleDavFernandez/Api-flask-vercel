import re
from flask import Flask, request, jsonify
from mangum import Mangum

app = Flask(__name__)
usuarios = {}

def es_correo_valido(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo)

@app.route("/usuarios", methods=["POST"])
def agregar_usuario():
    data = request.json
    correo = data.get("correo")
    contraseña = data.get("contraseña")

    if not correo or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    if not es_correo_valido(correo):
        return jsonify({"error": "Correo no válido"}), 400

    if correo in usuarios:
        return jsonify({"error": "El correo ya está registrado"}), 409

    usuarios[correo] = contraseña
    return jsonify({"mensaje": f"Usuario {correo} agregado correctamente."}), 201

@app.route("/usuarios", methods=["GET"])
def mostrar_usuarios():
    return jsonify(usuarios), 200

@app.route("/usuarios/<correo>", methods=["PUT"])
def modificar_contraseña(correo):
    if correo not in usuarios:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.json
    nueva_contraseña = data.get("contraseña")
    if not nueva_contraseña:
        return jsonify({"error": "Debe proporcionar una nueva contraseña"}), 400

    usuarios[correo] = nueva_contraseña
    return jsonify({"mensaje": f"Contraseña de {correo} actualizada correctamente."}), 200

@app.route("/usuarios/<correo>", methods=["DELETE"])
def eliminar_usuario(correo):
    if correo not in usuarios:
        return jsonify({"error": "Usuario no encontrado"}), 404

    del usuarios[correo]
    return jsonify({"mensaje": f"Usuario {correo} eliminado correctamente."}), 200

handler = Mangum(app)
