// OCR Tool JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('ocrForm');
    const pdfFileInput = document.getElementById('pdf_file');
    const processingState = document.getElementById('processingState');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        if (!pdfFileInput.files || pdfFileInput.files.length === 0) {
            showError('Please select a PDF file to process.');
            return;
        }

        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Processing...';
        submitButton.disabled = true;
        processingState.style.display = 'block';

        fetch('/ocr_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            return response.json().then(data => {
                throw new Error(data.message || 'Error running OCR');
            });
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const outputField = document.getElementById('output_filename');
            const fallbackName = pdfFileInput.files[0].name.replace('.pdf', '_ocr.pdf');
            a.download = outputField.value.trim() || fallbackName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            processingState.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            processingState.style.display = 'none';
            showError(error.message || 'Failed to process PDF.');
        });
    });
});

function showError(message) {
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorModal.style.display = 'block';
}

function closeErrorModal() {
    const errorModal = document.getElementById('errorModal');
    errorModal.style.display = 'none';
}
