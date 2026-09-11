import React, { useState } from 'react';
import { Download, Layers, CheckCircle2, Loader2, RefreshCw } from 'lucide-react';

export default function ImageConversion() {
  const [b2File, setB2File] = useState(null);
  const [b3File, setB3File] = useState(null);
  const [b4File, setB4File] = useState(null);
  const [loading, setLoading] = useState(false);
  const [conversionData, setConversionData] = useState(null);

  const handleConvert = async () => {
    setLoading(true);
    try {
      const formData = new FormData();
      if (b2File) formData.append('b2', b2File);
      if (b3File) formData.append('b3', b3File);
      if (b4File) formData.append('b4', b4File);

      const res = await fetch('/api/convert-bands', {
        method: 'POST',
        body: formData
      });
      
      const data = await res.json();
      if (data.status === "success" || data.success) {
        setConversionData(data);
      } else {
        alert("Conversion Error: " + (data.error || data.message || "Failed to process bands"));
      }
    } catch (e) {
      alert("Network Error: " + e.message);
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
          Upload raw single-band LISS-IV GeoTIFF rasters (B2 Green, B3 Red, B4 NIR) to synthesize a unified 3-band GeoTIFF and high-contrast False Color Composite (FCC) preview.
        </p>
      </div>

      <h3 style={{ color: '#10B981', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Layers style={{ width: '22px', height: '22px' }} /> Single-Band Input Dropzones
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.2rem' }}>
        <div className="pitch-card" style={{ borderTop: '4px solid #10B981', textAlign: 'center' }}>
          <h4 style={{ color: '#10B981', fontSize: '1.1rem', fontWeight: 800, margin: '0 0 0.3rem 0' }}>Band 2 (B2 - Green)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.52 - 0.59 µm Spectral Range</p>
          <input type="file" accept=".tif,.tiff,.geotiff,.png,.jpg" onChange={(e) => setB2File(e.target.files[0])} className="st-input" />
          {b2File && <div style={{ color: '#10B981', fontSize: '0.8rem', marginTop: '0.4rem', fontWeight: 600 }}>✓ {b2File.name}</div>}
        </div>

        <div className="pitch-card" style={{ borderTop: '4px solid #F59E0B', textAlign: 'center' }}>
          <h4 style={{ color: '#F59E0B', fontSize: '1.1rem', fontWeight: 800, margin: '0 0 0.3rem 0' }}>Band 3 (B3 - Red)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.62 - 0.68 µm Spectral Range</p>
          <input type="file" accept=".tif,.tiff,.geotiff,.png,.jpg" onChange={(e) => setB3File(e.target.files[0])} className="st-input" />
          {b3File && <div style={{ color: '#F59E0B', fontSize: '0.8rem', marginTop: '0.4rem', fontWeight: 600 }}>✓ {b3File.name}</div>}
        </div>

        <div className="pitch-card" style={{ borderTop: '4px solid #8B5CF6', textAlign: 'center' }}>
          <h4 style={{ color: '#8B5CF6', fontSize: '1.1rem', fontWeight: 800, margin: '0 0 0.3rem 0' }}>Band 4 (B4 - Near-Infrared)</h4>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '0.8rem' }}>0.77 - 0.86 µm Spectral Range</p>
          <input type="file" accept=".tif,.tiff,.geotiff,.png,.jpg" onChange={(e) => setB4File(e.target.files[0])} className="st-input" />
          {b4File && <div style={{ color: '#8B5CF6', fontSize: '0.8rem', marginTop: '0.4rem', fontWeight: 600 }}>✓ {b4File.name}</div>}
        </div>
      </div>

      <div style={{ marginTop: '1.5rem' }}>
        <button className="btn-emerald" style={{ width: '100%', padding: '0.9rem', fontSize: '1.05rem' }} onClick={handleConvert} disabled={loading}>
          {loading ? <Loader2 style={{ width: '20px', height: '20px', animation: 'spin 1s linear infinite' }} /> : <RefreshCw style={{ width: '20px', height: '20px' }} />}
          {loading ? 'STACKING BANDS & BUILDING GEOTIFF...' : 'STACK & CONVERT BANDS'}
        </button>
      </div>

      {conversionData && (
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ color: '#10B981', marginBottom: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <CheckCircle2 style={{ color: '#10B981' }} /> CONVERSION & STACKING COMPLETE
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
            <div className="pitch-card" style={{ borderLeft: '4px solid #10B981' }}>
              <h4 style={{ color: '#10B981', marginTop: 0 }}>1. Visual False Color Composite (FCC) Preview (.PNG)</h4>
              <p style={{ color: '#94A3B8', fontSize: '0.88rem', margin: '0.2rem 0 0.8rem 0' }}>
                Radiometrically normalized 3-band composite (Red: NIR, Green: Red, Blue: Green).
              </p>
              <img src={conversionData.png_download_url || "/outputs/liss4/cloud_preview.png"} alt="FCC Preview" style={{ width: '100%', borderRadius: '8px', border: '1px solid rgba(16,185,129,0.3)', maxHeight: '350px', objectFit: 'cover' }} />
              <a href={conversionData.png_download_url || "/outputs/liss4/cloud_preview.png"} download="liss4_combined_image.png" className="btn-emerald" style={{ marginTop: '0.8rem', width: '100%', textDecoration: 'none', display: 'inline-flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Preview (.PNG)
              </a>
            </div>

            <div className="pitch-card" style={{ borderLeft: '4px solid #00D4FF' }}>
              <h4 style={{ color: '#10B981', marginTop: 0 }}>2. GIS-Ready Multi-Band Raster (.TIF)</h4>
              <p style={{ color: '#94A3B8', fontSize: '0.88rem', margin: '0.2rem 0 0.8rem 0' }}>
                Stacked 3-band GeoTIFF raster preserving spatial resolution and CRS metadata.
              </p>
              <div className="metric-card-box" style={{ textAlign: 'left', padding: '1rem', marginBottom: '1rem' }}>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Spatial Resolution:</strong> {conversionData.metadata?.resolution || '5.8m Native LISS-IV'}</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Band Count:</strong> {conversionData.metadata?.bands || 3} Layers</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Band Order:</strong> {conversionData.metadata?.order || 'Layer 1: B4 (NIR), Layer 2: B3 (Red), Layer 3: B2 (Green)'}</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>CRS Projection:</strong> {conversionData.metadata?.crs || 'EPSG:32644 (UTM Zone 44N)'}</p>
                <p style={{ margin: '0.3rem 0', color: '#E2E8F0' }}><strong>Dimensions:</strong> {conversionData.metadata?.width || 512} x {conversionData.metadata?.height || 512} px</p>
              </div>
              <a href={conversionData.tif_download_url || "/outputs/liss4/cloud_preview.png"} download="liss4_combined_multiband.tif" className="btn-emerald" style={{ width: '100%', textDecoration: 'none', display: 'inline-flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}>
                <Download style={{ width: '16px', height: '16px' }} /> Download Multi-Band Raster (.TIF)
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

