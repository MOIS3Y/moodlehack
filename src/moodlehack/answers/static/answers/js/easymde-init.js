document.addEventListener('DOMContentLoaded', () => {
  const field = document.getElementById('id_answer');
  if (!field) return;

  const editor = new EasyMDE({
    element: field,
    autoDownloadFontAwesome: false,
    spellChecker: false,
    forceSync: true,
    minHeight: '250px',
    status: false,
    toolbar: [
      'bold',
      'italic',
      '|',
      'unordered-list',
      'ordered-list',
      '|',
      'link',
      '|',
      'preview',
      'side-by-side',
      'fullscreen',
    ],
    placeholder: field.placeholder,
    renderingConfig: { singleLineBreaks: false },
  });

  const icons = {
    bold: 'bold',
    italic: 'italic',
    'unordered-list': 'list',
    'ordered-list': 'list-numbers',
    link: 'link',
    preview: 'eye',
    'side-by-side': 'layout-sidebar-right',
    fullscreen: 'arrows-maximize',
  };
  for (const [name, glyph] of Object.entries(icons)) {
    const icon = editor.toolbarElements[name]?.querySelector('i');
    if (icon) {
      const svg = document
        .querySelector('#editor-icon-template')
        .content.firstElementChild.cloneNode(true);
      svg.querySelector('use').setAttribute('href', `#icon-${glyph}`);
      icon.replaceWith(svg);
    }
  }

  const container = editor.codemirror.getWrapperElement().parentElement;
  const input = editor.codemirror.getInputField();
  input.setAttribute('aria-labelledby', 'id_answer_label');
  const description = field.getAttribute('aria-describedby');
  if (description) input.setAttribute('aria-describedby', description);
  if (field.required) input.setAttribute('aria-required', 'true');

  const syncValidation = () => {
    const invalid = field.classList.contains('is-invalid');
    container.classList.toggle('is-invalid', invalid);
    input.setAttribute('aria-invalid', String(invalid));
  };
  syncValidation();
  editor.codemirror.on('change', () => {
    field.dispatchEvent(new Event('input'));
    syncValidation();
  });

  if (document.querySelector('form .is-invalid') === field) {
    editor.codemirror.focus();
  }
});
