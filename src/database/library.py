import duckdb
from typing import Iterable, Sequence
from src.entities.book import Book
from src.entities.subject import Subject


class Library:
    def __init__(self, path: str = "data/library.duckdb"):
        self.conn = duckdb.connect(path)

    # ---------- Books ----------

    def add_book(self, book: Book) -> None:
        row = self.conn.execute(
            "INSERT INTO books (title) VALUES (?) RETURNING id",
            [book.title],
        ).fetchone()
        if row is None:
            raise RuntimeError("Failed to insert book; no id returned")
        book.book_id = row[0]

    # ---------- TOC ----------

    def add_toc_entries(
        self,
        book_id: int,
        entries: Iterable[tuple[str, str]],
    ) -> None:
        self.conn.executemany(
            """
            INSERT INTO toc_entries (book_id, heading, page_number)
            VALUES (?, ?, ?)
            """,
            ((book_id, h, p) for h, p in entries),
        )

    def get_toc_entries(
        self,
        book_id: int,
    ) -> Sequence[tuple[int, str, str]]:
        return self.conn.execute(
            """
            SELECT id, heading, page_number
            FROM toc_entries
            WHERE book_id = ?
            """,
            [book_id],
        ).fetchall()

    # ---------- Subjects ----------

    def get_or_create_subject(self, name: str) -> Subject:
        row = self.conn.execute(
            "SELECT id, name FROM subjects WHERE name = ?",
            [name],
        ).fetchone()

        if row:
            return Subject(*row)

        row = self.conn.execute(
            """
            INSERT INTO subjects (name)
            VALUES (?) RETURNING id, name
            """,
            [name],
        ).fetchone()

        return Subject(*row)

    def link_heading_to_subject(
        self,
        toc_entry_id: int,
        subject_id: int,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO toc_subjects (toc_entry_id, subject_id)
            VALUES (?, ?)
            """,
            [toc_entry_id, subject_id],
        )

    def list_subjects(self) -> Sequence[Subject]:
        return [
            Subject(*row)
            for row in self.conn.execute(
                "SELECT id, name FROM subjects"
            ).fetchall()
        ]

    def get_subject_by_name(self, name: str) -> Subject | None:
        row = self.conn.execute(
            "SELECT id, name FROM subjects WHERE name = ?",
            [name],
        ).fetchone()
        return Subject(*row) if row else None

    # ---------- Reading Sections ----------

    def get_reading_sections_for_subject(
        self,
        subject_id: int,
    ) -> list[tuple[str, str, str]]:
        return self.conn.execute(
            """
            SELECT
                b.title,
                t.heading,
                t.page_number
            FROM toc_subjects ts
            JOIN toc_entries t ON ts.toc_entry_id = t.id
            JOIN books b ON t.book_id = b.id
            WHERE ts.subject_id = ?
            """,
            [subject_id],
        ).fetchall()
