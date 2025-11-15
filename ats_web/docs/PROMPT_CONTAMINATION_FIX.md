# Prompt Contamination Fix

## Problem Identified

The ATS system was analyzing resumes against **example data in the prompt** instead of the actual job description provided by the user.

### Root Cause

In `ats_web/backend/ats_service.py`, the prompts sent to the LLM contained example JSON responses with hardcoded values like:

```json
{
  "missing_critical_skills": [
    "Azure cloud platform",
    "Kubernetes orchestration", 
    "Team leadership experience",
    "PhD or equivalent research experience",
    "Healthcare domain knowledge"
  ],
  "weaknesses": [
    "No explicit leadership or mentoring experience mentioned for Principal-level role",
    "Limited cloud experience (only AWS, missing Azure/GCP)",
    "No healthcare/medical domain experience"
  ]
}
```

The LLM was treating these **examples** as the actual requirements, even when analyzing a completely different job description (like the Manhattan Associates Data Scientist role which doesn't require Azure, healthcare knowledge, or PhD).

## Solution Applied

### 1. Fixed Main Analysis Prompt (Line ~210)

**Before:**
```python
Return this exact JSON structure:
{
  "skill_match_score": 75.0,
  "missing_critical_skills": ["Azure cloud platform", "Kubernetes orchestration", ...],
  ...
}
```

**After:**
```python
Return this exact JSON structure (analyze based ONLY on the actual job description above):
{
  "skill_match_score": <number 0-100>,
  "missing_critical_skills": ["<missing skill from actual job description>", "..."],
  ...
}
```

### 2. Fixed Thinking Process Prompt (Line ~340)

**Before:**
```python
{
  "thoughts": [
    {"step": "...", "thinking": "...the job requires Azure and I only see AWS..."},
    {"step": "...", "thinking": "...missing domain knowledge in healthcare..."},
    {"step": "...", "thinking": "...For a Principal role..."}
  ]
}
```

**After:**
```python
{
  "thoughts": [
    {"step": "Understanding Requirements", "thinking": "What does this specific role need? Let me identify requirements from the actual job description..."},
    ...
  ]
}
```

## Impact

- The system will now analyze candidates based on the **actual job requirements** provided
- Missing skills and weaknesses will be specific to the **real job description**
- No more contamination from hardcoded example data

## Testing

To verify the fix:

1. Restart the backend server
2. Upload a job description (e.g., Manhattan Associates Data Scientist)
3. Analyze a resume
4. Verify that missing skills and weaknesses match the actual job requirements
5. Check that there are no references to Azure, healthcare, PhD, or Principal-level if those aren't in the job description

## Files Modified

- `ats_web/backend/ats_service.py` - Removed example data from prompts
