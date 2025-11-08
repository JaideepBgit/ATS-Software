# 🎯 Simple ATS Matcher - Quick Start Guide

## What This Does

This is a **simple, powerful ATS (Applicant Tracking System)** that works exactly like the systems companies use to screen resumes. 

You provide:
- 📄 PDF resumes (in a folder)
- 📋 Job description (in a text file)

You get:
- ✅ Match scores for each resume
- 📊 Detailed skill analysis
- ❌ Missing required skills
- 🏆 Ranked candidate list

---

## ⚡ Quick Setup (3 Steps)

### Step 1: Install PyPDF2
```bash
pip install PyPDF2
```

### Step 2: Add Your Files
- Put PDF resumes in: `data/resumes/`
- Edit job description: `data/job_description.txt`

### Step 3: Run It
```bash
python simple_ats.py
```

**OR** just double-click: `RUN_ATS.bat`

---

## 📁 File Structure

```
ats_python_project/
│
├── simple_ats.py              ← Main ATS script
├── ats_config.txt             ← Configuration (paths, settings)
├── RUN_ATS.bat                ← Double-click to run
│
└── data/
    ├── resumes/               ← PUT YOUR PDF RESUMES HERE
    │   ├── resume1.pdf
    │   ├── resume2.pdf
    │   └── ...
    │
    └── job_description.txt    ← EDIT WITH YOUR JOB POSTING
```

---

## 🎨 Example Output

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
   • node
   • postgresql
   • fastapi
   • agile
   • restful

❌ MISSING REQUIRED SKILLS (3):
   • kubernetes
   • graphql
   • typescript

================================================================================
📈 SUMMARY - All Candidates
================================================================================

Rank   Score    Resume                                   Status
--------------------------------------------------------------------------------
1      78.5     john_doe_resume.pdf                      ✓ PASS
2      65.2     jane_smith_resume.pdf                    ✓ PASS
3      52.8     candidate_xyz.pdf                        ✗ FAIL

📊 Statistics:
   • Total Resumes:  3
   • Passed (≥60%):  2
   • Failed (<60%):  1
   • Average Score:  65.5%
   • Highest Score:  78.5%
   • Lowest Score:   52.8%
```

---

## ⚙️ Configuration

Edit `ats_config.txt` to customize:

```ini
# Path to folder containing resume PDFs
RESUME_FOLDER=./data/resumes

# Path to job description text file
JOB_DESCRIPTION_FILE=./data/job_description.txt

# Minimum match score to consider (0-100)
MIN_MATCH_SCORE=60
```

**Want to use different folders?** Just update these paths!

---

## 🧠 How It Works (Like Real ATS)

### 1. Skill Extraction
- Identifies technical skills, programming languages, tools
- Recognizes synonyms (JS = JavaScript, K8s = Kubernetes)
- Extracts from both resume and job description

### 2. Experience Matching
- Finds years of experience mentioned
- Compares against job requirements
- Calculates match percentage

### 3. Keyword Analysis
- Measures keyword overlap between resume and job
- Higher density = better match
- Considers context and relevance

### 4. Scoring Algorithm
```
Overall Score = (Skills × 50%) + (Experience × 20%) + (Keywords × 30%)
```

**Score Ratings:**
- 🟢 80-100%: Excellent Match
- 🟡 60-79%: Good Match
- 🟠 40-59%: Moderate Match
- 🔴 0-39%: Poor Match

---

## 💡 Tips for Best Results

### For Job Descriptions:
✅ List specific skills and technologies
✅ Mention required years of experience
✅ Use industry-standard terminology
✅ Include both required and preferred skills

### For Resumes:
✅ Use standard PDF format (not scanned images)
✅ Include relevant keywords from job posting
✅ Clearly state years of experience
✅ List technical skills explicitly

---

## 🔧 Customization

### Add Custom Skills

Edit `simple_ats.py` and add to `skill_synonyms`:

```python
self.skill_synonyms = {
    'python': ['python', 'py', 'python3'],
    'your_skill': ['skill', 'synonym1', 'synonym2'],
    # Add more...
}
```

### Change Scoring Weights

Modify in `calculate_match_score` method:

```python
overall_score = (
    skill_match_pct * 0.5 +      # Skills: 50%
    exp_match_pct * 0.2 +         # Experience: 20%
    keyword_density * 0.3         # Keywords: 30%
)
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| "No PDF files found" | Add PDFs to `data/resumes/` folder |
| "Job description file not found" | Create/edit `data/job_description.txt` |
| "Could not extract text" | PDF might be scanned - needs text-based PDF |
| "Module not found: PyPDF2" | Run: `pip install PyPDF2` |
| Low scores | Ensure resume uses same terms as job description |

---

## 🚀 Real-World Usage

### Scenario 1: Hiring Manager
1. Get job description from HR
2. Paste into `data/job_description.txt`
3. Collect candidate resumes in `data/resumes/`
4. Run ATS to get ranked list
5. Interview top-scoring candidates

### Scenario 2: Job Seeker
1. Find job posting you want to apply for
2. Save as `data/job_description.txt`
3. Put your resume in `data/resumes/`
4. Run ATS to see your match score
5. Update resume to include missing skills

### Scenario 3: Recruiter
1. Process multiple positions
2. Create separate folders for each role
3. Update config paths for each run
4. Compare candidates across positions

---

## 📊 Understanding Your Results

### High Score (80%+)
- Strong skill alignment
- Meets experience requirements
- Good keyword match
- **Action:** Priority candidate for interview

### Good Score (60-79%)
- Most required skills present
- Close to experience requirements
- Decent keyword coverage
- **Action:** Consider for interview

### Moderate Score (40-59%)
- Some skills missing
- May lack experience
- Lower keyword match
- **Action:** Review manually, might need training

### Low Score (<40%)
- Many missing skills
- Insufficient experience
- Poor keyword alignment
- **Action:** Likely not a good fit

---

## 🎯 Next Steps

1. **Test it:** Run with sample data first
2. **Customize:** Add your industry-specific skills
3. **Iterate:** Adjust scoring weights for your needs
4. **Scale:** Process hundreds of resumes instantly

---

## 📝 Notes

- This is a **local tool** - your data stays on your computer
- No API keys or cloud services needed
- Works offline
- Fast processing (seconds per resume)
- Completely customizable

---

**Ready to start?** Just run:
```bash
python simple_ats.py
```

Or double-click: **RUN_ATS.bat**

Happy hiring! 🎉
