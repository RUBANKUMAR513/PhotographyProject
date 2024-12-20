let images = [];
let selectedImages = [];
let currentPage = 1;
let isImagesLoaded = false;
let allowDownloads = true;

// Fetch and display images
async function fetchUserImages(page = 1) {
    try {
        currentPage = page;
        const response = await fetch('/fetch-user-images/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ page })
        });

        if (response.ok) {
            const data = await response.json();
            allowDownloads = data.allow_to_download;
            images = data.images;
            displayImages(currentPage);
            setupPagination(data.total_pages,page);
        } else {
            console.error('Error fetching images:', response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Fetch favorite images from the database
async function fetchFavorites() {
    try {
        const response = await fetch('/favorites/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Fetched favorites:', data);

            // Populate selectedImages with valid image IDs from the response
            selectedImages = data.favorites.map(fav => fav.image__id);  // Ensure image__id is correctly accessed
            
            console.log("selectedImages after fetching:", selectedImages);
            
            // Now fill the heart icons
            fillHeartIcons();
            // Update the UI to reflect the current favorites
            updateSelectedImagesContainer(data.favorites);
        } else {
            console.error('Failed to fetch favorites:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching favorites:', error);
    }
}

window.addEventListener('load', function() {
    // Fetch favorite images and ensure heart icons are filled on page load
    fetchFavorites();
});

function fillHeartIcons() {
    console.log("fillhearticons are called")
    console.log("selectedImages:",selectedImages)
    // Find all image boxes and check if they are in the selectedImages array
    document.querySelectorAll('.image-box').forEach(imageBox => {
        const imageId = imageBox.getAttribute('data-id');
        console.log("fillhearticons are called",imageId)
        const heartIcon = imageBox.querySelector('.heart-icon');
        console.log("fillhearticons are called hearticon",heartIcon)
        // Check if the image is selected
        if (selectedImages.includes(Number(imageId))) {
            console.log("fillhearticons are called if")
            heartIcon.classList.add('filled'); // Fill the heart icon
            imageBox.classList.add('selected'); // Add selected class to the image box
        }
    });
}
// Display images on the page
function displayImages(page) {
    const imageContainer = document.getElementById("imageContainer");
    imageContainer.innerHTML = "";

    images.forEach(image => {
        const imageBox = document.createElement('div');
        imageBox.classList.add('image-box');
        imageBox.setAttribute('data-id', image.id);

        const img = document.createElement('img');
        img.src = image.src;
        img.alt = image.alt;

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
        downloadTooltip.textContent = allowDownloads ? 'Download' : 'Download Disabled';
        downloadContainer.appendChild(downloadIcon);
        downloadContainer.appendChild(downloadTooltip);
        downloadIcon.style.opacity = allowDownloads ? '1' : '0.5';
        downloadIcon.style.pointerEvents = allowDownloads ? 'auto' : 'none';
        downloadIcon.style.cursor = allowDownloads ? 'pointer' : 'not-allowed';
        buttonGroup.appendChild(heartContainer);
        buttonGroup.appendChild(viewContainer);
        buttonGroup.appendChild(downloadContainer);

        imageBox.appendChild(img);
        imageBox.appendChild(buttonGroup);

        imageContainer.appendChild(imageBox);
    });

    addHeartEventListeners();
}


// Add heart icon event listeners
function addHeartEventListeners() {
    document.querySelectorAll('.heart-icon').forEach(icon => {
        icon.addEventListener('click', function (e) {
            e.stopPropagation();
            const imageBox = this.closest('.image-box');
            const imageId = imageBox.getAttribute('data-id');
            
            // Check if the heart is filled (meaning it is currently a favorite)
            if (this.classList.contains('filled')) {
                console.log("this is statisfy remove")
                // Remove from favorites and unfill the heart icon
                this.classList.remove('filled');
                imageBox.classList.remove('selected');
                console.log("Removed from favorites:", imageId);

                // Remove imageId from selectedImages
                selectedImages = selectedImages.filter(id => id !== imageId);
                updateFavoriteImage(imageId, 'remove'); // Update backend to reflect removal
            } else {
                console.log("this is statisfy add")
                // Add to favorites and fill the heart icon
                this.classList.add('filled');
                imageBox.classList.add('selected');
                console.log("Added to favorites:", imageId);

                // Add imageId to selectedImages
                selectedImages.push(imageId);
                updateFavoriteImage(imageId, 'add'); // Update backend to reflect addition
            }

            updateSelectedImagesContainer(); // Update UI with current selection
        });
    });
}




// Update favorites on the backend
async function updateFavoriteImage(imageId, action) {
    try {
        const response = await fetch(`/favorites/${action}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ image_id: imageId })
        });

        if (response.ok) {
            console.log(action === 'add' ? 'Image added to favorites' : 'Image removed from favorites');
            updateSelectedImagesContainer();
        } else {
            console.error('Failed to update favorites');
        }
    } catch (error) {
        console.error('Error updating favorites:', error);
    }
}

// Update the selected images container
async function updateSelectedImagesContainer() {
    const selectedImagesContainer = document.getElementById('selectedImagesContainer');
    selectedImagesContainer.innerHTML = '';

    try {
        const response = await fetch('/favorites/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        });

        if (response.ok) {
            const data = await response.json();
            const favorites = data.favorites;
            console.log("fav:",favorites)
            console.log("data:",data)
            if (favorites.length === 0) {
                selectedImagesContainer.innerHTML = '<p class="no-images">No images selected</p>';
            } else {
                favorites.forEach(favorite => {
                    const imageBox = createImageBox(favorite);
                    selectedImagesContainer.appendChild(imageBox);
                });
            }
        } else {
            console.error('Failed to fetch selected images:', response.statusText);
            selectedImagesContainer.innerHTML = '<p class="no-images">Error fetching images</p>';
        }
    } catch (error) {
        console.error('Error fetching selected images:', error);
    }
    
}

// Function to create an image box for selected images
function createImageBox(image) {
    console.log("image on createimagebox:",image)
    // Debugging output for validation
    // console.log("Creating image box for:", image);

    // Main container for the image box
    const imageBox = document.createElement('div');
    imageBox.classList.add('image-box', 'selected-image');
    imageBox.setAttribute('data-id', image.image__id);
    const imageId = imageBox.getAttribute('data-id'); // Retrieve image ID

    // Create the image element
    const img = document.createElement('img');
    img.src = image.src; // Image source URL
    img.alt = image.alt || 'Image'; // Alt text for accessibility
    img.loading = 'lazy'; // Enable lazy loading for performance
    img.addEventListener('contextmenu', e => e.preventDefault()); // Disable right-click menu

    // Create a container for buttons (Button Group)
    const buttonGroup = document.createElement('div');
    buttonGroup.classList.add('button-group');

    // Add "View" button
    buttonGroup.appendChild(createIconButton('view-icon', 'fas fa-eye', 'View', () => viewImage(img.src)));

    // Conditionally add "Download" button
    if (typeof allowDownloads !== 'undefined' && allowDownloads) {
        buttonGroup.appendChild(
            createIconButton('download-icon', 'fas fa-download', 'Download', () => downloadImage(img.src))
        );
    } else {
        // Create a disabled "Download" button if downloads are not allowed
        const downloadButton = createIconButton('download-icon', 'fas fa-download', 'Download Disabled');
        downloadButton.style.opacity = '0.5';
        downloadButton.style.pointerEvents = 'none'; // Disable interaction
        downloadButton.style.cursor = 'not-allowed'; // Change cursor to indicate non-clickable
        buttonGroup.appendChild(downloadButton);
    }

    // Add "Remove" button
    buttonGroup.appendChild(
        createIconButton(
            'remove-icon', 
            'fas fa-times', 
            'Remove', 
            () => {
                // Perform backend update
                updateFavoriteImage(imageId, 'remove');
    
                // Remove the filled heart icon and selected class from the image
                const imageBox = document.querySelector(`.image-box[data-id="${imageId}"]`);
                if (imageBox) {
                    const heartIcon = imageBox.querySelector('.heart-icon');
                    if (heartIcon && heartIcon.classList.contains('filled')) {
                        heartIcon.classList.remove('filled'); // Unfill the heart icon
                        imageBox.classList.remove('selected'); // Remove selection highlight
                    }
                }
    
                // Optional: Update any UI elements or arrays that track favorites
                selectedImages = selectedImages.filter(id => id !== imageId);
                updateSelectedImagesContainer(); // Update UI with current selection
            }
        )
    );
    

    // Append the image and button group to the main container
    imageBox.appendChild(img);
    imageBox.appendChild(buttonGroup);

    // Return the completed image box
    return imageBox;
}


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


function setupPagination(totalPages, currentPage = 1) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // Clear existing pagination buttons

    const maxVisibleButtons = 5; // Max buttons visible
    let startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

    if (endPage - startPage < maxVisibleButtons - 1) {
        startPage = Math.max(1, endPage - maxVisibleButtons + 1);
    }

    // Add "Previous" button
    if (currentPage > 1) {
        const prevButton = createPaginationButton('Previous', currentPage - 1, totalPages);
        pagination.appendChild(prevButton);
    }

    // Add page buttons
    for (let i = startPage; i <= endPage; i++) {
        const button = createPaginationButton(i, i, totalPages, i === currentPage);
        pagination.appendChild(button);
    }

    // Add "Next" button
    if (currentPage < totalPages) {
        const nextButton = createPaginationButton('Next', currentPage + 1, totalPages);
        pagination.appendChild(nextButton);
    }
}

function createPaginationButton(text, page, totalPages, isActive = false) {
    const button = document.createElement('button');
    button.textContent = text;
    button.className = 'page-btn';
    if (isActive) button.classList.add('active');
    button.addEventListener('click', () => {
        fetchUserImages(page);
        setupPagination(totalPages, page);
        scrollToActiveButton(button); // Scroll to the active button
    });
    return button;
}

function scrollToActiveButton(button) {
    const container = document.getElementById('pagination');
    const containerRect = container.getBoundingClientRect();
    const buttonRect = button.getBoundingClientRect();

    // Scroll the container to center the active button
    container.scrollLeft += buttonRect.left - containerRect.left - container.clientWidth / 2 + buttonRect.width / 2;
}


async function saveSelection() {

    if (selectedImages.length === 0) {
        console.log("No images selected.");  // Log if no images are selected
        showPopupMessage("No images selected to save.", false);  // Show red popup for no selection
        return;
    }

    console.log("Selected image IDs:", selectedImages);  // Log the selected image IDs

    try {
        const response = await fetch('/save-selected-images/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), 
            },
            body: JSON.stringify({ imageIds: selectedImages })  // Send the selected image IDs
        });

        console.log("Server response:", response);  // Log the response object

        if (response.ok) {
            const result = await response.json();
            console.log("Server response JSON:", result);  // Log the result from the server
            showPopupMessage("Selected images saved successfully!", true);  // Green popup for success
            const submitButton = document.getElementById('submit-button');

            // Disable the button and start the cooldown
            submitButton.disabled = true;

            // Countdown from 10 seconds
            let countdown = 10;
            const originalText = submitButton.textContent;
            const interval = setInterval(() => {
                submitButton.textContent = `Please wait... (${countdown}s)`;
                countdown--;

                if (countdown < 0) {
                    clearInterval(interval); // Stop the countdown
                    submitButton.disabled = false; // Re-enable the button
                    submitButton.textContent = originalText; // Restore original text
                }
            }, 1000);

        } else {
            console.error('Error saving images:', response.statusText);  // Log any errors
            showPopupMessage("Failed to save images. Please try again.", false);  // Red popup for failure
        }
    } catch (error) {
        console.error('Error during fetch request:', error);  // Log any network or server errors
        showPopupMessage("An error occurred while saving images. Please check your connection and try again.", false);  // Red popup for network errors
    }
}

function showPopupMessage(message, isSuccess) {
    const popup = document.getElementById('popup-message');
    const text = document.getElementById('popup-text');

    text.textContent = message;
    popup.style.backgroundColor = isSuccess ? 'green' : 'red'; // Green for success, red for failure
    popup.style.display = 'block';

    // Automatically hide the popup after 3 seconds
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000);
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

// Call the function on window load
window.onload = function () {
    preventRightClick();
};



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

// Helper function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) return parts.pop().split(';').shift();
}


// Initialize fetching images
fetchUserImages(currentPage);


document.addEventListener('keyup', function (e) {
    if (e.key === 'PrintScreen') {
        navigator.clipboard.writeText('').then(() => {
            alert('Screenshots are not allowed on this page.');
        }).catch(err => {
            console.error('Failed to overwrite clipboard:', err);
        });
    }
});

document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey && e.key === 'p') || // Ctrl+P
        (e.ctrlKey && e.key === 's') || // Ctrl+S
        (e.ctrlKey && e.key === 'u') || // Ctrl+U
        (e.ctrlKey && e.shiftKey && e.key === 'i')) { // Ctrl+Shift+I
        e.preventDefault();
        alert('This action is disabled.');
    }
});


document.addEventListener('keydown', function (e) {
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        alert('Developer tools are disabled.');
    }
});
