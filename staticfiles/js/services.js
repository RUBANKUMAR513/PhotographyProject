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
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    
    // Iterate over all toggle buttons
    toggleButtons.forEach(button => {
        const serviceContent = button.closest('.service-content');
        const extraContent = serviceContent.querySelector('.extra-content');
        const seeMoreButton = serviceContent.querySelector('.see-more');
        const seeLessButton = serviceContent.querySelector('.see-less');

        // Check if extra content is empty when the page loads
        const extraContentText = extraContent ? extraContent.textContent.trim() : '';
        if (extraContentText === '') {
            console.log("extra empty on page load");
            // If there's no extra content, hide the buttons and stop functionality
            seeMoreButton.style.display = 'none';
            seeLessButton.style.display = 'none';
            return; // Exit the function early
        }

        // If extra content exists, set up the toggle functionality
        button.addEventListener('click', function () {
            if (extraContent && seeMoreButton && seeLessButton) {
                const isVisible = extraContent.style.display === 'block';

                // Toggle visibility of extra content
                if (isVisible) {
                    extraContent.style.display = 'none';
                    seeMoreButton.style.display = 'inline'; // Show 'See More'
                    seeLessButton.style.display = 'none'; // Hide 'See Less'
                } else {
                    extraContent.style.display = 'block';
                    seeMoreButton.style.display = 'none'; // Hide 'See More'
                    seeLessButton.style.display = 'inline'; // Show 'See Less'
                }
            }
        });
    });
});





