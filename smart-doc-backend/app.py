from flask import Flask, request, jsonify, send_from_directory
import os
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS   

# App setup
app = Flask(__name__)
CORS(app)  

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# DB connection (XAMPP MySQL)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # default XAMPP has no password for root
    database="smartdocdb"
)
cursor = db.cursor(dictionary=True)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # your XAMPP MySQL username
        password="",          # your XAMPP MySQL password (empty by default in XAMPP)
        database="smartdocdb"    # change this to your actual DB name
    )


# ------------------ Routes -------------------

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

    cursor.execute(
        "INSERT INTO documents (filename, filepath, uploaded_at) VALUES (%s, %s, %s)",
        (filename, filepath, datetime.now())
    )
    db.commit()

    return jsonify({"message": "File uploaded successfully", "filename": filename})



@app.route("/documents", methods=["GET"])
def list_documents():
    cursor.execute("SELECT id, filename, uploaded_at FROM documents ORDER BY uploaded_at DESC LIMIT 10")
    docs = cursor.fetchall()
    return jsonify(docs)


@app.route("/download/<int:doc_id>", methods=["GET"])
def download_file(doc_id):
    cursor.execute("SELECT * FROM documents WHERE id = %s", (doc_id,))
    doc = cursor.fetchone()
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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
