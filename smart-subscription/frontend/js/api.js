// Base API URL
// In development, this points to your local backend server
const API_URL = 'http://localhost:5001';

/**
 * Enhanced fetch wrapper that automatically handles
 * JSON parsing, Authentication headers, and standardized error throwing.
 */
async function apiCall(endpoint, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Attach JWT Token if it exists
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method,
        headers
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Something went wrong');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Helper to log out
 */
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/user/login.html';
}

/**
 * Check Authentication status and redirect if needed
 */
function requireAuth(role = null) {
    const token = localStorage.getItem('token');
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    if (!token) {
        window.location.href = '/user/login.html';
        return null;
    }

    if (role && user.role !== role) {
        // Fallback redirection if unauthorized for a specific dashboard
        alert(`Unauthorized. Requires ${role} access.`);
        window.location.href = '/index.html';
        return null;
    }

    return user;
}

// Attach to window so other scripts can access them easily
window.apiCall = apiCall;
window.logout = logout;
window.requireAuth = requireAuth;
