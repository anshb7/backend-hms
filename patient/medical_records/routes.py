import os
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from patient.medical_records.medical_record import MedicalRecord
from database import SessionLocal

UPLOAD_FOLDER = "uploads/medical_records"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "docx"}

records_bp = Blueprint("records", __name__, url_prefix="/records")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@records_bp.route("/upload", methods=["POST"])
def upload_record():
    db = SessionLocal()
    try:
        file = request.files.get("file")
        title = request.form.get("title")
        date_str = request.form.get("date")
        doc_name = request.form.get("doc_name")

        if not all([file, title, date_str, doc_name]):
            return jsonify({"error": "Missing field"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            record_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        new_record = MedicalRecord(
            title=title,
            date=record_date,
            doc_name=doc_name,
            file_path=filepath
        )
        db.add(new_record)
        db.commit()
        return jsonify({"message": "Record uploaded", "id": new_record.id}), 201
    finally:
        db.close()
