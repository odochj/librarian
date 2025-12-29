from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
GENERATE_ENDPOINT = os.getenv("ENDPOINT")

MODEL = os.getenv("MODEL")
TIMEOUT = 60  # seconds

# Conservative settings for classification/extraction
TEMPERATURE = 0.0
TOP_P = 0.9


# An incomplete list of canoncial subjects to guide llm responses
SUBJECTS = [
    "Data Analysis",
    "Machine Learning",
    "Data Warehousing",
    "Database Systems",
    "CI/CD Pipelines",
    "Cloud Computing",
    "Distributed Systems",
    "Microservices",
    "Networking",
    "Infrastructure as Code",
    "Cybersecurity",
    "Terraform",
    "Kubernetes",
    "Docker",
    "Big Data"
]

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
- Return a comma separated list as per the example below
section_title, page_number
title one, 10
title two, 25
- Do not add explanations

TEXT:
{chunk}
"""

SUBJECT_EXTRACTION_PROMPT = """
You are extracting subjects from the contents of a technical or engineering book.
The output will become a reference to allow for subject-based search and recommendation.

Intsructions:
- You will receive two inputs:
  - The section heading of a book, as taken from the table of contents
  - An existing list of canonical subjects
- Analyze the heading to infer relevant subjects
- Reuse subjects from the canonical list where possible
- Return a comma separated list of subjects
- Do not add explanations

TABLE:
{heading}
CANONICAL SUBJECTS:
{subjects}
"""

USER_QUERY_TO_SUBJECTS_PROMPT = """
You are a librarian mapping a user's learning goal to available subjects.

USER GOAL:
{query}

AVAILABLE SUBJECTS:
{subjects}

Return STRICT JSON:

{
  "matched_subjects": [string],
  "missing_subjects": [string]
}
"""