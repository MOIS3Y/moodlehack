/**
 * Cycle color mode toggler using Bootstrap Icons (bi-*)
 * Light -> Dark -> Auto
 */
(() => {
  'use strict'

  const THEMES = ['light', 'dark', 'auto']
  // Map themes to Bootstrap Icon classes
  const ICONS = {
    light: 'bi-sun-fill',
    dark: 'bi-moon-stars-fill',
    auto: 'bi-circle-half'
  }

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)
  const getPreferredTheme = () => getStoredTheme() || 'auto'

  const setTheme = theme => {
    const isDark = theme === 'auto' 
      ? window.matchMedia('(prefers-color-scheme: dark)').matches 
      : theme === 'dark'
    document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light')
  }

  const updateUI = (theme) => {
    const btn = document.querySelector('#bd-theme')
    if (!btn) return

    const iconEl = btn.querySelector('.theme-icon-active')
    if (iconEl) {
      // Remove all possible theme classes and add the current one
      iconEl.classList.remove('bi-sun-fill', 'bi-moon-stars-fill', 'bi-circle-half')
      iconEl.classList.add(ICONS[theme])
    }
    btn.setAttribute('aria-label', `Theme: ${theme}`)
  }

  // Initial execution
  const currentTheme = getPreferredTheme()
  setTheme(currentTheme)

  window.addEventListener('DOMContentLoaded', () => {
    updateUI(currentTheme)

    document.addEventListener('click', (e) => {
      const btn = e.target.closest('#bd-theme')
      if (!btn) return

      const now = getPreferredTheme()
      const nextTheme = THEMES[(THEMES.indexOf(now) + 1) % THEMES.length]

      setStoredTheme(nextTheme)
      setTheme(nextTheme)
      updateUI(nextTheme)
    })
  })

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (getPreferredTheme() === 'auto') setTheme('auto')
  })
})()
