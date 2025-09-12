// server.js
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Secret key for JWT (в реальном проекте использовать .env)
const JWT_SECRET = 'school-journal-secret-key-2024';

// In-memory data storage (в реальном проекте заменить на базу данных)
let students = [
    { id: 1, name: "Алексей Иванов", class: "9А", contact: "alex@example.com" },
    { id: 2, name: "Мария Петрова", class: "9А", contact: "maria@example.com" },
    { id: 3, name: "Иван Сидоров", class: "9Б", contact: "ivan@example.com" },
    { id: 4, name: "Елена Козлова", class: "9Б", contact: "elena@example.com" }
];

let grades = [
    { id: 1, studentId: 1, subject: "Математика", work: "Контрольная работа", date: "2024-01-15", score: 9, comment: "Отлично!", weight: 1.0, teacherId: 1 },
    { id: 2, studentId: 1, subject: "Русский язык", work: "Сочинение", date: "2024-01-14", score: 7, comment: "Хорошо, но нужно работать над грамматикой", weight: 1.0, teacherId: 2 },
    { id: 3, studentId: 1, subject: "Физика", work: "Лабораторная работа", date: "2024-01-13", score: 10, comment: "Безупречно!", weight: 1.2, teacherId: 1 },
    { id: 4, studentId: 2, subject: "Математика", work: "Контрольная работа", date: "2024-01-15", score: 8, comment: "Хорошо!", weight: 1.0, teacherId: 1 }
];

let goals = [
    { id: 1, studentId: 1, text: "Подтянуть Python", completed: false, targetDate: "2024-03-01", createdAt: "2024-01-10" },
    { id: 2, studentId: 1, text: "Подготовиться к олимпиаде по математике", completed: true, targetDate: "2024-02-15", createdAt: "2024-01-05" },
    { id: 3, studentId: 2, text: "Улучшить орфографию", completed: false, targetDate: "2024-04-01", createdAt: "2024-01-12" }
];

let achievements = [
    { id: 1, studentId: 1, title: "Победитель школьной олимпиады", description: "1 место в олимпиаде по математике", date: "2024-01-10", category: "Олимпиады" },
    { id: 2, studentId: 1, title: "Лучший проект по информатике", description: "Высшая оценка за проект", date: "2024-01-08", category: "Проекты" },
    { id: 3, studentId: 2, title: "Читатель года", description: "Прочитал 20 книг за год", date: "2023-12-20", category: "Чтение" }
];

let users = [
    { id: 1, username: "olga", password: "$2b$10$z.z.z.z.z.z.z.z.z.z.z.z.z.z.z.z", role: "teacher", subject: "Математика", name: "Ольга Петровна" },
    { id: 2, username: "anna", password: "$2b$10$z.z.z.z.z.z.z.z.z.z.z.z.z.z.z.z", role: "teacher", subject: "Русский язык", name: "Анна Сергеевна" },
    { id: 3, username: "admin", password: "$2b$10$z.z.z.z.z.z.z.z.z.z.z.z.z.z.z.z", role: "admin", name: "Администратор" },
    { id: 4, username: "alex_ivanov", password: "$2b$10$z.z.z.z.z.z.z.z.z.z.z.z.z.z.z.z", role: "student", studentId: 1, name: "Алексей Иванов" }
];

// Генерация хеша пароля (для демо)
const generatePasswordHash = async (password) => {
    return await bcrypt.hash(password, 10);
};

// Мидлвар для аутентификации
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: 'Требуется авторизация' });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Недействительный токен' });
        }
        req.user = user;
        next();
    });
};

// Мидлвар для проверки роли
const authorizeRole = (...allowedRoles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Неавторизованный доступ' });
        }
        
        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Недостаточно прав' });
        }
        next();
    };
};

// Тестовый маршрут
app.get('/', (req, res) => {
    res.json({ message: 'API для электронного журнала работает!', version: '1.0' });
});

