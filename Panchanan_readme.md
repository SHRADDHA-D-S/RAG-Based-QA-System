# Docling + RAG: Step-by-Step 

This document collects the learning path for building a modular RAG system using Docling, Jina Embeddings, Pinecone, Groq, and Python.

Main architecture:

```text
PDF
 ↓
Docling
 ↓
DoclingDocument
 ↓
HybridChunker
 ↓
Chunks
 ↓
Jina Embeddings
 ↓
Pinecone
 ↓
Retriever
 ↓
Groq
 ↓
Answer
```


# 1. Recommended Project Structure

```text
D:\Rag
│
├── src
│   └── rag
│       ├── __init__.py
│       ├── document_parser.py
│       ├── embedding_model.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── chat.py
│       └── main.py
│
├── data
│   └── research_paper.pdf
│
├── output.md
├── chunks.json
│
└── .venv
```

| File | Responsibility |
|---|---|
| `document_parser.py` | PDF → DoclingDocument → chunks |
| `embedding_model.py` | Text → vectors |
| `vector_store.py` | Vectors ↔ Pinecone |
| `retriever.py` | Question → relevant chunks |
| `chat.py` | Context + question → Groq answer |
| `main.py` | Connect the complete pipeline |


# 2. Important Python Naming Rule

Do not name your own file after a package that you import.

Avoid:

```text
docling.py
pandas.py
numpy.py
requests.py
torch.py
```

For example, if your file is:

```text
src/rag/docling.py
```

then:

```python
from docling.document_converter import DocumentConverter
```

may import your own file instead of the real Docling package.

Use:

```text
document_parser.py
```

instead.

To check which Docling Python is importing:

```bash
python -c "import docling; print(docling.__file__)"
```

It should point into your virtual environment, such as:

```text
D:\Rag\.venv\Lib\site-packages\docling\__init__.py
```


# 3. Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install Docling:

```bash
python -m pip install docling
```

Install Jupyter:

```bash
python -m pip install jupyter
```

Start Jupyter:

```bash
jupyter notebook
```

or:

```bash
jupyter lab
```


# 4. Hugging Face Warnings

When Docling downloads models, you may see:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This is a warning, not necessarily an error. It means Hugging Face is being accessed without authentication.

You may also see a Windows symlink warning:

```text
your machine does not support symlinks
```

This normally does not stop Docling from working. The cache can still work, although it may use more disk space.

These warnings should be separated from actual Python exceptions.


# 5. What Is Docling?

Docling is a document processing and understanding framework.

It is not an LLM.

Instead of thinking:

```text
PDF → Text
```

think:

```text
PDF
 ↓
Parsing
 ↓
Layout understanding
 ↓
Document structure
 ↓
DoclingDocument
 ↓
Export / Chunking
```

Docling is useful because documents often contain headings, paragraphs, lists, tables, pictures, formulas, multiple columns, and page information.


# 6. Why Docling Is Useful for RAG

A PDF can contain:

- headings
- paragraphs
- lists
- tables
- images
- formulas
- multiple columns
- page information

A basic text extractor may flatten these into one large string.

Docling attempts to preserve useful document structure:

```text
Document
│
├── Heading
├── Paragraph
├── List
├── Table
├── Picture
└── Page / provenance
```

Better document understanding can produce better chunks, which can improve retrieval.


# 7. First Docling Program

Import the converter:

```python
from docling.document_converter import DocumentConverter
```

Create the converter:

```python
converter = DocumentConverter()
```

Convert a PDF:

```python
result = converter.convert("data/research_paper.pdf")
```

Get the document:

```python
doc = result.document
```

The flow is:

```text
PDF
 ↓
DocumentConverter
 ↓
ConversionResult
 ↓
DoclingDocument
```


# 8. Export to Markdown

Export the converted document:

```python
markdown = doc.export_to_markdown()

print(markdown)
```

Save it:

```python
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown)
```

Flow:

```text
PDF
 ↓
Docling
 ↓
DoclingDocument
 ↓
Markdown
 ↓
output.md
```

