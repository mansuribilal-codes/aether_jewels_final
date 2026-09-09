/**
 * AETHER JEWELS – Dynamic Celestial Starfield & Nebula Canvas
 * Creates a high-performance background canvas simulating interstellar stars, twinkling gold pulsars, and cosmic stardust.
 */

(function () {
  let canvas, ctx;
  let stars = [];
  let mouseX = 0, mouseY = 0;
  let targetX = 0, targetY = 0;
  let width = window.innerWidth;
  let height = window.innerHeight;

  const STAR_COUNT = Math.min(120, Math.floor((width * height) / 12000));
  const GOLD_STARS_RATIO = 0.25;

  class Star {
    constructor() {
      this.reset(true);
    }

    reset(initial = false) {
      this.x = Math.random() * width;
      this.y = initial ? Math.random() * height : -10;
      this.z = Math.random() * 2 + 0.5; // depth
      this.radius = Math.random() * 1.5 + 0.5;
      this.baseAlpha = Math.random() * 0.7 + 0.2;
      this.alpha = this.baseAlpha;
      this.twinkleSpeed = Math.random() * 0.03 + 0.01;
      this.twinklePhase = Math.random() * Math.PI * 2;
      this.speedY = (Math.random() * 0.2 + 0.05) * this.z;
      this.isGold = Math.random() < GOLD_STARS_RATIO;
    }

    update() {
      this.y += this.speedY;
      if (this.y > height + 10) {
        this.reset();
      }

      this.twinklePhase += this.twinkleSpeed;
      this.alpha = this.baseAlpha + Math.sin(this.twinklePhase) * 0.25;
      if (this.alpha < 0.1) this.alpha = 0.1;
      if (this.alpha > 1) this.alpha = 1;
    }

    draw(ctx, parallaxX, parallaxY) {
      const px = this.x + parallaxX * this.z * 15;
      const py = this.y + parallaxY * this.z * 15;

      ctx.save();
      ctx.globalAlpha = this.alpha;
      ctx.beginPath();
      ctx.arc(px, py, this.radius, 0, Math.PI * 2);

      if (this.isGold) {
        ctx.fillStyle = '#D4AF37';
        ctx.shadowColor = '#F4E5B8';
        ctx.shadowBlur = 6;
      } else {
        ctx.fillStyle = '#FFFFFF';
        ctx.shadowColor = '#BEE3F8';
        ctx.shadowBlur = 3;
      }

      ctx.fill();
      ctx.restore();
    }
  }

  function init() {
    canvas = document.getElementById('celestial-bg-canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.id = 'celestial-bg-canvas';
      document.body.prepend(canvas);
    }
    
    // Always enforce fixed background positioning
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    canvas.style.background = 'transparent';
    canvas.style.display = 'block';

    ctx = canvas.getContext('2d');
    resize();

    stars = [];
    for (let i = 0; i < STAR_COUNT; i++) {
      stars.push(new Star());
    }

    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', onMouseMove);

    render();
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    if (canvas) {
      canvas.width = width;
      canvas.height = height;
    }
  }

  function onMouseMove(e) {
    mouseX = (e.clientX / width) - 0.5;
    mouseY = (e.clientY / height) - 0.5;
  }

  function render() {
    if (!ctx) return;

    // Smooth lerp for parallax
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;

    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < stars.length; i++) {
      stars[i].update();
      stars[i].draw(ctx, targetX, targetY);
    }

    requestAnimationFrame(render);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
