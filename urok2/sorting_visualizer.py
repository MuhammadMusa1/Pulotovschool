import tkinter as tk
from tkinter import Canvas, Frame, Button, Label, Scale, StringVar, OptionMenu
import random
import time

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 ИИ Визуализатор Сортировки - Python")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Массив для сортировки
        self.array = []
        self.array_size = 100
        
        # Параметры анимации
        self.speed = 5
        self.is_sorting = False
        self.current_algorithm = "Пузырьковая"
        self.comparisons = 0
        self.swaps = 0
        
        # Цвета
        self.colors = {
            'default': '#00b4d8',
            'comparing': '#ff6b6b',
            'sorted': '#4ecdc4',
            'selected': '#ffd166',
            'pivot': '#f72585'
        }
        
        # Создаем интерфейс
        self.create_gui()
        self.generate_array()
        self.draw_array()
        
    def create_gui(self):
        self.canvas = Canvas(self.root, width=1100, height=500, bg='#16213e', 
                           highlightthickness=0, relief='raised', bd=3)
        self.canvas.pack(pady=20)
        
        control_frame = Frame(self.root, bg='#0f3460', relief='raised', bd=3)
        control_frame.pack(pady=10, fill='x', padx=20)
        
        buttons = [
            ("🎲 Новый массив", self.generate_array),
            ("▶️ Начать сортировку", self.start_sorting),
            ("⏸️ Пауза", self.toggle_pause),
            ("⏹️ Стоп", self.stop_sorting),
        ]
        
        for text, command in buttons:
            btn = Button(control_frame, text=text, command=command,
                       bg='#e94560', fg='white', font=('Arial', 10, 'bold'),
                       relief='raised', bd=2, padx=10, pady=5)
            btn.pack(side='left', padx=5, pady=5)
        
        algo_frame = Frame(control_frame, bg='#0f3460')
        algo_frame.pack(side='left', padx=20)
        
        Label(algo_frame, text="Алгоритм:", bg='#0f3460', fg='white', 
             font=('Arial', 10)).pack(side='left')
        
        algorithms = ["Пузырьковая", "Быстрая", "Слиянием", "Вставками", 
                     "Выбором"]
        self.algo_var = StringVar(value=self.current_algorithm)
        algo_menu = OptionMenu(algo_frame, self.algo_var, *algorithms)
        algo_menu.config(bg='#533483', fg='white', font=('Arial', 10))
        algo_menu.pack(side='left', padx=5)
        
        speed_frame = Frame(control_frame, bg='#0f3460')
        speed_frame.pack(side='left', padx=20)
        
        Label(speed_frame, text="Скорость:", bg='#0f3460', fg='white',
             font=('Arial', 10)).pack(side='left')
        
        self.speed_scale = Scale(speed_frame, from_=1, to=100, orient='horizontal',
                               length=100, bg='#533483', fg='white', 
                               highlightthickness=0)
        self.speed_scale.set(100 - self.speed)
        self.speed_scale.pack(side='left', padx=5)
        
        self.stats_label = Label(self.root, text="", bg='#1a1a2e', fg='white',
                               font=('Courier', 12, 'bold'))
        self.stats_label.pack(pady=10)
        
        self.update_stats()
        
    def generate_array(self):
        if not self.is_sorting:
            self.array = [random.randint(10, 490) for _ in range(self.array_size)]
            self.comparisons = 0
            self.swaps = 0
            self.draw_array()
            self.update_stats()
            
    def draw_array(self, highlights={}):
        self.canvas.delete("all")
        width = 1100 / len(self.array)
        
        for i, value in enumerate(self.array):
            x1 = i * width
            y1 = 500 - value
            x2 = (i + 1) * width
            y2 = 500
            
            color = self.colors['default']
            if i in highlights.get('comparing', []):
                color = self.colors['comparing']
            elif i in highlights.get('sorted', []):
                color = self.colors['sorted']
            elif i in highlights.get('selected', []):
                color = self.colors['selected']
            elif i in highlights.get('pivot', []):
                color = self.colors['pivot']
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
            self.canvas.create_line(x1, y1, x1, y2, fill=self.darken_color(color))
            self.canvas.create_line(x1, y2, x2, y2, fill=self.darken_color(color))
        self.draw_grid()
        
    def draw_grid(self):
        for i in range(0, 1101, 50):
            self.canvas.create_line(i, 0, i, 500, fill='#2d4059', width=1)
        for i in range(0, 501, 50):
            self.canvas.create_line(0, i, 1100, i, fill='#2d4059', width=1)
            
    def darken_color(self, color):
        if color.startswith('#'):
            r = max(0, int(color[1:3], 16) - 30)
            g = max(0, int(color[3:5], 16) - 30)
            b = max(0, int(color[5:7], 16) - 30)
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
        
    def update_stats(self):
        text = f"🔍 Сравнений: {self.comparisons} | 🔄 Обменов: {self.swaps} | 📊 Элементов: {len(self.array)} | ⚡ Алгоритм: {self.current_algorithm}"
        self.stats_label.config(text=text)
        
    def start_sorting(self):
        if not self.is_sorting:
            self.is_sorting = True
            self.current_algorithm = self.algo_var.get()
            self.speed = 100 - self.speed_scale.get()
            if self.current_algorithm == "Пузырьковая":
                self.bubble_sort()
            elif self.current_algorithm == "Быстрая":
                self.quick_sort(0, len(self.array)-1)
            elif self.current_algorithm == "Слиянием":
                self.merge_sort(0, len(self.array)-1)
            elif self.current_algorithm == "Вставками":
                self.insertion_sort()
            elif self.current_algorithm == "Выбором":
                self.selection_sort()
            self.is_sorting = False
            self.draw_array({'sorted': list(range(len(self.array)))})
        
    def toggle_pause(self):
        self.is_sorting = not self.is_sorting
        if self.is_sorting:
            self.start_sorting()
            
    def stop_sorting(self):
        self.is_sorting = False
        self.generate_array()
        
    def sleep(self):
        delay = 0.01 * (self.speed / 10)
        self.root.update()
        time.sleep(delay)
        
    # Сортировки
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n-i-1):
                self.comparisons += 1
                self.draw_array({'comparing': [j, j+1]})
                self.sleep()
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self.swaps += 1
                    self.update_stats()
            self.update_stats()
    
    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)
    
    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            self.draw_array({'pivot': [high], 'comparing': [j]})
            self.sleep()
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.swaps += 1
                self.update_stats()
        self.array[i+1], self.array[high] = self.array[high], self.array[i+1]
        self.swaps += 1
        self.update_stats()
        return i + 1
    
    def merge_sort(self, l, r):
        if l < r:
            m = (l + r) // 2
            self.merge_sort(l, m)
            self.merge_sort(m+1, r)
            self.merge(l, m, r)
    
    def merge(self, l, m, r):
        L = self.array[l:m+1]
        R = self.array[m+1:r+1]
        i = j = 0
        k = l
        while i < len(L) and j < len(R):
            self.comparisons += 1
            self.draw_array({'comparing': [k]})
            self.sleep()
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            k += 1
            self.swaps += 1
            self.update_stats()
        while i < len(L):
            self.array[k] = L[i]
            i += 1
            k += 1
            self.swaps += 1
            self.update_stats()
        while j < len(R):
            self.array[k] = R[j]
            j += 1
            k += 1
            self.swaps += 1
            self.update_stats()
    
    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            j = i-1
            while j >= 0 and self.array[j] > key:
                self.comparisons += 1
                self.array[j+1] = self.array[j]
                self.swaps += 1
                self.draw_array({'selected': [i], 'comparing': [j]})
                self.sleep()
                j -= 1
            self.array[j+1] = key
            self.swaps += 1
            self.update_stats()
    
    def selection_sort(self):
        for i in range(len(self.array)):
            min_idx = i
            for j in range(i+1, len(self.array)):
                self.comparisons += 1
                self.draw_array({'selected': [min_idx], 'comparing': [j]})
                self.sleep()
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.swaps += 1
            self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()