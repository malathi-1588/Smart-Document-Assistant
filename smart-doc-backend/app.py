from flask import Flask, request, jsonify, send_from_directory
import os
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from text_extractor import extract_text

# ------------------ Setup ------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ------------------ DB helper ------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smartdocdb"
    )

# ------------------ Routes ------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO documents (filename, filepath, uploaded_at) VALUES (%s, %s, %s)",
        (filename, filepath, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "File uploaded successfully", "filename": filename})


@app.route("/documents", methods=["GET"])
def list_documents():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, filename, uploaded_at FROM documents ORDER BY uploaded_at DESC LIMIT 10")
    docs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(docs)


@app.route("/download/<int:doc_id>", methods=["GET"])
def download_file(doc_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents WHERE id = %s", (doc_id,))
    doc = cursor.fetchone()
    cursor.close()
    conn.close()

    if not doc:
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(app.config["UPLOAD_FOLDER"], doc["filename"], as_attachment=True)


@app.route('/documents/<string:doc_name>', methods=['GET'])
def get_document_by_name(doc_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents WHERE filename LIKE %s", (f"%{doc_name}%",))
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    if not result:
        return jsonify({"message": "No documents found"}), 404

    return jsonify(result)


# ---------- Preview ----------
@app.route("/preview/<filename>", methods=["GET"])
def preview_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    ext = filename.lower().split(".")[-1]

    if ext == "txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return jsonify({"type": "text", "content": content})

    elif ext in ["jpg", "jpeg", "png", "gif"]:
        return jsonify({"type": "image", "url": f"http://localhost:5000/files/{filename}"})

    elif ext == "pdf":
        return jsonify({"type": "pdf", "url": f"http://localhost:5000/files/{filename}"})

    else:
        return jsonify({"type": "download", "url": f"http://localhost:5000/files/{filename}"})


@app.route('/files/<filename>', methods=["GET"])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ---------- AI + OCR Extraction ----------
@app.route("/extract/<filename>", methods=["GET"])
def extract_text_route(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    result = extract_text(file_path)   # ✅ directly returns dict {source, text}
    return jsonify({"filename": filename, **result})



if __name__ == "__main__":
    app.run(port=5000, debug=True)
