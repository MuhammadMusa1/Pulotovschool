// script.js

// App Data and State
const appData = {
    currentLanguage: 'ru',
    currentUser: {
        name: 'Алексей',
        role: 'student', // student, teacher, admin
        class: '9 класс'
    },
    students: [
        { id: 1, name: 'Алексей', class: '9 класс', role: 'student' },
        { id: 2, name: 'Мария', class: '9 класс', role: 'student' },
        { id: 3, name: 'Иван', class: '9 класс', role: 'student' }
    ],
    teachers: [
        { id: 1, name: 'Ольга Петровна', subject: 'Математика', role: 'teacher' },
        { id: 2, name: 'Анна Сергеевна', subject: 'Русский язык', role: 'teacher' }
    ],
    grades: [
        { id: 1, studentId: 1, subject: 'Математика', grade: 9, date: '15.01.2024', teacherId: 1 },
        { id: 2, studentId: 1, subject: 'Русский язык', grade: 7, date: '14.01.2024', teacherId: 2 },
        { id: 3, studentId: 1, subject: 'Физика', grade: 10, date: '13.01.2024', teacherId: 1 },
        { id: 4, studentId: 1, subject: 'История', grade: 6, date: '12.01.2024', teacherId: 2 },
        { id: 5, studentId: 1, subject: 'Биология', grade: 8, date: '11.01.2024', teacherId: 1 }
    ],
    goals: [
        { id: 1, studentId: 1, text: 'Подготовиться к контрольной по математике', completed: false },
        { id: 2, studentId: 1, text: 'Прочитать главу по литературе', completed: true },
        { id: 3, studentId: 1, text: 'Сдать проект по информатике', completed: false }
    ],
    achievements: [
        { id: 1, studentId: 1, title: 'Лучший в математике', description: 'Высокие оценки за четверть', stars: 5, date: '10.01.2024' },
        { id: 2, studentId: 1, title: 'Читатель года', description: 'Прочитал 10 книг', stars: 3, date: '05.01.2024' }
    ],
    nextId: 1000
};

// Language translations
const translations = {
    ru: {
        greeting: 'Привет, ',
        welcomeTitle: 'Привет, ',
        welcomeSubtitle: 'Ты на правильном пути к успеху!',
        recentGradesTitle: 'Последние оценки',
        activeGoalsTitle: 'Активные цели',
        addGradeTitle: 'Добавить оценку',
        subjectLabel: 'Название предмета',
        gradeLabel: 'Оценка: ',
        addGradeBtnText: 'Добавить оценку',
        allGradesTitle: 'Все оценки',
        progressTitle: 'Прогресс',
        goalsTitle: 'Мои цели',
        addAchievementTitle: 'Добавить достижение',
        achievementTitleLabel: 'Название достижения',
        achievementDescLabel: 'Описание',
        addAchievementBtnText: 'Добавить достижение',
        achievementsTitle: 'Мои достижения',
        exportTitle: 'Экспорт данных',
        exportPdfText: 'Экспорт в PDF',
        exportExcelText: 'Экспорт в Excel',
        navHome: 'Главная',
        navGrades: 'Оценки',
        navGoals: 'Цели',
        navAchievements: 'Достижения',
        navExport: 'Экспорт',
        errorEmpty: 'Поле не может быть пустым',
        notificationGradeAdded: 'Оценка добавлена!',
        notificationGoalCompleted: 'Цель выполнена!',
        notificationAchievementAdded: 'Достижение добавлено!',
        notificationExportPdf: 'Данные экспортированы в PDF!',
        notificationExportExcel: 'Данные экспортированы в Excel!'
    },
    tg: {
        greeting: 'Салом, ',
        welcomeTitle: 'Салом, ',
        welcomeSubtitle: 'Шумо дар роҳи муваффақият ҳастед!',
        recentGradesTitle: 'Намудҳои охирин',
        activeGoalsTitle: 'Ҳадафҳои фаъол',
        addGradeTitle: 'Илова кардани нафар',
        subjectLabel: 'Номи фан',
        gradeLabel: 'Нафар: ',
        addGradeBtnText: 'Илова кардани нафар',
        allGradesTitle: 'Ҳамаи нафарҳо',
        progressTitle: 'Тараqqиёт',
        goalsTitle: 'Ҳадафҳои ман',
        addAchievementTitle: 'Илова кардани дастовард',
        achievementTitleLabel: 'Сарлавҳаи дастовард',
        achievementDescLabel: 'Тавсиф',
        addAchievementBtnText: 'Илова кардани дастовард',
        achievementsTitle: 'Дастовардҳои ман',
        exportTitle: 'Содироти маълумот',
        exportPdfText: 'Содирот ба PDF',
        exportExcelText: 'Содирот ба Excel',
        navHome: 'Асосӣ',
        navGrades: 'Нафарҳо',
        navGoals: 'Ҳадафҳо',
        navAchievements: 'Дастовардҳо',
        navExport: 'Содирот',
        errorEmpty: 'Майдон набояд холӣ бошад',
        notificationGradeAdded: 'Нафар илова шуд!',
        notificationGoalCompleted: 'Ҳадаф анҷом шуд!',
        notificationAchievementAdded: 'Дастовард илова шуд!',
        notificationExportPdf: 'Маълумот ба PDF содир шуд!',
        notificationExportExcel: 'Маълумот ба Excel содир шуд!'
    }
};

