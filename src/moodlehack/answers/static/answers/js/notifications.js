/**
 * Core notification controller.
 * Uses a template and translated UI labels supplied by the server.
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
      messages.forEach((m) => showDynamicToast(m.text, m.tags));
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

  icon.setAttribute('class', 'icon toast-icon me-2');
  const glyph = icon.querySelector('use');

  if (type.includes('danger') || type.includes('error')) {
    icon.classList.add('text-danger');
    glyph.setAttribute('href', '#icon-trash');
    title.textContent = labels.title_danger || 'Deletion';
  } else if (type.includes('warning')) {
    icon.classList.add('text-warning');
    glyph.setAttribute('href', '#icon-alert-triangle');
    title.textContent = labels.title_warning || 'Warning';
  } else if (type.includes('success')) {
    icon.classList.add('text-success');
    glyph.setAttribute('href', '#icon-circle-check');
    title.textContent = labels.title_success || 'Success';
  } else {
    icon.classList.add('text-primary');
    glyph.setAttribute('href', '#icon-info-circle');
    title.textContent = labels.title_info || 'Notification';
  }
}

/**
 * Handles toast lifecycle, hover, and relative time.
 */
function initializeSingleToast(element, labels) {
  const timeEl = element.querySelector('.toast-time');
  const startTime = new Date();
  let hideTimeout = null;
  let interval = null;

  const toast = new tabler.Toast(element, { autohide: false });

  const startHideTimer = () => {
    hideTimeout = setTimeout(() => {
      toast.hide();
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
  };

  element.onmouseleave = () => {
    if (element.classList.contains('show')) startHideTimer();
  };

  element.addEventListener('hidden.bs.toast', () => {
    clearTimeout(hideTimeout);
    clearInterval(interval);
    toast.dispose();
    element.remove();
  });

  toast.show();
  startHideTimer();
}
