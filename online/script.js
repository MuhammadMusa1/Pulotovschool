// script.js

// Initialize Lucide icons
lucide.createIcons();

// Global variables
let currentTab = 'dashboard';

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
function showNotification(message) {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notification-text');
    
    notificationText.textContent = message;
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
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
    updateContent();
}

function openModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'flex';
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById('modal-overlay').style.display = 'none';
    document.getElementById(modalId).style.display = 'none';
}

function populateStudentDropdown() {
    const students = api.getStudents();
    elements.gradeStudent.innerHTML = '<option value="">Выберите ученика</option>';
    
    students.forEach(student => {
        const option = document.createElement('option');
        option.value = student.id;
        option.textContent = `${student.name} (${student.class})`;
        elements.gradeStudent.appendChild(option);
    });
}

// Content Update Functions
function updateContent() {
    const user = api.getCurrentUser();
    if (!user) return;

    switch(currentTab) {
        case 'dashboard':
            updateDashboard();
            break;
        case 'grades':
            updateGrades();
            break;
        case 'students':
            updateStudents();
            break;
        case 'goals':
            updateGoals();
            break;
        case 'achievements':
            updateAchievements();
            break;
        case 'export':
            updateExport();
            break;
        case 'profile':
            updateProfile();
            break;
    }
}

function updateDashboard() {
    // Update stats
    const stats = api.getStatistics();
    elements.totalGrades.textContent = stats.totalGrades;
    elements.averageScore.textContent = stats.averageScore;
    
    // Update goals count
    const goals = api.getGoals();
    elements.activeGoals.textContent = goals.filter(g => !g.completed).length;
    
    // Update achievements count
    const achievements = api.getAchievements();
    elements.achievementsCount.textContent = achievements.length;
    
    // Update recent activity
    updateRecentActivity();
}

function updateRecentActivity() {
    const grades = api.getGrades();
    const sortedGrades = [...grades].sort((a, b) => new Date(b.date) - new Date(a.date));
    const recentGrades = sortedGrades.slice(0, 3);
    
    elements.recentActivity.innerHTML = '';
    
    recentGrades.forEach(grade => {
        const student = api.students.find(s => s.id === grade.studentId);
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
    });
}

function updateGrades() {
    const grades = api.getGrades();
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
    
    grades.forEach(grade => {
        const student = api.students.find(s => s.id === grade.studentId);
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
    });
    
    lucide.createIcons();
}

function updateStudents() {
    const students = api.getStudents();
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
    
    students.forEach(student => {
        const grades = api.grades.filter(g => g.studentId === student.id);
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
    });
    
    lucide.createIcons();
}

function updateGoals() {
    const goals = api.getGoals();
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
    
    goals.forEach(goal => {
        const student = api.students.find(s => s.id === goal.studentId);
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
    });
    
    lucide.createIcons();
    
    // Add event listeners to checkboxes
    document.querySelectorAll('.goal-checkbox').forEach(checkbox => {
        checkbox.addEventListener('click', () => {
            const goalId = checkbox.getAttribute('data-id');
            showNotification('Статус цели обновлен!');
        });
    });
}

function updateAchievements() {
    const achievements = api.getAchievements();
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
    
    achievements.forEach(achievement => {
        const student = api.students.find(s => s.id === achievement.studentId);
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
    });
}

function updateExport() {
    // Export functionality will be implemented here
    console.log('Export tab updated');
}

function updateProfile() {
    const user = api.getCurrentUser();
    if (!user) return;
    
    // Profile is updated in auth.js
}

// Helper Functions
function getGradeColor(score) {
    if (score >= 9) return '#8b5cf6'; // purple
    if (score >= 7) return '#06b6d4'; // cyan
    if (score >= 5) return '#f97316'; // orange
    if (score >= 3) return '#ef4444'; // red
    return '#6b7280'; // gray
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
        elements.addGradeBtn.addEventListener('click', () => {
            populateStudentDropdown();
            openModal('add-grade-modal');
        });
    }

    if (elements.addStudentBtn) {
        elements.addStudentBtn.addEventListener('click', () => {
            openModal('add-student-modal');
        });
    }

    if (elements.addGoalBtn) {
        elements.addGoalBtn.addEventListener('click', () => {
            showNotification('Цели можно добавлять только ученику');
        });
    }

    if (elements.addAchievementBtn) {
        elements.addAchievementBtn.addEventListener('click', () => {
            showNotification('Достижения можно добавлять только учителю');
        });
    }

    // Form submissions
    if (elements.addGradeForm) {
        elements.addGradeForm.addEventListener('submit', (e) => {
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
            
            const result = api.addGrade(gradeData);
            if (result.success) {
                showNotification('Оценка добавлена успешно!');
                closeModal('add-grade-modal');
                e.target.reset();
                updateContent();
            } else {
                showNotification(result.error);
            }
        });
    }

    if (elements.addStudentForm) {
        elements.addStudentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const studentData = {
                name: formData.get('student-name'),
                class: formData.get('student-class'),
                contact: formData.get('student-contact'),
                username: formData.get('student-username'),
                password: formData.get('student-password')
            };
            
            const result = api.addStudent(studentData);
            if (result.success) {
                showNotification('Ученик добавлен успешно!');
                closeModal('add-student-modal');
                e.target.reset();
                updateContent();
            } else {
                showNotification(result.error);
            }
        });
    }

    // Export buttons
    if (elements.exportPdfBtn) {
        elements.exportPdfBtn.addEventListener('click', () => {
            showNotification('Экспорт в PDF реализован в полной версии');
        });
    }

    if (elements.exportExcelBtn) {
        elements.exportExcelBtn.addEventListener('click', () => {
            showNotification('Экспорт в Excel реализован в полной версии');
        });
    }

    if (elements.exportStatsBtn) {
        elements.exportStatsBtn.addEventListener('click', () => {
            showNotification('Экспорт статистики реализован в полной версии');
        });
    }

    // Filter changes
    if (elements.classFilter) {
        elements.classFilter.addEventListener('change', updateContent);
    }

    if (elements.subjectFilter) {
        elements.subjectFilter.addEventListener('change', updateContent);
    }

    if (elements.studentClassFilter) {
        elements.studentClassFilter.addEventListener('change', updateContent);
    }
}

// Initialize app
function initApp() {
    // Check if user is logged in
    const user = api.getCurrentUser();
    if (user) {
        auth.showMainApp();
        updateContent();
    } else {
        auth.showLoginPage();
    }
    
    // Setup event listeners
    setupEventListeners();
    
    // Initial content update
    updateContent();
}

// Start the app when page loads
document.addEventListener('DOMContentLoaded', initApp);