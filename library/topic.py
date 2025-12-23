from book import Book
class Topic:
    name: str
    books: tuple[Book, list[str]]

    def extract_topics(self) -> None:
        """
        Infer Topic from a Book's contents
        """
        
        return None