import os

from dotenv import load_dotenv

load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# PINECONE_INDEX_NAME = "rag-qa-system"

EMBEDDING_MODEL = "nemotron-3-embed-1b"

TOP_K = 5