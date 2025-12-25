from abc import ABC, abstractmethod
from typing import Iterator


class TextSource(ABC):
    @abstractmethod
    def iter_chunks(self) -> Iterator[str]:
        """Yield text chunks lazily, front-to-back"""
