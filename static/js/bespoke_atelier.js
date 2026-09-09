/**
 * AETHER JEWELS – Interactive Bespoke Atelier 3D/Canvas Simulator
 */

const BespokeAtelier = (function () {
  let canvas, ctx;
  let rotationAngle = 0;
  let isDragging = false;
  let prevMouseX = 0;

  // Config State
  const state = {
    pieceType: 'Solitaire Ring',
    gemstone: 'Golconda Flawless Diamond',
    metal: '18k Celestial Champagne Gold',
    carat: 4.5,
    setting: 'Astral Halo',
    cut: 'Round Brilliant',
    estimatedPrice: 28500000, // INR
  };

  const GEM_COLORS = {
    'Golconda Flawless Diamond': { base: '#EBF4FA', core: '#FFFFFF', specular: '#FFF', accent: '#BEE3F8', fire: ['#FFD1DC', '#D0F0FD', '#FFE4B5'] },
    'Kashmir Royal Blue Sapphire': { base: '#0E2A66', core: '#1E4DB7', specular: '#70A1FF', accent: '#001A4E', fire: ['#4876FF', '#63B8FF', '#97C1A9'] },
    'Colombian Muzo Emerald': { base: '#0B4D2C', core: '#107E44', specular: '#55EFC4', accent: '#05311B', fire: ['#2ECC71', '#A8E6CF', '#88D49E'] },
    'Burmese Pigeon Blood Ruby': { base: '#6B0F1A', core: '#B31B2C', specular: '#FF7675', accent: '#45060D', fire: ['#E84118', '#FF6B81', '#F8A5C2'] },
    'Australian Black Opal': { base: '#1A1C29', core: '#2D3436', specular: '#00CEC9', accent: '#0C0D14', fire: ['#00B894', '#E17055', '#6C5CE7'] }
  };

  const METAL_COLORS = {
    '18k Celestial Champagne Gold': { ring: '#D4AF37', highlight: '#F7E7B4', shadow: '#7D6114' },
    '18k Rose Gold': { ring: '#E0A99A', highlight: '#FCE4DE', shadow: '#8C5749' },
    '950 Pure Platinum': { ring: '#DFE4EA', highlight: '#FFFFFF', shadow: '#747D8C' },
    '18k Midnight Black Rhodium': { ring: '#2C2D35', highlight: '#57606F', shadow: '#101115' }
  };

  function init() {
    canvas = document.getElementById('gemstone-canvas');
    if (!canvas) return;

    ctx = canvas.getContext('2d');
    canvas.width = 400;
    canvas.height = 400;

    bindEvents();
    calculatePrice();
    renderLoop();
  }

  function bindEvents() {
    // Canvas Mouse Interaction for 3D rotation
    canvas.addEventListener('mousedown', (e) => {
      isDragging = true;
      prevMouseX = e.clientX;
    });

    window.addEventListener('mouseup', () => { isDragging = false; });

    window.addEventListener('mousemove', (e) => {
      if (isDragging) {
        const deltaX = e.clientX - prevMouseX;
        rotationAngle += deltaX * 0.015;
        prevMouseX = e.clientX;
      }
    });

    // Touch events for mobile
    canvas.addEventListener('touchstart', (e) => {
      isDragging = true;
      prevMouseX = e.touches[0].clientX;
    }, { passive: true });

    window.addEventListener('touchend', () => { isDragging = false; });

    canvas.addEventListener('touchmove', (e) => {
      if (isDragging && e.touches.length > 0) {
        const deltaX = e.touches[0].clientX - prevMouseX;
        rotationAngle += deltaX * 0.015;
        prevMouseX = e.touches[0].clientX;
      }
    }, { passive: true });

    // Piece Type options
    document.querySelectorAll('.piece-type-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.piece-type-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.pieceType = this.dataset.value;
        calculatePrice();
      });
    });

    // Gemstone options
    document.querySelectorAll('.gem-option-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.gem-option-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.gemstone = this.dataset.value;
        calculatePrice();
      });
    });

    // Metal options
    document.querySelectorAll('.metal-option-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.metal-option-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.metal = this.dataset.value;
        calculatePrice();
      });
    });

    // Setting options
    document.querySelectorAll('.setting-option-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.setting-option-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.setting = this.dataset.value;
        calculatePrice();
      });
    });

    // Carat Slider
    const caratSlider = document.getElementById('carat-range-slider');
    const caratDisplay = document.getElementById('carat-val-num');
    if (caratSlider && caratDisplay) {
      caratSlider.addEventListener('input', function () {
        state.carat = parseFloat(this.value);
        caratDisplay.textContent = state.carat.toFixed(2) + ' ct';
        calculatePrice();
      });
    }

    // Bespoke Inquiry Form Submission via AJAX
    const bespokeForm = document.getElementById('bespoke-inquiry-form');
    if (bespokeForm) {
      bespokeForm.addEventListener('submit', handleBespokeSubmit);
    }
  }

  function calculatePrice() {
    let baseRatePerCarat = 2500000; // INR per carat

    if (state.gemstone === 'Golconda Flawless Diamond') baseRatePerCarat = 3800000;
    else if (state.gemstone === 'Kashmir Royal Blue Sapphire') baseRatePerCarat = 2900000;
    else if (state.gemstone === 'Colombian Muzo Emerald') baseRatePerCarat = 3200000;
    else if (state.gemstone === 'Burmese Pigeon Blood Ruby') baseRatePerCarat = 3500000;
    else if (state.gemstone === 'Australian Black Opal') baseRatePerCarat = 1200000;

    let metalFactor = 450000;
    if (state.metal && state.metal.includes('Platinum')) metalFactor = 750000;
    else if (state.metal && state.metal.includes('Rose')) metalFactor = 480000;

    let settingFactor = 350000;
    if (state.setting === 'Astral Halo') settingFactor = 850000;
    else if (state.setting === 'Royal Pavé Cascade') settingFactor = 1200000;

    const rawTotal = Math.round((baseRatePerCarat * Math.pow(state.carat, 1.25)) + metalFactor + settingFactor);
    state.estimatedPrice = rawTotal;

    // Update UI Valuation Display
    const priceDisplay = document.getElementById('config-price-estimate');
    if (priceDisplay) {
      if (rawTotal >= 10000000) {
        priceDisplay.textContent = `₹ ${(rawTotal / 10000000).toFixed(2)} Cr`;
      } else {
        priceDisplay.textContent = `₹ ${(rawTotal / 100000).toFixed(2)} Lakhs`;
      }
    }
  }

  function drawProngRing(centerX, centerY, radius, metal) {
    const m = METAL_COLORS[metal] || METAL_COLORS['18k Celestial Champagne Gold'];

    // Outer Ring Shank
    ctx.save();
    let ringGrad = ctx.createLinearGradient(centerX - radius, centerY, centerX + radius, centerY + radius * 1.5);
    ringGrad.addColorStop(0, m.highlight);
    ringGrad.addColorStop(0.5, m.ring);
    ringGrad.addColorStop(1, m.shadow);

    ctx.strokeStyle = ringGrad;
    ctx.lineWidth = 14;
    ctx.shadowBlur = 15;
    ctx.shadowColor = 'rgba(0,0,0,0.8)';

    ctx.beginPath();
    ctx.arc(centerX, centerY + radius * 0.75, radius * 0.95, Math.PI * 0.15, Math.PI * 0.85);
    ctx.stroke();
    ctx.restore();

    // Astral Prongs
    ctx.save();
    ctx.strokeStyle = m.highlight;
    ctx.lineWidth = 4;
    const prongCount = 6;
    for (let i = 0; i < prongCount; i++) {
      const angle = (Math.PI * 2 / prongCount) * i + rotationAngle * 0.5;
      const px = centerX + Math.cos(angle) * (radius * 0.78);
      const py = centerY + Math.sin(angle) * (radius * 0.78);

      ctx.beginPath();
      ctx.arc(px, py, 4, 0, Math.PI * 2);
      ctx.fillStyle = m.highlight;
      ctx.fill();
    }
    ctx.restore();
  }

  function drawGemstone(centerX, centerY, baseRadius, gemType) {
    const gem = GEM_COLORS[gemType] || GEM_COLORS['Golconda Flawless Diamond'];
    const scale = (state.carat / 4.5) * 0.85 + 0.4;
    const radius = baseRadius * scale;

    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(rotationAngle);

    // Gem Core Base
    let radialGlow = ctx.createRadialGradient(0, 0, 5, 0, 0, radius);
    radialGlow.addColorStop(0, gem.core);
    radialGlow.addColorStop(0.7, gem.base);
    radialGlow.addColorStop(1, gem.accent);

    ctx.fillStyle = radialGlow;
    ctx.shadowBlur = 30;
    ctx.shadowColor = gem.specular;

    // Outer Octagonal Facet Contour
    const facets = 8;
    ctx.beginPath();
    for (let i = 0; i < facets; i++) {
      const angle = (Math.PI * 2 / facets) * i;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fill();

    // Internal Triangular Facet Mesh
    ctx.lineWidth = 1.2;
    for (let i = 0; i < facets; i++) {
      const angle1 = (Math.PI * 2 / facets) * i;
      const angle2 = (Math.PI * 2 / facets) * (i + 1);

      const x1 = Math.cos(angle1) * radius;
      const y1 = Math.sin(angle1) * radius;
      const x2 = Math.cos(angle2) * radius;
      const y2 = Math.sin(angle2) * radius;

      const innerX1 = Math.cos(angle1) * (radius * 0.5);
      const innerY1 = Math.sin(angle1) * (radius * 0.5);

      // Facet fill with dynamic light flash
      let facetGrad = ctx.createLinearGradient(x1, y1, 0, 0);
      let flash = (Math.sin(rotationAngle * 2 + i) + 1) / 2;
      facetGrad.addColorStop(0, gem.fire[i % gem.fire.length]);
      facetGrad.addColorStop(1, 'transparent');

      ctx.save();
      ctx.globalAlpha = 0.45 * flash + 0.15;
      ctx.fillStyle = facetGrad;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.lineTo(0, 0);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // Facet wirelines
      ctx.strokeStyle = gem.specular;
      ctx.globalAlpha = 0.5;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(innerX1, innerY1);
      ctx.lineTo(0, 0);
      ctx.stroke();
    }

    // Central Table Facet
    ctx.beginPath();
    for (let i = 0; i < facets; i++) {
      const angle = (Math.PI * 2 / facets) * i;
      const x = Math.cos(angle) * (radius * 0.45);
      const y = Math.sin(angle) * (radius * 0.45);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = gem.core;
    ctx.globalAlpha = 0.7;
    ctx.fill();
    ctx.strokeStyle = '#FFFFFF';
    ctx.stroke();

    // Central Starlight Sparkle Glint
    ctx.globalAlpha = (Math.sin(rotationAngle * 3) + 1) / 2 * 0.8 + 0.2;
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.arc(-radius * 0.2, -radius * 0.2, 4, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  }

  function renderLoop() {
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Draw Setting Mount
    drawProngRing(centerX, centerY, 110, state.metal);

    // Draw Gemstone
    drawGemstone(centerX, centerY, 80, state.gemstone);

    // Auto rotate slowly if user is not dragging
    if (!isDragging) {
      rotationAngle += 0.004;
    }

    requestAnimationFrame(renderLoop);
  }

  async function handleBespokeSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    const clientName = form.querySelector('#client-name')?.value.trim();
    const email = form.querySelector('#client-email')?.value.trim();
    const phone = form.querySelector('#client-phone')?.value.trim();
    const customEngraving = form.querySelector('#custom-engraving')?.value.trim() || '';
    const notes = form.querySelector('#bespoke-notes')?.value.trim() || '';

    if (!clientName || !email || !phone) {
      if (window.showToast) window.showToast('Please complete name, email, and phone contact.', 'error');
      return;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise fs-5 me-1"></i> Transmitting Dossier...';
    }

    try {
      const response = await fetch('/api/bespoke/inquire/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || '',
        },
        body: JSON.stringify({
          client_name: clientName,
          email: email,
          phone: phone,
          piece_type: state.pieceType,
          gemstone: state.gemstone,
          metal: state.metal,
          carat_weight: state.carat,
          setting_style: state.setting,
          estimated_price_inr: state.estimatedPrice,
          custom_engraving: customEngraving,
          notes: notes,
        })
      });

      const data = await response.json();

      if (data.success) {
        if (window.showToast) window.showToast(data.message, 'success');
        form.reset();
      } else {
        if (window.showToast) window.showToast(data.error || 'Failed to submit inquiry.', 'error');
      }
    } catch (err) {
      if (window.showToast) window.showToast('Error connecting to Celestial Concierge.', 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-stars me-2"></i> Dispatch Commission Request';
      }
    }
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  document.addEventListener('DOMContentLoaded', init);

  return {
    getState: () => state,
    calculate: calculatePrice,
  };
})();
