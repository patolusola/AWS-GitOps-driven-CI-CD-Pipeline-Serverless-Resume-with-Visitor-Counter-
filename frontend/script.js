// Find the button on the page
const themeBtn = document.getElementById('theme-toggle');

// Listen for a click on the button
themeBtn.addEventListener('click', () => {
    // Flip the switch: add or remove the 'light-mode' class
    document.body.classList.toggle('light-mode');
    
    // Change the button text depending on which mode is active
    if (document.body.classList.contains('light-mode')) {
        themeBtn.textContent = '🌙 Dark Mode';
    } else {
        themeBtn.textContent = '☀️ Light Mode';
    }
});