from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from doctor import doctor
from models import models, schemas
from sqlalchemy.orm import Session
from patient import patient
from database import db_engine

get_db=db_engine.get_db


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)

@router.get("/", response_model=List[schemas.DoctorCreate])
def get_doctors(db: Session = Depends(get_db)):
    return doctor.get_all(db)

@router.post("/createDoctor", response_model=schemas.DoctorCreate)
def create_doctor(doctor_model: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return doctor.create_doctor(db, doctor_model)

@router.get("/{doctor_id}", response_model=schemas.DoctorCreate)
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    return doctor.get_doctor_details(db, doctor_id)
