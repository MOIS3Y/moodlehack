/**
 * Copies answer text to clipboard.
 */
document.addEventListener('click', function (event) {
  const btn = event.target.closest('.copy-btn');
  if (!btn) return;

  const targetId = btn.getAttribute('data-copy-target');
  const textElement = document.getElementById(targetId);

  if (textElement) {
    const textToCopy = textElement.innerText;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
      const icon = btn.querySelector('i');
      const originalClass = icon.className;

      icon.className = 'bi bi-check2';

      setTimeout(() => {
        icon.className = originalClass;
      }, 2000);
    });
  }
});
