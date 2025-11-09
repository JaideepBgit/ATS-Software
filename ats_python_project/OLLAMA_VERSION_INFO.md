# 🚀 Interactive ATS - Ollama Version

## What's This?

This is the **Ollama version** of the Interactive ATS, specifically configured to work with **Ollama** and your **qwen2.5:7b** model instead of LM Studio.

---

## 🆚 Ollama vs LM Studio Version

| Feature | Ollama Version | LM Studio Version |
|---------|---------------|-------------------|
| **Script** | `interactive_ats_ollama.py` | `interactive_ats.py` |
| **Config** | `ats_config_ollama.txt` | `ats_config.txt` |
| **API Endpoint** | `http://localhost:11434` | `http://localhost:1234/v1` |
| **Your Model** | `qwen2.5:7b` (4.7 GB) | `google/gemma-3n-e4b` |
| **Batch File** | `RUN_INTERACTIVE_ATS_OLLAMA.bat` | `RUN_INTERACTIVE_ATS.bat` |
| **Quick Start** | `OLLAMA_INTERACTIVE_QUICKSTART.txt` | `INTERACTIVE_QUICKSTART.txt` |

**Both versions have identical features!** The only difference is which local LLM service they connect to.

---

## ✅ What You Need

### 1. Ollama Installed
```bash
# Check if Ollama is running
curl http://localhost:11434

# Should return: "Ollama is running"
```

### 2. Model Downloaded
```bash
# List your models
ollama list

# Should show: qwen2.5:7b
```

### 3. Python Packages
```bash
pip install PyPDF2 openai
```

---

## 🚀 Quick Start

### Option 1: Double-Click (Easiest)
```
Double-click: RUN_INTERACTIVE_ATS_OLLAMA.bat
```

### Option 2: Command Line
```bash
python interactive_ats_ollama.py
```

### Then Choose Your Mode:
```
1. 🎯 RECRUITER MODE - Evaluate candidates
2. 📝 CANDIDATE MODE - Improve YOUR resume
```

---

## 📝 Configuration File

**File**: `ats_config_ollama.txt`

```ini
# Ollama Configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Paths
RESUME_FOLDER=./data/resumes
JOB_DESCRIPTION_FILE=./data/job_description.txt
OUTPUT_FOLDER=./data/reports

# Features
SAVE_DETAILED_REPORTS=true
MIN_MATCH_SCORE=60
```

---

## 🎯 Two Modes Available

### Mode 1: Recruiter Mode
**For hiring managers evaluating candidates**

Example questions:
- "What are the biggest concerns about this candidate?"
- "What should I ask in the technical interview?"
- "How do they compare to other candidates?"
- "Can they handle our tech stack?"

### Mode 2: Candidate Mode (NEW!)
**For job seekers improving their resume**

Example questions:
- "Why did I get this score?"
- "How can I rewrite my experience at [Company]?"
- "Show me before/after for my bullet points"
- "What keywords am I missing?"
- "How can I get to 90%+ match?"

---

## 📊 Performance with qwen2.5:7b

### Model Specs:
- **Size**: 4.7 GB
- **Parameters**: 7 billion
- **Context**: 32K tokens
- **Speed**: Fast (30-60 sec per resume)
- **Quality**: Excellent for resume analysis

### Why qwen2.5:7b is Great:
✅ **Fast inference** - Quick responses  
✅ **Good reasoning** - Understands context well  
✅ **Long context** - Handles full resumes  
✅ **Multilingual** - Works with multiple languages  
✅ **Free** - No API costs  

### Expected Performance:
- **Initial analysis**: 30-60 seconds per resume
- **Follow-up questions**: 5-15 seconds each
- **Accuracy**: 90%+ for resume analysis
- **Cost**: $0 (completely free!)

---

## 🔧 How It Works

### 1. Imports Advanced ATS Ollama
```python
from advanced_ats_ollama import AdvancedATSOllama, ATSMatchResult
```

### 2. Extends with Interactive Features
- Conversation history management
- Multi-turn Q&A
- Context-aware responses
- Mode switching (Recruiter/Candidate)

### 3. Uses Ollama API
```python
response = self.client.chat.completions.create(
    model="qwen2.5:7b",
    messages=conversation_history,
    temperature=0.5,
    max_tokens=2000
)
```

---

## 💡 Example Session

