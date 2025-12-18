# archivo: app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from qr_email_logic import generar_y_enviar
import os

app = Flask(__name__)
CORS(app)  # permite llamadas desde tu GitHub Pages

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.json
        nombre = data["nombre"]
        receiver_email = data["email"]
        qr_data = data["url"]

        generar_y_enviar(nombre, receiver_email, qr_data)

        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
