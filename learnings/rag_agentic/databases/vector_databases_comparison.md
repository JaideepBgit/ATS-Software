# Vector Databases for RAG Systems

A comprehensive comparison of vector databases for building RAG (Retrieval Augmented Generation) systems and feedback collection.

## Quick Recommendation

**For ATS Feedback System: Use ChromaDB**

Start with ChromaDB for development and small-medium production. Migrate to Pinecone only if you need massive scale (millions of users).

## Detailed Comparison

### 1. ChromaDB ⭐ (Recommended)

**Best for:** Development, small-medium production, LLM applications

**Pros:**
- Simplest setup - 3 lines of code
- Embedded mode (no separate server)
- Persistent storage built-in
- Designed specifically for LLM/RAG use cases
- Metadata filtering (filter by rating, date, user, etc.)
- Free and open source
- Can scale to millions of vectors
- Server mode available when needed

**Cons:**
- Not as fast as FAISS for pure vector search
- Relatively new (less battle-tested)

**Setup:**
```bash
pip install chromadb
```

**Usage:**
```python
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize
client = chromadb.PersistentClient(path="./feedback_db/chroma")
collection = client.get_or_create_collection(
    name="ats_feedback",
    metadata={"hnsw:space": "cosine"}
)

# Add vectors
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
text = "Sample feedback text"
embedding = embedding_model.encode(text).tolist()

collection.add(
    ids=["feedback_1"],
    embeddings=[embedding],
    documents=[text],
    metadatas=[{"rating": 5, "user": "john"}]
)

# Search with filters
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"rating": {"$gte": 4}}
)
```

**When to use:**
- Building RAG systems
- Feedback collection with metadata
- Development and prototyping
- Small to medium production deployments

---

### 2. FAISS

**Best for:** Maximum speed, large scale, research

**Pros:**
- Extremely fast vector search
- Can handle billions of vectors
- Battle-tested (by Meta/Facebook)
- Multiple index types for different use cases
- GPU support
- Free and open source

**Cons:**
- No built-in metadata filtering
- Manual persistence (save/load from disk)
- More complex API
- No server mode (file-based only)

**Setup:**
```bash
pip install faiss-cpu  # or faiss-gpu
```

**Usage:**
```python
import faiss
import numpy as np
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# With LangChain
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embeddings)

# Save/Load
vectorstore.save_local("./vector_store")
vectorstore = FAISS.load_local("./vector_store", embeddings)

# Search
results = vectorstore.similarity_search("query", k=5)
```

**When to use:**
- Need maximum search speed
- Large scale (millions+ vectors)
- Research projects
- Don't need metadata filtering
- Offline/local deployments

---

### 3. Pinecone

**Best for:** Production at scale, managed service

**Pros:**
- Fully managed (zero ops)
- Scales to billions of vectors
- Built-in metadata filtering
- High availability and reliability
- Real-time updates
- Hybrid search (vector + keyword)
- Good documentation and support

**Cons:**
- Costs money (free tier limited to 1M vectors)
- Requires internet connection
- Vendor lock-in
- Pricing: $70+/month after free tier

**Setup:**
```bash
pip install pinecone-client
```

**Usage:**
```python
import pinecone

# Initialize
pinecone.init(api_key="your-api-key", environment="us-west1-gcp")
index = pinecone.Index("ats-feedback")

# Upsert vectors
index.upsert(vectors=[
    ("feedback_1", embedding, {"rating": 5, "user": "john"})
])

# Query with filters
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={"rating": {"$gte": 4}}
)
```

**Pricing:**
- Free: 1M vectors, 1 index
- Starter: $70/month - 5M vectors
- Standard: $0.096/hour per pod

**When to use:**
- Production applications at scale
- Need high availability
- Don't want to manage infrastructure
- Have budget for managed service

---

### 4. Qdrant

**Best for:** Self-hosted production, advanced features

**Pros:**
- Rich filtering capabilities
- Payload (metadata) support
- Multiple vector per point
- Quantization for memory efficiency
- REST and gRPC APIs
- Good performance
- Open source with managed option

**Cons:**
- Requires Docker or separate server
- More complex setup than ChromaDB
- Managed service costs money

**Setup:**
```bash
# Docker
docker run -p 6333:6333 qdrant/qdrant

# Python client
pip install qdrant-client
```

