import logging
from fastapi import FastAPI, HTTPException, Request, logger
from fastapi.middleware.cors import CORSMiddleware
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

# Custom middleware for logging requests & errors
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        logger.info(f"➡️ Incoming request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"⬅️ Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"🔥 Error while handling request {request.url}: {e}")
        raise
app.include_router(user.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
