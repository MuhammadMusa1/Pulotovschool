// script.js

// Глобальные переменные
let currentTab = 'dashboard';
let currentStudentId = null;

// DOM Elements
const elements = {
    // Navigation
    navItems: document.querySelectorAll('.nav-item'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Modals
    modalOverlay: document.getElementById('modal-overlay'),
    modals: document.querySelectorAll('.modal'),
    
    // Buttons
    addGradeBtn: document.getElementById('add-grade-btn'),
    addStudentBtn: document.getElementById('add-student-btn'),
    addGoalBtn: document.getElementById('add-goal-btn'),
    addAchievementBtn: document.getElementById('add-achievement-btn'),
    exportPdfBtn: document.getElementById('export-pdf-btn'),
    exportExcelBtn: document.getElementById('export-excel-btn'),
    exportStatsBtn: document.getElementById('export-stats-btn'),
    
    // Forms
    addGradeForm: document.getElementById('add-grade-form'),
    addStudentForm: document.getElementById('add-student-form'),
    
    // Dropdowns
    classFilter: document.getElementById('class-filter'),
    subjectFilter: document.getElementById('subject-filter'),
    studentClassFilter: document.getElementById('student-class-filter'),
    gradeStudent: document.getElementById('grade-student'),
    
    // Data containers
    gradesBody: document.getElementById('grades-body'),
    studentsBody: document.getElementById('students-body'),
    goalsList: document.getElementById('goals-list'),
    achievementsGrid: document.getElementById('achievements-grid'),
    recentActivity: document.getElementById('recent-activity'),
    
    // Stats
    totalGrades: document.getElementById('total-grades'),
    activeGoals: document.getElementById('active-goals'),
    achievementsCount: document.getElementById('achievements-count'),
    averageScore: document.getElementById('average-score')
};

// Utility Functions
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notification-text');
    
    // Устанавливаем иконку в зависимости от типа
    const icon = notification.querySelector('.notification-icon');
    if (icon) {
        if (type === 'success') {
            icon.innerHTML = '<i data-lucide="check-circle"></i>';
        } else if (type === 'error') {
            icon.innerHTML = '<i data-lucide="alert-circle"></i>';
            notification.style.background = 'var(--danger)';
        } else if (type === 'warning') {
            icon.innerHTML = '<i data-lucide="alert-triangle"></i>';
            notification.style.background = 'var(--warning)';
        }
    }
    
    notificationText.textContent = message;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
        notification.style.background = 'var(--success)';
    }, 3000);
    
    // Пересоздаем иконки Lucide
    lucide.createIcons();
}

function switchTab(tabId) {
    // Remove active class from all items
    elements.navItems.forEach(item => item.classList.remove('active'));
    elements.tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected item
    const activeNavItem = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
    
    const activeContent = document.getElementById(tabId);
    if (activeContent) {
        activeContent.classList.add('active');
    }
    
    currentTab = tabId;
    
    // Загружаем данные для текущей вкладки
    loadData();
}

async function loadData() {
    loader.show();
    
    try {
        switch(currentTab) {
            case 'dashboard':
                await updateDashboard();
                break;
            case 'grades':
                await updateGrades();
                break;
            case 'students':
                await updateStudents();
                break;
            case 'goals':
                await updateGoals();
                break;
            case 'achievements':
                await updateAchievements();
                break;
            case 'export':
                // Ничего не делаем, экспорт обрабатывается отдельно
                break;
            case 'profile':
                await updateProfile();
                break;
        }
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification(`Ошибка загрузки данных: ${error.message}`, 'error');
    } finally {
        loader.hide();
    }
}

