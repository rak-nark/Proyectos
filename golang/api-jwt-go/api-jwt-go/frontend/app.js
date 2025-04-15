// Selección de elementos del DOM
const registerSection = document.getElementById('register-section');
const loginSection = document.getElementById('login-section');
const protectedSection = document.getElementById('protected-section');
const messageDiv = document.getElementById('message');

// Botones y enlaces
const registerBtn = document.getElementById('register-btn');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const showLoginLink = document.getElementById('show-login-link');
const showRegisterLink = document.getElementById('show-register-link');

// Variables para almacenar tokens
let accessToken = '';
let refreshToken = '';

// Configurar event listeners cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    // Asignar event listeners
    registerBtn.addEventListener('click', register);
    loginBtn.addEventListener('click', login);
    logoutBtn.addEventListener('click', logout);
    showLoginLink.addEventListener('click', showLogin);
    showRegisterLink.addEventListener('click', showRegister);
    
    // Prevenir el comportamiento por defecto de los enlaces
    showLoginLink.addEventListener('click', (e) => e.preventDefault());
    showRegisterLink.addEventListener('click', (e) => e.preventDefault());
    
    // Verificar si hay una sesión activa
    checkExistingSession();
});

// Función para mostrar/ocultar secciones
function showRegister() {
    loginSection.classList.add('hidden');
    registerSection.classList.remove('hidden');
    protectedSection.classList.add('hidden');
    clearMessage();
}

function showLogin() {
    registerSection.classList.add('hidden');
    loginSection.classList.remove('hidden');
    protectedSection.classList.add('hidden');
    clearMessage();
}

function showProtected() {
    registerSection.classList.add('hidden');
    loginSection.classList.add('hidden');
    protectedSection.classList.remove('hidden');
}

function clearMessage() {
    messageDiv.textContent = '';
    messageDiv.className = 'hidden';
}

// Función para mostrar mensajes
function showMessage(text, isError = false) {
    messageDiv.textContent = text;
    messageDiv.className = isError ? 'error' : 'success';
    messageDiv.classList.remove('hidden');
    
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 5000);
}

// Función de registro
async function register() {
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch('http://localhost:8080/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error en el registro');
        }

        showMessage('Registro exitoso! Por favor inicia sesión');
        showLogin();
    } catch (error) {
        showMessage(error.message, true);
        console.error('Error en registro:', error);
    }
}

// Función de login
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error en el login');
        }

        accessToken = data.token;
        refreshToken = data.refresh_token;
        
        // Guardar tokens en localStorage
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);

        await loadProfile();
        showProtected();
        showMessage('Sesión iniciada correctamente');
    } catch (error) {
        showMessage(error.message, true);
        console.error('Error en login:', error);
    }
}

// Función para cargar el perfil
async function loadProfile() {
    try {
        const response = await fetch('http://localhost:8080/api/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al cargar perfil');
        }

        document.getElementById('user-email').textContent = data.profile.email;
    } catch (error) {
        showMessage(error.message, true);
        console.error('Error cargando perfil:', error);
    }
}

// Función de logout
async function logout() {
    try {
        const response = await fetch('http://localhost:8080/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ refresh_token: refreshToken })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Error al cerrar sesión');
        }

        // Limpiar tokens
        accessToken = '';
        refreshToken = '';
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        
        showLogin();
        showMessage('Sesión cerrada correctamente');
    } catch (error) {
        showMessage(error.message, true);
        console.error('Error en logout:', error);
    }
}

// Verificar sesión existente
function checkExistingSession() {
    const savedToken = localStorage.getItem('accessToken');
    if (savedToken) {
        accessToken = savedToken;
        refreshToken = localStorage.getItem('refreshToken') || '';
        loadProfile().then(() => showProtected());
    } else {
        showLogin();
    }
}