If you successfully generated the complete Markdown file, your basic Docling conversion is working.


# 9. Inspect DoclingDocument

Check its type:

```python
print(type(doc))
```

Inspect available attributes:

```python
print(dir(doc))
```

Useful concepts include:

```text
texts
tables
pictures
pages
groups
export_to_markdown
export_to_html
```

The exact API can vary with the installed Docling version.


# 10. Inspect Text, Tables, Pictures, and Pages

Text:

```python
for item in doc.texts:
    print(item)
```

Tables:

```python
print("Number of tables:", len(doc.tables))

for i, table in enumerate(doc.tables):
    print(f"TABLE {i + 1}")
    print(table)
```

Pictures:

```python
print("Number of pictures:", len(doc.pictures))
```

Pages:

```python
print("Number of pages:", len(doc.pages))
```

Page information can later be useful for source references.


# 11. Chunking

A large document should not normally be sent to an embedding model as one huge piece.

Instead:

```text
Large document
       ↓
     Chunking
       ↓
 ┌─────┬─────┬─────┬─────┐
 │ C1  │ C2  │ C3  │ C4  │ ...
 └─────┴─────┴─────┴─────┘
```

Each chunk becomes a searchable unit.

RAG quality often follows:

```text
Bad parsing
 ↓
Bad chunks
 ↓
Bad embeddings
 ↓
Bad retrieval
 ↓
Bad answer
```

So chunking is a critical part of RAG.


# 12. Why Not Simply Split Markdown?

You can read:

```python
text = open("output.md", encoding="utf-8").read()
```

and use a generic text splitter.

However, generic splitting may not understand relationships such as:

```text
Heading
 ↓
Paragraph
 ↓
Table
 ↓
Subheading
```

Docling already understands document structure, so its native chunking can use that structure.


# 13. HybridChunker

Import:

```python
from docling.chunking import HybridChunker
```

Create it:

```python
chunker = HybridChunker()
```

Create chunks:

```python
chunks = list(chunker.chunk(doc))
```

Count them:

```python
print("Total chunks:", len(chunks))
```

The exact constructor options can vary by installed Docling version.


# 14. Inspect a Chunk

```python
chunk = chunks[0]

print(type(chunk))
print(dir(chunk))
print(chunk.text)
print(chunk.meta)
```

Then inspect multiple chunks:

```python
for i, chunk in enumerate(chunks[:10]):
    print("=" * 80)
    print(f"CHUNK {i + 1}")
    print("=" * 80)
    print(chunk.text)
```

Ask:

1. Does the chunk represent one idea?
2. Are headings preserved?
3. Are tables understandable?
4. Are sentences cut awkwardly?
5. Are chunks too small?
6. Are chunks too large?


# 15. Why Is It Called HybridChunker?

A simple splitter may use character count.

A structure-aware splitter may use document structure.

HybridChunker combines structure and size constraints.

Conceptually:

```text
HybridChunker
     │
     ├── Document structure
     │
     └── Token-size constraints
             ↓
      Meaningful chunks
```

The goal is not identical chunk sizes.

The goal is:

```text
semantic completeness
+
retrieval quality
+
token constraints
```


# 16. Tokenization and max_tokens

Tokens are not the same as characters.

A model processes tokens.

Conceptually:

```text
Chunk
 ↓
Tokenizer
 ↓
Token count
```

Depending on your installed Docling version, a token limit can be configured conceptually like:

```python
chunker = HybridChunker(
    max_tokens=512
)
```

Do not treat 512 as a magic number.

Possible values to experiment with include:

```text
256
512
768
1024
```

The best value depends on your document, embedding model, retrieval requirements, and evaluation.


# 17. Meaningful Chunking

Do not make every chunk a fixed number of characters just because fixed sizes are easy.

For example, a bad boundary might produce:

```text
Chunk 1:
Linear Regression is a supervised learning algorithm.
The main formula is:

Chunk 2:
y = mx + b

where m represents...
```

A structure-aware chunker tries to preserve meaningful boundaries.

The goal is:

```text
Meaningful retrieval unit
```

