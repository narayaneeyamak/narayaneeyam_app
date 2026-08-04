import React from 'react';
import { Play, Pause, ExternalLink, Volume2 } from 'lucide-react';

export default function SlokaView({
  dasakam,
  activeSloka,
  isPlaying,
  onPlaySloka,
  onPlayAll,
  fontSizeMultiplier
}) {
  if (!dasakam) return null;

  return (
    <div className="animate-fade-in" style={{ padding: '16px 16px 100px 16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Dasakam Title Header */}
      <div style={{
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-md)',
        padding: '16px',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--primary)', textTransform: 'uppercase' }}>
          Dasakam {dasakam.number}
        </span>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-main)', margin: '4px 0 2px 0' }}>
          {dasakam.title}
        </h2>
        {dasakam.titleTelugu && (
          <p style={{ fontSize: '1.05rem', color: 'var(--primary)', margin: '0 0 8px 0', fontFamily: 'var(--font-telugu)' }}>
            {dasakam.titleTelugu}
          </p>
        )}
        {dasakam.summary && (
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: 0 }}>
            {dasakam.summary}
          </p>
        )}

        {/* Play All Dasakam Button */}
        <button
          onClick={() => onPlayAll(dasakam.number)}
          style={{
            width: '100%',
            marginTop: '14px',
            backgroundColor: 'var(--primary)',
            color: '#ffffff',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            padding: '12px',
            fontSize: '0.95rem',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            cursor: 'pointer',
            boxShadow: 'var(--shadow-sm)'
          }}
        >
          <Play size={18} fill="#ffffff" />
          <span>Play All Dasakam {dasakam.number} Slokas</span>
        </button>
      </div>

      {/* Slokas List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {dasakam.slokas.map((sloka) => {
          const isCurrentActive = activeSloka?.dasakamNo === dasakam.number && activeSloka?.slokaNo === sloka.slokaNo;
          const isThisPlaying = isCurrentActive && isPlaying;

          return (
            <div
              key={sloka.slokaNo}
              id={`sloka-${sloka.slokaNo}`}
              style={{
                backgroundColor: 'var(--bg-card)',
                border: isCurrentActive ? '2px solid var(--primary)' : '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '18px 16px',
                boxShadow: isCurrentActive ? 'var(--shadow-md)' : 'var(--shadow-sm)',
                transition: 'all 0.2s ease',
                position: 'relative'
              }}
            >
              {/* Sloka Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    backgroundColor: isCurrentActive ? 'var(--primary)' : 'var(--bg-card-hover)',
                    color: isCurrentActive ? '#ffffff' : 'var(--text-main)',
                    fontWeight: 700,
                    fontSize: '0.85rem',
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-sm)'
                  }}>
                    Sloka {sloka.slokaNo}
                  </span>
                  {isCurrentActive && (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', color: 'var(--primary)', fontWeight: 600 }}>
                      <Volume2 size={14} className="animate-pulse" /> Playing
                    </span>
                  )}
                </div>

                {/* Play Buttons for individual sloka */}
                {sloka.audioUrl && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <button
                      onClick={() => onPlaySloka(dasakam.number, sloka.slokaNo)}
                      aria-label={`Play sloka ${sloka.slokaNo}`}
                      style={{
                        backgroundColor: isThisPlaying ? 'var(--primary-light)' : 'var(--bg-card-hover)',
                        color: isThisPlaying ? 'var(--primary)' : 'var(--text-main)',
                        border: 'none',
                        borderRadius: '50%',
                        width: '40px',
                        height: '40px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        transition: 'transform 0.15s'
                      }}
                    >
                      {isThisPlaying ? <Pause size={18} /> : <Play size={18} style={{ marginLeft: '2px' }} />}
                    </button>

                    {sloka.driveUrl && (
                      <a
                        href={sloka.driveUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="Open audio in Google Drive"
                        style={{
                          color: 'var(--text-light)',
                          padding: '6px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center'
                        }}
                      >
                        <ExternalLink size={16} />
                      </a>
                    )}
                  </div>
                )}
              </div>

              {/* Slokam Text in Telugu with exact pre-wrap spacing & indentation */}
              <div 
                className="telugu-text"
                style={{
                  fontSize: `calc(1.2rem * ${fontSizeMultiplier})`,
                  color: 'var(--text-main)',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  fontWeight: 500
                }}
              >
                {sloka.text}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
