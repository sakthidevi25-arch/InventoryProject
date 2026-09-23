# Secure Cloud Asset & API Inventory Management Platform

A production-focused platform for managing cloud assets, APIs, inventory intelligence, and compliance telemetry using FastAPI and Streamlit.

## Overview

This project is designed as an enterprise-grade portfolio application with:
- FastAPI backend with JWT auth, RBAC, validation, and Swagger docs
- Streamlit frontend for operational and AI-assisted workflows
- SQLite by default with SQLAlchemy for portability and easy migration
- Asset and API lifecycle tracking with audit logging
- Dashboard metrics and natural-language inventory exploration

## Architecture

- Backend: FastAPI
- Frontend: Streamlit
- Database: SQLite initially, compatible with PostgreSQL/SQL Server via SQLAlchemy
- ORM: SQLAlchemy
- Authentication: JWT + bcrypt hashing
- Documentation: OpenAPI/Swagger
- Security: rate limiting, validation, RBAC, secure error handling

## Project Structure

```text
InventoryProject/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── asset_routes.py
│   │   │   ├── api_routes.py
│   │   │   └── dashboard_routes.py
│   │   └── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   ├── database/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── asset.py
│   │   ├── audit_log.py
│   │   ├── role.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── api_repository.py
│   │   ├── asset_repository.py
│   │   ├── audit_repository.py
│   │   ├── base.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── api.py
│   │   ├── asset.py
│   │   ├── audit_log.py
│   │   └── user.py
│   ├── security/
│   │   ├── jwt_handler.py
│   │   └── password_utils.py
│   ├── services/
│   │   ├── api_service.py
│   │   ├── asset_service.py
│   │   ├── auth_service.py
│   │   └── dashboard_service.py
│   ├── logs/
│   ├── __init__.py
│   ├── seed_data.py
│   └── __init__.py
├── frontend/
│   ├── app.py
│   ├── components/
│   └── pages/
│   └── services/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── inventory.db
```

## Environment Setup

1. Create a virtual environment.
2. Copy `.env.example` to `.env`.
3. Install dependencies.
4. Run database initialization.
5. Start the backend and frontend.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
copy .env.example .env
python -c "from backend.database.init_db import init_db; init_db()"
python -m backend.seed_data
```

## Run Commands

### Backend

```bash
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
streamlit run frontend/app.py --server.port 8501
```

### API docs

Visit:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

## Core Security Practices

- Always hash passwords using bcrypt
- Validate all incoming requests through Pydantic
- Use JWT bearer tokens with expiration
- Store secrets only in `.env` or environment variables
- Log security-critical events
- Use rate limiting to reduce abuse
- Restrict CORS origins in production
- Use prepared queries via SQLAlchemy and avoid raw SQL

## Sample Data

The seed script creates:
- Default admin user: admin / Admin@123
- Example cloud assets
- Example APIs
- Default role assignments

## Features Included

- User registration and login
- Role-based access control
- Asset inventory CRUD
- API inventory CRUD
- Dashboard metrics
- Audit logging
- AI-ready architecture for future LLM integration

## Notes

This project intentionally uses SQLite initially to enable quick setup and demonstration. It can be migrated to SQL Server or PostgreSQL by changing the `DATABASE_URL` and adjusting dialect-specific configuration.
