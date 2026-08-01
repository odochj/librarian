"""Simple migration helper: dump DuckDB tables to Postgres.

Usage:
  POSTGRES_URL=postgresql://user:pass@host:5432/db python src/scripts/duckdb_to_postgres.py

Notes: This script is intentionally minimal — suitable for small datasets and as an example for the PR.
"""

import os
import duckdb
import psycopg2
import io

DUCKDB_PATH = os.environ.get("LIBRARY_DUCKDB_PATH", "src/librarian/database/library.duckdb")
PG_URL = os.environ.get("POSTGRES_URL")

if PG_URL is None:
    raise SystemExit("Please set POSTGRES_URL environment variable")

conn_duck = duckdb.connect(DUCKDB_PATH)
conn_pg = psycopg2.connect(PG_URL)
cur_pg = conn_pg.cursor()

# List tables we want to copy
tables = [
    "book",
    "toc_entry",
    "subject",
    "heading_subject",
    "query_cache",
]

for t in tables:
    print(f"Migrating table: {t}")
    # Read all rows from duckdb
    df = conn_duck.execute(f"SELECT * FROM {t}").fetchdf()
    if df.shape[0] == 0:
        print("  No rows — skipping")
        continue

    # Create a CSV in memory
    buf = io.StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)

    # Build COPY command
    copy_sql = f"COPY {t} FROM STDIN WITH (FORMAT csv)"
    try:
        cur_pg.copy_expert(copy_sql, buf)
        conn_pg.commit()
        print(f"  Copied {df.shape[0]} rows into {t}")
    except Exception as e:
        conn_pg.rollback()
        print(f"  Failed to copy {t}: {e}")

cur_pg.close()
conn_pg.close()
conn_duck.close()
print("Migration complete — validate counts in Postgres")
