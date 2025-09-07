from datetime import date
from typing import List
"""
This module defines API routes for managing patient data in the healthcare management system.

Routes:
    - GET /patients/:
        Retrieve a list of all patients.
        Returns:
            List[schemas.PatientResponse]: A list of patient response objects.
        Response Example:
            [
                {
                    "id": "123",
                    "name": "John Doe",
                    "age": 30,
                    "gender": "male",
                    "email": "john@example.com"
                }
            ]

    - POST /patients/createPatient:
        Create a new patient record.
        Request Body Example:
            {
                "name": "Jane Doe",
                "age": 28,
                "gender": "female",
                "email": "jane@example.com"
            }
        Dependencies:
            - User must have the "patient" role.
        Returns:
            schemas.PatientResponse: The created patient response object.
        Response Example:
            {
                "id": "124",
                "name": "Jane Doe",
                "age": 28,
                "gender": "female",
                "email": "jane@example.com"
            }

    - GET /patients/{patient_id}:
        Retrieve details of a specific patient by patient ID.
        Path Parameters:
            patient_id (str): The unique identifier of the patient.
        Dependencies:
            - User must have the "patient" role.
        Returns:
            schemas.PatientResponse: The patient response object for the specified patient.
        Response Example:
            {
                "id": "123",
                "name": "John Doe",
                "age": 30,
                "gender": "male",
                "email": "john@example.com"
            }
"""
from fastapi import APIRouter, Depends, File, Form, UploadFile, status, HTTPException
from models import models, schemas
from sqlalchemy.orm import Session
from patient import patient
from database import db_engine
from patient.medical_records.medical_record import upload_medical_record
from auth.authentication import role_required,get_current_user
get_db=db_engine.get_db


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.get("/", response_model=List[schemas.Patient])
def get_patients(db: Session = Depends(get_db)):
    return patient.get_all(db)

@router.post("/createPatient", response_model=schemas.Patient,dependencies=[Depends(role_required(["patient"]))])
def create_patient(patient_model: schemas.Patient, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return patient.create_patient(patient_model, db, current_user)

@router.get("/{patient_id}", response_model=schemas.Patient,dependencies=[Depends(role_required(["patient","doctor"]))])
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    return patient.get_patient_details(db, patient_id)
@router.put("/{patient_id}/update", response_model=schemas.Patient,dependencies=[Depends(role_required(["patient"]))])
def update_patient(patient_id: str, patient_model: schemas.Patient, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return patient.update_patient(db, patient_id, patient_model, current_user)

@router.post("/{patient_id}/u_medical_records/",response_model=schemas.MedRecord,dependencies=[Depends(role_required(["patient"]))],status_code=status.HTTP_201_CREATED)
async def upload_medRecord(
    title: str = Form(...),
    record_date: str = Form(...),
    doctor_name: str = Form(...),
    notes: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    currentUser: models.User = Depends(get_current_user),
):

    return await upload_medical_record(currentUser=currentUser, title=title, record_date=record_date, doctor_name=doctor_name, notes=notes, file=file, db=db)