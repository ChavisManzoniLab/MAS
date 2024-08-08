import tkinter as tk
from tkinter import filedialog, StringVar

global path 

path = 'No path selected'

def browseFiles():
    path = filedialog.askdirectory(title = "Select a folder")
    return path
window = tk.Tk()

button = tk.Button(
    text= "Click here to select " + "\n" + "the folder of the videos",
    width=20,
    height=3,
    bg="grey",
    fg="black",
    command = browseFiles
)

button.pack()

v = StringVar()
tk.Label(text=path).pack()
v.set(value = path)


button = tk.Button(
    text="Click me!",
    width=20,
    height=3,
    bg="orange",
    fg="purple",
    command = browseFiles
)

button.pack()

window.mainloop()
print(path)