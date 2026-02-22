function updateNavigation() {
    const authContainer = document.getElementById('auth-buttons');
    const authLinks = document.querySelectorAll('.auth-only');
    const token = localStorage.getItem('access_token');

    if (token) {
        // Show protected links
        authLinks.forEach(link => link.style.display = 'inline-block');

        // Set Logout button
        authContainer.innerHTML = `<a href="#" id="logout-btn" style="color: var(--accent-red);">Log Out</a>`;
        
        document.getElementById('logout-btn').addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('access_token');
            // Use replace so they can't go "back" into the session
            window.location.replace('index.html');
        });
    } else {
        // Not logged in - Hide protected links
        authLinks.forEach(link => link.style.display = 'none');
        
        // If the user is on a protected page (like scenes.html) without a token, kick them out
        if (window.location.pathname.includes('scenes.html') || window.location.pathname.includes('profile.html')) {
            window.location.replace('login.html');
        }

        authContainer.innerHTML = `<a href="login.html" style="color: var(--accent-red);">Log in/Sign up</a>`;
    }
}

document.addEventListener('DOMContentLoaded', updateNavigation);