// Content Update Functions
async function updateDashboard() {
    try {
        // Получаем все необходимые данные параллельно
        const [grades, goals, achievements] = await Promise.all([
            journalAPI.getGrades(),
            journalAPI.getGoals(),
            journalAPI.getAchievements()
        ]);
        
        // Update stats
        elements.totalGrades.textContent = grades.length;
        
        const average = grades.length > 0 ? 
            (grades.reduce((sum, g) => sum + g.score, 0) / grades.length).toFixed(1) : '0.0';
        elements.averageScore.textContent = average;
        
        // Update goals count
        const activeGoals = goals.filter(g => !g.completed).length;
        elements.activeGoals.textContent = activeGoals;
        
        // Update achievements count
        elements.achievementsCount.textContent = achievements.length;
        
        // Update recent activity
        await updateRecentActivity(grades);
        
        // Обновляем графики
        charts.updateCharts();
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
        showNotification(`Ошибка обновления главной страницы: ${error.message}`, 'error');
    }
}

async function updateRecentActivity(grades = null) {
    try {
        if (!grades) {
            grades = await journalAPI.getGrades();
        }
        
        const sortedGrades = [...grades].sort((a, b) => new Date(b.date) - new Date(a.date));
        const recentGrades = sortedGrades.slice(0, 3);
        
        elements.recentActivity.innerHTML = '';
        
        if (recentGrades.length === 0) {
            elements.recentActivity.innerHTML = `
                <div style="text-align: center; padding: 20px; color: var(--gray);">
                    Нет недавних событий
                </div>
            `;
            return;
        }
        
        for (const grade of recentGrades) {
            const student = await getStudentById(grade.studentId);
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            activityItem.innerHTML = `
                <div class="activity-icon">📝</div>
                <div class="activity-content">
                    <div class="activity-title">Новая оценка: ${grade.score} по ${grade.subject}</div>
                    <div class="activity-date">${grade.date} • ${student ? student.name : 'Ученик'}</div>
                </div>
            `;
            elements.recentActivity.appendChild(activityItem);
        }
        
        lucide.createIcons();
        
    } catch (error) {
        console.error('Error updating recent activity:', error);
        showNotification(`Ошибка обновления активности: ${error.message}`, 'error');
    }
}

async function updateGrades() {
    try {
        const params = {
            class: elements.classFilter ? elements.classFilter.value : 'all',
            subject: elements.subjectFilter ? elements.subjectFilter.value : 'all'
        };
        
        const grades = await journalAPI.getGrades(params);
        elements.gradesBody.innerHTML = '';
        
        if (grades.length === 0) {
            elements.gradesBody.innerHTML = `
                <tr>
                    <td colspan="8" style="text-align: center; padding: 40px; color: var(--gray);">
                        Нет оценок
                    </td>
                </tr>
            `;
            return;
        }
        
        for (const grade of grades) {
            const student = await getStudentById(grade.studentId);
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student ? student.name : 'Неизвестно'}</td>
                <td>${student ? student.class : '—'}</td>
                <td>${grade.subject}</td>
                <td>${grade.work}</td>
                <td>${grade.date}</td>
                <td><strong style="color: ${getGradeColor(grade.score)}">${grade.score}</strong></td>
                <td>${grade.teacher}</td>
                <td>
                    <button class="btn btn-small edit-grade" data-id="${grade.id}">
                        <i data-lucide="edit"></i>
                    </button>
                </td>
            `;
            elements.gradesBody.appendChild(row);
        }
        
        lucide.createIcons();
        
        // Добавляем обработчики для кнопок редактирования
        document.querySelectorAll('.edit-grade').forEach(btn => {
            btn.addEventListener('click', () => {
                const gradeId = btn.getAttribute('data-id');
                showNotification('Редактирование оценок доступно в полной версии', 'warning');
            });
        });
        
    } catch (error) {
        console.error('Error updating grades:', error);
        showNotification(`Ошибка загрузки оценок: ${error.message}`, 'error');
        elements.gradesBody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align: center; padding: 40px; color: var(--danger);">
                    Ошибка загрузки данных. Проверьте подключение к серверу.
                </td>
            </tr>
        `;
    }
}

