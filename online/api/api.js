
class JournalAPI {
    constructor() {
        this.baseUrl = 'http://localhost:3001'; // URL вашего сервера
        this.token = localStorage.getItem('authToken');
        this.isOnline = true; // Состояние подключения
    }

    // Проверка подключения к серверу
    async checkConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/`);
            this.isOnline = response.ok;
            return response.ok;
        } catch (error) {
            this.isOnline = false;
            return false;
        }
    }

    // Установка токена
    setToken(token) {
        this.token = token;
        localStorage.setItem('authToken', token);
    }

    // Удаление токена
    clearToken() {
        this.token = null;
        localStorage.removeItem('authToken');
    }

    // Базовый метод для запросов
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        // Проверяем подключение
        if (!await this.checkConnection()) {
            throw new Error('Нет подключения к серверу. Проверьте, что сервер запущен.');
        }

        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        // Добавляем токен, если он есть
        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.error || error.message || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Аутентификация
    async login(username, password) {
        try {
            const data = await this.request('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ username, password })
            });
            
            if (data.token) {
                this.setToken(data.token);
            }
            
            return data;
        } catch (error) {
            throw error;
        }
    }

    async logout() {
        this.clearToken();
        return { success: true };
    }

    // Ученики
    async getStudents(params = {}) {
        try {
            const queryString = new URLSearchParams(params).toString();
            const endpoint = `/api/students${queryString ? `?${queryString}` : ''}`;
            return await this.request(endpoint);
        } catch (error) {
            throw error;
        }
    }

    // Оценки
    async getGrades(params = {}) {
        try {
            const queryString = new URLSearchParams(params).toString();
            const endpoint = `/api/grades${queryString ? `?${queryString}` : ''}`;
            return await this.request(endpoint);
        } catch (error) {
            throw error;
        }
    }

    async createGrade(gradeData) {
        try {
            return await this.request('/api/grades', {
                method: 'POST',
                body: JSON.stringify(gradeData)
            });
        } catch (error) {
            throw error;
        }
    }

    // Профиль
    async getProfile() {
        try {
            return await this.request('/api/profile');
        } catch (error) {
            throw error;
        }
    }
}

// Создаем глобальный экземпляр API
const journalAPI = new JournalAPI();

// Экспортируем для использования в других модулях
export default journalAPI;