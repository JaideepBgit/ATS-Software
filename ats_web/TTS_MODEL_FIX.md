# 🔧 TTS Model Fix - Download Required

## Problem

The model file is corrupted (only 9 bytes instead of 63 MB):
```
Model: en_US-lessac-medium.onnx
Size: 9 bytes ❌ (should be ~63 MB)
Content: "Not Found"
```

## Solution: Download the Correct Model

You have **3 options** to download the model:

### Option 1: Batch File (Easiest) ⭐

```bash
cd ats_web\backend
DOWNLOAD_MODEL.bat
```

Just double-click `DOWNLOAD_MODEL.bat` and it will download everything!

### Option 2: PowerShell Script

```powershell
cd ats_web\backend
powershell -ExecutionPolicy Bypass -File download_model.ps1
```

### Option 3: Python Script

```bash
cd ats_web\backend
python download_model.py
```

## What Gets Downloaded

1. **Model file**: `en_US-lessac-medium.onnx` (~63 MB)
   - The neural network voice model
   - Natural sounding American English voice

2. **Config file**: `en_US-lessac-medium.onnx.json` (~1 KB)
   - Model configuration
   - Phoneme mappings

## After Download

### Step 1: Verify Download

```bash
python test_tts.py
```

**Expected output**:
```
2. Checking for model...
   ✓ Found: D:\...\models\en_US-lessac-medium.onnx
   Size: 63,201,278 bytes  ✅ (correct size!)

5. Generating test audio...
   ✓ Audio generated: tts_output\test_tts.wav
   ✓ File exists: 123,456 bytes
   Duration: 3.45 seconds
```

### Step 2: Restart Backend

```bash
python main.py
```

### Step 3: Test Voice Button

1. Analyze a resume
2. Go to candidate detail
3. Click Voice button
4. Hear the summary!

## Manual Download (If Scripts Fail)

If the scripts don't work, download manually:

1. **Go to**: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/en/en_US/lessac/medium

2. **Download these 2 files**:
   - `en_US-lessac-medium.onnx` (63 MB)
   - `en_US-lessac-medium.onnx.json` (1 KB)

3. **Save to**: `ats_web\backend\models\`

4. **Verify**:
   - Model file should be ~63 MB
   - Config file should be ~1 KB

## Why This Happened

The model file contains "Not Found" text, which means:
- It was a placeholder
- Download failed previously
- File got corrupted

## File Sizes Reference

| File | Expected Size | Your Size | Status |
|------|--------------|-----------|--------|
| piper.exe | ~500 KB | 509,952 bytes | ✅ OK |
| en_US-lessac-medium.onnx | ~63 MB | 9 bytes | ❌ Corrupted |
| en_US-lessac-medium.onnx.json | ~1 KB | ? | ? |

## Troubleshooting

### Download fails with "Access Denied"
- Run PowerShell as Administrator
- Or use Python script instead

### Download is very slow
- HuggingFace servers might be slow
- Be patient, it's 63 MB
- Or try manual download

### File still shows 9 bytes
- Delete the old file first
- Then run download script again

### "SSL Certificate Error"
- Update Python: `pip install --upgrade certifi`
- Or download manually from browser

## Quick Commands

```bash
# Delete corrupted model
del models\en_US-lessac-medium.onnx

# Download new model (choose one):
DOWNLOAD_MODEL.bat                                    # Easiest
powershell -File download_model.ps1                   # PowerShell
python download_model.py                              # Python

# Test
python test_tts.py

# Run backend
python main.py
```

## Summary

1. ❌ **Current**: Model is corrupted (9 bytes)
2. ⬇️ **Action**: Run `DOWNLOAD_MODEL.bat`
3. ✅ **Result**: Model downloaded (63 MB)
4. 🎉 **Success**: Voice button works!

**Status**: Ready to download - just run the batch file!
