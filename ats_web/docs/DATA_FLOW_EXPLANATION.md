# Data Flow Explanation: Company Name & Role Name

## Where Values Are Stored

### 1. Backend Storage (In-Memory)
**File:** `ats_web/backend/main.py`

```python
# Global variables (lines 24-26)
job_description: str = ""
company_name: str = ""      # ← Stored here
role_name: str = ""         # ← Stored here
```

### 2. Analysis Results Storage
**File:** `ats_web/backend/main.py`

```python
# Dictionary storing all candidate results (line 22)
analysis_results: Dict[str, Dict] = {}

# Each result contains:
{
  "candidate_name": "John Doe",
  "filename": "resume.pdf",
  "company_name": "Google",     # ← Stored in each result
  "role_name": "ML Engineer",   # ← Stored in each result
  "overall_score": 85.5,
  ...
}
```

### 3. ATSResult Dataclass
**File:** `ats_web/backend/ats_service.py`

```python
@dataclass
class ATSResult:
    candidate_name: str
    filename: str
    ...
    company_name: str = ""    # ← Field definition
    role_name: str = ""       # ← Field definition
```

## Data Flow

### Step 1: User Enters Job Description
1. User fills in Company Name, Role Name, and Job Description
2. Clicks "Save Job Description"
3. Frontend sends POST to `/api/job-description`
4. Backend stores in global variables: `company_name`, `role_name`

### Step 2: User Uploads Resume
1. User uploads PDF resume
2. Frontend sends POST to `/api/upload-resume`
3. Backend calls `analyze_resume(resume_text, job_description, filename, company_name, role_name)`
4. Result is created with company_name and role_name
5. Result is stored in `analysis_results` dictionary

### Step 3: Display Results
1. Frontend calls GET `/api/results`
2. Backend returns all results from `analysis_results`
3. Frontend displays in table with "Company - Role" column

## Debug Endpoints

### Check Current Storage
```bash
curl http://localhost:8000/api/debug/storage
```

Returns:
```json
{
  "job_description_length": 500,
  "company_name": "Google",
  "role_name": "ML Engineer",
  "total_results": 3,
  "sample_result": { ... }
}
```

### Check Job Description
```bash
curl http://localhost:8000/api/job-description
```

## Troubleshooting

### Issue: Company/Role not showing in results

**Possible Causes:**
1. **Old results**: Results uploaded before adding company/role fields won't have them
   - **Solution**: Clear results and re-upload resumes

2. **Empty values**: Company/Role fields were empty when job description was saved
   - **Solution**: Re-enter values and save job description again

3. **Backend not restarted**: Changes to code require backend restart
   - **Solution**: Restart the backend server

### Clear All Results
```bash
curl -X DELETE http://localhost:8000/api/results
```

## Console Logs

When you save job description, you'll see:
```
[DEBUG] Job description saved:
  Company: 'Google'
  Role: 'Machine Learning Engineer'
  Job Desc Length: 500
```

When you upload resume, you'll see:
```
[DEBUG] Analyzing resume with:
  Company: 'Google'
  Role: 'Machine Learning Engineer'
[DEBUG] Result stored:
  Company in result: 'Google'
  Role in result: 'Machine Learning Engineer'
```
