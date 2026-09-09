/**
 * AETHER JEWELS – GSAP & ScrollTrigger Luxury Animations
 */

document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined') return;

  // Register ScrollTrigger plugin if available
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // 1. CUSTOM STARDUST CURSOR PHYSICS
  const cursorDot = document.querySelector('.custom-cursor-dot');
  const cursorRing = document.querySelector('.custom-cursor-ring');

  if (cursorDot && cursorRing && window.innerWidth > 992) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let ringX = mouseX;
    let ringY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      gsap.to(cursorDot, { x: mouseX, y: mouseY, duration: 0.05, ease: 'power2.out' });
    });

    // Smooth ring lerp
    gsap.ticker.add(() => {
      ringX += (mouseX - ringX) * 0.15;
      ringY += (mouseY - ringY) * 0.15;
      gsap.set(cursorRing, { x: ringX, y: ringY });
    });

    // Hover expansions on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .btn, .product-card, .product-card-3d, .config-option-card, input, select');
    interactiveElements.forEach((el) => {
      el.addEventListener('mouseenter', () => cursorRing.classList.add('active'));
      el.addEventListener('mouseleave', () => cursorRing.classList.remove('active'));
    });
  }

  // 2. HERO TIMELINE ANIMATION
  const heroSection = document.querySelector('.hero-section, .hero-luxury');
  if (heroSection) {
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    heroTl
      .from('.hero-badge', { opacity: 0, y: -20, duration: 0.8, delay: 0.1 })
      .from('.hero-title, .hero-headline', { opacity: 0, y: 35, duration: 1 }, '-=0.5')
      .from('.hero-tagline, .hero-subheading', { opacity: 0, y: 20, duration: 0.8 }, '-=0.6')
      .from('.hero-actions, .hero-cta-group', { opacity: 0, y: 20, duration: 0.7 }, '-=0.5');
  }

  // 3. PRODUCT CARDS STAGGERED REVEAL
  const productGrids = document.querySelectorAll('.product-grid, .row-cards-reveal');
  productGrids.forEach((grid) => {
    const cards = grid.querySelectorAll('.product-card, .product-card-3d, .card-3d-wrap');
    if (cards.length > 0 && typeof ScrollTrigger !== 'undefined') {
      gsap.from(cards, {
        opacity: 0,
        y: 35,
        stagger: 0.08,
        duration: 0.8,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: grid,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        }
      });
    }
  });

  // 4. SECTION HEADERS REVEAL
  const sectionHeaders = document.querySelectorAll('.section-header, .luxury-section-title');
  sectionHeaders.forEach((header) => {
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.from(header.children, {
        opacity: 0,
        y: 25,
        stagger: 0.12,
        duration: 0.9,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: header,
          start: 'top 88%',
          toggleActions: 'play none none reverse',
        }
      });
    }
  });

  // 5. MAGNETIC BUTTON EFFECT
  const magneticBtns = document.querySelectorAll('.magnetic-btn, .btn-gold');
  magneticBtns.forEach((btn) => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      gsap.to(btn, { x: x * 0.2, y: y * 0.2, duration: 0.3, ease: 'power2.out' });
    });

    btn.addEventListener('mouseleave', () => {
      gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' });
    });
  });
});
