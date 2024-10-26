document.addEventListener('DOMContentLoaded', function () {
    console.log("Attempting to find elements...");

    // Wait for the specific input field to be available
    const checkInputInterval = setInterval(() => {
        const mainInput = document.getElementById('id_photo');

        if (mainInput) {
            console.log("Main photo input field found.");
            clearInterval(checkInputInterval); // Stop checking once found
            
            // Set the 'multiple' attribute to true
            mainInput.multiple = true; // Allow multiple files
            console.log("The 'multiple' attribute has been set to true.");

            // Add an event listener for file selection
            mainInput.addEventListener('change', function(event) {
                const files = event.target.files; // Get selected files
                const fileNames = Array.from(files).map(file => file.name); // Map to file names
                console.log('Selected files:', fileNames); // Log selected file names
            });
        }
    }, 100); // Check every 100ms
});
