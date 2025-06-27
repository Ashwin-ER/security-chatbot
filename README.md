# security-chatbot

---
title: Security Intelligence Chatbot
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
# This section requests a more powerful free CPU, crucial for running LLMs,
# and pre-caches the models for much faster startup times.
resources:
  cpu: "2"
  memory: "8Gi"
models:
  - ollama/gemma:2b
  - ollama/nomic-embed-text
---

# Security Intelligence AI Chatbot

This is a demonstration of a secure, lightweight AI chatbot designed to assist users within a security and risk intelligence application. The entire application, including the AI models, is self-hosted and runs for free on Hugging Face Spaces.

## 🚀 Core Features
- **Navigates Threat Data:** Answers questions based on internal documentation like playbooks and guides.
- **Interprets Risk Scores:** Explains what different risk scores mean and what actions to take.
- **Answers FAQs:** Provides instant, accurate answers from a curated knowledge base.
- **Real-time Responses:** Uses streaming to deliver answers word-by-word for a fast, responsive user experience.

## 🛠️ Tech Stack
- **Backend Framework:** FastAPI
- **LLM Serving:** Ollama (running `gemma:2b` and `nomic-embed-text` locally in the container)
- **RAG Framework:** LangChain
- **Vector Database:** ChromaDB
- **Deployment:** Hugging Face Spaces (Docker)

---

## 🏛️ Architecture
The application uses a Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware answers grounded in a specific knowledge base.

<details>
<summary>Click to view Architecture Diagram</summary>

```mermaid
graph TD
    subgraph User Device
        A[User in Web App] --> B{Chat Interface (HTML/JS)};
```

subgraph "Hugging Face Space (Docker Container)"
        B -- HTTPS Request --> C[API Endpoint (FastAPI)];
        C -- User Query --> D[RAG Chain (LangChain)];
        D -- Embeds Query --> E{Embedding Model (nomic-embed-text)};
        E -- Vectorized Query --> F[Vector DB (ChromaDB)];
        F -- Returns Relevant Docs --> D;
        D -- Query + Docs --> G{Chat LLM (gemma:2b)};
        G -- Streams Grounded Response --> D;
        D -- Streams Final Answer --> C;
        C -- Streaming HTTPS Response --> B;
    

  subgraph Data Source (Internal)
        H[Knowledge Base: .md files] --> I(ingest.py Script);
        I -- Chunks Docs --> E;
        E -- Creates Embeddings --> F;
  ```bash
uvicorn main:app --reload
```

```bash
python ingest.py
```
