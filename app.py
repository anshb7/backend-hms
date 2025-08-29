from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from medical_records.routes import records_bp
from models import models, schemas
from routes import patient,doctor, appointment,user
from database import db_engine

app = FastAPI()

models.Base.metadata.create_all(bind=db_engine.engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only!)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (Authorization, Content-Type, etc.)
)

app.include_router(user.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.register_blueprint(records_bp)