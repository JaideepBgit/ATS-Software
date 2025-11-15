# Quick Start: Job Application Tracking

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install openpyxl
```

Or install all requirements:
```bash
pip install -r requirements_advanced.txt
```

### Step 2: Run the Program

**For OpenAI/LM Studio:**
```bash
RUN_INTERACTIVE_ATS_WITH_TRACKING.bat
```

**For Ollama:**
```bash
RUN_INTERACTIVE_ATS_WITH_TRACKING_OLLAMA.bat
```

### Step 3: Follow the Prompts

1. **Load your resume** (one time)
2. **Paste job description** (for each job)
3. **Answer if you applied** (yes/no)
4. **Done!** Application is logged in Excel

## 📊 View Your Applications

Open the Excel file:
```
ats_python_project/data/jobs_applied/job_applicaiton.xlsx
```

## 💡 Example Session

```
Enter path to your resume PDF: data/my_resume.pdf
✅ Resume loaded

📋 MAIN MENU
1. Analyze a new job
Select option: 1

🔍 ANALYZE NEW JOB
[Paste job description]
[Press Enter twice]

⏳ Analyzing...
✅ Analysis complete!
Score: 85% - Strong Match

📝 JOB APPLICATION TRACKING
❓ Did you apply for this job? yes

✅ Job application logged!
   Company: Google
   Position: Senior Software Engineer
   Portal: LinkedIn
   Date: 2025-11-10

🎯 Total applications tracked: 1
```

## 🎯 Key Features

- ✅ Resume stays in session
- ✅ Analyze unlimited jobs
- ✅ Auto-track applications
- ✅ Excel spreadsheet logging
- ✅ AI-powered insights

## 📝 Excel Columns

| Company | Job | Portal | Full Time | Date Applied |
|---------|-----|--------|-----------|--------------|
| Auto-filled from job description | | LinkedIn (default) | Full Time (default) | Auto-added |

## 🔄 Typical Workflow

```
Load Resume → Analyze Job → Apply? → Log → Repeat
```

## ⚙️ Configuration

Edit these files before first run:
- `ats_config.txt` (for OpenAI/LM Studio)
- `ats_config_ollama.txt` (for Ollama)

Add your API key or Ollama endpoint.

## 🆘 Common Issues

**Resume won't load?**
- Use full path: `C:\Users\YourName\Documents\resume.pdf`
- Remove quotes from path

**Excel file not found?**
- It's created automatically on first use
- Location: `data/jobs_applied/job_applicaiton.xlsx`

**AI not responding?**
- Check API key in config file
- For Ollama: Run `ollama serve` first

## 📚 More Info

See `JOB_TRACKING_README.md` for complete documentation.

---

**That's it! Start tracking your job applications today! 🎉**
