from pydantic import BaseModel
import datetime
import enum


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: str
    address: str | None = None
    medical_history: str | None = None



class DoctorCreate(BaseModel):
    specialization: str
    full_name: str
    age: int
    gender: str
    experience_years: int

class AppointmentCreate(BaseModel):
    appointment_date: datetime.datetime
    reason: str | None = None
class AppointmentResponse(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: datetime.datetime
    reason: str | None = None

class AppointmentOut(AppointmentCreate):
    id: int
    status: str

    class Config:
        orm_mode = True