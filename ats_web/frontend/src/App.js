import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Container, Box, AppBar, Toolbar, Typography, Tabs, Tab, CssBaseline, Button } from '@mui/material';
import WorkIcon from '@mui/icons-material/Work';
import AssignmentIcon from '@mui/icons-material/Assignment';
import JobDescription from './components/JobDescription';
import UploadResume from './components/UploadResume';
import ResumeLibrary from './components/ResumeLibrary';
import ResultsList from './components/ResultsList';
import CandidateDetail from './components/CandidateDetail';
import JobTracking from './components/JobTracking';

const theme = createTheme({
  palette: {
    primary: { main: '#633394' },
    secondary: { main: '#967CB2' },
    background: {
      default: '#FBFAFA',
      paper: '#FBFAFA',
    },
    text: {
      primary: '#3B1C55',
      secondary: '#61382E',
    },
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", sans-serif',
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          border: '1px solid rgba(59, 28, 85, 0.15)',
          boxShadow: '0 2px 8px rgba(59, 28, 85, 0.08)',
          transition: 'all 0.3s ease',
          '&:hover': {
            boxShadow: '0 4px 16px rgba(59, 28, 85, 0.12)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
          padding: '8px 20px',
          transition: 'all 0.2s ease',
        },
        contained: {
          backgroundColor: '#633394',
          boxShadow: 'none',
          '&:hover': {
            backgroundColor: '#967CB2',
            boxShadow: '0 2px 8px rgba(99, 51, 148, 0.25)',
          },
        },
        outlined: {
          borderColor: '#967CB2',
          color: '#633394',
          '&:hover': {
            borderColor: '#633394',
            backgroundColor: 'rgba(99, 51, 148, 0.04)',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            backgroundColor: '#FBFAFA',
            transition: 'all 0.2s ease',
            '& fieldset': {
              borderColor: 'rgba(59, 28, 85, 0.2)',
            },
            '&:hover fieldset': {
              borderColor: '#967CB2',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#633394',
              borderWidth: 2,
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          fontWeight: 500,
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          fontSize: '0.95rem',
          minHeight: 48,
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          backgroundColor: '#3B1C55',
          color: '#FBFAFA',
          fontWeight: 600,
        },
        root: {
          borderBottom: '1px solid rgba(150, 124, 178, 0.2)',
        },
      },
    },
  },
});

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [showJobTracking, setShowJobTracking] = useState(false);
  const [companyName, setCompanyName] = useState('');
  const [roleName, setRoleName] = useState('');

  const loadResults = async () => {
    try {
      const response = await fetch('/api/results');
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Error loading results:', error);
    }
  };

  const loadJobDescription = async () => {
    try {
      const response = await fetch('/api/job-description');
      const data = await response.json();
      setJobDescription(data.job_description || '');
      setCompanyName(data.company_name || '');
      setRoleName(data.role_name || '');
    } catch (error) {
      console.error('Error loading job description:', error);
    }
  };

  useEffect(() => {
    loadResults();
    loadJobDescription();
  }, []);

  const handleTabChange = (_event, newValue) => {
    setTabValue(newValue);
  };

  const handleCandidateSelect = (candidate) => {
    setSelectedCandidate(candidate);
    setTabValue(2);
  };

  const handleUploadSuccess = () => {
    loadResults();
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, backgroundColor: '#FBFAFA', minHeight: '100vh', p: 2 }}>
        <AppBar 
          position="static" 
          elevation={0}
          sx={{ 
            backgroundColor: '#3B1C55',
            borderRadius: '12px',
            border: '1px solid rgba(150, 124, 178, 0.3)',
            overflow: 'hidden',
          }}
        >
          <Toolbar>
            <WorkIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              ATS Resume Analysis System
            </Typography>
            <Button
              variant="contained"
              startIcon={<AssignmentIcon />}
              onClick={() => setShowJobTracking(true)}
              sx={{
                backgroundColor: '#967CB2',
                '&:hover': {
                  backgroundColor: '#633394',
                },
              }}
            >
              Job Tracker
            </Button>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 3, mb: 4 }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            sx={{ 
              mb: 3,
              '& .MuiTabs-indicator': {
                backgroundColor: '#633394',
                height: 3,
                borderRadius: '3px 3px 0 0',
              },
            }}
          >
            <Tab label="Job & Resume Library" />
            <Tab label="Analysis Results" />
            <Tab label="Candidate Detail" disabled={!selectedCandidate} />
          </Tabs>

          {tabValue === 0 && (
            <Box>
              <JobDescription 
                jobDescription={jobDescription}
                setJobDescription={setJobDescription}
              />
              <Box sx={{ mt: 3 }}>
                <ResumeLibrary
                  jobDescription={jobDescription}
                  onAnalysisComplete={handleUploadSuccess}
                  onViewResults={() => setTabValue(1)}
                />
              </Box>
            </Box>
          )}

          {tabValue === 1 && (
            <ResultsList 
              results={results}
              onCandidateSelect={handleCandidateSelect}
              onRefresh={loadResults}
              onBackToUpload={() => setTabValue(0)}
            />
          )}

          {tabValue === 2 && selectedCandidate && (
            <CandidateDetail 
              candidate={selectedCandidate}
              jobDescription={jobDescription}
              onBack={() => setTabValue(1)}
            />
          )}
        </Container>

        {showJobTracking && (
          <JobTracking
            companyName={companyName}
            roleName={roleName}
            onClose={() => setShowJobTracking(false)}
          />
        )}
      </Box>
    </ThemeProvider>
  );
}

export default App;
