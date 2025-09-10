// components/charts.js

class ChartsComponent {
    constructor() {
        this.charts = new Map();
        this.initCharts();
    }

    initCharts() {
        // В реальной версии здесь инициализировались бы графики
        // Используя библиотеки типа Chart.js, D3.js или Recharts
        
        this.createPlaceholderCharts();
    }

    createPlaceholderCharts() {
        // Создаем placeholder для графиков
        this.createProgressChart();
        this.createGradeDistributionChart();
        this.createClassComparisonChart();
    }

    createProgressChart() {
        // Прогресс по предметам
        const progressData = this.getProgressData();
        const chartContainer = document.getElementById('progress-chart');
        
        if (chartContainer) {
            chartContainer.innerHTML = `
                <div class="chart-placeholder">
                    <h4>Прогресс по предметам</h4>
                    <div class="chart-visualization">
                        ${progressData.map(item => `
                            <div class="chart-bar" style="height: ${item.percentage}%">
                                <span class="bar-label">${item.subject}</span>
                                <span class="bar-value">${item.average}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }

    createGradeDistributionChart() {
        // Распределение оценок
        const stats = api.getStatistics();
        const distributionContainer = document.getElementById('grade-distribution');
        
        if (distributionContainer) {
            distributionContainer.innerHTML = `
                <div class="chart-placeholder">
                    <h4>Распределение оценок</h4>
                    <div class="pie-chart">
                        <div class="pie-segment" style="background: #8b5cf6; width: ${stats.gradeDistribution['9-10']}%"></div>
                        <div class="pie-segment" style="background: #06b6d4; width: ${stats.gradeDistribution['7-8']}%"></div>
                        <div class="pie-segment" style="background: #f97316; width: ${stats.gradeDistribution['4-6']}%"></div>
                        <div class="pie-segment" style="background: #ef4444; width: ${stats.gradeDistribution['1-3']}%"></div>
                    </div>
                    <div class="legend">
                        <div class="legend-item"><span class="legend-color" style="background: #8b5cf6"></span> 9-10 (${stats.gradeDistribution['9-10']})</div>
                        <div class="legend-item"><span class="legend-color" style="background: #06b6d4"></span> 7-8 (${stats.gradeDistribution['7-8']})</div>
                        <div class="legend-item"><span class="legend-color" style="background: #f97316"></span> 4-6 (${stats.gradeDistribution['4-6']})</div>
                        <div class="legend-item"><span class="legend-color" style="background: #ef4444"></span> 1-3 (${stats.gradeDistribution['1-3']})</div>
                    </div>
                </div>
            `;
        }
    }

    createClassComparisonChart() {
        // Сравнение классов
        const classData = this.getClassComparisonData();
        const comparisonContainer = document.getElementById('class-comparison');
        
        if (comparisonContainer) {
            comparisonContainer.innerHTML = `
                <div class="chart-placeholder">
                    <h4>Сравнение классов</h4>
                    <div class="bar-chart">
                        ${classData.map(item => `
                            <div class="bar-group">
                                <span class="bar-label">${item.class}</span>
                                <div class="bar-container">
                                    <div class="bar" style="width: ${item.average * 10}%; background: ${this.getClassColor(item.class)}"></div>
                                    <span class="bar-value">${item.average}</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }

    getProgressData() {
        const grades = api.getGrades();
        const subjectData = {};
        
        grades.forEach(grade => {
            if (!subjectData[grade.subject]) {
                subjectData[grade.subject] = { total: 0, count: 0 };
            }
            subjectData[grade.subject].total += grade.score;
            subjectData[grade.subject].count++;
        });
        
        return Object.keys(subjectData).map(subject => {
            const average = subjectData[subject].total / subjectData[subject].count;
            return {
                subject,
                average: average.toFixed(1),
                percentage: (average * 10) // Масштабируем для визуализации
            };
        }).sort((a, b) => b.average - a.average);
    }

    getClassComparisonData() {
        const grades = api.getGrades();
        const classData = {};
        
        grades.forEach(grade => {
            const student = api.students.find(s => s.id === grade.studentId);
            if (!student) return;
            
            if (!classData[student.class]) {
                classData[student.class] = { total: 0, count: 0 };
            }
            classData[student.class].total += grade.score;
            classData[student.class].count++;
        });
        
        return Object.keys(classData).map(className => {
            const average = classData[className].total / classData[className].count;
            return {
                class: className,
                average: average.toFixed(1)
            };
        });
    }

    getClassColor(className) {
        const colors = {
            '9А': '#8b5cf6',
            '9Б': '#06b6d4',
            '10А': '#f97316',
            '10Б': '#10b981'
        };
        return colors[className] || '#6b7280';
    }

    updateCharts() {
        // Обновление всех графиков при изменении данных
        this.createPlaceholderCharts();
    }

    // В реальной версии здесь были бы методы для реальных графиков
    createRealChart(chartType, data, container) {
        // Пример использования Chart.js
        /*
        const ctx = container.getContext('2d');
        new Chart(ctx, {
            type: chartType,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
        */
    }
}

// Initialize charts component
const charts = new ChartsComponent();