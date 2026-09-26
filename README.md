# Generic Data Ingestion Service

## Overview

A FastAPI-based data ingestion service that fetches data from public APIs and stores the responses in a SQLite database.

The project was extended with a local AI assistant using Ollama, allowing users to ask questions about ingestion runs and project documentation.

## Features

* Generic API ingestion
* Multiple API sources in one request
* FastAPI REST APIs
* SQLite + SQLAlchemy
* Ingestion run tracking
* Success and failure tracking
* Error handling and logging
* Swagger documentation
* Local AI assistant using Ollama
* Tool-based database queries
* Short-term conversation history
* Lightweight RAG for documentation-based questions
* Simple HTML/CSS/JavaScript frontend

## Architecture

```text
External APIs
      │
      ▼
   FastAPI
      │
      ▼
Ingestion Service
      │
      ▼
SQLite Database


AI Assistant
      │
      ├── Database Tools
      │
      └── RAG
           │
           ▼
      Ollama / Llama 3.2
```

## APIs Used

* JSONPlaceholder — https://jsonplaceholder.typicode.com/users
* DummyJSON — https://dummyjson.com/products

## API Endpoints

| Method | Endpoint          | Purpose                |
| ------ | ----------------- | ---------------------- |
| POST   | `/ingest`         | Start ingestion        |
| GET    | `/records`        | View stored records    |
| GET    | `/ingestion-runs` | View ingestion history |
| POST   | `/ai/chat`        | Ask the AI assistant   |

Swagger:

```text
http://127.0.0.1:8000/docs
```

## AI Assistant

The assistant uses **Ollama with Llama 3.2 3B**.

It can answer questions such as:

```text
What was my last ingestion?
```

and follow-up questions such as:

```text
And how many were successful?
```

It can also answer documentation-based questions using RAG.

Example:

```text
How does the ingestion system handle failed API requests?
```

The RAG pipeline uses **nomic-embed-text** embeddings and cosine similarity to retrieve relevant documentation.

## Running the Project

### Create virtual environment

```bash
python -m venv venv
```

### Activate

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama models

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### Start backend

```bash
uvicorn app:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Start frontend

```bash
python -m http.server 5500 --directory frontend
```

Open:

```text
http://127.0.0.1:5500
```

## Design Decisions

* FastAPI for REST APIs
* SQLAlchemy for database interaction
* SQLite for simplicity
* Separate Router, Service, and Database layers
* Ollama for local LLM inference
* Lightweight Python-based RAG without an external vector database

## AI Usage

AI tools were used during development to explore implementation approaches and architectural ideas.

One incorrect suggestion caused a database schema mismatch during development. The issue was identified through API testing and server logs, after which the schema was corrected and the application was tested end-to-end.

The final implementation and design decisions were manually reviewed and understood.