not:

```text
Perfectly equal-sized text
```


# 18. Heading Context

Suppose the document contains:

```text
Machine Learning

Supervised Learning

Linear Regression

Linear regression predicts continuous values.
```

Only storing:

```text
Linear regression predicts continuous values.
```

may lose hierarchy.

A richer representation can preserve:

```text
Machine Learning
Supervised Learning
Linear Regression

Linear regression predicts continuous values.
```

Context can improve semantic retrieval.


# 19. Tables and Chunking

Example:

```text
| Model | Accuracy |
|---|---:|
| Linear Regression | 82% |
| Logistic Regression | 91% |
```

A useful representation should preserve the relationship between model and accuracy.

A flattened representation such as:

```text
Model Accuracy Linear Regression 82 Logistic Regression 91
```

is less readable.

Docling's structured representation helps the chunking process deal with structured elements.


# 20. Chunk Statistics

Calculate character statistics:

```python
chunk_lengths = [
    len(chunk.text)
    for chunk in chunks
]

print("Number of chunks:", len(chunk_lengths))
print("Minimum:", min(chunk_lengths))
print("Maximum:", max(chunk_lengths))
print(
    "Average:",
    sum(chunk_lengths) / len(chunk_lengths)
)
```

Find large chunks:

```python
for i, chunk in enumerate(chunks):
    if len(chunk.text) > 2000:
        print("=" * 80)
        print(f"Large chunk: {i}")
        print(chunk.text)
```

Find small chunks:

```python
for i, chunk in enumerate(chunks):
    if len(chunk.text) < 200:
        print("=" * 80)
        print(f"Small chunk: {i}")
        print(chunk.text)
```

Small or large chunks are not automatically wrong. Inspect them.


# 21. Serialization

Serialization means converting structured information into a text representation.

Conceptually:

```text
Structured document
        ↓
    serialization
        ↓
       text
```

Inspect it:

```python
for i, chunk in enumerate(chunks[:5]):

    print("=" * 80)
    print(f"CHUNK {i + 1}")

    print("\\nTEXT:")
    print(chunk.text)

    print("\\nSERIALIZED:")
    print(chunker.serialize(chunk))
```

For simple paragraphs the representations may be similar. Structured content can benefit more from serialization.


# 22. chunk.text vs serialize()

Compare both representations:

```python
for i, chunk in enumerate(chunks[:10]):

    print("=" * 100)
    print(f"CHUNK {i + 1}")

    print("\\n--- chunk.text ---")
    print(chunk.text)

    print("\\n--- chunker.serialize(chunk) ---")
    print(chunker.serialize(chunk))
```

Do not assume one is always better.

The correct choice should eventually be tested using retrieval quality.


# 23. Inspect Your Installed Docling API

Libraries change over time.

Check the version:

```python
import docling

print(docling.__version__)
```

Inspect the HybridChunker constructor:

```python
import inspect
from docling.chunking import HybridChunker

print(inspect.signature(HybridChunker))
```

Read its documentation:

```python
help(HybridChunker)
```

This is safer than blindly copying code from an old tutorial.


# 24. Chunk Inspection Function

```python
def inspect_chunks(chunks, n=5):

    for i, chunk in enumerate(chunks[:n]):

        print("=" * 100)
        print(f"CHUNK {i + 1}")
        print("=" * 100)

        print(chunk.text)
        print("\\nCHARACTERS:", len(chunk.text))
        print()
```

Use:

```python
inspect_chunks(chunks, n=10)
```


# 25. Chunk Statistics Function

```python
def chunk_statistics(chunks):

    lengths = [
        len(chunk.text)
        for chunk in chunks
    ]

    print("Total chunks:", len(chunks))
    print("Minimum characters:", min(lengths))
    print("Maximum characters:", max(lengths))
    print(
        "Average characters:",
        sum(lengths) / len(lengths)
    )
```

Use:

```python
chunk_statistics(chunks)
```


# 26. Save Chunks to JSON

