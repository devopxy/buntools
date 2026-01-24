// PDF Version Comparison Tool JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const compareForm = document.getElementById('compareForm');
    const submitBtn = document.getElementById('submitBtn');
    const errorModal = document.getElementById('errorModal');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const pdfFile1Input = document.getElementById('pdf_file_1');
    const pdfFile2Input = document.getElementById('pdf_file_2');

    // Store original button text
    const originalButtonText = submitBtn.innerHTML;

    // Form submission handler
    compareForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate files
        if (!pdfFile1Input.files || pdfFile1Input.files.length === 0) {
            showError('Please select the first PDF file (Version 1)');
            return;
        }

        if (!pdfFile2Input.files || pdfFile2Input.files.length === 0) {
            showError('Please select the second PDF file (Version 2)');
            return;
        }

        const file1 = pdfFile1Input.files[0];
        const file2 = pdfFile2Input.files[0];

        // Validate file types
        if (!file1.name.toLowerCase().endsWith('.pdf')) {
            showError('Version 1 file must be a PDF');
            return;
        }

        if (!file2.name.toLowerCase().endsWith('.pdf')) {
            showError('Version 2 file must be a PDF');
            return;
        }

        // Validate file sizes (100 MB limit)
        const maxSize = 100 * 1024 * 1024;
        if (file1.size > maxSize) {
            showError('Version 1 file exceeds 100 MB limit');
            return;
        }

        if (file2.size > maxSize) {
            showError('Version 2 file exceeds 100 MB limit');
            return;
        }

        // Check if files are the same name
        if (file1.name === file2.name) {
            const confirmSameName = confirm('Both files have the same filename. Are you sure you want to compare these files?');
            if (!confirmSameName) {
                return;
            }
        }

        // Create FormData
        const formData = new FormData(compareForm);

        // Show loading state
        submitBtn.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Comparing PDFs...';
        submitBtn.disabled = true;
        successMessage.style.display = 'none';

        // Submit via AJAX
        fetch('/compare_pdfs_route', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Check if response is JSON (for identical files message)
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json().then(data => {
                        // Files are identical
                        showSuccess(data.message || 'Files are identical');
                        submitBtn.innerHTML = originalButtonText;
                        submitBtn.disabled = false;
                        return null; // Signal no file to download
                    });
                } else {
                    // HTML blob response
                    return response.blob();
                }
            } else if (response.status === 400 || response.status === 500) {
                return response.json().then(data => {
                    throw new Error(data.message || 'An error occurred during comparison');
                });
            } else {
                throw new Error('Server error occurred');
            }
        })
        .then(blob => {
            if (blob === null) {
                // Files were identical, no download
                return;
            }

            // Download the HTML report
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'comparison_report.html';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            // Show success message
            showSuccess('<strong>Comparison complete!</strong> Your comparison report has been downloaded. Open the HTML file in your browser to view the results.');

            // Reset form after 5 seconds
            setTimeout(() => {
                compareForm.reset();
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

    // File input change listeners (optional: show file info)
    pdfFile1Input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            console.log('Version 1 selected:', this.files[0].name);
        }
    });

    pdfFile2Input.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            console.log('Version 2 selected:', this.files[0].name);
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
