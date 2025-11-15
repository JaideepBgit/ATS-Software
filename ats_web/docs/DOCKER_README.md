# 🐳 ATS Application - Docker Edition

**One-click deployment for Windows, Mac, and Linux**

This Docker setup packages everything you need:
- ✅ Frontend (React)
- ✅ Backend (Python/FastAPI)
- ✅ Ollama (AI Model Server)
- ✅ All dependencies

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Docker

**Windows/Mac:**
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Start Docker Desktop

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
```

### Step 2: Start the Application

**Windows:**
```cmd
start-docker.bat
```

**Mac/Linux:**
```bash
chmod +x start-docker.sh
./start-docker.sh
```

**Or manually:**
```bash
docker-compose up -d
```

### Step 3: Open Your Browser

Go to: **http://localhost**

That's it! 🎉

---

## ⏱️ First Run

The first time you start the application:
- Docker will download the AI model (~2-4GB)
- This takes 5-10 minutes depending on your internet speed
- Subsequent starts are instant (< 30 seconds)

Watch the progress:
```bash
docker-compose logs -f
```

---

## 🛑 Stop the Application

```bash
docker-compose down
```

Or use Docker Desktop GUI to stop the container.

---

## 🔧 Configuration

### Change AI Model

Edit `docker-compose.yml`:
```yaml
environment:
  - MODEL_NAME=llama3.2:3b  # Change this
```

Popular models:
- `qwen2.5:7b` - Default, best quality
- `llama3.2:3b` - Faster, smaller
- `mistral:7b` - Alternative
- `phi3:mini` - Smallest, fastest

### Change Ports

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:80"      # Frontend on port 8080
  - "8001:8000"    # Backend on port 8001
  - "11435:11434"  # Ollama on port 11435
```

---

## 📊 System Requirements

**Minimum:**
- 4GB RAM
- 10GB disk space
- Docker Desktop installed

**Recommended:**
- 8GB RAM
- 20GB disk space
- SSD for better performance

---

## 🐛 Troubleshooting

### "Docker is not running"
- Start Docker Desktop
- Wait for it to fully start (whale icon in system tray)

### "Port already in use"
- Change ports in `docker-compose.yml`
- Or stop the conflicting application

### "Out of memory"
- Docker Desktop → Settings → Resources
- Increase memory to 8GB

### Model download is slow
- This is normal for first run
- Model is ~2-4GB
- Check progress: `docker-compose logs -f`

### Can't access http://localhost
- Wait 2-3 minutes after starting
- Check logs: `docker-compose logs`
- Try http://localhost:80

---

## 📦 What's Running

When you start the application, Docker runs:

1. **Ollama Server** (Port 11434)
   - Downloads and runs AI models
   - Handles all AI inference

2. **Python Backend** (Port 8000)
   - FastAPI server
   - Resume analysis logic
   - PDF processing

3. **React Frontend** (Port 80)
   - Web interface
   - Served by Nginx

All in one container! 🎁

---

## 🔄 Updates

To update the application:

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

---

## 🧹 Cleanup

Remove everything:
```bash
# Stop and remove containers
docker-compose down

# Remove downloaded models (frees ~4GB)
docker-compose down -v

# Remove Docker image
docker rmi ats-app
```

---

## 🚢 Share with Others

### Option 1: Share the code
```bash
# Others can clone and run
git clone <your-repo>
cd ats_web
docker-compose up -d
```

### Option 2: Share the Docker image
```bash
# Save image to file
docker save ats-app > ats-app.tar

# Send ats-app.tar to others
# They can load it:
docker load < ats-app.tar
docker run -d -p 80:80 -p 8000:8000 -p 11434:11434 ats-app
```

### Option 3: Push to Docker Hub
```bash
# Tag and push
docker tag ats-app yourusername/ats-app:latest
docker push yourusername/ats-app:latest

# Others can pull and run
docker pull yourusername/ats-app:latest
docker run -d -p 80:80 -p 8000:8000 -p 11434:11434 yourusername/ats-app:latest
```

---

## 📝 Files Created

```
ats_web/
├── Dockerfile              # Main Docker image definition
├── docker-compose.yml      # Easy orchestration
├── .dockerignore          # Files to exclude from build
├── docker/
│   ├── nginx.conf         # Web server config
│   └── start.sh           # Startup script
├── start-docker.bat       # Windows launcher
├── start-docker.sh        # Mac/Linux launcher
└── DOCKER_README.md       # This file
```

---

## ✅ Verification

After starting, check:

```bash
# All services running
docker ps

# Frontend accessible
curl http://localhost

# Backend accessible
curl http://localhost:8000

# Ollama accessible
curl http://localhost:11434/api/tags
```

---

## 🎯 Usage

1. Open http://localhost
2. Enter job description
3. Upload resume PDF
4. Get instant analysis
5. Chat with AI about candidates

---

## 💡 Tips

- **First run**: Be patient, model download takes time
- **Logs**: Use `docker-compose logs -f` to watch progress
- **Restart**: `docker-compose restart` if something breaks
- **Clean start**: `docker-compose down && docker-compose up -d`
- **Save resources**: Stop when not using: `docker-compose down`

---

## 🔐 Security Note

This setup is for **development/demo** purposes.

For production:
- Add authentication
- Use HTTPS
- Set up proper firewall
- Use environment variables for secrets
- Enable rate limiting

---

## 📞 Need Help?

1. Check logs: `docker-compose logs -f`
2. Restart: `docker-compose restart`
3. Clean rebuild: `docker-compose up -d --build`
4. Check Docker resources (RAM/disk)
5. Verify ports are available

---

## 🎉 Success!

If you see this, you're ready:

```
✅ All services started successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 Frontend:  http://localhost
🔧 Backend:   http://localhost:8000
🤖 Ollama:    http://localhost:11434
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Enjoy your ATS application!** 🚀
