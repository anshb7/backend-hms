# notifications.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.models import Appointment, Patient
from twilio.rest import Client
import os

# Configure your Twilio credentials via environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_number: str, message: str):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number,
        )
    except Exception as e:
        print(f"Error sending SMS to {to_number}: {e}")
        raise

def check_and_send_sms(db: Session):
    now = datetime.utcnow()
    window_end = now + timedelta(hours=24)
    upcoming = (
        db.query(Appointment)
          .filter(Appointment.appointment_date >= now,
                  Appointment.appointment_date <= window_end,
                  Appointment.notification_sent == False)
          .all()
    )
    for apt in upcoming:
        patient = db.query(Patient).filter(Patient.user_id == apt.patient_id).first()
        if patient and patient.ph_number:
            msg = f"Reminder: You have an appointment scheduled on {apt.appointment_date.strftime('%Y-%m-%d')} at {apt.appointment_time.strftime('%H:%M')}."
            try:
                send_sms(patient.ph_number, msg)
                apt.notification_sent = True
            except Exception as e:
                print(f"Failed to send SMS to {patient.ph_number}: {e}")
    db.commit()
