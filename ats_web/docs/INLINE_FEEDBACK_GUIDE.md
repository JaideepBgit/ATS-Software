# Inline Feedback System Guide

## Overview

You can now provide feedback on ANY point in the Candidate Detail page by simply clicking on it. This helps build a high-quality training database for your model.

## What Can You Provide Feedback On?

### 1. Executive Summary
- Click anywhere in the summary text
- Mark if it's accurate or needs correction
- Provide what the correct summary should be

### 2. Matched Skills
- Click on any green skill chip
- Confirm if it's truly a match or incorrectly identified
- Suggest corrections if wrong

### 3. Missing Skills
- Click on any red skill chip
- Confirm if it's truly missing or actually present in resume
- Provide corrections

### 4. Strengths
- Click on any strength bullet point
- Mark if it's accurate or overstated
- Provide corrected version

### 5. Weaknesses
- Click on any weakness bullet point
- Confirm if it's a real weakness or incorrectly identified
- Suggest what it should say instead

## How to Use

### Step 1: Hover Over Any Item
When you hover over items, you'll see a small edit icon (✏️) appear.

### Step 2: Click to Open Feedback Form
Click on the item or the edit icon to open the inline feedback form.

### Step 3: Mark as Correct or Incorrect
- Click **✓ Correct** if the AI got it right
- Click **✗ Incorrect** if the AI made a mistake

### Step 4: Provide Details (Optional)
- If incorrect, type what it should say instead
- If correct, you can add additional notes

### Step 5: Save
Click "Save Feedback" and it's automatically stored in your database!

## Visual Indicators

- **Hover Effect**: Items highlight when you hover over them
- **Edit Icon**: Small pencil icon appears on hover
- **Feedback Form**: Expands below the item when clicked
- **Success Indicator**: "✓ Saved" chip appears after submission

## Example Workflow

### Scenario: Incorrect Missing Skill

1. You see "Python" listed as a missing skill
2. But you know the candidate has Python experience
3. Click on "Python" chip
4. Click **✗ Incorrect**
5. Type: "Candidate has 5 years of Python experience, mentioned in work history"
6. Click "Save Feedback"
7. Done! This feedback will help train the model

### Scenario: Overstated Strength

1. You see "Expert in Machine Learning" in strengths
2. But the candidate only has basic ML knowledge
3. Click on the strength
4. Click **✗ Incorrect**
5. Type: "Basic machine learning knowledge, not expert level"
6. Click "Save Feedback"
7. The model learns to be more accurate

## Benefits

### 1. Contextual Feedback
- Feedback is tied to specific points, not general responses
- More precise training data

### 2. Quick and Easy
- No need to open separate forms
- Inline editing right where you see the issue

### 3. Comprehensive Coverage
- Every AI-generated point can be corrected
- Builds a complete training dataset

### 4. Visual Learning
- Hover effects guide you to clickable items
- Clear visual feedback on submission

## Data Stored

Each feedback submission includes:

```json
{
  "interaction_id": "candidate_123_missing_skill_1699999999",
  "query": "Is this missing_skill accurate: 'Python'?",
  "context": ["missing_skill", "Python"],
  "response": "Python",
  "rating": 2,
  "correct_points": [],
  "incorrect_points": ["Python"],
  "ideal_response": "Candidate has 5 years of Python experience"
}
```

## Tips for Effective Feedback

### Be Specific
❌ "This is wrong"
✅ "Candidate has Python listed in skills section, not missing"

### Provide Context
❌ "No"
✅ "This is overstated - candidate has 2 years experience, not 10"

### Use Both Correct and Incorrect
- Don't just mark things as wrong
- Also confirm when the AI gets it right
- This helps the model learn what's good

### Focus on High-Impact Items
- Executive summary (most important)
- Missing skills (often incorrect)
- Weaknesses (can be subjective)

## Integration with Training

All feedback is automatically:
1. Stored in ChromaDB with embeddings
2. Indexed in FAISS for fast retrieval
3. Backed up to JSONL file
4. Ready for LoRA training

Once you have 100+ feedback samples:
```bash
cd ../ats_lora_training
python database_builder.py --input ../ats_web/backend/feedback_db/interactions.jsonl
python lora_trainer.py
```

## Keyboard Shortcuts

- **Click item**: Open feedback form
- **Esc**: Close feedback form (coming soon)
- **Enter**: Submit feedback (when in text field)

## Troubleshooting

### Feedback Form Not Opening
- Make sure you're clicking directly on the text/chip
- Check browser console for errors

### Feedback Not Saving
- Check backend is running
- Verify ChromaDB is installed: `pip install chromadb`
- Check network tab in DevTools

### Edit Icon Not Appearing
- Hover directly over the item
- Some items may need a full hover to show the icon

## Statistics

View your feedback collection progress:
```bash
curl http://localhost:8000/api/feedback/statistics
```

Response:
```json
{
  "total_feedback": 150,
  "average_rating": 3.8,
  "chromadb_count": 150,
  "faiss_count": 150
}
```

## Next Steps

1. **Analyze Multiple Candidates**: Review 10-20 candidates and provide feedback
2. **Focus on Errors**: Pay special attention to incorrect assessments
3. **Build Dataset**: Aim for 100+ feedback samples
4. **Train Model**: Use the collected data to fine-tune your model
5. **Iterate**: Deploy improved model, collect more feedback, retrain

## Questions?

The inline feedback system makes it incredibly easy to build a high-quality training dataset. Every click helps improve the AI's accuracy!
