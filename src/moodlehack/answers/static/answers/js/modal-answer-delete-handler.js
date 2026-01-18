/**
 * Handle answer deletion via REST API.
 * Manages modal state, API calls, and triggers notifications for both success and error.
 */
document.addEventListener('DOMContentLoaded', () => {
  const deleteModalEl = document.getElementById('deleteAnswerModal');
  const confirmBtn = deleteModalEl?.querySelector('#modal-confirm-action');
  let targetId = null;
  let targetCard = null;

  if (deleteModalEl && confirmBtn) {
    const bsModal = new bootstrap.Modal(deleteModalEl);

    /**
     * Helper to get CSRF token from cookies.
     */
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

    /**
     * Set up context when modal opens.
     */
    deleteModalEl.addEventListener('show.bs.modal', (event) => {
      const trigger = event.relatedTarget;
      targetId = trigger.dataset.objectId;
      targetCard = document.getElementById(`answer-card-${targetId}`);
      
      const idDisplay = deleteModalEl.querySelector('#modal-object-id');
      if (idDisplay) idDisplay.textContent = targetId;
    });

    /**
     * Perform API request and handle UI response.
     */
    confirmBtn.addEventListener('click', async () => {
      if (!targetId) return;

      try {
        const response = await fetch(`/api/v1/answers/${targetId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
          }
        });

        // Close modal in any outcome to show the toast
        bsModal.hide();

        if (response.ok) {
          // Success: status 204 No Content
          if (targetCard) {
            targetCard.classList.add('remove-swapping');
            targetCard.addEventListener('transitionend', () => {
              targetCard.remove();
            }, { once: true });
          }

          if (typeof showDynamicToast === 'function') {
            showDynamicToast('Ответ успешно удален!', 'danger');
          }
        } else {
          // Server error (403, 404, 500)
          if (typeof showDynamicToast === 'function') {
            showDynamicToast(`Ошибка сервера: ${response.status}`, 'warning');
          }
        }
      } catch (error) {
        // Network error
        bsModal.hide();
        if (typeof showDynamicToast === 'function') {
          showDynamicToast('Сетевая ошибка или сервер недоступен', 'warning');
        }
        console.error('Request failed:', error);
      }
    });
  }
});
