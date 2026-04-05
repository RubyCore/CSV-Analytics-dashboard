import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.title("Modern CSV Dashboard")
root.geometry("1200x700")
root.configure(bg="#1e1e2f")

data = None
entries = {}
columns = []

# ================= LAYOUT =================
sidebar = tk.Frame(root, bg="#111827", width=200)
sidebar.pack(side="left", fill="y")

main = tk.Frame(root, bg="#1e1e2f")
main.pack(side="right", fill="both", expand=True)

def clear_main():
    for widget in main.winfo_children():
        widget.destroy()

# ================= CREATE PAGE =================
def create_page():
    clear_main()
    global data, entries, columns

    tk.Label(main, text="Create CSV", font=("Arial", 18), bg="#1e1e2f", fg="white").pack(pady=10)

    col_entry = tk.Entry(main, width=50)
    col_entry.pack(pady=5)

    form_frame = tk.Frame(main, bg="#1e1e2f")
    form_frame.pack(pady=10)

    table = ttk.Treeview(main, show="headings")
    table.pack(fill="both", expand=True)

    def refresh():
        table.delete(*table.get_children())
        for _, row in data.iterrows():
            table.insert("", "end", values=list(row))

    def create_form():
        global data, columns, entries

        columns = [c.strip() for c in col_entry.get().split(",") if c.strip() != ""]
        if not columns:
            messagebox.showerror("Error", "Enter valid columns")
            return

        data = pd.DataFrame(columns=columns)

        for w in form_frame.winfo_children():
            w.destroy()

        entries.clear()

        for i, col in enumerate(columns):
            tk.Label(form_frame, text=col, bg="#1e1e2f", fg="white").grid(row=0, column=i)
            e = tk.Entry(form_frame)
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

    btn_frame = tk.Frame(main, bg="#1e1e2f")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Create Form", command=create_form).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Add Row", command=add_row).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete Row", command=delete_row).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Save CSV", command=save_csv).grid(row=0, column=3, padx=5)

# ================= ANALYSIS PAGE =================
def analysis_page():
    clear_main()
    global data

    tk.Label(main, text="Analyze CSV", font=("Arial", 18), bg="#1e1e2f", fg="white").pack(pady=10)

    top = tk.Frame(main, bg="#1e1e2f")
    top.pack(pady=5)

    table = ttk.Treeview(main, show="headings")
    table.pack(fill="both", expand=True)

    chart_frame = tk.Frame(main, bg="#1e1e2f")
    chart_frame.pack(fill="both", expand=True)

    column_select = ttk.Combobox(top, state="readonly", width=20)
    column_select.pack(side="left", padx=5)

    def refresh(df=None):
        table.delete(*table.get_children())
        df = df if df is not None else data
        if df is not None:
            for _, row in df.iterrows():
                table.insert("", "end", values=list(row))

    def load_csv():
        global data
        file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file:
            data = pd.read_csv(file)

            table["columns"] = list(data.columns)
            for col in data.columns:
                table.heading(col, text=col)
                table.column(col, width=120)

            column_select["values"] = list(data.columns)
            column_select.current(0)

            refresh()

    def delete_row():
        global data
        selected = table.selection()
        if selected:
            index = table.index(selected[0])
            data = data.drop(index).reset_index(drop=True)
            refresh()

    def search():
        keyword = search_entry.get().lower()
        if data is not None:
            filtered = data[data.apply(lambda r: r.astype(str).str.lower().str.contains(keyword).any(), axis=1)]
            refresh(filtered)

    def draw_chart(kind):
        if data is None or data.empty:
            messagebox.showerror("Error", "No data loaded")
            return

        col = column_select.get()
        if col == "":
            messagebox.showerror("Error", "Select column")
            return

        # CLEAR OLD CHART
        for widget in chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5,4))

        try:
            if pd.api.types.is_numeric_dtype(data[col]):
                data[col].plot(kind=kind, ax=ax)
            else:
                data[col].value_counts().plot(
                    kind=kind,
                    ax=ax,
                    autopct='%1.1f%%' if kind == "pie" else None
                )

            ax.set_title(f"{kind.upper()} Chart of {col}")

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    search_entry = tk.Entry(top)
    search_entry.pack(side="left", padx=5)

    tk.Button(top, text="Search", command=search).pack(side="left", padx=5)
    tk.Button(top, text="Load CSV", command=load_csv).pack(side="left", padx=5)
    tk.Button(top, text="Delete Row", command=delete_row).pack(side="left", padx=5)
    tk.Button(top, text="Bar Chart", command=lambda: draw_chart("bar")).pack(side="left", padx=5)
    tk.Button(top, text="Pie Chart", command=lambda: draw_chart("pie")).pack(side="left", padx=5)


tk.Label(sidebar, text="Dashboard", bg="#111827", fg="white", font=("Arial", 16)).pack(pady=20)

tk.Button(sidebar, text="Create CSV", width=20, command=create_page).pack(pady=10)
tk.Button(sidebar, text="Analyze CSV", width=20, command=analysis_page).pack(pady=10)


create_page()
root.mainloop()
