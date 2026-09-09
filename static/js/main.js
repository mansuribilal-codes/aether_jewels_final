/**
 * AETHER JEWELS – Unified Luxury Interaction Controller & 3D Engine
 */

// Global Premium Toast System
window.showToast = function (message, type = 'gold') {
  let container = document.getElementById('luxury-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'luxury-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `luxury-toast ${type === 'error' ? 'toast-error' : type === 'info' ? 'toast-info' : 'toast-gold'}`;

  let icon = 'bi bi-stars text-warning';
  if (type === 'error') icon = 'bi bi-exclamation-triangle-fill text-danger';
  else if (type === 'info') icon = 'bi bi-info-circle-fill text-info';
  else if (type === 'success') icon = 'bi bi-check-circle-fill text-success';

  toast.innerHTML = `
    <i class="${icon} fs-5 me-3"></i>
    <div style="flex: 1;">
      <p style="margin: 0; line-height: 1.4; font-size: 13px; color: #EDE8DF;">${message}</p>
    </div>
    <button type="button" class="btn-close btn-close-white ms-2" style="font-size: 10px;" onclick="this.parentElement.remove()"></button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 4500);
};

document.addEventListener('DOMContentLoaded', function () {
  // =========================================================================
  // 1. NAVBAR SCROLL WATCHER
  // =========================================================================
  const navbar = document.querySelector('.navbar-aether');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // =========================================================================
  // 2. ELEGANT 3D PRODUCT CARD PARALLAX TILT & SPECULAR GLARE
  // =========================================================================
  const cards3D = document.querySelectorAll('.product-card-3d');
  cards3D.forEach(card => {
    let glare = card.querySelector('.card-glare');
    if (!glare) {
      glare = document.createElement('div');
      glare.className = 'card-glare';
      card.appendChild(glare);
    }

    card.addEventListener('mousemove', function (e) {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -10;
      const rotateY = ((x - centerX) / centerX) * 10;

      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(8px)`;

      const glarePercentX = (x / rect.width) * 100;
      const glarePercentY = (y / rect.height) * 100;
      glare.style.background = `radial-gradient(circle at ${glarePercentX}% ${glarePercentY}%, rgba(255, 235, 170, 0.22) 0%, transparent 60%)`;
    });

    card.addEventListener('mouseleave', function () {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
    });
  });

  // =========================================================================
  // 3. PRODUCT QUICK VIEW MODAL DYNAMICS
  // =========================================================================
  const quickviewModal = document.getElementById('quickviewModal');
  document.addEventListener('click', async function (e) {
    const qvBtn = e.target.closest('.card-quickview-btn, .quick-view-btn');
    if (qvBtn && quickviewModal) {
      e.preventDefault();
      const productId = qvBtn.dataset.productId || qvBtn.getAttribute('data-product-id');
      if (!productId) return;

      const bsModal = bootstrap.Modal.getOrCreateInstance(quickviewModal);
      bsModal.show();

      const container = document.getElementById('quickview-content');
      if (container) {
        container.innerHTML = `
          <div style="padding: 4rem; text-align: center;">
            <div class="spinner-border text-warning mb-3" role="status"></div>
            <p style="color: var(--gold-champagne, #E8D390); font-family: 'Playfair Display', serif; font-size: 1.1rem;">Accessing Sovereign Vault Registry...</p>
          </div>
        `;

        try {
          const res = await fetch(`/api/products/${productId}/quickview/`);
          const data = await res.json();
          if (data.success) {
            const p = data.product;
            container.innerHTML = `
              <div class="row g-4 p-4 align-items-center">
                <div class="col-md-6 text-center">
                  <div class="position-relative overflow-hidden rounded border border-warning" style="background: #0D0E14; max-height: 380px;">
                    <img src="${p.image_primary}" alt="${p.title}" class="img-fluid w-100" style="height: 360px; object-fit: cover;" onerror="this.src='https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80';">
                    <span class="badge-gold position-absolute top-0 start-0 m-3">${p.certification}</span>
                  </div>
                </div>
                <div class="col-md-6 d-flex flex-column justify-content-between">
                  <div>
                    <span class="text-gold text-uppercase small fw-bold" style="letter-spacing: 1.5px; font-size: 10px;">${p.metal_description}</span>
                    <h3 class="text-white font-heading mt-1 mb-2 fs-4">${p.title}</h3>
                    <p class="text-gold fst-italic small mb-3">${p.subtitle}</p>
                    <p class="text-secondary small mb-3" style="line-height: 1.6;">${p.description}</p>
                    
                    <div class="p-3 mb-3 rounded" style="background: rgba(22, 24, 38, 0.7); border: 1px solid rgba(212,175,55,0.2);">
                      <div class="row g-2 text-secondary small">
                        <div class="col-6">GEMSTONE: <strong class="text-white">${p.primary_gemstone}</strong></div>
                        <div class="col-6">METAL: <strong class="text-white">${p.metal_description}</strong></div>
                        <div class="col-6">WEIGHT/CARAT: <strong class="text-white">${p.carat_weight} ct/g</strong></div>
                        <div class="col-6">AVAILABILITY: <strong class="text-success">${p.stock > 0 ? 'In Vault Stock' : 'Pre-Order'}</strong></div>
                      </div>
                    </div>
                  </div>

                  <div>
                    <div class="d-flex align-items-baseline justify-content-between mb-3">
                      <span class="text-muted small text-uppercase" style="letter-spacing: 1px;">Sovereign Valuation</span>
                      <span class="text-gold fs-4 fw-bold font-heading">${p.formatted_price}</span>
                    </div>

                    <div class="d-flex gap-2">
                      <a href="${p.url}" class="btn btn-outline-gold flex-grow-1 btn-sm py-2">
                        <i class="bi bi-gem me-1"></i> Full Dossier
                      </a>
                      <a href="/cart/add/${p.id}/" class="btn btn-gold flex-grow-1 btn-sm py-2">
                        <i class="bi bi-bag-plus me-1"></i> Add to Bag
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            `;
          }
        } catch (err) {
          container.innerHTML = `<p class="p-4 text-center text-danger">Failed to load jewel specifications. Please try again.</p>`;
        }
      }
    }
  });

  // =========================================================================
  // 4. THREE.JS INTERACTIVE 3D CELESTIAL GEMSTONE VIEWER
  // =========================================================================
  let threeScene, threeCamera, threeRenderer, threeDiamond, threeControls;
  let threePointLight1, threePointLight2, threeAmbientLight;
  let threeInitialized = false;

  const threeContainer = document.getElementById('threeDiamondContainer');
  const diamondModalEl = document.getElementById('diamond3DModal');

  if (threeContainer && diamondModalEl && typeof THREE !== 'undefined') {
    diamondModalEl.addEventListener('shown.bs.modal', function () {
      if (!threeInitialized) {
        initThreeDiamond(threeContainer);
        threeInitialized = true;
      } else {
        onThreeWindowResize();
      }
    });
  }

  function initThreeDiamond(container) {
    const width = container.clientWidth || 700;
    const height = container.clientHeight || 420;

    threeScene = new THREE.Scene();
    threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    threeCamera.position.set(0, 1.2, 4.2);

    threeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    threeRenderer.setSize(width, height);
    threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    threeRenderer.toneMapping = THREE.ACESFilmicToneMapping;
    threeRenderer.toneMappingExposure = 1.3;
    container.appendChild(threeRenderer.domElement);

    if (typeof THREE.OrbitControls !== 'undefined') {
      threeControls = new THREE.OrbitControls(threeCamera, threeRenderer.domElement);
      threeControls.enableDamping = true;
      threeControls.dampingFactor = 0.05;
      threeControls.autoRotate = true;
      threeControls.autoRotateSpeed = 1.5;
      threeControls.maxDistance = 7;
      threeControls.minDistance = 2;
    }

    const diamondGeometry = new THREE.OctahedronGeometry(1.35, 2);
    const diamondMaterial = new THREE.MeshPhysicalMaterial({
      color: 0xffffff,
      metalness: 0.1,
      roughness: 0.05,
      transmission: 0.92,
      ior: 2.42,
      reflectivity: 0.9,
      clearcoat: 1.0,
      clearcoatRoughness: 0.05,
      flatShading: true,
    });

    threeDiamond = new THREE.Mesh(diamondGeometry, diamondMaterial);
    threeScene.add(threeDiamond);

    threeAmbientLight = new THREE.AmbientLight(0x222233, 1.2);
    threeScene.add(threeAmbientLight);

    threePointLight1 = new THREE.PointLight(0xfff0c8, 2.5, 20);
    threePointLight1.position.set(3, 4, 3);
    threeScene.add(threePointLight1);

    threePointLight2 = new THREE.PointLight(0xd4af37, 2.0, 20);
    threePointLight2.position.set(-3, -2, -3);
    threeScene.add(threePointLight2);

    const pointLight3 = new THREE.PointLight(0xffffff, 1.8, 15);
    pointLight3.position.set(0, 3, -3);
    threeScene.add(pointLight3);

    function animate() {
      requestAnimationFrame(animate);
      if (threeControls) threeControls.update();
      threeRenderer.render(threeScene, threeCamera);
    }
    animate();

    window.addEventListener('resize', onThreeWindowResize);
  }

  function onThreeWindowResize() {
    if (!threeRenderer || !threeContainer || !threeCamera) return;
    const width = threeContainer.clientWidth;
    const height = threeContainer.clientHeight;
    threeCamera.aspect = width / height;
    threeCamera.updateProjectionMatrix();
    threeRenderer.setSize(width, height);
  }

  // Gemstone Switcher
  const gemColorBtns = document.querySelectorAll('.gem-color-btn');
  gemColorBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      gemColorBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const gem = this.getAttribute('data-gem');
      if (!threeDiamond) return;

      const colors = {
        'diamond': { color: 0xffffff, transmission: 0.94, ior: 2.42 },
        'emerald': { color: 0x00d26a, transmission: 0.85, ior: 1.58 },
        'sapphire': { color: 0x1a73e8, transmission: 0.88, ior: 1.77 },
        'ruby': { color: 0xeb144c, transmission: 0.86, ior: 1.76 },
        'tanzanite': { color: 0x6a1b9a, transmission: 0.90, ior: 1.69 },
      };

      const cfg = colors[gem] || colors['diamond'];
      threeDiamond.material.color.setHex(cfg.color);
      threeDiamond.material.transmission = cfg.transmission;
      threeDiamond.material.ior = cfg.ior;
      threeDiamond.material.needsUpdate = true;
    });
  });

  // Lighting Switcher
  const lightEnvBtns = document.querySelectorAll('.light-env-btn');
  lightEnvBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      lightEnvBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const lightMode = this.getAttribute('data-light');
      if (!threePointLight1 || !threePointLight2) return;

      if (lightMode === 'candlelight') {
        threePointLight1.color.setHex(0xffaa33);
        threePointLight2.color.setHex(0xd4af37);
        threeAmbientLight.color.setHex(0x331900);
      } else if (lightMode === 'daylight') {
        threePointLight1.color.setHex(0xffffff);
        threePointLight2.color.setHex(0xe0f2fe);
        threeAmbientLight.color.setHex(0x444455);
      } else {
        threePointLight1.color.setHex(0xfff0c8);
        threePointLight2.color.setHex(0xd4af37);
        threeAmbientLight.color.setHex(0x222233);
      }
    });
  });

  // =========================================================================
  // 5. FLOATING VIP CONCIERGE WIDGET TOGGLE
  // =========================================================================
  const conciergeTrigger = document.getElementById('conciergeTriggerBtn');
  const conciergeMenu = document.getElementById('conciergeMenu');

  if (conciergeTrigger && conciergeMenu) {
    conciergeTrigger.addEventListener('click', function (e) {
      e.stopPropagation();
      conciergeMenu.classList.toggle('show');
    });

    document.addEventListener('click', function (e) {
      if (!conciergeMenu.contains(e.target) && !conciergeTrigger.contains(e.target)) {
        conciergeMenu.classList.remove('show');
      }
    });
  }

  // =========================================================================
  // 6. IMAGE GALLERY THUMBNAIL SWITCHER
  // =========================================================================
  const mainProductImg = document.getElementById('mainProductImage');
  const galleryThumbs = document.querySelectorAll('.gallery-thumb-item');

  if (mainProductImg && galleryThumbs.length > 0) {
    galleryThumbs.forEach(thumb => {
      thumb.addEventListener('click', function () {
        galleryThumbs.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        const newSrc = this.getAttribute('data-img-src');
        if (newSrc) {
          mainProductImg.style.opacity = '0.3';
          setTimeout(() => {
            mainProductImg.src = newSrc;
            mainProductImg.style.opacity = '1';
          }, 150);
        }
      });
    });
  }

  // =========================================================================
  // 7. AJAX WISHLIST TOGGLE WITH TOAST NOTIFICATION
  // =========================================================================
  const wishlistButtons = document.querySelectorAll('.wishlist-toggle-btn');
  wishlistButtons.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const productId = this.getAttribute('data-product-id');
      if (!productId) return;

      const url = `/cart/wishlist/toggle/${productId}/`;
      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
      .then(res => {
        if (res.status === 401) {
          window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
          return;
        }
        return res.json();
      })
      .then(data => {
        if (!data) return;
        if (data.status === 'success') {
          if (data.action === 'added') {
            this.classList.add('active');
            this.innerHTML = '<i class="bi bi-heart-fill text-danger"></i>';
          } else {
            this.classList.remove('active');
            this.innerHTML = '<i class="bi bi-heart"></i>';
          }

          const navWishlistBadge = document.getElementById('navWishlistCount');
          if (navWishlistBadge) {
            navWishlistBadge.textContent = data.wishlist_count;
            navWishlistBadge.style.display = data.wishlist_count > 0 ? 'flex' : 'none';
          }

          window.showToast(data.message, data.action === 'added' ? 'gold' : 'info');
        }
      })
      .catch(err => console.error('Wishlist error:', err));
    });
  });

  // =========================================================================
  // 8. INDIAN PIN CODE DELIVERY CHECKER
  // =========================================================================
  const pincodeBtn = document.getElementById('checkPincodeBtn');
  const pincodeInput = document.getElementById('pincodeInput');
  const pincodeResult = document.getElementById('pincodeResult');

  if (pincodeBtn && pincodeInput && pincodeResult) {
    pincodeBtn.addEventListener('click', function () {
      const pin = pincodeInput.value.trim();
      if (pin.length !== 6 || isNaN(pin)) {
        pincodeResult.innerHTML = '<span class="text-danger small"><i class="bi bi-exclamation-circle me-1"></i> Please enter a valid 6-digit Indian PIN code.</span>';
        return;
      }

      pincodeResult.innerHTML = '<span class="text-warning small"><i class="spinner-border spinner-border-sm me-1"></i> Verifying armored courier serviceability...</span>';

      setTimeout(() => {
        const firstTwo = pin.substring(0, 2);
        let city = 'Metro Region';
        let time = '2-3 Business Days';

        if (['40', '41', '42'].includes(firstTwo)) {
          city = 'Mumbai & Western Maharashtra';
          time = 'Next-Day Express (24 Hours)';
        } else if (['11', '12', '20'].includes(firstTwo)) {
          city = 'Delhi NCR & Northern Hub';
          time = 'Next-Day Express (24 Hours)';
        } else if (['56', '57', '58'].includes(firstTwo)) {
          city = 'Bengaluru & Karnataka';
          time = '1-2 Business Days';
        } else if (['50', '51', '52', '53'].includes(firstTwo)) {
          city = 'Hyderabad & Telangana';
          time = '1-2 Business Days';
        } else if (['30', '31', '32', '33', '34'].includes(firstTwo)) {
          city = 'Jaipur & Rajasthan';
          time = '1-2 Business Days';
        } else if (['60', '61', '62', '63', '64'].includes(firstTwo)) {
          city = 'Chennai & Tamil Nadu';
          time = '2 Business Days';
        } else if (['70', '71', '72'].includes(firstTwo)) {
          city = 'Kolkata & Eastern Hub';
          time = '2 Business Days';
        }

        pincodeResult.innerHTML = `
          <div class="p-2 mt-2 rounded bg-dark border border-warning">
            <div class="text-warning fw-semibold small"><i class="bi bi-shield-check me-1"></i> 100% Insured Delivery Serviceable to ${city} (${pin})</div>
            <div class="text-muted small mt-1">Estimated Dispatch: <strong class="text-white">${time}</strong> via High-Value Armored Express.</div>
          </div>
        `;
      }, 350);
    });
  }

  // =========================================================================
  // 9. RECENTLY VIEWED PRODUCTS TRACKER
  // =========================================================================
  const productDetailAnchor = document.getElementById('product-detail-marker');
  if (productDetailAnchor) {
    const pData = {
      id: productDetailAnchor.dataset.id,
      name: productDetailAnchor.dataset.name,
      price: productDetailAnchor.dataset.price,
      image: productDetailAnchor.dataset.image,
      url: window.location.pathname,
      category: productDetailAnchor.dataset.category,
    };

    let viewed = [];
    try {
      viewed = JSON.parse(localStorage.getItem('aether_viewed_products')) || [];
    } catch (e) { viewed = []; }

    viewed = viewed.filter(item => item.id !== pData.id);
    viewed.unshift(pData);
    if (viewed.length > 6) viewed = viewed.slice(0, 6);
    localStorage.setItem('aether_viewed_products', JSON.stringify(viewed));
  }

  // Render recently viewed products if container exists
  const recentlyViewedContainer = document.getElementById('recentlyViewedGrid');
  if (recentlyViewedContainer) {
    let viewed = [];
    try {
      viewed = JSON.parse(localStorage.getItem('aether_viewed_products')) || [];
    } catch (e) { viewed = []; }

    if (viewed.length > 0) {
      document.getElementById('recentlyViewedSection')?.classList.remove('d-none');
      recentlyViewedContainer.innerHTML = viewed.map(p => `
        <div class="col-lg-3 col-md-4 col-6">
          <div class="product-card">
            <div class="product-img-wrapper">
              <a href="${p.url}">
                <img src="${p.image}" alt="${p.name}" class="product-img" onerror="this.src='https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=800&q=80';">
              </a>
            </div>
            <div class="product-body">
              <div class="product-cat">${p.category || 'High Jewellery'}</div>
              <h4 class="product-title"><a href="${p.url}">${p.name}</a></h4>
              <div class="product-price">${p.price}</div>
            </div>
          </div>
        </div>
      `).join('');
    }
  }

  // CSRF Token Helper
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
});
