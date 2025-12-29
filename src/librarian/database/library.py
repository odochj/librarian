import duckdb
from typing import Iterable, Sequence, Optional
from librarian.entities.book import Book
from librarian.entities.subject import Subject


class Library:
    def __init__(self, path: str = "src/librarian/database/library.duckdb"):
        self.conn = duckdb.connect(path)

    # ---------- Books ----------

    def initialise_schema(self) -> None:
        with open("src/librarian/database/schema.sql", "r") as f:
            schema_sql = f.read()
        self.conn.execute(schema_sql)
    
    def add_book(self, book: Book) -> None:
        row = self.conn.execute(
            "INSERT INTO book (title, path) VALUES (?, ?) RETURNING id",
            [book.title, str(book.path)],
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
            INSERT INTO toc_entry (book_id, heading, page_number)
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
            FROM toc_entry
            WHERE book_id = ?
            """,
            [book_id],
        ).fetchall()

    # ---------- Subjects ----------

    def get_or_create_subject(self, name: str) -> Optional[Subject]:
        row = self.conn.execute(
            "SELECT id, name FROM subject WHERE name = ?",
            [name],
        ).fetchone()

        if row:
            return Subject(*row)

        row = self.conn.execute(
            """
            INSERT INTO subject (name)
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
            INSERT INTO heading_subject (toc_entry_id, subject_id)
            VALUES (?, ?)
            """,
            [toc_entry_id, subject_id],
        )

    def list_subjects(self) -> Sequence[Subject]:
        return [
            Subject(*row)
            for row in self.conn.execute(
                "SELECT id, name FROM subject"
            ).fetchall()
        ]

    def get_subject_by_name(self, name: str) -> Subject | None:
        row = self.conn.execute(
            "SELECT id, name FROM subject WHERE name = ?",
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
            FROM heading_subject ts
            JOIN toc_entry t ON ts.toc_entry_id = t.id
            JOIN book b ON t.book_id = b.id
            WHERE ts.subject_id = ?
            """,
            [subject_id],
        ).fetchall()
