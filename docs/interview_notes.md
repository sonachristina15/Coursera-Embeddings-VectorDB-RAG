# Interview Notes — PostgreSQL + pgvector RAG

## 1. What was my responsibility in the project?

My responsibility was the AI/RAG Vector Database portion of the project.

The upstream team prepared and validated the course data and loaded the RAG-ready data into PostgreSQL.

My work started from that PostgreSQL data and covered:

- Embedding generation
- Vector storage
- pgvector configuration
- Vector indexing
- Semantic similarity search
- Retrieval validation

---

## 2. What is RAG?

RAG stands for Retrieval-Augmented Generation.

Instead of asking an LLM to answer only from its pretrained knowledge, RAG first retrieves relevant information from an external knowledge source and provides that information to the LLM as context.

The basic flow is:

User Query
↓
Query Embedding
↓
Vector Similarity Search
↓
Relevant Documents
↓
Retrieved Context
↓
LLM
↓
Generated Answer

My contribution mainly covered the embedding and retrieval/vector database stages.

---

## 3. What data did I start with?

The preprocessing layer prepared RAG-ready data in PostgreSQL.

The relevant sources were:

- SRT transcript segments
- TXT chunks
- HTML reading content

Only records associated with RAG-enabled assets were considered for retrieval.

The database contained:

- 3,382 transcript segments
- 19 RAG-eligible reading records

Therefore, the embedding layer had:

3,382 + 19 = 3,401 records

to embed.

---

## 4. Why did I use embeddings?

Normal keyword search looks for matching words.

Semantic search instead represents text as numerical vectors.

For example, these two sentences may use different words but have similar meanings:

"What is data science?"

"Data science is the study of data."

Their vector representations can be close to each other in vector space.

This allows semantic similarity search.

---

## 5. Which embedding model did I use?

I used:

`all-MiniLM-L6-v2`

It is a Sentence Transformers model designed for generating sentence/text embeddings.

The model produces a vector with:

`384 dimensions`

Therefore, the PostgreSQL vector columns were defined as:

`vector(384)`

---

## 6. Why must the vector dimension match?

The PostgreSQL vector column has a fixed dimension.

For example:

`vector(384)`

means every stored vector must contain exactly 384 values.

Since `all-MiniLM-L6-v2` produces 384-dimensional vectors, the model output matches the database column.

If the dimensions did not match, the vector could not be stored correctly.

---

## 7. How did I store embeddings?

I used PostgreSQL with the `pgvector` extension.

The embedding columns were added to:

- `transcript_segments`
- `readings`

The column type was:

`vector(384)`

The text is converted into a vector by the embedding model, and that vector is stored in PostgreSQL.

---

## 8. What is pgvector?

pgvector is a PostgreSQL extension that adds support for vector data and vector similarity search.

Instead of using a separate vector database, this project stores the embeddings directly inside PostgreSQL.

This allows the existing relational metadata and vector data to be queried together.

---

## 9. What is cosine similarity?

Cosine similarity measures how similar two vectors are based on their direction.

For semantic search, a query embedding is compared with stored document embeddings.

A higher cosine similarity generally indicates that the vectors are more semantically similar.

In pgvector, I used cosine distance with:

`<=>`

Similarity was calculated as:

`1 - cosine_distance`

---

## 10. What is the `<=>` operator?

In pgvector, `<=>` is the cosine distance operator when used with the cosine distance operator class.

The query orders the records by vector distance.

The closest vectors are returned first.

Conceptually:

Query vector
↓
Compare against stored vectors
↓
Calculate cosine distance
↓
Order by distance
↓
Return top-K results

---

## 11. Why did I use HNSW?

HNSW stands for Hierarchical Navigable Small World.

It is an approximate nearest-neighbor indexing method.

Without an appropriate vector index, similarity search can require comparing a query against many stored vectors.

An HNSW index helps make nearest-neighbor searches more efficient as the vector collection grows.

I created HNSW indexes using cosine distance:

`vector_cosine_ops`

for both transcript and reading embeddings.

---

## 12. What does Top-K retrieval mean?

Top-K retrieval means returning the K most relevant results.

For example:

`LIMIT 5`

returns the five closest matching records.

In my similarity-search test, I used Top-5 retrieval.

---

## 13. How did I test the retrieval system?

I used the query:

"What is data science?"

The query was converted into an embedding using the same:

`all-MiniLM-L6-v2`

model.

The query vector was then compared against stored transcript embeddings using pgvector.

The top results included:

- "But what is Data Science?"
- "Data science is the study of data."
- "Let's begin, so what really is data science?"

This demonstrated that the system was retrieving semantically relevant text rather than simply matching exact keywords.

---

## 14. How did I verify that all embeddings were generated?

