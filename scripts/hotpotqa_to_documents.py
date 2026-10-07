from pathlib import Path
from datasets import load_dataset


OUTPUT_DIR = Path("data/hotpotqa/documents")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


print("Loading HotpotQA...")

dataset = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor",
    split="train[:100]"
)


for example in dataset:

    lines = []

    titles = example["context"]["title"]
    sentences = example["context"]["sentences"]

    for title, article_sentences in zip(titles, sentences):

        lines.append(f"# {title}")
        lines.append("")

        for sentence in article_sentences:
            lines.append(sentence)
            lines.append("")

    file_path = OUTPUT_DIR / f"{example['id']}.md"

    file_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )


print(f"Created {len(dataset)} documents.")
print(f"Location: {OUTPUT_DIR}")