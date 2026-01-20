/**
 * HTMX Event listeners for Bootstrap validation classes
 */
document.body.addEventListener('fieldInvalid', function(evt) {
  const el = document.getElementsByName(evt.detail.value)[0];
  if (el) {
    el.classList.add('is-invalid');
    el.classList.remove('is-valid');
  }
});

document.body.addEventListener('fieldValid', function(evt) {
  const el = document.getElementsByName(evt.detail.value)[0];
  if (el) {
    el.classList.remove('is-invalid');
    el.classList.add('is-valid');
  }
});
