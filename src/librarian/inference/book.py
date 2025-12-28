from typing import Iterable
from librarian.llm.agent import Agent
from librarian.llm.config import (
    TOC_DETECTION_PROMPT,
    TOC_EXTRACTION_PROMPT,
)

_agent = Agent()


def is_table_of_contents(text: str) -> bool:
    response = _agent.call(
        TOC_DETECTION_PROMPT.format(chunk=text)
    )
    return response.strip().upper() == "YES"


def extract_toc_entries(text: str) -> Iterable[tuple[str, str]]:
    csv = _agent.call(
        TOC_EXTRACTION_PROMPT.format(chunk=text)
    )
    for line in csv.splitlines():
        if not line.strip():
            continue
        h, p = line.split(",", 1)
        yield h.strip(), p.strip()
