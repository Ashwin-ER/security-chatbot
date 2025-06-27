#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Wait a few seconds for the server to be ready. 
# A more robust solution would poll the health endpoint, but this is fine for a demo.
echo "Waiting for Ollama server to start..."
sleep 10

# Run the database ingestion script on every start.
# This ensures the DB is always fresh if you update your knowledge base.
echo "Running database ingestion..."
python ingest.py

# Start the FastAPI application.
# Hugging Face Spaces expects the app to run on port 7860.
echo "Starting FastAPI server on port 7860..."
uvicorn main:app --host 0.0.0.0 --port 7860