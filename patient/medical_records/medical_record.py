from datetime import date
from azure.storage.blob import BlobServiceClient
import uuid
import os

from fastapi import Depends, Form, HTTPException, UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session

from database.db_engine import get_db
from models import models, schemas
from dotenv import load_dotenv
load_dotenv()
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_ACCESS_KEY")
AZURE_CONTAINER_NAME = "patientdocs"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
def upload_pdf_to_azure(file, patient_id: str, filename: str = None):
    if not filename:
        filename = f"{uuid.uuid4()}.pdf"
    blob_name = f"{patient_id}/{filename}"
    blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=blob_name)
    blob_client.upload_blob(file, overwrite=True)
    return blob_client.url
async def upload_medical_record(
    currentUser: models.User,
    db: Session,
    title: str = Form(...),
    doctor_name: str = Form(...),
    record_date: date = Form(...),
    notes: str | None = Form(None),
    file: UploadFile = File(...),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Upload stream directly
    pdf_link = upload_pdf_to_azure(file.file, str(currentUser.id), file.filename)

    new_record = models.MedicalRecords(
        patient_id=currentUser.id,
        doctor_name=doctor_name,
        title=title,
        pdf_link=pdf_link,
        record_date=record_date,
        notes=notes,
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record
