from sqlalchemy.orm import Session
from models import models,schemas
from fastapi import HTTPException, status
import uuid

def generate_patient_uid():
    return f"PAT-{uuid.uuid4().hex[:8].upper()}"  # e.g., PAT-1A2B3C4D


def get_all(db:Session):
    all_patients = db.query(models.Patient).all()
    return all_patients

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(full_name=patient.full_name, age=patient.age, gender=patient.gender, address=patient.address,medical_history=patient.medical_history,user_id=generate_patient_uid())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient_details(db:Session, patient_id: str):
    patient = db.query(models.Patient).filter(models.Patient.user_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient