# Job Tracking - Quick Reference Card

## 🚀 Quick Start

```bash
# 1. Install dependency
cd backend && pip install openpyxl

# 2. Restart backend
python main.py

# 3. Open app
http://localhost:3000

# 4. Click "Job Tracker" button (top-right)
```

## 📍 Key Locations

| Item | Location |
|------|----------|
| **Excel File** | `data/jobs_applied/job_applicaiton.xlsx` |
| **Backend Module** | `backend/job_tracker.py` |
| **Frontend Component** | `frontend/src/components/JobTracking.js` |
| **API Base** | `http://localhost:8000/api/` |

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/job-application` | Log new application |
| GET | `/api/job-applications` | Get all applications |
| GET | `/api/job-applications/recent?limit=10` | Get recent apps |
| GET | `/api/job-applications/statistics` | Get stats |
| GET | `/api/job-applications/check` | Check if applied |

## 📊 Excel Columns

```
Company | Job | Portal | Full Time | Date Applied
```

## 🎯 Portal Options

- LinkedIn
- Indeed
- Glassdoor
- Company Website
- Referral
- Recruiter
- Other

## 💼 Employment Types

- Full Time
- Part Time
- Contract
- Freelance
- Internship

## 🔧 Common Commands

```bash
# Install dependency
pip install openpyxl

# Check if installed
pip show openpyxl

# Restart backend
cd backend && python main.py

# Restart with Docker
docker-compose restart backend

# View Excel file
start data/jobs_applied/job_applicaiton.xlsx
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Module not found** | `pip install openpyxl` |
| **Excel not created** | Check `data/jobs_applied/` exists |
| **Button not showing** | Clear cache, restart frontend |
| **API error** | Check backend logs |
| **Can't open Excel** | Close Excel if already open |

## 📝 Usage Patterns

### Pattern 1: Quick Log
```
1. Analyze resume
2. Click "Job Tracker"
3. Click "Yes, Log Application"
4. Submit
```

### Pattern 2: Manual Entry
```
1. Click "Job Tracker"
2. Click "+ Add New"
3. Fill form
4. Submit
```

### Pattern 3: View Stats
```
1. Click "Job Tracker"
2. View statistics dashboard
3. Check portal breakdown
```

## 🎨 UI Elements

| Element | Description |
|---------|-------------|
| **Job Tracker Button** | Top-right corner, purple |
| **Statistics Cards** | Total, Recent, Portals |
| **Quick Add Prompt** | Green box with job info |
| **Application Form** | Gray box with inputs |
| **Applications Table** | White table with rows |

## 📈 Statistics Shown

- Total Applications (all-time)
- Recent Applications (last 7 days)
- Portals Used (count)
- By Portal (breakdown)
- By Type (breakdown)

## 🔄 Data Flow

```
User → Frontend → API → Backend → Excel
                                    ↓
User ← Frontend ← API ← Backend ← Excel
```

## 💡 Pro Tips

1. **Log immediately** after applying
2. **Use consistent names** for companies
3. **Check statistics** weekly
4. **Backup Excel file** regularly
5. **Edit in Excel** if needed

## 🎯 Key Features

✅ Auto-fill from job description  
✅ Duplicate detection  
✅ Statistics dashboard  
✅ Excel integration  
✅ Recent applications view  
✅ Portal tracking  

## 📞 Help Resources

| Resource | Location |
|----------|----------|
| **Full Docs** | `JOB_TRACKING_FEATURE.md` |
| **Setup Guide** | `SETUP_JOB_TRACKING.md` |
| **Architecture** | `JOB_TRACKING_ARCHITECTURE.md` |
| **Update Summary** | `UPDATE_SUMMARY_JOB_TRACKING.md` |

## 🔑 Important Notes

- Excel file created automatically
- All dates in YYYY-MM-DD format
- Applications sorted by date (newest first)
- No external dependencies (local only)
- Works offline

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Close Modal | `Esc` |
| Submit Form | `Enter` |

## 📦 Dependencies

```
Backend:
- openpyxl==3.1.2

Frontend:
- (No new dependencies)
```

## 🎨 Color Scheme

- **Primary**: Purple (#667eea)
- **Secondary**: Light Purple (#967CB2)
- **Success**: Green (#4caf50)
- **Warning**: Yellow (#ffc107)

## 📊 Sample Data

```json
{
  "company": "Google",
  "job_title": "Senior Software Engineer",
  "portal": "LinkedIn",
  "employment_type": "Full Time"
}
```

## 🔍 Search & Filter

Currently not available in UI, but you can:
- Open Excel file
- Use Excel's filter features
- Sort by any column

## 🎯 Success Metrics

Track your job search:
- Applications per week
- Response rate by portal
- Most used portals
- Application trends

## 🚨 Error Messages

| Error | Meaning |
|-------|---------|
| "Module not found" | Install openpyxl |
| "File not found" | Excel file not created |
| "Permission denied" | Check file permissions |
| "Already applied" | Duplicate detected |

## 📱 Mobile Support

✅ Responsive design  
✅ Touch-friendly  
✅ Scrollable tables  
✅ Mobile-optimized forms  

---

**Keep this card handy for quick reference! 📌**
