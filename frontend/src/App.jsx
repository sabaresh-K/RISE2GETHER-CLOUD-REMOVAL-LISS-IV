import React, { useState } from 'react';
import Navbar from './components/Navbar';
import StardustCanvas from './components/StardustCanvas';
import Home from './pages/Home';
import About from './pages/About';
import Features from './pages/Features';
import ModelWorkspace from './pages/ModelWorkspace';
import ImageConversion from './pages/ImageConversion';
import Contact from './pages/Contact';

export default function App() {
  const [activePage, setActivePage] = useState('Home');

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
      <StardustCanvas />
      <Navbar activePage={activePage} setActivePage={setActivePage} />

      <main style={{ flex: 1, padding: '0 1rem 3rem 1rem' }}>
        {activePage === 'Home' && <Home onNavigate={setActivePage} />}
        {activePage === 'About' && <About />}
        {activePage === 'Features' && <Features />}
        {activePage === 'Model' && <ModelWorkspace />}
        {activePage === 'Image Conversion' && <ImageConversion />}
        {activePage === 'Contact' && <Contact />}
      </main>

      <footer style={{
        borderTop: '1px solid rgba(16,185,129,0.2)',
        padding: '1.5rem 1rem',
        textAlign: 'center',
        color: '#94A3B8',
        fontSize: '0.88rem',
        background: 'rgba(6,9,19,0.85)'
      }}>
        © 2026 CloudClear-LISS. Built by Team Rise2Gether. All rights reserved.
      </footer>
    </div>
  );
}
