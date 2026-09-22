/** Copy the whole rendered answer, not just its visible scroll area. */
document.addEventListener('click', async (event) => {
  const button = event.target.closest('.copy-btn');
  if (!button || button.disabled) return;
  const content = document.getElementById(button.dataset.copyTarget);
  if (!content) return;

  const icon = button.querySelector('use');
  const originalHref = icon.getAttribute('href');
  button.disabled = true;
  try {
    await navigator.clipboard.writeText(content.innerText);
    icon.setAttribute('href', '#icon-check');
  } catch {
    icon.setAttribute('href', '#icon-alert-circle');
    showDynamicToast(button.dataset.copyError, 'warning');
  } finally {
    setTimeout(() => {
      icon.setAttribute('href', originalHref);
      button.disabled = false;
    }, 2000);
  }
});
