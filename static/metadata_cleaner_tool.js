// PDF Metadata Cleaner Tool JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const cleanerForm = document.getElementById('cleanerForm');
    const submitBtn = document.getElementById('submitBtn');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const pdfFileInput = document.getElementById('pdf_file');

    // Store original button text
    const originalButtonText = submitBtn.innerHTML;

    // Form submission handler
    cleanerForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate file
        if (!pdfFileInput.files || pdfFileInput.files.length === 0) {
            showError('Please select a PDF file to clean');
            return;
        }

        const file = pdfFileInput.files[0];

        // Validate file type
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showError('Selected file must be a PDF');
            return;
        }

        // Validate file size (100 MB limit)
        const maxSize = 100 * 1024 * 1024;
        if (file.size > maxSize) {
            showError('File exceeds 100 MB limit');
            return;
        }

        // Check if at least one option is selected
        const removeMetadata = document.getElementById('remove_metadata').checked;
        const removeXmp = document.getElementById('remove_xmp').checked;
        const removeAnnotations = document.getElementById('remove_annotations').checked;
        const removeBookmarks = document.getElementById('remove_bookmarks').checked;
        const anonymizeDates = document.getElementById('anonymize_dates').checked;

        if (!removeMetadata && !removeXmp && !removeAnnotations && !removeBookmarks && !anonymizeDates) {
            showError('Please select at least one cleaning option');
            return;
        }

        // Create FormData
        const formData = new FormData(cleanerForm);

        // Show loading state
        submitBtn.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Cleaning Metadata...';
        submitBtn.disabled = true;
        successMessage.style.display = 'none';

        // Submit via AJAX
        fetch('/clean_metadata_route', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else if (response.status === 400 || response.status === 500) {
                return response.json().then(data => {
                    throw new Error(data.message || 'An error occurred during metadata cleaning');
                });
            } else {
                throw new Error('Server error occurred');
            }
        })
        .then(blob => {
            // Download the cleaned PDF
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            // Generate download filename
            const originalName = file.name.replace('.pdf', '');
            a.download = originalName + '_cleaned.pdf';

            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            // Show success message
            showSuccess('<strong>Metadata cleaned successfully!</strong> Your cleaned PDF has been downloaded. The file contains no identifying metadata.');

            // Reset form after 5 seconds
            setTimeout(() => {
                cleanerForm.reset();
                successMessage.style.display = 'none';
                submitBtn.innerHTML = originalButtonText;
                submitBtn.disabled = false;
            }, 5000);
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error.message);
            submitBtn.innerHTML = originalButtonText;
            submitBtn.disabled = false;
        });
    });

    // File input change listener (optional: show file info)
    pdfFileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            console.log('File selected:', this.files[0].name);
        }
    });

    /**
     * Show error modal
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorModal.style.display = 'flex';
    }

    /**
     * Show success message
     */
    function showSuccess(message) {
        successMessage.innerHTML = message;
        successMessage.style.display = 'block';
    }
});

/**
 * Close error modal (global function for onclick handler)
 */
function closeErrorModal() {
    const errorModal = document.getElementById('errorModal');
    errorModal.style.display = 'none';
}
