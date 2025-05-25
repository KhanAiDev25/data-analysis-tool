import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CSVDataTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter CSV Data Analysis Tool")
        self.root.geometry("800x600")

        # Button to load CSV
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        # Text widget for showing data info & summary
        self.text = tk.Text(root, height=15)
        self.text.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Button to show plot
        self.plot_button = tk.Button(root, text="Show Histogram of First Numeric Column", command=self.plot_histogram)
        self.plot_button.pack(pady=10)

        self.df = None
        self.canvas = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f"Loaded file: {file_path}\n\n")
                self.text.insert(tk.END, f"Data Shape: {self.df.shape}\n\n")
                self.text.insert(tk.END, "Data Info:\n")
                buffer = []
                self.df.info(buf=buffer)
                self.text.insert(tk.END, "\n".join(buffer))
                self.text.insert(tk.END, "\n\nStatistical Summary:\n")
                self.text.insert(tk.END, str(self.df.describe()))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file:\n{e}")

    def plot_histogram(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Load a CSV file first!")
            return

        numeric_cols = self.df.select_dtypes(include='number').columns
        if len(numeric_cols) == 0:
            messagebox.showwarning("Warning", "No numeric columns found to plot.")
            return

        col = numeric_cols[0]

        fig, ax = plt.subplots(figsize=(5,4))
        ax.hist(self.df[col].dropna(), bins=20, color='skyblue')
        ax.set_title(f"Histogram of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVDataTool(root)
    root.mainloop()
