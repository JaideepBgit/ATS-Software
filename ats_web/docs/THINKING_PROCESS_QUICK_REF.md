# AI Thinking Process - Quick Reference

## 🎯 What Is It?
Chain-of-thought reasoning display showing how the AI evaluated a candidate. Similar to ChatGPT's reasoning or Perplexity's thought process.

## 📍 Where?
**Candidate Detail page** → Right after candidate header, before score breakdown

## 🎨 Look
- 🧠 Brain icon
- Purple theme (#967CB2)
- Collapsible section
- 6 numbered thinking steps

## 🔧 Files Changed

| File | What Changed |
|------|--------------|
| `backend/ats_service.py` | Added `thinking_process` field + generation logic |
| `frontend/src/components/CandidateDetail.js` | Added collapsible UI section |
| `README.md` | Updated features list |

## 📊 The 6 Thinking Steps

1. **Understanding Requirements** - What does the role need?
2. **Technical Skills Assessment** - What skills does candidate have?
3. **Experience Evaluation** - How does experience align?
4. **Gap Analysis** - What's missing or concerning?
5. **Standout Qualities** - What impresses me?
6. **Final Assessment** - Overall conclusion

## 🚀 Quick Test

```bash
# Backend test only
cd ats_web
python test_thinking_process.py

# Full app test
cd ats_web/backend && python main.py
cd ats_web/frontend && npm start
```

## 💡 Key Features

✅ Collapsible (starts minimized)  
✅ Self-questioning AI  
✅ 6 systematic steps  
✅ Smooth animations  
✅ Purple theme  
✅ Mobile responsive  

## 🎮 User Actions

| Action | Result |
|--------|--------|
| Click header | Expand/collapse |
| Hover | Highlight effect |
| Expand | See all 6 thinking steps |
| Collapse | Minimize to save space |

## 📖 Documentation

- `THINKING_PROCESS_FEATURE.md` - Feature overview
- `THINKING_PROCESS_GUIDE.md` - Complete guide
- `THINKING_PROCESS_SUMMARY.md` - Implementation summary
- `THINKING_PROCESS_UI_EXAMPLE.md` - Visual examples
- `THINKING_PROCESS_QUICK_REF.md` - This file

## 🔄 Customization

**Change default state (collapsed → expanded):**
```javascript
// CandidateDetail.js, line ~7
const [thinkingExpanded, setThinkingExpanded] = useState(true);
```

**Change colors:**
```javascript
// CandidateDetail.js, search for #967CB2
backgroundColor: 'rgba(150, 124, 178, 0.08)', // Change RGB
color: '#967CB2', // Change hex
```

**Add more steps:**
```python
# ats_service.py, _generate_thinking_process()
# Add more questions in the prompt
```

## ✅ Status
**Ready to use!** Upload a resume and check the Candidate Detail page.

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Not showing | Check if LLM is running |
| Empty | Check backend logs for errors |
| Styling off | Clear browser cache (Ctrl+F5) |

---

**Quick Start**: Upload resume → Click candidate → Look for 🧠 icon → Click to expand
