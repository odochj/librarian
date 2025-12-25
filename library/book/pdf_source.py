import pdfplumber
from text_source import TextSource

class PDFTextSource(TextSource):
    def __init__(self, pdf_path: str, max_pages=30, chunk_size=2000):
        self.pdf_path = pdf_path
        self.max_pages = max_pages
        self.chunk_size = chunk_size

    def iter_chunks(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            buffer = ""
            for page in pdf.pages[:self.max_pages]:
                text = page.extract_text()
                if not text:
                    continue

                buffer += text + "\n"

                while len(buffer) >= self.chunk_size:
                    yield buffer[:self.chunk_size]
                    buffer = buffer[self.chunk_size:]

            if buffer:
                yield buffer
