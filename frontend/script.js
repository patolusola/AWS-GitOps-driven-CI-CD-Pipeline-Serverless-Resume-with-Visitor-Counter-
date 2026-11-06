// Find the button on the page
const themeBtn = document.getElementById('theme-toggle');

// the dark and light mode toggle
themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    if (document.body.classList.contains('light-mode')) {
        themeBtn.textContent = '🌙 Dark Mode';
    } else {
        themeBtn.textContent = '☀️ Light Mode';
    }
});

// got my visitor counter here //
const apiURL = "https://uqfhs7qggjdnlilzl5t2cl7qey0bahis.lambda-url.us-east-1.on.aws/";

async function getVisitorCount() {
    console.log("1. Knocking on the Brain's door...");
    try {
        const response = await fetch(apiURL);
        console.log("2. The door opened! Raw response:", response);
        
        const data = await response.json();
        console.log("3. The data inside is:", data);
        
        document.getElementById('visitor-count').textContent = data.visit_count;
        console.log("4. Successfully updated the website!");
    } catch (error) {
        console.error("Error fetching count:", error);
        document.getElementById('visitor-count').textContent = "Error";
    }
}

getVisitorCount();