# Simple ATS Matcher - Quick Start Guide

A streamlined ATS (Applicant Tracking System) that works exactly like real company systems. Just provide your resume PDFs and job description, and get instant matching analysis.

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install PyPDF2
```

### 2. Setup Your Files

**Create the folder structure:**
```
ats_python_project/
├── simple_ats.py          # Main script (already created)
├── ats_config.txt         # Configuration file (already created)
└── data/
    ├── resumes/           # Put your PDF resumes here
    └── job_description.txt # Your job description (sample provided)
```

**Add your files:**
- Place PDF resumes in `data/resumes/` folder
- Edit `data/job_description.txt` with your job description
- Or update paths in `ats_config.txt` to point to your files

### 3. Run the ATS
```bash
python simple_ats.py
```

## 📋 Configuration

Edit `ats_config.txt` to customize:

```
# Path to folder containing resume PDFs
RESUME_FOLDER=./data/resumes

# Path to job description text file
JOB_DESCRIPTION_FILE=./data/job_description.txt

# Minimum match score to consider (0-100)
MIN_MATCH_SCORE=60
```

## 📊 What You Get

The ATS will show you:

### For Each Resume:
- **Overall ATS Match Score** (0-100%)
- **Detailed Breakdown:**
  - Skills Match percentage
  - Experience Match percentage
  - Keyword Density score
- **Experience Analysis:**
  - Years on resume vs required
- **✅ Matching Skills:** Skills that match the job
- **❌ Missing Skills:** Required skills not found
- **➕ Additional Skills:** Extra skills the candidate has

### Summary Report:
- Ranked list of all candidates by score
- Pass/Fail status based on minimum score
- Statistics (average, highest, lowest scores)

## 🎯 How It Works (Like Real ATS)

1. **Skill Extraction:** Identifies technical skills, tools, and technologies
2. **Experience Matching:** Compares years of experience
3. **Keyword Analysis:** Measures how well resume matches job description
4. **Scoring Algorithm:**
   - Skills Match: 50% weight
   - Experience Match: 20% weight
   - Keyword Density: 30% weight

## 📝 Example Output

```
================================================================================
📄 RESUME: john_doe_resume.pdf
================================================================================

🟢 ATS MATCH SCORE: 78.5% - GOOD MATCH

📊 DETAILED BREAKDOWN:
   • Skills Match:      85.0%
   • Experience Match:  100.0%
   • Keyword Density:   65.3%

💼 EXPERIENCE:
   • Resume:   6 years
   • Required: 5 years

✅ MATCHING SKILLS (12):
   • python
   • javascript
   • react
   • sql
   • docker
   • aws
   • git
   ...

❌ MISSING REQUIRED SKILLS (3):
   • kubernetes
   • graphql
   • typescript

================================================================================
```

## 🔧 Tips for Best Results

1. **Job Description:** Include clear skill requirements and experience needed
2. **Resume Format:** Use standard PDF format with readable text
3. **Keywords:** Ensure resumes contain relevant technical terms
4. **Skill Synonyms:** The system recognizes common variations (JS = JavaScript, etc.)

## 🎨 Customization

### Add Custom Skill Synonyms

Edit `simple_ats.py` and add to the `skill_synonyms` dictionary:

```python
self.skill_synonyms = {
    'your_skill': ['skill', 'synonym1', 'synonym2'],
    # Add more...
}
```

### Adjust Scoring Weights

Modify the weights in the `calculate_match_score` method:

```python
overall_score = (
    skill_match_pct * 0.5 +      # Change these weights
    exp_match_pct * 0.2 +
    keyword_density * 0.3
)
```

## ❓ Troubleshooting

**No text extracted from PDF:**
- Ensure PDF is not scanned image (needs OCR)
- Try re-saving PDF with text layer

**Skills not detected:**
- Add skill synonyms to the dictionary
- Ensure skills are spelled correctly in resume

**Low scores:**
- Check if resume uses same terminology as job description
- Ensure all required skills are mentioned
- Verify experience years are clearly stated

## 🚀 That's It!

Just run `python simple_ats.py` and get instant ATS analysis like real companies use!
