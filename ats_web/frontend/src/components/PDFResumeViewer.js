import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, TextField, Button, IconButton, CircularProgress, Divider } from '@mui/material';
import { Description, Chat, Close, Send } from '@mui/icons-material';
import { Document, Page, pdfjs } from 'react-pdf';
import SpeakButton from './SpeakButton';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

// Set up PDF.js worker - use version 2.16.105 that matches react-pdf 6.2.2
pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@2.16.105/build/pdf.worker.min.js`;

const PDFResumeViewer = ({ candidateId, candidateName }) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [selectedText, setSelectedText] = useState('');
  const [question, setQuestion] = useState('');
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [pdfUrl, setPdfUrl] = useState('');
  const [loadError, setLoadError] = useState('');

  useEffect(() => {
    fetchPDF();
  }, [candidateId]);

  const fetchPDF = () => {
    const encodedId = encodeURIComponent(candidateId);
    const url = `http://localhost:8000/api/resume/pdf/${encodedId}`;
    console.log('[PDFViewer] Loading PDF from:', url);
    setPdfUrl(url);
  };

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    console.log('[PDFViewer] PDF loaded successfully, pages:', numPages);
  };

  const onDocumentLoadError = (error) => {
    console.error('[PDFViewer] Error loading PDF:', error);
    console.error('[PDFViewer] PDF URL was:', pdfUrl);
    console.error('[PDFViewer] Candidate ID:', candidateId);
    setLoadError(`Failed to load PDF: ${error.message || 'File may not be available'}`);
  };

  const handleTextSelection = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text && text.length > 0) {
      console.log('[PDFViewer] Text selected:', text.substring(0, 50));
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

  const changePage = (offset) => {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  };

  const previousPage = () => {
    changePage(-1);
  };

  const nextPage = () => {
    changePage(1);
  };

  return (
    <Box sx={{ display: 'flex', gap: 2, height: '100%', p: 2 }}>
      {/* PDF Viewer */}
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

        {/* PDF Navigation */}
        {numPages && (
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            gap: 2, 
            p: 1,
            borderBottom: 1,
            borderColor: 'divider',
            backgroundColor: '#FBFAFA'
          }}>
            <Button 
              size="small" 
              onClick={previousPage} 
              disabled={pageNumber <= 1}
              sx={{ color: '#3B1C55' }}
            >
              Previous
            </Button>
            <Typography variant="body2" sx={{ color: '#3B1C55' }}>
              Page {pageNumber} of {numPages}
            </Typography>
            <Button 
              size="small" 
              onClick={nextPage} 
              disabled={pageNumber >= numPages}
              sx={{ color: '#3B1C55' }}
            >
              Next
            </Button>
          </Box>
        )}

        {/* PDF Document */}
        <Box 
          sx={{ 
            flex: 1,
            overflow: 'auto', 
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'flex-start',
            backgroundColor: '#f5f5f5',
            p: 2
          }}
          onMouseUp={handleTextSelection}
        >
          {loadError ? (
            <Box sx={{ textAlign: 'center', p: 4 }}>
              <Typography color="error">{loadError}</Typography>
            </Box>
          ) : (
            <Document
              file={pdfUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              onLoadError={onDocumentLoadError}
              loading={
                <Box sx={{ textAlign: 'center', p: 4 }}>
                  <CircularProgress sx={{ color: '#967CB2' }} />
                  <Typography sx={{ mt: 2 }}>Loading PDF...</Typography>
                </Box>
              }
            >
              <Page 
                pageNumber={pageNumber}
                renderTextLayer={true}
                renderAnnotationLayer={true}
                width={Math.min(window.innerWidth * 0.5, 800)}
              />
            </Document>
          )}
        </Box>

        {selectedText && (
          <Box sx={{ borderTop: 1, borderColor: 'divider', bgcolor: 'rgba(150, 124, 178, 0.1)', p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', gap: 2 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="body2" sx={{ fontWeight: 600, color: '#3B1C55', mb: 0.5 }}>
                  Selected Text:
                </Typography>
                <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                  "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
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
                <Paper elevation={1} sx={{ p: 1.5, bgcolor: '#FBFAFA' }}>
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
                bgcolor: '#967CB2',
                color: '#FBFAFA',
                '&:hover': {
                  bgcolor: '#7d5f9a',
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

export default PDFResumeViewer;
