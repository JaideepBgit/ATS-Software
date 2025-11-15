# Feedback Collection System Setup

This guide explains how to set up and use the feedback collection system for building your training database.

## What Was Added

### Frontend
- **FeedbackCollector Component**: Allows users to rate responses and provide detailed feedback
  - Quick feedback: Thumbs up/down buttons
  - Detailed feedback: Full form with ratings, correct/incorrect points, and ideal responses
  - Located in: `frontend/src/components/FeedbackCollector.js`

### Backend
- **feedback_store.py**: Manages feedback storage in ChromaDB and FAISS
  - Stores feedback with embeddings
  - Supports semantic search
  - Provides statistics and high-quality sample retrieval
  
- **New API Endpoints**:
  - `POST /api/feedback/submit` - Submit feedback
  - `GET /api/feedback/statistics` - Get feedback stats
  - `GET /api/feedback/search` - Search similar feedback
  - `GET /api/feedback/high-quality` - Get training samples

## Installation

### 1. Install Backend Dependencies

```bash
cd ats_web/backend
pip install chromadb faiss-cpu sentence-transformers numpy
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Verify Installation

The system will automatically initialize ChromaDB and FAISS when the backend starts. Check the console for:
```
✓ ChromaDB initialized
✓ FAISS initialized
```

## How to Use

### 1. Start Your ATS Application

```bash
# Backend
cd ats_web/backend
python main.py

# Frontend (in another terminal)
cd ats_web/frontend
npm start
```

### 2. Collect Feedback

When chatting with the AI about candidates:

**Quick Feedback:**
- Click 👍 if the response was helpful
- Click 👎 if the response needs improvement

**Detailed Feedback:**
- Click the 💬 feedback icon
- Rate the response (1-5 stars)
- List what was correct (comma-separated)
- List what was incorrect (comma-separated)
- List what was missing (comma-separated)
- Optionally provide an ideal response

### 3. View Feedback Statistics

Access the API endpoint:
```bash
curl http://localhost:8000/api/feedback/statistics
```

Response:
```json
{
  "total_feedback": 25,
  "average_rating": 4.2,
  "chromadb_count": 25,
  "faiss_count": 25
}
```

## Database Storage

Feedback is stored in three places:

### 1. ChromaDB (Primary)
- Location: `ats_web/backend/feedback_db/chroma/`
- Features: Semantic search, metadata filtering
- Use for: Finding similar feedback, filtering by rating

### 2. FAISS
- Location: `ats_web/backend/feedback_db/faiss_index.bin`
- Features: Fast vector similarity search
- Use for: Quick nearest neighbor search

### 3. JSONL Backup
- Location: `ats_web/backend/feedback_db/interactions.jsonl`
- Features: Human-readable, easy to process
- Use for: Data export, manual inspection

## Using the Feedback Data

### Search Similar Feedback

```python
# In your Python code
from feedback_store import feedback_store

results = feedback_store.search_similar_chromadb(
    query="What are the candidate's Python skills?",
    n_results=5,
    min_rating=4
)
```

### Get High-Quality Training Samples

```python
samples = feedback_store.get_high_quality_samples(
    min_rating=4,
    limit=100
)
```

### Export for LoRA Training

The feedback is automatically compatible with the LoRA training system in `ats_lora_training/`:

```bash
# Copy feedback to training folder
cp -r ats_web/backend/feedback_db ../ats_lora_training/

# Build training database
cd ../ats_lora_training
python database_builder.py
```

## API Examples

### Submit Feedback via API

```bash
curl -X POST http://localhost:8000/api/feedback/submit \
  -H "Content-Type: application/json" \
  -d '{
    "interaction_id": "unique_id_123",
    "query": "What are the key skills?",
    "context": ["Resume text here"],
    "response": "The candidate has Python and Java skills",
    "rating": 5,
    "correct_points": ["Identified Python", "Mentioned Java"],
    "incorrect_points": [],
    "missing_points": [],
    "ideal_response": "The candidate has Python and Java skills"
  }'
```

### Search Feedback

```bash
curl "http://localhost:8000/api/feedback/search?query=Python%20skills&n_results=5&min_rating=4"
```

### Get Statistics

```bash
curl http://localhost:8000/api/feedback/statistics
```

## Data Structure

Each feedback entry contains:

```json
{
  "id": "candidate_123_msg_0",
  "timestamp": "2025-11-11T13:00:00",
  "query": "What are the candidate's strengths?",
  "context": ["Resume context", "Job description"],
  "response": "The candidate has strong Python skills...",
  "feedback": {
    "rating": 4,
    "correct_points": ["Identified Python skills"],
    "incorrect_points": ["Missed leadership experience"],
    "missing_points": ["Should mention team size"],
    "ideal_response": "Corrected response here"
  },
  "embedding": [0.123, 0.456, ...]
}
```

## Troubleshooting

### ChromaDB Not Available
If you see "ChromaDB not available":
```bash
pip install chromadb
```

### FAISS Not Available
If you see "FAISS not available":
```bash
pip install faiss-cpu
```

For GPU support:
```bash
pip install faiss-gpu
```

### Sentence Transformers Not Available
```bash
pip install sentence-transformers
```

### Feedback Not Saving
1. Check backend console for errors
2. Verify `feedback_db` folder exists and is writable
3. Check API response in browser DevTools

## Next Steps

Once you've collected 100+ feedback samples:

1. **Build Training Database**
   ```bash
   cd ../ats_lora_training
   python database_builder.py --input ../ats_web/backend/feedback_db/interactions.jsonl
   ```

2. **Train LoRA Model**
   ```bash
   python lora_trainer.py --training_data feedback_db/training_pairs
   ```

3. **Evaluate Model**
   ```bash
   python evaluate_model.py --model models/ats_lora_v1
   ```

## Benefits

- **Semantic Understanding**: Embeddings capture meaning, not just keywords
- **Quality Filtering**: Filter by rating to get best training samples
- **Continuous Improvement**: Collect feedback → Train → Deploy → Repeat
- **Human-in-the-Loop**: Your corrections directly improve the model

## Questions?

The feedback system is now integrated into your ATS application. Every time you chat with the AI about candidates, you can provide feedback that will help train a better model!
