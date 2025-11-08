# 🚀 LM Studio Setup Guide for Advanced ATS

## Quick Start with LM Studio + Gemma

You already have LM Studio and the Gemma model - perfect! Here's how to use it with the Advanced ATS:

### Step 1: Start LM Studio Server

1. **Open LM Studio**
2. **Load your model**: `google/gemma-3n-e4b`
3. **Start the server**:
   - Click on the "Local Server" tab (or "Developer" tab)
   - Click "Start Server"
   - Default URL: `http://localhost:1234`
   - Keep LM Studio running while using the ATS

### Step 2: Verify Configuration

Your `ats_config.txt` is already configured:
```ini
LLM_PROVIDER=local
LOCAL_LLM_URL=http://localhost:1234/v1
LOCAL_LLM_MODEL=google/gemma-3n-e4b
```

✅ You're all set!

### Step 3: Run the Advanced ATS

```bash
python advanced_ats.py
```

Or double-click: **RUN_ADVANCED_ATS.bat**

---

## What to Expect

### Processing Time (with Gemma on local machine):
- **Per resume**: 30-90 seconds (depending on your hardware)
- **10 resumes**: 5-15 minutes
- **Faster than**: Manual review (hours)
- **More accurate than**: Simple keyword matching

### Quality:
- ✅ Deep semantic understanding
- ✅ Context-aware skill extraction
- ✅ Intelligent matching
- ✅ Detailed insights
- ✅ Interview questions
- ✅ Hiring recommendations

---

## Optimizing Performance

### For Faster Processing:

1. **GPU Acceleration** (if you have NVIDIA GPU):
   - LM Studio automatically uses GPU if available
   - Check LM Studio settings → Enable GPU

2. **Reduce Context Length**:
   - In LM Studio server settings
   - Set "Context Length" to 4096 or 8192
   - Faster inference, still accurate for resumes

3. **Adjust Temperature**:
   - Already optimized in code (0.1-0.4)
   - Lower = faster, more consistent

4. **Batch Processing**:
   - Process all resumes in one run
   - More efficient than one-by-one

### For Better Quality:

1. **Use Larger Models** (if you have RAM):
   - Gemma 7B or 9B (better than 3B)
   - Llama 3 8B
   - Mistral 7B

2. **Increase Max Tokens**:
   - Already set to 3000 in code
   - Good balance for detailed analysis

---

## Troubleshooting

### "LLM not configured" Error
**Solution**: Make sure LM Studio server is running
- Open LM Studio
- Go to Local Server tab
- Click "Start Server"
- Look for "Server running on http://localhost:1234"

### "Connection refused" Error
**Solution**: Check the port
- LM Studio default: `http://localhost:1234/v1`
- If you changed it, update `ats_config.txt`

### Slow Processing
**Normal**: 30-90 seconds per resume is expected
**Speed up**:
- Close other applications
- Use GPU if available
- Reduce context length in LM Studio

### "JSON parsing error"
**Normal**: Happens occasionally with local models
**Handled**: Code has fallback scoring
**Improve**: Use clearer prompts (already optimized)

### Low Quality Results
**Try**:
- Use a larger model (7B+ parameters)
- Ensure resume PDFs have clear text
- Make job description more detailed

---

## Comparing Models

### Gemma 3B (Your Current Model)
- ✅ Fast (30-60 sec/resume)
- ✅ Low RAM usage (4-6 GB)
- ✅ Good for basic analysis
- ⚠️  May miss nuances

### Gemma 7B (Recommended Upgrade)
- ✅ Better understanding
- ✅ More accurate insights
- ✅ Better interview questions
- ⚠️  Slower (60-90 sec/resume)
- ⚠️  More RAM (8-12 GB)

### Llama 3 8B (Best Quality)
- ✅ Excellent understanding
- ✅ Very accurate
- ✅ Great recommendations
- ⚠️  Slower (60-120 sec/resume)
- ⚠️  More RAM (10-16 GB)

---

## Testing Your Setup

### Quick Test:

1. **Start LM Studio server**
2. **Put 1-2 test resumes** in `data/resumes/`
3. **Run**: `python advanced_ats.py`
4. **Check output**: Should see detailed analysis

### What Success Looks Like:

```
✓ Using Local LLM: google/gemma-3n-e4b at http://localhost:1234/v1
📋 Loading job description from: ./data/job_description.txt
✓ Job description loaded (2847 characters)
📁 Found 2 resume(s) to analyze
🤖 Using AI for deep semantic analysis...

⏳ [1/2] Processing: john_doe_resume.pdf
✓ Extracted 3421 characters from resume
🤖 Analyzing candidate information...
🤖 Performing deep skill analysis...
🤖 Analyzing work experience...
🤖 Analyzing education...
🤖 Calculating comprehensive match score...

🟢 OVERALL ATS SCORE: 78.5% - GOOD MATCH
```

---

## Advanced Tips

### 1. Parallel Processing (Future Enhancement)
Currently processes one resume at a time. Could be parallelized for multiple LLM instances.

### 2. Custom Prompts
Edit prompts in `advanced_ats.py` to focus on specific aspects:
- More emphasis on soft skills
- Industry-specific requirements
- Cultural fit criteria

### 3. Save Costs
Local LLM = **FREE** unlimited processing!
- No API costs
- No rate limits
- Complete privacy
- Process 1000s of resumes

### 4. Privacy
All processing happens locally:
- ✅ Resumes never leave your computer
- ✅ No data sent to cloud
- ✅ GDPR/privacy compliant
- ✅ Secure for confidential hiring

---

## Comparison: Local vs Cloud

| Feature | Local (LM Studio) | Cloud (OpenAI) |
|---------|------------------|----------------|
| Cost | FREE | $0.01-0.05/resume |
| Speed | 30-90 sec | 5-15 sec |
| Quality | Good-Excellent | Excellent |
| Privacy | 100% Private | Data sent to API |
| Limits | None | Rate limits |
| Setup | Install LM Studio | API key needed |
| Offline | ✅ Works offline | ❌ Needs internet |

---

## Next Steps

1. ✅ **Start LM Studio server** (if not running)
2. ✅ **Add your resumes** to `data/resumes/`
3. ✅ **Edit job description** in `data/job_description.txt`
4. ✅ **Run**: `python advanced_ats.py`
5. ✅ **Review results** and detailed reports

---

## Need Help?

### LM Studio Not Starting?
- Check if port 1234 is available
- Try restarting LM Studio
- Check LM Studio logs

### Model Not Loading?
- Ensure model is downloaded in LM Studio
- Check available RAM
- Try a smaller model

### Poor Results?
- Use more detailed job descriptions
- Ensure resume PDFs are text-based
- Try a larger model (7B+)

---

**You're all set! Start analyzing resumes with AI! 🚀**

```bash
python advanced_ats.py
```
