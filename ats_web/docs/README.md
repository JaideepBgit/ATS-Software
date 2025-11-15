# ATS Web Application

Full-stack web application for resume analysis with React + Material UI frontend and FastAPI backend.

## Features

- 📝 Job description management
- 📤 PDF resume upload (single or multiple)
- 📊 Candidate scoring and ranking
- 💬 Interactive AI chat about candidates
- 🎯 Detailed candidate analysis
- 📈 Visual score breakdowns
- 🧠 **AI Thinking Process** - See chain-of-thought reasoning (collapsible)

## Tech Stack

**Frontend:**
- React 18
- Material-UI 5
- Axios

**Backend:**
- FastAPI
- OpenAI API (compatible with Ollama/LM Studio)
- PyPDF2

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
echo "LLM_URL=http://localhost:11434/v1" > .env
echo "LLM_MODEL=qwen2.5:7b" >> .env

# Start server
python main.py
```

Backend runs on: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on: http://localhost:3000

## Configuration

### Using Ollama (Recommended)

1. Install and start Ollama
2. Pull a model: `ollama pull qwen2.5:7b`
3. Backend will auto-connect to `http://localhost:11434/v1`

### Using LM Studio

1. Start LM Studio server
2. Set environment variable:
   ```bash
   LLM_URL=http://localhost:1234/v1
   LLM_MODEL=your-model-name
   ```

### Using OpenAI

1. Get API key from OpenAI
2. Set environment variable:
   ```bash
   OPENAI_API_KEY=your-key-here
   LLM_URL=https://api.openai.com/v1
   LLM_MODEL=gpt-4o-mini
   ```

## Usage

1. **Set Job Description**: Enter the job requirements in the first tab
2. **Upload Resumes**: Upload one or multiple PDF resumes
3. **View Results**: See ranked candidates with scores
4. **Analyze Candidates**: Click "View" to see detailed analysis
5. **Ask Questions**: Use the chat interface to get AI insights

## API Endpoints

- `POST /api/job-description` - Save job description
- `GET /api/job-description` - Get job description
- `POST /api/upload-resume` - Upload and analyze resume
- `GET /api/results` - Get all analysis results
- `GET /api/result/{candidate_id}` - Get specific result
- `POST /api/ask` - Ask question about candidate
- `DELETE /api/results` - Clear all results

## Project Structure

```
ats_web/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── ats_service.py       # Core ATS logic
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.js           # Main app component
    │   └── components/
    │       ├── JobDescription.js
    │       ├── UploadResume.js
    │       ├── ResultsList.js
    │       ├── CandidateDetail.js
    │       └── ChatInterface.js
    └── package.json
```

## Development

### Backend Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Run development server
npm start

# Build for production
npm run build
```

## Production Deployment

### Backend

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build production bundle
npm run build

# Serve with nginx or any static server
```

## Troubleshooting

**Backend won't start:**
- Check if Ollama/LM Studio is running
- Verify LLM_URL is correct
- Check port 8000 is available

**Frontend can't connect:**
- Ensure backend is running on port 8000
- Check CORS settings in main.py
- Verify proxy setting in package.json

**PDF upload fails:**
- Check file is valid PDF
- Ensure job description is set first
- Check backend logs for errors

**AI responses not working:**
- Verify LLM is running and accessible
- Check model name is correct
- Test with `/api/ask` endpoint directly

## License

MIT
