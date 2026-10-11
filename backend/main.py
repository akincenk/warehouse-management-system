import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import auth_routes
from database import Base, engine
from routes import products, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warehouse Management System API")

# Bearer tokens are sent in a header, so credentials (cookies) are not needed.
origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])


@app.get("/")
def root():
    return {"message": "Warehouse Management System API. See /docs."}
