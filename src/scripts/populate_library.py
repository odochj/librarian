from librarian.database.library import Library
from librarian.app import Librarian
from librarian.entities.book import Book
from librarian.sources.pdf_source import PDFSource
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
books = os.getenv("BOOK_PATH")
ACCEPTED_FORMATS = {".pdf"}

librarian = Librarian(Library())
librarian.initialise_library()
print("Library schema initialised.")

def populate_library(book):

    if books is None:
        print("No BOOK_PATH environment variable set. Exiting.")
        return

    book_path = Path(books)
    if not book_path.exists():
        print(f"Books path '{book_path}' does not exist. Exiting.")
        return

    all_books = []
    for subfolder in book_path.iterdir():
        if subfolder.is_dir():
            for file in subfolder.iterdir():
                if file.suffix.lower() in ACCEPTED_FORMATS:
                    all_books.append(file)
    
    for book_file in all_books:
        print(f"Processing: {book_file.name}")
        source = PDFSource(book_file)
        book = Book(source=source)
        librarian.ingest_book(book)
    print("Library population complete.")



if __name__ == "__main__":
    populate_library(books)