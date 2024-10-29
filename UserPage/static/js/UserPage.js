let selectedImages = JSON.parse(localStorage.getItem('selectedImages')) || [];
let currentPage = 1;
const imagesPerPage = 8;
let images = []; // This will hold the images from the server
let isImagesLoaded = false; // Flag to track loading state
let allowDownloads = false;


async function fetchUserImages(page = 1, callback) {
    try {
        currentPage = page; // Update currentPage here
        // console.log('current page:', currentPage);
        
        const response = await fetch('/fetch-user-images/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ page }) // Use `page` instead of `currentPage`
        });

        if (response.ok) {
            const data = await response.json();
            // console.log(data);
            allowDownloads = data.allow_to_download;
            images = data.images;
            // console.log("Fetched images:", images);
            // console.log("Image IDs:", images.map(img => img.id));
            isImagesLoaded = true;

            displayImages(currentPage);
            setupPagination(data.total_pages);

            // Call callback if provided and images loaded successfully
            if (callback) {
                callback();
            }
        } else {
            // console.error('Error fetching images:', response.statusText);
        }
    } catch (error) {
        // console.error('Fetch error:', error);
    }
}


// Setup pagination buttons with active state
function setupPagination(totalPages) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = ""; // Clear existing buttons

    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement("button");
        pageButton.innerText = i;
        pageButton.className = "page-btn";
        if (i === currentPage) pageButton.classList.add("active");

        pageButton.addEventListener("click", () => {
            fetchUserImages(i, updateSelectedImagesContainer); // Fetch for specific page i
            // console.log('page button', i);
        });

        pagination.appendChild(pageButton);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchUserImages(1, updateSelectedImagesContainer); // Initial fetch for page 1
});




window.onload = function () {
   
    preventRightClick();
    preventScreenshots();
  
};


// Function to display images on the current page
function displayImages(page) {
    // console.log("DisplayImagesPage:", page);
    const imageContainer = document.getElementById("imageContainer");
    imageContainer.innerHTML = "";
    const currentImages = images;
    // console.log("DisplayImagescurrentimages", currentImages);
    
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
        downloadTooltip.textContent =allowDownloads ?'Download' : 'Download Disabled';
        downloadContainer.appendChild(downloadIcon);
        downloadContainer.appendChild(downloadTooltip);
        downloadIcon.style.opacity = allowDownloads ? '1' : '0.5'; // Adjust visibility
        downloadIcon.style.pointerEvents = allowDownloads ? 'auto' : 'none'; // Disable interaction
        downloadIcon.style.cursor=allowDownloads ? 'pointer':'not-allowed';
        buttonGroup.appendChild(heartContainer);
        buttonGroup.appendChild(viewContainer);
        buttonGroup.appendChild(downloadContainer);

        imageBox.appendChild(img);
        imageBox.appendChild(buttonGroup);

        imageContainer.appendChild(imageBox);
    });

    // Add event listeners for heart icons after rendering
    addHeartEventListeners();
    updateHeartIcons(selectedImages)
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


function updateSelectedImagesContainer() {
    // console.log("Current images array:", images);
    
    // Check if images are loaded
    if (!isImagesLoaded || images.length === 0) {
        // console.warn("Images array is empty or not yet loaded when trying to update selected images.");
        return;
    }

    const selectedImagesContainer = document.getElementById('selectedImagesContainer');
    selectedImagesContainer.innerHTML = ''; // Clear previous images

    // If no images selected
    if (selectedImages.length === 0) {
        selectedImagesContainer.innerHTML = '<p class="no-images">No images selected</p>';
    } else {
        // console.log("Selected images IDs:", selectedImages);
        selectedImages.forEach(imageId => {
            // Convert imageId to Number for comparison if necessary
            const image = images.find(img => img.id === Number(imageId)); // Ensure types match
            if (image) {
                const imageBox = createImageBox(image);
                selectedImagesContainer.appendChild(imageBox);
            } else {
                // console.warn(`Image with ID: ${imageId} not found in images array`);
            }
        });
    }
}





