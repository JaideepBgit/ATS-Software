# TTS Usage Guide

## Overview
The TTS system now supports:
1. **Single audio file** - Always overwrites the same file (no clutter)
2. **Question/Answer TTS** - Speak any text, including Q&A responses

## Backend Changes

### 1. Single Audio File for Summaries
```python
# Now uses fixed filename that gets overwritten
audio_path = tts_service.text_to_speech(
    summary_text,
    output_filename="candidate_summary.wav"  # Always the same file
)
```

### 2. New General TTS Endpoint
```
POST /api/tts/speak
Body: { "text": "Your text here" }
```

This endpoint:
- Accepts any text
- Generates audio to `speech.wav` (always overwritten)
- Returns audio URL for playback

## Frontend Components

### SpeakButton Component
Reusable button to speak any text:

```jsx
import SpeakButton from './components/SpeakButton';

// Icon variant (default)
<SpeakButton text="Hello, this is a test" />

// Button variant with text
<SpeakButton text="Hello, this is a test" variant="button" />

// Different sizes
<SpeakButton text="Hello" size="sm" />  // Small
<SpeakButton text="Hello" size="md" />  // Medium (default)
<SpeakButton text="Hello" size="lg" />  // Large
```

### QuestionAnswer Component
Complete Q&A interface with TTS:

```jsx
import QuestionAnswer from './components/QuestionAnswer';

function App() {
  return <QuestionAnswer />;
}
```

Features:
- Ask questions
- Get answers
- Each answer has a speak button
- Clean conversation UI

## Integration Examples

### 1. Add TTS to Existing Components

#### In CandidateDetail.js
```jsx
import SpeakButton from './SpeakButton';

// Add next to any text
<div className="flex items-center gap-2">
  <p>{candidate.executive_summary}</p>
  <SpeakButton text={candidate.executive_summary} size="sm" />
</div>
```

#### In ResultsList.js
```jsx
import SpeakButton from './SpeakButton';

// Add to each result
<div className="flex justify-between items-start">
  <div>
    <h3>{result.candidate_name}</h3>
    <p>Score: {result.overall_score}%</p>
  </div>
  <SpeakButton 
    text={`${result.candidate_name}, score ${result.overall_score} percent`}
    size="sm"
  />
</div>
```

### 2. Add Q&A Page to Your App

In your main App.js or routing:

```jsx
import QuestionAnswer from './components/QuestionAnswer';

// Add as a new route/tab
<Route path="/questions" element={<QuestionAnswer />} />

// Or add as a section
<div className="container">
  <QuestionAnswer />
</div>
```

### 3. Custom Q&A Integration

If you have your own Q&A API:

```jsx
const generateAnswer = async (question) => {
  const response = await fetch('YOUR_API_ENDPOINT', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  
  const data = await response.json();
  return data.answer;
};
```

## API Reference

### POST /api/tts/speak
Generate TTS for any text.

**Request:**
```json
{
  "text": "Your text to speak"
}
```

**Response:**
```json
{
  "status": "success",
  "audio_path": "D:\\path\\to\\speech.wav",
  "duration": 3.5,
  "url": "/api/tts/audio/speech.wav"
}
```

### POST /api/tts/summary/{candidate_id}
Generate TTS for candidate summary (existing endpoint).

**Response:**
```json
{
  "status": "success",
  "candidate_id": "John_Doe_2025-11-14",
  "audio_path": "D:\\path\\to\\candidate_summary.wav",
  "duration": 15.2,
  "url": "/api/tts/audio/candidate_summary.wav"
}
```

### GET /api/tts/audio/{filename}
Serve audio file for playback.

## File Management

### Audio Files
All audio files are stored in: `backend/tts_output/`

Current files:
- `candidate_summary.wav` - Candidate summaries (overwritten)
- `speech.wav` - General speech (overwritten)

### Benefits of Single File Approach
- No disk space waste
- No cleanup needed
- Always fresh audio
- Simple file management

## Testing

### Test General TTS
```bash
curl -X POST http://localhost:8000/api/tts/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test of the text to speech system."}'
```

### Test in Browser Console
```javascript
fetch('http://localhost:8000/api/tts/speak', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Hello world' })
})
.then(r => r.json())
.then(data => {
  const audio = new Audio(`http://localhost:8000${data.url}`);
  audio.play();
});
```

## Troubleshooting

### Audio Not Playing
1. Check browser console for errors
2. Verify backend is running: `http://localhost:8000/api/tts/status`
3. Check audio file exists: `backend/tts_output/speech.wav`

### TTS Generation Fails
1. Check backend logs for detailed error messages
2. Verify Piper is installed: `backend/piper/piper.exe`
3. Verify model exists: `backend/models/en_US-lessac-medium.onnx`

### CORS Issues
If accessing from different domain, ensure CORS is configured in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Next Steps

1. **Add to existing pages**: Use `SpeakButton` component anywhere you have text
2. **Create Q&A page**: Use `QuestionAnswer` component or build your own
3. **Customize**: Modify components to match your design
4. **Extend**: Add more TTS features as needed

The system is now ready for both candidate summaries and general Q&A with TTS!
