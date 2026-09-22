/** Keep Tabler validation styles and accessibility in sync with HTMX. */
function updateQuestionValidation(event, invalid) {
  const field = document.getElementsByName(event.detail.value)[0];
  if (!field) return;
  field.classList.toggle('is-invalid', invalid);
  field.classList.toggle('is-valid', !invalid);
  field.setAttribute('aria-invalid', String(invalid));
}

document.body.addEventListener('fieldInvalid', (event) => {
  updateQuestionValidation(event, true);
});

document.body.addEventListener('fieldValid', (event) => {
  updateQuestionValidation(event, false);
});

document.getElementById('id_question')?.addEventListener('input', (event) => {
  const field = event.target;
  field.classList.remove('is-invalid', 'is-valid');
  field.removeAttribute('aria-invalid');
  document.getElementById('id_question_error').replaceChildren();
});
