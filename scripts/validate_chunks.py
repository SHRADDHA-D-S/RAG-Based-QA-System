import json
from collections import Counter
from pathlib import Path


CHUNKS_FILE = Path("data/hotpotqa/chunks/chunks.jsonl")


def main():
    if not CHUNKS_FILE.exists():
        print(f"ERROR: File not found: {CHUNKS_FILE}")
        return

    chunks = []
    errors = []

    # Read JSONL file
    with CHUNKS_FILE.open("r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                chunk = json.loads(line)
                chunks.append(chunk)

            except json.JSONDecodeError as error:
                errors.append(
                    f"Line {line_number}: Invalid JSON - {error}"
                )

    print("\n==============================")
    print("CHUNK VALIDATION")
    print("==============================")

    # Total chunks
    print(f"Total chunks: {len(chunks)}")

    # Duplicate IDs
    ids = [chunk.get("id") for chunk in chunks]

    duplicate_ids = [
        chunk_id
        for chunk_id, count in Counter(ids).items()
        if count > 1
    ]

    print(f"Duplicate IDs: {len(duplicate_ids)}")

    # Empty chunks
    empty_text_chunks = [
        chunk.get("id")
        for chunk in chunks
        if not chunk.get("text", "").strip()
    ]

    print(f"Empty chunks: {len(empty_text_chunks)}")

    # Metadata validation
    missing_metadata = [
        chunk.get("id")
        for chunk in chunks
        if not isinstance(chunk.get("metadata"), dict)
    ]

    print(f"Missing/invalid metadata: {len(missing_metadata)}")

    # Required fields
    missing_fields = []

    for chunk in chunks:
        for field in ["id", "text", "metadata"]:
            if field not in chunk:
                missing_fields.append(
                    (chunk.get("id", "UNKNOWN"), field)
                )

    print(f"Missing required fields: {len(missing_fields)}")

    # Text length statistics
    text_lengths = [
        len(chunk.get("text", "").strip())
        for chunk in chunks
    ]

    if text_lengths:
        print(
            f"Minimum text length: {min(text_lengths)} characters"
        )

        print(
            f"Maximum text length: {max(text_lengths)} characters"
        )

        print(
            f"Average text length: "
            f"{sum(text_lengths) / len(text_lengths):.2f} characters"
        )

    # Source statistics
    sources = [
        chunk.get("metadata", {}).get("source")
        for chunk in chunks
    ]

    unique_sources = set(sources)

    print(f"Unique source documents: {len(unique_sources)}")

    # Final result
    print("\n==============================")

    if (
        not errors
        and not duplicate_ids
        and not empty_text_chunks
        and not missing_metadata
        and not missing_fields
    ):
        print("VALIDATION PASSED")
        print("==============================")
        print("Chunks are ready for the embedding stage.")

    else:
        print("VALIDATION FAILED")
        print("==============================")

        if errors:
            print(f"JSON errors: {len(errors)}")

        if duplicate_ids:
            print(f"Duplicate IDs: {duplicate_ids[:5]}")

        if empty_text_chunks:
            print(f"Empty chunks: {empty_text_chunks[:5]}")

        if missing_fields:
            print(f"Missing fields: {missing_fields[:5]}")


if __name__ == "__main__":
    main()