// DOM Elements
const elements = {
    navItems: document.querySelectorAll('.nav-item'),
    contents: document.querySelectorAll('.content'),
    notification: document.getElementById('notification'),
    notificationText: document.getElementById('notification-text'),
    languageSwitch: document.getElementById('language-switch'),
    userName: document.getElementById('user-name'),
    greeting: document.getElementById('greeting'),
    // Form elements
    subject: document.getElementById('subject'),
    grade: document.getElementById('grade'),
    gradeValue: document.getElementById('grade-value'),
    rangeValue: document.getElementById('range-value'),
    addGradeBtn: document.getElementById('add-grade'),
    // Achievement form
    achievementTitle: document.getElementById('achievement-title'),
    achievementDesc: document.getElementById('achievement-desc'),
    addAchievementBtn: document.getElementById('add-achievement'),
    // Error messages
    subjectError: document.getElementById('subject-error'),
    achievementTitleError: document.getElementById('achievement-title-error'),
    achievementDescError: document.getElementById('achievement-desc-error'),
    // Export buttons
    exportPdf: document.getElementById('export-pdf'),
    exportExcel: document.getElementById('export-excel')
};

// Utility Functions
function getTranslation(key) {
    return translations[appData.currentLanguage][key] || key;
}

function updateTextContent() {
    // Update all text elements based on current language
    document.getElementById('greeting').textContent = getTranslation('greeting') + appData.currentUser.name;
    document.getElementById('welcome-title').textContent = getTranslation('welcomeTitle') + appData.currentUser.name + '!';
    document.getElementById('welcome-subtitle').textContent = getTranslation('welcomeSubtitle');
    
    // Update labels
    document.getElementById('recent-grades-title').textContent = getTranslation('recentGradesTitle');
    document.getElementById('active-goals-title').textContent = getTranslation('activeGoalsTitle');
    document.getElementById('add-grade-title').textContent = getTranslation('addGradeTitle');
    document.getElementById('subject-label').textContent = getTranslation('subjectLabel');
    document.getElementById('grade-label').innerHTML = getTranslation('gradeLabel') + '<span id="grade-value">5</span>';
    document.getElementById('add-grade-btn-text').textContent = getTranslation('addGradeBtnText');
    document.getElementById('all-grades-title').textContent = getTranslation('allGradesTitle');
    document.getElementById('progress-title').textContent = getTranslation('progressTitle');
    document.getElementById('goals-title').textContent = getTranslation('goalsTitle');
    document.getElementById('add-achievement-title').textContent = getTranslation('addAchievementTitle');
    document.getElementById('achievement-title-label').textContent = getTranslation('achievementTitleLabel');
    document.getElementById('achievement-desc-label').textContent = getTranslation('achievementDescLabel');
    document.getElementById('add-achievement-btn-text').textContent = getTranslation('addAchievementBtnText');
    document.getElementById('achievements-title').textContent = getTranslation('achievementsTitle');
    document.getElementById('export-title').textContent = getTranslation('exportTitle');
    document.getElementById('export-pdf-text').textContent = getTranslation('exportPdfText');
    document.getElementById('export-excel-text').textContent = getTranslation('exportExcelText');
    
    // Update navigation
    document.getElementById('nav-home').textContent = getTranslation('navHome');
    document.getElementById('nav-grades').textContent = getTranslation('navGrades');
    document.getElementById('nav-goals').textContent = getTranslation('navGoals');
    document.getElementById('nav-achievements').textContent = getTranslation('navAchievements');
    document.getElementById('nav-export').textContent = getTranslation('navExport');
}

