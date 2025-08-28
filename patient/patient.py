from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException, status
import uuid


 # e.g., PAT-1A2B3C4D


def get_all(db: Session):
    all_patients = db.query(models.Patient).all()
    return all_patients


def create_patient(
    patient: schemas.Patient, db: Session, current_user: models.User
):
    # Ensure only users with role=patient can create patient profiles
    if current_user.role != models.RoleEnum.patient:
        raise HTTPException(
            status_code=403, detail="Not authorized to create patient profile"
        )

    # Check if profile already exists
    existing_profile = (
        db.query(models.Patient)
        .filter(models.Patient.user_id == current_user.id)
        .first()
    )
    if existing_profile:
        raise HTTPException(status_code=400, detail="Patient profile already exists")

    db_patient = models.Patient(
        user_id=current_user.id,
        medical_history=patient.medical_history,
        full_name=patient.full_name,
        age=patient.age,
        gender=patient.gender,
        address=patient.address,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient_details(db: Session, patient_id: str):
    patient = (
        db.query(models.Patient).filter(models.Patient.user_id == patient_id).first()
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
