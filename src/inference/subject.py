from typing import Sequence
from src.llm.agent import Agent
from src.llm.config import SUBJECT_EXTRACTION_PROMPT, SUBJECTS

_agent = Agent()


def infer_subjects(heading: str) -> Sequence[str]:
    response = _agent.call(
        SUBJECT_EXTRACTION_PROMPT.format(
            heading=heading,
            subjects=", ".join(SUBJECTS),
        )
    )
    return [s.strip() for s in response.split(",") if s.strip()]
