# Job Tracking Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐         ┌─────────────────────────────────┐  │
│  │   App.js     │────────▶│   JobTracking Component         │  │
│  │              │         │                                 │  │
│  │ - Job Tracker│         │ - Statistics Dashboard          │  │
│  │   Button     │         │ - Application Form              │  │
│  │ - Modal State│         │ - Applications List             │  │
│  └──────────────┘         │ - Duplicate Detection           │  │
│                           └─────────────────────────────────┘  │
│                                        │                         │
│                                        │ HTTP Requests           │
│                                        ▼                         │
└────────────────────────────────────────────────────────────────┘
                                         │
                                         │
┌────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                      main.py                              │ │
│  │                                                            │ │
│  │  API Endpoints:                                           │ │
│  │  • POST   /api/job-application                           │ │
│  │  • GET    /api/job-applications                          │ │
│  │  • GET    /api/job-applications/recent                   │ │
│  │  • GET    /api/job-applications/statistics               │ │
│  │  • GET    /api/job-applications/check                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                           │                                     │
│                           │ Uses                                │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  job_tracker.py                           │ │
│  │                                                            │ │
│  │  JobTracker Class:                                        │ │
│  │  • add_job_application()                                 │ │
│  │  • get_all_applications()                                │ │
│  │  • get_recent_applications()                             │ │
│  │  • get_statistics()                                      │ │
│  │  • check_if_applied()                                    │ │
│  └──────────────────────────────────────────────────────────┘ │
│                           │                                     │
│                           │ Reads/Writes                        │
│                           ▼                                     │
└────────────────────────────────────────────────────────────────┘
                            │
                            │
┌────────────────────────────────────────────────────────────────┐
│                    Data Storage (Excel)                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📁 data/jobs_applied/job_applicaiton.xlsx                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Company │ Job │ Portal │ Full Time │ Date Applied      │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ Google  │ SWE │ LinkedIn│ Full Time │ 2025-11-10       │   │
│  │ Microsoft│ Dev│ Indeed  │ Full Time │ 2025-11-09       │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Log Application Flow

```
User Action                Frontend                Backend                Excel
───────────              ──────────              ─────────              ──────

Click "Log              JobTracking
Application"            Component
    │                        │
    │                        │ POST /api/job-application
    │                        │ {company, job_title, ...}
    │                        ├──────────────────────────▶ main.py
    │                        │                                │
    │                        │                                │ job_tracker.
    │                        │                                │ add_job_application()
    │                        │                                ├────────────▶ job_tracker.py
    │                        │                                │                   │
    │                        │                                │                   │ openpyxl
    │                        │                                │                   │ write
    │                        │                                │                   ├────────▶ Excel File
    │                        │                                │                   │          (append row)
    │                        │                                │                   │
    │                        │                                │ ◀────────────────┤
    │                        │                                │ Success response
    │                        │ ◀──────────────────────────────┤
    │                        │ {success: true, ...}
    │                        │
    │ ◀──────────────────────┤
    │ Show success message
    │
```

### 2. View Applications Flow

```
User Action                Frontend                Backend                Excel
───────────              ──────────              ─────────              ──────

Click "Job              JobTracking
Tracker"                Component
    │                        │
    │                        │ GET /api/job-applications
    │                        ├──────────────────────────▶ main.py
    │                        │                                │
    │                        │                                │ job_tracker.
    │                        │                                │ get_all_applications()
    │                        │                                ├────────────▶ job_tracker.py
    │                        │                                │                   │
    │                        │                                │                   │ openpyxl
    │                        │                                │                   │ read
    │                        │                                │                   ├────────▶ Excel File
    │                        │                                │                   │          (read rows)
    │                        │                                │                   │
    │                        │                                │ ◀────────────────┤
    │                        │                                │ Applications list
    │                        │ ◀──────────────────────────────┤
    │                        │ {applications: [...]}
    │                        │
    │ ◀──────────────────────┤
    │ Display applications
    │
```

### 3. Statistics Flow

