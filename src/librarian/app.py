from collections import defaultdict
from typing import Sequence
from librarian.entities.book import Book
from librarian.database.library import Library
from librarian.inference.book import (
    is_table_of_contents,
    extract_toc_entries,
)
from librarian.inference.subject import infer_subjects
from librarian.inference.user import infer_user_subjects


WORDS_PER_PAGE = 400  # conservative technical average


class Librarian:
    def __init__(self, library: Library):
        self.library = library

    # ---------- Ingestion ----------

    def ingest_book(self, book: Book) -> None:
        self.library.add_book(book)

        if book.book_id is None:
            raise RuntimeError("Book persistence failed")

        for chunk in book.source.iter_lines():
            if is_table_of_contents(chunk):
                self.library.add_toc_entries(
                    book.book_id,
                    extract_toc_entries(chunk),
                )
                break

        self._ingest_subjects(book.book_id)

    def _ingest_subjects(self, book_id: int) -> None:
        for toc_id, heading, _ in self.library.get_toc_entries(book_id):
            for name in infer_subjects(heading):
                subject = self.library.get_or_create_subject(name)
                self.library.link_heading_to_subject(
                    toc_id,
                    subject.subject_id,
                )

    # ---------- User-facing ----------

    def recommend_curriculum(self, query: str) -> str:
        subjects = self.library.list_subjects()
        subject_names = [s.name for s in subjects]

        interpretation = infer_user_subjects(query, subject_names)
        matched = interpretation.get("matched", [])
        missing = interpretation.get("missing", [])

        return self._render_plan(matched, missing)

    # ---------- Helpers ----------

    def _render_plan(
        self,
        matched_subjects: Sequence[str],
        missing_subjects: Sequence[str],
    ) -> str:
        lines: list[str] = ["# Targeted Reading Plan\n"]

        for subject_name in matched_subjects:
            subject = self.library.get_subject_by_name(subject_name)
            if not subject:
                continue

            raw = self.library.get_reading_sections_for_subject(
                subject.subject_id
            )
            grouped = defaultdict(list)

            for book, heading, page in raw:
                grouped[book].append((heading, int(page)))

            lines.append(f"## {subject.name}\n")

            for book, sections in grouped.items():
                sections.sort(key=lambda x: x[1])
                ranges = self._merge_pages(sections)

                lines.append(f"**{book}**")
                for start, end, headings in ranges:
                    minutes = self._estimate_time(start, end)
                    label = f"p. {start}" if start == end else f"pp. {start}–{end}"
                    lines.append(
                        f"- {label} (~{minutes} min): {', '.join(headings)}"
                    )
                lines.append("")

        if missing_subjects:
            lines.append("\n# Topics Not Covered\n")
            for name in missing_subjects:
                lines.append(f"- {name}")

        return "\n".join(lines)

    def _merge_pages(
        self,
        sections: list[tuple[str, int]],
    ) -> list[tuple[int, int, list[str]]]:
        merged = []
        current_start = current_end = sections[0][1]
        headings = [sections[0][0]]

        for heading, page in sections[1:]:
            if page == current_end + 1:
                current_end = page
                headings.append(heading)
            else:
                merged.append((current_start, current_end, headings))
                current_start = current_end = page
                headings = [heading]

        merged.append((current_start, current_end, headings))
        return merged

    def _estimate_time(self, start: int, end: int) -> int:
        pages = end - start + 1
        return max(5, (pages * WORDS_PER_PAGE) // 250)
