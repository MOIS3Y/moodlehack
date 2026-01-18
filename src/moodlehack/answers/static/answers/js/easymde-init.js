document.addEventListener('DOMContentLoaded', function() {
    // Target only the answer field specifically
    const answerTextarea = document.getElementById('id_answer');
    
    if (answerTextarea) {
        const easyMDE = new EasyMDE({
            element: answerTextarea,
            spellChecker: false,
            forceSync: true,
            minHeight: "250px",
            status: false,
            toolbar: [
                "bold", "italic", "|", 
                "unordered-list", "ordered-list", "|", 
                "link", "|", 
                "preview", "side-by-side", "fullscreen"
            ],
            placeholder: "Type your answer here...",
            renderingConfig: {
                singleLineBreaks: false,
            },
        });

        const mdeContainer = answerTextarea.closest('.EasyMDEContainer');

        // Sync initial validation (for Django form errors)
        if (answerTextarea.classList.contains('is-invalid') && mdeContainer) {
            mdeContainer.classList.add('is-invalid');
        }

        // Handle changes and sync validation classes
        easyMDE.codemirror.on("change", () => {
            answerTextarea.value = easyMDE.value();
            // Trigger input event for HTMX or other listeners
            answerTextarea.dispatchEvent(new Event('input'));
            
            if (answerTextarea.classList.contains('is-invalid')) {
                mdeContainer.classList.add('is-invalid');
            } else if (mdeContainer) {
                mdeContainer.classList.remove('is-invalid');
            }
        });
    }
});