```
User Action                Frontend                Backend                Excel
───────────              ──────────              ─────────              ──────

Open Modal              JobTracking
                        Component
    │                        │
    │                        │ GET /api/job-applications/statistics
    │                        ├──────────────────────────▶ main.py
    │                        │                                │
    │                        │                                │ job_tracker.
    │                        │                                │ get_statistics()
    │                        │                                ├────────────▶ job_tracker.py
    │                        │                                │                   │
    │                        │                                │                   │ Read & Calculate
    │                        │                                │                   ├────────▶ Excel File
    │                        │                                │                   │          - Count total
    │                        │                                │                   │          - Group by portal
    │                        │                                │                   │          - Count recent
    │                        │                                │                   │
    │                        │                                │ ◀────────────────┤
    │                        │                                │ Statistics object
    │                        │ ◀──────────────────────────────┤
    │                        │ {total: 10, by_portal: {...}}
    │                        │
    │ ◀──────────────────────┤
    │ Display statistics
    │
```

## 🧩 Component Structure

### Frontend Components

```
App.js
├── JobTracking Modal (conditional)
│   ├── Header
│   │   ├── Title
│   │   └── Close Button
│   │
│   ├── Statistics Section
│   │   ├── Stats Grid
│   │   │   ├── Total Applications Card
│   │   │   ├── Recent 7 Days Card
│   │   │   └── Portals Used Card
│   │   │
│   │   └── Portal Breakdown
│   │       └── Portal Items List
│   │
│   ├── Quick Add Section (conditional)
│   │   └── Application Prompt
│   │       └── "Yes, Log Application" Button
│   │
│   ├── Application Form (conditional)
│   │   ├── Company Input
│   │   ├── Job Title Input
│   │   ├── Portal Select
│   │   ├── Employment Type Select
│   │   └── Form Actions
│   │       ├── Cancel Button
│   │       └── Submit Button
│   │
│   ├── Applications List
│   │   ├── List Header
│   │   │   ├── Title
│   │   │   └── "+ Add New" Button
│   │   │
│   │   └── Applications Table
│   │       ├── Table Header
│   │       └── Table Rows
│   │
│   └── Excel Info
│       └── File Location
│
└── Job Tracker Button (AppBar)
```

### Backend Modules

```
main.py
├── JobApplicationRequest (Pydantic Model)
├── job_tracker (Instance)
└── API Endpoints
    ├── POST /api/job-application
    ├── GET /api/job-applications
    ├── GET /api/job-applications/recent
    ├── GET /api/job-applications/statistics
    └── GET /api/job-applications/check

job_tracker.py
└── JobTracker (Class)
    ├── __init__()
    ├── _ensure_excel_exists()
    ├── add_job_application()
    ├── get_application_count()
    ├── check_if_applied()
    ├── get_recent_applications()
    ├── get_all_applications()
    └── get_statistics()
```

## 📊 Data Models

### Frontend State

```javascript
// App.js
{
  showJobTracking: boolean,
  companyName: string,
  roleName: string
}

// JobTracking.js
{
  applications: Array<Application>,
  statistics: Statistics,
  loading: boolean,
  showForm: boolean,
  formData: FormData,
  alreadyApplied: boolean
}
```

### Backend Models

```python
# JobApplicationRequest
{
  company: str,
  job_title: str,
  portal: str = "LinkedIn",
  employment_type: str = "Full Time"
}

# Application (from Excel)
{
  company: str,
  job: str,
  portal: str,
  type: str,
  date: str
}

# Statistics
{
  total: int,
  by_portal: Dict[str, int],
  by_type: Dict[str, int],
  recent_7_days: int
}
```

## 🔌 API Contract

### POST /api/job-application

**Request:**
```json
{
  "company": "string",
  "job_title": "string",
  "portal": "string",
  "employment_type": "string"
}
```

**Response:**
```json
{
  "success": true,
  "company": "string",
  "job_title": "string",
  "portal": "string",
  "employment_type": "string",
  "date_applied": "YYYY-MM-DD",
  "total_applications": 0
}
```

### GET /api/job-applications

