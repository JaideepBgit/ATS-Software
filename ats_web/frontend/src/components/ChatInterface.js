import { useState } from 'react';
import {
  Paper, Typography, Box, TextField, Button, List, ListItem,
  CircularProgress, Chip, IconButton, Tooltip
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css';
import FeedbackCollector from './FeedbackCollector';

function ChatInterface({ candidate, jobDescription }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopyCode = (code, index) => {
    navigator.clipboard.writeText(code);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const suggestedQuestions = [
    "What are the **biggest concerns** about this candidate?",
    "How does their experience compare to the job requirements?",
    "What specific questions should I ask in the interview?",
    "Give me a LaTeX version of their key qualifications",
    "Can they handle the technical requirements?"
  ];

  const handleAskQuestion = async (questionText) => {
    if (!questionText.trim()) return;

    const userMessage = { role: 'user', content: questionText, query: questionText };
    setMessages([...messages, userMessage]);
    setQuestion('');
    setLoading(true);

    try {
      const response = await axios.post('/api/ask', {
        candidate_id: `${candidate.candidate_name}_${candidate.timestamp}`,
        question: questionText
      });

      const aiMessage = { 
        role: 'assistant', 
        content: response.data.answer,
        query: questionText,
        context: response.data.context || []
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Error: Unable to get response. Please try again.',
        query: questionText,
        context: []
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestedQuestion = (q) => {
    handleAskQuestion(q);
  };

  return (
    <Paper elevation={0} sx={{ p: 4, backgroundColor: '#FBFAFA' }}>
      <Typography variant="h5" gutterBottom sx={{ color: '#3B1C55', mb: 1 }}>
        Ask Questions About This Candidate
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Get AI-powered insights and recommendations
      </Typography>

      {messages.length === 0 && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="body2" sx={{ mb: 1 }}>Suggested questions:</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {suggestedQuestions.map((q, index) => (
              <Chip
                key={index}
                label={q}
                onClick={() => handleSuggestedQuestion(q)}
                clickable
                size="small"
              />
            ))}
          </Box>
        </Box>
      )}

      <Box
        sx={{
          height: 400,
          overflowY: 'auto',
          mb: 2,
          p: 2,
          backgroundColor: 'rgba(59, 28, 85, 0.03)',
          borderRadius: 2,
          border: '1px solid rgba(59, 28, 85, 0.1)',
        }}
      >
        {messages.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 10 }}>
            Ask a question to start the conversation
          </Typography>
        ) : (
          <List>
            {messages.map((msg, index) => (
              <ListItem
                key={index}
                sx={{
                  flexDirection: 'column',
                  alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  mb: 1
                }}
              >
                <Box
                  sx={{
                    maxWidth: '80%',
                    p: 2,
                    borderRadius: 2,
                    backgroundColor: msg.role === 'user' ? '#633394' : '#FBFAFA',
                    color: msg.role === 'user' ? '#FBFABA' : '#3B1C55',
                    border: '1px solid rgba(59, 28, 85, 0.15)',
                    boxShadow: '0 1px 3px rgba(59, 28, 85, 0.1)',
                    '& pre': {
                      position: 'relative',
                      backgroundColor: '#f6f8fa',
                      padding: '16px',
                      borderRadius: '6px',
                      overflow: 'auto',
                      border: '1px solid #d0d7de',
                      marginTop: '8px',
                      marginBottom: '8px',
                    },
                    '& code': {
                      fontFamily: 'Consolas, Monaco, "Courier New", monospace',
                      fontSize: '0.875rem',
                    },
                    '& p': {
                      margin: '8px 0',
                    },
                    '& strong': {
                      fontWeight: 700,
                      color: msg.role === 'user' ? '#FBFAFA' : '#3B1C55',
                    },
                    '& ul, & ol': {
                      paddingLeft: '20px',
                      margin: '8px 0',
                    },
                  }}
                >
                  {msg.role === 'user' ? (
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {msg.content}
                    </Typography>
                  ) : (
                    <>
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        rehypePlugins={[rehypeHighlight]}
                        components={{
                          code({ node, inline, className, children, ...props }) {
                            const codeString = String(children).replace(/\n$/, '');
                            
                            return !inline ? (
                              <Box sx={{ position: 'relative' }}>
                                <Tooltip title={copiedIndex === `${index}-${codeString}` ? "Copied!" : "Copy code"}>
                                  <IconButton
                                    size="small"
                                    onClick={() => handleCopyCode(codeString, `${index}-${codeString}`)}
                                    sx={{
                                      position: 'absolute',
                                      right: 8,
                                      top: 8,
                                      backgroundColor: 'rgba(255, 255, 255, 0.8)',
                                      '&:hover': {
                                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                                      },
                                      zIndex: 1,
                                    }}
                                  >
                                    <ContentCopyIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <pre>
                                  <code className={className} {...props}>
                                    {children}
                                  </code>
                                </pre>
                              </Box>
                            ) : (
                              <code
                                className={className}
                                style={{
                                  backgroundColor: 'rgba(59, 28, 85, 0.1)',
                                  padding: '2px 6px',
                                  borderRadius: '3px',
                                  fontSize: '0.875em',
                                }}
                                {...props}
                              >
                                {children}
                              </code>
                            );
                          },
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                      <FeedbackCollector 
                        message={msg} 
                        messageIndex={index}
                        candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                      />
                    </>
                  )}
                </Box>
              </ListItem>
            ))}
            {loading && (
              <ListItem sx={{ justifyContent: 'center' }}>
                <CircularProgress size={24} />
              </ListItem>
            )}
          </List>
        )}
      </Box>

      <Box sx={{ display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about this candidate..."
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleAskQuestion(question);
            }
          }}
          disabled={loading}
        />
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          onClick={() => handleAskQuestion(question)}
          disabled={loading || !question.trim()}
        >
          Ask
        </Button>
      </Box>
    </Paper>
  );
}

export default ChatInterface;
