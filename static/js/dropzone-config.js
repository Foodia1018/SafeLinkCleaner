/**
 * SafeLink Protection Cleaner - Dropzone Configuration
 * Configuration for the Dropzone.js file upload library
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Dropzone if the element exists
    if (typeof Dropzone !== 'undefined' && document.querySelector('#dropzone-upload')) {
        Dropzone.autoDiscover = false;
        
        const myDropzone = new Dropzone('#dropzone-upload', {
            url: '/upload',
            paramName: 'emailList',
            maxFilesize: 10, // 10MB
            acceptedFiles: '.csv,.txt,.xlsx',
            addRemoveLinks: true,
            dictDefaultMessage: 'Drop email list file here or click to upload',
            dictRemoveFile: 'Remove',
            dictFileTooBig: 'File is too big ({{filesize}}MB). Max filesize: {{maxFilesize}}MB.',
            dictInvalidFileType: 'Invalid file type. Please upload CSV, TXT, or XLSX files.',
            createImageThumbnails: false,
            
            // Style dropzone element
            previewTemplate: `
                <div class="dz-preview dz-file-preview">
                    <div class="dz-details">
                        <div class="dz-filename"><span data-dz-name></span></div>
                        <div class="dz-size" data-dz-size></div>
                    </div>
                    <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>
                    <div class="dz-error-message"><span data-dz-errormessage></span></div>
                    <div class="dz-success-mark"><span>✓</span></div>
                    <div class="dz-error-mark"><span>✗</span></div>
                </div>
            `,
            
            init: function() {
                this.on('addedfile', function(file) {
                    console.log('File added:', file.name);
                    
                    // Check file type
                    const extension = file.name.split('.').pop().toLowerCase();
                    if (!['csv', 'txt', 'xlsx'].includes(extension)) {
                        this.removeFile(file);
                        showAlert('Invalid file format. Please upload CSV, TXT, or XLSX files.', 'danger');
                        return;
                    }
                    
                    // Enable the process button
                    const processButton = document.getElementById('process-button');
                    if (processButton) {
                        processButton.disabled = false;
                    }
                });
                
                this.on('sending', function(file, xhr, formData) {
                    // Show loading state
                    const processButton = document.getElementById('process-button');
                    if (processButton) {
                        processButton.disabled = true;
                        processButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
                    }
                    
                    // Add CSRF token if needed
                    const csrfToken = document.querySelector('meta[name="csrf-token"]');
                    if (csrfToken) {
                        formData.append('csrf_token', csrfToken.content);
                    }
                });
                
                this.on('success', function(file, response) {
                    console.log('Upload successful:', response);
                    
                    // Redirect to results page if available
                    if (response && response.redirect_url) {
                        window.location.href = response.redirect_url;
                    } else {
                        // Reset button state
                        const processButton = document.getElementById('process-button');
                        if (processButton) {
                            processButton.disabled = false;
                            processButton.innerHTML = 'Process Email List';
                        }
                        
                        showAlert('File uploaded successfully! Processing email list...', 'success');
                    }
                });
                
                this.on('error', function(file, errorMessage) {
                    console.error('Upload error:', errorMessage);
                    
                    // Reset button state
                    const processButton = document.getElementById('process-button');
                    if (processButton) {
                        processButton.disabled = false;
                        processButton.innerHTML = 'Process Email List';
                    }
                    
                    // Show error message
                    let message = 'An error occurred during upload.';
                    if (typeof errorMessage === 'string') {
                        message = errorMessage;
                    } else if (errorMessage && errorMessage.message) {
                        message = errorMessage.message;
                    }
                    
                    showAlert(`Error: ${message}`, 'danger');
                });
            }
        });
        
        // Handle manual form submission
        const uploadForm = document.getElementById('upload-form');
        if (uploadForm) {
            uploadForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Check if files are added to dropzone
                if (myDropzone.getQueuedFiles().length > 0) {
                    myDropzone.processQueue();
                } else {
                    showAlert('Please select a file to upload', 'warning');
                }
            });
        }
    }
});

/**
 * Display an alert message
 */
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.role = 'alert';
    
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alertElement);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertElement.classList.remove('show');
        setTimeout(() => {
            alertElement.remove();
        }, 150);
    }, 5000);
}
