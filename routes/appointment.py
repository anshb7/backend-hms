from typing import List
from fastapi import APIRouter, Depends, status, HTTPException,Query
from models import models, schemas
from appointments import appointment
from sqlalchemy.orm import Session
from patient import patient
from database import db_engine
from auth.authentication import role_required
get_db=db_engine.get_db


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)



@router.post("/book_appointment/{patient_id}/{doctor_id}", response_model=schemas.AppointmentResponse,dependencies=[Depends(role_required("patient"))])
def create_appointment(doctor_id: str,patient_id:str,appointment_model: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return appointment.book_appointment(db, appointment_model, doctor_id,patient_id)

@router.get("/doctor/{doctor_id}", response_model=List[schemas.AppointmentResponse],dependencies=[Depends(role_required("doctor"))])
def get_appointmentbyDoctorID(doctor_id: str , db: Session = Depends(get_db)):
    query = db.query(models.Appointment)

    if doctor_id:   
        query = query.filter(models.Appointment.doctor_id == doctor_id)
    else:
        return HTTPException(status_code=404, detail="Doctor not found")

    appointments = query.all()
    return appointments