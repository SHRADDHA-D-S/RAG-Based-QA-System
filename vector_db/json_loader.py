import json
from pathlib import Path


class JSONDirectoryLoader:

    def __init__(self, directory):
        self.directory = Path(directory)

    def load(self):

        if not self.directory.exists():
            raise FileNotFoundError(
                f"Directory not found: {self.directory}"
            )

        documents = []

        json_files = list(self.directory.rglob("*.json"))

        for file_path in json_files:

            try:

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                documents.append({
                    "source": str(file_path),
                    "data": data
                })

                print(f"Loaded: {file_path}")

            except json.JSONDecodeError:
                print(f"Invalid JSON file: {file_path}")

        return documents