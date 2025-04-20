// Main JavaScript for Line Art Coloring Book Generator

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const darkModeToggle = document.getElementById('darkModeToggle');
    const generatePreviewBtn = document.getElementById('generatePreview');
    const generateBatchBtn = document.getElementById('generateBatch');
    const cancelGenerationBtn = document.getElementById('cancelGeneration');
    const modalCancelBtn = document.getElementById('modalCancelBtn');
    const downloadCurrentBtn = document.getElementById('downloadCurrent');
    const downloadAllBtn = document.getElementById('downloadAll');
    const previewPlaceholder = document.getElementById('previewPlaceholder');
    const previewImage = document.getElementById('previewImage');
    const batchGallery = document.getElementById('batchGallery');
    const batchPagination = document.getElementById('batchPagination');
    const progressModal = new bootstrap.Modal(document.getElementById('progressModal'));
    const progressBar = document.querySelector('.progress-bar');
    const progressStatus = document.getElementById('progressStatus');
    const timeRemaining = document.getElementById('timeRemaining');
    const apiStatus = document.getElementById('apiStatus');
    const enableTextToggle = document.getElementById('enableText');
    const textOptions = document.getElementById('textOptions');
    const randomSeedBtn = document.getElementById('randomSeed');
    
    // State variables
    let currentBatch = [];
    let currentBatchPage = 1;
    let imagesPerPage = 20;
    let isGenerating = false;
    let selectedFormat = 'png';
    let generationCancelled = false;
    
    // Check for saved preferences
    initializePreferences();
    
    // Event Listeners
    darkModeToggle.addEventListener('change', toggleDarkMode);
    generatePreviewBtn.addEventListener('click', generatePreview);
    generateBatchBtn.addEventListener('click', generateBatch);
    cancelGenerationBtn.addEventListener('click', cancelGeneration);
    modalCancelBtn.addEventListener('click', cancelGeneration);
    downloadCurrentBtn.addEventListener('click', downloadCurrentImage);
    downloadAllBtn.addEventListener('click', downloadAllImages);
    enableTextToggle.addEventListener('change', toggleTextOptions);
    randomSeedBtn.addEventListener('click', generateRandomSeed);
    
    // Format selection dropdown
    document.querySelectorAll('.dropdown-item[data-format]').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            selectedFormat = this.getAttribute('data-format');
            document.querySelectorAll('.dropdown-item[data-format]').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Advanced options toggle
    document.getElementById('advancedOptionsHeader').addEventListener('click', function() {
        const collapseElement = document.getElementById('advancedOptionsContent');
        const bsCollapse = new bootstrap.Collapse(collapseElement, {
            toggle: false
        });
        bsCollapse.toggle();
    });
    
    /**
     * Initialize user preferences from localStorage
     */
    function initializePreferences() {
        // Check for dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            darkModeToggle.checked = true;
            document.body.classList.add('dark-mode');
        }
        
        // Load other saved preferences if they exist
        const savedPreferences = JSON.parse(localStorage.getItem('generatorPreferences') || '{}');
        
        for (const [key, value] of Object.entries(savedPreferences)) {
            const element = document.getElementById(key);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = value;
                } else if (element.tagName === 'SELECT' || element.type === 'range' || element.type === 'number' || element.type === 'text') {
                    element.value = value;
                }
            }
        }
        
        // Initialize text options visibility
        toggleTextOptions();
    }
    
    /**
     * Save current preferences to localStorage
     */
    function savePreferences() {
        localStorage.setItem('darkMode', darkModeToggle.checked);
        
        const preferencesToSave = {};
        const formElements = document.getElementById('generationForm').elements;
        
        for (let i = 0; i < formElements.length; i++) {
            const element = formElements[i];
            if (element.id) {
                if (element.type === 'checkbox') {
                    preferencesToSave[element.id] = element.checked;
                } else if (element.tagName === 'SELECT' || element.type === 'range' || element.type === 'number' || element.type === 'text') {
                    preferencesToSave[element.id] = element.value;
                }
            }
        }
        
        localStorage.setItem('generatorPreferences', JSON.stringify(preferencesToSave));
    }
    
    /**
     * Toggle dark mode
     */
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode', darkModeToggle.checked);
        localStorage.setItem('darkMode', darkModeToggle.checked);
    }
    
    /**
     * Toggle text options visibility
     */
    function toggleTextOptions() {
        textOptions.classList.toggle('d-none', !enableTextToggle.checked);
    }
    
    /**
     * Generate a random seed value
     */
    function generateRandomSeed() {
        document.getElementById('seedValue').value = Math.floor(Math.random() * 1000000000);
    }
    
    /**
     * Get current form parameters
     */
    function getFormParameters() {
        return {
            sceneType: document.getElementById('sceneType').value,
            styleDescriptor: document.getElementById('styleDescriptor').value,
            batchSize: parseInt(document.getElementById('batchSize').value),
            batchName: document.getElementById('batchName').value,
            sequentialNumbering: document.getElementById('sequentialNumbering').checked,
            resolution: parseInt(document.getElementById('resolution').value),
            lineThickness: parseInt(document.getElementById('lineThickness').value),
            lineStyle: document.getElementById('lineStyle').value,
            marginSize: parseInt(document.getElementById('marginSize').value),
            enableText: document.getElementById('enableText').checked,
            textContent: document.getElementById('textContent').value,
            fontSelection: document.getElementById('fontSelection').value,
            textPosition: document.getElementById('textPosition').value,
            seedValue: parseInt(document.getElementById('seedValue').value),
            modelSelection: document.getElementById('modelSelection').value,
            guidanceScale: parseFloat(document.getElementById('guidanceScale').value),
            generationSteps: parseInt(document.getElementById('generationSteps').value)
        };
    }
    
    /**
     * Generate a preview image
     */
    function generatePreview() {
        if (isGenerating) return;
        
        const params = getFormParameters();
        savePreferences();
        
        // Show loading state
        previewPlaceholder.classList.remove('d-none');
        previewImage.classList.add('d-none');
        previewPlaceholder.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Generating preview...</p></div>';
        
        // Update API status
        apiStatus.textContent = 'API Status: Generating preview...';
        
        // In a real implementation, this would call the API
        // For now, we'll simulate the API call with a timeout
        isGenerating = true;
        
        // Simulate API call
        simulateApiCall(params, 1)
            .then(results => {
                if (results.length > 0) {
                    displayPreviewImage(results[0]);
                }
                isGenerating = false;
                apiStatus.textContent = 'API Status: Ready';
            })
            .catch(error => {
                console.error('Error generating preview:', error);
                previewPlaceholder.innerHTML = '<div class="text-center text-danger"><i class="bi bi-exclamation-triangle fs-1"></i><p>Error generating preview</p></div>';
                isGenerating = false;
                apiStatus.textContent = 'API Status: Error';
            });
    }
    
    /**
     * Generate a batch of images
     */
    function generateBatch() {
        if (isGenerating) return;
        
        const params = getFormParameters();
        savePreferences();
        
        // Validate batch size
        if (params.batchSize < 1 || params.batchSize > 60) {
            alert('Batch size must be between 1 and 60');
            return;
        }
        
        // Show progress modal
        progressBar.style.width = '0%';
        progressBar.setAttribute('aria-valuenow', 0);
        progressStatus.textContent = 'Initializing...';
        timeRemaining.textContent = 'Estimated time remaining: calculating...';
        progressModal.show();
        
        // Show cancel button
        cancelGenerationBtn.classList.remove('d-none');
        
        // Update API status
        apiStatus.textContent = 'API Status: Generating batch...';
        
        // Reset cancellation flag
        generationCancelled = false;
        
        // In a real implementation, this would call the API
        // For now, we'll simulate the API call with a timeout
        isGenerating = true;
        currentBatch = [];
        
        // Simulate API call with progress updates
        simulateApiCall(params, params.batchSize, updateProgress)
            .then(results => {
                if (!generationCancelled) {
                    currentBatch = results;
                    displayBatchGallery();
                    progressModal.hide();
                }
                isGenerating = false;
                cancelGenerationBtn.classList.add('d-none');
                apiStatus.textContent = 'API Status: Ready';
            })
            .catch(error => {
                console.error('Error generating batch:', error);
                progressStatus.textContent = 'Error: ' + error.message;
                isGenerating = false;
                cancelGenerationBtn.classList.add('d-none');
                apiStatus.textContent = 'API Status: Error';
                
                // Auto-close modal after error
                setTimeout(() => {
                    progressModal.hide();
                }, 3000);
            });
    }
    
    /**
     * Cancel the current generation
     */
    function cancelGeneration() {
        if (!isGenerating) return;
        
        generationCancelled = true;
        progressStatus.textContent = 'Cancelling...';
        
        // In a real implementation, this would call the API to cancel the generation
        // For now, we'll just update the UI
        setTimeout(() => {
            isGenerating = false;
            cancelGenerationBtn.classList.add('d-none');
            progressModal.hide();
            apiStatus.textContent = 'API Status: Ready';
        }, 1000);
    }
    
    /**
     * Update the progress bar and status
     */
    function updateProgress(current, total, timeLeft) {
        if (generationCancelled) return;
        
        const percent = Math.round((current / total) * 100);
        progressBar.style.width = percent + '%';
        progressBar.setAttribute('aria-valuenow', percent);
        progressStatus.textContent = `Generating image ${current} of ${total}`;
        
        if (timeLeft) {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = Math.floor(timeLeft % 60);
            timeRemaining.textContent = `Estimated time remaining: ${minutes}m ${seconds}s`;
        }
    }
    
    /**
     * Display the preview image
     */
    function displayPreviewImage(imageData) {
        // In a real implementation, imageData would be the URL or base64 data of the generated image
        // For now, we'll use a placeholder image
        previewImage.src = imageData.url;
        previewImage.classList.remove('d-none');
        previewPlaceholder.classList.add('d-none');
        
        // Enable download button
        downloadCurrentBtn.disabled = false;
    }
    
    /**
     * Display the batch gallery
     */
    function displayBatchGallery() {
        if (currentBatch.length === 0) {
            batchGallery.innerHTML = `
                <div class="col text-center text-muted">
                    <div class="gallery-placeholder d-flex align-items-center justify-content-center">
                        <p>No images generated yet</p>
                    </div>
                </div>
            `;
            batchPagination.classList.add('d-none');
            downloadAllBtn.disabled = true;
            return;
        }
        
        // Enable download all button
        downloadAllBtn.disabled = false;
        
        // Calculate pagination
        const totalPages = Math.ceil(currentBatch.length / imagesPerPage);
        const startIndex = (currentBatchPage - 1) * imagesPerPage;
        const endIndex = Math.min(startIndex + imagesPerPage, currentBatch.length);
        
        // Generate gallery HTML
        let galleryHTML = '';
        for (let i = startIndex; i < endIndex; i++) {
            const image = currentBatch[i];
            galleryHTML += `
                <div class="col">
                    <div class="gallery-item" data-index="${i}">
                        <img src="${image.url}" alt="Generated image ${i + 1}" class="img-fluid">
                    </div>
                </div>
            `;
        }
        
        batchGallery.innerHTML = galleryHTML;
        
        // Add click event to gallery items
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                displayPreviewImage(currentBatch[index]);
                
                // Update selected state
                document.querySelectorAll('.gallery-item').forEach(i => i.classList.remove('selected'));
                this.classList.add('selected');
            });
        });
        
        // Update pagination if needed
        if (totalPages > 1) {
            updatePagination(totalPages);
            batchPagination.classList.remove('d-none');
        } else {
            batchPagination.classList.add('d-none');
        }
    }
    
    /**
     * Update the pagination controls
     */
    function updatePagination(totalPages) {
        let paginationHTML = `
            <li class="page-item ${currentBatchPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="prev">Previous</a>
            </li>
        `;
        
        // Generate page numbers
        for (let i = 1; i <= totalPages; i++) {
            paginationHTML += `
                <li class="page-item ${i === currentBatchPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
        }
        
        paginationHTML += `
            <li class="page-item ${currentBatchPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="next">Next</a>
            </li>
        `;
        
        const paginationElement = document.querySelector('#batchPagination ul');
        paginationElement.innerHTML = paginationHTML;
        
        // Add click events to pagination links
        document.querySelectorAll('#batchPagination a.page-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const page = this.getAttribute('data-page');
                if (page === 'prev') {
                    if (currentBatchPage > 1) {
                        currentBatchPage--;
                        displayBatchGallery();
                    }
                } else if (page === 'next') {
                    if (currentBatchPage < totalPages) {
                        currentBatchPage++;
                        displayBatchGallery();
                    }
                } else {
                    currentBatchPage = parseInt(page);
                    displayBatchGallery();
                }
            });
        });
    }
    
    /**
     * Download the current image
     */
    function downloadCurrentImage() {
        if (previewImage.classList.contains('d-none')) return;
        
        // In a real implementation, this would download the actual image
        // For now, we'll just open the image in a new tab
        const params = getFormParameters();
        const filename = `${params.batchName}_preview.${selectedFormat}`;
        
        // Simulate download by opening in new tab
        window.open(previewImage.src, '_blank');
        
        // In a real implementation, we would use something like:
        // const link = document.createElement('a');
        // link.href = previewImage.src;
        // link.download = filename;
        // link.click();
    }
    
    /**
     * Download all images as a ZIP file
     */
    function downloadAllImages() {
        if (currentBatch.length === 0) return;
        
        // In a real implementation, this would create a ZIP file with all images
        // For now, we'll just show a message
        const params = getFormParameters();
        const filename = `${params.batchName}.zip`;
        
        alert(`In a real implementation, this would download a ZIP file named "${filename}" containing all ${currentBatch.length} images.`);
        
        // In a real implementation, we would use JSZip:
        // const zip = new JSZip();
        // currentBatch.forEach((image, index) => {
        //     const imgName = params.sequentialNumbering 
        //         ? `${params.batchName}_${(index + 1).toString().padStart(3, '0')}.${selectedFormat}`
        //         : `${params.batchName}_${image.seed}.${selectedFormat}`;
        //     
        //     // Add image to zip (would need to fetch the actual image data)
        //     zip.file(imgName, fetchImageData(image.url));
        // });
        // 
        // zip.generateAsync({type: 'blob'}).then(function(content) {
        //     saveAs(content, filename);
        // });
    }
    
    /**
     * Simulate an API call to generate images
     * @param {Object} params - The generation parameters
     * @param {number} count - The number of images to generate
     * @param {Function} progressCallback - Optional callback for progress updates
     * @returns {Promise<Array>} - A promise that resolves to an array of image data
     */
    function simulateApiCall(params, count, progressCallback) {
        return new Promise((resolve, reject) => {
            const results = [];
            let current = 0;
            
            // Calculate a realistic time per image based on parameters
            const baseTimePerImage = 2000; // 2 seconds base time
            const stepsFactor = params.generationSteps / 30; // Normalize to 30 steps
            const resolutionFactor = Math.pow(params.resolution / 512, 2); // Square factor for resolution
            
            const timePerImage = baseTimePerImage * stepsFactor * resolutionFactor;
            const totalTime = timePerImage * count;
            
            // Use the sample image as a placeholder
            const placeholderImage = '/home/ubuntu/upload/Gemini_Generated_Image_8rpznj8rpznj8rpz.jpeg';
            
            const interval = setInterval(() => {
                if (generationCancelled) {
                    clearInterval(interval);
                    resolve(results);
                    return;
                }
                
                current++;
                
                // Create a simulated result
                results.push({
                    url: placeholderImage,
                    seed: params.seedValue === -1 ? Math.floor(Math.random() * 1000000000) : params.seedValue + current,
                    params: { ...params }
                });
                
                // Call progress callback if provided
                if (progressCallback) {
                    const timeLeft = (count - current) * (totalTime / count) / 1000;
                    progressCallback(current, count, timeLeft);
                }
                
                // Resolve when all images are generated
                if (current >= count) {
                    clearInterval(interval);
                    resolve(results);
                }
            }, timePerImage / 10); // Speed up simulation by factor of 10
        });
    }
});
