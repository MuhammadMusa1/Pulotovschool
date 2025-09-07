import math
import random
import time
import tkinter as tk
from tkinter import Canvas, Scale, Label, Frame

class SolarSystemAI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 ИИ Симулятор Солнечной Системы - Python")
        self.root.geometry("1200x800")
        self.root.configure(bg='black')

        # Создаем холст
        self.canvas = Canvas(root, width=1000, height=700, bg='#000010')
        self.canvas.pack(pady=10)

        # Звездное небо
        self.stars = [(random.randint(0, 1000), random.randint(0, 700), 
                      random.random() * 2) for _ in range(200)]

        # Планеты солнечной системы (масса, радиус, цвет, позиция, скорость)
        self.planets = [
            # Солнце
            {'mass': 50000, 'radius': 30, 'color': '#FFD700', 'name': 'Солнце',
             'x': 500, 'y': 350, 'vx': 0, 'vy': 0, 'trail': []},
            
            # Меркурий
            {'mass': 100, 'radius': 8, 'color': '#A9A9A9', 'name': 'Меркурий',
             'x': 420, 'y': 350, 'vx': 0, 'vy': -4.5, 'trail': []},
            
            # Венера
            {'mass': 200, 'radius': 12, 'color': '#FFA500', 'name': 'Венера',
             'x': 380, 'y': 350, 'vx': 0, 'vy': -3.8, 'trail': []},
            
            # Земля
            {'mass': 250, 'radius': 13, 'color': '#1E90FF', 'name': 'Земля',
             'x': 320, 'y': 350, 'vx': 0, 'vy': -3.2, 'trail': []},
            
            # Марс
            {'mass': 150, 'radius': 10, 'color': '#FF4500', 'name': 'Марс',
             'x': 270, 'y': 350, 'vx': 0, 'vy': -2.8, 'trail': []},
            
            # Юпитер
            {'mass': 1000, 'radius': 25, 'color': '#FF8C00', 'name': 'Юпитер',
             'x': 180, 'y': 350, 'vx': 0, 'vy': -2.1, 'trail': []},
            
            # Сатурн
            {'mass': 800, 'radius': 22, 'color': '#FFD700', 'name': 'Сатурн',
             'x': 100, 'y': 350, 'vx': 0, 'vy': -1.8, 'trail': []}
        ]

        # Частицы для эффектов
        self.particles = []
        self.gravity_strength = 0.1
        self.time_scale = 1.0
        self.paused = False

        # Создаем элементы управления
        self.create_controls()
        self.draw_stars()
        self.animate()

    def create_controls(self):
        control_frame = Frame(self.root, bg='#2c3e50', relief='raised', bd=2)
        control_frame.pack(pady=10, fill='x', padx=20)

        # Кнопки управления
        buttons = [
            ("🌀 Запустить спутник", self.launch_satellite),
            ("💥 Взрыв астероидов", self.asteroid_explosion),
            ("🌠 Сверхновая", self.supernova),
            ("⏸️ Пауза", self.toggle_pause),
            ("🔄 Перезапуск", self.restart)
        ]

        for text, command in buttons:
            btn = tk.Button(control_frame, text=text, command=command,
                          bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                          relief='raised', bd=2)
            btn.pack(side='left', padx=5, pady=5)

        # Слайдеры
        slider_frame = Frame(self.root, bg='#2c3e50')
        slider_frame.pack(pady=5)

        Label(slider_frame, text="Сила гравитации:", fg='white', bg='#2c3e50').pack(side='left')
        self.gravity_scale = Scale(slider_frame, from_=0.01, to=0.5, resolution=0.01,
                                 orient='horizontal', length=200, bg='#34495e', fg='white')
        self.gravity_scale.set(self.gravity_strength)
        self.gravity_scale.pack(side='left', padx=10)

        Label(slider_frame, text="Скорость времени:", fg='white', bg='#2c3e50').pack(side='left')
        self.time_scale = Scale(slider_frame, from_=0.1, to=3.0, resolution=0.1,
                              orient='horizontal', length=200, bg='#34495e', fg='white')
        self.time_scale.set(self.time_scale)
        self.time_scale.pack(side='left', padx=10)

    def draw_stars(self):
        for x, y, size in self.stars:
            self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                  fill='white', outline='')

    def calculate_physics(self):
        G = self.gravity_strength
        
        for i, planet1 in enumerate(self.planets):
            for j, planet2 in enumerate(self.planets):
                if i != j:  # Не считаем гравитацию к себе
                    dx = planet2['x'] - planet1['x']
                    dy = planet2['y'] - planet1['y']
                    distance = max(math.sqrt(dx*dx + dy*dy), 20)  # Минимальная дистанция
                    
                    # Закон всемирного тяготения
                    force = G * planet1['mass'] * planet2['mass'] / (distance * distance)
                    angle = math.atan2(dy, dx)
                    
                    # Применяем силу
                    fx = force * math.cos(angle)
                    fy = force * math.sin(angle)
                    
                    planet1['vx'] += fx / planet1['mass'] * self.time_scale
                    planet1['vy'] += fy / planet1['mass'] * self.time_scale

    def update_positions(self):
        for planet in self.planets:
            planet['x'] += planet['vx'] * self.time_scale
            planet['y'] += planet['vy'] * self.time_scale
            
            # Добавляем точку в след (только для планет)
            if planet['name'] != 'Солнце':
                planet['trail'].append((planet['x'], planet['y']))
                if len(planet['trail']) > 50:
                    planet['trail'].pop(0)

    def draw_planets(self):
        # Рисуем следы орбит
        for planet in self.planets:
            if planet['trail']:
                for i in range(len(planet['trail'])-1):
                    x1, y1 = planet['trail'][i]
                    x2, y2 = planet['trail'][i+1]
                    alpha = i / len(planet['trail'])
                    color = self.adjust_alpha(planet['color'], alpha)
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

        # Рисуем планеты
        for planet in self.planets:
            x, y = planet['x'], planet['y']
            radius = planet['radius']
            
            # Основной круг
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                  fill=planet['color'], outline='white', width=2)
            
            # Подпись
            self.canvas.create_text(x, y-radius-15, text=planet['name'],
                                  fill='white', font=('Arial', 10, 'bold'))

    def update_particles(self):
        new_particles = []
        for particle in self.particles:
            x, y, vx, vy, life, color, size = particle
            
            # Применяем гравитацию к Солнцу
            dx = 500 - x
            dy = 350 - y
            dist = max(math.sqrt(dx*dx + dy*dy), 10)
            force = 0.1 / (dist * dist)
            angle = math.atan2(dy, dx)
            
            vx += force * math.cos(angle) * self.time_scale
            vy += force * math.sin(angle) * self.time_scale
            
            x += vx * self.time_scale
            y += vy * self.time_scale
            life -= 1
            
            if life > 0 and 0 <= x <= 1000 and 0 <= y <= 700:
                new_particles.append((x, y, vx, vy, life, color, size))
                
                # Рисуем частицу
                alpha = life / 100
                self.canvas.create_oval(x-size, y-size, x+size, y+size,
                                      fill=self.adjust_alpha(color, alpha), outline='')
        
        self.particles = new_particles

    def adjust_alpha(self, color, alpha):
        """Изменяет прозрачность цвета"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            return f'#{int(r*alpha):02x}{int(g*alpha):02x}{int(b*alpha):02x}'
        return color

    def launch_satellite(self):
        # Запускаем спутник с Земли
        earth = next(p for p in self.planets if p['name'] == 'Земля')
        for _ in range(20):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 4)
            self.particles.append((
                earth['x'], earth['y'],
                math.cos(angle) * speed, math.sin(angle) * speed,
                100, '#00FF00', 3
            ))

    def asteroid_explosion(self):
        # Взрыв астероидов
        for _ in range(100):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 8)
            self.particles.append((
                500, 350,  # От центра
                math.cos(angle) * speed, math.sin(angle) * speed,
                150, '#FF6B6B', random.randint(2, 5)
            ))

    def supernova(self):
        # Взрыв сверхновой (Солнце)
        sun = next(p for p in self.planets if p['name'] == 'Солнце')
        for _ in range(300):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(5, 15)
            self.particles.append((
                sun['x'], sun['y'],
                math.cos(angle) * speed, math.sin(angle) * speed,
                200, random.choice(['#FFD700', '#FF8C00', '#FF4500']),
                random.randint(3, 8)
            ))

    def toggle_pause(self):
        self.paused = not self.paused

    def restart(self):
        self.__init__(self.root)

    def animate(self):
        if not self.paused:
            self.canvas.delete("all")
            self.draw_stars()
            
            # Обновляем параметры из слайдеров
            self.gravity_strength = self.gravity_scale.get()
            self.time_scale = self.time_scale.get()
            
            # Физика
            self.calculate_physics()
            self.update_positions()
            self.update_particles()
            
            # Отрисовка
            self.draw_planets()
            
            # Информация
            info = f"Планет: {len(self.planets)} | Частиц: {len(self.particles)} | Гравитация: {self.gravity_strength:.2f}"
            self.canvas.create_text(500, 20, text=info, fill='white', font=('Arial', 12, 'bold'))

        self.root.after(16, self.animate)  # ~60 FPS

# Запуск симулятора
if __name__ == "__main__":
    root = tk.Tk()
    simulator = SolarSystemAI(root)
    
    # Горячие клавиши
    def on_key_press(event):
        if event.keysym == 'space':
            simulator.toggle_pause()
        elif event.keysym == 's':
            simulator.launch_satellite()
        elif event.keysym == 'a':
            simulator.asteroid_explosion()
        elif event.keysym == 'n':
            simulator.supernova()
        elif event.keysym == 'r':
            simulator.restart()
    
    root.bind('<KeyPress>', on_key_press)
    root.focus_set()
    
    root.mainloop()