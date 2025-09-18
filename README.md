# 🏥 HMS Backend (FastAPI + Azure)

Backend service for a **Healthcare Management System** built with **FastAPI**, deployed on **Azure App Service**, using **Azure SQL Database** and **Azure Blob Storage**.

---

## 🚀 Features
- JWT Auth (access + refresh, logout flow).
- Role-based access (patient, doctor, admin).
- Appointment management (`scheduled`, `completed`, `cancelled`).
- Medical records upload (PDF → Azure Blob → DB link).
- Swagger API docs (`/docs`).

---

## ⚙️ Setup

### Local Development
```bash
git clone https://github.com/<your-repo>/hms-backend.git
cd hms-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
