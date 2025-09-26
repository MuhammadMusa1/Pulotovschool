import tkinter as tk

root = tk.Tk()
root.title("Мое приложение")
root.geometry("400x300")

label = tk.Label(root, text="Введите текст:")
label.pack()

entry = tk.Entry(root)
entry.pack()

def on_button_click():
    text = entry.get()
    print("Вы ввели:", text)
    
def on_button_click():
    text = entry.get()
    new_label = tk.Label(root, text="Вы ввели: " + text)
    new_label.pack()
    
button = tk.Button(root, text="Отправить", command=on_button_click)
button.pack()

root.mainloop()