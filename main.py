from fastapi import FastAPI
from routes import users, products

app = FastAPI()

app.include_router(users.router, prefix="/users")
app.include_router(products.router, prefix="/products")

@app.get("/")
def root():
    return {"message": "Warehouse Management System"}
