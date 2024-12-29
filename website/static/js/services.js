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

document.addEventListener("DOMContentLoaded", function () {
    const serviceContents = document.querySelectorAll('.service-content');
    
    serviceContents.forEach(serviceContent => {
        const extraContent = serviceContent.querySelector('.extra-content');
        const seeMoreButton = serviceContent.querySelector('.see-more');
        const seeLessButton = serviceContent.querySelector('.see-less');
        
        // Check if elements exist to avoid errors
        if (!extraContent || !seeMoreButton || !seeLessButton) {
            console.warn("Missing required elements in a service content block.");
            return;
        }

        // Check if extra content is empty
        const extraContentText = extraContent.textContent.trim();
        if (!extraContentText) {
            console.log("Extra content is empty; hiding toggle buttons.");
            seeMoreButton.style.display = 'none';
            seeLessButton.style.display = 'none';
            return;
        }

        // Initial setup: ensure extra content is hidden
        extraContent.style.display = 'none';

        // Add event listener for "See More" button
        seeMoreButton.addEventListener('click', function () {
            extraContent.style.display = 'inline'; // Show extra content
            seeMoreButton.style.display = 'none'; // Hide "See More"
            seeLessButton.style.display = 'inline'; // Show "See Less"
        });

        // Add event listener for "See Less" button
        seeLessButton.addEventListener('click', function () {
            extraContent.style.display = 'none'; // Hide extra content
            seeMoreButton.style.display = 'inline'; // Show "See More"
            seeLessButton.style.display = 'none'; // Hide "See Less"
        });
    });
});






