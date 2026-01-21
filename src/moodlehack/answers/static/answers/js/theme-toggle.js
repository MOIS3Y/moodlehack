/**
 * Cycle color mode toggler using Bootstrap Icons (bi-*)
 * Light -> Dark -> Auto
 */
(() => {
  'use strict'

  const THEMES = ['light', 'dark', 'auto']
  const ICONS = {
    light: 'bi-sun-fill',
    dark: 'bi-moon-stars-fill',
    auto: 'bi-circle-half'
  }

  const getStoredTheme = () => localStorage.getItem('theme') || 'auto'
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const updateUI = (theme) => {
    const btn = document.querySelector('#bd-theme')
    if (!btn) return
    const iconEl = btn.querySelector('.theme-icon-active')
    if (iconEl) {
      iconEl.classList.remove('bi-sun-fill', 'bi-moon-stars-fill', 'bi-circle-half')
      iconEl.classList.add(ICONS[theme])
    }
  }

  window.addEventListener('DOMContentLoaded', () => {
    const currentTheme = getStoredTheme()
    updateUI(currentTheme)

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('#bd-theme')
      if (!btn) return

      const now = getStoredTheme()
      const nextTheme = THEMES[(THEMES.indexOf(now) + 1) % THEMES.length]

      setStoredTheme(nextTheme)
      // Call global setTheme or just update attribute:
      const isDark = nextTheme === 'auto' 
        ? window.matchMedia('(prefers-color-scheme: dark)').matches 
        : nextTheme === 'dark'
      document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light')
      
      updateUI(nextTheme)
    })
  })
})()
