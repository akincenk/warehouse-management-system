from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    quantity: int

class ProductOut(BaseModel):
    id: int
    name: str
    quantity: int
    class Config:
        orm_mode = True