**Response:**
```json
{
  "applications": [
    {
      "company": "string",
      "job": "string",
      "portal": "string",
      "type": "string",
      "date": "YYYY-MM-DD"
    }
  ],
  "total": 0
}
```

### GET /api/job-applications/statistics

**Response:**
```json
{
  "total": 0,
  "by_portal": {
    "LinkedIn": 0,
    "Indeed": 0
  },
  "by_type": {
    "Full Time": 0,
    "Contract": 0
  },
  "recent_7_days": 0
}
```

## 🎨 Styling Architecture

```
JobTracking.css
├── Layout
│   ├── .job-tracking-overlay (Full screen overlay)
│   ├── .job-tracking-modal (Centered modal)
│   └── .job-tracking-content (Scrollable content)
│
├── Components
│   ├── Statistics
│   │   ├── .statistics-section
│   │   ├── .stats-grid
│   │   ├── .stat-card
│   │   └── .portal-breakdown
│   │
│   ├── Forms
│   │   ├── .application-form
│   │   ├── .form-group
│   │   └── .form-actions
│   │
│   └── Lists
│       ├── .applications-list
│       ├── .applications-table
│       └── .portal-badge
│
└── Utilities
    ├── Buttons (.btn-primary, .btn-secondary)
    ├── Notices (.already-applied-notice)
    └── Responsive (@media queries)
```

## 🔄 State Management

### Frontend State Flow

```
Initial Load
    │
    ├─▶ Load Applications (GET /api/job-applications)
    ├─▶ Load Statistics (GET /api/job-applications/statistics)
    └─▶ Check If Applied (GET /api/job-applications/check)
    
User Logs Application
    │
    ├─▶ Submit Form (POST /api/job-application)
    ├─▶ Reload Applications
    ├─▶ Reload Statistics
    └─▶ Update Already Applied Flag

User Opens Modal
    │
    ├─▶ Fetch Latest Data
    └─▶ Render Components
```

## 🗄️ Database Schema (Excel)

```
Sheet: "Jobs Applied"

Columns:
┌──────────┬──────────┬──────────┬───────────┬──────────────┐
│ Company  │   Job    │  Portal  │ Full Time │ Date Applied │
│ (Text)   │ (Text)   │ (Text)   │  (Text)   │   (Date)     │
├──────────┼──────────┼──────────┼───────────┼──────────────┤
│ Google   │ SWE      │ LinkedIn │ Full Time │ 2025-11-10   │
│ Microsoft│ Dev      │ Indeed   │ Full Time │ 2025-11-09   │
└──────────┴──────────┴──────────┴───────────┴──────────────┘

Indexes:
- Row 1: Headers
- Row 2+: Data

Operations:
- Append: Add new row at end
- Read: Iterate all rows
- Search: Linear search through rows
```

## 🔐 Security Considerations

```
Frontend
├── Input Validation
│   ├── Required fields checked
│   ├── String length limits
│   └── XSS prevention (React auto-escapes)
│
Backend
├── Request Validation
│   ├── Pydantic models
│   ├── Type checking
│   └── Required field validation
│
└── File Operations
    ├── Path validation
    ├── Permission checks
    └── Error handling

Excel File
└── Local Storage
    ├── No external access
    ├── Server-side only
    └── File permissions respected
```

## 📈 Performance Characteristics

```
Operation                    Time Complexity    Space Complexity
─────────────────────────────────────────────────────────────────
Add Application              O(1)               O(1)
Get All Applications         O(n)               O(n)
Get Recent Applications      O(n)               O(k) where k=limit
Get Statistics              O(n)               O(p+t) where p=portals, t=types
Check If Applied            O(n)               O(1)

Where n = total number of applications
```

## 🎯 Integration Points

```
ATS Web Application
├── Job Description Module
│   └── Provides company name and role name
│
├── Resume Analysis Module
│   └── Triggers "Did you apply?" prompt
│
└── Job Tracking Module (NEW)
    ├── Receives job details
    ├── Logs applications
    └── Provides statistics
```

---

This architecture provides a clean separation of concerns, scalable design, and maintainable codebase for the job tracking feature.
