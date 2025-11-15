# 🐳 Docker Quick Start - Job Tracking Included!

## ✅ Yes! Use Docker - It's All Set Up!

The job tracking feature is **fully integrated** and works perfectly with Docker.

---

## 🚀 Super Quick Start (2 Commands)

### Option 1: Use the Batch File (Easiest)
```bash
docker-build-and-run.bat
```

### Option 2: Manual Commands
```bash
# Build and start
docker-compose up --build -d

# Open browser
start http://localhost
```

**That's it!** The application is running with job tracking enabled! 🎉

---

## 📊 What You Get with Docker

✅ **Backend** - FastAPI with job tracking  
✅ **Frontend** - React with Job Tracker button  
✅ **Excel Integration** - openpyxl included  
✅ **Data Persistence** - Files saved to `./data/`  
✅ **Auto-Setup** - Everything configured automatically  

---

## 🎯 Step-by-Step Guide

### Step 1: Make Sure Docker is Running
```bash
# Check Docker is running
docker --version
docker-compose --version
```

If not installed, download: https://www.docker.com/products/docker-desktop

### Step 2: Navigate to Project
```bash
cd d:\work\ATS_software_custom\ats_web
```

### Step 3: Build and Start
```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d
```

### Step 4: Wait for Services (30-60 seconds)
```bash
# Watch the logs
docker-compose logs -f
```

Wait for:
```
✅ Backend is ready!
✅ All services started successfully!
```

Press `Ctrl+C` to exit logs (container keeps running)

### Step 5: Open Application
```
http://localhost
```

### Step 6: Test Job Tracking
1. Click **"Job Tracker"** button (top-right)
2. Click **"+ Add New"**
3. Fill in test data
4. Click **"Log Application"**
5. Success! ✅

### Step 7: Check Excel File
```bash
# View the file
dir data\jobs_applied\job_applicaiton.xlsx

# Or open it
start data\jobs_applied\job_applicaiton.xlsx
```

---

## 📁 Data Persistence

### Where is the Excel File?

**On Your Computer:**
```
d:\work\ATS_software_custom\ats_web\data\jobs_applied\job_applicaiton.xlsx
```

**Inside Docker Container:**
```
/app/backend/data/jobs_applied/job_applicaiton.xlsx
```

### Volume Mount (Already Configured!)

Your `docker-compose.yml` includes:
```yaml
volumes:
  - ./data:/app/backend/data  # ✅ Already added!
```

**This means:**
- Excel file persists on your computer
- Survives container restarts
- Can be edited while container runs
- Easy to backup

---

## 🎮 Docker Commands

### Start/Stop
```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# Restart container
docker-compose restart

# Rebuild and start
docker-compose up --build -d
```

### View Logs
```bash
# All logs
docker-compose logs

# Follow logs (live)
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50
```

### Check Status
```bash
# Is container running?
docker ps

# Container details
docker ps -a

# Check health
docker inspect ats-application
```

### Access Container
```bash
# Open shell
docker exec -it ats-application bash

# Run command
docker exec ats-application ls -la /app/backend/data/jobs_applied/
```

---

## 🧪 Test Everything Works

### Automated Test
```bash
docker-test-job-tracking.bat
```

### Manual Test
```bash
# 1. Check container
docker ps | findstr ats-application

# 2. Test backend
curl http://localhost:8000/

# 3. Test job tracking API
curl http://localhost:8000/api/job-applications

# 4. Check data directory
dir data\jobs_applied
```

---

## 🔧 Troubleshooting

### Container Won't Start

**Check Docker is running:**
```bash
docker --version
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

### Port Already in Use

**Error:** "Port 80 is already allocated"

**Solution:** Stop other services or change port:
```yaml
ports:
  - "8080:80"  # Use port 8080 instead
```

### Excel File Not Found

**Check volume mount:**
```bash
docker inspect ats-application | findstr Mounts
```

**Check inside container:**
```bash
docker exec ats-application ls -la /app/backend/data/jobs_applied/
```

**Create manually:**
```bash
mkdir data\jobs_applied
```

### Job Tracker Button Not Showing

**Clear browser cache:**
- Press `Ctrl+Shift+Delete`
- Clear cache
- Refresh page

**Rebuild frontend:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Verify Installation

### Checklist

- [ ] Docker Desktop running
- [ ] Container built successfully
- [ ] Container running (`docker ps`)
- [ ] Frontend accessible (http://localhost)
- [ ] Backend accessible (http://localhost:8000)
- [ ] "Job Tracker" button visible
- [ ] Can open Job Tracker modal
- [ ] Can log test application
- [ ] Excel file created in `data/jobs_applied/`
- [ ] Data persists after restart

### Quick Verification

```bash
# 1. Check container
docker ps

# 2. Open browser
start http://localhost

# 3. Click "Job Tracker" button

# 4. Log test application

# 5. Check file
dir data\jobs_applied\job_applicaiton.xlsx
```

---

## 🎯 Common Workflows

### Daily Use
```bash
# Start
docker-compose up -d

# Use application
# (Open http://localhost)

# Stop when done
docker-compose down
```

### Development
```bash
# Start with logs
docker-compose up

# Make changes to code

# Rebuild
docker-compose up --build
```

### Backup Data
```bash
# Copy Excel file
copy data\jobs_applied\job_applicaiton.xlsx backups\backup_%date%.xlsx

# Or use Docker
docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx backup.xlsx
```

---

## 🚀 Production Tips

### Always Running
```yaml
restart: unless-stopped  # ✅ Already configured!
```

### Health Checks
```yaml
healthcheck:  # ✅ Already configured!
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
```

### Automatic Backups
```bash
# Create backup script
echo @echo off > backup-daily.bat
echo docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx backups\backup_%%date%%.xlsx >> backup-daily.bat

# Schedule with Windows Task Scheduler
```

---

## 📚 Additional Resources

- **Complete Docker Guide**: DOCKER_JOB_TRACKING_GUIDE.md
- **Job Tracking Docs**: START_HERE_JOB_TRACKING.md
- **Docker Compose Docs**: https://docs.docker.com/compose/

---

## 🎊 You're Ready!

### Quick Commands Summary

```bash
# Build and start
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Test
docker-test-job-tracking.bat

# Access
http://localhost
```

### Excel File Location

```
d:\work\ATS_software_custom\ats_web\data\jobs_applied\job_applicaiton.xlsx
```

---

## ✅ Final Checklist

Before using:
- [x] Docker Desktop installed and running
- [x] Project files in place
- [x] docker-compose.yml configured
- [x] Volume mount added for data persistence

To start:
- [ ] Run `docker-compose up --build -d`
- [ ] Wait 30-60 seconds
- [ ] Open http://localhost
- [ ] Click "Job Tracker" button
- [ ] Start tracking applications!

---

**Everything is ready! Start Docker and begin tracking! 🐳🎯**

---

**Last Updated**: November 10, 2025  
**Docker Support**: ✅ Full  
**Data Persistence**: ✅ Configured  
**Job Tracking**: ✅ Included  
