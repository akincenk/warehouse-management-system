# Warehouse Management System with JWT

A secure warehouse management API built with FastAPI, SQLAlchemy, and JWT-based authentication.

## Features
- FastAPI backend
- JWT authentication (login/register)
- User roles: admin, staff, manager
- Product and user CRUD (protected)
- SQLite database
- Modular project structure

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then go to: http://127.0.0.1:8000/docs
