from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Subject:
    subject_id: int
    name: str