I created a verification script that counted:

- Total RAG-eligible transcript segments
- Transcript segments containing embeddings
- Total RAG-eligible readings
- Reading records containing embeddings

The final verification was:

Transcript total: 3382
Transcript embedded: 3382

Reading total: 19
Reading embedded: 19

Total embedded: 3401

Therefore:

`3,401 / 3,401`

RAG-eligible records had embeddings.

---

## 15. What is the difference between embedding and retrieval?

Embedding and retrieval are two different stages.

### Embedding

Converts text into a numerical vector.

Example:

Text
↓
Embedding model
↓
384-dimensional vector

### Retrieval

Uses a query vector to find the most similar stored vectors.

Example:

User query
↓
Query embedding
↓
Vector similarity search
↓
Top-K relevant text

So generating embeddings alone does not mean that retrieval has happened.

---

## 16. What is the difference between retrieval and generation?

Retrieval finds relevant information.

Generation uses an LLM to produce the final natural-language response using that retrieved information.

For example:

Retrieval:

"Data science is the study of data."

Generation:

"Data science is a field that focuses on extracting useful insights from data."

My implementation primarily covers the embedding and retrieval/vector database portion.

---

## 17. Why did I use the same embedding model for documents and queries?

The query and stored documents need to exist in the same vector space.

Therefore, the same embedding model is used to:

1. Generate document embeddings
2. Generate the user's query embedding

This makes the vector comparison meaningful.

---

## 18. Why did I filter using `rag_enabled = true`?

The database contains both RAG-eligible and administrative/excluded assets.

The RAG pipeline should only retrieve content that is marked as eligible.

Therefore, the retrieval queries filter using:

`a.rag_enabled = true`

This prevents excluded content from entering the retrieval results.

---

## 19. What is the role of metadata?

The vector is useful for semantic similarity, but the relational database contains additional information such as:

- Course
- Module
- Lesson
- Asset
- Transcript
- Timestamp

This metadata can later be used to filter or enrich retrieved results.

This is one advantage of storing vectors inside PostgreSQL alongside the existing relational data.

---

## 20. What are the main technologies I used?

### Python

Used for:

- Connecting to PostgreSQL
- Loading the embedding model
- Generating embeddings
- Running retrieval tests
- Validation

### Sentence Transformers

Used to generate text embeddings.

### PostgreSQL

Used as the main relational database.

### pgvector

Used for vector storage and similarity search.

### HNSW

Used for approximate nearest-neighbor vector indexing.

### python-dotenv

Used to load database configuration from `.env`.

---

## 21. How did I handle database credentials?

Database credentials are stored in a local `.env` file.

Python loads them using:

`python-dotenv`

The `.env` file is included in `.gitignore`.

Therefore, credentials are not committed to GitHub.

A `.env.example` file is provided as a configuration template.

---

## 22. What happens when a new document is added?

Conceptually:

New text
↓
Generate embedding
↓
Store text + embedding
↓
Vector index makes it searchable
↓
Future queries can retrieve it

The important point is that the document must be embedded before vector similarity search can retrieve it.

---

## 23. What happens when a user asks a question?

For example:

"What is data science?"

The RAG retrieval process is:

1. Receive the user query.
2. Convert the query into a 384-dimensional embedding.
3. Compare the query vector with stored vectors.
4. Calculate cosine distance.
5. Order results by similarity.
6. Select the Top-K relevant records.
7. Pass the retrieved context to the generation layer.

---

## 24. What did I actually verify?

I verified the complete vector retrieval foundation:

- PostgreSQL connection
- RAG-ready transcript access
- Embedding model loading
- 384-dimensional embedding generation
- Embedding storage
- Embedding counts
- pgvector similarity search
- Top-K retrieval
- HNSW indexes

The final embedding verification showed:

`3,401 / 3,401`

RAG-eligible records embedded successfully.

---

## 25. Simple interview explanation

If an interviewer asks:

"Explain your contribution to the project."

I can answer:

> "My contribution was the AI/RAG vector database layer. The preprocessing team prepared the RAG-ready data and loaded it into PostgreSQL. I started from that data and generated embeddings using the `all-MiniLM-L6-v2` Sentence Transformer model. Since the model produces 384-dimensional vectors, I stored them in PostgreSQL using the pgvector extension with `vector(384)` columns. I then created HNSW indexes using cosine distance and implemented similarity search to retrieve the most relevant transcript segments for a user query. I also validated the pipeline and confirmed that all 3,401 RAG-eligible records had embeddings."

---

## 26. One-line project summary

> Built the embedding and vector retrieval layer for a PostgreSQL-based RAG pipeline using Sentence Transformers, pgvector, cosine similarity, and HNSW indexing.