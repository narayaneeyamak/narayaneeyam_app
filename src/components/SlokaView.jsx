import React from 'react';
import { Play, Pause, ExternalLink, Volume2, Music } from 'lucide-react';

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
    <div 
      className="animate-fade-in" 
      style={{ 
        padding: '16px 16px 140px 16px', 
        display: 'flex', 
        flexDirection: 'column', 
        gap: '18px',
        backgroundColor: '#faf5eb',
        minHeight: 'calc(100vh - 60px)',
        backgroundImage: 'radial-gradient(#e5d9c5 1px, transparent 1px)',
        backgroundSize: '20px 20px'
      }}
    >
      
      {/* Traditional Maroon & Gold Header Banner */}
      <div style={{
        background: 'linear-gradient(135deg, #4a0e17 0%, #2b070c 100%)',
        border: '2px solid #d4af37',
        borderRadius: '12px',
        padding: '18px 16px',
        boxShadow: '0 8px 24px rgba(74, 14, 23, 0.25)',
        textAlign: 'center',
        color: '#ffffff',
        position: 'relative'
      }}>
        {/* Golden Ornaments */}
        <div style={{ fontSize: '0.85rem', color: '#f3e5ab', letterSpacing: '0.1em', fontWeight: 600, marginBottom: '2px' }}>
          ❖ ౧౦౹ ❖
        </div>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, margin: '0 0 2px 0', fontFamily: 'var(--font-telugu)', color: '#ffd700', textShadow: '0 2px 4px rgba(0,0,0,0.5)' }}>
          శ్రీమన్నారాయణీయం
        </h2>
        <p style={{ fontSize: '0.82rem', color: '#fce8b3', margin: '0 0 10px 0', fontFamily: 'var(--font-telugu)', opacity: 0.95 }}>
          - మేల్పుత్తూర్ నారాయణ భట్టాత్రి -
        </p>

        <div style={{
          display: 'inline-block',
          backgroundColor: '#38090f',
          border: '1px solid #d4af37',
          padding: '4px 14px',
          borderRadius: '20px',
          fontSize: '0.9rem',
          fontWeight: 700,
          color: '#ffffff'
        }}>
          దశకము {dasakam.number} : {dasakam.titleTelugu || dasakam.title}
        </div>

        {/* Play All Button inside Header */}
        <button
          onClick={() => onPlayAll(dasakam.number)}
          style={{
            width: '100%',
            marginTop: '14px',
            background: 'linear-gradient(135deg, #d4af37 0%, #aa820a 100%)',
            color: '#2b070c',
            border: 'none',
            borderRadius: '8px',
            padding: '12px',
            fontSize: '0.95rem',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(212, 175, 55, 0.4)'
          }}
        >
          <Play size={18} fill="#2b070c" />
          <span>Play All Slokas (దశకం {dasakam.number})</span>
        </button>
      </div>

      {/* Slokas List with Traditional Gold Frames */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
        {dasakam.slokas.map((sloka) => {
          const isCurrentActive = activeSloka?.dasakamNo === dasakam.number && activeSloka?.slokaNo === sloka.slokaNo;
          const isThisPlaying = isCurrentActive && isPlaying;

          return (
            <div
              key={sloka.slokaNo}
              id={`sloka-${sloka.slokaNo}`}
              style={{
                backgroundColor: '#fffdfa',
                border: isCurrentActive ? '2px solid #b8860b' : '2px solid #d4af37',
                borderRadius: '12px',
                padding: '20px 18px',
                boxShadow: isCurrentActive ? '0 8px 24px rgba(184, 134, 11, 0.3)' : '0 4px 16px rgba(212, 175, 55, 0.15)',
                position: 'relative',
                transition: 'all 0.2s ease'
              }}
            >
              {/* Corner Golden Ornaments */}
              <div style={{ position: 'absolute', top: '4px', left: '8px', color: '#d4af37', fontSize: '0.75rem', opacity: 0.8 }}>
                ✦
              </div>
              <div style={{ position: 'absolute', top: '4px', right: '8px', color: '#d4af37', fontSize: '0.75rem', opacity: 0.8 }}>
                ✦
              </div>
              <div style={{ position: 'absolute', bottom: '4px', left: '8px', color: '#d4af37', fontSize: '0.75rem', opacity: 0.8 }}>
                ✦
              </div>
              <div style={{ position: 'absolute', bottom: '4px', right: '8px', color: '#d4af37', fontSize: '0.75rem', opacity: 0.8 }}>
                ✦
              </div>

              {/* Sloka Card Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', borderBottom: '1px solid #f0e6d2', paddingBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    backgroundColor: isCurrentActive ? '#4a0e17' : '#f5ebd9',
                    color: isCurrentActive ? '#ffffff' : '#4a0e17',
                    fontWeight: 700,
                    fontSize: '0.85rem',
                    padding: '4px 12px',
                    borderRadius: '16px',
                    border: '1px solid #d4af37'
                  }}>
                    శ్లోకం {sloka.slokaNo}
                  </span>
                  {isCurrentActive && (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', color: '#8b0000', fontWeight: 700 }}>
                      <Volume2 size={14} className="animate-pulse" /> Playing
                    </span>
                  )}
                </div>

                {/* Play Button for individual sloka */}
                {sloka.audioUrl && (
                  <button
                    onClick={() => onPlaySloka(dasakam.number, sloka.slokaNo)}
                    aria-label={`Play sloka ${sloka.slokaNo}`}
                    style={{
                      backgroundColor: isThisPlaying ? '#4a0e17' : '#fce8b3',
                      color: isThisPlaying ? '#ffffff' : '#4a0e17',
                      border: '1px solid #d4af37',
                      borderRadius: '50%',
                      width: '42px',
                      height: '42px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      cursor: 'pointer',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}
                  >
                    {isThisPlaying ? <Pause size={20} /> : <Play size={20} style={{ marginLeft: '2px' }} />}
                  </button>
                )}
              </div>

              {/* Slokam Text in Telugu with Centered Spacing & Golden Divider */}
              <div 
                className="telugu-text"
                style={{
                  fontSize: `calc(1.25rem * ${fontSizeMultiplier})`,
                  color: '#1a1a1a',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                  fontWeight: 600,
                  textAlign: 'center',
                  lineHeight: 1.85,
                  padding: '8px 0',
                  fontFamily: 'var(--font-telugu)'
                }}
              >
                {sloka.text}
              </div>

              {/* Bottom Decorative Divider */}
              <div style={{ textAlign: 'center', color: '#d4af37', fontSize: '0.85rem', marginTop: '6px', opacity: 0.8 }}>
                ❖ ─── 🪷 ─── ❖
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
