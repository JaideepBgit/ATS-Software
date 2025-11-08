# Docker Setup Guide for Resume-Matcher with LM Studio

## 🐳 **Super Easy Docker Setup**

### **Prerequisites:**
- ✅ Docker Desktop installed and running
- ✅ LM Studio running with gemma-3n-e4b model at http://127.0.0.1:1234

### **One-Command Setup:**

```powershell
# From d:/work/ATS_software_custom/ directory
docker-compose up --build
```

That's it! Docker will:
- ✅ Build both backend and frontend containers
- ✅ Install all dependencies automatically
- ✅ Configure ports (Backend: 8888, Frontend: 3333)
- ✅ Connect to your LM Studio automatically
- ✅ Set up networking between containers

## **Access Your Application:**
- **Frontend**: http://localhost:3333
- **Backend API**: http://localhost:8888
- **LM Studio**: http://127.0.0.1:1234 (your existing setup)

## **Docker Commands:**

### Start the application:
```powershell
docker-compose up --build
```

### Start in background (detached):
```powershell
docker-compose up -d --build
```

### Stop the application:
```powershell
docker-compose down
```

### View logs:
```powershell
# All services
docker-compose logs

# Backend only
docker-compose logs backend

# Frontend only
docker-compose logs frontend
```

### Restart services:
```powershell
docker-compose restart
```

## **Configuration Details:**

### **LM Studio Connection:**
- Uses `host.docker.internal:1234` to connect from Docker to your local LM Studio
- Automatically configured in docker-compose.yml
- No manual network configuration needed

### **Ports:**
- Frontend: `localhost:3333`
- Backend: `localhost:8888`
- LM Studio: `127.0.0.1:1234` (your existing setup)

### **Volumes:**
- Backend data persisted in Docker volume
- Source code mounted for development (hot reload)

## **Advantages of Docker Setup:**
- 🚀 **One command setup** - No manual file copying
- 🔧 **Automatic dependency management** - No pip/npm commands
- 🌐 **Network configuration handled** - Containers can talk to each other
- 📦 **Isolated environment** - No conflicts with your system
- 🔄 **Easy restart/rebuild** - Just run docker-compose up again
- 🧹 **Clean removal** - docker-compose down removes everything

## **Troubleshooting:**

### If containers fail to start:
```powershell
# Check Docker Desktop is running
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose up --build --force-recreate
```

### If LM Studio connection fails:
1. Ensure LM Studio server is running
2. Verify model is loaded
3. Check Windows firewall isn't blocking Docker
4. Try restarting Docker Desktop

### If ports are in use:
```powershell
# Check what's using the ports
netstat -ano | findstr :3333
netstat -ano | findstr :8888
```

## **Development Mode:**
The Docker setup includes hot reload, so you can:
- Edit code in Resume-Matcher directory
- Changes will automatically reflect in running containers
- No need to rebuild for code changes

## **Production Mode:**
For production deployment, modify docker-compose.yml:
- Remove volume mounts
- Use production builds
- Add proper environment variables
- Configure reverse proxy if needed
