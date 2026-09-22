/** Preserve layout choice across navigation and HTMX replacements. */
function applyAnswerView(view) {
  const grid = view === 'grid';
  const container = document.getElementById('answers-container');
  if (container) {
    container.classList.toggle('grid-mode', grid);
    container.classList.toggle('list-mode', !grid);
    container.classList.toggle('row-cols-md-2', grid);
    container.classList.toggle('row-cols-xl-3', grid);
  }

  for (const mode of ['list', 'grid']) {
    const button = document.getElementById(mode + '-view-btn');
    button?.classList.toggle('active', mode === view);
    button?.setAttribute('aria-pressed', String(mode === view));
  }
}

function restoreAnswerView() {
  const grid = document.cookie
    .split(';')
    .some((cookie) => cookie.trim() === 'answers_view=grid');
  applyAnswerView(grid ? 'grid' : 'list');
}

document.addEventListener('click', (event) => {
  const button = event.target.closest('#list-view-btn, #grid-view-btn');
  if (!button) return;
  const view = button.id === 'grid-view-btn' ? 'grid' : 'list';
  document.cookie =
    'answers_view=' + view + '; path=/; max-age=2592000; SameSite=Lax';
  applyAnswerView(view);
});

document.addEventListener('DOMContentLoaded', restoreAnswerView);
document.addEventListener('htmx:afterSwap', restoreAnswerView);
