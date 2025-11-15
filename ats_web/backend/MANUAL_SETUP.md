# Manual Piper TTS Setup

The automated script failed to download files. Please follow these manual steps:

## Step 1: Download Piper Executable

**For Windows:**

1. Go to: https://github.com/rhasspy/piper/releases/tag/v1.2.0
2. Download: **piper_windows_amd64.zip** (about 10MB)
3. Extract the ZIP file
4. You should see a folder structure like:
   ```
   piper/
   ├── piper.exe
   ├── espeak-ng-data/
   └── (other files)
   ```
5. Copy the entire `piper` folder to: `D:\work\ATS_software_custom\ats_web\backend\piper\`

Final structure should be:
```
D:\work\ATS_software_custom\ats_web\backend\
├── piper\
│   └── piper\
│       ├── piper.exe
│       └── espeak-ng-data\
```

## Step 2: Download Voice Model

1. Go to: https://github.com/rhasspy/piper/releases/tag/v1.2.0
2. Scroll down to "Assets" section
3. Download these TWO files:
   - **en_US-lessac-medium.onnx** (25MB)
   - **en_US-lessac-medium.onnx.json** (small config file)

4. Create a `models` folder if it doesn't exist:
   ```
   D:\work\ATS_software_custom\ats_web\backend\models\
   ```

5. Place both downloaded files in the `models` folder

Final structure:
```
D:\work\ATS_software_custom\ats_web\backend\
├── models\
│   ├── en_US-lessac-medium.onnx
│   └── en_US-lessac-medium.onnx.json
```

## Step 3: Test Installation

Open PowerShell in the backend directory and run:

```powershell
cd D:\work\ATS_software_custom\ats_web\backend

# Test Piper directly
echo "Hello, this is a test" | .\piper\piper\piper.exe --model .\models\en_US-lessac-medium.onnx --output_file test.wav

# If successful, you should see test.wav created
# Play it to verify the voice quality
```

## Step 4: Test Python Service

```bash
python tts_service.py
```

If everything is set up correctly, you should see:
```
✓ Audio generated: tts_output/tts_XXXX.wav
✓ Duration: X.XX seconds
```

## Alternative: Use Direct Links

If the GitHub releases page is slow, you can try these direct download links:

**Piper Windows:**
```
https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip
```

**Voice Model (ONNX):**
```
https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx
```

**Voice Model Config (JSON):**
```
https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json
```

You can paste these URLs directly in your browser or use a download manager.

## Troubleshooting

### "Piper executable not found"
- Verify the path: `D:\work\ATS_software_custom\ats_web\backend\piper\piper\piper.exe`
- Make sure you extracted the ZIP correctly
- The folder structure should have TWO "piper" folders (one inside the other)

### "Model not found"
- Verify both files exist:
  - `models\en_US-lessac-medium.onnx`
  - `models\en_US-lessac-medium.onnx.json`
- Both files are required!

### Downloads are blocked/slow
- Try using a different browser
- Try downloading from a different network
- Use a download manager like Internet Download Manager (IDM)
- Ask a colleague to download and share via USB/network

## Quick Verification Checklist

- [ ] `piper\piper\piper.exe` exists
- [ ] `piper\piper\espeak-ng-data\` folder exists
- [ ] `models\en_US-lessac-medium.onnx` exists (should be ~25MB)
- [ ] `models\en_US-lessac-medium.onnx.json` exists (small file)
- [ ] Test command works: `echo "test" | .\piper\piper\piper.exe --model .\models\en_US-lessac-medium.onnx --output_file test.wav`

## Next Steps

Once setup is complete:

1. Test the Python service: `python tts_service.py`
2. Start the backend: `python main.py`
3. Open the frontend and go to a candidate detail page
4. Click the "Listen" button to hear the audio summary!

## Need Help?

If you're still having issues:
1. Check that you have ~35MB free disk space (10MB Piper + 25MB model)
2. Verify you have permission to create files in the backend directory
3. Try running PowerShell as Administrator
4. Check your antivirus isn't blocking the downloads
