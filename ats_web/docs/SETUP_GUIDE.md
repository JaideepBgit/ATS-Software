# ATS Web - Complete Setup Guide

## Prerequisites

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download](https://nodejs.org/)
3. **Ollama** (recommended) - [Download](https://ollama.ai/)

## Step-by-Step Setup

### Step 1: Install Ollama (Recommended)

```bash
# Download and install Ollama from https://ollama.ai/

# Pull a model
ollama pull qwen2.5:7b
```

### Step 2: Install Backend

```bash
# Option A: Use batch file (Windows)
install_backend.bat

# Option B: Manual installation
cd backend
pip install -r requirements.txt
```

### Step 3: Install Frontend

```bash
# Option A: Use batch file (Windows)
install_frontend.bat

# Option B: Manual installation
cd frontend
npm install
```

### Step 4: Start Backend Server

```bash
# Option A: Use batch file (Windows)
start_backend.bat

# Option B: Manual start
cd backend
python main.py
```

Backend will start on: **http://localhost:8000**

### Step 5: Start Frontend (New Terminal)

```bash
# Option A: Use batch file (Windows)
start_frontend.bat

# Option B: Manual start
cd frontend
npm start
```

Frontend will open automatically at: **http://localhost:3000**

## First Time Usage

1. Open http://localhost:3000 in your browser
2. Go to "Job Description" tab
3. Paste your job description and click "Save"
4. Go to "Upload Resumes" tab
5. Select one or more PDF resumes
6. Wait for analysis to complete
7. View results in "Results" tab
8. Click "View" on any candidate for detailed analysis
9. Use the chat interface to ask questions

## Configuration Options

### Using Different LLM Providers

**Ollama (Default):**
```bash
# No configuration needed if using default settings
# Ollama runs on http://localhost:11434/v1
```

**LM Studio:**
```bash
# Create backend/.env file:
LLM_URL=http://localhost:1234/v1
LLM_MODEL=your-model-name
```

**OpenAI:**
```bash
# Create backend/.env file:
OPENAI_API_KEY=sk-your-key-here
LLM_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

## Troubleshooting

### Backend Issues

**"Module not found" error:**
```bash
cd backend
pip install -r requirements.txt
```

**"Port 8000 already in use":**
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in main.py:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**"LLM not available":**
- Check if Ollama is running: `ollama list`
- Verify model is pulled: `ollama pull qwen2.5:7b`
- Test connection: `curl http://localhost:11434/v1/models`

### Frontend Issues

**"npm not found":**
- Install Node.js from https://nodejs.org/

**"Port 3000 already in use":**
- Frontend will automatically try port 3001
- Or manually set: `PORT=3001 npm start`

**"Cannot connect to backend":**
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy setting in package.json

### PDF Upload Issues

**"Could not extract text":**
- Ensure PDF is not password protected
- Try a different PDF
- Check if PDF contains actual text (not just images)

**"Job description not set":**
- Go to "Job Description" tab first
- Enter and save job description
- Then upload resumes

## Performance Tips

1. **Use Ollama with GPU** for faster analysis
2. **Upload multiple resumes at once** for batch processing
3. **Use smaller models** (7B) for faster responses
4. **Close unused tabs** to save memory

## Next Steps

- Customize scoring weights in `ats_service.py`
- Add more suggested questions in `ChatInterface.js`
- Integrate with database for persistence
- Add user authentication
- Deploy to production server

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs in terminal
3. Check browser console for frontend errors
4. Verify all prerequisites are installed
