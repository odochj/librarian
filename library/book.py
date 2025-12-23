from pathlib import Path

class Book:
    name: str
    contents: dict
    summary: str
    path: Path

    def retrieve_contents(self) -> None:
        """
        Chunk through the book until the table of contnts is found
        Return a dictionary of page numbers (as strings) and content names
        """
        return None
    
