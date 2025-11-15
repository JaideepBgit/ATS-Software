# Interactive ATS with Job Application Tracking

## Overview

This enhanced version of the Interactive ATS keeps your resume in session and automatically tracks job applications in an Excel spreadsheet.

## Features

✅ **Session-Based Resume Management**
- Load your resume once and keep it in memory
- Analyze multiple jobs without re-uploading
- Replace resume anytime during the session

✅ **Automatic Job Application Tracking**
- After each analysis, you're asked if you applied
- Job details are automatically extracted from the description
- All applications are logged in Excel with timestamps

✅ **Excel Integration**
- Tracks: Company, Job Title, Portal, Employment Type, Date Applied
- Located at: `data/jobs_applied/job_applicaiton.xlsx`
- Automatically created if it doesn't exist
- Easy to view and edit in Excel

✅ **AI-Powered Insights**
- Get detailed resume analysis
- Ask questions about your match score
- Receive improvement suggestions
- Compare your skills to job requirements

## Installation

1. Install required packages:
```bash
pip install -r requirements_advanced.txt
```

2. Set up your API configuration:
   - For OpenAI/LM Studio: Edit `ats_config.txt`
   - For Ollama: Edit `ats_config_ollama.txt`

## Usage

### Option 1: OpenAI / LM Studio

Run the batch file:
```bash
RUN_INTERACTIVE_ATS_WITH_TRACKING.bat
```

Or run directly:
```bash
python interactive_ats_with_tracking.py
```

### Option 2: Ollama (Local)

Make sure Ollama is running:
```bash
ollama serve
```

Run the batch file:
```bash
RUN_INTERACTIVE_ATS_WITH_TRACKING_OLLAMA.bat
```

Or run directly:
```bash
python interactive_ats_with_tracking_ollama.py
```

## Workflow

### 1. Load Your Resume
```
Enter path to your resume PDF: data/resumes/my_resume.pdf
✅ Resume loaded: my_resume.pdf
```

### 2. Main Menu
```
📋 MAIN MENU
Current resume: my_resume.pdf
Applications tracked: 5

Options:
  1. Analyze a new job
  2. Replace resume
  3. View recent applications
  4. Ask questions about last analysis
  5. Quit
```

### 3. Analyze a Job
- Paste the job description
- Press Enter twice when done
- Get detailed analysis with match score

### 4. Track Application
```
📝 JOB APPLICATION TRACKING
❓ Did you apply for this job? (yes/no): yes

📋 Logging job application...
   Company: Google
   Job Title: Senior Software Engineer

Edit details? (yes/no): no
Portal [LinkedIn]: 
Employment Type [Full Time]: 

✅ Job application logged!
   Company: Google
   Position: Senior Software Engineer
   Portal: LinkedIn
   Type: Full Time
   Date: 2025-11-10

🎯 Total applications tracked: 6
```

### 5. View Applications
```
📊 RECENT JOB APPLICATIONS
Total applications: 6

Recent applications:
1. Senior Software Engineer at Google
   Portal: LinkedIn | Type: Full Time | Date: 2025-11-10

2. Backend Developer at Microsoft
   Portal: LinkedIn | Type: Full Time | Date: 2025-11-09
```

### 6. Ask Questions
```
💬 Q&A SESSION
Score: 85%
Recommendation: Strong Match

❓ Your question: How can I improve my score?

🤖 AI Response:
To improve your score from 85% to 90%+, focus on:
1. Add more specific examples of cloud architecture...
2. Quantify your achievements with metrics...
3. Highlight leadership experience more prominently...
```

## Excel File Structure

The tracking spreadsheet (`job_applicaiton.xlsx`) has these columns:

| Company | Job | Portal | Full Time | Date Applied |
|---------|-----|--------|-----------|--------------|
| Google | Senior Software Engineer | LinkedIn | Full Time | 2025-11-10 |
| Microsoft | Backend Developer | LinkedIn | Full Time | 2025-11-09 |

## Features in Detail

### Resume Session Management
- Your resume stays loaded throughout the session
- No need to re-upload for each job analysis
- Can replace resume anytime if needed
- Supports drag-and-drop paths (with quotes)

### Automatic Job Info Extraction
- AI automatically extracts company name and job title
- You can edit the extracted information
- Defaults to "Unknown Company" / "Unknown Position" if extraction fails

### Duplicate Detection
- Checks if you've already logged the same job
- Warns you before creating duplicate entries
- Option to log again if needed

### Application History
- View your 10 most recent applications
- See total application count
- Track which portals you're using most
- Monitor your job search progress

## Tips

1. **Keep Resume Updated**: Replace your resume when you make updates
2. **Consistent Naming**: Use consistent company names for better tracking
3. **Portal Tracking**: Track different portals (LinkedIn, Indeed, Company Site)
4. **Regular Reviews**: Check your Excel file to see application patterns
5. **Backup**: Keep backups of your `job_applicaiton.xlsx` file

## Troubleshooting

### Resume Not Loading
- Check file path is correct
- Remove quotes if copy-pasted
- Ensure PDF is not corrupted
- Try absolute path: `C:\Users\...\resume.pdf`

### Excel File Issues
- File is created automatically on first use
- Located at: `ats_python_project/data/jobs_applied/job_applicaiton.xlsx`
- Close Excel if file is open when running the program
- Check folder permissions

### AI Not Responding
- Verify API key in config file
- For Ollama: Ensure `ollama serve` is running
- Check internet connection (for OpenAI)
- Try a different model

### Job Info Not Extracted
- Paste complete job description
- Include company name in description
- Edit manually when prompted
- AI extraction works best with structured job posts

## Advanced Usage

### Custom Portal Names
When logging an application, you can specify any portal:
- LinkedIn
- Indeed
- Glassdoor
- Company Website
- Referral
- Recruiter

### Employment Types
Customize the employment type:
- Full Time
- Part Time
- Contract
- Freelance
- Internship

### Batch Analysis
You can analyze multiple jobs in one session:
1. Load resume once
2. Analyze job 1 → Log application
3. Analyze job 2 → Log application
4. Continue...

## Files Created

```
ats_python_project/
├── interactive_ats_with_tracking.py          # Main script (OpenAI/LM Studio)
├── interactive_ats_with_tracking_ollama.py   # Ollama version
├── job_tracker.py                            # Excel tracking module
├── data/
│   └── jobs_applied/
│       └── job_applicaiton.xlsx              # Your application log
```

## Integration with Existing ATS

This tool works alongside your existing ATS setup:
- Uses same config files (`ats_config.txt`)
- Uses same resume folder structure
- Compatible with all existing features
- Can run independently or alongside other ATS tools

## Future Enhancements

Potential additions:
- Export to CSV
- Application statistics dashboard
- Follow-up reminders
- Interview tracking
- Offer tracking
- Rejection analysis

## Support

For issues or questions:
1. Check this README
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check config files are set up correctly

## License

Same as the main ATS project.
