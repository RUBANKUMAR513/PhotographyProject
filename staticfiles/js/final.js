

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
        







