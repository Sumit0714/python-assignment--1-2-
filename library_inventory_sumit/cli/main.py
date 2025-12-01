from library_manager.book import Book
from library_manager.inventory import LibraryInventory

def menu():
    print("\n===== Library Inventory Manager =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")

def main():
    inventory = LibraryInventory()

    while True:
        menu()
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                isbn = input("ISBN: ").strip()

                if not title or not author or not isbn:
                    print("All fields are required.")
                    continue

                inventory.add_book(Book(title, author, isbn))
                print("Book added successfully!")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ").strip()
                book = inventory.search_by_isbn(isbn)

                if book:
                    if book.issue():
                        inventory.save()
                        print("Book issued successfully.")
                    else:
                        print("Book already issued.")
                else:
                    print("ISBN not found.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ").strip()
                book = inventory.search_by_isbn(isbn)

                if book:
                    book.return_book()
                    inventory.save()
                    print("Book returned successfully.")
                else:
                    print("Invalid ISBN.")

            elif choice == "4":
                books = inventory.display_all()

                if not books:
                    print("No books available.")
                else:
                    for b in books:
                        print(b)

            elif choice == "5":
                keyword = input("Enter title to search: ").strip()
                results = inventory.search_by_title(keyword)

                if not results:
                    print("No matching books found.")
                else:
                    for r in results:
                        print(r)

            elif choice == "6":
                print("Exiting program...")
                break

            else:
                print("Invalid input. Choose 1-6.")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
