# Module 6: Security - Authentication & Authorization

This project implements a secured FastAPI backend with **JWT Authentication**, **SQLAlchemy (PostgreSQL)**, and **Dockerized infrastructure**. It features user registration, login (token issuance), and protected route access.

---

## 🚀 Features

* **Dockerized Database:** PostgreSQL running on port **5422** to avoid conflicts with local installations.
* **User Registration:** Password hashing using **Bcrypt**.
* **Authentication:** OAuth2 Password Flow issuing **JWT Access Tokens**.
* **Authorization:** Protected endpoints verifying valid tokens.
* **Database Management:** Includes **pgAdmin 4** for visual database management.

---

## 🛠️ Prerequisites

* **Python 3.11+**
* **Docker & Docker Compose**

---

## 📦 Setup & Installation

### 1. Clone & Initialize Environment

```bash
# Clone the repository (if applicable) or go to project folder
git clone <repository-url>
cd FastAPI6
```
### Create Virtual Environment
```bash
python3 -m venv .venv
```

### Activate Environment
# macOS/Linux:
```bash
source .venv/bin/activate
```
# Windows:
```bash
.venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a .env file in the root directory.
```bash
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_week6

SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start Infrastructure (Docker)
```bash
docker compose up -d
```
* Postgres: Running on localhost:5433
* pgAdmin: Running on http://localhost:5050

## 🏃‍♂️ Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```