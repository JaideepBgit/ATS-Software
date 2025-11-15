# Storage System Quick Start Guide

## What's New?

Your ATS system now has **persistent storage** with unique IDs for everything:

✅ **Job Descriptions** - Each gets a unique ID (e.g., `a3f7b2c1`)  
✅ **Resumes** - PDFs are saved, no need to re-upload  
✅ **Analyses** - All results are stored with links to jobs  
✅ **Feedback** - Linked to analyses for LoRA training  

## Quick Start

### 1. Test the Storage System

```bash
cd ats_web/backend
python test_storage_system.py
```

This will:
- Create a test job description
- Show you all stored jobs
- Display storage statistics
- Verify everything works

### 2. Using the Web Interface

**Step 1: Create a Job**
1. Paste job description in the text area
2. Enter company name (e.g., "Manhattan Associates")
3. Enter role name (e.g., "Data Scientist")
4. Click "Save Job Description"
5. **You'll get a job_id** - this is saved permanently!

**Step 2: Upload Resume**
1. Click "Upload Resume" button
2. Select a PDF file
3. Click "Analyze"
4. **You'll get**: `analysis_id`, `resume_id`, `job_id`

**Step 3: Give Feedback**
1. Ask questions about the candidate
2. Rate the responses (1-5 stars)
3. Provide corrections if needed
4. **Feedback is linked to the analysis and job**

### 3. View Your Data

**List all jobs:**
```bash
curl http://localhost:8000/api/jobs
```

**Get specific job:**
```bash
curl http://localhost:8000/api/jobs/a3f7b2c1
```

**List all analyses:**
```bash
curl http://localhost:8000/api/analyses
```

**Get storage stats:**
```bash
curl http://localhost:8000/api/storage/stats
```

### 4. Reuse Saved Jobs

Instead of re-entering job descriptions:

```bash
# List your jobs
curl http://localhost:8000/api/jobs

# Select a job to use
curl -X POST http://localhost:8000/api/jobs/a3f7b2c1/select
```

Now any resume you upload will be analyzed against that job!

### 5. For LoRA Training

All feedback now includes:
- `analysis_id` - Links to the specific analysis
- `job_id` - Links to the job description
- Full context for training

Export feedback for training:
```bash
curl http://localhost:8000/api/feedback/export-csv > feedback.csv
```

Get high-quality samples (4+ stars):
```bash
curl "http://localhost:8000/api/feedback/high-quality?min_rating=4&limit=100"
```

## Data Location

All data is stored in `ats_web/backend/data/`:

```
data/
├── jobs/              # Job descriptions
├── resumes/           # Uploaded PDFs and text
├── analyses/          # Analysis results
└── jobs_applied/      # Job application tracking
```

## Benefits

1. **No More Re-uploading**: Upload resume once, analyze against multiple jobs
2. **Job Templates**: Save common job descriptions
3. **Complete History**: See all past analyses
4. **Better Training**: Feedback has full context
5. **No Data Loss**: Everything persists across restarts

## Troubleshooting

**"No job ID found" error:**
- Make sure you saved a job description first
- Or select an existing job: `POST /api/jobs/{job_id}/select`

**Can't find my resume:**
- Check: `GET /api/resumes`
- Resumes are stored by content hash
- Same PDF = same resume_id

**Where's my feedback?**
- Check: `GET /api/feedback/statistics`
- Feedback is in `feedback_db/interactions.jsonl`

## Next Steps

1. **Update Frontend** to display job_id, analysis_id, resume_id
2. **Add Job Selector** dropdown to switch between saved jobs
3. **Resume Library** to view and reuse uploaded resumes
4. **Analysis History** to see past results
5. **Training Pipeline** to use feedback for LoRA fine-tuning

## API Reference

See `STORAGE_SYSTEM.md` for complete API documentation.
