import tkinter as tk

root = tk.Tk()
root.title("Мое первое окно")
root.geometry("400x300")

label = tk.Label(root, text="Привет, мир!")
label.pack()

button = tk.Button(root, text="Нажми меня")
button.pack()

entry = tk.Entry(root)
entry.pack()

root.mainloop()