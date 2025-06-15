from fastapi import APIRouter
from schemas import UserCreate

router = APIRouter()

@router.post("/")
def create_user(user: UserCreate):
    return {"message": f"User {user.username} with role {user.role} created."}
