import React, { useState } from 'react';
import { Volume2, VolumeX, Loader } from 'lucide-react';

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

  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-10 h-10'
  };

  const iconSizes = {
    sm: 14,
    md: 18,
    lg: 22
  };

  if (variant === 'icon') {
    return (
      <button
        onClick={handleSpeak}
        disabled={isLoading}
        className={`${sizeClasses[size]} flex items-center justify-center rounded-full 
          ${isPlaying ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'} 
          text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
        title={isPlaying ? 'Stop' : 'Speak'}
      >
        {isLoading ? (
          <Loader size={iconSizes[size]} className="animate-spin" />
        ) : isPlaying ? (
          <VolumeX size={iconSizes[size]} />
        ) : (
          <Volume2 size={iconSizes[size]} />
        )}
      </button>
    );
  }

  return (
    <button
      onClick={handleSpeak}
      disabled={isLoading}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg 
        ${isPlaying ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'} 
        text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
    >
      {isLoading ? (
        <>
          <Loader size={18} className="animate-spin" />
          <span>Loading...</span>
        </>
      ) : isPlaying ? (
        <>
          <VolumeX size={18} />
          <span>Stop</span>
        </>
      ) : (
        <>
          <Volume2 size={18} />
          <span>Speak</span>
        </>
      )}
    </button>
  );
};

export default SpeakButton;
