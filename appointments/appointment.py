from sqlalchemy.orm import Session
from models import models, schemas
from fastapi import HTTPException, status

def book_appointment(db: Session, appointment: schemas.AppointmentCreate ,doctor_id: str,patient_id:str):
    # check doctor availability
    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.status == models.AppointmentStatus.scheduled
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor is not available at this time"
        )

    # create new appointment
    db_appointment = models.Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=models.AppointmentStatus.scheduled,
        appointment_date=appointment.appointment_date,
        reason=appointment.reason,
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
