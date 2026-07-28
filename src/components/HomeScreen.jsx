import React from 'react';
import { BookOpen, Play, Search, Sparkles, Heart } from 'lucide-react';

export default function HomeScreen({ 
  onSelectNarayaneeyam, 
  lastPlayedSloka, 
  onPlaySloka,
  searchQuery,
  setSearchQuery
}) {
  return (
    <div className="animate-fade-in" style={{ padding: '20px 16px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      {/* Welcome Banner */}
      <div style={{
        background: 'linear-gradient(135deg, var(--primary) 0%, #3730a3 100%)',
        color: '#ffffff',
        padding: '24px 20px',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-md)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', opacity: 0.9, marginBottom: '6px' }}>
            <Sparkles size={16} color="#fbbf24" />
            <span>Devotional Prayer App</span>
          </div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 700, margin: '0 0 4px 0', fontFamily: 'var(--font-telugu)' }}>
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
          opacity: 0.15,
          userSelect: 'none'
        }}>
          🪷
        </div>
      </div>

      {/* Main Feature Button: Narayaneeyam */}
      <div>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Select Prayer / ప్రార్థన
        </h3>

        <button
          onClick={onSelectNarayaneeyam}
          style={{
            width: '100%',
            backgroundColor: 'var(--bg-card)',
            border: '2px solid var(--primary)',
            borderRadius: 'var(--radius-md)',
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            boxShadow: 'var(--shadow-md)',
            transition: 'transform 0.15s, box-shadow 0.15s',
            textAlign: 'left'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{
              width: '52px',
              height: '52px',
              borderRadius: 'var(--radius-md)',
              backgroundColor: 'var(--primary-light)',
              color: 'var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <BookOpen size={28} />
            </div>
            <div>
              <h4 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-main)', margin: '0 0 2px 0' }}>
                Narayaneeyam
              </h4>
              <p style={{ fontSize: '1.05rem', color: 'var(--primary)', fontWeight: 600, margin: 0, fontFamily: 'var(--font-telugu)' }}>
                నారాయణీయం (100 దశకాలు)
              </p>
            </div>
          </div>
          <div style={{
            backgroundColor: 'var(--primary)',
            color: '#fff',
            padding: '8px 14px',
            borderRadius: 'var(--radius-sm)',
            fontSize: '0.85rem',
            fontWeight: 600
          }}>
            Open
          </div>
        </button>
      </div>

      {/* Continue Listening (If last played exists) */}
      {lastPlayedSloka && (
        <div style={{
          backgroundColor: 'var(--bg-card)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-md)',
          padding: '16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: 'var(--shadow-sm)'
        }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--accent-gold)', textTransform: 'uppercase' }}>
              Recently Played
            </span>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-main)', margin: '2px 0 0 0' }}>
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
        color: 'var(--text-muted)',
        fontSize: '0.8rem'
      }}>
        <p style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}>
          Made with <Heart size={14} color="#ef4444" fill="#ef4444" /> for Mom
        </p>
        <p style={{ marginTop: '4px', opacity: 0.8 }}>Srimad Narayaneeyam Devotional Player</p>
      </div>
    </div>
  );
}
