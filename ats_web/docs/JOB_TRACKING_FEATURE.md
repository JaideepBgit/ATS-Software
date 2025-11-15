# Job Application Tracking Feature

## 🎉 New Feature Added!

The ATS Web Application now includes a comprehensive **Job Application Tracker** that helps you keep track of all your job applications in one place.

## ✨ Features

### 📊 Application Dashboard
- View all your job applications in one place
- See statistics: total applications, recent applications, portals used
- Track applications by portal (LinkedIn, Indeed, Glassdoor, etc.)
- Monitor your job search progress

### 📝 Quick Logging
- After analyzing a resume, you're prompted to log the application
- Auto-fills company name and job title from the job description
- One-click logging with customizable details

### 📈 Statistics & Analytics
- Total applications count
- Applications in the last 7 days
- Breakdown by job portal
- Breakdown by employment type

### 💾 Excel Integration
- All applications saved to Excel: `data/jobs_applied/job_applicaiton.xlsx`
- Easy to open and edit in Excel
- Columns: Company, Job Title, Portal, Employment Type, Date Applied

### 🔍 Duplicate Detection
- Warns you if you've already logged an application
- Prevents duplicate entries
- Option to log again if needed

## 🚀 How to Use

### 1. Access Job Tracker

Click the **"Job Tracker"** button in the top-right corner of the application.

### 2. View Your Applications

The Job Tracker modal shows:
- **Statistics Dashboard**: Overview of your applications
- **Recent Applications**: List of your most recent applications
- **Quick Add**: Prompt to log current job if applicable

### 3. Log a New Application

**Option A: After Resume Analysis**
1. Upload a resume and analyze it
2. Click "Job Tracker" button
3. You'll see a prompt: "Did you apply for this job?"
4. Click "Yes, Log Application"
5. Review/edit the details
6. Click "Log Application"

**Option B: Manual Entry**
1. Click "Job Tracker" button
2. Click "+ Add New" button
3. Fill in the form:
   - Company Name
   - Job Title
   - Portal (LinkedIn, Indeed, etc.)
   - Employment Type (Full Time, Part Time, etc.)
4. Click "Log Application"

### 4. View Statistics

The dashboard shows:
- **Total Applications**: All-time count
- **Last 7 Days**: Recent activity
- **Portals Used**: Number of different portals
- **By Portal**: Breakdown of applications per portal

### 5. Review Application History

Scroll down to see a table of all your applications with:
- Company name
- Job title
- Portal used
- Employment type
- Date applied

## 📋 API Endpoints

The following endpoints have been added to the backend:

### POST `/api/job-application`
Log a new job application
```json
{
  "company": "Google",
  "job_title": "Senior Software Engineer",
  "portal": "LinkedIn",
  "employment_type": "Full Time"
}
```

### GET `/api/job-applications`
Get all job applications

### GET `/api/job-applications/recent?limit=10`
Get recent applications (default: 10)

### GET `/api/job-applications/statistics`
Get application statistics

### GET `/api/job-applications/check?company=Google&job_title=Engineer`
Check if already applied to a specific job

## 🗂️ File Structure

```
ats_web/
├── backend/
│   ├── job_tracker.py          # Job tracking logic
│   ├── main.py                 # Updated with tracking endpoints
│   └── requirements.txt        # Added openpyxl
├── frontend/
│   └── src/
│       └── components/
│           ├── JobTracking.js  # Job tracking component
│           └── JobTracking.css # Styling
└── data/
    └── jobs_applied/
        └── job_applicaiton.xlsx # Excel tracking file
```

## 🔧 Installation

### Backend Setup

1. Install the new dependency:
```bash
cd backend
pip install openpyxl
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Frontend Setup

No additional dependencies needed! The component uses existing React libraries.

## 🐳 Docker Setup

If using Docker, the setup is automatic:

1. Rebuild the containers:
```bash
docker-compose down
docker-compose up --build
```

The Excel file will be created automatically in the `data/jobs_applied/` directory.

## 💡 Usage Tips

### Best Practices

1. **Log Immediately**: Log applications right after submitting them
2. **Consistent Naming**: Use consistent company names (e.g., "Google" not "Google Inc.")
3. **Portal Tracking**: Track which portals work best for you
4. **Regular Reviews**: Check your statistics weekly to monitor progress
5. **Excel Backup**: Regularly backup your `job_applicaiton.xlsx` file

### Portal Options

- LinkedIn
- Indeed
- Glassdoor
- Company Website
- Referral
- Recruiter
- Other

### Employment Types

- Full Time
- Part Time
- Contract
- Freelance
- Internship

## 📊 Excel File Format

The Excel file has the following structure:

| Company | Job | Portal | Full Time | Date Applied |
|---------|-----|--------|-----------|--------------|
| Google | Senior Software Engineer | LinkedIn | Full Time | 2025-11-10 |
| Microsoft | Backend Developer | Indeed | Full Time | 2025-11-09 |

You can open this file in Excel, Google Sheets, or any spreadsheet application.

## 🔍 Troubleshooting

### Excel File Not Created

**Issue**: The Excel file doesn't exist

**Solution**: 
- The file is created automatically on first use
- Check that the `data/jobs_applied/` directory exists
- Ensure the backend has write permissions

### Can't Log Application

**Issue**: Error when trying to log an application

**Solution**:
- Check that the backend is running
- Verify the API endpoint is accessible
- Check browser console for errors
- Ensure openpyxl is installed: `pip install openpyxl`

### Duplicate Warning

**Issue**: Getting duplicate warning when it's not a duplicate

**Solution**:
- Check for slight differences in company name or job title
- Use consistent naming (e.g., "Google" vs "Google LLC")
- You can still log it again if needed

### Statistics Not Showing

**Issue**: Statistics dashboard is empty

**Solution**:
- Log at least one application first
- Refresh the Job Tracker modal
- Check that the Excel file exists and is readable

## 🎨 Customization

### Change Excel File Location

Edit `backend/job_tracker.py`:
```python
def __init__(self, excel_path: str = "your/custom/path/jobs.xlsx"):
```

### Add More Portal Options

Edit `frontend/src/components/JobTracking.js`:
```javascript
<option value="YourPortal">Your Portal</option>
```

### Modify Statistics

Edit `backend/job_tracker.py` in the `get_statistics()` method to add custom metrics.

## 📈 Future Enhancements

Potential additions:
- Interview tracking
- Follow-up reminders
- Application status updates
- Response rate analytics
- Salary tracking
- Export to CSV
- Email notifications
- Calendar integration

## 🤝 Integration with Existing Features

The Job Tracker integrates seamlessly with:
- **Resume Analysis**: Auto-fills company and job title
- **Job Description**: Uses stored job details
- **Results View**: Access from any page via top button

## 📝 Notes

- The Excel file is stored locally on the server
- All dates are in YYYY-MM-DD format
- Applications are sorted by date (most recent first)
- The tracker works offline (no external dependencies)
- Data persists across server restarts

## 🎯 Benefits

1. **Organized**: Keep all applications in one place
2. **Trackable**: Monitor your job search progress
3. **Insightful**: See which portals work best
4. **Efficient**: Quick logging after each application
5. **Portable**: Excel file can be shared or backed up
6. **Professional**: Maintain a professional application log

## 🔐 Privacy

- All data is stored locally on your server
- No external services or APIs used
- Excel file is only accessible to you
- No data is sent to third parties

---

**Happy Job Hunting! 🎉**

For questions or issues, check the troubleshooting section or review the code in `backend/job_tracker.py` and `frontend/src/components/JobTracking.js`.
