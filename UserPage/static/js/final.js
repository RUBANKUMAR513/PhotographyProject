
setInterval(changeReview, 5000); // Change review every 5 seconds

const reviews = [
    {
        text: '"Photography is the story I fail to put into words."',
        author: '- John Doe',
        backgroundImage: 'url("marriage.jpg")' // Set background image URL
    },
    {
        text: '"Every picture tells a story, and your photos are the best."',
        author: '- Jane Smith',
        backgroundImage: 'url("marriage1.jpg")'
    },
    {
        text: '"Your eye for detail is impressive; thank you for capturing our special day!"',
        author: '- Michael Johnson',
        backgroundImage: 'url("marriage2.jpg")'
    },
    {
        text: '"Amazing photos! You truly captured the essence of the event."',
        author: '- Sarah Brown',
        backgroundImage: 'url("marriage3.jpg")'
    },
    {
        text: '"The photos are breathtaking. We couldn’t be happier!"',
        author: '- Emily White',
        backgroundImage: 'url("marriage4.jpg")'
    }
];

let ActualIndex = 0;

function changeReview() {
    const reviewText = document.getElementById('reviewText');
    const quoteAuthor = document.querySelector('.quote-author');
    const quoteContainer = document.querySelector('.quote-container');

    // Update text and author
    reviewText.innerText = reviews[ActualIndex].text;
    quoteAuthor.innerText = reviews[ActualIndex].author;

    // Update background image
    quoteContainer.style.backgroundImage = reviews[ActualIndex].backgroundImage;

    // Loop back to the first review
    ActualIndex = (ActualIndex + 1) % reviews.length;
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
document.addEventListener("DOMContentLoaded", function() {
    const aboutSection = document.querySelector('.about-section');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                aboutSection.classList.add('reveal'); // Add reveal class to trigger animation
            }
        });
    }, {
        threshold: 0.1 // Trigger when 10% of the section is visible
    });

    observer.observe(aboutSection); // Observe the about-section
});

let currentSlide = 0;
const slides = document.getElementById('slides');
const totalSlides = document.querySelectorAll('.slide').length;

function showSlide(index) {
    // Loop back if index goes out of bounds
    if (index >= totalSlides) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = totalSlides - 1;
    } else {
        currentSlide = index;
    }

    // Move slides using translateX
    const offset = -currentSlide * 100; // Move by 100% per slide
    slides.style.transform = `translateX(${offset}vw)`;
}

function moveSlide(direction) {
    showSlide(currentSlide + direction);
}

// Auto slide every 3 seconds
setInterval(() => {
    moveSlide(1);
}, 3000); // Change slide every 3 seconds

// Manual controls using buttons (left/right)
document.querySelector('.prev').addEventListener('click', () => {
    moveSlide(-1);
});

document.querySelector('.next').addEventListener('click', () => {
    moveSlide(1);
});


const workSlider = document.querySelector('.recent-work-slider');
const workSlides = document.querySelectorAll('.recent-work-slide');
const nextButton = document.querySelector('.next-btn');
const prevButton = document.querySelector('.prev-btn');
const imageModal = document.getElementById("imageModal");
const modalImage = document.getElementById("fullImage");
const modalCaption = document.getElementById("caption");
const closeButton = document.querySelector(".closebtn");

let currentIndex = 0;
let slideWidth = 210; // Width of each slide
let visibleSlides = 5; // Number of slides visible at a time

function openFullScreen(image, captionText) {
    const modal = document.getElementById("imageModal");
    const fullImage = document.getElementById("fullImage");
    const caption = document.getElementById("caption");

    fullImage.src = image;
    caption.innerHTML = captionText;
    modal.style.display = "block";
}

document.querySelector(".closebtn").onclick = function() {
    document.getElementById("imageModal").style.display = "none";
}

function moveSlider(direction) {
    const totalSlides = document.querySelectorAll('.recent-work-slide').length;

    currentIndex += direction;

    // Boundary checks
    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex > totalSlides - visibleSlides) {
        currentIndex = totalSlides - visibleSlides;
    }

    const slider = document.getElementById("slider");
    slider.style.transform = `translateX(-${currentIndex * slideWidth}px)`; // Move slider

    updateButtonStates(totalSlides); // Update button states after moving
}

// Update slide configuration based on screen size
function updateSlideConfig() {
    const screenWidth = window.innerWidth;

    // Adjust slide dimensions and visible slides based on screen size
    if (screenWidth <= 480) {
        slideWidth = 110; // Adjust width for small screens
        visibleSlides = 4.5; // Fewer visible slides
    } else if (screenWidth <= 768) {
        slideWidth = 160; // Medium screen adjustment
        visibleSlides = 7; // More slides visible than small screens
    } else {
        slideWidth = 210; // Original setting for larger screens
        visibleSlides = 6.5; // Original setting for larger screens
    }

    // Reset currentIndex to fit within new boundaries
    const totalSlides = document.querySelectorAll('.recent-work-slide').length;
    currentIndex = Math.min(currentIndex, totalSlides - visibleSlides);

    moveSlider(0); // Reset slider position to accommodate new settings
}

window.onload = () => {
    updateSlideConfig(); // Call initially
    moveSlider(0); // Reset slider position to accommodate new settings
    updateButtonStates(document.querySelectorAll('.recent-work-slide').length); // Initialize button states
};

window.onresize = () => {
    updateSlideConfig(); // Update on screen resize
};

// Update button states based on current index
function updateButtonStates(totalSlides) {
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    // Disable the previous button if at the first slide
    prevBtn.disabled = currentIndex === 0;

    // Disable the next button if the last set of images is fully visible
    nextBtn.disabled = currentIndex >= totalSlides - visibleSlides;
}


document.getElementById("learnMoreBtn").addEventListener("click", function() {
    var infoSection = document.getElementById("photographerInfo");

    // Toggle the display of the section
    if (infoSection.style.display === "none" || infoSection.style.display === "") {
        infoSection.style.display = "flex";  // Show the section
    } else {
        infoSection.style.display = "none";  // Hide the section
    }
});







