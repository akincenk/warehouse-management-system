# 🏭 Warehouse Management System – Fullstack (FastAPI + React)

A full-featured warehouse management system with secure JWT authentication, built using **FastAPI** for the backend and **React** for the frontend.

---

## 🚀 Features

- 🔐 JWT-based user authentication (login/register)
- 🧑‍💼 Role-based access: admin, manager, staff
- 📦 Product management with real CRUD operations
- 👥 User list for admins
- ⚡ Swagger interactive API docs
- 💻 React frontend dashboard
- 🌐 Axios-based API calls
- 🗃 SQLite database with SQLAlchemy ORM

---

## 📁 Project Structure



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
