from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Enum, Date, Time
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Role enum
class RoleEnum(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, index=True)  # mix of int + string, e.g. "U123"
    username = Column(String(50), index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # store hashed
    ph_number = Column(String(15), nullable=False)  # as string, not int
    role = Column(Enum(RoleEnum), default=RoleEnum.patient, nullable=False)

    patients = relationship("Patient", back_populates="user")
    doctors = relationship("Doctor", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    medical_history = Column(String)
    full_name = Column(String(100), index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(255), nullable=False)

    appointments = relationship("Appointment", back_populates="patient")
    user = relationship("User", back_populates="patients")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience_years = Column(Integer, nullable=False)
    full_name = Column(String(100), index=True, nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")
    user = relationship("User", back_populates="doctors")

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled, nullable=False)
    reason = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class MedicalRecords(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    record_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String(500), nullable=True)

    patient = relationship("Patient")
    doctor = relationship("Doctor")
