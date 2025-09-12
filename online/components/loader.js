// components/loader.js

class Loader {
    constructor() {
        this.createLoader();
    }

    createLoader() {
        const loader = document.createElement('div');
        loader.id = 'global-loader';
        loader.innerHTML = `
            <div class="loader-overlay">
                <div class="loader-content">
                    <div class="loader-spinner"></div>
                    <p>Загрузка...</p>
                </div>
            </div>
        `;
        document.body.appendChild(loader);
    }

    show() {
        const loader = document.getElementById('global-loader');
        if (loader) {
            loader.style.display = 'flex';
        }
    }

    hide() {
        const loader = document.getElementById('global-loader');
        if (loader) {
            loader.style.display = 'none';
        }
    }
}

// Создаем глобальный экземпляр лоадера
const loader = new Loader();