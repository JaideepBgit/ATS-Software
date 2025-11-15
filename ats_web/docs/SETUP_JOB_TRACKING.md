# Quick Setup: Job Application Tracking

## 🚀 5-Minute Setup Guide

### Step 1: Install Backend Dependency

```bash
cd backend
pip install openpyxl
```

### Step 2: Restart Backend

**Option A: Without Docker**
```bash
cd backend
python main.py
```

**Option B: With Docker**
```bash
docker-compose down
docker-compose up --build
```

### Step 3: That's It!

The feature is now active. Open your browser and you'll see a **"Job Tracker"** button in the top-right corner.

## ✅ Verify Installation

1. Open the web app: `http://localhost:3000`
2. Click the **"Job Tracker"** button
3. You should see the Job Tracking modal
4. The Excel file will be created automatically at: `data/jobs_applied/job_applicaiton.xlsx`

## 🎯 First Use

1. Set up a job description
2. Upload and analyze a resume
3. Click **"Job Tracker"** button
4. Click **"Yes, Log Application"**
5. Fill in details and submit
6. Check the Excel file to see your logged application!

## 📊 What You Get

- **Job Tracker Button**: Top-right corner of the app
- **Statistics Dashboard**: Overview of all applications
- **Application List**: Table of all logged jobs
- **Excel File**: `data/jobs_applied/job_applicaiton.xlsx`

## 🔧 Troubleshooting

### Backend Error: "No module named 'openpyxl'"

**Solution:**
```bash
pip install openpyxl
```

### Excel File Not Found

**Solution:**
- The file is created automatically on first use
- Make sure the backend has write permissions
- Check that `data/jobs_applied/` directory exists

### Button Not Showing

**Solution:**
- Clear browser cache
- Restart the frontend: `npm start`
- Check browser console for errors

## 📝 Files Modified

- ✅ `backend/main.py` - Added tracking endpoints
- ✅ `backend/job_tracker.py` - New tracking module
- ✅ `backend/requirements.txt` - Added openpyxl
- ✅ `frontend/src/App.js` - Added Job Tracker button
- ✅ `frontend/src/components/JobTracking.js` - New component
- ✅ `frontend/src/components/JobTracking.css` - Styling

## 🎉 You're Ready!

Start tracking your job applications and monitor your job search progress!

For detailed documentation, see `JOB_TRACKING_FEATURE.md`.
