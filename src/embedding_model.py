import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)
    
text = "Python is a programming language."


def get_embedding(text):
    response = client.embeddings.create(
        model="nvidia/nemotron-3-embed-1b",
        input=text,
        extra_body={
            "input_type": "passage"
        }
    )

    return response.data[0].embedding

embedding = get_embedding(text)
print("Embedding generated successfully!")
print("Embedding dimension:", len(embedding))
print("First 10 values:", embedding[:10])