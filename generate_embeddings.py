import os
import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()


MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32


def main():
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

    cur = conn.cursor()

    # ---------------------------------------------------------
    # 1. Transcript segments
    # ---------------------------------------------------------
    cur.execute("""
        SELECT ts.id, ts.text
        FROM transcript_segments ts
        JOIN transcripts t ON ts.transcript_id = t.id
        JOIN assets a ON t.id = a.id
        WHERE a.rag_enabled = true
          AND ts.text IS NOT NULL
          AND ts.embedding IS NULL
        ORDER BY ts.id;
    """)

    transcript_rows = cur.fetchall()

    print(f"Transcript segments needing embeddings: {len(transcript_rows)}")

    for start in range(0, len(transcript_rows), BATCH_SIZE):
        batch = transcript_rows[start:start + BATCH_SIZE]

        texts = [row[1] for row in batch]

        embeddings = model.encode(
            texts,
            batch_size=BATCH_SIZE,
            show_progress_bar=False
        )

        for (segment_id, _), embedding in zip(batch, embeddings):
            cur.execute("""
                UPDATE transcript_segments
                SET embedding = %s
                WHERE id = %s;
            """, (embedding.tolist(), segment_id))

        conn.commit()

        print(
            f"Transcript progress: "
            f"{min(start + BATCH_SIZE, len(transcript_rows))}"
            f"/{len(transcript_rows)}"
        )

    # ---------------------------------------------------------
    # 2. HTML readings
    # ---------------------------------------------------------
    cur.execute("""
        SELECT r.id, r.extracted_text
        FROM readings r
        JOIN assets a ON r.id = a.id
        WHERE a.rag_enabled = true
          AND r.extracted_text IS NOT NULL
          AND r.embedding IS NULL
        ORDER BY r.id;
    """)

    reading_rows = cur.fetchall()

    print(f"Readings needing embeddings: {len(reading_rows)}")

    for start in range(0, len(reading_rows), BATCH_SIZE):
        batch = reading_rows[start:start + BATCH_SIZE]

        texts = [row[1] for row in batch]

        embeddings = model.encode(
            texts,
            batch_size=BATCH_SIZE,
            show_progress_bar=False
        )

        for (reading_id, _), embedding in zip(batch, embeddings):
            cur.execute("""
                UPDATE readings
                SET embedding = %s
                WHERE id = %s;
            """, (embedding.tolist(), reading_id))

        conn.commit()

        print(
            f"Reading progress: "
            f"{min(start + BATCH_SIZE, len(reading_rows))}"
            f"/{len(reading_rows)}"
        )

    cur.close()
    conn.close()

    print("\nEmbedding generation completed successfully.")


if __name__ == "__main__":
    main()