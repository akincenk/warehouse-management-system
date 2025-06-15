from fastapi import FastAPI
from database import Base, engine
from routes import users, products

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/")
def root():
    return {"message": "Warehouse Management System with Real Database"}
