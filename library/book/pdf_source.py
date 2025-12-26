import pdfplumber
from pathlib import Path
from text_source import TextSource

class PDFTextSource(TextSource):
    def __init__(self, path: Path, max_pages: int = 30):
        self.path = path
        self.max_pages = max_pages

    def iter_lines(self):
        with pdfplumber.open(self.path) as pdf:
            for page_number, page in enumerate(pdf.pages[:self.max_pages], start=1):
                text = page.extract_text()
                if not text:
                    continue

                for line in text.splitlines():
                    yield line