**Usage:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Initialize
client = QdrantClient(host="localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="ats_feedback",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Insert
client.upsert(
    collection_name="ats_feedback",
    points=[
        PointStruct(
            id="feedback_1",
            vector=embedding,
            payload={"rating": 5, "user": "john"}
        )
    ]
)

# Search with filters
results = client.search(
    collection_name="ats_feedback",
    query_vector=query_embedding,
    limit=5,
    query_filter={"must": [{"key": "rating", "range": {"gte": 4}}]}
)
```

**Pricing:**
- Self-hosted: Free
- Cloud: Starting at $25/month

**When to use:**
- Need advanced filtering
- Self-hosted production
- Multiple vectors per document
- Want open source with enterprise features

---

### 5. Weaviate

**Best for:** Complex schemas, GraphQL, semantic search

**Pros:**
- GraphQL API
- Built-in vectorization modules
- Hybrid search (vector + keyword + filters)
- Schema management
- Multi-tenancy support
- Open source

**Cons:**
- Heavier and more complex
- Steeper learning curve
- Requires Docker or cloud

**Setup:**
```bash
# Docker
docker run -p 8080:8080 semitechnologies/weaviate:latest

# Python client
pip install weaviate-client
```

**Usage:**
```python
import weaviate

# Initialize
client = weaviate.Client("http://localhost:8080")

# Create schema
schema = {
    "class": "Feedback",
    "properties": [
        {"name": "text", "dataType": ["text"]},
        {"name": "rating", "dataType": ["int"]}
    ]
}
client.schema.create_class(schema)

# Add data
client.data_object.create(
    data_object={"text": "feedback text", "rating": 5},
    class_name="Feedback",
    vector=embedding
)

# Search
results = client.query.get("Feedback", ["text", "rating"]) \
    .with_near_vector({"vector": query_embedding}) \
    .with_limit(5) \
    .with_where({"path": ["rating"], "operator": "GreaterThanEqual", "valueInt": 4}) \
    .do()
```

**When to use:**
- Need complex data schemas
- Want GraphQL interface
- Building knowledge graphs
- Need multi-tenancy

---

### 6. PostgreSQL + pgvector

**Best for:** Already using Postgres, simple vector needs

**Pros:**
- Use existing Postgres infrastructure
- ACID transactions
- Familiar SQL interface
- Good for hybrid (relational + vector) data
- Free and open source

**Cons:**
- Not as fast as specialized vector DBs
- Limited to ~1M vectors efficiently
- Requires Postgres management

**Setup:**
```bash
# Install extension in Postgres
CREATE EXTENSION vector;

# Python
pip install pgvector psycopg2
```

**Usage:**
```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect(database="ats_db")
register_vector(conn)

# Create table
cur = conn.cursor()
cur.execute("""
    CREATE TABLE feedback (
        id TEXT PRIMARY KEY,
        embedding vector(384),
        text TEXT,
        rating INTEGER
    )
""")

# Insert
cur.execute(
    "INSERT INTO feedback VALUES (%s, %s, %s, %s)",
    ("feedback_1", embedding, "text", 5)
)

# Search
cur.execute("""
    SELECT id, text, rating, embedding <=> %s AS distance
    FROM feedback
    WHERE rating >= 4
    ORDER BY distance
    LIMIT 5
""", (query_embedding,))
```

**When to use:**
- Already using PostgreSQL
- Need transactional guarantees
- Hybrid relational + vector data
- Small to medium scale

---

## Decision Matrix

| Database | Setup Complexity | Scale | Speed | Metadata | Cost | Best For |
|----------|-----------------|-------|-------|----------|------|----------|
| **ChromaDB** | ⭐ Easy | Medium | Good | ✅ Yes | Free | Development, RAG apps |
| **FAISS** | ⭐⭐ Medium | Very High | Excellent | ❌ No | Free | Speed, research |
| **Pinecone** | ⭐ Easy | Very High | Excellent | ✅ Yes | $$$ | Production, managed |
| **Qdrant** | ⭐⭐ Medium | Very High | Excellent | ✅ Yes | Free/$ | Self-hosted prod |
| **Weaviate** | ⭐⭐⭐ Hard | High | Good | ✅ Yes | Free/$ | Complex schemas |
| **pgvector** | ⭐⭐ Medium | Medium | Good | ✅ Yes | Free | Existing Postgres |

## Migration Path

**Recommended progression:**

1. **Development**: ChromaDB (embedded)
2. **Small Production**: ChromaDB (server mode)
3. **Scale Up**: Pinecone or Qdrant
4. **Enterprise**: Pinecone or self-hosted Qdrant cluster

## For ATS Feedback System

**Start with ChromaDB because:**
- Zero setup complexity
- Built for LLM/RAG use cases
- Metadata filtering for ratings, dates, users
- Persistent storage out of the box
- Can handle your scale (thousands to millions of feedback samples)
- Free and open source
- Easy to migrate later if needed

**Example Implementation:**

```python
# feedback_vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer

class FeedbackVectorStore:
    def __init__(self, path="./feedback_db/chroma"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name="ats_feedback",
            metadata={"hnsw:space": "cosine"}
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_feedback(self, feedback_id, query, response, rating, metadata=None):
        text = f"Query: {query}\nResponse: {response}"
        embedding = self.embedding_model.encode(text).tolist()
        
        self.collection.add(
            ids=[feedback_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "rating": rating,
                "query": query,
                "response": response,
                **(metadata or {})
            }]
        )
    
    def search_similar(self, query, n_results=5, min_rating=None):
        query_embedding = self.embedding_model.encode(query).tolist()
        where_filter = {"rating": {"$gte": min_rating}} if min_rating else None
        
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
    
    def get_high_quality_samples(self, min_rating=4, limit=100):
        return self.collection.get(
            where={"rating": {"$gte": min_rating}},
            limit=limit
        )
```

## Resources

- **ChromaDB**: https://www.trychroma.com/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Pinecone**: https://www.pinecone.io/
- **Qdrant**: https://qdrant.tech/
- **Weaviate**: https://weaviate.io/
- **pgvector**: https://github.com/pgvector/pgvector
