# 🚀 Quick Start: Resume Library

## What Changed?

You now have **full control** over when to analyze resumes!

### Before ❌
- Upload → Immediately analyzes
- Can't see uploaded resumes
- Must re-upload for each job

### After ✅
- Upload → Stored in library
- See all resumes in a table
- Click "Analyze" when ready
- Reuse for different jobs

## How to Use (3 Steps)

### Step 1: Upload Resumes 📤

```
1. Go to "Job & Resume Library" tab
2. Click "Upload Resume" button
3. Select PDF file(s)
4. ✅ Resumes stored in library
```

**Result**: Resumes appear in the table below

### Step 2: Set Job Description 📝

```
1. Enter job description in text area
2. Add company name (e.g., "Manhattan Associates")
3. Add role name (e.g., "Data Scientist")
4. Click "Save Job Description"
```

**Result**: Job is saved and ready for analysis

### Step 3: Analyze 🔍

```
1. Find resume in the library table
2. Click "Analyze" button next to it
3. Wait for analysis to complete
4. Go to "Analysis Results" tab
```

**Result**: Analysis complete!

## Visual Guide

### The Resume Library Table

```
┌──────────────────────────────────────────────────────────┐
│  Resume Library                      [Upload] [Refresh]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Candidate    Filename         Uploaded      Size  Action│
│  ──────────   ──────────────   ──────────   ────  ──────│
│  John Doe     john_resume.pdf  Nov 13 2:30  245KB [Analyze]│
│  Jane Smith   jane_cv.pdf      Nov 13 3:15  312KB [Analyze]│
│  Bob Wilson   bob_resume.pdf   Nov 13 4:00  198KB [Analyze]│
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### What Each Button Does

- **Upload Resume**: Add new resumes to library
- **Refresh**: Reload the resume list
- **Analyze**: Analyze this resume against current job

## Common Workflows

### Workflow 1: Single Job, Multiple Candidates

```
1. Set job description: "Data Scientist at TechCorp"
2. Upload 5 resumes
3. Click "Analyze" on each resume
4. View all results in "Analysis Results" tab
```

### Workflow 2: Multiple Jobs, Same Candidate

```
1. Upload John's resume
2. Set job: "Data Scientist at TechCorp"
3. Click "Analyze" on John's resume
4. Change job: "ML Engineer at AILabs"
5. Click "Analyze" on John's resume again
6. Compare results for different jobs
```

### Workflow 3: Build Library First

```
1. Upload 20 resumes (build your library)
2. Later: Set job description
3. Analyze selected resumes
4. Change job description
5. Analyze different resumes
```

## Tips & Tricks

### 💡 Tip 1: Upload Multiple Files
- Select multiple PDFs at once
- All will be added to library
- Analyze them one by one or all at once

### 💡 Tip 2: Reuse Resumes
- Upload once, analyze many times
- Great for comparing across jobs
- No need to re-upload

### 💡 Tip 3: Change Job Anytime
- Set job description
- Analyze some resumes
- Change job description
- Analyze same or different resumes

### 💡 Tip 4: Refresh to See Updates
- Click refresh button to reload
- See newly uploaded resumes
- Update after backend changes

## Troubleshooting

### ❓ "Analyze button is disabled"
**Solution**: Set a job description first

### ❓ "Don't see my uploaded resume"
**Solution**: Click the Refresh button

### ❓ "Analysis takes too long"
**Solution**: Wait, it's processing. Check backend logs.

### ❓ "Want to delete a resume"
**Solution**: Feature coming soon. For now, resumes stay in library.

## What You Get

### ✅ Control
- Choose when to analyze
- Not forced to analyze immediately

### ✅ Visibility
- See all uploaded resumes
- Table with metadata

### ✅ Reusability
- Upload once
- Analyze multiple times
- Against different jobs

### ✅ Flexibility
- Change job description anytime
- Analyze when ready

### ✅ Persistence
- Resumes saved forever
- No data loss

## Quick Reference

### Keyboard Shortcuts
- None yet (feature request!)

### API Endpoints
```
POST /api/upload-resume-only     # Upload without analyzing
POST /api/analyze-resume/{id}    # Analyze stored resume
GET  /api/resumes                # List all resumes
```

### File Locations
```
data/resumes/pdfs/    # Original PDFs
data/resumes/texts/   # Extracted text
```

## Next Steps

1. **Try it out**: Upload a resume and analyze it
2. **Build library**: Upload multiple resumes
3. **Experiment**: Try different job descriptions
4. **Compare**: Analyze same resume for different jobs

## Need Help?

- **Documentation**: See `RESUME_LIBRARY_FEATURE.md`
- **Full Update**: See `RESUME_LIBRARY_UPDATE.md`
- **Storage System**: See `STORAGE_README.md`

---

**Status**: ✅ Ready to Use  
**Last Updated**: November 13, 2025
