import React from 'react';
import { BookOpen, Play, Sparkles } from 'lucide-react';

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
        backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.35)), url('/images/home_bg.jpg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed'
      }}
    >
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(79, 70, 229, 0.95) 0%, rgba(49, 46, 129, 0.98) 100%)',
        color: '#ffffff',
        padding: '24px 20px',
        borderRadius: 'var(--radius-lg)',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.3)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', color: '#fde047', fontWeight: 600, marginBottom: '6px' }}>
            <Sparkles size={16} fill="#fde047" />
            <span>Devotional Prayer App</span>
          </div>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 800, margin: '0 0 4px 0', fontFamily: 'var(--font-telugu)', color: '#ffffff' }}>
            నారాయణీయం
          </h2>
          <p style={{ fontSize: '0.95rem', opacity: 0.95, margin: 0, color: '#e0e7ff' }}>
            Srimad Narayaneeyam Slokas with Audio
          </p>
        </div>
        <div style={{
          position: 'absolute',
          right: '-10px',
          bottom: '-15px',
          fontSize: '90px',
          opacity: 0.2,
          userSelect: 'none'
        }}>
          🪷
        </div>
      </div>

      {/* Main Feature Button: Narayaneeyam */}
      <div>
        <div style={{
          display: 'inline-block',
          backgroundColor: 'rgba(15, 23, 42, 0.75)',
          color: '#ffffff',
          padding: '6px 14px',
          borderRadius: '20px',
          fontSize: '0.85rem',
          fontWeight: 700,
          marginBottom: '12px',
          backdropFilter: 'blur(4px)',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)'
        }}>
          SELECT PRAYER / ప్రార్థన
        </div>

        <button
          onClick={onSelectNarayaneeyam}
          style={{
            width: '100%',
            backgroundColor: '#ffffff',
            border: '2px solid var(--primary)',
            borderRadius: 'var(--radius-md)',
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.25)',
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
              <h4 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#0f172a', margin: '0 0 2px 0' }}>
                Narayaneeyam
              </h4>
              <p style={{ fontSize: '1.05rem', color: 'var(--primary)', fontWeight: 700, margin: 0, fontFamily: 'var(--font-telugu)' }}>
                నారాయణీయం (100 దశకాలు)
              </p>
            </div>
          </div>
          <div style={{
            backgroundColor: 'var(--primary)',
            color: '#ffffff',
            padding: '8px 18px',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.9rem',
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
          backgroundColor: '#ffffff',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 8px 20px rgba(0, 0, 0, 0.2)'
        }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--accent-gold)', textTransform: 'uppercase' }}>
              Recently Played
            </span>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a', margin: '2px 0 0 0' }}>
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
        color: '#ffffff',
        fontSize: '0.85rem',
        fontWeight: 600,
        textShadow: '0 2px 6px rgba(0, 0, 0, 0.8)'
      }}>
        <p style={{ margin: 0 }}>Srimad Narayaneeyam Devotional Player</p>
      </div>
    </div>
  );
}
