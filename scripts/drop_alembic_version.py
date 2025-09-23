import os
import psycopg2

url = os.environ["DATABASE_URL"]
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("""
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'alembic_version') THEN
        EXECUTE 'DROP TABLE alembic_version CASCADE';
    END IF;
END$$;
""")
conn.commit()
cur.close()
conn.close()
print("Dropped alembic_version table if it existed.")
