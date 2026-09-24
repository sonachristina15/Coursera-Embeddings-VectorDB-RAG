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