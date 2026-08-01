This folder contains SQL migrations for running the librarian schema in PostgreSQL.

Run the example migration script to copy data from the existing DuckDB to Postgres (small datasets):

  POSTGRES_URL=postgresql://user:pass@host:5432/db \
    python src/scripts/duckdb_to_postgres.py

Files:
- migrations/001_create_tables.sql  — CREATE TABLE statements matching library.schema
- src/scripts/duckdb_to_postgres.py — minimal example script to copy tables from the DuckDB file into Postgres using COPY.

Notes:
- This is an example migration for small datasets. For larger datasets adapt the script to chunk and validate.
- The existing Library class continues to use DuckDB internally. To fully switch to Postgres, add a configuration option (POSTGRES_URL) and a Postgres-backed Repository implementation that mirrors Library methods.
