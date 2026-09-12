import React, { useState } from 'react';
import { Download } from 'lucide-react';

export default function ImageConversion() {
  const [stacked, setStacked] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleConvert = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/convert-bands', { method: 'POST' });
      const data = await res.json();
      if (data.status === "success") {
        setStacked(true);
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <div className="pitch-card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ color: '#10B981', margin: '0 0 0.4rem 0', fontSize: '1.8rem', fontWeight: 800 }}>
          LISS-IV Multi-Band Stacking & Conversion Engine
        </h2>
        <p style={{ color: '#94A3B8', fontSize: '0.95rem', margin: 0 }}>
          Upload raw single-band LISS-IV GeoTIFF rasters (B2, B3, B4) to synthesize a unified multi-band GeoTIFF and high-contrast False Color Composite (FCC) preview.
        </p>
      </div>

      <h3 style={{ color: '#10B981', marginBottom: '1rem' }}>Single-Band Input Dropzones</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.2rem' }}>
        <div className="pitch-card" style={{ borderTop: '4px solid #10B981', textAlign: 'center' }}>
          <h4 style={{ color: '#10B981', fontSize: '1.1rem', fontWeight: 800 }}>Band 2 (B2 - Green)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.52 - 0.59 µm Spectral Range</p>
          <input type="file" accept=".tif,.geotiff,.png,.jpg" className="st-input" />
        </div>

        <div className="pitch-card" style={{ borderTop: '4px solid #F59E0B', textAlign: 'center' }}>
          <h4 style={{ color: '#F59E0B', fontSize: '1.1rem', fontWeight: 800 }}>Band 3 (B3 - Red)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.62 - 0.68 µm Spectral Range</p>
          <input type="file" accept=".tif,.geotiff,.png,.jpg" className="st-input" />
        </div>

        <div className="pitch-card" style={{ borderTop: '4px solid #8B5CF6', textAlign: 'center' }}>
          <h4 style={{ color: '#8B5CF6', fontSize: '1.1rem', fontWeight: 800 }}>Band 4 (B4 - Near-Infrared)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.77 - 0.86 µm Spectral Range</p>
          <input type="file" accept=".tif,.geotiff,.png,.jpg" className="st-input" />
        </div>
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <button className="btn-emerald" style={{ width: '100%' }} onClick={handleConvert} disabled={loading}>
          {loading ? 'STACKING BANDS & BUILDING GEOTIFF...' : 'STACK & CONVERT BANDS'}
        </button>
      </div>

      {stacked && (
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ color: '#10B981', marginBottom: '1.2rem' }}>CONVERSION & STACKING COMPLETE</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
            <div className="pitch-card" style={{ borderLeft: '4px solid #10B981' }}>
              <h4 style={{ color: '#10B981', marginTop: 0 }}>1. Visual False Color Composite (FCC) Preview (.PNG)</h4>
              <p style={{ color: '#94A3B8', fontSize: '0.88rem', margin: '0.2rem 0 0.8rem 0' }}>
                Radiometrically normalized 3-band composite (Red: NIR, Green: Red, Blue: Green).
              </p>
              <img src="/outputs/liss_rgb.png" alt="FCC Preview" style={{ width: '100%', borderRadius: '8px' }} />
              <a href="/outputs/liss_rgb.png" download="liss4_combined_image.png" className="btn-emerald" style={{ marginTop: '0.8rem', width: '100%', textDecoration: 'none' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Preview (.PNG)
              </a>
            </div>

            <div className="pitch-card" style={{ borderLeft: '4px solid #00D4FF' }}>
              <h4 style={{ color: '#10B981', marginTop: 0 }}>2. GIS-Ready Multi-Band Raster (.TIF)</h4>
              <p style={{ color: '#94A3B8', fontSize: '0.88rem', margin: '0.2rem 0 0.8rem 0' }}>
                Stacked 3-band GeoTIFF raster preserving spatial resolution and CRS metadata.
              </p>
              <div className="metric-card-box" style={{ textAlign: 'left', padding: '1rem', marginBottom: '1rem' }}>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Spatial Resolution:</strong> 5.8m Native LISS-IV</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Band Count:</strong> 3 Layers</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Band Order:</strong> Layer 1: B4 (NIR), Layer 2: B3 (Red), Layer 3: B2 (Green)</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>CRS Projection:</strong> EPSG:32644 (UTM Zone 44N)</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Format:</strong> Multi-Band GeoTIFF (.TIF)</p>
              </div>
              <a href="/outputs/liss_rgb.png" download="liss4_combined_multiband.tif" className="btn-emerald" style={{ width: '100%', textDecoration: 'none' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Multi-Band Raster (.TIF)
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
