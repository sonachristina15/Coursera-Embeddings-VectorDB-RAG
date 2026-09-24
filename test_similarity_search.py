import os
import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Our search question
query = "What is data science?"

# Convert query into a 384-dimensional vector
query_embedding = model.encode(query).tolist()

print("Query:", query)
print("Query embedding dimension:", len(query_embedding))

# Connect to PostgreSQL
conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

# Find the closest stored embedding
cur.execute("""
    SELECT
        ts.id,
        ts.text,
        1 - (ts.embedding <=> %s::vector) AS similarity
    FROM transcript_segments ts
    JOIN transcripts t ON ts.transcript_id = t.id
    JOIN assets a ON t.id = a.id
    WHERE a.rag_enabled = true
      AND ts.embedding IS NOT NULL
    ORDER BY ts.embedding <=> %s::vector
    LIMIT 5;
""", (query_embedding, query_embedding))

results = cur.fetchall()

print("\nTop results:\n")

for i, row in enumerate(results, 1):
    print(f"Result {i}")
    print("Similarity:", row[2])
    print("Text:", row[1])
    print()

cur.close()
conn.close()