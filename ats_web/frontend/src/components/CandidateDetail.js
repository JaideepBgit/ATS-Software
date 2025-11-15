import React, { useState } from 'react';
import {
  Paper, Typography, Box, Grid, Chip, Divider, LinearProgress, Collapse, IconButton, Button, Dialog, DialogContent, DialogTitle
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon, Psychology as PsychologyIcon, Description as DescriptionIcon, Close as CloseIcon } from '@mui/icons-material';
import ChatInterface from './ChatInterface';
import InlineFeedback from './InlineFeedback';
import TTSButton from './TTSButton';
import PDFResumeViewer from './PDFResumeViewer';

function CandidateDetail({ candidate, jobDescription }) {
  const [thinkingExpanded, setThinkingExpanded] = useState(false);
  const [showResumeViewer, setShowResumeViewer] = useState(false);

  const ScoreBar = ({ label, value, color }) => (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="body2" fontWeight="bold">{value.toFixed(1)}%</Typography>
      </Box>
      <LinearProgress
        variant="determinate"
        value={value}
        sx={{
          height: 8,
          borderRadius: 1,
          backgroundColor: 'grey.200',
          '& .MuiLinearProgress-bar': { backgroundColor: color }
        }}
      />
    </Box>
  );

  const getScoreColor = (score) => {
    if (score >= 85) return '#4caf50';
    if (score >= 70) return '#2196f3';
    if (score >= 60) return '#ff9800';
    return '#f44336';
  };

  return (
    <Box>
      <Paper elevation={0} sx={{ p: 4, mb: 3, backgroundColor: '#FBFAFA' }}>
        <Typography variant="h4" gutterBottom sx={{ color: '#3B1C55', mb: 0.5 }}>
          {candidate.candidate_name}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {candidate.filename}
        </Typography>
        {(candidate.company_name || candidate.role_name) && (
          <Typography variant="h6" sx={{ color: '#967CB2', mt: 1, mb: 2 }}>
            {candidate.company_name && candidate.role_name 
              ? `${candidate.company_name} - ${candidate.role_name}`
              : candidate.company_name || candidate.role_name}
          </Typography>
        )}

        <Box sx={{ my: 3, display: 'flex', gap: 1.5, flexWrap: 'wrap', alignItems: 'center' }}>
          <Chip
            label={`Overall Score: ${candidate.overall_score}%`}
            sx={{
              backgroundColor: candidate.overall_score >= 70 ? '#4caf50' : candidate.overall_score >= 60 ? '#ff9800' : '#f44336',
              color: '#FBFAFA',
              fontWeight: 600,
              fontSize: '0.95rem',
              height: 36,
              px: 1,
            }}
          />
          <Chip
            label={candidate.hiring_recommendation}
            sx={{
              backgroundColor: '#967CB2',
              color: '#FBFAFA',
              fontWeight: 600,
              fontSize: '0.95rem',
              height: 36,
              px: 1,
            }}
          />
          <TTSButton 
            candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
            variant="button"
            size="medium"
          />
          <Button
            variant="contained"
            startIcon={<DescriptionIcon />}
            onClick={() => setShowResumeViewer(true)}
            sx={{
              backgroundColor: '#967CB2',
              color: '#FBFAFA',
              fontWeight: 600,
              height: 36,
              px: 2,
              '&:hover': {
                backgroundColor: '#7d5f9a',
              }
            }}
          >
            View Interactive Resume
          </Button>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* Thinking Process Section */}
        {candidate.thinking_process && candidate.thinking_process.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                cursor: 'pointer',
                p: 2,
                borderRadius: 2,
                backgroundColor: thinkingExpanded ? 'rgba(150, 124, 178, 0.08)' : 'rgba(150, 124, 178, 0.05)',
                border: '1px solid rgba(150, 124, 178, 0.2)',
                transition: 'all 0.3s',
                '&:hover': {
                  backgroundColor: 'rgba(150, 124, 178, 0.12)',
                  borderColor: 'rgba(150, 124, 178, 0.4)',
                }
              }}
              onClick={() => setThinkingExpanded(!thinkingExpanded)}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                <PsychologyIcon sx={{ color: '#967CB2', fontSize: 28 }} />
                <Box>
                  <Typography variant="h6" sx={{ color: '#3B1C55', mb: 0.5 }}>
                    AI Thinking Process
                  </Typography>
                  <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                    See how the AI reasoned through this evaluation
                  </Typography>
                </Box>
              </Box>
              <IconButton
                sx={{
                  transform: thinkingExpanded ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.3s',
                  color: '#967CB2'
                }}
              >
                <ExpandMoreIcon />
              </IconButton>
            </Box>

            <Collapse in={thinkingExpanded}>
              <Box sx={{ mt: 2, pl: 2 }}>
                {candidate.thinking_process.map((thought, index) => (
                  <Box
                    key={index}
                    sx={{
                      mb: 2.5,
                      pb: 2.5,
                      borderLeft: '3px solid rgba(150, 124, 178, 0.3)',
                      pl: 2.5,
                      borderBottom: index < candidate.thinking_process.length - 1 ? '1px solid rgba(0,0,0,0.06)' : 'none'
                    }}
                  >
                    <Typography
                      variant="subtitle2"
                      sx={{
                        color: '#967CB2',
                        fontWeight: 600,
                        mb: 1,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1
                      }}
                    >
                      <Box
                        component="span"
                        sx={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: 24,
                          height: 24,
                          borderRadius: '50%',
                          backgroundColor: 'rgba(150, 124, 178, 0.15)',
                          fontSize: '0.75rem',
                          fontWeight: 700
                        }}
                      >
                        {index + 1}
                      </Box>
                      {thought.step}
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: '#3B1C55',
                        lineHeight: 1.7,
                        fontStyle: 'italic',
                        pl: 4
                      }}
                    >
                      {thought.thinking}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </Collapse>
          </Box>
        )}

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>Score Breakdown</Typography>
            <ScoreBar
              label="Skills Match"
              value={candidate.skill_match_score}
              color={getScoreColor(candidate.skill_match_score)}
            />
            <ScoreBar
              label="Experience Match"
              value={candidate.experience_match_score}
              color={getScoreColor(candidate.experience_match_score)}
            />
            <ScoreBar
              label="Education Match"
              value={candidate.education_match_score}
              color={getScoreColor(candidate.education_match_score)}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Executive Summary
              <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                (click to provide feedback)
              </Typography>
            </Typography>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                '&:hover': {
                  backgroundColor: 'rgba(59, 28, 85, 0.03)',
                  cursor: 'pointer'
                }
              }}
            >
              <Typography variant="body2" paragraph sx={{ mb: 0, wordBreak: 'break-word' }}>
                <InlineFeedback
                  item={candidate.executive_summary}
                  itemType="executive_summary"
                  candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                />
              </Typography>
            </Box>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55', mb: 2 }}>
              Matched Skills
              <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                (click to provide feedback)
              </Typography>
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {candidate.matched_skills.slice(0, 15).map((skill, index) => (
                <Box
                  key={index}
                  sx={{
                    position: 'relative',
                    maxWidth: '100%',
                    '&:hover': {
                      '& .feedback-chip': {
                        boxShadow: '0 2px 8px rgba(76, 175, 80, 0.3)',
                      }
                    }
                  }}
                >
                  <Chip 
                    className="feedback-chip"
                    label={
                      <InlineFeedback
                        item={skill}
                        itemType="matched_skill"
                        candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                      />
                    }
                    size="small" 
                    sx={{ 
                      backgroundColor: 'rgba(76, 175, 80, 0.1)', 
                      color: '#2e7d32',
                      border: '1px solid rgba(76, 175, 80, 0.3)',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      maxWidth: '100%',
                      height: 'auto',
                      minHeight: '24px',
                      '& .MuiChip-label': {
                        width: '100%',
                        whiteSpace: 'normal',
                        wordBreak: 'break-word',
                        display: 'block',
                        padding: '4px 8px',
                        lineHeight: 1.4
                      }
                    }} 
                  />
                </Box>
              ))}
              {candidate.matched_skills.length > 15 && (
                <Chip 
                  label={`+${candidate.matched_skills.length - 15} more`} 
                  size="small"
                  sx={{ 
                    backgroundColor: 'rgba(150, 124, 178, 0.1)', 
                    color: '#633394',
                    border: '1px solid rgba(150, 124, 178, 0.3)',
                  }}
                />
              )}
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55', mb: 2 }}>
              Missing Skills
              <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                (click to provide feedback)
              </Typography>
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {candidate.missing_critical_skills.slice(0, 10).map((skill, index) => (
                <Box
                  key={index}
                  sx={{
                    position: 'relative',
                    maxWidth: '100%',
                    '&:hover': {
                      '& .feedback-chip': {
                        boxShadow: '0 2px 8px rgba(244, 67, 54, 0.3)',
                      }
                    }
                  }}
                >
                  <Chip 
                    className="feedback-chip"
                    label={
                      <InlineFeedback
                        item={skill}
                        itemType="missing_skill"
                        candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                      />
                    }
                    size="small" 
                    sx={{ 
                      backgroundColor: 'rgba(244, 67, 54, 0.1)', 
                      color: '#c62828',
                      border: '1px solid rgba(244, 67, 54, 0.3)',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      maxWidth: '100%',
                      height: 'auto',
                      minHeight: '24px',
                      '& .MuiChip-label': {
                        width: '100%',
                        whiteSpace: 'normal',
                        wordBreak: 'break-word',
                        display: 'block',
                        padding: '4px 8px',
                        lineHeight: 1.4
                      }
                    }} 
                  />
                </Box>
              ))}
            </Box>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55', mb: 2 }}>
              Strengths
              <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                (click to provide feedback)
              </Typography>
            </Typography>
            <Box component="ul" sx={{ pl: 2.5, color: '#3B1C55' }}>
              {candidate.strengths.map((strength, index) => (
                <Box
                  component="li"
                  key={index}
                  sx={{
                    mb: 1,
                    '&:hover': {
                      backgroundColor: 'rgba(59, 28, 85, 0.05)',
                      borderRadius: 1,
                      ml: -1,
                      pl: 1,
                      py: 0.5
                    }
                  }}
                >
                  <Typography variant="body2" sx={{ lineHeight: 1.6, wordBreak: 'break-word' }}>
                    <InlineFeedback
                      item={strength}
                      itemType="strength"
                      candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                    />
                  </Typography>
                </Box>
              ))}
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom sx={{ color: '#3B1C55', mb: 2 }}>
              Weaknesses
              <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                (click to provide feedback)
              </Typography>
            </Typography>
            <Box component="ul" sx={{ pl: 2.5, color: '#61382E' }}>
              {candidate.weaknesses.map((weakness, index) => (
                <Box
                  component="li"
                  key={index}
                  sx={{
                    mb: 1,
                    '&:hover': {
                      backgroundColor: 'rgba(97, 56, 46, 0.05)',
                      borderRadius: 1,
                      ml: -1,
                      pl: 1,
                      py: 0.5
                    }
                  }}
                >
                  <Typography variant="body2" sx={{ lineHeight: 1.6, wordBreak: 'break-word' }}>
                    <InlineFeedback
                      item={weakness}
                      itemType="weakness"
                      candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
                    />
                  </Typography>
                </Box>
              ))}
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <ChatInterface candidate={candidate} jobDescription={jobDescription} />

      {/* Resume Viewer Dialog */}
      <Dialog 
        open={showResumeViewer} 
        onClose={() => setShowResumeViewer(false)}
        maxWidth="xl"
        fullWidth
        PaperProps={{
          sx: {
            height: '90vh',
            maxHeight: '90vh'
          }
        }}
      >
        <DialogTitle sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          backgroundColor: '#3B1C55',
          color: '#FBFAFA'
        }}>
          <Typography variant="h6">Interactive Resume Viewer</Typography>
          <IconButton 
            onClick={() => setShowResumeViewer(false)}
            sx={{ color: '#FBFAFA' }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent sx={{ p: 0, overflow: 'hidden' }}>
          <PDFResumeViewer 
            candidateId={`${candidate.candidate_name}_${candidate.timestamp}`}
            candidateName={candidate.candidate_name}
          />
        </DialogContent>
      </Dialog>
    </Box>
  );
}

export default CandidateDetail;
