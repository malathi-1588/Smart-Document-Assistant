import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from db import get_conn, init_db
from ai_service import process_image_with_ai
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = Path("uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------
# User Routes
# ------------------------

@app.route("/api/users", methods=["POST"])
def api_create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
          properties:
            username:
              type: string
              example: Shashank123
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
            user_id:
              type: integer
      400:
        description: Invalid username
    """
    try:
        data = request.get_json()
        username = data.get("username", "").strip()

        if not username or not (3 <= len(username) <= 20) or not username.isalnum():
            return jsonify({"error": "Invalid username (3-20 alphanumeric)"}), 400

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_id = cur.lastrowid
        conn.close()

        return jsonify({"message": "user created", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/api/users", methods=["GET"])
def api_get_users():
    """Get all users."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200


@app.route("/api/users/<int:user_id>", methods=["GET"])
def api_get_user(user_id):
    """Get specific user by ID."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "user not found"}), 404

    return jsonify(dict(row)), 200


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    """Delete user by ID (and their documents)."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM documents WHERE user_id=?", (user_id,))
        cur.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"user {user_id} deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------
# Document Routes
# ------------------------

@app.route("/api/upload", methods=["POST"])
def api_upload():
    try:
        user_id = request.form.get("user_id")
        title = request.form.get("title", "").strip()
        file = request.files.get("file")

        if not user_id or not file:
            return jsonify({"error": "user_id and file required"}), 400
        try:
            int(user_id)
        except ValueError:
            return jsonify({"error": "invalid user_id"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "invalid file type"}), 400

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        dest_dir = UPLOAD_FOLDER / today
        dest_dir.mkdir(parents=True, exist_ok=True)

        filename = secure_filename(file.filename)
        save_path = dest_dir / f"{user_id}{int(datetime.now(timezone.utc).timestamp())}{filename}"
        file.save(str(save_path))

        # Process image with OpenAI — get title & text
        ai_title, extracted_text = process_image_with_ai(str(save_path))
        if not title:  # Use AI-generated title if not provided
            title = ai_title

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO documents (user_id, title, file_path, extracted_text)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, str(save_path), extracted_text))
        conn.commit()
        doc_id = cur.lastrowid
        conn.close()

        return jsonify({
            "doc_id": doc_id,
            "message": "File uploaded and processed successfully",
            "title": title,
            "extracted_text": extracted_text
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



@app.route("/api/document/<int:doc_id>", methods=["GET"])
def api_document(doc_id):
    """View full document details."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM documents
        WHERE doc_id=? AND user_id=?
    """, (doc_id, user_id))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    return jsonify(dict(row)), 200


@app.route("/api/search", methods=["GET"])
def api_search():
    """Search user's documents by title or extracted text."""
    user_id = request.args.get("user_id")
    query = request.args.get("q", "").strip()

    if not user_id or not query:
        return jsonify({"error": "user_id and search query required"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM documents
        WHERE user_id=?
        AND (title LIKE ? OR extracted_text LIKE ?)
    """, (user_id, f"%{query}%", f"%{query}%"))
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200


@app.route("/api/export/<int:doc_id>", methods=["GET"])
def api_export(doc_id):
    """Export extracted text as .txt file."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, extracted_text
        FROM documents
        WHERE doc_id=? AND user_id=?
    """, (doc_id, user_id))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    title = row["title"]
    text = row["extracted_text"] or ""
    filename = f"{title}.txt"

    tmp_path = Path("data") / f"export_{doc_id}.txt"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_text(text, encoding="utf-8")

    return send_file(str(tmp_path), as_attachment=True, download_name=filename)


@app.route("/api/document/<int:doc_id>", methods=["DELETE"])
def api_delete(doc_id):
    """Delete document and remove file from disk."""
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT file_path FROM documents
        WHERE doc_id=? AND user_id=?
    """, (doc_id, user_id))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404

    file_path = row["file_path"]

    try:
        if file_path and Path(file_path).exists():
            Path(file_path).unlink()
    except Exception as e:
        print(f"Warning: failed to remove file {file_path}: {e}")

    cur.execute("""
        DELETE FROM documents
        WHERE doc_id=? AND user_id=?
    """, (doc_id, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "deleted"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)