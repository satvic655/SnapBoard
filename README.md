# SnapBoard 🧠📸  
> Turn whiteboards & screenshots into clean, editable text — locally, instantly.

SnapBoard is a small web app that lets you **upload or capture images** of notes / whiteboards and converts them into **editable text** using local OCR (Tesseract) — no cloud required. You can then **clean the text** and **download it as TXT or PDF**.

---

## 🚀 Features

- 📷 **Image upload + live camera capture**
- 🔠 **Local OCR** using Tesseract (no internet needed after setup)
- 🧹 **Text cleanup** (removes extra spaces / blank lines)
- 📄 **Export options**: Download as `.txt` or `.pdf`
- 🔒 **Privacy-friendly** – images are processed on your own machine
- 🎨 Simple, responsive UI built specifically for hackathon demos

---

## 🛠 Tech Stack

**Frontend**

- HTML, CSS, Vanilla JavaScript  
- Live camera capture using `navigator.mediaDevices.getUserMedia`
- Fetch API for calling backend endpoints

**Backend**

- Python 3  
- Flask (REST API + serving UI)  
- Flask-CORS  
- Pillow (PIL) – image loading  
- PyTesseract – OCR wrapper  
- FPDF – PDF generation

**OCR Engine**

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed locally  
- Configured via `pytesseract.pytesseract.tesseract_cmd`

---

## 📁 Project Structure

```text
SnapBoard/
├─ app.py                  # Flask backend + OCR endpoints
├─ venv/                   # Python virtual environment (optional but recommended)
├─ uploads/                # Temporary image uploads
├─ templates/
│  └─ index.html           # Main frontend (UI + JS)
├─ static/                 # (optional) extra static assets
└─ README.md               # This file
