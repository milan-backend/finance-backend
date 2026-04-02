# 💰 Finance Tracker Backend API

A backend system for managing personal finances, built using FastAPI, PostgreSQL, and JWT authentication.

This project focuses on clean architecture, secure authentication, role-based access control, and analytical dashboard capabilities.

---

## 🚀 Features

### 🔐 Authentication & Security

* JWT-based authentication (access + refresh tokens)
* Secure password hashing (bcrypt)
* Refresh token storage in database
* Environment-based configuration (.env)

### 👥 Role-Based Access Control (RBAC)

* **viewer** → read-only access
* **analyst** → read + dashboard access
* **admin** → full access (CRUD + role management)

### 💰 Financial Records

* Create income/expense records (admin)
* Read records (all users)
* Update/Delete records (admin only)
* User-specific data isolation

### 📊 Dashboard

* Total income
* Total expense
* Net balance
* Category-wise totals
* Recent transactions

### 🔍 Filtering & Pagination

* Filter by:

  * date range (`start_date`, `end_date`)
  * category
  * type (income/expense)
* Pagination support:

  * `limit`
  * `offset`

---

## 🛠 Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT (python-jose)
* Passlib (bcrypt)

---

## 📁 Project Structure

```id="m12psa"
app/
│
├── core/
├── models/
├── schemas/
├── routers/
├── database.py
├── dependencies.py
├── main.py
│
alembic/
.env
requirements.txt
README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash id="d8w1vx"
git clone <your-repo-url>
cd finance-backend
```

---

### 2️⃣ Create Virtual Environment

```bash id="1p6k8c"
python -m venv venv
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash id="g1f9p4"
pip install -r requirements.txt
```

---

### 4️⃣ Setup Environment Variables

Create `.env` file:

```env id="y9y0xq"
DATABASE_URL=postgresql://user:password@localhost:5432/finance_db
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=15

ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

---

### 5️⃣ Run Migrations

```bash id="b9kt0x"
alembic upgrade head
```

---

### 6️⃣ Run Server

```bash id="4p7kqz"
uvicorn app.main:app --reload
```

---

### 7️⃣ API Docs

```id="e9m3hb"
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Login using `/auth/login` (OAuth2 form)
2. Receive access token (and refresh token)
3. Click 🔐 **Authorize** in Swagger
4. Access protected endpoints

---

## 👤 Default Admin

If no admin exists, one is automatically created:

```id="5m3x2j"
email: admin@example.com
password: admin123
```

---

## 📌 API Overview

### Auth

* `POST /auth/register`
* `POST /auth/login`
* `POST /auth/refresh`

### Records

* `POST /records/` (admin)
* `GET /records/` (all users)
* `PUT /records/{id}` (admin)
* `DELETE /records/{id}` (admin)

### Dashboard

* `GET /dashboard/` (analyst, admin)

### User Management

* `PUT /users/{id}/role` (admin only)

---

## 🔍 Example Requests

### Dashboard with Filters

```id="8q0tw2"
/dashboard?start_date=2025-01-01&end_date=2025-01-31&category=food&type=expense
```

### Pagination

```id="v3i6d7"
/dashboard?limit=10&offset=10
```

---

## 🧠 Key Design Decisions

* Used dependency injection for authentication and RBAC
* Stored refresh tokens in database for session control
* Enforced strict user-level data isolation
* Implemented dynamic query filtering
* Used Alembic for schema migrations
* Managed secrets via `.env` instead of hardcoding

---

## 👨‍💻 Author

## 👨‍💻 Author

Milan  

Backend Developer passionate about building scalable APIs using FastAPI and PostgreSQL.

This project demonstrates secure authentication, role-based access control, and financial analytics.