# Resume Library Feature

## Overview

The ATS system now has a **Resume Library** that separates resume upload from analysis. This gives you full control over when to analyze resumes.

## New Workflow

### Before ❌
```
Upload Resume → Immediately Analyzes → Can't reuse
```

### After ✅
```
1. Upload Resume → Stored in library
2. Set/Change Job Description
3. Click "Analyze" → Analyzes against current job
4. Reuse same resume for different jobs
```

## Features

### 1. Resume Library
- **Upload resumes** without analyzing
- **View all uploaded resumes** in a table
- **See metadata**: candidate name, filename, upload date, file size
- **Persistent storage**: resumes saved permanently

### 2. Separate Analysis
- **Analyze button** for each resume
- **Choose when to analyze**
- **Analyze against current job description**
- **Reuse resumes** for different jobs

### 3. Job Description Flexibility
- **Change job description** anytime
- **Analyze same resume** against multiple jobs
- **Compare results** across different positions

## How to Use

### Step 1: Upload Resumes
1. Go to "Job & Resume Library" tab
2. Click "Upload Resume" button
3. Select one or more PDF files
4. Resumes are stored in the library

### Step 2: Set Job Description
1. Enter job description in the text area
2. Add company name and role name
3. Click "Save Job Description"

### Step 3: Analyze
1. In the Resume Library table, find the resume
2. Click "Analyze" button next to the resume
3. Wait for analysis to complete
4. View results in "Analysis Results" tab

### Step 4: Reuse (Optional)
1. Change the job description
2. Click "Analyze" again on the same resume
3. Get new analysis for different job

## API Endpoints

### New Endpoints

**Upload Resume Only** (no analysis):
```
POST /api/upload-resume-only
- Uploads PDF
- Extracts text
- Stores in library
- Returns resume_id
```

**Analyze Existing Resume**:
```
POST /api/analyze-resume/{resume_id}
- Analyzes stored resume
- Uses current job description
- Returns analysis result
```

**List Resumes**:
```
GET /api/resumes
- Returns all uploaded resumes
- Includes metadata
```

### Existing Endpoints (Still Work)

**Upload and Analyze** (legacy):
```
POST /api/upload-resume
- Uploads and immediately analyzes
- For backward compatibility
```

## Benefits

### For Users
✅ **Upload once, analyze many times**  
✅ **Build a resume library**  
✅ **Control when to analyze**  
✅ **Compare same resume across jobs**  
✅ **No re-uploading needed**  

### For Workflow
✅ **Separate concerns**: upload vs analysis  
✅ **Flexible**: change job description anytime  
✅ **Efficient**: reuse resumes  
✅ **Organized**: see all resumes in one place  

## UI Components

### Resume Library Table

| Candidate | Filename | Uploaded | Size | Actions |
|-----------|----------|----------|------|---------|
| John Doe | john_resume.pdf | Nov 13, 2:30 PM | 245 KB | [Analyze] |
| Jane Smith | jane_cv.pdf | Nov 13, 3:15 PM | 312 KB | [Analyze] |

### Features
- **Sortable columns**
- **Refresh button** to reload
- **Upload button** to add more
- **Analyze button** per resume
- **Loading states** during analysis

## Example Workflow

### Scenario: Analyzing for Multiple Jobs

```
1. Upload 5 resumes
   → All stored in library

2. Set Job Description: "Data Scientist at TechCorp"
   → Click Analyze on Resume 1
   → Click Analyze on Resume 2
   → View results

3. Change Job Description: "ML Engineer at AILabs"
   → Click Analyze on Resume 1 (same resume!)
   → Click Analyze on Resume 3
   → Compare results

4. Later: Upload 2 more resumes
   → Analyze against current job
   → Or change job and analyze
```

## Technical Details

### Storage
- **PDFs**: `data/resumes/pdfs/`
- **Text**: `data/resumes/texts/`
- **Index**: `data/resumes/resumes_index.json`

### Resume ID
- Based on content hash
- Same PDF = same ID
- Prevents duplicates

### Analysis Linking
- Each analysis links to:
  - `resume_id` - which resume
  - `job_id` - which job description
  - `analysis_id` - unique analysis

## Migration

### Old Code (Still Works)
```javascript
// Upload and analyze immediately
POST /api/upload-resume
```

### New Code (Recommended)
```javascript
// Upload only
POST /api/upload-resume-only

// Analyze later
POST /api/analyze-resume/{resume_id}
```

## Troubleshooting

### "Please set job description first"
- Set a job description before clicking Analyze
- The Analyze button is disabled until job is set

### "Resume not found"
- Resume might have been deleted
- Refresh the library
- Re-upload if needed

### Can't see uploaded resume
- Click the Refresh button
- Check browser console for errors
- Verify backend is running

## Future Enhancements

Potential additions:
- **Bulk analyze**: Analyze all resumes at once
- **Resume search**: Search by candidate name
- **Resume tags**: Categorize resumes
- **Resume preview**: View PDF in browser
- **Delete resumes**: Remove from library
- **Resume comparison**: Side-by-side comparison

## Summary

The Resume Library feature gives you:
- ✅ **Control**: Choose when to analyze
- ✅ **Flexibility**: Reuse resumes for different jobs
- ✅ **Efficiency**: No re-uploading
- ✅ **Organization**: All resumes in one place
- ✅ **Persistence**: Resumes saved forever

**Status**: ✅ Complete and Ready to Use
