import React, { useEffect, useState } from 'react';
import { Activity, Radio } from 'lucide-react';

export default function Navbar({ activePage, setActivePage }) {
  const [apiOnline, setApiOnline] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/process-raster', { method: 'OPTIONS' })
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  const navItems = ['Home', 'About', 'Features', 'Model', 'Image Conversion', 'Contact'];

  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto', padding: '1.2rem 1rem 0 1rem' }}>
      <div className="pitch-header" style={{
        background: 'rgba(15, 23, 42, 0.85)',
        border: '1px solid rgba(16, 185, 129, 0.35)',
        borderBottom: '2px solid #10B981',
        borderRadius: '14px',
        padding: '1.4rem 2rem',
        marginBottom: '1.5rem',
        boxShadow: '0 12px 35px rgba(16, 185, 129, 0.18)',
        backdropFilter: 'blur(16px)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div>
          <div style={{
            fontSize: '2.3rem',
            fontWeight: 900,
            background: 'linear-gradient(90deg, #FFFFFF 0%, #10B981 50%, #34D399 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '1.2px'
          }}>
            CloudClear-LISS
          </div>
          <div style={{ fontSize: '0.98rem', color: '#94A3B8', marginTop: '0.25rem' }}>
            AI-Powered Satellite Imagery Cloud Reconstruction Platform (React Edition)
          </div>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.6rem',
          background: apiOnline ? 'rgba(16, 185, 129, 0.18)' : 'rgba(239, 68, 68, 0.18)',
          border: `1px solid ${apiOnline ? '#10B981' : '#EF4444'}`,
          color: apiOnline ? '#10B981' : '#EF4444',
          padding: '0.45rem 1.1rem',
          borderRadius: '20px',
          fontSize: '0.85rem',
          fontWeight: 700,
          boxShadow: `0 0 18px ${apiOnline ? 'rgba(16, 185, 129, 0.35)' : 'rgba(239, 68, 68, 0.35)'}`
        }}>
          <Radio style={{ width: '16px', height: '16px' }} />
          <span>{apiOnline ? 'MODEL ENGINE: ONLINE (PORT 8000)' : 'MODEL ENGINE: STANDBY'}</span>
        </div>
      </div>

      <div style={{
        background: 'rgba(15, 23, 42, 0.85)',
        border: '1px solid rgba(16, 185, 129, 0.35)',
        borderRadius: '30px',
        padding: '0.55rem 1.4rem',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '1.2rem',
        marginBottom: '1.8rem',
        boxShadow: '0 6px 25px rgba(0,0,0,0.45)',
        backdropFilter: 'blur(12px)',
        flexWrap: 'wrap'
      }}>
        {navItems.map((page) => {
          const isActive = activePage === page;
          return (
            <button
              key={page}
              onClick={() => setActivePage(page)}
              style={{
                background: isActive ? 'linear-gradient(90deg, #059669 0%, #10B981 100%)' : 'transparent',
                color: isActive ? '#FFFFFF' : '#CBD5E1',
                border: isActive ? '1px solid #34D399' : '1px solid transparent',
                borderRadius: '20px',
                padding: '0.45rem 1.2rem',
                fontWeight: 700,
                fontSize: '0.98rem',
                cursor: 'pointer',
                transition: 'all 0.25s ease',
                boxShadow: isActive ? '0 0 15px rgba(16, 185, 129, 0.4)' : 'none'
              }}
            >
              {page}
            </button>
          );
        })}
      </div>
    </div>
  );
}
