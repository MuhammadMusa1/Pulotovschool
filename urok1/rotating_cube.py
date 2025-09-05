import math
import time
import tkinter as tk
from tkinter import Canvas

class RotatingCube3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Вращающийся Куб - Python")
        self.root.geometry("800x600")
        
        # Создаем холст
        self.canvas = Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        
        # Вершины куба в 3D пространстве
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        
        # Грани куба (индексы вершин)
        self.faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]
        ]
        
        # Цвета для граней
        self.colors = ["#ff0000", "#00ff00", "#0000ff", 
                      "#ffff00", "#ff00ff", "#00ffff"]
        
        # Параметры анимации
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scale = 100
        self.center_x = 400
        self.center_y = 300
        
        # Создаем элементы управления
        self.create_controls()
        
        # Запускаем анимацию
        self.animate()
    
    def create_controls(self):
        # Фрейм для кнопок
        control_frame = tk.Frame(self.root, bg="gray")
        control_frame.place(x=10, y=10)
        
        # Кнопки управления
        tk.Button(control_frame, text="▮▮ Пауза", command=self.toggle_pause, 
                 bg="lightblue", font=("Arial", 10)).pack(pady=2)
        tk.Button(control_frame, text="🌀 Случайные цвета", command=self.random_colors,
                 bg="lightgreen", font=("Arial", 10)).pack(pady=2)
        tk.Button(control_frame, text="🔄 Сброс", command=self.reset,
                 bg="lightcoral", font=("Arial", 10)).pack(pady=2)
        
        # Метки информации
        self.info_label = tk.Label(self.root, text="", bg="black", fg="white", 
                                  font=("Courier", 10))
        self.info_label.place(x=10, y=550)
        
        self.paused = False
    
    def rotate_point(self, point, angle_x, angle_y, angle_z):
        x, y, z = point
        
        # Вращение вокруг X
        y_rot = y * math.cos(angle_x) - z * math.sin(angle_x)
        z_rot = y * math.sin(angle_x) + z * math.cos(angle_x)
        y, z = y_rot, z_rot
        
        # Вращение вокруг Y
        x_rot = x * math.cos(angle_y) + z * math.sin(angle_y)
        z_rot = -x * math.sin(angle_y) + z * math.cos(angle_y)
        x, z = x_rot, z_rot
        
        # Вращение вокруг Z
        x_rot = x * math.cos(angle_z) - y * math.sin(angle_z)
        y_rot = x * math.sin(angle_z) + y * math.cos(angle_z)
        x, y = x_rot, y_rot
        
        return [x, y, z]
    
    def project_point(self, point):
        x, y, z = point
        # Простая перспективная проекция
        factor = 400 / (400 + z * 3)
        x_proj = x * factor * self.scale + self.center_x
        y_proj = y * factor * self.scale + self.center_y
        return x_proj, y_proj
    
    def draw_cube(self):
        self.canvas.delete("all")
        
        # Рисуем координатные оси
        self.draw_axes()
        
        # Преобразуем и проецируем все вершины
        projected_vertices = []
        for vertex in self.vertices:
            rotated = self.rotate_point(vertex, self.angle_x, self.angle_y, self.angle_z)
            projected_vertices.append(self.project_point(rotated))
        
        # Рисуем грани с учетом глубины
        faces_with_depth = []
        for i, face in enumerate(self.faces):
            # Вычисляем среднюю глубину для сортировки
            z_sum = sum(self.vertices[vertex][2] for vertex in face)
            faces_with_depth.append((z_sum, i, face))
        
        # Сортируем грани по глубине (задние сначала)
        faces_with_depth.sort()
        
        for depth, face_idx, face in faces_with_depth:
            points = [projected_vertices[vertex] for vertex in face]
            
            # Рисуем грань
            self.canvas.create_polygon(
                points, fill=self.colors[face_idx], outline="white", width=2
            )
            
            # Рисуем номера вершин
            for vertex in face:
                x, y = projected_vertices[vertex]
                self.canvas.create_text(x, y, text=str(vertex), fill="white", font=("Arial", 8))
        
        # Обновляем информацию
        info_text = f"Углы: X={math.degrees(self.angle_x):.1f}° Y={math.degrees(self.angle_y):.1f}° Z={math.degrees(self.angle_z):.1f}°"
        self.info_label.config(text=info_text)
    
    def draw_axes(self):
        # Ось X (красная)
        self.canvas.create_line(50, 550, 150, 550, arrow=tk.LAST, fill="red", width=2)
        self.canvas.create_text(160, 550, text="X", fill="red", font=("Arial", 12))
        
        # Ось Y (зеленая)
        self.canvas.create_line(50, 550, 50, 450, arrow=tk.LAST, fill="green", width=2)
        self.canvas.create_text(50, 440, text="Y", fill="green", font=("Arial", 12))
        
        # Ось Z (синяя)
        self.canvas.create_line(50, 550, 100, 500, arrow=tk.LAST, fill="blue", width=2)
        self.canvas.create_text(110, 490, text="Z", fill="blue", font=("Arial", 12))
    
    def animate(self):
        if not self.paused:
            self.angle_x += 0.01
            self.angle_y += 0.015
            self.angle_z += 0.005
            
            self.draw_cube()
        
        self.root.after(16, self.animate)  # ~60 FPS
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def random_colors(self):
        import random
        self.colors = [
            f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
            for _ in range(6)
        ]
    
    def reset(self):
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.colors = ["#ff0000", "#00ff00", "#0000ff", 
                      "#ffff00", "#ff00ff", "#00ffff"]
        self.paused = False

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingCube3D(root)
    
    # Добавляем горячие клавиши
    def on_key_press(event):
        if event.keysym == 'space':
            app.toggle_pause()
        elif event.keysym == 'r':
            app.random_colors()
        elif event.keysym == 'c':
            app.reset()
    
    root.bind('<KeyPress>', on_key_press)
    root.focus_set()
    
    root.mainloop()