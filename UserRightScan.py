import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

class SQLAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Rights Scan Analyser")
        self.root.geometry("500x350")
        self.root.configure(padx=30, pady=30)

        # UI Elements
        self.header = tk.Label(root, text="User Right Permissions Analyser", font=("Segoe UI", 16, "bold"))
        self.header.pack(pady=(0, 10))

        self.desc = tk.Label(root, text="Do note that this has been optimized for Large Dataset Processing!\n(Handles millions of rows)", fg="gray")
        self.desc.pack(pady=5)

        self.btn = ttk.Button(root, text="Upload Data", command=self.start_thread)
        self.btn.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Ready", font=("Segoe UI", 9))
        self.status_label.pack()

    def update_status(self, text, value):
        self.status_label.config(text=text)
        self.progress['value'] = value
        self.root.update_idletasks()

    def start_thread(self):
        # Run processing in a separate thread so the GUI doesn't freeze
        thread = threading.Thread(target=self.process_large_data)
        thread.start()

    def process_large_data(self):
        file_path = filedialog.askopenfilename(
            title="Select Large User Rights File",
            filetypes=[("Data files", "*.csv *.xlsx")]
        )
        
        if not file_path: return

        try:
            self.btn.config(state="disabled")
            self.update_status("Reading file in chunks...", 20)

            # --- OPTIMIZATION: LOAD ONLY NECESSARY COLUMNS ---
            cols_to_use = ['Account Name', 'DB Name', 'Priv. Type', 'Obj. Type', 'Object Name']
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                # Read CSV in chunks for memory efficiency
                chunks = pd.read_csv(file_path, usecols=cols_to_use, chunksize=50000)
                df = pd.concat(chunks)
            else:
                df = pd.read_excel(file_path, usecols=cols_to_use)

            self.update_status("Aggregating hierarchical data...", 50)

            # --- OPTIMIZATION: GROUPING ---
            # Using 'observed=True' and efficient string joining for large object lists
            hierarchy = df.groupby(['Account Name', 'DB Name', 'Priv. Type', 'Obj. Type'], as_index=False).agg({
                'Object Name': lambda x: ', '.join(x.astype(str))
            })

            self.update_status("Calculating pivot summaries...", 70)
            pivot_acc = df.pivot_table(index='Account Name', columns='Priv. Type', aggfunc='size', fill_value=0)
            pivot_db = df.pivot_table(index='DB Name', columns='Obj. Type', aggfunc='size', fill_value=0)

            # --- EXPORT ---
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
            
            if save_path:
                self.update_status("Writing to Excel (this may take a moment)...", 90)
                with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                    hierarchy.to_excel(writer, sheet_name='Detailed_Hierarchy', index=False)
                    pivot_acc.to_excel(writer, sheet_name='Account_Priv_Summary')
                    pivot_db.to_excel(writer, sheet_name='DB_Object_Summary')

                self.update_status("Completed Successfully!", 100)
                messagebox.showinfo("Success", "Audit report ready.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing Failed: {e}")
        finally:
            self.btn.config(state="normal")
            self.update_status("Ready", 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SQLAuditApp(root)
    root.mainloop()