import json
from pathlib import Path

from rag.document_parser import DocumentParser


DOCUMENTS_DIR = Path("data/hotpotqa/documents")
OUTPUT_DIR = Path("data/hotpotqa/chunks")
OUTPUT_FILE = OUTPUT_DIR / "chunks.jsonl"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    parser = DocumentParser()

    files = sorted(DOCUMENTS_DIR.glob("*.md"))

    print(f"Found {len(files)} documents")

    total_chunks = 0
    processed_documents = 0
    failed_documents = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:

        for file_path in files:
            print(f"Processing: {file_path.name}")

            try:
                chunks = parser.parse(file_path)

                for chunk in chunks:
                    output.write(
                        json.dumps(
                            chunk,
                            ensure_ascii=False
                        )
                        + "\n"
                    )

                total_chunks += len(chunks)
                processed_documents += 1

                print(f"  Created {len(chunks)} chunks")

            except Exception as error:
                failed_documents += 1
                print(f"  ERROR: {error}")


    print("CHUNKING COMPLETE")
  

    print(f"Documents found: {len(files)}")
    print(f"Documents processed: {processed_documents}")
    print(f"Documents failed: {failed_documents}")
    print(f"Total chunks: {total_chunks}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()