function showNotification(message) {
    elements.notificationText.textContent = message;
    elements.notification.classList.add('show');
    
    setTimeout(() => {
        elements.notification.classList.remove('show');
    }, 3000);
}

function validateField(element, errorElement, errorMessage) {
    const value = element.value.trim();
    if (value === '') {
        element.classList.add('error');
        errorElement.textContent = errorMessage;
        errorElement.classList.add('show');
        return false;
    } else {
        element.classList.remove('error');
        errorElement.classList.remove('show');
        return true;
    }
}

function getGradeEmoji(grade) {
    if (grade >= 9) return '🥳';
    if (grade >= 7) return '😊';
    if (grade >= 5) return '😕';
    if (grade >= 3) return '🙁';
    return '😞';
}

// Navigation Functions
function switchTab(tabId) {
    // Remove active class from all items
    elements.navItems.forEach(item => item.classList.remove('active'));
    elements.contents.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected item
    const activeNavItem = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
    
    const activeContent = document.getElementById(tabId);
    if (activeContent) {
        activeContent.classList.add('active');
    }
    
    // Update content
    updateContent();
}

// Content Update Functions
function updateContent() {
    const activeTab = document.querySelector('.nav-item.active').getAttribute('data-tab');
    
    switch(activeTab) {
        case 'home':
            updateHomeContent();
            break;
        case 'grades':
            updateGradesContent();
            break;
        case 'goals':
            updateGoalsContent();
            break;
        case 'achievements':
            updateAchievementsContent();
            break;
        case 'export':
            updateExportContent();
            break;
    }
}

function updateHomeContent() {
    // Recent grades
    const recentGradesContainer = document.getElementById('recent-grades');
    recentGradesContainer.innerHTML = '';
    
    const studentGrades = appData.grades.filter(grade => grade.studentId === 1).slice(0, 3);
    if (studentGrades.length === 0) {
        recentGradesContainer.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #6b7280;">
                <div style="font-size: 2rem;">📚</div>
                <div>${getTranslation('noGrades')}</div>
            </div>
        `;
    } else {
        studentGrades.forEach(grade => {
            const gradeElement = document.createElement('div');
            gradeElement.className = `grade-item grade-${grade.grade}`;
            gradeElement.innerHTML = `
                <div class="grade-info">
                    <span class="grade-number">${grade.grade}</span>
                    <div>
                        <div class="grade-subject">${grade.subject}</div>
                        <div class="grade-date">${grade.date}</div>
                    </div>
                </div>
                <span class="grade-emoji">${getGradeEmoji(grade.grade)}</span>
            `;
            recentGradesContainer.appendChild(gradeElement);
        });
    }

    // Active goals
    const activeGoalsContainer = document.getElementById('active-goals');
    activeGoalsContainer.innerHTML = '';
    
    const studentGoals = appData.goals.filter(goal => goal.studentId === 1 && !goal.completed);
    if (studentGoals.length === 0) {
        activeGoalsContainer.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #6b7280;">
                <div style="font-size: 2rem;">🎉</div>
                <div>${getTranslation('allGoalsCompleted')}</div>
            </div>
        `;
    } else {
        studentGoals.slice(0, 3).forEach(goal => {
            const goalElement = document.createElement('div');
            goalElement.className = 'grade-item';
            goalElement.innerHTML = `
                <span style="font-size: 1.5rem; margin-right: 10px;">🎯</span>
                <span style="color: #333;">${goal.text}</span>
            `;
            activeGoalsContainer.appendChild(goalElement);
        });
    }
}