// Helper function to create an image box with controls
function createImageBox(image) {
    // console.log("Found image:", image); // Debug log

    const imageBox = document.createElement('div');
    imageBox.classList.add('image-box', 'selected-image');
    imageBox.setAttribute('data-id', image.id);

    // Image Element with Lazy Loading
    const img = document.createElement('img');
    img.src = image.src;
    img.alt = image.alt;
    img.loading = 'lazy';
    img.addEventListener('contextmenu', e => e.preventDefault()); // Disable right-click menu

    // Button Group
    const buttonGroup = document.createElement('div');
    buttonGroup.classList.add('button-group');

    // View, Download, and Remove Buttons
    buttonGroup.appendChild(createIconButton('view-icon', 'fas fa-eye', 'View', () => viewImage(img.src)));
     // Conditionally create the Download button if downloads are allowed
     if (allowDownloads) {
        buttonGroup.appendChild(createIconButton('download-icon', 'fas fa-download', 'Download', () => downloadImage(img.src)));
    } else {
        // If downloads aren't allowed, create a disabled download icon for visual feedback
        const downloadButton = createIconButton('download-icon', 'fas fa-download', 'Download Disabled');
        downloadButton.style.opacity = '0.5';
        downloadButton.style.pointerEvents = 'none';
        downloadButton.style.cursor='not-allowed';
        // downloadButton.style.border='1px solid black';
        buttonGroup.appendChild(downloadButton);
    }
    buttonGroup.appendChild(createIconButton('remove-icon', 'fas fa-times', 'Remove', () => removeSelectedImage(image.id)));

    imageBox.appendChild(img);
    imageBox.appendChild(buttonGroup);

    return imageBox;
}

// Update createIconButton to include remove functionality
function createIconButton(iconClass, fontAwesomeClass, tooltipText, onClick) {
    const iconContainer = document.createElement('div');
    iconContainer.classList.add('icon-container');

    const icon = document.createElement('i');
    icon.classList.add(iconClass, ...fontAwesomeClass.split(' '));
    icon.addEventListener('click', onClick);

    const tooltip = document.createElement('div');
    tooltip.classList.add('tooltip');
    tooltip.textContent = tooltipText;

    iconContainer.appendChild(icon);
    iconContainer.appendChild(tooltip);

    return iconContainer;
}


function removeSelectedImage(imageId) {
    // console.log("Removing image:", imageId);
    
    // Filter selectedImages to remove the imageId
    selectedImages = selectedImages.filter(id => id !== imageId.toString()); // Ensure id is a string
    localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
    
    // Log the current state of selectedImages after removal
    // console.log("After removal, current selected images:", selectedImages);
    
    // Update the UI to reflect the changes
    updateSelectedImagesContainer();
    
    // Update heart icon
    const imageBox = document.querySelector(`.image-box[data-id="${imageId}"]`);
    if (imageBox) {
        // console.log("Image box found:", imageBox);
        const heartIcon = imageBox.querySelector('.heart-icon');
        if (heartIcon) {
            heartIcon.classList.remove('filled'); // Change heart icon to unfilled
        }
        imageBox.classList.remove('selected'); // Remove the selected class if necessary
    } else {
        // console.log("Image box not found");
    }
}






function toggleHeartIcon(heartIcon, imageId) {
    heartIcon.classList.toggle('filled'); // Toggle filled class

    // Check if the icon is filled or not
    if (heartIcon.classList.contains('filled')) {
        if (!selectedImages.includes(imageId)) {
            selectedImages.push(imageId);
            localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
        }
    } else {
        selectedImages = selectedImages.filter(id => id !== imageId);
        localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
    }

    updateSelectedImagesContainer(); // Update selected images display
}

