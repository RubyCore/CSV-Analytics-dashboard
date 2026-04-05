import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Main window
root = tk.Tk()
root.title("Bike Sales Dashboard")
root.geometry("800x500")
root.configure(bg="#1e1e2f")

data = None

# Sidebar Frame
sidebar = tk.Frame(root, bg="#2c2c3e", width=200)
sidebar.pack(side="left", fill="y")

# Main Frame
main = tk.Frame(root, bg="#1e1e2f")
main.pack(side="right", expand=True, fill="both")

# Title
title = tk.Label(main, text="Bike Sales Dashboard", fg="white", bg="#1e1e2f", font=("Arial", 20, "bold"))
title.pack(pady=20)

# Functions
def load_file():
    global data
    file = filedialog.askopenfilename()
    if file:
        data = pd.read_csv(file)
        messagebox.showinfo("Success", "File Loaded")

def revenue():
    if data is not None:
        data["Total"] = data["Price"] * data["Quantity"]
        total = np.sum(data["Total"])
        messagebox.showinfo("Revenue", f"Total Revenue: {total}")
    else:
        messagebox.showwarning("Error", "Load file first")

def bike_bar():
    if data is not None:
        bike = data.groupby("Bike")["Quantity"].sum()
        bike.plot(kind="bar")
        plt.title("Bike Sales")
        plt.show()
    else:
        messagebox.showwarning("Error", "Load file first")

def bike_pie():
    if data is not None:
        bike = data.groupby("Bike")["Quantity"].sum()
        bike.plot(kind="pie", autopct='%1.1f%%')
        plt.title("Bike Distribution")
        plt.ylabel("")
        plt.show()
    else:
        messagebox.showwarning("Error", "Load file first")

# Sidebar Buttons
def create_btn(text, cmd):
    return tk.Button(
        sidebar,
        text=text,
        command=cmd,
        fg="white",
        bg="#3a3a5c",
        activebackground="#50507a",
        width=20,
        height=2,
        bd=0
    )

create_btn("Load CSV", load_file).pack(pady=10)
create_btn("Total Revenue", revenue).pack(pady=10)
create_btn("Bar Chart", bike_bar).pack(pady=10)
create_btn("Pie Chart", bike_pie).pack(pady=10)

root.mainloop()
