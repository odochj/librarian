from typing import Sequence
from librarian.llm.agent import Agent
from librarian.llm.config import CONSOLIDATE_RECOMMENDATIONS_PROMPT

_agent = Agent()

def consolidate_recommendations(
    query: str,
    plan: str,
    subjects: Sequence[str]
) -> str:
    response = _agent.call(
        CONSOLIDATE_RECOMMENDATIONS_PROMPT.format(
            # query=query,
            plan=plan
            # subjects=subjects
        )
    )
    return response
