from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin
from auth.jwt_handler import create_access_token, get_current_user
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered successfully."}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}
