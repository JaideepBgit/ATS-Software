"""
Quick test script for TTS functionality
"""
from pathlib import Path
import sys

print("=" * 60)
print("Testing Piper TTS Setup")
print("=" * 60)

# Test 1: Check if piper.exe exists
print("\n1. Checking for piper.exe...")
piper_path = Path("piper/piper.exe")
if piper_path.exists():
    print(f"   ✓ Found: {piper_path.absolute()}")
    print(f"   Size: {piper_path.stat().st_size:,} bytes")
else:
    print(f"   ✗ Not found: {piper_path.absolute()}")
    sys.exit(1)

# Test 2: Check if model exists
print("\n2. Checking for model...")
model_path = Path("models/en_US-lessac-medium.onnx")
if model_path.exists():
    print(f"   ✓ Found: {model_path.absolute()}")
    print(f"   Size: {model_path.stat().st_size:,} bytes")
else:
    print(f"   ✗ Not found: {model_path.absolute()}")
    sys.exit(1)

# Test 3: Import TTS service
print("\n3. Importing TTS service...")
try:
    from tts_service import PiperTTSService
    print("   ✓ Import successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 4: Initialize TTS service
print("\n4. Initializing TTS service...")
try:
    tts = PiperTTSService()
    print("   ✓ Initialization successful")
    print(f"   Executable: {tts.piper_executable}")
    print(f"   Model: {tts.model_path}")
    print(f"   Output dir: {tts.output_dir}")
except Exception as e:
    print(f"   ✗ Initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Generate test audio
print("\n5. Generating test audio...")
test_text = "Hello! This is a test of the text to speech system."
try:
    output_file = tts.text_to_speech(test_text, output_filename="test_tts.wav")
    print(f"   ✓ Audio generated: {output_file}")
    
    # Check file exists
    if Path(output_file).exists():
        print(f"   ✓ File exists: {Path(output_file).stat().st_size:,} bytes")
    else:
        print(f"   ✗ File not found: {output_file}")
        sys.exit(1)
    
    # Get audio info
    info = tts.get_audio_info(output_file)
    print(f"   Duration: {info.get('duration', 0):.2f} seconds")
    print(f"   Sample rate: {info.get('framerate', 0)} Hz")
    
except Exception as e:
    print(f"   ✗ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nTTS is working correctly!")
print(f"Test audio file: {Path(output_file).absolute()}")
print("\nYou can now use TTS in the web interface.")
