from pathlib import Path
from typing import Any

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


class DocumentParser:
    def __init__(self):
        self.converter = DocumentConverter()
        self.chunker = HybridChunker()

    def parse(self, file_path: str | Path) -> list[dict[str, Any]]:
        file_path = Path(file_path)

        result = self.converter.convert(str(file_path))
        doc = result.document

        chunks = list(self.chunker.chunk(doc))

        results = []

        for i, chunk in enumerate(chunks):
            results.append(
                {
                    "id": f"{file_path.stem}_chunk_{i}",
                    "text": chunk.text,
                    "metadata": {
                        "source": file_path.name,
                        "chunk_index": i,
                    },
                }
            )

        return results