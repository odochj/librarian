-- books
CREATE SEQUENCE IF NOT EXISTS book_id_seq;
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL('book_id_seq'),
    title TEXT,
    path TEXT
);

-- table of contents entries
CREATE SEQUENCE IF NOT EXISTS toc_entry_id_seq;
CREATE TABLE IF NOT EXISTS toc_entry (
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL('toc_entry_id_seq'),
    book_id INTEGER,
    heading TEXT,
    page_number TEXT
);

-- canonical subjects
CREATE SEQUENCE IF NOT EXISTS subject_id_seq;
CREATE TABLE IF NOT EXISTS subject (
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL('subject_id_seq'),
    name TEXT UNIQUE
);

-- many-to-many relationship
CREATE SEQUENCE IF NOT EXISTS heading_subject_id_seq;
CREATE TABLE IF NOT EXISTS heading_subject (
    id INTEGER PRIMARY KEY DEFAULT NEXTVAL('heading_subject_id_seq'),
    toc_entry_id INTEGER,
    subject_id INTEGER
);

-- cache for user intent → subjects
CREATE TABLE IF NOT EXISTS query_cache (
    query TEXT PRIMARY KEY,
    matched_subjects TEXT,
    missing_subjects TEXT
);
