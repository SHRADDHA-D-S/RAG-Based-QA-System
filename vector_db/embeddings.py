from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name):
        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully.")

    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_query(self, query):
        embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        return embedding.tolist()

    @property
    def dimension(self):
        return self.model.get_sentence_embedding_dimension()