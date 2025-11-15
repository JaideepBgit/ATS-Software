# Interactive Resume Viewer with Q&A

## Overview
View resumes directly in the platform, select text, and ask contextual questions with AI-powered answers and text-to-speech.

## Features

✅ **Resume Viewer** - Display full resume text in a clean, readable format
✅ **Text Selection** - Select any part of the resume
✅ **Contextual Q&A** - Ask questions about selected text
✅ **AI Answers** - Get intelligent responses using RAG
✅ **Text-to-Speech** - Hear answers spoken aloud
✅ **Chat History** - Keep track of all questions and answers

## How It Works

### User Flow
1. **View Resume** - Open candidate's resume in the viewer
2. **Select Text** - Highlight any text (e.g., "5 years Python experience")
3. **Ask Question** - Type question (e.g., "What projects did they work on?")
4. **Get Answer** - AI analyzes resume and provides contextual answer
5. **Listen** - Click speak button to hear the answer

### Example Interactions

**Scenario 1: Experience Details**
- Select: "Senior Software Engineer at Google (2020-2023)"
- Ask: "What were their main responsibilities?"
- Answer: "Based on the resume, they led a team of 5 engineers..."

**Scenario 2: Skills Verification**
- Select: "Python, React, AWS"
- Ask: "How many years of Python experience?"
- Answer: "The candidate has 5 years of Python experience..."

**Scenario 3: General Questions**
- No selection needed
- Ask: "What is their highest education level?"
- Answer: "The candidate holds a Master's degree in Computer Science..."

## Backend Implementation

### New Endpoints

#### 1. Get Resume Text
```
GET /api/resume/text/{candidate_id}
```

Returns full resume text for viewing.

**Response:**
```json
{
  "status": "success",
  "candidate_id": "John_Doe_2025-11-14",
  "text": "Full resume text here...",
  "has_analysis": true
}
```

#### 2. Ask About Resume
```
POST /api/resume/ask
```

Ask questions about resume with optional context.

**Request:**
```json
{
  "candidate_id": "John_Doe_2025-11-14",
  "question": "What were their main responsibilities?",
  "selected_text": "Senior Software Engineer at Google"
}
```

**Response:**
```json
{
  "status": "success",
  "question": "What were their main responsibilities?",
  "answer": "Based on the resume, they led a team...",
  "has_context": true
}
```

## Frontend Components

### ResumeViewer Component
Main component for viewing and interacting with resumes.

**Props:**
- `candidateId` - Candidate identifier
- `candidateName` - Candidate name for display

**Features:**
- Split-screen layout (resume + chat)
- Text selection detection
- Auto-generated question suggestions
- Conversation history
- TTS integration

**Usage:**
```jsx
import ResumeViewer from './components/ResumeViewer';

<ResumeViewer 
  candidateId="John_Doe_2025-11-14"
  candidateName="John Doe"
/>
```

### ResumeViewerTab Component
Wrapper to add as a tab in existing views.

**Usage:**
```jsx
import ResumeViewerTab from './components/ResumeViewerTab';

<ResumeViewerTab candidate={candidate} />
```

## Integration Guide

### Option 1: Add to CandidateDetail

In `CandidateDetail.js`:

```jsx
import ResumeViewer from './ResumeViewer';
import { Tabs, Tab } from '@mui/material';

// Add state
const [activeTab, setActiveTab] = useState(0);

// Add tabs
<Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
  <Tab label="Analysis" />
  <Tab label="Interactive Resume" />
</Tabs>

// Add resume viewer panel
{activeTab === 1 && (
  <ResumeViewer 
    candidateId={candidate.candidate_id}
    candidateName={candidate.candidate_name}
  />
)}
```

### Option 2: Standalone Page

Create a new route:

```jsx
import ResumeViewer from './components/ResumeViewer';

function ResumeViewPage({ match }) {
  const candidateId = match.params.id;
  
  return (
    <div className="container mx-auto p-6">
      <ResumeViewer 
        candidateId={candidateId}
        candidateName="Candidate Name"
      />
    </div>
  );
}
```

