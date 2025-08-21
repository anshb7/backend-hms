from datetime import date, time
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey,Enum,Date,Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class RoleEnum(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    ph_number=Column(Integer, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.patient)
    patients = relationship("Patient", back_populates="user")
    doctors = relationship("Doctor", back_populates="user")

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    medical_history = Column(String)
    full_name = Column(String, index=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    appointments = relationship("Appointment", back_populates="patient")

    user = relationship("User", back_populates="patients")
class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    specialization = Column(String, nullable=False)
    experience_years=Column(Integer, nullable=False)
    full_name = Column(String, index=True)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    appointments = relationship("Appointment", back_populates="doctor")
    
    user= relationship("User", back_populates="doctors")

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    reason = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    
class MedicalRecords(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    record_date = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    patient = relationship("Patient")
    doctor = relationship("Doctor")
