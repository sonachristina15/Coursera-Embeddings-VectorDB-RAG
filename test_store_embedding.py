import os
import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to PostgreSQL
conn = psycopg.connect(
    
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# Get ONE RAG-ready transcript segment
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

segment_id = row[0]
text = row[1]

print("Segment ID:", segment_id)
print("Text:", text)

# Generate embedding
embedding = model.encode(text).tolist()

print("Embedding dimension:", len(embedding))

# Store embedding
cur.execute("""
    UPDATE transcript_segments
    SET embedding = %s
    WHERE id = %s;
""", (embedding, segment_id))

conn.commit()

print("Embedding stored successfully!")

cur.close()
conn.close()