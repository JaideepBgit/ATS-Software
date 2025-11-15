import React, { useState, useEffect } from 'react';
import {
  Paper,
  Typography,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import RefreshIcon from '@mui/icons-material/Refresh';
import DescriptionIcon from '@mui/icons-material/Description';
import axios from 'axios';

function ResumeLibrary({ jobDescription, onAnalysisComplete, onViewResults }) {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(null);
  const [message, setMessage] = useState(null);
  const [analyzedResumes, setAnalyzedResumes] = useState(new Set());

  const loadResumes = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/resumes');
      setResumes(response.data.resumes || []);
    } catch (error) {
      console.error('Error loading resumes:', error);
      setMessage({ type: 'error', text: 'Failed to load resumes' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResumes();
  }, []);

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    
    setUploading(true);
    setMessage(null);

    for (const file of files) {
      if (!file.name.endsWith('.pdf')) {
        setMessage({ type: 'error', text: 'Only PDF files supported' });
        continue;
      }

      try {
        const formData = new FormData();
        formData.append('file', file);

        await axios.post('/api/upload-resume-only', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        setMessage({ type: 'success', text: `Uploaded ${file.name}` });
      } catch (error) {
        setMessage({
          type: 'error',
          text: error.response?.data?.detail || 'Upload failed'
        });
      }
    }

    setUploading(false);
    loadResumes();
  };

  const handleAnalyze = async (resumeId, candidateName) => {
    if (!jobDescription) {
      setMessage({ type: 'error', text: 'Please set job description first!' });
      return;
    }

    setAnalyzing(resumeId);
    setMessage(null);

    try {
      const response = await axios.post(`/api/analyze-resume/${resumeId}`);
      
      // Mark this resume as analyzed
      setAnalyzedResumes(prev => new Set([...prev, resumeId]));
      
      setMessage({
        type: 'success',
        text: `Analysis complete for ${candidateName}! Click "View Analysis" to see results.`
      });
      
      if (onAnalysisComplete) {
        onAnalysisComplete(response.data);
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Analysis failed'
      });
    } finally {
      setAnalyzing(null);
    }
  };

  const handleViewAnalysis = () => {
    if (onViewResults) {
      onViewResults();
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <Paper elevation={0} sx={{ p: 4, backgroundColor: '#FBFAFA' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5" gutterBottom sx={{ color: '#3B1C55', mb: 0.5 }}>
            Resume Library
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Upload resumes and analyze them against job descriptions
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <input
            accept=".pdf"
            style={{ display: 'none' }}
            id="resume-library-upload"
            multiple
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label htmlFor="resume-library-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<CloudUploadIcon />}
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Upload Resume'}
            </Button>
          </label>
          <Tooltip title="Refresh list">
            <IconButton onClick={loadResumes} disabled={loading}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {!jobDescription && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Set a job description first to analyze resumes
        </Alert>
      )}

      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : resumes.length === 0 ? (
        <Box sx={{ textAlign: 'center', p: 4, color: 'text.secondary' }}>
          <DescriptionIcon sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
          <Typography variant="h6" gutterBottom>
            No resumes uploaded yet
          </Typography>
          <Typography variant="body2">
            Upload PDF resumes to build your library
          </Typography>
        </Box>
      ) : (
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Candidate</TableCell>
                <TableCell>Filename</TableCell>
                <TableCell>Uploaded</TableCell>
                <TableCell>Size</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {resumes.map((resume) => (
                <TableRow key={resume.resume_id} hover>
                  <TableCell>
                    <Typography variant="body2" fontWeight={500}>
                      {resume.candidate_name}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="text.secondary">
                      {resume.original_filename}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="text.secondary">
                      {formatDate(resume.uploaded_at)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={formatFileSize(resume.file_size)}
                      size="small"
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                      {analyzedResumes.has(resume.resume_id) ? (
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={handleViewAnalysis}
                          sx={{ minWidth: 120 }}
                        >
                          View Analysis
                        </Button>
                      ) : (
                        <Button
                          variant="contained"
                          size="small"
                          startIcon={analyzing === resume.resume_id ? <CircularProgress size={16} color="inherit" /> : <AnalyticsIcon />}
                          onClick={() => handleAnalyze(resume.resume_id, resume.candidate_name)}
                          disabled={!jobDescription || analyzing === resume.resume_id}
                          sx={{ minWidth: 120 }}
                        >
                          {analyzing === resume.resume_id ? 'Analyzing...' : 'Analyze'}
                        </Button>
                      )}
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {resumes.length > 0 && (
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            {resumes.length} resume{resumes.length !== 1 ? 's' : ''} in library
          </Typography>
        </Box>
      )}
    </Paper>
  );
}

export default ResumeLibrary;
