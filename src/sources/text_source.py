from abc import ABC, abstractmethod
from typing import Iterator

class TextSource(ABC):
    @abstractmethod
    def iter_lines(self) -> Iterator[str]:
        """Yield text line-by-line, lazily."""
