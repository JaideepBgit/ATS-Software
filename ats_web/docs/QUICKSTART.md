# 🚀 Quick Start Guide

Get your ATS Web Application running in 5 minutes!

## Prerequisites Check

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed  
- [ ] Ollama installed and running

## Installation (3 steps)

### 1️⃣ Install Backend
```bash
# Double-click this file:
install_backend.bat

# Or run manually:
cd backend
pip install -r requirements.txt
```

**Note:** You may see dependency warnings - these are safe to ignore! See DEPENDENCY_NOTES.md for details.

### 2️⃣ Install Frontend
```bash
# Double-click this file:
install_frontend.bat

# Or run manually:
cd frontend
npm install
```

### 3️⃣ Pull Ollama Model
```bash
ollama pull qwen2.5:7b
```

## Running (2 terminals)

### Terminal 1: Start Backend
```bash
# Double-click:
start_backend.bat

# Or run:
cd backend
python main.py
```

✅ Backend ready at: http://localhost:8000

### Terminal 2: Start Frontend
```bash
# Double-click:
start_frontend.bat

# Or run:
cd frontend
npm start
```

✅ Frontend opens at: http://localhost:3000

## First Use

1. **Job Description Tab**
   - Paste your job description
   - Click "Save"

2. **Upload Resumes Tab**
   - Click "Select PDF Files"
   - Choose one or more resumes
   - Wait for analysis

3. **Results Tab**
   - See all candidates ranked by score
   - Click "View" for details

4. **Candidate Detail Tab**
   - View detailed analysis
   - Ask questions in chat

## That's It! 🎉

Your ATS system is now running. Upload resumes and start analyzing!

## Need Help?

- Backend not starting? → Check if Ollama is running
- Frontend errors? → Run `npm install` again
- PDF upload fails? → Set job description first
- See SETUP_GUIDE.md for detailed troubleshooting
