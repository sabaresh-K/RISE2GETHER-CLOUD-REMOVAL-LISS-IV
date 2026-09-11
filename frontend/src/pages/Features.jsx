import React from 'react';

export default function Features() {
  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <h3 style={{ color: '#10B981', marginBottom: '1rem' }}>System Features & Competitive Capabilities</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.2rem' }}>
        <div className="pitch-card" style={{ borderLeft: '4px solid #10B981' }}>
          <h4 style={{ color: '#10B981' }}>LISS-IV 5.8m Resolution Preservation</h4>
          <p style={{ color: '#94A3B8', marginTop: '0.4rem' }}>Specifically engineered for LISS-IV 5.8m pixel spacing without downscaling.</p>
        </div>
        <div className="pitch-card" style={{ borderLeft: '4px solid #10B981' }}>
          <h4 style={{ color: '#10B981' }}>Multi-Sensor Fusion Engine</h4>
          <p style={{ color: '#94A3B8', marginTop: '0.4rem' }}>Fuses optical reflection with Sentinel-1 C-band active radar backscatter.</p>
        </div>
        <div className="pitch-card" style={{ borderLeft: '4px solid #F59E0B' }}>
          <h4 style={{ color: '#F59E0B' }}>CycleGAN Generative Core</h4>
          <p style={{ color: '#94A3B8', marginTop: '0.4rem' }}>Dual generators ensure realistic, spectrally accurate ground texture synthesis.</p>
        </div>
        <div className="pitch-card" style={{ borderLeft: '4px solid #8B5CF6' }}>
          <h4 style={{ color: '#8B5CF6' }}>Full Georeferenced GeoTIFF Export</h4>
          <p style={{ color: '#94A3B8', marginTop: '0.4rem' }}>Exports GIS-ready GeoTIFF rasters with intact CRS metadata.</p>
        </div>
      </div>

      <h3 style={{ color: '#10B981', margin: '2.5rem 0 1rem 0' }}>Performance Comparison Matrix</h3>
      <div className="pitch-card" style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', color: '#E2E8F0' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #10B981', textAlign: 'left' }}>
              <th style={{ padding: '0.8rem', color: '#10B981' }}>Feature / Capability</th>
              <th style={{ padding: '0.8rem' }}>Spatial Interpolation</th>
              <th style={{ padding: '0.8rem' }}>Optical-Only Neural Net</th>
              <th style={{ padding: '0.8rem', color: '#10B981' }}>CloudClear-LISS (Fusion)</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <td style={{ padding: '0.8rem', fontWeight: 600 }}>Heavy Cloud (&gt;80%)</td>
              <td style={{ padding: '0.8rem', color: '#EF4444' }}>Fails (extreme blur)</td>
              <td style={{ padding: '0.8rem', color: '#EF4444' }}>Fails (lacks structure)</td>
              <td style={{ padding: '0.8rem', color: '#10B981', fontWeight: 700 }}>Reconstructs via Radar</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <td style={{ padding: '0.8rem', fontWeight: 600 }}>5.8m Resolution Preservation</td>
              <td style={{ padding: '0.8rem', color: '#EF4444' }}>Blurs textures (&gt;20m)</td>
              <td style={{ padding: '0.8rem', color: '#10B981' }}>Retains resolution</td>
              <td style={{ padding: '0.8rem', color: '#10B981', fontWeight: 700 }}>Retains Native 5.8m</td>
            </tr>
            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <td style={{ padding: '0.8rem', fontWeight: 600 }}>GeoTIFF CRS Transfer</td>
              <td style={{ padding: '0.8rem', color: '#10B981' }}>Retained</td>
              <td style={{ padding: '0.8rem', color: '#EF4444' }}>Exports JPEG/PNG</td>
              <td style={{ padding: '0.8rem', color: '#10B981', fontWeight: 700 }}>Full GeoTIFF Metadata</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
