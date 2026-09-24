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

# Transcript embedding count
cur.execute("""
    SELECT
        COUNT(*) AS total,
        COUNT(embedding) AS embedded
    FROM transcript_segments ts
    JOIN transcripts t ON ts.transcript_id = t.id
    JOIN assets a ON t.id = a.id
    WHERE a.rag_enabled = true
      AND ts.text IS NOT NULL;
""")

transcript_total, transcript_embedded = cur.fetchone()

# Reading embedding count
cur.execute("""
    SELECT
        COUNT(*) AS total,
        COUNT(embedding) AS embedded
    FROM readings r
    JOIN assets a ON r.id = a.id
    WHERE a.rag_enabled = true
      AND r.extracted_text IS NOT NULL;
""")

reading_total, reading_embedded = cur.fetchone()

print("Transcript total:", transcript_total)
print("Transcript embedded:", transcript_embedded)

print("Reading total:", reading_total)
print("Reading embedded:", reading_embedded)

print("Total embedded:", transcript_embedded + reading_embedded)

cur.close()
conn.close()