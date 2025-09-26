import tkinter as tk

def on_button_click():
    print("Кнопка нажата!")

root = tk.Tk()
root.title("Мое первое окно")
root.geometry("400x300")

label = tk.Label(root, text="Привет, мир!")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Нажми меня", command=on_button_click)
button.pack()
root.mainloop()