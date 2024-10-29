document.addEventListener("DOMContentLoaded", function () {
    const services = document.querySelectorAll('.service');

    const observerOptions = {
        root: null, // Use the viewport as the root
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible'); // Add 'visible' class to the service section
                const image = entry.target.querySelector('.service-image');
                if (image) {
                    image.classList.add('visible'); // Add 'visible' class to the image
                }
                observer.unobserve(entry.target); // Stop observing the current element
            }
        });
    };

    const observer = new IntersectionObserver(observerCallback, observerOptions);
    
    services.forEach(service => {
        observer.observe(service); // Observe each service section
    });
});
// Function to open the modal and display the full-screen image
function openModal(imageElement) {
const modal = document.getElementById('fullscreenModal');
const fullscreenImage = document.getElementById('fullscreenImage');
fullscreenImage.src = imageElement.querySelector('img').src; // Set the modal image source
modal.style.display = 'flex'; // Show the modal
}

// Function to close the modal
function closeModal() {
const modal = document.getElementById('fullscreenModal');
modal.style.display = 'none'; // Hide the modal
}

