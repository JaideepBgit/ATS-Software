# Testing Checklist - Candidate Details Fix

## Pre-Testing Setup

- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] LLM service (Ollama/LM Studio) is running
- [ ] Browser is open to http://localhost:3000

## Step 1: Clear Old Data (Recommended)

- [ ] Double-click `CLEAR_RESULTS.bat` OR
- [ ] Run: `curl -X DELETE http://localhost:8000/api/results` OR
- [ ] In browser console: `fetch('/api/results', {method: 'DELETE'})`
- [ ] Confirm: "Results cleared successfully" message

## Step 2: Save Job Description

- [ ] Go to "Setup & Upload" tab
- [ ] Enter Company Name: `Manhattan Associates`
- [ ] Enter Role Name: `Data Scientist`
- [ ] Paste the Data Scientist job description
- [ ] Click "Save Job Description"
- [ ] Confirm: Green success message appears
- [ ] Check backend logs for:
  ```
  [DEBUG] ===== JOB DESCRIPTION SAVED =====
  [DEBUG] Company: 'Manhattan Associates'
  [DEBUG] Role: 'Data Scientist'
  ```

## Step 3: Upload Resume

- [ ] Click "Choose File" or drag-and-drop your resume PDF
- [ ] Click "Analyze Resume"
- [ ] Wait for analysis to complete (progress indicator)
- [ ] Confirm: Success message appears
- [ ] Check backend logs for:
  ```
  [DEBUG] ===== ANALYZING RESUME =====
  [DEBUG] Company: 'Manhattan Associates'
  [DEBUG] Role: 'Data Scientist'
  [ATS] analyze_resume called with company='Manhattan Associates', role='Data Scientist'
  ```

## Step 4: Verify Results List

- [ ] Go to "Results" tab
- [ ] Confirm: Results list shows at least one entry
- [ ] Check "Company - Role" column shows: `Manhattan Associates - Data Scientist`
- [ ] Check "Overall Score" is displayed
- [ ] Check "Recommendation" chip is shown

## Step 5: Verify Candidate Detail View

- [ ] Click "View" button on the result
- [ ] Confirm: Candidate name is displayed
- [ ] Confirm: Filename is displayed
- [ ] **NEW:** Confirm: `Manhattan Associates - Data Scientist` is displayed below filename
- [ ] Confirm: Overall score and recommendation chips are shown
- [ ] Check "AI Thinking Process" section (expand it)
- [ ] Confirm: Thinking process mentions "Data Scientist" role
- [ ] Confirm: No mention of wrong roles (e.g., "Principal ML Engineer")

## Step 6: Verify Analysis Content

### Score Breakdown
- [ ] Skills Match score is displayed
- [ ] Experience Match score is displayed
- [ ] Education Match score is displayed

### Executive Summary
- [ ] Summary is relevant to Data Scientist role
- [ ] No mention of wrong job titles or requirements

### Matched Skills
- [ ] Skills listed are relevant to Data Scientist position
- [ ] Skills match what's in your resume

### Missing Skills
- [ ] Missing skills are relevant to Data Scientist job description
- [ ] No mention of irrelevant skills (e.g., "Healthcare domain knowledge" if not in job)
- [ ] Skills match what's actually required in the job posting

### Strengths
- [ ] Strengths are relevant to Data Scientist role
- [ ] References actual experience from resume

### Weaknesses
- [ ] Weaknesses are relevant to Data Scientist position
- [ ] No mention of wrong role levels (e.g., "Principal-level" if job is not Principal)
- [ ] Gaps identified match the actual job requirements

## Step 7: Test Chat Interface

- [ ] Scroll down to chat interface
- [ ] Ask: "What makes this candidate a good fit for this role?"
- [ ] Confirm: Response mentions Data Scientist role
- [ ] Confirm: Response references Manhattan Associates
- [ ] Confirm: No mention of wrong jobs or roles

## Step 8: Backend Logs Verification

Check backend console for complete flow:

- [ ] Job description saved with correct company/role
- [ ] Resume analysis started with correct company/role
- [ ] Result created with correct company/role
- [ ] No errors or warnings in logs

## Step 9: Test with Different Job (Optional)

- [ ] Go back to "Setup & Upload" tab
- [ ] Enter different company: `Google`
- [ ] Enter different role: `Senior Software Engineer`
- [ ] Paste a different job description
- [ ] Click "Save Job Description"
- [ ] Upload the same resume again
- [ ] Go to "Results" tab
- [ ] Confirm: TWO results now shown
- [ ] Confirm: Each result shows correct company/role
- [ ] Click "View" on the new result
- [ ] Confirm: Shows "Google - Senior Software Engineer"
- [ ] Confirm: Analysis is different from first one

## Step 10: Test Result Persistence

- [ ] Refresh the browser page (F5)
- [ ] Go to "Results" tab
- [ ] Confirm: Results are still there
- [ ] Click "View" on a result
- [ ] Confirm: Company and role still displayed correctly

## Common Issues Checklist

If something doesn't work, check:

- [ ] Backend server is running (check console for errors)
- [ ] Frontend is connected to backend (check browser console)
- [ ] LLM service is running and responding
- [ ] Job description was saved BEFORE uploading resume
- [ ] Browser cache is cleared if seeing old data
- [ ] Backend logs show correct company/role throughout

## Success Criteria

✅ All of these should be TRUE:

1. Company and role are displayed in candidate detail view
2. Results list shows company and role for each result
3. Analysis content matches the job description
4. Missing skills are relevant to the actual job
5. Weaknesses reference the correct role level
6. Backend logs show correct data flow
7. No mention of wrong/old job titles in analysis
8. Chat responses reference the correct job

## If Tests Fail

1. Read `QUICK_FIX_STEPS.md` for troubleshooting
2. Read `FIX_CANDIDATE_DETAILS_ISSUE.md` for detailed explanation
3. Run `python backend/test_job_flow.py` to test backend
4. Check backend logs for errors
5. Clear results and try again
6. Restart backend server if needed

## Test Results

Date Tested: _______________
Tester: _______________

Overall Result: [ ] PASS  [ ] FAIL

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
