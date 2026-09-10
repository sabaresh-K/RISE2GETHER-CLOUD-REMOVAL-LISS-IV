/**
 * CloudClear-LISS — Application Controller & Interactive Router
 * Created for Bharatiya Antariksh Hackathon 2026 (ISRO)
 */

document.addEventListener('DOMContentLoaded', () => {
  initRouter();
  initBackgroundCanvas();
  initContactForm();
  initHeaderScroll();
  initTypingEffect();
  initSRS();
});

/* ================= HEADER SCROLL EFFECT ================= */
function initHeaderScroll() {
  const header = document.getElementById('site-header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* ================= HASH ROUTER ================= */
function initRouter() {
  const pages = document.querySelectorAll('.page-section');
  const navItems = document.querySelectorAll('nav ul li');

  function handleRoute() {
    let hash = window.location.hash || '#/home';
    let targetPage = hash.replace('#/', '');

    const validPages = ['home', 'about', 'features', 'contact'];
    if (!validPages.includes(targetPage)) {
      targetPage = 'home';
      window.location.hash = '#/home';
    }

    pages.forEach(page => {
      if (page.id === targetPage) {
        page.classList.add('active');
      } else {
        page.classList.remove('active');
      }
    });

    navItems.forEach(item => {
      if (item.getAttribute('data-page') === targetPage) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  window.addEventListener('hashchange', handleRoute);
  handleRoute();
}

/* ================= NEURAL BACKGROUND CANVAS ================= */
function initBackgroundCanvas() {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  const particles = [];
  const particleCount = Math.min(60, Math.floor((width * height) / 18000));
  const maxDistance = 120;

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.radius = Math.random() * 2 + 1;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(0, 212, 255, 0.4)';
      ctx.fill();
    }
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];
      p1.update();
      p1.draw();

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDistance) {
          const alpha = (maxDistance - dist) / maxDistance * 0.18;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(0, 212, 255, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animate);
  }

  animate();
}

/* ================= TYPING EFFECT ================= */
function initTypingEffect() {
  const typingText = document.getElementById('typing-text');
  if (!typingText) return;

  const words = ["Beneath the Clouds.", "Through Multi-Sensor Fusion.", "For LISS-IV Satellite Scenes."];
  let wordIdx = 0, charIdx = 0, isDeleting = false;

  function type() {
    const current = words[wordIdx];
    if (isDeleting) {
      typingText.textContent = current.substring(0, charIdx - 1);
      charIdx--;
    } else {
      typingText.textContent = current.substring(0, charIdx + 1);
      charIdx++;
    }

    let speed = isDeleting ? 60 : 100;

    if (!isDeleting && charIdx === current.length) {
      isDeleting = true;
      speed = 1800;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      wordIdx = (wordIdx + 1) % words.length;
      speed = 500;
    }

    setTimeout(type, speed);
  }

  setTimeout(type, 800);
}

/* ================= SRS DATA VIEWER ================= */
const srsData = {
  intro: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">1. Introduction & Objectives</h3>
    <h4 style="color: #fff; margin-top: 1rem;">1.1 Purpose</h4>
    <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">Develop, train, validate, and deploy a production-grade Generative AI framework that ingests cloud-contaminated LISS-IV imagery along with auxiliary SAR data to generate georeferenced, cloud-free GeoTIFF products.</p>
    <h4 style="color: #fff; margin-top: 1rem;">1.2 Objectives</h4>
    <ul style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">
      <li>Develop an intelligent cloud removal framework for LISS-IV satellite imagery.</li>
      <li>Reconstruct high-quality cloud-free images with preserved 5.8m resolution.</li>
      <li>Deploy API-enabled scalable solution.</li>
    </ul>
  `,
  scope: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">2. Product Scope & Systems</h3>
    <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">Detects and removes cloud occlusions from LISS-IV satellite imagery using Sentinel-1 SAR microwave guidance and CycleGAN neural networks.</p>
  `,
  functional: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">3. Functional Requirements</h3>
    <ul style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.8;">
      <li><strong>FR 1:</strong> Upload LISS-IV Image asset up to 10GB.</li>
      <li><strong>FR 2:</strong> Preprocess & align optical and SAR raster tiles.</li>
      <li><strong>FR 3:</strong> Detect cloud and shadow masks with 94%+ accuracy.</li>
      <li><strong>FR 4:</strong> Run PyTorch CycleGAN reconstruction engine.</li>
      <li><strong>FR 5:</strong> Export georeferenced GeoTIFF and evaluate PSNR/SSIM/SAM/RMSE metrics.</li>
    </ul>
  `,
  nonfunctional: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">4. Non-Functional Requirements</h3>
    <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">Sub-second preprocessing latency, 99.9% uptime, CUDA GPU acceleration, and strict CRS metadata transfer.</p>
  `,
  system: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">5. System Requirements</h3>
    <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">Python 3.9+, PyTorch 2.0+, OpenCV, NumPy, Rasterio, GDAL, NVIDIA CUDA GPU with >=8GB VRAM.</p>
  `,
  diagrams: `
    <h3 style="color: var(--primary-cyan); font-size: 1.3rem; margin-top: 0;">6. Use Cases & Database</h3>
    <p style="font-size: 0.9rem; color: var(--text-muted); line-height: 1.6;">USER, SATELLITE_DATA, PROCESSING_JOB, RECONSTRUCTION_RESULT, QUALITY_METRICS.</p>
  `
};

function initSRS() {
  const tabs = document.querySelectorAll('.srs-tab');
  const container = document.getElementById('srs-content-container');
  if (!tabs.length || !container) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const key = tab.getAttribute('data-srs');
      container.innerHTML = srsData[key] || '';
    });
  });

  container.innerHTML = srsData['intro'];
}

/* ================= CONTACT FORM ================= */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you! Your message has been sent to Team Rise2Gether.');
    form.reset();
  });
}