```python
import json

chunk_data = []

for i, chunk in enumerate(chunks):

    chunk_data.append({
        "chunk_id": i,
        "text": chunk.text
    })

with open(
    "chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunk_data,
        f,
        ensure_ascii=False,
        indent=2
    )
```

Later, add metadata such as:

```json
{
  "chunk_id": 0,
  "text": "...",
  "source": "research_paper.pdf",
  "page": 4,
  "section": "Machine Learning",
  "metadata": {}
}
```


# 27. document_parser.py

This module should focus on:

```text
PDF
 ↓
Docling
 ↓
DoclingDocument
 ↓
Chunking
 ↓
Chunks
```

Example:

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


class DocumentParser:

    def __init__(self):
        self.converter = DocumentConverter()
        self.chunker = HybridChunker()

    def parse(self, file_path):

        result = self.converter.convert(file_path)

        doc = result.document

        chunks = list(
            self.chunker.chunk(doc)
        )

        return chunks
```


# 28. Test document_parser.py

Create:

```text
test_parser.py
```

Code:

```python
from src.rag.document_parser import DocumentParser


parser = DocumentParser()

chunks = parser.parse(
    "data/research_paper.pdf"
)

print(
    "Total chunks:",
    len(chunks)
)

for i, chunk in enumerate(chunks[:5]):

    print("=" * 80)
    print(f"CHUNK {i + 1}")
    print("=" * 80)

    print(chunk.text)
```

Run from:

```text
D:\Rag
```

with:

```bash
python test_parser.py
```

Test modules independently before connecting the complete system.


# 29. embedding_model.py

This module should have one main responsibility:

```text
text → vectors
```

Conceptual design:

```python
class EmbeddingModel:

    def __init__(self, model_name):
        # initialize embedding model
        pass

    def embed(self, texts):
        # convert text to vectors
        pass
```

For this project, the planned embedding stage is Jina.

The exact Jina model/API configuration should be selected based on the current model you intend to use.


# 30. Why the Embedding Model Is Used Twice

This is a core RAG concept.

During ingestion:

```text
Document chunk
      ↓
Jina
      ↓
Vector
      ↓
Pinecone
```

During querying:

```text
User question
      ↓
Jina
      ↓
Query vector
      ↓
Pinecone
      ↓
Similar document vectors
```

The document and query need to be represented in the same embedding space.

Conceptually:

```text
"Python is a programming language."
        ↓ Jina
Document vector

"What is Python?"
        ↓ Jina
Query vector

       ↓

Vector similarity
```


# 31. vector_store.py

This module should handle:

```text
vectors ↔ Pinecone
```

Conceptually:

```python
class VectorStore:

    def add_documents(self, chunks, embeddings):
        pass

    def search(self, query_vector, top_k=5):
        pass
```

It should not know how Docling parses a PDF.


# 32. retriever.py

The retriever should handle:

```text
question
 ↓
embedding
 ↓
vector database
 ↓
relevant chunks
```

Conceptually:

```python
class Retriever:

    def retrieve(self, question, top_k=5):
        pass
```

It should return relevant chunks rather than generate the final answer.


# 33. chat.py

`chat.py` should mainly handle LLM generation.

Conceptually:

```python
class ChatModel:

    def __init__(self, llm):
        self.llm = llm

    def answer(self, question, context):

        prompt = f\"\"\"
Answer the question using the context.

Context:
{context}

Question:
{question}
\"\"\"

        return self.llm.invoke(prompt)
```

The separation is:

```text
Retriever
    ↓
relevant context

Chat model
    ↓
answer
```


# 34. Do Not Put Everything in chat.py

Avoid:

```text
chat.py
 ├── PDF parsing
 ├── Docling
 ├── chunking
 ├── embeddings
 ├── Pinecone
 └── Groq
```

Prefer:

```text
document_parser.py
        ↓
      chunks

embedding_model.py
        ↓
     vectors

vector_store.py
        ↓
     Pinecone

retriever.py
        ↓
 relevant chunks

chat.py
        ↓
      Groq
