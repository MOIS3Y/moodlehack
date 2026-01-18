/**
 * Core notification controller.
 * Uses <template> as a blueprint for both server-side and client-side notifications.
 */

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('toast-messages-container');
  if (!container) return;

  /**
   * 1. Process initial messages from Django context.
   * Messages are passed via data-initial attribute as a JSON string.
   */
  const rawData = container.dataset.initial;
  if (rawData) {
    try {
      const messages = JSON.parse(rawData);
      messages.forEach(m => showDynamicToast(m.text, m.tags));
    } catch (e) {
      console.error('Failed to parse initial messages:', e);
    }
  }
});

/**
 * Creates and shows a toast from the <template> element.
 * @param {string} message - Notification text.
 * @param {string} type - Message type (success, danger, warning, etc.).
 */
function showDynamicToast(message, type = 'success') {
  const template = document.getElementById('toast-template');
  const container = document.getElementById('toast-messages-container');
  if (!template || !container) return;

  // Clone the structure from <template>
  const clone = template.content.cloneNode(true);
  const toastEl = clone.querySelector('.toast');
  
  // Fill text content
  toastEl.querySelector('.toast-body').textContent = message;
  
  // Update icons and titles based on the tag
  updateToastUI(toastEl, type);
  
  container.appendChild(toastEl);
  initializeSingleToast(toastEl);
}

/**
 * Common UI updater for icons and titles.
 * Synchronizes Django message tags with JS dynamic calls.
 */
function updateToastUI(el, type) {
  const icon = el.querySelector('.toast-icon');
  const title = el.querySelector('.toast-title');
  
  icon.className = 'bi toast-icon me-2'; // Reset
  
  if (type.includes('danger') || type.includes('error')) {
    // Red theme: for deletions and server errors
    icon.classList.add('bi-trash3-fill', 'text-danger');
    title.textContent = 'Удаление'; 
  } else if (type.includes('warning')) {
    // Yellow theme: for warnings
    icon.classList.add('bi-exclamation-triangle-fill', 'text-warning');
    title.textContent = 'Внимание';
  } else if (type.includes('success')) {
    // Green theme: for creations and updates
    icon.classList.add('bi-check-circle-fill', 'text-success');
    title.textContent = 'Успешно';
  } else {
    // Blue theme: for general info
    icon.classList.add('bi-info-circle-fill', 'text-primary');
    title.textContent = 'Уведомление';
  }
}

/**
 * Unified initialization for Bootstrap, Timers, and Cleanup.
 * @param {HTMLElement} element - The toast DOM element.
 */
function initializeSingleToast(element) {
  if (typeof bootstrap === 'undefined') return;

  const timeEl = element.querySelector('.toast-time');
  const startTime = new Date();
  let hideTimeout = null;
  let interval = null;

  const toast = new bootstrap.Toast(element, { autohide: false });

  /**
   * Triggers the CSS exit animation and then hides the toast.
   */
  const startHideTimer = () => {
    hideTimeout = setTimeout(() => {
      element.style.animation = 'slideOut 0.5s ease-in forwards';
      element.addEventListener('animationend', () => toast.hide(), { once: true });
    }, 5000);
  };

  /**
   * Helper to calculate relative time (seconds/minutes).
   */
  const getRelativeTime = (start) => {
    const seconds = Math.floor((new Date() - start) / 1000);
    if (seconds < 60) return `${seconds} сек. назад`;
    return `${Math.floor(seconds / 60)} мин. назад`;
  };

  // Live time counter update every second
  if (timeEl) {
    timeEl.textContent = 'только что';
    interval = setInterval(() => {
      timeEl.textContent = getRelativeTime(startTime);
    }, 1000);
  }

  // Hover logic: Pause the timer and reset animation
  element.onmouseenter = () => {
    clearTimeout(hideTimeout);
    element.style.animation = 'none';
  };

  // Resume on mouse leave
  element.onmouseleave = () => {
    if (element.classList.contains('show')) startHideTimer();
  };

  /**
   * Cleanup on hide: clear intervals and remove the element from DOM.
   */
  element.addEventListener('hidden.bs.toast', () => {
    if (interval) clearInterval(interval);
    if (hideTimeout) clearTimeout(hideTimeout);
    element.remove(); 
  }, { once: true });

  toast.show();
  startHideTimer();
}
