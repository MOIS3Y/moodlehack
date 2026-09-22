/** Focus the first server-side error without changing validation rules. */
document.addEventListener('DOMContentLoaded', () => {
  const invalid = document.querySelector('form .is-invalid');
  if (!invalid) return;
  const editor = invalid.parentElement.querySelector('.EasyMDEContainer');
  const focusTarget =
    editor?.querySelector(
      '.CodeMirror textarea, .CodeMirror [contenteditable="true"]',
    ) || invalid;
  focusTarget.focus();
  focusTarget.scrollIntoView({ block: 'center' });
});
