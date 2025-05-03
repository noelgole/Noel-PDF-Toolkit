import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, ImageTk

class PDFDeletePagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noel's PDF Delete Tool")
        self.set_geometry(500, 550)
        self.root.configure(bg="#121212")

        # Set icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print("App icon error:", e)

        self.style = ttk.Style()
        self.set_dark_theme()

        tk.Label(root, text="Delete Pages from PDF", font=("Helvetica", 18, "bold"),
                 fg="#f0c040", bg="#121212").pack(pady=20)

        ttk.Button(root, text="Select PDF File", command=self.select_pdf).pack(pady=10)

        self.info_label = tk.Label(root, text="", bg="#121212", fg="white", font=("Arial", 10))
        self.info_label.pack()

        ttk.Button(root, text="Enter Pages to Delete", command=self.delete_pages).pack(pady=10)

        # Home & Close buttons
        btn_frame = tk.Frame(root, bg="#121212")
        btn_frame.pack(pady=20)

        try:
            home_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.png")
            if os.path.exists(home_icon_path):
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

        self.file_path = None

    def set_geometry(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def set_dark_theme(self):
        self.style.theme_use("default")
        self.style.configure("TButton", background="#333", foreground="#f0f0f0",
                             padding=6, font=("Arial", 10))
        self.style.map("TButton", background=[("active", "#5c0000")])

    def select_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            try:
                reader = PdfReader(self.file_path)
                total = len(reader.pages)
                self.info_label.config(text=f"Loaded: {os.path.basename(self.file_path)} ({total} pages)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read PDF: {e}")

    def parse_page_range(self, input_str, total_pages):
        pages_to_delete = set()
        try:
            parts = input_str.split(",")
            for part in parts:
                part = part.strip()
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    pages_to_delete.update(range(start - 1, end))
                else:
                    pages_to_delete.add(int(part) - 1)
            return sorted(p for p in pages_to_delete if 0 <= p < total_pages)
        except Exception:
            return None

    def delete_pages(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please select a PDF file first.")
            return

        try:
            reader = PdfReader(self.file_path)
            total_pages = len(reader.pages)

            input_str = simpledialog.askstring("Delete Pages",
                f"Enter page numbers to delete (1–{total_pages}), e.g., 2,4-6:")
            if not input_str:
                return

            pages_to_delete = self.parse_page_range(input_str, total_pages)
            if pages_to_delete is None:
                messagebox.showerror("Invalid Input", "Invalid page range format.")
                return

            writer = PdfWriter()
            for i in range(total_pages):
                if i not in pages_to_delete:
                    writer.add_page(reader.pages[i])

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     title="Save PDF After Deletion",
                                                     filetypes=[("PDF Files", "*.pdf")])
            if not save_path:
                return

            with open(save_path, "wb") as f:
                writer.write(f)

            self.status.config(text=f"Saved to: {save_path}")
            messagebox.showinfo("Success", f"Saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Page deletion failed:\n{str(e)}")

    def go_home(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFDeletePagesApp(root)
    root.mainloop()
