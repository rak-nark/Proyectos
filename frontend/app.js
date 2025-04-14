let currentToken = null;

// Función para mostrar mensajes
function showMessage(text, isError = false) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = isError ? 'error' : 'success';
    messageDiv.classList.remove('hidden');

    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 3000);
}

// Login
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            currentToken = data.token;
            document.getElementById('login-section').classList.add('hidden');
            document.getElementById('protected-section').classList.remove('hidden');
            loadProfile();
            showMessage('¡Login exitoso!');
        } else {
            showMessage(data.error || 'Error en login', true);
        }
    } catch (error) {
        showMessage('Error de conexión', true);
    }
}

// Cargar perfil
    async function loadProfile() {
        try {
            const response = await fetch('http://localhost:8080/api/profile', {
                headers: {
                    'Authorization': `Bearer ${currentToken}`,
                },
            });

            const profile = await response.json();
            document.getElementById('profile-data').textContent = 
                `Email: ${profile.profile.email}\nCuenta creada: ${new Date(profile.profile.created_at).toLocaleDateString()}`;
        } catch (error) {
            showMessage('Error al cargar perfil', true);
        }
    }

// Logout
// Login
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Guardar token en localStorage
            localStorage.setItem('jwtToken', data.token);
            // Guardar refresh token si lo usas
            if (data.refresh_token) {
                localStorage.setItem('refreshToken', data.refresh_token);
            }
            
            document.getElementById('login-section').classList.add('hidden');
            document.getElementById('protected-section').classList.remove('hidden');
            loadProfile();
            showMessage('¡Login exitoso!');
        } else {
            showMessage(data.error || 'Error en login', true);
        }
    } catch (error) {
        showMessage('Error de conexión', true);
    }
}

// Load Profile
async function loadProfile() {
    const token = localStorage.getItem('jwtToken');
    
    if (!token) {
        showMessage('No hay sesión activa', true);
        return;
    }

    try {
        const response = await fetch('http://localhost:8080/api/profile', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const profile = await response.json();
        document.getElementById('profile-data').textContent = 
            `Email: ${profile.profile.email}\nCuenta creada: ${new Date(profile.profile.created_at).toLocaleDateString()}`;
    } catch (error) {
        showMessage('Error al cargar perfil: ' + error.message, true);
        console.error("Error en loadProfile:", error);
    }
}

// Logout
async function logout() {
    const refreshToken = localStorage.getItem('refreshToken');
    const token = localStorage.getItem('jwtToken');

    try {
        await fetch('http://localhost:8080/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh_token: refreshToken }),
        });

        // Limpiar almacenamiento
        localStorage.removeItem('jwtToken');
        localStorage.removeItem('refreshToken');
        
        document.getElementById('login-section').classList.remove('hidden');
        document.getElementById('protected-section').classList.add('hidden');
        showMessage('Sesión cerrada');
    } catch (error) {
        showMessage('Error al cerrar sesión: ' + error.message, true);
    }
}

// Al cargar la página, verificar sesión
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('jwtToken');
    if (token) {
        document.getElementById('login-section').classList.add('hidden');
        document.getElementById('protected-section').classList.remove('hidden');
        loadProfile();
    }
});