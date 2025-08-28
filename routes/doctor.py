from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from auth.authentication import get_current_user, role_required
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

@router.get("/", response_model=List[schemas.Doctor])
def get_doctors(db: Session = Depends(get_db)):
    return doctor.get_all(db)

@router.post("/createDoctor", response_model=schemas.Doctor,dependencies=[Depends(role_required(["doctor"]))])
def create_doctor(doctor_model: schemas.Doctor, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    return doctor.create_doctor(db, doctor_model,current_user)

@router.get("/{doctor_id}", response_model=schemas.Doctor,dependencies=[Depends(role_required(["doctor","patient"]))])
def get_doctor(doctor_id: str, db: Session = Depends(get_db)):
    return doctor.get_doctor_details(db, doctor_id)
