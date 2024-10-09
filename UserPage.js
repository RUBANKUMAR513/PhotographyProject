let selectedImages = JSON.parse(localStorage.getItem('selectedImages')) || [];

window.onload = function () {
    document.querySelectorAll('.image-box').forEach(imageBox => {
        const imageId = imageBox.getAttribute('data-id');
        const heartIcon = imageBox.querySelector('.heart-icon');

        if (selectedImages.includes(imageId)) {
            imageBox.classList.add('selected');
            heartIcon.classList.add('filled');
        } else {
            heartIcon.classList.remove('filled');
        }
     // Prevent right-click context menu on the image
     const image = imageBox.querySelector('img');
        image.addEventListener('contextmenu', function (e) {
            e.preventDefault();
        });
    });
    
    // Prevent right-click context menu on the image container
    document.getElementById('imageContainer').addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });
    // Prevent right-click context menu on the selected images container
    document.getElementById('selectedImagesContainer').addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });
    updateSelectedImagesContainer();
};


document.getElementById('imageContainer').addEventListener('click', function (e) {
    if (e.target.classList.contains('heart-icon')) {
        const clickedBox = e.target.closest('.image-box');
        const imageId = clickedBox.getAttribute('data-id');
        const heartIcon = clickedBox.querySelector('.heart-icon');

        if (clickedBox.classList.contains('selected')) {
            clickedBox.classList.remove('selected');
            heartIcon.classList.remove('filled');
            selectedImages = selectedImages.filter(id => id !== imageId);
        } else {
            clickedBox.classList.add('selected');
            heartIcon.classList.add('filled');
            selectedImages.push(imageId);
        }

        localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
        updateSelectedImagesContainer();
    }
});

function updateSelectedImagesContainer() {
const selectedImagesContainer = document.getElementById('selectedImagesContainer');
selectedImagesContainer.innerHTML = '';

if (selectedImages.length === 0) {
selectedImagesContainer.innerHTML = '<p class="no-images">No images selected</p>';
} else {
selectedImages.forEach(imageId => {
    const imageBox = document.querySelector(`.image-box[data-id="${imageId}"]`).cloneNode(true);
    imageBox.classList.add('selected-image');
    imageBox.querySelector('i.heart-icon').remove();

    // Create a remove icon container
    const iconContainer = document.createElement('div');
    iconContainer.classList.add('icon-container');

    // Create a remove icon
    const removeIcon = document.createElement('i');
    removeIcon.classList.add('remove-icon', 'fas', 'fa-times');
    removeIcon.addEventListener('click', () => removeSelectedImage(imageId));

    // Create a tooltip for the remove icon
    const removeTooltip = document.createElement('div');
    removeTooltip.classList.add('tooltip');
    removeTooltip.textContent = 'Remove';

    // Append the tooltip and icon to the icon container
    iconContainer.appendChild(removeIcon);
    iconContainer.appendChild(removeTooltip);

    // Append the icon container to the button group
    imageBox.querySelector('.button-group').appendChild(iconContainer);

    selectedImagesContainer.appendChild(imageBox);
});
}
}

function removeSelectedImage(imageId) {
    selectedImages = selectedImages.filter(id => id !== imageId);
    localStorage.setItem('selectedImages', JSON.stringify(selectedImages));
    updateSelectedImagesContainer();

    const originalImageBox = document.querySelector(`.image-box[data-id="${imageId}"]`);
    const heartIcon = originalImageBox.querySelector('.heart-icon');
    originalImageBox.classList.remove('selected');
    heartIcon.classList.remove('filled');
}

function saveSelection() {
    alert("Selected images saved!");
    // Implement save functionality here (e.g., send to server)
}

function viewImage(imageUrl) {
    const fullscreenOverlay = document.getElementById('fullscreenOverlay');
    const fullscreenImage = document.getElementById('fullscreenImage');

    fullscreenImage.src = imageUrl;
    fullscreenOverlay.style.display = 'flex';
    // Prevent right-click context menu on fullscreen image
    fullscreenImage.addEventListener('contextmenu', function (e) {
        e.preventDefault();
    });
}

function closeFullscreen() {
    const fullscreenOverlay = document.getElementById('fullscreenOverlay');
    fullscreenOverlay.style.display = 'none';
}

function downloadImage(imageUrl) {
const a = document.createElement('a');
a.href = imageUrl; // Directly set the file URL
a.download = imageUrl.split('/').pop(); // Get the filename
document.body.appendChild(a);
a.click();
document.body.removeChild(a);

alert("Download initiated for " + a.download); // Feedback to user
}