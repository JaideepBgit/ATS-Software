import React from 'react';
import {
  Paper, Typography, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Chip, Button, Box, IconButton, Grid, Card, CardContent
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import VisibilityIcon from '@mui/icons-material/Visibility';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PeopleIcon from '@mui/icons-material/People';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

function ResultsList({ results, onCandidateSelect, onRefresh, onBackToUpload }) {
  const getScoreColor = (score) => {
    if (score >= 85) return 'success';
    if (score >= 70) return 'primary';
    if (score >= 60) return 'warning';
    return 'error';
  };

  const getRecommendationChip = (recommendation) => {
    if (recommendation.startsWith('YES') || recommendation.includes('STRONG')) {
      return <Chip label="Hire" color="success" size="small" />;
    }
    if (recommendation.startsWith('NO')) {
      return <Chip label="Reject" color="error" size="small" />;
    }
    return <Chip label="Maybe" color="warning" size="small" />;
  };

  // Calculate statistics
  const totalCandidates = results.length;
  const hireCount = results.filter(r => 
    r.hiring_recommendation.startsWith('YES') || r.hiring_recommendation.includes('STRONG')
  ).length;
  const rejectCount = results.filter(r => 
    r.hiring_recommendation.startsWith('NO')
  ).length;
  const maybeCount = results.filter(r => 
    !r.hiring_recommendation.startsWith('YES') && 
    !r.hiring_recommendation.includes('STRONG') && 
    !r.hiring_recommendation.startsWith('NO')
  ).length;
  const avgScore = results.length > 0 
    ? (results.reduce((sum, r) => sum + r.overall_score, 0) / results.length).toFixed(1)
    : 0;

  return (
    <Box>
      {/* Sticky Statistics Boards */}
      <Box 
        sx={{ 
          position: 'sticky',
          top: 0,
          zIndex: 10,
          backgroundColor: '#FBFAFA',
          pb: 2,
          pt: 1,
        }}
      >
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card 
              elevation={0}
              sx={{ 
                backgroundColor: '#633394',
                color: 'white',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {totalCandidates}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Total Candidates
                    </Typography>
                  </Box>
                  <PeopleIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card 
              elevation={0}
              sx={{ 
                backgroundColor: '#4caf50',
                color: 'white',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {hireCount}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Recommended
                    </Typography>
                  </Box>
                  <ThumbUpIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card 
              elevation={0}
              sx={{ 
                backgroundColor: '#ff9800',
                color: 'white',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {maybeCount}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Maybe
                    </Typography>
                  </Box>
                  <HelpOutlineIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card 
              elevation={0}
              sx={{ 
                backgroundColor: '#f44336',
                color: 'white',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" fontWeight="bold">
                      {rejectCount}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Not Recommended
                    </Typography>
                  </Box>
                  <ThumbDownIcon sx={{ fontSize: 48, opacity: 0.3 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Results Table */}
      <Paper elevation={0} sx={{ p: 4, backgroundColor: '#FBFAFA' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <IconButton onClick={onBackToUpload} sx={{ color: '#633394' }}>
              <ArrowBackIcon />
            </IconButton>
            <Box>
              <Typography variant="h5" sx={{ color: '#3B1C55', mb: 0.5 }}>
                Analysis Results
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Average Score: {avgScore}%
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <IconButton onClick={onRefresh} sx={{ color: '#633394' }} title="Refresh Results">
              <RefreshIcon />
            </IconButton>
          </Box>
        </Box>

      {results.length === 0 ? (
        <Box sx={{ 
          textAlign: 'center', 
          py: 8,
          backgroundColor: 'rgba(99, 51, 148, 0.03)',
          borderRadius: 2,
          border: '1px dashed rgba(99, 51, 148, 0.3)',
        }}>
          <Typography variant="body1" color="text.secondary">
            No candidates analyzed yet. Upload resumes to get started.
          </Typography>
        </Box>
      ) : (
        <TableContainer sx={{ borderRadius: 2, overflow: 'hidden' }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Candidate</TableCell>
                <TableCell>Company - Role</TableCell>
                <TableCell>Overall Score</TableCell>
                <TableCell>Skills</TableCell>
                <TableCell>Experience</TableCell>
                <TableCell>Education</TableCell>
                <TableCell>Recommendation</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {results.map((result, index) => (
                <TableRow key={index} hover>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {result.candidate_name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {result.filename}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="medium">
                      {result.company_name && result.role_name 
                        ? `${result.company_name} - ${result.role_name}`
                        : result.company_name || result.role_name || '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={`${result.overall_score}%`}
                      color={getScoreColor(result.overall_score)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{result.skill_match_score.toFixed(1)}%</TableCell>
                  <TableCell>{result.experience_match_score.toFixed(1)}%</TableCell>
                  <TableCell>{result.education_match_score.toFixed(1)}%</TableCell>
                  <TableCell>{getRecommendationChip(result.hiring_recommendation)}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      startIcon={<VisibilityIcon />}
                      onClick={() => onCandidateSelect(result)}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      </Paper>
    </Box>
  );
}

export default ResultsList;
