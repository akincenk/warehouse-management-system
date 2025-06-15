from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    role: str

class ProductCreate(BaseModel):
    name: str
    quantity: int
