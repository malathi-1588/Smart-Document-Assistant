from flask import Flask, request, jsonify, send_from_directory
import os
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from text_extractor import extract_text   # unchanged

# ------------------ Setup ------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"   # 🔑 move to .env later
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# DB setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="smartdocdb"
)
cursor = db.cursor(dictionary=True)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smartdocdb"
    )

# ------------------ Auth ------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, generate_password_hash(password))
        )
        db.commit()
        return jsonify({"message": "User created successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user["password_hash"], password):
        # generate a simple token (for now username itself)
        token = f"TOKEN-{user['id']}"
        return jsonify({"token": token, "username": username})
    return jsonify({"error": "Invalid credentials"}), 401

# ------------------ Protected Routes ------------------
@app.route("/upload", methods=["POST"])
# @jwt_required()
def upload_file():
    user_id = None
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
# @jwt_required()
def list_documents():
    cursor.execute("SELECT id, filename, uploaded_at FROM documents ORDER BY uploaded_at DESC LIMIT 10")
    docs = cursor.fetchall()
    return jsonify(docs)

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
    
@app.route("/files/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/extract/<filename>", methods=["GET"])
def extract_text_route(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    result = extract_text(file_path)   
    return jsonify({"filename": filename, **result})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
