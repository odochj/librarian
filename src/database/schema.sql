-- books
CREATE TABLE book (
    id INTEGER PRIMARY KEY,
    title TEXT,
    path TEXT
);

-- table of contents entries
CREATE TABLE toc_entry (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    heading TEXT,
    page_number TEXT
);

-- canonical subjects
CREATE TABLE subject (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

-- many-to-many relationship
CREATE TABLE heading_subject (
    toc_entry_id INTEGER,
    subject_id INTEGER
);

-- cache for user intent → subjects
CREATE TABLE query_cache (
    query TEXT PRIMARY KEY,
    matched_subjects TEXT,
    missing_subjects TEXT
);
