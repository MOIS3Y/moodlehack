/**
 * Core notification controller.
 * Uses <template> as a blueprint and UI labels from the server for localization.
 */

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('toast-messages-container');
  if (!container) return;

  /**
   * 1. Process initial messages from Django context.
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
 * Creates and shows a toast.
 */
function showDynamicToast(message, type = 'success') {
  const template = document.getElementById('toast-template');
  const container = document.getElementById('toast-messages-container');
  if (!template || !container) return;

  const clone = template.content.cloneNode(true);
  const toastEl = clone.querySelector('.toast');
  
  toastEl.querySelector('.toast-body').textContent = message;
  
  // Get translated labels from container's data-attribute
  const labels = JSON.parse(container.dataset.labels || '{}');
  
  updateToastUI(toastEl, type, labels);
  
  container.appendChild(toastEl);
  initializeSingleToast(toastEl, labels);
}

/**
 * Updates icons and titles using translated labels.
 */
function updateToastUI(el, type, labels) {
  const icon = el.querySelector('.toast-icon');
  const title = el.querySelector('.toast-title');
  
  icon.className = 'bi toast-icon me-2';
  
  if (type.includes('danger') || type.includes('error')) {
    icon.classList.add('bi-trash3-fill', 'text-danger');
    title.textContent = labels.title_danger || 'Deletion';
  } else if (type.includes('warning')) {
    icon.classList.add('bi-exclamation-triangle-fill', 'text-warning');
    title.textContent = labels.title_warning || 'Warning';
  } else if (type.includes('success')) {
    icon.classList.add('bi-check-circle-fill', 'text-success');
    title.textContent = labels.title_success || 'Success';
  } else {
    icon.classList.add('bi-info-circle-fill', 'text-primary');
    title.textContent = labels.title_info || 'Notification';
  }
}

/**
 * Handles toast lifecycle: animations, hover, and relative time.
 */
function initializeSingleToast(element, labels) {
  const timeEl = element.querySelector('.toast-time');
  const startTime = new Date();
  let hideTimeout = null;
  let interval = null;

  const toast = new bootstrap.Toast(element, { autohide: false });

  const startHideTimer = () => {
    hideTimeout = setTimeout(() => {
      element.style.animation = 'slideOut 0.5s ease-in forwards';
      element.addEventListener('animationend', () => toast.hide(), { once: true });
    }, 5000);
  };

  const getRelativeTime = (start) => {
    const seconds = Math.floor((new Date() - start) / 1000);
    if (seconds < 60) return `${seconds} ${labels.time_sec || 'sec. ago'}`;
    return `${Math.floor(seconds / 60)} ${labels.time_min || 'min. ago'}`;
  };

  if (timeEl) {
    timeEl.textContent = labels.time_just_now || 'just now';
    interval = setInterval(() => {
      timeEl.textContent = getRelativeTime(startTime);
    }, 1000);
  }

  element.onmouseenter = () => {
    clearTimeout(hideTimeout);
    element.style.animation = 'none';
  };

  element.onmouseleave = () => {
    if (element.classList.contains('show')) startHideTimer();
  };

  element.addEventListener('hidden.bs.toast', () => {
    clearInterval(interval);
    element.remove();
  });

  toast.show();
  startHideTimer();
}
