import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db_engine import get_db
from models import models
from auth.authentication import verify_password, get_password_hash, create_access_token
from datetime import timedelta

from models import schemas
from models.schemas import LoginRequest

router = APIRouter()
def generate_patient_uid():
    return f"USER-{uuid.uuid4().hex[:8].upper()}" 

@router.post("/register")
def register(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the system.

    Args:
        user_create (schemas.UserCreate): The user registration data.
        db (Session, optional): SQLAlchemy database session dependency.
        

    Raises:
        HTTPException: If a user with the given email already exists.

    Returns:
        dict: A message indicating successful creation and the new user's ID.
    """
    # check if user already exists
    if db.query(models.User).filter(models.User.email == user_create.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        id=generate_patient_uid(),
        username=user_create.username,
        email=user_create.email,
        password=get_password_hash(user_create.password),
        role=user_create.role,
        ph_number=user_create.ph_number
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User created successfully", "user_id": user.id}

@router.post("/login",response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

