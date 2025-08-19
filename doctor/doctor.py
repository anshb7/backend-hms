from sqlalchemy.orm import Session
from models import models,schemas
from fastapi import HTTPException, status
import uuid

def generate_doctor_uid():
    return f"DOC-{uuid.uuid4().hex[:8].upper()}"  # e.g., DOC-1A2B3C4D


def get_all(db:Session):
    all_doctors = db.query(models.Doctor).all()
    return all_doctors

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(full_name=doctor.full_name, age=doctor.age, gender=doctor.gender, specialization=doctor.specialization, experience_years=doctor.experience_years, user_id=generate_doctor_uid())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctor_details(db:Session, doctor_id: str):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor