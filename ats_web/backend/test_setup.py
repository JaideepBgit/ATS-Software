"""
Test script to verify backend setup
"""
import sys

print("Testing ATS Backend Setup...")
print("=" * 50)

# Test imports
try:
    import fastapi
    print(f"✓ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"✗ FastAPI: {e}")
    sys.exit(1)

try:
    import uvicorn
    print(f"✓ Uvicorn: {uvicorn.__version__}")
except ImportError as e:
    print(f"✗ Uvicorn: {e}")
    sys.exit(1)

try:
    import PyPDF2
    print(f"✓ PyPDF2: {PyPDF2.__version__}")
except ImportError as e:
    print(f"✗ PyPDF2: {e}")
    sys.exit(1)

try:
    import openai
    print(f"✓ OpenAI: {openai.__version__}")
except ImportError as e:
    print(f"✗ OpenAI: {e}")
    sys.exit(1)

try:
    import pydantic
    print(f"✓ Pydantic: {pydantic.__version__}")
except ImportError as e:
    print(f"✗ Pydantic: {e}")
    sys.exit(1)

print("=" * 50)

# Test ATS Service
try:
    from ats_service import ATSService
    print("✓ ATS Service imported successfully")
    
    # Test initialization
    ats = ATSService()
    print(f"✓ ATS Service initialized")
    print(f"  - LLM URL: {ats.llm_url}")
    print(f"  - Model: {ats.model}")
    
except Exception as e:
    print(f"✗ ATS Service error: {e}")
    sys.exit(1)

print("=" * 50)
print("✅ All tests passed! Backend is ready.")
print("\nTo start the server, run:")
print("  python main.py")
print("\nOr double-click: start_backend.bat")
