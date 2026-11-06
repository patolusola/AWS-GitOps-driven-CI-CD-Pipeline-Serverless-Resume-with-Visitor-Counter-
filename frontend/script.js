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


// got my visitor counter here //

const apiURL = "https://uqfhs7qggjdnlilzl5t2cl7qey0bahis.lambda-url.us-east-1.on.aws/";

async function getVisitorCount() {
    try {
        // knock on the brain's door
        const response = await fetch(apiURL);
        const data = await response.json();
        
        // input the number on the screen
        document.getElementById('visitor-count').textContent = data.visit_count;
    } catch (error) {
        console.error("Error fetching count:", error);
    }
}

// this runs the function as soon as the website loads
getVisitorCount();