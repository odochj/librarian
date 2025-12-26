from PIL import Image
import pytesseract
from pathlib import Path
from text_source import TextSource

class ImageSource(TextSource):
    def __init__(self, image_paths: list[Path]):
        self.image_paths = image_paths

    def iter_lines(self):
        for path in self.image_paths:
            image = Image.open(path)
            text = pytesseract.image_to_string(image)

            for line in text.splitlines():
                yield line
