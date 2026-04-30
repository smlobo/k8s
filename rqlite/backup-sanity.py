#!/usr/bin/env python3

import json
import sqlite3
import sys
from pathlib import Path


DEFAULT_BACKUP_NAME = "rqlite.backup.sqlite3"


def open_readonly(db_file: Path) -> sqlite3.Connection:
    # SQLite read-only mode prevents accidental writes even if a statement tries.
    db_uri = f"file:{db_file.expanduser().resolve()}?mode=ro"
    conn = sqlite3.connect(db_uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print(f"Usage: {sys.argv[0]} <queries.json> [db_file]", file=sys.stderr)
        sys.exit(1)

    json_file = Path(sys.argv[1])
    db_file = Path.home() / DEFAULT_BACKUP_NAME
    if len(sys.argv) == 3:
        db_file = Path(sys.argv[2])

    with json_file.open() as f:
        statements = json.load(f)

    if not isinstance(statements, list):
        raise ValueError("JSON must contain an array of SQL statements")

    conn = open_readonly(db_file)

    try:
        cur = conn.cursor()

        for i, sql in enumerate(statements, start=1):
            if not isinstance(sql, str):
                raise ValueError(f"Item {i} is not a string")

            # print(f"\n[{i}] Running: {sql}")
            cur.execute(sql)

            if cur.description is not None:
                rows = cur.fetchall()
                for row in rows:
                    print(dict(row))
                # print(f"Returned {len(rows)} row(s)")
            # else:
            #     print(f"Done. {cur.rowcount} row(s) affected")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
