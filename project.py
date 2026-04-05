import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ================= MAIN WINDOW =================
root = tk.Tk()
root.title("Glass CSV Dashboard")
root.geometry("1300x850")
root.configure(bg="#0b1120")

data = None
entries = {}
columns = []

# ================= GLASS STYLES =================
def glass_frame(parent, bg="#1e293b"):
    return tk.Frame(parent, bg=bg, highlightthickness=1, highlightbackground="#334155")

def glass_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg="#38bdf8",
        fg="black",
        activebackground="#0ea5e9",
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=12,
        pady=6,
        cursor="hand2"
    )

# ================= LAYOUT =================
sidebar = glass_frame(root, "#020617")
sidebar.pack(side="left", fill="y", ipadx=10)

main = tk.Frame(root, bg="#0b1120")
main.pack(side="right", fill="both", expand=True)

def clear_main():
    for widget in main.winfo_children():
        widget.destroy()

# ================= SIDEBAR =================
tk.Label(sidebar, text="📊 Dashboard", bg="#020617", fg="#38bdf8",
         font=("Segoe UI", 18, "bold")).pack(pady=30)

# ================= CREATE PAGE =================
def create_page():
    clear_main()
    global data, entries, columns

    tk.Label(main, text="Create CSV", font=("Segoe UI", 22, "bold"),
             bg="#0b1120", fg="#7dd3fc").pack(pady=15)

    panel = glass_frame(main)
    panel.pack(padx=20, pady=10, fill="x")

    col_entry = tk.Entry(panel, width=50, bg="#0f172a", fg="white", bd=0)
    col_entry.pack(pady=10)

    form_frame = tk.Frame(panel, bg="#1e293b")
    form_frame.pack(pady=10)

    table = ttk.Treeview(main, show="headings")
    table.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh():
        table.delete(*table.get_children())
        for _, row in data.iterrows():
            table.insert("", "end", values=list(row))

    def create_form():
        global data, columns, entries
        columns = [c.strip() for c in col_entry.get().split(",") if c.strip()]
        if not columns:
            messagebox.showerror("Error", "Enter valid columns")
            return

        data = pd.DataFrame(columns=columns)

        for w in form_frame.winfo_children():
            w.destroy()

        entries.clear()

        for i, col in enumerate(columns):
            tk.Label(form_frame, text=col, bg="#1e293b", fg="white").grid(row=0, column=i)
            e = tk.Entry(form_frame, bg="#0f172a", fg="white", bd=0)
            e.grid(row=1, column=i, padx=5)
            entries[col] = e

        table["columns"] = columns
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120)

    def add_row():
        global data
        row = {}
        for col, e in entries.items():
            val = e.get()
            if val == "":
                messagebox.showerror("Error", f"{col} empty")
                return
            row[col] = val

        data.loc[len(data)] = row
        refresh()

        for e in entries.values():
            e.delete(0, tk.END)

    def delete_row():
        global data
        selected = table.selection()
        if selected:
            index = table.index(selected[0])
            data = data.drop(index).reset_index(drop=True)
            refresh()

    def save_csv():
        if data is None or data.empty:
            messagebox.showwarning("Warning", "No data")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if file:
            data.to_csv(file, index=False)
            messagebox.showinfo("Saved", "CSV Created")

    btn_frame = tk.Frame(panel, bg="#1e293b")
    btn_frame.pack(pady=10)

    glass_button(btn_frame, "Create Form", create_form).grid(row=0, column=0, padx=5)
    glass_button(btn_frame, "Add Row", add_row).grid(row=0, column=1, padx=5)
    glass_button(btn_frame, "Delete Row", delete_row).grid(row=0, column=2, padx=5)
    glass_button(btn_frame, "Save CSV", save_csv).grid(row=0, column=3, padx=5)

