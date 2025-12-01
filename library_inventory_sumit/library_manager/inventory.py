import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(filename="library.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class LibraryInventory:
    def __init__(self, filepath="data/catalog.json"):
        self.filepath = Path(filepath)
        self.books = []
        self.load()

    def load(self):
        try:
            if not self.filepath.exists():
                self.save()
                return

            with open(self.filepath, "r") as f:
                data = json.load(f)

            self.books = [Book(**book) for book in data]

        except Exception as e:
            logging.error(f"Error loading JSON: {e}")
            self.books = []

    def save(self):
        try:
            self.filepath.parent.mkdir(exist_ok=True)
            with open(self.filepath, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving JSON: {e}")

    def add_book(self, book):
        self.books.append(book)
        self.save()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def display_all(self):
        return self.books
