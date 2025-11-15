# Interactive ATS - Resume Analysis System

AI-powered resume analysis with interactive Q&A capabilities.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_advanced.txt
```

### 2. Choose Your Version

**Ollama (Recommended):**
```bash
python interactive_ats_ollama.py
```

**LM Studio:**
```bash
python interactive_ats.py
```

### 3. Select Mode
- Mode 1: Recruiter (evaluate candidates)
- Mode 2: Candidate (improve your resume)

## Files

**Core:**
- `advanced_ats.py` - Base ATS engine
- `interactive_ats.py` - LM Studio version
- `interactive_ats_ollama.py` - Ollama version (8192 context)

**Config:**
- `ats_config.txt` - LM Studio config
- `ats_config_ollama.txt` - Ollama config

**Test:**
- `test_ollama.py` - Test Ollama connection
- `test_lm_studio.py` - Test LM Studio connection

**Data:**
- `data/resumes/` - Put PDF resumes here
- `data/job_description.txt` - Edit with job description

## Configuration

**Ollama (qwen2.5:7b):**
- Endpoint: `http://localhost:11434/v1`
- Context: 8192 tokens (automatic)
- VRAM: ~6-7 GB

**LM Studio:**
- Endpoint: `http://localhost:1234/v1`
- Model: Configure in LM Studio

## Features

- AI-powered resume analysis
- Interactive Q&A about candidates
- Two modes: Recruiter & Candidate
- Before/after resume examples
- Candidate comparison
- Detailed scoring

## Usage

```bash
# Test connection
python test_ollama.py

# Run interactive ATS
python interactive_ats_ollama.py

# Choose mode and start asking questions!
```
