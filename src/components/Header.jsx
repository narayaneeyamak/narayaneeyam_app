import React from 'react';
import { ArrowLeft, Sun, Moon, Type } from 'lucide-react';

export default function Header({ 
  currentView, 
  title, 
  onBack, 
  theme, 
  onToggleTheme, 
  fontSize, 
  onChangeFontSize 
}) {
  return (
    <header style={{
      position: 'sticky',
      top: 0,
      zIndex: 40,
      backgroundColor: 'var(--bg-card)',
      borderBottom: '1px solid var(--border)',
      padding: '12px 16px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {currentView !== 'home' && (
          <button 
            onClick={onBack}
            aria-label="Back"
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-main)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              backgroundColor: 'var(--bg-card-hover)',
              transition: 'background 0.2s'
            }}
          >
            <ArrowLeft size={20} />
          </button>
        )}

        <div>
          <h1 style={{
            fontSize: '1.1rem',
            fontWeight: 700,
            color: 'var(--text-main)',
            margin: 0,
            lineHeight: 1.2
          }}>
            {title}
          </h1>
          <p style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            margin: 0,
            fontFamily: 'var(--font-telugu)'
          }}>
            శ్రీమన్నారాయణీయం
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {/* Font size adjustment for Sloka view */}
        {currentView === 'sloka' && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            backgroundColor: 'var(--bg-card-hover)',
            borderRadius: 'var(--radius-sm)',
            padding: '2px 4px'
          }}>
            <button
              onClick={() => onChangeFontSize(-0.1)}
              title="Decrease font size"
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--text-main)',
                fontSize: '0.8rem',
                fontWeight: 600,
                padding: '4px 8px',
                cursor: 'pointer'
              }}
            >
              A-
            </button>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>|</span>
            <button
              onClick={() => onChangeFontSize(0.1)}
              title="Increase font size"
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--text-main)',
                fontSize: '1rem',
                fontWeight: 700,
                padding: '4px 8px',
                cursor: 'pointer'
              }}
            >
              A+
            </button>
          </div>
        )}

        {/* Theme Toggle */}
        <button
          onClick={onToggleTheme}
          aria-label="Toggle Theme"
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-main)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            backgroundColor: 'var(--bg-card-hover)',
            transition: 'background 0.2s'
          }}
        >
          {theme === 'dark' ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} />}
        </button>
      </div>
    </header>
  );
}
