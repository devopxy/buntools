/* PDF Editor Tool JavaScript */

let currentFile = null;
let pdfDoc = null;
let pages = [];
let originalOrder = [];
let draggedIndex = null;

const MAX_THUMBNAIL_WIDTH = 180;

pdfjsLib.GlobalWorkerOptions.workerSrc =
    'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function showErrorModal(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorModal').classList.add('show');
}

function closeErrorModal() {
    document.getElementById('errorModal').classList.remove('show');
}

function toggleLoader(show) {
    document.getElementById('loader').style.display = show ? 'block' : 'none';
    document.getElementById('submitBtn').disabled = show;
}

function setEditorEnabled(enabled) {
    document.getElementById('editorSection').classList.toggle('hidden', !enabled);
    document.getElementById('submitBtn').disabled = !enabled;
}

function initializeUploadZone() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');

    uploadZone.addEventListener('click', () => fileInput.click());

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });
}

async function handleFile(file) {
    if (!file || (!file.type.includes('pdf') && !file.name.toLowerCase().endsWith('.pdf'))) {
        showErrorModal('Please select a valid PDF file.');
        return;
    }

    currentFile = file;
    const fileMeta = document.getElementById('fileMeta');
    fileMeta.textContent = `${file.name} (${formatFileSize(file.size)})`;
    fileMeta.classList.remove('hidden');

    const outputFilename = document.getElementById('outputFilename');
    const baseName = file.name.replace(/\\.pdf$/i, '');
    outputFilename.value = `${baseName}_edited.pdf`;

    await loadPdf(file);
}

async function loadPdf(file) {
    try {
        const data = await file.arrayBuffer();
        pdfDoc = await pdfjsLib.getDocument({ data }).promise;

        pages = [];
        for (let i = 1; i <= pdfDoc.numPages; i += 1) {
            pages.push({ pageNumber: i, rotation: 0 });
        }
        originalOrder = pages.map((page) => page.pageNumber);
        renderPageList();
        setEditorEnabled(true);
    } catch (err) {
        console.error(err);
        showErrorModal('Unable to read this PDF. Please try another file.');
        setEditorEnabled(false);
    }
}

function renderPageList() {
    const pageList = document.getElementById('pageList');
    const pageCount = document.getElementById('pageCount');

    pageCount.textContent = `${pages.length} page${pages.length === 1 ? '' : 's'}`;

    if (!pages.length) {
        pageList.innerHTML = '';
        return;
    }

    pageList.innerHTML = pages.map((page, index) => {
        const rotationBadge = page.rotation ? `<span class="badge">Rotate ${page.rotation} deg</span>` : '';
        return `
            <div class="page-item" draggable="true" data-index="${index}" data-page-number="${page.pageNumber}">
                <div class="page-header">
                    <span>Page ${page.pageNumber}</span>
                    <div class="page-badges">
                        <span class="badge">Order ${index + 1}</span>
                        ${rotationBadge}
                    </div>
                </div>
                <div class="page-preview">
                    <canvas id="pageCanvas-${page.pageNumber}"></canvas>
                </div>
                <div class="page-actions">
                    <button type="button" class="action-btn" onclick="rotatePage(${page.pageNumber}, -90)">Rotate left</button>
                    <button type="button" class="action-btn" onclick="rotatePage(${page.pageNumber}, 90)">Rotate right</button>
                    <button type="button" class="action-btn danger" onclick="deletePage(${page.pageNumber})">Delete</button>
                </div>
            </div>
        `;
    }).join('');

    addDragListeners();
    renderThumbnails();
}

async function renderThumbnails() {
    if (!pdfDoc) return;
    for (const page of pages) {
        await renderPageThumbnail(page);
    }
}

async function renderPageThumbnail(pageData) {
    if (!pdfDoc) return;
    const page = await pdfDoc.getPage(pageData.pageNumber);
    const viewport = page.getViewport({ scale: 1, rotation: pageData.rotation });
    const scale = MAX_THUMBNAIL_WIDTH / viewport.width;
    const scaledViewport = page.getViewport({ scale, rotation: pageData.rotation });

    const canvas = document.getElementById(`pageCanvas-${pageData.pageNumber}`);
    if (!canvas) return;
    const context = canvas.getContext('2d');
    canvas.width = scaledViewport.width;
    canvas.height = scaledViewport.height;

    await page.render({ canvasContext: context, viewport: scaledViewport }).promise;
}

function addDragListeners() {
    const items = document.querySelectorAll('.page-item');

    items.forEach((item) => {
        item.addEventListener('dragstart', (e) => {
            draggedIndex = Number(item.dataset.index);
            item.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        item.addEventListener('dragend', () => {
            item.classList.remove('dragging');
            draggedIndex = null;
        });

        item.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        item.addEventListener('drop', (e) => {
            e.preventDefault();
            const targetIndex = Number(item.dataset.index);
            if (draggedIndex === null || draggedIndex === targetIndex) return;
            const moved = pages.splice(draggedIndex, 1)[0];
            pages.splice(targetIndex, 0, moved);
            renderPageList();
        });
    });
}

function rotatePage(pageNumber, delta) {
    const page = pages.find((p) => p.pageNumber === pageNumber);
    if (!page) return;
    page.rotation = (page.rotation + delta + 360) % 360;
    renderPageList();
}

function deletePage(pageNumber) {
    pages = pages.filter((p) => p.pageNumber !== pageNumber);
    renderPageList();
}

function resetEdits() {
    pages = originalOrder.map((pageNumber) => ({ pageNumber, rotation: 0 }));
    renderPageList();
}

document.getElementById('resetEdits').addEventListener('click', resetEdits);

document.getElementById('editorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentFile || !pages.length) {
        showErrorModal('Please upload a PDF with at least one page.');
        return;
    }

    const outputFilename = document.getElementById('outputFilename').value.trim();
    const rotations = {};
    pages.forEach((page) => {
        if (page.rotation) {
            rotations[page.pageNumber] = page.rotation;
        }
    });

    const edits = {
        page_order: pages.map((page) => page.pageNumber),
        rotations
    };

    const formData = new FormData();
    formData.append('pdf_file', currentFile);
    formData.append('edits_json', JSON.stringify(edits));
    formData.append('output_filename', outputFilename);

    toggleLoader(true);

    try {
        const response = await fetch('/edit_pdf', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = outputFilename || 'edited_document.pdf';
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } else {
            const errorData = await response.json();
            showErrorModal(errorData.message || 'Error editing PDF.');
        }
    } catch (err) {
        console.error(err);
        showErrorModal(`Error: ${err.message}`);
    } finally {
        toggleLoader(false);
    }
});

window.addEventListener('DOMContentLoaded', () => {
    initializeUploadZone();
    setEditorEnabled(false);
});
