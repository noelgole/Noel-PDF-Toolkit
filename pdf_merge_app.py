import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger
from PIL import Image, ImageTk
import subprocess

class MergeWindow:
    def __init__(self, count):
        self.top = tk.Toplevel()
        self.top.title("Merge PDFs")
        self.top.configure(bg="#121212")
        self.center_window()

        self.file_paths = [None] * count
        self.labels = []

        tk.Label(self.top, text="Select PDFs to Merge", font=("Helvetica", 14, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=10)

        frame = tk.Frame(self.top, bg="#121212")
        frame.pack()

        for i in range(count):
            row = tk.Frame(frame, bg="#121212")
            row.grid(row=i, column=0, pady=5, padx=5)

            label = tk.Label(row, text="[Not selected]", bg="#121212", fg="white", width=40, anchor="w")
            label.grid(row=0, column=0, padx=3)
            self.labels.append(label)

            browse_btn = tk.Button(row, text="Browse", command=lambda idx=i: self.browse_file(idx),
                                   bg="#333333", fg="white", activebackground="#444444", activeforeground="white")
            browse_btn.grid(row=0, column=1, padx=3)

            remove_btn = tk.Button(row, text="Remove", command=lambda idx=i: self.remove_file(idx),
                                   bg="#333333", fg="white", activebackground="#444444", activeforeground="white")
            remove_btn.grid(row=0, column=2, padx=3)

        merge_btn = tk.Button(self.top, text="Merge PDF", command=self.merge_pdfs,
                              bg="#5c0000", fg="white", activebackground="#880000", activeforeground="white")
        merge_btn.pack(pady=20)

        self.status = tk.Label(self.top, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack()

        # Home button with icon only
        try:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if not os.path.exists(image_path):
                raise FileNotFoundError("home.png not found at: " + image_path)

            home_icon = Image.open(image_path)
            home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.home_img = ImageTk.PhotoImage(home_icon)

            home_btn = tk.Button(self.top, image=self.home_img, command=self.go_home,
                                 bg="#FFD700", borderwidth=0, activebackground="#FFD700")
            home_btn.pack(pady=10)
        except Exception as e:
            print("Home icon error:", e)
        except Exception as e:
            print("Home icon error:", e)

        self.top.mainloop()

    def center_window(self):
        self.top.update_idletasks()
        w, h = 500, 550
        x = (self.top.winfo_screenwidth() - w) // 2
        y = (self.top.winfo_screenheight() - h) // 2
        self.top.geometry(f"{w}x{h}+{x}+{y}")

    def browse_file(self, index):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.file_paths[index] = path
            self.labels[index].config(text=os.path.basename(path))

    def remove_file(self, index):
        self.file_paths[index] = None
        self.labels[index].config(text="[Not selected]")

    def merge_pdfs(self):
        valid_files = [f for f in self.file_paths if f]
        if not valid_files:
            messagebox.showwarning("No PDFs", "Please select at least one file.")
            return

        merger = PdfMerger()
        for pdf in valid_files:
            merger.append(pdf)

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save Merged PDF")
        if not save_path:
            return

        merger.write(save_path)
        merger.close()

        size_mb = os.path.getsize(save_path) / (1024 * 1024)
        self.status.config(text=f"Saved to: {save_path} ({size_mb:.2f} MB)")
        messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}\nSize: {size_mb:.2f} MB")

    def go_home(self):
        self.top.destroy()


class MergePDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Merger")
        self.root.configure(bg="#121212")
        self.center_window(400, 200)

        tk.Label(root, text="Select number of PDFs to merge:", fg="white", bg="#121212",
                 font=("Arial", 12)).pack(pady=20)

        self.num_var = tk.StringVar()
        self.num_dropdown = ttk.Combobox(root, textvariable=self.num_var,
                                         values=[str(i) for i in range(2, 11)],
                                         state="readonly", width=5)
        self.num_dropdown.pack(pady=5)

        next_btn = tk.Button(root, text="Next", command=self.launch_merge_window,
                             bg="#333333", fg="white", activebackground="#5c0000", activeforeground="white")
        next_btn.pack(pady=20)

    def center_window(self, w, h):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def launch_merge_window(self):
        try:
            count = int(self.num_var.get())
            self.root.withdraw()
            MergeWindow(count)
        except ValueError:
            messagebox.showerror("Invalid Selection", "Please select a valid number.")


if __name__ == "__main__":
    main_root = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
        main_root.iconbitmap(icon_path)
    except Exception as e:
        print("App icon error:", e)
    app = MergePDFApp(main_root)
    main_root.mainloop()
