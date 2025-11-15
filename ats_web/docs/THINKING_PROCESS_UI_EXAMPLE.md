# AI Thinking Process - UI Example

## Visual Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Jaideep Bommidi                                                │
│  Jaideep_Bommidi.pdf                                           │
│                                                                 │
│  [Overall Score: 83%]  [YES - Strong match for the role]      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 🧠 AI Thinking Process                              [▼]   │ │
│  │    See how the AI reasoned through this evaluation        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [WHEN COLLAPSED - Shows only the header above]                │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 🧠 AI Thinking Process                              [▲]   │ │
│  │    See how the AI reasoned through this evaluation        │ │
│  ├───────────────────────────────────────────────────────────┤ │
│  │                                                           │ │
│  │  ┃ ① Understanding Requirements                          │ │
│  │  ┃    "Looking at this Principal Data Scientist role,    │ │
│  │  ┃    what are the critical requirements? I see they     │ │
│  │  ┃    need 8+ years of ML experience, expertise in       │ │
│  │  ┃    Python and PyTorch/TensorFlow..."                  │ │
│  │  ┃                                                        │ │
│  │  ┃ ② Technical Skills Assessment                         │ │
│  │  ┃    "Examining the candidate's technical skills - I    │ │
│  │  ┃    see Python, PyTorch, and TensorFlow prominently    │ │
│  │  ┃    featured. The experience with LLM fine-tuning..."  │ │
│  │  ┃                                                        │ │
│  │  ┃ ③ Experience Evaluation                               │ │
│  │  ┃    "With 10 years in ML engineering, the candidate    │ │
│  │  ┃    exceeds the 8+ year requirement. The work on       │ │
│  │  ┃    retrieval systems directly aligns..."              │ │
│  │  ┃                                                        │ │
│  │  ┃ ④ Gap Analysis                                        │ │
│  │  ┃    "I'm concerned about the lack of explicit          │ │
│  │  ┃    leadership experience mentioned. For a Principal   │ │
│  │  ┃    role, I'd expect to see team leadership..."        │ │
│  │  ┃                                                        │ │
│  │  ┃ ⑤ Standout Qualities                                  │ │
│  │  ┃    "What really impresses me is the deep expertise    │ │
│  │  ┃    in retrieval systems and LLM fine-tuning. This     │ │
│  │  ┃    is exactly what the role needs..."                 │ │
│  │  ┃                                                        │ │
│  │  ┃ ⑥ Final Assessment                                    │ │
│  │  ┃    "Weighing everything together: strong technical    │ │
│  │  ┃    match (85%), excellent experience (90%), but       │ │
│  │  ┃    some gaps in leadership visibility. Overall..."    │ │
│  │                                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  [WHEN EXPANDED - Shows all thinking steps]                    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Score Breakdown                                                │
│  Skills Match        ████████████████░░░░  85.0%              │
│  Experience Match    ██████████████████░░  90.0%              │
│  Education Match     ██████████████░░░░░░  70.0%              │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Color Scheme

- **Background (collapsed)**: Light purple `rgba(150, 124, 178, 0.05)`
- **Background (expanded)**: Slightly darker `rgba(150, 124, 178, 0.08)`
- **Border**: Purple `rgba(150, 124, 178, 0.2)`
- **Icon & Text**: Purple `#967CB2`
- **Thought Text**: Dark purple `#3B1C55` (italic)
- **Left Border**: Purple `rgba(150, 124, 178, 0.3)` (3px solid)

## Interactive States

### Hover (Collapsed)
```
┌───────────────────────────────────────────────────────────┐
│ 🧠 AI Thinking Process                              [▼]   │ ← Darker background
│    See how the AI reasoned through this evaluation        │   Stronger border
└───────────────────────────────────────────────────────────┘   Cursor: pointer
```

### Hover (Expanded)
```
┌───────────────────────────────────────────────────────────┐
│ 🧠 AI Thinking Process                              [▲]   │ ← Darker background
│    See how the AI reasoned through this evaluation        │   Stronger border
├───────────────────────────────────────────────────────────┤   Cursor: pointer
│  [Thinking steps...]                                      │
└───────────────────────────────────────────────────────────┘
```

## Animation

- **Expand/Collapse**: Smooth slide animation (300ms)
- **Arrow Rotation**: Rotates 180° when expanding
- **Transition**: All changes are animated smoothly

## Responsive Design

### Desktop (md and up)
- Full width section
- Comfortable padding
- All steps visible when expanded

### Mobile (sm and down)
- Adapts to screen width
- Maintains readability
- Touch-friendly click area

## Typography

- **Header**: `variant="h6"` - Bold, purple
- **Subtitle**: `variant="caption"` - Gray, smaller
- **Step Title**: `variant="subtitle2"` - Bold, purple, with number badge
- **Thought Text**: `variant="body2"` - Italic, dark purple, indented

## Number Badges

```
┌─────┐
│  ①  │  ← Circular badge
└─────┘    Background: rgba(150, 124, 178, 0.15)
           Size: 24x24px
           Font: Bold, 0.75rem
```

## Accessibility

- **Keyboard Navigation**: Can be focused and activated with Enter/Space
- **Screen Readers**: Proper ARIA labels
- **Color Contrast**: Meets WCAG AA standards
- **Focus Indicators**: Visible focus state

## Example in Context

```
Candidate Detail Page
├── Header (Name, Score, Recommendation)
├── 🧠 AI Thinking Process ← NEW FEATURE (Collapsible)
├── Score Breakdown (Skills, Experience, Education)
├── Executive Summary
├── Matched Skills / Missing Skills
├── Strengths / Weaknesses
└── Chat Interface
```

## User Flow

1. User uploads resume → Analysis runs
2. User clicks candidate → Detail page opens
3. User sees collapsed "AI Thinking Process" section
4. User clicks to expand → Smooth animation reveals thinking steps
5. User reads through the AI's reasoning
6. User clicks again to collapse → Section minimizes

## Mobile View

```
┌─────────────────────────┐
│ Jaideep Bommidi        │
│ Overall: 83%           │
├─────────────────────────┤
│ 🧠 AI Thinking    [▼]  │
│ Process                │
├─────────────────────────┤
│ Score Breakdown        │
│ Skills:  85%           │
│ Exp:     90%           │
│ Edu:     70%           │
└─────────────────────────┘
```

---

**Note**: The actual implementation uses Material-UI components for a polished, professional look with smooth animations and responsive design.
