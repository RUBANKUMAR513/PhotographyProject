document.getElementById('send-otp-btn').addEventListener('click', function() {
    const sendOtpBtn = this;
    let timer = 30; // Countdown timer set to 30 seconds
    const successMessage = document.getElementById('otp-success');
    const errorMessage = document.getElementById('otp-error');

    // Disable the button and hide any previous messages
    sendOtpBtn.disabled = true;
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';

    // Start countdown timer
    const countdown = setInterval(function() {
        timer--;
        sendOtpBtn.innerText = `Re-send OTP in ${timer}s`;

        if (timer <= 0) {
            clearInterval(countdown);
            sendOtpBtn.disabled = false;
            sendOtpBtn.innerText = "Re-send OTP";
        }
    }, 1000);
    
    // Send the AJAX request to your Django backend
    fetch('/send-otp/', { // Adjust this URL to your actual endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token if using Django CSRF protection
        },
        body: JSON.stringify({ message: 'admin trigger otp' }) // Sending the message instead of an email
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            successMessage.style.display = 'block'; // Show success message
            console.log('OTP sent successfully');
            setTimeout(function() {
                successMessage.style.display = 'none'; // Hide after 5 seconds
            }, 5000); // Hide after 5 seconds
        }
         else {
            errorMessage.style.display = 'block'; // Show error message
            console.error('Error: ' + data.message);
            setTimeout(function() {
                errorMessage.style.display = 'none'; // Hide after 5 seconds
            }, 5000); // Hide after 5 seconds
        }
    })
    .catch(error => {
        errorMessage.style.display = 'block'; // Show error message on fetch error
        console.error('Error sending OTP: ' + error);
        setTimeout(function() {
            errorMessage.style.display = 'none'; // Hide after 5 seconds
        }, 5000); // Hide after 5 seconds
    });
});

// Function to get the CSRF token from cookies (optional)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
