import os
import io

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from PIL import Image
import pytesseract
from fpdf import FPDF



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def clean_text(text: str) -> str:
    lines = text.splitlines()
    return "\n".join([line.strip() for line in lines if line.strip()])


@app.route("/")
def index():
    # templates/index.html  (your big HTML file)
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "image" not in request.files:
        return jsonify({"error": "No file field 'image' in form-data"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        img = Image.open(filepath)
        raw_text = pytesseract.image_to_string(img)
        cleaned = clean_text(raw_text)
        return jsonify({"raw": raw_text, "cleaned": cleaned}), 200
    except Exception as e:
        # log to console for debugging
        print("OCR ERROR:", e)
        return jsonify({"error": f"OCR failed: {e}"}), 500


@app.route("/api/download_txt", methods=["POST"])
def api_download_txt():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "")

    buf = io.BytesIO()
    buf.write(text.encode("utf-8"))
    buf.seek(0)

    return send_file(
        buf,
        mimetype="text/plain",
        as_attachment=True,
        download_name="notes.txt",
    )


@app.route("/api/download_pdf", methods=["POST"])
def api_download_pdf():
    try:
        data = request.get_json(force=True, silent=True) or {}
        text = data.get("text", "")

        # Make text safe for FPDF (latin-1 only)
        safe_text = text.encode("latin-1", "replace").decode("latin-1")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for line in safe_text.split("\n"):
            pdf.multi_cell(0, 6, line)

        # fpdf vs fpdf2: handle both
        pdf_output = pdf.output(dest="S")
        if isinstance(pdf_output, str):
            pdf_output = pdf_output.encode("latin-1")

        buffer = io.BytesIO(pdf_output)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="snapboard-notes.pdf",
        )
    except Exception as e:
        # Log on server + send clear error to frontend
        print("PDF ERROR:", e)
        return jsonify({"error": f"PDF generation failed: {e}"}), 500


if __name__ == "__main__":
    # if needed on Windows, point pytesseract to the exe, e.g.:
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    app.run(host="0.0.0.0", port=5000, debug=True)
