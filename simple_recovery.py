import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class SimpleRecoveryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Data Recovery Tool")
        self.geometry("600x400")

        self.scan_path = tk.StringVar()
        self.recover_path = tk.StringVar()
        self.found_files = []

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Folder to Scan:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.scan_path, width=50).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse", command=self.browse_scan_folder).grid(row=0, column=2)

        ttk.Label(frame, text="Recovery Destination:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.recover_path, width=50).grid(row=1, column=1, sticky=tk.W)
        ttk.Button(frame, text="Browse", command=self.browse_recover_folder).grid(row=1, column=2)

        ttk.Button(frame, text="Scan for Files", command=self.scan_files).grid(row=2, column=0, columnspan=3, pady=10)

        self.listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=70, height=15)
        self.listbox.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=3, column=3, sticky=tk.N+tk.S)
        self.listbox.config(yscrollcommand=scrollbar.set)

        ttk.Button(frame, text="Recover Selected Files", command=self.recover_files).grid(row=4, column=0, columnspan=3, pady=10)

    def browse_scan_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.scan_path.set(folder)

    def browse_recover_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.recover_path.set(folder)

    def scan_files(self):
        scan_dir = self.scan_path.get()
        if not os.path.isdir(scan_dir):
            messagebox.showerror("Error", "Please select a valid folder to scan.")
            return

        self.found_files.clear()
        self.listbox.delete(0, tk.END)

        # Scan for .deleted and .txt files
        for root, dirs, files in os.walk(scan_dir):
            for file in files:
                if file.endswith(".deleted") or file.endswith(".txt"):
                    full_path = os.path.join(root, file)
                    self.found_files.append(full_path)
                    self.listbox.insert(tk.END, full_path)

        if not self.found_files:
            messagebox.showinfo("Scan Complete", "No files found with .deleted or .txt extensions.")
        else:
            messagebox.showinfo("Scan Complete", f"Found {len(self.found_files)} files.")

    def recover_files(self):
        recover_dir = self.recover_path.get()
        if not os.path.isdir(recover_dir):
            messagebox.showerror("Error", "Please select a valid recovery destination folder.")
            return

        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No files selected to recover.")
            return

        count = 0
        for i in selected_indices:
            file_path = self.found_files[i]
            filename = os.path.basename(file_path)
            dest_path = os.path.join(recover_dir, filename)
            try:
                shutil.copy2(file_path, dest_path)
                count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to recover {filename}.\n{e}")
                return

        messagebox.showinfo("Recovery Complete", f"Successfully recovered {count} files.")

if __name__ == "__main__":
    app = SimpleRecoveryApp()
    app.mainloop()
