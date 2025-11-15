# HOTFIX: Global Variable Scope Issue

## Problem
After the initial fix, the backend was throwing an error:
```
✗ Error processing resume: name 'company_name' is not defined
```

This occurred even when the company_name was properly defined.

## Root Cause
In Python, functions need to explicitly declare `global` variables if they want to **read** them (not just write). The functions were trying to access `company_name`, `role_name`, and `job_description` without declaring them as global.

## Fix Applied

### Part 1: Global Declarations in main.py
Added `global` declarations to all functions that read these variables:

1. `upload_resume()` - Added: `global job_description, company_name, role_name`
2. `get_job_description()` - Added: `global job_description, company_name, role_name`
3. `ask_question()` - Added: `global job_description`
4. `debug_storage()` - Added: `global job_description, company_name, role_name`

### Part 2: Function Parameter in ats_service.py
Fixed `_generate_thinking_process()` function:

1. Added `company_name` parameter to function signature
2. Updated the call to pass `company_name` from `analyze_resume()`

## Code Changes

### Before (BROKEN):
```python
@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze a resume"""
    if not job_description:  # ❌ Error: 'job_description' not defined
        raise HTTPException(...)
    
    print(f"Company: '{company_name}'")  # ❌ Error: 'company_name' not defined
```

### After (FIXED):
```python
@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and analyze a resume"""
    global job_description, company_name, role_name  # ✅ Declare globals
    
    if not job_description:  # ✅ Works now
        raise HTTPException(...)
    
    print(f"Company: '{company_name}'")  # ✅ Works now
```

## Why This Happened
Python's scoping rules:
- **Writing** to a variable makes it local by default
- **Reading** a global variable requires explicit `global` declaration
- The `set_job_description()` function had `global` because it **writes** to the variables
- Other functions only **read** them, but still need the `global` declaration

## Testing
After this fix, you should be able to:
1. Save a job description with company and role
2. Upload a resume without errors
3. See the analysis complete successfully

## Quick Test
```bash
# Restart the backend
cd ats_web/backend
python main.py

# Then try uploading a resume through the UI
```

## Verification
Check backend logs - you should see:
```
[DEBUG] ===== ANALYZING RESUME =====
[DEBUG] Company: 'Manhattan Associates'
[DEBUG] Role: 'Data Scientist'
```

No more "name 'company_name' is not defined" errors!

## Files Modified
- `ats_web/backend/main.py` - Added global declarations to 4 functions
- `ats_web/backend/ats_service.py` - Added company_name parameter to _generate_thinking_process()

## Status
✅ **FIXED** - Ready to test (restart backend required)
