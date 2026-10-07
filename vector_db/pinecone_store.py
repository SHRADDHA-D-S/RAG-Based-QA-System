import hashlib

from pinecone import Pinecone


class PineconeVectorStore:

    def __init__(
        self,
        api_key,
        index_name,
        embedding_service,
        namespace="production",
        cloud="aws",
        region="us-east-1",
        batch_size=100
    ):

        self.index_name = index_name
        self.namespace = namespace
        self.embedding_service = embedding_service
        self.batch_size = batch_size

        self.dimension = embedding_service.dimension

        # Connect to Pinecone
        self.pc = Pinecone(api_key=api_key)

        # Create index if it does not exist
        self._ensure_index(
            cloud=cloud,
            region=region
        )

        # Connect to index
        self.index = self.pc.Index(index_name)

        print(f"Connected to Pinecone index: {index_name}")

    # -----------------------------------
    # CREATE INDEX
    # -----------------------------------

    def _ensure_index(self, cloud, region):

        existing_indexes = [
            index["name"]
            for index in self.pc.list_indexes()
        ]

        if self.index_name in existing_indexes:

            print(
                f"Index already exists: {self.index_name}"
            )

            return

        print(
            f"Creating index: {self.index_name}"
        )

        self.pc.create_index(
            name=self.index_name,
            dimension=self.dimension,
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": cloud,
                    "region": region
                }
            }
        )

        print("Index created successfully.")

    # -----------------------------------
    # GENERATE VECTOR ID
    # -----------------------------------

    @staticmethod
    def generate_id(source, chunk_index):

        raw_id = f"{source}:{chunk_index}"

        return hashlib.sha256(
            raw_id.encode("utf-8")
        ).hexdigest()

    # -----------------------------------
    # INSERT / UPSERT
    # -----------------------------------

    def insert_documents(self, documents):

        if not documents:
            return 0

        texts = [
            document["text"]
            for document in documents
        ]

        # Generate embeddings
        embeddings = (
            self.embedding_service
            .embed_documents(texts)
        )

        vectors = []

        for document, embedding in zip(
            documents,
            embeddings
        ):

            vector_id = self.generate_id(
                document["source"],
                document["chunk_index"]
            )

            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": document["text"],
                    "source": document["source"],
                    "chunk_index": document["chunk_index"]
                }
            })

        total = 0

        # Insert in batches
        for i in range(
            0,
            len(vectors),
            self.batch_size
        ):

            batch = vectors[
                i:i + self.batch_size
            ]

            response = self.index.upsert(
                vectors=batch,
                namespace=self.namespace
            )

            total += response.get(
                "upserted_count",
                len(batch)
            )

        print(
            f"Inserted/updated {total} vectors."
        )

        return total

    # -----------------------------------
    # INSERT FROM JSON DIRECTORY
    # -----------------------------------

    def insert_from_directory(
        self,
        directory,
        chunker
    ):

        from .json_loader import JSONDirectoryLoader

        loader = JSONDirectoryLoader(
            directory
        )

        documents = loader.load()

        all_chunks = []

        for document in documents:

            chunks = chunker.create_chunks(
                document
            )

            all_chunks.extend(chunks)

        print(
            f"Total chunks: {len(all_chunks)}"
        )

        return self.insert_documents(
            all_chunks
        )

    # -----------------------------------
    # SEARCH
    # -----------------------------------

    def search(
        self,
        query,
        top_k=5,
        metadata_filter=None
    ):

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query_embedding = (
            self.embedding_service
            .embed_query(query)
        )

        search_arguments = {
            "vector": query_embedding,
            "top_k": top_k,
            "namespace": self.namespace,
            "include_metadata": True
        }

        if metadata_filter:
            search_arguments["filter"] = (
                metadata_filter
            )

        response = self.index.query(
            **search_arguments
        )

        results = []

        for match in response.matches:

            metadata = match.metadata or {}

            results.append({
                "id": match.id,
                "score": match.score,
                "text": metadata.get("text"),
                "source": metadata.get("source"),
                "chunk_index": metadata.get(
                    "chunk_index"
                )
            })

        return results

    # -----------------------------------
    # UPDATE DOCUMENT
    # -----------------------------------

    def update_document(
        self,
        source,
        chunk_index,
        new_text
    ):

        vector_id = self.generate_id(
            source,
            chunk_index
        )

        embedding = (
            self.embedding_service
            .embed_documents([new_text])[0]
        )

        self.index.upsert(
            vectors=[{
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": new_text,
                    "source": source,
                    "chunk_index": chunk_index
                }
            }],
            namespace=self.namespace
        )

        print(
            f"Updated vector: {vector_id}"
        )

        return vector_id

    # -----------------------------------
    # UPDATE METADATA
    # -----------------------------------

    def update_metadata(
        self,
        vector_id,
        metadata
    ):

        self.index.update(
            id=vector_id,
            set_metadata=metadata,
            namespace=self.namespace
        )

        print(
            f"Metadata updated: {vector_id}"
        )

    # -----------------------------------
    # FETCH VECTOR
    # -----------------------------------

    def fetch(self, vector_id):

        return self.index.fetch(
            ids=[vector_id],
            namespace=self.namespace
        )

    # -----------------------------------
    # DELETE BY ID
    # -----------------------------------

    def delete_by_id(self, vector_id):

        self.index.delete(
            ids=[vector_id],
            namespace=self.namespace
        )

        print(
            f"Deleted vector: {vector_id}"
        )

    # -----------------------------------
    # DELETE BY SOURCE
    # -----------------------------------

    def delete_by_source(self, source):

        self.index.delete(
            filter={
                "source": {
                    "$eq": source
                }
            },
            namespace=self.namespace
        )

        print(
            f"Deleted source: {source}"
        )

    # -----------------------------------
    # DELETE ENTIRE NAMESPACE
    # -----------------------------------

    def clear_namespace(self):

        self.index.delete(
            delete_all=True,
            namespace=self.namespace
        )

        print(
            f"Namespace cleared: {self.namespace}"
        )

    # -----------------------------------
    # INDEX STATISTICS
    # -----------------------------------

    def stats(self):

        return self.index.describe_index_stats()