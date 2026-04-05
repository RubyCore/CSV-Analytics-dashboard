import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

root = tk.Tk()
root.title("CSV Data Dashboard")
root.geometry("900x550")
root.configure(bg="#1e1e2f")

data = None


columns = ("Order_ID", "Customer", "City", "Bike", "Price", "Quantity")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

table.pack(pady=10, fill="both", expand=True)


def load_csv():
    global data
    file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file:
        data = pd.read_csv(file)
        show_data()
        messagebox.showinfo("Success", "CSV Loaded")

def show_data():
    table.delete(*table.get_children())
    if data is not None:
        for _, row in data.iterrows():
            table.insert("", "end", values=list(row))

def add_data():
    global data
    if data is None:
        messagebox.showwarning("Error", "Load CSV first")
        return

    try:
        new_row = {
            "Order_ID": len(data) + 1,
            "Customer": e_customer.get(),
            "City": e_city.get(),
            "Bike": e_bike.get(),
            "Price": int(e_price.get()),
            "Quantity": int(e_qty.get())
        }

        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        show_data()
        clear_fields()
        messagebox.showinfo("Success", "Data Added")

    except:
        messagebox.showerror("Error", "Invalid Input")

def save_csv():
    if data is not None:
        data.to_csv("updated_data.csv", index=False)
        messagebox.showinfo("Saved", "CSV Saved")

def bar_chart():
    if data is not None:
        bike = data.groupby("Bike")["Quantity"].sum()
        bike.plot(kind="bar")
        plt.title("Bike Sales")
        plt.show()

def pie_chart():
    if data is not None:
        bike = data.groupby("Bike")["Quantity"].sum()
        bike.plot(kind="pie", autopct='%1.1f%%')
        plt.title("Bike Distribution")
        plt.ylabel("")
        plt.show()

def clear_fields():
    e_customer.delete(0, tk.END)
    e_city.delete(0, tk.END)
    e_bike.delete(0, tk.END)
    e_price.delete(0, tk.END)
    e_qty.delete(0, tk.END)

frame = tk.Frame(root, bg="#222")
frame.pack(pady=10)

def create_entry(label):
    tk.Label(frame, text=label, fg="white", bg="#222").pack()
    entry = tk.Entry(frame)
    entry.pack()
    return entry

e_customer = create_entry("Customer")
e_city = create_entry("City")
e_bike = create_entry("Bike")
e_price = create_entry("Price")
e_qty = create_entry("Quantity")

btn_frame = tk.Frame(root, bg="#222")
btn_frame.pack(pady=10)

def btn(text, cmd):
    return tk.Button(btn_frame, text=text, command=cmd, width=15)

btn("Load CSV", load_csv).grid(row=0, column=0, padx=5)
btn("Add Data", add_data).grid(row=0, column=1, padx=5)
btn("Save CSV", save_csv).grid(row=0, column=2, padx=5)
btn("Bar Chart", bar_chart).grid(row=0, column=3, padx=5)
btn("Pie Chart", pie_chart).grid(row=0, column=4, padx=5)

root.mainloop()
