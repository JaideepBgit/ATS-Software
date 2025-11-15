# ✅ ATS Web Setup Checklist

## Pre-Installation

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] Ollama installed and running (`ollama list`)
- [ ] Model downloaded (`ollama pull qwen2.5:7b`)

## Installation

- [ ] Backend dependencies installed (`install_backend.bat`)
- [ ] Frontend dependencies installed (`install_frontend.bat`)
- [ ] Backend test passed (`cd backend && python test_setup.py`)

## First Run

- [ ] Backend server started (`start_backend.bat`)
  - [ ] Shows "Uvicorn running on http://0.0.0.0:8000"
  - [ ] No error messages
  
- [ ] Frontend app started (`start_frontend.bat`)
  - [ ] Browser opens at http://localhost:3000
  - [ ] App loads without errors

## First Use

- [ ] Job description entered and saved
- [ ] Test PDF uploaded successfully
- [ ] Results appear in Results tab
- [ ] Can view candidate details
- [ ] Chat interface responds to questions

## Troubleshooting (if needed)

- [ ] Checked START_HERE.md for solutions
- [ ] Reviewed DEPENDENCY_NOTES.md about warnings
- [ ] Verified Ollama is running
- [ ] Restarted both servers
- [ ] Checked browser console for errors

## All Done! 🎉

If all boxes are checked, your ATS Web Application is fully operational!

---

**Quick Reference:**

Start Backend: `start_backend.bat` → http://localhost:8000
Start Frontend: `start_frontend.bat` → http://localhost:3000

**Need Help?** See START_HERE.md