// Аутентификация
app.post('/api/auth/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // Валидация
        if (!username || !password) {
            return res.status(400).json({ error: 'Все поля обязательны' });
        }

        const user = users.find(u => u.username === username);
        if (!user) {
            return res.status(400).json({ error: 'Неверное имя пользователя или пароль' });
        }

        // В демо-режиме пропускаем проверку пароля для удобства
        // В реальном проекте раскомментировать:
        // const match = await bcrypt.compare(password, user.password);
        // if (!match) {
        //     return res.status(400).json({ error: 'Неверное имя пользователя или пароль' });
        // }

        const token = jwt.sign(
            { id: user.id, role: user.role, username: user.username },
            JWT_SECRET,
            { expiresIn: '24h' }
        );

        res.json({
            token,
            user: {
                id: user.id,
                username: user.username,
                role: user.role,
                name: user.name,
                subject: user.subject
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Ошибка сервера' });
    }
});

app.post('/api/auth/register', authorizeRole('admin'), async (req, res) => {
    try {
        const { username, password, role, name, subject, class: studentClass, contact } = req.body;
        
        // Валидация
        if (!username || !password || !role || !name) {
            return res.status(400).json({ error: 'Все обязательные поля должны быть заполнены' });
        }

        if (users.find(u => u.username === username)) {
            return res.status(400).json({ error: 'Пользователь с таким именем уже существует' });
        }

        const hashedPassword = await generatePasswordHash(password);
        const userId = users.length > 0 ? Math.max(...users.map(u => u.id)) + 1 : 1;
        
        let newUser;
        
        if (role === 'student') {
            // Создаем ученика
            const studentId = students.length > 0 ? Math.max(...students.map(s => s.id)) + 1 : 1;
            const newStudent = {
                id: studentId,
                name,
                class: studentClass,
                contact: contact || null
            };
            students.push(newStudent);
            
            newUser = {
                id: userId,
                username,
                password: hashedPassword,
                role,
                studentId,
                name
            };
        } else {
            newUser = {
                id: userId,
                username,
                password: hashedPassword,
                role,
                subject: subject || null,
                name
            };
        }

        users.push(newUser);
        res.status(201).json({ 
            message: 'Пользователь зарегистрирован успешно',
            user: {
                id: newUser.id,
                username: newUser.username,
                role: newUser.role,
                name: newUser.name
            }
        });
    } catch (error) {
        console.error('Register error:', error);
        res.status(500).json({ error: 'Ошибка сервера' });
    }
});

// Ученики
app.get('/api/students', authenticateToken, (req, res) => {
    try {
        let filteredStudents = [...students];
        
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId) {
                const student = students.find(s => s.id === userStudent.studentId);
                filteredStudents = student ? [student] : [];
            } else {
                filteredStudents = [];
            }
        } else if (req.user.role === 'teacher') {
            // Учитель видит всех учеников
            filteredStudents = students;
        }
        
        // Фильтрация по классу
        if (req.query.class && req.query.class !== 'all') {
            filteredStudents = filteredStudents.filter(s => s.class === req.query.class);
        }
        
        res.json(filteredStudents);
    } catch (error) {
        console.error('Get students error:', error);
        res.status(500).json({ error: 'Ошибка при получении списка учеников' });
    }
});

app.get('/api/students/:id', authenticateToken, (req, res) => {
    try {
        const studentId = parseInt(req.params.id);
        const student = students.find(s => s.id === studentId);
        
        if (!student) {
            return res.status(404).json({ error: 'Ученик не найден' });
        }
        
        // Проверка прав доступа
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId !== studentId) {
                return res.status(403).json({ error: 'Недостаточно прав' });
            }
        }
        
        res.json(student);
    } catch (error) {
        console.error('Get student error:', error);
        res.status(500).json({ error: 'Ошибка при получении данных ученика' });
    }
});

