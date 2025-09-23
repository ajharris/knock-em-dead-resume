import os
import psycopg2

url = os.environ["DATABASE_URL"]
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("ALTER TABLE alembic_version ALTER COLUMN version_num TYPE VARCHAR(128);")
conn.commit()
cur.close()
conn.close()
print("alembic_version.version_num column updated to VARCHAR(128)")
