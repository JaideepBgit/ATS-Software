# TTS Audio Generation Fix

## Problem
TTS was failing with error: "Audio file was not generated"

## Root Cause - FOUND!
The real issue was **invalid filename characters**:
- The candidate_id includes a timestamp like `2025-11-14T00:05:57.387310`
- **Colons (`:`) are not allowed in Windows filenames**
- Piper was running successfully but couldn't create the file due to the invalid filename
- The file `summary_Jaideep Bommidi_2025-11-14T00:05:57.387310.wav` is invalid on Windows

Secondary issues fixed:
1. Output paths were not being converted to absolute paths
2. Insufficient debugging information
3. No filename validation

## Changes Made

### 1. Fixed Filename Sanitization in `main.py` (PRIMARY FIX)
```python
# Sanitize filename - remove invalid characters for Windows
safe_filename = candidate_id.replace(':', '-').replace('/', '-').replace('\\', '-')
audio_path = tts_service.text_to_speech(
    summary_text,
    output_filename=f"summary_{safe_filename}.wav"
)
```

This converts:
- `summary_Jaideep Bommidi_2025-11-14T00:05:57.387310.wav` (INVALID)
- To: `summary_Jaideep Bommidi_2025-11-14T00-05-57.387310.wav` (VALID)

### 2. Added Filename Validation in `tts_service.py`
- Validates filenames before attempting to create them
- Rejects filenames with invalid characters: `< > : " / \ | ? *`
- Provides clear error message if invalid filename is used

### 3. Fixed Path Handling in `tts_service.py`
- Changed output directory to use absolute path: `Path(__file__).parent / "tts_output"`
- Convert output file path to absolute before passing to Piper subprocess
- Added extensive debug logging to track the generation process

### 4. Added Debug Logging
The service now logs:
- Output file path (absolute)
- Model path being used
- Piper executable path
- Text length
- Piper return code and output
- File creation confirmation with size

### 3. Created Diagnostic Tools

#### `diagnose_tts.py`
Run this to check your TTS setup:
```bash
python diagnose_tts.py
```

Checks:
- Piper executable exists and works
- Model file exists
- Output directory exists
- Can generate test audio
- TTS service can be imported and initialized

#### `RESTART_BACKEND_TTS_FIX.bat`
Quick way to restart the backend with the fixes applied.

## How to Apply the Fix

### Option 1: Restart Backend (Recommended)
1. Stop your current backend server (Ctrl+C in the terminal)
2. Run: `RESTART_BACKEND_TTS_FIX.bat`
3. Or manually: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Option 2: Test First
1. Run the diagnostic: `python diagnose_tts.py`
2. If all checks pass, restart the backend
3. Try generating TTS again from the web interface

## Verification

After restarting, you should see detailed logs like:
```
[TTS] Generating audio to: D:\work\...\tts_output\summary_xxx.wav
[TTS] Using model: D:\work\...\models\en_US-lessac-medium.onnx
[TTS] Using executable: D:\work\...\piper\piper.exe
[TTS] Text length: 234 characters
[TTS] Piper return code: 0
[TTS] Audio file created successfully: 149780 bytes
```

## What Was Working
- Piper executable: ✓
- Model file: ✓
- Manual Piper execution: ✓
- Piper was actually running successfully!

## What Was Broken
- **Filename had colons (`:`) which are invalid on Windows**
- Piper couldn't create the output file due to invalid filename
- No filename validation to catch this earlier

## Technical Details

### The Real Problem
Windows doesn't allow these characters in filenames: `< > : " / \ | ? *`

The candidate_id was: `Jaideep Bommidi_2025-11-14T00:05:57.387310`

This created filename: `summary_Jaideep Bommidi_2025-11-14T00:05:57.387310.wav`

The colons in the timestamp (`00:05:57`) made it invalid!

### The Fix
```python
# Before
audio_path = tts_service.text_to_speech(
    summary_text,
    output_filename=f"summary_{candidate_id}.wav"  # Contains colons!
)

# After
safe_filename = candidate_id.replace(':', '-').replace('/', '-').replace('\\', '-')
audio_path = tts_service.text_to_speech(
    summary_text,
    output_filename=f"summary_{safe_filename}.wav"  # Colons replaced with dashes
)
```

### Additional Improvements
- Added filename validation in TTS service
- Convert paths to absolute before passing to Piper
- Enhanced debug logging to catch issues faster
