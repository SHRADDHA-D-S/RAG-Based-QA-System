import os

from dotenv import load_dotenv

from vector_db.embeddings import EmbeddingService
from vector_db.chunker import TextChunker
from vector_db.pinecone_store import PineconeVectorStore


# Load environment variables
load_dotenv()


# -----------------------------------
# SETTINGS
# -----------------------------------

API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "rag-documents"
)

NAMESPACE = os.getenv(
    "PINECONE_NAMESPACE",
    "production"
)

MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)


# -----------------------------------
# CREATE EMBEDDING SERVICE
# -----------------------------------

embedding_service = EmbeddingService(
    MODEL_NAME
)


# -----------------------------------
# CREATE CHUNKER
# -----------------------------------

chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=50
)


# -----------------------------------
# CREATE PINECONE VECTOR STORE
# -----------------------------------

vector_store = PineconeVectorStore(
    api_key=API_KEY,
    index_name=INDEX_NAME,
    embedding_service=embedding_service,
    namespace=NAMESPACE
)


# -----------------------------------
# INSERT JSON DATA
# -----------------------------------

print("\n--- INSERTING DATA ---")

vector_store.insert_from_directory(
    "data",
    chunker
)


# -----------------------------------
# SEARCH
# -----------------------------------

print("\n--- SEARCHING ---")

results = vector_store.search(
    "What type of soil is suitable for tomato cultivation?",
    top_k=3
)

for result in results:

    print("\nScore:", result["score"])
    print("Text:", result["text"])
    print("Source:", result["source"])


# -----------------------------------
# STATISTICS
# -----------------------------------

print("\n--- PINECONE STATS ---")

print(
    vector_store.stats()
)