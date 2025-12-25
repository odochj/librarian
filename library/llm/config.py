BASE_URL = "http://localhost:11434"
GENERATE_ENDPOINT = "/api/generate"

MODEL = "llama3"
TIMEOUT = 60  # seconds

# Conservative settings for classification/extraction
TEMPERATURE = 0.0
TOP_P = 0.9


TOC_DETECTION_PROMPT = """
You are analyzing a non-fiction technical or engineering book.

Determine whether the text below is part of a TABLE OF CONTENTS.

A table of contents usually contains:
- Chapter or section titles
- Section numbering
- Page numbers
- Little or no prose

Ignore OCR errors.

Answer with ONLY:
YES or NO

TEXT:
{chunk}
"""


TOC_EXTRACTION_PROMPT = """
You are extracting topics from a table of contents
of a technical or engineering book.

Instructions:
- Extract page numbers and chapter or section titles
- Ignore OCR artifacts
- Preserve original wording where possible
- Return a comma separated list in the format:
  - section_title, page_number
- Do not add explanations

TEXT:
{chunk}
"""
