import unittest
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

class TestInventory(unittest.TestCase):

    def test_add_and_search(self):
        inv = LibraryInventory("data/test.json")
        inv.add_book(Book("Test Book", "Author", "111"))
        self.assertIsNotNone(inv.search_by_isbn("111"))

if __name__ == "__main__":
    unittest.main()
