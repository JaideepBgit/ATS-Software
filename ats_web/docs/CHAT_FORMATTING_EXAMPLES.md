# Chat Interface Formatting Examples

## Before vs After

### Before (Plain Text)
```
**Key Strengths:**
- Strong technical skills
- Good communication
```
This would display literally with the asterisks visible.

### After (Rich Markdown)
**Key Strengths:**
- Strong technical skills  
- Good communication

The text is now properly formatted with bold headings and bullet points.

---

## LaTeX Code Block Example

### How to Request LaTeX Code

**Question:** "Can you give me the LaTeX version of this candidate's resume?"

**Response:**
Here's a LaTeX template for the candidate's resume:

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{margin=1in}

\begin{document}

\section*{John Doe}
\textbf{Email:} john.doe@example.com \\
\textbf{Phone:} (555) 123-4567

\section*{Experience}
\textbf{Senior Software Engineer} \\
\textit{Tech Company Inc.} \hfill \textit{2020 - Present}
\begin{itemize}
    \item Led development of microservices architecture
    \item Improved system performance by 40\%
    \item Mentored junior developers
\end{itemize}

\section*{Skills}
Python, JavaScript, React, Node.js, Docker, Kubernetes

\end{document}
```

[Copy Button] ← Click this button in the top-right corner of the code block

---

## Formatting Features

### 1. Bold Text
Use `**text**` in your questions or the AI will use it in responses:
- **Important:** This is bold
- **Key Point:** Another bold item

### 2. Inline Code
Use backticks for inline code: `variable_name` or `function()`

### 3. Code Blocks
Use triple backticks with language specification:

```python
def analyze_resume(resume_text):
    return score
```

```javascript
const analyzeResume = (resumeText) => {
  return score;
};
```

```latex
\section{Education}
\textbf{Bachelor of Science in Computer Science}
```

### 4. Lists
Bullet points:
- Item 1
- Item 2
- Item 3

Numbered lists:
1. First step
2. Second step
3. Third step

### 5. Emphasis
- **Bold** for strong emphasis
- *Italic* for light emphasis
- `Code` for technical terms

---

## Tips for Best Results

1. **Ask for specific formats:** "Give me the LaTeX version" or "Format this as a code block"

2. **Use keywords:** Include "latex", "overleaf", or "tex" when you want LaTeX code

3. **Copy easily:** Hover over any code block to see the copy button

4. **Structured questions:** The AI will format responses with proper structure automatically

---

## Example Questions That Work Well

✅ "What are the **top 3 concerns** about this candidate?"
✅ "Can you provide a LaTeX template for their experience section?"
✅ "Give me the Overleaf-ready code for this resume"
✅ "Format the candidate's skills as a LaTeX itemize list"
✅ "What are the **key strengths** and **weaknesses**?"

---

## Technical Implementation

The chat interface now uses:
- **ReactMarkdown** for parsing markdown syntax
- **remark-gfm** for GitHub Flavored Markdown (tables, task lists, etc.)
- **rehype-highlight** for syntax highlighting
- **highlight.js** for code styling
- Custom copy-to-clipboard functionality with visual feedback

All code blocks automatically get:
- Syntax highlighting based on language
- Copy button in top-right corner
- Proper formatting and indentation
- Scrollable overflow for long code
