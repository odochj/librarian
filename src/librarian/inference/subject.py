from typing import Sequence
from librarian.llm.agent import Agent
from librarian.llm.config import SUBJECT_EXTRACTION_PROMPT, SUBJECTS

_agent = Agent()


def infer_subjects(heading: str) -> Sequence[str]:
    response = _agent.call(
        SUBJECT_EXTRACTION_PROMPT.format(
            heading=heading,
            subjects=", ".join(SUBJECTS),
        )
    )
    print(response)
    return [s.strip() for s in response.split(",") if s.strip()]
