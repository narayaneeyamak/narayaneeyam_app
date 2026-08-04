import React from 'react';
import { BookOpen, Play, Sparkles, Heart } from 'lucide-react';

export default function HomeScreen({ 
  onSelectNarayaneeyam, 
  lastPlayedSloka, 
  onPlaySloka 
}) {
  return (
    <div 
      className="animate-fade-in" 
      style={{
        padding: '20px 16px 140px 16px',
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        minHeight: 'calc(100vh - 60px)',
        backgroundImage: `linear-gradient(rgba(248, 250, 252, 0.82), rgba(248, 250, 252, 0.88)), url('/images/home_bg.jpg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(79, 70, 229, 0.92) 0%, rgba(55, 48, 163, 0.95) 100%)',
        color: '#ffffff',
        padding: '24px 20px',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-lg)',
        position: 'relative',
        overflow: 'hidden',
        backdropFilter: 'blur(4px)'
      }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', opacity: 0.95, marginBottom: '6px' }}>
            <Sparkles size={16} color="#fbbf24" />
            <span>Devotional Prayer App</span>
          </div>
          <h2 style={{ fontSize: '1.7rem', fontWeight: 700, margin: '0 0 4px 0', fontFamily: 'var(--font-telugu)' }}>
            నారాయణీయం
          </h2>
          <p style={{ fontSize: '0.9rem', opacity: 0.95, margin: 0 }}>
            Srimad Narayaneeyam Slokas with Audio
          </p>
        </div>
        <div style={{
          position: 'absolute',
          right: '-10px',
          bottom: '-15px',
          fontSize: '90px',
          opacity: 0.18,
          userSelect: 'none'
        }}>
          🪷
        </div>
      </div>

      {/* Main Feature Button: Narayaneeyam */}
      <div>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.05em', textShadow: '0 1px 2px rgba(255, 255, 255, 0.8)' }}>
          Select Prayer / ప్రార్థన
        </h3>

        <button
          onClick={onSelectNarayaneeyam}
          style={{
            width: '100%',
            backgroundColor: 'rgba(255, 255, 255, 0.92)',
            border: '2px solid var(--primary)',
            borderRadius: 'var(--radius-md)',
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: '0 8px 20px rgba(79, 70, 229, 0.15)',
            backdropFilter: 'blur(8px)',
            transition: 'transform 0.15s, box-shadow 0.15s',
            textAlign: 'left'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{
              width: '54px',
              height: '54px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--primary-light)',
              color: 'var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: 'var(--shadow-sm)'
            }}>
              <BookOpen size={28} />
            </div>
            <div>
              <h4 style={{ fontSize: '1.3rem', fontWeight: 700, color: 'var(--text-main)', margin: '0 0 2px 0' }}>
                Narayaneeyam
              </h4>
              <p style={{ fontSize: '1.05rem', color: 'var(--primary)', fontWeight: 700, margin: 0, fontFamily: 'var(--font-telugu)' }}>
                నారాయణీయం (100 దశకాలు)
              </p>
            </div>
          </div>
          <div style={{
            backgroundColor: 'var(--primary)',
            color: '#fff',
            padding: '8px 16px',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.85rem',
            fontWeight: 700,
            boxShadow: 'var(--shadow-sm)'
          }}>
            Open
          </div>
        </button>
      </div>

      {/* Continue Listening (If last played exists) */}
      {lastPlayedSloka && (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.92)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: 'var(--shadow-md)',
          backdropFilter: 'blur(8px)'
        }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-gold)', textTransform: 'uppercase' }}>
              Recently Played
            </span>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-main)', margin: '2px 0 0 0' }}>
              Dasakam {lastPlayedSloka.dasakamNo} - Sloka {lastPlayedSloka.slokaNo}
            </h4>
          </div>
          <button
            onClick={() => onPlaySloka(lastPlayedSloka.dasakamNo, lastPlayedSloka.slokaNo)}
            style={{
              backgroundColor: 'var(--accent-gold-light)',
              color: 'var(--accent-gold)',
              border: 'none',
              borderRadius: '50%',
              width: '42px',
              height: '42px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer'
            }}
          >
            <Play size={20} style={{ marginLeft: '2px' }} />
          </button>
        </div>
      )}

      {/* App Info Footer */}
      <div style={{
        marginTop: 'auto',
        textAlign: 'center',
        paddingTop: '20px',
        color: 'var(--text-main)',
        fontSize: '0.8rem',
        fontWeight: 600
      }}>
        <p style={{ marginTop: '4px', opacity: 0.9 }}>Srimad Narayaneeyam Devotional Player</p>
      </div>
    </div>
  );
}