app.post('/api/students', authenticateToken, authorizeRole('admin'), (req, res) => {
    try {
        const { name, class: studentClass, contact } = req.body;
        
        if (!name || !studentClass) {
            return res.status(400).json({ error: 'Имя и класс обязательны' });
        }

        const newStudent = {
            id: students.length > 0 ? Math.max(...students.map(s => s.id)) + 1 : 1,
            name,
            class: studentClass,
            contact: contact || null
        };

        students.push(newStudent);
        res.status(201).json(newStudent);
    } catch (error) {
        console.error('Add student error:', error);
        res.status(500).json({ error: 'Ошибка при добавлении ученика' });
    }
});

// Оценки
app.get('/api/grades', authenticateToken, (req, res) => {
    try {
        let filteredGrades = [...grades];
        
        // Фильтрация по ролям
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId) {
                filteredGrades = filteredGrades.filter(g => g.studentId === userStudent.studentId);
            } else {
                filteredGrades = [];
            }
        } else if (req.user.role === 'teacher') {
            filteredGrades = filteredGrades.filter(g => {
                const teacher = users.find(u => u.id === g.teacherId);
                return teacher && teacher.subject === req.user.subject;
            });
        }
        
        // Фильтрация по параметрам
        if (req.query.studentId) {
            filteredGrades = filteredGrades.filter(g => g.studentId === parseInt(req.query.studentId));
        }
        
        if (req.query.subject && req.query.subject !== 'all') {
            filteredGrades = filteredGrades.filter(g => g.subject === req.query.subject);
        }
        
        if (req.query.class && req.query.class !== 'all') {
            const classStudents = students.filter(s => s.class === req.query.class).map(s => s.id);
            filteredGrades = filteredGrades.filter(g => classStudents.includes(g.studentId));
        }
        
        res.json(filteredGrades);
    } catch (error) {
        console.error('Get grades error:', error);
        res.status(500).json({ error: 'Ошибка при получении оценок' });
    }
});

app.get('/api/grades/:id', authenticateToken, (req, res) => {
    try {
        const gradeId = parseInt(req.params.id);
        const grade = grades.find(g => g.id === gradeId);
        
        if (!grade) {
            return res.status(404).json({ error: 'Оценка не найдена' });
        }
        
        // Проверка прав доступа
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId !== grade.studentId) {
                return res.status(403).json({ error: 'Недостаточно прав' });
            }
        }
        
        if (req.user.role === 'teacher' && req.user.id !== grade.teacherId) {
            return res.status(403).json({ error: 'Вы можете просматривать только свои оценки' });
        }
        
        res.json(grade);
    } catch (error) {
        console.error('Get grade error:', error);
        res.status(500).json({ error: 'Ошибка при получении оценки' });
    }
});

app.post('/api/grades', authenticateToken, authorizeRole('teacher'), (req, res) => {
    try {
        const { studentId, subject, work, score, comment, weight = 1.0 } = req.body;
        
        // Валидация
        if (!studentId || !subject || !work || score === undefined) {
            return res.status(400).json({ error: 'Все обязательные поля должны быть заполнены' });
        }
        
        if (score < 1 || score > 10) {
            return res.status(400).json({ error: 'Оценка должна быть от 1 до 10' });
        }
        
        if (!students.find(s => s.id === studentId)) {
            return res.status(404).json({ error: 'Ученик не найден' });
        }
        
        const newGrade = {
            id: grades.length > 0 ? Math.max(...grades.map(g => g.id)) + 1 : 1,
            studentId,
            subject,
            work,
            date: new Date().toISOString().split('T')[0],
            score,
            comment: comment || null,
            weight,
            teacherId: req.user.id
        };
        
        grades.push(newGrade);
        res.status(201).json(newGrade);
    } catch (error) {
        console.error('Add grade error:', error);
        res.status(500).json({ error: 'Ошибка при добавлении оценки' });
    }
});

