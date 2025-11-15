# Quick TTS Integration - 5 Minutes

## What Changed

✅ **Backend**: Now uses single audio files (no more clutter)
✅ **New Endpoint**: `/api/tts/speak` for any text
✅ **New Components**: `SpeakButton` and `QuestionAnswer`

## Quick Start

### 1. Backend is Ready
The backend automatically reloaded with the changes. Test it:

```bash
# Test general TTS
curl -X POST http://localhost:8000/api/tts/speak \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello, this works!\"}"
```

### 2. Add Speak Button Anywhere

Copy `SpeakButton.js` to your components folder (already done), then use it:

```jsx
import SpeakButton from './components/SpeakButton';

// In any component, add next to text:
<div className="flex items-center gap-2">
  <p>Your text here</p>
  <SpeakButton text="Your text here" size="sm" />
</div>
```

### 3. Add Q&A Page (Optional)

If you want a Q&A interface:

```jsx
import QuestionAnswer from './components/QuestionAnswer';

// Add to your app
<QuestionAnswer />
```

## Real Examples

### Example 1: Add to Candidate Summary
In `CandidateDetail.js`:

```jsx
import SpeakButton from './SpeakButton';

// Find where you display executive summary
<div className="summary-section">
  <div className="flex items-center justify-between mb-2">
    <h3>Executive Summary</h3>
    <SpeakButton 
      text={candidate.executive_summary} 
      size="sm" 
    />
  </div>
  <p>{candidate.executive_summary}</p>
</div>
```

### Example 2: Add to Results List
In `ResultsList.js`:

```jsx
import SpeakButton from './SpeakButton';

// In each result card
<div className="result-card">
  <div className="flex justify-between">
    <div>
      <h3>{result.candidate_name}</h3>
      <p>Score: {result.overall_score}%</p>
    </div>
    <SpeakButton 
      text={`${result.candidate_name}, overall score ${result.overall_score} percent. ${result.hiring_recommendation}`}
      size="sm"
    />
  </div>
</div>
```

### Example 3: Speak Full Summary
Create a summary text and speak it:

```jsx
const summaryText = `
  Candidate: ${candidate.name}
  Overall Score: ${candidate.overall_score} percent
  Skills Match: ${candidate.skill_match_score} percent
  Recommendation: ${candidate.hiring_recommendation}
  Summary: ${candidate.executive_summary}
`;

<SpeakButton text={summaryText} variant="button" />
```

## Testing

1. **Start your frontend** (if not running):
   ```bash
   cd frontend
   npm start
   ```

2. **Test the speak button**: Add it to any component and click it

3. **Check it works**: You should hear the text spoken

## Files Created

- ✅ `backend/main.py` - Updated with single file + new endpoint
- ✅ `frontend/src/components/SpeakButton.js` - Reusable speak button
- ✅ `frontend/src/components/QuestionAnswer.js` - Q&A interface
- ✅ `TTS_USAGE_GUIDE.md` - Complete documentation
- ✅ `QUICK_TTS_INTEGRATION.md` - This file

## What You Get

1. **Single audio files**: No more disk clutter
   - `candidate_summary.wav` - For summaries
   - `speech.wav` - For questions/general text

2. **Speak any text**: Just pass text to `SpeakButton`

3. **Q&A with voice**: Use `QuestionAnswer` component

4. **Easy integration**: Drop `SpeakButton` anywhere

## Next Steps

1. Add `SpeakButton` to your existing components
2. Test it works
3. Optionally add the Q&A page
4. Customize styling to match your app

That's it! TTS is ready to use. 🎉