### Option 3: Modal/Dialog

```jsx
import { Dialog } from '@mui/material';
import ResumeViewer from './ResumeViewer';

<Dialog open={open} onClose={handleClose} maxWidth="xl" fullWidth>
  <ResumeViewer 
    candidateId={selectedCandidate.id}
    candidateName={selectedCandidate.name}
  />
</Dialog>
```

## UI/UX Features

### Resume Panel
- Clean, readable text display
- Scrollable content
- Text selection enabled
- Selected text highlight
- Clear selection button

### Chat Panel
- Collapsible sidebar
- Question input
- Conversation history
- Context indicators
- TTS buttons on answers
- Loading states

### Interactions
- **Select text** → Auto-opens chat panel
- **Auto-suggest** → Generates question from selection
- **Enter key** → Submit question
- **Speak button** → Hear answer
- **Clear** → Remove selection

## Styling

The component uses Tailwind CSS classes. Key styles:

```jsx
// Resume panel
className="flex-1 bg-white rounded-lg shadow-lg"

// Chat panel
className="w-96 bg-white rounded-lg shadow-lg"

// Question bubble
className="bg-blue-500 text-white rounded-lg p-3"

// Answer bubble
className="bg-gray-100 text-gray-800 rounded-lg p-3"
```

Customize colors to match your theme.

## Advanced Features

### 1. Smart Context
The system automatically includes:
- Selected text (if any)
- Full resume text
- Analysis results (scores, recommendations)

### 2. Question Suggestions
When text is selected, auto-generates questions like:
- "Tell me more about: [selected text]"
- "Explain this experience"
- "What skills are mentioned here?"

### 3. Conversation Memory
Maintains chat history during session:
- All questions and answers
- Context for each question
- Timestamps

### 4. TTS Integration
Every answer includes a speak button:
- Click to hear answer
- Click again to stop
- Uses single audio file (no clutter)

## API Integration

### RAG Service
The backend uses the existing RAG service:

```python
answer = rag_service.query(
    question=question,
    context=context
)
```

Context includes:
- Selected text (if any)
- Full resume
- Analysis summary

### Error Handling
- Resume not found → 404 error
- Question empty → 400 error
- RAG failure → 500 error with message

## Testing

### Test Resume Viewing
1. Open candidate detail
2. Click "Interactive Resume" tab
3. Verify resume text displays

### Test Text Selection
1. Select any text in resume
2. Verify selection shows in blue box
3. Verify chat panel opens
4. Verify question is auto-suggested

### Test Q&A
1. Type question
2. Press Enter or click "Ask Question"
3. Verify answer appears
4. Verify speak button works

### Test Without Selection
1. Clear any selection
2. Ask general question
3. Verify answer uses full resume context

## Performance

### Optimizations
- Resume text cached after first load
- Single audio file for TTS
- Lazy loading of chat panel
- Efficient text selection detection

### Considerations
- Large resumes (>10 pages) may need pagination
- Many questions may need conversation limits
- TTS generation takes 1-3 seconds

## Future Enhancements

### Possible Additions
- **Highlight matching text** in resume when answering
- **Export conversation** as PDF
- **Compare candidates** side-by-side
- **Smart suggestions** based on job requirements
- **Multi-language support** for resumes
- **PDF viewer** instead of text-only
- **Annotation tools** to mark important sections

## Files Created

- ✅ `backend/main.py` - Added `/api/resume/ask` and `/api/resume/text` endpoints
- ✅ `frontend/src/components/ResumeViewer.js` - Main viewer component
- ✅ `frontend/src/components/ResumeViewerTab.js` - Tab wrapper
- ✅ `INTERACTIVE_RESUME_VIEWER.md` - This documentation

## Quick Start

1. **Backend is ready** - Endpoints added to main.py
2. **Import component** - Add to your candidate view
3. **Test it** - Select text and ask questions
4. **Customize** - Adjust styling and layout

The interactive resume viewer is ready to use! 🎉
