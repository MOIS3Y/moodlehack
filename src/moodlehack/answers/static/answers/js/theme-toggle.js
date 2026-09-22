/**
 * Cycle color mode toggler using Tabler Icons
 * Light -> Dark -> Auto
 */
(() => {
  'use strict';

  const THEMES = ['light', 'dark', 'auto'];
  const ICONS = {
    light: 'sun',
    dark: 'moon',
    auto: 'circle-half-2',
  };

  const getStoredTheme = () => localStorage.getItem('theme') || 'auto';
  const setStoredTheme = (theme) => localStorage.setItem('theme', theme);

  const updateUI = (theme) => {
    const btn = document.querySelector('#bd-theme');
    if (!btn) return;
    const iconEl = btn.querySelector('.theme-icon-active use');
    if (iconEl) {
      iconEl.setAttribute('href', `#icon-${ICONS[theme]}`);
    }
  };

  window.addEventListener('DOMContentLoaded', () => {
    const currentTheme = getStoredTheme();
    updateUI(currentTheme);

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('#bd-theme');
      if (!btn) return;

      const now = getStoredTheme();
      const nextTheme = THEMES[(THEMES.indexOf(now) + 1) % THEMES.length];

      setStoredTheme(nextTheme);
      // Call global setTheme or just update attribute:
      const isDark =
        nextTheme === 'auto'
          ? window.matchMedia('(prefers-color-scheme: dark)').matches
          : nextTheme === 'dark';
      document.documentElement.setAttribute(
        'data-bs-theme',
        isDark ? 'dark' : 'light',
      );

      updateUI(nextTheme);
    });
  });
})();
