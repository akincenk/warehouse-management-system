from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.security import require_role
from database import get_db
from models import User
from schemas import Role, UserOut

router = APIRouter()


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(User).order_by(User.id).all()


@router.patch("/{user_id}/role", response_model=UserOut)
def set_role(
    user_id: int,
    role: Role = Body(embed=True),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin")),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = role
    db.commit()
    db.refresh(user)
    return user
