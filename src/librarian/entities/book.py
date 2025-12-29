from typing import Optional
from librarian.sources.text_source import TextSource


class Book:
    def __init__(self, source: TextSource):
        self.book_id: Optional[int] = None
        self.title = source.path.stem.replace("_", " ").title()
        self.source = source
        self.path = source.path

    @property
    def is_persisted(self) -> bool:
        return self.book_id is not None
