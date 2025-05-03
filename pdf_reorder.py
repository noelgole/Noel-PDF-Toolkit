import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import os
import subprocess
from PIL import Image, ImageTk

class PDFReorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Reorder Tool")
        self.set_geometry(500, 550)
        self.root.configure(bg="#121212")

        # Set custom .ico icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.file_path = None
        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Reorder PDF Pages", font=("Helvetica", 18, "bold"), fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.load_pdf).pack(pady=10)

        self.info_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Arial", 10))
        self.info_label.pack()

        ttk.Button(root, text="Enter Page Order & Save", command=self.reorder_pdf).pack(pady=10)

        # Home and Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if not os.path.exists(home_icon_path):
                raise FileNotFoundError("home.png not found")
            home_icon = Image.open(home_icon_path)
            home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
            self.home_img = ImageTk.PhotoImage(home_icon)
            home_btn = tk.Button(btn_frame, image=self.home_img, command=self.go_home,
                                 bg="#FFD700", borderwidth=0, activebackground="#FFD700")
            home_btn.pack(side="left", padx=10)
        except Exception as e:
            print("Home icon error:", e)


        self.status = tk.Label(root, text="", bg="#121212", fg="#ccc", font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", pady=10)

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0", padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            try:
                doc = fitz.open(self.file_path)
                self.total_pages = len(doc)
                self.info_label.config(text=f"Loaded: {os.path.basename(self.file_path)} ({self.total_pages} pages)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")

    def reorder_pdf(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return
        doc = fitz.open(self.file_path)
        order_input = simpledialog.askstring("New Page Order",
                                             f"Enter new order (1–{len(doc)}), e.g., 3,1,2 or 1-3,5:")
        if not order_input:
            return
        try:
            new_order = []
            for part in order_input.split(','):
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    new_order.extend(range(start - 1, end))
                else:
                    new_order.append(int(part) - 1)

            new_doc = fitz.open()
            for i in new_order:
                new_doc.insert_pdf(doc, from_page=i, to_page=i)

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("PDF Files", "*.pdf")],
                                                     title="Save Reordered PDF")
            if save_path:
                new_doc.save(save_path)
                self.status.config(text=f"Reordered PDF saved to: {save_path}")
                messagebox.showinfo("Success", f"Saved to:\n{save_path}")
            new_doc.close()
            doc.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_home(self):
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReorderApp(root)
    root.mainloop()
