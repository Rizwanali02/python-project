# Credit Approval System - Backend

This project is a backend system for managing customer credit approvals, loan eligibility, and loan records. It supports loading customer and loan data from Excel files and provides APIs for loan-related operations.

---

## 🚀 Tech Stack
- Python 3
- Django + Django Rest Framework
- PostgreSQL (Dockerized)
- Redis + Celery (Background Jobs)
- Pandas (Excel file processing)
- Docker + Docker Compose

---

## 🐳 Running Project with Docker

### 1️⃣ Build & Start Containers:
```bash
docker-compose up --build -d

docker-compose exec backend bash
python manage.py migrate

celery -A celery_app worker --loglevel=info

📥 Loading Excel Data (Django Shell)

1️⃣ Go inside Backend Container:

docker-compose exec backend bash
python manage.py shell

2️⃣ Run in Shell:

from credit.tasks import load_customer_data, load_loan_data
load_customer_data('/app/customer_data.xlsx')
load_loan_data('/app/loan_data.xlsx')



🔥 Available APIs (via Django Rest Framework)
API	Method	Description
/register	POST	Register a new customer
/check-eligibility	POST	Check loan eligibility
/create-loan	POST	Create loan for a customer
/view-loan/<loan_id>	GET	View single loan details
/view-loans/<customer_id>	GET	View all loans of a customer


✅ Project Highlights

    Dockerized PostgreSQL, Redis, Django Backend

    Celery for background data loading

    DRF APIs for loan management

    Data loading via Excel using Pandas

    Clean relational database schema (Customer, Loan)

    Ready for production deployment via Docker