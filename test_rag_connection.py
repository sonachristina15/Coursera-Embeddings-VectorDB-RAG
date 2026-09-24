import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

cur.execute("""
    SELECT ts.id, ts.text
    FROM transcript_segments ts
    JOIN transcripts t ON ts.transcript_id = t.id
    JOIN assets a ON t.id = a.id
    WHERE a.rag_enabled = true
      AND ts.text IS NOT NULL
    LIMIT 1;
""")

row = cur.fetchone()

print("Segment ID:", row[0])
print("Text:", row[1])

cur.close()
conn.close()