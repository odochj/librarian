from library.book.book import Book
from topic import Topic

"""
The Library must be an immutable registry of unique books.

"""

class Library:
    books: list[Book]
    subjects: dict[str,list[Topic]]

    def add_book(self, Book) -> None:
        """
        Add a new book to the Library
        
        - retrieve table of contents
        - extract topics
        - append Book to list of Books 
        """
        return None 
    
    def remove_book(self, Book) -> None:
        """
        Permanently delete a book from the Library
        """ 
        return None
    def recommend_book(self, str) -> Book | list[Book] | None:
        """
        Accept Natural Language as input, and recommend one or books
        """
        
        return None 
    def recommend_topics(self, str) ->  Book | list[Book] | None:
        """
        Accept Natural Language as input, and recommend one or books
        """
        return None

    