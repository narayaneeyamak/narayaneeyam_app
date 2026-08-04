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

  // Reset audio error when active sloka changes
  useEffect(() => {
    setAudioError(false);
    setCurrentTime(0);
    setDuration(0);
  }, [activeSloka?.audioUrl, activeSloka?.slokaNo]);

  // Handle Play / Pause changes
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

  // Handle Speed Change
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
      backgroundColor: 'var(--bg-card)',
      borderTop: '1px solid var(--border)',
      padding: '10px 16px 14px 16px',
      boxShadow: '0 -4px 20px rgba(0, 0, 0, 0.15)',
      zIndex: 50
    }}>
      {/* Hidden HTML Audio element */}
      <audio
        ref={audioRef}
        src={streamUrl}
        loop={isLooping}
        onTimeUpdate={() => audioRef.current && setCurrentTime(audioRef.current.currentTime)}
        onLoadedMetadata={() => audioRef.current && setDuration(audioRef.current.duration)}
        onEnded={onEnded}
        onError={() => setAudioError(true)}
      />

      {/* Header Row: Close ('X') button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary)' }}>
          Dasakam {activeSloka.dasakamNo} • Sloka {activeSloka.slokaNo}
        </span>
        <button
          onClick={onClose}
          aria-label="Close player"
          title="Close player"
          style={{
            background: 'var(--bg-card-hover)',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '4px 8px',
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
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', width: '32px' }}>
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
            accentColor: 'var(--primary)',
            cursor: 'pointer'
          }}
        />
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', width: '32px', textAlign: 'right' }}>
          {formatTime(duration)}
        </span>
      </div>

      {/* Main Controls Row */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        {/* Track Status */}
        <div style={{ flex: 1, minWidth: 0, marginRight: '12px' }}>
          {audioError ? (
            <a
              href={activeSloka.audioUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{ fontSize: '0.75rem', color: '#ef4444', textDecoration: 'underline', display: 'flex', alignItems: 'center', gap: '2px' }}
            >
              Permission needed <ExternalLink size={12} />
            </a>
          ) : (
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>
              {isPlaying ? 'Playing continuous audio' : 'Paused'}
            </p>
          )}
        </div>

        {/* Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {/* Speed Toggle */}
          <button
            onClick={cycleSpeed}
            title="Speed"
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              fontSize: '0.75rem',
              fontWeight: 700,
              padding: '4px 6px',
              borderRadius: 'var(--radius-sm)',
              cursor: 'pointer'
            }}
          >
            {playbackSpeed}x
          </button>

          {/* Prev Button */}
          <button
            onClick={onPrev}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-main)',
              cursor: 'pointer',
              padding: '6px'
            }}
          >
            <SkipBack size={20} />
          </button>

          {/* Main Play/Pause Button */}
          <button
            onClick={onTogglePlay}
            style={{
              backgroundColor: 'var(--primary)',
              color: '#ffffff',
              border: 'none',
              borderRadius: '50%',
              width: '44px',
              height: '44px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: 'var(--shadow-md)'
            }}
          >
            {isPlaying ? <Pause size={22} /> : <Play size={22} style={{ marginLeft: '2px' }} />}
          </button>

          {/* Next Button */}
          <button
            onClick={onNext}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-main)',
              cursor: 'pointer',
              padding: '6px'
            }}
          >
            <SkipForward size={20} />
          </button>

          {/* Loop Mode Toggle */}
          <button
            onClick={() => setIsLooping(!isLooping)}
            title="Loop Sloka"
            style={{
              background: 'none',
              border: 'none',
              color: isLooping ? 'var(--primary)' : 'var(--text-muted)',
              cursor: 'pointer',
              padding: '6px'
            }}
          >
            <Repeat size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
