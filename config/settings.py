import os

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#
PINECONE_INDEX_NAME = "rag-qa-system"

#

TOP_K = 5