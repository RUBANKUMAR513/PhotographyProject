let selectedImages = JSON.parse(localStorage.getItem('selectedImages')) || [];
let currentPage = 1;
const imagesPerPage = 8;

// Example image data
const images = [
    { id: '1', src: "test1.jpg", alt: "Image 1" },
    { id: '2', src: "test2.jpg", alt: "Image 2" },
    { id: '3', src: "test3.jpg", alt: "Image 3" },
    { id: '4', src: "test4.jpg", alt: "Image 4" },
    { id: '5', src: "marriage.jpg", alt: "Image 5" },
    { id: '6', src: "marriage1.jpg", alt: "Image 6" },
    { id: '7', src: "marriage2.jpg", alt: "Image 7" },
    { id: '8', src: "marriage3.jpg", alt: "Image 8" },
    { id: '9', src: "marriage4.jpg", alt: "Image 9" },
    { id: '10', src: "baby1_alt1.jpg", alt: "Image 10" }
];

window.onload = function () {
    displayImages(currentPage);
    setupPagination();
    updateSelectedImagesContainer();
    preventRightClick();
    preventScreenshots();
};

// Function to display images on the current page
function displayImages(page) {
    const imageContainer = document.getElementById("imageContainer");
    imageContainer.innerHTML = "";

    const start = (page - 1) * imagesPerPage;
    const end = start + imagesPerPage;
    const currentImages = images.slice(start, end);

    currentImages.forEach(image => {
        const imageBox = document.createElement('div');
        imageBox.classList.add('image-box');
        imageBox.setAttribute('data-id', image.id);

        const img = document.createElement('img');
        img.src = image.src;
        img.alt = image.alt;
        img.addEventListener('contextmenu', function (e) {
            e.preventDefault();
        });

        const buttonGroup = document.createElement('div');
        buttonGroup.classList.add('button-group');

        // Heart Icon
        const heartContainer = document.createElement('div');
        heartContainer.classList.add('icon-container');
        const heartIcon = document.createElement('i');
        heartIcon.classList.add('heart-icon', 'fas', 'fa-heart');
        if (selectedImages.includes(image.id)) {
            heartIcon.classList.add('filled');
            imageBox.classList.add('selected');
        }
        const heartTooltip = document.createElement('div');
        heartTooltip.classList.add('tooltip');
        heartTooltip.textContent = 'Favorite';
        heartContainer.appendChild(heartIcon);
        heartContainer.appendChild(heartTooltip);

        // View Icon
        const viewContainer = document.createElement('div');
        viewContainer.classList.add('icon-container');
        const viewIcon = document.createElement('i');
        viewIcon.classList.add('view-icon', 'fas', 'fa-eye');
        viewIcon.setAttribute('onclick', `viewImage('${image.src}')`);
        const viewTooltip = document.createElement('div');
        viewTooltip.classList.add('tooltip');
        viewTooltip.textContent = 'View';
        viewContainer.appendChild(viewIcon);
        viewContainer.appendChild(viewTooltip);

        // Download Icon
        const downloadContainer = document.createElement('div');
        downloadContainer.classList.add('icon-container');
        const downloadIcon = document.createElement('i');
        downloadIcon.classList.add('download-icon', 'fas', 'fa-download');
        downloadIcon.setAttribute('onclick', `downloadImage('${image.src}')`);
        const downloadTooltip = document.createElement('div');
        downloadTooltip.classList.add('tooltip');
        downloadTooltip.textContent = 'Download';
        downloadContainer.appendChild(downloadIcon);
        downloadContainer.appendChild(downloadTooltip);

        buttonGroup.appendChild(heartContainer);
        buttonGroup.appendChild(viewContainer);
        buttonGroup.appendChild(downloadContainer);

        imageBox.appendChild(img);
        imageBox.appendChild(buttonGroup);

        imageContainer.appendChild(imageBox);
    });

    // Add event listeners for heart icons after rendering
    addHeartEventListeners();
}

// Function to add event listeners to heart icons
function addHeartEventListeners() {
    document.querySelectorAll('.heart-icon').forEach(icon => {
        icon.addEventListener('click', function (e) {
            e.stopPropagation(); // Prevent event bubbling to imageContainer
            const imageBox = this.closest('.image-box');
            const imageId = imageBox.getAttribute('data-id');

            if (this.classList.contains('filled')) {
                this.classList.remove('filled');
                imageBox.classList.remove('selected');
                selectedImages = selectedImages.filter(id => id !== imageId);
            } else {
                this.classList.add('filled');
                imageBox.classList.add('selected');
                selectedImages.push(imageId);
            }

            localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
            updateSelectedImagesContainer();
        });
    });
}

// Function to setup pagination buttons
function setupPagination() {
    const pagination = document.getElementById("pagination");
    const totalPages = Math.ceil(images.length / imagesPerPage);

    pagination.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("button");
        pageButton.innerText = i;
        pageButton.className = "page-btn";
        if (i === currentPage) pageButton.classList.add("active");
        pageButton.addEventListener("click", () => {
            currentPage = i;
            displayImages(currentPage);
            setupPagination();
        });
        pagination.appendChild(pageButton);
    }
}

