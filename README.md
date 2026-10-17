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

# Generic Data Ingestion Assistant

A Python-based data ingestion application built with FastAPI, SQLite, and Ollama. It ingests data from public APIs, tracks ingestion results, and uses Retrieval-Augmented Generation (RAG) to answer questions about project documentation and uploaded PDF documents.

## Features

- **Generic API ingestion:** Fetches data from multiple API endpoints.
- **SQLite storage:** Stores ingested records and ingestion run details.
- **Ingestion monitoring:** Tracks successful and failed sources.
- **PDF upload:** Extracts text from uploaded PDF documents.
- **AI Assistant:** Answers questions using local LLMs and RAG.
- **Semantic retrieval:** Uses embeddings and cosine similarity to retrieve relevant document content.
- **Web interface:** Provides PDF upload, AI chat, and ingestion history.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Ollama
- Llama 3.2 (`llama3.2:3b`)
- `nomic-embed-text`
- PyPDF
- HTML, CSS, JavaScript

## Architecture

```text
Public APIs / Uploaded PDF
           |
           v
    FastAPI Backend
           |
     +-----+------+
     |            |
     v            v
 API Ingestion  PDF Text Extraction
     |            |
     v            v
   SQLite    Extracted Text
                  |
                  v
             RAG Retrieval
                  |
                  v
             Ollama LLM
                  |
                  v
             AI Response
```

## Prerequisites

Install the following:

- Python 3.10 or a compatible version for your dependencies
- Git
- Ollama

Download Ollama from: https://ollama.com/

## Setup and Run

### 1. Clone the repository

```powershell
git clone https://github.com/ApoorvaHegde09/generic-data-ingestion.git
cd generic-data-ingestion
```

### 2. Create and activate the virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama from https://ollama.com/ and make sure it is running.

Download the required models:

```powershell
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 5. Start the application

From the project root, run:

```powershell
.\start_project.ps1
```

The startup script launches the application components according to its configuration.

If PowerShell blocks the script, try:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_project.ps1
```

### 6. Open the application

- **Frontend:** `http://127.0.0.1:5500`
- **Backend API:** `http://127.0.0.1:8000`
- **API documentation:** `http://127.0.0.1:8000/docs`

Make sure the URLs and ports match the configuration in `start_project.ps1`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ingest` | Ingest data from API sources |
| GET | `/records` | Retrieve stored records |
| GET | `/ingestion-runs` | View ingestion history |
| POST | `/upload` | Upload a PDF and extract its text |
| POST | `/ai/chat` | Ask the AI Assistant a question |

## Example AI Questions

After uploading a text-based PDF, try asking:

- Summarize my uploaded PDF.
- Which technologies are mentioned in my uploaded document?
- How many records were processed, and how many failed?
- Explain the data pipeline mentioned in my PDF.
- What was my latest ingestion run?
- How many ingestion runs have I performed?
- Which ingestion runs had failures?

## Design Decisions

- **FastAPI** provides lightweight REST endpoints.
- **SQLite** provides simple local persistence.
- **Ollama** runs the language and embedding models locally.
- **RAG** retrieves relevant document text before generating answers.
- **Separate frontend and backend** allow the user interface and API service to run independently.

## Current Limitations

- PDF text extraction supports selectable text; scanned PDFs may require OCR.
- The current document storage supports one latest uploaded PDF text file.
- Uploaded text and the SQLite database are stored locally.
- Ollama must be running locally for AI functionality.
- This project is configured for local development, not production deployment.


## AI Usage

AI tools were used to assist with implementation and debugging. The project integrates local language models and retrieval techniques to provide AI-powered document question answering.


