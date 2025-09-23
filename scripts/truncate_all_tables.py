#!/usr/bin/env python3
"""
Truncate all user tables in the database before running tests.
"""
from backend.app import database, models
from sqlalchemy import text

def truncate_all_tables():
    engine = database.engine
    with engine.connect() as conn:
        meta = models.Base.metadata
        for table in reversed(meta.sorted_tables):
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))
        conn.commit()

if __name__ == "__main__":
    truncate_all_tables()
    print("All tables truncated.")
