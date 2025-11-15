# PDF Resume Viewer with Interactive Q&A

## What's New

✅ **PDF Display** - View actual PDF resume with original formatting
✅ **Text Selection** - Select text directly from the PDF
✅ **Page Navigation** - Browse through multi-page resumes
✅ **Interactive Q&A** - Ask questions about selected text
✅ **TTS Integration** - Hear answers spoken aloud

## Features

### PDF Viewing
- **Original Format**: See resume exactly as uploaded
- **Multi-Page Support**: Navigate through all pages
- **Zoom & Scroll**: Standard PDF viewing controls
- **Text Selection**: Select any text from the PDF

### Interactive Features
- **Select Text**: Click and drag to select text
- **Auto-Suggest Questions**: Question generated from selection
- **Contextual Answers**: AI uses selected text as context
- **Chat History**: Keep track of all Q&A
- **Text-to-Speech**: Hear answers read aloud

## How It Works

### Backend
1. **PDF Storage**: PDFs stored in `backend/data/resumes/pdfs/`
2. **PDF Endpoint**: `/api/resume/pdf/{candidate_id}` serves PDF files
3. **Q&A Endpoint**: `/api/resume/ask` handles questions

### Frontend
1. **react-pdf**: Renders PDF in browser
2. **Text Selection**: Captures selected text from PDF
3. **Chat Panel**: Manages Q&A interface
4. **TTS Integration**: Speaks answers

## Usage

### For Users
1. Click "View Interactive Resume" button
2. PDF loads with page navigation
3. Select any text in the PDF
4. Chat panel opens automatically
5. Ask questions about the selected text
6. Get AI-powered answers
7. Click 🔊 to hear answers

### Example Workflow
```
1. Open candidate detail page
2. Click "View Interactive Resume"
3. PDF displays with page 1
4. Navigate to experience section (page 2)
5. Select "Senior Engineer at Google"
6. Question auto-suggested
7. Modify or ask custom question
8. Get detailed answer
9. Click speak button to hear it
10. Continue asking follow-up questions
```

## Technical Details

### Libraries Used
- **react-pdf**: PDF rendering
- **pdfjs-dist**: PDF.js library
- **Material-UI**: UI components

### PDF.js Worker
Uses CDN-hosted worker:
```javascript
pdfjs.GlobalWorkerOptions.workerSrc = 
  `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;
```

### Text Selection
- Uses browser's native `window.getSelection()`
- Works with PDF text layer
- Captures selected text on `mouseup` event

### Page Navigation
- Previous/Next buttons
- Current page indicator
- Disabled when at first/last page

## API Endpoints

### GET /api/resume/pdf/{candidate_id}
Serves PDF file for viewing.

**Response**: PDF file (application/pdf)

**Example**:
```
GET /api/resume/pdf/John_Doe_2025-11-15T10:50:12.684695
```

### POST /api/resume/ask
Ask questions about resume (same as before).

**Request**:
```json
{
  "candidate_id": "John_Doe_2025-11-15T10:50:12.684695",
  "question": "What were their responsibilities?",
  "selected_text": "Senior Engineer at Google"
}
```

## Styling

### Color Palette (Your Theme)
- **Primary Purple**: `#3B1C55`
- **Secondary Purple**: `#967CB2`
- **Background**: `#FBFAFA`
- **Text**: `#3B1C55`

### Layout
```
┌─────────────────────────────────────────────────────────┐
│  PDF Viewer                          [Show/Hide Chat]   │
├─────────────────────────────────────┬───────────────────┤
│  [Previous] Page 1 of 3 [Next]      │                   │
├─────────────────────────────────────┤   CHAT PANEL      │
│                                     │   ════════════    │
│  ┌───────────────────────────────┐ │                   │
│  │                               │ │   💬 Questions    │
│  │   PDF CONTENT                 │ │                   │
│  │   (Original formatting)       │ │   🔊 Answers      │
│  │                               │ │                   │
│  │   [Selected text highlighted] │ │                   │
│  │                               │ │                   │
│  └───────────────────────────────┘ │                   │
│                                     │                   │
│  Selected: "Senior Engineer..."    │   [Ask Question]  │
└─────────────────────────────────────┴───────────────────┘
```

## Advantages Over Text View

### Better UX
- ✅ Original formatting preserved
- ✅ Professional appearance
- ✅ Familiar PDF interface
- ✅ Multi-page navigation
- ✅ Better readability

### Same Functionality
- ✅ Text selection works
- ✅ Q&A works
- ✅ TTS works
- ✅ Chat history works

## Files Created/Modified

### New Files
- `frontend/src/components/PDFResumeViewer.js` - PDF viewer component
- `PDF_RESUME_VIEWER.md` - This documentation

### Modified Files
- `backend/main.py` - Added `/api/resume/pdf` endpoint
- `frontend/src/components/CandidateDetail.js` - Uses PDFResumeViewer

### Packages Installed
```bash
npm install react-pdf pdfjs-dist react-pdf-highlighter
```

## Troubleshooting

### PDF Not Loading
- Check backend logs for PDF path
- Verify PDF file exists in `data/resumes/pdfs/`
- Check browser console for errors

### Text Selection Not Working
- Ensure PDF has text layer (not scanned image)
- Try selecting again
- Check if text layer is rendered

### Slow Loading
- Large PDFs take time to load
- Consider showing loading indicator
- PDF.js worker loads from CDN

### CORS Issues
- PDF served from same origin (localhost:8000)
- Should not have CORS issues
- Check browser console if problems

## Performance

### Optimization
- PDF loaded once per session
- Pages rendered on demand
- Text layer cached
- Worker loaded from CDN

### Considerations
- Large PDFs (>5MB) may be slow
- Multi-page PDFs need navigation
- Text selection requires text layer
- Worker download on first load

## Future Enhancements

### Possible Additions
- **Zoom controls**: In/out buttons
- **Search in PDF**: Find text
- **Highlight answers**: Show relevant sections
- **Annotations**: Mark important parts
- **Download PDF**: Save locally
- **Print**: Print resume
- **Thumbnail view**: See all pages
- **Full-screen mode**: Maximize PDF

## Quick Start

1. **Backend is ready** - PDF endpoint added
2. **Frontend updated** - Using PDFResumeViewer
3. **Packages installed** - react-pdf ready
4. **Test it** - Click "View Interactive Resume"

The PDF viewer is now live! 🎉
