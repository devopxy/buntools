// Pagination & Page Size Tool JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('paginationForm');
    const pageSizeSelect = document.getElementById('page_size');
    const customSizeFields = document.getElementById('customSizeFields');
    const pdfFileInput = document.getElementById('pdf_file');
    const processingState = document.getElementById('processingState');

    pageSizeSelect.addEventListener('change', function() {
        if (this.value === 'CUSTOM') {
            customSizeFields.style.display = 'block';
        } else {
            customSizeFields.style.display = 'none';
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        if (!pdfFileInput.files || pdfFileInput.files.length === 0) {
            showError('Please select a PDF file to process.');
            return;
        }

        if (pageSizeSelect.value === 'CUSTOM') {
            const width = document.getElementById('custom_width_mm').value.trim();
            const height = document.getElementById('custom_height_mm').value.trim();
            if (!width || !height) {
                showError('Please enter both custom width and height in millimeters.');
                return;
            }
        }

        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Processing...';
        submitButton.disabled = true;
        processingState.style.display = 'block';

        fetch('/paginate_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            return response.json().then(data => {
                throw new Error(data.message || 'Error processing PDF');
            });
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const outputField = document.getElementById('output_filename');
            const fallbackName = pdfFileInput.files[0].name.replace('.pdf', '_paginated.pdf');
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
