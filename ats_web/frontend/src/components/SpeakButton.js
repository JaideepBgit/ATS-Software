import React, { useState } from 'react';
import { IconButton, Button, CircularProgress, Tooltip } from '@mui/material';
import { VolumeUp, VolumeOff } from '@mui/icons-material';

const SpeakButton = ({ text, size = 'md', variant = 'icon' }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [audio, setAudio] = useState(null);

  const handleSpeak = async () => {
    if (isPlaying && audio) {
      // Stop current audio
      audio.pause();
      audio.currentTime = 0;
      setIsPlaying(false);
      return;
    }

    if (!text || !text.trim()) {
      console.error('No text to speak');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/tts/speak', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate speech');
      }

      const data = await response.json();
      
      // Create audio element
      const audioUrl = `http://localhost:8000${data.url}?t=${Date.now()}`;
      const newAudio = new Audio(audioUrl);
      
      newAudio.onplay = () => setIsPlaying(true);
      newAudio.onended = () => setIsPlaying(false);
      newAudio.onerror = () => {
        setIsPlaying(false);
        console.error('Audio playback error');
      };

      setAudio(newAudio);
      await newAudio.play();
      
    } catch (error) {
      console.error('TTS Error:', error);
      alert('Failed to generate speech. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const iconSizes = {
    sm: 'small',
    md: 'medium',
    lg: 'large'
  };

  if (variant === 'icon') {
    return (
      <Tooltip title={isPlaying ? 'Stop' : 'Speak'}>
        <IconButton
          onClick={handleSpeak}
          disabled={isLoading}
          size={iconSizes[size]}
          sx={{
            backgroundColor: isPlaying ? '#f44336' : '#2196f3',
            color: 'white',
            '&:hover': {
              backgroundColor: isPlaying ? '#d32f2f' : '#1976d2',
            },
            '&:disabled': {
              backgroundColor: '#bdbdbd',
            }
          }}
        >
          {isLoading ? (
            <CircularProgress size={20} sx={{ color: 'white' }} />
          ) : isPlaying ? (
            <VolumeOff />
          ) : (
            <VolumeUp />
          )}
        </IconButton>
      </Tooltip>
    );
  }

  return (
    <Button
      onClick={handleSpeak}
      disabled={isLoading}
      variant="contained"
      startIcon={isLoading ? <CircularProgress size={18} sx={{ color: 'white' }} /> : isPlaying ? <VolumeOff /> : <VolumeUp />}
      sx={{
        backgroundColor: isPlaying ? '#f44336' : '#2196f3',
        '&:hover': {
          backgroundColor: isPlaying ? '#d32f2f' : '#1976d2',
        }
      }}
    >
      {isLoading ? 'Loading...' : isPlaying ? 'Stop' : 'Speak'}
    </Button>
  );
};

export default SpeakButton;
