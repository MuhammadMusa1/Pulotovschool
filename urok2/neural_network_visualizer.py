import tkinter as tk
from tkinter import Canvas, Frame, Button, Label, Scale, Text, Toplevel
import random
import math
import time

class NeuralNetworkVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Визуальный Симулятор Нейросети - Python")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Статистика
        self.epoch = 0
        self.loss = 1.0
        self.accuracy = 0.0

        # Создаем холст для визуализации
        self.canvas = Canvas(root, width=1000, height=700, bg='#16213e', 
                           highlightthickness=0, relief='raised', bd=3)
        self.canvas.pack(pady=20, padx=20)
        
        # Параметры нейросети
        self.input_size = 2
        self.hidden_size = 4
        self.output_size = 1
        self.learning_rate = 0.5
        
        # Инициализация весов (заменяем numpy arrays на списки)
        self.W1 = [[random.uniform(-0.1, 0.1) for _ in range(self.hidden_size)] 
                  for _ in range(self.input_size)]
        self.W2 = [[random.uniform(-0.1, 0.1) for _ in range(self.output_size)] 
                  for _ in range(self.hidden_size)]
        self.b1 = [0.0] * self.hidden_size
        self.b2 = [0.0] * self.output_size
        
        # Данные для обучения (XOR проблема)
        self.X = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.y = [[0], [1], [1], [0]]
        
        # Текущие активации для визуализации
        self.current_activations = {
            'input': [0, 0],
            'hidden': [0, 0, 0, 0],
            'output': [0]
        }
        
        # Создаем элементы управления
        self.create_controls()
        self.draw_network()
        
    def create_controls(self):
        # Панель управления
        control_frame = Frame(self.root, bg='#0f3460', relief='raised', bd=3)
        control_frame.pack(pady=10, fill='x', padx=20)
        
        # Кнопки управления
        buttons = [
            ("🎯 Обучить 1 эпоху", self.train_one_epoch),
            ("🚀 Обучить 10 эпох", self.train_10_epochs),
            ("⚡ Быстрое обучение", self.fast_train),
            ("🔄 Сброс весов", self.reset_weights),
            ("🧪 Тестировать", self.test_network)
        ]
        
        for text, command in buttons:
            btn = Button(control_frame, text=text, command=command,
                       bg='#e94560', fg='white', font=('Arial', 10, 'bold'),
                       relief='raised', bd=2, padx=10, pady=5)
            btn.pack(side='left', padx=5, pady=5)
        
        # Настройки обучения
        settings_frame = Frame(control_frame, bg='#0f3460')
        settings_frame.pack(side='right', padx=20)
        
        Label(settings_frame, text="Скорость обучения:", bg='#0f3460', 
             fg='white', font=('Arial', 10)).pack(side='left')
        
        self.lr_scale = Scale(settings_frame, from_=0.01, to=2.0, 
                            resolution=0.01, orient='horizontal',
                            length=100, bg='#533483', fg='white')
        self.lr_scale.set(self.learning_rate)
        self.lr_scale.pack(side='left', padx=5)
        
        # Статистика
        self.stats_label = Label(self.root, text="", bg='#1a1a2e', fg='white',
                               font=('Courier', 12, 'bold'))
        self.stats_label.pack(pady=10)
        
        self.update_stats()
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def dot_product(self, a, b):
        """Замена numpy.dot для списков"""
        result = 0
        for i in range(len(a)):
            result += a[i] * b[i]
        return result
    
    def matrix_multiply(self, A, B):
        """Умножение матриц (списков)"""
        result = []
        for i in range(len(A)):
            row = []
            for j in range(len(B[0])):
                s = 0
                for k in range(len(B)):
                    s += A[i][k] * B[k][j]
                row.append(s)
            result.append(row)
        return result
    
    def forward(self, X_row):
        """Прямое распространение для одного примера"""
        # Вход -> Скрытый слой
        self.z1 = []
        self.a1 = []
        for j in range(self.hidden_size):
            s = self.b1[j]
            for i in range(self.input_size):
                s += X_row[i] * self.W1[i][j]
            self.z1.append(s)
            self.a1.append(self.sigmoid(s))
        
        # Скрытый -> Выходной слой
        self.z2 = []
        self.a2 = []
        for j in range(self.output_size):
            s = self.b2[j]
            for i in range(self.hidden_size):
                s += self.a1[i] * self.W2[i][j]
            self.z2.append(s)
            self.a2.append(self.sigmoid(s))
        
        # Для визуализации
        self.current_activations['input'] = X_row
        self.current_activations['hidden'] = self.a1.copy()
        self.current_activations['output'] = self.a2.copy()
        self.draw_network()
        self.root.update()
        time.sleep(0.05)
        return self.a2
    
    def backward(self, X_row, y_row, output):
        """Обратное распространение ошибки"""
        # Ошибка выходного слоя
        error_output = [y_row[i] - output[i] for i in range(self.output_size)]
        delta2 = [error_output[i] * self.sigmoid_derivative(output[i]) 
                 for i in range(self.output_size)]
        
        # Ошибка скрытого слоя
        error_hidden = [0] * self.hidden_size
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                error_hidden[j] += delta2[k] * self.W2[j][k]
        
        delta1 = [error_hidden[j] * self.sigmoid_derivative(self.a1[j])
                 for j in range(self.hidden_size)]
        
        # Обновление весов и смещений
        lr = self.lr_scale.get()
        for i in range(self.hidden_size):
            for j in range(self.output_size):
                self.W2[i][j] += lr * delta2[j] * self.a1[i]
        for j in range(self.output_size):
            self.b2[j] += lr * delta2[j]
        
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.W1[i][j] += lr * delta1[j] * X_row[i]
        for j in range(self.hidden_size):
            self.b1[j] += lr * delta1[j]
    
    def train_one_epoch(self):
        total_loss = 0
        correct = 0
        for i in range(len(self.X)):
            output = self.forward(self.X[i])
            self.backward(self.X[i], self.y[i], output)
            total_loss += (self.y[i][0] - output[0]) ** 2
            pred = 1 if output[0] > 0.5 else 0
            if pred == self.y[i][0]:
                correct += 1
        self.epoch += 1
        self.loss = total_loss / len(self.X)
        self.accuracy = correct / len(self.X)
        self.update_stats()
    
    def train_10_epochs(self):
        for _ in range(10):
            self.train_one_epoch()
    
    def fast_train(self):
        for _ in range(100):
            self.train_one_epoch()
    
    def reset_weights(self):
        self.W1 = [[random.uniform(-0.1, 0.1) for _ in range(self.hidden_size)] 
                  for _ in range(self.input_size)]
        self.W2 = [[random.uniform(-0.1, 0.1) for _ in range(self.output_size)] 
                  for _ in range(self.hidden_size)]
        self.b1 = [0.0] * self.hidden_size
        self.b2 = [0.0] * self.output_size
        self.epoch = 0
        self.loss = 1.0
        self.accuracy = 0.0
        self.update_stats()
        self.draw_network()
    
    def test_network(self):
        result_window = Toplevel(self.root)
        result_window.title("Результаты тестирования")
        result_window.geometry("400x300")
        txt = Text(result_window, font=('Courier', 12), bg='#22223b', fg='white')
        txt.pack(expand=True, fill='both')
        txt.insert('end', "XOR тест:\n\n")
        for i in range(len(self.X)):
            output = self.forward(self.X[i])
            txt.insert('end', f"Вход: {self.X[i]} | Ожид.: {self.y[i][0]} | Предсказание: {output[0]:.3f}\n")
    
    def update_stats(self):
        text = f"📈 Эпоха: {self.epoch} | 📉 Потери: {self.loss:.6f} | 🎯 Точность: {self.accuracy:.2%} | 🎓 Скорость: {self.lr_scale.get():.2f}"
        self.stats_label.config(text=text)
        
    def draw_network(self):
        self.canvas.delete("all")
        # Координаты слоев
        layer_x = [150, 500, 850]
        layer_y = [200, 350, 500, 650]
        node_r = 30
        
        # Входной слой
        for i in range(self.input_size):
            x = layer_x[0]
            y = layer_y[i]
            val = self.current_activations['input'][i]
            self.canvas.create_oval(x-node_r, y-node_r, x+node_r, y+node_r, fill='#00b4d8', outline='white', width=3)
            self.canvas.create_text(x, y, text=f"{val:.2f}", font=('Arial', 14, 'bold'), fill='white')
        
        # Скрытый слой
        for i in range(self.hidden_size):
            x = layer_x[1]
            y = layer_y[i]
            val = self.current_activations['hidden'][i]
            self.canvas.create_oval(x-node_r, y-node_r, x+node_r, y+node_r, fill='#ffd166', outline='white', width=3)
            self.canvas.create_text(x, y, text=f"{val:.2f}", font=('Arial', 14, 'bold'), fill='black')
        
        # Выходной слой
        for i in range(self.output_size):
            x = layer_x[2]
            y = layer_y[1]
            val = self.current_activations['output'][i]
            self.canvas.create_oval(x-node_r, y-node_r, x+node_r, y+node_r, fill='#4ecdc4', outline='white', width=3)
            self.canvas.create_text(x, y, text=f"{val:.2f}", font=('Arial', 14, 'bold'), fill='black')
        
        # Связи: вход -> скрытый
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                x1, y1 = layer_x[0], layer_y[i]
                x2, y2 = layer_x[1], layer_y[j]
                w = self.W1[i][j]
                color = '#888'
                if w > 0:
                    color = '#43aa8b'
                elif w < 0:
                    color = '#f94144'
                self.canvas.create_line(x1+node_r, y1, x2-node_r, y2, fill=color, width=2)
        
        # Связи: скрытый -> выход
        for i in range(self.hidden_size):
            for j in range(self.output_size):
                x1, y1 = layer_x[1], layer_y[i]
                x2, y2 = layer_x[2], layer_y[1]
                w = self.W2[i][j]
                color = '#888'
                if w > 0:
                    color = '#43aa8b'
                elif w < 0:
                    color = '#f94144'
                self.canvas.create_line(x1+node_r, y1, x2-node_r, y2, fill=color, width=2)
        
        self.draw_legend()
    
    def draw_legend(self):
        self.canvas.create_rectangle(20, 620, 320, 690, fill='#22223b', outline='white')
        self.canvas.create_text(40, 635, anchor='w', text="🟦 Входной нейрон", font=('Arial', 12), fill='#00b4d8')
        self.canvas.create_text(40, 655, anchor='w', text="🟨 Скрытый нейрон", font=('Arial', 12), fill='#ffd166')
        self.canvas.create_text(40, 675, anchor='w', text="🟩 Выходной нейрон", font=('Arial', 12), fill='#4ecdc4')
        self.canvas.create_text(180, 635, anchor='w', text="🟩 Связь > 0", font=('Arial', 12), fill='#43aa8b')
        self.canvas.create_text(180, 655, anchor='w', text="🟥 Связь < 0", font=('Arial', 12), fill='#f94144')
        self.canvas.create_text(180, 675, anchor='w', text="⬜ Связь ≈ 0", font=('Arial', 12), fill='#888')

# Запуск симулятора
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = NeuralNetworkVisualizer(root)
    
    # Горячие клавиши
    def on_key_press(event):
        if event.char == 'r':
            visualizer.reset_weights()
        elif event.char == 't':
            visualizer.test_network()
        elif event.char == '1':
            visualizer.train_one_epoch()
        elif event.char == '2':
            visualizer.train_10_epochs()
        elif event.char == '3':
            visualizer.fast_train()
    
    root.bind('<KeyPress>', on_key_press)
    root.focus_set()
    
    root.mainloop()