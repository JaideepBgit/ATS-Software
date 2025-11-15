# ATS Storage System Documentation

## Overview

The ATS system now has a comprehensive persistent storage system that tracks:
- **Job Descriptions** with unique IDs
- **Resumes** (PDFs and extracted text)
- **Analysis Results** linked to jobs and resumes
- **Feedback** linked to analyses for LoRA training

## Storage Architecture

### 1. Job Storage (`job_storage.py`)

Stores job descriptions with unique identifiers.

**Location**: `data/jobs/`
- `jobs.jsonl` - Full job records
- `jobs_index.json` - Quick lookup index

**Features**:
- Each job gets a unique 8-character ID (e.g., `a3f7b2c1`)
- Tracks company name, role name, and full job description
- Counts how many analyses have been performed for each job
- Search by company or role name

**API Endpoints**:
```
POST /api/job-description          # Create new job (returns job_id)
GET  /api/jobs                      # List all jobs
GET  /api/jobs/{job_id}             # Get specific job
POST /api/jobs/{job_id}/select     # Select job as current
GET  /api/jobs/search?query=...    # Search jobs
```

### 2. Resume Storage (`resume_storage.py`)

Stores uploaded resumes with persistent storage.

**Location**: `data/resumes/`
- `pdfs/` - Original PDF files
- `texts/` - Extracted text files
- `resumes_index.json` - Resume metadata

**Features**:
- Each resume gets a unique ID based on content hash
- Stores both PDF and extracted text
- Prevents duplicate uploads (same PDF = same ID)
- Tracks candidate name, upload date, file size

**API Endpoints**:
```
POST /api/upload-resume            # Upload resume (returns resume_id)
GET  /api/resumes                  # List all resumes
GET  /api/resumes/{resume_id}      # Get resume metadata
GET  /api/resumes/{resume_id}/text # Get resume text
```

### 3. Analysis Storage (`analysis_storage.py`)

Stores analysis results linking resumes to jobs.

**Location**: `data/analyses/`
- `analyses.jsonl` - Full analysis records
- `analyses_index.json` - Quick lookup index

**Features**:
- Each analysis gets a unique 12-character ID
- Links to both job_id and resume_id
- Stores complete analysis results
- Tracks feedback count for each analysis

**API Endpoints**:
```
GET /api/analyses                      # List all analyses
GET /api/analyses?job_id={job_id}     # Filter by job
GET /api/analyses/{analysis_id}       # Get specific analysis
```

### 4. Feedback Storage (`feedback_store.py`)

Enhanced to link feedback to analyses and jobs.

**Location**: `feedback_db/`
- `interactions.jsonl` - Feedback records
- `chroma/` - ChromaDB vector database
- `faiss_index.bin` - FAISS similarity index

**Features**:
- Links feedback to analysis_id and job_id
- Enables LoRA training with proper context
- Vector search for similar feedback
- High-quality sample extraction

**API Endpoints**:
```
POST /api/feedback/submit          # Submit feedback (with analysis_id, job_id)
GET  /api/feedback/statistics      # Get feedback stats
GET  /api/feedback/search          # Search similar feedback
GET  /api/feedback/high-quality    # Get training samples
```

## Workflow

### Complete Analysis Workflow

1. **Create/Select Job**:
   ```
   POST /api/job-description
   {
     "job_description": "...",
     "company_name": "Manhattan Associates",
     "role_name": "Data Scientist"
   }
   
   Response: { "job_id": "a3f7b2c1", ... }
   ```

2. **Upload Resume**:
   ```
   POST /api/upload-resume
   (multipart/form-data with PDF file)
   
   Response: {
     "analysis_id": "f8e2d1c4b3a9",
     "resume_id": "resume_a1b2c3d4e5f6",
     "job_id": "a3f7b2c1",
     "result": { ... analysis results ... }
   }
   ```

3. **Submit Feedback**:
   ```
   POST /api/feedback/submit
   {
     "interaction_id": "unique-id",
     "query": "What are the candidate's Python skills?",
     "response": "The candidate has 5 years of Python...",
     "rating": 5,
     "analysis_id": "f8e2d1c4b3a9",
     "job_id": "a3f7b2c1",
     ...
   }
   ```

### Resume Memory

The system now remembers uploaded resumes:
- PDFs are stored in `data/resumes/pdfs/`
- Extracted text is stored in `data/resumes/texts/`
- You can retrieve any previously uploaded resume
- No need to re-upload the same resume

### Job History

All job descriptions are saved:
- View all past jobs: `GET /api/jobs`
- Search for specific jobs: `GET /api/jobs/search?query=Manhattan`
- Reuse a job: `POST /api/jobs/{job_id}/select`

### Analysis History

All analyses are preserved:
- View all analyses: `GET /api/analyses`
- Filter by job: `GET /api/analyses?job_id=a3f7b2c1`
- See how many times feedback was given

## LoRA Training Integration

The storage system is designed for LoRA training:

1. **Feedback with Context**:
   - Each feedback includes `analysis_id` and `job_id`
   - Can retrieve full job description and resume
   - Provides complete context for training

2. **High-Quality Samples**:
   ```
   GET /api/feedback/high-quality?min_rating=4&limit=100
   ```
   Returns feedback samples rated 4+ stars

3. **Export for Training**:
   ```
   GET /api/feedback/export-csv
   ```
   Downloads all feedback as CSV for training

4. **Vector Search**:
   ```
   GET /api/feedback/search?query=Python+skills&n_results=5
   ```
   Finds similar feedback using embeddings

## Storage Statistics

Get overview of all stored data:
```
GET /api/storage/stats

Response:
{
  "jobs": {
    "total": 15,
    "recent": [...]
  },
  "resumes": {
    "total": 42,
    "recent": [...]
  },
  "analyses": {
    "total": 58,
    "recent": [...]
  },
  "feedback": {
    "total_feedback": 127,
    "average_rating": 4.2
  },
  "current_job_id": "a3f7b2c1"
}
```

## Data Persistence

All data is stored in the `data/` directory:
```
data/
├── jobs/
│   ├── jobs.jsonl
│   └── jobs_index.json
├── resumes/
│   ├── pdfs/
│   ├── texts/
│   └── resumes_index.json
├── analyses/
│   ├── analyses.jsonl
│   └── analyses_index.json
└── jobs_applied/
    └── job_applicaiton.xlsx
```

## Migration Notes

The system maintains backward compatibility:
- Old in-memory storage still works
- New persistent storage runs in parallel
- Gradually migrate to using IDs instead of candidate names

## Benefits

1. **No Data Loss**: All uploads and analyses are saved
2. **Resume Reuse**: Upload once, analyze multiple times
3. **Job Templates**: Save and reuse job descriptions
4. **Training Data**: Complete context for LoRA training
5. **Analytics**: Track which jobs get most applications
6. **Audit Trail**: Full history of all analyses
