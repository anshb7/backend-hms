from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from models import models, schemas
from sqlalchemy.orm import Session
from patient import patient
from database import db_engine

get_db=db_engine.get_db


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.get("/", response_model=List[schemas.PatientCreate])
def get_patients(db: Session = Depends(get_db)):
    return patient.get_all(db)

@router.post("/createPatient", response_model=schemas.PatientCreate)
def create_patient(patient_model: schemas.PatientCreate, db: Session = Depends(get_db)):
    return patient.create_patient(db, patient_model)

@router.get("/{patient_id}", response_model=schemas.PatientCreate)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    return patient.get_patient_details(db, patient_id)
