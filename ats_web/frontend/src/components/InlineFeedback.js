import { useState } from 'react';
import {
  Box, TextField, Button, Chip, IconButton, Tooltip, Collapse, Alert
} from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';
import CloseIcon from '@mui/icons-material/Close';
import EditIcon from '@mui/icons-material/Edit';
import axios from 'axios';

function InlineFeedback({ 
  item, 
  itemType, 
  candidateId, 
  onFeedbackSubmitted 
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [isCorrect, setIsCorrect] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async () => {
    if (!feedback.trim() && isCorrect === null) return;

    setSubmitting(true);
    try {
      await axios.post('/api/feedback/submit', {
        interaction_id: `${candidateId}_${itemType}_${Date.now()}`,
        query: `Is this ${itemType} accurate: "${item}"?`,
        context: [itemType, item],
        response: item,
        rating: isCorrect ? 5 : 2,
        correct_points: isCorrect ? [item] : [],
        incorrect_points: isCorrect ? [] : [item],
        missing_points: [],
        ideal_response: feedback.trim() || item
      });
      
      setSubmitted(true);
      setTimeout(() => {
        setIsEditing(false);
        setSubmitted(false);
        setFeedback('');
        setIsCorrect(null);
        if (onFeedbackSubmitted) onFeedbackSubmitted();
      }, 1500);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFeedback('');
    setIsCorrect(null);
    setSubmitted(false);
  };

  return (
    <Box sx={{ display: 'inline', width: '100%', position: 'relative' }}>
      <span style={{ wordBreak: 'break-word' }}>
        {item}
        {!isEditing && !submitted && (
          <Tooltip title="Provide feedback on this point">
            <IconButton
              size="small"
              onClick={() => setIsEditing(true)}
              sx={{
                opacity: 0,
                transition: 'opacity 0.2s',
                '.MuiBox-root:hover &': { opacity: 1 },
                color: 'rgba(59, 28, 85, 0.6)',
                '&:hover': { color: '#633394' },
                verticalAlign: 'middle',
                display: 'inline-flex',
                padding: '2px',
                marginLeft: '4px'
              }}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        )}
        {submitted && (
          <Chip
            label="✓ Saved"
            size="small"
            color="success"
            sx={{ 
              height: 20, 
              fontSize: '0.7rem',
              verticalAlign: 'middle',
              marginLeft: '4px'
            }}
          />
        )}
      </span>

      <Collapse in={isEditing}>
        <Box
          sx={{
            mt: 1,
            p: 2,
            backgroundColor: '#FFFFFF',
            borderRadius: 1,
            border: '2px solid rgba(99, 51, 148, 0.3)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
            position: 'relative',
            zIndex: 1000
          }}
        >
          <Box sx={{ mb: 2 }}>
            <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
              <Button
                size="small"
                variant={isCorrect === true ? 'contained' : 'outlined'}
                onClick={() => setIsCorrect(true)}
                sx={{
                  backgroundColor: isCorrect === true ? '#4caf50' : 'transparent',
                  borderColor: '#4caf50',
                  color: isCorrect === true ? 'white' : '#4caf50',
                  '&:hover': {
                    backgroundColor: isCorrect === true ? '#45a049' : 'rgba(76, 175, 80, 0.1)'
                  }
                }}
              >
                ✓ Correct
              </Button>
              <Button
                size="small"
                variant={isCorrect === false ? 'contained' : 'outlined'}
                onClick={() => setIsCorrect(false)}
                sx={{
                  backgroundColor: isCorrect === false ? '#f44336' : 'transparent',
                  borderColor: '#f44336',
                  color: isCorrect === false ? 'white' : '#f44336',
                  '&:hover': {
                    backgroundColor: isCorrect === false ? '#da190b' : 'rgba(244, 67, 54, 0.1)'
                  }
                }}
              >
                ✗ Incorrect
              </Button>
            </Box>
          </Box>

          <TextField
            fullWidth
            size="small"
            multiline
            rows={2}
            placeholder={
              isCorrect === false
                ? "What should it say instead?"
                : "Add any additional notes (optional)"
            }
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            sx={{ mb: 1 }}
          />

          <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
            <Button
              size="small"
              onClick={handleCancel}
              disabled={submitting}
            >
              Cancel
            </Button>
            <Button
              size="small"
              variant="contained"
              onClick={handleSubmit}
              disabled={submitting || (isCorrect === null && !feedback.trim())}
              startIcon={submitting ? null : <CheckIcon />}
              sx={{
                backgroundColor: '#633394',
                '&:hover': { backgroundColor: '#3B1C55' }
              }}
            >
              {submitting ? 'Saving...' : 'Save Feedback'}
            </Button>
          </Box>
        </Box>
      </Collapse>
    </Box>
  );
}

export default InlineFeedback;
