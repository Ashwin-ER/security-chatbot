---
title: Security Intelligence Chatbot
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
# This section tells Hugging Face to use a better free CPU instance
# and ensures the models are pre-downloaded for faster startup.
resources:
  cpu: "2"
  memory: "8Gi"
models:
  - ollama/gemma:2b
  - ollama/nomic-embed-text
---
# Security Intelligence AI Chatbot

This is a demo of a Retrieval-Augmented Generation (RAG) chatbot for a security and risk intelligence application.

## Features:

- **Navigates threat data:** Answers questions based on internal documentation.
- **Interprets risk scores:** Explains what different scores mean.
- **Answers FAQs:** Provides instant answers from a knowledge base.

## Tech Stack:

- **Backend:** FastAPI
- **LLM Serving:** Ollama (running `gemma:2b` and `nomic-embed-text`)
- **RAG Framework:** LangChain
- **Vector Database:** ChromaDB
