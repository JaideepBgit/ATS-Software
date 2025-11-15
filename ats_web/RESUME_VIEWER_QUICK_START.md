# Interactive Resume Viewer - Quick Start

## What You Get

A split-screen interface where you can:
1. **View the resume** on the left
2. **Select any text** you want to ask about
3. **Ask questions** in the chat panel on the right
4. **Get AI answers** with context
5. **Hear answers** with text-to-speech

## Visual Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Resume Viewer                          [Show/Hide Chat]    │
├─────────────────────────────────┬───────────────────────────┤
│                                 │                           │
│  RESUME TEXT                    │   CHAT PANEL              │
│  ═══════════════                │   ════════════            │
│                                 │                           │
│  John Doe                       │   💬 Ask About Resume     │
│  Software Engineer              │                           │
│                                 │   ┌─────────────────────┐ │
│  Experience:                    │   │ You:                │ │
│  ► Senior Engineer at Google    │   │ What were their     │ │
│    (2020-2023)                  │   │ responsibilities?   │ │
│    - Led team of 5              │   └─────────────────────┘ │
│    - Built scalable systems     │                           │
│                                 │   ┌─────────────────────┐ │
│  Skills:                        │   │ AI:                 │ │
│  Python, React, AWS             │   │ Based on the resume │ │
│                                 │   │ they led a team...  │ │
│  [Selected: "Senior Engineer"]  │   │              🔊     │ │
│                                 │   └─────────────────────┘ │
│                                 │                           │
│                                 │   Ask a question...       │
│                                 │   [Ask Question]          │
└─────────────────────────────────┴───────────────────────────┘
```

## How to Use

### Step 1: Add to Your App

In your candidate detail page:

```jsx
import ResumeViewer from './components/ResumeViewer';

// Inside your component
<ResumeViewer 
  candidateId={candidate.candidate_id}
  candidateName={candidate.candidate_name}
/>
```

### Step 2: View Resume

- Resume loads automatically
- Scroll to read full content
- Clean, readable format

### Step 3: Select Text

- **Click and drag** to select any text
- Selected text appears in blue box at bottom
- Chat panel opens automatically
- Question is auto-suggested

### Step 4: Ask Questions

**With Selection:**
```
Select: "5 years Python experience"
Ask: "What Python projects did they work on?"
```

**Without Selection:**
```
Ask: "What is their education background?"
Ask: "Summarize their key achievements"
```

### Step 5: Get Answers

- AI analyzes resume + selected context
- Answer appears in chat
- Click 🔊 to hear answer
- Continue conversation

## Example Conversations

### Example 1: Deep Dive on Experience
```
👤 Select: "Senior Software Engineer at Google (2020-2023)"
👤 Ask: "What were their main responsibilities?"

🤖 Answer: "Based on the resume, as a Senior Software Engineer 
   at Google from 2020-2023, they led a team of 5 engineers, 
   built scalable distributed systems, and improved performance 
   by 40%."

👤 Ask: "What technologies did they use?"

🤖 Answer: "They worked with Python, Go, Kubernetes, and Google 
   Cloud Platform. They also mention experience with microservices 
   architecture and CI/CD pipelines."
```

### Example 2: Skills Assessment
```
👤 Select: "Python, React, AWS, Docker"
👤 Ask: "How many years of experience with each?"

🤖 Answer: "According to the resume: Python - 5 years, React - 
   3 years, AWS - 4 years, Docker - 3 years. They've used Python 
   throughout their career starting from 2018."

👤 Ask: "Any certifications?"

🤖 Answer: "Yes, they hold AWS Solutions Architect certification 
   obtained in 2021."
```

### Example 3: General Questions
```
👤 Ask: "What makes this candidate stand out?"

🤖 Answer: "Key strengths include: 1) Strong leadership experience 
   managing teams, 2) Track record of improving system performance, 
   3) Experience at top tech companies, 4) Full-stack capabilities 
   with both frontend and backend."

👤 Ask: "Any red flags?"

🤖 Answer: "No major concerns. The candidate shows consistent 
   career progression and relevant experience for the role."
```

## Integration Options

### Option A: As a Tab
```jsx
<Tabs>
  <Tab label="Analysis" />
  <Tab label="Interactive Resume" />
</Tabs>

{activeTab === 1 && (
  <ResumeViewer candidateId={id} candidateName={name} />
)}
```

### Option B: As a Modal
```jsx
<Button onClick={() => setShowResume(true)}>
  View Interactive Resume
</Button>

<Dialog open={showResume} maxWidth="xl" fullWidth>
  <ResumeViewer candidateId={id} candidateName={name} />
</Dialog>
```

### Option C: Standalone Page
```jsx
<Route path="/resume/:id" element={
  <ResumeViewer candidateId={id} candidateName={name} />
} />
```

## Features

### Smart Context
- Uses selected text as context
- Includes full resume
- Adds analysis scores
- Provides relevant answers

### Auto-Suggestions
When you select text:
- "Tell me more about: [text]"
- "Explain this experience"
- "What does this mean?"

### Conversation History
- All Q&A saved during session
- Shows context for each question
- Scroll through history
- Clear and organized

### Text-to-Speech
- Every answer has speak button
- Click to play
- Click again to stop
- Uses your TTS system

## Customization

### Change Colors
```jsx
// Resume header
className="bg-gradient-to-r from-blue-500 to-blue-600"

// Chat header
className="bg-gradient-to-r from-green-500 to-green-600"

// Question bubbles
className="bg-blue-500 text-white"

// Answer bubbles
className="bg-gray-100 text-gray-800"
```

### Adjust Layout
```jsx
// Resume width
className="flex-1"  // Takes remaining space

// Chat width
className="w-96"    // Fixed 384px width

// Change to: w-80, w-1/3, w-1/2, etc.
```

### Hide/Show Chat by Default
```jsx
const [showChat, setShowChat] = useState(true);  // Show by default
const [showChat, setShowChat] = useState(false); // Hide by default
```

## Tips

### Best Practices
1. **Select specific text** for focused questions
2. **Ask follow-up questions** to dig deeper
3. **Use speak button** for long answers
4. **Clear selection** when asking general questions

### Question Types
- **Clarification**: "What does this mean?"
- **Details**: "Tell me more about..."
- **Comparison**: "How does this compare to requirements?"
- **Assessment**: "Is this experience relevant?"
- **Summary**: "Summarize their background"

### Performance
- Resume loads once and caches
- Questions answered in 1-2 seconds
- TTS generation takes 2-3 seconds
- Smooth scrolling and selection

## Troubleshooting

### Resume Not Loading
- Check candidate_id is correct
- Verify resume was uploaded
- Check browser console for errors

### Questions Not Working
- Ensure backend is running
- Check RAG service is initialized
- Verify API endpoint is accessible

### Selection Not Working
- Make sure you're clicking and dragging
- Text must be inside resume area
- Try selecting again

### TTS Not Playing
- Check TTS service is running
- Verify audio files are generated
- Check browser audio permissions

## Next Steps

1. **Add to your app** - Import and use ResumeViewer
2. **Test it** - Select text and ask questions
3. **Customize** - Adjust colors and layout
4. **Enhance** - Add more features as needed

You now have an interactive resume viewer with AI-powered Q&A! 🚀
