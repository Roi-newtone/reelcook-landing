// Reelcook landing — interactions

// ============ Mobile nav toggle ============
const toggle = document.querySelector('.mobile-toggle');
const links = document.querySelector('.nav-links');
if (toggle) {
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    if (links) {
      if (expanded) {
        links.removeAttribute('style');
      } else {
        links.style.display = 'flex';
        links.style.flexDirection = 'column';
        links.style.position = 'absolute';
        links.style.top = '70px';
        links.style.right = '24px';
        links.style.background = '#fff';
        links.style.padding = '20px';
        links.style.borderRadius = '16px';
        links.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
        links.style.border = '1px solid #ECEAE3';
      }
    }
  });
}

// ============ FAQ accordion (one open at a time) ============
document.querySelectorAll('.faq-item').forEach((item) => {
  item.addEventListener('toggle', () => {
    if (item.open) {
      document.querySelectorAll('.faq-item').forEach((other) => {
        if (other !== item) other.open = false;
      });
    }
  });
});

// ============ Lightbox: open on card click, close on backdrop/X/Esc/swipe-down ============
const lightbox = document.getElementById('lightbox');
const lightboxVideo = lightbox ? lightbox.querySelector('.lightbox-video') : null;
const lightboxSource = lightboxVideo ? lightboxVideo.querySelector('source') : null;

function openLightbox(src) {
  if (!lightbox || !lightboxVideo || !lightboxSource) return;
  lightboxSource.src = src;
  lightboxVideo.load();
  lightbox.setAttribute('aria-hidden', 'false');
  lightbox.classList.add('is-open');
  lightboxVideo.play().catch(() => {});
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  if (!lightbox || !lightboxVideo) return;
  lightbox.classList.remove('is-open');
  lightbox.setAttribute('aria-hidden', 'true');
  lightboxVideo.pause();
  // Clear src after closing animation finishes to free memory
  setTimeout(() => {
    if (!lightbox.classList.contains('is-open') && lightboxSource) {
      lightboxSource.src = '';
      lightboxVideo.load();
    }
  }, 320);
  document.body.style.overflow = '';
}

document.querySelectorAll('.ft-card').forEach((card) => {
  card.addEventListener('click', (e) => {
    e.preventDefault();
    const src = card.dataset.video;
    if (src) openLightbox(src);
  });
});

if (lightbox) {
  lightbox
    .querySelectorAll('[data-lightbox-close]')
    .forEach((el) => el.addEventListener('click', closeLightbox));

  // Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('is-open')) {
      closeLightbox();
    }
  });

  // Swipe down to close (mobile)
  let touchStartY = 0;
  lightbox.addEventListener(
    'touchstart',
    (e) => {
      touchStartY = e.touches[0].clientY;
    },
    { passive: true }
  );
  lightbox.addEventListener(
    'touchend',
    (e) => {
      const deltaY = e.changedTouches[0].clientY - touchStartY;
      if (deltaY > 80) closeLightbox();
    },
    { passive: true }
  );
}

// ============ Scroll-in reveal ============
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);

document
  .querySelectorAll('.step-card, .ft-card, .faq-item, .float-card, .btn-social')
  .forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'opacity .55s ease, transform .55s ease';
    revealObserver.observe(el);
  });
