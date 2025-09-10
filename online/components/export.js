// components/export.js

class ExportComponent {
    constructor() {
        this.exportPdfBtn = document.getElementById('export-pdf-btn');
        this.exportExcelBtn = document.getElementById('export-excel-btn');
        this.exportStatsBtn = document.getElementById('export-stats-btn');
        
        this.bindEvents();
    }

    bindEvents() {
        if (this.exportPdfBtn) {
            this.exportPdfBtn.addEventListener('click', () => {
                this.exportToPDF();
            });
        }

        if (this.exportExcelBtn) {
            this.exportExcelBtn.addEventListener('click', () => {
                this.exportToExcel();
            });
        }

        if (this.exportStatsBtn) {
            this.exportStatsBtn.addEventListener('click', () => {
                this.exportStatistics();
            });
        }
    }

    exportToPDF() {
        const user = api.getCurrentUser();
        const grades = api.getGrades();
        const students = api.getStudents();
        
        // В реальной версии использовалась бы библиотека jsPDF
        const pdfContent = `
# Электронный школьный журнал
## Отчет за ${new Date().toLocaleDateString('ru-RU')}

**Пользователь:** ${user.name} (${user.role})
**Роль:** ${user.role === 'admin' ? 'Администратор' : user.role === 'teacher' ? 'Учитель' : 'Ученик'}

---

### Статистика
- Всего оценок: ${grades.length}
- Средний балл: ${this.calculateAverageScore(grades)}
- Количество учеников: ${students.length}

---

### Последние оценки
${grades.slice(0, 10).map(grade => {
    const student = api.students.find(s => s.id === grade.studentId);
    return `- ${student ? student.name : 'Ученик'}: ${grade.score} по ${grade.subject} (${grade.work}) - ${grade.date}`;
}).join('\n')}

---

Сгенерировано автоматически
        `;

        // В реальной версии:
        // const { jsPDF } = window.jspdf;
        // const doc = new jsPDF();
        // doc.text(pdfContent, 10, 10);
        // doc.save('журнал.pdf');

        showNotification('PDF отчет готов к скачиванию!');
        
        // Для демонстрации - создаем "файл" для скачивания
        this.downloadFile('журнал.txt', pdfContent);
    }

    exportToExcel() {
        const user = api.getCurrentUser();
        const grades = api.getGrades();
        
        // Формат CSV
        let csvContent = 'data:text/csv;charset=utf-8,';
        csvContent += 'Ученик,Класс,Предмет,Работа,Оценка,Дата,Учитель,Комментарий\n';
        
        grades.forEach(grade => {
            const student = api.students.find(s => s.id === grade.studentId);
            const studentName = student ? student.name : 'Неизвестно';
            const studentClass = student ? student.class : '—';
            
            csvContent += `"${studentName}","${studentClass}","${grade.subject}","${grade.work}",${grade.score},"${grade.date}","${grade.teacher}","${grade.comment || ''}"\n`;
        });

        // Создаем ссылку для скачивания
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `журнал_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showNotification('Данные экспортированы в CSV!');
    }

    exportStatistics() {
        const stats = api.getStatistics();
        const grades = api.getGrades();
        
        const statsContent = `
# Статистика успеваемости
## ${new Date().toLocaleDateString('ru-RU')}

**Общая статистика:**
- Всего оценок: ${stats.totalGrades}
- Средний балл: ${stats.averageScore}

**Распределение оценок:**
- 9-10: ${stats.gradeDistribution['9-10']} (${this.calculatePercentage(stats.gradeDistribution['9-10'], stats.totalGrades)}%)
- 7-8: ${stats.gradeDistribution['7-8']} (${this.calculatePercentage(stats.gradeDistribution['7-8'], stats.totalGrades)}%)
- 4-6: ${stats.gradeDistribution['4-6']} (${this.calculatePercentage(stats.gradeDistribution['4-6'], stats.totalGrades)}%)
- 1-3: ${stats.gradeDistribution['1-3']} (${this.calculatePercentage(stats.gradeDistribution['1-3'], stats.totalGrades)}%)

**Топ предметов:**
${this.getTopSubjects(grades)}

**Рекомендации:**
${this.getRecommendations(stats)}
        `;

        // В реальной версии генерировался бы PDF с графиками
        showNotification('Статистический отчет готов!');
        
        // Для демонстрации
        this.downloadFile('статистика.txt', statsContent);
    }

    calculateAverageScore(grades) {
        if (grades.length === 0) return '0.0';
        const sum = grades.reduce((acc, grade) => acc + grade.score, 0);
        return (sum / grades.length).toFixed(1);
    }

    calculatePercentage(value, total) {
        if (total === 0) return '0';
        return ((value / total) * 100).toFixed(1);
    }

    getTopSubjects(grades) {
        const subjectCounts = {};
        const subjectScores = {};
        
        grades.forEach(grade => {
            subjectCounts[grade.subject] = (subjectCounts[grade.subject] || 0) + 1;
            subjectScores[grade.subject] = (subjectScores[grade.subject] || 0) + grade.score;
        });
        
        const sortedSubjects = Object.keys(subjectCounts)
            .sort((a, b) => subjectCounts[b] - subjectCounts[a])
            .slice(0, 3);
            
        return sortedSubjects.map((subject, index) => {
            const avgScore = (subjectScores[subject] / subjectCounts[subject]).toFixed(1);
            return `${index + 1}. ${subject} - ${subjectCounts[subject]} оценок (ср. ${avgScore})`;
        }).join('\n');
    }

    getRecommendations(stats) {
        const recommendations = [];
        
        if (stats.averageScore < 6.0) {
            recommendations.push('Рекомендуется уделить больше внимания учебе и обратиться к учителям за помощью.');
        } else if (stats.averageScore < 8.0) {
            recommendations.push('Хорошие результаты! Продолжайте в том же духе и старайтесь улучшить слабые предметы.');
        } else {
            recommendations.push('Отличные результаты! Рекомендуется участвовать в олимпиадах и конкурсах.');
        }
        
        if (stats.gradeDistribution['1-3'] > 0) {
            recommendations.push('Обратите внимание на предметы с низкими оценками и проконсультируйтесь с учителями.');
        }
        
        if (recommendations.length === 0) {
            recommendations.push('Продолжайте в том же духе!');
        }
        
        return recommendations.join('\n');
    }

    downloadFile(filename, content) {
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize export component
const exporter = new ExportComponent();