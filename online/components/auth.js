// components/auth.js

class AuthComponent {
    constructor() {
        this.loginForm = document.getElementById('login-form');
        this.logoutBtn = document.getElementById('logout-btn');
        
        this.bindEvents();
        this.checkAuthStatus();
    }

    bindEvents() {
        // Login form submission
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleLogin();
            });
        }

        // Logout button
        if (this.logoutBtn) {
            this.logoutBtn.addEventListener('click', async () => {
                await this.handleLogout();
            });
        }
    }

    async checkAuthStatus() {
        const token = localStorage.getItem('authToken');
        if (token) {
            try {
                // Проверяем валидность токена
                const profile = await journalAPI.getProfile();
                journalAPI.setToken(token);
                this.showMainApp(profile);
            } catch (error) {
                // Токен недействителен, очищаем и показываем форму входа
                journalAPI.clearToken();
                this.showLoginPage();
            }
        } else {
            this.showLoginPage();
        }
    }

    async handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (!username || !password) {
            showNotification('Пожалуйста, заполните все поля');
            return;
        }

        // Показываем индикатор загрузки
        this.showLoading(true);

        try {
            const result = await journalAPI.login(username, password);
            
            if (result.token) {
                const profile = await journalAPI.getProfile();
                showNotification('Вход выполнен успешно!');
                this.showMainApp(profile);
            } else {
                showNotification(result.error || 'Ошибка входа');
            }
        } catch (error) {
            console.error('Login error:', error);
            showNotification(`Ошибка входа: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    async handleLogout() {
        try {
            await journalAPI.logout();
            showNotification('Вы вышли из системы');
            this.showLoginPage();
        } catch (error) {
            console.error('Logout error:', error);
            showNotification('Ошибка выхода из системы');
        }
    }

    showMainApp(profile) {
        document.getElementById('login-page').style.display = 'none';
        document.getElementById('main-app').style.display = 'block';
        
        // Update UI with user info
        if (profile && profile.user) {
            const user = profile.user;
            document.getElementById('user-role').textContent = user.role === 'admin' ? 'Админ' : 
                                                               user.role === 'teacher' ? 'Учитель' : 'Ученик';
            document.getElementById('username').textContent = user.name;
            document.getElementById('welcome-name').textContent = user.name.split(' ')[0];
            document.getElementById('welcome-role').textContent = `Вы вошли как ${user.role === 'admin' ? 'администратор' : 
                                                                                   user.role === 'teacher' ? 'учитель' : 'ученик'}`;
            
            // Update profile
            document.getElementById('profile-name').textContent = user.name;
            document.getElementById('profile-username').textContent = user.username;
            document.getElementById('profile-role').textContent = user.role === 'admin' ? 'Админ' : 
                                                                       user.role === 'teacher' ? 'Учитель' : 'Ученик';
            document.getElementById('profile-full-role').textContent = user.role === 'admin' ? 'Администратор' : 
                                                                              user.role === 'teacher' ? 'Учитель' : 'Ученик';
        }
    }

    showLoginPage() {
        document.getElementById('main-app').style.display = 'none';
        document.getElementById('login-page').style.display = 'block';
        
        // Clear login form
        if (this.loginForm) {
            this.loginForm.reset();
        }
    }

    showLoading(show) {
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                if (show) {
                    submitBtn.innerHTML = '<i data-lucide="loader" class="animate-spin"></i> Вход...';
                    submitBtn.disabled = true;
                } else {
                    submitBtn.innerHTML = '<i data-lucide="log-in"></i> Войти';
                    submitBtn.disabled = false;
                }
            }
        }
    }
}

// Initialize auth component
const auth = new AuthComponent();

// Инициализация Lucide иконок
lucide.createIcons();