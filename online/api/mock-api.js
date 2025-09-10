// api/mock-api.js

class MockAPI {
    constructor() {
        this.students = [
            { id: 1, name: "Алексей Иванов", class: "9А", contact: "alex@example.com", username: "alex_ivanov" },
            { id: 2, name: "Мария Петрова", class: "9А", contact: "maria@example.com", username: "maria_petrova" },
            { id: 3, name: "Иван Сидоров", class: "9Б", contact: "ivan@example.com", username: "ivan_sidorov" },
            { id: 4, name: "Елена Козлова", class: "9Б", contact: "elena@example.com", username: "elena_kozlova" }
        ];

        this.grades = [
            { id: 1, studentId: 1, subject: "Математика", work: "Контрольная работа", date: "2024-01-15", score: 9, comment: "Отлично!", weight: 1.0, teacher: "Ольга Петровна" },
            { id: 2, studentId: 1, subject: "Русский язык", work: "Сочинение", date: "2024-01-14", score: 7, comment: "Хорошо, но нужно работать над грамматикой", weight: 1.0, teacher: "Анна Сергеевна" },
            { id: 3, studentId: 1, subject: "Физика", work: "Лабораторная работа", date: "2024-01-13", score: 10, comment: "Безупречно!", weight: 1.2, teacher: "Ольга Петровна" },
            { id: 4, studentId: 2, subject: "Математика", work: "Контрольная работа", date: "2024-01-15", score: 8, comment: "Хорошо!", weight: 1.0, teacher: "Ольга Петровна" },
            { id: 5, studentId: 2, subject: "Русский язык", work: "Диктант", date: "2024-01-12", score: 9, comment: "Отлично!", weight: 1.0, teacher: "Анна Сергеевна" },
            { id: 6, studentId: 3, subject: "Математика", work: "Тест", date: "2024-01-15", score: 6, comment: "Нужно повторить тему", weight: 1.0, teacher: "Ольга Петровна" }
        ];

        this.goals = [
            { id: 1, studentId: 1, text: "Подтянуть Python", completed: false, targetDate: "2024-03-01", createdAt: "2024-01-10" },
            { id: 2, studentId: 1, text: "Подготовиться к олимпиаде по математике", completed: true, targetDate: "2024-02-15", createdAt: "2024-01-05" },
            { id: 3, studentId: 2, text: "Улучшить орфографию", completed: false, targetDate: "2024-04-01", createdAt: "2024-01-12" }
        ];

        this.achievements = [
            { id: 1, studentId: 1, title: "Победитель школьной олимпиады", description: "1 место в олимпиаде по математике", date: "2024-01-10", category: "Олимпиады" },
            { id: 2, studentId: 1, title: "Лучший проект по информатике", description: "Высшая оценка за проект", date: "2024-01-08", category: "Проекты" },
            { id: 3, studentId: 2, title: "Читатель года", description: "Прочитал 20 книг за год", date: "2023-12-20", category: "Чтение" }
        ];

        this.users = [
            { id: 1, username: "olga", password: "123", role: "teacher", subject: "Математика", name: "Ольга Петровна" },
            { id: 2, username: "anna", password: "123", role: "teacher", subject: "Русский язык", name: "Анна Сергеевна" },
            { id: 3, username: "admin", password: "admin", role: "admin", name: "Администратор" },
            { id: 4, username: "alex_ivanov", password: "123", role: "student", studentId: 1, name: "Алексей Иванов" }
        ];

        this.currentUser = null;
        this.nextId = 100;
    }

    // Authentication
    login(username, password) {
        const user = this.users.find(u => u.username === username && u.password === password);
        if (user) {
            this.currentUser = { ...user };
            return { success: true, user: this.currentUser };
        }
        return { success: false, error: "Неверный логин или пароль" };
    }

    logout() {
        this.currentUser = null;
    }

    getCurrentUser() {
        return this.currentUser;
    }

    // Students
    getStudents() {
        if (!this.currentUser) return [];
        
        if (this.currentUser.role === 'student') {
            const student = this.students.find(s => s.username === this.currentUser.username);
            return student ? [student] : [];
        }
        
        return this.students;
    }

