# How to View the Interactive Resume

## Where to Find It

### Step 1: Open a Candidate
1. Go to your ATS web interface
2. Click on any candidate from the results list
3. You'll see the candidate detail page

### Step 2: Click "View Interactive Resume"
Look for the purple button at the top of the candidate detail page:

```
┌─────────────────────────────────────────────────────┐
│  John Doe                                           │
│  resume.pdf                                         │
│                                                     │
│  [Overall: 85%] [Hire] [🔊 Speak] [📄 View Resume] │
│                                    ↑                │
│                              CLICK HERE!            │
└─────────────────────────────────────────────────────┘
```

### Step 3: Interactive Resume Opens
A full-screen dialog will open with:
- **Left side**: The resume text (scrollable)
- **Right side**: Chat panel for questions

## What You Can Do

### 1. Read the Resume
- Scroll through the full resume text
- Clean, readable format
- All content visible

### 2. Select Text
- Click and drag to select any text
- Example: Select "5 years Python experience"
- The chat panel opens automatically
- A question is suggested

### 3. Ask Questions

**About Selected Text:**
```
Select: "Senior Engineer at Google (2020-2023)"
Ask: "What were their main responsibilities?"
```

**General Questions:**
```
Ask: "What is their education background?"
Ask: "Summarize their key achievements"
Ask: "What makes them a good fit?"
```

### 4. Get AI Answers
- AI analyzes the resume
- Provides contextual answers
- Uses selected text as context
- References full resume

### 5. Listen to Answers
- Every answer has a 🔊 button
- Click to hear the answer
- Click again to stop

## Visual Guide

```
┌─────────────────────────────────────────────────────────────────┐
│  Interactive Resume Viewer                          [X Close]   │
├──────────────────────────────────┬──────────────────────────────┤
│                                  │                              │
│  📄 John Doe's Resume            │  💬 Ask About Resume         │
│  [Select text to ask questions]  │  [Show/Hide Chat]            │
│                                  │                              │
│  ┌────────────────────────────┐ │  ┌────────────────────────┐ │
│  │ JOHN DOE                   │ │  │ You:                   │ │
│  │ Software Engineer          │ │  │ What were their main   │ │
│  │                            │ │  │ responsibilities?      │ │
│  │ EXPERIENCE:                │ │  └────────────────────────┘ │
│  │ ► Senior Engineer at Google│ │                              │
│  │   (2020-2023)              │ │  ┌────────────────────────┐ │
│  │   - Led team of 5          │ │  │ AI:                    │ │
│  │   - Built scalable systems │ │  │ Based on the resume... │ │
│  │                            │ │  │                   🔊   │ │
│  │ SKILLS:                    │ │  └────────────────────────┘ │
│  │ Python, React, AWS         │ │                              │
│  │                            │ │  [Type your question...]     │
│  │ EDUCATION:                 │ │  [Ask Question]              │
│  │ MS Computer Science        │ │                              │
│  └────────────────────────────┘ │                              │
│                                  │                              │
│  Selected: "Senior Engineer..."  │                              │
│                                  │                              │
└──────────────────────────────────┴──────────────────────────────┘
```

## Example Workflow

### Scenario: Checking Experience Details

1. **Open candidate** → Click "View Interactive Resume"
2. **Find experience section** → Scroll to work history
3. **Select text** → Highlight "Senior Engineer at Google (2020-2023)"
4. **Ask question** → "What technologies did they use?"
5. **Read answer** → AI explains: "They worked with Python, Go, Kubernetes..."
6. **Listen** → Click 🔊 to hear the answer
7. **Follow up** → Ask "How many years of Python?"
8. **Continue** → Keep asking questions

## Tips

### Best Practices
- **Select specific text** for focused questions
- **Ask follow-up questions** to dig deeper
- **Use the speak button** for long answers
- **Clear selection** (click X) for general questions

### Question Ideas
- "Tell me more about this experience"
- "What skills are mentioned here?"
- "How does this relate to our requirements?"
- "What are their key achievements?"
- "Summarize their education"
- "What makes them qualified?"

### Keyboard Shortcuts
- **Enter** → Submit question
- **Esc** → Close dialog
- **Click & Drag** → Select text

## Troubleshooting

### Can't See the Button?
- Make sure you're on the candidate detail page
- Look for the purple "View Interactive Resume" button
- It's next to the "Speak" button

### Resume Not Loading?
- Check that the resume was uploaded
- Refresh the page
- Check browser console for errors

### Questions Not Working?
- Ensure backend is running
- Check internet connection
- Try a simpler question first

### Selection Not Working?
- Click and drag across text
- Make sure you're in the resume area (left side)
- Try selecting again

## Where Is It?

**Location in UI:**
```
Home → Results List → Click Candidate → [View Interactive Resume] Button
```

**Button Location:**
- Top of candidate detail page
- Next to the TTS "Speak" button
- Purple color with document icon 📄

That's it! Click the button and start exploring resumes interactively! 🚀
