import math
import random
import tkinter as tk
from tkinter import Canvas

class AudioWaveVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор Музыкальных Волн - Python")
        self.root.geometry("1000x600")
        
        self.canvas = Canvas(root, width=1000, height=600, bg="black")
        self.canvas.pack()
        
        # Параметры волн
        self.waves = []
        self.colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#eb4d4b"]
        
        self.create_waves()
        self.create_controls()
        self.animate()
    
    def create_waves(self):
        # Создаем несколько волн с разными параметрами
        for i in range(5):
            self.waves.append({
                'amplitude': random.randint(20, 100),
                'frequency': random.uniform(0.01, 0.05),
                'phase': random.uniform(0, math.pi * 2),
                'color': self.colors[i],
                'points': [],
                'speed': random.uniform(0.5, 2.0)
            })
    
    def create_controls(self):
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.place(x=10, y=10)
        
        tk.Button(control_frame, text="🎵 Новые волны", command=self.new_waves,
                 bg="#3498db", fg="white", font=("Arial", 10)).pack(pady=2)
        
        tk.Button(control_frame, text="💥 Эксплозия", command=self.explosion,
                 bg="#e74c3c", fg="white", font=("Arial", 10)).pack(pady=2)
        
        self.info_label = tk.Label(self.root, text="", bg="black", fg="white", 
                                  font=("Courier", 10))
        self.info_label.place(x=10, y=560)
    
    def draw_waves(self):
        self.canvas.delete("all")
        
        time_val = time.time()
        
        # Рисуем сетку
        self.draw_grid()
        
        # Рисуем каждую волну
        for i, wave in enumerate(self.waves):
            points = []
            
            for x in range(0, 1000, 2):
                y = 300 + wave['amplitude'] * math.sin(
                    wave['frequency'] * x + wave['phase'] + time_val * wave['speed']
                )
                points.extend([x, y])
            
            # Рисуем плавную кривую
            self.canvas.create_line(points, fill=wave['color'], width=3, smooth=True)
            
            # Рисуем кружки на волне
            for x in range(0, 1000, 50):
                y = 300 + wave['amplitude'] * math.sin(
                    wave['frequency'] * x + wave['phase'] + time_val * wave['speed']
                )
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=wave['color'], outline="")
        
        # Обновляем информацию
        info_text = f"Волн: {len(self.waves)} | Время: {time_val:.1f}"
        self.info_label.config(text=info_text)
    
    def draw_grid(self):
        # Горизонтальные линии
        for y in range(100, 600, 100):
            self.canvas.create_line(0, y, 1000, y, fill="#34495e", width=1)
        
        # Вертикальные линии
        for x in range(0, 1000, 50):
            self.canvas.create_line(x, 0, x, 600, fill="#34495e", width=1)
        
        # Центральная линия
        self.canvas.create_line(0, 300, 1000, 300, fill="#7f8c8d", width=2)
    
    def animate(self):
        self.draw_waves()
        self.root.after(30, self.animate)  # ~33 FPS
    
    def new_waves(self):
        self.waves = []
        self.create_waves()
    
    def explosion(self):
        # Создаем взрыв частиц
        for _ in range(100):
            x = random.randint(0, 1000)
            y = random.randint(0, 600)
            size = random.randint(2, 8)
            color = random.choice(self.colors)
            
            self.canvas.create_oval(x-size, y-size, x+size, y+size, 
                                   fill=color, outline="")
        
        self.root.after(500, self.new_waves)  # Через 0.5 секунды новые волны

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioWaveVisualizer(root)
    root.mainloop()