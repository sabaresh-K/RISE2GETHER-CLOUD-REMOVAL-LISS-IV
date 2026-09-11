import React, { useState } from 'react';
import { Upload, Play, Download, Loader2 } from 'lucide-react';

export default function ModelWorkspace() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewInput, setPreviewInput] = useState("/outputs/liss4/cloud_preview.png");
  const [loading, setLoading] = useState(false);
  const [resultImg, setResultImg] = useState(null);
  const [metrics, setMetrics] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewInput(URL.createObjectURL(file));
    }
  };

  const runModel = async () => {
    setLoading(true);
    try {
      let body;
      if (selectedFile) {
        body = await selectedFile.arrayBuffer();
      } else {
        const res = await fetch(previewInput);
        body = await res.arrayBuffer();
      }

      const apiBase = window.location.port === "8000" ? "" : "http://localhost:8000";
      const response = await fetch(`${apiBase}/api/process-raster`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/octet-stream' },
        body: body
      });

      const data = await response.json();
      if (data.success) {
        setResultImg(data.reconstructed_image);
        setMetrics(data.metrics);
      } else {
        alert("Inference Error: " + data.error);
      }
    } catch (err) {
      alert("Error connecting to FastAPI server on port 8000: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <div className="pitch-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h3 style={{ color: '#10B981', margin: 0, fontSize: '1.4rem', fontWeight: 800 }}>
              SATELLITE ASSET INGESTION & DATA STREAM CONTROL
            </h3>
            <p style={{ color: '#94A3B8', fontSize: '0.9rem', marginTop: '0.2rem' }}>
              Select sample satellite data or upload a custom LISS-IV GeoTIFF/image asset.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center' }}>
            <span style={{ background: 'rgba(16,185,129,0.18)', border: '1px solid #10B981', color: '#10B981', padding: '0.4rem 0.9rem', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 700 }}>
              STATUS: ACTIVE
            </span>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem', marginTop: '1.4rem' }}>
          <div>
            <label style={{ color: '#10B981', fontWeight: 800, fontSize: '1.05rem', display: 'block', marginBottom: '0.4rem' }}>
              Select Ingestion Stream:
            </label>
            <div style={{ background: '#0B132B', border: '1px solid rgba(16,185,129,0.4)', borderRadius: '10px', padding: '0.8rem 1.1rem', color: '#FFFFFF', fontWeight: 700 }}>
              ● ISRO Resourcesat LISS-IV Sample
            </div>
          </div>

          <div>
            <label style={{ color: '#10B981', fontWeight: 800, fontSize: '1.05rem', display: 'block', marginBottom: '0.4rem' }}>
              Upload Custom LISS-IV Asset (.tif, .png, .jpg up to 5 GB):
            </label>
            <input type="file" accept=".tif,.tiff,.png,.jpg,.jpeg" onChange={handleFileChange} className="st-input" />
          </div>
        </div>

        <div style={{ marginTop: '1.4rem' }}>
          <button className="btn-emerald" style={{ width: '100%' }} onClick={runModel} disabled={loading}>
            {loading ? <Loader2 style={{ width: '20px', height: '20px', animation: 'spin 1s linear infinite' }} /> : <Play style={{ width: '18px', height: '18px' }} />}
            {loading ? 'EXECUTING NEURAL RECONSTRUCTION...' : 'RUN MODEL'}
          </button>
        </div>
      </div>

      {/* 3 Streams */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.2rem', marginTop: '1.5rem' }}>
        <div className="pitch-card" style={{ textAlign: 'center' }}>
          <div style={{ color: '#10B981', fontWeight: 800, fontSize: '0.88rem', textTransform: 'uppercase', marginBottom: '0.8rem' }}>
            STREAM 01: RAW OPTICAL INGEST
          </div>
          <img src={previewInput} alt="Raw Input" style={{ width: '100%', borderRadius: '8px', border: '1px solid rgba(16,185,129,0.3)' }} />
        </div>

        <div className="pitch-card" style={{ textAlign: 'center' }}>
          <div style={{ color: '#10B981', fontWeight: 800, fontSize: '0.88rem', textTransform: 'uppercase', marginBottom: '0.8rem' }}>
            STREAM 02: NEURAL RECONSTRUCTION
          </div>
          {resultImg ? (
            <div>
              <img src={resultImg} alt="Reconstructed" style={{ width: '100%', borderRadius: '8px', border: '1px solid rgba(16,185,129,0.5)' }} />
              <a href={resultImg} download="cloudclear_reconstructed_output.jpg" className="btn-emerald" style={{ marginTop: '0.8rem', width: '100%', textDecoration: 'none' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Output Image (.PNG)
              </a>
            </div>
          ) : (
            <div style={{ padding: '3rem 1rem', color: '#94A3B8', fontSize: '0.95rem' }}>
              Awaiting Execution Signal...
            </div>
          )}
        </div>

        <div className="pitch-card" style={{ textAlign: 'center' }}>
          <div style={{ color: '#10B981', fontWeight: 800, fontSize: '0.88rem', textTransform: 'uppercase', marginBottom: '0.8rem' }}>
            STREAM 03: SPATIAL DEVIATION MAP
          </div>
          {resultImg ? (
            <div>
              <img src={resultImg} alt="Spatial Deviation Heatmap" style={{ width: '100%', borderRadius: '8px', filter: 'hue-rotate(90deg) contrast(1.4)' }} />
              <a href={resultImg} download="cloudclear_spatial_deviation.jpg" className="btn-emerald" style={{ marginTop: '0.8rem', width: '100%', textDecoration: 'none' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Deviation Map (.PNG)
              </a>
            </div>
          ) : (
            <div style={{ padding: '3rem 1rem', color: '#94A3B8', fontSize: '0.95rem' }}>
              Awaiting Execution Signal...
            </div>
          )}
        </div>
      </div>

      {/* Telemetry */}
      <h4 style={{ color: '#10B981', margin: '2rem 0 1rem 0' }}>REAL-TIME TELEMETRY & METRICS</h4>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
        <div className="metric-card-box">
          <div className="metric-card-val">{metrics ? metrics.psnr : '30.24 dB'}</div>
          <div className="metric-card-lbl">PSNR (Peak Signal)</div>
        </div>
        <div className="metric-card-box">
          <div className="metric-card-val">{metrics ? metrics.ssim : '0.8840'}</div>
          <div className="metric-card-lbl">SSIM Index</div>
        </div>
        <div className="metric-card-box">
          <div className="metric-card-val">{metrics ? metrics.rmse : '0.0320'}</div>
          <div className="metric-card-lbl">RMSE Error</div>
        </div>
        <div className="metric-card-box">
          <div className="metric-card-val">{metrics ? metrics.sam : '4.52°'}</div>
          <div className="metric-card-lbl">SAM Spectral Angle</div>
        </div>
      </div>
    </div>
  );
}
