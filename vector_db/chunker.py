import json


class TextChunker:

    def __init__(self, chunk_size=500, chunk_overlap=50):

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def json_to_text(self, data):

        if isinstance(data, str):
            return data

        return json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

    def split_text(self, text):

        text = text.strip()

        if not text:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk.strip())

            if end >= len(text):
                break

            start = end - self.chunk_overlap

        return chunks

    def create_chunks(self, document):

        source = document["source"]

        data = document["data"]

        text = self.json_to_text(data)

        chunks = self.split_text(text)

        results = []

        for index, chunk in enumerate(chunks):

            results.append({
                "text": chunk,
                "source": source,
                "chunk_index": index
            })

        return results