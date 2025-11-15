"""
Download Piper TTS Model
Downloads the en_US-lessac-medium voice model for Piper TTS
"""
import urllib.request
import sys
from pathlib import Path

MODEL_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx"
MODEL_CONFIG_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"

def download_file(url, destination):
    """Download a file with progress bar"""
    print(f"Downloading: {url}")
    print(f"To: {destination}")
    
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            bar_length = 50
            filled = int(bar_length * percent / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f'\r[{bar}] {percent:.1f}% ({downloaded:,} / {total_size:,} bytes)', end='')
    
    try:
        urllib.request.urlretrieve(url, destination, progress_hook)
        print()  # New line after progress bar
        return True
    except Exception as e:
        print(f"\nError downloading: {e}")
        return False

def main():
    print("=" * 70)
    print("Piper TTS Model Downloader")
    print("=" * 70)
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    print(f"\n✓ Models directory: {models_dir.absolute()}")
    
    # Download model file
    model_path = models_dir / "en_US-lessac-medium.onnx"
    print(f"\n1. Downloading model file (~63 MB)...")
    
    if model_path.exists():
        size = model_path.stat().st_size
        if size > 1000000:  # More than 1 MB
            print(f"   Model already exists ({size:,} bytes)")
            response = input("   Download again? (y/n): ")
            if response.lower() != 'y':
                print("   Skipping model download")
            else:
                if not download_file(MODEL_URL, model_path):
                    sys.exit(1)
        else:
            print(f"   Existing file is corrupted ({size} bytes), re-downloading...")
            if not download_file(MODEL_URL, model_path):
                sys.exit(1)
    else:
        if not download_file(MODEL_URL, model_path):
            sys.exit(1)
    
    # Verify model
    if model_path.exists():
        size = model_path.stat().st_size
        print(f"   ✓ Model downloaded: {size:,} bytes")
        if size < 1000000:
            print(f"   ⚠ Warning: File seems too small (expected ~63 MB)")
    else:
        print("   ✗ Model file not found after download")
        sys.exit(1)
    
    # Download config file
    config_path = models_dir / "en_US-lessac-medium.onnx.json"
    print(f"\n2. Downloading config file...")
    
    if config_path.exists():
        print(f"   Config already exists")
        response = input("   Download again? (y/n): ")
        if response.lower() != 'y':
            print("   Skipping config download")
        else:
            if not download_file(MODEL_CONFIG_URL, config_path):
                sys.exit(1)
    else:
        if not download_file(MODEL_CONFIG_URL, config_path):
            sys.exit(1)
    
    # Verify config
    if config_path.exists():
        size = config_path.stat().st_size
        print(f"   ✓ Config downloaded: {size:,} bytes")
    else:
        print("   ✗ Config file not found after download")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✓ DOWNLOAD COMPLETE!")
    print("=" * 70)
    print(f"\nModel: {model_path.absolute()}")
    print(f"Config: {config_path.absolute()}")
    print(f"\nTotal size: {(model_path.stat().st_size + config_path.stat().st_size):,} bytes")
    print("\nYou can now run: python test_tts.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
