/**
 * Handle answer deletion via REST API with localization support.
 */
document.addEventListener('DOMContentLoaded', () => {
  const deleteModalEl = document.getElementById('deleteAnswerModal');
  const confirmBtn = deleteModalEl?.querySelector('#modal-confirm-action');
  let targetId = null;
  let targetCard = null;

  if (deleteModalEl && confirmBtn) {
    const bsModal = new bootstrap.Modal(deleteModalEl);

    const getCookie = (name) => {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };

    deleteModalEl.addEventListener('show.bs.modal', (event) => {
      const trigger = event.relatedTarget;
      targetId = trigger.dataset.objectId;
      targetCard = document.getElementById(`answer-card-${targetId}`);
      
      const idDisplay = deleteModalEl.querySelector('#modal-object-id');
      if (idDisplay) idDisplay.textContent = targetId;
    });

    confirmBtn.addEventListener('click', async () => {
      if (!targetId) return;

      // Localization labels from data attributes
      const msgSuccess = deleteModalEl.dataset.msgSuccess;
      const msgErrorPrefix = deleteModalEl.dataset.msgErrorPrefix;
      const msgNetworkError = deleteModalEl.dataset.msgNetworkError;

      try {
        const response = await fetch(`/api/v1/answers/${targetId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
          }
        });

        bsModal.hide();

        if (response.ok) {
          if (targetCard) {
            targetCard.classList.add('remove-swapping');
            targetCard.addEventListener('transitionend', () => {
              targetCard.remove();
            }, { once: true });
          }

          if (typeof showDynamicToast === 'function') {
            showDynamicToast(msgSuccess, 'danger');
          }
        } else {
          if (typeof showDynamicToast === 'function') {
            showDynamicToast(`${msgErrorPrefix}: ${response.status}`, 'warning');
          }
        }
      } catch (error) {
        bsModal.hide();
        if (typeof showDynamicToast === 'function') {
          showDynamicToast(msgNetworkError, 'warning');
        }
        console.error('Request failed:', error);
      }
    });
  }
});
