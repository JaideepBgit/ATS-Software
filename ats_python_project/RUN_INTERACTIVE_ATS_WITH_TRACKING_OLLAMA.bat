@echo off
echo ========================================
echo Interactive ATS with Job Tracking (OLLAMA)
echo ========================================
echo.
echo This will:
echo - Keep your resume in session
echo - Analyze multiple jobs
echo - Track applications in Excel
echo - Use Ollama local models
echo.
echo Make sure you have:
echo 1. Ollama running (ollama serve)
echo 2. A model installed (ollama pull llama2)
echo 3. Installed requirements: pip install -r requirements_advanced.txt
echo.
pause

python interactive_ats_with_tracking_ollama.py

pause
