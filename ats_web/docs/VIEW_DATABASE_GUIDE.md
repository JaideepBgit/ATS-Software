# How to View Your Feedback Database

You have **3 ways** to view and explore your feedback database:

## Method 1: Command Line Viewer (Recommended for Quick Checks)

### Run the Interactive Viewer

```bash
cd ats_web/backend
python view_database.py
```

### Features:
- ✅ View statistics (total feedback, average rating, etc.)
- ✅ Browse recent feedback
- ✅ Filter high-quality samples (rating >= 4)
- ✅ Filter low-quality samples (rating <= 2)
- ✅ Search for similar feedback
- ✅ Export to CSV
- ✅ View all feedback entries

### Menu Options:

```
1. View Statistics          - Overview of your database
2. View Recent Feedback     - Last 10 entries
3. View High-Quality        - Good training samples
4. View Low-Quality         - Samples needing correction
5. Search Feedback          - Semantic search
6. Export to CSV            - For Excel/analysis
7. View All Feedback        - Last 20 entries
0. Exit
```

---

## Method 2: Web Dashboard (Coming Soon - Add to Frontend)

### Access via Browser:
1. Add a "View Database" button to your app
2. Opens a dashboard with:
   - Statistics cards
   - Search functionality
   - Export options
   - Visual charts

### To Add to Your App:

Add this button to your main App.js:

```javascript
import FeedbackDashboard from './components/FeedbackDashboard';

// In your component:
const [dashboardOpen, setDashboardOpen] = useState(false);

// Add button:
<Button onClick={() => setDashboardOpen(true)}>
  View Feedback Database
</Button>

// Add component:
<FeedbackDashboard 
  open={dashboardOpen} 
  onClose={() => setDashboardOpen(false)} 
/>
```

---

## Method 3: Direct File Access

### Database Locations:

#### 1. JSONL File (Human-Readable)
**Location:** `ats_web/backend/feedback_db/interactions.jsonl`

**View with:**
- Any text editor (VS Code, Notepad++, etc.)
- Each line is a JSON object

**Example entry:**
```json
{
  "id": "candidate_123_weakness_1699999999",
  "timestamp": "2025-11-11T13:00:00",
  "query": "Is this weakness accurate: 'Limited Python experience'?",
  "context": ["weakness", "Limited Python experience"],
  "response": "Limited Python experience",
  "feedback": {
    "rating": 2,
    "correct_points": [],
    "incorrect_points": ["Limited Python experience"],
    "missing_points": [],
    "ideal_response": "Candidate has 5 years of Python experience"
  },
  "embedding": [0.123, 0.456, ...]
}
```

#### 2. ChromaDB (Vector Database)
**Location:** `ats_web/backend/feedback_db/chroma/`

**View with Python:**
```python
import chromadb

client = chromadb.PersistentClient(path="feedback_db/chroma")
collection = client.get_collection("ats_feedback")

# Get all entries
results = collection.get()
print(f"Total entries: {len(results['ids'])}")

# Search
query_results = collection.query(
    query_texts=["Python skills"],
    n_results=5
)
```

#### 3. FAISS Index (Fast Search)
**Location:** `ats_web/backend/feedback_db/faiss_index.bin`

**View with Python:**
```python
import faiss
import json

# Load index
index = faiss.read_index("feedback_db/faiss_index.bin")
print(f"Total vectors: {index.ntotal}")

# Load ID mapping
with open("feedback_db/faiss_id_map.json", 'r') as f:
    id_map = json.load(f)
    print(f"IDs: {id_map[:5]}")
```

---

## Quick Commands

### View Statistics
```bash
cd ats_web/backend
python -c "from feedback_store import feedback_store; import json; print(json.dumps(feedback_store.get_statistics(), indent=2))"
```

### Count Total Feedback
```bash
cd ats_web/backend
python -c "from pathlib import Path; print(f'Total: {sum(1 for _ in open(\"feedback_db/interactions.jsonl\"))}')"
```

### View Last Entry
```bash
cd ats_web/backend
tail -n 1 feedback_db/interactions.jsonl | python -m json.tool
```

### Export to CSV
```bash
cd ats_web/backend
python view_database.py
# Then select option 6
```

Or via API:
```bash
curl http://localhost:8000/api/feedback/export-csv -o feedback.csv
```

---

## API Endpoints for Viewing

### Get Statistics
```bash
curl http://localhost:8000/api/feedback/statistics
```

Response:
```json
{
  "total_feedback": 150,
  "average_rating": 4.2,
  "chromadb_count": 150,
  "faiss_count": 150
}
```

### Search Feedback
```bash
curl "http://localhost:8000/api/feedback/search?query=Python%20skills&n_results=5"
```

### Get High-Quality Samples
```bash
curl "http://localhost:8000/api/feedback/high-quality?min_rating=4&limit=10"
```

### Export CSV
```bash
curl http://localhost:8000/api/feedback/export-csv -o feedback_export.csv
```

---

## Analysis Tools

### Python Script to Analyze
```python
import json
from pathlib import Path
from collections import Counter

# Load all feedback
feedback = []
with open("feedback_db/interactions.jsonl", 'r') as f:
    for line in f:
        feedback.append(json.loads(line))

# Analyze ratings
ratings = [f['feedback']['rating'] for f in feedback]
print(f"Average rating: {sum(ratings)/len(ratings):.2f}")
print(f"Rating distribution: {Counter(ratings)}")

# Analyze types
types = [f['id'].split('_')[1] for f in feedback if '_' in f['id']]
print(f"Feedback types: {Counter(types)}")

# Find issues
low_rated = [f for f in feedback if f['feedback']['rating'] <= 2]
print(f"Low-rated entries: {len(low_rated)}")
```

### Excel Analysis
1. Export to CSV: `python view_database.py` → Option 6
2. Open in Excel
3. Use pivot tables, charts, filters

---

## Backup Your Database

### Create Backup
```bash
cd ats_web/backend
tar -czf feedback_backup_$(date +%Y%m%d).tar.gz feedback_db/
```

### Restore Backup
```bash
tar -xzf feedback_backup_20251111.tar.gz
```

---

## Database Structure

```
feedback_db/
├── interactions.jsonl          # Main data (human-readable)
├── chroma/                     # ChromaDB vector store
│   ├── chroma.sqlite3         # Metadata database
│   └── [uuid]/                # Vector data
├── faiss_index.bin            # FAISS index file
└── faiss_id_map.json          # ID to index mapping
```

---

## Tips

### Find Specific Feedback
```bash
# Search in JSONL
grep "Python" feedback_db/interactions.jsonl | python -m json.tool
```

### Count by Rating
```bash
grep -o '"rating": [0-9]' feedback_db/interactions.jsonl | sort | uniq -c
```

### View Latest 5 Entries
```bash
tail -n 5 feedback_db/interactions.jsonl | python -m json.tool
```

### Check Database Size
```bash
du -sh feedback_db/
```

---

## Troubleshooting

### "File not found"
- Make sure you're in `ats_web/backend` directory
- Check if `feedback_db/` folder exists
- Submit some feedback first to create the database

### "ChromaDB not available"
```bash
pip install chromadb
```

### "FAISS not available"
```bash
pip install faiss-cpu
```

### Empty Database
- Submit feedback through the UI first
- Check if backend is running
- Verify feedback is being saved (check console logs)

---

## Next Steps

1. **Collect Feedback**: Use the UI to provide feedback on candidates
2. **View Progress**: Run `python view_database.py` regularly
3. **Export Data**: Export to CSV for analysis
4. **Train Model**: Once you have 100+ samples, use for LoRA training

Your feedback database is the foundation for training a better AI model!
