# financial-doc-manager
AI Powered Financial Document Management System

# AI Powered Financial Document Management System

## Overview

This project is an AI-powered Financial Document Management System built using FastAPI, Streamlit, Qdrant Vector Database, and Sentence Transformers.

The system allows organizations to securely upload, manage, search, and analyze financial documents such as reports, invoices, and contracts using semantic AI search and retrieval.

The project also implements JWT Authentication and Role-Based Access Control (RBAC) for secure access management.

---

# Features

## Authentication & Security
- User Registration
- User Login
- JWT Authentication
- Role-Based Access Control (RBAC)

## User Roles
- Admin
- Financial Analyst
- Auditor
- Client

## Document Management
- Upload Financial PDF Documents
- View Documents
- Delete Documents
- Metadata-Based Search

## AI / RAG Features
- PDF Text Extraction
- Semantic Chunking
- Embeddings Generation
- Vector Database Storage using Qdrant
- Semantic Search using Sentence Transformers
- Reranking Pipeline for Improved Retrieval Accuracy

## Admin Panel
- View All Users
- Delete Users
- Change User Roles

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

## Frontend
- Streamlit

## AI / ML
- Sentence Transformers
- Cross Encoder Reranker
- LangChain Text Splitter
- Qdrant Vector Database

---

# Project Architecture

## Document Upload Flow

PDF Upload  
↓  
Text Extraction  
↓  
Chunking  
↓  
Embedding Generation  
↓  
Vector Storage in Qdrant

---

## Semantic Search Flow

User Query  
↓  
Query Embedding  
↓  
Vector Search  
↓  
Top Results Retrieval  
↓  
Reranking  
↓  
Most Relevant Results

---

# Folder Structure

```text
financial-doc-manager/

├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── main.py
│   └── database.py

├── uploads/

├── streamlit_app.py

├── requirements.txt

├── README.md

└── .env.example
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/banesanchit/financial-doc-manager
```

---

## Open Project Folder

```bash
cd financial-doc-manager
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Run Streamlit Frontend

Open a new terminal and run:

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# Semantic Search Example

Example Query:

```text
financial risk related to high debt ratio
```

The system retrieves semantically relevant financial document chunks using vector similarity search and reranking.

---

# RBAC Permissions

| Role | Permissions |
|------|-------------|
| Admin | Full Access |
| Financial Analyst | Upload and Search Documents |
| Auditor | Review and Search Documents |
| Client | View Documents |

---

# AI Models Used

## Embedding Model
```text
all-MiniLM-L6-v2
```

Used for semantic embeddings generation.

## Reranking Model
```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Used for reranking semantic search results.

---

# Future Improvements

- Password Hashing using bcrypt
- Docker Deployment
- Cloud Vector Database
- LLM-Based Answer Generation
- Multi-Document Financial Analysis

---

# Author

Sanchit Bane

AI / ML Engineering Assignment Project