function updateGradesContent() {
    // Update grade value display
    const gradeValueElement = document.getElementById('grade-value');
    if (gradeValueElement) {
        gradeValueElement.textContent = elements.grade.value;
    }
    
    if (elements.rangeValue) {
        elements.rangeValue.textContent = elements.grade.value;
    }

    elements.grade.addEventListener('input', () => {
        if (gradeValueElement) {
            gradeValueElement.textContent = elements.grade.value;
        }
        if (elements.rangeValue) {
            elements.rangeValue.textContent = elements.grade.value;
        }
    });

    // All grades
    const allGradesContainer = document.getElementById('all-grades');
    allGradesContainer.innerHTML = '';
    
    const studentGrades = appData.grades.filter(grade => grade.studentId === 1);
    if (studentGrades.length === 0) {
        allGradesContainer.innerHTML = `
            <div style="text-align: center; padding: 20px; color: #6b7280;">
                <div style="font-size: 2rem;">📚</div>
                <div>${getTranslation('noGrades')}</div>
            </div>
        `;
    } else {
        studentGrades.forEach(grade => {
            const teacher = appData.teachers.find(t => t.id === grade.teacherId);
            const teacherName = teacher ? teacher.name : '';
            
            const gradeElement = document.createElement('div');
            gradeElement.className = `grade-item grade-${grade.grade}`;
            gradeElement.innerHTML = `
                <div class="grade-info">
                    <span class="grade-number">${grade.grade}</span>
                    <div>
                        <div class="grade-subject">${grade.subject}</div>
                        <div class="grade-date">${grade.date} • ${teacherName}</div>
                    </div>
                </div>
                <span class="grade-emoji">${getGradeEmoji(grade.grade)}</span>
            `;
            allGradesContainer.appendChild(gradeElement);
        });
    }

    // Update chart
    updateChart();
}

function updateGoalsContent() {
    const goalsList = document.getElementById('goals-list');
    goalsList.innerHTML = '';
    
    const studentGoals = appData.goals.filter(goal => goal.studentId === 1);
    studentGoals.forEach(goal => {
        const goalElement = document.createElement('div');
        goalElement.className = 'goal-item';
        goalElement.innerHTML = `
            <div class="goal-checkbox ${goal.completed ? 'checked' : ''}">
                ${goal.completed ? '<i data-lucide="check" style="color: white; font-size: 14px;"></i>' : ''}
            </div>
            <div class="goal-text ${goal.completed ? 'completed' : ''}">${goal.text}</div>
        `;
        
        goalElement.addEventListener('click', () => {
            goal.completed = !goal.completed;
            updateContent();
            
            if (!goal.completed) {
                showNotification(getTranslation('notificationGoalCompleted'));
            }
        });
        
        goalsList.appendChild(goalElement);
    });

    // Initialize Lucide icons in dynamically created elements
    lucide.createIcons();
}

