import React, { useRef, useEffect, useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, Repeat, ExternalLink, X } from 'lucide-react';
import { getAudioStreamUrl } from '../utils/googleDrive';

export default function AudioPlayerBar({
  activeSloka,
  isPlaying,
  onTogglePlay,
  onNext,
  onPrev,
  onEnded,
  isAutoplay,
  onToggleAutoplay,
  onClose
}) {
  const audioRef = useRef(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [isLooping, setIsLooping] = useState(false);
  const [audioError, setAudioError] = useState(false);

  const streamUrl = activeSloka?.audioUrl ? getAudioStreamUrl(activeSloka.audioUrl) : '';

  useEffect(() => {
    setAudioError(false);
    setCurrentTime(0);
    setDuration(0);
  }, [activeSloka?.audioUrl, activeSloka?.slokaNo]);

  useEffect(() => {
    if (!audioRef.current || !streamUrl) return;
    if (isPlaying) {
      const playPromise = audioRef.current.play();
      if (playPromise !== undefined) {
        playPromise.catch(err => {
          console.error("Audio playback error:", err);
          setAudioError(true);
        });
      }
    } else {
      audioRef.current.pause();
    }
  }, [isPlaying, streamUrl]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.playbackRate = playbackSpeed;
    }
  }, [playbackSpeed]);

  if (!activeSloka) return null;

  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const handleSeek = (e) => {
    const newTime = parseFloat(e.target.value);
    if (audioRef.current) {
      audioRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  const cycleSpeed = () => {
    const speeds = [0.8, 1.0, 1.25];
    const nextIdx = (speeds.indexOf(playbackSpeed) + 1) % speeds.length;
    setPlaybackSpeed(speeds[nextIdx]);
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: '50%',
      transform: 'translateX(-50%)',
      width: '100%',
      maxWidth: '540px',
      background: 'linear-gradient(135deg, #3b090f 0%, #1f0407 100%)',
      borderTop: '2px solid #d4af37',
      padding: '10px 16px 14px 16px',
      boxShadow: '0 -6px 24px rgba(0, 0, 0, 0.4)',
      zIndex: 50,
      color: '#ffffff'
    }}>
      <audio
        ref={audioRef}
        src={streamUrl}
        loop={isLooping}
        onTimeUpdate={() => audioRef.current && setCurrentTime(audioRef.current.currentTime)}
        onLoadedMetadata={() => audioRef.current && setDuration(audioRef.current.duration)}
        onEnded={onEnded}
        onError={() => setAudioError(true)}
      />

      {/* Header Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#ffd700', letterSpacing: '0.02em' }}>
          దశకం {activeSloka.dasakamNo} • శ్లోకం {activeSloka.slokaNo}
        </span>
        <button
          onClick={onClose}
          aria-label="Close player"
          title="Close player"
          style={{
            background: 'rgba(212, 175, 55, 0.2)',
            border: '1px solid #d4af37',
            color: '#ffd700',
            cursor: 'pointer',
            padding: '3px 8px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            fontSize: '0.75rem',
            fontWeight: 600
          }}
        >
          <span>Close</span>
          <X size={14} />
        </button>
      </div>

      {/* Progress Bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
        <span style={{ fontSize: '0.75rem', color: '#fce8b3', width: '32px' }}>
          {formatTime(currentTime)}
        </span>
        <input
          type="range"
          min="0"
          max={duration || 100}
          value={currentTime}
          onChange={handleSeek}
          style={{
            flex: 1,
            height: '4px',
            accentColor: '#ffd700',
            cursor: 'pointer'
          }}
        />
        <span style={{ fontSize: '0.75rem', color: '#fce8b3', width: '32px', textAlign: 'right' }}>
          {formatTime(duration)}
        </span>
      </div>

      {/* Controls Row */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ flex: 1, minWidth: 0, marginRight: '12px' }}>
          <p style={{ fontSize: '0.75rem', color: '#fce8b3', margin: 0, opacity: 0.9 }}>
            {isPlaying ? 'AUDIO PLAYING' : 'AUDIO PAUSED'}
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <button
            onClick={cycleSpeed}
            title="Speed"
            style={{
              background: 'none',
              border: '1px solid #d4af37',
              color: '#ffd700',
              fontSize: '0.75rem',
              fontWeight: 700,
              padding: '2px 6px',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {playbackSpeed}x
          </button>

          <button
            onClick={onPrev}
            style={{ background: 'none', border: 'none', color: '#ffffff', cursor: 'pointer', padding: '4px' }}
          >
            <SkipBack size={20} />
          </button>

          <button
            onClick={onTogglePlay}
            style={{
              background: 'linear-gradient(135deg, #d4af37 0%, #aa820a 100%)',
              color: '#2b070c',
              border: 'none',
              borderRadius: '50%',
              width: '42px',
              height: '42px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.4)'
            }}
          >
            {isPlaying ? <Pause size={20} fill="#2b070c" /> : <Play size={20} fill="#2b070c" style={{ marginLeft: '2px' }} />}
          </button>

          <button
            onClick={onNext}
            style={{ background: 'none', border: 'none', color: '#ffffff', cursor: 'pointer', padding: '4px' }}
          >
            <SkipForward size={20} />
          </button>

          <button
            onClick={() => setIsLooping(!isLooping)}
            title="Loop Sloka"
            style={{
              background: 'none',
              border: 'none',
              color: isLooping ? '#ffd700' : 'rgba(255, 255, 255, 0.6)',
              cursor: 'pointer',
              padding: '4px'
            }}
          >
            <Repeat size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
