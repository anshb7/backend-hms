from pydantic import BaseModel, EmailStr
from datetime import date, time
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
    appointment_date: date
    appointment_time: time
    reason: str | None = None
class AppointmentResponse(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: date
    reason: str | None = None
class AppointmentOut(AppointmentCreate):
    id: int
    status: str
    class Config:
        orm_mode = True
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str