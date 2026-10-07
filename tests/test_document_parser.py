from src.rag.document_parser import DocumentParser


parser = DocumentParser()

file_path = "data/hotpotqa/documents/5a7a0a965542996c55b2dce7.md"

chunks = parser.parse(file_path)

print("Total chunks:", len(chunks))

for chunk in chunks[:5]:
    print("\n==============================")
    print("ID:", chunk["id"])
    print("TEXT:", chunk["text"])
    print("METADATA:", chunk["metadata"])