import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb # <-- Import chromadb

DB_PATH = "./db"

# --- AUTOMATIC DELETION ---
if os.path.exists(DB_PATH):
    print(f"Old database found at '{DB_PATH}'. Deleting it to rebuild...")
    shutil.rmtree(DB_PATH)
    print("Old database deleted successfully.")
# ---------------------------

# 1. Load Documents
loader = DirectoryLoader('./knowledge_base/', glob="**/*.md", loader_cls=TextLoader)
documents = loader.load()

# 2. Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_chunks = text_splitter.split_documents(documents)

# 3. Create embeddings
print("Creating embeddings with 'nomic-embed-text' model...")
embeddings = OllamaEmbeddings(model="nomic-embed-text") 

# 4. Create ChromaDB vector store
# --- PERMISSION FIX ---
# This tells ChromaDB to store its files in a specific, permitted folder.
client_settings = chromadb.Settings(
    is_persistent=True,
    persist_directory=DB_PATH,
)
# --------------------

db = Chroma.from_documents(
    text_chunks,
    embeddings,
    persist_directory=DB_PATH,
    client_settings=client_settings # <-- Pass the settings here
)

print("Vector database created successfully.")