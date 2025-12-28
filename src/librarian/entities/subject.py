from dataclasses import dataclass


@dataclass(frozen=True)
class Subject:
    subject_id: int
    name: str
