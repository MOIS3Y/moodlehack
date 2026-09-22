/** Manage Tabler tooltips without taking over modal or dropdown toggles. */
function tooltipTriggers(root) {
  if (!(root instanceof Element || root instanceof Document)) return [];
  const triggers = [...root.querySelectorAll('[data-ui-tooltip]')];
  if (root.matches?.('[data-ui-tooltip]')) triggers.unshift(root);
  return triggers;
}

function initTooltips(root) {
  for (const trigger of tooltipTriggers(root)) {
    tabler.Tooltip.getOrCreateInstance(trigger, {
      container: 'body',
      html: false,
      placement: trigger.dataset.bsPlacement || 'top',
      trigger: 'hover',
      delay: 0,
    });
  }
}

function disposeTooltips(root) {
  for (const trigger of tooltipTriggers(root)) {
    tabler.Tooltip.getInstance(trigger)?.dispose();
  }
}

document.addEventListener('DOMContentLoaded', () => initTooltips(document));
document.addEventListener('htmx:afterSwap', (event) => {
  initTooltips(event.detail.target);
});
document.addEventListener('htmx:beforeCleanupElement', (event) => {
  disposeTooltips(event.detail.elt);
});

// Mouse focus must not keep a tooltip open after the pointer leaves.
// Keyboard focus still exposes the same native Tabler tooltip.
document.addEventListener('focusin', (event) => {
  const trigger = event.target.closest('[data-ui-tooltip]');
  if (trigger && event.target.matches(':focus-visible')) {
    tabler.Tooltip.getInstance(trigger)?.show();
  }
});

document.addEventListener('focusout', (event) => {
  const trigger = event.target.closest('[data-ui-tooltip]');
  if (trigger) tabler.Tooltip.getInstance(trigger)?.hide();
});

function hideTooltips() {
  for (const trigger of tooltipTriggers(document)) {
    tabler.Tooltip.getInstance(trigger)?.hide();
  }
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') hideTooltips();
});
window.addEventListener('blur', hideTooltips);

document.addEventListener('show.bs.tooltip', (event) => {
  if (event.target.querySelector('[aria-expanded="true"]')) {
    event.preventDefault();
  }
});

// Hide before a click disables its trigger or opens a modal.
document.addEventListener(
  'click',
  (event) => {
    const trigger = event.target.closest('[data-ui-tooltip]');
    if (trigger) tabler.Tooltip.getInstance(trigger)?.hide();
  },
  true,
);