    addStudent(studentData) {
        if (!this.currentUser || this.currentUser.role !== 'admin') {
            return { success: false, error: "Недостаточно прав" };
        }

        const newStudent = {
            id: this.nextId++,
            ...studentData
        };

        this.students.push(newStudent);

        // Создаем пользователя для ученика
        this.users.push({
            id: this.nextId++,
            username: studentData.username,
            password: studentData.password,
            role: 'student',
            studentId: newStudent.id,
            name: studentData.name
        });

        return { success: true, student: newStudent };
    }

    // Grades
    getGrades() {
        if (!this.currentUser) return [];
        
        let filteredGrades = [...this.grades];
        
        if (this.currentUser.role === 'student') {
            const student = this.students.find(s => s.username === this.currentUser.username);
            if (student) {
                filteredGrades = filteredGrades.filter(g => g.studentId === student.id);
            }
        } else if (this.currentUser.role === 'teacher') {
            filteredGrades = filteredGrades.filter(g => {
                return this.currentUser.subject === g.subject;
            });
        }
        
        return filteredGrades;
    }

    addGrade(gradeData) {
        if (!this.currentUser || this.currentUser.role !== 'teacher') {
            return { success: false, error: "Недостаточно прав" };
        }

        const newGrade = {
            id: this.nextId++,
            ...gradeData,
            date: new Date().toISOString().split('T')[0],
            teacher: this.currentUser.name
        };

        this.grades.push(newGrade);
        return { success: true, grade: newGrade };
    }

    // Goals
    getGoals() {
        if (!this.currentUser) return [];
        
        let filteredGoals = [...this.goals];
        
        if (this.currentUser.role === 'student') {
            const student = this.students.find(s => s.username === this.currentUser.username);
            if (student) {
                filteredGoals = filteredGoals.filter(g => g.studentId === student.id);
            }
        }
        
        return filteredGoals;
    }

    addGoal(goalData) {
        if (!this.currentUser || this.currentUser.role !== 'student') {
            return { success: false, error: "Только ученики могут добавлять цели" };
        }

        const student = this.students.find(s => s.username === this.currentUser.username);
        if (!student) {
            return { success: false, error: "Ученик не найден" };
        }

        const newGoal = {
            id: this.nextId++,
            studentId: student.id,
            ...goalData,
            completed: false,
            createdAt: new Date().toISOString().split('T')[0]
        };

        this.goals.push(newGoal);
        return { success: true, goal: newGoal };
    }

    // Achievements
    getAchievements() {
        if (!this.currentUser) return [];
        
        let filteredAchievements = [...this.achievements];
        
        if (this.currentUser.role === 'student') {
            const student = this.students.find(s => s.username === this.currentUser.username);
            if (student) {
                filteredAchievements = filteredAchievements.filter(a => a.studentId === student.id);
            }
        }
        
        return filteredAchievements;
    }

    addAchievement(achievementData) {
        if (!this.currentUser || this.currentUser.role !== 'teacher') {
            return { success: false, error: "Только учителя могут добавлять достижения" };
        }

        const newAchievement = {
            id: this.nextId++,
            ...achievementData,
            date: new Date().toISOString().split('T')[0]
        };

        this.achievements.push(newAchievement);
        return { success: true, achievement: newAchievement };
    }

    // Statistics
    getStatistics() {
        const allGrades = this.getGrades();
        
        const stats = {
            totalGrades: allGrades.length,
            averageScore: allGrades.length > 0 ? 
                Math.round(allGrades.reduce((sum, g) => sum + g.score, 0) / allGrades.length * 10) / 10 : 0,
            gradeDistribution: {
                '1-3': allGrades.filter(g => g.score >= 1 && g.score <= 3).length,
                '4-6': allGrades.filter(g => g.score >= 4 && g.score <= 6).length,
                '7-8': allGrades.filter(g => g.score >= 7 && g.score <= 8).length,
                '9-10': allGrades.filter(g => g.score >= 9 && g.score <= 10).length
            }
        };

        return stats;
    }
}

// Create global API instance
const api = new MockAPI();