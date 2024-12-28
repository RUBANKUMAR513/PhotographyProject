setInterval(changeReview, 5000); // Change review every 5 seconds

let ActualIndex = 0;

function changeReview() {
    const reviewText = document.getElementById('reviewText');
    const quoteAuthor = document.querySelector('.quote-author');
    const quoteContainer=document.querySelector('.quote-container');
    const cartoonImage = document.getElementById('cartoonImage');

    // Use Fetch API to get data from the Django backend
    fetch('/get-happy-clients/', {  // Ensure this matches your URL pattern
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
        },
        body: JSON.stringify({}) // Body can be empty if no data is needed
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error:", data.error);
            reviewText.innerText = "Error loading reviews.";
            quoteAuthor.innerText = "";
        } else {
            const review = data[ActualIndex];
            reviewText.innerText = review.text;
            quoteAuthor.innerText = review.author;
            cartoonImage.src = review.cartoon_image; // Assuming the response includes a `cartoon_image` field
             // Change the background of the quote container with the fetched image
             quoteContainer.style.backgroundImage = `url('${review.image}')`; // Assuming the response includes an `image` field

            // Loop back to the first review
            ActualIndex = (ActualIndex + 1) % data.length;
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
        reviewText.innerText = "Error loading reviews.";
        quoteAuthor.innerText = "";
    });
}


// Call changeReview immediately to load the first review
changeReview();

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


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















