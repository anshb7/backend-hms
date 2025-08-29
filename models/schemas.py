from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, time
from sqlalchemy import Column, Integer, String, Date
from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    doc_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    ph_number: int
class Patient(BaseModel):
    full_name: str
    age: int
    gender: str
    address: str | None = None
    medical_history: str | None = None
class Doctor(BaseModel):
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
    appointment_time: time
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
class AppointmentStatus(BaseModel):
    status: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class AppointmentBase(BaseModel):
    date: date
    time:time
    reason: Optional[str] = None
    doctor: str   
    speciality:str
    is_scheduled:str

    class Config:
        orm_mode = True
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj[0],
            date=obj[1],
            time=obj[2].strftime("%H:%M"),  # <-- HH:mm format
            reason=obj[3],
            doctor=obj[4],
            speciality=obj[5],
            is_scheduled=obj[6]
        )
