# 🐳 Docker Deployment Guide

Deploy the complete ATS application (Frontend + Backend + Ollama) in a single Docker container.

## 📋 Prerequisites

- **Docker Desktop** installed on your system
  - Windows: [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
  - Mac: [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
  - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)
- **Docker Compose** (included with Docker Desktop)
- At least **8GB RAM** available for Docker
- At least **10GB disk space** for models

---

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Navigate to the project directory
cd ats_web

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t ats-app .

# Run the container
docker run -d \
  --name ats-application \
  -p 80:80 \
  -p 8000:8000 \
  -p 11434:11434 \
  -e MODEL_NAME=qwen2.5:7b \
  -v ollama_data:/root/.ollama \
  ats-app

# View logs
docker logs -f ats-application

# Stop the container
docker stop ats-application
docker rm ats-application
```

---

## 🌐 Access the Application

Once the container is running:

- **Frontend (Web UI)**: http://localhost
- **Backend API**: http://localhost:8000
- **Ollama API**: http://localhost:11434
- **API Documentation**: http://localhost:8000/docs

---

## ⚙️ Configuration

### Change the AI Model

Edit `docker-compose.yml` and change the `MODEL_NAME` environment variable:

```yaml
environment:
  - MODEL_NAME=llama3.2:3b  # or any other Ollama model
```

Available models:
- `qwen2.5:7b` (default, good balance)
- `llama3.2:3b` (faster, less accurate)
- `mistral:7b` (alternative)
- `phi3:mini` (smallest, fastest)

### Custom Ports

If ports 80, 8000, or 11434 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8080:80"        # Frontend on port 8080
  - "8001:8000"      # Backend on port 8001
  - "11435:11434"    # Ollama on port 11435
```

---

## 🔧 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Check if ports are available
# Windows
netstat -ano | findstr "80 8000 11434"

# Mac/Linux
lsof -i :80,8000,11434
```

### Ollama model download is slow

The first startup will download the AI model (2-4GB). This is normal and only happens once.

```bash
# Check download progress
docker-compose logs -f ats-app
```

### Out of memory errors

Increase Docker memory allocation:
- Docker Desktop → Settings → Resources → Memory
- Set to at least 8GB

### Backend can't connect to Ollama

```bash
# Check if Ollama is running inside container
docker exec -it ats-application curl http://localhost:11434/api/tags

# Restart the container
docker-compose restart
```

---

## 📦 What's Included

The Docker image contains:

1. **Python 3.11** with all backend dependencies
2. **Node.js 18** for building the frontend
3. **Ollama** for running AI models locally
4. **Nginx** for serving the frontend and routing requests
5. **All application code** (frontend + backend)

---

## 🔄 Updating the Application

### Update code and rebuild

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update AI model only

```bash
# Enter the container
docker exec -it ats-application bash

# Pull new model
ollama pull llama3.2:3b

# Exit
exit

# Update docker-compose.yml with new MODEL_NAME
# Restart
docker-compose restart
```

---

## 💾 Data Persistence

Models are stored in a Docker volume and persist across container restarts:

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect ats_web_ollama_data

# Remove volume (deletes downloaded models)
docker volume rm ats_web_ollama_data
```

---

## 🧹 Cleanup

### Stop and remove everything

```bash
# Stop containers
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove images
docker rmi ats-app
```

### Free up disk space

```bash
# Remove unused Docker resources
docker system prune -a

# Remove specific volume
docker volume rm ats_web_ollama_data
```

---

## 🖥️ Platform-Specific Notes

### Windows

- Use **PowerShell** or **Command Prompt** (not Git Bash)
- Ensure **WSL 2** is enabled for Docker Desktop
- If you see "file not found" errors, check line endings (should be LF, not CRLF)

```powershell
# Fix line endings for start.sh
git config core.autocrlf false
git rm --cached -r .
git reset --hard
```

### Mac (Apple Silicon M1/M2/M3)

- Docker will automatically use ARM64 architecture
- Some models may take longer to download
- Everything else works the same

### Linux

- You may need to run Docker commands with `sudo`
- Or add your user to the docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🔐 Security Notes

**For Production Deployment:**

1. Change default ports
2. Add authentication to the API
3. Use environment variables for sensitive data
4. Enable HTTPS with SSL certificates
5. Set up proper firewall rules
6. Use Docker secrets for API keys

**Current setup is for development/demo purposes only.**

---

## 📊 Resource Usage

Typical resource consumption:

- **CPU**: 2-4 cores (during model inference)
- **RAM**: 4-8GB (depends on model size)
- **Disk**: 5-10GB (models + application)
- **Network**: Initial download ~2-4GB

---

## 🐛 Debug Mode

Run with verbose logging:

```bash
# Docker Compose
docker-compose up

# Docker
docker run -it --rm \
  -p 80:80 -p 8000:8000 -p 11434:11434 \
  -e MODEL_NAME=qwen2.5:7b \
  ats-app
```

---

## 📝 Build Arguments

Customize the build:

```bash
# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t ats-app .

# Build without cache
docker build --no-cache -t ats-app .
```

---

## 🚢 Shipping to Others

### Share the Docker image

```bash
# Save image to file
docker save ats-app > ats-app.tar

# Load on another machine
docker load < ats-app.tar
```

### Push to Docker Hub

```bash
# Tag the image
docker tag ats-app yourusername/ats-app:latest

# Push to Docker Hub
docker push yourusername/ats-app:latest

# Others can pull and run
docker pull yourusername/ats-app:latest
docker run -d -p 80:80 -p 8000:8000 -p 11434:11434 yourusername/ats-app:latest
```

---

## ✅ Verification Checklist

After starting the container, verify:

- [ ] Container is running: `docker ps`
- [ ] Frontend loads: http://localhost
- [ ] Backend responds: http://localhost:8000
- [ ] Ollama is ready: http://localhost:11434/api/tags
- [ ] Can upload a resume and get analysis
- [ ] Chat feature works

---

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify all services are running inside container
3. Check Docker resource allocation
4. Ensure ports are not in use by other applications
5. Try rebuilding: `docker-compose up -d --build`

---

## 🎯 Next Steps

1. Start the application: `docker-compose up -d`
2. Wait for model download (first time only)
3. Open http://localhost in your browser
4. Upload a resume and test the system
5. Enjoy! 🎉

---

**Built with ❤️ using Docker, Python, React, and Ollama**
