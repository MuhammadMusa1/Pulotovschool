import tkinter as tk

def add():
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    result = num1 + num2
    result_label.config(text="Результат: " + str(result))

root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x200")

entry1 = tk.Entry(root)
entry1.pack()

entry2 = tk.Entry(root)
entry2.pack()

add_button = tk.Button(root, text="Сложить", command=add)
add_button.pack()

result_label = tk.Label(root, text="Результат:")
result_label.pack()

root.mainloop()