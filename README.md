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

warehouse-management-fullstack/
├── backend/    # FastAPI backend (Python)
└── frontend/   # React frontend (JavaScript)

---

## 🛠️ Installation & Startup Guide

### 🔧 Backend (FastAPI + JWT)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Then visit Swagger UI:
👉 http://127.0.0.1:8000/docs


💻 Frontend (React)

cd frontend
npm install
npm start

View app in browser:
👉 http://localhost:3000

👤 Test Credentials (for local use)

You must register a user before login using Swagger:

🔹 POST /auth/register

{
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}

Then login with:
	•	Username: admin
	•	Password: admin123

Already registered? Try different username or delete db file to reset.

📦 Technologies Used

Layer Tech
Backend FastAPI, Python, JWT
Frontend React, JavaScript, Axios
Auth Python-JOSE JWT tokens
Database SQLite + SQLAlchemy ORM
Styling Tailwind CSS / basic UI

🌍 Deployment Ready

You can deploy this app using:
	•	🔷 Render.com (backend)
	•	🔶 Railway.app
	•	⚛️ Vercel.com (frontend)

📸 Screenshots

Add screenshots here for login page, dashboard, product view, etc.

🙋 About the Author

Cenk Akın – github.com/akincenk
🇨🇦 Vancouver-based fullstack developer. Passionate about FastAPI, React, and elegant software design.

📘 License

This project is licensed under the MIT License – feel free to use, fork, or contribute!

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
