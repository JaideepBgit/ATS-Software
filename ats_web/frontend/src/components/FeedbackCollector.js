import { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions,
  Button, TextField, Box, Typography, Rating, Chip,
  IconButton, Tooltip, Divider, Alert
} from '@mui/material';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import FeedbackIcon from '@mui/icons-material/Feedback';
import CloseIcon from '@mui/icons-material/Close';
import axios from 'axios';

function FeedbackCollector({ message, messageIndex, candidateId }) {
  const [open, setOpen] = useState(false);
  const [rating, setRating] = useState(3);
  const [correctPoints, setCorrectPoints] = useState('');
  const [incorrectPoints, setIncorrectPoints] = useState('');
  const [missingPoints, setMissingPoints] = useState('');
  const [idealResponse, setIdealResponse] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    if (!submitting) {
      setOpen(false);
      setTimeout(() => setSubmitted(false), 300);
    }
  };

  const handleQuickFeedback = async (isPositive) => {
    setSubmitting(true);
    try {
      await axios.post('/api/feedback/submit', {
        interaction_id: `${candidateId}_msg_${messageIndex}`,
        query: message.query || '',
        context: message.context || [],
        response: message.content,
        rating: isPositive ? 5 : 2,
        correct_points: isPositive ? ['Response was helpful'] : [],
        incorrect_points: isPositive ? [] : ['Response needs improvement'],
        missing_points: [],
        ideal_response: message.content
      });
      setSubmitted(true);
      setTimeout(() => setSubmitted(false), 2000);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDetailedSubmit = async () => {
    setSubmitting(true);
    try {
      await axios.post('/api/feedback/submit', {
        interaction_id: `${candidateId}_msg_${messageIndex}`,
        query: message.query || '',
        context: message.context || [],
        response: message.content,
        rating: rating,
        correct_points: correctPoints.split(',').map(p => p.trim()).filter(p => p),
        incorrect_points: incorrectPoints.split(',').map(p => p.trim()).filter(p => p),
        missing_points: missingPoints.split(',').map(p => p.trim()).filter(p => p),
        ideal_response: idealResponse || message.content
      });
      setSubmitted(true);
      setTimeout(() => {
        handleClose();
        // Reset form
        setRating(3);
        setCorrectPoints('');
        setIncorrectPoints('');
        setMissingPoints('');
        setIdealResponse('');
      }, 1500);
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <Box sx={{ display: 'flex', gap: 0.5, mt: 1 }}>
        <Tooltip title="This response was helpful">
          <IconButton
            size="small"
            onClick={() => handleQuickFeedback(true)}
            disabled={submitting || submitted}
            sx={{
              color: submitted ? '#4caf50' : 'rgba(59, 28, 85, 0.6)',
              '&:hover': { color: '#4caf50' }
            }}
          >
            <ThumbUpIcon fontSize="small" />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="This response needs improvement">
          <IconButton
            size="small"
            onClick={() => handleQuickFeedback(false)}
            disabled={submitting || submitted}
            sx={{
              color: submitted ? '#f44336' : 'rgba(59, 28, 85, 0.6)',
              '&:hover': { color: '#f44336' }
            }}
          >
            <ThumbDownIcon fontSize="small" />
          </IconButton>
        </Tooltip>
        
        <Tooltip title="Provide detailed feedback">
          <IconButton
            size="small"
            onClick={handleOpen}
            disabled={submitting}
            sx={{
              color: 'rgba(59, 28, 85, 0.6)',
              '&:hover': { color: '#633394' }
            }}
          >
            <FeedbackIcon fontSize="small" />
          </IconButton>
        </Tooltip>

        {submitted && (
          <Chip
            label="Feedback saved!"
            size="small"
            color="success"
            sx={{ ml: 1, height: 24 }}
          />
        )}
      </Box>

      <Dialog
        open={open}
        onClose={handleClose}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            backgroundColor: '#FBFAFA'
          }
        }}
      >
        <DialogTitle sx={{ color: '#3B1C55', pb: 1 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">Provide Detailed Feedback</Typography>
            <IconButton onClick={handleClose} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>

        <DialogContent>
          {submitted ? (
            <Alert severity="success" sx={{ mb: 2 }}>
              Thank you! Your feedback has been saved and will help improve the model.
            </Alert>
          ) : (
            <>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Your feedback helps train the AI model to provide better responses.
              </Typography>

              <Box sx={{ mb: 3, p: 2, backgroundColor: 'rgba(59, 28, 85, 0.05)', borderRadius: 1 }}>
                <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                  AI Response:
                </Typography>
                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', maxHeight: 150, overflow: 'auto' }}>
                  {message.content}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  Overall Rating
                </Typography>
                <Rating
                  value={rating}
                  onChange={(event, newValue) => setRating(newValue)}
                  size="large"
                />
              </Box>

              <TextField
                fullWidth
                label="What was correct? (comma-separated)"
                placeholder="e.g., Identified key skills, Accurate experience assessment"
                value={correctPoints}
                onChange={(e) => setCorrectPoints(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 2 }}
                helperText="List the points that were accurate and helpful"
              />

              <TextField
                fullWidth
                label="What was incorrect? (comma-separated)"
                placeholder="e.g., Missed Python experience, Wrong education level"
                value={incorrectPoints}
                onChange={(e) => setIncorrectPoints(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 2 }}
                helperText="List the points that were inaccurate or misleading"
              />

              <TextField
                fullWidth
                label="What was missing? (comma-separated)"
                placeholder="e.g., Should mention leadership skills, Didn't address cultural fit"
                value={missingPoints}
                onChange={(e) => setMissingPoints(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 2 }}
                helperText="What important information was not included?"
              />

              <TextField
                fullWidth
                label="Ideal Response (optional)"
                placeholder="Write what the ideal response should have been..."
                value={idealResponse}
                onChange={(e) => setIdealResponse(e.target.value)}
                multiline
                rows={4}
                sx={{ mb: 2 }}
                helperText="Provide a corrected or improved version of the response"
              />
            </>
          )}
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={handleClose} disabled={submitting}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleDetailedSubmit}
            disabled={submitting || submitted}
            sx={{
              backgroundColor: '#633394',
              '&:hover': { backgroundColor: '#3B1C55' }
            }}
          >
            {submitting ? 'Submitting...' : 'Submit Feedback'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default FeedbackCollector;