// Initialize selected images on page load
document.addEventListener('DOMContentLoaded', () => {
    updateSelectedImagesContainer();
    renderImages([
        { src: 'https://via.placeholder.com/150/FF0000/FFFFFF?text=Image1' },
        { src: 'https://via.placeholder.com/150/00FF00/FFFFFF?text=Image2' },
        { src: 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Image3' },
        { src: 'https://via.placeholder.com/150/FFFF00/FFFFFF?text=Image4' },
        { src: 'https://via.placeholder.com/150/FF00FF/FFFFFF?text=Image5' }
    ]);
});

// Function to render images
function renderImages(images) {
    const imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = ''; // Clear existing images

    images.forEach(image => {
        const imageBox = document.createElement('div');
        imageBox.classList.add('image-box');
        imageBox.setAttribute('data-id', image.src); // Use image src as ID

        const imgElement = document.createElement('img');
        imgElement.src = image.src; // Assuming image object has a 'src' property
        imgElement.alt = 'Image';

        const heartIcon = document.createElement('i');
        heartIcon.classList.add('fa', 'fa-heart', 'heart-icon'); // Changed to heart-icon
        heartIcon.addEventListener('click', () => toggleHeartIcon(heartIcon, image.src)); // Use the image src as ID

        imageBox.appendChild(imgElement);
        imageBox.appendChild(heartIcon);
        imageContainer.appendChild(imageBox);
    });
}

// Function to save selection
async function saveSelection() {
    if (selectedImages.length === 0) {
        alert("No images selected to save.");
        return;
    }

    // Log the selected image IDs for debugging
    // console.log('Selected image IDs:', selectedImages);

    try {
        const response = await fetch('/save-selected-images/', { // Replace with your backend URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Ensure you have CSRF token
            },
            body: JSON.stringify({ imageIds: selectedImages }) // Send the selected image IDs
        });

        if (response.ok) {
            const result = await response.json();
            // console.log('Response from server:', result);
            alert('Selected images saved successfully!');
        } else {
            console.error('Error saving images:', response.statusText);
            alert('Failed to save images. Please try again.');
        }
    } catch (error) {
        // console.error('Error:', error);
        alert('An error occurred while saving images. Please check your connection and try again.');
    }
}


// Example function to get CSRF token (for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the given name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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



function updateHeartIcons(selectedImages) {
    // console.log("updateHeartIcons"); // Log to indicate function execution
    selectedImages.forEach(id => {
        // Corrected selector for .image-box with data-id attribute
        const imageBox = document.querySelector(`.image-box[data-id="${id}"]`);
        // console.log(`Looking for image box with ID: ${id}`, "Found:", imageBox);
        if (imageBox) {
            const heartIcon = imageBox.querySelector('.heart-icon');
            if (heartIcon) {
                heartIcon.classList.add('filled'); // Change heart icon to filled
                // console.log("Success: Heart icon filled for ID", id); // Log success message
            }
            imageBox.classList.add('selected'); // Add selected class if necessary
        } else {
            // console.error(`No image box found for ID: ${id}`); // Log error if not found
        }
    });
}


// Function to prevent screenshot functionality
function preventScreenshots() {
    // console.log("fuction calleld prevents")
    document.addEventListener('keydown', function (e) {
        // Preventing PrintScreen key and common shortcuts
        if (e.key === 'PrintScreen' || (e.ctrlKey && (e.key === 'p' || e.key === 's'))) {
            e.preventDefault();
            overlay.style.display = 'block'; // Show the overlay
            setTimeout(() => {
                overlay.style.display = 'none'; // Hide the overlay after 2 seconds
            }, 2000);
            alert("Screenshots are disabled.");
        }
    });

    // Additional attempts to prevent common screenshot methods
    document.addEventListener('keyup', function (e) {
        if (e.key === 'PrintScreen') {
            e.preventDefault();
            overlay.style.display = 'block'; // Show the overlay
            setTimeout(() => {
                overlay.style.display = 'none'; // Hide the overlay after 2 seconds
            }, 2000);
            alert('Screenshots are not allowed on this page.');
        }
    });
}

// Call the function
preventScreenshots();
