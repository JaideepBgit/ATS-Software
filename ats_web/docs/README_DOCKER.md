# 🐳 Docker Setup - Complete Guide

## ✅ YES! Docker is Fully Supported

The ATS application with job tracking is **100% ready for Docker**!

---

## 🚀 Fastest Way to Start

### One-Click Start
```bash
docker-build-and-run.bat
```

### Or Manual
```bash
docker-compose up --build -d
```

**Then open**: http://localhost

---

## 📦 What's Included

### ✅ Complete Application
- **Backend**: FastAPI with job tracking API
- **Frontend**: React with Job Tracker UI
- **Database**: Excel file for job applications
- **Dependencies**: All installed (including openpyxl)

### ✅ Data Persistence
- Excel file saved to: `./data/jobs_applied/`
- Survives container restarts
- Easy to backup
- Can edit while running

### ✅ Auto-Configuration
- Directories created automatically
- Excel file initialized on first use
- Health checks configured
- Restart policy set

---

## 📁 File Structure

### On Your Computer
```
d:\work\ATS_software_custom\ats_web\
├── docker-compose.yml          ✅ Volume mount configured
├── Dockerfile                  ✅ openpyxl included
├── docker-build-and-run.bat    ✅ Easy start script
├── docker-test-job-tracking.bat ✅ Test script
└── data/                       ✅ Persisted data
    └── jobs_applied/
        └── job_applicaiton.xlsx
```

### Inside Container
```
/app/
├── backend/
│   ├── main.py                 ✅ Job tracking endpoints
│   ├── job_tracker.py          ✅ Excel operations
│   └── data/                   ✅ Mounted from host
│       └── jobs_applied/
│           └── job_applicaiton.xlsx
└── frontend/
    └── build/                  ✅ React app
```

---

## 🎯 Quick Start Guide

### Step 1: Ensure Docker is Running
```bash
docker --version
```

### Step 2: Build and Start
```bash
cd d:\work\ATS_software_custom\ats_web
docker-compose up --build -d
```

### Step 3: Wait for Services
```bash
docker-compose logs -f
```

Wait for: `✅ All services started successfully!`

### Step 4: Access Application
- **Frontend**: http://localhost
- **Backend**: http://localhost:8000
- **Job Tracker**: Click button in top-right

### Step 5: Test Job Tracking
```bash
docker-test-job-tracking.bat
```

---

## 🔧 Docker Configuration

### docker-compose.yml
```yaml
version: '3.8'

services:
  ats-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ats-application
    ports:
      - "80:80"           # Frontend
      - "8000:8000"       # Backend API
    volumes:
      - ./data:/app/backend/data  # ✅ Data persistence
    environment:
      - LLM_URL=http://host.docker.internal:11434/v1
      - MODEL_NAME=qwen2.5:7b
      - PYTHONUNBUFFERED=1
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### Key Features
- ✅ **Volume Mount**: Data persists on host
- ✅ **Health Check**: Monitors backend
- ✅ **Auto Restart**: Restarts on failure
- ✅ **Host Access**: Can use Ollama on host

---

## 📊 Data Persistence

### Volume Mount (Configured!)
```yaml
volumes:
  - ./data:/app/backend/data
```

### What This Means
- Excel file saved to your computer
- Survives `docker-compose down`
- Can backup easily
- Can edit in Excel while container runs

### Excel File Location
**Host**: `d:\work\ATS_software_custom\ats_web\data\jobs_applied\job_applicaiton.xlsx`  
**Container**: `/app/backend/data/jobs_applied/job_applicaiton.xlsx`

---

## 🎮 Docker Commands

### Basic Operations
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose up --build -d

# View logs
docker-compose logs -f

# Check status
docker ps
```

### Data Management
```bash
# Backup Excel file
copy data\jobs_applied\job_applicaiton.xlsx backups\

# View Excel file
start data\jobs_applied\job_applicaiton.xlsx

# Check file in container
docker exec ats-application ls -la /app/backend/data/jobs_applied/
```

### Debugging
```bash
# Access container shell
docker exec -it ats-application bash

# View backend logs
docker-compose logs backend

# Test API
curl http://localhost:8000/api/job-applications

# Check health
docker inspect ats-application --format='{{.State.Health.Status}}'
```

---

## 🧪 Testing

### Automated Test
```bash
docker-test-job-tracking.bat
```

