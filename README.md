# Generic Data Ingestion Service

## Overview

This project is a generic data ingestion service built using FastAPI and Python. The service accepts one or more public API endpoints, fetches data from them, and stores the responses in a SQLite database. The design focuses on extensibility so that new data sources can be added without changing the core ingestion workflow.

---

## Features

- Generic API ingestion
- Supports multiple API endpoints in one request
- REST API built using FastAPI
- SQLite database using SQLAlchemy
- Layered architecture
- Request validation using Pydantic
- Logging for API requests
- Error handling with meaningful HTTP responses
- Interactive Swagger documentation

---

## Architecture

```
Client
   │
   ▼
FastAPI Router
   │
   ▼
Ingestion Service
   │
   ▼
API Service
   │
   ▼
External APIs
   │
   ▼
CRUD Layer
   │
   ▼
SQLite Database
```

---

## Folder Structure

```
generic-data-ingestion/

├── routers/
│   └── ingest.py
│
├── services/
│   ├── api_service.py
│   └── ingestion_service.py
│
├── utils/
│   └── logger.py
│
├── app.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## APIs Used

### JSONPlaceholder

https://jsonplaceholder.typicode.com/users

### DummyJSON

https://dummyjson.com/products

---

## Running the Project

### Create virtual environment

```bash
python -m venv venv
```

### Activate environment

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn app:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Sample Request

```json
{
  "sources": [
    {
      "name": "users",
      "url": "https://jsonplaceholder.typicode.com/users"
    },
    {
      "name": "products",
      "url": "https://dummyjson.com/products"
    }
  ]
}
```

---

## Design Decisions

- Used FastAPI for lightweight REST APIs.
- Used SQLAlchemy ORM for database interaction.
- Used SQLite for simplicity and portability.
- Separated Router, Service, and Database layers to improve maintainability.
- Added logging for better debugging and monitoring.
- Added error handling for external API failures.
- Designed request schema to support multiple API sources.

---

## AI Usage

AI tools were used to accelerate development and explore architectural ideas.

One incorrect suggestion generated during development resulted in a database schema mismatch after refactoring. This was identified by testing the API, reviewing the server traceback, recreating the SQLite database with the updated schema, and verifying the changes through end-to-end testing.

The final implementation and all design decisions were manually reviewed and understood.