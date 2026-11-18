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

// === CONTACT FORM LOGIC === //
const contactForm = document.getElementById('portfolio-contact-form');
const formStatus = document.getElementById('form-status');
const submitBtn = document.getElementById('submit-btn');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending...";
        formStatus.textContent = "";

        const payload = {
            name: document.getElementById('contact-name').value,
            email: document.getElementById('contact-email').value,
            message: document.getElementById('contact-message').value
        };

        try {
            const response = await fetch(apiURL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                formStatus.style.color = "#38bdf8";
                formStatus.textContent = "Message sent! I'll get back to you soon.";
                contactForm.reset();
            } else {
                throw new Error("Server error");
            }
        } catch (error) {
            formStatus.style.color = "#f87171";
            formStatus.textContent = "Something went wrong. Please try again later.";
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Send Message";
        }
    });
}