app.put('/api/grades/:id', authenticateToken, authorizeRole('teacher'), (req, res) => {
    try {
        const gradeId = parseInt(req.params.id);
        const grade = grades.find(g => g.id === gradeId);
        
        if (!grade) {
            return res.status(404).json({ error: 'Оценка не найдена' });
        }
        
        // Учитель может редактировать только свои оценки
        if (grade.teacherId !== req.user.id) {
            return res.status(403).json({ error: 'Вы можете редактировать только свои оценки' });
        }
        
        const { score, comment, weight } = req.body;
        
        if (score !== undefined) {
            if (score < 1 || score > 10) {
                return res.status(400).json({ error: 'Оценка должна быть от 1 до 10' });
            }
            grade.score = score;
        }
        
        if (comment !== undefined) {
            grade.comment = comment;
        }
        
        if (weight !== undefined) {
            grade.weight = weight;
        }
        
        grade.date = new Date().toISOString().split('T')[0]; // Обновляем дату
        
        res.json(grade);
    } catch (error) {
        console.error('Update grade error:', error);
        res.status(500).json({ error: 'Ошибка при обновлении оценки' });
    }
});

// Цели
app.get('/api/goals', authenticateToken, (req, res) => {
    try {
        let filteredGoals = [...goals];
        
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId) {
                filteredGoals = filteredGoals.filter(g => g.studentId === userStudent.studentId);
            } else {
                filteredGoals = [];
            }
        }
        
        if (req.query.studentId && req.user.role !== 'student') {
            filteredGoals = filteredGoals.filter(g => g.studentId === parseInt(req.query.studentId));
        }
        
        res.json(filteredGoals);
    } catch (error) {
        console.error('Get goals error:', error);
        res.status(500).json({ error: 'Ошибка при получении целей' });
    }
});

// Достижения
app.get('/api/achievements', authenticateToken, (req, res) => {
    try {
        let filteredAchievements = [...achievements];
        
        if (req.user.role === 'student') {
            const userStudent = users.find(u => u.id === req.user.id);
            if (userStudent && userStudent.studentId) {
                filteredAchievements = filteredAchievements.filter(a => a.studentId === userStudent.studentId);
            } else {
                filteredAchievements = [];
            }
        }
        
        if (req.query.studentId && req.user.role !== 'student') {
            filteredAchievements = filteredAchievements.filter(a => a.studentId === parseInt(req.query.studentId));
        }
        
        res.json(filteredAchievements);
    } catch (error) {
        console.error('Get achievements error:', error);
        res.status(500).json({ error: 'Ошибка при получении достижений' });
    }
});

// Профиль
app.get('/api/profile', authenticateToken, (req, res) => {
    try {
        const user = users.find(u => u.id === req.user.id);
        if (!user) {
            return res.status(404).json({ error: 'Пользователь не найден' });
        }
        
        const profile = {
            id: user.id,
            username: user.username,
            role: user.role,
            name: user.name,
            subject: user.subject
        };
        
        if (req.user.role === 'student') {
            const student = students.find(s => s.id === user.studentId);
            if (student) {
                profile.studentInfo = student;
            }
        }
        
        res.json({ user: profile });
    } catch (error) {
        console.error('Get profile error:', error);
        res.status(500).json({ error: 'Ошибка при получении профиля' });
    }
});

// Обработка ошибок
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Внутренняя ошибка сервера' });
});

// Маршрут для несуществующих эндпоинтов
app.use((req, res) => {
    res.status(404).json({ error: 'Маршрут не найден' });
});

app.listen(PORT, () => {
    console.log(`Сервер запущен на порту ${PORT}`);
    console.log(`API доступно по адресу: http://localhost:${PORT}`);
    console.log(`Для тестирования используйте следующие демо-пользователи:`);
    console.log(`- Ученик: login: "alex_ivanov", password: "123"`);
    console.log(`- Учитель: login: "olga", password: "123"`);
    console.log(`- Админ: login: "admin", password: "admin"`);
});

module.exports = app;