function updateAchievementsContent() {
    const achievementsGrid = document.getElementById('achievements-grid');
    achievementsGrid.innerHTML = '';
    
    const studentAchievements = appData.achievements.filter(achievement => achievement.studentId === 1);
    if (studentAchievements.length === 0) {
        achievementsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 20px; color: #6b7280;">
                <div style="font-size: 2rem;">🏆</div>
                <div>${getTranslation('noAchievements')}</div>
            </div>
        `;
    } else {
        studentAchievements.forEach(achievement => {
            const achievementElement = document.createElement('div');
            achievementElement.className = 'achievement-card';
            
            // Random emoji based on context
            const emojis = ['🎉', '🏆', '⭐', '🏅', '🎯', '📚', '🔬', '🎨', '⚽'];
            const emoji = emojis[Math.floor(Math.random() * emojis.length)];
            
            let starsHTML = '';
            for (let i = 0; i < achievement.stars; i++) {
                starsHTML += '<span class="star">⭐</span>';
            }
            
            achievementElement.innerHTML = `
                <div class="achievement-emoji">${emoji}</div>
                <div class="achievement-title">${achievement.title}</div>
                <div class="achievement-desc">${achievement.description}</div>
                <div class="stars">${starsHTML}</div>
                <div style="font-size: 0.7rem; color: #6b7280; margin-top: 5px;">${achievement.date}</div>
            `;
            
            achievementsGrid.appendChild(achievementElement);
        });
    }
}

function updateExportContent() {
    // This function can be expanded with actual export functionality
    console.log('Export content updated');
}

function updateChart() {
    // Simple text representation since we can't use full Chart.js
    const progressText = document.createElement('div');
    progressText.style.textAlign = 'center';
    progressText.style.padding = '20px';
    progressText.style.color = '#6b7280';
    progressText.innerHTML = 'График прогресса<br><small>В реальной версии здесь будет интерактивный график</small>';
    
    const chartContainer = document.getElementById('progress-chart');
    if (chartContainer) {
        chartContainer.innerHTML = '';
        chartContainer.appendChild(progressText);
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

    // Language switch
    elements.languageSwitch.addEventListener('change', () => {
        appData.currentLanguage = elements.languageSwitch.value;
        updateTextContent();
        showNotification('Язык изменён!');
    });

    // Add Grade
    elements.addGradeBtn.addEventListener('click', () => {
        const subject = elements.subject.value.trim();
        const grade = parseInt(elements.grade.value);
        
        // Validate fields
        const isSubjectValid = validateField(
            elements.subject, 
            elements.subjectError, 
            getTranslation('errorEmpty')
        );
        
        if (!isSubjectValid) return;
        
        if (!isNaN(grade)) {
            const newGrade = {
                id: appData.nextId++,
                studentId: 1,
                subject: subject,
                grade: grade,
                date: new Date().toLocaleDateString('ru-RU'),
                teacherId: 1
            };
            
            appData.grades.unshift(newGrade);
            elements.subject.value = '';
            elements.grade.value = 5;
            document.getElementById('grade-value').textContent = 5;
            elements.rangeValue.textContent = 5;
            
            showNotification(getTranslation('notificationGradeAdded'));
            updateContent();
        }
    });

    // Add Achievement
    elements.addAchievementBtn.addEventListener('click', () => {
        const title = elements.achievementTitle.value.trim();
        const desc = elements.achievementDesc.value.trim();
        
        // Validate fields
        const isTitleValid = validateField(
            elements.achievementTitle, 
            elements.achievementTitleError, 
            getTranslation('errorEmpty')
        );
        
        const isDescValid = validateField(
            elements.achievementDesc, 
            elements.achievementDescError, 
            getTranslation('errorEmpty')
        );
        
        if (!isTitleValid || !isDescValid) return;
        
        const newAchievement = {
            id: appData.nextId++,
            studentId: 1,
            title: title,
            description: desc,
            stars: Math.floor(Math.random() * 5) + 1,
            date: new Date().toLocaleDateString('ru-RU')
        };
        
        appData.achievements.unshift(newAchievement);
        elements.achievementTitle.value = '';
        elements.achievementDesc.value = '';
        
        showNotification(getTranslation('notificationAchievementAdded'));
        updateContent();
    });

    // Export functionality
    elements.exportPdf.addEventListener('click', () => {
        showNotification(getTranslation('notificationExportPdf'));
    });

    elements.exportExcel.addEventListener('click', () => {
        showNotification(getTranslation('notificationExportExcel'));
    });

    // Real-time validation
    elements.subject.addEventListener('blur', () => {
        validateField(elements.subject, elements.subjectError, getTranslation('errorEmpty'));
    });

    elements.achievementTitle.addEventListener('blur', () => {
        validateField(elements.achievementTitle, elements.achievementTitleError, getTranslation('errorEmpty'));
    });

    elements.achievementDesc.addEventListener('blur', () => {
        validateField(elements.achievementDesc, elements.achievementDescError, getTranslation('errorEmpty'));
    });
}

// Initialize app
function initApp() {
    // Set current user name
    elements.userName.textContent = appData.currentUser.name;
    
    // Initialize language
    updateTextContent();
    
    // Set up event listeners
    setupEventListeners();
    
    // Initial content update
    updateContent();
    
    // Initialize Lucide icons
    lucide.createIcons();
}

// Start the app when page loads
document.addEventListener('DOMContentLoaded', initApp);