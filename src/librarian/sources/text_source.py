from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

class TextSource(ABC):
    def __init__(self, path: Path):
        self.path = path

    @abstractmethod
    def iter_lines(self) -> Iterator[str]:
        """Yield text line-by-line, lazily."""
        pass
    @abstractmethod
    def iter_pages(self) -> Iterator[str]:
        """Yield text page-by-page, lazily."""
        pass