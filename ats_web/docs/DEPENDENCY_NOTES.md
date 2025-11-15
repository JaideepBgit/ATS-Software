# Dependency Notes

## About the Dependency Warnings

You may see dependency conflict warnings during installation. These are **normal and safe to ignore** for this application.

### Why These Warnings Appear

Your Python environment has many packages installed (langchain, selenium, mediapipe, etc.). When pip installs our ATS packages, it shows warnings about version mismatches with those other packages.

### What's Important

The ATS Web App only uses these packages:
- ✅ fastapi
- ✅ uvicorn  
- ✅ openai
- ✅ pydantic
- ✅ PyPDF2
- ✅ python-multipart

As long as these are installed, the app will work perfectly.

### Warnings You Can Ignore

These warnings are about **other packages** that the ATS app doesn't use:

```
langchain conflicts with tenacity/packaging
  → ATS doesn't use langchain

selenium conflicts with certifi/urllib3
  → ATS doesn't use selenium

mediapipe conflicts with protobuf
  → ATS doesn't use mediapipe

llama-stack conflicts with h11/openai
  → ATS doesn't use llama-stack directly

mcp/ollama conflicts with pydantic
  → These are CLI tools, not used by the web app
```

### How to Verify Everything Works

Run the test script:
```bash
cd ats_web/backend
python test_setup.py
```

If you see "✅ All tests passed!" then you're good to go!

### If You Want a Clean Environment

If the warnings bother you, create a dedicated virtual environment:

```bash
# Create new environment
python -m venv ats_env

# Activate it
ats_env\Scripts\activate  # Windows
source ats_env/bin/activate  # Linux/Mac

# Install only ATS requirements
cd ats_web/backend
pip install -r requirements.txt

# Now run the app
python main.py
```

This gives you a clean environment with only ATS dependencies.

## Summary

**The dependency warnings are cosmetic and don't affect the ATS Web App.**

Your installation is successful if:
1. No actual ERROR messages (warnings are OK)
2. `python test_setup.py` passes
3. Backend starts without crashes

Proceed with confidence! 🚀
