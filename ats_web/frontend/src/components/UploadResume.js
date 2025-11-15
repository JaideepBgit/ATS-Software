import React, { useState } from 'react';
import { Paper, Button, Typography, Box, Alert, LinearProgress, List, ListItem, ListItemText } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

function UploadResume({ jobDescription, onUploadSuccess, onViewResults, resultsCount }) {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [justUploaded, setJustUploaded] = useState(false);

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    
    if (!jobDescription) {
      setMessage({ type: 'error', text: 'Please set job description first!' });
      return;
    }

    setUploading(true);
    setMessage(null);
    const results = [];

    for (const file of files) {
      if (!file.name.endsWith('.pdf')) {
        results.push({ name: file.name, status: 'error', message: 'Only PDF files supported' });
        continue;
      }

      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post('/api/upload-resume', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        results.push({
          name: file.name,
          status: 'success',
          candidate: response.data.result.candidate_name,
          score: response.data.result.overall_score
        });
      } catch (error) {
        results.push({
          name: file.name,
          status: 'error',
          message: error.response?.data?.detail || 'Upload failed'
        });
      }
    }

    setUploadedFiles(results);
    setUploading(false);
    setMessage({ type: 'success', text: `Processed ${results.length} file(s)` });
    setJustUploaded(true);
    onUploadSuccess();
  };

  return (
    <Paper elevation={0} sx={{ p: 4, backgroundColor: '#FBFAFA' }}>
      <Typography variant="h5" gutterBottom sx={{ color: '#3B1C55', mb: 1 }}>
        Upload Resumes
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Upload PDF resumes to analyze against the job description
      </Typography>

      {!jobDescription && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Please set a job description first before uploading resumes
        </Alert>
      )}

      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }}>
          {message.text}
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <input
          accept=".pdf"
          style={{ display: 'none' }}
          id="resume-upload"
          multiple
          type="file"
          onChange={handleFileUpload}
          disabled={uploading || !jobDescription}
        />
        <label htmlFor="resume-upload">
          <Button
            variant="contained"
            component="span"
            startIcon={<CloudUploadIcon />}
            disabled={uploading || !jobDescription}
            size="large"
          >
            Select PDF Files
          </Button>
        </label>
      </Box>

      {uploading && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" sx={{ mb: 1 }}>Processing resumes...</Typography>
          <LinearProgress />
        </Box>
      )}

      {uploadedFiles.length > 0 && (
        <Box>
          <Typography variant="h6" sx={{ mb: 1 }}>Upload Results:</Typography>
          <List>
            {uploadedFiles.map((file, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={file.name}
                  secondary={
                    file.status === 'success'
                      ? `✓ ${file.candidate} - Score: ${file.score}%`
                      : `✗ ${file.message}`
                  }
                  secondaryTypographyProps={{
                    color: file.status === 'success' ? 'success.main' : 'error.main'
                  }}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}

      {(justUploaded || resultsCount > 0) && (
        <Box sx={{ 
          mt: 3, 
          p: 3, 
          backgroundColor: 'rgba(99, 51, 148, 0.05)', 
          borderRadius: 2,
          border: '1px solid rgba(99, 51, 148, 0.2)',
          textAlign: 'center',
        }}>
          <Typography variant="h6" sx={{ mb: 1, color: '#3B1C55' }}>
            {resultsCount} Candidate{resultsCount !== 1 ? 's' : ''} Analyzed
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Ready to review the analysis results
          </Typography>
          <Button 
            variant="contained" 
            size="large"
            onClick={onViewResults}
          >
            View Results
          </Button>
        </Box>
      )}
    </Paper>
  );
}

export default UploadResume;
