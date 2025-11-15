import React, { useState } from 'react';
import { Button, IconButton, CircularProgress, Tooltip } from '@mui/material';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import StopIcon from '@mui/icons-material/Stop';

function TTSButton({ text, candidateId, variant = 'button', size = 'medium' }) {
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [audio, setAudio] = useState(null);

  const handlePlay = async () => {
    try {
      setLoading(true);

      let audioUrl;

      if (candidateId) {
        // Generate candidate summary TTS
        const response = await fetch(`/api/tts/summary/${candidateId}`, {
          method: 'POST'
        });
        
        if (!response.ok) {
          throw new Error('TTS generation failed');
        }
        
        const data = await response.json();
        audioUrl = data.url;
      } else if (text) {
        // Generate TTS from text
        const response = await fetch(`/api/tts/generate?text=${encodeURIComponent(text)}`, {
          method: 'POST'
        });
        
        if (!response.ok) {
          throw new Error('TTS generation failed');
        }
        
        const data = await response.json();
        audioUrl = data.url;
      } else {
        throw new Error('No text or candidate ID provided');
      }

      // Create and play audio
      const audioElement = new Audio(audioUrl);
      
      audioElement.onended = () => {
        setPlaying(false);
        setAudio(null);
      };
      
      audioElement.onerror = () => {
        setPlaying(false);
        setAudio(null);
        alert('Error playing audio');
      };

      await audioElement.play();
      setAudio(audioElement);
      setPlaying(true);

    } catch (error) {
      console.error('TTS error:', error);
      alert('Text-to-speech is not available. Please check the setup guide.');
    } finally {
      setLoading(false);
    }
  };

  const handleStop = () => {
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
      setPlaying(false);
      setAudio(null);
    }
  };

  if (variant === 'icon') {
    return (
      <Tooltip title={playing ? "Stop Audio" : "Listen"}>
        <IconButton
          onClick={playing ? handleStop : handlePlay}
          disabled={loading}
          size={size}
          sx={{ color: playing ? '#f44336' : '#633394' }}
        >
          {loading ? (
            <CircularProgress size={20} />
          ) : playing ? (
            <StopIcon />
          ) : (
            <VolumeUpIcon />
          )}
        </IconButton>
      </Tooltip>
    );
  }

  return (
    <Button
      variant="outlined"
      startIcon={loading ? <CircularProgress size={20} /> : playing ? <StopIcon /> : <VolumeUpIcon />}
      onClick={playing ? handleStop : handlePlay}
      disabled={loading}
      size={size}
      sx={{
        borderColor: playing ? '#f44336' : '#967CB2',
        color: playing ? '#f44336' : '#633394',
        '&:hover': {
          borderColor: playing ? '#d32f2f' : '#633394',
          backgroundColor: playing ? 'rgba(244, 67, 54, 0.04)' : 'rgba(99, 51, 148, 0.04)',
        },
      }}
    >
      {playing ? 'Stop' : 'Listen'}
    </Button>
  );
}

export default TTSButton;