// Function to update selected images container
function updateSelectedImagesContainer() {
    const selectedImagesContainer = document.getElementById('selectedImagesContainer');
    selectedImagesContainer.innerHTML = '';

    if (selectedImages.length === 0) {
        selectedImagesContainer.innerHTML = '<p class="no-images">No images selected</p>';
    } else {
        selectedImages.forEach(imageId => {
            const image = images.find(img => img.id === imageId);
            if (image) {
                const imageBox = document.createElement('div');
                imageBox.classList.add('image-box', 'selected-image');
                imageBox.setAttribute('data-id', image.id);

                const img = document.createElement('img');
                img.src = image.src;
                img.alt = image.alt;
                img.addEventListener('contextmenu', function (e) {
                    e.preventDefault();
                });

                const buttonGroup = document.createElement('div');
                buttonGroup.classList.add('button-group');
                

                // View Button
                const viewIconContainer = document.createElement('div');
                viewIconContainer.classList.add('icon-container');
                const viewIcon = document.createElement('i');
                viewIcon.classList.add('view-icon', 'fas', 'fa-eye');
                viewIcon.addEventListener('click', () => viewImage(imageBox.querySelector('img').src));
                const viewTooltip = document.createElement('div');
                viewTooltip.classList.add('tooltip');
                viewTooltip.textContent = 'View';
                viewIconContainer.appendChild(viewIcon);
                viewIconContainer.appendChild(viewTooltip);
                buttonGroup.appendChild(viewIconContainer);

                // Download Button
                const downloadIconContainer = document.createElement('div');
                downloadIconContainer.classList.add('icon-container');
                const downloadIcon = document.createElement('i');
                downloadIcon.classList.add('download-icon', 'fas', 'fa-download');
                downloadIcon.addEventListener('click', () => downloadImage(imageBox.querySelector('img').src));
                const downloadTooltip = document.createElement('div');
                downloadTooltip.classList.add('tooltip');
                downloadTooltip.textContent = 'Download';
                downloadIconContainer.appendChild(downloadIcon);
                downloadIconContainer.appendChild(downloadTooltip);
                buttonGroup.appendChild(downloadIconContainer);

                // Remove Icon
                const removeContainer = document.createElement('div');
                removeContainer.classList.add('icon-container');
                const removeIcon = document.createElement('i');
                removeIcon.classList.add('remove-icon', 'fas', 'fa-times');
                removeIcon.addEventListener('click', () => removeSelectedImage(image.id));
                const removeTooltip = document.createElement('div');
                removeTooltip.classList.add('tooltip');
                removeTooltip.textContent = 'Remove';
                removeContainer.appendChild(removeIcon);
                removeContainer.appendChild(removeTooltip);

                buttonGroup.appendChild(removeContainer);

                imageBox.appendChild(img);
                imageBox.appendChild(buttonGroup);

                selectedImagesContainer.appendChild(imageBox);
            }
        });
    }
}

// Function to remove selected image
function removeSelectedImage(imageId) {
    selectedImages = selectedImages.filter(id => id !== imageId);
    localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
    updateSelectedImagesContainer();
    // Update heart icon in main image container if the image is on the current page
    const imageBox = document.querySelector(`.image-box[data-id="${imageId}"]`);
    if (imageBox) {
        imageBox.classList.remove('selected');
        const heartIcon = imageBox.querySelector('.heart-icon');
        if (heartIcon) {
            heartIcon.classList.remove('filled');
        }
    }
}

// Function to save selection
function saveSelection() {
    alert("Selected images saved!");
    // Implement save functionality here (e.g., send to server)
}

// Function to view image in fullscreen
function viewImage(imageUrl) {
    const fullscreenOverlay = document.getElementById('fullscreenOverlay');
    const fullscreenImage = document.getElementById('fullscreenImage');

    fullscreenImage.src = imageUrl;
    fullscreenOverlay.style.display = 'flex';
    fullscreenImage.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });
}

// Function to close fullscreen view
function closeFullscreen() {
    const fullscreenOverlay = document.getElementById('fullscreenOverlay');
    fullscreenOverlay.style.display = 'none';
}

// Function to download image
function downloadImage(imageUrl) {
    const a = document.createElement('a');
    a.href = imageUrl;
    a.download = imageUrl.split('/').pop();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    alert("Download initiated for " + a.download);
}

// Function to prevent right-click context menu on specific elements
function preventRightClick() {
    const elements = [
        document.getElementById('imageContainer'),
        document.getElementById('selectedImagesContainer'),
        ...document.querySelectorAll('.image-box img'),
        document.getElementById('fullscreenOverlay')
    ];

    elements.forEach(element => {
        if (element) {
            element.addEventListener('contextmenu', function (e) {
                e.preventDefault();
            });
        }
    });
}

// Function to prevent screenshot functionality
function preventScreenshots() {
    document.addEventListener('keydown', function (e) {
        if (e.key === 'PrintScreen' || (e.ctrlKey && (e.key === 'p' || e.key === 's'))) {
            e.preventDefault();
            alert("Screenshots are disabled.");
        }
    });

    // Attempt to prevent some screenshot methods
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.altKey) && e.key === 'PrintScreen') {
            e.preventDefault();
            alert('Screenshots are not allowed on this page.');
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'PrintScreen') {
            alert('Screenshots are not allowed on this page.');
        }
    });
}

document.getElementById('link').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default anchor click behavior
    
    const target = document.querySelector('#favorites');
    target.scrollIntoView({
      behavior: 'smooth',     // Smooth scrolling
      block: 'center'         // Scroll to the center of the screen
    });
  });

  document.getElementById('gallerylink').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default anchor click behavior
    
    const target = document.querySelector('#gallery');
    target.scrollIntoView({
      behavior: 'smooth',     // Smooth scrolling
      block: 'center'         // Scroll to the center of the screen
    });
  });