### Manual Test Steps
1. **Check container**: `docker ps`
2. **Open app**: http://localhost
3. **Click "Job Tracker"** button
4. **Log test application**
5. **Verify Excel file**: `dir data\jobs_applied\`

### API Test
```bash
# Test job tracking endpoints
curl http://localhost:8000/api/job-applications
curl http://localhost:8000/api/job-applications/statistics
```

---

## 🔍 Troubleshooting

### Container Won't Start

**Check Docker:**
```bash
docker --version
docker ps
```

**Check logs:**
```bash
docker-compose logs
```

**Rebuild:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Port Conflicts

**Error**: "Port 80 is already allocated"

**Solution**: Change port in docker-compose.yml
```yaml
ports:
  - "8080:80"  # Use 8080 instead
```

### Excel File Issues

**Not persisting:**
```bash
# Check volume mount
docker inspect ats-application | findstr Mounts
```

**Permission denied:**
```bash
# Fix permissions
docker exec ats-application chmod 777 /app/backend/data/jobs_applied/
```

### Frontend Not Updated

**Clear cache:**
- Browser: Ctrl+Shift+Delete
- Rebuild: `docker-compose build --no-cache`

---

## 📚 Documentation

### Docker-Specific
- **DOCKER_QUICK_START.md** - Quick start guide
- **DOCKER_JOB_TRACKING_GUIDE.md** - Complete Docker guide
- **README_DOCKER.md** - This file

### Job Tracking
- **START_HERE_JOB_TRACKING.md** - Feature quick start
- **JOB_TRACKING_FEATURE.md** - Complete feature docs
- **JOB_TRACKING_QUICK_REFERENCE.md** - Quick reference

### All Documentation
- **INDEX_JOB_TRACKING.md** - Complete index

---

## 🎯 Common Workflows

### Daily Use
```bash
# Morning: Start container
docker-compose up -d

# Use application all day
# (http://localhost)

# Evening: Stop container
docker-compose down
```

### Development
```bash
# Start with logs visible
docker-compose up

# Make code changes

# Rebuild and restart
docker-compose up --build
```

### Backup
```bash
# Manual backup
copy data\jobs_applied\job_applicaiton.xlsx backups\backup_%date%.xlsx

# Automated backup (create script)
# Schedule with Windows Task Scheduler
```

---

## 🚀 Production Deployment

### Recommended Configuration
```yaml
services:
  ats-app:
    restart: unless-stopped  # ✅ Auto-restart
    healthcheck:             # ✅ Health monitoring
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
    volumes:
      - ./data:/app/backend/data      # ✅ Data persistence
      - ./backups:/app/backups         # ✅ Backup location
```

### Monitoring
```bash
# Check health
docker inspect ats-application --format='{{.State.Health.Status}}'

# View logs
docker-compose logs --tail=100 -f

# Check resource usage
docker stats ats-application
```

---

## ✅ Verification Checklist

### Before Starting
- [ ] Docker Desktop installed
- [ ] Docker Desktop running
- [ ] Project files in place
- [ ] docker-compose.yml configured

### After Starting
- [ ] Container running (`docker ps`)
- [ ] Frontend accessible (http://localhost)
- [ ] Backend accessible (http://localhost:8000)
- [ ] "Job Tracker" button visible
- [ ] Can open Job Tracker modal
- [ ] Can log test application
- [ ] Excel file created
- [ ] Data persists after restart

---

## 🎊 You're Ready!

### Quick Start Commands
```bash
# Build and start
docker-compose up --build -d

# Test
docker-test-job-tracking.bat

# Access
start http://localhost
```

### Excel File
```
data\jobs_applied\job_applicaiton.xlsx
```

### Documentation
- Quick Start: **DOCKER_QUICK_START.md**
- Complete Guide: **DOCKER_JOB_TRACKING_GUIDE.md**
- Job Tracking: **START_HERE_JOB_TRACKING.md**

---

## 📞 Need Help?

1. **Quick Start**: DOCKER_QUICK_START.md
2. **Troubleshooting**: DOCKER_JOB_TRACKING_GUIDE.md
3. **Job Tracking**: JOB_TRACKING_FEATURE.md
4. **All Docs**: INDEX_JOB_TRACKING.md

---

**Everything is ready! Start Docker and begin tracking! 🐳🎯**

---

**Docker Version**: 3.8  
**Status**: ✅ Fully Configured  
**Data Persistence**: ✅ Enabled  
**Job Tracking**: ✅ Included  
**Ready to Use**: ✅ Yes!  