```

This modular design makes debugging and maintenance much easier.


# 35. main.py

`main.py` can connect the modules.

Conceptually:

```python
from src.rag.document_parser import DocumentParser
from src.rag.embedding_model import EmbeddingModel


def main():

    parser = DocumentParser()

    chunks = parser.parse(
        "data/research_paper.pdf"
    )

    texts = [
        chunk.text
        for chunk in chunks
    ]

    embedding_model = EmbeddingModel(
        "YOUR_JINA_MODEL"
    )

    embeddings = embedding_model.embed(
        texts
    )

    print("Chunks:", len(chunks))
    print("Embeddings:", embeddings.shape)


if __name__ == "__main__":
    main()
```

The exact Jina implementation is added after selecting/configuring the model.


# 36. Complete Ingestion Pipeline

```text
research_paper.pdf
        │
        ▼
document_parser.py
        │
        ▼
Docling
        │
        ▼
DoclingDocument
        │
        ▼
HybridChunker
        │
        ▼
Chunks
        │
        ▼
embedding_model.py
        │
        ▼
Jina Embeddings
        │
        ▼
Vectors
        │
        ▼
vector_store.py
        │
        ▼
Pinecone
```


# 37. Complete Query Pipeline

Example question:

```text
What is linear regression?
```

Pipeline:

```text
User question
      │
      ▼
retriever.py
      │
      ▼
embedding_model.py
      │
      ▼
Jina
      │
      ▼
Query vector
      │
      ▼
Pinecone
      │
      ▼
Top-K relevant chunks
      │
      ▼
chat.py
      │
      ▼
Groq
      │
      ▼
Final answer
```


# 38. Complete RAG Architecture

```text
                         USER
                           │
                           ▼
                    User Question
                           │
                           ▼
                     Retriever
                           │
                           ▼
                  Embedding Model
                           │
                           ▼
                         Jina
                           │
                           ▼
                       Pinecone
                           │
                           ▼
                    Relevant Chunks
                           │
                           ▼
                         Groq
                           │
                           ▼
                         Answer


        INGESTION PIPELINE

PDF / DOCX / etc.
       │
       ▼
 document_parser.py
       │
       ▼
     Docling
       │
       ▼
 DoclingDocument
       │
       ▼
 HybridChunker
       │
       ▼
    Chunks
       │
       ▼
 embedding_model.py
       │
       ▼
      Jina
       │
       ▼
    Vectors
       │
       ▼
 vector_store.py
       │
       ▼
   Pinecone
```


# 39. Recommended Learning Order

Follow this order:

```text
1. Docling installation                         ✓
2. PDF conversion                              ✓
3. Markdown export                             ✓
4. DoclingDocument                             ✓
5. Text / tables / pictures / pages            ✓
6. HybridChunker                               ✓
7. Chunk inspection                            ✓
8. Serialization                               ✓
9. Tokenization
10. Chunk-size experiments
11. Jina Embeddings
12. Embedding generation
13. Pinecone
14. Store vectors
15. Query embedding
16. Retrieval
17. Retriever module
18. Groq
19. Prompt construction
20. Complete RAG
21. Retrieval evaluation
22. RAG evaluation
23. Optimization
```


# 40. Most Important Principle

Do not think of RAG as:

```text
PDF → LLM
```

Think:

```text
PDF
 ↓
Document understanding
 ↓
Good chunks
 ↓
Good embeddings
 ↓
Good vector search
 ↓
Relevant context
 ↓
LLM
 ↓
Answer
```

The LLM is only one part of the system.

Good retrieval gives the LLM the information it needs.


# 41. Current Position and Next Step

Completed:

```text
PDF
 ↓
Docling
 ↓
DoclingDocument
 ↓
Markdown
```

Started:

```text
DoclingDocument
 ↓
HybridChunker
 ↓
Chunks
```

Next major stage:

```text
Chunks
   ↓
Jina Embedding Model
   ↓
Vectors
```

Then:

```text
Vectors
   ↓
Pinecone
```

Then:

```text
Question
   ↓
Jina
   ↓
Pinecone
   ↓
Relevant chunks
   ↓
Groq
   ↓