async function updateStudents() {
    try {
        const students = await journalAPI.getStudents();
        elements.studentsBody.innerHTML = '';
        
        if (students.length === 0) {
            elements.studentsBody.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align: center; padding: 40px; color: var(--gray);">
                        Нет учеников
                    </td>
                </tr>
            `;
            return;
        }
        
        for (const student of students) {
            const grades = await journalAPI.getGrades({ studentId: student.id });
            const average = grades.length > 0 ? 
                (grades.reduce((sum, g) => sum + g.score, 0) / grades.length).toFixed(1) : '—';
                
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.name}</td>
                <td>${student.class}</td>
                <td>${student.contact || '—'}</td>
                <td><strong style="color: ${getGradeColor(parseFloat(average))}">${average}</strong></td>
                <td>
                    <button class="btn btn-small view-grades" data-id="${student.id}">
                        <i data-lucide="book-open"></i>
                    </button>
                </td>
            `;
            elements.studentsBody.appendChild(row);
        }
        
        lucide.createIcons();
        
        // Добавляем обработчики для кнопок просмотра оценок
        document.querySelectorAll('.view-grades').forEach(btn => {
            btn.addEventListener('click', async () => {
                const studentId = btn.getAttribute('data-id');
                currentStudentId = studentId;
                switchTab('grades');
                
                // Устанавливаем фильтр по ученику
                if (elements.classFilter) {
                    elements.classFilter.value = 'all';
                }
                if (elements.subjectFilter) {
                    elements.subjectFilter.value = 'all';
                }
                
                showNotification('Фильтр установлен по выбранному ученику');
            });
        });
        
    } catch (error) {
        console.error('Error updating students:', error);
        showNotification(`Ошибка загрузки учеников: ${error.message}`, 'error');
        elements.studentsBody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px; color: var(--danger);">
                    Ошибка загрузки данных. Проверьте подключение к серверу.
                </td>
            </tr>
        `;
    }
}

async function updateGoals() {
    try {
        const goals = await journalAPI.getGoals();
        elements.goalsList.innerHTML = '';
        
        if (goals.length === 0) {
            elements.goalsList.innerHTML = `
                <div class="card" style="text-align: center; padding: 40px;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">🎯</div>
                    <h3>Нет целей</h3>
                    <p style="color: var(--gray);">Добавьте свою первую цель</p>
                </div>
            `;
            return;
        }
        
        for (const goal of goals) {
            const student = await getStudentById(goal.studentId);
            const goalCard = document.createElement('div');
            goalCard.className = 'goal-card';
            goalCard.innerHTML = `
                <div class="goal-content">
                    <div class="goal-title">${goal.text}</div>
                    <div class="goal-status">
                        <div class="goal-date">До ${goal.targetDate}</div>
                        <div class="goal-checkbox ${goal.completed ? 'checked' : ''}" data-id="${goal.id}">
                            ${goal.completed ? '<i data-lucide="check"></i>' : ''}
                        </div>
                    </div>
                </div>
            `;
            elements.goalsList.appendChild(goalCard);
        }
        
        lucide.createIcons();
        
        // Добавляем обработчики для чекбоксов
        document.querySelectorAll('.goal-checkbox').forEach(checkbox => {
            checkbox.addEventListener('click', async () => {
                const goalId = checkbox.getAttribute('data-id');
                const isCompleted = checkbox.classList.contains('checked');
                
                try {
                    // В реальной версии здесь был бы запрос к API
                    // await journalAPI.updateGoal(goalId, { completed: !isCompleted });
                    
                    checkbox.classList.toggle('checked');
                    if (checkbox.classList.contains('checked')) {
                        checkbox.innerHTML = '<i data-lucide="check"></i>';
                        showNotification('Цель выполнена!');
                    } else {
                        checkbox.innerHTML = '';
                    }
                    
                    lucide.createIcons();
                    
                } catch (error) {
                    console.error('Error updating goal:', error);
                    showNotification(`Ошибка обновления цели: ${error.message}`, 'error');
                }
            });
        });
        
    } catch (error) {
        console.error('Error updating goals:', error);
        showNotification(`Ошибка загрузки целей: ${error.message}`, 'error');
    }
}

async function updateAchievements() {
    try {
        const achievements = await journalAPI.getAchievements();
        elements.achievementsGrid.innerHTML = '';
        
        if (achievements.length === 0) {
            elements.achievementsGrid.innerHTML = `
                <div class="card" style="text-align: center; padding: 40px;">
                    <div style="font-size: 3rem; margin-bottom: 15px;">🏆</div>
                    <h3>Нет достижений</h3>
                    <p style="color: var(--gray);">Добавьте первое достижение</p>
                </div>
            `;
            return;
        }
        
        for (const achievement of achievements) {
            const student = await getStudentById(achievement.studentId);
            const achievementCard = document.createElement('div');
            achievementCard.className = 'achievement-card';
            
            const emojis = ['🏆', '🏅', '⭐', '🎉', '🌟', '💫', '✨'];
            const emoji = emojis[Math.floor(Math.random() * emojis.length)];
            
            achievementCard.innerHTML = `
                <div class="achievement-content">
                    <div class="achievement-emoji">${emoji}</div>
                    <div class="achievement-title">${achievement.title}</div>
                    <div class="achievement-desc">${achievement.description}</div>
                    <div style="font-size: 0.8rem; color: var(--gray);">${achievement.date}</div>
                </div>
            `;
            elements.achievementsGrid.appendChild(achievementCard);
        }
        
    } catch (error) {
        console.error('Error updating achievements:', error);
        showNotification(`Ошибка загрузки достижений: ${error.message}`, 'error');
    }
}

async function updateProfile() {
    try {
        const profile = await journalAPI.getProfile();
        if (profile && profile.user) {
            const user = profile.user;
            
            document.getElementById('profile-name').textContent = user.name;
            document.getElementById('profile-username').textContent = user.username;
            document.getElementById('profile-role').textContent = user.role === 'admin' ? 'Админ' : 
                                                                       user.role === 'teacher' ? 'Учитель' : 'Ученик';
            document.getElementById('profile-full-role').textContent = user.role === 'admin' ? 'Администратор' : 
                                                                              user.role === 'teacher' ? 'Учитель' : 'Ученик';
            
            // В реальной версии здесь были бы дополнительные данные
            const student = user.studentId ? await getStudentById(user.studentId) : null;
            if (student) {
                document.getElementById('profile-class').textContent = student.class;
                document.getElementById('profile-contact').textContent = student.contact || '—';
            }
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showNotification(`Ошибка загрузки профиля: ${error.message}`, 'error');
    }
}

// Helper Functions
function getGradeColor(score) {
    if (score >= 9) return '#8b5cf6'; // purple
    if (score >= 7) return '#06b6d4'; // cyan
    if (score >= 5) return '#f97316'; // orange
    if (score >= 3) return '#ef4444'; // red
    return '#6b7280'; // gray
}

async function getStudentById(studentId) {
    try {
        // В реальной версии был бы запрос к API
        // return await journalAPI.getStudent(studentId);
        
        // Для демо-версии используем mock-данные
        const students = [
            { id: 1, name: "Алексей Иванов", class: "9А", contact: "alex@example.com", username: "alex_ivanov" },
            { id: 2, name: "Мария Петрова", class: "9А", contact: "maria@example.com", username: "maria_petrova" },
            { id: 3, name: "Иван Сидоров", class: "9Б", contact: "ivan@example.com", username: "ivan_sidorov" },
            { id: 4, name: "Елена Козлова", class: "9Б", contact: "elena@example.com", username: "elena_kozlova" }
        ];
        
        return students.find(s => s.id === studentId);
    } catch (error) {
        console.error('Error getting student:', error);
        return null;
    }
}

// Event Listeners
function setupEventListeners() {
    // Navigation
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // Modal buttons
    document.querySelectorAll('.close-btn, .close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal') || btn.closest('.modal').id;
            closeModal(modalId);
        });
    });

    // Modal overlay click
    elements.modalOverlay.addEventListener('click', () => {
        document.querySelectorAll('.modal').forEach(modal => {
            if (modal.style.display === 'block') {
                closeModal(modal.id);
            }
        });
    });

    // Add buttons
    if (elements.addGradeBtn) {
        elements.addGradeBtn.addEventListener('click', async () => {
            try {
                const students = await journalAPI.getStudents();
                elements.gradeStudent.innerHTML = '<option value="">Выберите ученика</option>';
                
                students.forEach(student => {
                    const option = document.createElement('option');
                    option.value = student.id;
                    option.textContent = `${student.name} (${student.class})`;
                    elements.gradeStudent.appendChild(option);
                });
                
                openModal('add-grade-modal');
            } catch (error) {
                console.error('Error loading students for modal:', error);
                showNotification(`Ошибка загрузки учеников: ${error.message}`, 'error');
            }
        });
    }

    if (elements.addStudentBtn) {
        elements.addStudentBtn.addEventListener('click', () => {
            openModal('add-student-modal');
        });
    }

    if (elements.addGoalBtn) {
        elements.addGoalBtn.addEventListener('click', () => {
            showNotification('Добавление целей доступно ученикам в их профиле', 'warning');
        });
    }

    if (elements.addAchievementBtn) {
        elements.addAchievementBtn.addEventListener('click', () => {
            showNotification('Добавление достижений доступно учителям', 'warning');
        });
    }

    // Form submissions
    if (elements.addGradeForm) {
        elements.addGradeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            const gradeData = {
                studentId: parseInt(formData.get('grade-student')),
                subject: formData.get('grade-subject'),
                work: formData.get('grade-work'),
                score: parseInt(formData.get('grade-score')),
                comment: formData.get('grade-comment'),
                weight: parseFloat(formData.get('grade-weight'))
            };
            
            // Валидация
            if (!gradeData.studentId || !gradeData.subject || !gradeData.work || 
                isNaN(gradeData.score) || gradeData.score < 1 || gradeData.score > 10) {
                showNotification('Пожалуйста, заполните все поля корректно', 'error');
                return;
            }
            
            loader.show();
            
            try {
                // В реальной версии был бы запрос к API
                // const result = await journalAPI.createGrade(gradeData);
                
                showNotification('Оценка добавлена успешно! (демо-режим)', 'success');
                closeModal('add-grade-modal');
                e.target.reset();
                await loadData();
            } catch (error) {
                console.error('Error adding grade:', error);
                showNotification(`Ошибка добавления оценки: ${error.message}`, 'error');
            } finally {
                loader.hide();
            }
        });
    }

    if (elements.addStudentForm) {
        elements.addStudentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            const studentData = {
                name: formData.get('student-name'),
                class: formData.get('student-class'),
                contact: formData.get('student-contact'),
                username: formData.get('student-username'),
                password: formData.get('student-password')
            };
            
            // Валидация
            if (!studentData.name || !studentData.class || !studentData.username || !studentData.password) {
                showNotification('Пожалуйста, заполните все обязательные поля', 'error');
                return;
            }
            
            loader.show();
            
            try {
                // В реальной версии был бы запрос к API
                // const result = await journalAPI.createStudent(studentData);
                
                showNotification('Ученик добавлен успешно! (демо-режим)', 'success');
                closeModal('add-student-modal');
                e.target.reset();
                await loadData();
            } catch (error) {
                console.error('Error adding student:', error);
                showNotification(`Ошибка добавления ученика: ${error.message}`, 'error');
            } finally {
                loader.hide();
            }
        });
    }

    // Filter changes
    if (elements.classFilter) {
        elements.classFilter.addEventListener('change', loadData);
    }

    if (elements.subjectFilter) {
        elements.subjectFilter.addEventListener('change', loadData);
    }

    if (elements.studentClassFilter) {
        elements.studentClassFilter.addEventListener('change', loadData);
    }
}

// Modal Functions
function openModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'flex';
    document.getElementById(modalId).style.display = 'block';
    
    // Пересоздаем иконки Lucide
    lucide.createIcons();
}

function closeModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'none';
    document.getElementById(modalId).style.display = 'none';
}

// Initialize app
async function initApp() {
    // Проверяем статус аутентификации
    auth.checkAuthStatus();
    
    // Настройка обработчиков событий
    setupEventListeners();
    
    // Инициализация Lucide иконок
    lucide.createIcons();
}

// Запускаем приложение при загрузке страницы
document.addEventListener('DOMContentLoaded', initApp);