from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from models import models, schemas
from sqlalchemy.orm import Session
from patient import patient
from database import db_engine
from auth.authentication import role_required,get_current_user
get_db=db_engine.get_db


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.get("/", response_model=List[schemas.PatientCreate])
def get_patients(db: Session = Depends(get_db)):
    return patient.get_all(db)

@router.post("/createPatient", response_model=schemas.PatientCreate,dependencies=[Depends(role_required("patient"))])
def create_patient(patient_model: schemas.PatientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return patient.create_patient(patient_model, db, current_user)

@router.get("/{patient_id}", response_model=schemas.PatientCreate,dependencies=[Depends(role_required("patient"))])
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    return patient.get_patient_details(db, patient_id)