Answer
```

This produces a modular RAG system instead of one large script.


# 42. Using HotpotQA from Hugging Face as the Project Dataset

For this project, use the official Hugging Face `hotpotqa/hotpot_qa` dataset rather than a random research-paper PDF.

HotpotQA is especially suitable for learning RAG because it is a multi-hop question-answering dataset. It contains questions, answers, context passages, and sentence-level supporting facts. The official dataset provides `distractor` and `fullwiki` configurations. The `distractor` configuration has 90,447 training examples and 7,405 validation examples; `fullwiki` has 90,447 train, 7,405 validation, and 7,405 test examples. The dataset is distributed under CC BY-SA 4.0. citeturn0search0turn0search10

Official dataset:

urlHotpotQA on Hugging Facehttps://huggingface.co/datasets/hotpotqa/hotpot_qa

For learning, start with a small slice such as 100 or 1,000 examples. Do not download/process the entire dataset immediately.

---

# 43. Install the Hugging Face Dataset Library

Install:

```bash
python -m pip install datasets
```

You can also install pandas for inspection:

```bash
python -m pip install pandas
```

Check:

```python
import datasets

print(datasets.__version__)
```

---

# 44. Load HotpotQA

Use the official dataset:

```python
from datasets import load_dataset

dataset = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor"
)

print(dataset)
```

For learning, load only a small subset:

```python
train_dataset = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor",
    split="train[:100]"
)

print(train_dataset)
```

The dataset fields include:

```text
id
question
answer
type
level
supporting_facts
context
```

The `context` contains article titles and sentences, while `supporting_facts` identifies the relevant supporting sentences. citeturn0search0turn0search7

---

# 45. Inspect One HotpotQA Example

```python
example = train_dataset[0]

print(example.keys())
```

Print the question:

```python
print("QUESTION:")
print(example["question"])
```

Print the answer:

```python
print("\nANSWER:")
print(example["answer"])
```

Print question type:

```python
print("\nTYPE:")
print(example["type"])
```

Print difficulty:

```python
print("\nLEVEL:")
print(example["level"])
```

---

# 46. Inspect the Context

```python
context = example["context"]

print(context)
```

The context contains article titles and their sentences.

A useful inspection:

```python
for title, sentences in zip(
    context["title"],
    context["sentences"]
):
    print("=" * 80)
    print("TITLE:", title)
    print("=" * 80)

    for sentence in sentences:
        print(sentence)
```

This is the actual information that the RAG system will retrieve.

---

# 47. Inspect Supporting Facts

HotpotQA provides sentence-level supporting facts.

```python
supporting_facts = example["supporting_facts"]

print(supporting_facts)
```

Inspect them:

```python
for title, sent_id in zip(
    supporting_facts["title"],
    supporting_facts["sent_id"]
):
    print("Title:", title)
    print("Sentence ID:", sent_id)
```

This is extremely useful for RAG evaluation because you can compare retrieved chunks against the known supporting evidence.

---

# 48. Understand the HotpotQA Data Model

Conceptually:

```text
HotpotQA Example
│
├── question
│
├── answer
│
├── type
│
├── level
│
├── context
│   ├── article title
│   │   ├── sentence
│   │   ├── sentence
│   │   └── ...
│   │
│   └── another article
│       ├── sentence
│       └── ...
│
└── supporting_facts
    ├── title
    └── sentence ID
```

This makes HotpotQA a good dataset for learning retrieval and multi-hop RAG.

---

# 49. Convert One HotpotQA Example into Markdown

Docling works with documents. HotpotQA gives us structured text.

Therefore, create a Markdown representation from the HotpotQA context.

```python
def hotpot_to_markdown(example):

    lines = []

    for title, sentences in zip(
        example["context"]["title"],
        example["context"]["sentences"]
    ):

        lines.append(f"# {title}")
        lines.append("")

        for sentence in sentences:
            lines.append(sentence)
            lines.append("")

    return "\n".join(lines)
```

Test:

```python
markdown = hotpot_to_markdown(example)

