# Complete Setup Guide: Resume-Matcher with LM Studio

## Current Status ✅
- [x] LM Studio running with gemma-3n-e4b model
- [x] Local server: http://127.0.0.1:1234
- [x] Dependencies installed (Option B completed)
- [x] Backend port: 8888
- [x] Frontend port: 3333

## Next Steps to Complete Setup

### Step 1: Run the Backend Modification Script
```powershell
# From your current directory (d:/work/ATS_software_custom)
python modify_backend_for_lmstudio.py
```

### Step 2: Set Up Environment Files

**Backend Environment (.env):**
```powershell
# Navigate to Resume-Matcher backend directory
cd Resume-Matcher/apps/backend

# Copy the environment configuration
copy ../../backend_env_config.txt .env
```

**Frontend Environment (.env.local):**
```powershell
# Navigate to Resume-Matcher root directory
cd Resume-Matcher

# Copy the frontend configuration
copy ../frontend_env_config.txt .env.local
```

### Step 3: Install Additional Requirements
```powershell
# In Resume-Matcher/apps/backend directory
pip install openai python-dotenv
```

### Step 4: Start the Applications

**Terminal 1 - Backend:**
```powershell
# From Resume-Matcher root directory
../../start_backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
# From Resume-Matcher root directory (new terminal)
../../start_frontend.ps1
```

## Access URLs
- **Frontend**: http://localhost:3333
- **Backend API**: http://localhost:8888
- **LM Studio**: http://127.0.0.1:1234

## Verification Steps

### 1. Check LM Studio Connection
```powershell
# Test if LM Studio API is responding
curl http://127.0.0.1:1234/v1/models
```

### 2. Check Backend Health
```powershell
# Test backend API
curl http://localhost:8888/health
```

### 3. Check Frontend
Open browser and navigate to: http://localhost:3333

## Troubleshooting

### If Backend Fails to Start:
1. Check if port 8888 is available
2. Verify .env file exists in apps/backend/
3. Ensure LM Studio server is running
4. Check Python dependencies are installed

### If Frontend Fails to Start:
1. Check if port 3333 is available
2. Verify .env.local file exists in root directory
3. Ensure npm dependencies are installed
4. Check if backend is running first

### If LM Studio Connection Fails:
1. Verify LM Studio server is running
2. Check the model is loaded
3. Test the API endpoint directly
4. Ensure no firewall blocking localhost connections

## Configuration Details

### Backend Configuration (.env)
```env
LLM_URL=http://127.0.0.1:1234/v1
MODEL_NAME=gemma-3n-e4b
API_KEY=lm-studio
PORT=8888
CORS_ORIGIN=http://localhost:3333
DATABASE_URL=sqlite:///./resume_matcher.db
DEBUG=true
LOG_LEVEL=info
```

### Frontend Configuration (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8888
PORT=3333
```

## Success Indicators
- ✅ LM Studio shows API requests in its interface
- ✅ Backend logs show successful startup on port 8888
- ✅ Frontend loads at http://localhost:3333
- ✅ Resume upload and analysis features work
- ✅ AI-powered suggestions appear

## Next Steps After Setup
1. Upload a test resume
2. Upload a test job description
3. Verify AI analysis works with your Gemma model
4. Test all features end-to-end
