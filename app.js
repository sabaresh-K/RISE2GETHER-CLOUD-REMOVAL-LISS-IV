/**
 * CloudClear-LISS — Application Controller
 * Created for Bharatiya Antariksh Hackathon 2026 (ISRO)
 */

document.addEventListener('DOMContentLoaded', () => {
  initRouter();
  initBackgroundCanvas();
  initBeforeAfterSliders();
  initInteractiveDemo();
  initContactForm();
  initHeaderScroll();
  initInteractiveSRS();
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

    const validPages = ['home', 'about', 'features', 'demo', 'contact'];
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
  const particleCount = Math.min(60, Math.floor((width * height) / 20000));
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

/* ================= COMPARISON BEFORE/AFTER SLIDER ================= */
function initBeforeAfterSliders() {
  const container = document.getElementById('wb-comparison-slider');
  const afterImg = document.getElementById('wb-slider-img-after');
  const divider = document.getElementById('wb-slider-divider');

  if (!container || !afterImg || !divider) return;

  let isDragging = false;

  function move(clientX) {
    const rect = container.getBoundingClientRect();
    const x = clientX - rect.left;
    let percentage = (x / rect.width) * 100;

    if (percentage < 0) percentage = 0;
    if (percentage > 100) percentage = 100;

    afterImg.style.clipPath = `inset(0 0 0 ${percentage}%)`;
    divider.style.left = `${percentage}%`;
  }

  divider.addEventListener('mousedown', () => isDragging = true);
  window.addEventListener('mouseup', () => isDragging = false);
  window.addEventListener('mousemove', (e) => {
    if (isDragging) move(e.clientX);
  });

  divider.addEventListener('touchstart', () => isDragging = true);
  window.addEventListener('touchend', () => isDragging = false);
  window.addEventListener('touchmove', (e) => {
    if (isDragging) move(e.touches[0].clientX);
  });
}

/* ================= INTERACTIVE DEMO ================= */
function initInteractiveDemo() {
  const runBtn = document.getElementById('btn-workbench-run');
  const lissInput = document.getElementById('liss4Upload');
  const afterImg = document.querySelector('#wb-slider-img-after img');

  if (runBtn) {
    runBtn.addEventListener('click', async () => {
      runBtn.disabled = true;
      runBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running PyTorch UNet...';

      let file = lissInput && lissInput.files[0] ? lissInput.files[0] : null;

      try {
        let formData = new FormData();
        if (file) {
          formData.append('file', file);
        }

        let res = await fetch('/api/process-raster', {
          method: 'POST',
          body: file ? file : JSON.stringify({ preset: 'default' })
        });

        let data = await res.json();
        if (data.success && data.reconstructed_image) {
          if (afterImg) afterImg.src = data.reconstructed_image;
          runBtn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Process Complete!';
        } else {
          runBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Process Raster Tile';
        }
      } catch (e) {
        console.log('API call fallback mode');
        runBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Process Raster Tile';
      }

      setTimeout(() => {
        runBtn.disabled = false;
        runBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Process Raster Tile';
      }, 1500);
    });
  }
}

/* ================= CONTACT FORM ================= */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you! Your inquiry has been transmitted to Team Rise2Gether.');
    form.reset();
  });
}

/* ================= INTERACTIVE SRS DATA VIEWER ================= */
const srsData = {
  intro: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">1. Introduction & Objectives</h3>
    <p>This project aims to develop, train, validate, and deploy a production-grade Generative AI framework that ingests cloud-contaminated LISS-IV imagery along with auxiliary SAR data, detects and masks cloud pixels, reconstructs the underlying surface reflectance, and exports georeferenced GeoTIFF products.</p>
  `,
  scope: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">2. Product Scope & Existing Systems</h3>
    <p>In Scope: Detect and remove clouds from LISS-IV satellite images using Generative AI, fusing Sentinel-1 SAR radar backscatter.</p>
  `,
  functional: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">3. Functional Requirements</h3>
    <p>FR1: Upload LISS-IV | FR2: Upload SAR | FR3: Preprocess | FR4: Detect Clouds | FR5: AI Reconstruction | FR6: Export GeoTIFF.</p>
  `,
  nonfunctional: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">4. Non-Functional Details</h3>
    <p>Performance: Under 3 seconds response time per tile. Security: Encrypted transmission and authorized access.</p>
  `,
  system: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">5. System Requirements</h3>
    <p>Python 3.9+, PyTorch, OpenCV, Rasterio, GDAL, NVIDIA CUDA GPU acceleration with CPU fallback.</p>
  `,
  diagrams: `
    <h3 style="color: var(--primary-cyan); margin-top:0;">6. Use Cases & Database</h3>
    <p>Tables: USER, SATELLITE_DATA, PROCESSING_JOB, RECONSTRUCTION_RESULT, QUALITY_METRICS.</p>
  `
};

function initInteractiveSRS() {
  const tabs = document.querySelectorAll('.srs-tab');
  const container = document.getElementById('srs-content-container');
  if (!tabs.length || !container) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const key = tab.getAttribute('data-srs');
      if (container) container.innerHTML = srsData[key] || '';
    });
  });

  if (container) container.innerHTML = srsData['intro'];
}
