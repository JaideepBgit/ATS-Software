# ATS Storage Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      ATS Web Application                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (main.py)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Global State:                                       │   │
│  │  - current_job_id                                    │   │
│  │  - job_description, company_name, role_name          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ JobStorage   │ │ResumeStorage │ │AnalysisStore │ │FeedbackStore │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ data/jobs/   │ │data/resumes/ │ │data/analyses/│ │feedback_db/  │
│ - jobs.jsonl │ │ - pdfs/      │ │ - analyses.  │ │ - interact.  │
│ - index.json │ │ - texts/     │ │   jsonl      │ │   jsonl      │
│              │ │ - index.json │ │ - index.json │ │ - chroma/    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

## Data Flow

### 1. Job Description Flow

```
User Input                    Backend                     Storage
─────────                    ─────────                   ─────────

Job Description  ──────►  POST /api/job-description
Company Name                      │
Role Name                         │
                                  ▼
                          JobStorage.add_job()
                                  │
                                  ├──► Generate job_id (8 chars)
                                  │
                                  ├──► Save to jobs.jsonl
                                  │
                                  ├──► Update jobs_index.json
                                  │
                                  └──► Set current_job_id
                                  
                          Return: { job_id, ... }
```

### 2. Resume Upload & Analysis Flow

```
User Action                  Backend                      Storage
───────────                 ─────────                    ─────────

Upload PDF  ──────►  POST /api/upload-resume
                            │
                            ├──► Extract text from PDF
                            │
                            ├──► ResumeStorage.save_resume()
                            │         │
                            │         ├──► Generate resume_id (hash)
                            │         ├──► Save PDF to pdfs/
                            │         ├──► Save text to texts/
                            │         └──► Update index
                            │
                            ├──► ATSService.analyze_resume()
                            │         │
                            │         └──► Generate analysis result
                            │
                            ├──► AnalysisStorage.save_analysis()
                            │         │
                            │         ├──► Generate analysis_id (12 chars)
                            │         ├──► Link to job_id & resume_id
                            │         ├──► Save to analyses.jsonl
                            │         └──► Update index
                            │
                            └──► JobStorage.increment_analysis_count()
                            
                    Return: {
                      analysis_id,
                      resume_id,
                      job_id,
                      result: { ... }
                    }
```

### 3. Feedback Flow

```
User Feedback               Backend                      Storage
─────────────              ─────────                    ─────────

Question & Rating  ──►  POST /api/feedback/submit
Analysis ID                    │
Job ID                         │
                               ▼
                       FeedbackStore.add_feedback()
                               │
                               ├──► Generate embedding
                               │
                               ├──► Save to interactions.jsonl
                               │
                               ├──► Add to ChromaDB (vector search)
                               │
                               ├──► Add to FAISS index
                               │
                               └──► Link to analysis_id & job_id
                               
                       AnalysisStorage.increment_feedback_count()
                       
                Return: { feedback_id, ... }
```

## ID Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                         Job (job_id)                         │
│  "a3f7b2c1" - Manhattan Associates - Data Scientist         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ has many
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analysis (analysis_id)                    │
│  "f8e2d1c4b3a9" - John Doe - Score: 85%                     │
│  ├─ job_id: "a3f7b2c1"                                      │
│  └─ resume_id: "resume_a1b2c3d4e5f6"                        │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         │ references                         │ references
         ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────┐
│Resume (resume_id)    │          │Feedback (interaction)│
│"resume_a1b2c3d4e5f6" │          │"interaction_123"     │
│- PDF stored          │          │├─ analysis_id        │
│- Text extracted      │          │└─ job_id             │
└──────────────────────┘          └──────────────────────┘
```

## Storage Patterns

### JSONL Pattern (Jobs, Analyses)
```
Append-only log format for immutability:

jobs.jsonl:
{"job_id":"a3f7b2c1","company_name":"TechCorp",...}
{"job_id":"b4e8c3d2","company_name":"DataCorp",...}
{"job_id":"c5f9d4e3","company_name":"AILabs",...}

