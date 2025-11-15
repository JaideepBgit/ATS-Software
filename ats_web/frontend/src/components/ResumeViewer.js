import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, TextField, Button, IconButton, CircularProgress, Chip, Divider } from '@mui/material';
import { Description, Chat, Close, Send } from '@mui/icons-material';
import SpeakButton from './SpeakButton';

const ResumeViewer = ({ candidateId, candidateName }) => {
  const [resumeText, setResumeText] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchingResume, setIsFetchingResume] = useState(true);
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    fetchResumeText();
  }, [candidateId]);

  const fetchResumeText = async () => {
    try {
      console.log('[ResumeViewer] Fetching resume for:', candidateId);
      
      // URL encode the candidate ID to handle special characters
      const encodedId = encodeURIComponent(candidateId);
      console.log('[ResumeViewer] Encoded ID:', encodedId);
      
      const response = await fetch(`http://localhost:8000/api/resume/text/${encodedId}`);
      console.log('[ResumeViewer] Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('[ResumeViewer] Error response:', errorData);
        throw new Error(errorData.detail || 'Failed to fetch resume');
      }
      
      const data = await response.json();
      console.log('[ResumeViewer] Resume loaded, length:', data.text.length);
      setResumeText(data.text);
    } catch (error) {
      console.error('[ResumeViewer] Error fetching resume:', error);
      setResumeText(
        `Resume not available.\n\n` +
        `This could mean:\n` +
        `1. The resume hasn't been analyzed yet in this session\n` +
        `2. The backend was restarted and needs to reload data\n` +
        `3. The resume file wasn't stored properly\n\n` +
        `Try analyzing the resume again, or check the backend logs for more details.`
      );
    } finally {
      setIsFetchingResume(false);
    }
  };

  const handleTextSelection = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text) {
      setSelectedText(text);
      setShowChat(true);
      
      if (text.length > 20) {
        setQuestion(`Tell me more about: "${text.substring(0, 50)}..."`);
      }
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;

    const userMessage = {
      type: 'question',
      text: question,
      context: selectedText,
      timestamp: new Date().toISOString()
    };

    setConversations(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/resume/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          candidate_id: candidateId,
          question: question,
          selected_text: selectedText
        })
      });

      if (!response.ok) throw new Error('Failed to get answer');

      const data = await response.json();
      
      const answerMessage = {
        type: 'answer',
        text: data.answer,
        timestamp: new Date().toISOString()
      };

      setConversations(prev => [...prev, answerMessage]);
      
    } catch (error) {
      console.error('Error asking question:', error);
      const errorMessage = {
        type: 'answer',
        text: 'Sorry, I encountered an error processing your question.',
        timestamp: new Date().toISOString()
      };
      setConversations(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setQuestion('');
      setSelectedText('');
    }
  };

  const clearSelection = () => {
    setSelectedText('');
    setQuestion('');
    window.getSelection().removeAllRanges();
  };

  if (isFetchingResume) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: 12 }}>
        <CircularProgress sx={{ color: '#2196f3' }} size={32} />
        <Typography sx={{ ml: 3, color: 'text.secondary' }}>Loading resume...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', gap: 2, height: '100%', p: 2 }}>
      {/* Resume Viewer */}
      <Paper elevation={3} sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <Box sx={{ 
          backgroundColor: '#3B1C55',
          color: '#FBFAFA', 
          p: 2,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Description />
            <Box>
              <Typography variant="h6">{candidateName}'s Resume</Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                Select text to ask questions
              </Typography>
            </Box>
          </Box>
          <Button
            variant="contained"
            startIcon={<Chat />}
            onClick={() => setShowChat(!showChat)}
            sx={{
              backgroundColor: '#967CB2',
              color: '#FBFAFA',
              '&:hover': {
                backgroundColor: '#7d5f9a',
              }
            }}
          >
            {showChat ? 'Hide' : 'Show'} Chat
          </Button>
        </Box>

        <Box 
          sx={{ 
            p: 3, 
            overflow: 'auto', 
            maxHeight: '600px',
            userSelect: 'text'
          }}
          onMouseUp={handleTextSelection}
        >
          <Typography 
            component="pre" 
            sx={{ 
              whiteSpace: 'pre-wrap', 
              fontFamily: 'inherit',
              color: 'text.primary',
              lineHeight: 1.7
            }}
          >
            {resumeText}
          </Typography>
        </Box>

        {selectedText && (
          <Box sx={{ borderTop: 1, borderColor: 'divider', bgcolor: 'rgba(150, 124, 178, 0.1)', p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', gap: 2 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="body2" sx={{ fontWeight: 600, color: '#3B1C55', mb: 0.5 }}>
                  Selected Text:
                </Typography>
                <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                  "{selectedText}"
                </Typography>
              </Box>
              <IconButton size="small" onClick={clearSelection} title="Clear selection">
                <Close fontSize="small" />
              </IconButton>
            </Box>
          </Box>
        )}
      </Paper>

      {/* Chat Panel */}
      {showChat && (
        <Paper elevation={3} sx={{ width: 400, display: 'flex', flexDirection: 'column' }}>
          <Box sx={{ 
            backgroundColor: '#967CB2',
            color: '#FBFAFA', 
            p: 2,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}>
            <Chat />
            <Typography variant="h6">Ask About Resume</Typography>
          </Box>

          {/* Conversation Area */}
          <Box sx={{ flex: 1, p: 2, overflow: 'auto', maxHeight: '500px' }}>
            {conversations.length === 0 ? (
              <Box sx={{ textAlign: 'center', color: 'text.secondary', py: 8 }}>
                <Chat sx={{ fontSize: 48, opacity: 0.3, mb: 2 }} />
                <Typography variant="body2">Select text and ask questions</Typography>
              </Box>
            ) : (
              conversations.map((msg, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    justifyContent: msg.type === 'question' ? 'flex-end' : 'flex-start',
                    mb: 2
                  }}
                >
                  <Paper
                    elevation={1}
                    sx={{
                      maxWidth: '85%',
                      p: 1.5,
                      bgcolor: msg.type === 'question' ? '#967CB2' : '#FBFAFA',
                      color: msg.type === 'question' ? '#FBFAFA' : '#3B1C55'
                    }}
                  >
                    {msg.context && msg.type === 'question' && (
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          opacity: 0.8, 
                          display: 'block',
                          pb: 1,
                          mb: 1,
                          borderBottom: '1px solid rgba(255,255,255,0.3)'
                        }}
                      >
                        Context: "{msg.context.substring(0, 50)}..."
                      </Typography>
                    )}
                    <Box sx={{ display: 'flex', alignItems: 'start', gap: 1 }}>
                      <Typography variant="body2" sx={{ flex: 1 }}>
                        {msg.text}
                      </Typography>
                      {msg.type === 'answer' && (
                        <SpeakButton text={msg.text} size="sm" />
                      )}
                    </Box>
                  </Paper>
                </Box>
              ))
            )}

            {isLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                <Paper elevation={1} sx={{ p: 1.5, bgcolor: '#f5f5f5' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CircularProgress size={16} />
                    <Typography variant="body2" color="text.secondary">
                      Thinking...
                    </Typography>
                  </Box>
                </Paper>
              </Box>
            )}
          </Box>

          {/* Input Area */}
          <Box sx={{ borderTop: 1, borderColor: 'divider', p: 2 }}>
            <TextField
              fullWidth
              size="small"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleAskQuestion()}
              placeholder="Ask about the resume..."
              disabled={isLoading}
              sx={{ mb: 1 }}
            />
            <Button
              fullWidth
              variant="contained"
              endIcon={<Send />}
              onClick={handleAskQuestion}
              disabled={isLoading || !question.trim()}
              sx={{
                bgcolor: '#4caf50',
                '&:hover': {
                  bgcolor: '#388e3c',
                }
              }}
            >
              {isLoading ? 'Asking...' : 'Ask Question'}
            </Button>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default ResumeViewer;
