import React, { useState, useEffect } from "react";
import { Star, Trophy, CheckCircle, BookOpen, ChartLine, Smile, Meh, Frown, Plus, Award, Target } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const App = () => {
  const [activeTab, setActiveTab] = useState("home");
  const [studentName] = useState("Алексей");
  const [grades, setGrades] = useState([
    { id: 1, subject: "Математика", grade: 9, date: "2024-01-15" },
    { id: 2, subject: "Русский язык", grade: 7, date: "2024-01-14" },
    { id: 3, subject: "Физика", grade: 10, date: "2024-01-13" },
    { id: 4, subject: "История", grade: 6, date: "2024-01-12" },
    { id: 5, subject: "Биология", grade: 8, date: "2024-01-11" },
  ]);
  const [newGrade, setNewGrade] = useState({ subject: "", grade: 5 });
  const [goals, setGoals] = useState([
    { id: 1, text: "Подготовиться к контрольной по математике", completed: false },
    { id: 2, text: "Прочитать главу по литературе", completed: true },
    { id: 3, text: "Сдать проект по информатике", completed: false },
  ]);
  const [achievements, setAchievements] = useState([
    { id: 1, title: "Лучший в математике", description: "Высокие оценки за четверть", stars: 5, type: "math" },
    { id: 2, title: "Читатель года", description: "Прочитал 10 книг", stars: 3, type: "reading" },
  ]);
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState("");
  const [newAchievement, setNewAchievement] = useState({ title: "", description: "" });

  const gradeEmoji = (grade) => {
    if (grade >= 9) return "🥳";
    if (grade >= 7) return "😊";
    if (grade >= 5) return "😕";
    if (grade >= 3) return "🙁";
    return "😞";
  };

  const getGradeColor = (grade) => {
    if (grade >= 9) return "text-purple-600";
    if (grade >= 7) return "text-blue-500";
    if (grade >= 5) return "text-yellow-500";
    return "text-red-500";
  };

  const addGrade = () => {
    if (newGrade.subject.trim() && newGrade.grade) {
      const newGradeObj = {
        id: Date.now(),
        subject: newGrade.subject,
        grade: parseInt(newGrade.grade),
        date: new Date().toISOString().split('T')[0]
      };
      setGrades([newGradeObj, ...grades]);
      setNewGrade({ subject: "", grade: 5 });
    }
  };

  const toggleGoal = (id) => {
    const updatedGoals = goals.map(goal => 
      goal.id === id ? { ...goal, completed: !goal.completed } : goal
    );
    setGoals(updatedGoals);
    
    const goal = goals.find(g => g.id === id);
    if (!goal.completed) {
      setNotificationMessage(`Отлично! Вы выполнили цель: "${goal.text}"`);
      setShowNotification(true);
      setTimeout(() => setShowNotification(false), 3000);
    }
  };

  const addAchievement = () => {
    if (newAchievement.title.trim() && newAchievement.description.trim()) {
      const achievement = {
        id: Date.now(),
        title: newAchievement.title,
        description: newAchievement.description,
        stars: Math.floor(Math.random() * 5) + 1,
        type: ["math", "reading", "science", "art", "sports"][Math.floor(Math.random() * 5)]
      };
      setAchievements([achievement, ...achievements]);
      setNewAchievement({ title: "", description: "" });
    }
  };

  const getRecentGrades = () => {
    return grades.slice(0, 3);
  };

  const getActiveGoals = () => {
    return goals.filter(goal => !goal.completed);
  };

  const getProgressData = () => {
    const data = grades.slice(-7).map((grade, index) => ({
      name: grade.subject.substring(0, 3),
      score: grade.grade
    }));
    return data.length > 0 ? data : [{ name: 'Нет данных', score: 0 }];
  };

  const tabs = [
    { id: "home", label: "Главная", icon: BookOpen },
    { id: "grades", label: "Оценки", icon: ChartLine },
    { id: "goals", label: "Цели", icon: Target },
    { id: "achievements", label: "Достижения", icon: Trophy },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-cyan-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="max-w-md mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-purple-700 text-center">
            Мой цифровой дневник успеха
          </h1>
          {activeTab === "home" && (
            <p className="text-center text-gray-600 mt-1">Привет, {studentName}!</p>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-md mx-auto px-4 py-6 pb-20">
        <AnimatePresence mode="wait">
          {activeTab === "home" && (
            <motion.div
              key="home"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Welcome Card */}
              <motion.div 
                className="bg-white rounded-2xl shadow-xl p-6 text-center"
                whileHover={{ scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <div className="text-6xl mb-4">🌟</div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  Привет, {studentName}!
                </h2>
                <p className="text-gray-600">Ты на правильном пути к успеху!</p>
              </motion.div>

              {/* Recent Grades Widget */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <Star className="w-5 h-5 text-yellow-500 mr-2" />
                  Последние оценки
                </h3>
                <div className="space-y-3">
                  {getRecentGrades().map((grade) => (
                    <motion.div
                      key={grade.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-xl"
                      whileHover={{ scale: 1.02 }}
                    >
                      <div className="flex items-center">
                        <span className={`text-lg font-bold ${getGradeColor(grade.grade)} mr-2`}>
                          {grade.grade}
                        </span>
                        <span className="text-gray-700">{grade.subject}</span>
                      </div>
                      <span className="text-2xl">{gradeEmoji(grade.grade)}</span>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Active Goals Widget */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                  <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                  Активные цели
                </h3>
                {getActiveGoals().length > 0 ? (
                  <div className="space-y-2">
                    {getActiveGoals().slice(0, 3).map((goal) => (
                      <motion.div
                        key={goal.id}
                        className="flex items-center p-3 bg-blue-50 rounded-xl"
                        whileHover={{ scale: 1.02 }}
                      >
                        <span className="text-blue-600 mr-2">🎯</span>
                        <span className="text-gray-700 text-sm">{goal.text}</span>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    <p>🎉 Все цели выполнены!</p>
                    <p className="text-sm mt-1">Добавьте новые цели</p>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === "grades" && (
            <motion.div
              key="grades"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Add Grade Form */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Добавить оценку</h3>
                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="Название предмета"
                    value={newGrade.subject}
                    onChange={(e) => setNewGrade({ ...newGrade, subject: e.target.value })}
                    className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                  <div className="flex items-center space-x-4">
                    <label className="text-gray-700 font-medium">Оценка:</label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={newGrade.grade}
                      onChange={(e) => setNewGrade({ ...newGrade, grade: e.target.value })}
                      className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                    />
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-bold">
                      {newGrade.grade}
                    </span>
                  </div>
                  <button
                    onClick={addGrade}
                    className="w-full bg-gradient-to-r from-purple-500 to-purple-600 text-white py-3 rounded-xl font-semibold hover:from-purple-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
                  >
                    Добавить оценку
                  </button>
                </div>
              </div>

              {/* Grades List */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Все оценки</h3>
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {grades.map((grade) => (
                    <motion.div
                      key={grade.id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-xl"
                      whileHover={{ scale: 1.02 }}
                    >
                      <div className="flex items-center">
                        <span className={`text-2xl font-bold ${getGradeColor(grade.grade)} mr-3`}>
                          {grade.grade}
                        </span>
                        <div>
                          <p className="font-medium text-gray-800">{grade.subject}</p>
                          <p className="text-sm text-gray-500">{grade.date}</p>
                        </div>
                      </div>
                      <span className="text-3xl">{gradeEmoji(grade.grade)}</span>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Progress Chart */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Прогресс</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={getProgressData()}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="name" stroke="#888" />
                      <YAxis domain={[1, 10]} stroke="#888" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          border: 'none',
                          borderRadius: '12px',
                          boxShadow: '0 4px 20px rgba(0,0,0,0.15)'
                        }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="score" 
                        stroke="#8b5cf6" 
                        strokeWidth={3}
                        dot={{ r: 6, fill: '#8b5cf6' }}
                        activeDot={{ r: 8, fill: '#7c3aed' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === "goals" && (
            <motion.div
              key="goals"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center">
                  <Target className="w-5 h-5 text-orange-500 mr-2" />
                  Мои цели
                </h3>
                <div className="space-y-3">
                  {goals.map((goal) => (
                    <motion.div
                      key={goal.id}
                      className={`flex items-center p-4 rounded-xl transition-all duration-300 ${
                        goal.completed 
                          ? 'bg-green-50 border-l-4 border-green-500' 
                          : 'bg-blue-50 border-l-4 border-blue-500'
                      }`}
                      whileHover={{ scale: 1.02 }}
                      onClick={() => toggleGoal(goal.id)}
                    >
                      <div className={`w-6 h-6 rounded-full border-2 mr-3 flex items-center justify-center ${
                        goal.completed 
                          ? 'bg-green-500 border-green-500' 
                          : 'border-gray-400'
                      }`}>
                        {goal.completed && <CheckCircle className="w-4 h-4 text-white" />}
                      </div>
                      <span className={`flex-1 ${
                        goal.completed ? 'text-green-700 line-through' : 'text-gray-700'
                      }`}>
                        {goal.text}
                      </span>
                      {goal.completed && (
                        <span className="text-green-500 ml-2">✅</span>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === "achievements" && (
            <motion.div
              key="achievements"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Add Achievement Form */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Добавить достижение</h3>
                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Название достижения"
                    value={newAchievement.title}
                    onChange={(e) => setNewAchievement({ ...newAchievement, title: e.target.value })}
                    className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                  <textarea
                    placeholder="Описание"
                    value={newAchievement.description}
                    onChange={(e) => setNewAchievement({ ...newAchievement, description: e.target.value })}
                    rows="2"
                    className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                  <button
                    onClick={addAchievement}
                    className="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white py-3 rounded-xl font-semibold hover:from-orange-600 hover:to-orange-700 transition-all duration-200 transform hover:scale-105 flex items-center justify-center"
                  >
                    <Plus className="w-5 h-5 mr-2" />
                    Добавить достижение
                  </button>
                </div>
              </div>

              {/* Achievements Grid */}
              <div className="bg-white rounded-2xl shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center">
                  <Award className="w-5 h-5 text-yellow-500 mr-2" />
                  Мои достижения
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  {achievements.map((achievement) => (
                    <motion.div
                      key={achievement.id}
                      className="bg-gradient-to-br from-purple-50 to-cyan-50 p-4 rounded-xl text-center border-2 border-transparent hover:border-purple-200 transition-all duration-300"
                      whileHover={{ scale: 1.05, rotate: 2 }}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <div className={`text-4xl mb-2 ${
                        achievement.type === 'math' ? '🎉' :
                        achievement.type === 'reading' ? '📚' :
                        achievement.type === 'science' ? '🔬' :
                        achievement.type === 'art' ? '🎨' : '⚽'
                      }`}></div>
                      <h4 className="font-semibold text-gray-800 text-sm mb-1">
                        {achievement.title}
                      </h4>
                      <p className="text-xs text-gray-600 mb-2">
                        {achievement.description}
                      </p>
                      <div className="flex justify-center">
                        {Array(achievement.stars).fill(0).map((_, i) => (
                          <Star key={i} className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        ))}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Notification */}
      <AnimatePresence>
        {showNotification && (
          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            className="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg z-50 flex items-center"
          >
            <CheckCircle className="w-5 h-5 mr-2" />
            {notificationMessage}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-2xl border-t border-gray-200">
        <div className="max-w-md mx-auto px-4">
          <div className="flex justify-around">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex flex-col items-center py-3 px-4 transition-all duration-200 ${
                    isActive 
                      ? 'text-purple-600' 
                      : 'text-gray-400 hover:text-gray-600'
                  }`}
                >
                  <Icon className={`w-6 h-6 mb-1 ${isActive ? 'scale-110' : ''}`} />
                  <span className="text-xs font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #8b5cf6;
          cursor: pointer;
          box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
        
        .slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #8b5cf6;
          cursor: pointer;
          border: none;
          box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
      `}</style>
    </div>
  );
};

export default App;