print(markdown[:5000])
```

Now the flow becomes:

```text
HotpotQA
   ↓
context
   ↓
Markdown
   ↓
Docling
```

---

# 50. Save HotpotQA as a Markdown Document

Create a directory:

```python
from pathlib import Path

Path("data/hotpotqa").mkdir(
    parents=True,
    exist_ok=True
)
```

Save one example:

```python
file_path = Path(
    "data/hotpotqa/example_0000.md"
)

file_path.write_text(
    markdown,
    encoding="utf-8"
)
```

Now you have:

```text
data/
└── hotpotqa/
    └── example_0000.md
```

---

# 51. Why Convert HotpotQA to Markdown?

HotpotQA itself is not a PDF.

So there are two different learning goals:

### Goal A — Learn Docling

```text
PDF / Markdown / document
 ↓
Docling
 ↓
DoclingDocument
 ↓
HybridChunker
```

### Goal B — Build RAG with HotpotQA

```text
HotpotQA context
 ↓
Chunks
 ↓
Embeddings
 ↓
Pinecone
 ↓
Question retrieval
 ↓
Groq
```

Converting HotpotQA context to Markdown lets you combine both learning goals.

---

# 52. Parse the Generated Markdown with Docling

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

result = converter.convert(
    "data/hotpotqa/example_0000.md"
)

doc = result.document

print(type(doc))
```

Export it back to Markdown:

```python
output = doc.export_to_markdown()

print(output)
```

The flow is:

```text
HotpotQA
 ↓
Python
 ↓
Markdown file
 ↓
Docling
 ↓
DoclingDocument
```

---

# 53. Chunk the HotpotQA Document

```python
from docling.chunking import HybridChunker

chunker = HybridChunker()

chunks = list(
    chunker.chunk(doc)
)

print("Total chunks:", len(chunks))
```

Inspect:

```python
for i, chunk in enumerate(chunks):

    print("=" * 80)
    print("CHUNK:", i)
    print("=" * 80)
    print(chunk.text)
```

Now your learning pipeline is:

```text
HotpotQA context
       ↓
Markdown
       ↓
Docling
       ↓
HybridChunker
       ↓
Chunks
```

---

# 54. Important: Keep HotpotQA Metadata

Do not store only the text.

For each example, keep:

```text
dataset_id
question
answer
chunk_id
article_title
supporting_facts
chunk_text
```

For example:

```python
chunk_record = {
    "dataset_id": example["id"],
    "question": example["question"],
    "answer": example["answer"],
    "chunk_id": 0,
    "chunk_text": chunks[0].text
}
```

This metadata will be very useful during evaluation.

---

# 55. Better Chunk Records

A useful structure is:

```python
chunk_record = {
    "dataset_id": example["id"],
    "chunk_id": 0,
    "source_title": "Article title",
    "text": chunks[0].text,
    "question": example["question"],
    "answer": example["answer"],
    "supporting_facts": example["supporting_facts"]
}
```

Later, the `question` and `answer` should normally be kept in an evaluation dataset rather than duplicated into every production vector record. For learning, keeping them together can make debugging easier.

---

# 56. Build a Small HotpotQA Document Collection

Start with only 100 examples.

```python
from datasets import load_dataset

dataset = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor",
    split="train[:100]"
)
```

Create folders:

```python
from pathlib import Path

output_dir = Path("data/hotpotqa")

output_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

Create Markdown documents:

```python
for i, example in enumerate(dataset):

    markdown = hotpot_to_markdown(example)

    path = output_dir / f"{i:05d}.md"

    path.write_text(
        markdown,
        encoding="utf-8"
    )

print("Documents created:", len(dataset))
```

Result:

```text
data/
└── hotpotqa/
    ├── 00000.md
    ├── 00001.md
    ├── 00002.md
    ├── ...
    └── 00099.md
