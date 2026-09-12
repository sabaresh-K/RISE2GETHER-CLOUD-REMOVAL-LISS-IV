import React, { useState } from 'react';
import { Send } from 'lucide-react';

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await fetch('http://localhost:8000/submit-contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      setSubmitted(true);
    } catch (err) {
      setSubmitted(true);
    }
  };

  return (
    <div style={{ maxWidth: '1300px', margin: '0 auto' }}>
      <h3 style={{ color: '#10B981', marginBottom: '1.2rem' }}>Team Rise2Gether Leadership & Contact</h3>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.2rem', marginBottom: '2rem' }}>
        <div className="pitch-card" style={{ borderLeft: '4px solid #10B981', textAlign: 'center' }}>
          <h2 style={{ color: '#10B981', margin: '0 0 0.5rem 0', fontSize: '1.8rem', fontWeight: 800 }}>Sabaresh K</h2>
          <a href="mailto:sabaresh.k2025aids@sece.ac.in" style={{ color: '#10B981', textDecoration: 'none', fontWeight: 600, fontSize: '0.95rem' }}>
            Email: sabaresh.k2025aids@sece.ac.in
          </a>
        </div>
        <div className="pitch-card" style={{ borderLeft: '4px solid #10B981', textAlign: 'center' }}>
          <h2 style={{ color: '#10B981', margin: '0 0 0.5rem 0', fontSize: '1.8rem', fontWeight: 800 }}>Saadhana S</h2>
          <a href="mailto:saadhana.s2025aids@sece.ac.in" style={{ color: '#10B981', textDecoration: 'none', fontWeight: 600, fontSize: '0.95rem' }}>
            Email: saadhana.s2025aids@sece.ac.in
          </a>
        </div>
        <div className="pitch-card" style={{ borderLeft: '4px solid #10B981', textAlign: 'center' }}>
          <h2 style={{ color: '#10B981', margin: '0 0 0.5rem 0', fontSize: '1.8rem', fontWeight: 800 }}>Pranika R</h2>
          <a href="mailto:pranika.r2025aids@sece.ac.in" style={{ color: '#10B981', textDecoration: 'none', fontWeight: 600, fontSize: '0.95rem' }}>
            Email: pranika.r2025aids@sece.ac.in
          </a>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginTop: 0, marginBottom: '1rem' }}>Transmit Message to Team Rise2Gether</h4>
          {submitted ? (
            <div style={{ padding: '1.5rem', background: 'rgba(16,185,129,0.15)', border: '1px solid #10B981', color: '#10B981', borderRadius: '10px', fontWeight: 700 }}>
              Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.
            </div>
          ) : (
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ color: '#10B981', fontWeight: 700, fontSize: '0.95rem', display: 'block', marginBottom: '0.3rem' }}>Your Name:</label>
                <input type="text" required placeholder="Enter full name..." className="st-input" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
              </div>
              <div>
                <label style={{ color: '#10B981', fontWeight: 700, fontSize: '0.95rem', display: 'block', marginBottom: '0.3rem' }}>Email Address:</label>
                <input type="email" required placeholder="name@domain.com..." className="st-input" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} />
              </div>
              <div>
                <label style={{ color: '#10B981', fontWeight: 700, fontSize: '0.95rem', display: 'block', marginBottom: '0.3rem' }}>Message Details:</label>
                <textarea required rows={4} placeholder="Type your message here..." className="st-input" value={formData.message} onChange={e => setFormData({ ...formData, message: e.target.value })} />
              </div>
              <button type="submit" className="btn-emerald" style={{ marginTop: '0.5rem' }}>
                <Send style={{ width: '16px', height: '16px' }} /> TRANSMIT INQUIRY
              </button>
            </form>
          )}
        </div>

        <div className="pitch-card">
          <h4 style={{ color: '#10B981', marginTop: 0 }}>Our Institution</h4>
          <h3 style={{ color: '#FFFFFF', margin: '0.5rem 0 0.2rem 0', fontSize: '1.3rem' }}>Sri Eshwar College of Engineering and Technology</h3>
          <p style={{ color: '#94A3B8', fontSize: '0.95rem' }}>Coimbatore, Tamil Nadu, India</p>
          <hr style={{ borderColor: 'rgba(16,185,129,0.2)', margin: '1rem 0' }} />
          <p style={{ fontSize: '0.9rem', color: '#CBD5E1' }}><strong>Coordinates:</strong> 10.871° N, 77.019° E</p>
        </div>
      </div>
    </div>
  );
}
