/**
 * SafeLink Protection Cleaner - Main JavaScript
 * Handles UI interactions, form submissions, and dynamic content updates
 */

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('Initializing SafeLink Protection Cleaner...');
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize dropzone if upload form exists
    initFileUpload();
    
    // Initialize job polling if on results page
    initJobPolling();
    
    // Initialize domain analyzer
    initDomainAnalyzer();
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    // Initialize all tooltips using Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize file upload zone
 */
function initFileUpload() {
    const uploadForm = document.getElementById('upload-form');
    if (!uploadForm) return;
    
    const fileInput = document.getElementById('emailList');
    const dropZone = document.getElementById('drop-zone');
    const fileNameDisplay = document.getElementById('file-name');
    
    if (dropZone) {
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        // Remove highlighting when item leaves the zone
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);
        
        // Handle click to select files
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
        
        // Display selected filename
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                fileNameDisplay.textContent = fileInput.files[0].name;
                dropZone.classList.add('has-file');
            }
        });
    }
    
    // Validate file before form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                showAlert('Please select a file to upload', 'warning');
                return false;
            }
            
            const file = fileInput.files[0];
            const extension = file.name.split('.').pop().toLowerCase();
            
            if (!['csv', 'txt', 'xlsx'].includes(extension)) {
                e.preventDefault();
                showAlert('Invalid file format. Please upload CSV, TXT, or XLSX files.', 'danger');
                return false;
            }
            
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                e.preventDefault();
                showAlert('File size exceeds 10MB limit', 'danger');
                return false;
            }
        });
    }
}

/**
 * Initialize job polling on results page
 */
function initJobPolling() {
    const progressBar = document.getElementById('job-progress');
    const statusText = document.getElementById('job-status');
    
    if (!progressBar || !statusText) return;
    
    const jobId = progressBar.dataset.jobId;
    
    if (!jobId) return;
    
    // Poll the job status every 3 seconds
    const pollInterval = setInterval(() => {
        fetch(`/api/job-status/${jobId}`)
            .then(response => response.json())
            .then(data => {
                // Update progress bar
                progressBar.style.width = `${data.progress}%`;
                progressBar.setAttribute('aria-valuenow', data.progress);
                
                // Update status text
                statusText.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
                
                // If job is completed or failed, stop polling
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    statusText.classList.add('text-success');
                    progressBar.classList.add('bg-success');
                    
                    // Refresh the page to show results
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    statusText.classList.add('text-danger');
                    progressBar.classList.add('bg-danger');
                    
                    // Show error message
                    if (data.error) {
                        showAlert(`Processing failed: ${data.error}`, 'danger');
                    }
                }
            })
            .catch(error => {
                console.error('Error polling job status:', error);
                // Don't stop polling on temporary errors
            });
    }, 3000);
}

/**
 * Initialize domain analyzer
 */
function initDomainAnalyzer() {
    const analyzerForm = document.getElementById('domain-analyzer-form');
    if (!analyzerForm) return;
    
    analyzerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const emailInput = document.getElementById('email-to-analyze');
        const email = emailInput.value.trim();
        
        if (!email) {
            showAlert('Please enter an email address', 'warning');
            return;
        }
        
        if (!isValidEmail(email)) {
            showAlert('Please enter a valid email address', 'warning');
            return;
        }
        
        // Show loading indicator
        const resultsContainer = document.getElementById('analyzer-results');
        resultsContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Analyzing domain...</p></div>';
        
        // Call the API
        fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        })
            .then(response => response.json())
            .then(data => {
                // Display the results
                displayAnalyzerResults(data, resultsContainer);
            })
            .catch(error => {
                console.error('Error analyzing domain:', error);
                resultsContainer.innerHTML = '<div class="alert alert-danger">An error occurred while analyzing the domain. Please try again.</div>';
            });
    });
}

/**
 * Display domain analyzer results
 */
function displayAnalyzerResults(data, container) {
    const domain = data.domain;
    
    let resultHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Analysis Results for ${domain}</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <strong>Domain Status:</strong> 
                    ${data.valid_domain ? 
                        '<span class="badge bg-success">Valid</span>' : 
                        '<span class="badge bg-danger">Invalid</span>'}
                </div>
                
                <div class="mb-3">
                    <strong>MX Records:</strong> 
                    ${data.has_mx_records ? 
                        '<span class="badge bg-success">Found</span>' : 
                        '<span class="badge bg-danger">Not Found</span>'}
                </div>
                
                <div class="mb-3">
                    <strong>Security Protection:</strong> 
                    ${data.is_protected ? 
                        `<span class="badge bg-warning">Protected by ${data.security_system}</span>` : 
                        '<span class="badge bg-success">No Protection Detected</span>'}
                </div>
                
                <div class="mb-3">
                    <strong>Disposable Email:</strong> 
                    ${data.is_disposable ? 
                        '<span class="badge bg-danger">Yes</span>' : 
                        '<span class="badge bg-success">No</span>'}
                </div>
            </div>
            <div class="card-footer">
                <p class="mb-0">
                    ${data.is_protected || !data.valid_domain || !data.has_mx_records || data.is_disposable ? 
                        '<i class="fas fa-exclamation-triangle text-warning"></i> This email would be filtered out by SafeLink Protection Cleaner.' : 
                        '<i class="fas fa-check-circle text-success"></i> This email would pass SafeLink Protection Cleaner filters.'}
                </p>
            </div>
        </div>
    `;
    
    container.innerHTML = resultHTML;
}

/**
 * Prevent default behavior for events
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Highlight drop zone on drag
 */
function highlight(e) {
    const dropZone = document.getElementById('drop-zone');
    if (dropZone) {
        dropZone.classList.add('dropzone-active');
    }
}

/**
 * Remove highlight from drop zone
 */
function unhighlight(e) {
    const dropZone = document.getElementById('drop-zone');
    if (dropZone) {
        dropZone.classList.remove('dropzone-active');
    }
}

/**
 * Handle file drop event
 */
function handleDrop(e) {
    const fileInput = document.getElementById('emailList');
    const fileNameDisplay = document.getElementById('file-name');
    const dropZone = document.getElementById('drop-zone');
    
    if (!fileInput || !fileNameDisplay || !dropZone) return;
    
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        fileInput.files = files;
        fileNameDisplay.textContent = files[0].name;
        dropZone.classList.add('has-file');
    }
}

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

/**
 * Validate email format
 */
function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}
