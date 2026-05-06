// TrackIt — Main JS

// ─── Mobile Nav ───────────────────────────────────────────────────────────────
function toggleNav() {
  const menu = document.getElementById('mobileMenu');
  if (menu) menu.classList.toggle('open');
}

// Close mobile menu on outside click
document.addEventListener('click', (e) => {
  const menu = document.getElementById('mobileMenu');
  const toggle = document.querySelector('.nav-toggle');
  if (menu && menu.classList.contains('open') &&
      !menu.contains(e.target) && e.target !== toggle) {
    menu.classList.remove('open');
  }
});

// ─── Flash auto-dismiss ────────────────────────────────────────────────────────
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => {
    el.style.opacity = '0';
    el.style.transition = 'opacity .5s';
    setTimeout(() => el.remove(), 500);
  });
}, 4500);

// ─── Active nav link highlight ────────────────────────────────────────────────
document.querySelectorAll('.nav-link').forEach(link => {
  if (link.href === window.location.href) {
    link.style.color = 'var(--text)';
    link.style.background = 'var(--bg-3)';
  }
});

// ─── Confirm for destructive actions ─────────────────────────────────────────
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm(btn.dataset.confirm)) e.preventDefault();
  });
});

// ─── Status select submit flash ───────────────────────────────────────────────
document.querySelectorAll('.status-select').forEach(sel => {
  sel.addEventListener('change', () => {
    sel.style.borderColor = 'var(--accent)';
  });
});

// ─── Number animation for stat cards ─────────────────────────────────────────
function animateNumbers() {
  document.querySelectorAll('.stat-num, .as-num, .ds-num').forEach(el => {
    const target = parseInt(el.textContent);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 30);
    const interval = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(interval);
    }, 30);
  });
}

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
  animateNumbers();
});
