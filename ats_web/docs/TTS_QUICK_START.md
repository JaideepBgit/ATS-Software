# Piper TTS - Quick Start Guide

## What is Piper TTS?

Piper is an ultra-lightweight text-to-speech engine that:
- **Runs on CPU only** (no GPU needed)
- **Small models** (15-25MB)
- **Fast generation** (real-time speech)
- **High quality** natural-sounding voices
- **Offline** - no internet required

Perfect for the ATS system to provide audio summaries of candidate analyses!

## Quick Setup (Windows)

### Automated Setup

```powershell
cd ats_web/backend
powershell -ExecutionPolicy Bypass -File setup_piper_tts.ps1
```

This will:
1. Download Piper executable
2. Download voice model (en_US-lessac-medium, 25MB)
3. Test the installation

### Manual Setup

1. **Download Piper:**
   - Go to: https://github.com/rhasspy/piper/releases
   - Download: `piper_windows_amd64.zip`
   - Extract to `ats_web/backend/piper/`

2. **Download Voice Model:**
   - Download: `en_US-lessac-medium.onnx` (25MB)
   - Download: `en_US-lessac-medium.onnx.json`
   - Place in `ats_web/backend/models/`

3. **Test:**
   ```bash
   cd ats_web/backend
   python tts_service.py
   ```

## Usage in ATS System

### 1. Backend API

The TTS service is automatically integrated into the backend:

```python
# Check if TTS is available
GET /api/tts/status

# Generate TTS from text
POST /api/tts/generate?text=Hello%20World

# Generate candidate summary audio
POST /api/tts/summary/{candidate_id}

# Get audio file
GET /api/tts/audio/{filename}
```

### 2. Frontend - Listen Button

A "Listen" button is now available on the Candidate Detail page:

- Click "Listen" to hear the candidate summary
- Audio includes: scores, recommendation, and executive summary
- Click "Stop" to stop playback

### 3. Programmatic Usage

```python
from tts_service import get_tts_service

tts = get_tts_service()

# Generate audio
audio_path = tts.text_to_speech("Hello, this is a test")

# Get audio info
info = tts.get_audio_info(audio_path)
print(f"Duration: {info['duration']:.2f} seconds")
```

## Features

### Current Features
- ✅ Generate TTS from any text
- ✅ Candidate summary audio generation
- ✅ Play/Stop controls in UI
- ✅ Automatic cleanup of old audio files
- ✅ Status checking endpoint

### Potential Enhancements
- 🔄 Multiple voice options
- 🔄 Speed control (faster/slower)
- 🔄 Batch generation for all candidates
- 🔄 Download audio files
- 🔄 Multi-language support

## File Structure

```
ats_web/backend/
├── tts_service.py          # TTS service implementation
├── main.py                 # API endpoints added
├── models/                 # Voice models
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
├── piper/                  # Piper executable
│   └── piper/
│       └── piper.exe
└── tts_output/            # Generated audio files (auto-created)
    └── *.wav

ats_web/frontend/src/components/
├── TTSButton.js           # Reusable TTS button component
└── CandidateDetail.js     # Updated with Listen button
```

## Troubleshooting

### "Piper executable not found"

**Fix:**
```python
# In tts_service.py, specify the path:
tts = PiperTTSService(
    piper_executable="piper/piper/piper.exe"
)
```

### "Model not found"

**Fix:**
1. Verify model files exist in `models/` directory
2. Check both `.onnx` and `.onnx.json` files are present
3. Update path in `tts_service.py` if needed

### "TTS not available" in UI

**Fix:**
1. Check backend is running: `python main.py`
2. Test TTS status: `curl http://localhost:8000/api/tts/status`
3. Check browser console for errors

### Audio not playing

**Fix:**
1. Check if audio file was generated in `tts_output/`
2. Try accessing audio URL directly in browser
3. Check CORS settings in `main.py`

## Performance

- **Generation Time:** ~1-2 seconds for typical summary (real-time)
- **CPU Usage:** Low (single-threaded)
- **Memory:** ~100MB RAM
- **Storage:** 25MB model + ~100KB per audio file
- **Audio Quality:** 22kHz, 16-bit WAV

## Alternative Voices

Download additional voices from Piper releases:

**English Voices:**
- `en_US-lessac-medium` (25MB) - Clear, professional (default)
- `en_US-amy-medium` (25MB) - Warm, friendly
- `en_US-ryan-medium` (25MB) - Deep, authoritative
- `en_GB-alan-medium` (25MB) - British accent

**Other Languages:**
- Spanish: `es_ES-*`
- French: `fr_FR-*`
- German: `de_DE-*`
- Italian: `it_IT-*`
- And 40+ more languages!

## Resources

- **Piper GitHub:** https://github.com/rhasspy/piper
- **Voice Samples:** https://rhasspy.github.io/piper-samples/
- **Full Setup Guide:** See `PIPER_TTS_SETUP.md`

## Benefits for ATS

1. **Accessibility:** Audio summaries for all users
2. **Efficiency:** Listen while multitasking
3. **Quick Review:** Faster than reading
4. **Professional:** Impress stakeholders with audio reports
5. **Privacy:** All processing done locally (no cloud APIs)
6. **Cost:** Free and open-source
