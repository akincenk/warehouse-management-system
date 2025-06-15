from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserOut
from auth.jwt_handler import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).all()
