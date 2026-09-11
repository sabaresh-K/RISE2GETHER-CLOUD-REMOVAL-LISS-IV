import React from 'react';

export default function About() {
  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <div className="pitch-card">
        <h2 style={{ color: '#10B981', marginTop: 0 }}>About CloudClear-LISS Science & Benchmarks</h2>
        <p style={{ fontSize: '1.1rem', color: '#E2E8F0', lineHeight: 1.6 }}>
          The <strong>Linear Imaging Self-Scanning Sensor (LISS-IV)</strong> operating onboard Resourcesat satellites provides 
          high-resolution multispectral imagery with a spatial resolution of 5.8 meters. 
          Cloud removal is an essential preprocessing step for land cover classification, disaster management, and agricultural monitoring.
        </p>
      </div>

      <h3 style={{ color: '#10B981', margin: '2rem 0 1rem 0' }}>Verified Quantitative Benchmarks</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
        <div className="metric-card-box"><div className="metric-card-val">30.24 dB</div><div className="metric-card-lbl">PSNR</div></div>
        <div className="metric-card-box"><div className="metric-card-val">0.884</div><div className="metric-card-lbl">SSIM</div></div>
        <div className="metric-card-box"><div className="metric-card-val">4.52°</div><div className="metric-card-lbl">SAM</div></div>
        <div className="metric-card-box"><div className="metric-card-val">0.032</div><div className="metric-card-lbl">RMSE</div></div>
        <div className="metric-card-box"><div className="metric-card-val">94.6%</div><div className="metric-card-lbl">Mask Acc</div></div>
        <div className="metric-card-box"><div className="metric-card-val">2.84s</div><div className="metric-card-lbl">Speed</div></div>
      </div>
    </div>
  );
}
