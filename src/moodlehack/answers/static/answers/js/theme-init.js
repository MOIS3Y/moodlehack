// Set theme immediately to prevent screen flickering
(function () {
  'use strict'
  const getStoredTheme = () => localStorage.getItem('theme') || 'auto'
  
  const setTheme = theme => {
    if (theme === 'auto') {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light')
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  setTheme(getStoredTheme())
})()
