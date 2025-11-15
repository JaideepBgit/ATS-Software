# Piper TTS Setup for ATS System

## Quick Setup (Choose One Method)

### Method 1: Automated Download (Recommended)

Run this batch file which uses Windows built-in `curl`:

```cmd
download_piper.bat
```

This will:
- Download Piper executable (10MB)
- Download voice model (25MB)
- Extract and test automatically

### Method 2: Manual Download

If automated download fails, follow the guide in `MANUAL_SETUP.md`

## Verify Installation

Run the test script:

```cmd
test_piper.bat
```

This will:
- Check if Piper executable exists
- Check if voice model exists
- Generate a test audio file
- Play the audio automatically

## Expected File Structure

After setup, you should have:

```
ats_web/backend/
├── piper/
│   └── piper/
│       ├── piper.exe          ← Piper executable
│       └── espeak-ng-data/    ← Required data files
├── models/
│   ├── en_US-lessac-medium.onnx       ← Voice model (25MB)
│   └── en_US-lessac-medium.onnx.json  ← Model config
├── tts_output/                ← Generated audio files (auto-created)
└── tts_service.py             ← TTS service code
```

## Usage

### 1. Test Python Service

```bash
python tts_service.py
```

Expected output:
```
✓ Audio generated: tts_output/tts_XXXX.wav
✓ Duration: X.XX seconds
```

### 2. Start Backend with TTS

```bash
python main.py
```

The backend will now have TTS endpoints available.

### 3. Use in Frontend

1. Start the frontend: `npm start`
2. Go to any candidate detail page
3. Click the **"Listen"** button
4. Audio summary will play automatically!

## API Endpoints

Once the backend is running:

```bash
# Check TTS status
curl http://localhost:8000/api/tts/status

# Generate TTS from text
curl -X POST "http://localhost:8000/api/tts/generate?text=Hello%20World"

# Generate candidate summary audio
curl -X POST http://localhost:8000/api/tts/summary/JaideepBommidi_2024-01-15

# Get audio file
curl http://localhost:8000/api/tts/audio/tts_1234.wav
```

## Troubleshooting

### Downloads Fail

**Solution 1:** Use the batch file with curl:
```cmd
download_piper.bat
```

**Solution 2:** Download manually from browser:
- Piper: https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip
- Model: https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
- Config: https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json

### "Piper executable not found"

Check the path exists:
```cmd
dir piper\piper\piper.exe
```

If not found, re-extract the ZIP file to the correct location.

### "Model not found"

Check both files exist:
```cmd
dir models\en_US-lessac-medium.onnx
dir models\en_US-lessac-medium.onnx.json
```

Both files are required!

### Test audio doesn't play

- Check if `test_output.wav` was created
- Try playing it manually with Windows Media Player
- Verify your audio drivers are working

### Python service fails

Make sure you're in the correct directory:
```cmd
cd D:\work\ATS_software_custom\ats_web\backend
python tts_service.py
```

## Alternative Voices

Want a different voice? Download other models:

**English Voices:**
- `en_US-amy-medium` - Warm, friendly female voice
- `en_US-ryan-medium` - Deep male voice
- `en_GB-alan-medium` - British accent

**Other Languages:**
- Spanish: `es_ES-*`
- French: `fr_FR-*`
- German: `de_DE-*`

Download from: https://github.com/rhasspy/piper/releases

## Performance

- **Model Size:** 25MB (ultra-lightweight!)
- **Generation Speed:** Real-time (~1-2 seconds)
- **CPU Usage:** Low (no GPU needed)
- **Memory:** ~100MB RAM
- **Audio Quality:** 22kHz, 16-bit WAV

## What Gets Generated?

When you click "Listen" on a candidate page, the audio includes:

1. Candidate name
2. Overall score percentage
3. Skills match score
4. Experience match score
5. Education match score
6. Hiring recommendation
7. Executive summary

Example:
> "Candidate Analysis Summary for John Doe. Overall Score: 85 percent. Skills Match: 90 percent. Experience Match: 85 percent. Education Match: 80 percent. Hiring Recommendation: YES - Strong candidate. Executive Summary: John has excellent technical skills..."

## Files Created

- `tts_service.py` - TTS service implementation
- `download_piper.bat` - Automated download script
- `test_piper.bat` - Test script
- `MANUAL_SETUP.md` - Manual setup guide
- `README_TTS.md` - This file

## Support

If you need help:
1. Run `test_piper.bat` to diagnose issues
2. Check `MANUAL_SETUP.md` for detailed instructions
3. Verify file structure matches the expected layout above
4. Check that you have ~35MB free disk space

## Resources

- **Piper GitHub:** https://github.com/rhasspy/piper
- **Voice Samples:** https://rhasspy.github.io/piper-samples/
- **All Models:** https://github.com/rhasspy/piper/releases
