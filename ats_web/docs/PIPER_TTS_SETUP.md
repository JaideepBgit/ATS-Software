# Piper TTS Integration Guide

## Overview

Piper TTS is integrated into the ATS system for text-to-speech functionality. It's ultra-lightweight (models under 25MB) and runs on CPU without GPU requirements.

## Installation

### Step 1: Download Piper

**Windows:**
```bash
# Download from GitHub releases
# https://github.com/rhasspy/piper/releases

# Example: Download piper_windows_amd64.zip
# Extract to a folder (e.g., C:\piper)
```

**Linux:**
```bash
# Download the Linux binary
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz

# Extract
tar -xzf piper_linux_x86_64.tar.gz

# Move to /usr/local/bin (optional)
sudo mv piper/piper /usr/local/bin/
```

**macOS:**
```bash
# Download the macOS binary
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_macos_x64.tar.gz

# Extract
tar -xzf piper_macos_x64.tar.gz

# Move to /usr/local/bin (optional)
sudo mv piper/piper /usr/local/bin/
```

### Step 2: Download Voice Model

Download a voice model from the Piper releases page:

**Recommended Models:**

1. **en_US-lessac-medium** (25MB) - Best quality/size balance
   ```bash
   # Download model
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json
   ```

2. **en_US-lessac-low** (15MB) - Smaller, faster
   ```bash
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-low.onnx
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-low.onnx.json
   ```

3. **en_US-amy-medium** (25MB) - Alternative voice
   ```bash
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-amy-medium.onnx
   wget https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-amy-medium.onnx.json
   ```

### Step 3: Organize Files

Create a models directory in your project:

```
ats_web/backend/
├── models/
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
├── tts_output/  (auto-created)
└── tts_service.py
```

## Configuration

### Option 1: Auto-detection (Recommended)

If you place the piper executable in your PATH and models in `./models/`, the service will auto-detect them.

### Option 2: Manual Configuration

Edit `tts_service.py` or pass parameters:

```python
from tts_service import PiperTTSService

tts = PiperTTSService(
    piper_executable="C:/piper/piper.exe",  # Windows
    model_path="models/en_US-lessac-medium.onnx"
)
```

## Testing

### Test from Command Line

```bash
cd ats_web/backend

# Test the service
python tts_service.py
```

### Test via API

```bash
# Check TTS status
curl http://localhost:8000/api/tts/status

# Generate TTS
curl -X POST "http://localhost:8000/api/tts/generate?text=Hello%20World"

# Generate candidate summary TTS
curl -X POST http://localhost:8000/api/tts/summary/JaideepBommidi_2024-01-15
```

## API Endpoints

### 1. Generate TTS from Text
```
POST /api/tts/generate?text=<your_text>
```

**Response:**
```json
{
  "status": "success",
  "audio_path": "tts_output/tts_1234.wav",
  "duration": 5.2,
  "url": "/api/tts/audio/tts_1234.wav"
}
```

### 2. Get Audio File
```
GET /api/tts/audio/{filename}
```

Returns the WAV audio file.

### 3. Generate Candidate Summary TTS
```
POST /api/tts/summary/{candidate_id}
```

Generates TTS for a candidate's analysis summary.

### 4. Check TTS Status
```
GET /api/tts/status
```

**Response:**
```json
{
  "status": "available",
  "model": "models/en_US-lessac-medium.onnx",
  "executable": "piper",
  "output_dir": "tts_output"
}
```

## Frontend Integration

Add a "Listen" button to candidate details:

```javascript
// In CandidateDetail.js
const handleListenSummary = async () => {
  try {
    const response = await fetch(`/api/tts/summary/${candidate.candidate_id}`, {
      method: 'POST'
    });
    const data = await response.json();
    
    // Play audio
    const audio = new Audio(data.url);
    audio.play();
  } catch (error) {
    console.error('TTS error:', error);
  }
};

// Add button
<Button 
  startIcon={<VolumeUpIcon />}
  onClick={handleListenSummary}
>
  Listen to Summary
</Button>
```

## Performance

- **Model Size:** 15-25MB (ultra-lightweight)
- **Generation Speed:** Real-time on CPU (no GPU needed)
- **Memory Usage:** ~100MB RAM
- **CPU Usage:** Low (single-threaded)
- **Audio Quality:** 22kHz, 16-bit WAV

## Troubleshooting

### Error: "Piper executable not found"

**Solution:**
1. Download Piper from GitHub releases
2. Add to PATH or specify path in code
3. Verify: `piper --version`

### Error: "Model not found"

**Solution:**
1. Download model files (.onnx and .onnx.json)
2. Place in `models/` directory
3. Verify path in `tts_service.py`

### Error: "TTS generation failed"

**Solution:**
1. Check if model file is complete (not corrupted)
2. Verify piper has execute permissions (Linux/Mac)
3. Check logs for detailed error message

### Audio not playing in browser

**Solution:**
1. Check CORS settings in `main.py`
2. Verify audio file was generated in `tts_output/`
3. Test audio URL directly in browser

## Advanced Usage

### Custom Voice Speed

Modify the Piper command in `tts_service.py`:

```python
[
    self.piper_executable,
    '--model', self.model_path,
    '--output_file', str(output_path),
    '--length_scale', '1.0',  # Speed: 0.5=faster, 2.0=slower
]
```

### Multiple Languages

Download additional language models:
- Spanish: `es_ES-*`
- French: `fr_FR-*`
- German: `de_DE-*`
- And many more...

### Batch Processing

```python
texts = [
    "Candidate 1 summary...",
    "Candidate 2 summary...",
    "Candidate 3 summary..."
]

for i, text in enumerate(texts):
    tts.text_to_speech(text, output_filename=f"candidate_{i}.wav")
```

## Resources

- **Piper GitHub:** https://github.com/rhasspy/piper
- **Voice Samples:** https://rhasspy.github.io/piper-samples/
- **Model Downloads:** https://github.com/rhasspy/piper/releases
- **Documentation:** https://github.com/rhasspy/piper/blob/master/README.md

## Benefits for ATS System

1. **Accessibility:** Audio summaries for visually impaired users
2. **Multitasking:** Listen to candidate summaries while reviewing resumes
3. **Quick Review:** Audio playback faster than reading
4. **Low Resource:** No GPU needed, runs on any CPU
5. **Offline:** Works without internet connection
6. **Privacy:** All processing done locally
