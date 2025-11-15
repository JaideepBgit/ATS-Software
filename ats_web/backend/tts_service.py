"""
Piper TTS Service - Ultra-lightweight text-to-speech using Piper
"""
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
import wave


class PiperTTSService:
    """
    Piper TTS Service for converting text to speech
    
    Piper is ultra-lightweight (models under 25MB) and runs on CPU without GPU.
    Perfect for low-resource environments.
    """
    
    def __init__(self, model_path: Optional[str] = None, piper_executable: Optional[str] = None):
        """
        Initialize Piper TTS Service
        
        Args:
            model_path: Path to Piper model file (.onnx)
            piper_executable: Path to piper executable (auto-detected if None)
        """
        try:
            self.piper_executable = piper_executable or self._find_piper()
            print(f"[TTS] Found Piper executable: {self.piper_executable}")
        except Exception as e:
            print(f"[TTS ERROR] Could not find Piper executable: {e}")
            raise
        
        try:
            self.model_path = model_path or self._get_default_model()
            print(f"[TTS] Using model: {self.model_path}")
            
            # Verify model exists
            if not Path(self.model_path).exists():
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            print(f"[TTS] Model verified: {Path(self.model_path).stat().st_size} bytes")
        except Exception as e:
            print(f"[TTS ERROR] Could not find model: {e}")
            raise
        
        # Use absolute path for output directory
        self.output_dir = Path(__file__).parent / "tts_output"
        self.output_dir.mkdir(exist_ok=True)
        print(f"[TTS] Output directory: {self.output_dir.absolute()}")
        print(f"[TTS] Initialization complete!")
        
    def _find_piper(self) -> str:
        """Find piper executable in system PATH or common locations"""
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        
        # Check local piper folder first (most likely location)
        local_piper_paths = [
            script_dir / 'piper' / 'piper.exe',  # Windows
            script_dir / 'piper' / 'piper',      # Linux/Mac
            'piper/piper.exe',
            'piper/piper',
        ]
        
        for path in local_piper_paths:
            if Path(path).exists():
                return str(Path(path).absolute())
        
        # Check if piper is in PATH
        try:
            result = subprocess.run(['piper', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                return 'piper'
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check common installation paths
        common_paths = [
            'piper.exe',  # Windows current dir
            './piper',
            '/usr/local/bin/piper',
            '/usr/bin/piper',
            str(Path.home() / 'piper' / 'piper'),
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return str(Path(path).absolute())
        
        raise FileNotFoundError(
            "Piper executable not found. Please install Piper TTS:\n"
            "1. Download from: https://github.com/rhasspy/piper/releases\n"
            "2. Extract and add to PATH or specify path in constructor"
        )
    
    def _get_default_model(self) -> str:
        """Get default model path"""
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        
        # Check local models folder first (most likely location)
        local_model_paths = [
            script_dir / 'models' / 'en_US-lessac-medium.onnx',
            'models/en_US-lessac-medium.onnx',
        ]
        
        for model_path in local_model_paths:
            if Path(model_path).exists():
                return str(Path(model_path).absolute())
        
        # Check common model locations
        model_dirs = [
            script_dir / 'models',
            Path('models'),
            Path('piper_models'),
            Path.home() / 'piper' / 'models',
            Path('/usr/share/piper/models'),
        ]
        
        for model_dir in model_dirs:
            if model_dir.exists():
                # Look for any .onnx model file
                models = list(model_dir.glob('*.onnx'))
                if models:
                    return str(models[0].absolute())
        
        # Return expected path (will need to be downloaded)
        default_model = script_dir / 'models' / 'en_US-lessac-medium.onnx'
        return str(default_model)
    
    def text_to_speech(self, text: str, output_filename: Optional[str] = None) -> str:
        """
        Convert text to speech using Piper TTS
        
        Args:
            text: Text to convert to speech
            output_filename: Output filename (auto-generated if None)
            
        Returns:
            Path to generated audio file
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Generate output filename if not provided
        if output_filename is None:
            output_filename = f"tts_{hash(text) % 10000}.wav"
        
        # Validate filename - check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in output_filename for char in invalid_chars):
            raise ValueError(
                f"Invalid filename: {output_filename}\n"
                f"Filename contains invalid characters. Please remove: {invalid_chars}"
            )
        
        output_path = self.output_dir / output_filename
        
        # Check if model exists
        if not Path(self.model_path).exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}\n"
                f"Download models from: https://github.com/rhasspy/piper/releases\n"
                f"Recommended: en_US-lessac-medium.onnx (25MB)"
            )
        
        try:
            # Ensure output path is absolute
            output_path_abs = output_path.absolute()
            
            print(f"[TTS] Generating audio to: {output_path_abs}")
            print(f"[TTS] Using model: {self.model_path}")
            print(f"[TTS] Using executable: {self.piper_executable}")
            print(f"[TTS] Text length: {len(text)} characters")
            
            # Run Piper TTS
            # piper --model <model> --output_file <output> < input.txt
            process = subprocess.Popen(
                [
                    self.piper_executable,
                    '--model', self.model_path,
                    '--output_file', str(output_path_abs)
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text, timeout=30)
            
            print(f"[TTS] Piper return code: {process.returncode}")
            print(f"[TTS] Piper stdout: {stdout}")
            if stderr:
                print(f"[TTS] Piper stderr: {stderr}")
            
            if process.returncode != 0:
                raise RuntimeError(f"Piper TTS failed: {stderr}")
            
            if not output_path_abs.exists():
                print(f"[TTS ERROR] File not found at: {output_path_abs}")
                print(f"[TTS ERROR] Directory contents: {list(self.output_dir.glob('*'))}")
                raise RuntimeError("Audio file was not generated")
            
            print(f"[TTS] Audio file created successfully: {output_path_abs.stat().st_size} bytes")
            return str(output_path_abs)
            
        except subprocess.TimeoutExpired:
            process.kill()
            raise RuntimeError("TTS generation timed out")
        except Exception as e:
            raise RuntimeError(f"TTS generation failed: {str(e)}")
    
    def text_to_speech_stream(self, text: str) -> bytes:
        """
        Convert text to speech and return audio data as bytes
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio data as bytes (WAV format)
        """
        # Generate to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            self.text_to_speech(text, output_filename=Path(tmp_path).name)
            
            # Read audio data
            with open(tmp_path, 'rb') as f:
                audio_data = f.read()
            
            return audio_data
        finally:
            # Clean up temporary file
            if Path(tmp_path).exists():
                Path(tmp_path).unlink()
    
    def get_audio_info(self, audio_path: str) -> dict:
        """Get information about generated audio file"""
        try:
            with wave.open(audio_path, 'rb') as wav_file:
                return {
                    'channels': wav_file.getnchannels(),
                    'sample_width': wav_file.getsampwidth(),
                    'framerate': wav_file.getframerate(),
                    'frames': wav_file.getnframes(),
                    'duration': wav_file.getnframes() / wav_file.getframerate()
                }
        except Exception as e:
            return {'error': str(e)}
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old TTS files"""
        import time
        current_time = time.time()
        
        for file_path in self.output_dir.glob('*.wav'):
            file_age = current_time - file_path.stat().st_mtime
            if file_age > (max_age_hours * 3600):
                file_path.unlink()


# Singleton instance
_tts_service = None


def get_tts_service() -> PiperTTSService:
    """Get or create TTS service singleton"""
    global _tts_service
    if _tts_service is None:
        _tts_service = PiperTTSService()
    return _tts_service


# Example usage
if __name__ == "__main__":
    tts = PiperTTSService()
    
    # Test text
    test_text = """
    Hello! This is a test of Piper TTS. 
    The candidate has strong technical skills in Python and machine learning.
    Overall score is 85 percent. Recommendation: Hire.
    """
    
    try:
        output_file = tts.text_to_speech(test_text)
        print(f"✓ Audio generated: {output_file}")
        
        info = tts.get_audio_info(output_file)
        print(f"✓ Duration: {info.get('duration', 0):.2f} seconds")
        
    except Exception as e:
        print(f"✗ Error: {e}")
