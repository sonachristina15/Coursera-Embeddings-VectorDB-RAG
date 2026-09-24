# Coursera PostgreSQL + pgvector RAG

## Overview

This repository contains the **AI/RAG Vector Database layer** developed for the Coursera Multimodal Intelligence Platform project.

The project uses an authorized local copy of the IBM Data Science Professional Certificate dataset.

The database and preprocessing layer was completed as a separate team contribution. This repository starts from the **RAG-ready data available in PostgreSQL** and focuses on:

- Text embedding generation
- PostgreSQL `pgvector` integration
- Vector storage
- Vector similarity search
- Retrieval validation

---

## Project Architecture

```text
Authorized Course Dataset
          ↓
Data Ingestion
          ↓
Data Preprocessing
          ↓
Data Quality Checks
          ↓
PostgreSQL
          ↓
RAG-Ready Data
          ↓
Embedding Generation
          ↓
pgvector
          ↓
Vector Similarity Search
          ↓
Retrieved Context
          ↓
RAG / LLM Layer
```

## Dataset

The project uses an authorized local copy of the IBM Data Science Professional Certificate dataset.

The PostgreSQL database contains RAG-ready course content, including transcript segments and reading content.

The AI/RAG layer operates only on records marked as RAG-enabled.

---

## Embedding Model

Embeddings are generated using:

- Model: `all-MiniLM-L6-v2`
- Embedding dimension: `384`

The same embedding model is used for both document content and user queries so that they can be compared in the same vector space.

---

## PostgreSQL + pgvector

PostgreSQL is used for storing the RAG-ready data and generated embeddings.

The `pgvector` PostgreSQL extension is used to store and search vector embeddings.

Vector columns use:

```sql
vector(384)
```

Cosine distance is used for similarity search.

---

## Vector Index

HNSW indexes are created using cosine distance:

```sql
USING hnsw (embedding vector_cosine_ops)
```

This supports efficient vector similarity retrieval as the dataset grows.

---

## Similarity Search

User queries are converted into embeddings using the same `all-MiniLM-L6-v2` model.

The query vector is compared with stored embeddings using pgvector's cosine distance operator:

```sql
<=>
```

The most similar records are returned using Top-K retrieval.

Similarity is calculated as:

```text
similarity = 1 - cosine_distance
```

---

## Requirements

- Python
- PostgreSQL
- PostgreSQL `pgvector` extension
- `psycopg`
- `python-dotenv`
- `sentence-transformers`

---

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure the PostgreSQL connection details.

The PostgreSQL database must have the `pgvector` extension enabled.

---

## Repository Files

```text
.
├── docs/
│   └── interview_notes.md
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── generate_embeddings.py
├── test_rag_connection.py
├── test_similarity_search.py
├── test_store_embedding.py
└── verify_embedding.py
```

---

## RAG Scope

This repository focuses on the AI/RAG vector database portion of the larger project:

1. Generate embeddings
2. Store embeddings in PostgreSQL using pgvector
3. Create vector indexes
4. Perform similarity search
5. Validate retrieval results

The LLM generation and chatbot layer are outside the scope of this repository.

---

## Project Status

**Completed**

The embedding and vector database layer has been implemented and validated using the RAG-ready PostgreSQL data.