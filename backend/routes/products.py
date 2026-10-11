from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.security import get_current_user, require_role
from database import get_db
from models import Product, User
from schemas import ProductCreate, ProductOut, ProductUpdate

router = APIRouter()


def _get_or_404(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Product).order_by(Product.id).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return _get_or_404(db, product_id)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int, changes: ProductUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    product = _get_or_404(db, product_id)
    for field, value in changes.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin", "manager"))):
    db.delete(_get_or_404(db, product_id))
    db.commit()