# ================= ANALYSIS PAGE =================
def analysis_page():
    clear_main()
    global data

    tk.Label(main, text="Analyze CSV", font=("Segoe UI", 22, "bold"),
             bg="#0b1120", fg="#7dd3fc").pack(pady=15)

    top = glass_frame(main)
    top.pack(padx=10, pady=10, fill="x")

    tk.Label(top, text="📌 Select Columns", bg="#1e293b", fg="#22c55e",
             font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

    column_listbox = tk.Listbox(top, selectmode="multiple",
                               bg="#0f172a", fg="white",
                               selectbackground="#38bdf8", bd=0, height=5)
    column_listbox.pack(side="left", padx=10)

    table = ttk.Treeview(main, show="headings")
    table.pack(fill="both", expand=True, padx=10, pady=10)

    chart_frame = glass_frame(main)
    chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    entry_frame = tk.Frame(main, bg="#1e293b")
    entry_frame.pack(pady=10)

    entry_widgets = {}

    def refresh():
        table.delete(*table.get_children())
        if data is not None:
            table["columns"] = list(data.columns)
            for col in data.columns:
                table.heading(col, text=col)
                table.column(col, width=120)
            for _, row in data.iterrows():
                table.insert("", "end", values=list(row))

    def load_csv():
        global data
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            data = pd.read_csv(file)

            column_listbox.delete(0, tk.END)
            for col in data.columns:
                column_listbox.insert(tk.END, col)

            for w in entry_frame.winfo_children():
                w.destroy()

            entry_widgets.clear()

            for i, col in enumerate(data.columns):
                tk.Label(entry_frame, text=col, bg="#1e293b", fg="white").grid(row=0, column=i)
                e = tk.Entry(entry_frame, bg="#0f172a", fg="white", bd=0)
                e.grid(row=1, column=i, padx=5)
                entry_widgets[col] = e

            refresh()

    def get_filtered_data():
        df = data.copy()
        selected = [column_listbox.get(i) for i in column_listbox.curselection()]
        if selected:
            df = df[selected]
        return df

    def add_row_loaded():
        global data
        new_row = {}
        for col, e in entry_widgets.items():
            val = e.get()
            if val == "":
                messagebox.showerror("Error", f"{col} empty")
                return
            new_row[col] = val
        data.loc[len(data)] = new_row
        refresh()

    def delete_row():
        global data
        selected = table.selection()
        if selected:
            index = table.index(selected[0])
            data = data.drop(index).reset_index(drop=True)
            refresh()

    def draw_chart(kind):
        if data is None:
            return
        df = get_filtered_data()

        for w in chart_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(6,4))

        if kind == "hist":
            df.plot(kind="hist", ax=ax)
        elif kind == "line":
            df.plot(kind="line", ax=ax)
        elif kind == "bar":
            df.plot(kind="bar", ax=ax)
        elif kind == "pie" and len(df.columns) == 1:
            df.iloc[:,0].value_counts().plot(kind="pie", ax=ax, autopct='%1.1f%%')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    btn_frame = tk.Frame(top, bg="#1e293b")
    btn_frame.pack(side="right")

    glass_button(btn_frame, "Load", load_csv).pack(side="left", padx=5)
    glass_button(btn_frame, "Add", add_row_loaded).pack(side="left", padx=5)
    glass_button(btn_frame, "Delete", delete_row).pack(side="left", padx=5)

    glass_button(btn_frame, "Bar", lambda: draw_chart("bar")).pack(side="left", padx=5)
    glass_button(btn_frame, "Pie", lambda: draw_chart("pie")).pack(side="left", padx=5)
    glass_button(btn_frame, "Hist", lambda: draw_chart("hist")).pack(side="left", padx=5)
    glass_button(btn_frame, "Line", lambda: draw_chart("line")).pack(side="left", padx=5)

# ================= TABLE STYLE =================
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#0f172a",
                foreground="white",
                fieldbackground="#0f172a",
                rowheight=28)

style.configure("Treeview.Heading",
                background="#1e293b",
                foreground="#38bdf8",
                font=("Segoe UI", 10, "bold"))

# ================= NAVIGATION =================
glass_button(sidebar, "Create CSV", create_page).pack(pady=10)
glass_button(sidebar, "Analyze CSV", analysis_page).pack(pady=10)

# ================= START =================
create_page()
root.mainloop()
