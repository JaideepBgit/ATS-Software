import React, { useState, useEffect } from 'react';
import { Paper, TextField, Button, Typography, Box, Alert } from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import axios from 'axios';

function JobDescription({ jobDescription, setJobDescription }) {
  const [localJobDesc, setLocalJobDesc] = useState(jobDescription);
  const [companyName, setCompanyName] = useState('');
  const [roleName, setRoleName] = useState('');
  const [message, setMessage] = useState(null);

  useEffect(() => {
    loadJobDescription();
  }, []);

  const loadJobDescription = async () => {
    try {
      const response = await axios.get('/api/job-description');
      if (response.data.job_description) {
        setLocalJobDesc(response.data.job_description);
        setJobDescription(response.data.job_description);
        setCompanyName(response.data.company_name || '');
        setRoleName(response.data.role_name || '');
      }
    } catch (error) {
      console.error('Error loading job description:', error);
    }
  };

  const handleSave = async () => {
    try {
      await axios.post('/api/job-description', {
        job_description: localJobDesc,
        company_name: companyName,
        role_name: roleName
      });
      setJobDescription(localJobDesc);
      setMessage({ type: 'success', text: 'Job description saved successfully!' });
      setTimeout(() => setMessage(null), 3000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Error saving job description' });
    }
  };

  return (
    <Paper elevation={0} sx={{ p: 4, backgroundColor: '#FBFAFA' }}>
      <Typography variant="h5" gutterBottom sx={{ color: '#3B1C55', mb: 1 }}>
        Job Description
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Enter the job description to match candidates against
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 2 }}>
          {message.text}
        </Alert>
      )}

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          label="Company Name (Optional)"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          placeholder="Auto-extracted if left empty"
          variant="outlined"
          helperText="Leave empty to auto-extract from job description"
        />
        <TextField
          fullWidth
          label="Role Name (Optional)"
          value={roleName}
          onChange={(e) => setRoleName(e.target.value)}
          placeholder="Auto-extracted if left empty"
          variant="outlined"
          helperText="Leave empty to auto-extract from job description"
        />
      </Box>

      <TextField
        fullWidth
        multiline
        rows={12}
        value={localJobDesc}
        onChange={(e) => setLocalJobDesc(e.target.value)}
        placeholder="Paste job description here..."
        variant="outlined"
        sx={{ mb: 2 }}
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          {localJobDesc.length} characters
        </Typography>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={handleSave}
          disabled={!localJobDesc.trim()}
        >
          Save Job Description
        </Button>
      </Box>
    </Paper>
  );
}

export default JobDescription;
