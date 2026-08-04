import React, { useState } from 'react';
import { Folder, ChevronRight, Search, Music } from 'lucide-react';

export default function DasakamList({ dasakams, onSelectDasakam }) {
  const [filterText, setFilterText] = useState('');

  const filteredDasakams = dasakams.filter(d => {
    const q = filterText.toLowerCase();
    return (
      d.number.toString().includes(q) ||
      d.title.toLowerCase().includes(q) ||
      (d.titleTelugu && d.titleTelugu.includes(q))
    );
  });

  return (
    <div className="animate-fade-in" style={{ padding: '16px 16px 140px 16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
      
      {/* Search Input */}
      <div style={{ position: 'relative' }}>
        <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
        <input
          type="text"
          placeholder="Search Dasakam number or title..."
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 14px 12px 42px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            backgroundColor: 'var(--bg-card)',
            color: 'var(--text-main)',
            fontSize: '0.95rem',
            outline: 'none'
          }}
        />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-muted)' }}>
          All Dasakams ({filteredDasakams.length})
        </h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>
          దశకములు
        </span>
      </div>

      {/* Dasakam Folders List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {filteredDasakams.map((dasakam) => {
          const hasAudio = dasakam.slokas && dasakam.slokas.some(s => s.audioUrl);
          
          return (
            <button
              key={dasakam.id}
              onClick={() => onSelectDasakam(dasakam.id)}
              style={{
                backgroundColor: 'var(--bg-card)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'background 0.15s, border-color 0.15s',
                boxShadow: 'var(--shadow-sm)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <div style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: 'var(--radius-sm)',
                  backgroundColor: hasAudio ? 'var(--primary-light)' : 'var(--bg-card-hover)',
                  color: hasAudio ? 'var(--primary)' : 'var(--text-muted)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '1rem'
                }}>
                  {dasakam.number}
                </div>

                <div>
                  <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)', margin: '0 0 2px 0' }}>
                    {dasakam.title}
                  </h3>
                  {dasakam.titleTelugu && (
                    <p style={{ fontSize: '0.9rem', color: 'var(--primary)', margin: 0, fontFamily: 'var(--font-telugu)' }}>
                      {dasakam.titleTelugu}
                    </p>
                  )}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    <span>{dasakam.slokaCount || 0} Slokas</span>
                    {hasAudio && (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '2px', color: 'var(--accent-gold)' }}>
                        <Music size={12} /> Audio available
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <ChevronRight size={20} color="var(--text-muted)" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