```

---

# 57. Parse Multiple HotpotQA Documents

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

all_chunks = []

for file_path in output_dir.glob("*.md"):

    result = converter.convert(
        str(file_path)
    )

    doc = result.document

    chunks = list(
        chunker.chunk(doc)
    )

    for chunk_id, chunk in enumerate(chunks):

        all_chunks.append({
            "source": file_path.name,
            "chunk_id": chunk_id,
            "text": chunk.text
        })

print(
    "Total chunks:",
    len(all_chunks)
)
```

Now:

```text
100 HotpotQA examples
        ↓
100 Markdown documents
        ↓
Docling
        ↓
HybridChunker
        ↓
all_chunks
```

---

# 58. Save the Chunk Dataset

```python
import json

with open(
    "data/hotpotqa/chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )
```

This gives:

```text
data/
└── hotpotqa/
    ├── 00000.md
    ├── 00001.md
    ├── ...
    └── chunks.json
```

---

# 59. Embedding HotpotQA Chunks

The next stage is:

```text
chunks
 ↓
Jina embedding model
 ↓
vectors
```

Conceptually:

```python
texts = [
    item["text"]
    for item in all_chunks
]

embeddings = embedding_model.embed(
    texts
)
```

Check:

```python
print(embeddings.shape)
```

If there are 1,000 chunks and the embedding dimension is 1024, conceptually:

```text
(1000, 1024)
```

The exact dimension depends on the selected Jina model/configuration.

---

# 60. Store HotpotQA Vectors in Pinecone

The ingestion pipeline becomes:

```text
HotpotQA
 ↓
Markdown
 ↓
Docling
 ↓
HybridChunker
 ↓
Chunks
 ↓
Jina
 ↓
Vectors
 ↓
Pinecone
```

Each Pinecone record should contain metadata such as:

```text
id
text
source
dataset_id
chunk_id
article_title
```

Do not put huge unnecessary metadata into every vector record.

---

# 61. Query HotpotQA

Take a validation question:

```python
validation = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor",
    split="validation[:10]"
)

question = validation[0]["question"]

print(question)
```

Then:

```text
Question
   ↓
Jina embedding
   ↓
Query vector
   ↓
Pinecone similarity search
   ↓
Top-K chunks
```

---

# 62. Compare Retrieved Chunks with Supporting Facts

This is one of the biggest advantages of HotpotQA.

The dataset tells us which sentences are supporting facts.

Therefore you can evaluate:

```text
Expected supporting evidence
          vs
Retrieved chunks
```

Conceptually:

```text
HotpotQA supporting_facts
          │
          ▼
      Ground truth
          │
          │ compare
          ▼
Pinecone retrieved chunks
```

This lets you measure retrieval quality rather than only checking whether the final answer looks correct.

---

# 63. Retrieval Metrics

Useful metrics to learn:

### Recall@K

Did the retrieved top-K chunks contain the required supporting evidence?

```text
Recall@K =
relevant retrieved evidence
----------------------------
total relevant evidence
```

### Precision@K

How much of the retrieved content was relevant?

```text
Precision@K =
relevant retrieved chunks
-------------------------
all retrieved chunks
```

### Hit Rate@K

Did at least one relevant item appear in the top K?

```text
Hit@K = 1
```

if relevant evidence was retrieved.

Otherwise:

```text
Hit@K = 0
```

HotpotQA's supporting-fact annotations make this type of evaluation especially useful. citeturn0search0

---

# 64. HotpotQA Multi-Hop RAG

HotpotQA is especially interesting because many questions require information from multiple documents.

Conceptually:

```text
Question
   │
   ├───────────────┐
   ▼               ▼
Article A        Article B
   │               │
Fact A            Fact B
   │               │
   └───────┬───────┘
           ▼
        Reasoning
           │
           ▼
         Answer
```

This is more challenging than single-document retrieval.

---

# 65. Example RAG Goal

Suppose the question requires:

```text
Fact A from Article A
+
Fact B from Article B
```

The retriever should ideally return both:

```text
Top-K results
 ├── Article A chunk
 └── Article B chunk
```

Then Groq receives:

```text
Context:
[Article A evidence]
[Article B evidence]

Question:
...

Answer:
...
```

This is why HotpotQA is a strong dataset for learning multi-hop RAG.
