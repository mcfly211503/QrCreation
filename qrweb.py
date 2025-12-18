from flask import Flask, request, jsonify, send_from_directory
import os
import segno
from fpdf import FPDF
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib

app = Flask(__name__)
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# --- Convertir tu código en función ---
def generar_y_enviar(nombre, receiver_email, qr_data):
    nombre_pdf = nombre.replace(" ", "_")

    # --- Generar QR ---
    qr_file = f"{nombre_pdf}.png"
    segno.make(qr_data).save(qr_file)

    # --- Crear PDF ---
    pdf_file = f"C:\\Users\\Arturo\\Desktop\\qr_pdf_{nombre_pdf}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Su QR está listo", ln=True, align='C')
    pdf.image(qr_file, x=10, y=20, w=100)
    pdf.output(pdf_file)
    
    # --- Enviar email ---
    email_user = os.getenv("GMAIL_USER")
    email_pass = os.getenv("GMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = receiver_email
    msg['Subject'] = "Tu QR"
    
    with open(pdf_file, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_file)}')
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, email_pass)
    server.sendmail(email_user, receiver_email, msg.as_string())
    server.quit()

    os.remove(pdf_file)
    os.remove(qr_file)

# --- Endpoint Flask ---
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    qr_data = data.get("qr_data")
    
    try:
        generar_y_enviar(nombre, correo, qr_data)
        return jsonify({"status": "ok", "message": "Correo enviado correctamente!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


