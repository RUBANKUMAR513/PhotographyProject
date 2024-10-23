let currentImageIndex = 0;
let currentGalleryImages = [];

// Open modal and display clicked image in full screen
function openModal(image) {
    const modal = document.getElementById("modal");
    modal.classList.add("active");

    const galleryItem = image.closest('.carousel');
    currentGalleryImages = Array.from(galleryItem.getElementsByClassName('carousel-image'));
    currentImageIndex = currentGalleryImages.indexOf(image);
    updateModalImage();
}

// Close modal
function closeModal() {
    document.getElementById("modal").classList.remove("active");
}

// Display next image in modal
function nextModalImage() {
    currentImageIndex = (currentImageIndex + 1) % currentGalleryImages.length;
    updateModalImage();
}

// Display previous image in modal
function prevModalImage() {
    currentImageIndex = (currentImageIndex - 1 + currentGalleryImages.length) % currentGalleryImages.length;
    updateModalImage();
}

// Update modal image source
function updateModalImage() {
    const modalImage = document.getElementById("modalImage");
    modalImage.src = currentGalleryImages[currentImageIndex].src;
}

const menuBtn = document.getElementById('menuBtn');
const closeBtn = document.getElementById('closeBtn');
const sidebar = document.getElementById('sidebar');
const sidebarItems = sidebar.querySelectorAll('li'); // Select all the li elements in the sidebar

menuBtn.addEventListener('click', () => {
sidebar.classList.add('open');
menuBtn.classList.add('hidden');
closeBtn.classList.add('visible');
});

closeBtn.addEventListener('click', () => {
sidebar.classList.remove('open');
menuBtn.classList.remove('hidden');
closeBtn.classList.remove('visible');
});

// Add event listener to each li element to close the sidebar when clicked
sidebarItems.forEach(item => {
item.addEventListener('click', () => {
sidebar.classList.remove('open');
menuBtn.classList.remove('hidden');
closeBtn.classList.remove('visible');
});
});

// Add event listener to close the sidebar when clicking on the main content
home.addEventListener('click', () => {
if (sidebar.classList.contains('open')) {
sidebar.classList.remove('open');
menuBtn.classList.remove('hidden');
closeBtn.classList.remove('visible');
}
});

// Add event listener to close the sidebar when scrolling the window
window.addEventListener('scroll', () => {
if (sidebar.classList.contains('open')) {
sidebar.classList.remove('open');
menuBtn.classList.remove('hidden');
closeBtn.classList.remove('visible');
}
});