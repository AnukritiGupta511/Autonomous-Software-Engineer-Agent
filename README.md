# 🤖 Autonomous AI Software Engineer Agent

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-00a393)
![React](https://img.shields.io/badge/React-18-61dafb)
![Docker](https://img.shields.io/badge/Docker-compose-2496ed)

A production-ready, portfolio-level project demonstrating an AI-powered software engineering assistant. This system uses a Multi-Agent architecture to understand repositories, analyze code architecture, answer questions via RAG, generate features, and fix bugs.

## 🌟 Key Features
- **Multi-Agent Orchestration**: LangGraph-based state machines coordinating specialized agents (Project Manager, Repo Analyzer, Code Reviewer, Bug Fixer, Feature Generator).
- **Repository-Aware RAG**: Automatically clones GitHub repos, chunks code semantically via AST, and embeds them into ChromaDB for context-aware AI interactions.
- **SaaS Dashboard**: A stunning, dark-mode frontend built with React, Vite, and Tailwind CSS v4 featuring glassmorphism and modern aesthetics.
- **Robust Backend**: FastAPI with async SQLAlchemy, PostgreSQL, Redis caching, and JWT Authentication.
- **Full Dockerization**: One command (`docker compose up`) spins up all 5 microservices.

## 🏗️ Architecture

```text
User Request
   │
   ▼
[ FastAPI Backend ] ─── (JWT Auth) ─── PostgreSQL (Users, Workflows, Chats)
   │
   ├──> [ LangGraph Orchestrator ]
   │       ├── Project Manager Agent
   │       ├── Repo Analyzer Agent
   │       └── Code Reviewer Agent
   │
   └──> [ RAG Engine ]
           ├── GitHub API Integration
           ├── AST Code Chunker
           └── ChromaDB Vector Store
```

## 🚀 Quick Start

### 1. Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12 (for local backend dev)

### 2. Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
Make sure to add your `OPENAI_API_KEY` (and `GITHUB_TOKEN` for higher rate limits).

### 3. Run with Docker
```bash
docker compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📂 Project Structure

- `/backend` - FastAPI server, LangGraph agents, RAG engine, Database models
- `/frontend` - React/Vite dashboard, Tailwind styling, API hooks
- `docker-compose.yml` - Infrastructure definition

## 💡 Interview Talking Points

If reviewing this project for an AI Engineering role, note the following design decisions:
1. **Agent State Management**: Instead of a monolithic LLM call, we use LangGraph. This allows us to persist agent state into Redis, enabling human-in-the-loop approvals before code execution.
2. **Semantic Code Chunking**: Traditional naive text chunking destroys code context. The `CodeChunker` module specifically handles line-based structural boundaries to improve vector search recall.
3. **Database Concurrency**: The backend exclusively uses `asyncpg` and async SQLAlchemy to ensure the API doesn't block while waiting for LLM responses or GitHub API calls.

## 🛡️ License
MIT
