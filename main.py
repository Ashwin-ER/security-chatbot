import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
import asyncio
import chromadb # <-- Import chromadb

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Model and Database Setup ---
print("Loading vector database and Ollama embeddings...")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# --- PERMISSION FIX ---
# We must use the same settings here to access the database correctly.
client_settings = chromadb.Settings(
    is_persistent=True,
    persist_directory="./db",
)
# --------------------

vectorstore = Chroma(
    persist_directory="./db", 
    embedding_function=embeddings,
    client_settings=client_settings # <-- Pass the settings here
)

llm = Ollama(model="gemma:2b")

prompt_template = """
### Instruction:
You are an expert assistant for a security intelligence application.
Use only the following context to answer the question.
If you don't know the answer from the context, just say that you don't have enough information.
Do not make up any information.

### Context:
{context}

### User Question:
{question}

### Response:
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
)
print("Chatbot is ready!")
# ----------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(query: str = Form(...)):
    
    async def stream_response_generator():
        async for chunk in qa_chain.astream({"query": query}):
            if "result" in chunk:
                yield chunk["result"]
                await asyncio.sleep(0.01)

    return StreamingResponse(stream_response_generator(), media_type="text/plain")