"""
TTS Diagnostic Script - Helps identify TTS issues
"""
import subprocess
from pathlib import Path

print("=" * 70)
print("TTS DIAGNOSTIC TOOL")
print("=" * 70)

# Check 1: Piper executable
print("\n[1] Checking Piper executable...")
piper_path = Path(__file__).parent / "piper" / "piper.exe"
print(f"    Looking for: {piper_path}")
if piper_path.exists():
    print(f"    ✓ Found ({piper_path.stat().st_size:,} bytes)")
    
    # Test piper version
    try:
        result = subprocess.run([str(piper_path), "--version"], 
                              capture_output=True, text=True, timeout=5)
        print(f"    ✓ Executable works: {result.stdout.strip()}")
    except Exception as e:
        print(f"    ✗ Executable test failed: {e}")
else:
    print(f"    ✗ Not found")

# Check 2: Model file
print("\n[2] Checking model file...")
model_path = Path(__file__).parent / "models" / "en_US-lessac-medium.onnx"
print(f"    Looking for: {model_path}")
if model_path.exists():
    size_mb = model_path.stat().st_size / (1024 * 1024)
    print(f"    ✓ Found ({size_mb:.1f} MB)")
else:
    print(f"    ✗ Not found")

# Check 3: Output directory
print("\n[3] Checking output directory...")
output_dir = Path(__file__).parent / "tts_output"
print(f"    Looking for: {output_dir}")
if output_dir.exists():
    files = list(output_dir.glob("*.wav"))
    print(f"    ✓ Found ({len(files)} audio files)")
else:
    print(f"    ✗ Not found (will be created)")
    output_dir.mkdir(exist_ok=True)
    print(f"    ✓ Created directory")

# Check 4: Test generation
print("\n[4] Testing audio generation...")
test_output = output_dir / "diagnostic_test.wav"
test_text = "This is a diagnostic test of the text to speech system."

try:
    print(f"    Running: piper --model {model_path.name} --output_file {test_output.name}")
    process = subprocess.Popen(
        [str(piper_path), "--model", str(model_path), "--output_file", str(test_output)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=test_text, timeout=10)
    
    if process.returncode == 0:
        print(f"    ✓ Piper executed successfully")
        if test_output.exists():
            print(f"    ✓ Audio file created ({test_output.stat().st_size:,} bytes)")
        else:
            print(f"    ✗ Audio file NOT created")
            print(f"    stdout: {stdout}")
            print(f"    stderr: {stderr}")
    else:
        print(f"    ✗ Piper failed (exit code {process.returncode})")
        print(f"    stderr: {stderr}")
        
except Exception as e:
    print(f"    ✗ Test failed: {e}")
    import traceback
    traceback.print_exc()

# Check 5: Import TTS service
print("\n[5] Testing TTS service import...")
try:
    from tts_service import PiperTTSService, get_tts_service
    print(f"    ✓ Import successful")
    
    # Try to initialize
    print(f"    Initializing service...")
    tts = get_tts_service()
    print(f"    ✓ Service initialized")
    print(f"       Executable: {tts.piper_executable}")
    print(f"       Model: {tts.model_path}")
    print(f"       Output dir: {tts.output_dir}")
    
except Exception as e:
    print(f"    ✗ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
print("\nIf all checks passed, TTS should work correctly.")
print("If any checks failed, review the errors above.")