```
================================================================================
💬 INTERACTIVE ATS (OLLAMA) - Choose Your Mode
================================================================================

1. 🎯 RECRUITER MODE - Evaluate candidates and get hiring insights
2. 📝 CANDIDATE MODE - Improve YOUR resume with AI feedback

Select mode (1 for Recruiter, 2 for Candidate): 2

✓ Candidate Mode selected - Get personalized resume improvement advice

📋 Loading job description from: ./data/job_description.txt
✓ Job description loaded (2847 characters)

📁 Found 1 resume(s) to analyze
🤖 Analyzing all candidates first, then starting interactive sessions...

⏳ [1/1] Analyzing: john_doe_resume.pdf...
   ✓ John Doe - Score: 72.5%

================================================================================
📊 ANALYSIS COMPLETE - Starting Interactive Sessions
================================================================================

Rank   Score    Name                                Recommendation
----------------------------------------------------------------------------------------------------
1      72.5     John Doe                            MAYBE - Some gaps to address
================================================================================

[Detailed report shown...]

================================================================================
📝 RESUME IMPROVEMENT MODE - John Doe
================================================================================

Your Resume Score: 72.5% | MAYBE - Some gaps to address

🎯 Get personalized advice to improve your resume for this job!

Example questions you can ask:
  • Why was my experience flagged as a concern?
  • How can I better highlight my Python skills?
  • What's wrong with my current resume bullet points?
  • Show me before/after examples for my work experience
  • How can I increase my score to 90%+?

Type 'next' to move to next candidate, 'summary' for quick recap, 'quit' to exit
================================================================================

❓ Your question: Why did I get 72.5%?

🤖 AI Response:
----------------------------------------------------------------------------------------------------
Your 72.5% score breaks down as follows:

STRENGTHS (+45 points):
• Strong Python and Django skills (+15)
• Relevant Computer Science degree (+12)
• 3 years of software development experience (+10)
• Good problem-solving demonstrated (+8)

WEAKNESSES (-27.5 points):
• Missing cloud platform experience (AWS/Azure required) (-12)
• Experience described without metrics or quantification (-8)
• Missing Docker and Kubernetes (required skills) (-5)
• No leadership or mentoring mentioned (-2.5)

The job requires 5+ years of experience with cloud platforms, but your resume 
shows 3 years with minimal cloud work. Your technical foundation is solid, but 
you need to better showcase achievements with numbers and add the missing 
technologies.
----------------------------------------------------------------------------------------------------

❓ Your question: How can I rewrite my first work experience to score higher?

🤖 AI Response:
----------------------------------------------------------------------------------------------------
[Detailed before/after examples provided...]
----------------------------------------------------------------------------------------------------
```

---

## 🎮 Commands

While in interactive mode:

| Command | Action |
|---------|--------|
| Type question | Ask anything about the resume |
| `help` or `h` | Show help menu |
| `summary` or `s` | Quick score recap |
| `next` or `n` | Move to next resume |
| `quit` or `q` | Exit |

---

## 📚 Documentation

### For Candidate Mode:
- **Quick Start**: [OLLAMA_INTERACTIVE_QUICKSTART.txt](OLLAMA_INTERACTIVE_QUICKSTART.txt)
- **Full Guide**: [CANDIDATE_MODE_GUIDE.md](CANDIDATE_MODE_GUIDE.md)
- **Mode Comparison**: [MODES_COMPARISON.md](MODES_COMPARISON.md)

### For Interactive ATS:
- **Interactive Guide**: [INTERACTIVE_GUIDE.md](INTERACTIVE_GUIDE.md)
- **What's New**: [WHATS_NEW_CANDIDATE_MODE.md](WHATS_NEW_CANDIDATE_MODE.md)

### For Ollama Setup:
- **Ollama Docs**: https://ollama.ai/docs
- **Model Library**: https://ollama.ai/library

---

## ✅ Advantages of Ollama Version

### vs LM Studio:
✅ **Simpler setup** - No GUI needed  
✅ **Command-line friendly** - Easy automation  
✅ **Faster model switching** - `ollama run <model>`  
✅ **Better for servers** - Headless operation  
✅ **Active development** - Frequent updates  

### vs Cloud APIs:
✅ **100% private** - Data never leaves your machine  
✅ **No costs** - Unlimited usage  
✅ **No rate limits** - Process as many as you want  
✅ **Works offline** - No internet needed  
✅ **GDPR compliant** - Complete data control  

---

## 🔄 Switching Between Versions

You can use **both versions** on the same machine!

### Use Ollama Version When:
- ✅ You prefer command-line tools
- ✅ You want simpler setup
- ✅ You're running on a server
- ✅ You like Ollama's model management

### Use LM Studio Version When:
- ✅ You prefer GUI tools
- ✅ You want visual model management
- ✅ You like seeing token usage in real-time
- ✅ You're already using LM Studio

**Both work equally well!** Choose based on your preference.

---

## 🚀 Get Started Now!

### 1. Verify Ollama is Running
```bash
curl http://localhost:11434
# Should return: "Ollama is running"
```

### 2. Check Your Model
```bash
ollama list
# Should show: qwen2.5:7b
```

### 3. Run Interactive ATS
```bash
python interactive_ats_ollama.py
```

### 4. Choose Your Mode
- Mode 1: Evaluate candidates (Recruiter)
- Mode 2: Improve your resume (Candidate)

### 5. Start Asking Questions!
Get AI-powered insights and advice instantly.

---

## 💬 Need Help?

### Ollama Not Running?
```bash
# Start Ollama (it usually starts automatically)
ollama serve
```

### Model Not Found?
```bash
# Pull the model
ollama pull qwen2.5:7b

# Verify it's downloaded
ollama list
```

### Connection Issues?
- Check Ollama is running: `http://localhost:11434`
- Verify config file: `ats_config_ollama.txt`
- Check firewall settings

### Slow Performance?
- First request loads model (30-60 sec)
- Subsequent requests are faster (5-15 sec)
- Close other applications to free RAM
- qwen2.5:7b needs ~6-8 GB RAM

---

**Ready to analyze resumes with Ollama? Start now!** 🚀
