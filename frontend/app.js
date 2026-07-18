// Base URL of our Flask Backend
const API_URL = "https://resqmeal-ofhl.onrender.com";

// Simple navigation logic (Single Page App style)
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('section').forEach(sec => {
        sec.classList.remove('active-section');
        sec.classList.add('hidden-section');
    });
    
    // Show the requested section
    document.getElementById(sectionId).classList.remove('hidden-section');
    document.getElementById(sectionId).classList.add('active-section');
}

// Handle Login Form Submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page reload
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const btn = e.target.querySelector('button');
    const oldText = btn.innerText;
    btn.innerText = "Logging in...";
    
    try {
        // Send request to Flask API
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        });
        
        const data = await response.json();
        
        if (response.ok || data.message === "Login Successful") {
            // Save user details to localStorage so dashboard can use it
            localStorage.setItem("user", JSON.stringify(data.user));
            // Redirect to Dashboard seamlessly
            window.location.href = "dashboard.html";
        } else {
            alert(data.message || "Invalid Credentials");
            btn.innerText = oldText;
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Server is not running! Please start python app.py");
        btn.innerText = oldText;
    }
});

// Handle Signup Form Submission
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
    e.preventDefault(); 
    
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const role = document.getElementById('signupRole').value;
    const btn = e.target.querySelector('button');
    const oldText = btn.innerText;
    btn.innerText = "Creating Account...";
    
    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name, email: email, password: password, role: role })
        });
        
        const data = await response.json();
        
        if (response.ok || data.message === "User Registered Successfully") {
            // Instantly show login without alert
            btn.innerText = oldText;
            showSection('login');
        } else {
            alert(data.error || data.message || "Signup Failed");
            btn.innerText = oldText;
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Server is not running! Please start python app.py");
        btn.innerText = oldText;
    }
});
