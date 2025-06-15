from fastapi import APIRouter
from schemas import ProductCreate

router = APIRouter()

@router.post("/")
def create_product(product: ProductCreate):
    return {"message": f"Product {product.name} with quantity {product.quantity} created."}