+ Fast index for lookups:
jobs_index.json:
{
  "a3f7b2c1": {"company_name":"TechCorp","created_at":"..."},
  "b4e8c3d2": {"company_name":"DataCorp","created_at":"..."}
}
```

### File Storage Pattern (Resumes)
```
Content-based addressing:

1. Hash PDF content → resume_a1b2c3d4e5f6
2. Store PDF: pdfs/resume_a1b2c3d4e5f6.pdf
3. Store text: texts/resume_a1b2c3d4e5f6.txt
4. Index metadata: resumes_index.json

Benefits:
- Deduplication (same PDF = same ID)
- Fast retrieval by ID
- Separate text for search
```

### Vector Storage Pattern (Feedback)
```
Multi-backend approach:

1. JSONL: Permanent record
2. ChromaDB: Vector similarity search
3. FAISS: Fast approximate search

Query: "Python skills"
   │
   ├──► Generate embedding
   │
   ├──► Search ChromaDB (semantic)
   │
   └──► Return similar feedback
```

## API Endpoint Map

```
Jobs:
  POST   /api/job-description          Create job → job_id
  GET    /api/jobs                     List all jobs
  GET    /api/jobs/{job_id}            Get specific job
  POST   /api/jobs/{job_id}/select     Set as current
  GET    /api/jobs/search?query=...    Search jobs

Resumes:
  POST   /api/upload-resume            Upload → resume_id, analysis_id
  GET    /api/resumes                  List all resumes
  GET    /api/resumes/{resume_id}      Get metadata
  GET    /api/resumes/{resume_id}/text Get text content

Analyses:
  GET    /api/analyses                 List all analyses
  GET    /api/analyses?job_id={id}     Filter by job
  GET    /api/analyses/{analysis_id}   Get specific analysis

Feedback:
  POST   /api/feedback/submit          Submit with IDs
  GET    /api/feedback/statistics      Get stats
  GET    /api/feedback/search          Vector search
  GET    /api/feedback/high-quality    Training samples
  GET    /api/feedback/export-csv      Export all

Storage:
  GET    /api/storage/stats            Complete overview
```

## Scalability Considerations

### Current Implementation
- **JSONL files**: Good for < 100K records
- **File storage**: Good for < 10K resumes
- **In-memory index**: Fast, limited by RAM

### Future Scaling Options
```
Small Scale (Current)
├── JSONL files
├── File system storage
└── In-memory indexes

Medium Scale (1M+ records)
├── SQLite database
├── Compressed storage
└── Disk-based indexes

Large Scale (10M+ records)
├── PostgreSQL
├── S3/Object storage
└── Elasticsearch
```

## Backup Strategy

```
Critical Data:
├── data/jobs/          → Backup daily
├── data/resumes/       → Backup weekly (large files)
├── data/analyses/      → Backup daily
└── feedback_db/        → Backup daily

Backup Command:
tar -czf backup_$(date +%Y%m%d).tar.gz data/ feedback_db/
```

## Performance Characteristics

```
Operation              Time Complexity    Space Complexity
─────────────────────  ─────────────────  ────────────────
Add job                O(1)               O(n)
Get job by ID          O(1)               O(1)
List jobs              O(n)               O(n)
Search jobs            O(n)               O(n)

Add resume             O(1)               O(file_size)
Get resume by ID       O(1)               O(1)

Add analysis           O(1)               O(n)
Get analysis by ID     O(1)               O(1)
Filter by job          O(n)               O(n)

Add feedback           O(log n)           O(embedding_dim)
Vector search          O(log n)           O(k)
```

## Error Handling

```
Storage Layer:
├── File I/O errors → Retry with backoff
├── Disk full → Alert and cleanup
├── Corrupted data → Skip and log
└── Missing files → Rebuild from JSONL

API Layer:
├── Invalid IDs → 404 Not Found
├── Missing data → 400 Bad Request
├── Storage errors → 500 Internal Error
└── Validation errors → 422 Unprocessable
```

## Monitoring Points

```
Metrics to Track:
├── Storage size (GB)
├── Record counts (jobs, resumes, analyses)
├── API response times
├── Error rates
├── Disk usage
└── Memory usage

Alerts:
├── Disk > 90% full
├── Error rate > 1%
├── Response time > 1s
└── Memory > 80%
```
