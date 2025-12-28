import json
from typing import Sequence
from librarian.llm.agent import Agent
from librarian.llm.config import USER_QUERY_TO_SUBJECTS_PROMPT

_agent = Agent()


def infer_user_subjects(
    query: str,
    available_subjects: Sequence[str],
) -> dict:
    response = _agent.call(
        USER_QUERY_TO_SUBJECTS_PROMPT.format(
            query=query,
            subjects=", ".join(available_subjects),
        )
    )
    return json.loads(response)
