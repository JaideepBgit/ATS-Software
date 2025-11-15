# 🐳 Docker Setup - Job Application Tracking

## ✅ Yes! Docker is Fully Supported

The job tracking feature works perfectly with Docker. Everything is already configured!

---

## 🚀 Quick Start with Docker

### Step 1: Build the Docker Image
```bash
cd d:\work\ATS_software_custom\ats_web
docker-compose build
```

### Step 2: Start the Container
```bash
docker-compose up
```

### Step 3: Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Job Tracker**: Click the button in the top-right corner!

---

## 📦 What's Included in Docker

### ✅ Automatic Setup
- Backend with job tracking module
- Frontend with Job Tracker component
- Excel file directory created automatically
- All dependencies installed (including openpyxl)

### ✅ Data Persistence
The Excel file is stored inside the container at:
```
/app/backend/data/jobs_applied/job_applicaiton.xlsx
```

---

## 💾 Data Persistence Options

### Option 1: Use Docker Volumes (Recommended)

Update your `docker-compose.yml`:

```yaml
services:
  ats-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ats-application
    ports:
      - "80:80"
      - "8000:8000"
    volumes:
      - ./data:/app/backend/data  # 👈 Add this line
    environment:
      - LLM_URL=http://host.docker.internal:11434/v1
      - MODEL_NAME=qwen2.5:7b
      - PYTHONUNBUFFERED=1
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped
```

**Benefits:**
- Excel file persists on your host machine
- Survives container restarts
- Easy to backup
- Can edit in Excel while container runs

### Option 2: Copy File from Container

```bash
# Copy Excel file from container to host
docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx ./job_applications.xlsx

# Copy file from host to container
docker cp ./job_applications.xlsx ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx
```

---

## 🔧 Complete Docker Setup

### 1. Update docker-compose.yml (Optional but Recommended)

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
      - ./data:/app/backend/data  # Persist data
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

### 2. Build and Run

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

---

## 📊 Verify Job Tracking Works

### 1. Check Container is Running
```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE              PORTS                          STATUS
abc123def456   ats-app           0.0.0.0:80->80/tcp, ...        Up 2 minutes
```

### 2. Access the Application
Open browser: http://localhost

### 3. Click "Job Tracker" Button
Top-right corner of the application

### 4. Log a Test Application
- Click "+ Add New"
- Fill in test data
- Submit

### 5. Verify Excel File Created

**With Volume Mount:**
```bash
# Check on host machine
dir data\jobs_applied\job_applicaiton.xlsx
```

**Without Volume Mount:**
```bash
# Check inside container
docker exec ats-application ls -la /app/backend/data/jobs_applied/
```

---

## 🎯 Docker Commands Reference

### Build & Run
```bash
# Build image
docker-compose build

# Start container (detached)
docker-compose up -d

# Start container (with logs)
docker-compose up

# Rebuild and start
docker-compose up --build
```

### Manage Container
```bash
# Stop container
docker-compose down

# Restart container
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker ps
```

### Access Container
```bash
# Open shell in container
docker exec -it ats-application bash

# View backend logs
docker exec ats-application tail -f /app/backend/logs.txt

# Check if Excel file exists
docker exec ats-application ls -la /app/backend/data/jobs_applied/
```

### Data Management
```bash
# Copy Excel file OUT of container
docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx ./backup.xlsx

# Copy Excel file INTO container
docker cp ./backup.xlsx ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx

# View Excel file content (if installed)
docker exec ats-application cat /app/backend/data/jobs_applied/job_applicaiton.xlsx
```

---

## 🔍 Troubleshooting Docker

### Issue: Excel File Not Persisting

**Problem**: File disappears when container restarts

**Solution**: Add volume mount to docker-compose.yml
```yaml
volumes:
  - ./data:/app/backend/data
```

### Issue: Permission Denied

**Problem**: Cannot write to Excel file

**Solution**: Check container permissions
```bash
docker exec ats-application ls -la /app/backend/data/jobs_applied/
docker exec ats-application chmod 777 /app/backend/data/jobs_applied/
```

### Issue: Module Not Found (openpyxl)

**Problem**: Backend error about missing openpyxl

**Solution**: Rebuild the image
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Issue: Cannot Access Application

