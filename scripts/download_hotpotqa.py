from datasets import load_dataset


print("Downloading HotpotQA...")

dataset = load_dataset(
    "hotpotqa/hotpot_qa",
    "distractor",
    split="train[:100]"
)

print("Dataset downloaded successfully!")
print(dataset)

print("\nNumber of examples:", len(dataset))

print("\nFirst example:")
print(dataset[0])