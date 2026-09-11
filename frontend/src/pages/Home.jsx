import React from 'react';
import { ArrowRight } from 'lucide-react';

export default function Home({ onNavigate }) {
  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <div className="pitch-card" style={{ textAlign: 'center', padding: '3.5rem 2rem' }}>
        <h1 style={{ color: '#10B981', fontSize: '3rem', fontWeight: 900, margin: '0 0 1.2rem 0', lineHeight: 1.2 }}>
          Revealing the Earth Beneath the Clouds
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#E2E8F0', maxWidth: '850px', margin: '0 auto 2.2rem auto', lineHeight: 1.6 }}>
          AI-Powered Cloud Removal and Ground Surface Reconstruction for <strong>LISS-IV</strong> Satellite Imagery. 
          Fusing Sentinel-1 C-band SAR radar backscatter with multi-band optical sensors to restore obscured terrain details with 5.8m spatial precision.
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn-emerald" onClick={() => onNavigate('Model')}>
            Try Interactive Workbench <ArrowRight style={{ width: '18px', height: '18px' }} />
          </button>
          <button className="btn-emerald" style={{ background: 'rgba(15, 23, 42, 0.9)', border: '1px solid #10B981', color: '#10B981' }} onClick={() => onNavigate('About')}>
            Explore Science & Benchmarks
          </button>
        </div>
      </div>

      <h3 style={{ color: '#10B981', margin: '2rem 0 1rem 0', fontSize: '1.4rem' }}>End-to-End Technical Pipeline</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.2rem' }}>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginBottom: '0.4rem' }}>01. Data Acquisition</h4>
          <p style={{ fontSize: '0.9rem', color: '#94A3B8' }}>5.8m LISS-IV optical bands + Sentinel-1 C-band SAR radar.</p>
        </div>
        <div className="pitch-card">
          <h4 style={{ color: '#F97316', marginBottom: '0.4rem' }}>02. Preprocessing</h4>
          <p style={{ fontSize: '0.9rem', color: '#94A3B8' }}>Sub-pixel co-registration, calibration, and cloud/shadow mask extraction.</p>
        </div>
        <div className="pitch-card">
          <h4 style={{ color: '#F59E0B', marginBottom: '0.4rem' }}>03. AI Processing</h4>
          <p style={{ fontSize: '0.9rem', color: '#94A3B8' }}>SAR-guided CycleGAN / UNet model infuses radar structural features into masks.</p>
        </div>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginBottom: '0.4rem' }}>04. Output Layer</h4>
          <p style={{ fontSize: '0.9rem', color: '#94A3B8' }}>GeoTIFF export with full CRS metadata & telemetry validation.</p>
        </div>
      </div>

      <h3 style={{ color: '#10B981', margin: '2.5rem 0 1rem 0', fontSize: '1.4rem' }}>Downstream High-Value Impact</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.2rem' }}>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginBottom: '0.4rem' }}>Precision Agriculture</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.9rem' }}>Continuous NDVI monitoring throughout monsoon seasons without waiting gaps.</p>
        </div>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginBottom: '0.4rem' }}>Emergency Flood Response</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.9rem' }}>Active radar penetrates storm clouds to delineate standing water boundaries in real time.</p>
        </div>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginBottom: '0.4rem' }}>Forestry & Urban Sprawl</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.9rem' }}>Track canopy density and urban growth metrics with high spatial confidence.</p>
        </div>
      </div>
    </div>
  );
}