**Problem**: http://localhost not working

**Solution**: Check ports and container status
```bash
# Check if container is running
docker ps

# Check logs
docker-compose logs

# Check if ports are available
netstat -ano | findstr :80
netstat -ano | findstr :8000
```

### Issue: Job Tracker Button Not Showing

**Problem**: Frontend not updated

**Solution**: Clear browser cache or rebuild
```bash
# Rebuild with no cache
docker-compose build --no-cache

# Force recreate containers
docker-compose up --force-recreate
```

---

## 📁 File Locations in Docker

### Inside Container
```
/app/
├── backend/
│   ├── main.py
│   ├── job_tracker.py
│   └── data/
│       └── jobs_applied/
│           └── job_applicaiton.xlsx
└── frontend/
    └── build/
```

### On Host (with volume mount)
```
d:\work\ATS_software_custom\ats_web\
└── data/
    └── jobs_applied/
        └── job_applicaiton.xlsx
```

---

## 🎨 Docker-Specific Features

### Automatic Directory Creation
The container automatically creates:
- `/app/backend/data/`
- `/app/backend/data/jobs_applied/`

### Automatic Excel File Creation
On first application log:
- Excel file created automatically
- Headers added
- Ready to use

### Health Checks
Docker monitors the backend:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## 🚀 Production Deployment

### With Volume Mount (Recommended)

```yaml
version: '3.8'

services:
  ats-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ats-application
    ports:
      - "80:80"
      - "8000:8000"
    volumes:
      - ./data:/app/backend/data  # Persist data
      - ./backups:/app/backups     # Backup location
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

### Backup Strategy

```bash
# Create backup script
cat > backup.bat << 'EOF'
@echo off
set BACKUP_DIR=backups\%date:~-4,4%%date:~-10,2%%date:~-7,2%
mkdir %BACKUP_DIR%
docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx %BACKUP_DIR%\
echo Backup created in %BACKUP_DIR%
EOF

# Run backup
backup.bat
```

---

## 📊 Testing in Docker

### 1. Start Container
```bash
docker-compose up -d
```

### 2. Wait for Services
```bash
# Check logs
docker-compose logs -f
```

Wait for:
```
✅ Backend is ready!
✅ All services started successfully!
```

### 3. Test Job Tracking

**Open browser**: http://localhost

**Test steps**:
1. Click "Job Tracker" button
2. Click "+ Add New"
3. Fill in test data:
   - Company: "Test Company"
   - Job: "Test Position"
   - Portal: "LinkedIn"
   - Type: "Full Time"
4. Click "Log Application"
5. Verify success message

### 4. Verify Excel File

**With volume mount**:
```bash
type data\jobs_applied\job_applicaiton.xlsx
```

**Without volume mount**:
```bash
docker exec ats-application cat /app/backend/data/jobs_applied/job_applicaiton.xlsx
```

---

## 🎯 Quick Commands

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Backup Excel file
docker cp ats-application:/app/backend/data/jobs_applied/job_applicaiton.xlsx ./backup.xlsx

# Access container shell
docker exec -it ats-application bash

# Check if job tracking works
curl http://localhost:8000/api/job-applications
```

---

## ✅ Verification Checklist

- [ ] Docker image builds successfully
- [ ] Container starts without errors
- [ ] Frontend accessible at http://localhost
- [ ] Backend API accessible at http://localhost:8000
- [ ] "Job Tracker" button visible
- [ ] Can open Job Tracker modal
- [ ] Can log test application
- [ ] Excel file created
- [ ] Statistics showing correctly
- [ ] Data persists after restart (if using volumes)

---

## 🎊 You're Ready!

The job tracking feature is **fully compatible with Docker**!

### Quick Start:
```bash
cd d:\work\ATS_software_custom\ats_web
docker-compose up --build
```

Then open: **http://localhost**

**Happy tracking in Docker! 🐳**

---

## 📚 Additional Resources

- **Docker Compose Docs**: https://docs.docker.com/compose/
- **Volume Management**: https://docs.docker.com/storage/volumes/
- **Main Documentation**: See other JOB_TRACKING_*.md files

---

**Last Updated**: November 10, 2025  
**Docker Version**: 3.8  
**Status**: ✅ Fully Supported  
