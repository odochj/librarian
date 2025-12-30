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
        # Try to find the book
        row = self.conn.execute(
            """
            SELECT id
            FROM book
            WHERE path = ?
            """,
            [str(book.path)],
        ).fetchone()

        # If it already exists, we’re done
        if row:
            book.book_id = row[0]
            return

        # Otherwise, insert it
        row = self.conn.execute(
            """
            INSERT INTO book (title, path)
            VALUES (?, ?)
            RETURNING id
            """,
            [book.title, str(book.path)],
        ).fetchone()

        if row is None:
            raise RuntimeError("Failed to insert book")

        book.book_id = row[0]

    def get_book_state(self, book_id: int) -> dict:
        row = self.conn.execute(
            """
            SELECT toc_ingested, subjects_ingested
            FROM book
            WHERE id = ?
            """,
            [book_id],
        ).fetchone()

        if row is None:
            # Book not found
            return {
                "toc_ingested": False,
                "subjects_ingested": False
            }

        return {
            "toc_ingested": bool(row[0]),
            "subjects_ingested": bool(row[1]),
        }
    
    def mark_toc_ingested(self, book_id: int) -> None:
        self.conn.execute(
            "UPDATE book SET toc_ingested = TRUE WHERE id = ?",
            [book_id],
        )

    def mark_subjects_ingested(self, book_id: int) -> None:
        self.conn.execute(
            "UPDATE book SET subjects_ingested = TRUE WHERE id = ?",
            [book_id],
        )



    # ---------- TOC ----------

    def add_toc_entries(
        self,
        book_id: int | None,
        entries: Iterable[tuple[str, str]],
    ) -> None:
        entries_list = list(entries)
        if not entries_list:
            print(" WARNING: No TOC entries to add")
            return

        params = [(book_id, h, p) for h, p in entries_list]
        self.conn.executemany(
            """
            INSERT INTO toc_entry (book_id, heading, page_number)
            VALUES (?, ?, ?)
            """,
            params,
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
    def verify_subject_extraction_by_book(
        self,
        book : Book,
    ) -> bool:
        row = self.conn.execute(
            """
            SELECT COUNT(*)
            FROM heading_subject hs
            JOIN toc_entry te ON hs.toc_entry_id = te.id
            WHERE te.book_id = ?
            """,
            [book.book_id],
        ).fetchone()
        return row[0] > 0 if row else False 

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
