from sqlalchemy.orm import Session
from database.db_engine import get_db
from models import models, schemas
from fastapi import Depends, HTTPException, status

def book_appointment(db: Session, appointment: schemas.AppointmentCreate ,doctor_id: str,patient_id:str):
    # check doctor availability
    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.status == models.AppointmentStatus.scheduled
    ).first()

    # if existing:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Doctor is not available at this time"
    #     )

    # create new appointment
    db_appointment = models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=models.AppointmentStatus.scheduled,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        reason=appointment.reason,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
def get_patient_appointments(patient_id: str, db: Session):
    patient = db.query(models.Patient).filter(models.Patient.user_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    rows = (
        db.query(
            models.Appointment.id,
            models.Appointment.appointment_date,
            models.Appointment.appointment_time,
            models.Appointment.reason,
            models.Doctor.full_name.label("doctor_name"),
            models.Doctor.specialization.label("speciality"),
            models.Appointment.status,
        )
        .outerjoin(models.Doctor, models.Appointment.doctor_id == models.Doctor.user_id)
        .filter(models.Appointment.patient_id == patient_id)
        .order_by(models.Appointment.appointment_date.desc())
        .all()
    )


    return [schemas.AppointmentBase.from_orm(row) for row in rows]
def updateAppointmentStatus(patient_id:str,appointment_id:int,status: models.AppointmentStatus,db:Session):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.patient_id == patient_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.status = status
    db.commit()
    db.refresh(appointment)
    return appointment